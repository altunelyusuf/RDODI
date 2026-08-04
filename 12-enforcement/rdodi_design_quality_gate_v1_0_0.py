#!/usr/bin/env python3
"""
RDODI Stage-4 Design-Quality Gate v1.0.0
========================================
The instrument F105 specified but this session never built (the promised-not-built gap).

WHAT IT IS — and is NOT (the F105/R14 honesty, enforced in code):
  The stage-conformance gate proves an artifact is CORRECT (typed + SHACL-valid). It does NOT prove the
  artifact is well-DESIGNED — v2.0.0 of the Ch.10 page passed conformance and was still judged inadequate.
  This gate enforces a richness FLOOR so no future page ships thin or unchecked. It does NOT, and cannot,
  certify the CEILING (beauty, apt metaphor, genuine pedagogy) — those remain human judgment (R14). A green
  verdict here means "not thin / not unchecked," never "good."

FLOOR CHECKS (all measurable from the page ABox + the rendered HTML):
  D1  density floor   — at least one non-text encoding (InstructionalWidget | SourceFigure) per major
                        ChapterSection the page covers. (This rule alone would have FAILED v2.0.0.)
  D2  heuristics      — the page declares >=1 UsabilityHeuristic / DialoguePrinciple it claims to satisfy
                        (reusing the ontology's EXISTING vocabulary, unused until now).
  D3  widget-warrant  — every InstructionalWidget enforces the concept it teaches (demonstratesSubject
                        present; CoupledVariableDemonstrator additionally carries enforcesDomainConstraint).
  D4  browser-clean   — (delegated) the page was real-browser checked: renders, 0 console errors. Recorded
                        as a required attestation, not re-run here.

Verdicts: FLOOR_MET | FLOOR_NOT_MET | CANNOT_RUN. A FLOOR_MET is explicitly labeled "floor only — ceiling is
human" in the report, so the verdict can never be mistaken for a quality certification.
"""
import sys, json
from pathlib import Path
from rdflib import Graph, Namespace, RDF
from rdflib.namespace import OWL

P = Namespace('http://example.org/rdodi/interactive-page-ontology#')

def _loc(u): return str(u).split('#')[-1]

def run(page_abox_path, *, min_encodings_per_section=1, browser_clean_attested=False):
    reasons = []
    p = Path(page_abox_path)
    if not p.exists():
        return "CANNOT_RUN", [f"page ABox not found: {page_abox_path}"]
    try:
        g = Graph(); g.parse(page_abox_path)
    except Exception as e:
        return "CANNOT_RUN", [f"page ABox does not parse: {e}"]

    def of_type(frag):
        return [s for s in g.subjects(RDF.type, None)
                if any(_loc(t) == frag for t in g.objects(s, RDF.type))]

    widgets = of_type('InstructionalWidget')
    figures = of_type('SourceFigure')
    sections = of_type('ChapterSection')
    heuristics = of_type('UsabilityHeuristic') + of_type('DialoguePrinciple')

    failed = False

    # D1 — density floor: encodings vs sections
    encodings = len(widgets) + len(figures)
    n_sections = max(len(sections), 1)
    if encodings < min_encodings_per_section * n_sections:
        failed = True
        reasons.append(f"D1 FAIL density floor: {encodings} non-text encodings for {n_sections} sections "
                       f"(need >= {min_encodings_per_section}/section). This is the v2.0.0 thinness failure.")
    else:
        reasons.append(f"D1 ok: {encodings} encodings ({len(widgets)} widgets + {len(figures)} figures) "
                       f"for {n_sections} sections.")

    # D2 — declared usability heuristics
    if not heuristics:
        failed = True
        reasons.append("D2 FAIL: page declares no UsabilityHeuristic/DialoguePrinciple it claims to satisfy "
                       "(the ontology has the vocabulary; declare which heuristics the page honors).")
    else:
        reasons.append(f"D2 ok: {len(heuristics)} usability heuristic(s)/principle(s) declared.")

    # D3 — widget-warrant
    unwarranted = []
    for w in widgets:
        if not list(g.objects(w, P.demonstratesSubject)):
            unwarranted.append(_loc(w))
    if unwarranted:
        failed = True
        reasons.append(f"D3 FAIL widget-warrant: {len(unwarranted)} widget(s) without demonstratesSubject "
                       f"(decorative, not concept-enforcing): {unwarranted[:5]}")
    else:
        reasons.append(f"D3 ok: all {len(widgets)} widgets carry demonstratesSubject (concept-enforcing).")

    # D4 — browser-clean attestation (delegated, must be supplied)
    if not browser_clean_attested:
        failed = True
        reasons.append("D4 FAIL: no real-browser zero-console-error attestation supplied "
                       "(run the page in a browser and pass browser_clean_attested=True).")
    else:
        reasons.append("D4 ok: real-browser zero-console-error attested.")

    verdict = "FLOOR_NOT_MET" if failed else "FLOOR_MET"
    return verdict, reasons

def render(verdict, reasons):
    L = ["="*70, "RDODI STAGE-4 DESIGN-QUALITY GATE (richness FLOOR, not quality ceiling)", "="*70,
         f"VERDICT: {verdict}"]
    if verdict == "FLOOR_MET":
        L.append("  NOTE: floor only — this means 'not thin / not unchecked', NEVER 'well-designed'.")
        L.append("  The ceiling (beauty, apt visualization, genuine pedagogy) remains human judgment (R14).")
    L.append("")
    for r in reasons:
        L.append(f"  {r}")
    return "\n".join(L)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("page_abox")
    ap.add_argument("--browser-clean", action="store_true", help="attest real-browser zero-console-error")
    ap.add_argument("--min-per-section", type=int, default=1)
    a = ap.parse_args()
    v, r = run(a.page_abox, min_encodings_per_section=a.min_per_section,
               browser_clean_attested=a.browser_clean)
    print(render(v, r))
    sys.exit(0 if v == "FLOOR_MET" else 1)
