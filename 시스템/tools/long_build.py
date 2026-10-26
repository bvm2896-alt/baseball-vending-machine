# 10/18 밤: 야구롱폼\_long_build.py 에서 시스템\tools\long_build.py 로 옮김(사용자 "자주 쓰는 폴더를 지저분하게 하지 마"). 롱폼만들기·롱폼검수·롱폼_숏츠만들기.cmd 가 부른다.
# 롱폼 만들기: prep -> tts(음성 zip 자르기 또는 타입캐스트 API 줄마다 합성) -> render.
# 9/27: 날짜로 시작하는 롱폼 콘티(YYYY-MM-DD_롱폼*.json, chapters 있는 것) 중 가장 최근 것을 만든다.
#       '_샘플_롱폼.json' 같은 이름은 절대 고르지 않는다(9/27 사고: '_' 가 숫자보다 뒤로 정렬돼 샘플을 합성해 크레딧 소진).
#       특정 날짜는 인자로: python _long_build.py 2026-09-18
# 10/2: 롱폼을 쪼갠 컷 쇼츠(YYYY-MM-DD_롱폼컷N.json, "vertical": true)도 같이 만든다 — 롱폼을 먼저, 그다음 컷(컷은 롱폼 음성을 가져다 쓴다).
#       이미 같은 내용으로 만든 편(work\long_built.json 에 콘티 지문이 같은 것)은 건너뛴다. 검수판(KBO_DRAFT)과 최종판은 따로 센다.
# 10/22 밤 사용자 "롱폼만들기 하면 삼성이랑 롯데 같이 만들어지게": 가장 늦은 날짜의 롱폼 콘티(_롱폼.json·_롱폼2.json…)를 전부, 이름 순서로 만든다(이미 만든 편은 건너뜀).
# 합성 전에 어떤 콘티를 만드는지 보여 주고 Enter(y)를 받아야 시작한다.
# 10/2 밤 사용자 "롱폼만들기 말고 롱폼_숏츠만들기 배치파일을 하나 더" → 두 버튼으로 나눈다.
#       --long : 롱폼만 (롱폼만들기.cmd·롱폼검수.cmd)
#       --cuts : 컷 쇼츠만 (롱폼_숏츠만들기.cmd) — 롱폼은 건드리지 않는다. 날짜를 안 주면 가장 최근 날짜의 롱폼컷 콘티 전부.
#       둘 다 없으면 예전처럼 롱폼 + 그 롱폼의 컷.
# tts.py 는 새로 만들 글자 수를 보여 주고, 3,500자 넘거나 1번 계정이 떨어지면 여기서 y 를 받아야 계속한다(9/27).
import glob, json, io, os, re, subprocess, sys, hashlib
def load(p): return json.load(io.open(p, encoding='utf-8-sig'))
def fp(p): return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:16]
DRAFT = '검수' if os.environ.get('KBO_DRAFT') else '최종'
BUILT = os.path.join('work', 'long_built.json')
try: built = json.load(io.open(BUILT, encoding='utf-8'))
except Exception: built = {}
def done(p): return DRAFT != '검수' and built.get(f'{DRAFT}|{os.path.basename(p)}') == fp(p)   # 10/25 사용자 "롱폼검수 누르면 생성되게": 검수판은 같은 콘티여도 늘 다시 만든다(음성은 바뀐 줄만 합성)

args = sys.argv[1:]
MODE = 'long' if '--long' in args else 'cuts' if '--cuts' in args else 'both'
args = [a for a in args if a not in ('--long', '--cuts')]
iscut = lambda c: re.match(r'\d{4}-\d{2}-\d{2}_롱폼컷\d+\.json$', os.path.basename(c)) and load(c).get('vertical')
cutkey = lambda c: (os.path.basename(c)[:10], int(re.search(r'컷(\d+)', os.path.basename(c)).group(1)))
p = None; longs = []
if MODE == 'cuts':
    cuts = sorted((c for c in glob.glob('episodes/*.json') if iscut(c)), key=cutkey)
    if args: cuts = [c for c in cuts if args[0] in os.path.basename(c)]
    elif cuts: cuts = [c for c in cuts if os.path.basename(c)[:10] == max(os.path.basename(x)[:10] for x in cuts)]   # 가장 최근 날짜 컷만
    if not cuts: sys.exit('만들 컷 쇼츠 콘티가 없습니다 (episodes\\YYYY-MM-DD_롱폼컷N.json)')
    todo = [c for c in cuts if not done(c)]
    if not todo:
        sys.exit(f'다 만들어져 있어요({DRAFT}판): 컷 {len(cuts)}편 ' + ', '.join(os.path.basename(c) for c in cuts) + ' — 콘티를 고치면 다시 만듭니다')
else:
    ps = sorted(x for x in glob.glob('episodes/*.json')
                if re.match(r'\d{4}-\d{2}-\d{2}_롱폼', os.path.basename(x)) and not iscut(x) and load(x).get('chapters'))
    if args: ps = [x for x in ps if args[0] in os.path.basename(x)]
    if not ps: sys.exit('만들 롱폼 콘티가 없습니다 (episodes\\YYYY-MM-DD_롱폼.json)')
    # 10/22 밤: 가장 늦은 날짜의 롱폼 콘티를 전부(이름 순서: _롱폼 → _롱폼2 → …) 만든다. 이미 같은 내용으로 만든 편은 건너뛴다.
    last = max(os.path.basename(x)[:10] for x in ps)
    longs = sorted((x for x in ps if os.path.basename(x)[:10] == last),
                   key=lambda x: int((re.search(r'_롱폼(\d*)\.json$', os.path.basename(x)).group(1) or 1) if re.search(r'_롱폼(\d*)\.json$', os.path.basename(x)) else 99))
    # 10/24: 날짜가 바뀌어도 '검수판만 만들고 최종판을 아직 안 만든' 롱폼(최근 3일)은 함께 만든다 — 기아 방출(10/23) 최종판이 다음 날 새 콘티에 밀려 빠지지 않게
    if DRAFT == '최종' and not args:
        import datetime
        # 10/25: 검수판을 그대로 올린 편은 최종판을 만들지 않는다(work\long_uploaded.txt 에 콘티 파일 이름 한 줄씩)
        UPLOADED = {'2026-10-23_롱폼3.json'}
        try: UPLOADED |= {l.strip() for l in open(os.path.join('work', 'long_uploaded.txt'), encoding='utf-8') if l.strip()}
        except OSError: pass
        lim = (datetime.date.fromisoformat(last) - datetime.timedelta(days=3)).isoformat()
        pend = [x for x in ps if x not in longs and os.path.basename(x)[:10] >= lim
                and built.get(f'검수|{os.path.basename(x)}') and not built.get(f'최종|{os.path.basename(x)}')
                and os.path.basename(x) not in UPLOADED]
        longs = pend + longs
    p = longs[0]
    stems = {os.path.splitext(os.path.basename(x))[0] for x in longs}
    cuts = [] if MODE == 'long' else sorted(
        (c for c in glob.glob('episodes/*.json')
         if iscut(c) and (load(c).get('voiceFrom') or {}).get('ep') in stems), key=cutkey)
    todo = [x for x in longs if not done(x)] + [c for c in cuts if not done(c)]
    if not todo:
        sys.exit(f'다 만들어져 있어요({DRAFT}판): ' + ', '.join(os.path.basename(x) for x in longs) + (f' + 컷 {len(cuts)}편' if cuts else '') + ' — 콘티를 고치면 다시 만듭니다')

print('=' * 70)
print(f'이번에 만들 것({DRAFT}판):', ', '.join(os.path.basename(x) for x in todo))
for x in (longs if MODE != 'cuts' else []):
    if x not in todo: print(f'  (롱폼 {os.path.basename(x)} 은 이미 만들어져 있어 건너뜀)')
if MODE == 'cuts':
    skip = [c for c in cuts if c not in todo]
    if skip: print('  (이미 만들어져 있어 건너뜀: ' + ', '.join(os.path.basename(c) for c in skip) + ')')
    print('  롱폼은 만들지 않습니다(컷 쇼츠만). 롱폼에서 만든 음성은 그대로 가져다 씁니다.')
for x in todo:
    e = load(x); L = e.get('lines', [])
    print('=' * 70)
    print(('롱폼: ' if x in longs else '컷 쇼츠: ') + x)
    print('  제목:', (e.get('youtube') or {}).get('title', '')[:80])
    print('  줄 수:', len(L), ' / 타입캐스트 API' if e.get('ttsApi') else ' / 음성 zip', f" / 말 속도 {e.get('speed')}배" if e.get('vertical') else '')
    ch = {c.get('from'): c for c in e.get('chapters', [])}
    vf = (e.get('voiceFrom') or {}).get('lines') or []
    for i, l in enumerate(L):
        if i in ch: print(f"\n[챕터] {ch[i].get('title', '')}  ({ch[i].get('from')}~{ch[i].get('to')}줄)")
        tag = '' if not e.get('vertical') else ('  [롱폼 %02d번 음성]' % vf[i] if i < len(vf) and vf[i] is not None else '  [새 줄]')
        print(f"  {i:02d}  {l.get('narr', '').replace(' / ', ' ')}{tag}")
# 10/23 사용자("카드가 너무 늦게 떠서 나오자마자 다음 장면으로 넘어가"): 음성 zip 이 있으면 늦게 뜨는 글·카드(1.5초 미만 보임)를 먼저 잰다
for x in todo:
    vf = (load(x).get('voiceFrom') or {}).get('ep') if load(x).get('vertical') else None   # 10/23: 컷 쇼츠는 롱폼 음성 zip 으로 잰다
    if load(x).get('vertical') and not vf: continue
    zp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '야구롱폼', '음성', (vf or os.path.basename(x)[:-5]) + '.zip')
    if os.path.exists(zp):
        print(f'  [늦게 뜨는 글 검사] {os.path.basename(x)}'); subprocess.call([sys.executable, '-X', 'utf8', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'late_check.py'), x, zp])
# 10/24 사용자("상황에 따라 읽는 방식이 다른데 이런걸 내가 하나하나 다 지적할 수 없어"): 합성 전에 숫자 읽기(칠번 좌익수·세 명·스물다섯 살 등)를 검사해 보여 준다
# 10/24 사용자 "뭘 멈춰 진행계속 하고 그 부분만 나한테 검수받아" → 멈추지 않고 목록만 보여 준다(Claude 가 콘티를 넣기 전에 이미 0 으로 만든다)
subprocess.call([sys.executable, '-X', 'utf8', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'read_check.py'), '--warn'] + todo)
print('=' * 70)
print('  위 대본이 맞는지 보고 결정하세요. 이미 만든 줄·구독 멘트는 다시 합성하지 않습니다(tts 가 편마다 새로 만들 글자 수를 한 번 더 보여 줌).')
# 10/14: KBO_YES=1(롱폼검수_자동.cmd)이면 묻지 않고 시작 — Claude 가 PC 를 클릭만으로 돌릴 때(사용자 지시 "너가 컴퓨터 조작해서 영상 만들고 검수까지")
a = '' if os.environ.get('KBO_YES') else input('이대로 만들까요? (Enter 또는 y = 시작, 그 외 = 취소) ').strip().lower()
if a not in ('', 'y', 'ㅛ'): sys.exit('취소했습니다')
for x in todo:
    print('\n' + '#' * 70 + f'\n# {os.path.basename(x)}\n' + '#' * 70)
    for c in (['build.py', 'prep', x], ['tts.py'], ['build.py', 'render', x]):
        r = subprocess.call([sys.executable, '-X', 'utf8'] + c, env=dict(os.environ, KBO_ASK='1'))   # tts.py 가 글자 수 초과·계정 전환 때 여기 콘솔에서 묻는다
        if r: sys.exit(f'{os.path.basename(x)} 에서 멈췄어요 — 위 오류를 Claude 에게 보여 주세요' + (' (이 롱폼이 안 끝나서 뒤의 편·컷 쇼츠는 만들지 않았어요)' if x in longs else ''))
    built[f'{DRAFT}|{os.path.basename(x)}'] = fp(x)
    os.makedirs('work', exist_ok=True); json.dump(built, io.open(BUILT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'\n완료({DRAFT}판): ' + ', '.join(os.path.basename(x) for x in todo))
if MODE == 'cuts' and todo: print('영상 폴더: 야구롱폼\\영상\\' + os.path.basename(todo[0])[:10] + ' (그다음 깃저장)')
