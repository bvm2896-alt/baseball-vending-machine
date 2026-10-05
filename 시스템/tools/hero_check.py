#!/usr/bin/env python3
"""hero 썸네일 얼굴 가림 검사: spec.json(hero_fit 입력)으로 각 사람 얼굴 상자가 앞(z 큰) 사람 누끼에 몇 % 가려지는지, 화면 밖으로 몇 % 나가는지 출력."""
import sys, json, os
import numpy as np
from PIL import Image
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '선수이미지')
W, H = 1280, 720
spec = json.load(open(sys.argv[1], encoding='utf-8'))
layers = []
for f in spec:
    im = Image.open(os.path.join(base, f['img'] + '.png')).convert('RGBA')
    x, y, w, h = f['face']; s = f['F'] / h
    left = f['cx'] - (x + w / 2) * s; top = f['cy'] - (y + h / 2) * s
    nw, nh = round(im.width * s), round(im.height * s)
    a = np.array(im.resize((nw, nh), Image.BILINEAR))[:, :, 3] / 255.0
    canvas = np.zeros((H, W))
    x0, y0 = round(left), round(top)
    sx0, sy0 = max(0, -x0), max(0, -y0); dx0, dy0 = max(0, x0), max(0, y0)
    cw, ch = min(nw - sx0, W - dx0), min(nh - sy0, H - dy0)
    if cw > 0 and ch > 0: canvas[dy0:dy0 + ch, dx0:dx0 + cw] = a[sy0:sy0 + ch, sx0:sx0 + cw]
    face = (round(f['cx'] - w * s / 2), round(f['cy'] - h * s / 2), round(w * s), round(h * s))
    nm=f['img'].split('/')[-1].replace('스타일_','').split('_'); layers.append((nm[1] if len(nm)>1 else nm[0], f['z'], canvas, face))
# 머리 상자(모자까지): 얼굴 상자를 위로 0.7F, 옆으로 0.15F 넓힘 — 머리끼리 겹치면 z 와 상관없이 지적
heads=[]
for name, z, _, (fx, fy, fw, fh) in layers:
    heads.append((name, fx - int(fw*.15), fy - int(fh*.7), fx + fw + int(fw*.15), fy + fh))
for i in range(len(heads)):
    for j in range(i+1, len(heads)):
        a, b = heads[i], heads[j]
        ox = min(a[3], b[3]) - max(a[1], b[1]); oy = min(a[4], b[4]) - max(a[2], b[2])
        if ox > 0 and oy > 0: print(f"머리 겹침: {a[0]} ↔ {b[0]} {ox}x{oy}px")
for name, z, _, (fx, fy, fw, fh) in layers:
    front = np.zeros((H, W))
    for n2, z2, c2, _ in layers:
        if z2 > z: front = np.maximum(front, c2)
    X0, Y0, X1, Y1 = max(0, fx), max(0, fy), min(W, fx + fw), min(H, fy + fh)
    area = fw * fh; inside = max(0, X1 - X0) * max(0, Y1 - Y0)
    cov = front[Y0:Y1, X0:X1].sum() if inside else 0
    print(f"{name:6s} z{z} 얼굴 ({fx},{fy},{fw},{fh}) 화면밖 {100 - 100 * inside / area:4.1f}%  앞사람에 가림 {100 * cov / area:4.1f}%")
