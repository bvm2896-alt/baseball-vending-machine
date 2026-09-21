@echo off
chcp 65001 >nul
rem Cut chapters 2-4 of the 2026-09-18 longform into three shorts (2026-09-21 issue2/3/4) and render them.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 "%~dp0_shorts_build.py"
pause
