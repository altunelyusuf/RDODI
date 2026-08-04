# C2 — RDODI Bootstrap Kit v1.0.0
One command, profile-parameterized: `<domain.ttl> <ProfileLocalName> <profiles.ttl> <out_dir> <doc_tbox> <doc_shacl> <page_tbox> <page_shacl>` (generator/validator/assessor paths via GEN/VAL/ASR env).
Chain: detect → generate (document+page) → validate (10 gates) → assess (C1) → emit `bootstrap_report.json`.

## Discipline baked in (this session's lesson)
The report SURFACES every verdict including tier-C caveats and assessor REJECT/ADVISORY reasons under
`human_judgment_required`. It NEVER collapses to a green "DONE". Status distinguishes
"GENERATED + STRUCTURALLY VALIDATED" from substance/provenance proof — the latter is never claimed
(gates certify structure + real-sourcing only; the assessor certifies ontology quality, not prose substance).

## First run (ch9_domain + CourseCompanion) — honest output
STATUS: GENERATED + STRUCTURALLY VALIDATED — substance/provenance NOT proven. 10 gates; 7 human-judgment items
surfaced (substance-gate caveats ×2; 28 unsourced entities; RROnto/FAIR advisories).
