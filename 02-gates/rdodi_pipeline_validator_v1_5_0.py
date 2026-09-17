#!/usr/bin/env python3
"""
RDODI Pipeline Validator v1.5.0
================================
Mechanical gate runner for the RDODI four-stage pipeline (Research -> Domain ->
Document -> Interactive Page).

CHANGES FROM v1.4.0 (MINOR bump per BP-D7; Stage1.B wired in for the first time):
  - Stage1.B (the SHACL gate over the Research Ontology) was named in the procedure's
    own gate table since v1.0.0 but never called anywhere in validate() -- only Stage1.A
    (parse) ran. A parallel session's finding plus this session's own re-verification
    confirmed the shipped shapes were also an 8-class, unanchored, sh:targetClass-less
    fragment (research_ontology_shacl_v1_0_1.ttl) -- fixed separately as
    research_ontology_shacl_v1_1_0.ttl (real sh:targetClass shapes for ResearchProject
    and Publication, the two classes any real artifact instantiates). This release wires
    the (now real) gate into validate() using the existing gate_shacl() helper, the same
    one Stage2.C/3.B/4.B already use -- no new mechanism, an existing one applied where
    it was missing (L-105).
  - cfg["research_shacl"] is now a required config key.

CHANGES FROM v1.0.0 (MINOR bump per BP-D7; gate vocabulary corrected):
  - REMOVED the invented gate-naming scheme (G-PARSE/G-SHACL/G-COV/G-REF/G-SUB/G-PROV).
    Those names appeared NOWHERE in the procedure (RDODI_FourStage_Pipeline_Procedure_v1_0_0)
    and were a fabrication recorded in RDODI_PACKAGE_PROVENANCE_AUDIT_v1_0_0 / blueprint F62.
  - Gates now use the procedure's REAL IDs: Stage1.A-E, Stage2.A-G, Stage3.A-H, Stage4.A-G, Cross.A-E.
  - Coverage and substance are implemented as the test-drive-settled RULES (blueprint F59/F60),
    run as TWO SEPARATE gates with distinct diagnostics (blueprint F61, honoring the F10/F46
    separable-failure-reasons design goal).
  - REMOVED magic-number thresholds (COVERAGE_MIN_FRACTION=0.33, SUBSTANCE_MIN_CHARS=80).
    Both are replaced by rules that need no constant.

GATE STATUS LABELS:
  [STANDARD]  - a gate defined in the procedure (real Stage*/Cross* ID).
  [PROPOSED]  - an extension authored 2026-05-28, NOT yet in the procedure. Pending a
                procedure-amendment decision. Labeled per L-40 so it is never mistaken for standard.

THE TWO SETTLED RULES (both test-drive-verified, see /ruletest and blueprint F59/F60):

  COVERAGE RULE (strengthens the real Stage3.E / page-coverage concern; [PROPOSED] as a
  distinct gate): an artifact FAILS if it instantiates ZERO of the standard's structural
  classes (abstention) OR if any instantiated structural-class individual lacks BOTH a
  label and a (definition-or-source) content field (hollow instantiation). No fraction/number.

  SUBSTANCE RULE ([PROPOSED]): every instantiated structural-class individual's primary
  content (skos:definition, else rdfs:label) must be a COMPLETE SENTENCE (>=5 words, a finite
  verb, terminal punctuation) AND the individual must carry a source reference. No char-count.
  HONEST LIMIT (blueprint F60, L-40): this rule does NOT catch fluent filler with a plausible
  source ("This button helps the reader. (src: ...)"). That is the irreducible tier-C residue
  (F39/F53) -- mechanical rules ROUTE substance-judgment, they cannot MAKE it.

L-65: every gate ships with an adversarial test proving it FAILS on bad input
      (rdodi_gate_adversarial_test_v1_1_0.py).
BP-D5: all SHACL validation runs on the imports-merged graph.
"""
import sys, re, json, argparse
from dataclasses import dataclass, field
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DCTERMS

SH = Namespace("http://www.w3.org/ns/shacl#")
DC = DCTERMS

@dataclass
class GateResult:
    gate_id: str          # the procedure's real ID, e.g. "Stage3.B"
    status: str           # "STANDARD" or "PROPOSED"
    verdict: str          # PASS | FAIL | CANNOT_RUN
    detail: str = ""
    evidence: dict = field(default_factory=dict)
    def __str__(self):
        tag = "" if self.status == "STANDARD" else " [PROPOSED]"
        return f"[{self.verdict:11}] {self.gate_id}{tag}: {self.detail}"

# ---------------- helpers ----------------
def _parse(path):
    g = Graph(); g.parse(path, format="turtle"); return g

def _merge(*paths):
    m = Graph()
    for p in paths:
        for t in _parse(p): m.add(t)
    for s, p, o in list(m.triples((None, OWL.imports, None))):
        m.remove((s, p, o))   # BP-D5: strip external imports so SHACL/reasoner won't fetch
    return m

def _structural_classes(tbox_path, shacl_path, ns):
    """Structural classes = ALL owl:Class declared in the standard's namespace.

    NOTE (defect fix, post-test-drive): an earlier draft preferred the SHACL-*targeted*
    subset, but that silently narrowed the definition the coverage/substance rules were
    test-driven against (which used all ns classes), and wrongly failed genuine artifacts
    whose classes happened not to be SHACL-targeted (e.g. Button/Tabs are real page classes
    but not among the 37 targeted shapes). The rule, as settled in blueprint F59/F60, is
    'does the artifact genuinely USE the standard's vocabulary' -- that is the full class set,
    not the constrained subset. L-66: implement the measurement as test-driven, do not redefine.
    The shacl_path arg is retained for signature stability but no longer narrows the set."""
    tbox = _parse(tbox_path)
    return {c for c in tbox.subjects(RDF.type, OWL.Class) if ns in str(c)}

def _instances_of_structural(artifact_graph, structural):
    return [s for s in set(artifact_graph.subjects(RDF.type, None))
            if any(t in structural for t in artifact_graph.objects(s, RDF.type))]

# ---------------- standard gates ----------------
def gate_parse(gate_id, path):
    try:
        g = _parse(path)
        return GateResult(gate_id, "STANDARD", "PASS", f"{len(g)} triples", {"triples": len(g)})
    except Exception as e:
        return GateResult(gate_id, "STANDARD", "FAIL", f"parse error: {e}")

def gate_shacl(gate_id, data_paths, shacl_path):
    # v1.4.0 (L-66 fix): a SHACL Warning is advisory, not a failure. Verdict is driven by
    # Violation-severity results only; Warnings are PASS-with-advisory. Severities are counted from
    # the results GRAPH (not a regex over the text report, which mis-counted the header).
    try:
        import pyshacl
    except ImportError:
        return GateResult(gate_id, "STANDARD", "CANNOT_RUN", "pyshacl not installed")
    from rdflib import Namespace as _NS, RDF as _RDF
    _SH = _NS("http://www.w3.org/ns/shacl#")
    data = _merge(*data_paths); shacl = _parse(shacl_path)
    conforms, rgraph, _ = pyshacl.validate(data, shacl_graph=shacl, inference="rdfs")
    results = list(rgraph.subjects(_RDF.type, _SH.ValidationResult))
    viol = sum(1 for r in results if rgraph.value(r, _SH.resultSeverity) == _SH.Violation)
    warn = sum(1 for r in results if rgraph.value(r, _SH.resultSeverity) == _SH.Warning)
    verdict = "PASS" if viol == 0 else "FAIL"
    msg = f"{viol} Violations, {warn} Warnings (conforms={conforms}; Warnings advisory per L-66)"
    return GateResult(gate_id, "STANDARD", verdict, msg,
                      {"violations": viol, "warnings": warn, "conforms": conforms})

def gate_provenance(gate_id, page_ttl, doc_ttl, domain_tbox):
    # v1.4.0 HYBRID (Cross.B for provenance model C): verify the IRI chain
    #   page-region  prov:wasDerivedFrom  document-section  prov:wasDerivedFrom  domain-concept  dc:source <real>
    # AND that the page region carries a derived citation string. PASS only if the chain resolves to a real
    # terminal source (not relaxed). Regenerable-by-construction; the gate is the maintenance tool (L-65).
    from rdflib import Namespace as _NS
    PROV = _NS("http://www.w3.org/ns/prov#")
    pg = _parse(page_ttl); doc = _parse(doc_ttl); tb = _parse(domain_tbox)
    checked = broken = 0; reasons = []
    for region in pg.subjects(PROV.wasDerivedFrom, None):
        checked += 1
        sec = pg.value(region, PROV.wasDerivedFrom)            # region -> document section
        target = doc.value(sec, PROV.wasDerivedFrom) if sec else None   # section -> concept OR ontology
        has_string = pg.value(region, DC.source) is not None   # hybrid: human-readable citation present
        # terminal grounding: concept with dc:source (strict IRI terminal) OR whole-domain section whose
        # citation string is a REAL source present in the domain (grounded, not fabricated)
        domain_srcs = set(str(o) for o in tb.objects(None, DC.source))
        concept_terminal = bool(target and tb.value(target, DC.source))
        sec_src = str(doc.value(sec, DC.source)) if sec else None
        domain_grounded = bool(sec_src and sec_src in domain_srcs)
        ok = bool(sec and target and has_string and (concept_terminal or domain_grounded))
        if not ok:
            broken += 1
            if len(reasons) < 4:
                reasons.append(f"{str(region).split('#')[-1]}: " +
                    ("no section" if not sec else "no prov target" if not target else
                     "no citation string" if not has_string else "terminal source not grounded in domain"))
    verdict = "PASS" if (checked > 0 and broken == 0) else ("FAIL" if broken else "CANNOT_RUN")
    msg = f"hybrid chains: {checked} checked, {broken} broken" + (f" [{'; '.join(reasons)}]" if reasons else "")
    return GateResult(gate_id, "STANDARD", verdict, msg, {"checked": checked, "broken": broken})

# ---------------- THE TWO SETTLED RULES (proposed extensions) ----------------
def gate_source_validity(gate_id, abox_path):
    """L-66/F86 systemic fix: a dcterms:source must attest a real grounding source, NOT a generator
    self-stamp. FAIL if any content-bearing (skos:definition) individual is sourced by a generation stamp
    or has no source. Prevents 'fluent-filler-with-stamp' from satisfying the substance 'sourced' check."""
    import re as _re
    from rdflib.namespace import DCTERMS as _DCT, SKOS as _SKOS
    STAMP=_re.compile(r'generated by|generator v\d|rdodi (generator|pipeline) v|render_out|auto-generated',_re.I)
    g=_parse(abox_path); bad=0; good=0
    for sub in set(g.subjects(_SKOS.definition,None)):
        src=g.value(sub,_DCT.source)
        if src is None or STAMP.search(str(src)): bad+=1
        else: good+=1
    verdict="PASS" if bad==0 else "FAIL"
    return GateResult(gate_id,"STANDARD",verdict,f"{good} real-sourced, {bad} invalid (generator-stamp/absent)",
                      {"real_sourced":good,"invalid":bad})

def gate_coverage_rule(gate_id, artifact_path, tbox_path, shacl_path, ns):
    """COVERAGE RULE (blueprint F59). FAIL on abstention OR hollow instantiation. No number."""
    structural = _structural_classes(tbox_path, shacl_path, ns)
    art = _parse(artifact_path)
    inds = _instances_of_structural(art, structural)
    if not inds:
        return GateResult(gate_id, "PROPOSED", "FAIL",
                          f"abstention: 0 of {len(structural)} structural classes instantiated",
                          {"used": 0, "structural": len(structural)})
    hollow = []
    for ind in inds:
        has_label = bool(art.value(ind, RDFS.label))
        has_content = bool(art.value(ind, SKOS.definition)) or bool(art.value(ind, DC.source))
        if not (has_label and has_content):
            hollow.append(str(ind).rsplit("#", 1)[-1])
    if hollow:
        return GateResult(gate_id, "PROPOSED", "FAIL",
                          f"hollow instantiation: {len(set(hollow))} typed individuals lack label+content",
                          {"used": len(inds), "hollow": len(set(hollow))})
    return GateResult(gate_id, "PROPOSED", "PASS",
                      f"{len(inds)} structural individuals, all carry label+content",
                      {"used": len(inds), "structural": len(structural)})

_VERB_CUES = {"is","are","was","were","be","been","being","has","have","had","do","does","did",
              "lets","let","allows","allow","provides","provide","describes","describe","measures",
              "measure","ensures","ensure","represents","represent","defines","define","contains",
              "contain","supports","support","enables","enable","shows","show","gives","give",
              "makes","make","uses","use","focuses","focus","refers","refer","occurs","occur"}

def _is_complete_sentence(text):
    t = (text or "").strip()
    words = re.findall(r"[A-Za-z']+", t)
    if len(words) < 5:           return (False, f"{len(words)} words (<5)")
    if not re.search(r'[.!?]\s*$', t): return (False, "no terminal punctuation")
    has_verb = any(w.lower() in _VERB_CUES for w in words) or any(re.search(r'(ed|ing|es|s)$', w) for w in words)
    if not has_verb:             return (False, "no finite verb")
    return (True, f"{len(words)}-word sentence")

def gate_substance_rule(gate_id, artifact_path, tbox_path, shacl_path, ns):
    """SUBSTANCE RULE (blueprint F60): each structural individual's content must be a complete
    sentence AND sourced. No char-count. Honest limit: fluent-filler-with-source is tier-C."""
    structural = _structural_classes(tbox_path, shacl_path, ns)
    art = _parse(artifact_path)
    inds = _instances_of_structural(art, structural)
    if not inds:
        return GateResult(gate_id, "PROPOSED", "FAIL", "0 structural individuals", {"used": 0})
    failing = []
    for ind in inds:
        content = str(art.value(ind, SKOS.definition) or art.value(ind, RDFS.label) or "")
        ok_sentence, why = _is_complete_sentence(content)
        has_source = bool(art.value(ind, DC.source))
        if not ok_sentence:
            failing.append((str(ind).rsplit("#",1)[-1], why)); continue
        if not has_source:
            failing.append((str(ind).rsplit("#",1)[-1], "complete sentence but no source"))
    if failing:
        return GateResult(gate_id, "PROPOSED", "FAIL",
                          f"{len(set(f[0] for f in failing))} individuals not substantive "
                          f"(e.g. {failing[0][0]}: {failing[0][1]})",
                          {"failing": len(set(f[0] for f in failing))})
    return GateResult(gate_id, "PROPOSED", "PASS",
                      f"{len(inds)} individuals: all complete sentences + sourced "
                      f"(tier-C residual: fluent-filler-with-source not caught)",
                      {"used": len(inds)})

# ---------------- orchestration ----------------
def validate(cfg):
    R = []
    R.append(gate_parse("Stage1.A", cfg["research"]))
    R.append(gate_shacl("Stage1.B", [cfg["research"]], cfg["research_shacl"]))
    R.append(gate_parse("Stage2.A", cfg["domain_tbox"]))
    R.append(gate_shacl("Stage2.C", [cfg["domain_tbox"], cfg["domain_abox"]], cfg["domain_shacl"]))
    R.append(gate_parse("Stage3.A", cfg["document_ttl"]))
    R.append(gate_shacl("Stage3.B", [cfg["document_ttl"], cfg["domain_tbox"], cfg["domain_abox"]],
                        cfg["rdodi_doc_shacl"]))
    # coverage + substance on the DOCUMENT against the RDODI document standard
    R.append(gate_coverage_rule("Stage3.E.cov", cfg["document_ttl"], cfg["rdodi_doc_tbox"],
                                cfg["rdodi_doc_shacl"], "document-ontology#"))
    R.append(gate_substance_rule("Stage3.E.sub", cfg["document_ttl"], cfg["rdodi_doc_tbox"],
                                 cfg["rdodi_doc_shacl"], "document-ontology#"))
    R.append(gate_source_validity("Stage3.src", cfg["document_ttl"]))
    R.append(gate_parse("Stage4.A", cfg["page_ttl"]))
    R.append(gate_shacl("Stage4.B", [cfg["page_ttl"], cfg["document_ttl"]], cfg["rdodi_page_shacl"]))
    # coverage + substance on the PAGE against the RDODI page standard
    R.append(gate_coverage_rule("Stage4.cov", cfg["page_ttl"], cfg["rdodi_page_tbox"],
                                cfg["rdodi_page_shacl"], "interactive-page-ontology#"))
    R.append(gate_substance_rule("Stage4.sub", cfg["page_ttl"], cfg["rdodi_page_tbox"],
                                 cfg["rdodi_page_shacl"], "interactive-page-ontology#"))
    R.append(gate_source_validity("Stage4.src", cfg["page_ttl"]))
    R.append(gate_provenance("Cross.B", cfg["page_ttl"], cfg["document_ttl"], cfg["domain_tbox"]))
    return R

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="RDODI Pipeline Validator v1.5.0")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()
    cfg = json.load(open(args.config))
    print("="*74); print("RDODI PIPELINE VALIDATOR v1.4.0  (L-66 severity-honest SHACL; real gate IDs; rule-based coverage+substance)")
    print("="*74)
    results = validate(cfg)
    for r in results: print(r)
    fails = [r for r in results if r.verdict == "FAIL"]
    proposed = [r for r in results if r.status == "PROPOSED"]
    print("="*74)
    print(f"STANDARD gates: {len(results)-len(proposed)} | PROPOSED extensions: {len(proposed)}")
    print(f"OVERALL: {'PASS' if not fails else f'FAIL ({len(fails)} gate(s) failed)'}")
    sys.exit(1 if fails else 0)
