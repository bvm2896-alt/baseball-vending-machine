@echo off
chcp 65001 >nul
rem 이슈 한 편 만들기 — 콘티 이름만 주면 prep → (zip 있으면 tts) → render 까지 한 번에.
rem 사용:  이슈만들기.cmd 2026-09-22_이슈
rem 음성:  시스템\work\voice_<콘티>\NN.mp3 가 이미 있으면 그대로 쓰고,
rem        없으면 야구이슈\음성\<콘티>.zip(타입캐스트 문장별 zip)을 찾아 자른다.
rem        둘 다 없으면 대본 파일 위치를 알려 주고 멈춘다.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py 폴더를 못 찾았습니다 & pause & exit /b)
if "%~1"=="" (echo 사용: 이슈만들기.cmd 콘티이름   예^) 이슈만들기.cmd 2026-09-22_이슈 & pause & exit /b)
set EP=%~1
cd /d "%SYS%"
if not exist "episodes\%EP%.json" (echo 콘티가 없습니다: episodes\%EP%.json & pause & exit /b)

echo [1/3] prep
python -X utf8 build.py prep "episodes\%EP%.json" || goto :err

if exist "work\voice_%EP%\00.mp3" (
  echo [2/3] 음성 있음 - work\voice_%EP%\ 그대로 사용
) else if exist "..\야구이슈\음성\%EP%.zip" (
  echo [2/3] tts - zip 자르기
  python -X utf8 tts.py || goto :err
) else (
  echo.
  echo [2/3] 음성이 없습니다.
  echo   1. 야구이슈\음성\%EP%_대본.txt 를 타입캐스트에 붙여 넣고 (장운 / 스마트 이모션 OFF / 1.2x)
  echo   2. 다운로드 - 문장 별로 나누기 - zip 을 야구이슈\음성\%EP%.zip 으로 저장
  echo   3. 이 cmd 를 다시 실행
  pause
  exit /b
)

echo [3/3] render
python -X utf8 build.py render "episodes\%EP%.json" || goto :err
echo.
echo 완료 - 결과는 야구이슈\영상\ 아래 (H: 로 복사되는 설정이면 H: 에도)
pause
exit /b
:err
echo.
echo 실패했습니다. 위 메시지를 확인하세요.
pause
