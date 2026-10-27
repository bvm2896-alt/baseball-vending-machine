@echo off
chcp 65001 >nul
rem FINAL 2K 60fps render of ONLY the new PO game-2 review longform made by Claude (episodes\2026-10-27_longform2.json). Does not touch the editor chat file.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 tools\long_build.py --long 2026-10-27_롱폼2
pause
