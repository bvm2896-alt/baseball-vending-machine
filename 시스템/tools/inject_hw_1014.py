# -*- coding: utf-8 -*-
"""10/14 롱폼⑭ 새 장면(yearcount·yearline)을 template_long.html·template_long_v.html 의 function render 앞에 넣는다(다시 돌리면 블록만 바꿈)."""
import io, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
js = io.open(os.path.join(H, 'scenes_hanwha_1014.js'), encoding='utf-8').read().rstrip('\n') + '\n'
blk = js if js.startswith('/* @@HW1014 */') else '/* @@HW1014 */\n' + js
for f in (sys.argv[1:] or ('template_long.html', 'template_long_v.html')):
    p = os.path.join(R, f); t = io.open(p, encoding='utf-8').read()
    if '/* @@HW1014 */' in t:
        t = re.sub(r'/\* @@HW1014 \*/.*?/\* @@HW1014END \*/\n', lambda m: blk, t, flags=re.S)
    else:
        i = t.index('function render(t) {'); t = t[:i] + blk + t[i:]
    io.open(p, 'w', encoding='utf-8').write(t); print('ok', f)
