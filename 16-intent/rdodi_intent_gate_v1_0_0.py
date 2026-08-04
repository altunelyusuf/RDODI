#!/usr/bin/env python3
"""RDODI Intent-Conformance Gate v1.0.0 (B6) — MECHANICAL conformance only.
Checks the generated artifact against the declared authorial intent: are the must-cover concepts actually
covered (via the prov chain)? are excluded concepts absent? does the genre match? It reports coverage and
gaps. It does NOT certify that the artifact fulfils the author's deeper intent — that residual is tier-C
human judgment (L-66)."""
import sys, rdflib
from rdflib import Namespace
from rdflib.namespace import RDFS
INTENT = Namespace("http://example.org/rdodi/intent#")
PROV = Namespace("http://www.w3.org/ns/prov#")
IP = Namespace("http://example.org/rdodi/interactive-page-ontology#")
def loc(u): return str(u).split("#")[-1]
def check(intent_ttl, doc_ttl, page_ttl):
    it = rdflib.Graph(); it.parse(intent_ttl, format="turtle")
    doc = rdflib.Graph(); doc.parse(doc_ttl, format="turtle")
    pg = rdflib.Graph(); pg.parse(page_ttl, format="turtle")
    must = set(it.objects(None, INTENT.mustCoverConcept))
    excluded = set(it.objects(None, INTENT.excludedConcept))
    want_genre = it.value(None, INTENT.intendedGenre)
    covered = set(doc.objects(None, PROV.wasDerivedFrom))
    missing = must - covered
    excl_viol = excluded & covered
    got_genre = pg.value(None, IP.genre)
    genre_ok = (str(got_genre) == str(want_genre)) if want_genre else True
    verdict = "PASS" if (not missing and not excl_viol and genre_ok) else "FAIL"
    print(f"=== Intent-Conformance (mechanical) : {verdict} ===")
    print(f" must-cover: {len(must-missing)}/{len(must)} covered" + (f"  MISSING: {[loc(m) for m in missing]}" if missing else ""))
    print(f" exclusions: {'respected' if not excl_viol else 'VIOLATED: '+str([loc(e) for e in excl_viol])}")
    print(f" genre: {'match' if genre_ok else f'MISMATCH (want {want_genre}, got {got_genre})'}")
    print(" residual (NOT certified): whether the artifact fulfils the author's deeper intent is human judgment.")
    return verdict
if __name__ == "__main__":
    if len(sys.argv) < 4: print(__doc__); raise SystemExit(2)
    sys.exit(0 if check(sys.argv[1], sys.argv[2], sys.argv[3]) == "PASS" else 1)
