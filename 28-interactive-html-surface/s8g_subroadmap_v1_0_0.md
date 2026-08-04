# S8g Sub-Roadmap: RunnableCodeTool Taxonomy (v1.0.0)
**Decomposes:** CR-S8.8 of s8_backlog_roadmap_v1_0_0.md (frozen `93b70b36…`), by the same discipline S8 itself was decomposed under — applied to itself, per the analysis two turns ago.

## Objective
Deliver `RunnableCodeTool`'s 4 real execution engines + extensibility proof as ordered, independently-verifiable sub-packages, isolating the hardest decision (Python execution) rather than blending it into an undifferentiated build.

## Cost / Benefit / Risk

| Pkg | Content | Benefit | Risk | Cost |
|---|---|---|---|---|
| **S8g-a** | `JavaScriptEngine` — native browser execution | Proves umbrella→engine→live-visualization pattern cheaply, first | Low | Low |
| **S8g-b** | `SPARQLEngine` — the concretely evidenced gap (enterprise_agentic_kb) | Highest direct evidence-to-value ratio | Medium | Medium |
| **S8g-c** | `SHACLValidationEngine` — directly RDODI-relevant | High relevance to RDODI's own discipline | Medium-high | Medium-high |
| **S8g-d** | `PythonEngine` | Completes the user's literal spec | **Highest** — real dependency-vs-scope decision, isolated not blended | **Highest** |
| **S8g-e** | Extensibility proof — 5th engine, umbrella untouched | Proves CR-S8.8's own extensibility requirement | Low (once ≥2 engines exist) | Low |
| **S8g-final** | All engines assembled + full regression | Required — nothing counts as real until proven together | Medium | Medium |

## Roadmap (dependency order)
```
S8g-a (JS, cheapest) → S8g-b (SPARQL, evidenced) → S8g-c (SHACL) → S8g-d (Python, hardest, isolated)
                                                                              │
                                                                              ▼
                                                                  S8g-e (extensibility proof)
                                                                              │
                                                                              ▼
                                                                     S8g-final (assemble + regress)
```

## Definition of Done, per package
Each package: real behavioral verification (execution genuinely runs, live result genuinely renders,
synchronized across table/graph/schema views where applicable); no regression on S6/S8a/S8e's already-passing
suites; versioned CONTINUATION with self-verifying manifest; full-corpus TTL regression 0 failures.

## Final full package
One assembled `rdodi_ecosystem` release once S8g-a through S8g-e all meet DoD, with S8g-final's assembled
regression as its own explicit gate.

## Change control
Frozen before building, per the analysis given and approved. Divergence mid-build is the signal to stop and
re-version (BP-D7), the same rule honored throughout this whole effort.

---
**Freeze SHA-256:** `34a7b488b2ffe101f13026e00df5f36c219aadc244506ca76ff1bad9ad1ee55c`
