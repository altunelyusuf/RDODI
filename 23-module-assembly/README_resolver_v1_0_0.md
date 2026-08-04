# R-E8 — Module-Assembly Resolver v1.0.0
Resolves an ontology's owl:imports closure to LOCAL files (offline, deterministic), merges into a self-contained
assembly, strips now-redundant owl:imports, and reports every module included + any unresolved import (no silent drop).

## Measured result (parallel STG governance closure)
- partial ad-hoc merge (P3): SHACL 17 violations (ARTIFACT) + OWL-RL fallback (DL unverifiable).
- R-E8 resolved closure: SHACL **0 violations** (right verdict) + **full OWL-DL (HermiT)** consistency.
- accurate fidelity: 54/103 sourced (25 domain-concept literature + 29 normative-term authority; 49 unsourced)
  — far truer than the partial 0/74, and it shows the parallel ALSO authority-sources normative terms (converges with R-E1).

## Closes a P3 caveat
P3 noted "parallel DL-consistency unverified offline (5 imports)." R-E8 resolves+strips those imports, so the parallel
is now full-DL-checkable. With R-E8 assembly the harness comparison's shacl + consistency CONVERGE (both PASS).
