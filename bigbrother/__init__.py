__version__ = "0.1.3"

from typing import Callable, Dict, List, Set, Tuple, TypeVar

from .builtins import (
    _createObservedDict,
    _createObservedList,
    _createObservedSet,
    _ObservedDict,
    _ObservedList,
    _ObservedSet,
)
from .generic import _install_watcher_object

try:
    from pydantic import BaseModel

    from .libraries.pydantic import _install_watcher_pydantic

except ImportError:
    BaseModel = None


T = TypeVar("T")
Watcher = Callable[[T, str, T, Tuple, Dict], None]


def _install_watcher(obj: T, watcher: Watcher, recursive: bool = False) -> T:
    # Standard mutable containers: can't mutate their methods, so replace with an observed subclass.
    if isinstance(obj, List) and not isinstance(obj, _ObservedList):
        return _createObservedList(watcher, recursive=recursive, _install_watcher=_install_watcher)(obj)

    if isinstance(obj, Set) and not isinstance(obj, _ObservedSet):
        return _createObservedSet(watcher, recursive=recursive, _install_watcher=_install_watcher)(obj)

    if isinstance(obj, Dict) and not isinstance(obj, _ObservedDict):
        return _createObservedDict(watcher, recursive=recursive, _install_watcher=_install_watcher)(obj)

    # Pydantic models store their fields in __dict__; observe it.
    if BaseModel is not None and isinstance(obj, BaseModel):
        return _install_watcher_pydantic(obj=obj, watcher=watcher, recursive=recursive, _install_watcher=_install_watcher)

    # Generic objects (dataclasses, plain classes): swap the class for an observing subclass.
    return _install_watcher_object(obj, watcher, recursive, _install_watcher)


def watch(obj: T, watcher: Watcher, deepstate: bool = False) -> T:
    """Watch ``obj`` for mutation, invoking ``watcher(obj, method, ref, call_args, call_kwargs)``.

    With ``deepstate=True`` the watcher is installed recursively on nested containers and objects, so
    deep mutations (``obj.child.items.append(...)``) are reported too.
    """
    return _install_watcher(obj, watcher, recursive=deepstate)


__all__ = ["watch", "__version__"]
