#!/usr/bin/env python3
"""
doc_standards_gates_v1_0_0.py — enforces RDODI Documentation Standards v1.0.0.
Tier A = GUARANTEE (mechanical), Tier B = FLAG (proxy), Tier C = REQUIRE attestation (cannot pass here).
Run: python3 doc_standards_gates_v1_0_0.py <report.md> [--profile SeminalDoc] [--fk-low 11 --fk-high 16]
Honest by construction: Tier-C gates return REQUIRES_ATTESTATION, never PASS.
"""
import re, sys, json, math

def load(path): return open(path, encoding='utf-8').read()

# ---------- helpers ----------
def sentences(text):
    body=re.sub(r'`[^`]*`|\|.*\|',' ',text)  # strip code/tables
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', body) if len(s.strip())>3]
def words(text): return re.findall(r"[A-Za-z']+", text)
def syllables(w):
    w=w.lower(); v='aeiouy'; n=0; prev=False
    for c in w:
        isv=c in v
        if isv and not prev: n+=1
        prev=isv
    if w.endswith('e'): n=max(1,n-1)
    return max(1,n)

# ---------- TIER A (GUARANTEE) ----------
def gate_abbrev_firstuse(text):
    acro=re.findall(r'\b([A-Z]{2,}[0-9]*)\b', text)
    seen={}; missing=[]
    KNOWN_ORG={'ISO','IEC','IT','OE','OF','CMU','CD','CI'}  # org/short — expansion optional
    for a in acro:
        if a in seen: continue
        seen[a]=True
        if a in KNOWN_ORG: continue
        idx=text.find(a)
        window=text[max(0,idx-80):idx+len(a)+80]
        # expansion present if "Word Word (A)" or "A (Word Word)" near first use
        if re.search(rf'[A-Za-z][A-Za-z ]{{3,}}\(\s*{re.escape(a)}\s*\)', window) or \
           re.search(rf'{re.escape(a)}\s*\([A-Za-z][A-Za-z ]{{3,}}\)', window):
            continue
        missing.append(a)
    return ('GUARANTEE','gate_abbrev_firstuse', not missing,
            f"{len(missing)} acronyms lack first-use expansion: {missing[:10]}")

def gate_abbrev_list(text):
    has_list = bool(re.search(r'(?im)^#+\s*(list of )?abbreviations', text))
    used=set(a for a in re.findall(r'\b([A-Z]{2,}[0-9]*)\b', text))
    return ('GUARANTEE','gate_abbrev_list', has_list,
            ("abbreviations list present" if has_list else f"no List of Abbreviations (≈{len(used)} acronyms used)"))

def gate_intext_citations(text):
    author_year=re.findall(r'\([A-Z][A-Za-z]+(?: et al\.?)?,?\s*\d{4}[a-z]?\)', text)
    numeric=re.findall(r'\[\d+\]', text)
    style = 'author-year' if len(author_year)>len(numeric) else ('numeric' if numeric else None)
    n=max(len(author_year),len(numeric))
    return ('GUARANTEE','gate_intext_citations', n>0,
            f"{n} in-text citations ({style or 'NONE detected — uses informal Source: lines'})")

def gate_reference_list(text):
    has=bool(re.search(r'(?im)^#+\s*(references|bibliography)\b', text))
    return ('GUARANTEE','gate_reference_list', has, "References section present" if has else "no References section")

def gate_cite_ref_reconcile(text):
    cites=set(re.findall(r'\[(\d+)\]', text))
    refsec=re.split(r'(?im)^#+\s*references\b', text)
    listed=set(re.findall(r'(?m)^\s*\[?(\d+)\]?\.', refsec[1])) if len(refsec)>1 else set()
    orphan_cite=cites-listed; orphan_ref=listed-cites
    ok=bool(cites or listed) and not orphan_cite and not orphan_ref
    return ('GUARANTEE','gate_cite_ref_reconcile', ok,
            f"cited-not-listed={sorted(orphan_cite)[:5]}, listed-not-cited={sorted(orphan_ref)[:5]}" if (cites or listed) else "no reconcilable citation system")

def gate_quote_anchor(text):
    quotes=re.findall(r'[""][^""]{15,}[""]', text)
    anchored=sum(1 for q in quotes if re.search(r'p\.?\s*\d+|page\s*\d+', text[text.find(q):text.find(q)+120]))
    ok = (not quotes) or anchored==len(quotes)
    return ('GUARANTEE','gate_quote_anchor', ok, f"{len(quotes)} quotes, {anchored} with page anchor")

def gate_figure_ref(text):
    captions=set(re.findall(r'(?im)^(?:figure|table)\s+(\d+)', text))
    refs=set(re.findall(r'\b(?:Figure|Table)\s+(\d+)', text))
    # captions also counted as refs; unreferenced = caption nums never cited in prose
    prose_refs=set(re.findall(r'(?<!^)(?:Figure|Table)\s+(\d+)', text))
    unref=captions-prose_refs
    ok=not unref
    return ('GUARANTEE','gate_figure_ref', ok, f"{len(captions)} figures/tables, unreferenced: {sorted(unref)[:5]}" if captions else "no numbered figures/tables")

def gate_section_structure(text, profile):
    heads=[h.lower() for h in re.findall(r'(?im)^#+\s*(.+)$', text)]
    required=['introduction','conclusion'] if profile=='ReadableDraft' else ['abstract','introduction','conclusion','limitation']
    present=[r for r in required if any(r in h for h in heads)]
    missing=[r for r in required if r not in present]
    return ('GUARANTEE','gate_section_structure', not missing, f"missing required sections: {missing}" if missing else "required sections present")

def gate_heading_hierarchy(text):
    levels=[len(m.group(1)) for m in re.finditer(r'(?m)^(#+)\s', text)]
    skips=sum(1 for i in range(1,len(levels)) if levels[i]-levels[i-1]>1)
    return ('GUARANTEE','gate_heading_hierarchy', skips==0, f"{skips} heading-level skips")

# ---------- TIER B (FLAG, proxy) ----------
def gate_readability(text, low, high):
    sents=sentences(text); ws=words(text)
    if not sents or not ws: return ('FLAG','gate_readability', False, "no prose")
    syl=sum(syllables(w) for w in ws)
    fk=0.39*(len(ws)/len(sents))+11.8*(syl/len(ws))-15.59
    return ('FLAG','gate_readability', low<=fk<=high, f"FK grade {fk:.1f} (band {low}-{high}) — PROXY, not comprehension")

def gate_register(text):
    ws=words(text); n=max(1,len(ws))/1000
    hedges=len(re.findall(r'\b(may|might|could|suggest|appears?|likely|generally|tend(s|ed)?|often|typically)\b', text, re.I))
    firstp=len(re.findall(r'\b(I|we|our|us|my)\b', text))
    hd=hedges/n; fp=firstp/n
    ok = hd>=2 and fp<=15
    return ('FLAG','gate_register', ok, f"hedging {hd:.1f}/1k (floor 2), first-person {fp:.1f}/1k (ceil 15) — PROXY")

def gate_sentence(text):
    sents=sentences(text)
    frags=sum(1 for s in sents if len(words(s))>=3 and not re.search(r'\b(is|are|was|were|has|have|had|do|does|did|can|will|would|should|must|provides?|requires?|defines?|describes?|reduces?|measures?|ensures?|enables?)\b', s, re.I))
    rate=frags/max(1,len(sents))
    return ('FLAG','gate_sentence', rate<0.25, f"{frags}/{len(sents)} possible fragments ({rate:.0%}) — proxy")

# ---------- TIER C (REQUIRE attestation — never auto-PASS) ----------
def attest_cohesion(text):
    paras=[p for p in text.split('\n\n') if len(words(p))>25]
    return ('REQUIRE','attest_cohesion', None, f"{len(paras)} substantive paragraphs — human must confirm topic-sentence + given-new flow")
def attest_terminology(text):
    return ('REQUIRE','attest_terminology', None, "synonym-switch scan reported separately; human confirms one-concept-one-term")
def attest_warrant(text):
    return ('REQUIRE','attest_warrant', None, "citation→claim support is Tier-C; requires hash-bound content-correctness attestation")
def attest_calibration(text):
    return ('REQUIRE','attest_calibration', None, "claim-to-evidence calibration is human-only")
def attest_soundness(text):
    return ('REQUIRE','attest_soundness', None, "logical soundness + contribution is human-only")

def run(path, profile='SeminalDoc', fk_low=11, fk_high=16):
    t=load(path)
    A=[gate_abbrev_firstuse(t),gate_abbrev_list(t),gate_intext_citations(t),gate_reference_list(t),
       gate_cite_ref_reconcile(t),gate_quote_anchor(t),gate_figure_ref(t),gate_section_structure(t,profile),
       gate_heading_hierarchy(t)]
    B=[gate_readability(t,fk_low,fk_high),gate_register(t),gate_sentence(t)]
    C=[attest_cohesion(t),attest_terminology(t),attest_warrant(t),attest_calibration(t),attest_soundness(t)]
    def show(group,res):
        print(f"\n=== TIER {group} ===")
        for verb,name,ok,msg in res:
            tag = ('PASS' if ok else 'FAIL') if ok is not None else 'REQUIRES_ATTESTATION'
            print(f"  [{tag:20}] {name}: {msg}")
    show('A — GUARANTEE',A); show('B — FLAG (proxy)',B); show('C — REQUIRE attestation',C)
    a_pass=sum(1 for _,_,ok,_ in A if ok); a_tot=len(A)
    b_pass=sum(1 for _,_,ok,_ in B if ok)
    print(f"\n=== VERDICT (profile={profile}) ===")
    print(f"  Tier-A apparatus GUARANTEED: {a_pass}/{a_tot} pass")
    print(f"  Tier-B register FLAGGED: {b_pass}/{len(B)} clean")
    print(f"  Tier-C: {len(C)} items REQUIRE attestation (cannot be auto-certified)")
    print(f"  DOCUMENT STATUS: {'apparatus-floor MET' if a_pass==a_tot else 'apparatus-floor NOT met — '+str(a_tot-a_pass)+' Tier-A failures'}; "
          f"seminal/teaching certification BLOCKED pending {len(C)} attestations")
    return {'A':[(n,ok,m) for _,n,ok,m in A],'B':[(n,ok,m) for _,n,ok,m in B],'C':[(n,m) for _,n,_,m in C]}

if __name__=='__main__':
    args=sys.argv[1:]; path=args[0]
    prof='SeminalDoc'
    if '--profile' in args: prof=args[args.index('--profile')+1]
    res=run(path, prof)
    json.dump(res, open(path.replace('.md','_docgate.json'),'w'), indent=1)
