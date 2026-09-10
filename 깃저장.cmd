@echo off
chcp 65001 >nul
rem 이 PC의 프로그램·콘티 변경을 깃허브에 저장 (다른 PC로 옮기기 전에 한 번)
cd /d "%~dp0"
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (if exist "run_daily.py" (set SYS=.) else (echo run_daily.py not found & pause & exit /b))
cd /d "%SYS%"
if not exist ".git" (echo 아직 깃허브에 연결되지 않은 PC예요. pc연결.cmd 를 먼저 실행하세요. & pause & exit /b)
git add -A
git commit -q -m "pc update %date% %time%"
git pull -q --rebase
git push
echo.
echo 깃허브 저장 완료. 이제 다른 PC에서 지금실행.cmd 를 누르면 최신 상태로 받아요.
pause
