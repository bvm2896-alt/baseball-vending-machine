# -*- coding: utf-8 -*-
"""썸네일 사람 배치 좌우 균형 검사 (10/11): thumb json 의 people(top/chin/cx/x/y/H) 로 각 누끼의 잉크 상자를 캔버스에 놓고
전체 잉크의 왼쪽·오른쪽 여백, 사람별 얼굴 상자, 얼굴 가림을 출력한다. --fix 면 전체 잉크가 가운데 오도록 x 를 전부 옮겨 저장.
사용: python3 tools/poster_balance.py tools/thumb_1011_long11.json [--fix] [--yfrom=0 --yto=520]"""
import json, sys, os
import numpy as np
from PIL import Image
args = [a for a in sys.argv[1:] if not a.startswith('--')]; opt = {k: v for k, v in (a[2:].split('=', 1) if '=' in a else (a[2:], '1') for a in sys.argv[1:] if a.startswith('--'))}
cfg = json.load(open(args[0], encoding='utf-8')); W, H = 1280, 720
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '선수이미지')
y0, y1 = int(opt.get('yfrom', 0)), int(opt.get('yto', 520))   # 글씨 위 영역만 본다
L, R = 1e9, -1e9; faces = []
for p in cfg['people']:
    im = Image.open(os.path.join(ROOT, p['img'] + '.png')).convert('RGBA'); a = np.array(im)[..., 3]
    s = p['H'] / (p['chin'] - p['top']); cx, cy = p['cx'] * s, (p['top'] + p['chin']) / 2 * s
    X, Y = p['x'] - cx, p['y'] - cy
    ys, xs = np.where(a > 60)
    cxs, cys = xs * s + X, ys * s + Y
    m = (cys >= y0) & (cys <= y1) & (cys >= 0) & (cxs >= 0) & (cxs < W)
    if m.any():
        L = min(L, cxs[m].min()); R = max(R, cxs[m].max())
    fw = p['H'] * .72
    faces.append((p['img'].split('_')[1], p['x'] - fw / 2, p['y'] - p['H'] / 2, p['x'] + fw / 2, p['y'] + p['H'] / 2, p.get('z', 0)))
    print(f"{p['img'].split('/')[-1][:22]:24s} 얼굴 x {p['x']-fw/2:.0f}~{p['x']+fw/2:.0f} y {p['y']-p['H']/2:.0f}~{p['y']+p['H']/2:.0f}  잉크 x {cxs[m].min() if m.any() else 0:.0f}~{cxs[m].max() if m.any() else 0:.0f}")
print(f"전체 잉크 x {L:.0f}~{R:.0f} → 왼쪽 여백 {L:.0f} / 오른쪽 여백 {W-R:.0f} (차이 {abs(L-(W-R)):.0f}px)")
# 얼굴 가림: 앞(z 큰) 사람의 잉크가 뒤 사람 얼굴 상자를 덮는지
for i, (n, fx0, fy0, fx1, fy1, z) in enumerate(faces):
    for p in cfg['people']:
        if p.get('z', 0) <= z or p['img'].split('_')[1] == n: continue
        im = Image.open(os.path.join(ROOT, p['img'] + '.png')).convert('RGBA'); a = np.array(im)[..., 3]
        s = p['H'] / (p['chin'] - p['top']); X, Y = p['x'] - p['cx'] * s, p['y'] - (p['top'] + p['chin']) / 2 * s
        gx0, gy0 = int((fx0 - X) / s), int((fy0 - Y) / s); gx1, gy1 = int((fx1 - X) / s), int((fy1 - Y) / s)
        sub = a[max(0, gy0):max(0, gy1), max(0, gx0):max(0, gx1)]
        if sub.size: cov = (sub > 60).mean()
        else: cov = 0
        if cov > 0.02: print(f"  가림: {p['img'].split('_')[1]} 이(가) {n} 얼굴 {cov*100:.0f}% 덮음")
if opt.get('fix'):
    d = ((W - R) - L) / 2
    for p in cfg['people']: p['x'] = round(p['x'] + d)
    json.dump(cfg, open(args[0], 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(f"x 전부 {d:+.0f} 옮겨 저장")
