const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,HeadingLevel,
       WidthType,BorderStyle,AlignmentType,PageBreak,TableOfContents,ExternalHyperlink}=require('docx');
const d=JSON.parse(fs.readFileSync('/tmp/report_full.json','utf8'));

const ACCENT='2D4A52', INK='2A3438', MUT='586272';
const mono=(t,sz=17)=>new TextRun({text:t,font:'Consolas',size:sz});
const run=(t,o={})=>new TextRun({text:t,...o});
function para(text,o={}){return new Paragraph({children:[run(text,o.run||{})],...o.p||{}});}
function codeBlock(code){
  return code.split('\n').map(line=>new Paragraph({
    children:[mono(line||' ')],spacing:{after:0,line:240},
    shading:{type:'clear',color:'auto',fill:'F4F2EC'},
    border:{left:{style:BorderStyle.SINGLE,size:18,color:ACCENT,space:6}}}));
}
function cell(text,{bold=false,fill=null,sz=18,mono=false}={}){
  const r=mono?new TextRun({text:String(text),font:'Consolas',size:sz}):new TextRun({text:String(text),bold,size:sz});
  return new TableCell({children:[new Paragraph({children:[r]})],...(fill?{shading:{type:'clear',color:'auto',fill}}:{}),margins:{top:40,bottom:40,left:80,right:80}});
}
function dataTable(cols,rows,{monoCols=[]}={}){
  const head=new TableRow({tableHeader:true,children:cols.map(c=>cell(c,{bold:true,fill:'EBE5D7',sz:17}))});
  const body=rows.map(r=>new TableRow({children:r.map((c,i)=>cell(c,{sz:17,mono:monoCols.includes(i)}))}));
  return new Table({width:{size:100,type:WidthType.PERCENTAGE},rows:[head,...body],
    borders:{top:{style:BorderStyle.SINGLE,size:4,color:'C8CFD2'},bottom:{style:BorderStyle.SINGLE,size:4,color:'C8CFD2'},
             left:{style:BorderStyle.SINGLE,size:4,color:'C8CFD2'},right:{style:BorderStyle.SINGLE,size:4,color:'C8CFD2'},
             insideHorizontal:{style:BorderStyle.SINGLE,size:2,color:'DDE3E5'},insideVertical:{style:BorderStyle.SINGLE,size:2,color:'DDE3E5'}}});
}
const kids=[];

// ---- TITLE PAGE ----
kids.push(new Paragraph({spacing:{before:2400}}));
kids.push(new Paragraph({alignment:AlignmentType.CENTER,children:[run(d.title,{bold:true,size:48,color:ACCENT})]}));
kids.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:240},children:[run(d.subtitle,{italics:true,size:26,color:MUT})]}));
kids.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:1200},children:[run('An academic treatment of semantic technologies, with worked examples across retail, logistics, healthcare and finance. Example schemas are grounded in real, cited public sources; example instances are clearly marked illustrative data.',{size:22,color:INK})]}));
kids.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:2400},children:[run('Generated mechanically from the domain ontology — structure, prose, worked examples and computed results all derive from scp_domain v3.16.0.',{size:18,italics:true,color:MUT})]}));
kids.push(new Paragraph({children:[new PageBreak()]}));

// ---- TOC ----
kids.push(new Paragraph({text:'Contents',heading:HeadingLevel.HEADING_1}));
kids.push(new TableOfContents('Contents',{hyperlink:true,headingStyleRange:'1-2'}));
kids.push(new Paragraph({children:[new PageBreak()]}));

// ---- INTRODUCTION ----
kids.push(new Paragraph({text:'1  Introduction',heading:HeadingLevel.HEADING_1}));
kids.push(para('Semantic technologies represent data as a graph of explicitly-typed relationships rather than as rows in fixed tables, so that meaning is machine-readable and shareable across systems. This report treats the field as a layered stack, from the foundational idea of a triple through the W3C standards (RDF, RDFS, OWL, SPARQL, SHACL, SKOS), the layered organization of ontologies, and the modern synthesis of knowledge graphs with large language models.',{run:{size:22}}));
kids.push(para('Every section, definition, worked example and result table in this report is generated mechanically from a single source ontology. Where an example is executable, its result table is computed by loading the code into an RDF engine at build time — so the shown result is the real output of the shown code, not a hand-written illustration.',{run:{size:22},p:{spacing:{before:120}}}));

// ---- PROVENANCE NOTE ----
kids.push(new Paragraph({text:'1.1  A note on provenance',heading:HeadingLevel.HEADING_2}));
kids.push(para('Academic honesty requires distinguishing real, cited facts from invented teaching data. Throughout, three kinds of content are used: (a) real, publicly verifiable facts with a citation; (b) standard public patterns (e.g. the shape of a SKOS concept) as defined by their specifications; and (c) clearly-illustrative synthetic data in the ex: namespace, which never asserts a real-company specific without a source.',{run:{size:22}}));

// ---- AREA SECTIONS ----
let sec=2;
for(const A of d.areas){
  kids.push(new Paragraph({children:[new PageBreak()]}));
  kids.push(new Paragraph({text:`${sec}  ${A.short}`,heading:HeadingLevel.HEADING_1}));
  if(A.intro)kids.push(para(A.intro,{run:{size:22}}));
  let sub=1;
  for(const C of A.concepts){
    kids.push(new Paragraph({text:`${sec}.${sub}  ${C.name}`,heading:HeadingLevel.HEADING_2}));
    if(C.treatment)kids.push(para(C.treatment,{run:{size:22}}));
    // examples
    for(const ex of C.examples){
      if(ex.text)kids.push(para('Worked example'+(ex.domain?` (${ex.domain})`:'')+': '+ex.text,{run:{size:21,italics:true},p:{spacing:{before:120}}}));
      if(ex.code){
        kids.push(para('Code'+(ex.lang?` (${ex.lang})`:'')+':',{run:{size:18,bold:true,color:MUT},p:{spacing:{before:60}}}));
        kids.push(...codeBlock(ex.code));
      }
      if(ex.idgloss){
        kids.push(para('What the identifiers mean:',{run:{size:18,bold:true,color:MUT},p:{spacing:{before:60}}}));
        kids.push(dataTable(['ID','meaning','notes'],ex.idgloss.entries.map(e=>[e[0],e[1],e[3]]),{monoCols:[0]}));
        if(ex.idgloss.reads_as)kids.push(para('Reads as: '+ex.idgloss.reads_as,{run:{size:20,italics:true},p:{spacing:{before:60}}}));
      }
      if(ex.computed){
        kids.push(para('Result (computed by executing the code above):',{run:{size:18,bold:true,color:'3F7A4D'},p:{spacing:{before:60}}}));
        kids.push(dataTable(ex.computed.cols,ex.computed.rows,{monoCols:[0,1]}));
      }
    }
    // specials
    renderSpecials(C.specials,kids,dataTable,para,codeBlock,run);
    sub++;
  }
  sec++;
}

// ---- FORMAL AXIOMS SECTION ----
kids.push(new Paragraph({children:[new PageBreak()]}));
kids.push(new Paragraph({text:`${sec}  The domain ontology: formal structure`,heading:HeadingLevel.HEADING_1}));
kids.push(para(`Beyond prose, the concepts above are related by ${d.axioms.object_property_count} object properties that make the dependencies explicit and machine-checkable. The relationships asserted between concepts are:`,{run:{size:22}}));
kids.push(dataTable(['Concept','relationship','Concept'],d.axioms.relationships,{monoCols:[1]}));
kids.push(para('Disjointness axioms record which concepts are mutually exclusive; a reasoner uses them to detect contradictory data. The ontology was verified consistent (OWL-RL closure, no unsatisfiable classes). The disjoint pairs are:',{run:{size:22},p:{spacing:{before:120}}}));
kids.push(dataTable(['Concept','is disjoint with'],d.axioms.disjoint));
sec++;

// ---- REFERENCES ----
kids.push(new Paragraph({children:[new PageBreak()]}));
kids.push(new Paragraph({text:`${sec}  References`,heading:HeadingLevel.HEADING_1}));
d.publications.forEach((p,i)=>{
  const parts=[run(`[${i+1}] `,{size:20,bold:true})];
  if(p.author)parts.push(run(p.author+'. ',{size:20}));
  parts.push(run(p.title+'. ',{size:20,italics:true}));
  if(p.url)parts.push(new ExternalHyperlink({children:[run(p.url,{size:18,color:'2D4A52',underline:{}})],link:p.url}));
  kids.push(new Paragraph({children:parts,spacing:{after:80}}));
  if(p.note)kids.push(para('     '+p.note,{run:{size:17,color:MUT,italics:true},p:{spacing:{after:120}}}));
});

// specials renderer
function renderSpecials(sp,kids,dataTable,para,codeBlock,run){
  if(sp.layeredArchitecture){
    const la=sp.layeredArchitecture;
    kids.push(para(la.title||'Layered architecture',{run:{size:20,bold:true,color:'2D4A52'},p:{spacing:{before:120}}}));
    if(la.intro)kids.push(para(la.intro,{run:{size:21}}));
    la.layers.forEach(L=>kids.push(para(`• ${L.name}: ${L.role}  [${(L.contents||[]).join(', ')}]`,{run:{size:20}})));
    if(la.mapping)kids.push(dataTable(la.mapping.cols,la.mapping.rows,{monoCols:[0,1]}));
    if(la.takeaway)kids.push(para(la.takeaway,{run:{size:20,italics:true},p:{spacing:{before:60}}}));
  }
  if(sp.modelComparison){
    const mc=sp.modelComparison;
    kids.push(para('Model comparison'+(mc.scenario?': '+mc.scenario:''),{run:{size:20,bold:true,color:'2D4A52'},p:{spacing:{before:120}}}));
    (mc.lenses||[]).forEach(L=>{ if(L.note)kids.push(para(`• ${L.title||L.key}: ${L.note}`,{run:{size:20}})); });
  }
  if(sp.techCompareRich){
    const tc=sp.techCompareRich;
    kids.push(para('How other technologies would handle this'+(tc.scenario?': '+tc.scenario:''),{run:{size:20,bold:true,color:'2D4A52'},p:{spacing:{before:120}}}));
    (tc.techs||[]).forEach(t=>kids.push(para(`• ${t.tech}: ${t.note}`,{run:{size:20}})));
    if(tc.table_summary)kids.push(dataTable(tc.table_summary.cols,tc.table_summary.rows));
  }
  if(sp.inferenceContrast){
    const ic=sp.inferenceContrast;
    kids.push(para('Inference contrast',{run:{size:20,bold:true,color:'2D4A52'},p:{spacing:{before:120}}}));
    (ic.cards||[]).forEach(c=>{ if(c.title)kids.push(para(`• ${c.title}: ${c.note||''}`,{run:{size:20}})); });
  }
  if(sp.axiomReference){
    const ax=sp.axiomReference;
    const rows=[];
    (ax.groups||[]).forEach(grp=>(grp.rows||[]).forEach(r=>rows.push(r)));
    if(rows.length){kids.push(para('OWL axiom reference',{run:{size:20,bold:true,color:'2D4A52'},p:{spacing:{before:120}}}));
      kids.push(dataTable(ax.cols||['Axiom','Meaning'],rows.slice(0,24),{monoCols:[0]}));}
  }
}

const doc=new Document({
  features:{updateFields:true},
  styles:{default:{document:{run:{font:'Georgia',size:22,color:INK}}},
    paragraphStyles:[
     {id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:30,bold:true,font:'Arial',color:ACCENT},paragraph:{spacing:{before:280,after:160},outlineLevel:0}},
     {id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:24,bold:true,font:'Arial',color:'3A4750'},paragraph:{spacing:{before:200,after:120},outlineLevel:1}}]},
  sections:[{properties:{page:{size:{width:12240,height:15840},margin:{top:1440,right:1440,bottom:1440,left:1440}}},children:kids}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync('/tmp/scp_report.docx',b);console.log('wrote scp_report.docx ('+kids.length+' blocks)');});
