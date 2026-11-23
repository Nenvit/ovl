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

## CRLF and Exact Delimiters

The parser operates in binary mode and trims trailing CR/LF in `_ihMeta`.
Exact `': '` and `'] '` delimiters are required in metadata blobs. Text-format
expectations and line-ending behavior need tests for Windows CRLF and newline
values.

## Parser Malformed-Line Behavior

Every non-comment, non-matching line is appended to the buffer. It is therefore
capable of multiline values but has no separate malformed-line error mode.
Malformed metadata can silently alter or corrupt the previous value.

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
