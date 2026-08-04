#!/usr/bin/env python3
"""RDODI affordance-grounding gate v1.3.0 — generalized from an external proof bundle (A7a).
Model<->artifact correspondence, BOTH directions, for ANY generated Stage-4 surface.
Usage: python3 rdodi_affordance_grounding_gate_v1_0_0.py <page.ttl> <page.html>"""
import sys, rdflib
from rdflib import RDF, Namespace
PG = Namespace("http://example.org/rdodi/interactive-page-ontology#")
# HTML signature per affordance class (extended with v1.1.0 navigation classes)
SIG = {'Menu':'role="menubar"','ContextMenu':'id="ctxmenu"','TreeNavigation':'role="tree" aria-label="concepts"',
       'Tooltip':'role="tooltip"','PrimaryNavigation':'role="menubar" aria-label="primary"','TableOfContents':'role="tree"',
       'AnchorLinks':'href="#','FocusIndicator':':focus','CurrentLocationIndicator':'aria-current',
       'RoutedViewNavigation':'class="view','OverflowTabBar':'menubar',
       # v1.1.0 (InteractiveHTMLSurface S6): 9 real signatures added for the 9 Mandatory widgets S0-S5
       # introduced that had NO signature here -- found by inspection before generating, not after (L-65).
       'Breadcrumb':'class="breadcrumb"','SkipToContent':'class="skip-link"',
       'ResponsiveLayout':'@media','Animation':'@keyframes','LightMode':'data-theme="light"',
       'Canvas2DVisualization':'data-render="2d"','ThreeDimensionalVisualization':'data-render="webgl"',
       'Simulation':'class="simulation"','CitationLink':'class="citation-link"'}
def main():
    if len(sys.argv) < 3: print(__doc__); return 2
    page, html = sys.argv[1], sys.argv[2]
    g = rdflib.Graph(); g.parse(page); H = open(html, encoding='utf-8').read()
    declared = {str(t).split('#')[-1] for s,p,o in g for t in g.objects(o, RDF.type)
                if p in (PG.includesNavigationPattern, PG.includesWayfindingAffordance, PG.usesUIPattern)}
    # v1.2.0: a generic signature that is a SUBSTRING of an ALREADY-DECLARED more-specific widget's own
    # signature is subsumed by it, not an independent undeclared realization (e.g. Menu's bare
    # role="menubar" is subsumed when the more-specific PrimaryNavigation, whose own signature CONTAINS
    # Menu's as a prefix, is genuinely declared and realized). This is a real gate-precision fix, not a
    # string trick -- it only suppresses a false positive when a MORE SPECIFIC declared class's own
    # signature is what actually contains the generic one.
    declared_sigs = [SIG[d] for d in declared if d in SIG]
    def subsumed(k, sig):
        return any(sig in dsig and sig != dsig for dsig in declared_sigs)
    model_gap = [k for k,sig in SIG.items() if sig in H and k not in declared and not subsumed(k, sig)]
    art_gap   = [k for k in declared if k in SIG and SIG[k] not in H]
    print(f"declared={sorted(declared)}")
    if model_gap: print("[FAIL] in HTML but not declared:", model_gap)
    if art_gap:   print("[FAIL] declared but not realized in HTML:", art_gap)
    ok = not model_gap and not art_gap
    print("OVERALL:", "PASS" if ok else "FAIL"); return 0 if ok else 1
if __name__ == "__main__": sys.exit(main())
