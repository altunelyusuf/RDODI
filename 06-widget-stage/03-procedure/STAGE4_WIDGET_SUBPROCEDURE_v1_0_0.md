# Stage 4 Widget Sub-Procedure v1.0.0 (PROPOSED extension to RDODI procedure §5)

**Status:** PROPOSED — not yet adopted into RDODI_FourStage_Pipeline_Procedure. Consistent with the
coverage/substance gates, ships as a proposed extension pending a procedure-amendment decision.
**Governance:** grounds in the widget-primitives skill's mandatory order + the Phase 2 discourse-selection layer.

## Why this exists
The base procedure §5 requires "at least one interactive element per section" and Stage4.D COUNTS
elements (>=25 buttons, >=6 simulations, etc.). Counting is the count-not-substance trap: it cannot
tell a pedagogical widget from decoration. This sub-procedure makes widgets self-adapting (discourse
selects them) and verifiable (each must encode a tested constraint), closing that gap.

## The discipline (per section that warrants a widget)

**Step W1 — Detect discourse features (auto).**
Run the discourse-widget selector over the section's source text. It emits zero or more candidate
primitives, each with its warrant (which feature fired, mechanical or interpretive tier).
- MECHANICAL features (K-category enumeration, multi-source case set, filterable item set, mixed
  source tiers) fire deterministically.
- INTERPRETIVE features (monotone-temporal-cost, asymmetric-contrast, large-collection, cross-
  attribute-relation, ordered-argument) are routed to an LLM/human judge. The judge's confirmation
  is the fire signal. TIER-C is acceptable here: a wrong widget choice is a fitness-of-form issue,
  never a content-correctness issue.

**Step W2 — Self-adapt: select.**
The pipeline adopts the auto-selected primitive(s). No manual menu in the normal path. If the
selector fires nothing, the section gets a plain (non-widget) interactive element per base §5.2 —
absence of a discourse signal is a valid outcome, not a failure.

**Step W3 — State demonstrates + constraint (BEFORE any HTML).**
For each selected primitive, write down (from its ABox individual): what it demonstrates (tied to a
real Stage-2 concept) and its domain constraint. This is a do-X-before-Y: the constraint is authored
before the markup, never reverse-engineered from it (the skill's "mandatory order").

**Step W4 — Write the design-test (BEFORE the HTML).**
Author the Playwright design-test from the primitive's TestProcedure that proves the constraint holds
against the rendered widget (e.g. the sunk-cost slider is monotone). Test before build.

**Step W5 — Build to the structural spec.**
Implement the widget against the primitive's StructuralSpec (CSS classes, JS symbols), drawing
displayed content ONLY from the grounded Stage-2 ontology + verified sources.

**Step W6 — Run the design-test + emit the selection warrant into the page ABox.**
The widget's page-ABox individual records: which primitive, which discourse feature warranted it
(the span + tier), and the design-test pass/fail. This makes every widget auditable.

## What the gates check (Phase 4)
- **selection-warrant gate** (TIER-C-ok, audited): every widget cites a discourse warrant.
- **content-grounding gate** (TIER-A hard): displayed content traces to Stage-2 + verified sources.
- **design-test gate** (TIER-A hard): the widget's Playwright constraint-test passes.

## Honest boundary
Step W1's interpretive features and the selector's mechanical detectors are routers, not guarantees.
A widget can be mis-selected (wrong form) or a passage's signal missed. Neither corrupts content,
because content grounding (W5) and the design-test (W6) are tier-A and independent of selection.
