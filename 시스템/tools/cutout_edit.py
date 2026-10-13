#!/usr/bin/env python3
"""누끼 후처리 — 자동 누끼 결과를 눈으로 보고 '어디를 뺄지' 직접 지시해서 고친다(10/13 사용자 지적).
사용: python3 tools/cutout_edit.py 누끼.png 결과.png 지시 [지시...]
지시(좌표는 누끼 png 기준 px):
  erase:x0,y0,x1,y1              상자 안 전부 투명(지나가는 심판·동료 등)
  key:x0,y0,x1,y1:R,G,B:tol      상자 안에서 (R,G,B)와 가까운 색만 투명(팔 사이 배경 등). tol 은 채널 차이 합 기준(기본 90)
  keyauto:x0,y0,x1,y1[:tol]      상자 안에서 '상자 테두리 투명 픽셀 바로 옆 색' 의 중앙값을 배경색으로 잡아 key
  blue:x0,y0,x1,y1               상자 안 파란 계열(b > r+30, b>110)만 투명
  poly:x,y;x,y;...               다각형 안 전부 투명(경계가 비스듬할 때 — 격자 jpg 보고 점 찍기)
  grid                           원본 위에 100px 격자+좌표 그린 검사용 jpg 를 결과.png 옆에 _grid.jpg 로 저장"""
import sys, numpy as np
from PIL import Image, ImageDraw
src, dst, ops = sys.argv[1], sys.argv[2], sys.argv[3:]
im = Image.open(src).convert('RGBA'); a = np.array(im); rgb = a[..., :3].astype(int); al = a[..., 3]
def box(s):
    x0, y0, x1, y1 = [int(v) for v in s.split(',')]; return slice(y0, y1), slice(x0, x1)
for op in ops:
    kind, *rest = op.split(':')
    if kind == 'grid':
        g = im.copy(); d = ImageDraw.Draw(g)
        for x in range(0, g.width, 100): d.line([(x, 0), (x, g.height)], fill=(0, 255, 0, 255)); d.text((x + 2, 2), str(x), fill=(0, 0, 0, 255))
        for y in range(0, g.height, 100): d.line([(0, y), (g.width, y)], fill=(0, 255, 0, 255)); d.text((2, y + 2), str(y), fill=(0, 0, 0, 255))
        bg = Image.new('RGBA', g.size, (255, 0, 255, 255)); bg.alpha_composite(g); bg.convert('RGB').save(dst.rsplit('.', 1)[0] + '_grid.jpg', quality=80); continue
    if kind == 'poly':   # poly:x,y;x,y;... 다각형 안 전부 투명
        pts = [tuple(int(v) for v in p.split(',')) for p in rest[0].split(';')]
        pm = Image.new('L', im.size, 0); ImageDraw.Draw(pm).polygon(pts, fill=255); pm = np.array(pm) > 0
        al[pm] = 0; print('poly', len(pts), '점', int(pm.sum()), 'px'); continue
    ys, xs = box(rest[0]); sub = rgb[ys, xs]; sa = al[ys, xs]
    if kind == 'erase': sa[:] = 0; print('erase', rest[0], int((al[ys, xs] == 0).sum()), 'px')
    elif kind == 'blue':
        m = (sub[..., 2] > sub[..., 0] + 30) & (sub[..., 2] > 110); sa[m] = 0; print('blue', rest[0], int(m.sum()), 'px')
    elif kind in ('key', 'keyauto'):
        if kind == 'key': col = np.array([int(v) for v in rest[1].split(',')]); tol = int(rest[2]) if len(rest) > 2 else 90
        else:
            tol = int(rest[1]) if len(rest) > 1 else 90
            # 상자 안 투명 픽셀(이미 배경으로 뺀 곳)의 원본색 중앙값 — 없으면 상자 테두리 불투명 픽셀 중앙값
            t = sa < 128
            col = np.median(sub[t], axis=0) if t.sum() > 50 else np.median(np.concatenate([sub[0], sub[-1], sub[:, 0], sub[:, -1]]), axis=0)
            print('keyauto 배경색', col.round().tolist())
        d = np.abs(sub - col).sum(2); m = (d < tol) & (sa > 0)
        # 색으로 잡힌 픽셀 중 상자 테두리(또는 이미 투명한 곳)와 이어진 덩어리만 뺀다 — 인물 안쪽의 우연히 비슷한 색은 안 건드림
        try:
            import cv2
            seed = m.astype(np.uint8); nb, lab = cv2.connectedComponents(seed, connectivity=4)
            touch = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) | set(np.unique(lab[(sa < 128)]))
            m = np.isin(lab, [i for i in range(1, nb) if i in touch])
        except Exception as e: print('cv2 없음', e)
        sa[m] = 0; print(kind, rest[0], int(m.sum()), 'px')
    al[ys, xs] = sa
a[..., 3] = al
Image.fromarray(a).save(dst); print('ok', dst)
