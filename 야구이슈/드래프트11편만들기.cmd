@echo off
chcp 65001 >nul
rem Build the draft episodes in ONE run_daily process (2026-09-21 night):
rem   2026-09-21_issue2 (draft summary, Choi Ji-man photo fixed)
rem   2026-09-21_issue6..issue10 (Kiwoom / Doosan / KIA / Lotte / KT)
rem   2026-09-22_issue..issue5   (NC / Samsung / SSG / Hanwha / LG)
rem --force is on, so all 11 are rebuilt even if a video already exists. Voice zips are reused.
rem When the log says "Watch started" (Korean: gamsi sijak), all 11 are done: just close this window.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
python -X utf8 -c "import glob,subprocess,sys;pat=['episodes/2026-09-21_*2.json','episodes/2026-09-21_*6.json','episodes/2026-09-21_*7.json','episodes/2026-09-21_*8.json','episodes/2026-09-21_*9.json','episodes/2026-09-21_*10.json','episodes/2026-09-22_*.json'];ps=sum([sorted(glob.glob(p)) for p in pat],[]);ps=[p for p in ps if '_1' not in p[-9:] or p.endswith('10.json')];print('=== build',len(ps),'episodes in ONE run ===');[print('  ',p) for p in ps];a=[sys.executable,'-X','utf8','run_daily.py'];[a.extend(['--episode',p]) for p in ps];a+=['--force','--no-fetch','--now','--no-shutdown'];subprocess.call(a)"
pause
