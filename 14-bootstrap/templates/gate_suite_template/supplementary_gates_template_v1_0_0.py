#!/usr/bin/env python3
"""supplementary_gates_template.py — template for program 2 of the R21
four-program gate chain, generalized from semtech-landscape's own
semtech_supplementary_gates_vX_Y_0.py (which grew from 29 to 40 individual
gates purely by addition across roughly forty releases).

This template ships two READY-TO-USE gate patterns extracted directly from
real defects this byproduct found, plus the harness ('gate' helper,
'results'/'fails' bookkeeping, exit code) every other content-specific gate
in your own byproduct should be added to over time, one per release, the
same way semtech-landscape's own suite grew.

Fill in REPLACE_ME paths, then add your own byproduct-specific gates below
the two template ones using the same `gate(name, condition, detail)` call
shape.
"""
import sys

results = []


def gate(name, condition, detail=""):
    results.append((name, bool(condition)))
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}" + (f": {detail}" if detail else ""))


# ============================================================
# TEMPLATE GATE 1 — Pattern R18: completeness against the FULL expected
# set, never a hardcoded partial list that can silently stop growing.
#
# The real incident this generalizes: a documentation-completeness gate
# checked Annex-section presence against a hand-maintained list of
# expected headings; the list silently stopped being extended after one
# release, so the gate kept passing while checking fewer and fewer of the
# document's actual sections. The fix: derive the expected set from the
# SAME data structure the content itself was generated from, never from
# a second, independently-maintained copy of that list.
# ============================================================
def check_completeness_against_full_set(built_artifact_text, expected_items_source):
    """`expected_items_source` must be the SAME list/data structure the
    content generator itself iterated over to produce the artifact — not
    a separately hand-maintained list of what the checker author expects.
    Returns (all_present: bool, missing: list)."""
    missing = [item for item in expected_items_source if item not in built_artifact_text]
    return (len(missing) == 0, missing)


# Example wiring (uncomment and adapt):
# REPLACE_ME_built_doc_text = open("REPLACE_ME/built_document.txt").read()
# REPLACE_ME_expected_sections = REPLACE_ME_content_module.ALL_SECTIONS  # the generator's own source list, not a copy
# ok, missing = check_completeness_against_full_set(REPLACE_ME_built_doc_text, REPLACE_ME_expected_sections)
# gate("R18: document contains every section from the generator's own source list", ok,
#      f"{len(REPLACE_ME_expected_sections) - len(missing)}/{len(REPLACE_ME_expected_sections)} present" + (f"; missing: {missing}" if missing else ""))


# ============================================================
# TEMPLATE GATE 2 — Pattern R16: cross-artifact count agreement, computed
# directly from each artifact rather than trusted from one to the others.
# ============================================================
def check_cross_artifact_count(label, values_by_artifact):
    """`values_by_artifact` is a dict of {artifact_name: count}, each
    computed independently and directly from that artifact. Returns
    (agree: bool, values_by_artifact)."""
    distinct = set(values_by_artifact.values())
    return (len(distinct) <= 1, values_by_artifact)


# Example wiring (uncomment and adapt):
# tbox_count = REPLACE_ME_count_classes_in_tbox()
# docx_count = REPLACE_ME_count_headings_in_docx()
# page_count = REPLACE_ME_count_tree_nodes_in_page()
# ok, vals = check_cross_artifact_count("domain class count", {"tbox": tbox_count, "docx": docx_count, "page": page_count})
# gate("R16: domain class count agrees across TBox/document/page", ok, str(vals))


# ============================================================
# YOUR BYPRODUCT'S OWN CONTENT-SPECIFIC GATES GO HERE — add one per
# release, the same way semtech-landscape's own suite grew from 29 to 40.
# Each new instance/feature/content addition earns a gate verifying it
# directly against the built artifact, not just against the source data.
# ============================================================
# gate("G1 <describe what this release added>", <condition>, "<detail>")


fails = [r for r in results if not r[1]]
print(f"\nSUPPLEMENTARY: {len(results) - len(fails)}/{len(results)} PASS")
sys.exit(1 if fails else 0)
