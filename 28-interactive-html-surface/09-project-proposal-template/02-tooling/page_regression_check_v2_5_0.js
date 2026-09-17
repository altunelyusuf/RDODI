#!/usr/bin/env node
// page_regression_check_v2_5_0.js (v2.5.0: version-freeze fix, G94) — operate every control of the generated Stage 4 page and check what it shows.
// v2.5.0: renamed from v2_4_0.js, which had been content-edited 6 times under one frozen filename before anything checked it -- the same class of gap independently found and fixed this session in backlog-roadmap-framework's own lineage discipline document and its main shapes file. No attempt made to retroactively assign real version numbers to those 6 edits; one honest bump marks the point this stopped being silent.
// v2.1.0: sub-pages and sub-tabs, Explorer tree (expand/collapse all, icons, deeper levels), ontology graphs with
// detail cards, context menus and tooltips (page generator v2.0.0).
// Lessons carried from v1.0.0 (04-documentation/why_the_faults_kept_coming_back_v1_0_0.md): address elements by
// id, never by tag; click EVERY item, not the first; compare what is shown against what the register holds.
// Usage: node 03-tooling/page_regression_check_v2_4_0.js <page.html>   (needs jsdom; NODE_PATH may point at it)
// Exit 0 when every check passes, 2 otherwise. L-95: the check is proven to fail on a page whose register data
// is tampered (see the changelog entry for the release that shipped it).
const fs = require('fs'); const path = require('path');
const { JSDOM } = require('jsdom');
const file = process.argv[2]; if (!file) { console.error('usage: page_regression_check_v2_0_0.js <page.html>'); process.exit(1); }
const html = fs.readFileSync(file, 'utf8');
const errors = [];
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, beforeParse(w) { w.scrollTo = () => {}; w.HTMLElement.prototype.scrollIntoView = function(){}; w.URL.createObjectURL = () => 'blob:x'; w.print = () => {}; w.addEventListener('error', e => errors.push(e.message)); } });
const w = dom.window, d = w.document;
const results = []; const check = (name, ok, detail) => { results.push([name, !!ok, detail || '']); };
// register data as the page embeds it
const D = JSON.parse(d.getElementById('data').textContent);
const items = Object.values(D.items);
// 1. tabs
const tabs = Array.from(d.querySelectorAll('#tabs button[data-tab]'));
check('Seven top tabs exist', tabs.length === 7, String(tabs.length));
let allViews = true;
tabs.forEach(b => { b.click(); const v = d.getElementById('view-' + b.dataset.tab); if (!v || !v.classList.contains('active') || v.textContent.trim().length < 50) allViews = false; });
check('Every tab opens a view with content', allViews);
// 2. proposal document
tabs[0].click();
const h1s = Array.from(d.querySelectorAll('#view-proposal h2.doc-h1')).map(h => h.textContent);
check('Proposal has the 20 numbered sections plus abstract, abbreviations and references', h1s.filter(t => /^\d+\. /.test(t)).length === 20 && h1s.includes('Abstract') && h1s.includes('List of Abbreviations') && h1s.includes('References'), h1s.length + ' headings');
check('Section numbering starts at 1 and is contiguous', h1s.filter(t => /^\d+\. /.test(t)).map(t => +t.split('.')[0]).every((n, i) => n === i + 1));
const cites = Array.from(d.querySelectorAll('#view-proposal a.cite')); const refs = Array.from(d.querySelectorAll('#view-proposal p.ref'));
check('Every in-text citation resolves to a reference paragraph', cites.length > 0 && cites.every(a => d.getElementById('ref-' + a.dataset.ref)), cites.length + ' citations, ' + refs.length + ' references');
const tabrefs = Array.from(d.querySelectorAll('#view-proposal a.tabref, #view-appendix a.tabref'));
check('Every table reference resolves to a numbered table', tabrefs.length > 0 && tabrefs.every(a => d.querySelector(a.getAttribute('href'))), tabrefs.length + ' table references');
// 3. abbreviations
const abbrRows = d.querySelectorAll('#abbr-block tbody tr').length; const abbrUsed = new Set(Array.from(d.querySelectorAll('#view-proposal abbr.ab')).map(a => a.textContent));
check('Abbreviation list present and every listed abbreviation carries a tooltip in the prose or appendix tables', abbrRows > 10, abbrRows + ' listed, ' + abbrUsed.size + ' marked in prose');
// 3b. sub-pages: every sub-tab opens a pane with content
let subOK = true, subN = 0;
tabs.forEach(b => { b.click(); Array.from(d.querySelectorAll('#view-' + b.dataset.tab + ' .subtabs button[data-pane]')).forEach(sb => { sb.click(); subN++; const pane = d.querySelector('#view-' + b.dataset.tab + ' .pane.active'); if (!pane || pane.dataset.pane !== sb.dataset.pane || pane.textContent.trim().length < 30) subOK = false; }); });
check('Every sub-tab opens its own sub-page with content', subOK && subN >= 24, subN + ' sub-tabs');
tabs[0].click(); const propPanes = Array.from(d.querySelectorAll('#view-proposal .pane')).map(p => p.dataset.pane);
check('Proposal is split into front matter, four section groups and references', propPanes.join(',') === 'front,intent,plan,delivery,governance,refs', propPanes.join(','));
tabs[5].click(); check('Each appendix is its own sub-page', Array.from(d.querySelectorAll('#view-appendix .pane')).length === 7);
// 4. sidebar tree — click every node on every tab
let treeClicks = 0, treeFail = 0;
tabs.forEach(b => { b.click(); Array.from(d.querySelectorAll('#tree .node')).forEach(n => { try { n.click(); treeClicks++; } catch (e) { treeFail++; } }); });
check('Every sidebar tree node on every tab can be clicked', treeFail === 0 && treeClicks > 150, treeClicks + ' clicks, ' + treeFail + ' failures');
tabs[1].click(); const depth = Math.max(...Array.from(d.querySelectorAll('#tree .node')).map(n => { let k = 0, e = n; while ((e = e.parentElement) && e.id !== 'tree') if (e.tagName === 'UL') k++; return k; }));
check('Tree is at least three levels deep on the register tab', depth >= 3, 'depth ' + depth);
check('Every tree node carries an icon and a short label', Array.from(d.querySelectorAll('#tree .node')).every(n => n.querySelector('.ico') && n.querySelector('.lbl').textContent.length < 90));
d.getElementById('collapseall').click(); const collapsed = Array.from(d.querySelectorAll('#tree li')).filter(li => li.querySelector(':scope>ul')).every(li => li.classList.contains('collapsed'));
d.getElementById('expandall').click(); const expanded = Array.from(d.querySelectorAll('#tree li')).every(li => !li.classList.contains('collapsed'));
check('Collapse all and expand all work', collapsed && expanded);
const tw = d.querySelector('#tree li ul li .tw:not(.leaf)'); if (tw) { tw.click(); } check('A chevron toggles its own branch', tw && tw.closest('li').classList.contains('collapsed'));
d.getElementById('sidefilter').value = 'mission'; d.getElementById('sidefilter').dispatchEvent(new w.Event('input'));
check('Sidebar filter hides non-matching nodes', Array.from(d.querySelectorAll('#tree li')).some(li => li.style.display === 'none'));
d.getElementById('sidefilter').value = ''; d.getElementById('sidefilter').dispatchEvent(new w.Event('input'));
// 5. register explorer — every card, every filter
tabs[1].click(); d.getElementById('f-clear').click();
const cards = Array.from(d.querySelectorAll('#wi-list .card'));
check('Explorer shows one card per work item', cards.length === items.length, cards.length + '/' + items.length);
let detailOK = true; cards.forEach(c => { c.click(); const t = d.getElementById('wi-detail').textContent; if (!t.includes(D.items[c.dataset.id].label) || !t.includes('Pursues objective')) detailOK = false; });
check('Clicking every card shows that item in the detail pane', detailOK);
const setSel = (id, v) => { const s = d.getElementById(id); s.value = v; s.dispatchEvent(new w.Event('input')); };
let filterOK = true;
D.packages.forEach(p => { setSel('f-pkg', p.id); const n = d.querySelectorAll('#wi-list .card').length; if (n !== p.members.length) filterOK = false; }); setSel('f-pkg', '');
['Now', 'Next', 'Later'].forEach(h => { setSel('f-hz', h); if (d.querySelectorAll('#wi-list .card').length !== (D.horizons[h] || []).length) filterOK = false; }); setSel('f-hz', '');
setSel('f-ext', 'yes'); if (d.querySelectorAll('#wi-list .card').length !== items.filter(x => x.external).length) filterOK = false; setSel('f-ext', 'up'); if (d.querySelectorAll('#wi-list .card').length !== items.filter(x => x.needs_upstream).length) filterOK = false; setSel('f-ext', '');
check('Package, horizon and dependency filters return exactly the register counts', filterOK);
d.getElementById('f-clear').click(); check('Clear filters restores every card', d.querySelectorAll('#wi-list .card').length === items.length);
const si = d.getElementById('wi-search'); si.value = 'enumerator'; si.dispatchEvent(new w.Event('input'));
check('Search narrows the list and finds the enumerator item', d.querySelectorAll('#wi-list .card').length > 0 && d.querySelectorAll('#wi-list .card').length < items.length && d.getElementById('wi-list').textContent.includes('enumerator'));
si.value = 'zzzz-no-such'; si.dispatchEvent(new w.Event('input')); check('An empty search result tells the reader', d.getElementById('wi-list').textContent.includes('No work item')); si.value = ''; si.dispatchEvent(new w.Event('input'));
// 5b. other explorer panes and chips
tabs[1].click(); let paneOK = true; [['intent', D.goals.length + D.objectives.length], ['scope', D.areas.length + D.deliverables.length + D.exclusions.length], ['delivery', D.packages.length + D.iterations.length + D.milestones.length]].forEach(([p, n]) => { d.querySelector('#sub-register button[data-pane="' + p + '"]').click(); const cs = Array.from(d.querySelectorAll('#view-register .pane.active .card')); if (cs.length !== n) paneOK = false; cs.forEach(c => { c.click(); const det = d.querySelector('#' + p + '-detail'); if (!det.textContent.includes(c.querySelector('h4').textContent)) paneOK = false; }); });
check('Goals/objectives, scope and delivery panes show every element and open its card', paneOK);
d.querySelector('#sub-register button[data-pane="items"]').click(); d.getElementById('f-clear').click(); d.querySelector('#wi-list .card').click(); const chipBtn = d.querySelector('#wi-detail [data-go-kind="objective"]'); if (chipBtn) chipBtn.click();
check('A chip in a detail card navigates to the related element', chipBtn && d.querySelector('#view-register .pane.active').dataset.pane === 'intent' && d.getElementById('intent-detail').textContent.includes('objective'));
// 5c. context menu and tooltip
tabs[1].click(); d.querySelector('#sub-register button[data-pane="items"]').click(); const card = d.querySelector('#wi-list .card'); card.dispatchEvent(new w.MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 100, clientY: 100 }));
const ctxItems = Array.from(d.querySelectorAll('#ctx [data-i]')); check('Right-clicking a card opens a context menu with actions', d.getElementById('ctx').style.display === 'block' && ctxItems.length >= 5, ctxItems.length + ' entries');
const openEntry = ctxItems.find(x => /lineage traceability/i.test(x.textContent)); if (openEntry) openEntry.click(); check('A context-menu action navigates', openEntry && d.getElementById('view-models').classList.contains('active') && d.querySelector('#view-models .pane.active').dataset.pane === 'm-lineage');
tabs[1].click(); const treeNode = d.querySelector('#tree .node[data-ref-kind]'); treeNode.dispatchEvent(new w.MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 50, clientY: 50 })); check('Right-clicking a tree node opens a context menu', d.getElementById('ctx').style.display === 'block' && d.querySelectorAll('#ctx [data-i]').length >= 3); d.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Escape' }));
check('Escape closes the context menu', d.getElementById('ctx').style.display === 'none');
d.querySelector('#sub-register button[data-pane="items"]').click(); const tipCard = d.querySelector('#wi-list .card[data-tip]'); tipCard.dispatchEvent(new w.MouseEvent('mouseover', { bubbles: true })); check('Hovering a card shows a tooltip', d.getElementById('tip').style.display === 'block' && d.getElementById('tip').textContent.length > 10);
// 6. visual models — every model rendered as SVG, nodes clickable
tabs[2].click(); Array.from(d.querySelectorAll('#sub-models button')).forEach(b => b.click());
const vizes = Array.from(d.querySelectorAll('#models .viz'));
check('Eight visual models rendered as SVG, each on its own sub-page (one lineage chart)', vizes.length === 8 && vizes.every(v => v.querySelector('svg') && v.querySelector('svg').innerHTML.length > 200) && d.querySelectorAll('#sub-models button').length === 8 && !d.getElementById('m-trace'), vizes.length);
const lin = d.querySelectorAll('#lin-svg .ln').length, linExpected = 2 + D.areas.length + D.exclusions.length + D.goals.length + D.objectives.length + items.length + D.deliverables.length + D.packages.length + D.iterations.length + D.milestones.length;
check('Full-lineage model draws mission, scope, areas, exclusions, goals, objectives, items, deliverables, packages, iterations and milestones', lin === linExpected, lin + '/' + linExpected);
check('Full-lineage model groups goals by facing and items by investment category', /mission-achievement goals/i.test(d.getElementById('m-lineage').textContent) && /scope-coverage goals/i.test(d.getElementById('m-lineage').textContent) && /new capability/i.test(d.getElementById('m-lineage').textContent));
check('Title and subtitle come from the project data, not the shell', d.title.startsWith(D.project.title) && d.querySelector('header.top h1').textContent === D.project.title && d.querySelector('header.top .sub').textContent.includes(D.project.subtitle));
check('Full-lineage model has every typed relation kind switchable', d.querySelectorAll('#lin-toolbar input[data-edge]').length === 17 && d.querySelectorAll('#lin-svg .ledge').length > 100, d.querySelectorAll('#lin-svg .ledge').length + ' edges');
const cb = d.querySelector('#lin-toolbar input[data-edge="pursuesObjective"]'); cb.checked = false; cb.dispatchEvent(new w.Event('change', { bubbles: true })); check('Switching an edge kind off hides those edges', Array.from(d.querySelectorAll('#lin-svg .ledge[data-rel="pursuesObjective"]')).every(p => p.style.display === 'none')); cb.checked = true; cb.dispatchEvent(new w.Event('change', { bubbles: true }));
check('Scope statement is linked to the mission (scopeForMission, as the register asserts)', d.querySelectorAll('#lin-svg .ledge[data-rel="scopeForMission"]').length === 1);
check('Scope statement is linked to every area, deliverable and exclusion (coversArea, requiresDeliverable, hasScopeExclusion)', d.querySelectorAll('#lin-svg .ledge[data-rel="coversArea"]').length === D.areas.length && d.querySelectorAll('#lin-svg .ledge[data-rel="requiresDeliverable"]').length === D.deliverables.length && d.querySelectorAll('#lin-svg .ledge[data-rel="hasScopeExclusion"]').length === D.exclusions.length);
check('Every package reaches at least one deliverable through its items (derived, dashed)', D.packages.every(p => d.querySelectorAll('#lin-svg .ledge[data-rel="deliversDeliverable"][data-a="' + p.id + '"]').length >= 1) && Array.from(d.querySelectorAll('#lin-svg .ledge[data-rel="deliversDeliverable"]')).every(e => e.getAttribute('stroke-dasharray')));
const areaNode = d.querySelector('#lin-svg .ln[data-kind="area"]'); areaNode.dispatchEvent(new w.MouseEvent('mouseover', { bubbles: true })); check('Hovering an area lights its path through the statement to the mission', Array.from(d.querySelectorAll('#lin-svg .ledge[stroke="var(--accent)"]')).some(e => e.dataset.rel === 'scopeForMission') && Array.from(d.querySelectorAll('#lin-svg .ledge[stroke="var(--accent)"]')).some(e => e.dataset.rel === 'coversArea'));
check('Scope taxonomy note states what the register does not yet use', /no work-layer area/.test(d.getElementById('m-lineage').textContent) && /product-scope kind/.test(d.getElementById('m-lineage').textContent));
const goalNode = d.querySelector('#lin-svg .ln[data-kind="goal"]'); goalNode.dispatchEvent(new w.MouseEvent('mouseover', { bubbles: true })); check('Hovering a goal lights a path reaching the mission and a work item', d.querySelectorAll('#lin-svg .ledge[stroke="var(--accent)"]').length >= 3);
let vizClicks = 0; Array.from(d.querySelectorAll('#models .node-rect')).forEach(n => { n.dispatchEvent(new w.MouseEvent('click', { bubbles: true })); vizClicks++; });
check('Every node in every model can be clicked', vizClicks > 40, vizClicks + ' nodes');
check('Roadmap shows every iteration, package and milestone', d.getElementById('m-roadmap').querySelectorAll('[data-pkg]').length === D.packages.length && d.getElementById('m-roadmap').querySelectorAll('[data-ms]').length === D.milestones.length && (d.getElementById('m-roadmap').textContent.match(/Iteration \d/g) || []).length === D.iterations.length);
check('Coverage model marks every recorded gap', d.querySelectorAll('#m-coverage [data-ent]').length === D.blueprint.entities.length * 4 && (d.getElementById('m-coverage').textContent.match(/gap \(recorded\)/g) || []).length === D.gaps.length);
check('Pipeline model shows five agents', d.querySelectorAll('#m-pipeline [data-agent]').length === 5);
// 7. ontology graphs
tabs[3].click(); d.querySelector('#sub-ontology button[data-pane="project"]').click();
const gp = d.querySelectorAll('#g-project .gnode'); check('Project ontology graph draws every class, property, individual and aligned framework class', gp.length === D.graphs.project.nodes.length && d.querySelectorAll('#g-project .gedge').length === D.graphs.project.edges.length, gp.length + ' nodes');
let cardOK = true; D.graphs.project.nodes.forEach(node => { const n = d.querySelector('#g-project .gnode[data-id="' + node.id + '"]'); if (!n) { cardOK = false; return; } n.dispatchEvent(new w.MouseEvent('click', { bubbles: true })); const det = d.getElementById('d-project').textContent; if (!det.includes(node.label) || !det.includes('Outgoing')) cardOK = false; });
check('Clicking every ontology node opens its detail card with its relations', cardOK);
const sel = d.querySelector('#g-project .gnode.sel'); check('The selected node is highlighted and its edges emphasised', sel && d.querySelectorAll('#g-project .gedge.hi').length >= 0);
d.querySelector('#g-project [data-filter]').value = 'class'; d.querySelector('#g-project [data-filter]').dispatchEvent(new w.Event('change')); check('Graph filter shows only the chosen kind (plus the selected node)', Math.abs(d.querySelectorAll('#g-project .gnode').length - D.graphs.project.nodes.filter(x => x.kind === 'class').length) <= 1);
d.querySelector('#g-project [data-filter]').value = ''; d.querySelector('#g-project [data-filter]').dispatchEvent(new w.Event('change'));
gp[0] && d.querySelector('#g-project .gnode').dispatchEvent(new w.MouseEvent('contextmenu', { bubbles: true, cancelable: true, clientX: 60, clientY: 60 })); check('Right-clicking a graph node opens a context menu', d.getElementById('ctx').style.display === 'block'); d.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Escape' }));
d.querySelector('#sub-ontology button[data-pane="register"]').click(); const gr = d.querySelectorAll('#g-register .gnode'); check('Register graph draws every lineage individual with typed relations', gr.length === D.graphs.register.nodes.length && d.querySelectorAll('#g-register .gedge').length === D.graphs.register.edges.length, gr.length + ' nodes, ' + d.querySelectorAll('#g-register .gedge').length + ' edges');
let regCardOK = true; D.graphs.register.nodes.forEach(node => { const n = d.querySelector('#g-register .gnode[data-id="' + node.id + '"]'); if (!n) { regCardOK = false; return; } n.dispatchEvent(new w.MouseEvent('click', { bubbles: true })); if (!d.getElementById('d-register').textContent.includes(node.label)) regCardOK = false; }); check('Clicking every register node opens its card', regCardOK);
d.querySelector('#sub-ontology button[data-pane="alignment"]').click(); check('Alignment pane lists every project concept and every domain entity', d.querySelectorAll('#alignment .card').length === D.tbox.length + D.blueprint.entities.length);
// 8. console — every suggested question answers with a grounding
tabs[4].click(); const suggest = Array.from(d.querySelectorAll('#suggest button')); let answered = 0; suggest.forEach(b => { b.click(); const turns = d.querySelectorAll('#chat .turn.a'); const last = turns[turns.length - 1]; if (last && last.textContent.includes('Grounded in') && !last.textContent.includes('No register element')) answered++; });
check('Every suggested question is answered with a grounding', answered === suggest.length, answered + '/' + suggest.length);
d.getElementById('askinput').value = 'qwertyuiop'; d.getElementById('askbtn').click(); const t2 = d.querySelectorAll('#chat .turn.a'); check('A question with no match says so instead of inventing', t2[t2.length - 1].textContent.includes('No register element matches'));
d.getElementById('askinput').value = 'which work items depend on the framework'; d.getElementById('askbtn').click(); const t3 = d.querySelectorAll('#chat .turn.a'); check('Dependency question lists the register count', t3[t3.length - 1].textContent.includes('(' + items.filter(x => x.external).length + ')'));
// 9. appendix and provenance
tabs[5].click(); check('Appendices A to G present', ['A', 'B', 'C', 'D', 'E', 'F', 'G'].every(l => d.getElementById('view-appendix').textContent.includes('Appendix ' + l + '.')));
tabs[6].click(); check('Provenance names the register sources and generator', /lineage_/.test(d.getElementById('about').textContent) && d.getElementById('about').textContent.includes('page_from_register'));
// 10. register coverage — every label in the page
const text = d.body.textContent;
const missing = []; [D.goals, D.objectives, D.areas, D.deliverables, D.exclusions, D.packages, D.iterations, D.milestones, items, D.proposals].forEach(arr => arr.forEach(x => { if (!text.includes(x.label)) missing.push(x.label); }));
check('Every register element label appears in the page', missing.length === 0, missing.slice(0, 5).join(' | '));
const foreign = ['GraphCodeBERT', 'LangGraph', 'React', 'Fuseki', 'EP-1', 'PKG-1'].filter(t => text.includes(t));
check('No identifier of the retired plan appears', foreign.length === 0, foreign.join(','));
// 10b. embedded data agrees with the rendered document (a tampered data block must fail here)
const docText = d.getElementById('view-proposal').textContent + d.getElementById('view-appendix').textContent;
const disagree = [];
[D.goals, D.objectives, D.areas, D.deliverables, D.exclusions, D.packages, D.iterations, D.milestones, items, D.proposals].forEach(arr => arr.forEach(x => { if (!docText.includes(x.label)) disagree.push(x.label); }));
check('Embedded register data agrees with the rendered document', disagree.length === 0, disagree.slice(0, 3).join(' | '));
// 11. header controls and errors
d.getElementById('themebtn').click(); check('Theme toggle switches to dark', d.documentElement.dataset.theme === 'dark'); d.getElementById('themebtn').click();
d.getElementById('ttlbtn').click(); check('Register download produces Turtle', typeof w.LINEAGE_TTL === 'string' && w.LINEAGE_TTL.includes('backlog:'));
check('The page runs without script errors', errors.length === 0 && d.getElementById('errbanner').style.display !== 'block', errors.join(' | '));
// report
let pass = 0; results.forEach(([n, ok, det]) => { console.log((ok ? '  passed  ' : '  FAILED  ') + n + (det ? '  [' + det + ']' : '')); if (ok) pass++; });
console.log('\n' + pass + ' of ' + results.length + ' checks passed.');
process.exit(pass === results.length ? 0 : 2);
