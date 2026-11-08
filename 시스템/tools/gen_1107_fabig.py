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
# ── 2027 FA 큰손 순위 장면 (11/5) — 기아FA 편에서 검증한 rf_* 장면만 사용 ──
# 사진: 구단 제공·워터마크 없는 사진. 같은 사진은 롱폼 전체 2묶음까지.
P.update({
    "원태인": "경기/원태인_투구_0828_삼성제공", "원태인B": "경기/원태인_역투_삼성제공",
    "구자욱": "경기/구자욱_세리머니_0827_삼성제공", "구자욱B": "경기/구자욱_홈런세리머니_삼성제공",
    "최형우삼": "경기/최형우_만루포미소_0826_삼성제공",
    "김현수KT": "경기/김현수_송구_1006_KT제공", "박해민": "경기/박해민_주먹_LG제공",
    "홍창기": "경기/홍창기_상체_0921_LG제공", "박동원": "경기/박동원_세리머니_LG제공",
"김재환": "경기/김재환_300호축하_1001_SSG제공_카드", "김재환두": "경기/김재환_두산시절_두산제공", "최지훈": "경기/최지훈_타격_0920_SSG제공", "최지훈B": "경기/최지훈_주루_0920_SSG제공",
    "강백호": "경기/강백호_30호환대_0908_한화제공", "강백호B": "경기/강백호_헬멧인사_0915_한화제공",
    "류지현": "경기/류지현_취임_한화_사용자제공_카드", "노시환": "카드/P29c_노시환_경기_세로",
    "박찬호두": "경기/박찬호_홈쇄도_1005_두산제공", "양현종": "경기/양현종_글러브_1012_KIA제공", "김범수": "경기/김범수_투구_0304_KIA제공",
    "김호령": "경기/김호령_만루포_0821_KIA제공", "광주": "경기/광주_관중_1017_KIA제공",
    "이동욱": "카드/H14_이동욱", "이동욱2": "경기/이동욱_취임_1031_롯데제공", "박해민C": "경기/박해민_주먹_LG제공_카드", "노시환3": "경기/노시환_손하트_1010_한화제공", "노시환2": "카드/P29c_노시환_경기", "이택근": "경기/이택근_단장_1026_롯데제공", "레이예스": "경기/레이예스_타격_1012_롯데제공",
    "정수빈": "경기/정수빈_타격_1004_두산제공", "김원형": "카드/P21_김원형_박수",
    "최원준KT": "경기/최원준_204안타_1007_KT제공", "최원준KT2": "경기/최원준_미소_1005_KT제공", "KT덕아웃": "경기/최원준_더그아웃_0927_KT제공",
        "라일리": "경기/라일리_투구_NC제공", "알칸타라": "경기/알칸타라_주먹_키움제공", "송성문": "카드/P29c_송성문_SD",
    "삼성bg": "경기/최원태_경기_삼성제공", "최형우삼2": "경기/최형우_100타점_0918_삼성제공_중앙", "키움2": "경기/알칸타라_글러브_키움제공", "키움3": "경기/히우라_세리머니_키움제공", "키움4": "경기/데이비슨_손짓_키움제공",
    "KTbg2": "경기/이강철_덕아웃_KT제공", "KTbg3": "경기/고영표_투구_1011_KT제공", "최원준KT3": "경기/최원준_두검지_1006_KT제공",
    "LGbg2": "경기/오스틴_포효_LG제공", "LGbg3": "경기/문보경_10호_LG제공", "롯데2": "경기/레이예스_211안타_1012_롯데제공", "롯데3": "경기/한동희_타격_0918_롯데제공",
    "롯데4": "경기/전민재_세리머니_롯데제공", "롯데5": "경기/비슬리_박수_롯데제공", "롯데6": "경기/레이예스_204안타_1009_롯데제공", "두산2": "경기/정수빈_환영_0929_두산제공",
    "두산3": "경기/양의지_300호_두산제공_HQ", "NC2": "경기/라일리_포효_NC제공", "NC3": "경기/구창모_투구_1006_NC제공",
    "오지환": "경기/오지환_엄지_1017_LG제공", "최정": "경기/최정_타격_0716_SSG제공", "권희동": "경기/권희동_끝내기_0820_NC제공", "배정대": "경기/배정대_축하_0708_KT제공",
    "나성범": "경기/나성범_세리머니_KIA제공", "고영표": "경기/고영표_투구_1011_KT제공", "최원태세로": "경기/최원태_경기_삼성제공_세로", "양의지": "경기/양의지_300호_두산제공_HQ",
    "롯데FA3": "경기/롯데FA3_입단식_노진혁유강남한현희_롯데제공", "김현수LG": "경기/김현수_LG시절_LG제공", "SSGbg": "경기/김재환_결승포_1001_SSG제공", "삼성bg2": "경기/원태인_손짓_삼성제공",
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
NAME = {r[0]: r[1] for r in RT}
def BOARD(opened, nxt=None, last=None, **k):
    return dict(type="rf_rank", head="2027 FA 큰손 순위", unit=k.pop("unit", ""), cols=["순위", "구단", "나갈 연봉", "남은 돈"], rows=ROWS, open=opened,
                next=nxt, last=last, valW=230, bg=BG_NEU, noCenter=True, **k)
def BOARD_R(nxt, nat=2.0):   # 'N위는 / 힌트 / 바로 OO' — 이름 순간 칸에 이름(셋째 호흡)
    return BOARD(10 - nxt, nxt, (nxt + 1 if nxt < 10 else None), nextName=NAME[nxt], nextNameAt=nat)
CAP = 151.17
def _num(s):   # '131억 5천만' → 131.5
    import re as _re
    m = _re.match(r'(\d+)억(?: (\d)천만)?', s); return int(m.group(1)) + (int(m.group(2)) / 10 if m.group(2) else 0)
def CB(team, total=None, left=None, bgk=None, at1=1, at2=50, **k):   # 상한 막대(이미 쓸 돈 + 남은 돈)
    r = next((x for x in RT if x[1] == (team if team != "KIA" else "기아")), None)
    total = total or (r[2] if r else None); left = left or (r[3] if r else None)
    sc = dict(type="rf_capbar", who=TEAMN.get(team, team), team=team, cap=CAP, capLab="2027 상한 151억 1천만", total=(CAP - _num(left)) if left else 140,
              totalLab="", totalTxt=total, leftLab="남은 돈", leftTxt=left, totalAt=at1, leftAt=at2, capAt=at1, noCenter=True,
              bg=BGI(bgk, BLUR_F) if bgk else TBG(team), chain="cb" + team)
    if at1 is not None and 0 < at1 < 50: sc['totalAt'] = 0; sc['totalTxtAt'] = at1; sc['capAt'] = 0   # 11/7 검수본#2: '이미 쓸 돈은' 동안 빈 막대 ✗
    sc.update(k); return sc
TEAMN = {"삼성": "삼성 라이온즈", "LG": "LG 트윈스", "SSG": "SSG 랜더스", "한화": "한화 이글스", "KIA": "기아 타이거즈", "롯데": "롯데 자이언츠",
         "두산": "두산 베어스", "KT": "KT 위즈", "NC": "NC 다이노스", "키움": "키움 히어로즈"}
def LEFT_BARS(title, hi=(), hiAt=None, **k):   # 엔딩: 10개 구단 남은 돈 막대(남은 돈 적은 팀 → 많은 팀)
    its = [dict(label=r[1], v=r[4], txt=r[3], at=-1, hi=(r[1] in hi)) for r in RT]
    sc = RBARS(title, its, 110, bgk=None, bw=130, gap=40, valAt=-1, chain="lb", lfs=30, vfs=27, **k)
    sc["bg"] = BG_NEU
    if hiAt is not None: sc["hiAt"] = hiAt
    return sc
def SCEN(title, a, b, bgk, brk=None):   # 11/7 사용자 "이런 경우는 얼마, 저런 경우는 얼마" — 경우별 남은 돈 두 막대
    its = [dict(label=a[0], v=a[1], txt=a[2], at=a[3]), dict(label=b[0], v=b[1], txt=b[2], at=b[3], hi=True)]
    sc = RBARS(title, its, round(b[1] * 1.3), bgk=bgk, bw=300, gap=260, lfs=36, brkOff=150)
    if brk: sc["brk"] = brk
    if not bgk: sc["bg"] = BG_NEU
    return sc
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
# ── 오프닝 ──
SC['o1'] = dict(BOARD(0), chain="b0")
SC['o2'] = DUOT("2026 한국시리즈 뒤 최대어", [DCT("원태인", "원태인", "삼성", 0), DCT("구자욱", "구자욱", "삼성", 0)], chain="o2")
SC['o2h'] = dict(BOARD(0, 1, None), chain="b0h")   # 11/7 영상 검수: '돈이 가장 많이 남은 팀' 동안 삼성 듀오 ✗ → 순위표 1위 ? 깜빡
SC['o3'] = None
CAPS = [("2023년", 114.2, "114억 2천만"), ("2027년", 151.1, "151억 1천만")]
def CAPB():
    its = [dict(label=a, v=v, txt=t, at=0, valAt=(2 if a == "2027년" else 1), hi=(a == "2027년")) for a, v, t in CAPS]
    sc = RBARS("샐러리캡 상한", its, 160, bgk=None, bw=260, gap=160, chain="cap", lfs=36)
    sc["bg"] = BG_NEU; sc['hiAt'] = 2
    return sc
SC['o5'] = dict(type="rf_capbar", who="샐러리캡", team="", cap=CAP, capLab="상한", total=140, totalLab="외국인 뺀 구단 연봉 상위 40명의 합계", totalTxt="", totalAt=1, capAt=-1, noCenter=True, bg=BG_NEU, chain="o5", cont=True)
SC['o4'] = dict(SC['o5'], totalAt=50, capAt=0, cont=False)
SC['o3'] = KEEP(SC['o2h'])   # 11/7 검수본#2: 빈 막대 틀 2.5초 ✗ → 순위표 그대로, 샐러리캡 막대는 '샐러리캡'을 말하는 줄부터
SC['o6'] = KEEP(SC['o5'], capLab="2027 상한 151억 1천만")
SC['o7'] = dict(type="rf_capbar", who="샐러리캡을 처음 넘으면", team="", cap=CAP, capLab="상한", total=CAP, totalLab="구단 연봉 합계", totalTxt="", totalAt=-1, capAt=-1,
                over=dict(v=16, lab="넘은 돈", at=0), rate=dict(txt="× 30% = 제재금", at=1), noCenter=True, bg=BG_NEU)
SC['o8'] = dict(type="rf_capbar", who="팀마다 계산", team="", cap=CAP, capLab="2027 상한", total=110, totalLab="2027년에 나갈 연봉", totalTxt="", leftLab="", leftTxt="남은 돈",
                totalAt=1, leftAt=50, capAt=0, noCenter=True, bg=BG_NEU, chain="o8")
SC['o9'] = BAND("계약이 남은 선수", [], top=170, figY=400,
                fig=dict(type="steps", at=1, items=[dict(lab="계약금 + 보장 연봉", w=480, at=1), dict(lab="연수", join="÷", at=2), dict(lab="1년 몫", join="=", hi=True, at=2)]))
SC['o11'] = dict(type="rf_capbar", who="4년 계약 · 보장액 100억", team="", cap=CAP, capLab="2027 상한", total=25, totalLab="1년 몫", totalTxt="25억", totalAt=2, capAt=0, noCenter=True, bg=BG_NEU)   # 11/7 검수: 글자만 장면 → 상한 막대 위 1년 몫
SC['o9b'] = BAND("다년계약이 없는 선수", [V("2026년 연봉", "", 1, hi=True, size=100)], top=200, fig=dict(type="people", n=5, on=5, at=0))   # 11/7 20:13 사용자 "나머지 선수가 뭔 말이야?"
SC['o10'] = BAND("계산에서 뺀 선수", [V("FA 대상자", "2027", 0, size=100), V("방출·은퇴", "", 1, size=100)], top=200, fig=dict(type="people", n=3, on=0, at=0))
SC['o10b'] = dict(KEEP(SC['o8']), leftAt=1, cont=False)
SC['o12'] = KEEP(SC['o10b'], trend=dict(dir="none", lab="옵션·연봉 인상 빠진 추정치", at=2))
SC['o12c'] = BAND("보장액 비공개 계약", [], top=170, figY=400, fig=dict(type="steps", at=0, items=[dict(lab="총액"), dict(lab="연수", join="÷"), dict(lab="1년 몫", join="=", hi=True)]))
SC['o12b'] = BAND("FA 명단", [], top=170, figY=400, fig=dict(type="steps", at=0, items=[dict(lab="한국시리즈 뒤 공시", w=380, at=0), dict(lab="정해지지 않은 선수", w=380, at=2), dict(lab="남을 때", hi=True, at=3), dict(lab="떠날 때", join="none", hi=True, at=3)]))
SC['o13'] = dict(BOARD(0, 10, None), chain="b13")
# ── 10위 한화 ──
SC['h1'] = CB("한화", bgk="강백호B", at1=1, at2=2)
SC['h2'] = TC("노시환", "노시환", "한화", "한화 이글스", big=BIGV("11년 307억", "2027년부터", 0, size=150, yr=dict(per="27억 9천만", pv=27.9, at=2, pcAt=3)), imgAt=0, nameAt=0)
SC['h3'] = TC("강백호", "강백호", "한화", "한화 이글스", big=BIGV("4년 100억", "", 1, size=150, yr=dict(per="20억", pv=20.0, at=2, pcAt=3)), minor=[MI("보장액", "80억", 1)], imgAt=0, nameAt=0, chain="kbh")
SC['h5'] = TC("류지현", "류지현", "한화", "한화 이글스", minor=[MI("한화 2026년", "9위", 1)], imgAt=0, nameAt=0, chain="rjh")
SC['h6'] = KEEP(SC['h5']); SC['h6']['minor'] += [MI("약점", "중견수", 0), MI("감독 말", "첫 번째 시선은 우리 선수들 안에 있다", 3)]
SC['h6b'] = KEEP(SC['h6'])
SC['h7'] = TC("노시환", "노시환", "한화", "한화 이글스", big=BIGV("변수", "", 0, size=130), chain="nsh", imgAt=0, nameAt=0)
SC['h8'] = KEEP(SC['h7']); SC['h8']['minor'] = [MI("10월 31일", "포스팅 요청", 1)]
SC['h8q'] = KEEP(SC['h8']); SC['h8q']['minor'].append(MI("2026년 2월", "세계 최고의 무대에서 뛰는 게 꿈", 1))   # 스포츠조선 2026-02-24·노컷 02-23
SC['h10'] = SCEN("한화 남은 돈", ("노시환 남으면", 13.2, "13억 2천만", 0), ("노시환 메이저리그 가면", 40.8, "40억 8천만", 3), None,
                 brk=dict(a=1, b=1, lab="노시환 307억 제외", at=1))
SC['h10b'] = TC("노시환3", "노시환", "한화", "한화 이글스", big=BIGV("변수", "한화 FA 시장", 1, size=130), imgAt=0, nameAt=0)
# ── 9위 LG ──
SC['l1'] = CB("LG", bgk="LGbg3", at1=1, at2=2)
SC['l5'] = TC("박해민C", "박해민", "LG", "LG 트윈스", big=BIGV("4년 65억", "2025년 겨울 재계약", 2, size=170, yr=dict(per="15억", pv=15.0, at=4, pcAt=5)), minor=[MI("보장액", "60억", 3)], imgAt=0, nameAt=0, chain="phm")
SC['l4'] = TC("김현수KT", "김현수", "KT", "KT 위즈", minor=[MI("이적", "LG → KT", 0), MI("LG 2027 계산", "빠짐", 0)], imgAt=0, nameAt=0, chain="khs")   # 11/7 19:07 소감 줄 삭제 → 팀 돈과 잇기
SC['l6'] = DUOT("LG · 다년계약 거절", [DCT("홍창기", "홍창기", "LG", 0), DCT("박동원", "박동원", "LG", 0)], reserveStats=True, chain="l6")   # 11/7 19:00 사용자 "LG 팬은 두 선수 부진해서 내보내고 싶어하는데 다 잡는 게 숙제래" → 부진·구단 말 아낌으로 (OSEN 2026-11-04 한용섭, 마이데일리 2026-10-21)
SC['l6b'] = KEEP(SC['l6'], title="LG · 2026년 부진"); SC['l6b']['cards'][0]['stats'] = [dict(k="2026 타율", v="2할 3푼 9리", at=0)]; SC['l6b']['cards'][1]['stats'] = [dict(k="2026 타율", v="2할 2푼 5리", at=1)]
SC['l7'] = KEEP(SC['l6b'], title="“지금 아무런 얘기를 못 한다”")   # 차명석 단장, OSEN 2026-11-04
SC['l7c'] = KEEP(SC['l7'], title="LG 남은 돈 42억 4천만")   # 11/7 19:06 사용자 "LG 팬은 두 선수 내보내고 싶어하는데 잡는 게 숙제라는 소리"
# ── 8위 두산 ──
SC['d1'] = CB("두산", bgk="정수빈", at1=1, at2=2)
SC['d2'] = TC("박찬호두", "박찬호", "두산", "두산 베어스", big=BIGV("4년 80억", "", 1, size=170, yr=dict(per="19억 5천만", pv=19.5, at=3, pcAt=4)), minor=[MI("보장액", "78억", 2)], imgAt=0, nameAt=0, chain="pch")
SC['d3'] = TC("양의지", "양의지", "두산", "두산 베어스", big=BIGV("변수", "", 0, size=130), imgAt=0, nameAt=0, chain="yej")
SC['d4'] = KEEP(SC['d3']); SC['d4']['minor'] = [MI("2026시즌 뒤", "FA 선택 가능", 1)]
SC['d4q'] = KEEP(SC['d4']); SC['d4q']['minor'].append(MI("2026년 1월", "3~4년 뒤 그만할 생각", 2))   # OSEN 2026-01-20
SC['d4b'] = SCEN("두산 남은 돈", ("양의지 남으면", 49.7, "49억 7천만", 0), ("양의지 FA 택하면", 70.4, "70억 3천만", 3), "양의지",
                 brk=dict(a=0, b=0, lab="양의지 2년 42억 포함", at=1))
SC['d5'] = BAND("두산 · 2026년", [V("5위", "정규시즌", 0), V("탈락", "와일드카드", 1)], bgk="두산2", team="두산", top=130, fig=dict(type="rank", pos=5, cut=5, at=0))
SC['d6'] = TC("김원형", "김원형", "두산", "두산 베어스", minor=[MI("2026년 탈락 원인", "공격", 1)])
SC['d7'] = DUOT("두산 · 타자 보강 필요", [DCT("구자욱B", "구자욱", "삼성", 0, [dict(k="", v="특급 타자", at=1)])], cw=680, chain="d7")
SC['d7']['bg'] = TBG("두산")
SC['d8'] = KEEP(SC['d7'], title="두산 · 구자욱 영입전 뛰어들까")
# ── 7위 KT ──
SC['t1'] = CB("KT", bgk="KT덕아웃", at1=1, at2=2)
SC['t2'] = DUOT("KT · 2025년 겨울 외부 FA", [DCT("김현수KT", "김현수", "KT", 0), DCT("최원준KT3", "최원준", "KT", 0)], ttag="108억", ttagAt=2, reserveStats=True, chain="t2")
SC['t4'] = BAND("KT · 2026년", [V("90승", "", 1), V("1위", "정규시즌", 2, hi=True)], bgk="KTbg2", team="KT", top=130, fig=dict(type="rank", pos=1, cut=5, at=2))
SC['t5'] = BAND("KT · 1위 멤버", [V("여럿", "FA 앞둔 선수", 1, hi=True)], bgk="KT덕아웃", team="KT", top=130, fig=dict(type="rank", pos=1, cut=5, at=-1))
SC['t6'] = KEEP(SC['t5'])
# ── 6위 삼성 ──
SC['s1'] = CB("삼성", bgk="삼성bg", at1=1, at2=2)
SC['s1b'] = DUOT("삼성 · 계산에서 빠진 연봉", [DCT("원태인B", "원태인", "삼성", 0), DCT("구자욱B", "구자욱", "삼성", 0)], chain="s1b")
SC['s3'] = TC("최형우삼", "최형우", "삼성", "삼성 라이온즈", big=BIGV("2년 26억", "2025년 겨울", 2, size=170, yr=dict(per="13억", pv=13.0, at=3, pcAt=4)), imgAt=0, nameAt=0, chain="chw")
SC['s4'] = KEEP(SC['s1b'], title="삼성 단장 · 2025년 12월")   # 매일신문 2025-12-29 이종열 단장
SC['s5'] = TC("원태인", "원태인", "삼성", "삼성 라이온즈", big=BIGV("10억", "2026년 연봉", 2, size=170), minor=[MI("등급", "A 유력", 1)], chain="wti")
SC['s6'] = KEEP(SC['s5']); SC['s6']['minor'].append(MI("보상금", "최소 20억", 1))
SC['s6b'] = KEEP(SC['s6']); SC['s6b']['minor'].append(MI("2025년 12월", "날 인정해준다면 도전할 생각은 갖고 있다", 2))   # OSEN 2025-12-03
SC['s7'] = TC("구자욱", "구자욱", "삼성", "삼성 라이온즈", big=BIGV("5년 120억", "", 0, size=160, yr=False), minor=[MI("2026시즌", "끝", 1)], chain="gju")
SC['s8'] = KEEP(SC['s7']); SC['s8']['minor'].append(MI("타 구단 단장 전망", "100억 넘게", 2))
SC['s10'] = CB("삼성", bgk="삼성bg2", at1=-1, at2=0, totalTxt="")
# ── 5위 기아 ──
SC['k1'] = CB("KIA", bgk="광주", at1=1, at2=2)
SC['k2'] = DUOT("2025년 겨울 떠난 주전", [DCT("박찬호두", "박찬호", "두산", 0, [dict(k="기아 2027 계산", v="빠짐", at=2)]), DCT("최형우삼", "최형우", "삼성", 0, [dict(k="기아 2027 계산", v="빠짐", at=2)])])   # 11/7 19:05 사용자 "59억 말하고 쓸데없는 이야기 하다가 또 59억" → 인용·반복 줄 삭제, 나간 몫·들어온 몫으로
SC['k3'] = DUOT("2025년 겨울 계약", [DCT("양현종", "양현종", "KIA", 0, [dict(k="기아 2027 계산", v="포함", at=2, hi=True)]), DCT("김범수", "김범수", "KIA", 1, [dict(k="기아 2027 계산", v="포함", at=2, hi=True)])], chain="k3")
SC['k5'] = TC("김호령", "김호령", "KIA", "기아 타이거즈", minor=[MI("중견수", "생애 첫 FA", 1)], chain="khr")
SC['k5q'] = KEEP(SC['k5']); SC['k5q']['minor'].append(MI("기아 감독", "빨리 계약하라", 2))   # 스포츠경향·일간스포츠 2026-07-19
SC['k6'] = KEEP(SC['k5']); SC['k6']['big'] = BIGV("13홈런", "2026년", 1, size=170); SC['k6']['minor'] = [MI("타점", "68", 1), MI("커리어", "최다", 2)]
SC['k7'] = KEEP(SC['k6']); SC['k7']['minor'].append(MI("후반기 타율", "2할 4푼 5리", 1))
SC['k8'] = KEEP(SC['k7'])
# ── 4위 SSG ──
SC['g1'] = CB("SSG", bgk="최지훈B", at1=1, at2=2)
SC['g2'] = TC("최정", "최정", "SSG", "SSG 랜더스", big=BIGV("4년 110억", "", 0, size=150, yr=dict(per="27억 5천만", pv=27.5, at=1, pcAt=2)), imgAt=0, nameAt=0, chain="cj")
SC['g2b'] = BAND("SSG · 계산에서 빠진 연봉", [], bgk="SSGbg", team="SSG", top=170, figY=400, fig=dict(type="steps", at=1, items=[dict(lab="다년계약 끝", at=1), dict(lab="FA로 풀림", at=1), dict(lab="방출", join="+", at=2), dict(lab="연봉 빠짐", hi=True, at=3)]))
SC['g3'] = TC("김재환", "김재환", "SSG", "SSG 랜더스", big=BIGV("2년 22억", "2025년 겨울", 2, size=170, yr=dict(per="8억", pv=8.0, at=4, pcAt=5)), minor=[MI("옵션 6억 빼면", "16억", 3)], imgAt=0, nameAt=0, chain="kjh")   # 11/7 19:09 사용자 "2년 22억인데 어떻게 1년 8억?" — 계약금 6+연봉 10+옵션 6
SC['g4'] = TC("최지훈", "최지훈", "SSG", "SSG 랜더스", minor=[MI("2026시즌 전 다년계약 제안", "거절", 1)], chain="cjh")
SC['g5'] = KEEP(SC['g4']); SC['g5']['minor'].append(MI("관계자", "잡아야 한다. 저만한 선수가 없다", 1))
SC['g6'] = KEEP(SC['g5'])
# ── 3위 롯데 ──
SC['r1'] = CB("롯데", bgk="레이예스", at1=1, at2=2)
SC['r1b'] = BAND("롯데 · 2026년", [V("64승 77패", "", 1), V("7위", "정규시즌", 2, hi=True)], bgk="롯데2", team="롯데", top=130, fig=dict(type="rank", pos=7, cut=5, at=2))
SC['r2'] = BAND("롯데 · 2026년 팀 홈런", [V("113개", "", 1), V("최소", "10개 구단", 2, hi=True)], bgk="롯데3", team="롯데", top=130, fig=dict(type="rank", pos=10, lab="팀 홈런 순위", at=2))
SC['r3'] = BAND("롯데 · 보강 필요", [V("수비형 외야수", "", 0, hi=True)], bgk="롯데4", team="롯데", top=120, figY=420, fig=dict(type="field", at=0))
SC['r4'] = BAND("롯데 · 2025년 겨울", [V("0명", "외부 FA", 2, hi=True)], bgk="롯데5", team="롯데", chain="r4", top=130, fig=dict(type="people", n=3, on=0, at=0))
SC['r5'] = KEEP(SC['r4'])
SC['r6'] = DUO("롯데 · 2022년 겨울 FA 세 명", [DC("롯데FA3", "", 0, [dict(k="", v="170억", at=1, hi=True)], team="롯데")], cw=1000, chain="r6")
SC['r6']['bg'] = TBG("롯데")
SC['r6b'] = KEEP(SC['r6']); SC['r6b']['cards'][0]['stats'].append(dict(k="", v="2026시즌 끝", at=1))
SC['r6c'] = SCEN("롯데 남은 돈", ("세 명 모두 남으면", 65.4, "65억 4천만", 0), ("세 명 모두 떠나면", 82.4, "82억 4천만", 2), "롯데FA3")
SC['r7'] = DUOT("롯데 · 2026년 10월", [DCT("이동욱2", "이동욱", "롯데", 0, [dict(k="", v="새 감독", at=0)]), DCT("이택근", "이택근", "롯데", 0, [dict(k="", v="새 단장", at=0)])], cw=520, chain="r7")
SC['r8'] = KEEP(SC['r7'])
# ── 2위 NC ──
SC['n1'] = CB("NC", bgk="라일리", at1=1, at2=2)
SC['n1b'] = BAND("NC · 2026년", [V("64승 78패", "", 1), V("8위", "정규시즌", 2, hi=True)], bgk="NC2", team="NC", top=130, fig=dict(type="rank", pos=8, cut=5, at=2))
SC['n2'] = BAND("NC · 2026년", [V("2경기 차", "9월 5위와", 1), V("탈락", "", 2, hi=True)], bgk="NC3", team="NC", top=130, fig=dict(type="rank", pos=8, cut=5, at=2))
SC['n3'] = BAND("NC · 탈락 원인", [V("부상", "중심 타자", 0), V("교체 실패", "외국인 타자", 1, hi=True)], bgk="NC2", team="NC", top=130, fig=dict(type="people", n=2, on=0, at=1))
SC['n3b'] = BAND("NC · 2026년 겨울", [V("타선 보강", "", 1, hi=True)], bgk="NC3", team="NC", top=130, fig=dict(type="rank", pos=8, cut=5, at=-1))
SC['n4'] = TC("최원준KT3", "최원준", "KT", "KT 위즈", minor=[MI("2025년 겨울 이적", "NC → KT", 1), MI("NC 외야", "빈자리", 2)], imgAt=0, nameAt=0)
SC['n5'] = BAND("NC · 2024년부터", [V("내부 육성", "FA보다", 1, hi=True)], bgk="권희동", team="NC", top=130, fig=dict(type="people", n=3, on=3, at=0))   # 11/7 검수: 값 없는 NC 막대 다시 뜸 ✗
SC['n6'] = dict(BOARD(9, None, None, hiRows=[2], hiAt=0), chain="n6")   # 11/7 검수: '남은 돈이 가장 많아서' 동안 NC 줄 강조 유지
# ── 1위 키움 ──
SC['w2'] = CB("키움", bgk="알칸타라", at1=1, at2=3)
SC['w3'] = RBARS("2027 상한까지 남은 돈", [dict(label="NC", v=70.4, txt="70억 4천만", at=0), dict(label="키움", v=109.3, txt="109억 3천만", at=0, hi=True)], 120, bw=260, gap=120, lfs=36,
                 brk=dict(a=0, b=1, lab="38억 넘게 차이", at=1))
SC['w3']["bg"] = BG_NEU
_KF = dict(type="rf_capbar", who="키움 히어로즈", team="키움", cap=CAP, capLab="2027 상한", total=41.80, totalLab="", totalTxt="41억 7천만", totalAt=-1, capAt=-1,
           noCenter=True, bg=BGI("키움3", BLUR_F), chain="w4")
SC['w4'] = dict(_KF, floor=dict(v=60.65, lab="2027년 새 하한", at=1))
SC['w5'] = dict(_KF, floor=dict(v=60.65, lab="하한 60억 6천만", at=-1), short=dict(txt="18억 8천만", lab="키움 부족", at=1), cont=True)
SC['w6'] = dict(_KF, floor=dict(v=60.65, lab="하한 60억 6천만", at=-1), short=dict(txt="18억 8천만", lab="키움 부족", at=-1), rate=dict(txt="못 채우면 부족분 × 30%", at=1), cont=True)
SC['w7'] = KEEP(SC['w6'])
SC['w8a'] = TC("송성문", "송성문", "키움", "키움 → 샌디에이고", big=BIGV("최소 44억", "포스팅 금액", 50, size=150), minor=[MI("2025년 겨울", "메이저리그 이적", 1)], chain="ssm")   # 11/7 19:08 사용자 "선수 말은 영상과 관련 있을 때만"   # 헤럴드경제 2025-12-22·노컷 12-23
SC['w8'] = KEEP(SC['w8a']); SC['w8']['big']['at'] = 1
SC['w9'] = KEEP(SC['w8'])
# ── 정리·엔딩 ──
ET = "2027 상한까지 남은 돈 · 추정치"
SC['e1'] = LEFT_BARS(ET, hi=("키움", "NC", "롯데"), hiAt=2)
SC['e2'] = dict(LEFT_BARS(ET, hi=("한화",), hiAt=0), cont=True)
SC['e3'] = dict(LEFT_BARS(ET, hi=("삼성",), hiAt=0), cont=True)
SC['e3b'] = dict(LEFT_BARS(ET), cont=True)
SC['e4'] = dict(LEFT_BARS(ET, hi=("KT", "삼성", "기아", "SSG", "롯데", "NC", "키움")), cont=True)   # 11/7 19시: LG 는 두 선수를 다 잡을지 미정 → 집토끼 무리에서 뺌   # 11/7 검수: 두 무리 색 나눔(파랑 집토끼 · 노랑 지갑)
for _it in SC['e4']['items']:
    if _it['label'] in ("KT", "삼성", "기아", "SSG"): _it['hiAt'] = 1; _it['col'] = "#7DD3FC"
    else: _it['hiAt'] = 2
SC['e4']['legend'] = [dict(c="#7DD3FC", lab="집토끼 지키기", at=1), dict(c="#FFD43B", lab="남은 돈 많은 팀", at=2)]
SC['e5'] = KEEP(SC['e4'])
SC['e6'] = RBARS("2027 FA 진짜 큰손은?", [dict(label="삼성", v=57.0, txt="57억", at=0, valAt=1, hi=True, col="#7DD3FC"), dict(label="키움", v=109.3, txt="109억 3천만", at=0, valAt=3, hi=True)], 120, bw=260, gap=120, lfs=36)
SC['e6']["bg"] = BG_NEU
HINT = {"h0": "2024년 겨울부터 외부 FA 228억", "l0": "2025년 통합 우승", "d0": "2025년 겨울 FA 186억", "t0": "2026년 한국시리즈 직행", "s0": "투타 최대어", "k0": "2026년 플레이오프", "g0": "중견수 집토끼",
        "r0": "2026년까지 9년 연속 가을야구 놓침", "n0": "2026년 막판 8연패", "w1": "2026년까지 4년 연속 최하위"}   # 11/7 검수: 힌트에 말한 숫자 → 화면에
for _k, _n in REVEAL.items():
    SC[_k] = dict(BOARD_R(_n, 3.0 if _k in ("h0", "d0") else 2.0), chain="rv" + _k, hint=HINT[_k], hintAt=1)
HOLD = {"o13": 0.7, "h10b": 0.6, "l7c": 0.6, "d8": 0.7, "t6": 0.6, "s10": 0.6, "k8": 0.7, "g6": 0.6, "r8": 0.6, "n6": 0.7, "w9": 0.7}   # 11/7 검수: 챕터 경계 0.75   # 기준표 §7 순위표 쉼 0.6 — 순위 공개 직전·챕터 끝
RV_KEYS = list(REVEAL)
NOW, NOW_KEYS = {}, []
SC['h0']['chain'] = "b13"; SC['h0']['cont'] = True   # 오프닝 끝 순위표(10위 칸 깜빡)에서 그대로 이름만
SC['w1']['chain'] = "n6"; SC['w1']['cont'] = True   # n6 순위표에서 그대로

# ── 11/5 15:11 사용자 "선수 사진은 이런 템플릿(금테 카드 rf_gold) 사용해줘 · 선수 사진 가운데로 잘 맞춰라" ──
# 선수 카드(rf_card)를 전부 금테 카드로 바꾼다. 바탕은 소속 팀 색(14:54 지시), 사진은 몸 가운데(CX: 사진 폭 대비 몸 중심)를 카드 가운데로.
EN = {"원태인": "WON TAE-IN", "구자욱": "KOO JA-WOOK", "최형우": "CHOI HYOUNG-WOO", "김현수": "KIM HYUN-SOO", "박해민": "PARK HAE-MIN",
      "김재환": "KIM JAE-HWAN", "최지훈": "CHOI JI-HOON", "강백호": "KANG BAEK-HO", "류지현": "RYU JI-HYUN", "노시환": "NOH SI-HWAN",
      "김호령": "KIM HO-RYUNG", "박찬호": "PARK CHAN-HO", "김원형": "KIM WON-HYUNG", "최원준": "CHOI WON-JUN", "송성문": "SONG SUNG-MUN", "양의지": "YANG EUI-JI", "배정대": "BAE JUNG-DAE", "최정": "CHOI JEONG"}
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
QUOTE_K = ('목표', '소감', '각오', '기아 감독', '2026년 2월', '2025년 12월', 'LG', '이적 소감', '관계자', 'KT 단장 평가', '감독 말')   # 11/7 검수본#2: 양의지·최정은 원문 대조 못 함 → 따옴표 없는 요약
def _per(total, n):   # 1년 몫(천만 아래 자름)
    v = int(total * 10 / n) / 10; a = int(v); c = round((v - a) * 10)
    return f"{a}억" + (f" {c}천만" if c else "")
def TO_GOLD(sc):
    import re as _re
    st = []
    b = sc.get('big')
    if b:
        it = dict(k=b.get('k', ''), v=b['v'], at=b['at'], hi=True, size=min(b.get('size', 110), 110))
        m = _re.fullmatch(r'(\d+)년 (\d+)억', b['v'])
        if m and b.get('yr') is not False:
            it['years'] = dict(n=int(m.group(1)), per=_per(int(m.group(2)), int(m.group(1))), pv=int(int(m.group(2)) * 10 / int(m.group(1))) / 10)   # 11/5 23:14 계약 = 연도 칸
            if isinstance(b.get('yr'), dict): it['years'].update(b['yr'])   # 11/7 1년 몫 = (계약금+보장 연봉)/연수
        st.append(it)
    for m in sc.get('minor') or []:
        it = dict(k=m['k'], v=m['v'], at=m['at'], size=64)
        if m['k'].endswith('이적') and ' → ' in m['v']: a_, b_ = m['v'].split(' → '); it['move'] = dict(frm=a_, to=b_); it['move']['from'] = a_
        elif m['k'] in QUOTE_K: it['quote'] = True
        st.append(it)
    if st and st[0].get('years') and any(('보장액' in x['k'] or '빼면' in x['k']) for x in st[1:]):   # 11/7 19:09: 총액 → 보장액(옵션 뺀 값) → 1년 몫 원, 계산 순서대로 위에서 아래
        yr_ = st[0].pop('years'); st.append(dict(k='', v='', at=yr_.get('at', st[0]['at']), years=yr_))
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
CH = [ch("FA 큰손 10위~8위", "h0", "d8"), ch("FA 큰손 7위~5위", "t0", "k8"), ch("FA 큰손 4위~2위", "g0", "n6"), ch("FA 큰손 1위", "w1", "w9"), ch("FA 큰손 정리", "e1", "e6")]
DESC = ("2027 FA 큰손 순위 — 10개 구단이 2027년 샐러리캡(상한 151억 1천만 원) 안에서 FA에 쓸 수 있는 돈을 비교했어요.\n"
        "원태인·구자욱 같은 2027 FA 최대어를 데려갈 큰손은 어느 구단일까요?\n\n"
        "구단마다 2027년에 나갈 연봉을 계산해 상한에서 뺐어요. 계약이 남은 선수는 (계약금 + 보장 연봉) ÷ 연수(보장액이 공개되지 않은 계약은 총액 ÷ 연수), 다년계약이 없는 선수는 2026년 연봉으로 셌고, 2027 FA 대상자·방출·은퇴 선수와 외국인 선수는 뺐어요(국내 상위 40명, 천만 원 아래는 자름). "
        "옵션과 2027년 연봉 인상이 빠진 추정치라 실제 2027년엔 금액도 순위도 달라질 수 있고, FA 공시 전이라 아직 정해지지 않은 선수는 남을 때와 떠날 때를 둘 다 계산했어요.\n\n"
        "등장 구단: 기아 타이거즈, 두산 베어스, 롯데 자이언츠, 삼성 라이온즈, 키움 히어로즈, 한화 이글스, KT 위즈, LG 트윈스, NC 다이노스, SSG 랜더스.\n"
        "등장 인물: 강백호, 구자욱, 김범수, 김원형, 김재환, 김현수, 김호령, 노시환, 류지현, 박동원, 박찬호, 박해민, 송성문, 양의지, 양현종, 원태인, 이동욱, 이택근, 최원준, 최정, 최지훈, 최형우, 홍창기.\n\n"
        "야구자판기는 매일 야구 이슈를 정리해요. 2027 FA 시장의 진짜 큰손은 집토끼를 지키려는 팀일까요? 아니면 남은 돈이 많은 팀일까요? 댓글로 남겨 주세요.\n\n▶ 지난 영상: 기아 역대 FA 돈값 순위\n\n"
        "#FA큰손 #샐러리캡 #2027FA #원태인 #구자욱 #프로야구 #KBO #야구자판기\n")
TAGS = ["FA 큰손", "2027 FA", "샐러리캡", "경쟁균형세", "KBO 샐러리캡", "FA 시장", "원태인", "구자욱", "노시환", "양의지", "최지훈", "홍창기", "박동원", "프로야구", "KBO"]
SOURCE = "사실 출처 = 2027년 묶인 돈 모형 /home/claude/cap27 (statiz·KBO 선수 페이지 2026 연봉, 나무위키 FA 계약표 + 기사 대조: 양의지 데일리안 2026-03-20, 박세웅 노컷 2022-10-26 등), 상한: 시사저널 2026-08-15·OSEN 2026-01-05"
EP = {"theme": "m3", "introChapter": "FA 큰손 기준 · 샐러리캡", "date": "2026-11-07", "gameDate": "2026-11-07", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1107-fabig-v2", "topic": "FA큰손순위", "endcardSec": 10, "gapScale": 1.15, "pauseMax": 0.35, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "2027 FA 큰손 순위 | 원태인·구자욱 데려갈 팀은? 10개 구단 샐러리캡 여유", "description": DESC, "tags": TAGS, "hashtags": ["#FA큰손", "#샐러리캡", "#2027FA", "#원태인", "#구자욱", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'o2h', 'h10', 'd4b', 'r6c', 'w3', 'e4', 'e6') + tuple(RV_KEYS)}   # 11/5 종합진단: 질문·반전·결론·순위 공개 줄은 느리게(완급)
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    for l in EP['lines'][:-1]:   # 11/7 영상 검수: 짧은 첫 조각('삼성은'·'9월엔')이 다음 조각과 합쳐져 낱말 중간에서 꺾임 → 합치지 않음
        if len(l['narr'].split(' / ')) > 1 and len(l['sub'].split('|')[0]) <= 4: l['noMerge'] = True
    EP['lines'][KEYS.index('e6')]['noMerge'] = True   # 11/7 검수본#2: '아니면'이 앞 질문 끝에 붙음
    for _k, _h in HOLD.items(): EP['lines'][KEYS.index(_k)]['holdAfter'] = _h
    for _k in NOW_KEYS: EP['lines'][KEYS.index(_k)]['holdAfter'] = 0.7   # 11/5 10:28 근황 줄 뒤 순위표 머묾 → 카드
    for _k in RV_KEYS: EP['lines'][KEYS.index(_k)]['pauseMax'] = 0.8   # 11/5 15:23 사용자 "자문자답(1위는 누구일까요? 바로 OO)은 텀이 살짝 길게" — 힌트 뒤 '..' 쉼을 0.5초로 줄이지 않게
    for _k in RV_KEYS:
        if _k in NOW: EP['lines'][KEYS.index(_k)]['noMerge'] = True; continue   # 11/5 11:22 사용자 "김범수예요 / 현재 기아 불펜에서 — 텀이 너무 길어" → 근황 줄이 이어지면 0.7초 머묾 없이 보통 줄 사이 텀만
        EP['lines'][KEYS.index(_k)]['holdAfter'] = 0.7; EP['lines'][KEYS.index(_k)]['noMerge'] = True   # 11/5 검수: '8위는'처럼 짧은 첫 조각도 자막 따로   # 11/5 01:20 사용자 "순위표에서 몇 위는 누구예요 할 때 특히 빨라서 휙휙" — 이름 공개 뒤 순위표에 0.7초 머묾   # 순위표 보여 줄 쉼
    # 11/6 10:57 사용자 "단락 안에서 호흡 쉼이 살짝 길다 · 상황과 대사마다 섞어서" → 단락 안은 조이고(줄 안 0.35·줄 사이 ×1.15),
    #   자문자답(줄 중간 '?')은 0.5, 팀이 바뀌는 자리(순위 공개 앞)는 0.6, 챕터(단락)가 바뀌는 자리는 0.75 로 쉼을 남긴다
    _rvi = {KEYS.index(k) for k in RV_KEYS}; _chs = {c['from'] for c in CH}
    for i, l in enumerate(EP['lines'][:-1]):
        sg = l['narr'].split(' / ')
        if l.get('pauseMax') is None and any(x.rstrip().endswith('?') for x in sg[:-1]): l['pauseMax'] = 0.5
        if l.get('holdAfter') is None and l.get('gapAfter') is None:
            if (i + 1) in _chs: l['gapAfter'] = 0.75
            elif (i + 1) in _rvi: l['gapAfter'] = 0.6
    # 11/4 16시 검수본(132줄)과 대사가 같은 줄은 그 음성을 새 번호로 옮긴다(voiceRemap, 재합성 0) — 바뀐 15줄만 새로 합성
    _vo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voice_old_1107.json')
    if os.path.exists(_vo):
        _old = json.load(open(_vo, encoding='utf-8'))
        EP['voiceRemap'] = [(_old.index(l['narr']) if l['narr'] in _old else None) for l in EP['lines']]
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-07_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
