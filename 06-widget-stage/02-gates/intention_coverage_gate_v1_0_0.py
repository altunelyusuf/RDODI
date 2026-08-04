#!/usr/bin/env python3
"""
Intention-Coverage Gate v1.0.0  (Phase: adopted STANDARD)
==========================================================
"Match the intention with the interactivity." Recovers the full intention set from the
ontology and matches each against the widgets. Settled by test-drive as ONE-HOP
(intention is the coverage unit, NOT the subject — two-hop hid uncovered intentions
that share a subject with a covered one; see blueprint F-record).

RULE (no number):
  - An intention (pg:LearningObjective declared via pg:hasLearningObjective) is COVERED
    iff some widget pg:coversLearningObjective it.
  - Uncovered intention  -> DISCLOSED SCOPE (reported, NOT a fail). [user decision (a)]
  - A widget that covers NO declared intention -> FAIL (decoration). [asymmetry]
Reuses existing page-ontology properties; adds NO new vocabulary (L-72).
Honest residual (L-40): whether a widget TRULY covers an intention (the
coversLearningObjective assertion) is tier-C judgment, not mechanically verified here.
"""
import rdflib
from rdflib.namespace import RDF, RDFS
from dataclasses import dataclass, field

PG = rdflib.Namespace("http://example.org/rdodi/interactive-page-ontology#")

@dataclass
class CoverageManifest:
    covered: list = field(default_factory=list)      # (intention, widget)
    disclosed_scope: list = field(default_factory=list)  # intentions with no widget
    decoration_fails: list = field(default_factory=list) # widgets covering no intention
    @property
    def verdict(self):
        # FAIL only on decoration; uncovered intentions are disclosed scope, not a fail
        return "FAIL" if self.decoration_fails else "PASS"

def intention_coverage(graph_path):
    g = rdflib.Graph(); g.parse(graph_path, format="turtle")
    intentions = set(g.objects(None, PG.hasLearningObjective))
    widgets = set(g.subjects(PG.coversLearningObjective, None))
    m = CoverageManifest()
    # coverage per intention (one-hop)
    for i in intentions:
        covering = [w for w in g.subjects(PG.coversLearningObjective, i)]
        if covering:
            for w in covering: m.covered.append((i, w))
        else:
            m.disclosed_scope.append(i)
    # decoration: a widget that covers nothing in the declared intention set
    for w in widgets:
        wcov = set(g.objects(w, PG.coversLearningObjective))
        if not (wcov & intentions):
            m.decoration_fails.append(w)
    return m

def gate(graph_path):
    m = intention_coverage(graph_path)
    n = lambda u: str(u).rsplit('#',1)[-1]
    detail = (f"{len(m.covered)} intention(s) covered; "
              f"{len(m.disclosed_scope)} disclosed-scope (uncovered, reported not failed); "
              f"{len(m.decoration_fails)} decoration widget(s)")
    return m.verdict, detail, m

if __name__ == "__main__":
    import sys
    v, d, m = gate(sys.argv[1])
    n = lambda u: str(u).rsplit('#',1)[-1]
    print(f"[{v}] Stage4.intention-coverage: {d}")
    if m.disclosed_scope:
        print("  DISCLOSED SCOPE (uncovered intentions):", [n(i) for i in m.disclosed_scope])
    if m.decoration_fails:
        print("  DECORATION (widgets covering no intention):", [n(w) for w in m.decoration_fails])
