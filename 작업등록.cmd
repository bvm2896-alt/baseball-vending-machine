@echo off
chcp 65001 >nul
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
set HERE=%~dp0%SYS%
schtasks /Delete /TN "BaseballVending" /F >nul 2>&1
schtasks /Delete /TN "야구자판기" /F >nul 2>&1
schtasks /Create /SC DAILY /ST 07:30 /TN "BaseballVending" /RL HIGHEST /F /TR "cmd /c cd /d \"%HERE%\" && python -X utf8 run_daily.py > data\run_log.txt 2>&1"
if %errorlevel%==0 (echo OK: every day 07:30) else (echo FAILED - run as administrator)
pause
