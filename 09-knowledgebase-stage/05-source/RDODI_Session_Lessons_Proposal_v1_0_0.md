# RDODI Session — Lessons & Best-Practices Proposal v1.0.0

**For:** the RDODI session (owner of the four-stage pipeline + procedure + widget stage).
**From:** mining of the shared conversation transcript spanning predecessor and current RDODI sessions.
**Companion file:** `OE_Session_Lessons_Proposal_v1_0_0.md` — addressed to the OE governance session, with the cross-cutting candidates framed as general governance principles. Both files originate from `Conversation_Lessons_Proposal_v1_0_0.md`.

**Status (L-40):** PROPOSED PATTERNS / adopt-this-pattern directives, NOT ratified procedure changes. Each is grounded in a transcript incident (line citation) and tied to a real artifact in the current package (`rdodi_ecosystem_v1_5_1`).
**Discipline followed:** BP-D2 (transcript read raw), BP-D41 (every claim line-cited), L-72 (dedup against existing RDODI procedure v1.2.0 and existing OE BPs/Ls), L-66 (no synthetic taxonomy).

---

## What this file contains
**Five RDODI-specific patterns** (the procedure-level lessons that emerged from real session incidents), plus **five cross-cutting patterns** that have RDODI applications but also general OE relevance (also present in the OE file as governance principles). Each cross-cutting pattern is framed here as an *adopt-this-pattern* directive bound to the procedure / gates already in v1.5.1; the OE-general principle is referenced.

The RDODI session's role on this file: **integrate any of these as procedure addenda, blueprint findings (F71+), or methodology notes**. None of these change the procedure's existing gates (Stage4.H–K, reference rule, etc., are already adopted); they record the *patterns those gates implement* so a future build inherits the reasoning, not just the artifacts.

---

## RDODI-specific patterns (5)

### PATTERN R1 — **Each stage has its own quality vocabulary; no umbrella QualityDimension class across stages**

**Pattern.** A research-stage artifact's quality has nothing to do with keyboard-accessibility; an interactive-page-stage artifact's quality has nothing to do with Harvard citation form. Collapsing into one polymorphic QualityDimension class with cross-stage instances hides this fact and forces every consumer to disambiguate at query time.

**Evidence.** Transcript line 6534: *"Each stage's quality is shaped by what that stage produces. A research artefact's quality has nothing to do with whether buttons are keyboard-accessible; an interactive page's quality has nothing to do with Harvard citation form. Collapsing them into one QualityDimension class with 8 named instances (the way the legacy bundle did) hides this fact."*

**Existing-coverage check.** BP-D32 (InteractivityCouplingMustEncodeDomainSemantics) is adjacent but addresses *interactivity*, not *quality-vocabulary-by-stage*. The RDODI procedure v1.2.0 already implements this stage-by-stage at the gate level (Stage1–Stage4 each have their own acceptance gates); the underlying vocabulary discipline is currently implicit.

**RDODI form.** The RDODI quality vocabulary uses stage-specific subclasses (already followed in stage-specific gates). SHACL shapes attach to the stage-specific classes, narrower not broader. When future quality vocabulary is added, do not introduce an umbrella class spanning stages.

---

### PATTERN R2 — **Quality does not propagate across pipeline stages — the polished report does not yield a polished page automatically**

**Pattern.** A polished research report at the document stage does not yield a polished interactive page at the page stage — quality is not transitive across the RDODI pipeline. The page must be governed at its own stage with its own gates. This pattern motivated the entire widget-stage adoption (Stage4.H–K).

**Evidence.** Transcript line 1599: *"Report is almost perfect, yet HTML file is disappointing. It seems the RRWPC pipeline is not properly applied for the HTML generation."* — followed by 6 specific page-level defects under an upstream-polished report. The entire procedure v1.1.0 widget-stage adoption (and the intention-coverage gate) is the engineering response to this pattern.

**Existing-coverage check.** The widget gates (Stage4.H/I/J) and Stage4.K (intention-coverage) in procedure v1.2.0 *implement* this lesson, but no procedure note or blueprint finding names the underlying principle: quality is not transitive across stages. F69 (OE baseline) names the symptom (no positive end-to-end exemplar); this pattern names the *reason*.

**RDODI form.** Record as a blueprint finding (proposed F71): "Quality does not propagate across RDODI stages — each stage gates its own output. An upstream PASS never licenses a downstream PASS. The widget-stage adoption (Stage4.H–K) is this principle's structural response."

---

### PATTERN R3 — **Intention-coverage is ONE-HOP (intention-as-unit), settled by test-drive on a separating case**

**Pattern.** Coverage-unit in `intention_coverage_gate_v1_0_0.py` is the **intention** (LearningObjective), not the **subject** the intention is about. The two-hop schema would launder an uncovered intention into "covered" because its subject was covered by a different intention's widget. The schema choice was settled by building a separating case (two intentions sharing one subject, widget covers one) and observing the manifests differ on the uncovered intention's status.

**Evidence.** F65 in methodology_blueprint_v1_29_0; `intention_coverage_gate_v1_0_0.py` adversarial test (7/7); the test-drive run in this session that authored the gate. Confirmed in CLEAN_SESSION_BOOTSTRAP_v1_2_0.

**Existing-coverage check.** Already encoded in Stage4.K and the adversarial test; the *reason* is recorded as F65. This pattern preserves the meta-lesson: **build the separating case rather than choose a schema by preference**, applicable whenever a schema fork has a case that distinguishes the readings.

**RDODI form (already adopted; record as method-pattern in methodology blueprint, proposed F72):** When a schema choice has a *separating case* (an input on which the readings yield different output), the test-drive — not preference — is what decides. The richer-looking option may lose on evidence (two-hop did). This is the canonical example of the rule-vs-number / test-drive discipline applied to schema design.

---

### PATTERN R4 — **Asymmetric coverage gate: widget-without-intention FAILS (decoration); intention-without-widget DISCLOSES (scope)**

**Pattern.** Coverage gates should not be symmetric by default. The page cannot demonstrate everything in the ontology, but it can never contain interactivity that demonstrates nothing. So uncovered intentions are honest scope-disclosure (reported, not failed); widgets matching no intention are decoration and fail.

**Evidence.** Procedure v1.1.0 Stage4.K; F66 in methodology_blueprint_v1_29_0; `intention_coverage_gate` code: *"a widget covering no declared intention = FAIL (decoration). An intention with no widget = DISCLOSED SCOPE (reported, NOT a fail)."*

**Existing-coverage check.** L-40 (ObservationsVsDecisionsInDisclosures) addresses disclosure language but not the asymmetric pass/fail design itself. Adopted in RDODI v1.1.0; the pattern is already operational.

**RDODI form (already adopted; record as design-pattern in blueprint, proposed F73):** When designing any coverage gate in the RDODI procedure (or extending it), explicitly answer two questions: (a) which direction is a real defect (the thing the gate must fail on), (b) which direction is honest scope-disclosure (the thing the gate must report-but-not-fail). Default-symmetric coverage gates either over-strict or over-permissive; the asymmetry must be intentional.

---

### PATTERN R5 — **The negative-exemplar pattern: ship at least one worked example designed to FAIL the gates**

**Pattern.** The Ch.9 worked example fails the RDODI gates *by design* — it is the negative exemplar. A gated pipeline without a negative exemplar gives no evidence its gates are load-bearing. The positive exemplar (EX) may not yet exist; the negative is the proof-of-failure-mechanism.

**Evidence.** Session closure record; `CLEAN_SESSION_BOOTSTRAP_v1_2_0.md`: *"The worked example is a NEGATIVE exemplar by design — has 0 of everything the gates check."* Confirmed by the OE baseline run where Ch.9 has 0/27 widget markers and fails Stage4.H/I/J/K.

**Existing-coverage check.** L-65 (VerifyBeforePublishing) requires the gate fails on bad input, but doesn't address *shipping a worked example as the bad input* so the failure is permanently demonstrable. This is the design counterpart: ship the negative.

**RDODI form (already adopted in Ch.9; record as procedure addendum, proposed methodology note):** the RDODI procedure requires that every gated pipeline ship at least one negative worked example — an artifact the gates fail on by design, with the failure mode stated. A pipeline that only ships positive examples cannot be trusted to gate anything. (The EX gap — no positive exemplar yet — is the *other* side of this discipline; both are required, neither substitutes for the other.)

---

## Cross-cutting patterns (also in the OE file as governance principles)

These have OE-general framings in the OE file. Here they appear as *adopt-this-pattern* directives bound to the current procedure / gates.

### PATTERN R6 — **"0 violations" / conformance claims in RDODI documentation must name shape version AND method**

**Adopt-this-pattern.** Any "N violations" / "conforms" claim in any RDODI README, blueprint, baseline, or procedure note must name, in the same sentence: shape version, imports policy, corpus scope, exclusions. The OE baseline was corrected to this form in v1.5.1 after the parallel-OE-session caught my earlier under-specified "0 violations" claim.

**Already-applied location.** `RDODI_OE_ASSESSMENT_BASELINE_v1_0_0.md` correction section in v1.5.1. The wording rule applies forward to all RDODI documentation.

**See OE file for the general principle (BP-X1).**

---

### PATTERN R7 — **Two-rounds-of-guessing antipattern: stop on the second identical user challenge**

**Adopt-this-pattern.** When a user repeats the same challenge against an RDODI build/decision, the next action is a direct ask (e.g. `ask_user_input_v0`), not another iteration. The transcript line 1259 incident occurred during predecessor RDODI work; the discipline applies forward.

**See OE file for the general principle (L-X2).**

---

### PATTERN R8 — **Cross-LLM bibliography labels: CORROBORATED, not VERIFIED**

**Adopt-this-pattern.** Any reference list reaching RDODI's reference rule via a parallel LLM session must be labeled CORROBORATED until resolved against an authoritative non-LLM source. The reference rule's BP-D41 verification cannot be satisfied by another LLM's claim.

**Already-applied at gate level.** The reference rule gate (`reference_rule_gate_v1_0_0.py`) already checks status `verified` / `unavailable_flagged` / `unverified`. Adding a `corroborated` tier as an intermediate value would make the cross-LLM case explicitly tractable rather than forcing it into `unverified`.

**See OE file for the general principle (L-X3).**

---

### PATTERN R9 — **Adversarial harness tests must be hermetic from the package — package-relative paths, bundled fixtures**

**Adopt-this-pattern.** All RDODI adversarial tests resolve paths via `__file__` and bundle every fixture. The remediation from `rdodi_gate_adversarial_test_v1_1_0` (5 absolute paths, 3 unbundled fixtures, claimed "13/13 verified" but unreproducible) to `_v1_2_0` (hermetic, 13/13 actually reproducible from files) is the canonical implementation.

**Already-applied location.** `02-gates/rdodi_gate_adversarial_test_v1_2_0.py` and `02-gates/fixtures/` in v1.5.1. The pattern applies forward to all future RDODI tests.

**See OE file for the general principle (L-X5).**

---

### PATTERN R10 — **Disposition wording must be scoped to exactly what is being retired**

**Adopt-this-pattern.** Every RDODI disposition statement (A-series items, future closeouts) names exactly what is being retired, what remains intact, and what becomes of the residual. The A4 disposition's first wording over-reached (read as retiring pages, not just count-metrics); the correction section records the fix.

**Already-applied location.** `A4_reference_template_disposition_v1_0_0.md` correction section in v1.5.x.

**See OE file for the general principle (L-X6).**

---

## Patterns already covered — no new RDODI lesson needed (L-72 dedup)
- **Stage4.D count floors retired in favor of rule-not-number** (Stage4.H–K, procedure v1.1.0): an application of L-66 to the RDODI stage-discipline, not a new lesson.
- **≥40-reference count retired for grounded reference rule** (procedure v1.2.0): same — application of L-66 to the reference gate.
- **OE quality gates apply to RDODI** (the OE assessment baseline this session): an application of the OE governance framework, not RDODI-specific.

---

## Honest residuals (L-40)
- The "already adopted" patterns (R1–R5 are mostly already operational in v1.5.1) — this proposal records their *reasoning* in the blueprint, not new procedure clauses. A reader inheriting only the gates without these patterns would lack the rationale.
- The cross-cutting patterns (R6–R10) overlap with the OE file by design; the framings differ. Neither file is complete without the other.
- Every pattern is PROPOSED; integration into procedure / blueprint is the RDODI session's call.

## Recommended next-action
The RDODI session: (1) integrate R1–R5 into methodology_blueprint as F71–F73+ findings (the R1–R5 numbering above is illustrative, not procedure-binding), (2) add a procedure addendum noting the negative-exemplar requirement (R5) and asymmetric-coverage-design principle (R4), (3) verify the cross-cutting patterns (R6–R10) align with what's already in v1.5.1 documentation; correct any drift.
