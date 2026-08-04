# RDODI Authoring Scaffolds — v1.0.0
# Closes the depth-capture loop: the rubric says WHAT is missing; scaffolds DRAFT it for review.

## The loop (now complete)
  richness rubric (measures depth, flags gaps)
       ->  authoring scaffolds (draft the missing content as reviewable TTL)
       ->  human reviews/edits the REVIEW: markers, merges
       ->  re-run rubric (score rises) ; re-run gate (BAR_MET when depth >=75%)

## What it drafts (deterministic, structural — always reliable)
- missing-example : an ExampleCase skeleton per concept lacking one, with the concept's own definition as a
  hint, exampleDomain/exampleText prompts, and a turtle caseCode stub (so the result can later be COMPUTED).
- thin-treatment  : a treatment template with section prompts (definition / why / how-used-with-example /
  relations / contrast), target >=300 chars.
- missing-feature : correct JSON skeletons for rich features (techCompareRich etc.), targeted at the
  most-connected concepts, with REVIEW: fields (schemas in RDODI_feature_schemas_v1_0_0.json).
- formal-axioms   : a domain ObjectProperty stub + conservative candidate relationships (each marked REVIEW,
  presented as suggestions not facts) + a disjointness prompt.

Everything is emitted marked "DRAFT — needs review" with REVIEW: markers; nothing is auto-committed (HITL).

## Content hook (--llm) — honest status
Structural scaffolding is deterministic and shipped. Filling drafts with real prose/examples is an LLM task;
the documented hook calls the Anthropic API (same pattern the artifact pipeline already uses) and REQUIRES a
key at run time. Without a key, scaffolds emit structurally-correct placeholders + guidance (always works).

## Proven (loop validated end-to-end)
Thin crypto demo: rubric 24.4% BELOW_BAR -> scaffolds drafted 3 examples + 5 treatments + 3 features + axioms ->
an author filled them -> rubric 51.7% (Treatment depth & Worked examples now 1.0; formal axioms credited).
The demo stays below bar only because it is genuinely small (5 concepts < 12) — correct behavior.
Rubric bug fixed in passing: formal-axioms now counts assertions via ANY domain ObjectProperty (was hard-coded to
the semantic-tech property names). SCP unchanged at 97.9% (no regression).
