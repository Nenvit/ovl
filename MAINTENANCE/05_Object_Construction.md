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
- `_LastClass`, the previously active class;
- `ClassCounterDatabase`, counters for `nil` names.

The returned constructor processes records from `InternalPlumbing`.

## Class Changes

When `_lRegisterSubClass` sees a new class, it splits the class at dots and
walks or creates nested dictionaries in `Root`.

The implementation intentionally retains the last registered class. Consecutive
records with the same class reuse `Node`; a class change recreates the current
walk position.

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
