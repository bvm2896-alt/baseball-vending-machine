# -*- coding: utf-8 -*-
"""11/7 롱폼 「2027 FA 큰손 순위 — 10개 구단 샐러리캡 여유」 콘티.
대사 = tools/text_1107_fabig.py. 근거 = 데일리안·더게이트 2025-12-18 구단별 상위 40명 합계, 시사저널·OSEN 상한액 (fabig/research_*.md).
실행: python -X utf8 tools/gen_1107_fabig.py → episodes/2026-11-07_롱폼.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t36', os.path.join(HERE, 'text_1107_fabig.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
KEYS = [x[0] for x in _t.LINES]

BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억|(?:^| )다|(?:^| )못|(?:^| )안|(?:^| )만|(?:^| )(?:이번|지난|다음|올|그)|(?:^| )(?:네|다섯|여섯|일곱|여덟|아홉|열|열일곱)|중심|KBO|기아|WAR|\d+할|남는|좋은|\d+푼|\d+천만|역대|(?:^| )수|(?:^| )할|상위|넘은|(?:^| )더|\d+ FA)$'); BAD_B = re.compile(r'^(건|타선|겨울|코치|차|\d+차전|첫 |것 |수 |때 |중 |구단|달러|일|명|개|경기|원|타수|안타|\d+(?:푼|리)(?![가-힣]*할))')
WRAP = {'마음대로 쓸 수 있는 건 아니에요': '마음대로 쓸 수 있는 건\n아니에요', '구단마다 상위 40명 연봉 합계에': '구단마다\n상위 40명 연봉 합계에', '구단별 2025시즌 합계를 빼 봤어요': '구단별\n2025시즌 합계를 빼 봤어요', '10개 구단 가운데 가장 많았고': '10개 구단 가운데\n가장 많았고', '10개 구단 가운데 가장 적었고': '10개 구단 가운데\n가장 적었고', '보상금만 최소 20억 원이 들어서': '보상금만\n최소 20억 원이 들어서', '그때는 넘은 돈의 50%를 냈는데': '그때는\n넘은 돈의 50%를 냈는데', '류지현 감독이 새로 지휘봉을 잡았죠': '류지현 감독이\n새로 지휘봉을 잡았죠', '노시환의 메이저리그 포스팅을 요청했어요': '노시환의\n메이저리그 포스팅을 요청했어요', 'FA 세 명과 맺은 170억 계약이': 'FA 세 명과\n맺은 170억 계약이', '모자란 돈의 30%를 내야 하고요': '모자란 돈의 30%를\n내야 하고요', '들어온 돈과 나간 돈이 모두 커서': '들어온 돈과\n나간 돈이 모두 커서', '2025년 겨울에 영입한 강백호의': '2025년 겨울에\n영입한 강백호의', '샐러리캡을 넘겨야 할 수도 있어요': '샐러리캡을\n넘겨야 할 수도 있어요', '김재환의 1년 몫 11억만 빼도': '김재환의\n1년 몫 11억만 빼도', '강백호의 1년 몫 25억만 빼도': '강백호의\n1년 몫 25억만 빼도', '최형우의 1년 몫 13억만 빼도': '최형우의\n1년 몫 13억만 빼도', '2026년까지 9년 연속 가을야구를 놓친': '2026년까지\n9년 연속 가을야구를 놓친', '2026년 겨울 타선 보강이 급해요': '2026년 겨울\n타선 보강이 급해요', '2025년까지 2년 동안 FA에 228억을 투자한': '2025년까지 2년 동안\nFA에 228억을 투자한', '2026년 13홈런 68타점으로': '2026년\n13홈런 68타점으로', '2023년 114억 2천만 원에서 올라': '2023년 114억 2천만 원에서\n올라', '그런데 강백호의 4년 100억은': '그런데 강백호의\n4년 100억은'}   # 11/5 검수: 직접 정한 꺾임
def wrap2(t):
    if t in WRAP: return WRAP[t]
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
# ── 2027 FA 큰손 순위 장면 (11/5) — 기아FA 편에서 검증한 rf_* 장면만 사용 ──
# 사진: 구단 제공·워터마크 없는 사진. 같은 사진은 롱폼 전체 2묶음까지.
P.update({
    "원태인": "경기/원태인_투구_0828_삼성제공", "원태인B": "경기/원태인_역투_삼성제공",
    "구자욱": "경기/구자욱_세리머니_0827_삼성제공", "구자욱B": "경기/구자욱_홈런세리머니_삼성제공",
    "최형우삼": "경기/최형우_만루포미소_0826_삼성제공",
    "김현수KT": "경기/김현수_송구_1006_KT제공", "박해민": "경기/박해민_주먹_LG제공",
    "홍창기": "경기/홍창기_타석_LG제공", "박동원": "경기/박동원_포수_LG제공",
"김재환": "경기/김재환_결승포_1001_SSG제공", "최지훈": "경기/최지훈_타격_0920_SSG제공", "최지훈B": "경기/최지훈_주루_0920_SSG제공",
    "강백호": "경기/강백호_30호_0908_한화제공", "강백호B": "경기/강백호_헬멧인사_0915_한화제공",
    "류지현": "카드/H14_류지현_한화_A", "노시환": "카드/P29c_노시환_경기_세로",
    "박찬호두": "경기/박찬호_홈쇄도_1005_두산제공", "양현종": "경기/양현종_글러브_1012_KIA제공", "김범수": "경기/김범수_투구_0729_KIA제공",
    "김호령": "경기/김호령_만루포_0821_KIA제공", "광주": "경기/광주_관중_1017_KIA제공",
    "이동욱": "카드/H14_이동욱", "이택근": "경기/이택근_단장_1026_롯데제공", "레이예스": "경기/레이예스_타격_1012_롯데제공",
    "정수빈": "경기/정수빈_타격_1004_두산제공", "김원형": "카드/P21_김원형_박수",
    "최원준KT": "경기/최원준_204안타_1007_KT제공", "최원준KT2": "경기/최원준_미소_1005_KT제공", "KT덕아웃": "경기/최원준_더그아웃_0927_KT제공",
    "배정대": "카드/F16_배정대",
    "라일리": "경기/라일리_투구_NC제공", "알칸타라": "경기/알칸타라_주먹_키움제공", "송성문": "카드/P29c_송성문_SD",
    "삼성bg": "경기/최원태_경기_삼성제공", "최형우삼2": "경기/최형우_100타점_0918_삼성제공_중앙", "키움2": "경기/알칸타라_글러브_키움제공", "키움3": "경기/히우라_세리머니_키움제공", "키움4": "경기/데이비슨_손짓_키움제공",
    "KTbg2": "경기/이강철_덕아웃_KT제공", "KTbg3": "경기/고영표_투구_1011_KT제공", "최원준KT3": "경기/최원준_두검지_1006_KT제공",
    "LGbg2": "경기/오스틴_포효_LG제공", "LGbg3": "경기/문보경_10호_LG제공", "롯데2": "경기/레이예스_211안타_1012_롯데제공", "롯데3": "경기/한동희_타격_0918_롯데제공",
    "롯데4": "경기/전민재_세리머니_롯데제공", "롯데5": "경기/비슬리_박수_롯데제공", "롯데6": "경기/레이예스_204안타_1009_롯데제공", "두산2": "경기/정수빈_환영_0929_두산제공",
    "두산3": "경기/양의지_300호_두산제공_HQ", "NC2": "경기/라일리_포효_NC제공", "NC3": "경기/구창모_투구_1006_NC제공",
})
BG_NEU = {"css": "linear-gradient(115deg,#0E1016 0%,#1A1C24 50%,#1C2433 100%),repeating-linear-gradient(115deg,rgba(255,255,255,.035) 0 30px,rgba(0,0,0,0) 30px 90px)"}
BLUR_F = "blur(12px) brightness(.42) saturate(1.2)"
_BAND0 = BAND
def BAND(who, vals, bgk=None, team="", tag=None, **k):
    szs = [v.get("size", 128) for v in vals]
    vals = [dict(v, size=min(szs)) if len(set(szs)) > 1 else v for v in vals]
    sc = _BAND0(who, vals, bgk=bgk, team=team, tag=tag, **k)
    sc["bg"] = BGI(bgk, BLUR_F) if bgk else BG_NEU
    return sc
# 11/5 14:54 사용자 "선수마다 팀이 다른 영상들은 해당 선수의 소속 팀별로 배경 색 다르게" — 선수 카드 바탕 = 소속 팀 색(어두운 사선 무늬)
TEAMC = {"삼성": "#0A5BD1", "LG": "#C30452", "SSG": "#CE0E2D", "한화": "#FF6600", "KIA": "#EA0029", "롯데": "#123E8C", "두산": "#3B3A9A", "KT": "#EB1C24", "NC": "#2F6FB0", "키움": "#8A1530"}
def TBG(team):
    c = TEAMC.get(team)
    if not c: return BG_NEU
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    d = "#%02X%02X%02X" % (int(r * .28) + 8, int(g * .28) + 8, int(b * .28) + 10)
    return {"css": "linear-gradient(115deg,#0E1016 0%%,#1A1C24 45%%,%s 100%%),repeating-linear-gradient(115deg,rgba(%d,%d,%d,.09) 0 30px,rgba(0,0,0,0) 30px 90px)" % (d, r, g, b)}
def TC(img, name, team, kicker, big=None, minor=None, imgAt=None, nameAt=None, bgk=None, **k):
    sc = S(0, "rf_card", img=ph(img), name=name, team=team, kicker=kicker, big=big, minor=minor or [], bg=BGI(bgk, BLUR_F) if bgk else TBG(team), noCenter=True, **k)
    if imgAt is not None: sc["imgAt"] = imgAt
    if nameAt is not None: sc["nameAt"] = nameAt
    return sc
def TCc(*a, **k): return TC(*a, imgAt=-1, nameAt=-1, **k)
def DCT(img, name, team, at, stats=None): return DC(img, name, at, stats, team=team)
def DUOT(title, cards, bgk=None, **k):
    sc = DUO(title, cards, bgk=bgk, **k)
    if not bgk: _ts = {c.get("team") for c in cards}; sc["bg"] = TBG(_ts.pop()) if len(_ts) == 1 else BG_NEU   # 같은 팀 두 장이면 그 팀 색
    return sc

# ── 순위표 ── 2027 상한 151억 1709만 − 2025시즌 상위 40명 합계(데일리안·더게이트 2025-12-18), 천만 원 아래 자름
RT = [(10, "삼성", "132억", "19억 1천만", 19.1), (9, "LG", "131억 5천만", "19억 6천만", 19.6), (8, "SSG", "131억 1천만", "20억", 20.0),
      (7, "한화", "126억 5천만", "24억 6천만", 24.6), (6, "기아", "123억", "28억 1천만", 28.1), (5, "롯데", "122억 1천만", "29억", 29.0),
      (4, "두산", "105억 5천만", "45억 6천만", 45.6), (3, "KT", "105억 1천만", "46억", 46.0), (2, "NC", "89억 4천만", "61억 6천만", 61.6),
      (1, "키움", "43억 9천만", "107억 1천만", 107.1)]
ROWS = [[r[0], r[1], r[2], r[3]] for r in RT]
NAME = {r[0]: r[1] for r in RT}
def BOARD(opened, nxt=None, last=None, **k):
    return dict(type="rf_rank", head="2027 FA 큰손 순위", unit=k.pop("unit", ""), cols=["순위", "구단", "2025 합계", "남은 돈"], rows=ROWS, open=opened,
                next=nxt, last=last, valW=230, bg=BG_NEU, noCenter=True, **k)
def BOARD_R(nxt, nat=2.25):   # 'N위는 / 힌트 / 팀이에요' — 이름 순간 칸에 이름(셋째 호흡)
    return BOARD(10 - nxt, nxt, (nxt + 1 if nxt < 10 else None), nextName=NAME[nxt], nextNameAt=nat)
def TB(team, total, left, bgk, at1=1, at2=50, hi2=True):   # 팀 합계·남은 돈 띠
    return BAND(TEAMN[team], [V(total, "2025 합계", at1), V(left, "남은 돈", at2, hi=hi2)], bgk=bgk, team=team, chain="tb" + team)
TEAMN = {"삼성": "삼성 라이온즈", "LG": "LG 트윈스", "SSG": "SSG 랜더스", "한화": "한화 이글스", "KIA": "기아 타이거즈", "롯데": "롯데 자이언츠",
         "두산": "두산 베어스", "KT": "KT 위즈", "NC": "NC 다이노스", "키움": "키움 히어로즈"}
def LEFT_BARS(title, hi=(), hiAt=None, **k):   # 엔딩: 10개 구단 남은 돈 막대(남은 돈 적은 팀 → 많은 팀)
    its = [dict(label=r[1], v=r[4], txt=r[3], at=-1, hi=(r[1] in hi)) for r in RT]
    sc = RBARS(title, its, 110, bgk=None, bw=130, gap=40, valAt=-1, chain="lb", lfs=30, vfs=27, **k)
    sc["bg"] = BG_NEU
    if hiAt is not None: sc["hiAt"] = hiAt
    return sc
REVEAL = {"s0": 10, "l0": 9, "g0": 8, "h0": 7, "k0": 6, "r0": 5, "d0": 4, "t0": 3, "n0": 2, "w1": 1}

import copy as _copy
def KEEP(sc, **k):   # 11/5: 이어지는 장면 — 이미 보인 항목은 처음부터 보임(at -1). 다시 자라거나 튀어나오면 깜빡임
    sc = _copy.deepcopy(sc)
    def f(o):
        if isinstance(o, dict):
            for kk in list(o):
                if kk in ('at', 'imgAt', 'nameAt', 'valAt', 'whoAt', 'hiAt') and isinstance(o[kk], (int, float)) and o[kk] < 50: o[kk] = -1
                else: f(o[kk])
        elif isinstance(o, list):
            for v in o: f(v)
    f(sc); sc['cont'] = True; sc.update(k); return sc
# ── 오프닝 ──
SC['o1'] = dict(BOARD(0), chain="b0")
SC['o2'] = DUOT("2027 FA 최대어", [DCT("원태인", "원태인", "삼성", 1), DCT("구자욱", "구자욱", "삼성", 1)], chain="o2")
SC['o2h'] = KEEP(SC['o2'])   # 11/5 분석 채팅 종합진단 '첫 30초 공식' — 20~30초에 끝까지 볼 이유(1위는 의외의 팀)
SC['o3'] = KEEP(SC['o2'])
CAPS = [("2023년", 114.2, "114억 2천만"), ("2027년", 151.1, "151억 1천만")]   # 11/5 2라운드: 말하는 두 해만
def CAPB(hi27=False):   # 값은 말하는 2027년만
    its = [dict(label=a, v=v, txt=t, at=0, hi=(hi27 and a == "2027년"), valAt=50) for a, v, t in CAPS]
    sc = RBARS("샐러리캡 · 상위 40명 합계 상한", its, 160, bgk=None, bw=260, gap=160, chain="cap", lfs=36)
    sc["bg"] = BG_NEU
    return sc
SC['o4'] = KEEP(SC['o2'])
SC['o5'] = CAPB()
for _it in SC['o5']['items']: _it['valAt'] = 50
SC['o6'] = KEEP(SC['o5'], hiAt=1)
for _it in SC['o6']['items']:
    if _it['label'] == "2027년": _it['hi'] = True; _it['valAt'] = 2
    else: _it['valAt'] = 1
SC['o6']['hiAt'] = 2
SC['o7'] = BAND("샐러리캡 처음 넘으면", [V("30%", "넘은 돈의 제재금", 0, hi=True)], bgk="LGbg2")
SC['o8'] = RBARS("2027 상한 − 2025시즌 합계", [dict(label="구단 2025시즌 합계", v=118, txt="", at=1)], 160, bw=300, gap=120, lfs=36,
                 ref=dict(v=151.1, lab="2027 상한", at=0), brk=dict(a=0, b=0, lab="남은 돈", at=1), brkOff=80, chain="o8")
SC['o8']["bg"] = BG_NEU
SC['o9'] = KEEP(SC['o8'])
SC['o10'] = KEEP(SC['o8'])
SC['o11'] = RBARS("4년 100억 FA", [dict(label="", v=25, txt="25억", at=1, hi=True) for _ in range(4)], 40, bw=220, gap=50, lfs=36)
SC['o11']["bg"] = BG_NEU
SC['o12'] = BAND("2026시즌 합계", [V("2026년 12월", "발표 예정", 1)], bgk="광주")
SC['o13'] = dict(BOARD(0, 10, None), chain="b13")
# ── 10위 삼성 ──
SC['s1'] = BAND(TEAMN["삼성"], [V("132억", "2025 합계", 1), V("최다", "10개 구단", 2), V("19억 1천만", "남은 돈", 50, hi=True)], bgk="삼성bg", team="삼성", chain="tb삼성")
SC['s2'] = KEEP(SC['s1']); SC['s2']['vals'][2]['at'] = 1
SC['s3'] = TC("최형우삼", "최형우", "삼성", "삼성 라이온즈", big=BIGV("2년 26억", "2025년 겨울", 1, size=170), imgAt=1, nameAt=1, chain="chw")
SC['s3b'] = KEEP(SC['s3']); SC['s3b']['minor'] = [MI("목표", "삼성 우승뿐", 1)]   # 스포츠경향·일간스포츠 2025-12-03
SC['s4'] = DUOT("삼성 단장 · 다음 차례는 원·구", [DCT("원태인B", "원태인", "삼성", 1), DCT("구자욱B", "구자욱", "삼성", 1)])   # 매일신문 2025-12-29 이종열 단장
SC['s5'] = TC("원태인", "원태인", "삼성", "삼성 라이온즈", big=BIGV("10억", "2026년 연봉", 2, size=170), minor=[MI("등급", "A 유력", 1)], chain="wti")
SC['s6'] = KEEP(SC['s5']); SC['s6']['minor'].append(MI("보상금", "최소 20억", 1))
SC['s6b'] = KEEP(SC['s6']); SC['s6b']['minor'].append(MI("2025년 12월", "해외 인정 땐 도전", 1))   # OSEN 2025-12-03
SC['s7'] = TC("구자욱", "구자욱", "삼성", "삼성 라이온즈", big=BIGV("5년 120억", "", 0, size=160), minor=[MI("2026시즌", "끝", 1)], chain="gju")
SC['s8'] = KEEP(SC['s7']); SC['s8']['minor'].append(MI("타 구단 단장 전망", "100억 넘게", 2))
SC['s9'] = TC("최형우삼2", "최형우", "삼성", "삼성 라이온즈", big=BIGV("13억", "1년 몫", 0, size=170), minor=[MI("빼면 삼성 남은 돈", "6억 남짓", 1)])
SC['s10'] = BAND(TEAMN["삼성"], [V("19억 1천만", "순위표 남은 돈", -1), V("6억 남짓", "최형우 몫 빼면", -1, hi=True)], bgk="삼성bg", team="삼성")
# ── 9위 LG ──
SC['l1'] = TB("LG", "131억 5천만", "19억 6천만", "박해민", 1, 2)
SC['l2'] = BAND("LG 트윈스 · 2024년", [V("최초", "샐러리캡 초과", 1, hi=True)], bgk="LGbg2", team="LG")
SC['l3'] = BAND("샐러리캡 첫 초과 제재금", [V("50%", "2024년", 0), V("30%", "2026년부터", 1, hi=True)], bgk="LGbg3", team="LG", chain="l3")
SC['l3b'] = KEEP(SC['l3'])
SC['l4'] = TC("김현수KT", "김현수", "KT", "KT 위즈", minor=[MI("이적", "LG → KT", 1)], imgAt=1, nameAt=1, chain="khs")
SC['l4b'] = KEEP(SC['l4']); SC['l4b']['minor'].append(MI("소감", "KT에 감사", 2))   # 뉴시스·경기일보 2025-11-25
SC['l5'] = TC("박해민", "박해민", "LG", "LG 트윈스", big=BIGV("4년 65억", "", 1, size=170), chain="phm")
SC['l5b'] = KEEP(SC['l5']); SC['l5b']['minor'] = [MI("LG", "남아 줘서 고맙다", 2)]   # 스포츠조선·스포티비 2025-11-21
SC['l6'] = DUOT("FA 앞둔 LG 집토끼", [DCT("홍창기", "홍창기", "LG", 0), DCT("박동원", "박동원", "LG", 0)], chain="l6")
SC['l6b'] = KEEP(SC['l6'], title="LG 단장 · 다년계약 원했지만")   # 엑스포츠 2025-12-09·스타뉴스 12-10 차명석
SC['l8'] = KEEP(SC['l6b'])
# ── 8위 SSG ──
SC['g1'] = TB("SSG", "131억 1천만", "20억", "최지훈B", 1, 2)
SC['g3'] = TC("김재환", "김재환", "SSG", "SSG 랜더스", big=BIGV("2년 22억", "2025년 겨울", 1, size=170), imgAt=1, nameAt=1, chain="kjh")
SC['g3q'] = KEEP(SC['g3']); SC['g3q']['minor'] = [MI("각오", "마지막 도전", 1)]   # 스타뉴스·OSEN·스포츠경향 2025-12-05
SC['g3b'] = KEEP(SC['g3']); SC['g3b']['minor'] = [MI("1년 몫", "11억", 0), MI("빼면 SSG 남은 돈", "9억 남짓", 1)]
SC['g4'] = TC("최지훈", "최지훈", "SSG", "SSG 랜더스", minor=[MI("2026시즌 전 다년계약 제안", "거절", 2)], chain="cjh")
SC['g5'] = KEEP(SC['g4']); SC['g5']['minor'].append(MI("관계자", "잡아야 한다", 1))
SC['g6'] = KEEP(SC['g5'])
SC['m0'] = dict(BOARD(3), chain="m0")
# ── 7위 한화 ──
SC['h1'] = TB("한화", "126억 5천만", "24억 6천만", "강백호B", 1, 2)
SC['h2'] = TC("강백호", "강백호", "한화", "한화 이글스", big=BIGV("4년 100억", "", 0, size=170), minor=[MI("2025 합계", "빠짐", 2)], imgAt=0, nameAt=0)
SC['h2q'] = KEEP(SC['h2']); SC['h2q']['minor'] = [MI("이적 소감", "한화가 날 원했다", 1)]   # 스포츠경향·스포츠조선 2025-11-20
SC['h4'] = BAND("한화 이글스", [V("24억 6천만", "남은 돈", 0), V("25억", "강백호 1년 몫", 1), V("바닥", "빼면", 2, hi=True)], bgk="강백호B", team="한화")
SC['h5'] = TC("류지현", "류지현", "한화", "한화 이글스", minor=[MI("한화 2026년", "9위", 1)], imgAt=2, nameAt=2, chain="rjh")
SC['h6'] = KEEP(SC['h5']); SC['h6']['minor'].append(MI("약점", "중견수", 0))
SC['h7'] = TC("노시환", "노시환", "한화", "한화 이글스", big=BIGV("11년 307억", "", 50, size=150), chain="nsh")
SC['h8'] = KEEP(SC['h7']); SC['h8']['minor'] = [MI("10월 31일", "포스팅 요청", 1)]
SC['h8q'] = KEEP(SC['h8']); SC['h8q']['minor'].append(MI("2026년 2월", "세계 최고 무대가 꿈", 2))   # 스포츠조선 2026-02-24·노컷 02-23
SC['h9'] = KEEP(SC['h8']); SC['h9']['big']['at'] = 1; SC['h9']['minor'].append(MI("2027년", "시작", 2))
SC['h10'] = KEEP(SC['h8']); SC['h10']['big']['at'] = -1; SC['h10']['minor'].append(MI("메이저리그 가면", "무효", 1))
SC['h10b'] = KEEP(SC['h10'])
# ── 6위 KIA ──
SC['k1'] = TB("KIA", "123억", "28억 1천만", "광주", 1, 2)
SC['k2'] = DUOT("2025년 겨울 떠난 주전", [DCT("박찬호두", "박찬호", "두산", 1), DCT("최형우삼", "최형우", "삼성", 1)])
SC['k3'] = DUOT("2025년 겨울 계약", [DCT("양현종", "양현종", "KIA", 1), DCT("김범수", "김범수", "KIA", 2)], reserveStats=True, chain="k3")
SC['k3q'] = KEEP(SC['k3']); SC['k3q']['cards'][0]['stats'] = [dict(k="", v="도전은 계속", at=1)]; SC['k3q']['cards'][1]['stats'] = [dict(k="", v="명문 구단 영광", at=3)]   # 스타뉴스·시대 2025-12 / 엑스포츠·트윅 2026-01-21
SC['k4'] = TB("KIA", "123억", "28억 1천만", "양현종", -1, -1)
SC['k5'] = TC("김호령", "김호령", "KIA", "기아 타이거즈", minor=[MI("중견수", "생애 첫 FA", 1)], chain="khr")
SC['k5q'] = KEEP(SC['k5']); SC['k5q']['minor'].append(MI("기아 감독", "빨리 계약하라", 2))   # 스포츠경향·일간스포츠 2026-07-19
SC['k6'] = KEEP(SC['k5']); SC['k6']['big'] = BIGV("13홈런", "2026년", 1, size=170); SC['k6']['minor'] = [MI("타점", "68", 1), MI("커리어", "최다", 2)]
SC['k7'] = KEEP(SC['k6']); SC['k7']['minor'].append(MI("후반기 타율", "2할 4푼 5리", 1))
SC['k8'] = TB("KIA", "123억", "28억 1천만", "김호령", -1, -1)
# ── 5위 롯데 ──
SC['r1'] = TB("롯데", "122억 1천만", "29억", "레이예스", 1, 2)
SC['r1b'] = BAND("롯데 · 2026년", [V("64승 77패", "", 1), V("7위", "정규시즌", 2, hi=True)], bgk="롯데2", team="롯데")
SC['r2'] = BAND("롯데 · 2026년 팀 홈런", [V("113개", "", 1), V("최소", "10개 구단", 2, hi=True)], bgk="롯데3", team="롯데")
SC['r3'] = BAND("롯데 · 보강 필요", [V("수비형 외야수", "", 0, hi=True)], bgk="롯데4", team="롯데")
SC['r4'] = BAND("롯데 · 2025년 겨울", [V("0명", "외부 FA", 2, hi=True)], bgk="롯데5", team="롯데", chain="r4")
SC['r5'] = KEEP(SC['r4'])
SC['r6'] = BAND("롯데 · 2022년 겨울", [V("170억", "FA 세 명", 1, hi=True)], bgk="롯데6", team="롯데")
SC['r7'] = BAND("롯데 자이언츠 · 2026년 10월", [V("이동욱", "새 감독", 1), V("이택근", "새 단장", 1)], bgk="레이예스", team="롯데", chain="r7")
SC['r8'] = KEEP(SC['r7'])
SC['m1'] = dict(BOARD(6), chain="m1")
SC['m2'] = dict(BOARD(6, 4, None), chain="m1", cont=True)
# ── 4위 두산 ──
SC['d1'] = TB("두산", "105억 5천만", "45억 6천만", "정수빈", 1, 2)
SC['d2'] = TC("박찬호두", "박찬호", "두산", "두산 베어스", big=BIGV("4년 80억", "", 1, size=170), minor=[MI("집토끼", "셋", 2)])
SC['d2q'] = KEEP(SC['d2']); SC['d2q']['minor'] = [MI("소감", "어린 시절 꿈의 팀", 1)]   # 경향·일간스포츠 2025-11-18
SC['d3'] = TC("김재환", "김재환", "SSG", "SSG 랜더스", minor=[MI("이적", "두산 → SSG", 0)])
SC['d4'] = TB("두산", "105억 5천만", "45억 6천만", "두산3", -1, -1); SC['d4']['tag'] = "2026 합계 12월 발표"; SC['d4']['tagAt'] = 2
SC['d5'] = BAND("두산 · 2026년", [V("5위", "정규시즌", 0), V("탈락", "와일드카드", 1)], bgk="두산2", team="두산")
SC['d6'] = TC("김원형", "김원형", "두산", "두산 베어스", minor=[MI("부진 원인", "공격", 1)])
SC['d7'] = TC("구자욱B", "구자욱", "삼성", "삼성 라이온즈", big=BIGV("타자", "두산 보강 필요", 0, size=170), imgAt=2, nameAt=2, chain="d7")
SC['d8'] = KEEP(SC['d7'])
SC['d8b'] = KEEP(SC['d7']); SC['d8b']['minor'] = [MI("삼성 남은 돈", "가장 적음", 1)]
# ── 3위 KT ──
SC['t1'] = TB("KT", "105억 1천만", "46억", "KT덕아웃", 1, 2)
SC['t2'] = DUOT("KT · 2025년 겨울 외부 FA", [DCT("김현수KT", "김현수", "KT", 1), DCT("최원준KT3", "최원준", "KT", 1)], ttag="108억", ttagAt=2, reserveStats=True, chain="t2")
SC['t2q'] = KEEP(SC['t2']); SC['t2q']['cards'][1]['stats'] = [dict(k="KT 단장 평가", v="공수주 두루", at=1)]   # OSEN·일간스포츠 2025-11-26 나도현
SC['t3'] = TC("강백호", "강백호", "한화", "한화 이글스", minor=[MI("이적", "KT → 한화", 0)])
SC['t4'] = BAND("KT · 2026년", [V("108억", "2025년 겨울 투자", 0), V("90승", "", 1), V("1위", "정규시즌", 2, hi=True)], bgk="KTbg2", team="KT")
SC['t5'] = BAND("KT · 1위 멤버", [V("여럿", "FA 앞둔 선수", 2, hi=True)], bgk="KT덕아웃", team="KT")
SC['t6'] = TB("KT", "105억 1천만", "46억", "KTbg3", -1, -1)
# ── 2위 NC ──
SC['n1'] = TB("NC", "89억 4천만", "61억 6천만", "라일리", 1, 2)
SC['n1b'] = BAND("NC · 2026년", [V("64승 78패", "", 1), V("8위", "정규시즌", 2, hi=True)], bgk="NC2", team="NC")
SC['n2'] = BAND("NC · 2026년 9월", [V("2경기 차", "5위와", 1), V("탈락", "", 2, hi=True)], bgk="NC3", team="NC", chain="n2")
SC['n3'] = BAND("NC · 탈락 원인", [V("부상", "중심 타자", 0), V("교체 실패", "외국인 타자", 1, hi=True)], bgk="NC2", team="NC")
SC['n3b'] = BAND("NC · 2026년 겨울", [V("타선 보강", "급한 숙제", 1, hi=True)], bgk="NC3", team="NC")
SC['n4'] = TC("최원준KT2", "최원준", "KT", "KT 위즈", minor=[MI("이적", "NC → KT", 1)], imgAt=1, nameAt=1)
SC['n5'] = TB("NC", "89억 4천만", "61억 6천만", "라일리", -1, -1); SC['n5']['tag'] = "2024년부터 육성"; SC['n5']['tagAt'] = 0
SC['n6'] = dict(BOARD(9, None, 2), chain="n6")
# ── 1위 키움 ──
SC['w2'] = BAND(TEAMN["키움"], [V("43억 9천만", "2025 합계", 1), V("107억 1천만", "남은 돈", 3, hi=True)], bgk="알칸타라", team="키움")
SC['w2b'] = BAND(TEAMN["키움"], [V("43억 9천만", "2025 합계", -1), V("유일", "50억 미만", 1, hi=True)], bgk="키움2", team="키움")
SC['w3'] = RBARS("2027 상한까지 남은 돈", [dict(label="NC", v=61.6, txt="61억 6천만", at=0), dict(label="키움", v=107.1, txt="107억 1천만", at=0, hi=True)], 120, bw=260, gap=120, lfs=36,
                 brk=dict(a=0, b=1, lab="45억 넘게 차이", at=1))
SC['w3']["bg"] = BG_NEU
_W3 = lambda a, b, c: [V("60억 6천만", "최소 금액", a), V("16억 6천만", "키움 부족", b, hi=True), V("30%", "부족분 납부", c)]   # 11/5 2라운드: 세 칸 자리를 처음부터(칸이 늘며 옆으로 밀리던 것)
SC['w4'] = BAND("2027년 샐러리캡 하한", _W3(50, 50, 50), bgk="키움3", team="키움", chain="w4")
SC['w5'] = BAND("2027년 샐러리캡 하한", _W3(0, 1, 50), bgk="키움3", team="키움", chain="w4", cont=True)
SC['w6'] = BAND("2027년 샐러리캡 하한", _W3(-1, -1, 1), bgk="키움3", team="키움", chain="w4", cont=True)
SC['w7'] = KEEP(SC['w6'])
SC['w8a'] = TC("송성문", "송성문", "키움", "키움 → 샌디에이고", big=BIGV("44억 이상", "포스팅 금액", 50, size=150), minor=[MI("소감", "나 같은 선수가 이런 대우", 2)], chain="ssm")   # 헤럴드경제 2025-12-22·노컷 12-23
SC['w8'] = KEEP(SC['w8a']); SC['w8']['big']['at'] = 1
SC['w9'] = TB("키움", "43억 9천만", "107억 1천만", "키움4", -1, -1)
# ── 정리·엔딩 ──
SC['e1'] = LEFT_BARS("2027 상한까지 남은 돈", hi=("키움", "NC", "KT"), hiAt=2)
SC['e2'] = dict(LEFT_BARS("2027 상한까지 남은 돈", hi=("삼성", "LG", "SSG"), hiAt=1), cont=True)
SC['e3'] = dict(LEFT_BARS("2027 상한까지 남은 돈", hi=("삼성", "LG", "SSG", "키움")), cont=True, brk=dict(a=0, b=2, lab="세 팀 합 58억 7천만", at=0))
for _it in SC['e3']['items']: _it['hiAt'] = 1 if _it['label'] == "키움" else -1
SC['e3b'] = dict(BOARD(10), chain="e3b")
SC['e3c'] = dict(KEEP(SC['e3b']), hiRows=[9], hiAt=0)
SC['e4'] = LEFT_BARS("2027 상한까지 남은 돈")
SC['e5'] = dict(BOARD(10), chain="e5")
SC['e6'] = RBARS("2027 FA 진짜 큰손은?", [dict(label="삼성", v=19.1, txt="19억 1천만", at=1, hi=True), dict(label="키움", v=107.1, txt="107억 1천만", at=3, hi=True)], 120, bw=260, gap=120, lfs=36)
SC['e6']["bg"] = BG_NEU
for _k, _n in REVEAL.items():
    SC[_k] = dict(BOARD_R(_n), chain="rv" + _k)
HOLD = {"o13": 0.6, "s10": 0.6, "l8": 0.6, "m0": 0.6, "h10b": 0.6, "k8": 0.6, "m2": 0.6, "d8b": 0.6, "t6": 0.6, "n6": 0.6, "w9": 0.6}   # 기준표 §7 순위표 쉼 0.6   # 순위 공개 직전·챕터 끝 쉼
RV_KEYS = list(REVEAL)
NOW, NOW_KEYS = {}, []
SC['s0']['chain'] = "b13"; SC['s0']['cont'] = True   # 오프닝 끝 순위표(10위 칸 깜빡)에서 그대로 이름만
SC['h0']['chain'] = "m0"; SC['h0']['cont'] = True   # m0 순위표에서 그대로
SC['d0']['chain'] = "m1"; SC['d0']['cont'] = True   # '이제 네 팀은' 순위표에서 그대로
SC['w1']['chain'] = "n6"; SC['w1']['cont'] = True   # n6 순위표에서 그대로

# ── 11/5 15:11 사용자 "선수 사진은 이런 템플릿(금테 카드 rf_gold) 사용해줘 · 선수 사진 가운데로 잘 맞춰라" ──
# 선수 카드(rf_card)를 전부 금테 카드로 바꾼다. 바탕은 소속 팀 색(14:54 지시), 사진은 몸 가운데(CX: 사진 폭 대비 몸 중심)를 카드 가운데로.
EN = {"원태인": "WON TAE-IN", "구자욱": "KOO JA-WOOK", "최형우": "CHOI HYOUNG-WOO", "김현수": "KIM HYUN-SOO", "박해민": "PARK HAE-MIN",
      "김재환": "KIM JAE-HWAN", "최지훈": "CHOI JI-HOON", "강백호": "KANG BAEK-HO", "류지현": "RYU JI-HYUN", "노시환": "NOH SI-HWAN",
      "김호령": "KIM HO-RYUNG", "박찬호": "PARK CHAN-HO", "김원형": "KIM WON-HYUNG", "최원준": "CHOI WON-JUN", "송성문": "SONG SUNG-MUN"}
CX = {"최형우삼": .42, "원태인": .45, "구자욱": .5, "최형우삼2": .35, "김현수KT": .52, "박해민": .53, "김재환": .62, "최지훈": .45, "강백호": .64,
      "류지현": .5, "노시환": .45, "김호령": .36, "박찬호두": .3, "김원형": .6, "구자욱B": .36, "최원준KT2": .3, "송성문": .55}
import os as _os
from PIL import Image as _Im
_PB = '/mnt/user-data/uploads/야구자판기/선수이미지/'
def _focus(key):
    p = P.get(key, key)
    for e in ('.jpg', '.png', '.webp', '.jpeg'):
        if _os.path.exists(_PB + p + e):
            w, h = _Im.open(_PB + p + e).size; v = (h * 474 / 674) / w
            c = CX.get(key, .5)
            x = 50 if v >= 1 else max(0, min(100, (c - v / 2) / (1 - v) * 100))
            return "%d%% 18%%" % round(x)
    return None
_IMGKEY = {}
for _k, _v in P.items(): _IMGKEY.setdefault(_v, _k)
def TO_GOLD(sc):
    st = []
    b = sc.get('big')
    if b: st.append(dict(k=b.get('k', ''), v=b['v'], at=b['at'], hi=True, size=min(b.get('size', 110), 110)))
    for m in sc.get('minor') or []: st.append(dict(k=m['k'], v=m['v'], at=m['at'], size=64))
    g = {kk: vv for kk, vv in sc.items() if kk not in ('type', 'big', 'minor', 'kicker', 'imgAt', 'nameAt', 'focus')}
    g.update(type="rf_gold", season=sc.get('kicker', ''), en=EN.get(sc.get('name', ''), ''), stats=st)
    key = _IMGKEY.get(sc['img'], sc['img']); f = _focus(key)
    if f: g['focus'] = f
    if sc.get('imgAt') is not None: g['cardAt'] = sc['imgAt']
    return g
for _k in list(SC):
    if SC[_k].get('type') == 'rf_card': SC[_k] = TO_GOLD(SC[_k])

for _k in [k for k in SC if k not in KEYS]: SC.pop(_k)
missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing and not extra, (missing, extra)
lines, scenes = [], []
for j, (k, narr, sub) in enumerate(_t.LINES):
    sc = dict(SC[k]); sc['startLine'] = j
    lines.append(L(narr, sub)); scenes.append(sc)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})
scenes.append(dict(END_SC, startLine=len(lines) - 1, bg=BG_NEU))   # 11/4 사용자 "배경 템플릿도 다른 장면이랑 어울리게" — 엔딩도 빨간 줄무늬 어두운 바탕

def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
CH = [ch("FA 큰손 10위~8위", "s0", "m0"), ch("FA 큰손 7위~5위", "h0", "m1"), ch("FA 큰손 4위~2위", "m2", "n6"), ch("FA 큰손 1위", "w1", "w9"), ch("FA 큰손 정리", "e1", "e6")]
DESC = ("2027 FA 큰손 순위 — 10개 구단의 2027년 샐러리캡 여유(상한 151억 1709만 원)를 비교했어요.\n"
        "원태인·구자욱 같은 2027 FA 최대어를 데려갈 큰손은 어느 구단일까요?\n\n"
        "구단별 2025시즌 상위 40명 연봉 합계를 2027년 상한에서 빼서, 남은 돈이 적은 팀부터 순위를 매겼어요(KBO 2025년 12월 발표, 천만 원 아래는 자름). 2026시즌 합계는 2026년 12월 발표 예정이라, 2025년 겨울 FA 이동은 영상에서 팀마다 따로 짚었어요.\n\n"
        "등장 구단: 기아 타이거즈, 두산 베어스, 롯데 자이언츠, 삼성 라이온즈, 키움 히어로즈, 한화 이글스, KT 위즈, LG 트윈스, NC 다이노스, SSG 랜더스.\n"
        "등장 인물: 원태인, 구자욱, 최형우, 김현수, 박해민, 홍창기, 박동원, 김재환, 최지훈, 강백호, 노시환, 류지현, 양현종, 김범수, 김호령, 박찬호, 김원형, 최원준, 송성문, 이동욱, 이택근.\n\n"
        "야구자판기는 매일 야구 이슈를 정리해요. 2027 FA 시장의 진짜 큰손은 집토끼를 지키려는 팀일까요? 아니면 지갑이 두꺼운 팀일까요? 댓글로 남겨 주세요.\n\n▶ 지난 영상: 기아 역대 FA 돈값 순위\n\n"
        "#FA큰손 #샐러리캡 #2027FA #원태인 #구자욱 #프로야구 #KBO #야구자판기\n")
TAGS = ["FA 큰손", "2027 FA", "샐러리캡", "경쟁균형세", "KBO 샐러리캡", "FA 시장", "10개 구단", "원태인", "구자욱", "최지훈", "홍창기", "박동원", "프로야구", "KBO"]
SOURCE = "사실 출처 = 샐러리캡·구단별 합계: 데일리안·더게이트 2025-12-18, 상한 인상: 시사저널 2026-08-15·OSEN 2026-01-05 (fabig/research_cap.md · research_teams.md · review1/fact_round1.md)"
EP = {"theme": "m3", "introChapter": "FA 큰손 기준 · 샐러리캡", "date": "2026-11-07", "gameDate": "2026-11-07", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1107-fabig-v1", "topic": "FA큰손순위", "endcardSec": 10, "gapScale": 1.3, "pauseMax": 0.5, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "2027 FA 큰손 순위 | 원태인·구자욱 데려갈 팀은? 10개 구단 샐러리캡 여유", "description": DESC, "tags": TAGS, "hashtags": ["#FA큰손", "#샐러리캡", "#2027FA", "#원태인", "#구자욱", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'o2h', 'm0', 'm1', 'm2', 'w3', 'e3', 'e4', 'e6') + tuple(RV_KEYS)}   # 11/5 종합진단: 질문·반전·결론·순위 공개 줄은 느리게(완급)
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    for _k, _h in HOLD.items(): EP['lines'][KEYS.index(_k)]['holdAfter'] = _h
    for _k in NOW_KEYS: EP['lines'][KEYS.index(_k)]['holdAfter'] = 0.7   # 11/5 10:28 근황 줄 뒤 순위표 머묾 → 카드
    for _k in RV_KEYS: EP['lines'][KEYS.index(_k)]['pauseMax'] = 0.8   # 11/5 15:23 사용자 "자문자답(1위는 누구일까요? 바로 OO)은 텀이 살짝 길게" — 힌트 뒤 '..' 쉼을 0.5초로 줄이지 않게
    for _k in RV_KEYS:
        if _k in NOW: EP['lines'][KEYS.index(_k)]['noMerge'] = True; continue   # 11/5 11:22 사용자 "김범수예요 / 현재 기아 불펜에서 — 텀이 너무 길어" → 근황 줄이 이어지면 0.7초 머묾 없이 보통 줄 사이 텀만
        EP['lines'][KEYS.index(_k)]['holdAfter'] = 0.7; EP['lines'][KEYS.index(_k)]['noMerge'] = True   # 11/5 검수: '8위는'처럼 짧은 첫 조각도 자막 따로   # 11/5 01:20 사용자 "순위표에서 몇 위는 누구예요 할 때 특히 빨라서 휙휙" — 이름 공개 뒤 순위표에 0.7초 머묾   # 순위표 보여 줄 쉼
    # 11/4 16시 검수본(132줄)과 대사가 같은 줄은 그 음성을 새 번호로 옮긴다(voiceRemap, 재합성 0) — 바뀐 15줄만 새로 합성
    _vo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voice_old_1107.json')
    if os.path.exists(_vo):
        _old = json.load(open(_vo, encoding='utf-8'))
        EP['voiceRemap'] = [(_old.index(l['narr']) if l['narr'] in _old else None) for l in EP['lines']]
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-07_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
