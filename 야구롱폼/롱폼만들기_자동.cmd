@echo off
chcp 65001 >nul
rem Same as the longform build cmd for 2026-11-08_longform (APBC) only, without the Enter prompt (KBO_YES=1).
rem run_daily.py does not handle the longform series, so build.py is called directly.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
set KBO_YES=1
python -X utf8 tools\long_build.py --long 2026-11-08_
pause
