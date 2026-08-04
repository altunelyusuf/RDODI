# InteractiveHTMLSurface Roadmap — S7 Addendum (v1.0.0)
**Extends:** InteractiveHTMLSurface_backlog_roadmap_v1_0_0.md (frozen `f5b7be06…`), per its own §8 change control.
**Trigger:** S6's exemplar passed its DoD (structural + non-inert) but was diagnosed as quality-shallow — the DoD never specified depth, only presence. This addendum closes that gap with its own measurable bar.

## Objective
Bring the S6 exemplar to genuine content/visual quality, measured — not "make it better" by impression.

## Confirmation Rules (independently callable, no conversational context needed)
| CR | Measurable bar |
|---|---|
| **CR-S7.1** | `ThreeDimensionalVisualization` issues a real `drawArrays`/`drawElements` call against a non-trivial vertex buffer (≥8 vertices) with a perspective/rotation transform — not just `gl.clear()`. |
| **CR-S7.2** | `Simulation` has ≥3 distinct, JS-verifiable visual states demonstrating a real operation (not a bare counter). |
| **CR-S7.3** | Every concept's prose is ≥3 sentences, forming a paragraph — checked by sentence count, not just character count. |
| **CR-S7.4** | All 8 Optional widgets present AND functionally non-inert (checked via the router-aware functional gate). |
| **CR-S7.5** | A real design system: ≥4 CSS custom-property colors, ≥3 distinct font-size steps, a consistent spacing scale — checked by regex against the shipped CSS. |
| **CR-S7.reg** | Regression: all 17 Mandatory widgets still pass the affordance-grounding gate; functional gate still 0 inert / 0 console errors. |

## Definition of Done
CR-S7.1 through CR-S7.5 PASS, CR-S7.reg PASS (no regression on S6's already-verified structural correctness).

## Content-quality boundary, restated (per the earlier finding this session)
Prose enrichment stays within well-established, general cryptography knowledge (no fabricated statistics, no invented citations). This closes the *presence/depth* gap CR-S7.3 measures; it does not cross into asserting research-grade novel claims, which stays outside what a generation script should originate.
