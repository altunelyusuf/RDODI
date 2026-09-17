function modelChain(){
  const stages = ['Mission','Scope','Goal','Objective','Backlog']; const w=900,h=170; let s=svgOpen(w,h);
  const counts = {Mission:1, Scope:D.counts.areas+' areas · '+D.counts.deliverables+' deliverables', Goal:D.counts.goals+' goals', Objective:D.counts.objectives+' objectives', Backlog:D.counts.items+' work items'};
  stages.forEach((st,i)=>{ const x=30+i*175, so=D.stage_outputs.find(o=>o.stage===st); s+=`<g class="node-rect" data-stage="${st}"><rect x="${x}" y="40" width="150" height="70" rx="10" fill="var(--soft)" stroke="var(--accent)" stroke-width="1.5"/>${tspan(x+75,63,[st],14,'var(--accent)')}${tspan(x+75,82,[String(counts[st])],10.5,'var(--muted)')}${tspan(x+75,100,[so?'commit '+so.commit.slice(0,7):'—'],10,'var(--accent2)')}</g>`; if(i<4) s+=`<path d="M${x+150} 75 L${x+175} 75" stroke="var(--muted)" stroke-width="1.5" marker-end="url(#arr)"/>`; });
  s+=`<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="var(--muted)"/></marker></defs>${tspan(450,135,wrap('Each stage closed in its own commit before the next began; the commit witnesses the order. A bypass was found and answered by a restart; the rebuilt chain is what is shown.',120),11,'var(--muted)')}</svg>`;
  return s;
}
function modelTrace(){
  const cols = [D.goals.map(g=>({id:g.id,label:g.label,kind:'goal'})), D.objectives.map(o=>({id:o.id,label:o.label,kind:'obj'})), items.map(w=>({id:w.id,label:w.label,kind:'wi'})), D.deliverables.map(d=>({id:d.id,label:d.label,kind:'del'}))];
  const w=1100, rowH=22, h=Math.max(...cols.map(c=>c.length))*rowH+60; let s=svgOpen(w,h); const xs=[20,300,580,860]; const pos={};
  const colors={goal:'#1f4e8c',obj:'#2e7d5b',wi:'#6a5acd',del:'#b8641c'};
  cols.forEach((col,ci)=>{ const off=(h-40-col.length*rowH)/2; s+=`<text x="${xs[ci]}" y="18" font-size="12" font-weight="600" fill="var(--muted)">${['Goals','Objectives','Work items','Deliverables'][ci]}</text>`; col.forEach((n,i)=>{ const y=30+off+i*rowH; pos[n.id]={x:xs[ci],y:y+8,ci}; s+=`<g class="node-rect tn" data-id="${n.id}" data-kind="${n.kind}"><rect x="${xs[ci]}" y="${y}" width="220" height="18" rx="4" fill="var(--panel)" stroke="${colors[n.kind]}"/><text x="${xs[ci]+6}" y="${y+13}" font-size="10.5" fill="var(--ink)">${esc(n.label.length>36?n.label.slice(0,35)+'…':n.label)}</text></g>`; }); });
  const edges=[]; D.objectives.forEach(o=>o.goals.split(', ').forEach(gl=>{ const g=D.goals.find(x=>x.label===gl); if(g) edges.push([g.id,o.id]); })); items.forEach(wi=>{ wi.objectives.split(', ').forEach(ol=>{ const o=D.objectives.find(x=>x.label===ol); if(o) edges.push([o.id,wi.id]); }); wi.deliverables.split(', ').forEach(dl=>{ const d=D.deliverables.find(x=>x.label===dl); if(d) edges.push([wi.id,d.id]); }); });
  let e=''; edges.forEach(([a,b])=>{ const A=pos[a],B=pos[b]; if(!A||!B) return; e+=`<path class="edge" data-a="${a}" data-b="${b}" d="M${A.x+220} ${A.y} C ${A.x+260} ${A.y}, ${B.x-40} ${B.y}, ${B.x} ${B.y}" fill="none" stroke="var(--line)" stroke-width="1.2"/>`; });
  return s.replace('role="img">', 'role="img">'+e)+'</svg>';
}
function modelRoadmap(){
  const w=1000, h=285; let s=svgOpen(w,h); const its=D.iterations; const x0=140, cw=(w-x0-20)/its.length;
  its.forEach((it,i)=>{ const x=x0+i*cw; s+=`<rect x="${x}" y="40" width="${cw-6}" height="32" rx="5" fill="var(--soft)" stroke="var(--line)"/>${tspan(x+cw/2-3,53,[it.label+' · '+it.members.length+' items'],11)}${tspan(x+cw/2-3,65,[it.start?it.start.slice(5)+' → '+it.end.slice(5):''],9.5,'var(--muted)')}`; });
  s+=`<text x="10" y="57" font-size="12" font-weight="600" fill="var(--muted)">Iterations</text><text x="10" y="107" font-size="12" font-weight="600" fill="var(--muted)">Packages</text><text x="10" y="200" font-size="12" font-weight="600" fill="var(--muted)">Milestones</text>`;
  D.packages.forEach((p,i)=>{ const idx=its.findIndex(it=>p.iterations.includes(it.label)); const x=x0+(idx<0?0:idx)*cw; s+=`<g class="node-rect" data-pkg="${p.id}"><rect x="${x}" y="80" width="${cw-6}" height="46" rx="6" fill="var(--panel)" stroke="var(--accent)" stroke-width="1.4"/>${tspan(x+cw/2-3,98,wrap(p.label,26).slice(0,2),10)}${tspan(x+cw/2-3,120,['release '+p.version],10,'var(--accent2)')}</g>`; });
  const dates=D.milestones.map(m0=>new Date(m0.date)); const t0=Math.min(...dates), t1=Math.max(...dates); D.milestones.forEach((m0,i)=>{ const x=x0+((new Date(m0.date)-t0)/((t1-t0)||1))*(w-x0-60)+20; s+=`<g class="node-rect" data-ms="${m0.id}"><line x1="${x}" y1="150" x2="${x}" y2="180" stroke="var(--warn)" stroke-width="2"/><circle cx="${x}" cy="180" r="7" fill="var(--warn)"/>${tspan(x,214,[m0.date],10.5,'var(--warn)')}${tspan(x,228,wrap(m0.label,34).slice(0,2),9.5,'var(--muted)')}</g>`; });
  s+=`<line x1="${x0}" y1="180" x2="${w-20}" y2="180" stroke="var(--line)"/>${tspan(w/2,262,wrap('Packages sit under the iteration that targets them; milestones are placed on a proportional time axis by their register target dates. Nothing has started: every package is unreleased and every milestone is pending.',130),10.5,'var(--muted)')}</svg>`;
  return s;
}
function modelObjectives(){
  const w=1000,rh=44,h=D.objectives.length*rh+30; let s=svgOpen(w,h); const bx=400, bwmax=w-bx-190;
  D.objectives.forEach((o,i)=>{ const y=16+i*rh; const b=parseFloat(o.baseline)||0, t=parseFloat(o.target)||0, mx=Math.max(b,t,1); const bw=bwmax*(b/mx), tw=bwmax*(t/mx);
    s+=`<text x="10" y="${y+13}" font-size="11.5" fill="var(--ink)">${esc(o.label.length>58?o.label.slice(0,57)+'…':o.label)}</text><text x="10" y="${y+28}" font-size="10" fill="var(--muted)">${esc(o.metric)} · ${esc(o.direction.toLowerCase())}</text>`;
    s+=`<rect x="${bx}" y="${y+4}" width="${bwmax}" height="18" rx="3" fill="var(--soft)"/><rect x="${bx}" y="${y+4}" width="${tw}" height="18" rx="3" fill="#bcd3f5"/><rect x="${bx}" y="${y+4}" width="${Math.max(bw,2)}" height="18" rx="3" fill="var(--accent)"/>`;
    s+=`<text x="${bx+bwmax+8}" y="${y+17}" font-size="10.5" fill="var(--ink)">${esc(o.baseline)} → ${esc(o.target)}</text>`; });
  s+=`<text x="${bx}" y="${h-6}" font-size="10" fill="var(--muted)">dark = baseline · light = target; the bar is scaled to each objective's own target</text>`;
  return s+'</svg>';
}
function modelCoverage(){
  const stages=['Creation','ActiveUse','Termination','SuspensionException']; const ents=D.blueprint.entities; const w=980, cellW=150, x0=300, h=ents.length*30+70; let s=svgOpen(w,h);
  stages.forEach((st,j)=>{ s+=`<text x="${x0+j*cellW+cellW/2}" y="20" font-size="11.5" font-weight="600" fill="var(--muted)" text-anchor="middle">${esc(st.replace('SuspensionException','Suspension / exception').replace('ActiveUse','Active use'))}</text>`; });
  ents.forEach((e,i)=>{ const y=36+i*30; s+=`<text x="10" y="${y+18}" font-size="11.5" fill="var(--ink)">${esc(e.label)}</text>`; stages.forEach((st,j)=>{ const gap=D.gaps.find(g=>g.entity===e.label && g.stage===st); const covered=items.some(wi=>wi.entities.includes(e.label)); const fill = gap ? '#f4d1c2' : (covered ? '#cfe9d6' : 'var(--soft)'); s+=`<g class="node-rect" data-ent="${esc(e.label)}" data-stage="${st}"><rect x="${x0+j*cellW+4}" y="${y}" width="${cellW-8}" height="24" rx="4" fill="${fill}" stroke="var(--line)"/><text x="${x0+j*cellW+cellW/2}" y="${y+16}" font-size="10.5" text-anchor="middle" fill="#1c2230">${gap?'gap (recorded)':(covered?'covered':'—')}</text></g>`; }); });
  s+=`</svg><div class="legend"><span><i style="background:#cfe9d6"></i>covered by at least one work item</span><span><i style="background:#f4d1c2"></i>recorded gap with a stated reason (${D.gaps.length}, ${D.gaps_semantic} trace to the framework's semantic calculi)</span><span><i style="background:var(--soft)"></i>not separately recorded</span></div>`;
  return s;
}
function modelPipeline(){
  const agents=D.tbox.filter(c=>/(agent|role) \(Stage \d\)/i.test(c.label)).sort((a,b)=>{ const n=x=>{const m0=/Stage (\d)/.exec(x.label); return m0?+m0[1]:9;}; return n(a)-n(b); });
  const w=1000,h=230; let s=svgOpen(w,h); const cw=(w-40)/agents.length;
  agents.forEach((a,i)=>{ const x=20+i*cw; s+=`<g class="node-rect" data-agent="${esc(a.label)}"><rect x="${x+8}" y="50" width="${cw-16}" height="70" rx="10" fill="var(--soft)" stroke="var(--accent)" stroke-width="1.5"/>${tspan(x+cw/2,75,[a.label.replace(/ \(Stage \d\)/,'')],13,'var(--accent)')}${tspan(x+cw/2,95,wrap('≈ '+(a.match||'—'),30).slice(0,2),10,'var(--accent2)')}</g>`; if(i<agents.length-1) s+=`<path d="M${x+cw-8} 85 L${x+cw+8} 85" stroke="var(--muted)" stroke-width="1.5" marker-end="url(#arr2)"/>`; });
  s+=`<defs><marker id="arr2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 z" fill="var(--muted)"/></marker></defs>`;
  s+=`<rect x="20" y="150" width="${w-40}" height="50" rx="8" fill="none" stroke="var(--warn)" stroke-dasharray="5 4"/>${tspan(w/2,170,[(D.project && D.project.review_note) || 'Every handoff is gated by a named SHACL shape; handoffs that require human review are marked in the register.'],11,'var(--warn)')}${tspan(w/2,188,['Each agent is aligned (skos:closeMatch) to the framework class whose machinery it drives; the framework is never imported.'],10.5,'var(--muted)')}</svg>`;
  return s;
}
function modelDependency(){
  const w=1000,h=260; let s=svgOpen(w,h);
  s+=`<rect x="20" y="30" width="300" height="200" rx="10" fill="var(--soft)" stroke="var(--accent)" stroke-width="1.5"/>${tspan(170,58,['External dependency'],13,'var(--accent)')}${tspan(170,80,wrap(D.external.label,40),11)}${tspan(170,120,['type: '+D.external.type,'owner: '+D.external.party],10.5,'var(--muted)')}${tspan(170,160,[D.external.dependants.length+' of '+D.counts.items+' work items depend on it', D.external.needing_upstream.length+' are blocked on an upstream change'],10.5,'var(--accent2)')}`;
  D.proposals.forEach((p,i)=>{ const y=30+i*70; s+=`<path d="M320 130 C 380 130, 380 ${y+30}, 400 ${y+30}" fill="none" stroke="var(--muted)" stroke-width="1.2"/><g class="node-rect" data-prop="${p.id}"><rect x="400" y="${y}" width="580" height="60" rx="8" fill="var(--panel)" stroke="var(--accent2)"/>${tspan(690,y+20,wrap(p.label,80).slice(0,1),11)}${tspan(690,y+38,['status: '+p.status+' · raised '+p.raised+' · unblocks: '+p.unblocks].map(x=>x.length>95?x.slice(0,94)+'…':x),10,'var(--muted)')}${tspan(690,y+52,['filed in the framework\'s own inbox'],9.5,'var(--accent2)')}</g>`; });
  return s+'</svg>';
}
function modelHorizons(){
  const w=1000,h=190; let s=svgOpen(w,h); const hz=['Now','Next','Later']; const mx=Math.max(...hz.map(x=>(D.horizons[x]||[]).length));
  hz.forEach((x,i)=>{ const n=(D.horizons[x]||[]).length, bh=120*(n/mx); s+=`<rect x="${60+i*110}" y="${150-bh}" width="70" height="${bh}" rx="4" fill="var(--accent)"/><text x="${95+i*110}" y="${145-bh}" font-size="12" text-anchor="middle" fill="var(--ink)">${n}</text><text x="${95+i*110}" y="168" font-size="12" text-anchor="middle" fill="var(--muted)">${x}</text>`; });
  const px=420; s+=`<text x="${px}" y="30" font-size="12" font-weight="600" fill="var(--muted)">Items per package</text>`; D.packages.forEach((p,i)=>{ const bw=440*(p.members.length/Math.max(...D.packages.map(q=>q.members.length))); s+=`<rect x="${px}" y="${40+i*26}" width="${bw}" height="18" rx="3" fill="var(--accent2)"/><text x="${px+bw+6}" y="${53+i*26}" font-size="11" fill="var(--ink)">${p.members.length} · ${esc(p.label)}</text>`; });
  const orphan = items.filter(w0=>!D.packages.some(p=>p.members.includes(w0.id))).length; s+=`<text x="${px}" y="${40+D.packages.length*26+14}" font-size="11" fill="var(--muted)">${orphan} evaluation items belong to no package</text>`;
  return s+'</svg>';
}

// ---------- v2.1.0: the whole lineage in one traceability chart, taxonomy visible
// Columns follow the chain the register is built on (Mission → Scope → Goals → Objectives → Work items) and then how
// the work reaches users (Deliverables, Packages, Iterations, Milestones). Within a column, elements are grouped by
// the taxonomy the framework gives them: scope layer, goal facing, investment category, horizon. Every edge is a typed
// relation read from the register; edge kinds can be switched on and off; hovering highlights the whole path through
// an element in both directions.
const LIN_EDGE_KINDS = [['scopeForMission','scope statement → mission'],['coversArea','scope statement → area'],['requiresDeliverable','scope statement → deliverable'],['hasScopeExclusion','scope statement → exclusion'],['contributesToMission','goal → mission'],['derivesFromScope','goal → scope statement'],['goalCoversArea','goal → area'],['guardsExclusion','goal → exclusion'],['contributesToGoal','objective → goal'],['pursuesObjective','work item → objective'],['satisfiesDeliverable','work item → deliverable'],['deliverableForArea','deliverable → area'],['memberOfPackage','work item → package'],['memberOfIteration','work item → iteration'],['contributesToMilestone','work item → milestone'],['targetsIteration','package → iteration'],['deliversDeliverable','package → deliverable (derived through its items; BRSF has no direct relation)']];
function modelLineage(){
  const cols=[]; const nodes=[]; const edges=[]; const byId={};
  function col(title){ const c={title, groups:[]}; cols.push(c); return c; }
  function grp(c,title,color){ const g={title,color,nodes:[]}; c.groups.push(g); return g; }
  function add(g,id,label,kind,extra){ const n=Object.assign({id,label,kind,col:cols.length-1},extra||{}); g.nodes.push(n); nodes.push(n); byId[id]=n; return n; }
  // 1 Mission
  let c=col('Mission'); let g=grp(c,'owner-stated','#1f4e8c'); add(g,'Mission',D.mission.label,'mission',{tip:D.mission.statement});
  // 2 Scope: statement, areas by layer, exclusions
  c=col('Scope'); g=grp(c,'scope statement','#4a6fa5'); add(g,'Scope',D.scope.label||'Scope statement','scope',{tip:D.scope.definition});
  const layers=[...new Set(D.areas.map(a=>a.layer||'unstated'))];
  layers.forEach(l=>{ const gl=grp(c,'areas · '+l.toLowerCase()+' layer','#4a6fa5'); D.areas.filter(a=>(a.layer||'unstated')===l).forEach(a=>add(gl,a.id,a.label,'area',{tip:a.measure})); });
  const ge=grp(c,'exclusions','#8a3a3a'); D.exclusions.forEach(x=>add(ge,x.id,x.label,'exclusion',{tip:x.rationale}));
  // 3 Goals by facing
  c=col('Goals'); [['Mission','mission-achievement goals','#1f4e8c'],['Scope','scope-coverage goals','#2e7d5b'],['Containment','guard: containment','#7a7a7a'],['Exclusion','guards: exclusions','#8a3a3a']].forEach(([f,t,colr])=>{ const gs=D.goals.filter(x=>x.facing===f); if(!gs.length) return; const gg=grp(c,t,colr); gs.forEach(x=>add(gg,x.id,x.label,'goal',{tip:x.metric+' · target '+x.target})); });
  // 4 Objectives (ordered by goal facing)
  c=col('Objectives'); g=grp(c,'measured, with baseline and target','#2e7d5b');
  const facingOf=lab=>{ const x=D.goals.find(y=>y.label===lab); return x?x.facing:''; }; const ford={Mission:0,Scope:1,Containment:2,Exclusion:3};
  D.objectives.slice().sort((a,b)=>(ford[facingOf(a.goals)]??9)-(ford[facingOf(b.goals)]??9)).forEach(o=>add(g,o.id,o.label,'objective',{tip:o.metric+' · '+o.baseline+' → '+o.target}));
  // 5 Work items by investment category
  c=col('Work items'); const cats=[...new Set(items.map(w=>w.category||'uncategorised'))]; cats.forEach(cat=>{ const gc=grp(c,cat.replace(/([a-z])([A-Z])/g,'$1 $2').toLowerCase(),'#6a5acd'); items.filter(w=>(w.category||'uncategorised')===cat).forEach(w=>add(gc,w.id,w.label,'wi',{tip:w.state+' · '+w.horizon+(w.external?' · depends on framework':'')})); });
  // 6 Deliverables
  c=col('Deliverables'); g=grp(c,'scope deliverables','#b8641c'); D.deliverables.forEach(d=>add(g,d.id,d.label,'del',{tip:'area: '+d.area}));
  // 7 Packages
  c=col('Packages'); g=grp(c,'roadmap packages · release','#c48a1a'); D.packages.forEach(p=>add(g,p.id,p.label+' · '+p.version,'pkg',{tip:p.definition}));
  // 8 Iterations
  c=col('Iterations'); g=grp(c,'two-week windows','#7a7a7a'); D.iterations.forEach(i=>add(g,i.id,i.label+(i.start?' · '+i.start.slice(5)+'→'+i.end.slice(5):''),'iter',{tip:i.goal}));
  // 9 Milestones
  c=col('Milestones'); g=grp(c,'target dates','#b8641c'); D.milestones.forEach(m0=>add(g,m0.id,m0.date+' · '+m0.label,'ms',{tip:m0.definition}));
  // edges
  const E=(a,b,rel)=>{ if(byId[a]&&byId[b]) edges.push({a,b,rel}); };
  E('Scope','Mission','scopeForMission'); D.areas.forEach(a=>E('Scope',a.id,'coversArea')); D.deliverables.forEach(d=>E('Scope',d.id,'requiresDeliverable')); D.exclusions.forEach(x=>E('Scope',x.id,'hasScopeExclusion'));
  D.packages.forEach(p=>{ const dels=new Set(); p.members.forEach(w=>D.deliverables.filter(d=>D.items[w].deliverables.includes(d.label)).forEach(d=>dels.add(d.id))); dels.forEach(d=>E(p.id,d,'deliversDeliverable')); });
  D.goals.forEach(x=>{ E(x.id,'Mission','contributesToMission'); E(x.id,'Scope','derivesFromScope'); x.areas.split(', ').forEach(al=>{ const a=D.areas.find(y=>y.label===al); if(a) E(x.id,a.id,'goalCoversArea'); }); x.guards.split(', ').forEach(gl=>{ const ex=D.exclusions.find(y=>y.label===gl); if(ex) E(x.id,ex.id,'guardsExclusion'); }); });
  D.objectives.forEach(o=>o.goals.split(', ').forEach(gl=>{ const x=D.goals.find(y=>y.label===gl); if(x) E(o.id,x.id,'contributesToGoal'); }));
  items.forEach(w=>{ w.objectives.split(', ').forEach(ol=>{ const o=D.objectives.find(y=>y.label===ol); if(o) E(w.id,o.id,'pursuesObjective'); }); w.deliverables.split(', ').forEach(dl=>{ const d=D.deliverables.find(y=>y.label===dl); if(d) E(w.id,d.id,'satisfiesDeliverable'); }); D.milestones.filter(m0=>w.milestone.includes(m0.label)).forEach(m0=>E(w.id,m0.id,'contributesToMilestone')); });
  D.deliverables.forEach(d=>{ const a=D.areas.find(y=>y.label===d.area); if(a) E(d.id,a.id,'deliverableForArea'); });
  D.packages.forEach(p=>{ p.members.forEach(w=>E(w,p.id,'memberOfPackage')); D.iterations.filter(i=>p.iterations.includes(i.label)).forEach(i=>E(p.id,i.id,'targetsIteration')); });
  D.iterations.forEach(i=>i.members.forEach(w=>E(w,i.id,'memberOfIteration')));
  // layout
  const colW=215, gap=22, rowH=20, hdr=18, x0=10; const w=x0+cols.length*(colW+gap); const pos={}; let h=60;
  cols.forEach((c,ci)=>{ let y=46; c.groups.forEach(gr=>{ gr.y=y; y+=hdr; gr.nodes.forEach(n=>{ pos[n.id]={x:x0+ci*(colW+gap), y}; y+=rowH; }); y+=10; }); h=Math.max(h,y+10); });
  // centre short columns vertically
  cols.forEach((c,ci)=>{ const ns=c.groups.flatMap(gr=>gr.nodes); if(!ns.length) return; const top=pos[ns[0].id].y, bot=pos[ns[ns.length-1].id].y+rowH; const off=Math.max(0,(h-40-(bot-top))/2-(top-46)); if(off>0){ c.groups.forEach(gr=>{ gr.y+=off; gr.nodes.forEach(n=>pos[n.id].y+=off); }); } });
  let s=`<div class="toolbar" id="lin-toolbar" style="margin:0 0 6px">${LIN_EDGE_KINDS.map(([k,l])=>`<label class="small" style="margin-right:6px"><input type="checkbox" data-edge="${k}" checked> ${esc(l)}</label>`).join('')}</div><div class="tblwrap" style="overflow:auto"><svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" id="lin-svg">`;
  const KC={mission:'#1f4e8c',scope:'#4a6fa5',area:'#4a6fa5',exclusion:'#8a3a3a',goal:'#1f4e8c',objective:'#2e7d5b',wi:'#6a5acd',del:'#b8641c',pkg:'#c48a1a',iter:'#7a7a7a',ms:'#b8641c'};
  cols.forEach((c,ci)=>{ const x=x0+ci*(colW+gap); s+=`<text x="${x}" y="22" font-size="13" font-weight="700" fill="var(--ink)">${esc(c.title)}</text><text x="${x}" y="36" font-size="10" fill="var(--muted)">${c.groups.reduce((n,gr)=>n+gr.nodes.length,0)} element${c.groups.reduce((n,gr)=>n+gr.nodes.length,0)===1?'':'s'}</text>`; c.groups.forEach(gr=>{ s+=`<rect x="${x-4}" y="${gr.y-2}" width="${colW+8}" height="${hdr+gr.nodes.length*rowH+4}" rx="6" fill="var(--soft)" opacity=".55"/><text x="${x+2}" y="${gr.y+12}" font-size="10" font-weight="600" fill="${gr.color}" style="text-transform:uppercase;letter-spacing:.4px">${esc(gr.title)}</text>`; }); });
  let e=''; edges.forEach(ed=>{ const A=pos[ed.a],B=pos[ed.b]; if(!A||!B) return; if(A.x===B.x){ const x=A.x-4, y1=A.y+rowH/2, y2=B.y+rowH/2; e+=`<path class="ledge" data-a="${ed.a}" data-b="${ed.b}" data-rel="${ed.rel}" d="M${A.x} ${y1} C ${x-14} ${y1}, ${x-14} ${y2}, ${B.x} ${y2}" fill="none" stroke="var(--line)" stroke-width="1.1" opacity=".8"/>`; return; } const left = A.x<B.x ? A : B, right = A.x<B.x ? B : A; const x1=left.x+colW, y1=left.y+rowH/2, x2=right.x, y2=right.y+rowH/2; e+=`<path class="ledge" data-a="${ed.a}" data-b="${ed.b}" data-rel="${ed.rel}" d="M${x1} ${y1} C ${x1+gap*0.6} ${y1}, ${x2-gap*0.6} ${y2}, ${x2} ${y2}" fill="none" stroke="var(--line)" stroke-width="1.1" opacity=".8"${ed.rel==='deliversDeliverable'?' stroke-dasharray="4 3"':''}/>`; });
  s+=e;
  nodes.forEach(n=>{ const p=pos[n.id]; s+=`<g class="node-rect ln" data-id="${esc(n.id)}" data-kind="${n.kind}" data-col="${n.col}" data-tip="${esc(n.tip||'')}" data-ctx-kind="${({wi:'workitem',goal:'goal',objective:'objective',area:'area',del:'deliverable',exclusion:'exclusion',pkg:'package',iter:'iteration',ms:'milestone'})[n.kind]||''}" data-ctx-id="${esc(n.id)}" data-ctx-label="${esc(n.label)}"><rect x="${p.x}" y="${p.y+1}" width="${colW}" height="${rowH-3}" rx="4" fill="var(--panel)" stroke="${KC[n.kind]}" stroke-width="1.2"/><text x="${p.x+6}" y="${p.y+13}" font-size="10" fill="var(--ink)">${esc(n.label.length>36?n.label.slice(0,35)+'…':n.label)}</text></g>`; });
  s+='</svg></div>';
  s+=`<div class="legend"><span><i style="background:#1f4e8c"></i>mission / mission-achievement goal</span><span><i style="background:#4a6fa5"></i>scope statement, area (product layer)</span><span><i style="background:#8a3a3a"></i>exclusion, exclusion guard</span><span><i style="background:#2e7d5b"></i>scope-coverage goal, objective</span><span><i style="background:#7a7a7a"></i>containment guard, iteration</span><span><i style="background:#6a5acd"></i>work item (grouped by investment category)</span><span><i style="background:#b8641c"></i>deliverable, milestone</span><span><i style="background:#c48a1a"></i>roadmap package</span></div>`;
  const layersPresent=[...new Set(D.areas.map(a=>a.layer))]; const taxNote = `Scope taxonomy as the register holds it: areas in ${layersPresent.length} layer${layersPresent.length===1?'':'s'} (${layersPresent.join(', ').toLowerCase()}); ${layersPresent.includes('Work')?'':'no work-layer area and therefore no productViewOf pairing; '}${D.deliverables.some(d=>d.kind)?'':'no deliverable carries a product-scope kind (functional / non-functional); '}the framework offers both and the register does not yet use them.`;
  s+=`<p class="small muted" style="margin:6px 0 0">${esc(taxNote)}</p>`;
  s+=`<p class="small muted" style="margin:6px 0 0">${nodes.length} elements and ${edges.length} typed relations, all read from the register. Hover an element to light its path upstream to the mission and downstream to its milestones (monotone in the chain, so the whole graph does not light up); click to open it; right-click for actions. Dashed edges are derived, not asserted: BRSF has no relation from a package to the deliverables it delivers, so the chart derives it through each package's work items and their satisfiesDeliverable; a proposal to make it assertable and checkable is in the framework's inbox. Not drawn here, by design: the stage outputs and their commit witnesses (see the intent-chain model), the external dependency and proposals (dependency model), blueprint entities and coverage gaps (coverage model), Definition-of-Done criteria, compliance obligations, metrics and observations (register explorer and appendices).</p>`;
  return s;
}

function initLineageModel(){
  const svg=$('#lin-svg'); if(!svg) return;
  const col={}; $$('#lin-svg .ln').forEach(n=>col[n.dataset.id]=+n.dataset.col);
  const adj={}; $$('#lin-svg .ledge').forEach(p=>{ (adj[p.dataset.a]=adj[p.dataset.a]||new Set()).add(p.dataset.b); (adj[p.dataset.b]=adj[p.dataset.b]||new Set()).add(p.dataset.a); });
  // the path THROUGH an element: everything reachable moving only leftwards from it, plus everything reachable moving only rightwards — not the whole connected graph
  const level=id=> id==='Scope' ? 0.5 : col[id]; // the statement is the hub between the mission and its areas, deliverables and exclusions
  const reachDir=(id,dir)=>{ const seen=new Set([id]); const q=[id]; while(q.length){ const x=q.shift(); (adj[x]||[]).forEach(y=>{ if(!seen.has(y) && Math.sign(level(y)-level(x))===dir){ seen.add(y); q.push(y); } }); } return seen; };
  const reach=id=>new Set([...reachDir(id,-1),...reachDir(id,1)]);
  const hi=id=>{ const set=id?reach(id):null; $$('#lin-svg .ledge').forEach(p=>{ const on=set&&set.has(p.dataset.a)&&set.has(p.dataset.b); p.setAttribute('stroke',on?'var(--accent)':'var(--line)'); p.setAttribute('stroke-width',on?'2':'1.1'); p.setAttribute('opacity', set&&!on?'.15':(on?'1':'.8')); }); $$('#lin-svg .ln').forEach(n=>{ n.style.opacity = set&&!set.has(n.dataset.id) ? '.3' : '1'; }); };
  svg.addEventListener('mouseover',e=>{ const n=e.target.closest('.ln'); if(n) hi(n.dataset.id); }); svg.addEventListener('mouseout',()=>hi(null));
  svg.addEventListener('click',e=>{ const n=e.target.closest('.ln'); if(!n) return; const k=n.dataset.kind,id=n.dataset.id; if(k==='wi') selectItem(id); else if(k==='goal') selectIntent('goal',id); else if(k==='objective') selectIntent('objective',id); else if(k==='area') selectScope('area',id); else if(k==='del') selectScope('deliverable',id); else if(k==='exclusion') selectScope('exclusion',id); else if(k==='pkg') selectDelivery('package',id); else if(k==='iter') selectDelivery('iteration',id); else if(k==='ms') selectDelivery('milestone',id); else if(k==='mission'||k==='scope') goto('proposal', k==='mission'?'intent':'intent', k==='mission'?'#sec-3-mission':'#sec-4-scope'); });
  $('#lin-toolbar').addEventListener('change',e=>{ const cb=e.target.closest('input[data-edge]'); if(!cb) return; $$('#lin-svg .ledge[data-rel="'+cb.dataset.edge+'"]').forEach(p=>p.style.display=cb.checked?'':'none'); });
}
