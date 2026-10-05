#!/usr/bin/env python3
"""썸네일 누끼 '거친 포스터' 보정 (10/3 사용자 레퍼런스 '골글 내놔라'형 — "뽀샤시 말고 이렇게"):
   피부 뭉개기 없음 → 하이패스 선명(질감·주름 살림) + 국소 명암(clarity) 강하게 → 채도 ↓ + 따뜻한 톤 → 대비 ↑ + 그림자 깊게. 알파 그대로.
사용: python3 tools/stylize_gritty.py in.png out.png [--strength 1.0]"""
import sys, numpy as np, cv2
from PIL import Image, ImageEnhance, ImageFilter
src, dst = sys.argv[1], sys.argv[2]
k = float(sys.argv[sys.argv.index('--strength') + 1]) if '--strength' in sys.argv else 1.0
im = Image.open(src).convert('RGBA'); a = im.split()[3]; rgb = np.array(im.convert('RGB')).astype(np.float32)
# 1) 하이패스 디테일(질감) 강조: 원본 - 블러 를 두 반경으로 더함
def hp(x, r, amt):
    b = cv2.GaussianBlur(x, (0, 0), r); return x + (x - b) * amt
y = hp(rgb, 2.0, 0.9 * k)      # 잔질감(수염·땀구멍)
y = hp(y, 12.0, 0.45 * k)      # 중간 구조(광대·그늘)
y = hp(y, 45.0, 0.35 * k)      # 큰 명암(clarity)
y = y.clip(0, 255).astype(np.uint8)
p = Image.fromarray(y)
# 2) 채도 내리고 따뜻한 톤(약간 황갈색 섞기)
p = ImageEnhance.Color(p).enhance(1 - .22 * k)
arr = np.array(p).astype(np.float32)
warm = np.array([1.06, 1.0, 0.90], dtype=np.float32); arr = (arr * warm).clip(0, 255)
# 3) 대비 ↑ + 그림자 깊게(S자 커브)
t = arr / 255.0; t = np.where(t < .5, (2 * t) ** (1 + .35 * k) / 2, 1 - (2 * (1 - t)) ** (1 + .25 * k) / 2); arr = (t * 255).clip(0, 255)
out = Image.fromarray(arr.astype(np.uint8)).convert('RGBA'); out.putalpha(a); out.save(dst); print('ok', dst, out.size)
