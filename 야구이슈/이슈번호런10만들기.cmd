@echo off
chcp 65001 >nul
rem Build 2026-09-23_issue10 (home run race) alone. Voice zip must be in ../yagu-issue/voice.
rem When the log says "Watch started" (gamsi sijak), close this window.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
rem 9/23: each window gets its own work folder so two build windows never share frames/narration (issue9 got rank frames)
set KBO_WORK=work\issue
if not exist "%KBO_WORK%" mkdir "%KBO_WORK%"
python -X utf8 -c "import glob,subprocess,sys;ps=sorted(glob.glob('episodes/2026-09-23_*10.json'));print('=== build',ps,'===');a=[sys.executable,'-X','utf8','run_daily.py'];[a.extend(['--episode',p]) for p in ps];a+=['--force','--no-fetch','--now','--no-shutdown'];subprocess.call(a)"
pause
