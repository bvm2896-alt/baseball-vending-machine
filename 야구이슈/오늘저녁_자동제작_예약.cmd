@echo off
chcp 65001 >nul
rem Double-click ONCE: registers a one-time Windows task that runs _auto_tonight.cmd today at 19:15.
schtasks /create /tn "yagu_auto_tonight" /tr "\"%~dp0_auto_tonight.cmd\"" /sc once /st 19:15 /f
if errorlevel 1 (echo. & echo [FAIL] task not registered. & pause & exit /b)
echo.
echo [OK] Registered: today 19:15 auto build, up to 3 rounds, no upload. Keep the PC and Chrome on, no sleep.
echo      To cancel: schtasks /delete /tn yagu_auto_tonight /f
pause
