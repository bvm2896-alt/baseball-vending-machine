@echo off
chcp 65001 >nul
rem Update title/description/tags of already-uploaded videos from the episode files (no re-upload)
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
python -X utf8 upload.py update 7tIYwtQkwlM episodes\2026-09-11_1.json
python -X utf8 upload.py update j58njlLdPFA episodes\2026-09-11_2.json
echo.
echo Title/description updated for both videos.
pause
