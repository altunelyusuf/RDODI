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

---

# Update v1.1.0 (2026-09-17)

**Derived from:** governed `rdodi-ecosystem` v1.124.0, repo `main @ f014066`.

**Scope, deliberately partial and disclosed as such**: this update adds
three new sub-packages under `28-interactive-html-surface/` —
`08-brsf-corpus-template`, `09-project-proposal-template`,
`10-programmable-content-template` — built since the v1.0.0 base
(v1.74.0-era). It does **not** attempt a full re-sync of every directory
that has since drifted from v1.74.0; the governed tree has moved in
`01-stage-vocabularies/`, `02-gates/`, `12-enforcement/`, `14-bootstrap/`,
`01-profiles/`, `03-procedure/` and others too, none of which are
touched here. Those remain a separate, future update.

## Included

- `08-brsf-corpus-template/`: the schema contract, the instantiation
  tool (`instantiate_corpus_v1_2_0.py`, genericized — see below), two
  example corpora, and a built, verified instance
  (`rdodi_lineage_interactive_v14_0_0.html`).
- `09-project-proposal-template/`: included in full — checked and found
  to already carry zero internal-source references throughout (schema,
  tooling, source reference, and built instance alike).
- `10-programmable-content-template/`: the corpus data, both built
  instances, and the verification script.

## Excluded

- `08-brsf-corpus-template/05-source-reference/` (two raw internal
  source templates, each heavily branded with the internal company this
  package's own development used as its working example) and
  `10-programmable-content-template/05-source-reference/` (the same
  raw template) — matching this edition's own v1.0.0 precedent of
  excluding raw internal sources rather than trying to genericize them
  wholesale.
- `08-brsf-corpus-template/07-handovers-received/` and the entire
  `09-handover-response/` package — internal cross-session governance
  records naming a specific internal package throughout (as a citable
  reference implementation, by name, repeatedly) rather than reusable
  public teaching material. Matches this edition's own precedent of
  excluding internal session/handover records (see the original
  exclusion of `05-documentation/`).

## Modified

| File | Change |
|---|---|
| `08-brsf-corpus-template/02-tooling/instantiate_corpus_v1_2_0.py` | The literal find/replace table this package's own development used against its internal source template (~44 lines, all pairing internal-source-specific strings with generic ones) removed and replaced with a comment explaining the technique it demonstrated; that table is meaningless without the excluded source and its literal old-side strings are themselves exactly the internal content this edition excludes. Every other transform in the function — dark mode, sidebar filter, tree restructure, the force-directed ontology graph, and the real UI-layout fixes — is source-agnostic and shipped unchanged, verified still functional (re-run end to end, 20 of the original transforms still apply cleanly). One further, minor comment reference to the internal source's naming genericized for consistency. |
| `08-brsf-corpus-template/BUILD_INSTRUCTIONS_v1_0_0.md` | One reference to an internal identifier count genericized. |
| `08-brsf-corpus-template/01-schema/corpus_contract_v1_1_0.json` | One reference to the internal source's own namespace genericized. |
| `08-brsf-corpus-template/README_v1_0_0.md` | Not genericized line-by-line — replaced outright with a fresh, short public README, since the original is a full internal development diary referencing the internal source by name throughout (closer in kind to a session record than reusable documentation, so treated the same way this edition already treats those). |
| `10-programmable-content-template/README_v2_3_0.md` | Three verification-result mentions of internal identifiers genericized ("zero X present" style statements; no internal content was actually described, just confirmed absent). |
| `08-brsf-corpus-template/06-instance/rdodi_lineage_interactive_v14_0_0.html`, `10-programmable-content-template/06-instance/programmable_content_generation_v3_0_0.html`, `10-programmable-content-template/06-instance/vaf_operators_knowledge_base_v1_0_0.html` | A real finding made during this update's own absence-verification pass, not anticipated going in: all three embed the shared, standard `backlog-roadmap-framework` TBox verbatim as a data constant, and that TBox's own v1.0.0 header comment documents its origin as a generalisation of an internal product-backlog deposit tied to a specific named personal business. Genericized in all three (the specific business name and its internal deposit path removed from the embedded comment; the rest of the governed ontology text, including every substantive definition, left untouched). |

## Verification performed on this update (executed, not asserted)

Comprehensive case-insensitive grep across every file included in this
update for the internal source's own name/abbreviation, the personal
business name found during the pass above, and the author's employer
name: zero occurrences, content and filenames both. The genericized
tool re-run end to end against its own internal test source (this
sandbox only, not shipped) to confirm it still functions after the
excision. All three edited HTML instances re-checked for valid
JavaScript syntax after the embedded-TTL edit.

## Not yet done, and named rather than left silent

A full re-sync against governed `rdodi-ecosystem` v1.124.0 covering
every directory this edition originally derived from — the drift is
real (new ontology versions, new gates, new profiles) and has not been
reviewed for public-safety here. This update is scoped to the three new
sub-packages only, as agreed before starting.

---

# Update v1.2.0 (2026-09-17) — full re-sync against governed rdodi-ecosystem v1.124.0

**Derived from:** governed `rdodi-ecosystem` v1.124.0, repo `main`.

**Scope:** every directory this edition draws from was checked against the
current governed tree, not just the three packages v1.1.0 added. Where
governed had moved since the v1.0.0/v1.1.0 basis, new content was reviewed
for safety and included or excluded on the same footing as the original
export. Where a file's version number differed but governed had NOT
actually moved past what this edition was already built from, nothing was
touched — confirmed individually, not assumed from a differing filename.

## A real finding, corrected before anything else in this update

While re-verifying `08-brsf-corpus-template`'s own already-published
content (added in v1.1.0) against a fuller marker set than was checked at
the time, one more internal-session reference was found still present:
principle R13's text, embedded both in the raw corpus JSON and in the
built HTML instance, named a specific internal cross-session codename
("PAMG CogniTwin session") that the equivalent record in
`09-knowledgebase-stage` had already had genericized. This means the
public repo carried this reference from the moment v1.1.0 was published
until this update. Fixed in both files (the same substitution already
used elsewhere: the codename removed, "a parallel session" retained),
verified both files still parse (valid JSON; valid JavaScript inside the
HTML). A full re-scan of this file for every other embedded governed-TTL
constant it carries (`BACKLOG_ABOX_TTL`, `BACKLOG_RULES_TTL`,
`BACKLOG_SHACL_TTL`, `AGENTIC_TTL`, `BIAS_TTL`, `LINEAGE_TTL`,
`PROV_TTL`, `SKOS_TTL`) found nothing further.

## Included (new since v1.0.0/v1.1.0, reviewed and confirmed safe)

- `01-stage-vocabularies/`: new research (v1.1.0), domain (shacl v1.2.0,
  tbox v1.3.0, a RULING record, 3 fixtures), and document (abox v1.1.0)
  ontology versions.
- `01-profiles/`: versions v1.1.0 through v1.4.0, plus
  `RDODI_EXEMPLAR_STANDARD_v1_1_1.md` and
  `rdodi_exemplar_program_backlog_v1_1_0.ttl`. One internal-assessor
  reference ("PAMG assessor") genericized to "the assessing body" in
  v1.2.0-v1.4.0; noted at the top of each affected file.
- `09-knowledgebase-stage`: rebuilt as v1.6.1 (superseding the stale
  v1.4.1) — the same 4 parallel-session references the original v1.4.1
  had already genericized, re-applied to the newer v1.6.0 content;
  confirmed no new sensitive references in the R16-R21 additions it
  brings in.
- `02-gates/`: two new pipeline-validator versions, a docling-corpus
  bridge and its fixture set, three new stage3f fixtures. One script's
  comments and one fixture's namespace (referencing the excluded
  worked-example material and a chapter-numbered identifier
  respectively) genericized to match this edition's existing "ch9/ch10
  -> demo" convention.
- `03-procedure/`: versions v1.2.1 through v1.6.0. A citation of a
  specific internal package by name, carried unchanged across four
  versions, genericized in all four.
- `03-tooling/` (new directory): the disk-audit tool and release-check
  script, both clean as-is; one negative test fixture had the same
  internal-package citation pattern as several other files, genericized
  the same way.
- `14-bootstrap/`: the current bootstrap script, a new stage4-nav-gates
  script, and a full new `templates/` subdirectory, all confirmed clean.
- `21-worked-example-stg/`: one new file (`JOURNEY_stg_candidate.md`) —
  read directly rather than only keyword-scanned, since the original
  edition had excluded it; found to be a short, generic gate-status
  table with no sensitive content, included.
- `28-interactive-html-surface/README_v1_15_0.md`: the package's own
  navigation/index document, genuinely useful and general-purpose (not
  a session diary), included with its own internal-source citations and
  its now-broken cross-references to the excluded `08-brsf-corpus-
  template/README_v1_0_0.md` genericized or redirected.

## Confirmed already correct, nothing to do

A large fraction of the apparent drift turned out to be files where
governed had not moved since the original export, and the public
edition's own existing (differently-versioned) file was already the
correct, current genericization: `08-academic-authoring-stage`,
`10-knowledgebase-ext-stage`, `18-provenance`, `19-oquare-aggregation`,
`12-enforcement`'s non-excluded files, `13-pipeline`'s conformance gate,
`21-worked-example-stg`'s governance TTLs, `24-cite-not-import-
modularity` (the OEE -> external-authority pattern, all five files),
`25-scp-fair-completeness`, and `26-stage4-navigation-adoption`'s vocab
delta. Verified individually in each case (checking the file's own
`priorVersion`/basis against governed's current state, or diffing
directly), not assumed from a differing filename — one redundant copy
was caught and removed during this process before it shipped
(`document_ontology_abox_v1_1_0.ttl`, already correctly superseded by
the existing `v1_1_1.ttl`).

`06-widget-stage`, `07-pedagogy-professional-stage`,
`11-documentation-standards-stage`, `13-pipeline` (structure),
`15-presentation`, `17-stage-discipline`, `20-upper-alignment`,
`22-validation-harness`, `23-module-assembly` showed zero content
difference from governed at all.

## Still excluded, matching the v1.0.0 precedent exactly

`00-dev-env/`, `00-responses/`, `04-worked-example/`, `05-documentation/`,
`07-handover-inbox/`, `08-brsf-corpus-template/{05-source-reference,
07-handovers-received}/`, `09-handover-response/`,
`10-programmable-content-template/05-source-reference/`,
`12-enforcement/{OE_FORWARDED_PROPOSALS_NOTE, R11_PREFILTER_PROVENANCE,
rdodi_variant_admissibility_gate}`,
`13-oee-compliance/`, `24-vaf-adaptation/`,
`26-stage4-navigation-adoption/{ASSESSMENT,PROOF_VERIFICATION,
SOURCE_proposal,WIRING}` — confirmed still present and still matching
the same exclusion rationale (internal session records, raw sources
tied to unpublished internal material, or cross-session governance
records naming other internal packages throughout).

## Verification performed on this update

Comprehensive case-insensitive scan, across the entire tree, for: the
internal source's own name/abbreviation, the personal business name
found in the previous update, the author's employer name, and the
internal session codename found and fixed in this one. Confirmed clean
except four lines that are this edition's own traceability notes
describing what was fixed (naming the removed term, as this document
also does) — not the sensitive content itself. Both PAMG-bearing files
re-verified as syntactically valid after the fix.
