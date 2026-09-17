const SUGGEST = ['What is the mission?','Which work items depend on the framework?','What is the target of detection accuracy?','When is the first milestone?','What does iteration 1 deliver?','Which items are blocked on an upstream change?','What is excluded from scope?','Which package carries the central claim?','What are the coverage gaps?','Which objective has the tier-5 review gate as its checkpoint?'];
$('#suggest').innerHTML = SUGGEST.map(q => `<button data-q="${esc(q)}">${esc(q)}</button>`).join(''); $('#suggest').addEventListener('click', e => { const b = e.target.closest('button'); if (b) ask(b.dataset.q); });
const ENTRIES = [];
D.goals.forEach(g => ENTRIES.push({id:g.id, kind:'goal', label:g.label, text:[g.label,g.definition,g.metric,'target',g.target,g.areas].join(' '), obj:g}));
D.objectives.forEach(o => ENTRIES.push({id:o.id, kind:'objective', label:o.label, text:[o.label,o.metric,'baseline',o.baseline,'target',o.target,o.direction,o.checkpoint,o.goals].join(' '), obj:o}));
items.forEach(w => ENTRIES.push({id:w.id, kind:'work item', label:w.label, text:[w.label,w.definition,w.objectives,w.deliverables,w.horizon,w.milestone,w.external?'depends on the framework external dependency':'',w.needs_upstream?'blocked upstream change':''].join(' '), obj:w}));
D.packages.forEach(p => ENTRIES.push({id:p.id, kind:'package', label:p.label, text:[p.label,p.definition,'release',p.version,p.iterations].join(' '), obj:p}));
D.iterations.forEach(i => ENTRIES.push({id:i.id, kind:'iteration', label:i.label, text:[i.label,i.goal,'sprint goal'].join(' '), obj:i}));
D.milestones.forEach(m0 => ENTRIES.push({id:m0.id, kind:'milestone', label:m0.label, text:[m0.label,m0.definition,m0.date,'milestone when'].join(' '), obj:m0}));
D.areas.forEach(a => ENTRIES.push({id:a.id, kind:'scope area', label:a.label, text:[a.label,a.location,a.measure,'scope area'].join(' '), obj:a}));
D.deliverables.forEach(d => ENTRIES.push({id:d.id, kind:'deliverable', label:d.label, text:[d.label,d.area,'deliverable'].join(' '), obj:d}));
D.exclusions.forEach(x => ENTRIES.push({id:x.id, kind:'exclusion', label:x.label, text:[x.label,x.concern,x.rationale,'excluded exclusion out of scope'].join(' '), obj:x}));
D.proposals.forEach(p => ENTRIES.push({id:p.id, kind:'proposal', label:p.label, text:[p.label,p.change,p.status,p.unblocks,'proposal upstream inbox'].join(' '), obj:p}));
D.gaps.forEach(g => ENTRIES.push({id:g.label, kind:'gap', label:g.label, text:[g.label,g.entity,g.stage,g.reason,'coverage gap'].join(' '), obj:g}));
ENTRIES.push({id:'Mission', kind:'mission', label:D.mission.label, text:[D.mission.statement,D.mission.definition,'mission'].join(' '), obj:D.mission});
ENTRIES.push({id:'ExtDep', kind:'external dependency', label:D.external.label, text:[D.external.label,D.external.definition,'framework dependency'].join(' '), obj:D.external});
const STOP = new Set('the a an of to in on for and or is are what which when who how does do it its this that with by as at from be'.split(' '));
const tok = s => String(s).toLowerCase().replace(/[^a-z0-9\- ]/g,' ').split(/\s+/).filter(x=>x && !STOP.has(x));
const DF = {}; ENTRIES.forEach(e => { e.tf = {}; tok(e.text).forEach(t => e.tf[t]=(e.tf[t]||0)+1); Object.keys(e.tf).forEach(t=>DF[t]=(DF[t]||0)+1); });
function score(q, e){ const qt = tok(q); let s=0; qt.forEach(t=>{ if(e.tf[t]) s += (1+Math.log(e.tf[t])) * Math.log(ENTRIES.length/(DF[t]||1)); if (e.label.toLowerCase().includes(t)) s += 1.5; }); return s; }
function explain(e){ const o=e.obj; switch(e.kind){
  case 'mission': return `The mission is: “${o.statement}” It is owner-stated and is the root of the intent chain.`;
  case 'goal': return `The goal “${o.label}” is measured by ${o.metric.toLowerCase()} with a target of ${o.target}. ${o.definition}`;
  case 'objective': return `The objective “${o.label}” contributes to the goal “${o.goals}”. It is measured by ${o.metric || 'a counted measure'} (${o.kind}), from a baseline of ${o.baseline} to a target of ${o.target} (${o.direction.toLowerCase()}). Its checkpoint is the work item “${o.checkpoint}” and its outcome is currently ${o.outcome}.`;
  case 'work item': { const p=pkgOf(o.id), it=iterOf(o.id); return `“${o.label}” (${o.ident}) is a ${o.state.toLowerCase()} work item in ${p?'the package “'+p.label+'” (release '+p.version+')':'no package'}${it?', '+it.label:''}, scheduled in the ${o.horizon} horizon. It pursues the objective “${o.objectives}” and satisfies the deliverable “${o.deliverables}”${o.milestone?', contributing to the milestone “'+o.milestone+'”':''}.${o.external?' It depends on the framework as an external dependency.':''}${o.needs_upstream?' It is blocked on an upstream change the project cannot make.':''} ${o.definition||''}`; }
  case 'package': return `The package “${o.label}” releases as ${o.version} in ${o.iterations} and holds ${o.members.length} work items: ${o.members.map(i=>D.items[i].label).join('; ')}. ${o.definition}`;
  case 'iteration': return `${o.label}${o.start?' ('+o.start+' to '+o.end+')':''} (capacity ${o.capacity}, committed ${o.committed}) has the sprint goal: ${o.goal} Its members are: ${o.members.map(i=>D.items[i].label).join('; ')}.`;
  case 'milestone': return `The milestone “${o.label}” has the target date ${o.date} and its outcome is ${o.outcome}. It is reached when: ${o.definition}`;
  case 'scope area': return `The scope area “${o.label}” lives at ${o.location}; its measure is ${o.measure}.`;
  case 'deliverable': return `The deliverable “${o.label}” belongs to the area “${o.area}” and is satisfied by: ${items.filter(w0=>w0.deliverables.includes(o.label)).map(w0=>w0.label).join('; ')||'no work item yet'}.`;
  case 'exclusion': return `“${o.label}” is excluded (${o.concern}). Rationale: ${o.rationale}`;
  case 'proposal': return `The proposal “${o.label}” (status ${o.status}, raised ${o.raised}) asks: ${o.change} It would unblock: ${o.unblocks}.`;
  case 'gap': return `${o.label}: the entity “${o.entity}” has no work item at the ${o.stage} life stage. Reason recorded: ${o.reason}`;
  case 'external dependency': return `${o.label} is an external dependency of type ${o.type}, owned by ${o.party}. ${o.definition}`;
  } return e.label; }
function ask(q){ q = (q||$('#askinput').value).trim(); if(!q) return; $('#askinput').value=''; const chat=$('#chat'); const qdiv=document.createElement('div'); qdiv.className='turn q'; qdiv.textContent=q; chat.insertBefore(qdiv, chat.querySelector('.askrow'));
  const ql=q.toLowerCase(); let ans='', srcs=[];
  const listAns = (title, arr, fmt) => { ans = `<b>${title}</b> (${arr.length}):<ul>${arr.map(x=>`<li>${fmt(x)}</li>`).join('')}</ul>`; srcs = arr.map(x=>x.id||x.label); };
  if (/depend(s|ent)? on the framework|framework dependen/.test(ql)) listAns('Work items that depend on the framework', items.filter(w0=>w0.external), w0=>esc(w0.label));
  else if (/blocked|upstream change/.test(ql)) listAns('Work items blocked on an upstream change', items.filter(w0=>w0.needs_upstream), w0=>esc(w0.label));
  else if (/exclu|out of scope/.test(ql)) listAns('Scope exclusions', D.exclusions, x=>`<b>${esc(x.label)}</b>: ${esc(x.rationale)}`);
  else if (/coverage gap|gaps/.test(ql)) listAns('Recorded coverage gaps', D.gaps, x=>`<b>${esc(x.entity)}</b> at ${esc(x.stage)}: ${esc(x.reason)}`);
  else if (/first milestone|earliest milestone|next milestone/.test(ql)) { const m0=D.milestones[0]; ans=esc(explain(ENTRIES.find(e=>e.id===m0.id))); srcs=[m0.id]; }
  else if (/central claim/.test(ql)) { const p=D.packages.find(x=>/central claim/i.test(x.definition)); if(p){ ans=esc(explain(ENTRIES.find(e=>e.id===p.id))); srcs=[p.id]; } }
  else if (/how many|count/.test(ql)) { ans=`The register holds ${D.counts.items} work items (${Object.entries(D.counts.states).map(([k,v])=>v+' '+k.toLowerCase()).join(', ')}), ${D.counts.goals} goals, ${D.counts.objectives} objectives, ${D.counts.areas} scope areas, ${D.counts.deliverables} deliverables, ${D.counts.exclusions} exclusions, ${D.counts.packages} packages, ${D.counts.iterations} iterations, ${D.counts.milestones} milestones and ${D.counts.proposals} enhancement proposals.`; srcs=['register counts']; }
  if (!ans){ const ranked = ENTRIES.map(e=>({e,s:score(q,e)})).sort((a,b)=>b.s-a.s).filter(x=>x.s>0).slice(0,3);
    if (!ranked.length) { ans = 'No register element matches that question. Try naming a work item, objective, package, milestone or scope area, or use one of the suggested questions.'; }
    else { const best=ranked[0]; ans = esc(explain(best.e)); if (ranked.length>1) ans += `<div class="small muted" style="margin-top:6px">Also related: ${ranked.slice(1).map(r=>esc(r.e.label)+' ('+r.e.kind+')').join('; ')}</div>`; ans += `<div class="small muted">Confidence: match score ${best.s.toFixed(2)} on ${best.e.kind} “${esc(best.e.label)}”.</div>`; srcs=[best.e.id]; } }
  const adiv=document.createElement('div'); adiv.className='turn a'; adiv.innerHTML = ans + `<div class="src">Grounded in: ${srcs.map(s=>`<code>${esc(s)}</code>`).join(' ')}</div>`; chat.insertBefore(adiv, chat.querySelector('.askrow')); adiv.scrollIntoView({block:'nearest'}); }
$('#askbtn').onclick = () => ask(); $('#askinput').addEventListener('keydown', e => { if (e.key==='Enter') ask(); });
