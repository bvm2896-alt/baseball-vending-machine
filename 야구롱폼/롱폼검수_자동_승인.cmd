@echo off
chcp 65001 >nul
rem Same as the longform review cmd, but starts without the Enter prompt (KBO_YES=1) - for Claude clicking on the PC.
rem Same steps as the full build (prep -> tts -> render). Only changed scenes are redrawn.
rem When everything is fixed, run the normal longform build once for the final 2K 60fps video.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
set KBO_DRAFT=1
set KBO_YES=1
rem 11/9: user approved 4175 chars (4410 with spaces) in chat - skip the char-count prompt
set KBO_CHARS_OK=4500
python -X utf8 tools\long_build.py --long %*
pause
