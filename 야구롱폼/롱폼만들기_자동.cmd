@echo off
chcp 65001 >nul
rem Same as the longform build cmd (latest longform episode), without the Enter prompt (KBO_YES=1) - for Claude clicking on the PC.
rem 11/14: was hardcoded to 2026-11-08_ (APBC) - now builds the latest date like the review cmd.
rem run_daily.py does not handle the longform series, so build.py is called directly.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
set KBO_YES=1
python -X utf8 tools\long_build.py --long %*
pause
