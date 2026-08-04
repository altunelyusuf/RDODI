#!/usr/bin/env python3
"""RDODI Module-Assembly Resolver v1.0.0 (R-E8).

The harness (R-E7) measured the need: a mechanical comparison of a modular/import ontology reproduces partial-merge
artifacts (e.g. the spurious 17 SHACL violations in P3) unless the module closure is assembled correctly first.

This resolver assembles a complete ontology from its owl:imports closure, deterministically and offline:
  - builds an ontologyIRI -> local-file map across the given search roots;
  - follows owl:imports transitively from a root file, resolving each target to a LOCAL file (never the network);
  - merges all modules into one graph (rdflib graph union dedups triples — no duplication);
  - reports every module included AND any import it could NOT resolve locally (no silent drop).

Usage: python3 rdodi_module_assembly_resolver_v1_0_0.py <root.ttl> <out.ttl> <search_dir> [<search_dir> ...]
"""
import sys, glob, os, rdflib
from rdflib import OWL, RDF

def _index(search_dirs):
    iri2file = {}
    for d in search_dirs:
        for f in glob.glob(os.path.join(d, "**", "*.ttl"), recursive=True):
            try:
                g = rdflib.Graph(); g.parse(f, format="turtle")
                for o in g.subjects(RDF.type, OWL.Ontology):
                    iri2file[str(o).rstrip("#/")] = f
            except Exception:
                pass
    return iri2file

def resolve(root_file, search_dirs):
    iri2file = _index(search_dirs)
    merged = rdflib.Graph()
    included, unresolved, queue, seen_files = [], [], [root_file], set()
    while queue:
        f = queue.pop(0)
        if f in seen_files:
            continue
        seen_files.add(f)
        g = rdflib.Graph(); g.parse(f, format="turtle")
        before = len(merged)
        merged += g
        included.append((os.path.basename(f), len(g), len(merged) - before))  # (file, triples, new triples added)
        for tgt in g.objects(None, OWL.imports):
            key = str(tgt).rstrip("#/")
            if key in iri2file:
                queue.append(iri2file[key])
            else:
                unresolved.append(str(tgt))
    # after inlining the closure, owl:imports statements are redundant; removing them makes the assembly
    # self-contained and DL-checkable (the reasoner no longer tries to fetch already-merged modules).
    n_imp = 0
    for s_,p_,o_ in list(merged.triples((None, OWL.imports, None))):
        merged.remove((s_, p_, o_)); n_imp += 1
    return merged, {"modules_included": included, "unresolved_imports": sorted(set(unresolved)),
                    "total_triples": len(merged), "imports_stripped": n_imp}

def main():
    if len(sys.argv) < 4:
        print(__doc__); raise SystemExit(2)
    root, out, dirs = sys.argv[1], sys.argv[2], sys.argv[3:]
    merged, rep = resolve(root, dirs)
    merged.serialize(destination=out, format="turtle")
    print(f"assembled {len(rep['modules_included'])} modules -> {rep['total_triples']} triples -> {out}")
    for name, t, added in rep["modules_included"]:
        print(f"  + {name}: {t} triples ({added} new)")
    print(f"  stripped {rep.get('imports_stripped',0)} redundant owl:imports (assembly is self-contained)")
    if rep["unresolved_imports"]:
        print("  UNRESOLVED imports (reported, not dropped silently):")
        for u in rep["unresolved_imports"]:
            print("    !", u)
    else:
        print("  all imports resolved to local files (offline).")
    return rep

if __name__ == "__main__":
    main()
