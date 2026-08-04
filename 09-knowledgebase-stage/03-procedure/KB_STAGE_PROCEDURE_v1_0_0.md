# RDODI Stage KB — Knowledgebase (procedure v1.0.0)

**Ecosystem:** lifts RDODI from v1.7.0 to **v1.8.0** (additive; v1.7.0 untouched — BP-D6/D7).
**Source:** `RDODI_Session_Lessons_Proposal_v1_0_0.md` (user upload, preserved at `05-source/`).
**Governing discipline:** OE Operating Discipline v2.0.0.
**Anchoring (L-72):** every pattern that overlaps existing discipline carries a `kb:relatedOEDiscipline` link to a real BP/L code verified against `kb_abox_v1_35_0` (OE Pack v20.1.0).

## What this stage is

A graph-structured RDODI-specific lessons-learned and best-practices knowledgebase. Ten patterns
(R1–R10 from the source proposal) encoded as `kb:LessonsLearnedPattern` individuals, each carrying
evidence (`kb:patternEvidence`), a coverage-check against existing discipline (`kb:coversExisting`),
an integration recommendation (`kb:recommendsIntegration`), and a lifecycle status
(`kb:patternStatus`). Cross-cutting patterns link to their OE-general counterparts via
`kb:companionPattern` (held externally in the OE companion proposal).

## What this stage is NOT

This is **not** ratified procedure. The proposal explicitly says PROPOSED; the patterns marked
`kb:Proposed` are awaiting the RDODI session ratifier's decision. The patterns marked
`kb:AlreadyAdoptedAtGateLevel` are mechanically operational in existing gates/procedure but their
*reasoning* is what this knowledgebase records — so a future build inherits the rationale, not just
the artifacts.

## Honest discrepancies disclosed (BP-D41 / L-40)

The proposal references the predecessor session's ecosystem `v1_5_1`; my current ecosystem is at
v1.7.0 (going to v1.8.0 with this stage). Several specific files the proposal cites are not
guaranteed to exist at the exact paths it names in my current ecosystem:

- `RDODI_OE_ASSESSMENT_BASELINE_v1_0_0.md` (R6) — referenced as in v1.5.1.
- `rdodi_gate_adversarial_test_v1_2_0.py` and `02-gates/fixtures/` (R9) — referenced as in v1.5.1.
- `A4_reference_template_disposition_v1_0_0.md` (R10) — referenced as in v1.5.x.
- `reference_rule_gate_v1_0_0.py` (R8) — referenced as in predecessor ecosystem.
- Methodology blueprint findings F65, F66, F69 (and proposed F71/F72/F73) — held in the predecessor
  session's `methodology_blueprint_v1_29_0`, **not** in `kb_abox_v1_35_0`.

These are encoded as `kb:externalReference` literals with provenance tags, not as resolved IRIs.
The audit trail is intact; the user's review can confirm or correct each path in the current
ecosystem.

## Pattern lifecycle states

- **kb:Proposed** — offered for ratification; user is the ratifier; Claude must not silently promote.
- **kb:AlreadyAdoptedAtGateLevel** — mechanism operational in existing gates/procedure; reasoning
  not yet codified in the methodology blueprint or procedure note.
- **kb:Ratified** — accepted by the RDODI session ratifier and integrated into procedure or blueprint.

## Gates

| Gate | Requirement | Tier |
|------|-------------|------|
| KB.shacl | merged TBox+ABox conforms to `rdodi_knowledgebase_shacl_v1_0_0.ttl` under `inference=rdfs`; 0 Violations | A |
| KB.coverage | every pattern carries label + skos:definition + patternCode + evidence + coverage-check + integration-recommendation + status | A |
| KB.audit | summarises pattern count by status and explicitly lists `kb:Proposed` patterns awaiting ratification | A (proxy) |

The gates do not certify the truth of any pattern. They certify that the proposal is graph-complete
and that external references are explicitly flagged rather than silently treated as locally verified.

## How a user ratifies a pattern

1. Read the pattern's `skos:definition`, its evidence's `kb:quotedSourceText` and `kb:transcriptLineRef`,
   and its `kb:proposedAddendumText`.
2. Verify (or flag) the external references against the user's authoritative copy of the
   predecessor ecosystem.
3. If satisfied, edit `01-vocabularies/rdodi_knowledgebase_abox_v1_0_0.ttl` to retract
   `kb:patternStatus kb:Proposed` (or `kb:AlreadyAdoptedAtGateLevel`) and assert
   `kb:patternStatus kb:Ratified`.
4. Bump the ABox to a PATCH version (v1.0.1) — never reuse v1.0.0 for changed content (BP-D7).
5. Re-run the KB gate; record the ratification in the methodology blueprint as a numbered finding.

## Honest residuals (L-40)

- The transcript line citations (R1@6534, R2@1599, R7@1259) are from sessions Claude could not
  re-verify in this build. They are recorded with `kb:transcriptLineRef` and
  `kb:provenanceSession "predecessor-session"`. A user holding the predecessor transcript can verify.
- The OE companion patterns (R6 → BP-X1, R7 → L-X2, R8 → L-X3, R9 → L-X5, R10 → L-X6) are held in
  `OE_Session_Lessons_Proposal_v1_0_0.md`, not in this bundle. Their codes (BP-Xn / L-Xn) are
  placeholders pending OE-session ratification; the linkage is via `kb:externalReference`.
- The knowledgebase does not auto-promote a pattern from `Proposed` to `Ratified`; only a hash-bound
  edit by a qualified ratifier (the user) does that, and the discipline mirrors the Stage P
  `content-correctness` attestation pattern.
