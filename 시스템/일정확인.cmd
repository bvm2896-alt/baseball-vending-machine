@echo off
chcp 65001 >nul
rem Fetch today/tomorrow KBO schedule + probable starters -> data\schedule_latest.json
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
node fetch_schedule.js %*
pause
