# API Reference

## `watch`

```python
watch(obj, watcher, deepstate=False)
```

Watches `obj` for mutation.

### Parameters

| Name        | Type                                       | Description                                                                                |
| ----------- | ------------------------------------------ | ------------------------------------------------------------------------------------------ |
| `obj`       | `T`                                        | Object to watch.                                                                           |
| `watcher`   | `Callable[[T, str, T, Tuple, Dict], None]` | Callback called when a watched mutation occurs.                                            |
| `deepstate` | `bool`                                     | When `True`, installs watchers on nested values reachable from `obj`. Defaults to `False`. |

### Returns

The watched object.

For built-in containers, the return value is a watched container initialized
with the contents of `obj`. For pydantic models, plain objects, and dataclasses,
the return value is the original object when observation succeeds. Objects
without a `__dict__` are returned unchanged.

## Callback

```python
def watcher(obj, method, ref, call_args, call_kwargs):
    ...
```

| Name          | Type    | Description                                                                                                                |
| ------------- | ------- | -------------------------------------------------------------------------------------------------------------------------- |
| `obj`         | `Any`   | Watched object receiving the mutation. For pydantic field assignment, this is the model field dictionary.                  |
| `method`      | `str`   | Mutating method name, without leading or trailing double underscores.                                                      |
| `ref`         | `Any`   | Watched entry point. For nested mutations with `deepstate=True`, this remains the object originally watched at that level. |
| `call_args`   | `tuple` | Positional arguments passed to the mutating method.                                                                        |
| `call_kwargs` | `dict`  | Keyword arguments passed to the mutating method.                                                                           |

The callback is called before the underlying mutation completes. Its return
value is ignored. Exceptions raised by the callback propagate to the caller.

## Supported Mutations

### `list`

| Mutation               | Reported `method` |
| ---------------------- | ----------------- |
| `append(value)`        | `append`          |
| `clear()`              | `clear`           |
| `extend(iterable)`     | `extend`          |
| `insert(index, value)` | `insert`          |
| `pop(...)`             | `pop`             |
| `remove(value)`        | `remove`          |
| `sort(...)`            | `sort`            |
| `obj[index] = value`   | `setitem`         |
| `obj.name = value`     | `setattr`         |

### `dict`

| Mutation                    | Reported `method` |
| --------------------------- | ----------------- |
| `clear()`                   | `clear`           |
| `pop(...)`                  | `pop`             |
| `popitem()`                 | `popitem`         |
| `update(mapping, **kwargs)` | `update`          |
| `obj[key] = value`          | `setitem`         |
| `obj.name = value`          | `setattr`         |

### `set`

| Mutation                           | Reported `method`             |
| ---------------------------------- | ----------------------------- |
| `add(value)`                       | `add`                         |
| `clear()`                          | `clear`                       |
| `difference_update(...)`           | `difference_update`           |
| `discard(value)`                   | `discard`                     |
| `intersection_update(...)`         | `intersection_update`         |
| `pop()`                            | `pop`                         |
| `remove(value)`                    | `remove`                      |
| `symmetric_difference_update(...)` | `symmetric_difference_update` |
| `update(...)`                      | `update`                      |
| `obj.name = value`                 | `setattr`                     |

### `pydantic.BaseModel`

Field assignment is reported as `setitem` because pydantic stores field values
in the model field dictionary.

With `deepstate=True`, nested pydantic models and nested mutable containers are
watched when they are reachable from the watched model.

### Plain Objects And Dataclasses

Attribute assignment is reported as `setattr`.

With `deepstate=True`, nested values present during installation are watched.
Objects without a `__dict__` are returned unchanged.
