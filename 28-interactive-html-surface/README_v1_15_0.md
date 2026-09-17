# 28-interactive-html-surface — start here, before opening any file below

**Owner ruling 2026-08-27 (reverses README_v1_0_0.md's guidance — see that
file's history in git, not deleted, retired per this package's
current-versions-only convention for standard docs):** the rich,
sidebar-tree + tabs + grounded-chat pattern is now RDODI's **default**
Stage 4 deliverable. The single flowing anchor-page and the native S6
generator are both real, valid **variations for other requirements** (a
smaller artifact, a minimal-dependency context), not the default any more.

## The default

`08-brsf-corpus-template/` — corpus-instantiation mechanism (source page +
`instantiate_corpus_v1_0_0.py`), producing pages like
`06-instance/rdodi_lineage_interactive_v3_0_0.html`: hierarchical left
sidebar tree, top+sub tabs, grounded chat/prompt console over the
artifact's own content. Pattern originates in this ecosystem's own internal knowledge-base package, an
unrelated package in the same monorepo — adopted here deliberately, not by
accident (see `Handover_RDODI_Template_Drift_v1_0_0.md`,
github.com/altunelyusuf/RDODI-Research, for the investigation that
surfaced the choice).

**Honest limit, unchanged by this ruling:** the sidebar/tabs are in-page JS
panel-swapping over one HTML file, not separate routable pages
(`grep`-confirmed: 0 routing constructs). `ipo:SubPageTabs`/
`ipo:PageHierarchy` require real routable sub-pages and do not correctly
describe this pattern despite the visual resemblance — they remain
genuinely unused vocabulary. Making this the default does not close that
gap; it would be a category error to claim otherwise.

## The variations

- **Single flowing anchor-page** —
  the excluded worked-example material's own single-page variant
  or `15-presentation/rdodi_presentation_renderer_v1_0_0.py`. Use for
  smaller artifacts or minimal-dependency contexts (BP-D34's pill-bar/
  sidebar thresholds still govern this variation's own navigation shape).
- **`06-s6-exemplar/`** — RDODI's native Stage-4 generator family, a third,
  separate mechanism, still not reconciled with the corpus-instantiation
  approach above (open question, unchanged since it was first raised).

## Proposal-genre pages (2026-09-14)

`08-brsf-corpus-template/`'s own README named this question open (which
mechanism fits `prof:ProjectProposalKind`'s 18-hierarchical-section shape).
Answered with a working example, not a rule: **`09-project-proposal-template/`**
— a register-compiling generator extracted from `vaf-agentic-pipeline`'s
real Stage 4 page, independently re-verified before being brought in (see
its own README for what was checked). Genuinely a fourth mechanism, not a
variant of the three above: it compiles from a governed BRSF register
rather than swapping a corpus or rendering a flat document. Not yet a
finished, generic template — real, identified, disclosed follow-on work
remains (namespace parameterization, externalizing project-specific data
tables) — but proven end-to-end on one real instance.

## Programmable content generation (2026-09-16, corrected same day)

**`10-programmable-content-template/`** — a fifth mechanism, orthogonal to
the four above: gives a page the ability to generate real, tested code
from a plain-language request against its own corpus, live, in the
browser. First built by hand-reimplementing a subset of
`corpus-kb-template`'s real "Code Generation on the Fly" mechanism --
direct owner correction: wrong method, not just incomplete. Rebuilt the
same day the right way, proven twice already in this same package
(`08-brsf-corpus-template`, `09-project-proposal-template`): the real,
full source file run through `08-brsf-corpus-template`'s own real
`instantiate_corpus_v1_1_0.py` -- no new tool, no reimplementation, every
one of the source's 17 real sub-tabs and 11 real agents kept intact,
confirmed by direct headless testing, not assumed. See its own README
for the full trail, including a real finding (the source's own corpus
data was already generic, zero LC Waikiki content) and one honestly
unremoved limitation (the source's real governed lineage/provenance
history, the same structural limit already disclosed for
`09-project-proposal-template`).

See `RDODI_FourStage_Pipeline_Procedure_v1_3_0.md` §5.3 for the governing
procedure text.

## Default resynced (2026-09-17)

The default's own instance (`08-brsf-corpus-template/06-instance/`) had
gone stale — one commit since v1.102.0, its upstream source 17 real
releases behind. Resynced to this ecosystem's own internal source template's latest version; see that
package's own README addendum (internal, not part of this public edition) for the full, real verification trail.
`rdodi_lineage_interactive_v5_0_0.html` replaces v4.0.0.

## Real internal-data removal, same day — v6.0.0

Direct legal/compliance instruction: a real company's internal data in a
generally-accessible repository is not acceptable, disclosed or not.
`rdodi_lineage_interactive_v6_0_0.html` replaces v5.0.0 — 253,498 bytes of
real internal governed-development history and internal-document-derived
content removed, proven safe by direct testing (0 page errors, every real
consuming sub-view exercised). A real, disclosed remainder — content woven
into the shell's own JS logic (prompts, regex, hardcoded UI strings), not
swappable constants — is named precisely, not implied solved. Full trail in that package's own internal README addendum (not part of this public edition).

## Job finished, same day — v7.0.0

`rdodi_lineage_interactive_v7_0_0.html` replaces v6.0.0 — grep-confirmed
0 remaining occurrences of the internal source's own company name or package identifiers anywhere in the file
(down from 57), every category replaced with generic naming where deletion
wasn't possible (a hardcoded field key, LLM prompts, namespace URIs,
identifiers, download filenames, UI text), function fully preserved and
directly re-verified. One real syntax bug introduced by a careless
apostrophe-in-replacement was caught by `node --check` and fixed before
shipping, not assumed clean. Full trail in
that package's own internal README addendum (not part of this public edition).

**This is the current default Stage 4 template:**
https://github.com/altunelyusuf/Ontologies/blob/main/rdodi-ecosystem/28-interactive-html-surface/08-brsf-corpus-template/06-instance/rdodi_lineage_interactive_v14_0_0.html

## Structural fix, same day — instantiate_corpus_v1_2_0.py

The default's own real internal-data leak, fixed by hand in
`rdodi_lineage_interactive_v7_0_0.html`, is now structural:
`08-brsf-corpus-template/02-tooling/instantiate_corpus_v1_2_0.py` applies
the same, now-proven fix to *every* future instantiation, unconditionally.
Proven correct against two genuinely different corpora before being
trusted (byte-identical reproduction of the real hand-fixed file; a
second, independent run with VAF's real algebra operators). The same real
gap was also found and fixed in both of `10-programmable-content-template`'s
own shipped instances while verifying this was actually complete. Full
trail in each package's own README addenda.

## Six real UI/data bugs fixed, same day — v8.0.0

`rdodi_lineage_interactive_v8_0_0.html` replaces v7.0.0: sidebar menu
items were full sentences (the corpus lacked real short labels, now
authored); no visible tooltip on hover (added as a new tool transform);
2 of 3 external framework links pointed at retired file versions
(corrected); relations didn't appear in the relation map (the corpus's
relation-type vocabulary didn't match the shell's fixed 5-type set,
remapped); "Principle undefined" (two missing corpus fields, added);
hardcoded "of 20" wrong for a 21-principle corpus (now derives from the
real count). Full verification trail in
that package's own internal README addendum (not part of this public edition).

## Two more real fixes, same day — v9.0.0

`rdodi_lineage_interactive_v9_0_0.html` replaces v8.0.0: Code Lab's preset
buttons populated empty/`"undefined"` source (a real gap in v1.1.0's own
`SNIPPETS` default, now carrying working, generic Python for all 4 real
buttons, verified by actually running one through Pyodide); WebLLM's two
engines converted from main-thread `CreateMLCEngine` to Worker-based
`CreateWebWorkerMLCEngine`, the library's own documented fix for exactly
the class of blocking concern raised — the deterministic pipeline was
directly measured and never actually blocks the main thread, but the
Worker conversion is the correct fix regardless for the one path (real
WebLLM inference) this sandbox has no GPU to verify. The requested sidebar
style and ontology-graph representation from the COM8090 capstone's
interactive companion were investigated and identified concretely, but
are scoped as a separate, larger next increment. Full trail in
that package's own internal README addendum (not part of this public edition).

## Sidebar style adoption from the COM8090 reference page — v10.0.0

`rdodi_lineage_interactive_v10_0_0.html` replaces v9.0.0: dark-mode CSS
variables with a header toggle, a serif/sans-serif font pairing, a live
sidebar filter input, and tree-row markup restructured to match
`vaf_ap_page_v7_7_0.html`'s own twisty/icon/label/count pattern — all
built as new unconditional tool transforms, so every future instance
gets them too. Full regression re-confirmed clean after the change. The
reference page's genuine interactive ontology-graph view remains a
separate, scoped next increment. Full trail in
that package's own internal README addendum (not part of this public edition).

## Genuine interactive Ontology & Taxonomy graph — v11.0.0, completes the request

`rdodi_lineage_interactive_v11_0_0.html` replaces v10.0.0: a real
node-link "Ontology graph" sub-tab under Overview, distinct from the
existing relation map. Real `{nodes, edges}` model (classes/individuals/
external, built from the corpus itself) rendered via a genuine
force-directed layout verified standalone in Node before being trusted
(0 overlaps, 0 out-of-bounds at real scale), with Fit/Re-layout/
Filter-by-kind controls matching the reference page's own pattern.
Verified directly: 28 nodes, 53 edges, node-click detail cards, working
filter and re-layout, 0 page errors. Full regression re-confirmed every
earlier fix this session still intact. This closes the four-part style/
representation request from `vaf_ap_page_v7_7_0.html` in full. Full
trail in that package's own internal README addendum (not part of this public edition).

## WebLLM Worker reverted; real layout bug fixed — v12.0.0

`rdodi_lineage_interactive_v12_0_0.html` replaces v11.0.0: reverted the
Worker-based WebLLM conversion (disclosed unverified when shipped;
direct real-user report the same day that Live LLM can no longer be
enabled is the strongest evidence a GPU-capable browser hit a real
problem with it) back to the previously-proven main-thread
`CreateMLCEngine()`. Separately, root-caused and fixed the real layout
bug behind "prompt space hardly visible, below the fold": a forced
180px minimum height on the empty chat area, stacked with banner/toggle
padding and an oversized placeholder margin. Measured before/after at a
realistic small viewport: input moved from y=509 (below the fold) to
y=359 (fully visible). Full regression re-confirmed everything else
still works. Full trail in
that package's own internal README addendum (not part of this public edition).

## Code Generation view decluttered — v13.0.0

`rdodi_lineage_interactive_v13_0_0.html` replaces v12.0.0: restructured
the Code Generation view per a direct "too much for interaction" report.
The request textarea and Process button now open the view directly; the
engine-order/output-mode pickers and the long explainer collapse into
`<details>` sections, the same pattern the shell already uses for
"Browse by category" and "How this works". Measured before/after at a
realistic viewport: request input moved from y=794 (far off-screen) to
y=262 (immediately visible). Full regression re-confirmed everything
else still works. Full trail in
that package's own internal README addendum (not part of this public edition).

## Regression from the previous fix: agent team leaking into unrelated sub-pages — v14.0.0

`rdodi_lineage_interactive_v14_0_0.html` replaces v13.0.0: fixed a real
bug introduced by v1.123.0's own restructuring. That change closed the
Request Intake card's div early, leaving the original tail content
(still expecting to close it) to instead consume `#sub-search-codegen`'s
own closing tag — pushing the "agent team" card out to become a direct
sibling of every Interact sub-tab, outside the `.subview` visibility
toggling, so it rendered permanently on Ask, Code Lab, SPARQL Console
and elsewhere. Found by tracing the live DOM ancestor chain, reproduced
with a simulated completed run (11 stray `.agent-chip` elements on three
unrelated views), fixed by correctly closing the card once around all
of its real content. Verified after: 0 leaked chips anywhere but Code
Generation itself. Full trail, including what the uploaded session logs
corroborated, in that package's own internal README addendum (not part of this public edition).
