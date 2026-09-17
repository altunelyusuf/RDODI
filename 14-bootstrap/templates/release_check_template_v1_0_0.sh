#!/usr/bin/env bash
# release_check_template.sh — the R21 four-program gate chain, generalized
# from the semtech-landscape byproduct's own release_check_vX.sh scripts.
#
# Pattern R21: a structural validator, per-release supplementary gates, a
# cross-stage procedure audit, and a live DOM/interaction smoke test,
# chained into one script a publish step refuses to bypass. Demonstrated
# to scale from ~14/29/22/25 assertions to 10+4/40/22/149 across roughly
# forty releases of one real byproduct, purely by adding assertions —
# never restructured.
#
# USAGE: fill in the four REPLACE_ME command lines below for your
# byproduct's own gate scripts, then wire this file into your publish
# tool exactly the way the source byproduct's oe_publish script does:
# refuse to push if this script's exit code is non-zero.
set -e
cd "$(dirname "$0")/.."

echo "== release check: $(cat VERSION.txt 2>/dev/null || echo '?') =="

find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# ---- 1. structural validator: Turtle/SHACL parse + stage conformance ----
echo "-- 1/4 structural validator --"
python3 -B REPLACE_ME_validator.py --config REPLACE_ME_validator_config.json \
  | tail -2 | grep -q "OVERALL: PASS" \
  || { echo "REFUSED: structural validator did not report OVERALL: PASS"; exit 1; }
echo "structural validator: PASS"

# ---- 2. supplementary gates: content-specific, one added per release ----
echo "-- 2/4 supplementary gates --"
python3 -B REPLACE_ME_supplementary_gates.py > /tmp/rc_supp.log 2>&1 \
  && tail -1 /tmp/rc_supp.log \
  || { tail -20 /tmp/rc_supp.log; echo "REFUSED: supplementary gates failed"; exit 1; }

# ---- 3. procedure audit: cross-stage properties no single stage sees ----
echo "-- 3/4 procedure audit --"
python3 -B REPLACE_ME_procedure_audit.py > /tmp/rc_audit.log 2>&1 \
  && tail -1 /tmp/rc_audit.log \
  || { tail -20 /tmp/rc_audit.log; echo "REFUSED: procedure audit failed"; exit 1; }

# ---- 4. DOM/interaction smoke test: drive the real rendered artifact ----
echo "-- 4/4 DOM smoke test --"
NODE_PATH="${NODE_PATH:-/home/claude/node_modules}" node REPLACE_ME_dom_smoke.js > /tmp/rc_smoke.log 2>&1 \
  && tail -1 /tmp/rc_smoke.log \
  || { tail -20 /tmp/rc_smoke.log; echo "REFUSED: DOM smoke test failed"; exit 1; }

echo "release_check: ALL FOUR GATE PROGRAMS PASS"
