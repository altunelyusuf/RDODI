# RDODI Richness Rubric & Gate — v1.0.0
# Captures the AUTHORING-DEPTH intelligence: turns "BAR_MET" from an HTML byte-size check into a
# genuine depth/rigor/richness check on the SOURCE ontology, and tells the author what to add.

## Why
The pipeline reliably renders/executes/navigates, but the DEPTH (treatment quality, example design,
comparative analysis, formal axioms, citations, quiz) was hand-authored content the engine only displays.
This rubric measures that depth and produces a prioritized gap list — so a new domain can be brought to the
hand-built bar by following the gaps, not by guesswork.

## Eight weighted dimensions (thresholds grounded in the rich SCP artifact, which scores 97.9%)
| # | Dimension | Wt | Measures |
|---|-----------|----|----------|
| D1 | Coverage | 20 | #concepts (>=12) and every concept has a >=200-char treatment |
| D2 | Treatment depth | 15 | median treatment length (target >=300 chars) |
| D3 | Worked examples | 15 | every concept has >=1 example |
| D4 | Executable examples | 10 | fraction of examples that are executable RDF/SPARQL |
| D5 | Rich features | 15 | concepts carrying modelComparison / techCompareRich / layeredArchitecture / inferenceContrast / idGlossary |
| D6 | Formal axioms | 10 | object properties + asserted relationships + disjointness (+consistency) |
| D7 | Citations | 8 | #publications (>=10) with verifiable URLs |
| D8 | Self-check quiz | 7 | >=15 questions mixing deduction + concept + spot-the-error |

Verdict RICHNESS_MET at >=75%. Output includes per-concept thin-flags and a priority-ordered fix list.

## Calibration (proven)
- Rich SCP artifact (hand-built to satisfaction): 97.9% -> RICHNESS_MET, 0 thin concepts.
- Thin crypto demo (5 concepts, shell-only): 24.4% -> BELOW_BAR, every concept flagged, 7 prioritized gaps.

## Integrated gate
rdodi_deployed_bar_gate_v1_3_0.py now requires BOTH the HTML artifact checks AND richness:
  `gate <page.html> --ontology <domain.ttl>`  -> BAR_MET only if HTML passes AND richness >=75%.

## Honest scope
This captures depth MEASUREMENT + GUIDANCE (what's missing). It does not yet AUTHOR the missing content
(that is the next capability: authoring scaffolds that draft treatments/examples/features for human review).
