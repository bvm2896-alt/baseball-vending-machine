# -*- coding: utf-8 -*-
"""10/15 컷5 '자막이 나레이션보다 밀림' 고침: 이미 만든 음성(NN.mp3)은 그대로 두고 자막 경계(NN.segs.json)만 다시 잡는다(크레딧 0).
원인: tts.seg_bounds 의 말 속도 기준 하한 0.08초/음절 — 1.2배 합성은 0.065~0.075 라 맞는 쉼을 버리고 경계를 한 칸씩 밀었다(하한 0.06 으로 고침).
사용: python -X utf8 tools\\fix_segs.py work\\voice_<콘티이름> [더 많은 폴더...]   (인자 없으면 가장 최근 날짜 롱폼컷 음성 폴더 전부)
lock(사람이 고정)·keep(구독 멘트 고정 음성)·한 호흡 줄은 건드리지 않는다. 바뀐 줄은 옛 경계 → 새 경계를 찍는다."""
import os, sys, json, glob, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE); sys.path.insert(0, HERE)
argv = sys.argv[1:]; sys.argv = ['tts.py']
import tts
dirs = argv
if not dirs:
    c = sorted(glob.glob(os.path.join('work', 'voice_*_롱폼컷*')))
    last = max((re.search(r'voice_(\d{4}-\d\d-\d\d)', d).group(1) for d in c), default=None)
    dirs = [d for d in c if last and last in d]
changed = []
for d in dirs:
    print('==', d); dch = False
    for mp3 in sorted(glob.glob(os.path.join(d, '[0-9][0-9].mp3'))):
        txt = mp3[:-4] + '.txt'; sj = mp3[:-4] + '.segs.json'
        if not os.path.exists(txt) or os.path.exists(mp3[:-4] + '.keep'): continue
        segs = [x.strip() for x in open(txt, encoding='utf-8').read().split('/') if x.strip()]
        if len(segs) <= 1: continue
        old = {}
        try: old = json.load(open(sj))
        except Exception: pass
        if old.get('lock'): print(' ', os.path.basename(mp3), '고정(lock) — 그대로'); continue
        b = [x for x, _ in tts.seg_bounds(mp3, segs)]
        durs = [round(b[k + 1] - b[k], 3) for k in range(len(b) - 1)] + [0.0]
        ob = old.get('bounds') or []
        ch = len(ob) != len(b) or any(abs(x - y) > 0.05 for x, y in zip(ob, b))
        json.dump({'durs': durs, 'pause': 0.0, 'bounds': b, 'src': 'fix_segs 1015'}, open(sj, 'w'))
        dch = dch or ch
        print(' ', os.path.basename(mp3), ('바뀜 ' if ch else '같음 ') + ' '.join(f'{x:.2f}' for x in ob[1:]), '→', ' '.join(f'{x:.2f}' for x in b[1:]))
    if dch: changed.append(d)
# 자막 경계가 바뀐 편은 롱폼_숏츠만들기가 다시 만들도록 만든 기록(work\\long_built.json)에서 뺀다(바뀐 장면 조각만 새로 그림)
bp = os.path.join('work', 'long_built.json')
try: B = json.load(open(bp, encoding='utf-8'))
except Exception: B = {}
gone = []
for d in changed:
    key = os.path.basename(d.rstrip('/\\'))[len('voice_'):] + '.json'
    for k in [k for k in B if k.endswith('|' + key)]: B.pop(k); gone.append(k)
if gone: json.dump(B, open(bp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n자막 경계가 바뀐 편:', ', '.join(os.path.basename(d) for d in changed) or '없음')
print('다시 만들 편으로 표시:', ', '.join(gone) or '없음', '→ 이제 야구롱폼\\롱폼_숏츠만들기.cmd 를 실행하세요')
