#!/usr/bin/env python3
"""Adversarial test for intention_coverage_gate (L-65 + verifies the one-hop semantics)."""
import sys, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import intention_coverage_gate_v1_0_0 as G

PG="http://example.org/rdodi/interactive-page-ontology#"
TMP=tempfile.mkdtemp()
HEAD=f"@prefix pg: <{PG}> .\n@prefix ex: <http://test#> .\n@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
def w(name, body): p=os.path.join(TMP,name); open(p,"w").write(HEAD+body); return p

passed=[]; failed=[]
def expect(label, cond): (passed if cond else failed).append(label); print(f"  {'OK ' if cond else 'XX'} {label}")

print("="*68); print("INTENTION-COVERAGE GATE ADVERSARIAL TEST (L-65)"); print("="*68)

# all intentions covered, no decoration -> PASS
allcov = w("allcov.ttl","""
ex:Doc pg:hasLearningObjective ex:I1, ex:I2 .
ex:W1 pg:coversLearningObjective ex:I1 .
ex:W2 pg:coversLearningObjective ex:I2 .
""")
# one uncovered intention -> still PASS (disclosed scope), but manifest shows it
oneuncov = w("oneuncov.ttl","""
ex:Doc pg:hasLearningObjective ex:I1, ex:I2 .
ex:W1 pg:coversLearningObjective ex:I1 .
""")
# a decoration widget (covers nothing declared) -> FAIL
decoration = w("decoration.ttl","""
ex:Doc pg:hasLearningObjective ex:I1 .
ex:W1 pg:coversLearningObjective ex:I1 .
ex:Wdecor pg:coversLearningObjective ex:Iundeclared .
""")

v1,_,m1 = G.gate(allcov)
v2,_,m2 = G.gate(oneuncov)
v3,_,m3 = G.gate(decoration)

print("\ncore semantics:")
expect("all covered -> PASS", v1=="PASS")
expect("all covered -> 0 disclosed", len(m1.disclosed_scope)==0)
print("\ndisclosed-scope is NOT a fail (user decision a):")
expect("one uncovered -> still PASS", v2=="PASS")
expect("one uncovered -> appears in disclosed_scope", len(m2.disclosed_scope)==1)
print("\ndecoration IS a fail (the asymmetry):")
expect("decoration widget -> FAIL", v3=="FAIL")
expect("decoration widget -> listed", len(m3.decoration_fails)==1)
print("\nthe gate CAN fail (not vacuous):")
expect("at least one input produces FAIL", v3=="FAIL")

print("\n"+"="*68)
print(f"RESULT: {len(passed)} passed, {len(failed)} failed")
sys.exit(1 if failed else 0)
