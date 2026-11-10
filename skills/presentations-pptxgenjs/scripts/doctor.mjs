import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
try {
  const PptxGenJS=require('pptxgenjs');
  const p=new PptxGenJS();
  const major=Number(process.versions.node.split('.')[0]);
  if(major<18)throw new Error('Node.js 18+ required.');
  console.log(JSON.stringify({ok:true,node:process.version,pptxgenjs:p.version,dependencyEntry:require.resolve('pptxgenjs'),networkRequired:false,nodeBundled:false,rendering:'Optional installed PowerPoint or LibreOffice; fonts must be available locally.'},null,2));
} catch(e) {
  console.error('Dependency check failed: '+e.message+'\nOnline: npm ci --ignore-scripts --no-audit --no-fund in the skill directory. Offline: copy the prepared directory including node_modules.');
  process.exitCode=1;
}
