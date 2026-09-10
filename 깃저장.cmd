@echo off
rem Save this PC's program/episode changes to GitHub (run once before switching PC)
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
if not exist ".git" (echo This PC is not linked to GitHub yet. Run the link cmd first. & pause & exit /b)
git add -A
git commit -q -m "pc update"
git pull -q --rebase
git push
echo.
echo GitHub save done. On the other PC, run the launcher and it will pull the latest.
pause
