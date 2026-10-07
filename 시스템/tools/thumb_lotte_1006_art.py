# -*- coding: utf-8 -*-
"""10/6 롯데 고춧가루 쇼츠 썸네일 그림(사용자 지정): 얼굴 = 롯데 로고인 캐릭터가 고춧가루 통을 들고,
그 앞에서 얼굴 = KIA·LG·두산 로고인 캐릭터 3명이 굽신거린다. 직접 그린 SVG(크레딧 0) → 투명 PNG
출력: ../선수이미지/누끼/그림_롯데고춧가루_굽신.png (thumb.cutout 으로 쓴다)"""
import os, sys, json, subprocess
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE); sys.path.insert(0, HERE)
sys.argv = ['build.py']; import build
LG_ = build.logos_data_uri()
W, H = 1080, 1240
NAVY, RED = '#0B2349', '#E5484D'
def head(cx, cy, r, code, rot=0, ring='#12161F'):
    s = r * 1.5
    return f'''<g transform="rotate({rot} {cx} {cy})"><circle cx="{cx}" cy="{cy+8}" r="{r}" fill="rgba(0,0,0,.18)"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{ring}" stroke-width="10"/>
      <image href="{LG_[code]}" x="{cx-s/2}" y="{cy-s/2}" width="{s}" height="{s}" preserveAspectRatio="xMidYMid meet"/></g>'''
def glove(x, y, r=34):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#12161F" stroke-width="7"/>'
def shaker(x, y, sc=1.0, rot=0):
    lg = LG_['LT']
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({sc})">
      <g transform="rotate(180 0 0)"><rect x="-38" y="-100" width="76" height="40" rx="12" fill="#12161F"/>
      {''.join(f'<circle cx="{a}" cy="{b}" r="4.5" fill="#F4F6FA"/>' for a,b in [(-18,-88),(0,-92),(18,-88),(-9,-76),(9,-76)])}
      <rect x="-30" y="-62" width="60" height="12" fill="#2A303C"/>
      <rect x="-48" y="-52" width="96" height="150" rx="26" fill="#E0303B" stroke="#12161F" stroke-width="7"/>
      <rect x="-36" y="-40" width="12" height="118" rx="6" fill="#fff" opacity=".3"/></g>
      <circle cx="0" cy="-20" r="34" fill="#fff"/><image href="{lg}" x="-27" y="-47" width="54" height="54"/></g>'''
def flakes(x0, y0, pts, n=70):
    o = ''
    for i in range(n):
        tx, ty = pts[i % len(pts)]
        f = ((i * 37) % 100) / 100
        x = x0 + (tx - x0) * f + ((i * 53) % 41 - 20) * (0.4 + f)
        y = y0 + (ty - y0) * f + ((i * 29) % 31 - 15)
        r = 5 + (i % 4) * 2
        o += f'<rect x="{x:.0f}" y="{y:.0f}" width="{r}" height="{r*0.8:.0f}" rx="2" fill="{["#E5484D","#B3121F","#F06A4F"][i%3]}" transform="rotate({i*33} {x:.0f} {y:.0f})"/>'
    return o
def sweat(x, y, s=1.0):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 -26 C10 -8 18 4 18 14 A18 18 0 0 1 -18 14 C-18 4 -10 -8 0 -26Z" fill="#5AB8FF" stroke="#12161F" stroke-width="5"/>'
def bow(cx, code, col, rot):
    hy = 985
    torso = (f'<path d="M{cx-160} 1240 L{cx-158} 960 Q{cx-150} 880 {cx-92} 872 Q{cx-40} 900 {cx} 900 Q{cx+40} 900 {cx+92} 872 Q{cx+150} 880 {cx+158} 960 L{cx+160} 1240 Z" fill="{col}" stroke="#12161F" stroke-width="9"/>')
    arms = (f'<path d="M{cx-130} 960 Q{cx-135} 1130 {cx-40} 1135" fill="none" stroke="#12161F" stroke-width="66" stroke-linecap="round"/>'
            f'<path d="M{cx-130} 960 Q{cx-135} 1130 {cx-40} 1135" fill="none" stroke="{col}" stroke-width="52" stroke-linecap="round"/>'
            f'<path d="M{cx+130} 960 Q{cx+135} 1130 {cx+40} 1135" fill="none" stroke="#12161F" stroke-width="66" stroke-linecap="round"/>'
            f'<path d="M{cx+130} 960 Q{cx+135} 1130 {cx+40} 1135" fill="none" stroke="{col}" stroke-width="52" stroke-linecap="round"/>')
    hands = glove(cx - 22, 1128, 36) + glove(cx + 22, 1118, 36)
    rub = (f'<path d="M{cx-78} 1100 q-16 -14 -10 -36" fill="none" stroke="#12161F" stroke-width="7" stroke-linecap="round"/>'
           f'<path d="M{cx+78} 1100 q16 -14 10 -36" fill="none" stroke="#12161F" stroke-width="7" stroke-linecap="round"/>')
    bowl = (f'<path d="M{cx-150} {hy-170} q18 -44 64 -54" fill="none" stroke="#12161F" stroke-width="8" stroke-linecap="round"/>'
            f'<path d="M{cx-172} {hy-122} q14 -30 46 -38" fill="none" stroke="#12161F" stroke-width="8" stroke-linecap="round"/>'
            f'<text x="{cx-30}" y="{hy-196}" text-anchor="middle" font-family="KBO, Noto Sans CJK KR" font-weight="900" font-size="46" fill="#12161F" stroke="#fff" stroke-width="10" paint-order="stroke" transform="rotate(-10 {cx-30} {hy-196})">굽신</text>')
    return torso + head(cx, hy, 118, code, rot) + arms + hands + rub + bowl + sweat(cx + 122, hy - 92, 1.0) + sweat(cx + 152, hy - 30, .7)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <!-- 롯데: 뒤에 크게, 한 손은 허리, 한 손은 고춧가루 통 -->
  <path d="M370 1240 L380 560 Q390 470 470 455 L610 455 Q690 470 700 560 L710 1240 Z" fill="{NAVY}" stroke="#12161F" stroke-width="10"/>
  <path d="M540 470 L540 760" stroke="{RED}" stroke-width="16"/>
  <path d="M400 520 Q300 600 360 690" fill="none" stroke="{NAVY}" stroke-width="64" stroke-linecap="round"/>
  {glove(372, 690, 40)}
  <path d="M680 520 Q790 470 840 330" fill="none" stroke="{NAVY}" stroke-width="64" stroke-linecap="round"/>
  {head(540, 300, 175, 'LT', -7, '#12161F')}
  <path d="M445 175 l40 18 M635 175 l-40 18" stroke="#12161F" stroke-width="12" stroke-linecap="round"/>
  {shaker(860, 300, 1.35, 40)}
  {glove(842, 330, 42)}
  {flakes(770, 420, [(190, 860), (540, 860), (890, 860), (360, 820), (700, 820)], 80)}
  {bow(190, 'HT', '#C8102E', 18)}
  {bow(890, 'OB', '#1A1748', -18)}
  {bow(540, 'LG', '#A50034', 8)}
</svg>'''
out_html = os.path.join(os.environ.get('SPD', '.'), 'thumb_art_1006.html')
FONT = 'file://' + os.path.abspath(os.path.join('..', '폰트', 'KBO Dia Gothic_bold.ttf'))
open(out_html, 'w', encoding='utf-8').write('<!doctype html><html><head><style>@font-face{font-family:KBO;src:url("' + FONT + '")}</style></head>'
    '<body style="margin:0;background:transparent">' + svg + '</body></html>')
out_png = os.path.join('..', '선수이미지', '누끼', '그림_롯데고춧가루_굽신.png')
js = f"""const {{chromium}}=require('{HERE}/node_modules/playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{W},height:{H}}}}});
await p.goto('file://{os.path.abspath(out_html)}');await p.waitForTimeout(300);await p.screenshot({{path:'{os.path.abspath(out_png)}',omitBackground:true}});await b.close();}})();"""
subprocess.run(['node', '-e', js], check=True)
print('ok', out_png)
