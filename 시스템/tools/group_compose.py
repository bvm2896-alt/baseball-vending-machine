#!/usr/bin/env python3
"""여러 명 누끼를 세로 컷 썸네일용 한 장(투명 png, 기본 1080x1475)으로 합친다. 10/21 골든글러브 컷1(외야 4명)·컷3(오스틴+디아즈)·컷6(강백호+최형우).
tools/group_cutout.py 와 같은 일인데, 머리 크기를 '헬멧 폭(px)'으로 맞추고 앞사람 뒤에 옅은 그림자를 깐다.
사용: python3 tools/group_compose.py 배치.json
배치.json = {"out": "출력.png", "size": [1080, 1475], "people": [
   {"name": "구자욱", "src": "누끼 png 경로", "head": [헬멧왼쪽x, 헬멧오른쪽x, 머리중심x, 머리중심y],   ← 원본 누끼 기준 px
    "hw": 215, "x": 540, "y": 300, "z": 0}, ...]}       ← hw = 놓일 헬멧 폭, (x,y) = 놓일 머리 중심, z 작은 사람부터 그림
썸네일 콘티: "thumb": {"img": "누끼/그룹_…", "cutout": true, "cutoutCrop": 0.8, …} — 1475 중 위 1180(=0.8)이 보이고, 제목이 그 아래 330px 를 덮는다.
그래서 얼굴은 y 800 위에. 배율(scale)이 1.25 를 넘으면 흐려지니 출력 로그의 scale 을 본다.
겹침 규칙(스킬 yagu-poster-thumbnail 4-2): 얼굴 가림 0, 안쪽으로 뻗은 팔은 뒷사람 것이 앞사람 몸 뒤로, 사진 틀에 잘린 직선 끝은 앞사람 뒤·제목 뒤·캔버스 밖으로."""
import json, sys
from PIL import Image, ImageFilter
S = json.load(open(sys.argv[1], encoding='utf-8'))
W, H = S.get('size', [1080, 1475])
can = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for p in sorted(S['people'], key=lambda p: p['z']):
    im = Image.open(p['src']).convert('RGBA')
    hx0, hx1, cx, cy = p['head']
    s = p['hw'] / (hx1 - hx0)
    im2 = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    ox, oy = round(p['x'] - cx * s), round(p['y'] - cy * s)
    if S.get('shadow', True) and p['z'] > 0:   # 앞사람 가장자리 뒤 옅은 그림자(4-2 E16)
        a = im2.split()[-1].filter(ImageFilter.GaussianBlur(8))
        sh = Image.new('RGBA', im2.size, (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * .3)))
        t2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); t2.paste(sh, (ox, oy + 6), sh); can = Image.alpha_composite(can, t2)
    tmp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); tmp.paste(im2, (ox, oy), im2)
    can = Image.alpha_composite(can, tmp)
    print(p['name'], 'scale', round(s, 3), '(1.25 넘으면 흐림)', 'pos', ox, oy)
can.save(S['out']); print('saved', S['out'])
