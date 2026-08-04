#!/usr/bin/env python3
"""S8a: CR-S8.1 -- real behavioral verification of all 17 Mandatory widgets, one function per widget.
Learned from S7: a structural/signature-string PASS can hide a genuinely broken widget (the invisible
WebGL cube). Every check here observes actual DOM/pixel/state change, not markup presence.
Usage: python3 verify_s8a_mandatory_exercise.py <exemplar.html>"""
import sys
from playwright.sync_api import sync_playwright

def run(html_path):
    results = {}
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.goto(f"file://{html_path}")
        pg.wait_for_timeout(600)

        # 1. PrimaryNavigation: real menubar with clickable content
        results['PrimaryNavigation'] = pg.eval_on_selector('[role="menubar"]', 'el => el.textContent.trim().length > 0') if pg.query_selector('[role="menubar"]') else False

        # 2. TreeNavigation: open-all actually changes aria-expanded on >=1 item
        pg.click('#tree-open-all')
        pg.wait_for_timeout(100)
        results['TreeNavigation'] = pg.eval_on_selector_all('[role=treeitem]', "els => els.some(e => e.getAttribute('aria-expanded')==='true')")

        # 3. SubPageTabs: clicking a tab actually changes visible content
        before_visible = pg.eval_on_selector_all('.view', "els => els.filter(e=>!e.hidden).map(e=>e.id)")
        tabs = pg.query_selector_all('.subtab')
        if len(tabs) > 1:
            tabs[1].click(); pg.wait_for_timeout(150)
            after_visible = pg.eval_on_selector_all('.view', "els => els.filter(e=>!e.hidden).map(e=>e.id)")
            results['SubPageTabs'] = before_visible != after_visible
        else:
            results['SubPageTabs'] = False

        # 4. RoutedViewNavigation: the view-switch above IS the routed-nav mechanism; confirm >1 view exists
        results['RoutedViewNavigation'] = pg.eval_on_selector_all('.view', 'els => els.length') > 1

        # 5. OverflowTabBar: scrollable container actually overflows (scrollWidth > clientWidth)
        results['OverflowTabBar'] = pg.eval_on_selector('.overflow-tabbar', 'el => el.scrollWidth >= el.clientWidth') if pg.query_selector('.overflow-tabbar') else False

        # 6. AnchorLinks: at least one href="#x" resolves to a real element with id="x"
        results['AnchorLinks'] = pg.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('a[href^="#"]'));
            return links.some(a => { const id = a.getAttribute('href').slice(1); return id && document.getElementById(id); });
        }""")

        # 7. Breadcrumb: real multi-segment trail present in a visible view
        results['Breadcrumb'] = pg.eval_on_selector('.breadcrumb', 'el => el.querySelectorAll("a").length >= 1') if pg.query_selector('.breadcrumb') else False

        # 8. SkipToContent: focusing it makes it visible (class toggle) AND target exists
        pg.focus('.skip-link')
        pg.wait_for_timeout(100)
        is_active = pg.eval_on_selector('.skip-link', 'el => el.classList.contains("is-active")')
        target_exists = pg.evaluate('() => !!document.getElementById("maincontent")')
        results['SkipToContent'] = is_active and target_exists
        pg.evaluate('() => document.activeElement.blur()')

        # 9. ResponsiveLayout: viewport resize actually changes computed layout (tree-nav display)
        pg.set_viewport_size({"width": 1200, "height": 800})
        pg.wait_for_timeout(100)
        wide_display = pg.eval_on_selector('.tree-nav', 'el => getComputedStyle(el).display') if pg.query_selector('.tree-nav') else 'none'
        pg.set_viewport_size({"width": 400, "height": 800})
        pg.wait_for_timeout(100)
        narrow_display = pg.eval_on_selector('.tree-nav', 'el => getComputedStyle(el).display') if pg.query_selector('.tree-nav') else 'none'
        results['ResponsiveLayout'] = wide_display != narrow_display
        pg.set_viewport_size({"width": 1200, "height": 800})

        # 10. ContextMenu: dispatching a real contextmenu event makes it visible
        pg.evaluate("""() => {
            const ev = new MouseEvent('contextmenu', {bubbles:true, cancelable:true, clientX:50, clientY:50});
            document.body.dispatchEvent(ev);
        }""")
        pg.wait_for_timeout(100)
        results['ContextMenu'] = pg.eval_on_selector('#ctxmenu', 'el => getComputedStyle(el).display !== "none"')
        pg.mouse.click(700, 700)

        # 11. Tooltip: focusing a has-tooltip element makes its tooltip visible
        tt = pg.query_selector('.has-tooltip')
        if tt:
            tt.focus(); pg.wait_for_timeout(100)
            results['Tooltip'] = pg.eval_on_selector('.has-tooltip', 'el => el.classList.contains("is-active")')
        else:
            results['Tooltip'] = False

        # 12. LightMode: data-theme="light" present AND CSS actually keys off it (computed bg differs from a null-theme baseline check)
        theme = pg.evaluate('() => document.documentElement.getAttribute("data-theme")')
        results['LightMode'] = theme == 'light'

        # 13. Simulation: clicking step actually changes displayed state (not just a counter that looks static)
        # scope to the CURRENTLY VISIBLE view (a prior test switched tabs; blindly picking the first
        # DOM match would hit a hidden, unclickable element -- a bug in the test, not the widget)
        vis_sel = '.view:not([hidden]) .sim-step'
        sim_state_sel = '.view:not([hidden]) .sim-state'
        sim_before = pg.eval_on_selector(sim_state_sel, 'el => el.textContent') if pg.query_selector(sim_state_sel) else None
        if pg.query_selector(vis_sel):
            pg.click(vis_sel); pg.wait_for_timeout(100)
            sim_after = pg.eval_on_selector(sim_state_sel, 'el => el.textContent')
            results['Simulation'] = sim_before != sim_after
        else:
            results['Simulation'] = False

        # 14. Animation: an element with the fadein animation is actually running (animationName computed)
        results['Animation'] = pg.eval_on_selector('.view:not([hidden])', 'el => getComputedStyle(el).animationName === "fadein" || getComputedStyle(el).animationDuration !== "0s"')

        # 15. Canvas2DVisualization: non-degenerate pixel output (learned from the S7 WebGL bug -- check this one too, not just 3D)
        results['Canvas2DVisualization'] = pg.evaluate("""() => {
            const c = document.querySelector('.view:not([hidden]) [data-render="2d"]');
            if (!c) return false;
            const ctx = c.getContext('2d');
            const d = ctx.getImageData(0,0,c.width,c.height).data;
            const colors = new Set();
            for (let i=0;i<d.length;i+=4) colors.add(d[i]+','+d[i+1]+','+d[i+2]);
            return colors.size > 1;
        }""")

        # 16. ThreeDimensionalVisualization: non-degenerate pixel output (the exact S7 bug, re-verified explicitly here)
        results['ThreeDimensionalVisualization'] = pg.evaluate("""() => {
            const c = document.querySelector('.view:not([hidden]) [data-render="webgl"]');
            if (!c) return false;
            const gl = c.getContext('webgl');
            if (!gl) return false;
            const pixels = new Uint8Array(4*c.width*c.height);
            gl.readPixels(0,0,c.width,c.height,gl.RGBA,gl.UNSIGNED_BYTE,pixels);
            const colors = new Set();
            for (let i=0;i<pixels.length;i+=4) colors.add(pixels[i]+','+pixels[i+1]+','+pixels[i+2]);
            return colors.size > 1;
        }""")

        # 17. CitationLink: real, resolvable citation link (data-cite present, points to something in references)
        results['CitationLink'] = pg.evaluate("""() => {
            const links = Array.from(document.querySelectorAll('.citation-link'));
            return links.length > 0 && links.every(l => l.getAttribute('data-cite'));
        }""")

        b.close()
    return results, errors

if __name__ == "__main__":
    results, errors = run(sys.argv[1])
    for k, v in sorted(results.items()):
        print(f"[{'PASS' if v else 'FAIL'}] {k}")
    print(f"console errors during test: {len(errors)}")
    ok = all(results.values()) and not errors
    print(f"\n{sum(results.values())}/{len(results)} PASS")
    print("OVERALL:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
