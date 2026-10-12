# -*- coding: utf-8 -*-
"""10/12: 롱폼⑫ 음성만(prep → tts). 렌더는 클라우드에서. 야구롱폼\음성만.cmd 가 부른다."""
import os, sys, subprocess
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ep = 'episodes/2026-10-12_롱폼.json'
for c in (['build.py', 'prep', ep], ['tts.py']):
    r = subprocess.call([sys.executable, '-X', 'utf8'] + c)
    if r: sys.exit(r)
print('VOICE DONE')
