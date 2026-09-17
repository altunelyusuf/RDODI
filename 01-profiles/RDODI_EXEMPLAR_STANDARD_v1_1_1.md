# RDODI Exemplar Standard v1.1.1

**Status:** adopted by the RDODI governor, 2026-08-06 · **Governs:** every future RDODI byproduct (Stage 1–4 output set) · **Mechanism:** cite-not-import — the exemplar artifacts remain in their owning package (`semtech-landscape/`, this monorepo) and are pinned here by SHA-256; RDODI references, never copies or mutates them (L-X7).

## 1. The exemplar

The **semtech-landscape** byproduct at **v6.9.0** (package manifest 472/472 self-verified on adoption day; manifest file SHA `d5a3984304ff9d961690028b2398cf8fe1dcf2f038126d61bfa664254a49de12`) is designated the reference standard for what a completed RDODI byproduct looks like. The four artifacts:

| Stage | Artifact (path in `semtech-landscape/`) | SHA-256 |
|---|---|---|
| 1 — Research | `01-research/semtech_research_v6_9_0.ttl` (1048 triples) | `64e769f54629c06e56c75ae0f9752d73e66b774f908cca57a325407954d073a7` |
| 2 — Domain ontology | `02-ontology/semtech_tbox_v6_9_0.ttl` (1378 triples) | `4e8414a8e02a700e02160e6c301f5e03917eec59d7d5352397c029d5135ec835` |
| 3 — Document | `03-document/semtech_document_v6_9_0.docx` + companion `.ttl` (563 triples) | `8a8440cc20ccef87d8271097631439c5eb30dd953ec9393b0d973fde5626d14d` / `8771a06cd8dfa9686f3e5b73da28036002bf03a7aa03178f0f7c74cf35344fb9` |
| 4 — Interactive page | `04-page/semtech_page_v6_9_0.html` (991,976 b, single file) | `58986633bbb4bacd88f3463c03e75532b9191e687842f751ba34e4beea153dc1` |

*(All hashes recomputed from the files on adoption day, not copied from their manifest — R16.)*

## 2. The bar — mechanisms, not admiration

A future byproduct **meets the exemplar standard** when all of the following hold. These are the mechanisms the proposal (`Proposal_RDODI_Enhancement_semtech_landscape_v1_0_0`, adopted v1.75.0) documented as the *cause* of the exemplar's quality; reference magnitudes from v6.9.0 are given for calibration, not as thresholds.

1. **R21 gate chain, from day one.** Four separately-runnable programs — structural validator, content-specific supplementary gates, cross-stage procedure audit, live DOM/interaction smoke test — chained by one release-check script that the publish step refuses to bypass. Instantiate from `14-bootstrap/templates/` (`release_check_template_v1_0_0.sh`, `gate_suite_template/`). *Reference: 10+ validator gates, 40 supplementary, 22 procedure, 149 DOM checks by v6.9.0 — grown by addition, never restructured.*
2. **Gates grow with every release.** Each release that fixes a real defect adds the gate that would have caught it (the exemplar grew 29→40 supplementary gates this way). A fixed defect without a new gate is an open recurrence.
3. **Closure healthcheck.** The byproduct is not complete until a full cross-artifact healthcheck runs clean: R16 numeric reconciliation re-derived from *each* artifact directly, R17 git-freshness before any "missing" conclusion, citation/registry integrity. Instantiate from `healthcheck_template_v1_0_0.py`.
4. **Coverage closed, honestly counted.** Leaf-level subject coverage is tracked in a BRSF backlog with denominators re-derived on closure (R20) — the exemplar closed all 47 leaf areas after correcting its own miscounted denominator openly.
5. **Content honesty.** Every factual claim carries a source or an honest disclosure of unavailability (the exemplar disclosed an unavailable source rather than fabricating); provenance tiers marked; no reader-facing build-process language in the final document.
6. **BRSF-compliant program tracking.** The byproduct's fit-gap backlog validates 0-violation against the *current* BRSF shapes (`backlog-roadmap-framework/`, check version — it drifts), with `notYetScoreable`+reason on unscored items and ReleaseEvidence carrying real package hashes. **Reference register:** the exemplar's own `fitgap_backlog_v1_22_0.ttl` (SHA-256 `81b58ac6386cfb7960c95862bc2e6346321635b0eb2c076019b5c98b7c6b5c11`, 693 triples, delivered out-of-band 2026-08-06, re-validated CONFORMANT 0-violation with `backlog_validate_v1_3_0` on receipt; at time of writing (v1.1.0) their last in-repo publication was v1_19_0 -- **superseded 2026-08-06 by semtech-landscape v6.9.1/v6.9.2, which pushed fitgap_backlog_v1_22_0.ttl then v1_23_0.ttl into governed history, closing that gap; the reference pin above (v1_22_0) is retained as the register this standard adopted, not a claim about current in-repo state**) — the shape that tracked all 27+ of the exemplar's own epics.

## 3. What this standard is not

Not a widget-count or page-size quota; not a requirement to reach 41 releases; not a license to copy the exemplar's content. A small byproduct with the full mechanism set at small magnitudes meets the bar; a large one missing the gate chain does not.

## 4. Provenance

Derived from the semtech-landscape enhancement proposal + handover (files.zip SHA `35d65f527a7bf56a3f2c2fc0854647d59ab8c21b0b453b2af75c3905fc8974f4`), adopted with patterns R16–R21 (kb:Proposed) in v1.75.0. The sender's corrected handover package v1.1.0 (zip SHA `e893db8c15febcd8e7a1476e2fb5369ffdf5802bd5c4390dade940ea1ca489a8`, internal manifest 9/9 verified) added a top-level manifest in response to RDODI's packaging observation; all substantive files verified byte-identical to the adopted v1.0.0 set — nothing re-merged. v1.1.0 of this standard adds the reference-register pin above. This standard operationalizes the proposal's §2–§4 "how" as RDODI policy. Enforcement wiring (bootstrap default — Enhancement Plan item C2) is tracked in `rdodi_exemplar_program_backlog_v1_0_0.ttl` (EP5).


## v1.1.1 (2026-08-07) — PATCH: provenance note corrected, no vocabulary change
Confirmed via disk re-verification that the four exemplar artifacts (research, domain
ontology, document, interactive page) are unchanged from v6.9.0 and still SHA-match this
standard's pins -- semtech-landscape v6.9.1/v6.9.2 were both content-free PATCHes.
However, this doc's own **provenance (Section 4)** had drifted: it stated the exemplar's
reference backlog register was "delivered out-of-band ... last in-repo publication was
v1_19_0" -- true when v1.1.0 was written, no longer true after v6.9.1/v6.9.2 pushed
`fitgap_backlog_v1_22_0.ttl` then `v1_23_0.ttl` into the exemplar's own governed history.
Corrected in place with the state-at-time-of-writing preserved (BP-D2: the old claim was
accurate for its moment, not fabricated) rather than silently rewritten. No mechanism,
pin, or SHA in Sections 1-3 changed.
