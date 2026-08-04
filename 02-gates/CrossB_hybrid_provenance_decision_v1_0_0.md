# Cross.B — Hybrid Provenance (Model C) Decision & Implementation v1.0.0
**Decision:** provenance model **C (hybrid)** — IRI lineage chain + human-readable citation.

## Maintenance-cost reductions adopted (so C is affordable)
1. **Generated, never hand-maintained** — the generator emits `prov:wasDerivedFrom` at generation time; repair = regenerate.
2. **Anchored to stable domain IRIs** — concept sections terminate at the domain concept's own IRI (survives reordering).
3. **Citation string DERIVED from the chain** — `dcterms:source` comes from the domain's own source; one source of truth, no string/IRI drift.
4. **Cross.B is the maintenance tool** — run on every generation; dangling links fail fast and are fixed by regeneration.

## Mechanism
- **generator v2.4.0** emits: page region `prov:wasDerivedFrom` document section `prov:wasDerivedFrom` domain concept (concept sections) or domain ontology (meta sections); `dcterms:source` derived from the domain.
- **validator v1.4.0** Cross.B verifies the hybrid chain with a DUAL honest terminal:
  - concept sections → terminal = concept with `dc:source` (strict IRI terminal);
  - meta sections (Abstract/Intro/…) → terminal = domain ontology, grounded by a citation string that PROVABLY exists in the domain's source set (not fabricated).

## Honest verification (L-65 / L-66)
- On generated ch9_domain + CourseCompanion artifacts: **Cross.B PASS — 7 chains checked, 0 broken** — PASS by genuine resolution, not by relaxation.
- **Regression guard:** a prov-less page → **CANNOT_RUN** (0 checked) — the gate does not pass an absent chain.
- **Residual (not hidden):** terminal grounding depends on the domain being sourced. the demo domain ontology carries no `dc:source` (meta sections grounded via the in-domain primary citation); 61/86 concepts are sourced — a concept section deriving from an UNSOURCED concept FAILS Cross.B (same tier-C domain-sourcing gap the fidelity gate reports). The irreducible cost lives at sourcing domain concepts, where human judgment belongs.
