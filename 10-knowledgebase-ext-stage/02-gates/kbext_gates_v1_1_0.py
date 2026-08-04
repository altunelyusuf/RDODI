#!/usr/bin/env python3
"""RDODI KB-EXT stage gates v1.0.1.

PATCH bump — adds KBX.catalogue_resolution_audit. The prior four gates are preserved verbatim.

KBX.shacl                       — TIER-A: SHACL conformance on merged TBox+ABox.
KBX.consultation_audit          — TIER-A (honesty discipline): consultation status per stage.
KBX.stage_coverage              — TIER-A (proxy): every stage ≥N items of ≥M kinds.
KBX.cross_stage_balance         — TIER-A (proxy): no stage exceeds X% of stage-applications.
KBX.catalogue_resolution_audit  — TIER-A (PATCH v1.0.1): reports per-stage CatalogueVerified count,
                                   total catalogues, total resolution records; FAILS only on dangling
                                   CatalogueRecord (a record whose resolvedIn target is not a declared
                                   BibliographicCatalogue) or a CatalogueVerified item without any
                                   catalogueResolution.
"""
import os, sys, argparse
import rdflib
from rdflib.namespace import RDF, RDFS
from pyshacl import validate
from collections import Counter, defaultdict
from dataclasses import dataclass

KBX = rdflib.Namespace("http://example.org/rdodi/knowledgebase-ext#")
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

@dataclass
class GateResult:
    name: str; status: str; detail: str; tier: str
    def __repr__(self): return f"[{self.status:12}] {self.name} [{self.tier}]: {self.detail}"

def _g(*paths):
    g = rdflib.Graph()
    for p in paths:
        if p and os.path.exists(p): g.parse(p)
    return g

def _items(g):
    return list(g.subjects(RDF.type, KBX.Standard)) + list(g.subjects(RDF.type, KBX.Methodology)) + \
           list(g.subjects(RDF.type, KBX.Tool)) + list(g.subjects(RDF.type, KBX.BestPractice)) + \
           list(g.subjects(RDF.type, KBX.EmpiricalStudy))

def shacl_gate(tbox, abox_paths, shapes):
    data = rdflib.Graph(); data.parse(tbox)
    for p in abox_paths: data.parse(p)
    shp = _g(shapes)
    conforms, rg, _ = validate(data, shacl_graph=shp, inference="rdfs", advanced=True)
    violations = list(rg.subjects(SH.resultSeverity, SH.Violation))
    warnings = list(rg.subjects(SH.resultSeverity, SH.Warning))
    if violations:
        msgs = []
        for v in violations[:5]:
            foc = str(rg.value(v, SH.focusNode)).split("#")[-1] if rg.value(v, SH.focusNode) else "?"
            pth_val = rg.value(v, SH.resultPath)
            pth = str(pth_val).split("#")[-1] if pth_val else "—"
            m = str(rg.value(v, SH.resultMessage))[:100]
            msgs.append(f"{foc}.{pth}: {m}")
        return GateResult("KBX.shacl", "FAIL", f"{len(violations)} Violation(s), {len(warnings)} Warning(s): {msgs}", "TIER-A")
    return GateResult("KBX.shacl", "PASS", f"0 Violations (kbx_shacl v1_0_1, inference=rdfs, advanced=True); {len(warnings)} Warning(s) recorded as advisory", "TIER-A")

def consultation_audit_gate(abox_paths):
    g = rdflib.Graph()
    for p in abox_paths: g.parse(p)
    items = _items(g)
    if not items: return GateResult("KBX.consultation_audit", "CANNOT_RUN", "no items", "TIER-A")
    per_stage = defaultdict(Counter); total = Counter(); uncategorised = []
    for it in items:
        statuses = [str(s).split("#")[-1] for s in g.objects(it, KBX.consultationStatus)]
        if not statuses: uncategorised.append(str(it).split("#")[-1]); continue
        # Count the strongest tier the item carries (Consulted > CatalogueVerified > Reconstructed > RequiresConsultation)
        order = ["Consulted", "CatalogueVerified", "Reconstructed", "RequiresConsultation"]
        strongest = next((s for s in order if s in statuses), statuses[0])
        total[strongest] += 1
        for s in g.objects(it, KBX.appliesToStage):
            per_stage[str(s).split("#")[-1]][strongest] += 1
    if uncategorised:
        return GateResult("KBX.consultation_audit", "FAIL", f"items missing consultationStatus: {uncategorised[:5]}", "TIER-A")
    breakdown = "; ".join(f"{stg}: {dict(per_stage[stg])}" for stg in sorted(per_stage.keys()))
    return GateResult("KBX.consultation_audit", "PASS",
                      f"strongest-tier totals={dict(total)}; per-stage {{ {breakdown} }}", "TIER-A")

def stage_coverage_gate(abox_paths, min_items=5, min_kinds=2):
    g = rdflib.Graph()
    for p in abox_paths: g.parse(p)
    stages = ["Stage1Research","Stage2DomainOntology","Stage3Document","Stage4InteractivePage","CrossStageGovernance"]
    per_items = defaultdict(set); per_kinds = defaultdict(set)
    for it in _items(g):
        kind_val = g.value(it, KBX.knowledgeKind)
        kind = str(kind_val).split("#")[-1] if kind_val else None
        for s in g.objects(it, KBX.appliesToStage):
            sn = str(s).split("#")[-1]
            per_items[sn].add(it)
            if kind: per_kinds[sn].add(kind)
    under_items = [s for s in stages if len(per_items[s]) < min_items]
    under_kinds = [s for s in stages if len(per_kinds[s]) < min_kinds]
    if under_items or under_kinds:
        return GateResult("KBX.stage_coverage", "FAIL", f"under-covered: items {under_items}, kinds {under_kinds}", "TIER-A")
    detail = "; ".join(f"{s}: {len(per_items[s])} items / {len(per_kinds[s])} kinds" for s in stages)
    return GateResult("KBX.stage_coverage", "PASS", f"every stage ≥{min_items} items / ≥{min_kinds} kinds: {detail}", "TIER-A")

def cross_stage_balance_gate(abox_paths, max_share=0.45):
    g = rdflib.Graph()
    for p in abox_paths: g.parse(p)
    counts = Counter()
    for it in _items(g):
        for s in g.objects(it, KBX.appliesToStage):
            counts[str(s).split("#")[-1]] += 1
    if not counts: return GateResult("KBX.cross_stage_balance", "CANNOT_RUN", "no items", "TIER-A")
    total = sum(counts.values())
    over = [(s, round(n/total,2)) for s, n in counts.items() if n/total > max_share]
    if over:
        return GateResult("KBX.cross_stage_balance", "FAIL", f"stages over {int(max_share*100)}%: {over}", "TIER-A")
    detail = "; ".join(f"{s}: {n} ({100*n/total:.0f}%)" for s, n in counts.most_common())
    return GateResult("KBX.cross_stage_balance", "PASS", f"no stage exceeds {int(max_share*100)}% of {total} stage-applications: {detail}", "TIER-A")

def catalogue_resolution_audit_gate(abox_paths):
    g = rdflib.Graph()
    for p in abox_paths: g.parse(p)
    catalogues = set(g.subjects(RDF.type, KBX.BibliographicCatalogue))
    records = list(g.subjects(RDF.type, KBX.CatalogueRecord))
    if not catalogues:
        return GateResult("KBX.catalogue_resolution_audit", "PASS", "no catalogues registered yet (KB-EXT v1.0.0 has no catalogue layer; this gate is a no-op until v1.0.1 is loaded)", "TIER-A")
    # dangling records: resolvedIn target not in catalogues
    dangling = []
    for r in records:
        for tgt in g.objects(r, KBX.resolvedIn):
            if tgt not in catalogues:
                dangling.append(f"{str(r).split('#')[-1]} -> {str(tgt).split('#')[-1]}")
    # CatalogueVerified items without resolution
    cv_items_missing = []
    for it in _items(g):
        if KBX.CatalogueVerified in list(g.objects(it, KBX.consultationStatus)):
            if not list(g.objects(it, KBX.catalogueResolution)):
                cv_items_missing.append(str(it).split("#")[-1])
    if dangling or cv_items_missing:
        return GateResult("KBX.catalogue_resolution_audit", "FAIL",
                          f"dangling CatalogueRecord targets: {dangling[:3]}; CatalogueVerified items without resolution: {cv_items_missing[:3]}", "TIER-A")
    # Per-stage CatalogueVerified count
    per_stage = Counter()
    for it in _items(g):
        if KBX.CatalogueVerified in list(g.objects(it, KBX.consultationStatus)):
            for s in g.objects(it, KBX.appliesToStage):
                per_stage[str(s).split("#")[-1]] += 1
    return GateResult("KBX.catalogue_resolution_audit", "PASS",
                      f"{len(catalogues)} catalogues registered; {len(records)} resolution records; CatalogueVerified per-stage: {dict(per_stage)}", "TIER-A")

def run(tbox, abox_paths, shapes):
    return [
        shacl_gate(tbox, abox_paths, shapes),
        consultation_audit_gate(abox_paths),
        stage_coverage_gate(abox_paths),
        cross_stage_balance_gate(abox_paths),
        catalogue_resolution_audit_gate(abox_paths),
    ]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tbox", required=True)
    ap.add_argument("--abox", required=True, nargs="+")
    ap.add_argument("--shapes", required=True)
    a = ap.parse_args()
    print("=== KB-EXT gate run (v1.0.1) ===")
    rs = run(a.tbox, a.abox, a.shapes)
    for r in rs: print(" ", r)
    fail = any(r.status == "FAIL" for r in rs)
    print(f"VERDICT: {'REFUSED' if fail else 'CERTIFIED'}")
