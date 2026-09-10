@echo off
chcp 65001 >nul
rem Re-render video only (reuse voices, no TTS credits)
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
if exist ".git" (git add -A & git commit -q -m "pc update" & git pull -q --rebase & git push -q)
python -X utf8 run_daily.py --now --no-shutdown --no-fetch --no-tts %*
pause
