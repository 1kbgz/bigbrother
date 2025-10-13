from typing import Any, Callable

from pydantic import BaseModel

from ..common import _partial

# def _install_watcher_pydantic_field(field, watcher: Callable[[BaseModel, str, Any], None], recursive: bool, _install_watcher: Callable):
#     if field.default_factory and not hasattr(field.default_factory, "is_bigbrother_field_factory"):
#         field.default_factory = lambda default_factory=field.default_factory: _install_watcher(default_factory(), watcher=watcher, recursive=recursive)
#         field.default_factory.is_bigbrother_field_factory = True
#     elif field.default:
#         field.default = _install_watcher(field.default, watcher, recursive=recursive)
#     return field


def _install_watcher_pydantic(
    obj: BaseModel, watcher: Callable[[BaseModel, str, Any], None], recursive: bool, _install_watcher: Callable
) -> BaseModel:
    # Library types
    # Pydantic object
    if BaseModel and isinstance(obj, BaseModel):
        if recursive:
            # TODO can't really mutate the class
            # iterate through fields converting them
            # for name, field in obj.__fields__.items():
            #     obj.__fields__[name] = _install_watcher_pydantic_field(field=field, watcher=watcher, recursive=recursive, _install_watcher=_install_watcher)
            # TODO but don't want to do this on the dict either
            # for key, value in obj.__dict__.items():
            #     obj.__dict__[key] = _install_watcher(value, watcher, recursive=recursive)
            ...
        # replace dict with watched version
        object.__setattr__(obj, "__dict__", _install_watcher(obj.__dict__, watcher=_partial(watcher, ref=obj), recursive=recursive))
        return obj
