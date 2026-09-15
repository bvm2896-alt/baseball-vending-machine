@echo off
chcp 65001 >nul
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
set GITOK=0
if exist ".git" set GITOK=1
if exist "..\.git" set GITOK=1
if "%GITOK%"=="1" (git add -A & git commit -q -m "pc update" & (git pull -q --rebase -X theirs || git rebase --abort) & git push -q)
python -X utf8 run_daily.py --now --no-shutdown %*
pause
