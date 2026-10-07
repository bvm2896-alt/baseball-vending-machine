#!/usr/bin/env python3
"""누끼 여러 장을 한 장(투명 png)으로 모아 세로 썸네일 cutout 으로 쓴다(10/8 컷6: 롱폼 썸네일 선수 4명).
사용: python3 tools/group_cutout.py 배치.json 출력.png
배치.json = {"W":1300,"H":1000,"people":[{"img":"누끼/…","top":모자꼭대기y,"chin":턱y,"fx":얼굴가운데x,"head":머리px,"X":얼굴x,"Y":꼭대기y,"z":1}, …]}
(top/chin/fx 는 원본 누끼 기준 — tools/stage_1007_mvp.json 과 같은 값). 뒤(z 작은 것)부터 그린다."""
import sys, json, os
from PIL import Image
L = json.load(open(sys.argv[1], encoding='utf-8'))
base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '선수이미지')
cv = Image.new('RGBA', (L['W'], L['H']), (0, 0, 0, 0))
for p in sorted(L['people'], key=lambda p: p.get('z', 1)):
    im = Image.open(os.path.join(base, p['img'] + '.png')).convert('RGBA')
    k = p['head'] / (p['chin'] - p['top'])
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x, y = round(p['X'] - p['fx'] * k), round(p['Y'] - p['top'] * k)
    fd = p.get('fade', L.get('fade', 0))   # 사람 아래 끝을 fd px 동안 서서히 투명하게(잘린 끝이 칼선으로 안 보이게)
    if fd and y + im.height < L['H'] + fd:
        import numpy as np
        a = np.array(im); h = a.shape[0]; r = np.ones(h); r[h - fd:] = np.linspace(1, 0, fd)
        a[:, :, 3] = (a[:, :, 3] * r[:, None]).astype('uint8'); im = Image.fromarray(a)
    tmp = Image.new('RGBA', cv.size, (0, 0, 0, 0)); tmp.paste(im, (x, y)); cv = Image.alpha_composite(cv, tmp)
    print(p['img'], f'k={k:.3f} left={x} top={y} bottom={y + im.height}')
gf = L.get('bottomFade', 0)   # 그림 전체 아래 gf px 도 서서히
if gf:
    import numpy as np
    a = np.array(cv); r = np.ones(a.shape[0]); r[-gf:] = np.linspace(1, 0, gf); a[:, :, 3] = (a[:, :, 3] * r[:, None]).astype('uint8'); cv = Image.fromarray(a)
cv.save(sys.argv[2]); print(sys.argv[2], cv.size, cv.getbbox())
