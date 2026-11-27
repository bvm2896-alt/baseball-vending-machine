# -*- coding: utf-8 -*-
"""11/27 11:00 사용자: 톤 시험 C(tonedown 세기 0.4)가 제일 좋다 → 118줄 전부 그 설정으로 다시 합성(--fresh). 야구롱폼\음성만_톤C.cmd 가 부른다."""
import os, sys, subprocess
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['TTS_INTENSITY'] = '0.4'
ep = 'episodes/2026-11-27_롱폼.json'
for c in (['build.py', 'prep', ep], ['tts.py', '--chars-ok', '--fresh']):
    r = subprocess.call([sys.executable, '-X', 'utf8'] + c)
    if r: sys.exit(r)
print('VOICE C DONE')
