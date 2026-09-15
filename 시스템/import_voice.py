#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
외부(힉스필드 등)에서 만든 음성을 편 음성 폴더로 가져온다.
  python -X utf8 import_voice.py work\voice_import.json
voice_import.json: {"episode": "2026-09-13_이슈", "lines": [{"i": 0, "url": "...wav", "text": "대사"}, ...]}
→ work\voice_<episode>\NN.mp3 (44.1kHz 모노 192k) + NN.txt (대사 기록). 이후 지금실행/영상만다시 를 누르면
  tts.py 가 '이미 있음' 으로 건너뛰고 qa_voice → 렌더로 이어진다.
"""
import sys, os, json, io, subprocess, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join('work', 'voice_import.json')
spec = json.load(io.open(src, encoding='utf-8-sig'))
vdir = os.path.join('work', 'voice_' + spec['episode']); os.makedirs(vdir, exist_ok=True)
io.open(os.path.join('work', 'current.txt'), 'w', encoding='utf-8').write(spec['episode'])
ok = 0
for it in spec['lines']:
    i = int(it['i']); tmp = os.path.join(vdir, f'{i:02d}.src'); mp3 = os.path.join(vdir, f'{i:02d}.mp3')
    try:
        urllib.request.urlretrieve(it['url'], tmp)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-ar', '44100', '-ac', '1', '-b:a', '192k', mp3], check=True)
        io.open(mp3.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(it['text'])
        for extra in ('.segs.json',):
            p = mp3.replace('.mp3', extra)
            if os.path.exists(p): os.remove(p)   # 옛 구간 정보는 지운다(새 음성에 맞게 다시 계산)
        d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp3], capture_output=True, text=True).stdout.strip()
        print(f'{i:02d} OK {float(d or 0):.1f}s  {it["text"][:40]}'); ok += 1
    except Exception as e:
        print(f'{i:02d} 실패: {e}')
    finally:
        try: os.remove(tmp)
        except Exception: pass
print(f'{ok}/{len(spec["lines"])}줄 가져옴 → {vdir}')
