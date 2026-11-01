# 장면 경계(BD) 기준: 이어지는 장면 — 앞 장면 끝(BD-0.15) vs 새 장면 0.4초/끝 위치. 제목 높이: 장면 안 여러 시점
import json
from playwright.sync_api import sync_playwright
R='/mnt/user-data/uploads/야구자판기/시스템/work/render_fix.html'
h=open(R,encoding='utf-8').read(); i=h.find('window.EP=');j=h.find(';</script>',i); EP=json.loads(h[i+10:j])
SC=EP['scenes']; BD=EP['bounds']
JS=open('/home/claude/g5/movecheck.py',encoding='utf-8').read().split('JS="""')[1].split('"""')[0]
TJ="""(w)=>{const t=[...document.querySelectorAll('#body .title')].find(x=>x.textContent.replace(/\\s+/g,' ').trim()===w); return t?Math.round(t.getBoundingClientRect().top):null}"""
def snap(p,t): p.evaluate('t=>window.render(t)',t); p.wait_for_timeout(15); return {x[0]:x[1:] for x in p.evaluate(JS)}
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1920,'height':1080})
    p.goto('file://'+R); p.wait_for_timeout(1500)
    for k,s in enumerate(SC):
        a=0 if k==0 else BD[k-1]; e=BD[k] if k<len(BD) else a+3
        if s.get('title'):
            ys=[]
            for f in [0.25,0.5,0.75,0.97]:
                p.evaluate('t=>window.render(t)',a+(e-a)*f); p.wait_for_timeout(10); ys.append(p.evaluate(TJ,' '.join(s['title'].split())))
            if any(y is not None and y!=172 for y in ys) or all(y is None for y in ys): print('TITLE',k,s['type'],s['title'][:18],ys)
        if k and s.get('cont'):
            A=snap(p,a-0.15); B=snap(p,a+min(0.6,(e-a)*0.4))
            mv=[(key[:24],A[key][:4],B[key][:4]) for key in A if key in B and A[key][4]>0.9 and B[key][4]>0.9 and any(abs(A[key][q]-B[key][q])>3 for q in range(4))]
            if mv: print('MOVE',k,s['type'],SC[k-1]['type'],len(mv),mv[:3])
    b.close()
