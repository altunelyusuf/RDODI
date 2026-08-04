#!/usr/bin/env python3
"""
reference_verification_gate_v1_0_0.py — reuses the pipeline's R11 tier-maximizing resolution
(ch9_reference_resolution_tiered) as a live gate. For each reference in a report it queries REAL
bibliographic authorities (Crossref, Open Library) highest-tier-first; a reference that resolves is
KEPT with its verified identifier+tier; one that does NOT resolve is ELIMINATED (not asserted as real).
This is the anti-fake-reference check: reconstructed citations that cannot be confirmed are removed.
"""
import urllib.request, urllib.parse, json, re, sys, time

def crossref(title, author=None, year=None):
    """Definitive/High tier: Crossref. STRICT: title overlap AND author AND year must agree."""
    q=urllib.parse.urlencode({'query.bibliographic':f"{title} {author or ''}",'rows':8})
    url=f"https://api.crossref.org/works?{q}"
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'RDODI-refcheck/1.0 (mailto:research@example.org)'})
        with urllib.request.urlopen(req,timeout=25) as r: d=json.load(r)
        for item in d.get('message',{}).get('items',[]):
            it_title=' '.join(item.get('title',[])).lower()
            if not it_title: continue
            tt=set(re.findall(r'[a-z]+',title.lower())); ot=set(re.findall(r'[a-z]+',it_title))
            # STRICT title: most of the query title's content words must be present
            content=tt-{'the','of','a','and','to','in','for','quality'}  # 'quality' too common to discriminate
            if not content or len(content&ot)<max(2,len(content)*0.7): continue
            # YEAR must match (±1) if we have one
            iy=(item.get('issued',{}).get('date-parts',[[None]])[0][0])
            if year and iy and abs(int(iy)-int(year))>1: continue
            # AUTHOR must match if we have one
            if author:
                surnames=' '.join(a.get('family','') for a in item.get('author',[])).lower()
                if author.split(',')[0].split()[-1].lower() not in surnames: continue
            return {'tier':'Definitive','authority':'Crossref','doi':item.get('DOI'),
                    'title':' '.join(item.get('title',[])),'year':iy}
    except Exception as e:
        return {'error':str(e)[:60]}
    return None

def openlibrary(title, author=None):
    """High tier: Open Library (catalogue)."""
    q=urllib.parse.urlencode({'title':title,'limit':5})
    url=f"https://openlibrary.org/search.json?{q}"
    try:
        with urllib.request.urlopen(url,timeout=25) as r: d=json.load(r)
        for doc in d.get('docs',[]):
            dt=doc.get('title','').lower()
            tt=set(re.findall(r'[a-z]+',title.lower())); ot=set(re.findall(r'[a-z]+',dt))
            content=tt-{'the','of','a','and','to','in','for','quality'}
            if not content or len(content&ot)<max(2,len(content)*0.7): continue
            # author must match
            ok_author=True
            if author:
                an=' '.join(doc.get('author_name',[])).lower()
                ok_author = author.split(',')[0].split()[-1].lower() in an
            # year must match (±1)
            fy=doc.get('first_publish_year')
            ok_year = (not year) or (not fy) or abs(int(fy)-int(year))<=1
            if ok_author and ok_year:
                return {'tier':'High','authority':'OpenLibrary','olid':doc.get('key'),
                        'title':doc.get('title'),'year':fy,
                        'isbn':(doc.get('isbn',[None])[0] if doc.get('isbn') else None)}
    except Exception as e:
        return {'error':str(e)[:60]}
    return None

def parse_references(text):
    """extract reference entries from a References section."""
    m=re.split(r'(?im)^#+\s*references\b', text)
    if len(m)<2: return []
    block=m[1]
    refs=[]
    for line in re.findall(r'(?m)^\s*\d+\.\s*(.+)', block):
        # parse: Author (Year). *Title*. Publisher.
        ym=re.search(r'\((\d{4})\)', line)
        tm=re.search(r'\*([^*]+)\*', line) or re.search(r'\.\s*([A-Z][^.]{8,})\.', line)
        am=re.match(r'^([^(]+?)\s*\(', line)
        refs.append({'raw':line.strip(),'author':am.group(1).strip() if am else None,
                     'title':tm.group(1).strip() if tm else line[:40],'year':ym.group(1) if ym else None})
    return refs

def resolve(ref):
    """R11 tier-maximizing: Definitive (Crossref) first, then High (OpenLibrary), then Unresolvable."""
    title=ref['title']
    c=crossref(title, ref.get('author'), ref.get('year'))
    if c and 'error' not in c and c: return {'verdict':'RESOLVED','via':c}
    time.sleep(0.5)
    o=openlibrary(title, ref.get('author'))
    if o and 'error' not in o and o: return {'verdict':'RESOLVED','via':o}
    return {'verdict':'UNRESOLVABLE','via':None}

def run(path):
    text=open(path,encoding='utf-8').read()
    refs=parse_references(text)
    print(f"=== REFERENCE VERIFICATION GATE (R11 tier-maximizing, live catalogues) ===")
    print(f"  references parsed: {len(refs)}\n")
    kept=[]; eliminated=[]
    for r in refs:
        res=resolve(r)
        if res['verdict']=='RESOLVED':
            v=res['via']
            print(f"  [RESOLVED   {v['tier']:10}] {r['title'][:45]}")
            print(f"               via {v['authority']}: {v.get('doi') or v.get('olid') or v.get('isbn')} (year {v.get('year')})")
            kept.append({**r,'resolution':v})
        else:
            print(f"  [ELIMINATED unverifiable] {r['title'][:45]} — no catalogue match; reconstructed/fake -> REMOVED")
            eliminated.append(r)
    print(f"\n  VERDICT: {len(kept)} verified-kept, {len(eliminated)} eliminated-as-unverifiable")
    print(f"  (eliminated references are reconstructed-and-unconfirmed; asserting them = fake rigor)")
    json.dump({'kept':kept,'eliminated':eliminated}, open(path.replace('.md','_refcheck.json'),'w'), indent=1, default=str)
    return kept, eliminated

if __name__=='__main__':
    run(sys.argv[1])
