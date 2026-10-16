@echo off
chcp 65001 >nul
rem Draft (1080p 30fps) longform build without the Enter prompt - for Claude clicking. Log: long_draft_log.txt
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
set KBO_DRAFT=1
set KBO_YES=1
set KBO_CHARS_OK=8000
set PYTHONUNBUFFERED=1
echo START %date% %time% > "%~dp0long_draft_log.txt"
title Longform review build - running, do not close
echo ============================================================
echo  Making the longform REVIEW video (1080p).
echo  Nothing new appears here while it works - that is normal.
echo  It takes about 20-40 minutes. Do NOT close this window.
echo  Progress is written to long_draft_log.txt in the longform folder.
echo  When it finishes, the log is shown here and the window waits.
echo ============================================================
python -u -X utf8 "%~dp0_long_build.py" --long %* >> "%~dp0long_draft_log.txt" 2>&1
echo EXIT %errorlevel% %date% %time% >> "%~dp0long_draft_log.txt"
type "%~dp0long_draft_log.txt"
title Longform review build - finished
echo DONE
rem 10/16: keep the window open so the message can be read
pause
