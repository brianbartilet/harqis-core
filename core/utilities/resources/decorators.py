import functools
from typing import Any, Dict

def get_decorator_attrs(fn, prefix: str = "_hud_") -> Dict[str, Any]:
    """
    Walk the decorator chain and collect all attributes that look like
    decorator parameters (e.g. _hud_item_name, _hud_config, ...).

    - If `fn` is a Celery Task, start from `fn.run`.
    - Only attributes starting with `prefix` are included.
    """
    collected: Dict[str, Any] = {}

    # If this is a Celery Task, the actual callable is on .run
    cur = getattr(fn, "run", fn)

    visited = set()
    while cur is not None and cur not in visited:
        visited.add(cur)

        for attr in dir(cur):
            if not attr.startswith(prefix):
                continue
            if attr in collected:
                continue
            try:
                value = getattr(cur, attr)
            except AttributeError:
                continue
            collected[attr] = value

        # Walk down the decorator chain via functools.wraps
        cur = getattr(cur, "__wrapped__", None)

    return collected
