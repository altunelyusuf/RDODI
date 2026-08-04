# Assessment & adoption — STG enrichment proposal (RDODI_enrichment_proposal_v1_0_0)
**Proposal SHA-256:** `9a4f02101696f3d1958d6c69295504829021029eba1c6b211b2941b98cb420ad` (verified this session).

## Objective verdict: useful, accurate, adoptable — improved with R-E1
Every proposal claim was VERIFIED by running (not taken on its say-so, BP-D2/L-65):
- L-64 clean: shapes mint 0 rdodi.org IRIs; STG-namespace, targeting scp: by reference. ✓
- 28 violations exactly (title/license/creator/description 1 each, definition 9, source 15). ✓
- 9 undefined + 15 unsourced classes confirmed; 27 scp:Publication instances (shape 3 is a real forward-guard). ✓
- "gap-filled -> 0" achievability confirmed. The proposal is honest and well-grounded.

## Improvement applied (our own R-E1)
The proposal required a literature `dcterms:source` on ALL 44 classes. Several are STRUCTURAL (ComparisonPage,
ExampleCase, Publication, ReportSection, Simulation) or domain-SPINE (OntologyTier, SemanticTechnology,
SemanticTechnologyArea, Taxonomy) — not domain concepts. Forcing them to literature-sourcing is the exact
miscalibration R-E1 fixed. The adopted constraint (`rdodi_scp_fair_completeness_shacl_v2_0_0.ttl`) makes provenance
**source-type-aware**: literature `dcterms:source` (domain-concept) OR authority `dcterms:conformsTo`
(structural/normative). Anti-loophole invariant preserved: no class passes with zero provenance.

## Applied factually (L-65, no fabrication): 28 -> 6
- ontology FAIR metadata (4): title/license/creator/description — declared, same basis as R-E2/R-E4. CLOSED.
- 9 definitions (5 structural + 4 spine) + 9 authority cites. CLOSED.
- SCP enriched to v3.17.0.

## Honest residual (6) — NOT fabricated
Foundations, KnowledgeGraphs, LayeredOntology, PropertyGraph, RelationalModel, W3CStack are genuine domain concepts
whose provenance is LITERATURE. They were NOT authority-cited to game the gate (that is the loophole R-E1 forbids)
and NO citations were invented. They remain as the sourcing-bottleneck residual — genuine literature citations are
owner/human work. This is the same irreducible limitation the post-mortem named: sourcing is located, not removed.

## Credit
The STG proposal was sound, evidence-led, and discipline-aware (it killed its own richness candidate on evidence,
deferred authoritative content to the owner, and stayed L-64-clean). Adopted with one engine-consistency improvement.
