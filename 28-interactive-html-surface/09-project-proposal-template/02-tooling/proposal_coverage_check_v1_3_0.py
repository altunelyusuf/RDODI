#!/usr/bin/env python3
"""proposal_coverage_check_v1_3_0.py (v1.3.0: refuses to run against the frozen 05-lineage snapshot unless ALLOW_SNAPSHOT=1 — RDODI found that snapshot stale relative to the pin and got 3 false "missing")

proposal_coverage_check_v1_2_0.py (v1.2.0: the register is read from $SCAMPS_ROOT/08-lineage when set, else from the frozen 05-lineage snapshot)

proposal_coverage_check_v1_1_0.py — does the proposal (or the interactive page) describe the register, or a different plan?

v1.1.0: also accepts an .html page (text extracted from the whole file, script data included), so the same gate
guards the Stage 4 page. Negative fixture for the page: a copy whose embedded register label is altered must FAIL.

The gate the package lacked. Proposal v2.0.0 validated nothing against the register and described a lineage
the register does not hold (G1-G4, O1-O6, EP-1..5, F-1..11, PKG-1..3). Every artefact gate reported clean.
This check reads the .docx text and the register and fails on either direction of drift:
  MISSING  a register element (goal, objective, area, deliverable, exclusion, package, iteration, milestone,
           work item, proposal) whose label does not appear in the document;
  FOREIGN  an identifier pattern from the retired hand-written plan (EP-n, PKG-n, F-n, IN-n, G-n gate) or a
           technology commitment no governed artefact names (see FOREIGN_TERMS).
Exit 0 when both lists are empty, 2 otherwise, 1 on error. L-95: proposal v2.0.0 is the known-bad input and
must FAIL; the generated v3.0.0 must PASS.

Usage (from the package root):  python3 03-tooling/proposal_coverage_check_v1_1_0.py <proposal.docx | page.html>
"""
import glob, re, sys, zipfile
import rdflib
from rdflib import RDF, RDFS, Namespace
B = Namespace('http://example.org/backlog#')
FOREIGN_PATTERNS = [r'\bEP-\d', r'\bPKG-\d', r'\bF-\d{1,2}\b', r'\bIN-\d', r'\bG-\d\b', r'\bRICE\b', r'\bDoDC-\d']
FOREIGN_TERMS = ['GraphCodeBERT', 'Code2Vec', 'R-GCN', 'StarCoder', 'LangGraph', 'Fuseki', 'Oxigraph', 'HuggingFace', 'React']

def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf8')
    return ' '.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', xml))

def page_text(path):
    raw = open(path, encoding='utf-8').read()
    # The page embeds the register itself verbatim (const LINEAGE_TTL = "..."); that is the source, not the
    # presentation, so it is excluded: the gate asks whether what the page SHOWS matches the register.
    raw = re.sub(r'const LINEAGE_TTL = "(?:[^"\\]|\\.)*";', ' ', raw)
    return re.sub(r'<[^>]+>', ' ', raw)

def main(path):
    text = (page_text(path) if path.lower().endswith('.html') else docx_text(path)).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&apos;', "'").replace('&quot;', '"')
    norm = lambda t: re.sub(r'\s+', ' ', t).strip().lower()
    T = norm(text)
    g = rdflib.Graph()
    import os
    if not os.environ.get('SCAMPS_ROOT') and os.environ.get('ALLOW_SNAPSHOT') != '1':
        print('SCAMPS_ROOT is not set. The register lives in altunelyusuf/SCAMPS (SCAMPS_PIN.txt); 05-lineage/ is a frozen proposal-stage snapshot and reads stale against a generated artefact. Set SCAMPS_ROOT, or ALLOW_SNAPSHOT=1 to check knowingly against the snapshot.'); sys.exit(1)
    reg = os.path.join(os.environ['SCAMPS_ROOT'], '08-lineage') if os.environ.get('SCAMPS_ROOT') else '05-lineage'
    for f in glob.glob(os.path.join(reg, '*.ttl')): g.parse(f)
    missing = []; total = 0
    for cls in [B.Goal, B.Objective, B.ScopeArea, B.ScopeDeliverable, B.ScopeExclusion, B.Package, B.Iteration, B.Milestone, B.Feature, B.EnhancementProposal, B.ExternalDependency]:
        for x in g.subjects(RDF.type, cls):
            lab = g.value(x, RDFS.label)
            if lab is None: continue
            total += 1
            if norm(str(lab)) not in T: missing.append((cls.split('#')[-1], str(lab)))
    foreign = []
    for pat in FOREIGN_PATTERNS:
        hits = re.findall(pat, text)
        if hits: foreign.append('%s x%d' % (pat, len(hits)))
    for term in FOREIGN_TERMS:
        n = text.count(term)
        if n: foreign.append('%s x%d' % (term, n))
    print('proposal :', path)
    print('register :', total, 'labelled elements across 11 classes')
    print('MISSING  :', len(missing))
    for c, l in missing[:40]: print('   ', c, '|', l)
    print('FOREIGN  :', len(foreign), ' '.join(foreign))
    ok = not missing and not foreign
    print('VERDICT  :', 'PASS — the proposal names every register element and no retired identifier' if ok else 'FAIL — the proposal and the register describe different plans')
    return 0 if ok else 2

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
