# 이미 만든 롱폼 mp4 끝에 엔딩 카드(12초)를 붙인다. 두 번 실행해도 한 번만 붙는다.
import glob, json, io, os, sys
sys.path.insert(0, os.getcwd()); sys.argv = ['build.py']
import build
ps = [p for p in glob.glob('episodes/2026-09-18_*.json') if json.load(io.open(p, encoding='utf-8-sig')).get('chapters')]
p = ps[0]; ep = build.load_episode(p); ep['_path'] = p
out = build.out_paths(ep, p)[0]
if not os.path.exists(out): sys.exit('mp4 없음: ' + out)
mark = build.W('endcard_applied.txt')
stamp = f'{out}|{os.path.getsize(out)}'
if os.path.exists(mark) and io.open(mark, encoding='utf-8').read().strip() == stamp:
    print('이미 엔딩 카드가 붙어 있습니다:', out); sys.exit(0)
build.append_endcard(dict(ep), out)
io.open(mark, 'w', encoding='utf-8').write(f'{out}|{os.path.getsize(out)}')
print('완료:', out, f'{build.dur_of(out):.1f}초')
