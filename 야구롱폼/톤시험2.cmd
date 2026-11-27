@echo off
chcp 65001 >nul
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
cd /d "%SYS%"
echo === C: tonedown 0.4 ===
set TTS_INTENSITY=0.4
python -X utf8 build.py prep episodes/2026-11-27_롱폼톤C.json
python -X utf8 tts.py --chars-ok
echo === D: tonedown 0.7 ===
set TTS_INTENSITY=0.7
python -X utf8 build.py prep episodes/2026-11-27_롱폼톤D.json
python -X utf8 tts.py --chars-ok
set TTS_INTENSITY=
echo TONE TEST 2 DONE
pause
