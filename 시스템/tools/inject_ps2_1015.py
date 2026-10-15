# -*- coding: utf-8 -*-
"""10/15: tools/scenes_ps2_1015.js 를 scenes_ps_1015.js 안 @@PS2_1015 블록에 넣고 두 템플릿에 다시 주입한다."""
import io, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(H, 'scenes_ps_1015.js'); t = io.open(p, encoding='utf-8').read()
add = io.open(os.path.join(H, 'scenes_ps2_1015.js'), encoding='utf-8').read()
t = re.sub(r'/\* @@PS2_1015 \*/.*?/\* @@PS2_1015END \*/\n', '', t, flags=re.S)
end = '})();\n/* @@PS1015END */'; assert end in t
t = t.replace(end, '/* @@PS2_1015 */\n' + add + '/* @@PS2_1015END */\n' + end)
io.open(p, 'w', encoding='utf-8').write(t)
subprocess.run([sys.executable, os.path.join(H, 'inject_ps_1015.py')], check=True)
