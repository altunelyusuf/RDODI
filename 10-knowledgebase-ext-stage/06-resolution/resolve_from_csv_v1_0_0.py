#!/usr/bin/env python3
"""Offline-deterministic catalogue-resolution helper.

Reads a CSV of manual resolutions and emits a TTL fragment that can be appended to the KB-EXT ABox.
This is a build-time tool — NOT a gate. It never hits the network. Network resolution (Crossref API,
DBLP API, etc.) is intentionally NOT performed by this script: doing so would make the gates
non-deterministic and would risk silently treating a partial match as a confirmation. The ratifier
runs network lookups by hand (or with their own scripts), records the result in CSV, then runs this
helper to produce TTL.

Input CSV format (header line required):
  item_local_id,catalogue_local_id,identifier_kind,identifier_value,resolved_url,resolved_title,resolved_authors,resolved_year,resolved_at_utc,resolver_note

Example:
  marchewka2014,worldcat,ISBN,978-1118947074,https://www.worldcat.org/oclc/...,Information Technology Project Management 8th Edition,"Marchewka, Jack T.",2018,2026-05-29T14:30:00Z,8th edition; multiple editions exist — verify which is cited

Output: TTL fragment to stdout (or to --out file).
"""

import csv, sys, argparse, os

def esc(s): return (s or "").replace('\\','\\\\').replace('"','\\"')

def emit(rows, out_path):
    lines = [
        '# Catalogue-resolution TTL fragment — produced offline from CSV input.',
        '@prefix owl: <http://www.w3.org/2002/07/owl#> .',
        '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',
        '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .',
        '@prefix skos: <http://www.w3.org/2004/02/skos/core#> .',
        '@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .',
        '@prefix kbx: <http://example.org/rdodi/knowledgebase-ext#> .',
        '@prefix kbxi: <http://example.org/rdodi/knowledgebase-ext/instance#> .',
        '',
    ]
    per_item = {}
    for i, r in enumerate(rows, 1):
        per_item.setdefault(r['item_local_id'], []).append((i, r))
    for item_id, recs in per_item.items():
        for seq, r in recs:
            rec_iri = f"kbxi:rec_manual_{item_id}_{seq}"
            lines.append(f'{rec_iri} a kbx:CatalogueRecord, owl:NamedIndividual ;')
            lines.append(f'  rdfs:label "Manual catalogue resolution: {esc(item_id)} via {esc(r["catalogue_local_id"])}"@en ;')
            lines.append(f'  skos:definition "Manual CatalogueRecord asserting that {esc(item_id)} was located in {esc(r["catalogue_local_id"])} at {esc(r["resolved_at_utc"])}."@en ;')
            lines.append(f'  kbx:resolvedIn kbxi:cat_{r["catalogue_local_id"]} ;')
            lines.append(f'  kbx:resolvedAtUTC "{esc(r["resolved_at_utc"])}"^^xsd:dateTime ;')
            lines.append(f'  kbx:resolvedIdentifier "{esc(r["identifier_value"])}" ;')
            lines.append(f'  kbx:resolvedURL "{esc(r["resolved_url"])}" ;')
            lines.append(f'  kbx:resolvedTitle "{esc(r["resolved_title"])}" ;')
            if r.get("resolved_authors"):
                lines.append(f'  kbx:resolvedAuthors "{esc(r["resolved_authors"])}" ;')
            if r.get("resolved_year"):
                lines.append(f'  kbx:resolvedYear "{esc(r["resolved_year"])}"^^xsd:gYear ;')
            if r.get("resolver_note"):
                lines.append(f'  kbx:resolverNote "{esc(r["resolver_note"])}" ;')
            lines.append(f'  kbx:resolvedIdentifierKind "{esc(r["identifier_kind"])}" .')
            lines.append("")
        # Promote the item
        lines.append(f'kbxi:{item_id} kbx:catalogueResolution {", ".join(f"kbxi:rec_manual_{item_id}_{seq}" for seq, _ in recs)} ; kbx:consultationStatus kbx:CatalogueVerified .')
        lines.append("")
    text = "\n".join(lines) + "\n"
    if out_path:
        open(out_path, "w").write(text)
        print(f"wrote {out_path} ({len(rows)} records, {len(per_item)} items promoted)")
    else:
        print(text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Input CSV of manual resolutions (see manual_resolution_template.md for schema)")
    ap.add_argument("--out", help="Output TTL file (default: stdout)")
    args = ap.parse_args()
    if not os.path.exists(args.csv):
        print(f"FAIL: CSV not found: {args.csv}", file=sys.stderr); sys.exit(2)
    rows = list(csv.DictReader(open(args.csv, encoding="utf-8")))
    if not rows:
        print("FAIL: CSV empty", file=sys.stderr); sys.exit(2)
    expected = {"item_local_id","catalogue_local_id","identifier_kind","identifier_value","resolved_url","resolved_title","resolved_at_utc"}
    missing = expected - set(rows[0].keys())
    if missing:
        print(f"FAIL: CSV missing required columns: {missing}", file=sys.stderr); sys.exit(2)
    emit(rows, args.out)

if __name__ == "__main__":
    main()
