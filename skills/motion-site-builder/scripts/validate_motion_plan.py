#!/usr/bin/env python3
import json,sys
from pathlib import Path
MODES={'full-bleed-cinematic','framed-media-stage','transparent-layered-object','layered-2.5d','dom-motion','interactive-vector','webgl-scene','video-scrub'}
BGS={'exact-match','stage','ambient-extension','transparent','full-bleed'}
def main():
 if len(sys.argv)!=2: print('Usage: validate_motion_plan.py motion-plan.json',file=sys.stderr); return 2
 try: d=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
 except Exception as e: print(f'ERROR: {e}',file=sys.stderr); return 1
 ss=d.get('sections'); errors=[]; ids=set()
 if not isinstance(ss,list) or not ss: errors.append('sections must be non-empty array'); ss=[]
 for i,s in enumerate(ss):
  p=f'sections[{i}]'; sid=s.get('id')
  if not isinstance(sid,str) or not sid: errors.append(f'{p}.id invalid')
  elif sid in ids: errors.append(f'duplicate id {sid}')
  else: ids.add(sid)
  if s.get('renderMode') not in MODES: errors.append(f'{p}.renderMode invalid')
  safe=s.get('safeArea')
  if safe is not None and (not isinstance(safe,(int,float)) or not 0<=safe<.5): errors.append(f'{p}.safeArea invalid')
  a=s.get('initialScale',1); b=s.get('maxScale',a)
  if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or b<a: errors.append(f'{p}.scale invalid')
  bg=s.get('backgroundStrategy')
  if bg is not None and bg not in BGS: errors.append(f'{p}.backgroundStrategy invalid')
 for e in errors: print('ERROR:',e,file=sys.stderr)
 if errors: return 1
 print(f'OK: {len(ss)} section(s) validated.'); return 0
if __name__=='__main__': raise SystemExit(main())
