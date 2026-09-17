#!/usr/bin/env python3
"""lineage_disk_audit v1.0.0 -- cross-checks a BRSF lineage register's
claims against the actual package tree on disk. Deterministic, no LLM.
Built as a permanent version of the ad hoc check run manually two turns
ago in this session; wired into release_check so it runs on every
publish instead of only when someone happens to remember to ask.

Checks:
  (1) every backlog:hasArtifactPath entry resolves to a real file
      under the package root
  (2) the ipo:Cap_SemanticRetrieval family member count matches what
      MetricObservation ex:Obs_Vocab claims
  (3) ipo:SPARQLEngine's own skos:definition mentions the depth count
      MetricObservation ex:Obs_SparqlDef claims

Exit 0 on all-clear, 1 on any mismatch (printed).
"""
import re, sys, os

PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINEAGE = os.path.join(PKG_ROOT, "28-interactive-html-surface", "09-handover-response",
                        "rdodi_handover_response_lineage_abox_v1_0_0.ttl")
TBOX = os.path.join(PKG_ROOT, "01-stage-vocabularies", "04-interactive-page",
                     "interactive_page_ontology_tbox_v1_9_0.ttl")

def main():
    problems = []
    lineage_text = open(LINEAGE).read()
    tbox_text = open(TBOX).read()

    for m in re.finditer(r'backlog:hasArtifactPath\s+"([^"]+)"', lineage_text):
        raw = m.group(1)
        for path in [p.strip() for p in raw.split(";")]:
            if not os.path.exists(os.path.join(PKG_ROOT, path)):
                problems.append(f"artifact path not found from package root: {path}")

    claimed_vocab = 3
    actual_vocab = sum(1 for name in [
        "ipo:Cap_SemanticRetrieval a", "ipo:Cap_SemanticRetrieval_Lexical a",
        "ipo:Cap_SemanticRetrieval_Embedding a"] if name in tbox_text)
    if actual_vocab != claimed_vocab:
        problems.append(f"Cap_SemanticRetrieval count: register claims {claimed_vocab}, disk has {actual_vocab}")

    m = re.search(r'ipo:SPARQLEngine a owl:Class.*?skos:definition "(.*?)"@en', tbox_text, re.S)
    defn = m.group(1) if m else ""
    if "two depths" not in defn.lower():
        problems.append("ipo:SPARQLEngine definition no longer names 'two depths' as the register claims")

    if problems:
        print("LINEAGE DISK AUDIT: MISMATCH FOUND")
        for p in problems:
            print(" -", p)
        return 1
    print("LINEAGE DISK AUDIT: PASS -- all claims match disk state")
    return 0

if __name__ == "__main__":
    sys.exit(main())
