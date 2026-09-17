# 09-project-proposal-template — Stage 4 mechanism for the Project Proposal profile

Answers `28-interactive-html-surface/README_v1_1_0.md`'s own open item 4
("which mechanism fits a proposal-genre page") for real, with a working
example rather than a plan. Extracted from
`vaf-agentic-pipeline`'s real, register-compiled Stage 4 page
(`HANDOVER_vaf-agentic-pipeline_to_RDODI_project-proposal-interactive-template_v1_0_0.md`,
2026-09-14), independently re-verified before anything here was built —
not trusted from the handover's own report.

## Verification performed (not assumed)

- Every cited file's SHA-256 checked against `altunelyusuf/Ontologies` at
  the cited commit (`71de0d9`): **all 12 matched exactly.**
- Regression check (`page_regression_check_v2_4_0.js`) actually run
  against the real page: **63 of 63 passed**, matching the claim exactly.
- Ran it again against a page with one embedded label tampered: **62 of
  63** — the check genuinely discriminates (L-95), not just reports.
- Coverage gate (`proposal_coverage_check_v1_2_0.py`) run twice: first
  against the package's own bundled fallback register (`05-lineage`),
  which reported 3 missing — **a real finding, not a defect in the page**:
  that fallback snapshot is stale relative to the package's own
  `SCAMPS_PIN.txt` (it doesn't even contain the pinned files). Re-run
  against the actual pinned `altunelyusuf/SCAMPS` commit (`99b6546`,
  confirmed to still be that repo's current HEAD): **0 missing, 0
  foreign, PASS** — exactly the claim, once tested correctly.

## What's real and complete here

- `05-source-reference/` — the offered artifacts exactly as received,
  SHA-verified.
- `06-instance/` — the real page, as the example instance the template
  was extracted from (per the handover's own ask 4: this project's page
  stays where it is; this is a copy for RDODI's own reference).
- `02-tooling/page_from_register_v2_6_0.py`,
  `page_regression_check_v2_4_0.js`, `proposal_coverage_check_v1_2_0.py` —
  copied in as-is, per the handover's own measured verdict ("generic as
  is" / "none" project-bound content, checked by grep before trusting).
- `02-tooling/page_template_v2_1_0.html` — the one piece of real
  parameterization done this pass: the two genuinely static,
  visible-text locations (`<title>`, the `<h1>`/`.sub` header) now read
  `%%TITLE%%`/`%%SUBTITLE%%`, reusing this file's own existing
  `%%VERSION%%`/`%%GENERATED%%` placeholder convention (L-105) rather
  than inventing a new one. Diffed against the source: exactly these two
  substitutions, nothing else touched.

## What's real, identified, and NOT done here — genuine follow-on work

- **`page_from_register_v2_6_0.py`'s two namespace parameters** (which
  namespace counts as "the project's" vs "the framework's" in the
  ontology-graph extraction) — the handover's own §4 named this
  precisely; not attempted this pass. The script is usable today only for
  a project whose namespace happens to already match VAF's.
- **`proposal_from_register_v2_3_0.py`'s five project-data tables**
  (risk, team, learning-objectives, institution, abbreviations) — the
  handover's own §4 is explicit these are project data currently written
  in code, not template. Not copied into this package at all yet,
  precisely because copying them as-is would ship VAF's own project data
  as if it were generic template content — worse than not shipping them.
  A future pass should externalise them to the prose file or a YAML
  beside it (the handover's own suggestion), then bring the generator in.
- **`01-schema/`** — left empty this pass. The real contract (one BRSF
  register directory + one blueprint file + one prose file in the
  placeholder grammar + one pin file, per the handover's §6.2) can't be
  written honestly until the two items above are actually done — writing
  it now would describe a contract this package can't yet fulfil.
- **The provenance-tab and "one ontology caption" text** the handover's
  §4 also named as project-bound: not located in the static shell
  (`page_template_v2_1_0.html`) — almost certainly generated dynamically
  by `page_from_register_v2_6_0.py` itself, which is one of the two items
  above.

## Addendum (2026-09-15) — follow-ons done, contract now real

`vaf-agentic-pipeline` returned with both deferred items done and the
packaging finding closed
(`HANDOVER_vaf-agentic-pipeline_to_RDODI_project-proposal-template-followons_v1_0_0.md`),
independently re-verified before anything below was accepted:

- All 8 newly-cited SHA-256s matched exactly against `altunelyusuf/Ontologies`
  commit `af14fb2` (package v0.17.0, manifest 52/52).
- Regression check re-run for real: **64/64** (one new check: title/subtitle
  now genuinely come from project data, not the shell).
- Coverage gate re-run for real: **0 missing, 0 foreign, PASS**.
- The packaging finding this README raised — a stale bundled fallback
  register producing false "missing" results — **independently confirmed
  fixed**: with `SCAMPS_ROOT` unset, the gate now refuses outright rather
  than silently falling back.
- **`01-schema/corpus_contract_v1_0_0.md` written** — the real contract
  this README said couldn't be written honestly until now. See it for
  the full shape.
- Retired: `page_from_register_v2_6_0.py`, the old
  `page_regression_check_v2_4_0.js` and `proposal_coverage_check_v1_2_0.py`
  copies, `vaf_ap_page_v7_6_0.html`, `page_models_v2_3_0.js` — all
  superseded by the versions above.
- **One honest anomaly found while verifying, not silently absorbed**:
  the new `page_regression_check_v2_4_0.js` carries real, different
  content (a 64th check) under the exact same version-numbered filename
  as the copy taken one turn ago — the same class of versioning-discipline
  gap independently found this session in a different package's core
  discipline document. Named in the contract file; not blocking,
  since the content actually used was verified directly.
  **Fixed, 2026-09-16**: renamed to `page_regression_check_v2_5_0.js`,
  6 real edits under the old name disclosed. See the contract file.

Recorded, not re-litigated: the handover is explicit these are decisions
its filing session made once for all adopters (sub-page grouping,
model count/choice, colour-by-kind, the 17 edge kinds, tree depth/icons,
the console's deterministic ranking, no-invention refusal, generated
artefacts never hand-edited). Nothing here overrides any of them; a
future session extending this template should treat changing one of
these eight as a real decision of its own, not a default to drift past.
