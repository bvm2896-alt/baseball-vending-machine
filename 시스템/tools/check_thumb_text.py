#!/usr/bin/env python3
"""썸네일 글 줄 겹침 검사 — 1줄(.t1)을 숨긴 렌더와 비교해, 1줄(그림자 포함)이 2줄 글자 픽셀을 바꾸지 않고 2줄 잉크 위로 4px 이상 떨어져 있으면 통과. 사용: python3 check_text.py thumb.html"""
import sys, os, subprocess, numpy as np
from PIL import Image
html = sys.argv[1]; d = os.path.dirname(os.path.abspath(html)); shot = os.path.join(d, 'shot13.js')
no1 = os.path.join(d, '_no1.html'); open(no1, 'w', encoding='utf-8').write(open(html, encoding='utf-8').read().replace('<div class="t t1">', '<div class="t t1" style="visibility:hidden">'))
subprocess.run(['node', shot, html, os.path.join(d, '_full.png')], check=True); subprocess.run(['node', shot, no1, os.path.join(d, '_no1.png')], check=True)
a = np.array(Image.open(os.path.join(d, '_full.png')).convert('RGB')).astype(int); b = np.array(Image.open(os.path.join(d, '_no1.png')).convert('RGB')).astype(int)
diff = np.abs(a - b).sum(2) > 40
g = (b[..., 0] > 200) & (b[..., 1] > 170) & (b[..., 2] < 170); g[:540] = False   # 2줄 노란 글자
top2 = int(np.where(g.any(1))[0].min()); rows = np.where(diff[:top2 + 5].any(1))[0]; gap = top2 - int(rows.max())
changed = int((diff & g).sum())
# 글리프 잘림 검사(10/13): .t2 에 여유 padding 을 더 준 렌더와 잉크 높이가 같아야 함(background-clip:text 는 상자 밖을 안 칠함)
pad = os.path.join(d, '_pad.html'); open(pad, 'w', encoding='utf-8').write(open(no1, encoding='utf-8').read().replace('</style>', '.t2{padding:120px 0 !important;margin-top:-80px}</style>'))
subprocess.run(['node', shot, pad, os.path.join(d, '_pad.png')], check=True)
c = np.array(Image.open(os.path.join(d, '_pad.png')).convert('RGB')).astype(int); gp = (c[..., 0] > 200) & (c[..., 1] > 170) & (c[..., 2] < 170); gp[:500] = False
h0 = np.where(g.any(1))[0]; h1 = np.where(gp.any(1))[0]; clip = (int(h1.max() - h1.min()) - int(h0.max() - h0.min()))
print(f'2줄 글리프 잘림: 잉크 높이 {h0.max()-h0.min()} vs 여유 상자 {h1.max()-h1.min()} → 잘림 {clip}px')
os.remove(pad); os.remove(os.path.join(d, '_pad.png'))
ok = changed == 0 and gap >= 4 and clip <= 0
print(f'줄 겹침: 2줄 잉크 시작 y={top2}, 1줄+그림자 끝 y={rows.max()}, 간격 {gap}px, 2줄 글자 픽셀 변화 {changed}px → {"통과" if ok else "불통과"}')
for f in (no1, os.path.join(d, '_full.png'), os.path.join(d, '_no1.png')): os.remove(f)
sys.exit(0 if ok else 1)
