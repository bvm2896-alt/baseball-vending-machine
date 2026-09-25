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

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

LEAD, TAIL, SUBLEAD = 0.25, 1.30, 0.05   # SUBLEAD: 자막을 말보다 살짝(0.05초) 먼저 — 거의 동시
FPS = 15   # (옛 값, 지금은 설정.txt VIDEO_FPS 사용)
WORK = os.environ.get('KBO_WORK', 'work')            # 중간 파일(프레임, 임시 html) 폴더. 시리즈 창마다 다르게(work\순위, work\이슈) 주면 두 시리즈를 동시에 만들 수 있다
VOICE_ROOT = 'work'                                  # 편별 음성 폴더(voice_<콘티이름>)는 시리즈와 상관없이 늘 여기
OUT_ROOT = os.path.join(HERE, '..', '영상')           # 결과물: 영상/2026-09-06/1_두산.mp4
def _cfg_raw(k, default=''):
    try:
        for line in open_cfg(os.path.join(HERE, '설정.txt')):
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

def topic_label(ep):
    """파일 이름용 주제(9/24 사용자 지시: 이슈5_KT 가 아니라 이슈5_한일전미리보기 처럼 주제로).
    콘티 "topic" → 없으면 썸네일 큰 글씨 첫 줄 → 그것도 없으면 예전처럼 팀 이름"""
    clean = lambda t: re.sub(r'[^0-9A-Za-z가-힣]', '', str(t or ''))[:24]
    t = clean(ep.get('topic'))
    if not t:
        big = str((ep.get('thumb') or {}).get('big') or '').split('\n')[0]
        t = clean(big)
    return t or team_label(ep)

def game_date(ep):
    """영상이 다루는 '경기 날짜'(YYYY-MM-DD). 콘티 gameDate 가 있으면 그것, 없으면 콘티 날짜 하루 전
    (월요일 아침 영상 = 일요일 경기). 화요일 콘티는 전날 경기가 없으니 콘티 날짜 그대로."""
    g = ep.get('gameDate')
    if g: return g
    d = ep.get('date') or datetime.date.today().isoformat()
    try:
        dt = datetime.date.fromisoformat(d)
        if dt.weekday() != 1: dt -= datetime.timedelta(days=1)   # 1 = 화요일
        return dt.isoformat()
    except Exception: return d

SERIES_BY_SLOT = {'순위': '야구순위', '이슈': '야구이슈', '분석': '야구분석', '롱폼': '야구롱폼', '1': '야구순위', '2': '야구이슈'}   # 하루 콘티 슬롯 → 시리즈 폴더 (콘티에 "series" 를 적으면 그게 우선)

def series_of(ep, ep_path):
    """결과물을 나눠 담을 시리즈 폴더 이름: 콘티의 series → 없으면 슬롯 번호(1=야구순위, 2=야구이슈)"""
    if ep.get('series'): return str(ep['series']).strip()
    stem = os.path.splitext(os.path.basename(ep_path))[0]
    key = stem.rsplit('_', 1)[-1] if '_' in stem else stem
    return SERIES_BY_SLOT.get(key, '야구순위')

def out_paths(ep, ep_path):
    r"""(영상 mp4, 썸네일 jpg, 유튜브 제목설명 txt) 경로. 폴더는 <결과물 루트>/<시리즈>/경기날짜/, 이름은 번호_팀
       결과물 루트: 설정 OUTPUT_DIR(드라이브) 또는 상위 폴더. 상위 폴더일 땐 야구자판기\야구순위\영상\날짜 처럼 시리즈 폴더 안의 영상\ 에 둔다"""
    stem = os.path.splitext(os.path.basename(ep_path))[0]
    key = stem.rsplit('_', 1)[-1] if '_' in stem else stem
    date = game_date(ep)
    series = series_of(ep, ep_path)
    if os.path.abspath(OUT_ROOT) == os.path.abspath(os.path.join(HERE, '..', '영상')):
        d = os.path.abspath(os.path.join(HERE, '..', series, '영상', date))       # 드라이브 없을 때: 야구자판기\<시리즈>\영상\날짜
    else:
        d = os.path.abspath(os.path.join(OUT_ROOT, series, date))                # 드라이브: 야구자판기_영상확인\<시리즈>\날짜
    base = os.path.join(d, f'{key}_{topic_label(ep)}')
    return base + '.mp4', base + '_썸네일.jpg', base + '_유튜브.txt'

# 구단 코드 → KBO_logos 폴더의 파일 이름
LOGO_FILES = {'HT': '기아', 'SS': '삼성', 'LG': 'LG', 'OB': '두산', 'KT': 'KT',
              'NC': 'NC', 'LT': '롯데', 'SK': 'SSG', 'HH': '한화', 'WO': '키움'}
LOGO_DIRS = [os.path.join(HERE, '..', 'KBO_logos'), os.path.join(HERE, 'KBO_logos'), os.path.join(HERE, 'logos')]

# 야구이슈 편 사진: 콘티 장면의 img("김도영_번트.jpg" 또는 확장자 없이 "김도영_번트")를 아래 순서로 찾는다.
#   1) 야구자판기\야구이슈\재료\사진\<콘티 이름>\   (예: 사진\2026-09-11_이슈\ — 그 편 전용)
#   2) 야구자판기\선수이미지\                        (선수·감독 프로필 — 사용자가 계속 모아 두는 공용 폴더. 파일명 = 이름, 예: 김도영.jpg)
#   3) 야구자판기\야구이슈\재료\사진\공용\ , 야구자판기\야구이슈\재료\사진\  (옛 위치)
# 없으면 템플릿이 로고로 대신 그린다.
PHOTO_ROOT = os.path.join(HERE, '..', '야구이슈', '재료', '사진')
PHOTO_ROOT2 = os.path.join(HERE, '..', '야구분석', '재료', '사진')   # 야구분석 편 전용 사진 (9/15)
PLAYER_IMG_DIR = os.path.join(HERE, '..', '선수이미지')
PHOTO_EXTS = ('.jpg', '.jpeg', '.png', '.webp')
ASSETS = os.path.join(HERE, 'assets')   # 깃허브로 주고받는 사진 사본 (sync_assets.py 가 바깥 폴더와 맞춘다)
def photo_dirs(ep_key_name=''):
    return [os.path.join(PHOTO_ROOT, ep_key_name) if ep_key_name else '', os.path.join(PHOTO_ROOT2, ep_key_name) if ep_key_name else '', PLAYER_IMG_DIR, os.path.join(PHOTO_ROOT, '공용'), PHOTO_ROOT, PHOTO_ROOT2,
            os.path.join(ASSETS, '이슈사진', ep_key_name) if ep_key_name else '', os.path.join(ASSETS, '선수이미지'), os.path.join(HERE, 'photos')]

def is_long(ep):
    """롱폼 편인가 — series 가 '야구롱폼' 이면 가로(1920x1080)로 그린다(9/18)"""
    return str(ep.get('series', '')).strip() == '야구롱폼'

def canvas_of(ep):
    return (1920, 1080) if is_long(ep) else (1080, 1920)

def template_for(ep):
    """시리즈별 템플릿: 야구이슈 이고 template_issue.html 이 있으면 그것(화이트), 아니면 template.html(순위 편, 다크)"""
    ser = str(ep.get('series', '')).strip()
    if ser == '야구롱폼' and os.path.exists('template_long.html'):       # 9/18: 롱폼 전용(가로 1920x1080)
        return 'template_long.html'
    if ser == '야구분석' and os.path.exists('template_analysis.html'):   # 9/15: 분석 전용(팀 색 띠 리포트형)
        return 'template_analysis.html'
    if ser in ('야구이슈', '야구분석') and os.path.exists('template_issue.html'):
        return 'template_issue.html'
    return 'template.html'

def _photo_names(ep):
    """콘티 안의 모든 img 항목(장면·카드·목록 항목)을 모은다"""
    names = set()
    def walk(x):
        if isinstance(x, dict):
            v = x.get('img')
            if isinstance(v, str) and v.strip(): names.add(v.strip())
            for vv in x.values(): walk(vv)
        elif isinstance(x, list):
            for vv in x: walk(vv)
    walk(ep.get('scenes') or [])
    walk(ep.get('thumb') or {})
    return names

PHOTO_SIZES = {}   # 이름 → [가로, 세로] (photos_data_uri 가 채움, EP.photoSizes 로 템플릿에 전달)
# 선수이미지\ 는 하위 폴더로 나눠 둘 수 있다(9/14): KBO프로필\ · 국가대표프로필\ · 고등학교\(하현승·엄준상 같은 고교 선수) · 상황별\ (+ 그 외 폴더).
# 콘티 img 가 "국가대표프로필/김도영" 처럼 폴더를 지정하면 그 폴더에서만, "김도영" 이면 KBO프로필 → 국가대표프로필 → 고등학교 → 상황별 → 나머지 순으로 찾는다.
SUB_ORDER = ['KBO프로필', '국가대표프로필', '고등학교', '상황별']

def _search_dirs(d):
    out = [d]
    if os.path.isdir(d):
        subs = [x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x))]
        subs.sort(key=lambda x: (SUB_ORDER.index(x) if x in SUB_ORDER else len(SUB_ORDER), x))
        out += [os.path.join(d, x) for x in subs]
    return out

def find_photo(name, ep_path=None):
    """콘티에 적힌 사진 이름 → 실제 파일 경로(없으면 None). run_daily 의 사진 준비 확인도 이 함수를 쓴다(같은 규칙)."""
    dirs = [d for d in photo_dirs(ep_key(ep_path) if ep_path else '') if d]
    sub = ''
    key = str(name).replace('\\', '/')
    if '/' in key: sub, key = key.rsplit('/', 1)
    base = os.path.splitext(key)[0]
    for d0 in dirs:
        cands = [os.path.join(d0, sub)] if sub else _search_dirs(d0)
        for d in cands:
            if not os.path.isdir(d): continue
            for f in os.listdir(d):
                if f.lower() == key.lower() or os.path.splitext(f)[0].lower() == base.lower() and f.lower().endswith(PHOTO_EXTS):   # 대소문자 무시(kt_2021우승 = KT_2021우승)
                    return os.path.join(d, f)
    return None

def photos_data_uri(ep, ep_path=None):
    """콘티가 쓰는 사진만 data URI 로 (키 = 콘티에 적힌 이름 그대로). 큰 사진은 렌더 html 이 무거워지니 1600px 이하로 줄여 넣는다"""
    out = {}; sizes = PHOTO_SIZES
    names = _photo_names(ep)
    if not names: return out
    for name in names:
        base = os.path.splitext(str(name).replace('\\', '/').rsplit('/', 1)[-1])[0]
        found = find_photo(name, ep_path)
        if not found:
            print(f'경고: 사진 없음 "{name}" → 로고로 대신 표시 (야구이슈\\재료\\사진\\<콘티이름>\\ 또는 선수이미지\\ 에 넣어 주세요)')
            continue
        src = found
        ext0 = os.path.splitext(found)[1].lower()
        if ext0 != '.png':   # png 는 원본 그대로. webp 는 png 로(투명 배경이 있으면 지켜야 누끼 사진이 흐린 배경 없이 놓인다, 9/15), jpg 는 1600px jpg 로
            try:
                safe = re.sub(r'[^0-9A-Za-z가-힣_.-]', '_', base)
                if ext0 == '.webp':
                    tmp = W('photo_' + safe + '.png')
                    r = run(['ffmpeg', '-y', '-loglevel', 'error', '-i', found, '-vf', "scale='min(1600,iw)':-2", tmp])
                else:
                    tmp = W('photo_' + safe + '.jpg')
                    r = run(['ffmpeg', '-y', '-loglevel', 'error', '-i', found, '-vf', "scale='min(1600,iw)':-2", '-q:v', '3', tmp])
                if r.returncode == 0 and os.path.exists(tmp): src = tmp
            except Exception: pass
        ext = os.path.splitext(src)[1].lower()
        mime = 'image/png' if ext == '.png' else 'image/webp' if ext == '.webp' else 'image/jpeg'
        out[name] = f'data:{mime};base64,' + base64.b64encode(open(src, 'rb').read()).decode()
        # 원본 크기(템플릿이 작은 사진은 늘리지 않고 흐린 배경 위에 원본 크기로 놓는다) + 투명 배경 여부(변환된 파일 기준)
        try:
            pr = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,pix_fmt', '-of', 'csv=p=0', found])
            parts = pr.stdout.strip().split(',')
            w_, h_ = int(parts[0]), int(parts[1])
            pf = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=pix_fmt', '-of', 'csv=p=0', src]).stdout.strip().lower()
            alpha = 1 if re.search(r'^(rgba|bgra|argb|abgr|ya8|ya16|gbrap|pal8|yuva)', pf) else 0   # 투명 배경(누끼) → 템플릿이 흐린 배경 대신 단색 배경에 놓는다
            sizes[name] = [w_, h_, alpha]
            if min(w_, h_) < 500: print(f'참고: 사진 "{name}" 해상도 낮음({w_}x{h_}) → 화면에서 흐릿할 수 있음. 900px 이상 권장')
        except Exception: pass
    print(f'사진 {len(out)}/{len(names)}장 넣음')
    return out

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
    # 화면 오른쪽 위 날짜 = '올리는 날짜'(콘티 date, 제목 해시태그와 같은 날) — 2026-09-17 사용자 지시
    # 썸네일 날짜 배지·결과물 폴더는 그대로 '경기 날짜' 기준
    ep['dateLabel'] = (ep.get('date') or game_date(ep)).replace('-', '.')
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
            # 소수점("십이 점 삼팔", "오 점 영이")은 한자어가 맞다 — 점 뒤에 바로 숫자가 이어지면 넘어간다
            if m.group(2) == '점' and re.match(r' ?(영|일|이|삼|사|오|육|칠|팔|구)', t[m.end():]): continue
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
    d = os.path.join(VOICE_ROOT, 'voice_' + key) if key else os.path.join(VOICE_ROOT, 'voice')
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
    if ep_path:
        # 타입캐스트 웹(구독)에 붙여 넣을 대본: 줄 사이 빈 줄(문단 쉼) → 통째로 내려받아 <시리즈>\음성\<콘티이름>.mp3 로 두면 tts.py 가 줄별로 자른다
        try:
            drop = os.path.join(HERE, '..', series_of(ep, ep_path), '음성'); os.makedirs(drop, exist_ok=True)
            txt = '\n\n'.join(l.replace(' / ', ', ') for l in lines) + '\n'
            io.open(os.path.join(drop, ep_key(ep_path) + '_대본.txt'), 'w', encoding='utf-8').write(txt)
            print(f'대본 저장: {os.path.relpath(os.path.join(drop, ep_key(ep_path) + "_대본.txt"), os.path.join(HERE, ".."))}  (타입캐스트 웹에 붙여 넣고, 받은 mp3 를 같은 폴더에 {ep_key(ep_path)}.mp3 로)')
        except Exception as e: print('대본 저장 실패(무시):', e)

# ---------- render ----------
def dur_of(f):
    """영상/음성 길이(초). 파일이 깨져 있으면(N/A) 0"""
    try: return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).stdout.strip())
    except (ValueError, TypeError): return 0.0

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

GAP_OVERRIDE = None   # 9/24: 콘티 "gapScale" 가 있으면 그 편만 이 배율(설정.txt 보다 우선) — 사용자 "말 사이 텀이 너무 길다"
def gap_scale():
    """줄 사이 쉼 배율 (9/13 1.5배는 "텀이 너무 길어 지루" → 9/14 기본 1.25배). 설정.txt GAP_SCALE 로 조절, 콘티 gapScale 이 우선"""
    if GAP_OVERRIDE is not None: return max(0.3, float(GAP_OVERRIDE))
    try: return max(0.5, float(cfg_get('GAP_SCALE', '1.25')))
    except Exception: return 1.25
MAX_GAP = 0.6   # 어떤 쉼도 이보다 길지 않게(답답함 방지)

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
    return round(min(gap * gap_scale(), MAX_GAP), 2)

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
    # 9/21: 음성 폴더는 콘티 이름으로 정한다 — current.txt(마지막 prep) 를 따르면 다른 편 음성이 붙는다(하현승⑥에 드래프트 편 음성이 들어간 사고)
    io.open(W('current.txt'), 'w', encoding='utf-8').write(ep_key(ep_path))
    global GAP_OVERRIDE; GAP_OVERRIDE = ep.get('gapScale')
    lines = ep['lines']; N = len(lines)
    spd = float(cfg_get('SPEED', '1.12'))   # 말 자체 배속(9/14 "말은 빠르되 문단 사이 텀은 적절히" → 기본 1.12). 타입캐스트는 1.0x 로 뽑고 여기서 올린다. 설정.txt SPEED 로 조절
    # 9/18: 편마다 다르게 하고 싶을 때는 콘티에 "speed": 1.30 (설정.txt 는 건드리지 않는다).
    # 줄 사이 쉼(gap_after)은 이 배속과 무관하게 따로 넣으므로, 이 값만 올리면 '텀은 그대로, 말만 빨라진다'
    if ep.get('speed'):
        spd = float(ep['speed']); print(f'말 속도: 콘티 지정 {spd:.2f}배')
    # 1) 음성 확인 + 트리밍 (자르기는 atrim 필터로, 속도 조절은 그 다음에 → -to 가 느려진 소리 끝을 잘라먹지 않는다)
    clips, warns, seg_start, seg_rate = [], [], [], []
    retried = set()
    i = 0
    while i < N:
        src = VW(f'{i:02d}.mp3')
        if not os.path.exists(src): raise SystemExit(f'음성 없음: {src}')
        # 대사가 바뀌었는데 음성은 옛 대사면 그 줄만 다시 합성
        txt = src.replace('.mp3', '.txt')
        if os.path.exists(txt) and i not in retried:
            made = io.open(txt, encoding='utf-8').read().strip()
            if made != lines[i]['narr'].strip():
                print(f'음성 {i:02d} 은 옛 대사로 만든 것 → 다시 합성')
                retried.add(i)
                r = subprocess.run([sys.executable, '-X', 'utf8', 'tts.py', f'--only={i}'], capture_output=True, text=True, encoding='utf-8', errors='replace')
                if r.returncode != 0: print('  다시 합성 실패(옛 음성 그대로 사용):', (r.stdout + r.stderr)[-200:])
                else:
                    subprocess.run([sys.executable, '-X', 'utf8', 'qa_voice.py', '--check'], capture_output=True)   # 자막 경계 다시
        d, lead, tail = probe(src)
        ss, to = max(0, lead - 0.06), min(d, tail + 0.12)
        dst = VW(f't{i:02d}.wav')
        # 9/26: 줄에 "rate" 가 있으면 콘티 speed 와 상관없이 그 배속(구독 멘트 줄은 1.0 — 본문만 1.2배)
        rate = float(lines[i]['rate']) if lines[i].get('rate') else spd * pace_of(i, lines[i], N)
        gain = static_gain(src, ss, to)
        def cut(ss, to):
            af = f'atrim=start={ss:.3f}:end={to:.3f},asetpts=PTS-STARTPTS'
            # 9/18: 콘티에 "tight": true 인 줄은 문장 안의 긴 쉼("한국 야구가 .. 대만한테 ..")을 잘라 붙인다.
            # tightMs 로 남길 쉼 길이를 바꿀 수 있다(기본 0.12초). 줄과 줄 사이 쉼(gap_after)은 건드리지 않는다.
            if lines[i].get('tight'):
                keep = float(lines[i].get('tightMs', 120)) / 1000.0
                af += f',silenceremove=stop_periods=-1:stop_duration={keep:.3f}:stop_threshold=-36dB:detection=peak'
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
        if syl / (clips[-1] * rate) > 10.5:   # 9/14: 장운 1.1x 후킹 줄은 9~10음절/초가 정상이라 기준을 올림
            if i not in retried:
                # 잘린 음성으로 보임 → 그 줄만 자동으로 다시 만들고 한 번 더 시도
                print(f'음성 {i:02d} 이 글자 수에 비해 너무 짧아요 ({clips[-1]:.2f}s/{syl}음절) → 다시 합성')
                retried.add(i)
                r = subprocess.run([sys.executable, '-X', 'utf8', 'tts.py', f'--only={i}'], capture_output=True, text=True, encoding='utf-8', errors='replace')
                if r.returncode == 0:
                    clips.pop(); seg_start.pop(); seg_rate.pop(); continue
                print('  다시 합성 실패:', (r.stdout + r.stderr)[-300:])
            # 다시 못 만들면(웹에서 받은 음성·API 없음) 멈추지 말고 경고만 남기고 그대로 쓴다 — 사람이 듣고 그 줄만 다시 뽑는다
            warns.append(f'{i:02d} 글자 수 대비 짧음({clips[-1]:.2f}s/{syl}음절) — 잘렸는지 들어보세요')
            print(f'음성 {i:02d} 이 글자 수에 비해 짧아요 ({clips[-1]:.2f}s/{syl}음절) — 그대로 진행')
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
    EP = dict(ep); EP['subs'] = subs; EP['bounds'] = bounds; EP['logos'] = logos_data_uri(); EP['total'] = round(total, 2); EP['_path'] = ep_path
    EP['photos'] = photos_data_uri(ep, ep_path)  # 야구이슈 편 사진(없으면 빈 dict)
    EP['photoSizes'] = PHOTO_SIZES
    tpl = template_for(ep); print('템플릿:', tpl)
    html = io.open(tpl, encoding='utf-8').read().replace('__FONT_DIR__', font_dir_url())
    html = html.replace('<script>', '<script>window.EP=' + json.dumps(EP, ensure_ascii=False) + ';</script><script>', 1)
    io.open(W('render.html'), 'w', encoding='utf-8').write(html)
    json.dump({'total': round(total, 2), 'starts': st, 'durs': clips, 'gaps': gaps, 'bounds': bounds, 'subs': subs},
              io.open(W('timeline.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 5) 프레임 렌더 → 무음 영상 (설정.txt VIDEO_FPS 기본 60, VIDEO_SCALE 기본 1.3333 = 1440x2560 2K)
    fps = int(cfg_get('VIDEO_FPS', '60')); scale = cfg_get('VIDEO_SCALE', '1.3333')
    shutil.rmtree(W('frames'), ignore_errors=True)
    print(f'프레임 렌더 {fps}fps x{scale} ({round(total)}초) …')
    cw, ch = canvas_of(ep)
    fenv = dict(os.environ); fenv['FRAME_W'], fenv['FRAME_H'] = str(cw), str(ch)
    r = subprocess.run(['node', 'frames.js', str(round(total, 2)), W('silent.mp4'), str(fps), scale], capture_output=True, text=True, encoding='utf-8', errors='replace', env=fenv)
    if r.returncode != 0: print('프레임 렌더 1차 실패 → 동시작업 1 로 다시:\n' + ((r.stderr or '') + '\n' + (r.stdout or ''))[-1200:])
    elif r.stdout: print((r.stdout or '').strip().splitlines()[-1])
    vd = dur_of(W('silent.mp4')) if os.path.exists(W('silent.mp4')) else 0.0
    if r.returncode != 0 or vd < total * 0.95:
        # 조각 파일을 동시에 쓰다 깨진 경우(OneDrive 동기화 폴더에서 가끔) → 한 번 더, 이번엔 조각 없이 한 번에 그린다
        print(f'경고: 무음 영상이 깨졌거나 짧음({vd:.1f}s / {total:.1f}s) → 한 번 더 그립니다(동시작업 1)')
        try: os.remove(W('silent.mp4'))
        except Exception: pass
        r = subprocess.run(['node', 'frames.js', str(round(total, 2)), W('silent.mp4'), str(fps), scale, '1'], capture_output=True, text=True, encoding='utf-8', errors='replace', env=fenv)
        if r.returncode != 0 or not os.path.exists(W('silent.mp4')): raise SystemExit('프레임 렌더 실패(재시도):\n' + ((r.stderr or '') + '\n' + (r.stdout or ''))[-1500:])
        vd = dur_of(W('silent.mp4'))
        if vd < total * 0.95: raise SystemExit(f'영상 길이 부족: {vd:.1f}s / {total:.1f}s (재시도 후에도)')
    # 6) 합성 → 결과물 폴더(영상/날짜/번호_팀.mp4)
    out, thumb_path, yt_path = out_paths(ep, ep_path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    name = os.path.splitext(os.path.basename(ep_path))[0]
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
    if is_long(ep): append_endcard(EP, out)   # 9/20: 롱폼은 끝에 어두운 엔딩 카드(유튜브 최종 화면 자리)
    d = dur_of(out)
    thumb = make_thumb(EP, thumb_path)
    write_youtube_txt(ep, yt_path, d)
    srt_path = yt_path.replace('_유튜브.txt', '_자막.srt')
    if ep.get('chapters'): write_chapters(ep, st, yt_path)   # 9/18 롱폼: 설명란 챕터 타임스탬프
    write_srt(subs, srt_path)   # 9/15 SEO: 유튜브 업로드 때 자막 파일로 첨부 → 자동 자막보다 정확하게 검색 색인
    print(f'완료: {out} {d:.2f}초 (자막 {len(subs)}개, 장면 {len(ep["scenes"])}개) 썸네일 {thumb}')
    return out

def append_endcard(EP, out):
    """롱폼 mp4 끝에 어두운 엔딩 카드(설정 ENDCARD_SEC, 기본 12초)를 붙인다(9/20 사용자 지시).
       유튜브 '최종 화면'(구독·다음 영상)은 마지막 5~20초에 얹히는데, 본편 위에 얹히면 화면을 가린다 → 본편 뒤에 빈 화면을 둔다.
       endcard.html → png → 본편과 같은 코덱(h264 High/Level/픽셀형식/60fps, aac 44.1k mono)으로 12초를 만들고 concat 으로 재인코딩 없이 이어 붙인다."""
    sec = float(cfg_get('ENDCARD_SEC', '12'))
    if sec <= 0 or not os.path.exists('endcard.html'): return out
    html = io.open('endcard.html', encoding='utf-8').read().replace('__FONT_DIR__', font_dir_url())
    html = html.replace('<script>', '<script>window.EP=' + json.dumps({'lines': EP.get('lines', []), 'endTop': EP.get('endTop')}, ensure_ascii=False) + ';</script><script>', 1)
    io.open(W('render_endcard.html'), 'w', encoding='utf-8').write(html)
    png = W('endcard.png')
    env = dict(os.environ); env['THUMB_W'], env['THUMB_H'] = '2560', '1440'
    r = subprocess.run(['node', 'thumb.js', W('render_endcard.html'), png], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
    if r.returncode != 0 or not os.path.exists(png): print('엔딩 카드 그리기 실패(엔딩 없이 진행):', (r.stderr or r.stdout)[-200:]); return out
    # 본편 코덱 파라미터를 읽어 똑같이 맞춘다(안 맞으면 concat 복사가 깨진다)
    pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height,profile,level,pix_fmt,r_frame_rate', '-of', 'default=nw=1', out], capture_output=True, text=True).stdout
    kv = dict(l.split('=', 1) for l in pr.strip().splitlines() if '=' in l)
    w_, h_ = kv.get('width', '2560'), kv.get('height', '1440'); pix = kv.get('pix_fmt', 'yuvj420p'); lvl = kv.get('level', '51'); prof = (kv.get('profile') or 'High').lower()
    fps = kv.get('r_frame_rate', '60/1').split('/'); fps = str(int(round(float(fps[0]) / float(fps[1] or 1))))
    lvl = f'{int(lvl) // 10}.{int(lvl) % 10}' if lvl.isdigit() else lvl
    tail = W('endcard.mp4')
    r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', fps, '-i', png, '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', f'{sec:.2f}',
                        '-vf', f'scale={w_}:{h_},fade=t=in:st=0:d=0.6,format={pix}', '-c:v', 'libx264', '-profile:v', prof, '-level', lvl, '-pix_fmt', pix, '-r', fps, '-g', str(int(fps) * 2),
                        '-preset', 'medium', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '1', '-shortest', tail], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0: print('엔딩 카드 인코딩 실패(엔딩 없이 진행):', r.stderr[-200:]); return out
    lst = W('endcard_list.txt'); joined = W('with_endcard.mp4')
    io.open(lst, 'w', encoding='utf-8').write("file '" + os.path.abspath(out).replace("'", "'\\''") + "'\nfile '" + os.path.abspath(tail).replace("'", "'\\''") + "'\n")
    r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', joined], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0 or not os.path.exists(joined) or dur_of(joined) < dur_of(out) + sec * 0.9:
        print('엔딩 카드 붙이기 실패(엔딩 없이 진행):', (r.stderr or '')[-200:]); return out
    shutil.move(joined, out); print(f'엔딩 카드 {sec:.0f}초 붙임')
    return out

def write_chapters(ep, st, yt_path):
    """롱폼 설명란에 붙일 챕터 목록을 유튜브 txt 끝에 덧붙인다.
       유튜브 챕터 규칙: 첫 줄이 반드시 0:00, 챕터 3개 이상, 각 10초 이상."""
    ch = ep.get('chapters') or []
    if len(ch) < 3: return None
    def ts(t):
        t = max(0.0, float(t)); m = int(t // 60); s_ = int(t % 60)
        return f'{m}:{s_:02d}'
    rows, prev = [], -99.0
    for i, c in enumerate(ch):
        k = int(c.get('from', 0))
        t = 0.0 if i == 0 else float(st[k]) if k < len(st) else prev + 10
        if i and t < prev + 10: t = prev + 10
        prev = t
        rows.append(f'{ts(t)} {c.get("title", "")}'.rstrip())
    try: cur = io.open(yt_path, encoding='utf-8').read()
    except Exception: cur = ''
    io.open(yt_path, 'w', encoding='utf-8').write(cur.rstrip() + '\n\n[챕터 — 설명란 맨 아래에 그대로 붙여넣기]\n' + '\n'.join(rows) + '\n')
    print('챕터', len(rows), '개')
    return rows

def cut_chapter(ep, ep_path, which):
    """롱폼 콘티의 챕터 하나를 쇼츠 콘티로 떼어낸다(9/18).
       - lines/scenes 를 그 구간만 잘라 startLine 을 0 부터 다시 매긴다
       - 챕터의 short 블록(thumb/youtube/date/slot)을 쇼츠 콘티에 얹는다
       - 롱폼에서 이미 만든 음성 mp3 를 쇼츠 음성 폴더로 번호를 다시 매겨 복사한다(타입캐스트 재사용)
       결과: episodes/<날짜>_<슬롯>.json  → 그대로 build.py prep/render 하면 된다"""
    ch = ep.get('chapters') or []
    if not ch: raise SystemExit('이 콘티에는 chapters 가 없습니다')
    idx = None
    for i, c in enumerate(ch):
        if str(which) == str(i + 1) or str(which) == str(c.get('key', '')): idx = i; break
    if idx is None: raise SystemExit(f'챕터를 못 찾음: {which} (1~{len(ch)} 또는 key)')
    c = ch[idx]
    a = int(c.get('from', 0)); b = int(c.get('to', len(ep['lines']) - 1))
    if not (0 <= a <= b < len(ep['lines'])): raise SystemExit(f'챕터 구간이 이상합니다: {a}~{b}')
    sh = c.get('short') or {}
    # 9/20: 챕터를 그대로 자르면 첫마디가 "그 대만에서…" 처럼 앞 얘기를 받는 말이라 혼자서는 뜻이 안 통한다.
    #   short.intro / short.outro : 롱폼의 다른 줄(번호)을 앞/뒤에 붙인다 — 음성·자막·장면을 그대로 가져오므로 재녹음 없음.
    #   short.drop               : 챕터 안에서 뺄 줄 번호("그럼 마운드 말고 나머지는" 같은 연결용 문장)
    #   항목은 숫자 또는 {"line": 0, "scene": {...덮어쓸 값}} — 훅 사진을 편마다 바꿀 때 scene 으로 덮는다.
    def _norm(v):
        return [(int(x), {}) if not isinstance(x, dict) else (int(x['line']), dict(x.get('scene') or {})) for x in (v or [])]
    drop = set(int(x) for x in (sh.get('drop') or []))
    seq = _norm(sh.get('intro')) + [(i, {}) for i in range(a, b + 1) if i not in drop] + _norm(sh.get('outro'))
    n = len(ep['lines'])
    for i, _ in seq:
        if not (0 <= i < n): raise SystemExit(f'intro/outro 줄 번호가 범위 밖: {i}')
    by_line = {}
    for sc in ep.get('scenes', []):
        by_line.setdefault(int(sc.get('startLine', 0)), sc)   # 줄마다 첫 장면 하나
    out = {
        'date': sh.get('date') or ep.get('date'), 'gameDate': ep.get('gameDate'),
        'series': sh.get('series') or '야구이슈', 'railTitle': sh.get('railTitle') or 'KBO 이슈',
        'focusTeam': sh.get('focusTeam') or ep.get('focusTeam'),
        'source': f'롱폼 {os.path.basename(ep_path)} 챕터 {idx + 1}({c.get("title", "")}) 에서 잘라냄. ' + str(ep.get('source', '')),
        'thumb': sh.get('thumb') or ep.get('thumb'),
        'youtube': sh.get('youtube') or ep.get('youtube'),
        'lines': [dict(ep['lines'][i]) for i, _ in seq],
        'scenes': [],
    }
    if ep.get('speed') is not None: out['speed'] = ep['speed']   # 9/20: 롱폼 음성이 타입캐스트 1.2x 원음이면 쇼츠도 atempo 안 태운다(설정 SPEED 무시)
    for j, (i, ov) in enumerate(seq):
        sc = by_line.get(i)
        if sc is None: continue
        d = dict(sc); d.update(ov); d['startLine'] = j
        if d.get('type') == 'chapter': d['type'] = 'hook'          # 챕터 표지는 쇼츠에서 훅으로
        out['scenes'].append(d)
    if not out['scenes'] or out['scenes'][0]['startLine'] != 0:
        out['scenes'].insert(0, {'type': 'hook', 'startLine': 0, 'text': (c.get('title') or '')})
    slot = sh.get('slot') or f'이슈{idx + 1}'
    dst = os.path.join('episodes', f'{out["date"]}_{slot}.json')
    os.makedirs('episodes', exist_ok=True)
    # 9/18 사고: 롱폼 챕터의 date+slot 이 이미 있는 편과 같아 그 콘티와 음성을 통째로 덮어썼다.
    # 남의 편을 지우지 않게, 이미 있으면 여기서 멈춘다(챕터 short.slot 을 바꿔서 다시 실행).
    if os.path.exists(dst):
        import json as _j
        try: cur = _j.load(io.open(dst, encoding='utf-8-sig'))
        except Exception: cur = {}
        if cur.get('_fromLong') != os.path.basename(ep_path):
            raise SystemExit(f'이미 있는 콘티라 덮어쓰지 않았습니다: {dst}\n'
                             f'  → 롱폼 콘티의 chapters[].short.slot 을 다른 이름(이슈3 등)으로 바꾸고 다시 실행하세요.')
    out['_fromLong'] = os.path.basename(ep_path)
    json.dump(out, io.open(dst, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 음성 복사 (롱폼 → 쇼츠)
    src_dir, dst_dir = voice_dir(ep_key(ep_path)), voice_dir(ep_key(dst))
    moved = 0
    for j, (i, _) in enumerate(seq):
        for ext in ('.mp3', '.txt', '.segs.json'):   # 9/20: 호흡 경계(segs)도 같이 — 없으면 자막이 한 덩어리로 나온다
            f = os.path.join(src_dir, f'{i:02d}{ext}')
            if os.path.exists(f):
                shutil.copyfile(f, os.path.join(dst_dir, f'{j:02d}{ext}'))
                if ext == '.mp3': moved += 1
    # 줄 수가 줄었으면 남은 옛 번호 파일이 자막에 섞이지 않게 치운다
    for f in os.listdir(dst_dir) if os.path.isdir(dst_dir) else []:
        m = re.match(r'^(\d{2})\.(mp3|txt|segs\.json)$', f)
        if m and int(m.group(1)) >= len(seq): os.remove(os.path.join(dst_dir, f))
    print(f'잘라냄: {dst}  ({len(seq)}줄 = 도입 {len(sh.get("intro") or [])} + 본문 {b - a + 1 - len(drop)} + 마무리 {len(sh.get("outro") or [])}, 장면 {len(out["scenes"])}개, 음성 {moved}개 복사)')
    print(f'  다음: python -X utf8 build.py prep {dst}  →  python -X utf8 build.py render {dst}')
    return dst

def write_srt(subs, path):
    """영상 자막(subs: [시작초, 끝초, 글])을 SRT 로. 유튜브 업로드 화면 → 자막 → 파일 업로드에 쓴다(검색 색인용, 화면엔 이미 자막이 있으니 '자막 표시'는 꺼도 됨)"""
    def ts(t):
        t = max(0.0, float(t)); h = int(t // 3600); m = int(t % 3600 // 60); s = int(t % 60); ms = int(round((t - int(t)) * 1000))
        if ms == 1000: s, ms = s + 1, 0
        return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
    body = []
    for k, (a, b_, text) in enumerate(subs, 1):
        if b_ <= a: continue
        body.append(f'{k}\n{ts(a)} --> {ts(b_)}\n{str(text).replace(chr(10), " ").strip()}\n')
    io.open(path, 'w', encoding='utf-8').write('\n'.join(body) + '\n')
    return path

def upload_tag(ep):
    """제목 맨 앞 해시태그 = 영상 올리는 날짜(콘티 date, 밤 제작이면 다음날). 예: #9월13일"""
    try:
        d = datetime.date.fromisoformat(str(ep.get('date', ''))[:10])
        return f'#{d.month}월{d.day}일'
    except Exception: return ''

def title_with_date(ep):
    """제목의 첫 해시태그를 업로드 날짜로(9/13 규칙): '... 이유 #야구순위 #KT #삼성' → '... 이유 #9월13일 #야구순위 #KT #삼성'. 이미 있으면 그대로"""
    t = ((ep.get('youtube') or {}).get('title') or '').strip()
    t = re.sub(r'^\d{1,2}월\s*\d{1,2}일\s*', '', t)   # 제목 맨 앞 날짜는 쓰지 않는다(9/15) — 날짜는 해시태그(#9월15일)로만
    tag = upload_tag(ep)
    if not tag or not t: return t
    if re.search(r'#\d+월\d+일', t): return t
    m = re.search(r'\s#', t)   # 첫 해시태그 앞
    return (t[:m.start()] + ' ' + tag + t[m.start():]) if m else (t + ' ' + tag)

def write_youtube_txt(ep, path, dur=0):
    """사용자가 확인하기 쉽게 유튜브 제목·설명·태그를 텍스트로 같이 저장"""
    y = ep.get('youtube') or {}
    desc = (y.get('description') or '').rstrip()
    desc = re.sub(r'\n*📊 이 영상의 숫자\n(?:•[^\n]*\n?)+', '\n', desc)   # 옛 콘티의 숫자 목록은 빼고(9/15)
    desc = re.sub(r'\n+(?:#\S+\s*)+$', '', desc).strip()   # 설명 끝 해시태그 줄은 [해시태그] 칸으로
    hashtags = y.get('hashtags') or []
    if not hashtags:   # 콘티에 없으면 태그로 만든다(띄어쓰기 제거)
        stag = {'야구이슈': '#야구이슈', '야구분석': '#야구분석'}.get(str(ep.get('series', '')), '#야구순위')
        base = ['#야구자판기', stag, '#프로야구', '#KBO', '#야구']
        hashtags = base + ['#' + t.replace(' ', '') for t in y.get('tags', []) if '#' + t.replace(' ', '') not in base][:10] + ['#야구스타그램', '#야구팬', '#Shorts']
    body = ['[제목]', title_with_date(ep), '', '[설명]', desc, '', '[태그]  (유튜브 태그 칸에 그대로)', ', '.join(y.get('tags', [])), '',
            '[해시태그]  (인스타그램·틱톡 캡션에 복붙 / 유튜브 설명 끝에 붙여도 됨)', ' '.join(hashtags)]
    io.open(path, 'w', encoding='utf-8').write('\n'.join(body) + '\n')

def cfg_get(k, default=''):
    try:
        for line in open_cfg():
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
    # 야구이슈 편은 화이트 사진형 썸네일(thumb_issue.html), 순위 편은 기존 thumb.html
    ser = str(EP.get('series', '')).strip()
    if ser == '야구롱폼' and os.path.exists('thumb_long.html'): tpl = 'thumb_long.html'           # 9/18: 롱폼은 가로 1280x720
    elif ser == '야구분석' and os.path.exists('thumb_analysis.html'): tpl = 'thumb_analysis.html'   # 9/15: 분석은 구단 색 바탕 + 구단 로고 화면 가득
    else: tpl = 'thumb_issue.html' if (ser in ('야구이슈', '야구분석') and os.path.exists('thumb_issue.html')) else 'thumb.html'
    if 'photos' not in EP:
        EP['photos'] = photos_data_uri(EP, EP.get('_path')); EP['photoSizes'] = PHOTO_SIZES
    m = re.search(r'_(?:순위|이슈|분석)(\d*)\.json$', str(EP.get('_path') or ''))   # 그날 몇 번째 편인지(이슈=0, 이슈2=1 …) → 썸네일 큰 글씨 색을 편마다 바꾼다(9/15)
    EP['epIndex'] = (int(m.group(1)) - 1) if (m and m.group(1)) else 0
    html = io.open(tpl, encoding='utf-8').read().replace('__FONT_DIR__', font_dir_url())
    html = html.replace('<script>', '<script>window.EP=' + json.dumps(EP, ensure_ascii=False) + ';</script><script>', 1)
    io.open(W('render_thumb.html'), 'w', encoding='utf-8').write(html)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    env = dict(os.environ)
    if ser == '야구롱폼': env['THUMB_W'], env['THUMB_H'] = '1280', '720'     # 유튜브 롱폼 썸네일은 16:9
    r = subprocess.run(['node', 'thumb.js', W('render_thumb.html'), out], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
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
        EP = dict(ep); EP['logos'] = logos_data_uri(); EP['_path'] = path
        print(make_thumb(EP, out_paths(ep, path)[1]))
    elif mode == 'cut':      # 9/18: 롱폼 콘티의 챕터 하나 → 쇼츠 콘티 + 음성.  build.py cut episodes/X_롱폼.json 2
        if len(sys.argv) < 4: raise SystemExit('사용: build.py cut <롱폼 콘티> <챕터 번호 또는 key>')
        cut_chapter(ep, path, sys.argv[3])
    elif mode == 'cutall':   # 챕터 전부 한 번에
        for i in range(len(ep.get('chapters') or [])): cut_chapter(ep, path, i + 1)
    else: raise SystemExit(__doc__)
