# Type System and Dispatch

## Dispatch Contract

`TypeLibraryDispatch` receives a lowercase byte label and returns:

- a callable conversion function; and
- a boolean indicating whether `Eval` should first decode bytes to text.

`Eval` then invokes that callable with raw bytes or decoded text.

## Text-Converted Types

These dispatch entries call `Eval` with decoded text:

- `html`, `html5`, `htm`
- `path`
- URL and identifier validators
- `md`
- `int`, `float`
- complex number labels
- `toml`

The README's dispatch table is the public summary. The implementation is the
authoritative behavior.

## Byte-Converted Types

These dispatch entries receive raw bytes:

- `blob`
- `json`
- `yaml`
- delimited-value labels
- `bool`
- date and time labels
- `datetime` and `dt`

## Known Labels

The active dispatch includes HTML5, path, validation, finance identifiers,
blob, JSON, YAML, delimited lists, Markdown, numeric values, booleans,
dates/times, and TOML.

Unknown labels return a callable that decodes text and is not reassigned to a
default conversion.

## Dispatch Risks

Dispatch changes affect `loads`, `loadsarray`, and `loadsiter` because all
three call `TypeLibraryDispatch`.

A new label should account for:

- lowercase normalization;
- bytes versus text input;
- exact output type;
- multiline buffer behavior;
- tests for each public loader.

## Deferred or Commented Behavior

The source has a commented-out pickle dispatch case for `pckl` and `pkl`.
It is not active behavior and should not be documented as supported.
