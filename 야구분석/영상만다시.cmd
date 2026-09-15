@echo off
chcp 65001 >nul
rem Re-render THIS series only (reuse voices, no TTS credits)
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
set GITOK=0
if exist ".git" set GITOK=1
if exist "..\.git" set GITOK=1
if "%GITOK%"=="1" (git add -A & git commit -q -m "pc update" & (git pull -q --rebase -X theirs || git rebase --abort) & git push -q)
python -X utf8 run_daily.py --now --no-shutdown --no-fetch --no-tts --series analysis %*
pause
