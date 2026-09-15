@echo off
rem Pull the latest from GitHub (run after pressing save on the other PC)
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
set GITOK=0
if exist ".git" set GITOK=1
if exist "..\.git" set GITOK=1
if "%GITOK%"=="0" (echo This PC is not linked to GitHub yet. Run the pc link cmd first. & pause & exit /b)
echo Saving this PC's local changes first...
git add -A
git commit -q -m "pc update before pull" >nul 2>&1
echo Pulling from GitHub (remote wins on conflict)...
git pull --rebase -X ours || (git rebase --abort & echo Pull failed. Check network/token. & pause & exit /b)
if exist "sync_assets.py" python -X utf8 sync_assets.py
echo.
echo Done. Latest 5 changes:
git log --oneline -5
pause
