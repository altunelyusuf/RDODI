#!/usr/bin/env python3
"""RDODI Bootstrap v1.0.0 (C2) — one command: pick a genre, point at a source ontology.

Chain: detect -> generate (document + page) -> validate -> assess -> emit an HONEST consolidated report.

Discipline (this session's lesson, enforced here): the report SURFACES every gate verdict, including the
tier-C caveats and the assessor's REJECT/ADVISORY reasons. It NEVER collapses to a green "DONE". The overall
status distinguishes "structurally generated + validated" from "substance/provenance proven" — the latter is
never claimed, because the gates cannot certify it.

Usage: python3 rdodi_bootstrap_v1_0_0.py <domain.ttl> <ProfileLocalName> <profiles.ttl> <out_dir> \
         <doc_tbox> <doc_shacl> <page_tbox> <page_shacl>
"""
import sys, os, json, importlib.util

def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def run(domain, profile, profiles, outdir, doc_tbox, doc_shacl, page_tbox, page_shacl, mods):
    GEN, VAL, ASR = mods["gen"], mods["val"], mods["asr"]
    os.makedirs(outdir, exist_ok=True)
    report = {"input": {"domain": domain, "profile": profile}, "verdicts": [], "human_judgment_required": []}

    # 1) GENERATE
    doc_path = GEN.generate(domain, profiles, profile, outdir)
    page_path = GEN.generate_page(domain, profiles, profile, doc_path, outdir)
    report["generated"] = {"document": doc_path, "page": page_path}

    # 2) VALIDATE (structural + source-validity) — collect EVERY verdict
    def rec(gr):
        d = {"gate": gr.gate_id, "verdict": gr.verdict, "detail": gr.detail}
        report["verdicts"].append(d)
        # surface tier-C / caveats / failures for human
        if gr.verdict == "FAIL":
            report["human_judgment_required"].append(f"{gr.gate_id} FAILED: {gr.detail}")
        if "not caught" in str(gr.detail) or "tier-C" in str(gr.detail):
            report["human_judgment_required"].append(f"{gr.gate_id} caveat (gate cannot certify): {gr.detail}")
        return gr
    rec(VAL.gate_parse("Stage3.A", doc_path))
    rec(VAL.gate_shacl("Stage3.B", [doc_path, doc_tbox], doc_shacl))
    rec(VAL.gate_coverage_rule("Stage3.E.cov", doc_path, doc_tbox, doc_shacl, "document-ontology#"))
    rec(VAL.gate_substance_rule("Stage3.E.sub", doc_path, doc_tbox, doc_shacl, "document-ontology#"))
    rec(VAL.gate_source_validity("Stage3.src", doc_path))
    rec(VAL.gate_parse("Stage4.A", page_path))
    rec(VAL.gate_shacl("Stage4.B", [page_path, page_tbox], page_shacl))
    rec(VAL.gate_coverage_rule("Stage4.cov", page_path, page_tbox, page_shacl, "interactive-page-ontology#"))
    rec(VAL.gate_substance_rule("Stage4.sub", page_path, page_tbox, page_shacl, "interactive-page-ontology#"))
    rec(VAL.gate_source_validity("Stage4.src", page_path))

    # 3) ASSESS the domain ontology (C1)
    overall_asr, gates_asr, _ = ASR.assess(domain, None, _quiet=True)
    report["assessor"] = {"overall": overall_asr,
                          "gates": [{"gate": g["gate"], "verdict": g["verdict"], "detail": g["detail"],
                                     "recommend": g.get("recommend", [])} for g in gates_asr]}
    for g in gates_asr:
        if g["verdict"] in ("FAIL", "ADVISORY"):
            for r in g.get("recommend", []):
                report["human_judgment_required"].append(f"assessor[{g['gate'][:24]}]: {r}")

    # 4) HONEST overall status
    struct_fail = any(v["verdict"] == "FAIL" for v in report["verdicts"])
    report["status"] = ("STRUCTURAL_FAIL — generated artifacts do not pass the structural gates"
                        if struct_fail else
                        "GENERATED + STRUCTURALLY VALIDATED — substance/provenance NOT proven (see human_judgment_required)")
    report["honest_note"] = ("Gates certify structure + real-sourcing, NOT substance. The assessor certifies "
                             "ontology quality, NOT prose substance. Items under human_judgment_required are "
                             "tier-C and must be reviewed by a person; they are not auto-passed.")
    out = os.path.join(outdir, "bootstrap_report.json")
    json.dump(report, open(out, "w"), indent=2)
    return report, out

if __name__ == "__main__":
    if len(sys.argv) < 9:
        print(__doc__); raise SystemExit(2)
    a = sys.argv
    base = os.path.dirname(os.path.abspath(__file__))
    mods = {
        "gen": _load(a.pop(0) if False else os.environ["GEN"], "gen"),
    } if False else None
    # modules located via env (set by the runner)
    mods = {"gen": _load(os.environ["GEN"], "gen"),
            "val": _load(os.environ["VAL"], "val"),
            "asr": _load(os.environ["ASR"], "asr")}
    rep, out = run(a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], mods)
    print(f"STATUS: {rep['status']}")
    print(f"verdicts: {len(rep['verdicts'])} gates | human-judgment items: {len(rep['human_judgment_required'])}")
    for h in rep["human_judgment_required"]:
        print(f"  ⚠ {h}")
    print(f"report: {out}")
