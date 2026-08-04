# RDODI Domain Ontology Contract — v1.0.0
# The vocabulary a domain ontology must provide so the pipeline can generate an interactive
# HTML page AND an academic report from it, for ANY domain (not only semantic technologies).

Namespace used below: `d:` = the domain ontology's namespace. The pipeline is namespace-agnostic;
it discovers structure by rdf:type and a small fixed set of annotation properties.

## 1. REQUIRED — minimum to produce any output
| Term | Type | Meaning |
|------|------|---------|
| `d:Area` (was `SemanticTechnologyArea`) | Class | A top-level section. Concepts are `rdfs:subClassOf` an Area. ≥1 required. |
| `rdfs:label` | on Area & Concept | Human-readable name. |
| `d:definition` | annotation on Concept | One-sentence definition (used in tooltips, lead paragraph). |
| `d:Concept` | Class, `rdfs:subClassOf d:Area` | A topic within an area. ≥1 per area. |
| `d:ExampleCase` + `d:ofConcept` | Class + obj prop | A worked example; `d:ofConcept` points to its Concept. |
| `d:Publication` (+ `d:pubAuthor`,`d:pubUrl`,`d:pubNote`) | Class | A cited source. ≥1 recommended. |

## 2. STRUCTURAL CONTENT — per-concept depth (strongly recommended)
| Term | On | Meaning |
|------|----|---------|
| `d:extendedTreatment` | Concept | The main prose treatment (1–2 paragraphs). |
| `d:exampleDomain` | ExampleCase | The sub-domain label (e.g. "Retail", "Healthcare"). |
| `d:exampleText` | ExampleCase | One-sentence "what this example shows". |
| `d:caseCode` + `d:caseCodeLang` | ExampleCase | The code snippet + its language (turtle/sparql/sql/python/cypher/json). |
| `d:caseGraph` | ExampleCase | Optional JSON node-link graph to draw for the example. |

## 3. OPTIONAL FEATURES — each renders only if present (graceful absence)
Every one of these is a JSON-valued annotation on a Concept (or Area). If absent, the pipeline skips it.
`d:modelComparison`, `d:layeredArchitecture`, `d:techCompareRich`, `d:inferenceContrast`, `d:axiomReference`,
`d:idGlossary` (on an ExampleCase), `d:primerData`, `d:provLegend`, `d:corpusData`, `d:taxonomyTree`,
`d:crossTech`, `d:industryLabel`/`d:industryLink`, `d:prefixGlossary`, `d:termGlossary`, `d:quizBank`.
(JSON schemas for each are in RDODI_feature_schemas_v1_0_0.json.)

## 4. MECHANICAL EXECUTION (automatic)
Any ExampleCase whose `d:caseCodeLang` is turtle/rdf and whose code is SKOS resolution, OWL inverseOf, or RDFS
subclass inference is EXECUTED at build time (rdodi_example_executor) and its result table is computed, not
authored. List conceptual-breakdown cases in the executor's exclusion set to keep curated results.

## 5. WHAT IS NOT IN THE ONTOLOGY (pipeline-provided, domain-agnostic)
- The rendering engine (HTML SPA: sidebar, top menu, tabs, tooltips, context menus, quiz interaction).
- The executor, gates, verifiers.
- The report renderer (docx).
These are reused unchanged across domains.

## 6. DOMAIN-SPECIFIC RENDERERS (the only code a new domain may need)
- `modelComparison` diagrams: the *content* is JSON in the ontology, but the SVG drawing for ERD/UML/tree is
  generic and reused. A domain only writes the JSON (entities, relationships); no new code.
- If a domain wants a brand-new visual type not in the feature set, it adds one renderer function + one JSON
  schema — the rest of the pipeline is untouched.

## 7. PRODUCING OUTPUTS
1. Author `d_domain_tbox_vX.ttl` per this contract.
2. `python3 gen_render_deployed.py d_domain_tbox_vX.ttl` → interactive HTML (gated by deployed-bar-gate).
3. `python3 gen_report_data.py d_domain_tbox_vX.ttl && node gen_report_docx.js` → academic docx.
4. Verify: example verifier (all code parses), executor (computed results), gate (BAR_MET), consistency
   (OWL-RL, no owl:Nothing). All are domain-agnostic.
