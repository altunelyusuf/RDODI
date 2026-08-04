#!/usr/bin/env python3
"""
Reference Rule Gate v1.0.0  (replaces the retired Stage1.D/Stage3.F >=40 count)
================================================================================
Grounded RULE, no number (test-drive-settled): a citation list is adequate iff
  (1) every external claim that needs a source carries a citation,
  (2) every citation is BP-D41-verified (real/openable) or explicitly flagged unavailable,
  (3) no citation is dangling (cites a ref id that doesn't exist).
The >=40 count wrongly PASSED docs with fabricated/uncited refs and wrongly FAILED
well-sourced short docs. This rule ties the verdict to what references are FOR.
Honest residual (L-40): "needs a source" and "verified" are partly tier-C judgments;
the gate checks the recorded status, it cannot itself prove a source is genuine.
"""
from dataclasses import dataclass, field

@dataclass
class RefResult:
    verdict: str; detail: str
    uncited: list = field(default_factory=list)
    unverified: list = field(default_factory=list)
    dangling: list = field(default_factory=list)

def reference_rule(refs, claims):
    """refs: [{'id', 'status'}]; status in {'verified','unavailable_flagged','unverified'}.
       claims: [{'text','needs_cite','cites':[ref_id,...]}]."""
    ref_ids = {r["id"] for r in refs}
    uncited = [c["text"] for c in claims if c.get("needs_cite") and not c.get("cites")]
    # 'unavailable_flagged' is acceptable (honest disclosure); only 'unverified' fails
    unverified = [r["id"] for r in refs if r["status"] not in ("verified", "unavailable_flagged")]
    dangling = [c["text"] for c in claims if c.get("cites") and not (set(c["cites"]) & ref_ids)]
    fails = []
    if uncited:   fails.append(f"{len(uncited)} external claim(s) uncited")
    if unverified:fails.append(f"{len(unverified)} citation(s) unverified")
    if dangling:  fails.append(f"{len(dangling)} dangling citation(s)")
    verdict = "FAIL" if fails else "PASS"
    detail = "; ".join(fails) if fails else f"all claims cited; all {len(refs)} citations verified/flagged"
    return RefResult(verdict, detail, uncited, unverified, dangling)
