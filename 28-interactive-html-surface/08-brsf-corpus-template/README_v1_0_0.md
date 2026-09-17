# BRSF Corpus Template

A generic template and instantiation tool for producing a single-file,
self-contained interactive HTML "knowledge base" page from any small
corpus — a set of principles/items organized by category, with typed
relations between them and citations to external frameworks. The page
that comes out is a real, working single-page application: a
hierarchical sidebar, a relation map, an ontology/taxonomy graph, an
agent-based Q&A console (deterministic by default, optionally backed by
in-browser LLM inference via WebGPU), an in-browser Python code lab
(via Pyodide), and a SPARQL console (via a WASM-compiled RDF store) —
all running client-side, no backend required.

## What's here

- `01-schema/` — the corpus contract: the JSON shape your data needs to
  supply (required fields: `MISSION`, `CATEGORIES`, `PRINCIPLES`,
  `FRAMEWORKS`, `RELATIONS`; several optional fields with documented
  defaults).
- `02-tooling/instantiate_corpus_v1_2_0.py` — the instantiation tool.
  Takes a source HTML template and a corpus JSON file, swaps the
  corpus-specific constants, and applies a set of unconditional
  shell-identity transforms (dark-mode support, a live sidebar filter,
  a restructured tree-row layout, a genuine force-directed ontology
  graph, and several real UI-layout fixes) so every instance benefits
  from fixes made to any one of them.
- `03-example-corpus/`, `04-rdodi-corpus/` — two example corpora this
  template has been instantiated against.
- `06-instance/` — a built, verified instance (RDODI's own principles
  corpus), ready to open directly in a browser.

## Try it

```bash
cd 02-tooling
python3 instantiate_corpus_v1_2_0.py \
    --source <your-source-template.html> \
    --corpus <your-corpus.json> \
    --out out/my_instance.html
# open out/my_instance.html in a browser
```

The `02-tooling` directory's own docstrings describe exactly which
constants and shell transforms the tool applies, and why each one
exists — several were added in direct response to real, specific UI
bugs found by testing the generated page in a real browser (an
in-browser Python code lab whose preset buttons silently produced no
code; a UI layout where the primary input control was pushed off-screen
below several rows of secondary configuration and explanatory text; a
malformed-HTML bug that let one view's contents leak into unrelated
tabs). Each is documented at its own fix site in the tool's source.

## A note on the source template

This package's own development used an internal, unpublished source
template as its working example while building and testing the tool —
not included here, since it carried real internal content. The tool
itself has no dependency on that specific template: point it at any
HTML page that follows the pattern its own docstrings describe (a
`buildExplorer()`-style sidebar renderer, corpus constants declared as
top-level `const` assignments, `.subview`/`.subtabs` navigation) and a
corpus JSON matching `01-schema/`'s contract, and it will produce a
working instance.

## License & attribution

CC BY 4.0 — © 2026 Yusuf Altunel, İstanbul Kültür Üniversitesi.
