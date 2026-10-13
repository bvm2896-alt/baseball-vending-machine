#!/usr/bin/env python3
"""롱폼⑬ 썸네일 v6 — 10개 구단 대표 10명 + 큰 글 2줄(강조줄이 더 큼, 행간 분리), 매번 다른 배경.
S: 선수 → (누끼 파일, 얼굴 중심 x, 얼굴 중심 y, 머리 높이 px — 전부 누끼 png 원본 좌표). 배치 L: (선수, 화면 얼굴 중심 x, y, 화면 머리 높이 px, z).
python3 work/l13/thumb13c.py [--dbg] [--check]   → work/l13/thumb13c.html (+ --check 면 얼굴 가림률 표)
10/13 사용자 지적: 다른 인물이 얼굴을 가리면 안 된다 → --check 로 가림률을 실제로 재고(15% 넘으면 고침) 넘긴다."""
import sys, os, numpy as np
from PIL import Image, ImageFont
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'work', 'l13'); NK = os.path.join(R, '..', '..', '..', '선수이미지', '누끼')   # tools 에 둔 보관본: work/l13 기준으로 동작
S = {
 '레이예스': ('경기_레이예스_양손가리키기_롯데제공_up', 1007, 300, 380), '데이비슨': ('경기_데이비슨_홈런후질주_키움제공', 454, 188, 235),
 '김재윤': ('경기_김재윤_투구_1007_삼성제공', 610, 355, 270), '손주영': ('경기_손주영_포효_LG제공', 660, 324, 223),
 '곽빈': ('경기_곽빈_박수_1006_두산제공', 721, 199, 245), '구창모': ('경기_구창모_투구_1006_NC제공', 452, 150, 189),
 '힐리어드': ('경기_힐리어드_미소손짓_KT제공', 741, 214, 225), '아빌라': ('경기_아빌라_글러브응시_SSG제공', 534, 301, 301),
 '김도영': ('경기_김도영_45호_포효_1012_스포츠조선', 676, 302, 330), '강백호': ('경기_강백호_헬멧인사_0915_한화제공', 745, 250, 300),
}
# 3줄 배치. 글 블록이 y≈440 부터라 3줄째 턱(얼굴 중심+머리/2)이 440 위에 오게.
L = [
 ('강백호', 65, 122, 180, 1), ('손주영', 330, 128, 180, 1), ('데이비슨', 640, 104, 150, 1), ('곽빈', 950, 122, 180, 1), ('김재윤', 1215, 120, 180, 1),
 ('힐리어드', 195, 268, 185, 3), ('레이예스', 420, 268, 185, 3), ('아빌라', 860, 268, 185, 3), ('구창모', 1085, 268, 185, 4), ('김도영', 640, 266, 190, 5),
]
TXT = [('2026 정규시즌 성적표', 't1'), ('우리팀은 몇점?', 't2')]
FONT = os.path.join(R, '..', '..', '..', '폰트', 'Jalnan2.ttf'); LS = -4; WMAX = 1236; FB_MAX = 152

def fitsize(txt, wmax, cap):
    f = 60
    while f < cap:
        w = ImageFont.truetype(FONT, f + 1).getlength(txt) + LS * len(txt)
        if w > wmax: break
        f += 1
    return f
fb = fitsize(TXT[1][0], WMAX, FB_MAX); fa = fitsize(TXT[0][0], WMAX, int(fb * 0.86))   # 강조줄(노랑)이 흰 줄보다 확실히 크게
ink = lambda f, t: ImageFont.truetype(FONT, f).getbbox(t)   # (l, top, r, bottom) — top 은 ascent 기준선에서의 잉크 시작
# line-height:1 블록 안에서 글리프 잉크 위치: 블록 top + (f - (ascent+descent))/2 + ascent + bbox.top ≈ 실측으로 맞춤 → 잉크 상·하단을 bbox 로 계산
def inkbox(f, t):
    fo = ImageFont.truetype(FONT, f); a, d = fo.getmetrics(); l, tp, r, bt = fo.getbbox(t)
    off = (f - (a + d)) / 2   # 크롬 line-height:1 에서 콘텐츠 박스 중앙 정렬
    return off + tp, off + bt
ta, ba = inkbox(fa, TXT[0][0]); tb, bb = inkbox(fb, TXT[1][0])
top2 = 712 - bb; top1 = top2 + tb - 28 - ba   # 두 줄 잉크 사이 28px — 1줄 그림자(8px 단색+14px 번짐)가 2줄 글자에 닿지 않게(10/13 사용자 '윗부분 잘림' 지적)
TEXT_TOP = top1 + ta
print(f'글 크기: 흰 {fa}px / 노랑 {fb}px, 잉크 1줄 {top1+ta:.0f}~{top1+ba:.0f}, 2줄 {top2+tb:.0f}~{top2+bb:.0f}')

imgs = []; masks = []
for n, cx, cy, hh, z in L:
    f, fcx, fcy, head = S[n]; im = Image.open(os.path.join(NK, f + '.png')).convert('RGBA'); bb_ = im.getbbox()
    crop = im.crop(bb_); fcx -= bb_[0]; fcy -= bb_[1]
    s = hh / head; W, H = round(crop.width * s), round(crop.height * s); left, top = cx - fcx * s, cy - fcy * s
    out = os.path.join(R, f'u2_{n}.png')
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(os.path.join(NK, f + '.png')): crop.save(out)
    if '--dbg' in sys.argv: imgs.append(f'<div style="position:absolute;left:{cx-15}px;top:{cy-2}px;width:30px;height:4px;background:#0f0;z-index:9"></div><div style="position:absolute;left:{cx-2}px;top:{cy-15}px;width:4px;height:30px;background:#0f0;z-index:9"></div>')
    imgs.append(f'<img class="p" src="u2_{n}.png" style="left:{left:.0f}px;top:{top:.0f}px;height:{H}px;z-index:{z}">')
    if '--check' in sys.argv:
        m = np.zeros((720, 1280), bool); a = np.array(crop.resize((W, H)).split()[-1]) > 128
        x0, y0 = int(round(left)), int(round(top)); xs0, ys0 = max(0, -x0), max(0, -y0); xs1, ys1 = min(W, 1280 - x0), min(H, 720 - y0)
        if xs1 > xs0 and ys1 > ys0: m[y0 + ys0:y0 + ys1, x0 + xs0:x0 + xs1] = a[ys0:ys1, xs0:xs1]
        masks.append((n, cx, cy, hh, z, m))
if '--check' in sys.argv:
    yy, xx = np.mgrid[0:720, 0:1280]; bad = 0
    order = sorted(range(len(masks)), key=lambda i: (masks[i][4], i))
    for i, (n, cx, cy, hh, z, m) in enumerate(masks):
        face = ((xx - cx) / (hh * 0.38)) ** 2 + ((yy - cy) / (hh * 0.5)) ** 2 <= 1
        above = np.zeros_like(face)
        for j in order:
            if (masks[j][4], j) > (z, i): above |= masks[j][5]
        tot = face.sum(); cov = (face & above).sum() / tot; txt = (face & (yy >= TEXT_TOP)).sum() / tot
        off = (face & ~m).sum() / tot; frame = 1 - face.sum() / (np.pi * hh * 0.38 * hh * 0.5)   # off: 자기 손·틈 등 투명(참고) / frame: 화면 밖(불통과)
        who = [masks[j][0] for j in order if (masks[j][4], j) > (z, i) and (face & masks[j][5]).sum() > tot * 0.03]
        cut = int(m[0:2, max(0, cx - int(hh * 0.3)):cx + int(hh * 0.3)].any())   # 머리(얼굴 폭 범위)가 화면 위 끝에 닿으면 잘린 것
        body = TEXT_TOP - (cy + hh * 0.5)   # 턱 아래 보이는 상체 높이(앞줄은 50px 이상 — 10/13 '얼굴만 달랑')
        flag = '  ← 고쳐야 함' if cov > 0.15 or txt > 0.03 or frame > 0.08 or (z >= 3 and body < 50) or cut else ''
        if flag: bad += 1
        print(f'{n:5s} 얼굴 가림 {cov*100:4.0f}% {who} / 글에 {txt*100:3.0f}% / 화면 밖 {frame*100:3.0f}% (자기 틈 {off*100:.0f}%) / 턱 아래 상체 {body:.0f}px / 머리 위 잘림 {cut}{flag}')
    print('문제', bad, '명')
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:J;src:url('../../../폰트/Jalnan2.ttf')}}
*{{margin:0;padding:0}}body{{width:1280px;height:720px;overflow:hidden;position:relative;font-family:J,sans-serif;background:#03121c}}
/* v6 배경: 전광판 네온 — 청록→남색 사선 + 빛줄기 + 육각 그물 (v5 노을보라·v4 이전과 다름) */
.bg{{position:absolute;inset:0;background:
 radial-gradient(ellipse 620px 420px at 50% 30%,rgba(120,255,240,.45) 0%,rgba(0,200,255,.25) 35%,rgba(0,0,0,0) 72%),
 radial-gradient(ellipse 600px 420px at 6% 8%,rgba(0,255,170,.45) 0%,rgba(0,0,0,0) 65%),
 radial-gradient(ellipse 600px 420px at 94% 8%,rgba(60,120,255,.55) 0%,rgba(0,0,0,0) 65%),
 linear-gradient(160deg,#0a3d62 0%,#0f7c8c 30%,#123a7a 62%,#06102a 100%)}}
.beams{{position:absolute;left:-250px;top:-760px;width:1780px;height:1780px;border-radius:50%;
 background:conic-gradient(from 140deg at 50% 50%,rgba(255,255,255,0) 0deg,rgba(180,255,255,.28) 4deg,rgba(255,255,255,0) 9deg,rgba(255,255,255,0) 16deg,rgba(180,255,255,.22) 21deg,rgba(255,255,255,0) 26deg,rgba(255,255,255,0) 36deg,rgba(180,255,255,.24) 41deg,rgba(255,255,255,0) 46deg,rgba(255,255,255,0) 56deg,rgba(180,255,255,.18) 60deg,rgba(255,255,255,0) 65deg,rgba(255,255,255,0) 100%);filter:blur(3px)}}
.hex{{position:absolute;inset:0;opacity:.55;background-image:
 linear-gradient(30deg,rgba(255,255,255,.14) 1px,transparent 1.5px),linear-gradient(150deg,rgba(255,255,255,.14) 1px,transparent 1.5px),linear-gradient(90deg,rgba(255,255,255,.14) 1px,transparent 1.5px);
 background-size:38px 66px,38px 66px,38px 66px;-webkit-mask-image:linear-gradient(180deg,rgba(0,0,0,.9),rgba(0,0,0,.3) 50%,rgba(0,0,0,0) 78%)}}
.stripe{{position:absolute;inset:0;background:repeating-linear-gradient(-28deg,rgba(255,255,255,0) 0 90px,rgba(255,255,255,.06) 90px 130px)}}
.spark{{position:absolute;border-radius:50%;background:#fff;box-shadow:0 0 16px 5px rgba(160,255,255,.9)}}
.floor{{position:absolute;left:0;right:0;bottom:0;height:330px;z-index:7;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(3,12,40,.6) 40%,rgba(3,12,40,.9))}}
.t{{position:absolute;left:0;width:1280px;text-align:center;line-height:1;letter-spacing:{LS}px;white-space:nowrap;z-index:8}}
.t1{{top:{top1:.0f}px;font-size:{fa}px;color:#fff;-webkit-text-stroke:3px #06203a;paint-order:stroke fill;text-shadow:0 0 28px rgba(0,220,255,.9),0 8px 0 #06203a,0 14px 26px rgba(0,0,0,.8)}}
.t2{{top:{top2-40:.0f}px;padding:40px 0;font-size:{fb}px;background:linear-gradient(180deg,#fffbd0 0%,#ffe13b 45%,#ff8a00 100%);-webkit-background-clip:text;color:transparent;
 filter:drop-shadow(0 0 3px #06203a) drop-shadow(0 0 3px #06203a) drop-shadow(0 0 22px rgba(255,220,80,.8)) drop-shadow(0 8px 0 #2a1a60) drop-shadow(0 14px 22px rgba(0,0,0,.8))}}
.p{{position:absolute;filter:drop-shadow(0 0 2px rgba(255,255,255,.55)) drop-shadow(0 22px 28px rgba(0,0,0,.65))}}
</style></head><body>
<div class="bg"></div><div class="beams"></div><div class="hex"></div><div class="stripe"></div>
<div class="spark" style="left:70px;top:150px;width:8px;height:8px"></div><div class="spark" style="left:1190px;top:120px;width:10px;height:10px"></div>
<div class="spark" style="left:980px;top:60px;width:6px;height:6px"></div><div class="spark" style="left:300px;top:70px;width:6px;height:6px"></div>
<div class="spark" style="left:1230px;top:300px;width:7px;height:7px"></div><div class="spark" style="left:40px;top:330px;width:7px;height:7px"></div>
{"".join(imgs)}
<div class="floor"></div>
<div class="t t1"><span>{TXT[0][0]}</span></div>
<div class="t t2"><span>{TXT[1][0]}</span></div>
<script>
// PIL 로 잰 크기가 크롬과 다르면 안쪽 span 폭으로 1236 에 맞춘다(블록 scrollWidth 는 1280 이라 못 씀 — 10/13 교훈)
for(const el of document.querySelectorAll('.t')){{const sp=el.querySelector('span');const f=parseFloat(el.style.fontSize||getComputedStyle(el).fontSize);const w=sp.getBoundingClientRect().width;if(w>{WMAX}){{el.style.fontSize=Math.floor(f*{WMAX}/w)+'px';}}}}
</script>
</body></html>'''
open(os.path.join(R, 'thumb13c.html'), 'w', encoding='utf-8').write(html); print('ok', len(L))
