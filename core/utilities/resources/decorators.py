import functools
from typing import Any, Dict


def get_decorator_attrs(fn) -> Dict[str, Any]:
    """
    Walk the decorator chain via __wrapped__ and collect
    all attributes attached to decorators (e.g. _hud_item_name).

    Returns:
        A dict mapping attribute_name -> value
    """

    collected = {}
    cur = fn

    while cur is not None:
        # Collect all custom attrs (non-dunder, non-callable, non-function attributes)
        for attr in dir(cur):
            if attr.startswith("__"):
                continue  # skip dunders
            if attr in collected:
                continue  # do not overwrite earlier values
            try:
                value = getattr(cur, attr)
            except AttributeError:
                continue
            # Keep only non-callable decorator metadata
            # (func code, closures, and methods are excluded)
            if not callable(value):
                collected[attr] = value

        # Walk to next wrapped level
        cur = getattr(cur, "__wrapped__", None)

    return collected
