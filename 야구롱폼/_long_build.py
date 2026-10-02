# 롱폼 만들기: prep -> tts(음성 zip 자르기 또는 타입캐스트 API 줄마다 합성) -> render.
# 9/27: 날짜로 시작하는 롱폼 콘티(YYYY-MM-DD_롱폼*.json, chapters 있는 것) 중 가장 최근 것을 만든다.
#       '_샘플_롱폼.json' 같은 이름은 절대 고르지 않는다(9/27 사고: '_' 가 숫자보다 뒤로 정렬돼 샘플을 합성해 크레딧 소진).
#       특정 날짜는 인자로: python _long_build.py 2026-09-18
# 10/2: 롱폼을 쪼갠 컷 쇼츠(YYYY-MM-DD_롱폼컷N.json, "vertical": true)도 같이 만든다 — 롱폼을 먼저, 그다음 컷(컷은 롱폼 음성을 가져다 쓴다).
#       이미 같은 내용으로 만든 편(work\long_built.json 에 콘티 지문이 같은 것)은 건너뛴다. 검수판(KBO_DRAFT)과 최종판은 따로 센다.
# 합성 전에 어떤 콘티를 만드는지 보여 주고 Enter(y)를 받아야 시작한다.
# tts.py 는 새로 만들 글자 수를 보여 주고, 3,500자 넘거나 1번 계정이 떨어지면 여기서 y 를 받아야 계속한다(9/27).
import glob, json, io, os, re, subprocess, sys, hashlib
def load(p): return json.load(io.open(p, encoding='utf-8-sig'))
def fp(p): return hashlib.sha1(open(p, 'rb').read()).hexdigest()[:16]
DRAFT = '검수' if os.environ.get('KBO_DRAFT') else '최종'
BUILT = os.path.join('work', 'long_built.json')
try: built = json.load(io.open(BUILT, encoding='utf-8'))
except Exception: built = {}
def done(p): return built.get(f'{DRAFT}|{os.path.basename(p)}') == fp(p)

ps = sorted(p for p in glob.glob('episodes/*.json')
            if re.match(r'\d{4}-\d{2}-\d{2}_롱폼', os.path.basename(p)) and load(p).get('chapters'))
if len(sys.argv) > 1: ps = [p for p in ps if sys.argv[1] in os.path.basename(p)]
if not ps: sys.exit('만들 롱폼 콘티가 없습니다 (episodes\\YYYY-MM-DD_롱폼.json)')
p = ps[-1]; ep = load(p)
cuts = sorted((c for c in glob.glob('episodes/*.json')
               if re.match(r'\d{4}-\d{2}-\d{2}_롱폼컷\d+\.json$', os.path.basename(c)) and load(c).get('vertical')
               and (load(c).get('voiceFrom') or {}).get('ep') == os.path.splitext(os.path.basename(p))[0]),
              key=lambda c: int(re.search(r'컷(\d+)', c).group(1)))
todo = ([] if done(p) else [p]) + [c for c in cuts if not done(c)]
if not todo:
    sys.exit(f'다 만들어져 있어요({DRAFT}판): {os.path.basename(p)} + 컷 {len(cuts)}편 — 콘티를 고치면 다시 만듭니다')

print('=' * 70)
print(f'이번에 만들 것({DRAFT}판):', ', '.join(os.path.basename(x) for x in todo))
if p not in todo: print(f'  (롱폼 {os.path.basename(p)} 은 이미 만들어져 있어 건너뜀)')
for x in todo:
    e = load(x); L = e.get('lines', [])
    print('=' * 70)
    print(('롱폼: ' if x == p else '컷 쇼츠: ') + x)
    print('  제목:', (e.get('youtube') or {}).get('title', '')[:80])
    print('  줄 수:', len(L), ' / 타입캐스트 API' if e.get('ttsApi') else ' / 음성 zip', f" / 말 속도 {e.get('speed')}배" if e.get('vertical') else '')
    ch = {c.get('from'): c for c in e.get('chapters', [])}
    vf = (e.get('voiceFrom') or {}).get('lines') or []
    for i, l in enumerate(L):
        if i in ch: print(f"\n[챕터] {ch[i].get('title', '')}  ({ch[i].get('from')}~{ch[i].get('to')}줄)")
        tag = '' if not e.get('vertical') else ('  [롱폼 %02d번 음성]' % vf[i] if i < len(vf) and vf[i] is not None else '  [새 줄]')
        print(f"  {i:02d}  {l.get('narr', '').replace(' / ', ' ')}{tag}")
print('=' * 70)
print('  위 대본이 맞는지 보고 결정하세요. 이미 만든 줄·구독 멘트는 다시 합성하지 않습니다(tts 가 편마다 새로 만들 글자 수를 한 번 더 보여 줌).')
a = input('이대로 만들까요? (Enter 또는 y = 시작, 그 외 = 취소) ').strip().lower()
if a not in ('', 'y', 'ㅛ'): sys.exit('취소했습니다')
for x in todo:
    print('\n' + '#' * 70 + f'\n# {os.path.basename(x)}\n' + '#' * 70)
    for c in (['build.py', 'prep', x], ['tts.py'], ['build.py', 'render', x]):
        r = subprocess.call([sys.executable, '-X', 'utf8'] + c, env=dict(os.environ, KBO_ASK='1'))   # tts.py 가 글자 수 초과·계정 전환 때 여기 콘솔에서 묻는다
        if r: sys.exit(f'{os.path.basename(x)} 에서 멈췄어요 — 위 오류를 Claude 에게 보여 주세요' + (' (롱폼이 안 끝나서 컷 쇼츠는 만들지 않았어요)' if x == p else ''))
    built[f'{DRAFT}|{os.path.basename(x)}'] = fp(x)
    os.makedirs('work', exist_ok=True); json.dump(built, io.open(BUILT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'\n완료({DRAFT}판): ' + ', '.join(os.path.basename(x) for x in todo))
