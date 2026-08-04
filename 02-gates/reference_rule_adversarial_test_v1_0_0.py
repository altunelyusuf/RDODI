#!/usr/bin/env python3
"""Adversarial test for reference_rule_gate (L-65). Mirrors the test-drive that settled it."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reference_rule_gate_v1_0_0 import reference_rule

def refs(n, n_unverified=0, n_flagged=0):
    out=[{"id":f"r{i}","status":"verified"} for i in range(n-n_unverified-n_flagged)]
    out+=[{"id":f"u{j}","status":"unverified"} for j in range(n_unverified)]
    out+=[{"id":f"f{k}","status":"unavailable_flagged"} for k in range(n_flagged)]
    return out
def claims(n, n_uncited=0, dangling=0):
    out=[{"text":f"c{i}","needs_cite":True,"cites":["r0"]} for i in range(n-n_uncited-dangling)]
    out+=[{"text":f"unc{j}","needs_cite":True,"cites":[]} for j in range(n_uncited)]
    out+=[{"text":f"dng{k}","needs_cite":True,"cites":["nonexistent"]} for k in range(dangling)]
    return out

passed=[]; failed=[]
def expect(label, cond): (passed if cond else failed).append(label); print(f"  {'OK ' if cond else 'XX'} {label}")

print("="*64); print("REFERENCE RULE ADVERSARIAL TEST (L-65)"); print("="*64)
print("\nrule PASSES the genuinely-good cases:")
expect("8 refs all verified, all claims cited -> PASS", reference_rule(refs(8), claims(10)).verdict=="PASS")
expect("flagged-unavailable ref is acceptable -> PASS", reference_rule(refs(5,n_flagged=1), claims(3)).verdict=="PASS")
print("\nrule FAILS each defect the >=40 number missed:")
expect("40 refs but 1 uncited claim -> FAIL", reference_rule(refs(40), claims(10,n_uncited=1)).verdict=="FAIL")
expect("40 refs but 3 unverified -> FAIL", reference_rule(refs(40,n_unverified=3), claims(10)).verdict=="FAIL")
expect("dangling citation -> FAIL", reference_rule(refs(5), claims(5,dangling=1)).verdict=="FAIL")
print("\nthe gate can fail (not vacuous):")
expect("at least one input FAILs", reference_rule(refs(40,n_unverified=3), claims(10)).verdict=="FAIL")

print("\n"+"="*64)
print(f"RESULT: {len(passed)} passed, {len(failed)} failed")
sys.exit(1 if failed else 0)
