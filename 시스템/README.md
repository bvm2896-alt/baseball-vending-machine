# 야구자판기 자동화 (시스템 폴더)

## 깃허브 저장소 (bvm2896-alt/baseball-vending-machine, 비공개)
- 프로그램·콘티(episodes/)·신호(signals/)·상태(status/오늘.txt)는 이 저장소로 주고받는다. Claude 가 고치면 저장소에 올리고, PC 는 실행할 때마다 `git pull` 로 받는다.
- PC 처음 연결: `pc연결.cmd` 실행 → 토큰 붙여넣기 (Git for Windows 필요). 설정.txt / client_secret.json / token.json 은 PC 에만 두고 절대 올리지 않는다(.gitignore).
- 두 PC(집 sh705 / 회사)를 번갈아 쓰는 규칙: 프로그램은 항상 깃허브가 원본. PC 에서 파일을 직접 고치지 않는다. 실행(지금실행.cmd·아침 자동 실행) 때마다 git pull 로 받고, 오늘 상태(status/state_날짜.json, 오늘.txt)는 저장소에 올려 다른 PC 가 이어받는다. 결과 영상은 구글 드라이브(OUTPUT_DIR).
- 새 작업 PC 추가: Python·Node·ffmpeg 설치 → 폴더 만들고 `pc연결.cmd` → `npm install` → 설정.txt·client_secret.json·token.json 복사 → `작업등록.cmd`.

이 폴더는 프로그램과 작업용 파일이 있는 곳이라 평소에 볼 일이 없어요.
- 완성 영상·썸네일·유튜브 제목/설명  → 상위 폴더 `영상\날짜\번호_팀.mp4` (여기만 보면 됨)
- 오늘 진행 상황                       → 상위 폴더 `오늘.txt`
- 신호 파일(상위 폴더)                 → 공개.txt / 재생성.txt / 종료.txt / 절전.txt

## 매일 돌아가는 순서 (run_daily.py, 07:30)
1. fetch_rank.js, fetch_news.js : 네이버 순위·뉴스 → data/rank_latest.json, data/news_latest.json
2. (Claude 예약 작업) episodes/오늘날짜_1.json, _2.json 콘티 2개 저장  ← run_daily 가 최대 45분 기다림
3. build.py prep  : 콘티의 대사 → work/narration.txt
4. tts.py         : 타입캐스트로 work/voice/00.mp3 ...
5. build.py render: 타임라인 계산 → template.html 에 데이터 주입 → 프레임 렌더 → ../영상/날짜/번호_팀.mp4 (+ _썸네일.jpg, _유튜브.txt)
6. upload.py      : 유튜브에 비공개 업로드 + 썸네일
7. 감시            : 신호 파일 확인 (공개·재생성은 파일 내용에 1 또는 2 를 쓰면 그 영상만, "1 lines=3,7" 이면 그 줄 음성만 다시)
8. 안전 종료 시각(설정.txt SAFETY_SHUTDOWN)에 PC 종료

## 폴더
- episodes/  콘티(JSON). Claude 가 매일 아침 저장
- data/      순위·뉴스 데이터, 실행 로그(run_log.txt, status_날짜.json)
- work/      중간 파일(음성, 프레임, 임시 html) — 매번 덮어써짐, 지워도 됨
- 옛날/      예전 파일 보관
- template.html 화면 틀 / thumb.html 썸네일 틀 / 설정.txt API 키·스케줄
- 작업등록.cmd  윈도우 작업 스케줄러에 07:30 등록(한 번만) / 지금실행.cmd  지금 바로 한 번(종료 안 함)

## 수동 테스트
```
node fetch_rank.js
python -X utf8 build.py prep episodes/2026-09-06_1.json
python -X utf8 tts.py
python -X utf8 build.py render episodes/2026-09-06_1.json
python -X utf8 upload.py auth        (최초 1회)
python -X utf8 upload.py upload "../영상/2026-09-06/1_두산.mp4" episodes/2026-09-06_1.json
```
