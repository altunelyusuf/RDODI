#!/usr/bin/env python3
"""S8e: CR-S8.2 -- real behavioral check per Optional widget, same discipline as S8a's Mandatory checks."""
import sys
from playwright.sync_api import sync_playwright

def run(html_path):
    results, errors = {}, []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.goto(f"file://{html_path}"); pg.wait_for_timeout(500)

        # DataTable: sort by TYPE (not pre-sorted, unlike name -- concepts load already alphabetical,
        # so sorting by name legitimately produces no visible change; type is the real discriminator)
        before_types = pg.eval_on_selector_all('[data-render-from="tabledata"] tr td:nth-child(2)', 'els=>els.map(e=>e.textContent)')
        pg.click('th[data-sort="type"]'); pg.wait_for_timeout(100)
        after_types = pg.eval_on_selector_all('[data-render-from="tabledata"] tr td:nth-child(2)', 'els=>els.map(e=>e.textContent)')
        results['DataTable'] = after_types == sorted(before_types) and before_types != after_types

        # CopyCodeButton: actually writes to clipboard (grant permission first)
        try:
            ctx = pg.context
            ctx.grant_permissions(['clipboard-read', 'clipboard-write'])
            pg.click('.copy-code-btn')
            pg.wait_for_timeout(150)
            clip = pg.evaluate("() => navigator.clipboard.readText()")
            results['CopyCodeButton'] = bool(clip and 'def' in clip)
        except Exception as e:
            results['CopyCodeButton'] = f'ERROR: {str(e)[:60]}'

        # MathRendering: real MathML actually renders (has child nodes, not empty)
        results['MathRendering'] = pg.eval_on_selector('math', 'el => el.children.length > 0') if pg.query_selector('math') else False

        # ProvenanceBadge: shows real, non-generic content (references an actual filename)
        results['ProvenanceBadge'] = pg.eval_on_selector('.provenance-badge', 'el => el.textContent.includes(".ttl")') if pg.query_selector('.provenance-badge') else False

        # RefinementContributionWidget: submitting actually adds to the visible list
        pg.fill('textarea[aria-label="refinement contribution"]', 'Test contribution from S8e verifier')
        pg.click('#submit-refinement'); pg.wait_for_timeout(100)
        results['RefinementContributionWidget'] = pg.eval_on_selector_all('#refinement-list li', 'els => els.length') > 0

        # ThemeSwitcher: clicking actually changes data-theme
        before_theme = pg.evaluate('() => document.documentElement.getAttribute("data-theme")')
        pg.click('.theme-switcher'); pg.wait_for_timeout(100)
        after_theme = pg.evaluate('() => document.documentElement.getAttribute("data-theme")')
        results['ThemeSwitcher'] = before_theme != after_theme

        # CopyCitationButton: writes to clipboard
        try:
            pg.click('.copy-citation-btn'); pg.wait_for_timeout(150)
            clip2 = pg.evaluate("() => navigator.clipboard.readText()")
            results['CopyCitationButton'] = bool(clip2 and len(clip2) > 5)
        except Exception as e:
            results['CopyCitationButton'] = f'ERROR: {str(e)[:60]}'

        # ChartWidget: already checked in S8c (data-driven, non-empty) -- re-confirm here
        results['ChartWidget'] = pg.eval_on_selector_all('.chart-widget rect', 'els => len(els) if False else els.length' if False else 'els => els.length') > 0

        b.close()
    return results, errors

if __name__ == "__main__":
    results, errors = run(sys.argv[1])
    for k, v in sorted(results.items()):
        ok = v is True
        print(f"[{'PASS' if ok else 'FAIL'}] {k}: {v}")
    print(f"console errors: {len(errors)}")
    ok_all = all(v is True for v in results.values()) and not errors
    print(f"\n{sum(1 for v in results.values() if v is True)}/{len(results)} PASS")
    print("OVERALL:", "PASS" if ok_all else "FAIL")
    sys.exit(0 if ok_all else 1)
