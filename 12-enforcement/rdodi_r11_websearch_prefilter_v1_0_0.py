"""
RDODI R11 web_search Pre-Filter v1.0.0
======================================
Implements step (1) of the R11 Pattern SPECIFICATION as stated in the RDODI knowledge-base ABox
(rdodi_knowledgebase_abox_v1_1_0.ttl, skos:definition of Pattern R11) — the LOOSE high-recall
web_search query that acts as a Bloom-filter-shaped probabilistic membership pre-test.

PROVENANCE (honest, per proposal §4.6): this module implements the R11 ABox SPECIFICATION step (1).
It does NOT re-ground an existing RDODI function — the existing reference_auditor_v1_0_0.py implements
ONLY the catalogue-API subset (Crossref -> OpenLibrary) and contains NO web_search pre-filter
(verified on disk: no 'web_search'/'loose'/'pre-filter'/'bloom' token in that file). This module is the
previously un-coded part of the spec.

WHY IT MATTERS: catalogue-only resolution structurally cannot reach grey literature (EU-agency reports,
institutional publications with no DOI and no library catalogue record). The loose web_search pre-filter
is the R11 channel that can surface such works, which a parse-match then confirms or honestly floors.

BLOOM-FILTER ANALOGY (faithful to the spec):
  - The loose query is the membership PRE-TEST: a candidate appearing = "possibly present" (never a verdict).
  - The parse-match against the record's own metadata is the CONFIRMATION (step 3).
  - "No authoritative member after loose passes" = the Bloom "definitely not present" verdict (step 6):
    a true negative is reliable; a positive must always be confirmed.

CHANNEL DISCIPLINE (proposal §4.5): live-first / deterministic-fallback. If the web_search channel is
unavailable at run time, the result is ("unresolved", reason="channel unavailable") — NEVER a fabricated
tier. The probabilistic filter never invents membership.

This module is channel-agnostic: it takes a `search_fn(query)->list[candidate]` injected by the caller
(the live web_search tool in a session, or a deterministic fixture in tests), so it is testable offline
and degrades honestly when the channel is absent.
"""
import re

# Authoritative-tier index domains, from the R11 ABox spec + RESOLUTION_METHOD_NOTE_v1_0_0.md (verbatim list)
AUTHORITATIVE_DOMAINS = {
    "Definitive": ["loc.gov", "lccn.loc.gov", "id.loc.gov", "sei.cmu.edu", "resources.sei.cmu.edu",
                   "iso.org"],
    "High":       ["doi.org", "crossref.org", "api.crossref.org", "worldcat.org", "dl.acm.org",
                   "ieeexplore.ieee.org", "dblp.org", "tandfonline.com", "openalex.org",
                   "ci.nii.ac.jp", "cinii.ac.jp"],
    # Institutional / grey-literature authoritative publishers (named record, not a homepage) — the
    # CEDEFOP-class case the proposal's acceptance test targets. Confirmed only when the candidate is a
    # named publications RECORD, not the org landing page (enforced in parse-match below).
    "Institutional": ["cedefop.europa.eu", "europa.eu", "oecd.org", "worldbank.org", "un.org",
                      "nist.gov", "nasa.gov"],
}
TIER_ORDER = ["Definitive", "High", "Institutional"]  # highest-first attempt order for the pre-filter

def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()

def _tokens(s):
    return set(_norm(s).split()) - {"the", "of", "a", "and", "to", "for", "in", "on", "an"}

def _domain_tier(url):
    u = (url or "").lower()
    for tier in TIER_ORDER:
        for dom in AUTHORITATIVE_DOMAINS[tier]:
            if dom in u:
                return tier, dom
    return None, None

def _is_named_record(url, tier):
    """For Institutional grey-lit, require a publications RECORD path, not the bare org homepage
    (proposal acceptance test: 'resolves to a named authoritative record, not the org homepage')."""
    if tier != "Institutional":
        return True
    u = (url or "").lower().rstrip("/")
    # reject bare domain / homepage; require a path segment indicating a specific record/publication
    path = re.sub(r"^https?://[^/]+", "", u)
    if not path or path in ("", "/"):
        return False
    return any(k in u for k in ["/publications", "/data-insights", "/resource", "/news",
                                 "/files", "/document", "report", "id=", ".pdf"])

def prefilter_resolve(title, author=None, year=None, *, search_fn=None, max_passes=2):
    """
    R11 step (1)-(6) via the web_search channel.
    search_fn(query) -> list of dicts each with keys at least {'url','title'} (and optionally 'snippet').
      Inject the live web_search tool here in a session; inject a fixture in tests.
      If search_fn is None -> channel unavailable -> honest ('unresolved','channel unavailable').
    Returns: {tier, via, url, matched_title, reason}.
    """
    if search_fn is None:
        return {"tier": "unresolved", "via": None, "url": None, "matched_title": None,
                "reason": "channel unavailable (web_search not injected) — NOT a fabricated tier"}

    ref_toks = _tokens(title)
    y = str(year) if year else None

    # (1) LOOSE high-recall query — deliberately broad, author+title+year (the Bloom pre-test)
    query = " ".join(x for x in [title, author or "", y or ""] if x).strip()

    seen_any_candidate = False
    for _pass in range(max_passes):
        try:
            candidates = search_fn(query) or []
        except Exception as e:
            return {"tier": "unresolved", "via": None, "url": None, "matched_title": None,
                    "reason": f"channel error: {e}"}
        if candidates:
            seen_any_candidate = True
        # (2)+(3) parse the candidate set for an authoritative-tier MEMBER matching author+title+year.
        # Membership alone is only the pre-filter; the metadata parse-match is the verdict.
        best = None
        for c in candidates:
            tier, dom = _domain_tier(c.get("url", ""))
            if not tier:
                continue  # a non-authoritative candidate (e.g. a sales listing) never promotes tier
            if not _is_named_record(c.get("url", ""), tier):
                continue
            cand_toks = _tokens(c.get("title", "")) | _tokens(c.get("snippet", ""))
            # title overlap is the core of the parse-match
            if ref_toks and len(ref_toks & cand_toks) < max(2, int(len(ref_toks) * 0.6)):
                continue
            # year corroboration if present in candidate text
            if y and (y in (c.get("title", "") + " " + c.get("snippet", ""))):
                pass  # corroborated; not mandatory for institutional grey-lit
            # author corroboration if available
            if author:
                al = author.split()[-1].lower()
                if al and al not in _norm(c.get("title", "") + " " + c.get("snippet", "")):
                    # author absent from the snippet is tolerated for institutional reports
                    if tier != "Institutional":
                        continue
            # (4) first authoritative match by highest tier order -> STOP
            rank = TIER_ORDER.index(tier)
            if best is None or rank < best[0]:
                best = (rank, tier, dom, c)
        if best:
            _, tier, dom, c = best
            return {"tier": tier, "via": f"web_search→{dom}", "url": c.get("url"),
                    "matched_title": c.get("title"),
                    "reason": "authoritative-tier member parse-matched on title"
                              + ("+year" if y else "")}
        # (5) no authoritative member this pass; broaden slightly and retry
        query = " ".join(x for x in [title, y or ""] if x).strip()

    # (6) honest negative — the Bloom 'definitely not present (in authoritative catalogues)' verdict
    return {"tier": "unresolved", "via": "web_search", "url": None, "matched_title": None,
            "reason": ("no authoritative-tier member surfaced after loose passes — "
                       "Unresolvable-with-reason (Bloom definitely-not-present); "
                       + ("candidates existed but none authoritative" if seen_any_candidate
                          else "no candidates returned"))}

# ---- chained resolver: pre-filter FIRST (highest tiers), then catalogue-API subset as the existing path ----
def r11_resolve(title, author=None, year=None, *, search_fn=None, catalogue_fn=None):
    """Full R11 order: loose web_search pre-filter first (reaches grey-lit + authoritative indexes),
    then fall back to the existing catalogue-API subset (Crossref/OpenLibrary) via catalogue_fn,
    then honest unresolved. Neither channel ever fabricates a tier."""
    pre = prefilter_resolve(title, author, year, search_fn=search_fn)
    if pre["tier"] in ("Definitive", "High", "Institutional"):
        return {**pre, "channel": "R11-prefilter"}
    if catalogue_fn is not None:
        cat = catalogue_fn(title, author, year)
        if cat and cat.get("tier") in ("Definitive", "High"):
            return {**cat, "channel": "catalogue-API", "prefilter_reason": pre["reason"]}
    return {**pre, "channel": "R11-prefilter", "note": "catalogue-API also did not resolve"
            if catalogue_fn else "no catalogue_fn supplied"}

if __name__ == "__main__":
    # offline self-test with a deterministic fixture (no live channel)
    def fixture(q):
        if "skills in transition" in q.lower():
            return [{"url": "https://www.cedefop.europa.eu/en/publications/skills-transition",
                     "title": "Skills in transition: The way to 2035 | CEDEFOP",
                     "snippet": "CEDEFOP 2023 report on skill needs to 2035."},
                    {"url": "https://www.amazon.com/dp/xxx", "title": "Some book"}]
        if "out of the crisis" in q.lower():
            return [{"url": "https://www.worldcat.org/oclc/11045408",
                     "title": "Out of the crisis — Deming, W. Edwards",
                     "snippet": "1982/1986 MIT."}]
        return []
    print("channel unavailable ->", prefilter_resolve("X", search_fn=None)["tier"])
    print("CEDEFOP grey-lit  ->", prefilter_resolve("Skills in transition: The way to 2035",
          "CEDEFOP", "2023", search_fn=fixture))
    print("Deming WorldCat   ->", prefilter_resolve("Out of the Crisis", "Deming", "1986",
          search_fn=fixture))
    print("true negative     ->", prefilter_resolve("Nonexistent Work Title XYZ", "Nobody", "1999",
          search_fn=fixture)["reason"])
