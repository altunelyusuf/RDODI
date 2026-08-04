# Package 13 — Definition Conformance Backlog v1.0.0
**Frozen 2026-07-08.** Seeded from `definition_conformance_gate_v1_0_0.py`'s actual run (9/13 clauses failing) against `rdodi_html_generator_v1_0_1.py`. Every cost estimate below cites a real line number in that file; every DoD item is a named gate clause, checkable by re-running the gate — not a prose claim.

Freeze rule (BP-D7): this document is version-controlled like any other artifact. Any change to scope, priority, or DoD after today is a new version (`v1_0_1`+), not a silent edit.

---

## CR-13.1 — Tooltip: focus-triggered display
**Gate clause:** `Tooltip / "...focus help text affordance"` — currently FAIL.
**Location:** `rdodi_html_generator_v1_0_1.py:1901` (`mouseover` handler already exists; no `focus`/`focusin` counterpart).
**Cost:** LOW. Mirror the existing `mouseover`/`mouseout` pair with `focusin`/`focusout` on the same `[data-tip]` selector — same tooltip element, same positioning logic, ~4 new lines.
**Benefit:** Closes the single largest accessibility gap for the cheapest price — keyboard-only and screen-reader users currently get zero tooltip content anywhere in the artifact.
**Risk:** Very low. Additive, isolated, no interaction with other widgets.
**DoD (measurable):** gate clause `Tooltip / "...focus help text affordance"` flips to PASS. No regression on the existing `Tooltip / "Hover..."` PASS.

---

## CR-13.2 — ContextMenu: keyboard trigger, Escape dismissal, focus return
**Gate clauses:** 3 FAIL — `"Shift+F10/ContextMenu key"`, `"dismissed by Escape"`, `"focus returned to the originating element"`.
**Location:** `rdodi_html_generator_v1_0_1.py:1906` (`contextmenu` event listener — mouse-only open path; the existing `click` handler at the unified action-handler block is the only close path).
**Cost:** MEDIUM. Needs: (a) a `keydown` listener detecting `Shift+F10` or the `ContextMenu` key, computing an anchor position from the focused element (no `clientX`/`clientY` available on a keyboard event, unlike the current mouse-driven `e.clientX`/`e.clientY` positioning) — this is the one non-trivial part; (b) a `keydown` listener for `Escape` closing the menu; (c) storing the triggering element on open and calling `.focus()` on it at close, both from Escape and from the existing click-away path.
**Benefit:** Closes 3 of the 9 failing clauses at once — the single highest-yield CR by clause count.
**Risk:** MEDIUM. Touches the existing `contextmenu`/`click` handlers directly (`1906`–`1922`); must not break the already-PASSing context-sensitivity behavior (`data-ctx` branching) while adding the keyboard path.
**DoD (measurable):** all 3 `ContextMenu` FAIL clauses flip to PASS; the 2 existing `ContextMenu` PASS clauses (contextmenu-event-open, context-sensitivity) still PASS.

---

## CR-13.3 — TreeNavigation: focusable, arrow-key traversal, aria-selected
**Gate clauses:** 3 FAIL — `"navigable by keyboard (arrow keys, Home/End, expand/collapse)"`, `"aria-selected"`, `"tree items are focusable"` (tabindex).
**Location:** `rdodi_html_generator_v1_0_1.py:503-510` (`.tx-folder`/`.tx-children` HTML generation, no `tabindex`/`role`/`aria-*` emitted) and `:1944` (`.onclick` only, no `keydown`).
**Cost:** HIGH — the largest single CR. Requires: (a) emitting `tabindex="0"` and `role="treeitem"` on every generated `.tx-folder`/leaf at template-generation time (`503-510`), not just at runtime; (b) a real keyboard state machine for arrow-key tree traversal (Down/Up move focus to next/previous visible item accounting for open/closed state, Right expands or moves into children, Left collapses or moves to parent, Home/End jump to first/last) — this is genuine new logic, not a small patch; (c) toggling `aria-selected` on focus/activation.
**Benefit:** Closes the remaining 3 failing clauses on the widget furthest from conformant (0/3 passing today).
**Risk:** HIGH. The arrow-key traversal logic has real edge cases (nested open/closed state, empty folders, focus loss on DOM changes) that are easy to get subtly wrong; needs the most testing of the four CRs.
**DoD (measurable):** all 3 `TreeNavigation` clauses flip to PASS. Recommend a manual keyboard-only walkthrough in addition to the gate, since the gate checks for the presence of the mechanism (event listeners, attributes), not the correctness of the traversal state machine — that correctness is outside what static source-text checking can verify.

---

## CR-13.4 — SubPageTabs (real routing) + PrimaryNavigation (real distinct widget)
**Gate clauses:** 2 FAIL — `SubPageTabs / "...not in-place panel swaps...routable sub-page with its own location"`, `PrimaryNavigation / "distinct top-level navigation...not the same mechanism as SubPageTabs"`.
**Location:** `rdodi_html_generator_v1_0_1.py:1374` (tab button generation), `:1835` (`show(p)` — pure `classList` toggle, no `pushState`/`location.hash`/`history`).
**Cost:** HIGHEST of the four, and qualitatively different from the other three. This is not a bug-fix patch — it's an information-architecture gap: **the generator currently has only one navigation level.** `PrimaryNavigation` ("major sections") and `SubPageTabs` ("sibling sub-pages under one parent") are two distinct concepts in the TBox, but the generator's content model has no notion of "major section containing sub-pages" — it has one flat set of `.tab`s. Fixing the gate clauses honestly requires deciding what a "major section" is for a domain-agnostic generator before any routing code is written, not just adding `location.hash` to the existing tabs.
**Benefit:** Closes the last 2 failing clauses; also gives the artifact real deep-linking/back-button support, a genuine UX improvement beyond gate conformance.
**Risk:** HIGHEST. Two compounding risks: (a) technical — introducing hash-routing changes `show()`, which every other widget's `gotoTarget()` (`:1839`) already calls, so routing must be threaded through that shared path without breaking context-menu "Open concept" or sidebar navigation; (b) architectural — the major-section/sub-page split has to be inferred generically from the domain ontology's structure (per the generator's own "domain-agnostic" design constraint), which is a real design question, not a coding task.
**DoD (measurable):** both clauses flip to PASS. Additionally recommend: a written one-paragraph design note on what "major section" means generically, reviewed before implementation starts — this CR should not begin with code.

---

## Priority order (cost/risk ascending — quick wins first)

| Order | CR | Clauses closed | Cost | Risk |
|---|---|---|---|---|
| 1 | CR-13.1 Tooltip focus | 1 | LOW | LOW |
| 2 | CR-13.2 ContextMenu keyboard | 3 | MEDIUM | MEDIUM |
| 3 | CR-13.3 TreeNavigation keyboard | 3 | HIGH | HIGH |
| 4 | CR-13.4 SubPageTabs routing + PrimaryNavigation | 2 | HIGHEST | HIGHEST |

Rationale: CR-13.1–13.3 are independent of each other and of CR-13.4 — no ordering dependency forces this sequence, it's pure cost/risk-ascending so gate conformance climbs fastest with least exposure early. CR-13.4 is placed last not because it's less important but because it's the only CR that shouldn't start with code (needs the design note first) — starting it last avoids blocking the other three behind a design decision.

## Definition of Done for the whole backlog
All 13/13 gate clauses PASS on a fresh `definition_conformance_gate_v1_0_0.py` run against a freshly-generated artifact (not a cached one) — matching the same re-verification discipline used to close Package 13's DownloadableResource and generator-fallback proposals.
