# -*- coding: utf-8 -*-
"""10/10 롱폼⑩ 「2026 FA 돈값 순위 — 누가 돈값 했고 누가 먹튀였을까」 (10/9 경기까지, 음성 API · 타입캐스트 줄별 배속 1.2 / 숫자·결론·질문 1.15)
대사 = tools/text_1010_long10.py (v4, 독립 검수 5차 오류 0). 근거 모음 = 프로젝트 claude/1010-롱폼10-FA돈값-근거모음.md
사진: 2026 구단 공식 프로필(나무위키 인포박스 원본 = 구단 프로필) → 카드/FA10_<이름> (person_card 0.774)
      경기 사진 = 다음 뉴스 원본(구단 제공 캡션) → 카드/FA10_<이름>_<장면>"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import wrap, S, END, OUT
from text_1010_long10 import TEXT
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}

BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억)$'); BAD_B = re.compile(r'^(달러|일|명|개|경기|원)')
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
        t = re.sub(r' +', ' ', re.sub(r',\s*', ' ', p)).replace('?', '').strip()
        out.append(t if '\n' in t else wrap2(t))
    return {"narr": narr, "sub": "|".join(out)}

RED, GOLD, GRAY, GREEN = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55"
C = "카드/FA10_"
P = {k: C + k for k in ["최형우", "박해민", "양현종", "홍건희", "강민호", "손아섭", "조수행", "이영하", "강백호", "박찬호", "김태훈", "이승현", "김재환", "김범수",
                         "최원준투", "이준영", "김태혁", "조상우", "한승택", "장성우", "김현수"]}
P.update({"최원준": "카드/최원준_MVP_프로필", "최원준_상체": "카드/최원준_MVP_상체", "이강철": "카드/FA9_이강철_덕아웃", "김원형": "카드/FA9_김원형", "이범호": "카드/FA9_이범호",
          "김태형": "카드/FA9_김태형", "레이예스": "카드/FA9_레이예스"})
# 경기 사진(구단 제공) — 있으면 쓰고, 없으면 프로필
GAME = {"최형우_100타점": "최형우", "강백호_30호": "강백호", "강백호_환대": "강백호", "이영하_물세례": "이영하", "이영하_포효": "이영하", "최원준_204": "최원준_상체", "한승택_세리머니": "한승택", "김재환_결승포": "김재환"}
for k, v in GAME.items():
    P[k] = C + k
P["최원준_상체"] = "카드/최원준_MVP_상체"
FACE = lambda n: "카드/FA10원_" + n   # 얼굴 원(facegrid)

def prof(i, img, name, sub, stats, **k): return S(i, "profile", img=P[img], name=name, sub=sub, stats=stats, **k)
def pv(i, img, name, sub, viz, **k): return S(i, "profile", img=P[img], name=name, sub=sub, stats=k.pop("stats", []), viz=viz, **k)
def sp(i, img, name, sub, bubbles, **k): return S(i, "speech", img=P[img], name=name, sub=sub, bubbles=bubbles, **k)
def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def ppl(i, items, **k): return S(i, "people", full=True, items=items, **k)
def pc(img, name, note="", **x): return dict({"img": P[img], "name": name, "note": note}, **x)
def tiles(i, items, **k): return S(i, "tiles", items=items, **k)
def icons(i, items, **k): return S(i, "icontiles", items=items, **k)
def bars(i, items, **k): return S(i, "bars", items=items, **k)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
def vrank(k, v, r, at=0, **x): return dict(type="rank", k=k, v=v, r=r, at=at, **x)   # 10/10 사용자 "숫자 5 원 옆에 돈값 5위 — 5위를 두 번 말하는 것 같다" → 원 안에 '5위', 옆엔 '22명 중 / 돈값한 선수'
def vpoll(title, items, **k): return dict(type="poll", title=title, items=items, **k)
def vsplit(l, r, **k): return dict(type="split", left=l, right=r, **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vduo(items, **k): return dict(type="duo", items=items, **k)
A9 = "10월 9일 기준"

SC = {}
# ── 기 (훅) 0~5
H8 = [("최원준", "최원준"), ("최형우", "최형우"), ("이영하", "이영하"), ("강백호", "강백호"), ("한승택", "한승택"), ("김범수", "김범수"), ("김재환", "김재환"), ("박찬호", "박찬호")]
FG = dict(title="2025년 겨울 FA 계약", cols=4, whole="top", items=[{"img": FACE(a), "name": n} for a, n in H8])
SC[0] = S(0, "facegrid", **FG)
SC[1] = S(1, "photo", img="경기/최원준_전광판204안타_1007_KT제공", fit="cover", text="")
SC[2] = prof(2, "김범수", "김범수", "KIA 투수", [st("3년 계약", "20억", 0), st("평균자책점", "5점대", 1, bad=True)], asof=A9)
SC[3] = prof(3, "강백호_30호", "강백호", "한화 타자", [st("4년 계약", "100억", 0), st("데뷔 첫", "30홈런", 1, hi=True), st("한화", "9위", 2, bad=True)], asof=A9)
ALL22 = ["최원준", "김현수", "한승택", "장성우", "강백호", "손아섭", "박찬호", "이영하", "최원준투:최원준(두산)", "조수행", "최형우", "강민호", "김태훈", "이승현",
         "박해민", "양현종", "조상우", "이준영", "김범수", "홍건희", "김재환", "김태혁"]
FG22 = dict(title="2025년 겨울 계약 22명", cols=6, whole="top", items=[{"img": FACE(x.split(":")[0]), "name": x.split(":")[-1]} for x in ALL22])
SC[4] = S(4, "facegrid", **FG22)
SC[5] = icons(5, [{"icon": "calendar", "n": "10/9", "v": "10월 9일", "k": "경기까지 기록", "at": 0}], title="기록 기준")
# ── 기준 6~10
SC[6] = icons(6, [{"icon": "bills", "n": 3, "v": "한 해 몸값", "k": "총액 ÷ 계약 연수", "at": 0}, {"icon": "trophy", "v": "역할 · 기록", "k": "팀 성적", "at": 0.3}, {"icon": "ticket", "v": "언론 · 팬", "k": "평가", "at": 0.6}],
                  title="돈값 순위 기준", chain="crit")
SC[7] = icons(7, [{"icon": "bills", "n": 3, "v": "한 해 몸값", "k": "총액 ÷ 계약 연수", "hi": True, "at": 0}, {"icon": "trophy", "v": "역할 · 기록", "k": "팀 성적", "at": 0}, {"icon": "ticket", "v": "언론 · 팬", "k": "평가", "at": 0}],
                  title="돈값 순위 기준", chain="crit")
SC[8] = bars(8, [{"label": "4년 100억", "value": 25, "unit": "억", "hi": True, "at": 0}, {"label": "4년 48억", "value": 12, "unit": "억", "at": 1}], max=25, title="한 해 몸값 = 총액 ÷ 계약 연수")
SC[9] = icons(9, [{"icon": "bills", "n": 3, "v": "한 해 몸값", "k": "총액 ÷ 계약 연수", "at": 0}, {"icon": "trophy", "v": "역할 · 기록", "k": "팀 성적", "hi": True, "at": 1}, {"icon": "ticket", "v": "언론 · 팬", "k": "평가", "hi": True, "at": 3}],
                  title="돈값 순위 기준", chain="crit")
SC[10] = ppl(10, [pc("최원준투", "최원준", "두산 투수", noteAt=0), pc("이준영", "이준영", "KIA 투수", noteAt=0), pc("홍건희", "홍건희", "KIA 투수", noteAt=0)], title="다쳐서 뛰지 못한 선수",
             text="순위와 따로", textAt=2, size=60)
# ── 시장 11~20
SC[11] = icons(11, [{"icon": "calendar", "v": "2025년 겨울", "k": "FA 시장", "at": 0}])
SC[12] = icons(12, [{"icon": "ticket", "v": "21명", "k": "FA 승인 선수", "at": 0}, {"icon": "calendar", "v": "황재균", "k": "협상 중 은퇴", "color": GRAY, "at": 2}], title="2025년 겨울 FA 시장", chain="mkt")
SC[13] = icons(13, [{"icon": "ticket", "v": "20명", "k": "FA 계약", "at": 0}, {"icon": "trophy", "v": "+ 2명", "k": "FA 신청 없이 이적", "hi": True, "at": 2}], title="이 영상에서 다루는 22명", chain="mkt2")
SC[14] = pv(14, "홍건희", "홍건희", "투수 · FA 신청 없이 이적", [vsteps([stp("두산 계약", "남은 2년\n15억", 0, size=38), stp("옵트아웃", "스스로 포기", 2, "bad", size=38), stp("KIA", "1년 7억", 3, "good", size=44)], h=250)])
SC[15] = pv(15, "김재환", "김재환", "타자 · FA 신청 없이 이적", [vsteps([stp("FA 신청", "안 함", 0, size=44), stp("두산 계약 조항", "협상 결렬 시\n조건 없이 풀어 줌", 2, size=34), stp("SSG", "2년 22억", 4, "good", size=44)], h=250)])
SC[16] = tiles(16, [{"team": "KT", "v": "3명", "k": "다른 팀 FA 영입\n가장 많아", "hi": True, "at": 0}])
SC[17] = ppl(17, [pc("김현수", "김현수", "LG → KT", noteAt=1), pc("최원준", "최원준", "NC → KT", noteAt=1), pc("한승택", "한승택", "KIA → KT", noteAt=1)], title="KT가 데려온 FA",
             text="강백호는 KT → 한화", textAt=0, size=56)
SC[18] = ppl(18, [pc("박찬호", "박찬호", "→ 두산", noteAt=1), pc("최형우", "최형우", "→ 삼성", noteAt=1), pc("한승택", "한승택", "→ KT", noteAt=1)], title="KIA를 떠난 FA")
SC[19] = ppl(19, [pc("김범수", "김범수", "데려옴", noteAt=1), pc("홍건희", "홍건희", "데려옴", noteAt=1), pc("양현종", "양현종", "붙잡음", noteAt=2), pc("조상우", "조상우", "붙잡음", noteAt=2),
                  pc("이준영", "이준영", "붙잡음", noteAt=2)], title="KIA가 돈을 쓴 투수 5명")
SC[20] = tiles(20, [{"team": "KT", "v": "3명 영입", "k": "", "at": 0}, {"team": "KIA", "v": "투수 5명", "k": "", "at": 0}], text="결과는 마지막에", textAt=2, size=64)
# ── 1장 돈값 TOP5 21~75
SC[21] = icons(21, [{"icon": "trophy", "v": "돈값 TOP 5", "k": "5위부터 차례로", "hi": True, "at": 0}])
SC[22] = pv(22, "한승택", "한승택", "KT 포수", [vrank("22명 중", "돈값한 선수", "5위", at=0)])
SC[23] = pv(23, "한승택", "한승택", "KT 포수", [vrank("22명 중", "돈값한 선수", "5위", at=0)], stats=[st("KIA → KT", "4년 10억", 0), st("한 해", "2억 5천만 원", 1, hi=True)])
SC[24] = bars(24, [{"label": "손아섭", "value": 1, "unit": "억", "at": 0}, {"label": "한승택", "value": 2.5, "dec": 1, "unit": "억", "hi": True, "at": 0}, {"label": "이승현 · 김태혁", "value": 3, "unit": "억", "at": 0.5},
                   {"label": "강백호", "value": 25, "unit": "억", "color": GRAY, "at": 1}], max=25, title="한 해 몸값 · 22명 중 적은 순", )
SC[25] = prof(25, "한승택_세리머니", "한승택", "KT 포수", [st("타율", "0.231", 0), st("출장", "126경기", 2, hi=True)], asof=A9)
SC[26] = ppl(26, [pc("장성우", "장성우", "무릎 → 왼손 → 옆구리", noteAt=1, bad=True), pc("한승택", "한승택", "그 자리를 메움", noteAt=2, hi=True)], title="KT 안방")
SC[27] = tiles(27, [{"team": "KT", "v": "정규리그 1위", "k": "한국시리즈 직행", "hi": True, "at": 0}])
SC[28] = sp(28, "이강철", "이강철", "KT 감독", [bb("10월 5일", "정말 든든하게\n안방을 지켰다", 1), bb("한승택에 대해", "없어선 안 될\n선수였다", 2, hi=True)])
SC[29] = pv(29, "강백호", "강백호", "한화 타자", [vrank("22명 중", "돈값한 선수", "4위", at=0)])
SC[30] = pv(30, "강백호", "강백호", "한화 타자", [vrank("22명 중", "돈값한 선수", "4위", at=0)], stats=[st("KT → 한화", "4년 100억", 1), st("2025년 겨울 FA 중", "가장 큰 금액", 3, hi=True)])
SC[31] = prof(31, "강백호_30호", "강백호", "한화 타자", [st("타율", "0.287", 0), st("홈런", "34개", 1, hi=True), st("타점", "117개", 2, hi=True)], asof=A9)
SC[32] = pv(32, "강백호_30호", "강백호", "한화 타자", [vtrend([dict(x="2018년\n신인", v=29, vt="29개"), dict(x="2026년", v=34, vt="34개", c="good")], title="한 시즌 홈런", mx=34, gap=110, delta="데뷔 첫 30홈런")])   # 10/10: stats 를 그래프 옆 배지로(그래프+기록이 세로로 넘쳐 화면이 통째로 작아졌음)
SC[33] = pv(33, "강백호_30호", "강백호", "한화 타자", [vtrend([dict(x="2021년", v=102, vt="102"), dict(x="2026년", v=117, vt="117", c="good")], title="한 시즌 타점", mx=117, gap=110)])
SC[34] = sp(34, "강백호_환대", "강백호", "한화 타자", [bb("9월 8일", "아직 전성기는\n안 왔다", 1), bb("언론", "100억도 싸다", 2, hi=True)])
SC[35] = pv(35, "강백호", "강백호", "한화 타자", [vrank("22명 중", "돈값한 선수", "4위", at=0)])
SC[36] = pv(36, "강백호", "강백호", "한화 타자", [vduo([dict(icon="money", v="25억", k="한 해 · 22명 중 최고", c="bad", at=0), dict(icon="person", v="지명타자", k="수비 없이 타격만", at=2), dict(icon="ball", v="1루수 7경기", k="9월부터", at=0, ghost=True)])])   # 10/10: 다음 장면 셋째 칸 자리 미리(숨김)
SC[37] = pv(37, "강백호", "강백호", "한화 타자", [vduo([dict(icon="money", v="25억", k="한 해 · 22명 중 최고", c="bad", at=0), dict(icon="person", v="지명타자", k="수비 없이 타격만", at=0),
                                                  dict(icon="ball", v="1루수 7경기", k="9월부터", at=0)])], asof=A9)
SC[38] = tiles(38, [{"team": "한화", "top": "2025년", "v": "준우승", "k": "", "at": 0}, {"team": "한화", "top": "2026년", "v": "9위 확정", "k": "", "color": RED, "at": 1}])
SC[39] = tiles(39, [{"team": "한화", "top": "2025년", "v": "준우승", "k": "", "at": 0}, {"team": "한화", "top": "2026년", "v": "9위 확정", "k": "", "color": RED, "at": 1}], cont=True,
               text="팬 커뮤니티: 100억 쓰고도 9위", textAt=1, size=60)
SC[40] = pv(40, "이영하", "이영하", "두산 투수", [vrank("22명 중", "돈값한 선수", "3위", at=0)])
SC[41] = pv(41, "이영하", "이영하", "두산 투수", [vrank("22명 중", "돈값한 선수", "3위", at=0)], stats=[st("두산 잔류", "4년 52억", 0), st("한 해", "13억", 1, hi=True)])
SC[42] = sp(42, "이영하", "이영하", "두산 투수", [bb("계약 직후", "두산이 내가 생각한\n선을 넘었다", 1)])
SC[43] = pv(43, "이영하_포효", "이영하", "두산 투수", [vsteps([stp("시즌 준비", "선발", 0), stp("개막", "엔트리 제외", 1, "bad")], h=220, slots=4)])
SC[44] = pv(44, "이영하_포효", "이영하", "두산 투수", [vsteps([stp("시즌 준비", "선발", 0), stp("개막", "엔트리 제외", 0, "bad"), stp("4월 15일", "선발 1번", 1, size=38),
                                                          stp("그 뒤", "마무리 앞", 2, size=38)], h=220, slots=4)])
SC[45] = pv(45, "이영하_포효", "이영하", "두산 투수", [vsteps([stp("시즌 준비", "선발", 0), stp("개막", "엔트리 제외", 0, "bad"), stp("4월 15일", "선발 1번", 0, size=38),
                                                          stp("김택연 부상", "마무리", 2, "good", size=38)], h=220, slots=4)])
SC[46] = pv(46, "이영하_물세례", "이영하", "두산 마무리", [vtrend([dict(x="2020년", v=6, vt="6"), dict(x="2026년", v=26, vt="26", c="good")], title="한 시즌 세이브", mx=26, gap=110, delta="데뷔 첫 20세이브", deltaAt=1)])
SC[47] = prof(47, "이영하", "이영하", "두산 마무리", [st("세이브", "26개 · 4위", 0, hi=True), st("67이닝", "삼진 88개", 2), st("평균자책점", "3.22", 3)], asof=A9)
SC[48] = sp(48, "이영하", "이영하", "두산 마무리", [bb("8월 · 선발 꿈을 접은 이유", "돈 받으니까요.\n프로잖아요.", 1, hi=True)])
SC[49] = pv(49, "이영하_포효", "이영하", "두산 마무리", [vpoll("팬 커뮤니티", [dict(t="52억 혜자", n=5, c="good", at=1)])])
SC[50] = icons(50, [{"icon": "bills", "v": "혜자", "k": "받는 값보다 더 해 준다", "hi": True, "at": 0}])
SC[51] = pv(51, "최형우", "최형우", "삼성 타자", [vrank("22명 중", "돈값한 선수", "2위", at=0)])
SC[52] = pv(52, "최형우", "최형우", "삼성 타자", [vrank("22명 중", "돈값한 선수", "2위", at=0)], stats=[st("KIA → 삼성", "2년 26억", 0), st("한 해", "13억", 1, hi=True)])
SC[53] = prof(53, "최형우_100타점", "최형우", "삼성 타자 · 만 42세", [st("나이", "만 42세", 0, hi=True), st("타율", "0.305", 1), st("홈런", "18개", 2), st("타점", "106개", 3, hi=True)], asof=A9)
SC[54] = prof(54, "최형우_100타점", "최형우", "삼성 타자 · 만 42세", [st("9월 18일 한화전", "100타점", 0), st("42세 9개월 2일", "KBO 최고령", 3, hi=True)])
SC[55] = pv(55, "최형우_100타점", "최형우", "삼성 타자 · 만 42세", [vtrend([dict(x="2024년 KIA", v=40.7, vt="40세 8개월"), dict(x="2026년 삼성", v=42.8, vt="42세 9개월", c="good")],
                                                                               title="최고령 100타점", mx=42.8)])
SC[56] = sp(56, "최형우", "최형우", "삼성 타자", [bb("9월 18일", "기록은 큰 의미가 없다\n팀이 이기는 게 중요", 1)])
SC[57] = tiles(57, [{"team": "삼성", "v": "2위 확정", "k": "", "at": 0}, {"v": "26억", "k": "싸 보인다 · 언론", "hi": True, "at": 1}])
SC[58] = pv(58, "최원준", "최원준", "KT 외야수", [vrank("22명 중", "돈값한 선수", "1위", at=0)])
SC[59] = pv(59, "최원준", "최원준", "KT 외야수", [vrank("22명 중", "돈값한 선수", "1위", at=0)], stats=[st("NC → KT", "4년 48억", 0), st("한 해", "12억", 1, hi=True)])
SC[60] = pv(60, "최원준", "최원준", "KT 외야수", [vsplit({"who": "계약 때", "t": "2025년 부진\n오버페이 비판", "c": "bad", "at": 0, "size": 40}, {"who": "뜻", "t": "너무 비싸게\n줬다", "c": "bad", "at": 2, "size": 40}, sep="=")])   # 10/10: 같은 뜻 풀이 → VS 대신 =, 같은 색
SC[61] = sp(61, "최원준", "최원준", "KT 외야수", [bb("계약 때", "구단이 싸게 데려왔다는\n말을 꼭 듣고 싶다", 1)])
SC[62] = prof(62, "최원준_204", "최원준", "KT 외야수", [st("타율", "0.355", 0), st("안타", "204개", 1, hi=True), st("득점", "124개", 2, hi=True)], asof=A9)
SC[63] = prof(63, "최원준_204", "최원준", "KT 외야수", [st("타율", "0.355", 0), st("안타", "204개", 0, hi=True), st("득점", "124개 · 리그 1위", 0, hi=True)], asof=A9)
SC[64] = bars(64, [{"label": "레이예스\n2024년", "value": 202, "unit": "안타", "color": GRAY, "at": 0}, {"label": "최원준\n2026년", "value": 204, "unit": "안타", "hi": True, "at": 3}],
              max=210, title="KBO 한 시즌 최다 안타")
SC[65] = bars(65, [{"label": "레이예스\n2024년", "value": 202, "unit": "안타", "color": GRAY, "at": 0}, {"label": "최원준\n2026년", "value": 204, "unit": "안타", "hi": True, "at": 0},
                   {"label": "레이예스\n2026년", "value": 204, "unit": "안타", "hi": True, "at": 1}], max=210, title="KBO 한 시즌 최다 안타", cont=True, asof=A9)
SC[66] = bars(66, [{"label": "레이예스\n2024년", "value": 202, "unit": "안타", "color": GRAY, "at": 0}, {"label": "최원준\n2026년", "value": 204, "unit": "안타", "hi": True, "at": 0},
                   {"label": "레이예스\n2026년", "value": 204, "unit": "안타", "hi": True, "at": 0}], max=210, title="KBO 한 시즌 최다 안타", cont=True, text="정규시즌 남은 경기 → 바뀔 수도", textAt=0, size=58)
SC[67] = pv(67, "최원준_상체", "최원준", "KT 외야수", [vsplit({"who": "언론", "t": "역대급\n저점 매수", "c": "good", "at": 0, "size": 44}, {"who": "뜻", "t": "몸값 떨어졌을 때\n싸게 잘 데려왔다", "c": "good", "at": 2, "size": 36}, sep="=")])
SC[68] = pv(68, "최원준_상체", "최원준", "KT 외야수", [vpoll("팬 커뮤니티", [dict(t="역대 최고 가성비 FA", n=5, c="good", at=1)])])
SC[69] = ppl(69, [pc("조상우", "조상우", ""), pc("김태훈", "김태훈", ""), pc("조수행", "조수행", "")], title="5위 밖 · 돈값을 해낸 선수")
SC[70] = prof(70, "조상우", "조상우", "KIA 투수", [st("2년 15억", "한 해 7억 5천만 원", 0), st("출장", "70경기", 2, hi=True)], asof=A9)
SC[71] = prof(71, "조상우", "조상우", "KIA 투수", [st("2년 15억", "한 해 7억 5천만 원", 0), st("출장", "70경기", 0, hi=True), st("홀드 · 마무리 앞 리드 지킴", "20개", 0, hi=True)], asof=A9)   # 10/10: 홀드 카드(viz)가 기록과 겹쳐 화면이 0.81배로 줄었음 → 기록 칸 하나로
SC[72] = prof(72, "김태훈", "김태훈", "삼성 투수", [st("최대 4년", "20억", 0), st("46경기", "평균자책점 2.54", 1, hi=True)], asof=A9)
SC[73] = prof(73, "조수행", "조수행", "두산 외야수", [st("4년", "16억", 0), st("타율", "0.323", 1, hi=True), st("언론", "혜자 계약", 2, hi=True)], asof=A9)
SC[74] = ppl(74, [pc("조상우", "조상우", "70경기 20홀드", noteAt=0), pc("김태훈", "김태훈", "46경기 2.54", noteAt=0), pc("조수행", "조수행", "타율 0.323", noteAt=0)], title="5위 밖 · 돈값을 해낸 선수",
             text="역할이 TOP 5보다 작아서", textAt=1, size=58)
SC[75] = ppl(75, [pc("조상우", "조상우", "마무리 앞 투수", noteAt=1), pc("김태훈", "김태훈", "마무리 앞 투수", noteAt=1), pc("조수행", "조수행", "221타석", noteAt=2)], title="5위 밖 · 돈값을 해낸 선수", cont=True)
# ── 2장 엇갈린 계약 76~98
SC[76] = ppl(76, [pc("박찬호", "박찬호", ""), pc("김현수", "김현수", ""), pc("박해민", "박해민", ""), pc("양현종", "양현종", ""), pc("장성우", "장성우", "")], title="평가가 엇갈린 계약")
SC[77] = prof(77, "박찬호", "박찬호", "두산 유격수", [st("KIA → 두산", "4년 80억", 0), st("한 해", "20억", 1, hi=True)])
SC[78] = prof(78, "박찬호", "박찬호", "두산 유격수", [st("KIA → 두산", "4년 80억", 0), st("한 해", "20억", 0, hi=True), st("타율 · 홈런 · 도루", "0.283 · 5개 · 33개", 0)], asof=A9)
SC[79] = prof(79, "박찬호", "박찬호", "두산 유격수", [st("KIA → 두산", "4년 80억", 0), st("한 해", "20억", 0, hi=True), st("타율 · 홈런 · 도루", "0.283 · 5개 · 33개", 0), st("타격 기록만 보면", "20억엔 못 미쳐", 1, bad=True)])
SC[80] = pv(80, "박찬호", "박찬호", "두산 유격수", [vduo([dict(icon="ball", v="142경기", k="두산 143경기 중", c="good", at=1)])], asof=A9)
SC[81] = pv(81, "박찬호", "박찬호", "두산 유격수", [vduo([dict(icon="ball", v="142경기", k="두산 143경기 중", c="good", at=0), dict(icon="cal", v="8년 연속 130경기", k="손아섭 다음 · 내야수 최초", c="good", at=1)])])
SC[82] = sp(82, "김원형", "김원형", "두산 감독", [bb("9월 19일 · 박찬호에 대해", "군말 없이 계속 나가 주는 게\n감독으로서 고마운 일", 1)])
SC[83] = sp(83, "박찬호", "박찬호", "두산 유격수", [bb("시즌 중", "FA 계약 하고 나니\n오히려 스트레스가 더 심해졌다", 2)])
SC[84] = prof(84, "김현수", "김현수", "KT 외야수", [st("LG → KT", "3년 50억", 0), st("옵션 없이", "전액 보장", 2, hi=True)])
SC[85] = prof(85, "김현수", "김현수", "KT 외야수", [st("LG → KT", "3년 50억", 0), st("옵션 없이", "전액 보장", 0, hi=True), st("타율 · 홈런 · 타점", "0.284 · 13개 · 93개", 0)], asof=A9)
SC[86] = sp(86, "이강철", "이강철", "KT 감독", [bb("6월", "최원준·김현수가 타석에 서면\n기대감이 생긴다", 1)])
SC[87] = pv(87, "김현수", "김현수", "KT 외야수", [vsplit({"who": "팬 커뮤니티", "t": "50억 치고\n아쉽다", "c": "bad", "at": 1, "size": 40}, {"who": "팬 커뮤니티", "t": "KT가 FA를\n잘 데려왔다", "c": "good", "at": 2, "size": 40})])
SC[88] = prof(88, "박해민", "박해민", "LG 중견수", [st("4년", "65억", 0), st("한 해", "16억 2천5백만 원", 1, hi=True)])
SC[89] = prof(89, "박해민", "박해민", "LG 중견수", [st("4년", "65억", 0), st("한 해", "16억 2천5백만 원", 0, hi=True), st("타율 · 도루", "0.291 · 41개", 0)], asof=A9)
SC[90] = bars(90, [{"label": "전준호", "value": 549, "unit": "개", "color": GRAY, "at": 1}, {"label": "이종범", "value": 510, "unit": "개", "color": GRAY, "at": 1.3}, {"label": "이대형", "value": 505, "unit": "개", "color": GRAY, "at": 1.6},
                   {"label": "박해민", "value": 500, "unit": "개", "hi": True, "at": 2, "note": "500 · 10월 6일"}], max=549, title="KBO 통산 500도루 · 역대 4번째")
SC[91] = pv(91, "박해민", "박해민", "LG 중견수", [vduo([dict(icon="person", v="중견수 수비", k="", c="good", at=1), dict(icon="ball", v="주루", k="", c="good", at=1)])], stats=[st("가치", "기록만으로 매기기 어려워", 2)])
SC[92] = prof(92, "양현종", "양현종", "KIA 투수", [st("2년 + 조건 맞으면 1년", "45억", 0, hi=True)])
SC[93] = pv(93, "양현종", "양현종", "KIA 투수", [vpoll("5~6월 팬 커뮤니티", [dict(t="왜 45억을 줬나", n=4, c="bad", at=1)])])
SC[94] = prof(94, "양현종", "양현종", "KIA 투수", [st("2026년", "12승", 0, hi=True), st("언론", "한물갔다는 혹평 뒤집어", 1, hi=True)], asof=A9)
SC[95] = prof(95, "양현종", "양현종", "KIA 투수", [st("2026년", "12승", 0, hi=True), st("언론", "한물갔다는 혹평 뒤집어", 0, hi=True), st("평균자책점", "4.29", 0, bad=True)], asof=A9)
SC[96] = prof(96, "장성우", "장성우", "KT 포수", [st("2년 16억", "한 해 8억", 0), st("4월", "홈런 선두 · 혜자 소리", 2, hi=True)])
SC[97] = pv(97, "장성우", "장성우", "KT 포수", [vsteps([stp("6월", "무릎", 0, "bad"), stp("6월", "왼손 골절", 0.3, "bad"), stp("7월 · 8월", "옆구리 두 번", 0.6, "bad")], h=220)],
            stats=[st("출장", "75경기", 2, bad=True), st("타율", "1할대", 3, bad=True)], asof=A9)
SC[98] = pv(98, "장성우", "장성우", "KT 포수", [vstamp("엇갈린 계약", 2, c="gold")], stats=[st("출장", "75경기", 0, bad=True), st("타율", "1할대", 0, bad=True)])   # 10/10: 도장 뜨기 전 빈칸 → 앞 장면 기록 그대로
# ── 3장 아쉬운 계약 99~119
SC[99] = icons(99, [{"icon": "bills", "v": "아쉬운 계약", "k": "몸값만큼 해 주지 못한", "color": RED, "at": 0}])
SC[100] = pv(100, "이승현", "이승현", "삼성 우완 투수", [vrank("22명 중", "아쉬운 계약", "3위", at=0, c="bad")])
SC[101] = pv(101, "이승현", "이승현", "삼성 우완 투수", [vrank("22명 중", "아쉬운 계약", "3위", at=0, c="bad")], stats=[st("2년 6억", "한 해 3억", 0), st("평균자책점", "6.02", 2, bad=True)], asof=A9)   # 10/10: 순위 그림은 그대로, 기록만 아래에
SC[102] = pv(102, "이승현", "이승현", "삼성 우완 투수", [vrank("22명 중", "아쉬운 계약", "3위", at=0, c="bad")], stats=[st("2년 6억", "한 해 3억", 0, hi=True), st("평균자책점", "6.02", 0, bad=True)])   # "몸값이 작아서 3위" → 몸값 칸 강조
SC[103] = pv(103, "김재환", "김재환", "SSG 타자", [vrank("22명 중", "아쉬운 계약", "2위", at=0, c="bad")])
SC[104] = pv(104, "김재환", "김재환", "SSG 타자", [vrank("22명 중", "아쉬운 계약", "2위", at=0, c="bad")], stats=[st("SSG", "2년 22억", 0), st("한 해", "11억", 1)])
SC[105] = prof(105, "김재환", "김재환", "SSG 타자", [st("타율", "0.218", 0, bad=True), st("규정 타석 48명 중", "가장 낮음", 1, bad=True)], asof=A9)
SC[106] = icons(106, [{"icon": "ball", "v": "규정 타석", "k": "타율 순위에 드는 최소 타석 수", "at": 0}])
SC[107] = pv(107, "김재환", "김재환", "SSG 타자", [vsteps([stp("4월", "타율 0.110", 1, "bad"), stp("4월 27일", "2군행", 2, "bad")], h=220)])
SC[108] = pv(108, "김재환", "김재환", "SSG 타자", [vpoll("5월 잠실 두산전", [dict(t="두산 팬 야유", note="이적 과정에 분노", n=6, c="bad", at=2)])])
SC[109] = sp(109, "김재환", "김재환", "SSG 타자", [bb("8월", "솔직히 마음은\n좋지 않다", 2)])
SC[110] = prof(110, "김재환_결승포", "김재환", "SSG 타자", [st("타율", "0.218", 0, bad=True), st("홈런", "24개", 0, hi=True), st("장타", "살아 있었다", 1, hi=True)], asof=A9)
SC[111] = pv(111, "김범수", "김범수", "KIA 투수", [vrank("22명 중", "아쉬운 계약", "1위", at=0, c="bad")])
SC[112] = pv(112, "김범수", "김범수", "KIA 투수", [vrank("22명 중", "아쉬운 계약", "1위", at=0, c="bad")], stats=[st("한화 → KIA", "3년 20억", 0), st("한 해", "6억 넘게", 1)])
SC[113] = prof(113, "김범수", "김범수", "KIA 투수", [st("출장", "59경기", 0), st("평균자책점", "5.77", 1, bad=True), st("이닝당 출루 허용", "2.05명", 0, bad=True, ghost=True)], asof=A9)   # 10/10: 다음 장면 세 번째 칸 자리를 미리(숨김) → 앞 칸이 안 움직임
SC[114] = prof(114, "김범수", "김범수", "KIA 투수", [st("출장", "59경기", 0), st("평균자책점", "5.77", 0, bad=True), st("이닝당 출루 허용", "2.05명", 0, bad=True)], asof=A9,
               viz=[vduo([dict(icon="person", v="2명+", k="이닝마다 안타·볼넷", c="bad", at=0)])])
SC[115] = pv(115, "김범수", "김범수", "KIA 투수", [vsteps([stp("7월 평균자책점", "9점대", 0, "bad"), stp("그 뒤", "2군에서 재정비", 2, "bad")], h=220)])
SC[116] = sp(116, "이범호", "이범호", "KIA 감독", [bb("9월 · 김범수에 대해", "너무 단순하게\n들어간다", 1)])
SC[117] = ppl(117, [pc("김재환", "김재환", "한 해 11억\n홈런 24개", noteAt=0), pc("김범수", "김범수", "한 해 6억 넘게\n평균자책점 5.77", noteAt=0, bad=True)], title="아쉬운 계약 1위 · 2위")
SC[118] = ppl(118, [pc("김재환", "김재환", "한 해 11억\n홈런 24개", noteAt=0, dim=True), pc("김범수", "김범수", "한 해 6억 넘게\n평균자책점 5.77", noteAt=0, bad=True)], title="아쉬운 계약 1위 · 2위", cont=True)   # 10/10: 아래 문구가 들어가면 카드가 작아져(설명 24px) 117 과 크기가 달라짐 → 문구 빼고 카드 그대로
SC[119] = pv(119, "김범수", "김범수", "KIA 투수", [vduo([dict(icon="cal", v="2028년까지", k="계약 남음", at=0)])])
# ── 4장 다쳐서 뛰지 못한 계약 120~128
SC[120] = ppl(120, [pc("최원준투", "최원준", "두산 투수", noteAt=0), pc("이준영", "이준영", "KIA 투수", noteAt=0), pc("홍건희", "홍건희", "KIA 투수", noteAt=0)], title="다쳐서 뛰지 못한 계약",
              text="선수 탓은 아니지만 구단엔 아픈 계약", textAt=1, size=56)
SC[121] = ppl(121, [pc("최원준투", "최원준", "두산 투수", noteAt=0, hi=True), pc("최원준", "최원준", "KT 외야수", noteAt=1)], title="이름만 같은 다른 선수")
SC[122] = prof(122, "최원준투", "최원준", "두산 투수", [st("두산 잔류", "4년 38억", 0), st("한 해", "9억 5천만 원", 1)])
SC[123] = pv(123, "최원준투", "최원준", "두산 투수", [vsteps([stp("3/28 · 4/1", "2경기 2이닝", 0), stp("4월 초", "팔꿈치 근육 부상", 2, "bad")], h=230, slots=4)])
SC[124] = pv(124, "최원준투", "최원준", "두산 투수", [vsteps([stp("3/28 · 4/1", "2경기 2이닝", 0), stp("4월 초", "팔꿈치 근육 부상", 0, "bad"), stp("5월 말", "인대 손상", 1, "bad")], h=230, slots=4)])
SC[125] = pv(125, "최원준투", "최원준", "두산 투수", [vsteps([stp("3/28 · 4/1", "2경기 2이닝", 0), stp("4월 초", "팔꿈치 근육 부상", 0, "bad"), stp("5월 말", "인대 손상", 0, "bad"),
                                                          stp("6월 6일", "인대 접합\n수술 발표", 1, "bad", size=34)], h=230, slots=4)], stats=[st("2026시즌", "마감", 3, bad=True)])
SC[126] = prof(126, "이준영", "이준영", "KIA 투수", [st("KIA 잔류", "3년 12억", 0), st("시즌 전", "팔 부상", 2, bad=True), st("1군 등판", "0경기", 3, bad=True)], asof=A9)
SC[127] = prof(127, "홍건희", "홍건희", "KIA 투수", [st("KIA", "1년 7억", 0), st("4월", "오른쪽 어깨 부상", 1, bad=True), st("1군 등판", "4경기", 2, bad=True)], asof=A9)
SC[128] = sp(128, "홍건희", "홍건희", "KIA 투수", [bb("9월 복귀 때", "팀에 굉장히\n미안했다", 2)], stats=[])
# ── 나머지 129~136
SC[129] = ppl(129, [pc("강민호", "강민호", "삼성", noteAt=0), pc("손아섭", "손아섭", "두산", noteAt=0), pc("김태혁", "김태혁", "롯데", noteAt=0)], title="나머지 3명")
SC[130] = prof(130, "강민호", "강민호", "삼성 포수", [st("2년 20억", "한 해 10억", 0), st("KBO 최초", "4번째 FA 계약", 2, hi=True)])
SC[131] = prof(131, "강민호", "강민호", "삼성 포수", [st("2년 20억", "한 해 10억", 0), st("KBO 최초", "4번째 FA 계약", 0, hi=True), st("109경기", "홈런 13개", 0), st("순위", "몸값만큼은 했다", 1)], asof=A9)
SC[132] = pv(132, "손아섭", "손아섭", "두산 외야수", [vsteps([stp("한화", "1년 1억", 0), stp("4월 14일", "두산 트레이드", 2), stp("두산", "타율 0.232", 3)], h=220)], asof=A9)
SC[133] = pv(133, "손아섭", "손아섭", "두산 외야수", [vsteps([stp("한화", "1년 1억", 0), stp("4월 14일", "두산 트레이드", 0), stp("두산", "타율 0.232", 0)], h=220)], stats=[st("순위", "넣지 않음", 2)])
SC[134] = prof(134, "김태혁", "김태혁", "롯데 투수 · 옛 이름 김상수", [st("통산", "700경기", 0, hi=True)])
SC[135] = prof(135, "김태혁", "김태혁", "롯데 투수 · 옛 이름 김상수", [st("통산", "700경기", 0, hi=True), st("롯데", "1년 3억", 0), st("9월 15일", "은퇴 발표", 2)])
SC[136] = sp(136, "김태형", "김태형", "롯데 감독", [bb("감독 첫해 2024년 · 김태혁에 대해", "마당쇠 역할을\n정말 잘해 줬다", 2), bb("9월 29일", "수고 많이 했다", 3)])
# ── 결론 137~146
SC[137] = tiles(137, [{"team": "KT", "v": "3명 영입", "k": "", "at": 0}, {"team": "KIA", "v": "투수 5명", "k": "", "at": 0}])
SC[138] = tiles(138, [{"team": "KT", "top": "2025년 겨울 시장", "v": "승자", "k": "", "hi": True, "at": 0}])
SC[139] = ppl(139, [pc("최원준", "최원준", "138경기", noteAt=1), pc("김현수", "김현수", "140경기", noteAt=1), pc("한승택", "한승택", "126경기", noteAt=1)], title="KT가 데려온 FA",
              text="KT 정규리그 1위", textAt=3, size=64)
SC[140] = tiles(140, [{"team": "KT", "v": "정규리그 1위", "k": "팬: FA 영입 덕분", "hi": True, "at": 0}])
SC[141] = tiles(141, [{"team": "KIA", "v": "FA 성적", "k": "아쉬웠다", "color": RED, "at": 0}])
SC[142] = ppl(142, [pc("최형우", "최형우", "삼성 · 제 몫", noteAt=0), pc("한승택", "한승택", "KT · 제 몫", noteAt=0), pc("박찬호", "박찬호", "두산 · 142경기", noteAt=2)], title="KIA를 떠난 FA")
SC[143] = ppl(143, [pc("조상우", "조상우", "제 몫", noteAt=1, hi=True), pc("양현종", "양현종", "12승", noteAt=2, hi=True), pc("김범수", "김범수", "부진", noteAt=3, bad=True),
                    pc("이준영", "이준영", "부상", noteAt=4, bad=True), pc("홍건희", "홍건희", "부상", noteAt=4, bad=True)], title="KIA가 돈을 쓴 투수 5명")
SC[144] = tiles(144, [{"team": "KIA", "top": "2025년", "v": "가을야구 탈락", "k": "", "color": GRAY, "at": 0}, {"team": "KIA", "top": "10월 9일", "v": "3위", "k": "", "hi": True, "at": 1}])
SC[145] = ppl(145, [pc("강백호", "강백호", "4년 100억", noteAt=1), pc("박찬호", "박찬호", "4년 80억", noteAt=1)], title="계약이 가장 큰 두 명")
SC[146] = ppl(146, [pc("강백호", "강백호", "4년 100억", noteAt=0), pc("박찬호", "박찬호", "4년 80억", noteAt=0)], title="계약이 가장 큰 두 명", cont=True,
              text="계약이 끝날 때 돈값을 했다는\n말을 들을 선수는?", textAt=0, size=60)

lines, scenes = [], []
for i, (narr, sub) in enumerate(TEXT):
    lines.append(L(narr, sub))
    sc = SC[i]; assert sc['startLine'] == i, i; scenes.append(sc)
lines[-1]['gapAfter'] = 0.5
lines.append(dict(CTA_LINE))

CH = [("기준과 시장", 6, 20), ("돈값 TOP 5", 21, 75), ("엇갈린 계약", 76, 98), ("아쉬운 계약", 99, 119), ("다쳐서 뛰지 못한 계약", 120, 128), ("나머지와 결론", 129, 146)]

TAGS = ["FA 돈값", "FA 먹튀", "2026 FA", "프로야구 FA", "KBO FA", "최원준", "최형우", "이영하", "강백호", "한승택", "김현수", "박찬호", "박해민", "양현종", "장성우", "김재환", "김범수",
        "이승현", "조상우", "김태훈", "조수행", "강민호", "손아섭", "홍건희", "이준영", "김태혁", "프로야구", "KBO", "야구자판기"]
_tl = sum(len(t) + (2 if " " in t else 0) for t in TAGS) + len(TAGS) - 1
assert _tl <= 500, _tl
DESC = ("2026 FA 돈값 순위 — 2025년 겨울 FA 계약 선수들의 2026시즌을 정리했어요. 누가 돈값을 했고, 누가 아쉬웠을까요? (기록은 10월 9일 경기까지)\n"
        "계약 총액을 계약 연수로 나눈 '한 해 몸값'에 비해 팀에서 맡은 역할과 기록, 팀 성적, 언론과 팬들의 평가를 함께 봤어요. 다쳐서 뛰지 못한 선수는 순위와 따로 봤어요.\n\n"
        "돈값 TOP 5: 1위 KT 최원준(4년 48억, 타율 0.355·204안타·득점 1위), 2위 삼성 최형우(2년 26억, 106타점·KBO 최고령 100타점), 3위 두산 이영하(4년 52억, 26세이브), "
        "4위 한화 강백호(4년 100억, 데뷔 첫 30홈런·117타점), 5위 KT 한승택(4년 10억, 126경기 안방).\n\n"
        "평가가 엇갈린 계약: 두산 박찬호, KT 김현수, LG 박해민, KIA 양현종, KT 장성우. 아쉬운 계약: KIA 김범수, SSG 김재환, 삼성 이승현. "
        "다쳐서 뛰지 못한 계약: 두산 최원준(투수), KIA 이준영, KIA 홍건희.\n\n"
        "결론적으로 김현수·최원준·한승택을 데려온 KT가 2025년 겨울 시장의 승자였다고 봤어요. KIA는 FA 성적만 보면 아쉬웠지만, 10월 9일 기준 3위예요.\n\n"
        "야구자판기는 매일 오늘의 야구 이슈를 정리해 드려요.\n\n"
        "계약이 끝날 때 돈값을 했다는 말을 들을 선수는 100억 강백호일까요? 80억 박찬호일까요? 댓글로 알려 주세요.\n\n"
        "사진: 구단 공식 선수 프로필 — KT 위즈·삼성 라이온즈·KIA 타이거즈·LG 트윈스·두산 베어스·SSG 랜더스·한화 이글스·롯데 자이언츠 / "
        "경기 사진 — KT 위즈 제공(최원준·한승택·장성우), 삼성 라이온즈 제공(최형우), 한화 이글스 제공(강백호), 두산 베어스 제공(이영하), SSG 랜더스 제공(김재환)")
SOURCE = "기록: KBO 기록실 10/9. 사건·발언·여론 출처 = 프로젝트 claude/1010-롱폼10-FA돈값-근거모음.md (선수별 기사 2곳 이상 + 엠팍 글 제목)."

EP = {"date": "2026-10-10", "gameDate": "2026-10-09", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1010-long10-v3", "topic": "FA돈값2026",
      "gapScale": 1.05, "pauseMax": 0.4,   # 10/10 사용자 "전체적으로 루즈, 텀이 길다 — 롱폼⑨ 속도·텀이 적절": 검수판 무음 26.4% vs ⑨ 23.0% → 줄 사이 쉼 1.25→1.05배, 줄 안 쉼 0.4초까지
      "chapters": [{"key": t, "title": t, "from": a, "to": b} for t, a, b in CH],
      "lines": lines, "scenes": scenes, "thumb": {}, "source": SOURCE,
      "youtube": {"title": "2026 FA 돈값 순위 | 누가 돈값 했고 누가 먹튀였을까 최원준 최형우 강백호 #FA #프로야구",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#FA", "#돈값", "#먹튀", "#프로야구", "#KBO", "#최원준", "#최형우", "#강백호", "#이영하", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 3, 4, 8, 10, 22, 29, 40, 51, 58, 62, 64, 65, 74, 79, 95, 100, 103, 105, 111, 118, 120, 131, 138, 141, 144, 146}
    HOLD = {5: 0.6, 10: 0.6, 20: 0.7, 28: 0.6, 39: 0.6, 50: 0.6, 57: 0.6, 68: 0.6, 75: 0.6, 98: 0.6, 119: 0.6, 128: 0.6, 136: 0.6, 145: 0.4}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    th = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumb_1010_long10.json')
    if os.path.exists(th): EP['thumb'] = json.load(open(th, encoding='utf-8'))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-10_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for b in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', b)) > 22: print('호흡 초과', i, b)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
