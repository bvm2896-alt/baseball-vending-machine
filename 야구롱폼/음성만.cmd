@echo off
chcp 65001 >nul
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
cd /d "%SYS%"
python -X utf8 tools\voice_only_1012.py
pause
