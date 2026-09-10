#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
episode.json 하나로 영상을 만든다.
  python build.py prep   episodes/2026-09-06_1.json   → work/narration.txt 생성 (tts.py 가 읽음)
  python build.py render episodes/2026-09-06_1.json   → work/voice/NN.mp3 로 타임라인 계산 → 렌더 → ../영상/2026-09-06/1_두산.mp4 (+ 썸네일, 유튜브 제목설명 txt)
  python build.py thumb  episodes/2026-09-06_1.json   → 썸네일만
중간 파일은 전부 work/ 에, 결과물은 상위 폴더 영상/날짜/ 에 저장한다.
필요: ffmpeg, node + playwright(chromium)
"""
import json, re, subprocess, os, shutil, sys, base64, io, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

LEAD, TAIL, SUBLEAD = 0.25, 1.30, 0.05   # SUBLEAD: 자막을 말보다 살짝(0.05초) 먼저 — 거의 동시
FPS = 15
WORK = 'work'                                        # 중간 파일(음성, 프레임, 임시 html) 폴더
OUT_ROOT = os.path.join(HERE, '..', '영상')           # 결과물: 영상/2026-09-06/1_두산.mp4
def _cfg_raw(k, default=''):
    try:
        for line in io.open(os.path.join(HERE, '설정.txt'), encoding='utf-8-sig'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                kk, v = line.split('=', 1)
                if kk.strip() == k and v.strip(): return v.strip().strip('"')
    except Exception: pass
    return default
# 설정.txt 에 OUTPUT_DIR=G:\내 드라이브\야구자판기 처럼 적으면 결과물을 그 폴더(구글 드라이브 동기화 폴더 등)에 저장
_out_cfg = _cfg_raw('OUTPUT_DIR', '')
if _out_cfg:
    # 설정된 드라이브/폴더가 이 PC 에 없으면(예: 구글 드라이브 앱이 없는 PC) 상위 폴더 영상\ 로 대신 저장
    _drive = os.path.splitdrive(_out_cfg)[0] + os.sep if os.path.splitdrive(_out_cfg)[0] else os.path.dirname(_out_cfg)
    if os.path.isdir(_drive): OUT_ROOT = _out_cfg
    else: print(f'경고: OUTPUT_DIR {_out_cfg} 를 찾을 수 없어 상위 폴더 영상\\ 에 저장합니다')
os.makedirs(WORK, exist_ok=True)
W = lambda *a: os.path.join(WORK, *a)

def team_label(ep):
    """파일 이름용 팀 이름: '두산' 또는 '롯데_한화'"""
    th = ep.get('thumb') or {}
    teams = th.get('teams') or ([th['team']] if th.get('team') else []) or ([ep['focusTeam']] if ep.get('focusTeam') else [])
    lab = '_'.join(re.sub(r'[^0-9A-Za-z가-힣]', '', str(t)) for t in teams if t)
    return lab or 'KBO'

def out_paths(ep, ep_path):
    """(영상 mp4, 썸네일 jpg, 유튜브 제목설명 txt) 경로. 폴더는 영상/날짜/, 이름은 번호_팀"""
    stem = os.path.splitext(os.path.basename(ep_path))[0]
    key = stem.rsplit('_', 1)[-1] if '_' in stem else stem
    date = ep.get('date') or (stem.split('_')[0] if re.match(r'\d{4}-\d{2}-\d{2}', stem) else datetime.date.today().isoformat())
    d = os.path.abspath(os.path.join(OUT_ROOT, date))
    base = os.path.join(d, f'{key}_{team_label(ep)}')
    return base + '.mp4', base + '_썸네일.jpg', base + '_유튜브.txt'

# 구단 코드 → KBO_logos 폴더의 파일 이름
LOGO_FILES = {'HT': '기아', 'SS': '삼성', 'LG': 'LG', 'OB': '두산', 'KT': 'KT',
              'NC': 'NC', 'LT': '롯데', 'SK': 'SSG', 'HH': '한화', 'WO': '키움'}
LOGO_DIRS = [os.path.join(HERE, '..', 'KBO_logos'), os.path.join(HERE, 'KBO_logos'), os.path.join(HERE, 'logos')]

def run(cmd, check=False):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode != 0:
        raise SystemExit(f'실패: {" ".join(cmd)}\n{r.stderr[-800:]}')
    return r

def load_episode(path):
    ep = json.load(io.open(path, encoding='utf-8-sig'))
    if not ep.get('standings'):
        rk = json.load(io.open('data/rank_latest.json', encoding='utf-8-sig'))
        ep['standings'] = rk['standings']
    if not ep.get('dateLabel'):
        d = ep.get('date') or datetime.date.today().isoformat()
        ep['dateLabel'] = d.replace('-', '.')
    return ep

def font_dir_url():
    """상위 폴더 폰트\\ 의 file:// 주소 (템플릿의 __FONT_DIR__ 자리에 넣는다)"""
    import pathlib
    for d in (os.path.join(HERE, '..', '폰트'), os.path.join(HERE, 'fonts'), os.path.join(HERE, '폰트')):
        if os.path.isdir(d): return pathlib.Path(os.path.abspath(d)).as_uri()
    return ''

def logos_data_uri():
    out = {}
    for code, name in LOGO_FILES.items():
        for d in LOGO_DIRS:
            for ext in ('.webp', '.png', '.PNG', '.jpg'):
                p = os.path.join(d, name + ext)
                if os.path.exists(p):
                    mime = 'image/webp' if ext == '.webp' else 'image/png' if ext.lower() == '.png' else 'image/jpeg'
                    out[code] = f'data:{mime};base64,' + base64.b64encode(open(p, 'rb').read()).decode()
                    break
            if code in out: break
        if code not in out:
            print('경고: 로고 없음', code, name)
    return out

# ---------- prep ----------
# 숫자 읽기 규칙: 나레이션은 한글로 적는다(타입캐스트가 숫자를 제멋대로 읽는 것 방지).
#  고유어(하나·둘·셋…): 점, 경기, 게임 차, 개, 명, 번, 시, 가지, 장  → "열두 점", "스물두 경기", "두 시"
#  한자어(일·이·삼…): 승, 패, 위, 이닝, 회, 년, 월, 일, 분, 초, 억, 달러, 순위, 라운드, 연승/연패, 점수(삼 대 십구), 승률·타율 → "이 승 십 패", "이십사 이닝"
NATIVE = r'(한|두|세|네|다섯|여섯|일곱|여덟|아홉|열\S*|스물\S*|서른\S*)'
SINO = r'(일|이|삼|사|오|육|칠|팔|구|십\S*|백\S*)'
def narr_check(lines):
    warns = []
    for i, t in enumerate(lines):
        if re.search(r'\d', t): warns.append(f'{i:02d} 숫자는 한글로 적어 주세요: {t}')
        for m in re.finditer(NATIVE + r' ?(승|패|위|이닝|회|년|월|일|분|초|억|달러|순위|라운드)(?![가-힣])', t):
            warns.append(f'{i:02d} "{m.group(0)}" → 한자어로 (이 승, 십 패, 삼 위)')
        for m in re.finditer(r'(?<![가-힣])' + SINO + r' ?(점|경기|게임|개|명|가지|장)(?![가-힣])', t):
            warns.append(f'{i:02d} "{m.group(0)}" → 고유어로 (열두 점, 스물두 경기)')
    return warns

def ep_key(ep_path):
    stem = os.path.splitext(os.path.basename(ep_path))[0]
    return stem

def voice_dir(key=None):
    """편마다 음성 폴더를 따로 둔다(work/voice_<콘티이름>/). 1편·2편 음성이 서로 덮어쓰지 않게"""
    if key is None:
        try: key = io.open(W('current.txt'), encoding='utf-8').read().strip()
        except Exception: key = ''
    d = W('voice_' + key) if key else W('voice')
    os.makedirs(d, exist_ok=True)
    return d

def VW(*a): return os.path.join(voice_dir(), *a)

def prep(ep, ep_path=None):
    lines = [l['narr'].strip() for l in ep['lines']]
    if ep_path:
        io.open(W('current.txt'), 'w', encoding='utf-8').write(ep_key(ep_path))
        voice_dir(ep_key(ep_path))
    for w_ in narr_check(lines): print('숫자 읽기 경고:', w_)
    io.open(W('narration.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print(f'work/narration.txt {len(lines)}줄')

# ---------- render ----------
def dur_of(f):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).stdout.strip())

def probe(f):
    """앞뒤 무음 위치. 문턱 -40dB/0.12초 (말끝 여운을 자르지 않도록 넉넉하게)"""
    d = dur_of(f)
    r = run(['ffmpeg', '-i', f, '-af', 'silencedetect=n=-40dB:d=0.12', '-f', 'null', '-'])
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    lead = ends[0] if starts and ends and starts[0] < 0.02 else 0.0
    tail = d
    if starts and (len(ends) < len(starts) or ends[-1] >= d - 0.03):
        tail = starts[-1]
    return d, lead, tail

TARGET_MEAN, PEAK_CAP = -19.0, -1.0   # 줄 평균 음량 목표(dB), 피크 상한(dB)
def static_gain(f, ss, to):
    """잘라낼 구간의 평균·최대 음량을 재서 한 번에 적용할 고정 이득(dB). 평균을 목표에 맞추되 피크가 상한을 넘지 않게"""
    r = run(['ffmpeg', '-i', f, '-af', f'atrim=start={ss:.3f}:end={to:.3f},volumedetect', '-f', 'null', '-'])
    m = re.search(r'mean_volume: ([\-\d.]+)', r.stderr); p = re.search(r'max_volume: ([\-\d.]+)', r.stderr)
    if not m or not p: return 0.0
    mean, peak = float(m.group(1)), float(p.group(1))
    return round(min(TARGET_MEAN - mean, PEAK_CAP - peak), 2)

def end_level(f, ms=30):
    """파일 마지막 ms 구간의 평균 음량(dB). 말이 잘렸으면 크게 나온다"""
    d = dur_of(f)
    r = run(['ffmpeg', '-i', f, '-af', f'atrim=start={max(0, d - ms/1000):.3f},volumedetect', '-f', 'null', '-'])
    m = re.search(r'mean_volume: ([\-\d.]+)', r.stderr)
    return float(m.group(1)) if m else -99.0

CONNECT_END = re.compile(r'(는데|고요|지만|면|니까|서|고|도|은|는|이|가)$')   # 말이 이어지는 어미
TURN_START = ('그래서', '근데', '그런데', '그러니까', '변수는', '결론', '제 예측', '문제는', '이유는', '단 ', '그럼', '만약')

MAX_GAP = 0.5   # 어떤 쉼도 이보다 길지 않게(답답함 방지)

def gap_after(i, line, n, nxt=None, scene_change=False):
    """줄과 줄 사이 쉼(초). 말이 이어지면 거의 안 쉬고, 문장이 끝나면 짧게, 장면(이미지)이 바뀌거나 방향을 바꾸는 말 앞에서만 조금 더 (최대 0.5초)"""
    g = line.get('gapAfter')
    if g is not None: return min(MAX_GAP, float(g))
    t = line['narr'].strip()
    if CONNECT_END.search(t) and not t.endswith(('요', '죠')): gap = 0.10
    elif t.endswith('?'): gap = 0.30
    else: gap = 0.24
    if nxt and nxt['narr'].strip().startswith(TURN_START): gap = max(gap, 0.38)
    if scene_change: gap = max(gap, 0.32)
    if i == 0: gap = min(gap, 0.18)   # 후킹 대사 뒤는 뜸 들이지 않고 바로 본론으로
    return round(min(gap, MAX_GAP), 2)

def pace_of(i, line, n):
    """줄별 말 속도 배율. 기본은 그대로(1.0) — 느리게 하면 답답하다는 피드백. 콘티에 pace: slow|normal|fast 로만 조절"""
    p = line.get('pace')
    if p in ('slow', 'normal', 'fast'): return {'slow': 0.94, 'normal': 1.0, 'fast': 1.08}[p]
    return 1.0

# 장면 종류별 최소 길이(초): 모션이 다 끝나기 전에 장면이 넘어가지 않도록, 나레이션이 짧으면 장면 끝에 여유를 둔다
MIN_SCENE = {'streaks': 3.4, 'table': 3.2, 'verdict': 3.0, 'shift': 2.6, 'versus': 2.4, 'need': 2.4, 'rival': 2.2, 'matchup': 2.4, 'hook': 1.0, 'big': 1.4, 'question': 1.4}

SUB_MAX = 16   # 자막 한 줄 최대 글자 수(공백 포함, 한글 기준)

def wrap2(text):
    """자막을 최대 2줄로. 이미 줄바꿈이 있으면 각 줄이 길지 않은지 확인하고, 없으면 띄어쓰기에서 균형 있게 나눈다"""
    text = text.strip()
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    if len(lines) == 2 and all(len(l) <= SUB_MAX for l in lines): return '\n'.join(lines)
    flat = ' '.join(lines)
    if len(flat) <= SUB_MAX: return flat
    words = flat.split(' ')
    best, bestd = None, 1e9
    for k in range(1, len(words)):
        a, b = ' '.join(words[:k]), ' '.join(words[k:])
        d = abs(len(a) - len(b)) + (100 if max(len(a), len(b)) > SUB_MAX else 0)
        if d < bestd: best, bestd = (a, b), d
    return '\n'.join(best) if best else flat

def sub_pieces(line):
    """'sub' 가 '|' 로 나뉘어 있으면 호흡 단위 자막 조각들, 아니면 한 조각"""
    sub = line.get('sub') or ''
    pieces = [p_.strip() for p_ in sub.split('|')] if '|' in sub else [sub]
    return [wrap2(p_) for p_ in pieces]

def silence(name, sec):
    run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', f'{sec:.3f}', name])

def render(ep, ep_path):
    lines = ep['lines']; N = len(lines)
    spd = float(cfg_get('SPEED', '1.0'))   # 1.0 = 그대로(배속은 타입캐스트 TTS_TEMPO 로), 0.9 = 10% 느리게
    # 1) 음성 확인 + 트리밍 (자르기는 atrim 필터로, 속도 조절은 그 다음에 → -to 가 느려진 소리 끝을 잘라먹지 않는다)
    clips, warns, seg_start, seg_rate = [], [], [], []
    retried = set()
    i = 0
    while i < N:
        src = VW(f'{i:02d}.mp3')
        if not os.path.exists(src): raise SystemExit(f'음성 없음: {src}')
        d, lead, tail = probe(src)
        ss, to = max(0, lead - 0.06), min(d, tail + 0.12)
        dst = VW(f't{i:02d}.wav')
        rate = spd * pace_of(i, lines[i], N)
        gain = static_gain(src, ss, to)
        def cut(ss, to):
            af = f'atrim=start={ss:.3f}:end={to:.3f},asetpts=PTS-STARTPTS'
            if abs(rate - 1.0) > 0.01: af += f',atempo={rate:.3f}'
            # 음량은 줄마다 '고정 이득'으로만 맞춘다(loudnorm 같은 동적 정규화는 짧은 클립의 앞뒤 음량을 출렁이게 해 기계음처럼 들림)
            # + 앞뒤 12ms 페이드(딱 끊기는 소리 방지)
            af += f',volume={gain:.2f}dB,aresample=44100,afade=t=in:d=0.012,areverse,afade=t=in:d=0.012,areverse'
            run(['ffmpeg', '-y', '-i', src, '-af', af, '-ar', '44100', '-ac', '1', dst], check=True)
        cut(ss, to)
        # 검수: 잘린 끝이 아직 말소리(-30dB 이상)면 끝을 자르지 않고 다시
        if to < d and end_level(dst) > -30:
            cut(ss, d); warns.append(f'{i:02d} 끝 여운 보존')
        clips.append(dur_of(dst)); seg_start.append(ss); seg_rate.append(rate)
        # 검수: 글자 수 대비 너무 짧으면(말이 잘린 음성) 중단
        syl = len(re.findall(r'[가-힣]', lines[i]['narr'])) or 1
        if syl / (clips[-1] * rate) > 9.3:
            if i not in retried:
                # 잘린 음성으로 보임 → 그 줄만 자동으로 다시 만들고 한 번 더 시도
                print(f'음성 {i:02d} 이 글자 수에 비해 너무 짧아요 ({clips[-1]:.2f}s/{syl}음절) → 다시 합성')
                retried.add(i)
                r = subprocess.run([sys.executable, '-X', 'utf8', 'tts.py', f'--only={i}'], capture_output=True, text=True, encoding='utf-8', errors='replace')
                if r.returncode == 0:
                    clips.pop(); seg_start.pop(); seg_rate.pop(); continue
                print('  다시 합성 실패:', (r.stdout + r.stderr)[-300:])
            raise SystemExit(f'음성 {i:02d} 이 글자 수에 비해 너무 짧아요 ({clips[-1]:.2f}s/{syl}음절). 타입캐스트 크레딧을 확인하고 tts.py --only={i} 로 다시 만들어 주세요.')
        i += 1
    if warns: print('트리밍 조정:', ', '.join(warns))
    # 2) 타임라인 (장면 최소 길이 보장: 장면의 마지막 줄 뒤 여유를 늘린다)
    starts = [s.get('startLine', 0) for s in ep['scenes']]
    scene_first = set(starts)
    gaps = [gap_after(i, lines[i], N, lines[i + 1] if i + 1 < N else None, scene_change=(i + 1) in scene_first) for i in range(N)]
    def line_starts():
        st, t = [], LEAD
        for i in range(N):
            st.append(t); t += clips[i] + gaps[i]
        return st
    for k, s in enumerate(ep['scenes']):
        a = starts[k]; b = starts[k + 1] if k + 1 < len(starts) else N
        if b <= a or b > N: continue
        st = line_starts()
        span = (st[b] if b < N else st[N - 1] + clips[N - 1] + TAIL) - st[a]
        need = float(s.get('minDur', MIN_SCENE.get(s.get('type'), 1.2)))
        if span < need:
            gaps[b - 1] = min(MAX_GAP, gaps[b - 1] + (need - span))   # 모션은 template 이 장면 길이에 맞춰 빨라지므로 쉼은 0.5초까지만
    st = line_starts()
    total = st[N - 1] + clips[N - 1] + TAIL
    # 자막은 "실제로 말이 나오는 동안"만: 잘라낸 클립 안에서 말이 시작·끝나는 시각을 다시 재서 그 사이에만 띄운다
    subs = []
    for i in range(N):
        dst = VW(f't{i:02d}.wav')
        d2, lead2, tail2 = probe(dst)
        sp_start, sp_end = st[i] + max(0, lead2 - SUBLEAD), st[i] + min(d2, tail2 + 0.05)
        pieces = sub_pieces(lines[i])
        segf = VW(f'{i:02d}.segs.json')
        if len(pieces) > 1 and os.path.exists(segf):
            # 호흡 구간(' / ')과 자막 조각('|') 수가 같으면 구간 시작마다 자막을 바꾼다 (조각 사이는 빈틈 없이 이어서)
            sg = json.load(open(segf)); durs, pause = sg['durs'], sg['pause']
            if len(durs) == len(pieces):
                ss_i = seg_start[i]; rate = seg_rate[i]
                starts_k, acc = [], 0.0
                for k, d_ in enumerate(durs):
                    starts_k.append(st[i] + max(0, (acc - ss_i)) / rate); acc += d_ + pause
                items = []
                for k, pc in enumerate(pieces):
                    a = sp_start if k == 0 else max(sp_start, starts_k[k] - SUBLEAD)
                    b = min(sp_end, starts_k[k + 1] - SUBLEAD) if k + 1 < len(pieces) else sp_end
                    items.append([a, b, pc])
                # 너무 짧게(0.45초 미만) 스쳐 가는 조각은 앞 조각과 합쳐 보여준다(깜빡임 방지)
                merged = []
                for it in items:
                    if merged and (it[1] - it[0] < 0.45 or merged[-1][1] - merged[-1][0] < 0.45):
                        merged[-1] = [merged[-1][0], it[1], wrap2(merged[-1][2].replace('\n', ' ') + ' ' + it[2].replace('\n', ' '))]
                    else: merged.append(it)
                for a, b, pc in merged: subs.append([round(a, 2), round(b, 2), pc])
                continue
            print(f'경고: {i:02d} 자막 조각({len(pieces)})과 호흡 구간({len(durs)}) 수가 달라 한 덩어리로 표시')
        subs.append([round(sp_start, 2), round(sp_end, 2), wrap2(' '.join(pieces)) if len(pieces) > 1 else pieces[0]])
    bounds = [round(st[k] - 0.10, 2) for k in starts[1:]]
    # 3) 나레이션 합치기
    silence(VW('lead.wav'), LEAD); silence(VW('tail.wav'), TAIL)
    with open(VW('list.txt'), 'w') as f:
        f.write("file 'lead.wav'\n")
        for i in range(N):
            f.write(f"file 't{i:02d}.wav'\n")
            if i < N - 1:
                silence(VW(f'g{i:02d}.wav'), gaps[i]); f.write(f"file 'g{i:02d}.wav'\n")
        f.write("file 'tail.wav'\n")
    run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', VW('list.txt'), W('narration.wav')], check=True)
    # 4) 템플릿에 데이터 주입
    EP = dict(ep); EP['subs'] = subs; EP['bounds'] = bounds; EP['logos'] = logos_data_uri(); EP['total'] = round(total, 2)
    html = io.open('template.html', encoding='utf-8').read().replace('__FONT_DIR__', font_dir_url())
    html = html.replace('<script>', '<script>window.EP=' + json.dumps(EP, ensure_ascii=False) + ';</script><script>', 1)
    io.open(W('render.html'), 'w', encoding='utf-8').write(html)
    json.dump({'total': round(total, 2), 'starts': st, 'durs': clips, 'gaps': gaps, 'bounds': bounds, 'subs': subs},
              io.open(W('timeline.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 5) 프레임 렌더
    shutil.rmtree(W('frames'), ignore_errors=True); os.makedirs(W('frames'))
    r = subprocess.run(['node', 'frames.js', str(round(total, 2))], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0: raise SystemExit('프레임 렌더 실패:\n' + (r.stderr or r.stdout)[-1500:])
    nframes = len(os.listdir(W('frames')))
    if nframes < FPS * total * 0.95: raise SystemExit(f'프레임 부족: {nframes}')
    # 6) 합성 → 결과물 폴더(영상/날짜/번호_팀.mp4)
    out, thumb_path, yt_path = out_paths(ep, ep_path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    name = os.path.splitext(os.path.basename(ep_path))[0]
    run(['ffmpeg', '-y', '-framerate', str(FPS), '-i', W('frames', 'f%04d.jpg'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '30', '-crf', '20', W('silent.mp4')], check=True)
    bgm = pick_bgm(ep)
    if bgm:
        # 배경음악: 나레이션 아래에 깔고(볼륨 설정.txt BGM_VOLUME, 기본 0.12), 말할 때 자동으로 더 낮춤(사이드체인), 끝에 페이드아웃
        vol = float(cfg_get('BGM_VOLUME', '0.12'))
        fade = max(0.5, total - 1.6)
        fc = (f"[2:a]aloop=loop=-1:size=2e9,atrim=0:{total:.2f},volume={vol},afade=t=in:d=0.8,afade=t=out:st={fade:.2f}:d=1.5[bg];"
              f"[1:a]asplit=2[n1][n2];[bg][n2]sidechaincompress=threshold=0.05:ratio=6:attack=40:release=500[bgd];"
              f"[n1][bgd]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]")
        run(['ffmpeg', '-y', '-i', W('silent.mp4'), '-i', W('narration.wav'), '-i', bgm, '-filter_complex', fc, '-map', '0:v', '-map', '[a]',
             '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
        print('배경음악:', os.path.basename(bgm))
    else:
        run(['ffmpeg', '-y', '-i', W('silent.mp4'), '-i', W('narration.wav'), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
    d = dur_of(out)
    thumb = make_thumb(EP, thumb_path)
    write_youtube_txt(ep, yt_path, d)
    print(f'완료: {out} {d:.2f}초 (자막 {len(subs)}개, 장면 {len(ep["scenes"])}개) 썸네일 {thumb}')
    return out

def write_youtube_txt(ep, path, dur=0):
    """사용자가 확인하기 쉽게 유튜브 제목·설명·태그를 텍스트로 같이 저장"""
    y = ep.get('youtube') or {}
    body = [f'[제목]', y.get('title', ''), '', '[설명]', y.get('description', ''), '', '[태그]', ', '.join(y.get('tags', [])), '',
            f'[정보] 기준 {ep.get("dateLabel", "")} / 길이 {dur:.1f}초 / 콘티 {ep.get("focusTeam", "")}']
    io.open(path, 'w', encoding='utf-8').write('\n'.join(body) + '\n')

def cfg_get(k, default=''):
    try:
        for line in io.open('설정.txt', encoding='utf-8-sig'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                kk, v = line.split('=', 1)
                if kk.strip() == k: return v.strip()
    except Exception: pass
    return default

def pick_bgm(ep):
    """bgm/ 폴더의 음악 중 하나. 콘티에 bgm 이름이 있으면 그것, 없으면 날짜로 돌아가며 선택"""
    d = os.path.join(HERE, 'bgm')
    if not os.path.isdir(d): return None
    files = sorted(f for f in os.listdir(d) if f.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')))
    if not files: return None
    want = ep.get('bgm')
    if want:
        for f in files:
            if want.lower() in f.lower(): return os.path.join(d, f)
    try: idx = int((ep.get('date') or '2026-01-01').replace('-', '')) % len(files)
    except Exception: idx = 0
    return os.path.join(d, files[idx])

def make_thumb(EP, out):
    """thumb.html 에 데이터 주입 → out (jpg, 2MB 이하)"""
    if not EP.get('thumb'): return None
    html = io.open('thumb.html', encoding='utf-8').read().replace('__FONT_DIR__', font_dir_url())
    html = html.replace('<script>', '<script>window.EP=' + json.dumps(EP, ensure_ascii=False) + ';</script><script>', 1)
    io.open(W('render_thumb.html'), 'w', encoding='utf-8').write(html)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    r = subprocess.run(['node', 'thumb.js', W('render_thumb.html'), out], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0: print('썸네일 실패:', (r.stderr or r.stdout)[-300:]); return None
    if os.path.getsize(out) > 2 * 1024 * 1024:
        run(['ffmpeg', '-y', '-i', out, '-q:v', '5', out])
    return out

if __name__ == '__main__':
    if len(sys.argv) < 3: raise SystemExit(__doc__)
    mode, path = sys.argv[1], sys.argv[2]
    ep = load_episode(path)
    if mode == 'prep': prep(ep, path)
    elif mode == 'render': render(ep, path)
    elif mode == 'thumb':
        EP = dict(ep); EP['logos'] = logos_data_uri()
        print(make_thumb(EP, out_paths(ep, path)[1]))
    else: raise SystemExit(__doc__)
