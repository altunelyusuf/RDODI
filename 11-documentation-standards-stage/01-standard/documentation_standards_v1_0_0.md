# RDODI Documentation Standards — Seminal & Readable (v1.0.0)

Extends Stage AA. Defines the **craft and apparatus** standards for RDODI-produced documents
(reports, courseware, interactive-page prose) and the **actions** and **gates** that enforce them.

## The honesty boundary (L-40 — read first)
A gate's verb is not uniform. Each standard below is tagged with what its gate can actually do:
- **GUARANTEE (Tier A)** — mechanically checkable; the gate's PASS is a real guarantee of conformance.
- **FLAG (Tier B)** — proxy heuristic; PASS means "no egregious failure detected", NOT conformance.
- **REQUIRE (Tier C)** — not auto-certifiable; the gate forces a hash-bound human attestation and
  cannot itself pass the item. Calling a Tier-C item "guaranteed" by a gate is selling fake rigor.

"Guarantee documentation quality" is therefore precise only for Tier-A. The standard guarantees the
apparatus floor, flags the register, and routes judgment to an accountable attestor.

---

## A. APPARATUS (Tier A — GUARANTEED by gate)

| ID | Standard | Action (how to satisfy) | Gate |
|----|----------|------------------------|------|
| DOC-A1 | **First-use abbreviation expansion** | On first occurrence write `Full Term (ABBR)`; use `ABBR` thereafter; abstract expands independently | `gate_abbrev_firstuse` — every detected acronym's first prose occurrence carries an expansion |
| DOC-A2 | **Abbreviations list mirrors usage** | Maintain a List of Abbreviations = exactly the set used | `gate_abbrev_list` — listed == used (no unused, no unlisted) |
| DOC-A3 | **In-text citations present & styled** | Every non-trivial claim carries an in-text citation in ONE consistent style | `gate_intext_citations` — claims/sections carry citations; single style detected |
| DOC-A4 | **Citation–reference reconciliation** | Every in-text cite appears in References; every reference is cited | `gate_cite_ref_reconcile` — zero orphans either direction |
| DOC-A5 | **Reference list present & complete** | A `References` section with complete, consistently-formatted entries | `gate_reference_list` — section exists; entries well-formed |
| DOC-A6 | **Quotation page anchors** | Direct quotes carry page numbers; paraphrase is reworded | `gate_quote_anchor` — quoted spans have page anchors |
| DOC-A7 | **Figure/table numbering + reference** | Number all figures/tables; reference each in prose; caption each | `gate_figure_ref` — every figure/table defined is referenced |
| DOC-A8 | **Section structure** | Required section types present (Abstract; Intro w/ scope; body; synthesizing Conclusion; Limitations) | `gate_section_structure` — required headings present |
| DOC-A9 | **Heading hierarchy well-formed** | Numbered, parallel, no skipped levels | `gate_heading_hierarchy` — no level skips; consistent |

## B. READABILITY & REGISTER (Tier B — FLAGGED by gate, proxy only)

| ID | Standard | Action | Gate (proxy) |
|----|----------|--------|--------------|
| DOC-B1 | **Readability in target band** | Write to the audience; keep FK grade in declared band | `gate_readability` — FK grade within band (proxy for comprehension, NOT a measure of it) |
| DOC-B2 | **Academic register** | Measured tone; hedge claims to evidence; limited first person | `gate_register` — hedging density ≥ floor, first-person ≤ ceiling (proxy only) |
| DOC-B3 | **Sentence completeness** | Complete grammatical sentences | `gate_sentence` — fragment heuristic flags egregious cases |

## C. COHERENCE & WARRANT (Tier C — REQUIRE attestation, NOT guaranteed)

| ID | Standard | Action | Gate (attestation) |
|----|----------|--------|--------------------|
| DOC-C1 | **Paragraph cohesion** | Topic sentence + given-new flow + transitions | `attest_cohesion` — proxy counts reported; human confirms true coherence |
| DOC-C2 | **Terminology consistency** | Same concept → same term throughout | `attest_terminology` — synonym-switch candidates flagged; human confirms |
| DOC-C3 | **Claim calibration** | Certainty matches evidence | `attest_calibration` — human-only |
| DOC-C4 | **Citation warrant** | Cited source actually supports the claim | `attest_warrant` — human-only (the Stage-AA / Stage-P content-correctness sign-off) |
| DOC-C5 | **Logical soundness & contribution** | Valid argument; stated contribution | `attest_soundness` — human-only |

---

## Integrity (always-on, Tier A floor)
DOC-INT: no fabrication, no plagiarism; paraphrase genuinely reworded; disclosure statements present
(funding/COI/data-availability where applicable). `gate_integrity_apparatus` checks presence of the
disclosure apparatus; it cannot detect fabrication (Tier C).

## Profiles (rising bar, inherits Stage AA profiles)
- **ReadableDraft** — Tier A apparatus + Tier B proxies. The floor.
- **CoursewareDoc** — adds DOC-A8/A9 structure + DOC-C1/C2 attestations.
- **SeminalDoc** — adds DOC-A3/A4/A5/A6 full citation apparatus + DOC-C3/C4/C5 attestations +
  ConsultedOnly source binding. **Only certifies with genuinely consulted, tamper-bound primary sources.**

## What this standard will NOT do (L-40)
- It will not make a document scholarly by passing Tier-A. Apparatus is the floor, not the building.
- It will not certify warrant, coherence, or contribution — those REQUIRE the attestation and are
  never auto-passed.
- "Guarantee" in this standard means Tier-A conformance only.
