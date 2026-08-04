# RDODI / SCP enrichment proposal — FAIR & documentation completeness

**Artifact:** `RDODI_enrichment_proposal_v1_0_0`
**Status:** *Advisory proposal, not a release.* STG authors it; the RDODI / SCP owner adjudicates and supplies all authoritative content (B1/L-64 — this proposes a constraint and an inventory, it does not edit governed RDODI artifacts).
**Basis (verified from disk this session):** OE Operating Discipline `v2.1.2` (SHA `a2d9a1fc…`), OE KB ABox `v2.7.0` (SHA `31b09600…`), SCP TBox `scp_domain_tbox_v3_16_1.ttl` (`http://rdodi.org/scp/domain#`, 44 classes).
**Companion artifact:** `scp_fair_completeness_shacl_v1_0_0.ttl` (the proposed constraint).

---

## 1. What this proposes — and what it deliberately does *not*

It proposes to raise SCP's **FAIR metadata** and **documentation completeness** to a governed bar, via a SHACL constraint anchored wholly to FAIR (Wilkinson et al. 2016) and OntoQA documentation completeness (Tartir et al. 2005) — no bespoke metric or threshold (L-72).

It does **not** propose enriching SCP's *richness*. That candidate (roadmap candidate **D**, "enrich SCP richness") was **falsified and killed** on evidence: SCP's OntoQA Relationship Richness is RR = 0.7736, Inheritance Richness IR = 0.8182, and citation-resolvability is 27/27 = 1.0 — already adequate. Re-proposing it would be a phantom enhancement (L-71). This proposal targets only the dimensions the richness spike never examined.

## 2. Verified evidence (the gap, read from the SCP bytes)

Validating the proposed constraint against current SCP yields **28 violations** (`conforms = False`), broken down by the per-class read of the TBox:

| Gap (FAIR / OntoQA criterion) | Count | Examples |
|---|---|---|
| Classes missing `skos:definition` (R1.2 / OntoQA documentation) | **9 / 44** | `Publication`, `SemanticTechnology`, `SemanticTechnologyArea`, `ReportSection`, `OntologyTier`, `Taxonomy`, `ComparisonPage`, `Simulation`, `ExampleCase` |
| Classes missing `dcterms:source` (R1.2 provenance) | **15 / 44** | `PropertyGraph`, `RelationalModel`, `Foundations`, `LayeredOntology`, … |
| Ontology-level FAIR metadata absent (F2 / R1.1) | **4** | `dcterms:title`, `dcterms:license`, `dcterms:creator`, `dcterms:description` — none present under any predicate |
| Cited `Publication`s without a resolvable identifier (F1) | **0** | — SCP already complies (forward-guard only) |

Five of the nine undefined classes (`ComparisonPage`, `Simulation`, `Taxonomy`, `ReportSection`, `ExampleCase`) carry **no documentation at all** (no label, comment, or note). A **gap-filled SCP validates at 0 violations**, so the bar is achievable — the constraint discriminates *current-fails / completed-passes*, it is not an impossible gate.

## 3. The three enrichment items

**Item A — Ontology-level FAIR metadata (FAIR F2 + R1.1).** Add `dcterms:title`, `dcterms:license`, `dcterms:creator`, `dcterms:description` to the SCP ontology header. Highest value, lowest risk, purely additive. **The values are the owner's to supply** — STG will not fabricate a license string or a creator (L-65). The proposal provides the slots and the gate; RDODI fills them.

**Item B — Class documentation completeness (FAIR R1.2 / OntoQA).** Supply a `skos:definition` for the 9 undefined classes and a `dcterms:source` for the 15 unsourced classes. Draft starting points for the unambiguous *structural* classes are in the appendix (clearly non-authoritative); the **domain-core** classes (`SemanticTechnology`, `SemanticTechnologyArea`, `OntologyTier`, `Taxonomy`) should be authored or ratified by the owner, not drafted by STG, to avoid scope-bleed (L-64).

**Item C — Citation-resolvability lock-in (FAIR F1/R1.2).** Promote the STG PA-6 shape (`scp:Publication` must carry a resolvable http(s) identifier) from "STG happens to validate SCP" to a **governed RDODI constraint**. SCP already passes (0 violations), so this is a *forward-guard* preventing future regressions, not a fix.

## 4. The proposed constraint (companion SHACL)

`scp_fair_completeness_shacl_v1_0_0.ttl` carries three `sh:NodeShape`s — class documentation (SPARQL-targeted to `scp:`-namespace classes), ontology metadata (targets `owl:Ontology`), and publication resolvability (the PA-6 promotion). Each `sh:message` cites its FAIR/OntoQA criterion. The shape IRIs are **STG-namespace** (`http://stg.org/proposal/scp-fair#`) and *target* `scp:` classes by reference — no `rdodi.org` IRI is minted and nothing is asserted into SCP (B1/L-64). On adoption, RDODI may re-home the shapes under its own namespace; that is the owner's decision.

## 5. Acceptance / Definition of Done

1. The four ontology-metadata slots are populated with owner-supplied values.
2. All 44 SCP classes carry a `skos:definition` and a `dcterms:source`.
3. SCP validates against `scp_fair_completeness_shacl_v1_0_0.ttl` at **0 violations** (the gate that is currently 28 now passes).
4. The constraint is adopted into RDODI governance so the bar is held going forward (regression-guard).

## 6. Discipline boundaries honoured

- **B1 / L-64:** advisory proposal, not an edit to governed RDODI artifacts; STG-namespace shapes referencing (not minting) `scp:` IRIs; no STG vocabulary bled into SCP.
- **B3 / L-65:** every count in §2 is read from the SCP bytes and re-validated by the companion SHACL before being stated; no license, creator, or definition is fabricated and presented as RDODI's.
- **L-71:** only the verified gaps are proposed; the (killed) richness candidate is excluded.
- **L-72:** completeness criteria anchor to FAIR F1/F2/R1.1/R1.2 and OntoQA documentation — no invented metric or threshold.

---

## Appendix — DRAFT definitions for structural classes (non-authoritative; for owner ratification)

> These are proposed starting points only. They are **not** RDODI's authoritative definitions and must be reviewed, edited, or replaced by the owner before adoption (L-64/L-65).

- **`Publication`** — *draft:* a cited bibliographic resource (paper, specification, or report) referenced by the ontology as a source.
- **`ReportSection`** — *draft:* a structural division of a generated RDODI report deliverable.
- **`ComparisonPage`** — *draft:* a generated page that contrasts two or more semantic-technology options on stated dimensions.
- **`ExampleCase`** — *draft:* a worked illustrative instance demonstrating a concept in use.
- **`Simulation`** — *draft:* an interactive or executable artifact that models a concept's behaviour for the reader.

Domain-core classes (`SemanticTechnology`, `SemanticTechnologyArea`, `OntologyTier`, `Taxonomy`) are intentionally left for owner authoring.
