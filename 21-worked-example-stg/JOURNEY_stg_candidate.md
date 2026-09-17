# Worked example — STG candidate: REJECT -> ACCEPT (R-E1 + R-E2 + R-E4)
| Stage | consistency | SHACL | fidelity | FAIR-F | FAIR-R | OVERALL |
|-------|-------------|-------|----------|--------|--------|---------|
| P2 (baseline) | PASS | PASS | **FAIL 0/6** | absent | absent | **REJECT** |
| + R-E1 authority cites | PASS | PASS | **PASS 6/6 (normative-term, authority)** | absent | absent | REJECT→ |
| + R-E2 versionIRI/metadata | PASS | PASS | PASS | **present** | partial | → |
| + R-E4 license/provenance | PASS | PASS | PASS | present | **present** | **ACCEPT** |
Remaining advisory (honest, not blocking): OQuaRE INROnto 0.00 (flat governance hierarchy) — structural, an E3 matter.
All flips are honest: R-E1 PASS came from genuine authority cites (not gate relaxation); license was DECLARED, not invented.
