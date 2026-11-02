# -*- coding: utf-8 -*-
"""11/2 롱폼㉟ 「한국시리즈 KT 우승 예측」 콘티 (집 PC · 음성 API).
대사 = tools/text_1102_long35.py. 근거 = KBO 기록실·기사 원문(롱폼㉝㉟㊱ 근거모음).
실행: python -X utf8 tools/gen_1102_long35.py → episodes/2026-11-02_롱폼.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t36', os.path.join(HERE, 'text_1102_long35.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
KEYS = [x[0] for x in _t.LINES]

BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억|(?:^| )다|(?:^| )못|(?:^| )안|(?:^| )만|(?:^| )(?:이번|지난|다음|올|그))$'); BAD_B = re.compile(r'^(건 |것 |수 |때 |중 |구단|달러|일|명|개|경기|원|타수|안타|\d+(?:푼|리)(?![가-힣]*할))')
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
    return {"narr": narr, "sub": "|".join(t if '\n' in t else wrap2(t) for t in (re.sub(r' +', ' ', p).strip() for p in b))}


RED, GOLD, GRAY, GREEN = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55"
TC = {"삼성": "#074CA1", "KIA": "#EA0029", "KT": "#12161F"}.get
def PL(img, name, team, res, kind, at, **k): return dict(dict(name=name, img=P.get(img, img), team=team, res=res, kind=kind, at=at), **k)
def TA(k, v, at, hi=False): return dict(k=k, v=v, at=at, hi=hi)
def RL(title, plays, tally, **k): return S(0, "rally", title=title, plays=plays, tally=tally, noCenter=True, **k)
def PLOG(img, name, team, sub, blocks, **k): return S(0, "plog", img=P.get(img, img) if img else None, name=name, team=team, sub=sub, blocks=blocks, noCenter=True, **k)
def LN(*items, at=0): return dict(type="line", items=[list(x) for x in items], at=at)
def WDL(title, rows, **k): return S(0, "wdl", title=title, rows=rows, noCenter=True, **k)
def TL(title, items, **k): return S(0, "tline", title=title, items=items, noCenter=True, **k)
def Q(text, logos, **k): return S(0, "question", text=text, logos=logos, logoSize=k.pop('logoSize', 200), size=k.pop('size', 96), **k)
def MU(l, r, score, text, tag, **k): return S(0, "matchup", left=l, right=r, score=score, text=text, tag=tag, **k)
def RS(title, rows, team="KT", **k): return S(0, "rankstrip", title=title, team=team, rows=rows, noCenter=True, **k)
def SCALE(title, left, right, tilt, **k): return S(0, "scale", title=title, left=left, right=right, tilt=tilt, noCenter=True, **k)
def BARS(title, items, mx, **k): return S(0, "bars", title=title, items=items, max=mx, noCenter=True, **k)
def FACE(img, name, team, role, say=None, sayAt=1.0, at=0): return S(0, "faces", items=[dict(img=P.get(img, img), name=name, team=team, role=role, at=at, **(dict(say=say, sayAt=sayAt) if say else {}))], noCenter=True)
def FO(title, L_, R_, rows, **k): return S(0, "faceoff", title=title, left=L_, right=R_, rows=rows, noCenter=True, **k)
def side(img, name, team, role, at): return dict(img=P.get(img, img), name=name, team=team, role=role, at=at)
def G(n, venue, home, win, at): return dict(n=n, venue=venue, home=home, win=win, at=at)
def SER(title, games, **k): return S(0, "series5", title=title, games=games, noCenter=True, **k)
def PC(title, base, chips, **k): return S(0, "probcalc", title=title, base=base, team="KT", chips=chips, noCenter=True, **k)
def CHIP(k, d, at, team=None): return dict(dict(k=k, d=d, at=at), **(dict(team=team) if team else {}))

# ── 11/1 02:40 사용자 "모션그래픽·인포그래픽 같은 스타일만이라 식상 — 다른 스타일도 전부 섞어서": 사진 중심(hero)·전광판(board)·신문 스크랩(clip)·작전판(chalk) ──
def HERO(img, name, team, kicker, stats, **k): return S(0, "hero", img=P.get(img, img), name=name, team=team, kicker=kicker, stats=stats, noCenter=True, **k)
def ST(k, v, at, hi=False, **x): return dict(dict(k=k, v=v, at=at, hi=hi), **x)
def BOARD(title, **k): return S(0, "board", title=title, noCenter=True, **k)
def BIG(lt, lv, rt, rv, at, note=None): return dict(dict(l=dict(team=lt, v=lv), r=dict(team=rt, v=rv), at=at), **({"note": note} if note else {}))
def CLIP(clips, **k): return S(0, "clip", clips=clips, noCenter=True, **k)
def CL(head, at, **x): return dict(dict(head=head, at=at), **{kk: (P.get(v, v) if kk == "img" else v) for kk, v in x.items()})
def CHALK(title, lines, **k): return S(0, "chalk", title=title, lines=lines, noCenter=True, **k)
def LNc(t, at, c="w", **x): return dict(dict(t=t, at=at, c=c), **x)

P = {
    "고영표": "경기/고영표_상체_1011_KT제공", "고영표B": "경기/고영표_투구_1011_KT제공", "김현수": "경기/김현수_송구_1006_KT제공", "소형준": "카드/G18_소형준_B", "최원준D": "경기/최원준_204안타_1007_KT제공", "힐리어드T": "경기/힐리어드_타격_1011_KT제공", "최원태C": "경기/최원태_경기_삼성제공_세로", "힐리어드D": "경기/힐리어드_하늘가리키기_KT제공", "힐리어드C": "경기/힐리어드_하이파이브_1011_KT제공", "최원준C": "경기/최원준_두검지_1006_KT제공",
    "김지찬": "상황별/김지찬_상체", "김지찬B": "상황별/김지찬_홈충돌", "박승규": "상황별/박승규_타격_0830_삼성제공", "구자욱": "경기/구자욱_적시타세리머니_스타뉴스",
    "최형우": "경기/최형우_만루포미소_0826_삼성제공_세로", "최형우B": "경기/최형우_100타점_0918_삼성제공_중앙_세로", "최형우C": "카드/G18_최형우_미소",
    "강민호": "상황별/강민호_3점포_중앙", "강민호B": "카드/G18_강민호_포수", "이재현": "상황별/이재현_상체", "류지혁": "카드/G18_류지혁_A",
    "올러": "카드/P18_올러_투구", "올러B": "경기/올러_경기_KIA제공_세로", "양현종": "경기/양현종_글러브_1012_KIA제공",
    "하주석": "카드/P22_하주석_타격", "디아즈": "카드/FA9_디아즈_경기", "디아즈B": "경기/디아즈_경기_삼성제공", "디아즈C": "카드/G18_디아즈_B", "박재현": "경기/박재현_주루_KIA제공",
    "나성범": "경기/나성범_세리머니_KIA제공", "김선빈": "카드/P17_김선빈", "한준수": "경기/한준수_주루_KIA제공", "한준수B": "카드/P18_한준수_세리머니", "김도영": "경기/김도영_덕아웃_KIA제공",
    "카스트로": "경기/카스트로_엄지_0810_KIA제공",
    "후라도": "카드/P20_후라도_투구", "후라도B": "경기/후라도_경기_1019_삼성제공", "후라도C": "경기/후라도_경기_삼성제공", "후라도D": "경기/후라도_박수_삼성제공_세로", "후라도E": "카드/FA9_후라도",
    "이승민": "카드/P31_이승민_삼성제공", "원태인": "경기/원태인_투구_0828_삼성제공_세로", "원태인B": "경기/원태인_포효_스타뉴스", "원태인C": "경기/원태인_역투_삼성제공",
    "김재윤": "경기/김재윤_투구_1007_삼성제공", "페덱": "경기/페덱_포효_연합뉴스", "페덱B": "경기/페덱_환호_삼성제공", "페덱C": "경기/페덱_사용자제공_1004", "힐리어드C": "경기/힐리어드_하이파이브_1011_KT제공", "힐리어드D": "경기/힐리어드_하늘가리키기_KT제공", "최원준C": "경기/최원준_두검지_1006_KT제공", "최원태": "경기/최원태_경기_삼성제공_세로", "최원태B": "상황별/최원태_KIA전_0908_삼성제공",
    "박진만": "경기/박진만_박수_0908_삼성제공", "이범호": "경기/이범호_박수_0915_KIA제공_세로", "이강철": "경기/이강철_덕아웃_KT제공", "이강철B": "경기/이강철_상체_스포츠조선",
    "대니엘": "경기/대니엘_역투_스포츠경향", "대니엘B": "경기/대니엘_주먹_KT제공", "대니엘C": "카드/FA9원_대니엘",
    "힐리어드": "경기/힐리어드_포효_KT제공_1280", "최원준": "경기/최원준_역전타_KT제공", "스기모토": "경기/스기모토_역투_스포츠경향",
}
def pc(img, name, team, note="", **x): return dict({"img": P.get(img, img), "name": name, "team": team, "note": note}, **x)
def PEO(title, items, **k): return S(0, "people", title=title, items=items, size=k.pop('size', 100), **k)
def PL(img, name, team, res, kind, at, **k): return dict(dict(name=name, img=P.get(img, img), team=team, res=res, kind=kind, at=at), **k)
def TA(k, v, at, hi=False): return dict(k=k, v=v, at=at, hi=hi)
def RL(title, plays, tally, **k): return S(0, "rally", title=title, plays=plays, tally=tally, noCenter=True, **k)
def BARS(title, items, mx, **k): return S(0, "bars", title=title, items=items, max=mx, noCenter=True, **k)
def TL(title, items, **k): return S(0, "tline", title=title, items=items, noCenter=True, **k)
def Q(text, logos, **k): return S(0, "question", text=text, logos=logos, logoSize=k.pop('logoSize', 200), size=k.pop('size', 96), **k)
def SCALE(title, left, right, tilt, **k): return S(0, "scale", title=title, left=left, right=right, tilt=tilt, noCenter=True, **k)
def HERO(img, name, team, kicker, stats, **k): return S(0, "hero", img=P.get(img, img), name=name, team=team, kicker=kicker, stats=stats, noCenter=True, **k)
def ST(k, v, at, hi=False, **x): return dict(dict(k=k, v=v, at=at, hi=hi), **x)
def FC(img, name, team, role, at, **x): return dict(dict(img=P.get(img, img), name=name, team=team, role=role, at=at), **x)
def FACES(items, **k): return S(0, "faces", items=items, noCenter=True, **k)
def G(n, venue, home, win, at): return dict(n=n, venue=venue, home=home, win=win, at=at)
def SER(title, games, **k): return S(0, "series5", title=title, games=games, noCenter=True, **k)

# 5차전 점수판 (대구 · KIA 원정 위, 삼성 아래)
KIA5 = [0, 0, 1, 0, 0, 0, 0, 0, 0]; SS5 = [1, 3, 0, 0, 0, 2, 0, 0, None]
def box(hi=(), marks=(), upto=9, label=None, labelAt=0.5, cont=True, sup=None, **k):
    sup = upto if sup is None else sup
    kr = [v if j < upto else None for j, v in enumerate(KIA5)]; sr = [v if j < sup else None for j, v in enumerate(SS5)]
    d = dict(title="플레이오프 5차전 · 대구", rows=[{"team": "KIA", "runs": kr, "r": sum(v for v in kr if v)}, {"team": "삼성", "runs": sr, "r": sum(v for v in sr if v), "hi": True}], hi=list(hi), marks=list(marks), chain="box5")
    if label: d.update(label=label, labelAt=labelAt)
    if cont: d['cont'] = True
    d.update(k)
    return S(0, "scoreboard", **d)
PO = [("1차전", "대구", "삼성", "KIA"), ("2차전", "대구", "삼성", "삼성"), ("3차전", "광주", "KIA", "삼성"), ("4차전", "광주", "KIA", "KIA"), ("5차전", "대구", "삼성", "삼성")]

SC = {}
GM = [dict(g=1, place="수원", venue="KT"), dict(g=2, place="수원", venue="KT"), dict(g=3, place="대구", venue="삼성"), dict(g=4, place="대구", venue="삼성"),
      dict(g=5, place="대구", venue="삼성"), dict(g=6, place="수원", venue="KT"), dict(g=7, place="수원", venue="KT")]
DAYS = [dict(d="화", g=1, place="수원", venue="KT"), dict(d="수", g=2, place="수원", venue="KT"), dict(d="목", off=True), dict(d="금", g=3, place="대구", venue="삼성"),
        dict(d="토", g=4, place="대구", venue="삼성"), dict(d="일", g=5, place="대구", venue="삼성"), dict(d="월", off=True), dict(d="화", g=6, place="수원", venue="KT"), dict(d="수", g=7, place="수원", venue="KT")]
def sched(sp=None, brackets=None, **k): return S(0, "ks_sched", title="2026 한국시리즈 일정", days=DAYS, sp=sp, brackets=brackets or [], chain="sch", **k)
# 경기별 변수(1~7차전)
STEPS = [dict(lab="수원 +4 · 대구 −4", d=[4, 4, -4, -4, -4, 4, 4], mix=True), dict(lab="1차전 공백 −5", d=[-5, 0, 0, 0, 0, 0, 0], neg=True),
         dict(lab="삼성 불펜 피로 +2", d=[2, 2, 0, 0, 0, 0, 0]), dict(lab="세이브왕 공백 +3", d=[3] * 7), dict(lab="삼성 선발 사흘 휴식 +6", d=[0, 0, 0, 6, 6, 6, 6])]
FIN = ["47.75", "52.75", "42.75", "48.75", "48.75", "56.75", "56.75"]
def prob7(ats, **k):
    st = [dict(x, at=a) for x, a in zip(STEPS, ats)]
    return S(0, "ks_prob7", title="경기별 KT 승리 확률", games=GM, base=43.75, steps=st, chain="p7", final=FIN, **k)
OUTS = [dict(team="KT", outs=[dict(k="4승 0패", v=5.249), dict(k="4승 1패", v=11.21), dict(k="4승 2패", v=17.064), dict(k="4승 3패", v=17.811)]),
        dict(team="삼성", outs=[dict(k="4승 0패", v=7.244), dict(k="4승 1패", v=13.841), dict(k="4승 2패", v=14.008), dict(k="4승 3패", v=13.574)])]
def outs(his, bracket=None, **k): return S(0, "ks_outs", title="시리즈 결과별 확률", rows=OUTS, his=his, bracket=bracket, chain="outs", max=20, **k)

# ── 오프닝 ──
SC['o1'] = Q("KT 통합 우승?", ["KT"], logoSize=220, size=110)
SC['o2'] = box(cont=False)
SC['o3'] = S(0, "vA_gap", title="KT의 공백", rows=[dict(team="삼성", days=1, lab="하루", at=50, fillAt=50), dict(team="KT", days=21, lab="22일 만", at=0, fillAt=1.0)], legendAt=50)
SC['o4'] = S(0, "toc", itemFrom=1)
# ── 1. 역대 1위 팀 ──
SC['h0'] = None
SC['h1'] = S(0, "vB_units", title="정규시즌 1위 팀의 한국시리즈", sub="2005~2025", n=21, slotAt=1.0, fillAt=50, fills=["trophy"] * 19 + ["x"] * 2, big=dict(v="19", unit="/ 21번 우승", at=50, c="#B07A00"), chain="u21")
SC['h2'] = S(0, "vB_units", title="정규시즌 1위 팀의 한국시리즈", sub="2005~2025", n=21, slotAt=-1, fillAt=0.3, fills=["trophy"] * 19 + ["x"] * 2, big=dict(v="19", unit="/ 21번 우승", at=0.6, c="#B07A00"), chain="u21", cont=True)
_lost = lambda rows, **k: S(0, "grid", title="1위 팀이 우승을 놓친 해", cols=[dict(team="삼성", label="2015"), dict(team="두산", label="2018")], rows=rows, chain="lost", **k)
SC['h3'] = _lost([], colAt=1.0)
SC['h4'] = S(0, "vB_units", title="2015 삼성 · 빠진 주축 투수", n=3, slotAt=1.0, fillAt=2.0, fills=["x"] * 3, big=dict(v="1승 4패", unit="", at=3.0, c="#E5484D"))
SC['h5'] = _lost([dict(k="시리즈", at=1.0, vals=[dict(t="1승 4패", c="bad"), dict(t="2승 4패", c="bad")])], colAt=-1)
SC['h5b'] = S(0, "grid", title="2018 플레이오프 5차전", cols=[dict(team="", label="SK")], colAt=0, rows=[dict(k="연장", at=1.0, vals=[dict(t="10회", c="")]), dict(k="스코어", at=2.0, vals=[dict(t="11대10", c="bad")])])
SC['h6'] = _lost([dict(k="시리즈", at=-1, vals=[dict(t="1승 4패", c="bad"), dict(t="2승 4패", c="bad")])], colAt=-1, cont=True)
SC['h7'] = _lost([dict(k="시리즈", at=-1, vals=[dict(t="1승 4패", c="bad"), dict(t="2승 4패", c="bad")]), dict(k="상대 휴식", at=1.0, vals=[dict(t="하루", c="bad"), dict(t="하루", c="bad")])], colAt=-1, cont=True)
SC['h8'] = _lost([dict(k="시리즈", at=-1, vals=[dict(t="1승 4패", c="bad"), dict(t="2승 4패", c="bad")]), dict(k="상대 휴식", at=-1, vals=[dict(t="하루", c="bad"), dict(t="하루", c="bad")]), dict(k="1·2차전", at=1.0, vals=[dict(t="1승 1패", c=""), dict(t="1승 1패", c="")])], colAt=-1, cont=True)
SC['h9'] = _lost([dict(k="시리즈", at=-1, vals=[dict(t="1승 4패", c="bad"), dict(t="2승 4패", c="bad")]), dict(k="상대 휴식", at=-1, vals=[dict(t="하루", c="bad"), dict(t="하루", c="bad")]), dict(k="1·2차전", at=-1, vals=[dict(t="1승 1패", c=""), dict(t="1승 1패", c="")]), dict(k="3차전부터", at=0.5, vals=[dict(t="3연패", c="bad"), dict(t="1승 3패", c="bad")])], colAt=-1, cont=True)
SC['h10'] = S(0, "vA_days", title="2026 삼성", team="삼성", days=[dict(date="11/1", k="p", lab="5차전", at=0.5), dict(date="11/2", k="r", lab="", at=1.5), dict(date="11/3", k="g", lab="1차전", at=2.0)])
SC['h11'] = S(0, "vB_units", title="안방 1·2차전을 다 이긴 1위 팀", sub="2005~2025", n=10, slotAt=1.0, fillAt=2.5, fills=["trophy"] * 10, big=dict(v="10", unit="/ 10번 우승", at=3.0, c="#B07A00"))
SC['h12'] = S(0, "vB_units", title="안방 1·2차전을 나눈 1위 팀", sub="2005~2025", n=9, slotAt=0, fillAt=1.0, fills=["trophy"] * 7 + ["x"] * 2, big=dict(v="7", unit="/ 9번 우승", at=1.4, c="#B07A00"))
SC['h13x'] = BARS("1위 팀이 쉰 기간", [dict(label="가장 짧게", value=13, unit="일", at=50), dict(label="가장 길게", value=25, unit="일", at=50)], 26, chain="rest")
SC['h13b'] = S(0, "grid", title="휴식과 우승", cols=[dict(team="KT", label="2021"), dict(team="LG", label="2025")], colAt=1.0, rows=[dict(k="공백", at=1.5, vals=[dict(t="14일 만", c=""), dict(t="25일 만", c="")]), dict(k="결과", at=4.0, vals=[dict(t="우승", c="good", icon="trophy"), dict(t="우승", c="good", icon="trophy")])])
SC['h14'] = S(0, "grid", title="2017 한국시리즈", cols=[dict(team="KIA", label="")], colAt=0, rows=[dict(k="공백", at=0, vals=[dict(t="22일 만", c="")]), dict(k="1차전", at=2.0, vals=[dict(t="패", c="bad")]), dict(k="그 뒤", at=3.0, vals=[dict(t="4연승 우승", c="good", icon="trophy")])])
SC['h15'] = S(0, "vB_units", title="1차전을 진 1위 팀", sub="2005~2025", n=8, slotAt=0, fillAt=1.0, fills=["trophy"] * 7 + ["x"], big=dict(v="7", unit="/ 8번 우승", at=2.0, c="#B07A00"))
SC['h16'] = S(0, "vB_branch", title="1위 팀의 한국시리즈", hubTop="안방", hub="1·2차전", up=dict(team="KT", steps=[dict(icon="score", v="연승", t="\u00a0", at=0.5), dict(icon="score", v="우승", t="대부분", at=1.0, hi=True)]),
              dn=dict(team="삼성", steps=[dict(icon="score", v="반반", t="\u00a0", at=3.0), dict(icon="q", t="이변", at=3.4)]))
SC['k1'] = Q("2026년 KT", ["KT"], logoSize=200, size=104, tr="through")
SC['k2'] = S(0, "vA_streak", z=1.0, title="KT 정규시즌 마지막 10경기", n=10, at=2.0, tagAt=0.5, lab="구단 최다 90승")
SC['k3'] = BARS("KT 정규시즌 승수", [dict(label="2026년", value=90, unit="승", at=0, hi=True, color="#12161F"), dict(label="2021년 첫 우승", value=76, unit="승", at=1.0)], 100)
SC['k4'] = S(0, "vA_rank", title="2026 타선 · 리그 1위", logoAt=0, items=[dict(lab="팀 타율", ic="bat", v="", at=1.0), dict(lab="팀 득점", ic="ball", v="", at=1.2)])
SC['k5'] = HERO("힐리어드", "힐리어드", "KT", "", [ST("타점왕", "139", 0.3, True), ST("홈런 2위", "44개", 1.2)])
SC['k6'] = HERO("최원준", "최원준", "KT", "", [ST("득점왕", "125", 0.3, True)])
SC['k7'] = S(0, "ks_rank", title="2026 팀 홈런 순위", team="KT", n=10, rank=7, at=1.0, note="121개")
SC['k8'] = FACES([FC("고영표", "고영표", "KT", "15승 · 다승 1위", 0.3, keep=True), FC("소형준", "소형준", "KT", "10승 3패 · 승률 1위", 2.0, keep=True)])
SC['k9'] = HERO("대니엘B", "대니엘", "KT", "", [ST("정규시즌", "10경기", 1.0), ST("평균자책점", "2.13", 2.0, True)], chain="dn")
SC['k9b'] = HERO("대니엘B", "대니엘", "KT", "", [ST("상무전", "5이닝", 1.5), ST("피안타", "0개", 2.5), ST("삼진", "10개", 2.5, True)], chain="dn", cont=True)
SC['k9c'] = HERO("대니엘B", "대니엘", "KT", "", [ST("상무전", "5이닝", -1), ST("피안타", "0개", -1), ST("삼진", "10개", -1, True)], chain="dn", cont=True, stamp=dict(t="첫 포스트시즌", at=0.3))
SC['k10'] = sched(sp=[], dayAt=0.3)
SC['k11'] = sched(sp=[], dayAt=-1, cont=True, brackets=[dict(**{"from": 0, "to": 8}, lab="KT 선발 넷 · 나흘 휴식", c="#12161F", at=0.5)])
SC['k12'] = S(0, "vA_saves", z=1.15, title="KT 마무리 · 2026 정규시즌", n=30, at=0.2, v="30", vl="세이브", eraAt=1.0, eraLab="평균자책점", era="2.48")
SC['k13'] = S(0, "mu_pstat", title="2026 홀드왕", img=P["스기모토"], name="스기모토", team="KT", at=1.0, n=25, iconLab="홀드", iconAt=0.3, era=5.90, eraAt=1.0)
SC['k13b'] = FACES([FC("이강철", "이강철", "KT", "", 0, say="감각 유지가 아니라\n찾는 것", sayAt=2.0)], chain="lk")
SC['k13c'] = S(0, "vA_games", z=1.0, title="연습경기", games=[dict(date="10월 27일", opp="상무", badge="army", a="7", b="0", at=0.5, scAt=1.0)])
SC['k14'] = S(0, "grid", title="2021 KT 한국시리즈", cols=[dict(team="KT", label="")], colAt=0.3, chain="k21", rows=[dict(k="공백", at=50, vals=[dict(t="14일 만", c="")]), dict(k="상대", at=50, vals=[dict(t="두산", c="")]), dict(k="시리즈", at=50, vals=[dict(t="4전 전승", c="good", icon="trophy")])])
SC['k15'] = S(0, "grid", title="2021 한국시리즈", cols=[dict(team="KT", label="")], colAt=0, rows=[dict(k="공백", at=1.0, vals=[dict(t="14일 만", c="")]), dict(k="상대", at=2.0, vals=[dict(t="두산", c="")]), dict(k="시리즈", at=2.5, vals=[dict(t="4전 전승", c="good", icon="trophy")])])
SC['k16'] = FACES([FC("이강철B", "이강철", "KT", "", 1.0)])
SC['k17'] = S(0, "vA_tiles", z=1.15, title="2026 KT 정리", items=[dict(lab="타선", ic="bat", c="good", at=1.0), dict(lab="선발", ic="pitcher", c="good", at=1.0), dict(lab="장타", ic="bat", c="bad", at=2.0), dict(lab="중간 불펜", ic="pen", c="bad", at=3.0)])
# ── 3. 삼성 ──
SC['s1'] = Q("삼성의 남은 힘", ["삼성"], logoSize=200, size=104, tr="through")
SC['s2'] = S(0, "vB_only", title="정규시즌 상대 전적", me="KT", opps=["KIA", "LG", "NC", "SSG", "두산", "롯데", "키움", "한화", "삼성"], hit="삼성", oppAt=0.6, hitAt=2.5, badge="유일한 열세")
SC['s3'] = S(0, "mu_blocks", title="2026 정규시즌 맞대결", chain="bl", groups=[dict(team="삼성", n=9, at=0), dict(team="KT", n=3, at=0), dict(team="KT", n=4, at=0.5, hi=True)], tally=dict(at=0, items=[dict(team="삼성", v="9", u="승"), dict(team="KT", v="7", u="승")]), runs=dict(at=50, label="", items=[dict(team="KT", v=27), dict(team="삼성", v=8)]))
SC['s4'] = S(0, "vA_units", title="플레이오프 · 삼성 투수 등판", team="삼성", groups=[dict(g="1차전", n=5), dict(g="2차전", n=3), dict(g="3차전", n=7), dict(g="4차전", n=6), dict(g="5차전", n=3)], at=0.3, fillAt=1.0, totAt=50, v="\u00a0", vl="", chain="un")
SC['s5'] = S(0, "vA_units", title="플레이오프 · 삼성 투수 등판", team="삼성", groups=[dict(g="1차전", n=5), dict(g="2차전", n=3), dict(g="3차전", n=7), dict(g="4차전", n=6), dict(g="5차전", n=3)], at=-1, fillAt=-1, totAt=0.4, v="24", vl="번", chain="un", cont=True)
SC['s5b'] = FACES([FC("이승민", "이승민", "삼성", "다섯 경기 모두 등판", 0, keep=True)])
SC['s6'] = FACES([FC("김재윤", "김재윤", "삼성", "", 0.5), FC("원태인B", "원태인", "삼성", "", 2.5)])
SC['s7'] = FACES([FC("최원태C", "최원태", "삼성", "", 1.0), FC("페덱B", "페덱", "삼성", "", 1.0), FC("후라도D", "후라도", "삼성", "", 2.0)], chain="sp3")
SC['s7b'] = FACES([FC("최원태C", "최원태", "삼성", "플레이오프 3차전 1⅔이닝", -1, keep=True), FC("페덱B", "페덱", "삼성", "플레이오프 4차전 5⅓이닝", -1, keep=True), FC("후라도C", "후라도", "삼성", " ", -1, keep=True)], chain="sp3", cont=True)
SC['s7c'] = FACES([FC("박진만", "박진만", "삼성", "", 0, say="5차전엔 두 선발만 빼고\n불펜 총동원", sayAt=1.0)])
SC['s8'] = sched(sp=[dict(g=1, name="최원태", rest="", at=2.0), dict(g=2, name="페덱", rest="", at=3.0), dict(g=3, name="후라도", rest="", at=3.2)], spAt=2.0, dayAt=0)
SC['s9'] = sched(sp=[dict(g=1, name="최원태", rest="", at=-1), dict(g=2, name="페덱", rest="", at=-1), dict(g=3, name="후라도", rest="", at=-1)], spAt=-1, dayAt=-1)
SC['s10'] = sched(sp=[dict(g=1, name="최원태", rest="", at=-1), dict(g=2, name="페덱", rest="", at=-1), dict(g=3, name="후라도", rest="", at=-1)], spAt=-1, dayAt=-1, cont=True,
                  brackets=[dict(**{"from": 3, "to": 5}, lab="대구 3연전", at=3.0)])
SC['s11'] = sched(sp=[dict(g=1, name="최원태", rest="", at=-1), dict(g=2, name="페덱", rest="", at=-1), dict(g=3, name="후라도", rest="", at=-1),
                      dict(g=4, name="최원태", rest="사흘", bad=True, at=1.0), dict(g=5, name="페덱", rest="사흘", bad=True, at=1.4), dict(g=6, name="후라도", rest="사흘", bad=True, at=2.0), dict(g=7, name="최원태", rest="사흘", bad=True, at=2.4)],
                  spAt=-1, dayAt=-1, cont=True, brackets=[dict(**{"from": 4, "to": 8}, lab="4차전부터 사흘 휴식", at=2.6)])
SC['s12'] = HERO("원태인", "원태인", "삼성", "", [ST("지금", "마무리", 0), ST("선발로 가면", "뒷문 공백", 0.4, True)])
SC['s13'] = HERO("후라도D", "후라도", "삼성", "2026 정규시즌 KT전", [ST("등판", "세 경기", 1.0), ST("평균자책점", "5.17", 2.0, True), ST("피홈런", "4개", 2.6)], chain="hd")
SC['s13b'] = HERO("후라도B", "후라도", "삼성", "", [ST("5차전", "7이닝", 1.0), ST("투구", "95구", 1.0, True)], stamp=dict(t="플레이오프 MVP", at=2.0))
SC['s13c'] = S(0, "vA_errs", title="플레이오프 실책", items=[dict(g="4차전", n=3, slots=3, v="3개", at=1.0), dict(g="5차전", n=2, slots=3, v="2개", at=1.3)])
SC['s13d'] = FACES([FC("박진만", "박진만", "삼성", "", 0, say="작은 수비 하나가\n승부를 좌우", sayAt=2.0)])
SC['s14'] = Q("삼성의 한 방", ["삼성"], logoSize=160, size=90)
SC['s15'] = PEO("플레이오프 홈런", [pc("디아즈B", "디아즈", "삼성", "2개", at=1.0), pc("최형우", "최형우", "삼성", "2개", at=1.0)], size=110, text="합작 4개", textAt=2.6)
SC['s16'] = S(0, "mu_fly", title="2026 정규시즌 팀 홈런", lt="KT", rt="삼성", rows=[dict(k="", l=121, r=140, worse="l", at=0.5)])
SC['s17'] = S(0, "vA_tiles", z=1.15, title="2026 삼성 정리", items=[dict(lab="상대전적", ic="glove", c="good", at=1.0), dict(lab="장타", ic="bat", c="good", at=1.0), dict(lab="선발", ic="pitcher", c="bad", at=2.0)])
# ── 4. 시리즈를 가를 장면 ──
SC['v1'] = Q("시리즈를 가를 장면", ["KT", "삼성"], logoSize=180, size=104, tr="through")
SC['v2'] = S(0, "vB_three", title="시리즈를 가를 세 장면", items=[dict(n="첫째", icon="glove", k="수원 1·2차전", c="#12161F", at=0), dict(n="둘째", icon="bat", k="대구 3차전", c="#074CA1", at=50), dict(n="셋째", icon="pen", k="7회 이후", c="#F08C00", at=50)], chain="v3")
SC['v3'] = S(0, "vB_units", title="안방 1·2차전을 다 이긴 1위 팀", sub="2005~2025", n=10, slotAt=0, fillAt=0.5, fills=["trophy"] * 10, big=dict(v="10", unit="/ 10번 우승", at=1.5, c="#B07A00"))
SC['v4'] = S(0, "vA_gap", title="KT의 공백", rows=[dict(team="KT", days=21, lab="22일 만", at=0, fillAt=0)], legendAt=50)
SC['v5'] = FACES([FC("이강철", "이강철", "KT", "", 0, say="두 경기 정도는\n투수들로 버틴다", sayAt=1.5)])
SC['v6'] = S(0, "vB_three", title="시리즈를 가를 세 장면", items=[dict(n="첫째", icon="glove", k="수원 1·2차전", c="#12161F", at=-1), dict(n="둘째", icon="bat", k="대구 3차전", c="#074CA1", at=0), dict(n="셋째", icon="pen", k="7회 이후", c="#F08C00", at=50)], chain="v3b")
SC['v7'] = HERO("후라도C", "후라도", "삼성", "", [ST("3차전", "대구", 1.0), ST("휴식", "나흘", 0.5, True)])
SC['v8'] = S(0, "vA_games", z=1.0, title="시즌 막판 대구 원정", games=[dict(date="10월 11일", opp="삼성", badge="", a="12", b="3", at=1.0, scAt=2.0), dict(date="10월 12일", opp="삼성", badge="", a="4", b="2", at=1.0, scAt=3.0)])
SC['v8b'] = S(0, "mu_streak", title="시즌 막판 삼성전", img=P["힐리어드D"], name="힐리어드", team="KT", chain="hs", at=0, bracket="3연타석 홈런", bracketAt=2.0,
               games=[dict(d="10월 7일", vs="삼성", abs=[dict(k="hr", t="만루", streak=True)], at=1.0), dict(d="10월 11일", vs="삼성", abs=[dict(k="hr", t=" ", streak=True), dict(k="hr", t=" ", streak=True)], at=1.0)])
SC['v9'] = sched(sp=[dict(g=3, name="후라도", rest="나흘", at=0), dict(g=4, name="최원태", rest="사흘", bad=True, at=1.0), dict(g=5, name="페덱", rest="사흘", bad=True, at=1.2), dict(g=6, name="후라도", rest="사흘", bad=True, at=1.4), dict(g=7, name="최원태", rest="사흘", bad=True, at=1.6)], spAt=0, dayAt=0, brackets=[dict(**{"from": 4, "to": 8}, lab="4차전부터 사흘 휴식", at=1.8)])
SC['v10'] = S(0, "vB_three", title="시리즈를 가를 세 장면", items=[dict(n="첫째", icon="glove", k="수원 1·2차전", c="#12161F", at=-1), dict(n="둘째", icon="bat", k="대구 3차전", c="#074CA1", at=-1), dict(n="셋째", icon="pen", k="7회 이후", c="#F08C00", at=0)], chain="v3c")
SC['v11'] = S(0, "vA_innings", z=1.05, title="셋째 · 7회 이후", team="KT", segs=[dict(frm=1, to=6, lab="선발", at=0), dict(frm=7, to=9, lab="불펜 싸움", c="#E5484D", at=0.5)], v="\u00a0", vn=0, vAt=50)
SC['v12'] = S(0, "vA_tiles", z=1.15, title="선발 싸움", items=[dict(lab="KT 선발 · 나흘 휴식", ic="pitcher", c="good", at=1.0), dict(lab="삼성 선발 · 사흘 휴식", ic="pitcher", c="bad", at=1.0)])
SC['p1'] = Q("KT 우승 확률", ["KT"], logoSize=200, size=104, tr="through")
SC['p2'] = prob7([50, 50, 50, 50, 50], baseLabAt=50)
SC['p3'] = prob7([50, 50, 50, 50, 50], baseLabAt=2.0, cont=True)
SC['p4'] = prob7([0.5, 50, 50, 50, 50], baseLabAt=-1, cont=True)
SC['p5'] = prob7([-1, 0.3, 50, 50, 50], baseLabAt=-1, cont=True)
SC['p5b'] = S(0, "vB_rings", title="1위 팀의 한국시리즈 승률", sub="2005~2025", items=[dict(k="1차전", v=61.9, dec=1, c="#E5484D", at=0.5), dict(k="2차전", v=76.1, dec=1, c="#16A34A", at=1.5)])
SC['p6'] = prob7([-1, -1, 1.0, 50, 50], baseLabAt=-1)
SC['p7'] = prob7([-1, -1, -1, 0.5, 50], baseLabAt=-1, cont=True)
SC['p8'] = prob7([-1, -1, -1, -1, 1.0], baseLabAt=-1, cont=True)
SC['p8b'] = S(0, "vA_battery", title="선발 휴식과 구위", items=[dict(lab="나흘 휴식", lvl=0.7, c="good", at=0.3), dict(lab="사흘 휴식", lvl=0.32, c="bad", at=1.0)])
SC['p9'] = prob7([-1] * 5, baseLabAt=-1, valAt=0, hi=[dict(g=1, at=0), dict(g=2, at=1.0)])
SC['p10'] = prob7([-1] * 5, baseLabAt=-1, valAt=-1, hi=[dict(g=3, at=0, c="#E5484D"), dict(g=4, at=2.0), dict(g=5, at=2.0)], cont=True)
SC['p11'] = prob7([-1] * 5, baseLabAt=-1, valAt=-1, hi=[dict(g=6, at=1.0, c="#16A34A"), dict(g=7, at=1.0, c="#16A34A")], cont=True)
SC['p12'] = S(0, "vB_split", title="KT 한국시리즈 우승 확률", l="KT", r="삼성", from_=50, to=51.33, moveAt=1.0, label=dict(v="51.33", at=2.0), chain="sp")
SC['p13'] = S(0, "vB_split", title="KT 한국시리즈 우승 확률", l="KT", r="삼성", from_=51.33, to=51.33, moveAt=-1, label=dict(v="51.33", at=-1), rlabel=dict(v="48.66", at=0), chain="sp", cont=True)
SC['p14'] = outs([dict(team="KT", i=3, lab="가장 높음", at=1.0)], bracket=dict(lab="7차전까지 31.38%", at=3.0))
SC['p14b'] = outs([dict(team="KT", i=3, lab="가장 높음", at=-1), dict(team="삼성", i=2, lab="14.00%", c="#074CA1", at=1.0)], bracket=dict(lab="7차전까지 31.38%", at=-1), cont=True)
SC['p14c'] = S(0, "vB_units", title="수원 두 경기 모두 KT 승리", n=2, slotAt=0, fillAt=1.0, fills=["win", "win"], big=dict(v="25.18%", unit="", at=2.0, c="#12161F"))
SC['p15'] = S(0, "vB_meter", title="7차전 끝 KT 우승", l="KT", r="삼성", from_=0, to=-0.25, moveAt=1.0, lBadge=dict(t="7차전 끝", at=1.5), crown=dict(side="l", at=2.0), tr="through")
SC['p16'] = BARS("수원 1·2차전 뒤 KT 우승 확률", [dict(label="2연승", value=82.35, unit="%", dec=2, at=50), dict(label="1승 1패", value=51.41, unit="%", dec=2, at=50), dict(label="2연패", value=19.52, unit="%", dec=2, at=50)], 100, chain="c12")
SC['p17'] = BARS("수원 1·2차전 뒤 KT 우승 확률", [dict(label="2연승", value=82.35, unit="%", dec=2, at=2.0, color="#12161F"), dict(label="1승 1패", value=51.41, unit="%", dec=2, at=3.0), dict(label="2연패", value=19.52, unit="%", dec=2, at=4.0, color="#E5484D")], 100)
SC['p17b'] = BARS("1승 1패 뒤 대구 3차전", [dict(label="3차전 승", value=72.84, unit="%", dec=2, at=2.0, color="#12161F"), dict(label="3차전 패", value=35.41, unit="%", dec=2, at=3.0, color="#E5484D")], 100)
SC['p17c'] = _lost([dict(k="1·2차전", at=0.5, vals=[dict(t="1승 1패", c=""), dict(t="1승 1패", c="")]), dict(k="결과", at=1.0, vals=[dict(t="이변", c="bad"), dict(t="이변", c="bad")])], colAt=0)
SC['q1'] = Q("KT 통합 우승?", ["KT", "삼성"], logoSize=200, size=110, chain="q")
SC['q2'] = Q("KT 통합 우승?", ["KT", "삼성"], logoSize=200, size=110, chain="q", cont=True)
SC['k8b'] = HERO("고영표B", "고영표", "KT", "2026 정규시즌 삼성전", [ST("등판", "네 경기", 1.0), ST("승패", "3승 1패", 2.0), ST("평균자책점", "2.25", 3.0, True)])
SC['k16b'] = HERO("김현수", "김현수", "KT", "", [ST("한국시리즈 반지", "세 개", 1.0, True), ST("2025 한국시리즈", "MVP", 2.5), ST("2026 정규시즌", "14홈런 95타점", 4.0)], chain="khs")
SC['k16c'] = FACES([FC("김현수", "김현수", "KT", "", -1, say="모두가 서로를\n내려놓지 않는 게 장점", sayAt=1.0)])
SC['s12b'] = FACES([FC("박진만", "박진만", "삼성", "", 0, say="원태인 몸 상태 확인 중", sayAt=1.0)])
SC['s15b'] = HERO("디아즈", "디아즈", "삼성", "2026 정규시즌", [ST("홈런", "26", 1.0), ST("타점", "129", 1.0, True)])
SC['p11b'] = S(0, "vB_next", title="계산이 바뀌는 때", steps=[dict(icon="cal", big="11/2", t="미디어데이", at=1.0), dict(icon="pitchers", t="선발 순서", at=1.5), dict(icon="trophy", t="우승 확률", at=2.0, hi=True)])
SC['k4'] = S(0, "vA_rank", title="2026 타선 · 리그 1위", logoAt=0, items=[dict(lab="팀 타율", ic="bat", v="", at=0.3), dict(lab="팀 득점", ic="ball", v="", at=0.5)])
SC['k4b'] = S(0, "ks_rank", title="2026 팀 홈런 순위", team="KT", n=10, rank=7, at=0.4)
SC['k5'] = S(0, "ks_rank", title="2026 팀 평균자책점 순위", team="KT", n=10, rank=2, at=1.0, note="4.14")
SC['k9'] = HERO("대니엘B", "대니엘", "KT", "", [ST("포스트시즌", "첫 무대", 1.0, True)])
SC['k11b'] = sched(sp=[dict(g=1, name="1선발", rest="", at=0), dict(g=2, name="2선발", rest="", at=1.0), dict(g=5, name="1선발", rest="나흘", at=0.5), dict(g=6, name="2선발", rest="닷새", at=1.5)], spTeam="KT", spAt=0, dayAt=-1, cont=True, brackets=[dict(**{"from": 0, "to": 8}, lab="KT 선발 넷 · 나흘 휴식", c="#12161F", at=-1)])
SC['s4'] = S(0, "vA_units", title="플레이오프 · 삼성 투수 등판", team="삼성", groups=[dict(g="1차전", n=5), dict(g="2차전", n=3), dict(g="3차전", n=7), dict(g="4차전", n=6), dict(g="5차전", n=3)], at=1.0, fillAt=2.0, totAt=50, v="\u00a0", vl="")
SC['s6b'] = S(0, "ks_rank", title="2026 팀 세이브 순위", team="삼성", n=10, rank=2, at=0.5, note="42개")
SC['s7'] = FACES([FC("최원태C", "최원태", "삼성", "", 1.0), FC("페덱B", "페덱", "삼성", "", 1.0), FC("후라도D", "후라도", "삼성", "", 2.0)])
SC['s12c'] = HERO("원태인B", "원태인", "삼성", "2026 정규시즌 KT전", [ST("등판", "다섯 경기", 0.5), ST("평균자책점", "3.25", 1.0, True)])
SC['v1'] = Q("차전별 맞대결", ["KT", "삼성"], logoSize=180, size=104, tr="through")
SC['v2'] = FACES([FC("대니엘", "대니엘", "KT", "", 0), FC("최원태", "최원태", "삼성", "KT전 평균자책점 6.94", 0, keep=True)])
SC['v3a'] = FACES([FC("고영표", "고영표", "KT", "", 1.0)])
SC['v3'] = PEO("삼성 중심 타선 · 모두 왼손", [pc("구자욱", "구자욱", "삼성", "\u00a0", at=1.0), pc("디아즈", "디아즈", "삼성", "\u00a0", at=1.0), pc("최형우", "최형우", "삼성", "\u00a0", at=1.0)], size=100, chain="lefty")
SC['v3b'] = PEO("삼성 중심 타선 · 모두 왼손", [pc("구자욱", "구자욱", "삼성", "KT전 3할 3푼 3리", at=-1), pc("디아즈", "디아즈", "삼성", "\u00a0", at=-1), pc("최형우", "최형우", "삼성", "\u00a0", at=-1)], size=100, chain="lefty", cont=True)
SC['v4'] = FACES([FC("이강철B", "이강철", "KT", "", 0, say="요즘엔 사이드암이\n좌타자를 더 잘 잡는다", sayAt=1.0)])
SC['v5'] = HERO("고영표B", "고영표", "KT", "2026 정규시즌 삼성전", [ST("등판", "네 경기", 1.0), ST("승패", "3승 1패", 2.0), ST("평균자책점", "2.25", 3.0, True)])
SC['v6'] = HERO("후라도C", "후라도", "삼성", "", [ST("3차전", "대구", 0.5), ST("휴식", "나흘", 0.3, True)])
SC['v7'] = FACES([FC("후라도D", "후라도", "삼성", "KT전 평균자책점 5.17", 0.3, keep=True), FC("힐리어드", "힐리어드", "KT", "삼성전 3할 4리 · 홈런 5개", 2.0, keep=True)])
SC['v8'] = FACES([FC("힐리어드C", "힐리어드", "KT", "홈런 두 개 · 5타점", 0, keep=True), FC("후라도B", "후라도", "삼성", "4이닝 6실점", 3.0, keep=True)])
SC['p10b'] = BARS("대구 3연전 KT", [dict(label="2승 이상", value=45.12, unit="%", dec=2, at=1.0, color="#12161F"), dict(label="1승 2패", value=39.83, unit="%", dec=2, at=3.0)], 100)
SC['k8c'] = S(0, "ks_rank", title="배제성 · 2026 정규시즌", team="KT", n=1, rank=1, at=50)
SC['k12'] = FACES([FC("이강철", "이강철", "KT", "", 0, say="타자들 컨디션 괜찮다\n이제서야 분위기가 난다", sayAt=2.0)])
SC['v9b'] = sched(sp=[dict(g=3, name="후라도", rest="나흘", at=-1), dict(g=4, name="최원태", rest="사흘", bad=True, at=-1), dict(g=5, name="페덱", rest="사흘", bad=True, at=-1), dict(g=6, name="후라도", rest="사흘", bad=True, at=-1), dict(g=7, name="최원태", rest="사흘", bad=True, at=-1)], spAt=-1, dayAt=-1, cont=True, brackets=[dict(**{"from": 7, "to": 7}, lab="에이스도 사흘", at=0.5)])
SC['p13b'] = S(0, "vB_rings", title="우승 확률 비교", items=[dict(k="역대 1위 팀", v=90.4, dec=1, c="#B07A00", at=1.0), dict(k="2026 KT", v=51.33, dec=2, c="#12161F", at=0.5)])
SC['p14d'] = outs([dict(team="KT", i=3, lab="가장 높음", at=-1), dict(team="삼성", i=2, lab="14.00%", c="#074CA1", at=-1), dict(team="KT", i=0, lab="5.24%", c="#12161F", at=1.0), dict(team="삼성", i=0, lab="7.24%", c="#074CA1", at=2.0)], bracket=dict(lab="7차전까지 31.38%", at=-1), cont=True)
SC['p17d'] = BARS("2연승 뒤 대구 3차전", [dict(label="3차전 승", value=95.08, unit="%", dec=2, at=3.0, color="#12161F")], 100)
SC['v9c'] = HERO("최원태C", "최원태", "삼성", "", [ST("4차전", "사흘 휴식", 1.2, True), ST("플레이오프 3차전", "1⅔이닝", 2.5)], imgAt=1.0)
SC['p15b'] = sched(sp=None, dayAt=0, brackets=[dict(**{"from": 0, "to": 1}, lab="1승 1패", c="#3B4A63", at=1.0), dict(**{"from": 3, "to": 5}, lab="1승 2패", c="#E5484D", at=2.0), dict(**{"from": 7, "to": 8}, lab="2연승", c="#12161F", at=3.0)])

# ── 11/2 검수 2차 반영 ──
SC['o1'] = Q("통합 우승?", ["KT"], logoSize=220, size=110)
SC['k1'] = Q("2026년 전력", ["KT"], logoSize=200, size=104, tr="through")
SC['s1'] = Q("남은 힘", ["삼성"], logoSize=200, size=104, tr="through")
SC['p1'] = Q("우승 확률", ["KT"], logoSize=200, size=104, tr="through")
SC['q1'] = Q("우승은 어디로?", ["KT", "삼성"], logoSize=200, size=110, chain="q")
SC['q2'] = Q("우승은 어디로?", ["KT", "삼성"], logoSize=200, size=110, chain="q", cont=True)
SC['h4'] = S(0, "vB_units", title="2015 삼성 · 빠진 주축 투수", n=3, slotAt=1.0, fillAt=2.0, fills=["outp"] * 3, big=dict(v="1승 4패", unit="", at=3.0, c="#E5484D"))
SC['h10'] = S(0, "vA_days", title="2026 삼성", team="삼성", days=[dict(date="일", k="p", lab="5차전", at=0.5), dict(date="월", k="r", lab="", at=1.5), dict(date="화", k="g", lab="1차전", at=2.0)])
SC['k13'] = S(0, "mu_pstat", title="홀드왕", img=P["스기모토"], name="스기모토", team="KT", at=1.0, n=25, iconLab="홀드", iconAt=2.0, era=5.90, eraAt=2.3)
SC['k16c'] = HERO("김현수", "김현수", "KT", "", [], quote=dict(t="모두가 서로를 내려놓지 않는 게\n우리 팀의 장점", at=2.0))
SC['s2'] = S(0, "vB_only", title="정규시즌 상대 전적", me="KT", opps=["KIA", "LG", "NC", "SSG", "두산", "롯데", "키움", "한화", "삼성"], hit="삼성", oppAt=0.6, hitAt=1.0, badge="7승 9패")
SC['s4'] = FACES([FC("이승민", "이승민", "삼성", "플레이오프 다섯 경기 모두 등판", 2.0, keep=True)])
SC['s6b'] = S(0, "ks_rank", title="2026 팀 세이브 순위", team="삼성", n=10, rank=2, at=1.0, note="42개")
SC['s7'] = FACES([FC("최원태C", "최원태", "삼성", "", 1.0), FC("페덱C", "페덱", "삼성", "", 1.0), FC("후라도D", "후라도", "삼성", "", 2.0)])
SC['s12'] = HERO("원태인", "원태인", "삼성", "", [ST("지금", "마무리", 0), ST("선발로 가면", "뒷문 공백", 0.4, True)])
SC['s12c'] = HERO("원태인", "원태인", "삼성", "2026 정규시즌 KT전", [ST("등판", "다섯 경기", 1.0), ST("승패", "1승 3패", 2.0), ST("평균자책점", "3.25", 3.0, True)])
SC['s17'] = S(0, "vA_tiles", z=1.15, title="2026 삼성 정리", items=[dict(lab="상대전적", ic="glove", c="good", at=1.0), dict(lab="선발", ic="pitcher", c="bad", at=2.0)])
SC['v3'] = PEO("삼성 중심 타선 · 모두 왼손", [pc("구자욱", "구자욱", "삼성", " ", at=1.0), pc("디아즈", "디아즈", "삼성", " ", at=1.0), pc("최형우C", "최형우", "삼성", " ", at=1.0)], size=100, chain="lefty")
SC['v3b'] = PEO("삼성 중심 타선 · 모두 왼손", [pc("구자욱", "구자욱", "삼성", "KT전 3할 3푼 3리", at=-1), pc("디아즈", "디아즈", "삼성", " ", at=-1), pc("최형우C", "최형우", "삼성", " ", at=-1)], size=100, chain="lefty", cont=True)
SC['v6'] = HERO("후라도C", "후라도", "삼성", "", [ST("3차전", "대구", 2.0), ST("휴식", "나흘", 1.2, True)], imgAt=1.0)
SC['v7'] = FACES([FC("후라도D", "후라도", "삼성", "KT전 평균자책점 5.17", 0.3, keep=True), FC("힐리어드C", "힐리어드", "KT", "삼성전 3할 4리 · 홈런 5개", 3.0, keep=True)])
SC['v8'] = FACES([FC("후라도D", "후라도", "삼성", "", -1, note="4이닝 6실점", noteAt=3.0), FC("힐리어드C", "힐리어드", "KT", "홈런 두 개", -1, keep=True, note="5타점", noteAt=1.0)])
SC['v8c'] = FACES([FC("후라도D", "후라도", "삼성", "", -1, note="4이닝 6실점", noteAt=-1), FC("힐리어드C", "힐리어드", "KT", "홈런 두 개", -1, keep=True, note="5타점", noteAt=-1)])
SC['v9c'] = HERO("최원태B", "최원태", "삼성", "", [ST("4차전", "사흘 휴식", 2.0, True), ST("플레이오프 3차전", "1⅔이닝", 3.5)], imgAt=1.0)
SC['v9b'] = HERO("후라도E", "후라도", "삼성", "", [ST("6차전", "사흘 휴식", 2.0, True)], imgAt=1.0)
SC['v12'] = S(0, "vA_gap", title="선발 휴식", rows=[dict(team="KT", days=4, lab="나흘 이상", at=1.0, fillAt=1.0), dict(team="삼성", days=3, lab="사흘", at=1.5, fillAt=1.5)], goal="등판", legend="쉬는 날", legendAt=1.5)
SC['p5b'] = S(0, "vB_rings", title="1위 팀의 한국시리즈 승률", items=[dict(k="1차전", v=61.9, dec=1, c="#E5484D", at=0.3), dict(k="2차전", v=76.1, dec=1, c="#16A34A", at=1.0)])
SC['p8b'] = HERO("페덱C", "페덱", "삼성", "", [ST("플레이오프 4차전", "사흘 휴식", 1.0), ST("결과", "5⅓이닝 1실점", 2.0, True, size=84)])
SC['p10b'] = BARS("대구 세 경기 · KT 결과별 확률", [dict(label="3승", value=10.15, unit="%", dec=2, at=1.0), dict(label="2승 1패", value=34.96, unit="%", dec=2, at=2.0), dict(label="1승 2패", value=39.83, unit="%", dec=2, at=3.0, color="#12161F"), dict(label="3패", value=15.03, unit="%", dec=2, at=4.0, color="#E5484D")], 100)
SC['p11b'] = S(0, "vB_next", title="계산이 바뀌는 때", steps=[dict(icon="cal", t="미디어데이", at=1.0), dict(icon="pitchers", t="선발 순서", at=1.5), dict(icon="trophy", t="우승 확률", at=2.0, hi=True)])
SC['p14b'] = outs([dict(team="KT", i=3, lab="가장 높음", at=-1), dict(team="삼성", i=2, lab="14%", c="#074CA1", at=1.0)], bracket=dict(lab="7차전까지 31.38%", at=-1), cont=True)
SC['p14d'] = outs([dict(team="KT", i=3, lab="가장 높음", at=-1), dict(team="삼성", i=2, lab="14%", c="#074CA1", at=-1), dict(team="KT", i=0, lab="5.24%", c="#12161F", at=1.0), dict(team="삼성", i=0, lab="7.24%", c="#074CA1", at=2.0)], bracket=dict(lab="7차전까지 31.38%", at=-1), cont=True)
SC['p15'] = S(0, "vB_meter", title="제 예상", l="KT", r="삼성", from_=0, to=-0.25, moveAt=1.0, lBadge=dict(t="7차전 끝", at=1.0), crown=dict(side="l", at=2.0), tr="through")
_GT = "갈림길별 KT 우승 확률"
_B1 = [dict(label="2연승", value=82.35, unit="%", dec=2, color="#12161F"), dict(label="1승 1패", value=51.41, unit="%", dec=2), dict(label="2연패", value=19.52, unit="%", dec=2, color="#E5484D")]
_B2 = [dict(label="1승 1패 뒤\n3차전 승", value=72.84, unit="%", dec=2, color="#12161F"), dict(label="1승 1패 뒤\n3차전 패", value=35.41, unit="%", dec=2, color="#E5484D")]
_B3 = [dict(label="2연승 뒤\n3차전 승", value=95.08, unit="%", dec=2, color="#12161F")]
_A = lambda xs, ats: [dict(x, at=a) for x, a in zip(xs, ats)]
SC['p17'] = BARS(_GT, _A(_B1, [2.0, 3.0, 4.0]), 100, chain="c17")
SC['p17b'] = BARS(_GT, _A(_B1, [-1] * 3) + _A(_B2, [2.0, 3.0]), 100, chain="c17", cont=True)
SC['p17d'] = BARS(_GT, _A(_B1, [-1] * 3) + _A(_B2, [-1] * 2) + _A(_B3, [3.0]), 100, chain="c17", cont=True)
SC['v2b'] = FACES([FC("대니엘", "대니엘", "KT", "평균자책점", -1, note="2.13", noteAt=1.0), FC("최원태", "최원태", "삼성", "KT전 평균자책점 6.94", -1, keep=True)])
SC['v5c'] = HERO("페덱", "페덱", "삼성", "", [ST("8월 29일 KT전", "6이닝 무실점", 3.0, True, size=84), ST("삼진", "7개", 3.5)], imgAt=1.0)

# ── 11/2 검수 3차 반영 ──
SC['h10b'] = S(0, "vB_units", title="5차전 치르고 올라온 팀의 한국시리즈", n=8, slotAt=0.5, fillAt=1.0, fills=["trophy"] * 2 + ["x"] * 6, big=dict(v="2", unit="/ 8번 우승", at=2.0, c="#E5484D"))
SC['k4'] = S(0, "vA_rank", title="2026 타선 · 리그 1위", logoAt=0, items=[dict(lab="팀 타율", ic="bat", v="", at=1.0), dict(lab="팀 득점", ic="ball", v="", at=1.9)])
SC['k11'] = sched(sp=[], dayAt=-1, cont=True, brackets=[dict(**{"from": 0, "to": 8}, lab="KT 선발 넷 · 나흘 이상 휴식", c="#12161F", at=0.5)])
SC['k11b'] = sched(sp=[dict(g=1, name="1선발", rest="", at=0), dict(g=2, name="2선발", rest="", at=1.0), dict(g=5, name="1선발", rest="나흘", at=0.5), dict(g=6, name="2선발", rest="닷새", at=1.5)], spTeam="KT", spAt=0, dayAt=-1, cont=True, brackets=[dict(**{"from": 0, "to": 8}, lab="KT 선발 넷 · 나흘 이상 휴식", c="#12161F", at=-1)])
SC['k12'] = FACES([FC("이강철", "이강철", "KT", "", 0, say="타자들 컨디션 괜찮다\n이제서야 분위기가 난다", sayAt=1.0)])
SC['k17'] = S(0, "vA_tiles", z=1.15, title="2026 KT 정리", items=[dict(lab="타선", ic="bat", c="good", at=1.0), dict(lab="선발", ic="pitcher", c="good", at=1.0), dict(lab="장타", ic="bat", c="bad", at=2.0), dict(lab="불펜", ic="pen", c="bad", at=3.0)])
SC['s4'] = FACES([FC("이승민", "이승민", "삼성", "플레이오프 다섯 경기 모두 등판", 2.0, keep=True)])
SC['s6'] = FACES([FC("김재윤", "김재윤", "삼성", "", 0), FC("원태인B", "원태인", "삼성", "", 2.0)])
SC['s6b'] = S(0, "ks_rank", title="2026 팀 세이브 순위", team="삼성", n=10, rank=2, at=0.5, note="42개")
SC['s11'] = sched(sp=[dict(g=1, name="최원태", rest="", at=-1), dict(g=2, name="페덱", rest="", at=-1), dict(g=3, name="후라도", rest="", at=-1),
                      dict(g=4, name="최원태", rest="사흘", bad=True, at=1.0), dict(g=5, name="페덱", rest="사흘", bad=True, at=1.4), dict(g=6, name="후라도", rest="사흘", bad=True, at=2.0), dict(g=7, name="최원태", rest="사흘", bad=True, at=2.4)],
                  spAt=-1, dayAt=-1, cont=True, brackets=[dict(**{"from": 4, "to": 8}, lab="4차전부터 사흘 휴식", at=2.6)])
SC['v2b'] = HERO("대니엘", "대니엘", "KT", "", [ST("시즌 평균자책점", "2.13", 1.0, True), ST("삼성전", "등판 없음", 2.5)])
SC['v2'] = HERO("최원태B", "최원태", "삼성", "", [ST("KT전 평균자책점", "6.94", 2.0, True), ST("플레이오프 3차전", "1⅔이닝", 3.5)])
SC['v5c'] = HERO("페덱", "페덱", "삼성", "", [ST("2차전", "선발 차례", 1.0), ST("8월 29일 KT전", "6이닝 무실점", 3.0, True, size=84), ST("삼진", "7개", 3.5)], imgAt=1.0)
SC['v7'] = FACES([FC("후라도D", "후라도", "삼성", "KT전 평균자책점 5.17", 0.3, keep=True), FC("힐리어드C", "힐리어드", "KT", "삼성전 3할 4리 · 홈런 5개", 2.0, keep=True)])
SC['v8'] = FACES([FC("후라도D", "후라도", "삼성", "", -1, note="4이닝 6실점", noteAt=1.0), FC("힐리어드C", "힐리어드", "KT", "홈런 두 개", -1, keep=True, note="5타점", noteAt=3.0)])
SC['v12'] = S(0, "vA_gap", title="4차전부터 선발 휴식", rows=[dict(team="KT", days=4, lab="나흘 이상", at=2.0, fillAt=2.0), dict(team="삼성", days=3, lab="사흘", at=1.0, fillAt=1.0)], goal="등판", legend="쉬는 날", legendAt=1.0)
SC['p5b'] = S(0, "vB_rings", title="1위 팀의 한국시리즈 승률", items=[dict(k="1차전", v=61.9, dec=1, c="#E5484D", at=2.0), dict(k="2차전", v=76.1, dec=1, c="#16A34A", at=1.0)])
SC['p9'] = prob7([-1] * 5, baseLabAt=-1, valAt=[0, 1.0, 50, 50, 50, 50, 50], hi=[dict(g=1, at=0), dict(g=2, at=1.0)])
SC['p10'] = prob7([-1] * 5, baseLabAt=-1, valAt=[-1, -1, 0, 3.0, 3.0, 50, 50], hi=[dict(g=3, at=0, c="#E5484D"), dict(g=4, at=2.0), dict(g=5, at=2.0)], cont=True)
SC['p11'] = prob7([-1] * 5, baseLabAt=-1, valAt=[-1, -1, -1, -1, -1, 2.0, 2.0], hi=[dict(g=6, at=1.0, c="#16A34A"), dict(g=7, at=1.0, c="#16A34A")], cont=True)
SC['p13'] = S(0, "vB_split", title="KT 한국시리즈 우승 확률", l="KT", r="삼성", from_=51.33, to=51.33, moveAt=-1, label=dict(v="51.33", at=-1), rlabel=dict(v="48.66", at=0), halfAt=2.0, chain="sp", cont=True)
SC['s4'] = HERO("후라도E", "후라도", "삼성", "", [ST("5차전", "7이닝", 2.0, True), ST("5차전 불펜", "두 명", 2.6)], imgAt=2.0)
SC['k17'] = S(0, "vA_tiles", z=1.15, title="2026 KT 정리", items=[dict(lab="타선", ic="bat", c="good", at=1.0), dict(lab="선발", ic="pitcher", c="good", at=1.0), dict(lab="장타", ic="bat", c="bad", at=2.0), dict(lab="중간 불펜", ic="pen", c="bad", at=3.0)])
SC.pop('h0')
END_SC = Q("야구자판기 · 매일 야구 이슈", ["KIA", "KT", "LG", "NC", "SSG", "두산", "롯데", "삼성", "키움", "한화"], logoSize=150, size=72)
# 11/1 20:18 사용자 "10월 27일은 왜 들어간 거야. 쓸데없는 서브텍스트들 다 지워" — 인물 장면의 꼬리표(감독·날짜·'선발 후보' 등)와 사진 장면 위 작은 머리글을 지운다(기록 범위를 알려 주는 'KT전'만 남김)
for _k, _s in SC.items():
    if _s.get('type') == 'hero' and _s.get('kicker') and 'KT전' not in _s['kicker']: _s['kicker'] = ''
    if _s.get('type') == 'faces':
        for _it in _s.get('items', []):
            if not _it.get('keep') and any(w in (_it.get('role') or '') for w in ('감독', '선발', '월 ', '차전 뒤', '경기 전')):
                if '감독' in _it['role']: _it['mgr'] = '감독'   # 화면엔 안 나옴 · 사전검사(감독은 사진 규칙 제외)용
                _it['role'] = ''
# 11/1 22:01 사용자 "제목이 지 멋대로 왔다갔다" — 자동 가운데 맞춤(_cx)이 칸이 하나씩 뜰 때마다 본문을 옮김 → 새 그림 장면은 처음부터 가운데로 그리고 자동 맞춤 끔
for _k, _s in SC.items():
    if _s.get('type', '').startswith(('mu_', 'vA_', 'vB_', 'ks_')) or _s.get('type') in ('rest', 'grid', 'errs'): _s['noCenter'] = True
# 11/1 22:10 흐린 여백(contain) 금지(10/13 규칙) — 상황별 폴더 선수 사진도 칸을 꽉 채운다
def _cov(o):
    if isinstance(o, dict):
        if isinstance(o.get('img'), str) and o['img'].startswith('상황별/') and not o.get('fit'): o['fit'] = 'cover'
        for v in o.values(): _cov(v)
    elif isinstance(o, list):
        for v in o: _cov(v)
for _s in SC.values(): _cov(_s)
for _k in list(SC): SC[_k] = dict(SC[_k], minDur=0.8)

for _k in [k for k in SC if k not in KEYS]: SC.pop(_k)
missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing and not extra, (missing, extra)
lines, scenes = [], []
for j, (k, narr, sub) in enumerate(_t.LINES):
    sc = dict(SC[k]); sc['startLine'] = j
    lines.append(L(narr, sub)); scenes.append(sc)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})
scenes.append(dict(END_SC, startLine=len(lines) - 1))

def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
CH = [ch("역대 1위 팀의 한국시리즈", "h1", "h15"), ch("2026년 KT", "k1", "k17"), ch("삼성의 남은 힘", "s1", "s17"), ch("차전별 맞대결", "v1", "v12"), ch("KT 우승 확률", "p1", "q2")]
DESC = ("2026 한국시리즈 KT 삼성 우승 예측 — 1차전부터 7차전까지 경기별 KT 승리 확률로 계산한 KT 통합 우승 확률은 51.33%예요.\n\n"
                "역대 1위 팀의 한국시리즈: 2005~2025년 정규시즌 1위 팀은 21번 중 19번 우승. 우승을 놓친 2015년 삼성·2018년 두산은 모두 플레이오프 5차전을 치르고 하루 쉰 상대에게 안방 1·2차전을 1승 1패로 나눴고 3차전부터 무너졌어요. 다만 플레이오프 5차전을 치르고 올라온 팀이 1위 팀을 꺾은 건 8번 중 2번뿐. 안방 1·2차전을 다 이긴 1위 팀은 10번 모두 우승.\n\n"
        "2026년 KT: 90승 5무 49패 구단 최다승, 팀 타율·득점 1위, 팀 평균자책점 2위, 팀 홈런은 7위, 홀드 1위 스기모토 평균자책점 5.90. 고영표 다승 1위·소형준 승률 1위, 1차전 선발 유력 대니엘은 첫 포스트시즌. 선발 넷이 나흘 이상 쉬며 7차전까지 돌 수 있는 일정. 큰 경기 경험은 김현수(한국시리즈 반지 세 개).\n\n"
        "삼성의 남은 힘: 정규시즌 맞대결 삼성 9승 7패. 세이브왕 김재윤 부상으로 원태인이 마무리, 선발은 최원태·페덱·후라도 순서가 유력 — 대구 3~5차전이 사흘 연속이라 셋으로만 돌리면 4차전부터 사흘 휴식.\n\n"
        "차전별 맞대결: 대니엘은 삼성전 등판 없음, 최원태 KT전 평균자책점 6.94, 삼성 중심 타선(구자욱·디아즈·최형우) 모두 왼손 — 사이드암 고영표 삼성전 3승 1패 2.25, 페덱 8월 29일 KT전 6이닝 무실점. 후라도 KT전 5.17, 힐리어드 삼성전 3할 4리 5홈런.\n\n"
        "제 계산: 출발점 43.75%(맞대결 7승 9패)에 수원 +4·대구 −4, 1차전 공백 −5, 삼성 불펜 피로 +2(1·2차전), 세이브왕 공백 +3, 삼성 선발 사흘 휴식 +6(4차전부터).\n"
        "1차전 47.75% · 2차전 52.75% · 3차전 42.75% · 4·5차전 48.75% · 6·7차전 56.75% → KT 우승 51.33%, 삼성 48.66%. 가장 가능성 높은 결과는 KT 4승 3패. 수원 2연승이면 82.35%, 1승 1패면 51.41%, 2연패면 19.52%.\n\n"
        "KT가 22일 공백을 딛고 통합 우승을 할까요? 아니면 플레이오프를 뚫고 올라온 삼성이 KT를 넘을까요? 댓글로 알려 주세요.\n\n▶ 지난 영상: 한국시리즈 1차전 예측 KT 삼성 · 플레이오프 5차전 리뷰\n\n"
        "#한국시리즈 #한국시리즈예측 #KT위즈 #삼성라이온즈 #KT우승 #고영표 #프로야구 #야구자판기\n")
TAGS = ["한국시리즈 예측", "한국시리즈 우승", "한국시리즈", "KT 위즈", "삼성 라이온즈", "KT 우승 확률", "이강철", "힐리어드", "대니엘", "고영표", "후라도", "원태인", "김현수", "프로야구", "KBO"]
SOURCE = "사실 출처 = KBO 기록실 + 기사 원문 — /home/claude/ks35/research, /home/claude/g5/research_*.md, 롱폼㉝ 근거모음"
EP = {"theme": "m3", "introChapter": "오프닝", "date": "2026-11-02", "gameDate": "2026-11-03", "series": "야구롱폼", "focusTeam": "KT", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1102-long35-v6", "topic": "KS예측_KT우승확률", "endcardSec": 20, "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "2026 한국시리즈 예측 KT 삼성 우승 확률 | 22일 공백·삼성 선발 휴식까지 계산해 보니", "description": DESC, "tags": TAGS, "hashtags": ["#한국시리즈", "#한국시리즈예측", "#KT위즈", "#삼성라이온즈", "#KT우승", "#고영표", "#프로야구", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'q1', 'q2')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-02_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
