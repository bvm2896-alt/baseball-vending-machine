@echo off
chcp 65001 >nul
rem Append the 12-second dark end card (for YouTube end screen) to the already-rendered longform mp4.
rem Safe to run twice: it skips when the card is already there.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 "%~dp0_ending.py"
pause
