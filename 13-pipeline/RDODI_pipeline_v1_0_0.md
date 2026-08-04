# RDODI Domain-Ontology Pipeline — v1.0.0
# A reusable pipeline that turns a domain ontology into BOTH an interactive HTML page and an
# academic report, for ANY domain. Proven on two unrelated domains (semantic technologies; cryptography).

## Components (all domain-agnostic, in 13-pipeline/)
| File | Role |
|------|------|
| rdodi_html_generator_v1_1_0.py | Reads a domain ontology → interactive HTML SPA (sidebar, top menu, tabs, tooltips, context menus, examples with computed results, quiz, catalog). Namespace + area-marker auto-detected; page title/labels from ontology metadata. |
| rdodi_report_data_v1_0_0.py | Extracts the full report-data tree from any domain ontology, computing example results via the executor. |
| rdodi_report_docx_v1_0_0.js | Renders that data into a complete academic .docx (title, TOC, sections, examples, computed tables, formal-axioms summary, references). |
| rdodi_executor_lib_v1_0_0.py | Mechanical execution of RDF/SKOS/OWL/RDFS examples — works on any domain's RDF. |
| RDODI_domain_ontology_contract_v1_0_0.md | The vocabulary a domain ontology must provide. |
| RDODI_feature_schemas_v1_0_0.json | JSON shapes for each optional feature. |
| example_second_domain_crypto_v1_0_0.ttl | A worked second domain proving generalization. |

## Usage (any domain)
```
python3 rdodi_html_generator_v1_1_0.py  my_domain.ttl  out_dir/    # → interactive HTML
python3 rdodi_report_data_v1_0_0.py     my_domain.ttl              # → /tmp/report_full.json
node    rdodi_report_docx_v1_0_0.js                                # → /tmp/scp_report.docx
```

## What was generalized this step (honest record)
Starting point: the driver READ content from the ontology generically (good) but had a few hard-coded couplings:
the page title/h1, the compare/taxonomy labels, the SCP namespace, the SemanticTechnologyArea marker, a
short_area name map, and the IO path/filename. Fixed all of these:
- IO: accepts an ontology FILE path + output dir; output filename derived from input.
- Namespace + area marker: AUTO-DETECTED from the ontology (no hard-coded namespace).
- Page title / subtitle / compare label / taxonomy label: from ontology metadata (owl:Ontology annotations),
  with the original semantic-tech strings kept as fallbacks.
- short_area: from scp:shortLabel, else truncation.
The model-comparison/diagram CONTENT is already ontology JSON; the SVG drawing is generic and reused.

## Proof of generalization
Authored a 53-triple CRYPTOGRAPHY ontology (2 areas, 5 concepts, 2 examples, 1 citation) per the contract and
ran the UNCHANGED pipeline: produced an "Applied Cryptography" HTML page (8 subpages, correct concepts, 0 console
errors) AND a validated docx report — and the executor COMPUTED the SHA-256 SKOS resolution on the new domain.
The semantic-tech domain still builds identically (322 elements; 31-concept/27-citation report) — no regression.

## Not yet generalized (honest limits / future)
- The "Traditional vs Semantic" comparison page and the primer/provenance pages still carry semantic-tech-specific
  default content; a new domain that doesn't provide its own comparisonData will show those defaults or should omit
  the tab. A fully clean multi-domain release would make those pages render only when the ontology supplies them.
- Diagrams beyond the built-in feature set require one renderer function + one schema entry (by design).
