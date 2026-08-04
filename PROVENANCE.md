# PROVENANCE — RDODI Public Edition v1.0.0

**Derived from:** governed `rdodi_ecosystem` **v1.74.0** (zip SHA-256 `8b33cb3c1ee52e640d8fd93df87c60a4f3a37df9b199ba9bc58703c893ce7a38`, repo `main @ 8e7e7e4`), on 2026-08-03, under the OE Operating Discipline v2.2.0 (ceremony: L-65 enumerate→verify→remove→prove-absence; BP-D2 raw-byte scanning; BP-D7 version identity on every changed file).

**Purpose:** a clean public teaching edition — personal projects, employer references, parallel-workstream records, and internal session records removed; methodology, vocabularies, gates, pipeline, and the Semantic Technologies worked domain retained, fully runnable.

**Retained by explicit decision:** author attribution (Yusuf Altunel, 25 files) and institutional publisher (İstanbul Kültür Üniversitesi, 20 files) — CC BY 4.0 requires attribution; authorship is not private data.

## Excluded (internal / cross-project material)

`24-vaf-adaptation/`, `13-oee-compliance/`, `05-documentation/` (session records incl. the methodology blueprint), `04-worked-example/` (textbook chapter 9/10 material in full), `21-worked-example-stg/JOURNEY_stg_candidate.md`, `26-stage4-navigation-adoption/{ASSESSMENT,PROOF_VERIFICATION,SOURCE_proposal,WIRING}` records, `12-enforcement/{rdodi_variant_admissibility_gate_v1_0_1.py, OE_FORWARDED_PROPOSALS_NOTE, R11_PREFILTER_PROVENANCE}`, `CHANGELOG_v1_74_0.md` + `MANIFEST_SHA256_v1_74_0.txt` (internal chain — replaced by this file + a fresh manifest), 14 superseded `28-…` surface-generator versions + `interactive_html_surface_exemplar_v1_0_0.html` (version clutter), `selftest_v1_22_1.sh` (replaced).

## Modified (all parse-verified; ontologies get `versionIRI` under a `/public/` branch, `priorVersion` → governed version)

| Public file | Was | Change |
|---|---|---|
| `scp_domain_tbox_v4_0_0.ttl` | v3_17_0 | **MAJOR.** The running retail case was grounded in a named real company (the author's employer) with REAL·CITED links. Renaming alone would have fabricated citations — so per the content's own provenance legend, those items were converted to a fictional retailer tagged **ILLUSTRATIVE**, real URLs and real category codes removed, `tax_lcw` → `tax_apparel`. Narrative sections genericized. Also fixes an inherited BP-D7 defect (below) |
| `interactive_page_ontology_tbox_v1_9_1.ttl` | v1_9_0 | Named-site references in three specialization definitions genericized; workstream mentions neutralized; widget-rules namespace updated |
| `interactive_page_ontology_abox_v2_0_0.ttl` | v1_1_0 | **MAJOR.** 5 project Page/Resource individuals removed; 27-individual QA worked-example family renamed to generic anchors (ConceptDemo / BusinessSite / HandbookChapter) with descriptions scrubbed; 6 dangling reference lines removed |
| `document_ontology_abox_v1_1_1.ttl` | v1_1_0 | Header narrative neutralized (workstream/backlog wording) |
| `domain_ontology_tbox_v1_1_1.ttl` | v1_1_0 | Proposal-source strings genericized ("an externally-reviewed enhancement proposal") |
| `rdodi_knowledgebase_abox_v1_4_1.ttl` | v1_4_0 | 4 lesson-provenance narratives: parallel-session names redacted, lesson substance unchanged |
| `definition_conformance_gate_v1_0_1.py` | v1_0_0 | Session-specific default paths → usage error + relative default |
| `rdodi_validation_orchestrator_v1_0_1.py` | v1_0_0 | Hard-coded worked-example path → `RDODI_WORKED_EXAMPLE_MD` env var with honest SKIP |
| `rdodi_interactive_html_surface_generator_v4_1_1.py` | v4_1_0 | Two precedent-name comments genericized; only current version shipped |
| `rdodi_affordance_grounding_gate_v1_1_1.py` | v1_1_0 | External proof-bundle name genericized |
| 7 × `…surface/…rules…_v1_0_1.ttl` | v1_0_0 | Namespace `…/vaf-alignment#` → `…/widget-rules#` (consistently, incl. the interactive TBox) |
| `ingest_source_v1_0_1.py`, fixtures, `sample_intent_demo_course_v1_0_0.ttl`, `demo_validation_config.json`, several READMEs | — | Chapter-anchored fixture namespaces/ids (`ch9`/`ch10`) → `demo`; stg governance `oee:`/authority IRIs → neutral `external-authority#ExternalOEAuthority`; stale filename references updated |
| `selftest_v1_22_2.sh` | v1_22_1 | Rewritten against the public tree only |

**Not changed:** everything else — including `domain_ontology_abox_v1_0_1.ttl` and all SHACL suites — byte-identical to the governed v1.74.0.

## Verification performed on this edition (executed, not asserted)

Parse **66/66** TTLs · SHACL **domain** and **interactive-page** suites: conforms, 0 violations, 0 warnings · pipeline end-to-end on the public domain: generator OK, **Definition Conformance Gate 13/13**, generated page marker-free · `./selftest_v1_22_2.sh` PASS · **absence proof PASS**: zero occurrences tree-wide (content *and* filenames) of any excluded project/company/workstream marker · manifest `MANIFEST_SHA256_v1_0_0.txt` self-check clean, round-trip verified from the zip.

## Findings reported back to the governed lineage (not fixed there by this edition)

1. **BP-D7 misalignment in governed `scp_domain_tbox_v3_17_0.ttl`**: `versionInfo "3.17.0"` vs `versionIRI …/3.16.1` — carried since v3.17.0's metadata patch.
2. **Version clutter in governed `28-…/06-s6-exemplar/`**: 15 generator versions and 2 exemplar versions shipped side-by-side, against the no-multi-version-clutter rule.
3. `13-pipeline/PACKAGE_13_DEFINITION_CONFORMANCE_BACKLOG_v1_0_0.md` is retained here as a frozen historical planning record; its line-number references describe the v1_9_0-era generator.
