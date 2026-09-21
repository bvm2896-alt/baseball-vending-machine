import glob,json,io,subprocess,sys
ps=[p for p in glob.glob('episodes/2026-09-18_*.json') if json.load(io.open(p,encoding='utf-8-sig')).get('chapters')]
p=ps[0]; print('EPISODE', p)
for a in (['build.py','prep',p],['tts.py'],['build.py','render',p],['build.py','cutall',p]):
    r=subprocess.call([sys.executable,'-X','utf8']+a)
    if r: sys.exit(r)
