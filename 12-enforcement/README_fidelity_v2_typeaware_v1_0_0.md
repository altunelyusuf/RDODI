# R-E1 — Source-Type-Aware Fidelity Gate v2.0.0
From the STG study: the v1 fidelity gate wrongly rejected normative/governance vocabulary by demanding a
LITERATURE source on every defined entity. v2 distinguishes domain-concept (literature-sourced) from
normative-term (authority-sourced) — WITHOUT a loophole.

## Anti-loophole invariant (proven by running)
No entity passes with zero sourcing. domain-concept needs a real literature dcterms:source; normative-term
needs a valid authority cite (dct:conformsTo / referencesAuthority / prov:wasInformedBy / IRI source).
Declaring something normative does NOT exempt it.

## Demonstration (STG candidate)
- current candidate (governance vocab unsourced) → FAIL (6 unsourced) — not a loophole.
- with genuine authority cites (dct:conformsTo the external OE authority) → PASS (6 normative-terms) — HONEST flip, gate not relaxed.
- injected unsourced normative term → FAIL — invariant holds.
- the demo domain domain regression → domain-concepts still literature-classified; unsourced domain concepts still FAIL.
