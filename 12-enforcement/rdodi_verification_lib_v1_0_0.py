"""
RDODI Verification Library v1.0.0
Removes mechanical verification from the human. Reusable across domains.

Instruments:
  4. exact-match substrate      (normalise + exact token/phrase matching; fuzzy only proposes)
  1. insertion/retention verifier (edit landed? retention vector preserved?)
  3. number/count reconciler     (re-derive every claimed number from the artifact)

Design rule: a result is trusted only because it was re-derived from the actual artifact this run,
never because it was asserted. Fuzzy matching may PROPOSE candidates but an exact check must CONFIRM.
"""
import re, unicodedata

# ---------------------------------------------------------------- Instrument 4: exact-match substrate
def normalise(s: str) -> str:
    """Canonical form for exact comparison: unicode-fold, lowercase, collapse whitespace, strip md emphasis."""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("*", "").replace("_", "")            # markdown emphasis is not content
    s = re.sub(r"\s+", " ", s)                          # collapse wraps/newlines
    return s.strip().lower()

def contains_exact(haystack: str, needle: str) -> bool:
    """True iff needle appears in haystack as a normalised substring (wrap-safe, emphasis-safe)."""
    return normalise(needle) in normalise(haystack)

def count_exact(haystack: str, needle: str) -> int:
    h, n = normalise(haystack), normalise(needle)
    return h.count(n) if n else 0

def token_set(s: str) -> set:
    return set(re.findall(r"[a-z0-9]+", normalise(s)))

def fuzzy_propose(haystack_terms, needle, min_overlap=0.6):
    """Fuzzy CANDIDATE generator only. Returns candidates; caller must confirm with an exact check."""
    nt = token_set(needle)
    if not nt: return []
    out = []
    for term in haystack_terms:
        tt = token_set(term)
        if tt and len(nt & tt) >= max(1, len(nt) * min_overlap):
            out.append(term)
    return out

# ---------------------------------------------------------------- Instrument 1: insertion/retention
def verify_insertions(text: str, expected_insertions: dict) -> dict:
    """
    expected_insertions: {label: (phrase, expected_min_count)}
    Confirms each intended insertion is actually present >= expected_min_count times.
    """
    results, ok = {}, True
    for label, (phrase, want) in expected_insertions.items():
        got = count_exact(text, phrase)
        passed = got >= want
        ok = ok and passed
        results[label] = {"want>=": want, "got": got, "pass": passed}
    return {"all_present": ok, "detail": results}

def retention_vector(text: str, concept_checklist) -> dict:
    """Fixed mechanical retention metrics, re-derived from the artifact itself."""
    body = text.split("## References")[0] if "## References" in text else text
    return {
        "inline_citations": len(re.findall(r"\([A-Z][A-Za-z .&]+,?\s*\d{4}\)", body)) +
                             len(re.findall(r"\[\d+\]", body)),
        "reference_entries": (len(re.findall(r"(?m)^\[\d+\]", text)) +
                              len(re.findall(r"(?m)^[A-Z][A-Za-z'-]+,? .*\(\d{4}\)", text))),
        "sections": len(re.findall(r"(?m)^##\s", text)),
        "tables": text.count("|---") + text.count("| ---"),
        "figures": len(re.findall(r"!\[", text)),
        "concepts_present": {c: contains_exact(text, c) for c in concept_checklist},
        "concepts_present_count": sum(1 for c in concept_checklist if contains_exact(text, c)),
        "words": len(body.split()),
    }

def verify_no_regression(old_text, new_text, concept_checklist, allow_cut=False) -> dict:
    """Fail if any retention metric dropped without an explicit instruction to cut (F90 guard)."""
    old, new = retention_vector(old_text, concept_checklist), retention_vector(new_text, concept_checklist)
    drops = {}
    for k in ["inline_citations", "reference_entries", "sections", "tables", "figures",
              "concepts_present_count"]:
        if new[k] < old[k]:
            drops[k] = {"old": old[k], "new": new[k]}
    lost = [c for c in concept_checklist if old["concepts_present"][c] and not new["concepts_present"][c]]
    if lost: drops["lost_concepts"] = lost
    return {"regression": (bool(drops) and not allow_cut), "drops": drops,
            "old": old, "new": new, "allow_cut": allow_cut}

# ---------------------------------------------------------------- Instrument 3: number/count reconciler
def reconcile_numbers(text: str, claimed: dict, rederive: dict) -> dict:
    """
    claimed:  {label: number the document/report STATES}
    rederive: {label: callable(text)->number that INDEPENDENTLY recomputes it from the artifact}
    A number is trusted only if claimed == re-derived.
    """
    results, ok = {}, True
    for label, claim in claimed.items():
        if label not in rederive:
            results[label] = {"claimed": claim, "rederived": None, "pass": None,
                              "note": "no re-derivation supplied"}
            continue
        actual = rederive[label](text)
        passed = (claim == actual)
        ok = ok and passed
        results[label] = {"claimed": claim, "rederived": actual, "pass": passed}
    return {"all_reconcile": ok, "detail": results}

if __name__ == "__main__":
    # self-test on a tiny sample
    doc = "Quality is **fitness** for use (Deming, 1986). See section.\n## References\nDeming, W. E. (1986)."
    print("contains_exact (wrap/emphasis safe):", contains_exact(doc, "fitness for use"))
    print("retention:", retention_vector(doc, ["fitness for use", "grade"]))
    ins = verify_insertions(doc, {"deming_cite": ("(Deming, 1986)", 1), "missing": ("Taguchi", 1)})
    print("insertions:", ins["all_present"], ins["detail"])
    rec = reconcile_numbers(doc, {"citations": 1},
                            {"citations": lambda t: len(re.findall(r"\(\w+, \d{4}\)", t.split('## References')[0]))})
    print("reconcile:", rec)
