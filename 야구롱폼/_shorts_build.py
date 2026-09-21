# 롱폼 챕터 2·3·4 → 쇼츠 3편 (9/21 이슈2·3·4). 음성은 롱폼 폴더에서 복사되므로 tts 는 안 돈다.
import subprocess, sys, os, glob, io, json
p = 'episodes/2026-09-18_롱폼.json'
r = subprocess.call([sys.executable, '-X', 'utf8', 'build.py', 'cutall', p])
if r: sys.exit(r)
for e in ('2026-09-21_이슈2', '2026-09-21_이슈3', '2026-09-21_이슈4'):
    c = f'episodes/{e}.json'
    if not os.path.exists(c): sys.exit('없음: ' + c)
    for a in (['build.py', 'prep', c], ['build.py', 'render', c]):
        r = subprocess.call([sys.executable, '-X', 'utf8'] + a)
        if r: sys.exit(r)
print('쇼츠 3편 완료')
