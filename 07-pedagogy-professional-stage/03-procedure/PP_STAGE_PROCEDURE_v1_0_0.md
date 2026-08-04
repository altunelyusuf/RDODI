# RDODI Stage P — Pedagogy & Professional Standards (procedure v1.0.0)

**Ecosystem:** lifts RDODI from v1.5.2 to **v1.6.0** (additive; v1.5.2 untouched — BP-D6/D7).
**Runs after** Stage 4 (interactive page). **Governing discipline:** OE Operating Discipline v2.0.0.
**Anchoring (L-72):** quality vocabulary anchors in ISO/IEC 25010 + OQuaRE; pedagogy in the revised
Bloom taxonomy (Anderson & Krathwohl 2001); accessibility in WCAG 2.2 AA.

## The one honest principle this stage rests on
A gate can enforce that a quality claim is **made, structurally supported, automatically tested where
testable, and signed by a named human where not.** It cannot make a weak treatment good or an invented
number valid. Every gate below is labelled by what it *can* enforce — never dressed up as more.

## Three honesty tiers
- **TIER-A (mechanical):** a runnable check decides it (axe-core WCAG run; DOM label presence; SHACL).
- **TIER-B (declared-and-checked):** the artifact declares a target and the gate checks the declaration is
  present, complete, and internally consistent — it enforces the *claim is made and structured*, not that
  the content is pedagogically excellent.
- **TIER-C (accountable attestation):** irreducibly human (pedagogical soundness, model validity,
  professional adequacy, content correctness). Enforced as a **hash-bound `ReviewAttestation`**: the gate
  verifies a qualified human signed *these exact bytes* and fails on a missing or **stale** sign-off — it
  never asserts the verdict is correct.

## Gates
| Gate | Requirement | Tier | Does NOT certify |
|------|-------------|------|------------------|
| PP.wcag | axe-core run at the declared WCAG level: 0 violations | A | usability beyond automated rules (~30–50% of WCAG) |
| PP.model_provenance | every numeric widget declares `mp:numericModelStatus`; `Illustrative` ⇒ the label is rendered in the DOM; `Validated` ⇒ cited derivation + numeric-conformance test | A | that a `Validated` model is professionally adequate (→ attestation) |
| PP.assessment_rigor | every `ld:AssessmentItem` has ≥3 options, exactly 1 key, per-distractor rationale, a cognitive level, and an assessed objective; every objective has ≥1 item | B | whether items are *good* questions |
| PP.bloom_coverage | every objective declares `ld:bloomLevel`; covered only by an affordance/assessment whose `ld:cognitiveLevel` ≥ the objective's level | B | whether the activity truly builds that cognition |
| PP.overclaim | every standard in the `StandardsConformanceManifest` resolves to a passing automated gate OR a fresh attestation; the declared `DeliveryProfile`'s mandatory gates all PASS | A | — (this is the guard against marketing above the evidence) |
| PP.attestation | each TIER-C scope the profile requires has a `ReviewAttestation` whose `artifactHash` == current bytes | C | correctness of the human verdict |

## Delivery profiles (block over-claiming)
- **Companion** — supplement to a text/lecture; single-source permitted; base RDODI convention only. *(This is the bar the Ch.9 v1.1.0 artifact actually meets.)*
- **Courseware** — standalone teaching; mandates PP.wcag + PP.model_provenance + PP.assessment_rigor + PP.bloom_coverage + a `pedagogical-soundness` attestation.
- **ResearchGrade** — citable; ≥3 independent sources with primary-standard citation + a `content-correctness` attestation.
- **ProfessionalTool** — used for real decisions; all numeric widgets `Validated` + `professional-adequacy` and `model-validity` attestations.

An artifact is certified only at a profile whose mandatory gates all PASS; the verdict is composed from
**only** the gate outputs (L-66) — no synthesis-time "looks ready" judgment.

## Honest ceiling & anti-patterns
- **No count floors.** Depth/assessment are enforced by structure + grounding + a test or attestation, never
  by word/element counts (the Stage4.D count-floor retirement precedent).
- **Attestation integrity.** TIER-C weight rests on the attester; attestations are role-scoped, hash-bound,
  and a missing/stale one is a **FAIL**, not a Warning.
- **Effectiveness is outcome data.** Whether students learned or a practitioner was helped is empirical and
  belongs in an optional post-ship Stage 5 feedback loop (PROV-O evidence) — never a pre-ship gate.
- **Residual (L-40):** the TIER-B substance gates can still be satisfied by fluent-but-shallow content that
  is correctly structured; that gap is closed only by the TIER-C human attestation, not by more automation.
