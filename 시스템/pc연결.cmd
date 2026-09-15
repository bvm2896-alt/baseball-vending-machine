@echo off
chcp 65001 >nul
cd /d "%~dp0"
git --version >nul 2>&1 || (echo git 이 없습니다. https://git-scm.com/download/win 에서 설치 후 다시 실행 & pause & exit /b)
set /p TOKEN=깃허브 토큰(github_pat_...)을 붙여넣고 엔터: 
if "%TOKEN%"=="" (echo 토큰이 비었습니다 & pause & exit /b)
if not exist ".git" git init -q -b main
git remote remove origin >nul 2>&1
git remote add origin https://x-access-token:%TOKEN%@github.com/bvm2896-alt/baseball-vending-machine.git
git config user.name "baseball-vending-pc"
git config user.email "pc@baseball-vending.local"
git config core.autocrlf false
git fetch -q origin || (echo 저장소에 접속하지 못했습니다. 토큰을 확인하세요 & pause & exit /b)
git ls-remote --exit-code --heads origin main >nul 2>&1
if %errorlevel%==0 (
  echo 저장소의 최신 버전을 받습니다...
  git reset -q --hard origin/main
  git branch -q -M main
  git branch -q --set-upstream-to=origin/main main
) else (
  echo 저장소가 비어 있어 이 PC 의 프로그램을 처음으로 올립니다...
  git add -A
  git commit -q -m "first upload from PC"
  git branch -q -M main
  git push -q -u origin main || (echo 올리기 실패 & pause & exit /b)
)
echo.
echo 연결 완료.
git log --oneline -3
pause
