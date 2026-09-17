#!/usr/bin/env python3
"""RDODI Bootstrap v1.2.0 (C2; R21 default per REX-EP5) — one command: pick a genre, point at a source ontology.

Chain: detect -> generate (document + page) -> validate -> assess -> emit an HONEST consolidated report.

Discipline (this session's lesson, enforced here): the report SURFACES every gate verdict, including the
tier-C caveats and the assessor's REJECT/ADVISORY reasons. It NEVER collapses to a green "DONE". The overall
status distinguishes "structurally generated + validated" from "substance/provenance proven" — the latter is
never claimed, because the gates cannot certify it.

Usage: python3 rdodi_bootstrap_v1_2_0.py <domain.ttl> <ProfileLocalName> <profiles.ttl> <out_dir> \
         <doc_tbox> <doc_shacl> <page_tbox> <page_shacl>
"""
import sys, os, json, importlib.util

def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def _scaffold_gate_suite(outdir):
    """v1.2.0 (REX-EP5): every bootstrapped byproduct starts with the R21 four-program
    gate-chain scaffold from 14-bootstrap/templates/ (Ratified R21), REPLACE_ME markers kept."""
    import shutil as _sh
    tdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    dst = os.path.join(outdir, "03-tooling")
    os.makedirs(os.path.join(dst, "gate_suite"), exist_ok=True)
    pairs = [("release_check_template_v1_0_0.sh", "release_check.sh"),
             ("healthcheck_template_v1_0_0.py", "healthcheck.py"),
             ("fitgap_backlog_template_v1_0_0.ttl", os.path.join("..", "fitgap_backlog_v0_1_0.ttl")),
             (os.path.join("gate_suite_template", "supplementary_gates_template_v1_0_0.py"), os.path.join("gate_suite", "supplementary_gates.py")),
             (os.path.join("gate_suite_template", "validator_config_template_v1_0_0.json"), os.path.join("gate_suite", "validator_config.json"))]
    for s, d in pairs:
        _sh.copy(os.path.join(tdir, s), os.path.join(dst, d))
    with open(os.path.join(dst, "GATES_README.md"), "w") as f:
        f.write("# R21 gate chain (scaffolded by rdodi_bootstrap v1.2.0)\n\n"
                "Fill every REPLACE_ME, then wire release_check.sh into your publish step so a failing\n"
                "run blocks the push. Per the RDODI Exemplar Standard: gates grow with every fixed defect;\n"
                "close the byproduct with healthcheck.py (R16+R17); track in the fitgap backlog and validate\n"
                "it against backlog-roadmap-framework/ CURRENT shapes.\n")
    print(f"  R21 gate-suite scaffold -> {dst} (5 files + README)")

def run(domain, profile, profiles, outdir, doc_tbox, doc_shacl, page_tbox, page_shacl, mods, html_path=None):
    GEN, VAL, ASR = mods["gen"], mods["val"], mods["asr"]
    os.makedirs(outdir, exist_ok=True)
    _scaffold_gate_suite(outdir)
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
        if gr.verdict == "CANNOT_RUN":
            report["human_judgment_required"].append(f"{gr.gate_id} CANNOT_RUN (precondition absent, NOT a pass): {gr.detail}")
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
    # Stage-4 navigation gates (A7) — wired; degrade to CANNOT_RUN honestly if HTML/browser absent
    try:
        import rdodi_stage4_nav_gates_v1_0_0 as NAV
        rec(NAV.gate_affordance_grounding("Stage4.nav.grounding", page_path, html_path))
        rec(NAV.gate_router_functional("Stage4.nav.functional", html_path))
    except Exception as _e:
        report["human_judgment_required"].append(f"Stage4.nav gates unavailable: {_e}")

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
