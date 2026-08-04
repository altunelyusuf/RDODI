# R-E7 — Convergent-Validation Harness v1.0.0
Productizes the STG method: pre-register -> blind-build -> seal-reveal -> measured-compare, as a repeatable tool.

## Independence enforced IN CODE (not by manual discipline)
State machine INIT -> PREREGISTERED -> CANDIDATE_FROZEN -> SEALED -> REVEALED -> COMPARED.
- seal_parallel() allowed only AFTER freeze_candidate() — opening earlier could contaminate the build.
- reveal() re-verifies the sealed package is byte-identical, else raises.
- compare() RUNS the same criteria function on both artifacts (measured, never narrated).
Out-of-order calls raise — contamination becomes impossible, not merely discouraged.

## STG regression (this package)
Run on candidate v1.0.1 (`ace69a6c…`) vs sealed parallel (`5196d23f…`):
- premature reveal() correctly RAISES (enforcement proven).
- measured compare reproduces frozen P3: fidelity converges FAIL, OVERALL converges REJECT — both rejected for the SAME reason.
- the one divergence (parallel shacl FAIL) is the partial-assembly artifact P3 documented; the harness reproduces it
  mechanically BECAUSE it lacks correct module assembly — a measured demonstration that **R-E8 (module-assembly
  resolver)** is the right next architecture item.
