#!/usr/bin/env python3
"""RDODI Presentation Renderer v1.0.0 — domain-GENERAL, profile-driven, provenance-aware.

Renders a gate-passing interactive-page ABox to rich HTML. It reads ONLY the generic page/document/prov
vocabulary and resolves domain IRIs by local name — it hardcodes NO domain (the SCP-specific renderer it
supersedes did the opposite). The genre/profile on the page drives layout; the prov chain is surfaced as
honest provenance ("where each claim came from"), and ungrounded regions are shown as ungrounded — the
presentation never masks thin or unsourced content (L-66).

Usage: python3 rdodi_presentation_renderer_v1_0_0.py <page_abox.ttl> <document_abox.ttl> <domain_tbox.ttl> <out.html>
"""
import sys, html, rdflib
from rdflib import RDF, OWL, Namespace
from rdflib.namespace import SKOS, DCTERMS, RDFS
PAGE = Namespace("http://example.org/rdodi/interactive-page-ontology#")
PROV = Namespace("http://www.w3.org/ns/prov#")
DC = Namespace("http://purl.org/dc/elements/1.1/")

def loc(u): return str(u).split("#")[-1].split("/")[-1]

# genre → light, profile-appropriate styling (no domain assumptions)
THEMES = {
    "course-document": ("#1f5f8b", "#eaf3f9", "Study Companion"),
    "technical-report": ("#37474f", "#eceff1", "Technical Report"),
    "whitepaper": ("#4527a0", "#ede7f6", "Whitepaper"),
}

def render(page_ttl, doc_ttl, domain_ttl, out_html):
    pg = rdflib.Graph(); pg.parse(page_ttl, format="turtle")
    doc = rdflib.Graph(); doc.parse(doc_ttl, format="turtle")
    tb = rdflib.Graph(); tb.parse(domain_ttl, format="turtle")

    genre = None
    for _, _, g in pg.triples((None, PAGE.hasGenre, None)): genre = str(g)
    if not genre:
        for s in pg.subjects(RDF.type, None):
            v = pg.value(s, PAGE.genre)
            if v: genre = str(v)
    genre = genre or "course-document"
    accent, soft, kind_label = THEMES.get(genre, THEMES["course-document"])

    # regions in declared order
    regions = []
    for r in pg.subjects(PROV.wasDerivedFrom, None):
        order = pg.value(r, PAGE.order)
        regions.append((int(order) if order is not None else 999, r))
    if not regions:
        regions = [(i, r) for i, r in enumerate(pg.subjects(RDF.type, OWL.NamedIndividual))]
    regions.sort()

    rows, grounded_n = [], 0
    for _, r in regions:
        title = loc(r).replace("_", " ")
        defn = pg.value(r, SKOS.definition)
        cite = pg.value(r, DCTERMS.source)
        # resolve provenance chain region -> section -> domain entity -> dc:source
        sec = pg.value(r, PROV.wasDerivedFrom)
        target = doc.value(sec, PROV.wasDerivedFrom) if sec else None
        term_src = tb.value(target, DCTERMS.source) if target else None
        if target is not None and (term_src or (cite and str(cite) in set(str(o) for o in tb.objects(None, DCTERMS.source)))):
            grounded_n += 1
            prov_html = (f"<div class='prov ok'>provenance: derived from "
                         f"<code>{html.escape(loc(target))}</code>"
                         f" · source: {html.escape(str(term_src or cite))}</div>")
        else:
            prov_html = ("<div class='prov gap'>provenance: chain does not resolve to a grounded source "
                         "(ungrounded — flagged, not hidden)</div>")
        body = html.escape(str(defn)) if defn else "<em>(no grounded content for this region)</em>"
        rows.append(f"<section class='card'><h2>{html.escape(title)}</h2>"
                    f"<p>{body}</p>{prov_html}</section>")

    total = len(regions)
    honesty = (f"{grounded_n}/{total} regions resolve to a grounded source. "
               + ("" if grounded_n == total else "Ungrounded regions are flagged above — this page reflects "
                  "the artifact's real provenance state, including gaps."))
    doc_title = next((str(pg.value(s, RDFS.label)) for s in pg.subjects(RDF.type, PAGE.Page)
                      if pg.value(s, RDFS.label)), f"{kind_label}")

    html_out = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(doc_title)}</title><style>
:root {{ --accent:{accent}; --soft:{soft}; }}
* {{ box-sizing:border-box; }} body {{ font-family:-apple-system,Segoe UI,Roboto,sans-serif; margin:0; color:#1a1a1a; background:#fafafa; }}
header {{ background:var(--accent); color:#fff; padding:28px 32px; }}
header .kind {{ opacity:.85; font-size:13px; text-transform:uppercase; letter-spacing:.08em; }}
header h1 {{ margin:6px 0 0; font-size:26px; }}
.honesty {{ background:var(--soft); border-left:4px solid var(--accent); padding:12px 32px; font-size:14px; color:#333; }}
main {{ max-width:820px; margin:0 auto; padding:24px 20px; }}
.card {{ background:#fff; border:1px solid #e3e3e3; border-radius:10px; padding:18px 20px; margin:14px 0; }}
.card h2 {{ margin:0 0 8px; font-size:18px; color:var(--accent); }}
.card p {{ margin:0 0 10px; line-height:1.55; }}
.prov {{ font-size:12.5px; padding:7px 10px; border-radius:6px; }}
.prov.ok {{ background:#eef7ee; color:#27632a; }} .prov.ok code {{ background:#dceedc; padding:1px 5px; border-radius:4px; }}
.prov.gap {{ background:#fdeeee; color:#8a2a2a; }}
footer {{ text-align:center; color:#888; font-size:12px; padding:20px; }}
</style></head><body>
<header><div class="kind">{html.escape(kind_label)} · genre: {html.escape(genre)}</div><h1>{html.escape(doc_title)}</h1></header>
<div class="honesty">{html.escape(honesty)}</div>
<main>{''.join(rows)}</main>
<footer>Rendered by RDODI Presentation Renderer v1.0.0 — domain-general, profile-driven, provenance-surfaced.</footer>
</body></html>"""
    open(out_html, "w").write(html_out)
    return total, grounded_n, genre

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(__doc__); raise SystemExit(2)
    t, gr, genre = render(*sys.argv[1:5])
    print(f"rendered {t} regions ({gr} grounded) genre={genre} -> {sys.argv[4]}")
