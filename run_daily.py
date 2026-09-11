# -*- coding: utf-8 -*-
"""
야구자판기 하루 자동 실행 (윈도우 작업 스케줄러가 07:30 에 실행)
  순위 읽기 → 콘티(episodes/오늘_순위.json = 야구순위, 오늘_이슈.json = 야구이슈) 대기
  → 각각 음성 → 영상(상위 폴더 영상\\날짜\\번호_팀.mp4) → 비공개 업로드 → 신호 파일 감시 → 안전 종료 시각에 PC 종료

옵션:  --series rank|issue (야구순위/야구이슈 전용 — 그 시리즈 콘티만, 신호·오늘.txt 는 시리즈 폴더)  --now (시간과 상관없이 바로)  --latest (오늘 콘티 없으면 최근 콘티로)  --no-upload  --no-shutdown  --no-fetch  --no-tts
        --episode 파일경로 (콘티 대기 생략, 여러 개 가능)
신호 파일(상위 폴더 야구자판기\\):
  업로드.txt  만들어 둔 영상을 유튜브에 올림. 비어 있으면 전부(비공개), "1"/"2" 면 그 번호만, "공개" 가 들어 있으면 바로 공개로
  공개.txt    올라간 영상을 공개로 전환. 비어 있으면 전부, "1" 또는 "2" 면 그 번호만
  재생성.txt  내용이 비어 있으면 전부, "1"/"2" 면 그 번호만 다시 만듦 ("1 lines=3,7" 이면 그 줄 음성만 다시)
  메타.txt    이미 올린 영상의 제목·설명·태그를 콘티 youtube 항목으로 교체(재업로드 없음). 비어 있으면 전부, "1"/"2" 면 그 번호만
  종료.txt / 절전.txt
설정.txt 의 AUTO_UPLOAD=1 이면 만들자마자 비공개로 자동 업로드(기본 0: 업로드.txt 신호를 기다림)
상태는 상위 폴더의 오늘.txt 에 한국어로 기록.
"""
import os, sys, io, json, time, datetime, subprocess, traceback, glob, re

def open_cfg(path='설정.txt'):
    """설정.txt 열기 — 메모장이 ANSI(cp949)로 저장해도 읽히게 utf-8 → cp949 순서로 시도"""
    import io as _io
    for enc in ('utf-8-sig', 'cp949', 'euc-kr'):
        try:
            f = _io.open(path, encoding=enc); f.read(); f.seek(0); return f
        except UnicodeDecodeError:
            try: f.close()
            except Exception: pass
    return _io.open(path, encoding='utf-8-sig', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
BASE = os.path.abspath(os.path.join(HERE, '..'))
SIG = lambda n: os.path.join(BASE, n)
STATUS_TXT = os.path.join(BASE, '오늘.txt')
ARGS = sys.argv[1:]
# 콘티 날짜 = '올리는 날'. 저녁(설정 NIGHT_HOUR, 기본 18시) 이후에 돌리면 그날 경기 결과로 '다음 날' 콘티를 만드는 것이므로 날짜를 하루 넘긴다.
def _cfg(k, d=''):
    try:
        for line in open_cfg():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line and line.split('=', 1)[0].strip() == k: return line.split('=', 1)[1].strip()
    except Exception: pass
    return d
_now = datetime.datetime.now()
NIGHT = _now.hour >= int(_cfg('NIGHT_HOUR', '18'))
TODAY = (_now.date() + datetime.timedelta(days=1 if NIGHT else 0)).isoformat()
# 시리즈: --series rank(야구순위) / issue(야구이슈). 시리즈 전용 실행이면 콘티는 episodes/날짜_순위.json 처럼 하나만 다루고,
# 신호 파일과 오늘.txt 는 그 시리즈 폴더(야구자판기\야구순위\)에서 읽고 쓴다. 시리즈 없이 실행하면 순위·이슈 둘 다.
SERIES_CODES = {'rank': ('야구순위', '순위'), 'issue': ('야구이슈', '이슈')}
SERIES = [ARGS[i + 1] for i, a in enumerate(ARGS) if a == '--series' and i + 1 < len(ARGS) and ARGS[i + 1] in SERIES_CODES]
EPS = [ARGS[i + 1] for i, a in enumerate(ARGS) if a == '--episode' and i + 1 < len(ARGS)]
if not EPS:
    slots = [SERIES_CODES[c][1] for c in SERIES] or ['순위', '이슈']
    EPS = [f'episodes/{TODAY}_{k}.json' for k in slots]
    if not SERIES:   # 옛 이름(_1, _2)으로 된 콘티만 있으면 그걸 쓴다
        legacy = [f'episodes/{TODAY}_1.json', f'episodes/{TODAY}_2.json']
        if not any(os.path.exists(p) for p in EPS) and any(os.path.exists(p) for p in legacy): EPS = legacy
if len(SERIES) == 1:
    SERIES_DIR = os.path.join(BASE, SERIES_CODES[SERIES[0]][0]); os.makedirs(SERIES_DIR, exist_ok=True)
    SIG = lambda n: os.path.join(SERIES_DIR, n)
    STATUS_TXT = os.path.join(SERIES_DIR, '오늘.txt')
    print(f'[{SERIES_CODES[SERIES[0]][0]}] 전용 실행 — 콘티 {EPS[0]}, 신호·오늘.txt 는 {SERIES_DIR}')
if NIGHT: print(f'저녁 실행 → 내일({TODAY}) 콘티로 만듭니다 (오늘 경기 결과 기준)')
STATE_PATH = f'status/state_{TODAY}' + (('_' + SERIES[0]) if len(SERIES) == 1 else '') + '.json'   # 저장소에 올려서 다른 PC 에서도 오늘 상태를 이어받는다
for d in ('data', 'episodes', 'work', 'work/voice', 'status', 'signals'): os.makedirs(d, exist_ok=True)
import build   # 결과물 경로 계산(영상/날짜/번호_팀.mp4)

def cfg():
    c = {}
    for line in open_cfg():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1); c[k.strip()] = v.strip()
    return c
CFG = cfg()
REPO_GIT = os.path.isdir(os.path.join(HERE, '.git'))   # 깃허브 저장소로 연결돼 있으면 pull/push 사용
_last_push = 0.0

def git(*args, timeout=90):
    try:
        return subprocess.run(['git'] + list(args), cwd=HERE, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    except Exception:
        return None

def git_pull(quiet=True):
    """깃허브와 맞춘다: 이 PC 에서 바뀐 파일(Claude 가 PC 연결로 넣은 것)은 먼저 올리고, 최신을 받아온다 (실패해도 계속 진행)"""
    if not REPO_GIT: return False
    try: subprocess.run([sys.executable, '-X', 'utf8', 'sync_assets.py'], cwd=HERE, capture_output=True, timeout=120)
    except Exception: pass
    git('add', '-A')
    git('commit', '-q', '-m', f'pc update {now()}')
    r = git('pull', '--rebase', '-q')
    if r is not None and r.returncode == 0:
        git('push', '-q')
    try:   # 사진 폴더(선수이미지, 야구이슈\재료\사진) <-> assets\ 동기화 (깃으로 받은 사진을 바깥 폴더로, 바깥 새 사진을 assets 로)
        subprocess.run([sys.executable, '-X', 'utf8', 'sync_assets.py'], cwd=HERE, capture_output=True, timeout=120)
    except Exception: pass
    if r is None or r.returncode != 0:
        if not quiet: log('깃허브 받기 실패: ' + ((r.stderr if r else '') or '')[-160:])
        return False
    return True

def git_push_status(force=False):
    """오늘.txt 를 저장소 status/ 에 올려서 PC 연결 없이도 상태를 볼 수 있게 (1분에 한 번)"""
    global _last_push
    if not REPO_GIT: return
    if not force and time.time() - _last_push < 60: return
    _last_push = time.time()
    try:
        os.makedirs('status', exist_ok=True)
        import shutil; sname = '오늘' + (('_' + SERIES[0]) if len(SERIES) == 1 else '') + '.txt'; shutil.copyfile(STATUS_TXT, os.path.join('status', sname))
        git('add', 'status/' + sname, STATE_PATH)
        git('commit', '-q', '-m', f'status {TODAY} {now()}')
        git('push', '-q')
    except Exception: pass
SAFETY = CFG.get('SAFETY_SHUTDOWN', '12:00')
WAIT_EPISODE_MIN = int(CFG.get('WAIT_EPISODE_MIN', '45'))
AUTO_UPLOAD = CFG.get('AUTO_UPLOAD', '0').strip() == '1'

# ---------- 상태 ----------
state = {'date': TODAY, 'step': '', 'videos': {}, 'built': {}, 'log': []}   # videos: 업로드된 것 {"1": {"id","privacy","title"}}, built: 만들어 둔 것 {"1": {"video","ep"}}
if os.path.exists(STATE_PATH):
    try: state.update(json.load(io.open(STATE_PATH, encoding='utf-8')))
    except Exception: pass

def now(): return datetime.datetime.now().strftime('%H:%M:%S')
def log(msg, step=None):
    line = f'[{now()}] {msg}'
    print(line, flush=True)
    state['log'].append(line); state['log'] = state['log'][-100:]
    if step: state['step'] = step
    json.dump(state, io.open(STATE_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    write_status()

def write_status():
    lines = [f'날짜: {TODAY}', f'단계: {state.get("step")}', '']
    for k, b in sorted(state.get('built', {}).items()):
        lines.append(f'영상 {k} 파일: {b.get("video","")}')
    for k, v in sorted(state['videos'].items()):
        lines.append(f'영상 {k} 유튜브: {v.get("title","")}  https://youtu.be/{v["id"]}  ({v.get("privacy")})')
    if not state['videos'] and not state.get('built'): lines.append('영상: 아직 없음')
    if state.get('built') and not AUTO_UPLOAD:
        lines.append('→ 영상 폴더에서 확인한 뒤 업로드.txt 신호를 주면 유튜브에 올립니다')
    lines += ['', '기록:'] + state['log'][-30:]
    io.open(STATUS_TXT, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    git_push_status()

def sh(cmd, timeout=1800):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    return r.returncode, (r.stdout or '') + (r.stderr or '')
def py(*a, **k): return sh([sys.executable, '-X', 'utf8'] + list(a), **k)
def key_of(ep_path):
    stem = os.path.splitext(os.path.basename(ep_path))[0]
    return stem.rsplit('_', 1)[-1] if '_' in stem else stem

# ---------- 단계 ----------
def step_fetch():
    if '--no-fetch' in ARGS: log('순위 읽기 생략(--no-fetch)', '순위'); return True
    for i in range(3):
        rc, out = sh(['node', 'fetch_rank.js'], timeout=300)
        if rc == 0 and os.path.exists('data/rank_latest.json'):
            log('순위 읽기 완료', '순위')
            rc2, out2 = sh(['node', 'fetch_news.js'], timeout=400)
            log('뉴스 헤드라인 수집 완료' if rc2 == 0 else '뉴스 수집 실패(콘티는 순위만으로 진행): ' + out2.strip()[-150:])
            rc3, out3 = sh(['node', 'fetch_schedule.js'], timeout=300)   # 오늘·내일 경기 일정 + 예고 선발투수
            log('경기 일정·선발 수집 완료' if rc3 == 0 else '일정 수집 실패(무시): ' + out3.strip()[-150:])
            return True
        log(f'순위 읽기 실패({i + 1}/3): {out.strip()[-200:]}')
        time.sleep(120)
    return False

def valid_episode(p):
    try:
        ep = json.load(io.open(p, encoding='utf-8-sig'))
        ok = len(ep.get('lines', [])) >= 5 and len(ep.get('scenes', [])) >= 2 and all('narr' in l and 'sub' in l for l in ep['lines'])
        return ok, ep
    except Exception:
        return False, None

def latest_episodes():
    """episodes 폴더에서 가장 최근 날짜의 콘티 파일들"""
    cand = sorted(f for f in glob.glob(os.path.join('episodes', '*.json')) if re.match(r'\d{4}-\d{2}-\d{2}_\d+\.json$', os.path.basename(f)))
    if not cand: return []
    latest = os.path.basename(cand[-1])[:10]
    return sorted(f.replace('\\', '/') for f in cand if os.path.basename(f).startswith(latest))

def step_wait_episodes():
    global EPS
    if '--latest' in ARGS and not any(os.path.exists(p) for p in EPS):
        alt = latest_episodes()
        if alt:
            log(f'(--latest) 오늘({TODAY}) 콘티가 없어 가장 최근 콘티 사용: {", ".join(alt)}')
            EPS = alt
    if not any(os.path.exists(p) for p in EPS):
        log(f'오늘({TODAY}) 콘티가 아직 없어요. Claude 에게 "오늘 콘티 써줘" 라고 하면 episodes/{TODAY}_1.json, _2.json 이 들어옵니다')
    wait_min = WAIT_EPISODE_MIN
    log(f'콘티 대기: {", ".join(EPS)} (최대 {wait_min}분)', '콘티대기')
    end = time.time() + wait_min * 60
    while time.time() < end:
        ready = [p for p in EPS if os.path.exists(p) and valid_episode(p)[0]]
        if len(ready) == len(EPS):
            time.sleep(3); log('콘티 도착', '콘티'); return EPS
        if check_signals(during_build=True) == 'stop': return []
        time.sleep(20); git_pull()
    ready = [p for p in EPS if os.path.exists(p) and valid_episode(p)[0]]
    if ready: log(f'콘티 {len(ready)}개만 도착, 그것만 진행', '콘티'); return ready
    log('콘티가 제시간에 오지 않아 오늘은 건너뜀', '건너뜀'); return []

def step_build(ep_path, only_lines=None):
    k = key_of(ep_path)
    log(f'[{k}] 음성 생성 시작' + (f' (줄 {only_lines} 만 다시)' if only_lines else ''), '음성')
    rc, out = py('build.py', 'prep', ep_path)
    if rc: log(f'[{k}] prep 실패: ' + out[-300:], '실패'); return None
    if '--no-tts' in ARGS:
        log(f'[{k}] 음성 생성 생략(--no-tts) — 자막 타이밍만 다시 맞춤')
        rc, out = py('qa_voice.py', '--check', timeout=900)
        if rc: log(f'[{k}] 자막 맞춤 오류(무시): ' + out[-200:])
    else:
        args = ['tts.py'] + ([f'--only={only_lines}'] if only_lines else [])
        rc, out = py(*args, timeout=1200)
        if rc: log(f'[{k}] 음성 실패: ' + out[-300:], '실패'); return None
        # 음성 검수: 톤·속도 이탈 줄 다시 합성, 자막 타이밍 정밀 맞춤 (qa_voice.py)
        log(f'[{k}] 음성 검수 시작', '검수')
        rc, out = py('qa_voice.py', timeout=1500)
        tail = [l for l in out.strip().splitlines() if l.strip()][-3:]
        if rc: log(f'[{k}] 음성 검수 오류(무시하고 진행): ' + out[-300:])
        else: log(f'[{k}] 음성 검수: ' + ' | '.join(tail))
    ok, ep = valid_episode(ep_path)
    n = len(ep['lines'])
    vdir = build.voice_dir(build.ep_key(ep_path))
    missing = [i for i in range(n) if not os.path.exists(os.path.join(vdir, f'{i:02d}.mp3'))]
    if missing: log(f'[{k}] 음성 파일 누락 {missing}', '실패'); return None
    log(f'[{k}] 영상 렌더 시작 (3~5분)', '영상')
    rc, out = py('build.py', 'render', ep_path, timeout=1800)
    if rc: log(f'[{k}] 렌더 실패: ' + out[-400:], '실패'); return None
    video, thumb, _ = build.out_paths(ep, ep_path)
    if not os.path.exists(video): log(f'[{k}] 영상 파일이 없음', '실패'); return None
    rc, d = sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', video])
    try: dur = float(d.strip())
    except Exception: dur = 0
    if not (25 <= dur <= 90): log(f'[{k}] 영상 길이 이상: {dur:.1f}초', '실패'); return None
    log(f'[{k}] 영상 완성 {dur:.1f}초 → {video}', '영상완료')
    return video

UPLOAD_ENABLED = CFG.get('UPLOAD_ENABLED', '1').strip() != '0'          # 설정 UPLOAD_ENABLED=0 → 이 PC 에서는 절대 업로드하지 않음(회사 PC 용)
UPLOAD_MIN_GAP_MIN = int(CFG.get('UPLOAD_MIN_GAP_MIN', '120'))               # 업로드 사이 최소 간격(분). 사람 손 속도처럼 보이게
UPLOAD_MAX_PER_DAY = int(CFG.get('UPLOAD_MAX_PER_DAY', '2'))

def upload_allowed(k):
    """업로드해도 되는지: 이 PC 허용 여부, 하루 편수, 직전 업로드와의 간격. 안 되면 이유를 돌려준다"""
    if not UPLOAD_ENABLED: return '이 PC 는 업로드 금지(설정 UPLOAD_ENABLED=0). 집 PC 에서 올리세요'
    if len(state['videos']) >= UPLOAD_MAX_PER_DAY and k not in state['videos']: return f'오늘 업로드 {UPLOAD_MAX_PER_DAY}편 한도'
    last = state.get('last_upload_ts', 0)
    gap = (time.time() - last) / 60
    if last and gap < UPLOAD_MIN_GAP_MIN: return f'직전 업로드 후 {int(gap)}분 — {UPLOAD_MIN_GAP_MIN}분 지나면 자동으로 올립니다'
    return ''

def step_upload(ep_path, video, privacy='private'):
    k = key_of(ep_path)
    if '--no-upload' in ARGS: log(f'[{k}] 업로드 생략(--no-upload)', '업로드생략'); return None
    old = state['videos'].get(k, {}).get('id')
    if old:
        # 절대 삭제·재업로드하지 않는다(채널 정지 원인). 이미 올라간 영상은 제목·설명만 콘티대로 갱신
        rc, out = py('upload.py', 'update', old, ep_path)
        log(f'[{k}] 이미 올라간 영상 https://youtu.be/{old} — 재업로드 안 함, 제목·설명만 갱신' + ('' if not rc else ' 실패: ' + out[-150:]))
        return old
    why = upload_allowed(k)
    if why:
        q = state.setdefault('upload_queue', [])
        if not any(x['ep'] == ep_path for x in q): q.append({'ep': ep_path, 'video': video, 'privacy': privacy})
        log(f'[{k}] 업로드 보류: {why}', '업로드대기'); return None
    rc, out = py('upload.py', 'upload', video, ep_path, privacy, timeout=1200)
    vid = None
    for line in out.splitlines():
        if line.startswith('VIDEO_ID'): vid = line.split()[1]
    if rc or not vid: log(f'[{k}] 업로드 실패: ' + out[-300:], '실패'); return None
    ok, ep = valid_episode(ep_path)
    state['videos'][k] = {'id': vid, 'privacy': privacy, 'title': ep.get('youtube', {}).get('title', ''), 'ep': ep_path}
    state['last_upload_ts'] = time.time()
    log(f'[{k}] {"공개" if privacy == "public" else "비공개"} 업로드 완료 https://youtu.be/{vid}', '업로드완료')
    thumb = build.out_paths(ep, ep_path)[1]
    if os.path.exists(thumb):
        rc, out = py('upload.py', 'thumb', vid, thumb, timeout=300)
        log(f'[{k}] 썸네일 등록' if not rc else f'[{k}] 썸네일 등록 실패: ' + out[-200:])
    return vid

def flush_upload_queue():
    """보류된 업로드를 간격이 지났을 때 하나씩 처리"""
    q = state.get('upload_queue') or []
    if not q: return
    item = q[0]
    if upload_allowed(key_of(item['ep'])): return
    q.pop(0)
    if os.path.exists(item['video']): step_upload(item['ep'], item['video'], item.get('privacy', 'private'))

def after_build(ep_path, video):
    k = key_of(ep_path)
    state.setdefault('built', {})[k] = {'video': video, 'ep': ep_path}
    if '--no-upload' in ARGS: log(f'[{k}] 업로드 생략(--no-upload)', '영상완료'); return
    if k in state['videos']:
        log(f'[{k}] 이미 유튜브에 올라간 편이라 다시 올리지 않습니다(삭제·재업로드 금지). 새 영상은 폴더에만 저장', '영상완료'); return
    if AUTO_UPLOAD:
        step_upload(ep_path, video)
    else:
        log(f'[{k}] 영상 준비 완료. 확인 후 업로드.txt 신호를 주면 올립니다', '업로드대기')

def make_all(paths):
    for p in paths:
        video = step_build(p)
        if video: after_build(p, video)

# ---------- 신호 ----------
def take(name):
    """신호 파일을 읽고 지운다. 상위 폴더(야구자판기\\) 와 저장소 signals\\ 둘 다 확인"""
    for p in (SIG(name), os.path.join(HERE, 'signals', name)):
        if not os.path.exists(p): continue
        try: body = io.open(p, encoding='utf-8-sig').read().strip()
        except Exception: body = ''
        if p.startswith(os.path.join(HERE, 'signals')):
            # 저장소 신호는 같은 내용을 두 번 처리하지 않도록 기록하고, 처리 후 저장소에서도 지운다
            key = f'{name}:{body}'
            if key in state.setdefault('signals_done', []): continue
            state['signals_done'].append(key); state['signals_done'] = state['signals_done'][-50:]
            if REPO_GIT:
                git('rm', '-q', '--cached', p); 
                try: os.remove(p)
                except Exception: pass
                git('commit', '-q', '-m', f'signal {name} done'); git('push', '-q')
        else:
            try: os.remove(p)
            except Exception: pass
        return body.split('\n')[0].strip() if body else 'all'
    return None

def targets(sel):
    keys = sorted(state['videos'].keys())
    if sel in ('all', ''): return keys
    return [k for k in keys if k in sel.replace(',', ' ').split()]

def check_signals(during_build=False):
    if take('종료.txt') is not None: log('종료 신호 → PC 종료', '종료'); shutdown('shutdown'); return 'stop'
    if take('절전.txt') is not None: log('절전 신호 → 절전', '절전'); shutdown('sleep'); return 'stop'
    if during_build: return None
    sel = take('업로드.txt')
    if sel is not None:
        # 형식: "" | "1" | "2" | "1 2" | "공개" | "1 공개"  (공개 가 있으면 바로 공개로 올림)
        privacy = 'public' if '공개' in sel else 'private'
        keys = [k for k in sorted(state.get('built', {}).keys()) if sel in ('all', '') or k in sel.replace('공개', ' ').replace(',', ' ').split()]
        if not keys: log('업로드할 영상이 없음(먼저 만들어져 있어야 해요)')
        for k in keys:
            b = state['built'][k]
            if not os.path.exists(b['video']): log(f'[{k}] 영상 파일이 없음: {b["video"]}'); continue
            log(f'[{k}] 업로드 신호 → {"공개" if privacy == "public" else "비공개"} 업로드', '업로드')
            step_upload(b['ep'], b['video'], privacy)
    sel = take('공개.txt')
    if sel is not None:
        for k in targets(sel):
            v = state['videos'][k]
            rc, out = py('upload.py', 'publish', v['id'])
            if rc: log(f'[{k}] 공개 전환 실패: ' + out[-200:])
            else: v['privacy'] = 'public'; log(f'[{k}] 공개 전환 완료', '공개')
        if not state['videos']: log('공개할 영상이 없음')
    sel = take('메타.txt')
    if sel is not None:
        # 이미 올린 영상의 제목·설명·태그를 콘티 파일 youtube 항목으로 교체(재업로드 없음). 비어 있으면 전부, "1"/"2" 면 그 번호만
        for k in targets(sel):
            v = state['videos'][k]; b = state.get('built', {}).get(k) or {}
            ep_path = b.get('ep') or next((p for p in EPS if key_of(p) == k), None)
            if not ep_path or not os.path.exists(ep_path): log(f'[{k}] 콘티 파일을 못 찾아 메타 갱신 불가'); continue
            rc, out = py('upload.py', 'update', v['id'], ep_path)
            if rc: log(f'[{k}] 제목·설명 갱신 실패: ' + out[-200:])
            else: log(f'[{k}] 제목·설명 갱신 완료', '메타')
        if not state['videos']: log('갱신할 영상이 없음')
    sel = take('재생성.txt')
    if sel is not None:
        # 형식: "all" | "1" | "1 2" | "1 lines=3,7" (그 줄 음성만 다시 뽑고 렌더)
        log(f'재생성 신호({sel}) → 다시 만들기', '재생성')
        import re as _re
        m = _re.search(r'lines=([\d,\s]+)', sel)
        only = ','.join(_re.findall(r'\d+', m.group(1))) if m else None
        rest = _re.sub(r'lines=[\d,\s]+', ' ', sel) if m else sel
        toks = rest.replace(',', ' ').split() if sel != 'all' else []
        keys = toks or [key_of(p) for p in EPS]
        for k in keys:
            ep_path = next((p for p in EPS if key_of(p) == k), None)
            if not ep_path or not os.path.exists(ep_path): log(f'[{k}] 콘티 파일 없음'); continue
            video = step_build(ep_path, only)
            if video: after_build(ep_path, video)
    return None

def shutdown(kind):
    if '--no-shutdown' in ARGS: log('(--no-shutdown) 종료 안 함'); sys.exit(0)
    write_status()
    if kind == 'sleep': subprocess.Popen(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
    else: subprocess.Popen(['shutdown', '/s', '/t', '30', '/c', '야구자판기 작업 완료'])
    sys.exit(0)

def watch_loop():
    log(f'감시 시작 (안전 종료 {SAFETY})', state.get('step'))
    hh, mm = map(int, SAFETY.split(':'))
    last_pull = 0
    while True:
        if time.time() - last_pull > 60:
            git_pull(); last_pull = time.time()
        if check_signals() == 'stop': return
        flush_upload_queue()
        n = datetime.datetime.now()
        if (n.hour, n.minute) >= (hh, mm) and '--now' not in ARGS:
            log('안전 종료 시각 → PC 종료', '종료'); shutdown('shutdown'); return
        time.sleep(15)

# ---------- 메인 ----------
def main():
    try:
        if state['videos'] and '--now' not in ARGS:
            log('오늘 이미 업로드됨, 감시만 진행'); watch_loop(); return
        log('시작', '시작')
        if git_pull(quiet=False): log('깃허브에서 최신 프로그램·콘티 받음')
        if not step_fetch():
            log('순위를 못 읽어 오늘은 건너뜀', '건너뜀'); watch_loop(); return
        paths = EPS if '--episode' in ARGS else step_wait_episodes()
        if paths: make_all(paths)
        watch_loop()
    except SystemExit: raise
    except Exception:
        log('오류: ' + traceback.format_exc()[-600:], '오류'); watch_loop()

if __name__ == '__main__':
    main()
