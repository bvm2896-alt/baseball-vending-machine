# 10/1 사용자: "순위(가을야구 5팀)를 이미 만들고 있으니 2·3번(이슈 두 편)이 같이 만들어지게 배치파일 따로"
# 이슈 두 편만 순위 창과 동시에 만든다: prep -> tts(API) -> qa_voice -> render. 깃 동기화·자료 수집은 하지 않는다.
# 작업 폴더는 work\이슈2편 (순위 창 work\순위, 이슈 지금실행 work\이슈 와 안 겹침). 음성 폴더는 편마다 work\voice_<편> 이라 안 겹침.
# 다 만들면 status\built.json 에 적어서 나중에 지금실행이 같은 편을 다시 만들지 않게 한다.
import os, sys, io, json, hashlib, platform, datetime, subprocess
EPS = sys.argv[1:] or ['episodes/2026-10-01_이슈.json', 'episodes/2026-10-01_이슈2.json']
env = dict(os.environ, KBO_WORK=os.path.join('work', '이슈2편'), KBO_ASK='1')
env.setdefault('FRAME_WORKERS', '2')   # 순위 창과 CPU 나눠 쓰기
os.makedirs(env['KBO_WORK'], exist_ok=True)
def run(*a):
    print('\n>>', ' '.join(a), flush=True)
    return subprocess.call([sys.executable, '-X', 'utf8', *a], env=env)
print('만들 편:', ', '.join(os.path.basename(p) for p in EPS), '/ 작업 폴더', env['KBO_WORK'])
done, fail = [], []
for p in EPS:
    name = os.path.basename(p)
    if not os.path.exists(p): print('콘티 없음:', p); fail.append(name); continue
    if run('build.py', 'prep', p): print('prep 실패:', name); fail.append(name); continue
    if run('tts.py'): print('음성 실패:', name); fail.append(name); continue
    if run('qa_voice.py'): print('음성 검수 오류(무시하고 진행):', name)
    if run('build.py', 'render', p): print('렌더 실패:', name); fail.append(name); continue
    done.append(p)
# 만든 기록(run_daily 와 같은 지문: 콘티 JSON + 음성 zip — API 편은 zip 없음)
try:
    sys.path.insert(0, os.getcwd()); import build
    reg_path = os.path.join('status', 'built.json')
    try: reg = json.load(io.open(reg_path, encoding='utf-8'))
    except Exception: reg = {}
    for p in done:
        ep = json.load(io.open(p, encoding='utf-8-sig')); stem = os.path.splitext(os.path.basename(p))[0]
        h = hashlib.sha1(json.dumps(ep, ensure_ascii=False, sort_keys=True).encode('utf-8'))
        for e in ('.zip', '.mp3', '.wav', '.m4a'):
            f = os.path.join('..', str(ep.get('series') or '야구이슈'), '음성', stem + e)
            if os.path.exists(f): h.update(open(f, 'rb').read())
        reg[stem] = {'hash': h.hexdigest(), 'video': build.out_paths(ep, p)[0], 'pc': platform.node(), 'at': datetime.datetime.now().isoformat(timespec='minutes')}
    os.makedirs('status', exist_ok=True)
    json.dump(reg, io.open(reg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
except Exception as e:
    print('만든 기록 저장 실패(영상은 괜찮음):', e)
print('\n끝 — 완성', len(done), '편' + (', 실패: ' + ', '.join(fail) if fail else ''))
for p in done:
    try: print('  ', build.out_paths(json.load(io.open(p, encoding='utf-8-sig')), p)[0])
    except Exception: pass
