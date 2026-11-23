# Object Construction

## Initial Root

`loads` creates a root dictionary by copying `dict(update)`. The default
`update={}` is not mutated directly because the class factory receives
`dict(update)`.

`dict(update)` can be passed a dictionary, or another object accepted by
`dict`. The public README focuses on dictionary updates.

## `ClassFactory`

`ClassFactory` closes over:

- `Root`, the initial root dictionary;
- `Node`, the current nested dictionary;
- `ClassPath`, the normalized tuple of active class segments;
- `ClassCounterDatabase`, counters keyed by class path for `nil` names.

If `Root` is already a `frozendict`, `ClassFactory` converts it to `dict`
before construction.

The returned constructor processes records from `InternalPlumbing`.

## Class Changes

`_lResolveClassPath` normalizes the class string by splitting it on optional
spaces around dots. `_lResolveClassPath` compares the resulting tuple with
`ClassPath`; equal paths do not trigger a walk. A new path is resolved through
`_lWalkObject`, which starts from `Root` and creates or walks each segment.

## Item Names

Normal names are decoded and used as dictionary keys. The special name `nil`
does not become a key. `_lRegisterItemName` returns an incrementing integer
for each `nil` item in the active class.

Counters are stored per class. This allows repeated `nil` entries to become
numeric positions in a class-specific list-like mapping.

## Freezing

By default `loads` calls `frozendict(Root)` after construction. `freeze=False`
returns the mutable root dictionary.

`loadsarray` and `loadsiter` use separate freeze parameters. `loadsarray`
freezes to a tuple by default. `loadsiter` is not frozen by default and yields
its generator expression directly.
