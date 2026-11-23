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

## Strict Metadata Recognition

`META_REGEXP` is:

```python
rb"^\w+\]\s[\w]+(\$[\w]+(?:\.[\w]+)*)?:\s"
```

It recognizes a record beginning with:

```text
type] name$class.subclass:
```

In the implementation, `\w+` covers the type and name portions, `$` starts an
optional class, and dots separate class segments. The final separator is
captured as whitespace or newline.

## Buffering

`_ihBlobber` accumulates bytes until it encounters another matching metadata
line. A matching line flushes the previous buffer. Lines beginning with `...`
are skipped as comments.

Malformed or non-metadata lines are appended to the current buffer. Therefore
they can form multiline values. They can also corrupt the preceding value when
inserted intentionally or accidentally.

This behavior is explicit in `_ihBlobber` and should not be replaced by fallback
metadata inference without a broad compatibility assessment.

## Inline and Newline Values

The same metadata line may contain data after `: `:

```text
int] port$networks.servers.server0: 8080
```

A colon followed by a newline is also buffered and yields the following line as
data:

```text
int] port$networks.servers.server0:
8080
```

`_ihMeta` splits each buffered record on `': '` and is therefore sensitive to
that exact byte delimiter.

## Metadata Split

After a complete blob is produced, `_ihMeta`:

1. splits metadata and data at `b': '`;
2. splits type and metadata at `b'] '`;
3. splits name and class at `$`;
4. yields `_type`, `_name`, `_class`, and `_blob`.

The data portion is stripped of trailing CR/LF bytes.

## Ambiguity

The README states that the loader accepts `.ovl` and `.conf`; the active
constant in source agrees. Earlier suffix names mentioned in repository history
or prior documentation are not active behavior in the current source.
