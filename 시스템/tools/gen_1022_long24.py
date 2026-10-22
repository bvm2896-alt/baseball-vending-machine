# -*- coding: utf-8 -*-
"""10/22 롱폼㉔ 「롯데 방출 16명 — 2억 주고 데려온 최충연도 떠났다」 (방출 시리즈 3편).
대사 = tools/text_1022_long24.py. 근거 = 프로젝트 claude/1022-롱폼24-롯데방출-근거모음.md.
사진: 인물 카드 = 카드/P24_* (0.774) · 16명 얼굴판 = KBO프로필/<이름>_롯데 (나무위키 인포박스 = 구단 프로필)."""
import json, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1022_long24.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]
import narr_1020
def narr_of(t):
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)          # 사 월 → 사월
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)   # 10/18 '이 회'가 지시어로 들림
    return n.replace('KT', '케이티').replace('KIA', '기아').replace('삼 루타', '삼루타').replace('삼 연승', '삼연승')
def sub_of(t): return re.sub(r'\.(?= / )', '', t)

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
RED, GOLD, GRAY, NAVY = "#E5484D", "#E8A100", "#8A93A3", "#3B4A63"
C, K = '카드/P24_', 'KBO프로필/'
IMG = {None: None, "최롯": C + "최충연_롯데", "최롯투": C + "최충연_롯데투구", "최삼": C + "최충연_삼성투구", "최18": C + "최충연_삼성2018",
       "최국대": C + "최충연_대표팀", "최뒤": C + "최충연_삼성뒷모습", "정": C + "정성종_롯데", "이": C + "이인한_롯데"}
def pv(img, name, sub, viz=(), stats=(), **k): return S(0, "pstat", img=IMG.get(img, img), team=k.pop("team", "롯데"), name=name, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, **k)
def sp(img, name, sub, bubbles, **k): return S(0, "speech", img=IMG.get(img, img), team=k.pop("team", "롯데"), name=name, sub=sub, bubbles=bubbles, **k)

POS = [("정성종", "투수"), ("최충연", "투수"), ("석상호", "투수"), ("박로건", "투수"), ("조경민", "투수"), ("박성준", "투수"), ("손준이", "투수"), ("전하원", "투수"),
       ("이인한", "외야수"), ("엄장윤", "외야수"), ("윤수녕", "외야수"), ("김현도", "포수"), ("배인혁", "내야수"), ("박지훈", "내야수"), ("김호범", "내야수"), ("이정민", "내야수")]
OLD3 = ("정성종", "최충연", "이인한")
def prof(n): return K + n + "_롯데"
def F16(text=None, textAt=0.3, hi=(), **k):
    return S(0, "facegrid", title="롯데 · 재계약 불가 16명", cols=8, card=True, chain="f16", profile=True,
             items=[dict(name=n, img=prof(n), team="롯데", pos=p, **({"hi": True} if n in hi else {}), **({"dim": True} if hi and n not in hi else {}),
                         **({"at": 0.2 + i * 0.04} if not k.get("cont") else {})) for i, (n, p) in enumerate(POS)],
             **({"text": text, "textAt": textAt, "size": 56} if text else {}), **k)
REST = [x for x in POS if x[0] not in OLD3]
def F13(hi=(), text=None, textAt=0.3, **k):
    return S(0, "facegrid", title="나머지 13명", cols=7, card=True, chain="f13", profile=True, cont=bool(hi or text) and k.pop("first", False) is False,
             items=[dict(name=n, img=prof(n), team="롯데", pos=p, **({"hi": True} if n in hi else {}), **({"dim": True} if hi and n not in hi else {})) for n, p in REST],
             **({"text": text, "textAt": textAt, "size": 52} if text else {}), **k)
YOUNG = tuple(n for n, _ in POS if n not in OLD3)

SC = []
# ── 오프닝 ──
SC.append(F16(text="올해 방출 발표 구단 중 최다", textAt=2.0))                                                                    # 0
SC.append(pv("최롯", "최충연", "롯데 투수", [], [st("2018 아시안게임", "금메달", 1.0, hi=True)], chain="o1"))                        # 1
SC.append(pv("최롯", "최충연", "롯데 투수", [], [st("2018 아시안게임", "금메달", 0), st("지난겨울 삼성에", "양도금 2억 원", 0.6, hi=True)], chain="o1", cont=True))   # 2
SC.append(pv("최롯", "최충연", "롯데 투수", [], [st("2018 아시안게임", "금메달", 0), st("지난겨울 삼성에", "양도금 2억 원", 0), st("2026년 1군", "1경기 · 1이닝", 0.8, hi=True)], chain="o1", cont=True))   # 3
SC.append(S(0, "toc", on=-1, itemFrom=99))                                                                                   # 4
# ── 1막 · 롯데의 10월 ──
SC.append(S(0, "rankstrip", team="롯데", title="2026 롯데", rows=[dict(k="정규시즌", v="64승 3무 77패", rank=7, at=0)]))           # 5
SC.append(S(0, "rankstrip", team="롯데", title="롯데 · 4년 연속 7위", rows=[dict(k=f"{y}년", v="7위", rank=7, at=k * 0.15) for k, y in enumerate((2023, 2024, 2025, 2026))]))   # 6
SC.append(S(0, "rankstrip", team="롯데", title="롯데 · 마지막 가을야구", rows=[dict(k="2017년", v="3위 · 준플레이오프", rank=3, at=0.3)]))                          # 7
SC.append(pv(None, "롯데 자이언츠", "9월 30일", [], [st("롯데", "키움에 8대 6 승", 0.8), st("같은 날 두산", "NC에 끝내기 승", 1.8), st("결과", "가을야구 탈락 확정", 2.8, hi=True)]))   # 8
SC.append(F16(text="10월 7일 · 투수 8명 · 야수 8명", textAt=1.0, cont=True))                                                     # 8
SC.append(F16(text="16명 중 13명 · 2000년 이후 출생", textAt=0.6, hi=YOUNG, cont=True))                                           # 9
# ── 2막 · 최충연 ──
SC.append(S(0, "photo", img="경기/최충연_롯데투구_2026캠프_OSEN", fit="cover", text="", h=760))                                  # 10
SC.append(pv("최18", "최충연", "삼성 라이온즈 · 경북고", [vsteps([stp("2016년", "삼성 1차 지명", 0.6)])]))                            # 11
SC.append(pv("최18", "최충연", "2018년 삼성", [], [st("경기", "70경기", 0.1), st("이닝", "85이닝", 0.4), st("홀드 · 세이브", "16홀드 8세이브", 1.0), st("평균자책점", "3.60", 1.6, hi=True)]))   # 12
SC.append(pv("최국대", "최충연", "대한민국 대표팀", [vstamp("아시안게임 금메달", 0.6, "gold", size=52)], [st("대회", "2018 자카르타-팔렘방", 0)]))   # 13
SC.append(pv("최뒤", "최충연", "삼성 라이온즈", [vsteps([stp("2020년 1월", "음주운전 · 150경기 출장정지", 0.8, c="bad")])], chain="t14"))   # 14
SC.append(pv("최뒤", "최충연", "삼성 라이온즈", [vsteps([stp("2020년 1월", "음주운전 · 150경기 출장정지", -1, c="bad"), stp("2020년 11월", "팔꿈치 인대 접합 수술", 0.3, c="bad"),
                                                    stp("2021년", "시즌 전체 결장", 1.6)])], chain="t14", cont=True))               # 15
SC.append(pv("최삼", "최충연", "2025년 삼성", [], [st("1군", "4경기", 0.4), st("평균자책점", "37.80", 1.2, hi=True)]))                # 16
SC.append(pv("최롯투", "최충연", "2025년 11월", [vsteps([stp("2차 드래프트", "3라운드 · 롯데", 1.0, c="good")])]))                  # 17
SC.append(pv("최롯투", "최충연", "2차 드래프트란?", [vsteps([stp("1단계", "각 팀이 보호 선수 명단 제출", 0.6), stp("2단계", "명단 밖 선수를 다른 팀이 지명", 1.6, c="good")])]))   # 19
SC.append(pv("최롯투", "최충연", "2025년 11월 · 2차 드래프트", [], [st("롯데 → 삼성", "양도금 2억 원", 0.6, hi=True)]))              # 19
SC.append(pv("최롯", "최충연", "4월 7일 KT전", [], [st("이닝", "1이닝", 0.4), st("피안타", "3개", 1.6), st("실점", "2점", 2.4, hi=True)]))   # 20
SC.append(sp("최롯", "최충연", "4월 · 영상 논란", [bb("4월 10일", "팬 외모 비하 발언 영상 확산", 0.6, src=True)], chain="e21"))          # 21
SC.append(sp("최롯", "최충연", "4월 · 영상 논란", [bb("4월 10일", "팬 외모 비하 발언 영상 확산", 0, src=True), bb("롯데", "1군 말소 · 2군행", 0.6, src=True)], chain="e21", cont=True))   # 22
SC.append(pv("최롯", "최충연", "2026년 2군", [], [st("2군", "5경기", 0.2), st("평균자책점", "1.29", 0.8), st("마지막 등판", "4월 13일", 2.0, hi=True)]))   # 23
SC.append(pv("최롯", "최충연", "1군 통산 · KBO 기록", [], [st("경기", "199경기", 0.1), st("승패", "5승 19패", 0.6), st("세이브 · 홀드", "9세이브 23홀드", 1.4), st("평균자책점", "6.14", 2.4, hi=True)]))   # 24
SC.append(pv("최롯", "최충연", "제 생각", [], [st("바로 1군 자리", "어려움", 1.0), st("2018년처럼 던진다면", "불펜 테스트 가능", 3.0, hi=True)]))   # 25
# ── 3막 · 정성종 · 이인한 · 나머지 13명 ──
SC.append(pv("정", "정성종", "롯데 투수 · 인하대", [], [st("롯데에서", "9년", 0.6)], chain="j26"))                                   # 26
SC.append(pv("정", "정성종", "롯데 투수 · 인하대", [], [st("롯데에서", "9년", 0), st("2018년 드래프트", "2차 2라운드 · 전체 13순위", 1.6, hi=True)], chain="j26", cont=True))   # 27
SC.append(pv("정", "정성종", "1군 통산 · KBO 기록", [], [st("경기", "73경기", 0.2), st("승패", "1승 3패 1홀드", 0.8), st("평균자책점", "5.76", 1.6), st("올해 1군", "0경기", 3.0, hi=True)]))   # 28
SC.append(pv("이", "이인한", "롯데 외야수", [vsteps([stp("2020년", "KIA 입단", 0.6), stp("2024년", "롯데 합류", 1.6, c="good")])]))           # 29
SC.append(pv("이", "이인한", "1군 통산 · KBO 기록", [], [st("경기", "9경기", 0.2), st("타수 · 안타", "4타수 2안타", 0.8), st("타율", "5할", 1.6, hi=True)]))   # 30
SC.append(F13(text="1군 기록이 거의 없는 2000년대생", textAt=0.8, first=True))                                                      # 31
SC.append(F13(hi=("석상호", "박로건", "조경민", "박성준", "손준이", "전하원"), text="투수 6명", textAt=0.2))                       # 32
SC.append(F13(hi=("엄장윤", "윤수녕", "김현도", "배인혁", "박지훈", "김호범", "이정민"), text="야수 7명", textAt=0.2))              # 33
# ── 4막 · 롯데의 겨울과 다른 구단 ──
SC.append(pv(None, "롯데 자이언츠", "이번 겨울", [vsteps([stp("10월 7일", "16명 방출", 0.3)])]))                                        # 35
KTH = "KBO프로필/김태형_감독"
SC.append(pv(KTH, "김태형", "롯데 감독 · 2024~2026", [], [st("계약", "3년 · 24억 원", 0.3), st("3년 순위", "7위 · 7위 · 7위", 1.6, hi=True)], chain="k36", profile=True))   # 36
SC.append(pv(KTH, "김태형", "롯데 감독 · 2024~2026", [], [st("계약", "3년 · 24억 원", 0), st("3년 순위", "7위 · 7위 · 7위", 0), st("외부 FA 영입", "0명", 1.0, hi=True)], chain="k36", cont=True, profile=True))   # 37
SC.append(pv(KTH, "김태형", "롯데 감독 · 2024~2026", [], [st("계약", "3년 · 24억 원", 0), st("3년 순위", "7위 · 7위 · 7위", 0), st("외부 FA 영입", "0명", 0), st("10월 22일", "결과 발표 전", 1.4, hi=True)], chain="k36", cont=True, profile=True))   # 38
SC.append(pv(None, "롯데 감독 후보", "언론 보도 · 10월 19~21일", [], [st("재신임", "김태형", 0.3), st("거론", "이동욱 · 조성환", 1.2, hi=True)]))   # 39
SC.append(pv(None, "롯데 자이언츠", "이번 겨울", [vsteps([stp("11월", "박준혁 단장 계약 만료", 0.6)])], chain="w40"))                  # 40
SC.append(pv(None, "롯데 자이언츠", "이번 겨울", [vsteps([stp("11월", "박준혁 단장 계약 만료", -1), stp("11월 4일", "미야자키 마무리 캠프", 0.3), stp("그 전에", "감독 결정 전망", 2.0, c="good")])], chain="w40", cont=True))   # 41
REY = "KBO프로필/레이예스_롯데"
SC.append(pv(REY, "레이예스", "롯데 외야수 · 2026년", [], [st("안타", "211개", 1.6, hi=True), st("기록", "한 시즌 최다 안타", 2.4)], chain="r42", profile=True))   # 42
SC.append(pv(REY, "레이예스", "롯데 외야수 · 2026년", [], [st("안타", "211개", 0), st("기록", "한 시즌 최다 안타", 0), st("안타왕", "3년 연속", 0.3, hi=True), st("이병규 이후", "처음", 1.6)], chain="r42", cont=True, profile=True))   # 43
_RL = [dict(label="롯데", team="롯데", value=16, unit="명", at=0.6, hi=True), dict(label="두산", team="두산", value=11, unit="명", at=0.6), dict(label="삼성", team="삼성", value=10, unit="명", at=0.6),
       dict(label="SSG", team="SSG", value=8, unit="명", at=0.6), dict(label="키움", team="키움", value=8, unit="명", at=0.6), dict(label="한화", team="한화", value=6, unit="명", at=0.6)]
SC.append(S(0, "bars", title="재계약 불가 · 10월 20일 기준", items=_RL, max=16, chain="b39", text="6개 구단 · 모두 59명", textAt=1.8, size=56))   # 39
SC.append(S(0, "bars", title="재계약 불가 · 10월 20일 기준", items=_RL, max=16, chain="b39", cont=True, text="두산 11명엔 손아섭도", textAt=1.6, size=56))   # 40
SC.append(S(0, "tiles", title="아직 명단 발표 전", items=[dict(team=t, k="10월 22일", v="발표 전", at=0.1 + i * 0.25) for i, t in enumerate(["NC", "KT", "LG", "KIA"])]))   # 41
SC.append(S(0, "question", text="최충연\n다른 팀에서 다시?", img=IMG["최롯"], size=96))   # 10/22 밤 사용자 "마지막 사진 장난하냐" → 흐린 투구 확대 컷 대신 얼굴 정면 사진(R1 때문에 프로필은 못 씀)                                       # 42

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "롯데의 10월", "title": "롯데의 10월", "from": 5, "to": 10},
      {"key": "최충연", "title": "최충연 · 2억 원의 1이닝", "from": 11, "to": 26},
      {"key": "나머지 15명", "title": "정성종 · 이인한 · 나머지 13명", "from": 27, "to": 34},
      {"key": "다른 구단", "title": "롯데의 겨울과 다른 구단", "from": 35, "to": 46}]

TAGS = ["롯데 방출", "최충연 방출", "최충연", "롯데 자이언츠", "재계약 불가", "방출 명단", "2차 드래프트", "정성종", "이인한", "김태형 감독", "프로야구 방출", "2026 방출",
        "레이예스", "손아섭 방출", "프로야구", "KBO", "야구자판기"]
DESC = ("롯데 자이언츠가 10월 7일 선수 16명(투수 8명·야수 8명)에게 재계약 불가를 통보했어요. 올해 방출을 발표한 구단 가운데 가장 많아요.\n\n"
        "명단에는 2018년 아시안게임 금메달리스트 최충연이 있어요. 롯데는 지난해 11월 2차 드래프트 3라운드로 최충연을 뽑으며 삼성에 양도금 2억 원을 냈지만, 최충연은 올해 1군에서 1경기 1이닝(4월 7일 KT전)만 던졌어요. 1군 통산 199경기 5승 19패 9세이브 23홀드 평균자책점 6.14.\n\n"
        "재계약 불가 16명: 투수 정성종·최충연·석상호·박로건·조경민·박성준·손준이·전하원 / 외야수 이인한·엄장윤·윤수녕 / 포수 김현도 / 내야수 배인혁·박지훈·김호범·이정민\n\n"
        "롯데는 올해 64승 3무 77패로 7위, 9년 연속 가을야구에 나가지 못했어요(구단 최장). 김태형 감독의 3년 계약은 올해로 끝났고, 10월 22일 현재 재계약이나 새 감독 선임은 발표되지 않았어요. 레이예스는 211안타로 한 시즌 최다 안타 신기록을 세우고 3년 연속 안타왕에 올랐어요.\n\n"
        "10월 20일 기준 6개 구단(롯데 16명·두산 11명·삼성 10명·SSG 8명·키움 8명·한화 6명)이 모두 59명에게 재계약 불가를 알렸어요.\n\n"
        "여러분은 최충연이 다른 팀에서 다시 기회를 받을 수 있다고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록: KBO 기록실·선수 조회(10월 22일 조회). 기사: SPOTV·재경일보·연합뉴스·OSEN(머니투데이)·마이데일리·스포츠경향·스포츠월드·톱스타뉴스·FT스포츠(10/7), 매일신문(2025/11/19), OSEN(2025/11/20·2026/2/3), 헤럴드경제(4/12), YTN(4/13), 재경일보(10/17), 머니투데이·SPOTV(10/20~21), 마이데일리(10/21), 파이낸셜뉴스·부산일보(10/12~13), 엑스포츠뉴스·일간스포츠(10/19)\n"
        "사진: OSEN, SPOTV(롯데 자이언츠 제공), 구단 공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1022-롱폼24-롯데방출-근거모음.md (기사 본문 2곳 이상 + KBO 선수 조회 생년)."

EP = {"introChapter": "오프닝", "date": "2026-10-22", "gameDate": "2026-10-22", "series": "야구롱폼", "focusTeam": "롯데", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.3,
      "rev": "1022-long24-v3", "topic": "롯데방출", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼24_롯데방출.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "롯데 방출 16명 | 2억 주고 데려온 금메달리스트 최충연도 떠났다 #롯데 #최충연 #방출",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#롯데자이언츠", "#최충연", "#방출", "#재계약불가", "#2차드래프트", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {0: 0.35, 3: 0.35, 4: 0.35, 10: 0.35, 26: 0.4, 34: 0.35, 46: 0.35}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-22_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i + 1, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
