#!/usr/bin/env python3
"""RDODI Source Consultation ingestor v1.0.0.

Ingests a primary source file (PDF or plain text), extracts citable passages with page anchors,
emits an aa:ConsultedSource ABox so the AA.consultation_link gate has real evidence to verify
claims against. PDF text extraction uses pypdf when available; plain text is split into ~150-word
passages keyed to line ranges. SHA-256 of the source file is recorded for tamper-detection.

Usage:
  python3 ingest_source.py --source <path> --citation-id <id> --out <abox.ttl> [--passages-per-page N]

The emitted ABox declares demo:cite_<id> a aa:ConsultedSource with aa:sourceHash, aa:ingestedAt,
and one aa:ConsultedPassage per extracted span. Re-types the existing Citation as ConsultedSource
when merged. Honest: extraction is best-effort; verbatim accuracy of pdf-extracted text is the
responsibility of the attester reviewing the passages.
"""
import os, sys, hashlib, datetime, argparse, re

def _sha256(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()

def _extract_text_pdf(path):
    """Returns list of (page_label, text) tuples."""
    try:
        import pypdf
    except ImportError:
        try:
            from pypdf import PdfReader
        except ImportError:
            print("pypdf not installed; pip install pypdf", file=sys.stderr); sys.exit(2)
    from pypdf import PdfReader
    r = PdfReader(path); out = []
    for i, page in enumerate(r.pages):
        try: txt = page.extract_text() or ""
        except Exception: txt = ""
        out.append((f"p.{i+1}", txt))
    return out

def _extract_text_plain(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    # split into chunks of ~150 words, anchor by line range
    words = re.findall(r"\S+|\n", txt); chunks=[]; cur=[]; cur_lines=0
    cur_start=1; line=1
    for w in words:
        if w=="\n": line+=1; cur.append(w); continue
        cur.append(w)
        if sum(1 for x in cur if x!="\n") >= 150:
            chunks.append((f"l.{cur_start}-{line}"," ".join(x for x in cur if x!='\n')))
            cur=[]; cur_start=line+1
    if cur: chunks.append((f"l.{cur_start}-{line}"," ".join(x for x in cur if x!='\n')))
    return chunks

def ingest(source_path, citation_id, out_path, max_passages=20):
    if not os.path.exists(source_path):
        print(f"FAIL: source not found: {source_path}", file=sys.stderr); sys.exit(2)
    h = _sha256(source_path)
    if source_path.lower().endswith(".pdf"): passages = _extract_text_pdf(source_path)
    else: passages = _extract_text_plain(source_path)
    # filter empty/near-empty pages; cap
    passages = [(a,t) for a,t in passages if len(t.strip())>50][:max_passages]
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    cid = f"demo:cite_{citation_id}"
    lines = [
      "@prefix demo: <http://example.org/demo-pqm#> .",
      "@prefix aa: <http://example.org/rdodi/academic-authoring#> .",
      "@prefix rres: <http://example.org/rdodi/research-ontology#> .",
      "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
      "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
      "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
      "",
      f'{cid} a aa:ConsultedSource, rres:Citation, owl:NamedIndividual ;',
      f'  rdfs:label "Consulted source: {citation_id}"@en ;',
      f'  aa:sourceHash "{h}" ;',
      f'  aa:ingestedAt "{ts}"^^xsd:dateTime ;',
      f'  rres:hasContext "primary; verified=True; reconstruction=False; not_consulted_at_authoring=False; ingested_from={os.path.basename(source_path)}"',
    ]
    if passages:
        lines[-1] = lines[-1] + " ;"
        lines.append("  " + " , ".join(f"aa:hasPassage demo:cite_{citation_id}_pas{i}" for i,_ in enumerate(passages)) + " .")
        for i,(anchor,text) in enumerate(passages):
            safe = text.replace("\\","\\\\").replace('"','\\"').replace("\n"," ").strip()[:600]
            lines.append(f'\ndemo:cite_{citation_id}_pas{i} a aa:ConsultedPassage, owl:NamedIndividual ;')
            lines.append(f'  rdfs:label "Passage {i+1} of {citation_id}"@en ;')
            lines.append(f'  aa:pageAnchor "{anchor}" ;')
            lines.append(f'  aa:verbatimText "{safe}" .')
    else:
        lines[-1] = lines[-1] + " ."
    open(out_path,"w").write("\n".join(lines)+"\n")
    print(f"ingested {citation_id}: {len(passages)} passage(s), sha256={h[:16]}…, out={out_path}")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--citation-id", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-passages", type=int, default=20)
    a=ap.parse_args()
    ingest(a.source, a.citation_id, a.out, a.max_passages)
