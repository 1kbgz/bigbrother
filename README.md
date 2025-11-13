# bigbrother

An evil, awful, terrible, no-good library for watching objects for mutation. Do not use this library.

[![Build Status](https://github.com/1kbgz/bigbrother/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/1kbgz/bigbrother/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/1kbgz/bigbrother/branch/main/graph/badge.svg)](https://codecov.io/gh/1kbgz/bigbrother)
[![License](https://img.shields.io/github/license/1kbgz/bigbrother)](https://github.com/1kbgz/bigbrother)
[![PyPI](https://img.shields.io/pypi/v/bigbrother.svg)](https://pypi.python.org/pypi/bigbrother)

## Overview

`bigbrother` is a mutation observer library. You can use it to watch your objects for changes. When your object changes, `bigbrother` will trigger your choice of callback.

```python
x = {1: "a", 2: "b", 3: "c"}

def track_changes(obj, method, ref, call_args, call_kwargs):
    print(f"method: {method}, args: {args}, kwargs: {kwargs}")

x = watch(x, track_changes)

x[1] = "x"

# prints: method: setitem, args: (1, 'x'), kwargs: {}
```

`bigbrother` can also embed itself recursively in your object by passing in argument `deepstate=True`.

## Callback

```python
def callback(obj, method, ref, call_args, call_kwargs):
    '''Callback called when object is mutated

    Args:
        obj (Any): The object being mutated via `method`
        method (str): The method called on the object (dunders removed)
        ref (Any): Reference object. If callback installed recursively, `ref` will be the entrypoint
        call_args (Tuple[Any]): Positional arguments that `method` was called with on `obj`
        call_kwargs (Dict[Any, Any]): Keyword arguments that `method` was called with on `obj`
    '''
```

## Supported types

### Builtins

Most builtin types are read-only and cannot have their method structure mutated, so we observe via replacement with thin wrappers.

- `list` via `_ObservedList`
  - `append`
  - `clear`
  - `extend`
  - `insert`
  - `pop`
  - `remove`
  - `sort`
  - `__setattr__`
  - `__setitem__`
- `dict` via `_ObservedDict`
  - `clear`
  - `pop`
  - `popitem`
  - `update`
  - `__setattr__`
  - `__setitem__`
- `set` via `_ObservedSet`
  - `add`
  - `clear`
  - `difference_update`
  - `discard`
  - `intersection_update`
  - `pop`
  - `remove`
  - `symmetric_difference_update`
  - `update`
  - `__setattr__`

### Libraries

- `pydantic.BaseModel`

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
