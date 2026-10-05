@echo off
chcp 65001 >nul
rem Build the latest longform only: prep -> tts -> render. Cut shorts are built by the separate longform-shorts button.
rem run_daily.py does not handle the longform series, so build.py is called directly.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 "%~dp0_long_build.py" --long %*
pause
