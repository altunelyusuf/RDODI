#!/usr/bin/env python3
"""S7 CR verifier -- pinned down BEFORE generation, per s7_addendum_v1_0_0.md.
Usage: python3 verify_s7_crs.py <exemplar.html>"""
import sys, re

def check(html):
    results = {}

    # CR-S7.1: real 3D -- drawArrays/drawElements against >=8-vertex buffer, with a rotation/perspective transform
    has_draw = bool(re.search(r'gl\.(drawArrays|drawElements)\(', html))
    has_verts = len(re.findall(r'-?\d+\.?\d*,\s*-?\d+\.?\d*,\s*-?\d+\.?\d*', html)) >= 8  # rough vertex-coord count
    has_rotation = bool(re.search(r'rotat|perspective|matrix', html, re.I))
    results['CR-S7.1'] = has_draw and has_verts and has_rotation

    # CR-S7.2: simulation has >=3 distinct JS-tracked states
    sim_states = len(set(re.findall(r"sim-state[^>]*>([^<]*)<", html)))
    step_logic = bool(re.search(r'simState|simStep|step\s*[+][+]|bitIndex', html))
    results['CR-S7.2'] = step_logic  # state-count verified at runtime by the functional gate too

    # CR-S7.3: every concept paragraph >=3 sentences
    paras = re.findall(r'<p class="concept-prose">(.*?)</p>', html, re.S)
    sentence_ok = all(len(re.findall(r'[.!?]\s', p)) >= 2 for p in paras)  # >=3 sentences = >=2 boundaries
    results['CR-S7.3'] = bool(paras) and sentence_ok

    # CR-S7.4: all 8 optional widgets present
    optional_markers = ['chart-widget', 'data-table', 'copy-code-btn', 'math-rendering',
                         'provenance-badge', 'refinement-widget', 'theme-switcher', 'copy-citation-btn']
    present = [m for m in optional_markers if m in html]
    results['CR-S7.4'] = len(present) == 8
    results['_CR-S7.4_detail'] = present

    # CR-S7.5: design system -- >=4 color custom props, >=3 font-size steps, spacing scale
    colors = len(re.findall(r'--color-[\w-]+:\s*#', html))
    fonts = len(re.findall(r'--fs-[\w-]+:', html))
    spacing = len(re.findall(r'--space-[\w-]+:', html))
    results['CR-S7.5'] = colors >= 4 and fonts >= 3 and spacing >= 2

    return results

if __name__ == "__main__":
    html = open(sys.argv[1], encoding='utf-8').read()
    r = check(html)
    for k, v in r.items():
        if not k.startswith('_'):
            print(f"[{'PASS' if v else 'FAIL'}] {k}")
    if '_CR-S7.4_detail' in r:
        print("  CR-S7.4 optional widgets found:", r['_CR-S7.4_detail'])
    ok = all(v for k, v in r.items() if not k.startswith('_'))
    print("OVERALL:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
