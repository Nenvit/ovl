# Testing Strategy

## Framework

The suite uses Python's standard-library `unittest` and requires no separate
test package.

Run it from the repository root:

```console
python -m unittest discover -s tests -v
```

The test module inserts `src/` into `sys.path` before importing `ovl`.

## Fixture Pattern

`OVLTestCase` creates a temporary directory per test and provides `write_ovl`,
which writes UTF-8 text and returns a `Path`.

The suite is organized into:

- `PublicLoaderTests`; and
- `ConversionTests`.

## Public API Coverage

Tests cover frozen and mutable `loads`, update dictionaries, nested classes,
`loadsarray` tuple/list behavior, keyed and value-only iteration, `nil`
indexes, comments, suffixes, whitespace-permissive inline metadata, and
newline-separated values with whitespace.

The expanded suite contains 19 tests.

## Conversion Coverage

Tests cover booleans, integers, floats, complex values, blobs, CSV, TSV, JSON,
YAML, TOML, text, and paths.

## Current Gaps

The suite does not currently establish behavior for every dispatch label.
Examples omitted from dedicated tests include HTML, Markdown, URLs, network
validators, finance identifiers, WSV/LSV, dates, and times.

The suite also does not explicitly cover every interleaving of class changes,
mixed empty classes, repeated normal names, unknown dispatch labels, CRLF
handling, permission failures, or malformed metadata.

These gaps are observable from the test file rather than inferred defects.
