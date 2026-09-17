@echo off
chcp 65001 >nul
rem Build the five Ha Hyun-seung episodes in one go.
rem   2026-09-17_issue4 / issue5 / 2026-09-18 / 2026-09-19 / 2026-09-20
rem The four episodes already made last night are NOT touched.
rem Do not run this at the same time as the normal run.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
python -X utf8 -c "import glob,subprocess,sys;pat=['episodes/2026-09-17_*4.json','episodes/2026-09-17_*5.json','episodes/2026-09-18_*.json','episodes/2026-09-19_*.json','episodes/2026-09-20_*.json'];ps=sorted(sum([glob.glob(p) for p in pat],[]));print('=== build',len(ps),'episodes ===');[print(' ',p) for p in ps];[subprocess.call([sys.executable,'-X','utf8','run_daily.py','--episode',p,'--force','--no-fetch','--now','--no-shutdown']) for p in ps]"
echo.
echo DONE - check the video folders.
pause
