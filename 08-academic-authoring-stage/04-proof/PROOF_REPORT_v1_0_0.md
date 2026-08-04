# Proof Report — AA-Stage Gates v1.0.0  (re-run, L-65)

All runs below were executed against real artifacts.

## 1. Bites on the shipped Ch.9 v1.4.0 (which has narrative but no AA graph)
**@ CompanionAuthoring → REFUSED**, naming the gaps:
- AA.structure FAIL — 32 domain classes lack `aa:ExtendedTreatment` (named: QualityPlanning, ProcessMetric, ProjectQualityManagement, ScientificManagement, QualityAssurance, Quality, …).
- AA.claim_evidence FAIL — no `aa:Claim` individuals declared (genre requires explicit claims with citations).
- AA.readability — CANNOT_RUN (no treatments to score).

## 2. Satisfiable end-to-end (fixture passes)
Two-class fixture (DemoArea + DemoConcept), full ExtendedTreatments, 6 claims each `supportedBy` a real `rres:Citation`, FK 15.1 in the [12,18] band, hedging ≥ 2/1000, first-person ≤ 1/1000, two distinct citations per treatment. **@ CoursewareAuthoring → CERTIFIED.**

## 3. Discriminating (catches a real fault when only one distinct citation supports a treatment)
Initial fixture used the same citation twice for DemoConcept → AA.citation_density correctly FAILed naming the treatment under the threshold. After adding a second distinct citation, gate flipped to PASS. The gate distinguishes structural presence from substantive citation diversity.

## 4. Adversarial: ConsultedOnly cannot be gamed
On the same fixture where one claim (`cl_da_3`) is `supportedBy` an `aa:ReconstructedSource`:
- **@ ConsultedOnly → REFUSED** — AA.consultation_link names the exact culprit: `cl_da_3 → cite_demo_reconstructed (reconstructed)`.

## 5. End-to-end source consultation (ingestor)
- Ingested a Boehm-1981-style excerpt (plain text fixture) via `ingest_source_v1_0_1.py`.
- The ingestor emitted `demo:cite_boehm1981 a aa:ConsultedSource` with `aa:sourceHash` (SHA-256 `8f42075aecbe4e2d…`, tamper-bound), `aa:ingestedAt`, and one `aa:ConsultedPassage` with `aa:pageAnchor` and `aa:verbatimText`.
- After merging the consulted overlay AND retracting the `aa:ReconstructedSource` type from the previously-reconstructed citation, **@ ConsultedOnly → CERTIFIED**. The gate honestly required *retraction* of the reconstruction claim, not just addition of a Consulted type — which mirrors the operational meaning of "actually consulted."

## Honest limits the gates do NOT close
- Whether a `Claim`'s text is actually supported by the `verbatimText` of its `ConsultedPassage` is a TIER-C judgment and remains the Stage P `content-correctness` attestation.
- Readability and register are honest proxies, not measures of scholarship.
- The stage raises the structural floor on academic-genre artifacts; it does not author scholarship.
