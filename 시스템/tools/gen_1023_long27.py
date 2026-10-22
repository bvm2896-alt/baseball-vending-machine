# -*- coding: utf-8 -*-
"""10/23 롱폼㉗ 「KT 방출 10명 — LG에 방출을 요청했던 최동환, 2년 만에 또」 (방출 시리즈 6편).
대사 = tools/text_1023_long27.py. 근거 = 프로젝트 claude/1023-롱폼27-KT방출-근거모음.md.
사진: 인물 카드 = 카드/P27_* (0.774) · 경기/ (SPOTV·KT 제공) · 얼굴판 = KBO프로필/<이름>_KT (나무위키 인포박스 = 구단 프로필).
김민성 포지션이 매체마다 달라(투수 4곳 · 포수 2곳) 얼굴판에 포지션을 쓰지 않는다."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1023_long27.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]
import narr_1020
def narr_of(t):
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)
    n = n.replace('KT', '케이티').replace('KIA', '기아').replace('LG', '엘지').replace('SK', '에스케이').replace('십일 월', '십일월').replace('십이 월', '십이월')
    n = n.replace('일여섯 시즌', '십육 시즌').replace('이천이십이시즌', '이천이십이 시즌').replace('이천이십삼시즌', '이천이십삼 시즌')
    return re.sub(r'(일|이|삼|사|오|육|칠|팔|구|십) 연패', r'\1연패', n)
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
C, K = '카드/P27_', 'KBO프로필/'
IMG = {None: None, "최LG": C + "최동환_LG우승", "최KT": C + "최동환_KT", "조": C + "조이현_KT", "조원": C + "조이현_KT원정"}
def pv(img, name, sub, viz=(), stats=(), **k): return S(0, "pstat", img=IMG.get(img, img), team=k.pop("team", "KT"), name=name, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, **k)
def sp(img, name, sub, bubbles, **k): return S(0, "speech", img=IMG.get(img, img), team=k.pop("team", "KT"), name=name, sub=sub, bubbles=bubbles, **k)
def prof(n): return K + n + "_KT"
NAMES = ["최동환", "조이현", "이현민", "이준명", "권효준", "김민성", "정정우", "김규한", "박치성", "최동희"]
def item(n, **x): return dict(name=n, team="KT", img=prof(n), **x)   # 10/23 사용자 "김민성 사진 찾아서 넣어" — 로고 칸 금지(나무위키 2024 프로필, 2005년생 우투 · 2024 3R 27순위)
def F10(text=None, textAt=0.3, hi=(), **k):
    return S(0, "facegrid", title="KT · 재계약 불가 10명", cols=5, card=True, chain="f10", profile=True,
             items=[item(n, **({"hi": True} if n in hi else {}), **({"dim": True} if hi and n not in hi else {}), **({"at": 0.2 + i * 0.05} if not k.get("cont") else {})) for i, n in enumerate(NAMES)],
             **({"text": text, "textAt": textAt, "size": 56} if text else {}), **k)
LK = K + "이강철"

SC = []
# ── 오프닝 ──
SC.append(F10(text="정규시즌 1위 팀", textAt=0.4))                                                                          # 0
SC.append(pv("최LG", "최동환", "LG 트윈스 · 2009 ~ 2024", [], [st("LG에서", "16년", 1.4, hi=True)], team="LG", chain="o1"))          # 1
SC.append(pv("최LG", "최동환", "LG 트윈스 · 2009 ~ 2024", [], [st("LG에서", "16년", 0), st("2024시즌 뒤", "직접 방출 요청", 1.2, hi=True)], team="LG", chain="o1", cont=True))   # 2
SC.append(pv("최KT", "최동환", "KT 위즈 · 2025 ~ 2026", [vsteps([stp("2024년 12월", "KT 입단", 0.3, c="good"), stp("2026년 10월", "재계약 불가", 1.6, c="bad")])]))   # 3
SC.append(S(0, "toc", on=-1, itemFrom=99))                                                                                   # 4
# ── 1막 · KT의 10월 ──
SC.append(S(0, "rankstrip", team="KT", title="2026 KT", rows=[dict(k="정규시즌", v="90승 5무 49패", rank=1, at=0)]))             # 5
SC.append(pv(None, "KT 위즈", "10월 5일 · 수원 롯데전", [], [st("롯데에", "9대 0 승", 0.3), st("정규시즌 우승", "5년 만", 1.6, hi=True)]))   # 6
SC.append(pv(None, "한국시리즈", "7전 4선승제", [vsteps([stp("정규시즌 1위", "한국시리즈 직행", 0.2, c="good"), stp("11월 2일", "1차전 · 수원", 1.6)])]))   # 7
SC.append(S(0, "tiles", title="KT의 한국시리즈 상대", items=[dict(team="삼성", k="정규시즌 2위", v="삼성", at=0.2), dict(team="KIA", k="준PO LG에 3연승", v="KIA", at=0.5)],
            text="플레이오프 승자", textAt=0.9, size=56))                                                                        # 8
SC.append(pv(LK, "이강철", "KT 감독", [], [st("10월 19일", "재계약", 0.3), st("조건", "3년 총액 34억 원", 1.4, hi=True)], chain="l9", profile=True))   # 9
SC.append(pv(LK, "이강철", "KT 감독", [], [st("10월 19일", "재계약", 0), st("조건", "3년 총액 34억 원", 0), st("KBO 감독", "역대 최고 대우", 0.3, hi=True)], chain="l9", cont=True, profile=True))   # 10
SC.append(F10(text="사흘 뒤 · 10월 22일", textAt=0.6, cont=True))                                                               # 11
SC.append(F10(text="같은 날 문상철 은퇴 · 모두 11명", textAt=1.6, cont=True))                                                     # 12
# ── 2막 · 최동환 ──
SC.append(S(0, "photo", img="경기/최동환_LG우승_SPOTV", fit="cover", text="", h=760))                                           # 13
SC.append(pv("최LG", "최동환", "LG 트윈스 · 경동고", [vsteps([stp("2009년", "2차 2라운드 · 전체 13순위", 1.0, c="good")])], team="LG"))   # 14
SC.append(pv("최LG", "최동환", "LG 트윈스", [], [st("LG 한 팀에서", "16년", 0.4, hi=True)], team="LG"))                             # 15
SC.append(pv("최LG", "최동환", "2023년 LG", [], [st("경기", "45경기", 0.4), st("평균자책점", "3.19", 1.2, hi=True)], team="LG", chain="c16"))   # 16
SC.append(pv("최LG", "최동환", "2023년 LG", [vstamp("데뷔 첫 한국시리즈 등판", 2.6, "gold", size=48)], [st("경기", "45경기", 0), st("평균자책점", "3.19", 0), st("LG", "29년 만에 통합우승", 0.6)], team="LG", chain="c16", cont=True))   # 17
SC.append(pv("최LG", "최동환", "2024년 LG", [], [st("1군", "26경기", 0.4), st("평균자책점", "6.95", 1.0, hi=True)], team="LG", chain="c18"))   # 18
SC.append(pv("최LG", "최동환", "2024년 LG", [], [st("1군", "26경기", 0), st("평균자책점", "6.95", 0, hi=True), st("2군 평균자책점", "1.08", 0.4, hi=True)], team="LG", chain="c18", cont=True))   # 19
SC.append(pv("최LG", "최동환", "2024시즌 뒤", [vsteps([stp("시즌 뒤", "구단에 직접 방출 요청", 1.2, c="bad")])], team="LG", chain="c20"))   # 20
SC.append(pv("최LG", "최동환", "2024시즌 뒤", [vsteps([stp("시즌 뒤", "구단에 직접 방출 요청", -1, c="bad"), stp("10월 초", "LG 방출", 0.1, c="bad"), stp("12월 2일", "KT 입단 · 불펜 보강", 0.4, c="good")])], team="LG", chain="c20", cont=True))   # 21
SC.append(pv("최KT", "최동환", "2025년 KT", [], [st("1군", "20경기", 0.6), st("평균자책점", "8.68", 1.4, hi=True)]))                # 22
SC.append(pv("최KT", "최동환", "2026년 KT", [], [st("1군", "0경기", 0.4, hi=True), st("2군", "36경기", 1.4), st("2군 평균자책점", "6.11", 2.2)]))   # 23
SC.append(pv("최KT", "최동환", "1군 통산 · KBO 기록", [], [st("경기", "364경기", 0.1), st("승패", "11승 7패", 0.6), st("세이브 · 홀드", "4세이브 16홀드", 1.3), st("평균자책점", "5.28", 2.2, hi=True)]))   # 24
SC.append(pv(None, "LG 트윈스", "10월 22일 · 같은 날", [], [st("재계약 불가", "11명", 1.2, hi=True), st("은퇴 포함", "장시환 · 송대현", 2.4)], team="LG"))   # 25
# ── 3막 · 조이현 · 나머지 ──
SC.append(S(0, "photo", img="경기/조이현_KT원정_SPOTV", fit="cover", text="", h=760))                                           # 26
SC.append(pv("조", "조이현", "제주고", [vsteps([stp("2014년", "한화 · 2차 5라운드 · 전체 47순위", 1.0)])], chain="j27"))              # 27
SC.append(pv("조", "조이현", "제주고", [vsteps([stp("2014년", "한화 · 2차 5라운드 · 전체 47순위", -1), stp("2015년 말", "정우람 FA 보상선수 · SK", 0.6)])], chain="j27", cont=True))   # 28
SC.append(pv("조", "조이현", "제주고", [vsteps([stp("2014년", "한화 · 2차 5라운드 · 전체 47순위", -1), stp("2015년 말", "정우람 FA 보상선수 · SK", -1),
                                          stp("2022시즌 뒤", "SSG에서 방출", 2.2, c="bad")])], chain="j27", cont=True))         # 29
SC.append(pv("조", "조이현", "제주고", [vsteps([stp("2014년", "한화 · 2차 5라운드 · 전체 47순위", -1), stp("2015년 말", "정우람 FA 보상선수 · SK", -1),
                                          stp("2022시즌 뒤", "SSG에서 방출", -1, c="bad"), stp("2023시즌", "KT 입단 · 테스트 통과", 0.6, c="good")])], chain="j27", cont=True))   # 30
SC.append(pv("조원", "조이현", "2025년 2군 남부리그", [], [st("승리", "10승 · 1위", 1.0), st("평균자책점", "3.60 · 1위", 1.6), st("타이틀", "2관왕", 2.2, hi=True)]))   # 31
SC.append(pv("조원", "조이현", "2026년", [], [st("1군", "0경기", 0.6, hi=True), st("2군", "24경기", 1.4), st("2군 평균자책점", "5.67", 2.2)]))   # 32
SC.append(pv("조", "조이현", "1군 통산 · KBO 기록", [], [st("경기", "116경기", 0.1), st("승패", "10승 18패", 0.6), st("평균자책점", "6.29", 1.3, hi=True)]))   # 33
SC.append(pv("조", "조이현", "거친 팀", [vsteps([stp("한화", "2014년 입단", 0.2), stp("SK · SSG", "2022시즌 뒤 방출", 0.8, c="bad"), stp("KT", "2026년 재계약 불가", 1.6, c="bad")])]))   # 34
SC.append(pv(None, "KT 위즈", "나머지 8명", [], [st("1군 기록", "대부분 없음", 0.6, hi=True)]))                                   # 35
REST = [n for n in NAMES if n not in ("최동환", "조이현")]
SC.append(S(0, "facegrid", title="나머지 8명", cols=4, card=True, profile=True, items=[item(n, at=0.05 + i * 0.12) for i, n in enumerate(REST)]))   # 36
# ── 4막 · KT의 겨울과 다른 구단 ──
SC.append(pv(None, "KT 위즈", "이번 겨울", [vstamp("한국시리즈 기다리는 중", 0.3, "good", size=52)]))   # 10/23 사용자 "이 장면도 너무 금방 지나가" — 2.4초 줄에 일정 두 줄은 못 읽음 → 한 마디 도장으로   # 37
SC.append(sp(LK, "이강철", "KT 감독 · 10월 19일 재계약", [bb("10월 19일", "아직 시즌이 끝나지 않았다", 0.8, src=True), bb("다짐 · 요약", "더 높은 곳에서 마무리하도록 노력", 2.0, src=True)], profile=True))   # 38
SC.append(S(0, "rankstrip", team="KT", title="KT 위즈", rows=[dict(k="2021년", v="통합우승", rank=1, at=0.6), dict(k="2026년", v="정규시즌 1위", rank=1, at=2.2)]))   # 39
SC.append(S(0, "tiles", title="10월 22일 하루", items=[dict(team="KT", k="재계약 불가", v="10명", at=0.6), dict(team="LG", k="재계약 불가 · 은퇴 포함", v="11명", at=0.9)], text="모두 21명", textAt=1.8, size=64))   # 40
_RL = [dict(label="롯데", team="롯데", value=16, unit="명", at=0.6), dict(label="두산", team="두산", value=11, unit="명", at=0.6), dict(label="LG", team="LG", value=11, unit="명", at=0.6),
       dict(label="삼성", team="삼성", value=10, unit="명", at=0.6), dict(label="KT", team="KT", value=10, unit="명", at=0.6, hi=True), dict(label="SSG", team="SSG", value=8, unit="명", at=0.6),
       dict(label="키움", team="키움", value=8, unit="명", at=0.6), dict(label="한화", team="한화", value=6, unit="명", at=0.6)]
SC.append(S(0, "bars", title="재계약 불가 · 10월 22일 기준", items=_RL, max=16, chain="b41", text="8개 구단 발표 인원 합계 · 80명", textAt=1.6, size=56))   # 41
SC.append(S(0, "bars", title="재계약 불가 · 10월 22일 기준", items=_RL, max=16, chain="b41", cont=True))                          # 42
SC.append(S(0, "tiles", title="아직 발표 소식 없음", items=[dict(team=t, k="10월 22일 기준", v="발표 소식 없음", at=0.1 + i * 0.3) for i, t in enumerate(["NC", "KIA"])]))   # 43
SC.append(S(0, "question", text="최동환\n다른 팀에서 다시?", img=IMG["최KT"], size=96))                                       # 44

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "KT의 10월", "title": "KT의 10월", "from": 5, "to": 12},
      {"key": "최동환", "title": "최동환 · 스스로 나온 LG, 2년 만의 방출", "from": 13, "to": 25},
      {"key": "조이현", "title": "조이현 · 나머지 8명", "from": 26, "to": 36},
      {"key": "다른 구단", "title": "KT의 겨울과 다른 구단", "from": 37, "to": 44}]

TAGS = ["KT 방출", "최동환 방출", "최동환", "조이현", "KT 위즈", "재계약 불가", "방출 명단", "이강철 재계약", "문상철 은퇴", "LG 방출", "장시환 은퇴",
        "프로야구 방출", "2026 방출", "한국시리즈", "프로야구", "KBO", "야구자판기"]
DESC = ("정규시즌 1위(90승 5무 49패) KT 위즈가 10월 22일 선수 10명과 재계약하지 않기로 했어요. 같은 날 창단 특별지명 출신 문상철도 은퇴를 발표해 KT를 떠나는 선수는 모두 11명이에요.\n\n"
        "명단에는 LG에서 16년을 보낸 최동환이 있어요. 2023년 45경기 평균자책점 3.19로 LG의 29년 만의 통합우승에 힘을 보태고 데뷔 첫 한국시리즈 마운드에 섰지만, 2024시즌을 마친 뒤 현역을 이어 가려고 LG에 직접 방출을 요청했어요. "
        "12월 KT에 입단했지만 2025년 1군 20경기 평균자책점 8.68, 올해는 1군 등판이 없었어요. 1군 통산 364경기 11승 7패 4세이브 16홀드 평균자책점 5.28.\n\n"
        "한화·SK·SSG를 거쳐 입단 테스트로 KT에 온 조이현은 지난해 2군 남부리그 다승·평균자책점 2관왕이었지만, 올해 1군 등판 없이 두 번째 방출 통보를 받았어요.\n\n"
        "재계약 불가 10명: 최동환·조이현·이현민·이준명·권효준·김민성·정정우·김규한·박치성·최동희\n\n"
        "KT는 10월 19일 이강철 감독과 3년 총액 34억 원(KBO 감독 역대 최고 대우)에 재계약했고, 11월 2일 수원에서 한국시리즈 1차전을 치러요.\n\n"
        "같은 날 LG도 11명과 재계약하지 않기로 했어요. 10월 22일 기준 8개 구단(롯데 16·두산 11·LG 11·삼성 10·KT 10·SSG 8·키움 8·한화 6)의 발표 인원을 모두 더하면 80명이에요(LG는 은퇴 2명 포함).\n\n"
        "여러분은 최동환이 다른 팀에서 다시 기회를 받을 수 있다고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록: KBO 기록실(10월 22일 조회). 기사: 뉴시스·일간스포츠·SPOTV·스타뉴스·재경일보(10/22), SPOTV(2024/10/7), OSEN(2024/12/2·2025/5/21), 마이데일리(2025/1/10·2026/10/19), 세계일보(10/19), "
        "뉴스서울(2025/9/28), 미디어펜·아주경제(10/5), 이투데이(10/13), 톱스타뉴스(10/12), 이코노믹리뷰·신아일보(10/22)\n"
        "사진: SPOTV, KT 위즈 제공, 구단 공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1023-롱폼27-KT방출-근거모음.md (기사 본문 2곳 이상 + KBO 기록실)."

EP = {"introChapter": "오프닝", "date": "2026-10-23", "gameDate": "2026-10-23", "series": "야구롱폼", "focusTeam": "KT", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.3,
      "rev": "1023-long27-v2", "topic": "KT방출", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼27_KT방출.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "KT 방출 10명 | LG에 방출 요청했던 최동환, 2년 만에 또 방출 #KT #최동환 #방출",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#KT위즈", "#최동환", "#조이현", "#방출", "#재계약불가", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {0: 0.35, 3: 0.35, 4: 0.35, 12: 0.35, 25: 0.4, 36: 0.35, 43: 0.35}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-23_롱폼2.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i + 1, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
