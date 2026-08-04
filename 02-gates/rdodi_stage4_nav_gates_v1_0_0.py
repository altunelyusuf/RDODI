#!/usr/bin/env python3
"""RDODI Stage-4 navigation gates v1.0.0 — bootstrap-wireable adapters (A7).
Exposes gate_affordance_grounding + gate_router_functional returning GateResult(gate_id, verdict, detail),
matching the pipeline's rec() contract. Both DEGRADE HONESTLY to CANNOT_RUN (never a false PASS) when the HTML
or a browser is absent — the missing precondition is surfaced, not papered over."""
import os, rdflib
from collections import namedtuple
from rdflib import RDF, Namespace
GateResult = namedtuple("GateResult", ["gate_id", "verdict", "detail"])
PG = Namespace("http://example.org/rdodi/interactive-page-ontology#")
SIG = {'Menu':'role="menubar"','ContextMenu':'id="ctxmenu"','TreeNavigation':'role="tree"',
       'Tooltip':'role="tooltip"','PrimaryNavigation':'role="menubar"','TableOfContents':'role="tree"',
       'AnchorLinks':'href="#','FocusIndicator':':focus','CurrentLocationIndicator':'aria-current',
       'RoutedViewNavigation':'class="view','OverflowTabBar':'menubar'}

def gate_affordance_grounding(gate_id, page_ttl, html_path):
    if not (page_ttl and os.path.exists(page_ttl) and html_path and os.path.exists(html_path)):
        return GateResult(gate_id, "CANNOT_RUN", "page TTL or generated HTML absent — grounding not evaluable (not a pass)")
    g = rdflib.Graph(); g.parse(page_ttl); H = open(html_path, encoding='utf-8').read()
    declared = {str(t).split('#')[-1] for s,p,o in g for t in g.objects(o, RDF.type)
                if p in (PG.includesNavigationPattern, PG.includesWayfindingAffordance, PG.usesUIPattern)}
    model_gap = [k for k,sig in SIG.items() if sig in H and k not in declared]
    art_gap   = [k for k in declared if k in SIG and SIG[k] not in H]
    if model_gap or art_gap:
        return GateResult(gate_id, "FAIL", f"realized-not-declared={model_gap}; declared-not-realized={art_gap}")
    return GateResult(gate_id, "PASS", f"{len(declared)} affordances grounded both directions")

def gate_router_functional(gate_id, html_path):
    if not (html_path and os.path.exists(html_path)):
        return GateResult(gate_id, "CANNOT_RUN", "generated HTML absent — functional test not evaluable (not a pass)")
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return GateResult(gate_id, "CANNOT_RUN", "playwright/browser unavailable — functional test not evaluable (not a pass)")
    import pathlib
    html = pathlib.Path(html_path).resolve(); errors = []
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page()
            pg.on("console", lambda m: errors.append(m.text) if m.type=="error" else None)
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.goto(f"file://{html}"); pg.wait_for_timeout(700)
            mounts = pg.eval_on_selector_all(".widget-mount, .widget",
                "els => els.map(e => { let v=e.closest('section.view'); return v? v.id:''; })")
            views = sorted(set(v for v in mounts if v)); rendered = inert = 0
            for vid in views:
                pg.evaluate(f"location.hash = '#{vid}'"); pg.wait_for_timeout(400)
                info = pg.eval_on_selector_all(f"#{vid} .widget-mount, #{vid} .widget",
                    "els => els.map(e => (e.querySelector('svg,img,canvas')||e.children.length>0)?1:0)")
                rendered += sum(info); inert += sum(1 for x in info if not x)
            b.close()
    except Exception as e:
        return GateResult(gate_id, "CANNOT_RUN", f"browser launch failed: {str(e)[:50]} (not a pass)")
    ok = inert == 0 and len(errors) == 0
    return GateResult(gate_id, "PASS" if ok else "FAIL",
                      f"views={len(views)} rendered={rendered} inert={inert} console_errors={len(errors)}")
