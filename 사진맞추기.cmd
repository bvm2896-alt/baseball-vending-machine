@echo off
chcp 65001 >nul
rem ONE-TIME (this PC only, before gitrestructure): make photo/voice folders match the GitHub assets copy
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
python -X utf8 mirror_from_assets.py
pause
