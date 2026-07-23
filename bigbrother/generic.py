"""Observe plain objects (e.g. dataclasses) that keep their state in ``__dict__``.

``object.__setattr__`` writes to the instance dict at the C level, *bypassing* a dict subclass's
``__setitem__`` — so the ``__dict__``-swap trick used for pydantic (whose ``__setattr__`` does a
Python-level ``dict[name] = value``) does not catch attribute assignment on ordinary objects.
Instead we swap the instance's class for a thin subclass whose ``__setattr__`` notifies the watcher.
Objects without a ``__dict__`` (``__slots__``, e.g. ``msgspec.Struct``), or objects that reject
``__class__`` assignment, can't be observed this way and are returned unchanged.
"""

from collections.abc import Callable

from .common import _partial


def _observed_class_for(cls: type, watcher: Callable) -> type:
    base_setattr = cls.__setattr__

    def _setattr(self, name, value):
        watcher(self, "setattr", self, (name, value), {})
        base_setattr(self, name, value)

    return type(cls.__name__, (cls,), {"__setattr__": _setattr, "_bigbrother_observed": True})


def _install_watcher_object(obj, watcher: Callable, recursive: bool, _install_watcher: Callable):
    obj_dict = getattr(obj, "__dict__", None)
    if not isinstance(obj_dict, dict):
        return obj  # no __dict__ (e.g. __slots__): cannot observe
    if getattr(type(obj), "_bigbrother_observed", False):
        return obj  # already observed
    try:
        object.__setattr__(obj, "__class__", _observed_class_for(type(obj), watcher))
    except TypeError:
        return obj
    if recursive:
        for key, value in list(obj_dict.items()):
            # write through the base setattr so installing doesn't itself notify
            object.__setattr__(obj, key, _install_watcher(value, _partial(watcher, ref=obj), recursive=True))
    return obj
