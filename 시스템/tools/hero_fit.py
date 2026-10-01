#!/usr/bin/env python3
"""썸네일 hero 배치 계산: 사람마다 원하는 얼굴 가운데(cx,cy)·얼굴 높이(F)와 누끼 안의 얼굴 상자로 left/top/h/wpx/head 를 낸다.
사용: python3 tools/hero_fit.py spec.json → people JSON. spec: [{"img":"누끼/…","face":[x,y,w,h],"cx":640,"cy":285,"F":185,"z":5}, …]"""
import sys, json, os
from PIL import Image
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '선수이미지')
out = []
for f in json.load(open(sys.argv[1], encoding='utf-8')):
    W, H = Image.open(os.path.join(base, f['img'] + '.png')).size
    x, y, w, h = f['face']; s = f['F'] / h
    left = round(f['cx'] - (x + w / 2) * s); top = round(f['cy'] - (y + h / 2) * s)
    hw = f.get('headW', 1.15) * f['F']; hy = f.get('headUp', 1.6) * f['F']
    head = [round(f['cx'] - hw), round(f['cy'] - hy), round(f['cx'] + hw), round(f['cy'] + f['F'] * .62)]
    o = {k: v for k, v in f.items() if k not in ('face', 'cx', 'cy', 'F', 'headW', 'headUp')}
    o.update({'left': left, 'top': top, 'h': round(H * s), 'wpx': round(W * s)})
    if f.get('head', True): o['head'] = head
    else: o.pop('head', None)
    out.append(o)
print(json.dumps(out, ensure_ascii=False))
