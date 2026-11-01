import json
from playwright.sync_api import sync_playwright
R='/mnt/user-data/uploads/야구자판기/시스템/work/render_fix.html'
h=open(R,encoding='utf-8').read(); i=h.find('window.EP=');j=h.find(';</script>',i); EP=json.loads(h[i+10:j])
SC=EP['scenes']; BD=EP['bounds']
JS="""()=>{const G=document.getElementById('ghost'); if(!G||!G.innerHTML||+G.style.opacity<0.05) return null; const t=G.querySelector('.title'); return t?Math.round(t.getBoundingClientRect().top):'nt'}"""
bad=[]
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1920,'height':1080})
    p.goto('file://'+R); p.wait_for_timeout(1500)
    for k in range(1,len(SC)):
        if not SC[k-1].get('title'): continue
        ys=[]
        for d in [0.02,0.06,0.12]:
            p.evaluate('t=>window.render(t)',BD[k-1]+d); p.wait_for_timeout(10); ys.append(p.evaluate(JS))
        if any(y not in (None,172,'nt') for y in ys): bad.append((k,ys))
    b.close()
print('ghost title off:',bad)
