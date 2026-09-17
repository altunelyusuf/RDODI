#!/usr/bin/env python3
"""healthcheck_template.py — byproduct-agnostic RDODI healthcheck, generalized
from the semtech-landscape byproduct's own v6.9.0 FG-EP27 healthcheck.

Implements two of the patterns proposed in the accompanying handover:

  R16 — cross-artifact numeric consistency must be re-derived from each
        artifact directly, never assumed from one artifact being correct.
  R17 — a stale local clone of a governed repository can manufacture false
        negative findings; fetch/pull before concluding published state is
        broken or missing.

USAGE
-----
Fill in the CONFIG block below for your byproduct's own file layout, then run:

    python3 healthcheck_template.py

It does NOT modify any file. It reports agreement or disagreement across
artifacts and exits non-zero if any disagreement is found, so it can be
wired into a CI job the same way the byproduct's own release-check chains
its four gate programs.

This file intentionally has no byproduct-specific paths hardcoded past the
CONFIG block, so it can be copied into a new byproduct's 06-gates/ (or
equivalent) directory and adapted by editing CONFIG only.
"""
import json
import re
import subprocess
import sys

# ============================================================
# CONFIG — fill in for your byproduct. Every path is relative to this
# script's own directory unless given absolute.
# ============================================================
CONFIG = {
    # Turtle files whose counts define ground truth for cross-checking.
    "tbox_path": "REPLACE_ME/domain_tbox.ttl",
    "abox_path": "REPLACE_ME/domain_abox.ttl",

    # The rendered Stage-3 document (.docx). Counts are derived from its
    # actual heading structure, not a stored table of contents.
    "docx_path": "REPLACE_ME/document.docx",

    # The rendered Stage-4 interactive page (.html). Its runtime data is
    # extracted via bracket-matching on a known JS variable assignment,
    # not regex-guessed — regex against nested braces is fragile.
    "page_path": "REPLACE_ME/page.html",
    "page_data_var": "const DATA = ",  # exact JS source text preceding the object

    # An optional compiled knowledge base (JSON) if your byproduct has one.
    "kb_path": None,  # e.g. "REPLACE_ME/agents_kb.json", or None to skip

    # The counts to reconcile across every artifact above that can supply
    # them. Each entry: (label, tbox_fn, abox_fn, docx_fn, page_fn, kb_fn).
    # A _fn may be None if that artifact cannot supply the count.
    "counts_to_check": [
        # Example (uncomment and adapt once tbox/abox loaders are wired):
        # ("domain classes", count_classes_tbox, None, count_sections_docx,
        #  count_tree_nodes_page, count_classes_kb),
    ],

    # Governed monorepo git root to freshness-check (R17). Set to None to skip.
    "governed_repo_root": None,  # e.g. "/home/claude/Ontologies"
}


# ============================================================
# R17 — git freshness check
# ============================================================
def check_git_freshness(repo_root):
    """Returns (is_fresh: bool, detail: str). Does not modify the repo;
    only inspects HEAD age and offers the fetch command to run if stale.
    A byproduct's CI should actually run the fetch before trusting any
    'commit missing' finding from this repo, per Pattern R17."""
    if repo_root is None:
        return True, "no governed_repo_root configured — freshness check skipped"
    try:
        head = subprocess.run(["git", "log", "-1", "--format=%ci"], cwd=repo_root,
                               capture_output=True, text=True, check=True).stdout.strip()
        branch_status = subprocess.run(["git", "status", "-sb"], cwd=repo_root,
                                        capture_output=True, text=True, check=True).stdout.strip()
        ahead_behind = "[behind" in branch_status or "[ahead" in branch_status
        detail = f"local HEAD committed at {head}; branch status: {branch_status.splitlines()[0] if branch_status else '?'}"
        if ahead_behind:
            return False, detail + " — local clone is NOT current; run `git pull` before trusting any commit-existence check against this repo (Pattern R17)"
        return True, detail
    except Exception as e:
        return False, f"could not inspect {repo_root}: {e} — treat any commit-existence check against it as unverified until this is resolved"


# ============================================================
# R16 — cross-artifact count reconciliation
# ============================================================
def extract_docx_headings(docx_path):
    """Returns the list of heading paragraph texts, using python-docx.
    Import is local so this file has no hard dependency if DOCX checks
    are unused for a given byproduct."""
    import docx
    d = docx.Document(docx_path)
    return [p.text for p in d.paragraphs if p.style.name.startswith("Heading")]


def extract_page_data_object(page_path, marker):
    """Bracket-matches the JS object literal following `marker` in the
    page's inline script, rather than regex-guessing its extent — nested
    braces inside string values make a naive regex unreliable."""
    html = open(page_path, encoding="utf-8").read()
    start = html.index(marker) + len(marker)
    depth = 0
    started = False
    end = start
    for i in range(start, len(html)):
        c = html[i]
        if c == "{":
            depth += 1
            started = True
        elif c == "}":
            depth -= 1
            if started and depth == 0:
                end = i + 1
                break
    return json.loads(html[start:end])


def reconcile_counts(config):
    """Runs every configured count check across every artifact that can
    supply it, and reports agreement/disagreement. Returns True if every
    check that ran agreed across all artifacts that supplied it."""
    all_ok = True
    for label, tbox_fn, abox_fn, docx_fn, page_fn, kb_fn in config["counts_to_check"]:
        values = {}
        for name, fn, path_key in [
            ("tbox", tbox_fn, "tbox_path"), ("abox", abox_fn, "abox_path"),
            ("docx", docx_fn, "docx_path"), ("page", page_fn, "page_path"),
            ("kb", kb_fn, "kb_path"),
        ]:
            if fn is None:
                continue
            path = config.get(path_key)
            if not path:
                continue
            try:
                values[name] = fn(path)
            except Exception as e:
                values[name] = f"ERROR: {e}"
        distinct = set(v for v in values.values() if not isinstance(v, str))
        ok = len(distinct) <= 1
        all_ok = all_ok and ok
        print(f"[{'OK' if ok else 'MISMATCH'}] {label}: {values}")
    return all_ok


def main():
    print("=== R17: governed-repo freshness ===")
    fresh, detail = check_git_freshness(CONFIG["governed_repo_root"])
    print(f"[{'OK' if fresh else 'STALE'}] {detail}")

    print("\n=== R16: cross-artifact count reconciliation ===")
    if not CONFIG["counts_to_check"]:
        print("no counts configured — fill in CONFIG['counts_to_check'] for this byproduct")
        counts_ok = True
    else:
        counts_ok = reconcile_counts(CONFIG)

    print(f"\nVERDICT: {'PASS' if (fresh and counts_ok) else 'ATTENTION NEEDED'}")
    sys.exit(0 if (fresh and counts_ok) else 1)


if __name__ == "__main__":
    main()
