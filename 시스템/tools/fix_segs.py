# -*- coding: utf-8 -*-
"""10/31 노트북: FFmpeg 설치 전에 API 음성을 만들어서 호흡 경계(NN.segs.json)·긴 쉼 줄이기가 빠진 줄을 다시 잡는다(재합성 없음 · 크레딧 0).
쓰는 법: 시스템 폴더에서  python -X utf8 tools\fix_segs.py   → 끝나면 롱폼검수.cmd 다시 실행.
segs.json 이 이미 있는 줄은 건드리지 않는다(쉼을 두 번 넣지 않게). 고정 음성(.keep) 줄도 건드리지 않는다."""
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE); sys.path.insert(0, HERE)
import tts
lines = tts.load_lines()
print('음성 폴더:', tts.VDIR, '·', len(lines), '줄')
done = skip = 0
for i, line in enumerate(lines):
    mp3 = os.path.join(tts.VDIR, f'{i:02d}.mp3')
    if not os.path.exists(mp3) or os.path.exists(mp3.replace('.mp3', '.keep')): skip += 1; continue
    if '/' not in line or os.path.exists(mp3.replace('.mp3', '.segs.json')): skip += 1; continue
    tts.mark_breaths(mp3, line, first=False)
    ok = os.path.exists(mp3.replace('.mp3', '.segs.json'))
    done += ok
    print(f'{i:02d} {"OK" if ok else "실패"} {line}')
print(f'끝: 호흡 경계 다시 잡음 {done}줄 · 그대로 {skip}줄')
