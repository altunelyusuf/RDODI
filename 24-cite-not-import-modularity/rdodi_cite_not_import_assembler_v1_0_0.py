#!/usr/bin/env python3
"""RDODI Cite-Not-Import Assembler v1.0.0 (R-E3).

RDODI's OWN modularity — distinct from R-E8. R-E8 follows owl:imports (for import-based ontologies). R-E3 assembles
RDODI module sets declared in a MANIFEST, merged by reference-resolution, with ZERO owl:imports (L-64). Modules add
depth by referencing base classes via IRI; the assembler simply merges the declared files. The result stays full-DL
(no dangling import statements to fetch), in deliberate contrast to owl:imports modularity which forces RL fallback.
Usage: python3 rdodi_cite_not_import_assembler_v1_0_0.py <manifest.ttl> <out.ttl>
"""
import sys, os, rdflib
from rdflib import OWL, Namespace
RDODI = Namespace("http://example.org/rdodi/modules#")

def assemble(manifest_path, out_path):
    base = os.path.dirname(os.path.abspath(manifest_path))
    m = rdflib.Graph(); m.parse(manifest_path, format="turtle")
    files = [str(o) for o in m.objects(None, RDODI.file)]
    merged = rdflib.Graph(); included = []
    for rel in files:
        f = os.path.join(base, rel)
        g = rdflib.Graph(); g.parse(f, format="turtle")
        before = len(merged); merged += g
        included.append((os.path.basename(f), len(g), len(merged) - before))
    # L-64 invariant: the assembled module set must contain NO owl:imports
    n_imp = len(list(merged.objects(None, OWL.imports)))
    merged.serialize(destination=out_path, format="turtle")
    print(f"assembled {len(included)} cite-not-import modules -> {len(merged)} triples -> {out_path}")
    for name, t, added in included:
        print(f"  + {name}: {t} triples ({added} new)")
    print(f"  owl:imports in assembly: {n_imp} (L-64 invariant: MUST be 0)")
    if n_imp:
        raise SystemExit("L-64 VIOLATION: assembled module set contains owl:imports")
    return merged

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); raise SystemExit(2)
    assemble(sys.argv[1], sys.argv[2])
