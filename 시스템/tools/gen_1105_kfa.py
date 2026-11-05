# -*- coding: utf-8 -*-
"""11/5 롱폼 「기아 역대 FA 돈값 순위」 콘티 (회사 PC · 음성 API).
대사 = tools/text_1105_kfa.py. 근거 = 계약 기사 2곳 이상 · KBO 기록실 · 스탯티즈 WAR(kfa contracts.md·stats.md·statiz_war_1104.md).
실행: python -X utf8 tools/gen_1105_kfa.py → episodes/2026-11-05_롱폼.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t36', os.path.join(HERE, 'text_1105_kfa.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
KEYS = [x[0] for x in _t.LINES]

BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억|(?:^| )다|(?:^| )못|(?:^| )안|(?:^| )만|(?:^| )(?:이번|지난|다음|올|그)|(?:^| )(?:네|다섯|여섯|일곱|여덟|아홉|열|열일곱)|중심|KBO|기아|WAR|\d+할|남는|좋은|\d+푼|\d+천만)$'); BAD_B = re.compile(r'^(건|타선|겨울|코치|\d+차전|첫 |것 |수 |때 |중 |구단|달러|일|명|개|경기|원|타수|안타|\d+(?:푼|리)(?![가-힣]*할))')
def wrap2(t):
    # 11/5 검수: PC build.py 가 자막 한 줄 16자(SUB_MAX)로 다시 나눈다 → 16자 넘는 조각은 여기서 직접 꺾어 넘긴다(두 줄 다 16자 이하면 그대로 씀).
    # 숫자·단위('1할 8푼 6리', '5천만 원'), '중심 타선', '일곱 건', '시즌 중' 사이에서는 꺾지 않는다
    if len(t) <= 16: return t
    best, bs = None, 1e9
    for m in re.finditer(' ', t):
        x, y = t[:m.start()], t[m.start() + 1:]
        if max(len(x), len(y)) > 16: continue
        sc = abs(len(x) - len(y)) + (100 if (' ' not in x or ' ' not in y) else 0) + (300 if (BAD_A.search(x) or BAD_B.match(y) or (re.search(r'\d+년$', x) and re.match(r'\d+(?:억|년|월)|WAR', y))) else 0)
        if sc < bs: best, bs = x + '\n' + y, sc
    assert best and bs < 300, ('자막 꺾기 자리 없음', t, best)
    return best
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
P = {}
def ph(k): return P.get(k, k)
SC = {}
# 바탕
BG_RED = {"css": "linear-gradient(115deg,#0E1016 0%,#1A1C24 45%,#3A0A10 100%),repeating-linear-gradient(115deg,rgba(234,0,41,.08) 0 30px,rgba(0,0,0,0) 30px 90px)"}
BG_GOLD = {"css": "radial-gradient(40% 60% at 22% 0%,rgba(255,200,90,.45),rgba(0,0,0,0) 70%),radial-gradient(40% 60% at 78% 0%,rgba(255,200,90,.40),rgba(0,0,0,0) 70%),radial-gradient(70% 50% at 50% 100%,rgba(120,80,20,.55),rgba(0,0,0,0) 70%),linear-gradient(#120D08,#120D08)"}
def BGI(k, f=None, pos="center 15%"): return dict(img=ph(k), pos=pos, **({"f": f} if f else {}))
BAND_F = "contrast(1.25) saturate(1.15) brightness(.5)"
def CARD(img, name, kicker, big=None, minor=None, bg=None, **k): return S(0, "rf_card", img=ph(img), name=name, team="KIA", kicker=kicker, big=big, minor=minor or [], bg=bg or BG_RED, noCenter=True, **k)
def BIGV(v, k, at, sub=None, size=None): return dict(dict(v=v, k=k, at=at), **({"sub": sub} if sub else {}), **({"size": size} if size else {}))
def MI(k, v, at): return dict(k=k, v=v, at=at)
def GOLD(img, name, en, profile, stats=None, **k): return S(0, "rf_gold", img=ph(img), name=name, en=en, team="KIA", season="2026 SEASON", plist=profile, stats=stats or [], bg=BG_GOLD, noCenter=True, **k)
def BAND(who, vals, bgk=None, team="KIA", tag=None, **k): return S(0, "rf_band", who=who, tag=tag, team=team, vals=vals, bg=BGI(bgk, BAND_F) if bgk else BG_RED, noCenter=True, **k)
def V(v, k, at, hi=False, size=None): return dict(dict(v=v, k=k, at=at, hi=hi), **({"size": size} if size else {}))
def DUO(title, cards, bgk=None, **k): return S(0, "rf_duo", title=title, cards=cards, bg=BGI(bgk, "blur(22px) brightness(.4)") if bgk else BG_RED, noCenter=True, **k)
def DC(img, name, at, stats=None, team="KIA", focus=None): return dict(dict(img=ph(img), name=name, team=team, at=at, stats=stats or []), **({"focus": focus} if focus else {}))
def RBARS(title, items, mx, bgk=None, glass=False, **k): return S(0, "rf_bars", title=title, items=items, max=mx, glass=glass, bg=BGI(bgk, "blur(18px) brightness(.45) saturate(1.2)") if bgk else BG_RED, noCenter=True, **k)
def SLOT(title, slots, **k): return S(0, "slotboard", title=title, team="KIA", slots=slots, noCenter=True, profile=k.pop("profile", True), **k)
def SL(img, name, pos, at=-1, **x): return dict(dict(img=ph(img) if img else None, name=name, pos=pos or "", at=at), **x)
def FG(title, items, **k): return S(0, "facegrid", title=title, items=items, noCenter=True, profile=True, whole=True, **k)
def FI(img, name, at, pos=None): return dict(img=ph(img), name=name, team="KIA", at=at)
def SP(img, name, bubbles, **k): return S(0, "speech", img=ph(img), name=name, bubbles=bubbles, **k)
def BB(date, text, at, hi=False): return dict(date=date, text=text, at=at, hi=hi)
def CAP(title, segs, **k): k.setdefault("chain", "cap"); return S(0, "capbar", title=title, segs=segs, max=500, **k)
def SEG(label, v, at, color=None): return dict(dict(label=label, v=v, at=at), **({"color": color} if color else {}))
def Q(text, logos, **k): return S(0, "question", text=text, logos=logos, logoSize=k.pop('logoSize', 200), size=k.pop('size', 96), **k)
def G(n, venue, home, win, at): return dict(n=n, venue=venue, home=home, win=win, at=at)
def SER(title, games, **k): return S(0, "series5", title=title, games=games, noCenter=True, **k)
END_SC = Q("야구자판기 · 매일 야구 이슈", ["KIA", "KT", "LG", "NC", "SSG", "두산", "롯데", "삼성", "키움", "한화"], logoSize=150, size=72)

BG_DARK = {"css": "linear-gradient(115deg,#0E1016 0%,#1A1C24 55%,#24262E 100%)"}
BG_NAVY = {"css": "linear-gradient(115deg,#0E1016 0%,#1A1C24 45%,#0A1E3F 100%)"}

# ── 기아 역대 FA 가성비 순위 장면 (11/4, 검수 1라운드 반영) ──
# 사진: 워터마크 없는 스포츠경향 원문 사진·구단 제공 사진만(마해영은 사람만 오린 원 사진 = 누끼 예외). 카드 칸보다 1.25배 넘게 키우지 않는 크기.
P.update({
    "김범수": "경기/김범수_투구_0729_KIA제공", "김범수N": "누끼/KBO스타일_경기_김범수_투구_0729_KIA제공_up_center",
    "윤석민": "경기/윤석민_KIA_세이브_2015_스포츠경향",
    "김주찬A": "경기/김주찬_KIA_타격_2018_스포츠경향", "김주찬B": "경기/김주찬_KIA_타격_2015_스포츠경향",
    "양현종22": "경기/양현종_KIA_투구_2022_스포츠경향", "양현종26": "경기/양현종_글러브_1012_KIA제공", "양현종17": "경기/양현종_KIA_20승_2017_스포츠경향",
    "마해영원": "KBO프로필/마해영_원", "마해영K": "경기/마해영_KIA_2004_사용자제공",   # 11/4 23:07 사용자가 준 기아 시절 사진(301px → 2.5배 확대)
    "나성범": "경기/나성범_세리머니_KIA제공", "나성범B": "경기/나성범_KIA_2025_스포츠경향", "나성범HR": "카드/P22_나성범_솔로홈런", "나성범HR6": "카드/P22_나성범_6회홈런", "나성범30": "상황별/나성범_30호",
    "최형우A": "경기/최형우_KIA_타격_2017_스포츠경향", "최형우D": "경기/최형우_KIA_브이_2022_OSEN", "최형우B": "경기/최형우_KIA_홈런세리머니_2017_스포츠경향", "최형우C": "경기/최형우_KIA_타격왕_2020_스포츠경향",
    "나지완": "경기/나지완_KIA_홈런_2017_스포츠경향", "나지완09": "경기/나지완_KS끝내기_2009_스포츠경향",
    "이범호": "경기/이범호_KS만루홈런_2017_스포츠경향", "이대형": "경기/이대형_KIA_주루_2014_스포츠경향",
    "김선빈20": "경기/김선빈_KIA_타격_2020_스포츠경향", "김선빈26": "경기/김선빈_스퀴즈_1012_KIA제공",
    "안치홍": "경기/안치홍_KIA_2019_스포츠경향", "장성호": "경기/장성호_KIA_주루_2008_스포츠경향",
    "광주": "경기/광주_전경_1017_KIA제공", "관중": "경기/광주_관중_1017_KIA제공",
})
# 10억당 = (계약 기간 WAR ÷ 뛴 시즌) ÷ (총액 ÷ 연수) × 10, 둘째 자리에서 자름(11/4 사용자 '자르기로 통일')
RK = [(17, "김범수", "3년 20억", -0.07), (16, "윤석민", "4년 90억", 0.40), (15, "김주찬", "2+1년 27억", 0.73), (14, "양현종", "4년 103억", 1.13),
      (13, "마해영", "4년 28억", 1.32), (12, "양현종", "2+1년 45억", 1.39), (11, "나성범", "6년 150억", 1.52), (10, "최형우", "3년 47억", 1.64),
      (9, "나지완", "4년 40억", 2.08), (8, "최형우", "4년 100억", 2.17), (7, "이범호", "3+1년 36억", 2.23), (6, "이대형", "4년 24억", 2.30),
      (5, "김주찬", "4년 50억", 2.31), (4, "양현종", "1년 22억 5천만", 2.42), (3, "김선빈", "3년 30억", 2.44), (2, "김선빈", "4년 40억", 2.87), (1, "장성호", "4년 42억", 3.30)]
import math
_W = {17: (-0.05, 1, 20, 3), 16: (2.74, 3, 90, 4), 15: (1.98, 3, 27, 3), 14: (11.72, 4, 103, 4), 13: (1.86, 2, 28, 4), 12: (2.09, 1, 45, 3), 11: (19.00, 5, 150, 6),
      10: (7.73, 3, 47, 3), 9: (8.32, 4, 40, 4), 8: (21.74, 4, 100, 4), 7: (8.03, 4, 36, 4), 6: (1.38, 1, 24, 4), 5: (11.55, 4, 50, 4), 4: (5.45, 1, 22.5, 1),
      3: (7.34, 3, 30, 3), 2: (11.48, 4, 40, 4), 1: (13.88, 4, 42, 4)}
_ex = {r: (w / s) / (t / y) * 10 for r, (w, s, t, y) in _W.items()}
_tr = lambda x: math.trunc(x * 100 + (1e-9 if x >= 0 else -1e-9)) / 100
for r in RK: assert abs(_tr(_ex[r[0]]) - r[3]) < 1e-9, (r, _ex[r[0]])
assert _tr(sum(_ex.values()) / 17) == 1.77
def RANK17(title, at=-1, hi=(), names=False, ref=None, cont=True, brk=None, valAt=50, **k):
    its = [dict(label=(r[1] if names else f"{r[0]}위"), v=r[3], at=at, hi=(r[0] in hi), dec=2, **({"txt": "-0.07"} if r[3] < 0 else {})) for r in RK]
    sc = RBARS(title, its, 3.6, bgk="광주", bw=70, gap=14, valAt=valAt, chain="rk", cont=cont, **({"lfs": 26} if names else {}), **k)
    if ref: sc["ref"] = dict(ref, side="left")
    if brk: sc["brk"] = brk
    return sc
def KC(img, name, kicker, big=None, minor=None, imgAt=None, nameAt=None, **k):
    sc = CARD(img, name, kicker, big=big, minor=minor, **k)
    if imgAt is not None: sc["imgAt"] = imgAt
    if nameAt is not None: sc["nameAt"] = nameAt
    return sc
def KCc(img, name, kicker, big=None, minor=None, **k): return KC(img, name, kicker, big, minor, imgAt=-1, nameAt=-1, **k)
BLUR_F = "blur(12px) brightness(.42) saturate(1.2)"
SHARP = {"윤석민", "양현종26", "나성범", "나성범B", "최형우C", "나지완", "이대형", "김선빈20", "김주찬B", "광주", "관중"}   # 1200px 넘는 사진만 또렷한 바탕, 나머지는 흐린 바탕
_BAND0 = BAND
def BAND(who, vals, bgk=None, team="KIA", tag=None, **k):
    # 2라운드 규칙 검수: 띠 바탕 사진은 전부 흐리게(얼굴·글 겹침, 1.25배 확대, 사진 시기 어긋남이 바탕에서 안 보이게), 한 띠 안 값 글자 크기는 하나로
    szs = [v.get("size", 128) for v in vals]
    vals = [dict(v, size=min(szs)) if len(set(szs)) > 1 else v for v in vals]
    sc = _BAND0(who, vals, bgk=bgk, team=team, tag=tag, **k)
    if bgk: sc["bg"] = BGI(bgk, BLUR_F)
    return sc
def VAL(v, at=0, k="10억당"): return BIGV(v, k, at, size=200)
def GOLDJ(stats, **k): return S(0, "rf_gold", img=ph("장성호"), name="장성호", en="JANG SEONG-HO", team="KIA", season="1위 · FA 2005", plist=["2006~2009년"], stats=stats, bg=BG_GOLD, noCenter=True, chain="jsh6", **k)

# ── 오프닝 ──
SC['o1'] = BAND("기아 역대 FA 돈값 순위", [V("1위?", "가장 남는 장사", 1, hi=True)], bgk="광주")
SC['o2'] = BAND("기아 FA 계약 · 20억 이상", [V("2003년 겨울부터", "", 0, size=96), V("17건", "", 2, hi=True)], bgk="광주")
SC['o3'] = DUO("17건 가운데", [DC("최형우B", "최형우", 0, [dict(k="KBO 첫", v="100억", at=0)]), DC("나성범", "나성범", 1, [dict(k="기아 역대 최고액", v="150억", at=1)])], bgk="관중")
SC['o4'] = RANK17("기아 FA 17건 · 가성비 순서", at=None, cont=False, st0=.05, stag=.045)   # 11/4 사용자 "17위에서 1위까지 좀 빨리, 나레이션 끝나기 1초 전까지" — 마지막 막대 1.15초에 다 섬(장면 2.3초)
SC['o5'] = BAND("1위는?", [V("100억", "최형우", 1), V("150억", "나성범", 1), V("아님", "둘 다", 1, hi=True)])
SC['o6'] = BAND("가성비 기준", [V("하나", "", 0, hi=True)], bgk="관중", chain="std0")
SC['o6b'] = BAND("가성비 기준", [V("1년 몸값 10억", "", 0, size=110), V("한 시즌 WAR", "", 1, hi=True, size=110)], bgk="관중", chain="std")
SC['o7'] = BAND("WAR", [V("기여도", "팀 승리", 1, hi=True)], bgk="관중")   # 11/4 16:09 사용자 "팀의 승리에 얼마나 기여했는지 나타내는 지표"
SC['o8'] = BAND("예시 ①", [V("10억", "1년 몸값", 0), V("WAR 2", "한 시즌", 0), V("2", "10억당", 1, hi=True)], bgk="관중", chain="ex")
SC['o9'] = BAND("예시 ②", [V("20억", "1년 몸값", 0), V("WAR 2", "한 시즌", 0), V("1", "10억당", 1, hi=True)], bgk="관중", chain="ex", cont=True)
SC['o10'] = BAND("계약 기간 제각각", [V("1년~6년", "계약 기간", 1), V("1년 단위", "연수로 나눔", 2, hi=True)], bgk="관중")
SC['o11'] = RANK17("기아 FA 17건 · 가성비 순서", ref=dict(v=1.77, lab="평균 1.77", at=1))
SC['o12'] = BAND("진행 중 계약", [V("진행 중", "계약 남은 선수", 0), V("2026시즌까지", "성적으로 계산", 1, hi=True)], bgk="광주")
SC['o13'] = BAND("이번 순위에서 뺀 계약", [V("20억 미만", "작은 계약", 0, hi=True)], bgk="광주")
# ── 1. 17~13위 ──
SC['a1'] = KC("김범수N", "김범수", "17위 · 2026~2028년", big=BIGV("3년 20억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['a2'] = KCc("김범수N", "김범수", "17위 · 2026~2028년", big=BIGV("3년 20억", "", -1, size=170), minor=[MI("평균자책점", "5.63", 1), MI("WAR", "-0.05", 2)])
SC['a3'] = BAND("김범수 시즌 WAR", [V("1.33", "2025년 한화", 1), V("-0.05", "2026년 기아", 2, hi=True), V("2027년", "두 시즌 남은 계약 · 시험대", 50, hi=True)], bgk="김범수", chain="kbs")   # 11/4 16:31 사용자 "너무 금방 지나가서 다 읽기도 전에 다음 장면으로 — 다음 장면이랑 합쳐서 한 장면에서 다 보이게"
SC['a4'] = BAND("김범수 시즌 WAR", [V("1.33", "2025년 한화", -1), V("-0.05", "2026년 기아", -1, hi=True), V("2027년", "두 시즌 남은 계약 · 시험대", 1, hi=True)], bgk="김범수", chain="kbs", cont=True)
SC['a5'] = KC("윤석민", "윤석민", "16위 · 2015~2018년", big=BIGV("4년 90억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['a6'] = KCc("윤석민", "윤석민", "16위 · 2015~2018년", big=BIGV("4년 90억", "", -1, size=170), minor=[MI("볼티모어에서", "복귀", 0), MI("당시 기아", "역대 최고액", 2)])
SC['a7'] = BAND("윤석민", [V("30세이브", "2015년 뒷문", 0, hi=True), V("0경기", "2017년 1군 출전", 50, hi=True)], bgk="윤석민", chain="ysm")   # 11/4 16:31 사용자 "너무 금방 지나가서 다 읽기도 전에 다음 장면으로 — 다음 장면이랑 합쳐서 한 장면에서 다 보이게"
SC['a8'] = BAND("윤석민", [V("30세이브", "2015년 뒷문", -1, hi=True), V("0경기", "2017년 1군 출전", 1, hi=True)], bgk="윤석민", chain="ysm", cont=True)
SC['a9'] = KC("윤석민", "윤석민", "16위 · 4년 90억", big=VAL("0.40", 1), minor=[MI("세 시즌 WAR", "2.74", 0)])
SC['a10'] = KC("김주찬A", "김주찬", "15위 · 2018~2020년", big=BIGV("2+1년 27억", "", 1, size=160))   # 11/4 22:46 계약 기간 소개
SC['a11'] = BAND("김주찬 · 2018년", [V("3할 4푼", "타율", 0), V("18홈런", "", 1, hi=True)], bgk="김주찬A")
SC['a12'] = BAND("김주찬 · 마지막 두 시즌", [V("3홈런", "2019년", 0), V("7경기", "2020년", 1), V("은퇴", "시즌 뒤", 2, hi=True)], bgk="김주찬A")
SC['a13'] = KC("김주찬A", "김주찬", "15위 · 2+1년 27억", big=VAL("0.73", 1), minor=[MI("세 시즌 WAR", "1.98", 0)])
SC['a13b'] = KCc("김주찬A", "김주찬", "15위 · 2+1년 27억", big=VAL("0.73", -1), minor=[MI("세 시즌 WAR", "1.98", -1)])
SC['a14'] = None   # 아래 순위표로 채움
SC['a14b'] = KC("양현종22", "양현종", "14위 · 2022~2025년", big=BIGV("4년 103억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['a15'] = KCc("양현종22", "양현종", "14위 · 2022~2025년", big=BIGV("4년 103억", "", -1, size=170), minor=[MI("2021년 겨울", "텍사스에서 복귀", 0)])
SC['a16'] = BAND("양현종 · 103억 계약 4년", [V("150이닝+", "4년 내내", 0), V("11승", "2024년", 1), V("우승", "선발진", 2, hi=True)], bgk="양현종22")
SC['a17'] = BAND("양현종 · 2025년", [V("5.06", "평균자책점", 1), V("0.86", "WAR", 2, hi=True)], bgk="양현종22")
SC['a18'] = KC("양현종22", "양현종", "14위 · 4년 103억", big=VAL("1.13", 2), minor=[MI("4년 WAR", "11.72", 0), MI("1년 몸값", "25억+", 1)])
SC['a19'] = BAND("양현종 · 4년 103억", [V("48억", "옵션", 0, hi=True), V("옵션 포함", "계산 기준", 1, size=110)], bgk="양현종22")
# 11/4 23:07 사용자 "자 마해영"(사진 제공) — 다른 선수와 같은 카드·띠로
SC['a20'] = KC("마해영K", "마해영", "13위 · 2004~2007년", big=BIGV("4년 28억", "", 1, size=170), focus="45% 25%")
SC['a20b'] = KCc("마해영K", "마해영", "13위 · 2004~2007년", big=BIGV("4년 28억", "", -1, size=170), minor=[MI("2002년 한국시리즈", "끝내기 홈런", 1)], focus="45% 25%")
SC['a21'] = BAND("마해영 · 기아 두 시즌", [V("11홈런", "첫 시즌", 1), V("12홈런", "둘째 시즌", 1), V("LG", "2005년 시즌 뒤 트레이드", 50, hi=True)], bgk="마해영K", chain="mhy")
SC['a22'] = BAND("마해영 · 기아 두 시즌", [V("11홈런", "첫 시즌", -1), V("12홈런", "둘째 시즌", -1), V("LG", "2005년 시즌 뒤 트레이드", 1, hi=True)], bgk="마해영K", chain="mhy", cont=True)
SC['a23'] = KC("마해영K", "마해영", "13위 · 4년 28억", big=VAL("1.32", 1), minor=[MI("기아에서 남긴 WAR", "1.86", 0)], focus="45% 25%")
SC['a23b'] = KCc("마해영K", "마해영", "13위 · 4년 28억", big=VAL("1.32", -1), minor=[MI("기아에서 남긴 WAR", "1.86", -1)], focus="45% 25%")
SC['a24'] = RBARS("여기까지 다섯 건 · 가성비", [dict(label=r[1], place=r[2], venue="KIA", v=r[3], dec=2, at=0, **({"txt": "-0.07"} if r[3] < 0 else {})) for r in RK[:5]], 2.2, bgk="광주", ref=dict(v=1.77, lab="평균 1.77", at=1))
# ── 2. 12~8위 ──
SC['b1'] = KC("양현종26", "양현종", "12위 · 2026~2028년", big=BIGV("2+1년 45억", "", 1, size=160))   # 11/4 22:46 계약 기간 소개
SC['b2'] = BAND("양현종 · 2026년", [V("12승 6패", "첫해", 0, hi=True), V("반등", "103억 계약 마지막 해보다", 1, size=110)], bgk="양현종26")
SC['b3'] = KC("양현종26", "양현종", "12위 · 2+1년 45억", big=VAL("1.39", 0), minor=[MI("반영", "2026년 한 시즌", 1)])
SC['b4'] = KC("나성범B", "나성범", "11위 · 2022~2027년", big=BIGV("6년 150억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['b5'] = KCc("나성범B", "나성범", "11위 · 2021년 겨울 NC에서 영입", big=BIGV("6년 150억", "", -1, size=170), minor=[MI("광주 진흥고", "출신", 1)])   # 11/4 16:31 사용자 "너무 금방 지나가서 다 읽기도 전에 다음 장면으로 — 다음 장면이랑 합쳐서 한 장면에서 다 보이게"
SC['b5b'] = KCc("나성범B", "나성범", "11위 · 2021년 겨울 NC에서 영입", big=BIGV("6년 150억", "", -1, size=170), minor=[MI("광주 진흥고", "출신", -1), MI("고향 팀", "대형 FA", 0)])
SC['b6'] = KC("나성범", "나성범", "11위 · 2022년", big=BIGV("7.16", "WAR", 2, size=200), minor=[MI("출전", "144경기", 1)])
SC['b7'] = RBARS("나성범 출전 경기", [dict(label=f"{y}년", v=g, unit="경기", at=0, hi=(g >= 110)) for y, g in [(2022, 144), (2023, 58), (2024, 102), (2025, 82), (2026, 140)]], 160, bgk="나성범B", ref=dict(v=110, lab="110경기", at=1))
SC['b8'] = BAND("2024년 우승 시즌", [V("21홈런", "중심 타선", 1, hi=True)], bgk="나성범HR")
SC['b9'] = BAND("2026년 시즌", [V("31홈런", "다시 반등", 0, hi=True)], bgk="나성범30")
SC['b10'] = BAND("6년 150억 · 11위", [V("19.00", "다섯 시즌 WAR", 0), V("1.52", "10억당", 1, hi=True), V("아래", "평균보다", 2)], bgk="나성범B")
SC['b11'] = BAND("6년 계약 마지막 해", [V("2027년", "남은 한 시즌", 0, hi=True)], bgk="나성범B")
SC['b12'] = KC("최형우D", "최형우", "10위 · 2021~2023년", big=BIGV("3년 47억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['b12b'] = KCc("최형우D", "최형우", "10위 · 2021~2023년", big=BIGV("3년 47억", "", -1, size=170), minor=[MI("2020년", "타격왕 직후", 0)])
SC['b13'] = BAND("최형우 · 2021년", [V("2할 3푼 3리", "타율", 1, hi=True)], bgk="최형우D", chain="chw")
SC['b14'] = BAND("최형우 · 2023년", [V("3할 2리", "타율", 0), V("17홈런", "", 1, hi=True)], bgk="최형우D", chain="chw", cont=True)
SC['b15'] = KC("최형우D", "최형우", "10위 · 3년 47억", big=VAL("1.64", 1), minor=[MI("세 시즌 WAR", "7.73", 0)])
SC['b15b'] = KCc("최형우D", "최형우", "10위 · 3년 47억", big=VAL("1.64", -1), minor=[MI("세 시즌 WAR", "7.73", -1), MI("첫해", "부진", 0)])
SC['b16'] = KC("나지완", "나지완", "9위 · 2017~2020년", big=BIGV("4년 40억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['b16b'] = KCc("나지완", "나지완", "9위 · 2017~2020년", big=BIGV("4년 40억", "", -1, size=170), minor=[MI("기아에서만", "15시즌", 1)])
SC['b17'] = KC("나지완09", "나지완", "2009년 한국시리즈 7차전", big=BIGV("끝내기 홈런", "", 1, size=150), minor=[MI("2016년 겨울", "기아 잔류", 2)])
SC['b18'] = BAND("나지완 · 2017년", [V("27홈런", "", 0, hi=True), V("통합 우승", "", 1)], bgk="나지완", chain="njw")
SC['b19'] = BAND("나지완 · 2019년", [V("1할 8푼 6리", "타율", 1, hi=True)], bgk="나지완", chain="njw", cont=True)
SC['b20'] = BAND("나지완 · 2020년", [V("17홈런", "", 0), V("92타점", "", 0, hi=True)], bgk="나지완", chain="njw", cont=True)
SC['b21'] = KC("나지완", "나지완", "9위 · 4년 40억", big=VAL("2.08", 1), minor=[MI("4년 WAR", "8.32", 0), MI("평균", "넘음", 2)])
SC['b22'] = KC("최형우A", "최형우", "8위 · 2017~2020년", big=BIGV("4년 100억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['b23'] = KCc("최형우A", "최형우", "8위 · 2017~2020년", big=BIGV("4년 100억", "", -1, size=170), minor=[MI("2016년 겨울", "삼성에서 영입", 0)])
SC['b24'] = BAND("최형우 · 2017년", [V("3할 4푼 2리", "타율", 1, size=100), V("26홈런", "", 2, size=100), V("120타점", "", 2, size=100)], tag="통합 우승", tagAt=3, bgk="최형우B")
SC['b25'] = BAND("최형우 · 2020년", [V("3할 5푼 4리", "타율", 1), V("타격왕", "", 2, hi=True)], bgk="최형우C")
SC['b26'] = RBARS("최형우 타율 · 첫 FA 4년", [dict(label=f"{y}년", v=a, txt=t, at=0) for y, a, t in [(2017, .342, "0.342"), (2018, .339, "0.339"), (2019, .300, "0.300"), (2020, .354, "0.354")]], .4, bgk="광주", ref=dict(v=.3, lab="3할", at=0), h=420)
SC['b27'] = BAND("최형우 · 첫 FA 4년 100억", [V("21.74", "4년 WAR", 0, hi=True), V("1위", "17건 가운데", 1)], bgk="최형우A", chain="chw2")
SC['b28'] = BAND("최형우 · 첫 FA 4년 100억", [V("25억", "1년 몸값", 0), V("2.17", "10억당", 1, hi=True), V("8위", "가성비", 1)], bgk="최형우A", chain="chw2", cont=True, whoAt=-1)
SC['b29'] = BAND("최형우 · 첫 FA 4년 100억", [V("1위", "WAR 합계", 0, hi=True), V("2.17", "10억당", 1, hi=True), V("8위", "가성비", 1)], bgk="최형우A", chain="chw2", cont=True, whoAt=-1)   # 11/5 검수: 8위가 같은 자리에 머물게 세 칸 유지
# ── 3. 7~3위 ──
SC['c1'] = S(0, "rf_sil", n=7, bg=BGI("관중", "blur(22px) brightness(.4)"), noCenter=True)   # 11/4 22:46 사용자 "남은 7명의 실루엣만 — 최형우 사진·텍스트 다 빼고"
SC['c2'] = KC("이범호", "이범호", "7위 · 2016~2019년", big=BIGV("3+1년 36억", "", 1, size=160))   # 11/4 22:46 계약 기간 소개
SC['c2b'] = KCc("이범호", "이범호", "7위 · 2016~2019년", big=BIGV("3+1년 36억", "", -1, size=160), minor=[MI("2011년", "기아 입단", 0), MI("2015년 겨울", "FA 잔류", 2)])   # 11/4 16:31 사용자 "너무 금방 지나가서 다 읽기도 전에 다음 장면으로 — 다음 장면이랑 합쳐서 한 장면에서 다 보이게"
SC['c3'] = BAND("이범호 · 2016년", [V("33홈런", "", 1, hi=True), V("108타점", "", 1)], bgk="이범호")
SC['c4'] = BAND("이범호 · 2017 한국시리즈 5차전", [V("만루홈런", "", 1, hi=True)], bgk="이범호")
SC['c5'] = KC("이범호", "이범호", "7위 · 3+1년 36억", big=VAL("2.23", 2), minor=[MI("은퇴", "2019년", 0), MI("4년 WAR", "8.03", 1)])
SC['c5b'] = KCc("이범호", "이범호", "7위 · 3+1년 36억", big=VAL("2.23", -1), minor=[MI("첫해", "33홈런", 0), MI("4년 WAR", "절반 넘게", 1)])
SC['c6'] = KC("이대형", "이대형", "6위 · 2014~2017년", big=BIGV("4년 24억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['c7'] = KCc("이대형", "이대형", "6위 · 2014~2017년", big=BIGV("4년 24억", "", -1, size=170), minor=[MI("2013년 겨울", "LG에서 영입", 0)])
SC['c8'] = BAND("이대형 · 2014년", [V("3할 2푼 3리", "타율", 1, hi=True)], bgk="이대형")
SC['c9'] = BAND("이대형 · 2014년 겨울", [V("20명", "기아 보호선수", 2), V("KT 특별지명", "신생팀", 3, hi=True)], bgk="이대형", whoAt=-1)
SC['c10'] = KC("이대형", "이대형", "6위 · 4년 24억", big=VAL("2.30", 2), minor=[MI("한 시즌 WAR", "1.38", 0), MI("1년 몸값", "6억", 1)])
SC['c11'] = BAND("이대형 4년 계약", [V("1년", "기아에서 뜀", 0), V("3년", "못 쓴 기간", 0, hi=True)], bgk="이대형")
SC['c12'] = KC("김주찬B", "김주찬", "5위 · 2013~2016년", big=BIGV("4년 50억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['c13'] = KCc("김주찬B", "김주찬", "5위 · 2012년 겨울 롯데에서 영입", big=BIGV("4년 50억", "", -1, size=170), minor=[MI("당시 역대 FA 총액", "공동 2위", 3)])   # 11/4 16:41 사용자 "순위표가 끼어들어 다음 장면이 너무 짧게 지나가 읽기 전에 지나가" — 첫 카드 내용 유지하고 쌓기
SC['c14'] = BAND("김주찬", [V("47경기", "2013년", 0), V("23홈런", "2016년", 2, hi=True), V("101타점", "", 2)], bgk="김주찬B")
SC['c15'] = KC("김주찬B", "김주찬", "5위 · 4년 50억", big=VAL("2.31", 2), minor=[MI("두 번째 FA", "15위", 0), MI("4년 WAR", "11.55", 1)])
SC['c16'] = KC("양현종17", "양현종", "4위 · 2017년", big=BIGV("1년 22억 5천만", "", 1, size=140))   # 11/4 22:46 계약 기간 소개
SC['c17'] = KCc("양현종17", "양현종", "4위 · 2017년", big=BIGV("1년 22억 5천만", "", -1, size=140), minor=[MI("2016년 겨울", "1년 계약", 0)])
SC['c18'] = BAND("양현종 · 2017년", [V("20승", "", 0), V("정규시즌 MVP", "", 1, hi=True, size=84), V("한국시리즈 MVP", "", 2, hi=True, size=84)], bgk="양현종17")
SC['c19'] = KC("양현종17", "양현종", "4위 · 1년 22억 5천만", big=VAL("2.42", 1), minor=[MI("한 시즌 WAR", "5.45", 0), MI("세 계약 중", "최고", 2)], imgAt=-1, nameAt=-1)
SC['c20'] = KC("김선빈26", "김선빈", "3위 · 2024~2026년", big=BIGV("3년 30억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['c21'] = BAND("김선빈 · 2024년", [V("3할 2푼 9리", "타율", 1), V("한국시리즈 MVP", "", 2, hi=True, size=100)], bgk="김선빈26")
SC['c22'] = KC("김선빈26", "김선빈", "3위 · 3년 30억", big=VAL("2.44", 2), minor=[MI("세 시즌 모두", "WAR 2+", 0), MI("합계", "7.34", 1)])
SC['c22b'] = KCc("김선빈26", "김선빈", "3위 · 3년 30억", big=VAL("2.44", -1), minor=[MI("세 시즌 모두", "WAR 2+", -1), MI("합계", "7.34", -1)])
SC['c23'] = S(0, "rf_sil", n=2, bg=BGI("관중", "blur(22px) brightness(.4)"), noCenter=True)   # 같은 종류(남은 두 건)
# ── 4. 2위·1위 ──
SC['d1'] = KC("김선빈20", "김선빈", "2위 · 2020~2023년", big=BIGV("4년 40억", "", 1, size=170))   # 11/4 22:46 계약 기간 소개
SC['d1b'] = DUO("2020년 1월", [DC("안치홍", "안치홍", 1, [dict(k="이적", v="롯데", at=1)]), DC("김선빈26", "김선빈", 2, [dict(k="잔류", v="기아", at=2, hi=True)])], bgk="관중")
SC['d2'] = KC("김선빈20", "김선빈", "2위 · 4년 40억", big=BIGV("11.48", "4년 WAR", 1, size=200), minor=[MI("3할 타율", "세 시즌", 0)])
SC['d3'] = BAND("김선빈 · 4년 40억", [V("10억", "1년 몸값", 0), V("2.87", "10억당", 1, hi=True)], bgk="김선빈20")
SC['d4'] = RBARS("김선빈 시즌 WAR", [dict(label=f"{y}년", v=w, dec=2, at=0) for y, w in [(2020, 2.51), (2021, 3.04), (2022, 3.22), (2023, 2.71), (2024, 2.46), (2025, 2.11), (2026, 2.77)]], 4.4, bgk="김선빈20", ref=dict(v=2, lab="WAR 2", at=2), chain="sbw")
SC['d4b'] = RBARS("김선빈 시즌 WAR", [dict(label=f"{y}년", v=w, dec=2, at=-1) for y, w in [(2020, 2.51), (2021, 3.04), (2022, 3.22), (2023, 2.71), (2024, 2.46), (2025, 2.11), (2026, 2.77)]], 4.4, bgk="김선빈20", ref=dict(v=2, lab="WAR 2", at=-1), chain="sbw", cont=True, brkOff=150, brk=[dict(a=0, b=3, lab="2위 · 4년 40억", at=1), dict(a=4, b=6, lab="3위 · 3년 30억", at=1)])
SC['d5'] = RANK17("가성비 1위는?", hi=(1,), cont=False)
SC['d6'] = GOLDJ([dict(k="계약", v="4년 42억", at=50, hi=True)])
SC['d6a'] = GOLDJ([dict(k="계약", v="4년 42억", at=1, hi=True)])
SC['d6b'] = GOLDJ([dict(k="계약", v="4년 42억", at=-1, hi=True), dict(k="2005년 겨울 원소속팀 협상", v="마감일", at=1)], cont=True, cardAt=-1)
SC['d7'] = BAND("장성호 · 2006년", [V("3할 6리", "타율", 1), V("9년 연속", "3할", 2, hi=True), V("6.26", "WAR", 50, hi=True)], bgk="장성호", chain="jsh")
SC['d8'] = BAND("장성호 · 2006년", [V("3할 6리", "타율", -1), V("9년 연속", "3할", -1), V("6.26", "WAR", 0, hi=True)], bgk="장성호", chain="jsh", cont=True, whoAt=-1)
SC['d9'] = RBARS("장성호 시즌 WAR", [dict(label=f"{y}년", v=w, dec=2, at=0) for y, w in [(2006, 6.26), (2007, 3.27), (2008, 2.78), (2009, 1.57)]], 7, bgk="장성호", ref=dict(v=1.5, lab="WAR 1.5", at=1))
SC['d10'] = BAND("계약 마지막 해 2009년", [V("열 번째 우승", "기아", 1, hi=True)], bgk="장성호")
SC['d11'] = GOLDJ([dict(k="4년 WAR", v="13.88", at=0), dict(k="10억당", v="3.30", at=1, hi=True), dict(k="2위보다", v="+0.43", at=2)], cardAt=-1)
SC['d11']['chain'] = "jsh11"
SC['d12'] = GOLDJ([dict(k="2010년 시즌 중", v="한화로", at=2, hi=True)], cardAt=-1)
SC['d12']['chain'] = "jsh12"
SC['d13'] = GOLDJ([dict(k="2010년 시즌 중", v="한화로", at=-1, hi=True), dict(k="42억", v="회수", at=1)], cont=True, cardAt=-1)
SC['d13']['chain'] = "jsh12"
# ── 정리 ──
SC['e1'] = RANK17("기아 FA 17건 가성비 순위", names=True, cont=False, at=-1)
SC['e2'] = RANK17("기아 FA 17건 가성비 순위", names=True, hi=(1, 2, 3, 4), brk=dict(a=13, b=16, lab="1~4위 모두 잔류 FA", at=1))
SC['e3'] = RANK17("1~4위 = 잔류 FA", names=True, hi=(1, 2, 3, 4))
SC['e4'] = RANK17("1년 25억 이상 계약 세 건", names=True, hi=(8, 11, 14), cont=False, at=-1, hiAt=2)
SC['e5'] = RANK17("우승 2017년 · 2024년", names=True, hi=(8, 11, 14), at=-1)
SC['e6'] = RANK17("우승 2017년 · 2024년", names=True, hi=(8, 11, 14), at=-1)
BOARD_ALL = dict(type="rf_rank", head="기아 FA 가성비 순위", unit="", cols=["순위", "선수", "계약", "10억당 WAR"], open=17, next=None, last=None, noCenter=True, chain="fin", bg=BG_RED)
SC['e6b'] = dict(BOARD_ALL)
SC['e7'] = dict(BOARD_ALL, cont=True)
QQ = lambda a1, a2: [DC("최형우C", "최형우", a1, [dict(k="WAR 합계 1위", v="100억", at=a1)]), DC("장성호", "장성호", a2, [dict(k="가성비 1위", v="42억", at=a2, hi=True)])]
SC['e8'] = DUO("어느 계약이 최고였을까?", QQ(1, 3), bgk="관중", chain="q", reserveStats=True, cw=560)
SC['e9'] = DUO("어느 계약이 최고였을까?", [dict(c, at=-1, stats=[dict(s, at=-1) for s in c["stats"]]) for c in QQ(1, 3)], bgk="관중", chain="q", cont=True, reserveStats=True, cw=560)
SC['o3']['cw'] = 600

# ── 11/4 09:44 사용자 "선수와 순위가 공개될 때마다 순위표를 한번씩 잠깐 보여줘" ──
RANK_ROWS = [[r[0], r[1], r[2], ("%.2f" % r[3])] for r in RK]
SC['e6b']['rows'] = RANK_ROWS; SC['e7']['rows'] = RANK_ROWS
def BOARD_R(nxt, lead=0.6):   # 11/4 14:52 사용자 "이번엔 뺐어요 하고 17위는… 이 사이 텀이 너무 길어" — 쉼 1.2 → 0.6
    return dict(type="rf_rank", head="기아 FA 가성비 순위", unit="", cols=["순위", "선수", "계약", "10억당 WAR"], rows=RANK_ROWS, open=17 - nxt, next=nxt, last=(nxt + 1 if nxt < 17 else None), lead=lead, bg=BG_RED)
# 11/4 22:31 사용자 "순위표 장면에서 'N위는 누구예요' 나레이션이 나온 뒤에 선수 장면으로 넘어가고 설명 시작 — 다른 장면도 다" :
#   'N위는 OOO예요' 줄 = 순위표(다음 칸 깜빡 → 이름 말하는 순간 그 칸에 이름) · 다음 줄부터 선수 카드(줄 시작에 바로)
NAME = {r[0]: r[1] for r in RK}
REVEAL = [("a1r", 17, 2.25), ("a5r", 16, 2.25), ("a10r", 15, 2.25), ("a14", 14, 1.25), ("a20r", 13, 2.25), ("b1r", 12, 2.25), ("b4r", 11, 2.25),
          ("b12r", 10, 2.25), ("b16r", 9, 2.25), ("b22r", 8, 2.25), ("c2r", 7, 2.25), ("c6r", 6, 2.25), ("c12r", 5, 2.25), ("c16r", 4, 2.25),
          ("c20r", 3, 2.25), ("d1r", 2, 1.25), ("d6", 1, 1.25)]   # 11/5 01:20 힌트 / 이름 사이 텀 → 이름은 셋째 호흡   # 11/4 23:48 힌트 줄: 이름은 둘째 호흡 끝
HOLD = {'o13': 0.7, "a24": 0.7, "b29": 0.7, "c22b": 0.7, "d13": 0.7}   # 11/5 검수: 챕터 끝 줄 뒤 쉼
RV_KEYS = [r[0] for r in REVEAL]
for r_key, nxt, nat in REVEAL:
    SC[r_key] = dict(BOARD_R(nxt), noCenter=True, nextName=NAME[nxt], nextNameAt=nat); SC[r_key].pop("lead")
SC["d5"] = dict(BOARD_R(1), noCenter=True, chain="rk1"); SC["d5"].pop("lead")
SC["d6"]["chain"] = "rk1"; SC["d6"]["cont"] = True
# 11/5 10:28 사용자 "순위표에서 추가된 멘트까지 말하고 나서 다음 장면으로" — 근황 줄은 같은 순위표(이름 뜬 채 그대로), 선수 카드는 그다음 줄부터
NOW = {"a1r": "a1n", "a5r": "a5n", "a10r": "a10n", "a14": "a14n", "b4r": "b4n", "b12r": "b12n", "b16r": "b16n", "c2r": "c2n", "c6r": "c6n", "c20r": "c20n", "d6": "d6n"}
for r_key, n_key in NOW.items():
    ch = SC[r_key].get("chain") or ("rv" + r_key)
    SC[r_key]["chain"] = ch
    SC[n_key] = dict(SC[r_key], nextNameAt=-1, chain=ch, cont=True)
NOW_KEYS = list(NOW.values())


# 카드 사진: 선수 몸 중심(CX)을 칸 가운데로
CX = {'경기/김선빈_KIA_타격_2020_스포츠경향': 0.25, '경기/김주찬_KIA_타격_2015_스포츠경향': 0.55, '경기/김주찬_KIA_타격_2018_스포츠경향': 0.5, '경기/나성범_KIA_2025_스포츠경향': 0.5, '경기/나지완_KIA_홈런_2017_스포츠경향': 0.6, '경기/나지완_KS끝내기_2009_스포츠경향': 0.52, '경기/안치홍_KIA_2019_스포츠경향': 0.55, '경기/양현종_KIA_20승_2017_스포츠경향': 0.5, '경기/양현종_KIA_투구_2022_스포츠경향': 0.45, '경기/윤석민_KIA_세이브_2015_스포츠경향': 0.55, '경기/이대형_KIA_주루_2014_스포츠경향': 0.45, '경기/이범호_KS만루홈런_2017_스포츠경향': 0.5, '경기/최형우_KIA_타격_2017_스포츠경향': 0.45, '경기/최형우_KIA_타격왕_2020_스포츠경향': 0.5, '경기/최형우_KIA_홈런세리머니_2017_스포츠경향': 0.55, '누끼/KBO스타일_경기_김범수_투구_0729_KIA제공_up_center': 0.5, '경기/양현종_글러브_1012_KIA제공': 0.5, '경기/나성범_세리머니_KIA제공': 0.52, '경기/김선빈_스퀴즈_1012_KIA제공': 0.42, '경기/장성호_KIA_주루_2008_스포츠경향': 0.35}
SZ = {'경기/김선빈_KIA_타격_2020_스포츠경향': (1200, 747), '경기/김주찬_KIA_타격_2015_스포츠경향': (1200, 1861), '경기/김주찬_KIA_타격_2018_스포츠경향': (700, 998), '경기/나성범_KIA_2025_스포츠경향': (1200, 1800), '경기/나지완_KIA_홈런_2017_스포츠경향': (1200, 1522), '경기/나지완_KS끝내기_2009_스포츠경향': (1200, 594), '경기/안치홍_KIA_2019_스포츠경향': (700, 912), '경기/양현종_KIA_20승_2017_스포츠경향': (600, 784), '경기/양현종_KIA_투구_2022_스포츠경향': (700, 1050), '경기/윤석민_KIA_세이브_2015_스포츠경향': (1200, 1495), '경기/이대형_KIA_주루_2014_스포츠경향': (1200, 1008), '경기/이범호_KS만루홈런_2017_스포츠경향': (1200, 814), '경기/최형우_KIA_타격_2017_스포츠경향': (600, 770), '경기/최형우_KIA_타격왕_2020_스포츠경향': (1200, 1575), '경기/최형우_KIA_홈런세리머니_2017_스포츠경향': (600, 641), '누끼/KBO스타일_경기_김범수_투구_0729_KIA제공_up_center': (654, 840), '경기/양현종_글러브_1012_KIA제공': (1280, 853), '경기/나성범_세리머니_KIA제공': (1200, 800), '경기/김선빈_스퀴즈_1012_KIA제공': (960, 800), '경기/장성호_KIA_주루_2008_스포츠경향': (500, 750)}
def _fx(img, bw, bh, tx, f):
    if img not in CX or img not in SZ: return f
    W, H = SZ[img]; s = max(bw / W, bh / H); sw = W * s
    y = (f or "50% 18%").split()[1] if f and len(f.split()) > 1 else "18%"
    if sw - bw < 2: return "50% " + y
    p = (CX[img] * sw - tx * bw) / (sw - bw); p = min(1, max(0, p))
    return f"{round(p * 100)}% {y}"
KEEPF = {"경기/이창진_KS4_엑스포츠"}   # 워터마크 피하려고 정한 위치는 그대로
for _k, _s in SC.items():
    t = _s.get("type")
    if t == "rf_card" and _s.get("img") not in KEEPF: _s["focus"] = _fx(_s.get("img"), 700, 714, .46, _s.get("focus"))
    elif t == "rf_gold": _s["focus"] = _fx(_s.get("img"), 474, 674, .5, _s.get("focus"))
    elif t == "rf_duo":
        cw = _s.get("cw") or (520 if len(_s.get("cards", [])) > 2 else 680)
        _s["cards"] = [dict(c, focus=_fx(c.get("img"), cw, 590, .5, c.get("focus"))) for c in _s.get("cards", [])]

for _k in [k for k in SC if k not in KEYS]: SC.pop(_k)
missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing and not extra, (missing, extra)
lines, scenes = [], []
for j, (k, narr, sub) in enumerate(_t.LINES):
    sc = dict(SC[k]); sc['startLine'] = j
    lines.append(L(narr, sub)); scenes.append(sc)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})
scenes.append(dict(END_SC, startLine=len(lines) - 1, bg=BG_RED))   # 11/4 사용자 "배경 템플릿도 다른 장면이랑 어울리게" — 엔딩도 빨간 줄무늬 어두운 바탕

def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
CH = [ch("기아 FA 17위~13위", "a1r", "a24"), ch("기아 FA 12위~8위", "b1r", "b29"), ch("기아 FA 7위~3위", "c1", "c22b"), ch("기아 FA 2위·1위", "c23", "d13"), ch("기아 FA 가장 남는 장사", "e1", "e9")]
DESC = ("기아 타이거즈 역대 FA 돈값 순위 — 2003년 겨울부터 기아가 맺은 20억 원 이상 FA 계약 17건을 가성비 순서로 줄 세웠어요. 최형우 4년 100억, 나성범 6년 150억까지, 가장 남는 장사는 누구였을까요?\n\n"
        "기준: 1년 몸값 10억 원마다 한 시즌 WAR이 얼마인지 = (계약 기간 기아에서 기록한 WAR ÷ 뛴 시즌 수) ÷ (총액 ÷ 계약 연수) × 10(둘째 자리에서 자름). WAR은 스탯티즈 기준이고, 계약이 남은 나성범·양현종(2+1년 45억)·김범수는 2026시즌까지 성적으로 계산했어요. 17건 평균은 10억당 1.77이에요. 양현종 4년 103억은 옵션 48억까지 다 받은 걸로 치고 계산했어요.\n\n"
        "순위에 든 계약: 최형우(4년 100억·3년 47억), 나성범 6년 150억, 양현종(1년 22억 5천만 원·4년 103억·2+1년 45억), 김선빈(4년 40억·3년 30억), 김주찬(4년 50억·2+1년 27억), 윤석민 4년 90억, 이범호 3+1년 36억, 나지완 4년 40억, 이대형 4년 24억, 마해영 4년 28억, 장성호 4년 42억, 김범수 3년 20억. 안치홍이 롯데로 떠난 2020년 1월 이야기도 함께 담았어요.\n\n"
        "1년 25억 원 이상 큰 계약 세 건(최형우 100억·나성범 150억·양현종 103억)의 순위는 영상에서 확인해 주세요. 세 계약 모두 계약 기간 안에 우승(2017년·2024년)이 있었어요.\n\n"
        "야구자판기는 매일 야구 이슈를 정리해요. 여러분은 기아 역대 FA 가운데 어느 계약이 최고였다고 보세요? WAR이 가장 높은 최형우 100억? 아니면 가성비 1위 계약? 댓글로 남겨 주세요.\n\n▶ 지난 영상: 롯데 2027 스토브리그\n\n"
        "#기아타이거즈 #기아FA #최형우 #나성범 #양현종 #김선빈 #프로야구 #야구자판기\n")
TAGS = ["기아 역대 FA", "기아 FA 돈값", "기아 FA 순위", "FA 가성비", "기아 타이거즈", "KIA 타이거즈", "최형우", "나성범", "양현종", "김선빈", "장성호", "윤석민", "이범호", "프로야구", "KBO"]
SOURCE = "사실 출처 = 계약: 기사 원문 2곳 이상(kfa/contracts.md) · 성적: KBO 기록실 · WAR: 스탯티즈 11/4 확인(kfa/audit/statiz_war_1104.md)"
EP = {"theme": "m3", "introChapter": "오프닝", "date": "2026-11-05", "gameDate": "2026-11-05", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1105-kfa-v1", "topic": "기아역대FA돈값", "endcardSec": 10, "gapScale": 1.3, "pauseMax": 0.5, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "기아 역대 FA 돈값 순위 | 최형우 100억·나성범 150억보다 남는 장사", "description": DESC, "tags": TAGS, "hashtags": ["#기아타이거즈", "#기아FA", "#최형우", "#나성범", "#양현종", "#김선빈", "#프로야구", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'd5', 'e8')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    for _k, _h in HOLD.items(): EP['lines'][KEYS.index(_k)]['holdAfter'] = _h
    for _k in NOW_KEYS: EP['lines'][KEYS.index(_k)]['holdAfter'] = 0.7   # 11/5 10:28 근황 줄 뒤 순위표 머묾 → 카드
    for _k in RV_KEYS:
        if _k in NOW: EP['lines'][KEYS.index(_k)]['noMerge'] = True; continue   # 11/5 11:22 사용자 "김범수예요 / 현재 기아 불펜에서 — 텀이 너무 길어" → 근황 줄이 이어지면 0.7초 머묾 없이 보통 줄 사이 텀만
        EP['lines'][KEYS.index(_k)]['holdAfter'] = 0.7; EP['lines'][KEYS.index(_k)]['noMerge'] = True   # 11/5 검수: '8위는'처럼 짧은 첫 조각도 자막 따로   # 11/5 01:20 사용자 "순위표에서 몇 위는 누구예요 할 때 특히 빨라서 휙휙" — 이름 공개 뒤 순위표에 0.7초 머묾   # 순위표 보여 줄 쉼
    # 11/4 16시 검수본(132줄)과 대사가 같은 줄은 그 음성을 새 번호로 옮긴다(voiceRemap, 재합성 0) — 바뀐 15줄만 새로 합성
    _vo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voice_old_1105.json')
    if os.path.exists(_vo):
        _old = json.load(open(_vo, encoding='utf-8'))
        EP['voiceRemap'] = [(_old.index(l['narr']) if l['narr'] in _old else None) for l in EP['lines']]
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-05_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
