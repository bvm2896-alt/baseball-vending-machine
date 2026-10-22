# -*- coding: utf-8 -*-
"""10/22 롱폼㉕ 「삼성 방출 10명 — 13연패 끊은 1라운더 허윤동도 떠났다」 (방출 시리즈 4편).
대사 = tools/text_1022_long25.py. 근거 = 프로젝트 claude/1022-롱폼25-삼성방출-근거모음.md.
사진: 인물 카드 = 카드/P25_* (0.774) · 10명 얼굴판 = KBO프로필/<이름>_삼성 (나무위키 인포박스 = 구단 프로필)."""
import json, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1022_long25.py'")
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
C, K = '카드/P25_', 'KBO프로필/'
IMG = {None: None, "허투": C + "허윤동_투구", "허역": C + "허윤동_역투", "양투": C + "양현_투구", "양삼": C + "양현_삼성", "홍삼": C + "홍현빈_삼성", "홍KT": C + "홍현빈_KT끝내기"}
def pv(img, name, sub, viz=(), stats=(), **k): return S(0, "pstat", img=IMG.get(img, img), team=k.pop("team", "삼성"), name=name, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, **k)
def sp(img, name, sub, bubbles, **k): return S(0, "speech", img=IMG.get(img, img), team=k.pop("team", "삼성"), name=name, sub=sub, bubbles=bubbles, **k)
POS = [("양현", "투수"), ("홍원표", "투수"), ("허윤동", "투수"), ("박주혁", "투수"), ("김동현", "투수"), ("신윤호", "투수"), ("박시원", "투수"), ("유병선", "투수"), ("박장민", "내야수"), ("홍현빈", "외야수")]
def prof(n): return K + n + "_삼성"
def F10(text=None, textAt=0.3, **k):
    return S(0, "facegrid", title="삼성 · 재계약 불가 10명", cols=5, card=True, chain="f10", profile=True,
             items=[dict(name=n, img=prof(n), team="삼성", pos=p, **({"at": 0.2 + i * 0.05} if not k.get("cont") else {})) for i, (n, p) in enumerate(POS)],
             **({"text": text, "textAt": textAt, "size": 56} if text else {}), **k)
D3 = [("허윤동", "1라운드"), ("홍원표", "3라운드"), ("박주혁", "5라운드")]
def FD(text=None, textAt=0.3, **k):
    return S(0, "facegrid", title="2020년 삼성 드래프트 동기", cols=3, card=True, chain="fd", profile=True,
             items=[dict(name=n, img=prof(n), team="삼성", pos=p, **({"at": 0.3 + i * 0.5} if not k.get("cont") else {})) for i, (n, p) in enumerate(D3)],
             **({"text": text, "textAt": textAt, "size": 56} if text else {}), **k)
R5 = [("김동현", "투수"), ("신윤호", "투수"), ("박시원", "투수"), ("유병선", "투수"), ("박장민", "내야수")]

SC = []
# ── 오프닝 ──
SC.append(F10())                                                                                                             # 0
SC.append(F10(text="10월 19일 · 플레이오프 엿새 전", textAt=0.6, cont=True))                                                   # 1
SC.append(pv("허투", "허윤동", "삼성 왼손 투수", [], [st("2020년 드래프트", "1라운드 · 전체 5순위", 1.2, hi=True)], chain="o2"))     # 2
SC.append(pv("허투", "허윤동", "삼성 왼손 투수", [], [st("2020년 드래프트", "1라운드 · 전체 5순위", 0), st("2022년 7월", "팀 13연패 끊음", 0.6, hi=True), st("구단 역사상", "최장 연패", 1.8)], chain="o2", cont=True))   # 3
SC.append(S(0, "toc", on=-1, itemFrom=99))                                                                                   # 4
# ── 1막 · 삼성의 10월 ──
SC.append(S(0, "rankstrip", team="삼성", title="2026 삼성", rows=[dict(k="정규시즌", v="83승 3무 58패", rank=2, at=0)]))           # 5
SC.append(pv(None, "삼성 라이온즈", "2026 정규시즌", [], [st("1위 KT와", "8경기 차", 0.3), st("플레이오프", "직행", 1.4, hi=True)]))   # 6
SC.append(S(0, "tiles", title="2026 플레이오프", chain="t7", items=[dict(team="삼성", k="정규시즌 2위", v="삼성", at=0.1), dict(team="KIA", k="준PO LG에 3연승", v="KIA", at=1.0)]))   # 7
SC.append(S(0, "tiles", title="2026 플레이오프", chain="t7", cont=True, items=[dict(team="삼성", k="정규시즌 2위", v="삼성", at=0), dict(team="KIA", k="23년 만에 PO", v="KIA", at=0.2, hi=True)]))   # 8
SC.append(pv(None, "플레이오프", "5전 3선승제", [vsteps([stp("10월 25일", "1차전 · 대구", 0.3, c="good")])]))                        # 9
SC.append(F10(text="투수 8명 · 내야수 1명 · 외야수 1명", textAt=0.8, cont=True))                                                  # 10
SC.append(sp(None, "삼성 라이온즈", "10월 19일 구단 설명", [bb("이유", "선수단 체질 개선 · 유망주 육성", 0.4, src=True)]))              # 11
# ── 2막 · 허윤동 ──
SC.append(pv("허역", "허윤동", "삼성 왼손 투수", [], [st("투구", "왼손 투수", 0.6, hi=True)]))                                      # 12
SC.append(pv("허투", "허윤동", "삼성 라이온즈 · 유신고", [vsteps([stp("2020년", "2차 1라운드 · 전체 5순위", 0.8, c="good")])]))         # 13
SC.append(pv("허투", "허윤동", "2020년 데뷔 시즌", [], [st("1군", "11경기", 0.2), st("승패", "2승 1패", 0.7), st("평균자책점", "4.80", 1.4, hi=True)]))   # 14
SC.append(pv("허역", "허윤동", "2022년 7월 24일 · 고척 키움전", [], [st("그날 삼성", "13연패 중", 0.8, hi=True)], chain="g15"))         # 15
SC.append(pv("허역", "허윤동", "2022년 7월 24일 · 고척 키움전", [], [st("선발", "6이닝", 0.2), st("피안타", "2개", 0.9), st("삼진", "7개", 1.8), st("실점", "0점", 2.8, hi=True)], chain="g15", cont=True))   # 16
SC.append(pv("허역", "허윤동", "2022년 7월 24일 · 고척 키움전", [vstamp("13연패 탈출", 0.8, "good", size=52)], [st("선발", "6이닝", 0), st("피안타", "2개", 0), st("삼진", "7개", 0), st("실점", "0점", 0), st("결과", "8대 0 승", 0.2)], chain="g15", cont=True))   # 17
SC.append(pv("허투", "허윤동", "2022년 시즌", [], [st("1군", "12경기", 0.3), st("승패", "4승 3패", 1.0, hi=True)]))                  # 18
SC.append(pv("허투", "허윤동", "그 뒤", [vsteps([stp("2022년", "1군 12경기", 0.3)])], chain="h19"))                                    # 19
SC.append(pv("허투", "허윤동", "그 뒤", [vsteps([stp("2022년", "1군 12경기", -1), stp("2023년", "1군 7경기 · 마지막 1군", 0.3, c="bad")])], chain="h19", cont=True))   # 20
SC.append(pv("허투", "허윤동", "그 뒤", [vsteps([stp("2022년", "1군 12경기", -1), stp("2023년", "1군 7경기 · 마지막 1군", -1, c="bad"), stp("2024년", "상무 입대", 0.2),
                                               stp("2025년", "복귀", 0.9), stp("2026년", "1군 0경기", 1.8, c="bad")])], chain="h19", cont=True))   # 21
SC.append(pv("허투", "허윤동", "2026년 2군", [], [st("2군", "33경기", 0.2), st("승패", "6승 1패 3홀드", 0.8), st("평균자책점", "5.05", 1.6, hi=True)]))   # 22
SC.append(pv("허투", "허윤동", "1군 통산 · KBO 기록", [], [st("경기", "31경기", 0.1), st("승패", "6승 6패", 0.6), st("평균자책점", "6.38", 1.4, hi=True)]))   # 23
SC.append(FD())                                                                                                                # 24
SC.append(FD(text="동기 3명이 한꺼번에", textAt=2.0, cont=True))                                                                 # 25
SC.append(pv("허투", "허윤동", "제 생각", [], [st("나이", "25살 왼손", 1.0), st("최근 3년", "1군 기록 없음", 3.0), st("바로 1군 자리", "쉽지 않음", 5.0, hi=True)]))   # 26
# ── 3막 · 양현 · 홍현빈 · 나머지 ──
SC.append(pv("양투", "양현", "삼성 투수", [], [st("투구", "잠수함 · 언더핸드", 0.4, hi=True)]))                                      # 27
SC.append(pv("양삼", "양현", "삼성 투수 · 대전고", [vsteps([stp("2011년", "두산 입단", 0.3), stp("이적", "2차 드래프트로만 두 번", 1.2, c="good")])], chain="y28"))   # 28
SC.append(pv("양삼", "양현", "삼성 투수 · 대전고", [vsteps([stp("2011년", "두산 입단", -1), stp("2015년", "2차 드래프트 · 넥센", 0.2), stp("2023년", "2차 드래프트 · 삼성", 1.4, c="good")])], chain="y28", cont=True))   # 29
SC.append(pv("양삼", "양현", "1군 통산 · KBO 기록", [], [st("경기", "284경기", 0.2), st("승패", "14승 15패 4세이브", 0.8), st("평균자책점", "4.22", 1.6, hi=True)]))   # 30
SC.append(pv("양투", "양현", "2026년", [], [st("1군", "2경기", 0.3), st("평균자책점", "27.00", 1.0, hi=True)]))                       # 31
SC.append(pv("홍삼", "홍현빈", "삼성 외야수", [vsteps([stp("2017년", "KT 입단", 0.6)])]))                                            # 32
SC.append(pv("홍KT", "홍현빈", "2024년 6월 28일 · KT", [], [st("상대", "삼성 마무리 오승환", 1.0), st("초구", "끝내기 역전 3루타", 2.6, hi=True)], team="KT"))   # 33
SC.append(pv("홍삼", "홍현빈", "삼성 외야수", [vsteps([stp("2024년 10월", "KT 방출", 0.3, c="bad"), stp("시즌 뒤", "삼성 입단", 1.4, c="good")])]))   # 34
SC.append(pv("홍삼", "홍현빈", "1군 통산 · KBO 기록", [], [st("경기", "281경기", 0.2), st("타율", "1할 9푼 2리", 0.8), st("삼성에서", "2년 만에 방출", 2.4, hi=True)]))   # 35
SC.append(S(0, "facegrid", title="나머지 5명", cols=5, card=True, profile=True, items=[dict(name=n, img=prof(n), team="삼성", pos=p, at=0.1 + i * 0.3) for i, (n, p) in enumerate(R5)],
             text="1군 기록 없이 떠나요", textAt=3.0, size=56))                                                                  # 36
# ── 4막 · 삼성의 겨울과 다른 구단 ──
SC.append(pv(None, "삼성 라이온즈", "이번 겨울", [vsteps([stp("10월 25일부터", "플레이오프", 0.2), stp("그 뒤", "겨울 본격 시작", 0.8, c="good")])]))   # 37
SC.append(pv("KBO프로필/박진만_감독", "박진만", "삼성 감독", [], [st("2025년 11월", "재계약", 0.3), st("조건", "최대 23억 원", 1.0), st("2026년", "새 계약 첫해", 2.0, hi=True)], profile=True))   # 38
SC.append(pv("KBO프로필/구자욱", "구자욱", "삼성 외야수", [], [st("비FA 다년계약", "5년 120억 원", 0.4), st("올해로", "계약 끝", 1.2), st("생애 첫", "FA", 2.0, hi=True)], profile=True))   # 39
SC.append(pv("KBO프로필/원태인", "원태인", "삼성 투수", [], [st("이번 시즌 뒤", "FA", 0.4, hi=True)], chain="w40", profile=True))         # 40
SC.append(pv("KBO프로필/원태인", "원태인", "삼성 투수", [], [st("이번 시즌 뒤", "FA", 0, hi=True), st("2026년 연봉", "10억 원", 0.2), st("2026년 성적", "7승 9패 · 4.52", 1.0)], chain="w40", cont=True, profile=True))   # 41
_RL = [dict(label="롯데", team="롯데", value=16, unit="명", at=0.6), dict(label="두산", team="두산", value=11, unit="명", at=0.6), dict(label="삼성", team="삼성", value=10, unit="명", at=0.6, hi=True),
       dict(label="SSG", team="SSG", value=8, unit="명", at=0.6), dict(label="키움", team="키움", value=8, unit="명", at=0.6), dict(label="한화", team="한화", value=6, unit="명", at=0.6)]
SC.append(S(0, "bars", title="재계약 불가 · 10월 20일 기준", items=_RL, max=16, chain="b42", text="6개 구단 · 모두 59명", textAt=1.8, size=56))   # 42
SC.append(S(0, "bars", title="재계약 불가 · 10월 20일 기준", items=_RL, max=16, chain="b42", cont=True, text="두산 11명엔 손아섭도", textAt=1.6, size=56))   # 43
SC.append(S(0, "tiles", title="아직 명단 발표 전", items=[dict(team=t, k="10월 22일", v="발표 전", at=0.1 + i * 0.25) for i, t in enumerate(["NC", "KT", "LG", "KIA"])]))   # 44
SC.append(S(0, "question", text="허윤동\n다시 1군 마운드에?", img=IMG["허투"], size=96))                                       # 45

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "삼성의 10월", "title": "삼성의 10월", "from": 5, "to": 11},
      {"key": "허윤동", "title": "허윤동 · 13연패를 끊은 1라운더", "from": 12, "to": 26},
      {"key": "양현 · 홍현빈", "title": "양현 · 홍현빈 · 나머지 5명", "from": 27, "to": 36},
      {"key": "다른 구단", "title": "삼성의 겨울과 다른 구단", "from": 37, "to": 44}]

TAGS = ["삼성 방출", "허윤동 방출", "허윤동", "삼성 라이온즈", "재계약 불가", "방출 명단", "양현", "홍현빈", "홍원표", "박주혁", "구자욱 FA", "원태인 FA", "삼성 기아 플레이오프",
        "프로야구 방출", "2026 방출", "손아섭 방출", "프로야구", "KBO", "야구자판기"]
DESC = ("삼성 라이온즈가 플레이오프를 엿새 앞둔 10월 19일 선수 10명에게 재계약 불가를 통보했어요.\n\n"
        "명단에는 2020년 2차 1라운드 전체 5순위 왼손 투수 허윤동이 있어요. 허윤동은 2022년 7월 24일 고척 키움전에서 6이닝 무실점으로 구단 최다 13연패를 끊었지만, 2023년을 끝으로 1군 기록이 없어요. 1군 통산 31경기 6승 6패 평균자책점 6.38.\n"
        "같은 해 입단한 홍원표(3라운드)·박주혁(5라운드)도 함께 떠나요. 2차 드래프트로만 두 번 팀을 옮긴 잠수함 양현(통산 284경기), KT 시절 오승환에게 끝내기 3루타를 친 홍현빈도 명단에 있어요.\n\n"
        "재계약 불가 10명: 투수 양현·홍원표·허윤동·박주혁·김동현·신윤호·박시원·유병선 / 내야수 박장민 / 외야수 홍현빈\n\n"
        "삼성은 83승 3무 58패로 정규시즌 2위, 10월 25일 대구에서 KIA와 플레이오프 1차전을 치러요. 시즌 뒤엔 구자욱과 원태인이 FA 자격을 얻어요.\n\n"
        "10월 20일 기준 6개 구단(롯데 16명·두산 11명·삼성 10명·SSG 8명·키움 8명·한화 6명)이 모두 59명에게 재계약 불가를 알렸어요.\n\n"
        "여러분은 허윤동이 다른 팀에서 다시 1군 마운드에 설 수 있다고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록: KBO 기록실(10월 22일 조회). 기사: 뉴스핌·스타뉴스·SBS·스포츠경향·이데일리·재경일보·SPOTV·OSEN·이투데이(10/19), 노컷뉴스(2022/7/25), 강원일보·SPOTV(2015/11/27), 매일신문(2023/11/22), OSEN(2024/6/28), 시대일보(2024/10/10), 뉴스핌·서울신문·위키트리(10/21), 일간스포츠(10/13), 경북매일·SBS(2025/11/3), 세계일보(9/7)·영남일보(1/26)·대구신문(10/7)\n"
        "사진: OSEN, SPOTV, 구단 공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1022-롱폼25-삼성방출-근거모음.md (기사 본문 2곳 이상 + KBO 기록실)."

EP = {"introChapter": "오프닝", "date": "2026-10-22", "gameDate": "2026-10-22", "series": "야구롱폼", "focusTeam": "삼성", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.3,
      "rev": "1022-long25-v2", "topic": "삼성방출", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼25_삼성방출.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "삼성 방출 10명 | 13연패 끊은 1라운더 허윤동도 떠났다 #삼성 #허윤동 #방출",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#삼성라이온즈", "#허윤동", "#방출", "#재계약불가", "#양현", "#홍현빈", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {1: 0.35, 3: 0.35, 4: 0.35, 11: 0.35, 26: 0.4, 36: 0.35, 44: 0.35}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-22_롱폼2.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i + 1, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
