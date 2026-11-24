# Project Overview

## Purpose

The repository implements **OVL Standard Loader**, distributed as
`ovl-standard-loader` and imported as `ovl`. It reads OVL-style text files and
converts records according to explicit type metadata.

The public package has three functions: `loads`, `loadsarray`, and `loadsiter`.
They are exported from `src/ovl/__init__.py` and implemented in
`src/ovl/utils/loaders.py`.

## Repository Layout

```text
pyproject.toml
README.md
VERSION
src/
  ovl/
    __init__.py
    utils/
      __internals.py
      loaders.py
tests/
  test_ovl.py
```

`src/ovl/utils/__internals.py` contains path validation, source buffering,
metadata parsing, dispatch, boolean translation, and object construction.
`src/ovl/utils/loaders.py` exposes the three high-level operations.

## Runtime and Distribution

`pyproject.toml` declares Python 3.15 or newer and defines the setuptools
build backend. The `src/` layout is enabled by `package-dir = {"" = "src"}`.
Package discovery includes `ovl*`.

The public distribution version is `1.0.1`. Python 3.15 is also the minimum
used to describe standard-library `frozendict` behavior in the README.

## Observable Design Principles

The recurring implementation patterns support these descriptions:

- **Strict parsing:** metadata is accepted only when it matches
  `META_REGEXP`.
- **Explicit type handling:** each known type label maps to a conversion
  function or value parser.
- **Minimal inference:** unknown type labels become decoded text rather than
  undergoing a second guessing mechanism.
- **Known-type dispatch:** `TypeLibraryDispatch` performs direct label
  matching.
- **Hierarchical construction:** `$class` and dot-separated class segments
  become nested dictionaries.
- **Class-path alias state:** `ItemNameDatabase` and `ClassPath` enable
  sequential named and current-path alias resolution.
- **Immutable-by-default loading:** `loads` uses `freeze=True` by default.

These are observations from code and tests, not claims of a broader product
strategy.
