from typing import Any, Callable, List, Type

from ..common import _partial


class _ObservedList(List):
    _watcher: Callable[["_ObservedList", str, Any], None]
    _recursive: bool
    _install_watcher: Callable
    _watcher_ready: bool

    def __init__(self, list: List):
        super().__init__(list)
        object.__setattr__(self, "_watcher_ready", False)
        if self.__class__._recursive:
            # install watcher on all items
            # just defer to my own __setitem__
            for i, item in enumerate(self):
                self[i] = item
        object.__setattr__(self, "_watcher_ready", True)

    def _notify_watcher(self, method, *args, **kwargs):
        if self._watcher_ready:
            self.__class__._watcher(self, method, self, args, kwargs)

    def append(self, __object: Any):
        self._notify_watcher("append", __object)
        if self._recursive:
            __object = self.__class__._install_watcher(__object, watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive)
        return super().append(__object)

    def clear(self, *args, **kwargs):
        self._notify_watcher("clear", *args, **kwargs)
        return super().clear(*args, **kwargs)

    def extend(self, __iterable):
        self._notify_watcher("extend", __iterable)
        if self._recursive:
            __iterable = self.__class__._install_watcher(
                list(__iterable), watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive
            )
        return super().extend(__iterable)

    def insert(self, __key: int, __value: Any):
        self._notify_watcher("insert", __key, __value)
        if self._recursive:
            __value = self.__class__._install_watcher(__value, watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive)
        return super().insert(__key, __value)

    def pop(self, *args, **kwargs):
        self._notify_watcher("pop", *args, **kwargs)
        return super().pop(*args, **kwargs)

    def remove(self, *args, **kwargs):
        self._notify_watcher("remove", *args, **kwargs)
        return super().remove(*args, **kwargs)

    def sort(self, *args, **kwargs):
        self._notify_watcher("sort", *args, **kwargs)
        return super().sort(*args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        self._notify_watcher("setattr", *args, **kwargs)
        return super().__setattr__(*args, **kwargs)

    def __setitem__(self, __key: int, __value: Any):
        self._notify_watcher("setitem", __key, __value)
        if self._recursive:
            __value = self.__class__._install_watcher(__value, watcher=_partial(self.__class__._watcher, ref=self), recursive=self._recursive)
        return super().__setitem__(__key, __value)


def _create(watcher: Callable[[_ObservedList, str, Any], None], recursive: bool, _install_watcher: Callable) -> Type[_ObservedList]:
    return type(
        "_ObservedList",
        (_ObservedList,),
        {"_watcher": watcher, "_recursive": recursive, "_install_watcher": _install_watcher, "_watcher_ready": False},
    )
