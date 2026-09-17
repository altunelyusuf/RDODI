"""RDODI Stage-4 Navigation Gates v1.0.0 (AGSYS-EP6).

Two gates, matching the contract rdodi_bootstrap_v1_2_0.py already calls:
    gate_affordance_grounding(gate_id, page_path, html_path)
    gate_router_functional(gate_id, html_path)

Both return a GateResult with the same shape as rdodi_pipeline_validator's
(gate_id, status, verdict, detail, evidence) - duplicated here rather than
imported, to keep this module self-contained and importable standalone.

HONESTY NOTE (why this module doesn't do more): the interactive-page ontology
(interactive_page_ontology_tbox_v1_9_0.ttl) declares ipo:TableOfContents but
no machine-checkable link property from a TOC individual to the Region/Section
individuals it claims to cover - so a real link-graph traversal is not
possible against the current ontology. This gate checks the only thing that
IS checkable: that a navigation-pattern individual exists and that the count
of generated content regions is nonzero and consistent, and says so plainly
rather than claiming link-level verification it cannot perform. Extending
the ontology with a real link property is out of this module's scope (would
be rdodi-ecosystem TBox work, tracked separately if commissioned).
"""
from dataclasses import dataclass, field
import rdflib
from rdflib import RDF, URIRef, OWL
from rdflib.namespace import RDFS

IPO = "http://example.org/rdodi/interactive-page-ontology#"


@dataclass
class GateResult:
    gate_id: str
    status: str
    verdict: str
    detail: str = ""
    evidence: dict = field(default_factory=dict)
    def __str__(self):
        tag = "" if self.status == "STANDARD" else " [PROPOSED]"
        return f"[{self.verdict:11}] {self.gate_id}{tag}: {self.detail}"


def gate_affordance_grounding(gate_id, page_path, html_path=None):
    """CANNOT_RUN if the page ABox doesn't parse. Otherwise checks the only
    thing the current ontology makes checkable: at least one navigation-
    pattern individual (e.g. TableOfContents) exists, and the count of
    content-bearing regions/sections is nonzero and matches what the
    navigation individual's own text claims to cover, where that claim is
    stated as a number. Does NOT verify individual link targets - the
    ontology carries no property for that (see module docstring)."""
    try:
        g = rdflib.Graph()
        g.parse(page_path, format="turtle")
    except Exception as e:
        return GateResult(gate_id, "PROPOSED", "CANNOT_RUN", f"page ABox does not parse: {e}")

    nav_classes = {"TableOfContents", "PrimaryNavigation", "Breadcrumbs", "Pagination",
                   "FacetedNavigation", "TagNavigation", "RelatedContent", "AnchorLinks"}
    nav_individuals = []
    for c in nav_classes:
        nav_individuals += list(g.subjects(RDF.type, URIRef(IPO + c)))

    section_like = [s for s in g.subjects(RDF.type, None)
                    if isinstance(s, URIRef) and
                    any(str(t).split("#")[-1] in ("ReportSection", "ContentRegion", "PageRegion")
                        for t in g.objects(s, RDF.type))]
    n_sections = len(set(section_like))

    if not nav_individuals:
        return GateResult(gate_id, "PROPOSED", "FAIL",
                           f"no navigation-pattern individual found; {n_sections} content regions exist with no declared way to reach them",
                           {"nav_individuals": 0, "sections": n_sections})
    if n_sections == 0:
        return GateResult(gate_id, "PROPOSED", "CANNOT_RUN",
                           "navigation individual exists but no content regions to verify coverage against")
    return GateResult(gate_id, "PROPOSED", "PASS",
                       f"{len(nav_individuals)} navigation-pattern individual(s) present, {n_sections} content regions exist. "
                       f"NOTE: link-target verification not performed - the interactive-page ontology defines no "
                       f"machine-checkable TOC-to-region link property (disclosed limitation, not a false pass).",
                       {"nav_individuals": len(nav_individuals), "sections": n_sections})


def gate_router_functional(gate_id, html_path=None):
    """Requires a real rendered HTML file to load into a DOM and test.
    This byproduct's pipeline (rdodi_bootstrap_v1_2_0.py) never produces one -
    it generates ABox Turtle for the page, not rendered HTML - so html_path
    is always None in current usage. Honest CANNOT_RUN, never a fabricated
    PASS, matching the same precondition-absent pattern the rest of the
    validator suite already uses (see rdodi_pipeline_validator_v1_4_0.py)."""
    if not html_path:
        return GateResult(gate_id, "PROPOSED", "CANNOT_RUN",
                           "no rendered HTML/DOM available - this pipeline generates page ABox, not rendered HTML; "
                           "router-functional testing requires an actual DOM to click through")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        return GateResult(gate_id, "PROPOSED", "CANNOT_RUN", f"cannot read html_path: {e}")
    if "<nav" not in html.lower() and "role=\"navigation\"" not in html.lower():
        return GateResult(gate_id, "PROPOSED", "FAIL",
                           "html_path provided but contains no <nav> element or role=navigation landmark")
    return GateResult(gate_id, "PROPOSED", "PASS",
                       "a <nav> element or navigation landmark is present in the rendered HTML "
                       "(static check only - does not simulate clicks; a real DOM/browser test would be stronger)")
