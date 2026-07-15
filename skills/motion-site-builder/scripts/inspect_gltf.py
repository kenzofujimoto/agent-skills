#!/usr/bin/env python3
import argparse,json,struct
from pathlib import Path
def scene(t):
 if t.is_file(): return t
 xs=list(t.rglob('*.glb'))+list(t.rglob('*.gltf'))
 if not xs: raise FileNotFoundError('No glTF/GLB found')
 return sorted(xs,key=lambda p:(p.name!='scene.gltf',len(p.parts),str(p)))[0]
def load(p):
 if p.suffix.lower()=='.gltf': return json.loads(p.read_text(encoding='utf-8-sig'))
 b=p.read_bytes(); off=12
 if b[:4]!=b'glTF': raise ValueError('Invalid GLB')
 while off+8<=len(b):
  n,t=struct.unpack_from('<II',b,off); off+=8; c=b[off:off+n]; off+=n
  if t==0x4E4F534A: return json.loads(c.decode('utf-8').rstrip('\x00 '))
 raise ValueError('JSON chunk not found')
def ac(d,i):
 a=d.get('accessors',[]); return int(a[i].get('count') or 0) if isinstance(i,int) and 0<=i<len(a) else 0
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('target'); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); p=scene(Path(a.target)); d=load(p); tri=verts=prims=0
 for m in d.get('meshes',[]):
  for q in m.get('primitives',[]):
   prims+=1; attrs=q.get('attributes',{}); v=ac(d,attrs.get('POSITION')); verts+=v; count=ac(d,q.get('indices')) or v; mode=q.get('mode',4); tri+=count//3 if mode==4 else max(0,count-2) if mode in (5,6) else 0
 r={'scene':str(p),'totalBytes':sum(x.stat().st_size for x in p.parent.rglob('*') if x.is_file()),'nodes':len(d.get('nodes',[])),'meshes':len(d.get('meshes',[])),'primitives':prims,'estimatedTriangles':tri,'positionAccessorVertices':verts,'materials':len(d.get('materials',[])),'textures':len(d.get('textures',[])),'images':len(d.get('images',[])),'animations':[{'name':x.get('name'),'channels':len(x.get('channels',[]))} for x in d.get('animations',[])],'skins':len(d.get('skins',[])),'extensionsUsed':d.get('extensionsUsed',[]),'extensionsRequired':d.get('extensionsRequired',[])}; print(json.dumps(r,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
