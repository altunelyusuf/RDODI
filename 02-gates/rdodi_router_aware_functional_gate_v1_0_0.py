#!/usr/bin/env python3
"""RDODI router-aware widget-functional gate v1.0.0 — generalized (A7b/A6).
Navigates each routed view containing an exhibit, asserts every mount RENDERS (non-inert) and the surface emits
0 console errors. Usage: python3 rdodi_router_aware_functional_gate_v1_0_0.py <page.html>  (exit 0=PASS)"""
import sys, pathlib
from playwright.sync_api import sync_playwright
def main():
    if len(sys.argv) < 2: print(__doc__); return 2
    html = pathlib.Path(sys.argv[1]).resolve(); errors = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.on("console", lambda m: errors.append(m.text) if m.type=="error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(f"file://{html}"); pg.wait_for_timeout(800)
        mounts = pg.eval_on_selector_all(".widget-mount, .widget",
            "els => els.map(e => { let v=e.closest('section.view'); return v? v.id:''; })")
        views = sorted(set(v for v in mounts if v)); rendered = inert = 0
        for vid in views:
            pg.evaluate(f"location.hash = '#{vid}'"); pg.wait_for_timeout(450)
            info = pg.eval_on_selector_all(f"#{vid} .widget-mount, #{vid} .widget",
                "els => els.map(e => (e.querySelector('svg,img,canvas') || e.children.length>0) ? 1 : 0)")
            rendered += sum(info); inert += sum(1 for x in info if not x)
        ok = inert == 0 and len(errors) == 0
        print(f"exhibit views={len(views)} mounts_rendered={rendered} inert={inert} console_errors={len(errors)}")
        for e in errors[:5]: print("  !", e[:80])
        print("OVERALL:", "PASS" if ok else "FAIL"); b.close()
    return 0 if ok else 1
if __name__ == "__main__": sys.exit(main())
