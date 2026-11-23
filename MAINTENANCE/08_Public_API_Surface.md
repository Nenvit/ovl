# Public API Surface

The package exports `loads`, `loadsarray`, and `loadsiter` from
`src/ovl/__init__.py`.

## `loads`

```python
loads(o: str | Path, update: DictLike = {}, freeze: bool = True) -> DictLike
```

The public README states that `update` supplies initial values and `freeze`
controls immutable or mutable output.

The implementation creates a copy with `dict(update)`, constructs the root,
and wraps it in `frozendict` when frozen.

## `loadsarray`

```python
loadsarray(o: str | Path, freeze: bool = True) -> tuple[Any] | list[Any]
```

It preserves file order. The frozen default is a tuple; `freeze=False` returns
a list.

## `loadsiter`

```python
loadsiter(
    o: str | Path,
    keys: bool = True,
    freeze: bool = False,
) -> Generator[Any] | Iterator[Any]
```

With `keys=True`, each yield contains class, name, and evaluated data.
With `keys=False`, only evaluated data is yielded.

The implementation's `freeze` parameter chooses `iter(...)` or an identity
function around the generator expression. The public README describes key and
value behavior; tests cover both key modes.

## Input Types

The public signatures accept `str | pathlib.Path` conceptually. Internally,
loader functions pass input to `Path(o)`.

## Compatibility Boundary

The current repository contains no compatibility golf-loader module. Deleted
source and package entries are not active public behavior. The README also
documents no compatibility loader.
