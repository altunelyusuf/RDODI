#!/usr/bin/env python3
"""RDODI Pedagogy-&-Professional stage gates v1.0.0.
Honesty tiers are explicit. Gates enforce disclosure / structure / automated-test / accountable
attestation — never truth. Composed verdict uses ONLY gate outputs (L-66)."""
import os, hashlib, rdflib
from rdflib.namespace import RDF, RDFS
from dataclasses import dataclass
HERE=os.path.dirname(os.path.abspath(__file__)); LIB=os.path.join(HERE,"..","lib","axe.min.js")
RPG=rdflib.Namespace("http://example.org/rdodi/interactive-page-ontology#")
LD=rdflib.Namespace("http://example.org/rdodi/learning-design#")
MP=rdflib.Namespace("http://example.org/rdodi/model-provenance#")
SC=rdflib.Namespace("http://example.org/rdodi/standards-conformance#")
AT=rdflib.Namespace("http://example.org/rdodi/attestation#")
DC=rdflib.Namespace("http://purl.org/dc/terms/")
NUMERIC_WIDGET_CLASSES={"ParametricCalculator","CoupledVariableDemonstrator"}

@dataclass
class GateResult:
    name:str; status:str; detail:str; tier:str
    def __repr__(self): return f"[{self.status:12}] {self.name} [{self.tier}]: {self.detail}"

def sha256_file(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
def _g(p):
    g=rdflib.Graph(); g.parse(p,format="turtle"); return g

# ---- TIER-A: WCAG via axe-core in the existing Playwright harness ----
def wcag_gate(html_path, level="wcag2aa"):
    if not os.path.exists(LIB):
        return GateResult("PP.wcag","CANNOT_RUN","axe-core not bundled; cannot certify WCAG (will NOT claim AA from a partial check)","TIER-A")
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return GateResult("PP.wcag","CANNOT_RUN","playwright unavailable","TIER-A")
    axe=open(LIB).read()
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page()
        pg.goto("file://"+os.path.abspath(html_path)); pg.wait_for_timeout(300)
        pg.add_script_tag(content=axe)
        res=pg.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['%s']}});return r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length}));}"%level)
        b.close()
    if not res: return GateResult("PP.wcag","PASS",f"axe-core {level}: 0 violations","TIER-A")
    top="; ".join(f"{v['id']}({v['impact']},{v['n']})" for v in res[:4])
    return GateResult("PP.wcag","FAIL",f"axe-core {level}: {len(res)} violation rule(s): {top}","TIER-A")

# ---- TIER-A/B: model-provenance disclosure for numeric widgets ----
def model_provenance_gate(page_ttl, html_path=None):
    g=_g(page_ttl)
    numeric=[]
    for w in g.subjects(RDF.type, RPG.InstructionalWidget):
        classes={str(c).split('#')[-1] for c in g.objects(w,RDF.type)}
        if classes & NUMERIC_WIDGET_CLASSES: numeric.append(w)
    if not numeric: return GateResult("PP.model_provenance","CANNOT_RUN","no numeric widgets declared","TIER-A")
    dom_text=""
    if html_path and os.path.exists(html_path):
        import re; dom_text=re.sub(r'<[^>]+>',' ',open(html_path).read()).lower()
    bad=[]
    for w in numeric:
        wn=str(w).split('#')[-1]; st=g.value(w,MP.numericModelStatus)
        if st is None: bad.append(f"{wn}: no numericModelStatus declared"); continue
        sname=str(st).split('#')[-1]
        if sname=="Illustrative":
            lbl=g.value(w,MP.visibleLabelText)
            if not lbl: bad.append(f"{wn}: Illustrative but no visibleLabelText"); continue
            if dom_text and str(lbl).lower() not in dom_text: bad.append(f"{wn}: illustrative label not rendered in DOM")
        elif sname=="Validated":
            if not g.value(w,MP.hasValidationDerivation): bad.append(f"{wn}: Validated but no hasValidationDerivation")
            if not g.value(w,MP.hasConformanceTest): bad.append(f"{wn}: Validated but no numeric-conformance test")
    if bad: return GateResult("PP.model_provenance","FAIL","; ".join(bad[:4]),"TIER-A")
    return GateResult("PP.model_provenance","PASS",f"{len(numeric)} numeric widget(s) declare status + satisfy disclosure","TIER-A")

# ---- TIER-B: assessment rigor + coverage ----
def assessment_rigor_gate(page_ttl):
    g=_g(page_ttl)
    items=list(g.subjects(RDF.type, LD.AssessmentItem))
    los=set(g.objects(None,RPG.hasLearningObjective))
    if not items: return GateResult("PP.assessment_rigor","FAIL","no ld:AssessmentItem present (self-check questions are not graded assessment)","TIER-B")
    bad=[]
    for it in items:
        n=str(it).split('#')[-1]; opts=list(g.objects(it,LD.hasOption)); keys=list(g.objects(it,LD.hasCorrectOption))
        rats=list(g.objects(it,LD.distractorRationale)); lvl=g.value(it,LD.cognitiveLevel); obj=g.value(it,LD.assessesObjective)
        if len(opts)<3: bad.append(f"{n}: <3 options")
        if len(keys)!=1: bad.append(f"{n}: must have exactly 1 key (has {len(keys)})")
        if len(rats)<max(len(opts)-1,1): bad.append(f"{n}: missing distractor rationales")
        if not lvl: bad.append(f"{n}: no cognitiveLevel")
        if not obj: bad.append(f"{n}: no assessesObjective")
    assessed=set(g.objects(None,LD.assessesObjective))
    uncovered=[str(o).split('#')[-1] for o in los if o not in assessed]
    if uncovered: bad.append(f"objectives with no assessment item: {uncovered}")
    if bad: return GateResult("PP.assessment_rigor","FAIL","; ".join(bad[:5]),"TIER-B")
    return GateResult("PP.assessment_rigor","PASS",f"{len(items)} rigorous item(s); every objective assessed","TIER-B")

# ---- TIER-B: Bloom level declared + level-adequate coverage (extends Stage4.K) ----
def bloom_coverage_gate(page_ttl, ld_tbox):
    g=_g(page_ttl); t=_g(ld_tbox)
    rank={s:int(o) for s,o in t.subject_objects(LD.bloomRank)}
    los=set(g.objects(None,RPG.hasLearningObjective))
    if not los: return GateResult("PP.bloom_coverage","CANNOT_RUN","no learning objectives","TIER-B")
    missing=[str(lo).split('#')[-1] for lo in los if not g.value(lo,LD.bloomLevel)]
    if missing: return GateResult("PP.bloom_coverage","FAIL",f"objectives without bloomLevel: {missing}","TIER-B")
    under=[]
    for lo in los:
        need=rank.get(g.value(lo,LD.bloomLevel),99)
        coverers=list(g.subjects(RPG.coversLearningObjective,lo))+list(g.subjects(LD.assessesObjective,lo))
        ok=any(rank.get(g.value(c,LD.cognitiveLevel),0)>=need for c in coverers)
        if not ok: under.append(str(lo).split('#')[-1])
    if under: return GateResult("PP.bloom_coverage","FAIL",f"objectives not covered at their cognitive level: {under}","TIER-B")
    return GateResult("PP.bloom_coverage","PASS",f"{len(los)} objective(s) covered at or above declared Bloom level","TIER-B")

# ---- TIER-A/B: standards over-claim guard ----
def standards_overclaim_gate(manifest_ttl, gate_status:dict, attest_ttl, artifact_hash):
    if not os.path.exists(manifest_ttl):
        return GateResult("PP.overclaim","PASS","no standards-conformance manifest -> no standards claimed","TIER-A")
    g=_g(manifest_ttl); at=_g(attest_ttl) if attest_ttl and os.path.exists(attest_ttl) else rdflib.Graph()
    AUTO={"WCAG_2_2_AA":"wcag","Bloom_Revised":"bloom"}
    fresh_std={str(s).split('#')[-1] for s in at.objects(None,AT.standardReviewedAgainst)
               if str(at.value(_subj_for(at,AT.standardReviewedAgainst,s),AT.artifactHash))==artifact_hash} if len(at) else set()
    # simpler: collect standards with a fresh attestation
    fresh=set()
    for a in at.subjects(RDF.type,AT.ReviewAttestation):
        if str(at.value(a,AT.artifactHash))==artifact_hash:
            for s in at.objects(a,AT.standardReviewedAgainst): fresh.add(str(s).split('#')[-1])
    unmet=[]
    for man in g.subjects(RDF.type,SC.StandardsConformanceManifest):
        for std in g.objects(man,SC.claimsStandard):
            sn=str(std).split('#')[-1]
            if sn in AUTO:
                if gate_status.get(AUTO[sn])!="PASS": unmet.append(f"{sn} claimed but {AUTO[sn]} gate != PASS")
            else:
                if sn not in fresh: unmet.append(f"{sn} claimed but no fresh attestation")
    if unmet: return GateResult("PP.overclaim","FAIL","; ".join(unmet[:5]),"TIER-A")
    return GateResult("PP.overclaim","PASS","every claimed standard has passing automated evidence or a fresh attestation","TIER-A")

def _subj_for(g,p,o):
    for s in g.subjects(p,o): return s
    return None

# ---- TIER-C accountability: hash-bound attestations ----
def attestation_gate(required_scopes, attest_ttl, artifact_hash):
    if not required_scopes: return GateResult("PP.attestation","CANNOT_RUN","profile requires no attestation","TIER-C")
    if not (attest_ttl and os.path.exists(attest_ttl)):
        return GateResult("PP.attestation","FAIL",f"no attestations; required scopes {required_scopes}","TIER-C")
    g=_g(attest_ttl); have={}
    for a in g.subjects(RDF.type,AT.ReviewAttestation):
        fresh=str(g.value(a,AT.artifactHash))==artifact_hash
        have[str(g.value(a,AT.attestationScope))]=fresh
    missing=[s for s in required_scopes if not have.get(s)]
    stale=[s for s in required_scopes if s in have and not have[s]]
    if missing: return GateResult("PP.attestation","FAIL",f"missing/stale attestation scopes: {missing} (stale={stale})","TIER-C")
    return GateResult("PP.attestation","PASS",f"fresh hash-bound attestation present for: {required_scopes}","TIER-C")
