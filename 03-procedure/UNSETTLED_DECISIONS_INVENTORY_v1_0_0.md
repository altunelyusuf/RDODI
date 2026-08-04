# Inventory of Recorded Unsettled Decisions

**Compiled:** 2026-05-28
**Method:** BP-D2 — extracted by reading the actual source files this session, each item cited to file + line so it is independently verifiable.
**Sources scanned:**
- `RDODI_FourStage_Pipeline_Procedure_v1_0_0.md` (the pipeline procedure)
- `methodology_blueprint_v1_27_0.md` (the running findings blueprint, F1–F58)
- `RDODI_Ontology_Adequacy_Audit_Findings_v1_0_0.md` (the adequacy audit)

This inventory lists decisions that the records themselves mark as *not yet made* — deferred, pending, undecided, or explicitly flagged as an open question. It does **not** list completed findings. Where a record says "decided" the item is excluded.

---

## Group A — Recorded in the pipeline procedure (§7 "What this procedure does NOT include" + §8)

These are the procedure's own honest-scope disclosures.

**A1. No mechanical validator ships.** (procedure line 172)
`validate_rdodi_pipeline.py` does not exist; the gates are stated in prose, and a runnable validator that mechanically applies them is named a *future deliverable*. (This run implemented the gate checks inline as a one-off; that is not the shipped validator.)

**A2. No stage-discipline TTL artefacts in RDODI v1.0.1.** (procedure line 173)
The operational content (InstructionalChapterCompanion structure template, AcademicResearchReport structure, reference-template inventory) lives only in two legacy `rrwpc_stage{2,4}_artifact_kind_*.ttl` files. Whether to port any of it as RDODI-native stage-discipline TTLs is **"Item 2 in the work sequence"** — explicitly undecided.

**A3. No Bloom's-taxonomy / pedagogy framework.** (procedure line, §7 item 3)
Pedagogical structure for Stage 4 interactive elements is currently determined per-deliverable by the author, with no governing framework. (Relevant to your "rule not numbers" point — Stage 4's affordance gate is the numeric counterpart that lacks a pedagogical rule behind it.)

**A4. No reference-template artefacts.** (procedure line 175)
The legacy `Reference_Template_COM0463_Ch{1,2,4,5}_*` individuals named gold-standard exemplars at specific byte/LOC/widget counts. Whether those carry forward into RDODI's procedure is part of **Item 2's** disposition — undecided.

**A5. Stages 1 and 2 have no reference-template inventory.** (procedure line 176)
The procedure states their gates but points at no exemplar deliverable. Authoring such exemplars is named a **v1.1.0 enhancement** — deferred. *(This is the item directly under your current question: the ≥40 figure is asserted in the gate table with no exemplar and no rationale behind it.)*

**A6. Disposition of the two referenced legacy stage-discipline TTLs.** (procedure lines 183–184)
`rrwpc_stage2_artifact_kind_v1_0_0.ttl` and `rrwpc_stage4_artifact_kind_v1_1_1.ttl` — "Disposition (port to RDODI vs leave as legacy reference) decided in Item 2." Undecided.

---

## Group B — Recorded in the methodology blueprint (deferred / pending findings)

**B1. Standardization-vocabulary primitive: placement decided, build deferred.** (blueprint line 118, F5)
The claim-representation primitive belongs in OE KnowledgeBase, and RDODI's `Finding` class should descend from it. "Placement decided; build deferred — a versioned OE KB release, MINOR." Build not done.

**B2. The richness-metric usage decision is deferred.** (blueprint lines 139 & 279, F35)
The ratio-based richness metric was shown to mislead on dense ontologies (penalizes breadth-addition). An absolute-count or field-coverage companion measure is argued for but not chosen. "Metric-usage decision deferred (user: metrics under investigation)… the output stage is its arbiter." Open.

**B3. 8-subsystem content-first rebuild — pending execution.** (blueprint line 206)
"8 subsystems rebuilt content-first on WITHIN-only content; BEYOND step (§14) was skipped (F32) — now locked and pending execution for all 8." Pending.

**B4. The QM subsystems are reclassified SKELETONS pending content-first rebuild.** (blueprint lines 123 & 199, F19)
The 9 QM subsystems were retracted from "done" to "taxonomic skeletons"; they are "the baseline to REBUILD content-first, not a finished deliverable." Rebuild pending.

**B5. Element-wide enrichment retrofit required for all 8 subsystems.** (blueprint line 137, F33)
WITHIN-built relationships carried ~0 passages; correction requires re-enriching WITHIN relationships + deep BEYOND across all 8. "Retrofit required." Not done.

**B6. Document-intent layer (step 0) — designed, not built.** (blueprint line 166, F52)
The facet map is researched and grounded (DCMI umbrella + value vocabularies), and a review-surface catalog exists, but the governed `DocumentIntent` schema is not built and the human's actual intent for any specific document is not yet captured/wired as step-0. "NEXT after user approves menu: build governed DocumentIntent schema… capture user's actual intent for THIS document, wire as step-0." Build pending. **This is the most consequential open item for "is the survey the document the human wanted?" — the pipeline currently has no intent layer, so document shape is still selected without explicit human intent capture.**

**B7. Domain-backbone pattern — validated once, generalization deferred.** (blueprint line 172, F55 item 2)
Validated on PQM v2.1.0 with measurable improvement (DIT 4→5, NOC 0.31→0.69); "generalization untested; recorded as validated on one case, generalization deferred to natural next domain ontology." Generalization open. *(The Ch.9 run just performed was arguably the "natural next domain ontology" — but I did not run the backbone-pattern metrics on it, so the generalization remains untested even now.)*

**B8. Epistemic-source (PROV-O EstimationMethod) layer — design only, build deferred.** (blueprint line 172, F55 item 3)
Design fixed (PROV-O Entity/Activity/Agent with DirectDeduction / ContextualEstimate / ResearchEstimate subclasses); "build deferred until populated cost instances exist." Pending.

**B9. Upper-ontology anchoring — resolved to instance-level, not yet populated.** (blueprint line 172, F55 item 1)
Test-drive found no TBox-level OVERLAP with QUDT/PROV-O; anchoring "activates at the INSTANCE level… when populated data exists." No populated instance data exists yet, so the pattern is designed but dormant.

**B10. "Build into a real usable system" — committed, not yet built.** (blueprint line 250)
Generalizing the Ch.9 test-drive slice into a standing domain-ontology stage (all source concepts, all subsystems, auto-OE-assessed) is "committed, not yet built."

**B11. OE quality-gates clause (d) — the principal open gap.** (blueprint line 233)
Against the v1.2.0 completion criterion: tiering ✅, no-truth-certification ✅, verified-sources sample-only, traceability machinery-only, human-cost n=1 — but "(d) OE quality gates (SHACL, coverage ≥80%, OE frameworks) — NOT YET RUN — the principal open gap. Next action: run clause (d)." *(The Ch.9 run partially addressed this — it ran SHACL and coverage — but on a fresh pipeline artifact, not on the corpus this criterion referred to.)*

---

## Group C — Recorded in the adequacy audit

**C1. SemVer mode choice is conditional, decided per-bundle.** (audit line 66)
Per BP-D13, PER-BUNDLE (ORIGINATION) vs ECOSYSTEM (CONTINUATION) SemVer "depends on whether a predecessor of matching scope exists." Not a standing decision; re-evaluated each release. (Listed for completeness — it is a recorded conditional, not a parked task.)

---

## The pattern across these items

Nearly every open item shares one shape: **something was specified or asserted before the discipline behind it was grounded.** The ≥40 references (A5), the richness metric (B2), the skeleton subsystems (B4), the intent layer (B6), the backbone generalization (B7) — each is a place where a number, a measure, or a structure was put in place ahead of the rule/evidence that would justify it. Your instinct on the ≥40 ("set a rule rather than a number") is the same correction these items are all waiting for, applied to one of them.

The two that most directly affect whether the pipeline produces *trustworthy research output* (as opposed to *structurally valid output*):
- **A5 / the reference rule** — what counts as adequate citation for a survey, expressed as a rule not a count.
- **B6 / the intent layer** — whether the document is the one the human intended, which the verification machinery structurally cannot certify.

Neither is decided. Both are recorded as pending in the sources above.
