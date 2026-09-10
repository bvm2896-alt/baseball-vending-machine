@echo off
chcp 65001 >nul
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
if exist ".git" git pull -q --ff-only
python -X utf8 run_daily.py --now --no-shutdown %*
pause
