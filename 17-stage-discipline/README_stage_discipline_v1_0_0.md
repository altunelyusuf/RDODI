# R2 — Stage-Discipline TTLs v1.0.0
Makes the per-stage pipeline discipline DECLARATIVE and auditable in RDF, instead of hardcoded.

- **stage_discipline_v1_0_0.ttl** — each Stage declares the gates it requires:
  Document & Interactive-Page → parse, shacl, coverage, substance, sourceValidity; Cross.B → provenance.
  This is a FAITHFUL encoding of gates the validator already runs — no aspirational checks (L-66).
- **rdodi_stage_discipline_runner_v1_0_0.py** — reads the TTL and dispatches exactly the declared gates to
  the existing validator (v1.4.0).

## Verified (L-65)
On generated artifacts: 3 stages, 11 gates run, 0 FAIL, **0 undispatched**. The declared gate set matches the
validator's implemented gates exactly — declarative discipline reproduces the hardcoded verdicts (no regression),
and declares nothing it cannot run.
