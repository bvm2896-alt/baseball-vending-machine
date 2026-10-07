# -*- coding: utf-8 -*-
"""10/7 리뷰 썸네일 B안: 수평 저울 — 왼쪽 접시 KIA 로고, 오른쪽 접시 LG 로고, 가운데 '승차 0'(직접 그린 SVG, 크레딧 0)
출력: ../선수이미지/누끼/그림_KIA_LG_저울.png"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(HERE); sys.path.insert(0, HERE)
sys.argv = ['build.py']; import build
L = build.logos_data_uri(); W, H = 1080, 1000; INK = '#12161F'
def pan(cx, code):
    return (f'<path d="M{cx} 300 L{cx-170} 620 M{cx} 300 L{cx+170} 620" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M{cx-215} 620 Q{cx} 700 {cx+215} 620 Z" fill="#C9D0DB" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="470" r="150" fill="#fff" stroke="{INK}" stroke-width="10"/>'
            f'<image href="{L[code]}" x="{cx-115}" y="355" width="230" height="230" preserveAspectRatio="xMidYMid meet"/>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
       f'<path d="M540 300 L540 900" stroke="{INK}" stroke-width="26"/><path d="M380 960 L700 960 L620 900 L460 900 Z" fill="{INK}"/>'
       f'<rect x="150" y="282" width="780" height="36" rx="18" fill="#E5B84B" stroke="{INK}" stroke-width="9"/>'
       f'<circle cx="540" cy="300" r="34" fill="#E5484D" stroke="{INK}" stroke-width="9"/>'
       f'{pan(250, "HT")}{pan(830, "LG")}'
       f'<rect x="395" y="120" width="290" height="110" rx="55" fill="{INK}"/><text x="540" y="200" text-anchor="middle" font-family="KBO" font-weight="900" font-size="72" fill="#fff">승차 0</text></svg>')
FONT = 'file://' + os.path.abspath(os.path.join('..', '폰트', 'KBO Dia Gothic_bold.ttf'))
html = os.path.join(os.environ.get('SPD', '.'), 'thumb_scale_1007.html')
open(html, 'w', encoding='utf-8').write('<!doctype html><html><head><style>@font-face{font-family:KBO;src:url("' + FONT + '")}</style></head><body style="margin:0;background:transparent">' + svg + '</body></html>')
out = os.path.join('..', '선수이미지', '누끼', '그림_KIA_LG_저울.png')
js = f"""const {{chromium}}=require('{HERE}/node_modules/playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:{W},height:{H}}}}});await p.goto('file://{os.path.abspath(html)}');await p.waitForTimeout(400);await p.screenshot({{path:'{os.path.abspath(out)}',omitBackground:true}});await b.close();}})();"""
subprocess.run(['node', '-e', js], check=True); print('ok', out)
