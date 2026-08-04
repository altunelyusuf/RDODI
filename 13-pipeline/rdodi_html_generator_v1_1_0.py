#!/usr/bin/env python3
"""
gen_render_deployed_v2_0_0.py — RDODI deployed-bar generation driver, enhanced.
Adds (all GENERATED from the ontology, R12 fidelity-traced):
  - SPA multi-subpage navigation (top menu switches area-pages; no long scroll)
  - MS-Explorer collapsible tree (click folder to open/close) from the class hierarchy
  - example callouts from scp:example
  - concept-diagram SVGs from scp:hasVisual (triple/pattern/shape/ragflow/tiers/synonyms)
  - reframed SHORT tables (2 cols, narrative-adjacent) instead of long ones
  - hover tooltips on concept terms (definition) and right-click context menus (definition/source/copy)
Usage: python3 gen_render_deployed_v2_0_0.py <onto_dir>
"""
import rdflib, html, json, sys, os, re
from rdflib import OWL, RDF, RDFS, Namespace, Literal
from rdflib.namespace import SKOS, DCTERMS

# ---- strict-notation diagrams (clean hand-built SVG) ----
# Clean, legible strict-notation diagrams (hand-built SVG, orthogonal routing).
def _hh(s): 
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def strict_erd():
    # two entity tables, clean FK line + clean self-loop, legible cardinality (crow's foot drawn cleanly)
    return ('<svg class="mc-svg" viewBox="0 0 380 200" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica,Arial,sans-serif">'
      # PRODUCT table
      '<g>'
      '<rect x="14" y="40" width="120" height="20" fill="#4a7c8c"/>'
      '<text x="74" y="54" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold">PRODUCT</text>'
      '<rect x="14" y="60" width="120" height="19" fill="#fff" stroke="#7a8a92"/><text x="20" y="73" font-size="10"><tspan text-decoration="underline">PK</tspan> id</text>'
      '<rect x="14" y="79" width="120" height="19" fill="#fff" stroke="#7a8a92"/><text x="20" y="92" font-size="10">name</text>'
      '<rect x="14" y="98" width="120" height="19" fill="#fff" stroke="#7a8a92"/><text x="20" y="111" font-size="10" fill="#b5803a">FK category_id</text>'
      '</g>'
      # CATEGORY table
      '<g>'
      '<rect x="236" y="40" width="128" height="20" fill="#5b8a72"/>'
      '<text x="300" y="54" text-anchor="middle" fill="#fff" font-size="11" font-weight="bold">CATEGORY</text>'
      '<rect x="236" y="60" width="128" height="19" fill="#fff" stroke="#7a8a92"/><text x="242" y="73" font-size="10"><tspan text-decoration="underline">PK</tspan> id</text>'
      '<rect x="236" y="79" width="128" height="19" fill="#fff" stroke="#7a8a92"/><text x="242" y="92" font-size="10">name</text>'
      '<rect x="236" y="98" width="128" height="19" fill="#fff" stroke="#7a8a92"/><text x="242" y="111" font-size="10" fill="#b5803a">FK parent_id</text>'
      '</g>'
      # FK relationship product.category_id -> category.id  (clean orthogonal line, crow's foot at PRODUCT/many side)
      '<g stroke="#444" stroke-width="1.3" fill="none">'
      '<path d="M134,107 H236"/>'
      # crow's foot (many) at the product end
      '<path d="M148,107 L134,101 M148,107 L134,107 M148,107 L134,113"/>'
      # single bar (one) at the category end
      '<path d="M224,101 V113"/>'
      '</g>'
      '<text x="158" y="103" font-size="9" fill="#586272">N</text>'
      '<text x="214" y="103" font-size="9" fill="#586272">1</text>'
      '<text x="185" y="100" text-anchor="middle" font-size="8.5" fill="#586272">belongs to</text>'
      # self-referencing parent_id (clean loop above CATEGORY)
      '<g stroke="#b5803a" stroke-width="1.3" fill="none">'
      '<path d="M300,40 V26 H352 V60"/>'
      '<path d="M352,60 L347,54 M352,60 L352,54 M352,60 L357,54"/>'
      '</g>'
      '<text x="300" y="20" text-anchor="middle" font-size="7.5" fill="#b5803a">parent_id (self-ref = hierarchy)</text>'
      '<text x="14" y="140" font-size="9.5" fill="#586272">Hierarchy = recursive parent_id; reading ancestors needs a recursive CTE.</text>'
      '</svg>')

def strict_uml_class():
    return ('<svg class="mc-svg" viewBox="0 0 380 190" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica,Arial,sans-serif">'
      # Product class box (3 compartments)
      '<g>'
      '<rect x="20" y="46" width="130" height="60" fill="#fff" stroke="#5b8a72" stroke-width="1.4"/>'
      '<line x1="20" y1="66" x2="150" y2="66" stroke="#5b8a72"/><line x1="20" y1="86" x2="150" y2="86" stroke="#5b8a72"/>'
      '<text x="85" y="60" text-anchor="middle" font-size="11" font-weight="bold">Product</text>'
      '<text x="26" y="80" font-size="9.5">- name : String</text>'
      '<text x="26" y="100" font-size="9.5">- category</text>'
      '</g>'
      # Category class box
      '<g>'
      '<rect x="230" y="46" width="130" height="60" fill="#fff" stroke="#5b8a72" stroke-width="1.4"/>'
      '<line x1="230" y1="66" x2="360" y2="66" stroke="#5b8a72"/><line x1="230" y1="86" x2="360" y2="86" stroke="#5b8a72"/>'
      '<text x="295" y="60" text-anchor="middle" font-size="11" font-weight="bold">Category</text>'
      '<text x="236" y="80" font-size="9.5">- name : String</text>'
      '<text x="236" y="100" font-size="9.5">- parent</text>'
      '</g>'
      # association Product -> Category (clean, open arrow), multiplicities
      '<g stroke="#444" stroke-width="1.3" fill="none"><path d="M150,76 H230"/></g>'
      '<path d="M222,71 L230,76 L222,81" fill="none" stroke="#444" stroke-width="1.3"/>'
      '<text x="158" y="72" font-size="9" fill="#586272">1</text>'
      '<text x="218" y="72" font-size="9" fill="#586272">1</text>'
      '<text x="190" y="71" text-anchor="middle" font-size="8.5" fill="#586272">category</text>'
      # self-association parent (clean loop above Category)
      '<g stroke="#444" stroke-width="1.3" fill="none"><path d="M270,46 V30 H340 V44"/></g>'
      '<path d="M335,44 L340,50 L345,44" fill="none" stroke="#444" stroke-width="1.3"/>'
      '<text x="305" y="26" text-anchor="middle" font-size="8.5" fill="#586272">parent 0..1</text>'
      '<text x="20" y="135" font-size="9.5" fill="#586272">Category references its own parent (self-association);</text>'
      '<text x="20" y="149" font-size="9.5" fill="#586272">the hierarchy is a chain of object references.</text>'
      '</svg>')

def strict_uml_object():
    # MS-Explorer / directory-style TREE of the category taxonomy with product leaves
    rows=[
      (0,'folder','Root'),
      (1,'folder','Clothing'),
      (2,'folder',"Women's T-Shirt"),
      (3,'file','tshirt_A : Product'),
      (3,'file','tshirt_B : Product'),
      (2,'folder',"Men's Shirt"),
      (3,'file','shirt_C : Product'),
    ]
    parts=['<svg class="mc-svg" viewBox="0 0 380 215" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica,Arial,sans-serif">']
    y=24; x0=16; step=22; indent=26
    # draw connector guide lines (tree) + nodes
    prev_y_at_depth={}
    for depth,kind,label in rows:
        x=x0+depth*indent
        cy=y
        # vertical/horizontal tree connector from parent
        if depth>0:
            px=x0+(depth-1)*indent+8
            parts.append(f'<path d="M{px},{prev_y_at_depth.get(depth-1,cy)-0} L{px},{cy} L{x-4},{cy}" fill="none" stroke="#b9c2c8" stroke-width="1"/>')
        prev_y_at_depth[depth]=cy
        if kind=='folder':
            parts.append(f'<rect x="{x}" y="{cy-9}" width="14" height="11" rx="1.5" fill="#e7c873" stroke="#bfa24a"/>')
            parts.append(f'<rect x="{x}" y="{cy-11}" width="7" height="3" rx="1" fill="#e7c873" stroke="#bfa24a"/>')
            parts.append(f'<text x="{x+20}" y="{cy}" font-size="10.5" font-weight="bold" fill="#3a4750">{_hh(label)}</text>')
        else:
            parts.append(f'<rect x="{x}" y="{cy-9}" width="11" height="13" rx="1" fill="#fff" stroke="#9a5b6e"/>')
            parts.append(f'<path d="M{x+7},{cy-9} L{x+11},{cy-5} L{x+7},{cy-5} Z" fill="#d8c0c8"/>')
            parts.append(f'<text x="{x+17}" y="{cy}" font-size="10" fill="#7a3b4e">{_hh(label)}</text>')
        y+=step
    parts.append(f'<text x="16" y="{y+10}" font-size="9.5" fill="#586272">Category hierarchy as a directory tree; products are leaves under their category.</text>')
    parts.append('</svg>')
    return ''.join(parts)

def strict_semantic():
    # TWO branching TREES: class hierarchy (left) + category taxonomy (right), individuals as leaves.
    # Designed so the TAXONOMY reads as a tree (a parent fanning out to children).
    return ('<svg class="mc-svg" viewBox="0 0 400 330" xmlns="http://www.w3.org/2000/svg" font-family="Helvetica,Arial,sans-serif">'
      '<defs>'
      '<marker id="arc" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#5b8a72"/></marker>'
      '<marker id="art" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#4a7c8c"/></marker>'
      '<marker id="arx" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#999"/></marker>'
      '</defs>'
      # ============ LEFT: CLASS hierarchy tree (rdfs:subClassOf) ============
      '<text x="100" y="14" text-anchor="middle" font-size="9" font-weight="bold" fill="#5b8a72">Class hierarchy (rdfs:subClassOf)</text>'
      # :Product (root)
      '<rect x="58" y="24" width="84" height="22" rx="11" fill="#eef4f0" stroke="#5b8a72"/><text x="100" y="39" text-anchor="middle" font-size="9">:Product</text>'
      # :Clothing (child)
      '<rect x="58" y="74" width="84" height="22" rx="11" fill="#eef4f0" stroke="#5b8a72"/><text x="100" y="89" text-anchor="middle" font-size="9">:Clothing</text>'
      # :TShirt and :Shirt (two children -> BRANCHING)
      '<rect x="18" y="128" width="74" height="22" rx="11" fill="#eef4f0" stroke="#5b8a72"/><text x="55" y="143" text-anchor="middle" font-size="9">:TShirt</text>'
      '<rect x="110" y="128" width="74" height="22" rx="11" fill="#eef4f0" stroke="#5b8a72"/><text x="147" y="143" text-anchor="middle" font-size="9">:Shirt</text>'
      # subClassOf edges (child -> parent, pointing UP), with a branch under Clothing
      '<g stroke="#5b8a72" stroke-width="1.2" fill="none">'
      '<path d="M100,74 V46" marker-end="url(#arc)"/>'                       # Clothing -> Product
      '<path d="M55,128 V112 H100 V96" marker-end="url(#arc)"/>'            # TShirt -> Clothing (branch)
      '<path d="M147,128 V112 H100" marker-end="url(#arc)"/>'               # Shirt  -> Clothing (branch)
      '</g>'
      # ============ RIGHT: CATEGORY taxonomy tree (skos:broader) ============
      '<text x="300" y="14" text-anchor="middle" font-size="9" font-weight="bold" fill="#4a7c8c">Category taxonomy (skos:broader)</text>'
      # root_cat
      '<rect x="258" y="24" width="84" height="22" rx="4" fill="#fff" stroke="#4a7c8c"/><text x="300" y="39" text-anchor="middle" font-size="8.5">ex:root_cat</text>'
      # clothing_cat
      '<rect x="252" y="74" width="96" height="22" rx="4" fill="#fff" stroke="#4a7c8c"/><text x="300" y="89" text-anchor="middle" font-size="8.5">ex:clothing_cat</text>'
      # womenTshirt_cat + menShirt_cat (two children -> BRANCHING = the taxonomy shape)
      '<rect x="206" y="128" width="92" height="22" rx="4" fill="#fff" stroke="#4a7c8c"/><text x="252" y="143" text-anchor="middle" font-size="7.5">ex:womenTshirt_cat</text>'
      '<rect x="312" y="128" width="84" height="22" rx="4" fill="#fff" stroke="#4a7c8c"/><text x="354" y="143" text-anchor="middle" font-size="7.5">ex:menShirt_cat</text>'
      '<g stroke="#4a7c8c" stroke-width="1.2" fill="none">'
      '<path d="M300,74 V46" marker-end="url(#art)"/>'                      # clothing -> root
      '<path d="M252,128 V112 H300 V96" marker-end="url(#art)"/>'          # women -> clothing (branch)
      '<path d="M354,128 V112 H300" marker-end="url(#art)"/>'             # men   -> clothing (branch)
      '</g>'
      # ============ INDIVIDUALS as LEAVES under their category ============
      '<ellipse cx="222" cy="188" rx="38" ry="15" fill="#fbeef2" stroke="#9a5b6e"/><text x="222" y="190" text-anchor="middle" font-size="8.5">ex:tshirt_A</text><text x="222" y="199" text-anchor="middle" font-size="6.5" fill="#9a5b6e">a :TShirt</text>'
      '<ellipse cx="222" cy="224" rx="38" ry="15" fill="#fbeef2" stroke="#9a5b6e"/><text x="222" y="226" text-anchor="middle" font-size="8.5">ex:tshirt_B</text><text x="222" y="235" text-anchor="middle" font-size="6.5" fill="#9a5b6e">a :TShirt</text>'
      '<ellipse cx="354" cy="188" rx="36" ry="14" fill="#fbeef2" stroke="#9a5b6e"/><text x="354" y="190" text-anchor="middle" font-size="8.5">ex:shirt_C</text><text x="354" y="199" text-anchor="middle" font-size="6.5" fill="#9a5b6e">a :Shirt</text>'
      # inCategory links (leaf -> its category concept), short and downward from the concept
      '<g stroke="#9a5b6e" stroke-width="1.1" fill="none">'
      '<path d="M240,174 C250,165 252,158 252,150" marker-end="url(#arx)" stroke="#9a5b6e"/>'
      '<path d="M232,212 C246,205 252,165 252,150" marker-end="url(#arx)" stroke="#9a5b6e"/>'
      '<path d="M354,174 V150" marker-end="url(#arx)" stroke="#9a5b6e"/>'
      '</g>'
      '<text x="258" y="172" font-size="7.5" fill="#9a5b6e" text-anchor="middle">:inCategory</text>'

      # caption
      '<text x="14" y="270" font-size="8.5" fill="#586272">Each hierarchy is a TREE: a parent concept branches to its children.</text>'
      '<text x="14" y="283" font-size="8.5" fill="#586272">tshirt_A and tshirt_B are two individuals of the same class :TShirt,</text>'
      '<text x="14" y="296" font-size="8.5" fill="#586272">each placed in the taxonomy via :inCategory.</text>'
      '</svg>')

_STRICT={'erd':strict_erd,'class':strict_uml_class,'object':strict_uml_object,'semantic':strict_semantic}


def loc(n): return str(n).split('#')[-1].split('/')[-1]
SCP=Namespace('http://rdodi.org/scp/domain#')
def _detect_ns(graph):
    # domain-agnostic: find the namespace whose '#Area' or '#SemanticTechnologyArea' class is used as an area marker
    from rdflib import RDF, RDFS
    for marker in ('SemanticTechnologyArea','Area'):
        for s,p,o in graph:
            if str(o).endswith('#'+marker) and p==RDF.type:
                return Namespace(str(o).rsplit('#',1)[0]+'#'), marker
        # also areas declared as subClassOf the marker
        for s,p,o in graph:
            if p==RDFS.subClassOf and str(o).endswith('#'+marker):
                return Namespace(str(o).rsplit('#',1)[0]+'#'), marker
    # v1.0.1 FIX (was: silent `return SCP,'SemanticTechnologyArea'`): a domain with
    # neither marker class is not the SCP domain in disguise -- defaulting to SCP's
    # namespace here silently mislabeled every such domain's area markers. Fail
    # stop instead, per the HONEST STOP convention used elsewhere in this pipeline
    # (see rdodi_artifact_generator_v2_6_0.py's detect_domain).
    raise SystemExit(
        "HONEST STOP: no 'SemanticTechnologyArea' or 'Area' marker class found in this "
        "domain (checked both rdf:type and rdfs:subClassOf). Cannot safely guess the "
        "domain's namespace -- refusing to silently default to the SCP namespace."
    )

# ===== embedded RDODI example executor (mechanical result computation) =====
import owlrl as _owlrl_check
_EXECUTOR_NS={}
exec('"""Build-time executors: compute exec results MECHANICALLY from actual code. result == code output."""\nimport rdflib, re\nfrom rdflib import Graph, Namespace, RDF, RDFS, URIRef\nfrom rdflib.namespace import SKOS\nimport owlrl\nOWL=Namespace(\'http://www.w3.org/2002/07/owl#\')\nSTD={\'\':\'http://ex.org/\',\'ex\':\'http://ex.org/\',\'owl\':\'http://www.w3.org/2002/07/owl#\',\n \'rdf\':\'http://www.w3.org/1999/02/22-rdf-syntax-ns#\',\'rdfs\':\'http://www.w3.org/2000/01/rdf-schema#\',\n \'xsd\':\'http://www.w3.org/2001/XMLSchema#\',\'skos\':\'http://www.w3.org/2004/02/skos/core#\',\n \'schema\':\'http://schema.org/\',\'sh\':\'http://www.w3.org/ns/shacl#\',\'prov\':\'http://www.w3.org/ns/prov#\',\n \'foaf\':\'http://xmlns.com/foaf/0.1/\',\'dcterms\':\'http://purl.org/dc/terms/\',\'bfo\':\'http://purl.obolibrary.org/obo/\'}\n\ndef _hdr(code):\n    decl=set(re.findall(r\'@prefix\\s+([\\w]*):\',code)); out=\'\'\n    if re.search(r\'(?<![\\w]):[A-Za-z]\',code) and \':\' not in decl: out+=f"@prefix : <{STD[\'\']}> .\\n"\n    for u in sorted(set(re.findall(r\'(\\b[a-z][\\w]*):[A-Za-z]\',code))):\n        if u in STD and u not in decl: out+=f"@prefix {u}: <{STD[u]}> .\\n"\n    return out\n\ndef _load(code):\n    g=Graph(); g.parse(data=_hdr(code)+code,format=\'turtle\'); return g\ndef _n3(g,t):\n    try:\n        s=t.n3(g.namespace_manager)\n        return s\n    except: return str(t)\ndef _clean(g,t):\n    # render as prefix:local, dropping junk\n    s=_n3(g,t)\n    return s\n\ndef exec_skos_resolution(code):\n    if \'skos:Concept\' not in code: return None\n    g=_load(code); rows=[]\n    for c in sorted(g.subjects(RDF.type,SKOS.Concept),key=str):\n        cn=_n3(g,c)\n        for prop in (SKOS.prefLabel,SKOS.altLabel,SKOS.hiddenLabel):\n            for lbl in g.objects(c,prop):\n                lang=f" ({lbl.language})" if getattr(lbl,\'language\',None) else ""\n                rows.append([f\'"{lbl}"{lang}\', cn])\n    if not rows: return None\n    steps=[\'Parse the Turtle into a graph\']+[f\'Index label {r[0]} → {r[1]}\' for r in rows]+[\'Any of these queries now resolves to the concept\']\n    return {\'cols\':[\'query (label)\',\'resolves to\'],\'rows\':rows,\'steps\':steps}\n\ndef exec_owl_inverse(code):\n    if \'owl:inverseOf\' not in code: return None\n    g=_load(code); base=set(g)\n    # find the inverseOf pair and the asserted edge, compute the inverse manually (clean, no owlrl noise)\n    pairs=[(s,o) for s,p,o in g if p==OWL.inverseOf]\n    rows=[]\n    for s,p,o in base:\n        if isinstance(s,URIRef) and isinstance(o,URIRef) and p not in (RDF.type,OWL.inverseOf):\n            rows.append([f"{_n3(g,s)} {_n3(g,p)} {_n3(g,o)}",\'asserted\'])\n            for a,b in pairs:\n                if p==a:\n                    rows.append([f"{_n3(g,o)} {_n3(g,b)} {_n3(g,s)}",\'inferred\'])\n                elif p==b:\n                    rows.append([f"{_n3(g,o)} {_n3(g,a)} {_n3(g,s)}",\'inferred\'])\n    if not any(r[1]==\'inferred\' for r in rows): return None\n    steps=[\'Parse the Turtle into a graph\',\'Read the owl:inverseOf axiom\']+[f\'{r[1].capitalize()}: {r[0]}\' for r in rows]\n    return {\'cols\':[\'fact\',\'origin\'],\'rows\':rows,\'steps\':steps}\n\ndef exec_rdfs_subclass(code):\n    # only for examples whose POINT is subclass inference (have subClassOf AND an individual typed at a leaf)\n    if \'rdfs:subClassOf\' not in code or \' a \' not in code: return None\n    g=_load(code); base=set(g)\n    try: owlrl.DeductiveClosure(owlrl.RDFS_Semantics).expand(g)\n    except Exception: return None\n    rows=[]\n    for s,o in [(s,o) for s,p,o in g if p==RDF.type and (s,p,o) not in base\n                and isinstance(o,URIRef) and isinstance(s,URIRef)\n                and str(RDFS) not in str(o) and str(RDF) not in str(o) and str(OWL) not in str(o)]:\n        rows.append([_n3(g,s),_n3(g,o),\'inferred\'])\n    # also include the asserted type for context\n    asserted=[[_n3(g,s),_n3(g,o),\'asserted\'] for s,p,o in base if p==RDF.type and isinstance(o,URIRef)]\n    allrows=asserted+sorted(rows)\n    if not rows: return None\n    steps=[\'Parse the Turtle into a graph\',\'Apply RDFS subclass closure\']+[f\'{r[2].capitalize()}: {r[0]} is a {r[1]}\' for r in allrows]\n    return {\'cols\':[\'individual\',\'type\',\'origin\'],\'rows\':allrows,\'steps\':steps}\n\n# Only these concept examples are mechanically executed; others stay representative (honest).\nEXECUTORS=[exec_skos_resolution, exec_owl_inverse, exec_rdfs_subclass]\n\n# Cases whose stored result is a CURATED conceptual breakdown (not a raw code output) — never override.\nCONCEPTUAL_RESULT_CASES={\'case_TBoxABoxRBox_0\',\'case_TBoxABoxRBox_1\'}\n\ndef compute_result(code, lang, case_id=None):\n    if case_id in CONCEPTUAL_RESULT_CASES: return None\n    if lang and lang.lower() not in (\'turtle\',\'rdf\',\'ttl\'): return None\n    for ex in EXECUTORS:\n        try:\n            r=ex(code)\n            if r and r[\'rows\']: return r\n        except Exception:\n            continue\n    return None\n', _EXECUTOR_NS)
_exec_compute=_EXECUTOR_NS["compute_result"]
# ==========================================================================
TODAY="2026-06-18"
ONTO=sys.argv[1] if len(sys.argv)>1 else "/home/claude/scp_pipeline/scp_domain_tbox_v3_15_0.ttl"
# domain-agnostic IO: accept either a .ttl file path (preferred) or a legacy directory
import os as _os
if _os.path.isdir(ONTO):
    ONTO_FILE=ONTO+"/scp_domain_tbox_v3_15_0.ttl"; OUT=ONTO+"/render_v30"
else:
    ONTO_FILE=ONTO
    OUT=(sys.argv[2] if len(sys.argv)>2 else _os.path.join(_os.path.dirname(ONTO_FILE) or ".","render_out"))
g=rdflib.Graph(); g.parse(ONTO_FILE)
SCP,_AREA_MARKER=_detect_ns(g)   # domain-agnostic namespace + area-class detection
_os.makedirs(OUT,exist_ok=True)
# domain-agnostic page metadata (from ontology, with fallbacks)
def _meta(prop,default):
    for s in g.subjects(rdflib.RDF.type, rdflib.OWL.Ontology):
        v=g.value(s,SCP[prop])
        if v: return str(v)
    # also accept on the Area-marker class
    v=g.value(SCP[_AREA_MARKER],SCP[prop])
    return str(v) if v else default
_OUTNAME=_os.path.splitext(_os.path.basename(ONTO_FILE))[0]+"_page.html"
_PAGE_TITLE=_meta('pageTitle','Semantic Technologies')
_PAGE_SUBTITLE=_meta('pageSubtitle','pipeline-generated')
_COMPARE_LABEL=_meta('compareLabel','Traditional vs Semantic')
_COMPARE_SHORT=_meta('compareShort','Trad. vs Sem.')
_TAXONOMY_LABEL=_meta('taxonomyLabel','Taxonomies')
EXT=SCP.extendedTreatment; EX=SCP.example; VIS=SCP.hasVisual

classes=set(g.subjects(RDF.type,OWL.Class)); inds=set(g.subjects(RDF.type,OWL.NamedIndividual))
def label(c):
    l=g.value(c,RDFS.label); return str(l) if l else re.sub(r'(?<=[a-z])(?=[A-Z])',' ',loc(c))
def defn(c): d=g.value(c,SKOS.definition); return str(d) if d else ""
def ext(c): e=g.value(c,EXT); return str(e) if e else ""
def example(c): e=g.value(c,EX); return str(e) if e else ""
def visual(c): v=g.value(c,VIS); return str(v) if v else ""
def icon(c): i=g.value(c,SCP.icon); return str(i) if i else ""
def url(c): u=g.value(c,SCP.url); return str(u) if u else ""
def modelkind(a): m=g.value(a,SCP.modelKind); return str(m) if m else ""
def reslink(c):
    u=g.value(c,SCP.resourceLink); lab=g.value(c,SCP.resourceLabel)
    return (str(u),str(lab)) if u else ("","")
def related(c):
    return sorted([(loc(r),label(r)) for r in g.objects(c,SCP.relatedConcept)], key=lambda x:x[1])
import json as _json
def casegraph(k):
    v=g.value(k,SCP.caseGraph); return _json.loads(str(v)) if v else None
import json as _jg
_PFXG=None
def prefix_glossary():
    global _PFXG
    if _PFXG is None:
        v=g.value(SCP.PrefixGlossary,SCP.prefixGlossary); _PFXG=_jg.loads(str(v)) if v else {}
    return _PFXG
_TERMG=None
def term_glossary():
    global _TERMG
    if _TERMG is None:
        v=g.value(SCP.TermGlossary,SCP.termGlossary); _TERMG=_jg.loads(str(v)) if v else {}
    return _TERMG
def taxonomy_page_data():
    v=g.value(SCP.TaxonomyExplainer,SCP.taxonomyPageData); return _jg.loads(str(v)) if v else None
def comparison_data():
    v=g.value(SCP.TradVsSemantic,SCP.comparisonData); return _jg.loads(str(v)) if v else None
def model_comparison(c):
    v=g.value(c,SCP.modelComparison); return _jg.loads(str(v)) if v else None
def prov_legend():
    v=g.value(SCP.ProvenanceLegend,SCP.provLegend); return _jg.loads(str(v)) if v else None
def corpus_data():
    v=g.value(SCP.WorkedCorpus,SCP.corpusData); return _jg.loads(str(v)) if v else None
def primer_data():
    v=g.value(SCP.PrimitivesPrimer,SCP.primerData); return _jg.loads(str(v)) if v else None
def inference_contrast(c):
    v=g.value(c,SCP.inferenceContrast); return _jg.loads(str(v)) if v else None
def axiom_reference(c):
    v=g.value(c,SCP.axiomReference); return _jg.loads(str(v)) if v else None
def crosstech(c):
    v=g.value(c,SCP.crossTech); return _jg.loads(str(v)) if v else None
def syntaxnotes(c):
    import json as _j3
    v=g.value(c,SCP.syntaxNote); return _j3.loads(str(v)) if v else None
def techcompare_rich(c):
    v=g.value(c,SCP.techCompareRich); return _jg.loads(str(v)) if v else None
def techcompare(c):
    import json as _j4
    v=g.value(c,SCP.techCompare); return _j4.loads(str(v)) if v else None
def casecode(k):
    cc=g.value(k,SCP.caseCode); cl=g.value(k,SCP.caseCodeLang)
    return (str(cc),str(cl) if cl else 'turtle') if cc else ('','')
def case_idgloss(k):
    v=g.value(k,SCP.idGlossary)
    return _json.loads(str(v)) if v else None
def caseexec(k):
    s=g.value(k,SCP.caseExecSteps); r=g.value(k,SCP.caseExecResult)
    import json as _j2
    steps=_j2.loads(str(s)) if s else None
    result=_j2.loads(str(r)) if r else None
    # MECHANICAL EXECUTION: where the example's point is "run this code → get this result",
    # compute the result from the ACTUAL code so it can never drift from the snippet.
    ccode=g.value(k,SCP.caseCode); clang=g.value(k,SCP.caseCodeLang)
    if ccode is not None:
        cid=loc(k)
        computed=_exec_compute(str(ccode), str(clang) if clang else 'turtle', cid)
        if computed:
            if computed.get('steps'): steps=computed['steps']   # steps computed from code too
            result={'cols':computed['cols'],'rows':computed['rows'],'_computed':True}
    return (steps,result)
def execdata(c):
    s=g.value(c,SCP.execSteps); r=g.value(c,SCP.execResult)
    return (_json.loads(str(s)) if s else None,_json.loads(str(r)) if r else None)
def taxonomies():
    out=[]
    for t in g.subjects(RDF.type,SCP.Taxonomy):
        out.append((str(g.value(t,RDFS.label)),str(g.value(t,SCP.exampleDomain)),_json.loads(str(g.value(t,SCP.taxonomyTree)))))
    return sorted(out,key=lambda x:x[1])
def explainer(c):
    v=g.value(c,SCP.explainerData); return _json.loads(str(v)) if v else None
def code(c):
    s=g.value(c,SCP.codeSnippet); l=g.value(c,SCP.codeLang)
    return (str(s),str(l) if l else 'turtle') if s else ('','')
def industry(c):
    lab=g.value(c,SCP.industryLabel); lk=g.value(c,SCP.industryLink); nt=g.value(c,SCP.industryNote)
    return (str(lab),str(lk),str(nt) if nt else '') if lk else ('','','')
def cases(c):
    out=[]
    for k in g.subjects(SCP.ofConcept,c):
        out.append((str(g.value(k,SCP.exampleDomain)),str(g.value(k,SCP.exampleText)),str(g.value(k,SCP.exampleVisual) or ""),casegraph(k),k))
    return sorted(out,key=lambda x:x[0])
def source(c): s=g.value(c,DCTERMS.source); return label(s) if isinstance(s,rdflib.URIRef) else (str(s) if s else "")
def h(s): return html.escape(str(s))
def hattr(s): return html.escape(str(s),quote=True)

AXIS=SCP[_AREA_MARKER]
areas=[s for s in g.subjects(RDFS.subClassOf,AXIS) if isinstance(s,rdflib.URIRef)]
order=['Foundations','W3CStack','LayeredOntology','KnowledgeGraphs']
areas=sorted(areas, key=lambda a: order.index(loc(a)) if loc(a) in order else 99)
def concepts_of(a): return sorted([s for s in g.subjects(RDFS.subClassOf,a) if isinstance(s,rdflib.URIRef)],key=label)
pubs=sorted([p for p in g.subjects(RDF.type,SCP.Publication)],key=label)
sims=sorted([s for s in g.subjects(RDF.type,SCP.Simulation)],key=label)

fidelity=[]
def trace(elem,subj,pred,obj): fidelity.append({'element':elem,'triple':f"{loc(subj)} {loc(pred)} {loc(obj) if isinstance(obj,rdflib.URIRef) else 'literal'}"})

def short_table(headers,rows):
    th=''.join(f'<th>{h(x)}</th>' for x in headers)
    tb=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)
    return f'<table class="short"><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table>'

# ---- concept-diagram SVGs (generated by VIS kind) ----
def concept_svg(kind):
    s='<svg viewBox="0 0 420 90" style="width:100%;max-width:420px;margin:6px 0;font-family:ui-sans-serif,system-ui,sans-serif;font-size:11px">'
    A='<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#888"/></marker></defs>'
    if kind=='triple':
        return s+A+'<g><rect x="10" y="30" width="100" height="30" rx="5" fill="#4a7c8c"/><text x="60" y="49" fill="#fff" text-anchor="middle">subject</text></g><line x1="110" y1="45" x2="160" y2="45" stroke="#888" marker-end="url(#ar)"/><text x="190" y="40" text-anchor="middle" fill="#586272">predicate</text><g><rect x="230" y="30" width="100" height="30" rx="5" fill="#5b8a72"/><text x="280" y="49" fill="#fff" text-anchor="middle">object</text></g><line x1="330" y1="45" x2="380" y2="45" stroke="#888" marker-end="url(#ar)"/></svg>'
    if kind=='pattern':
        return s+A+'<g><rect x="10" y="20" width="80" height="26" rx="5" fill="#4a7c8c"/><text x="50" y="37" fill="#fff" text-anchor="middle">?dc</text></g><line x1="90" y1="33" x2="140" y2="33" stroke="#888" marker-end="url(#ar)"/><text x="175" y="28" text-anchor="middle" fill="#586272">replenishes</text><g><rect x="210" y="20" width="90" height="26" rx="5" fill="#b5803a"/><text x="255" y="37" fill="#fff" text-anchor="middle">?store</text></g><text x="155" y="72" text-anchor="middle" fill="#586272">matches every DC→store edge</text></svg>'
    if kind=='shape':
        return s+'<g><rect x="10" y="20" width="120" height="50" rx="6" fill="#fff" stroke="#9a5b6e" stroke-width="2"/><text x="70" y="40" text-anchor="middle" fill="#9a5b6e">SKU shape</text><text x="70" y="58" text-anchor="middle" fill="#586272" font-size="9">exactly 1 category</text></g><line x1="130" y1="45" x2="180" y2="45" stroke="#888" stroke-dasharray="3"/><g><rect x="200" y="20" width="100" height="24" rx="4" fill="#eef4ee" stroke="#3f7a4d"/><text x="250" y="36" text-anchor="middle" fill="#3f7a4d">✓ valid</text></g><g><rect x="200" y="50" width="100" height="24" rx="4" fill="#f6efe9" stroke="#a4502f"/><text x="250" y="66" text-anchor="middle" fill="#a4502f">✗ rejected</text></g></svg>'
    if kind=='ragflow':
        return s+A+'<g><rect x="6" y="32" width="78" height="26" rx="5" fill="#fff" stroke="#d8d2c4"/><text x="45" y="49" text-anchor="middle">question</text></g><line x1="84" y1="45" x2="110" y2="45" stroke="#888" marker-end="url(#ar)"/><g><rect x="112" y="32" width="86" height="26" rx="5" fill="#b5803a"/><text x="155" y="49" fill="#fff" text-anchor="middle">subgraph</text></g><line x1="198" y1="45" x2="224" y2="45" stroke="#888" marker-end="url(#ar)"/><g><rect x="226" y="32" width="74" height="26" rx="5" fill="#9a5b6e"/><text x="263" y="49" fill="#fff" text-anchor="middle">ground</text></g><line x1="300" y1="45" x2="326" y2="45" stroke="#888" marker-end="url(#ar)"/><g><rect x="328" y="32" width="84" height="26" rx="5" fill="#3f7a4d"/><text x="370" y="49" fill="#fff" text-anchor="middle">answer</text></g></svg>'
    if kind=='tiers':
        return s+'<g><rect x="120" y="6" width="180" height="20" rx="4" fill="#5b8a72"/><text x="210" y="20" fill="#fff" text-anchor="middle">TBox — schema</text></g><g><rect x="120" y="32" width="180" height="20" rx="4" fill="#9a5b6e"/><text x="210" y="46" fill="#fff" text-anchor="middle">ABox — instances</text></g><g><rect x="120" y="58" width="180" height="20" rx="4" fill="#b5803a"/><text x="210" y="72" fill="#fff" text-anchor="middle">RBox — role axioms</text></g></svg>'
    if kind=='synonyms':
        return s+A+'<g><rect x="10" y="10" width="80" height="20" rx="10" fill="#eef2f8" stroke="#4a7c8c"/><text x="50" y="24" text-anchor="middle" fill="#4a7c8c">vendor</text></g><g><rect x="10" y="35" width="80" height="20" rx="10" fill="#eef2f8" stroke="#4a7c8c"/><text x="50" y="49" text-anchor="middle" fill="#4a7c8c">source</text></g><g><rect x="10" y="60" width="80" height="20" rx="10" fill="#eef2f8" stroke="#4a7c8c"/><text x="50" y="74" text-anchor="middle" fill="#4a7c8c">partner</text></g><line x1="90" y1="20" x2="200" y2="42" stroke="#888" marker-end="url(#ar)"/><line x1="90" y1="45" x2="200" y2="45" stroke="#888" marker-end="url(#ar)"/><line x1="90" y1="70" x2="200" y2="48" stroke="#888" marker-end="url(#ar)"/><g><rect x="200" y="32" width="100" height="26" rx="5" fill="#5b8a72"/><text x="250" y="49" fill="#fff" text-anchor="middle">:Supplier</text></g></svg>'
    if kind=='subclass':
        return s+A+'<g><rect x="130" y="8" width="160" height="26" rx="5" fill="#4a7c8c"/><text x="210" y="25" fill="#fff" text-anchor="middle">parent class</text></g><line x1="210" y1="34" x2="210" y2="56" stroke="#888" marker-end="url(#ar)"/><text x="250" y="50" fill="#586272" font-size="9">rdfs:subClassOf</text><g><rect x="130" y="58" width="160" height="26" rx="5" fill="#5b8a72"/><text x="210" y="75" fill="#fff" text-anchor="middle">subclass</text></g><text x="60" y="48" fill="#586272" font-size="9">query parent</text><text x="60" y="60" fill="#3f7a4d" font-size="9">→ returns both</text></svg>'
    if kind=='inverse':
        return s+A+'<g><rect x="20" y="32" width="120" height="26" rx="5" fill="#4a7c8c"/><text x="80" y="49" fill="#fff" text-anchor="middle">A</text></g><g><rect x="280" y="32" width="120" height="26" rx="5" fill="#5b8a72"/><text x="340" y="49" fill="#fff" text-anchor="middle">B</text></g><line x1="140" y1="40" x2="280" y2="40" stroke="#888" marker-end="url(#ar)"/><text x="210" y="33" text-anchor="middle" fill="#586272" font-size="9">relates</text><line x1="280" y1="52" x2="140" y2="52" stroke="#b5803a" stroke-dasharray="3" marker-end="url(#ar)"/><text x="210" y="68" text-anchor="middle" fill="#b5803a" font-size="9">inverse (inferred)</text></svg>'
    if kind=='prov':
        return s+A+'<g><rect x="10" y="32" width="90" height="26" rx="5" fill="#9a5b6e"/><text x="55" y="49" fill="#fff" text-anchor="middle">Entity</text></g><line x1="100" y1="45" x2="150" y2="45" stroke="#888" marker-end="url(#ar)"/><text x="175" y="40" text-anchor="middle" fill="#586272" font-size="9">wasGeneratedBy</text><g><rect x="200" y="32" width="90" height="26" rx="5" fill="#b5803a"/><text x="245" y="49" fill="#fff" text-anchor="middle">Activity</text></g><line x1="290" y1="45" x2="330" y2="45" stroke="#888" marker-end="url(#ar)"/><g><rect x="330" y="32" width="80" height="26" rx="5" fill="#4a7c8c"/><text x="370" y="49" fill="#fff" text-anchor="middle">Agent</text></g><text x="210" y="80" text-anchor="middle" fill="#586272" font-size="9">who made what, when — auditable trail</text></svg>'
    if kind=='vector':
        return s+'<g><line x1="40" y1="78" x2="40" y2="12" stroke="#ccc"/><line x1="40" y1="78" x2="290" y2="78" stroke="#ccc"/>'+''.join(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{col}"/><text x="{cx+8}" y="{cy+3}" font-size="9" fill="#586272">{lb}</text>' for cx,cy,col,lb in [(90,55,'#4a7c8c','blazer'),(110,48,'#4a7c8c','trousers'),(230,25,'#9a5b6e','mug')])+'<line x1="90" y1="55" x2="110" y2="48" stroke="#b5803a" stroke-dasharray="2"/><text x="150" y="40" font-size="9" fill="#b5803a">near → "bought together"</text></g><text x="165" y="90" text-anchor="middle" fill="#586272" font-size="9" font-family="ui-sans-serif">entities as vectors; proximity predicts links</text></svg>'
    if kind=='panel':
        return s+'<g><rect x="10" y="10" width="150" height="70" rx="5" fill="#fff" stroke="#d8d2c4"/><text x="20" y="26" font-size="9" fill="#586272">"search a thing"</text><line x1="20" y1="32" x2="150" y2="32" stroke="#eee"/><text x="20" y="46" font-size="9" fill="#aaa">…ten blue links…</text><text x="20" y="60" font-size="9" fill="#aaa">…text matches…</text></g><line x1="160" y1="45" x2="200" y2="45" stroke="#888" marker-end="url(#ar)"/><g><rect x="200" y="10" width="210" height="70" rx="5" fill="#eef2f4" stroke="#4a7c8c"/><text x="210" y="26" font-size="9" fill="#2d4a52" font-weight="bold">structured panel</text><text x="210" y="42" font-size="9" fill="#586272">• born · works · related</text><text x="210" y="56" font-size="9" fill="#586272">• facts, not strings</text><text x="210" y="70" font-size="9" fill="#586272">(knowledge graph)</text></g></svg>'
    if kind=='pyramid':
        return s.replace('0 0 420 90','0 0 420 120')+'<g><polygon points="160,12 260,12 240,40 180,40" fill="#2d4a52"/><text x="210" y="30" fill="#fff" text-anchor="middle" font-size="9">foundational (BFO)</text></g><g><polygon points="175,44 245,44 270,76 150,76" fill="#5b8a72"/><text x="210" y="64" fill="#fff" text-anchor="middle" font-size="9">domain</text></g><g><polygon points="145,80 275,80 300,108 120,108" fill="#b5803a"/><text x="210" y="98" fill="#fff" text-anchor="middle" font-size="9">application</text></g><text x="60" y="60" font-size="9" fill="#586272">shared</text><text x="60" y="72" font-size="9" fill="#586272">backbone</text></svg>'
    return ''


def code_block(snippet,lang):
    """Render a real code snippet with light syntax highlighting (turtle/sparql/json/python)."""
    import re as _re
    esc=h(snippet)
    # comments
    esc=_re.sub(r'(#[^\n]*)', r'<span class="c-com">\1</span>', esc)
    if lang=='sparql':
        for kw in ['PREFIX','SELECT','WHERE','ORDER BY','FILTER','OPTIONAL','LIMIT','DISTINCT']:
            esc=esc.replace(kw,f'<span class="c-kw">{kw}</span>')
    elif lang in ('turtle',):
        for kw in ['@prefix','rdfs:subClassOf','rdfs:subPropertyOf','owl:inverseOf','owl:disjointWith','sh:NodeShape','sh:targetClass','sh:property','sh:path','sh:minCount','sh:maxCount','sh:datatype','skos:prefLabel','skos:altLabel','prov:wasGeneratedBy','prov:wasAttributedTo','prov:generatedAtTime','a ']:
            esc=esc.replace(kw,f'<span class="c-kw">{kw}</span>')
        esc=_re.sub(r'(&quot;[^&]*&quot;(?:@\w+)?)', r'<span class="c-str">\1</span>', esc)
    elif lang=='json':
        esc=_re.sub(r'(&quot;[^&]*&quot;)(\s*:)', r'<span class="c-key">\1</span>\2', esc)
        esc=_re.sub(r'(:\s*)(&quot;[^&]*&quot;)', r'\1<span class="c-str">\2</span>', esc)
    elif lang=='sql':
        for kw in ['SELECT','FROM','JOIN','ON','WHERE','GROUP BY','SUM','PRIMARY KEY','FOREIGN KEY','CHECK']:
            esc=esc.replace(kw,f'<span class="c-kw">{kw}</span>')
    elif lang=='cypher':
        for kw in ['MATCH','RETURN','WHERE','CREATE','MERGE']:
            esc=esc.replace(kw,f'<span class="c-kw">{kw}</span>')
    elif lang=='python':
        for kw in ['def ','return','import ','for ','in ','None','True','False']:
            esc=esc.replace(kw,f'<span class="c-kw">{kw}</span>')
        esc=_re.sub(r'(&quot;[^&]*&quot;)', r'<span class="c-str">\1</span>', esc)
    label={'turtle':'Turtle (RDF)','sparql':'SPARQL','json':'JSON-LD','python':'Python','sql':'SQL','cypher':'Cypher'}.get(lang,lang)
    return (f'<div class="codeblock"><div class="code-bar"><span class="code-lang">{h(label)}</span>'
            f'<button class="code-copy" data-code="{hattr(snippet)}">copy</button></div>'
            f'<pre><code>{esc}</code></pre></div>')


def render_case_graph(graph,cid,idx):
    """Generic node/edge graph renderer with correct, bounds-aware layout (no clipping/overlap)."""
    if not graph: return ''
    nodes=graph.get('nodes',[]); edges=graph.get('edges',[])
    if not nodes: return ''
    colors={'s':'#4a7c8c','p':'#b5803a','o':'#5b8a72','ok':'#3f7a4d','bad':'#a4502f'}
    NW,NH=120,28           # node box size
    COLW=170               # column spacing
    PAD=12                 # outer padding
    # assign columns by role: subjects=0, process=1, objects/ok/bad=2 (but collapse empty middle)
    colmap={'s':0,'p':1,'o':2,'ok':2,'bad':2}
    cols={}
    for i,(lab,r) in enumerate(nodes): cols.setdefault(colmap.get(r,1),[]).append(i)
    used_cols=sorted(cols.keys())
    col_x={c:PAD+NW/2+used_cols.index(c)*COLW for c in used_cols}   # left-to-right, no gaps
    W=PAD*2+NW+ (len(used_cols)-1)*COLW
    maxrows=max(len(v) for v in cols.values())
    rowh=NH+16
    H=PAD*2+maxrows*rowh
    pos={}
    for c in used_cols:
        ids=cols[c]; ystart=PAD+ (H-PAD*2-len(ids)*rowh)/2
        for j,i in enumerate(ids):
            pos[i]=(col_x[c], ystart+j*rowh+NH/2)
    svg=[f'<svg viewBox="0 0 {W:.0f} {H:.0f}" class="case-graph" style="width:100%;max-width:{W:.0f}px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:10px">']
    svg.append('<defs><marker id="cg" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#8a99a4"/></marker></defs>')
    # edges first
    looselabels=[]
    for e in edges:
        if len(e)<2:
            if len(e)==1: looselabels.append(str(e[0]))
            continue
        a,b=e[0],e[1]; lbl=e[2] if len(e)>2 else ''
        if a not in pos or b not in pos:
            if lbl: looselabels.append(lbl)
            continue
        x1,y1=pos[a]; x2,y2=pos[b]
        # connect from right edge of a to left edge of b (or nearest)
        sx = x1+NW/2 if x2>x1 else (x1-NW/2 if x2<x1 else x1)
        ex = x2-NW/2 if x2>x1 else (x2+NW/2 if x2<x1 else x2)
        svg.append(f'<line x1="{sx:.0f}" y1="{y1:.0f}" x2="{ex:.0f}" y2="{y2:.0f}" stroke="#8a99a4" marker-end="url(#cg)"/>')
        if lbl:
            mx,my=(sx+ex)/2,(y1+y2)/2
            svg.append(f'<text x="{mx:.0f}" y="{my-4:.0f}" text-anchor="middle" fill="#586272" font-size="9">{h(lbl)}</text>')
    # nodes
    for i,(lab,r) in enumerate(nodes):
        if i not in pos: continue
        x,y=pos[i]; col=colors.get(r,'#5b8a72'); rx=14 if r in('s','o') else 5
        svg.append(f'<g><rect x="{x-NW/2:.0f}" y="{y-NH/2:.0f}" width="{NW}" height="{NH}" rx="{rx}" fill="{col}"/><text x="{x:.0f}" y="{y+4:.0f}" fill="#fff" text-anchor="middle">{h(lab)[:18]}</text></g>')
    # loose labels (e.g. SHACL self-relations) shown under the diagram, not floating
    if looselabels:
        svg.append(f'<text x="{W/2:.0f}" y="{H-4:.0f}" text-anchor="middle" fill="#b5803a" font-size="9">{h(" · ".join(looselabels))}</text>')
    svg.append('</svg>')
    return ''.join(svg)

def build_explainer(exp):
    cards=[]
    for r in exp['rows']:
        cards.append(
            '<div class="ex4-card" style="border-top:3px solid '+r['color']+'">'
            '<div class="ex4-name">'+h(r['name'])+'</div>'
            '<div class="ex4-full">'+h(r['full'])+'</div>'
            '<div class="ex4-q">'+h(r['q'])+'</div>'
            '<div class="ex4-gov">'+h(r['governs'])+'</div>'
            '<code class="ex4-ex">'+h(r['example'])+'</code></div>')
    return ('<div class="explainer"><div class="ex4-title">'+h(exp['title'])+'</div>'
            '<div class="ex4-grid">'+''.join(cards)+'</div>'
            '<p class="ex4-note">'+h(exp['note'])+'</p></div>')

def build_taxonomy(label,domain,tree,tid):
    """Real taxonomy as an MS-Explorer collapsible tree."""
    def node(name,children,depth):
        nid=tid+'_'+str(abs(hash(name))%99999)
        if isinstance(children,dict):
            sub=''.join(node(k,v,depth+1) for k,v in children.items())
            return ('<div class="tx-folder" data-tx="'+nid+'" tabindex="0" role="treeitem" aria-selected="false"><span class="tx-tw">▸</span> '
                    '<span class="tx-name">'+h(name)+'</span></div>'
                    '<div class="tx-children" id="txc-'+nid+'">'+sub+'</div>')
        elif isinstance(children,list):
            items=''.join('<div class="tx-leaf">📄 '+h(x)+'</div>' for x in children)
            return ('<div class="tx-folder" data-tx="'+nid+'" tabindex="0" role="treeitem" aria-selected="false"><span class="tx-tw">▸</span> '
                    '<span class="tx-name">'+h(name)+'</span></div>'
                    '<div class="tx-children" id="txc-'+nid+'">'+items+'</div>')
        return ''
    body=''.join(node(k,v,0) for k,v in tree.items())
    return ('<div class="taxonomy-explorer"><div class="tx-head"><span class="tx-domain">'+h(domain)+'</span> '
            '<span class="tx-label">'+h(label)+'</span></div>'+body+'</div>')

def build_id_glossary(d,uid):
    """Decode opaque IDs (e.g. Wikidata Q/P codes) used in a code snippet, with verified labels + source."""
    if not d: return ''
    rows=''.join(
        '<tr><td class="idg-code">'+h(e[0])+'</td><td class="idg-label">'+h(e[1])+'</td>'
        '<td class="idg-desc">'+h(e[3])+'</td>'
        '<td><a class="idg-src" href="'+hattr(e[2])+'" target="_blank" rel="noopener">source \u2197</a></td></tr>'
        for e in d['entries'])
    reads=('<div class="idg-reads"><span class="idg-reads-lbl">Reads as:</span> '+h(d['reads_as'])+'</div>') if d.get('reads_as') else ''
    live =('<div class="idg-live">'+h(d['live_result'])+'</div>') if d.get('live_result') else ''
    note =('<p class="idg-note">'+h(d['note'])+'</p>') if d.get('note') else ''
    return ('<div class="idgloss"><div class="idg-head"><span class="idg-lbl">What the IDs mean</span></div>'
            +note+
            '<table class="idg-table"><thead><tr><th>ID</th><th>meaning</th><th>notes</th><th></th></tr></thead>'
            '<tbody>'+rows+'</tbody></table>'+reads+live+'</div>')

def exec_widget(steps,result,uid):
    """Code-execution step animation + result table, with a unique id (per pane)."""
    stepli=''.join('<li>'+h(s)+'</li>' for s in steps)
    cols=''.join('<th>'+h(x)+'</th>' for x in result['cols'])
    rws=''.join('<tr>'+''.join('<td>'+h(cell)+'</td>' for cell in r)+'</tr>' for r in result['rows'])
    # honest provenance of the result: computed from the code, or a representative illustration
    computed = result.get('_computed')
    rlbl = ('Result <span class="exec-computed" title="This table is computed by actually loading the code '
            'above into an RDF engine at build time — it is the real output, not a hand-written illustration.">'
            '⚙ computed from the code</span>') if computed else 'Result'
    return ('<div class="exec">'
            '<div class="exec-bar"><span class="exec-lbl">What this produces</span>'
            '<button class="exec-run" data-exec="'+uid+'">\u25b6 run step-by-step</button></div>'
            '<ol class="exec-steps" id="exec-steps-'+uid+'">'+stepli+'</ol>'
            '<div class="exec-result"><div class="exec-rlbl">'+rlbl+'</div>'
            '<table class="result-tbl"><thead><tr>'+cols+'</tr></thead>'
            '<tbody id="exec-rows-'+uid+'">'+rws+'</tbody></table></div></div>')

def build_syntax_notes(notes,uid,codetext=''):
    """Glossary derived ENTIRELY from this code: prefixes present + specific terms present. No fixed list."""
    rows=[]; seen=set()
    pg=prefix_glossary()
    for pfx,meaning in pg.items():
        present = ('@prefix' in codetext) if pfx=='@prefix' else ((':' in codetext) if pfx==':' else (pfx in codetext))
        if present and pfx not in seen:
            rows.append((pfx,meaning)); seen.add(pfx)
    # specific terms: only those that actually appear in THIS code
    tg=term_glossary()
    # longer tokens first so 'GROUP BY ' wins over 'SELECT' etc.
    for term in sorted(tg.keys(), key=lambda t:-len(t)):
        if term in seen: continue
        tok=term.rstrip()  # allow trailing-space disambiguation in glossary keys
        if tok and tok in codetext:
            rows.append((term.strip(),tg[term])); seen.add(term)
    if not rows: return ''
    items=''.join('<div class="syn-row"><code class="syn-term">'+h(t)+'</code><span class="syn-mean">'+h(m)+'</span></div>' for t,m in rows)
    return ('<details class="syntax-notes"><summary>What does this syntax &amp; these prefixes mean? ('+str(len(rows))+' terms)</summary>'
            '<div class="syn-body"><div class="syn-hint">Namespaces (prefixes) first, then the specific terms that appear in the code above:</div>'+items+'</div></details>')

def build_tech_compare(rows):
    """How OTHER technologies would represent the same example."""
    if not rows: return ''
    cards=''.join('<div class="tc-card"><div class="tc-tech">'+h(t)+'</div><div class="tc-how">'+h(how)+'</div></div>' for t,how in rows)
    return ('<div class="techcompare"><div class="tc-head"><span class="tc-lbl">How other technologies would handle this</span></div>'
            '<div class="tc-grid">'+cards+'</div></div>')

def build_cross_tech(techs,cid):
    """Cross-technology TAB: same example re-expressed in each technology, with code + impact."""
    if not techs: return ''
    tabs=''.join('<button class="ct-tab'+(' active' if i==0 else '')+'" data-ct="'+cid+'" data-i="'+str(i)+'">'+h(t['tech'])+'</button>' for i,t in enumerate(techs))
    panes=''
    for i,t in enumerate(techs):
        cb=code_block(t['code'],t.get('lang','turtle'))
        panes+=('<div class="ct-pane'+(' active' if i==0 else '')+'" id="ct-'+cid+'-'+str(i)+'">'
                +cb+'<div class="ct-impact"><span class="ct-impact-lbl">Impact</span> '+h(t['impact'])+'</div></div>')
    return ('<div class="crosstech-tab"><div class="ct-head"><span class="ct-lbl">Same example across technologies</span>'
            '<span class="ct-hint">↔ switch technology — see the code and its impact change</span></div>'
            '<div class="ct-tabs">'+tabs+'</div>'+panes+'</div>')

def graph_type_svg(shape):
    s='<svg viewBox="0 0 160 90" class="gt-svg" style="width:100%;max-width:160px">'
    if shape=='rdf':
        s+='<defs><marker id="gta" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L5,3 L0,6 Z" fill="#8a99a4"/></marker></defs>'
        s+='<line x1="35" y1="30" x2="80" y2="30" stroke="#8a99a4" marker-end="url(#gta)"/><line x1="80" y1="40" x2="80" y2="60" stroke="#8a99a4" marker-end="url(#gta)"/>'
        for x,y,c in [(25,30,'#4a7c8c'),(90,30,'#5b8a72'),(80,68,'#b5803a')]:
            s+=f'<circle cx="{x}" cy="{y}" r="11" fill="{c}"/>'
    elif shape=='pg':
        s+='<rect x="14" y="20" width="44" height="22" rx="5" fill="#4a7c8c"/><rect x="100" y="48" width="44" height="22" rx="5" fill="#5b8a72"/><line x1="58" y1="31" x2="100" y2="58" stroke="#b5803a" stroke-width="2"/><text x="80" y="40" font-size="7" fill="#586272" text-anchor="middle">{props}</text>'
    elif shape=='tree':
        s+='<line x1="80" y1="20" x2="40" y2="50" stroke="#8a99a4"/><line x1="80" y1="20" x2="120" y2="50" stroke="#8a99a4"/><line x1="40" y1="50" x2="25" y2="75" stroke="#8a99a4"/><line x1="40" y1="50" x2="55" y2="75" stroke="#8a99a4"/>'
        for x,y in [(80,18),(40,50),(120,50),(25,75),(55,75)]:
            s+=f'<rect x="{x-10}" y="{y-7}" width="20" height="14" rx="3" fill="#5b8a72"/>'
    elif shape=='bipartite':
        for i,y in enumerate([25,50,75]): s+=f'<circle cx="35" cy="{y}" r="8" fill="#4a7c8c"/>'
        for i,y in enumerate([35,65]): s+=f'<circle cx="125" cy="{y}" r="8" fill="#b5803a"/>'
        for y1 in [25,50,75]:
            for y2 in [35,65]: s+=f'<line x1="43" y1="{y1}" x2="117" y2="{y2}" stroke="#ddd"/>'
    elif shape=='flat':
        for i,x in enumerate([28,64,100,136]):
            s+=f'<rect x="{x-13}" y="38" width="26" height="16" rx="4" fill="#5b8a72"/>'
    elif shape=='poly':
        # DAG: a child with two parents
        s+='<defs><marker id="gtp" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0,0 L5,3 L0,6 Z" fill="#8a99a4"/></marker></defs>'
        s+='<line x1="45" y1="28" x2="80" y2="62" stroke="#8a99a4" marker-end="url(#gtp)"/><line x1="115" y1="28" x2="80" y2="62" stroke="#8a99a4" marker-end="url(#gtp)"/>'
        for x,y,c in [(45,22,'#5b8a72'),(115,22,'#5b8a72'),(80,68,'#9a5b6e')]:
            s+=f'<rect x="{x-16}" y="{y-7}" width="32" height="15" rx="4" fill="{c}"/>'
    elif shape=='facet':
        # three independent dimension columns
        for col,x in enumerate([30,80,130]):
            s+=f'<rect x="{x-16}" y="14" width="32" height="12" rx="3" fill="#b5803a"/>'
            for r,y in enumerate([34,52,70]):
                s+=f'<rect x="{x-14}" y="{y}" width="28" height="11" rx="2" fill="#5b8a72" opacity="0.85"/>'
    elif shape=='network':
        s+='<line x1="40" y1="30" x2="90" y2="25" stroke="#9a5b6e" stroke-dasharray="3"/><line x1="90" y1="25" x2="120" y2="60" stroke="#9a5b6e" stroke-dasharray="3"/><line x1="40" y1="30" x2="55" y2="65" stroke="#9a5b6e" stroke-dasharray="3"/><line x1="55" y1="65" x2="120" y2="60" stroke="#9a5b6e" stroke-dasharray="3"/>'
        for x,y in [(40,30),(90,25),(120,60),(55,65)]:
            s+=f'<circle cx="{x}" cy="{y}" r="9" fill="#4a7c8c"/>'
    elif shape=='hyper':
        s+='<ellipse cx="80" cy="45" rx="55" ry="28" fill="none" stroke="#9a5b6e" stroke-width="2" stroke-dasharray="4"/>'
        for x,y in [(45,35),(115,35),(60,62),(100,62)]: s+=f'<circle cx="{x}" cy="{y}" r="9" fill="#4a7c8c"/>'
    return s.replace('{props}','')+'</svg>'

def build_taxonomy_page(tax_explorers_html):
    d=taxonomy_page_data()
    if not d: return '<div class="page" id="page-sims"><h2>Taxonomies</h2>'+''.join(tax_explorers_html)+'</div>'
    P=['<div class="page" id="page-sims"><div class="secnum">Taxonomies</div>',
       '<h2>Taxonomies — the entry layer of semantic technology</h2>',
       f'<p>{h(d["intro"])}</p>']
    # DEFINITION + building blocks
    P.append('<h2>What a taxonomy is</h2>')
    P.append(f'<p>{h(d["definition"]["text"])}</p>')
    P.append('<div class="tx-blocks">'+''.join(
        f'<div class="tx-block"><div class="tx-block-name">{h(n)}</div><div class="tx-block-desc">{h(desc)}</div></div>'
        for n,desc in d['definition']['blocks'])+'</div>')
    # TYPES (with graph-type visuals)
    P.append('<h2>Types of taxonomy</h2>')
    P.append('<div class="tx-types">')
    for t in d['types']:
        P.append(f'<div class="tx-type-card">{graph_type_svg(t["shape"])}<div class="tx-type-name">{h(t["type"])}</div>'
                 f'<div class="tx-type-desc">{h(t["desc"])}</div><div class="tx-type-ex">e.g. {h(t["ex"])}</div></div>')
    P.append('</div>')
    # RELATIONSHIP TO ONTOLOGIES (spectrum)
    P.append('<h2>Relationship to ontologies &amp; semantic technologies</h2>')
    P.append(f'<p>{h(d["ontology_rel"]["text"])}</p>')
    P.append('<div class="tx-spectrum">')
    levels={'low':1,'low-mid':2,'mid':3,'high':5}
    for name,desc,lvl in d['ontology_rel']['spectrum']:
        w=levels.get(lvl,3)
        P.append(f'<div class="tx-spec-row"><div class="tx-spec-name">{h(name)}</div>'
                 f'<div class="tx-spec-bar"><span style="width:{w*20}%"></span></div>'
                 f'<div class="tx-spec-desc">{h(desc)}</div></div>')
    P.append('</div><p class="note">Increasing formal expressivity, left to right — a taxonomy is the hierarchy an ontology is built on.</p>')
    # USAGE
    P.append('<h2>How taxonomies are used</h2>')
    urows=''.join(f'<tr><td class="cmp-dim">{h(u["use"])}</td><td>{h(u["how"])}</td><td class="tx-ex-cell">{h(u["ex"])}</td></tr>' for u in d['usage'])
    P.append(f'<table class="cmp-table"><thead><tr><th>Usage</th><th>How</th><th>Example</th></tr></thead><tbody>{urows}</tbody></table>')
    # DISCOVERY
    P.append('<h2>How to discover a taxonomy</h2>')
    for m in d['discovery']:
        P.append(f'<div class="cmp-syn"><div class="cmp-syn-name">{h(m["method"])}</div><div class="cmp-syn-how">{h(m["how"])}</div></div>')
    # MULTIPLE taxonomies
    P.append('<h2>Implementing multiple taxonomies</h2>')
    P.append(f'<p>{h(d["multiple"]["text"])}</p>')
    P.append('<table class="cmp-table"><thead><tr><th>Mapping relation</th><th>Meaning</th></tr></thead><tbody>'
             +''.join(f'<tr><td class="cmp-dim"><code>{h(rel)}</code></td><td>{h(mean)}</td></tr>' for rel,mean in d['multiple']['mappings'])
             +'</tbody></table>')
    # COMPARISON traditional vs semantic (with graph-type visuals on the views)
    P.append('<h2>Traditional hierarchy management vs. semantic (SKOS)</h2>')
    crows=''.join(f'<tr><td class="cmp-dim">{h(r["dim"])}</td><td class="cmp-tcell">{h(r["trad"])}</td><td class="cmp-scell">{h(r["sem"])}</td></tr>' for r in d['comparison'])
    P.append(f'<table class="cmp-table"><thead><tr><th>Dimension</th><th>Traditional</th><th>Semantic (SKOS)</th></tr></thead><tbody>{crows}</tbody></table>')
    # GRAPH VIEWS of the data (requested enhancement)
    P.append('<h2>Visualizing taxonomy data with different graph types</h2>')
    P.append('<p class="note">The same taxonomic data takes different graph shapes depending on its structure:</p>')
    P.append('<div class="gt-grid">')
    for gv in d['graph_views']:
        P.append(f'<div class="gt-card">{graph_type_svg(gv["shape"])}<div class="gt-name">{h(gv["name"])}</div><div class="gt-use">{h(gv["desc"])}</div></div>')
    P.append('</div>')
    # RUNNING EXAMPLES (code)
    P.append('<h2>Running examples</h2>')
    for ex in d['examples']:
        P.append(f'<h3>{h(ex["title"])}</h3>')
        P.append(code_block(ex['code'],ex['lang']))
        P.append(f'<p class="cmp-wnote">{h(ex["note"])}</p>')
    # REAL EXPLORERS (kept)
    P.append('<h2>Real taxonomies, explorable</h2>')
    P.append('<p>Three <strong>real</strong> classification trees — click a folder to expand it, exactly as a knowledge engineer browses a vocabulary:</p>')
    P.extend(tax_explorers_html)
    # CLOSING
    P.append(f'<div class="card cmp-closing">{h(d["closing"])}</div>')
    P.append('</div>')
    return ''.join(P)

def build_comparison_page():
    d=comparison_data()
    if not d: return ''
    P=['<div class="page" id="page-compare"><div class="secnum">Paradigms</div>',
       '<h2>Traditional software development vs. semantic technologies</h2>',
       f'<p>{h(d["intro"])}</p>',
       '<div class="cmp-legend"><span class="cmp-trad">Traditional</span><span class="cmp-vs">vs</span><span class="cmp-sem">Semantic</span></div>']
    def cmp3(title,sub,headers,rows,keyfn):
        out=[f'<h2>{h(title)}</h2>']
        if sub: out.append(f'<p class="note">{h(sub)}</p>')
        hr=''.join(f'<th>{h(x)}</th>' for x in headers)
        body=''.join('<tr>'+keyfn(r)+'</tr>' for r in rows)
        out.append(f'<table class="cmp-table"><thead><tr>{hr}</tr></thead><tbody>{body}</tbody></table>')
        return ''.join(out)
    # DIFFERENCES
    P.append(cmp3('Key differences','',['Dimension','Traditional','Semantic'],
        d['differences'], lambda r:f'<td class="cmp-dim">{h(r["dim"])}</td><td class="cmp-tcell">{h(r["trad"])}</td><td class="cmp-scell">{h(r["sem"])}</td>'))
    # SIMILARITIES
    P.append('<h2>Similarities (more than people expect)</h2>')
    P.append('<ul class="cmp-sim">'+''.join(f'<li>{h(s)}</li>' for s in d['similarities'])+'</ul>')
    # DECISION GUIDE
    P.append('<h2>When to use which — and when to replace</h2>')
    P.append('<div class="cmp-decision"><div class="cmp-dec-col cmp-wtrad"><div class="cmp-wlbl">Choose traditional when…</div><ul>'
             +''.join(f'<li>{h(x)}</li>' for x in d['decision']['use_traditional'])+'</ul></div>'
             '<div class="cmp-dec-col cmp-wsem"><div class="cmp-wlbl">Choose semantic when…</div><ul>'
             +''.join(f'<li>{h(x)}</li>' for x in d['decision']['use_semantic'])+'</ul></div></div>')
    P.append('<h3>Signals it\'s time to REPLACE a layer (with reasons)</h3>')
    for rw in d['decision']['replace_when']:
        P.append(f'<div class="cmp-syn"><div class="cmp-syn-name">{h(rw["sig"])}</div><div class="cmp-syn-how">{h(rw["reason"])}</div></div>')
    P.append(f'<div class="card">{h(d["decision"]["keep_both"])}</div>')
    # FIT / GAP
    P.append(cmp3('Fit / gap analysis','Where each paradigm fits the need, and where it gaps:',['Need','Traditional','Semantic','Best fit'],
        d['fitgap'], lambda r:f'<td class="cmp-dim">{h(r["need"])}</td><td class="cmp-tcell">{h(r["trad"])}</td><td class="cmp-scell">{h(r["sem"])}</td><td class="cmp-verdict cmp-v-{ "t" if r["verdict"]=="Traditional" else "s"}">{h(r["verdict"])}</td>'))
    # RISKS & BENEFITS
    rb=d['risks_benefits']
    P.append('<h2>Risks &amp; benefits</h2>')
    def rbcol(title,cls,data):
        return (f'<div class="cmp-rb-col {cls}"><div class="cmp-wlbl">{h(title)}</div>'
                '<div class="cmp-rb-sub">Benefits</div><ul>'+''.join(f'<li>{h(x)}</li>' for x in data['benefits'])+'</ul>'
                '<div class="cmp-rb-sub cmp-rb-risk">Risks</div><ul>'+''.join(f'<li>{h(x)}</li>' for x in data['risks'])+'</ul></div>')
    P.append('<div class="cmp-decision">'+rbcol('Traditional','cmp-wtrad',rb['trad'])+rbcol('Semantic','cmp-wsem',rb['sem'])+'</div>')
    # METHODOLOGIES
    P.append(cmp3('Methodologies, stage by stage','',['Stage','Traditional','Semantic'],
        d['methodologies'], lambda r:f'<td class="cmp-dim">{h(r["stage"])}</td><td class="cmp-tcell">{h(r["trad"])}</td><td class="cmp-scell">{h(r["sem"])}</td>'))
    # TOOLS WITH LINKS
    P.append('<h2>Tools &amp; libraries — with links</h2>')
    def toolcell(items):
        links=[]
        for name,url in items:
            links.append(f'<a href="{hattr(url)}" target="_blank" rel="noopener">{h(name)} ↗</a>' if url else h(name))
        return ', '.join(links)
    trows=''.join(f'<tr><td class="cmp-dim">{h(t["cat"])}</td><td class="cmp-tcell">{toolcell(t["trad"])}</td><td class="cmp-scell">{toolcell(t["sem"])}</td></tr>' for t in d['tools'])
    P.append(f'<table class="cmp-table"><thead><tr><th>Layer</th><th>Traditional stack</th><th>Semantic stack</th></tr></thead><tbody>{trows}</tbody></table>')
    # MULTIPLE WORKED EXAMPLES
    P.append('<h2>Worked examples — the same problem, both ways</h2>')
    for w in d['worked_multi']:
        P.append(f'<h3>{h(w["title"])}</h3>')
        P.append('<div class="cmp-worked"><div class="cmp-wcol cmp-wtrad"><div class="cmp-wlbl">Traditional</div>'
                 +code_block(w['trad']['code'],w['trad']['lang'])+f'<p class="cmp-wnote">{h(w["trad"]["note"])}</p></div>'
                 '<div class="cmp-wcol cmp-wsem"><div class="cmp-wlbl">Semantic</div>'
                 +code_block(w['sem']['code'],w['sem']['lang'])+f'<p class="cmp-wnote">{h(w["sem"]["note"])}</p></div></div>')
    # GRAPH TYPES (visual)
    P.append('<h2>Representing data with different graph types</h2>')
    P.append('<p class="note">Semantic data isn\'t one shape — different problems call for different graph structures:</p>')
    P.append('<div class="gt-grid">')
    for gt in d['graph_types']:
        P.append(f'<div class="gt-card">{graph_type_svg(gt["shape"])}<div class="gt-name">{h(gt["name"])}</div><div class="gt-use">{h(gt["use"])}</div></div>')
    P.append('</div>')
    # SYNTHESIS PATTERNS
    P.append('<h2>How to synthesize them — architectural patterns</h2>')
    P.append('<p class="note">The strongest systems are hybrids. Concrete ways to combine a traditional core with a semantic layer:</p>')
    for s in d['synthesis']:
        P.append(f'<div class="cmp-syn"><div class="cmp-syn-name">{h(s["pattern"])}</div><div class="cmp-syn-how">{h(s["how"])}</div><div class="cmp-syn-impact"><span class="ct-impact-lbl">Impact</span> {h(s["impact"])}</div></div>')
    # BEST PRACTICES
    P.append('<h2>Best practices</h2>')
    P.append('<ol class="cmp-bp">'+''.join(f'<li>{h(x)}</li>' for x in d['best_practices'])+'</ol>')
    # STATISTICS
    P.append('<h2>By the numbers (researched)</h2>')
    srows=''.join(f'<tr><td>{h(s["stat"])}</td><td class="cmp-statval">{h(s["value"])}</td><td class="cmp-statsrc">{h(s["src"])}</td></tr>' for s in d['statistics'])
    P.append(f'<table class="cmp-table"><thead><tr><th>Metric</th><th>Value</th><th>Source</th></tr></thead><tbody>{srows}</tbody></table>')
    P.append('<p class="note">Market figures vary by analyst; ranges reflect multiple 2025-2026 reports. Treat as directional, not precise.</p>')
    # STATE OF THE ART
    P.append('<h2>State of the art (2024-2026)</h2>')
    P.append('<ul class="cmp-sim">'+''.join(f'<li>{h(x)}</li>' for x in d['state_of_art'])+'</ul>')
    # CLOSING
    P.append(f'<div class="card cmp-closing">{h(d["closing"])}</div>')
    P.append('</div>')
    return ''.join(P)

def build_inference_contrast(d,cid):
    cards=[]
    for i,c in enumerate(d['cards']):
        cb=code_block(c['code'],c['lang'])
        ew=exec_widget(c['steps'],c['result'],f'{cid}_contrast_{i}')
        cards.append(
          '<div class="ic-card" style="border-top:4px solid '+c['color']+'">'
          '<div class="ic-op"><code>'+h(c['op'])+'</code><span class="ic-role" style="color:'+c['color']+'">'+h(c['role'])+'</span></div>'
          +cb+ew+
          '<div class="ic-reads"><span class="ic-reads-lbl">How to read it</span> '+h(c['reads'])+'</div></div>')
    return ('<div class="infcontrast"><div class="ic-title">'+h(d['title'])+'</div>'
            '<p class="ic-lead">'+h(d['lead'])+'</p>'
            '<div class="ic-grid">'+''.join(cards)+'</div>'
            '<div class="ic-summary">'+h(d['summary'])+'</div></div>')

def build_axiom_reference(d):
    out=['<details class="axref"><summary>'+h(d['title'])+'</summary>',
         '<p class="axref-note">'+h(d['note'])+'</p>']
    for grp in d['groups']:
        out.append('<div class="axref-group">'+h(grp['group'])+'</div>')
        rows=''.join('<tr><td class="axref-term"><code>'+h(term)+'</code></td><td>'+h(mean)+'</td>'
                     '<td class="axref-kind axref-'+("d" if "derive" in kind else "c")+'">'+h(kind)+'</td>'
                     '<td class="axref-ex">'+h(ex)+'</td></tr>' for term,mean,kind,ex in grp['items'])
        out.append('<table class="axref-table"><thead><tr><th>Axiom</th><th>Meaning</th><th>Reasoner</th><th>Example</th></tr></thead><tbody>'+rows+'</tbody></table>')
    out.append('</details>')
    return ''.join(out)

def build_primer():
    d=primer_data()
    if not d: return ''
    P=['<div class="primer"><div class="primer-tag">Start here</div>',
       '<h2 class="primer-h">The building blocks: triple, class, property, individual</h2>',
       '<p>'+h(d['intro'])+'</p>']
    # THE TRIPLE
    t=d['triple']
    P.append('<h3>'+h(t['title'])+'</h3><p>'+h(t['text'])+'</p>')
    P.append('<div class="triple-row">'+''.join(
        '<div class="triple-part"><div class="triple-role">'+h(role)+'</div><div class="triple-desc">'+h(desc)+'</div><code class="triple-ex">'+h(ex)+'</code></div>'
        +('<div class="triple-arrow">→</div>' if i<2 else '')
        for i,(role,desc,ex) in enumerate(t['parts']))+'</div>')
    P.append(code_block(t['code'],t['lang']))
    # THE FOUR PRIMITIVES
    P.append('<h3>The four primitives</h3>')
    P.append('<div class="prim-grid">')
    for pr in d['primitives']:
        P.append('<div class="prim-card" style="border-top:4px solid '+pr['color']+'">'
                 '<div class="prim-head"><span class="prim-icon" style="color:'+pr['color']+'">'+h(pr['icon'])+'</span>'
                 '<span class="prim-name">'+h(pr['name'])+'</span><span class="prim-analogy">'+h(pr['analogy'])+'</span></div>'
                 '<p class="prim-is">'+h(pr['is'])+'</p>'
                 '<div class="prim-repr"><span class="prim-repr-lbl">How it is written</span> '+h(pr['repr'])+'</div>'
                 +code_block(pr['code'],'turtle')+'</div>')
    P.append('</div>')
    # HOW THEY RELATE
    P.append('<h3>How they relate</h3>')
    rows=''.join('<tr><td class="cmp-dim">'+h(a)+'</td><td class="rel-pred"><code>'+h(p)+'</code></td><td class="cmp-dim">'+h(b)+'</td><td>'+h(desc)+'</td><td class="rel-ex"><code>'+h(ex)+'</code></td></tr>' for a,p,b,desc,ex in d['relations'])
    P.append('<table class="cmp-table"><thead><tr><th>From</th><th>via</th><th>To</th><th>Meaning</th><th>Example</th></tr></thead><tbody>'+rows+'</tbody></table>')
    P.append('<div class="card">'+h(d['tbox_abox'])+'</div>')
    # ALL-IN-ONE worked example
    w=d['worked']
    P.append('<h3>'+h(w['title'])+'</h3>')
    P.append(code_block(w['code'],w['lang']))
    P.append(exec_widget(w['steps'],w['result'],'primer_allinone'))
    P.append('<div class="card cmp-closing">'+h(d['closing'])+'</div>')
    P.append('</div>')
    return ''.join(P)

def build_prov_legend():
    d=prov_legend()
    if not d: return ''
    cards=''.join('<div class="pl-card" style="border-left:4px solid '+L['color']+'">'
                  '<div class="pl-tag" style="color:'+L['color']+'"><span class="pl-mark">'+h(L['mark'])+'</span> '+h(L['tag'])+'</div>'
                  '<div class="pl-desc">'+h(L['desc'])+'</div></div>' for L in d['levels'])
    return ('<div class="provlegend"><div class="pl-title">'+h(d['title'])+'</div>'
            '<p class="pl-text">'+h(d['text'])+'</p>'
            '<div class="pl-grid">'+cards+'</div>'
            '<div class="pl-rule">'+h(d['rule'])+'</div></div>')

def build_corpus():
    d=corpus_data()
    if not d: return ''
    rg=d['real_grounding']; ii=d['illustrative_instances']
    realrows=''.join('<tr><td>'+h(fact)+'</td><td class="cp-real">'+h(tag)+'</td>'
                     '<td><a href="'+hattr(url)+'" target="_blank" rel="noopener">source ↗</a></td></tr>' for fact,tag,url in rg['facts'])
    illrows=''.join('<tr><td><code>'+h(idn)+'</code></td><td>'+h(what)+'</td><td class="cp-ill">'+h(role)+'</td></tr>' for idn,what,role in ii['items'])
    return ('<div class="corpus"><div class="cp-title">'+h(d['title'])+'</div>'
            '<p>'+h(d['intro'])+'</p>'
            '<div class="cp-sub cp-sub-real">'+h(rg['label'])+'</div>'
            '<table class="cmp-table"><thead><tr><th>Fact</th><th>Status</th><th>Source</th></tr></thead><tbody>'+realrows+'</tbody></table>'
            '<div class="cp-sub cp-sub-ill">'+h(ii['label'])+'</div>'
            '<p class="note">'+h(ii['note'])+'</p>'
            '<table class="cmp-table"><thead><tr><th>Identifier</th><th>What it is</th><th>Status</th></tr></thead><tbody>'+illrows+'</tbody></table>'
            '<div class="card">'+h(d['closing'])+'</div></div>')

def _svg_erd():
    # two entity tables with attributes; FK relationship + self-referencing parent_id
    return ('<svg viewBox="0 0 360 210" class="mc-svg" xmlns="http://www.w3.org/2000/svg">'
      '<g font-family="ui-monospace,monospace" font-size="9">'
      # PRODUCT entity
      '<rect x="14" y="20" width="130" height="74" rx="3" fill="#fff" stroke="#4a7c8c" stroke-width="1.5"/>'
      '<rect x="14" y="20" width="130" height="18" rx="3" fill="#4a7c8c"/>'
      '<text x="79" y="33" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">PRODUCT</text>'
      '<text x="20" y="52">id  (PK)</text><text x="20" y="66">name</text>'
      '<text x="20" y="80" fill="#b5803a">category_id (FK)</text>'
      # CATEGORY entity
      '<rect x="210" y="20" width="135" height="88" rx="3" fill="#fff" stroke="#5b8a72" stroke-width="1.5"/>'
      '<rect x="210" y="20" width="135" height="18" rx="3" fill="#5b8a72"/>'
      '<text x="277" y="33" text-anchor="middle" fill="#fff" font-size="10" font-weight="bold">CATEGORY</text>'
      '<text x="216" y="52">id  (PK)</text><text x="216" y="66">name</text>'
      '<text x="216" y="80" fill="#b5803a">parent_id (FK)</text>'
      # FK product->category
      '<line x1="144" y1="80" x2="210" y2="60" stroke="#888" stroke-width="1.3" marker-end="url(#erdar)"/>'
      '<text x="150" y="74" font-size="8" fill="#586272">N:1</text>'
      # self-ref parent_id (hierarchy)
      '<path d="M345,94 q34,4 30,-30 q-4,-30 -38,-26" fill="none" stroke="#b5803a" stroke-width="1.3" marker-end="url(#erdar)"/>'
      '<text x="300" y="128" font-size="8" fill="#b5803a">parent (self-join = hierarchy)</text>'
      '<text x="14" y="150" font-size="9" fill="#586272">Taxonomy = recursive parent_id; ancestors need a recursive CTE.</text>'
      '<defs><marker id="erdar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#888"/></marker></defs>'
      '</g></svg>')

def _svg_class():
    return ('<svg viewBox="0 0 360 200" class="mc-svg" xmlns="http://www.w3.org/2000/svg">'
      '<g font-family="ui-monospace,monospace" font-size="9">'
      # Product class
      '<rect x="20" y="24" width="120" height="58" fill="#fff" stroke="#5b8a72" stroke-width="1.5"/>'
      '<rect x="20" y="24" width="120" height="18" fill="#eef4f0"/>'
      '<text x="80" y="37" text-anchor="middle" font-weight="bold" font-size="10">Product</text>'
      '<line x1="20" y1="42" x2="140" y2="42" stroke="#5b8a72"/>'
      '<text x="26" y="56">- name: String</text>'
      '<text x="26" y="72">- category: Category</text>'
      # Category class
      '<rect x="215" y="24" width="125" height="58" fill="#fff" stroke="#5b8a72" stroke-width="1.5"/>'
      '<rect x="215" y="24" width="125" height="18" fill="#eef4f0"/>'
      '<text x="277" y="37" text-anchor="middle" font-weight="bold" font-size="10">Category</text>'
      '<line x1="215" y1="42" x2="340" y2="42" stroke="#5b8a72"/>'
      '<text x="221" y="56">- name: String</text>'
      '<text x="221" y="72">- parent: Category</text>'
      # association product->category
      '<line x1="140" y1="60" x2="215" y2="56" stroke="#586272" stroke-width="1.3"/>'
      '<text x="150" y="52" font-size="8" fill="#586272">category 1</text>'
      # self-association parent
      '<path d="M340,66 q30,8 26,-26 q-4,-26 -36,-22" fill="none" stroke="#586272" stroke-width="1.3"/>'
      '<text x="300" y="104" font-size="8" fill="#586272">parent (self-assoc)</text>'
      '<text x="20" y="135" font-size="9" fill="#586272">Hierarchy = parent reference; inheritance is for TYPES, not</text>'
      '<text x="20" y="148" font-size="9" fill="#586272">the category instances.</text>'
      '</g></svg>')

def _svg_object():
    # instance chain: tshirt_A -> womenTshirt -> clothing -> root
    boxes=[('tshirt_A : Product','#b5803a',14),('womenTshirt : Category','#5b8a72',98),('clothing : Category','#5b8a72',182),('root : Category','#5b8a72',266)]
    parts=['<svg viewBox="0 0 360 200" class="mc-svg" xmlns="http://www.w3.org/2000/svg"><g font-family="ui-monospace,monospace" font-size="8">']
    y=30
    for i,(lbl,col,x) in enumerate(boxes):
        parts.append(f'<rect x="14" y="{y}" width="200" height="22" rx="3" fill="#fff" stroke="{col}" stroke-width="1.5"/>')
        parts.append(f'<text x="22" y="{y+14}" font-weight="bold" text-decoration="underline">{lbl}</text>')
        if i<len(boxes)-1:
            lab='category' if i==0 else 'parent'
            parts.append(f'<line x1="114" y1="{y+22}" x2="114" y2="{y+34}" stroke="#888" stroke-width="1.2" marker-end="url(#obar)"/>')
            parts.append(f'<text x="120" y="{y+31}" fill="#586272">{lab} →</text>')
        y+=34
    parts.append('<defs><marker id="obar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#888"/></marker></defs>')
    parts.append('<text x="230" y="60" font-size="9" fill="#586272">A specific</text><text x="230" y="74" font-size="9" fill="#586272">product walking</text><text x="230" y="88" font-size="9" fill="#586272">up its category</text><text x="230" y="102" font-size="9" fill="#586272">chain — followed</text><text x="230" y="116" font-size="9" fill="#586272">by code.</text>')
    parts.append('</g></svg>')
    return ''.join(parts)

def _svg_semantic():
    # node-link: product -inCategory-> tshirt_cat -broader-> clothing -broader-> root ; shared IRIs
    return ('<svg viewBox="0 0 360 200" class="mc-svg" xmlns="http://www.w3.org/2000/svg">'
      '<g font-family="ui-monospace,monospace" font-size="8">'
      '<defs><marker id="sear" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#9a5b6e"/></marker></defs>'
      # product node
      '<ellipse cx="60" cy="40" rx="46" ry="18" fill="#fbeef2" stroke="#9a5b6e" stroke-width="1.5"/><text x="60" y="38" text-anchor="middle">ex:tshirt_A</text><text x="60" y="48" text-anchor="middle" font-size="7" fill="#9a5b6e">a :TShirt</text>'
      # category nodes (skos:Concept) in a hierarchy
      '<ellipse cx="200" cy="40" rx="52" ry="18" fill="#fff" stroke="#5b8a72" stroke-width="1.5"/><text x="200" y="38" text-anchor="middle">ex:tshirt_cat</text><text x="200" y="48" text-anchor="middle" font-size="7" fill="#5b8a72">skos:Concept</text>'
      '<ellipse cx="200" cy="105" rx="52" ry="18" fill="#fff" stroke="#5b8a72" stroke-width="1.5"/><text x="200" y="103" text-anchor="middle">ex:clothing</text><text x="200" y="113" text-anchor="middle" font-size="7" fill="#5b8a72">skos:Concept</text>'
      '<ellipse cx="200" cy="168" rx="46" ry="17" fill="#fff" stroke="#5b8a72" stroke-width="1.5"/><text x="200" y="171" text-anchor="middle">ex:root</text>'
      # edges
      '<line x1="106" y1="40" x2="148" y2="40" stroke="#9a5b6e" stroke-width="1.3" marker-end="url(#sear)"/><text x="127" y="33" text-anchor="middle" font-size="7" fill="#9a5b6e">:inCategory</text>'
      '<line x1="200" y1="58" x2="200" y2="87" stroke="#5b8a72" stroke-width="1.3" marker-end="url(#sear)"/><text x="244" y="76" font-size="7" fill="#5b8a72">skos:broader</text>'
      '<line x1="200" y1="123" x2="200" y2="151" stroke="#5b8a72" stroke-width="1.3" marker-end="url(#sear)"/><text x="244" y="140" font-size="7" fill="#5b8a72">skos:broader</text>'
      '<text x="14" y="194" font-size="8.5" fill="#586272">Taxonomy is first-class &amp; traversable; categories are shared IRIs.</text>'
      '</g></svg>')

_MC_SVG={'erd':strict_erd,'class':strict_uml_class,'object':strict_uml_object,'semantic':strict_semantic}

def build_model_comparison(d):
    lenses=''
    for L in d['lenses']:
        svg=_MC_SVG.get(L['diagram'],lambda:'')()
        lenses+=('<div class="mc-card" style="border-top:4px solid '+L['color']+'">'
                 '<div class="mc-card-t" style="color:'+L['color']+'">'+h(L['title'])+'</div>'
                 '<div class="mc-diagram">'+svg+'</div>'
                 +code_block(L['code'],'text')+
                 '<div class="mc-note">'+h(L['note'])+'</div></div>')
    t=d['table']
    head=''.join('<th>'+h(c)+'</th>' for c in t['cols'])
    rows=''.join('<tr><td class="mc-aspect">'+h(r[0])+'</td>'+''.join('<td>'+h(c)+'</td>' for c in r[1:])+'</tr>' for r in t['rows'])
    return ('<div class="modelcmp"><div class="mc-title">'+h(d['title'])+'</div>'
            '<p class="mc-intro">'+h(d['intro'])+'</p>'
            '<div class="mc-grid">'+lenses+'</div>'
            '<table class="cmp-table mc-table"><thead><tr>'+head+'</tr></thead><tbody>'+rows+'</tbody></table>'
            '<div class="mc-takeaway">'+h(d['takeaway'])+'</div></div>')

def build_tech_compare_rich(d):
    if not d: return ''
    cards=''
    for t in d['techs']:
        rec = ' tcr-recommended' if t.get('recommended') else ''
        badge = '<span class="tcr-badge">purpose-built</span>' if t.get('recommended') else ''
        if t.get('repr_kind')=='table' and t.get('table'):
            tb=t['table']
            head=''.join('<th>'+h(c)+'</th>' for c in tb['cols'])
            rows=''.join('<tr>'+''.join('<td>'+h(str(c))+'</td>' for c in r)+'</tr>' for r in tb['rows'])
            repr_html='<table class="tcr-table"><thead><tr>'+head+'</tr></thead><tbody>'+rows+'</tbody></table>'
            if t.get('code'): repr_html+=code_block(t['code'],t.get('lang','sql'))
        else:
            repr_html=code_block(t.get('code',''),t.get('lang','turtle'))
        cards+=('<div class="tcr-card'+rec+'" style="border-top:4px solid '+t.get('color','#888')+'">'
                '<div class="tcr-tech" style="color:'+t.get('color','#333')+'">'+h(t['tech'])+badge+'</div>'
                +repr_html+
                '<div class="tcr-note">'+h(t['note'])+'</div></div>')
    # capability summary table
    summ=''
    if d.get('table_summary'):
        ts=d['table_summary']
        head=''.join('<th>'+h(c)+'</th>' for c in ts['cols'])
        rows=''
        for r in ts['rows']:
            cells='<td class="tcr-cap">'+h(str(r[0]))+'</td>'
            for c in r[1:]:
                cls='tcr-yes' if str(c).lower().startswith(('yes','native')) else ('tcr-no' if str(c).lower() in ('no','') else 'tcr-mid')
                cells+='<td class="'+cls+'">'+h(str(c))+'</td>'
            rows+='<tr>'+cells+'</tr>'
        summ=('<div class="tcr-summary-lbl">Capability comparison</div>'
              '<table class="cmp-table tcr-summary"><thead><tr>'+head+'</tr></thead><tbody>'+rows+'</tbody></table>')
    return ('<div class="techrich"><div class="tcr-head"><span class="tcr-lbl">How other technologies would handle this</span></div>'
            '<p class="tcr-scenario">'+h(d['scenario'])+'</p>'
            '<div class="tcr-grid">'+cards+'</div>'+summ+'</div>')

def layered_arch(c):
    v=g.value(c,SCP.layeredArchitecture); return _json.loads(str(v)) if v else None

def build_layered_arch(d):
    if not d: return ''
    # stacked layers as horizontal bands (standard layered-architecture notation), top=most concrete
    W=560; pad=14; lh=78; gap=30; n=len(d['layers'])
    H=pad*2 + n*lh + (n-1)*gap + 16
    svg=[f'<svg class="la-svg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="ui-sans-serif,system-ui,sans-serif">']
    svg.append('<defs><marker id="ladown" markerWidth="9" markerHeight="9" refX="4" refY="7" orient="auto"><path d="M1,1 L7,1 L4,7 Z" fill="#888"/></marker></defs>')
    y=pad
    for i,L in enumerate(d['layers']):
        col=L.get('color','#5b8a72')
        svg.append(f'<rect x="{pad}" y="{y}" width="{W-2*pad}" height="{lh}" rx="8" fill="#fff" stroke="{col}" stroke-width="2"/>')
        svg.append(f'<rect x="{pad}" y="{y}" width="6" height="{lh}" rx="3" fill="{col}"/>')
        svg.append(f'<text x="{pad+16}" y="{y+20}" font-size="12" font-weight="bold" fill="{col}">{h(L["name"])}</text>')
        # role (word-aware wrap)
        role=L['role']; words=role.split(); line1=''; line2=''
        for w in words:
            if len(line1)+len(w)+1<=72: line1=(line1+' '+w).strip()
            else: line2=(line2+' '+w).strip()
        svg.append(f'<text x="{pad+16}" y="{y+37}" font-size="9.5" fill="#586272">{h(line1)}</text>')
        if line2:
            svg.append(f'<text x="{pad+16}" y="{y+50}" font-size="9.5" fill="#586272">{h(line2[:90])}</text>')
        # contents as chips
        cx=pad+16; cyc=y+lh-14
        for item in L['contents']:
            wch=8+len(item)*6.0
            svg.append(f'<rect x="{cx}" y="{cyc-12}" width="{wch}" height="17" rx="8" fill="{col}22" stroke="{col}66"/>')
            svg.append(f'<text x="{cx+wch/2}" y="{cyc}" font-size="9" text-anchor="middle" fill="{col}" font-family="ui-monospace,monospace">{h(item)}</text>')
            cx+=wch+7
        # dependency arrow to the layer below
        if i<n-1:
            ay=y+lh; svg.append(f'<line x1="{W/2}" y1="{ay}" x2="{W/2}" y2="{ay+gap}" stroke="#888" stroke-width="1.4" marker-end="url(#ladown)"/>')
            svg.append(f'<text x="{W/2+8}" y="{ay+gap/2+3}" font-size="8.5" fill="#888" font-style="italic">«{h(d["dependency"])}»</text>')
        y+=lh+gap
    svg.append(f'<text x="{pad}" y="{H-4}" font-size="8.5" fill="#586272">Lower tiers are shared/abstract; upper tiers are concrete. Arrows = import/anchor dependency.</text>')
    svg.append('</svg>')
    # mapping table
    m=d['mapping']
    head=''.join('<th>'+h(c)+'</th>' for c in m['cols'])
    rows=''.join('<tr>'+''.join('<td>'+h(str(c))+'</td>' for c in r)+'</tr>' for r in m['rows'])
    table=('<div class="la-maplbl">Example: anchoring domain terms to the foundational layer</div>'
           '<table class="cmp-table la-map"><thead><tr>'+head+'</tr></thead><tbody>'+rows+'</tbody></table>')
    return ('<div class="layered"><div class="la-head"><span class="la-lbl">'+h(d['title'])+'</span></div>'
            '<p class="la-intro">'+h(d['intro'])+'</p>'+''.join(svg)+table+
            '<p class="la-take">'+h(d['takeaway'])+'</p></div>')

def concept_block(c):
    lbl=h(label(c)); d=ext(c) or defn(c); ex=example(c); vis=visual(c); src=source(c)
    ic=icon(c); icon_html=f'<span class="cicon">{ic}</span> ' if ic else ''
    parts=[f'<h3 class="concept-h" id="concept-{loc(c)}" data-def="{hattr(defn(c))}" data-src="{hattr(src)}" data-label="{hattr(label(c))}">{icon_html}{lbl}</h3>']
    # tooltip-bearing lead term: wrap label term inline
    parts.append(f'<p><span class="term" data-tip="{hattr(defn(c))}">{lbl}</span> — {h(d)}</p>')
    trace(f'concept:{loc(c)}',c,EXT,None)
    vsvg=concept_svg(vis) if vis else ''
    if vsvg: parts.append(vsvg); trace(f'visual:{loc(c)}',c,VIS,None)
    # multi-domain example cases, rendered as a tabbed comparison (each with its own visual)
    cs_list=cases(c); cid=loc(c)
    concept_snip,concept_lang=code(c)
    concept_steps,concept_result=execdata(c)
    if cs_list:
        tabs=''.join(f'<button class="ex-tab{" active" if i==0 else ""}" data-ex="{cid}" data-i="{i}">{h(dom)}</button>' for i,(dom,txt,v,gr,k) in enumerate(cs_list))
        panes=''
        for i,(dom,txt,v,gr,k) in enumerate(cs_list):
            # domain-specific diagram from THIS case's own graph (changes when tab changes)
            visual_html=render_case_graph(gr,cid,i) if gr else (concept_svg(v) if v else '')
            # domain-specific code + execution (fall back to concept-level only if case has none)
            ccode,clang=casecode(k)
            csteps,cresult=caseexec(k)
            if not ccode and i==0 and concept_snip:  # show concept code on first tab if no case code anywhere
                ccode,clang=concept_snip,concept_lang; csteps,cresult=concept_steps,concept_result
            code_html=''
            if ccode:
                code_html=code_block(ccode,clang)
                if ccode: code_html+=build_syntax_notes(None,f'{cid}_{i}',ccode)
                _idg=case_idgloss(k)
                if _idg:
                    code_html+=build_id_glossary(_idg,f'{cid}_{i}'); trace(f'idgloss:{cid}',c,SCP.idGlossary,None)
                if csteps and cresult:
                    code_html+=exec_widget(csteps,cresult,f'{cid}_{i}')
                trace(f'casecode:{cid}:{dom}',c,SCP.caseCode,None)
            panes+=(f'<div class="ex-pane{" active" if i==0 else ""}" id="ex-{cid}-{i}">'
                    f'<div class="ex-domain">{h(dom)} <span class="ex-domain-tag">domain</span></div>'
                    f'<div class="ex-grid"><div class="ex-diagram">{visual_html}</div>'
                    f'<p class="ex-text">{h(txt)}</p></div>{code_html}</div>')
            trace(f'case:{cid}:{dom}',c,SCP.caseGraph,None)
        compare_hint='<span class="ex-compare">↔ switch domains — diagram, code and result all change</span>' if len(cs_list)>1 else ''
        parts.append(f'<div class="ex-block"><div class="ex-head"><span class="ex-lbl">Examples</span> {compare_hint}</div>'
                     f'<div class="ex-tabs">{tabs}</div>{panes}</div>')
    elif concept_snip:
        # concept has code but no domain cases -> render once
        parts.append(code_block(concept_snip,concept_lang)); trace(f'code:{cid}',c,SCP.codeSnippet,None)
        if concept_steps and concept_result:
            parts.append(exec_widget(concept_steps,concept_result,cid)); trace(f'exec:{cid}',c,SCP.execResult,None)
    # inverseOf vs disjointWith contrast + axiom reference (OWL concept)
    ic=inference_contrast(c)
    if ic:
        parts.append(build_inference_contrast(ic,cid)); trace(f'contrast:{cid}',c,SCP.inferenceContrast,None)
    axr=axiom_reference(c)
    if axr:
        parts.append(build_axiom_reference(axr)); trace(f'axref:{cid}',c,SCP.axiomReference,None)
    # layered ontology architecture diagram (rendered once, on FoundationalOntology) — replaces repeated pyramids
    la=layered_arch(c)
    if la:
        parts.append(build_layered_arch(la)); trace(f'layered:{cid}',c,SCP.layeredArchitecture,None)
    # cross-technology TAB (same example across technologies + impacts)
    ct=crosstech(c)
    if ct:
        parts.append(build_cross_tech(ct,cid)); trace(f'crosstech:{cid}',c,SCP.crossTech,None)
    # "How other technologies would handle this" — prefer the RICH version (actual representation in each
    # technology + capability table); fall back to the text-only prose where rich isn't authored.
    tcr=techcompare_rich(c)
    if tcr:
        parts.append(build_tech_compare_rich(tcr)); trace(f'techcompare_rich:{cid}',c,SCP.techCompareRich,None)
    else:
        tc=techcompare(c)
        if tc:
            parts.append(build_tech_compare(tc)); trace(f'techcompare:{cid}',c,SCP.techCompare,None)
    # TBox/ABox/RBox/SHACL explainer (where present) — explains the distinctions explicitly
    exp=explainer(c)
    if exp:
        parts.append(build_explainer(exp)); trace(f'explainer:{cid}',c,SCP.explainerData,None)
    # categorization across modelling paradigms (ERD / class / object vs semantic) — replaces low-value anim
    mc=model_comparison(c)
    if mc:
        parts.append(build_model_comparison(mc)); trace(f'modelcmp:{cid}',c,SCP.modelComparison,None)
    # NOTE: per-concept example animations removed (v21): they were fixed per concept, did not reflect the
    # selected example domain, and duplicated the step-through exec widget without adding explanatory value.
    # real industry ontology where this concept is used in production
    ilab,ilink,inote=industry(c)
    if ilink:
        parts.append(f'<div class="industry"><span class="ind-lbl">In production</span> '
                     f'<a href="{hattr(ilink)}" target="_blank" rel="noopener">{h(ilab)} ↗</a>'
                     f'<span class="ind-note"> — {h(inote)}</span></div>')
        trace(f'industry:{cid}',c,SCP.industryLink,None)
    # external resource + related-concept links (access to external/internal resources)
    links=[]
    ru,rl=reslink(c)
    if ru: links.append(f'<a class="reslink" href="{hattr(ru)}" target="_blank" rel="noopener">↗ {h(rl)}</a>'); trace(f'reslink:{cid}',c,SCP.resourceLink,None)
    rel=related(c)
    if rel:
        rlinks=' '.join(f'<a class="rellink" data-goto-concept="{rid}">{h(rlab)}</a>' for rid,rlab in rel)
        links.append(f'<span class="rel-wrap">Related: {rlinks}</span>')
        for rid,_ in rel: trace(f'related:{cid}:{rid}',c,SCP.relatedConcept,None)
    if links: parts.append(f'<div class="links-row">{"  ·  ".join(links)}</div>')
    return '\n'.join(parts)


def model_diagram(kind,aid):
    """Generated model diagram per area: stack_model, class_model, graph_model, concept_map."""
    if kind=='graph_model':
        s='<svg viewBox="0 0 560 230" class="model-svg"><defs><marker id="gm" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#888"/></marker></defs>'
        nodes=[(70,40,'ex:supplier_1','#4a7c8c'),(70,150,'ex:supplier_2','#4a7c8c'),(260,95,'ex:dc_1','#5b8a72'),(450,40,'ex:store_1','#b5803a'),(450,110,'ex:store_2','#b5803a'),(450,180,'ex:tshirt_A','#9a5b6e')]
        edges=[(140,52,230,90),(140,158,230,110),(330,88,420,52),(330,98,420,118),(330,108,420,180)]
        for x1,y1,x2,y2 in edges: s+=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#aaa" marker-end="url(#gm)"/>'
        for x,y,t,col in nodes: s+=f'<g><rect x="{x-55}" y="{y-13}" width="110" height="26" rx="13" fill="{col}"/><text x="{x}" y="{y+4}" fill="#fff" text-anchor="middle" font-size="10">{t}</text></g>'
        return s+'<text x="280" y="220" text-anchor="middle" font-size="10" fill="#586272">RDF graph model — nodes are entities, edges are relations (the knowledge graph)</text></svg>'
    if kind=='class_model':
        s='<svg viewBox="0 0 560 230" class="model-svg"><defs><marker id="cm" markerWidth="12" markerHeight="12" refX="10" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="none" stroke="#888"/></marker></defs>'
        boxes=[(230,12,'\u00abfoundational\u00bb Entity','#2d4a52'),(120,90,'SupplyChainNode','#5b8a72'),(360,90,'SCMProcess','#5b8a72'),(120,165,'RetailStore','#b5803a'),(360,165,'Replenishment','#b5803a')]
        for x,y,t,col in boxes: s+=f'<g><rect x="{x-90}" y="{y}" width="180" height="34" rx="3" fill="#fff" stroke="{col}" stroke-width="2"/><text x="{x}" y="{y+21}" text-anchor="middle" font-size="10" fill="{col}">{t}</text></g>'
        s+='<line x1="180" y1="90" x2="290" y2="46" stroke="#888" marker-end="url(#cm)"/><line x1="400" y1="90" x2="310" y2="46" stroke="#888" marker-end="url(#cm)"/>'
        s+='<line x1="170" y1="165" x2="180" y2="124" stroke="#888" marker-end="url(#cm)"/><line x1="410" y1="165" x2="400" y2="124" stroke="#888" marker-end="url(#cm)"/>'
        return s+'<text x="280" y="218" text-anchor="middle" font-size="10" fill="#586272">class model — generalization from foundational to domain to application</text></svg>'
    if kind=='stack_model':
        s='<svg viewBox="0 0 560 210" class="model-svg">'
        for t,y,c in [('IRI \u00b7 identity',30,'#4a7c8c'),('RDF \u00b7 model',56,'#527e88'),('RDFS \u00b7 schema',82,'#5b8a72'),('OWL \u00b7 ontology',108,'#b5803a'),('SPARQL \u00b7 query / SHACL \u00b7 validate',134,'#9a5b6e'),('SKOS \u00b7 PROV-O \u00b7 serializations',160,'#6a6a8a')]:
            s+=f'<g><rect x="80" y="{y}" width="400" height="22" rx="3" fill="{c}"/><text x="280" y="{y+15}" text-anchor="middle" fill="#fff" font-size="10">{t}</text></g>'
        return s+'<text x="280" y="200" text-anchor="middle" font-size="10" fill="#586272">stack model — each W3C layer builds on those below (the layer cake)</text></svg>'
    if kind=='concept_map':
        s='<svg viewBox="0 0 560 200" class="model-svg"><defs><marker id="pm" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#888"/></marker></defs>'
        s+='<g><ellipse cx="280" cy="40" rx="90" ry="22" fill="#2d4a52"/><text x="280" y="45" fill="#fff" text-anchor="middle" font-size="11">Semantic Web</text></g>'
        for x,y,t in [(110,130,'Vision (2001)'),(280,140,'Ontology (Gruber 93)'),(450,130,'KG synthesis (2021)')]:
            s+=f'<line x1="280" y1="62" x2="{x}" y2="{y-18}" stroke="#aaa" marker-end="url(#pm)"/><g><rect x="{x-75}" y="{y-18}" width="150" height="30" rx="6" fill="#fff" stroke="#5b8a72"/><text x="{x}" y="{y}" text-anchor="middle" font-size="9" fill="#1a222d">{t}</text></g>'
        return s+'<text x="280" y="190" text-anchor="middle" font-size="10" fill="#586272">concept map — the founding ideas and their relations</text></svg>'
    return ''


# (anim_demo removed in v21 — animations retired)

def quiz_bank():
    v=g.value(SCP.quizBank,SCP.quizBank); return _json.loads(str(v)) if v else []

def build_quiz_page():
    qb=quiz_bank()
    if not qb: return ''
    # group by section
    from collections import OrderedDict
    secs=OrderedDict()
    for i,q in enumerate(qb):
        secs.setdefault(q['sec'],[]).append((i,q))
    typebadge={'deduce':'deduce','concept':'concept','error':'spot the error'}
    typecol={'deduce':'#4a7c8c','concept':'#5b8a72','error':'#a4502f'}
    body=[]
    for sec,items in secs.items():
        body.append(f'<h3 class="qp-sec">{h(sec)}</h3>')
        for qi,q in items:
            tb=typebadge.get(q['type'],q['type']); tc=typecol.get(q['type'],'#586272')
            code=('<pre class="qp-code"><code>'+h(q['code'])+'</code></pre>') if q.get('code') else ''
            opts=''.join(f'<div class="qp-opt" data-q="{qi}" data-o="{oi}">{h(o)}</div>' for oi,o in enumerate(q['opts']))
            body.append(
              f'<div class="qp-q" id="qpq-{qi}" data-correct="{q["correct"]}">'
              f'<div class="qp-qhead"><span class="qp-type" style="background:{tc}">{h(tb)}</span>'
              f'<span class="qp-qtext">{qi+1}. {h(q["q"])}</span></div>'
              f'{code}<div class="qp-opts">{opts}</div>'
              f'<div class="qp-explain" id="qpe-{qi}"><strong>Why:</strong> {h(q["explain"])}</div>'
              f'</div>')
    n=len(qb)
    return ('<div class="page" id="page-quiz"><div class="secnum">Self-check</div>'
            '<h2>Comprehensive self-check quiz</h2>'
            f'<p class="note">{n} questions across every section — a mix of <em>deduction</em> (read the code, work out the result), '
            '<em>concept</em> (why it works), and <em>spot-the-error</em>. Pick an answer to see if it is right and read the explanation. '
            'Your running score is tracked below.</p>'
            '<div class="qp-scorebar"><span id="qp-score">0</span> / '+str(n)+' answered correctly '
            '<button class="qp-reset" id="qp-reset">reset</button></div>'
            +''.join(body)+
            '<div class="qp-final" id="qp-final"></div></div>')

def build_sidebar():
    """Persistent MS-Explorer left nav, styled like a file explorer (folder/file rows + indent guides).
    Two clean groups so flat pages and deep folders are not mixed: BROWSE (area->concept tree) and PAGES."""
    out=['<aside class="sidebar"><div class="sb-titlebar"><span class="sb-title">Explorer</span>'
         '<span class="sb-tools"><button class="sb-btn" id="sb-openall" title="Expand all folders">expand all</button>'
         '<button class="sb-btn" id="sb-closeall" title="Collapse all folders">collapse all</button></span></div>'
         '<nav class="sb-tree">']
    # ---- group 1: BROWSE (the concept tree) ----
    def short_area_name(a):  # ontology-driven: use scp:shortLabel if present, else truncate the label
        sl=g.value(a,SCP.shortLabel)
        return str(sl) if sl else label(a).split('—')[0].strip()[:18]
    out.append('<div class="msx-root">')
    for a in areas:
        aid=loc(a); cs=concepts_of(a); full=label(a).split('—')[0].strip(); short=short_area_name(a)
        out.append(
          f'<div class="msx-row msx-folder" data-sf="{aid}" data-tip="{hattr(full)}" '
          f'data-ctx="area" data-goto="{aid}" data-label="{hattr(full)}">'
          f'<span class="msx-tw">▸</span><span class="msx-ico">📁</span>'
          f'<span class="msx-name">{h(short)}</span><span class="msx-count">{len(cs)}</span></div>')
        out.append(f'<div class="msx-children" id="sbch-{aid}">')
        for c in cs:
            out.append(
              f'<div class="msx-row msx-file" data-goto="{aid}" data-anchor="concept-{loc(c)}" '
              f'data-tip="{hattr(defn(c))}" data-ctx="concept" data-label="{hattr(label(c))}" '
              f'data-src="{hattr(source(c) or "")}" tabindex="0">'
              f'<span class="msx-ico">📄</span><span class="msx-name">{h(label(c))}</span></div>')
        out.append('</div>')
    out.append('</div>')
    out.append('</nav></aside>')
    return ''.join(out)

def build_examples_catalog():
    """Catalog every worked example: concept, domain, what it demonstrates, how it is used."""
    # gather cases grouped by concept (in area order)
    by_concept={}
    for k in g.subjects(SCP.ofConcept,None):
        c=g.value(k,SCP.ofConcept)
        by_concept.setdefault(c,[]).append(k)
    rows=[]
    # iterate areas->concepts for stable order
    seen=set()
    ordered=[]
    for a in areas:
        for c in concepts_of(a):
            if c in by_concept: ordered.append(c); seen.add(c)
    for c in by_concept:
        if c not in seen: ordered.append(c)
    n=0
    sections=[]
    for c in ordered:
        ks=sorted(by_concept[c],key=lambda k:str(g.value(k,SCP.exampleDomain) or ''))
        cards=[]
        for k in ks:
            dom=str(g.value(k,SCP.exampleDomain) or '—')
            txt=str(g.value(k,SCP.exampleText) or '')
            lang=str(g.value(k,SCP.caseCodeLang) or g.value(k,SCP.codeLang) or '')
            # 'what it demonstrates' = first sentence of exampleText; 'how used' = derived from lang/concept
            what=txt.split('. ')[0].strip()
            if what and not what.endswith('.'): what+='.'
            # concept-aware usage note: what you DO with this specific example
            cl=loc(c)
            usage_by_lang={
              'sparql':'Run this query against the graph to retrieve the matching results.',
              'sql':'Contrast case — the same task in relational SQL, for comparison.',
              'cypher':'Contrast case — the same task in property-graph Cypher.',
              'python':'Programmatic use — run this code to drive retrieval / processing.',
              'json':'A JSON / JSON-LD serialization of the same data.',
            }
            usage_by_concept={
              'SKOS':'Load into a vocabulary so any of the labels resolves to the one concept.',
              'OWL':'Load into a reasoner to derive new facts or detect contradictions.',
              'RDFS':'Load into a reasoner to infer types up the subclass hierarchy.',
              'SHACL':'Validate data against this shape — conforming data passes, violations are flagged.',
              'PROVO':'Attach to records to capture an auditable who/what/when provenance trail.',
              'RDF':'Load these triples into a triple store as the base data.',
              'TBoxABoxRBox':'Load all three tiers together so the reasoner combines schema, data and roles.',
              'FoundationalOntology':'Anchor domain terms to these upper categories for interoperability.',
              'PropertyGraph':'Model entities and relationships as a traversable property graph.',
              'RelationalModel':'Baseline relational design — shown to contrast with the graph approach.',
              'GraphRAG':'Retrieve a connected subgraph to ground an LLM answer.',
              'Embeddings':'Embed entities as vectors so proximity predicts related items.',
              'KGOrigin':'Background example illustrating how knowledge graphs are built.',
              'OntologyDefinition':'Writes down a shared conceptualization formally as a vocabulary/schema.',
              'SemanticWebVision':'Illustrates the vision: machine-readable data agents can combine and act on.',
            }
            usage = usage_by_lang.get(lang.lower()) or usage_by_concept.get(cl) or 'Illustrative snippet for this concept.'
            if lang.lower() in ('turtle','rdf','ttl') and cl in usage_by_concept:
                usage = usage_by_concept[cl]
            n+=1
            cards.append(
              f'<tr><td class="ec-dom">{h(dom)}</td>'
              f'<td class="ec-what">{h(what)}</td>'
              f'<td class="ec-lang">{h(lang or "—")}</td>'
              f'<td class="ec-use">{h(usage)}</td>'
              f'<td><span class="ec-link" data-goto="{loc(area_of(c))}" data-anchor="concept-{loc(c)}" data-tip="Jump to this example in the {h(label(c))} concept">open ↗</span></td></tr>')
        sections.append(
          f'<h3 class="ec-concept">{h(label(c))}</h3>'
          f'<table class="ec-table"><thead><tr><th>Domain</th><th>What it demonstrates</th>'
          f'<th>Form</th><th>How it is used</th><th></th></tr></thead><tbody>'+''.join(cards)+'</tbody></table>')
    return ('<div class="page" id="page-examples"><div class="secnum">Worked examples</div>'
            '<h2>Examples catalog</h2>'
            f'<p class="note">Every worked example on this page in one place — {n} examples across '
            f'{len(ordered)} concepts. Each row says what the example demonstrates and how that form is used; '
            'click <em>open ↗</em> to jump to it in context.</p>'
            +''.join(sections)+'</div>')

def area_of(c):
    for a in areas:
        if c in concepts_of(a): return a
    return areas[0] if areas else c

def page():
    # ---- SPA pages: overview, one per area, sims, quiz, refs ----
    def short_area_name2(a):
        sl=g.value(a,SCP.shortLabel)
        return str(sl) if sl else label(a).split('—')[0].strip()[:12]
    menu=[('overview','Overview','The landing page: intro, concept explorer and provenance key.')]
    for a in areas:
        full=label(a).split('—')[0].strip(); aid=loc(a)
        menu.append((aid, short_area_name2(a), full))
    menu+=[('sims','Taxonomies','Deep dive on taxonomies with real explorer trees.'),
           ('compare',_COMPARE_SHORT,_COMPARE_LABEL+': when to use each approach.'),
           ('examples','Examples','Catalog of every worked example, with what it shows and how it is used.'),
           ('quiz','Self-check','Comprehensive quiz across every section.'),
           ('refs','References','The cited source publications.')]
    nav='<nav class="primary-nav" aria-label="Primary navigation">'+''.join(f'<button class="tab{ " active" if i=="overview" else ""}" data-p="{i}" data-tip="{hattr(tip)}">{h(n)}</button>' for i,n,tip in menu)+'</nav>'

    pages=[]
    # OVERVIEW page: intro + MS-Explorer tree (collapsible) + reframed short summary
    tree=['<div class="explorer">']
    for a in areas:
        aid=loc(a)
        tree.append(f'<div class="folder" data-f="{aid}"><span class="tw">▸</span> <span class="fname">{h(label(a))}</span> <span class="count">{len(concepts_of(a))}</span></div>')
        tree.append(f'<div class="children" id="ch-{aid}">')
        for c in concepts_of(a):
            tree.append(f'<div class="item" data-tip="{hattr(defn(c))}" data-goto="{aid}">📄 {h(label(c))}</div>')
        tree.append('</div>')
    tree.append('</div>')
    trace('explorer:tree',AXIS,RDF.type,OWL.Class)
    overview=f'''<div class="page active" id="page-overview"><div class="secnum">Pipeline-generated · semantic technologies</div>
<h1>{h(_PAGE_TITLE)}</h1>
<div class="sub">An interactive treatment of semantic technologies, illustrated with worked examples across retail, logistics, healthcare, finance and other domains. Example <em>schemas</em> are grounded in real, cited public sources; example <em>instances</em> are clearly-marked illustrative data (see the provenance key below).</div>
<div class="card">Use the top menu to move between areas, or the explorer below to jump to a concept. This page was produced by <code>gen_render_deployed v30</code> from <code>scp_domain v3.15.0</code> ({len(classes)} classes, {len(pubs)} references). Right-click a concept heading for its definition and source; hover any <span class="term" data-tip="a highlighted term shows its definition on hover">highlighted term</span> for a tooltip.</div>
<h3>Concept explorer</h3>
<p class="note">Click a folder to expand or collapse it; click a concept to open its area.</p>
{''.join(tree)}
{build_prov_legend()}
{build_corpus()}</div>'''
    pages.append(overview)

    # AREA pages
    areafig={}
    for a in areas:
        aid=loc(a); cs=concepts_of(a)
        # reframed SHORT table: concept + grounded-in only (narrative carries the rest)
        srows=[(f'<span class="term" data-tip="{hattr(defn(c))}">{h(label(c))}</span>',h(source(c) or '—')) for c in cs]
        defrows=[(h(label(c)),h(defn(c))) for c in cs]
        mk=modelkind(a); model_html=(f'<h3>Model</h3><div class="model-wrap">{model_diagram(mk,aid)}</div>' if mk else '')
        if mk: trace(f'model:{aid}',a,SCP.modelKind,None)
        body=[f'<div class="page" id="page-{aid}"><div class="secnum">Area</div><h2>{h(label(a))}</h2>',
              f'<p>{h(ext(a) or defn(a))}</p>',
              (build_primer() if aid=='Foundations' else ''),
              model_html,
              f'<div class="card"><strong>Concepts in this area</strong> — {", ".join(h(label(c)) for c in cs)}.</div>',
              f'<h2>{h(label(a))} — concepts at a glance</h2>',
              f'<p class="note">A short index before the detailed treatment:</p>',
              short_table(['Concept','In one line'],defrows)]
        # per-concept blocks (prose + example + diagram), the heavy content
        body.append(f'<h2>{h(label(a))} — concept treatments</h2>')
        for c in cs: body.append(concept_block(c))
        # area-level rich tech comparison (e.g. KnowledgeGraphs vs relational/document)
        area_tcr=techcompare_rich(a)
        if area_tcr:
            body.append(build_tech_compare_rich(area_tcr)); trace(f'techcompare_rich:{aid}',a,SCP.techCompareRich,None)
        # short grounding table AFTER the narrative it supports
        body.append('<h2>Grounding summary</h2>')
        body.append(f'<p class="note">Each concept above traces to a source publication:</p>')
        body.append(short_table(['Concept','Grounded in'],srows))
        body.append('</div>')
        pages.append('\n'.join(body))
        trace(f'page:{aid}',a,EXT,None)

    # TAXONOMIES page — comprehensive explainer + real explorer trees (data-driven)
    sim_js=[]  # kept empty; abstract simulations removed
    tax_html=[]
    for ti,(tlab,tdom,ttree) in enumerate(taxonomies()):
        tax_html.append(build_taxonomy(tlab,tdom,ttree,f'tx{ti}'))
        trace(f'taxonomy:{ti}',AXIS,RDF.type,SCP.Taxonomy)
    trace('taxonomy-explainer',SCP.TaxonomyExplainer,SCP.taxonomyPageData,None)
    pages.append(build_taxonomy_page(tax_html))

    # QUIZ page
    quiz_data=[]  # legacy inline quiz retired; comprehensive quiz page below
    pages.append(build_comparison_page())
    pages.append(build_examples_catalog()); trace('examples-catalog',SCP[_AREA_MARKER],SCP.ofConcept,None)
    pages.append(build_quiz_page()); trace('quizpage',SCP.quizBank,SCP.quizBank,None)

    # REFS page
    rrows=[]
    for p in pubs:
        u=url(p); link=f'<a href="{hattr(u)}" target="_blank" rel="noopener">{h(label(p))}</a>' if u else h(label(p))
        linkcell=f'<a href="{hattr(u)}" target="_blank" rel="noopener">link \u2197</a>' if u else '\u2014'
        rrows.append((link,h(defn(p)),linkcell))
        if u: trace(f'refurl:{loc(p)}',p,SCP.url,None)
    rtable='<table class="short"><thead><tr><th>Reference</th><th>Contribution</th><th>Link</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in rrows)+'</tbody></table>'
    pages.append(f'<div class="page" id="page-refs"><div class="secnum">Sources</div><h2>References</h2><p>The {len(pubs)} reference individuals from the Stage-1 research artefact:</p>{rtable}</div>')
    for p in pubs: trace(f'ref:{loc(p)}',p,RDF.type,SCP.Publication)

    CSS=""":root{--paper:#f5f3ec;--ink:#1a222d;--muted:#586272;--line:#d8d2c4;--card:#fffdf7;--accent:#2d4a52;--good:#3f7a4d;--warn:#a4502f}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:"Iowan Old Style","Palatino Linotype",Georgia,serif;line-height:1.62}
.wrap{max-width:1000px;margin:0 auto;padding:0 24px}
header{position:sticky;top:0;z-index:30;background:rgba(245,243,236,.97);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
nav{display:flex;gap:6px;flex-wrap:wrap;padding:9px 24px;max-width:1000px;margin:0 auto}
.tab{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;font-weight:600;padding:8px 15px;border:none;border-radius:8px;background:transparent;color:#5a6b73;cursor:pointer;white-space:nowrap;letter-spacing:.01em}
.tab:hover{color:var(--accent);background:#eef2f3}.tab.active{background:var(--accent);color:#fff}
.page{display:none;padding:24px 0 12px}.page.active{display:block}
h1{font-size:2.2rem;margin:.3em 0 .12em}h2{font-size:1.5rem;margin:0 0 .4em}h3{font-size:1.05rem;font-family:ui-sans-serif,system-ui,sans-serif;margin:1.1em 0 .3em}
.sub{color:var(--muted);font-size:1.05rem;font-style:italic;margin-bottom:1.2em}p{margin:.7em 0}
.secnum{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 17px;margin:13px 0}
.note{font-size:.84rem;color:var(--muted);font-style:italic}
table.short{width:auto;min-width:60%;border-collapse:collapse;font-size:.82rem;margin:10px 0;font-family:ui-sans-serif,system-ui,sans-serif}
table.short th,table.short td{border:1px solid var(--line);padding:5px 10px;text-align:left}table.short th{background:#ebe5d7}
.example{background:#eef2f4;border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:9px 13px;margin:8px 0;font-family:ui-monospace,monospace;font-size:.82rem}
.ex-lbl{display:inline-block;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;color:var(--accent);font-weight:bold;margin-right:6px}
.src{font-size:.8rem;color:var(--muted)}.badge{display:inline-block;font-size:.66rem;background:#e7f3ee;color:var(--good);border:1px solid #cfe9df;border-radius:4px;padding:1px 6px;margin-left:4px}
.term{border-bottom:1px dotted var(--accent);cursor:help}
.explorer{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.86rem;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;max-width:520px}
.folder{cursor:pointer;padding:5px 0;user-select:none}.folder:hover{color:var(--accent)}.tw{display:inline-block;width:14px;transition:transform .15s}.folder.open .tw{transform:rotate(90deg)}
.fname{font-weight:bold}.count{color:var(--muted);font-size:.76rem}
.children{display:none;padding-left:22px}.children.open{display:block}
.item{padding:3px 0;cursor:pointer;color:var(--ink)}.item:hover{color:var(--accent)}
.sim{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:14px 16px;margin:12px 0}
.sim-t{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;margin-bottom:4px}.sim-d{font-size:.86rem;color:var(--muted);margin-bottom:9px}
.sim-controls{display:flex;flex-wrap:wrap;gap:13px}.sim-ctrl{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.8rem;min-width:165px}.sim-ctrl label{display:block;color:var(--muted);margin-bottom:3px}.sim-ctrl input{width:165px}
.sim-out{background:#ebe5d7;border-radius:8px;padding:10px 13px;margin-top:9px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.9rem}
.quiz-q{border:1px solid var(--line);border-radius:8px;background:var(--card);padding:11px 13px;margin:8px 0}
.quiz-q .opt{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.85rem;padding:6px 10px;border:1px solid var(--line);border-radius:6px;margin:4px 0;cursor:pointer}
.quiz-q .opt:hover{background:#f0ebdd}.quiz-q .opt.right{background:#eef4ee;border-color:var(--good)}.quiz-q .opt.wrong{background:#f6efe9;border-color:var(--warn)}
#tooltip{position:fixed;z-index:100;background:#1a222d;color:#f5f3ec;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.78rem;padding:7px 11px;border-radius:6px;max-width:300px;display:none;pointer-events:none;box-shadow:0 4px 14px rgba(0,0,0,.2)}
#ctxmenu{position:fixed;z-index:101;background:var(--card);border:1px solid var(--line);border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,.15);display:none;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;min-width:180px;overflow:hidden}
#ctxmenu div{padding:8px 13px;cursor:pointer}#ctxmenu div:hover{background:#ebe5d7}
footer{padding:24px 0;color:var(--muted);font-size:.8rem;font-family:ui-sans-serif,system-ui,sans-serif}
/* ---- animated example demos ---- */
.anim-demo{margin:8px 0 12px;background:linear-gradient(180deg,#fffdf7,#f3efe4);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.anim-svg{width:100%;max-width:430px;font-family:ui-sans-serif,system-ui,sans-serif}
.anim-cap{font-size:.78rem;color:var(--muted);font-style:italic;margin-top:4px;display:flex;align-items:center;gap:10px}
.replay{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.72rem;font-style:normal;border:1px solid var(--line);background:var(--card);border-radius:5px;padding:2px 9px;cursor:pointer;color:var(--accent)}
.replay:hover{background:var(--accent);color:#fff}
.anim-stage .ab,.anim-stage .qm,.anim-stage .rp,.anim-stage .sm,.anim-stage .vc,.anim-stage .if{opacity:0}
.anim-stage.run .ab1{animation:fade .4s .1s forwards}.anim-stage.run .ab2{animation:fade .4s .6s forwards}.anim-stage.run .ab3{animation:fade .4s 1.1s forwards}
.anim-stage.run .qm1{animation:fade .4s .2s forwards}.anim-stage.run .qm2{animation:fade .4s .7s forwards}.anim-stage.run .qm3{animation:fade .4s 1.2s forwards}
.anim-stage.run .rp1{animation:fade .4s .1s forwards}.anim-stage.run .rp2{animation:fade .4s .5s forwards}.anim-stage.run .rp3{animation:fade .4s .9s forwards}.anim-stage.run .rp4{animation:fade .4s 1.3s forwards}
.anim-stage.run .sm1{animation:fade .35s .1s forwards}.anim-stage.run .sm2{animation:fade .35s .4s forwards}.anim-stage.run .sm3{animation:fade .35s .7s forwards}.anim-stage.run .sm4{animation:fade .4s 1.1s forwards}.anim-stage.run .sm5{animation:fade .5s 1.5s forwards}
.anim-stage.run .vc1{animation:fade .4s .1s forwards}.anim-stage.run .vc2{animation:fade .4s .7s forwards}.anim-stage.run .vc3{animation:fade .4s 1.2s forwards}
.anim-stage.run .if1{animation:fade .4s .1s forwards}.anim-stage.run .if2{animation:fade .4s .6s forwards}.anim-stage.run .if3{animation:fade .5s 1.2s forwards}
@keyframes fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}
/* ---- aesthetic polish ---- */
body{background:radial-gradient(1200px 500px at 50% -200px,#fbf9f2,var(--paper))}
header{box-shadow:0 1px 0 rgba(0,0,0,.02)}
h1{letter-spacing:-.01em;background:linear-gradient(90deg,var(--accent),#3a6470);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.card{box-shadow:0 1px 3px rgba(45,74,82,.05)}
.tab{transition:all .15s}.tab.active{box-shadow:0 2px 8px rgba(45,74,82,.22)}
.example{box-shadow:inset 3px 0 0 var(--accent),0 1px 2px rgba(0,0,0,.03)}
.sim{box-shadow:0 2px 10px rgba(45,74,82,.06)}
h2{position:relative;padding-bottom:4px}h2::after{content:"";position:absolute;left:0;bottom:0;width:48px;height:3px;background:var(--accent);border-radius:2px}
.term{transition:color .12s}.term:hover{color:var(--accent)}
.folder,.item{transition:color .12s,background .12s;border-radius:5px;padding-left:4px}.item:hover{background:#f0ebdd}
.model-wrap{background:#fbfaf5;border:1px solid var(--line);border-radius:10px;padding:10px;margin:10px 0;box-shadow:0 1px 3px rgba(45,74,82,.05)}
.model-svg{width:100%;max-width:560px;font-family:ui-sans-serif,system-ui,sans-serif}
.cicon{font-size:1.05em;margin-right:3px}
.short td a{color:var(--accent);text-decoration:none}.short td a:hover{text-decoration:underline}
.ex-block{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:12px 14px;margin:10px 0;box-shadow:0 1px 3px rgba(45,74,82,.05)}
.ex-head{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.ex-lbl{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;color:var(--accent);font-weight:bold}
.ex-compare{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.72rem;color:var(--muted);font-style:italic}
.ex-tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.ex-tab{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.74rem;padding:5px 12px;border:none;border-bottom:2px solid transparent;background:transparent;color:var(--muted);cursor:pointer;transition:all .12s}
.ex-tab:hover{color:var(--accent)}.ex-tab.active{color:var(--accent);border-bottom-color:var(--accent);font-weight:600;background:transparent}
.ex-pane{display:none}.ex-pane.active{display:block}
.ex-domain{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.7rem;font-weight:bold;color:var(--accent);margin-bottom:4px}
.ex-text{margin:.3em 0 0;font-size:.92rem}
.ex-pane svg{margin:4px 0}
.links-row{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.8rem;margin:8px 0 2px;color:var(--muted)}
.reslink{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}.reslink:hover{border-color:var(--accent)}
.rel-wrap{color:var(--muted)}.rellink{color:var(--accent);text-decoration:none;cursor:pointer;border-bottom:1px dotted var(--accent);margin-right:2px}.rellink:hover{background:#eef2f4}
.codeblock{margin:10px 0;border:1px solid #2a3642;border-radius:9px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08)}
.code-bar{display:flex;justify-content:space-between;align-items:center;background:#222d38;padding:5px 11px}
.code-lang{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.68rem;letter-spacing:.06em;text-transform:uppercase;color:#9db4c0}
.code-copy{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.68rem;background:#33414f;color:#cfe0e8;border:none;border-radius:4px;padding:2px 9px;cursor:pointer}
.code-copy:hover{background:#3f5160}.code-copy.done{background:#3f7a4d;color:#fff}
.codeblock pre{margin:0;background:#1b242d;padding:11px 13px;overflow-x:auto}
.codeblock code{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:.79rem;line-height:1.5;color:#dce6ec;white-space:pre}
.c-kw{color:#8fd0c4}.c-str{color:#e0b58a}.c-com{color:#6b7d88;font-style:italic}.c-key{color:#9db8e0}
.industry{margin:8px 0 2px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;background:#eef2f4;border-radius:8px;padding:7px 11px}
.ind-lbl{font-size:.64rem;text-transform:uppercase;letter-spacing:.06em;color:var(--accent);font-weight:bold;margin-right:6px}
.industry a{color:var(--accent);text-decoration:none;font-weight:bold}.industry a:hover{text-decoration:underline}
.ind-note{color:var(--muted)}
.syntax-notes{margin:6px 0 2px;border:1px solid var(--line);border-radius:8px;background:#f7f5ef;font-family:ui-sans-serif,system-ui,sans-serif}
.syntax-notes summary{cursor:pointer;padding:7px 12px;font-size:.78rem;color:var(--accent);font-weight:600;user-select:none}
.syntax-notes summary:hover{background:#f0ebdd;border-radius:8px}
.syn-body{padding:4px 12px 10px}
.syn-row{display:flex;gap:10px;padding:3px 0;border-top:1px solid #eee;align-items:baseline}
.syn-term{font-family:ui-monospace,monospace;font-size:.74rem;background:#1b242d;color:#8fd0c4;border-radius:4px;padding:1px 6px;white-space:nowrap;flex:0 0 auto;min-width:90px}
.syn-mean{font-size:.82rem;color:var(--ink)}
.techcompare{border:1px solid var(--line);border-radius:10px;background:linear-gradient(180deg,#fffdf7,#f3efe4);padding:12px 14px;margin:12px 0;box-shadow:0 1px 3px rgba(45,74,82,.05)}
.tc-head{margin-bottom:9px}.tc-lbl{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent);font-weight:bold}
.tc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}
.tc-card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:9px 11px}
.tc-tech{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.82rem;color:var(--accent);margin-bottom:4px}
.tc-how{font-size:.84rem;line-height:1.5}
.syn-hint{font-size:.74rem;color:var(--muted);font-style:italic;margin-bottom:6px}
.crosstech-tab{border:1px solid var(--line);border-radius:10px;background:linear-gradient(180deg,#fffdf7,#f1ede2);padding:12px 14px;margin:12px 0;box-shadow:0 1px 3px rgba(45,74,82,.06)}
.ct-head{margin-bottom:9px}.ct-lbl{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.7rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent);font-weight:bold}
.ct-hint{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.72rem;color:var(--muted);font-style:italic;margin-left:8px}
.ct-tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.ct-tab{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.74rem;padding:5px 12px;border:1px solid var(--line);border-radius:14px;background:var(--paper);color:var(--muted);cursor:pointer;transition:all .12s}
.ct-tab:hover{color:var(--ink)}.ct-tab.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.ct-pane{display:none}.ct-pane.active{display:block}
.ct-impact{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.84rem;line-height:1.5;background:#eef2f4;border-radius:8px;padding:8px 11px;margin-top:6px}
.ct-impact-lbl{font-size:.64rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent);font-weight:bold;margin-right:6px}
.infcontrast{border:1px solid var(--line);border-radius:12px;background:linear-gradient(180deg,#fffdf7,#f1ede2);padding:14px 16px;margin:14px 0;box-shadow:0 1px 3px rgba(45,74,82,.06)}
.ic-title{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:1rem;margin-bottom:5px}
.ic-lead{font-size:.88rem;line-height:1.55;margin:0 0 12px}
.ic-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:720px){.ic-grid{grid-template-columns:1fr}}
.ic-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:11px 12px}
.ic-op{display:flex;flex-direction:column;gap:2px;margin-bottom:8px}
.ic-op code{font-family:ui-monospace,monospace;font-size:.86rem;font-weight:bold}
.ic-role{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.74rem;font-weight:bold}
.ic-reads{font-size:.83rem;line-height:1.5;background:#eef2f4;border-radius:8px;padding:8px 10px;margin-top:8px}
.ic-reads-lbl{font-size:.64rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent);font-weight:bold;margin-right:5px}
.ic-summary{font-size:.88rem;line-height:1.55;font-style:italic;border-left:4px solid var(--good);background:var(--card);padding:9px 12px;border-radius:0 8px 8px 0;margin-top:12px}
.axref{margin:12px 0;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.axref summary{cursor:pointer;padding:10px 14px;font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.92rem;color:var(--accent);user-select:none}
.axref summary:hover{background:#f0ebdd;border-radius:10px}
.axref-note{font-size:.84rem;color:var(--muted);padding:0 14px;margin:4px 0 8px;font-style:italic}
.axref-group{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.82rem;color:var(--ink);background:#ebe5d7;padding:5px 14px;margin-top:4px}
.axref-table{width:100%;border-collapse:collapse;font-size:.82rem}
.axref-table th,.axref-table td{border:1px solid var(--line);padding:5px 10px;text-align:left;vertical-align:top}
.axref-table th{background:#f5f3ec;font-family:ui-sans-serif,system-ui,sans-serif}
.axref-term code{font-family:ui-monospace,monospace;font-size:.78rem;color:var(--accent);white-space:nowrap}
.axref-kind{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.74rem;font-weight:bold;white-space:nowrap}
.axref-d{color:#3f7a4d}.axref-c{color:#a4502f}
.axref-ex{font-size:.78rem;color:var(--muted);font-style:italic}
.primer{border:1px solid var(--accent);border-radius:12px;background:linear-gradient(180deg,#f3f7f8,#eef4f0);padding:16px 18px;margin:14px 0 22px;box-shadow:0 2px 10px rgba(45,74,82,.08)}
.primer-tag{display:inline-block;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.64rem;font-weight:bold;text-transform:uppercase;letter-spacing:.08em;color:#fff;background:var(--accent);border-radius:4px;padding:2px 9px;margin-bottom:8px}
.primer-h{margin-top:4px !important}
.triple-row{display:flex;align-items:stretch;gap:8px;margin:10px 0;flex-wrap:wrap}
.triple-part{flex:1;min-width:130px;border:1px solid var(--line);border-radius:9px;background:var(--card);padding:9px 11px}
.triple-role{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.82rem;color:var(--accent)}
.triple-desc{font-size:.8rem;color:var(--ink);margin:3px 0 5px;line-height:1.4}
.triple-ex{font-family:ui-monospace,monospace;font-size:.76rem;background:#1b242d;color:#dce6ec;border-radius:4px;padding:2px 7px;display:inline-block}
.triple-arrow{display:flex;align-items:center;color:var(--muted);font-size:1.2rem}
@media(max-width:600px){.triple-arrow{display:none}}
.prim-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0}
@media(max-width:720px){.prim-grid{grid-template-columns:1fr}}
.prim-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 13px}
.prim-head{display:flex;align-items:baseline;gap:8px;margin-bottom:6px;flex-wrap:wrap}
.prim-icon{font-size:1.1rem;font-weight:bold}
.prim-name{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:1rem}
.prim-analogy{font-size:.74rem;color:var(--muted);font-style:italic;margin-left:auto}
.prim-is{font-size:.85rem;line-height:1.5;margin:5px 0 7px}
.prim-repr{font-size:.8rem;line-height:1.45;background:#eef2f4;border-radius:7px;padding:6px 9px;margin-bottom:7px}
.prim-repr-lbl{font-size:.62rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent);font-weight:bold;margin-right:5px}
.rel-pred code,.rel-ex code{font-family:ui-monospace,monospace;font-size:.76rem;color:var(--accent);white-space:nowrap}
.rel-ex code{color:var(--ink)}
.provlegend{border:2px solid var(--accent);border-radius:12px;background:linear-gradient(180deg,#f3f7f8,#eef4f0);padding:15px 17px;margin:18px 0}
.pl-title{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:1rem;margin-bottom:5px}
.pl-text{font-size:.87rem;line-height:1.5;margin:0 0 10px}
.pl-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px}
.pl-card{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:9px 11px}
.pl-tag{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;margin-bottom:4px}
.pl-mark{font-size:.95rem}
.pl-desc{font-size:.82rem;line-height:1.45}
.pl-rule{font-size:.84rem;line-height:1.5;font-style:italic;background:var(--card);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:8px 11px;margin-top:10px}
.corpus{border:1px solid var(--line);border-radius:12px;background:var(--card);padding:15px 17px;margin:16px 0}
.cp-title{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:1rem;margin-bottom:5px}
.cp-sub{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.82rem;text-transform:uppercase;letter-spacing:.04em;margin:12px 0 5px;padding:4px 10px;border-radius:5px;display:inline-block}
.cp-sub-real{background:#eef5f0;color:#3f7a4d}.cp-sub-ill{background:#fbf3ee;color:#b5803a}
.cp-real{color:#3f7a4d;font-weight:bold;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.76rem;white-space:nowrap}
.cp-ill{color:#b5803a;font-style:italic;font-size:.82rem}
.corpus table td a{color:var(--accent);text-decoration:none}.corpus table td a:hover{text-decoration:underline}
.modelcmp{border:1px solid var(--accent);border-radius:12px;background:linear-gradient(180deg,#f6f4ef,#efeae0);padding:15px 17px;margin:16px 0}
.mc-title{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:1rem;margin-bottom:5px}
.mc-intro{font-size:.87rem;line-height:1.55;margin:0 0 12px}
.mc-grid{display:grid;grid-template-columns:1fr 1fr;gap:13px}
@media(max-width:760px){.mc-grid{grid-template-columns:1fr}}
.mc-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:11px 12px}
.mc-card-t{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.86rem;margin-bottom:7px}
.mc-diagram{background:#fcfbf8;border:1px solid var(--line);border-radius:8px;padding:6px;margin-bottom:8px}
.mc-svg{width:100%;height:auto;display:block}
.mc-note{font-size:.8rem;line-height:1.45;color:var(--ink);margin-top:7px}
.mc-table{margin-top:14px}
.mc-table .mc-aspect{font-weight:bold;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.8rem}
.mc-table td,.mc-table th{font-size:.8rem}
.mc-takeaway{font-size:.88rem;line-height:1.55;font-style:italic;border-left:4px solid var(--accent);background:var(--card);border-radius:0 8px 8px 0;padding:9px 12px;margin-top:12px}
.techrich{border:1px solid var(--line);border-radius:12px;background:linear-gradient(180deg,#f7f6f1,#efeee7);padding:14px 16px;margin:14px 0}
.tcr-head{margin-bottom:4px}
.tcr-lbl{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.95rem;color:var(--accent)}
.tcr-scenario{font-size:.86rem;line-height:1.5;margin:4px 0 12px;font-style:italic;color:var(--ink)}
.tcr-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:760px){.tcr-grid{grid-template-columns:1fr}}
.tcr-card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:11px 12px}
.tcr-recommended{box-shadow:0 0 0 2px #9a5b6e33;border-color:#9a5b6e}
.tcr-tech{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.9rem;margin-bottom:7px;display:flex;align-items:center;gap:7px}
.tcr-badge{font-size:.6rem;text-transform:uppercase;letter-spacing:.04em;background:#9a5b6e;color:#fff;border-radius:4px;padding:2px 6px;font-weight:bold}
.tcr-table{width:100%;border-collapse:collapse;font-size:.78rem;margin-bottom:8px}
.tcr-table th,.tcr-table td{border:1px solid var(--line);padding:3px 7px;text-align:left}
.tcr-table th{background:#f0ece2;font-family:ui-sans-serif,system-ui,sans-serif}
.tcr-note{font-size:.81rem;line-height:1.45;margin-top:8px;color:var(--ink)}
.tcr-summary-lbl{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.82rem;color:var(--accent);margin:14px 0 5px}
.tcr-summary{font-size:.8rem}
.tcr-summary .tcr-cap{font-weight:bold;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.78rem}
.tcr-yes{color:#3f7a4d;font-weight:bold}.tcr-no{color:#a4502f}.tcr-mid{color:#586272}
.cmp-legend{display:flex;align-items:center;gap:12px;margin:10px 0 16px;font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.9rem}
.cmp-trad{color:#a4502f}.cmp-sem{color:#3f7a4d}.cmp-vs{color:var(--muted);font-style:italic;font-weight:normal}
.cmp-table{width:100%;border-collapse:collapse;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.84rem;margin:10px 0 18px}
.cmp-table th,.cmp-table td{border:1px solid var(--line);padding:7px 11px;text-align:left;vertical-align:top}
.cmp-table th{background:#ebe5d7}.cmp-table th:nth-child(2){color:#a4502f}.cmp-table th:nth-child(3){color:#3f7a4d}
.cmp-dim{font-weight:600;background:#f5f3ec;white-space:nowrap}
.cmp-tcell{background:#fbf3ee}.cmp-scell{background:#eef5f0}
.cmp-sim{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.88rem;line-height:1.6;margin:8px 0 18px}
.cmp-sim li{margin:4px 0}
.cmp-worked{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0 18px}
@media(max-width:680px){.cmp-worked{grid-template-columns:1fr}}
.cmp-wcol{border:1px solid var(--line);border-radius:10px;padding:11px 13px}
.cmp-wtrad{background:#fbf3ee;border-color:#e3cdbf}.cmp-wsem{background:#eef5f0;border-color:#cfe3d6}
.cmp-wlbl{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.82rem;margin-bottom:7px}
.cmp-wtrad .cmp-wlbl{color:#a4502f}.cmp-wsem .cmp-wlbl{color:#3f7a4d}
.cmp-wnote{font-size:.83rem;line-height:1.5;color:var(--ink);margin:8px 0 0}
.cmp-syn{border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:0 9px 9px 0;background:var(--card);padding:11px 14px;margin:9px 0}
.cmp-syn-name{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.92rem;color:var(--accent);margin-bottom:5px}
.cmp-syn-how{font-size:.88rem;line-height:1.55;margin-bottom:6px}
.cmp-syn-impact{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;background:#eef2f4;border-radius:7px;padding:6px 10px}
.cmp-closing{font-size:.95rem;line-height:1.65;border-left:4px solid var(--good)}
.cmp-decision{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0 18px}
@media(max-width:680px){.cmp-decision{grid-template-columns:1fr}}
.cmp-dec-col{border:1px solid var(--line);border-radius:10px;padding:11px 14px}
.cmp-dec-col ul{margin:6px 0 0;padding-left:18px;font-size:.86rem;line-height:1.55}.cmp-dec-col li{margin:4px 0}
.cmp-verdict{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.78rem;text-align:center;white-space:nowrap}
.cmp-v-t{color:#a4502f}.cmp-v-s{color:#3f7a4d}
.cmp-rb-col{border:1px solid var(--line);border-radius:10px;padding:11px 14px}
.cmp-rb-col ul{margin:4px 0 8px;padding-left:18px;font-size:.84rem;line-height:1.5}.cmp-rb-col li{margin:3px 0}
.cmp-rb-sub{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.74rem;text-transform:uppercase;letter-spacing:.04em;color:#3f7a4d;margin-top:6px}
.cmp-rb-risk{color:#a4502f}
.cmp-bp{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.88rem;line-height:1.6;margin:8px 0 18px;padding-left:22px}.cmp-bp li{margin:5px 0}
.cmp-statval{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;color:var(--accent)}.cmp-statsrc{font-size:.78rem;color:var(--muted)}
.gt-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:10px 0 18px}
.gt-card{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:10px;text-align:center}
.gt-svg{display:block;margin:0 auto 6px}
.gt-name{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.8rem;margin-bottom:3px}
.gt-use{font-size:.76rem;color:var(--muted);line-height:1.4}
.cmp-table td a{color:var(--accent);text-decoration:none}.cmp-table td a:hover{text-decoration:underline}
.tx-blocks{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin:10px 0 18px}
.tx-block{border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:0 8px 8px 0;background:var(--card);padding:9px 12px}
.tx-block-name{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.84rem;color:var(--accent)}
.tx-block-desc{font-size:.82rem;line-height:1.45;margin-top:3px}
.tx-types{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:10px 0 18px}
.tx-type-card{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:11px;text-align:center}
.tx-type-card .gt-svg{margin:0 auto 7px}
.tx-type-name{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.84rem;margin-bottom:4px}
.tx-type-desc{font-size:.8rem;line-height:1.45;color:var(--ink);text-align:left}
.tx-type-ex{font-size:.76rem;color:var(--muted);margin-top:5px;font-style:italic;text-align:left}
.tx-spectrum{margin:10px 0 6px}
.tx-spec-row{display:grid;grid-template-columns:140px 120px 1fr;gap:12px;align-items:center;padding:5px 0;border-top:1px solid var(--line)}
@media(max-width:640px){.tx-spec-row{grid-template-columns:1fr;gap:3px}}
.tx-spec-name{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.84rem}
.tx-spec-bar{background:#e7e1d3;border-radius:5px;height:11px;overflow:hidden}
.tx-spec-bar span{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--good))}
.tx-spec-desc{font-size:.82rem;color:var(--muted)}
.tx-ex-cell{font-size:.82rem;color:var(--muted);font-style:italic}
/* ex grid: diagram + narrative side by side (narrative shown through the diagram) */
.ex-grid{display:grid;grid-template-columns:minmax(200px,1fr) 1fr;gap:14px;align-items:center}
@media(max-width:640px){.ex-grid{grid-template-columns:1fr}}
.ex-diagram{min-width:0}.ex-domain-tag{font-size:.6rem;background:#e7eef1;color:var(--accent);border-radius:3px;padding:1px 5px;text-transform:uppercase;letter-spacing:.05em}
.case-graph{background:#fbfaf5;border:1px solid var(--line);border-radius:8px;padding:6px}
/* code execution */
.exec{border:1px solid var(--line);border-top:none;border-radius:0 0 9px 9px;background:var(--card);padding:0 0 10px;margin:-10px 0 12px}
.exec-bar{display:flex;justify-content:space-between;align-items:center;background:#eef2f4;padding:6px 12px;border-bottom:1px solid var(--line)}
.exec-lbl{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent);font-weight:bold}
.exec-run{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.72rem;background:var(--accent);color:#fff;border:none;border-radius:5px;padding:3px 11px;cursor:pointer}.exec-run:hover{opacity:.9}
.exec-steps{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;margin:8px 14px;padding-left:20px;color:var(--muted)}
.exec-steps li{margin:3px 0;opacity:.45;transition:opacity .2s,color .2s}.exec-steps li.on{opacity:1;color:var(--ink);font-weight:600}
.exec-result{margin:6px 14px 0}.layered{border:1px solid var(--line);border-radius:12px;background:linear-gradient(180deg,#f6f8f7,#eef2f0);padding:14px 16px;margin:14px 0}
.la-head{margin-bottom:4px}.la-lbl{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.98rem;color:var(--accent)}
.la-intro{font-size:.86rem;line-height:1.5;margin:4px 0 10px;color:var(--ink)}
.la-svg{width:100%;max-width:560px;display:block;margin:0 auto 8px}
.la-maplbl{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.82rem;color:var(--accent);margin:12px 0 5px}
.la-map{font-size:.8rem}.la-map td:first-child,.la-map td:nth-child(2){font-family:ui-monospace,Menlo,monospace;font-size:.76rem}
.la-take{font-size:.85rem;line-height:1.5;font-style:italic;border-left:4px solid var(--accent);background:var(--card);border-radius:0 8px 8px 0;padding:9px 12px;margin-top:12px}
.idgloss{border:1px solid var(--line);border-radius:9px;background:#f3f6f8;padding:10px 12px;margin:8px 0}
.idg-head{margin-bottom:4px}.idg-lbl{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.82rem;color:var(--accent)}
.idg-note{font-size:.78rem;color:#586272;margin:2px 0 8px;line-height:1.4}
.idg-table{width:100%;border-collapse:collapse;font-size:.8rem}
.idg-table th,.idg-table td{border:1px solid var(--line);padding:3px 8px;text-align:left;vertical-align:top}
.idg-table th{background:#e7edf0;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.74rem}
.idg-code{font-family:ui-monospace,Menlo,monospace;color:#2d4a52;white-space:nowrap;font-weight:bold}
.idg-label{font-weight:bold}.idg-desc{color:#586272}
.idg-src{font-size:.72rem;color:var(--accent);text-decoration:none;white-space:nowrap}.idg-src:hover{text-decoration:underline}
.idg-reads{font-size:.82rem;margin-top:8px;padding:6px 9px;background:#fff;border-left:3px solid var(--accent);border-radius:0 6px 6px 0;line-height:1.5}
.idg-reads-lbl{font-weight:bold;color:var(--accent);font-family:ui-sans-serif,system-ui,sans-serif}
.idg-live{font-size:.78rem;margin-top:6px;color:#3f7a4d;font-style:italic}
.exec-computed{font-size:.66rem;font-weight:bold;color:#3f7a4d;background:#eaf3ec;border:1px solid #bcd9c4;border-radius:4px;padding:1px 6px;margin-left:6px;cursor:help;font-family:ui-sans-serif,system-ui,sans-serif}
.exec-rlbl{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.68rem;text-transform:uppercase;color:var(--muted);margin-bottom:3px}
.result-tbl{border-collapse:collapse;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.8rem;width:auto;min-width:50%}
.result-tbl th,.result-tbl td{border:1px solid var(--line);padding:4px 9px;text-align:left}.result-tbl th{background:#ebe5d7}
.result-tbl tbody tr{opacity:.3;transition:opacity .25s}.result-tbl tbody tr.shown{opacity:1}

/* ---- sticky readable top menu ---- */
header{position:sticky;top:0;z-index:40;background:rgba(247,246,241,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header nav{display:flex;gap:3px;flex-wrap:wrap;padding:9px 16px;max-width:1280px;margin:0 auto;align-items:center}
@media(max-width:900px){header nav{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch}}
/* ---- two-column layout: persistent sidebar + main ---- */
.layout{display:flex;gap:0;max-width:1280px;margin:0 auto;align-items:flex-start}
.sidebar{position:sticky;top:50px;align-self:flex-start;width:268px;min-width:268px;max-height:calc(100vh - 56px);overflow-y:auto;
  border-right:1px solid var(--line);background:#fbfaf6;padding:0 0 30px}
.sb-titlebar{position:sticky;top:0;background:#f0ede6;border-bottom:1px solid var(--line);padding:7px 11px;display:flex;align-items:center;gap:8px;z-index:2}
.sb-title{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:#54616a;font-weight:bold}
.sb-tools{margin-left:auto;display:flex;gap:4px}
.sb-btn{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.64rem;background:var(--card);border:1px solid var(--line);border-radius:4px;padding:2px 7px;cursor:pointer;color:var(--muted)}
.sb-btn:hover{background:#e3e9e6;color:var(--accent)}
.sb-group{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.64rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);font-weight:bold;padding:10px 11px 3px}
.sb-tree{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.82rem;padding:0 4px}
/* MS-Explorer rows: folder/file with indent guides */
.msx-root{padding-left:2px}
.msx-row{display:flex;align-items:center;gap:5px;padding:3px 6px;border-radius:4px;cursor:pointer;user-select:none;white-space:nowrap;position:relative}
.msx-row:hover{background:#e8efe7}
.msx-tw{display:inline-block;width:11px;font-size:.62rem;color:#8a99a0;transition:transform .12s;flex-shrink:0}
.msx-folder.open .msx-tw{transform:rotate(90deg)}
.msx-ico{font-size:.82rem;flex-shrink:0;width:16px;text-align:center}
.msx-name{overflow:hidden;text-overflow:ellipsis}
.msx-folder .msx-name{font-weight:600;color:#34424a}
.msx-count{margin-left:auto;font-size:.62rem;color:var(--muted);background:#e4e9e5;border-radius:8px;padding:0 6px}
.msx-children{display:none;margin-left:13px;border-left:1px solid #dde3e0;padding-left:3px}
.msx-children.open{display:block}
.msx-file{color:#54616a}.msx-file .msx-name{font-size:.8rem}
.msx-file.sel,.msx-page.sel{background:#d7e3e6;color:var(--accent);font-weight:600}
.msx-page{color:#34424a;font-weight:500}
.wrap{flex:1;min-width:0;padding:0 28px;max-width:920px}
@media(max-width:820px){.sidebar{display:none}.wrap{padding:0 16px}}
/* ---- examples catalog ---- */
.ec-concept{font-family:ui-sans-serif,system-ui,sans-serif;font-size:1rem;color:var(--accent);border-bottom:2px solid var(--line);padding-bottom:4px;margin:20px 0 8px}
.ec-table{width:100%;border-collapse:collapse;font-size:.82rem;margin-bottom:8px}
.ec-table th,.ec-table td{border:1px solid var(--line);padding:5px 9px;text-align:left;vertical-align:top}
.ec-table th{background:#ebe5d7;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.74rem}
.ec-dom{font-weight:bold;white-space:nowrap;color:#2d4a52}.ec-lang{font-family:ui-monospace,monospace;font-size:.74rem;color:var(--muted)}
.ec-what{color:var(--ink)}.ec-use{color:#586272;font-size:.79rem}
.ec-link{color:var(--accent);font-size:.76rem;cursor:pointer;white-space:nowrap;font-weight:600}.ec-link:hover{text-decoration:underline}

.qp-sec{font-family:ui-sans-serif,system-ui,sans-serif;font-size:1rem;color:var(--accent);border-bottom:2px solid var(--line);padding-bottom:4px;margin:20px 0 10px}
.qp-scorebar{position:sticky;top:0;z-index:5;background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:8px 12px;font-family:ui-sans-serif,system-ui,sans-serif;font-size:.88rem;font-weight:bold;color:var(--accent);margin:10px 0 14px;display:flex;align-items:center;gap:8px}
#qp-score{font-size:1.1rem}
.qp-reset{margin-left:auto;font-size:.72rem;font-weight:normal;background:var(--card);border:1px solid var(--line);border-radius:5px;padding:3px 10px;cursor:pointer}.qp-reset:hover{background:#f0ebdd}
.qp-q{border:1px solid var(--line);border-radius:9px;background:var(--card);padding:12px 14px;margin:10px 0}
.qp-qhead{display:flex;align-items:baseline;gap:8px;margin-bottom:7px}
.qp-type{font-size:.62rem;text-transform:uppercase;letter-spacing:.04em;color:#fff;border-radius:4px;padding:2px 7px;font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;white-space:nowrap}
.qp-qtext{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.92rem;font-weight:bold;line-height:1.4}
.qp-code{background:#1b242d;color:#dce6ec;border-radius:6px;padding:9px 11px;font-family:ui-monospace,Menlo,monospace;font-size:.78rem;overflow-x:auto;margin:6px 0 9px;line-height:1.45}
.qp-opt{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.86rem;padding:7px 11px;border:1px solid var(--line);border-radius:6px;margin:5px 0;cursor:pointer;transition:background .15s}
.qp-opt:hover{background:#f0ebdd}.qp-opt.right{background:#eef4ee;border-color:var(--good);font-weight:bold}.qp-opt.wrong{background:#f6efe9;border-color:var(--warn)}
.qp-opt.locked{cursor:default;opacity:.7}.qp-opt.right.locked{opacity:1}
.qp-explain{display:none;font-size:.84rem;line-height:1.5;margin-top:9px;padding:8px 11px;background:#eef2f4;border-left:3px solid var(--accent);border-radius:0 6px 6px 0}
.qp-explain.show{display:block}
.qp-final{font-family:ui-sans-serif,system-ui,sans-serif;font-size:1rem;font-weight:bold;text-align:center;margin:18px 0;padding:14px;border-radius:9px;background:var(--paper);border:1px solid var(--line);display:none}
.qp-final.show{display:block}
/* TBox/ABox/RBox/SHACL explainer */
.explainer{border:1px solid var(--line);border-radius:10px;background:var(--card);padding:14px 16px;margin:12px 0;box-shadow:0 1px 3px rgba(45,74,82,.05)}
.ex4-title{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.95rem;margin-bottom:10px}
.ex4-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.ex4-card{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:9px 11px}
.ex4-name{font-family:ui-sans-serif,system-ui,sans-serif;font-weight:bold;font-size:.9rem}.ex4-full{font-size:.72rem;color:var(--muted);margin-bottom:5px}
.ex4-q{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.78rem;font-style:italic;color:var(--accent);margin-bottom:4px}
.ex4-gov{font-size:.8rem;margin-bottom:6px}.ex4-ex{display:block;font-family:ui-monospace,monospace;font-size:.72rem;background:#1b242d;color:#dce6ec;border-radius:5px;padding:5px 7px}
.ex4-note{font-size:.84rem;color:var(--muted);margin-top:10px;font-style:italic}
/* real taxonomy explorer */
.taxonomy-explorer{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.86rem;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:12px 0;max-width:560px}
.tx-head{margin-bottom:8px}.tx-domain{font-size:.62rem;background:var(--accent);color:#fff;border-radius:3px;padding:2px 7px;text-transform:uppercase;letter-spacing:.05em}
.tx-label{font-weight:bold;margin-left:6px}
.tx-folder{cursor:pointer;padding:4px 4px;user-select:none;border-radius:5px}.tx-folder:hover{background:#f0ebdd}
.tx-folder:focus{outline:2px solid var(--accent);outline-offset:1px}
.tx-folder[aria-selected="true"]{background:#e4dcc4;font-weight:600}
.tx-tw{display:inline-block;width:14px;transition:transform .15s}.tx-folder.open .tx-tw{transform:rotate(90deg)}
.tx-name{font-weight:600}.tx-children{display:none;padding-left:20px}.tx-children.open{display:block}
.tx-leaf{padding:3px 4px;color:var(--muted)}"""

    JS=f'''const QD={json.dumps(quiz_data)};
// SPA tab navigation
function show(p,pushHist){{document.querySelectorAll('.page').forEach(x=>x.classList.remove('active'));document.getElementById('page-'+p)?.classList.add('active');
document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.p===p));
// sync sidebar active state
document.querySelectorAll('.sb-page').forEach(s=>s.classList.toggle('active',s.dataset.goto===p));
if(pushHist!==false&&location.hash.slice(1)!==p)history.pushState({{p}},'','#'+p);
window.scrollTo(0,0);}}
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>show(t.dataset.p));
// CR-13.4: back/forward button support -- popstate restores the page from history state
window.addEventListener('popstate',e=>{{show((e.state&&e.state.p)||location.hash.slice(1)||'overview',false);}});
// CR-13.4: initial load honors a deep-linked hash (e.g. reload, shared URL, bookmark)
if(location.hash.slice(1))show(location.hash.slice(1),false);
// ---- persistent sidebar (MS-Explorer) ----
function gotoTarget(goto,anchor){{
  show(goto);
  if(anchor){{setTimeout(()=>{{const t=document.getElementById(anchor);
    if(t){{t.scrollIntoView({{behavior:'smooth',block:'start'}});t.style.transition='background .2s';t.style.background='#fff3d6';setTimeout(()=>t.style.background='',1300);}}}},130);}}
  document.querySelectorAll('.msx-file,.msx-page').forEach(s=>s.classList.toggle('sel', s.dataset.goto===goto && (s.dataset.anchor||null)===(anchor||null)));
}}
function toggleFolder(f){{f.classList.toggle('open');document.getElementById('sbch-'+f.dataset.sf)?.classList.toggle('open');}}
document.querySelectorAll('.msx-folder').forEach(f=>{{
  f.onclick=e=>{{ if(e.target.closest('.msx-name')||e.target.closest('.msx-tw')){{ if(e.target.closest('.msx-name')&&!e.target.closest('.msx-tw')){{toggleFolder(f);}} else {{toggleFolder(f);}} }} else {{toggleFolder(f);}} }};
}});
document.querySelectorAll('.msx-file').forEach(it=>it.onclick=()=>gotoTarget(it.dataset.goto,it.dataset.anchor));
document.querySelectorAll('.msx-page').forEach(pg=>pg.onclick=()=>gotoTarget(pg.dataset.goto,null));
document.getElementById('sb-openall').onclick=()=>{{document.querySelectorAll('.msx-folder').forEach(f=>f.classList.add('open'));document.querySelectorAll('.msx-children').forEach(c=>c.classList.add('open'));}};
document.getElementById('sb-closeall').onclick=()=>{{document.querySelectorAll('.msx-folder').forEach(f=>f.classList.remove('open'));document.querySelectorAll('.msx-children').forEach(c=>c.classList.remove('open'));}};
document.querySelectorAll('.ec-link').forEach(l=>l.onclick=()=>gotoTarget(l.dataset.goto,l.dataset.anchor));
// open the first folder by default
document.querySelector('.msx-folder')?.classList.add('open');
document.querySelector('.msx-children')?.classList.add('open');
// MS-Explorer tree (overview page)
document.querySelectorAll('.folder').forEach(f=>f.onclick=()=>{{f.classList.toggle('open');document.getElementById('ch-'+f.dataset.f)?.classList.toggle('open');}});
document.querySelectorAll('.item').forEach(it=>it.onclick=()=>show(it.dataset.goto));
// simulations
{''.join(sim_js)}
// quiz
const qd=document.getElementById('quiz');
// ---- comprehensive quiz page interaction ----
(function(){{
  const qs=[...document.querySelectorAll('.qp-q')];
  const total=qs.length; const answered={{}}; let correct=0;
  function refresh(){{
    const sc=document.getElementById('qp-score'); if(sc)sc.textContent=correct;
    const fin=document.getElementById('qp-final');
    if(fin && Object.keys(answered).length===total){{
      const pct=Math.round(correct/total*100);
      let msg = pct>=80?'Excellent — strong grasp of the material.':pct>=50?'Good — revisit the sections you missed.':'Worth re-reading the concept treatments above.';
      fin.textContent='You answered '+correct+' of '+total+' correctly ('+pct+'%). '+msg; fin.classList.add('show');
    }}
  }}
  document.querySelectorAll('.qp-opt').forEach(o=>o.onclick=()=>{{
    const q=o.closest('.qp-q'); const qi=q.id; const c=+q.dataset.correct; const oi=+o.dataset.o;
    if(answered[qi]!==undefined) return;              // lock after first answer
    answered[qi]=oi;
    q.querySelectorAll('.qp-opt').forEach((x,xi)=>{{x.classList.add('locked'); if(xi===c)x.classList.add('right');}});
    if(oi!==c) o.classList.add('wrong');
    if(oi===c) correct++;
    const ex=q.querySelector('.qp-explain'); if(ex)ex.classList.add('show');
    refresh();
  }});
  const rb=document.getElementById('qp-reset');
  if(rb)rb.onclick=()=>{{
    for(const k in answered)delete answered[k]; correct=0;
    document.querySelectorAll('.qp-opt').forEach(x=>x.classList.remove('right','wrong','locked'));
    document.querySelectorAll('.qp-explain').forEach(x=>x.classList.remove('show'));
    const fin=document.getElementById('qp-final'); if(fin)fin.classList.remove('show');
    refresh();
  }};
}})();
// hover tooltip
const tip=document.createElement('div');tip.id='tooltip';document.body.appendChild(tip);
document.addEventListener('mouseover',e=>{{const t=e.target.closest('[data-tip]');if(t&&t.dataset.tip){{tip.textContent=t.dataset.tip;tip.style.display='block';}}}});
document.addEventListener('mousemove',e=>{{if(tip.style.display==='block'){{tip.style.left=Math.min(e.clientX+14,innerWidth-310)+'px';tip.style.top=(e.clientY+16)+'px';}}}});
document.addEventListener('mouseout',e=>{{if(e.target.closest('[data-tip]'))tip.style.display='none';}});
// CR-13.1: focus-triggered tooltip (keyboard/screen-reader parity with hover)
document.addEventListener('focusin',e=>{{const t=e.target.closest('[data-tip]');if(t&&t.dataset.tip){{tip.textContent=t.dataset.tip;const r=t.getBoundingClientRect();tip.style.left=Math.min(r.left,innerWidth-310)+'px';tip.style.top=(r.bottom+6)+'px';tip.style.display='block';}}}});
document.addEventListener('focusout',e=>{{if(e.target.closest('[data-tip]'))tip.style.display='none';}});
// right-click context menu on concept headings
const menu=document.createElement('div');menu.id='ctxmenu';document.body.appendChild(menu);
let ctxTriggerEl=null;
function openCtxMenuFor(target,x,y){{
  const sbc=target.closest('.msx-file[data-ctx="concept"]');
  if(sbc){{
    menu.innerHTML='<div data-a="open">📂 Open concept</div><div data-a="def">📖 Definition</div><div data-a="src">🔗 Source: '+(sbc.dataset.src||'—')+'</div><div data-a="copy">📋 Copy name</div>';
    menu.dataset.label=sbc.dataset.label||''; menu.dataset.def=sbc.dataset.tip||''; menu.dataset.goto=sbc.dataset.goto||''; menu.dataset.anchor=sbc.dataset.anchor||'';
    menu.style.left=Math.min(x,innerWidth-200)+'px';menu.style.top=y+'px';menu.style.display='block';
    ctxTriggerEl=sbc; return true;}}
  const c=target.closest('.concept-h');if(!c)return false;
  menu.innerHTML='<div data-a="def">📖 Definition</div><div data-a="src">🔗 Source: '+(c.dataset.src||'—')+'</div><div data-a="copy">📋 Copy concept name</div>';
  menu.dataset.label=c.dataset.label||''; menu.dataset.def=c.dataset.def||''; menu.dataset.goto=''; menu.dataset.anchor='';
  menu.style.left=Math.min(x,innerWidth-190)+'px';menu.style.top=y+'px';menu.style.display='block';
  ctxTriggerEl=c; return true;
}}
function closeCtxMenu(returnFocus){{
  menu.style.display='none';
  if(returnFocus&&ctxTriggerEl&&ctxTriggerEl.focus)ctxTriggerEl.focus();
  ctxTriggerEl=null;
}}
document.addEventListener('contextmenu',e=>{{
  if(openCtxMenuFor(e.target,e.clientX,e.clientY))e.preventDefault();
}});
// CR-13.2: keyboard trigger -- Shift+F10 or the dedicated ContextMenu key, positioned at the
// focused element's own location since keyboard events carry no clientX/clientY.
document.addEventListener('keydown',e=>{{
  if(e.key==='ContextMenu'||(e.key==='F10'&&e.shiftKey)){{
    const r=document.activeElement&&document.activeElement.getBoundingClientRect?document.activeElement.getBoundingClientRect():null;
    if(r&&openCtxMenuFor(document.activeElement,r.left,r.bottom)){{e.preventDefault();}}
  }}
  // CR-13.2: Escape dismisses and returns focus to the triggering element
  else if(e.key==='Escape'&&menu.style.display==='block'){{closeCtxMenu(true);}}
}});
// unified context-menu action handler (works for both sidebar files and concept headings)
document.addEventListener('click',ev=>{{
  const it=ev.target.closest('#ctxmenu div'); if(!it){{closeCtxMenu(false);return;}}
  const a=it.dataset.a;
  if(a==='open'&&menu.dataset.goto){{gotoTarget(menu.dataset.goto,menu.dataset.anchor||null);}}
  else if(a==='def'){{tip.textContent=menu.dataset.def||'—';tip.style.left=Math.min(ev.clientX,innerWidth-310)+'px';tip.style.top=(ev.clientY+10)+'px';tip.style.display='block';setTimeout(()=>tip.style.display='none',3500);}}
  else if(a==='copy'){{navigator.clipboard&&navigator.clipboard.writeText(menu.dataset.label||'');}}
  closeCtxMenu(false);
}});


// code execution step-by-step animation
document.querySelectorAll('.exec-run').forEach(btn=>btn.onclick=()=>{{
  const k=btn.dataset.exec;
  const steps=[...document.querySelectorAll('#exec-steps-'+k+' li')];
  const rows=[...document.querySelectorAll('#exec-rows-'+k+' tr')];
  steps.forEach(s=>s.classList.remove('on')); rows.forEach(r=>r.classList.remove('shown'));
  let i=0;
  const tick=()=>{{
    if(i>0&&steps[i-1])steps[i-1].classList.remove('on');
    if(i<steps.length){{steps[i].classList.add('on');
      const rr=rows[Math.min(i,rows.length-1)]; if(rr&&i>=steps.length-rows.length-1)rr.classList.add('shown');
      i++; setTimeout(tick,650);
    }} else {{ rows.forEach(r=>r.classList.add('shown')); steps.forEach(s=>s.classList.remove('on')); }}
  }};
  tick();
}});
// real taxonomy explorer toggle
// CR-13.3: tree keyboard navigation -- visible-items list respects open/closed ancestor state
function txVisibleItems(){{
  return [...document.querySelectorAll('.tx-folder')].filter(f=>{{
    let anc=f.parentElement&&f.parentElement.closest('.tx-children');
    while(anc){{ if(!anc.classList.contains('open'))return false; anc=anc.parentElement&&anc.parentElement.closest('.tx-children'); }}
    return true;
  }});
}}
function txSetSelected(el){{
  document.querySelectorAll('.tx-folder[aria-selected="true"]').forEach(x=>x.setAttribute('aria-selected','false'));
  el.setAttribute('aria-selected','true'); el.focus();
}}
document.querySelectorAll('.tx-folder').forEach(f=>{{
  f.onclick=(e)=>{{e.stopPropagation();f.classList.toggle('open');const c=document.getElementById('txc-'+f.dataset.tx);if(c)c.classList.toggle('open');txSetSelected(f);}};
  f.addEventListener('keydown',e=>{{
    const items=txVisibleItems(); const i=items.indexOf(f);
    if(e.key==='ArrowDown'){{e.preventDefault();const n=items[i+1];if(n)txSetSelected(n);}}
    else if(e.key==='ArrowUp'){{e.preventDefault();const p=items[i-1];if(p)txSetSelected(p);}}
    else if(e.key==='ArrowRight'){{e.preventDefault();
      const c=document.getElementById('txc-'+f.dataset.tx);
      if(c&&!f.classList.contains('open')){{f.classList.add('open');c.classList.add('open');}}
      else{{const items2=txVisibleItems();const ni=items2.indexOf(f);const n=items2[ni+1];if(n)txSetSelected(n);}}
    }}
    else if(e.key==='ArrowLeft'){{e.preventDefault();
      const c=document.getElementById('txc-'+f.dataset.tx);
      if(c&&f.classList.contains('open')){{f.classList.remove('open');c.classList.remove('open');}}
      else{{const pc=f.parentElement&&f.parentElement.closest('.tx-children');const pf=pc&&pc.previousElementSibling;if(pf&&pf.classList.contains('tx-folder'))txSetSelected(pf);}}
    }}
    else if(e.key==='Home'){{e.preventDefault();const all=txVisibleItems();if(all[0])txSetSelected(all[0]);}}
    else if(e.key==='End'){{e.preventDefault();const all=txVisibleItems();if(all.length)txSetSelected(all[all.length-1]);}}
  }});
}});

document.querySelectorAll('.ct-tab').forEach(t=>t.onclick=()=>{{const k=t.dataset.ct,i=t.dataset.i;
document.querySelectorAll('.ct-tab[data-ct="'+k+'"]').forEach(x=>x.classList.toggle('active',x.dataset.i===i));
document.querySelectorAll('[id^="ct-'+k+'-"]').forEach(p=>p.classList.toggle('active',p.id==='ct-'+k+'-'+i));}});
document.querySelectorAll('.code-copy').forEach(b=>b.onclick=()=>{{navigator.clipboard&&navigator.clipboard.writeText(b.dataset.code);b.textContent='copied';b.classList.add('done');setTimeout(()=>{{b.textContent='copy';b.classList.remove('done');}},1200);}});
// multi-domain example tabs
document.querySelectorAll('.ex-tab').forEach(t=>t.onclick=()=>{{const k=t.dataset.ex,i=t.dataset.i;
document.querySelectorAll('.ex-tab[data-ex="'+k+'"]').forEach(x=>x.classList.toggle('active',x.dataset.i===i));
document.querySelectorAll('[id^="ex-'+k+'-"]').forEach(p=>p.classList.toggle('active',p.id==='ex-'+k+'-'+i));}});
// related-concept internal navigation
const conceptPage={{}};
document.querySelectorAll('.concept-h').forEach(h=>{{const pg=h.closest('.page');if(pg)conceptPage[h.dataset.label]=pg.id.replace('page-','');}});
document.querySelectorAll('.rellink').forEach(a=>a.onclick=()=>{{const lab=a.textContent.trim();
for(const [k,v] of Object.entries(conceptPage)){{if(k.toLowerCase()===lab.toLowerCase()){{show(v);setTimeout(()=>{{const t=[...document.querySelectorAll('#page-'+v+' .concept-h')].find(x=>x.dataset.label.toLowerCase()===lab.toLowerCase());if(t){{t.scrollIntoView({{behavior:'smooth',block:'center'}});t.style.transition='background .2s';t.style.background='#fff3d6';setTimeout(()=>t.style.background='',1200);}}}},120);break;}}}}}});
// animated example demos
function runAnim(stage){{stage.classList.remove('run');void stage.offsetWidth;stage.classList.add('run');}}
const io=new IntersectionObserver((es)=>es.forEach(e=>{{if(e.isIntersecting){{runAnim(e.target);io.unobserve(e.target);}}}}),{{threshold:.4}});
document.querySelectorAll('.anim-stage').forEach(s=>io.observe(s));
document.querySelectorAll('.replay').forEach(b=>b.onclick=()=>{{const d=document.getElementById(b.dataset.target);if(d)runAnim(d.querySelector('.anim-stage'));}});
const _show=show;show=function(p){{_show(p);setTimeout(()=>{{document.getElementById('page-'+p)?.querySelectorAll('.anim-stage').forEach(runAnim);}},60);}};'''

    HTML=f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{h(_PAGE_TITLE)} — {h(_PAGE_SUBTITLE)}</title><style>{CSS}</style></head><body>
<header><nav>{nav}</nav></header>
<div class="layout">{build_sidebar()}<main class="wrap">{''.join(pages)}
<footer>Generated by gen_render_deployed v30 from scp_domain v3.15.0 · SPA subpages · explorer tree · examples · tooltips · context menus.</footer>
</main></div><script>{JS}</script></body></html>'''
    open(OUT+"/"+_OUTNAME,"w").write(HTML); print("WROTE:",OUT+"/"+_OUTNAME)
    return len(pages)

def report():
    L=[f"# Semantic Technologies — Domain Report (v3.3.0, pipeline-generated)\n",
       f"*Generated by gen_render_deployed v30 from scp_domain v3.15.0 on {TODAY}. Includes the full textual treatment (the HTML keeps it lighter via subpages; the report retains everything).*\n"]
    for a in areas:
        L.append(f"\n## {label(a)}\n"); L.append(ext(a) or defn(a))
        for c in concepts_of(a):
            L.append(f"\n### {label(c)}\n"); L.append(ext(c) or defn(c))
            ex=example(c)
            if ex: L.append(f"\n*Example:* {ex}")
            s=source(c)
            if s: L.append(f"\n<sub>Grounded in {s}</sub>")
    L.append("\n## References\n")
    for p in pubs: L.append(f"- **{label(p)}** — {defn(p)}")
    open(OUT+"/scp_deployed_report_v3_15_0.md","w").write("\n".join(L))
    return len([x for x in L if x.startswith("## ")])

nsec=report(); npg=page()
json.dump(fidelity,open(OUT+"/fidelity_trace_v3_12_0.json","w"),indent=1)
print(f"REPORT: {nsec} top-sections -> scp_deployed_report_v3_15_0.md")
print(f"PAGE: {npg} SPA subpages -> scp_deployed_page_v3_15_0.html")
print(f"FIDELITY: {len(fidelity)} elements traced; features: explorer-tree, examples, concept-SVGs, tooltips, context-menu, SPA tabs")
