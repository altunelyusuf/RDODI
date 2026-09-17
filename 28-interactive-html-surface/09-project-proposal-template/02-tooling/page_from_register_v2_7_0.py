#!/usr/bin/env python3
"""page_from_register_v2_7_0.py (v2.7.0: the project, instance and framework namespaces, the framework's label and the page title come from proposal_project_data_v*.json; shell template v2.1.0 with %%TITLE%%/%%SUBTITLE%% as parameterised by RDODI; models v2.4.0)

page_from_register_v2_6_0.py (v2.6.0: one lineage chart — the older Traceability model retired; scope statement → mission / area / deliverable / exclusion edges; derived package → deliverable edges, dashed; scope taxonomy note; models v2.3.0)

page_from_register_v2_4_0.py (v2.4.0: full-lineage traceability model with taxonomy; models v2.1.0)

page_from_register_v2_3_0.py (v2.3.0: goal facings)

page_from_register_v2_2_0.py (v2.2.0: dated iterations)

page_from_register_v2_1_0.py — the interactive Stage 4 page, generated from the register.

v2.1.0: reads the register and the pipeline ontology from the pinned SCAMPS checkout ($SCAMPS_ROOT), see
proposal_from_register_v2_1_0.py.

v2.0.0 (owner review of v1.0.0): long views are split into sub-pages with sub-tabs; the left menu is an
Explorer-style tree (icons, chevrons, expand all / collapse all, short labels only, deeper hierarchy); the
ontologies (project TBox/ABox, framework alignment, the register itself) are drawn as interactive graphs whose
selected element opens a detail card on the right; context menus (right-click) and tooltips on tree nodes,
cards and graph nodes.

Skeleton: RDODI's default Stage 4 shape (28-interactive-html-surface/README_v1_1_0.md, owner ruling
2026-08-27): hierarchical left sidebar tree, permanent top tabs with sub-sections, in-page panel swapping,
and a grounded console that answers only from the artefact's own content. Navigation follows BP-D34
(more than 25 sections with long titles: grouped permanent top bar with a sub-section sidebar).

Why this is generated rather than instantiated from the shipped corpus template: the template's own
instantiation tool swaps six constants inside a 1.2 MB page whose shell — title, tab labels, agent prose,
hundreds of identifiers in script — stays bound to the package it was written for, and whose engines load
from five CDNs. Measured on RDODI's own instance (rdodi_lineage_interactive_v3_0_0.html): the <title> still
names that other package. A proposal page cannot ship under another project's title, so this generator
produces the same skeleton from the same source of truth as the proposal document (05-lineage/*.ttl,
the blueprint, the project TBox/ABox and proposal_prose_v*.md), with every visual model computed from the
register at build time and no network dependency. Recorded as a variation of the default, not a replacement.

Usage, from the package root:
  python3 03-tooling/page_from_register_v2_7_0.py --out 04-documentation/vaf_ap_page_vX_Y_Z.html
Generated artefact: regenerate, never hand-edit (L-112 file class c).
"""
import argparse, datetime, glob, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import proposal_from_register_v2_4_0 as P

def esc(t): return html.escape(str(t), quote=True)

def blocks_to_html(blocks, T):
    out = []; sec = 0
    for b in blocks:
        if 'title' in b: continue
        if 'h' in b:
            lvl = b['h']; text = b['text']
            sid = 'sec-' + re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')[:60]
            out.append('<h%d id="%s" class="doc-h%d">%s</h%d>' % (lvl + 1, sid, lvl, esc(text), lvl + 1))
        elif 'p' in b:
            cls = 'ref' if b.get('ref') else 'para'
            txt = esc(b['p'])
            txt = re.sub(r'\[(\d+)\]', r'<a class="cite" href="#ref-\1" data-ref="\1">[\1]</a>', txt)
            txt = re.sub(r'\bTable (\d+)\b', r'<a class="tabref" href="#table-\1">Table \1</a>', txt)
            if b.get('ref'):
                n = re.match(r'\[(\d+)\]', b['p']).group(1); out.append('<p id="ref-%s" class="ref">%s</p>' % (n, txt))
            else: out.append('<p class="%s">%s</p>' % (cls, txt))
        elif 'table' in b:
            t = b['table']; m = re.match(r'Table (\d+)\.', b['caption']); tid = 'table-' + (m.group(1) if m else 'x')
            out.append('<figure class="tbl" id="%s"><figcaption>%s</figcaption><div class="tblwrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div></figure>' % (
                tid, esc(b['caption']), ''.join('<th>%s</th>' % esc(h) for h in t['header']),
                ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % esc(c) for c in r) for r in t['rows'])))
    return '\n'.join(out)

def toc(blocks):
    items = []
    for b in blocks:
        if 'h' in b and b['h'] in (1, 2):
            sid = 'sec-' + re.sub(r'[^a-z0-9]+', '-', b['text'].lower()).strip('-')[:60]
            items.append({'level': b['h'], 'id': sid, 'text': b['text']})
    return items

def graphs(t, g):
    import rdflib
    from rdflib import RDF, RDFS, OWL
    PD = P.project_data(); FW = PD['framework']; OTHER = PD.get('other_namespaces', {})
    SKOS = P.SKOS; VAP = rdflib.Namespace(PD['project_namespace']) if os.environ.get('SCAMPS_ROOT') else P.VAP; B = P.B
    def isfw(u): return str(u).startswith(FW['namespace'])
    def fwlab(u): return FW['prefix'] + ':' + P.local(u)
    def otherpref(u): return next((v['prefix'] for k, v in OTHER.items() if str(u).startswith(k)), 'ext') + ':'
    def lab(x): return P.s(t.value(x, RDFS.label)) or P.local(x)
    def defn(x): return P.s(t.value(x, SKOS.definition)) or P.s(t.value(x, RDFS.comment))
    nodes, edges = [], []; seen = set()
    def add(nid, kind, label, desc='', ns=''):
        if nid in seen: return
        seen.add(nid); nodes.append({'id': nid, 'kind': kind, 'label': label, 'desc': desc, 'ns': ns})
    for c in t.subjects(RDF.type, OWL.Class):
        if str(c).startswith(str(VAP)):
            add(P.local(c), 'class', lab(c), defn(c), 'vap')
            for sc in t.objects(c, RDFS.subClassOf):
                if str(sc).startswith(str(VAP)): edges.append({'a': P.local(c), 'b': P.local(sc), 'rel': 'subClassOf'})
            for m in t.objects(c, SKOS.closeMatch):
                add(P.local(m), 'vaf', fwlab(m), 'A class of %s (%s), aligned by skos:closeMatch; never imported.' % (FW['label'], FW['ontology_file']), 'va'); edges.append({'a': P.local(c), 'b': P.local(m), 'rel': 'closeMatch'})
    for pr in t.subjects(RDF.type, OWL.ObjectProperty):
        if not str(pr).startswith(str(VAP)): continue
        add(P.local(pr), 'property', lab(pr), defn(pr), 'vap')
        for dm in t.objects(pr, RDFS.domain):
            add(P.local(dm), 'class' if str(dm).startswith(str(VAP)) else 'vaf', lab(dm) if str(dm).startswith(str(VAP)) else fwlab(dm), defn(dm), 'vap' if str(dm).startswith(str(VAP)) else 'va'); edges.append({'a': P.local(dm), 'b': P.local(pr), 'rel': 'domain'})
        for rg in t.objects(pr, RDFS.range):
            add(P.local(rg), 'class' if str(rg).startswith(str(VAP)) else 'vaf', lab(rg) if str(rg).startswith(str(VAP)) else fwlab(rg), defn(rg), 'vap' if str(rg).startswith(str(VAP)) else 'va'); edges.append({'a': P.local(pr), 'b': P.local(rg), 'rel': 'range'})
    META = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.Ontology, OWL.NamedIndividual, OWL.AnnotationProperty}
    indivs = sorted({i for i, ty in t.subject_objects(RDF.type) if ty not in META and not str(i).startswith(str(VAP)) or (ty == OWL.NamedIndividual)}, key=str)
    indivs = [i for i in indivs if not any(ty in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.Ontology) for ty in t.objects(i, RDF.type))]
    for i in indivs:
        add(P.local(i), 'individual', lab(i), defn(i), 'vapi')
        for ty in t.objects(i, RDF.type):
            if ty == OWL.NamedIndividual: continue
            if str(ty).startswith(str(VAP)): edges.append({'a': P.local(i), 'b': P.local(ty), 'rel': 'type'})
            else:
                add(P.local(ty), 'vaf' if isfw(ty) else 'external', (FW['prefix'] + ':' if isfw(ty) else otherpref(ty)) + P.local(ty), 'A class of %s, used as it is (never re-declared here).' % (FW['label'] if isfw(ty) else next((v['label'] for k, v in OTHER.items() if str(ty).startswith(k)), 'another package')), 'va' if isfw(ty) else 'agdev'); edges.append({'a': P.local(i), 'b': P.local(ty), 'rel': 'type'})
        for pr, o in t.predicate_objects(i):
            if isinstance(o, rdflib.URIRef) and pr not in (RDF.type, RDFS.label, RDFS.seeAlso) and (str(pr).startswith(str(VAP)) or isfw(pr) or any(str(pr).startswith(k) for k in OTHER)):
                if P.local(o) not in seen: add(P.local(o), 'vaf' if isfw(o) else 'individual', fwlab(o) if isfw(o) else lab(o), defn(o), 'va' if isfw(o) else 'vapi')
                edges.append({'a': P.local(i), 'b': P.local(o), 'rel': P.local(pr)})
    project = {'nodes': nodes, 'edges': edges}
    # register graph: lineage individuals by backlog class with typed relations
    rn, re_, rseen = [], [], set()
    keep = {'Mission': 'mission', 'ScopeStatement': 'scope', 'ScopeArea': 'area', 'ScopeDeliverable': 'deliverable', 'ScopeExclusion': 'exclusion', 'Goal': 'goal', 'Objective': 'objective', 'Feature': 'workitem', 'Package': 'package', 'Iteration': 'iteration', 'Milestone': 'milestone', 'Roadmap': 'roadmap', 'ExternalDependency': 'external', 'EnhancementProposal': 'proposal', 'Blueprint': 'blueprint', 'DomainEntity': 'entity'}
    props = {'contributesToMission', 'derivesFromScope', 'contributesToGoal', 'fillsScope', 'pursuesObjective', 'satisfiesDeliverable', 'hasMember', 'targetsIteration', 'contributesToMilestone', 'dependsOnExternal', 'proposalFor', 'unblocksItem', 'coversArea', 'requiresDeliverable', 'deliverableForArea', 'goalCoversArea', 'guardsExclusion', 'hasScopeExclusion', 'coversEntity', 'blueprintFor', 'roadmapOf', 'scopeForMission', 'missionFor', 'roadmapRealises', 'hasDomainEntity'}
    for cls, kind in keep.items():
        for x in g.subjects(RDF.type, B[cls]):
            nid = P.local(x); rseen.add(nid); rn.append({'id': nid, 'kind': kind, 'label': P.s(g.value(x, RDFS.label)) or nid, 'desc': P.s(g.value(x, SKOS.definition)), 'cls': cls})
    for x in list(rseen):
        pass
    for s_, p_, o_ in g:
        if P.local(p_) in props and P.local(s_) in rseen and isinstance(o_, rdflib.URIRef) and P.local(o_) in rseen:
            re_.append({'a': P.local(s_), 'b': P.local(o_), 'rel': P.local(p_)})
    register = {'nodes': rn, 'edges': re_}
    return {'project': project, 'register': register}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    g, t = P.load(); m = P.build(g, t)
    P_ = P.paths(); m['sources'] = sorted(os.path.basename(f) for f in glob.glob(os.path.join(P_['lineage'], '*.ttl'))) + [os.path.basename(P.highest(os.path.join(P_['onto'], 'vaf_ap_blueprint_v*_*_*.ttl')))]; m['register_label'] = P_['label']
    m['prose'] = P.highest('04-documentation/proposal_prose_v*_*_*.md')
    m['version'] = '.'.join(re.findall(r'_v(\d+)_(\d+)_(\d+)\.html$', a.out)[0])
    m['generated_at'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%MZ')
    T = P.Tables(); P.define_tables(m, T)
    body = P.prose_blocks(m, m['prose'], T); apps = P.appendices(m, T)
    first_h = next(i for i, b in enumerate(body) if b.get('h') == 1 and b.get('text') != 'Abstract')
    abstract, rest = body[:first_h], body[first_h:]
    refs_i = next(i for i, b in enumerate(rest) if b.get('h') == 1 and b['text'] == 'References')
    main_blocks, ref_blocks = rest[:refs_i], rest[refs_i:]
    # sub-pages of the proposal by section number
    groups = [('intent', 'Intent (1–6)', range(1, 7)), ('plan', 'Plan (7–10)', range(7, 11)), ('delivery', 'Delivery (11–14)', range(11, 15)), ('governance', 'Governance (15–20)', range(15, 21))]
    panes = {'front': [], 'refs': ref_blocks}; sec_pane = {'sec-abstract': 'front', 'sec-list-of-abbreviations': 'front', 'sec-references': 'refs'}
    cur = None
    for b in main_blocks:
        if b.get('h') == 1:
            n = int(re.match(r'(\d+)\.', b['text']).group(1)); cur = next(k for k, _, r in groups if n in r)
        panes.setdefault(cur, []).append(b)
        if 'h' in b: sec_pane['sec-' + re.sub(r'[^a-z0-9]+', '-', b['text'].lower()).strip('-')[:60]] = cur
    prop_subtabs = [['front', 'Front matter']] + [[k, l] for k, l, _ in groups] + [['refs', 'References']]
    prop_panes = '<div class="pane active" data-pane="front"><div class="doc">%s<div id="abbr-block"></div></div></div>' % blocks_to_html(abstract, T)
    for k, _, _ in groups: prop_panes += '<div class="pane" data-pane="%s"><div class="doc">%s</div></div>' % (k, blocks_to_html(panes[k], T))
    prop_panes += '<div class="pane" data-pane="refs"><div class="doc">%s</div></div>' % blocks_to_html(ref_blocks, T)
    # appendices: one sub-page per appendix
    app_panes = ''; app_subtabs = []; app_pane = {}; cur = None; chunks = {}
    for b in apps:
        if b.get('h') == 1: cur = re.match(r'Appendix ([A-G])\.', b['text']).group(1); app_subtabs.append([cur, 'Appendix ' + cur + ' · ' + b['text'].split('. ', 1)[1]])
        chunks.setdefault(cur, []).append(b)
        if 'h' in b: app_pane['sec-' + re.sub(r'[^a-z0-9]+', '-', b['text'].lower()).strip('-')[:60]] = cur
    for k, _ in app_subtabs: app_panes += '<div class="pane%s" data-pane="%s"><div class="doc">%s</div></div>' % (' active' if k == 'A' else '', k, blocks_to_html(chunks[k], T))
    md = P.to_markdown(body + apps); used = P.abbreviations(md); abbr = {u: P.ABBR[u] for u in used if u in P.ABBR}
    lineage_ttl = '\n'.join(open(f, encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(P_['lineage'], '*.ttl'))))
    data = {k: m[k] for k in ['mission', 'scope', 'areas', 'deliverables', 'exclusions', 'goals', 'objectives', 'items', 'packages', 'iterations', 'milestones', 'roadmap', 'horizons', 'external', 'proposals', 'disclosure', 'dod', 'blueprint', 'gaps', 'obligations', 'stage_outputs', 'tbox', 'tbox_props', 'counts', 'gaps_semantic', 'sources', 'version', 'generated_at']}
    PD = P.project_data(); data['graphs'] = graphs(t, g); data['abbr'] = abbr; data['register_label'] = m['register_label']; data['project'] = {'title': PD['title'], 'subtitle': PD['subtitle'], 'framework': PD['framework'], 'review_note': PD.get('review_note', '')}; data['prose_file'] = os.path.basename(m['prose']); data['tables'] = T.n
    data['toc'] = toc(main_blocks); data['app_toc'] = toc(apps); data['sec_pane'] = sec_pane; data['app_pane'] = app_pane
    page = open(os.path.join(here, 'page_template_v2_1_0.html'), encoding='utf-8').read().replace('%%TITLE%%', PD['title']).replace('%%SUBTITLE%%', PD['subtitle'])
    page = page.replace('%%MODEL_FUNCTIONS%%', open(os.path.join(here, 'page_models_v2_4_0.js'), encoding='utf-8').read()).replace('%%CONSOLE%%', open(os.path.join(here, 'page_console_v2_0_0.js'), encoding='utf-8').read())
    page = page.replace('%%VERSION%%', m['version']).replace('%%GENERATED%%', m['generated_at'])
    page = page.replace('%%PROPOSAL_PANES%%', prop_panes).replace('%%APPENDIX_PANES%%', app_panes)
    page = page.replace('%%PROPOSAL_SUBTABS%%', json.dumps(prop_subtabs)).replace('%%APPENDIX_SUBTABS%%', json.dumps(app_subtabs, ensure_ascii=False))
    page = page.replace('%%DATA%%', json.dumps(data, ensure_ascii=False).replace('</', '<\\/'))
    page = page.replace('%%LINEAGE_TTL%%', json.dumps(lineage_ttl).replace('</', '<\\/'))
    assert '%%' not in page.replace('%%', '', 0) or not re.search(r'%%[A-Z_]+%%', page), 'unresolved placeholder'
    open(a.out, 'w', encoding='utf-8').write(page)
    print('wrote', a.out, len(page), 'bytes;', 'graph nodes:', len(data['graphs']['project']['nodes']), '+', len(data['graphs']['register']['nodes']), '; abbreviations:', len(abbr))

TEMPLATE = None  # loaded from page_template_v2_0_0.html beside this script

if __name__ == '__main__':
    main()
