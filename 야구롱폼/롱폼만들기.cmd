@echo off
chcp 65001 >nul
rem Build the 2026-09-18 longform: prep -> tts (splits the voice zip) -> render -> cut into shorts.
rem run_daily.py does not handle the longform series, so build.py is called directly.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 "%~dp0_long_build.py"
pause
