@echo off
chcp 65001 >nul
rem Remote run of the review build (same as the review button). Answers y to the start prompt; output also goes to remote_log.txt.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
set KBO_DRAFT=1
echo Building... progress is written to remote_log.txt
echo y| python -u -X utf8 "%~dp0_long_build.py" --long > "%~dp0remote_log.txt" 2>&1
echo EXIT=%ERRORLEVEL% >> "%~dp0remote_log.txt"
type "%~dp0remote_log.txt"
pause
