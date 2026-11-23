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

## Empty Class

The `_ihMeta` splitter supplies `b''` when no `$class` is present.
`_lResolveClassPath` converts an empty path to `('',)` and `_lWalkObject`
does not create a node for it.

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
