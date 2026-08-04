#!/usr/bin/env python3
"""RDODI Deployed-Bar Gate v1.3.0 — now checks RICHNESS (depth) in addition to the HTML artifact.
Combines: (1) the v1.2.0 HTML artifact checks (sections, tables, interactives, quiz, size) on the page,
and (2) the richness rubric on the SOURCE ontology. BAR_MET requires BOTH.
Usage: python3 rdodi_deployed_bar_gate_v1_3_0.py <page.html> [--ontology <domain.ttl>]
"""
import sys, re, os, importlib.util

def html_checks(html):
    checks={}
    checks['words']=len(re.findall(r'\w+',re.sub(r'<[^>]+>',' ',html)))
    checks['sections']=len(re.findall(r'class="page"',html))
    checks['tables']=len(re.findall(r'<table',html))
    checks['svg']=len(re.findall(r'<svg',html))
    checks['interactives']=len(re.findall(r'class="exec-run"|class="taxonomy-explorer"|class="anim-demo"',html))
    checks['quiz']=('id="page-quiz"' in html) or ('qp-q' in html)
    checks['size_kb']=round(len(html)/1024,1)
    passed = (checks['words']>=4000 and checks['sections']>=8 and checks['tables']>=8 and
              checks['svg']>=3 and checks['interactives']>=3 and checks['quiz'] and checks['size_kb']>=50)
    return checks, passed

def load_rubric():
    p='/home/claude/rdodi_ecosystem_v1_22_1/13-pipeline/rdodi_richness_rubric_v1_0_0.py'
    spec=importlib.util.spec_from_file_location('rubric',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

if __name__=='__main__':
    if len(sys.argv)<2: print('usage: gate <page.html> [--ontology <ttl>]'); sys.exit(2)
    html=open(sys.argv[1]).read()
    hc, hpass = html_checks(html)
    print('=== HTML ARTIFACT CHECKS ===')
    for k,v in hc.items(): print(f'  {k}: {v}')
    print(f'  HTML artifact: {"PASS" if hpass else "FAIL"}')
    rpass=True; rpct=None
    if '--ontology' in sys.argv:
        onto=sys.argv[sys.argv.index('--ontology')+1]
        r=load_rubric().score_ontology(onto)
        rpct=r['score_pct']; rpass=(r['verdict']=='RICHNESS_MET')
        print(f'\n=== RICHNESS (DEPTH) CHECK on {onto} ===')
        print(f'  richness: {rpct}% -> {r["verdict"]} (threshold {r["threshold"]}%)')
        if r['gaps']:
            print('  top gaps:')
            for g in r['gaps'][:3]: print(f'    - {g["dimension"]}: {g["fix"]}')
    else:
        print('\n(no --ontology given: richness not checked; pass --ontology for the full depth gate)')
    verdict = 'BAR_MET' if (hpass and rpass) else 'BELOW_BAR'
    print(f'\n  VERDICT: {verdict}' + (f' (HTML {"ok" if hpass else "fail"}, richness {rpct}%)' if rpct is not None else ''))
    sys.exit(0 if verdict=='BAR_MET' else 1)
