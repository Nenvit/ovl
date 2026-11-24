# Architecture

## Module Boundaries

The package has a small two-layer implementation:

1. `src/ovl/utils/loaders.py` defines the public operations.
2. `src/ovl/utils/__internals.py` implements parsing and conversion.

`src/ovl/__init__.py` re-exports the public functions and sets `__all__`.

## Loader Call Flow

### `loads`

`loads`:

1. copies or accepts an update dictionary;
2. creates `Root` and a `_lConstruct` closure through `ClassFactory`;
3. validates and converts `Path(o)` through `InternalPlumbing`;
4. optionally wraps the result in `frozendict`;
5. returns the mutable root dictionary when `freeze=False`.

### `loadsarray`

`loadsarray` calls `InternalPlumbing`, dispatches every record type, and wraps
the resulting values in a tuple or list.

### `loadsiter`

`loadsiter` is a generator expression over `InternalPlumbing`. With `keys=True`,
it yields class, name, and value; with `keys=False`, it yields only values.
The default `freeze=False` means it returns the generator expression itself
rather than an iterator wrapper, in the implementation currently present.

## Byte and Text Boundaries

Path validation and source reading operate on `Path` objects and binary lines.
The parser maintains buffered `bytes`. Metadata and values are separated with
byte delimiters. Dispatch conversion receives either:

- decoded text, when `toString=True`; or
- raw bytes, when `toString=False`.

This boundary is important because dispatch implementations do not all accept
the same representation.

## Broad-Effect Areas

Changes to `META_REGEXP`, `_ihBlobber`, `_ihMeta`, `TypeLibraryDispatch`, or
`ClassFactory` can affect all three public loaders. `loaders.py` is small, while
these internals centralize most behavior.

`ClassFactory` now has an alias-sensitive state model: `ClassPath`,
`ItemNameDatabase`, and `ClassCounterDatabase` are used before a record is
stored. Alias changes affect `_lResolveClassPath`, `_lSetClassPath`,
`_lWalkObject`, `_lResolveItemName`, and `_lConstruct` together.
