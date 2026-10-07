# -*- coding: utf-8 -*-
"""10/7 롱폼⑧ 새 장면(mvp10)을 template_long.html·template_long_v.html 의 function render 앞에 넣는다(다시 돌리면 블록만 바꿈)."""
import io, os, re
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
js = io.open(os.path.join(H, 'scenes_mvp_1007.js'), encoding='utf-8').read()
blk = '/* @@MVP1007 */\n' + js.rstrip('\n') + '\n/* @@MVP1007END */\n'
for f in ('template_long.html', 'template_long_v.html'):
    p = os.path.join(R, f); t = io.open(p, encoding='utf-8').read()
    if '/* @@MVP1007 */' in t:
        t = re.sub(r'/\* @@MVP1007 \*/.*?/\* @@MVP1007END \*/\n', lambda m: blk, t, flags=re.S)
    else:
        i = t.index('function render(t) {'); t = t[:i] + blk + t[i:]
    io.open(p, 'w', encoding='utf-8').write(t); print('ok', f)
