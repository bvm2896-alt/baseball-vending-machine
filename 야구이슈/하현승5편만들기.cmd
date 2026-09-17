@echo off
chcp 65001 >nul
rem Build ALL FIVE Ha Hyun-seung episodes in ONE run_daily process.
rem   2026-09-17_issue4 / issue5 / 2026-09-18 / 2026-09-19 / 2026-09-20
rem --force is on, so they are rebuilt even if a video already exists
rem (use this after changing SPEED in the settings file).
rem When the log says "Watch started", all five are done: just close this window.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
python -X utf8 -c "import glob,subprocess,sys;pat=['episodes/2026-09-17_*4.json','episodes/2026-09-17_*5.json','episodes/2026-09-18_*.json','episodes/2026-09-19_*.json','episodes/2026-09-20_*.json'];ps=sorted(sum([glob.glob(p) for p in pat],[]));print('=== build',len(ps),'episodes in ONE run ===');[print('  ',p) for p in ps];a=[sys.executable,'-X','utf8','run_daily.py'];[a.extend(['--episode',p]) for p in ps];a+=['--force','--no-fetch','--now','--no-shutdown'];subprocess.call(a)"
pause
