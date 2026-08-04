# Phase 0 — Concordance + Validation of the Three Stage-4 Vocabularies

**Date:** 2026-05-28 | **Governance:** BP-D2 (read raw), L-72 (reuse-before-invent), L-66 (criteria as written), L-40 (label plainly)
**Purpose:** before originating the discourse-driven widget layer, reconcile what already exists and validate it, so the build extends rather than duplicates and does not sit on an ungrounded base.

## Sources read (raw, this session)
1. SKILL — `widget_skill/widget_primitives_v1_1_0.ttl` (12 classes, 9 props, 0 individuals)
2. RDODI_S4 — `rdodi-v1_1_0/05-stage-disciplines/stage4_page_artifact_kind_v1_0_0.ttl` (2 classes, 27 individuals) + its SHACL (8 NodeShapes)
3. RRWPC_S4 — `rrwpc-v6_3/.../09-stage4-discipline/01-artifact-kind/rrwpc_stage4_artifact_kind_v1_1_1.ttl` (2 classes, 27 individuals)

## Concordance verdicts

| Pair | Verdict | Evidence |
|---|---|---|
| RDODI_S4 vs RRWPC_S4 | **DUPLICATE** | Same 2 classes, same 27 individual names; 23/27 definitions byte-identical; 4 differ only in namespace detail. RDODI_S4 is RRWPC_S4 ported to the RDODI namespace (`example.org/rdodi/...` vs `example.org/rrwpc`). **Disposition: build on RDODI_S4; treat RRWPC_S4 as the retired upstream.** |
| SKILL vs RDODI_S4 | **DISTINCT (different grain) + 1 OVERLAP point** | Zero class-name overlap. SKILL models per-WIDGET patterns (WidgetPrimitive -> DomainConstraint -> TestProcedure); RDODI_S4 models PAGE-level interaction constraints + section roles. They compose at different grains. The single conceptual bridge: `DemonstratesSubject` is a SKILL class AND an RDODI InteractionConstraint individual — the same "must demonstrate its subject" principle at widget-grain vs page-grain. **Disposition: keep both; link via the DemonstratesSubject bridge; neither duplicates the other.** |

## What this means for the build (L-72 reuse-before-invent)
- The page-level interaction-constraint + section-role vocabulary ALREADY EXISTS (RDODI_S4, 27 individuals). Do NOT re-create it.
- The per-widget primitive SCHEMA exists (SKILL, 12 classes) but its DATA does not (0 individuals). Phase 1 instantiates.
- The discourse-signal -> widget-selection layer EXISTS IN NEITHER. Confirmed by property search: SKILL's 9 props cover what a widget IS, none covers WHEN it applies. **This layer must be ORIGINATED (Phase 2) — no prior art to reuse.**

## Validation (grounding check, L-66 criteria as written)

| Check | Result | Verdict |
|---|---|---|
| RDODI_S4 SHACL fires on bad input | empty InteractiveLearningSurface -> 13 sh:Violation | **REAL shapes (not skeleton)** — safe to build on |
| RDODI_S4 individuals grounded | 27/27 labeled, 27/27 defined, **0/27 sourced** | **GAP: no dcterms:source provenance** (BP-D24). Not disqualifying; Phase 1 adds provenance when extending. |
| SKILL classes grounded | 12/12 defined | OK as schema |
| SKILL primitives instantiated | 0/9 | **schema-only — Phase 1 must instantiate** |

## Phase 0 disposition (settled, no fork)
- Build on RDODI_S4 (page grain) + SKILL schema (widget grain), linked via DemonstratesSubject.
- Originate the discourse-selection layer in Phase 2 (no reuse available).
- Carry forward the flagged provenance gap (0/27 sourced) as a Phase-1 fix item.
- No new vocabulary created in Phase 0 (correct — reconciliation only).
