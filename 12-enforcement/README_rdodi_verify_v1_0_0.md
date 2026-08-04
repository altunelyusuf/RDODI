# RDODI Verification Suite v1.0.0 — Offloading Mechanical Verification from the Human

Purpose: remove the mechanical checking a human does by hand (reading every sentence, checking every
reference, re-verifying counts) so their attention goes only to judgment, and so academic/industrial work
products reach review-grade faster. The human reads a one-page validation sheet, not the whole document.

## Modules
- `rdodi_verification_lib_v1_0_0.py` — Instrument 4 (exact-match substrate) + Instrument 1
  (insertion/retention verifier) + Instrument 3 (number/count reconciler).
- `rdodi_reference_auditor_v1_0_0.py` — Instrument 2 (reference existence+tier resolution, F86 points-to
  check, cite<->ref reconciliation, warrant surfacing).
- `rdodi_validation_orchestrator_v1_0_0.py` — Instrument 5: runs all checks, emits mechanical-floor
  pass/fail + the human validation sheet.

## What is automated (human need NOT re-check)
- insertions actually landed (wrap/emphasis-safe exact match)
- no silent regression on rewrite (citation count, concept checklist, sections, tables, figures)
- every claimed number re-derived from the artifact and reconciled
- every reference resolved to its highest catalogue tier; identifier POINTS-TO verified (review-vs-work)
- in-text citations reconcile with the reference list (exact author-year)

## What is SURFACED for the human (judgment — never decided by the tool)
- warrant: does each confirmed-real source support the specific claim made of it?
- document intent: what the artifact is for
- references at Indirect/unresolved tier needing an edition decision

## Validated against this session's real failures (test-driven)
- F90 regression (v7.1->v8.1): correctly FLAGGED (citations 9->0, lost concepts listed).
- Silent Mars-story insertion (absent in v9.3 body): correctly FLAGGED missing.
- v10.1.0 citation count: correctly RECONCILED (17==17).
- F86 review-vs-work: "Deming 1986" correctly tagged Indirect (resolved to a review of the book).

## Usage (next domain — Instrument 6 bootstrap)
```python
from rdodi_validation_orchestrator_v1_0_0 import run, render_sheet
rep = run(text, prior_text=old, concept_checklist=[...], expected_insertions={...},
          claimed_numbers={...}, rederivations={...}, references=[...], intent="...",
          do_live_refs=True)   # do_live_refs=True hits Crossref/OpenLibrary
print(render_sheet(rep))
```
Point it at a new domain's draft + reference list; the mechanical floor and validation sheet are domain-neutral.

## NOT claimed
This suite does not judge factual truth or warrant, and does not author intent — by design. It guarantees
the mechanical floor so the human spends their whole budget on those irreducible judgments.
