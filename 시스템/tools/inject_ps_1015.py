# -*- coding: utf-8 -*-
"""10/15 롱폼 와일드카드·준PO: tools/scenes_ps_1015.js 를 template_long.html·template_long_v.html 의 function render 앞에 넣는다(다시 돌리면 블록만 바꿈)."""
import io, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
blk = io.open(os.path.join(H, 'scenes_ps_1015.js'), encoding='utf-8').read()
for f in (sys.argv[1:] or ('template_long.html', 'template_long_v.html')):
    p = os.path.join(R, f); t = io.open(p, encoding='utf-8').read()
    if '/* @@PS1015 */' in t:
        t = re.sub(r'/\* @@PS1015 \*/.*?/\* @@PS1015END \*/\n', lambda m: blk, t, flags=re.S)
    else:
        i = t.index('function render(t) {'); t = t[:i] + blk + t[i:]
    io.open(p, 'w', encoding='utf-8').write(t); print('ok', f)
