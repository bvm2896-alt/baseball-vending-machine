# -*- coding: utf-8 -*-
"""10/19 망상 극장 블록(tools/scenes_mang_1019.js)을 template_long.html 의 function render 앞에 넣고,
render 끝에 오버레이 호출(window.__mangFx)을 단다. 다시 돌려도 한 번만 들어간다."""
import re, sys, io
P = sys.argv[1] if len(sys.argv) > 1 else 'template_long.html'
h = io.open(P, encoding='utf-8').read(); js = io.open('tools/scenes_mang_1019.js', encoding='utf-8').read()
h = re.sub(r'/\* @@MANG1019.*?/\* @@MANG1019END \*/\n?', '', h, flags=re.S)
h = h.replace('function render(t) {', js.rstrip() + '\nfunction render(t) {', 1)
hook = "  drawRail(k, t); drawSub(t);\n"
if 'window.__mangFx' not in h.split('function render(t) {')[1][:4000]:
    h = h.replace(hook, hook + "  if (window.__mangFx) window.__mangFx(t, s, lt, k, start, end);   /* 10/19 망상 극장 */\n", 1)
io.open(P, 'w', encoding='utf-8').write(h); print('ok', P)
