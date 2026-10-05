@echo off
chcp 65001 >nul
rem Build only the vertical cut shorts made from a longform (episodes\YYYY-MM-DD_longform-cutN.json). The longform itself is not built.
rem Uses the latest date by default. Already-built cuts (same script) are skipped. Voices are copied from the longform.
rem For a specific date, run this file from a command prompt followed by the date (e.g. 2026-10-02).
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 "%~dp0_long_build.py" --cuts %*
pause
