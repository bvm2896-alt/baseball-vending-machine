@echo off
chcp 65001 >nul
rem Import externally generated voice files (Higgsfield etc.) into work\voice_<episode>\
cd /d "%~dp0"
python -X utf8 import_voice.py work\voice_import.json
pause
