#!/usr/bin/env python3
import argparse,json,shutil,subprocess
from pathlib import Path
def img(p):
 from PIL import Image
 with Image.open(p) as im: return {'type':'image','format':im.format,'width':im.width,'height':im.height,'mode':im.mode,'bytes':p.stat().st_size}
def vid(p):
 if not shutil.which('ffprobe'): raise RuntimeError('ffprobe is required')
 raw=subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True,encoding='utf-8'); d=json.loads(raw)
 v=next((x for x in d.get('streams',[]) if x.get('codec_type')=='video'),{}); a=[x for x in d.get('streams',[]) if x.get('codec_type')=='audio']
 return {'type':'video','codec':v.get('codec_name'),'width':v.get('width'),'height':v.get('height'),'pixelFormat':v.get('pix_fmt'),'duration':d.get('format',{}).get('duration'),'bytes':p.stat().st_size,'audioStreams':len(a)}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('paths',nargs='+'); ap.add_argument('--json',action='store_true'); a=ap.parse_args(); out=[]
 for x in a.paths:
  p=Path(x)
  try:
   if not p.exists(): raise FileNotFoundError('missing')
   info=img(p) if p.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.avif'} else vid(p) if p.suffix.lower() in {'.mp4','.mov','.webm','.mkv'} else {'type':'unknown','bytes':p.stat().st_size}
   info['path']=str(p); out.append(info)
  except Exception as e: out.append({'path':str(p),'error':str(e)})
 print(json.dumps(out,indent=2 if a.json else None,ensure_ascii=False)); return 1 if any('error' in x for x in out) else 0
if __name__=='__main__': raise SystemExit(main())
