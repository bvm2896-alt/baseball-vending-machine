# -*- coding: utf-8 -*-
"""10/21 롱폼㉓ 「SSG 방출 8명 — 5년 65억 박종훈도 떠났다」 (방출 시리즈 2편 · 타입캐스트 웹 zip).
대사 = tools/text_1021_long23.py (v1.1). 근거 = 프로젝트 claude/1021-롱폼23-SSG방출-근거모음.md.
사진: 인물 카드 = 카드/P23_* (0.774) · 8명 얼굴판 = KBO프로필/<이름>_SSG (나무위키 인포박스 = 구단 프로필)."""
import json, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1021_long23.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]
import narr_1020
def narr_of(t):
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)          # 사 월 → 사월
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)   # 10/18 '이 회'가 지시어로 들림
    return n.replace('SK', '에스케이')
def sub_of(t): return re.sub(r'\.(?= / )', '', t)

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
RED, GOLD, GRAY, NAVY = "#E5484D", "#E8A100", "#8A93A3", "#3B4A63"
C, K = '카드/P23_', 'KBO프로필/'
IMG = {None: None, "박D": C + "박종훈_포효", "박SK": C + "박종훈_SK", "박국대": C + "박종훈_대표팀", "박KS": C + "박종훈_KS2022", "아빌라": C + "아빌라_포효"}
def pv(img, name, sub, viz=(), stats=(), **k): return S(0, "pstat", img=IMG[img], team=k.pop("team", "SSG"), name=name, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, **k)
def sp(img, name, sub, bubbles, **k): return S(0, "speech", img=IMG[img], team=k.pop("team", "SSG"), name=name, sub=sub, bubbles=bubbles, **k)
def steps(title, items, **k): return S(0, "steps", title=title, items=[dict(date=d, text=t, at=a, **({"hi": True} if h else {})) for d, t, a, h in items], **k)

POS = [("박종훈", "투수"), ("김성민", "투수"), ("김준영", "투수"), ("안현서", "투수"), ("이승훈", "투수"), ("한지헌", "투수"), ("석정우", "내야수"), ("박정빈", "외야수")]
def prof(n): return K + n + "_SSG"
def F8(text=None, textAt=0.3, **k):
    return S(0, "facegrid", title="SSG · 재계약 불가 8명", cols=6, card=True, chain="f8", profile=True,
             items=[dict(name=n, img=prof(n), team="SSG", pos=p, **({"at": 0.2 + i * 0.05} if not k.get("cont") else {})) for i, (n, p) in enumerate(POS)],
             **({"text": text, "textAt": textAt, "size": 56} if text else {}), **k)
SEVEN = POS[1:]
def F7(hi=(), text=None, textAt=0.3, **k):
    return S(0, "facegrid", title="나머지 7명", cols=5, card=True, chain="f7", profile=True, cont=bool(hi or text),
             items=[dict(name=n, img=prof(n), team="SSG", pos=p, **({"hi": True} if n in hi else {}), **({"dim": True} if hi and n not in hi else {})) for n, p in SEVEN],
             **({"text": text, "textAt": textAt, "size": 52} if text else {}), **k)

SC = []
# ── 오프닝 ──
SC.append(F8())                                                                                                              # 0
SC.append(pv("박KS", "박종훈", "SSG 투수 · 잠수함", [], [st("한국시리즈 우승", "2018 · 2022", 1.0, hi=True)], chain="o1"))          # 1
SC.append(pv("박KS", "박종훈", "SSG 투수 · 잠수함", [], [st("한국시리즈 우승", "2018 · 2022", 0), st("2021년 12월", "5년 65억 원", 0.6, hi=True)], chain="o1", cont=True))   # 2
SC.append(pv("박KS", "박종훈", "SSG 투수 · 잠수함", [], [st("한국시리즈 우승", "2018 · 2022", 0), st("2021년 12월", "5년 65억 원", 0), st("2026년 1군", "0경기", 1.2, hi=True)], chain="o1", cont=True))   # 3
SC.append(S(0, "toc", on=-1, itemFrom=99))                                                                                   # 4
# ── 1막 · SSG의 10월 ──
SC.append(S(0, "rankstrip", team="SSG", title="2026 SSG", rows=[dict(k="정규시즌", v="65승 5무 74패", rank=6, at=0)]))            # 5
SC.append(S(0, "tiles", title="2026 SSG", items=[dict(team="SSG", k="전반기", v="9위", at=0.2), dict(team="SSG", k="후반기 · 34승 2무 22패", v="2위", at=1.6)]))   # 6
SC.append(F8(text="10월 10일 · 재계약 불가 통보", textAt=1.4, cont=True))                                                         # 7
SC.append(F8(text="투수 6명 · 야수 2명", textAt=0.2, cont=True))                                                                  # 8
# ── 2막 · 박종훈 ──
SC.append(S(0, "photo", img="경기/박종훈_포효_0628_OSEN", fit="cover", text="", h=760))                                         # 9
SC.append(pv("박SK", "박종훈", "SK 와이번스 · 군산상고", [vsteps([stp("2010년", "SK 2라운드 입단", 0.6)])], chain="s10"))           # 10
SC.append(pv("박SK", "박종훈", "SK 와이번스 · 군산상고", [vsteps([stp("2010년", "SK 2라운드 입단", -1), stp("투구 방식", "잠수함 · 언더핸드", 0.4, c="good")])], chain="s10", cont=True))   # 11
SC.append(S(0, "bars", title="박종훈 · 두 자릿수 승리", items=[dict(label="2017년", value=12, unit="승", at=0.2), dict(label="2018년", value=14, unit="승", at=0.9, hi=True),
                                                      dict(label="2020년", value=13, unit="승", at=1.6)], max=15, text="두 자릿수 승리 3번", textAt=2.6, size=56))   # 12
SC.append(pv("박SK", "박종훈", "2018년 SK", [vstamp("한국시리즈 우승", 1.0, "gold", size=52)], [st("정규시즌", "14승 8패", 0)]))      # 13
SC.append(pv("박국대", "박종훈", "대한민국 대표팀", [vsteps([stp("2018년", "아시안게임 금메달", 0.8, c="good"), stp("2019년", "프리미어12", 2.0)])]))   # 14
SC.append(S(0, "steps", title="박종훈 · 2021년", items=[dict(date="6월", text="팔꿈치 인대 접합 수술", at=0.6), dict(date="12월", text="5년 65억 · 국내 첫 비FA 다년계약", hide=True)], chain="t15"))                                     # 15
SC.append(steps("박종훈 · 2021년", [("6월", "팔꿈치 인대 접합 수술", 0, False), ("12월", "5년 65억 · 국내 첫 비FA 다년계약", 0.6, True)], chain="t15", cont=True))   # 16
SC.append(S(0, "tiles", title="비FA 다년계약", items=[dict(team="SSG", k="언제", v="FA 되기 전", at=0.2), dict(team="SSG", k="무엇을", v="여러 해 계약\n미리 묶기", at=1.2),
                                                   dict(team="SSG", k="박종훈", v="5년 65억", at=2.4)]))                           # 17
SC.append(pv("박KS", "박종훈", "2022년 한국시리즈 3차전", [vsteps([stp("8회 무사 2루", "구원 등판", 0.3), stp("1이닝", "무실점", 2.0, c="good")])],
             [st("그해 SSG", "통합 우승", 5.0, hi=True)]))                                                                        # 18
_ERA = [dict(label="2022년", value=6.00, dec=2, at=0.3), dict(label="2023년", value=6.19, dec=2, at=0.6), dict(label="2024년", value=6.94, dec=2, at=0.9), dict(label="2025년", value=7.11, dec=2, at=1.2)]
SC.append(S(0, "bars", title="박종훈 · 1군 평균자책점", items=_ERA, max=8, chain="b19", text="수술 뒤 4년", textAt=1.0, size=52))                                          # 19
SC.append(S(0, "bars", title="박종훈 · 1군 평균자책점", items=_ERA, max=8, chain="b19", cont=True, text="4년 합계 44경기 6승 17패 · 6.38", textAt=0.3, size=52))   # 20
SC.append(S(0, "bars", title="박종훈 · 1군 평균자책점", items=[dict(x, at=0, **({"hi": True} if x["label"] == "2025년" else {})) for x in _ERA], max=8, chain="b19", cont=True,
             text="2025년 1군 5경기 · 7.11", textAt=0.3, size=52))                                                                 # 21
SC.append(pv("박D", "박종훈", "2026년", [], [st("1군", "0경기", 0.3, hi=True), st("2군", "21경기 · 평균자책점 3.51", 2.0)]))           # 22
SC.append(pv("박D", "박종훈", "10월 10일", [vstamp("서로 합의해 계약 해지", 1.2, "bad", size=46)]))                                  # 23
SC.append(sp(None, "SSG 랜더스", "10월 10일 구단 설명", [bb("공로", "두 번의 우승 기여", 0.4, src=True), bb("이유", "새 팀 찾을 시간", 2.4, src=True)]))   # 24
SC.append(pv("박D", "박종훈", "통산 · KBO 기록", [], [st("경기", "245경기", 0.1), st("승패", "72승 79패", 0.8), st("평균자책점", "4.85", 1.6, hi=True)]))   # 25
SC.append(pv("박D", "박종훈", "1991년생", [], [st("지금", "35살", 0.1), st("은퇴 대신", "현역 연장", 1.2, hi=True), st("몸 상태", "아픈 곳 없음", 2.6)]))   # 26
SC.append(sp("박D", "박종훈", "10월 21일 기준", [bb("관심 보인 구단", "기사 없음", 0.4, src=True)]))                                 # 27
SC.append(pv("박D", "박종훈", "제 생각", [], [st("선발 자리", "약속받기 어려움", 2.4), st("잠수함 불펜", "적은 몸값으로 기회", 6.0, hi=True)]))   # 28
# ── 3막 · 나머지 7명 ──
SC.append(F7(hi=("석정우",), text="올해 1군에 오른 선수 · 석정우 1명", textAt=1.0))                                                  # 29
SC.append(F7(hi=("김성민",), text="김성민 · 2020년 2차 2라운드 · 2군 평균자책점 11.74", textAt=0.8))                                 # 30
SC.append(F7(hi=("김준영",), text="김준영 · 2023년 11라운드 · 2군 2세이브 2홀드", textAt=0.8))                                      # 31
SC.append(F7(hi=("안현서", "이승훈"), text="안현서 4라운드 · 이승훈 9라운드 · 올해 2군 기록 없음", textAt=0.8))                     # 32
SC.append(F7(hi=("한지헌",), text="한지헌 · 경희대 얼리 드래프트 · 2025년 10라운드", textAt=0.8))                                   # 33
SC.append(F7(hi=("박정빈",), text="박정빈 · 2021년 2차 5라운드 · 2군 43경기 타율 2할 4푼 5리", textAt=0.8))                        # 34
SC.append(F7(hi=("석정우",), text="석정우 · 2022년 육성선수 · 1군 3경기 · 2군 타율 2할 4푼 3리", textAt=0.8))                     # 35
# ── 4막 · SSG의 겨울과 다른 구단 ──
SC.append(steps("SSG의 겨울", [("10월 10일", "8명 재계약 불가", 0, False), ("10월 15일", "박정권 2군 감독 계약 종료", 1.4, False), ("10월 16일", "아빌라 최대 2년 재계약", 3.4, True)]))   # 36
SC.append(pv("아빌라", "아빌라", "SSG 외국인 투수 · 2026년", [], [st("경기", "14경기", 0.1), st("승패", "9승 2패", 0.6), st("평균자책점", "1.44", 1.4, hi=True)]))   # 37
_RL = [dict(label="롯데", team="롯데", value=16, unit="명", at=0.6), dict(label="두산", team="두산", value=11, unit="명", at=0.6), dict(label="삼성", team="삼성", value=10, unit="명", at=0.6),
       dict(label="SSG", team="SSG", value=8, unit="명", at=0.6, hi=True), dict(label="키움", team="키움", value=8, unit="명", at=0.6), dict(label="한화", team="한화", value=6, unit="명", at=0.6)]
SC.append(S(0, "bars", title="재계약 불가 · 10월 21일 기준", items=_RL, max=16, chain="b38", text="6개 구단 · 모두 59명", textAt=1.8, size=56))   # 38
SC.append(S(0, "bars", title="재계약 불가 · 10월 21일 기준", items=_RL, max=16, chain="b38", cont=True, text="두산 11명엔 손아섭도", textAt=1.6, size=56))   # 39
SC.append(S(0, "tiles", title="아직 명단 발표 전", items=[dict(team=t, k="10월 21일", v="발표 전", at=0.1 + i * 0.25) for i, t in enumerate(["NC", "KT", "LG", "KIA"])]))   # 40
SC.append(S(0, "question", text="박종훈\n다시 1군 마운드에?", img=IMG["박D"], size=96))                                          # 41

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "SSG의 10월", "title": "SSG의 10월", "from": 5, "to": 8},
      {"key": "박종훈", "title": "박종훈 · 5년 65억", "from": 9, "to": 28},
      {"key": "나머지 7명", "title": "나머지 7명", "from": 29, "to": 35},
      {"key": "다른 구단", "title": "SSG의 겨울과 다른 구단", "from": 36, "to": 40}]

TAGS = ["SSG 방출", "박종훈 방출", "박종훈", "SSG 랜더스", "재계약 불가", "방출 명단", "비FA 다년계약", "잠수함 투수", "프로야구 방출", "2026 방출",
        "김성민", "김준영", "안현서", "이승훈", "한지헌", "박정빈", "석정우", "아빌라", "이숭용", "손아섭 방출", "프로야구", "KBO", "야구자판기"]
DESC = ("SSG 랜더스가 10월 10일 선수 8명에게 재계약 불가를 통보했어요. 명단에는 2018년과 2022년 두 번의 우승을 함께한 잠수함 투수 박종훈이 있어요.\n\n"
        "박종훈은 2021년 12월 국내 첫 비FA 다년계약(5년 65억 원)을 맺었지만, 2022년부터 2025년까지 1군 44경기 6승 17패 평균자책점 6.38에 그쳤고 계약 마지막 해인 올해는 1군에 오르지 못했어요. 통산 245경기 72승 79패 평균자책점 4.85.\n\n"
        "재계약 불가 8명: 투수 박종훈·김성민·김준영·안현서·이승훈·한지헌 / 내야수 석정우 / 외야수 박정빈\n\n"
        "10월 21일 기준 6개 구단(롯데 16명·두산 11명·삼성 10명·SSG 8명·키움 8명·한화 6명)이 모두 59명에게 재계약 불가를 알렸어요. NC·KT·LG·KIA 명단도 나오는 대로 구단별로 정리해 드릴게요.\n\n"
        "여러분은 박종훈이 다른 팀에서 다시 1군 마운드에 설 수 있다고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록: KBO 기록실(10월 21일 조회). 기사: 스포츠경향·파이낸셜뉴스(뉴시스)·일간스포츠·스포츠월드·MK스포츠·미디어펜·머니투데이·OSEN(10/10), 일간스포츠·MHN(10/12), 일간스포츠·경인일보(10/11~12), OSEN·이투데이(10/15), 스포츠경향·머니투데이(10/16), 아이뉴스24(2021/12/14), OSEN·노컷뉴스(2022/11/5), 스포티비뉴스(4/13)\n"
        "사진: OSEN, 연합뉴스, 스포츠동아, 스포츠서울, 구단 공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1021-롱폼23-SSG방출-근거모음.md (기사 본문 + KBO 기록실 10/21 직접 대조)."

EP = {"introChapter": "오프닝", "date": "2026-10-21", "gameDate": "2026-10-21", "series": "야구롱폼", "focusTeam": "SSG", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.3,
      "rev": "1021-long23-v1", "topic": "SSG방출", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼23_SSG방출.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "SSG 방출 8명 | 5년 65억 박종훈도 떠났다, 우승 두 번의 잠수함 #SSG #박종훈 #방출",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#SSG랜더스", "#박종훈", "#방출", "#재계약불가", "#비FA다년계약", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = set()   # 타입캐스트 웹 zip(한 배속)
    HOLD = {0: 0.35, 3: 0.35, 4: 0.35, 8: 0.35, 28: 0.4, 35: 0.35, 40: 0.35}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-21_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i + 1, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
