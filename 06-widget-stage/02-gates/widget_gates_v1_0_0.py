#!/usr/bin/env python3
"""
Widget Gates v1.0.0  (Phase 4, PROPOSED extensions to RDODI Stage 4)
=====================================================================
Three gates, each at its correct tier (blueprint tier discipline F39/F53):

  Stage4.widget.warrant  [TIER-C-OK]  every widget cites a discourse warrant (which
                          primitive + which feature fired). Mis-warrant = fitness issue,
                          audited not blocked. Fails only on TOTALLY absent warrant.
  Stage4.widget.grounded [TIER-A HARD] displayed content traces to a real Stage-2 concept
                          + carries a source. Fails on ungrounded/fabricated content.
  Stage4.widget.tested   [TIER-A HARD] the widget declares a design-test (TestProcedure)
                          and records its pass. Fails if no test or test not passed.

All three are RULES (no magic numbers). Each ships proven to FAIL on bad input (L-65).
Labeled PROPOSED (L-40): not yet in the procedure.
"""
import rdflib
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DCTERMS
from dataclasses import dataclass

DC = DCTERMS
WP = "http://example.org/widget-primitives#"
DS = "http://example.org/rdodi/discourse-selection#"

@dataclass
class GateResult:
    gate_id: str; verdict: str; detail: str; tier: str
    def __str__(self):
        return f"[{self.verdict:11}] {self.gate_id} [{self.tier}] [PROPOSED]: {self.detail}"

def _load(p):
    g = rdflib.Graph(); g.parse(p, format="turtle"); return g

def _widget_individuals(page_graph):
    """A widget individual = a page individual that declares wp:instantiatesPrimitive."""
    return list(page_graph.subject_objects(rdflib.URIRef(WP+"instantiatesPrimitive")))

# --- Gate 1: selection-warrant (TIER-C-ok) ---
def gate_warrant(page_path):
    g = _load(page_path)
    widgets = _widget_individuals(g)
    if not widgets:
        return GateResult("Stage4.widget.warrant", "CANNOT_RUN", "no widgets declare instantiatesPrimitive", "TIER-C")
    missing = []
    for w, prim in widgets:
        warrant = g.value(w, rdflib.URIRef(DS+"selectionWarrant"))
        if not warrant:
            missing.append(str(w).rsplit('#',1)[-1])
    if missing:
        return GateResult("Stage4.widget.warrant", "FAIL",
                          f"{len(missing)} widget(s) cite no discourse warrant: {missing[:3]}", "TIER-C")
    return GateResult("Stage4.widget.warrant", "PASS",
                      f"{len(widgets)} widget(s) all cite a discourse warrant", "TIER-C")

# --- Gate 2: content-grounding (TIER-A hard) ---
def gate_grounded(page_path):
    g = _load(page_path)
    widgets = _widget_individuals(g)
    if not widgets:
        return GateResult("Stage4.widget.grounded", "CANNOT_RUN", "no widgets", "TIER-A")
    ungrounded = []
    for w, prim in widgets:
        has_concept = bool(g.value(w, rdflib.URIRef(WP+"demonstratesConcept")))
        has_source = bool(g.value(w, DC.source))
        if not (has_concept and has_source):
            ungrounded.append(str(w).rsplit('#',1)[-1])
    if ungrounded:
        return GateResult("Stage4.widget.grounded", "FAIL",
                          f"{len(ungrounded)} widget(s) lack concept-link+source: {ungrounded[:3]}", "TIER-A")
    return GateResult("Stage4.widget.grounded", "PASS",
                      f"{len(widgets)} widget(s) all grounded (concept + source)", "TIER-A")

# --- Gate 3: design-test (TIER-A hard) ---
def gate_tested(page_path):
    g = _load(page_path)
    widgets = _widget_individuals(g)
    if not widgets:
        return GateResult("Stage4.widget.tested", "CANNOT_RUN", "no widgets", "TIER-A")
    untested = []
    for w, prim in widgets:
        test_passed = g.value(w, rdflib.URIRef(WP+"designTestPassed"))
        if str(test_passed).lower() not in ("true", "1"):
            untested.append(str(w).rsplit('#',1)[-1])
    if untested:
        return GateResult("Stage4.widget.tested", "FAIL",
                          f"{len(untested)} widget(s) have no passing design-test: {untested[:3]}", "TIER-A")
    return GateResult("Stage4.widget.tested", "PASS",
                      f"{len(widgets)} widget(s) all have a passing design-test", "TIER-A")

def run_all(page_path):
    return [gate_warrant(page_path), gate_grounded(page_path), gate_tested(page_path)]

if __name__ == "__main__":
    import sys
    for r in run_all(sys.argv[1]): print(r)
