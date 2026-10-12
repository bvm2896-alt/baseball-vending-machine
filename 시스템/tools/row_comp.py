# -*- coding: utf-8 -*-
"""10/11 롱폼⑪ 썸네일: 선수 누끼 여러 명을 머리 크기(모자 꼭대기~턱 = F px)가 같게 한 줄로 세워 한 장 png 로 합친다.
사용: python3 tools/row_comp.py tools/row_1011_long11.json 출력.png
json: {W,H,F,cy, people:[{img, top, chin, cx(원본 얼굴 가운데 x), x(캔버스 얼굴 가운데 x), y?(캔버스 얼굴 가운데 y, 없으면 cy — 트리 배치), z, fade?, bright?}]}
- 얼굴 가운데가 (x, cy) 에 오도록 배치, z 작은 것부터 그린다(가운데 앞). 아래 끝은 fade(px, 기본 140) 만큼 서서히 투명.
- 밝기는 사람마다 bright(기본: 얼굴 밝기 중앙값을 맞춤) — 보정은 밝기·대비만."""
import json, sys, os
import numpy as np
from PIL import Image, ImageEnhance
cfg = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '선수이미지')
W, H, F, CY = cfg['W'], cfg['H'], cfg['F'], cfg['cy']
canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
layers = []
for p in cfg['people']:
    im = Image.open(os.path.join(ROOT, p['img'])).convert('RGBA')
    s = F / (p['chin'] - p['top'])
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    cx, cy = p['cx'] * s, (p['top'] + p['chin']) / 2 * s
    a = np.array(im)
    # 얼굴 밝기 맞춤(얼굴 상자 안 밝기 중앙값 → 목표 150)
    fy0, fy1 = int(p['top'] * s), int(p['chin'] * s); fx0, fx1 = int(cx - F * .3), int(cx + F * .3)
    face = a[max(0, fy0):fy1, max(0, fx0):fx1]; m = face[..., 3] > 128
    L = float(np.median((0.299 * face[..., 0] + 0.587 * face[..., 1] + 0.114 * face[..., 2])[m])) if m.sum() > 50 else 150
    br = p.get('bright') or min(1.25, max(0.85, 150 / max(L, 1)))
    im = ImageEnhance.Brightness(im).enhance(br); im = ImageEnhance.Contrast(im).enhance(1.05)
    a = np.array(im); fade = p.get('fade', 140)
    if fade:
        ramp = np.ones(a.shape[0]); ramp[-fade:] = np.linspace(1, 0, fade); a[..., 3] = (a[..., 3] * ramp[:, None]).astype(np.uint8)
    im = Image.fromarray(a)
    X, Y = round(p['x'] - cx), round((p.get('y') if p.get('y') is not None else CY) - cy)
    layers.append((p.get('z', 0), im, X, Y, p['img'], round(br, 2), round(L)))
for z, im, X, Y, name, br, L in sorted(layers, key=lambda t: t[0]):
    # 뒤 사람에 그림자
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').point(lambda v: int(v * .55)))
    from PIL import ImageFilter
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    canvas.alpha_composite(sh, (X + 10, Y + 8)); canvas.alpha_composite(im, (X, Y))
    print(f'{os.path.basename(name)}: z{z} left {X} top {Y} 밝기 {L}→x{br}')
canvas.save(out); print('ok', out, canvas.size)
