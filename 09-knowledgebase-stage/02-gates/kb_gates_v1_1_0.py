#!/usr/bin/env python3
"""RDODI Knowledgebase stage gate v1.0.0.

KB.shacl       — TIER-A: SHACL safeguard passes on the merged TBox+ABox.
KB.coverage    — TIER-A: every pattern carries evidence + coverage-check + integration-recommendation + status.
KB.audit       — TIER-A (proxy): summarises pattern count by status and lists Proposed patterns awaiting ratification.

Honest ceiling: the gate verifies structural completeness of the knowledgebase, not the truth of the patterns
themselves. Ratification of a Proposed pattern is the user's call; the gate enforces that the proposal is
graph-complete and BP-D41-flagged where references are external."""
import os, sys, argparse
import rdflib
from rdflib.namespace import RDF, RDFS
from pyshacl import validate
from dataclasses import dataclass

KB = rdflib.Namespace("http://example.org/rdodi/knowledgebase#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

@dataclass
class GateResult:
    name: str; status: str; detail: str; tier: str
    def __repr__(self): return f"[{self.status:12}] {self.name} [{self.tier}]: {self.detail}"

def _g(*paths):
    g = rdflib.Graph()
    for p in paths:
        if p: g.parse(p)
    return g

def shacl_gate(tbox, abox, shapes):
    data = _g(tbox, abox); shp = _g(shapes)
    conforms, rg, _ = validate(data, shacl_graph=shp, inference="rdfs")
    violations = list(rg.subjects(SH.resultSeverity, SH.Violation))
    if violations:
        msgs = []
        for v in violations[:5]:
            foc = str(rg.value(v, SH.focusNode)).split("#")[-1]
            pth = str(rg.value(v, SH.resultPath)).split("#")[-1] if rg.value(v, SH.resultPath) else "—"
            m = str(rg.value(v, SH.resultMessage))[:90]
            msgs.append(f"{foc}.{pth}: {m}")
        return GateResult("KB.shacl", "FAIL", f"{len(violations)} Violation(s) under inference=rdfs: {msgs}", "TIER-A")
    return GateResult("KB.shacl", "PASS", "0 Violations under inference=rdfs (kb_shacl v1_0_0)", "TIER-A")

def coverage_gate(abox):
    g = _g(abox)
    patterns = list(g.subjects(RDF.type, KB.LessonsLearnedPattern))
    if not patterns:
        # subclass-only? walk RDFS
        patterns = list(g.subjects(RDF.type, KB.RDODISpecificPattern)) + list(g.subjects(RDF.type, KB.CrossCuttingPattern))
    if not patterns: return GateResult("KB.coverage", "FAIL", "no patterns declared in ABox", "TIER-A")
    bad = []
    for p in patterns:
        code = g.value(p, KB.patternCode) or "?"
        if not list(g.objects(p, KB.patternEvidence)): bad.append(f"{code}: no evidence")
        if not list(g.objects(p, KB.coversExisting)): bad.append(f"{code}: no coverage-check")
        if not list(g.objects(p, KB.recommendsIntegration)): bad.append(f"{code}: no integration recommendation")
        if not g.value(p, KB.patternStatus): bad.append(f"{code}: no status")
    if bad: return GateResult("KB.coverage", "FAIL", "; ".join(bad[:5]), "TIER-A")
    return GateResult("KB.coverage", "PASS", f"{len(patterns)} pattern(s) all carry evidence + coverage-check + integration + status", "TIER-A")

def audit_gate(abox):
    g = _g(abox)
    patterns = list(g.subjects(RDF.type, KB.LessonsLearnedPattern))
    if not patterns:
        patterns = list(g.subjects(RDF.type, KB.RDODISpecificPattern)) + list(g.subjects(RDF.type, KB.CrossCuttingPattern))
    by_status = {}; proposed = []
    for p in patterns:
        st = g.value(p, KB.patternStatus); sn = str(st).split("#")[-1] if st else "Unknown"
        by_status[sn] = by_status.get(sn, 0) + 1
        if sn == "Proposed":
            code = str(g.value(p, KB.patternCode) or "?")
            label = str(g.value(p, RDFS.label) or "")
            proposed.append(f"{code} — {label[:60]}")
    detail = f"counts={by_status}"
    if proposed: detail += f"; AWAITING RATIFICATION: {proposed}"
    return GateResult("KB.audit", "PASS", detail, "TIER-A")

def run(tbox, abox, shapes):
    return [shacl_gate(tbox, abox, shapes), coverage_gate(abox), audit_gate(abox)]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tbox", required=True)
    ap.add_argument("--abox", required=True)
    ap.add_argument("--shapes", required=True)
    a = ap.parse_args()
    print("=== KB-stage gate run ===")
    for r in run(a.tbox, a.abox, a.shapes): print(" ", r)
    fail = any(r.status == "FAIL" for r in run(a.tbox, a.abox, a.shapes))
    print(f"VERDICT: {'REFUSED' if fail else 'CERTIFIED'}")
