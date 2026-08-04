#!/usr/bin/env python3
"""Enriched acceptance driver v1.0.0. Selects the gate set mandated by the declared DeliveryProfile,
runs it, and composes a verdict from ONLY the gate outputs (L-66). Blocks over-claiming: an artifact
can be certified only at a profile whose mandatory gates all PASS."""
import os, sys, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pp_gates_v1_0_0 as G

# profile -> mandatory automated gates + required attestation scopes + min independent sources
PROFILES = {
 "Companion":       {"gates":[],                                              "attest":[],                                              "min_sources":1},
 "Courseware":      {"gates":["wcag","model_provenance","assessment_rigor","bloom"], "attest":["pedagogical-soundness"],                "min_sources":1},
 "ResearchGrade":   {"gates":["assessment_rigor"],                            "attest":["content-correctness"],                         "min_sources":3},
 "ProfessionalTool":{"gates":["wcag","model_provenance"],                     "attest":["professional-adequacy","model-validity"],      "min_sources":1},
}

def run(profile, page_ttl, html_path, ld_tbox, manifest_ttl=None, attest_ttl=None):
    spec=PROFILES[profile]; ah=G.sha256_file(html_path)
    results=[]; status={}
    def add(r): results.append(r); 
    # always-available individual gates (run those the profile needs; others reported as not-required)
    runners={
      "wcag":      lambda: G.wcag_gate(html_path),
      "model_provenance": lambda: G.model_provenance_gate(page_ttl, html_path),
      "assessment_rigor": lambda: G.assessment_rigor_gate(page_ttl),
      "bloom":     lambda: G.bloom_coverage_gate(page_ttl, ld_tbox),
    }
    for k in ["wcag","model_provenance","assessment_rigor","bloom"]:
        if k in spec["gates"]:
            r=runners[k](); results.append(r); status[k]=r.status
    # over-claim guard (always, even Companion) + attestation
    oc=G.standards_overclaim_gate(manifest_ttl or "", status, attest_ttl, ah); results.append(oc)
    att=G.attestation_gate(spec["attest"], attest_ttl, ah); results.append(att)
    # verdict from gate outputs only
    blocking=[r for r in results if r.status=="FAIL"]
    verdict="CERTIFIED @ "+profile if not blocking else "REFUSED @ "+profile
    return verdict, ah, results, spec

def report(profile, page_ttl, html_path, ld_tbox, manifest_ttl=None, attest_ttl=None):
    v,ah,results,spec=run(profile,page_ttl,html_path,ld_tbox,manifest_ttl,attest_ttl)
    print(f"=== Enriched acceptance @ {profile} ===")
    print(f"artifact (page html) sha256: {ah[:16]}…   required attestations: {spec['attest'] or 'none'}")
    for r in results: print("  ",r)
    print(f"VERDICT: {v}")
    return v

if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument("--profile",required=True); ap.add_argument("--page",required=True); ap.add_argument("--html",required=True)
    ap.add_argument("--ld",required=True); ap.add_argument("--manifest"); ap.add_argument("--attest")
    a=ap.parse_args()
    report(a.profile,a.page,a.html,a.ld,a.manifest,a.attest)
