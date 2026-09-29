# -*- coding: utf-8 -*-
"""9/30 야구이슈 「아시안게임 야구 스트라이크존은 어땠을까」 콘티 생성 (14줄, pitchZone 장면 5개)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from subdigits import to_digits

def wrap(s, n=16):
    """16자 넘으면 낱말 단위로 두 줄(\n) — 두 줄 길이가 가장 비슷한 자리에서 나눈다."""
    s = s.strip()
    if len(s) <= n: return s
    words = s.split(' '); best = None; bd = 99
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        if len(a) <= n and len(b) <= n and abs(len(a) - len(b)) < bd: best, bd = a + '\n' + b, abs(len(a) - len(b))
    if best: return best
    mid = len(words) // 2 or 1
    return ' '.join(words[:mid]) + '\n' + ' '.join(words[mid:])

SUBFIX = [('사 피안타', '4피안타'), ('이 루', '2루'), ('칠 이닝', '7이닝'), ('삼 이닝', '3이닝')]
def L(narr, **k):
    subs = [to_digits(p.strip()) for p in narr.split(' / ')]
    subs = [re.sub(r',\s*', ' ', p) for p in subs]
    subs = [__import__('functools').reduce(lambda t, ab: t.replace(*ab), SUBFIX, p) for p in subs]
    d = {"narr": narr, "sub": '|'.join(wrap(p) for p in subs)}; d.update(k); return d

END = "채널 구독하고 매일 야구 이슈 받아보세요"
CTA = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
BG = "상황별/주심시점_배경"; BAT = {"img": "상황별/타자_재현_대기"}
def PZ(i, mode): return {"type": "pitchZone", "startLine": i, "mode": mode, "img": BG, "batter": BAT}
def press(i, img, tag): return {"type": "photo", "startLine": i, "img": "상황별/" + img, "text": "", "size": 96, "fit": "contain", "h": 880, "tag": tag}

lines = [
 L("이번 아시안게임엔 ABS가 없었어요 / 그런데 한국은 그것 때문에 지고 / 그것 덕분에 이겼어요"),
 L("케이비오는 이천이십사 년부터 / ABS로 볼 스트라이크를 봐요 / 이번 대회는 주심이 / 볼 스트라이크를 ABS 없이 봤고 / 비디오 판독도 없었어요"),
 L("이틀 전 일본에 영 대 오로 진 날 / 팬들은 스트라이크존이 한국보다 좁다고 했어요 / 케이비오에선 스트라이크인 공이 / 여기선 볼이라고요"),
 L("한신에서 뛴 오승환은 / 전부 변명이다 / 이겼으면 그런 말 안 했을 거라고 했어요"),
 L("그런데 이틀 뒤 결승에서 / 류지현 감독은 심판을 탓하지 않고 / 오히려 심판을 파악했어요"),
 L("주심 존이 바깥쪽으로 공 한두 개 넓다는 걸 / 전력분석팀이 밤을 새워 알아냈다고 해요"),
 L("그래서 타자들한테 / 평소보다 홈플레이트에 바짝 붙어서 치라고 했어요"),
 L("붙으니까 바깥쪽 공이 배트에 닿고 / 투수가 더 바깥으로 던지면 볼이 됐어요"),
 L("이틀 전 한국을 칠 이닝 사 피안타로 막은 히구치가 / 결승에선 삼 이닝에 볼넷 세 개 / 육십 구 만에 내려갔어요"),
 L("판독이 없어서 생긴 장면도 있었어요 / 이 회 이 루에선 태그가 먼저였는데 세이프였고 / 대만 매체는 명백한 오심이라고 썼어요 / 일본은 항의할 방법이 없었어요"),
 L("팔 회엔 김지찬이 협살 중에 / 일본 수비수와 부딪혀 넘어졌는데 / 류지현 감독이 뛰어나가 항의해도 / 아웃은 그대로였어요"),
 L("제 생각엔 이번 대회 심판 존은 / 좁지도 넓지도 않았어요 / 존을 탓한 날은 졌고 / 존을 파악한 날은 이겼어요"),
 L("국제대회에도 ABS가 있어야 할까요 / 심판을 파악하는 것도 실력일까요?", gapAfter=0.5),
 CTA,
]
scenes = [
 PZ(0, "intro"),
 {"type": "cards", "startLine": 1, "title": "볼 스트라이크는 누가 보나", "items": [
   {"badge": "KBO", "name": "ABS\n2024년부터", "sub": "비디오 판독 O"},
   {"badge": "아시안게임", "name": "주심 판정\nABS 없음", "sub": "비디오 판독 X", "hi": True}], "text": "", "size": 80},
 PZ(2, "narrow"),
 press(3, "풀카운트_오승환_보도", "일본 풀카운트 · 9월 27일 · 오승환"),
 {"type": "photo", "startLine": 4, "img": "국가대표프로필/류지현", "text": "심판을 파악했다", "size": 84, "tag": "류지현 감독 · 결승 9월 27일"},
 PZ(5, "outside"),
 PZ(6, "closer"),
 PZ(7, "ball"),
 {"type": "profile", "startLine": 8, "img": "일본대표/히구치", "name": "히구치 신", "sub": "9월 25일 → 9월 27일", "text": "볼넷 0개 → 3개", "textSize": 72,
  "stats": [{"k": "25일", "v": "7이닝 4피안타"}, {"k": "27일", "v": "3이닝 볼넷 3", "hi": True}, {"k": "27일 투구", "v": "60구"}]},
 press(9, "자유시보_2회오심_보도", "대만 자유시보 · 결승 2회"),
 {"type": "photo", "startLine": 10, "img": "상황별/김지찬_홈충돌", "text": "항의해도 그대로", "size": 84, "tag": "8회 · 주루방해 항의 · 판정 유지"},
 {"type": "league", "startLine": 11, "title": "이번 대회 한일전", "rows": [
   {"team": "일본", "rec": "0-5", "sub": "9월 25일 · 존을 탓한 날", "tag": "패"},
   {"team": "일본", "rec": "3-1", "sub": "9월 27일 · 존을 파악한 날", "hi": True, "tag": "승"}], "text": "", "size": 76},
 {"type": "question", "startLine": 12, "text": "국제대회 ABS?", "choices": [{"label": "있어야 한다"}, {"label": "파악도 실력"}]},
]
ep = {
 "date": "2026-09-30", "gameDate": "2026-09-27", "series": "야구이슈", "railTitle": "KBO 이슈", "speed": 1.0, "gapScale": 0.75,
 "ttsApi": True, "ttsTempo": 1.2, "rev": "0930-zone-v1", "focusTeam": "HT", "topic": "스트라이크존",
 "source": ("규정(ABS·비디오 판독 없음, KBO 2024 ABS): 이투데이 2628266. 팬 '존이 좁다' 불만·오승환 '전부 변명·이겼으면 안 했다'(풀카운트 2026/09/27 post2022389) / '경기의 일부'(풀카운트 2026/09/28 post2023017). "
            "류지현 '주심 존이 바깥쪽으로 공 한두 개 넓다는 점을 간파, 전력분석팀이 밤을 지새우며 심판 성향 파악, 홈플레이트에 바짝 붙어 타격 지시': 데일리안 1694778(한국어), NOWnews 6878630(대만). "
            "히구치 9/25 7이닝 92구 4피안타 무실점 볼넷 0 삼진 4(데일리스포츠 0020859978·머니투데이 2026092521210197811·나무위키 일본전) / 9/27 3이닝 4피안타 1실점 볼넷 3 60구(나무위키 결승전 항목, 주간베이스볼 097-20260928-02 '3四死球') — KBO 기록 2차 확인 필요. "
            "2회초 2루 태그 오심(주자 이름 미확인이라 안 부름): 자유시보 5587815 '明顯誤判卻沒輔助判決 南韓隊先馳得點'. 8회 협살 접촉·류지현 항의·판정 유지: 데일리스포츠 0020867320, 스포티비뉴스 1009885, 자유시보 5587894. "
            "타자 이미지는 AI 재현(실제 선수 아님, 로고·번호 없음), 배경은 KIA 제공 사진(9/26 롯데전, 다음 뉴스 mydaily 20260929061202605wedz) 흐림 처리."),
 "lines": lines, "scenes": scenes,
 "thumb": {"img": "국가대표프로필/류지현_상반신", "fit": "cover", "focus": "50% 25%", "top": "아시안게임 야구", "big": "스트라이크존은\n어땠을까", "perLine": True, "teams": [], "logos": False, "color": "#E5484D"},
 "youtube": {
  "title": "아시안게임 야구 스트라이크존은 어땠을까 | ABS 없는 한일전, 0-5 땐 \"존이 좁다\" 결승엔 류지현 \"바깥쪽 넓다, 붙어라\"… 히구치 볼넷 3 #아시안게임야구 #스트라이크존 #ABS",
  "description": ("아시안게임 야구 스트라이크존은 어땠을까요. 이번 대회엔 ABS도 비디오 판독도 없었어요.\n\n"
                  "이틀 전 일본에 0-5로 진 날, 팬들은 '존이 한국보다 좁다'고 했고 오승환은 '전부 변명'이라고 했어요. 그런데 결승에서 류지현 감독은 심판을 탓하지 않고 파악했어요. 주심 존이 바깥쪽으로 공 한두 개 넓다는 걸 전력분석팀이 밤새 알아냈고, 타자들에게 홈플레이트에 바짝 붙어 치라고 했죠. 이틀 전 한국을 7이닝 4피안타로 막은 히구치는 결승에선 3이닝 볼넷 3개, 60구 만에 내려갔어요.\n\n"
                  "판독이 없어서 생긴 장면도 있었어요. 2회 2루 태그(대만 자유시보 '명백한 오심'), 8회 김지찬 협살 접촉과 류지현 감독의 항의.\n\n"
                  "존을 탓한 날은 졌고, 존을 파악한 날은 이겼어요.\n\n"
                  "※ 영상 속 타자 이미지는 실제 선수가 아닌 재현 이미지입니다. 배경 사진: KIA 타이거즈 제공.\n\n"
                  "야구자판기는 야구 이슈를 매일 1분으로 정리해요.\n\n국제대회에도 ABS가 있어야 할까요, 심판을 파악하는 것도 실력일까요?"),
  "tags": ["아시안게임 야구 스트라이크존", "아시안게임 야구 심판", "ABS", "자동 투구 판정", "아시안게임 야구", "한일전", "류지현", "히구치", "오승환", "아시안게임 야구 결승", "비디오 판독", "2026 아시안게임", "아이치 나고야 아시안게임", "야구 대표팀", "류지현호", "한국 야구", "야구 쇼츠", "1분 야구", "야구자판기"],
  "hashtags": ["#Shorts", "#아시안게임야구", "#스트라이크존", "#ABS", "#한일전", "#류지현", "#KBO", "#야구자판기"],
 },
}
out = os.path.join(os.path.dirname(__file__), '..', 'episodes', '2026-09-30_이슈.json')
json.dump(ep, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', out, len(lines), 'lines')
for i, l in enumerate(lines): print(i, l['sub'].replace('\n', '↵'))
