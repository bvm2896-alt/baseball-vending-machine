# 10/7 무대형 썸네일 겹침 검사(시스템 폴더 기준). occ(thumb설정, [(머리꼭대기y, 턱y)…]) → [(이름, 머리+상체 가림%, 머리 가림%)]
# 겹침 검사: 각 선수의 '머리+상체'(머리 꼭대기~턱 아래 머리 1.6개 길이) 영역이 앞 선수에게 가려진 비율
import json,sys
import numpy as np
from PIL import Image
import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','선수이미지')+os.sep
def occ(c, heads):
    W,H=1280,720; L=[]
    for p in c['people']:
        im=Image.open(D+p['img']+'.png').convert('RGBA').resize((p['wpx'],p['h']))
        a=np.zeros((H,W),bool); al=np.array(im)[...,3]>40
        x0,y0=p['left'],p['top']; xs,ys=max(0,x0),max(0,y0); xe,ye=min(W,x0+p['wpx']),min(H,y0+p['h'])
        if xe>xs and ye>ys: a[ys:ye,xs:xe]=al[ys-y0:ye-y0,xs-x0:xe-x0]
        L.append((p,a))
    out=[]
    for i,(p,a) in enumerate(L):
        ht,hb=heads[i]; zone=np.zeros_like(a); zone[max(0,ht):min(720,int(hb+(hb-ht)*1.6)),:]=True
        mine=a&zone; front=np.zeros_like(a)
        for j,(q,b) in enumerate(L):
            if j!=i and (q.get('z',1)>p.get('z',1) or (q.get('z',1)==p.get('z',1) and j>i)): front|=b
        headz=np.zeros_like(a); headz[ht:hb,:]=True
        out.append((p['img'].split('_')[1], round((mine&front).sum()/max(1,mine.sum())*100,1), round((a&headz&front).sum()/max(1,(a&headz).sum())*100,1)))
    return out
