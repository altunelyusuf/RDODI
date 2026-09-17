# Building an RDODI Interactive HTML for a New Corpus

Version 1.0.0. Every figure below was measured against a real shipped page
(`lcw_kb_interactive_v0_71_0.html`, 1,116,524 bytes) and every claim about the
result was verified by loading an instantiated page in a browser, not inferred.

## 1. What this template actually is

**There is no separate template file, deliberately.** L-105 of the OE knowledge
base, verbatim:

> "Before building any new component, gate, or subsystem for a capability, first
> search the existing codebase/graph for an implementation of that capability; if
> one exists, extend or delegate to it, never parallel it."

A hand-maintained second copy of a 1.1 MB page would drift from the real one
within a turn or two. So the template is **the latest shipped page plus an
instantiation script**. You point the script at a real page and a corpus file;
it produces a new page.

## 2. The measured split

| Portion | Bytes | Share | Reused? |
|---|---:|---:|---|
| Corpus-specific constants | 296,337 | 27% | **replaced per corpus** |
| BRSF governance (TBox/ABox/shapes/rules) | 540,115 | 48% | unchanged — corpus-independent |
| Engines, 11-agent team, UI shell, styles | ~280,000 | 25% | unchanged |

Instantiating a corpus therefore rewrites roughly a quarter of the file and
inherits three quarters, including every gate.

## 3. Procedure

### Step 1 — Run the ceremony before anything else
Both parts, in order. They are different things and running one is not running
both:
- **OE boundary B5**: rehydrate the packages, SHA-verify them against their own
  manifests, and check freshness against origin.
- **OE 3-step ceremony**: list the BP/L ids that govern the action with a reason
  each; extract their `skos:definition` **programmatically** from the highest
  `knowledge_base_abox_v*.ttl` (the predicate is `kb:hasLessonId` — do not guess
  it); state what enforcement looks like on this specific action.
- **Lineage ceremony**, if you are starting a new development rather than only
  swapping data: declare the level, fix Mission → **Scope with exclusions** →
  Goals → Objectives *in that order*, state your granularity choice and why, and
  decide how work reaches users.

### Step 2 — Write the corpus file
Match `01-schema/corpus_contract_v1_0_0.json`. Six required keys, six optional.
`04-example-corpus/rcm_corpus_v1_0_0.json` is a complete worked example in a
deliberately different domain (reliability-centred maintenance) so you can see
the shape without the original corpus colouring it.

Two things that will bite otherwise:
- **`PRINCIPLES` cannot be renamed.** The retrieval layer, the SPARQL
  materialiser and the Pyodide bridge all bind to that identifier. Read it as
  "the corpus entry list"; the name is historical.
- **`CATEGORIES[].css` must name a class that exists in the stylesheet**, or
  entries render unstyled. Reuse `strategy` / `execution` / `people` or add your
  own class.

### Step 3 — Instantiate
```
python3 02-tooling/instantiate_corpus_v1_0_0.py \
    --source <a real shipped interactive html> \
    --corpus <your corpus.json> \
    --out    <new page.html> [--check]
```
`--check` prints the replacement plan and writes nothing. The script scans
brace/bracket depth rather than regex-matching the constants, because the values
contain nested JSON and Turtle with escaped quotes.

### Step 4 — Understand what it deliberately empties
`EPICS`, `LINEAGE_TASKS` and `OBJECTIVES` are set to `[]`. They are **not corpus
data** — they mirror the *development's own* governed lineage. Carrying the
source development's lineage into a new page would assert a governed history
that never happened, which is the same class of error as dating a release that
never shipped. Run the lineage ceremony for the new development and let its own
audit tooling repopulate them.

### Step 5 — Verify, do not assume
The claim "it still works" is externally verifiable, so L-65 applies: load the
instantiated page and check it. The reference verification, all of which passed
on the worked example:
- the new corpus renders (entry ids and category labels visible in the DOM)
- the old corpus is **fully** gone — grep the rendered body for the previous
  ids and organisation name
- `AGENT_REGISTRY.length === 11` and the composer still emits its full stage set
- `BACKLOG_SHACL_TTL` is still present and >100 KB — governance intact
- zero page errors captured via `pageerror`
- the rendered `<title>` and visible tab labels contain no identifier of the
  source package (v1.1.0, per HANDOVER_vaf-agentic-pipeline_to_RDODI_stage4-template-keeps-source-shell_v1_0_0.md,
  2026-09-09: the prior version only checked that the old *corpus* was gone,
  which is why the standard instance shipped with the wrong title for two
  versions. HONEST REMAINING GAP, not fixed here: `LINEAGE_TTL` still embeds
  the SOURCE package's real governed lineage (~96 internal-identifier references) --
  this is documented, intentional, out-of-scope for the corpus contract
  (`governed_by_lineage_not_corpus`, "regenerated from the real governed
  TTL, never hand-edited") -- a new instance needs its OWN real lineage
  ceremony, not an emptied/borrowed one. Check the DOM's visible text only,
  not the embedded TTL.)

## 4. What you inherit for free

- **11 registered agents**, each owning exactly one capability, orchestrator
  owning none: intent test, story author, grooming, product owner, lineage
  composer, SHACL conformance, code generation, test generation, execution,
  sprint planner, devops packaging.
- **Real gate enforcement in the browser** — pySHACL via micropip against the
  framework's own shapes, not a re-implementation of them.
- **The full 11-stage BRSF pipeline**: Mission → Scope+exclusion → Goal →
  Objective → Epic/Story → Roadmap+Milestone → Grooming → Planning →
  Iteration → Task → Package.
- Engines: TF-IDF, opt-in embeddings, opt-in local LLM, Oxigraph SPARQL,
  Pyodide.
- Safety infrastructure earned from real failures: non-stdlib import detection,
  `ast.parse` pre-flight syntax checking, output-truncation detection via
  `finish_reason`, HTML-attribute escaping, and session/Code-Lab logging
  detailed enough to diagnose a bug from a downloaded zip.

## 5. What the template will not do for you

Stated plainly so nobody plans around a capability that does not exist:
- **It cannot write to your repository.** No backend, no credentials — by
  design, and building around it would mean shipping write access in code
  anyone can read.
- **It cannot approve its own work on judgement.** Approval must derive from
  Definition-of-Done criterion queries, real test results, MetricObservations
  against objective targets, and SHACL conformance. That constraint is the
  owner's, and it is what makes the automation trustworthy rather than fast.
- **The local model is small.** A 360M model will reach for unavailable
  packages and occasionally produce malformed code. The safety scan and syntax
  pre-check exist because that was measured, not feared — they catch it; they do
  not make the model larger.
