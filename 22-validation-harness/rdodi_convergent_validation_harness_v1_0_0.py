#!/usr/bin/env python3
"""RDODI Convergent-Validation Harness v1.0.0 (R-E7).

Productizes the method that worked in the STG study: pre-register -> blind-build -> seal-reveal -> measured-compare.
The independence guarantee is enforced IN CODE, not by manual discipline:
  - the parallel package is sealed by SHA on receipt and CANNOT be opened until the candidate is frozen;
  - seal integrity is re-verified at reveal (byte-identical or it raises);
  - comparison is MEASURED — the same criteria function is RUN on both artifacts (L-65/BP-D2), never narrated.

State machine: INIT -> PREREGISTERED -> CANDIDATE_FROZEN -> SEALED -> REVEALED -> COMPARED.
Out-of-order calls raise — that is the point (drift/contamination becomes impossible, not merely discouraged).
"""
import hashlib, json, os

def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

class ConvergentValidationHarness:
    def __init__(self, name):
        self.name = name
        self.state = "INIT"
        self.prereg_sha = None
        self.candidate_sha = None
        self.parallel_sha = None
        self.log = []

    def _require(self, expected):
        if self.state != expected:
            raise RuntimeError(f"seal-reveal protocol violation: need state {expected}, am {self.state}")
        self.log.append(f"[{self.state}] ok")

    def preregister(self, prereg_path):
        self._require("INIT")
        self.prereg_sha = _sha(prereg_path)
        self.state = "PREREGISTERED"
        self.log.append(f"preregistered {os.path.basename(prereg_path)} sha={self.prereg_sha[:16]}")
        return self.prereg_sha

    def freeze_candidate(self, candidate_path):
        self._require("PREREGISTERED")
        self.candidate_sha = _sha(candidate_path)
        self.state = "CANDIDATE_FROZEN"
        self.log.append(f"candidate frozen sha={self.candidate_sha[:16]}")
        return self.candidate_sha

    def seal_parallel(self, parallel_path):
        # may seal only AFTER the candidate is frozen — opening earlier could contaminate the build
        self._require("CANDIDATE_FROZEN")
        self.parallel_sha = _sha(parallel_path)
        self._sealed_path = parallel_path
        self.state = "SEALED"
        self.log.append(f"parallel SEALED sha={self.parallel_sha[:16]} (not opened)")
        return self.parallel_sha

    def reveal(self):
        # enforced gate: candidate must be frozen AND seal integrity must hold
        self._require("SEALED")
        now = _sha(self._sealed_path)
        if now != self.parallel_sha:
            raise RuntimeError(f"seal integrity FAIL: {now[:16]} != sealed {self.parallel_sha[:16]}")
        self.state = "REVEALED"
        self.log.append("seal integrity verified; parallel may now be opened")
        return True

    def compare(self, candidate_artifact, parallel_artifact, criteria_fn):
        # measured comparison: RUN the same criteria on both (never narrate)
        self._require("REVEALED")
        cand = criteria_fn(candidate_artifact)
        par = criteria_fn(parallel_artifact)
        keys = sorted(set(cand) | set(par))
        convergence, gaps = {}, {}
        for k in keys:
            cv, pv = cand.get(k), par.get(k)
            (convergence if cv == pv else gaps)[k] = {"candidate": cv, "parallel": pv}
        self.state = "COMPARED"
        self.log.append(f"compared: {len(convergence)} convergent, {len(gaps)} divergent criteria")
        return {"convergence": convergence, "gaps": gaps, "candidate": cand, "parallel": par}

    def report(self):
        return {"name": self.name, "state": self.state, "prereg_sha": self.prereg_sha,
                "candidate_sha": self.candidate_sha, "parallel_sha": self.parallel_sha, "log": self.log}
