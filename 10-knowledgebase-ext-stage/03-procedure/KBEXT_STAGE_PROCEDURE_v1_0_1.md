# RDODI Stage KB-EXT — Knowledgebase External-Knowledge Extension (procedure v1.0.1)

**Ecosystem:** lifts RDODI from v1.10.0 to **v1.11.0** (the v1.10.0 ecosystem carried KB-EXT at module v1.0.1 with the prior v1.0.0 module files retained alongside as drift from OE convention; v1.11.0 consolidates KB-EXT into single-version-per-artifact discipline).
**Module:** KB-EXT **v1.0.1** (consolidated; supersedes v1.0.0 in-place; v1.0.0 surface preserved verbatim inside each v1.0.1 artifact, prior version recorded via `owl:priorVersion`).
**Governing discipline:** OE Operating Discipline v2.0.0.
**Anchoring (L-72):** consultation-tier ladder extends Stage AA's source-consultation discipline; ISO/IEC 25010 + OQuaRE anchor preserved from KB v1.0.0.

## OE convention restated (and where v1.10.0 drifted)

A module's stage directory holds **exactly one version of each artifact at any time** — the current one. Module version history lives in (a) the `owl:priorVersion` chain in the TBox, (b) the ecosystem zip archive of each prior release, and (c) the changelog inside this procedure. It does **not** live in a parallel set of versioned files inside the same directory. The v1.10.0 ecosystem incorrectly carried both v1.0.0 and v1.0.1 module files side-by-side in the KB-EXT stage directory; v1.11.0 corrects this by removing the v1.0.0 files (their content is preserved verbatim inside the v1.0.1 artifacts) and consolidating the two-part ABox into a single v1.0.1 ABox.

## What this stage is

A graph-structured catalogue of external standards, methodologies, tools, best practices, and empirical studies relevant to the four-stage RDODI pipeline, plus a catalogue-resolution layer enabling ratifiers to verify item existence and metadata against authoritative bibliographic catalogues.

The full v1.0.1 stage contains:
- **68 external knowledge items** (the original KB-EXT v1.0.0 catalogue: 24 Standards, 17 Tools, 13 BestPractices, 10 Methodologies, 4 EmpiricalStudies) covering Stage 1 Research, Stage 2 Domain Ontology, Stage 3 Document, Stage 4 Interactive Page, and Cross-stage Governance.
- **42 BibliographicCatalogue individuals** registered for catalogue resolution (Crossref, DOI.org, OpenAlex, Semantic Scholar, Google Scholar with explicit LOW-authority caveat, Wikidata, ACM DL, IEEE Xplore, DBLP, ACL Anthology, arXiv, MathSciNet, INSPEC, PubMed, bioRxiv, six commercial publishers, formal standards bodies, code/artefact archives, books-and-theses indexes, Turkish national infrastructure, ORCID, USPTO, EPO Espacenet).
- **27 CatalogueRecord resolution records** for items whose canonical identifier is uncontroversially known.
- **Five gates**: KBX.shacl, KBX.consultation_audit, KBX.stage_coverage, KBX.cross_stage_balance, KBX.catalogue_resolution_audit.

## Consultation-tier ladder

`RequiresConsultation` → `Reconstructed` → `CatalogueVerified` → `Consulted`.

`CatalogueVerified` is **strictly weaker** than `Consulted`: a catalogue hit confirms metadata correctness (title, author, year, identifier) at a recorded time, but not content correctness. Promotion to `Consulted` requires Stage AA primary-source consultation via `08-academic-authoring-stage/06-consultation/ingest_source_v1_0_1.py`.

The ladder is structurally enforced. A SHACL SPARQL constraint refuses any item asserting `kbx:CatalogueVerified` without a corresponding `kbx:catalogueResolution`. Status promotion is additive (a new tier is added; prior tiers remain) so the provenance ladder is always visible to a ratifier; explicit retraction of a prior tier is the ratifier's call when a deeper consultation supersedes a weaker one.

## Gates

| Gate | Requirement | Tier |
|---|---|---|
| KBX.shacl | merged TBox+ABox conforms to `rdodi_knowledgebase_ext_shacl_v1_0_1.ttl` under `inference=rdfs, advanced=True`; 0 Violations | A |
| KBX.consultation_audit | every item carries `kbx:consultationStatus`; reports per-stage strongest-tier breakdown as honest disclosure | A |
| KBX.stage_coverage | every stage has ≥5 items of ≥2 knowledge-kinds | A |
| KBX.cross_stage_balance | no stage holds more than 45% of all stage-applications | A |
| KBX.catalogue_resolution_audit | no dangling CatalogueRecord targets; no CatalogueVerified item without resolution; reports per-stage CatalogueVerified count | A |

## Honest residuals (L-40)

- **The catalogue layer does not promote to Consulted.** Content correctness remains a TIER-C judgment routed to Stage AA primary-source consultation followed by Stage P content-correctness attestation.
- **No live API calls from any gate.** Network resolution introduces non-determinism and risks silently treating partial matches as confirmation. The `06-resolution/resolve_from_csv_v1_0_0.py` helper is offline-deterministic — a ratifier performs network lookups manually (or with their own scripts), records the result in CSV, then runs the helper to produce TTL.
- **The strongest-tier audit counts the strongest tier each item carries**, which means items promoted to `CatalogueVerified` while retaining their original `Reconstructed` tag are counted under `CatalogueVerified` in the audit summary; the full multi-tier status is visible in the graph and in the SHACL-validated ABox.
- **Catalogue authority is itself honestly disclosed.** Each `kbx:BibliographicCatalogue` carries a `kbx:catalogueAuthorityNote`. Google Scholar carries an explicit LOW-authority warning. Deposit-based servers (arXiv, bioRxiv, Zenodo) carry deposit-vs-peer-review caveats. Hosting platforms (DergiPark) are distinguished from editorial bodies (TR Dizin).

## Module changelog

| Module version | Ecosystem version | Change |
|---|---|---|
| v1.0.0 | v1.9.0 | Initial release. 68 items, 4 gates. |
| v1.0.1 (introduced as PATCH alongside v1.0.0) | v1.10.0 | Added catalogue-resolution layer: BibliographicCatalogue class, CatalogueRecord class, CatalogueVerified tier, 42 catalogues, 27 resolution records, fifth gate KBX.catalogue_resolution_audit. **Convention drift: both v1.0.0 and v1.0.1 module files shipped side-by-side.** |
| v1.0.1 (consolidated) | **v1.11.0 (this release)** | **Consolidation:** v1.0.0 module files removed (their content is preserved verbatim inside v1.0.1 artifacts); two-part ABox merged into single v1.0.1 ABox; procedure consolidated into single document; one file per artifact across the stage. No semantic content change versus v1.10.0; conformance to OE single-version-per-artifact discipline restored. |

## How to extend in future PATCH releases

1. Edit the v1.0.1 artifact in-place (TBox, ABox, SHACL, gates, procedure, proof report).
2. PATCH-bump the module to v1.0.2 by renaming each affected file to `_v1_0_2`. Remove the v1.0.1 files in the same commit — one version per artifact.
3. Update the `owl:versionInfo`, `owl:versionIRI`, and `owl:priorVersion` triples inside each TBox/ABox/SHACL to reflect the new chain.
4. Add a row to the Module Changelog table in this procedure.
5. Bump the ecosystem to its next MINOR release (additive PATCH inside a module is still an ecosystem MINOR bump because the user-observable file surface changes).
6. Re-run all gates; verdicts from gate output; record in proof report.
