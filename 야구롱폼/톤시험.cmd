@echo off
chcp 65001 >nul
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
cd /d "%SYS%"
echo === A: tonedown ===
python -X utf8 build.py prep episodes/2026-11-27_롱폼톤A.json
python -X utf8 tts.py --chars-ok
echo === B: tonemid ===
python -X utf8 build.py prep episodes/2026-11-27_롱폼톤B.json
python -X utf8 tts.py --chars-ok
echo TONE TEST DONE
pause
