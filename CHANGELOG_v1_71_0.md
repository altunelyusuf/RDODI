# RDODI Ecosystem — CHANGELOG v1.71.0
**Bump:** MINOR · **Lineage:** CONTINUATION · **Predecessor:** rdodi_ecosystem_v1_70_0 · SHA-256 `e28f1c13f1f2a0bf7178faf32537d261c08a317063a5e3dc7c8a4fdf6dffb54e`
**Package S11** — comprehensive correction round, triggered directly by user-reported, precisely-described bugs. Full disclosure below; nothing smoothed over.

## Issue 1 — PrimaryNav rendered literal "{{c}}" text (the exact bug the user quoted)
**Root cause, precisely traced**: line 306 of the generator mixed an f-string prefix with a later
plain-string concatenation segment inconsistently — `f'...{{c}}...'` (f-string, correctly escapes to
literal `{c}`) + `'...{{c}}...'` (plain string, NO escaping rule applies, so `{{c}}` passed through
completely literally). This bug existed since S8b and was never caught because the affordance-grounding gate
only checks the wrapping `<nav>` element's signature, never its children's actual text content — a real,
now-acknowledged blind spot in structural-only verification. Fixed by rewriting via plain-string
concatenation throughout (the same safe pattern used everywhere else in this codebase since S7).
**Systematic sweep performed**, not a single-point patch: searched the whole rendered HTML for every
`{x}`/`{{x}}` artifact; found and ruled out false positives (`${v}`, `${x}`, `${y}` are legitimate JS
template-literal syntax, confirmed by checking each is preceded by `$`).

## Issue 2 — subtabs appeared to run together with no visible separation
Verified subtab *clicking* was always functionally correct (confirmed by direct test). The genuine issue was
insufficient visual separation. Strengthened: 2px borders (was 1px), visible box-shadow, larger padding,
explicit gap, focus-visible outline.

## Issue 3 — TreeNavigation "not functional," "no sub-menus at all" (accurate, serious finding)
**The user was correct in the deepest sense**: the tree used real `role="tree"`/`role="treeitem"` ARIA
markup over content that was never actually hierarchical — a flat 6-item list wearing tree semantics
dishonestly. Rebuilt as a genuine 2-level hierarchy: 4 real groups (by actual cryptographic classification —
Public-Key, Symmetric, Hashing, Protocols) each containing real nested `<ul role="group">` children.
**Two bugs found and fixed while wiring this**, both disclosed:
1. `aria-expanded` was initially set to the INVERSE of the actual visible state (a genuine logic inversion,
   caught by testing, not assumed correct because the code "looked right").
2. Clicking the group area itself was ambiguous once expanded (Playwright/a real click can land in the now
   larger child region rather than the header) — fixed with a dedicated `.tree-group-toggle` button, unambiguous
   regardless of expand state.
Tree leaves now genuinely navigate to their concept's view on click (previously wired to nothing at all).

## Issue 4 — Open All / Close All "not functional" (accurate — genuinely no visible effect existed)
Confirmed: the `aria-expanded` attribute DID technically flip before this fix, but with a flat tree there was
nothing to expand or collapse, so the buttons had **zero practical effect** — a passing automated check
(attribute changes) masking a real, meaningful failure (nothing visibly happens). Now genuinely shows/hides
the real nested groups built in Issue 3.

## Issue 5 — "Browser pop-ups are not a good solution"
The reference-details modal was a centered dark-overlay box, visually similar to a native browser
alert/confirm dialog. Converted to a clearly custom right-side slide-in panel (fixed position, 360px,
left border accent, box-shadow) — unambiguously a custom UI element, not overlay-modal styling. Focus-trap
logic (S9c) re-verified working identically in the new layout.

## A new, genuine (not false-positive) affordance-grounding finding
Adding real `:focus-visible` outlines for keyboard accessibility (on subtabs and the new tree-toggle button)
made `FocusIndicator` show up as realized-but-undeclared. Unlike the earlier Tooltip `:focus` collision
(fixed by removing it — that one served a different purpose), this one is a genuine, honest focus indicator.
Declared it in `page.ttl` rather than suppressing the signature.

## Verified (L-65) — full regression, all suites, after every fix
Affordance-grounding gate: PASS (19 declared, including the new honest `FocusIndicator`). S8a's 17/17
Mandatory: PASS. S8e's 8/8 Optional: PASS. Router-functional gate: PASS, 0 console errors. S9c's modal
focus-trap sequence re-verified working identically in the new side-panel layout.

## The honest summary
Every one of the user's reported issues was real. Several (TreeNavigation's dishonest markup, Open/Close
All's non-functional buttons) were more serious than a surface bug — they were features that LOOKED correct
to automated tests checking narrow properties (does an attribute change) while genuinely failing the actual
user need (does anything meaningful happen). This round fixes the substance, not just the symptom.
