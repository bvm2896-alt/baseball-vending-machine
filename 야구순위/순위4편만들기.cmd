rem Build the four 2026-09-23 standings episodes in ONE run_daily process (2026-09-23 early morning):
rem   2026-09-23_rank (KT magic 11), rank2 (LG-Samsung 2nd), rank3 (KIA-LG 3rd), rank4 (Doosan-NC 5th)
rem Voice zips must be in ../yagu-rank/voice. --force rebuilds even if a video exists.
rem When the log says "Watch started" (Korean: gamsi sijak), all 4 are done: just close this window.
@echo off
chcp 65001 >nul
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
rem 9/23: each window gets its own work folder so two build windows never share frames/narration (issue9 got rank frames)
set KBO_WORK=work\rank
if not exist "%KBO_WORK%" mkdir "%KBO_WORK%"
python -X utf8 -c "import glob,subprocess,sys;ps=sorted(glob.glob('episodes/2026-09-23_*.json'));ps=[p for p in ps if p.split('_',1)[1].startswith('\uc21c\uc704')];print('=== build',len(ps),'rank episodes in ONE run ===');[print('  ',p) for p in ps];a=[sys.executable,'-X','utf8','run_daily.py'];[a.extend(['--episode',p]) for p in ps];a+=['--force','--no-fetch','--now','--no-shutdown'];subprocess.call(a)"
pause
