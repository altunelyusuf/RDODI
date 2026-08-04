#!/usr/bin/env python3
"""Extract a complete report-data structure from the enriched ontology (structure+coverage),
computing example results mechanically (executor). Output: /tmp/report_full.json"""
import rdflib, json, sys
from rdflib import RDF, RDFS, OWL, Namespace
ONTO=sys.argv[1] if len(sys.argv)>1 else 'scp_domain_tbox_v3_16_0.ttl'
g=rdflib.Graph(); g.parse(ONTO)
def _detect_ns(graph):
    from rdflib import RDF, RDFS
    for marker in ('SemanticTechnologyArea','Area'):
        for s,p,o in graph:
            if str(o).endswith('#'+marker) and p in (RDF.type,RDFS.subClassOf):
                return Namespace(str(o).rsplit('#',1)[0]+'#'), marker
    return Namespace('http://rdodi.org/scp/domain#'),'SemanticTechnologyArea'
SCP,_MARK=_detect_ns(g)
sys.path.insert(0,'.'); exec(open('_executor.py').read())
def loc(u): return str(u).split('#')[-1]
def lbl(u): return str(g.value(u,RDFS.label) or loc(u))
def txt(u,p):
    v=g.value(u,p); return str(v) if v else ''
def jget(u,p):
    v=g.value(u,p); return json.loads(str(v)) if v else None

# area order: Foundations, W3CStack, LayeredOntology, KnowledgeGraphs
ORDER=['Foundations','W3CStack','LayeredOntology','KnowledgeGraphs']
areas=sorted(g.subjects(RDFS.subClassOf,SCP[_MARK]),
             key=lambda a: ORDER.index(loc(a)) if loc(a) in ORDER else 99)

def concept_order(a):
    # stable: by label
    return sorted(g.subjects(RDFS.subClassOf,a), key=lambda c: lbl(c))

def _meta(prop,default):
    for s in g.subjects(RDF.type,rdflib.OWL.Ontology):
        v=g.value(s,SCP[prop])
        if v: return str(v)
    return default
report={'title':_meta('pageTitle','Semantic Technologies')+' — A Pipeline-Generated Treatment',
        'subtitle':'Generated mechanically from a domain ontology',
        'areas':[],'publications':[],'axioms':{}}

for a in areas:
    A={'name':lbl(a),'short':lbl(a).split('—')[0].strip(),'intro':txt(a,SCP.extendedTreatment) or txt(a,SCP.definition),'concepts':[]}
    # area-level special: layeredArchitecture (FoundationalOntology), techCompareRich (KnowledgeGraphs)
    for c in concept_order(a):
        C={'name':lbl(c),'id':loc(c),'treatment':txt(c,SCP.extendedTreatment) or txt(c,SCP.definition),
           'examples':[],'specials':{}}
        # examples (with mechanical computation)
        for k in sorted(g.subjects(SCP.ofConcept,c),key=lambda k:txt(k,SCP.exampleDomain)):
            code=txt(k,SCP.caseCode); clang=txt(k,SCP.caseCodeLang)
            comp=None
            if code:
                try: comp=compute_result(code,clang,loc(k))
                except: comp=None
            C['examples'].append({'domain':txt(k,SCP.exampleDomain),'text':txt(k,SCP.exampleText),
                                  'code':code,'lang':clang,'computed':comp,
                                  'idgloss':jget(k,SCP.idGlossary)})
        # specials attached to the concept
        for nm,pr in [('modelComparison',SCP.modelComparison),('layeredArchitecture',SCP.layeredArchitecture),
                      ('techCompareRich',SCP.techCompareRich),('inferenceContrast',SCP.inferenceContrast),
                      ('axiomReference',SCP.axiomReference)]:
            v=jget(c,pr)
            if v: C['specials'][nm]=v
        A['concepts'].append(C)
    report['areas'].append(A)

# publications (citations) — sorted by label
for pub in sorted(g.subjects(RDF.type,SCP.Publication),key=lambda p:lbl(p)):
    report['publications'].append({
      'title':lbl(pub),
      'author':txt(pub,SCP.pubAuthor),
      'url':txt(pub,SCP.pubUrl) or txt(pub,SCP.url),
      'note':txt(pub,SCP.pubNote)})

# formal axioms summary (the enrichment)
DOMAIN_RELS=['builtOn','foundationFor','serializes','queries','validates','addsExpressivity',
             'usesVocabularyFrom','anchorsTo','anchorFor','groundsRetrievalFor','standardizedBy']
rels=[]
for s,p,o in g:
    pn=loc(p)
    if pn in DOMAIN_RELS and str(p).startswith(str(SCP)) and isinstance(o,rdflib.URIRef) and str(o).startswith(str(SCP)):
        rels.append([lbl(s),pn,lbl(o)])
disj=[[lbl(s),lbl(o)] for s,p,o in g if p==OWL.disjointWith]
report['axioms']={'relationships':sorted(rels),'disjoint':sorted(disj),
                  'object_property_count':len(list(g.subjects(RDF.type,OWL.ObjectProperty)))}

json.dump(report,open('/tmp/report_full.json','w'),ensure_ascii=False)
ne=sum(len(c['examples']) for A in report['areas'] for c in A['concepts'])
print(f"report data: {len(report['areas'])} areas, "
      f"{sum(len(A['concepts']) for A in report['areas'])} concepts, {ne} examples, "
      f"{len(report['publications'])} citations, {len(rels)} relationships, {len(disj)} disjoint axioms")
