@echo off
chcp 65001 >nul
rem Build the Asian Games episodes in ONE run_daily process (2026-09-22 night):
rem   2026-09-23_issue..issue8  (Thailand preview, HK review, PHI-JPN / HK-TPE / PLE-CHN previews, TPE-THA, JPN-PLE, CHN-PHI reviews)
rem   2026-09-24_issue..issue4  (Taiwan reaction, THA-HK, JPN-CHN, PHI-PLE reviews)
rem Voice zips are already in ../yagu-issue/voice. --force rebuilds even if a video exists.
rem When the log says "Watch started" (Korean: gamsi sijak), all 12 are done: just close this window.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
rem 9/23: each window gets its own work folder so two build windows never share frames/narration (issue9 got rank frames)
set KBO_WORK=work\issue
if not exist "%KBO_WORK%" mkdir "%KBO_WORK%"
python -X utf8 -c "import glob,subprocess,sys;ps=sorted(glob.glob('episodes/2026-09-23_*.json'))+sorted(glob.glob('episodes/2026-09-24_*.json'));ps=[p for p in ps if p.split('_',1)[1].startswith('\uc774\uc288')];print('=== build',len(ps),'episodes in ONE run ===');[print('  ',p) for p in ps];a=[sys.executable,'-X','utf8','run_daily.py'];[a.extend(['--episode',p]) for p in ps];a+=['--force','--no-fetch','--now','--no-shutdown'];subprocess.call(a)"
pause
