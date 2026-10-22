@echo off
chcp 65001 >nul
rem Build only the Golden Glove cut shorts (episodes\2026-10-18_longform-cut1~6.json) made from the 2026 Golden Glove longform.
rem Already-built cuts (same script) are skipped. Voices are copied from the longform; only new lines are synthesized.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 tools\long_build.py --cuts 2026-10-18_롱폼컷
pause
