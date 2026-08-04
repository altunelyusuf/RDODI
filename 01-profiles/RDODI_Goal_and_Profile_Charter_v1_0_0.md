# RDODI Goal & Profile Charter v1.0.0
**Date:** 2026-06-23 · **Status:** GOVERNING — every stage standard, gate, and worked example is measured against this. Authoring session: RDODI-canonical.
**Why this exists:** the any-artifact goal was never recorded; that absence let course-companion assumptions drift into the Stage-3/4 standards. This charter records it so the drift cannot recur unchallenged.

## 1. The goal
**RDODI is a general engine that generates high-quality, trustworthy artifacts of *any type* for *any subject and domain*.** Output type is selected by an **output profile**; the engine, gates, and mechanical-verification layer are profile- and domain-agnostic.

## 2. What an output profile is (grounded in the existing document ontology)
A profile is a first-class **`ArtifactKindSpec`** (already in `document_ontology_tbox_v1_0_1`), composed of:
- `hasGenre` → an **`ArtifactGenre`** (research-report, technical-report, whitepaper, handbook, FAQ, study-guide, **course-document**, …);
- `hasStructuralTemplate` → a **`StructuralTemplate`** (required/optional sections by name + `sectionOrder`);
- `hasCitationForm`, `hasVoiceConstraint`, `hasQualityScorecardForm` → the genre's citation, voice, and quality conventions;
- a page **surface** profile (to be added to the interactive-page stage — its current `InteractiveLearningSurface` is *one* surface, the course-companion's, not the only one).

The pipeline reads the profile and produces an artifact `conformsToArtifactKind` that spec. **No genre is privileged in the engine.**

## 3. Course companions = profile #1 (a proving ground, not the goal)
The **course-companion** profile is built and proven first — deliberately — because its source content is ready, reference-rich, and has real consumers (registered students). It validates the engine on a consumer-backed vertical. It is **one** profile among many; its presence must never re-shape the general core.

## 4. Governing rules (carry into all RDODI work)
1. **Profile, don't privilege.** Course/education concepts (`BookChapter`, `ChapterSection`, `ReviewQuestion`, `InteractiveLearningSurface`) belong inside the course-companion profile, not in the general stage core. New stage-core vocabulary must be genre-neutral.
2. **Prove by generation.** The engine is demonstrated by *generating* an artifact from source and gating the generated output — never by hand-authoring content into an ABox to pass a gate (the F105 manual-injection trap).
3. **Generality check.** Any claim that "RDODI produces X" must be backed by a profile + a generated, gate-passing exemplar — ideally across ≥2 contrasting genres, so generality is demonstrated, not asserted.
4. **The four stages are genre-neutral.** Research → Domain Ontology → Document → Interactive Page is the fixed spine; only the *profile* varies the output shape.

## 5. Relationship to the enhancement plan
This charter is Track-A1 of `RDODI_Enhancement_Plan_reassessed_v2_0_0`. A2 formalizes profiles on this model; A3 generalizes the page surface; B1 proves the engine by generation under profile #1; C1/C2 (OE-assessor, bootstrap kit) are profile-agnostic leverage.
