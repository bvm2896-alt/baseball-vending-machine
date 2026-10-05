@echo off
chcp 65001 >nul
rem Quick review render of the longform only (no cut shorts): 1080p 30fps, output file gets a review suffix.
rem Same steps as the full build (prep -> tts -> render). Only changed scenes are redrawn.
rem When everything is fixed, run the normal longform build once for the final 2K 60fps video.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
set KBO_DRAFT=1
python -X utf8 "%~dp0_long_build.py" --long %*
pause
