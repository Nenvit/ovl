# Class and Hierarchy Semantics

## Syntax

A record can assign a class after `$`:

```text
int] retries$network: 3
```

Dot-separated class segments represent hierarchy:

```text
int] retries$network.timeout: 3
```

This becomes nested dictionaries through `_lWalkObject`.

## Empty Class

The `_ihMeta` splitter supplies `b''` when no `$class` is present. `_lRegisterSubClass`
walks an empty class as no subnodes and assigns the item to the current root.

Records with no class interact with `_LastClass`; class semantics should be
tested carefully because `Node` is a mutable closure.

## Repeated Classes

Consecutive records with the same class reuse `Node`. A new class walks from
`Root` and replaces `Node` with the corresponding nested dictionary.

## Repeated Names

Normal repeated names overwrite the existing dictionary entry. `nil` names are
the special counter case and do not overwrite.

## Ambiguity

The exact behavior of mixed class changes, repeated names, and an empty class
is implemented by closure state. Tests cover nested classes and `nil`, but do
not establish every possible interleaving.

Future changes to `_LastClass`, `_lWalkObject`, or `_lCounter` need an explicit
matrix of consecutive and non-consecutive class records.
