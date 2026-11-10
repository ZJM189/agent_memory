import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const PptxGenJS=require('pptxgenjs');
const [sceneArg,outArg]=process.argv.slice(2);
if(!sceneArg||!outArg){console.error('Usage: node scripts/build.mjs <scene.json> <new-output.pptx>');process.exit(2);}
const input=path.resolve(sceneArg),output=path.resolve(outArg);
try {
 if(path.extname(output).toLowerCase()!=='.pptx')throw new Error('Output must end in .pptx');
 try{await fs.access(output);throw new Error('Output already exists; choose a new filename.');}catch(e){if(e.code!=='ENOENT')throw e;}
 const d=JSON.parse((await fs.readFile(input,'utf8')).replace(/^\uFEFF/,''));
 const width=d.width??13.333333,height=d.height??7.5;
 if(!Number.isFinite(width)||!Number.isFinite(height)||width<=0||height<=0)throw new Error('Invalid slide size.');
 if(!Array.isArray(d.slides)||!d.slides.length)throw new Error('At least one slide required.');
 const pptx=new PptxGenJS();pptx.defineLayout({name:'CUSTOM',width,height});pptx.layout='CUSTOM';
 const font=d.fontFace||'Arial';pptx.theme={headFontFace:font,bodyFontFace:font,lang:d.lang||'zh-CN'};
 pptx.author=d.author||'PptxGenJS Skill';pptx.subject=d.subject||'';pptx.title=d.title||'';pptx.company='';
 let count=0;
 function color(s){return typeof s==='string'?s.replace(/^#/,''):s;}
 function fill(s){return s==='none'?{color:'FFFFFF',transparency:100}:typeof s==='string'?{color:color(s)}:s;}
 function line(s){return s==='none'?{color:'FFFFFF',transparency:100}:typeof s==='string'?{color:color(s)}:s;}
 for(const [si,data] of d.slides.entries()){
  const slide=pptx.addSlide();slide.background={color:color(data.background||'FFFFFF')};
  if(data.notes)slide.addNotes(data.notes);
  for(const [ei,e]of(data.elements||[]).entries()){
   const label=`slide ${si+1} element ${ei+1} (${e.type})`;
   for(const k of ['x','y','w','h'])if(!Number.isFinite(e[k])||e[k]<0)throw new Error(`${label}: invalid ${k}`);
   if(e.x+e.w>width+.015||e.y+e.h>height+.015)throw new Error(`${label}: outside slide`);
   const pos={x:e.x,y:e.y,w:e.w,h:e.h,objectName:e.name||`${e.type}-${ei+1}`};
   if(e.type==='text'){
    if(typeof e.text!=='string')throw new Error(`${label}: text must be a string`);
    const opts={...pos,fontFace:e.fontFace||font,fontSize:e.fontSize??18,color:color(e.color||'082F60'),margin:e.margin??0,align:e.align||'left',valign:e.valign||'mid',breakLine:false};
    for(const k of ['bold','italic','paraSpaceAfterPt','transparency','charSpacing','lineSpacingMultiple'])if(e[k]!==undefined)opts[k]=e[k];
    slide.addText(e.text,opts);
   }else if(e.type==='shape'){
    const geom=pptx.ShapeType[e.shape||'rect'];if(!geom)throw new Error(`${label}: unknown shape ${e.shape}`);
    slide.addShape(geom,{...pos,fill:fill(e.fill||'none'),line:line(e.line||'none'),radius:e.radius??.15,rotate:e.rotate??0});
   }else if(e.type==='line'){
    slide.addShape(pptx.ShapeType.line,{...pos,line:{color:color(e.color||'0878D8'),width:e.width??1,beginArrowType:e.beginArrowType,endArrowType:e.endArrowType}});
   }else if(e.type==='image'){
    if(typeof e.path!=='string')throw new Error(`${label}: image path required`);
    const imagePath=path.resolve(path.dirname(input),e.path);await fs.access(imagePath);
    slide.addImage({...pos,path:imagePath,altText:e.alt||e.name||''});
   }else if(e.type==='table'){
    if(!Array.isArray(e.rows)||!e.rows.length||e.rows.some(r=>!Array.isArray(r)))throw new Error(`${label}: rows must be a nonempty array of arrays`);
    slide.addTable(e.rows,{fontFace:font,fontSize:16,color:'082F60',margin:.08,...e.options,...pos});
   }else if(e.type==='chart'){
    if(!Array.isArray(e.series)||!e.series.length)throw new Error(`${label}: series required`);
    for(const ser of e.series)if(!Array.isArray(ser.labels)||!Array.isArray(ser.values)||ser.labels.length!==ser.values.length||ser.values.some(v=>!Number.isFinite(v)))throw new Error(`${label}: invalid labels/values`);
    const chartType=pptx.ChartType[e.chartType||'bar'];if(!chartType)throw new Error(`${label}: unsupported chart type`);
    slide.addChart(chartType,e.series,{showTitle:false,showLegend:false,lang:d.lang||'zh-CN',catAxisLabelFontFace:font,valAxisLabelFontFace:font,dataLabelFormatCode:'0',dataLabelBkgrdColor:'FFFFFF',...e.options,...pos});
   }else throw new Error(`${label}: unsupported element type`);
   count++;
  }
 }
 const payload=await pptx.write({outputType:'nodebuffer',compression:true});
 await fs.mkdir(path.dirname(output),{recursive:true});await fs.writeFile(output,payload,{flag:'wx'});
 console.log(JSON.stringify({output,slides:d.slides.length,elements:count,bytes:payload.length,engine:'PptxGenJS',version:pptx.version}));
}catch(e){console.error('Build failed: '+e.message);process.exitCode=1;}
