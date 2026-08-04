# R4 — PROV-O Deepening v1.0.0
Deepens the hybrid provenance spine (Cross.B model C) with factual activity/agent provenance and GROUNDED epistemic typing.

- **13-pipeline/rdodi_artifact_generator_v2_6_0.py** — emits, in addition to the wasDerivedFrom chain:
  a `prov:Activity` (generation) `prov:used` the domain ontology and `prov:wasAssociatedWith` a
  `prov:SoftwareAgent`; the artifact `prov:wasGeneratedBy` the activity and `prov:wasAttributedTo` the agent
  (all FACTUAL). Each section gets one `epist:sourceType` grounded in the section's OWN source.
- **epistemic_tbox_v1_0_0.ttl** — Verbatim / Paraphrase / DeclaredMixed / Unspecified.
- **rdodi_prov_completeness_check_v1_0_0.py** — PASS requires activity+agent+wasGeneratedBy AND every epistemic
  type traceable to a domain source declaration (0 invented).

## Honesty (L-66) — and a real catch
Epistemic precision is NEVER invented. On the demo fixture the result is 6 DeclaredMixed + 1 Unspecified — faithfully
reflecting that the domain declares "verbatim-OR-paraphrase" imprecisely. During build, the check caught the
generator borrowing a fallback source's type (overclaim); fixed to type by each section's OWN source. PASS,
0 invented. Cross.B regression: still 7/7.
