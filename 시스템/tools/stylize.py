#!/usr/bin/env python3
"""썸네일용 누끼 '포스터 보정' (2026-10-03 밤, 사용자 레퍼런스 4장 — 출처 다른 사진을 한 톤으로):
   회화풍 뭉개기(bilateral) → 국소 명암(clarity, 큰 반경 언샤프) → 윤곽 선명(작은 반경 언샤프) → 채도·대비 ↑ → 살짝 포스터화. 알파는 그대로.
사용: python3 tools/stylize.py in.png out.png [--strength 1.0]"""
import sys, numpy as np, cv2
from PIL import Image, ImageEnhance, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
k = float(sys.argv[sys.argv.index('--strength') + 1]) if '--strength' in sys.argv else 1.0
clean = '--clean' in sys.argv   # 10/3 사용자 '보정이 이상하다' → 포스터화 없이 선명·명암·채도만(레퍼런스 톤)
im = Image.open(src).convert('RGBA'); a = im.split()[3]; rgb = np.array(im.convert('RGB'))
# 1) 회화풍: bilateral 2회(작은 디테일 뭉개고 윤곽은 유지)
x = rgb
for _ in range(1 if clean else 2): x = cv2.bilateralFilter(x, d=9, sigmaColor=int((14 if clean else 28) * k), sigmaSpace=7)
# 2) clarity: 큰 반경 언샤프(국소 명암) + 3) 윤곽 선명
p = Image.fromarray(x)
p = p.filter(ImageFilter.UnsharpMask(radius=int(40 * k) or 1, percent=int(60 * k), threshold=0))
p = p.filter(ImageFilter.UnsharpMask(radius=2, percent=int(120 * k), threshold=2))
# 4) 채도·대비
p = ImageEnhance.Color(p).enhance(1 + .35 * k); p = ImageEnhance.Contrast(p).enhance(1 + .22 * k)
# 5) 살짝 포스터화(톤 수 줄임) — 그림 느낌
y = np.array(p).astype(np.float32)
if not clean:
    levels = 40; q = np.round(y / 255 * levels) / levels * 255; y = 0.75 * q + 0.25 * y
y = y.clip(0, 255).astype(np.uint8)
out = Image.fromarray(y).convert('RGBA'); out.putalpha(a); out.save(dst); print('ok', dst, out.size)
