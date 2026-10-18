@echo off
chcp 65001 >nul
rem 10/19 PO2 cut shorts 5 (own work folder work\po2cuts)
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
set KBO_DRAFT=
set KBO_WORK=work\po2cuts
if not exist "work\po2cuts" mkdir "work\po2cuts"
python -X utf8 tools\long_build.py --cuts 2026-10-19_롱폼컷
pause
