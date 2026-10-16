# -*- coding: utf-8 -*-
"""10/15 롱폼 「와일드카드 리뷰 + 준플레이오프 KIA vs LG 예측」 (음성 API · 줄별 배속)
대사 = tools/text_1015_long15.py (1차 기사 대조 + 2차 반박 검수 반영).
근거 = KBO 기록실·일정·공식 박스(GetBoxScoreScroll srId=4) 직접 조회 10/15 + 기사 원문 — 프로젝트 claude/1015-롱폼15-가을야구-*.
화면 글은 약어·기호·내부 줄임말 없이. 경기 장면은 diamond(쇼츠 리뷰 장면을 롱폼 템플릿에 주입 — tools/scenes_ps_1015.js)."""
import json, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t15', os.path.join(os.path.dirname(__file__), 'text_1015_long15.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
TEXT = [x[0] for x in _t.LINES] + ['__CTA__']

CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억|(?:^| )다|(?:^| )못|(?:^| )안|(?:^| )만|(?:^| )(?:이번|지난|다음|올|그))$'); BAD_B = re.compile(r'^(건 |것 |수 |때 |중 |구단|달러|일|명|개|경기|원|타수|안타|\d+(?:푼|리)(?![가-힣]*할))')   # 10/16: '2할 4푼 | 7리'·'만 | 34살'·'꾸준했던 | 건'·'열 개 | 구단' 처럼 한 덩어리가 두 줄로 갈라지지 않게
def wrap2(t):
    w = wrap(t)
    if '\n' not in w: return w
    a, b = w.split('\n', 1)
    if not (BAD_A.search(a) or BAD_B.match(b)): return w
    best, bs = None, 1e9
    for m in re.finditer(' ', t):
        x, y = t[:m.start()], t[m.start() + 1:]
        if BAD_A.search(x) or BAD_B.match(y) or max(len(x), len(y)) > 16: continue
        sc = abs(len(x) - len(y))
        if sc < bs: best, bs = x + '\n' + y, sc
    return best or w
def L(narr, sub):
    a, b = narr.split(' / '), sub.split(' / ')
    assert len(a) == len(b), (narr, sub)
    out = []
    for p in b:
        t = re.sub(r' +', ' ', re.sub(r'(?<!\d),\s*|,(?!\d)', ' ', p)).strip()   # 10/15 사용자: 질문 자막에도 물음표
        out.append(t if '\n' in t else wrap2(t))
    return {"narr": narr, "sub": "|".join(out)}

# ── 나레이션 숫자 읽기 ──
DIG = '영일이삼사오육칠팔구'
def sino(n):
    n = int(n)
    if n == 0: return '영'
    out = ''
    for v, u in ((10000, '만'), (1000, '천'), (100, '백'), (10, '십')):
        q, n = divmod(n, v)
        if q: out += ('' if q == 1 else DIG[q]) + u
    return out + (DIG[n] if n else '')
NAT = {1: '한', 2: '두', 3: '세', 4: '네', 5: '다섯', 6: '여섯', 7: '일곱', 8: '여덟', 9: '아홉', 10: '열', 11: '열한', 12: '열두', 13: '열세', 14: '열네', 15: '열다섯', 16: '열여섯', 17: '열일곱', 18: '열여덟', 19: '열아홉'}
def native(n): n = int(n); return NAT.get(n) or sino(n)
def narr_of(t):
    t = t.replace('2만 3,650석', '이만 삼천육백오십 석')
    t = re.sub(r'(\d+)\.(\d+)', lambda m: sino(m.group(1)) + '쩜' + ''.join('공' if c == '0' else DIG[int(c)] for c in m.group(2)), t)   # 10/15 사용자: 4.24 = 사쩜이사(사 점 이사 ✗), 소수 0 은 공   # 평균자책점 4.24 → 사 점 이사
    for a, b in (('2대0', '이 대 영'), ('2대1', '이 대 일'), ('4대1', '사 대 일')): t = t.replace(a, b)
    t = t.replace('1사', '원 아웃').replace('2사', '투 아웃')
    t = re.sub(r'([0-3])(스트라이크|볼)', lambda m: ['노','원','투','쓰리'][int(m.group(1))] + ' ' + m.group(2), t)   # 10/15 사용자: 2스트라이크 = 투 스트라이크(볼카운트는 영어 수사)
    t = re.sub(r'(\d)·(\d)·(\d)차전', lambda m: f'{sino(m.group(1))} {sino(m.group(2))} {sino(m.group(3))} 차전', t)
    t = re.sub(r'(\d)·(\d)(차전|루)', lambda m: f'{sino(m.group(1))} {sino(m.group(2))} {m.group(3)}', t)
    t = re.sub(r'(\d+)번 타자', lambda m: sino(m.group(1)) + ' 번 타자', t)
    t = re.sub(r'(\d+)년', lambda m: sino(m.group(1)) + ' 년', t)
    t = re.sub(r'(\d+)월', lambda m: sino(m.group(1)) + ' 월', t)
    t = re.sub(r'(\d+)일', lambda m: sino(m.group(1)) + ' 일', t)
    t = re.sub(r'(\d+)(승|무|패|위|이닝|회말|회초|회|연승|연패|차전|루|할|푼|리|타수|안타|홈런|타점|세이브|킬로|분의|대|실점)', lambda m: sino(m.group(1)) + ' ' + m.group(2), t)
    t = re.sub(r'(\d+)점', lambda m: sino(m.group(1)) + ' 점', t)
    t = re.sub(r'(\d+)(경기|번|명|개|가지)', lambda m: (native(m.group(1)) if (m.group(2) in ('경기', '가지') or int(m.group(1)) < 20) else sino(m.group(1))) + ' ' + m.group(2), t)
    t = re.sub(r'(\d+)과 ', lambda m: sino(m.group(1)) + '과 ', t)
    t = t.replace('·', ' ')
    for en, ko in (("KIA", "기아"), ("SSG", "에스에스지"), ("LG", "엘지"), ("KT", "케이티"), ("NC", "엔씨")):
        t = re.sub(r'(?<![A-Za-z])' + en + r'(?![A-Za-z])', ko, t)
    t = re.sub(r'(\d+)', lambda m: sino(m.group(1)), t)
    t = re.sub(r' +', ' ', t).strip()
    return ' / '.join(re.sub(r'^이 (위|승|점)', r'이\1', b) for b in t.split(' / '))
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))   # 10/15: '+'(이어 읽기)·구간 끝 '.'(한 박자 쉼)은 나레이션에만

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vduo(items, **k): return dict(type="duo", items=items, **k)
def vstreak(n, at=0, c="good", **k): return dict(type="streak", n=n, at=at, c=c, **k)
RED, GOLD, GRAY, GREEN, NAVY = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55", "#3B4A63"
KIAC, LGC = "#C70125", "#C30452"
LGB = "#2563EB"   # 10/15 사용자: KIA·LG 가 같은 빨강으로 보임 → KIA 와 맞붙는 장면에서 LG 는 파랑
TCKL = {"LG": LGB}

C = '카드/'
P = {
    # 10/15 새로 자른 카드(tools/person_card.py 0.774) — P15_*
    "오스틴_WC": C + "P15_오스틴_WC", "곽빈_WC": C + "P15_곽빈_WC", "카라스코_WC": C + "P15_카라스코_WC", "박해민_WC": C + "P15_박해민_WC",
    "신민재": C + "P15_신민재", "전상현": C + "P15_전상현", "문정빈": C + "P15_문정빈", "오지환": C + "P15_오지환",
    "홍창기": "경기/홍창기_뉴스엔_상체", "문보경": C + "문보경_LG홈런카드", "염경엽_B": C + "P15_염경엽_더그아웃", "유영찬": C + "P15_유영찬",
    "박재현": C + "P15_박재현", "양현종": C + "FA10_양현종", "올러_B": C + "P15_올러_포효",
    "오스틴_WC원본": "경기/오스틴_WC세리머니_1014_LG제공", "박해민_캐치": "경기/박해민_펜스캐치_LG제공",
    # 이미 있는 카드
    "김도영_A": C + "김도영_MVP_43호", "김도영_B": C + "R13_김도영", "오스틴_A": C + "오스틴_MVP_포효", "오스틴_B": C + "오스틴_MVP_하트",
    "톨허스트_A": C + "FA9P_톨허스트", "톨허스트_B": C + "FA9_톨허스트_상체", "네일_A": C + "FA9_네일_역투", "올러_A": C + "FA9_올러_경기",
    "임찬규": C + "R13_임찬규_투구", "카라스코": C + "FA9_카라스코", "곽빈": C + "곽빈_MVP_포효", "염경엽_A": C + "FA9_염경엽",
    "박해민": C + "FA10_박해민", "손주영": C + "R13_손주영_포효", "케네디": C + "R13_케네디_2026LG", "카스트로": C + "FA9_카스트로_홈런",
}
JAMSIL = "상황별/잠실_WC관중_1014_LG제공"
def pv(i, img, name, sub, viz, **k): return S(i, "pstat", img=P.get(img, img), name=name, sub=sub, stats=k.pop("stats", []), viz=viz, noCenter=True, **k)   # 10/15: 사진 크기·자리 고정
def pvt(i, team, sub, viz, **k): return S(i, "pstat", team=team, name=team, sub=sub, stats=k.pop("stats", []), viz=viz, noCenter=True, **k)
def sp(i, img, name, sub, bubbles, **k): return S(i, "speech", img=P.get(img, img), name=name, sub=sub, bubbles=bubbles, **k)
def ppl(i, items, **k): return S(i, "people", full=True, items=items, **k)
def pc(img, name, note="", **x): return dict({"img": P.get(img, img), "name": name, "note": note}, **x)
def card(team, img, label): return {"team": team, "img": P.get(img, img), "label": label}
AS = "2026 정규시즌 최종"

# ── 와일드카드 다이아몬드 ──
WC = dict(away="두산", home="LG")
def dm(i, title, bat, score, outs, steps, **k):
    return S(i, "diamond", title=title, bat=bat, batIdx=(1 if bat == "LG" else 0), score=score, outs=outs, steps=steps, **WC, **k)

SC = {}
# 훅
SC[0] = S(0, "matchup", left="KIA", right="LG", score="VS")   # 10/15 사용자: 카드 없이 로고만, VS 크게
SC[1] = S(0, "photo", img=P["오스틴_WC원본"], fit="cover", text="", h=760)
_G16 = [dict(t=d, bad=(w == 'K'), hi=(w == 'L'), c=("#2563EB" if w == 'L' else None), at=0.3 + j * 0.08, fs=30) for j, (d, w) in enumerate(
    [("3/31", "K"), ("4/1", "L"), ("4/2", "L"), ("5/19", "K"), ("5/21", "L"), ("5/29", "L"), ("5/30", "L"), ("5/31", "L"), ("6/16", "L"),
     ("6/17", "K"), ("6/18", "K"), ("9/26", "K"), ("10/3", "K"), ("10/4", "K"), ("10/5", "K"), ("10/12", "K")])]
def g16(at_last=0.3, **k):
    its = [dict(x) for x in _G16]
    for x in its[9:]: x["at"] = at_last
    return S(0, "cells", title="2026 KIA vs LG · 맞대결 16경기", cols=8, cw=170, ch=96, items=its, label="빨강 = KIA 승리 · 파랑 = LG 승리", chain="g16", **k)
_GS = [(d, w) for d, w in [("3/31", "K"), ("4/1", "L"), ("4/2", "L"), ("5/19", "K"), ("5/21", "L"), ("5/29", "L"), ("5/30", "L"), ("5/31", "L"), ("6/16", "L"),
     ("6/17", "K"), ("6/18", "K"), ("9/26", "K"), ("10/3", "K"), ("10/4", "K"), ("10/5", "K"), ("10/12", "K")]]
GS_T = "2026 KIA vs LG · 맞대결 16경기"
G_LG = {"from": 0, "to": 8, "label": "6월 16일까지 · LG 7승 2패", "team": "LG"}
G_KIA = {"from": 9, "to": 15, "label": "6월 17일부터 · KIA 7연승", "team": "KIA"}
def gs(**k): return S(0, "gamestrip", tc=TCKL, title=GS_T, teams={"K": "KIA", "L": "LG"}, games=[list(x) for x in _GS], rows=[[0, 8], [9, 15]], chain="g16", **k)   # 10/15 사용자: 날짜 칸 색 구분(범례 글) 대신 경기마다 이긴 팀 로고
SC[2] = gs(at=0.2, step=0.04, dimTo=9, groups=[dict(G_KIA, label="KIA 7연승 · LG 7연패", at=1)])
SC[3] = S(0, "tiles", title="2016년 10월 11일 와일드카드", items=[{"team": "LG", "v": "준플레이오프\n진출", "at": 1}, {"team": "KIA", "v": "탈락", "color": NAVY, "dim": True, "at": 1.4}])   # 10/15 사용자: 날짜는 제목으로, 점수 빼고, KIA 옅은 회색
SC[4] = S(0, "toc", on=-1, itemFrom=99)
# 1장 와일드카드
SC[5] = S(0, "wcrule", title="10월 14일 잠실 · 와일드카드 결정전", teams=[{"team": "LG", "rank": "정규시즌 4위", "need": 2, "have": 1, "goal": "1승만 더 하면 통과", "at": 1}, {"team": "두산", "rank": "정규시즌 5위", "need": 2, "have": 0, "goal": "2승 해야 통과", "at": 2}], slotAt=2, advAt=3, advLabel="4위 혜택 · 1승 안고 시작", goalAt=4)   # 10/15 사용자: 글 카드 → 통과에 필요한 승리 칸
SC[6] = S(0, "duel", left={"img": P["카라스코_WC"], "name": "카라스코", "team": "LG", "role": "LG 선발", "at": 0}, right={"img": P["곽빈_WC"], "name": "곽빈", "team": "두산", "role": "두산 선발", "at": 1}, vsAt=0.6)   # 10/15 사용자: 카드 없이 사진 그대로
SC[7] = S(0, "photo", img=JAMSIL, fit="cover", text="", h=760)
SC[8] = dm(0, "1회말 · LG 공격", "LG", [0, 0], 0, [dict(at=1, who="홍창기", bases=["홍창기", None, None], outs=0, label="홍창기 몸에 맞는 공"),
                                                dict(at=2, who="박해민", bases=["박해민", None, None], out=["홍창기"], outs=1, label="박해민 1루 땅볼 · 2루 아웃")], chain="d1")
SC[9] = dm(0, "1회말 · LG 공격", "LG", [0, 0], 0, [dict(at=-1, who="박해민", bases=["박해민", None, None], outs=1),
                                                dict(at=1.4, who="오스틴", hr=True, runs=2, bases=[None, None, None], outs=1, label="오스틴 2점 홈런")], chain="d1", cont=True)
SC[10] = pv(0, "오스틴_B", "오스틴", "LG 지명타자 · 10월 14일", [vstamp("결승타", 1, "gold")], stats=[st("1회", "2점 홈런", 0, hi=True), st("이날 최우수 선수", "데일리 MVP", 1)])
SC[11] = dm(0, "2회말 · LG 공격", "LG", [0, 2], 0, [dict(at=1, who="구본혁", bases=[None, "구본혁", None], outs=0, label="구본혁 2루타"),
                                                 dict(at=2, who="박동원", bases=["박동원", "구본혁", None], outs=0, label="박동원 볼넷"),
                                                 dict(at=3, who="신민재", bases=["신민재", "박동원", "구본혁"], outs=0, label="번트 · 3루수 송구 실책")], chain="d2")
SC[12] = dm(0, "2회말 · LG 공격", "LG", [0, 2], 0, [dict(at=-1, who="신민재", bases=["신민재", "박동원", "구본혁"], outs=0),
                                                 dict(at=0, who="홍창기", bases=["신민재", "박동원", "구본혁"], outs=1, label="홍창기 삼진"),
                                                 dict(at=0.6, who="박해민", bases=["신민재", "박동원", "구본혁"], outs=2, label="박해민 삼진"),
                                                 dict(at=1.2, who="오스틴", bases=[None, None, None], outs=3, label="오스틴 삼진 · 무사 만루 무득점")], chain="d2", cont=True)
SC[13] = S(0, "speedgun", title="2회 무사 만루 · 곽빈의 삼진", pitcher={"img": P["곽빈_WC"], "name": "곽빈", "team": "두산", "role": "두산 선발"}, items=[{"vs": "박해민", "team": "LG", "v": 157, "at": 0, "res": "삼진", "resAt": 2}, {"vs": "오스틴", "team": "LG", "v": 158, "at": 1, "res": "삼진", "resAt": 2}], unit="킬로")
SC[14] = pv(0, "곽빈_WC", "곽빈", "두산 선발 · 10월 14일", [vstamp("와일드카드 한 경기 최다 탈삼진 타이", 1, "gold", size=50)], stats=[st("6이닝", "3피안타 2실점", 0), st("삼진", "10개", 0, hi=True)])
SC[15] = pv(0, "카라스코_WC", "카라스코", "LG 선발 · 10월 14일", [vsteps([stp("1회", "안타 1", 1), stp("2회", "안타 1", 1.2), stp("3~6회", "안타 0", 2, c="good")])],
            stats=[st("나흘 쉬고", "6이닝 1실점", 0, hi=True)])
SC[16] = dm(0, "7회초 · 두산 공격", "두산", [0, 2], 0, [dict(at=1, who="세베리노", bases=["세베리노", None, None], outs=0, label="세베리노 안타"),
                                                   dict(at=2, who="양의지", bases=[None, "양의지", "세베리노"], outs=0, label="양의지 2루타 · 무사 2·3루")], chain="d7")
SC[17] = dm(0, "7회초 · 두산 공격", "두산", [0, 2], 0, [dict(at=-1, who="양의지", bases=[None, "양의지", "세베리노"], outs=0),
                                                   dict(at=2, who="김민석", bases=[None, "양의지", "세베리노"], outs=1, label="케네디 · 김민석 삼진"),
                                                   dict(at=3, who="강승호", bases=["강승호", "양의지", "세베리노"], outs=1, label="강승호 몸에 맞는 공 · 1사 만루")], chain="d7", cont=True)
SC[18] = dm(0, "7회초 · 두산 공격", "두산", [0, 2], 1, [dict(at=-1, who="강승호", bases=["강승호", "양의지", "세베리노"], outs=1),
                                                   dict(at=0, who="양석환", bases=["강승호", "양의지", "세베리노"], outs=1, label="대타 양석환 · 우중간 깊은 타구")], chain="d7", cont=True)
SC[19] = S(0, "photo", img=P["박해민_캐치"], fit="cover", text="", h=760)
SC[20] = sp(0, "박해민_WC", "박해민", "LG 중견수", [bb("10월 14일 경기 뒤", "“2스트라이크 후에는\n원래 위치에서 한 두 걸음\n오른쪽으로 가 있었던 게 주효했다”", 1)])
SC[21] = dm(0, "7회말 · LG 공격", "LG", [1, 2], 2, [dict(at=0, bases=["문정빈", "박해민", "신민재"], outs=2, label="2사 만루"), dict(at=1, who="문보경", bases=[None, None, None], outs=3, label="문보경 유격수 땅볼")], lead="2사 만루")  # 10/15 검수: 주자 표시 누락 → KBO 박스(신민재 좌안·박해민 중안·문정빈 4구)
SC[22] = dm(0, "8회초 · 두산 공격", "두산", [1, 2], 1, [dict(at=0, who="안재석", bases=["안재석", "조수행", None], outs=1, label="1사 1·2루"),
                                                   dict(at=2, who="세베리노", bases=["안재석", "조수행", None], outs=2, label="이우찬 · 세베리노 삼진"),
                                                   dict(at=3, who="류승민", bases=[None, None, None], outs=3, label="류승민 삼진")])
SC[23] = dm(0, "8회말 · LG 공격", "LG", [1, 2], 0, [dict(at=1, who="송찬의", bases=["송찬의", None, None], outs=0, label="송찬의 안타"),
                                                 dict(at=2, who="구본혁", bases=[None, "송찬의", None], outs=1, label="구본혁 희생번트"),
                                                 dict(at=3, who="박동원", bases=["박동원", None, "송찬의"], outs=1, label="박동원 안타 · 1사 1·3루")], chain="d8")
SC[24] = dm(0, "8회말 · LG 공격", "LG", [1, 2], 1, [dict(at=-1, who="박동원", bases=["박동원", None, "최원영"], outs=1),
                                                 dict(at=0.4, who="신민재", bases=["신민재", "박동원", None], scored=["최원영"], runs=1, outs=1, label="신민재 번트 안타 · 1점")], chain="d8", cont=True)
SC[25] = dm(0, "8회말 · LG 공격", "LG", [1, 3], 2, [dict(at=-1, who="신민재", bases=["이영빈", "박동원", None], outs=2),
                                                 dict(at=1, who="박해민", bases=["박해민", "이영빈", "박동원"], outs=2, label="이영하 폭투 · 박해민 볼넷"),
                                                 dict(at=2, who="박해민", bases=["박해민", None, "이영빈"], scored=["박동원"], runs=1, outs=2, label="또 폭투 · 박동원 홈인")], chain="d8", cont=True)
SC[26] = S(0, "scoreboard", title="10월 14일 잠실 · 와일드카드 결정전", rows=[{"team": "두산", "runs": [0, 0, 0, 0, 0, 0, 1, 0, 0], "r": 1},
                                                               {"team": "LG", "runs": [2, 0, 0, 0, 0, 0, 0, 2, "X"], "r": 4, "hi": True}],
           hi=[1, 8], label="LG 준플레이오프 진출", labelAt=1)
SC[27] = pv(0, "톨허스트_B", "톨허스트", "LG 선발 · 준플레이오프 1차전", [vsteps([stp("10월 10일", "롯데전 등판", 1), stp("11~16일", "엿새 휴식", 2, c="good"), stp("10월 17일", "1차전", 3, c="gold")])])
SC[28] = pv(0, "신민재", "신민재", "LG 2루수", [vstamp("준플레이오프 출전 쉽지 않아", 3, "bad", size=52)], stats=[st("8회", "스퀴즈 번트 안타", 1), st("교체", "왼쪽 햄스트링", 2, hi=True)])
# 2장
SC[29] = S(0, "matchup", left="KIA", right="LG", score="9 : 7", text="KIA 9승 7패")
SC[30] = gs(at=0.2, step=0.05, hideFrom=9, groups=[dict(G_LG, at=2)])
SC[31] = gs(at=0, step=0.08, cont=True, groups=[dict(G_LG, at=-1), dict(G_KIA, at=1, sub="그중 6경기 2점 차 이내", subAt=2.5)])
SC[32] = S(0, "photo", img="경기/김도영_45호_타격_1012_KIA제공", fit="cover", text="", h=760)
SC[33] = pv(0, "김도영_A", "김도영", "KIA 3루수", [vsteps([stp("10월 5일 잠실", "9회 2사 · 역전 3점 홈런", 0, c="gold"), stp("10월 12일 광주", "8회 · 결승 2점 홈런", 2, c="gold")])])
SC[34] = sp(0, "염경엽_A", "염경엽", "LG 감독 · 10월 14일", [bb("", "“결정적일 때마다\n김도영에게 맞았다”", 1), bb("", "“초점은 김도영을\n어떻게 막는지다”", 2.5)])
SC[35] = pv(0, "김도영_B", "김도영", "KIA 3루수", [vtrend([dict(x="정규시즌", v=308, vt="3할 8리", at=0), dict(x="LG전", v=208, vt="2할 8리", c="bad", at=1)], title="타율")],
            stats=[st("LG전", "48타수 10안타", 2, hi=True)])
SC[36] = pv(0, "김도영_B", "김도영", "KIA 3루수", [vduo([dict(icon="ball", v="4개", k="LG전 홈런", at=0, c="bad"), dict(icon="person", v="12개", k="LG전 볼넷", at=1)])],
            stats=[st("LG전", "48타수 10안타", 0, hi=True)])
SC[37] = pv(0, "오스틴_B", "오스틴", "LG 1루수 · 41홈런", [vtrend([dict(x="정규시즌", v=331, vt="3할 3푼 1리", at=0), dict(x="KIA전", v=228, vt="2할 2푼 8리", c="bad", at=2)], title="타율")],
            stats=[st("KIA전 홈런", "4개", 3, hi=True)])
SC[38] = S(0, "faceoff", tc=TCKL, title="두 간판의 상대 전적", left={"img": P["김도영_A"], "name": "김도영", "team": "KIA", "role": "LG전"}, right={"img": P["오스틴_A"], "name": "오스틴", "team": "LG", "role": "KIA전"}, rows=[dict(k="상대 팀\n타율", l="2할 8리", r="2할 2푼 8리", lv=.208, rv=.228, at=0), dict(k="상대 팀\n홈런", l="4개", r="4개", lv=4, rv=4, at=1), dict(k="상대 팀\n타점", l="12개", r="8개", lv=12, rv=8, at=2.5)])
SC[39] = sp(0, "염경엽_B", "염경엽", "LG 감독 · 10월 14일", [bb("", "“홍창기가 출루하고\n문보경이 찬스에서 해결”", 3), bb("", "“그래야 우리 팀\n득점력이 올라간다”", 5)])   # 뉴스엔 10/14 22:57 안형준 — 왜 두 선수인지(사용자 10/15)
SC[40] = pv(0, "홍창기", "홍창기", "LG 외야수", [vtrend([dict(x="정규시즌", v=239, vt="2할 3푼 9리", at=0), dict(x="9월 이후", v=143, vt="1할 4푼 3리", c="bad", at=1), dict(x="KIA전", v=188, vt="1할 8푼 8리", c="bad", at=3)], title="타율")])
SC[41] = S(0, "pgroup", title="LG · KIA전에 강했던 타자", items=[dict(img=P["문보경"], name="문보경", team="LG", k="KIA전 타율", v="3할 1푼 3리", at=0), dict(img=P["문정빈"], name="문정빈", team="LG", k="KIA전 타율", v="3할 1푼 3리", at=0.5)], vAt=1.5)
# 3장 선발
SC[42] = pv(0, "톨허스트_A", "톨허스트", "LG 선발 · 1차전", [vstamp("1차전 선발", 2, "gold")])   # 10/15 사용자: 나레이션이 톨허스트인데 화면이 목차 → 톨허스트
SC[43] = pv(0, "톨허스트_A", "톨허스트", "LG 선발 · 1차전", [], stats=[st("2026 정규시즌", "12승 11패", 0), st("평균자책점", "4.24", 1, hi=True), st("이닝", "163과 3분의 1", 1)])
SC[44] = pv(0, "톨허스트_A", "톨허스트", "LG 선발 · 1차전", [vtrend([dict(x="정규시즌", v=4.24, vt="4.24", at=0), dict(x="KIA전", v=6.20, vt="6.20", c="bad", at=0)], title="평균자책점")],
            stats=[st("KIA전 피안타율", "3할 7리", 1, hi=True)])
SC[45] = pv(0, "톨허스트_A", "톨허스트", "LG 선발 · 1차전", [vsteps([stp("3월 31일", "3이닝 7실점", 0, c="bad"), stp("5월 19일", "1회 퇴장", 1, c="bad"), stp("5월 31일", "6이닝 1실점", 2, c="good"), stp("6월 18일", "6이닝 3실점", 2.3), stp("10월 5일", "5이닝 2실점", 2.6)])], stats=[st("나머지 3경기", "17이닝 6실점", 3, hi=True)])
SC[46] = pv(0, "네일_A", "네일", "KIA 선발 · 1차전 가능성 높음", [], stats=[st("2026 정규시즌", "13승 7패", 2), st("평균자책점", "3.49", 2.5), st("183이닝", "리그 1위", 3, hi=True)])
SC[47] = pv(0, "네일_A", "네일", "KIA 선발 · 1차전 가능성 높음", [vtrend([dict(x="정규시즌", v=3.49, vt="3.49", at=0), dict(x="9월 이후", v=2.76, vt="2.76", c="good", at=0)], title="평균자책점")])
SC[48] = pv(0, "네일_A", "네일", "KIA 선발 · 1차전 가능성 높음", [vtrend([dict(x="정규시즌", v=3.49, vt="3.49", at=0), dict(x="9월 이후", v=2.76, vt="2.76", c="good", at=0), dict(x="LG전", v=4.58, vt="4.58", c="bad", at=1)], title="평균자책점")])
SC[49] = S(0, "faceoff", tc=TCKL, title="1차전 선발 · 평균자책점(낮을수록 좋음)", left={"img": P["톨허스트_B"], "name": "톨허스트", "team": "LG", "role": "LG 선발"}, right={"img": P["네일_A"], "name": "네일", "team": "KIA", "role": "KIA 선발"}, rows=[dict(k="9월 이후", l="3.60", r="2.76", lv=3.60, rv=2.76, low=True, at=1), dict(k="맞대결 상대로", l="6.20", r="4.58", lv=6.20, rv=4.58, low=True, at=1.5)])
SC[50] = S(0, "pgroup", title="네일이 조심할 타자", items=[dict(img=P["문정빈"], name="문정빈", team="LG", k="네일 상대", v="8타수 5안타", at=0, vAt=2), dict(img=P["문보경"], name="문보경", team="LG", k="네일 상대", v="3타수 3안타", at=0.6, vAt=3)])
SC[51] = pv(0, "올러_A", "올러", "KIA 선발 · 2차전", [vsteps([stp("3월 31일", "6이닝 0실점", 2, c="good"), stp("5월 19일", "6이닝 0실점", 2.2, c="good"), stp("5월 30일", "6이닝 3실점", 2.4), stp("6월 17일", "6이닝 1실점", 2.6), stp("10월 5일", "6이닝 4실점", 4, c="bad")])],
            stats=[st("LG전 평균자책점", "2.40", 2, hi=True), st("피안타율", "1할 9푼 8리", 3)])
SC[52] = pv(0, "올러_B", "올러", "KIA 선발 · 광주", [vtrend([dict(x="정규시즌", v=3.13, vt="3.13", at=0), dict(x="광주", v=2.28, vt="2.28", c="good", at=1)], title="평균자책점")],
            stats=[st("광주 피안타율", "1할 7푼 9리", 2, hi=True)])
def ab(i, L, R, total, groups, **k): return S(i, "abdots", left=L, right=R, total=total, groups=groups, **k)
OL = {"img": P["올러_A"], "name": "올러", "team": "KIA", "role": "KIA 투수"}
TH = {"img": P["톨허스트_B"], "name": "톨허스트", "team": "LG", "role": "LG 투수"}
SC[53] = ab(0, OL, {"img": P["홍창기"], "name": "홍창기", "team": "LG", "role": "LG 외야수"}, "10타수 1안타", [dict(k="H", n=1, at=2), dict(k="O", n=5, at=2, to="K", toAt=3), dict(k="O", n=4, at=2)], totalAt=2, chips=[dict(label="볼넷 5개", at=1, c="#16A34A")], cols=5)
SC[54] = ab(0, OL, {"img": P["오스틴_A"], "name": "오스틴", "team": "LG", "role": "LG 1루수"}, "12타수 2안타", [dict(k="H", n=1, at=1, to="HR", toAt=2), dict(k="H", n=1, at=1), dict(k="O", n=10, at=1)], totalAt=1, cols=6, cont=True)
SC[55] = pv(0, "임찬규", "임찬규", "LG 2차전 후보", [], stats=[st("2026 정규시즌", "15승 7패", 2), st("KIA전 평균자책점", "6.23", 4, hi=True)])
SC[56] = pv(0, "양현종", "양현종", "KIA 선발", [vduo([dict(icon="ball", v="2할 6리", k="LG전 피안타율", at=1, c="good"), dict(icon="person", v="15개", k="LG전 볼넷", at=4, c="bad")])],
            stats=[st("LG전", "4경기 18과 3분의 2이닝", 0)])
SC[57] = S(0, "pgroup", title="톨허스트에게 강했던 KIA 타자", items=[dict(img=P["박재현"], name="박재현", team="KIA", k="톨허스트 상대", v="10타수 4안타", at=0, vAt=2), dict(img=P["카스트로"], name="카스트로", team="KIA", k="톨허스트 상대", v="7타수 3안타", at=3, vAt=3)])
SC[58] = ab(0, TH, {"img": P["김도영_B"], "name": "김도영", "team": "KIA", "role": "KIA 3루수"}, "9타수 2안타", [dict(k="H", n=1, at=1, to="HR", toAt=2), dict(k="H", n=1, at=1), dict(k="O", n=7, at=1)], totalAt=1, cols=5)
# 4장 뒷문
SC[59] = S(0, "toc", on=3)
SC[60] = pv(0, "전상현", "전상현", "KIA 마무리", [vstamp("10월 피안타 0", 5, "gold")], stats=[st("블론세이브", "KIA 22 · LG 22", 0, hi=True), st("10월", "6경기 8과 3분의 2이닝", 4)])
SC[61] = ab(0, {"img": P["전상현"], "name": "전상현", "team": "KIA", "role": "KIA 마무리"}, {"team": "LG", "name": "LG 타자 11명", "role": "오스틴 · 문보경 등"}, "21타수 1안타", [dict(k="O", n=4, at=2), dict(k="H", n=1, at=2), dict(k="O", n=16, at=2)], totalAt=2, cols=7)
SC[62] = pv(0, "손주영", "손주영", "LG 마무리", [vstamp("준플레이오프 합류 미정", 3, "bad", size=54)], stats=[st("선발 → 마무리", "31세이브", 1, hi=True), st("부상", "목", 2)])
SC[63] = pv(0, "유영찬", "유영찬", "LG 투수", [vstamp("시즌 아웃", 1, "bad")], stats=[st("수술", "팔꿈치", 0)])
SC[64] = S(0, "relay", title="와일드카드 · LG 불펜 이어 던지기", team="LG", inn=[7, 8, 9], pitchers=[dict(name="케네디", outs=3, at=1), dict(name="김진수", outs=1, at=1.25), dict(name="이우찬", outs=2, at=1.5), dict(name="김강률", outs=3, at=1.75)], brace=dict(label="네 명이 3이닝", at=2), note=dict(inn=0, label="희생플라이 1점 → 카라스코 실점", at=3), text="다섯 경기도 버틸까?", textAt=5, size=60)
SC[65] = S(0, "bars", term="팀 평균자책점", title="선발 + 불펜 · 낮을수록 좋음", items=[dict(label="KIA", team="KIA", value=4.27, unit="", sub="3위", at=1, hi=True), dict(label="LG", team="LG", value=4.81, unit="", sub="7위", at=2, color=GRAY)], max=6, asof=AS)
SC[66] = S(0, "rundiff", title="득점 − 실점 · 2026 정규시즌", rows=[dict(team="KIA", rs=769, ra=664, at=1), dict(team="LG", rs=723, ra=726, at=2)], max=800, asof=AS)
SC[67] = S(0, "ring10", tc=TCKL, title="정규시즌 마지막 10경기", items=[dict(team="KIA", w=7, l=3, at=1), dict(team="LG", w=3, l=7, at=2)])
SC[68] = pvt(0, "KIA", "KIA 타이거즈", [vsteps([stp("10월 12일", "최종전", 0), stp("13~16일", "나흘 휴식", 1, c="gold"), stp("10월 17일", "1차전", 1.5)])], stats=[st("변수", "실전 감각", 2, hi=True)])
SC[69] = pv(0, "오지환", "오지환", "LG 유격수", [vstamp("준플레이오프 출전 미정", 4, "bad", size=54)], stats=[st("10월 5일", "왼쪽 무릎 부상", 2, hi=True), st("와일드카드", "결장", 3)])
SC[70] = S(0, "big", team="LG", text="LG에게도\n희망은 있다", size=120)
SC[71] = S(0, "cells", title="KIA 준플레이오프 · 해태 시절 포함", cols=4, cw=300, ch=140, items=[dict(t="1994", bad=True, at=1), dict(t="2004", bad=True, at=1.3), dict(t="2006", bad=True, at=1.6), dict(t="2011", bad=True, at=1.9)],
           label="네 번 모두 탈락 · 통산 2승 9패", text="마지막 탈락은 2011년", textAt=4)
SC[72] = S(0, "cells", title="와일드카드 거친 팀 · 준플레이오프", cols=6, cw=210, ch=96, items=[dict(t=str(y), hi=(y in (2016, 2017, 2018, 2021, 2023, 2025)), at=1.5 + 0.1 * k, fs=34) for k, y in enumerate(range(2015, 2026))],
           label="11번 중 6번 통과")
SC[73] = pvt(0, "LG", "2025년 한국시리즈 우승", [vstamp("디펜딩 챔피언", 1, "gold")], stats=[st("와일드카드", "한 경기 통과", 2, hi=True)])
# 5장
SC[74] = S(0, "toc", on=4)
_CMP = [dict(k="상대 전적", l="7승", r="9승 · 7연승", w="r"), dict(k="1·2차전 선발", l="톨허스트", r="네일 · 올러", w="r"), dict(k="뒷문", l="마무리 합류 미정", r="전상현 무피안타", w="r"),
        dict(k="광주 맞대결", l="2승", r="5승", w="r"), dict(k="변수", l="우승 경험 · 기세", r="나흘 실전 공백", w="l")]
def cmp(i, n, **k):
    rows = [dict(k=r["k"], l=r["l"], r=r["r"], w=r["w"], at=(0 if j < n - 1 else 0.3), hide=j >= n) for j, r in enumerate(_CMP)]
    return S(i, "faceoff", title="준플레이오프 · 다섯 가지로 비교", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, rows=rows, chain="cmp", pw=260, **k)
SC[75] = cmp(0, 1)
SC[76] = cmp(0, 2, cont=True)
SC[77] = cmp(0, 3, cont=True)
SC[78] = cmp(0, 4, cont=True)
SC[79] = cmp(0, 5, cont=True)
SC[80] = S(0, "matchup", left="KIA", right="LG", score="3 : 1", tag="야구자판기 예상", text="KIA 3승 1패", size=96)
def g5(**k): return dict(**k)
SER81 = [g5(n="1차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="2차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="3차전", venue="잠실", home="LG", win="?", at=0, glow="LG", glowAt=0),
         g5(n="4차전", venue="잠실", home="LG", win="?", at=0, glow="LG", glowAt=0), g5(n="5차전", venue="광주", home="KIA", off=True, at=0)]
SC[81] = S(0, "series5", tc=TCKL, title="준플레이오프 · 야구자판기 예상", games=SER81, brace=dict(**{"from": 2, "to": 3}, label="두 경기 중 한 경기는 LG", team="LG", at=5.5),
           pills=[dict(label="잠실 맞대결 LG 5승 4패", at=1, c=LGB), dict(label="최근 3경기 KIA 3연승", at=2, c="#C70125")])
SC[82] = S(0, "series5", tc=TCKL, title="변수 · 1차전을 LG가 잡으면", games=[g5(n="1차전", venue="광주", home="KIA", win="LG", tag="만약", at=0), g5(n="2차전", venue="광주", home="KIA", at=0), g5(n="3차전", venue="잠실", home="LG", at=0, glow="LG", glowAt=3), g5(n="4차전", venue="잠실", home="LG", at=0, glow="LG", glowAt=3), g5(n="5차전", venue="광주", home="KIA", at=0)],
           pills=[dict(label="LG 홈 승률 5할 7푼 5리", at=2, c=LGB)])
SC[83] = S(0, "psladder", steps=[dict(name="준플레이오프", sub="10월 17일~", teams=[dict(team="KIA", rank="3위"), dict(team="LG", rank="4위")], at=0),
                                dict(name="플레이오프", sub="10월 25일~", teams=[dict(team="삼성", rank="2위")], at=1),
                                dict(name="한국시리즈", sub="11월 2일~", teams=[dict(team="KT", rank="1위")], at=3)])
SC[84] = S(0, "question", text="준플레이오프 통과는\nKIA일까요?\nLG일까요?", logos=["KIA", "LG"], size=96)

N = len(TEXT) - 1
assert sorted(SC) == list(range(N)), (N, sorted(set(range(N)) - set(SC)))
lines, scenes = [], []
for j, t in enumerate(TEXT[:-1]):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))
for s in scenes:
    if s['type'] == 'toc' and s.get('on', -1) < 0 and s.get('itemFrom', 1) < 50:
        nbr = len(lines[s['startLine']]['narr'].split(' / ')); assert nbr >= s.get('itemFrom', 1) + 5, s

CH = [{"key": "와일드카드 리뷰", "title": "와일드카드 리뷰", "from": 5, "to": 28},
      {"key": "KIA 7연승", "title": "KIA 7연승", "from": 29, "to": 41},
      {"key": "선발 대결", "title": "선발 대결", "from": 42, "to": 58},
      {"key": "뒷문과 변수", "title": "뒷문과 변수", "from": 59, "to": 73},
      {"key": "예측", "title": "예측", "from": 74, "to": 84}]

TAGS = ["2026 준PO", "준플레이오프", "준PO", "준플레이오프 예측", "KIA LG 준플레이오프", "와일드카드", "LG 두산 와일드카드", "KIA 타이거즈", "LG 트윈스", "가을야구", "가을야구 예측",
        "김도영", "오스틴", "톨허스트", "네일", "올러", "곽빈", "박해민", "프로야구", "KBO", "2026 프로야구", "야구자판기"]
DESC = ("2026 프로야구 준플레이오프 KIA 타이거즈와 LG 트윈스, 누가 이길까요? 10월 14일 와일드카드 결정전(LG 4-1 두산)을 경기 내용으로 돌아보고, KBO 공식 기록으로 준플레이오프를 예측했어요.\n"
        "상대 전적·선발 투수 맞대결·투수 대 타자 기록·불펜·부상·일정까지 따져 봤어요.\n\n"
        "LG는 1회 오스틴의 2점 홈런과 8회 신민재의 스퀴즈 번트, 7회 박해민의 호수비로 두산을 한 경기 만에 꺾었어요. 두산 곽빈은 6이닝 삼진 10개로 와일드카드 한 경기 최다 탈삼진 타이 기록을 세웠지만 팀은 시즌을 마쳤어요.\n\n"
        "2026 정규시즌 KIA와 LG의 맞대결은 KIA가 9승 7패로 앞섰고, 6월 17일부터 KIA가 7연승을 했어요. LG 1차전 선발 톨허스트는 KIA전 평균자책점 6.20, KIA 올러는 LG전 평균자책점 2.40이에요. LG는 마무리 손주영의 합류가 정해지지 않았고, KIA는 마무리 전상현이 10월 6경기 8⅔이닝 동안 안타를 하나도 맞지 않았어요.\n\n"
        "야구자판기의 예상은 KIA 3승 1패예요. 다만 1차전을 LG가 잡으면 2025년 우승 팀 LG 쪽으로 기울 수 있어요. 준플레이오프 1차전은 10월 17일 광주에서 열려요.\n\n"
        "야구자판기는 매일 오늘의 야구 이슈를 정리해 드려요.\n\n"
        "준플레이오프를 통과할 팀은 KIA일까요, LG일까요? 댓글로 알려 주세요.\n\n"
        "기록: KBO 기록실(2026 정규시즌 최종 팀·선수 기록, 투수 vs 타자, 팀간 승패, 와일드카드 박스스코어)\n"
        "사진: LG 트윈스 제공, KIA 타이거즈 제공, 두산 베어스 제공, 스포츠서울(썸네일 네일), 스타뉴스(썸네일 톨허스트)")
SOURCE = "사실 출처 = KBO 기록실 직접 조회(10/15) + 기사 원문 — 프로젝트 claude/1015-롱폼15-가을야구-대사v1 및 검수 기록."

EP = {"date": "2026-10-15", "gameDate": "2026-10-14", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1015-long15-v2-8m01s", "topic": "준플레이오프예측", "totalSec": 481.4,   # 10/15 사용자: 8분 1초로(중간광고) — 엔딩 카드를 늘려 맞춤
      "gapScale": 1.05, "pauseMax": 0.4, "ttsCharsOk": 4500,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "source": SOURCE,
      "youtube": {"title": "2026 준PO 준플레이오프 예측 | KIA vs LG 누가 이길까, 와일드카드 리뷰까지 #준플레이오프 #KIA #LG",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#준플레이오프", "#가을야구", "#KIA타이거즈", "#LG트윈스", "#김도영", "#오스틴", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 2, 14, 26, 31, 38, 49, 61, 80, 84}
    HOLD = {j: 0.5 for j, s in enumerate(scenes) if s['type'] == 'toc' and j > 4}
    HOLD.update({0: 0.5, 9: 0.5, 12: 0.5, 19: 0.5, 26: 0.6, 80: 0.6})
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-15_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
