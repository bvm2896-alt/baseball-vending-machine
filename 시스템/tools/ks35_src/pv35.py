# 클라우드 미리보기: 노트북 render.html(템플릿+사진·로고 내장)에 새 콘티를 끼워 장면 끝 프레임을 찍는다
import json,sys,os,base64,urllib.parse,re,io
from playwright.sync_api import sync_playwright
R='/mnt/user-data/uploads/야구자판기/시스템/work/render.html'
EPF='/home/claude/ks35/episodes/2026-11-01_롱폼.json'
OUT=sys.argv[1]; LINES=sys.argv[2] if len(sys.argv)>2 else 'all'; SEC=float(os.environ.get('PV_SEC','4'))
FR=[float(x) for x in os.environ.get('PV_FR','0.95').split(',')]
h0=open(R,encoding='utf-8').read()
i=h0.find('window.EP=');j=h0.find(';</script>',i)
old=json.loads(h0[i+10:j])
T=open('/home/claude/ks35/template_long.html',encoding='utf-8').read().replace('__FONT_DIR__','file:///mnt/user-data/uploads/야구자판기/폰트')
h=T.replace('<script>','<script>window.EP={};</script><script>',1)
i=h.find('window.EP=');j=h.find(';</script>',i)
ep=json.load(open(EPF,encoding='utf-8'))
EP=dict(ep); N=len(ep['lines'])
for _k in ('standings','dateLabel'): EP.setdefault(_k, old.get(_k))
EP['logos']=old['logos']; EP['photos']=dict(old['photos']); EP['photoSizes']=dict(old.get('photoSizes',{}))
# 없는 사진은 클라우드 사본에서
need=set()
def walk(o):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in('img','img2') and isinstance(v,str): need.add(v)
            walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(ep['scenes'])
from PIL import Image
for n in need:
    if n in EP['photos'] or not n: continue
    for base in ['/mnt/user-data/uploads/야구자판기/선수이미지/','/mnt/user-data/outputs/po34/선수이미지/','/mnt/user-data/outputs/po34/']:
        for ext in ('.jpg','.png','.webp','.jpeg'):
            p=base+n+ext
            if os.path.exists(p):
                b=open(p,'rb').read(); mt='image/png' if ext=='.png' else 'image/webp' if ext=='.webp' else 'image/jpeg'
                EP['photos'][n]='data:%s;base64,'%mt+base64.b64encode(b).decode()
                im=Image.open(p); EP['photoSizes'][n]=[im.width,im.height]; break
        if n in EP['photos']: break
    if n not in EP['photos']: print('사진 없음',n)
EP['bounds']=[float(x['startLine'])*SEC for x in ep['scenes'][1:]]
EP['subs']=[[k*SEC,(k+1)*SEC,ep['lines'][k]['sub'].split('|')[-1]] for k in range(N)]
EP['segT']=[[round(k*SEC+m*SEC/max(1,len(l['narr'].split(' / '))),3) for m in range(len(l['narr'].split(' / ')))] for k,l in enumerate(ep['lines'])]
EP['total']=N*SEC; EP['_path']=EPF
h2=h[:i+10]+json.dumps(EP,ensure_ascii=False)+h[j:]
FD='file:///mnt/user-data/uploads/야구자판기/폰트/'
h2=re.sub(r"file:///C:/Users/NAME/OneDrive/[^'\")]*?/%ED%8F%B0%ED%8A%B8/",urllib.parse.quote(FD,safe=':/'),h2)
open(OUT+'.html','w',encoding='utf-8').write(h2)
ls=range(N) if LINES=='all' else [int(x) for x in LINES.split(',')]
os.makedirs(OUT,exist_ok=True)
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1920,'height':1080})
    errs=[]; p.on('pageerror',lambda e: errs.append(str(e)))
    p.goto('file://'+OUT+'.html'); p.wait_for_timeout(600)
    for k in ls:
        for f in FR:
            p.evaluate('t=>window.render(t)',k*SEC+f*SEC); p.wait_for_timeout(60)
            p.screenshot(path=f'{OUT}/{k:03d}_{int(f*100):02d}.png')
    b.close()
print('ok',len(list(ls)),'errs',errs[:5])
