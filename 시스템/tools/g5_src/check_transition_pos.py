import json
from playwright.sync_api import sync_playwright
R='/mnt/user-data/uploads/야구자판기/시스템/work/render_fix.html'
h=open(R,encoding='utf-8').read(); i=h.find('window.EP=');j=h.find(';</script>',i); EP=json.loads(h[i+10:j])
SC=EP['scenes']; BD=EP['bounds']
J="""(sel)=>[...document.querySelectorAll(sel+' img, '+sel+' .title')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width)]}).filter(x=>x[2]>20)"""
bad=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1920,'height':1080})
    p.goto('file://'+R); p.wait_for_timeout(1500)
    for k in range(1,len(SC)):
        p.evaluate('t=>window.render(t)',BD[k-1]-0.08); p.wait_for_timeout(10); A=p.evaluate(J,'#body')
        p.evaluate('t=>window.render(t)',BD[k-1]+0.05); p.wait_for_timeout(10); B=p.evaluate(J,'#ghost')
        if not B: continue
        if len(A)!=len(B) or any(abs(a[q]-c[q])>3 for a,c in zip(A,B) for q in range(3)): bad.append((k,A[:2],B[:2]))
    b.close()
print(len(bad)); [print(x) for x in bad[:12]]
