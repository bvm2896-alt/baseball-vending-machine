# -*- coding: utf-8 -*-
"""10/24 롱폼㉙ 「다음 메이저리거 언제 가? | 원태인·노시환은 이번 겨울, 곽빈·김주원은 1년 뒤」 콘티 v2(검수 X 전부 반영).
대사 = tools/text_1024_long29.py v4 (마지막 구독 줄은 CTA_LINE 이 맡으므로 TEXT 에서 뺀다).
근거 = 프로젝트 claude/1024-롱폼29-다음메이저리거-근거모음.md + 대사v4 문서(발언·용어 근거).
v2 화면 원칙(검수 X): 글자만 있는 장면 → 아이콘 카드(icontiles)·칸 채우기(cells)·막대(capbar·bars)·로고(tiles)·사진(pstat·faces·duel·pgroup)
 · 이름 부르면 그 사람 사진(그 시절·그 사건 사진, 같은 선수 사진 번갈아) · 가운데 파란 큰 글 없음 · 화면에 '제 생각' 없음 · 약어 라벨 없음
 · 챕터마다 목차 강조(toc on=k) · 오프닝 6칸은 처음부터 자리 고정 · 라벨과 값은 같이 뜸(템플릿 keepK·had 수정).
사진: 카드/P29*(10/24 수집 — 사진 출처는 DESC), 카드/F16_원태인_*·G18_*·P15_곽빈_WC·R13_고우석_투구, 경기/*(구단 제공), 메이저리그 로고 = KBO_logos/MLB_*.svg(mlbstatic.com)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('\ndef sub_of')].replace("'text_1015_long15.py'", "'text_1024_long29.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
assert LINES[-1][0].startswith('채널 구독하고')
TEXT = [x[0] for x in LINES[:-1]]
import narr_1020
_NU = ['', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉']; _NT = ['', '열', '스물', '서른', '마흔', '쉰', '예순', '일흔', '여든', '아흔']
def _native(n): n = int(n); return _NT[n // 10] + _NU[n % 10] if 0 < n < 100 else None
def narr_of(t):
    t = re.sub(r'(\d),(\d{3})', r'\1\2', t)
    # 10/25 규칙 검수(10/1 경기 수 · 10/10 사람 수는 고유어): 99 이하 '○경기'·'○명'은 고유어로 읽는다(스물여덟 경기, 스물여섯 명). 100 이상은 한자어(백삼십오 경기)
    t = re.sub(r'(?<![\d.])(\d{1,2})(경기|명)', lambda m: (_native(m.group(1)) + ' ' + m.group(2)) if _native(m.group(1)) else m.group(0), t)
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)
    n = n.replace('KT', '케이티').replace('KIA', '기아').replace('LG', '엘지').replace('SSG', '에스에스지').replace('NC', '엔씨').replace('FA', '에프에이').replace('WBC', '더블유비씨')
    n = n.replace('십일 월', '십일월').replace('십이 월', '십이월')
    return n
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))
# 10/24 검수(롱폼㉙ L116 자막 '500만 437만 5천 945만' 이 한 숫자로 읽힘): 더하는 줄은 자막에 '+'
SUBFIX = {141: '이정후는 1억 1300만 달러라 / 세 구간을 다 거쳐 / 500만\n437만 5천 / 945만 달러를 더한 / 1882만 5천 달러였어요',
          131: '2018년에 규정이 바뀌기 전엔 / 메이저리그 구단들이 / 금액을 써내는 입찰이었어요',   # 10/25 검수: '써내다'는 한 단어
          132: '가장 많이 써낸 구단 한 곳만 / 선수와 협상할 수 있었고, / 그 입찰액이 그대로 이적료였어요',
          133: '류현진의 2573만 달러도 / 다저스가 써낸 입찰액이에요'}

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
C, K, G = '카드/', 'KBO프로필/', '경기/'
IMG = {None: None}
PROF = {"원태인": K + "원태인", "노시환": K + "노시환_한화", "곽빈": K + "곽빈", "김주원": K + "김주원", "김도영": K + "김도영", "안우진": K + "안우진"}
TEAM = {"원태인": "삼성", "노시환": "한화", "곽빈": "두산", "김주원": "NC", "김도영": "KIA", "안우진": "키움", "송성문": "샌디에이고", "김혜성": "다저스", "고우석": "LG",
        "이정후": "샌프란시스코", "류현진": "한화", "강정호": "피츠버그", "김하성": "샌디에이고", "박병호": "미네소타", "스즈키 세이야": "컵스"}
RED, GREEN = '#E5484D', '#1F9D55'
def pv(img, name, sub, viz=(), stats=(), **k):
    return S(0, "pstat", img=IMG.get(img, img), team=k.pop("team", TEAM.get(name, "KBO")), name=name, sub=sub, viz=list(viz), stats=list(stats), **k)   # 10/25: noCenter 뺌(10/18 골든글러브 검수 X "인물 카드 왼쪽 치우침") — 묶음 전체 가운데·사진은 묶음 내내 고정(ensureCx data-anchor)
def sp(name, sub, bubbles, img, **k): return S(0, "speech", img=img, team=k.pop("team", TEAM[name]), name=name, sub=sub, bubbles=bubbles, **k)
def fg(title, people, chain, at0=None, posAt=None, **k):
    """facegrid — people: [(이름, 묶음 이름표)]. 얼굴 칸은 프로필(요약판 예외). cw·d 로 칸을 크게(10/24 검수 '얼굴 작고 아래 빔')"""
    its = []
    for i, (n, pos) in enumerate(people):
        d = dict(name=n, img=PROF[n], team=TEAM[n], pos=pos)
        if at0 is not None: d["at"] = at0[i] if isinstance(at0, (list, tuple)) else at0 + i * 0.12
        if posAt is not None and posAt[i] is not None: d["posAt"] = posAt[i]
        its.append(d)
    return S(0, "facegrid", title=title, cols=k.pop("cols", len(people)), card=True, chain=chain, profile=True, nameLogo=True, items=its, **k)
def ict(title, items, **k): return S(0, "icontiles", title=title, items=items, **k)
def tile(icon, top, v, at=0, **x): return dict({"icon": icon, "top": top, "v": v, "at": at, "k": " "}, **x)   # k 자리는 늘 잡아 둔다(설명 줄이 생길 때 칸 높이가 안 바뀌게)
def ghost(d): return dict(d, at=50, ghost=True)
def toc(on, **k): return S(0, "toc", on=on, **k)

SC = []
# ── 오프닝 0~6 ──
O6 = "다음 메이저리거 후보"
G1, G2, G3 = "이번 겨울", "빠르면 1년 뒤", "더 기다려야 함"   # 10/25 사용자 "더 기다려야가 뭐야"
P6 = [("원태인", G1), ("노시환", G1), ("곽빈", G2), ("김주원", G2), ("안우진", G3), ("김도영", G3)]
OG = dict(cols=6, cw=182, d=146, posPad=True)   # posPad: 묶음 이름표 자리를 처음부터(첫 줄 ? 칸이 둘째 줄에서 내려가지 않게)
FG2 = dict(cols=2, cw=440, d=232)
SC.append(fg(O6, [], "o0", phShow=2, **OG))   # 0 (10/25 검수: "두 명이에요"인데 ? 6칸 → 처음엔 ? 2칸만 보이고 나머지 자리는 비워 둠) — 10/25 사용자 "누군지 말도 안 했는데 먼저 나와 있지 않게": 이름 부르기 전엔 ? 6칸만
SC.append(fg(O6, P6[:2], "o0", at0=[0.15, 1.55], cont=True, **OG))   # 1 — 삼성 원태인 / 그리고 한화 노시환: 부르는 호흡에 뜬다
SC.append(fg(O6, P6[:4], "o0", at0=[-1, -1, 0.2, 0.62], posAt=[-1, -1, 1.0, 1.0], cont=True, **OG))                                 # 2
SC.append(fg(O6, P6, "o0", at0=[-1, -1, -1, -1, 0.2, 0.62], posAt=[-1, -1, -1, -1, 1.0, 1.0], cont=True, **OG))                             # 3
SC.append(fg(O6, P6, "o0", at0=-1, cont=True, **OG))                                                    # 4
SC.append(toc(-1, itemSeg=[0.0, 1.0, 1.5, 2.0, 3.0, 4.0, None, None, None]))                            # 5
SC.append(toc(-1, itemSeg=[None] * 6 + [0.0, 1.0, 2.0], cont=True))                                     # 6
# ── 1막 · 규칙 7~24 ── (10/25 사용자 "카드와 텍스트로 떼우지 말고 모션그래픽으로": 두 갈래 길 · 등록일수 막대 · 포스팅 흐름)
SC.append(toc(0))                                                                                        # 7
def roads(step, **k): return S(0, "roads", step=step, chain="rd", **k)
def dayf(step, **k): return S(0, "dayfill", step=step, chain="df", **k)
def post(step): return S(0, "posting", step=step, chain="ps", deal="SD", team="KBO", title="포스팅 절차 · 매년 겨울")
SC.append(roads(1, title="KBO → 메이저리그 · 두 가지 길"))                                                  # 8
SC.append(roads(2, title="KBO → 메이저리그 · 두 가지 길"))                                                  # 9
SC.append(dayf(1, title="1시즌 인정 기준"))                                                                 # 10
SC.append(dayf(2, title="1시즌 인정 기준"))                                                                 # 11
for st_ in range(1, 7): SC.append(post(st_))                                                             # 12~17
SC.append(roads(3, title="FA · 구단 허락 없이"))                                                             # 18
SC.append(roads(4, title="FA · 구단 허락 없이"))                                                             # 19
SC.append(dayf(3, title="국가대표 포인트"))                                                                 # 20
SC.append(dayf(4, title="국가대표 포인트"))                                                                 # 21
SC.append(dayf(5, title="국가대표 포인트"))                                                                 # 22
SC.append(dayf(6, title="국가대표 포인트"))                                                                 # 23
SC.append(roads(5, title="정리 · 두 가지 길"))                                                              # 24
SC.append(toc(1))                                                                                        # 25
# ── 2막 · 원태인 26~41 ── (10/25 사용자 "사진이 너무 자주 바뀌고 틀의 크기가 자주 바뀌어": 한 묶음 · 사진 2장 · 꼬리표 고정)
WA = G + "원태인_투구_0828_삼성제공"; WB_ = WA   # 10/25 검수(같은 원태인 구간에서 사진이 바뀜): 같은 2026시즌이라 한 장으로
def wt(img, viz=(), stats=(), **k): return pv(img, "원태인", "삼성 투수", viz, stats, chain="w26", **k)
def mini(items): return dict(type="mini", items=items)
def vq(date, text, at, src=True, **k): return dict(type="quote", date=date, text=text, at=at, src=src, **k)   # 10/25 사용자 "글자들이 갑자기 너무 작아졌어" — 크기는 템플릿 기본(60)
def seasons(items, title=None, **k): return dict(type="seasons", items=items, **({"title": title} if title else {}), **k)
SC.append(wt(WA, enterAt=1.0))                                                                           # 26
SC.append(wt(WA, [vsteps([stp("2019년", "삼성 데뷔", 0.5, c="good")])]))                                    # 27
SC.append(wt(WA, [vsteps([stp("2019년", "삼성 데뷔", -1, c="good"), stp("2024년", "28경기 15승 6패", 0.3), stp("평균자책점", "3.66", 1.0)]),
                  dict(mini([dict(img=C + "G18P_곽빈", name="곽빈", team="두산", k="15승", at=2.0)]), stamp=dict(t="공동 다승왕", at=3.0, c="gold", size=48))]))   # 10/25: 도장을 작은 얼굴 옆으로(세로로 쌓이면 묶음 전체가 줄어듦)   # 28
SC.append(wt(WA, [seasons([dict(t=str(i), at=1.0 + (i - 1) * 0.08) for i in range(1, 9)] + [dict(t="FA", hi=True, at=2.0)], title="고졸 선수 FA = 8시즌", bw=96)]))   # 29
SC.append(wt(WA, [seasons([dict(t=str(j + 1), at=0.2 + j * 0.1) for j, y in enumerate(range(2019, 2027))] + [dict(t="첫 FA", hi=True, at=3.0, fs=38, w=150)], title="원태인 · 2019 ~ 2026 = 8시즌", bw=90, gap=8)]))   # 30
W31 = [st("삼성 허락", "필요 없음", 1.0, hi=True), st("해외 구단", "협상 가능", 2.0)]
SC.append(wt(WA, [vstamp("삼성은 못 막는다", 50, "bad", size=52)], W31))                                     # 31
SC.append(wt(WA, [vstamp("삼성은 못 막는다", 0.6, "bad", size=52)], [dict(x, at=-1) for x in W31]))            # 32
WQ = [("2024년 12월 · 포스팅", "신청할 생각 없다"), ("이유 · 요약", "아직 부족하다"), ("도전 · 요약", "2년 더 발전하면 FA 때")]
def wq(ats): return wt(WA, [vq(d, t, a) for (d, t), a in zip(WQ, ats)])
SC.append(wq([0.3, 50, 50]))                                                                             # 33
SC.append(wq([-1, 0.2, 50]))                                                                             # 34
SC.append(wq([-1, -1, 0.3]))                                                                             # 35
SC.append(wt(WA, [vsteps([stp("2024년 12월", "포스팅 생각 없음", 0.0), stp("2026시즌 뒤", "첫 FA · 이번 겨울", 1.0, c="gold")])]))   # 36
SC.append(wt(WB_, [vsteps([stp("시즌 전", "부상 · WBC(국가대항전) 못 나감", 1.0, c="bad"), stp("개막", "출발 늦음", 2.0, c="bad")])]))   # 37 (사진: 2026시즌)
W38 = [st("승패", "7승 9패", 1.0), st("평균자책점", "4.52", 2.0, hi=True), st("8월 보도 기준", "메이저리그 에이전트 아직 안 정함", 50, hi=True)]
SC.append(wt(WB_, [], W38))                                                                               # 38
SC.append(wt(WB_, [], [dict(W38[0], at=-1), dict(W38[1], at=-1), dict(W38[2], at=1.5)]))                     # 39
SC.append(wt(WB_, [dict(type="hops", items=[dict(team="삼성", t="삼성", at=0.2), dict(icon="VS", t="10월 25일~ 플레이오프", at=1.0, hi=True), dict(team="KIA", t="기아", at=2.0)])]))   # 40 플레이오프
SC.append(wt(WB_, [], [st("FA 자격", "있음", 1.0), st("남은 것", "본인 선택", 1.2, hi=True)]))                  # 41
# ── 3막 · 노시환 42~54 ── (사진 1장: 한화 제공 · 워터마크 없음)
SC.append(toc(2))                                                                                        # 42
NH = "카드/P29w_노시환_0512"   # 10/25 사용자 "노시환 사진 화질이 너무 구려" — 손하트(640px) → 0512 경기(워터마크 잘라냄)
def nh(viz=(), stats=(), **k): return pv(NH, "노시환", "한화 내야수", viz, stats, chain="n43", **k)
SC.append(nh([], [st("2023년", "31홈런 · 101타점", 1.0), st("타이틀", "홈런왕 · 타점왕", 1.6, hi=True)]))   # 43
N44 = [st("2026년 2월 23일", "한화와 11년 계약", 0.2, hi=True), st("기간", "2027 ~ 2037시즌", 50), st("옵션 포함 총액", "307억 원", 50, hi=True)]
SC.append(nh([], N44))                                                                                   # 44
SC.append(nh([], [dict(N44[0], at=-1), dict(N44[1], at=0.2), dict(N44[2], at=2.0)]))                       # 45
NS = [stp("계약서", "특별 조항 1개", 0, c="gold"), stp("시점", "2026시즌 뒤 포스팅", 0, c="good"), stp("범위", "메이저리그만", 0), stp("돌아오면", "한화 선수", 0)]
def ns(ats, stampAt=50): return nh([vsteps([dict(x, at=a) for x, a in zip(NS, ats)]), vstamp("이번 겨울이 그때", stampAt, "gold", size=48)])
SC.append(ns([1.0, 50, 50, 50]))                                                                         # 46
SC.append(ns([-1, 0.3, 50, 50]))                                                                         # 47
SC.append(ns([-1, -1, 0.3, 2.0]))                                                                        # 48
SC.append(ns([-1, -1, -1, -1], stampAt=1.0))                                                             # 49
NQ = [("2026년 2월 · 계약 직후", "한국 최고가 됐을 때 도전"), ("계약 이유 · 요약", "구단이 기회를 마련해 줘서")]
SC.append(nh([vq(*NQ[0], 1.0), vq(*NQ[1], 50)]))                                                          # 50
SC.append(nh([vq(*NQ[0], -1), vq(*NQ[1], 0.3)]))                                                          # 51
N52 = [st("타율", ".283", 1.0), st("홈런 · 타점", "29홈런 · 96타점", 2.0), st("10월 14일 보도 기준", "포스팅 신청 발표 없음", 50, hi=True)]
SC.append(nh([], N52))                                                                                   # 52
SC.append(nh([], [dict(N52[0], at=-1), dict(N52[1], at=-1), dict(N52[2], at=0.1)]))                       # 53
SC.append(nh([], [st("구단 허락", "이미 계약서에", 1.0), st("남은 것", "본인 결정", 2.0, hi=True)]))           # 54
# ── 4막 · 직장폐쇄 55~71 ── (모션 그래픽: 노사협약 · 지침 · 멈춤 · 99일 · 이번 겨울 달력 · 다른 길)
SC.append(toc(3))                                                                                        # 55
def lk(mode, step=1, **k): return S(0, "lockout", mode=mode, step=step, **k)
for st_ in range(1, 5): SC.append(lk("cba", st_, title="메이저리그 노사협약", chain="lk56"))                   # 56~59
SC.append(S(0, "capbar", title="쟁점 · 샐러리캡", max=480, cap=360, capLabel="샐러리캡", capAt=0.3,
            segs=[dict(label="팀 연봉 총액", vt=" ", v=360, at=0.1), dict(label="넘으면 ✕", vt=" ", v=110, at=0.5, color=RED)]))   # 10/25 검수: 상한선 = 파랑 끝, 빨강은 선 바깥부터   # 60 (10/25 검수: 넘는 칸이 막히는 그림)
SC.append(S(0, "debate", title="샐러리캡 · 팀 연봉 총액 상한선", left=dict(label="구단주", t="도입하려 함", at=2.0), right=dict(label="선수노조", t="강하게 반대", at=3.0), enterAt=2.0))   # 61 (10/25 검수: 상한선 설명 동안 막대 유지 · 양쪽 같은 색)
SC.append(lk("memo", title="메이저리그 사무국 · 10월 초"))                                                    # 62
SC.append(lk("freeze", title="직장폐쇄가 시작되면"))                                                         # 63
SC.append(lk("past", title="지난번 직장폐쇄"))                                                              # 64
SZI = C + "P29w_스즈키_컵스"
SC.append(lk("pause30", 1, title="2021년 겨울 · 직장폐쇄", chain="z65"))                                 # 65 (10/25 검수: 컵스 사진이 계약보다 먼저 보이지 않게)
SC.append(lk("pause30", 2, title="2021년 겨울 · 직장폐쇄", chain="z65"))                                 # 66
SC.append(pv(SZI, "스즈키 세이야", "시카고 컵스", [vq("2022년 3월 · 입단 회견", "마이크 트라웃, 사랑해요", 1.0, src=False)], team="컵스"))   # 67
SC.append(lk("winter", 1, title="이번 겨울 포스팅", chain="lk68"))                                           # 68
SC.append(lk("alt", title="직장폐쇄가 길어지면"))                                                            # 69
SC.append(lk("winter", 2, title="이번 겨울의 관건"))                                                         # 70
SC.append(S(0, "question", text="직장폐쇄 전체 편은\n오른쪽 위 카드에서", img="상황별/썸네일_롱폼11_직장폐쇄_윗줄뺌", ph=495, arrow="ur", size=78))   # 71 (10/25: 영상 중간 = 오른쪽 위 카드)
# ── 5막 · 곽빈 · 김주원 72~86 ──
SC.append(toc(4))                                                                                        # 72
GBi = dict(img=C + "G18_곽빈_C", name="곽빈", team="두산", role="두산 투수")
KJi = dict(img=C + "G18_김주원_A", name="김주원", team="NC", role="NC 유격수")
def g73(gb, kj, **k): return S(0, "faces", title=G2, chain="g73", side=True, items=[dict(GBi, **gb), dict(KJi, **kj)], **k)   # 10/25: 사진 옆에 기록(세로로 넘쳐 80%로 줄던 것)
SC.append(g73(dict(at=0.1, note="2023 항저우 금\n병역 해결", noteAt=50), dict(at=1.0, note="2023 항저우 금\n병역 해결", noteAt=50)))   # 꼬리표 자리를 처음부터 잡아 둔다(R4)                                                                # 73
SC.append(g73(dict(at=-1, note="2023 항저우 금\n병역 해결", noteAt=1.0), dict(at=-1, note="2023 항저우 금\n병역 해결", noteAt=1.0), cont=True))   # 74
SC.append(g73(dict(at=-1, note="아시안게임 금\n+25포인트", noteAt=0.9), dict(at=-1, note="아시안게임 금\n+25포인트", noteAt=0.9), cont=True))   # 75
SC.append(g73(dict(at=-1, note="아시안게임 금\n+25포인트", noteAt=-1), dict(at=-1, note="포인트로\n등록일수 채움", noteAt=0.4), cont=True))   # 76
SC.append(g73(dict(at=-1, note="2027시즌 뒤\n포스팅", noteAt=1.5), dict(at=-1, note="2027시즌 뒤\n포스팅", noteAt=1.5), cont=True))   # 77
GB = G + "곽빈_포효0823_두산제공_상체"   # 10/25 검수(같은 사진이 작은 카드 ↔ 큰 카드로 튐): 혼자 나오는 곽빈 장면은 다른 사진(2026시즌)
GB24 = C + "P29c_곽빈_2024"   # 2024년 공동 다승왕 장면은 그 시절 사진
def gb(viz=(), stats=(), **k): return pv(GB, "곽빈", "두산 투수", viz, stats, chain=k.pop("chain", "g78"), **k)
SC.append(pv(GB24, "곽빈", "두산 투수", [dict(mini([dict(img=C + "G18P_원태인", name="원태인", team="삼성", k="15승", at=1.0)]), stamp=dict(t="2024년 공동 다승왕", at=1.5, c="gold", size=48))], [], chain="g78"))   # 78
SC.append(gb([], [st("2026시즌", "27경기 11승 7패", 0.3), st("평균자책점", "2.24", 1.0, hi=True), st("탈삼진", "197개", 2.0, hi=True), st("두 부문 1위", "평균자책점 · 탈삼진", 2.6, hi=True)]))   # 79
DL = dict(img=C + "P29c_곽빈_0829B", name="곽빈", team="두산", at=1.0); DR = dict(img=C + "P29c_안우진_역투2", name="안우진", team="키움", at=1.55)
SC.append(S(0, "duel", title="8월 29일 잠실 · 맞대결", left=DL, right=DR, vsAt=1.0, pw=300, chain="d80", badge=dict(t="메이저리그 스카우트 5개 구단", at=2.0)))       # 80
SC.append(S(0, "duel", title="8월 29일 잠실 · 맞대결", left=dict(DL, at=-1), right=dict(DR, at=-1), vsAt=-1, pw=300, chain="d80", badge=dict(t="메이저리그 스카우트 5개 구단", at=-1),
            logos=[dict(team=n, t=n, at=a) for n, a in [("다저스", 0.1), ("양키스", 0.35), ("샌디에이고", 0.6), ("토론토", 0.85), ("캔자스시티", 1.05)]]))   # 81
GQ = [("2026년 9월 · 아시안게임 결승 뒤 · 요약", "야구 시작할 때부터 미국 도전"), ("목표 · 요약", "보완해서 최고의 상태로 미국행")]
SC.append(gb([vq(*GQ[0], 1.0), vq(*GQ[1], 50)], chain="g82"))                                              # 82
SC.append(gb([vq(*GQ[0], -1), vq(*GQ[1], 1.0)], chain="g82"))                                              # 83
KJ = C + "P29c_김주원_대표팀"   # 10/25 검수(같은 사진이 작은 카드 ↔ 큰 카드로 튐): 혼자 나오는 김주원 장면은 다른 사진
def kj(viz=(), **k): return pv(KJ, "김주원", "NC 유격수", viz, chain="k84", **k)
KQ = ("2026년 1월 · 요약", "미국에 도전할 만한 선수가 첫 번째")   # 10/25: 날짜 띠를 줄여 한 줄로(글이 작아지지 않게)
SC.append(kj([vq(*KQ, 1.0)]))                                                                             # 84
SC.append(kj([vq(*KQ, -1), mini([dict(img=C + "G18P_김혜성", name="김혜성", team="다저스", k="다저스", at=0.1), dict(img=C + "G18P_송성문", name="송성문", team="샌디에이고", k="샌디에이고", at=0.3)]) | dict(d=104),
              vq("요약", "자연스럽게 미국 무대가 생각나", 2.0)]))                                                # 85
SC.append(g73(dict(at=0.1, note="내년 풀타임이\n첫 조건", noteAt=1.5), dict(at=0.1, note="내년 풀타임이\n첫 조건", noteAt=1.5), )) # 86
# ── 6막 · 김도영 · 안우진 87~102 ── (김도영 사진 2장: 45호 → 아시안게임)
SC.append(toc(5))                                                                                        # 87
KD45 = G + "김도영_45호_포효_1012_스포츠조선"; KDAG = KD45   # 10/25 검수(김도영 구간 중간에 사진이 바뀜): 한 장으로
def kd(img, viz=(), stats=(), **k): return pv(img, "김도영", "KIA 3루수", viz, stats, chain="k88", **k)
K88 = [st("2026년", "45홈런 · 홈런왕", 1.0, hi=True), st("135경기", "타율 .308", 50), st("타점 · 득점", "118타점 · 120득점", 50)]
SC.append(kd(KD45, [], K88))                                                                              # 88
SC.append(kd(KD45, [], [dict(K88[0], at=-1), dict(K88[1], at=0.3), dict(K88[2], at=2.0)]))                   # 89
K90 = [stp("9월", "아시안게임 금메달", 0, c="good"), stp("병역", "해결", 0, c="good"), stp("이 대회 포인트", "받지 못함", 0, c="bad")]
SC.append(kd(KDAG, [vsteps([dict(x, at=a) for x, a in zip(K90, [0.4, 1.0, 50])])]))                          # 90
SC.append(kd(KDAG, [vsteps([dict(x, at=a) for x, a in zip(K90, [-1, -1, 2.5])])]))                           # 91
K92 = [stp("2025년", "부상 · 등록 145일 미만", 0, c="bad"), stp("포스팅 자격", "1년 밀림", 0, c="bad"), stp("계산", "2029시즌 뒤", 0, c="gold"), stp("다른 보도", "2028시즌 뒤", 0)]
def k92(ats): return kd(KDAG, [vsteps([dict(x, at=a) for x, a in zip(K92, ats)])])
SC.append(k92([1.0, 50, 50, 50]))                                                                        # 92
SC.append(k92([-1, 0.3, 2.0, 50]))                                                                       # 93
SC.append(k92([-1, -1, -1, 0.2]))                                                                        # 94
DQ = [("2025년 1월 · 출국 인터뷰 · 요약", "최종 목표는 메이저리그"), ("요약", "아직 한참 남은 꿈")]
SC.append(kd(KDAG, [vq(*DQ[0], 1.0), vq(*DQ[1], 50)]))                                                     # 95
SC.append(kd(KDAG, [vq(*DQ[0], -1), vq(*DQ[1], 0.2)]))                                                     # 96
AW = C + "P29c_안우진_역투2"
def aw(viz=(), stats=(), **k): return pv(AW, "안우진", "키움 투수", viz, stats, chain="a97", **k)
SC.append(aw())                                                                                           # 97
SC.append(aw([seasons([dict(t="지금 5시즌", at=0.2, w=250, c="#7A8BA8"), dict(t="+ 2027년", at=1.0, w=240), dict(t="+ 2028년", at=1.3, w=240), dict(t="= 7시즌", hi=True, at=3.0, w=230)], title="포스팅 자격 7시즌")]))   # 98
SC.append(aw([], [st("대부분 보도", "2028시즌 뒤", 1.0, hi=True), st("일부 기사", "2027시즌 뒤", 2.0)]))          # 99
AQ = [("2026년 4월 · 복귀전 뒤 · 요약", "기회 되면 모든 선수가 도전"), ("지금은 · 요약", "7·8이닝 던질 몸이 먼저")]
SC.append(aw([vq(*AQ[0], 0.6), vq(*AQ[1], 50)]))                                                          # 100
SC.append(aw([vq(*AQ[0], -1), vq(*AQ[1], 1.0)]))                                                          # 101
SC.append(fg("보도 기준 · 포스팅 시점", [("안우진", "2028시즌 뒤"), ("김도영", "2028~29시즌 뒤")], "f102", at0=[1.0, 2.0], **FG2))   # 102
# ── 7막 · 먼저 진출한 선수들 103~117 ── (한 사람 한 묶음)
SC.append(toc(6))                                                                                        # 103
SS_ = C + "P29c_송성문_SD"
def ss(viz=(), stats=(), **k): return pv(SS_, "송성문", "샌디에이고 내야수", viz, stats, chain="s104", team="샌디에이고", **k)
SC.append(ss(viz=[dict(type="hops", items=[dict(team="키움", t="키움", at=0.4), dict(icon="공시", t="11월 포스팅", at=1.0, hi=True), dict(team="샌디에이고", t="30일 안 계약", at=3.0)])], enterAt=0.4))   # 104
SC.append(ss([], [st("보장", "4년 1500만 달러", 0.3, hi=True), st("키움 이적료", "300만 달러", 2.0, hi=True)]))   # 105
SSQ = ("2025년 12월 · 귀국한 날 · 요약", "1차 목표는 메이저리그 로스터")
SC.append(ss([vq(*SSQ, 2.0)], [st("로스터", "경기에 뛸 수 있는 26명", 50)]))                                 # 106
SC.append(ss([vq(*SSQ, -1)], [st("로스터", "경기에 뛸 수 있는 26명", 1.7)]))                                  # 107
SC.append(ss([], [st("2026 메이저리그", "78경기", 0.6), st("타율", ".191", 1.0, hi=True), st("홈런", "1개", 1.2)]))   # 108
HS = C + "P29c_김혜성_다저스"
def hs(viz=(), stats=(), **k): return pv(HS, "김혜성", "LA 다저스", viz, stats, chain="h109", **k)
H109 = [st("2025년 1월 계약", "3년 보장 1250만 달러", 2.0, hi=True), st("2026 메이저리그", "43경기 · 타율 .259", 50), st("리그 결승(챔피언십시리즈)", "엔트리 제외", 50, hi=True)]
SC.append(hs([], H109))                                                                                   # 109
SC.append(hs([], [dict(H109[0], at=-1), dict(H109[1], at=0.3), dict(H109[2], at=2.0)]))                     # 110
SC.append(hs([vq("2026시즌을 마치며 · 요약", "실망스러운 한 해", 0.0)], [dict(x, at=-1) for x in H109]))          # 111
GW1, GW2 = C + "P29c_고우석_SD", G + "고우석_마운드_LG제공"
def gw(img, viz=(), stats=(), **k): return pv(img, "고우석", "LG 출신 투수", viz, stats, chain="w112", team=k.pop("team", "샌디에이고"), **k)
SC.append(gw(GW1, [], [st("2024년 1월", "샌디에이고", 1.0), st("계약", "2년 450만 달러", 2.0, hi=True)]))       # 112
SC.append(gw(GW1, [dict(type="hops", items=[dict(team="샌디에이고", t="샌디에이고", at=0.0), dict(team="마이애미", t="마이애미", at=0.2), dict(team="디트로이트", t="디트로이트", at=0.5),
                                          dict(team="미네소타", t="미네소타", at=0.8), dict(icon="7/10", t="첫 등판", at=1.0, hi=True)])]))   # 113
SC.append(gw(GW1, [], [st("2026 메이저리그", "4경기", 1.0), st("평균자책점", "9.00", 2.0, hi=True)]))           # 114
SC.append(gw(GW2, [vsteps([stp("9월 1일", "LG 복귀", 1.0, c="good")])], [st("계약", "1년 · 연봉 5억 원", 1.3, hi=True)], team="LG"))   # 115 (사진: LG)
SC.append(gw(GW2, [vsteps([stp("9월 1일", "LG 복귀", -1, c="good")]), vq("2026년 9월 3일 · 잠실", "가족이 가장 컸다", 0.6)], [st("계약", "1년 · 연봉 5억 원", -1, hi=True)], team="LG"))   # 116
SC.append(S(0, "faces", title="먼저 진출한 선수들 · 2026", items=[
    dict(img=SS_, name="송성문", team="샌디에이고", role="타율", note=".191", at=0.0, noteAt=3.0),
    dict(img=HS, name="김혜성", team="다저스", role="타율", note=".259", at=0.1, noteAt=3.0),
    dict(img=GW1, name="고우석", team="", role="평균자책점", note="9.00", at=0.2, noteAt=3.0)]))   # 117
# ── 8막 · 역대 이적료 118~137 ── (선수마다 한 카드: 이적료 → 본인 말)
SC.append(toc(7))                                                                                        # 118
def fp(img, name, sub, viz=(), stats=(), chain=None, **k): return pv(img, name, sub, viz, stats, chain=chain, **k)
RH = C + "P29d_류현진_2012한화"   # 10/25 사용자 "류현진도 화질이 너무 구려" — 500px → 매일경제 2012 한화 사진(1100px, 워터마크 없음)
R119 = [st("포스팅 이적료", "2573만 달러 남짓", 2.0, hi=True), st("다저스 계약", "6년 3600만 달러", 50)]
SC.append(fp(RH, "류현진", "2012년 · 한화", [], R119, "r119", team="한화", enterAt=1.4))                       # 119
SC.append(fp(RH, "류현진", "2012년 · 한화", [], [dict(R119[0], at=-1), dict(R119[1], at=1.0)], "r119", team="한화"))   # 120
SC.append(fp(RH, "류현진", "2012년 · 한화", [vq("2012년 12월 · 입단 회견", "최종 목표는 박찬호의 124승 넘기", 1.4, src=False)], [dict(x, at=-1) for x in R119], "r119", team="한화"))   # 121
LJ = C + "P29w_이정후_SF"
SC.append(fp(LJ, "이정후", "2023년 · 키움 → 샌프란시스코", [], [st("포스팅 이적료", "1882만 5천 달러", 2.0, hi=True)], "l122", team="키움", enterAt=1.2))   # 122
SC.append(fp(LJ, "이정후", "2023년 · 키움 → 샌프란시스코", [vq("2023년 12월 · 입단식", "이기기 위해 여기 왔다", 0.3, src=False)], [st("포스팅 이적료", "1882만 5천 달러", -1, hi=True)], "l122", team="키움"))   # 123
PB = C + "P29w_박병호_미네소타"
SC.append(fp(PB, "박병호", "2015년 · 넥센 → 미네소타", [], [st("포스팅 이적료", "1285만 달러", 1.0, hi=True)], "p124", team="키움"))   # 124
SC.append(fp(PB, "박병호", "2015년 · 넥센 → 미네소타", [vq("2015년 12월 · 입단 회견 · 요약", "내 선택, 크게 만족", 0.4)], [st("포스팅 이적료", "1285만 달러", -1, hi=True)], "p124", team="키움"))   # 125
KH = C + "P29w_김하성_SD"
SC.append(fp(KH, "김하성", "2020년 · 키움 → 샌디에이고", [], [st("포스팅 이적료", "552만 5천 달러", 1.0, hi=True)], "h126", team="키움"))   # 126
SC.append(fp(KH, "김하성", "2020년 · 키움 → 샌디에이고", [vq("2021년 1월 · 입단 회견 · 요약", "월드시리즈 우승할 팀", 1.0), vq("입단 이유", "이기는 팀에 있고 싶었다", 2.0, src=False)],
             [st("포스팅 이적료", "552만 5천 달러", -1, hi=True)], "h126", team="키움"))   # 127
KJH = C + "P29c_강정호_피츠버그"
SC.append(fp(KJH, "강정호", "2014년 · 넥센 → 피츠버그", [], [st("포스팅 이적료", "500만 달러 남짓", 1.0, hi=True)], "j128", team="키움"))   # 128
SC.append(fp(KJH, "강정호", "2014년 · 넥센 → 피츠버그", [vq("2015년 1월 · 계약 발표 · 요약", "피츠버그 승리 위해 최선", 0.5)], [st("포스팅 이적료", "500만 달러 남짓", -1, hi=True)], "j128", team="키움"))   # 129
FEE = [dict(label="류현진", sub="2012년 · 한화", img=C + "G18P_류현진", team="한화", value=2573, note="2573만 달러 남짓"),
       dict(label="이정후", sub="2023년 · 키움", img=C + "G18P_이정후", team="키움", value=1882.5, note="1882만 5천 달러"),
       dict(label="송성문", sub="2025년 · 키움", img=C + "G18P_송성문", team="키움", value=300, note="300만 달러"),
       dict(label="김혜성", sub="2025년 · 키움", img=C + "G18P_김혜성", team="키움", value=250, note="250만 달러")]
SC.append(S(0, "bars", title="포스팅 이적료 비교", max=2600, items=[dict(FEE[0], at=0.0), dict(FEE[1], at=0.0), dict(FEE[2], at=1.0, hi=True), dict(FEE[3], at=2.0, hi=True)]))   # 130
# 10/25 사용자 "포스팅 이적료 계산법에 대해서 좀만 더 자세히" → 대사 5줄 늘림(131~137), "계산한 것도 텍스트로 떼우지 말고 모션그래픽으로" → feecalc 묶음(138~142)
# 10/25 사용자 "시청자가 보기 편하게 깔끔하게 정리" → 한 화면에 이야기 하나: 옛 방식(131~133) / 지금 30개 구단(134) / 보장 금액 → 구간(135~137)
for st_ in range(1, 4): SC.append(S(0, "feerule", step=st_, title="2018년 규정 변경 전 · 입찰 방식", chain="fr131"))   # 131~133
SC.append(S(0, "feerule", step=4, title="지금 포스팅 방식"))                                                     # 134
for st_ in range(5, 8): SC.append(S(0, "feerule", step=st_, title="이적료는 보장 금액으로", chain="fr135"))          # 135~137
# 10/25 사용자 "5천만 달러까지는 이야기하는데 막대에 5천만 달러가 안 써져 있어 / 2500만 달러도" · "눈에 하나도 안 들어와" → 구간 칸은 말하는 순간 끝 금액과 같이, 계산은 그림(막대 → ×비율 → 금색 조각 → 모아서 이적료)
SC.append(S(0, "feecalc", title="구간마다 다른 비율", zAt=[0.0, 1.0, 2.0]))                                                     # 138
FT = "보장 금액 구간별 이적료"
SC.append(S(0, "feecalc", title=FT, chain="fc139", p=dict(name="송성문", img=C + "G18P_송성문", amt=1500, fillAt=0.1, partAt=[0.9], sumAt=1.35)))   # 139
SC.append(S(0, "feecalc", title=FT, chain="fc139", p=dict(name="김하성", img=C + "G18P_김하성", amt=2800, fillAt=0.1, partAt=[1.0, 2.0], sumAt=2.75)))   # 140
SC.append(S(0, "feecalc", title=FT, chain="fc139", p=dict(name="이정후", img=C + "G18P_이정후", amt=11300, fillAt=0.1, partAt=[2.0, 2.4, 2.85], sumAt=3.75)))   # 141
SC.append(S(0, "feecalc", mode="cmp", title="보장 금액과 이적료", pct=True, pctAt=3.0, feeAt=0.25,
            rows=[dict(name="이정후", img=C + "G18P_이정후", amt=11300, fee=1882.5, at=0.0), dict(name="김하성", img=C + "G18P_김하성", amt=2800, fee=552.5, at=0.08),
                  dict(name="송성문", img=C + "G18P_송성문", amt=1500, fee=300, at=0.16)]))   # 142
# ── 9막 · 정리 138~147 ──
SC.append(toc(8))                                                                                        # 138
SUM = [("원태인", G1), ("노시환", G1), ("곽빈", "2027시즌 뒤"), ("김주원", "2027시즌 뒤"), ("안우진", "2028\n시즌 뒤"), ("김도영", "2028~29\n시즌 뒤")]
ST = "정리 · 언제 갈 수 있나"
SC.append(fg(ST, SUM, "f139", at0=[1.0, 2.25, 50, 50, 50, 50], posAt=[0.0, 0.0, None, None, None, None], **OG))                                                 # 139
SC.append(lk("winter", 1, title="단, 이번 겨울 변수", t=dict(win=-1, lk=0.3, wait=1.0)))                           # 140
SC.append(fg(ST, SUM[:4], "f141", at0=[-1, -1, 2.0, 2.1], posAt=[-1, -1, 0.0, 0.0], **OG))                                         # 141
SC.append(fg(ST, SUM[:5], "f141", at0=[-1, -1, -1, -1, 2.0], posAt=[-1, -1, -1, -1, 0.0], cont=True, **OG))                           # 142
SC.append(fg(ST, SUM, "f141", at0=[-1, -1, -1, -1, -1, 0.1], posAt=[-1, -1, -1, -1, -1, 1.0], cont=True, **OG))                           # 143
N144 = [st("포스팅 조항", "2026시즌 뒤로 정해짐", 50), st("구단 허락", "이미 계약서에", 50, hi=True)]
SC.append(pv(NH, "노시환", "이번 겨울", [vstamp("먼저 움직일 쪽", 2.0, "gold", size=52)], N144, chain="n144", enterAt=2.0))   # 144
SC.append(pv(NH, "노시환", "이번 겨울", [vstamp("먼저 움직일 쪽", -1, "gold", size=52)], [dict(N144[0], at=1.0), dict(N144[1], at=1.85)], chain="n144"))   # 145
SC.append(pv(G + "원태인_포효_스타뉴스", "원태인", "이번 겨울", [], [st("8월 보도 기준", "메이저리그 에이전트 아직 안 정함", 1.0), st("2026시즌", "7승 9패 · 4.52", 2.0, hi=True)]))   # 146
SC.append(fg("이번 겨울 먼저 사인할 선수는?", [("원태인", ""), ("노시환", "")], "f147", at0=[2.0, 3.0], **FG2))   # 147 (10/25 검수: 이름 전엔 ? 칸)


N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
# 10/24 검수(완급 없음): 훅·나열은 빠르게, 숫자·결론·계산은 천천히(줄 pace slow → ttsTempoSlow)
FAST = {1, 2, 3, 5, 6, 81, 113}   # 10/25 사용자 "맨 처음 대사 너무 빨라" — 0번 줄은 보통 속도
SLOW = {9, 10, 24, 30, 41, 54, 70, 86, 102, 117, 133, 134, 135, 136, 137, 139, 141, 142, 143, 144, 145}
lines, scenes = [], []
# 10/25 사용자(원태인 "이 장면 너무 금방 지나가서 다 읽기도 전에 다음 화면으로 넘어가버려" / "여기도 마찬가지야"):
# 줄 끝에 뜬 글이 다음 장면에서 바로 바뀌면 1초 남짓만 보였다 → 다음 장면을 그 호흡까지 늦게 들인다(enterAt, 앞 장면 유지).
# 값은 1차 검수본의 실제 음성 시각(work/timeline.json, 새 줄은 음절 비례 어림)으로 late_check --timeline 이 '글 한 칸 2.5초 + 10자당 1초, 장면 전체 9자/초' 가 되게 계산한 것(2차 사용자 "시각 자료도 읽을 시간을 충분히 — 나레이션을 멈추라는 건 아니야").
ENTER = {}   # 10/25 04시 사용자 "첫 번째 대사를 할 때 이미 두 번째 이미지가 나와 있어야 나레이션이랑 매치" — 다음 장면을 늦게 들이는 것 전부 뺌, 읽을 시간은 앞 장면 글을 그 문장 안에서 일찍 띄워 확보
if os.environ.get('NO_ENTER') != '1':
    for k_, v_ in ENTER.items(): SC[k_] = dict(SC[k_], enterAt=max(v_, SC[k_].get('enterAt') or 0))
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    if j > 0 and sc.get('chain') and SC[j - 1].get('chain') == sc['chain']: sc['cont'] = True   # 10/25: 같은 묶음 둘째 장면부터 이어받기 표시(rule_check R8)
    l = L(narr_of(t), SUBFIX.get(j, sub_of(t)))
    if j in FAST: l['ttsTempo'] = 1.4
    if j in SLOW: l['pace'] = 'slow'
    lines.append(l); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "규칙", "title": "포스팅 · FA 규칙", "from": 7, "to": 24},
      {"key": "원태인", "title": "원태인 · 이번 겨울 FA", "from": 25, "to": 41},
      {"key": "노시환", "title": "노시환 · 포스팅 조항", "from": 42, "to": 54},
      {"key": "직장폐쇄", "title": "변수 · 직장폐쇄", "from": 55, "to": 71},
      {"key": "곽빈 · 김주원", "title": "곽빈 · 김주원", "from": 72, "to": 86},
      {"key": "김도영 · 안우진", "title": "김도영 · 안우진", "from": 87, "to": 102},
      {"key": "먼저 진출한 선수들", "title": "먼저 진출한 선수들", "from": 103, "to": 117},
      {"key": "이적료", "title": "역대 포스팅 이적료", "from": 118, "to": 142},   # 10/25 이적료 설명 +5줄
      {"key": "정리", "title": "정리", "from": 143, "to": N - 1}]

TAGS = ["다음 메이저리거", "메이저리그 포스팅", "포스팅 자격", "원태인", "원태인 메이저리그", "노시환", "노시환 포스팅", "곽빈", "곽빈 메이저리그", "김주원", "김도영 메이저리그",
        "안우진", "송성문", "김혜성", "고우석", "스즈키 세이야", "포스팅 이적료", "메이저리그 직장폐쇄", "국가대표 포인트", "프로야구", "KBO", "야구자판기"]
DESC = ("▶ 지난 영상: 기아 방출 | 15억 포기하고 친정 돌아온 홍건희, 1년 만에 방출 https://youtu.be/YIE6BXvV4Ew\n\n"
        "이번 겨울 메이저리그 도전이 가능한 대표 KBO 선수는 삼성 원태인과 한화 노시환이에요. 두산 곽빈과 NC 김주원은 빠르면 1년 뒤, 키움 안우진과 기아 김도영은 그보다 더 기다려야 해요. "
        "선수마다 언제 갈 수 있는지 포스팅·FA 규정과 국가대표 포인트, 보도를 바탕으로 정리했어요.\n\n"
        "포스팅: KBO 7시즌(1시즌 = 1군 등록 145일, 풀타임) + 소속 구단 허락, 매년 11월 1일~12월 5일 신청, 메이저리그 사무국이 30개 구단에 알리는 '공시' 뒤 30일 동안 협상. "
        "FA: 구단 허락 없이 해외 구단과 협상(고졸 8시즌). 국가대표 포인트 1점 = 등록일수 1일, 아시안게임 금메달 25포인트(그 대회로 병역 혜택을 받으면 제외).\n\n"
        "원태인: 2019년 데뷔, 2024년 28경기 15승 6패 평균자책점 3.66(곽빈과 공동 다승왕), 올 시즌 뒤 생애 첫 FA. 2024년 12월 포스팅은 신청할 생각이 없고, 2년 더 발전한다면 FA가 되는 해에 도전하고 싶다고 밝힘(요지). 2026년 7승 9패 4.52.\n"
        "노시환: 2023년 31홈런 101타점(홈런왕·타점왕), 2026년 2월 23일 한화와 11년(2027~2037) 옵션 포함 307억 원 계약 + 2026시즌 뒤 포스팅 허용 조항(메이저리그 한정, 복귀 시 한화). 2026년 타율 .283 29홈런 96타점.\n"
        "곽빈·김주원: 2023 항저우 금메달로 병역 해결 → 올해 아시안게임 금메달 25포인트 → 2027시즌 풀타임이면 포스팅 자격. 곽빈 2026년 11승 7패 평균자책점 2.24 탈삼진 197개(2관왕).\n"
        "김도영: 2026년 45홈런 홈런왕, 아시안게임 금메달로 병역 해결(그 대회 포인트 없음), 2025년 부상으로 등록일수 미달 → 계산상 2029시즌 뒤(2028시즌 뒤라는 보도도 있음).\n"
        "안우진: 2027·2028년 풀타임이면 7시즌 → 대부분 2028시즌 뒤(2027시즌 뒤 보도도 있음).\n\n"
        "변수: 구단과 선수노조의 메이저리그 노사협약이 미국 시간 12월 1일 밤(한국 시간 12월 2일) 끝나고, 합의가 없으면 12월 2일부터 직장폐쇄가 가능해요(쟁점: 팀 연봉 총액 상한선인 샐러리캡). "
        "직장폐쇄 중에는 FA·포스팅 계약과 트레이드가 멈춰요. 2021년 직장폐쇄(99일) 때 일본 스즈키 세이야의 포스팅 협상 30일은 멈췄다가 다시 이어졌어요.\n\n"
        "역대 포스팅 이적료(주요 선수): 류현진 2573만 달러 남짓(2012 한화) · 이정후 1882만 5천 달러(2023) · 박병호 1285만 달러(2015) · 김하성 552만 5천 달러(2020) · 강정호 500만 달러 남짓(2014) · 송성문 300만 달러(2025) · 김혜성 250만 달러(2025). "
        "지금은 보장 금액 2500만 달러까지 20%, 5000만 달러까지 17.5%, 그 위 15%.\n\n"
        "이번 겨울 메이저리그 계약서에 먼저 사인할 선수는 원태인일까요, 노시환일까요? 여러분 생각을 댓글로 남겨 주세요.\n\n"
        "기록 출처: 마이데일리(2025/1/23·2026/4/13·6/12·10/19)·MHN(2026/9/30)·스포츠동아(2026/2/25·9/29)·뉴시스(2020/8/18·2021/1/5·2026/2/23)·일간스포츠(2023/8/25·12/16·2024/12/10·2026/9/3·9/28)·스포티비뉴스(2026/9/29·10/8·10/9·10/14)·"
        "경향신문(2020/1/21)·머니투데이(2020/1/10)·데일리안(2026/3/12)·전남일보(2026/10/1)·엑스포츠뉴스(2018/7/12·2024/12/11·2025/12/23·2026/1/28·2/23·5/3·6/12·10/9)·MK스포츠(2018/7/12)·MLB.com·"
        "MLB Trade Rumors(2026/10/7)·스포츠경향(2025/12/23·2026/8/23·8/24·8/31·9/9·9/28·10/11·10/19)·뉴스Q(2026/10/16)·OSEN(2015/1/17·2017/1/20·2021/12/3·2023/12/16·2025/1/4·1/24·12/22·2026/4/13·5/13·8/29·9/3)·"
        "한겨레(2026/2/23)·스타뉴스(2024/12/4·2026/4/13)·미디어펜(2026/2/23)·MAXPORTS(2026/3/6)·파이낸셜뉴스(2026/9/28·9/29)·더팩트(2026/9/24)·연합뉴스·서울신문(2015/11/7·2026/1/5~6)·뉴스핌(2025/12/23·2026/9/2·10/13)·재경일보(2026/10/21)·이투데이(2024/1/4·2026/10/19)·"
        "뉴스1(2025/1/4)·대구신문(2026/10/7)·세계일보(2015/12/3·2026/10/23)·경북매일(2015/12/4)·헤럴드K(2025/12/22)·Korea JoongAng Daily(2012/12/11)·Reuters(2012/12/12)·"
        "NBC San Diego(2021/1/5)·CBS Pittsburgh(2015/1/16)·Chicago Sun-Times(2022/3/20)·CBS Sports(2021/12/8·2022/3/18·2025/3/10)·Field Level Media(2024/4/14)\n"
        "사진 출처: 구단 제공(삼성·한화·두산·NC·기아·LG), 구단 공식 프로필, 연합뉴스·매일경제·스포츠투데이·스포티비뉴스·gettyimages·엑스포츠뉴스·스타뉴스·한겨레·iMBC·스포츠조선(사진 기사), "
        "메이저리그 구단 로고 MLB.com · 썸네일: 동아일보·스포츠투데이·구단 제공")
SOURCE = "사실 출처 = 프로젝트 claude/1024-롱폼29-다음메이저리거-근거모음.md + 대사v4 문서(기사 본문 2곳 이상)."
PINNED = ("이번 겨울 메이저리그 계약서에 먼저 사인할 선수, 원태인일까요 노시환일까요? 👇 댓글로 남겨 주세요!\n"
          "매일 야구 이슈 받아보려면 구독 + 알림 설정 부탁드려요 ⚾")

EP = {"introChapter": "오프닝", "date": "2026-10-24", "gameDate": "2026-10-24", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.15,
      "rev": "1024-long29-v3", "topic": "다음메이저리거", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 9000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼29_메이저리거.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "다음 메이저리거 언제 가? | 원태인·노시환은 이번 겨울, 곽빈·김주원은 1년 뒤 #원태인 #노시환 #메이저리그",
                  "description": DESC, "tags": TAGS, "pinned": PINNED,
                  "hashtags": ["#메이저리그", "#포스팅", "#원태인", "#노시환", "#곽빈", "#김주원", "#김도영", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {0: 0.35, 4: 0.35, 6: 0.5, 7: 0.3, 24: 0.4, 25: 0.35, 41: 0.5, 42: 0.3, 54: 0.5, 55: 0.3, 71: 0.5, 72: 0.3, 86: 0.5, 87: 0.3,
            102: 0.5, 103: 0.3, 117: 0.6, 118: 0.3, 137: 0.5, 138: 0.3, 143: 0.35}
    # 10/25 검수(장면 끝 글이 1~2초만 보이고 넘어감): 문장 끝 쉼을 0.65초까지만 늘린 값(나레이션은 멈추지 않는 자연스러운 숨) — scratchpad gap_solve.py 가 계산
    _gf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gap_fix_1024_long29.json')
    if os.path.exists(_gf):
        for k_, v_ in json.load(open(_gf, encoding='utf-8')).items(): HOLD[int(k_)] = max(HOLD.get(int(k_), 0), v_)
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    # 10/25 검수(자막 윗줄에 한 단어만 '이정후는 / 1억 1300만 달러라'): 한 줄(16자)에 들어가면 한 줄로, 아니면 윗줄 두 단어 이상·숫자와 단위는 안 떼는 자리에서 나눈다
    import re as _re
    _CNT = _re.compile(r'^(구단|명|개|경기|년|월|일|시즌|달러|억|만|천|번|승|패|홈런|타점|포인트|퍼센트|%)')
    def _rewrap(pc):
        if '\n' not in pc: return pc
        top, bot = pc.split('\n', 1)
        if _re.match(r'^[\d.,]', top.strip()): return pc   # 숫자를 쌓아 보여 주는 자막(SUBFIX)은 그대로
        if len(top.split()) >= 2: return pc
        flat = (top + ' ' + bot.replace('\n', ' ')).strip()
        if len(flat) <= 16: return flat
        w = flat.split(' '); best = None
        for k in range(2, len(w)):
            A_, B_ = ' '.join(w[:k]), ' '.join(w[k:])
            d = abs(len(A_) - len(B_)) + (100 if max(len(A_), len(B_)) > 16 else 0) + (30 if (_re.search(r'\d', w[k - 1]) and (_CNT.match(w[k]) or _re.match(r'^\d', w[k]))) else 0)
            if best is None or d < best[0]: best = (d, A_ + '\n' + B_)
        return best[1] if best and best[0] < 30 else pc   # 숫자·단위를 떼야만 나눌 수 있으면 원래대로
    _PF = {'미국 무대에 도전할 만한 선수가 되는 게': '미국 무대에 도전할 만한\n선수가 되는 게'}   # 10/25 검수: 뜻 단위 줄바꿈
    for l in EP['lines']:
        if l.get('sub'): l['sub'] = '|'.join(_PF.get(p_.replace('\n', ' '), _rewrap(p_)) for p_ in l['sub'].split('|'))
    # (10/24 23:35 voiceRemap 은 그 빌드에서 옮기기를 마쳐 뺐다 — 지금 PC 음성 폴더는 v4 줄 번호 그대로)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-24_롱폼.json')
    # 10/25 줄 추가(이적료 설명 +5줄 · 마지막 질문 고침) — 옛 번호 음성을 새 번호로 옮긴다(10/24 실수로그: 줄을 끼우면 voiceRemap 필수). 새로 합성: 131~137, 152
    # (10/25 03시 voiceRemap 은 02:05 빌드에서 옮기기를 마쳐 뺐다 — 지금 PC 음성 폴더는 새 줄 번호 그대로)
    # 10/25 04시: 다음 장면을 늦게 들이지 않는 대신, 읽을 시간이 모자란 글을 그 문장 안에서 조금 일찍 띄운 값(tools/at_solve.py + 눈으로 다듬음)
    _fx = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'at_fix_1024_long29.json')
    if os.path.exists(_fx):
        import at_solve as _AS
        for _j, _m in json.load(open(_fx, encoding='utf-8')).items():
            _R = _AS.refs(EP['scenes'][int(_j)])
            for _k, _v in _m.items():
                _kk = tuple(json.loads(_k))
                if _kk in _R: _d, _f = _R[_kk]; _d[_f] = _v
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
