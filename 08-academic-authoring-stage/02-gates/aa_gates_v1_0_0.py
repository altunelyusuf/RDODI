#!/usr/bin/env python3
"""RDODI Academic-Authoring stage gates v1.0.0.

AA.structure       — TIER-A (mechanical): every domain class has an ExtendedTreatment with the
                     required paragraph types for its depth (area: 4 types; concept: 2+).
AA.claim_evidence  — TIER-A (mechanical): every Claim has supportedBy a Citation.
AA.citation_density— TIER-A (mechanical): every treatment carries ≥ N citations.
AA.readability     — TIER-A (proxy):    Flesch-Kincaid within the declared target band.
AA.register        — TIER-B (proxy):    hedging density and first-person density within bounds.
AA.consultation_link — TIER-A (mechanical, profile-gated): when profile is ConsultedOnly, no Claim may
                     be supportedBy a ReconstructedSource.

Honest ceiling restated (L-40): gates enforce disclosure / structure / mechanical thresholds. They
do NOT certify scholarship; that remains the content-correctness attestation (Stage P, v1.6.0).
"""
import os, re, math
from dataclasses import dataclass
import rdflib
from rdflib.namespace import RDF, RDFS, OWL

AA = rdflib.Namespace("http://example.org/rdodi/academic-authoring#")
RRES = rdflib.Namespace("http://example.org/rdodi/research-ontology#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
DC = rdflib.Namespace("http://purl.org/dc/terms/")
DEMO_NS = rdflib.Namespace("http://example.org/demo-pqm#")

@dataclass
class GateResult:
    name: str; status: str; detail: str; tier: str
    def __repr__(self): return f"[{self.status:12}] {self.name} [{self.tier}]: {self.detail}"

def _g(*paths):
    g = rdflib.Graph()
    for p in paths:
        if p and os.path.exists(p): g.parse(p)
    return g

# ---------- AA.structure ----------
def structure_gate(treatments_ttl, domain_tbox_ttl, area_depth=4, concept_depth=2):
    g = _g(treatments_ttl, domain_tbox_ttl)
    # collect domain classes (those defined in the chapter namespace) excluding owl:Thing etc
    domain_classes = {c for c in g.subjects(RDF.type, OWL.Class) if str(c).startswith(str(DEMO_NS))}
    if not domain_classes:
        return GateResult("AA.structure","CANNOT_RUN","no domain classes found in the chapter namespace","TIER-A")
    # is it an "area" (no rdfs:subClassOf) or a "concept" (has one)
    area = {c for c in domain_classes if not list(g.objects(c, RDFS.subClassOf))}
    # treatments
    treats = {}
    for t in g.subjects(RDF.type, AA.ExtendedTreatment):
        c = g.value(t, AA.treats)
        if c: treats[c] = t
    missing = [str(c).split('#')[-1] for c in domain_classes if c not in treats]
    if missing:
        return GateResult("AA.structure","FAIL",f"classes without ExtendedTreatment: {missing[:6]}{'…' if len(missing)>6 else ''}","TIER-A")
    # check paragraph-type coverage per treatment
    REQUIRED_AREA = {AA.AbstractParagraph, AA.BackgroundParagraph, AA.DiscussionParagraph, AA.ImplicationsParagraph}
    REQUIRED_CONCEPT = {AA.BackgroundParagraph, AA.DiscussionParagraph}
    bad = []
    for c, t in treats.items():
        req = REQUIRED_AREA if c in area else REQUIRED_CONCEPT
        paras = list(g.objects(t, AA.hasParagraph))
        types = set()
        for p in paras:
            for ty in g.objects(p, RDF.type):
                if ty in (AA.AbstractParagraph, AA.BackgroundParagraph, AA.DiscussionParagraph, AA.ImplicationsParagraph):
                    types.add(ty)
        miss = req - types
        if miss:
            bad.append(f"{str(c).split('#')[-1]} missing {[str(m).split('#')[-1] for m in miss]}")
    if bad:
        return GateResult("AA.structure","FAIL","; ".join(bad[:5]),"TIER-A")
    return GateResult("AA.structure","PASS",f"{len(treats)} treatments, all paragraph types present (area={len(area)} need 4-type, concept={len(domain_classes)-len(area)} need 2-type)","TIER-A")

# ---------- AA.claim_evidence ----------
def claim_evidence_gate(treatments_ttl, research_ttl=None):
    g = _g(treatments_ttl, research_ttl)
    citations = set(g.subjects(RDF.type, RRES.Citation))
    claims = list(g.subjects(RDF.type, AA.Claim))
    if not claims:
        return GateResult("AA.claim_evidence","FAIL","no Claim individuals declared (genre requires explicit claims with citations)","TIER-A")
    bad = []
    for c in claims:
        sup = list(g.objects(c, AA.supportedBy))
        if not sup: bad.append(f"{str(c).split('#')[-1]}: no supportedBy"); continue
        for cit in sup:
            if cit not in citations:
                bad.append(f"{str(c).split('#')[-1]}: supportedBy {str(cit).split('#')[-1]} which is not a rres:Citation")
    if bad:
        return GateResult("AA.claim_evidence","FAIL","; ".join(bad[:5]),"TIER-A")
    return GateResult("AA.claim_evidence","PASS",f"{len(claims)} claims all supported by a real rres:Citation","TIER-A")

# ---------- AA.citation_density ----------
def citation_density_gate(treatments_ttl, min_per_treatment=2):
    g = _g(treatments_ttl)
    treats = list(g.subjects(RDF.type, AA.ExtendedTreatment))
    if not treats: return GateResult("AA.citation_density","CANNOT_RUN","no treatments","TIER-A")
    under = []
    for t in treats:
        # citations supporting any claim appearing in this treatment's paragraphs
        paras = set(g.objects(t, AA.hasParagraph))
        claim_ids = {c for p in paras for c in g.subjects(AA.appearsIn, p)}
        cits = {cit for c in claim_ids for cit in g.objects(c, AA.supportedBy)}
        if len(cits) < min_per_treatment:
            under.append(f"{str(g.value(t,AA.treats)).split('#')[-1]}: {len(cits)} cites (< {min_per_treatment})")
    if under:
        return GateResult("AA.citation_density","FAIL","; ".join(under[:5]),"TIER-A")
    return GateResult("AA.citation_density","PASS",f"{len(treats)} treatments, all carry ≥{min_per_treatment} citations","TIER-A")

# ---------- AA.readability (Flesch-Kincaid; honest proxy) ----------
def _syllables(word):
    word = word.lower()
    if len(word) <= 3: return 1
    word = re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$', '', word)
    word = re.sub(r'^y', '', word)
    return max(1, len(re.findall(r'[aeiouy]+', word)))

def _fk_grade(text):
    sents = max(1, len(re.findall(r'[.!?]+(?:\s|$)', text)))
    words = re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text)
    if not words: return None
    syls = sum(_syllables(w) for w in words)
    return 0.39*(len(words)/sents) + 11.8*(syls/len(words)) - 15.59

def readability_gate(treatments_ttl, band_low=12.0, band_high=18.0):
    g = _g(treatments_ttl)
    treats = list(g.subjects(RDF.type, AA.ExtendedTreatment))
    if not treats: return GateResult("AA.readability","CANNOT_RUN","no treatments to score","TIER-A")
    out_of_band, scores = [], []
    for t in treats:
        text = "\n".join(str(g.value(p, AA.paragraphText) or "") for p in g.objects(t, AA.hasParagraph))
        grade = _fk_grade(text)
        if grade is None: continue
        scores.append(grade)
        if not (band_low <= grade <= band_high):
            out_of_band.append(f"{str(g.value(t,AA.treats)).split('#')[-1]}: FK={grade:.1f}")
    avg = (sum(scores)/len(scores)) if scores else float("nan")
    if out_of_band:
        return GateResult("AA.readability","FAIL",f"avg FK={avg:.1f} target [{band_low},{band_high}]; out-of-band: {out_of_band[:5]}","TIER-A")
    return GateResult("AA.readability","PASS",f"{len(scores)} treatments, avg FK={avg:.1f} within [{band_low},{band_high}]","TIER-A")

# ---------- AA.register (academic register heuristic; TIER-B proxy) ----------
HEDGES = {"may","might","appears","suggests","tends","approximately","largely","typically","often","generally","arguably","plausibly"}
FIRST_PERSON = {"I","me","my","we","us","our"}
def register_gate(treatments_ttl, min_hedge_per_1000=2, max_firstperson_per_1000=1):
    g = _g(treatments_ttl)
    treats = list(g.subjects(RDF.type, AA.ExtendedTreatment))
    bad = []
    for t in treats:
        text = " ".join(str(g.value(p, AA.paragraphText) or "") for p in g.objects(t, AA.hasParagraph))
        words = re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text)
        if not words: continue
        n=len(words); hedge = sum(1 for w in words if w.lower() in HEDGES)
        fp = sum(1 for w in words if w in FIRST_PERSON)
        hedge_rate = hedge/n*1000; fp_rate = fp/n*1000
        if hedge_rate < min_hedge_per_1000 or fp_rate > max_firstperson_per_1000:
            bad.append(f"{str(g.value(t,AA.treats)).split('#')[-1]}: hedge={hedge_rate:.1f}/k fp={fp_rate:.1f}/k")
    if bad:
        return GateResult("AA.register","FAIL","; ".join(bad[:5]),"TIER-B")
    return GateResult("AA.register","PASS",f"{len(treats)} treatments meet hedge≥{min_hedge_per_1000}/k and first-person≤{max_firstperson_per_1000}/k","TIER-B")

# ---------- AA.consultation_link (ConsultedOnly profile only) ----------
def consultation_link_gate(treatments_ttl, research_ttl=None):
    g = _g(treatments_ttl, research_ttl)
    reconstructed = set(g.subjects(RDF.type, AA.ReconstructedSource))
    # also accept ones flagged via rres:hasContext "...reconstruction=True..."
    for cit in g.subjects(RDF.type, RRES.Citation):
        for ctx in g.objects(cit, RRES.hasContext):
            if "reconstruction=True" in str(ctx): reconstructed.add(cit)
    bad = []
    for c in g.subjects(RDF.type, AA.Claim):
        for cit in g.objects(c, AA.supportedBy):
            if cit in reconstructed:
                bad.append(f"{str(c).split('#')[-1]} -> {str(cit).split('#')[-1]} (reconstructed)")
    if bad:
        return GateResult("AA.consultation_link","FAIL",f"{len(bad)} claims supported by ReconstructedSource (ConsultedOnly profile refuses): {bad[:3]}{'…' if len(bad)>3 else ''}","TIER-A")
    return GateResult("AA.consultation_link","PASS","no claim is supported by a ReconstructedSource","TIER-A")

# ---------- Profile driver ----------
PROFILES = {
 "CompanionAuthoring":  ["structure","claim_evidence","readability"],
 "CoursewareAuthoring": ["structure","claim_evidence","citation_density","readability","register"],
 "ConsultedOnly":       ["structure","claim_evidence","citation_density","readability","register","consultation_link"],
}

def run_profile(profile, treatments_ttl, domain_tbox_ttl, research_ttl=None,
                band_low=12.0, band_high=18.0, min_cit=2):
    spec = PROFILES[profile]; results=[]
    runners = {
      "structure": lambda: structure_gate(treatments_ttl, domain_tbox_ttl),
      "claim_evidence": lambda: claim_evidence_gate(treatments_ttl, research_ttl),
      "citation_density": lambda: citation_density_gate(treatments_ttl, min_cit),
      "readability": lambda: readability_gate(treatments_ttl, band_low, band_high),
      "register": lambda: register_gate(treatments_ttl),
      "consultation_link": lambda: consultation_link_gate(treatments_ttl, research_ttl),
    }
    for k in spec: results.append(runners[k]())
    blocking = [r for r in results if r.status == "FAIL"]
    verdict = ("CERTIFIED @ " if not blocking else "REFUSED @ ") + profile
    return verdict, results

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True)
    ap.add_argument("--treatments", required=True)
    ap.add_argument("--domain-tbox", required=True)
    ap.add_argument("--research")
    ap.add_argument("--band-low", type=float, default=12.0)
    ap.add_argument("--band-high", type=float, default=18.0)
    ap.add_argument("--min-cit", type=int, default=2)
    a = ap.parse_args()
    v, rs = run_profile(a.profile, a.treatments, a.domain_tbox, a.research, a.band_low, a.band_high, a.min_cit)
    print(f"=== AA acceptance @ {a.profile} ===")
    for r in rs: print(" ", r)
    print(f"VERDICT: {v}")
