# -*- coding: utf-8 -*-
"""10/23 롱폼㉖ 「LG 방출 11명 — 현대 유니콘스 마지막 선수 장시환도 떠났다」 (방출 시리즈 5편).
대사 = tools/text_1023_long26.py. 근거 = 프로젝트 claude/1023-롱폼26-LG방출-근거모음.md.
사진: 인물 카드 = 카드/P26_* (0.774) · 경기/ (뉴스1·SPOTV) · 11명 얼굴판 = KBO프로필/<이름>_LG (나무위키 인포박스 = 구단 프로필)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1023_long26.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]
import narr_1020
def narr_of(t):
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)
    n = n.replace('KT', '케이티').replace('KIA', '기아').replace('LG', '엘지').replace('SK', '에스케이').replace('십일 월', '십일월').replace('십이 월', '십이월').replace('이~삼 년', '이삼 년')
    n = re.sub(r'(일|이|삼|사|오|육|칠|팔|구|십) 연패', r'\1연패', n)
    return n
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
C, K = '카드/P26_', 'KBO프로필/'
IMG = {None: None, "장불": C + "장시환_LG불펜", "장한": C + "장시환_한화투구", "진": C + "진우영_LG", "염": C + "염경엽_준PO1", "최LG": "카드/P27_최동환_LG우승"}
def pv(img, name, sub, viz=(), stats=(), **k): return S(0, "pstat", img=IMG.get(img, img), team=k.pop("team", "LG"), name=name, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, **k)
def sp(img, name, sub, bubbles, **k): return S(0, "speech", img=IMG.get(img, img), team=k.pop("team", "LG"), name=name, sub=sub, bubbles=bubbles, **k)
def prof(n): return K + n + "_LG"
JP = prof("장시환")
def pj(sub, viz=(), stats=(), **k): return pv(JP, "장시환", sub, viz, stats, profile=True, **k)
POS = [("장시환", "투수"), ("임정균", "투수"), ("하현규", "투수"), ("김주온", "투수"), ("진우영", "투수"), ("김지용", "투수"), ("오승윤", "투수"),
       ("김준태", "포수"), ("김민수", "포수"), ("송대현", "내야수"), ("김정율", "내야수")]
def F11(text=None, textAt=0.3, hi=(), **k):
    return S(0, "facegrid", title="LG · 재계약 불가 11명", cols=6, card=True, chain="f11", profile=True,
             items=[dict(name=n, img=prof(n), team="LG", pos=p, **({"hi": True} if n in hi else {}), **({"dim": True} if hi and n not in hi else {}),
                         **({"at": 0.2 + i * 0.05} if not k.get("cont") else {})) for i, (n, p) in enumerate(POS)],
             **({"text": text, "textAt": textAt, "size": 56} if text else {}), **k)
REST = [("임정균", "투수"), ("하현규", "투수"), ("김지용", "투수"), ("오승윤", "투수"), ("김정율", "내야수"), ("송대현", "내야수 · 은퇴")]

SC = []
# ── 오프닝 ──
SC.append(F11(text="준플레이오프 탈락 이틀 만", textAt=2.6))                                                                   # 0
SC.append(pj("LG 투수 · 39살", [], [st("재계약 불가 명단", "맨 앞", 0.8, hi=True)], chain="o1"))                                   # 1
SC.append(pj("LG 투수 · 39살", [], [st("재계약 불가 명단", "맨 앞", 0), st("현대 유니콘스 출신", "마지막 현역", 0.8, hi=True)], chain="o1", cont=True))   # 2
SC.append(pj("LG 투수 · 39살", [], [st("재계약 불가 명단", "맨 앞", 0), st("현대 유니콘스 출신", "마지막 현역", 0), st("2026년 1군", "0경기", 1.0, hi=True),
                                   st("2026년 2군 공식 경기", "0경기", 1.4, hi=True)], chain="o1", cont=True))                   # 3
SC.append(S(0, "toc", on=-1, itemFrom=99))                                                                                   # 4
# ── 1막 · LG의 10월 ──
SC.append(S(0, "rankstrip", team="LG", title="LG 트윈스", rows=[dict(k="2025년", v="통합우승", rank=1, at=0.3)], chain="r5"))   # 5
SC.append(pv(None, "LG 트윈스", "2026 정규시즌", [], [st("순위", "4위", 0.3, hi=True), st("마무리 유영찬", "4월 말 팔꿈치 부상 · 수술", 1.8)]))   # 6
SC.append(pv(None, "와일드카드 결정전", "10월 14일 · 잠실", [], [st("LG", "4대 1 승", 1.0, hi=True), st("상대", "두산", 1.05)]))            # 7
SC.append(pv(None, "준플레이오프", "LG vs 기아", [vsteps([stp("1차전 · 광주", "1대 5 패", 0.5, c="bad"), stp("2차전 · 광주", "3대 6 패", 1.4, c="bad"), stp("3차전 · 잠실", "1대 13 패", 2.3, c="bad")])]))   # 8
SC.append(S(0, "photo", img="경기/LG_준PO3_인사_1020_뉴스1", fit="cover", text="10월 20일 · 잠실야구장 마지막 경기", h=760))             # 9
SC.append(pv(None, "LG vs 기아", "2026년 맞대결", [], [st("정규시즌 막판", "7연패", 0.2), st("준플레이오프", "3연패", 0.6), st("합계", "기아전 10연패", 1.0, hi=True)]))   # 10
SC.append(F11(text="10월 22일 · 투수 7 · 포수 2 · 내야수 2", textAt=1.0, cont=True))                                            # 11
SC.append(F11(text="장시환 · 송대현 은퇴", textAt=0.4, hi=("장시환", "송대현"), cont=True))                                       # 12
# ── 2막 · 장시환 ──
SC.append(pj("현대 유니콘스 · 2007년", [vsteps([stp("2007년", "2차 1라운드 · 전체 2순위", 0.8, c="good"), stp("당시 이름", "장효훈", 3.0)])]))   # 13
SC.append(pj("20년 동안 거친 팀", [vsteps([stp("2007년", "현대", 0), stp("2008년~", "히어로즈", 0.3), stp("2015년", "KT", 0.55), stp("2017년", "롯데", 0.8), stp("2019년", "한화", 1.05)])]))   # 14
SC.append(pv("장한", "장시환", "마무리 시절", [], [st("2015년 KT", "12세이브", 0.8), st("2022년 한화", "14세이브", 2.6, hi=True)]))   # 15
SC.append(pv("장한", "장시환", "KBO 최다 연패", [], [st("연패", "19연패", 0.5, hi=True), st("기간", "2020년 ~ 2023년", 2.8)]))      # 16
SC.append(pv("장한", "장시환", "2025시즌 뒤", [vsteps([stp("2025시즌 뒤", "한화에서 방출", 0.8, c="bad")])]))                        # 17
SC.append(pv(None, "현대 유니콘스 출신", "2025 시즌 뒤 은퇴", [], [st("정훈", "은퇴", 0.6), st("황재균", "은퇴", 0.9), st("오재일", "은퇴", 1.3),
                                                          st("공통점", "모두 현대 출신", 2.0, hi=True)], team="LG"))                   # 18
SC.append(pv(None, "현대 유니콘스 출신 현역", "2025년 12월", [], [st("남은 선수", "장시환 1명", 0.4, hi=True), st("장시환 은퇴 시", "0명", 1.8)]))   # 19
SC.append(pj("2025년 12월", [vsteps([stp("2025년 12월", "LG 입단", 0.4, c="good")])], [st("연봉", "1억 원", 1.6, hi=True)]))        # 20
SC.append(sp("장불", "장시환", "2025년 12월 ~ 2026년 1월", [bb("2025년 12월", "1군에 있으면서, 박수받으며 떠나고 싶었다", 0.6, src=True),
                                                      bb("2026년 1월 · 신년인사회", "'마지막 유산' 소리를 2~3년은 더 들어야 할 것 같다", 50, src=True)], chain="s21"))   # 10/23: 다음 장면 말풍선 자리를 미리 잡아(at 50) 카드가 위아래로 안 움직이게   # 10/23: 앞뒤 프로필 장면과 사진이 같으면 자리만 옮겨 튀어 보임 → 다른 사진(LG 불펜)   # 21
SC.append(sp("장불", "장시환", "2025년 12월 ~ 2026년 1월", [bb("2025년 12월", "1군에 있으면서, 박수받으며 떠나고 싶었다", 0, src=True),
                                                      bb("2026년 1월 · 신년인사회", "'마지막 유산' 소리를 2~3년은 더 들어야 할 것 같다", 0.6, src=True)], chain="s21", cont=True))   # 22
SC.append(pj("2026년", [], [st("1군", "0경기", 0.6, hi=True), st("2군 공식 경기", "0경기", 1.4, hi=True)]))                        # 23
SC.append(pv("장한", "장시환", "1군 통산 · KBO 기록", [], [st("경기", "416경기", 0.1), st("이닝", "787이닝", 0.6), st("승패", "29승 74패", 1.3),
                                                      st("세이브 · 홀드", "34세이브 35홀드", 2.0), st("평균자책점", "5.31", 3.0, hi=True)]))   # 24
SC.append(pj("2026년 10월 22일 · 은퇴", [vstamp("현대 유니콘스 출신 현역 0명", 0.8, "bad", size=48)]))                            # 25
# ── 3막 · 진우영 · 김준태 · 김민수 · 나머지 ──
SC.append(pv("진", "진우영", "LG 투수", [], [st("2024년 드래프트", "4라운드", 0.6, hi=True)]))                                     # 26
SC.append(pv("진", "진우영", "돌아온 길", [vsteps([stp("고교", "글로벌선진학교", 0.4), stp("미국", "캔자스시티 로열스 계약", 1.6, c="good")])], chain="j27"))   # 27
SC.append(pv("진", "진우영", "돌아온 길", [vsteps([stp("고교", "글로벌선진학교", -1), stp("미국", "캔자스시티 로열스 계약", -1, c="good"), stp("2021년", "미국에서 방출", 0.3, c="bad")])], chain="j27", cont=True))   # 28
SC.append(pv("진", "진우영", "돌아온 길", [vsteps([stp("고교", "글로벌선진학교", -1), stp("미국", "캔자스시티 로열스 계약", -1, c="good"), stp("2021년", "미국에서 방출", -1, c="bad"),
                                               stp("군 복무 뒤", "독립리그 파주 챌린저스", 0.8)])], chain="j27", cont=True))           # 29
SC.append(pv("진", "진우영", "돌아온 길", [vsteps([stp("고교", "글로벌선진학교", -1), stp("미국", "캔자스시티 로열스 계약", -1, c="good"), stp("2021년", "미국에서 방출", -1, c="bad"),
                                               stp("군 복무 뒤", "독립리그 파주 챌린저스", -1), stp("2024년", "LG 4라운드 · 전체 38순위", 0.8, c="good")])], chain="j27", cont=True))   # 30
SC.append(pv("진", "진우영", "1군 기록", [], [st("2024년", "6경기 · 평균자책점 4.70", 0.4), st("2025 ~ 2026년", "1군 0경기", 2.6, hi=True)]))   # 31
SC.append(pv(prof("김준태"), "김준태", "LG 포수", [vsteps([stp("시작", "롯데 육성선수", 1.0), stp("그 뒤", "상무 · KT", 2.2)])], profile=True))   # 32
SC.append(pv(prof("김준태"), "김준태", "2025년 6월 트레이드", [], [st("LG가 내준 선수", "임준형", 0.8), st("LG가 받은 선수", "천성호 · 김준태", 1.8, hi=True)], profile=True))   # 33
SC.append(pv(prof("김준태"), "김준태", "1군 통산 · KBO 기록", [], [st("경기", "520경기", 0.2), st("타율", "2할 3푼", 0.8), st("홈런", "18개", 1.4), st("2026년 1군", "0경기", 2.6, hi=True)], profile=True))   # 34
SC.append(pv(prof("김민수"), "김민수", "LG 포수", [vsteps([stp("2025년 겨울", "삼성에서 방출", 0.8, c="bad"), stp("2025년 12월", "장시환과 함께 LG행", 2.2, c="good")])], profile=True))   # 35
SC.append(S(0, "facegrid", title="지난겨울 함께 온 두 사람", cols=2, card=True, profile=True,
             items=[dict(name=n, img=prof(n), team="LG", pos=p, at=0.2 + i * 0.3) for i, (n, p) in enumerate([("장시환", "투수 · 은퇴"), ("김민수", "포수")])],
             text="1년 만에 이별", textAt=1.4, size=56))                                                                         # 36
SC.append(pv(prof("김주온"), "김주온", "LG 투수", [vsteps([stp("2015년", "삼성 지명", 0.6), stp("그 뒤", "SK · SSG", 1.2), stp("2024년", "LG", 1.8, c="good")])], profile=True))   # 37
SC.append(S(0, "facegrid", title="나머지 6명", cols=6, card=True, profile=True,
             items=[dict(name=n, img=prof(n), team="LG", pos=p, at=0.1 + i * 0.35) for i, (n, p) in enumerate(REST)]))           # 38
# ── 4막 · LG의 겨울과 다른 구단 ──
SC.append(pv(None, "LG 트윈스", "이번 겨울", [vsteps([stp("10월 22일", "11명 재계약 불가", 0.3, c="bad")])]))                       # 39
YK = K + "염경엽_감독"
SC.append(pv(YK, "염경엽", "LG 감독", [], [st("2025년 11월", "재계약", 0.6), st("조건", "3년 · 최대 30억 원", 1.6, hi=True)], profile=True))   # 40
SC.append(sp("염", "염경엽", "준플레이오프 탈락 뒤", [bb("탈락 뒤", "준비에 부족한 부분이 있었다", 1.0, src=True), bb("다음", "마무리 훈련부터 잘 준비", 2.0, src=True)]))   # 41
SC.append(pv(K + "홍창기", "홍창기", "LG 외야수", [], [st("이번 겨울", "FA 자격", 1.0, hi=True)], profile=True))   # 42
SC.append(pv("최LG", "최동환", "LG에서 16년", [], [st("같은 날 KT", "10명 재계약 불가", 1.0), st("그 명단에", "최동환", 2.6, hi=True)], team="LG"))   # 43
_RL = [dict(label="롯데", team="롯데", value=16, unit="명", at=0.6), dict(label="두산", team="두산", value=11, unit="명", at=0.6), dict(label="LG", team="LG", value=11, unit="명", at=0.6, hi=True),
       dict(label="삼성", team="삼성", value=10, unit="명", at=0.6), dict(label="KT", team="KT", value=10, unit="명", at=0.6, hi=True), dict(label="SSG", team="SSG", value=8, unit="명", at=0.6),
       dict(label="키움", team="키움", value=8, unit="명", at=0.6), dict(label="한화", team="한화", value=6, unit="명", at=0.6)]
SC.append(S(0, "bars", title="재계약 불가 · 10월 22일 기준", items=_RL, max=16, text="10월 22일 하루 21명 · 발표 인원 합계 80명", textAt=2.0, size=56))   # 44
SC.append(S(0, "tiles", title="아직 발표 소식 없음", items=[dict(team=t, k="10월 22일 기준", v="발표 소식 없음", at=0.1 + i * 0.3) for i, t in enumerate(["NC", "KIA"])]))   # 45
SC.append(S(0, "question", text="장시환의 마지막이\n1군 마운드였다면?", img=IMG["장한"], size=88))                                 # 46

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "LG의 10월", "title": "LG의 10월", "from": 5, "to": 12},
      {"key": "장시환", "title": "장시환 · 현대 유니콘스의 마지막 선수", "from": 13, "to": 25},
      {"key": "진우영 · 김준태", "title": "진우영 · 김준태 · 김민수 · 나머지", "from": 26, "to": 38},
      {"key": "다른 구단", "title": "LG의 겨울과 다른 구단", "from": 39, "to": 46}]

TAGS = ["LG 방출", "장시환 은퇴", "장시환", "현대 유니콘스", "LG 트윈스", "재계약 불가", "방출 명단", "진우영", "김준태", "김민수", "송대현", "염경엽", "홍창기 FA",
        "최동환 방출", "KT 방출", "프로야구 방출", "2026 방출", "프로야구", "KBO", "야구자판기"]
DESC = ("LG 트윈스가 준플레이오프 탈락 이틀 만인 10월 22일 선수 11명(투수 7명·포수 2명·내야수 2명)과 재계약하지 않기로 했어요. 장시환과 송대현은 은퇴를 결정했어요.\n\n"
        "장시환은 2007년 현대 유니콘스 2차 1라운드 전체 2순위(당시 이름 장효훈)로 입단해 히어로즈·KT·롯데·한화를 거쳤고, 지난해 12월 연봉 1억 원에 LG와 계약했어요. "
        "정훈·황재균·오재일이 은퇴한 뒤 남은 마지막 현대 출신 현역이었지만, 올해는 1군은 물론 2군 공식 경기에도 나서지 못했어요. 1군 통산 416경기 787이닝 29승 74패 34세이브 35홀드 평균자책점 5.31.\n\n"
        "재계약 불가 11명: 투수 장시환(은퇴)·임정균·하현규·김주온·진우영·김지용·오승윤 / 포수 김준태·김민수 / 내야수 송대현(은퇴)·김정율\n\n"
        "LG는 지난해 통합우승 뒤 올해 정규시즌 4위, 와일드카드 결정전에서 두산을 꺾었지만 준플레이오프에서 기아에 3연패했어요. 3차전은 44년 잠실야구장의 마지막 경기였어요.\n\n"
        "같은 날 KT도 10명과 재계약하지 않기로 했어요(LG에서 16년을 보낸 최동환 포함). 10월 22일 기준 8개 구단의 발표 인원을 모두 더하면 80명이에요(LG는 은퇴 2명 포함).\n\n"
        "여러분은 장시환의 마지막이 1군 마운드였다면 어땠을 것 같나요? 댓글로 남겨 주세요.\n\n"
        "기록: KBO 기록실(10월 22일 조회). 기사: 스타뉴스·마이데일리·일간스포츠·더게이트·이투데이·STN·시대일보·위키트리·미디어펜·뉴스1·뉴스핌·MHN·오마이스타·알파경제·재경일보(10/22), "
        "OSEN(2025/12/22·2026/1/6), 트윅(1/6), 더게이트(2025/12/23), 뉴시스(2023/9/14), 스포츠경향(2025/6/25), 연합뉴스(2025/11/9), 세계일보·서울신문·경향신문(10/20~21), 노컷뉴스(5/4), 위키트리(10/15·10/21)\n"
        "사진: 뉴스1, SPOTV, 구단 공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1023-롱폼26-LG방출-근거모음.md (기사 본문 2곳 이상 + KBO 기록실)."

EP = {"introChapter": "오프닝", "date": "2026-10-23", "gameDate": "2026-10-23", "series": "야구롱폼", "focusTeam": "LG", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.3,
      "rev": "1023-long26-v2", "topic": "LG방출", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼26_LG방출.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "LG 방출 11명 | 현대 유니콘스 마지막 선수 장시환도 떠났다 #LG #장시환 #방출",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#LG트윈스", "#장시환", "#현대유니콘스", "#방출", "#재계약불가", "#진우영", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {0: 0.35, 3: 0.35, 4: 0.35, 12: 0.35, 14: 0.8, 25: 0.4, 38: 0.35, 45: 0.35}   # 14: 팀 다섯 칸 읽을 시간
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-23_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i + 1, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
