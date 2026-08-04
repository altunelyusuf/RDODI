# KB-EXT Stage Proof Report v1.1.1

## Scope of this release (v1.0.1 -> v1.1.0 -> v1.1.1)
- v1.1.0 (MINOR, additive): added the `kbx:CatalogueAuthorityTier` class with four ordered tiers
  (Tier_Definitive rank=1 > Tier_High=2 > Tier_Moderate=3 > Tier_Low=4), the `hasAuthorityTier`,
  `tierRank`, and `resolvedAtTier` properties, assigned all 42 pre-existing catalogues to a tier
  (derived from each catalogue's own `catalogueAuthorityNote` keyword, not invented), and registered
  6 commercial/crowd sources (Amazon, AbeBooks, Biblio, Goodreads, Internet Archive, generic
  publisher page) at Tier_Low.
- v1.1.1 (PATCH): completed the SHACL-required catalogue properties (catalogueAccessModel,
  catalogueOperator, catalogueScope, applicabilityNote, appliesToStage, knowledgeKind,
  consultationStatus, definition, dcterms:source) on the 6 new commercial catalogues, which v1.1.0
  had omitted. This was caught by running the existing v1.0.1 SHACL (18 violations = 6 catalogues x
  3 missing core props + others); fixed by completing the data, NOT by weakening the shape (L-66).

## SHACL verdict (pySHACL, rdfs inference)
- TBox v1.1.0 + ABox v1.1.1 against rdodi_knowledgebase_ext_shacl_v1_0_1.ttl: **conforms = True**.

## SPARQL checks
- Every BibliographicCatalogue has exactly one authority tier: 0 untiered (48 catalogues total).
- Tier distribution: 13 Definitive / 22 High / 6 Moderate / 7 Low; clean total order rank 1..4.

## Purpose
The tier layer makes "CatalogueVerified" carry the authority of the catalogue that produced it,
so a Low-tier commercial sales listing can never be presented as an authoritative verdict. It is
the ranking that RDODI Pattern R11 (tier-maximizing resolution, KB stage) maximizes against.
