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
- `ItemNameDatabase`, mappings from ordinary string item names to the resolved
  class tuple for those records.

If `Root` is already a `frozendict`, `ClassFactory` converts it to `dict`
before construction.

The returned constructor processes records from `InternalPlumbing`.

## Class Changes

`_lResolveClassPath` normalizes the class string by splitting it on optional
spaces around dots. `_lResolveClassPath` compares the resulting tuple with
`ClassPath`; equal paths do not trigger a walk. A new path is resolved through
`_lWalkObject`, which starts from `Root` and creates or walks each segment.

## Named and Current-Path Aliases

`ItemNameDatabase` is a per-construction dictionary. `_lConstruct` registers
ordinary string item names after resolving both `_name` and `_class`.
The value stored is the resolved class tuple, not the original class text.
`nil` item names are not registered as database keys.

`[nil]` uses `ClassPath` directly. A named alias uses
`ItemNameDatabase.get(name, tuple())`. Alias lookup is sequential and the
database is not searched backward or forward outside the records already
processed.

## Alias Splices

`_lResolveClassPath` strips the brackets and splits the alias at `;` or `-`
using `split(r'[;-]', ..., maxsplit=1)`.

For `;suffix`:

- numeric suffix `N` becomes `slice(0, N + 1)`;
- word suffix becomes `slice(0, index(word) + 1)`.

For `-suffix`:

- numeric suffix `N` becomes `slice(0, -N)`;
- word suffix becomes `slice(0, -index(word))`.

The selected tuple slice is concatenated with additional dotted segments from
the original class path.

## Alias Failure

The entire lookup/splice block is guarded by a broad `except`. It converts
lookup or splice errors to an empty class path rather than preserving a partial
result or reporting the failure. `_lSetClassPath` then sets `ClassPath` to the
empty path or leaves construction at the root.

## Item Names

Normal names are decoded and used as dictionary keys. The special name `nil`
does not become a key. `_lResolveItemName` returns an incrementing integer
for each `nil` item in the active class.

Counters are stored per class. This allows repeated `nil` entries to become
numeric positions in a class-specific list-like mapping.

## Construction Caveat

Direct source probes show ordinary tuple class paths can currently appear as
tuple keys instead of nested string keys. Alias tuple reuse can also create
nested tuple keys. This is a source-observed result of `ClassPath`,
`ItemNameDatabase`, `_lSetClassPath`, and `_lWalkObject` interacting, and is
documented as technical debt rather than stable public behavior.

## Freezing

By default `loads` calls `frozendict(Root)` after construction. `freeze=False`
returns the mutable root dictionary.

`loadsarray` and `loadsiter` use separate freeze parameters. `loadsarray`
freezes to a tuple by default. `loadsiter` is not frozen by default and yields
its generator expression directly.
