@echo off
chcp 65001 >nul
rem Build the two 10/1 issue episodes (issue, issue2) while the rank window is still running.
rem Separate work folder, no git sync, no data fetch. Voice: Typecast API.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 "%~dp0_two_build.py" %*
pause
