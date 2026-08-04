"""
RDODI Validation Orchestrator v1.0.0  (Instrument 5 + glue)
Runs the mechanical verifiers, then emits ONE validation sheet for the human containing ONLY judgment items.

The human reads the validation sheet, not the document: they confirm sources support claims and that the
document intent is right. Everything mechanical (insertions landed, no regression, numbers reconcile,
references exist + reconcile) is asserted automatically and reported as a pass/fail floor.
"""
import sys, os, json
sys.path.insert(0, ".")
from rdodi_verification_lib_v1_0_0 import (verify_insertions, verify_no_regression,
                                           retention_vector, reconcile_numbers, count_exact)
from rdodi_reference_auditor_v1_0_0 import audit, reconcile_citations

def run(text, *, prior_text=None, concept_checklist=None, expected_insertions=None,
        claimed_numbers=None, rederivations=None, references=None, intent=None, do_live_refs=False):
    """
    Returns {mechanical_floor: {...pass/fail...}, validation_sheet: {...judgment only...}}.
    Mechanical items are decided here. Judgment items are SURFACED, never decided.
    """
    concept_checklist = concept_checklist or []
    report = {"mechanical_floor": {}, "validation_sheet": {}}

    # --- MECHANICAL FLOOR (offloaded from human) ---
    if expected_insertions:
        report["mechanical_floor"]["insertions"] = verify_insertions(text, expected_insertions)
    if prior_text is not None:
        report["mechanical_floor"]["regression"] = verify_no_regression(
            prior_text, text, concept_checklist, allow_cut=False)
    if claimed_numbers and rederivations:
        report["mechanical_floor"]["numbers"] = reconcile_numbers(text, claimed_numbers, rederivations)
    report["mechanical_floor"]["citation_reconciliation"] = reconcile_citations(text)
    report["mechanical_floor"]["retention"] = retention_vector(text, concept_checklist)

    # overall mechanical pass
    floor = report["mechanical_floor"]
    passes = []
    if "insertions" in floor: passes.append(floor["insertions"]["all_present"])
    if "regression" in floor: passes.append(not floor["regression"]["regression"])
    if "numbers" in floor: passes.append(floor["numbers"]["all_reconcile"])
    passes.append(floor["citation_reconciliation"]["reconciles"])
    report["mechanical_floor"]["ALL_PASS"] = all(passes)

    # --- VALIDATION SHEET (judgment only — for the human) ---
    sheet = {"document_intent": intent or "(intent not declared — human must confirm what this artifact is for)",
             "warrant_items": [], "references_needing_human_attention": []}
    if references:
        a = audit(text, references) if do_live_refs else None
        if a:
            sheet["warrant_items"] = a["warrant_sheet"]
            sheet["references_needing_human_attention"] = a["mechanical"]["needs_attention"]
        else:
            # offline: still surface the warrant questions from the supplied claims
            sheet["warrant_items"] = [
                {"citation": f"{r.get('author','?')} {r.get('year','?')}",
                 "claim": r.get("claim","(claim not supplied)"),
                 "human_must_confirm": "Does this source support the claim?"} for r in references]
    report["validation_sheet"] = sheet
    return report

def render_sheet(report):
    """Human-readable one-page validation sheet."""
    floor = report["mechanical_floor"]; sheet = report["validation_sheet"]
    L = []
    L.append("=" * 64)
    L.append("MECHANICAL FLOOR (verified automatically — human need not re-check)")
    L.append("=" * 64)
    L.append(f"  ALL MECHANICAL CHECKS PASS: {floor.get('ALL_PASS')}")
    if "insertions" in floor:
        L.append(f"  insertions landed: {floor['insertions']['all_present']}")
    if "regression" in floor:
        r = floor["regression"]
        L.append(f"  no regression: {not r['regression']}" +
                 (f"  DROPS={list(r['drops'].keys())}" if r["regression"] else ""))
    if "numbers" in floor:
        L.append(f"  numbers reconcile: {floor['numbers']['all_reconcile']}")
    cr = floor["citation_reconciliation"]
    L.append(f"  citations reconcile: {cr['reconciles']} ({cr['cited_count']} cited)" +
             (f"  ORPHANS={cr['orphans']}" if cr["orphans"] else ""))
    ret = floor["retention"]
    L.append(f"  retention: {ret['inline_citations']} cites, {ret['reference_entries']} refs, "
             f"{ret['sections']} sections, concepts {ret['concepts_present_count']}/{len(ret['concepts_present'])}")
    L.append("")
    L.append("=" * 64)
    L.append("VALIDATION SHEET (JUDGMENT — only the human can decide these)")
    L.append("=" * 64)
    L.append(f"  DOCUMENT INTENT: {sheet['document_intent']}")
    if sheet["references_needing_human_attention"]:
        L.append("  REFERENCES NEEDING ATTENTION (Indirect/unresolved tier):")
        for r in sheet["references_needing_human_attention"]:
            L.append(f"    - {r.get('author')} {r.get('year')}: tier={r.get('tier')} "
                     f"points to '{r.get('points_to_title')}'")
    L.append("  WARRANT — confirm each source supports its claim:")
    for w in sheet["warrant_items"]:
        L.append(f"    [ ] {w['citation']}: {w.get('claim','')}")
    return "\n".join(L)

if __name__ == "__main__":
    worked_md = os.environ.get("RDODI_WORKED_EXAMPLE_MD", "")
    if not worked_md or not os.path.exists(worked_md):
        print("  SKIP: no worked-example markdown provided (set RDODI_WORKED_EXAMPLE_MD)"); return True
    t = open(worked_md).read()
    import re
    rep = run(t,
              concept_checklist=["Taylor","Shewhart","Deming","Six Sigma","verification","validation",
                                 "configuration management","DMAIC"],
              claimed_numbers={"citations": 17},
              rederivations={"citations": lambda x: len(re.findall(
                  r"\([A-Z][A-Za-z .&]+,?\s*\n?\d{4}\)", x.split("## References")[0]))},
              references=[{"author":"Taylor","year":"1911","title":"The Principles of Scientific Management",
                           "claim":"Taylor separated planning from doing"}],
              intent="Teaching companion for an IT Project Management course (book Chapter 10).",
              do_live_refs=False)
    print(render_sheet(rep))
