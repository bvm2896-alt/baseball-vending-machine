@echo off
chcp 65001 >nul
rem Build THIS series with TODAY's date even after 18:00 (finish today's episodes in the evening)
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
if exist ".git" (git add -A & git commit -q -m "pc update" & (git pull -q --rebase -X theirs || git rebase --abort) & git push -q)
python -X utf8 run_daily.py --now --no-shutdown --today --series rank %*
pause
