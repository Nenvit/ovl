# Maintenance Rules

## AI Policy

The implementation is human-authored.

AI usage is limited primarily to:

- documentation drafting;
- README generation;
- maintenance documentation;
- autocomplete assistance;
- boilerplate generation.

Core architecture, parser design, loaders, dispatch systems, object
construction, format decisions, and implementation logic should be treated as
author-driven unless the repository itself explicitly states otherwise.

## Maintainer Covenant

Future maintainers should preserve:

- simplicity over cleverness;
- explicit behavior over inference;
- narrow solutions over generalized frameworks;
- strict parsing;
- explicit type handling;
- known-type dispatch;
- hierarchical object construction;
- immutable-by-default loading.

## Broad-Effect Change Checklist

Before a change, identify whether it touches:

- `META_REGEXP`;
- `_ihBlobber` or `_ihMeta`;
- accepted suffixes;
- `TypeLibraryDispatch`;
- boolean translation;
- `ClassFactory`;
- public loader signatures;
- `pyproject.toml`;
- public README behavior;
- tests.

## Documentation Consistency

README statements are public contracts only where the implementation and tests
support them. Source behavior is the stronger evidence if documentation and
implementation diverge.

When resolving such divergence, document the ambiguity instead of silently
inventing a new policy.
