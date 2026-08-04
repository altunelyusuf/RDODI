# RDODI Enrichment Prompt Patterns v1.0.0

**What this is:** a catalogue of the prompt/framing features that, in this session, measurably enriched
both the report and the interactive page — turned into (a) guidance for the human and, more importantly,
(b) a **self-application directive** so the LLM adopts these frames *proactively* instead of waiting to be
told. **What this is NOT:** a gate. Prompt style is a *lever* on a probabilistic generator — it raises
expected quality, it does not guarantee it (see §4). It complements the conformance gate (correctness) and
the proposed design-quality gate (richness floor); it does not replace either.

## 1. Why this earns a place in the methodology

This was the user's observation, and the session's evidence confirms it. Every quality *leap* this session
followed a prompt carrying a specific feature, and every *thin* output followed a generic one:

| Output leap | Prompt feature that drove it |
|---|---|
| Report PM-side made the centerpiece | NAMED DEFICIENCY ("the PM side is short") + DIRECTIVE ("make it bolder") |
| Report reorganised to the book | STRUCTURAL PREFERENCE ("match the original book") |
| Four-tradition synthesis written | COMPOSITIONAL DIRECTIVE (name the parts + the operation: "synthesize") |
| Abstract/intro reframed | NAMED DEFICIENCY + corrective DIRECTIVE |
| Page v3 editorial redesign | ROLE ASSIGNMENT ("experienced designer/UX/interactivity") + QUALITY-GOAL ("best expose") |
| Page v4 density + 10 visuals | CONCRETE TRANSFORM DIRECTIVES ("more X, reduce Y, keep Z") + STRUCTURAL PREFERENCE |
| *(counter-evidence)* generic page v1, thin v2 | generic "build the interactive html" — no role, no goal, no transform |

The correlation is consistent enough to act on: **specificity, role, goal-altitude, and named transforms
track enrichment; generic framing tracks thinness.**

## 2. The patterns (the lever)

1. **Role assignment.** Frame the work as a named expert would do it ("as an experienced UX and
   interactivity professional…"). Effect: replaces the generic default frame with a craft frame.
2. **Named deficiency.** State the specific gap, not a vague "improve" ("the PM side is short"; "the
   abstract carries meta-commentary"). Effect: concentrates effort on the real shortfall.
3. **Concrete transform directives.** Say what to change and how, as verbs on content ("more visualization,
   *reduce* textual density, *keep* the text but *thin* it"). Effect: removes guesswork about the operation.
4. **Quality-goal / altitude framing.** State the target standard ("best expose the knowledge"; "academic
   and industrial grade"). Effect: sets the bar the output reaches for.
5. **Structural preference.** Name the desired structure when you have one ("top menu, not left";
   "follow the book's organisation"). Effect: resolves layout/organisation ambiguity directly.

## 3. The important part — LLM SELF-APPLICATION (proactive, not reactive)

The session's quality came late because these frames were supplied *by the user, one round at a time*. The
methodology gain is to have the **LLM apply them by default** at the report and interactive-page stages,
before the first draft — so the floor of effort starts where it took three rounds to reach:

- For a **report** stage, self-frame as a domain expert and academic writer; before drafting, name the
  likely deficiencies (coverage gaps, thin sections, missing synthesis) and address them up front.
- For an **interactive-page** stage, self-frame as a designer + UX + interactivity professional; before
  building, decide the concrete transforms (which concepts become visuals, where density is reduced, what
  the navigation structure is) rather than producing a generic document and awaiting critique.
- Treat the patterns in §2 as a **pre-draft checklist the LLM runs on itself**, then state the frame it
  adopted so the human can correct the frame, not just the output.

This is how prompt style "joins" RDODI: not as a gate, but as a **standing self-elicitation step** at the
two enrichment-sensitive stages, recorded in the operating checklist (rule A2-bis below).

## 4. The honest limits (why this is a lever, not a gate)

- **It raises the expected floor, not a guaranteed one.** A self-applied "act as a great designer" can
  still produce generic "AI-slop" if ungrounded; the patterns improve odds, they do not certify results.
  The conformance gate and the design-quality floor still do the *checking*; this only improves the *input*.
- **Self-prompting is not self-certification.** Adopting an expert role must not become a license to claim
  the output is expert-grade. The output is still judged by the gates and the human ceiling (F105). The
  LLM states the frame it used; it does not grade itself by having used it.
- **Over-framing can distort.** Too many role layers or conflicting directives degrade output; keep the
  self-frame minimal and let the user's actual directives override the defaults.
- It does not touch the irreducibles: factual warrant (F39) and design taste (F105) remain human.

## 5. Checklist addition (wired into the operating checklist)

> **A2-bis — Self-elicit before drafting (report & interactive-page stages).** Before the first draft,
> adopt the relevant expert frame, name the likely deficiencies, and decide the concrete transforms and
> structure. State the frame adopted. This is a lever to raise the starting floor — it does NOT certify
> the result, which is still subject to the conformance gate, the design-quality floor, and human review.
