__version__ = "0.1.3"

from types import MethodType
from typing import Any, Callable, Dict, List, Set, Tuple, TypeVar

from .builtins import (
    _createObservedDict,
    _createObservedList,
    _createObservedSet,
    _ObservedDict,
    _ObservedList,
    _ObservedSet,
)
from .generic import _replacement_setattr, _replacement_setitem

try:
    from pydantic import BaseModel

    from .libraries.pydantic import _install_watcher_pydantic

except ImportError:
    BaseModel = None


T = TypeVar("T")


def _partial(watcher, obj):
    def _watcher_wrapper(*args, **kwargs):
        if args:
            args = args[1:]
        if kwargs:
            kwargs.pop("obj", None)
            kwargs.pop("self", None)
        return watcher(obj, *args, **kwargs)

    return _watcher_wrapper


def _install_watcher(obj: T, watcher: Callable[[T, str, T, Tuple, Dict], None], recursive: bool = False) -> T:
    # Standard mutable types
    if isinstance(obj, List) and not isinstance(obj, _ObservedList):
        # can't mutate list so replace with watcher variant
        return _createObservedList(watcher, recursive=recursive, _install_watcher=_install_watcher)(obj)

    if isinstance(obj, Set) and not isinstance(obj, _ObservedSet):
        return _createObservedSet(watcher, recursive=recursive, _install_watcher=_install_watcher)(obj)

    if isinstance(obj, Dict) and not isinstance(obj, _ObservedDict):
        return _createObservedDict(watcher, recursive=recursive, _install_watcher=_install_watcher)(obj)

    # Library types
    # Pydantic object
    if BaseModel and isinstance(obj, BaseModel):
        return _install_watcher_pydantic(obj=obj, watcher=watcher, recursive=recursive, _install_watcher=_install_watcher)

    # Pydantic class
    # TODO

    # Others
    try:
        if hasattr(obj, "__setitem__"):
            object.__setattr__(obj, "__setitem__", MethodType(_replacement_setitem, obj))
    except AttributeError:
        # Ignore
        pass

    try:
        if hasattr(obj, "__setattr__"):
            object.__setattr__(obj, "__setattr__", MethodType(_replacement_setattr, obj))
    except AttributeError:
        # Ignore
        pass

    return obj


def watch(obj: T, watcher: Callable[[T, str, T, Tuple, Dict], None], deepstate: bool = False) -> T:
    return _install_watcher(obj, watcher, recursive=deepstate)


__all__ = ["watch", "__version__"]
