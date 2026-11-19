# OVL Standard Loader

OVL Standard Loader reads OVL-style text files and converts typed values into
Python objects. The main implementation is available as `ovl.loads`; a second,
older implementation is available as `ovl.golf_ovl.loads` and through the
compatibility import `golf_ovl`.

## Requirements

- Python 3.15 or newer.
- The runtime packages listed in `pyproject.toml`:
  - `boolean-parser` (imported as `boolean_parser`) for boolean values.
  - `frozendict` for immutable mapping results.
  - `html5lib` for HTML values.
  - `Markdown` (imported as `markdown`) for Markdown values.
  - `python-dateutil` (imported as `dateutil`) for date and time values.
  - `PyYAML` (imported as `yaml`) for YAML values.
  - `validators` for URL, email, network address, and identifier validation.

The standard-library modules used by the loaders include `pathlib`, `re`,
`typing`, `os`, `json`, `pickle`, and `tomllib`. In particular, `tomllib` is
included with Python 3.11 and later, so it does not need a separate package.

## Install

Install the project from a checkout:

```console
python -m pip install .
```

For development, install it in editable mode:

```console
python -m pip install -e .
```

The project uses a PEP 517 `pyproject.toml` build configuration and a `src/`
package layout. The distribution name is `ovl-standard-loader`; the primary
Python import name is `ovl`.

## Quick start

```python
from ovl import loads

values = loads("settings.ovl")
```

`loads(path)` accepts a string or `pathlib.Path`. The main implementation
accepts files with these suffixes: `.ovl`, `.oval`, `.oconf`, `.ov`, `.conf`,
and `.ovlconf`. It returns an immutable `frozendict`, grouped by the class
portion of each entry. In the current parser, separate the key and class with
`$`; records with an empty class (a trailing `$`) are merged into the top
level of the result.

To request the older implementation instead:

```python
from golf_ovl import loads

values = loads("settings.ovl")
```

The older loader accepts only `.ovl` files. Its parsing and supported type
conversions differ from the main `ovl.loads` implementation; prefer the main
implementation for new code.

## File format

The main loader recognizes metadata records shaped like:

```text
type] key$class: value
```

The `$class` portion identifies the result group. For example:

```text
int] retries$network: 3
csv] formats$display: json,xml
... continuation lines are ignored by the loader
```

The main implementation's dispatch table recognizes labels such as `html`,
`json`, `yaml`, `pckl`/`pkl`, `md`,
`url`, `email`, `ipv4`, `ipv6`, `mac`, `date`, `time`, `datetime`/`dt`,
`bool`, `int`, `float`, `complex`/`cplx`, `path`, `blob`, `csv`, `tsv`, and
`toml`. Unrecognized types are returned as text. The two implementations have
different conversion paths; verify the specific conversions your application
uses rather than assuming they behave identically.

Only load OVL files from trusted sources. Some typed-value conversions
evaluate generated Python expressions, so untrusted input is not safe to
process.

## Package layout

```text
pyproject.toml
src/
  golf_ovl.py          # compatibility import
  ovl/
    __init__.py        # main implementation; exports loads
    golf_ovl.py        # older implementation
```

## Development and build

Build a wheel without installing the project:

```console
python -m pip wheel --no-deps .
```

There is currently no automated test suite in the repository.
