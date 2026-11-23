# Extension Guidelines

## Adding a Type Label

Before adding a label to `TypeLibraryDispatch`, determine:

1. whether it consumes raw bytes or text;
2. the exact return type;
3. whether the external package already handles validation;
4. whether unknown or invalid input should return text, `None`, or raise;
5. whether each public loader receives the expected result.

Add tests that call `loads`, `loadsarray`, and `loadsiter` when the result
shape differs or the implementation dispatch is shared.

## Adding an Accepted Suffix

Update `ACCEPTED_OVL_SUFFIXES` and test `_ihAssert` through public loading.
Update the README suffix list and maintenance documentation when behavior is
complete and intentional.

## Adding a Boolean Value

Add exact bytes to `BOOLEAN_TRANSLATION_MAP.TRUE` or `.FALSE`. Preserve
lowercase and whitespace normalization behavior. Add tests for direct parser
results and at least one public loader.

Do not remove or alter phrase entries for unrelated cleanup. The false set is
part of the current public format and includes project and source-specific
phrases.

## Adding Hierarchical Behavior

Prefer tests before changing `_lRegisterSubClass`, `_lWalkObject`, `_lCounter`,
or `_LastClass`. Those functions interact through mutable closure state.

At minimum, test:

- consecutive same-class records;
- class changes;
- dot-separated classes;
- repeated normal names;
- repeated `nil` names;
- empty classes;
- frozen and mutable output.

## Adding Multiline Parsing

The strict metadata regex, `_ihBlobber`, `_ihMeta`, and dispatch must be tested
together. A change to one delimiter or line boundary can alter `: ` splitting,
CRLF handling, comments, or data buffering.
