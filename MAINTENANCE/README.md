# OVL Maintenance Manual

This manual describes the repository as implemented. It is intended for future
maintainers and records observable behavior rather than an inferred roadmap.

## Reading Order

1. [Project Overview](01_Project_Overview.md)
2. [Architecture](02_Architecture.md)
3. [Parsing Pipeline](03_Parsing_Pipeline.md)
4. [Type System and Dispatch](04_Type_System_and_Dispatch.md)
5. [Object Construction](05_Object_Construction.md)
6. [Boolean Parsing](06_Boolean_Parsing.md)
7. [Class and Hierarchy Semantics](07_Class_and_Hierarchy_Semantics.md)
8. [Public API Surface](08_Public_API_Surface.md)
9. [Testing Strategy](09_Testing_Strategy.md)
10. [Extension Guidelines](10_Extension_Guidelines.md)
11. [Dependency Philosophy](11_Dependency_Philosophy.md)
12. [Versioning and Releases](12_Versioning_and_Releases.md)
13. [Maintenance Rules](13_Maintenance_Rules.md)
14. [Known Technical Debt](14_Known_Technical_Debt.md)
15. [Future Work](15_Future_Work.md)

## Evidence Key

The primary evidence is the package source under `src/ovl/`, the public
documentation in `README.md`, package metadata in `pyproject.toml`, automated
tests under `tests/`, and the binary `VERSION` file.

Where behavior is unclear, the relevant chapter identifies the ambiguity and
the evidence visible in the repository. It does not treat absence of evidence
as a future requirement.
