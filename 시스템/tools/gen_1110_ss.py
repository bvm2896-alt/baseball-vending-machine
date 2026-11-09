# -*- coding: utf-8 -*-
"""11/10 롱폼 「삼성 2027 스토브리그」 콘티.
대사 = tools/text_1110_ss.py. 근거 = research.md · cap_samsung.md
실행: python -X utf8 tools/gen_1110_ss.py → episodes/2026-11-10_롱폼.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t36', os.path.join(HERE, 'text_1110_ss.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
KEYS = [x[0] for x in _t.LINES]

BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억|(?:^| )다|(?:^| )못|(?:^| )안|(?:^| )만|(?:^| )(?:이번|지난|다음|올|그)|(?:^| )(?:네|다섯|여섯|일곱|여덟|아홉|열|열일곱)|중심|KBO|기아|WAR|\d+할|남는|좋은|\d+푼|\d+천만|역대|(?:^| )수|(?:^| )할|상위|넘은|(?:^| )더|\d+ FA)$'); BAD_B = re.compile(r'^(건|타선|겨울|코치|차|\d+차전|첫 |것 |수 |때 |중 |구단|달러|일|명|개|경기|원|타수|안타|\d+(?:푼|리)(?![가-힣]*할))')
WRAP = {'마음대로 쓸 수 있는 건 아니에요': '마음대로 쓸 수 있는 건\n아니에요', '구단마다 상위 40명 연봉 합계에': '구단마다\n상위 40명 연봉 합계에', '구단별 2025시즌 합계를 빼 봤어요': '구단별\n2025시즌 합계를 빼 봤어요', '10개 구단 가운데 가장 많았고': '10개 구단 가운데\n가장 많았고', '10개 구단 가운데 가장 적었고': '10개 구단 가운데\n가장 적었고', '보상금만 최소 20억 원이 들어서': '보상금만\n최소 20억 원이 들어서', '그때는 넘은 돈의 50%를 냈는데': '그때는\n넘은 돈의 50%를 냈는데', '류지현 감독이 새로 지휘봉을 잡았죠': '류지현 감독이\n새로 지휘봉을 잡았죠', '노시환의 메이저리그 포스팅을 요청했어요': '노시환의\n메이저리그 포스팅을 요청했어요', 'FA 세 명과 맺은 170억 계약이': 'FA 세 명과\n맺은 170억 계약이', '모자란 돈의 30%를 내야 하고요': '모자란 돈의 30%를\n내야 하고요', '들어온 돈과 나간 돈이 모두 커서': '들어온 돈과\n나간 돈이 모두 커서', '2025년 겨울에 영입한 강백호의': '2025년 겨울에\n영입한 강백호의', '샐러리캡을 넘겨야 할 수도 있어요': '샐러리캡을\n넘겨야 할 수도 있어요', '김재환의 1년 몫 11억만 빼도': '김재환의\n1년 몫 11억만 빼도', '강백호의 1년 몫 25억만 빼도': '강백호의\n1년 몫 25억만 빼도', '최형우의 1년 몫 13억만 빼도': '최형우의\n1년 몫 13억만 빼도', '2026년까지 9년 연속 가을야구를 놓친': '2026년까지\n9년 연속 가을야구를 놓친', '2026년 겨울 타선 보강이 급해요': '2026년 겨울\n타선 보강이 급해요', '남은 돈이 가장 많은 키움일까요?': '남은 돈이 가장 많은\n키움일까요?', '2025년까지 2년 동안 FA에 228억을 투자한': '2025년까지 2년 동안\nFA에 228억을 투자한', '2026년 13홈런 68타점으로': '2026년\n13홈런 68타점으로', '2023년 114억 2천만 원에서 올라': '2023년\n114억 2천만 원에서 올라', '그런데 강백호의 4년 100억은': '그런데 강백호의\n4년 100억은', '2026년 8월 고관절 수술 뒤': '2026년 8월\n고관절 수술 뒤', '옵션을 빼면 1년 몫은 8억 원이에요': '옵션을 빼면\n1년 몫은 8억 원이에요', '옵션을 빼면 1년 몫은 8억 원': '옵션을 빼면\n1년 몫은 8억 원', '모자란 돈의 30%를 내야 되고요': '모자란 돈의 30%를\n내야 되고요', '2026년 겨울엔 타선 보강이 급해요': '2026년 겨울엔\n타선 보강이 급해요', '5위와 2경기 차까지 쫓아갔지만': '5위와 2경기 차까지\n쫓아갔지만', 'FA를 앞둔 두 선수의 연봉이 빠지면서': 'FA를 앞둔\n두 선수의 연봉이 빠지면서', '옵션과 2027년 연봉 인상이 빠진': '옵션과\n2027년 연봉 인상이 빠진', '삼성의 원태인과 구자욱 같은 최대어들이': '삼성의 원태인과 구자욱 같은\n최대어들이', '시장에 나올 특급 타자라는 분석인데': '시장에 나올\n특급 타자라는 분석인데', '롯데는 이동욱 감독과 이택근 단장으로': '롯데는\n이동욱 감독과 이택근 단장으로', '그래도 원태인과 구자욱의 연봉이': '그래도\n원태인과 구자욱의 연봉이', '비FA 다년계약 선수들이 FA로 풀리고': '비FA 다년계약 선수들이\nFA로 풀리고', '2025년 겨울에 2년 26억에 삼성으로 와서': '2025년 겨울에\n2년 26억에 삼성으로 와서', '2025년 겨울에 2년 22억에 SSG로 왔고': '2025년 겨울에\n2년 22억에 SSG로 왔고', '이렇게 나가고 들어온 돈을 합치면': '이렇게 나가고\n들어온 돈을 합치면', '기아의 남은 돈은 59억 5천만 원이에요': '기아의 남은 돈은\n59억 5천만 원이에요', '박찬호를 4년 80억에 데려왔는데': '박찬호를\n4년 80억에 데려왔는데', '2026년 10월에 이동욱 감독과 이택근 단장으로': '2026년 10월에\n이동욱 감독과 이택근 단장으로', '길어봤자 3~4년 뒤엔 야구를 그만할 생각이라고 했죠': '길어봤자 3~4년 뒤엔\n야구를 그만할 생각이라고 했죠', '내년엔 건강한 모습으로 돌아오겠다고 했어요': '내년엔 건강한 모습으로\n돌아오겠다고 했어요', '내부 선수에게 먼저 기회를 줄 것으로 보여요': '내부 선수에게\n먼저 기회를 줄 것으로 보여요', '그래도 비FA 다년계약을 맺었던 선수들이': '그래도\n비FA 다년계약을 맺었던 선수들이', '2027년에 나갈 연봉을 계산해 봤어요': '2027년에 나갈 연봉을\n계산해 봤어요', '외국인을 뺀 구단 연봉 상위 40명의 합계에': '외국인을 뺀 구단 연봉\n상위 40명의 합계에', '2024년 겨울부터 FA에 228억을 쓴': '2024년 겨울부터\nFA에 228억을 쓴', '연수로 나눈 1년 몫으로 셌어요': '연수로 나눈\n1년 몫으로 셌어요', '한국시리즈가 끝난 뒤에 공시돼서': '한국시리즈가 끝난 뒤에\n공시돼서', '2024년부터 FA에 228억을 쓴': '2024년부터\nFA에 228억을 쓴', '두산은 2026년 5위에 올랐지만': '두산은\n2026년 5위에 올랐지만', '와일드카드 결정전에서 탈락했는데': '와일드카드 결정전에서\n탈락했는데', '두산이 구자욱 영입전에 뛰어들지가': '두산이 구자욱 영입전에\n뛰어들지가', '키움은 18억 8천만 원이 모자라요': '키움은\n18억 8천만 원이 모자라요', '다만 옵션과 연봉 인상이 빠진 추정이라': '다만 옵션과 연봉 인상이\n빠진 추정이라', '2026년까지 4년 연속 최하위': '2026년까지\n4년 연속 최하위', 'FA를 앞둔 원태인과 구자욱의 연봉이': 'FA를 앞둔\n원태인과 구자욱의 연봉이', '다음 차례는 원태인과 구자욱이라고 했지만': '다음 차례는\n원태인과 구자욱이라고 했지만', '아직 도전이 끝나지 않았다고 했고': '아직 도전이\n끝나지 않았다고 했고', '두 선수와 다년계약을 하고 싶다고 했지만': '두 선수와\n다년계약을 하고 싶다고 했지만', '다른 팀의 좋은 조건을 마다하고': '다른 팀의 좋은 조건을\n마다하고'}   # 11/5 검수: 직접 정한 꺾임
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
# ── 삼성 2027 스토브리그 장면 (11/9) — FA 큰손 편 rf_* 장면 + APBC 템플릿 ──
P.update({
    "원태인A": "경기/원태인_포효_스타뉴스", "원태인B": "경기/원태인_역투_삼성제공", "원태인C": "경기/원태인_손짓_삼성제공", "원태인D": "경기/원태인_투구_0828_삼성제공",
    "구자욱A": "경기/구자욱_적시타세리머니_스타뉴스", "구자욱B": "경기/구자욱_홈런세리머니_삼성제공", "구자욱C": "경기/구자욱_세리머니_0827_삼성제공",
    "강민호": "상황별/강민호_3점포_중앙", "김재윤": "경기/김재윤_투구_1007_삼성제공", "디아즈": "경기/디아즈_만루포세리머니_삼성제공",
    "후라도": "경기/후라도_경기_1019_삼성제공", "페덱": "경기/페덱_환호_삼성제공", "박진만": "경기/박진만_박수_0908_삼성제공",
    "이재현": "상황별/이재현_상체", "김지찬": "상황별/김지찬_상체", "김영웅": "상황별/김영웅_적시타_1026_삼성제공_중앙",
    "삼성bg": "경기/최원태_경기_삼성제공", "삼성bg2": "경기/최형우_100타점_0918_삼성제공_중앙",
    # 집 PC 에서 새로 받을 사진(11/9 밤) — 받기 전엔 빈 칸
    "우승": "경기/삼성_KS우승_1108", "MVP": "경기/구자욱_KSMVP_1108", "원태인KS": "경기/원태인_KS5차전_1108", "강민호우승": "경기/강민호_KS우승_1108",
    "이종열": "경기/이종열_단장_삼성", "매닝": "경기/매닝_삼성", "김도환": "경기/김도환_삼성",
    "윤석민BAL": "경기/윤석민_볼티모어_2014", "양현종TEX": "경기/양현종_텍사스_2021", "김현수BAL": "경기/김현수_볼티모어_2016",
})
_BIGV0 = BIGV
def BIGV(v, k, at, sub=None, size=None, yr=None):   # 11/7: yr=False 원 없음 · dict(per, pv, at) 1년 몫(보장 기준) 덮어쓰기
    d = _BIGV0(v, k, at, sub, size)
    if yr is not None: d["yr"] = yr
    return d
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
CY = {"김범수": 3}   # 11/6 세로 사진을 듀오(가로) 카드에 넣을 때 얼굴이 잘리지 않게 위쪽 기준(%)
CX = {"최정": .33, "이동욱2": .4, "김재환두": .58, "김범수": .5, "홍창기": .45, "박동원": .4, "원태인B": .5, "구자욱B": .36, "양현종": .45, "최원준KT3": .55, "최형우삼": .42, "원태인": .45, "구자욱": .5, "최형우삼2": .35, "김현수KT": .52, "박해민": .53, "김재환": .5, "최지훈": .45, "강백호": .5,
      "류지현": .5, "노시환": .45, "김호령": .36, "박찬호두": .3, "김원형": .6, "구자욱B": .36, "최원준KT2": .3, "송성문": .55}
def DCT(img, name, team, at, stats=None):
    c = DC(img, name, at, stats, team=team)
    import os as _o
    from PIL import Image as _I
    p = P.get(img, img); B = '/mnt/user-data/uploads/야구자판기/선수이미지/'
    f = next((B + p + e for e in ('.jpg', '.png') if _o.path.exists(B + p + e)), None)
    if f:   # 11/5 23:16 사용자 "홍창기 가운데로 오게": 듀오 카드(680×590)도 몸 가운데
        w, h = _I.open(f).size; cx = CX.get(img, .5); v = (h * 680 / 590) / w
        if v < 1: c['focus'] = "%d%% %d%%" % (round(max(0, min(100, (cx - v / 2) / (1 - v) * 100))), CY.get(img, 22))
        else: c['focus'] = "%d%% %d%%" % (round(cx * 100), CY.get(img, 22)); c['zoom'] = round(min(1.25, 1 / max(.5, 1 - abs(cx - .5) * 1.6)), 2) if abs(cx - .5) > .04 else 1
    return c
def DUOT(title, cards, bgk=None, **k):
    sc = DUO(title, cards, bgk=bgk, **k)
    if not bgk: _ts = {c.get("team") for c in cards}; sc["bg"] = TBG(_ts.pop()) if len(_ts) == 1 else BG_NEU   # 같은 팀 두 장이면 그 팀 색
    return sc

# ── 순위표 ── 11/7 재계산: 2027 상한 151억 1709만 − 2027년에 이미 쓸 돈(계약 선수 = (계약금+보장 연봉)/연수, 나머지 = 2026 연봉, FA 대상·방출·은퇴·외국인 제외, 국내 상위 40명) — /home/claude/cap27, 천만 원 아래 자름
RT = [(10, "한화", "137억 9천만", "13억 2천만", 13.2), (9, "LG", "108억 7천만", "42억 4천만", 42.4), (8, "두산", "101억 4천만", "49억 7천만", 49.7),
      (7, "KT", "96억 2천만", "54억 8천만", 54.8), (6, "삼성", "94억 1천만", "57억", 57.0), (5, "기아", "91억 6천만", "59억 5천만", 59.5),
      (4, "SSG", "88억 9천만", "62억 2천만", 62.2), (3, "롯데", "85억 7천만", "65억 4천만", 65.4), (2, "NC", "80억 7천만", "70억 4천만", 70.4),
      (1, "키움", "41억 7천만", "109억 3천만", 109.3)]
ROWS = [[r[0], r[1], r[2], r[3]] for r in RT]
def ST1(v, at, k=""): return [dict(k=k, v=v, at=at, hi=True)]
REVEAL = {"h0": 10, "l0": 9, "d0": 8, "t0": 7, "s0": 6, "k0": 5, "g0": 4, "r0": 3, "n0": 2, "w1": 1}

import copy as _copy
def KEEP(sc, **k):   # 이어지는 장면 — 이미 보인 항목은 처음부터 보임(at -1). 다시 자라거나 튀어나오면 깜빡임
    sc = _copy.deepcopy(sc)
    def f(o):
        if isinstance(o, dict):
            for kk in list(o):
                if kk in ('at', 'imgAt', 'nameAt', 'valAt', 'whoAt', 'hiAt', 'totalAt', 'leftAt', 'capAt', 'tagAt', 'ttagAt', 'cardAt', 'totalTxtAt', 'pcAt') and isinstance(o[kk], (int, float)) and o[kk] < 50: o[kk] = -1
                else: f(o[kk])
        elif isinstance(o, list):
            for v in o: f(v)
    f(sc); sc['cont'] = True; sc.update(k); return sc
CAP = 151.17
def _num(s):   # '131억 5천만' → 131.5
    import re as _re
    m = _re.match(r'(\d+)억(?: (\d)천만)?', s); return int(m.group(1)) + (int(m.group(2)) / 10 if m.group(2) else 0)
def CB(team, total=None, left=None, bgk=None, at1=1, at2=50, **k):   # 상한 막대(이미 쓸 돈 + 남은 돈)
    r = None
    total = total or (r[2] if r else None); left = left or (r[3] if r else None)
    sc = dict(type="rf_capbar", who=TEAMN.get(team, team), team=team, cap=CAP, capLab="2027 상한 151억 1천만", total=(CAP - _num(left)) if left else 140,
              totalLab="", totalTxt=total, leftLab="남은 돈", leftTxt=left, totalAt=at1, leftAt=at2, capAt=at1, noCenter=True,
              bg=BGI(bgk, BLUR_F) if bgk else TBG(team), chain="cb" + team)
    if at1 is not None and 0 < at1 < 50: sc['totalAt'] = 0; sc['totalTxtAt'] = at1; sc['capAt'] = 0   # 11/7 검수본#2: '이미 쓸 돈은' 동안 빈 막대 ✗
    sc.update(k); return sc
TEAMN = {"삼성": "삼성 라이온즈", "LG": "LG 트윈스", "SSG": "SSG 랜더스", "한화": "한화 이글스", "KIA": "기아 타이거즈", "롯데": "롯데 자이언츠",
         "두산": "두산 베어스", "KT": "KT 위즈", "NC": "NC 다이노스", "키움": "키움 히어로즈"}
P.update({"구자욱G": "경기/구자욱_삼성_G", "원태인G": "경기/원태인_삼성_G", "원태인H": "경기/원태인_투구_삼성제공", "우승2": "경기/삼성_KS우승_1108_2", "구장A": "경기/최형우_만루포미소_0826_삼성제공", "구장B": "경기/후라도_박수_삼성제공", "구자욱F": "경기/구자욱_결론_삼성", "원태인F": "경기/원태인_결론_삼성", "구자욱D": "상황별/구자욱_타격", "구자욱E": "경기/구자욱_부상_삼성제공_상체", "박세혁": "경기/박세혁_삼성", "디아즈": "경기/디아즈_경기_삼성제공", "디아즈2": "경기/디아즈_만루포세리머니_삼성제공", "후라도2": "경기/후라도_경기_삼성제공"})
P.update({"원태인B": "경기/원태인_KS5투구_뉴스1", "구자욱D": "경기/구자욱_KS5타격_뉴스1", "구자욱E": "경기/구자욱_KS5득점_뉴스1", "디아즈2": "경기/디아즈_KS2적시타_뉴스1", "디아즈3": "경기/디아즈_KS2환호_뉴스1", "강민호": "경기/강민호_타격_0621_뉴스1"})  # 11/10 사용자가 준 뉴스1 원본(작은 사진 교체)
SS = "삼성"; BG_SS = TBG(SS)
def TCs(img, name, kicker, big=None, minor=None, at=0, **k): return TC(img, name, SS, kicker, big=big, minor=minor or [], imgAt=at, nameAt=at, **k)
def BANDs(who, vals, bgk=None, **k): return BAND(who, vals, bgk=bgk, team=SS, **k)
def DUOs(title, cards, **k): return DUOT(title, cards, **k)
def SPs(img, name, bubbles, **k): sc = SP(img, name, bubbles, **k); sc['bg'] = BG_SS; sc['team'] = SS; return sc
def TLs(title, items, **k): sc = S(0, "tline", title=title, items=items, noCenter=True, **k); sc['bg'] = BG_SS; return sc
def Qs(text, logos=("삼성",), **k): sc = Q(text, list(logos), **k); sc['bg'] = BG_SS; return sc
def CAPS(who, total, **k):
    d = dict(type="rf_capbar", who=who, team=SS, cap=CAP, capLab="2027 상한 151억 1천만", total=total, totalLab="", totalTxt="", leftLab="", leftTxt="",
             totalAt=0, leftAt=50, capAt=0, noCenter=True, bg=BG_SS)
    d.update(k); return d
def KS(n, venue, win, at=-1, **x): return dict(dict(n=n, venue=venue, home=("KT" if venue == "수원" else "삼성"), win=win, at=at), **x)

def PS(img, name, sub, viz, stats=None, imgAt=None, team=SS, **k):
    sc = S(0, "pstat", img=ph(img), name=name, team=team, sub=sub, viz=viz, stats=stats or [], noCenter=True, bg=BG_SS, **k)
    if imgAt is not None: sc["imgAt"] = imgAt
    return sc
def VST(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def VSTEPS(items, **k): return dict(type="steps", items=items, **k)
def STP(d, t, at=0, c=None): return dict(d=d, t=t, at=at, **({"c": c} if c else {}))
def VQ(date, text, at, **k): return dict(type="quote", date=date, text=text, at=at, **k)
def STT(k, v, at=0, hi=False): return dict(k=k, v=v, at=at, hi=hi)
# ① 오프닝
SC['o1'] = BANDs("삼성 라이온즈", [V("12년 만", "한국시리즈 우승", 0, hi=True), V("2027년", "또 우승?", 1)], bgk="우승")
SC['o2'] = DUOs("우승 주역 두 사람 · 동시에 FA 시장으로", [DCT("원태인A", "원태인", SS, 0), DCT("구자욱A", "구자욱", SS, 0)], chain="o2")
SC['o3'] = KEEP(SC['o2'], title="둘 중 누가 남을까? · 영상 마지막에")
# ② 우승
SC['w0'] = TLs("삼성 라이온즈 우승", [dict(d="2011~2014년", t="4년 연속 통합우승", c="gold", at=0.4), dict(d="그 뒤", t="11년 동안 우승 없음", c="bad", at=2)])
SC['w1'] = BANDs("2026 정규시즌 · 삼성", [V("2위", "플레이오프 직행", 0.6, hi=True), V("83승 58패 3무", "", 3)], bgk="삼성bg")
SC['w2'] = TLs("2026 한국시리즈 · 삼성 vs KT", [dict(d="1차전", t="패", c="bad", at=2), dict(d="2차전", t="승", c="gold", at=2), dict(d="3차전", t="승", c="gold", at=2), dict(d="4차전", t="승", c="gold", at=2), dict(d="5차전", t="승", c="gold", at=2), dict(d="통산", t="9번째 우승\n1985년 포함", c="gold", at=50)], chain="ks")
SC['w2b'] = KEEP(SC['w2'], title="2026 한국시리즈 · 삼성 4승 1패"); SC['w2b']['items'][0]['t'] = "0:8 → 7:8\n추격 끝 패"; SC['w2b']['items'][1]['t'] = "연장 12회\n승리"; SC['w2b']['items'][0]['at'] = 0; SC['w2b']['items'][1]['at'] = 2; SC['w2b']['items'][2]['hl'] = 3; SC['w2b']['items'][3]['hl'] = 3  # 11/10 01:17~18 사용자: 바뀌는 칸은 그 말을 할 때 부드럽게 · 3·4차전은 '내리 이겼죠'에 반짝
SC['w3'] = KEEP(SC['w2b'], title="2026 한국시리즈 · 삼성 우승"); SC['w3']['items'][5]['at'] = 1; SC['w3']['items'][4]['t'] = "11월 8일\n12:1 승"; SC['w3']['items'][4]['at'] = 0
SC['w4'] = TCs("MVP", "구자욱", "2026 한국시리즈 MVP", big=BIGV("5할", "다섯 경기 타율", 1, size=170), minor=[MI("홈런", "1", 2), MI("타점", "6", 2)])
SC['w5'] = PS("원태인KS", "원태인", "한국시리즈 5차전 선발", [VST("우승 확정 5차전 선발", 0.2, size=52), VST("5이닝 1실점", 2, size=60)], imgAt=1)
SC['w5b'] = PS("강민호우승", "강민호", "2026 한국시리즈", [VST("프로 생활 내내 우승 없음", 0.2, "bad", size=52), VST("첫 우승", 2, size=60)], imgAt=1, focus="60% 28%")
SC['w6'] = DUOs("2026시즌 뒤 FA", [DCT("원태인B", "원태인", SS, 0, [dict(k="FA 신청하면", v="해외 협상 가능", at=1.5, hi=True)]), DCT("구자욱B", "구자욱", SS, 0, [dict(k="FA 신청하면", v="해외 협상 가능", at=1.5, hi=True)])], chain="w6")
# ③ 우승 직후 한 말
SC['s1'] = BANDs("우승을 확정한 날", [V("두 사람의 말", "", 0.3, hi=True)], bgk="우승2")
SC['s2'] = SPs("원태인C", "원태인", [BB("11월 8일", "에이전트를 이미 선임해 둔 상태다", 1, hi=True), BB("", "묵묵히 가을야구에만 모든 걸 쏟아부었다", 50)], chain="spw")
SC['s3'] = KEEP(SC['s2']); SC['s3']['bubbles'][1]['at'] = 0.4; SC['s3']['bubbles'][0]['hi'] = False; SC['s3']['bubbles'][1]['hi'] = True
SC['s4'] = SPs("구자욱D", "구자욱", [BB("11월 8일", "에이전트가 없어서 혼자 협상해야 하지만", 1), BB("", "진심으로 미국 무대에 도전해 보고 싶다", 50, hi=True), BB("구단주 대행 약속", "우승만 해라, 돈은 다 챙겨주겠다", 50), BB("", "우승만 하면 된다고 하셨으니 기다려보겠다", 50)], chain="spg")
SC['s5'] = KEEP(SC['s4']); SC['s5']['bubbles'][1]['at'] = 1
SC['s6'] = KEEP(SC['s5']); SC['s6']['bubbles'][2]['at'] = 1; SC['s6']['bubbles'][3]['at'] = 2; SC['s6']['bubbles'][3]['hi'] = True; SC['s6']['bubbles'][1]['hi'] = False
SC['s6b'] = SPs("원태인D", "원태인", [BB("11월 8일", "나와 자욱이 형을 위해 총대를 메어줄 차례", 1, hi=True)])
SC['s6c'] = PS("강민호우승", "강민호", "2026 한국시리즈 우승", [VST("두 후배 잔류 · 왕조 재건", 1, size=52)], focus="60% 28%")
SC['s7'] = TCs("이종열", "이종열", "단장", big=BIGV("최우선 목표", "두 사람 모두 잔류", 1.5, size=120))
# ④ 원태인
SC['t1'] = PS("원태인A", "원태인", "2019년 입단", [VSTEPS([STP("2019년", "삼성 입단", 1), STP("8년 동안", "75승", 2, c="gold"), STP("2024년", "15승 · 공동 다승왕", 50), STP("2026년", "7승 9패 · 평균자책점 4.52", 50, c="bad")])], chain="wti")
SC['t1b'] = KEEP(SC['t1']); SC['t1b']['viz'][0]['items'][2]['at'] = 0.4
SC['t2'] = KEEP(SC['t1b']); SC['t2']['viz'][0]['items'][3]['at'] = 1
SC['t3'] = DUOs("원태인의 2026 가을", [DCT("김재윤", "김재윤", SS, 1, [dict(k="마무리", v="부상", at=1)]), DCT("원태인KS", "원태인", SS, 0, [dict(k="불펜 → 선발", v="보직 안 가림", at=2.5, hi=True)])])
SC['t4'] = BANDs("원태인 · A등급 FA", [V("보상선수 + 20억", "", 3), V("보상금만 30억", "", 4, hi=True)], bgk="원태인G")
SC['t5'] = BANDs("원태인 · 국내 몸값 전망", [V("100억 원+", "", 1), V("200억 원까지", "", 2, hi=True)], bgk="원태인C")
SC['t6'] = PS("원태인B", "원태인", "미국 진출 평가", [VST("MLB닷컴", 0.2, size=52), VSTEPS([STP("직구", "시속 140km 후반", 2), STP("변화구", "좋은 체인지업", 3), STP("미국에선", "선발보다 불펜", 50), STP("포스팅 아닌 FA", "이적료 없음", 50, c="gold")])], imgAt=1, chain="mlb")
SC['t7'] = KEEP(SC['t6']); SC['t7']['viz'][1]['items'][2]['at'] = 1
SC['t8'] = KEEP(SC['t7']); SC['t8']['viz'][1]['items'][3]['at'] = 0.4
# ⑤ 구자욱
SC['u1'] = TCs("구자욱B", "구자욱", "2022년 다년계약", big=BIGV("5년 120억", "2022년 계약", 2, size=160), minor=[MI("2026시즌", "계약 끝", 3)])
SC['u2'] = PS("구자욱B", "구자욱", "2026년", [VST("타율 3할 7푼 1리", 0, size=60), VST("생애 첫 타격왕", 1, size=52)], stats=[STT("타점", "102", 2, hi=True), STT("OPS", "1.039", 50)], chain="gju2")
SC['u2b'] = KEEP(SC['u2']); SC['u2b']['stats'][1]['at'] = 0.4
SC['u3'] = TCs("MVP", "구자욱", "2026 한국시리즈", big=BIGV("부상 안고 출전", "허벅지", 1, size=120), chain="gmvp")
SC['u3a'] = KEEP(SC['u3']); SC['u3a']['minor'] = [MI("1차전", "대타 홈런", 1), MI("3차전", "2타점 3루타", 3)]
SC['u3b'] = BANDs("구자욱 · 통산", [V("3할 2푼 2리", "통산 타율 · 역대 4위", 0.4, hi=True), V("3년 연속", "외야수 골든글러브", 3)], bgk="구자욱G")
SC['u4'] = BANDs("구자욱 · 변수", [V("나이", "", 0.3), V("부상 이력", "", 1)], bgk="구자욱E")
SC["u5"] = Qs("중심 타자가 필요한 팀 · 관심 가능성", ("두산", "롯데"), logoAt=2)
SC['u6'] = BANDs("타격왕 FA · 협상 출발점", [V("100억 원+", "", 0.5, hi=True)], bgk="우승2")
# 미국행
SC["a1"] = Qs("KBO에서 FA로 바로 미국 · 현실적일까?")
SC['a2'] = PS("윤석민BAL", "윤석민", "2014년 볼티모어", [VST("메이저리그 0경기", 1.5, "bad", size=60)], team="")
SC['a3'] = PS("양현종TEX", "양현종", "2021년 텍사스", [VST("12경기 · 1년 만에 복귀", 2, "bad", size=56)], team="")
SC['a4'] = PS("김현수BAL", "김현수", "타자", [VST("첫해 3할 · 2년 만에 복귀", 3, size=52)], stats=[STT("2015년 겨울", "FA로 볼티모어", 1)], team="")
SC['a5'] = DUOs("FA로 미국 도전 · 나이", [DCT("구자욱C", "구자욱", SS, 0, [dict(k="2027년", v="34살", at=1, hi=True), dict(k="미국에선", v="쉽지 않은 나이", at=2.5)]), DCT("원태인C", "원태인", SS, 50, [dict(k="출생", v="2000년생", at=50, hi=True), dict(k="미국에서도", v="젊은 나이", at=50)])], chain="age")
SC['a6'] = KEEP(SC['a5']); SC['a6']['cards'][1]['at'] = 0; SC['a6']['cards'][1]['stats'][0]['at'] = 1; SC['a6']['cards'][1]['stats'][1]['at'] = 2
# ⑥ 샐러리캡
SC['c1'] = Qs("두 사람을 다 잡을 돈이 있을까?")
SC['c1b'] = BANDs("2027년 삼성 여유 자금 계산", [V("옵션 + 인상", "", 0.3), V("래리 버드 룰", "", 1, hi=True)], bgk="삼성bg")
SC['c2'] = CAPS("샐러리캡(경쟁균형세)", 0.01, capLab="상한", totalLab="", totalAt=-1, capAt=2, tag="국내 선수 상위 40명 연봉 합", tagAt=1, chain="cap0")
SC['c2b'] = BANDs("합계에 넣는 돈", [], tag="외국인·신인 제외", top=170, figY=400,
                  fig=dict(type="steps", at=0, items=[dict(lab="연봉", w=260, at=1), dict(lab="받은 옵션", join="+", at=1.3), dict(lab="계약금 ÷ 연수", join="+", hi=True, at=2)]))
SC['c3'] = BANDs("샐러리캡 상한", [V("151억 1700만", "2027년 상한", 1, hi=True)], bgk="구장B")
SC['c4'] = CAPS("삼성 라이온즈 · 2025년", 132.07, cap=137.12, capLab="2025 상한", tag="10개 구단 1위", tagAt=2, totalLab="상위 40명 합계", totalTxt="132억", leftLab="남은 돈", leftTxt="5억", totalAt=0, totalTxtAt=1, capAt=0, leftAt=3, chain="c4")
SC['c5'] = TCs("구자욱E", "구자욱", "2025년 합계 안에 든 돈", big=BIGV("20억", "2025년 연봉", 0.3, size=170), minor=[MI("은퇴 선수", "연봉도 포함", 1)], at=0)
SC['c6b'] = DUOs("계산에서 뺀 선수 · FA 4명 · 방출 10명", [DCT("원태인H", "원태인", SS, 0, [dict(k="FA", v="제외", at=1)]), DCT("구자욱D", "구자욱", SS, 0, [dict(k="FA", v="제외", at=1)])])
SC['c7'] = RBARS("2027년에 나갈 돈", [dict(label="계약 남은 8명 · 1년 몫 넉넉히", v=63.5, txt="63억 5천만", at=0, valAt=2), dict(label="나머지 32명 · 2026 연봉", v=30.6, txt="30억 6천만", at=3, valAt=4)], 75, bw=330, gap=200, lfs=34)
SC['c7']['bg'] = BG_SS
SC['c8'] = CAPS("삼성 라이온즈 · 2027년", 94.12, capLab="2027 상한 151억 1700만", totalLab="2027년에 나갈 돈", totalTxt="94억 1천만", totalAt=-1, capAt=-1, chain="c27")
SC['c9'] = BANDs("같은 방식으로 다시 센 2025년", [V("공식 발표보다", "", 0.3), V("10억 가까이 적게", "옵션 같은 비공개 몫", 2, hi=True)], bgk="구장A")
SC['c9a'] = CAPS("삼성 라이온즈 · 2027년", 94.12, capLab="2027 상한 151억 1700만", totalLab="2027년에 나갈 돈", totalTxt="94억 1천만", totalAt=-1, capAt=-1, capBelow=True, tag="옵션 최대 11억", tagAt=1, minus=dict(v=5.5, lab="옵션 절반", txt="5억 5천만", sign="+ ", at=2), chain="c27a")
SC['c9b'] = KEEP(SC['c9a'], tag="연봉 15% 인상(가정)", tagAt=1.5); SC['c9b']['minus2'] = dict(v=4.59, lab="연봉 32명 15% 인상", txt="4억 5천만", at=3)
SC['c9c'] = CAPS("삼성 라이온즈 · 2027년", 104.2, capLab="2027 상한 151억 1700만", totalLab="2027년에 나갈 돈(추정)", totalTxt="104억 안팎", totalAt=0.3, capAt=-1, tag="옵션 절반 + 연봉 인상", tagAt=-1, chain="c27b")
SC['c10'] = KEEP(SC['c9c']); SC['c10'].update(leftLab="남는 돈", leftTxt="47억 가까이", leftAt=1)
SC['c10b'] = CAPS("삼성 라이온즈 · 2027년", 112.7, capLab="2027 상한 151억 1700만", totalLab="최악의 경우", totalTxt="112억 7천만", totalAt=0.3, totalTxtAt=2, capAt=0, tag="옵션 전부 + 연봉 25% 인상", tagAt=0, leftLab="남는 돈", leftTxt="38억", leftAt=3, chain="c27c")
SC['c12'] = CAPS("두 사람을 다 잡으면", 104.2, capLab="2027 상한 151억 1700만", totalLab="2027년에 나갈 돈", totalTxt="104억", totalAt=-1, capAt=-1, capBelow=True, minus=dict(v=49.2, lab="연평균 25억씩 두 사람", txt="50억", sign="+ ", at=2), result=dict(lab="상한", txt="2억쯤 초과 또는 겨우 맞춤", at=3), tag="래리 버드 룰 = 프랜차이즈 선수 특례", tagAt=50, chain="c12")
SC['c13'] = KEEP(SC['c12'], tag="래리 버드 룰 = 프랜차이즈 선수 특례", tagAt=1)
SC['c14'] = BANDs("프랜차이즈 선수 특례", [V("해마다 1명", "한 팀에서 7시즌 이상", 0.4), V("절반만 계산", "그 선수 몫", 3, hi=True)], bgk="구장A")
SC['c15'] = CAPS("한 명을 특례로 지정하면", 104.2, capLab="2027 상한 151억 1700만", totalLab="2027년에 나갈 돈", totalTxt="104억", totalAt=-1, capAt=-1, capBelow=True, minus=dict(v=36.65, lab="두 사람(한 명은 절반만 계산)", txt="", sign="", at=0.3), ghost=dict(v=12.5, lab="특례로 빠지는 몫", txt="− 12억 5천만", at=1), result=dict(lab="", txt="10억쯤 남음", at=2), chain="c15")
SC['c16'] = BANDs("삼성 구상 · 보도", [V("특례 활용", "", 1), V("250억 원+", "두 사람에게", 3, hi=True)], bgk="우승")
SC['c16b'] = CAPS("4년 250억 원이면", 104.2, capLab="2027 상한 151억 1700만", totalLab="2027년에 나갈 돈", totalTxt="104억", totalAt=-1, capAt=-1, capBelow=True, minus=dict(v=45.0, lab="한 해 몫 · 특례 적용", txt="4년 250억", sign="+ ", at=1), result=dict(lab="남는 돈", txt="1억 미만 ~ 4억", at=3))
SC['c17'] = CAPS("상한을 넘으면", CAP, capLab="상한", totalLab="연봉 합계", totalAt=-1, capAt=-1, tag="2026년에 안 넘었다면", tagAt=1, over=dict(v=12, lab="넘은 돈", at=0.4), rate=dict(txt="넘은 돈 × 30%", at=2))
SC['c18'] = BANDs("아직 모르는 것", [V("12월", "KBO 2026 합계 발표", 1, hi=True), V("연봉 배분 · 군 입대", "옛 계약 · 방출", 2), V("몇억 원", "달라질 수 있음", 4)], bgk="구장B")
SC['k1'] = RBARS("2027년 남는 돈 · 옵션·인상 뺀 같은 방식", [dict(label="롯데", v=65.5, txt="삼성보다 8억+ ↑", at=2, valAt=3), dict(label="삼성", v=57.1, txt="삼성 기준", at=0.3, valAt=0.3, hi=True), dict(label="두산", v=49.7, txt="양의지 남으면 최대 7억 ↓", at=4, valAt=5)], 80, bw=260, gap=140, lfs=36)
SC['k1']['bg'] = BG_SS
SC['k2'] = TCs("원태인D", "원태인", "국내 팀이 데려가려면", big=BIGV("보상금까지", "얹어야", 1, size=150), minor=[MI("부담", "큼", 2)], at=0)
# ⑦ 외국인
SC['f1'] = BANDs("외국인 선수", [V("계산 제외", "샐러리캡", 0.6), V("재계약", "따로", 2, hi=True)], bgk="디아즈")
SC['f1b'] = DUOs("2025년 겨울 재계약", [DCT("디아즈3", "디아즈", SS, 0, [dict(k="최대", v="160만 달러", at=1)]), DCT("후라도", "후라도", SS, 0, [dict(k="최대", v="170만 달러", at=1.2)])])
SC['f2'] = PS("디아즈2", "디아즈", "외국인 타자", [VSTEPS([STP("2025년", "50홈런 158타점", 1, c="gold"), STP("2026년", "26홈런", 2, c="bad")])], stats=[STT("2026년", "144경기 전부", 50, hi=True), STT("한국시리즈 5차전", "적시타", 50)], chain="dz")
SC['f3'] = KEEP(SC['f2']); SC['f3']['viz'] = SC['f3']['viz'] + [VQ("2026년 9월", "50홈런 못 쳐도 좋은 타자로 남고 싶다", 1)]
SC['f4'] = KEEP(SC['f3']); SC['f4']['stats'][0]['at'] = 0; SC['f4']['stats'][1]['at'] = 1
SC['f5'] = PS("후라도", "후라도", "외국인 투수", [VST("플레이오프 13과 2/3이닝 3실점", 2, size=48)], stats=[STT("7월", "어깨 부상 · 6주", 1)])
SC['f6'] = PS("페덱", "페덱", "2026년 7월 합류", [VST("한국시리즈 5차전 4이닝 무실점", 3, size=48)], stats=[STT("정규시즌", "7승", 1, hi=True), STT("몸값", "약 48만 달러", 50), STT("평가", "신의 한 수", 50, hi=True)], chain="pd")
SC['f6b'] = KEEP(SC['f6']); SC['f6b']['stats'][1]['at'] = 0; SC['f6b']['stats'][2]['at'] = 1
SC['f7'] = PS("매닝", "매닝", "외국인 투수", [VST("팔꿈치 수술", 1.2, "bad", size=60)], stats=[STT("스프링캠프", "부상", 0.6)])
SC['f8'] = BANDs("외국인 재계약", [V("11월 9일까지", "발표 없음", 0.3), V("마지막 조각", "2연패 전력", 3, hi=True)], bgk="후라도2")
# ⑧ 2연패
SC['g1'] = SPs("박진만", "박진만", [BB("11월 8일", "당연히 2연패에 도전한다", 1, hi=True), BB("", "예상치 못한 부상 탓에 힘들었다", 50), BB("", "대체 자원을 키우는 데 집중해야 할 것 같다", 50)], chain="pjm")
SC['g2'] = KEEP(SC['g1']); SC['g2']['bubbles'][1]['at'] = 0; SC['g2']['bubbles'][2]['at'] = 1; SC['g2']['bubbles'][0]['hi'] = False; SC['g2']['bubbles'][2]['hi'] = True
SC['g3'] = TLs("KBO 2연패", [dict(d="2016년", t="두산 2연패", at=0.5), dict(d="그 뒤 10년", t="2연패 없음", c="bad", at=2), dict(d="2026년 겨울", t="계약이 핵심", c="gold", at=50), dict(d="2027년", t="삼성 도전", c="gold", at=50)], chain="g3")
SC['g3b'] = KEEP(SC['g3']); SC['g3b']['items'][3]['at'] = 0.3; SC['g3b']['items'][2]['at'] = 1
SC['g4'] = PS("강민호", "강민호", "포수", [VST("2027년까지 계약", 1, size=56)], stats=[STT("한국시리즈", "옆구리 부상 안고 출전", 3)], chain="kmh")
SC['g5'] = DUOs("삼성 안방", [DCT("강민호", "강민호", SS, 0, [dict(k="2026년 7월", v="“주전 포수는 김도환”", at=2, hi=True)]), DCT("김도환", "김도환", SS, 3)], chain="g5")
SC['g6'] = DUOs("2027년 삼성 안방", [DCT("박세혁", "박세혁", SS, 0, [dict(k="백업 포수", v="FA", at=0.4)]), DCT("김도환", "김도환", SS, -1, [dict(k="2027년", v="얼마나 크느냐", at=2, hi=True)])])
SC['g7'] = PS("김재윤", "김재윤", "마무리", [VST("불펜 과제", 0.2, "bad", size=56), VST("35세이브 · 세이브왕", 1, size=56)], stats=[STT("2027년", "30대 후반", 3, hi=True)], imgAt=2)
# ⑨ 결론
SC['e1'] = DUOs("삼성의 2027년", [DCT("원태인G", "원태인", SS, 0, [dict(k="한 명만 빠져도", v="2연패 어려움", at=50)]), DCT("구자욱G", "구자욱", SS, 0, [dict(k="한 명만 빠져도", v="2연패 어려움", at=50)])], chain="e1")
SC['e1b'] = KEEP(SC['e1'], title="둘 다 남으면 전력 유지"); SC['e1b']['cards'][0]['stats'][0]['at'] = 2; SC['e1b']['cards'][1]['stats'][0]['at'] = 2
SC['e2'] = PS("구자욱F", "구자욱", "거취 전망", [VST("잔류 가능성 ↑", 1, size=60), VSTEPS([STP("미국", "34살 타자 · 쉽지 않음", 50), STP("본인", "“기다려보겠다”", 50, c="gold")])], chain="e2")
SC['e3'] = KEEP(SC['e2']); SC['e3']['viz'][1]['items'][0]['at'] = 0.5; SC['e3']['viz'][1]['items'][1]['at'] = 2.5
SC['e4'] = PS("원태인F", "원태인", "거취 전망", [VST("미국행 문 열림", 4, size=60), VSTEPS([STP("에이전트", "해외 진출 위해 선임", 1), STP("FA", "이적료 없음", 2), STP("떠나면", "토종 선발 새로", 50, c="bad"), STP("2026년", "평균자책점 4점대 · 우승 확정", 50)])], chain="e4")
SC['e4b'] = KEEP(SC['e4']); SC['e4b']['viz'][1]['items'][2]['at'] = 1
SC['e4c'] = KEEP(SC['e4b']); SC['e4c']['viz'][1]['items'][3]['at'] = 0.3
SC['e5'] = KEEP(SC['e4c']); SC['e5']['viz'] = SC['e5']['viz'] + [VST("2연패의 열쇠", 1, size=64)]
SC['e6'] = DUOs("원태인·구자욱 · 남을까요? 떠날까요?", [DCT("원태인A", "원태인", SS, 0), DCT("구자욱A", "구자욱", SS, 0)])

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
CH = [ch("오프닝", "o1", "o3"), ch("12년 만의 한국시리즈 우승", "w0", "w6"), ch("우승 직후 원태인·구자욱이 한 말", "s1", "s7"),
      ch("원태인 · 몸값과 해외 진출", "t1", "t8"), ch("구자욱 · 타격왕의 다음 계약", "u1", "u6"), ch("FA로 바로 미국? 선배들의 길", "a1", "a6"),
      ch("삼성 지갑 계산 · 래리 버드 룰", "c1", "k2"), ch("외국인 선수 · 디아즈·후라도·페덱·매닝", "f1", "f8"),
      ch("2연패 과제 · 안방과 불펜", "g1", "g7"), ch("결론 · 누가 남을까", "e1", "e6")]
DESC = ("12년 만에 한국시리즈 우승을 차지한 삼성 라이온즈의 2027 스토브리그를 정리했어요. 우승 주역 원태인과 구자욱이 동시에 FA 시장에 나오는데, 두 사람은 삼성에 남을까요?\n\n"
        "한국시리즈 5경기 흐름, 우승 직후 원태인(해외 진출을 위한 에이전트 선임)과 구자욱(미국 도전, 구단의 약속을 기다리겠다)이 한 말, 이종열 단장의 '두 사람 모두 잔류' 목표, "
        "두 선수의 기록과 예상 몸값, FA로 바로 미국에 간 선배들(윤석민·양현종·김현수)의 사례를 담았어요.\n\n"
        "삼성의 2027년 샐러리캡도 옵션 절반 지급과 연봉 15% 인상(가정)을 넣어 계산했고(남는 돈 47억 원 가까이, 옵션을 다 주고 연봉이 25% 오르면 38억 원), "
        "래리 버드 룰로 불리는 프랜차이즈 선수 특례(구단마다 해마다 한 팀에서 7시즌 이상 뛴 선수 1명의 몫을 절반만 계산)를 쓰면 두 사람을 다 잡아도 상한 안에 들어오는지 따져 봤어요. "
        "삼성의 실제 2026년 상위 40명 합계는 12월 KBO 발표로 확정되고, 군 입대·추가 방출은 반영하지 못했어요.\n\n"
        "등장 인물: 강민호, 구자욱, 김도환, 김재윤, 김현수, 디아즈, 매닝, 박세혁, 박진만, 양의지, 양현종, 원태인, 윤석민, 이종열, 페덱, 후라도.\n\n"
        "야구자판기는 매일 야구 이슈를 정리해요. 원태인과 구자욱, 삼성에 남을까요? 떠날까요? 댓글로 남겨 주세요.\n\n▶ 지난 영상: APBC 대표팀 28명 총정리\n\n"
        "#삼성라이온즈 #스토브리그 #원태인 #구자욱 #샐러리캡 #프로야구 #KBO #야구자판기\n")
TAGS = ["삼성 라이온즈", "삼성 스토브리그", "2027 스토브리그", "원태인", "구자욱", "원태인 FA", "구자욱 FA", "삼성 샐러리캡", "프랜차이즈 특례", "래리 버드 룰", "샐러리캡", "한국시리즈 우승", "프로야구", "KBO"]
SOURCE = "근거 = /home/claude/ss27/research.md · 샐러리캡 계산 = /home/claude/ss27/cap_samsung.md (/home/claude/cap27 모형)"
EP = {"theme": "mg", "mgWord": "SAMSUNG LIONS", "introChapter": "오프닝", "date": "2026-11-10", "gameDate": "2026-11-10", "series": "야구롱폼", "focusTeam": "삼성", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1110-ss27-v1", "topic": "삼성2027스토브리그", "endcardSec": 10, "gapScale": 1.05, "pauseMax": 0.42, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "삼성 2027 스토브리그 | 우승 주역 원태인·구자욱 남을까? 해외·FA 총정리", "description": DESC, "tags": TAGS,
                  "hashtags": ["#삼성라이온즈", "#스토브리그", "#원태인", "#구자욱", "#샐러리캡", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'c1', 'c10', 'c15', 'e2', 'e5', 'e6')}   # 질문·반전·결론 줄은 느리게
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    for l in EP['lines'][:-1]:
        if len(l['narr'].split(' / ')) > 1 and len(l['sub'].split('|')[0]) <= 4: l['noMerge'] = True
    EP['lines'][KEYS.index('e6')]['noMerge'] = True
    for _k in ('w3', 'c10', 'c15'): EP['lines'][KEYS.index(_k)]["holdAfter"] = 0.8   # 결과·숫자 장면은 보고 넘어가게
    _chs = {c['from'] for c in CH}
    for i, l in enumerate(EP['lines'][:-1]):
        sg = l['narr'].split(' / ')
        if l.get('pauseMax') is None and any(x.rstrip().endswith('?') for x in sg[:-1]): l['pauseMax'] = 0.5
        if l.get('holdAfter') is None and l.get('gapAfter') is None and (i + 1) in _chs: l["gapAfter"] = 0.55
        if sg[-1].rstrip().endswith('?') and l.get('pauseMax') is None: l['pauseMax'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-10_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
