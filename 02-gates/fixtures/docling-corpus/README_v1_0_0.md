# docling-corpus fixtures

Real output from `docling_corpus_bridge_v1_0_0.py`, run 2026-09-15 against
`PROJECT_PROPOSAL_TEMPLATE_BRSF_v6_0.docx` (a real, operator-supplied
document, not itself committed here — not RDODI's content to redistribute;
the SHA-256 recorded in the TTL is the checkable, portable part of the
provenance, not the sandbox-local path it was run from).

- `brsf_proposal_template_corpus_v1_0_0.md` — the real, structured Markdown
  Docling produced: 76 headings (every one of the source's real section and
  sub-section levels, correctly nested), 248 table rows, recovered with
  zero manual configuration.
- `brsf_proposal_template_corpus_v1_0_0.ttl` — the real `DomainCorpus`
  individual the bridge emitted, citing genuine provenance (source SHA-256,
  Docling v2.127.0, conversion timestamp, output SHA-256).

Verified: 0 `sh:Violation` against `domain_ontology_shacl_v1_2_0.ttl`. Two
real negative cases proven separately (not committed as fixtures — both
produce no output files at all, nothing to fix a fixture against): a
missing source file (`FileNotFoundError`, exit 1) and a genuinely malformed
one (`docling.exceptions.ConversionError`, exit 1) — the bridge never
writes a corpus TTL when conversion fails, matching its own docstring's
"no silent fallback" claim.
