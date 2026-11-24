# Class and Hierarchy Semantics

## Syntax

A record can assign a class after `$`:

```text
int] retries$network: 3
```

Dot-separated class segments represent hierarchy. Spaces around dots are
permitted by the active metadata and class normalization:

```text
int] retries$network . timeout: 3
```

This becomes nested dictionaries through `_lWalkObject`.

## Alias Syntax

The first class segment may be bracketed:

- `[name]` copies the class tuple recorded for `name`;
- `[nil]` copies the current `ClassPath`;
- `[name;suffix]` copies a positive prefix slice;
- `[name-suffix]` copies a negative prefix slice.

The alias may be followed by dotted continuation segments.

### Named aliases

For ordinary string item names, `_lConstruct` stores:

```text
ItemNameDatabase[name] = resolved_class_tuple
```

A later alias can retrieve that tuple. Forward aliases do not work retroactively.
Repeated names overwrite the database entry with the latest resolved tuple.

### `[nil]` aliases

`[nil]` uses `ClassPath` rather than `ItemNameDatabase`. This makes it a
current-path reference and not a reference to a record with the name `nil`.

### Positive semicolon splices

If the suffix is numeric, `_lResolveClassPath` uses `N + 1` as the exclusive
slice index. If the suffix is a word, `_dbPath.index(word) + 1` is used.

The selected prefix is followed by any dotted continuation segments in
`[name;suffix].continuation`.

### Negative hyphen splices

If the suffix is numeric, `_lResolveClassPath` uses `-N`.
If the suffix is a word, it uses `-_dbPath.index(word)`.
The implementation then applies `slice(0, index)`.

### Empty and failed alias paths

Unknown names receive `tuple()` from `ItemNameDatabase.get`.
Missing or invalid suffixes can make the splice fail. The broad exception sets
the resolved path to an empty class path.

## Empty Class

The `_ihMeta` splitter supplies `b''` when no `$class` is present.
`_lResolveClassPath` converts an unresolved or empty path to `''` and
`_lSetClassPath` leaves `ClassPath` at the empty path.

Records with no class interact with `ClassPath`; class semantics should be
tested carefully because `Node` is mutable closure state.

## Repeated Classes

The implementation compares normalized class tuples. Consecutive records with
the same normalized path reuse `Node`. A new normalized path walks from `Root`
and replaces `Node` with the corresponding nested dictionary.

## Repeated Names

Normal repeated names overwrite the existing dictionary entry. `nil` names are
the special counter case and do not overwrite.

## Ambiguity

The exact behavior of mixed class changes, repeated names, and an empty class
is implemented by closure state. Tests cover nested classes and `nil`, but do
not establish every possible interleaving.

Future changes to `ClassPath`, `_lResolveClassPath`, `_lWalkObject`, or
`_lCounter` need an explicit matrix of spaced and unspaced dots, consecutive
class records, class changes, and empty classes.

## Tuple-Key Construction Caveat

Direct probes of the current `ClassFactory` show tuple-valued class paths used
in result construction. An ordinary class can appear as `('network',)` in the
root keys, and a named alias can appear with nested tuple keys. This is not
treated as the intended public nested-dictionary shape in the maintenance
documentation; it is an observed defect to isolate and test.
