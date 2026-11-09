# -*- coding: utf-8 -*-
"""11/8 롱폼 「APBC 대표팀 10개 구단 총정리」 콘티.
대사 = tools/text_1108_apbc.py. 근거 = /home/claude/apbc/research.md
실행: python -X utf8 tools/gen_1108_apbc.py → episodes/2026-11-08_롱폼.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t36', os.path.join(HERE, 'text_1108_apbc.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
KEYS = [x[0] for x in _t.LINES]

BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억|(?:^| )다|(?:^| )못|(?:^| )안|(?:^| )만|(?:^| )(?:이번|지난|다음|올|그)|(?:^| )(?:네|다섯|여섯|일곱|여덟|아홉|열|열일곱)|중심|KBO|기아|WAR|\d+할|남는|좋은|\d+푼|\d+천만|역대|(?:^| )수|(?:^| )할|상위|넘은|(?:^| )더|\d+ FA)$'); BAD_B = re.compile(r'^(건|타선|겨울|코치|차|\d+차전|첫 |것 |수 |때 |중 |구단|달러|일|명|개|경기|원|타수|안타|\d+(?:푼|리)(?![가-힣]*할))')
WRAP = {'한일전에 약 3천 석이 마련됐고': '한일전에 약 3천 석이\n마련됐고', '감각이 떨어져 있을 것으로 생각했는데': '감각이 떨어져 있을 것으로\n생각했는데'}   # 11/8 검수: 단위·의존명사 앞 꺾임
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
# ── APBC 대표팀 10개 구단 총정리 장면 (11/8) ──
# 사진: 구단·KBO 제공 사진을 사람 중심 4:5 로 자른 카드(경기/APBC_<이름>_카드, 워터마크 잘라 냄) — /home/claude/apbc/mkcards.py
import copy as _copy
BG_NEU = {"css": "linear-gradient(115deg,#0E1016 0%,#1A1C24 50%,#1C2433 100%),repeating-linear-gradient(115deg,rgba(255,255,255,.035) 0 30px,rgba(0,0,0,0) 30px 90px)"}
BG_KOR_OLD = {"css": "linear-gradient(115deg,#0E1016 0%,#141B2E 45%,#0B2A6B 100%),repeating-linear-gradient(115deg,rgba(255,255,255,.04) 0 30px,rgba(0,0,0,0) 30px 90px)"}
BG_KOR = {"css": "repeating-linear-gradient(45deg,rgba(255,255,255,.035) 0 2px,rgba(0,0,0,0) 2px 64px),repeating-linear-gradient(-45deg,rgba(255,255,255,.035) 0 2px,rgba(0,0,0,0) 2px 64px),radial-gradient(70% 80% at 30% 40%,#16295C 0%,#0B1634 60%,#070D20 100%)"}   # 11/7 23:30 새 스타일 — 대표팀 남색 마름모 무늬
TEAMC = {"삼성": "#0A5BD1", "LG": "#C30452", "SSG": "#CE0E2D", "한화": "#FF6600", "KIA": "#EA0029", "롯데": "#123E8C", "두산": "#3B3A9A", "KT": "#EB1C24", "NC": "#2F6FB0", "키움": "#8A1530"}
def TBG(team):
    c = TEAMC.get(team)
    if not c: return BG_NEU
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    d = "#%02X%02X%02X" % (int(r * .28) + 8, int(g * .28) + 8, int(b * .28) + 10)
    return {"css": "linear-gradient(115deg,#0E1016 0%%,#1A1C24 45%%,%s 100%%),repeating-linear-gradient(115deg,rgba(%d,%d,%d,.09) 0 30px,rgba(0,0,0,0) 30px 90px)" % (d, r, g, b)}
TEAMN = {"삼성": "삼성 라이온즈", "LG": "LG 트윈스", "SSG": "SSG 랜더스", "한화": "한화 이글스", "KIA": "기아 타이거즈", "롯데": "롯데 자이언츠",
         "두산": "두산 베어스", "KT": "KT 위즈", "NC": "NC 다이노스", "키움": "키움 히어로즈"}
TEAMOF = {}
M = {'키움': ['전준표'], 'KT': ['안현민'], '삼성': ['이재현', '김지찬'], '두산': ['안재석', '김민석'], '한화': ['조동욱', '허인서', '문현빈'],
     'NC': ['이준혁', '김휘집', '김주원'], 'LG': ['김영우', '박시원', '우강훈', '문정빈'], 'SSG': ['김민준', '이로운', '김건우', '조형우'],
     '롯데': ['최준용', '박정민', '김진욱', '한동희'], 'KIA': ['성영탁', '김태형', '김도영', '박재현']}
for _tm, _ns in M.items():
    for _n in _ns: TEAMOF[_n] = _tm
TEAMOF.update({'최원호': '', '노시환': '한화'})
def CI(n): return "경기/APBC_%s_카드" % n
def IT(n, at=-1, **k): return dict(dict(img=CI(n), name=n, team=TEAMOF.get(n, ''), at=at), **k)
def SAY(sc, d):   # 11/8 카드마다 말풍선(기록·역할) — 그 호흡에
    for it in sc.get('items', []):
        if it.get('name') in d: it['say'], it['sayAt'] = d[it['name']]
    return sc
def GRID(title, names, at=None, chain=None, cols=None, **k):
    its = [IT(n, (at.get(n, 0) if isinstance(at, dict) else (0 if at is None else at))) for n in names]
    sc = S(0, "facegrid", title=title, items=its, noCenter=True, card=True, **k)
    if cols: sc['cols'] = cols
    if chain: sc['chain'] = chain
    return sc
SEEN = {}; STARTED = set()
def TG(team, hi=(), new=None, text=None, textAt=1, size=54, **k):   # 구단 카드판 — 이름을 말한 선수만 카드(이름 부르는 호흡에 등장), 아직 안 부른 선수는 '?' 칸, 말하는 선수 강조·나머지 흐리게
    hi = [hi] if isinstance(hi, str) else list(hi); new = new or {}
    seen = SEEN.setdefault(team, [])
    its = [IT(n, -1) for n in seen] + [IT(n, a) for n, a in new.items() if n not in seen]
    for n in new:
        if n not in seen: seen.append(n)
    its += [dict(name=n, ph=True, team=team) for n in M[team] if n not in seen]   # 11/8 검수: ph 칸에도 팀(이름 줄 높이 같게 → 새로 뜨는 카드만 위로 뜨던 것)   # 아직 이름을 안 부른 선수 = '?' 칸(앞뒤 장면이 다른 종류여도 칸 수 그대로)
    its.sort(key=lambda it: M[team].index(it['name']))
    for it in its:
        if hi: it.update({'hi': True} if it['name'] in hi else {'dim': True})
    first = team not in STARTED; STARTED.add(team)
    sc = S(0, "facegrid", title=TEAMN[team], items=its, noCenter=True, card=True, chain="tg" + team, bg=TBG(team), size=size)
    sc['cols'] = len(M[team])
    if text: sc['text'] = text; sc['textAt'] = textAt
    if not first: sc['cont'] = True
    sc.update(k); return sc
def BAR(label, v, at, txt=None, hi=False, unit="명"): return dict(dict(label=label, v=v, at=at, hi=hi, unit=unit), **({"txt": txt} if txt else {}))
def RB(title, items, mx, **k):
    sc = RBARS(title, items, mx, **k); sc['bg'] = k.pop('bg', BG_KOR) if 'bg' in k else BG_KOR
    return sc
def TLK(title, items, **k): sc = TL(title, items, **k); sc['bg'] = BG_KOR; return sc
def MUK(l, r, score, text, tag, **k): sc = MU(l, r, score, text, tag, **k); sc['bg'] = BG_KOR; return sc
def QK(text, logos, **k): sc = Q(text, logos, **k); sc.setdefault('bg', BG_KOR); return sc
def KEEP(sc, **k):   # 이어지는 장면 — 이미 보인 항목은 처음부터(at -1)
    sc = _copy.deepcopy(sc)
    def f(o):
        if isinstance(o, dict):
            for kk in list(o):
                if kk in ('at', 'textAt', 'valAt', 'hiAt', 'sayAt') and isinstance(o[kk], (int, float)) and o[kk] < 50: o[kk] = -1
                else: f(o[kk])
        elif isinstance(o, list):
            for v in o: f(v)
    f(sc); sc['cont'] = True; sc.update(k); return sc
ALL10 = ["KIA", "KT", "LG", "NC", "SSG", "두산", "롯데", "삼성", "키움", "한화"]

# ── 오프닝 ──
SC['o1'] = RB("28명 중 가장 많은 팀 · 적은 팀", [dict(BAR("LG", 4, 0), valAt=3), dict(BAR("SSG", 4, 0), valAt=3), dict(BAR("롯데", 4, 0), valAt=3), dict(BAR("기아", 4, 0), valAt=3), dict(BAR("키움", 1, 0, hi=True), valAt=4), dict(BAR("KT", 1, 0, hi=True), valAt=4)], 5, bw=170, gap=48, chain="o1")
SC['o2'] = QK("누가 도쿄돔에 갈까요?", ALL10, logoSize=150, size=96, chain="o2")
SC['o2b'] = QK("구단별 명단 · 한일전 관전 포인트", ALL10, logoSize=150, size=80, chain="o2", cont=True)   # 11/7 23:19 사용자 "같은 로고가 나오는 장면인데 또 깜빡인다" — 같은 로고 줄은 이어받기(글만 바뀜)
AG11 = ['김도영', '박재현', '성영탁', '최준용', '김진욱', '김영우', '조형우', '이재현', '김지찬', '김주원', '문현빈']
SC['o3'] = RB("9월 아시안게임 금메달", [dict(BAR("대표팀", 28, 0), valAt=0), dict(BAR("금메달 멤버", 11, 0, hi=True), valAt=0)], 30, bw=260, gap=160)
SC['o4'] = TLK("APBC 출전 자격", [dict(d="나이", t="24세 이하", at=1), dict(d="또는", t="입단 3년 차 이내", at=1), dict(d="더해서", t="와일드카드 세 명", c="gold", at=2)])
SC['o4b'] = QK("와일드카드 세 명", ["롯데", "삼성"], logoSize=220, size=96, note="모두 2002년 이전 출생")
SC['o5'] = TLK("2026 APBC · 도쿄돔", [dict(d="11월 12일부터", t="한국 · 일본 · 대만 · 호주", at=0), dict(d="예선", t="한 번씩 맞붙기", at=2)], chain="o5")
SC['o6'] = KEEP(SC['o5'], items=[dict(d="11월 12일부터", t="한국 · 일본 · 대만 · 호주", at=-1), dict(d="예선", t="세 경기 성적", at=0), dict(d="15일", t="상위 두 팀 결승", c="gold", at=1)])
SC['o7'] = TLK("한국 일정", [dict(d="12일 정오", t="호주", at=0), dict(d="13일 금요일 저녁 7시", t="일본", c="gold", at=1), dict(d="14일 저녁 7시", t="대만", at=2)])
SC['o7b'] = dict(GRID("APBC 대표팀 감독", ['최원호'], at=1, cols=1), bg=BG_KOR)
# ── 지난 두 대회 ──
P1 = [dict(d="2017년", t="첫 대회", at=0), dict(d="2023년", t="두 번째 대회", at=0), dict(d="2026년", t="세 번째 대회", c="gold", at=1)]
SC['p1'] = TLK("APBC", P1, chain="p")
SC['p2'] = KEEP(SC['p1'], items=[dict(d="2017년", t="일본에 져 준우승", c="bad", at=1), dict(d="2023년", t="일본에 져 준우승", c="bad", at=1), dict(d="2026년", t="세 번째 대회", c="gold", at=-1)])
SC['p3'] = KEEP(SC['p2'], items=[dict(d="2017년", t="결승 0대 7 패", c="bad", at=0.3), dict(d="2023년", t="일본에 져 준우승", c="bad", at=-1), dict(d="2026년", t="세 번째 대회", c="gold", at=-1)])
SC['p4'] = TLK("2023 APBC 결승 한일전", [dict(d="2023년 결승", t="연장 승부치기", at=0), dict(d="10회 초", t="3대 2 리드", at=2), dict(d="10회 말", t="2실점 · 3대 4 패", c="bad", at=3)])
SC['p5'] = dict(GRID("2023년에 이어 다시", ['김도영', '김주원', '김휘집', '문현빈', '최준용'], at={'김도영': 1, '김주원': 1, '김휘집': 1, '문현빈': 2, '최준용': 2}, cols=5), bg=BG_KOR)
# ── 명단 변화 ──
SC['o8'] = RB("대표팀 명단", [BAR("처음 발표", 33, 0), BAR("부상", 3, 1, hi=True), BAR("한국시리즈", 2, 2, hi=True)], 36, bw=230, gap=90)
SC['o9'] = RB("최종 28명", [dict(BAR("투수", 14, 0), valAt=1), dict(BAR("포수", 2, 0), valAt=1), dict(BAR("내야수", 7, 0), valAt=2), dict(BAR("외야수", 5, 0), valAt=2)], 16, bw=200, gap=70)
SC['o9b'] = RB("투수가 가장 많은 팀", [dict(BAR("LG", 3, 0, hi=True), valAt=2), dict(BAR("SSG", 3, 0, hi=True), valAt=2), dict(BAR("롯데", 3, 0, hi=True), valAt=2)], 4, bw=220, gap=80)
SC['o9c'] = RB("야수가 가장 많은 팀", [dict(BAR("기아", 2, 0, hi=True), valAt=2), dict(BAR("한화", 2, 0, hi=True), valAt=2), dict(BAR("NC", 2, 0, hi=True), valAt=2), dict(BAR("삼성", 2, 0, hi=True), valAt=2), dict(BAR("두산", 2, 0, hi=True), valAt=2)], 3, bw=180, gap=60)
SC['o10'] = QK("한 명뿐인 팀부터", ["키움", "KT"], logoSize=220, size=96)
# ── 키움·KT ──
SC['w1'] = TG('키움', new={'전준표': 1}, text="투수 한 명", textAt=1)
SC['w2'] = TG('키움', hi='전준표', text="2005년생 · 2026년 21경기\n평균자책점 4.29", textAt=0.5, size=52)
SC['t1'] = TG('KT', new={'안현민': 1}, text="외야수 한 명", textAt=1)
SC['t1b'] = TG('KT', text="정규시즌 1위 · 한국시리즈 직행", textAt=1)
SC['t2'] = TG('KT', hi='안현민', text="부상 두 달 · 94경기 14홈런\n2026년 타율 2할 9푼 8리", textAt=1, size=50)
SC['t2b'] = TG('KT', hi='안현민', text="2025년 신인왕\n그해 11월 일본 평가전 홈런", textAt=0.5, size=52)
SC['t4'] = TG('KT', hi='안현민', text="7차전까지 가면\n12일 호주전 못 나올 수도", textAt=2, size=52)
# ── 삼성·두산 ──
SC['s0'] = QK("두 명씩 뽑힌 팀", ["삼성", "두산"], logoSize=220, size=96)
SC['s1'] = TG('삼성', text="투수 둘 빠짐 · 야수만", textAt=2)
SC['s2'] = TG('삼성', hi='이재현', new={'이재현': 0}, text="2026년 타율 2할 2푼 2리\n17홈런", textAt=1, size=52)
SC['s4'] = TG('삼성', hi='김지찬', new={'김지찬': 0}, text="타율 3할 1푼 5리 · 도루 22개", textAt=1, size=50)
SC['s4b'] = TG('삼성', hi='김지찬', text="대표팀 타자 타율 1위", textAt=0.5)
SC['s4c'] = TG('삼성', hi='김지찬', text="2023년 항저우 · 이번에도 금메달", textAt=0, size=50)
SC['s5'] = TG('삼성', hi='김지찬', text="중견수 자리 따로 준비", textAt=1)
SC['d1'] = TG('두산', text="투수 이탈 · 야수 두 명만", textAt=1)
SC['d2'] = TG('두산', hi='안재석', new={'안재석': 0}, text="2026년 타율 2할 7푼 8리\n11홈런 · 67타점", textAt=1, size=52)
SC['d3'] = TG('두산', hi='안재석', text="소속팀 3루 → 대표팀 2루", textAt=1)
SC['d4'] = TG('두산', hi='안재석', text="2루수 후보 부상", textAt=0)
SC['d5'] = TG('두산', hi='안재석', text="3루수 두 명이 2루 번갈아", textAt=1)
SC['d6'] = TG('두산', hi='김민석', new={'김민석': 0}, text="2026년 135경기\n타율 3할 1푼 · 57타점", textAt=1, size=52)
SC['d7'] = TG('두산', hi='김민석', text="연습경기 1번 타자 중견수", textAt=1)
SC['d8'] = TG('두산', hi=('안재석', '김민석'), text="2루 · 중견수 후보 두 명", textAt=1)
# ── 한화·NC ──
SC['h0'] = QK("세 명씩 뽑힌 팀", ["한화", "NC"], logoSize=220, size=96)
SC['h1'] = TG('한화', new={'조동욱': 1, '허인서': 1, '문현빈': 1}, text="세 명", textAt=1)
SC['h2'] = TG('한화', hi='허인서', text="2026년 타율 2할 8푼 3리\n20홈런 · 79타점", textAt=1, size=52)
SC['h3'] = TG('한화', hi='문현빈', text="타율 2할 9푼 7리\n15홈런 · 76타점", textAt=1, size=52)
SC['h5'] = TG('한화', hi='문현빈', text="연습경기 우익수\nKT 외야수 합류 늦어질 수도", textAt=1, size=52)
SC['h6'] = TG('한화', hi='조동욱', text="75경기 · 10홀드\n대표팀 투수 최다 경기", textAt=1, size=52)
SC['n1'] = TG('NC', new={'이준혁': 2, '김휘집': 2, '김주원': 2}, text="투수 한 명 부상 이탈", textAt=1)
SC['n2'] = TG('NC', hi='김주원', text="18홈런 · 도루 30개\n연습경기 유격수", textAt=1, size=52)
SC['n3'] = TG('NC', hi='김주원', text="2023 APBC 베스트나인 유격수", textAt=1, size=50)
SC['n4'] = TG('NC', hi='김휘집', text="90경기 · 14홈런 · 64타점", textAt=1)
SC['n6'] = TG('NC', hi='이준혁', text="34경기 · 평균자책점 2.78\n대표팀 투수 가장 낮음", textAt=1, size=52)
SC['n7'] = TG('NC', hi=('김주원', '김휘집'), text="유격수 김주원 · 2루 후보 김휘집", textAt=2, size=48)
# ── LG·SSG·롯데·기아 ──
SC['l0'] = QK("네 명씩 뽑힌 팀", ["LG", "SSG", "롯데", "KIA"], logoSize=190, size=96)
SC['l1'] = TG('LG', new={'문정빈': 2}, text="투수 세 명 · 내야수 문정빈", textAt=2)
SC['l2'] = TG('LG', hi='문정빈', text="2026년 91경기 19홈런 66타점\n연습경기 1루수", textAt=1, size=50)
SC['l3'] = SAY(TG('LG', hi=('우강훈', '김영우', '박시원'), new={'우강훈': 1, '김영우': 2, '박시원': 3}, text="박시원 · 김영우 상무전 7·8회 무실점", textAt=5, size=46), {'우강훈': ('20홀드', 1), '김영우': ('금메달', 2), '박시원': ('2006년생', 3)})
SC['l4'] = TG('LG', hi='김영우', new={'김영우': 0}, text="51경기 · 3승 5홀드", textAt=1)
SC['l5'] = TG('LG', hi='박시원', new={'박시원': 0}, text="2006년생 · 29경기 2승", textAt=1)
SC['l6'] = TG('LG', text="2023년 한국시리즈로 0명\n이번엔 네 명", textAt=1, size=52)
SC['g1'] = TG('SSG', new={'조형우': 2}, text="투수 세 명 · 포수 조형우 · 네 명", textAt=2, size=50)
SC['g2'] = TG('SSG', hi='김민준', new={'김민준': 0}, text="2006년생 · 9승 3패\n평균자책점 3.56 · 상무전 선발", textAt=1, size=50)
SC['g3'] = TG('SSG', hi=('김건우', '이로운'), new={'김건우': 0, '이로운': 2}, text="김건우 132이닝 9승 · 이로운 8승", textAt=2, size=50)
SC['g4'] = TG('SSG', hi='조형우', text="타율 2할 6푼 8리 · 8홈런", textAt=1)
SC['r1'] = TG('롯데', text="와일드카드 두 명 포함 · 네 명", textAt=1)
SC['r2'] = TG('롯데', hi='한동희', new={'한동희': 0}, text="2026년 타율 3할 6리\n25홈런 · 81타점", textAt=1, size=52)
SC['r2b'] = TG('롯데', hi='한동희', text="대표팀 타자 홈런 2위", textAt=0.5)
SC['r3'] = TG('롯데', hi='한동희', text="1999년생 · 최고령\n연습경기 4번 타자 3루수", textAt=0.5, size=52)
SC['r4'] = SAY(TG('롯데', hi=('김진욱', '최준용', '박정민'), new={'김진욱': 1, '최준용': 3, '박정민': 3}, text="최준용 · 박정민 마무리 경쟁", textAt=3, size=48), {'김진욱': ('144이닝 · 선발 후보', 1)})
SC['r6'] = TG('롯데', hi='김진욱', new={'김진욱': 0}, text="144이닝 · 7승", textAt=1)
SC['r7'] = TG('롯데', hi='박정민', new={'박정민': 0}, text="63경기 · 9승 14홀드", textAt=1)
SC['k1'] = TG('KIA', text="투수 한 명 부상 · 그래도 네 명", textAt=2)
SC['k2'] = TG('KIA', hi='김도영', new={'김도영': 1}, text="2024년 MVP", textAt=1)
SC['k2b'] = TG('KIA', hi='김도영', text="3월 WBC · 9월 아시안게임\n2026년 세 번째 태극마크", textAt=1, size=52)
SC['k3'] = TG('KIA', hi='김도영', text="2026년 타율 3할 8리\n45홈런 · 118타점", textAt=0.5, size=52)
SC['k3b'] = TG('KIA', hi='김도영', text="홈런 · 타점 대표팀 1위", textAt=0)
SC['k5'] = TG('KIA', hi='박재현', new={'박재현': 0}, text="2006년생 · 19홈런 21도루\n대표팀 중견수 후보", textAt=0.5, size=52)
SC['k5b'] = TG('KIA', hi='박재현', text="대표팀 야수 최연소", textAt=1)
SC['k6'] = SAY(TG('KIA', hi=('성영탁', '김태형'), new={'성영탁': 1, '김태형': 2}, text="김태형 = 스윙맨", textAt=4, size=48), {'성영탁': ('13세이브', 1), '김태형': ('2006년생', 2)})
SC['k7'] = TG('KIA', hi='김태형', new={'김태형': 0}, text="2006년생 · 24경기 3승", textAt=1)
SC['q0'] = dict(MUK("한국", "호주", "vs", "도쿄돔 상대 팀", "2026 APBC"), chain='qa')
# ── 상대 팀 ──
SC['q1'] = dict(MUK("한국", "호주", "vs", "2023년에도 첫 경기", "첫 상대"), chain='qa', cont=True)
SC['q2'] = dict(MUK("한국", "호주", "3 : 2", "연장 10회 말 끝내기", "2023 APBC"), chain='qb')
SC['q2b'] = dict(MUK("한국", "호주", "vs", "그해 3월 WBC 패배 설욕", "WBC"), chain='qb', cont=True)
SC['q3'] = dict(MUK("한국", "대만", "vs", "2024 프리미어12 우승팀", "14일 · 대만"), chain='qc')
SC['q4'] = dict(MUK("한국", "대만", "vs", "대만 · 일본에 패 · 슈퍼라운드 탈락", "2024 프리미어12", size=72), chain='qc', cont=True)
SC['q5'] = TLK("결승으로 가는 길", [dict(d="일본전", t="지더라도", c="bad", at=0), dict(d="호주 · 대만전", t="모두 승리", c="good", at=1), dict(d="그러면", t="결승 도전", c="gold", at=1.5)])
# ── 한일전 ──
SC['j4'] = dict(MUK("한국", "일본", "vs", "한일전은?", "2026 APBC"), chain='qj')
SC['j5'] = dict(MUK("한국", "일본", "vs", "일본 3연패 도전", "한일전"), chain='qj', cont=True)
SC['j6'] = TLK("APBC 한일전", [dict(d="2017년 조별리그", t="연장 10회 7대 8 패", c="bad", at=1), dict(d="2023년 조별리그", t="1대 2 패", c="bad", at=2.5)], chain="jt")
SC['j6b'] = TLK("APBC 일본전 네 경기", [dict(d="조별리그 · 결승", t="네 경기 모두 패", c="bad", at=0), dict(d="그 가운데", t="세 경기가 1점 차", c="gold", at=1)])
SC['j7'] = TLK("9월 아시안게임 · 일본전", [dict(d="슈퍼라운드", t="0대 5 패", c="bad", at=0), dict(d="결승", t="3대 1 승 · 금메달", c="gold", at=2)], chain="ag")
SC['j7b'] = KEEP(SC['j7'], items=[dict(d="슈퍼라운드", t="0대 5 패", c="bad", at=-1), dict(d="결승", t="3대 1 승 · 금메달", c="gold", at=-1), dict(d="그때 일본", t="사회인 선수", at=1), dict(d="이번 일본", t="프로 유망주", c="gold", at=2)])
SC['j8'] = TLK("대표팀 변수 · 낯선 자리", [dict(d="2루", t="두 선수가 번갈아", at=0), dict(d="중견수", t="새 얼굴 시험", at=1), dict(d="우익수", t="외야 합류 대비", at=1)])
SC['j8b'] = MUK("한국", "상무", "8 : 4", "6일 연습경기 승리", "연습경기", chain="pr")
SC['j8c'] = dict(S(0, "facegrid", title="상무전", items=[dict(img="경기/APBC_김도영_상무전_카드", name="김도영", team="KIA", at=0), dict(img="경기/APBC_허인서_상무전_카드", name="허인서", team="한화", at=2)], noCenter=True, card=True, cols=2), bg=BG_KOR, text="김도영 홈런 두 개\n허인서 역전 3점 홈런", textAt=1, size=48)
SC['j8e'] = dict(GRID("최원호 감독", ['최원호'], at=0, cols=1), bg=BG_KOR, items=[IT('최원호', 0, say="의외로 괜찮았다", sayAt=3)])
SC['j8d'] = MUK("한국", "울산 웨일즈", "11 : 1", "7일 연습경기 승리", "연습경기")
SC['j8f'] = dict(GRID("울산전 마운드", ['김진욱', '이로운'], at={'김진욱': 0, '이로운': 0}, cols=2), bg=BG_KOR, text="나란히 2이닝 무실점", textAt=1)
SC['j9'] = RB("연습경기 두 경기 · 19득점", [dict(BAR("상무전", 8, 0, unit="점"), valAt=0), dict(BAR("울산전", 11, 0, unit="점"), valAt=0)], 12, bw=260, gap=140)
SC['j10'] = QK("100이닝 넘은 투수 두 명", ["롯데", "SSG"], logoSize=200, size=84, note="2026년")
SC['j10b'] = MUK("한국", "일본", "vs", "승부처 = 불펜 이어 던지기", "한일전", size=72)
# ── 정리 ──
SC['e2c'] = MUK("한국", "일본", "vs", "한국 응원석 약 3천 석 · 앰프 응원", "한일전", size=64)
SC['e2d'] = MUK("한국", "일본", "vs", "전 경기 티빙 생중계", "2026 APBC", size=72)
SC['e3'] = MUK("한국", "일본", "?", "한국 설욕? 아니면 일본?", "2026 APBC", size=80)

SC['w3'] = TG('키움', hi='전준표', text="2023년 세 명 → 이번엔 한 명", textAt=1)
SC['s6'] = TG('삼성', hi=('이재현', '김지찬'), text="한국시리즈 뒤 합류", textAt=1)
SC['q4b'] = dict(MUK("한국", "대만", "6 : 1", "2023 APBC 승리 · 결승행", "2023 APBC"), chain='qd')
SC['q5b'] = TLK("반대로", [dict(d="첫 경기 호주전", t="패배", c="bad", at=0), dict(d="그러면", t="일본전 부담 ↑", c="bad", at=1)])

# ── 11/7 23:30 사용자 "템플릿이 너무 이전 영상들과 같아 금방 질린다 · 다른 유튜브 참고" → 선수 기록 줄은 bt_stat(사진 액자 + 흰 기록 칸), 상징 장면은 bt_full(큰 사진 + 빨간 이름표) ──
BG_BT = {"css": "repeating-linear-gradient(45deg,rgba(255,255,255,.035) 0 2px,rgba(0,0,0,0) 2px 64px),repeating-linear-gradient(-45deg,rgba(255,255,255,.035) 0 2px,rgba(0,0,0,0) 2px 64px),radial-gradient(70% 80% at 30% 40%,#16295C 0%,#0B1634 60%,#070D20 100%)"}
def PH(n): return "경기/APBC_%s_사진" % n
def TI(k, v, at=1, hi=False): return dict(k=k, v=v, at=at, hi=hi)
def STT(n, head, tiles, big=None, tag=None, tagAt=0, cont=False, img=None, focus=None, **k):
    sc = S(0, "bt_stat", img=img or PH(n), name=n, team=TEAMOF.get(n, ''), head=head, tiles=tiles, noCenter=True, bg={"img": img or PH(n), "f": "blur(28px) brightness(.34) saturate(1.15)"}, **k)
    if big: sc['big'] = big
    if tag: sc['tag'] = tag; sc['tagAt'] = tagAt
    if focus: sc['focus'] = focus
    if cont: sc['cont'] = True; sc['chain'] = 'st' + n
    else: sc['chain'] = 'st' + n
    return sc
def FULL(img, tag, cap=None, tagAt=0, capAt=1, focus=None, name=None, **k):
    sc = S(0, "bt_full", img=img, name=name or img.split("_")[1], tag=tag, tagAt=tagAt, noCenter=True, bg={"img": img, "f": "blur(26px) brightness(.38) saturate(1.2)"}, **k)
    if cap: sc['cap'] = cap; sc['capAt'] = capAt
    if focus: sc['focus'] = focus
    return sc
SC['w2'] = STT('전준표', "2026 전준표", [TI("출생", "2005년생", 0), TI("2026 경기", "21", 1), TI("평균자책점", "4.29", 2, True)], big="2026")
SC['t2'] = STT('안현민', "2026 안현민", [TI("부상 공백", "두 달", 1), TI("경기", "94", 2), TI("홈런", "14", 2), TI("타율", "2할 9푼 8리", 3, True)], big="2026")
SC['t2b'] = FULL(PH('안현민'), "2025 신인왕", "그해 11월 도쿄돔 일본전 홈런", tagAt=0, capAt=1)
SC['t4'] = STT('안현민', "안현민", [TI("한국시리즈", "7차전까지 가면", 1), TI("12일 호주전", "못 나올 수도", 2, True)])
SC['s2'] = STT('이재현', "2026 이재현", [TI("타율", "2할 2푼 2리", 1), TI("홈런", "17", 2, True)], big="2026")
SC['s4'] = STT('김지찬', "2026 김지찬", [TI("타율", "3할 1푼 5리", 1, True), TI("도루", "22", 2)], big="2026")
SC['s4b'] = STT('김지찬', "2026 김지찬", [TI("타율", "3할 1푼 5리", 1, True), TI("도루", "22", 2), TI("대표팀 타자 중", "타율 1위", 1, True)], big="2026", cont=True)
SC['s4c'] = FULL(PH('김지찬'), "2023 항저우 · 2026 아시안게임", "이번에도 금메달", tagAt=0, capAt=1)
SC['d2'] = STT('안재석', "2026 안재석", [TI("타율", "2할 7푼 8리", 1), TI("홈런", "11", 2), TI("타점", "67", 2, True)], big="2026")
SC['d3'] = STT('안재석', "안재석의 자리", [TI("소속팀", "3루", 0), TI("대표팀", "2루", 1, True)], cont=True)
SC['d4'] = STT('안재석', "안재석의 자리", [TI("소속팀", "3루", -1), TI("대표팀", "2루", -1, True), TI("이유", "2루수 후보 부상", 0)], cont=True)
SC['d6'] = STT('김민석', "2026 김민석", [TI("경기", "135", 1), TI("타율", "3할 1푼", 1, True), TI("타점", "57", 2)], big="2026")
SC['d7'] = STT('김민석', "상무전", [TI("타순", "1번 타자", 1, True), TI("수비", "중견수", 1)], cont=True)
SC['h2'] = STT('허인서', "2026 허인서", [TI("타율", "2할 8푼 3리", 1), TI("홈런", "20", 2, True), TI("타점", "79", 2)], big="2026")
SC['h3'] = STT('문현빈', "2026 문현빈", [TI("타율", "2할 9푼 7리", 1), TI("홈런", "15", 1), TI("타점", "76", 2, True)], big="2026")
SC['h5'] = STT('문현빈', "대표팀 연습경기", [TI("수비", "우익수", 1, True), TI("이유", "외야 합류 대비", 2)], cont=True)
SC['h6'] = STT('조동욱', "2026 조동욱", [TI("경기", "75", 1), TI("홀드", "10", 1), TI("대표팀 투수 중", "최다 경기", 3, True)], big="2026")
SC['n2'] = STT('김주원', "2026 김주원", [TI("홈런", "18", 1), TI("도루", "30", 1, True), TI("연습경기", "유격수", 3)], big="2026")
SC['n3'] = FULL(PH('김주원'), "2023 APBC 베스트나인", "유격수 김주원", tagAt=0, capAt=1)
SC['n6'] = STT('이준혁', "2026 이준혁", [TI("경기", "34", 1), TI("평균자책점", "2.78", 1, True), TI("대표팀 투수 중", "가장 낮음", 3, True)], big="2026")
SC['l2'] = STT('문정빈', "2026 문정빈", [TI("경기", "91", 1), TI("홈런", "19", 1, True), TI("타점", "66", 2), TI("상무전", "1루수", 4)], big="2026")
SC['l4'] = STT('김영우', "2026 김영우", [TI("경기", "51", 1), TI("승리", "3", 1), TI("홀드", "5", 1, True)], big="2026")
SC['l5'] = STT('박시원', "2026 박시원", [TI("출생", "2006년생", 0, True), TI("경기", "29", 1), TI("승리", "2", 1)], big="2026")
SC['g2'] = STT('김민준', "2026 김민준", [TI("출생", "2006년생", 0), TI("승패", "9승 3패", 1, True), TI("평균자책점", "3.56", 2), TI("상무전", "선발", 3)], big="2026")
SC['g4'] = STT('조형우', "2026 조형우", [TI("타율", "2할 6푼 8리", 1), TI("홈런", "8", 1, True)], big="2026")
SC['r2'] = STT('한동희', "2026 한동희", [TI("타율", "3할 6리", 1), TI("홈런", "25", 1, True), TI("타점", "81", 2)], big="2026")
SC['r2b'] = STT('한동희', "2026 한동희", [TI("타율", "3할 6리", -1), TI("홈런", "25", -1, True), TI("타점", "81", -1), TI("대표팀 타자 중", "홈런 2위", 1, True)], big="2026", cont=True)
SC['r3'] = STT('한동희', "한동희", [TI("출생", "1999년생 · 최고령", 0, True), TI("상무전", "4번 타자 3루수", 3)], cont=True)
SC['r6'] = STT('김진욱', "2026 김진욱", [TI("이닝", "144", 1, True), TI("승리", "7", 1)], big="2026")
SC['r7'] = STT('박정민', "2026 박정민", [TI("경기", "63", 1), TI("승리", "9", 1), TI("홀드", "14", 2, True)], big="2026")
SC['k2b'] = STT('김도영', "김도영의 태극마크", [TI("3월", "WBC", 1), TI("9월", "아시안게임", 1), TI("2026년에만", "세 번째", 2, True)], big="2026")
SC['k3'] = STT('김도영', "2026 김도영", [TI("타율", "3할 8리", 1), TI("홈런", "45", 1, True), TI("타점", "118", 2, True)], big="2026", cont=True)
SC['k3b'] = STT('김도영', "2026 김도영", [TI("타율", "3할 8리", -1), TI("홈런", "45", -1, True), TI("타점", "118", -1, True), TI("대표팀 타자 중", "홈런 · 타점 1위", 0, True)], big="2026", cont=True)
SC['k5'] = STT('박재현', "2026 박재현", [TI("출생", "2006년생", 0), TI("홈런", "19", 1), TI("도루", "21", 1), TI("대표팀", "중견수 후보", 3, True)], big="2026")
SC['k5b'] = STT('박재현', "2026 박재현", [TI("출생", "2006년생", -1), TI("홈런", "19", -1), TI("도루", "21", -1), TI("대표팀 야수 중", "최연소", 1, True)], big="2026", cont=True)
SC['k7'] = STT('김태형', "2026 김태형", [TI("출생", "2006년생", 0), TI("경기", "24", 1), TI("승리", "3", 1, True)], big="2026")
# ── 11/7 23:58 사용자 "자료 영상이 들어가면 좋겠다 · 그 장면을 실제 영상으로"(사용자가 받아 둔 2023 APBC 클립) → bt_clip: 영상 자리에 렌더 뒤 ffmpeg 로 소리 없이 덮는다 ──
CLIPS = {"호주전": dict(file="APBC_영상_호주전.mp4", cw=1480, ch=648), "결승": dict(file="APBC_영상_결승.mp4", cw=1098, ch=912),
         "2017결승": dict(file="APBC_영상_2017결승.mp4", cw=1908, ch=866, hide=[[1440, 625, 380, 241]]),
         "안현민홈런": dict(file="APBC_영상_안현민홈런.mp4", cw=1288, ch=648),
         "프리미어12": dict(file="APBC_영상_프리미어12.mp4", cw=1316, ch=852, hide=[[1110, 660, 206, 192]]),
         "대만전": dict(file="APBC_영상_대만전.mp4", cw=1530, ch=844, hide=[[1175, 645, 330, 199]]),
         "아시안게임": dict(file="APBC_영상_아시안게임.mp4", cw=1484, ch=816),
         "김도영홈런": dict(file="APBC_영상_김도영홈런.mp4", cw=1138, ch=812),
         "한동희홈런": dict(file="APBC_영상_한동희홈런.mp4", cw=1180, ch=760)}   # hide = 중계 점수판 자리(영상 픽셀) — 대사에 없는 점수가 보이지 않게 흐리게
def CLIP(c, tag, tiles, head=None, frm=0.0, cont=False, clipCuts=None, **k):   # clipCuts = 영상에서 쓸 구간들(이어 붙임) — 없으면 frm 부터 끝까지
    z = CLIPS[c]; po = "경기/APBC_영상_" + c
    sc = S(0, "bt_clip", clip=c, clipFile=z['file'], clipFrom=frm, cw=z['cw'], ch=z['ch'], poster=po, tag=tag, tagAt=0, tiles=tiles, noCenter=True, chain='clip' + c, bg={"img": po, "f": "blur(30px) brightness(.32) saturate(1.1)"}, **k)
    if head: sc['head'] = head; sc['headAt'] = 1
    if cont: sc['cont'] = True
    if clipCuts: sc['clipCuts'] = clipCuts
    if z.get('hide'): sc['clipHide'] = z['hide']
    return sc
SC['p4'] = CLIP("결승", "2023 APBC 결승 한일전", [TI("10회 초", "3 : 2 리드", 2), TI("10회 말", "2실점", 3), TI("최종", "3 : 4 패", 4, True)], head="연장 승부치기", frm=0.2, clipCuts=[[0.2, 6.2], [11.2, 12.95]])
SC['q2'] = CLIP("호주전", "2023 APBC 첫 경기 호주전", [TI("연장", "10회 말", 0), TI("결승타", "끝내기 안타", 1), TI("최종", "3 : 2 승", 2, True)])
SC['q2b'] = CLIP("호주전", "2023 APBC 첫 경기 호주전", [TI("그해 3월 WBC", "호주에 패", 1), TI("그해 APBC", "끝내기로 설욕", 2, True)], cont=True)

# ── 11/8 00:27 사용자가 받아 준 클립 7개 + 반론 댓글 에이전트 반영(11/8 01시) ──
SC['p3'] = CLIP("2017결승", "2017 APBC 결승 한일전", [TI("2017년 결승", "0 : 7 패", 1, True)], clipCuts=[[1.5, 4.4]])
SC['t2b'] = CLIP("안현민홈런", "안현민 · 2025년 11월 한일 평가전", [TI("2025년", "신인왕", 0), TI("11월 도쿄돔 일본 평가전", "두 경기 연속 홈런", 2, True)], clipCuts=[[0.2, 2.8], [3.4, 4.4], [8.4, 10.5]])
SC['q3'] = CLIP("프리미어12", "2024 프리미어12 결승", [TI("14일 상대", "대만", 0), TI("2024 프리미어12", "우승", 1, True), TI("결승", "일본에 승", 2)], clipCuts=[[0.6, 4.6], [5.2, 6.8]])
SC['q4'] = MUK("한국", "대만", "vs", "대만 · 일본에 패 · 슈퍼라운드 탈락", "2024 프리미어12", size=72)
SC['q4c'] = MUK("한국", "대만", "4 : 5", "3월 WBC 패", "2026 WBC")
SC['q4d'] = MUK("한국", "대만", "5 : 0", "9월 아시안게임 승", "2026 아시안게임")
SC['q4b'] = CLIP("대만전", "2023 APBC 대만전", [TI("2023 APBC", "6 : 1 승", 1, True), TI("다음", "결승 진출", 2)], clipCuts=[[0.3, 3.2], [9.0, 11.0], [13.8, 15.1]])
SC['j7b'] = TLK("그때 일본 · 이번 일본", [dict(d="그때 일본", t="사회인 선수", at=0), dict(d="이번 일본", t="프로 유망주", c="gold", at=2)])
SC['j7c'] = TLK("프로 한일전", [dict(d="2015년 프리미어12", t="준결승 승리", c="good", at=1), dict(d="그 뒤", t="1무 11패", c="bad", at=2)])
SC['k3'] = CLIP("김도영홈런", "김도영 · 2026 시즌 홈런", [TI("타율", "3할 8리", 1), TI("홈런", "45", 1, True), TI("타점", "118", 2, True)], clipCuts=[[0.8, 9.08]])
SC['k3b'] = CLIP("김도영홈런", "김도영 · 2026 시즌 홈런", [TI("타율", "3할 8리", -1), TI("홈런", "45", -1, True), TI("타점", "118", -1, True), TI("대표팀 타자 중", "홈런 · 타점 1위", 0, True)], clipCuts=[[0.8, 9.08]], cont=True)
SC['r2b'] = CLIP("한동희홈런", "한동희 · 2026 시즌 홈런", [TI("2026년", "25홈런", -1), TI("대표팀 타자 중", "홈런 2위", 1, True)], clipCuts=[[0.3, 2.7], [8.0, 9.85]])
for _k in list(SC):   # 영상 장면 바로 뒤 장면은 이어받기 표시를 뗀다(종류가 달라 이어받을 게 없음)
    pass

# ── 11/8 01:40 검수 에이전트 1라운드(검수본 #3) 반영 ──
SC['o4b'] = TLK("와일드카드 세 명", [dict(d="롯데", t="두 명", at=1), dict(d="삼성", t="한 명", at=1), dict(d="세 명 모두", t="2002년 이전 출생", c="gold", at=3)])
SC['p2'] = KEEP(SC['p1'], items=[dict(d="2017년", t="일본에 져 준우승", c="bad", at=0), dict(d="2023년", t="일본에 져 준우승", c="bad", at=0), dict(d="2026년", t="세 번째 대회", c="gold", at=-1)])
SC['s1'] = TL("삼성 라이온즈", [dict(d="한국시리즈 중", t="투수 둘 빠짐", c="bad", at=2), dict(d="남은 선수", t="야수 두 명", c="gold", at=2)], bg=TBG('삼성'))
SC['d1'] = TL("두산 베어스", [dict(d="팔꿈치 부상", t="투수 이탈", c="bad", at=1), dict(d="남은 선수", t="야수 두 명", c="gold", at=1)], bg=TBG('두산'))
SC['d5'] = STT('안재석', "안재석의 자리", [TI("소속팀", "3루", -1), TI("대표팀", "2루", -1, True), TI("2루는", "3루수 두 명이 번갈아", 1, True)], cont=True)
SC['h5'] = STT('문현빈', "대표팀 연습경기", [TI("수비", "우익수", 1, True), TI("이유", "KT 외야수 합류 늦을 수도", 2)], cont=True)
SC['n4'] = STT('김휘집', "2026 김휘집", [TI("경기", "90", 1), TI("홈런", "14", 1, True), TI("타점", "64", 2)], big="2026")
SC['l6'] = TG('LG', text="2023년 한 명도 → 이번엔 네 명", textAt=3)

# ── 11/8 01:50 검수 3/3 반영 ──
SC['q0'] = TLK("도쿄돔에서 만날 상대", [dict(d="상대 팀", t="호주 · 일본 · 대만", c="gold", at=1)])
SC['q1'] = MUK("한국", "호주", "vs", "2023년에도 첫 경기", "첫 상대")
SC['e2d'] = TLK("2026 APBC 중계", [dict(d="대회 전 경기", t="티빙 생중계", c="gold", at=0)])
SC['j8'] = TLK("대표팀 변수 · 낯선 자리", [dict(d="자리", t="2루 · 중견수 · 우익수", at=1), dict(d="변수", t="낯선 자리에서 뛰는 선수들", c="gold", at=2)])
SC['k2b'] = STT('김도영', "김도영의 태극마크", [TI("3월", "WBC", 1), TI("9월", "아시안게임", 1), TI("2026년에만", "세 번째", 2, True)], img="경기/APBC_김도영_상무전_사진")

# ── 11/8 16시 사용자 "분석이 너무 아쉽고 AI로 돌렸냐는 이야기가 많아"(F-211) → 분석 파트(반론 댓글 에이전트 반영판) ──
SC['a0'] = MUK("한국", "일본", "?", "이 명단으로 일본을 어떻게 잡을까", "분석", size=64)
SC['a1'] = STT('최원호', "마운드 운용", [TI("일정", "4일 연속 경기", 2), TI("선발", "하루씩 다른 네 명", 3, True)], img=PH('최원호'), imgAt=1)
SC['a2'] = SAY(dict(GRID("선발 후보 네 명", ['김진욱', '이로운', '김건우', '김민준'], at={'김진욱': 0, '이로운': 0, '김건우': 1, '김민준': 1}, cols=4), bg=BG_KOR, text="2026년 100이닝 넘긴 투수 둘", textAt=2, size=50), {'김건우': ('평균자책점 6점대', 5)})
SC['a3'] = MUK("한국", "일본", "vs", "일본 선발 후보 모두 120이닝 이상", "선발 싸움", size=60)
SC['a3b'] = MUK("한국", "일본", "vs", "시즌 내내 선발로 버틴 투수 수 차이", "선발 싸움", size=60)
SC['a4'] = TLK("한국 마운드 운용", [dict(d="선발", t="3이닝만 버텨도 성공", at=1), dict(d="승부처", t="4회~6회 스윙맨", c="gold", at=3)], chain='a4')
SC['a4b'] = dict(TLK("한국 마운드 운용", [dict(d="선발", t="3이닝만 버텨도 성공", at=-1), dict(d="승부처", t="4회~6회 스윙맨", c="gold", at=-1), dict(d="4일 연속 경기", t="필승조 매일 못 씀", c="bad", at=0)], chain='a4'), cont=True)
SC['a5'] = SAY(dict(GRID("마무리 후보", ['최준용', '박정민'], at={'최준용': 3, '박정민': 3}, cols=2), bg=BG_KOR, text="감독: 경험·기록 보고 둘 중 한 명", textAt=1, size=40), {'최준용': ('15세이브', 3), '박정민': ('14홀드', 3)})
SC['a6'] = TLK("왼손 불펜", [dict(d="왼손 불펜", t="두 명 이탈", c="bad", at=0), dict(d="감독 대책", t="좌타자에 강했던 투수", c="gold", at=3)], chain='a6')
SC['a6b'] = dict(TLK("왼손 불펜", [dict(d="왼손 불펜", t="두 명 이탈", c="bad", at=-1), dict(d="감독 대책", t="좌타자에 강했던 투수", c="gold", at=-1), dict(d="후반 승부", t="그 투수가 누구냐", at=0)], chain='a6'), cont=True)
SC['a7'] = STT('김도영', "타선의 열쇠", [TI("더 중요한 것", "김도영 뒤 타자", 2, True)], img=PH('김도영_상무전'), imgAt=1)
SC['a8'] = dict(GRID("최원호 감독", ['최원호'], at=-1, cols=1), bg=BG_KOR, items=[IT('최원호', -1, say="특히 일본 투수들은 뒤가 조금 약하다고 느끼면 계속 유인구만 던질 것이다", sayAt=1)])
SC['a9'] = STT('김도영', "울산전 김도영", [TI("울산전", "네 타석 모두 삼진", 2, True), TI("첫 두 타석", "바깥쪽 높은 볼에 헛스윙", 4)], img=PH('김도영'), chain='a9')
SC['a9b'] = STT('김도영', "울산전 김도영", [TI("울산전", "네 타석 모두 삼진", -1, True), TI("첫 두 타석", "바깥쪽 높은 볼에 헛스윙", -1), TI("일본 투수들이 노릴 곳", "바깥쪽 높은 볼", 0, True)], img=PH('김도영_상무전'), cont=True)
SC['a10'] = dict(GRID("연습경기 4번 타자", ['한동희', '문정빈'], at={'한동희': 1, '문정빈': 1}, cols=2), bg=BG_KOR)
SC['a11'] = dict(GRID("김도영 다음 타순", ['김도영', '안현민'], at={'김도영': 1, '안현민': 6}, cols=2, chain='a11'), bg=BG_KOR, text="뒤 타자 조건: 선구안 · 컨택 · 파워", textAt=2, size=46)
SC['a12'] = dict(GRID("김도영 다음 타순", ['김도영', '안현민'], at={'김도영': -1, '안현민': -1}, cols=2, chain='a11'), bg=BG_KOR, text="안현민 출루율 2년 연속 4할 · 앞 타순도 고민", textAt=1, size=44, cont=True)
SC['a13'] = MUK("한국", "일본", "vs", "와일드카드 셋 중 둘 = 홈런 타자", "이구치 감독", size=64)
SC['a14'] = SAY(dict(GRID("일본 경계 타자", ['마사키 도모야', '야마구치 고키'], cols=2), bg=BG_KOR, items=[dict(img="경기/JPN_마사키_카드", name="마사키 도모야", team="", at=0), dict(img="경기/JPN_야마구치_카드", name="야마구치 고키", team="", at=3)]), {'마사키 도모야': ('28홈런 · 일본시리즈 MVP', 1), '야마구치 고키': ('38홈런', 4)})
SC['a15'] = STT('야마구치 고키', "야마구치 고키", [TI("113경기 볼넷", "27개", 1, True), TI("출루율", "3할 2푼 9리", 2)], img="경기/JPN_야마구치")
SC['a15b'] = STT('야마구치 고키', "야마구치 고키", [TI("113경기 볼넷", "27개", -1, True), TI("출루율", "3할 2푼 9리", -1), TI("한국의 수", "유인구 승부", 2, True)], img="경기/JPN_야마구치", cont=True)
SC['a16'] = STT('다카하시 히로토', "일본 에이스", [TI("일본 언론 보도", "13일 한국전 대신", 2), TI("유력", "결승 선발", 3, True)], img="경기/JPN_다카하시")
SC['a16b'] = STT('다카하시 히로토', "일본 에이스", [TI("일본 언론 보도", "13일 한국전 대신", -1), TI("유력", "결승 선발", -1, True), TI("결승에 가면", "다카하시와 대결", 1, True)], img="경기/JPN_다카하시", cont=True)
SC['a17'] = MUK("한국", "일본", "vs", "일본 28명 중 23명 첫 대표팀", "경험", size=64)
SC['a17b'] = MUK("한국", "일본", "vs", "한국 11명 · 아시안게임 결승에서 일본 격파", "경험", size=58)
SC['a17c'] = MUK("한국", "일본", "vs", "사회인 상대지만 · 결승 압박을 이겨 본 경험", "경험", size=58)
# ── 11/8 15:50 사용자 "KT 5차전에서 질 거 같아, 한국시리즈 끝났다고 알고 만들어줘" ──
SC['t4'] = STT('안현민', "안현민", [TI("한국시리즈 뒤", "대표팀 합류", 1, True)])
SC['s1'] = TL("삼성 라이온즈", [dict(d="한국시리즈", t="투수 둘 빠짐", c="bad", at=2), dict(d="남은 선수", t="야수 두 명", c="gold", at=2)], bg=TBG('삼성'))
SC['h5'] = STT('문현빈', "대표팀 연습경기", [TI("수비", "우익수", 1, True), TI("이유", "KT 외야수 늦은 합류 대비", 2)], cont=True)

# ── 11/8 17시 검수본4 반영 ──
SC['o3'] = CLIP("아시안게임", "2026 아시안게임 결승 한일전", [TI("대표팀 28명 중", "11명", 0, True), TI("9월 아시안게임", "금메달", 2, True)], frm=1.0, clipCuts=[[1.0, 3.8], [8.4, 11.5]])
SC['j8'] = TLK("대표팀 변수 · 낯선 자리", [dict(d="자리", t="2루 · 중견수 · 우익수", at=1), dict(d="변수", t="낯선 자리 출전", c="gold", at=2)])
SC['s1'] = TL("삼성 라이온즈", [dict(d="한국시리즈", t="KT와 맞대결", at=0), dict(d="투수 둘", t="빠짐", c="bad", at=2), dict(d="남은 선수", t="야수만", c="gold", at=3)], bg=TBG('삼성'))


# ── 11/8 18시 검수본4 구조 수정(사용자 "구조까지 고치기") — 연결어·기록줄·분석 파트 새 장면 ──
def CELLS(title, items, cols, cw=230, ch=110, **k):
    sc = S(0, "cells", title=title, items=items, cols=cols, cw=int(cw * 1.3), ch=int(ch * 1.3), **k); sc.setdefault('bg', BG_KOR)
    for it in sc['items']: it['fs'] = int(it.get('fs', 40) * 1.3)
    return sc
def C(t, at=0, **k): return dict(dict(t=t, at=at), **k)
POS8 = ["포수", "1루수", "2루수", "3루수", "유격수", "좌익수", "중견수", "우익수"]
def POSC(bad, at): return [C(x, -1 if x not in bad else at, **({'bad': True} if x in bad else {})) for x in POS8]
SC['w1'] = TG('키움', new={'전준표': 1}, text="투수 한 명", textAt=1)
SC['w3'] = TG('키움', hi='전준표', text="감독이 꼽은 스윙맨 후보", textAt=2)
SC['s1'] = TL("삼성 라이온즈", [dict(d="한국시리즈", t="우승", c="gold", at=0), dict(d="투수 둘", t="빠짐", c="bad", at=2), dict(d="남은 선수", t="야수만", at=2.4)], bg=TBG('삼성'))
SC['s4c'] = FULL(PH('김지찬'), "2023 항저우 · 2026 아시안게임", "9월 아시안게임도 금메달", tagAt=0, capAt=1)
SC['d8'] = CELLS("대표팀 수비 자리", POSC(("2루수",), 0), 4, cw=220, ch=100, text="2루 후보 = 모두 3루수", textAt=0.5, size=60)
SC['j8'] = CELLS("대표팀 변수 · 낯선 자리", POSC(("2루수", "중견수", "우익수"), 1), 4, cw=220, ch=100, text="연습경기 · 낯선 선수들이 맡은 자리", textAt=2, size=52)
SC['h2'] = STT('허인서', "2026 허인서", [TI("타율", "2할 8푼 3리", 1), TI("홈런", "20", 1, True), TI("타점", "79", 2), TI("대표팀 포수 둘 중", "장타력 앞섬", 4, True)], big="2026")
SC['n4b'] = STT('김휘집', "2026 김휘집", [TI("경기", "90", -1), TI("홈런", "14", -1, True), TI("타점", "64", -1), TI("울산전 2루", "넓은 수비 범위", 2, True)], big="2026", cont=True)
SC['g4'] = STT('조형우', "2026 조형우", [TI("타율", "2할 6푼 8리", 1), TI("홈런", "8", 1, True), TI("연습경기", "포수 둘이 번갈아", 3)], big="2026")
SC['e2d'] = KEEP(SC['e2c'], text="대회 전 경기 · 티빙 생중계")
SC['j7b'] = CELLS("그때 일본 · 이번 일본", [C("9월 아시안게임\n사회인 선수", 1), C("이번 APBC\n프로 유망주", 2, hi=True)], 2, cw=440, ch=170, fs=46)
SC['a1'] = CELLS("4일 연속 경기 · 선발 운용", [C("첫째 날", 1), C("둘째 날", 1), C("셋째 날", 1), C("넷째 날", 1)], 4, cw=220, ch=110, text="하루씩 다른 선발 네 명", textAt=2, size=60)
SC['a3'] = RB("2026년 100이닝 넘긴 선발 후보", [dict(BAR("한국", 2, 0), valAt=0), dict(BAR("일본", 4, 0, hi=True, txt="4명 · 모두 120이닝+"), valAt=0)], 4, bw=260, gap=200, chain='a3')
SC['a3b'] = KEEP(SC['a3'], title="시즌 내내 버틴 선발 · 두 배 차이")
SC['a4'] = CELLS("한국 마운드 운용 · 제 생각", [C("3회까지\n선발", 1), C("4~6회\n스윙맨", 3, hi=True), C("그 뒤\n필승조", 3)], 3, cw=330, ch=170, fs=46, chain='a4', text="4일 연속 · 필승조 매일 못 씀", thide=True, size=56)
SC['a4b'] = CELLS("한국 마운드 운용 · 제 생각", [C("3회까지\n선발", -1), C("4~6회\n스윙맨", -1, hi=True), C("그 뒤\n필승조", -1, bad=True)], 3, cw=330, ch=170, fs=46, chain='a4', cont=True, text="4일 연속 · 필승조 매일 못 씀", textAt=1, size=56)
SC['a4c'] = CELLS("연습경기 두 번 · 마운드 운용", [C("상무전", 0, on=False), C("선발\n2이닝", 1), C("다음 투수\n2이닝", 2, hi=True), C("울산전", 0, on=False), C("선발\n2이닝", 1), C("다음 투수\n2이닝", 2, hi=True)], 3, cw=300, ch=140, fs=44)
SC['a5b'] = KEEP(SC['a5'], text=None)
for _it in SC['a5b']['items']:
    if _it.get('name') == '최준용': _it['say'], _it['sayAt'] = '마무리', 1
    if _it.get('name') == '박정민': _it['say'], _it['sayAt'] = '7·8회', 3
SC['a5b'].pop('text', None)
SC['a6'] = CELLS("빠진 왼손 불펜", [C("왼손 불펜\n부상 이탈", 1, bad=True), C("왼손 불펜\n한국시리즈", 1, bad=True)], 2, cw=420, ch=160, fs=46, text="대신: 좌타자에게 강했던 투수", textAt=3, size=56)
SC['a6b'] = STT('조동욱', "제 생각 · 왼손 첫 카드", [TI("2026 경기", "75", 1), TI("왼손 불펜", "첫 번째 카드", 2, True)], imgAt=1)
SC['a8'] = FULL("경기/김도영_45호_타격_1012_KIA제공", "감독이 본 일본", '"계속 유인구만 던질 것이다"', tagAt=0, capAt=1, name='김도영')
SC['a9'] = STT('김도영', "울산전 김도영", [TI("울산전", "네 타석 모두 삼진", 2, True), TI("첫 두 타석", "바깥쪽 높은 볼에 헛스윙", 4)], img=PH('김도영_상무전'), chain='a9')
SC['a11'] = dict(GRID("김도영 뒤 타자 조건", ['김도영'], at={'김도영': 1}, cols=1), bg=BG_KOR, items=[IT('김도영', 1, img="경기/김도영_45호_주루_1012_KIA제공")], text="선구안 · 컨택 · 어느 정도 파워", textAt=2, size=52)
SC['a11b'] = SAY(dict(GRID("제 생각 · 조건에 더 가까운 타자", ['안현민', '한동희'], at={'안현민': 1, '한동희': 2}, cols=2), bg=BG_KOR), {'안현민': ('OPS 0.947', 1), '한동희': ('OPS 0.915', 2)})
SC['a12'] = dict(GRID("제 생각 · 김도영 다음 타자", ['안현민', '김도영'], at={'안현민': 0, '김도영': 3}, cols=2), bg=BG_KOR, items=[IT('안현민', 0, img="경기/APBC_안현민_카드"), IT('김도영', 3, img="경기/김도영_43호_타격_KIA제공")], text="저라면 김도영 뒤에 안현민", textAt=3, size=52)
SC['a13'] = CELLS("일본 와일드카드 세 자리", [C("와일드카드\n홈런 타자", 3, hi=True), C("와일드카드\n홈런 타자", 3, hi=True), C("와일드카드", 2)], 3, cw=330, ch=170, fs=44, text="장타를 칠 수 있는 선수", textAt=1, size=56)
SC['a16b'] = STT('다카하시 히로토', "일본 에이스", [TI("일본 언론 보도", "13일 한국전 대신", -1), TI("유력", "결승 선발", -1, True), TI("13일 한일전", "결승 대비 타순 시험", 3, True)], img="경기/JPN_다카하시", cont=True)
SC['a17'] = CELLS("일본 대표팀 28명", [C("", 0, hi=True) for _ in range(23)] + [C("", 0) for _ in range(5)], 14, cw=70, ch=70, label="23명이 첫 대표팀")
SC['a17b'] = CELLS("한국 대표팀 28명", [C("", 0, hi=True, c="#D9A21B") for _ in range(11)] + [C("", 0) for _ in range(17)], 14, cw=60, ch=60, label="11명 · 9월 아시안게임 결승에서 일본 격파")
SC['a18'] = CELLS("제가 보는 일본 잡는 법", [C("선발\n3이닝", 1), C("4회부터\n물량 계투", 2), C("뒤 타순까지\n강하게", 3), C("유인구\n돌려주기", 4, hi=True)], 4, cw=250, ch=170, fs=40)

# ── 11/8 19시 반론 댓글 에이전트 반영 + 사진 시기·중복 정리 ──
SC['o2b'] = QK("구단별 명단 · 일본 잡는 법", ALL10, logoSize=150, size=80, chain="o2", cont=True)
SC['w3'] = TG('키움', hi='전준표', text="선발이 무너질 때 · 스윙맨 후보", textAt=1.5)
SC['s4c'] = FULL("경기/APBC_김지찬_AG_사진", "2023 항저우 · 2026 아시안게임", "9월 아시안게임도 금메달", tagAt=0, capAt=1, name='김지찬')
SC['h3'] = STT('문현빈', "2026 문현빈", [TI("타율", "2할 9푼 7리", 1), TI("홈런", "15", 1), TI("타점", "76", 2, True)], big="2026", img="경기/APBC_문현빈_한화_사진")
SC['n2'] = STT('김주원', "2026 김주원", [TI("홈런", "18", 1), TI("도루", "30", 1, True), TI("연습경기", "유격수", 3)], big="2026", img="경기/APBC_김주원_NC_사진")
SC['g2'] = STT('김민준', "2026 김민준", [TI("출생", "2006년생", 0), TI("승패", "9승 3패", 1, True), TI("평균자책점", "3.56", 2), TI("상무전", "선발", 3)], big="2026", img="경기/APBC_김민준_투구_사진")
SC['g3'] = TG('SSG', hi=('김건우', '이로운'), new={'김건우': 0, '이로운': 2}, text="김건우 130이닝+ 9승 · 이로운 8승", textAt=2, size=50)
SC['l6'] = TG('LG', text="2023년 한 명도 → 이번엔 네 명", textAt=1)
SC['j8f'] = dict(GRID("울산전 마운드", ['김진욱', '이로운'], cols=2), bg=BG_KOR, items=[IT('김진욱', 0, img="경기/김진욱_1011_롯데제공"), IT('이로운', 1, img="경기/APBC_이로운_투구_카드")], text="둘 다 2이닝 무실점", textAt=2)
SC['a2'] = SAY(dict(GRID("선발 후보 네 명", ['김진욱', '이로운', '김건우', '김민준'], cols=4), bg=BG_KOR, items=[IT('김진욱', 0, img="경기/김진욱_1011_롯데제공"), IT('이로운', 0, img="경기/APBC_이로운_투구_카드"), IT('김건우', 1), IT('김민준', 1, img="경기/APBC_김민준_투구_사진")], text="2026년 100이닝 넘긴 투수 둘", textAt=2, size=50), {'김건우': ('평균자책점 6점대', 5)})
SC['a4b'] = CELLS("한국 마운드 운용 · 제 생각", [C("3회까지\n선발", 0), C("4~6회\n스윙맨", 0, hi=True), C("그 뒤\n필승조", 0.5, bad=True)], 3, cw=330, ch=170, fs=46, text="필승조는 일본전 · 대만전에", textAt=1, size=56)
SC['a4c'] = CELLS("연습경기 두 번 · 선발 후보 넷", [C("상무전", 0, on=False), C("선발 후보\n2이닝", 1), C("선발 후보\n2이닝", 1, hi=True), C("울산전", 0, on=False), C("선발 후보\n2이닝", 1), C("선발 후보\n2이닝", 1, hi=True)], 3, cw=300, ch=140, fs=42)
SC['a5b'] = KEEP(SC['a5'])
SC['a5b'].pop('text', None)
for _it in SC['a5b']['items']:
    if _it.get('name') == '최준용': _it['say'], _it['sayAt'] = '2023 APBC · 9월 아시안게임', 1.5
SC['a5b']['items'] = [x for x in SC['a5b']['items']]
SC['a5b']['text'] = "저라면 마무리는 최준용"; SC['a5b']['textAt'] = 3; SC['a5b']['size'] = 50
SC['a9'] = STT('김도영', "울산전 김도영", [TI("울산전", "네 타석 연속 삼진", 2, True), TI("첫 두 타석", "존 밖 공에 방망이", 4)], img=PH('김도영_상무전'), chain='a9')
SC['a9b'] = STT('김도영', "울산전 김도영", [TI("울산전", "네 타석 연속 삼진", -1, True), TI("첫 두 타석", "존 밖 공에 방망이", -1), TI("일본 투수들이 노릴 곳", "존 밖 유인구", 0, True)], img=PH('김도영_상무전'), cont=True)
SC['a11b'] = SAY(dict(GRID("조건에 가장 가까운 타자", ['안현민'], at={'안현민': 1}, cols=1), bg=BG_KOR), {'안현민': ('2년 연속 출루율 4할', 2)})
SC['a12'] = dict(GRID("김도영 다음 타자", ['안현민', '김도영'], cols=2), bg=BG_KOR, items=[IT('안현민', 0, img="경기/APBC_안현민_카드"), IT('김도영', 2, img="경기/김도영_43호_타격_KIA제공")], text="안현민은 김도영 뒤에", textAt=2.5, size=52)
SC['a15'] = STT('야마구치 고키', "야마구치 고키", [TI("경기", "113", 1), TI("삼진", "107개", 2, True)], img="경기/JPN_야마구치")
SC['a15b'] = STT('야마구치 고키', "야마구치 고키", [TI("경기", "113", -1), TI("삼진", "107개", -1, True), TI("한국의 수", "유인구 승부", 2, True)], img="경기/JPN_야마구치", cont=True)
SC['a16b'] = STT('다카하시 히로토', "일본 에이스", [TI("일본 언론 보도", "13일 한국전 대신", -1), TI("유력", "결승 선발", -1, True), TI("결승에 가면", "다카하시와 대결", 1, True)], img="경기/JPN_다카하시", cont=True)
SC['a17b'] = CELLS("한국 대표팀 28명", [C("", 0, hi=True, c="#D9A21B") for _ in range(11)] + [C("", 0) for _ in range(17)], 14, cw=70, ch=70, label="9월 아시안게임 금메달 멤버 11명")
SC['a18'] = CELLS("제가 보는 일본 잡는 법", [C("선발\n짧게", 1), C("4회부터\n물량 계투", 2), C("뒤 타순까지\n두껍게", 3), C("유인구\n돌려주기", 4, hi=True)], 4, cw=250, ch=170, fs=40)
SC['h5'] = STT('문현빈', "대표팀 연습경기", [TI("수비", "우익수", 1, True), TI("이유", "KT 외야수 늦은 합류 대비", 2)])
SC['h5']['chain'] = 'st문현빈_대표팀'
SC['p5']['items'][0]['img'] = "경기/김도영_45호_1012_KIA제공"
SC['a7'] = STT('김도영', "타선의 열쇠", [TI("더 중요한 것", "김도영 뒤 타자", 2, True)], img="경기/김도영_세리머니_1017_KIA제공", imgAt=1)
SC['a10'] = dict(GRID("연습경기 4번 타자", ['한동희', '문정빈'], cols=2), bg=BG_KOR, items=[IT('한동희', 1, img="경기/한동희_타격_0918_롯데제공"), IT('문정빈', 1, img="경기/문정빈_타격_LG제공")])
for _k in ('a5', 'a5b'):
    for _it in SC[_k]['items']:
        if _it.get('name') == '최준용': _it['img'] = "경기/APBC_최준용_원정_카드"
SC['q4'] = MUK("한국", "대만", "vs", "대만 · 일본에 져 슈퍼라운드 탈락", "2024 프리미어12")   # 검수본4 #28: 이어지는 대결 화면 글 크기 통일(국기 위치 고정)
SC['j5'] = dict(MUK("한국", "일본", "vs", "일본 3연패 도전", "한일전", size=64), cont=True)

# ── 11/8 밤 인포그래픽 샘플(사용자 "카드만 주구장창") ──
R28 = [('LG', ['김영우', '박시원', '우강훈', '문정빈'], 'top'), ('SSG', ['김민준', '이로운', '김건우', '조형우'], 'top'), ('롯데', ['최준용', '박정민', '김진욱', '한동희'], 'top'), ('KIA', ['성영탁', '김태형', '김도영', '박재현'], 'top'),
       ('한화', ['조동욱', '허인서', '문현빈'], ''), ('NC', ['이준혁', '김휘집', '김주원'], ''), ('삼성', ['이재현', '김지찬'], ''), ('두산', ['안재석', '김민석'], ''), ('키움', ['전준표'], 'low'), ('KT', ['안현민'], 'low')]
SC['o1'] = S(0, "apbc_teams", title="APBC 대표팀", teams=[dict(team=t, faces=[CI(n) for n in ns], top=(f == 'top'), low=(f == 'low')) for t, ns, f in R28], hiTop=2, hiLow=4, bg=BG_KOR)
SC['o5'] = S(0, "apbc_sched", title="2026 APBC", phase='rr', when="11월 12일부터 · 도쿄돔", big="네 나라가\n한 번씩 맞붙기", rrAt=2, bg=BG_KOR, chain='sched')
SC['o6'] = S(0, "apbc_sched", title="2026 APBC", phase='final', l0="세 경기 성적", l1="상위 두 팀", l2="15일 결승", fAt0=0, fAt1=1, fAt2=2, dimLines=True, bg=BG_KOR, chain='sched', cont=True)
SC['o7'] = S(0, "apbc_sched", title="한국 경기 일정", phase='kor', games=[dict(d="12일", t="정오", vs="호주", at=0), dict(d="13일 금요일", t="저녁 7시", vs="일본", at=1), dict(d="14일", t="저녁 7시", vs="대만", at=2)],
             korHi=[dict(vs="호주", at=0), dict(vs="일본", at=1), dict(vs="대만", at=2)], dimLines=True, bg=BG_KOR, chain='sched', cont=True)
SC['a4'] = S(0, "apbc_innings", title="한국 마운드 운용 · 제 생각", groups=[dict(**{'from': 1}, to=3, label="선발", at=1, c="#FFFFFF"), dict(**{'from': 4}, to=6, label="스윙맨", at=3, c="#3D7BFF"), dict(**{'from': 7}, to=9, label="필승조", at=4, c="#E8A100")], bg=BG_KOR, chain='inn')
SC['j8'] = S(0, "apbc_field", title="연습경기 · 낯선 자리", hi=[dict(pos="2루수", at=1), dict(pos="중견수", at=1.4), dict(pos="우익수", at=1.8)], side=[dict(t="2루 · 중견수 · 우익수", at=1), dict(t="낯선 선수들이 맡음", at=2, gold=True)], bg=BG_KOR)

# ══════════ 11/8 밤 v7 전면 재설계 — 장면 설계표(카드·글 30% 이하, 단락마다 인포그래픽) · 새 호흡 번호 ══════════
BLUE_ = "#3D7BFF"; GOLD_ = "#E8A100"; PURP_ = "#B07CFF"; GRN_ = "#16A34A"
BY = {'성영탁': 2004, '김태형': 2006, '최준용': 2001, '박정민': 2003, '김진욱': 2002, '김민준': 2006, '이로운': 2004, '김건우': 2002, '김영우': 2005, '박시원': 2006, '우강훈': 2002, '조동욱': 2004, '이준혁': 2003, '전준표': 2005,
      '김도영': 2003, '박재현': 2006, '한동희': 1999, '조형우': 2002, '문정빈': 2003, '허인서': 2003, '문현빈': 2004, '김주원': 2002, '김휘집': 2002, '이재현': 2003, '김지찬': 2001, '안재석': 2002, '김민석': 2004, '안현민': 2003}
BAT14 = ['김도영', '박재현', '한동희', '조형우', '문정빈', '허인서', '문현빈', '김주원', '김휘집', '이재현', '김지찬', '안재석', '김민석', '안현민']
def AX(title, names, hi, **k): return S(0, "apbc_ages", title=title, people=[dict(img=CI(n), y=BY[n], hi=(n == hi)) for n in sorted(names, key=lambda n: BY[n])], bg=BG_KOR, **k)
def RK(title, rows, **k): return S(0, "apbc_rank", title=title, rows=rows, bg=BG_KOR, **k)
def RR(n, v, lab=None, hi=False, at=None, **k): return dict(dict(img=CI(n), v=v, hi=hi), **({'lab': lab} if lab else {}), **({'at': at} if at is not None else {}), **k)
def FLD(title, **k): return S(0, "apbc_field", title=title, bg=BG_KOR, **k)
def INN(title, groups=None, rows=None, **k): return S(0, "apbc_innings", title=title, **({'groups': groups} if groups else {'rows': rows}), bg=BG_KOR, **k)
def G9(a, b, label, at, c="#FFFFFF", **k): return dict(dict(to=b, label=label, at=at, c=c), **{'from': a}, **k)
def SL(team, slots, badges=None, **k): return S(0, "apbc_slots", team=team, slots=slots, badges=badges or [], bg=BG_KOR, **k)
def MV(team, imgs, fromLabel, cap, moveAt, capAt, **k): return S(0, "apbc_move", team=team, imgs=imgs, fromLabel=fromLabel, cap=cap, moveAt=moveAt, capAt=capAt, bg=BG_KOR, **k)

# 오프닝
SC['o1'] = S(0, "apbc_teams", title="APBC 대표팀", teams=[dict(team=t, faces=[CI(n) for n in ns], top=(f == 'top'), low=(f == 'low')) for t, ns, f in R28], hiTop=2, hiLow=4, bg=BG_KOR)
SC['o3'] = CLIP("아시안게임", "2026 아시안게임 결승 한일전", [TI("대표팀 28명 중", "11명", 0, True), TI("9월 아시안게임", "금메달 멤버", 2, True)], frm=1.0, clipCuts=[[1.0, 3.8], [8.4, 11.5]])
SC['o4'] = S(0, "apbc_wild", title="APBC 출전 자격", rules=[dict(t="24세 이하", at=1), dict(t="입단 3년 차 이내", at=2)], wildAt=3, bg=BG_KOR, chain='wild')
SC['o4b'] = S(0, "apbc_wild", title="APBC 출전 자격", rules=[dict(t="24세 이하", at=-1), dict(t="입단 3년 차 이내", at=-1)], wildAt=-1, faces=[dict(img=CI('한동희'), team='롯데', at=1), dict(img=CI('최준용'), team='롯데', at=1.3), dict(img=CI('김지찬'), team='삼성', at=1.6)], badge="세 명 모두 2002년 이전 출생", badgeAt=3, bg=BG_KOR, chain='wild', cont=True)
SC['o5'] = S(0, "apbc_sched", title="2026 APBC", phase='rr', when="11월 12일부터 · 도쿄돔", whenAt=0, big="네 나라가\n한 번씩 맞붙기", rrAt=3, bg=BG_KOR, chain='sched')
SC['o6'] = S(0, "apbc_sched", title="2026 APBC", phase='final', l0="세 경기 성적", l1="상위 두 팀", l2="15일 결승", fAt0=0, fAt1=1, fAt2=2, dimLines=True, bg=BG_KOR, chain='sched', cont=True)
SC['o7'] = S(0, "apbc_sched", title="한국 경기 일정", phase='kor', games=[dict(d="12일", t="정오", vs="호주", at=0), dict(d="13일 금요일", t="저녁 7시", vs="일본", at=1), dict(d="14일", t="저녁 7시", vs="대만", at=2)],
             korHi=[dict(vs="호주", at=0), dict(vs="일본", at=1), dict(vs="대만", at=2)], dimLines=True, bg=BG_KOR, chain='sched', cont=True)
SC['o7b'] = dict(GRID("APBC 대표팀 감독", ['최원호'], at=1, cols=1), bg=BG_KOR)
# 지난 대회
SC['p1'] = S(0, "apbc_hist", title="APBC 연혁", nodes=[dict(y="2017", at=0), dict(y="2023", at=0.4), dict(y="2026", sub="세 번째 대회", at=1, hi=True)], bg=BG_KOR, chain='hist')
SC['p2'] = S(0, "apbc_hist", title="APBC 연혁", nodes=[dict(y="2017", at=-1, res="결승 일본에 패", resAt=1), dict(y="2023", at=-1, res="결승 일본에 패", resAt=1.3), dict(y="2026", sub="세 번째 대회", at=-1, hi=True)], bg=BG_KOR, chain='hist', cont=True)
SC['p3'] = CLIP("2017결승", "2017 APBC 결승 한일전", [TI("2017년 결승", "0 : 7 패", 1, True)], clipCuts=[[1.5, 4.4]])
SC['p4'] = CLIP("결승", "2023 APBC 결승 한일전", [TI("연장", "승부치기", 1), TI("10회 초", "3 : 2 리드", 2), TI("10회 말", "2실점", 3), TI("최종", "3 : 4 패", 4, True)], head="연장 승부치기", frm=0.2, clipCuts=[[0.2, 6.2], [11.2, 12.95]])
SC['p5'] = S(0, "apbc_hist", title="2023 대표팀 → 2026 대표팀", gap=900, nodes=[dict(y="2023", sub="APBC 준우승", at=0), dict(y="2026", sub="이번 대표팀", at=0, hi=True)],
             carry=dict(imgs=[CI('김도영'), CI('김주원'), CI('김휘집'), CI('문현빈'), CI('최준용')], ats=[1, 1.3, 1.6, 2, 2.3], at=1, **{'from': 0}, to=1, moveAt=3), bg=BG_KOR)
SC['o8'] = S(0, "apbc_waffle", title="처음 뽑힌 33명", n=33, out=[dict(idx=[4, 15, 27], at=1, c="#E5484D", label="부상 3명"), dict(idx=[9, 30], at=3, c="#8A93A6", label="한국시리즈 2명")], bg=BG_KOR, chain='waf')
SC['o9'] = S(0, "apbc_waffle", title="최종 28명", n=33, out=[dict(idx=[4, 15, 27], at=-1, c="#E5484D", label=""), dict(idx=[9, 30], at=-1, c="#8A93A6", label="")],
             groups=[dict(n=14, label="투수 14", c=BLUE_, at=1), dict(n=2, label="포수 2", c=GRN_, at=1.4), dict(n=7, label="내야수 7", c=GOLD_, at=2), dict(n=5, label="외야수 5", c=PURP_, at=2.4)], bg=BG_KOR, chain='waf', cont=True)
for _o in SC['o9']['out']: _o['label'] = None
# 키움
SC['w1'] = TG('키움', new={'전준표': 1}, text="투수 한 명", textAt=1)
SC['w2'] = STT('전준표', "2026 전준표", [TI("출생", "2005년생", 0), TI("경기", "21", 1), TI("평균자책점", "4.29", 2, True)], big="2026")
SC['w3'] = INN("감독이 본 전준표의 자리", [G9(1, 3, "선발이 무너질 때", 1, bad=True), G9(4, 6, "스윙맨 후보", 2, c=BLUE_, img=CI('전준표'), imgAt=0)])
# KT
SC['t1'] = TG('KT', new={'안현민': 1}, text="외야수 한 명", textAt=1)
SC['t1b'] = SL('KT', [dict(icon='bat', label="외야수", at=0), dict(icon='ball', label="투수", at=2, xAt=3, xLabel="원칙상 제외")], [dict(t="정규시즌 1위", at=0), dict(t="한국시리즈 직행", at=1, gold=True)], title="KT 위즈 · 대표팀")
SC['t2'] = STT('안현민', "2026 안현민", [TI("부상", "두 달 쉼", 1), TI("경기", "94", 2), TI("홈런", "14", 3, True), TI("타율", "2할 9푼 8리", 4)], big="2026")
SC['t2b'] = CLIP("안현민홈런", "안현민 · 2025년 11월 한일 평가전", [TI("2025년", "신인왕", 0), TI("11월 도쿄돔 일본 평가전", "두 경기 연속 홈런", 1.5, True)], clipCuts=[[0.2, 2.8], [3.4, 4.4], [5.6, 7.5]])
SC['t4'] = MV('KT', [PH('안현민')], "한국시리즈", "한국시리즈 마치고 합류", 1, 2, title="안현민 합류")
# 삼성
SC['s1'] = SL('삼성', [dict(icon='ball', label="투수", at=1, xAt=2, xLabel="한국시리즈"), dict(icon='ball', label="투수", at=1, xAt=2.2, xLabel="한국시리즈"), dict(icon='bat', label="야수", at=3), dict(icon='bat', label="야수", at=3.2)], [dict(t="한국시리즈 우승", at=0, gold=True)], title="삼성 라이온즈 · 대표팀")
SC['s2'] = STT('이재현', "2026 이재현", [TI("타율", "2할 2푼 2리", 1), TI("홈런", "17", 2, True)], big="2026")
SC['s4'] = STT('김지찬', "2026 김지찬", [TI("타율", "3할 1푼 5리", 1, True), TI("도루", "22", 2)], big="2026")
SC['s4b'] = RK("대표팀 타자 타율", [RR('김지찬', .315 - .25, "3할 1푼 5리", True), RR('김민석', .310 - .25), RR('김도영', .308 - .25), RR('한동희', .306 - .25), RR('안현민', .298 - .25), RR('문현빈', .297 - .25)], note="대표팀 타자 타율 1위", noteAt=1)
SC['s4c'] = FULL("경기/APBC_김지찬_AG_사진", "2023 항저우 · 2026 아시안게임", "9월 아시안게임도 금메달", tagAt=0, capAt=1, name='김지찬')
SC['s5'] = FLD("대표팀 중견수 준비", hi=[dict(pos="중견수", at=2, c=GOLD_, label="중견수 따로 준비")], side=[dict(t="김지찬 · 한국시리즈 중", at=0), dict(t="연습경기에서 따로 준비", at=2, gold=True)])
SC['s6'] = MV('삼성', [PH('이재현'), PH('김지찬')], "한국시리즈 우승", "한국시리즈 마치고 합류", 1, 2, title="삼성 두 명 합류")
# 두산
SC['d1'] = SL('두산', [dict(icon='ball', label="투수", at=1, xAt=1.3, xLabel="팔꿈치 부상"), dict(icon='bat', label="야수", at=2), dict(icon='bat', label="야수", at=2.2)], title="두산 베어스 · 대표팀")
SC['d2'] = STT('안재석', "2026 안재석", [TI("타율", "2할 7푼 8리", 1), TI("홈런", "11", 2, True), TI("타점", "67", 2)], big="2026")
SC['d3'] = FLD("안재석의 자리", players=[dict(img=CI('안재석'), pos="2루수", **{'from': "3루수"}, at=0, moveAt=1, tag="안재석")], side=[dict(t="소속팀 · 주로 3루", at=0), dict(t="대표팀 · 2루", at=1, gold=True)], chain='d2b')
SC['d4'] = FLD("안재석의 자리", players=[dict(img=CI('안재석'), pos="2루수", at=-1, tag="안재석", tagAt=-1)], side=[dict(t="소속팀 · 주로 3루", at=-1), dict(t="대표팀 · 2루", at=-1, gold=True), dict(t="2루수 후보들 부상", at=1, red=True)], chain='d2b', cont=True)
SC['d5'] = FLD("2루 · 3루수 둘이 번갈아", players=[dict(img=CI('안재석'), pos="2루수", at=-1, tag="안재석", tagAt=-1, outAt=2), dict(img=CI('김휘집'), pos="2루수", **{'from': "3루수"}, at=1, moveAt=2)], side=[dict(t="3루수 둘", at=1), dict(t="2루 번갈아", at=2, gold=True)], chain='d2b', cont=True)
SC['d6'] = STT('김민석', "2026 김민석", [TI("경기", "135", 1), TI("타율", "3할 1푼", 1, True), TI("타점", "57", 2)], big="2026")
SC['d7'] = FLD("상무 연습경기", players=[dict(img=CI('김민석'), pos="중견수", at=0, tag="1번 타자", tagAt=1)], side=[dict(t="1번 타자 · 중견수", at=1, gold=True)])
# 한화
SC['h1'] = TG('한화', new={'조동욱': 1, '허인서': 1.3, '문현빈': 1.6}, text="세 명", textAt=2)
SC['h2'] = RK("대표팀 포수 둘 · 홈런", [RR('허인서', 20, "20홈런", True, at=0), RR('조형우', 8, at=0)], bw=900, note="타율 2할 8푼 3리 · 79타점", noteAt=1)
SC['h2']['rows'][0]['labAt'] = 2; SC['h2']['note2'] = None
SC['h3'] = STT('문현빈', "2026 문현빈", [TI("타율", "2할 9푼 7리", 1), TI("홈런", "15", 2), TI("타점", "76", 2, True)], big="2026", img="경기/APBC_문현빈_한화_사진")
SC['h5'] = FLD("연습경기 문현빈", players=[dict(img=CI('문현빈'), pos="우익수", at=1, tag="문현빈")], side=[dict(t="우익수 출전", at=1, gold=True), dict(t="KT 외야수 합류 늦어질까 대비", at=2, fs=40)])
SC['h6'] = RK("대표팀 투수 · 경기 수", [RR('조동욱', 75, "75경기", True), RR('우강훈', 68), RR('박정민', 63), RR('최준용', 61), RR('성영탁', 60), RR('김영우', 51)], note="10홀드 · 대표팀 투수 최다 경기", noteAt=1)
# NC
SC['n1'] = SL('NC', [dict(icon='ball', label="투수", at=1, xAt=1.3, xLabel="부상"), dict(img=CI('이준혁'), label="이준혁", at=2), dict(img=CI('김휘집'), label="김휘집", at=2.3), dict(img=CI('김주원'), label="김주원", at=2.6)], title="NC 다이노스 · 대표팀")
SC['n2'] = STT('김주원', "2026 김주원", [TI("홈런", "18", 1), TI("도루", "30", 1, True), TI("연습경기", "유격수", 3)], big="2026", img="경기/APBC_김주원_NC_사진")
SC['n3'] = FULL(PH('김주원'), "2023 APBC 베스트나인", "유격수 김주원", tagAt=0, capAt=1)
SC['n4'] = STT('김휘집', "2026 김휘집", [TI("경기", "90", 1), TI("홈런", "14", 1, True), TI("타점", "64", 2)], big="2026")
SC['n4b'] = FLD("울산전 김휘집", players=[dict(img=PH('김휘집'), pos="2루수", at=0, tag="김휘집")], range=dict(pos="2루수", at=2), side=[dict(t="익숙하지 않은 2루", at=1), dict(t="넓은 수비 범위", at=2, gold=True)])
SC['n6'] = RK("대표팀 투수 평균자책점", [RR('이준혁', 2.78, "2.78", True), RR('성영탁', 3.47), RR('김민준', 3.56), RR('박정민', 3.66), RR('최준용', 3.71), RR('박시원', 3.79)], inv=True, invPad=.6, note="대표팀 투수 중 가장 낮음", noteAt=2)
# LG
SC['l1'] = TG('LG', new={'김영우': 1, '박시원': 1, '우강훈': 1, '문정빈': 2}, text="투수 세 명 · 내야수 한 명", textAt=2, size=50)
SC['l2'] = STT('문정빈', "2026 문정빈", [TI("경기", "91", 1), TI("홈런", "19", 1, True), TI("타점", "66", 2), TI("상무전", "1루수", 4)], big="2026")
SC['l3'] = INN("LG 투수 셋 · 상무전", [G9(7, 7, "박시원", 5, c=BLUE_, img=CI('박시원'), imgAt=3), G9(8, 8, "김영우", 5.4, c=GOLD_, img=CI('김영우'), imgAt=2), G9(1, 1, "우강훈", 50, img=CI('우강훈'), imgAt=1)], text="7 · 8회 무실점", textAt=6, sw=150)
SC['l6'] = RB("LG 대표팀 인원", [dict(BAR("2023년", 0, 1), valAt=1), dict(BAR("이번", 4, 2, hi=True), valAt=2)], 4, bw=260, gap=200)
# SSG
SC['g1'] = TG('SSG', new={'김민준': 1, '이로운': 1, '김건우': 1, '조형우': 2}, text="투수 세 명 · 포수 한 명", textAt=2, size=50)
SC['g2'] = STT('김민준', "2026 김민준", [TI("출생", "2006년생", 0), TI("승패", "9승 3패", 1, True), TI("평균자책점", "3.56", 2), TI("상무전", "선발", 4)], big="2026", img="경기/APBC_김민준_투구_사진")
SC['g3'] = RK("SSG 선발 · 승수", [RR('김건우', 9, "9승", True, at=0), RR('이로운', 8, "8승", True, at=2, c=BLUE_)], max=10, bw=860, note="김건우 130이닝+", noteAt=1)
SC['g4'] = FLD("포수 조형우", players=[dict(img=CI('조형우'), pos="포수", at=0, tag="조형우", outAt=3), dict(img=CI('허인서'), pos="포수", at=3)], side=[dict(t="타율 2할 6푼 8리 · 8홈런", at=1), dict(t="연습경기 · 포수 둘이 번갈아", at=3, gold=True)])
# 롯데
SC['r1'] = TG('롯데', new={'한동희': 1, '최준용': 1, '박정민': 1, '김진욱': 1}, text="와일드카드 두 명 포함 네 명", textAt=1, size=50)
SC['r2'] = STT('한동희', "2026 한동희", [TI("타율", "3할 6리", 1), TI("홈런", "25", 2, True), TI("타점", "81", 2)], big="2026")
SC['r2b'] = CLIP("한동희홈런", "한동희 · 2026 시즌 홈런", [TI("2026년", "25홈런", -1), TI("대표팀 타자 중", "홈런 2위", 1, True)], clipCuts=[[0.3, 2.7], [8.0, 9.85]])
SC['r3'] = AX("대표팀 28명 · 나이", list(BY), '한동희', hiAt=0, labels=[dict(y=1999, t="1999년생", at=0)], notes=[dict(t="대표팀 최고참", at=1, gold=True), dict(t="상무전 4번 타자 · 3루수", at=3)])
SC['r4'] = INN("롯데 투수 · 자리", [G9(1, 6, "선발 후보 김진욱", 1, img=CI('김진욱'), imgAt=1), G9(9, 9, "마무리 다툼", 4, c=GOLD_, imgs=[CI('최준용'), CI('박정민')], imgAt=[3, 3.3])], text="김진욱 2026년 144이닝", textAt=1.5, size=50)
# 기아
SC['k1'] = SL('KIA', [dict(icon='ball', label="투수", at=1, xAt=2, xLabel="허벅지 부상"), dict(icon='person', label="네 명", at=3)], title="기아 타이거즈 · 대표팀")
SC['k2'] = FULL("경기/김도영_45호_1012_KIA제공", "2024년 MVP", "김도영", tagAt=1, capAt=1, name='김도영')
SC['k2b'] = S(0, "apbc_hist", title="2026년 김도영의 태극마크", nodes=[dict(y="3월", sub="WBC", flag="한국", at=1), dict(y="9월", sub="아시안게임", flag="한국", at=1.3), dict(y="11월", sub="APBC · 세 번째", flag="한국", at=2, hi=True)],
              walker=dict(img=CI('김도영'), at=0, path=[dict(at=1), dict(at=1.5), dict(at=2)]), bg=BG_KOR)
SC['k3'] = CLIP("김도영홈런", "김도영 · 2026 시즌 홈런", [TI("타율", "3할 8리", 1), TI("홈런", "45", 2, True), TI("타점", "118", 2, True)], clipCuts=[[0.8, 9.08]])
SC['k3b'] = CLIP("김도영홈런", "김도영 · 2026 시즌 홈런", [TI("타율", "3할 8리", -1), TI("홈런", "45", -1, True), TI("타점", "118", -1, True), TI("대표팀 타자 중", "홈런 · 타점 1위", 0, True)], clipCuts=[[0.8, 9.08]], cont=True)
SC['k5'] = STT('박재현', "2026 박재현", [TI("출생", "2006년생", 0), TI("홈런", "19", 1), TI("도루", "21", 1, True), TI("대표팀", "중견수 후보", 3)], big="2026")
SC['k5b'] = AX("대표팀 야수 14명 · 나이", BAT14, '박재현', hiAt=0, labels=[dict(y=2006, t="2006년생", at=0)], notes=[dict(t="야수 중 가장 어림", at=2, gold=True)])
SC['k6'] = INN("기아 투수 · 자리", [G9(4, 6, "스윙맨 후보 김태형", 3, c=BLUE_, img=CI('김태형'), imgAt=2), G9(9, 9, "13세이브 성영탁", 1, c=GOLD_, img=CI('성영탁'), imgAt=1)])
# 상대 팀
SC['q1'] = MUK("한국", "호주", "vs", "2023년에도 첫 경기", "첫 상대")
SC['q2'] = CLIP("호주전", "2023 APBC 첫 경기 호주전", [TI("연장", "10회 말", 0), TI("결승타", "끝내기 안타", 1), TI("최종", "3 : 2 승", 2, True)])
SC['q2b'] = CLIP("호주전", "2023 APBC 첫 경기 호주전", [TI("그해 3월 WBC", "호주에 패", 1), TI("그해 APBC", "끝내기로 설욕", 2, True)], cont=True)
SC['q5'] = S(0, "fork", title="결승 가는 길", left=dict(label="호주 · 대만 모두 승", sub="일본에 져도 결승 보임"), right=dict(label="첫 경기 호주전 패", sub="일본전 부담 커짐", bad=True), pick='left', bg=BG_KOR, chain='fk')
SC['q5b'] = S(0, "fork", title="결승 가는 길", left=dict(label="호주 · 대만 모두 승", sub="일본에 져도 결승 보임"), right=dict(label="첫 경기 호주전 패", sub="일본전 부담 커짐", bad=True), pick='right', bg=BG_KOR, chain='fk', cont=True)
SC['e2c'] = MUK("한국", "일본", "vs", "한국 응원석 약 3천 석 · 앰프 응원", "한일전", size=64)
SC['e2d'] = dict(MUK("한국", "일본", "vs", "대회 전 경기 · 티빙 생중계", "한일전", size=64), cont=True)
SC['j5'] = dict(MUK("한국", "일본", "vs", "일본 3연패 도전", "한일전", size=64), cont=True)
SC['j6'] = S(0, "apbc_games", title="APBC 한일전", tiles=[dict(y="2017", stage="조별리그", a=7, b=8, res='L', note="연장 10회", at=0.5, hi=True), dict(y="2017", stage="결승", a=0, b=7, res='L', at=50), dict(y="2023", stage="조별리그", a=1, b=2, res='L', at=2.5, hi=True), dict(y="2023", stage="결승", a=3, b=4, res='L', note="연장", at=50, hi=True)], bg=BG_KOR, chain='jg')
SC['j6b'] = S(0, "apbc_games", title="APBC 한일전", tiles=[dict(y="2017", stage="조별리그", a=7, b=8, res='L', note="연장 10회", at=-1, keep=True, hi=True), dict(y="2017", stage="결승", a=0, b=7, res='L', at=0), dict(y="2023", stage="조별리그", a=1, b=2, res='L', at=-1, keep=True, hi=True), dict(y="2023", stage="결승", a=3, b=4, res='L', note="연장", at=0, hi=True)], hiAt=1.5, hiLabel="1점 차", bg=BG_KOR, chain='jg', cont=True)
SC['j7'] = S(0, "apbc_games", title="9월 아시안게임 한일전", tiles=[dict(y="조별", stage="9월 아시안게임", a=0, b=5, res='L', at=1), dict(y="결승", stage="9월 아시안게임", a=3, b=1, res='W', at=2)], bg=BG_KOR)
SC['j7b'] = CELLS("그때 일본 · 이번 일본", [C("9월 아시안게임\n사회인 선수", 1), C("이번 APBC\n프로 유망주", 2, hi=True)], 2, cw=440, ch=170, fs=46)
SC['j7c'] = S(0, "wdl", title="프로끼리 한일전 · 2015 프리미어12 이후", rows=[dict(team="한국", w=0, d=1, l=11, at=2, tag="한 번도 못 이김", tagAt=3)], bg=BG_KOR)
SC['j8'] = FLD("연습경기 · 낯선 자리", hi=[dict(pos="2루수", at=1), dict(pos="중견수", at=1.3), dict(pos="우익수", at=1.6)], side=[dict(t="2루 · 중견수 · 우익수", at=1), dict(t="낯선 선수들이 맡음", at=2, gold=True)])
SC['j8b'] = MUK("한국", "상무", "8 : 4", "6일 연습경기 승리", "연습경기", chain="pr")
SC['j8c'] = SAY(dict(S(0, "facegrid", title="상무전", items=[dict(img="경기/APBC_김도영_상무전_카드", name="김도영", team="KIA", at=0), dict(img="경기/APBC_허인서_상무전_카드", name="허인서", team="한화", at=2)], cols=2), bg=BG_KOR), {'김도영': ('지명타자 · 홈런 두 개', 1), '허인서': ('역전 3점 홈런', 3)})
SC['j8e'] = dict(GRID("최원호 감독", ['최원호'], at=0, cols=1), bg=BG_KOR, items=[IT('최원호', 0, say="의외로 괜찮았다", sayAt=4)])
SC['j8d'] = MUK("한국", "울산 웨일즈", "11 : 1", "7일 연습경기 승리", "연습경기")
SC['j8f'] = INN("울산전 마운드", [G9(1, 2, "김진욱", 0, c=BLUE_, img="경기/김진욱_1011_롯데제공", imgAt=0), G9(3, 4, "이로운", 1, c=GOLD_, img="경기/APBC_이로운_투구_카드", imgAt=1)], text="둘 다 2이닝 무실점", textAt=2)
# 분석
SC['a0'] = MUK("한국", "일본", "?", "이 명단으로 일본을 어떻게 잡을까", "분석", size=64)
SC['a1'] = S(0, "apbc_rot", title="선발 로테이션 · 4일 연속", days=[dict(label="12일", flag="호주"), dict(label="13일", flag="일본"), dict(label="14일", flag="대만"), dict(label="15일 결승")], text="하루씩 다른 선발 네 명", textAt=2, bg=BG_KOR, chain='rot')
SC['a2'] = S(0, "apbc_rot", title="선발 로테이션 · 4일 연속", days=[dict(label="12일", flag="호주", img=CI('김진욱'), at=0, tags=[dict(t="100이닝+", at=4)]), dict(label="13일", flag="일본", img=CI('이로운'), at=0.4), dict(label="14일", flag="대만", img=CI('김건우'), at=1, tags=[dict(t="100이닝+", at=4.3), dict(t="평균자책점 6점대", at=6, red=True)]), dict(label="15일 결승", img=CI('김민준'), at=1.4)],
             bg=BG_KOR, chain='rot', cont=True)
SC['a3'] = RB("2026년 100이닝 넘긴 선발 후보", [dict(BAR("한국", 2, 0), valAt=0), dict(BAR("일본", 4, 0, hi=True, txt="4명 · 모두 120이닝+"), valAt=0)], 4, bw=260, gap=200, chain='a3')
SC['a3b'] = KEEP(SC['a3'], title="시즌 내내 버틴 선발 · 두 배 차이")
SC['a4'] = INN("한국 마운드 운용 · 제 생각", [G9(1, 3, "선발 3이닝이면 성공", 1, c="#FFFFFF"), G9(4, 6, "진짜 승부 · 스윙맨", 3, c=BLUE_), G9(7, 9, "필승조", 4, c=GOLD_)])
SC['a4c'] = INN("연습경기 두 번 · 선발 후보 넷", rows=[dict(label="상무전", groups=[G9(1, 2, "선발 후보", 1, c="#FFFFFF"), G9(3, 4, "선발 후보", 1.5, c=BLUE_)]), dict(label="울산전", groups=[G9(1, 2, "선발 후보", 1.2, c="#FFFFFF"), G9(3, 4, "선발 후보", 1.7, c=BLUE_)])], text="2이닝씩 나눠 던짐", textAt=2)
SC['a4b'] = CELLS("필승조는 어디에", [C("12일\n호주전", 0), C("13일\n일본전", 1, hi=True), C("14일\n대만전", 1.3, hi=True), C("15일\n결승", 0)], 4, cw=250, ch=160, fs=42, text="필승조 · 일본전과 대만전에 몰아 씀", textAt=1.5, size=52)
SC['a5'] = SAY(dict(GRID("마무리 후보", ['최준용', '박정민'], at={'최준용': 3, '박정민': 4}, cols=2), bg=BG_KOR, items=[IT('최준용', 3, img="경기/APBC_최준용_원정_카드"), IT('박정민', 4)], text="감독: 경험·기록 보고 한 명", textAt=1, size=50), {'최준용': ('15세이브', 3), '박정민': ('14홀드', 4)})
SC['a5b'] = KEEP(SC['a5'], text="저라면 마무리는 최준용", textAt=3)
for _it in SC['a5b']['items']:
    if _it.get('name') == '최준용': _it['say'], _it['sayAt'] = '2023 APBC · 9월 아시안게임', 1.5
SC['a6'] = CELLS("빠진 왼손 불펜", [C("왼손 불펜\n부상 이탈", 1, bad=True), C("왼손 불펜\n한국시리즈", 1, bad=True)], 2, cw=420, ch=160, fs=46, text="대신: 좌타자에게 강했던 투수", textAt=3, size=56)
SC['a7'] = S(0, "apbc_lineup", title="타선의 열쇠", slots=[dict(label="앞 타자", dash=True), dict(label="김도영"), dict(label="뒤 타자", q=True, hiAt=2)], people=[dict(img=CI('김도영'), slot=1, at=1)], chips=[dict(t="김도영 뒤에 누가 서느냐", at=2, gold=True)], bg=BG_KOR)
SC['a8'] = FULL("경기/김도영_45호_타격_1012_KIA제공", "감독이 본 일본", '"계속 유인구만 던질 것이다"', tagAt=0, capAt=1, name='김도영')
SC['a9'] = S(0, "apbc_zone", title="울산전 김도영", who="경기/김도영_세리머니_1017_KIA제공", whoLabel="김도영", ks=4, ksAt=1, balls=[dict(x=1.32, y=-.12, at=3, t="첫 타석"), dict(x=1.28, y=.08, at=3.4, t="둘째 타석")], side=[dict(t="네 타석 연속 삼진", at=1, red=True), dict(t="첫 두 타석 · 존 밖 공에 헛스윙", at=3)], bg=BG_KOR, chain='zone')
SC['a9b'] = S(0, "apbc_zone", title="울산전 김도영", who="경기/김도영_세리머니_1017_KIA제공", whoLabel="김도영", ks=4, ksAt=-1, balls=[dict(x=1.32, y=-.12, at=-1, t="첫 타석"), dict(x=1.28, y=.08, at=-1, t="둘째 타석")], outAt=0.5, side=[dict(t="네 타석 연속 삼진", at=-1, red=True), dict(t="첫 두 타석 · 존 밖 공에 헛스윙", at=-1), dict(t="일본이 노릴 곳", at=0.5, gold=True)], bg=BG_KOR, chain='zone', cont=True)
SL3 = [dict(label="앞 타자", dash=True), dict(label="김도영"), dict(label="뒤 타자 · 4번", q=True)]
SC['a10'] = S(0, "apbc_lineup", title="김도영 뒤 · 연습경기 4번 타자", slots=SL3, people=[dict(img="경기/김도영_43호_타격_KIA제공", slot=1, at=0), dict(img="경기/한동희_타격_0918_롯데제공", slot=2, at=1, outAt=1.8), dict(img="경기/문정빈_타격_LG제공", slot=2, at=1.8)], chips=[dict(t="한동희 · 문정빈 나눠 맡음", at=2)], bg=BG_KOR, chain='lu')
SC['a11'] = S(0, "apbc_lineup", title="김도영 뒤 타자 조건", slots=SL3, people=[dict(img="경기/김도영_43호_타격_KIA제공", slot=1, at=-1)], chips=[dict(t="선구안", at=2, gold=True), dict(t="컨택", at=2.3, gold=True), dict(t="어느 정도 파워", at=3, gold=True)], bg=BG_KOR, chain='lu', cont=True)
SC['a11b'] = S(0, "apbc_lineup", title="조건에 가장 가까운 타자", slots=SL3, people=[dict(img="경기/김도영_43호_타격_KIA제공", slot=1, at=-1), dict(img=CI('안현민'), slot=2, at=1)], chips=[dict(t="안현민", at=1, gold=True), dict(t="2년 연속 출루율 4할", at=2)], bg=BG_KOR, chain='lu', cont=True)
SC['a12'] = S(0, "apbc_lineup", title="안현민 · 앞이냐 뒤냐", slots=SL3, people=[dict(img="경기/김도영_43호_타격_KIA제공", slot=1, at=-1), dict(img=CI('안현민'), slot=2, at=-1, moves=[dict(to=0, at=0.5), dict(to=2, at=3)])], chips=[dict(t="감독 · 앞에 두는 것도 고민", at=1), dict(t="제 생각 · 김도영 뒤", at=4, gold=True)], bg=BG_KOR, chain='lu', cont=True)
SC['a13'] = CELLS("일본 와일드카드 세 자리", [C("와일드카드\n홈런 타자", 4, hi=True), C("와일드카드\n홈런 타자", 4, hi=True), C("와일드카드", 2)], 3, cw=330, ch=170, fs=44, text="장타를 칠 수 있는 선수", textAt=1, size=56)
SC['a14'] = SAY(dict(GRID("일본 경계 타자", ['마사키 도모야', '야마구치 고키'], cols=2), bg=BG_KOR, items=[dict(img="경기/JPN_마사키_카드", name="마사키 도모야", team="", at=1), dict(img="경기/JPN_야마구치_카드", name="야마구치 고키", team="", at=4)]), {'마사키 도모야': ('1번 · 28홈런 · 일본시리즈 MVP', 2), '야마구치 고키': ('4번 후보 · 38홈런', 5)})
SC['a15'] = STT('야마구치 고키', "야마구치 고키", [TI("경기", "113", 1), TI("삼진", "107개", 2, True)], img="경기/JPN_야마구치")
SC['a15b'] = STT('야마구치 고키', "야마구치 고키", [TI("경기", "113", -1), TI("삼진", "107개", -1, True), TI("한국의 수", "유인구 승부", 2, True)], img="경기/JPN_야마구치", cont=True)
SC['a16'] = STT('다카하시 히로토', "일본 에이스", [TI("일본 언론 보도", "13일 한국전 대신", 2), TI("유력", "결승 선발", 3, True)], img="경기/JPN_다카하시")
SC['a16b'] = S(0, "apbc_sched", title="결승에 가면", phase='final', l2="15일 결승", fAt2=0, fImg="경기/JPN_다카하시_카드", fImgAt=1, fCap="결국 다카하시와 대결", fCapAt=1, dimLines=True, bg=BG_KOR)
SC['a17'] = CELLS("일본 대표팀 28명", [C("", 0, hi=True) for _ in range(23)] + [C("", 0) for _ in range(5)], 14, cw=70, ch=70, label="23명이 첫 대표팀")
SC['a17b'] = CELLS("한국 대표팀 28명", [C("", 0, hi=True, c="#D9A21B") for _ in range(11)] + [C("", 0) for _ in range(17)], 14, cw=70, ch=70, label="9월 아시안게임 금메달 멤버 11명")
SC['a17c'] = MUK("한국", "일본", "vs", "사회인 상대지만 · 결승 압박을 이겨 본 경험", "경험", size=58)
SC['a18'] = CELLS("제가 보는 일본 잡는 법", [C("선발\n짧게", 1), C("4회부터\n물량 계투", 2), C("뒤 타순까지\n두껍게", 3), C("유인구\n돌려주기", 4, hi=True)], 4, cw=250, ch=170, fs=40)
SC['e3'] = MUK("한국", "일본", "?", "한국 설욕? 아니면 일본?", "2026 APBC", size=80)
# ── v7 보정 ──
SC['l3'] = SAY(dict(GRID("LG 투수 셋", ['우강훈', '김영우', '박시원'], at={'우강훈': 1, '김영우': 2, '박시원': 3}, cols=3), bg=BG_KOR), {'우강훈': ('20홀드', 1), '김영우': ('아시안게임 금메달', 2), '박시원': ('2006년생', 3)})
SC['l3']['text'] = "박시원 · 김영우 상무전 7 · 8회 무실점"; SC['l3']['textAt'] = 5.5; SC['l3']['size'] = 48
SC['a1'] = S(0, "apbc_rot", title="선발 로테이션 · 4일 연속", days=[dict(label="첫째 날"), dict(label="둘째 날"), dict(label="셋째 날"), dict(label="넷째 날")], text="하루씩 다른 선발 네 명", textAt=2, bg=BG_KOR, chain='rot')
SC['a2'] = S(0, "apbc_rot", title="선발 후보 네 명", days=[dict(label="김진욱", img=CI('김진욱'), at=0, tags=[dict(t="100이닝+", at=4)]), dict(label="이로운", img=CI('이로운'), at=0.4), dict(label="김건우", img=CI('김건우'), at=1, tags=[dict(t="100이닝+", at=4.3), dict(t="평균자책점 6점대", at=6, red=True)]), dict(label="김민준", img=CI('김민준'), at=1.4)], bg=BG_KOR, chain='rot', cont=True)
SC['a10']['people'][1]['outAt'] = 1.5; SC['a10']['people'][2]['at'] = 1.5
SC['a12']['people'][1]['moves'] = [dict(to=0, at=1), dict(to=2, at=4)]; SC['a12']['chips'] = [dict(t="감독 · 앞에 두는 것도 고민", at=1), dict(t="제 생각 · 김도영 뒤", at=4, gold=True)]
SC['a14'] = SAY(dict(GRID("일본 경계 타자", ['마사키 도모야', '야마구치 고키'], cols=2), bg=BG_KOR, items=[dict(img="경기/JPN_마사키_카드", name="마사키 도모야", team="", at=1), dict(img="경기/JPN_야마구치_카드", name="야마구치 고키", team="", at=4)]), {'마사키 도모야': ('1번 · 28홈런 · 일본시리즈 MVP', 3), '야마구치 고키': ('4번 후보 · 38홈런', 5)})
for _tt in SC['j6']['tiles']: _tt['hi'] = False
SC['j6']['tiles'][0]['at'] = 0.7; SC['j6']['tiles'][2]['at'] = 2.7
SC['j7']['tiles'][0]['y'] = "슈퍼라운드"
SC['j7c'] = CELLS("프로끼리 한일전 · 2015 프리미어12 이후", [C("무", 2)] + [C("패", 2, bad=True) for _ in range(11)], 12, cw=88, ch=88, fs=34, text="1무 11패", textAt=2, size=72)
SC['s5'] = FLD("대표팀 중견수 준비", players=[dict(img=CI('김지찬'), pos="중견수", at=0, outAt=1.5, tag="김지찬 · 한국시리즈")], hi=[dict(pos="중견수", at=2, c=GOLD_, label="중견수 따로 준비")], side=[dict(t="김지찬 · 한국시리즈 중", at=0), dict(t="연습경기에서 따로 준비", at=2, gold=True)])
SC['h2']['rows'][1]['at'] = 3; SC['h2']['noteAt'] = 2; SC['h2']['note'] = "타율 2할 8푼 3리 · 79타점"; SC['h2']['rows'][0]['labAt'] = 2
SC['h2']['notes'] = None
SC['h6']['rows'][0]['labAt'] = 1; SC['h6']['noteAt'] = 2.5
SC['n6']['rows'][0]['labAt'] = 1; SC['n6']['noteAt'] = 3
SC['g3']['rows'][0]['labAt'] = 1; SC['g3']['rows'][1]['labAt'] = 3
SC['k1'] = SL('KIA', [dict(icon='ball', label="투수", at=1, xAt=2, xLabel="허벅지 부상"), dict(icon='ball', label="투수", at=3), dict(icon='ball', label="투수", at=3.2), dict(icon='bat', label="내야수", at=3.4), dict(icon='bat', label="외야수", at=3.6)], title="기아 타이거즈 · 대표팀")
SC['k6']['groups'][0]['at'] = 4
SC['l1'] = TG('LG', new={'문정빈': 2}, text="투수 세 명 · 내야수 한 명", textAt=1, size=50)   # 투수 얼굴은 l3 에서 처음(같은 단락 재등장 ✗)
# ── v7 보정 2 ──
SC['o8']['out'][0]['label'] = "부상 세 명"; SC['o8']['out'][1]['label'] = "한국시리즈 두 명"
SC['t2'] = STT('안현민', "2026 안현민", [TI("부상", "두 달 쉼", 1.5), TI("경기", "94", 3), TI("홈런", "14", 4, True), TI("타율", "2할 9푼 8리", 5)], big="2026")
SC['s4c'] = FULL("경기/APBC_김지찬_AG_사진", "2023 항저우 · 2026 아시안게임", "9월 아시안게임도 금메달", tagAt=0, capAt=1)
SC['l3']['textAt'] = 5
SC['r3']['title'] = "대표팀 나이 순"; SC['k5b']['title'] = "대표팀 야수 · 나이 순"
SC['k2'] = FULL("경기/김도영_45호_1012_KIA제공", "2024년 MVP", "김도영", tagAt=0, capAt=0, name='김도영')
SC['a4b'] = CELLS("필승조는 어디에", [C("호주전", 0), C("일본전", 1, hi=True), C("대만전", 1.3, hi=True), C("결승", 0)], 4, cw=250, ch=160, fs=46, text="필승조 · 일본전과 대만전에 몰아 씀", textAt=1.5, size=52)
SC['h1']['textAt'] = 1.5
SC['a4c']['textAt'] = 1.6
SC['a5'] = SAY(dict(GRID("마무리 후보", ['최준용', '박정민'], at={'최준용': 1, '박정민': 1}, cols=2), bg=BG_KOR, items=[IT('최준용', 1, img="경기/APBC_최준용_원정_카드"), IT('박정민', 1.2)], text="감독: 경험·기록 보고 한 명", textAt=2, size=50), {'최준용': ('15세이브', 4), '박정민': ('14홀드', 5)})
SC['a5b'] = KEEP(SC['a5'], text="저라면 마무리는 최준용", textAt=3)
for _it in SC['a5b']['items']:
    if _it.get('name') == '최준용': _it['say'], _it['sayAt'] = '2023 APBC · 9월 아시안게임', 1.5
for _c in SC['a13']['items'][:2]: _c['at'] = 3
SC['l1'] = SL('LG', [dict(icon='ball', label="투수", at=1), dict(icon='ball', label="투수", at=1.2), dict(icon='ball', label="투수", at=1.4), dict(img=CI('문정빈'), label="문정빈", at=2)], title="LG 트윈스 · 대표팀")
# 인포그래픽 얼굴 → precheck 용 이름·호흡(_ppl): 대사에서 이름을 말하는 사람만
import re as _re
def _nm(img):
    b = img.split('/')[-1]; m = _re.match(r'(?:APBC_|JPN_)?([가-힣]{2,4})(?:_|$)', b); n = m.group(1) if m else None
    return {'마사키': '마사키 도모야', '야마구치': '야마구치 고키', '다카하시': '다카하시 히로토'}.get(n, n)
def _ppl(sc):
    t = sc.get('type', ''); out = {}
    def add(img, at):
        n = _nm(img or '')
        if n: out.setdefault(n, -1 if (at is not None and at < 0) else (at or 0))
    if t == 'apbc_hist':
        c = sc.get('carry')
        if c: [add(im, (c.get('ats') or [c.get('at', 0)] * 9)[i]) for i, im in enumerate(c['imgs'])]
        if sc.get('walker'): add(sc['walker']['img'], sc['walker'].get('at', 0))
    for q in sc.get('players', []) if t == 'apbc_field' else []: add(q['img'], q.get('at', 0))
    for g in (sc.get('groups') or []) + sum([r.get('groups', []) for r in sc.get('rows', []) if isinstance(r, dict) and 'groups' in r], []) if t == 'apbc_innings' else []:
        ims = g.get('imgs') or ([g['img']] if g.get('img') else []); ia = g.get('imgAt')
        for i, im in enumerate(ims): add(im, ia[i] if isinstance(ia, list) else (ia if ia is not None else g.get('at', 0)))
    for r in sc.get('rows', []) if t == 'apbc_rank' else []: add(r['img'], r.get('at', 0))
    for q in sc.get('people', []) if t in ('apbc_ages', 'apbc_lineup') else []:
        if t == 'apbc_ages' and not q.get('hi'): continue
        add(q['img'], q.get('at', 0))
    for d in sc.get('days', []) if t == 'apbc_rot' else []:
        if d.get('img'): add(d['img'], d.get('at', 0))
    if t == 'apbc_move': [add(im, sc.get('at', 0)) for im in sc.get('imgs', [])]
    if t == 'apbc_zone' and sc.get('who'): add(sc['who'], -1 if sc.get('cont') else 0)
    for f in sc.get('faces', []) if t == 'apbc_wild' else []: add(f['img'], f.get('at', 0))
    for q in sc.get('slots', []) if t == 'apbc_slots' else []:
        if q.get('img'): add(q['img'], q.get('at', 0))
    if t == 'apbc_sched' and sc.get('fImg'): add(sc['fImg'], sc.get('fImgAt', 0))
    return out
_TXT = {k: v for k, v, _ in __import__('importlib').import_module('lines_apbc').L} if False else None
for _k, _sc in SC.items():
    if str(_sc.get('type', '')).startswith('apbc_'):
        _p = _ppl(_sc)
        if _p: _sc['_ppl'] = _p
# ── v7 보정 3: 이름을 말하지 않는 사람은 얼굴 대신 구단 로고 ──
for _k in ('s4b', 'h2', 'h6', 'n6'):
    for _r in SC[_k]['rows']:
        if not _r.get('hi'): _r['logo'] = TEAMOF.get(_nm(_r['img']), '')
for _k in ('r3', 'k5b'):
    for _q in SC[_k]['people']:
        if not _q.get('hi'): _q['logo'] = TEAMOF.get(_nm(_q['img']), '')
SC['o4b']['faces'] = [dict(img=None, team='롯데', at=1), dict(img=None, team='롯데', at=1.2), dict(img=None, team='삼성', at=1.5)]
SC['s6']['at'] = 0
SC['d5']['players'][1]['at'] = 1; SC['d5']['players'][1]['moveAt'] = 3; SC['d5']['players'][0]['outAt'] = 3; SC['d5']['side'] = [dict(t="3루수 둘", at=2), dict(t="2루 번갈아", at=3, gold=True)]
SC['g4']['players'][0]['outAt'] = 3; SC['g4']['players'][1]['at'] = 3; SC['g4']['side'] = [dict(t="타율 2할 6푼 8리 · 8홈런", at=1), dict(t="연습경기 · 허인서와 번갈아", at=3, gold=True)]
for _b in SC['a9']['balls']: _b['at'] += 1
SC['a9']['ksAt'] = 2; SC['a9']['side'] = [dict(t="네 타석 연속 삼진", at=2, red=True), dict(t="첫 두 타석 · 존 밖 공에 헛스윙", at=4)]
SC['j8c'] = SAY(dict(GRID("상무전", ['김도영', '허인서'], at={'김도영': 0, '허인서': 2}, cols=2), bg=BG_KOR), {'김도영': ('지명타자 · 홈런 두 개', 1), '허인서': ('역전 3점 홈런', 3)})
_LT = {}
try:
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location('_lines', '/home/claude/apbc/lines_apbc.py'); _lm = _iu.module_from_spec(_sp); _sp.loader.exec_module(_lm); _LT = {k: v for k, v, _ in _lm.L}
except Exception: pass
for _k, _sc in SC.items():
    if str(_sc.get('type', '')).startswith('apbc_'):
        _p = {n: a for n, a in _ppl(_sc).items() if n and n in _LT.get(_k, '')}
        if _p: _sc['_ppl'] = _p
        else: _sc.pop('_ppl', None)
SC['s4c']['tagAt'] = 1; SC['s4c']['capAt'] = 2
for _k in ('s4b', 'h2', 'h6', 'n6'):
    for _r in SC[_k]['rows']:
        if not _r.get('hi'): _r['anon'] = True; _r.pop('logo', None)
SC['o4b']['faces'] = [dict(img=CI('한동희'), team='롯데', at=1), dict(img=CI('최준용'), team='롯데', at=1.4), dict(img=CI('김지찬'), team='삼성', at=2)]
SC['o4b']['badgeAt'] = 4
for _k, _sc in SC.items():
    if str(_sc.get('type', '')).startswith('apbc_'):
        _p = {n: a for n, a in _ppl(_sc).items() if n and n in _LT.get(_k, '')}
        if _p: _sc['_ppl'] = _p
        else: _sc.pop('_ppl', None)
# ── v7 반론 댓글 반영 ──
SC['d5'] = FLD("2루 · 3루수 둘을 시험", players=[dict(img=CI('안재석'), pos="2루수", at=-1, tag="안재석", tagAt=-1, outAt=2), dict(img=CI('김휘집'), pos="2루수", **{'from': "3루수"}, at=1, moveAt=2, tag="김휘집", tagAt=2)], side=[dict(t="2루에 세워 보고", at=2), dict(t="한 명 선택", at=3, gold=True)], chain='d2b', cont=True)
SC['j7c'] = CELLS("프로끼리 한일전 · 2015 프리미어12 4강 이후", [C("무", 2)] + [C("패", 2, bad=True) for _ in range(11)], 12, cw=88, ch=88, fs=34, text="1무 11패", textAt=2, size=72)
SC['a16b']['fCap'] = "다카하시와 만날 가능성 큼"
SC['a13'] = CELLS("일본 감독이 강조한 것", [C("장타", 1, hi=True, icon='bat')], 1, cw=460, ch=220, fs=84)
SL3 = [dict(label="앞 타자", dash=True), dict(label="김도영 · 3번 전망"), dict(label="4번", q=True)]
SC['a10'] = S(0, "apbc_lineup", title="김도영 뒤 · 4번 타자", slots=SL3, people=[dict(img="경기/김도영_43호_타격_KIA제공", slot=1, at=0), dict(img="경기/한동희_타격_0918_롯데제공", slot=2, at=3, outAt=3.5), dict(img="경기/문정빈_타격_LG제공", slot=2, at=3.5)], chips=[dict(t="본선 · 김도영 3번 전망", at=1), dict(t="연습경기 4번 · 한동희 · 문정빈", at=3)], bg=BG_KOR, chain='lu')
SC['a11'] = S(0, "apbc_lineup", title="4번 타자 조건", slots=SL3, people=[dict(img="경기/김도영_43호_타격_KIA제공", slot=1, at=-1)], chips=[dict(t="선구안", at=2, gold=True), dict(t="컨택", at=2.3, gold=True), dict(t="어느 정도 파워", at=3, gold=True)], bg=BG_KOR, chain='lu', cont=True)
SC['a11b'] = S(0, "apbc_lineup", title="제 생각 · 4번엔 안현민", slots=SL3, people=[dict(img="경기/김도영_43호_타격_KIA제공", slot=1, at=-1), dict(img=CI('안현민'), slot=2, at=1)], chips=[dict(t="안현민", at=1, gold=True), dict(t="2년 연속 출루율 4할", at=2), dict(t="2026년 14홈런", at=3)], bg=BG_KOR, chain='lu', cont=True)
SC['a12'] = S(0, "apbc_lineup", title="안현민 · 앞이냐 뒤냐", slots=SL3, people=[dict(img="경기/김도영_43호_타격_KIA제공", slot=1, at=-1), dict(img=CI('안현민'), slot=2, at=-1, moves=[dict(to=0, at=1), dict(to=2, at=2.5)])], chips=[dict(t="감독 · 앞에 두는 것도 고민", at=1), dict(t="제 생각 · 김도영 뒤", at=2.5, gold=True)], bg=BG_KOR, chain='lu', cont=True)
SC['a15'] = STT('야마구치 고키', "야마구치 고키", [TI("경기", "113", 1), TI("삼진", "107개", 2, True), TI("출루율", "3할 2푼 9리", 3)], img="경기/JPN_야마구치")
SC['a15b'] = STT('야마구치 고키', "야마구치 고키", [TI("경기", "113", -1), TI("삼진", "107개", -1, True), TI("출루율", "3할 2푼 9리", -1), TI("한국의 수", "유인구 승부", 2, True)], img="경기/JPN_야마구치", cont=True)
SC['a4c'] = INN("연습경기 두 번 · 선발", rows=[dict(label="상무전", groups=[G9(1, 2, "선발 2이닝", 1, c="#FFFFFF")]), dict(label="울산전", groups=[G9(1, 2, "선발 2이닝", 1.2, c="#FFFFFF")])])
SC['a2']['days'][0]['tags'] = [dict(t="100이닝+", at=3)]; SC['a2']['days'][2]['tags'] = [dict(t="100이닝+", at=3.3), dict(t="평균자책점 6점대", at=5, red=True)]
SC['a18'] = CELLS("제가 보는 일본 잡는 법", [C("선발\n짧게", 0), C("4회부터\n물량 계투", 1), C("중심 뒤\n두껍게", 2), C("유인구엔\n유인구로", 3, hi=True)], 4, cw=250, ch=170, fs=40)
SC['d6'] = STT('김민석', "2026 김민석", [TI("경기", "135", 1), TI("타율", "3할 1푼", 1, True), TI("대표팀 타자 타율", "2위", 3)], big="2026")
SC['l2'] = STT('문정빈', "2026 문정빈", [TI("경기", "91", 1), TI("홈런", "19", 1, True), TI("상무전", "1루수", 3)], big="2026")
SC['n4'] = STT('김휘집', "2026 김휘집", [TI("경기", "90", 1), TI("홈런", "14", 2, True), TI("타점", "64", 2)], big="2026")
SC['s1'] = SL('삼성', [dict(icon='ball', label="투수", at=1, xAt=1.3, xLabel="원칙상 제외"), dict(icon='ball', label="투수", at=1, xAt=1.5, xLabel="원칙상 제외"), dict(icon='bat', label="야수", at=2), dict(icon='bat', label="야수", at=2.2)], [dict(t="한국시리즈 우승", at=0, gold=True)], title="삼성 라이온즈 · 대표팀")
SC['h5']['side'] = [dict(t="우익수 출전", at=1, gold=True), dict(t="한국시리즈 길어질까 대비", at=2.5)]
SC['w2'] = STT('전준표', "2026 전준표", [TI("출생", "2005년생", 0), TI("경기", "21", 1), TI("승리", "없음", 1), TI("평균자책점", "4.29", 2, True)], big="2026")
for _k, _sc in SC.items():
    if str(_sc.get('type', '')).startswith('apbc_'):
        _p = {n: a for n, a in _ppl(_sc).items() if n and n in _LT.get(_k, '')}
        if _p: _sc['_ppl'] = _p
        else: _sc.pop('_ppl', None)
# ── 미리보기 보정 (11/8 밤) ──
SC['d5'] = FLD("2루 · 3루수 둘을 시험", players=[dict(img=CI('안재석'), pos="2루수", at=1, tag="안재석", tagAt=1), dict(img=CI('김휘집'), pos="3루수", at=1.2, tag="김휘집", tagAt=1.2)], side=[dict(t="둘 다 2루 시험", at=2), dict(t="한 명 선택", at=3, gold=True)], chain='d2b', cont=True)
SC['j7c'] = CELLS("프로끼리 한일전 · 2015 프리미어12 4강 이후", [C("무", 2)] + [C("패", 2, bad=True) for _ in range(11)], 6, cw=150, ch=120, fs=56, text="1무 11패", textAt=2, size=80)
for _k, _sc in SC.items():
    if str(_sc.get('type', '')).startswith('apbc_'):
        _p = {n: a for n, a in _ppl(_sc).items() if n and n in _LT.get(_k, '')}
        if _p: _sc['_ppl'] = _p
        else: _sc.pop('_ppl', None)
# ── 11/8 22시 사용자: 첫 장면 선수 사진 빼고 로고+인원수만 · 제목 장면 글자 크기 같게(로고 안 움직이게) ──
_AT = {'LG': 2, 'SSG': 2, '롯데': 3, 'KIA': 3, '한화': 5, 'NC': 5, '삼성': 6, '두산': 6, '키움': 7, 'KT': 7}
SC['o1'] = S(0, "apbc_teams", logoOnly=True, title="APBC 대표팀", teams=[dict(team=t, n=len(ns), at=_AT[t], top=(f == 'top'), low=(f == 'low')) for t, ns, f in R28], bg=BG_KOR)
SC['o1'].pop('_ppl', None)
SC['o2b']['size'] = SC['o2']['size'] if 'o2' in SC else 96
# ── 11/8 22시 텀 관문 17곳(쉼 없이 2.8초 넘게) 대사 고침에 맞춘 장면 호흡 ──
SC['p5']['carry'].update(at=2, ats=[2, 2.3, 2.6, 3, 3.3], moveAt=3.6)
SC['d5']['players'][0].update(at=2, tagAt=2); SC['d5']['players'][1].update(at=2.2, tagAt=2.2); SC['d5']['side'][0]['at'] = 1
SC['a5']['items'][0]['sayAt'] = 3; SC['a5']['items'][1]['sayAt'] = 4
for _k, _sc in SC.items():
    if str(_sc.get('type', '')).startswith('apbc_'):
        _p = {n: a for n, a in _ppl(_sc).items() if n and n in _LT.get(_k, '')}
        if _p: _sc['_ppl'] = _p
        else: _sc.pop('_ppl', None)
SC['j7c']['title'] = "프로끼리 한일전 · 2015년 4강 승리 이후"
# ── 11/8 22시 반론 댓글 반영 2 ──
SC['j7c']['title'] = "프로끼리 한일전 · 2015 프리미어12 4강 이후"
SC['a5']['items'][0].update(at=2, sayAt=3); SC['a5']['items'][1].update(at=2.2, sayAt=4); SC['a5']['textAt'] = 1; SC['a5']['text'] = "감독: 경험·기록 보면 둘 중 한 명"
SC['a6']['text'] = "한 자리는 좌타자에게 강했던 투수들로"
SC['a11b']['chips'][1]['t'] = "2년 연속 출루율 4할대"
SC['a3b']['title'] = "120이닝 넘긴 선발 · 두 배 차이"
# ── 11/8 23:42 사용자 "왜 13일만 금요일이야? 요일 빼고 말해" ──
for _g in SC['o7']['games']: _g['d'] = _g['d'].replace(' 금요일', '')
# ── 11/8 23:46 사용자: 감독 소개가 뜬금없음(일정 뒤) → 명단 단락 첫머리로 옮겨 '처음 고른 명단이 바뀐' 이야기로 잇는다 ──
SC['o7b'] = dict(GRID("APBC 대표팀 감독", ['최원호'], at=1, cols=1), bg=BG_KOR)
SC['o9b'] = RB("투수가 가장 많은 팀", [dict(BAR("LG", 3, 1, hi=True), valAt=2), dict(BAR("SSG", 3, 1.2, hi=True), valAt=2), dict(BAR("롯데", 3, 1.4, hi=True), valAt=2)], 4, bw=220, gap=80)
SC['o9c'] = RB("야수가 가장 많은 팀", [dict(BAR("기아", 2, 1, hi=True), valAt=3), dict(BAR("한화", 2, 1.2, hi=True), valAt=3), dict(BAR("NC", 2, 2, hi=True), valAt=3), dict(BAR("삼성", 2, 2.2, hi=True), valAt=3), dict(BAR("두산", 2, 2.4, hi=True), valAt=3)], 3, bw=180, gap=60)
SC['p5']['carry'].update(**{'from': 1, 'to': 1, 'moveAt': 0})
# ── 11/8 23:47 사용자 "일본에 졌다 ✗ → 일본에게 졌다" (사람·팀 상대는 '에게') — 화면 글도 같이 ──
for _n in SC['p2']['nodes']:
    if _n.get('res'): _n['res'] = "결승에서 일본에게 패"
for _k in ('p3', 'p4'):
    for _n in SC.get(_k, {}).get('nodes', []):
        if _n.get('res') == "결승 일본에 패": _n['res'] = "결승에서 일본에게 패"
SC['q2b']['tiles'][0]['v'] = "호주에게 패"
def _rw(o):
    if isinstance(o, str): return o.replace('일본에 패', '일본에게 패').replace('호주에 패', '호주에게 패').replace('대만에 패', '대만에게 패')
    if isinstance(o, list): return [_rw(x) for x in o]
    if isinstance(o, dict): return {k: (_rw(v) if k not in ('img', 'narr') else v) for k, v in o.items()}
    return o
for _k in list(SC): SC[_k] = _rw(SC[_k])
# ── 11/8 23:55 말투 전수 점검 반영에 맞춘 장면 ──
for _it in SC['j7c']['items']: _it['at'] = 3
SC['j7c']['textAt'] = 3
SC['a5']['text'] = "감독: 경험·기록 보고 둘 중 한 명"
SC['h5']['side'] = [dict(t="우익수 출전", at=1, gold=True), dict(t="한국시리즈 팀 외야수 늦게 합류", at=2.5)]
# ── 11/8 23:56 사용자 "'대표팀 포수 둘 · 홈런' AI 같은 말 + 이름 없는 막대가 헷갈림" → 허인서 기록 한 장(비교 없이) ──
SC['h2'] = STT('허인서', "2026 허인서", [TI("타율", "2할 8푼 3리", 1), TI("홈런", "20", 2, True), TI("타점", "79", 2)], big="2026")
SC['p5']['chain'] = 'hist2'
# ── 11/8 23:57 사용자 "부상으로 빠지는 선수가 누군지도 말해줘" — 빠진 칸에 그 선수 프로필 + 이름 + 빨간 사유 ──
_PF = lambda n: 'KBO프로필/APBC프로필_' + n
SC['d1'] = SL('두산', [dict(img=_PF('최민석'), label="최민석", at=1, xAt=2, xLabel="팔꿈치 부상"), dict(icon='bat', label="야수", at=3), dict(icon='bat', label="야수", at=3.2)], title="두산 베어스 · 대표팀")
SC['n1'] = SL('NC', [dict(img=_PF('신영우'), label="신영우", at=1, xAt=1.4, xLabel="부상"), dict(img=CI('이준혁'), label="이준혁", at=2), dict(img=CI('김휘집'), label="김휘집", at=2.3), dict(img=CI('김주원'), label="김주원", at=2.6)], title="NC 다이노스 · 대표팀")
SC['k1'] = SL('KIA', [dict(img=_PF('곽도규'), label="곽도규", at=1, xAt=2, xLabel="허벅지 부상"), dict(icon='ball', label="투수", at=3), dict(icon='ball', label="투수", at=3.2), dict(icon='bat', label="내야수", at=3.4), dict(icon='bat', label="외야수", at=3.6)], title="기아 타이거즈 · 대표팀")
SC['s1'] = SL('삼성', [dict(img=_PF('장찬희'), label="장찬희", at=2, xAt=2.3, xLabel="원칙상 제외"), dict(img=_PF('배찬승'), label="배찬승", at=2.2, xAt=2.5, xLabel="원칙상 제외"), dict(icon='bat', label="야수", at=3), dict(icon='bat', label="야수", at=3.2)], [dict(t="한국시리즈 우승", at=0, gold=True), dict(t="원칙상 투수 제외", at=1)], title="삼성 라이온즈 · 대표팀")
for _k in ('d1', 'n1', 'k1', 's1'):
    _p = {n: a for n, a in _ppl(SC[_k]).items() if n and n in _LT.get(_k, '')}
    if _p: SC[_k]['_ppl'] = _p
SC['s1']['badges'] = [dict(t="한국시리즈 우승", at=0, gold=True)]
# ── 11/9 00:02 사용자 "이딴 건 만들지 마"(나이 순 점 그래프 apbc_ages) → 쓰지 않음. 아는 그림(구장·기록판)으로 ──
SC['r3'] = FLD("롯데 한동희", players=[dict(img=CI('한동희'), pos="3루수", at=0, tag="한동희", tagAt=0)], side=[dict(t="1999년생 · 대표팀 최고참", at=1, gold=True), dict(t="상무전 4번 타자 · 3루수", at=3)])
SC['k5b'] = dict(SC['k5'], tiles=[dict(t_, at=-1) for t_ in SC['k5']['tiles']] + [TI("대표팀 야수 중", "가장 어림", 1, True)], cont=True)
SC['r3'].pop('_ppl', None); SC['r3']['_ppl'] = {'한동희': 0}
# ── 11/9 00:05 사용자 "결승 가는 길 좀 더 직관적으로" → 한국 세 경기 줄에 승/패 칩 ──
SC['q5'] = S(0, "apbc_path", title="결승 가는 길", rows=[dict(d="12일", vs="호주", res=dict(t="승", at=1)), dict(d="13일", vs="일본", res=dict(t="패", at=0)), dict(d="14일", vs="대만", res=dict(t="승", at=1.3))], sum=dict(t="2승 1패 → 결승 노려 볼 만", at=2), bg=BG_KOR, chain='path')
SC['q5b'] = S(0, "apbc_path", title="결승 가는 길", rows=[dict(d="12일", vs="호주", res=dict(t="패", at=0)), dict(d="13일", vs="일본", hi=dict(t="반드시 이겨야", at=1)), dict(d="14일", vs="대만")], sum=dict(t="일본전 부담 ↑", at=2, red=True), bg=BG_KOR, chain='path', cont=True)
# 결승 가는 길: 날짜는 대사에 없으니 빼고 상대만(순서 = 경기 순서)
for _k in ('q5', 'q5b'):
    for _r in SC[_k]['rows']: _r['d'] = ''
# ── 11/9 00:08 사용자 "23년 결승에 1점 차로 진 건 왜 얘기 안 해?" → j6 에 2023 결승 3대 4 추가, j6b 는 '2017 결승만 빼고 셋 다 1점 차' ──
SC['j6']['tiles'][0]['at'] = 0.7; SC['j6']['tiles'][2]['at'] = 2
SC['j6']['tiles'][3]['at'] = 3
SC['j6b']['tiles'][3]['at'] = -1; SC['j6b']['tiles'][3]['keep'] = True; SC['j6b']['hiAt'] = 2
# ── 11/9 00:12 사용자 "흐름을 알 수가 없다. 단락을 나눠 무슨 이야기인지 설명해. 스윙맨 얘기하다 갑자기 첫 상대는 호주 / 대만에 지고 이기고… 불친절" ──
#    → 단락 첫 줄에 길잡이 말(구단별로 볼게요 · 명단은 여기까지, 결승 가는 길 · 이제 가장 중요한 13일 한일전)
#    → 결승 가는 길(조건)을 먼저 말하고 호주 · 대만을 그 뒤에, 대만 맞대결은 시간 순 한 장 기록판
for _it in SC['w1']['items']:
    if _it.get('name') == '전준표': _it['at'] = 2
SC['w1']['textAt'] = 2.6
_R3 = lambda: [dict(d="", vs="호주"), dict(d="", vs="일본"), dict(d="", vs="대만")]
# 11/9 00:25 사용자 OK 한 새 순서: 결승 가는 길(q5·q5b)은 대회 일정 바로 뒤 → 명단 끝난 뒤 q0 에서 같은 판을 다시 불러 '호주·대만 꼭 잡아야'
SC['q5']['cont'] = False; SC['q5']['sum'] = dict(t="일본에 져도 결승 보여", at=2)
SC['q0'] = S(0, "apbc_path", title="결승 가는 길", rows=[dict(d="", vs="호주", hi=dict(t="꼭 잡아야", at=2)), dict(d="", vs="일본"), dict(d="", vs="대만", hi=dict(t="꼭 잡아야", at=2.2))], bg=BG_KOR, chain='path0')
SC['q3']['tiles'][0]['k'] = "마지막 상대"
_REC = lambda: [dict(d="2023 APBC", vs="대만", sc="6 : 1", res=dict(t="승", at=3), at=2), dict(d="2024 프리미어12", vs="대만", res=dict(t="패", at=5), at=4),
                dict(d="2026 WBC", vs="대만", res=dict(t="패", at=5.3), at=5), dict(d="2026 아시안게임", vs="대만", sc="5 : 0", res=dict(t="승", at=99), at=99)]
SC['q4'] = S(0, "apbc_path", rec=True, title="대만전 기록", rows=_REC(), bg=BG_KOR, chain='rec')
_r = _REC()
for _x in _r[:3]: _x['at'] = -1; _x['res']['at'] = -1
_r[3]['at'] = 0; _r[3]['res']['at'] = 1
SC['q4d'] = S(0, "apbc_path", rec=True, title="대만전 기록", rows=_r, sum=dict(t="4번 맞대결 2승 2패", at=2), bg=BG_KOR, chain='rec', cont=True)
SC['j5'] = MUK("한국", "일본", "vs", "일본 3연패 도전", "13일 한일전", size=64, chain='hj')

# ── 11/9 00:31 사용자 "1번은 'APBC 대표팀은 28명이에요'로 시작하고 팀마다 뽑힌 인원" → 로고 뜨는 호흡 다시 맞춤 ──
_AT = {'LG': 1, 'SSG': 1, '롯데': 2, 'KIA': 2, '한화': 4, 'NC': 4, '삼성': 5, '두산': 5, '키움': 6, 'KT': 6}
SC['o1'] = S(0, "apbc_teams", logoOnly=True, title="APBC 대표팀", teams=[dict(team=t, n=len(ns), at=_AT[t], top=(f == 'top'), low=(f == 'low')) for t, ns, f in R28], bg=BG_KOR)
SC['o1'].pop('_ppl', None)
# ── 11/9 00:45 반론 에이전트 반영 ──
SC['q0']['rows'][0]['hi']['at'] = 3; SC['q0']['rows'][2]['hi']['at'] = 3.2
_REC = lambda: [dict(d="2023 APBC", vs="대만", sc="6 : 1", res=dict(t="승", at=2), at=1), dict(d="2024 프리미어12", vs="대만", res=dict(t="패", at=4), at=3),
                dict(d="2026 WBC", vs="대만", res=dict(t="패", at=4.3), at=4), dict(d="2026 아시안게임", vs="대만", sc="5 : 0", res=dict(t="승", at=99), at=99)]
SC['q4'] = S(0, "apbc_path", rec=True, title="대만전 기록", rows=_REC(), bg=BG_KOR, chain='rec')
for _it in SC['a4b']['items']:
    if _it['t'] == '일본전': _it['at'] = 2
    if _it['t'] == '대만전': _it['at'] = 2.2
SC['a4b']['text'] = "필승조 · 일본전과 대만전에"; SC["a4b"]["textAt"] = 2.4
SC['a6'] = S(0, "apbc_slots", team='', slots=[dict(img=_PF('곽도규'), label="곽도규", at=1, xAt=2, xLabel="부상"), dict(img=_PF('배찬승'), label="배찬승", at=1.2, xAt=2.2, xLabel="한국시리즈")], badges=[dict(t="좌타자에게 강했던 투수로", at=4, gold=True)], title="빠진 왼손 불펜", bg=BG_KOR)

# ── 11/9 01:14 사용자 "일본 잡는 법이 뒤에 나온다는 걸 맨 처음 인트로처럼" → 새 첫 줄 o0(질문) · o2b(목차 줄) 삭제. 끝 a0('?' 대결 화면)와 짝 ──
SC['o0'] = MUK("한국", "일본", "?", "일본 잡을 수 있을까?", "2026 APBC", size=72, chain='o0')
# 01:20 반론 에이전트: 첫 줄 예고와 a0 예고("제 생각을 말해 볼게요")가 같은 말 두 번 → a0 는 처음 질문을 다시 받아 답하는 줄로(같은 화면 짝)
SC['a0'] = MUK("한국", "일본", "?", "일본 잡을 수 있을까?", "처음 질문", size=72, chain='a0')
# 11/9 14:07 사용자 "3대 4로 졌죠 뒤에 화면이 잠깐 멈춘다" — 장면 8.4초(텀 1.6 포함)인데 클립이 7.75초라 끝에서 멈춤 → 끝내기 득점 장면(10.2~)부터 이어 붙여 8.75초
SC['p4']['clipCuts'] = [[0.2, 6.2], [10.2, 12.95]]
# 같은 검사(장면 길이 > 클립 길이)로 찾은 멈춤 두 곳도 같이: 2017결승 0.13초 · 안현민홈런 0.5초 → 같은 화면 안에서 앞·뒤로 늘림
SC['p3']['clipCuts'] = [[1.0, 4.4]]
SC['t2b']['clipCuts'] = [[0.2, 2.8], [3.4, 4.4], [5.6, 8.3]]
# 11/9 14:18 사용자 "다만 그때 일본은 → 심지어 그때 일본은" + 첫 호흡에 빈 화면(제목만) → 첫 칸을 첫 호흡 안에서 띄움
SC['j7b']['items'][0]['at'] = 0.5
# 11/9 14:18 같은 검사(첫 호흡에 제목만 있는 빈 화면)로 찾은 곳 같이: 1무 11패(세 호흡 빔) · 아시안게임 한일전 · 대만전 기록 · 일본 감독 강조
SC['j7c']['items'] = [C("승", 0.6, hi=True, fs=52)] + SC['j7c']['items']
SC['j7c']['cols'] = 7
SC['j7c']['title'] = "프로끼리 한일전 · 2015 프리미어12 4강부터"
SC['j7']['tiles'][0]['at'] = 0.6
SC['q4']['rows'][0]['at'] = 0.6
SC['a13']['items'][0]['at'] = 0.5

for _k in [k for k in SC if k not in KEYS]: SC.pop(_k)
missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing and not extra, (missing, extra)
lines, scenes = [], []
for j, (k, narr, sub) in enumerate(_t.LINES):
    sc = dict(SC[k]); sc['startLine'] = j
    sc.setdefault('bg', BG_NEU)
    lines.append(L(narr, sub)); scenes.append(sc)
for _i in range(1, len(scenes)):   # 11/8 영상 장면(bt_clip) 바로 뒤 다른 종류 장면은 이어받을 게 없으니 cont 를 뗀다
    if scenes[_i - 1]['type'] == 'bt_clip' and scenes[_i]['type'] != 'bt_clip': scenes[_i].pop('cont', None)
for _i in range(1, len(scenes)):   # 11/7 23:19 F-208: 같은 로고·국기가 이어지는 장면은 이어받기(로고·국기는 그대로, 글만)
    _a, _b = scenes[_i - 1], scenes[_i]
    if _a['type'] == _b['type'] and ((_a.get('logos') and _a.get('logos') == _b.get('logos')) or (_a['type'] == 'matchup' and (_a.get('left'), _a.get('right')) == (_b.get('left'), _b.get('right')))):
        _a.setdefault('chain', 'lk%d' % _i); _b['chain'] = _a['chain']; _b['cont'] = True
import re as _re   # 11/8 검수: 굵은 글꼴에서 '100이닝'이 '1000이닝'처럼 보임 → 숫자와 '이닝' 사이 아주 얇은 띄움(U+200A, 검수본4: U+2009 는 띄어쓰기로 읽힘), 화면 글·자막 모두
def _thin(o):
    if isinstance(o, str): return _re.sub(r'(\d)이닝', '\\1\u200a이닝', o)
    if isinstance(o, list): return [_thin(x) for x in o]
    if isinstance(o, dict): return {k_: (_thin(v_) if k_ not in ('img', 'narr', 'clip', 'clipFile', 'poster') else v_) for k_, v_ in o.items()}
    return o
scenes[:] = [_thin(x) for x in scenes]
_SP = lambda o: (_re.sub('(\\d)\u200a이닝', '\\1 이닝', o) if isinstance(o, str) else [_SP(x) for x in o] if isinstance(o, list) else {k_: (_SP(v_) if k_ not in ('img', 'narr') else v_) for k_, v_ in o.items()} if isinstance(o, dict) else o)
scenes[:] = [_SP(x) for x in scenes]   # 11/8 밤 화면 글은 '144 이닝'(맞춤법 제43항 띄어쓰기) — 아주 얇은 띄움도 '1440'처럼 보임
for _l in lines: _l['sub'] = _thin(_l['sub'])
# 11/8 22시 사용자 "화면이 이리저리 춤을 춘다": 이어받는 묶음 안에서 칸 수가 달라 가운데 맞춤이 흔들리던 것 →
# 묶음의 앞 장면에 뒤 장면 칸을 보이지 않게(at 50) 미리 깔아 둔다 · 1점 차 같은 아래 알약 자리도 미리 잡는다
_grp, _cur = [], []
for _i, _s in enumerate(scenes):
    if _cur and _s.get('cont') and _s['type'] == scenes[_cur[-1]]['type']: _cur.append(_i)
    else:
        if len(_cur) > 1: _grp.append(_cur)
        _cur = [_i]
if len(_cur) > 1: _grp.append(_cur)
for _g in _grp:
    _ty = scenes[_g[0]]['type']
    if _ty in ('bt_clip', 'bt_stat'):
        _mx = max(len(scenes[j].get('tiles') or []) for j in _g)
        for j in _g:
            _ts = scenes[j].get('tiles') or []
            _src = next(scenes[q]['tiles'] for q in _g if len(scenes[q].get('tiles') or []) == _mx)
            scenes[j]['tiles'] = _ts + [dict(_src[k], at=50) for k in range(len(_ts), _mx)]
    if _ty == 'apbc_games' and any(scenes[j].get('hiLabel') for j in _g):
        for j in _g: scenes[j]['hiSpace'] = True
# 11/8 23:49 사용자 "이런 작은 원으로 할 거면 프로필로 해": 인포그래픽(apbc_*) 안 원형 얼굴은 모두 KBO 공식 2026 프로필(네이버 스포츠 210×262)로
_PN = ["신영우", "곽도규", "최민석", "장찬희", "배찬승", "김도영", "김주원", "김휘집", "문현빈", "최준용", "안현민", "한동희", "김지찬", "김민석", "문정빈", "안재석", "이재현", "김민준", "박정민", "김진욱", "이로운", "김건우", "허인서", "조형우", "우강훈", "김영우", "박시원", "성영탁", "전준표", "이준혁", "조동욱", "박재현", "김태형"]
def _prof(o):
    if isinstance(o, str) and o.startswith('경기/') and 'JPN' not in o and '영상' not in o:
        n_ = next((n for n in _PN if n in o), None)
        return 'KBO프로필/APBC프로필_' + n_ if n_ else o
    if isinstance(o, list): return [_prof(x) for x in o]
    if isinstance(o, dict): return {k_: (_prof(v_) if k_ not in ('bg', 'poster', 'clip', 'clipFile', '_ppl') else v_) for k_, v_ in o.items()}
    return o
scenes[:] = [(_prof(x) if str(x.get('type', '')).startswith('apbc_') else x) for x in scenes]
def _extra_pics(o, acc):   # 11/8 PC build.py 는 img·img2·faces 만 모은다 → imgs·who·fImg 등 다른 칸 사진은 숨은 _pics 로 넘겨야 빈 원이 안 된다
    if isinstance(o, dict):
        for k_, v_ in o.items():
            if k_ in ('img', 'img2', 'faces', 'poster', '_pics', 'bg'): continue
            if isinstance(v_, str) and (v_.startswith('경기/') or v_.startswith('KBO프로필/')): acc.append(v_)
            elif isinstance(v_, list) and k_ in ('imgs',): acc += [x for x in v_ if isinstance(x, str) and x]
            else: _extra_pics(v_, acc)
    elif isinstance(o, list):
        for v_ in o: _extra_pics(v_, acc)
for _s in scenes:
    _a = []; _extra_pics(_s, _a)
    if _a: _s['_pics'] = [{'img': x} for x in dict.fromkeys(_a)]
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})
scenes.append(dict(END_SC, startLine=len(lines) - 1, bg=BG_NEU))

def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
CH = [ch("APBC 대표팀 28명 · 대회 일정", "o0", "q5b"), ch("지난 두 대회 준우승", "p1", "p5"), ch("최종 28명 명단", "o7b", "o9c"),
      ch("키움 전준표 · KT 안현민", "w1", "t4"), ch("삼성 김지찬 · 두산 안재석", "s1", "d7"), ch("한화 문현빈 · NC 김주원", "h1", "n6"),
      ch("LG 문정빈 · SSG 김민준", "l1", "g4"), ch("롯데 한동희 · 기아 김도영", "r1", "k6"), ch("꼭 잡아야 할 호주 · 대만", "q0", "q4d"), ch("한일전 관전 포인트", "j5", "j8f"), ch("일본 잡는 법 · 마운드와 타순 분석", "a0", "e3")]
DESC = ("APBC 대표팀 28명을 10개 구단별로 정리했어요. LG·SSG·롯데·기아가 네 명씩이고, 키움과 KT는 한 명씩이에요.\n"
        "11월 12일부터 도쿄돔에서 열리는 2026 아시아 프로야구 챔피언십(APBC), 우리 팀 선수는 누가 나가고 한일전은 어떻게 될까요?\n\n"
        "출전 자격(24세 이하·입단 3년 차 이내·와일드카드 3명), 처음 33명에서 최종 28명이 되기까지, 구단별 2026년 기록과 대표팀에서 맡을 자리, "
        "2017년·2023년 대회 결승 한일전, 한국시리즈 우승팀 삼성 등 구단별 합류 상황, 6일 상무전·7일 울산 웨일즈전 연습경기 결과, 그리고 제가 보는 일본 잡는 법(선발은 짧게, 4회부터 물량 계투, 김도영 뒤 타순)과 일본 경계 선수(마사키 도모야·야마구치 고키·다카하시 히로토) 분석까지 담았어요.\n\n"
        "등장 구단: 기아 타이거즈, 두산 베어스, 롯데 자이언츠, 삼성 라이온즈, 키움 히어로즈, 한화 이글스, KT 위즈, LG 트윈스, NC 다이노스, SSG 랜더스.\n"
        "등장 인물: 김건우, 김도영, 김민석, 김민준, 김영우, 김주원, 김지찬, 김진욱, 김태형, 김휘집, 문정빈, 문현빈, 박시원, 박재현, 박정민, 성영탁, 안재석, 안현민, 우강훈, 이로운, 이재현, 이준혁, 전준표, 조동욱, 조형우, 최원호, 최준용, 한동희, 허인서 / 부상·한국시리즈로 빠진 선수: 곽도규, 배찬승, 신영우, 장찬희, 최민석 / 일본: 다카하시 히로토, 마사키 도모야, 야마구치 고키.\n\n"
        "야구자판기는 매일 야구 이슈를 정리해요. 이번 한일전, 한국이 설욕할까요? 아니면 일본이 또 이길까요? 댓글로 남겨 주세요.\n\n▶ 지난 영상: 2027 FA 큰손 순위\n\n"
        "#APBC #야구대표팀 #한일전 #김도영 #도쿄돔 #프로야구 #KBO #야구자판기\n\n"
        "일본 선수 사진(위키미디어 공용): 마사키 도모야 — Orixbaseballclub, CC BY-SA 4.0 / 야마구치 고키 — Hotta Akahane, CC BY 4.0 / 다카하시 히로토 — neko kabachi, CC BY-SA 2.0\n")
TAGS = ["APBC", "APBC 대표팀", "야구 대표팀", "아시아 프로야구 챔피언십", "한일전", "APBC 명단", "김도영", "한동희", "문현빈", "김주원", "도쿄돔", "최원호", "프로야구", "KBO"]
SOURCE = "근거 = /home/claude/apbc/research.md (KBO 공식 선수 기록 11/7, 일간스포츠 11/5 명단, 마이데일리 11/4·스포츠경향 11/6 포지션, 스포츠조선 11/6·11/7 연습경기, OSEN 2023 APBC, 위키트리 아시안게임 명단, 주간경향 9/27)"
EP = {"theme": "m3", "introChapter": "APBC 대표팀 28명", "date": "2026-11-08", "gameDate": "2026-11-08", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1108-apbc-v7", "topic": "APBC대표팀", "endcardSec": 10, "gapScale": 1.15, "pauseMax": 0.42, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "2026 APBC 대표팀 28명 총정리 | 김도영·한동희 우리 팀은 누가? 한일전 관전 포인트", "description": DESC, "tags": TAGS, "hashtags": ["#APBC", "#야구대표팀", "#한일전", "#김도영", "#도쿄돔", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o0', 'o1', 'o2', 'a0', 'e3')}   # 질문·결론 줄은 느리게(완급)
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    for l in EP['lines'][:-1]:   # 짧은 첫 조각이 다음 조각과 합쳐져 낱말 중간에서 꺾이지 않게
        if len(l['narr'].split(' / ')) > 1 and len(l['sub'].split('|')[0]) <= 4: l['noMerge'] = True
    EP['lines'][KEYS.index('e3')]['noMerge'] = True
    EP['lines'][KEYS.index('p4')]['holdAfter'] = 1.6   # 11/8 23:48 사용자 "3:4 장면 너무 빨리 지나가서 볼 시간이 없어" — 결과(최종 3:4 패)를 보고 넘어가게
    _chs = {c['from'] for c in CH}; _tb = {KEYS.index(k) for k in ('t1', 's1', 'd1', 'h1', 'n1', 'l1', 'g1', 'r1', 'k1')}
    for i, l in enumerate(EP['lines'][:-1]):
        sg = l['narr'].split(' / ')
        if l.get('pauseMax') is None and any(x.rstrip().endswith('?') for x in sg[:-1]): l['pauseMax'] = 0.5
        if l.get('holdAfter') is None and l.get('gapAfter') is None and (i + 1) in _chs: l['gapAfter'] = 0.75
        elif l.get('gapAfter') is None and (i + 1) in _tb: l['gapAfter'] = 0.6   # 기준§6 11/6 팀이 바뀌는 자리 0.6
        if sg[-1].rstrip().endswith('?') and l.get('pauseMax') is None: l['pauseMax'] = 0.5
    # 11/7 23:20 검수본(7분 55초)과 대사가 같은 줄은 그 음성을 새 번호로 옮긴다(voiceRemap, 재합성 0)
    _vo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voice_old_1108.json')
    if os.path.exists(_vo):
        _old = json.load(open(_vo, encoding='utf-8'))
        EP['voiceRemap'] = [(_old.index(l['narr']) if l['narr'] in _old else None) for l in EP['lines']]
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-08_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
