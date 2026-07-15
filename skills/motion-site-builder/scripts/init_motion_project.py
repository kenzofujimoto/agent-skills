#!/usr/bin/env python3
import argparse,json
from pathlib import Path
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--project',required=True); ap.add_argument('--stack',default='nextjs'); ap.add_argument('--output',default='.'); a=ap.parse_args()
 skill=Path(__file__).resolve().parents[1]; out=Path(a.output).resolve(); out.mkdir(parents=True,exist_ok=True)
 d=json.loads((skill/'templates/motion-plan.example.json').read_text(encoding='utf-8')); d['project']=a.project; d['stack']=a.stack
 dest=out/'motion-plan.json'
 if dest.exists(): raise SystemExit(f'Refusing to overwrite {dest}')
 dest.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 docs=out/'docs'; docs.mkdir(exist_ok=True); (docs/'motion-rationale.md').write_text(f'# Motion rationale — {a.project}\n',encoding='utf-8')
 print(dest)
if __name__=='__main__': main()
