# 롱폼 만들기: prep -> tts(음성 zip 자르기 또는 타입캐스트 API 줄마다 합성) -> render.
# 9/27: 날짜로 시작하는 롱폼 콘티(YYYY-MM-DD_롱폼*.json, chapters 있는 것) 중 가장 최근 것을 만든다.
#       '_샘플_롱폼.json' 같은 이름은 절대 고르지 않는다(9/27 사고: '_' 가 숫자보다 뒤로 정렬돼 샘플을 합성해 크레딧 소진).
#       특정 날짜는 인자로: python _long_build.py 2026-09-18
# 합성 전에 어떤 콘티를 만드는지 보여 주고 Enter(y)를 받아야 시작한다.
# tts.py 는 새로 만들 글자 수를 보여 주고, 3,500자 넘거나 1번 계정이 떨어지면 여기서 y 를 받아야 계속한다(9/27).
# 챕터 쇼츠 자르기(cutall)는 따로(챕터쇼츠만들기.cmd).
import glob,json,io,os,re,subprocess,sys
ps=sorted(p for p in glob.glob('episodes/*.json')
          if re.match(r'\d{4}-\d{2}-\d{2}_롱폼', os.path.basename(p)) and json.load(io.open(p,encoding='utf-8-sig')).get('chapters'))
if len(sys.argv)>1: ps=[p for p in ps if sys.argv[1] in os.path.basename(p)]
if not ps: sys.exit('만들 롱폼 콘티가 없습니다 (episodes\\YYYY-MM-DD_롱폼.json)')
p=ps[-1]; ep=json.load(io.open(p,encoding='utf-8-sig'))
print('만들 롱폼:', p)
print('  제목:', (ep.get('youtube') or {}).get('title','')[:70])
print('  줄 수:', len(ep.get('lines',[])), ' / 타입캐스트 API' if ep.get('ttsApi') else ' / 음성 zip')
# 9/27: 콘티 내용(챕터·대본 전 줄)을 보여 준 뒤에 묻는다 — 제목만 보고는 맞는 콘티인지 알 수 없어서
L=ep.get('lines',[]); ch={c.get('from'):c for c in ep.get('chapters',[])}
print('=' * 70)
for i,l in enumerate(L):
    if i in ch: print(f"\n[챕터] {ch[i].get('title','')}  ({ch[i].get('from')}~{ch[i].get('to')}줄)")
    elif i==0: print('[도입]')
    print(f"  {i:02d}  {l.get('narr','').replace(' / ',' ')}")
print('=' * 70)
print(f"  총 {len(L)}줄 / 대본 약 {sum(len(l.get('narr','').replace(' / ',' ')) for l in L)}자(공백 포함, 구독 멘트 포함)")
print('  위 대본이 맞는지 보고 결정하세요. 이미 만든 줄·구독 멘트는 다시 합성하지 않습니다(tts 가 이번에 새로 만들 글자 수를 한 번 더 보여 줌).')
a=input('이 콘티로 만들까요? (Enter 또는 y = 시작, 그 외 = 취소) ').strip().lower()
if a not in ('','y','ㅛ'): sys.exit('취소했습니다')
for c in (['build.py','prep',p],['tts.py'],['build.py','render',p]):
    r=subprocess.call([sys.executable,'-X','utf8']+c, env=dict(os.environ, KBO_ASK='1'))   # tts.py 가 글자 수 초과·계정 전환 때 여기 콘솔에서 묻는다
    if r: sys.exit(r)
