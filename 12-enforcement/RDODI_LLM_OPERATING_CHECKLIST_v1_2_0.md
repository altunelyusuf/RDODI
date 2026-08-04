# RDODI PIPELINE — MANDATORY LLM OPERATING CHECKLIST v1.2.0

**Read this BEFORE doing anything with the pipeline. It is derived from real recurring failures
(findings F20, F72, F73, F81, F85, F86, F90, F92, F94, F100). Each rule exists because skipping it
caused a documented, costly mistake.**

> The governing rule: **a fact in your context is NOT a fact you verified.** Fluency feels identical to
> grounding from the inside (L-80). Therefore every claim below must be PROVEN by an action THIS RUN,
> never asserted from memory, summary, or prior turns.

---

## A. BEFORE planning or offering options (PER STAGE)

- [ ] **A1 — Read the stage's OWN governing ontology this run.** Each stage (research, domain, document,
      interactive-page) has its own TBox+SHACL. Reading one stage's ontology does NOT cover another.
      Having it "in context" does not count — `view`/parse the actual file. *(F100, F20, F72)*
- [ ] **A2 — Ground the options you present in that ontology's choice space**, not your generic sense of
      the artifact. (e.g. for an interactive page: `WPC_Educational` profile, `InstructionalWidget`
      types, `SourceProvenance` tagging — not "study vs reference vs full".) *(F100)*
- [ ] **A2-bis — Self-elicit before drafting (report & interactive-page stages only).** Adopt the relevant expert frame (domain expert/academic writer for reports; designer + UX + interactivity professional for pages); name the likely deficiencies; decide the concrete transforms and structure BEFORE the first draft; state the frame adopted. This is a LEVER that raises the starting floor (see `RDODI_ENRICHMENT_PROMPT_PATTERNS_v1_0_0.md`) — it does NOT certify the result and is NOT self-certification; the conformance gate, design-quality floor, and human review still judge it. *(F106)*
- [ ] **A3 — Read the actual source/inputs** (uploaded files, prior-stage artifact) before composing —
      SHA-verify against any manifest, parse, count. Never trust a summary of a file. *(F81/L-80, BP-D2)*

## B. WHILE producing a stage artifact

- [ ] **B1 — Produce the stage's REQUIRED artifact type.** A stage artifact is an ABox typed against its
      ontology. Free-form markdown/HTML is NOT a conformant stage artifact — it may accompany the ABox,
      but it does not replace it. *(F100)*
- [ ] **B2 — Compose, do not template.** A loop over concepts cannot produce cohesion. *(F84)*
- [ ] **B3 — Verify every external/historical claim before writing it** (web/catalogue). Attribute
      semi-parables carefully. Never embellish or invent. *(F39, F92)*
- [ ] **B4 — Verify every reference points to the actual work**, not a review/precursor of it. "Resolved"
      ≠ "correctly resolved." *(F86)*

## C. AFTER any edit or rewrite

- [ ] **C1 — Confirm the edit actually landed** (keyword/occurrence count). Programmatic edits on
      wrapped text fail silently. *(F92, F94)*
- [ ] **C2 — Run the regression guard.** After any rewrite, confirm citation count, seminal-concept
      checklist, sections, tables, figures did NOT drop without an explicit instruction to cut. *(F90)*
- [ ] **C3 — Re-derive every number you state** from the artifact; never trust a stated count. *(F81/F3)*
- [ ] **C4 — Use exact (normalised) matching for every check.** Fuzzy matching may only PROPOSE
      candidates an exact check confirms. *(this session's fuzzy false +/-)*

## D. BEFORE shipping a stage artifact (THE HARD GATE)

- [ ] **D1 — Run the STAGE-CONFORMANCE GATE.** It asserts, per stage: (a) the governing ontology was read
      this run, (b) the artifact is an ABox typed against it, (c) the stage SHACL ran and conformed.
      No artifact ships from a stage with a NON_CONFORMANT verdict. *(F100 — the instrument that would
      have caught the Stage-4 skip)*
- [ ] **D2 — Run the content verification suite** (insertions/retention/numbers/references). *(F90/F92)*
- [ ] **D3 — Distinguish MECHANICAL pass from JUDGMENT.** The gates guarantee the mechanical floor only.
      Surface the warrant items (does each source support its claim?) and document intent on a validation
      sheet for the human. Never self-certify content truth. *(§1 self-certification limit, F39/F53)*

- [ ] **D4 — New lessons recorded? (release-completeness, R13).** If lessons emerged this session, they are written to the governed store BEFORE the release is called complete. A negative answer blocks the release-COMPLETE claim (not the artifact's correctness). Targets the capture process, not within-artifact validity. *(R13 — adopted 2026-06-04 from OE proposal item R)*

## E. ALWAYS

- [ ] **E1 — Versions increment on every rebuild.** Never reuse a version for a changed file.
- [ ] **E2 — Additive change = MINOR bump, breaking = MAJOR; no silent removals.** *(BP-D7)*
- [ ] **E3 — Light theme for any HTML/dashboard.**
- [ ] **E4 — Report at TRUE magnitude.** If a check reports a regression, verify the CHECK before
      trusting it — but never soften a real gap. Honest deflation over optimistic claim. *(F85, F96)*
- [ ] **E5 — If you cannot prove it this run, say "not verified" — do not assert it.** *(L-80, L-81)*

---

## Machine-readable enforcement
`rdodi_alert_manifest_v1_0_0.json` encodes A–E for programmatic preflight. Any LLM driving the pipeline
should load it and refuse to mark a stage done until its checklist items return proven-true.
