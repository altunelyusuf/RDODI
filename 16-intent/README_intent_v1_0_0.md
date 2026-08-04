# B6 — Document-Intent "Step 0" Layer v1.0.0
Instruments authorial intent BEFORE generation and checks the result against it.

- **intent_tbox_v1_0_0.ttl** — domain-neutral intent vocabulary: Intent, intendedGenre, mustCoverConcept,
  mustCoverArea, excludedConcept, declaredAudience, scopeNote (concepts/areas by IRI — no domain hardcoding).
- **sample_intent_demo_course_v1_0_0.ttl** — example intent (must cover ChangeControl, CostOfGoodQuality,
  CostOfPoorQuality, ConfigurationManagement; exclude DevOpsQualityCulture; genre course-document).
- **13-pipeline/rdodi_artifact_generator_v2_5_0.py** — intent-aware: `generate(..., intent_ttl=...)` brings
  uncovered must-cover concepts to the front and drops excluded ones (step 0 drives generation).
- **rdodi_intent_gate_v1_0_0.py** — MECHANICAL conformance only: must-cover covered? exclusions respected?
  genre matched? It does NOT certify the artifact fulfils the author's deeper intent — that is tier-C human (L-66).

## Verified loop (L-65)
WITH intent → 4/4 must-cover covered, exclusions respected, genre match → PASS.
WITHOUT intent → 2/4 covered (ChangeControl, ConfigurationManagement missing) → FAIL (not relaxed).
