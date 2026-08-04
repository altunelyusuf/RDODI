"""Build-time executors: compute exec results MECHANICALLY from actual code. result == code output."""
import rdflib, re
from rdflib import Graph, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import SKOS
import owlrl
OWL=Namespace('http://www.w3.org/2002/07/owl#')
STD={'':'http://ex.org/','ex':'http://ex.org/','owl':'http://www.w3.org/2002/07/owl#',
 'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#','rdfs':'http://www.w3.org/2000/01/rdf-schema#',
 'xsd':'http://www.w3.org/2001/XMLSchema#','skos':'http://www.w3.org/2004/02/skos/core#',
 'schema':'http://schema.org/','sh':'http://www.w3.org/ns/shacl#','prov':'http://www.w3.org/ns/prov#',
 'foaf':'http://xmlns.com/foaf/0.1/','dcterms':'http://purl.org/dc/terms/','bfo':'http://purl.obolibrary.org/obo/'}

def _hdr(code):
    decl=set(re.findall(r'@prefix\s+([\w]*):',code)); out=''
    if re.search(r'(?<![\w]):[A-Za-z]',code) and ':' not in decl: out+=f"@prefix : <{STD['']}> .\n"
    for u in sorted(set(re.findall(r'(\b[a-z][\w]*):[A-Za-z]',code))):
        if u in STD and u not in decl: out+=f"@prefix {u}: <{STD[u]}> .\n"
    return out

def _load(code):
    g=Graph(); g.parse(data=_hdr(code)+code,format='turtle'); return g
def _n3(g,t):
    try:
        s=t.n3(g.namespace_manager)
        return s
    except: return str(t)
def _clean(g,t):
    # render as prefix:local, dropping junk
    s=_n3(g,t)
    return s

def exec_skos_resolution(code):
    if 'skos:Concept' not in code: return None
    g=_load(code); rows=[]
    for c in sorted(g.subjects(RDF.type,SKOS.Concept),key=str):
        cn=_n3(g,c)
        for prop in (SKOS.prefLabel,SKOS.altLabel,SKOS.hiddenLabel):
            for lbl in g.objects(c,prop):
                lang=f" ({lbl.language})" if getattr(lbl,'language',None) else ""
                rows.append([f'"{lbl}"{lang}', cn])
    if not rows: return None
    steps=['Parse the Turtle into a graph']+[f'Index label {r[0]} → {r[1]}' for r in rows]+['Any of these queries now resolves to the concept']
    return {'cols':['query (label)','resolves to'],'rows':rows,'steps':steps}

def exec_owl_inverse(code):
    if 'owl:inverseOf' not in code: return None
    g=_load(code); base=set(g)
    # find the inverseOf pair and the asserted edge, compute the inverse manually (clean, no owlrl noise)
    pairs=[(s,o) for s,p,o in g if p==OWL.inverseOf]
    rows=[]
    for s,p,o in base:
        if isinstance(s,URIRef) and isinstance(o,URIRef) and p not in (RDF.type,OWL.inverseOf):
            rows.append([f"{_n3(g,s)} {_n3(g,p)} {_n3(g,o)}",'asserted'])
            for a,b in pairs:
                if p==a:
                    rows.append([f"{_n3(g,o)} {_n3(g,b)} {_n3(g,s)}",'inferred'])
                elif p==b:
                    rows.append([f"{_n3(g,o)} {_n3(g,a)} {_n3(g,s)}",'inferred'])
    if not any(r[1]=='inferred' for r in rows): return None
    steps=['Parse the Turtle into a graph','Read the owl:inverseOf axiom']+[f'{r[1].capitalize()}: {r[0]}' for r in rows]
    return {'cols':['fact','origin'],'rows':rows,'steps':steps}

def exec_rdfs_subclass(code):
    # only for examples whose POINT is subclass inference (have subClassOf AND an individual typed at a leaf)
    if 'rdfs:subClassOf' not in code or ' a ' not in code: return None
    g=_load(code); base=set(g)
    try: owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)
    except Exception: return None
    rows=[]
    for s,o in [(s,o) for s,p,o in g if p==RDF.type and (s,p,o) not in base
                and isinstance(o,URIRef) and isinstance(s,URIRef)
                and str(RDFS) not in str(o) and str(RDF) not in str(o) and str(OWL) not in str(o)]:
        rows.append([_n3(g,s),_n3(g,o),'inferred'])
    # also include the asserted type for context
    asserted=[[_n3(g,s),_n3(g,o),'asserted'] for s,p,o in base if p==RDF.type and isinstance(o,URIRef)]
    allrows=asserted+sorted(rows)
    if not rows: return None
    steps=['Parse the Turtle into a graph','Apply RDFS subclass closure']+[f'{r[2].capitalize()}: {r[0]} is a {r[1]}' for r in allrows]
    return {'cols':['individual','type','origin'],'rows':allrows,'steps':steps}

# Only these concept examples are mechanically executed; others stay representative (honest).
EXECUTORS=[exec_skos_resolution, exec_owl_inverse, exec_rdfs_subclass]

# Cases whose stored result is a CURATED conceptual breakdown (not a raw code output) — never override.
CONCEPTUAL_RESULT_CASES={'case_TBoxABoxRBox_0','case_TBoxABoxRBox_1'}

def compute_result(code, lang, case_id=None):
    if case_id in CONCEPTUAL_RESULT_CASES: return None
    if lang and lang.lower() not in ('turtle','rdf','ttl'): return None
    for ex in EXECUTORS:
        try:
            r=ex(code)
            if r and r['rows']: return r
        except Exception:
            continue
    return None
