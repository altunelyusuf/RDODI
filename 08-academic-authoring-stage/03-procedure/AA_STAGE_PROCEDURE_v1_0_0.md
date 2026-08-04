# RDODI Stage AA — Academic Authoring (procedure v1.0.0)

**Ecosystem:** lifts RDODI from v1.6.0 to **v1.7.0** (additive; v1.6.0 untouched — BP-D6/D7).
**Runs after** Stage 4 (interactive page) and alongside Stage P (Pedagogy & Professional v1.6.0).
**Governing discipline:** OE Operating Discipline v2.0.0.
**Anchoring (L-72):** quality vocabulary anchors in ISO/IEC 25010 + OQuaRE; readability scoring is an
**honest proxy**, not a measure of scholarship.

## The honest principle (restated, because this stage is the most tempting to over-claim)
A gate can enforce that an academic-genre claim is **structurally present, citation-linked,
mechanically scored, and (for ConsultedOnly) verifiably backed by an ingested primary source.**
It cannot certify the prose is good scholarship; that remains the `content-correctness`
attestation under Stage P. Any pipeline that says otherwise is selling fake rigor.

## Three honesty tiers
- **TIER-A (mechanical):** graph-structural and runnable checks (presence of paragraph types,
  citation linkage, source-typing, FK score in band).
- **TIER-B (proxy):** academic-register heuristics (hedging density, first-person density). Catches
  egregious failures; cannot judge scholarship.
- **TIER-C (accountable attestation):** scholarship correctness, novelty, soundness — handed to the
  Stage P `content-correctness` attestation. Not auto-certifiable.

## Gates

| Gate | Requirement | Tier | Does NOT certify |
|------|-------------|------|------------------|
| AA.structure | every domain class has `aa:ExtendedTreatment` with the required paragraph types (area: Abstract+Background+Discussion+Implications; concept: Background+Discussion) | A | that the paragraphs are good |
| AA.claim_evidence | every `aa:Claim` has `aa:supportedBy` linking to a real `rres:Citation` | A | that the citation actually supports the claim |
| AA.citation_density | every treatment carries ≥ N distinct citations (default 2; configurable per profile) | A | citation quality |
| AA.readability | Flesch-Kincaid grade per treatment within declared `aa:targetBandLow`–`aa:targetBandHigh` band | A (proxy) | comprehension |
| AA.register | hedging density ≥ floor and first-person density ≤ ceiling per 1000 words | B (proxy) | scholarly register beyond two heuristics |
| AA.consultation_link | when profile is `ConsultedOnly`, no `aa:Claim` may be `aa:supportedBy` an `aa:ReconstructedSource` | A | that consulted passages actually support the cited claim |

## Profiles
- **CompanionAuthoring** — single-source companion. Mandates AA.structure, AA.claim_evidence, AA.readability. Permits Reconstructed citations.
- **CoursewareAuthoring** — standalone teaching. Adds AA.citation_density and AA.register.
- **ConsultedOnly** — research-grade. Adds AA.consultation_link, refusing any claim supported by a Reconstructed source. **This profile only certifies when the user has supplied actual primary documents via the consultation ingestor.**

## Source consultation layer
The Stage AA `06-consultation/ingest_source_v1_0_1.py` ingests a PDF or plain-text source the user
supplies, extracts citable passages with page anchors, computes the source SHA-256 (tamper binding),
and emits an `aa:ConsultedSource` ABox declaring the citation a `ConsultedSource` and attaching one
or more `aa:ConsultedPassage` individuals carrying `aa:verbatimText` + `aa:pageAnchor`.

**The operational meaning** of "the author actually consulted the source" is that the prior
`aa:ReconstructedSource` type for that citation is **retracted** when the consulted overlay is
merged. The AA.consultation_link gate reads both types and refuses any citation that retains the
Reconstructed type — so the only honest way to flip the gate from REFUSED to CERTIFIED is to
genuinely retract the reconstruction claim, which requires actually consulting the source.

## Honest limits (L-40) — what this stage will NOT do
- **It will not author scholarship.** It enforces the structural floor on what reaches an
  attestor's desk; the actual writing is a human task or an authoring task by a model held to the
  same honesty discipline.
- **It will not verify claim-passage match.** That an `aa:Claim` is `aa:supportedBy` an
  `aa:ConsultedSource` with attached `aa:verbatimText` does not mechanically prove the passage
  supports the claim. That match remains a TIER-C judgement and is the explicit subject of the
  Stage P `content-correctness` attestation.
- **It will not gate scholarship by readability or register.** Both are honest proxies for catching
  failures, never measurements of scholarship.
- **It will not bypass Stage P.** All gate verdicts compose with Stage P's hash-bound attestation
  requirement; CoursewareAuthoring/ConsultedOnly do not eliminate the need for `content-correctness`
  sign-off, they raise the structural floor that sign-off rests on.

## Effectiveness as outcome data
Whether a treatment actually teaches better or supports practice better is empirical and belongs
in the post-ship Stage 5 feedback loop (Stage P procedure), never in a pre-ship AA gate.
