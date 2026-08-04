#!/usr/bin/env python3
"""Adversarial test for widget_gates v1.0.0 (L-65: each gate must FAIL on bad input)."""
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import widget_gates_v1_0_0 as G

WP="http://example.org/widget-primitives#"; DS="http://example.org/rdodi/discourse-selection#"
DC="http://purl.org/dc/terms/"
TMP=tempfile.mkdtemp()
HEAD=f"""@prefix wp: <{WP}> .
@prefix ds: <{DS}> .
@prefix dcterms: <{DC}> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix ex: <http://test#> .
"""
def w(name, body):
    p=os.path.join(TMP,name); open(p,"w").write(HEAD+body); return p

# GOOD widget: warrant + concept + source + passing test
good = w("good.ttl", """
ex:widget1 a owl:NamedIndividual ;
    wp:instantiatesPrimitive wp:Primitive_MultiClassSelectorDistinct ;
    ds:selectionWarrant "fired on K-category enumeration at section 3" ;
    wp:demonstratesConcept ex:VarianceTypes ;
    dcterms:source "Marchewka 2016 Ch.9 p.240" ;
    wp:designTestPassed true .
""")
# BAD-warrant: no selectionWarrant
bad_warrant = w("bad_warrant.ttl", """
ex:widget1 a owl:NamedIndividual ;
    wp:instantiatesPrimitive wp:Primitive_MultiClassSelectorDistinct ;
    wp:demonstratesConcept ex:VarianceTypes ;
    dcterms:source "p.240" ;
    wp:designTestPassed true .
""")
# BAD-grounded: no concept + no source
bad_grounded = w("bad_grounded.ttl", """
ex:widget1 a owl:NamedIndividual ;
    wp:instantiatesPrimitive wp:Primitive_MultiClassSelectorDistinct ;
    ds:selectionWarrant "fired on enumeration" ;
    wp:designTestPassed true .
""")
# BAD-tested: test not passed
bad_tested = w("bad_tested.ttl", """
ex:widget1 a owl:NamedIndividual ;
    wp:instantiatesPrimitive wp:Primitive_MultiClassSelectorDistinct ;
    ds:selectionWarrant "fired on enumeration" ;
    wp:demonstratesConcept ex:VarianceTypes ;
    dcterms:source "p.240" ;
    wp:designTestPassed false .
""")

passed=[]; failed=[]
def expect(label, cond): (passed if cond else failed).append(label); print(f"  {'OK ' if cond else 'XX THEATER'} {label}")

print("="*70); print("WIDGET GATES ADVERSARIAL TEST (L-65)"); print("="*70)
print("\ngood widget passes all three:")
expect("warrant PASS on good",  G.gate_warrant(good).verdict=="PASS")
expect("grounded PASS on good", G.gate_grounded(good).verdict=="PASS")
expect("tested PASS on good",   G.gate_tested(good).verdict=="PASS")
print("\neach gate FAILS on its specific bad input:")
expect("warrant FAILS on missing warrant",   G.gate_warrant(bad_warrant).verdict=="FAIL")
expect("grounded FAILS on missing concept+source", G.gate_grounded(bad_grounded).verdict=="FAIL")
expect("tested FAILS on failed design-test",  G.gate_tested(bad_tested).verdict=="FAIL")
print("\ncross-check: a gate does NOT fail on a different gate's defect (no false coupling):")
expect("grounded PASSES when only warrant is missing", G.gate_grounded(bad_warrant).verdict=="PASS")
expect("tested PASSES when only grounding is missing",  G.gate_tested(bad_grounded).verdict=="PASS")

print("\n"+"="*70)
print(f"RESULT: {len(passed)} passed, {len(failed)} theater-detections")
if failed:
    for t in failed: print(f"   THEATER: {t}")
    sys.exit(1)
print("ALL WIDGET GATES VERIFIED REAL — each fails on its bad input (L-65).")
sys.exit(0)
