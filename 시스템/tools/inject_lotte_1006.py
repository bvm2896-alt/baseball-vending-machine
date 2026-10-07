# -*- coding: utf-8 -*-
"""tools/scenes_lotte_1006.js 를 template_issue.html 의 `function render(t)` 바로 앞에 넣는다(이미 있으면 바꿔 끼움).
render 안에 s._t = t (장면이 호흡 시각을 알 수 있게) 한 줄도 넣는다. 여러 번 돌려도 같음."""
import io, os, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tp = os.path.join(HERE, 'template_issue.html')
js = io.open(os.path.join(HERE, 'tools', 'scenes_lotte_1006.js'), encoding='utf-8').read().strip()
h = io.open(tp, encoding='utf-8').read()
h = re.sub(r'/\* @@LOTTE1006 .*?/\* @@LOTTE1006 END \*/\n', '', h, flags=re.S)
h = h.replace('function render(t) {', js + '\nfunction render(t) {', 1)
if 's._t = t;' not in h:
    h = h.replace("  s._same = !!(s.cont && prev && prev.type === s.type);\n  (SCENE[s.type] || SCENE.big)(lt, s);",
                  "  s._same = !!(s.cont && prev && prev.type === s.type); s._t = t;\n  (SCENE[s.type] || SCENE.big)(lt, s);", 1)
assert 's._t = t;' in h and '@@LOTTE1006' in h
io.open(tp, 'w', encoding='utf-8').write(h)
print('ok', tp)
