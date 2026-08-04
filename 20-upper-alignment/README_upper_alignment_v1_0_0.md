# R5 — Upper-Ontology Alignment v1.0.0 (CITE-NOT-IMPORT)
A separate, interpretive alignment of RDODI's top information-artifact concepts to upper-ontology anchors — built cite-not-import because importing an upper ontology is the scope-bleed risk the risk plan flagged.

- **upper_ontology_alignment_v1_0_0.ttl** — skos:closeMatch mappings:
  doc:ReportGenerationArtifact, ip:Page → IAO InformationContentEntity (obo:IAO_0000030);
  gen:GenerationActivity → BFO process (obo:BFO_0000015).

## L-64 guarantees (verified)
- 0 owl:imports; 0 rdfs:subClassOf into the upper ontology; only skos match predicates — no axiom coupling, no scope-bleed.
- Mappings flagged PROPOSED / verify (alignment is interpretive; confirm anchor IRIs + correspondences before external use).
- Separate file: domain DL-consistency unchanged (still PASS) — no regression.
