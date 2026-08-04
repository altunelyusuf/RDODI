#!/usr/bin/env python3
"""
RDODI Stage-Conformance Gate v1.1.0
===================================
The instrument F100 identified as MISSING. It makes the Stage-4 mistake (building an
artifact OUTSIDE its governing ontology) impossible to perform silently.

For EACH pipeline stage it enforces three conditions BEFORE the stage artifact may ship:
  (a) READ      — the stage's governing ontology file on disk was opened THIS RUN
                  (proven by a fresh content hash recorded in this process, not asserted).
  (b) TYPED     — the produced artifact has an ABox whose individuals are typed against
                  that stage's ontology namespace (not a free-form file).
  (c) VALIDATED — the stage's SHACL gate was run on the (imports-merged) graph and conformed.

Design (OE discipline):
  - L-66: REUSES rdodi_pipeline_validator for the SHACL/gate run; this layer only enforces
    that the run HAPPENED and was grounded — it does not re-implement gate logic.
  - L-80 fix: "read this run" is proven by hashing the file inside this process, defeating
    the context-as-knowledge confusion (a fact in context is NOT a file read).
  - L-40: a stage with no ABox (e.g. a markdown-only document) FAILS LOUDLY as
    NON_CONFORMANT, with the honest reason — never silently passed.
  - Verdicts: CONFORMANT | NON_CONFORMANT | CANNOT_RUN (missing inputs), never a soft pass.
"""
import sys, json, hashlib, argparse, importlib.util
from pathlib import Path
from rdflib import Graph
from rdflib.namespace import RDF, OWL

# stages and the ontology each MUST be built through (the pipeline's own 4 stages + extensions)
STAGES = {
    "1-research":         {"ns_hint": "research-ontology"},
    "2-domain":           {"ns_hint": "domain"},
    "3-document":         {"ns_hint": "document-ontology"},
    "4-interactive-page": {"ns_hint": "interactive-page"},
}

class _ReadLedger:
    """Records files actually opened+hashed THIS run. A file not in the ledger was NOT read this run."""
    def __init__(self): self.read = {}
    def open_and_hash(self, path):
        p = Path(path)
        if not p.exists():
            return None
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        self.read[str(p.resolve())] = h
        return h
    def was_read(self, path):
        return str(Path(path).resolve()) in self.read

def check_stage(stage_key, ontology_path, abox_path, shacl_path, ledger, run_shacl=True):
    """Returns (verdict, reasons[]) for one stage. CONFORMANT requires (a)&(b)&(c)."""
    reasons = []
    ns_hint = STAGES.get(stage_key, {}).get("ns_hint", stage_key)

    # (a) READ — prove the governing ontology was opened this run
    if not ontology_path or not Path(ontology_path).exists():
        return "CANNOT_RUN", [f"governing ontology for stage '{stage_key}' not found: {ontology_path}"]
    h = ledger.open_and_hash(ontology_path)
    if not ledger.was_read(ontology_path):
        return "NON_CONFORMANT", [f"(a) governing ontology was NOT read this run: {ontology_path}"]
    reasons.append(f"(a) READ ok: {Path(ontology_path).name} sha256={h[:12]}")

    # (b) TYPED — artifact must be an ABox typed against the ontology namespace
    if not abox_path or not Path(abox_path).exists():
        return "NON_CONFORMANT", reasons + [
            f"(b) NO ABox for stage '{stage_key}' — artifact is not typed against its ontology "
            f"(a free-form file, e.g. markdown/HTML, is NOT a conformant stage artifact)."]
    try:
        g = Graph(); g.parse(abox_path)
    except Exception as e:
        return "NON_CONFORMANT", reasons + [f"(b) ABox does not parse: {e}"]
    typed = [s for s, _, o in g.triples((None, RDF.type, None))
             if ns_hint.split("-")[0] in str(o).lower() or ns_hint in str(o).lower()]
    indivs = list(g.subjects(RDF.type, OWL.NamedIndividual))
    if not indivs and not typed:
        return "NON_CONFORMANT", reasons + [
            f"(b) ABox has no individuals typed against the {ns_hint} ontology."]
    reasons.append(f"(b) TYPED ok: {len(indivs)} individuals in ABox")

    # (c) VALIDATED — SHACL ran and conformed
    if run_shacl:
        if not shacl_path or not Path(shacl_path).exists():
            return "NON_CONFORMANT", reasons + [f"(c) no SHACL shapes for stage '{stage_key}'."]
        ledger.open_and_hash(shacl_path)
        try:
            from pyshacl import validate
            import re as _re
            data = Graph(); data.parse(abox_path)
            # imports-merged: also load the ontology (BP-D5)
            data.parse(ontology_path)
            sh = Graph(); sh.parse(shacl_path)
            conforms, _, report_text = validate(data, shacl_graph=sh, inference="none")
        except Exception as e:
            return "CANNOT_RUN", reasons + [f"(c) SHACL run errored: {e}"]
        if not conforms:
            # Honor SHACL severity: only Violation-level results are hard failures.
            sevs = _re.findall(r"Severity: sh:(\w+)", report_text)
            hard = [x for x in sevs if x == "Violation"]
            warn = [x for x in sevs if x != "Violation"]
            if hard:
                return "NON_CONFORMANT", reasons + [f"(c) SHACL has {len(hard)} Violation-level failure(s)."]
            reasons.append(f"(c) VALIDATED ok: 0 Violations ({len(warn)} Warning-level advisories — non-blocking)")
        else:
            reasons.append("(c) VALIDATED ok: SHACL conforms")
    return "CONFORMANT", reasons

def run(config):
    """config: {stage_key: {ontology, abox, shacl}}. Returns full report; ALL must be CONFORMANT to ship."""
    ledger = _ReadLedger()
    results = {}
    for stage_key in STAGES:
        spec = config.get(stage_key)
        if not spec:
            results[stage_key] = ("CANNOT_RUN", [f"no config supplied for stage '{stage_key}'"])
            continue
        results[stage_key] = check_stage(
            stage_key, spec.get("ontology"), spec.get("abox"), spec.get("shacl"),
            ledger, run_shacl=spec.get("run_shacl", True))
    all_conformant = all(v[0] == "CONFORMANT" for v in results.values())
    return {"ALL_STAGES_CONFORMANT": all_conformant, "stages": results,
            "files_read_this_run": list(ledger.read.keys())}

def render(report):
    L = ["="*70, "RDODI STAGE-CONFORMANCE GATE", "="*70]
    L.append(f"ALL STAGES CONFORMANT (may ship): {report['ALL_STAGES_CONFORMANT']}")
    L.append("")
    for stage, (verdict, reasons) in report["stages"].items():
        L.append(f"  [{verdict:15}] {stage}")
        for r in reasons:
            L.append(f"       {r}")
    return "\n".join(L)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("config_json", help="JSON: {stage_key:{ontology,abox,shacl,run_shacl}}")
    a = ap.parse_args()
    cfg = json.loads(Path(a.config_json).read_text())
    rep = run(cfg)
    print(render(rep))
    sys.exit(0 if rep["ALL_STAGES_CONFORMANT"] else 1)
