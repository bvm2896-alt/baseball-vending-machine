# -*- coding: utf-8 -*-
"""10/20 롱폼㉑ 「두산 방출 11명 — 2655안타 손아섭도 떠났다」 (방출 시리즈 1편 · 음성 API · 줄별 배속).
대사 = tools/text_1020_long21.py (v1.2, KBO 기록실 대조 확정). 나레이션 앞·뒤처리 = tools/narr_1020.py.
근거 = 프로젝트 claude/1020-롱폼21-두산방출-근거모음.md.
사진: 인물 카드 = 카드/P21_*(경기·두산 제공 사진, 0.774) · 9명 얼굴판 = KBO프로필/<이름>_2026두산(나무위키 인포박스 = 구단 프로필, 전원 같은 종류)."""
import json, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1020_long21.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]
import narr_1020
def narr_of(t):
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)          # 사 월 → 사월
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)   # 10/18 '이 회'가 지시어로 들림
    return n
def sub_of(t): return re.sub(r'\.(?= / )', '', t)

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
RED, GOLD, GRAY, NAVY = "#E5484D", "#E8A100", "#8A93A3", "#3B4A63"
C, K = '카드/P21_', 'KBO프로필/'
IMG = {None: None, "손아섭A": C + "손아섭_홈런", "손아섭B": C + "손아섭_스윙", "손아섭C": C + "손아섭_질주", "손아섭D": C + "손아섭_인사", "손아섭P": K + "손아섭_2026두산",
       "김명신A": C + "김명신_역투", "김명신B": C + "김명신_2017복귀", "김명신P": K + "김명신_2026두산",
       "정재훈": C + "정재훈_단장", "김태룡": C + "김태룡", "김원형": C + "김원형_박수"}
def pv(img, name, sub, viz=(), stats=(), **k): return S(0, "pstat", img=IMG[img], team=k.pop("team", "두산"), name=name, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, **k)
def sp(img, name, sub, bubbles, **k): return S(0, "speech", img=IMG[img], team=k.pop("team", "두산"), name=name, sub=sub, bubbles=bubbles, **k)
def steps(title, items, **k): return S(0, "steps", title=title, items=[dict(date=d, text=t, at=a, **({"hi": True} if h else {})) for d, t, a, h in items], **k)

# 11명 얼굴판(포지션별) — 1·13줄
POS = [("김명신", "투수"), ("박강민", "투수"), ("김지윤", "투수"), ("장우진", "투수"), ("이기석", "투수"), ("백승우", "투수"),
       ("김민혁", "내야수"), ("지강혁", "내야수"), ("이종혁", "내야수"), ("손아섭", "외야수"), ("양현진", "외야수")]
def prof(n): return {"백승우": K + "백승우_두산", "이종혁": None}.get(n, K + n + "_2026두산")
def F11(**k): return S(0, "facegrid", title="두산 · 재계약 불가 11명", cols=6, card=True, chain="f11", profile=True,
                       items=[dict(name=n, img=prof(n), team="두산", pos=p, **({"at": 0.2 + i * 0.05} if not k.get("cont") else {})) for i, (n, p) in enumerate(POS)], **k)
# 나머지 9명 — 43~51줄
NINE = [("박강민", "투수"), ("김지윤", "투수"), ("장우진", "투수"), ("이기석", "투수"), ("백승우", "투수"), ("김민혁", "내야수"), ("지강혁", "내야수"), ("이종혁", "내야수"), ("양현진", "외야수")]
def F9(hi=(), text=None, textAt=0.2, **k):
    return S(0, "facegrid", title="나머지 9명", cols=5, card=True, chain="f9", profile=True, cont=bool(hi or text),
             items=[dict(name=n, img=prof(n), team="두산", pos=p, **({"hi": True} if n in hi else {}), **({"dim": True} if hi and n not in hi else {})) for n, p in NINE],
             **({"text": text, "textAt": textAt, "size": 56} if text else {}), **k)

SC = []
# ── 오프닝 ──
SC.append(F11())                                                                                                             # L1
SC.append(pv("손아섭A", "손아섭", "두산 외야수", [], [st("통산 안타", "2655개", 0.6, hi=True)]))                                   # L2
SC.append(pv("손아섭D", "손아섭", "두산에서 6개월", [vsteps([stp("4월 14일", "한화에서 트레이드", 0.1), stp("10월 19일", "재계약 불가", 0.8, c="bad")])]))   # L3
SC.append(pv("김태룡", "김태룡", "두산 단장 · 2011~2026", [], [st("단장", "16년", 0.6, hi=True)]))                                       # L4
SC.append(S(0, "toc", on=-1, itemFrom=99))                                                                                    # L5
# ── 1막 · 10월 19일, 두산이 바꾼 것 ──
SC.append(S(0, "rankstrip", team="두산", title="2026 두산", rows=[dict(k="정규시즌", v="73승 5무 66패", rank=5, at=0)]))          # L6
SC.append(S(0, "matchup", left="LG", right="두산", score="4 : 1", tag="와일드카드 결정전 · 10월 14일 잠실", text="한 경기 만에 탈락", size=84))   # L7
SC.append(sp("김원형", "김원형", "두산 감독 · 10월 14일", [bb("", "“감독 입장에서\n창피한 경기였다”", 0.4)]))                         # L8
SC.append(pv("정재훈", "정재훈", "10월 19일 · 새 단장", [vsteps([stp("김태룡 단장", "구단 자문으로", 1.0), stp("정재훈 운영팀장", "새 단장", 2.0, c="good")])]))   # L9
SC.append(S(0, "tiles", title="김태룡 단장 · 2011~2026", items=[dict(team="두산", k="단장", v="16년\nKBO 최장수", at=1.2), dict(team="두산", k="한국시리즈", v="7년 연속", at=3.2),
                                                             dict(team="두산", k="우승", v="3번", at=4.2)]))                         # L10
SC.append(pv("정재훈", "정재훈", "두산 새 단장", [vstamp("마무리 투수 정재훈과 다른 사람", 3.2, "bad", size=44)],
             [st("나이", "45살", 0), st("2006년", "두산 선수 입단", 1), st("2011년부터", "프런트", 2)]))                               # L11
SC.append(sp(None, "두산 베어스", "10월 19일 구단 발표", [bb("", "“구단 시스템 전반을\n혁신하겠다는 의지”", 0.8)]))                     # L12
SC.append(F11(cont=True))                                           # L13
# ── 2막 · 손아섭 ──
SC.append(S(0, "photo", img="경기/손아섭_홈런_0414_두산제공", fit="cover", text="", h=760))                                     # L14
SC.append(pv("손아섭B", "손아섭", "외야수 · 부산고", [vsteps([stp("2007년", "롯데 입단", 0.1), stp("2010년", "주전 외야수", 1.0, c="good")])]))   # L15
SC.append(pv("손아섭C", "손아섭", "롯데 · NC 시절", [], [st("최다안타 1위", "4번", 0.1), st("골든글러브", "6번", 1.0), st("2023년 NC", "첫 타격왕", 2.4, hi=True)]))   # L16
SC.append(pv("손아섭A", "손아섭", "2024년 6월 20일 · 잠실 두산전", [vstamp("통산 최다 안타 1위", 2.0, "gold", size=52)], [st("넘은 기록", "박용택 2504안타", 1.0)]))   # L17
SC.append(S(0, "bars", title="손아섭 · 시즌 안타", items=[dict(label="2021년", value=173, unit="개", at=0), dict(label="2022년", value=152, unit="개", at=0),
                                                       dict(label="2023년", value=187, unit="개", at=0), dict(label="2024년 · 무릎 부상", value=95, unit="개", at=2, hi=True)],
             max=200, text="2010년부터 14년 연속 100안타 → 끊김", textAt=3.2, size=52))                                               # L18
SC.append(pv(None, "손아섭", "2025년 → 2026년", [vsteps([stp("2025년 7월", "NC → 한화 트레이드", 1.0)])], chain="s19", team="한화"))             # L19
SC.append(pv(None, "손아섭", "2025년 → 2026년", [vsteps([stp("2025년 7월", "NC → 한화 트레이드", -1), stp("그 겨울 FA", "다른 구단 제안 없음", 0.5, c="bad"),
                                                         stp("2026년 2월 5일", "한화와 1년 1억 원", 2.4)])], chain="s19", cont=True, team="한화"))      # L20
SC.append(pv(None, "손아섭", "2026년 한화", [vsteps([stp("3월 28일 개막전", "대타 한 타석", 1.0), stp("3월 30일", "2군행", 2.0, c="bad")])], chain="s21", team="한화"))   # L21
SC.append(pv(None, "손아섭", "2026년 한화 → 두산", [vsteps([stp("3월 28일 개막전", "대타 한 타석", -1), stp("3월 30일", "2군행", -1, c="bad"),
                                                          stp("4월 14일 트레이드", "두산이 이교훈 + 현금 1억 5천만 원", 1.0, c="good")])], chain="s21", cont=True, team="한화"))   # L22
SC.append(sp("손아섭A", "손아섭", "두산 데뷔전 · 4월 14일 인천 SSG전", [bb("", "홈런 · 2타점", 1.2, src=True), bb("경기 뒤", "“너무 야구가\n하고 싶었다”", 3.6)]))   # L23
SC.append(pv("손아섭C", "손아섭", "두산 · 4월", [], [st("그 뒤 10경기", "32타수 3안타", 0.2, hi=True), st("4월 29일", "2군행", 2.0)]))           # L24
SC.append(pv("손아섭B", "손아섭", "두산 · 5월", [], [st("5월 14일 복귀 뒤", "6경기 중 4경기 멀티히트", 0.3), st("5월 21일 친정 NC전", "1회 결승 적시타 · 1대0", 2.6, hi=True)]))   # L25
SC.append(sp("김원형", "김원형", "두산 감독 · 5월 21일 NC전 뒤", [bb("", "“설렁설렁 안 하고 열심히 한다는\n자체가 귀감”", 0.6), bb("", "OSEN 5월 22일", 99, src=True)]))   # L26
SC.append(pv("손아섭C", "손아섭", "2026년 두산 · 1군 말소", [vsteps([stp("4월 29일", "1번째", 0.1), stp("6월 21일", "2번째", 1.0), stp("7월 31일", "3번째", 1.4, c="bad")])]))   # L27
SC.append(pv("손아섭B", "손아섭", "2026년 1군 · KBO 기록", [], [st("경기", "54경기", 0.1), st("타율", "2할 3푼 6리", 0.6, hi=True), st("홈런", "1개", 1.2)]))   # L28
_HR = [dict(label="최형우", team="삼성", value=2734, unit="개", at=0.3), dict(label="김현수", team="KT", value=2691, unit="개", at=2.0), dict(label="손아섭", team="두산", value=2655, unit="개", at=0, hi=True)]
SC.append(S(0, "bars", title="KBO 통산 안타 · 10월 20일", items=_HR, max=3000, chain="b29"))                                     # L29
SC.append(S(0, "bars", title="KBO 통산 안타 · 10월 20일", items=_HR, max=3000, chain="b29", cont=True))   # L30
SC.append(pv("손아섭A", "손아섭", "1988년 3월생", [], [st("지금", "38살", 0.1), st("내년 3월", "39살", 1.0, hi=True)]))                  # L31
SC.append(pv("손아섭D", "손아섭", "재계약 불가 · 10월 19일", [], [st("방출 선수", "바로 다른 구단과 계약 가능", 0.6, hi=True)]))           # L32
SC.append(sp("손아섭D", "손아섭", "10월 19일 이후", [bb("관심 보인 구단", "기사 없음", 1.2, src=True), bb("본인 입장", "아직 없음", 3.0, src=True)]))   # L33
SC.append(pv("손아섭B", "손아섭", "제 생각", [], [st("주전 자리", "약속받기 어려움", 3.0), st("왼손 대타", "한 번 더 기회", 4.2, hi=True)]))      # L34
# ── 3막 · 김명신 ──
SC.append(S(0, "photo", img="경기/김명신_역투_2023_오마이뉴스", fit="cover", text="", h=760))                                   # L35
SC.append(pv("김명신A", "김명신", "두산 투수 · 33살", [], [st("2017년", "2차 2라운드 입단", 0.1), st("10년", "두산 한 팀", 1.0, hi=True)]))   # L36
SC.append(pv("김명신B", "김명신", "2017년 신인", [vsteps([stp("4월 25일", "타구에 얼굴 · 광대뼈 3곳 골절", 1.0, c="bad"), stp("수술 뒤 복귀", "그해 39경기", 4.0, c="good")])]))   # L37
SC.append(S(0, "bars", title="김명신 · 시즌 홀드", items=[dict(label="2022년", value=10, unit="홀드", at=1.0), dict(label="2023년", value=24, unit="홀드", at=2.2, hi=True)],
             max=26, text="2023년 리그 홀드 3위", textAt=3.0, size=60))                                                             # L38
SC.append(S(0, "bars", title="김명신 · 평균자책점", items=[dict(label="2022년", value=3.62, dec=2, at=0), dict(label="2023년", value=3.65, dec=2, at=0), dict(label="2024년", value=9.37, dec=2, at=1.0, hi=True)], max=10, text="1군 · 2025년 8경기 → 2026년 3경기", textAt=2.0, size=56))   # L39
SC.append(pv("김명신B", "김명신", "통산 · KBO 기록", [], [st("경기", "297경기", 0.1), st("승리", "15승", 1.0), st("홀드", "45홀드", 1.2, hi=True)]))   # L40
SC.append(sp("김명신A", "김명신", "방출 뒤 SNS · SPOTV 10월 20일 보도", [bb("", "“두산 베어스 김명신은 끝일지 몰라도\n야구선수 김명신은 조금 더 이어가 볼 생각”", 0.6)]))   # L41
SC.append(pv("김명신A", "김명신", "33살 · 오른손 투수", [], [st("2026년 2군", "31경기", 1.0), st("2군 평균자책점", "3.35", 2.0, hi=True)]))   # L42
# ── 4막 · 나머지 9명 ──
SC.append(F9())                                                                                                              # L43
SC.append(F9(hi=("박강민",), text="박강민 · 29살 · 2군 25경기 평균자책점 3.93"))                                                # L44
SC.append(F9(hi=("김지윤",), text="김지윤 · 22살 · 2군 15경기 평균자책점 7.38", textAt=1.0))                                   # L45
SC.append(F9(hi=("장우진",), text="장우진 · 22살 · 2023년 3라운드 · 북일고"))                                                    # L46
SC.append(F9(hi=("이기석",), text="이기석 · 24살 왼손 · 2군 4승 무패 평균자책점 6.52", textAt=1.0))                              # L47
SC.append(F9(hi=("백승우",), text="백승우 · 26살 · 2023년 7라운드 · 데뷔전 1이닝 무실점", textAt=1.0))                         # L48
SC.append(F9(hi=("김민혁",), text="김민혁 · 1군 통산 120경기 홈런 9개 · 올해 1군 0경기", textAt=1.0))                            # L49
SC.append(F9(hi=("지강혁",), text="지강혁 · KT 방출 → 독립리그 → 두산 육성선수", textAt=1.0))                                     # L50
SC.append(F9(hi=("이종혁", "양현진"), text="이종혁 · 올해 육성선수 / 양현진 · 2021년 10라운드", textAt=0.6))                       # L51
# ── 5막 · 다른 구단과 두산의 겨울 ──
_RL = [dict(label="롯데", team="롯데", value=16, unit="명", at=0.6), dict(label="두산", team="두산", value=11, unit="명", at=0.6, hi=True), dict(label="삼성", team="삼성", value=10, unit="명", at=0.6),
       dict(label="SSG", team="SSG", value=8, unit="명", at=0.6), dict(label="키움", team="키움", value=8, unit="명", at=0.6), dict(label="한화", team="한화", value=6, unit="명", at=0.6)]
SC.append(S(0, "bars", title="재계약 불가 · 10월 20일 기준", items=_RL, max=16, chain="b52", text="6개 구단 · 모두 59명", textAt=1.8, size=56))   # L52
SC.append(S(0, "bars", title="재계약 불가 · 10월 20일 기준", items=_RL, max=16, chain="b52", cont=True, text="SSG 박종훈도 방출", textAt=2.0, size=56))   # L53
SC.append(S(0, "tiles", title="아직 명단 발표 전", items=[dict(team=t, k="10월 20일", v="발표 전", at=0.1 + i * 0.25) for i, t in enumerate(["NC", "KT", "LG", "KIA"])]))   # L54
SC.append(sp("정재훈", "정재훈", "두산 새 단장", [bb("2027년부터", "잠실 떠나 임시 구장", 0.2, src=True), bb("첫 소감", "“변화를 두려워하지 않고”", 2.4)]))   # L55
SC.append(S(0, "question", text="손아섭\n다른 팀에서 다시 뛸까?", img=IMG["손아섭D"], size=96))                                   # L56

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "10월 19일 두산", "title": "10월 19일, 두산이 바꾼 것", "from": 5, "to": 12},
      {"key": "손아섭", "title": "손아섭 · 2655안타", "from": 13, "to": 33},
      {"key": "김명신", "title": "김명신 · 10년 원클럽", "from": 34, "to": 41},
      {"key": "나머지 9명", "title": "나머지 9명", "from": 42, "to": 50},
      {"key": "다른 구단", "title": "다른 구단과 두산의 겨울", "from": 51, "to": 55}]

TAGS = ["두산 방출", "손아섭 방출", "손아섭", "두산 베어스", "재계약 불가", "방출 명단", "김명신", "정재훈 단장", "김태룡 단장", "두산 단장 교체", "프로야구 방출",
        "2026 방출", "박강민", "김지윤", "장우진", "이기석", "백승우", "김민혁", "지강혁", "이종혁", "양현진", "통산 최다안타", "최형우", "김현수", "프로야구", "KBO", "야구자판기"]
DESC = ("두산 베어스가 10월 19일 선수 11명에게 재계약 불가를 통보했어요. 명단에는 통산 2655안타의 손아섭과 10년 동안 두산에서만 뛴 김명신이 있어요. 같은 날 두산은 16년 동안 팀을 맡은 김태룡 단장을 구단 자문으로 옮기고 정재훈 운영팀장을 새 단장으로 선임했어요.\n\n"
        "손아섭은 4월 14일 한화에서 트레이드로 두산에 왔지만 올해 1군 54경기 타율 2할 3푼 6리, 홈런 1개에 그쳤고 6개월 만에 팀을 떠나게 됐어요. 통산 안타는 최형우·김현수에 이어 역대 3위예요.\n\n"
        "재계약 불가 11명: 투수 김명신·박강민·김지윤·장우진·이기석·백승우 / 내야수 김민혁·지강혁·이종혁 / 외야수 손아섭·양현진\n\n"
        "10월 20일 기준 6개 구단(롯데 16명·두산 11명·삼성 10명·SSG 8명·키움 8명·한화 6명)이 모두 59명에게 재계약 불가를 알렸어요. NC·KT·LG·KIA 명단도 나오는 대로 구단별로 정리해 드릴게요.\n\n"
        "여러분은 손아섭이 다른 팀에서 다시 뛸 수 있다고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록: KBO 기록실(10월 20일 조회). 기사: 머니투데이·마이데일리·뉴스핌·재경일보·국제뉴스·스포츠월드(10/19), SPOTV·OSEN(10/20), OSEN(4/15·5/21·5/22), 엑스포츠뉴스(4/14), 스포츠경향(4/14·5/3), 스포츠동아(10/19), 일간스포츠(10/15)\n"
        "사진: 두산 베어스 제공, 스포츠조선, 오마이뉴스, 스포티비뉴스, 구단 공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1020-롱폼21-두산방출-근거모음.md (기사 본문 + KBO 기록실 10/20 직접 대조)."

EP = {"introChapter": "오프닝", "date": "2026-10-20", "gameDate": "2026-10-20", "series": "야구롱폼", "focusTeam": "두산", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.25, "ttsTempoSlow": 1.2,
      "rev": "1020-long21-v1", "topic": "두산방출", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼21_두산방출.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "두산 방출 11명 | 2655안타 손아섭도 6개월 만에 떠났다, 김명신까지 #두산 #손아섭 #방출",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#두산베어스", "#손아섭", "#방출", "#김명신", "#재계약불가", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 33, 55}
    HOLD = {0: 0.35, 3: 0.35, 4: 0.35, 12: 0.35, 33: 0.4, 41: 0.35, 50: 0.35, 54: 0.35}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-20_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i + 1, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
