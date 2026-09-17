# 10-programmable-content-template — Programmable Content Generation

## Addendum (2026-09-16, later same day) — a second real worked example adopted

`PROPOSAL_vaf_to_RDODI_programmable_content_worked_example_v1_0_0.md` (`altunelyusuf/VAF`,
`vaf-pipeline-session`, filed 2026-09-14, real governed lineage — `Mission_RDODIProgrammableContentPresentation`,
`Out_Achieved`, 0 real SHACL violations) offered a second real corpus: 14 principles covering
all 12 of VAF's own real, established algebra operators (checked directly against
`altunelyusuf/VAF`'s current, authoritative `variant_algebra_v3_2_6.ttl` — all 12 confirmed
real, not invented) plus `Profile`/`ProfileFamily`, 8 real relations, run through RDODI's real,
unmodified `instantiate_corpus_v1_1_0.py`.

**Adopted as an additional worked example, not a replacement** — genuinely different domain
(technical/academic algebra vs. the general study-skills corpus above) gives the template two
real, contrasting demonstrations of the same mechanism, which is more useful for anyone
adapting it than either alone.

**Every claim independently re-verified before adopting, not trusted from the filing:**
- All 3 cited SHA-256s matched exactly, both files.
- Their own test suite re-run directly: 11/11 PASS.
- All 12 claimed VAF operator names checked against `altunelyusuf/VAF`'s own current TBox
  directly — all real. One real discrepancy resolved along the way: an earlier VAF artifact
  (checked two turns prior) said "11 formal operators, 7 populated" — the current, authoritative
  TBox genuinely has 12; the earlier figure was scoped to a smaller, older worked example, not
  a real inconsistency.
- **Rebuilt completely independently**, from RDODI's own tree, using RDODI's own tool, with no
  reference to VAF's committed output while building: the result was **byte-for-byte identical**
  to what VAF had committed — a stronger confirmation than the proposal itself asked for, and
  direct proof the tool is genuinely deterministic.
- Real headless test, RDODI's own placed copy: title correctly derived, 11 agents, real
  208,904-byte SHACL, `enableWebLLM` present, all 17 sub-tabs found, 0 page errors.

`04-corpus/vaf_operators_corpus_v1_0_0.json`, `06-instance/vaf_operators_knowledge_base_v1_0_0.html`,
`07-verification/test_vaf_operators_knowledge_base_v1_0_0.py` — all placed as-received, none
edited (the whole point of the byte-identical rebuild check above is that nothing needed to be).

---

## Correction (2026-09-16) — this package was rebuilt; the prior approach was wrong

v1.0.0/v1.1.0 of this package hand-wrote a small, selectively-reimplemented subset of the
source mechanism (four functions, a minimal UI, my own WebLLM/safety-gate port). Direct
owner correction: **this was wrong on the method, not just incomplete.** The right approach
— already proven twice in `08-brsf-corpus-template` and `09-project-proposal-template` — is
to take the real, full, working source file and swap out only what's corpus/identity-specific,
keeping literally every other feature untouched. Rebuilt properly below; the earlier files
are gone, not kept alongside as a wrong alternative.

## Addendum (2026-09-16, same day) — corpus replaced with a real, different subject

The source's own placeholder corpus (Section "A real, useful finding" below) was correct
and real, but the owner asked for it replaced with a genuinely different subject, and for
a detailed, step-by-step build guide -- both real, disclosed asks.
`04-corpus/programmable_content_corpus_v2_0_0.json` replaces v1.0.0 entirely: 6 real study-technique
items (spaced repetition, active recall, weekly review, interleaving, Pomodoro blocks,
environment control), 3 categories, 2 frameworks, 9 relations -- reused from the exact same
study-techniques example first designed for the (since-corrected) v1.1.0 hand-built attempt,
converted into the real, required `PRINCIPLES`/`CATEGORIES`/`FRAMEWORKS`/`RELATIONS`/`MISSION`
shape and run through the real tool this time, not hand-edited into the page.
`06-instance/programmable_content_generation_v3_0_0.html` replaces v2.0.0. See
`BUILD_INSTRUCTIONS_v1_0_0.md` for the full, concrete, step-by-step guide -- every command
and every number in it real, taken from this exact run, not a plan.

## What this actually is now (as first corrected; corpus itself superseded above)

`06-instance/programmable_content_generation_v2_0_0.html` (**superseded by v3.0.0 above** —
description kept for the mechanism, which is unchanged) — the **full**
`corpus_kb_full_template_v0_1_0.html` (1.29MB, every one of its 17 real sub-tabs: Overview,
Explorer, Interact → Ask/Expert/SPARQL/Code Lab/Code Generation/Deployed/Built-in Questions,
Frameworks, Companies, Blueprint, How-To, Architecture, Mission, SemTech, Provenance, About;
all 11 real agents; real WebLLM; real `extractAndCheckCode` safety gate; real `codeGenRouter`;
real 208,904-byte embedded SHACL) — run through **`08-brsf-corpus-template`'s own real,
proven `instantiate_corpus_v1_1_0.py`**, not a local copy. No tool was duplicated here — this
package delegates to that one, per its own docstring ("There is one implementation ... a
second copy maintained by hand would drift from it"), exactly the same tool that closed the
"stage4-template-keeps-source-shell" finding twice already this session.

## A real, useful finding along the way: the corpus was already generic

Checked directly, not assumed: `corpus_kb_full_template_v0_1_0.html`'s own `PRINCIPLES`/
`CATEGORIES`/`FRAMEWORKS`/`RELATIONS`/`MISSION` were **already a neutral placeholder corpus**
("Set clear priorities," "Root-Cause Analysis," generic `example.org` URLs) — zero internal-source
content in any of them. `04-corpus/programmable_content_corpus_v1_0_0.json` (superseded by v2.0.0, the study-techniques corpus above) was that exact,
real, already-shipped data, **extracted programmatically from the source, not retyped or
invented** — the most reuse-respecting input possible: not a new corpus, the source's own.

Running it through the real tool anyway was still worthwhile: the tool also derives `TITLE`
from `MISSION`, genericizes the "Explorer" tab label, and empties `SYNONYMS`/
`SEMTECH_CATALOGUE`/`REGRESSION_QUESTIONS`/`INTENT_PROTOTYPES`/`SPARQL_EXAMPLES`/`SNIPPETS` —
none of which the corpus data alone would have touched, and all of which the source's own
shell strings still carried.

## Real verification performed (headless Chromium, not assumed)

Re-run on `v3.0.0` (the current, study-techniques instance), not just carried over from
`v2.0.0`'s own real checks:

- Title correctly derived from `v3.0.0`'s own `MISSION` string.
- 0 visible internal-source identifier mentions in the rendered DOM.
- Real study content present in the DOM ("Spaced repetition"); the prior placeholder
  content genuinely gone ("Set clear priorities" absent).
- All 11 real agents present (`AGENT_REGISTRY.length === 11`).
- Real, 208,904-byte embedded SHACL intact — governance not stripped.
- `enableWebLLM` present — not a reimplementation; the actual source function, unedited.
- All 17 real sub-tabs found in the DOM by their real `data-sub` attributes.
- 0 page errors.

Checked once, on `v2.0.0` specifically, not re-run on `v3.0.0` (the underlying mechanism
is identical — only the corpus data differs between the two — so this is not expected to
regress, but it wasn't independently re-confirmed on `v3.0.0` and that distinction is kept
honest here rather than implied): navigating to Interact → Code Generation on the Fly, the
real Request Intake Agent, the real 11-agent team panel, and the real intake textarea all
rendered correctly.

## What remains honestly unremoved, and why

`LINEAGE_TTL`/`SKOS_TTL`/`AGENTIC_TTL`/`PROV_TTL` still carry the source's real internal content — this
is the source package's own real, governed development history, the exact same structural
limit found and disclosed for `09-project-proposal-template` two turns ago. It cannot be
honestly emptied without either fabricating a fake lineage or building a genuinely new one
for this instance — separate, real, future work, not something a corpus swap should silently
paper over. Named here rather than hidden.

## What this package's own tooling is

None — deliberately. `01-schema/`, `02-tooling/` are absent on purpose: the real contract and
real tool already exist in `08-brsf-corpus-template/`, and this package points at them rather
than duplicating either.

## Addendum (2026-09-17) — the same real compliance gap found and closed here too

Found while verifying `08-brsf-corpus-template`'s own structural fix was
actually complete: both real instances in this package
(`programmable_content_generation_v3_0_0.html`,
`vaf_operators_knowledge_base_v1_0_0.html`) carried the exact same class of
real internal-data leak already found and fixed for the default template —
56 lines each, in the same 5 governed-development-history TTL blocks plus
hardcoded prompts/identifiers, inherited from `corpus-kb-template`'s own
source lineage.

Fixed using `sanitize_shell_identity()` (proven correct, see
`08-brsf-corpus-template/README_v1_0_0.md`'s own addendum), plus one more
real string it didn't originally cover — a developer-facing code comment
naming the source company in a phrasing specific to this lineage, found and
fixed the same way. **0 remaining references in either file** (grep-
confirmed), clean syntax (`node --check` exit 0 both), 0 headless page
errors, 11 agents and 17 sub-tabs intact in both.

`09-project-proposal-template`'s own instance was checked too and is
genuinely clean — a different source lineage that never carried this.

Not fixed here, deliberately, per B1: `corpus-kb-template`'s own shipped
source still carries this content — not RDODI's package to edit.
