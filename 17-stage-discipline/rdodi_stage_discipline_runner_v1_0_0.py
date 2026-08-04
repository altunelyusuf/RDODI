#!/usr/bin/env python3
"""RDODI Stage-Discipline Runner v1.0.0 (R2) — discipline-DRIVEN gate execution.

Reads the declarative stage-discipline TTL and runs exactly the gates each stage declares (by dispatching to
the existing validator). This makes the per-stage discipline auditable in RDF rather than hardcoded — but it
runs ONLY gates that are actually implemented (L-66), and is verified to reproduce the hardcoded validator's
verdicts (L-65, no regression).

Usage: python3 rdodi_stage_discipline_runner_v1_0_0.py <stage_discipline.ttl> <validator.py> \
        <document.ttl> <doc_tbox> <doc_shacl> <page.ttl> <page_tbox> <page_shacl> <domain.ttl>
"""
import sys, importlib.util, rdflib
from rdflib import Namespace
SD = Namespace("http://example.org/rdodi/stage-discipline#")

def load(path, name):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

def run(sd_ttl, validator_py, doc, doc_tbox, doc_shacl, page, page_tbox, page_shacl, domain):
    g = rdflib.Graph(); g.parse(sd_ttl, format="turtle")
    V = load(validator_py, "validator")
    def loc(u): return str(u).split("#")[-1]

    # how each declared gate-type is dispatched, per stage (faithful to the validator's signatures)
    DISPATCH = {
        "DocumentStage": {
            "parse":         lambda gid: V.gate_parse(gid, doc),
            "shacl":         lambda gid: V.gate_shacl(gid, [doc, doc_tbox], doc_shacl),
            "coverage":      lambda gid: V.gate_coverage_rule(gid, doc, doc_tbox, doc_shacl, "document-ontology#"),
            "substance":     lambda gid: V.gate_substance_rule(gid, doc, doc_tbox, doc_shacl, "document-ontology#"),
            "sourceValidity":lambda gid: V.gate_source_validity(gid, doc),
        },
        "InteractivePageStage": {
            "parse":         lambda gid: V.gate_parse(gid, page),
            "shacl":         lambda gid: V.gate_shacl(gid, [page, page_tbox], page_shacl),
            "coverage":      lambda gid: V.gate_coverage_rule(gid, page, page_tbox, page_shacl, "interactive-page-ontology#"),
            "substance":     lambda gid: V.gate_substance_rule(gid, page, page_tbox, page_shacl, "interactive-page-ontology#"),
            "sourceValidity":lambda gid: V.gate_source_validity(gid, page),
        },
        "CrossStageProvenance": {
            "provenance":    lambda gid: V.gate_provenance(gid, page, doc, domain),
        },
    }
    results = []
    for stage in g.subjects(rdflib.RDF.type, SD.Stage):
        sname = loc(stage)
        gates = sorted(loc(gt) for gt in g.objects(stage, SD.requiresGate))
        for gt in gates:
            disp = DISPATCH.get(sname, {}).get(gt)
            if not disp:
                results.append((sname, gt, "NOT_DISPATCHED", "declared but no implementation bound")); continue
            gr = disp(f"{sname}.{gt}")
            results.append((sname, gt, gr.verdict, gr.detail))
    return results

if __name__ == "__main__":
    if len(sys.argv) < 10:
        print(__doc__); raise SystemExit(2)
    res = run(*sys.argv[1:10])
    cur = None
    for sname, gt, verdict, detail in res:
        if sname != cur: print(f"\n[{sname}]"); cur = sname
        print(f"  {verdict:12s} {gt:16s} {str(detail)[:70]}")
    fails = [r for r in res if r[2] == "FAIL"]
    nd = [r for r in res if r[2] == "NOT_DISPATCHED"]
    print(f"\nstages: {len(set(r[0] for r in res))} | gates run: {len(res)-len(nd)} | FAIL: {len(fails)} | undispatched: {len(nd)}")
