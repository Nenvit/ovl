# Known Technical Debt

## Mutable Default in the Signature

`loads` declares `update={}`. The implementation immediately calls
`dict(update)`, so the default object is copied and not mutated by this
function. However, the mutable-looking default remains part of the signature
and can confuse readers and static analysis.

No test demonstrates shared-state mutation through the default. Replacement
should preserve the copy behavior.

## Assertion-Based Path Validation

`_ihAssert` is called with `assert _ihAssert(o)`. Python assertion behavior can
be disabled with optimized interpreter settings. The function already raises
its own validation exceptions, so this assertion wrapper is not the validation
mechanism and may be unclear to maintainers.

## Whitespace, CRLF, and Split Rules

The parser operates in binary mode and trims trailing CR/LF in `_ihMeta`.
`META_REGEXP` permits bounded spaces/tabs, and `_ihMeta` uses separate split
patterns rather than fixed `': '` and `'] '` delimiters. The implementation
does not permit arbitrary whitespace; maintainers should test the exact regexp
limits and line-ending behavior.

## Parser Malformed-Line Behavior

Every non-comment, non-matching line is appended to the buffer. It is therefore
capable of multiline values but has no separate malformed-line error mode.
Malformed metadata can silently alter or corrupt the previous value.

The updated `_ihBlobber` also requires both the incoming chunk and the existing
buffer to match `META_REGEXP` before flushing the buffer. This stricter
two-sided condition is central to buffer behavior and should be tested with
consecutive whitespace variants.

## Coverage Gaps

Tests cover the main loader operations and several conversions, but not every
dispatch label or every hierarchy interleaving. External-package conversions
have especially limited direct coverage.

## Compact Implementation

Several internals use compact expressions and closures. This is consistent
with the repository's concise implementation style, but broad edits are risky
because behavior is concentrated in few functions.

## Commented Dispatch

`pckl` and `pkl` are commented out in `TypeLibraryDispatch`. The repository
does not establish a completed support contract for these labels.

## Class-Path Aliasing

`ClassFactory` now keeps `ClassPath` as tuple state and `ItemNameDatabase` as
named-to-tuple state. Ordinary and alias classes are resolved by
`_lResolveClassPath` before `_lSetClassPath` and `_lWalkObject`.

The broad `except` in `_lResolveClassPath` hides lookup and splice failures and
replaces the resolved path with an empty path.

Forward aliases are not revisited. Unknown names and invalid suffixes do not
produce an alias-specific exception.

The latest source contains a construction inconsistency: direct probes show
ordinary classes can be stored under tuple keys such as `('network',)` instead
of the expected string key `network`, and alias paths can produce nested tuple
keys. This is observable in `ClassFactory` and should be treated as a
maintenance defect, not documented as stable nested-dictionary behavior.
