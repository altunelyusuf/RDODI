#!/usr/bin/env python3
"""RDODI affordance re-grounder v1.0.0 — makes re-grounding a repeatable capability.
Given a (page.ttl, page.html) pair, detects affordances REALIZED in the HTML but NOT DECLARED in the page model
(e.g. v1.1.0 RoutedViewNavigation/OverflowTabBar on a page authored pre-adoption) and adds the missing
declarations. Only adds what is genuinely realized (never fabricates a declaration for an unrealized affordance).
Usage: python3 rdodi_affordance_regrounder_v1_0_0.py <page.ttl> <page.html> <out.ttl>  |  --scan <ecosystem_dir>"""
import sys, os, glob, rdflib
from rdflib import RDF, Namespace, URIRef
PG = Namespace("http://example.org/rdodi/interactive-page-ontology#")
# only affordances with a RELIABLE html signature + their declaration predicate
REALIZABLE = {'RoutedViewNavigation':('class="view', PG.includesNavigationPattern),
              'OverflowTabBar':('role="menubar"', PG.includesWayfindingAffordance)}

def needs(page_ttl, html_path):
    g = rdflib.Graph(); g.parse(page_ttl); H = open(html_path, encoding='utf-8').read()
    declared = {str(t).split('#')[-1] for s,p,o in g for t in g.objects(o, RDF.type)
                if p in (PG.includesNavigationPattern, PG.includesWayfindingAffordance, PG.usesUIPattern)}
    return [k for k,(sig,_) in REALIZABLE.items() if sig in H and k not in declared], g

def reground(page_ttl, html_path, out):
    missing, g = needs(page_ttl, html_path)
    if not missing:
        print("no re-grounding needed (all realized affordances already declared)."); return []
    pg = next(iter(s for s,p,o in g if p in (PG.includesNavigationPattern, PG.includesWayfindingAffordance, PG.usesUIPattern)), None)
    if pg is None:
        print("no page individual declaring affordances found — cannot re-ground"); return []
    for k in missing:
        _, pred = REALIZABLE[k]; inst = URIRef(str(PG)+k.lower()+"_inst")
        g.add((pg, pred, inst)); g.add((inst, RDF.type, PG[k]))
    g.serialize(destination=out, format="turtle")
    print(f"re-grounded: declared {missing} -> {out}"); return missing

def scan(root):
    pages = glob.glob(os.path.join(root, "**", "*page*abox*.ttl"), recursive=True) + \
            glob.glob(os.path.join(root, "**", "*page*v*.ttl"), recursive=True)
    htmls = glob.glob(os.path.join(root, "**", "*.html"), recursive=True)
    flagged = 0
    for pt in set(pages):
        for h in htmls:
            try:
                m, _ = needs(pt, h)
                if m: print(f"  NEEDS re-grounding: {os.path.basename(pt)} vs {os.path.basename(h)} -> {m}"); flagged += 1
            except Exception: pass
    print(f"scan complete: {flagged} page/html pairs need re-grounding")
    return flagged

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--scan":
        scan(sys.argv[2])
    elif len(sys.argv) >= 4:
        reground(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
