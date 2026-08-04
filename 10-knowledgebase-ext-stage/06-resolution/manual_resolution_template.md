# Manual Catalogue Resolution Template

Use this template when promoting an item from `kbx:Reconstructed` to `kbx:CatalogueVerified` by hand.
The ratifier looks up the item in a catalogue, fills in the fields below, and the result is appended to the ABox as a new `kbx:CatalogueRecord`.

**Honesty rule** (PATCH v1.0.1):
- `CatalogueVerified` confirms **metadata correctness**, not content correctness.
- A `CatalogueVerified` promotion does **not** retract a `Reconstructed` flag automatically; both tiers coexist until a Stage AA primary-source consultation promotes the item further to `Consulted`.
- `resolvedAtUTC` is required so a future re-check can detect drift if the catalogue record changes.

---

## Fields to fill in

| Field | Example | Notes |
|---|---|---|
| `item_local_id` | `marchewka2014` | The local ID of the item in `rdodi_knowledgebase_ext_abox_v1_0_0.ttl` or in your bundle's citation ABox. |
| `catalogue_local_id` | `crossref` | One of the 42 `kbxi:cat_*` catalogues. See the catalogue list at the bottom of this file. |
| `identifier_kind` | `DOI` | DOI, ISBN, ISSN, RFC number, W3C TR shortname, ISO catalogue number, arXiv ID, DBLP key, ACM DL number, PMID, LCCN, YÖK Tez number, ORCID iD, USPTO patent number, EPO publication number. |
| `identifier_value` | `10.xxxx/yyyyy` | The actual identifier returned by the catalogue. |
| `resolved_url` | `https://doi.org/10.xxxx/yyyyy` | The canonical URL at resolution time. |
| `resolved_title` | The book/paper title as the catalogue reports it. | Compare to the item's `rdfs:label` — divergence is grounds for a resolverNote. |
| `resolved_authors` | "Marchewka, J. T." | Authors as the catalogue formats them. |
| `resolved_year` | `2014` | Publication year per the catalogue. |
| `resolved_at_utc` | `2026-05-29T14:30:00Z` | ISO-8601 UTC timestamp of resolution. Use UTC. |
| `resolver_note` | "Edition matches — 5th edition 2014." | Any honest disclosure about the resolution (partial match, multiple editions, ambiguous record, etc.). Optional but recommended. |

---

## TTL fragment to append

Once the form is filled in, append this fragment to the ABox PATCH (or to a new file referenced by the bundle):

```turtle
kbxi:rec_<item_local_id>_<sequence> a kbx:CatalogueRecord, owl:NamedIndividual ;
    rdfs:label "Catalogue resolution: <item_local_id> via <catalogue_local_id>"@en ;
    skos:definition "CatalogueRecord asserting that <item_local_id> was located in <catalogue_local_id> with identifier <identifier_kind>=<identifier_value> at <resolved_at_utc>."@en ;
    kbx:resolvedIn kbxi:cat_<catalogue_local_id> ;
    kbx:resolvedAtUTC "<resolved_at_utc>"^^xsd:dateTime ;
    kbx:resolvedIdentifier "<identifier_value>" ;
    kbx:resolvedURL "<resolved_url>" ;
    kbx:resolvedTitle "<resolved_title>" ;
    kbx:resolvedAuthors "<resolved_authors>" ;
    kbx:resolvedYear "<resolved_year>"^^xsd:gYear ;
    kbx:resolverNote "<resolver_note>" .

kbxi:<item_local_id>
    kbx:catalogueResolution kbxi:rec_<item_local_id>_<sequence> ;
    kbx:consultationStatus kbx:CatalogueVerified .
```

After appending, re-run `kbext_gates_v1_0_1.py` to confirm structural validity.

---

## Catalogue chooser — which catalogue for which item

| Item kind | Try first | Fallback |
|---|---|---|
| ACM-published conference or journal | `acm_dl` | `dblp` (CS metadata cross-check), `crossref` (DOI) |
| IEEE-published conference, journal, or standard | `ieee_xplore` | `crossref`, `inspec` |
| Springer / LNCS volume | `springer_link` | `dblp`, `crossref` |
| Elsevier journal | `sciencedirect` | `crossref` |
| Wiley, Taylor & Francis, SAGE journal | `wiley_online`, `taylor_francis`, `sage_journals` | `crossref` |
| Older journal article (pre-2000) without DOI | `jstor` (humanities/social sci), `inspec`, `mathscinet` | `wikidata`, `worldcat` |
| Mathematics article | `mathscinet` | `crossref`, `arxiv` |
| Biomedicine article | `pubmed` | `crossref`, `wikidata` |
| Preprint (CS, math, physics) | `arxiv` | `dblp`, `crossref` (if published) |
| Preprint (biology) | `biorxiv` | — |
| NLP / computational linguistics paper | `acl_anthology` | `dblp`, `arxiv` |
| W3C standard | `w3c_tr` | — |
| IETF standard or RFC | `ietf_rfc`, `ietf_datatracker` | — |
| ISO standard | `iso_obp` | `iec_webstore` (if joint) |
| IEC standard | `iec_webstore` | `iso_obp` |
| NIST publication (FIPS, SP, NISTIR) | `nist_publications` | — |
| OASIS standard | `oasis_standards` | — |
| Book (general) | `library_of_congress`, `worldcat` | `openlibrary`, `crossref` (if assigned DOI) |
| Doctoral thesis (US) | `proquest_dissertations` | `worldcat` |
| Doctoral thesis (Europe) | `dart_europe` | `proquest_dissertations` |
| Doctoral thesis (Turkey) | `yok_tez` | `tubitak_ulakbim` |
| Turkish academic journal | `tr_dizin`, `dergipark` | `tubitak_ulakbim` |
| Software/code artefact | `software_heritage` | `zenodo` (if DOI-assigned release) |
| Data deposit | `zenodo` | `crossref` (if DOI-assigned) |
| Researcher identity | `orcid_registry` | — |
| US patent | `uspto` | `epo_espacenet` (cross-jurisdiction) |
| European or worldwide patent | `epo_espacenet` | — |
| Discovery / broad search | `openalex`, `semantic_scholar` | `google_scholar` (with LOW-authority caveat) |
| Cross-link or triangulation | `wikidata` | — |

---

## Catalogues with strong caveats (read before using)

- **`google_scholar`** — **LOW authority**. Not curated; indexes predatory journals and grey literature indiscriminately. A Google Scholar hit confirms only that something exists at that URL with that title at the time of crawl. **Always verify a positive hit in a curated catalogue** (Crossref, DBLP, publisher) before treating it as catalogue resolution.
- **`openlibrary`** — Moderate authority; editorial control less strict than Library of Congress or WorldCat. Useful for cross-checking ISBNs.
- **`wikidata`** — Authority varies by item. Well-known works have authoritative cross-linked metadata; niche works may have user-edited records.
- **`openalex`**, **`semantic_scholar`** — Useful for discovery and citation graphs. Automatic concept tagging and ML-generated summaries may introduce noise; **not authoritative for exact metadata correctness**.
- **`dergipark`** — Hosting platform, not editorial authority. A DergiPark hit confirms hosting; the editorial standing belongs to each journal.
- **`zenodo`**, **`arxiv`**, **`biorxiv`** — Deposit-based; a hit confirms a specific artefact was deposited at a specific time. **Not peer-review certifications.**

---

## What to do if no catalogue resolves the item

The item stays `Reconstructed` (or is moved to `RequiresConsultation` if the reconstructed account is too thin to publish). The ratifier should record an honest note in the item's `kbx:applicabilityNote` explaining why no catalogue resolution was possible (out-of-scope work, lost-to-time reference, etc.). The next step is **content consultation** via the Stage AA ingestor when the primary source can be obtained.
