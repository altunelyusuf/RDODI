# Phase 5 — Research Pass for Missing/Ungrounded Concepts

**Governance:** BP-D41 (verify against authoritative sources or flag), BP-D21 (placement test), L-72 (reuse-before-invent), L-40 (label status plainly).
**Status key:** VERIFIED (authoritative source confirmed) | PENDING (not yet fetched) | UNGROUNDED (no source found, flagged) | REUSE (existing vocabulary covers it — do not invent).

## Targets and findings

### 1. RST (discourse-feature anchor for rhetorical features) — VERIFIED
Rhetorical Structure Theory (Mann, W.C. & Thompson, S.A., 1987/1988). Confirmed relation inventory:
Elaboration, Contrast, Cause, Evidence, Background, Condition, Sequence, List, Joint (multinuclear).
Nucleus/satellite span model. Sources: sfu.ca/rst (Mann's own site), multiple peer-reviewed reviews.
**Disposition:** anchors ds:RhetoricalStructureFeature. Used for Contrast (P2) and Sequence (P9) features.

### 2. Shneiderman Task-by-Data-Type Taxonomy (data-pattern anchor) — VERIFIED
Shneiderman, B. (1996) "The Eyes Have It", IEEE VL, DOI:10.1109/VL.1996.545307. Fetched cs.umd.edu PDF.
7 data types (1D/2D/3D/temporal/multidimensional/tree/network) x 7 tasks (overview/zoom/filter/
details-on-demand/relate/history/extract). Concrete when-to-use rule confirmed: "buttons for small
sets of categories (cardinality < 10)"; "dynamic queries with sliders for filtering."
**Disposition:** anchors ds:DataPatternFeature. Directly grounds the K-category (P3), filter (P7),
overview-detail (P6), relate (P8) features.

### 3. Primitive 9 weak anchor (Segel & Heer 2010) — VERIFIED (upgraded from skill's PENDING)
The skill honestly disclosed it had NOT fetched Segel & Heer 2010. Now fetched and confirmed:
"Narrative Visualization: Telling Stories with Data", IEEE TVCG 16(6):1139-1148, DOI:10.1109/TVCG.2010.179
(Stanford vis lab authoritative PDF). Core framework: balance between author-imposed narrative flow
and reader-driven story discovery; 7 genres (magazine/annotated-chart/partitioned-poster/flow-chart/
comic-strip/slide-show/video). **Disposition:** the guided-narrative primitive (P9) "authored path vs
free exploration" claim is now directly grounded. The skill's flagged weakness is RESOLVED.

### 4. Research-ontology Tool/Library/Implementation/Pattern gap — REUSE (do not invent)
The skill flagged that the research ontology (v6.9.2) lacks classes for Tool/Library/Implementation/
Pattern. Research finding (L-72): schema.org ALREADY provides this vocabulary —
schema:SoftwareApplication, schema:WebApplication, schema:SoftwareSourceCode (subclasses of
CreativeWork); SoftwareSourceCode explicitly covers "code snippet samples, scripts, templates."
A w3id.org/software-types extension exists for finer types. **Disposition: REUSE schema.org when this
gap needs filling. Do NOT invent Tool/Library/Pattern classes (would violate L-72).** Flag for the
research ontology's future work, not for this widget layer.

### 5. The skill's disclosed FUTURE primitives (spatial-zoning, network-criticality,
   state-machine-illegal-transitions, decision-tree-EMV-rollback) — PENDING (correctly deferred)
The skill names these as future primitives from chapters 8-12 / other courses. Per the GENERIC-build
constraint, the catalogue should grow as real frameworks warrant — but per honest-grounding, none has
been extracted from a verified source YET. Two anchor candidates surface from this session's research:
Shneiderman's tree + network data types could anchor network-criticality and spatial-zoning. But until
a primitive is actually authored with its demonstrates/constraint/test triple from a real source, these
remain PENDING. **Disposition: do NOT instantiate as primitives now (would be ungrounded). Recorded as
the catalogue's grounded growth path.**

### 6. DiscourseFeature taxonomy completeness — HONEST GAP (L-40)
The 9 features map 1:1 to the 9 primitives. This is a CONVENIENCE not a proof of completeness: the
taxonomy currently covers exactly the discourse patterns the 9 primitives need, no more. A real chapter
may exhibit a discourse pattern with NO matching primitive (the skill's "novel widget" case). The
selector correctly returns nothing in that case (test-driven: negative cases pass). **Disposition:
the taxonomy is grounded but NOT claimed complete; gaps surface as real content is processed.**

## Summary
| Target | Status |
|---|---|
| RST anchor | VERIFIED |
| Shneiderman anchor | VERIFIED |
| Primitive 9 (Segel & Heer) | VERIFIED (upgraded) |
| Tool/Library/Pattern gap | REUSE schema.org (do not invent) |
| Future primitives (4) | PENDING (correctly deferred, not instantiated) |
| DiscourseFeature completeness | HONEST GAP (grounded, not claimed complete) |

No concept was fabricated. Every instantiated feature traces to RST or Shneiderman. Every deferred
concept is flagged PENDING/REUSE rather than invented.
