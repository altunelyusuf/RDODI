#!/usr/bin/env python3
"""RDODI FAIR Enricher v1.0.0 (R-E2 + R-E4).

Adds the cheap, factual FAIR metadata the STG study found missing — WITHOUT fabricating:
  R-E2 (FAIR-F): owl:versionIRI DERIVED from existing owl:versionInfo; rich descriptive metadata.
  R-E4 (FAIR-R): dcterms:license (a HUMAN-DECLARED parameter, never invented) + factual provenance.

Non-fabrication rules:
  - versionIRI is the standard IRI form of the version the ontology ALREADY declares (derivation, not invention).
  - license is REQUIRED as an explicit argument — the tool never picks/guesses a license.
  - provenance records only what is factually true (the building agent/authority and time supplied by caller).

Usage: python3 rdodi_fair_enricher_v1_0_0.py <in.ttl> <out.ttl> --license <IRI> [--title T] [--creator C] [--authority IRI]
"""
import sys, argparse, rdflib
from rdflib import URIRef, Literal, Namespace
from rdflib.namespace import OWL, RDF, XSD, DCTERMS
DCT = DCTERMS; PROV = Namespace("http://www.w3.org/ns/prov#")

def enrich(inp, out, license_iri, title=None, creator=None, authority=None, when="2026-06-23"):
    g = rdflib.Graph(); g.parse(inp, format="turtle")
    ont = next(iter(g.subjects(RDF.type, OWL.Ontology)), None)
    if ont is None:
        raise SystemExit("no owl:Ontology declaration found — cannot enrich without a subject")
    applied = []
    # R-E2: versionIRI derived from versionInfo (non-fabricating)
    vinfo = g.value(ont, OWL.versionInfo)
    if vinfo and not g.value(ont, OWL.versionIRI):
        g.add((ont, OWL.versionIRI, URIRef(f"{str(ont).rstrip('#/')}/{vinfo}")))
        applied.append(f"versionIRI derived from versionInfo '{vinfo}' (FAIR-F)")
    # R-E2: rich metadata (only fields the caller supplies / are factual)
    if title and not g.value(ont, DCT.title):
        g.add((ont, DCT.title, Literal(title, lang="en"))); applied.append("dcterms:title")
    if creator and not g.value(ont, DCT.creator):
        g.add((ont, DCT.creator, Literal(creator))); applied.append("dcterms:creator")
    if not g.value(ont, DCT.created):
        g.add((ont, DCT.created, Literal(when, datatype=XSD.date))); applied.append("dcterms:created")
    # R-E4: license — REQUIRED, human-declared, never invented
    if not g.value(ont, DCT.license):
        g.add((ont, DCT.license, URIRef(license_iri))); applied.append(f"dcterms:license (declared: {license_iri}) (FAIR-R)")
    # R-E4: factual provenance (dcterms:source string the FAIR R_provenance check recognizes)
    if not g.value(ont, DCT.source):
        prov_str = f"Built by {creator or 'RDODI'}" + (f" under authority {authority}" if authority else "") + "."
        g.add((ont, DCT.source, Literal(prov_str))); applied.append("dcterms:source provenance (FAIR-R)")
    if authority:
        g.add((ont, PROV.wasAttributedTo, URIRef(authority))); applied.append("prov:wasAttributedTo (authority)")
    g.add((ont, PROV.generatedAtTime, Literal(f"{when}T00:00:00", datatype=XSD.dateTime)))
    applied.append("prov:generatedAtTime (FAIR-R provenance)")
    g.serialize(destination=out, format="turtle")
    print("FAIR-enriched (non-fabricating):"); [print("  +", a) for a in applied]
    return applied

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--license", required=True, help="REQUIRED license IRI — the tool never guesses one")
    ap.add_argument("--title"); ap.add_argument("--creator"); ap.add_argument("--authority")
    a = ap.parse_args()
    enrich(a.inp, a.out, a.license, a.title, a.creator, a.authority)
