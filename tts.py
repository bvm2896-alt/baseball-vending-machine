# -*- coding: utf-8 -*-
"""
타입캐스트 API로 나레이션 음성 생성
  python tts.py --test          → voice/test.mp3 한 줄 테스트
  python tts.py                 → work/narration.txt 각 줄 → work/voice/00.mp3, 01.mp3 ...
설정은 같은 폴더의 설정.txt 에서 읽는다 (TYPECAST_API_KEY, TYPECAST_VOICE_ID)
"""
import os, sys, json, time, subprocess, io
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

def load_cfg():
    cfg = {}
    with io.open('설정.txt', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    return cfg

CFG = load_cfg()
API_KEY = CFG.get('TYPECAST_API_KEY', '')
VOICE = CFG.get('TYPECAST_VOICE_ID', '')
if not API_KEY or not VOICE:
    sys.exit('설정.txt 에 TYPECAST_API_KEY 와 TYPECAST_VOICE_ID 를 채워주세요.')

EMOTION = CFG.get('TTS_EMOTION', 'smart')      # smart | normal | happy | sad | angry | whisper | toneup | tonemid | tonedown
INTENSITY = float(CFG.get('TTS_INTENSITY', '1.0'))
TEMPO = float(CFG.get('TTS_TEMPO', '1.0'))      # 타입캐스트 자체 배속. 줄별 속도 조절은 build.py 가 하므로 보통 1.0
URL = 'https://api.typecast.ai/v1/text-to-speech'
HEAD = {'X-API-KEY': API_KEY, 'Content-Type': 'application/json'}

import re
def check_audio(path, text):
    """길이가 글자 수 대비 비정상이거나 클리핑이 있으면 False"""
    try:
        d = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',path],capture_output=True,text=True).stdout.strip())
        r = subprocess.run(['ffmpeg','-i',path,'-af','volumedetect','-f','null','-'],capture_output=True,text=True)
        mx = float(re.search(r'max_volume: ([\-\d.]+)', r.stderr).group(1))
        syl = len(re.findall(r'[가-힣]', text)) or 1
        rate = syl / max(d, 0.1)
        if mx > -0.05: return False, f'클리핑 {mx}dB'   # 음량 정리는 build.py 가 하므로 진짜 클리핑만 재시도
        if rate > 9.5 or rate < 2.5: return False, f'길이 이상 {d:.1f}s/{syl}음절'
        return True, ''
    except Exception as e:
        return True, ''

def prompt_variants(prev, nxt):
    """설정.txt 의 TTS_EMOTION 에 따라 prompt 후보를 순서대로 (400 이면 다음 후보로)"""
    if EMOTION == 'smart':
        return [{'emotion_type': 'smart', 'previous_text': prev, 'next_text': nxt}]
    return [{'emotion_type': 'preset', 'emotion_preset': EMOTION, 'emotion_intensity': INTENSITY},
            {'emotion_preset': EMOTION, 'emotion_intensity': INTENSITY},
            {'emotion_type': 'smart', 'previous_text': prev, 'next_text': nxt}]

def synth(text, prev='', nxt='', out_path='work/voice/out.mp3'):
    """한 줄 합성. 앞뒤 문장을 같이 보내면 억양이 자연스럽게 이어진다."""
    prompts = prompt_variants(prev, nxt)
    payload = {
        'model': 'ssfm-v30',
        'text': text,
        'voice_id': VOICE,
        'prompt': prompts[0],
        'output': ({'audio_format': 'mp3', 'audio_tempo': TEMPO} if abs(TEMPO - 1.0) > 0.01 else {'audio_format': 'mp3'}),
    }
    pi = 0
    for attempt in range(6):
        r = requests.post(URL, headers=HEAD, json=payload, timeout=60)
        if r.status_code == 200:
            ctype = r.headers.get('Content-Type', '')
            print(f'  응답 {ctype} {len(r.content)} bytes')
            if 'wav' in ctype or r.content[:4] == b'RIFF':
                # wav 로 왔으면 mp3 로 변환 (헤더의 길이 정보가 틀린 경우가 있어 무시하고 끝까지 읽는다)
                tmp = out_path + '.wav'
                open(tmp, 'wb').write(r.content)
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ignore_length', '1', '-i', tmp,
                                '-b:a', '192k', out_path], check=True)
                if '--keep' not in sys.argv:
                    os.remove(tmp)
            else:
                open(out_path, 'wb').write(r.content)
            ok, why = check_audio(out_path, text)
            if not ok and attempt < 5:
                print(f'  품질 재시도({why})'); time.sleep(1); continue
            return True
        if r.status_code == 400:
            # 감정 형식이 안 맞으면 다음 후보, 그래도 안 되면 output 의 배속 옵션을 뺀다
            if pi + 1 < len(prompts):
                pi += 1; payload['prompt'] = prompts[pi]; print(f'  감정 형식 재시도({pi})'); continue
            if 'audio_tempo' in payload.get('output', {}):
                payload['output'] = {'audio_format': 'mp3'}; print('  배속 옵션 없이 재시도'); continue
            if 'output' in payload:
                payload.pop('output'); continue
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 + attempt * 2)
            continue
        print(f'  실패 {r.status_code}: {r.text[:300]}')
        return False
    return False

os.makedirs('work/voice', exist_ok=True)

if __name__ == '__main__' and '--test' in sys.argv:
    ok = synth('야구자판기 음성 테스트예요. 삼성이 일위, 케이티가 영점오 게임 차예요.', out_path='work/voice/test.mp3')
    print('OK → work/voice/test.mp3 재생해 보세요.' if ok else '실패')
    sys.exit(0 if ok else 1)

def load_lines():
    return [l.strip() for l in io.open('work/narration.txt', encoding='utf-8-sig') if l.strip()]
PAUSE = float(CFG.get('TTS_PAUSE', '0.12'))   # 대사 안의 " / " 표시 자리에서 쉬는 시간(초). 구간 자체의 앞뒤 무음은 잘라내므로 아주 짧게

def tts_text(segs, is_last_q=False):
    """TTS 에 넣을 문장: 호흡 구간(' / ')은 쉼표로, 끝은 마침표/물음표로 → 한 사람이 쭉 읽는 자연스러운 억양.
    (쉼표·마침표 금지 규칙은 화면 자막 얘기고, TTS 입력엔 넣어야 억양이 자연스럽다)"""
    t = ', '.join(segs)
    if not t.endswith(('?', '!', '.')): t += '.'
    return t

def probe_silences(path, thr='-35dB', mind=0.06):
    r = subprocess.run(['ffmpeg', '-i', path, '-af', f'silencedetect=n={thr}:d={mind}', '-f', 'null', '-'], capture_output=True, text=True)
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip() or 0)
    if len(en) < len(st): en.append(d)
    return d, list(zip(st, en))

def seg_bounds(path, segs):
    """한 번에 합성한 음성 안에서 각 호흡 구간이 시작하는 시각(초)과 그 자리의 실제 쉼(무음 구간).
    타입캐스트는 쉼표마다 짧게 쉬므로, 음성 속 쉼의 개수가 호흡 구간 경계 수와 같으면 그대로 순서대로 쓴다.
    더 많으면 글자 수 비율로 예상한 위치에 가장 잘 맞는 조합을 고르고, 적으면 있는 것만 맞추고 나머지는 비율로 추정.
    반환: [(시작초, (무음시작,무음끝) 또는 None)]"""
    d, sil = probe_silences(path, thr='-36dB', mind=0.08)
    lead = sil[0][1] if sil and sil[0][0] < 0.02 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] >= d - 0.03 else d
    inner = [(a, b) for a, b in sil if a > lead + 0.05 and b < tail - 0.05]
    need = len(segs) - 1
    syl = [max(1, len(re.findall(r'[가-힣A-Za-z0-9]', x))) for x in segs]
    tot = sum(syl); speech = max(0.2, tail - lead)
    exp = []
    acc = 0
    for k in range(need):
        acc += syl[k]; exp.append(lead + speech * acc / tot)
    chosen = [None] * need
    if len(inner) == need:
        chosen = list(inner)
    elif len(inner) > need:
        # 순서를 지키며 need 개 고르기: 예상 위치와의 차이 합이 최소인 조합 (동적 계획법)
        import functools
        mids = [(a + b) / 2 for a, b in inner]
        @functools.lru_cache(None)
        def best(i, k):   # inner[i:] 에서 exp[k:] 를 순서대로 맞출 때 최소 비용, 선택 인덱스
            if k == need: return (0.0, ())
            if len(inner) - i < need - k: return (1e9, ())
            skip = best(i + 1, k)
            c, rest = best(i + 1, k + 1)
            take = (c + abs(mids[i] - exp[k]), (i,) + rest)
            return min(skip, take, key=lambda x: x[0])
        for k, idx in enumerate(best(0, 0)[1]): chosen[k] = inner[idx]
    else:
        # 쉼이 부족: 가까운 예상 위치에 하나씩 배정
        used = set()
        for a, b in inner:
            m = (a + b) / 2
            k = min((abs(m - e), j) for j, e in enumerate(exp) if j not in used)[1] if len(used) < need else None
            if k is not None: chosen[k] = (a, b); used.add(k)
    out, prev = [(0.0, None)], lead
    for k in range(need):
        iv = chosen[k]
        pos = iv[1] if iv else max(prev + 0.15, exp[k])
        out.append((round(pos, 3), iv)); prev = pos
    return out

BREATH = float(CFG.get('TTS_BREATH', '0.18'))   # 긴 대사의 호흡 자리(' / ')에 살짝 끼워 넣는 쉼(초). 실제 쉼이 감지된 자리에만 넣는다

def insert_breaths(path, bounds):
    """실제 쉼이 감지된 호흡 자리마다 BREATH 초의 무음을 끼워 넣어 '와다다다' 읽는 느낌을 없앤다. 새 경계 목록을 돌려준다"""
    cuts = [iv for _, iv in bounds[1:] if iv]
    if not cuts or BREATH <= 0: return [b for b, _ in bounds]
    wav = path.replace('.mp3', '_w.wav'); sil = path.replace('.mp3', '_b.wav'); lst = path.replace('.mp3', '_b.txt')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-ar', '44100', '-ac', '1', wav], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', f'{BREATH:.2f}', sil], check=True)
    mids = [round((a + b) / 2, 3) for a, b in cuts]
    pieces, start = [], 0.0
    for j, m in enumerate(mids + [None]):
        pc = path.replace('.mp3', f'_p{j}.wav')
        af = f'atrim=start={start:.3f}' + (f':end={m:.3f}' if m else '') + ',asetpts=PTS-STARTPTS'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', af, pc], check=True)
        pieces.append(pc); start = m or start
    with open(lst, 'w', encoding='utf-8') as f:
        for j, pc in enumerate(pieces):
            if j: f.write(f"file '{os.path.basename(sil)}'\n")
            f.write(f"file '{os.path.basename(pc)}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-ar', '44100', '-ac', '1', '-b:a', '192k', path], check=True)
    for f_ in pieces + [wav, sil, lst]:
        try: os.remove(f_)
        except Exception: pass
    # 경계 보정: 각 경계 앞에 끼워 넣은 쉼만큼 뒤로 밀린다
    new, n_ins = [], 0
    for b, iv in bounds:
        if iv: n_ins += 1
        new.append(round(b + n_ins * BREATH, 3))
    return new

def synth_line(line, prev, nxt, out, pause=None):
    """한 줄 합성. ' / ' 로 나뉜 호흡 구간을 따로 만들지 않고 한 문장으로 합성한다(억양이 끊기지 않게).
    그 다음 실제 쉼이 감지된 호흡 자리에만 짧은 쉼(TTS_BREATH)을 끼워 넣고, 경계를 NN.segs.json 에 기록 → build.py 가 자막을 구간별로 바꾼다"""
    segs = [x.strip() for x in line.split('/') if x.strip()]
    text = tts_text(segs) if segs else line
    p_ = [x.strip() for x in prev.split('/') if x.strip()]; n_ = [x.strip() for x in nxt.split('/') if x.strip()]
    ok = synth(text, tts_text(p_) if p_ else '', tts_text(n_) if n_ else '', out)
    sj = out.replace('.mp3', '.segs.json')
    if not ok: return False
    if len(segs) <= 1:
        try: os.remove(sj)
        except Exception: pass
        return True
    try:
        bounds = seg_bounds(out, segs)
        b = insert_breaths(out, bounds) if pause is None else [x for x, _ in bounds]   # pause=0 이면(후킹 대사) 쉼을 안 넣는다
        durs = [b[k + 1] - b[k] for k in range(len(b) - 1)] + [0.0]
        json.dump({'durs': durs, 'pause': 0.0, 'bounds': b, 'breaths': sum(1 for _, iv in bounds[1:] if iv)}, open(sj, 'w'))
    except Exception as e:
        print('  구간 추정 실패(자막은 한 덩어리로):', e)
        try: os.remove(sj)
        except Exception: pass
    return True

def synth_index(lines, i, out=None):
    """i번째 줄 합성(앞뒤 문맥 포함). qa_voice.py 가 다시 만들 때도 이걸 쓴다"""
    prev = lines[i-1] if i > 0 else ''
    nxt = lines[i+1] if i+1 < len(lines) else ''
    out = out or f'work/voice/{i:02d}.mp3'
    return synth_line(lines[i], prev, nxt, out, pause=0 if i == 0 else None)   # 첫 줄(후킹)은 한 호흡

if __name__ == '__main__':
    lines = load_lines()
    only = None
    for a in sys.argv:
        if a.startswith('--only='): only = {int(x) for x in a.split('=',1)[1].replace(',', ' ').split()}
    print(f'{len(lines)}줄 합성 시작' + (f' (줄 {sorted(only)} 만)' if only else ''))
    fail = 0
    for i, line in enumerate(lines):
        if only is not None and i not in only: continue
        ok = synth_index(lines, i)
        print(f'{i:02d} {"OK " if ok else "XX "} {line}')
        fail += (not ok)
        time.sleep(0.3)
    if fail:
        sys.exit(f'{fail}줄 실패')
    print('완료')
