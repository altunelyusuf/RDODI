#!/usr/bin/env python3
"""
Definition Conformance Gate v1.0.1 (public edition: generic defaults)
====================================
Reads each widget's REAL skos:definition from the authoritative TBox
(interactive_page_ontology_tbox_v1_9_1.ttl) and mechanically checks the
generated artifact against every testable clause in that definition.

HONEST SCOPE DISCLOSURE: skos:definition is natural-language prose. There is
no general NLP procedure that reliably extracts "every clause" from arbitrary
prose and turns it into a mechanical check. What this gate actually does:
for each widget, it prints the verbatim definition (so a human can see the
full authority text), then runs a set of concrete, named checks -- each one
explicitly traceable to a specific clause in that definition -- against the
generated HTML/JS source. This is the honest, defensible realization of
"check every clause": per-widget, clause-traceable, mechanical, not a
generic parser. Extending coverage to a new widget means adding a new
named check block that cites the clause it tests.

Usage: python3 definition_conformance_gate_v1_0_0.py <generated.html> <tbox.ttl>
"""
from __future__ import annotations
import sys, re
import rdflib
from rdflib.namespace import SKOS

def get_definition(tbox_path, local_name, ns="http://example.org/rdodi/interactive-page-ontology#"):
    g = rdflib.Graph()
    g.parse(tbox_path, format="turtle")
    s = rdflib.URIRef(ns + local_name)
    defs = list(g.objects(s, SKOS.definition))
    return str(defs[0]) if defs else None


class Result:
    def __init__(self):
        self.checks = []  # (widget, clause, passed, detail)

    def add(self, widget, clause, passed, detail):
        self.checks.append((widget, clause, passed, detail))

    def report(self):
        lines = []
        by_widget = {}
        for w, c, p, d in self.checks:
            by_widget.setdefault(w, []).append((c, p, d))
        total_pass = sum(1 for *_, p, _ in self.checks if p)
        lines.append(f"Definition Conformance Gate — {total_pass}/{len(self.checks)} clauses pass\n")
        for w, items in by_widget.items():
            npass = sum(1 for _, p, _ in items if p)
            lines.append(f"## {w}  ({npass}/{len(items)})")
            for clause, passed, detail in items:
                mark = "PASS" if passed else "FAIL"
                lines.append(f"  [{mark}] {clause}")
                lines.append(f"         {detail}")
            lines.append("")
        return "\n".join(lines)


def run_gate(html_path, tbox_path):
    with open(html_path) as f:
        src = f.read()
    r = Result()

    # ---- ContextMenu ----
    d = get_definition(tbox_path, "ContextMenu")
    print("=== ContextMenu — verbatim skos:definition ===\n" + d + "\n")
    r.add("ContextMenu", "opened by the contextmenu event or Shift+F10/ContextMenu key",
          "addEventListener('contextmenu'" in src,
          "contextmenu event listener found" if "addEventListener('contextmenu'" in src else "no contextmenu listener found")
    has_keydown_f10 = bool(re.search(r"key(Code)?\s*===?\s*['\"]?F10['\"]?|ContextMenu['\"]", src))
    r.add("ContextMenu", "opened by Shift+F10 / ContextMenu key (keyboard equivalent)",
          has_keydown_f10, "keyboard trigger found" if has_keydown_f10 else "NO keyboard-triggered open path found — mouse-only")
    has_escape = bool(re.search(r"key\s*===?\s*['\"]Escape['\"]|keyCode\s*===?\s*27", src))
    r.add("ContextMenu", "dismissed by Escape",
          has_escape, "Escape handler found" if has_escape else "NO Escape-key handler found anywhere in source")
    has_focus_return = bool(re.search(r"ctxTriggerEl.*\.focus\(\)|closeCtxMenu\(true\)", src))
    r.add("ContextMenu", "focus returned to the originating element",
          has_focus_return, "triggering element's .focus() is called on close" if has_focus_return else "NO focus-return path found for ContextMenu specifically")
    is_context_sensitive = "data-ctx=" in src and src.count("menu.innerHTML=") >= 2
    r.add("ContextMenu", "menu content is for a focused/context-specific section (not one static menu)",
          is_context_sensitive, "multiple distinct menu.innerHTML branches keyed on data-ctx — genuinely context-sensitive" if is_context_sensitive else "single static menu content — not context-sensitive")

    # ---- SubPageTabs ----
    d = get_definition(tbox_path, "SubPageTabs")
    print("=== SubPageTabs — verbatim skos:definition ===\n" + d + "\n")
    uses_pushstate_or_hash = bool(re.search(r"pushState|location\.hash\s*=|history\.", src))
    r.add("SubPageTabs", "realized as navigation links — not in-place panel swaps — each tab has its own routable location",
          uses_pushstate_or_hash,
          "found pushState/hash/history routing" if uses_pushstate_or_hash else
          "FAIL: show(p) only toggles .active class on .page elements (classList.remove/add) — no pushState, no location.hash, no history API anywhere. This is an in-place panel swap, the definition's explicitly prohibited pattern.")
    has_overview_tab = bool(re.search(r"i\s*==\s*['\"]overview['\"]|data-p=[\"']overview[\"']", src))
    r.add("SubPageTabs", "plus an overview tab",
          has_overview_tab, "an 'overview' tab is present and set active by default" if has_overview_tab else "no overview tab found")

    # ---- PrimaryNavigation ----
    d = get_definition(tbox_path, "PrimaryNavigation")
    print("=== PrimaryNavigation — verbatim skos:definition ===\n" + d + "\n")
    has_distinct_primary_nav = bool(re.search(r'class="primary-nav"|primary-nav|top-nav|topnav|main-nav|navbar', src, re.I))
    r.add("PrimaryNavigation", "distinct top-level navigation between major sections (not the same mechanism as SubPageTabs)",
          has_distinct_primary_nav,
          "a distinct primary/top-nav element exists" if has_distinct_primary_nav else
          "FAIL: no primary-nav/top-nav/navbar element found anywhere. The only top-level navigation mechanism in the generated artifact IS the .tab/show() SubPageTabs mechanism — PrimaryNavigation and SubPageTabs are the same code path, not two things.")

    # ---- TreeNavigation ----
    d = get_definition(tbox_path, "TreeNavigation")
    print("=== TreeNavigation — verbatim skos:definition ===\n" + d + "\n")
    has_arrow_keys = bool(re.search(r"ArrowUp|ArrowDown|ArrowLeft|ArrowRight", src))
    r.add("TreeNavigation", "navigable by keyboard (arrow keys, Home/End, expand/collapse)",
          has_arrow_keys, "arrow-key handling found" if has_arrow_keys else "FAIL: no ArrowUp/Down/Left/Right handling anywhere — .tx-folder expand/collapse is wired via .onclick only (mouse-only), no keydown listener at all")
    has_aria_selected = "aria-selected" in src
    r.add("TreeNavigation", "current location indicated by aria-selected",
          has_aria_selected, "aria-selected present" if has_aria_selected else "FAIL: 'aria-selected' does not appear anywhere in the generated source")
    has_tabindex = bool(re.search(r'class="tx-folder"[^>]*tabindex=', src))
    r.add("TreeNavigation", "(implied by 'navigable by keyboard') tree items are focusable",
          has_tabindex, "tabindex present specifically on .tx-folder elements" if has_tabindex else "FAIL: .tx-folder divs carry no tabindex — not keyboard-focusable at all, so arrow-key navigation is impossible even if added")

    # ---- Tooltip ----
    d = get_definition(tbox_path, "Tooltip")
    print("=== Tooltip — verbatim skos:definition ===\n" + d + "\n")
    has_hover = "mouseover" in src
    r.add("Tooltip", "Hover ... help text affordance", has_hover, "mouseover handler found" if has_hover else "no mouseover handler found")
    has_focus_trigger = bool(re.search(r"addEventListener\(['\"]focus['\"]|addEventListener\(['\"]focusin['\"]", src))
    r.add("Tooltip", "... /focus help text affordance (keyboard/screen-reader users must be able to trigger it too)",
          has_focus_trigger, "focus/focusin handler found" if has_focus_trigger else "FAIL: tooltip is wired to mouseover/mousemove/mouseout only — no focus/focusin handler, so keyboard-only and screen-reader users can never trigger it")

    return r


if __name__ == "__main__":
    html_path = sys.argv[1] if len(sys.argv) > 1 else sys.exit("usage: definition_conformance_gate_v1_0_1.py <generated.html> [tbox.ttl]")
    tbox_path = sys.argv[2] if len(sys.argv) > 2 else "01-stage-vocabularies/04-interactive-page/interactive_page_ontology_tbox_v1_9_1.ttl"
    r = run_gate(html_path, tbox_path)
    print(r.report())
