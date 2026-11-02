# -*- coding: utf-8 -*-
"""11/2 롱폼 「기아 2027 스토브리그」 콘티 (회사 PC · 음성 API).
대사 = tools/text_1102_kia.py. 근거 = 기사 원문 2곳 이상(kia27 facts_A·B).
실행: python -X utf8 tools/gen_1102_kia.py → episodes/2026-11-02_롱폼2.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t36', os.path.join(HERE, 'text_1102_kia.py'))
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

# ── 롱폼 ① 기아 2027 스토브리그 장면 — 새 디자인(11/2): 주 A3 rf_card · B3 rf_bars · C1 rf_band / 섞기 A1 rf_gold · B1 rf_bars(glass) · C3 rf_duo, 바탕 테마 m3 ──
P = {
    "카스트로": "경기/카스트로_홈런세리머니_1010_KIA제공", "카스트로B": "경기/카스트로_엄지_0810_KIA제공", "카스트로C": "경기/카스트로_홈런후_1009_KIA제공", "카스트로K": "KBO프로필/카스트로",
    "네일": "경기/네일_역투_KIA제공", "네일B": "경기/네일_주먹환호_KIA제공", "네일C": "경기/네일_하늘가리키기_1012_스포츠조선", "네일K": "KBO프로필/네일",
    "올러": "경기/올러_포효_0929_KIA제공", "올러B": "경기/올러_경기_KIA제공_세로", "올러C": "경기/올러_포효_0412_뉴스1", "올러K": "KBO프로필/올러",
    "김도영": "경기/김도영_45호_타격_1012_KIA제공", "김도영B": "경기/김도영_덕아웃_KIA제공", "김도영C": "경기/김도영_45호_덕아웃_1012_KIA제공",
    "이범호": "경기/이범호_박수_0915_KIA제공_세로", "이창진": "경기/이창진_KS4_엑스포츠", "홍건희": "경기/홍건희_KIA투구_SPOTV", "정해영": "경기/정해영_마운드_마이데일리",
    "김태군": "경기/김태군_덕아웃_0729_KIA제공", "김호령": "경기/김호령_만루포_0821_KIA제공_세로", "김호령B": "경기/김호령_환호_연합뉴스", "김선빈": "경기/김선빈_스퀴즈_1012_KIA제공",
    "박찬호": "경기/박찬호_타격_0922_두산제공", "최형우": "경기/최형우_만루포미소_0826_삼성제공_세로", "최형우B": "경기/최형우_100타점_0918_삼성제공_중앙_세로",
    "시라카와": "경기/시라카와_투구_KIA제공", "김범수": "경기/김범수_투구_0729_KIA제공", "조상우": "카드/FA10_조상우", "하주석": "경기/하주석_인사_KIA제공",
    "광주": "경기/광주_전경_1017_KIA제공", "카스트로D": "카드/P18_카스트로_환호", "카스트로E": "카드/FA9_카스트로_홈런", "네일D": "카드/P17_네일_역투", "네일E": "카드/P17_네일_포효", "올러D": "카드/P18_올러_포효", "올러E": "카드/P18_올러_투구", "올러F": "경기/올러_하이파이브_1018", "김도영D": "카드/P22_김도영_포효_중앙", "김도영K": "KBO프로필/김도영", "김호령C": "카드/F16_김호령_A", "한승택": "경기/한승택_세리머니_0915_KT제공", "양현종": "경기/양현종_글러브_1012_KIA제공", "관중": "경기/광주_관중_1017_KIA제공",
    "고종욱K": "KBO프로필/고종욱_KIA", "이창진K": "KBO프로필/이창진_KIA", "홍건희K": "KBO프로필/홍건희_KIA", "김사윤K": "KBO프로필/김사윤_KIA", "김대유K": "KBO프로필/김대유_KIA", "윤중현K": "KBO프로필/윤중현_KIA",
}
P.update({"한준수": "경기/한준수_주루_KIA제공", "네일F": "경기/네일_포효_엑스포츠뉴스", "김도영E": "경기/김도영_포효_스포츠조선", "잠실승리": "경기/KIA_잠실마지막승리_1020_연합", "올러카": "경기/올러_카스트로_1018", "이호민": "경기/이호민_드래프트_0921_KIA제공"})
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

FOR3 = [DC("카스트로D", "카스트로", 2, focus="50% 25%"), DC("네일D", "네일", 2, focus="50% 25%"), DC("올러D", "올러", 2, focus="50% 25%")]
# ── 오프닝 ──
SC['o1'] = DUO("기아 2027 스토브리그", FOR3, bgk="광주")
SC['o2'] = S(0, "rf_band", who="11월 1일 · 플레이오프 5차전", team="KIA", vals=[V("1대6", "삼성 승", 3), V("2승 3패", "시리즈 탈락", 4, hi=True)], bg=BGI("관중", BAND_F), noCenter=True)
SC['o3'] = BAND("기아 정규시즌 순위", [V("8위", "2025년", 0), V("3위", "2026년", 1, hi=True)], bgk="잠실승리")
SC['o4'] = S(0, "toc", itemFrom=1)
# ── 1. 떠나는 사람 ──
REL = [FI("고종욱K", "고종욱", 0), FI("이창진K", "이창진", 0), FI("홍건희K", "홍건희", 1), FI("김사윤K", "김사윤", 1), FI("김대유K", "김대유", 1), FI("윤중현K", "윤중현", 1)]
SC['n1'] = FG("2027년 재계약 불가", [], chain="rel", text="10월 23일 · 여섯 명", textAt=50)
SC['n2'] = FG("2027년 재계약 불가", [], chain="rel", cont=True, text="10월 23일 · 여섯 명", textAt=1)
SC['n3'] = FG("2027년 재계약 불가", REL, chain="rel", cont=True, text="10월 23일 · 여섯 명", textAt=-1)
SC['n4'] = CARD("이창진", "이창진", "외야수", big=BIGV("3", "경기", 3, sub="2026년 1군"), minor=[MI("2024년", "우승 멤버", 1)])
SC['n5'] = CARD("홍건희", "홍건희", "투수", big=BIGV("1년 7억", "", 2, size=170), minor=[MI("2027년", "재계약 불가", 3)])
SC['n6'] = FG("상무 입대", [FI("KBO프로필/정해영", "정해영", 1), FI("KBO프로필/한재승", "한재승", 1), FI("KBO프로필/윤도현", "윤도현", 2)], text="12월 입대 · 2028년 6월 복귀", textAt=3)
SC["n8"] = DUO("FA 자격 취득 유력", [DC("김태군", "김태군", 3), DC("김호령", "김호령", 3)])
SC['n8']['bg'] = BG_DARK
SC['n10'] = S(0, "rf_band", who="김호령 · 플레이오프", team="KIA", vals=[V("4", "3차전 삼진", 2), V("제외", "5차전 선발", 3, hi=True)], bg=BGI("김호령C", BAND_F), noCenter=True, chain="hr", tag="FA 몸값 ↓?", tagAt=50)
SC['n10b'] = S(0, "rf_band", who="김호령 · 플레이오프", team="KIA", vals=[V("4", "3차전 삼진", -1), V("제외", "5차전 선발", -1, hi=True)], tag="FA 몸값 ↓?", bg=BGI("김호령C", BAND_F), whoAt=-1, noCenter=True, chain="hr", cont=True)
SC['n12'] = CARD("김선빈", "김선빈", "2루수", big=BIGV("3년 30억", "", 1, size=170), minor=[MI("계약 끝", "2026년", 2)], imgAt=0)
SC['n13'] = DUO("2025년 겨울 떠난 내부 FA", [DC("박찬호", "박찬호", 2, team="두산"), DC("최형우", "최형우", 2, team="삼성")], chain="left", reserveStats=True)
SC['n13']['bg'] = BG_NAVY
SC['n14'] = DUO("2025년 겨울 떠난 내부 FA", [DC("박찬호", "박찬호", -1, [dict(k="두산", v="4년 80억", at=1)], team="두산"), DC("최형우", "최형우", -1, [dict(k="삼성", v="2년 26억", at=3)], team="삼성")], chain="left", cont=True, reserveStats=True)
SC['n14']['bg'] = BG_NAVY
SC['n14b'] = S(0, "rf_card", img=ph("한승택"), name="한승택", team="KT", kicker="포수", big=BIGV("4년 10억", "", 1, size=170), bg=BG_DARK, noCenter=True)
SC['n16'] = SLOT("2026년 겨울 첫 숙제", [SL("김호령C", "김호령", "중견수", 2), SL("김태군", "김태군", "포수", 2)], chain="job", profile=False)
SC['n16b'] = CARD("한준수", "한준수", "포수", big=BIGV("안방 부담", "", 3, size=150), minor=[MI("김태군", "FA 협상", 1)], imgAt=2, nameAt=2)
# ── 2. 카스트로·네일·올러 ──
F3 = [SL("카스트로K", "카스트로", "타자"), SL("네일K", "네일", "투수"), SL("올러K", "올러", "투수")]
SC['f1'] = SLOT("2026 기아 외국인 선수", [dict(F3[0], at=2), dict(F3[1], at=3), dict(F3[2], at=3)])
SC['f3'] = GOLD("카스트로", "카스트로", "HAROLD CASTRO", ["KIA 타이거즈", "타자"], [dict(k="기아에서", v="첫 시즌", at=1, hi=True)])
SC['f4'] = BAND("카스트로 · 2026 정규시즌", [V("99", "경기", 3), V("3할 2푼 7리", "타율", 4, hi=True, size=104), V("21", "홈런", 5), V("88", "타점", 5)], bgk="카스트로B")
SC['f5'] = CARD("카스트로E", "카스트로", "플레이오프 1차전", big=BIGV("3", "안타", 3, sub="3타점"), minor=[MI("홈런", "투런", 2)])
SC['f6'] = CARD("카스트로B", "카스트로", "2026년 총액", big=BIGV("100만", "달러", 1), minor=[MI("세 명 중", "가장 적음", 2)])
SC['f7'] = SP("김도영B", "김도영", [BB("", "카스트로가 빨리\n계약하면 좋겠다", 2, hi=True)])
SC['f8'] = DUO("\"카스트로가 너무 고맙다\"", [DC("카스트로E", "카스트로", 0), DC("김도영D", "김도영", 0)], bgk="광주", chain="kc", reserveStats=True)
SC['f9'] = DUO("카스트로도 남고 싶다", [DC("카스트로E", "카스트로", -1, [dict(k="김도영에게", v="재계약 부탁", at=1)]), DC("김도영D", "김도영", -1)], bgk="광주", chain="kc", cont=True, reserveStats=True)
SC['f10b'] = CARD("카스트로C", "카스트로", "2027년 숙제", big=BIGV("부상 없이", "한 시즌?", 1, size=150), minor=[MI("2026년", "시즌 초 부상", 0)])
SC['f11'] = GOLD("네일", "네일", "JAMES NAILE", ["KIA 타이거즈", "투수"], [dict(k="기아에서", v="세 번째 시즌", at=1, hi=True, size=84)])
SC['f11b'] = CARD("네일B", "네일", "2025년 겨울", big=BIGV("메이저리그 관심", "", 3, size=110), minor=[MI("선택", "기아 잔류", 4)])
SC['f12'] = BAND("네일 · 2026 정규시즌", [V("31", "경기", 1), V("13", "승", 2), V("3.49", "평균자책점", 3, hi=True)], bgk="네일E")
SC['f13'] = CARD("네일", "네일", "플레이오프 1차전", big=BIGV("1안타", "4회까지", 1, size=180), minor=[MI("다음 이닝", "헤드샷 퇴장", 2)])
SC['f14'] = CARD("네일D", "네일", "플레이오프 4차전", big=BIGV("4대2", "역전승", 2), minor=[MI("1승 2패", "선발 등판", 0)])
SC['f15'] = CARD("네일F", "네일", "2026년 총액", big=BIGV("200만", "달러", 3), minor=[MI("세 명 중", "가장 많음", 4)], imgAt=1, nameAt=1)
SC['f16'] = GOLD("올러", "올러", "ADAM OLLER", ["KIA 타이거즈", "투수"], [dict(k="기아에서", v="두 번째 시즌", at=1, hi=True, size=84)])
SC['f17'] = BAND("올러 · 2026 정규시즌", [V("11", "승", 2), V("3.13", "평균자책점", 3, hi=True)], bgk="올러E")
SC['f17b'] = RBARS("올러 시즌 승수", [dict(label="2025년", v=11, at=0, unit="승"), dict(label="2026년", v=11, at=-1, unit="승")], 15, glass=True, ref=dict(v=10, lab="두 자릿수", at=1))
SC['f18'] = CARD("올러B", "올러", "플레이오프 · 대구 원정", big=BIGV("2경기", "모두 조기 강판", 2, size=170), imgAt=0)
SC['f19'] = S(0, "rf_band", who="올러 · 플레이오프 대구 원정", team="KIA", vals=[V("4⅔", "2차전 이닝", 1), V("5", "2차전 실점", 1, hi=True), V("2", "5차전 이닝", 2), V("4", "5차전 실점", 2, hi=True)], bg=BGI("올러C", BAND_F), noCenter=True)
SC['f20'] = CARD("올러F", "올러", "2026년 총액", big=BIGV("120만", "달러", 1))
SC['f21'] = SLOT("시즌 중 나온 전망", [SL("올러K", "올러", "", 1), SL("카스트로K", "카스트로", "", 1), SL("네일K", "네일", "", 3, tag="깎아서 재계약?", tagAt=3, tc="bad")], bracket=dict(a=0, b=1, label="몸값 오른다", at=2, c="gold"))
SEGS = [SEG("카스트로", 100, 0, "#3B4A63"), SEG("올러", 120, 0, "#E8A100"), SEG("네일", 200, 0)]
SC['f22'] = CAP("외국인 선수 총액 한도", [], cap=400, capAt=3, capLabel="한도 400만 달러")
SC['f24'] = CAP("외국인 선수 총액 한도", [], cap=400, capAt=-1, capLabel="한도 400만 달러", cont=True, text="재계약 연차마다 +10만 달러", textAt=2, size=60)
SC['f25'] = CAP("외국인 선수 총액 한도", [dict(x, at=0) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", cont=True, text="2026년 총액 합계 420만 달러", textAt=1, size=60)
SC['f25b'] = CAP("외국인 선수 총액 한도", [dict(x, at=-1) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", ext=430, extAt=3, extLabel="2026년 한도 430만 달러", cont=True, text="2026년 총액 합계 420만 달러", textAt=-1, size=60)
SC['f26'] = CAP("외국인 선수 총액 한도", [dict(x, at=-1) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", ext=460, extAt=3, extLabel="2027년 최대 460만 달러", cont=True, text="2026년 총액 합계 420만 달러", textAt=-1, size=60)
SC['f27'] = CAP("외국인 선수 총액 한도", [dict(x, at=-1) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", ext=460, extAt=-1, extLabel="2027년 최대 460만 달러", cont=True, text="여유 40만 달러", textAt=1, size=60)
EX = [SL("카스트로K", "카스트로", "", -1, money="150만 달러"), SL("네일K", "네일", "", -1, money="200만 달러"), SL("올러K", "올러", "", -1, money="110만 달러")]
SC['f27b'] = SLOT("예시 · 2027년 한도 안에서", [dict(EX[0], at=1), dict(EX[1], at=3), dict(EX[2], at=4)], chain="ex")
SC['f27c'] = SLOT("예시 · 2027년 한도 안에서", [EX[0], EX[1], dict(EX[2], tag="2026년보다 적음", tagAt=0, tc="bad")], chain="ex", cont=True)
SC['f32'] = CARD("시라카와", "시라카와", "아시아쿼터 · 투수", big=BIGV("시즌 중", "합류", 3, sub="선발 한 자리", size=150), imgAt=1, nameAt=1)
SC['f32b'] = BAND("아시아쿼터 선수", [V("20만 달러", "첫 계약 총액 한도", 2, hi=True, size=110)], bgk="시라카와")
V3 = [SL("카스트로K", "카스트로", ""), SL("네일K", "네일", ""), SL("올러K", "올러", "")]
def verdict(tags, cont=True):
    sl = [dict(x) for x in V3]
    for i, (t, a, c) in enumerate(tags):
        if t: sl[i].update(tag=t, tagAt=a, tc=c)
    return SLOT("2027 기아 외국인 재계약 전망", sl, chain="vd", **({"cont": True} if cont else {}))
SC['f28'] = verdict([(None, 0, ''), (None, 0, ''), (None, 0, '')], cont=False)
SC['f29'] = verdict([("잔류 유력", 1, "good"), (None, 0, ''), (None, 0, '')])
SC['f30'] = verdict([("잔류 유력", -1, "good"), ("몸값 관건", 1, "gold"), (None, 0, '')])
SC['f30b'] = verdict([("잔류 유력", -1, "good"), ("몸값 관건", -1, "gold"), (None, 0, '')])
SC['f31'] = verdict([("잔류 유력", -1, "good"), ("몸값 관건", -1, "gold"), ("반반", 1, "bad")])
SC['f31b'] = BAND("새 외국인 선수 몸값", [V("몸값 ↑", "올러가 원한다면", 0), V("100만 달러", "새 선수 첫해 상한", 2, hi=True)], bgk="올러카")
# ── 3. 들어오는 사람 ──
SC['i1'] = BAND("기아에 들어오는 사람", [], bgk="광주")
SC['i2'] = CARD("이호민", "이호민", "경남고 내야수", big=BIGV("3순위", "전체", 3), minor=[MI("2027 신인 드래프트", "1라운드", 1)], imgAt=2, nameAt=2, focus="50% 5%")
SC['i3'] = S(0, "quote", src="기아 스카우트", text="1년에 한두 명 나올 만한\n우타 거포형 재목", chain="iq")
SC['i4'] = S(0, "quote", src="기아 스카우트", text="프로에서 수비 빌드업을 잘 거친다면\n이범호 감독급 3루수가 될 것", chain="iq", cont=True, name="이범호", role="감독")
SC['i9'] = DUO("백업 내야가 과제", [DC("김선빈", "김선빈", 3), DC("하주석", "하주석", 3)])
SC['i9']['bg'] = BG_DARK
# ── 4. 2027년 기아 ──
SC['p1'] = BAND("2027년 기아는?", [], bgk="관중")
SC['p3'] = CARD("김도영", "김도영", "45홈런 · 홈런왕", big=BIGV("2028", "시즌 뒤", 4, sub="빠르면 도전"), minor=[MI("2026년 겨울", "도전 불가", 2)], imgAt=0, nameAt=0)
SC['i10b'] = CARD("김도영E", "김도영", "2026 아시안게임", big=BIGV("금메달", "병역 해결", 1, size=170), minor=[MI("메이저리그", "여러 구단 관심", 2)])
SC['i10c'] = BAND("김도영과 함께 우승을 노릴 시간", [V("2027 · 2028", "가장 확실한 두 시즌", 1, hi=True, size=120)], bgk="김도영B")
SC['p4'] = SP("이범호", "이범호", [BB("", "내년에 당연히 한국시리즈 간다고\n생각하면 오산", 2, hi=True), BB("", "", 50)], chain="lbh")
SC['p5'] = SP("이범호", "이범호", [BB("", "내년에 당연히 한국시리즈 간다고\n생각하면 오산", -1, hi=True), BB("", "부족한 부분을 찾아서\n잘 채우겠다", 0)], chain="lbh", cont=True)
SC['p5b'] = SP("양현종", "양현종", [BB("", "솔직히 1·2위 팀보다\n전력이 약하지 않나", 2, hi=True), BB("", "고개 숙이지 마", 4)])
SC['p6'] = DUO("2027 기아의 열쇠", [DC("카스트로C", "카스트로", 2, focus="50% 20%"), DC("네일B", "네일", 2, focus="50% 20%"), DC("올러C", "올러", 2, focus="50% 20%")])
SC['p6']['bg'] = BG_RED
NP = [SL("네일K", "네일", "", x=True, xAt=0), SL("올러K", "올러", "", x=True, xAt=0), SL(None, "새 투수", "", at=2), SL(None, "새 투수", "", at=2)]
SC['p7'] = SLOT("선발 두 자리 교체", NP)
SC['p8b'] = CARD("카스트로D", "카스트로", "2026년", big=BIGV("첫 시즌", "한국 무대", 3, size=170), imgAt=2, nameAt=2)
SC['p9'] = BAND("셋 다 남고 내부 FA까지 잡으면", [V("상위권", "2027년도", 3, hi=True)], bgk="잠실승리")
SC['p10b'] = SLOT("한 명만 바뀐다면", [SL("올러K", "올러", "", 1, x=True, xAt=1), SL(None, "새 투수", "", 2, tag="상위권 싸움", tagAt=3, tc="good")])
SC['p10'] = S(0, "rf_band", who="외국인 두 명 이상 교체", team="KIA", vals=[V("5강 싸움", "다시 시작", 1, hi=True)], bg=BGI("광주", BAND_F), noCenter=True)
SC['p11'] = verdict([("잔류 유력", 1, "good"), ("몸값 관건", 2, "gold"), ("반반", 3, "bad")], cont=False)
SC['q1'] = DUO("셋 다 남을까? 한 명 이상 바뀔까?", [DC("카스트로", "카스트로", 2), DC("네일E", "네일", 2), DC("올러F", "올러", 2)], bgk="관중")

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
CH = [ch("기아를 떠나는 사람", "n1", "n16b"), ch("남을지 모르는 외국인 세 명", "f1", "f32b"), ch("기아에 들어오는 사람", "i1", "i9"), ch("2027년 기아 예상", "p1", "q1")]
DESC = ("기아 타이거즈 2027 스토브리그 — 2026년 플레이오프에서 삼성에 2승 3패로 탈락한 기아의 겨울, 외국인 선수 카스트로·네일·올러 재계약 전망과 떠나는 사람·들어오는 사람을 정리했어요.\n"
        "카스트로·네일·올러는 2027년에도 기아에 남을까요?\n\n"
        "떠나는 사람: 기아는 10월 23일 고종욱·이창진·홍건희·김사윤·김대유·윤중현과 2027년 재계약을 하지 않기로 했어요. 정해영·한재승·윤도현은 12월 상무에 입대해 2028년 6월 돌아오고, 포수 김태군·중견수 김호령은 FA 자격 취득이 유력해요. 김선빈의 3년 30억 원 계약도 2026년으로 끝나요. 2025년 겨울엔 박찬호(두산 4년 80억 원)·최형우(삼성 2년 26억 원)·한승택(KT 4년 10억 원)이 떠났어요.\n\n"
        "해럴드 카스트로·제임스 네일·아담 올러: 카스트로는 99경기 타율 3할 2푼 7리 21홈런 88타점에 2026년 총액 100만 달러. 네일은 31경기 13승 평균자책점 3.49에 총액 200만 달러, 올러는 11승 평균자책점 3.13에 총액 120만 달러. 외국인 3명 계약 총액 한도는 400만 달러이고 재계약 연차마다 선수당 10만 달러씩 늘어나요 — 규정대로 계산하면 2026년 한도는 430만 달러, 셋 다 재계약하면 2027년 한도는 최대 460만 달러예요. 아시아쿼터 시라카와 케이쇼도 재계약 대상이에요.\n\n"
        "들어오는 사람: 2027 신인 드래프트 1라운드 전체 3순위 경남고 내야수 이호민.\n\n"
        "제 예상: 카스트로는 잔류 유력, 네일은 몸값이 관건, 올러는 반반. 셋 중 한 명만 바뀐다면 올러일 가능성이 가장 커요. 김도영은 빠르면 2028시즌 뒤 메이저리그에 도전할 수 있어서, 2027·2028년이 김도영과 함께 우승을 노릴 가장 확실한 두 시즌이라고 봐요.\n\n"
        "야구자판기는 매일 야구 이슈를 정리해요. 카스트로·네일·올러, 셋 다 남을까요? 아니면 한 명 이상 바뀔까요? 댓글로 알려 주세요.\n\n▶ 지난 영상: \n\n"
        "#기아타이거즈 #기아스토브리그 #카스트로 #제임스네일 #올러 #김도영 #프로야구 #야구자판기\n")
TAGS = ["기아 스토브리그", "기아 2027", "기아 타이거즈", "KIA 타이거즈", "기아 외국인 선수", "카스트로", "제임스 네일", "올러", "김도영", "김호령", "김태군", "이호민", "이범호", "프로야구", "KBO"]
SOURCE = "사실 출처 = 기사 원문 2곳 이상 — /home/claude/kia27/facts_A.md, facts_B.md (일간스포츠·스포츠경향·OSEN·스타뉴스·엑스포츠뉴스·SPOTV·뉴시스·파이낸셜뉴스·데일리안·마이데일리)"
EP = {"theme": "m3", "introChapter": "오프닝", "date": "2026-11-02", "gameDate": "2026-11-02", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1102-kia27-v1", "topic": "기아2027스토브리그", "endcardSec": 20, "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "기아 2027 스토브리그 | 카스트로·네일·올러 남을까? 떠나는 사람·들어오는 사람 총정리", "description": DESC, "tags": TAGS, "hashtags": ["#기아타이거즈", "#기아스토브리그", "#카스트로", "#제임스네일", "#올러", "#김도영", "#프로야구", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'q1')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-02_롱폼2.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
