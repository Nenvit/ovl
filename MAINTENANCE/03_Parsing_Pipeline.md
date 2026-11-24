# Parsing Pipeline

## Path Validation

`InternalPlumbing` first passes the input to `_ihGenerateSrc`.
`_ihGenerateSrc` converts the input to `Path` and `_ihAssert` verifies:

1. the path exists;
2. it is a file;
3. its suffix is in `ACCEPTED_OVL_SUFFIXES`;
4. read permission is available according to `os.access`.

The active suffix tuple is `.ovl` and `.conf`. `_ihAssert` raises
`FileNotFoundError`, `IsADirectoryError`, `NotImplementedError`, or
`PermissionError` for the corresponding failures.

## Source Reading

`_ihGenerateSrc` opens the file in binary mode and yields each physical line.
Keeping source bytes in the pipeline avoids implicit text decoding until a
known conversion dispatch is selected.

## Whitespace-Permissive Metadata Recognition

`META_REGEXP` is:

```python
rb"^\w+\][ \t]{1,3}[\w]+ {0,3}(\$ ?(\w+|(\[\w+([;-](\w+|([1-9][0-9]*)))?\]))(?: ?\.[\w]+)*)? {0,3}:[\s]{0,3}"
```

It recognizes a record beginning with:

```text
type] name$class.subclass:
```

The active limits are:

- `]` is followed by one to three spaces or tabs;
- the name may have zero to three spaces before an optional `$`;
- `$` may have one optional space after it;
- the first class segment may be ordinary `\w+` text or a bracketed alias;
- bracketed aliases support `[name]`, `[nil]`, `[name;suffix]`, and
  `[name-suffix]`;
- dotted class segments may have one optional space before or after dots;
- zero to three spaces may precede the colon;
- zero to three whitespace characters may follow the colon.

These are the exact source limits. They do not permit arbitrary indentation,
arbitrary tab counts, or arbitrary spaces around every separator.

## Buffering

`_ihBlobber` accumulates bytes until it encounters a chunk that:

1. matches `META_REGEXP`; and
2. is followed while the existing buffer also matches `META_REGEXP`.

Under the current implementation, a matching chunk flushes the previous
buffer only when both conditions hold. Lines beginning with `...` are skipped
as comments.

Malformed or non-metadata lines are appended to the current buffer. Therefore
they can form multiline values. They can also corrupt the preceding value when
inserted intentionally or accidentally.

This behavior is explicit in `_ihBlobber` and should not be replaced by fallback
metadata inference without a broad compatibility assessment.

## Inline and Newline Values

The same metadata line may contain data after the colon:

```text
int] port$networks.servers.server0: 8080
```

A colon followed by a newline is also buffered and yields the following line as
data:

```text
int] port$networks.servers.server0:
8080
```

`_ihMeta` uses the following regular-expression splits:

```python
rb" ?:[\s]{0,3}"
rb"\][ \t]{1,3}"
rb" {0,3}\$ ?"
rb" ?\."
```

The split behavior removes permitted surrounding spaces in metadata and
normalizes dot-separated class segments. The active implementation does not
use fixed `: ` and `] ` values as its metadata split contract.

After `_ihMeta`, `_lResolveClassPath` performs alias resolution. It recognizes
semicolon positive slices and hyphen negative slices using
`split(r'[;-]', ..., maxsplit=1)`. `_ihMeta` itself does not split semicolons
or hyphens, so these characters remain available for alias processing.

## Metadata Split

After a complete blob is produced, `_ihMeta`:

1. splits metadata and data with `rb" ?:[\s]{0,3}"`;
2. splits type and metadata with `rb"\][ \t]{1,3}"`;
3. splits name and class with `rb" {0,3}\$ ?"`;
4. normalizes dot-separated class segments with `rb" ?\."`;
5. yields `_type`, `_name`, `_class`, and `_blob`.

The data portion is stripped of trailing CR/LF bytes.

## Ambiguity

The README states that the loader accepts `.ovl` and `.conf`; the active
constant in source agrees. Earlier suffix names mentioned in repository history
or prior documentation are not active behavior in the current source.
