# -*- coding: utf-8 -*-
"""11/1 밤 롱폼㊱ 「플레이오프 5차전 리뷰 + 한국시리즈 1차전 승부 예측」 콘티 (집 PC · 음성 API).
대사 = tools/text_1101_long36.py. 근거 = 기사 원문(5차전 11/1 스타뉴스·일간·스포티비 등) + KBO 기록실(롱폼㉟ 근거).
실행: python -X utf8 tools/gen_1101_long36.py → episodes/2026-11-01_롱폼2.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t36', os.path.join(HERE, 'text_1101_long36.py'))
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
def poser(ats, **k): return SER("2026 플레이오프 · 삼성 vs KIA", [G(n, v, h, w, a) for (n, v, h, w), a in zip(PO, ats)], chain="poser", **k)

SC = {}
def CELLS(title, items, cols=None, cw=460, ch=170, **k): return S(0, "cells", title=title, cols=cols or len(items), cw=cw, ch=ch, items=items, **k)
def CI(t, at, bad=False, hi=False, fs=44): return dict(t=t, at=at, bad=bad, hi=hi, fs=fs)
# ── 오프닝 ──
SC['o0'] = PEO("한국시리즈 1차전 · 중심 타자", [pc("디아즈", "디아즈", "삼성", "", at=0), pc("최형우B", "최형우", "삼성", "", at=0), pc("힐리어드", "힐리어드", "KT", "", at=1.0), pc("최원준", "최원준", "KT", "", at=1.0)], size=100)
SC['o1'] = HERO("후라도B", "후라도", "삼성", "플레이오프 5차전 · 삼성 승", [ST("투구", "7이닝", 0.3), ST("스코어", "6대1", 1.0), ST("플레이오프", "3승 2패", 2.0, True)])
SC['o2'] = poser([0.1, 0.15, 0.2, 0.25, 0.3], text="2024년 이후 · 2년 만의 한국시리즈", textAt=1.8)
SC['o3'] = S(0, "matchup", left="KT", right="삼성", score="VS", text="11월 3일 · 수원", tag="한국시리즈 1차전")
SC['o4'] = S(0, "vA_gap", title="1차전까지 쉬는 날", rows=[dict(team="삼성", days=1, lab="하루", at=0, fillAt=0.3), dict(team="KT", days=21, lab="3주", at=1.0, fillAt=2.0)], legendAt=50)
SC['o4b'] = Q("5차전 승부처는?\n1차전 승자는?", ["삼성", "KT"], logoSize=180, size=96)
SC['o5'] = S(0, "toc", itemFrom=1)
# ── 1. 5차전 승부처 ──
SC['g1'] = box(cont=False, tr="through")
SC['g2'] = box(hi=[1], marks=[dict(row=1, inn=1, label="선취점", at=0.5)])
_r12 = lambda ats, notes, text, **k: PEO("1·2회 · 삼성 공격", [pc("김지찬", "김지찬", "삼성", notes[0], at=ats[0]), pc("박승규", "박승규", "삼성", notes[1], at=ats[5]), pc("구자욱", "구자욱", "삼성", "볼넷", at=ats[1]), pc("최형우", "최형우", "삼성", "중전 적시타", at=ats[2]),
                                                       pc("강민호", "강민호", "삼성", "안타", at=ats[3]), pc("이재현", "이재현", "삼성", "2루타", at=ats[4])], size=62, chain="r12", text=text, textAt=k.pop('textAt', 1.4), **k)
SC['g3'] = PEO("1·2회 · 삼성 적시타", [pc("최형우", "최형우", "삼성", "1회 · 1타점", at=1.0), pc("김지찬", "김지찬", "삼성", "2회 · 2타점", at=2.0), pc("박승규", "박승규", "삼성", "2회 · 1타점", at=2.0)], size=100, text="4대0", textAt=2.7)
SC['g6'] = HERO("올러", "올러", "KIA", "KIA 선발 · 5차전", [ST("이닝", "2이닝", 1.0), ST("피안타", "6개", 1.0), ST("실점", "4점", 2.0, True)], chain="ol")
SC['g6b'] = HERO("올러", "올러", "KIA", "KIA 선발 · 2·5차전", [ST("2차전", "4⅔이닝 5실점", 2.0), ST("5차전", "2이닝 4실점", -1, True)], stamp=dict(t="대구 두 경기 모두", at=3.0), chain="ol", cont=True)
SC['g7'] = FACES([FC("이범호", "이범호", "KIA", "감독 · 5차전 경기 전", 0, say="“오늘 지면 탈락이기 때문에\n모든 선수가 대기한다”", sayAt=1.0)])
SC['g8'] = HERO("양현종", "양현종", "KIA", "KIA · 플레이오프 첫 등판", [ST("등판", "3회부터", 0.8, True)])
SC['g9'] = box(hi=[3], upto=3, sup=2, marks=[dict(row=0, inn=3, label="1점", at=0.5)])
SC['g10'] = PEO("3회초 · KIA 공격", [pc("하주석", "하주석", "KIA", "실책으로 출루", at=0), pc("디아즈", "디아즈", "삼성", "1루수 포구 실책", at=1.0), pc("박재현", "박재현", "KIA", "적시 3루타", at=2.0)], size=100)
SC['g11'] = box(hi=[3, 4, 5], upto=5, marks=[dict(row=1, inn=3, label="무실점", at=1.0)])
SC['g11b'] = box(hi=[4, 5], upto=5, marks=[dict(row=0, inn=4, label="무득점", at=1.0)])
SC['g12'] = box(hi=[6], upto=5, sup=5, marks=[dict(row=0, inn=6, label="승부처", at=0.3)])
SC['g12b'] = PEO("5차전 · KIA 타순", [pc("김도영", "김도영", "KIA", "2번 타자", at=1.0), pc("한준수", "한준수", "KIA", "지명타자", at=2.0)], size=110)
SC['g13'] = PEO("6회초 · 실책 뒤 1사 1·2루", [pc("나성범", "나성범", "KIA", "우전 안타", at=0)], size=120)
_r6 = lambda ats, **k: PEO("6회초 · 후라도 연속 삼진", [pc("후라도", "후라도", "삼성", "\u00a0", at=ats[0]), pc("김선빈", "김선빈", "KIA", "\u00a0", at=ats[1]), pc("한준수B", "한준수", "KIA", "\u00a0", at=ats[2])], size=100, chain="r6", **k)
SC['g14'] = _r6([0, 1.0, 1.0])
SC['g15'] = _r6([-1, -1, -1], cont=True)
SC['g15b'] = box(hi=[6], upto=6, sup=5, cont=False)
SC['g16'] = PEO("6회말 · 삼성 공격", [pc("류지혁", "류지혁", "삼성", "안타", at=1.0), pc("강민호B", "강민호", "삼성", "희생번트", at=1.0)], size=110)
SC['g17'] = PEO("6회말 · 2사 2루 · 김지찬 타구", [pc("카스트로", "카스트로", "KIA", "\u00a0", at=2.0)], size=120, chain="r6b", text="3루타 · 삼성 5대1", textAt=3.0)
SC['g18'] = PEO("6회말 · 2사 2루 · 김지찬 타구", [pc("카스트로", "카스트로", "KIA", "\u00a0", at=-1)], size=120, chain="r6b", cont=True, text="3루타 · 삼성 5대1", textAt=-1)
_r6c = lambda ats, **k: PEO("6회말 · 삼성 공격", [pc("박승규", "박승규", "삼성", "적시타", at=ats[0]), pc("양현종", "양현종", "KIA", "KIA 투수", at=ats[1]), pc("이범호", "이범호", "KIA", "감독", at=ats[2])], size=110, chain="r6c", text="삼성 6대1", **k)
SC['g19'] = PEO("6회말 · 쐐기 적시타", [pc("박승규", "박승규", "삼성", "\u00a0", at=0), pc("양현종", "양현종", "KIA", "\u00a0", at=1.0)], size=110, text="6대1", textAt=1.6)
SC['g19c'] = CELLS("5차전을 가른 차이", [CI("삼성\n위기에서 삼진", 1.0, hi=True), CI("KIA\n타구 판단 실수", 2.0, bad=True)], cw=520, ch=190)
_hf = lambda st, **k: HERO("후라도B", "후라도", "삼성", k.pop('kicker', "플레이오프 5차전 · 선발승"), st, chain="hf", **k)
SC['g20'] = _hf([ST("투구", "7이닝 95구", 1.0), ST("피안타 · 볼넷 · 탈삼진", "5 · 2 · 3", 2.0), ST("실점", "1점", 3.0, True)])
SC['g21'] = _hf([ST("투구", "7이닝 95구", -1), ST("피안타 · 볼넷 · 탈삼진", "5 · 2 · 3", -1), ST("실점", "1점 · 비자책", -1, True)], cont=True)
SC['g21b'] = _hf([ST("2차전", "6⅔이닝 2실점", 2.0), ST("플레이오프 두 경기", "13⅔이닝 3실점", 4.0), ST("승리", "2승", 4.6, True)], cont=True, kicker="플레이오프 2·5차전 · 2승")
SC['g22'] = HERO("김지찬", "김지찬", "삼성", "플레이오프 5차전 · 타선의 주인공", [ST("타격", "4타수 3안타", 1.0), ST("타점 · 득점", "3타점 3득점", 1.0, True), ST("도루", "1개", 1.5)])
SC['g23'] = PEO("5차전 · 삼성 타선", [pc("김지찬", "김지찬", "삼성", "3안타 3타점", at=0), pc("박승규", "박승규", "삼성", "2안타 2타점", at=1.0), pc("최형우B", "최형우", "삼성", "멀티히트", at=2.0)], size=100)
SC['g24'] = PEO("5차전 · 삼성 마운드", [pc("이승민", "이승민", "삼성", "8회", at=0), pc("원태인", "원태인", "삼성", "9회", at=1.0)], size=110)
_TG = ["5대1", "8대3", "6대4", "4대2", "6대1"]
def poser2(ats, **k):
    d = poser(ats, **k)
    for g_, t_ in zip(d['games'], _TG): g_['tag'] = t_
    return d
SC['g25a'] = poser2([2.0, 50, 50, 50, 50])
SC['g25b'] = poser2([-1, 0.3, 1.0, 50, 50], cont=True)
SC['g25c'] = poser2([-1, -1, -1, 1.0, 50], cont=True)
SC['g25'] = poser2([-1, -1, -1, -1, 0.2], cont=True)
# ── 2. 삼성이 치른 대가 ──
SC['b1'] = Q("삼성이 치른 대가", ["삼성"], logoSize=200, size=104, tr="through")
SC['b2'] = S(0, "vA_units", title="플레이오프 · 삼성 투수 등판", team="삼성", groups=[dict(g="1차전", n=5), dict(g="2차전", n=3), dict(g="3차전", n=7), dict(g="4차전", n=6), dict(g="5차전", n=3)], at=0, fillAt=1.0, totAt=1.4, v="24", vl="번")
SC['b2b'] = BARS("4차전까지 + 5차전", [dict(label="1~4차전", value=21, unit="번", at=0, color=GRAY), dict(label="5차전", value=3, unit="번", at=1.0, color=TC("삼성"))], 30)
SC['b3'] = FACES([FC("이승민", "이승민", "삼성", "", 0), FC("원태인C", "원태인", "삼성", "", 2.0)])
SC['b4'] = HERO("후라도C", "후라도", "삼성", "한국시리즈 1차전", [ST("5차전 투구", "95구", 1.0), ST("1차전", "등판 불가", 1.6, True)], imgAt=1.0, chain="hfc")
SC['b5'] = HERO("김재윤", "김재윤", "삼성", "", [ST("부상", "오른쪽 전거근(옆구리)", 1.0), ST("진단", "약 2주 휴식", 2.0, True)], stamp=dict(t="2026 세이브왕", at=0))
SC['b5b'] = HERO("원태인B", "원태인", "삼성", "삼성 뒷문", [ST("보직", "선발 → 마무리", 1.0), ST("5차전", "9회 등판", 2.0, True)])
_er = lambda ats, **k: S(0, "errs", title="삼성 실책", items=[dict(k="4차전", v="3개", at=ats[0]), dict(k="5차전", v="2개", at=ats[1])], chain="er", **k)
SC['b6a'] = S(0, "vA_errs", title="삼성 실책", items=[dict(g="4차전", n=3, slots=3, v="3개", at=50), dict(g="5차전", n=2, slots=3, v="2개", at=50)], chain="er")
SC['b6'] = S(0, "vA_errs", title="삼성 실책", items=[dict(g="4차전", n=3, slots=3, v="3개", at=0.2), dict(g="5차전", n=2, slots=3, v="2개", at=1.0)], chain="er", cont=True)
SC['b6b'] = HERO("디아즈B", "디아즈", "삼성", "삼성 1루수", [ST("4·5차전", "모두 실책", 1.0, True)])
SC['b7'] = S(0, "vA_battery", title="삼성 마운드의 남은 힘", items=[dict(lab="흔한 생각", lvl=0.18, c="bad", at=0.3), dict(lab="남은 힘", lvl=0.68, frm=0.18, c="good", bolt=True, at=1.0)], tr="through")
SC['b8'] = S(0, "vA_innings", z=1.05, title="5차전 · 삼성 마운드", team="삼성", segs=[dict(frm=1, to=7, lab="선발 · 7회까지", at=0), dict(frm=8, to=9, lab="불펜", c="#0E9384", at=2.0)], v="불펜은 두 명뿐", vn=2, vc="#0E9384", vAt=2.6)
SC['b9'] = S(0, "vA_days", title="나머지 삼성 불펜", team="삼성", days=[dict(date="10/30", k="p", lab="4차전", at=1.0), dict(date="10/31", k="r", lab="", at=2.0), dict(date="11/1", k="r", lab="", at=2.1), dict(date="11/2", k="r", lab="", at=2.2), dict(date="11/3", k="g", lab="1차전", at=3.0)], brackets=[dict(lab="적어도 사흘 휴식", w=662, at=2.3)])
SC['b9b'] = S(0, "vA_days", title="이틀 연속 경기", team="삼성", cw=300, ch=300, days=[dict(date="11/3", k="g", lab="1차전", at=0, ic="pen", icAt=2.0, arrow=True, arrowAt=1.0), dict(date="11/4", k="bad", lab="2차전", at=1.0, ic="tired", icAt=3.0)], brackets=[dict(lab="불펜 운용이 그대로 이어짐", w=722, c="#E5484D", at=3.0)])
SC['b10'] = PEO("삼성 타선", [pc("디아즈C", "디아즈", "삼성", "플레이오프 홈런", at=0), pc("최형우C", "최형우", "삼성", "플레이오프 홈런", at=0)], size=110, text="두 선수 홈런 4개 합작", textAt=1.0)
SC['b11'] = FACES([FC("박진만", "박진만", "삼성", "감독 · 4차전 뒤", 0, say="“마지막 5차전이기에 페덱과 최원태 빼고는\n불펜을 다 쓸 수 있게”", sayAt=1.0), FC("페덱", "페덱", "삼성", "4차전 선발", 1.0), FC("최원태", "최원태", "삼성", "3차전 선발", 1.0)], chain="b11")
SC['b12'] = FACES([FC("박진만", "박진만", "삼성", "감독 · 4차전 뒤", -1, say="“마지막 5차전이기에 페덱과 최원태 빼고는\n불펜을 다 쓸 수 있게”", sayAt=-1), FC("페덱", "페덱", "삼성", "", -1), FC("최원태", "최원태", "삼성", "", -1)], chain="b11", cont=True)
SC['b13'] = HERO("최원태B", "최원태", "삼성", "1차전 선발 후보", [ST("3차전", "1⅔이닝", 1.0), ST("1차전이면", "나흘 휴식", 2.0, True)])
_pd = lambda st, **k: HERO("페덱B", "페덱", "삼성", "1차전 선발 후보", st, chain="pd", **k)
SC['b14'] = _pd([ST("4차전", "5⅓이닝 1실점", 2.0), ST("1차전이면", "사흘 휴식", 3.0, True)])
SC['b14b'] = FACES([FC("페덱", "페덱", "삼성", "", 1.0), FC("박진만", "박진만", "삼성", "감독 · 4차전 뒤", 0, say="페덱은 사흘 쉬고도\n구속 유지", sayAt=1.0)])
SC['b14d'] = S(0, "rest", title="삼성 선발 · 쉬는 날", days=["10/26", "10/27", "10/28", "10/29", "10/30", "10/31", "11/1", "11/2", "11/3"],
    items=[dict(img=P["최원태B"], name="최원태", team="삼성", at=-1, cells={"10/29": dict(k="p", t="3차전"), "10/30": dict(k="r"), "10/31": dict(k="r"), "11/1": dict(k="r"), "11/2": dict(k="r"), "11/3": dict(k="g")}, chip="1⅔이닝 강판 · 일찍 내려갈 걱정", chipAt=0, chipBad=True),
          dict(img=P["페덱B"], name="페덱", team="삼성", at=-1, cells={"10/26": dict(k="p", t="1차전"), "10/27": dict(k="r"), "10/28": dict(k="r"), "10/29": dict(k="r"), "10/30": dict(k="p", t="4차전"), "10/31": dict(k="r"), "11/1": dict(k="r"), "11/2": dict(k="r"), "11/3": dict(k="g")}, chip="사흘 휴식 두 번 연속", chipAt=1.0, chipBad=True)])
SC['b15'] = HERO("후라도D", "후라도", "삼성", "2026 정규시즌 KT전", [ST("등판", "세 경기", 50, ghost=True), ST("평균자책점", "5.17", 50, True, ghost=True), ST("피홈런", "4개", 50, ghost=True)], chain="hd", stamp=dict(t="1차전 결장", at=0.3))
SC['b16'] = HERO("후라도D", "후라도", "삼성", "2026 정규시즌 KT전", [ST("등판", "세 경기", 1.0), ST("평균자책점", "5.17", 2.0, True), ST("피홈런", "4개", 3.0)], chain="hd", cont=True, stamp=dict(t="1차전 결장", at=-1))
SC['b17'] = S(0, "vA_tiles", z=1.15, title="삼성 정리", items=[dict(lab="선발", ic="pitcher", c="bad", at=1.0), dict(lab="수비", ic="glove", c="bad", at=1.0), dict(lab="불펜", ic="pen", c="good", at=2.0)])
# ── 3. KT의 1차전 ──
SC['k1'] = Q("KT의 1차전 준비", ["KT"], logoSize=200, size=104, tr="through")
SC['k2'] = BARS("KT의 공식 경기 공백", [dict(label="10월 12일 → 1차전", value=22, unit="일", at=2.0, hi=True, color=RED)], 25)
SC['k2c'] = S(0, "vA_streak", z=1.0, title="KT 정규시즌 마지막 10경기", n=10, at=1.0, tagAt=1.0, lab="창단 첫 10연승")
SC['k2b'] = S(0, "grid", title="22일 이상 공백 뒤 나선 1위 팀", cols=[dict(team="KIA", label="2017"), dict(team="SSG", label="2022"), dict(team="LG", label="2023"), dict(team="LG", label="2025")], colAt=2.0,
    rows=[dict(k="1차전", at=3.0, vals=[dict(t="패", c="bad"), dict(t="패", c="bad"), dict(t="패", c="bad"), dict(t="승", c="good")]), dict(k="시리즈", at=4.0, vals=[dict(t="", c="good", icon="trophy")] * 4)])
SC['k3'] = S(0, "vA_games", z=1.0, title="KT 연습경기", games=[dict(date="10월 27일", opp="상무", badge="army", a="7", b="0", at=1.0, scAt=1.3), dict(date="10월 28일", opp="23세 이하 대표팀", badge="u23", a="8", b="2", at=2.0, scAt=3.6)])
_dn = lambda st, **k: HERO("대니엘", "대니엘", "KT", k.pop('kicker', "1차전 선발 유력"), st, chain="dn", **k)
SC['k3b'] = _dn([ST("합류", "시즌 중", 1.0, True)])
SC['k4'] = _dn([ST("정규시즌", "10경기", 1.0), ST("승패", "5승 2패", 2.0), ST("평균자책점", "2.13", 3.0, True)], cont=True)
SC['k5'] = _dn([ST("상무전", "5이닝", 1.0), ST("피안타", "0개", 1.0), ST("삼진", "10개", 2.0, True)], kicker="10월 27일 · 상무 연습경기", cont=True)
SC['k6'] = _dn([ST("상무전", "5이닝", -1), ST("피안타", "0개", -1), ST("삼진", "10개", -1, True)], kicker="10월 27일 · 상무 연습경기", cont=True, stamp=dict(t="첫 포스트시즌 · 첫 삼성전", at=1.6))
SC['k7'] = S(0, "vA_rank", title="2026 KT 타선 · 리그 1위", logoAt=0, items=[dict(lab="팀 타율", ic="bat", v="", at=1.0), dict(lab="팀 득점", ic="ball", v="", at=1.2)])
SC['k7b'] = PEO("2026 KT 타선", [pc("힐리어드", "힐리어드", "KT", "타점왕 · 139타점", at=0), pc("최원준", "최원준", "KT", "득점왕 · 125득점", at=1.0)], size=120, chain="kt7")
SC['k8'] = FACES([FC("이강철B", "이강철", "KT", "감독 · 10월 27일", 1.0, say="“두 경기 정도 … 타자들이 못 치면\n투수들로 버티는 것”", sayAt=2.0)])
SC['k9'] = S(0, "vA_relay", title="KT 마운드", nodes=[dict(lab="선발", at=0), dict(lab="중간 불펜", c="bad", at=1.0, warnAt=1.3), dict(lab="마무리", c="good", at=1.0, warnAt=1.1)])
SC['k10'] = S(0, "vA_saves", z=1.15, title="KT 마무리 · 2026 정규시즌", n=30, at=0.2, v="30", vl="세이브", eraAt=1.0, eraLab="평균자책점", era="2.48")
SC['k11'] = S(0, "mu_pstat", title="2026 KT 홀드왕", img=P["스기모토"], name="스기모토", team="KT", at=0, n=25, iconLab="홀드", iconAt=0.2, era=5.90, eraAt=1.0)
SC['k12'] = S(0, "mu_inn", title="KT가 이기는 길", img=P["대니엘B"], name="대니엘", team="KT", at=1.0, chain="dnb", segs=[dict(frm=1, to=7, lab="길게 버티기", at=1.0), dict(frm=8, to=8, lab="중간 불펜", skip=True, at=2.0), dict(frm=9, to=9, lab="마무리", c="#0E9384", at=2.0)])
SC['k12b'] = S(0, "mu_inn", title="KT가 이기는 길", img=P["대니엘B"], name="대니엘", team="KT", at=-1, chain="dnb", cont=True, segs=[dict(frm=1, to=7, lab="길게 버티기", at=-1), dict(frm=8, to=8, lab="중간 불펜", skip=True, at=-1), dict(frm=9, to=9, lab="마무리", c="#0E9384", at=-1)], marks=[dict(inn=6, lab="교체 시점?", at=1.0)])
# ── 4. 1차전 승부 예측 ──
SC['p1'] = Q("1차전 승부 예측", ["KT", "삼성"], logoSize=180, size=104, tr="through")
SC['p2'] = S(0, "vB_units", title="1차전 이긴 1위 팀의 시리즈", sub="2005~2025 한국시리즈", n=13, slotAt=1.0, fillAt=2.0, fills=["trophy"] * 12 + ["x"], big=dict(v="12", unit="/ 13팀 우승", at=2.3, c="#B07A00"))
SC['p3'] = S(0, "vB_meter", title="5차전 치르고 온 팀의 1차전", l="KT", r="삼성", from_=0, to=-0.6, moveAt=2.0, lBadge=dict(t="유리", at=2.2), rBadge=dict(t="1차전 약세", at=2.0, bg="#9AA3B2"), chain="mt")
SC['p4'] = S(0, "vB_units", title="5차전 치르고 온 팀의 1차전", sub="2005~2025", n=8, slotAt=1.0, fillAt=2.0, fills=["win", "win"] + ["loss"] * 6, big=dict(v="2승 6패", unit="", at=2.3, c="#E5484D"))
SC['p4b'] = S(0, "vB_rings", title="1위 팀의 한국시리즈 승률", sub="2005~2025", items=[dict(k="1차전", v=61.9, dec=1, c="#E5484D", at=1.0, down=dict(t="첫 경기", at=3.0)), dict(k="2차전", v=76.1, dec=1, c="#16A34A", at=2.0)])
SC['p5'] = S(0, "vB_meter", title="1차전 예상", l="KT", r="삼성", from_=-0.6, to=0.18, moveAt=2.0, lBadge=dict(t="기록상 유리", at=0.5, bg="#9AA3B2"), rBadge=dict(t="아주 조금", at=2.3), chain="mt", cont=True)
SC['p6'] = S(0, "vB_only", title="KT의 정규시즌 상대", me="KT", opps=["KIA", "LG", "NC", "SSG", "두산", "롯데", "키움", "한화", "삼성"], hit="삼성", oppAt=0.3, hitAt=2.0, badge="유일한 열세")
def _w(steps, end_at=50, **k):
    return S(0, "water", title="KT 1차전 승리 확률 계산", team="KT", min=0, max=55, dec=2, base=dict(v=43.75, k="출발점\n맞대결 7승 9패", at=k.pop('base_at', -1)), steps=steps, end=dict(v=47.75, k="1차전\nKT 승리 확률", at=end_at), noCenter=True, chain="w1", **k)
_st = lambda a: [dict(k="수원 안방", d=4, at=a[0]), dict(k="22일 만의\n공식 경기", d=-5, at=a[1]), dict(k="삼성 뒷문 공백", d=3, at=a[2]), dict(k="삼성 불펜 피로\n(마무리 제외)", d=2, at=a[3])]
SC['p7'] = _w(_st([50, 50, 50, 50]), base_at=0.5)
SC['p8'] = _w(_st([1.0, 3.0, 50, 50]), cont=True)
SC['p9'] = _w(_st([-1, -1, 1.0, 50]), cont=True)
SC['p10'] = _w(_st([-1, -1, -1, 4.0]), cont=True)
SC['p11'] = _w(_st([-1, -1, -1, -1]), end_at=1.0, cont=True)
SC['p12'] = S(0, "probpair", title="1차전 승리 확률", items=[dict(team="KT", label="KT", v=47.75, at=-1), dict(team="삼성", label="삼성", v=52.25, at=0, hi=True)], dec=2, noCenter=True)
SC['p12b'] = S(0, "vB_split", title="삼성 불펜 피로를 더 주면", l="KT", r="삼성", from_=47.75, to=50.75, moveAt=1.5, push=dict(t="+3", at=1.0), label=dict(v="50.75", at=2.0))
SC['p12c'] = _w(_st([-1, -1, -1, -1]), end_at=-1)
SC['p13'] = S(0, "vB_three", title="1차전을 가를 세 장면", items=[dict(n="첫째", icon="glove", k="삼성 선발", c="#074CA1", at=0), dict(n="둘째", icon="bat", k="KT 타선", c="#12161F", at=0.04), dict(n="셋째", icon="pen", k="7회 이후 불펜", c="#F08C00", at=0.08)])
SC['p14'] = S(0, "vB_inn", title="첫째 · 삼성 선발", team="삼성", line=dict(inn=5, at=1.0), rows=[dict(k="버티면", icon="glove", sp=5, at=1.0, mark="ok", markAt=1.6), dict(k="일찍 강판", icon="glove", ic="#E5484D", sp=3, at=2.0, pen=True, penAt=3.0, mark="bad", markAt=4.0)])
SC['p14b'] = S(0, "vB_inn", title="플레이오프 삼성 선발 이닝", team="삼성", line=dict(inn=5, at=3.0), rows=[dict(k="1차전", sp=4.67, at=2.0, mark="bad", markAt=3.2), dict(k="3차전", sp=1.67, at=2.1, mark="bad", markAt=3.3), dict(k="4차전", sp=5.33, at=2.2, mark="ok", markAt=3.4)])
_dc = lambda st, **k: HERO("대니엘", "대니엘", "KT", "둘째 · 초반 싸움", st, chain="dc", **k)
SC['p15'] = S(0, "mu_inn", title="둘째 · KT 타선 초반", img=P["대니엘"], name="대니엘", team="KT", at=0, chain="dc", segs=[dict(frm=1, to=3, lab="초반", hi=True, at=0.2)], badges=[dict(team="KT", ic="bat", lab="감각 찾기", at=1.0), dict(team="삼성", ic="run", lab="빠른 발", at=50), dict(team="삼성", ic="bunt", lab="희생번트", at=50)])
SC['p15b'] = S(0, "mu_inn", title="둘째 · KT 타선 초반", img=P["대니엘"], name="대니엘", team="KT", at=-1, chain="dc", cont=True, segs=[dict(frm=1, to=3, lab="초반", hi=True, at=-1)], badges=[dict(team="KT", ic="bat", lab="감각 찾기", at=-1), dict(team="삼성", ic="run", lab="빠른 발", at=1.0), dict(team="삼성", ic="bunt", lab="희생번트", at=2.0)])
SC['p16'] = S(0, "mu_pen2", title="셋째 · 7회 이후 불펜 싸움", l=dict(team="KT", label="불펜", v="4.68", cap="정규시즌 평균자책점", at=1.0), r=dict(team="삼성", label="불펜", v="24번", n=24, cap="플레이오프 5경기 투수 등판", at=2.0))
SC['p17'] = S(0, "errs", title="변수 · 삼성 수비", items=[dict(k="4·5차전 모두", v="실책", at=0, shake=False)], text="리그 1위 KT 타선이 노린다", textAt=1.0)
SC['p18'] = S(0, "vB_meter", title="1차전 예상", l="KT", r="삼성", from_=0, to=0.3, moveAt=1.0, rBadge=dict(t="한두 점 차", at=1.0), tr="through")
SC['p18x'] = S(0, "mu_inn", title="반대 시나리오", img=P["대니엘B"], name="대니엘", team="KT", at=1.0, segs=[dict(frm=1, to=6, lab="6회 넘게", at=1.0), dict(frm=7, to=8, lab="중간 불펜", skip=True, at=2.0), dict(frm=9, to=9, lab="마무리", c="#0E9384", at=2.5)])
SC['p18b'] = S(0, "vB_branch", title="결과에 따라", up=dict(team="삼성", steps=[dict(logo="삼성", t="승리", at=0), dict(icon="score", v="2차전", t="내줘도", at=1.0), dict(icon="score", v="1승 1패", t="수원 2경기", at=2.0), dict(icon="home", t="안방 대구로", at=3.0, hi=True)]), dn=dict(team="KT", steps=[dict(logo="KT", t="승리", at=50), dict(icon="q", t="걱정 덜기", at=50)]), chain="nx")
SC['p18c'] = S(0, "vB_branch", title="결과에 따라", up=dict(team="삼성", steps=[dict(logo="삼성", t="승리", at=-1), dict(icon="score", v="2차전", t="내줘도", at=-1), dict(icon="score", v="1승 1패", t="수원 2경기", at=-1), dict(icon="home", t="안방 대구로", at=-1, hi=True)]), dn=dict(team="KT", steps=[dict(logo="KT", t="승리", at=0.1), dict(icon="q", t="걱정 덜기", at=1.0, strike=1.4, hi=True)]), chain="nx", cont=True)
SC['p19'] = S(0, "vB_next", title="시리즈 우승 확률은?", steps=[dict(icon="trophy", t="우승 확률", at=0), dict(icon="cal", big="11/2", t="미디어데이", at=1.0), dict(icon="pitchers", t="선발 발표", at=2.0), dict(icon="play", t="다음 영상", at=3.0, hi=True)])
SC['p20'] = TL("정리", [dict(d="5차전", t="선발 7이닝\n1번 타자 3안타", c="good", at=1.0), dict(d="1차전 열쇠", t="삼성 선발 이닝\n7회 이후 불펜", c="gold", at=4.0, big=True)])
SC['q1'] = Q("1차전 승자는?", ["KT", "삼성"], logoSize=200, size=110, chain="q")
SC['q2'] = Q("1차전 승자는?", ["KT", "삼성"], logoSize=200, size=110, chain="q", cont=True)
END_SC = Q("야구자판기 · 매일 야구 이슈", ["KIA", "KT", "LG", "NC", "SSG", "두산", "롯데", "삼성", "키움", "한화"], logoSize=150, size=72)

# ── 11/1 20:20 롱폼㊱ 추가: 대니엘 첫 맞대결·구종, 불펜 비교, 4. 1차전 핵심 맞대결 ──
SC['k6c'] = S(0, "mu_donut", title="상무전 62구 · 구종", center="구", chain="dnut", items=[dict(k="기타", v=23, c="#D5DAE2", at=0, noLeg=True), dict(k="투심", v=24, c=TC("KT"), at=1.0), dict(k="스위퍼", v=15, c="#E5484D", at=2.0)], text="삼성 타자들 · 처음 보는 공", thide=True)
SC['k6d'] = S(0, "mu_donut", title="상무전 62구 · 구종", center="구", chain="dnut", cont=True, items=[dict(k="기타", v=23, c="#D5DAE2", at=-1, noLeg=True), dict(k="투심", v=24, c=TC("KT"), at=-1), dict(k="스위퍼", v=15, c="#E5484D", at=-1)])
SC['k9b'] = S(0, "mu_fly", title="2026 정규시즌 불펜", lt="KT", rt="삼성", rows=[dict(k="평균자책점", l=4.68, r=4.23, dec=2, worse="l", at=1.0), dict(k="블론세이브", l=22, r=17, worse="l", at=3.0)])
SC['m1'] = Q("1차전 핵심 맞대결", ["KT", "삼성"], logoSize=180, size=104, tr="through")
SC['m2'] = S(0, "mu_pgames", title="2026 수원 KT전", img=P["최원태"], name="최원태", team="삼성", at=0, chain="cw", statsCap="정규시즌 전체", stats=[dict(k="승패", v="7승 5패", at=50), dict(k="평균자책점", v="4.68", at=50)], statAt=1.0,
    rows=[dict(opp="KT", d="4월", inn=5, runs=5, at=50), dict(opp="KT", d="6월", inn=None, runs=4, rl="4자책", res="패", at=50)])
SC['m3'] = S(0, "mu_pgames", title="2026 수원 KT전", img=P["최원태"], name="최원태", team="삼성", at=-1, chain="cw", cont=True, statsCap="정규시즌 전체", stats=[dict(k="승패", v="7승 5패"), dict(k="평균자책점", v="4.68")], statAt=-1,
    rows=[dict(opp="KT", d="4월", inn=5, runs=5, at=0), dict(opp="KT", d="6월", inn=None, runs=4, rl="4자책", res="패", at=1.0)])
SC['m4'] = S(0, "mu_pgames", title="2026 KT전", img=P["페덱C"], name="페덱", team="삼성", at=0, statsCap="정규시즌 전체", stats=[dict(k="경기", v="13"), dict(k="승패", v="7승 3패"), dict(k="평균자책점", v="2.95")], statAt=1.0,
    rows=[dict(opp="KT", d="8월 29일", inn=6, runs=0, res="승", at=3.0)])
SC['m4b'] = S(0, "mu_choice", title="삼성 1차전 선발 · 관전 포인트", team="삼성", at=0, qAt=1.0, items=[dict(ic="rest", k="휴식", who=["최원태 · 나흘"], at=0), dict(ic="record", k="상대 기록", who=["페덱 · 8월 29일 무실점"], at=0)])
_h2 = lambda a, sa, ba, **k: S(0, "mu_hr2", title="삼성 중심 타자 · 시즌 홈런 · 타점", chain="hr2", items=[
    dict(img=P["디아즈C"], name="디아즈", team="삼성", at=a[0], stats=[dict(k="홈런", v="26", at=sa[0]), dict(k="타점", v="129", at=sa[0])], statAt=sa[0], balls=2, ballLab="", ballAt=ba[0]),
    dict(img=P["최형우C"], name="최형우", team="삼성", at=a[1], stats=[dict(k="홈런", v="18", at=sa[1]), dict(k="타점", v="106", at=sa[1])], statAt=sa[1], balls=2, ballLab="", ballAt=ba[1])], **k)
SC['m6'] = _h2([1.0, 1.0], [50, 50], [50, 50], text="플레이오프 홈런", thide=True)
SC['m7'] = _h2([-1, -1], [1.0, 3.0], [50, 50], cont=True, text="플레이오프 홈런", thide=True)
SC['m8'] = _h2([-1, -1], [-1, -1], [1.0, 2.0], cont=True, text="플레이오프 홈런", textAt=0)
_cl = lambda ra, oa, **k: S(0, "mu_closer", title="마무리 맞대결", chain="cl", l=dict(team="KT", label="마무리", cap="삼성전 6경기", stats=[dict(k="세이브", v="5"), dict(k="평균자책점", v="1.69", hi=True)], at=k.pop('la', -1)),
    r=dict(img=P["김재윤"], name="김재윤", team="삼성", cap="KT전 7경기", stats=[dict(k="세이브", v="5"), dict(k="평균자책점", v="1.42", hi=True)], at=ra, out="이탈 유력", outAt=oa), **k)
SC['m10'] = _cl(50, 50, la=0)
SC['m11'] = _cl(1.0, 1.4, cont=True)
_hs = lambda ga, ba, **k: S(0, "mu_streak", title="시즌 막판 삼성전", img=P["힐리어드C"], name="힐리어드", team="KT", chain="hs", at=k.pop('at', -1), bracket="3연타석 홈런", bracketAt=ba,
    games=[dict(d="10월 7일", vs="삼성", abs=[dict(k="hr", t="만루", streak=True)], at=ga[0]), dict(d="10월 11일", vs="삼성", abs=[dict(k="hr", t="\u00a0", streak=True), dict(k="hr", t="\u00a0", streak=True)], note="5타점", at=ga[1])], **k)
SC['m12'] = _hs([50, 50], 50, at=1.0)
SC['m13'] = _hs([0, 2.0], 50, cont=True)
SC['m14'] = _hs([-1, -1], 1.0, cont=True)
SC['m15'] = S(0, "mu_abs", title="10월 7일 · 삼성전", img=P["최원준C"], name="최원준", team="KT", at=0, abs=[1, 1, 1, 0], absAt=1.0)
_bl = lambda gs, **k: S(0, "mu_blocks", title="2026 정규시즌 맞대결", chain="bl", groups=gs, **k)
SC['m16'] = _bl([dict(team="삼성", n=9, at=50), dict(team="KT", n=3, at=50), dict(team="KT", n=4, at=50, hi=True)], tally=dict(at=50, items=[dict(team="삼성", v="9", u="승"), dict(team="KT", v="3", u="승")]), runs=dict(at=50, label="마지막 4경기 득점", items=[dict(team="KT", v=27), dict(team="삼성", v=8)]))
SC['m17'] = _bl([dict(team="삼성", n=9, at=0), dict(team="KT", n=3, at=0), dict(team="KT", n=4, at=50, hi=True)], cont=True, tally=dict(at=1.0, items=[dict(team="삼성", v="9", u="승"), dict(team="KT", v="3", u="승")]), runs=dict(at=50, label="마지막 4경기 득점", items=[dict(team="KT", v=27), dict(team="삼성", v=8)]))
SC['m18'] = _bl([dict(team="삼성", n=9, at=-1), dict(team="KT", n=3, at=-1), dict(team="KT", n=4, at=0, hi=True)], cont=True, runs=dict(at=1.0, label="마지막 4경기 득점", items=[dict(team="KT", v=27), dict(team="삼성", v=8)]), tally=dict(at=-1, items=[dict(team="삼성", v="9", u="승"), dict(team="KT", v="3", u="승")]))
SC['m19'] = _bl([dict(team="삼성", n=9, at=-1), dict(team="KT", n=3, at=-1), dict(team="KT", n=4, at=-1, hi=True)], cont=True, runs=dict(at=-1, label="마지막 4경기 득점", items=[dict(team="KT", v=27), dict(team="삼성", v=8)]), tally=dict(at=1.0, items=[dict(team="삼성", v="9", u="승"), dict(team="KT", v="7", u="승")]))
SC['b6c'] = FACES([FC("박진만", "박진만", "삼성", "", 0, say="작은 수비 하나가\n승부를 좌우", sayAt=2.0)])
SC['k3c'] = HERO("힐리어드D", "힐리어드", "KT", "", [ST("상무전", "3안타", 1.5, True), ST("홈런", "투런포", 1.0)], chain="hd2", imgAt=1.0)
SC['k3d'] = HERO("힐리어드D", "힐리어드", "KT", "", [ST("상무전", "3안타", -1, True), ST("홈런", "투런포", -1)], chain="hd2", cont=True, imgAt=-1, stamp=dict(t="투수마다 맞춤 전략", at=0.5))
SC['k7c'] = PEO("2026 KT 타선", [pc("힐리어드", "힐리어드", "KT", "타점왕 · 139타점", at=-1), pc("최원준", "최원준", "KT", "안타 2위 · 208안타", at=-1)], size=120, chain="kt7", cont=True)
SC['b4b'] = HERO("후라도C", "후라도", "삼성", "", [ST("5차전 투구", "95구", -1), ST("1·2차전", "건너뜀", 2.0), ST("대구 3차전", "유력", 2.6, True)], imgAt=-1, chain="hfc", cont=True, stamp=dict(t="플레이오프 MVP", at=1.0))
SC['k2d'] = S(0, "grid", title="2021 KT 한국시리즈", cols=[dict(team="KT", label="")], colAt=0,
    rows=[dict(k="공백", at=1.0, vals=[dict(t="14일 만", c="")]), dict(k="시리즈", at=3.0, vals=[dict(t="4전 전승", c="good", icon="trophy")])])
SC['m15b'] = S(0, "mu_fly", title="2026 정규시즌 팀 홈런", lt="KT", rt="삼성", rows=[dict(k="", l=121, r=140, worse="l", at=1.0)])
SC['p18d'] = PEO("1차전 키플레이어", [pc("김지찬", "김지찬", "삼성", "\u00a0", at=1.0), pc("스기모토", "스기모토", "KT", "\u00a0", at=2.0)], size=120, chain="kp")
SC['p18e'] = PEO("1차전 키플레이어", [pc("김지찬", "김지찬", "삼성", "출루 · 발로 흔들기", at=-1), pc("스기모토", "스기모토", "KT", "7·8회 지키기", at=-1)], size=120, chain="kp", cont=True)
SC['p10b'] = _w(_st([-1, -1, -1, -1]), cont=True)
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
    if _s.get('type', '').startswith(('mu_', 'vA_', 'vB_')) or _s.get('type') in ('rest', 'grid', 'errs'): _s['noCenter'] = True
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
# 11/1 영상 검수: 자막 줄바꿈을 낱말 묶음 단위로(꾸밈말+명사·숫자쌍·부사+동사 안 가름)
WRAP = {('g1', 0): '먼저 5차전 흐름부터\n짚어 보죠', ('g4', 3): '김지찬이\n2타점 적시타를 쳤어요', ('b4', 1): '5차전에서\n95구를 던진 후라도가',
        ('b14d', 2): '두 번 연속\n사흘 휴식이라는 부담 중', ('p4', 3): '1차전에선\n2승 6패에 그쳤거든요', ('p5', 2): '1차전은 삼성이\n아주 조금 앞선다고 봐요',
        ('p7', 0): '출발점은\n2026년 정규시즌 맞대결로', ('p12c', 3): 'KT가\n내리 이겼던 것도 있어서', ('p17', 0): '여기에\n삼성 수비가 또 흔들리면', ('b6', 1): '5차전에도\n실책 2개가 나왔거든요', ('b11', 0): '그리고\n박진만 감독은 4차전 뒤', ('p18c', 1): '긴 공백이라는 물음표를\n지우게 되죠'}
for (k_, b_), t_ in WRAP.items():
    if k_ not in KEYS: continue
    j_ = KEYS.index(k_); parts = lines[j_]['sub'].split('|')
    if b_ >= len(parts) or parts[b_].replace('\n', ' ') != t_.replace('\n', ' '): print('WRAP 건너뜀', k_, b_); continue
    parts[b_] = t_; lines[j_]['sub'] = '|'.join(parts)   # 11/1 롱폼㊱ 검수: 엔딩 = 10구단 로고 줄

def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
CH = [ch("5차전 승부처", "g1", "g23"), ch("삼성이 치른 대가", "b1", "b17"), ch("KT의 1차전 준비", "k1", "k12b"), ch("1차전 핵심 맞대결", "m1", "m19"), ch("1차전 승부 예측", "p1", "q2")]
DESC = ("한국시리즈 1차전(11월 3일 수원) KT vs 삼성 승부 예측과 플레이오프 5차전 리뷰예요.\n22일 만에 나서는 1위 KT와 기세가 오른 삼성, 한국시리즈 1차전은 누가 가져갈까요?\n\n"
        "5차전 승부처: 삼성이 기아를 6대1로 꺾고 3승 2패로 한국시리즈 진출. 1회 최형우 적시타, 2회 김지찬·박승규 적시타로 4대0. 4대1로 쫓기던 6회초 1사 1·2루에서 후라도가 김선빈·한준수 연속 삼진, 6회말 좌익수 카스트로의 판단 실수로 3루타·박승규 적시타로 6대1. 김지찬 3안타 3타점, 박승규 2안타 2타점, 최형우 멀티히트.\n\n"
        "삼성이 치른 대가: 플레이오프 다섯 경기 투수 등판 24번(이승민 다섯 경기 모두, 원태인 불펜 세 경기). 후라도는 1차전에 못 나오고 세이브왕 김재윤은 전거근 부상. 4·5차전 실책 5개. 하지만 5차전 불펜은 두 명뿐이라 나머지 불펜은 적어도 사흘을 쉬어요. 1차전 선발은 최원태 유력(나흘 휴식), 페덱이면 두 번 연속 사흘 휴식.\n\n"
        "KT의 1차전 준비: 창단 첫 10연승으로 정규시즌을 마친 뒤 22일 만의 공식 경기(2015년 이후 정규시즌이 끝나고 22일 이상 지나 한국시리즈를 치른 1위 팀 네 팀 중 세 팀이 1차전 패, 네 팀 모두 우승). 연습경기 상무 7대0(힐리어드 투런포 포함 3안타)·23세 이하 대표팀 8대2. 1차전 선발 유력 대니엘은 커리어 첫 포스트시즌이자 삼성전 첫 등판. 불펜 평균자책점 4.68·블론세이브 22개로 삼성(4.23·17개)보다 약했어요.\n\n"
        "1차전 핵심 맞대결: 최원태는 2026년 수원 KT전 두 번 모두 부진(5이닝 5실점, 4자책점 패), 페덱은 8월 29일 KT전 6이닝 무실점 승. 디아즈 26홈런 129타점·최형우 18홈런 106타점, 플레이오프 홈런 2개씩. KT 마무리는 삼성전 6경기 5세이브 1.69, 삼성은 KT전 5세이브 1.42의 김재윤이 빠질 가능성이 커요. 힐리어드는 시즌 막판 삼성전 만루홈런·2홈런 5타점·3연타석 홈런, 최원준도 10월 7일 삼성전 4타수 3안타. 삼성이 9승 3패로 앞서다 마지막 네 경기는 KT가 모두 이겼어요(27점 대 8점).\n\n"
        "1차전 예측: 2005년부터 1차전을 이긴 1위 팀은 13팀 중 12팀 우승, 플레이오프 5차전까지 치른 팀은 한국시리즈 1차전 2승 6패 — 기록상으로는 KT가 유리해요. 그래도 저는 1차전은 삼성이 아주 조금 앞선다고 봐요. 계산은 2026년 정규시즌 맞대결 7승 9패 43.75%에서 수원 안방 +4, 22일 만의 공식 경기 −5, 삼성 뒷문 공백 +3, 삼성 불펜 피로 +2(KT 막판 4연승은 맞대결 승률에 이미 포함) → KT 47.75%, 삼성 52.25%.\n"
        "→ 제 예상: 한두 점 차 접전 끝에 삼성의 1차전 승리. 열쇠는 삼성 선발이 5회까지 버티느냐, KT 타선의 초반 감각, 7회 이후 불펜 싸움. 시리즈 전체 우승 확률은 11월 2일 미디어데이 선발 발표 뒤 다음 영상에서.\n\n"
        "여러분은 1차전 어느 팀이 가져갈 것 같으세요? 댓글로 알려 주세요.\n\n▶ 지난 영상: 플레이오프 4차전 리뷰 · 5차전 승부 예측\n\n"
        "#한국시리즈 #한국시리즈1차전 #KT위즈 #삼성라이온즈 #플레이오프5차전 #대니엘 #프로야구 #야구자판기\n\n"
        "기록 출처: KBO 기록실(2026 정규시즌 기록·팀간 승패, 10/28 조회), 위키백과(역대 한국시리즈)\n"
        "기사 출처: 스타뉴스·일간스포츠·스포티비뉴스·세계일보·스포츠경향 11/1(플레이오프 5차전), 마이데일리·스포츠경향 11/1(이범호 감독), 스포츠경향·일간스포츠 10/30(박진만 감독), 서울신문 10/24·재경일보(김재윤), 스포츠경향 10/27·서울신문 10/29·스타뉴스 10/28(대니엘), 뉴스핌 10/27·엑스포츠뉴스 10/28(연습경기), 머니투데이 10/27(이강철 감독), OSEN 10/30·아주경제 10/31(한국시리즈 일정), 일간스포츠 10/7·10/12·10/13(KT 10연승·막판 삼성전), 스포츠경향 10/14(대니엘), 엑스포츠뉴스 10/16·파이낸셜뉴스 10/8(스기모토), 대구신문·재경일보 11/1(삼성 1차전 선발·박진만 감독), 마이데일리 6/9·엑스포츠뉴스 10/29(최원태), 헤럴드경제 10/22·고스포츠 8/30(페덱), 스포티비뉴스 10/27·뉴시스 10/29(디아즈), 톱스타뉴스 11/1·뉴스핌 10/30(최형우), 스타뉴스 10/22(불펜·마무리), 일간스포츠 10/7·10/11·10/20·머니투데이 10/7(힐리어드·최원준), 노컷뉴스 8/29(맞대결)\n"
        "사진 출처: 삼성 라이온즈 제공, 기아 타이거즈 제공, KT 위즈 제공, 스포츠경향, 스포츠조선, 스타뉴스, 연합뉴스, KBO")
TAGS = ["한국시리즈 1차전", "한국시리즈 예측", "한국시리즈", "KT 위즈", "삼성 라이온즈", "플레이오프 5차전", "대니엘", "후라도", "디아즈", "힐리어드", "김지찬", "스기모토", "최원태", "프로야구", "KBO"]   # 11/1 22:55 검수: 15개, 영상에 안 나오는 이름 빼기
SOURCE = "사실 출처 = 기사 원문 + KBO 기록실 — /home/claude/g5/facts_g5.md, claude/롱폼35 근거"
EP = {"introChapter": "오프닝", "date": "2026-11-01", "gameDate": "2026-11-01", "series": "야구롱폼", "focusTeam": "삼성", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.15,
      "rev": "1101-long36-v1", "topic": "PO5차전리뷰_KS1차전예측", "endcardSec": 15, "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "한국시리즈 1차전 예측 KT 삼성 | 디아즈냐 힐리어드냐, 플레이오프 5차전 삼성 기아 리뷰", "description": DESC, "tags": TAGS, "hashtags": ["#한국시리즈", "#한국시리즈1차전", "#KT위즈", "#삼성라이온즈", "#플레이오프5차전", "#대니엘", "#프로야구", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o0', 'q1', 'q2')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-01_롱폼2.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
