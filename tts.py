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
# 계정(키)을 여러 개 등록해 두면 크레딧이 떨어진 계정은 건너뛰고 다음 계정으로 자동 전환한다.
#   TYPECAST_API_KEY=…  TYPECAST_VOICE_ID=…            (1번 계정)
#   TYPECAST_API_KEY2=… TYPECAST_VOICE_ID2=…(없으면 1번 목소리)   (2번 계정)  … KEY3, KEY4 도 가능
ACCOUNTS = []
for n in ('', '2', '3', '4', '5'):
    k = CFG.get('TYPECAST_API_KEY' + n, '').strip()
    if k: ACCOUNTS.append({'key': k, 'voice': CFG.get('TYPECAST_VOICE_ID' + n, '').strip() or CFG.get('TYPECAST_VOICE_ID', '').strip(), 'name': '계정' + (n or '1')})
if not ACCOUNTS or not ACCOUNTS[0]['voice']:
    sys.exit('설정.txt 에 TYPECAST_API_KEY 와 TYPECAST_VOICE_ID 를 채워주세요.')
ACC = 0   # 지금 쓰는 계정 번호 (크레딧 소진·인증 오류 시 다음으로)
API_KEY, VOICE = ACCOUNTS[0]['key'], ACCOUNTS[0]['voice']

EMOTION = CFG.get('TTS_EMOTION', 'smart')      # smart | normal | happy | sad | angry | whisper | toneup | tonemid | tonedown
INTENSITY = float(CFG.get('TTS_INTENSITY', '1.0'))
TEMPO = float(CFG.get('TTS_TEMPO', '1.0'))      # 타입캐스트 자체 배속. 줄별 속도 조절은 build.py 가 하므로 보통 1.0
URL = 'https://api.typecast.ai/v1/text-to-speech'
def head(): return {'X-API-KEY': ACCOUNTS[ACC]['key'], 'Content-Type': 'application/json'}

FAILS = {}   # 계정 이름 → 왜 못 썼는지 (마지막에 한 줄로 정리해서 보여준다)
def next_account(reason):
    """다음 계정으로 전환. 더 없으면 False"""
    global ACC
    FAILS[ACCOUNTS[ACC]['name']] = reason
    if ACC + 1 >= len(ACCOUNTS):
        print(f'  {ACCOUNTS[ACC]["name"]} {reason} — 남은 계정 없음')
        print('  계정별 결과: ' + ' / '.join(f'{k}({ACCOUNTS[i]["key"][:6]}…): {v}' for i, (k, v) in enumerate(FAILS.items())))
        return False
    ACC += 1
    print(f'  {ACCOUNTS[ACC - 1]["name"]} {reason} → {ACCOUNTS[ACC]["name"]} 으로 전환')
    return True

def err_code(r):
    """타입캐스트 오류 응답의 error_code (예: UNUSUAL_ACTIVITY_DETECTED, INSUFFICIENT_CREDITS)"""
    try: return r.json().get('error_code') or r.json().get('message', '')[:60]
    except Exception: return r.text[:60]

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
        if rate > 8.5 or rate < 2.5: return False, f'길이 이상 {d:.1f}s/{syl}음절'
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

def synth(text, prev='', nxt='', out_path=None):
    out_path = out_path or os.path.join(VDIR, 'out.mp3')
    """한 줄 합성. 앞뒤 문장을 같이 보내면 억양이 자연스럽게 이어진다."""
    prompts = prompt_variants(prev, nxt)
    payload = {
        'model': 'ssfm-v30',
        'text': text,
        'voice_id': ACCOUNTS[ACC]['voice'],
        'prompt': prompts[0],
        'output': ({'audio_format': 'mp3', 'audio_tempo': TEMPO} if abs(TEMPO - 1.0) > 0.01 else {'audio_format': 'mp3'}),
    }
    pi = 0
    for attempt in range(6 + len(ACCOUNTS)):
        payload['voice_id'] = ACCOUNTS[ACC]['voice']
        r = requests.post(URL, headers=head(), json=payload, timeout=60)
        if r.status_code in (402, 401, 403) or (r.status_code == 200 and not r.content):
            # 크레딧 소진(402) / 키 오류(401·403) → 다음 계정으로
            why = ('크레딧 소진' if r.status_code == 402 else f'거부 {r.status_code}') + f' {err_code(r)}'
            if next_account(why): continue
            print(f'  실패 {r.status_code}: {r.text[:200]}')
            return False
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

def voice_dir():
    """편별 음성 폴더: build.py prep 이 work/current.txt 에 적은 콘티 이름 → work/voice_<이름>/"""
    try: key = io.open('work/current.txt', encoding='utf-8').read().strip()
    except Exception: key = ''
    d = os.path.join('work', 'voice_' + key) if key else os.path.join('work', 'voice')
    os.makedirs(d, exist_ok=True)
    return d
VDIR = voice_dir()

if __name__ == '__main__' and '--test' in sys.argv:
    ok = synth('야구자판기 음성 테스트예요. 삼성이 일위, 케이티가 영점오 게임 차예요.', out_path=os.path.join(VDIR, 'test.mp3'))
    print(f'OK → {VDIR}/test.mp3 재생해 보세요.' if ok else '실패')
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
    out = out or os.path.join(VDIR, f'{i:02d}.mp3')
    ok = synth_line(lines[i], prev, nxt, out, pause=0 if i == 0 else None)   # 첫 줄(후킹)은 한 호흡
    if ok:
        io.open(out.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(lines[i])   # 어떤 대사로 만든 음성인지 기록(대사 바뀌면 build 가 그 줄만 다시)
    return ok

def fetch_external(lines):
    """다른 TTS(힉스필드 등)로 만든 음성을 쓰는 경우: work/voice_<편>/external.json 에
       {"0": {"url": "...wav", "text": "대사"}, ...} 가 있으면 내려받아 NN.mp3 + NN.txt 로 저장한다(대사가 같은 줄만).
       그 뒤 아래 루프가 '재사용'으로 건너뛰므로 타입캐스트를 안 쓴다."""
    ext = os.path.join(VDIR, 'external.json')
    if not os.path.exists(ext): return 0
    try: data = json.load(io.open(ext, encoding='utf-8-sig'))
    except Exception as e: print(f'  external.json 읽기 실패: {e}'); return 0
    got = 0
    for i, line in enumerate(lines):
        item = data.get(str(i)) or {}
        url, text = item.get('url', ''), item.get('text', '')
        if not url or text.strip() != line.strip(): continue
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3'); txt = mp3.replace('.mp3', '.txt'); src = mp3.replace('.mp3', '.src')
        same_src = os.path.exists(src) and io.open(src, encoding='utf-8').read().strip() == url
        if same_src and os.path.exists(mp3) and os.path.exists(txt) and io.open(txt, encoding='utf-8').read().strip() == line.strip(): got += 1; continue
        try:
            r = requests.get(url, timeout=120); r.raise_for_status()
            raw = mp3 + '.dl'
            open(raw, 'wb').write(r.content)
            # 앞뒤 무음을 -38dB 기준으로 잘라낸다(외부 TTS 는 바닥 잡음이 높아 build 의 -40dB 트림에 안 걸리는 경우가 있음)
            af = 'silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse'
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-af', af, '-b:a', '192k', mp3], check=True)
            os.remove(raw)
            io.open(txt, 'w', encoding='utf-8').write(line)
            io.open(src, 'w', encoding='utf-8').write(url)   # 어느 주소에서 받은 음성인지 (주소가 바뀌면 다시 받는다)
            sj = mp3.replace('.mp3', '.segs.json')
            if os.path.exists(sj): os.remove(sj)   # 호흡 경계는 qa_voice(whisper)가 새로 잡는다
            got += 1; print(f'{i:02d} 외부 음성 받음')
        except Exception as e:
            print(f'{i:02d} 외부 음성 실패: {e}')
    if got: print(f'외부 음성 {got}줄 준비됨 (external.json)')
    return got

def _silences(path, thr='-32dB', min_d=0.35):
    """(시작, 끝) 무음 구간 목록 (ffmpeg silencedetect)"""
    r = subprocess.run(['ffmpeg', '-i', path, '-af', f'silencedetect=noise={thr}:d={min_d}', '-f', 'null', '-'], capture_output=True, text=True, errors='replace')
    out = []; st = None
    for ln in r.stderr.splitlines():
        m = re.search(r'silence_start: ([\d.]+)', ln)
        if m: st = float(m.group(1)); continue
        m = re.search(r'silence_end: ([\d.]+)', ln)
        if m and st is not None: out.append((st, float(m.group(1)))); st = None
    return out

def _dur(path):
    try: return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip())
    except Exception: return 0.0

def split_full(full_path, lines, keep_idx=None):
    """대본 전체를 한 번에 합성한 음성을 줄(장면) 단위로 자른다.
       1차: 줄 사이에 넣은 문단 쉼(긴 무음)을 찾아 자른다 — 무음 중 긴 것 N-1개를 시간순으로.
       검증: 잘린 조각 길이가 글자 수 비율과 크게 어긋나면 2차(faster-whisper 단어 시각으로 경계 추정)로 넘어간다.
       결과: work/voice_<편>/NN.mp3 + NN.txt (keep_idx 가 있으면 그 줄만 저장)"""
    N = len(lines); total = _dur(full_path)
    if N == 1: bounds = [(0.0, total)]
    else:
        sil = _silences(full_path)
        inner = [x for x in sil if x[0] > 0.2 and x[1] < total - 0.2]
        cuts = None
        if len(inner) >= N - 1:
            top = sorted(inner, key=lambda x: x[1] - x[0], reverse=True)[:N - 1]
            cuts = sorted((a + b) / 2 for a, b in top)
            bounds = [(0.0 if i == 0 else cuts[i - 1], total if i == N - 1 else cuts[i]) for i in range(N)]
            # 글자 수 비율로 검증 (각 조각이 기대 길이의 0.5~2배 안이면 OK)
            chars = [max(1, len(re.sub(r'[^가-힣]', '', l))) for l in lines]; sc = sum(chars)
            ok = all(0.5 <= ((b - a) / max(total * c / sc, 0.1)) <= 2.0 for (a, b), c in zip(bounds, chars))
            if not ok: print('  무음 기준 분할이 글자 수와 안 맞아 whisper 로 다시 잡습니다'); cuts = None
        if cuts is None:
            # 2차: whisper 단어 시각 → 누적 글자 비율로 경계
            from faster_whisper import WhisperModel
            m = WhisperModel(CFG.get('QA_WHISPER', 'small'), device='cpu', compute_type='int8')
            segs, _ = m.transcribe(full_path, language='ko', word_timestamps=True, beam_size=3, initial_prompt=' '.join(lines)[:200], vad_filter=False)
            words = [w for sg in segs for w in (sg.words or [])]
            if not words: raise SystemExit('통 음성 분할 실패: whisper 단어 시각을 못 얻음')
            wchars = [len(re.sub(r'[^가-힣]', '', w.word)) for w in words]; wsum = sum(wchars) or 1
            chars = [len(re.sub(r'[^가-힣]', '', l)) for l in lines]; sc = sum(chars) or 1
            targets = []; acc = 0
            for c in chars[:-1]: acc += c; targets.append(acc / sc)
            cuts = []; acc = 0; ti = 0
            for i, w in enumerate(words):
                acc += wchars[i]
                while ti < len(targets) and acc / wsum >= targets[ti]:
                    nxt = words[i + 1].start if i + 1 < len(words) else total
                    cuts.append((w.end + nxt) / 2); ti += 1
            while len(cuts) < N - 1: cuts.append(total)
            bounds = [(0.0 if i == 0 else cuts[i - 1], total if i == N - 1 else cuts[i]) for i in range(N)]
    af = 'silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse'
    for i, (a, b) in enumerate(bounds):
        if keep_idx is not None and i not in keep_idx: continue
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', full_path, '-af', af, '-b:a', '192k', mp3], check=True)
        io.open(mp3.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(lines[i])
        sj = mp3.replace('.mp3', '.segs.json')
        if os.path.exists(sj): os.remove(sj)
        print(f'{i:02d} 통 음성에서 잘라냄 {a:.2f}~{b:.2f}s')
    return N

def fetch_full(lines):
    """external.json 에 "full": {"url": ..., "lines": [...]} 가 있으면(대본 통째 합성) 내려받아 줄별로 자른다.
       lines 가 현재 대사와 같아야 하고, 같은 url 로 이미 잘라 둔 게 있으면 건너뛴다."""
    ext = os.path.join(VDIR, 'external.json')
    if not os.path.exists(ext): return 0
    try: data = json.load(io.open(ext, encoding='utf-8-sig'))
    except Exception: return 0
    full = data.get('full') or {}
    url = full.get('url', '')
    if not url: return 0
    if [t.strip() for t in full.get('lines', [])] != [l.strip() for l in lines]:
        print('  external.json 의 full.lines 가 지금 대사와 달라 통 음성을 쓰지 않습니다'); return 0
    src = os.path.join(VDIR, 'full.src')
    if os.path.exists(src) and io.open(src, encoding='utf-8').read().strip() == url and all(os.path.exists(os.path.join(VDIR, f'{i:02d}.mp3')) for i in range(len(lines))):
        return len(lines)
    raw = os.path.join(VDIR, 'full.dl')
    r = requests.get(url, timeout=300); r.raise_for_status(); open(raw, 'wb').write(r.content)
    wav = os.path.join(VDIR, 'full.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', raw, '-ac', '1', '-ar', '24000', wav], check=True)
    n = split_full(wav, lines)
    io.open(src, 'w', encoding='utf-8').write(url)
    print(f'통 음성 {n}줄로 분할 완료')
    return n

if __name__ == '__main__':
    lines = load_lines()
    try: fetch_full(lines)
    except SystemExit: raise
    except Exception as e: print(f'  통 음성 처리 실패(줄별 external 또는 TTS 로 진행): {e}')
    fetch_external(lines)
    only = None
    for a in sys.argv:
        if a.startswith('--only='): only = {int(x) for x in a.split('=',1)[1].replace(',', ' ').split()}
    print(f'{len(lines)}줄 합성 시작' + (f' (줄 {sorted(only)} 만)' if only else ''))
    fail = 0
    reuse = 0
    for i, line in enumerate(lines):
        if only is not None and i not in only: continue
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3'); txt = mp3.replace('.mp3', '.txt'); segs = mp3.replace('.mp3', '.segs.json')
        if '--fresh' not in sys.argv and only is None and os.path.exists(mp3) and os.path.exists(txt) \
                and io.open(txt, encoding='utf-8').read().strip() == line.strip():
            reuse += 1; print(f'{i:02d} 재사용 {line}'); continue   # 같은 대사로 이미 만든 음성이 있으면 크레딧 안 씀 (--fresh 면 전부 새로)
        ok = synth_index(lines, i)
        print(f'{i:02d} {"OK " if ok else "XX "} {line}')
        fail += (not ok)
        time.sleep(0.3)
    if fail:
        if FAILS: print('계정별 결과: ' + ' / '.join(f'{k}: {v}' for k, v in FAILS.items()))
        sys.exit(f'{fail}줄 실패' + (' — 모든 타입캐스트 계정이 거부됨(UNUSUAL_ACTIVITY 는 같은 PC 에서 무료 계정 여러 개를 쓴다고 본 것 → 계정 하나에 크레딧 충전이 확실한 해결)' if FAILS and all('UNUSUAL' in v for v in FAILS.values()) else ''))
    print('완료' + (f' (기존 음성 {reuse}줄 재사용)' if reuse else ''))
