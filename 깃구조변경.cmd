@echo off
chcp 65001 >nul
rem ONE-TIME on each PC: move the git repo root from SYS\ up to this folder,
rem so player images, series folders, voices, thumbnails all sync (videos excluded).
rem Run this BEFORE any other git action on this PC once the other PC has done it.
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
if exist ".git" (echo Already moved to this folder. Nothing to do. & pause & exit /b)
if not exist "%SYS%\.git" (echo %SYS%\.git not found. Run the pc link cmd first. & pause & exit /b)
if exist "%SYS%\%SYS%\run_daily.py" (echo Nested folder %SYS%\%SYS% found - an old-layout pull already happened. Ask Claude before continuing. & pause & exit /b)
echo [1/5] Committing this PC's current files (no pull)...
cd /d "%SYS%"
git add -A
git commit -q -m "pc update before restructure" >nul 2>&1
cd /d "%~dp0"
echo [2/5] Moving .git up one level...
attrib -h -s "%SYS%\.git"
move "%SYS%\.git" ".git" >nul || (echo move failed & pause & exit /b)
attrib +h ".git"
copy /y "%SYS%\gitignore_root.txt" ".gitignore" >nul
if exist "%SYS%\.gitignore" del "%SYS%\.gitignore"
echo [3/5] Aligning with GitHub...
git fetch -q origin || (echo fetch failed - check network/token & pause & exit /b)
git reset -q --mixed origin/main
rem if GitHub already has the new layout, restore files this PC lacks (never overwrites local files)
git cat-file -e origin/main:%SYS%/run_daily.py >nul 2>&1 && git checkout-index -a -q
if exist "%SYS%\assets" rmdir /s /q "%SYS%\assets"
echo [4/5] Committing everything (videos and work files excluded)...
git add -A
git commit -q -m "repo root moved to folder root: everything syncs except videos"
echo [5/5] Pushing...
git push -q || (git pull -q --rebase -X theirs && git push -q)
echo.
echo Done. Save = gitsave cmd, fetch = gitpull cmd, same as before.
git log --oneline -3
pause
