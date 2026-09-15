@echo off
chcp 65001 >nul
rem Get the latest program files from GitHub, letting GitHub win over this PC's copies.
rem Use this on the PC you just arrived at, after pressing gitsave on the other PC.
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
if not exist ".git" (echo This PC is not linked to GitHub. & pause & exit /b)
git fetch origin
for /f "delims=" %%B in ('git rev-parse --abbrev-ref HEAD') do set BR=%%B
git reset --hard origin/%BR%
if exist "sync_assets.py" python -X utf8 sync_assets.py
echo.
git log -1 --date=format:"%%Y-%%m-%%d %%H:%%M" --format="Now at: %%ad  %%s"
echo Done. Local program files now match GitHub.
pause
