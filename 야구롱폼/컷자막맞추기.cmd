@echo off
chcp 65001 >nul
rem Re-detect subtitle breath boundaries of the latest cut shorts voices (no new voice synthesis, no credit).
rem Cuts whose subtitle timing changed are marked to be rebuilt. Then run the shorts build cmd.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 tools\fix_segs.py %*
pause
