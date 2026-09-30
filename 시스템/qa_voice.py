# -*- coding: utf-8 -*-
"""
음성 검수(QA): tts.py 가 만든 work/voice/NN.mp3 를 자동으로 검사하고 고친다. 렌더(build.py render) 전에 실행.
  python qa_voice.py            → 검사 + 이상한 줄 다시 합성 + 자막 타이밍 정밀 맞춤 + work/voice/qa.json 보고
  python qa_voice.py --check    → 검사만(다시 합성 안 함)

1) 톤·속도 일관성: 줄마다 목소리 높이(기본 주파수)와 말 속도를 재서, 영상 전체의 중간값에서 많이 벗어난 줄은
   다시 합성해 보고(최대 QA_RETRY 번) 가장 일관된 후보를 고른다. 깨짐(클리핑)·긴 무음·너무 짧은 음성도 잡는다.
2) 자막 타이밍: faster-whisper(설치돼 있으면)로 단어 시각을 받아 ' / ' 호흡 구간의 실제 시작 시각을 잡고
   NN.segs.json 을 고쳐 쓴다 → build.py 가 자막을 정확히 그 시점에 바꾼다. (없으면 tts.py 의 무음 기반 추정 그대로)
   설치: python -m pip install faster-whisper   (처음 한 번 모델 내려받음, 이후엔 오프라인)
3) 앞·끝 깨짐: 첫/끝 0.3초에 기계음·잡음·클릭이 섞이면(고역 잡음, 평탄한 스펙트럼, 음높이 떨림, 클릭) 다시 합성.
설정.txt: QA_RETRY=2  QA_PITCH_TOL=2.5(반음)  QA_RATE_MIN=4.3  QA_RATE_MAX=8.5  QA_WHISPER=small  QA_EDGE_SEC=0.3
"""
import os, sys, io, re, json, math, subprocess, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
def _voice_dir():
    try: key = io.open(os.path.join(os.environ.get('KBO_WORK', 'work'), 'current.txt'), encoding='utf-8').read().strip()
    except Exception: key = ''
    return os.path.join('work', 'voice_' + key) if key else os.path.join('work', 'voice')
VOICE = _voice_dir()   # 편별 음성 폴더 (build.py prep 이 정함)
CHECK_ONLY = '--check' in sys.argv

def cfg(k, d=''):
    try:
        for line in __import__('build').open_cfg('설정.txt'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                kk, v = line.split('=', 1)
                if kk.strip() == k: return v.strip()
    except Exception: pass
    return d
RETRY = int(cfg('QA_RETRY', '2')); PITCH_TOL = float(cfg('QA_PITCH_TOL', '2.5'))
RATE_MIN = float(cfg('QA_RATE_MIN', '4.3')); RATE_MAX = float(cfg('QA_RATE_MAX', '8.5'))
WHISPER = cfg('QA_WHISPER', 'small')

# ---------- 오디오 읽기 / 분석 (numpy 만 사용) ----------
SR = 16000
def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

def frames(x, win=0.04, hop=0.01):
    w, h = int(SR * win), int(SR * hop)
    n = max(0, (len(x) - w) // h + 1)
    idx = np.arange(w)[None, :] + h * np.arange(n)[:, None]
    return x[idx], h

def f0_track(x):
    """자기상관 기반 기본 주파수(Hz) 추정. 무성/무음 프레임은 0"""
    F, h = frames(x)
    if len(F) == 0: return np.zeros(0)
    F = F - F.mean(axis=1, keepdims=True)
    rms = np.sqrt((F ** 2).mean(axis=1)) + 1e-9
    thr = max(0.02, np.percentile(rms, 60) * 0.3)
    lo, hi = int(SR / 400), int(SR / 70)
    out = np.zeros(len(F))
    win = np.hanning(F.shape[1])
    for i, fr in enumerate(F):
        if rms[i] < thr: continue
        fr = fr * win
        ac = np.correlate(fr, fr, 'full')[len(fr) - 1:]
        if ac[0] <= 0: continue
        ac = ac / ac[0]
        seg = ac[lo:hi]
        k = int(np.argmax(seg)) + lo
        if ac[k] < 0.55: continue           # 주기성이 약하면 무성음
        out[i] = SR / k
    # 옥타브 튐 정리: 중간값의 절반/두 배 근처는 버림
    v = out[out > 0]
    if len(v) > 10:
        med = np.median(v)
        bad = (out > 0) & ((out < med * 0.6) | (out > med * 1.7))
        out[bad] = 0
    return out

def analyze(path, text):
    x = load(path)
    dur = len(x) / SR
    F, h = frames(x, 0.03, 0.01)
    if len(F) == 0: return {'dur': dur, 'bad': ['빈 파일']}
    rms = np.sqrt((F ** 2).mean(axis=1))
    on = rms > max(0.01, rms.max() * 0.06)
    idx = np.where(on)[0]
    lead = idx[0] * h / SR if len(idx) else 0.0
    tail = (idx[-1] * h / SR + 0.03) if len(idx) else dur
    # 안쪽 긴 무음
    gaps, run, start = [], 0, 0
    for i in range(len(on)):
        if not on[i]:
            if run == 0: start = i
            run += 1
        else:
            if run * 0.01 >= 0.6 and start > idx[0] and i < idx[-1]: gaps.append(round(run * 0.01, 2))
            run = 0
    syl = len(re.findall(r'[가-힣]', text)) or 1
    speech = max(0.1, tail - lead)
    f0 = f0_track(x[int(lead * SR):int(tail * SR)])
    v = f0[f0 > 0]
    peak = float(np.abs(x).max()) if len(x) else 0
    edge = edge_artifacts(x, lead, tail)
    r = {'edge': edge,'dur': round(float(dur), 2), 'speech': round(float(speech), 2), 'rate': round(float(syl / speech), 2), 'syl': syl,
         'f0': round(float(np.median(v)), 1) if len(v) else 0, 'f0_iqr': round(float(np.percentile(v, 75) - np.percentile(v, 25)), 1) if len(v) > 4 else 0,
         'voiced': round(len(v) / max(1, len(f0)), 2), 'peak': round(peak, 3), 'gaps': gaps}
    # 끝부분 억양(마지막 0.35초 vs 그 앞 0.35초, 반음)
    if len(f0) > 70:
        a, b = f0[-70:-35], f0[-35:]
        a, b = a[a > 0], b[b > 0]
        if len(a) > 5 and len(b) > 5: r['end_st'] = round(float(12 * math.log2(np.median(b) / np.median(a))), 1)
    return r

EDGE = float(cfg('QA_EDGE_SEC', '0.3'))   # 앞·끝에서 검사할 길이(초)

def spectral_feats(seg):
    """프레임별 (고역 비율, 스펙트럼 평탄도) — 기계음·잡음 감지용"""
    F, h = frames(seg, 0.032, 0.008)
    if len(F) == 0: return np.zeros(0), np.zeros(0)
    W = F * np.hanning(F.shape[1])
    P = np.abs(np.fft.rfft(W, axis=1)) ** 2 + 1e-12
    freqs = np.fft.rfftfreq(F.shape[1], 1 / SR)
    hf = P[:, freqs > 4000].sum(axis=1) / P.sum(axis=1)
    flat = np.exp(np.log(P).mean(axis=1)) / P.mean(axis=1)
    return hf, flat

def edge_artifacts(x, lead, tail):
    """앞·끝 EDGE 초 구간이 몸통과 달리 잡음·버즈·클릭이 섞였는지. 문제 있으면 설명 목록"""
    out = []
    a, b = int(lead * SR), int(tail * SR)
    body = x[a:b]
    if len(body) < SR * 0.8: return out
    hf_b, fl_b = spectral_feats(body)
    f0_b = f0_track(body)
    def stats(seg, f0):
        hf, fl = spectral_feats(seg)
        v = f0[f0 > 0]
        jit = float(np.mean(np.abs(np.diff(v)) / v[:-1])) if len(v) > 4 else 0.0
        rms = float(np.sqrt((seg ** 2).mean()) + 1e-9)
        click = float(np.abs(np.diff(seg)).max() / rms) if len(seg) > 2 else 0.0
        return (float(np.median(hf)) if len(hf) else 0, float(np.median(fl)) if len(fl) else 0, jit, click, len(v) / max(1, len(f0)))
    hb, fb, jb, _, _ = stats(body, f0_b)
    n = int(EDGE * SR)
    for name, seg in (('앞부분', body[:n]), ('끝부분', body[-n:])):
        if len(seg) < SR * 0.12: continue
        hf, fl, jit, click, vr = stats(seg, f0_track(seg))
        why = []
        if hf > max(0.22, hb * 3.0): why.append(f'고역잡음 {hf:.2f}')
        if fl > max(0.30, fb * 2.5): why.append(f'평탄스펙트럼 {fl:.2f}')
        if jit > max(0.12, jb * 3.0): why.append(f'음높이 떨림 {jit:.2f}')
        if click > 9.0: why.append(f'클릭 {click:.0f}')
        if why: out.append(f'{name} 깨짐({", ".join(why)})')
    return out

def semitones(a, b): return 12 * math.log2(a / b) if a > 0 and b > 0 else 0.0

def flags(r, target_f0, text):
    bad = []
    if r.get('bad'): return r['bad']
    if r['peak'] > 0.985: bad.append('클리핑')
    if r['voiced'] < 0.25: bad.append('목소리 불명확')
    if r['rate'] < RATE_MIN: bad.append(f'너무 느림 {r["rate"]}음절/초')
    if r['rate'] > RATE_MAX: bad.append(f'너무 빠름 {r["rate"]}음절/초')
    if target_f0 and r['f0'] and abs(semitones(r['f0'], target_f0)) > PITCH_TOL: bad.append(f'톤 이탈 {semitones(r["f0"], target_f0):+.1f}반음')
    if r['gaps']: bad.append(f'긴 무음 {r["gaps"]}')
    bad += r.get('edge', [])
    if text.strip().endswith('?') and r.get('end_st', 0) < -3: bad.append('질문인데 끝이 내려감')
    return bad

def score(r, target_f0, target_rate):
    """작을수록 좋음: 톤 차이(반음) + 속도 차이 + 결함"""
    s = abs(semitones(r['f0'], target_f0)) if (r.get('f0') and target_f0) else 3
    s += abs(r.get('rate', 6) - target_rate) * 1.5
    s += 4 * (r.get('peak', 0) > 0.985) + 4 * (r.get('voiced', 1) < 0.25) + 2 * len(r.get('gaps', [])) + 5 * len(r.get('edge', []))
    return round(s, 2)

# ---------- 자막 타이밍 정밀 맞춤 (faster-whisper, 선택) ----------
_model = None
def whisper_model():
    global _model
    if _model is not None: return _model
    try:
        from faster_whisper import WhisperModel
        _model = WhisperModel(WHISPER, device='cpu', compute_type='int8')
    except Exception as e:
        print(f'  (faster-whisper 없음 → 자막 시각은 무음 기반 추정 사용. 설치: python -m pip install faster-whisper) {str(e)[:80]}')
        _model = False
    return _model

def align_words(path, text):
    m = whisper_model()
    if not m: return None
    segs, _ = m.transcribe(path, language='ko', word_timestamps=True, beam_size=3, initial_prompt=text.replace('/', ','), vad_filter=False)
    words = []
    for s in segs:
        for w in (s.words or []):
            words.append((w.start, w.end, re.sub(r'[^가-힣A-Za-z0-9]', '', w.word)))
    return [w for w in words if w[2]]

def bounds_from_words(words, parts):
    """호흡 구간(parts)의 글자 수 누적 비율을 인식된 단어의 글자 누적과 맞춰 각 구간 시작 시각을 구한다"""
    if not words: return None
    tot_txt = sum(len(re.sub(r'[^가-힣A-Za-z0-9]', '', p)) for p in parts)
    tot_rec = sum(len(w[2]) for w in words)
    if tot_txt == 0 or tot_rec == 0: return None
    if abs(tot_rec - tot_txt) > max(4, 0.35 * tot_txt): return None   # 인식이 크게 어긋나면 신뢰 안 함
    bounds, acc_txt, acc_rec, wi = [0.0], 0, 0, 0
    for p in parts[:-1]:
        acc_txt += len(re.sub(r'[^가-힣A-Za-z0-9]', '', p))
        frac = acc_txt / tot_txt
        while wi < len(words) and (acc_rec + len(words[wi][2])) / tot_rec < frac - 1e-6:
            acc_rec += len(words[wi][2]); wi += 1
        # 이 단어까지 읽으면 구간 경계를 넘는다 → 경계는 다음 단어 시작(이 단어가 경계 직전 단어)
        if wi < len(words):
            # 남은 글자가 경계에 딱 맞으면 다음 단어 시작, 아니면(단어 중간) 이 단어 안에서 비례
            need = frac * tot_rec - acc_rec
            w = words[wi]
            if need < len(w[2]) - 0.5:      # 경계가 이 단어 안에 있음(단어가 붙어 인식된 경우) → 단어 안에서 비례
                t = w[0] + (w[1] - w[0]) * (need / len(w[2]))
            else:
                acc_rec += len(w[2]); wi += 1
                t = words[wi][0] if wi < len(words) else w[1]
            bounds.append(round(max(t - 0.03, bounds[-1] + 0.15), 3))
        else:
            bounds.append(round(words[-1][1], 3))
    return bounds

def inner_silences(path, thr='-36dB', mind=0.08):
    """음성 안쪽의 무음 구간 [(시작, 끝)] (앞뒤 무음 제외)"""
    r = subprocess.run(['ffmpeg', '-i', path, '-af', f'silencedetect=n={thr}:d={mind}', '-f', 'null', '-'], capture_output=True, text=True)
    st = [float(v) for v in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    en = [float(v) for v in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip() or 0)
    if len(en) < len(st): en.append(d)
    return [(a, b) for a, b in zip(st, en) if a > 0.05 and b < d - 0.05], d

def nchars(t): return len(re.sub(r'[^가-힣A-Za-z0-9]', '', t))

def assign_bounds(sil, lead, tail, parts, guess=None):
    """호흡 구간 경계 확정. 경계 후보는 실제 쉼(무음)뿐이다. 쉼이 경계 수보다 적으면(성우가 쉼표에서 안 쉼)
    어떤 경계가 그 쉼인지는 '말 속도가 일정하다'는 가정으로 고른다: 각 배정마다 구간별 초당 글자 수를 계산해
    전체 속도와 가장 고르게 맞는 배정을 택한다(whisper 예상 시각은 보조). 쉼이 없는 경계는 연속 발화 구간을 글자 수 비율로 나눈다."""
    need = len(parts) - 1
    syl = [max(1, nchars(x)) for x in parts]
    tot = sum(syl); speech = max(0.2, tail - lead)
    overall = tot / speech
    import itertools, math as _m
    def dist(t, iv):
        a, e = iv
        return 0.0 if a <= t <= e else min(abs(t - a), abs(t - e))
    def build(pairs):
        bounds = [lead] + [None] * need
        anchors = [(0, lead, lead)]
        for k in range(need):
            j = pairs[k]
            if j is not None:
                bounds[k + 1] = sil[j][1]; anchors.append((k + 1, sil[j][1], sil[j][0]))
        anchors.append((need + 1, tail, tail))
        cost = 0.0
        for (i0, start, _), (i1, _, stop) in zip(anchors, anchors[1:]):
            seg_syl = syl[i0:i1]; tot2 = sum(seg_syl); dur = max(0.05, stop - start)
            cost += abs(_m.log((tot2 / dur) / overall)) * (tot2 / tot + 0.3)   # 구간 속도가 전체와 다를수록 비용
            acc = 0
            for m in range(i0, i1 - 1):
                acc += syl[m]; bounds[m + 1] = start + (stop - start) * acc / tot2
        return bounds, cost
    best = None
    ns = len(sil)
    # 경계마다 (쉼 번호 또는 None), 쉼 번호는 증가해야 함
    def gen(k, j):
        if k == need: yield (); return
        for rest in gen(k + 1, j): yield (None,) + rest
        for jj in range(j, ns):
            for rest in gen(k + 1, jj + 1): yield (jj,) + rest
    for pairs in gen(0, 0):
        bounds, cost = build(pairs)
        used = sum(1 for x in pairs if x is not None)
        cost += 0.15 * (ns - used)                       # 안 쓴 쉼(조각 중간에 쉰 셈)은 약간 불리
        cost += 0.25 * (need - used)                     # 쉼 없는 경계(비율 추정)도 약간 불리
        if guess:
            cost += 0.15 * sum(dist(guess[k], sil[pairs[k]]) for k in range(need) if pairs[k] is not None)
        if best is None or cost < best[0]: best = (cost, bounds, used)
    _, bounds, used = best
    bounds[0] = 0.0
    for k in range(1, need + 1): bounds[k] = round(max(bounds[k], bounds[k - 1] + 0.15), 3)
    return bounds, used

# 9/30 사용자 지적(순위3 "삼 위 엘지는 칠십오 승 오십팔 패 / 기아도 져서" 를 "58패기아도" 로 붙여 읽음):
#   ' / ' 앞 구간이 이음말(-고·-서·-데·조사 등)로 안 끝나고 숫자·명사·'-요'로 끝나면 그 자리는 문장이 끊기는 곳 → 한 박자(STOP_PAUSE) 쉬어야 한다.
#   쉼이 그보다 짧으면 그 쉼 한가운데에 무음을 끼워 늘린다(다시 합성 안 함 → 크레딧 0). 쉼이 아예 없으면 경계 근처 가장 조용한 곳에 끼운다.
#   이미 충분히 쉬면 건드리지 않으므로 여러 번 돌려도 같다.
STOP_PAUSE = float(cfg('QA_STOP_PAUSE', '0.40'))
_JOIN = ('고', '서', '며', '면', '데', '지만', '니까', '려고', '도록', '듯', '게', '은', '는', '이', '가', '을', '를', '에', '에게', '한테',
         '와', '과', '랑', '도', '의', '로', '에서', '엔', '선', '까지', '부터', '보다', '처럼', '나', '든', '께', '론', '만',
         '어', '아', '해', '워', '야', '자', '러', '라', '아래', '때', '중', '동안')
_NUM = set('일이삼사오육칠팔구십백천만억영')
def is_stop(seg):
    ws = seg.split()
    w = re.sub(r'[^가-힣A-Za-z0-9]', '', ws[-1]) if ws else ''
    if not w: return False
    if w.endswith(('요', '다', '죠', '까', '니다')): return True
    if set(w) <= _NUM: return True   # 숫자로 끝남("일 대 칠", "오십팔")
    c = ord(w[-1]) - 0xAC00
    if 0 <= c < 11172 and c % 28 in (4, 8): return False   # 받침 ㄴ·ㄹ = '돌아온 / 김지찬', '할 / 것' 같은 꾸밈말
    return not w.endswith(_JOIN)

def widen_stops(path, parts, b):
    """문장이 끊기는 호흡 자리의 쉼을 STOP_PAUSE 까지 늘리고 늘어난 만큼 뒤 경계를 민다. (새 경계, 보고 글) 반환"""
    ks = [k for k in range(1, len(parts)) if k < len(b) and is_stop(parts[k - 1])]
    if not ks or STOP_PAUSE <= 0: return b, ''
    sil, d = inner_silences(path, '-38dB', 0.03)
    sr_ = 24000
    try: sr_ = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=sample_rate', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip() or 24000)
    except Exception: pass
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(sr_), '-'], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).copy()
    if not len(x): return b, ''
    ins = []   # (삽입 시각, 늘릴 길이, 경계 번호)
    for k in ks:
        t = b[k]
        iv = next(((s0, e0) for s0, e0 in sil if s0 - 0.06 <= t <= e0 + 0.06), None)
        if iv:
            gap = iv[1] - iv[0]
            if gap >= STOP_PAUSE - 0.02: continue
            ins.append(((iv[0] + iv[1]) / 2, STOP_PAUSE - gap, k))
        else:   # 쉼 없이 붙여 읽은 자리: 경계 ±0.1초 안에서 가장 조용한 10ms
            w = int(sr_ * 0.01); a0 = max(0, int((t - 0.1) * sr_)); a1 = min(len(x) - w, int((t + 0.1) * sr_))
            if a1 <= a0: continue
            en = [float(np.mean(x[j:j + w] ** 2)) for j in range(a0, a1, w)]
            at = (a0 + int(np.argmin(en)) * w + w / 2) / sr_
            ins.append((at, STOP_PAUSE, k))
    if not ins: return b, ''
    ins.sort()
    fade = int(sr_ * 0.004); out, prev = [], 0
    for at, add, _ in ins:
        j = int(at * sr_); seg = x[prev:j].copy()
        if len(seg) > fade: seg[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)
        out += [seg, np.zeros(int(add * sr_), dtype=np.float32)]
        prev = j
    tailx = x[prev:].copy()
    if len(tailx) > fade: tailx[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)
    y = np.concatenate(out + [tailx])
    tmp = path + '.stop.mp3'
    r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'f32le', '-ar', str(sr_), '-ac', '1', '-i', '-', '-b:a', '192k', tmp], input=y.tobytes(), capture_output=True)
    if r.returncode != 0 or not os.path.exists(tmp): return b, ''
    os.replace(tmp, path)
    nb = list(b)
    for j in range(1, len(b)):
        nb[j] = round(b[j] + sum(add for at, add, _ in ins if at <= b[j] + 1e-6), 3)
    for at, add, k in ins:   # 끼운 자리의 경계 = 끼운 무음이 끝나는 곳(다음 말 시작) 이상
        nb[k] = round(max(nb[k], at + sum(a2 for t2, a2, _ in ins if t2 <= at) ), 3)
    return nb, ' +한박자 ' + ','.join(f'{k}:{add:.2f}' for _, add, k in ins)

def refine_subs(i, line):
    """호흡 구간 경계 확정 → NN.segs.json. 자막이 말 도중에 넘어가거나 잠깐 깜빡이지 않도록 경계는 쉼 끝에, 쉼이 없으면 글자 비율로"""
    parts = [p.strip() for p in line.split('/') if p.strip()]
    if len(parts) <= 1: return 'single'
    path = os.path.join(VOICE, f'{i:02d}.mp3'); sj = path.replace('.mp3', '.segs.json')
    need = len(parts) - 1
    # 9/28: 사람이 확인해 고정한 경계("lock": true)는 건드리지 않는다
    try:
        if json.load(open(sj)).get('lock'): return 'lock(고정)'
    except Exception: pass
    # 9/28: whisper 가 없으면 tts.seg_bounds(말하는 시간 기준 · 말 속도 고르게)로 잡는다 — 옛 assign_bounds 는 쉼 개수가 맞으면 순서대로 붙여 한 칸씩 밀렸다
    if not whisper_model():
        import tts
        bb = tts.seg_bounds(path, parts)
        b = [x for x, _ in bb]
        b, wide = widen_stops(path, parts, b)
        durs = [b[k + 1] - b[k] for k in range(len(b) - 1)] + [0.0]
        json.dump({'durs': durs, 'pause': 0.0, 'bounds': b, 'src': 'speech-time' + wide}, open(sj, 'w'))
        return 'speech-time' + wide + ' ' + ' '.join(f'{x:.2f}' for x in b[1:])
    sil, d = inner_silences(path)
    x = load(path)
    F, h = frames(x, 0.03, 0.01)
    rms = np.sqrt((F ** 2).mean(axis=1)) if len(F) else np.zeros(0)
    on = np.where(rms > max(0.01, (rms.max() if len(rms) else 0) * 0.06))[0]
    lead = on[0] * 0.01 if len(on) else 0.0
    tail = (on[-1] * 0.01 + 0.03) if len(on) else d
    words = align_words(path, line)
    guess = bounds_from_words(words, parts) if words else None
    guess = guess[1:] if guess else None
    b, matched = assign_bounds(sil, lead, tail, parts, guess)
    b, wide = widen_stops(path, parts, b)
    durs = [b[k + 1] - b[k] for k in range(len(b) - 1)] + [0.0]
    src = f'쉼 {matched}/{need}' + (' +whisper' if guess else '') + ('' if matched == need else ' +비율') + wide
    json.dump({'durs': durs, 'pause': 0.0, 'bounds': b, 'src': src}, open(sj, 'w'))
    return src + ' ' + ' '.join(f'{x:.2f}' for x in b[1:])

# ---------- 메인 ----------
def main():
    import tts
    # 9/26: 타입캐스트가 직접 배속(TTS_TEMPO/콘티 ttsTempo)해서 만들면 음절 속도 기준도 그만큼 올린다(1.2배 줄을 '너무 빠름'으로 다시 합성하지 않게)
    global RATE_MIN, RATE_MAX
    _t = max(1.0, float(getattr(tts, 'TEMPO', 1.0) or 1.0)); RATE_MIN *= _t; RATE_MAX *= _t
    lines = tts.load_lines()
    N = len(lines)
    rep = {}
    for i in range(N):
        p = os.path.join(VOICE, f'{i:02d}.mp3')
        if not os.path.exists(p): print(f'{i:02d} 파일 없음'); continue
        rep[i] = analyze(p, lines[i])
    f0s = [r['f0'] for r in rep.values() if r.get('f0')]
    rates = [r['rate'] for r in rep.values() if r.get('rate')]
    target_f0 = float(np.median(f0s)) if f0s else 0
    target_rate = float(np.median(rates)) if rates else 6.0
    print(f'기준: 목소리 높이 {target_f0:.0f}Hz, 속도 {target_rate:.1f}음절/초 ({N}줄)')
    redo = []
    for i in range(N):
        if i not in rep: continue
        b = flags(rep[i], target_f0, lines[i])
        rep[i]['flags'] = b
        print(f'{i:02d} {rep[i]["f0"]:>4.0f}Hz {rep[i]["rate"]:.1f}음/초 {rep[i]["dur"]:.1f}s' + (f'  ← {", ".join(b)}' if b else ''))
        # 9/26: NN.keep 이 있는 줄(따로 녹음해 넣은 구독 멘트 등)은 톤이 달라도 다시 합성하지 않는다
        if b and not os.path.exists(os.path.join(VOICE, f'{i:02d}.keep')): redo.append(i)
    if redo and getattr(tts, 'whole_mode', lambda: False)(): print(f'주의 줄 {redo} — 통 합성이라 한 줄만 다시 만들지 않음(억양이 튐)'); redo = []
    if redo and getattr(tts, 'NO_API', False): print(f'주의 줄 {redo} — API 키가 없어 다시 합성하지 않음(웹 zip 그대로)'); redo = []
    if redo and not CHECK_ONLY and RETRY > 0:
        print(f'다시 합성 시도: {redo}')
        for i in redo:
            p = os.path.join(VOICE, f'{i:02d}.mp3')
            best = (score(rep[i], target_f0, target_rate), p, rep[i])
            cands = []
            for t in range(RETRY):
                cp = os.path.join(VOICE, f'{i:02d}_c{t}.mp3')
                if not tts.synth_index(lines, i, out=cp): continue
                r = analyze(cp, lines[i]); s = score(r, target_f0, target_rate)
                cands.append(cp)
                print(f'   후보{t}: {r["f0"]:.0f}Hz {r["rate"]:.1f}음/초 점수 {s} (원본 {best[0]})')
                if s < best[0]: best = (s, cp, r)
            if best[1] != p:
                shutil.copy(best[1], p)
                sj = best[1].replace('.mp3', '.segs.json')
                if os.path.exists(sj): shutil.copy(sj, p.replace('.mp3', '.segs.json'))
                rep[i] = best[2]; rep[i]['flags'] = flags(rep[i], target_f0, lines[i]); rep[i]['replaced'] = True
                print(f'   → 교체 (점수 {best[0]})')
            else:
                print('   → 원본 유지')
            for cp in cands:
                for f_ in (cp, cp.replace('.mp3', '.segs.json')):
                    try: os.remove(f_)
                    except Exception: pass
    # 자막 타이밍 정밀 맞춤
    print('자막 타이밍:')
    for i in range(N):
        if i not in rep: continue
        how = refine_subs(i, lines[i])
        rep[i]['subs'] = how
        if how not in ('single',): print(f'  {i:02d} {how}')
    remaining = [i for i in rep if rep[i].get('flags')]
    out = {'target_f0': round(target_f0, 1), 'target_rate': round(target_rate, 2), 'lines': rep, 'remaining_flags': remaining}
    json.dump(out, io.open(os.path.join(VOICE, 'qa.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if remaining: print(f'남은 주의 줄: {remaining} (' + '; '.join(f'{i:02d}: {", ".join(rep[i]["flags"])}' for i in remaining) + ')')
    else: print('검수 통과: 톤·속도 일관, 결함 없음')

if __name__ == '__main__':
    main()
