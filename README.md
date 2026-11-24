# OVL Standard Loader

OVL Standard Loader reads typed, structured configuration files and converts
their values into Python objects. The package exposes mapping, array, and
iterator APIs while preserving a small, dependency-focused surface.

**Current release:** `1.0.1`

## Installation

### Requirements

- Python 3.15 or newer
- The runtime dependencies declared in `pyproject.toml`

The current runtime dependencies are `html5lib`, `Markdown`, `python-dateutil`,
`PyYAML`, and `validators`.

On Python 3.15, immutable mappings are provided by the standard-library
`frozendict` implementation and do not require a separate package.

### From a source checkout

```console
python -m pip install .
```

### For development

```console
python -m pip install -e .
```

The distribution is published as `ovl-standard-loader`; the import package is
`ovl`.

## Quick Start

Load an OVL file into an immutable mapping:

```python
from ovl import loads

settings = loads("settings.ovl")
```

To receive a mutable dictionary, disable freezing:

```python
settings = loads("settings.ovl", freeze=False)
```

An existing dictionary can be supplied as the initial mapping:

```python
settings = loads(
    "settings.ovl",
    update={"environment": "development"},
)
```

## Public API

### `loads(path, update={}, freeze=True)`

Loads a file into a nested mapping. The `path` argument accepts both a string
and a `pathlib.Path`.

Classes form nested mappings. Dot notation can be used to create additional
levels:

```text
int] retries$network.timeout: 3
```

Set `freeze=False` to return a mutable dictionary. The `update` argument
provides values that are present before the file is processed.

## Class-Path Aliases

The first class segment may reference another record's resolved class path.
The bracketed forms implemented by `__internals.py` are:

```text
[name]
[nil]
[name;suffix]
[name-suffix]
```

### Named aliases

`ItemNameDatabase` records the resolved class tuple for normal string item names.
A later bracketed alias can copy that tuple:

```text
int] primary$network.servers.primary: 8080
int] port$[primary]: 8081
```

Aliases are resolved sequentially. `[primary]` can refer to `primary` only after
the earlier record has been processed and has registered its name. Repeated
string item names replace the database entry with the most recent resolved
class tuple.

### `[nil]`

`[nil]` does not search `ItemNameDatabase`. It resolves from `ClassPath`, the
tuple currently active for construction:

```text
int] first$network.servers: 8080
int] port$[nil].alternate: 8081
```

The optional dotted continuation after the bracket is appended to the resolved
alias path.

### Semicolon positive splices

`[name;suffix]` selects a prefix of the referenced tuple:

- a numeric suffix `N` uses `slice(0, N + 1)`;
- a word suffix uses `slice(0, index(word) + 1)`.

For example:

```text
int] port$[primary;2]: 8081
int] port$[primary;servers]: 8081
```

These forms use a semicolon; `_ihMeta` does not split semicolons from
metadata.

### Hyphen negative splices

`[name-suffix]` selects a prefix of the referenced tuple with an exclusion
slice:

- a numeric suffix `N` uses `slice(0, -N)`;
- a word suffix uses `slice(0, -index(word))`.

For example:

```text
int] port$[primary-1]: 8081
int] port$[primary-servers]: 8081
```

The suffix is resolved from the tuple stored for `name`, or from `ClassPath`
for `[nil-suffix]`.

### Alias failure behavior

Alias lookup or splice resolution is inside a broad `except` in
`_lResolveClassPath`. Lookup failures, missing `nil` context, invalid word
suffixes, or other splice errors fall back to an empty class path instead of
raising an alias-specific exception.

The fallback is not a later lookup pass: forward references and unknown names
do not resolve retroactively.

### `loadsarray(path, freeze=True)`

Returns values in file order as a tuple by default:

```python
from ovl import loadsarray

values = loadsarray("settings.ovl")
```

Pass `freeze=False` to return a list instead.

### `loadsiter(path, keys=True, freeze=False)`

Returns an iterator over parsed records:

```python
from ovl import loadsiter

for value in loadsiter("settings.ovl"):
    print(value)
```

With `keys=True`, the iterator yields `(class, name, value)` tuples:

```python
for value_class, name, value in loadsiter("settings.ovl", keys=True):
    print(value_class, name, value)
```

## File Format

Value-bearing records use the metadata form below:

```text
type] name$class.subclass.es: data
```

The parser accepts limited whitespace variation. `]` may be followed by one to
three spaces or tabs, while class and colon regions may contain up to three
spaces. The colon may be followed by zero to three whitespace characters.

Examples include:

```text
int] retries$network: 3
csv] formats$display.colors: json,xml
int]\tport $ networks .servers.server0 :   8080
int]   port   $ networks.servers: 8080
```

Any line that does not match the strict metadata syntax is not parsed as a
separate value. Instead, it is appended to the buffered content of the preceding
record. It can therefore build a multiline value, but it can also alter or
corrupt the preceding value if inserted accidentally.

```text
yaml] server$config: host: localhost
port: 8080
```

In this example, `host: localhost` and `port: 8080` do not match the strict
record syntax, so they become part of the YAML value.

Lines beginning with `...` are comments. They are ignored by the parser rather
than appended to the buffer or interpreted as data.

A record is also technically acceptable when the metadata is followed only by
a colon and newline, with the value on the following line:

```ovl
type] name$class.es:
data
```

For example:

```ovl
int] port$networks.servers.server0:
8080
```

The loader does not perform fallback parsing for malformed metadata. The
matching and splitting rules are:

- type: one or more `\w` characters;
- after `]`: one to three spaces or tabs;
- name: one or more `\w` characters;
- class: optional, beginning with `$`, with optional spaces around `$` and dots;
- class segments: one or more `\w` characters;
- before the colon: zero to three spaces;
- after the colon: zero to three whitespace characters.

Additional characters outside these ranges can prevent a line from matching
and may cause it to be buffered with the preceding value.

The loader accepts:

- `.ovl`
- `.conf`

Metadata and values are read as bytes, then converted according to the type
label.

## Supported Value Types

| Label | Result |
| --- | --- |
| `html`, `html5`, `htm` | HTML5 document |
| `json` | JSON value |
| `yaml` | YAML value |
| `md` | Markdown-rendered text |
| `path` | `pathlib.Path` |
| `url`, `email`, `card`, `uuid`, `iban` | Validated value |
| `ipv4`, `ipv6`, `mac` | Validated network value |
| `cusip`, `isin`, `sedol` | Validated financial identifier |
| `blob` | UTF-8 bytes |
| `csv`, `tsv`, `wsv`, `lsv` | Delimited list |
| `int`, `float` | Numeric value |
| `cplx`, `complex`, `imag` | Complex numeric value |
| `bool` | Boolean or `None`; parsed by the built-in boolean parser |
| `date`, `time`, `datetime`, `dt` | Date, time, or datetime value |
| `toml` | TOML value |

Unknown type labels are decoded as text. A name of `nil` assigns an automatic
numeric index within the active class.

## Boolean Parsing

Boolean values use the native `BooleanParser` implementation in
[`__internals.py`](./src/ovl/utils/__internals.py). Parsing is case-insensitive
and ignores surrounding whitespace.

```text
bool] enabled: yes
bool] fallback: no
bool] unknown: maybe
```

Recognized true values include `yes`, `y`, `true`, `t`, `on`, `enabled`,
`1`, and `ofc`. Recognized false values include `no`, `n`, `false`, `f`,
`off`, `0`, `disabled`, and `negative`.

The parser also recognizes selected English phrases, including
`thanks, but no thanks`, and multilingual equivalents such as `oui`, `ja`,
`да`, `нет`, `ложь`, `faux`, and `nein`. Any value outside these translation
maps returns `None`.

The translation tables are an intentional part of OVL's public boolean format.
They are maintained in
[`BOOLEAN_TRANSLATION_MAP`](./src/ovl/utils/__internals.py). The false-value
collection includes a "99 ways to say No" reference, attributed in source
comments to
[LinkedIn's 99 ways to say no article](https://www.linkedin.com/pulse/20130501190655-52397036-100-ways-to-say-no).
Individual phrases originate from that reference or from the project's own
examples and modifications.

## Version Information

The `VERSION` file is maintained primarily for internal version control as part
of the author's proprietary standard library. That standard-library API is not
currently offered as a public interface and may remain unavailable or change
without notice for an indeterminate period.

For public package information, use `pyproject.toml`, this README, package
metadata, and installed-package metadata instead. The package's authoritative
release and compatibility information is declared in `pyproject.toml`; details
in `VERSION` should not be assumed to represent a public API or format
guarantee. The binary format may change in the future, while the public sources
remain the reference for users.

## Package Layout

```text
pyproject.toml
src/
  ovl/
    __init__.py        # Public exports
    utils/
      __internals.py   # Parser and conversion internals
      loaders.py       # Public loader functions
```

## Development

Run the automated test suite from the repository root:

```console
python -m unittest discover -s tests -v
```

Build a wheel without installing the package:

```console
python -m pip wheel --no-deps .
```

Build a source distribution and wheel:

```console
python -m build
```
