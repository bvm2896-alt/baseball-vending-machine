@echo off
chcp 65001 >nul
rem 10/18 PO2 FINAL 2K render (episode 2026-10-18_[long]2.json) - can run while another longform is rendering: own work folder work\po2
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
set KBO_DRAFT=
set KBO_WORK=work\po2
if not exist "work\po2" mkdir "work\po2"
python -X utf8 tools\long_build.py --long 2026-10-18_롱폼2
pause
