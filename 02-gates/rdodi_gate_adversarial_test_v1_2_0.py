#!/usr/bin/env python3
"""
RDODI Gate Adversarial Test v1.2.0  (L-65) — HERMETIC
======================================================
Proves each gate in rdodi_pipeline_validator_v1_1_0 FAILS on bad input. A gate that
cannot fail is theater.

v1.2.0 (remediation R1): runs FROM FILES ALONE. All inputs resolve package-relative
from __file__ — no working-tree or outputs absolute paths anywhere. The F59 coverage/
substance fixtures (A/B/C/D) are:
  A = the real Ch.9 page bundled at 02-gates/fixtures/adversarial_fixture_zero_class_page_v1_0_0.ttl (0 structural classes)
  B/C/D = the byte-exact F59 ruletest fixtures bundled at 02-gates/fixtures/
The verdicts asserted are F59/F60 as written (L-66: not redefined). The parse-gate good/bad
inputs are still synthesized in-test via the existing w() helper (L-72: reuse, don't invent a loader).

Run: python3 rdodi_gate_adversarial_test_v1_2_0.py
Exit 0 = all gates proven real; exit 1 = a gate passed bad input (theater).
"""
import sys, os, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))          # 02-gates/
PKG  = os.path.dirname(HERE)                                # package root
sys.path.insert(0, HERE)
import rdodi_pipeline_validator_v1_1_0 as V
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, DCTERMS

DC = DCTERMS
TMP = tempfile.mkdtemp()
def w(name, ttl): p=os.path.join(TMP,name); open(p,"w").write(ttl); return p

# --- package-relative inputs (R1: no absolute paths) ---
STD_TBOX  = os.path.join(PKG, "01-stage-vocabularies/04-interactive-page/interactive_page_ontology_tbox_v1_0_1.ttl")
STD_SHACL = os.path.join(PKG, "01-stage-vocabularies/04-interactive-page/interactive_page_ontology_shacl_v1_0_1.ttl")
NS = "interactive-page-ontology#"

# F59 test-drive artifacts — bundled, byte-exact (02-gates/fixtures/ + the worked example)
A = os.path.join(PKG, "02-gates/fixtures/adversarial_fixture_zero_class_page_v1_0_0.ttl")   # real Ch.9 page: 0 classes
B = os.path.join(HERE, "fixtures/artifact_B_shell.ttl")          # 6 classes, empty
C = os.path.join(HERE, "fixtures/artifact_C_genuine.ttl")        # 6 classes, content
D = os.path.join(HERE, "fixtures/artifact_D_thin.ttl")           # 6 classes, junk fields

# fail fast with a clear message if any bundled input is missing (hermetic guarantee)
for label, p in [("STD_TBOX",STD_TBOX),("STD_SHACL",STD_SHACL),("A",A),("B",B),("C",C),("D",D)]:
    if not os.path.isfile(p):
        print(f"HERMETIC-FAIL: required bundled input {label} missing at {p}"); sys.exit(2)

passed=[]; failed=[]
def expect(label, cond):
    (passed if cond else failed).append(label)
    print(f"  {'OK ' if cond else 'XX THEATER'} {label}")

print("="*72); print("ADVERSARIAL GATE TESTS v1.2.0 (L-65: each gate must FAIL on bad input)"); print("="*72)

# ---- parse gate ----
print("\nparse gate (Stage*.A):")
good = w("good.ttl", "@prefix ex: <http://e#> . ex:s a ex:C .")
bad  = w("bad.ttl",  "@prefix ex: <http://e#> . ex:s a ex:C  <<<broken")
expect("parse passes valid ttl", V.gate_parse("Stage1.A", good).verdict=="PASS")
expect("parse FAILS malformed ttl", V.gate_parse("Stage1.A", bad).verdict=="FAIL")

# ---- COVERAGE RULE (blueprint F59): the 4 test-drive artifacts ----
print("\ncoverage rule (Stage4.cov) — the settled F59 rule:")
expect("coverage FAILS A (real Ch.9, 0 classes = abstention)",
       V.gate_coverage_rule("Stage4.cov", A, STD_TBOX, STD_SHACL, NS).verdict=="FAIL")
expect("coverage FAILS B (shell: 6 classes, empty = hollow)",
       V.gate_coverage_rule("Stage4.cov", B, STD_TBOX, STD_SHACL, NS).verdict=="FAIL")
expect("coverage PASSES C (genuine: 6 classes + content)",
       V.gate_coverage_rule("Stage4.cov", C, STD_TBOX, STD_SHACL, NS).verdict=="PASS")
expect("coverage PASSES D (thin: fields present — coverage's job is presence, not quality)",
       V.gate_coverage_rule("Stage4.cov", D, STD_TBOX, STD_SHACL, NS).verdict=="PASS")

# ---- SUBSTANCE RULE (blueprint F60): must catch the junk D that coverage passes ----
print("\nsubstance rule (Stage4.sub) — the settled F60 sentence+source rule:")
expect("substance FAILS A (0 individuals)",
       V.gate_substance_rule("Stage4.sub", A, STD_TBOX, STD_SHACL, NS).verdict=="FAIL")
expect("substance FAILS B (empty shells)",
       V.gate_substance_rule("Stage4.sub", B, STD_TBOX, STD_SHACL, NS).verdict=="FAIL")
expect("substance FAILS D (junk content 'n/a'/'x' — not complete sentences)",
       V.gate_substance_rule("Stage4.sub", D, STD_TBOX, STD_SHACL, NS).verdict=="FAIL")
expect("substance PASSES C (complete sentences + sourced)",
       V.gate_substance_rule("Stage4.sub", C, STD_TBOX, STD_SHACL, NS).verdict=="PASS")

# ---- divergence proof: D separates coverage (PASS) from substance (FAIL) ----
print("\nseparability proof (blueprint F61 — distinct diagnostics):")
cov_D = V.gate_coverage_rule("Stage4.cov", D, STD_TBOX, STD_SHACL, NS).verdict
sub_D = V.gate_substance_rule("Stage4.sub", D, STD_TBOX, STD_SHACL, NS).verdict
expect(f"artifact D: coverage={cov_D} but substance={sub_D} (gates give DISTINCT verdicts)",
       cov_D=="PASS" and sub_D=="FAIL")

# ---- sentence-form internal check (F60 cases) ----
print("\nsentence-form rule internals (F60 cases):")
expect("'n/a' is not a sentence", V._is_complete_sentence("n/a")[0]==False)
expect("genuine Ch.9 prose IS a sentence",
       V._is_complete_sentence("Quality assurance provides an auditing of the project to ensure standards are followed.")[0]==True)

print("\n" + "="*72)
print(f"RESULT: {len(passed)} passed, {len(failed)} theater-detections")
if failed:
    print("THEATER (a gate passed bad input):")
    for t in failed: print(f"   {t}")
    sys.exit(1)
print("ALL GATES VERIFIED REAL — each fails on bad input as required by L-65.")
sys.exit(0)
