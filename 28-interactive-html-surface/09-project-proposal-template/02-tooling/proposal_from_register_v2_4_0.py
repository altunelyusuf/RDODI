#!/usr/bin/env python3
"""proposal_from_register_v2_4_0.py (v2.4.0: every project-bound table and the abbreviations dictionary read from 04-documentation/proposal_project_data_v*.json — the code no longer carries this project's data; the frozen-snapshot fallback needs --allow-snapshot)

proposal_from_register_v2_3_0.py (v2.3.0: goal facings from the register — mission-achievement, scope-coverage and guard goals presented separately; learning objectives keyed by goal identifier; any number of packages)

proposal_from_register_v2_2_0.py (v2.2.0: iteration windows and dated milestones from the register)

proposal_from_register_v2_1_0.py — build the Stage 3 proposal from the register, in the shape the

v2.1.0: the register and the pipeline ontology live in altunelyusuf/SCAMPS (migrated 2026-09-10). The generator
reads them from the checkout named by $SCAMPS_ROOT, verified against SCAMPS_PIN.txt (commit + file hashes); it
refuses to build from an unpinned checkout. Without $SCAMPS_ROOT it reads the frozen proposal-stage snapshot
under 05-lineage/ and 01-ontologies/ and says so on the document's provenance line.
RDODI project-proposal profile and documentation standards require.

v2.0.0 replaces v1.0.0 after the owner's review of the v3.0.0 document: numbering now starts at 1 (RDODI
profile #5 template v1.4.0: 18 mandatory sections, numbered from 1); the body is cohesive prose with numbered
citations, an abstract, a list of abbreviations, limitations and a conclusion (RDODI Documentation Standards
v1.0.0, Tier A); and every register table, the ontology alignment, the external dependency and the lineage
witness live in lettered appendices. The generator emits the document first as Markdown so that the RDODI
Tier-A gates can be run on it, then renders the same blocks to .docx. Both outputs are generated artefacts:
regenerate them, never hand-edit them (L-112 file class c).

Usage, from the package root:
  SCAMPS_ROOT=<checkout> python3 03-tooling/proposal_from_register_v2_4_0.py --out 04-documentation/vaf_ap_stage3_proposal_vX_Y_Z.docx
Writes the .docx and, beside it, the .md the gates were run on. Needs rdflib and node with `docx`.
"""
import argparse, datetime, glob, json, os, re, subprocess, sys
import rdflib
from rdflib import RDF, RDFS, Namespace

B = Namespace('http://example.org/backlog#')
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
VAP = Namespace('http://example.org/vaf-agentic-pipeline#')
SCAMPS_NS = Namespace('http://example.org/scamps#')

def register_root():
    """Where the register and ontology are read from: the pinned SCAMPS checkout, or the frozen snapshot."""
    root = os.environ.get('SCAMPS_ROOT')
    if not root:
        if os.environ.get('ALLOW_SNAPSHOT') != '1': raise SystemExit('SCAMPS_ROOT is not set. The register lives in altunelyusuf/SCAMPS (see SCAMPS_PIN.txt); the frozen snapshot under 05-lineage/ is a record, not a source. Set SCAMPS_ROOT, or ALLOW_SNAPSHOT=1 to build knowingly from the snapshot.')
        return None
    import hashlib, subprocess
    pin = {}; commit = None
    for line in open('SCAMPS_PIN.txt'):
        line = line.strip()
        if line.startswith('commit '): commit = line.split()[1]
        elif re.match(r'^[0-9a-f]{64}\s', line): h, f = line.split(None, 1); pin[f.strip()] = h
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True).stdout.strip()
    bad = [f for f, h in pin.items() if not os.path.exists(os.path.join(root, f)) or hashlib.sha256(open(os.path.join(root, f), 'rb').read()).hexdigest() != h]
    if head != commit or bad: raise SystemExit('SCAMPS checkout does not match SCAMPS_PIN.txt (commit %s vs %s; %d file mismatches) — refusing to generate from an unpinned register' % (head[:7], (commit or '')[:7], len(bad)))
    return root

def paths():
    root = register_root()
    if root: return {'lineage': os.path.join(root, '08-lineage'), 'onto': os.path.join(root, '01-ontologies'), 'label': 'altunelyusuf/SCAMPS @ ' + open('SCAMPS_PIN.txt').read().split('commit ')[1].split()[0][:12]}
    return {'lineage': '05-lineage', 'onto': '01-ontologies', 'label': 'frozen proposal-stage snapshot in this package (SCAMPS_ROOT not set)'}

def local(u): return str(u).split('#')[-1]
def s(v): return '' if v is None else str(v)
def highest(pattern):
    fs = glob.glob(pattern)
    if not fs: raise SystemExit('no file matches ' + pattern)
    fs.sort(key=lambda n: [int(i) for i in re.findall(r'_v(\d+)_(\d+)_(\d+)', n)[0]])
    return fs[-1]
def lab(g, x): return s(g.value(x, RDFS.label)) or local(x)
def defn(g, x): return s(g.value(x, SKOS.definition))
def objs(g, x, p): return sorted(g.objects(x, p), key=str)
def ordered(g, cls): return sorted(g.subjects(RDF.type, cls), key=lambda x: lab(g, x))
def strip(v, pre): return v.replace(pre, '') if v else v

# ------------------------------------------------------------------ register model
def load():
    P_ = paths(); g = rdflib.Graph()
    for f in sorted(glob.glob(os.path.join(P_['lineage'], '*.ttl'))): g.parse(f)
    g.parse(highest(os.path.join(P_['onto'], 'vaf_ap_blueprint_v*_*_*.ttl')))
    t = rdflib.Graph()
    if os.environ.get('SCAMPS_ROOT'):
        t.parse(highest(os.path.join(P_['onto'], 'scamps_vocabulary_v*_*_*.ttl'))); t.parse(highest(os.path.join(P_['onto'], 'scamps_pipeline_abox_v*_*_*.ttl')))
    else:
        t.parse(highest(os.path.join(P_['onto'], 'vaf_ap_tbox_v*_*_*.ttl'))); t.parse(highest(os.path.join(P_['onto'], 'vaf_ap_abox_v*_*_*.ttl')))
    return g, t

def project_ns():
    return SCAMPS_NS if os.environ.get('SCAMPS_ROOT') else VAP

def build(g, t):
    m = {}
    mission = next(g.subjects(RDF.type, B.Mission))
    m['mission'] = {'label': lab(g, mission), 'statement': s(g.value(mission, B.hasMissionStatement)), 'definition': defn(g, mission), 'origin': strip(local(g.value(mission, B.hasMissionOrigin) or ''), 'Origin_')}
    scope = next(g.subjects(RDF.type, B.ScopeStatement))
    m['scope'] = {'label': lab(g, scope), 'definition': defn(g, scope)}
    m['areas'] = [{'id': local(a), 'label': lab(g, a), 'location': s(g.value(a, B.areaLocation)), 'measure': s(g.value(a, B.areaMeasure)), 'layer': strip(local(g.value(a, B.hasScopeLayer) or ''), 'Layer_')} for a in ordered(g, B.ScopeArea)]
    m['deliverables'] = [{'id': local(d), 'label': lab(g, d), 'area': lab(g, g.value(d, B.deliverableForArea)) if g.value(d, B.deliverableForArea) else ''} for d in ordered(g, B.ScopeDeliverable)]
    m['exclusions'] = [{'id': local(e), 'label': lab(g, e), 'rationale': s(g.value(e, B.hasExclusionRationale)), 'concern': s(g.value(e, B.excludesConcern))} for e in ordered(g, B.ScopeExclusion)]
    m['goals'] = [{'id': local(x), 'label': lab(g, x), 'definition': defn(g, x), 'facing': strip(local(g.value(x, B.hasGoalFacing) or ''), 'Facing_'), 'metric': s(g.value(x, B.hasMetricName)), 'target': s(g.value(x, B.hasTargetValue)),
                   'areas': ', '.join(lab(g, d) for d in objs(g, x, B.goalCoversArea)), 'guards': ', '.join(lab(g, d) for d in objs(g, x, B.guardsExclusion))} for x in ordered(g, B.Goal)]
    items = {}
    for w in ordered(g, B.Feature):
        items[local(w)] = {'id': local(w), 'ident': s(g.value(w, B.hasIdentifier)).replace('VAFAP-', ''), 'label': lab(g, w), 'definition': defn(g, w), 'state': local(g.value(w, B.hasState) or ''),
            'category': strip(local(g.value(w, B.hasInvestmentCategory) or ''), 'Cat_'), 'objectives': ', '.join(lab(g, d) for d in objs(g, w, B.pursuesObjective)),
            'deliverables': ', '.join(lab(g, d) for d in objs(g, w, B.satisfiesDeliverable)), 'milestone': ', '.join(lab(g, d) for d in objs(g, w, B.contributesToMilestone)),
            'horizon': ', '.join(local(d) for d in objs(g, w, B.scheduledInHorizon)), 'external': bool(list(g.objects(w, B.dependsOnExternal))), 'needs_upstream': bool(list(g.objects(w, B.requiresExternalEnhancement))),
            'entities': ', '.join(lab(g, d) for d in objs(g, w, B.coversEntity))}
    m['items'] = items
    def wl(wid): return items[local(wid)]['label'] if local(wid) in items else (local(wid) if str(wid).startswith('http') else str(wid))
    m['objectives'] = []
    for x in ordered(g, B.Objective):
        cp = g.value(x, B.hasCheckpoint)
        m['objectives'].append({'id': local(x), 'label': lab(g, x), 'metric': s(g.value(x, B.hasSuccessMetric)), 'kind': strip(local(g.value(x, B.hasMeasurementKind) or ''), 'Meas_'), 'baseline': s(g.value(x, B.hasBaselineValue)), 'target': s(g.value(x, B.hasTargetValue)),
            'direction': strip(local(g.value(x, B.hasTargetDirection) or ''), 'Dir_'), 'goals': ', '.join(lab(g, d) for d in objs(g, x, B.contributesToGoal)), 'checkpoint': wl(s(g.value(cp, B.checkpointCondition))) if cp else '', 'outcome': strip(local(g.value(x, B.objectiveOutcome) or ''), 'Ach_')})
    m['packages'] = []
    for p in sorted(g.subjects(RDF.type, B.Package), key=lambda x: [int(i) for i in re.findall(r'\d+', s(g.value(x, B.hasPackageVersion)) or '999')]):
        m['packages'].append({'id': local(p), 'label': lab(g, p), 'definition': defn(g, p), 'version': s(g.value(p, B.hasPackageVersion)), 'iterations': ', '.join(lab(g, d) for d in objs(g, p, B.targetsIteration)), 'members': [local(x) for x in objs(g, p, B.hasMember)]})
    m['iterations'] = [{'id': local(i), 'label': lab(g, i), 'goal': s(g.value(i, B.hasSprintGoal)), 'start': s(g.value(i, B.iterationStart))[:10], 'end': s(g.value(i, B.iterationEnd))[:10], 'capacity': s(g.value(i, B.hasCapacity)), 'committed': s(g.value(i, B.hasCommittedEffort)), 'duration_source': s(g.value(i, B.hasDurationSource)), 'members': [local(x) for x in objs(g, i, B.hasMember)]} for i in ordered(g, B.Iteration)]
    m['milestones'] = sorted([{'id': local(x), 'label': lab(g, x), 'definition': defn(g, x), 'date': s(g.value(x, B.hasTargetDate))[:10], 'outcome': strip(local(g.value(x, B.milestoneOutcome) or ''), 'Ach_'), 'items': [k for k, v in items.items() if lab(g, x) in v['milestone']]} for x in g.subjects(RDF.type, B.Milestone)], key=lambda x: x['date'])
    rm = next(g.subjects(RDF.type, B.Roadmap))
    m['roadmap'] = {'label': lab(g, rm), 'definition': defn(g, rm), 'realises': ', '.join(lab(g, d) for d in objs(g, rm, B.roadmapRealises))}
    m['horizons'] = {}
    for v in items.values():
        for h in v['horizon'].split(', '):
            if h: m['horizons'].setdefault(h, []).append(v['id'])
    ed = next(g.subjects(RDF.type, B.ExternalDependency))
    m['external'] = {'label': lab(g, ed), 'definition': defn(g, ed), 'type': strip(local(g.value(ed, B.hasExternalDependencyType) or ''), 'Ext_'), 'party': s(g.value(ed, B.hasExternalParty)),
                     'dependants': sorted(local(w) for w in g.subjects(B.dependsOnExternal, ed)), 'needing_upstream': sorted(local(w) for w in g.subjects(B.requiresExternalEnhancement, ed))}
    m['proposals'] = [{'id': local(p), 'label': lab(g, p), 'status': strip(local(g.value(p, B.hasProposalStatus) or ''), 'Prop_'), 'change': s(g.value(p, B.hasRequestedChange)), 'submitted_to': s(g.value(p, B.submittedTo)), 'raised': s(g.value(p, B.proposalRaisedAt))[:10], 'unblocks': ', '.join(lab(g, d) for d in objs(g, p, B.unblocksItem))} for p in ordered(g, B.EnhancementProposal)]
    dd = next(g.subjects(RDF.type, B.DependencyDisclosure), None)
    m['disclosure'] = s(g.value(dd, B.hasDisclosureSource)) if dd else ''
    m['dod'] = [{'definition': defn(g, c), 'query': s(g.value(c, B.hasCheckQuery)), 'expected': s(g.value(c, B.hasExpectedResult)), 'status': local(g.value(c, B.hasCriterionStatus) or '')} for c in ordered(g, B.DoDCriterion)]
    bp = next(g.subjects(RDF.type, B.Blueprint))
    m['blueprint'] = {'label': lab(g, bp), 'definition': defn(g, bp), 'entities': [{'label': lab(g, e), 'definition': defn(g, e), 'match': ', '.join(local(x) for x in objs(g, e, SKOS.closeMatch))} for e in ordered(g, B.DomainEntity)]}
    m['gaps'] = [{'label': lab(g, x), 'entity': lab(g, g.value(x, B.gapForEntity)) if g.value(x, B.gapForEntity) else '', 'stage': strip(local(g.value(x, B.gapForStage) or ''), 'Stage_'), 'reason': s(g.value(x, B.hasGapReason))} for x in ordered(g, B.BlueprintGap)]
    m['obligations'] = [{'label': lab(g, x), 'definition': defn(g, x)} for x in ordered(g, B.ComplianceObligation)]
    order = ['Stage_Mission', 'Stage_Scope', 'Stage_Goal', 'Stage_Objective', 'Stage_Backlog']
    outs = [o for o in g.subjects(RDF.type, B.StageOutput) if s(g.value(o, B.outputRetracted)) != 'true']
    m['stage_outputs'] = sorted([{'stage': strip(local(g.value(o, B.outputOfStage) or ''), 'Stage_'), 'commit': s(g.value(o, B.closedAtCommit)), 'note': s(g.value(o, B.note))} for o in outs], key=lambda x: order.index('Stage_' + x['stage']) if 'Stage_' + x['stage'] in order else 99)
    # project TBox concepts and their alignment
    NS = project_ns(); m['tbox'] = []
    for c in sorted(t.subjects(RDF.type, rdflib.OWL.Class), key=str):
        if str(c).startswith(str(NS)):
            m['tbox'].append({'label': lab(t, c), 'match': ', '.join(local(x) for x in objs(t, c, SKOS.closeMatch)), 'definition': defn(t, c) or s(t.value(c, RDFS.comment))})
    AGDEV = Namespace('http://example.org/agentic-sdlc#'); VA = Namespace('http://example.org/variant-algebra#')
    for i in sorted(t.subjects(RDF.type, AGDEV.AgentRole), key=str):
        m['tbox'].append({'label': lab(t, i), 'match': 'agdev:AgentRole' + (' · ' + ', '.join(local(x) for x in objs(t, i, RDFS.seeAlso)) if list(objs(t, i, RDFS.seeAlso)) else ''), 'definition': defn(t, i)})
    for i in sorted(t.subjects(RDF.type, AGDEV.AgentTeam), key=str):
        m['tbox'].append({'label': lab(t, i), 'match': 'agdev:AgentTeam · ' + ', '.join(local(x) for x in objs(t, i, RDFS.seeAlso)), 'definition': defn(t, i)})
    m['tbox_props'] = [{'label': lab(t, p), 'definition': defn(t, p) or s(t.value(p, RDFS.comment))} for p in sorted(set(t.subjects(RDF.type, rdflib.OWL.ObjectProperty)) | set(t.subjects(RDF.type, rdflib.OWL.DatatypeProperty)), key=str) if str(p).startswith(str(NS))]
    m['counts'] = {'goals': len(m['goals']), 'objectives': len(m['objectives']), 'areas': len(m['areas']), 'deliverables': len(m['deliverables']), 'exclusions': len(m['exclusions']), 'items': len(items), 'packages': len(m['packages']), 'iterations': len(m['iterations']), 'milestones': len(m['milestones']), 'proposals': len(m['proposals']), 'gaps': len(m['gaps']), 'states': {st: sum(1 for v in items.values() if v['state'] == st) for st in sorted({v['state'] for v in items.values()})}}
    m['gaps_semantic'] = sum(1 for x in m['gaps'] if 'semantic' in (x['label'] + x['entity']).lower())
    return m

# ------------------------------------------------------------------ blocks
def H(level, text): return {'h': level, 'text': text}
def P(text, **k): d = {'p': text}; d.update(k); return d
class Tables:
    def __init__(self): self.n = 0; self.num = {}; self.defs = {}
    def define(self, key, caption, header, rows, widths=None):
        self.defs[key] = {'caption': caption, 'header': header, 'rows': [[calm(s(c)) for c in r] for r in rows], 'widths': widths}
    def number(self, key):
        if key not in self.num: self.n += 1; self.num[key] = self.n
        return self.num[key]
    def block(self, key):
        d = self.defs[key]; n = self.number(key)
        return {'table': d, 'caption': 'Table %d. %s' % (n, d['caption'])}

def sentences(m):
    wl = lambda i: m['items'][i]['label']
    areas = 'the areas are ' + '; '.join('%s, measured as %s' % (a['label'].lower(), a['measure'].split(';')[0].split(',')[0].lower()) for a in m['areas'])
    excl = ' and '.join('%s, because %s' % (e['label'].lower(), e['rationale'].split('.')[0].replace('Excluded because ', '').replace('excluded because ', '')) for e in m['exclusions'])
    mg = [g for g in m['goals'] if g['facing'] == 'Mission']; sg = [g for g in m['goals'] if g['facing'] == 'Scope']; gg = [g for g in m['goals'] if g['facing'] in ('Containment', 'Exclusion')]
    goals = 'The %d mission-achievement goals state what the mission will have delivered, one per clause of the mission statement: ' % len(mg) + '; '.join('%s, measured by %s with a target of %s' % (g['label'].lower(), g['metric'].lower(), g['target']) for g in mg) + '. '
    goals += 'The %d scope-coverage goals state the finish condition of each scope area, with the target the scope itself declares: ' % len(sg) + '; '.join('%s (%s, target %s)' % (g['label'].lower(), g['metric'].lower(), g['target']) for g in sg) + '. '
    goals += 'The %d remaining goals are guards, not achievements — %s — kept because the framework requires a containment-facing goal and one exclusion-facing goal per exclusion, and named as guards so that they are not mistaken for aims.' % (len(gg), '; '.join(g['label'].lower() for g in gg))
    objs_ = ' '.join('The objective %s is measured by %s, moving from a baseline of %s to a target of %s, with its checkpoint at the work item %s.' % (o['label'], o['metric'].lower() if o['metric'] else 'a counted measure', o['baseline'], o['target'], o['checkpoint']) for o in m['objectives'])
    pk = ' '.join('The package %s (release %s, %s) holds %d items and %s' % (p['label'], p['version'], p['iterations'].lower(), len(p['members']), p['definition'][0].lower() + p['definition'][1:].split('. ')[0] + '.') for p in m['packages'])
    hz = ', '.join('%d items in %s' % (len(m['horizons'].get(h, [])), h) for h in ['Now', 'Next', 'Later'])
    return {'areas.sentence': areas, 'exclusions.sentence': excl, 'goals.sentence': goals, 'objectives.sentence': objs_, 'packages.sentence': pk, 'horizons.sentence': hz}

def project_data():
    return json.load(open(highest('04-documentation/proposal_project_data_v*_*_*.json'), encoding='utf-8'))

def resolve(m, text):
    """{wi:ID} → work item label; {goal:ID} → goal label; {goals_facing:F} → labels of goals with that facing; {external_blocked}; {gaps_semantic}. Unknown names fail the build."""
    def wi(mm):
        i = mm.group(1)
        if i not in m['items']: raise SystemExit('project data names an unknown work item: ' + i)
        return m['items'][i]['label']
    def goal(mm):
        for g in m['goals']:
            if g['id'] == mm.group(1): return g['label']
        raise SystemExit('project data names an unknown goal: ' + mm.group(1))
    text = re.sub(r'\{wi:([A-Za-z0-9_]+)\}', wi, text); text = re.sub(r'\{goal:([A-Za-z0-9_]+)\}', goal, text)
    text = re.sub(r'\{goals_facing:([A-Za-z]+)\}', lambda mm: '; '.join(g['label'] for g in m['goals'] if g['facing'] == mm.group(1)), text)
    text = text.replace('{external_blocked}', '; '.join(m['items'][w]['label'] for w in m['external']['needing_upstream'])).replace('{gaps_semantic}', str(m['gaps_semantic']))
    return text

def wl_goal(m, gid):
    for g in m['goals']:
        if g['id'] == gid: return g['label']
    return gid

def define_tables(m, T):
    PD = project_data(); R = lambda rows: [[resolve(m, c) for c in r] for r in rows]
    wl = lambda i: m['items'][i]['label']
    wids = lambda ids: '; '.join(wl(i) for i in ids)
    sat = lambda d: [k for k, v in m['items'].items() if d['label'] in v['deliverables']]
    T.define('gap', 'Gap between the current and the desired state, by scope deliverable', ['Area', 'Current state', 'Desired state (register deliverable)', 'Addressed by'], [[d['area'], 'No formal mechanism', d['label'], wids(sat(d))] for d in m['deliverables']], [1500, 1500, 3200, 3200])
    T.define('fr', 'Functional requirements, traced to the work items that satisfy them', ['Requirement', 'Statement', 'Area', 'Satisfying work items'], [['FR-%d' % (i + 1), d['label'], d['area'], wids(sat(d))] for i, d in enumerate(m['deliverables'])], [1000, 3100, 1700, 3600])
    rows = [['NFR-%d' % (i + 1), 'Compliance obligation', o['label'], o['definition']] for i, o in enumerate(m['obligations'])]
    rows += [['NFR-%d' % (len(m['obligations']) + i + 1), 'Definition of Done', d['definition'], 'Expected result %s; status %s' % (d['expected'], d['status'])] for i, d in enumerate(m['dod'])]
    T.define('nfr', 'Non-functional requirements: compliance obligations and Definition of Done criteria', ['Requirement', 'Kind', 'Statement', 'Detail'], rows, [1000, 1500, 3400, 3500])
    T.define('packages', 'Roadmap packages, their release versions and their work items', ['Package', 'Release', 'Iteration', 'Work items'], [[p['label'], p['version'], p['iterations'], wids(p['members'])] for p in m['packages']], [2400, 900, 1100, 5000])
    T.define('team', 'Proposed team allocation by roadmap package', ['Member', 'Role', 'Owns package', 'Hours per week'], [['Student %s (TBD)' % chr(65 + k), 'Package owner', p['label'], 'TBD'] for k, p in enumerate(m['packages'])] + R(PD['team_extra_rows']), [2400, 2200, 3000, 1800])
    T.define('milestones', 'Milestones with target dates and the condition for reaching them', ['Milestone', 'Target date', 'Reached when', 'Outcome'], [[x['label'], x['date'], x['definition'], x['outcome']] for x in m['milestones']], [2200, 1100, 5000, 1100])
    T.define('risks', 'Risks visible in the register and their mitigations', ['Risk', 'Description', 'Register element affected', 'Mitigation'], R(PD['risks']), [700, 2600, 3000, 3100])
    T.define('deliverables', 'Deliverables, the milestone each contributes to and its acceptance condition', ['Deliverable', 'Statement', 'Milestone', 'Acceptance'], [['D-%d' % (i + 1), d['label'], '; '.join(sorted({m['items'][k]['milestone'] for k in sat(d)} - {''})), 'All satisfying work items Done under the Definition of Done'] for i, d in enumerate(m['deliverables'])], [900, 3400, 2600, 2500])
    # appendices
    T.define('a_institution', 'Institutional information', ['Field', 'Value'], PD['institution'], [3000, 6400])
    T.define('a_lo', 'Learning objectives aligned to register goals', ['Objective', 'Statement', 'Bloom level', 'Assessment', 'Register goal'], R(PD['learning_objectives']), [900, 3600, 1000, 2100, 1800])
    T.define('a_academic_ms', 'Academic milestones aligned to register milestones', ['Academic milestone', 'Register milestone', 'Target date', 'Weight'], [PD['academic_milestones_first']] + [['Progress review %d' % (i + 1) if i < len(m['milestones']) - 1 else 'Final presentation and report', x['label'], x['date'], PD['academic_milestone_weights'][i] if i < len(PD['academic_milestone_weights']) else ''] for i, x in enumerate(m['milestones'])], [2400, 3800, 1600, 1600])
    T.define('a_peer', 'Peer evaluation criteria', ['Criterion', 'Weight', 'Description'], PD['peer_evaluation'], [2200, 1200, 6000])
    T.define('b_areas', 'Scope areas', ['Area', 'Where it lives', 'Measure', 'Layer'], [[a['label'], a['location'], a['measure'], a['layer']] for a in m['areas']], [2000, 3600, 2800, 1000])
    T.define('b_deliverables', 'Scope deliverables and the work items that satisfy them', ['Deliverable', 'Area', 'Satisfying work items'], [[d['label'], d['area'], wids(sat(d))] for d in m['deliverables']], [3200, 1800, 4400])
    T.define('b_exclusions', 'Scope exclusions with rationale', ['Exclusion', 'Concern excluded', 'Rationale'], [[e['label'], e['concern'], e['rationale']] for e in m['exclusions']], [2000, 2400, 5000])
    T.define('b_goals', 'Goals with facing, metric, target, coverage and guarded exclusions (mission-achievement first, then scope-coverage, then guards)', ['Goal', 'Facing', 'Metric', 'Target', 'Covers or guards', 'Definition'], [[g['label'], g['facing'], g['metric'], g['target'], g['areas'] + ((' Guards: ' + g['guards']) if g['guards'] else ''), g['definition']] for g in sorted(m['goals'], key=lambda g: {'Mission': 0, 'Scope': 1, 'Containment': 2, 'Exclusion': 3}.get(g['facing'], 9))], [1700, 900, 1700, 700, 2200, 2200])
    T.define('b_objectives', 'Objectives with metric, baseline, target, checkpoint and outcome', ['Objective', 'Goal', 'Metric (kind)', 'Baseline', 'Target', 'Checkpoint', 'Outcome'], [[o['label'], o['goals'], '%s (%s)' % (o['metric'], o['kind']), o['baseline'], o['target'] + (' ' + o['direction'].lower() if o['direction'] else ''), o['checkpoint'], o['outcome']] for o in m['objectives']], [1900, 1500, 1500, 800, 900, 1900, 900])
    for p in m['packages']:
        T.define('b_pkg_' + p['id'], 'Work items of the package %s' % p['label'], ['Identifier', 'Work item', 'Pursues objective', 'Horizon', 'State'], [[m['items'][w]['ident'], wl(w), m['items'][w]['objectives'], m['items'][w]['horizon'], m['items'][w]['state'] + (' (needs upstream change)' if m['items'][w]['needs_upstream'] else '')] for w in p['members']], [1900, 3000, 2300, 800, 1400])
    orphan = [k for k in m['items'] if not any(k in p['members'] for p in m['packages'])]
    T.define('b_orphan', 'Work items in no package (evaluation evidence)', ['Identifier', 'Work item', 'Pursues objective', 'Horizon', 'State'], [[m['items'][w]['ident'], wl(w), m['items'][w]['objectives'], m['items'][w]['horizon'], m['items'][w]['state']] for w in orphan], [1900, 3000, 2300, 800, 1400])
    T.define('b_iterations', 'Iterations with windows, sprint goals and members', ['Iteration', 'Window', 'Sprint goal', 'Members', 'Capacity and committed effort'], [[i['label'], '%s to %s' % (i['start'], i['end']) if i['start'] else 'undated', i['goal'], wids(i['members']), '%s and %s' % (i['capacity'], i['committed'])] for i in m['iterations']], [1000, 1300, 3600, 2500, 1000])
    T.define('b_horizons', 'Roadmap horizons', ['Horizon', 'Count', 'Work items'], [[h, str(len(m['horizons'].get(h, []))), wids(m['horizons'].get(h, []))] for h in ['Now', 'Next', 'Later']], [1000, 700, 7700])
    T.define('b_dod', 'Definition of Done criteria with their check queries', ['Criterion', 'Check query', 'Expected', 'Status'], [[d['definition'], d['query'].lower(), d['expected'], d['status']] for d in m['dod']], [3600, 3300, 900, 1600])
    T.define('c_tbox', 'Project concepts and their alignment to framework classes', ['Project concept', 'Aligned framework class', 'Meaning'], [[c['label'], c['match'], c['definition']] for c in m['tbox']], [2200, 2600, 4600])
    T.define('c_props', 'Project relationships', ['Relationship', 'Meaning'], [[p['label'], p['definition']] for p in m['tbox_props']], [2600, 6800])
    T.define('c_entities', 'Blueprint domain entities and their framework alignment', ['Domain entity', 'Aligned framework class', 'Definition'], [[e['label'], e['match'], e['definition']] for e in m['blueprint']['entities']], [2000, 2000, 5400])
    T.define('c_gaps', 'Recorded blueprint coverage gaps', ['Gap', 'Entity', 'Life stage', 'Why it remains a gap'], [[x['label'], x['entity'], x['stage'], x['reason']] for x in m['gaps']], [2400, 1500, 1100, 4400])
    T.define('d_proposals', 'Enhancement proposals filed with the framework', ['Proposal', 'Status', 'Requested change', 'Unblocks'], [[p['label'], p['status'], p['change'], p['unblocks']] for p in m['proposals']], [2200, 900, 4300, 2000])
    T.define('d_tools', 'Tooling shipped with the package', ['Tool', 'Purpose'], [['SCAMPS_PIN.txt', 'Pins the SCAMPS checkout (commit and file hashes) the register and ontology are read from'], ['vaf_integration_probe_v1_0_0.py', 'Proves the framework is really called and that its algebra refuses what it must'], ['page_regression_check_v1_0_0.js', 'Operates every control of the interactive page'], ['proposal_from_register_v2_3_0.py and proposal_render_v2_0_0.js', 'Generate this document from the register in the pinned SCAMPS checkout'], ['proposal_coverage_check_v1_2_0.py', 'Fails if this document or the page omits a register element or names a retired one'], ['fixtures/verify_shapes_v1_0_0.py', 'Proves the project shapes discriminate on positive and negative fixtures']], [3600, 5800])
    T.define('e_witness', 'Active stage outputs and the commits at which they closed', ['Stage', 'Commit', 'Note'], [[x['stage'], x['commit'][:12], x['note']] for x in m['stage_outputs']], [1500, 1500, 6400])
    T.define('f_glossary', 'Glossary of register terms', ['Term', 'Register class', 'Meaning in this project'], [
        ['Mission', 'Mission', 'Why the development exists; owner-declared root of the intent chain'], ['Scope area, deliverable, exclusion', 'ScopeArea, ScopeDeliverable, ScopeExclusion', 'Where work lives, what it must deliver, and what it refuses, with rationale'],
        ['Goal and objective', 'Goal, Objective', 'A durable outcome; a measurable target with baseline, target, checkpoint and outcome'], ['Work item', 'Feature', 'The granularity chosen here; every item pursues an objective and satisfies a deliverable'],
        ['Roadmap package', 'Package', 'A group of work items delivered together under one release version'], ['Release package', 'This directory', 'A versioned, checksummed folder described by a manifest'],
        ['Iteration', 'Iteration', 'A time box with a goal stated in terms of what the framework must do by its end'], ['Planning event', 'PlanningEvent', 'The dated act of taking an item into an iteration; none exists until work begins'],
        ['Milestone', 'Milestone', 'A point reached when its recorded outcome says so'], ['External dependency', 'ExternalDependency', 'Something the development depends on, does not own, and cannot change by deciding to'],
        ['Enhancement proposal', 'EnhancementProposal', 'A change asked of the external party, filed in its inbox, with the items it would unblock'], ['Requirements analysis', 'Project phase', 'Working out what the system must do, done by people'],
        ['Dependency detection', 'Pipeline step', 'The framework calculi reading harvested code, done by a program'], ['Blueprint gap', 'BlueprintGap', 'A domain entity and life stage no work item covers, with the reason']], [2200, 2600, 4600])
    T.define('g_provenance', 'Provenance of this document', ['Item', 'Value'], [['Generated by', 'proposal_from_register_v2_3_0.py and proposal_render_v2_0_0.js'], ['Register read from', m['register_label']], ['Register sources', ', '.join(m['sources'])], ['Prose source', os.path.basename(m['prose'])], ['Framework commit', 'd310082 (altunelyusuf/VAF)'], ['Generated at', m['generated_at']], ['Rule', 'Generated artefact: regenerate, never hand-edit']], [2200, 7200])
    T.define('g_signatures', 'Approval signatures', ['Role', 'Name', 'Signature', 'Date'], PD['signatures'], [2200, 2600, 2600, 2000])

ABBR = project_data()['abbreviations']

def calm(text):
    """Register and ontology comments sometimes shout a word in capitals for emphasis. The document is not the place
    for that, and the abbreviation gates would read each such word as an acronym; so any all-capital English word that
    is not a known abbreviation is written in lower case. Case only; no word is changed."""
    text = re.sub(r'\b([A-Z]{2,})\b', lambda mm: mm.group(1) if (mm.group(1) in ABBR or re.fullmatch(r'(WI|COM|SEN|C)\d*', mm.group(1))) else mm.group(1).lower(), text)
    # Register definitions quote mission clauses with straight double quotes; in a document those read as citations. Typography only: rendered as single curly quotes.
    return re.sub(r'"([^"]*)"', lambda mm: '\u2018' + mm.group(1) + '\u2019', text)

def fill(text, m, ctx):
    return re.sub(r'\{\{([A-Za-z_.]+)\}\}', lambda mm: ctx.get(mm.group(1), mm.group(0)), text)

def prose_blocks(m, path, T):
    ctx = {'external.label': m['external']['label'], 'external.n_dependants': str(len(m['external']['dependants'])), 'gaps.semantic_count': str(m['gaps_semantic']), 'mission.statement': m['mission']['statement']}
    for k, v in m['counts'].items():
        if not isinstance(v, dict): ctx['counts.' + k] = str(v)
    ctx.update(sentences(m))
    body = open(path, encoding='utf-8').read()
    body = body.split('\n## ', 1)[1]; body = '## ' + body  # drop file preamble
    for k in T.defs: ctx['tab:' + k] = None  # filled lazily below
    blocks = []; refs = []
    for raw in body.split('\n\n'):
        raw = raw.strip()
        if not raw: continue
        if raw.startswith('#'):
            lvl = len(raw) - len(raw.lstrip('#')); title = raw.lstrip('#').strip()
            if title.upper() == 'ABSTRACT': blocks.append(H(1, 'Abstract', front=True)); continue
            if title == 'References': blocks.append(H(1, 'References', front=True)); continue
            blocks.append(H(lvl - 1, title)); continue
        mt = re.match(r'\{\{TABLE:(\w+)\}\}', raw)
        if mt: blocks.append(T.block(mt.group(1))); continue
        if raw.startswith('[') and re.match(r'\[\d+\]\.', raw):
            for line in raw.split('\n'): blocks.append(P(line.strip(), ref=True))
            continue
        text = ' '.join(raw.split())
        text = re.sub(r'\{\{tab:(\w+)\}\}', lambda mm: 'Table %d' % T.number(mm.group(1)), text)
        blocks.append(P(fill(text, m, ctx)))
    return blocks

def H(level, text, front=False): return {'h': level, 'text': text, 'front': front}

def appendices(m, T):
    b = []
    b.append(H(1, 'Appendix A. Academic Context', front=True))
    b.append(P('This appendix records the institutional setting of the project and the assessment apparatus the course applies. The institution and course are listed in Table %d, the learning objectives in Table %d, the academic milestones in Table %d and the peer-evaluation criteria in Table %d.' % (T.number('a_institution'), T.number('a_lo'), T.number('a_academic_ms'), T.number('a_peer'))))
    for k in ['a_institution', 'a_lo', 'a_academic_ms', 'a_peer']: b.append(T.block(k))
    b.append(H(1, 'Appendix B. The Register', front=True))
    b.append(P('Every table in this appendix is read from the register files %s at build time. The scope is given in Tables %d to %d, the goals and objectives in Tables %d and %d, the work items by package in Tables %d to %d, and the delivery layer in Tables %d to %d.' % (', '.join(m['sources']), T.number('b_areas'), T.number('b_exclusions'), T.number('b_goals'), T.number('b_objectives'), T.number('b_pkg_' + m['packages'][0]['id']), T.number('b_orphan'), T.number('b_iterations'), T.number('b_dod'))))
    b.append(H(2, 'B.1 Scope')); b.append(P(m['scope']['definition']))
    for k in ['b_areas', 'b_deliverables', 'b_exclusions']: b.append(T.block(k))
    b.append(H(2, 'B.2 Goals and Objectives'))
    for k in ['b_goals', 'b_objectives']: b.append(T.block(k))
    b.append(H(2, 'B.3 Work Items by Package'))
    for p in m['packages']:
        b.append(P(calm(p['definition']))); b.append(T.block('b_pkg_' + p['id']))
    b.append(T.block('b_orphan'))
    b.append(H(2, 'B.4 Iterations, Horizons and Definition of Done'))
    b.append(P('Iteration duration follows the register: %s The roadmap %s realises %s.' % (m['iterations'][0]['duration_source'], m['roadmap']['label'], m['roadmap']['realises'])))
    for k in ['b_iterations', 'b_horizons', 'b_dod']: b.append(T.block(k))
    b.append(H(1, 'Appendix C. Ontology and Representation', front=True))
    b.append(P('The project ontology declares its own concepts and relationships and aligns each concept to the framework class it drives by a close-match link; the framework is never imported. Table %d lists the concepts, Table %d the relationships, Table %d the blueprint domain entities that the work items cover, and Table %d the coverage gaps that remain recorded.' % (T.number('c_tbox'), T.number('c_props'), T.number('c_entities'), T.number('c_gaps'))))
    for k in ['c_tbox', 'c_props', 'c_entities', 'c_gaps']: b.append(T.block(k))
    b.append(H(1, 'Appendix D. External Dependency, Proposals and Tooling', front=True))
    b.append(P('%s is recorded as an external dependency of type %s, owned by %s. %s' % (m['external']['label'], m['external']['type'].lower(), m['external']['party'], m['external']['definition'])))
    b.append(P('%d work items depend on it: %s. %d work items are blocked on an upstream change: %s. The proposals filed with the framework are listed in Table %d and the tooling shipped with this package in Table %d.' % (len(m['external']['dependants']), '; '.join(m['items'][w]['label'] for w in m['external']['dependants']), len(m['external']['needing_upstream']), '; '.join(m['items'][w]['label'] for w in m['external']['needing_upstream']), T.number('d_proposals'), T.number('d_tools'))))
    if m['disclosure']: b.append(P('Disclosure recorded in the register: ' + m['disclosure']))
    for k in ['d_proposals', 'd_tools']: b.append(T.block(k))
    b.append(H(1, 'Appendix E. Lineage Witness', front=True))
    b.append(P('The intent chain was built as a pipeline, one commit per stage, after a recorded bypass and a restart; the active stage outputs and the commits at which they closed are listed in Table %d. Every commit is an ancestor of the published branch of the repository altunelyusuf/Ontologies.' % T.number('e_witness')))
    b.append(T.block('e_witness'))
    b.append(H(1, 'Appendix F. Glossary', front=True)); b.append(P('Table %d defines the register terms as they are used in this document.' % T.number('f_glossary'))); b.append(T.block('f_glossary'))
    b.append(H(1, 'Appendix G. Provenance and Approval', front=True)); b.append(P('Table %d records how this document was produced and Table %d carries the approval signatures.' % (T.number('g_provenance'), T.number('g_signatures'))))
    for k in ['g_provenance', 'g_signatures']: b.append(T.block(k))
    return b

def to_markdown(blocks):
    out = []
    for b in blocks:
        if 'h' in b: out.append('#' * b['h'] + ' ' + b['text'] + '\n')
        elif 'p' in b: out.append(b['p'] + '\n')
        elif 'table' in b:
            t = b['table']; out.append(b['caption']); out.append('| ' + ' | '.join(t['header']) + ' |'); out.append('|' + '---|' * len(t['header']))
            for r in t['rows']: out.append('| ' + ' | '.join(c.replace('|', '/').replace('\n', ' ') for c in r) + ' |')
            out.append('')
        elif 'front' in b: out.append('')
    return '\n'.join(out)

def abbreviations(md):
    used = sorted(set(re.findall(r'\b([A-Z]{2,}[0-9]*)\b', md)))
    return used

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); a = ap.parse_args()
    g, t = load(); m = build(g, t)
    P_ = paths(); m['sources'] = sorted(os.path.basename(f) for f in glob.glob(os.path.join(P_['lineage'], '*.ttl'))) + [os.path.basename(highest(os.path.join(P_['onto'], 'vaf_ap_blueprint_v*_*_*.ttl')))]; m['register_label'] = P_['label']
    m['prose'] = highest('04-documentation/proposal_prose_v*_*_*.md')
    m['version'] = '.'.join(re.findall(r'_v(\d+)_(\d+)_(\d+)\.docx$', a.out)[0])
    m['generated_at'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%MZ')
    T = Tables(); define_tables(m, T)
    body = prose_blocks(m, m['prose'], T)
    # references are the last run of ref paragraphs; appendices go after them
    apps = appendices(m, T)
    PD = project_data(); front = [{'title': 'Project Proposal', 'subtitle': PD['title'], 'meta': [['Course', PD['course_line']], ['Institution', PD['institution_line']], ['Advisor', PD['advisor']], ['Document version', m['version']], ['Generated from the register', m['generated_at']]]}]
    md_probe = to_markdown(body + apps)
    used = abbreviations(md_probe)
    unknown = [u for u in used if u not in ABBR and not re.fullmatch(r'(WI|COM|SEN)\d*', u)]
    rows = [['%s (%s)' % (ABBR[u], u), u] for u in used if u in ABBR]
    abbr_blocks = [H(1, 'List of Abbreviations', front=True), {'table': {'caption': 'Abbreviations used in this document', 'header': ['Expansion (abbreviation)', 'Abbreviation'], 'rows': rows, 'widths': [6400, 3000]}, 'caption': 'Abbreviations used in this document, in alphabetical order of the abbreviation'}]
    # insert abbreviations after the abstract
    idx = next(i for i, b in enumerate(body) if b.get('h') == 1 and b.get('text') != 'Abstract')
    blocks = front + body[:idx] + abbr_blocks + body[idx:] + apps
    md = to_markdown(blocks)
    mp = re.sub(r'\.docx$', '.md', a.out)
    open(mp, 'w', encoding='utf-8').write(md)
    json.dump({'blocks': blocks, 'version': m['version']}, open(a.out + '.model.json', 'w'), ensure_ascii=False)
    print('markdown:', mp, len(md.split()), 'words;', 'tables:', T.n, '; abbreviations:', len(rows), '; unknown acronyms:', unknown)
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run(['node', os.path.join(here, 'proposal_render_v2_0_0.js'), a.out + '.model.json', a.out], capture_output=True, text=True)
    print(r.stdout.strip()); 
    if r.returncode: print(r.stderr, file=sys.stderr)
    os.remove(a.out + '.model.json')
    sys.exit(r.returncode)

if __name__ == '__main__':
    main()
