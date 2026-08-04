# R-E3 — Cite-Not-Import Modularity v1.0.0
RDODI's own modularity, distinct from R-E8: module sets declared in a MANIFEST and merged by reference-resolution
with ZERO owl:imports (L-64). Extension modules add real subclass depth, referencing base classes by IRI. The
assembly stays full-DL (no dangling imports to fetch) — the deliberate contrast with owl:imports modularity (which
forced the parallel into OWL-RL fallback).

## Measured result (STG modular candidate)
- 5 modules (base tbox+abox + 3 extension taxonomies: policy/rule/steward; 7 new subclasses) merged by manifest.
- owl:imports in assembly: **0** (L-64 invariant enforced by the assembler — raises if violated).
- consistency **OWL-DL (HermiT)** PASS; SHACL PASS; fidelity **13/13** authority-sourced PASS; OVERALL **ACCEPT**.
- **INROnto 0.0 -> 0.538** (>0.50 floor): the flat-hierarchy advisory carried since P2 is RETIRED.

## Contrast captured
parallel: owl:imports modularity -> RL fallback (DL unverifiable offline until R-E8 resolved it).
RDODI R-E3: cite-not-import modularity -> stays full-DL natively. Same breadth benefit, no DL cost.
