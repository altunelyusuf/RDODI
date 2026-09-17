# Ruling: execution-oracle evidence for ValidationActivity

**Asked by:** `HANDOVER_automate-python-book_to_RDODI_chapter-domain-ontology-gaps_v1_0_0.md`,
ask 4 — is "the claim was confirmed by running the code and comparing against the source's own
printed output" admissible `ValidationActivity` evidence?

**Ruling: yes, admissible — and no new vocabulary was needed to make it so.**

Checked directly before ruling, not assumed: `ValidationActivity`'s own definition
(`domain_ontology_tbox_v1_2_0.ttl`, carried unchanged into v1.3.0) states plainly that this
class deliberately carries **no outcome/evidence-type vocabulary at all** — results attach to
the run via PROV-O, pointing at real pipeline gate outputs (pyshacl reports, gate runs), not as
a closed enumeration of validation *kinds* declared inside this module. That design choice
already answers the question: nothing in `ValidationActivity` restricts what a "real pipeline
gate output" may be. An execution-harness run that extracts a printed example, executes it, and
diffs the result against the source's own printed output *is* exactly such a gate output — the
same shape as a pyshacl report, just for a different, execution-based claim.

**What this means concretely for `automate-python-book`:** attach the execution-oracle
comparison the same way any other gate output attaches — a real, committed, re-runnable script
(matching this ecosystem's own standing discipline that a verification leaving no re-runnable
artifact proves the moment, not the property) whose output is linked to the `ValidationActivity`
individual via `prov:wasGeneratedBy`/`prov:used`, exactly as an existing pyshacl-report
attachment would be. No `rdodi-domain:` property needs adding for this specific ask.

**What this ruling does not do:** it does not create a preference for execution-oracle evidence
over other kinds, and it does not exempt an execution-oracle claim from PROV-O attachment —
the same "a validation whose result is not recorded is not evidence of validity" standard
`ValidationActivity`'s own definition already states applies here as everywhere else.

Ruled 2026-09-15, package owner authority, `rdodi-ecosystem` v1.107.0.
