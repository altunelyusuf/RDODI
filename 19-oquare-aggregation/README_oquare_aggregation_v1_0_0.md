# R1 — ISO-25000 OQuaRE Characteristic Aggregation v1.0.0 (GUARDED)
Aggregates the OQuaRE base metrics into ISO/IEC-25000-aligned characteristic scores — built behind a structural honesty guard because an aggregated score is easily mistaken for a certification.

## Structural honesty guards
- **G1 declared config** — `oquare_scaling_config_v1_0_0.ttl` holds the scaling bands + characteristic matrix, attributed to OQuaRE (Duque-Ramos et al.) and flagged VERIFY-AGAINST-SOURCE. No invented canonical values; replace bands with the published ones for OQuaRE-exact scores.
- **G2 no bare scores** — every characteristic emits its constituent metrics, each metric's raw + scaled (1–5) value, and the exact band derivation.
- **G3 indicative status** — output declares itself INDICATIVE / computed-per-declared-method / NOT a certification.
- **G4 separate overlay** — the base-metric layer (assessor v1.2.0) is untouched.

## Verified run (the demo domain)
Structural 3.8/5, Maintainability 4.2/5, FunctionalAdequacy 3.0/5 — each shown WITH full derivation (see oquare_aggregation_report.json). Guard checks: no bare scores, indicative label, derivation on every constituent — all True.

## What this is NOT
Not a certification, not OQuaRE-exact unless the declared bands are replaced with the published thresholds. It is a transparent, auditable, indicative aggregation.
