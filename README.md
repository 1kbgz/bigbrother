# bigbrother

Mutation callbacks for Python objects.

[![Build Status](https://github.com/1kbgz/bigbrother/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/1kbgz/bigbrother/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/1kbgz/bigbrother/branch/main/graph/badge.svg)](https://codecov.io/gh/1kbgz/bigbrother)
[![License](https://img.shields.io/github/license/1kbgz/bigbrother)](https://github.com/1kbgz/bigbrother)
[![PyPI](https://img.shields.io/pypi/v/bigbrother.svg)](https://pypi.python.org/pypi/bigbrother)

`bigbrother` watches mutable Python objects and calls your callback when they
change. It is useful when another layer needs to mark state dirty, schedule a
refresh, or react to model changes without replacing every mutation call.

## Install

```bash
pip install bigbrother
```

## Example

```python
from bigbrother import watch

changes = []


def track_change(obj, method, ref, call_args, call_kwargs):
    changes.append((method, call_args, call_kwargs))


state = watch({"items": []}, track_change, deepstate=True)
state["items"].append("alpha")

assert changes[-1] == ("append", ("alpha",), {})
```

Keep the object returned by `watch()`. Built-in containers are observed by
returning watched container instances.

## Supported Objects

`bigbrother` supports:

- `list`, `dict`, and `set`
- `pydantic.BaseModel`
- plain Python objects and dataclasses with a `__dict__`

Objects without a `__dict__`, such as slot-only classes, are returned unchanged.
Callbacks fire before the underlying mutation completes.

## Documentation

- [API reference](https://1kbgz.github.io/bigbrother/docs/src/api.html)

## Development

```bash
make develop
python -m pytest bigbrother/tests -q
```

## License

`bigbrother` is licensed under Apache-2.0.

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
