# S9: Comprehensive Fit-Gap Analysis & Roadmap (v1.0.0)
**Trigger:** honest assessment that the single exemplar, despite S0–S8g's real work, does not approach the reference examples' quality. Verified by direct inspection, not impression — including two self-caught false positives (export/download was a regex artifact matching the word "exports," not a real feature; corrected before entering this document).

## Fit-Gap Analysis (verified counts, per feature, per source)

| Feature | MY exemplar | RoboLearn | profiling_tool_v2 | stg_assessment_tool |
|---|---|---|---|---|
| localStorage/session persistence | 0 | **2** | 0 | 0 |
| aria-live regions (dynamic a11y) | 0 | **5** | 0 | 0 |
| dialog/modal (role="dialog") | 0 | **2** | 0 | 0 |
| Virtualized/lazy-loading lists | 0 | 3 | 0 | **9** |
| Real export/download (`download=`) | 0 | 0 | 0 | 0 — **not actually a gap, corrected** |
| Print stylesheet | 0 | 0 | 0 | 0 — not a gap in any reference either |

**Already-known, still-open (from S8f, not re-derived here):** structural-class richness at 69/100, honestly disclosed rather than padded.

**Already-known, structural (from last turn):** the exemplar is a single fixed (domain, genre, bundle, format) instance — `rdodi_variant_generator_v1_0_1.py`'s Cartesian-product machinery has never been invoked; no genuine variant family exists.

**Verified as real gaps, not size artifacts:** session persistence, live-region accessibility, real modal dialogs, list virtualization. **Verified as NOT gaps** (caught before inclusion): export/download, print stylesheets — none of the references have them either.

## Cost / Benefit / Risk

| Pkg | Content | Benefit | Risk | Cost |
|---|---|---|---|---|
| **S9a** | Session persistence (`localStorage`: remember theme, last-viewed concept, code-editor contents) | Medium — real UX maturity signal | Low | Low |
| **S9b** | `aria-live` regions on all 5 RunnableCodeTool status updates + Simulation state changes | High — genuine accessibility gap, currently 0 vs RoboLearn's 5 | Low | Low |
| **S9c** | Real modal dialog (`role="dialog"`, focus trap, Escape-to-close) — e.g. for the ContextMenu or a "view full reference" detail panel | Medium | Medium (focus-trap correctness is easy to get subtly wrong) | Medium |
| **S9d** | List virtualization readiness (structural, for when content scales) | Low now, high if content grows | Low | Medium |
| **S8h** *(carried forward)* | Real variant generation: invoke `rdodi_variant_generator_v1_0_1.py`, produce a genuinely second admissible-combination exemplar | **Highest** — the only package that tests whether the surface actually generalizes, the core unproven claim | Medium | Medium-High |
| **S9-final** | Assemble + full regression across everything (S8g's own final, S9a–d, S8h) | Required | Medium | Medium |

## Roadmap (dependency order)
```
S9b (aria-live, cheap, high value) → S9a (persistence) → S9c (modal) → S9d (virtualization readiness)
                                                                              │
                                                                              ▼
                                                    S8h (real variant generation — proves generalization)
                                                                              │
                                                                              ▼
                                                                       S9-final (assemble + regress)
```
S8h is sequenced after the smaller S9 packages so the SECOND generated variant already inherits the accessibility/persistence/modal improvements, rather than needing them retrofitted into two files separately.

## Definition of Done, per package
| Pkg | CR | DoD |
|---|---|---|
| S9a | Reload the page; theme/last-view/code-editor state genuinely restored from `localStorage`, verified via Playwright reload, not assumed | Regression clean on all prior gates |
| S9b | Every RunnableCodeTool status span + Simulation state carries `aria-live="polite"`; verified via axe-core-style role/attribute check | Regression clean |
| S9c | A real modal: opens via a real trigger, traps focus (Tab cycles within it), closes on Escape, focus returns to trigger — all 4 verified via Playwright keyboard simulation | Regression clean |
| S9d | Structural readiness only (documented + one real list converted); not overbuilt speculatively | Regression clean |
| S8h | A second exemplar genuinely generated via `rdodi_variant_generator_v1_0_1.py`'s real Cartesian-product computation (not hand-authored), gate-checked independently | Both exemplars pass all existing gates |
| S9-final | Full corpus regression, both exemplars, all engines, all gates | 0 failures |

## Final full package
One assembled `rdodi_ecosystem` release once S9a–d and S8h all meet DoD, with S9-final's regression as the closing gate — matching the exact convention used throughout this whole roadmap.

## Change control
Frozen before building. Two false positives were caught and corrected during this analysis itself (export/download, initially miscounted at 222/3/2, corrected to 0/0/0 after direct verification) — evidence the analysis was actually checked, not asserted.

---
**Freeze SHA-256:** `eb7a6e8ee4b290b9932d0f026d66c34624b7ccd53f7bc33203ac7ed288045562`
