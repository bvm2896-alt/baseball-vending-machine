# -*- coding: utf-8 -*-
"""10/8 롱폼⑨ 새 장면(tiers·capbar + viz·roster·debate)을 template_long.html·template_long_v.html 의 function render 앞에 넣는다(다시 돌리면 블록만 바꿈)."""
import io, os, re
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
js = ''.join(io.open(os.path.join(H, f), encoding='utf-8').read().rstrip('\n') + '\n' for f in ('scenes_fa_1008.js', 'scenes_info_1008.js'))   # 10/8 밤: 인포그래픽 장면도 같이
blk = '/* @@FA1008 */\n' + js.rstrip('\n') + '\n/* @@FA1008END */\n'
import sys
for f in (sys.argv[1:] or ('template_long.html', 'template_long_v.html')):   # 10/10: 롱폼 렌더 중엔 세로만 — python tools/inject_fa_1008.py template_long_v.html
    p = os.path.join(R, f); t = io.open(p, encoding='utf-8').read()
    if '/* @@FA1008 */' in t:
        t = re.sub(r'/\* @@FA1008 \*/.*?/\* @@FA1008END \*/\n', lambda m: blk, t, flags=re.S)
    else:
        i = t.index('function render(t) {'); t = t[:i] + blk + t[i:]
    io.open(p, 'w', encoding='utf-8').write(t); print('ok', f)
