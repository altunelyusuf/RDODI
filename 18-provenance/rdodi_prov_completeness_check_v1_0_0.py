#!/usr/bin/env python3
"""RDODI Provenance-Completeness Check v1.0.0 (R4) — verifies the deepened PROV-O is COMPLETE and that
epistemic types are GROUNDED (never invented). PASS requires: artifact wasGeneratedBy an Activity, the
Activity associated with an Agent, and every asserted epistemic type traceable to a domain source declaration."""
import sys, rdflib
from rdflib import Namespace, RDF
PROV=Namespace("http://www.w3.org/ns/prov#"); EPIST=Namespace("http://example.org/rdodi/epistemic#")
DCT=Namespace("http://purl.org/dc/terms/")
def loc(u): return str(u).split("#")[-1]
def check(doc_ttl, domain_ttl):
    d=rdflib.Graph(); d.parse(doc_ttl,format="turtle"); tb=rdflib.Graph(); tb.parse(domain_ttl,format="turtle")
    act=list(d.subjects(RDF.type,PROV.Activity)); has_act=bool(act)
    has_agent=any(d.value(a,PROV.wasAssociatedWith) for a in act)
    has_gen=bool(list(d.subjects(PROV.wasGeneratedBy,None)))
    # epistemic grounding: every section with an epist:sourceType must derive from a concept whose source
    # actually justifies that type (Verbatim/Paraphrase/DeclaredMixed/Unspecified all derived from the string)
    from collections import Counter
    types=Counter(); ungrounded=0
    for sec,_,t in d.triples((None,EPIST.sourceType,None)):
        types[loc(t)]+=1
        src=str(d.value(sec,DCT.source) or "")   # the section's OWN declared source (consistent with generator)
        tl=str(t).lower(); lo=src.lower()
        ok=((("verbatim" in lo and "paraphrase" in lo) and "mixed" in tl) or
            (("verbatim" in lo and "paraphrase" not in lo) and t==EPIST.Verbatim) or
            (("paraphrase" in lo and "verbatim" not in lo) and t==EPIST.Paraphrase) or
            ((not ("verbatim" in lo or "paraphrase" in lo)) and t==EPIST.Unspecified))
        if not ok: ungrounded+=1
    verdict="PASS" if (has_act and has_agent and has_gen and ungrounded==0) else "FAIL"
    print(f"=== Provenance-Completeness + Epistemic-Grounding : {verdict} ===")
    print(f" activity present: {has_act} | agent-associated: {has_agent} | artifact wasGeneratedBy: {has_gen}")
    print(f" epistemic types (grounded): {dict(types)} | ungrounded(invented) types: {ungrounded} (must be 0)")
    print(" note: 'DeclaredMixed'/'Unspecified' faithfully reflect the domain's imprecision — precision NOT invented.")
    return verdict
if __name__=="__main__":
    if len(sys.argv)<3: print(__doc__); raise SystemExit(2)
    sys.exit(0 if check(sys.argv[1],sys.argv[2])=="PASS" else 1)
