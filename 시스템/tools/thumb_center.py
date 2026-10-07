#!/usr/bin/env python3
"""썸네일 누끼를 '얼굴 + 몸 + 몸통' 기준으로 가운데에 두게 잘라 준다(10/8 사용자: "몸이랑 얼굴 고려해서 가운데에 잘 맞추라고 했잖아").
사용: python3 tools/thumb_center.py 입력.png 출력.png [--mask=다른누끼.png] [--keep=0.6]
- 사람 픽셀(알파>128)에서 세 중심을 잰다: 얼굴(위 22% 의 가운데) · 몸 상자(팔·손 포함 bbox 가운데) · 몸통(위 22~60% 높이의 무게중심).
- 기준 = 셋의 평균. 이 x 가 결과 png 의 정가운데가 되도록 좌우를 잘라 내거나(사람 쪽은 자르지 않음) 투명으로 덧댄다.
- 썸네일 템플릿(thumb_issue cutout)은 png 를 가운데 정렬로 그리므로, 결과 png 가운데 = 썸네일 가운데.
- 결과에 세 중심이 썸네일 가운데에서 몇 % 떨어졌는지 출력(±6% 안이면 통과).
"""
import sys
import numpy as np
from PIL import Image

a = [x for x in sys.argv[1:] if not x.startswith('--')]
opt = {k: v for k, v in (x[2:].split('=', 1) for x in sys.argv[1:] if x.startswith('--'))}
im = Image.open(a[0]).convert('RGBA')
al = np.array(Image.open(opt['mask']).convert('RGBA'))[:, :, 3] if 'mask' in opt else np.array(im)[:, :, 3]
m = al > 128
ys, xs = np.nonzero(m)
top, bot = ys.min(), ys.max()
h = bot - top
keep = float(opt.get('keep', '0.6'))          # 썸네일에 보이는 높이 비율(위에서부터) — 몸통 무게중심도 이 안에서만
def band_cx(y0, y1):
    sub = m[top + int(h * y0): top + int(h * y1)]
    c = np.nonzero(sub)[1]
    return c.mean() if len(c) else xs.mean()
face = band_cx(0, .22)
torso = band_cx(.22, keep)
vis = m[top: top + int(h * keep)]
vx = np.nonzero(vis.any(axis=0))[0]
box = (vx.min() + vx.max()) / 2
c = (face + box + torso) / 3
W, H = im.size
half = int(max(c - vx.min(), vx.max() - c) + 10)       # 사람(보이는 부분)을 다 담는 반폭
x0, x1 = int(round(c - half)), int(round(c + half))
out = Image.new('RGBA', (x1 - x0, H), (0, 0, 0, 0))
out.paste(im.crop((max(0, x0), 0, min(W, x1), H)), (max(0, -x0), 0))
out.save(a[1])
w = x1 - x0
pct = lambda v: (v - c) / w * 100
print(f"{a[0]} → {a[1]} {w}x{H} | 가운데에서(+오른쪽): 얼굴 {pct(face):+.1f}% · 몸상자 {pct(box):+.1f}% · 몸통 {pct(torso):+.1f}%")
