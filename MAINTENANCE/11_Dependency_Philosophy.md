# Dependency Philosophy

## Runtime Dependencies

`pyproject.toml` declares:

- `html5lib`;
- `Markdown`;
- `python-dateutil`;
- `PyYAML`;
- `validators`.

The implementation imports these packages only for relevant dispatch labels.
This is a narrower dependency set than a broad framework and maps package
imports to conversion features.

## Standard Library

The source uses `pathlib`, `re`, `typing`, `os`, `json`, `pickle` modules
through imports or dispatch comments, and `tomllib` for TOML conversion.
The README notes that Python 3.15 supplies `frozendict` in the standard
library.

## Build Dependencies

The build system requires `setuptools>=68` and uses the setuptools build
backend. Package discovery is limited to `ovl*` in `src/`.

## Dependency Risk

Dependency changes can affect:

- HTML parsing;
- Markdown rendering;
- date/time parsing;
- YAML loading;
- validation and finance/network checks;
- package metadata and wheel discovery.

The test suite currently covers fewer external dependencies than are declared,
so a dependency update should include focused conversion tests.
