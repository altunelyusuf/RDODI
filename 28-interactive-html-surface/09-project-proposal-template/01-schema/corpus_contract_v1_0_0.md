# Project Proposal template — corpus contract v1.0.0

Written honestly late, per `README_v1_0_0.md`'s own statement: this contract couldn't
be written until the two follow-on items it named were actually done. They are
(`HANDOVER_vaf-agentic-pipeline_to_RDODI_project-proposal-template-followons_v1_0_0.md`,
2026-09-14, independently re-verified — every SHA matched, 64/64 regression re-run,
0/0 coverage re-run — before this contract was written from it).

## What an adopter supplies

1. **A BRSF register directory** (`08-lineage/*.ttl`) — the governed Mission/Scope/
   Goal/Objective/Backlog register the page and document are both compiled from.
2. **A blueprint file** — the domain-entity/lifecycle-coverage model
   (`backlog:Blueprint`) the register's own work items reference.
3. **A prose file** in the placeholder grammar (`{{counts.*}}`, `{{TABLE:*}}`,
   `{{tab:*}}`) — the narrative every adopter genuinely writes themselves; the
   template is the section skeleton and the placeholder grammar, never the sentences.
4. **A project-data JSON**, in the shape of `02-tooling/proposal_project_data_v1_0_0.json`
   (real, shipped example — not a stub): `title`, `subtitle`, `course_line`,
   `institution_line`, `advisor`/`advisor_email`, `owner_name`, `framework` (name/
   namespace/prefix/label/repository/pin), `project_namespace`, `instances_namespace`,
   `other_namespaces` (any further aligned packages), plus the five tables the
   handover's own §4 originally flagged as project-bound: `team_extra_rows`, `risks`,
   `institution`, `supervision`, `learning_objectives`, `academic_milestones_first`,
   `academic_milestone_weights`, `peer_evaluation`, `signatures`, `abbreviations`,
   and `review_note`. Register references inside this data use `{wi:<id>}`,
   `{goal:<id>}`, `{goals_facing:<Facing>}`, `{external_blocked}`, `{gaps_semantic}`
   — resolved against the register at build time; an unknown name fails the build
   rather than silently printing a bare identifier.
5. **A pin file** (`SCAMPS_PIN.txt`-shaped) — commit and per-file hashes for the
   register directory. The generators refuse to build from a checkout that doesn't
   match it; the coverage gate now refuses to check against anything else too
   (`proposal_coverage_check_v1_3_0.py`, closing the real finding this session
   raised: a stale bundled fallback snapshot silently produced false "missing"
   results — the gate now requires `SCAMPS_ROOT` set explicitly, or
   `ALLOW_SNAPSHOT=1` to use a snapshot knowingly).

## What is reused unchanged (generic, checked by grep before trusting)

`page_from_register_v2_7_0.py`, `page_models_v2_4_0.js`,
`proposal_from_register_v2_4_0.py`, `proposal_coverage_check_v1_3_0.py`,
`page_regression_check_v2_4_0.js`, `page_console_v2_0_0.js`, and
`page_template_v2_1_0.html` (RDODI's own `%%TITLE%%`/`%%SUBTITLE%%` placeholders,
adopted unchanged per L-105 — the one piece RDODI itself parameterized last pass,
now confirmed reused rather than duplicated).

## Real verification this contract rests on, not assumed

- 64/64 page regression (headless, all tabs/sub-tabs/models/graphs, title/subtitle
  now checked as coming from the data, not the shell).
- 0 missing / 0 foreign coverage, against the real pinned register
  (`altunelyusuf/SCAMPS` commit `99b654688358cef29b906a835053495b91b787c3`, `v0.5.0`).
- The coverage gate's new refusal behavior independently re-run: with `SCAMPS_ROOT`
  unset, it now refuses outright rather than falling back silently.

## Honest, disclosed anomaly found while verifying this deposit

`page_regression_check_v2_4_0.js` carries genuinely different content than the copy
this package shipped one turn ago (a 64th check was added) under the **same**
version-numbered filename — a real, same-class versioning-discipline gap as one
found independently this session in `backlog-roadmap-framework`'s own lineage
discipline document. Not blocking (the current content is what was verified and
used), but named rather than silently absorbed.

**Fixed, 2026-09-16**: renamed to `page_regression_check_v2_5_0.js`, disclosing the real
edit count under the old frozen filename (6 edits, `git log --follow`, checked not
assumed). `backlog-roadmap-framework` built a real, permanent mechanism against this
exact pattern recurring (`backlog_version_freeze_check_v1_0_0.py`, wired into its own
release gate); this package's own copy is fixed by the same standard, not left as an
open anomaly.
