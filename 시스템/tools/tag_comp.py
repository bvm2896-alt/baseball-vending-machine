#!/usr/bin/env python3
"""롱폼 썸네일 선수 묶음 합성 (10/10 롱폼⑩ 다시). 사용: python3 tools/tag_comp.py 설정.json 출력.png
people(뒤→앞): {src, top 머리꼭대기y, chin 턱y, cx 얼굴가운데x, head 목표 머리px, x 얼굴 목표x, chinY 턱 목표y, fade, fadeLen, cut:[[x0,y0,x1,y1]]}
- 한 장면처럼: 사람마다 밝기(사람 픽셀 평균 휘도)를 lum 에 맞추고 대비·채도를 같은 값으로 가볍게(10/7 규칙 — 거친 보정 금지).
- 작은 사진을 키우면 언샤프로 살짝 선명하게. 얼굴 상자와 겹침(앞사람이 가리는 비율)을 출력한다."""
import json, sys, numpy as np
from PIL import Image, ImageEnhance, ImageFilter
L = json.load(open(sys.argv[1], encoding='utf-8')); OUT = sys.argv[2]
CW, CH = L.get('W', 1280), L.get('H', 720); LUM = L.get('lum', 135)
canvas = Image.new('RGBA', (CW, CH), (0, 0, 0, 0)); masks = []; faces = []
for p in L['people']:
    im = Image.open(p['src']).convert('RGBA')
    if p.get('cut'):
        a0 = np.array(im)
        for x0, y0, x1, y1 in p['cut']: a0[y0:y1, x0:x1, 3] = 0
        im = Image.fromarray(a0)
    s = p['head'] / (p['chin'] - p['top'])
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    if s > 1.05: im = im.filter(ImageFilter.UnsharpMask(2, 60, 2))
    a = np.array(im).astype(np.float32); al = a[:, :, 3] > 128
    y = (a[:, :, :3] @ [0.299, 0.587, 0.114])[al].mean()
    rgb = Image.fromarray(a[:, :, :3].clip(0, 255).astype(np.uint8))
    rgb = ImageEnhance.Brightness(rgb).enhance(np.clip(LUM / max(1, y), .85, 1.25) * p.get('bright', 1))
    rgb = ImageEnhance.Contrast(rgb).enhance(1.06); rgb = ImageEnhance.Color(rgb).enhance(1.05)
    a[:, :, :3] = np.array(rgb)
    h = a.shape[0]; chin = p['chin'] * s; yy = np.arange(h)[:, None]
    st = chin + p.get('fade', 1.2) * p['head']; e = st + p.get('fadeLen', 1.2) * p['head']
    a[:, :, 3] *= np.clip(1 - (yy - st) / max(1, e - st), 0, 1)
    lay = Image.fromarray(a.clip(0, 255).astype(np.uint8))
    ox = round(p['x'] - p['cx'] * s); oy = round(p['chinY'] - chin)
    sh = Image.new('RGBA', lay.size, (0, 0, 0, 0)); sa = np.array(lay)[:, :, 3].astype(np.float32) * .5
    sh.putalpha(Image.fromarray(sa.astype(np.uint8)).filter(ImageFilter.GaussianBlur(16)))
    canvas.alpha_composite(sh, (ox + 12, oy + 6)); canvas.alpha_composite(lay, (ox, oy))
    m = Image.new('L', (CW, CH), 0); m.paste(lay.getchannel('A'), (ox, oy)); masks.append(np.array(m) > 128)
    faces.append((p['src'].split('/')[-1], int(p['x'] - .42 * p['head']), int(p['chinY'] - p['head']), int(p['x'] + .42 * p['head']), int(p['chinY'])))
canvas.save(OUT); print('saved', OUT)
for i, (n, x0, y0, x1, y1) in enumerate(faces):
    later = np.zeros((CH, CW), bool)
    for m in masks[i + 1:]: later |= m
    box = later[max(0, y0):y1, max(0, x0):x1]; print(f'{n} 얼굴상자 {x0},{y0}-{x1},{y1} 가림 {box.mean()*100:.1f}%')
