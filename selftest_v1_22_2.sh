#!/usr/bin/env bash
# RDODI Public Edition selftest v1.22.2 — parse + SHACL over the shipped public tree
set -e
echo "== all TTLs parse =="
python3 - << 'PY'
import glob, rdflib, sys
bad=[]
for f in glob.glob('**/*.ttl', recursive=True):
    try: rdflib.Graph().parse(f, format='turtle')
    except Exception as e: bad.append((f,str(e)[:60]))
print(f"  parsed {len(glob.glob('**/*.ttl',recursive=True))-len(bad)} files, {len(bad)} failures")
sys.exit(1 if bad else 0)
PY
echo "== domain module SHACL =="
python3 - << 'PY'
import rdflib, pyshacl
d=rdflib.Graph(); d.parse('01-stage-vocabularies/02-domain/domain_ontology_tbox_v1_1_1.ttl'); d.parse('01-stage-vocabularies/02-domain/domain_ontology_abox_v1_0_1.ttl')
s=rdflib.Graph(); s.parse('01-stage-vocabularies/02-domain/domain_ontology_shacl_v1_1_0.ttl')
c,_,rt=pyshacl.validate(d, shacl_graph=s, inference='rdfs')
v=rt.count('Severity: sh:Violation'); print(f"  conforms={c} violations={v}"); import sys; sys.exit(0 if v==0 else 1)
PY
echo "== KB abox parses =="
python3 -c "import rdflib;g=rdflib.Graph();g.parse('09-knowledgebase-stage/01-vocabularies/rdodi_knowledgebase_abox_v1_4_1.ttl');print(f'  {len(g)} triples')"
echo "== SELFTEST PASS =="
