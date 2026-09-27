# 이미 만든 롱폼 mp4 끝에 엔딩 카드(12초)를 붙인다. 두 번 실행해도 한 번만 붙는다.
import glob, json, io, os, sys
sys.path.insert(0, os.getcwd()); sys.argv = ['build.py']
import build
import re
ps = sorted(p for p in glob.glob('episodes/*.json') if re.match(r'\d{4}-\d{2}-\d{2}_롱폼', os.path.basename(p)) and json.load(io.open(p, encoding='utf-8-sig')).get('chapters'))   # 9/27: 날짜로 시작하는 가장 최근 롱폼(_샘플 제외)
if len(sys.argv) > 1: ps = [p for p in ps if sys.argv[1] in p]
p = ps[-1]; ep = build.load_episode(p); ep['_path'] = p
out = build.out_paths(ep, p)[0]
if not os.path.exists(out): sys.exit('mp4 없음: ' + out)
mark = build.W('endcard_applied.txt')
stamp = f'{out}|{os.path.getsize(out)}'
if os.path.exists(mark) and io.open(mark, encoding='utf-8').read().strip() == stamp:
    print('이미 엔딩 카드가 붙어 있습니다:', out); sys.exit(0)
build.append_endcard(dict(ep), out)
io.open(mark, 'w', encoding='utf-8').write(f'{out}|{os.path.getsize(out)}')
print('완료:', out, f'{build.dur_of(out):.1f}초')
