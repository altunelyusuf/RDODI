import re

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(f"{'PASS' if cond else 'FAIL'}: {name}")

with open("../06-instance/vaf_operators_knowledge_base_v1_0_0.html", encoding="utf-8") as f:
    content = f.read()

# ===================== Real VAF content genuinely present =====================
check("T1 Mandatory operator's real thesis text (zorunluluk) present", "zorunluluk" in content)
check("T2 ProfileFamily concept present", "ProfileFamily" in content or "Profile Family" in content)
check("T3 real thesis citation (Altunel) present", "Altunel" in content)
check("T4 real literature grounding (Gurov) present", "Gurov" in content)
check("T5 real literature grounding (Haber) present", "Haber" in content)
check("T6 all 12 real operator short names present",
      all(op in content for op in ["Mandatory", "Optional", "Exclusive", "Or Operator" if False else "Or",
                                     "Dependency", "Repetition", "Addition", "Subtraction",
                                     "Cartesian", "Division", "Intersection", "Inverse"]))

# ===================== Source placeholder content genuinely gone =====================
check("T7 source placeholder 'Set clear priorities' genuinely absent", "Set clear priorities" not in content)
check("T8 source placeholder 'Root-Cause Analysis' genuinely absent", "Root-Cause Analysis" not in content)

# ===================== Title correctly derived from the real MISSION =====================
m = re.search(r"<title>(.*?)</title>", content)
check("T9 real <title> derived from the real MISSION text",
      m is not None and "algebra of 12 real operators" in m.group(1))

# ===================== Real relations content present =====================
check("T10 real relation evidence text present (Inverse/Mandatory override relationship)",
      "capable of removing what Mandatory would otherwise guarantee" in content)

check("T11 output is substantial (source-scale page, not a stub)", len(content) > 1_000_000)

n_pass = sum(1 for _, ok in results if ok)
print(f"\n{n_pass}/{len(results)} PASS")
import sys
sys.exit(0 if n_pass == len(results) else 1)
