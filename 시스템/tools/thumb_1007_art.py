# -*- coding: utf-8 -*-
"""10/7 리뷰 쇼츠(KIA LG 승차 0) 썸네일 그림: KIA·LG 로고 얼굴 캐릭터가 '3위' 깃발이 가운데 걸린 줄을 당기는 줄다리기(직접 그린 SVG, 크레딧 0)
출력: ../선수이미지/누끼/그림_KIA_LG_줄다리기.png (thumb.cutout 으로 쓴다)"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE); sys.path.insert(0, HERE)
sys.argv = ['build.py']; import build
LG_ = build.logos_data_uri()
W, H = 1080, 1100
INK = '#12161F'

def head(cx, cy, r, code, rot=0):
    s = r * 1.5
    return f'''<g transform="rotate({rot} {cx} {cy})"><circle cx="{cx}" cy="{cy+8}" r="{r}" fill="rgba(0,0,0,.18)"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="10"/>
      <image href="{LG_[code]}" x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" preserveAspectRatio="xMidYMid meet"/></g>'''
def glove(x, y, r=36):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="7"/>'
def sweat(x, y, s=1.0):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -26 C10 -8 18 4 18 14 A18 18 0 0 1 -18 14 C-18 4 -10 -8 0 -26Z" fill="#5AB8FF" stroke="{INK}" stroke-width="5"/>'
def puller(cx, code, col, trim, side):
    # side = -1 (왼쪽 사람, 왼쪽으로 당김) / +1 (오른쪽 사람)
    lean = -10 * side           # 몸을 바깥쪽으로 젖힘(위가 바깥으로)
    hx, hy = cx + 40 * side, 330
    body = (f'<g transform="rotate({lean} {cx} 900)">'
            f'<path d="M{cx-125} 1100 L{cx-120} 560 Q{cx-110} 470 {cx-40} 460 L{cx+40} 460 Q{cx+110} 470 {cx+120} 560 L{cx+125} 1100 Z" fill="{col}" stroke="{INK}" stroke-width="10"/>'
            f'<path d="M{cx} 470 L{cx} 1100" stroke="{trim}" stroke-width="16"/></g>')
    # 두 팔을 가운데(줄) 쪽으로 쭉 뻗음
    ax = cx - 210 * side
    arms = ''
    for dy, gx in ((0, ax), (34, ax + 60 * side)):
        arms += (f'<path d="M{cx - 60*side} {560+dy} Q{(cx+gx)/2} {610+dy} {gx} {640+dy}" fill="none" stroke="{INK}" stroke-width="66" stroke-linecap="round"/>'
                 f'<path d="M{cx - 60*side} {560+dy} Q{(cx+gx)/2} {610+dy} {gx} {640+dy}" fill="none" stroke="{col}" stroke-width="52" stroke-linecap="round"/>')
    hands = glove(ax, 640) + glove(ax + 60 * side, 674)
    effort = (f'<path d="M{hx + 150*side} {hy-120} l{40*side} -30 M{hx + 165*side} {hy-60} l{48*side} -10 M{hx + 160*side} {hy} l{44*side} 14" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    brows = (f'<path d="M{hx-80} {hy-108} l50 {16 if side<0 else 8} M{hx+80} {hy-108} l-50 {16 if side<0 else 8}" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>')
    return body + arms + head(hx, hy, 160, code, -6 * side) + brows + hands + effort + sweat(hx - 150*side, hy - 60, 1.1) + sweat(hx - 175*side, hy + 10, .75)

rope = f'<path d="M150 655 Q540 690 930 655" fill="none" stroke="#B8894A" stroke-width="22" stroke-linecap="round"/><path d="M150 655 Q540 690 930 655" fill="none" stroke="#7A5A2E" stroke-width="22" stroke-dasharray="6 18" stroke-linecap="round"/>'
flag = (f'<g transform="translate(540 676)"><path d="M0 0 L0 22" stroke="{INK}" stroke-width="8"/>'
        f'<path d="M-140 20 L140 20 L0 300 Z" fill="#E5484D" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>'
        f'<text x="0" y="128" text-anchor="middle" font-family="KBO" font-weight="900" font-size="80" fill="#fff">3위</text></g>')
center = f'<path d="M540 760 L540 1100" stroke="{INK}" stroke-width="8" stroke-dasharray="20 16"/>'
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'{center}{puller(250, "HT", "#C8102E", "#12161F", -1)}{puller(830, "LG", "#1A1A1A", "#C30452", 1)}{rope}{flag}</svg>')
FONT = 'file://' + os.path.abspath(os.path.join('..', '폰트', 'KBO Dia Gothic_bold.ttf'))
out_html = os.path.join(os.environ.get('SPD', '.'), 'thumb_art_1007.html')
open(out_html, 'w', encoding='utf-8').write('<!doctype html><html><head><style>@font-face{font-family:KBO;src:url("' + FONT + '")}</style></head>'
                                           '<body style="margin:0;background:transparent">' + svg + '</body></html>')
out_png = os.path.join('..', '선수이미지', '누끼', '그림_KIA_LG_줄다리기.png')
js = f"""const {{chromium}}=require('{HERE}/node_modules/playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{W},height:{H}}}}});
await p.goto('file://{os.path.abspath(out_html)}');await p.waitForTimeout(400);await p.screenshot({{path:'{os.path.abspath(out_png)}',omitBackground:true}});await b.close();}})();"""
subprocess.run(['node', '-e', js], check=True)
print('ok', out_png)
