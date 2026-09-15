@echo off
rem Save this PC's changes to GitHub (run once before switching PC)
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
set GITOK=0
if exist ".git" set GITOK=1
if exist "..\.git" set GITOK=1
if "%GITOK%"=="0" (echo This PC is not linked to GitHub yet. Run the link cmd first. & pause & exit /b)
if exist "sync_assets.py" python -X utf8 sync_assets.py
git add -A
git commit -q -m "pc update"
git pull -q --rebase -X theirs || git rebase --abort
git push
echo.
echo GitHub save done. On the other PC, run gitpull cmd (or the launcher).
pause
