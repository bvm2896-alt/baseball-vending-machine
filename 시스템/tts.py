# -*- coding: utf-8 -*-
"""
타입캐스트 API로 나레이션 음성 생성
  python tts.py --test          → voice/test.mp3 한 줄 테스트
  python tts.py                 → work/narration.txt 각 줄 → work/voice/00.mp3, 01.mp3 ...
설정은 같은 폴더의 설정.txt 에서 읽는다 (TYPECAST_API_KEY, TYPECAST_VOICE_ID)
"""
import shutil, os, sys, json, time, subprocess, io
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

def open_cfg(path='설정.txt'):
    """설정.txt 열기 — 메모장이 ANSI(cp949)로 저장해도 읽히게 utf-8 → cp949 순서로 시도 (build.py 와 같음, 9/15 회사 PC 사고)"""
    for enc in ('utf-8-sig', 'cp949', 'euc-kr'):
        try:
            f = io.open(path, encoding=enc); f.read(); f.seek(0); return f
        except UnicodeDecodeError:
            try: f.close()
            except Exception: pass
    return io.open(path, encoding='utf-8-sig', errors='replace')

def load_cfg():
    cfg = {}
    with open_cfg('설정.txt') as f:
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
NO_API = not ACCOUNTS or not ACCOUNTS[0]['voice']   # 9/15: API 키가 없어도 웹에서 받은 zip 은 자를 수 있어야 한다(회사 PC 는 키 없음) → 여기서 멈추지 않는다
if NO_API: ACCOUNTS = [{'key': '', 'voice': '', 'name': '없음'}]
ACC = 0   # 지금 쓰는 계정 번호 (크레딧 소진·인증 오류 시 다음으로)
API_KEY, VOICE = ACCOUNTS[0]['key'], ACCOUNTS[0]['voice']

EMOTION = CFG.get('TTS_EMOTION', 'smart')      # smart | normal | happy | sad | angry | whisper | toneup | tonemid | tonedown
INTENSITY = float(CFG.get('TTS_INTENSITY', '1.0'))
TEMPO = float(CFG.get('TTS_TEMPO', '1.0'))      # 타입캐스트 자체 배속. 줄별 속도 조절은 build.py 가 하므로 보통 1.0
URL = 'https://api.typecast.ai/v1/text-to-speech'
try:   # 9/26: 콘티 ttsTempo(build prep 이 work\tts_tempo.txt 에 적음)가 설정.txt TTS_TEMPO 보다 우선
    _tt = io.open(os.path.join(os.environ.get('KBO_WORK', 'work'), 'tts_tempo.txt'), encoding='utf-8').read().strip()
    if _tt: TEMPO = float(_tt)
except Exception: pass
def head(): return {'X-API-KEY': ACCOUNTS[ACC]['key'], 'Content-Type': 'application/json'}

FAILS = {}   # 계정 이름 → 왜 못 썼는지 (마지막에 한 줄로 정리해서 보여준다)
# 9/27 사고 뒤: 계정 자동 전환 금지. 1번 계정이 떨어지면 멈추고 사람에게 묻는다.
#   KBO_ASK=1(롱폼만들기처럼 사람이 콘솔을 보고 있을 때) → 그 자리에서 y/n 을 묻는다
#   그 외(지금실행 안에서 run_daily 가 부를 때) → 종료 코드 3 + 'ASK_SWITCH' 표시 → run_daily 가 묻고 --switch-ok 로 다시 부른다
#   예약 실행(사람 없음)은 묻지 못하므로 그냥 멈춘다
SWITCH_OK = '--switch-ok' in sys.argv
NEED_ASK = None   # 사람에게 물어야 해서 멈춘 이유 (main 이 종료 코드 3 으로 알린다)
def asking(): return os.environ.get('KBO_ASK') == '1' and sys.stdin is not None and sys.stdin.isatty()
def next_account(reason):
    """다음 계정으로 전환. 더 없거나 사람이 허락 안 하면 False"""
    global ACC, SWITCH_OK, NEED_ASK
    FAILS[ACCOUNTS[ACC]['name']] = reason
    if ACC + 1 >= len(ACCOUNTS):
        print(f'  {ACCOUNTS[ACC]["name"]} {reason} — 남은 계정 없음')
        print('  계정별 결과: ' + ' / '.join(f'{k}: {v}' for k, v in FAILS.items()))
        return False
    if not SWITCH_OK:
        nxt = ACCOUNTS[ACC + 1]['name']
        if asking():
            a = input(f'  {ACCOUNTS[ACC]["name"]} {reason} — {nxt} 크레딧을 써서 계속할까요? (y = 계속, Enter = 멈춤) ').strip().lower()
            if a in ('y', 'ㅛ'): SWITCH_OK = True
        if not SWITCH_OK:
            NEED_ASK = f'SWITCH {ACCOUNTS[ACC]["name"]} {reason} → {nxt}'
            print(f'  {ACCOUNTS[ACC]["name"]} {reason} — {nxt} 로 자동으로 넘어가지 않고 멈춤')
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
        if rate > 8.5 * max(1.0, TEMPO) or rate < 2.5: return False, f'길이 이상 {d:.1f}s/{syl}음절'   # 9/26: 타입캐스트 배속만큼 기준도 올림
        return True, ''
    except Exception as e:
        return True, ''

def prompt_variants(prev, nxt):
    """설정.txt 의 TTS_EMOTION 에 따라 prompt 후보를 순서대로 (400 이면 다음 후보로)"""
    if EMOTION == 'smart':
        return [{'emotion_type': 'smart', 'previous_text': prev, 'next_text': nxt}]
    # 9/26: 설정한 감정이 거부돼도 스마트 이모션으로 몰래 바꾸지 않는다(사용자가 스마트를 끔) → 두 형식 다 거부면 실패
    return [{'emotion_type': 'preset', 'emotion_preset': EMOTION, 'emotion_intensity': INTENSITY},
            {'emotion_preset': EMOTION, 'emotion_intensity': INTENSITY}]

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
                # 9/26: 배속 없이 1.0배로 몰래 만들면 영상이 느려진다 → 멈추고 알린다
                print(f'  실패 400: 타입캐스트가 배속 {TEMPO} 옵션을 거부했어요 — 1.0배로 대신 만들지 않음: {r.text[:200]}'); return False
            if 'output' in payload:
                payload.pop('output'); continue
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 + attempt * 2)
            continue
        print(f'  실패 {r.status_code}: {r.text[:300]}')
        return False
    return False

WORK = os.environ.get('KBO_WORK', 'work')   # 시리즈별 작업 폴더(current.txt·narration.txt). 음성 폴더는 늘 work\voice_<편>

def voice_dir():
    """편별 음성 폴더: build.py prep 이 work/current.txt 에 적은 콘티 이름 → work/voice_<이름>/"""
    try: key = io.open(os.path.join(WORK, 'current.txt'), encoding='utf-8').read().strip()
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
    return [l.strip() for l in io.open(os.path.join(WORK, 'narration.txt'), encoding='utf-8-sig') if l.strip()]

# 9/30 사용자 지시: "마지막 구독멘트는 앞으로 계속 지금 생성한걸로" (9/30 KT편 스마트 이모션 구독 멘트)
#   대사가 시스템\고정음성\구독멘트.txt 와 같으면 API·웹 zip 과 상관없이 고정음성\구독멘트.mp3 를 NN.mp3 로 복사하고 NN.keep 를 둔다.
#   → 다시 합성하지 않음(크레딧 안 씀), qa_voice 도 다시 만들지 않음. 파일을 바꾸려면 고정음성 폴더의 두 파일만 바꾸면 된다.
PIN_DIR = os.path.join(HERE, '고정음성')
def _pin_norm(t): return re.sub(r'[\s/.,!?~·]', '', t or '')
def pinned_idx(lines):
    src = os.path.join(PIN_DIR, '구독멘트.mp3')
    try: key = _pin_norm(io.open(os.path.join(PIN_DIR, '구독멘트.txt'), encoding='utf-8-sig').read())
    except Exception: return []
    if not key or not os.path.exists(src): return []
    return [i for i, l in enumerate(lines) if _pin_norm(l) == key]
def pin_lines(lines, quiet=False):
    src = os.path.join(PIN_DIR, '구독멘트.mp3'); idx = pinned_idx(lines)
    for i in idx:
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3')
        same = os.path.exists(mp3) and os.path.getsize(mp3) == os.path.getsize(src) and open(mp3, 'rb').read() == open(src, 'rb').read()
        if not same:
            shutil.copyfile(src, mp3)
            for suf in ('.segs.json', '.src'):   # 다른 음성으로 잡힌 자막 경계는 버린다
                if os.path.exists(mp3.replace('.mp3', suf)): os.remove(mp3.replace('.mp3', suf))
        io.open(mp3.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(lines[i])
        io.open(mp3.replace('.mp3', '.keep'), 'w', encoding='utf-8').write('고정음성\\구독멘트.mp3')
    if idx and not quiet: print(f'구독 멘트 고정 음성 사용: 줄 {idx} (고정음성\\구독멘트.mp3, 합성 안 함)')
    return set(idx)
PAUSE = float(CFG.get('TTS_PAUSE', '0.12'))   # 대사 안의 " / " 표시 자리에서 쉬는 시간(초). 구간 자체의 앞뒤 무음은 잘라내므로 아주 짧게

def tts_text(segs, is_last_q=False):
    """TTS 에 넣을 문장: 호흡 구간(' / ')은 쉼표로, 끝은 마침표/물음표로 → 한 사람이 쭉 읽는 자연스러운 억양.
    (쉼표·마침표 금지 규칙은 화면 자막 얘기고, TTS 입력엔 넣어야 억양이 자연스럽다)"""
    # 9/28: 구간 끝에 물음표가 있으면(질문) 쉼표를 붙이지 않는다 → '보세요?, 댓글로' 대신 '보세요? 댓글로' (끝을 올려 읽게)
    # 9/30 사용자 지적(순위5 "확정할까요, 아니면" → '요'가 뚝 끊김): 물음표 없이 끝난 질문 구간(-까요·-나요)에도 물음표를 붙여 끝을 올려 다 읽게 한다
    segs = [sg + '?' if re.search(r'(까요|나요)$', sg) else sg for sg in segs]
    # 10/1 사용자 지적(롱폼④ 목차 "키움은 선수를 팔고도 강했다, 한화는 …" → 쉼표라 '강했다한화는' 으로 이어 읽고,
    #   seg_bounds 가 '했'과 '다' 사이 파열음 틈(0.17초)을 호흡 자리로 잡아 "강했 / 다한화는" 이 됨):
    #   줄 가운데 구간이 '-었다·-했다·-겠다' 같은 서술형 '-다'로 끝나면 쉼표 대신 마침표 → 타입캐스트가 확실히 끊어 읽는다.
    #   ('때마다'·'바다' 같은 말은 받침 있는 어미 앞 글자만 보므로 걸리지 않는다)
    segs = [sg + '.' if k < len(segs) - 1 and re.search(r'[았었였했겠꿨웠쳤났갔왔졌렸봤줬됐섰켰혔렀]다$', sg) else sg for k, sg in enumerate(segs)]
    t = ''
    for k, sg in enumerate(segs):
        t += sg if k == 0 else ((' ' if segs[k - 1].endswith(('?', '!', '.')) else ', ') + sg)
    if not t.endswith(('?', '!', '.')): t += '.'
    return t

def probe_silences(path, thr='-35dB', mind=0.06):
    r = subprocess.run(['ffmpeg', '-i', path, '-af', f'silencedetect=n={thr}:d={mind}', '-f', 'null', '-'], capture_output=True, text=True)
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip() or 0)
    if len(en) < len(st): en.append(d)
    return d, list(zip(st, en))

def _syl(t):
    return len(re.findall(r'[가-힣]', t)) + 1.3 * len(re.findall(r'[0-9A-Za-z]', t)) or 1

def seg_bounds(path, segs, NONE=0.08, GAPB=0.5):
    """한 번에 합성한 음성 안에서 각 호흡 구간(' / ')이 시작하는 시각(초)과 그 자리의 실제 쉼(무음 구간).
    9/28 롱폼③ 사고(자막이 1초 넘게 먼저/늦게 넘어가고, 호흡 쉼이 단어 가운데 끼어 '말이 끊김') 뒤 새 방식:
      - 타입캐스트는 쉼표 자리에서 안 쉬기도 하고, 쉼표 아닌 곳('셋째,' '경찰야구단이 ..')에서 쉬기도 한다.
        그래서 '쉼 개수 = 경계 수면 순서대로 쓴다'는 옛 규칙이 경계를 통째로 한 칸씩 밀었다.
      - 이제는 쉼을 뺀 '말하는 시간'으로 재서, 경계마다 (쉼 하나 | 쉼 없음)을 배정했을 때
        구간별 말 속도(초/음절)가 가장 고르게 되는 배정을 고른다(동적 계획법). 긴 쉼은 경계일 가능성이 높아 가산점,
        음절당 0.08~0.175초를 벗어나는 구간은 벌점. 쉼 없는 경계는 앞뒤 확정 경계 사이를 글자 수로 나눈다.
    반환: [(시작초, (무음시작,무음끝) 또는 None)] — None 자리엔 호흡 쉼을 끼우지 않는다(단어 가운데 끼면 말이 끊긴다)"""
    import functools, math
    d, sil = probe_silences(path, thr='-36dB', mind=0.04)
    lead = sil[0][1] if sil and sil[0][0] < 0.02 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] >= d - 0.03 else d
    inner = [(a, b) for a, b in sil if a > lead + 0.05 and b < tail - 0.05]
    cs, acc, prev = [], 0.0, lead
    for a, b in inner:
        acc += a - prev; cs.append(acc); prev = b
    total = max(0.2, acc + (tail - prev))
    need = len(segs) - 1
    raw = [_syl(x) for x in segs]
    w = [r + 1.0 for r in raw]; W = sum(w); ov = total / W   # +1: 구간 끝 음절은 늘어진다
    def pen(sp_, k0, k1):
        rr = sp_ / sum(raw[k0:k1])
        return 0.0 if 0.08 <= rr <= 0.175 else 1.0
    @functools.lru_cache(None)
    def best(k, i, s0):
        ws = sum(w[k + 1:]); r = (total - s0) / ws
        opts = [(ws / W * abs(math.log(max(r, 1e-3) / ov)) + NONE * (need - k - 1) + pen(total - s0, k + 1, need + 1), ())]
        for k2 in range(k + 1, need):
            ws = sum(w[k + 1:k2 + 1])
            for j in range(i, len(inner)):
                s1 = cs[j]
                if s1 <= s0: continue
                g = inner[j][1] - inner[j][0]
                c = ws / W * abs(math.log(((s1 - s0) / ws) / ov)) + NONE * (k2 - k - 1) - GAPB * min(g, 0.4) + pen(s1 - s0, k + 1, k2 + 1)
                sub, path_ = best(k2, j + 1, s1)
                opts.append((c + sub, ((k2, j),) + path_))
        return min(opts, key=lambda z: z[0])
    pick = [None] * need
    for k2, j in best(-1, 0, 0.0)[1]: pick[k2] = j
    def s2t(s):
        acc, prev = 0.0, lead
        for a, b in inner:
            if acc + (a - prev) >= s: return prev + (s - acc)
            acc += a - prev; prev = b
        return prev + (s - acc)
    anc = {-1: 0.0}
    for k, p in enumerate(pick):
        if p is not None: anc[k] = cs[p]
    anc[need] = total
    out, last = [(0.0, None)], 0.0
    for k, p in enumerate(pick):
        if p is not None: pos, iv = inner[p][1], inner[p]
        else:
            lo = max(j for j in anc if j < k); hi = min(j for j in anc if j > k)
            pos = s2t(anc[lo] + (anc[hi] - anc[lo]) * sum(w[lo + 1:k + 1]) / sum(w[lo + 1:hi + 1])); iv = None
        pos = max(pos, last + 0.15); last = pos
        out.append((round(pos, 3), iv))
    return out

BREATH = float(CFG.get('TTS_BREATH', '0.1'))   # 긴 대사의 호흡 자리(' / ')에 살짝 끼워 넣는 쉼(초). 실제 쉼이 감지된 자리에만 넣는다

PAUSE_MAX = float(CFG.get('TTS_PAUSE_MAX', '0.9'))   # 10/4 사용자("그 중심에는 손주영이 있어요 하고 한참 가만히 있다가 말해, 텀 줄여"): 한 줄 안의 쉼이 이보다 길면 PAUSE_KEEP 으로 줄인다
PAUSE_KEEP = float(CFG.get('TTS_PAUSE_KEEP', '0.5'))
def trim_long_pauses(path, maxp=None, keep=None):
    """타입캐스트가 쉼표·마침표 뒤에 1초 넘게 멈추는 줄: 줄 안의 무음이 maxp 초를 넘으면 keep 초만 남기고 잘라 낸다(앞뒤 4ms 페이드). 자른 구간 수를 돌려준다.
    seg_bounds 보다 먼저 불러야 경계가 잘린 음성 기준으로 잡힌다."""
    import numpy as np
    maxp = PAUSE_MAX if maxp is None else maxp; keep = PAUSE_KEEP if keep is None else keep
    if maxp <= 0 or keep >= maxp: return 0
    d, sil = probe_silences(path, thr='-35dB', mind=maxp)
    inner = [(a, b) for a, b in sil if a > 0.1 and b < d - 0.1]
    if not inner: return 0
    sr_ = 44100
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(sr_), '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).copy()
    if not len(x): return 0
    fade = int(sr_ * 0.004); out, prev = [], 0
    for a, b in inner:
        cut0 = int((a + keep / 2) * sr_); cut1 = int((b - keep / 2) * sr_)   # 쉼 가운데를 잘라 양쪽에 keep/2 씩 남긴다
        seg = x[prev:cut0].copy()
        if len(seg) > fade: seg[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)
        out.append(seg); prev = cut1
    tailx = x[prev:].copy()
    if len(tailx) > fade: tailx[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)
    y = np.concatenate(out + [tailx])
    tmp = path + '.trim.mp3'
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(sr_), '-ac', '1', '-i', '-', '-b:a', '192k', tmp], input=y.tobytes(), capture_output=True)
    if r.returncode != 0 or not os.path.exists(tmp): return 0
    os.replace(tmp, path)
    print(f'  긴 쉼 {len(inner)}곳 줄임({os.path.basename(path)}: ' + ', '.join(f'{b - a:.2f}s→{keep:.2f}s' for a, b in inner) + ')')
    return len(inner)

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
    try: trim_long_pauses(out)   # 10/4: 줄 안의 1초 가까운 멈춤을 0.5초로
    except Exception as e: print('  긴 쉼 줄이기 실패:', e)
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

def mark_breaths(mp3, line, first=False):
    """웹(zip/통 음성)에서 받은 한 줄 음성에도 API 음성과 똑같이: ' / ' 호흡 자리의 실제 쉼을 찾아 TTS_BREATH 만큼 쉼을 더 끼우고 NN.segs.json 을 쓴다.
    첫 줄(후킹)은 한 호흡이라 쉼을 안 끼운다."""
    segs = [x.strip() for x in line.split('/') if x.strip()]
    sj = mp3.replace('.mp3', '.segs.json')
    if len(segs) <= 1: return
    try:
        trim_long_pauses(mp3)   # 10/4
        bounds = seg_bounds(mp3, segs)
        b = [x for x, _ in bounds] if first else insert_breaths(mp3, bounds)
        durs = [b[k + 1] - b[k] for k in range(len(b) - 1)] + [0.0]
        json.dump({'durs': durs, 'pause': 0.0, 'bounds': b, 'breaths': 0 if first else sum(1 for _, iv in bounds[1:] if iv)}, open(sj, 'w'))
    except Exception as e:
        print(f'  {os.path.basename(mp3)} 구간 추정 실패(자막은 한 덩어리로):', e)
        try: os.remove(sj)
        except Exception: pass

def synth_index(lines, i, out=None):
    """i번째 줄 합성(앞뒤 문맥 포함). qa_voice.py 가 다시 만들 때도 이걸 쓴다"""
    prev = lines[i-1] if i > 0 else ''
    nxt = lines[i+1] if i+1 < len(lines) else ''
    out = out or os.path.join(VDIR, f'{i:02d}.mp3')
    ok = synth_line(lines[i], prev, nxt, out, pause=0 if i == 0 else None)   # 첫 줄(후킹)은 한 호흡
    if ok:
        io.open(out.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(lines[i])   # 어떤 대사로 만든 음성인지 기록(대사 바뀌면 build 가 그 줄만 다시)
    return ok

# ---------- 9/26: 한 편 통째 합성 (콘티 "ttsWhole": true) ----------
# 줄마다 따로 만들면 1줄·2줄 억양이 따로 논다 → 구독 멘트(NN.keep) 뺀 줄 전부를 API 한 번으로 이어 읽게 하고 줄 경계에서 자른다.
def whole_mode():
    try: return io.open(os.path.join(WORK, 'tts_whole.txt'), encoding='utf-8').read().strip() == '1'
    except Exception: return False

def whole_bounds(path, texts):
    """통 음성에서 줄 경계 N-1 개 → (무음 구간 목록, 전체 길이, 방법)
       1) 줄 사이(대본의 빈 줄)에서 확실히 길게 쉬었으면: 가장 긴 무음 N-1 개 (N번째보다 뚜렷이 길 때만)
       2) 아니면 whisper 단어 시각으로 줄 끝 위치를 잡고 가장 가까운 무음에 붙인다(PC 에 faster-whisper 가 있을 때)
       3) 둘 다 안 되면 글자 수 위치 + 긴 무음 우선(정확도 낮음 → 경고)"""
    d, sil = probe_silences(path, thr='-36dB', mind=0.06)
    lead = sil[0][1] if sil and sil[0][0] < 0.02 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] >= d - 0.03 else d
    inner = [(a, b) for a, b in sil if a > lead + 0.05 and b < tail - 0.05]
    N = len(texts); need = N - 1
    if need == 0: return [], d, '한 줄'
    if len(inner) < need: return None, d, '무음 부족'
    def norm(t): return re.sub(r'[^가-힣A-Za-z0-9]', '', t)
    chars = [max(1, len(norm(t))) for t in texts]; sc = sum(chars)
    def plausible(cuts):
        b = [lead] + [(x + y) / 2 for x, y in cuts] + [tail]
        return all(0.6 <= (b[k + 1] - b[k]) / max((tail - lead) * chars[k] / sc, 0.1) <= 1.7 for k in range(N))
    # 1) 뚜렷한 문단 쉼
    by_len = sorted(inner, key=lambda iv: iv[1] - iv[0], reverse=True)
    top = sorted(by_len[:need])
    nth = (by_len[need][1] - by_len[need][0]) if len(by_len) > need else 0.0
    shortest_top = min(y - x for x, y in top)
    if shortest_top >= 1.35 * nth and plausible(top): return top, d, f'문단 쉼(최소 {shortest_top:.2f}s > 다음 {nth:.2f}s)'
    # 2) whisper
    try:
        from faster_whisper import WhisperModel
        m = WhisperModel(CFG.get('QA_WHISPER', 'small'), device='cpu', compute_type='int8')
        segs, _ = m.transcribe(path, language='ko', word_timestamps=True, beam_size=3, vad_filter=False,
                               initial_prompt=' '.join(norm(t)[:40] for t in texts)[:200])
        words = [w for sg in segs for w in (sg.words or [])]
        if not words: raise RuntimeError('단어 시각 없음')
        wl = [max(1, len(norm(w.word))) for w in words]; ws = sum(wl)
        cuts, acc, k, used = [], 0, 0, set()
        targets = []; t_ = 0
        for c in chars[:-1]: t_ += c; targets.append(t_ / sc)
        est = []
        for i, w in enumerate(words):
            acc += wl[i]
            while k < need and acc / ws >= targets[k] - 1e-9:
                nxt = words[i + 1].start if i + 1 < len(words) else tail
                est.append((w.end + nxt) / 2); k += 1
        while len(est) < need: est.append(tail)
        prev = lead
        for e in est:
            near = [iv for iv in inner if iv[0] > prev + 0.2 and abs((iv[0] + iv[1]) / 2 - e) <= 0.7]
            iv = max(near, key=lambda v: (v[1] - v[0]) - 0.3 * abs((v[0] + v[1]) / 2 - e)) if near else (e, e)
            cuts.append(iv); prev = (iv[0] + iv[1]) / 2
        return cuts, d, 'whisper'
    except Exception as ex:
        print(f'  whisper 로 줄 경계 못 잡음({ex})')
    # 3) 글자 수 위치 + 긴 무음 우선
    exp = []; acc = 0
    for k in range(need): acc += chars[k]; exp.append(lead + (tail - lead) * acc / sc)
    per_line = (tail - lead) / N
    cuts, prev = [], lead
    for k, e in enumerate(exp):
        near = [iv for iv in inner if iv[0] > prev + 0.2 and abs((iv[0] + iv[1]) / 2 - e) <= 0.6 * per_line]
        iv = max(near, key=lambda v: (v[1] - v[0]) - 0.3 * abs((v[0] + v[1]) / 2 - e) / per_line) if near else (e, e)
        cuts.append(iv); prev = (iv[0] + iv[1]) / 2
    return cuts, d, '글자 수 추정(부정확할 수 있음 — 영상에서 자막·장면 타이밍 확인)'

def whole_split(full, idx, lines):
    """통 음성 full 을 idx 줄들로 잘라 NN.mp3 + NN.txt + 호흡 경계(segs.json)"""
    texts = [lines[i] for i in idx]
    cuts, d, how = whole_bounds(full, texts)
    if cuts is None: raise RuntimeError(f'통 음성을 줄로 못 자름({how})')
    print(f'  줄 경계 찾기: {how}')
    io.open(os.path.join(VDIR, 'whole_split.txt'), 'w', encoding='utf-8').write(how + '\n' + ' '.join(f'{(a + c) / 2:.2f}' for a, c in cuts))
    b = [0.0] + [round((a + c) / 2, 3) for a, c in cuts] + [d]
    af = 'silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse'
    for k, i in enumerate(idx):
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{b[k]:.3f}', '-to', f'{b[k + 1]:.3f}', '-i', full, '-af', af, '-b:a', '192k', mp3], check=True)
        io.open(mp3.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(lines[i])
        for suf in ('.segs.json', '.src'):
            if os.path.exists(mp3.replace('.mp3', suf)): os.remove(mp3.replace('.mp3', suf))
        mark_breaths(mp3, lines[i], first=(i == 0))
        print(f'{i:02d} 통 음성에서 잘라냄 {b[k]:.2f}~{b[k + 1]:.2f}s')
    return len(idx)

def synth_whole(lines):
    """구독 멘트(NN.keep) 뺀 줄을 한 번에 합성해 자른다. 이미 이번 기준(fresh.flag 이후)으로 다 만들어져 있으면 건너뜀"""
    idx = [i for i in range(len(lines)) if not os.path.exists(os.path.join(VDIR, f'{i:02d}.keep'))]
    ff = os.path.join(VDIR, 'fresh.flag')
    def fresh(i):
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3'); txt = mp3.replace('.mp3', '.txt')
        if not (os.path.exists(mp3) and os.path.exists(txt)): return False
        if io.open(txt, encoding='utf-8').read().strip() != lines[i].strip(): return False
        return not (os.path.exists(ff) and os.path.getmtime(txt) < os.path.getmtime(ff))
    if all(fresh(i) for i in idx):
        print('통 합성: 이미 만든 음성 재사용'); return True
    text = '\n\n'.join(tts_text([x.strip() for x in lines[i].split('/') if x.strip()]) for i in idx)
    full = os.path.join(VDIR, 'whole.mp3')
    print(f'통 합성: {len(idx)}줄 {len(text)}자 한 번에 (배속 {TEMPO}, 감정 {EMOTION})')
    if not synth(text, out_path=full): return False
    io.open(os.path.join(VDIR, 'whole.txt'), 'w', encoding='utf-8').write(text)
    whole_split(full, idx, lines)
    return True

def drop_external(lines):
    """external.json 에 {"disabled": true} 가 있으면 외부(힉스필드)에서 받았던 음성(NN.src / full.src 표시가 있는 것)을 지워서
       타입캐스트로 다시 만들게 한다. 타입캐스트로 만든 음성은 그대로 둔다."""
    ext = os.path.join(VDIR, 'external.json')
    if not os.path.exists(ext): return False
    try: data = json.load(io.open(ext, encoding='utf-8-sig'))
    except Exception: return False
    if not data.get('disabled'): return False
    n = 0
    fsrc = os.path.join(VDIR, 'full.src')
    full_is_url = os.path.exists(fsrc) and io.open(fsrc, encoding='utf-8').read().strip().lower().startswith('http')   # 사람이 넣은 파일(경로|시각)은 남긴다
    for i in range(len(lines)):
        base = os.path.join(VDIR, f'{i:02d}')
        if os.path.exists(base + '.src') or full_is_url:
            for suf in ('.mp3', '.txt', '.src', '.segs.json'):
                try: os.remove(base + suf); n += 1
                except FileNotFoundError: pass
    if full_is_url:
        for f in ('full.src', 'full.wav', 'full.dl'):
            try: os.remove(os.path.join(VDIR, f))
            except FileNotFoundError: pass
    if n: print(f'외부 음성 {n}개 파일 정리 — 타입캐스트로 다시 만듭니다')
    return True

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
            try:
                # 2차: whisper 단어 시각 → 누적 글자 비율로 경계
                from faster_whisper import WhisperModel
                m = WhisperModel(CFG.get('QA_WHISPER', 'small'), device='cpu', compute_type='int8')
                segs, _ = m.transcribe(full_path, language='ko', word_timestamps=True, beam_size=3, initial_prompt=' '.join(lines)[:200], vad_filter=False)
                words = [w for sg in segs for w in (sg.words or [])]
                if not words: raise RuntimeError('whisper 단어 시각을 못 얻음')
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
            except Exception as e:
                # 3차(안전망): whisper 를 못 쓰면 글자 수 비율로 시간을 나눈다(대략적이지만 영상은 만들어짐)
                print(f'  whisper 분할 실패({e}) → 글자 수 비율로 대략 분할합니다')
                chars = [max(1, len(re.sub(r'[^가-힣]', '', l))) for l in lines]; sc = sum(chars) or 1
                cuts = []; acc = 0
                for c in chars[:-1]: acc += c; cuts.append(total * acc / sc)
            bounds = [(0.0 if i == 0 else cuts[i - 1], total if i == N - 1 else cuts[i]) for i in range(N)]
    af = 'silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse'
    for i, (a, b) in enumerate(bounds):
        if keep_idx is not None and i not in keep_idx: continue
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{a:.3f}', '-to', f'{b:.3f}', '-i', full_path, '-af', af, '-b:a', '192k', mp3], check=True)
        io.open(mp3.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(lines[i])
        for suf in ('.segs.json', '.src'):
            if os.path.exists(mp3.replace('.mp3', suf)): os.remove(mp3.replace('.mp3', suf))
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

def drop_paths():
    r"""사람이 타입캐스트 웹에서 받아 넣는 통 음성 파일 후보: <야구자판기>\<시리즈>\음성\<콘티이름>.mp3|wav|m4a, 또는 work\voice_<편>\full.mp3"""
    key = os.path.basename(VDIR).replace('voice_', '')
    slot = key.rsplit('_', 1)[-1] if '_' in key else ''
    # 9/18: 롱폼(<콘티이름>_롱폼)이 빠져 있어 야구순위\음성\ 을 뒤지다 zip 을 못 찾았다 → 슬롯 이름 그대로 시리즈를 고른다
    series = ('야구이슈' if slot.startswith('이슈') or slot == '2' else '야구분석' if slot.startswith('분석')
              else '야구롱폼' if slot.startswith('롱폼') else '야구순위')
    base = os.path.join(HERE, '..', series, '음성')
    out = [os.path.join(base, key + ext) for ext in ('.zip', '.mp3', '.wav', '.m4a')]
    out += [os.path.join(VDIR, 'full' + ext) for ext in ('.zip', '.mp3', '.wav', '.m4a')]
    return out

def _natkey(name):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', name)]

def split_zip(zip_path, lines):
    """타입캐스트 '문장 별로 나누기' zip: 파일 수가 줄 수와 같으면 이름 순서대로 NN.mp3 로. 다르면 이어 붙여 통 음성으로 취급해 무음으로 자른다."""
    import zipfile, tempfile
    tmp = os.path.join(VDIR, 'zip_tmp'); shutil_rm(tmp); os.makedirs(tmp, exist_ok=True)
    # zip 안 파일 이름(한글·긴 이름·인코딩 플래그 없는 zip)은 윈도우에서 풀다 실패할 수 있어, 순서만 취해 짧은 영문 이름으로 꺼낸다(9/15)
    with zipfile.ZipFile(zip_path) as z:
        infos = [zi for zi in z.infolist() if zi.filename.lower().endswith(('.mp3', '.wav', '.m4a')) and not zi.filename.endswith('/') and zi.file_size > 0]
        infos.sort(key=lambda zi: _natkey(os.path.basename(zi.filename)))
        files = []
        for k, zi in enumerate(infos):
            dst = os.path.join(tmp, f'src{k:02d}' + os.path.splitext(zi.filename)[1].lower())
            with z.open(zi) as fi, open(dst, 'wb') as fo: shutil.copyfileobj(fi, fo)
            files.append(dst)
    af = 'silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-38dB:start_silence=0.05,areverse'
    _pin = pinned_idx(lines)
    if _pin and len(files) == len(lines) - len(_pin):   # 9/30: 대본에서 구독 멘트를 뺀 zip → 나머지 줄에 순서대로
        _free = [i for i in range(len(lines)) if i not in _pin]
        for i, f in zip(_free, files):
            mp3 = os.path.join(VDIR, f'{i:02d}.mp3')
            r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f, '-af', af, '-b:a', '192k', mp3], capture_output=True, text=True, encoding='utf-8', errors='replace')
            if r.returncode != 0 or not os.path.exists(mp3):
                print(f'  {i:02d} 무음 다듬기 실패 → 원본 그대로 사용: {(r.stderr or "")[-120:]}')
                shutil.copyfile(f, mp3)
            io.open(mp3.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(lines[i])
            for suf in ('.segs.json', '.src'):
                if os.path.exists(mp3.replace('.mp3', suf)): os.remove(mp3.replace('.mp3', suf))
            mark_breaths(mp3, lines[i], first=(i == 0))
        pin_lines(lines, quiet=True)
        print(f'zip 의 문장 파일 {len(files)}개 → 구독 멘트 뺀 줄별 음성으로 사용'); shutil_rm(tmp); return len(lines)
    if len(files) == len(lines):
        for i, f in enumerate(files):
            mp3 = os.path.join(VDIR, f'{i:02d}.mp3')
            r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f, '-af', af, '-b:a', '192k', mp3], capture_output=True, text=True, encoding='utf-8', errors='replace')
            if r.returncode != 0 or not os.path.exists(mp3):   # 앞뒤 무음 자르기가 실패하면 원본 그대로 쓴다
                print(f'  {i:02d} 무음 다듬기 실패 → 원본 그대로 사용: {(r.stderr or "")[-120:]}')
                shutil.copyfile(f, mp3)
            io.open(mp3.replace('.mp3', '.txt'), 'w', encoding='utf-8').write(lines[i])
            for suf in ('.segs.json', '.src'):
                if os.path.exists(mp3.replace('.mp3', suf)): os.remove(mp3.replace('.mp3', suf))
            mark_breaths(mp3, lines[i], first=(i == 0))
        print(f'zip 의 문장 파일 {len(files)}개 → 줄별 음성으로 사용 (호흡 자리 쉼 {BREATH:.2f}초)'); shutil_rm(tmp); return len(files)
    print(f'zip 파일 수({len(files)})가 줄 수({len(lines)})와 달라 이어 붙여 통 음성으로 자릅니다')
    lst = os.path.join(tmp, 'list.txt')
    io.open(lst, 'w', encoding='utf-8').write('\n'.join("file '" + f.replace("'", "'\\''") + "'" for f in files) + '\n')
    wav = os.path.join(VDIR, 'full.wav')
    # 문장 사이에 0.9초 무음을 넣어 이어 붙인다(자르기 쉽게)
    gap = os.path.join(tmp, 'gap.wav'); subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', '0.9', gap], check=True)
    parts = []
    for f in files:
        w = f + '.wav'; subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f, '-ac', '1', '-ar', '24000', w], check=True); parts += [w, gap]
    io.open(lst, 'w', encoding='utf-8').write('\n'.join("file '" + f.replace("'", "'\\''") + "'" for f in parts[:-1]) + '\n')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, wav], check=True)
    n = split_full(wav, lines); shutil_rm(tmp); return n

def shutil_rm(p):
    import shutil
    shutil.rmtree(p, ignore_errors=True)

def fetch_drop(lines, wait_min=0):
    """통 음성 파일이 있으면 줄별로 자른다. 같은 파일(수정 시각)로 이미 잘라 뒀으면 건너뛴다. wait_min>0 이면 파일이 올 때까지 기다린다."""
    end = time.time() + wait_min * 60; said = False
    while True:
        found = [p for p in drop_paths() if os.path.exists(p)]
        if found: break
        if time.time() >= end:
            return 0
        if not said:
            print(f'통 음성 파일 대기 중 (최대 {wait_min}분): {os.path.abspath(drop_paths()[0])}  ← 타입캐스트 웹에서 받은 mp3 를 이 이름으로 넣어 주세요'); said = True
        time.sleep(10)
    src_file = found[0]
    stamp = f'{os.path.abspath(src_file)}|{os.path.getmtime(src_file):.0f}|b{BREATH:.2f}'   # 호흡 쉼 길이가 바뀌면 다시 자른다
    mark = os.path.join(VDIR, 'full.src')
    if os.path.exists(mark) and io.open(mark, encoding='utf-8').read().strip() == stamp and all(os.path.exists(os.path.join(VDIR, f'{i:02d}.mp3')) for i in range(len(lines))):
        return len(lines)
    if src_file.lower().endswith('.zip'):
        n = split_zip(src_file, lines)
    else:
        wav = os.path.join(VDIR, 'full.wav') if not src_file.endswith('full.wav') else os.path.join(VDIR, 'full_src.wav')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src_file, '-ac', '1', '-ar', '24000', wav], check=True)
        n = split_full(wav, lines)
    io.open(mark, 'w', encoding='utf-8').write(stamp)
    print(f'통 음성({os.path.basename(src_file)}) {n}줄로 분할 완료')
    return n

if __name__ == '__main__':
    lines = load_lines()
    PINNED = pin_lines(lines)   # 9/30: 구독 멘트 고정 음성
    manual = CFG.get('TTS_MANUAL', '0').strip() == '1'
    try:
        got = fetch_drop(lines, wait_min=int(CFG.get('TTS_WAIT_MIN', '40')) if manual else 0)
        if got: pin_lines(lines, quiet=True)   # 웹 zip 이 구독 멘트 줄을 덮었으면 다시 고정 음성으로
        if got and manual:
            print(f'완료 (통 음성에서 {got}줄 잘라 씀)'); sys.exit(0)
    except SystemExit: raise
    except Exception as e:
        import traceback; print(f'  통 음성 파일 처리 실패: {e!r}'); traceback.print_exc()
        if any(p.lower().endswith('.zip') and os.path.exists(p) for p in drop_paths()):
            sys.exit('음성 zip 은 있는데 자르지 못했습니다 — 위 오류를 Claude 에게 보여 주세요 (API 로 대신 만들지 않음)')
    disabled = drop_external(lines)
    try:
        if not disabled: fetch_full(lines)
    except SystemExit: raise
    except Exception as e: print(f'  통 음성 처리 실패(줄별 external 또는 TTS 로 진행): {e}')
    if not disabled: fetch_external(lines)
    pin_lines(lines, quiet=True)   # 9/30: 통 음성·external 이 구독 멘트 줄을 덮었어도 고정 음성으로
    only = None
    for a in sys.argv:
        if a.startswith('--only='): only = {int(x) for x in a.split('=',1)[1].replace(',', ' ').split()}
    if NO_API:
        need = [i for i, line in enumerate(lines) if only is None or i in only]
        need = [i for i in need if not (os.path.exists(os.path.join(VDIR, f'{i:02d}.mp3')) and os.path.exists(os.path.join(VDIR, f'{i:02d}.txt')) and io.open(os.path.join(VDIR, f'{i:02d}.txt'), encoding='utf-8').read().strip() == lines[i].strip())]
        if need:
            sys.exit(f'음성 실패: 줄 {need} 의 음성이 없고 API 키도 없습니다 — 타입캐스트 웹 zip 을 ' + os.path.abspath(drop_paths()[0]) + ' 에 넣어 주세요 (zip 파일 수 = 줄 수)')
        print('완료 (웹 zip 음성 그대로 사용, API 없음)'); sys.exit(0)
    # 9/27 사고 뒤: 합성 전에 이번에 새로 만들 줄·글자 수를 보여 주고, 평소보다 많으면 멈춘다
    def _made(i):
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3'); txt = mp3.replace('.mp3', '.txt'); ff = os.path.join(VDIR, 'fresh.flag')
        if os.path.exists(mp3.replace('.mp3', '.keep')) and os.path.exists(mp3): return True
        if not (os.path.exists(mp3) and os.path.exists(txt)): return False
        if io.open(txt, encoding='utf-8').read().strip() != lines[i].strip(): return False
        return not (os.path.exists(ff) and os.path.getmtime(txt) < os.path.getmtime(ff))
    if only is not None: todo = sorted(i for i in only if i < len(lines) and i not in PINNED)
    elif whole_mode():
        _idx = [i for i in range(len(lines)) if not os.path.exists(os.path.join(VDIR, f'{i:02d}.keep'))]
        todo = [] if all(_made(i) for i in _idx) else _idx
    else: todo = [i for i in range(len(lines)) if '--fresh' in sys.argv or not _made(i)]
    chars = sum(len(lines[i].replace('/', ' ').replace('  ', ' ').strip()) for i in todo)
    LIMIT = 3500 if '롱폼' in VDIR else 800   # 숏폼 1편 보통 300~500자, 롱폼 보통 2,000~3,000자(공백 포함)
    print(f'이번 합성: {len(todo)}줄 / 약 {chars}자(공백 포함) — 이 글자 수만큼 타입캐스트 크레딧이 듭니다 · 음성 폴더 {VDIR}')
    if chars > LIMIT and '--chars-ok' not in sys.argv:
        ok_ = False
        if asking():
            ok_ = input(f'  평소 분량({LIMIT}자)보다 많습니다. 정말 합성할까요? (y = 합성, Enter = 멈춤) ').strip().lower() in ('y', 'ㅛ')
        if not ok_:
            print(f'ASK_CHARS {chars} {LIMIT}')
            sys.exit(3)
    if only is None and whole_mode():
        if not synth_whole(lines):
            if NEED_ASK: print('ASK_' + NEED_ASK); sys.exit(3)
            if FAILS: print('계정별 결과: ' + ' / '.join(f'{k}: {v}' for k, v in FAILS.items()))
            sys.exit('통 합성 실패 — 줄별로 대신 만들지 않음(억양이 따로 놀아서)')
    print(f'{len(lines)}줄 합성 시작' + (f' (줄 {sorted(only)} 만)' if only else ''))
    fail = 0
    reuse = 0
    for i, line in enumerate(lines):
        if only is not None and i not in only: continue
        mp3 = os.path.join(VDIR, f'{i:02d}.mp3'); txt = mp3.replace('.mp3', '.txt'); segs = mp3.replace('.mp3', '.segs.json')
        # 9/26: 음성 폴더에 fresh.flag 가 있으면 그보다 먼저 만든 줄은 다시 만든다(NN.keep 줄은 그대로). 중간에 멈춰도 새로 만든 줄은 재사용
        _ff = os.path.join(VDIR, 'fresh.flag')
        if os.path.exists(_ff) and not os.path.exists(mp3.replace('.mp3', '.keep')) and os.path.exists(txt) and os.path.getmtime(txt) < os.path.getmtime(_ff):
            print(f'{i:02d} fresh.flag 이전 음성 → 다시 만듦')
        elif '--fresh' not in sys.argv and only is None and os.path.exists(mp3) and os.path.exists(txt) \
                and io.open(txt, encoding='utf-8').read().strip() == line.strip():
            reuse += 1; print(f'{i:02d} 재사용 {line}'); continue   # 같은 대사로 이미 만든 음성이 있으면 크레딧 안 씀 (--fresh 면 전부 새로)
        if i in PINNED: print(f'{i:02d} 구독 멘트 고정 음성 → 합성 안 함'); continue
        ok = synth_index(lines, i)
        print(f'{i:02d} {"OK " if ok else "XX "} {line}')
        fail += (not ok)
        if NEED_ASK:   # 1번 계정이 떨어져 멈춤 — 나머지 줄은 시도하지 않는다(만든 줄은 다음 실행 때 재사용)
            print('ASK_' + NEED_ASK); sys.exit(3)
        if not ok and FAILS and len(FAILS) >= len(ACCOUNTS):   # 모든 계정이 거부 → 나머지 줄은 시도해도 똑같이 실패하니 멈춘다
            print('모든 타입캐스트 계정이 거부해서 나머지 줄은 시도하지 않음'); break
        time.sleep(0.3)
    if fail:
        if FAILS: print('계정별 결과: ' + ' / '.join(f'{k}: {v}' for k, v in FAILS.items()))
        sys.exit(f'{fail}줄 실패' + (' — 모든 타입캐스트 계정이 거부됨(UNUSUAL_ACTIVITY 는 같은 PC 에서 무료 계정 여러 개를 쓴다고 본 것 → 계정 하나에 크레딧 충전이 확실한 해결)' if FAILS and all('UNUSUAL' in v for v in FAILS.values()) else ''))
    print('완료' + (f' (기존 음성 {reuse}줄 재사용)' if reuse else ''))
