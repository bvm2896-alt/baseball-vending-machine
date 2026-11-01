# 이어지는 장면(cont) 앞 장면 끝 ↔ 이 장면 처음: 같은 사진·같은 글 요소가 움직이거나 크기 바뀌면 보고
import json,sys,subprocess,os
from playwright.sync_api import sync_playwright
subprocess.run(['python3','pv35.py','/home/claude/g5/pv/mv','0'],capture_output=True)
ep=json.load(open('episodes/2026-11-01_롱폼2.json'))
SC=ep['scenes']; SEC=4.0
JS="""() => { const out=[]; const seen={};
 document.querySelectorAll('img, div, span, b, i').forEach(el=>{
  const r=el.getBoundingClientRect(); if(r.width<4||r.height<4) return;
  const cs=getComputedStyle(el); if(cs.visibility==='hidden') return;
  let key=null;
  if(el.tagName==='IMG') key='img:'+(el.getAttribute('src')||'').slice(-40);
  else if(el.children.length===0 && el.innerText && el.innerText.trim()) key='t:'+el.innerText.trim();
  if(!key) return; seen[key]=(seen[key]||0)+1; key+='#'+seen[key];
  out.push([key,Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height),+cs.opacity]); });
 return out; }"""
bad=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1920,'height':1080})
    p.goto('file:///home/claude/g5/pv/mv.html'); p.wait_for_timeout(800)
    for k,s in enumerate(SC):
        if k==0 or not s.get('cont'): continue
        sl=s['startLine']
        p.evaluate('t=>window.render(t)',(sl-1)*SEC+0.97*SEC); p.wait_for_timeout(40); A={x[0]:x[1:] for x in p.evaluate(JS)}
        p.evaluate('t=>window.render(t)',sl*SEC+0.03*SEC); p.wait_for_timeout(40); B={x[0]:x[1:] for x in p.evaluate(JS)}
        mv=[]
        for key in A:
            if key in B and key.split('#')[0] not in ('t:',):
                a,bb=A[key],B[key]
                if a[4]<0.5 or bb[4]<0.5: continue
                if abs(a[0]-bb[0])>3 or abs(a[1]-bb[1])>3 or abs(a[2]-bb[2])>3 or abs(a[3]-bb[3])>3: mv.append((key[:40],a[:4],bb[:4]))
        if mv: bad.append((k,s.get('type'),mv[:4],len(mv)))
    b.close()
for x in bad: print(x)
print('cont 장면 이동 있음:',len(bad))
