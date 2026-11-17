# -*- coding: utf-8 -*-
"""helpers copied from gen_1110_ss.py (11/10 삼성 2027) for 11/13 FA 공시 총정리.
대사 = tools/text_1110_ss.py. 근거 = research.md · cap_samsung.md
실행: python -X utf8 tools/gen_1110_ss.py → episodes/2026-11-10_롱폼.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT

BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억|(?:^| )다|(?:^| )못|(?:^| )안|(?:^| )만|(?:^| )(?:이번|지난|다음|올|그)|(?:^| )(?:네|다섯|여섯|일곱|여덟|아홉|열|열일곱)|중심|KBO|기아|WAR|\d+할|남는|좋은|\d+푼|\d+천만|역대|(?:^| )수|(?:^| )할|상위|넘은|(?:^| )더|\d+ FA|남은|나쁜|(?:^| )갈|(?:^| )줄|(?:^| )새|(?:^| )꼭|(?:^| )(?:오후|오전|아침|밤)|\d+인|(?:^| )든)$'); BAD_B = re.compile(r'^(않|못 |곳|것|수도|중인|줘|로스터|옵션|이슈|공시|\d+시|건|타선|겨울|코치|차|\d+차전|첫 |것 |수 |때 |중 |구단|달러|일|명|개|경기|원|타수|안타|\d+(?:푼|리)(?![가-힣]*할))')
BAD_B2 = re.compile(r'^(밖에서|외에서|없이|되거든요|되는|돼요|등(?: |$|이|은|을)|보겠|볼 |볼$|거라|거예요|거고|하는|할 |만한|수 |있어|있는|있다|있고|줘야|써야|해요|했어요|한다|않|못 )')
JOSA_END = re.compile(r'(은|는|이|가|을|를|에|의|도|로|와|과|서|고|며|면|데|만|요|죠|다|게|지|니|까|해|돼|라|여|어|아|께|엔|선|든|듯|럼|큼|야|,|\?)$')
WRAP = {'메이저리그가 직장폐쇄에 들어갈 수 있어요': '메이저리그가 직장폐쇄에\n들어갈 수 있어요', '메이저리그 노사협약이 끝나거든요': '메이저리그 노사협약이\n끝나거든요', '왜 또 멈출 수 있다는 걸까요?': '왜 또 멈출 수\n있다는 걸까요?', '4억 4100만 달러라고 했어요': '4억 4100만\n달러라고 했어요', '선수노조 브루스 마이어 위원장 대행은': '선수노조 브루스 마이어\n위원장 대행은', '40인 로스터 선수를 데려오려면': '40인 로스터 선수를\n데려오려면', '왓슨을 40인 로스터에 올리면서': '왓슨을\n40인 로스터에 올리면서', '마음대로 쓸 수 있는 건 아니에요': '마음대로 쓸 수 있는 건\n아니에요', '구단마다 상위 40명 연봉 합계에': '구단마다\n상위 40명 연봉 합계에', '구단별 2025시즌 합계를 빼 봤어요': '구단별\n2025시즌 합계를 빼 봤어요', '10개 구단 가운데 가장 많았고': '10개 구단 가운데\n가장 많았고', '10개 구단 가운데 가장 적었고': '10개 구단 가운데\n가장 적었고', '보상금만 최소 20억 원이 들어서': '보상금만\n최소 20억 원이 들어서', '그때는 넘은 돈의 50%를 냈는데': '그때는\n넘은 돈의 50%를 냈는데', '류지현 감독이 새로 지휘봉을 잡았죠': '류지현 감독이\n새로 지휘봉을 잡았죠', '노시환의 메이저리그 포스팅을 요청했어요': '노시환의\n메이저리그 포스팅을 요청했어요', 'FA 세 명과 맺은 170억 계약이': 'FA 세 명과\n맺은 170억 계약이', '모자란 돈의 30%를 내야 하고요': '모자란 돈의 30%를\n내야 하고요', '들어온 돈과 나간 돈이 모두 커서': '들어온 돈과\n나간 돈이 모두 커서', '2025년 겨울에 영입한 강백호의': '2025년 겨울에\n영입한 강백호의', '샐러리캡을 넘겨야 할 수도 있어요': '샐러리캡을\n넘겨야 할 수도 있어요', '김재환의 1년 몫 11억만 빼도': '김재환의\n1년 몫 11억만 빼도', '강백호의 1년 몫 25억만 빼도': '강백호의\n1년 몫 25억만 빼도', '최형우의 1년 몫 13억만 빼도': '최형우의\n1년 몫 13억만 빼도', '2026년까지 9년 연속 가을야구를 놓친': '2026년까지\n9년 연속 가을야구를 놓친', '2026년 겨울 타선 보강이 급해요': '2026년 겨울\n타선 보강이 급해요', '남은 돈이 가장 많은 키움일까요?': '남은 돈이 가장 많은\n키움일까요?', '2025년까지 2년 동안 FA에 228억을 투자한': '2025년까지 2년 동안\nFA에 228억을 투자한', '2026년 13홈런 68타점으로': '2026년\n13홈런 68타점으로', '2023년 114억 2천만 원에서 올라': '2023년\n114억 2천만 원에서 올라', '그런데 강백호의 4년 100억은': '그런데 강백호의\n4년 100억은', '2026년 8월 고관절 수술 뒤': '2026년 8월\n고관절 수술 뒤', '옵션을 빼면 1년 몫은 8억 원이에요': '옵션을 빼면\n1년 몫은 8억 원이에요', '옵션을 빼면 1년 몫은 8억 원': '옵션을 빼면\n1년 몫은 8억 원', '모자란 돈의 30%를 내야 되고요': '모자란 돈의 30%를\n내야 되고요', '2026년 겨울엔 타선 보강이 급해요': '2026년 겨울엔\n타선 보강이 급해요', '5위와 2경기 차까지 쫓아갔지만': '5위와 2경기 차까지\n쫓아갔지만', 'FA를 앞둔 두 선수의 연봉이 빠지면서': 'FA를 앞둔\n두 선수의 연봉이 빠지면서', '옵션과 2027년 연봉 인상이 빠진': '옵션과\n2027년 연봉 인상이 빠진', '삼성의 원태인과 구자욱 같은 최대어들이': '삼성의 원태인과 구자욱 같은\n최대어들이', '시장에 나올 특급 타자라는 분석인데': '시장에 나올\n특급 타자라는 분석인데', '롯데는 이동욱 감독과 이택근 단장으로': '롯데는\n이동욱 감독과 이택근 단장으로', '그래도 원태인과 구자욱의 연봉이': '그래도\n원태인과 구자욱의 연봉이', '비FA 다년계약 선수들이 FA로 풀리고': '비FA 다년계약 선수들이\nFA로 풀리고', '2025년 겨울에 2년 26억에 삼성으로 와서': '2025년 겨울에\n2년 26억에 삼성으로 와서', '2025년 겨울에 2년 22억에 SSG로 왔고': '2025년 겨울에\n2년 22억에 SSG로 왔고', '이렇게 나가고 들어온 돈을 합치면': '이렇게 나가고\n들어온 돈을 합치면', '기아의 남은 돈은 59억 5천만 원이에요': '기아의 남은 돈은\n59억 5천만 원이에요', '박찬호를 4년 80억에 데려왔는데': '박찬호를\n4년 80억에 데려왔는데', '2026년 10월에 이동욱 감독과 이택근 단장으로': '2026년 10월에\n이동욱 감독과 이택근 단장으로', '길어봤자 3~4년 뒤엔 야구를 그만할 생각이라고 했죠': '길어봤자 3~4년 뒤엔\n야구를 그만할 생각이라고 했죠', '내년엔 건강한 모습으로 돌아오겠다고 했어요': '내년엔 건강한 모습으로\n돌아오겠다고 했어요', '내부 선수에게 먼저 기회를 줄 것으로 보여요': '내부 선수에게\n먼저 기회를 줄 것으로 보여요', '그래도 비FA 다년계약을 맺었던 선수들이': '그래도\n비FA 다년계약을 맺었던 선수들이', '2027년에 나갈 연봉을 계산해 봤어요': '2027년에 나갈 연봉을\n계산해 봤어요', '외국인을 뺀 구단 연봉 상위 40명의 합계에': '외국인을 뺀 구단 연봉\n상위 40명의 합계에', '2024년 겨울부터 FA에 228억을 쓴': '2024년 겨울부터\nFA에 228억을 쓴', '연수로 나눈 1년 몫으로 셌어요': '연수로 나눈\n1년 몫으로 셌어요', '한국시리즈가 끝난 뒤에 공시돼서': '한국시리즈가 끝난 뒤에\n공시돼서', '2024년부터 FA에 228억을 쓴': '2024년부터\nFA에 228억을 쓴', '두산은 2026년 5위에 올랐지만': '두산은\n2026년 5위에 올랐지만', '와일드카드 결정전에서 탈락했는데': '와일드카드 결정전에서\n탈락했는데', '두산이 구자욱 영입전에 뛰어들지가': '두산이 구자욱 영입전에\n뛰어들지가', '키움은 18억 8천만 원이 모자라요': '키움은\n18억 8천만 원이 모자라요', '다만 옵션과 연봉 인상이 빠진 추정이라': '다만 옵션과 연봉 인상이\n빠진 추정이라', '2026년까지 4년 연속 최하위': '2026년까지\n4년 연속 최하위', 'FA를 앞둔 원태인과 구자욱의 연봉이': 'FA를 앞둔\n원태인과 구자욱의 연봉이', '다음 차례는 원태인과 구자욱이라고 했지만': '다음 차례는\n원태인과 구자욱이라고 했지만', '아직 도전이 끝나지 않았다고 했고': '아직 도전이\n끝나지 않았다고 했고', '두 선수와 다년계약을 하고 싶다고 했지만': '두 선수와\n다년계약을 하고 싶다고 했지만', '다른 팀의 좋은 조건을 마다하고': '다른 팀의 좋은 조건을\n마다하고'}   # 11/5 검수: 직접 정한 꺾임
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
        # 11/14 검수: 의존명사·보조용언 앞, 한 글자 낱말 뒤, 조사 없는 명사 뒤(명사+명사 가운데)에서는 꺾지 않는다
        if BAD_B2.match(y) or re.search(r'(?:^| )[가-힣]$', x): sc += 300
        elif not JOSA_END.search(x): sc += 80
        if sc < bs: best, bs = x + '\n' + y, sc
    if not best or bs >= 300: print('  자막 꺾기 확인:', t, '→', best); best = best or wrap(t)
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