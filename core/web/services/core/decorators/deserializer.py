# deserializer.py
import functools
import time
import inspect

from dataclasses import is_dataclass
from dataclasses import fields as dc_fields

from typing import (
    Any, Callable, Optional, Type, TypeVar, List, get_args, get_origin, overload, Literal, Union
)

from core.web.services.core.contracts.response import IResponse
from core.web.services.core.json import JsonObject
from core.utilities.data.strings import convert_object_keys_to_snake
from core.utilities.logging.custom_logger import create_logger


T = TypeVar("T")  # DTO type
R = TypeVar("R")  # raw response type

# 1) Single DTO type, force list via many=True
@overload
def deserialized(
    type_hook: Type[T],
    child: str | None = ...,
    wait: float | None = ...,
    many: Literal[True] = ...,
) -> Callable[[Callable[..., R]], Callable[..., list[T]]]: ...

# 2) Single DTO type, force single via many=False
@overload
def deserialized(
    type_hook: Type[T],
    child: str | None = ...,
    wait: float | None = ...,
    many: Literal[False] = ...,
) -> Callable[[Callable[..., R]], Callable[..., T]]: ...

# 3) Single DTO type, many unspecified -> could be T or list[T]
@overload
def deserialized(
    type_hook: Type[T],
    child: str | None = ...,
    wait: float | None = ...,
    many: None = ...,
) -> Callable[[Callable[..., R]], Callable[..., Union[T, list[T]]]]: ...

# 4) list[DTO] type explicitly -> list[T]
@overload
def deserialized(
    type_hook: list[T],
    child: str | None = ...,
    wait: float | None = ...,
    many: bool | None = ...,
) -> Callable[[Callable[..., R]], Callable[..., list[T]]]: ...

# 5) dict case (returns dict; you could widen to Union[dict, list[dict]] if you want)
@overload
def deserialized(
    type_hook: Type[dict],
    child: str | None = ...,
    wait: float | None = ...,
    many: bool | None = ...,
) -> Callable[[Callable[..., R]], Callable[..., dict]]: ...

# ---------- Runtime implementation ----------
def deserialized(
    type_hook: Type[Any] | Any,
    child: Optional[str] = None,
    wait: Optional[float] = None,
    many: Optional[bool] = None,
) -> Callable[[Callable[..., R]], Callable[..., Any]]:
    """
    Deserialize a response into DTO(s) when return_data_only is True; otherwise return the raw response.
    """

    def _is_list_type(tp: Any) -> bool:
        return get_origin(tp) in (list, List)

    def _list_item_type(tp: Any) -> Optional[Type[Any]]:
        if not _is_list_type(tp):
            return None
        args = get_args(tp)
        return args[0] if args else None

    def _to_dict(obj: Any) -> Any:
        return dict(obj) if isinstance(obj, JsonObject) else obj

    def _access_child(container: Any, key: Optional[str]) -> Any:
        if not key:
            return container

        cur = container
        for part in key.split('.'):
            # list index (e.g., "0")
            if isinstance(cur, list) and part.isdigit():
                idx = int(part)
                cur = cur[idx]
                continue

            # dict lookup
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
                continue

            # attribute access (rare)
            if hasattr(cur, part):
                cur = getattr(cur, part)
                continue

            raise KeyError(f"Child path '{key}' not found in response data.")
        return cur

    def _construct_one(d: Any, cls: Type[Any]) -> Any:
        # Normalize JsonObject → dict
        d = _to_dict(d)
        if isinstance(d, JsonObject):
            d = dict(d)

        # If it's already the right instance, just return it
        if not isinstance(d, dict):
            if isinstance(d, cls):
                return d
            raise TypeError(f"Cannot construct {cls.__name__} from non-dict: {type(d)}")

        # 1) If DTO exposes from_dict, use it (lets the DTO own mapping/validation)
        if hasattr(cls, "from_dict") and callable(getattr(cls, "from_dict")):
            return cls.from_dict(d)

        # 2) Dataclass: filter to declared field names
        if is_dataclass(cls):
            field_names = {f.name for f in dc_fields(cls)}
            filtered = {k: v for k, v in d.items() if k in field_names}
            return cls(**filtered)

        # 3) Generic class: filter using __init__ signature
        try:
            sig = inspect.signature(cls)  # usually __init__ of the class
            param_names = {
                name for name, p in sig.parameters.items()
                if name != "self" and p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
            }
            # If **kwargs is accepted, we can pass all
            accepts_kwargs = any(p.kind == p.VAR_KEYWORD for p in sig.parameters.values())
            filtered = d if accepts_kwargs else {k: v for k, v in d.items() if k in param_names}
            return cls(**filtered)
        except Exception:
            # Last resort: try full dict (may still fail, but keeps prior behavior)
            return cls(**d)

    def _as_sequence(x: Any) -> Any:
        x = _to_dict(x)
        if isinstance(x, dict) and "data" in x and isinstance(x["data"], list):
            return x["data"]
        return x

    def _coerce(value: Any, hook: Type[Any], *, force_many: Optional[bool]) -> Any:
        # dict passthrough (optionally snake-cased)
        if hook is dict:
            # If it's a JsonObject, let convert_object_keys_to_snake handle it
            if isinstance(value, JsonObject):
                return convert_object_keys_to_snake(value)

            # Otherwise just normalize to a plain dict and return as-is
            v = _to_dict(value)
            if isinstance(v, JsonObject):
                v = dict(v)
            return v

        # If user passed list[DTO], honor it
        elem = _list_item_type(hook)
        if elem is not None:
            seq = _as_sequence(value)
            if not isinstance(seq, list):
                raise TypeError(f"Expected list payload for {hook}, got {type(seq)}")
            return [_construct_one(item, elem) for item in seq]

        # Hook is DTO class; decide many/single
        if force_many is True:
            seq = _as_sequence(value)
            if not isinstance(seq, list):
                raise TypeError(f"Expected list payload for many=True, got {type(seq)}")
            return [_construct_one(item, hook) for item in seq]

        if force_many is False:
            return _construct_one(_to_dict(value), hook)

        # Auto-infer from runtime payload
        payload = _as_sequence(value)
        if isinstance(payload, list):
            return [_construct_one(item, hook) for item in payload]
        return _construct_one(payload, hook)

    def decorator(func: Callable[..., R]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            log = create_logger("JSON Deserialization decorator")

            if wait is not None:
                time.sleep(wait)

            response_instance: IResponse = func(self, *args, **kwargs)

            # Accept either self.config.return_data_only or self._config.return_data_only
            cfg = getattr(self, "config", None) or getattr(self, "_config", None)
            if getattr(cfg, "return_data_only", False):
                try:
                    data = response_instance.data
                    data = _access_child(data, child)
                    return _coerce(data, type_hook, force_many=many)
                except Exception as e:
                    log.warning(
                        "Cannot deserialize into requested type. "
                        "Returning full response. ERROR: %s", e
                    )
                    return response_instance

            return response_instance

        return wrapper

    return decorator
