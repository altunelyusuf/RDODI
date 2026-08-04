#!/usr/bin/env python3
"""RDODI Richness Rubric & Gate v1.0.0
Scores a domain ontology on DEPTH/RIGOR/RICHNESS (not HTML byte-size). Tells the author concretely
what is missing to reach the artifact bar we built by hand. Domain-agnostic (namespace auto-detected).

Usage:  python3 rdodi_richness_rubric_v1_0_0.py <domain_ontology.ttl> [--json]
Exit 0 if RICHNESS_MET, else 1 (with a prioritized gap list).
"""
import rdflib, sys, json
from rdflib import RDF, RDFS, OWL, Namespace

def detect(g):
    for marker in ('SemanticTechnologyArea','Area'):
        for s,p,o in g:
            if str(o).endswith('#'+marker) and p in (RDF.type,RDFS.subClassOf):
                return Namespace(str(o).rsplit('#',1)[0]+'#'), marker
    return Namespace('http://rdodi.org/scp/domain#'),'SemanticTechnologyArea'

def loc(u): return str(u).split('#')[-1]

# ---- the rubric: dimensions, weights, thresholds (grounded in the rich SCP artifact) ----
# Each check returns (score 0..1, detail, fix-hint). Artifact-level + per-concept.
def score_ontology(path):
    g=rdflib.Graph(); g.parse(path)
    NS,MARK=detect(g)
    def P(n): return NS[n]
    def val(s,n): 
        v=g.value(s,P(n)); return str(v) if v else ''
    areas=[a for a in g.subjects(RDFS.subClassOf,P(MARK)) if isinstance(a,rdflib.URIRef)]
    concepts=[c for a in areas for c in g.subjects(RDFS.subClassOf,a) if isinstance(c,rdflib.URIRef)]
    specials=['modelComparison','layeredArchitecture','techCompareRich','inferenceContrast','idGlossary',
              'primerData','crossTech','axiomReference']
    report={'dimensions':[], 'per_concept':[], 'gaps':[]}

    def dim(name,weight,score,detail,fix):
        report['dimensions'].append({'name':name,'weight':weight,'score':round(score,2),'detail':detail})
        if score<0.7 and fix: report['gaps'].append({'priority':round((1-score)*weight,2),'dimension':name,'fix':fix})
        return weight*score

    total=0; maxw=0
    # D1 — Coverage: enough concepts, all with treatment
    nC=len(concepts)
    with_treat=sum(1 for c in concepts if len(val(c,'extendedTreatment') or val(c,'definition'))>=200)
    s=min(1.0, nC/12) * (with_treat/nC if nC else 0)
    maxw+=20; total+=dim('Coverage',20,s,f'{nC} concepts, {with_treat} with >=200-char treatment',
        f'Add concepts (>=12) and ensure every concept has a >=200-char extendedTreatment' if s<0.7 else None)

    # D2 — Treatment depth: median treatment length (rich artifact median ~346)
    tl=[len(val(c,'extendedTreatment') or val(c,'definition')) for c in concepts] or [0]
    med=sorted(tl)[len(tl)//2]
    s=min(1.0, med/300)
    maxw+=15; total+=dim('Treatment depth',15,s,f'median treatment {med} chars',
        f'Deepen treatments to a multi-sentence explanation (target >=300 chars median)' if s<0.7 else None)

    # D3 — Worked examples: examples per concept + multi-domain breadth
    exper=[len(list(g.subjects(P('ofConcept'),c))) for c in concepts] or [0]
    have_ex=sum(1 for e in exper if e>=1)
    s=have_ex/len(concepts) if concepts else 0
    maxw+=15; total+=dim('Worked examples',15,s,f'{have_ex}/{nC} concepts have >=1 example',
        f'Add a worked example for every concept (the {nC-have_ex} without one)' if s<0.7 else None)

    # D4 — Executable/computed examples: fraction of code examples that are mechanically executable
    code_ex=[k for k in g.subjects(P('ofConcept'),None) if val(k,'caseCode')]
    rdf_ex=[k for k in code_ex if val(k,'caseCodeLang').lower() in ('turtle','rdf','sparql')]
    s=min(1.0, len(rdf_ex)/max(1,len(code_ex)))
    maxw+=10; total+=dim('Executable examples',10,s,f'{len(rdf_ex)}/{len(code_ex)} examples are RDF/SPARQL (executable)',
        'Prefer executable RDF/SPARQL examples so results can be computed, not hand-written' if s<0.7 else None)

    # D5 — Special features (comparisons/diagrams): concepts carrying >=1 rich feature
    cw=sum(1 for c in concepts if any(g.value(c,P(sp)) for sp in specials))
    s=min(1.0, cw/max(1,nC*0.2))   # rich artifact had ~6/31 ~= 0.19; reward >=20% of concepts
    maxw+=15; total+=dim('Rich features',15,s,f'{cw}/{nC} concepts carry a special feature (comparison/diagram/etc.)',
        'Add rich features (modelComparison, techCompareRich, layeredArchitecture, inferenceContrast) to key concepts' if s<0.7 else None)

    # D6 — Formal axiomatization: object properties + disjointness + consistency
    op=len(list(g.subjects(RDF.type,OWL.ObjectProperty)))
    dj=len([1 for s,p,o in g if p==OWL.disjointWith])
    # domain-agnostic: count assertions that use any domain-defined ObjectProperty (not a fixed name list),
    # excluding the structural 'ofConcept' plumbing property
    _domain_oprops={op for op in g.subjects(RDF.type,OWL.ObjectProperty)
                    if str(op).startswith(str(NS)) and loc(op) not in ('ofConcept','relatedConcept','resourceLink')}
    rels=len([1 for s,p,o in g if p in _domain_oprops and isinstance(o,rdflib.URIRef)
              and isinstance(s,rdflib.URIRef) and str(s).startswith(str(NS))])
    s=min(1.0,(min(op,10)/10*0.4 + min(rels,15)/15*0.4 + min(dj,3)/3*0.2))
    maxw+=10; total+=dim('Formal axioms',10,s,f'{op} object props, {rels} asserted relations, {dj} disjoint axioms',
        'Add domain object properties + assert concept relationships + disjointness axioms' if s<0.7 else None)

    # D7 — Citations: count + URL coverage
    pubs=list(g.subjects(RDF.type,P('Publication')))
    withurl=sum(1 for p in pubs if val(p,'pubUrl') or val(p,'url'))
    s=min(1.0, len(pubs)/10) * (withurl/len(pubs) if pubs else 0)
    maxw+=8; total+=dim('Citations',8,s,f'{len(pubs)} publications, {withurl} with URLs',
        'Add cited sources (target >=10) each with a verifiable URL' if s<0.7 else None)

    # D8 — Self-check quiz: present + sized + typed
    qb=g.value(P('quizBank'),P('quizBank'))
    qn=0; types=set()
    if qb:
        try:
            q=json.loads(str(qb)); qn=len(q); types={x.get('type') for x in q}
        except: pass
    s=min(1.0, qn/15) * (min(1.0,len(types)/2))
    maxw+=7; total+=dim('Self-check quiz',7,s,f'{qn} questions, types={sorted(t for t in types if t)}',
        'Add a comprehensive quiz (>=15 questions, mixing deduction + concept + spot-the-error)' if s<0.7 else None)

    pct=round(100*total/maxw,1)
    # per-concept depth flags (which concepts are thin)
    for c in concepts:
        tlen=len(val(c,'extendedTreatment') or val(c,'definition'))
        ne=len(list(g.subjects(P('ofConcept'),c)))
        nsp=sum(1 for sp in specials if g.value(c,P(sp)))
        flags=[]
        if tlen<200: flags.append('thin-treatment')
        if ne<1: flags.append('no-example')
        report['per_concept'].append({'concept':loc(c),'treatment_chars':tlen,'examples':ne,'features':nsp,'flags':flags})

    report['gaps'].sort(key=lambda x:-x['priority'])
    report['score_pct']=pct
    report['verdict']='RICHNESS_MET' if pct>=75 else 'BELOW_BAR'
    report['threshold']=75
    return report

if __name__=='__main__':
    if len(sys.argv)<2:
        print("usage: rdodi_richness_rubric_v1_0_0.py <ontology.ttl> [--json]"); sys.exit(2)
    r=score_ontology(sys.argv[1])
    if '--json' in sys.argv:
        print(json.dumps(r,indent=1)); sys.exit(0 if r['verdict']=='RICHNESS_MET' else 1)
    print(f"\n=== RICHNESS RUBRIC — {sys.argv[1]} ===")
    print(f"OVERALL: {r['score_pct']}% / 100   ->  {r['verdict']} (threshold {r['threshold']}%)\n")
    print(f"{'DIMENSION':<22}{'WEIGHT':>7}{'SCORE':>7}   DETAIL")
    for d in r['dimensions']:
        print(f"{d['name']:<22}{d['weight']:>7}{d['score']:>7}   {d['detail']}")
    thin=[p for p in r['per_concept'] if p['flags']]
    print(f"\nPER-CONCEPT: {len(r['per_concept'])} concepts, {len(thin)} flagged thin")
    for p in thin[:10]:
        print(f"  - {p['concept']}: {', '.join(p['flags'])} (treatment {p['treatment_chars']}ch, {p['examples']} ex)")
    if r['gaps']:
        print(f"\nPRIORITIZED GAPS (what to fix to reach the bar):")
        for gp in r['gaps']:
            print(f"  [{gp['priority']:>4}] {gp['dimension']}: {gp['fix']}")
    sys.exit(0 if r['verdict']=='RICHNESS_MET' else 1)
