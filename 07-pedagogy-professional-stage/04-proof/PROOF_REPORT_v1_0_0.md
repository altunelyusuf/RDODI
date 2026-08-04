# Proof Report — PP-Stage Gates v1.0.0  (re-run, not asserted; L-65)

All runs below were executed against real artifacts. The WCAG gate runs axe-core 4.9.1 headless.

## 1. The gates encode the prose assessment of the Ch.9 v1.1.0 artifact
- **@ Companion → CERTIFIED.** No standards over-claimed; profile requires no attestation. This is the bar
  the artifact actually meets.
- **@ Courseware → REFUSED**, with the exact gaps named in the fitness assessment:
  - PP.wcag FAIL — axe-core wcag2aa: `color-contrast` (serious, 40 nodes). *A real defect, previously only flagged as "unaudited".*
  - PP.model_provenance FAIL — `widget_CostOfQuality` and `widget_Rework` declare no `numericModelStatus` (the invented cost-of-quality formula was undisclosed).
  - PP.assessment_rigor FAIL — no `ld:AssessmentItem` (self-check questions are not graded assessment).
  - PP.bloom_coverage FAIL — all four objectives lack a declared Bloom level.
  - PP.attestation FAIL — no `pedagogical-soundness` sign-off.

## 2. The gates are satisfiable (passing fixture @ Courseware → CERTIFIED)
A minimal accessible fixture with a labelled `Illustrative` numeric widget, one rigorous assessment item,
a Bloom-levelled objective covered at level, a manifest claiming WCAG 2.2 AA + Bloom, and a hash-bound
`pedagogical-soundness` attestation passes all six gates — axe-core: 0 violations.

## 3. The honesty cannot be gamed (adversarial)
- **Stale attestation:** mutating the certified fixture by one byte changes its hash; the prior sign-off no
  longer matches → PP.attestation FAIL → REFUSED.
- **Over-claim:** declaring WCAG 2.2 AA on the contrast-failing v1.1.0 page → PP.overclaim FAIL (a standard
  cannot be claimed unless its gate passes) → REFUSED.

## Verdict
The pipeline now mechanically reproduces the human fitness judgment, catches at least one real defect the
prose missed, refuses over-claiming, and requires fresh accountable sign-off for the dimensions automation
cannot reach — while honestly disclosing that TIER-C correctness and learning-outcome effectiveness remain
human/empirical, never certified by the gates.
