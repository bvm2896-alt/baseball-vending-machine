@echo off
chcp 65001 >nul
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
cd /d "%SYS%"
set TTS_INTENSITY=0.4
python -X utf8 build.py prep episodes/2026-11-27_롱폼고침.json
python -X utf8 tts.py --chars-ok
set TTS_INTENSITY=
echo FIX VOICE DONE
pause
