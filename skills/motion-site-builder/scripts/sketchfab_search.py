#!/usr/bin/env python3
import argparse,json,urllib.parse,urllib.request
from pathlib import Path
API='https://api.sketchfab.com/v3/search'
def get(url):
 req=urllib.request.Request(url,headers={'User-Agent':'motion-site-builder/1.1'}); return json.load(urllib.request.urlopen(req,timeout=30))
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('query'); ap.add_argument('--count',type=int,default=24); ap.add_argument('--animated',action='store_true'); ap.add_argument('--output'); a=ap.parse_args()
 params={'type':'models','q':a.query,'downloadable':'true','count':str(max(1,min(a.count,100)))}
 if a.animated: params['animated']='true'
 url=API+'?'+urllib.parse.urlencode(params); d=get(url); rows=[]
 for x in d.get('results',[]):
  u=x.get('user') if isinstance(x.get('user'),dict) else {}; lic=x.get('license'); lname=(lic.get('label') or lic.get('name') or lic.get('slug')) if isinstance(lic,dict) else lic
  rows.append({'uid':x.get('uid'),'name':x.get('name'),'viewerUrl':x.get('viewerUrl'),'downloadable':x.get('isDownloadable',x.get('downloadable')),'animated':x.get('isAnimated',x.get('animated')),'animationCount':x.get('animationCount'),'faceCount':x.get('faceCount'),'vertexCount':x.get('vertexCount'),'license':lname,'author':{'displayName':u.get('displayName') or u.get('username'),'username':u.get('username'),'profileUrl':u.get('profileUrl')},'tags':[t.get('name') if isinstance(t,dict) else t for t in x.get('tags',[])]})
 out={'query':a.query,'apiUrl':url,'count':len(rows),'results':rows}; text=json.dumps(out,indent=2,ensure_ascii=False)
 if a.output: Path(a.output).write_text(text+'\n',encoding='utf-8'); print(a.output)
 else: print(text)
if __name__=='__main__': main()
