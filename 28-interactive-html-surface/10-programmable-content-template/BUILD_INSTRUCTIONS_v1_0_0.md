# Building a Live, Full-Featured Interactive HTML from This Template

Every step below is exactly what produced `06-instance/programmable_content_generation_v3_0_0.html`
— real commands, real output, real verification, not a plan. Where a number appears, it was
measured on this run, not estimated.

## 1. What you're actually building

**There is no separate "blank" template file.** Per L-105 (reuse before building — verbatim
from the OE knowledge base: *"search the existing codebase for an implementation of that
capability; if one exists, extend or delegate to it, never parallel it"*), the real source is
`05-source-reference/corpus_kb_full_template_v0_1_0.html` (1,287,152 bytes) plus one existing
tool, `08-brsf-corpus-template/02-tooling/instantiate_corpus_v1_1_0.py`. You point the tool at
the source and a corpus file; it writes a new, complete page. No local copy of either the
source or the tool lives in this package — pointing at them directly is the whole design.

Doing this by hand — copying the file and manually editing out one project's content — is the
mistake this guide exists to prevent: it produces exactly what v1.0.0/v1.1.0 of this package
did, a partial, drifted reimplementation instead of the real, full mechanism.

## 2. Design your corpus data — the one part that's actually new

Five real, required top-level constants (checked against the tool's own
`CONTRACT_REQUIRED` list, not just its documentation, which is one version ahead in places):

```
MISSION      — one sentence: what this application is for.
CATEGORIES   — { key: { label } }, one entry per grouping your items fall into.
PRINCIPLES   — the actual name the tool matches on; do not rename it, "renaming the
               const is NOT supported" per the tool's own corpus-contract documentation
               (retrieval, SPARQL materialisation, and the Pyodide bridge all bind to
               it by name). Read it as "your corpus items," regardless of subject.
               Each item: id, n, cat, short, en, en_short, fw (list), tools/biases/
               ceremonies (lists, may be empty), reinforces (list), apply, roles (list).
FRAMEWORKS   — { key: { name, url, note } }, external sources your items cite.
RELATIONS    — [{ source, target, type, subtype, evidence }], every real relationship
               worth tracking. type is one of structural/syntactic/semantic/behavioral/
               business.
```

**Real example, from this run** (`04-corpus/programmable_content_corpus_v2_0_0.json`,
6 items, 3 categories, 2 frameworks, 9 relations — a genuinely different subject, study
techniques, not the source's own placeholder content):

```json
{
  "MISSION": "Help a student build a small, real set of evidence-based study habits.",
  "CATEGORIES": {"memory": {"label": "Memory & Recall"}, "planning": {"label": "Planning & Scheduling"}, "focus": {"label": "Focus & Environment"}},
  "FRAMEWORKS": {"spacedrep": {"name": "Spaced Repetition", "url": "...", "note": "..."}},
  "PRINCIPLES": [
    {"id":"P01","n":1,"cat":"memory","short":"Spaced repetition","en":"Review material at increasing intervals rather than cramming once.","en_short":"Review at increasing intervals, not all at once.","fw":["spacedrep"],"tools":[],"biases":[],"ceremonies":[],"reinforces":["P02"],"apply":"Before your next exam, schedule three review passes spaced days apart instead of one long session.","roles":["Student"]}
  ],
  "RELATIONS": [
    {"source":"P01","target":"P02","type":"semantic","subtype":"reinforces","evidence":"Both are retrieval-strengthening techniques."}
  ]
}
```

**Two things this run found worth naming:**
- The relation `type` matters, and it should be true, not decorative — `semantic`
  ("reinforces," a conceptual link) reads differently from `structural`
  ("is-a member of category") or `behavioral` ("co-occurs in practice"). Real corpora with
  richer relation typing get more out of the SPARQL/multi-hop layer than a flat list of
  `"related"` would.
- Reuse your source material's own words for `apply` fields where you can — a concrete,
  actionable instruction ("schedule three review passes...") is what the deterministic
  intent parser and the agents both render back to the reader; vague `apply` text produces
  vague generated output regardless of how good the underlying item is.

## 3. Dry-run before writing anything

```
python3 02-tooling/instantiate_corpus_v1_2_0.py \
    --source <path-to-source>.html \
    --corpus <your-corpus>.json \
    --out <planned-output>.html \
    --check
```

Real output from this run:

```
[PLAN] source 1,287,152 bytes; replacing 5 constant(s):
   MISSION              148 bytes ->        88 bytes
   CATEGORIES           290 bytes ->       150 bytes
   PRINCIPLES         8,788 bytes ->     2,558 bytes
   FRAMEWORKS           675 bytes ->       361 bytes
   RELATIONS          9,417 bytes ->     1,500 bytes
[CHECK] plan only, nothing written.
```

If a constant is missing from `CONTRACT_REQUIRED`, the tool errors here — you find out
before anything is written, not after.

## 4. Run it for real

Drop `--check`. Real output from this run:

```
[OK] wrote .../pct_study_v1_0_0.html (1,237,934 bytes)
[NOTE] EPICS / LINEAGE_TASKS / OBJECTIVES were emptied: a new corpus has no governed
lineage yet. Run the lineage ceremony for the new development and let its own audit
tool repopulate them - do not hand-write them.
[NOTE] TITLE derived from MISSION (unless supplied); TOP_TABS 'explorer' label
genericized (unless supplied); SYNONYMS/SEMTECH_CATALOGUE/REGRESSION_QUESTIONS/
INTENT_PROTOTYPES/SPARQL_EXAMPLES/SNIPPETS emptied where the corpus did not supply
its own. COMPANY_DATA is NOT auto-emptied (buildCompanyView() hardcodes its 5
company keys rather than deriving them) -- still carries the SOURCE package's
company data unless the corpus explicitly overrides it.
```

Read both notes. The first tells you the Deployed-capabilities/governance layer starts
genuinely empty (correct — it has to be earned by real use, not seeded). The second names
exactly one thing the tool cannot safely do for you: if the source's `COMPANY_DATA`
comparison feature matters for your corpus, you must either supply your own (matching
`buildCompanyView`'s real hardcoded key expectations) or accept that the source's stays,
disclosed, until someone patches that one function.

## 5. Verify — don't assume the write succeeded correctly

Every check below is real, run against the actual output file, headless Chromium
(`--ignore-certificate-errors` needed in a sandboxed container whose proxy cert Chromium
doesn't trust by default; not needed on a normal machine):

```python
page.goto("file://.../your-output.html")
page.title()                                            # should be MISSION-derived
document.body.innerText.count("<old corpus's own identifying string>")  # should be 0
typeof AGENT_REGISTRY !== 'undefined' ? AGENT_REGISTRY.length : 'undefined'  # 11
typeof BACKLOG_SHACL_TTL !== 'undefined' ? BACKLOG_SHACL_TTL.length : 'undefined'  # 208904
typeof enableWebLLM === 'function'                       # true
Array.from(document.querySelectorAll('[data-sub]')).map(e => e.dataset.sub)  # 17 real sub-tabs
```

Real results from this run: title correctly derived, 0 mentions of the prior corpus's own
identity, 11 agents, 208,904-byte SHACL, `enableWebLLM` present, all 17 sub-tabs found, 0
page errors. Then navigate to at least one real sub-tab and confirm real content renders —
title/agent-count/tab-list checks alone don't prove the *content* swap actually reached the
UI:

```python
page.click("text='Interact'"); page.click("[data-sub=ask]")
# confirm a real item from your corpus appears, e.g. "Spaced repetition" in this run
```

## 6. What a corpus swap does not, and should not, fix

The source's own governed development history (`LINEAGE_TTL`, `SKOS_TTL`, `AGENTIC_TTL`,
`PROV_TTL`) still names the source package after a swap — checked directly on this run, real
references remain. This is not a bug in the tool: it's the real record of who built the
source template and how, and a corpus swap has no honest way to replace it with a fabricated
history for your new instance. If your new instance needs its own governed lineage, that's a
separate, real lineage ceremony — building one, not silently borrowing or erasing the source's.
