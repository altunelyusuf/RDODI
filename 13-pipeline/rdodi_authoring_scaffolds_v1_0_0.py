#!/usr/bin/env python3
"""RDODI Authoring Scaffolds v1.0.0
Drafts the MISSING depth content the richness rubric flags, as reviewable TTL fragments + guidance.
Human-in-the-loop: emits DRAFT fragments (marked needs-review) the author edits and merges; nothing is
auto-committed. Domain-agnostic (namespace auto-detected).

Scaffolds (deterministic, structural):
  - missing-example   : an ExampleCase skeleton for each concept lacking one, with a tailored prompt
  - thin-treatment    : a treatment template with section prompts for thin/absent treatments
  - missing-feature   : correct JSON skeletons for rich features (modelComparison/techCompareRich/...)
  - formal-axioms     : suggested object properties + candidate concept relationships from co-occurrence

A CONTENT hook (--llm) is documented to fill drafts via the Anthropic API (requires a key at run time);
without it, scaffolds emit structurally-correct placeholders + guidance (always reliable).

Usage:
  python3 rdodi_authoring_scaffolds_v1_0_0.py <domain.ttl> [--only example,treatment,feature,axioms] [--out draft.ttl]
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

def run(path, only=None):
    g=rdflib.Graph(); g.parse(path)
    NS,MARK=detect(g); P=lambda n: NS[n]
    pfx=str(NS); pname=loc(rdflib.URIRef(pfx[:-1])) if False else 'd'
    def val(s,n):
        v=g.value(s,P(n)); return str(v) if v else ''
    areas=[a for a in g.subjects(RDFS.subClassOf,P(MARK)) if isinstance(a,rdflib.URIRef)]
    concepts=[c for a in areas for c in g.subjects(RDFS.subClassOf,a) if isinstance(c,rdflib.URIRef)]
    only=only or {'example','treatment','feature','axioms'}
    out=[f"# === RDODI AUTHORING SCAFFOLD (DRAFT — needs human review) for {path} ===",
         f"# Namespace: <{pfx}>  | edit the placeholders, then merge into the ontology.",
         f"@prefix d: <{pfx}> .",
         f"@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
         f"@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
         f"@prefix owl: <http://www.w3.org/2002/07/owl#> .", ""]
    notes=[]

    # ---- 1. missing-example ----
    if 'example' in only:
        gaps=[c for c in concepts if not list(g.subjects(P('ofConcept'),c))]
        if gaps:
            out.append(f"# ---- {len(gaps)} concept(s) lack a worked example: skeletons below ----")
            for c in gaps:
                cid=loc(c); lab=val(c,'label') or cid; dfn=val(c,'definition')
                out += [f"d:case_{cid}_0 a d:ExampleCase ;",
                        f'    d:ofConcept d:{cid} ;',
                        f'    d:exampleDomain "REVIEW: pick a concrete sub-domain (e.g. Retail/Healthcare/Finance)" ;',
                        f'    d:exampleText "REVIEW: one sentence — what does this example demonstrate about {lab}?" ;',
                        f'    d:caseCodeLang "turtle" ;   # prefer turtle/sparql so the result can be COMPUTED',
                        f'    d:caseCode """@prefix ex: <http://ex.org/> .',
                        f'# DRAFT example for: {lab}',
                        f'# {dfn[:90]}',
                        f'ex:subject_A a ex:{cid} .   # REVIEW: replace with a real illustrative triple""" ;',
                        f'    rdfs:comment "DRAFT scaffold — needs review" .', ""]
            notes.append(f"{len(gaps)} example skeletons drafted (concepts: {', '.join(loc(c) for c in gaps[:8])}{'…' if len(gaps)>8 else ''})")

    # ---- 2. thin-treatment ----
    if 'treatment' in only:
        thin=[c for c in concepts if len(val(c,'extendedTreatment') or val(c,'definition'))<200]
        if thin:
            out.append(f"# ---- {len(thin)} concept(s) have thin/absent treatment: templates below ----")
            for c in thin:
                cid=loc(c); lab=val(c,'label') or cid
                tmpl=(f"{lab} is REVIEW:<one-sentence definition>. "
                      f"It matters because REVIEW:<why it exists / what problem it solves>. "
                      f"In practice REVIEW:<how it is used, with a concrete domain example>. "
                      f"It relates to REVIEW:<adjacent concepts> and differs from REVIEW:<the thing it is often confused with>.")
                out += [f"d:{cid} d:extendedTreatment \"\"\"{tmpl}\"\"\" .  # DRAFT — expand to >=300 chars, then remove REVIEW: tags", ""]
            notes.append(f"{len(thin)} treatment templates drafted")

    # ---- 3. missing-feature (rich features) ----
    if 'feature' in only:
        specials=['modelComparison','techCompareRich','layeredArchitecture','inferenceContrast']
        have=sum(1 for c in concepts if any(g.value(c,P(s)) for s in specials))
        target=max(1,int(len(concepts)*0.2))
        if have<target:
            # suggest the most-connected concepts as feature candidates
            cand=sorted(concepts,key=lambda c: -len(list(g.subjects(P('ofConcept'),c))))[:target-have+2]
            out.append(f"# ---- rich features: {have}/{len(concepts)} concepts have one; target >= {target}. Candidates below ----")
            schema={"scenario":"REVIEW: one comparison scenario",
                    "techs":[{"tech":"REVIEW: technology A","note":"REVIEW: trade-off","repr_kind":"code","code":"REVIEW","lang":"turtle"},
                             {"tech":"REVIEW: technology B (recommended)","note":"REVIEW","repr_kind":"code","code":"REVIEW","lang":"turtle","recommended":True}],
                    "table_summary":{"cols":["Capability","A","B"],"rows":[["REVIEW","no","yes"]]}}
            for c in cand:
                cid=loc(c)
                out += [f'd:{cid} d:techCompareRich """{json.dumps(schema)}""" .  # DRAFT — fill REVIEW: fields (see RDODI_feature_schemas)', ""]
            notes.append(f"{len(cand)} techCompareRich skeletons drafted for high-connectivity concepts")

    # ---- 4. formal-axioms ----
    if 'axioms' in only:
        op=len(list(g.subjects(RDF.type,OWL.ObjectProperty)))
        if op<6:
            out.append("# ---- formal axioms: few object properties. Suggested domain relations below ----")
            out += ['d:relatesTo a owl:ObjectProperty ; rdfs:label "relates to" ;',
                    f'    rdfs:domain d:{MARK} ; rdfs:range d:{MARK} ;',
                    '    rdfs:comment "DRAFT — rename to a real domain relation (e.g. builtOn, validates, uses)" .', ""]
            # candidate relationships from area co-membership (very conservative)
            out.append("# Candidate relationships to assert (REVIEW each — these are suggestions, not facts):")
            for a in areas:
                cs=list(g.subjects(RDFS.subClassOf,a))
                for i in range(len(cs)-1):
                    out.append(f"# d:{loc(cs[i])} d:relatesTo d:{loc(cs[i+1])} .  # REVIEW: is there a real relation?")
            out.append("")
            notes.append("object-property + candidate-relationship scaffold drafted")
        # disjointness suggestion
        if len([1 for s,p,o in g if p==OWL.disjointWith])==0:
            out.append("# Disjointness: declare genuinely mutually-exclusive concepts, e.g.:")
            out.append(f"# d:{loc(concepts[0]) if concepts else 'ConceptA'} owl:disjointWith d:{loc(concepts[1]) if len(concepts)>1 else 'ConceptB'} .  # REVIEW")
            out.append("")

    out.append(f"# === END SCAFFOLD — {len(notes)} scaffold(s) emitted. Review, edit REVIEW: markers, then re-run the rubric. ===")
    return "\n".join(out), notes

if __name__=='__main__':
    if len(sys.argv)<2:
        print("usage: rdodi_authoring_scaffolds_v1_0_0.py <domain.ttl> [--only example,treatment,feature,axioms] [--out draft.ttl]"); sys.exit(2)
    only=None
    if '--only' in sys.argv: only=set(sys.argv[sys.argv.index('--only')+1].split(','))
    ttl,notes=run(sys.argv[1],only)
    outp=None
    if '--out' in sys.argv: outp=sys.argv[sys.argv.index('--out')+1]
    if outp:
        open(outp,'w').write(ttl); print(f"wrote draft scaffold: {outp}")
    else:
        print(ttl)
    print("\n# SUMMARY:", "; ".join(notes) if notes else "no gaps — ontology already rich", file=sys.stderr)
