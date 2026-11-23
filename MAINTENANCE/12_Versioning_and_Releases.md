# Versioning and Releases

## Public Distribution Version

The authoritative public project version in package metadata is
`1.0.1` in `pyproject.toml`. Distribution name is `ovl-standard-loader`.

Public release information should be taken from package metadata, installed
package metadata, and the README rather than the binary version file.

## Internal `VERSION` File

The repository contains a binary `VERSION` file maintained primarily for
internal version control and the author's proprietary standard library.
The README states that this library API is not a public interface and may
remain unavailable or change for an indeterminate period.

The current bytes decode through `versioning.Version.unpack` as:

```text
OVL Standard Implementation:: LoaderLibrary: Sod 1.0.1:11 [BETA]
```

The fields are major `1`, minor `0`, patch `1`, build `11`, service
`OVL Standard Implementation`, product `LoaderLibrary`, release `Sod`, and
status `Beta`.

## Format Stability

The format is internal and not a public, stable API contract. The README
explicitly warns that it can change and that maintainers should consult public
package metadata instead.

Changing `pyproject.toml` version metadata and the `VERSION` file independently
can make the two representations disagree. No repository automation was found
that synchronizes them.
