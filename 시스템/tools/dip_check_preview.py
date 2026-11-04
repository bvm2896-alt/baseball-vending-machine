import json,sys
from playwright.sync_api import sync_playwright
H=sys.argv[1]; SEC=4.0
ep=json.load(open('/home/claude/kfa/episodes/2026-11-05_롱폼.json',encoding='utf-8'))
JS="""() => { const out={}; const walk=(el,op)=>{ const cs=getComputedStyle(el); const o=op*parseFloat(cs.opacity||1);
  if(cs.display==='none'||cs.visibility==='hidden') return;
  for(const n of el.childNodes){ if(n.nodeType===3){const t=n.textContent.trim(); if(t){const r=el.getBoundingClientRect(); const key=t+'@'+Math.round(r.left/4)+','+Math.round(r.top/4); out[key]=Math.max(out[key]||0,o);}} else if(n.nodeType===1) walk(n,o);} };
  const b=document.getElementById('body'); if(b) walk(b,1); const g=document.getElementById('ghost'); const go={}; 
  return out; }"""
res=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1920,'height':1080}); p.goto('file://'+H); p.wait_for_timeout(500)
    for k in range(1,len(ep['scenes'])):
        s=ep['scenes'][k]; t0=s['startLine']*SEC
        if s.get('enterAt') is not None: continue
        p.evaluate('t=>window.render(t)',t0-0.05); before=p.evaluate(JS)
        for dt in (0.03,0.08,0.15,0.25,0.4):
            p.evaluate('t=>window.render(t)',t0+dt); now=p.evaluate(JS)
            for txt,o in now.items():
                if before.get(txt,0)>0.95 and o<0.9: res.append((k,s['startLine'],round(dt,2),txt,round(o,2)))
    b.close()
seen=set()
for r in res:
    if (r[0],r[3]) in seen: continue
    seen.add((r[0],r[3])); print(r)
print('total',len(seen))
