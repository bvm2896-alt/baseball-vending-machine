# -*- coding: utf-8 -*-
"""10/12: 롱폼 음성만(prep → tts). 렌더는 클라우드에서. 야구롱폼\음성만.cmd 가 부른다.
11/27: 「10개 구단 역대 최악의 외국인」(다큐 톤, 화면은 클라우드 렌더) 음성으로 바꿈."""
import os, sys, subprocess
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ep = 'episodes/2026-11-27_롱폼.json'
# 11/27: 글자 수 확인은 사용자가 창에서 본 뒤 다시 누르는 것으로 대신(4,440자) → --chars-ok
for c in (['build.py', 'prep', ep], ['tts.py', '--chars-ok']):
    r = subprocess.call([sys.executable, '-X', 'utf8'] + c)
    if r: sys.exit(r)
print('VOICE DONE')
