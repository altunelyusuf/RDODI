#!/usr/bin/env python3
"""
Discourse-Driven Widget Auto-Selector v1.0.0  (Phase 2, ORIGINATED)
====================================================================
Self-adapting: given a source passage, detects discourse features and auto-selects
the warranted widget primitive(s). No manual menu. Each selection emits its warrant.

Tier discipline: MECHANICAL features are detected deterministically here. INTERPRETIVE
features are, in production, routed to an LLM/human judge — for the test-drive they are
simulated via an explicit signal dict so the selector logic itself can be tested.
Mis-selection affects fitness-of-form only, never content correctness (blueprint F39/F53).
"""
import re, rdflib
from rdflib.namespace import RDF
DS = "http://example.org/rdodi/discourse-selection#"
WP = "http://example.org/widget-primitives#"

def load_rules(abox_path):
    g = rdflib.Graph(); g.parse(abox_path, format="turtle")
    rules = []  # (primitive, feature, tier, detection_rule_text)
    for prim, feat in g.subject_objects(rdflib.URIRef(DS+"autoSelectsWhen")):
        tier = g.value(feat, rdflib.URIRef(DS+"hasDetectionTier"))
        rule = g.value(feat, rdflib.URIRef(DS+"detectionRule"))
        rules.append((str(prim).rsplit('#',1)[-1], str(feat).rsplit('#',1)[-1],
                      str(tier).rsplit('#',1)[-1] if tier else "?", str(rule)))
    return rules

# --- MECHANICAL feature detectors (deterministic on passage text) ---
def detect_k_category_enumeration(text):
    # >=3 enumerated named categories each with a definition-like continuation
    items = re.findall(r'(?:^|\n)\s*(?:[-*\u2022]|\d+\.)\s+([A-Z][^\n:]{2,40})[:\-]', text)
    return len(items) >= 3, f"{len(items)} enumerated named categories"

def detect_multi_source_case_set(text):
    cites = re.findall(r'\((?:19|20)\d{2}\)|https?://|\[\d+\]', text)
    cases = re.findall(r'(?:case|example|incident)\b', text, re.I)
    return (len(cites) >= 2 and len(cases) >= 2), f"{len(cases)} case-words, {len(cites)} citations"

def detect_filterable_item_set(text):
    has_items = bool(re.search(r'\b(items?|products?|records?|entries|projects?)\b', text, re.I))
    attrs = re.findall(r'\b(price|cost|date|category|size|rating|duration|status|type)\b', text, re.I)
    return (has_items and len(set(a.lower() for a in attrs)) >= 2), f"items + {len(set(a.lower() for a in attrs))} attributes"

def detect_mixed_source_tiers(text):
    tiers = 0
    if re.search(r'textbook|chapter|p\.\s?\d+', text, re.I): tiers += 1
    if re.search(r'https?://|announced|blog|press release', text, re.I): tiers += 1
    if re.search(r'\[\d+\]|et al|journal|proceedings', text, re.I): tiers += 1
    return tiers >= 2, f"{tiers} source tiers"

MECHANICAL = {
 "Feature_KCategoryEnumeration": detect_k_category_enumeration,
 "Feature_MultiSourceCaseSet": detect_multi_source_case_set,
 "Feature_FilterableItemSet": detect_filterable_item_set,
 "Feature_MixedSourceTiers": detect_mixed_source_tiers,
}

def select_widgets(passage_text, rules, interpretive_signals=None):
    """Returns list of (primitive, feature, tier, warrant). interpretive_signals: dict
    feature_name->bool simulating the LLM/human judge for TIER-C features."""
    interpretive_signals = interpretive_signals or {}
    selected = []
    for prim, feat, tier, ruletext in rules:
        if tier == "Tier_Mechanical":
            detector = MECHANICAL.get(feat)
            if detector:
                fired, evidence = detector(passage_text)
                if fired:
                    selected.append((prim, feat, "TIER-A", f"mechanical: {evidence}"))
        elif tier == "Tier_Interpretive":
            if interpretive_signals.get(feat, False):
                selected.append((prim, feat, "TIER-C", "interpretive: judge confirmed"))
    return selected

if __name__ == "__main__":
    rules = load_rules("discourse_selection_abox_v1_0_0.ttl")
    print(f"loaded {len(rules)} selection rules")
