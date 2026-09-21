import subprocess,sys
eps=['episodes/2026-09-19_이슈.json','episodes/2026-09-20_이슈.json']
a=[sys.executable,'-X','utf8','run_daily.py']
for e in eps: a+=['--episode',e]
a+=['--force','--no-fetch','--now','--no-shutdown']
print('REBUILD', eps)
sys.exit(subprocess.call(a))
