# deserializer.py
import functools
import time
from dataclasses import is_dataclass
from typing import (
    Any, Callable, Optional, Type, TypeVar, List, get_args, get_origin, overload
)

from core.web.services.core.contracts.response import IResponse
from core.web.services.core.json import JsonObject
from core.utilities.data.strings import convert_object_keys_to_snake
from core.utilities.logging.custom_logger import create_logger

T = TypeVar("T")  # DTO type
R = TypeVar("R")  # raw response type

# ---------- Overload stubs (for IDE/type checkers) ----------
@overload
def deserialized(
    type_hook: Type[T],
    child: str | None = ...,
    wait: float | None = ...,
    many: bool | None = ...,
) -> Callable[[Callable[..., R]], Callable[..., T]]: ...
@overload
def deserialized(
    type_hook: list[T],
    child: str | None = ...,
    wait: float | None = ...,
    many: bool | None = ...,
) -> Callable[[Callable[..., R]], Callable[..., list[T]]]: ...
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
        if hasattr(container, key):
            return getattr(container, key)
        if isinstance(container, dict):
            return container[key]
        raise KeyError(f"Child '{key}' not found in response data.")

    def _construct_one(d: Any, cls: Type[Any]) -> Any:
        d = _to_dict(d)
        if isinstance(d, JsonObject):
            d = dict(d)
        if not isinstance(d, dict):
            if isinstance(d, cls):
                return d
            raise TypeError(f"Cannot construct {cls.__name__} from non-dict: {type(d)}")
        if is_dataclass(cls):
            return cls(**d)
        if hasattr(cls, "from_dict") and callable(getattr(cls, "from_dict")):
            return cls.from_dict(d)
        return cls(**d)

    def _coerce(value: Any, hook: Type[Any], *, force_many: Optional[bool]) -> Any:
        # dict passthrough (snake-cased)
        if hook is dict:
            return convert_object_keys_to_snake(_to_dict(value))

        # If user passed list[DTO], honor it
        elem = _list_item_type(hook)
        if elem is not None:
            seq = value if not isinstance(value, JsonObject) else list(value)
            if not isinstance(seq, list):
                raise TypeError(f"Expected list payload for {hook}, got {type(seq)}")
            return [_construct_one(item, elem) for item in seq]

        # Hook is DTO class; decide many/single
        if force_many is True:
            seq = value if not isinstance(value, JsonObject) else list(value)
            if not isinstance(seq, list):
                raise TypeError(f"Expected list payload for many=True, got {type(seq)}")
            return [_construct_one(item, hook) for item in seq]

        if force_many is False:
            return _construct_one(value, hook)

        # Auto-infer from runtime payload
        payload = value if not isinstance(value, JsonObject) else list(value)
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
