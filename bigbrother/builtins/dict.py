from typing import Any, Callable, Dict, Type

from ..common import _partial


class _ObservedDict(Dict):
    _watcher: Callable[["_ObservedDict", str, Any], None]
    _recursive: bool
    _install_watcher: Callable
    _watcher_ready: bool

    def __init__(self, dict: Dict):
        super().__init__(dict)
        object.__setattr__(self, "_watcher_ready", False)
        if self.__class__._recursive:
            # install watcher on all items
            # just defer to my own __setitem__, but without the watcher
            for i, item in self.items():
                self[i] = item
        object.__setattr__(self, "_watcher_ready", True)

    def _notify_watcher(self, method, *args, **kwargs):
        if self._watcher_ready:
            self.__class__._watcher(self, method, self, args, kwargs)

    def clear(self, *args, **kwargs):
        self._notify_watcher("clear", *args, **kwargs)
        return super().clear(*args, **kwargs)

    def pop(self, *args, **kwargs):
        self._notify_watcher("pop", *args, **kwargs)
        return super().pop(*args, **kwargs)

    def popitem(self, *args, **kwargs):
        self._notify_watcher("popitem", *args, **kwargs)
        return super().popitem(*args, **kwargs)

    def update(self, __m, **kwargs):
        other = dict(__m, **kwargs)
        if self.__class__._recursive:
            other = self.__class__._install_watcher(other, watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive)
        self._notify_watcher("update", other)
        return super().update(other)

    def __setattr__(self, *args, **kwargs):
        self._notify_watcher("setattr", *args, **kwargs)
        return super().__setattr__(*args, **kwargs)

    def __setitem__(self, __key, __value):
        if self._recursive:
            __key = self.__class__._install_watcher(__key, watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive)
            __value = self.__class__._install_watcher(__value, watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive)
        self._notify_watcher("setitem", __key, __value)
        return super().__setitem__(__key, __value)


def _create(watcher: Callable[[_ObservedDict, str, Any], None], recursive: bool, _install_watcher: Callable) -> Type[_ObservedDict]:
    return type(
        "_ObservedDict",
        (_ObservedDict,),
        {"_watcher": watcher, "_recursive": recursive, "_install_watcher": _install_watcher, "_watcher_ready": False},
    )
