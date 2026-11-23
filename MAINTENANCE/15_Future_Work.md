# Future Work

## Repository Evidence

No formal roadmap, issue plan, or future-work section is present in the
repository.

The only clearly identified inactive implementation area is the commented-out
`pckl`/`pkl` dispatch case in `TypeLibraryDispatch`. It is not evidence that
pickle support is approved or that its return semantics are decided.

## Test Coverage

The test suite leaves public dispatch branches without direct coverage,
including HTML, Markdown, network and finance validation, date/time, WSV/LSV,
and hierarchical edge cases. Expanding coverage would follow existing behavior
but is not documented by the repository as a roadmap commitment.

## Ambiguous Format Evolution

The binary `VERSION` format is explicitly internal and may change. Any future
tooling that reads or writes it should remain outside the public package API
unless explicitly adopted in separate source.

## No Speculative Roadmap

The repository does not specify planned:

- new format versions;
- backward compatibility guarantees;
- additional public APIs;
- migration tooling;
- broader Python support;
- new parser modes.

Those items should not be described as project plans unless a maintainer adds
an evidence-bearing source or issue outside this repository.
