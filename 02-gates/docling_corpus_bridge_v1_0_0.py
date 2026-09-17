#!/usr/bin/env python3
"""
docling_corpus_bridge_v1_0_0.py -- Stage 1/2 bridge: runs Docling against a
real, non-code source document and emits a real rdodi-domain:DomainCorpus
individual, citing genuine provenance (source SHA-256, Docling version,
conversion timestamp, output file SHA-256).

PROVENANCE (L-105 -- adapted, not authored from scratch): closes the
syntactic/mechanic-layer gap this session's own research established --
RDODI's Stage 2 has no native parser for non-code artifacts (requirements
docs, design docs, ADRs) the way source code has an AST parser. Docling
(IBM, MIT-licensed, github.com/docling-project/docling) was chosen after a
real comparison against GROBID/MinerU/Unstructured/Marker and a real
test-drive against PROJECT_PROPOSAL_TEMPLATE_BRSF_v6_0.docx (2026-09-15):
recovered all 15 mandatory sections, every sub-heading level, and real
table structure, with zero manual configuration.

WHAT THIS BRIDGE DOES: converts a source document to structured Markdown
and declares it as a real DomainCorpus, with real provenance -- matching
DomainCorpus's own definition ("body of ... material from which candidate
concepts are extracted"). It does NOT extract concepts itself -- that is
a separate Stage 2 CorpusDrivenMethod activity, out of scope here, the
same way stage3f_ttl_bridge_v1_0_0.py bridges data into an existing gate
rather than reimplementing the gate's own logic.

Usage:
  python3 docling_corpus_bridge_v1_0_0.py --source <doc.docx|.pdf|...> \
      --out-md <corpus.md> --out-ttl <corpus.ttl> --corpus-id <local-name>
"""
import argparse
import hashlib
import re
from datetime import datetime, timezone


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run_docling(source_path):
    """Real conversion -- no simulation, no stub. Raises if Docling is
    unavailable or the conversion fails; this bridge never silently
    substitutes a fallback (the exact class of defect this session found
    and fixed twice already: rdodi_html_generator's namespace fallback,
    and instantiate_corpus's shell-content leak)."""
    from docling.document_converter import DocumentConverter
    import docling

    converter = DocumentConverter()
    result = converter.convert(source_path)
    markdown = result.document.export_to_markdown()
    docling_version = getattr(docling, "__version__", "unknown")
    return markdown, docling_version


def count_structure(markdown):
    """Real, measured structure counts -- for the provenance record, not
    for validation (a bridge records what it found; it does not judge
    whether the count is enough)."""
    headings = len(re.findall(r"^#{1,6}\s", markdown, re.M))
    table_rows = len(re.findall(r"^\|", markdown, re.M))
    return headings, table_rows


def build_ttl(corpus_id, source_path, source_sha, md_path, md_sha,
              docling_version, heading_count, table_row_count):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""@prefix rdodi-domain: <http://example.org/rdodi/domain-ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Produced by docling_corpus_bridge_v1_0_0.py -- real conversion, not simulated.
# Source: {source_path} (SHA-256 {source_sha})
# Structured output: {md_path} (SHA-256 {md_sha})
# Docling version: {docling_version}
# Converted: {now}
# Measured (not validated): {heading_count} headings, {table_row_count} table rows recovered.

<http://example.org/rdodi-corpus-bridge#{corpus_id}> a rdodi-domain:DomainCorpus, owl:NamedIndividual ;
    rdfs:label "{corpus_id}"@en ;
    dcterms:source "Converted by Docling v{docling_version} from {source_path} (SHA-256 {source_sha}), {now}. Structured output at {md_path} (SHA-256 {md_sha}), {heading_count} headings and {table_row_count} table rows recovered -- measured directly from the real conversion, not asserted."^^xsd:string ;
    skos:definition "Structured Markdown produced from a real, non-code source document via Docling -- the syntactic/mechanic layer this session's research established RDODI's Stage 2 lacked natively for artifact types with no upstream parser (requirements/design documents, unlike source code's own AST parser)."@en .
"""


def main():
    ap = argparse.ArgumentParser(description="docling_corpus_bridge_v1_0_0")
    ap.add_argument("--source", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-ttl", required=True)
    ap.add_argument("--corpus-id", required=True)
    a = ap.parse_args()

    source_sha = sha256_file(a.source)
    markdown, docling_version = run_docling(a.source)
    open(a.out_md, "w", encoding="utf-8").write(markdown)
    md_sha = sha256_file(a.out_md)
    heading_count, table_row_count = count_structure(markdown)

    ttl = build_ttl(a.corpus_id, a.source, source_sha, a.out_md, md_sha,
                     docling_version, heading_count, table_row_count)
    open(a.out_ttl, "w", encoding="utf-8").write(ttl)

    print(f"[OK] {a.source} -> {a.out_md} ({len(markdown):,} bytes, "
          f"{heading_count} headings, {table_row_count} table rows) -> {a.out_ttl}")
    print(f"[OK] Docling v{docling_version}, source SHA {source_sha[:16]}, "
          f"output SHA {md_sha[:16]}")


if __name__ == "__main__":
    main()
