@echo off
chcp 65001 >nul
rem Save this PC to GitHub: everything except videos (run once before switching PC)
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
rem 10/16: work is not in git - pack recent voice folders into each series voice folder as zip
if exist "tools\voice_pack.py" python -X utf8 tools\voice_pack.py pack
git add -A
git commit -q -m "pc update" >nul 2>&1
rem 10/16: if the other PC cleaned the git history, match it first (this PC changes are kept)
if exist "tools\git_archive.py" python -X utf8 tools\git_archive.py pullcheck
git add -A
git commit -q -m "pc update" >nul 2>&1
git pull -q --rebase -X theirs || git rebase --abort
git push
echo.
echo GitHub save done. On the other PC, run gitpull cmd (or the launcher).
pause
