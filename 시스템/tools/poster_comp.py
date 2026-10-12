import json, sys, numpy as np, cv2
from PIL import Image
D='/tmp/claude-0/-home-claude/34137b2d-2843-5a52-8053-6f4466ba2f45/scratchpad/pos/'
G=json.load(open(D+'geo.json',encoding='utf-8'))
L=json.load(open(sys.argv[1],encoding='utf-8')); OUT=sys.argv[2]
CW,CH=1280,720
def lum_of(arr,box):
    x0,y0,x1,y1=[int(v) for v in box]; r=arr[max(0,y0):y1,max(0,x0):x1]; a=r[:,:,3]>200
    return float(r[:,:,:3][a].mean()) if a.sum()>50 else None
layers=[]
for p in L['people']:   # back → front order
    k=p['k']; top,chin,cx=G[k]; head=p['head']; s=head/(chin-top)
    im=Image.open(D+f'k/k_{k}.png').convert('RGBA')
    if p.get('flip'): im=im.transpose(Image.FLIP_LEFT_RIGHT); cx=im.width-cx
    W,H=im.size; im=im.resize((max(1,round(W*s)),max(1,round(H*s))),Image.LANCZOS)
    a=np.array(im).astype(np.float32); h,w=a.shape[:2]
    c=chin*s
    # bottom fade (into mist)
    yy=np.arange(h)[:,None]
    if p.get('edge'):   # 10/8: 뒷줄·가운데 줄은 몸을 중간에서 흐리지 않는다(흐리면 '몸이 지워진' 것처럼 보임) — 사진이 잘린 아래 끝만 짧게
        rows=np.where(a[:,:,3].max(1)>20)[0]; bot=rows.max() if len(rows) else h
        e=bot+1; st=e-p['edge']*head
    else:
        st=c+p.get('f0',1.1)*head; e=c+p.get('f1',2.6)*head
    a[:,:,3]*=np.clip(1-(yy-st)/max(1,e-st),0,1)
    # 사진 왼쪽·오른쪽 끝에서 잘린 몸은 그 끝만 짧게 흐림(곧은 세로선 안 보이게)
    sw=0.25*head; xx=np.arange(w)[None,:]
    if a[:, :3, 3].max()>20: a[:,:,3]*=np.clip(xx/sw,0,1)
    if a[:, -3:, 3].max()>20: a[:,:,3]*=np.clip((w-1-xx)/sw,0,1)
    if p.get('side'):
        xx=np.arange(w)[None,:]; a[:,:,3]*=np.clip(np.minimum(xx,w-1-xx)/(p['side']*head),0,1)
    # light correction: face luminance toward target (0.9~1.12), tiny contrast
    fl=lum_of(a,((cx*s-head*.28),top*s+head*.3,(cx*s+head*.28),c))
    tgt=p.get('lum',L.get('lum',138))
    if fl: g=float(np.clip(tgt/fl,0.9,1.12)); a[:,:,:3]=np.clip(a[:,:,:3]*g,0,255)
    m=a[:,:,:3].mean(); a[:,:,:3]=np.clip((a[:,:,:3]-m)*1.04+m,0,255)
    # depth: back rows darker + toward haze colour
    dk=p.get('dark',0.0); hz=np.array(L.get('haze',[120,30,40]),np.float32)
    a[:,:,:3]=a[:,:,:3]*(1-dk)+hz*dk*0.6
    ox=round(p['x']-cx*s); oy=round(p['chin']-c)
    layers.append(dict(k=k,a=a,ox=ox,oy=oy,top=oy+top*s,chin=p['chin'],head=head,x=p['x']))
canvas=np.zeros((CH,CW,4),np.float32); masks=[]
for i,Ly in enumerate(layers):
    a,ox,oy=Ly['a'],Ly['ox'],Ly['oy']; h,w=a.shape[:2]
    x0,y0,x1,y1=max(0,ox),max(0,oy),min(CW,ox+w),min(CH,oy+h)
    m=np.zeros((CH,CW),bool)
    if x1<=x0 or y1<=y0: masks.append(m); continue
    sub=a[y0-oy:y1-oy,x0-ox:x1-ox]; al=sub[:,:,3]/255
    # contact shadow on what is behind (soft, offset down-right)
    if i>0:
        sh=np.zeros((CH,CW),np.float32); sh[y0:y1,x0:x1]=al
        sh=cv2.GaussianBlur(sh,(0,0),Ly['head']*0.12); sh=np.roll(np.roll(sh,int(Ly['head']*.06),0),int(Ly['head']*.05),1)
        canvas[:,:,:3]*=(1-0.45*sh[:,:,None])
    canvas[y0:y1,x0:x1,:3]=canvas[y0:y1,x0:x1,:3]*(1-al[:,:,None])+sub[:,:,:3]*al[:,:,None]
    canvas[y0:y1,x0:x1,3]=canvas[y0:y1,x0:x1,3]*(1-al)+al*255
    m[y0:y1,x0:x1]=sub[:,:,3]>110; masks.append(m)
Image.fromarray(canvas.clip(0,255).astype(np.uint8)).save(OUT)
rep=[]
for i,Ly in enumerate(layers):
    front=np.zeros((CH,CW),bool)
    for j in range(i+1,len(layers)): front|=masks[j]
    t,c,hd=int(max(0,Ly['top'])),int(Ly['chin']),Ly['head']
    hm=masks[i].copy(); hm[:t]=False; hm[c:]=False
    um=masks[i].copy(); um[:t]=False; um[int(min(CH,c+0.8*hd)):]=False
    rep.append((Ly['k'],round((hm&front).sum()/max(1,hm.sum())*100,1),round((um&front).sum()/max(1,um.sum())*100,1),int(Ly['top']),c))
for r in rep: print('%s 머리가림 %.1f%% 상체가림 %.1f%% top %d chin %d'%r)
# 10/8: 사진이 잘린 아래 끝(또는 좌우 끝)이 앞사람에게 가려지지 않고 보이는지 — 보이면 '몸이 사라진' 것처럼 보인다
TXT_TOP=int(L.get('textTop',455))
for i,Ly in enumerate(layers):
    a,ox,oy=Ly['a'],Ly['ox'],Ly['oy']; h,w=a.shape[:2]
    rows=np.where(a[:,:,3].max(1)>20)[0]
    if not len(rows): continue
    bot=oy+rows.max()
    front=np.zeros((CH,CW),bool)
    for j in range(i+1,len(layers)): front|=masks[j]
    # 아래 끝 띠: 그 사람 아래 끝 0.6머리 구간에서 알파가 있는 열
    y0=max(0,int(bot-0.6*Ly['head'])); y1=min(CH,int(bot)+1)
    if y0>=min(y1,TXT_TOP): print('%s 아래 끝 y%d (글씨 아래라 안 보임)'%(Ly['k'],bot)); continue
    band=masks[i][y0:min(y1,TXT_TOP)] | ((np.zeros_like(masks[i][y0:min(y1,TXT_TOP)]))); cols=np.where(band.any(0))[0]
    vis=[x for x in cols if not front[y0:min(y1,TXT_TOP),x].any()]
    print('%s 아래 끝 y%d · 보이는 끝 %d/%d열'%(Ly['k'],bot,len(vis),len(cols)))
