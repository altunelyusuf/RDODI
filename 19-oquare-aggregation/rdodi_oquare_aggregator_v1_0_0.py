#!/usr/bin/env python3
"""RDODI OQuaRE Characteristic Aggregator v1.0.0 (R1) — GUARDED ISO-25000 aggregation overlay.

Aggregates the OQuaRE base metrics (computed by the assessor) into ISO/IEC-25000-aligned characteristic
scores, using a DECLARED, attributed, verify-against-source scaling config. Honesty guards are structural:
  G1  scaling bands + characteristic matrix are read from the declared config — no invented canonical values.
  G2  no bare scores — every characteristic emits its constituent metrics, their scaled values, and the bands.
  G3  output status is INDICATIVE / computed-per-declared-method / NOT a certification.
  G4  the base-metric layer is untouched; this is a separate overlay.

Usage: python3 rdodi_oquare_aggregator_v1_0_0.py <domain.ttl> <assessor.py> <scaling_config.ttl>
"""
import sys, json, importlib.util, rdflib
from rdflib import Namespace
OQ = Namespace("http://example.org/rdodi/oquare-scaling#")

def load(path, name):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

def scale(value, b1, b2, b3, b4, direction):
    """Map a raw metric to 1..5 using declared band edges + direction. Returns (scaled, band_desc)."""
    edges = [b1, b2, b3, b4]
    asc = 1
    for i, e in enumerate(edges):
        if value <= e:
            asc = i + 1; break
    else:
        asc = 5
    sc = asc if direction == "higher_better" else (6 - asc)
    return sc, f"v={value:.3f} vs bands {edges} ({direction}) -> {sc}/5"

def aggregate(domain_ttl, assessor_py, config_ttl):
    ASR = load(assessor_py, "asr")
    # G4: pull base metrics from the assessor WITHOUT touching that layer
    _, gates, _ = ASR.assess(domain_ttl, None, _quiet=True)
    base = {}
    for g in gates:
        if isinstance(g.get("detail"), dict) and "OQuaRE" in g["detail"]:
            base = g["detail"]["OQuaRE"]; break
    cfg = rdflib.Graph(); cfg.parse(config_ttl, format="turtle")
    # G1: read scaling from declared config
    scalings = {}
    for s in cfg.subjects(rdflib.RDF.type, OQ.Scaling):
        m = str(cfg.value(s, OQ.metric))
        scalings[m] = (float(cfg.value(s, OQ.b1)), float(cfg.value(s, OQ.b2)),
                       float(cfg.value(s, OQ.b3)), float(cfg.value(s, OQ.b4)),
                       str(cfg.value(s, OQ.direction)))
    out = {"status": "INDICATIVE — computed per the DECLARED OQuaRE-attributed scaling; NOT a certification. "
                     "Verify the bands/matrix in the config against Duque-Ramos et al. before any external use.",
           "base_metrics_source": "assessor (unchanged base-metric layer)",
           "characteristics": []}
    for c in cfg.subjects(rdflib.RDF.type, OQ.Characteristic):
        cname = str(cfg.value(c, OQ.characteristic))
        metrics = [str(m) for m in cfg.objects(c, OQ.includesMetric)]
        constituents, vals = [], []
        for m in metrics:
            if m in base and m in scalings:
                sc, desc = scale(base[m], *scalings[m])
                vals.append(sc)
                constituents.append({"metric": m, "raw": base[m], "scaled_1to5": sc, "derivation": desc})
        score = round(sum(vals) / len(vals), 2) if vals else None
        # G2: never a bare score — always with constituents + derivations
        out["characteristics"].append({
            "characteristic": cname,
            "indicative_score_1to5": score,
            "label": "INDICATIVE, not certified",
            "constituents": constituents})
    return out

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__); raise SystemExit(2)
    rep = aggregate(sys.argv[1], sys.argv[2], sys.argv[3])
    print("=== OQuaRE Characteristic Aggregation (GUARDED) ===")
    print(rep["status"])
    for c in rep["characteristics"]:
        print(f"\n[{c['characteristic']}] indicative {c['indicative_score_1to5']}/5  ({c['label']})")
        for k in c["constituents"]:
            print(f"   {k['metric']:9s} raw={k['raw']:.3f}  scaled={k['scaled_1to5']}/5   [{k['derivation']}]")
    json.dump(rep, open("oquare_aggregation_report.json", "w"), indent=2)
    print("\n(report -> oquare_aggregation_report.json)")
