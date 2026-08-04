# RDODI — Public Edition v1.0.0

**RDODI** (Research → Domain → Document → Interactive page) is a governed ontology-engineering methodology: a pipeline of formally-defined stages that takes a subject from research inputs, through a domain ontology (TBox/ABox/SHACL), to generated documents and interactive HTML teaching surfaces — with every stage gated by machine-checkable verification rather than assertion.

This is the **public teaching edition**, prepared for colleagues and students. It is derived from the governed RDODI ecosystem (see `PROVENANCE.md` for the exact lineage, SHA-chained) with personal projects and internal working records removed. Everything here is runnable and self-verifying.

## What's inside

| Area | Content |
|---|---|
| `01-stage-vocabularies/` | The four stage ontologies (research, domain, document, interactive page) — each as TBox + ABox + SHACL, versioned per BP-D7 (filename = versionInfo = versionIRI) |
| `25-scp-fair-completeness/` | A complete worked domain: **Semantic Technologies** (44 classes, 4 areas, every class carrying a `skos:definition`) with rich teaching content — taxonomies, W3C stack, knowledge graphs. All example data is honestly tagged per its embedded provenance legend (ILLUSTRATIVE / PUBLIC PATTERN) |
| `13-pipeline/` | The generator: domain ontology → interactive HTML SPA (explorer tree, tooltips, context menus, keyboard navigation, quiz), plus the Definition Conformance Gate that checks generated widgets against their own `skos:definition` text |
| `02-gates/`, `12-enforcement/`, `22-validation-harness/` | The verification machinery: SHACL suites, fidelity gates, reference auditors, adversarial fixtures |
| `28-interactive-html-surface/` | Stage-6 interactive surface exemplar (cryptography domain) with its generator |
| Other numbered stages | Procedure, provenance, intent, pedagogy, academic authoring, knowledge-base staging — the full methodology skeleton |

## Try it (5 minutes)

```bash
pip install rdflib pyshacl owlrl
./selftest_v1_22_2.sh                       # parse everything + SHACL gates
cd 13-pipeline
python3 rdodi_html_generator_v1_1_0.py ../25-scp-fair-completeness/scp_domain_tbox_v4_0_0.ttl out/
# open out/scp_domain_tbox_v4_0_0_page.html — a full interactive teaching page, generated from the ontology
python3 definition_conformance_gate_v1_0_1.py out/scp_domain_tbox_v4_0_0_page.html   # 13/13 clauses
```

## Principles you'll see enforced everywhere

- **Definitions are the spec**: generated artifacts are checked against `skos:definition` text mechanically.
- **Verification is by running**: every release claim traces to a re-runnable gate (manifest self-check, SHACL, conformance gate), never to prose.
- **Version identity** (BP-D7): filename token = `owl:versionInfo` = `owl:versionIRI`, with `owl:priorVersion` chains.
- **Honest provenance**: teaching examples are explicitly tagged ILLUSTRATIVE vs PUBLIC PATTERN — invented data is never dressed as real data.

## License & attribution

CC BY 4.0 — © 2026 Yusuf Altunel, İstanbul Kültür Üniversitesi. Attribution retained per license; see `PROVENANCE.md` for what this edition changes relative to the governed ecosystem.

Integrity: `MANIFEST_SHA256_v1_0_0.txt` covers every file; verify with the snippet inside it or `./selftest_v1_22_2.sh`.
