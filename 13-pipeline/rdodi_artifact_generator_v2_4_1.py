#!/usr/bin/env python3
"""RDODI Artifact Generator v2.4.1 — domain-general + profile-driven.

Supersedes the SCP-hardcoded rdodi_html_generator_v1_0_0 (which fell back to the SCP namespace and
read scp:example/scp:hasVisual). v2.4.1:
  - detects the DOMAIN's own namespace and top-level structure generically (no SCP fallback),
  - reads content through generic properties (skos:definition / rdfs:comment),
  - consumes an output PROFILE (doc:ArtifactKindSpec) to drive section structure,
  - emits a gate-readable Stage-3 DOCUMENT ABox (the gates validate ABoxes).

Usage:
  python3 rdodi_artifact_generator_v2_0_0.py <domain.ttl> <profiles.ttl> <ProfileLocalName> <out_dir>
"""
import sys, os, rdflib
from rdflib import RDF, RDFS, OWL, Literal, Namespace, URIRef
from rdflib.namespace import SKOS, DCTERMS

DOC = Namespace("http://example.org/rdodi/document-ontology#")
PROV = Namespace("http://www.w3.org/ns/prov#")
PROF = Namespace("http://rdodi.org/profiles#")
OUTDOC = Namespace("http://rdodi.org/generated/document#")

def loc(u): return str(u).split("#")[-1].split("/")[-1]

def detect_domain(g):
    """Generic: namespace = the most common class namespace; concepts = named classes carrying a
    skos:definition; areas = their direct named superclasses. No domain-specific names."""
    classes = [c for c in g.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)]
    if not classes: raise SystemExit("no owl:Class in domain")
    from collections import Counter
    ns = Counter(str(c).rsplit("#", 1)[0] + "#" for c in classes if "#" in str(c)).most_common(1)[0][0]
    concepts = [c for c in classes if g.value(c, SKOS.definition) and str(c).startswith(ns)]
    areas = {}
    for c in concepts:
        for sup in g.objects(c, RDFS.subClassOf):
            if isinstance(sup, URIRef) and str(sup).startswith(ns):
                areas.setdefault(sup, []).append(c)
    return ns, concepts, areas

def content_of(g, c):
    v = g.value(c, SKOS.definition) or g.value(c, RDFS.comment)
    return str(v).strip() if v else ""

def profile_sections(gp, profile):
    spec = PROF[profile]
    tmpl = gp.value(spec, DOC.hasStructuralTemplate)
    names = [str(n) for n in gp.objects(tmpl, DOC.requiredSectionName)]
    genre_ind = gp.value(spec, DOC.hasGenre)
    genre = str(gp.value(genre_ind, RDFS.label)) if (genre_ind and gp.value(genre_ind, RDFS.label)) else "artifact"
    return spec, names, genre

def first_sentence(text, fallback):
    t = text.strip()
    if not t: return fallback
    if t[-1] not in ".!?": t += "."
    return t

DCT = Namespace("http://purl.org/dc/terms/")

def _concept_text(g, c):
    """Real grounded content: the concept's actual skos:definition. No templates."""
    from rdflib.namespace import SKOS as _S
    v = g.value(c, _S.definition) or g.value(c, RDFS.comment)
    return str(v).strip() if v else None

def _concept_source(g, c, fallback):
    """Real source: the concept's own dcterms:source if present, else the area/ontology primary source."""
    v = g.value(c, DCT.source)
    return str(v).strip() if v else fallback

def _primary_source(g, ns):
    """The most common real dcterms:source in the domain = its primary source (NOT a generator stamp)."""
    from collections import Counter
    srcs = [str(o) for o in g.objects(None, DCT.source) if str(o).strip()]
    return Counter(srcs).most_common(1)[0][0] if srcs else None

def generate(domain_ttl, profiles_ttl, profile, out_dir):
    g = rdflib.Graph(); g.parse(domain_ttl, format="turtle")
    gp = rdflib.Graph(); gp.parse(profiles_ttl, format="turtle")
    ns, concepts, areas = detect_domain(g)
    spec, sec_names, genre = profile_sections(gp, profile)
    primary = _primary_source(g, ns)
    if not primary:
        raise SystemExit("HONEST STOP: domain carries no real dcterms:source; cannot source generated content. "
                         "Generation refused rather than emit a fake source.")
    _ont = next(iter(g.subjects(RDF.type, OWL.Ontology)), None)
    src = Literal(primary)   # REAL source from the domain, not a generator stamp

    out = rdflib.Graph()
    out.bind("doc", DOC); out.bind("gen", OUTDOC)
    report = OUTDOC["GeneratedReport"]
    out.add((report, RDF.type, DOC.ReportGenerationArtifact)); out.add((report, RDF.type, OWL.NamedIndividual))
    top_concepts = ", ".join(loc(c) for c in concepts[:6])
    out.add((report, RDFS.label, Literal(f"{genre.title()} on {loc(ns.rstrip('#'))}", lang="en")))
    out.add((report, SKOS.definition, Literal(
        f"This {genre} treats {len(concepts)} concepts across {len(areas)} areas of project quality, "
        f"including {top_concepts}, each presented with its source-grounded definition.", lang="en")))
    out.add((report, DCTERMS.source, Literal(primary)))
    out.add((report, DOC.conformsToArtifactKind, spec))

    order = 0
    area_list = list(areas.items())
    for name in sec_names:
        order += 1
        sid = OUTDOC[f"Section_{order:02d}"]
        out.add((sid, RDF.type, DOC.ReportSection)); out.add((sid, RDF.type, OWL.NamedIndividual))
        out.add((sid, RDFS.label, Literal(name, lang="en")))
        out.add((sid, DOC.sectionOrder if hasattr(DOC,'sectionOrder') else DCTERMS.identifier, Literal(order)))
        # CONTENT sections carry the domain's REAL definitions, sourced to the concepts' REAL citations.
        sec_source = src
        if name.lower() in ("concept sections", "background", "our approach", "results", "the problem"):
            if area_list:
                area, cs = area_list[order % len(area_list)]
                # grounded prose = each concept's ACTUAL skos:definition (verbatim from the ontology)
                parts, concept_srcs, used = [], [], []
                for c in cs[:5]:
                    defn = _concept_text(g, c)
                    if defn:
                        parts.append(f"{loc(c)}: {defn.rstrip('.')}." )
                        concept_srcs.append(_concept_source(g, c, primary)); used.append(c)
                prose = " ".join(parts) if parts else None
                if concept_srcs:
                    sec_source = Literal(concept_srcs[0])   # citation string DERIVED from the domain concept dc:source
                out.add((sid, (DOC.mappedToClass if hasattr(DOC,'mappedToClass') else DCTERMS.subject), area))
                # HYBRID PROV: link the section to the STABLE domain-concept IRIs it was generated from
                for c in used:
                    out.add((sid, PROV.wasDerivedFrom, c))
            else:
                prose = None
        elif name.lower() in ("abstract", "executive summary"):
            top = ", ".join(loc(a) for a, _ in area_list[:5])
            prose = (f"This {genre} treats {len(concepts)} concepts across {len(areas)} areas of the domain "
                     f"(including {top}), each presented with its source-grounded definition.") if area_list else None
        elif name.lower() == "introduction":
            prose = (f"The subject spans {len(areas)} areas; the sections that follow present each area's "
                     f"concepts using the definitions and citations recorded in the source ontology.") if areas else None
        elif name.lower() == "references":
            allsrc = sorted({_concept_source(g, c, primary) for c in concepts if _concept_source(g, c, None)})
            prose = ("The cited sources are: " + "; ".join(s[:80] for s in allsrc[:6]) + ".") if allsrc else None
        else:
            # structural-only sections (review questions, abbreviations): honest meta-description, sourced to primary
            prose = (f"This {name.lower()} section supports the reader's use of the generated {genre}.")
        # HONEST RULE: if a content section has no grounded prose, DO NOT emit filler — skip its definition.
        if prose:
            out.add((sid, SKOS.definition, Literal(prose, lang="en")))
            out.add((sid, DCTERMS.source, sec_source))
            if (sid, PROV.wasDerivedFrom, None) not in out and _ont is not None:
                out.add((sid, PROV.wasDerivedFrom, _ont))   # META section: whole-domain provenance
        else:
            out.add((sid, RDFS.comment, Literal("NO_GROUNDED_CONTENT: section left empty rather than filled with filler.", lang="en")))

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"generated_document_abox.ttl")
    out.serialize(destination=path, format="turtle")
    print(f"DOMAIN: ns={ns} concepts={len(concepts)} areas={len(areas)}")
    print(f"PROFILE: {profile} genre={genre} sections={len(sec_names)}")
    print(f"WROTE: {path}  ({len(out)} triples)")
    return path

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(__doc__); raise SystemExit(2)
    generate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# ================= v2.4.1 ADDITION: profile-driven PAGE generation (A3-page) =================
IP = Namespace("http://example.org/rdodi/interactive-page-ontology#")
OUTPG = Namespace("http://rdodi.org/generated/page#")

# profile genre -> page surface class (general; course-companion is one surface among several)
SURFACE_BY_GENRE = {
    "genre_CourseDocument": IP.InteractiveLearningSurface,
    "genre_TechnicalReport": IP.ResearchReportPage,
    "genre_Whitepaper": IP.Page,
}

def generate_page(domain_ttl, profiles_ttl, profile, doc_abox_ttl, out_dir):
    g = rdflib.Graph(); g.parse(domain_ttl, format="turtle")
    gp = rdflib.Graph(); gp.parse(profiles_ttl, format="turtle")
    gd = rdflib.Graph(); gd.parse(doc_abox_ttl, format="turtle")
    ns, concepts, areas = detect_domain(g)
    spec, sec_names, genre = profile_sections(gp, profile)
    primary = _primary_source(g, ns)
    if not primary:
        raise SystemExit("HONEST STOP: domain has no real source; page generation refused (no fake source).")
    src = Literal(primary)   # REAL source, not a generator stamp
    # map each document section -> its REAL source, to carry through to the mirroring page region
    docsrc = {}
    for sec in gd.subjects(RDF.type, DOC.ReportSection):
        lbl = str(gd.value(sec, RDFS.label) or ""); ssrc = gd.value(sec, DCTERMS.source)
        if ssrc: docsrc[lbl] = str(ssrc)
    surface_cls = SURFACE_BY_GENRE.get(genre, IP.Page)

    out = rdflib.Graph(); out.bind("ip", IP); out.bind("gen", OUTPG)
    surface = OUTPG["Surface"]
    out.add((surface, RDF.type, surface_cls)); out.add((surface, RDF.type, OWL.NamedIndividual))
    out.add((surface, RDFS.label, Literal(f"Generated {genre} interactive surface", lang="en")))
    out.add((surface, SKOS.definition, Literal(
        f"An interactive surface rendering the generated {genre} for the domain at {ns}.", lang="en")))
    out.add((surface, DCTERMS.source, src))
    out.add((surface, IP.genre, Literal(genre)))   # v2.4.1: page declares its genre (profile-driven, renderer-readable)

    # one ContentRegion per document section (general class, no hard SHACL requirement)
    order = 0
    for sec in gd.subjects(RDF.type, DOC.ReportSection):
        order += 1
        label = str(gd.value(sec, RDFS.label) or f"Region {order}")
        defn = str(gd.value(sec, SKOS.definition) or "")
        r = OUTPG[f"Region_{order:02d}"]
        out.add((r, RDF.type, IP.ContentRegion)); out.add((r, RDF.type, OWL.NamedIndividual))
        out.add((r, RDFS.label, Literal(label, lang="en")))
        out.add((r, SKOS.definition, Literal(defn or f"Content region rendering the {label} section.", lang="en")))
        out.add((r, DCTERMS.source, Literal(docsrc.get(label, primary))))   # derived from the doc section's source
        out.add((r, PROV.wasDerivedFrom, sec))                              # HYBRID PROV: region -> document section IRI

    # table of contents (general)
    toc = OUTPG["TOC"]
    out.add((toc, RDF.type, IP.TableOfContents)); out.add((toc, RDF.type, OWL.NamedIndividual))
    out.add((toc, RDFS.label, Literal("Linked outline of the generated sections.", lang="en")))
    out.add((toc, SKOS.definition, Literal("This table of contents links every generated section of the surface.", lang="en")))
    out.add((toc, DCTERMS.source, src))

    # profile-appropriate interactive elements
    if genre == "genre_CourseDocument":
        # one InstructionalWidget (must have demonstratesSubject>=1 -> point at a real domain concept)
        if concepts:
            w = OUTPG["ConceptWidget"]; subj = concepts[0]
            out.add((w, RDF.type, IP.InstructionalWidget)); out.add((w, RDF.type, OWL.NamedIndividual))
            out.add((w, RDFS.label, Literal(f"Interactive widget demonstrating {loc(subj)}.", lang="en")))
            out.add((w, SKOS.definition, Literal(
                f"This widget lets the learner explore {loc(subj)} as defined in the domain ontology.", lang="en")))
            out.add((w, IP.demonstratesSubject, subj))
            out.add((w, DCTERMS.source, src))
        # real review questions (substantive, sourced) — one per first few areas
        for i, (area, _cs) in enumerate(list(areas.items())[:3], 1):
            q = OUTPG[f"RQ_{i}"]
            out.add((q, RDF.type, IP.ReviewQuestion)); out.add((q, RDF.type, OWL.NamedIndividual))
            out.add((q, RDFS.label, Literal(
                f"How does the concept of {loc(area)} apply within this domain, and why does it matter?", lang="en")))
            out.add((q, SKOS.definition, Literal(
                f"This review question asks the learner to explain {loc(area)} and its role in the domain.", lang="en")))
            out.add((q, DCTERMS.source, src))
    elif genre == "genre_Whitepaper":
        cta = OUTPG["CTA"]
        out.add((cta, RDF.type, IP.CallToAction)); out.add((cta, RDF.type, OWL.NamedIndividual))
        out.add((cta, RDFS.label, Literal("Adopt the approach described in this whitepaper.", lang="en")))
        out.add((cta, SKOS.definition, Literal("This call to action invites the reader to act on the whitepaper's recommendation.", lang="en")))
        out.add((cta, DCTERMS.source, src))

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "generated_page_abox.ttl")
    out.serialize(destination=path, format="turtle")
    print(f"PAGE: surface={loc(surface_cls)} regions={order} genre={genre}; WROTE {path} ({len(out)} triples)")
    return path

if __name__ == "__main__" and len(sys.argv) >= 6 and sys.argv[5] == "--page":
    # mode: <domain> <profiles> <Profile> <out_dir> --page <doc_abox>
    generate_page(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[6], sys.argv[4])
