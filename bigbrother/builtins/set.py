from typing import Any, Callable, Set, Type

from ..common import _partial


class _ObservedSet(Set):
    _watcher: Callable[["_ObservedSet", str, Any], None]
    _recursive: bool
    _install_watcher: Callable
    _watcher_ready: bool

    def __init__(self, set: Set):
        super().__init__(set)
        object.__setattr__(self, "_watcher_ready", False)
        if self._recursive:
            # install watcher on all items
            # just defer to my own add
            x = list(self)
            self.clear()
            for i in x:
                self.add(x)
        object.__setattr__(self, "_watcher_ready", True)

    def _notify_watcher(self, method, *args, **kwargs):
        if self._watcher_ready:
            self.__class__._watcher(self, method, self, args, kwargs)

    def add(self, __element: Any):
        self._notify_watcher("add", __element)
        if self._recursive:
            __element = self.__class__._install_watcher(__element, watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive)
        return super().add(__element)

    def clear(self, *args, **kwargs):
        self._notify_watcher("clear", *args, **kwargs)
        return super().clear(*args, **kwargs)

    def difference_update(self, *args, **kwargs):
        self._notify_watcher("difference_update", *args, **kwargs)
        # TODO install watcher on items
        return super().difference_update(*args, **kwargs)

    def discard(self, *args, **kwargs):
        self._notify_watcher("discard", *args, **kwargs)
        return super().discard(*args, **kwargs)

    def intersection_update(self, *args, **kwargs):
        self._notify_watcher("intersection_update", *args, **kwargs)
        # TODO install watcher on items
        return super().intersection_update(*args, **kwargs)

    def pop(self, *args, **kwargs):
        self._notify_watcher("pop", *args, **kwargs)
        return super().pop(*args, **kwargs)

    def remove(self, *args, **kwargs):
        self._notify_watcher("remove", *args, **kwargs)
        return super().remove(*args, **kwargs)

    def symmetric_difference_update(self, *args, **kwargs):
        self._notify_watcher("symmetric_difference_update", *args, **kwargs)
        # TODO install watcher on items
        return super().symmetric_difference_update(*args, **kwargs)

    def update(self, *args):
        self._notify_watcher("update", *args)
        s = set(*args)
        if self._recursive:
            s = self._install_watcher(s, watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive)
        return super().update(s)

    def __setattr__(self, *args, **kwargs):
        self._notify_watcher("setattr", *args, **kwargs)
        return super().__setattr__(*args, **kwargs)


def _create(watcher: Callable[[_ObservedSet, str, Any], None], recursive: bool, _install_watcher: Callable) -> Type[_ObservedSet]:
    return type(
        "_ObservedSet", (_ObservedSet,), {"_watcher": watcher, "_recursive": recursive, "_install_watcher": _install_watcher, "_watcher_ready": False}
    )
