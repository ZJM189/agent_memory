"""Read-only PPTX structure inspection using Python's standard library."""
import sys,zipfile,json,re,posixpath
from pathlib import Path
from xml.etree import ElementTree as ET
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
def inspect(file):
 with zipfile.ZipFile(file) as z:
  if z.testzip(): raise ValueError('Corrupt ZIP member')
  names=z.namelist(); files=set(names)
  for name in names:
   if name.endswith(('.xml','.rels')):ET.fromstring(z.read(name))
  missing=[]
  for name in names:
   if not name.endswith('.rels'):continue
   base=posixpath.dirname(posixpath.dirname(name))
   for rel in ET.fromstring(z.read(name)):
    if rel.get('TargetMode')=='External':continue
    target=rel.get('Target','')
    resolved=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(base,target))
    if resolved not in files:missing.append({'part':name,'target':resolved})
  slides=[]
  for name in sorted((n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)),key=lambda s:int(re.search(r'(\d+)\.xml',s).group(1))):
   root=ET.fromstring(z.read(name))
   slides.append({'part':name,'text_boxes':len([s for s in root.findall('.//p:sp',NS) if s.find('p:txBody',NS) is not None]),'pictures':len(root.findall('.//p:pic',NS)),'tables':len(root.findall('.//a:tbl',NS)),'charts':len(root.findall('.//c:chart',NS)),'texts':[t.text or '' for t in root.findall('.//a:t',NS)]})
  charts=[]
  for name in names:
   if re.fullmatch(r'ppt/charts/chart\d+\.xml',name):
    root=ET.fromstring(z.read(name));charts.append({'part':name,'series':[{'name':[v.text for v in s.findall('c:tx//c:v',NS)],'categories':[v.text for v in s.findall('c:cat//c:pt/c:v',NS)],'values':[v.text for v in s.findall('c:val//c:pt/c:v',NS)]} for s in root.findall('.//c:ser',NS)]})
  return dict(ok=not missing,slides=slides,charts=charts,embedded_workbooks=[n for n in names if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')],missing_relationships=missing,claim='Structure and content inventory only; no rendering, glyph fit or visual fidelity check.')
if __name__=='__main__':
 try:
  report=inspect(Path(sys.argv[1]));print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(0 if report['ok'] else 1)
 except Exception as e:print(json.dumps({'ok':False,'error':str(e)},ensure_ascii=False));sys.exit(1)
