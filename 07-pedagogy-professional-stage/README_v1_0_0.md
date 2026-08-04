# RDODI Pedagogy & Professional Standards Stage — v1.0.0  (ecosystem → v1.6.0)

Additive new stage for the RDODI four-stage pipeline that enriches it to cover pedagogical and professional
standards **and enforces them in runnable gates**, keeping OE Operating Discipline v2.0.0. v1.5.2 is untouched
(BP-D6/D7); this module lifts the ecosystem to v1.6.0.

## Contents
- `01-vocabularies/` — learning-design (Bloom, worked examples, assessment items), model-provenance,
  standards-conformance (ISO/IEC 25010 + OQuaRE anchored, L-72), attestation. All carry BP-D24 metadata.
- `02-gates/` — six runnable gates + `enriched_acceptance` driver with the profile registry.
- `03-procedure/PP_STAGE_PROCEDURE_v1_0_0.md` — gates, honesty tiers, profiles, the honest ceiling.
- `04-proof/PROOF_REPORT_v1_0_0.md` — re-run evidence (assessment / satisfiability / adversarial).
- `05-fixtures/` — the passing Courseware fixture.
- `lib/axe.min.js` — axe-core 4.9.1 for the WCAG gate.

## Run
```
python3 02-gates/enriched_acceptance_v1_0_0.py --profile Courseware \
  --page <page_abox.ttl> --html <page.html> \
  --ld 01-vocabularies/learning_design_tbox_v1_0_0.ttl \
  --manifest <manifest.ttl> --attest <attestations.ttl>
```

## What it does and does not do (L-40)
Enforces disclosure, structure, automated tests (WCAG via axe-core), and **hash-bound accountable
attestation**; blocks over-claiming (a profile certifies only if its mandatory gates pass; a standard is
claimable only with passing evidence or a fresh sign-off). It does **not** certify pedagogical excellence,
quantitative model validity, or learning outcomes — those are TIER-C human judgments (enforced as required,
change-tracking sign-offs) or post-ship empirical evidence. Effectiveness belongs in a future Stage 5 loop.
