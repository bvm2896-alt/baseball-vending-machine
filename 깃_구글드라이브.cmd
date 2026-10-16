@echo off
chcp 65001 >nul
rem Move finished-video files (7+ days old) from git to Google Drive, then erase them from git history.
rem Run on the PC that has the Google Drive folder (home). Asks Y before changing anything.
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
set GITOK=0
if exist ".git" set GITOK=1
if exist "..\.git" set GITOK=1
if "%GITOK%"=="0" (echo This PC is not linked to GitHub yet. & pause & exit /b)
if exist "tools\voice_pack.py" python -X utf8 tools\voice_pack.py pack
python -X utf8 tools\git_archive.py archive
pause
