# RDODI Four-Stage Pipeline Procedure v1.0.0

**Version:** 1.0.0 · **Date:** 2026-05-20 · **Author:** Yusuf Altunel · **License:** CC BY 4.0
**Status:** ORIGINATION (no predecessor in this lineage; supersedes the framing in `RRWPC_pipeline_canonical_reference_v1_0_0.md`)

This document defines how to execute the four-stage pipeline whose vocabularies are shipped in RDODI v1.0.1. The pipeline order is fixed; each stage consumes the prior stage's artefact; the four RDODI subjects are the vocabularies for the four stages, one-to-one.

## 1. Pipeline definition

The pipeline has exactly four stages, executed in order. Stage *n+1* requires Stage *n*'s artefact as input. The order, vocabularies, and dependencies are stated [source: user-message 2026-05-19]:

| Stage | Produces | Vocabulary subject | Required input |
|---|---|---|---|
| 1. Research | A research artefact based on the scope or raw content | `http://example.org/rdodi/research-ontology` | Scope statement OR raw source content |
| 2. Domain Ontology | A domain ontology whose taxonomy serves as Stage 3's section structure | `http://example.org/rdodi/domain-ontology` | Stage 1 research artefact |
| 3. Document | A document whose section titles are built from the Stage 2 ontology's taxonomy | `http://example.org/rdodi/document-ontology` | Stage 1 + Stage 2 |
| 4. Interactive Page | An interactive page rendering the document with experienceable affordances | `http://example.org/rdodi/interactive-page-ontology` | Stage 3 |

The four vocabulary subjects are the four `01-research-ontology/`, `02-domain-ontology/`, `03-document-ontology/`, `04-interactive-page-ontology/` directories of the RDODI v1.0.1 bundle [source: rdodi-v1_0_1/README_v1_0_1.md §3].

## 2. Stage 1 — Research

### 2.1 Inputs

One of:
- a **scope statement** — a short description of the subject under research (e.g., "Project stakeholder management and communication in IT projects, with Marchewka 2016 Chapter 8 as primary source").
- **raw content** — primary source text (e.g., a textbook chapter, regulatory document, research paper, customer brief).

### 2.2 Output artefact

A `ResearchArtefact` instance conformant to the Research Ontology TBox at `http://example.org/rdodi/research-ontology` [source: rdodi-v1_0_1/01-research-ontology/research_ontology_tbox_v1_0_1.ttl]. The artefact records the methodology, scope, citations, findings, and quality scorecard of a comprehensive scholarly review of the subject. It uses the SPAR/VIVO/FRAPO scholarly-vocabulary imports declared in the research-ontology TBox.

### 2.3 Procedure

1. Identify the primary source. If raw content is provided, that is the primary source. If only a scope statement is provided, identify and locate the canonical primary source for the subject.
2. Enumerate the primary source's named concepts: heading terms, defined terms, figure/table captions, enumerated lists. This inventory becomes the coverage denominator for the BP-D31 primary-source-concept-coverage gate at Stage 3.
3. Conduct the comprehensive research: primary source plus contemporary developments (post-publication papers, standards updates, industry references).
4. Author the research artefact as a TBox-conformant instance graph with:
   - Title, scope, abstract, methodology declaration
   - Citation list (≥40 published references; no self-references; primary-source citations distinguishable from secondary)
   - Concept inventory of the primary source (the BP-D31 denominator)
   - Findings sections covering background, contemporary developments, comparative analysis, conclusion
   - Quality scorecard (visible-to-reader machinery: topic coverage table, citation strength, methodology compliance)
5. Save as Stage 1 ABox: `<subject>_research_v<X_Y_Z>.ttl`.

### 2.4 Acceptance gates

| Gate | Check |
|---|---|
| Stage1.A | rdflib parse: 0 errors |
| Stage1.B | Conforms to `research_ontology_shacl_v1_0_1.ttl` when merged with the TBox |
| Stage1.C | Concept inventory enumerates ≥10 primary-source-named concepts |
| Stage1.D | ≥40 published references; 0 unpublished self-references |
| Stage1.E | Quality scorecard present with 4 components |

## 3. Stage 2 — Domain Ontology

### 3.1 Inputs

Stage 1 research artefact (the ResearchArtefact instance graph from §2.2).

### 3.2 Output artefact

A domain ontology — a TBox + ABox + SHACL triple — covering the subject's concepts as discovered in the research artefact's concept inventory. Conforms to the methodology framework at `http://example.org/rdodi/domain-ontology` [source: rdodi-v1_0_1/02-domain-ontology/domain_ontology_tbox_v1_0_1.ttl].

The Domain Ontology subject in RDODI is a methodology framework, not a domain itself: it defines what a properly-formed subject ontology looks like (taxonomy depth, competency questions, source provenance tagging, validation activities). Each pipeline run instantiates this methodology with a fresh subject ontology specific to its scope.

### 3.3 Procedure

1. Read the Stage 1 research artefact's concept inventory.
2. Author a subject TBox declaring those concepts as `owl:Class` hierarchies, with appropriate `rdfs:subClassOf`, `owl:disjointWith`, and property declarations. The taxonomy depth must be sufficient to serve as Stage 3's section structure: top-level classes become Stage 3 H1 sections, second-level classes become H2 sections, and so on.
3. Author a subject ABox declaring exemplar NamedIndividuals for each leaf class, with `rdfs:label`, `skos:definition`, and `dcterms:source` citing the Stage 1 research artefact.
4. Author a subject SHACL constraining the ABox to the TBox structure.
5. Each subject ontology header carries the 10 mandatory ontology-metadata predicates per BP-D24.
6. Save as three Stage 2 files: `<subject>_tbox_v<X_Y_Z>.ttl`, `<subject>_abox_v<X_Y_Z>.ttl`, `<subject>_shacl_v<X_Y_Z>.ttl`.

### 3.4 Acceptance gates

| Gate | Check |
|---|---|
| Stage2.A | rdflib parse: 0 errors across all 3 files |
| Stage2.B | HermiT consistency check on merged graph (TBox + ABox) |
| Stage2.C | pyshacl on merged graph: 0 sh:Violation severities |
| Stage2.D | Taxonomy depth ≥2 levels (top-level + at least one sublevel) |
| Stage2.E | Every leaf class has ≥1 exemplar NamedIndividual in the ABox |
| Stage2.F | Each owl:Ontology header carries 10 BP-D24 predicates |
| Stage2.G | Filename matches `^[a-z][a-z0-9_]*_v\d+_\d+_\d+\.ttl$` (BP-D6) |

## 4. Stage 3 — Document

### 4.1 Inputs

- Stage 1 research artefact (citations, findings, primary-source content)
- Stage 2 domain ontology (taxonomy that becomes the document's section structure)

### 4.2 Output artefact

A document — a long-form prose deliverable — conformant to the Document Ontology TBox at `http://example.org/rdodi/document-ontology` [source: rdodi-v1_0_1/03-document-ontology/document_ontology_tbox_v1_0_1.ttl]. The document's section structure is mechanically derived from the Stage 2 ontology's taxonomy: each top-level `owl:Class` is an H1 section; each `rdfs:subClassOf`-child is an H2; and so on.

### 4.3 Procedure

1. Walk the Stage 2 TBox's class hierarchy in document-order.
2. For each class, emit a section whose title is the class's `rdfs:label` and whose body draws on:
   - The class's `skos:definition` from the Stage 2 ABox
   - The Stage 1 research artefact's findings for that concept
   - The class's exemplar NamedIndividuals and their `dcterms:source` citations
3. Section ordering follows the TBox's `owl:Ontology` declaration order (or an explicit `rdfs:label` ordering if declared).
4. The document is structured per the Document Ontology — IMRaD-style for academic genres, structural-document for manuals/specs/white papers (the broader Document scope contemplated in RDODI's renaming from Report).
5. Each Section instance in the ABox carries `dcterms:source` citing the Stage 2 ontology class it derives from.
6. Save as Stage 3 ABox + companion DOCX/PDF render: `<subject>_document_v<X_Y_Z>.ttl` + `<subject>_document_v<X_Y_Z>.docx`.

### 4.4 Acceptance gates

| Gate | Check |
|---|---|
| Stage3.A | rdflib parse: 0 errors |
| Stage3.B | pyshacl on merged graph: 0 sh:Violation severities against `document_ontology_shacl_v1_0_1.ttl` |
| Stage3.C | Section count equals Stage 2 class count (1:1 mapping) |
| Stage3.D | Section titles equal Stage 2 class `rdfs:label` values (exact-string match) |
| Stage3.E | Primary-source-concept-coverage ≥0.80 (BP-D31): fraction of Stage 1 concept-inventory concepts present in document sections |
| Stage3.F | ≥40 published references in the document's citation list |
| Stage3.G | ≥25% of substantive paragraphs carry in-line `(Surname, Year)` citations |
| Stage3.H | Each Section ABox individual has `dcterms:source` linking to its Stage 2 class |

## 5. Stage 4 — Interactive Page

### 5.1 Inputs

Stage 3 document (ABox + DOCX/PDF) and the Stage 2 ontology (for live concept lookup in the page).

### 5.2 Output artefact

An interactive HTML page conformant to the Interactive Page Ontology TBox at `http://example.org/rdodi/interactive-page-ontology` [source: rdodi-v1_0_1/04-interactive-page-ontology/interactive_page_ontology_tbox_v1_0_1.ttl]. The page renders the Stage 3 document content with affordances that make the subject *experienceable* — interactive simulations, drag-and-drop demonstrations, ARIA-compliant navigation, in-line glossary lookups — distinct from the document's role of *describing* the subject [source: build-v7_0_0/06-stage-disciplines/rrwpc_stage4_artifact_kind_v1_1_1.ttl, RDODI-relevant content extracted].

### 5.3 Procedure

1. Render the Stage 3 document's section structure as the page's permanent visible navigation per BP-D34 (inline pill-bar for ≤25 sections; grouped pill-bar + sidebar for 26-50).
2. For each Stage 3 section, render:
   - The document's prose
   - At least one interactive element (button, simulation, drag-drop, calculator, table-walker, or canvas-based visualisation) tied to the section's concept(s) from Stage 2
3. Section content is co-located with its interactive elements (no modal dialogs; affordances appear inside the section that introduces the concept).
4. Each page-level ABox individual references its Stage 3 Section individual via `dcterms:source`.
5. Page ABox declares conformance to the InstructionalChapterCompanion structure: `rdfs:label`, mandatory section roles (Introduction, Body, Quiz, Glossary, References), and the interactive element inventory.
6. Save as: `<subject>_page_v<X_Y_Z>.html` + `<subject>_page_abox_v<X_Y_Z>.ttl`.

### 5.4 Acceptance gates

| Gate | Check |
|---|---|
| Stage4.A | rdflib parse on page ABox: 0 errors |
| Stage4.B | pyshacl on merged graph: 0 sh:Violation severities against `interactive_page_ontology_shacl_v1_0_1.ttl` |
| Stage4.C | DOM smoke (Playwright headless): page loads with 0 console errors |
| Stage4.D | ≥25 interactive buttons; ≥12 tables; ≥4 SVG figures; ≥6 simulations; 0 modal dialogs (`role='dialog'` count = 0) |
| Stage4.E | Page section count equals Stage 3 section count (1:1 mapping) |
| Stage4.F | Permanent visible top navigation (BP-D34 acceptance test: mobile viewport identifies all major sections without clicks) |
| Stage4.G | Every page ABox individual has `dcterms:source` linking to its Stage 3 Section |

## 6. Cross-stage gates

| Gate | Check |
|---|---|
| Cross.A | Stage 2 class count = Stage 3 section count = Stage 4 page section count (1:1:1 mapping through the pipeline) |
| Cross.B | Stage 4 ABox individuals' `dcterms:source` chains resolve back through Stage 3 → Stage 2 → Stage 1 (transitive provenance) |
| Cross.C | Stage 1 concept-inventory coverage at Stage 3 ≥0.80; coverage at Stage 4 ≥0.80 (BP-D31) |
| Cross.D | All 4 stages' filenames at the same `vX_Y_Z` for a coherent release (BP-D7 alignment) |
| Cross.E | All 4 stages' ABox individuals carry mixed-source provenance tagging when appropriate (BP-D33) |

## 7. What this procedure does NOT include

Honest disclosure of scope:

1. **No mechanical validator (`validate_rdodi_pipeline.py`) ships with v1.0.0 of this procedure.** The gates above are stated; a runnable validator that mechanically applies them is a future deliverable.
2. **No stage-discipline TTL artefacts in RDODI v1.0.1.** The two legacy `rrwpc_stage{2,4}_artifact_kind_*.ttl` files contain operational content (the InstructionalChapterCompanion structure template, the AcademicResearchReport structure, the reference-template inventory) that this procedure references in prose. A separate decision (Item 2 in the work sequence) addresses whether to port any of that content as RDODI-native stage-discipline TTLs.
3. **No explicit Bloom's taxonomy or pedagogy framework.** The procedure focuses on the technical pipeline. Pedagogical structure for Stage 4 interactive elements is currently determined per-deliverable by the author.
4. **No reference-template artefacts.** The legacy bundle's `Reference_Template_COM0463_Ch{1,2,4,5}_*` individuals named gold-standard exemplars at specific byte/LOC/widget counts. Whether these exemplar references carry forward into RDODI's procedure is part of Item 2's stage-discipline disposition.
5. **Stages 1 and 2 have no shipped reference-template inventory analogous to Stage 4's.** The procedure states their gates but does not point at exemplar deliverables for them. Authoring such exemplars would be a v1.1.0 enhancement.

## 8. Predecessors and superseded documents

| Document | Relationship to this one |
|---|---|
| `RRWPC_pipeline_canonical_reference_v1_0_0.md` at `/home/claude/work/standards/_standards/` | **Superseded.** That document conflated multiple scopes and pointed at the wrong pipeline (the 8-stage OE Pack Subject Pipeline). Its §1 four-scope taxonomy is retained as background; its §2-§5 are obsolete. |
| `rrwpc_stage2_artifact_kind_v1_0_0.ttl` at `build-v7_0_0/06-stage-disciplines/` | **Referenced.** Operational content cited in §4.2. Disposition (port to RDODI vs leave as legacy reference) decided in Item 2. |
| `rrwpc_stage4_artifact_kind_v1_1_1.ttl` at `build-v7_0_0/06-stage-disciplines/` | **Referenced.** Operational content cited in §5.2. Disposition decided in Item 2. |
| `build-v7_0_0/README.md` | **Referenced for vocabulary scope.** The four subject ontologies it lists are the four pipeline stage vocabularies as ported into RDODI v1.0.1. |
