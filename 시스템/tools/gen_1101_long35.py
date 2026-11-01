# -*- coding: utf-8 -*-
"""11/1 롱폼㉟ 「한국시리즈 KT — 22일 쉰 1위팀, 통합우승 확률은?」 콘티 (집 PC · 음성 API).
대사 = tools/text_1101_long35.py. 근거 = KBO 기록실(팀·선수 기록, 상대전적) + 기사 원문(1101 근거모음).
화면: 글자만 장면 ✗ — 모션그래픽(연표·승패 칸·순위 띠·투수 기록판·두 사진 비교·확률 계산판)으로만.
실행: python -X utf8 tools/gen_1101_long35.py → episodes/2026-11-01_롱폼.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t35', os.path.join(HERE, 'text_1101_long35.py'))
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
P = {
    "대니엘": "경기/대니엘_역투_스포츠경향", "고영표": "경기/고영표_투구_1011_KT제공",
    "힐리어드": "경기/힐리어드_포효_KT제공_1280", "힐리어드B": "경기/힐리어드_타격_1011_KT제공", "최원준": "경기/최원준_역전타_KT제공",
    "이강철": "경기/이강철_덕아웃_KT제공", "김현수": "경기/김현수_송구_1006_KT제공",
    "후라도": "경기/후라도_박수_삼성제공_세로", "후라도B": "카드/P20_후라도_투구", "원태인": "경기/원태인_투구_0828_삼성제공_세로",
    "최원태": "경기/최원태_경기_삼성제공_세로", "디아즈": "카드/FA9_디아즈_경기", "최형우": "경기/최형우_만루포미소_0826_삼성제공_세로",
    "김재윤": "경기/김재윤_투구_1007_삼성제공", "김영웅": "상황별/김영웅_적시타_1026_삼성제공",
    "네일": "카드/P17_네일_역투", "올러": "카드/P18_올러_포효", "올러B": "카드/P18_올러_투구", "김도영": "카드/P22_김도영_포효_중앙", "이범호": "경기/이범호_박수_0915_KIA제공_세로", "이강철B": "경기/이강철_상체_스포츠조선", "고영표B": "경기/고영표_상체_1011_KT제공", "대니엘B": "경기/대니엘_주먹_KT제공", "김도영C": "카드/G18_김도영_45호", "김도영D": "카드/P17_김도영_질주", "힐리어드C": "경기/힐리어드_하이파이브_1011_KT제공", "원태인B": "경기/원태인_역투_삼성제공", "네일B": "경기/네일_역투_KIA제공", "이승민": "카드/P31_이승민_삼성제공", "전상현": "경기/전상현_투구_1012_KIA제공", "조상우": "상황별/조상우_KIA_얼굴", "페덱": "경기/페덱_포효_연합뉴스", "페덱B": "경기/페덱_환호_삼성제공", "양현종": "경기/양현종_글러브_1012_KIA제공_세로", "스기모토": "경기/스기모토_역투_스포츠경향", "최원태B": "경기/최원태_경기_삼성제공", "최원태C": "상황별/최원태_KIA전_0908_삼성제공", "후라도C": "경기/후라도_경기_1019_삼성제공", "원태인C": "경기/원태인_포효_스타뉴스", "대니엘C": "카드/FA9원_대니엘", "올러C": "카드/P18_올러_환호", "양현종P": "경기/양현종_글러브_1012_KIA제공", "시라카와": "경기/시라카와_투구_KIA제공",
}
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

# 정규시즌 1위 팀 2015~2025 (우승 9 · 준우승 2)
YL = [(2015, "삼성", "bad"), (2016, "두산", "good"), (2017, "KIA", "good"), (2018, "두산", "bad"), (2019, "두산", "good"), (2020, "NC", "good"),
      (2021, "KT", "good"), (2022, "SSG", "good"), (2023, "LG", "good"), (2024, "KIA", "good"), (2025, "LG", "good")]
def YLINE(colored, at_items, **k):
    its = [dict(y=y, team=t, label=str(y), at=at_items, **({"c": c} if colored == 'all' or (colored == 'bad' and c == 'bad') else {})) for y, t, c in YL]
    return S(0, "yearline", title="정규시즌 1위 팀의 한국시리즈", **{"from": 2014.5, "to": 2025.5}, items=its, chain="yl", noCenter=True, **k)
PO = [("1차전", "대구", "삼성", "KIA"), ("2차전", "대구", "삼성", "삼성"), ("3차전", "광주", "KIA", "삼성"), ("4차전", "광주", "KIA", "KIA")]

SC = {}
# ── 오프닝 ──
SC['o1'] = HERO("힐리어드", "", "KT", "KT 위즈 · 2026 정규시즌 1위", [ST("한국시리즈", "통합 우승?", 1.0, True, size=130)], focus="50% 15%")
SC['o2'] = TL("KT의 한국시리즈", [dict(d="정규시즌 90승", t="1위 직행", c="good", at=0.2), dict(d="11월 3일 · 수원", t="한국시리즈 1차전", c="gold", at=1.0)])
SC['o3'] = TL("KT의 공식 경기 공백", [dict(d="10월 12일", t="정규시즌 마지막 경기", at=0.1), dict(d="첫 공식 경기", t="한국시리즈", c="gold", at=1.8)], text="공식 경기 없이 22일", textAt=1.0)
_poc = ["1차전", "2차전", "3차전", "4차전", "5차전"]
def _pob(ats, a5, big_at, foot_at, **k):
    cells = [dict(t=w, team=w, at=a) for (n, v, h, w), a in zip(PO, ats)] + [dict(t="?", at=a5, c="#FFB020")]
    return BOARD(None, big=BIG("삼성", "?" if big_at == 50 else 2, "KIA", "?" if big_at == 50 else 2, 0 if big_at == 50 else big_at), cols=_poc, rows=[dict(k="플레이오프", cells=cells)], **({"foot": dict(t="5차전 · 11월 1일 대구", at=foot_at)} if foot_at is not None else {}), **k)
SC['o4'] = _pob([50] * 4, 50, 50, None, chain="o4")
SC['o4b'] = _pob([0.1, 0.2, 0.3, 0.4], 1.0, 0, 1.0, chain="o4", cont=True)
SC['o5'] = S(0, "toc", itemFrom=1)
# ── 1. 역대 1위 직행팀 ──
SC['h1'] = YLINE(None, 1.0)
SC['h2'] = dict(YLINE('good_only', -1, cont=True), title="1위 팀 11번 중 9번 우승")
SC['h2']['items'] = [dict(it, c='good') if it['label'] not in ('2015', '2018') else it for it in SC['h2']['items']]
SC['h3'] = dict(YLINE('all', -1, cont=True), title="1위 팀 11번 중 9번 우승 · 81.8%")
SC['h4'] = SER("2015년 한국시리즈 · 삼성 vs 두산", [G("1차전", "대구", "삼성", "삼성", 3.0), G("2차전", "대구", "삼성", "두산", 3.1), G("3차전", "잠실", "두산", "두산", 3.2), G("4차전", "잠실", "두산", "두산", 3.3), G("5차전", "잠실", "두산", "두산", 3.4)], brace=dict(label="주축 투수 세 명 이탈", team="삼성", at=1.0))
SC['h5'] = TL("2018년 한국시리즈 · 두산", [dict(d="2018년", t="두산 정규시즌 93승", at=1.0), dict(d="한국시리즈", t="SK에 2승 4패", c="bad", at=2.0), dict(d="6차전 연장 13회", t="홈런 한 방", c="bad", at=3.0)])
SC['h6'] = SCALE("휴식 일수와 우승", dict(label="오래 쉬고 나온 1위 팀"), dict(label="짧게 쉬고 나온 1위 팀"), 0)
SC['h7'] = BARS("14일~25일 만의 한국시리즈", [dict(label="21일 만에", sub="다섯 팀 중", value=3, max=5, unit="/5팀 우승", at=4.3),
                                     dict(label="24일 · 25일 만에", sub="두 팀 중", value=2, max=2, unit="/2팀 우승", at=6.3)], 5)
SC['h8'] = SER("2017년 한국시리즈 · KIA vs 두산", text="22일 만에 한국시리즈", textAt=0, games=[G("1차전", "광주", "KIA", "두산", 2.0), G("2차전", "광주", "KIA", "KIA", 3.0), G("3차전", "잠실", "두산", "KIA", 3.15), G("4차전", "잠실", "두산", "KIA", 3.3), G("5차전", "잠실", "두산", "KIA", 3.45)])
SC['h9'] = BARS("1위 팀의 한국시리즈", [dict(label="1차전 패배 뒤 우승", sub="네 팀 중", value=3, max=4, unit="/4팀", at=1.0),
                                  dict(label="4전 전승 우승", sub="11번 중", value=3, max=11, unit="/11번", at=3.0, hi=True)], 4)
SC['h10'] = SCALE("1위 팀의 한국시리즈", dict(label="우승", chips=["대부분"]), dict(label="놓친 이유", chips=["주축 이탈", "상대의 한 방"]), 8)
SC['h11'] = Q("두 번의 공통점은?", ["삼성", "두산"], logoSize=200, size=104)
SC['k1'] = S(0, "podium", title="2026 정규시즌 최종 순위", items=[dict(medal="금", team="KT", hi=True), dict(medal="은", team="삼성"), dict(medal="동", team="KIA")], noName=True, noCenter=True)
SC['k2'] = S(0, "ring10", title="90승 5무 49패 · 마지막 10경기", items=[dict(team="KT", w=10, l=0, at=2.0)], noCenter=True)
SC['k2b'] = BARS("KT의 정규시즌 승수", [dict(label="2021년 · 첫 우승", value=76, unit="승", at=1.0), dict(label="2026년", value=90, unit="승", at=1.6, hi=True)], 100,
                 text="+14승", textAt=1.7)
SC['k3'] = RS("2026 KT 타선 · 리그 순위", [dict(k="팀 타율", v="1위", rank=1, at=1.0), dict(k="팀 득점", v="1위", rank=1, at=1.2)], chain="ktr")
SC['k4'] = RL("2026 KT 타선", [PL("힐리어드", "힐리어드", "KT", "타점왕", "run", 0.1), PL("최원준", "최원준", "KT", "득점왕", "run", 1.0)],
              [TA("힐리어드 타점", 139, 0.3, True), TA("최원준 득점", 125, 1.2)])
SC['k4b'] = HERO("힐리어드B", "힐리어드", "KT", "2026 정규시즌", [ST("홈런", "44개", 1.0), ST("홈런 순위", "2위", 1.0, True)], chain="hl")
SC['k4c'] = HERO("힐리어드B", "힐리어드", "KT", "2026 정규시즌 · 10월 28일 인터뷰", [ST("홈런", "44개", -1), ST("홈런 순위", "2위", -1, True)], quote=dict(t="“상대 팀 투수들에 따른\n맞춤 전략을 준비하고 있다”", at=1.0), chain="hl", cont=True)
SC['k5'] = RS("2026 KT 타선 · 리그 순위", [dict(k="팀 타율", v="1위", rank=1, at=-1), dict(k="팀 득점", v="1위", rank=1, at=-1), dict(k="팀 홈런", v="121개", rank=7, at=0.2)], chain="ktr2")
SC['k6'] = HERO("고영표", "고영표", "KT", "2026 정규시즌", [ST("승리", "15승", 1.0, True)], stamp=dict(t="공동 다승왕", at=2.0))
SC['k6b'] = BARS("KT 마무리 · 2026 정규시즌", [dict(label="세이브", value=30, unit="개", at=0.3, color=TC("KT"))], 35, text="평균자책점 2.48", textAt=1.0)
SC['k7'] = TL("KT 외국인 투수 교체", [dict(d="7월 말", t="교체 결정", at=0.2), dict(d="7승 투수", t="방출", c="bad", at=1.0)], chain="kt7")
SC['k7b'] = TL("KT 외국인 투수 교체", [dict(d="7월 말", t="교체 결정", at=-1), dict(d="7승 투수", t="방출", c="bad", at=-1), dict(d="구단 설명", t="“1선발로서 임팩트가 없었다”", c="gold", at=0.2)], chain="kt7", cont=True)
SC['k8a'] = HERO("대니엘", "대니엘", "KT", "KT 새 외국인 투수", [], chain="dn")
SC['k8'] = HERO("대니엘", "대니엘", "KT", "2026 정규시즌", [ST("10경기", "5승 2패", 1.0), ST("평균자책점", "2.13", 2.0, True)], stamp=dict(t="1차전 선발 유력", at=3.0), chain="dn", cont=True)
SC['k9'] = HERO("대니엘", "대니엘", "KT", "10월 27일 · 상무 연습경기", [ST("이닝", "5이닝", 1.0), ST("피안타", "0개", 2.0, True), ST("삼진", "10개", 2.0)], chain="dn", cont=True)
SC['k9b'] = HERO("대니엘", "대니엘", "KT", "10월 27일 · 상무 연습경기", [ST("이닝", "5이닝", -1), ST("피안타", "0개", -1, True), ST("삼진", "10개", -1)], quote=dict(t="“한국시리즈 1선발 영광이\n주어진다면 정말 기쁠 것”", at=1.0), stamp=dict(t="커리어 첫 포스트시즌", at=3.0), chain="dn", cont=True)
_g21 = lambda w_at, title="2021 한국시리즈 · KT vs 두산", **k: SER(title, [G("1차전", "고척", "KT", "KT" if w_at is not None else None, (w_at or 0)), G("2차전", "고척", "KT", "KT" if w_at is not None else None, (w_at or 0) + .1),
                                                  G("3차전", "고척", "두산", "KT" if w_at is not None else None, (w_at or 0) + .2), G("4차전", "고척", "두산", "KT" if w_at is not None else None, (w_at or 0) + .3)], chain="ks21", **k)
SC['k10'] = _g21(None)
SC['k11'] = _g21(3.7, cont=True, text="1위 결정전 승리 → 14일 만에 한국시리즈 → 4전 전승", textAt=1.0, brace=dict(label="창단 첫 통합 우승", team="KT", at=50))
SC['k11b'] = _g21(-1, cont=True, text="1위 결정전 승리 → 14일 만에 한국시리즈 → 4전 전승", textAt=-1, brace=dict(label="창단 첫 통합 우승", team="KT", at=1.0))
SC['k12'] = HERO("이강철", "이강철", "KT", "KT 감독", [ST("2021년", "통합 우승 사령탑", 1.0, True)])
SC['k13'] = SCALE("2026 KT 정리", dict(label="강점", chips=["타선", "마운드"]), dict(label="약점", chips=["장타", "중간 불펜", "1선발 첫 가을"]), 7)
SC['c1'] = Q("KT의 상대는?", ["삼성", "KIA"], logoSize=180)
SC['c2'] = BOARD(None, big=BIG("삼성", 2, "KIA", 2, 3.0), cols=_poc,
                rows=[dict(k="플레이오프", cells=[dict(t=w, team=w, at=a) for (n, v, h, w), a in zip(PO, [0.3, 1.0, 1.3, 2.0])] + [dict(t="?", at=3.0, c="#FFB020")])])
SC['c2b'] = RL("플레이오프 3차전 · 광주", [PL("최원태", "최원태", "삼성", "선발 · 일찍 강판", "out", 1.0), PL("원태인", "원태인", "삼성", "불펜 등판", "def", 2.0)], [TA("삼성", 6, 3.0, True), TA("KIA", 4, 3.0)])
SC['c2c'] = BOARD("플레이오프 4차전 · 광주", big=BIG("삼성", 2, "KIA", 4, 2.0, note="KIA 7회 상대 실책 뒤 3점"))
SC['c3'] = FO("5차전 선발 · 11월 1일 대구", side("후라도", "후라도", "삼성", "", 1.0), side("올러", "올러", "KIA", "", 1.0), [])
SC['c4'] = TL("플레이오프 승자의 일정", [dict(d="11월 2일", t="하루 휴식", c="bad", at=0.2), dict(d="11월 3일", t="한국시리즈 1차전", c="gold", at=1.0)])
SC['c4b'] = S(0, "faces", items=[dict(img=P["이강철B"], name="이강철", team="KT", role="감독 · 10월 30일", at=0, say="“누가 올라와도 좋으니\n5차전까지 하고 올라왔으면”", sayAt=1.0)], noCenter=True)
SC['c5'] = SER("플레이오프", [G(n, v, h, w, -1) for (n, v, h, w) in PO] + [G("5차전", "대구", "삼성", "?", -1)], chain="po2", text="두 팀 마운드 총력전", textAt=1.0)
SC['f1'] = BARS("4차전까지 마운드에 올린 투수", [dict(label="삼성", value=21, unit="번", at=1.0, color=TC("삼성")), dict(label="KIA", value=25, unit="번", at=2.0, color=TC("KIA"))], 30)
FC = lambda img, name, team, role, at, **x: dict(dict(img=P.get(img, img), name=name, team=team, role=role, at=at), **x)
SC['f2'] = HERO("이승민", "이승민", "삼성", "삼성 · 플레이오프", [ST("등판", "네 경기 모두", 0.5, True)])
SC['f3'] = HERO("전상현", "전상현", "KIA", "KIA 마무리", [ST("3차전과 4차전", "이틀 연속 등판", 1.0, True)])
SC['f4'] = FO("5차전 선발 두 명", side("후라도C", "후라도", "삼성", "", 1.0), side("올러B", "올러", "KIA", "", 1.0), [dict(k="한국시리즈", l="빨라야 3차전", r="빨라야 3차전", at=2.0)])
SC['f5'] = FO("4차전 선발 두 명", side("페덱", "페덱", "삼성", "", 0), side("네일B", "네일", "KIA", "", 0), [dict(k="1차전이면", l="사흘 휴식", r="사흘 휴식", at=1.0), dict(k="2차전이면", l="나흘 휴식", r="나흘 휴식", at=2.0)])
SC['f6'] = SCALE("한국시리즈 선발 순서", dict(label="KT", chips=["1차전부터 정상"]), dict(label="상대", chips=["에이스는 3차전부터"]), 8)
_sch = lambda ats, **k: TL("한국시리즈 일정", [dict(d="1 · 2차전", t="수원", c="gold", at=ats[0]), dict(d="하루", t="휴식", at=ats[1]), dict(d="3~5차전", t="상대 안방\n사흘 연속", c="bad", at=ats[2]),
                                            dict(d="하루", t="휴식", at=ats[3]), dict(d="6 · 7차전", t="수원", c="gold", at=ats[4])], chain="sch", **k)
SC['c8'] = _sch([1.0, 2.0, 3.5, 50, 50])
SC['c8b'] = _sch([-1, -1, -1, 0.1, 1.0], cont=True)
SC['c9'] = _sch([-1] * 5, cont=True, text="고비 ① 1차전 공백 · ② 3차전 상대 에이스 복귀", textAt=2.0, size=56)
SC['s1'] = Q("첫 번째 경우", ["삼성"], logoSize=220, size=104)
SC['s2'] = BOARD("2026 정규시즌 상대전적", big=BIG("KT", 7, "삼성", 9, 1.0, note="KT 기준 승 : 패"), foot=dict(t="상대 9개 팀 중 유일한 열세", at=2.5))
SC['s3'] = SCALE("지금의 삼성", dict(label="상대전적", chips=["KT 열세"]), dict(label="지금 전력", chips=["?"]), 0)
SC['s4'] = S(0, "faces", items=[FC("김재윤", "김재윤", "삼성", "세이브왕 · 부상 이탈", 0), FC("원태인B", "원태인", "삼성", "선발 → 마무리", 2.0)], noCenter=True)
SC['s4b'] = S(0, "faces", items=[FC("후라도B", "후라도", "삼성", "", 1.0), FC("페덱B", "페덱", "삼성", "", 1.2), FC("최원태C", "최원태", "삼성", "", 2.0)], noCenter=True)
SC['s4c'] = TL("삼성 선발 · 3~5차전은 연이어 사흘", [dict(d="3차전", t="후라도", at=0.2), dict(d="4차전", t="1차전 선발\n사흘 휴식", c="bad", at=2.5, big=True), dict(d="5차전", t="2차전 선발\n사흘 휴식", c="bad", at=3.0)])
SC['s4d'] = HERO("원태인C", "원태인", "삼성", "삼성의 고민", [ST("다시 선발로 돌리면", "뒷문 공백", 0.5, True)])
SC['s6'] = PLOG("후라도C", "후라도", "삼성", "2026 KT전", [LN(["경기", "세 경기", False], at=1.0), LN(["평균자책점", "5.17", True], at=2.0), LN(["피홈런", "4개", True], at=3.0)])
SC['s7'] = BARS("플레이오프 4차전 · 삼성 수비", [dict(label="실책", value=3, unit="개", at=1.0, color=RED)], 4)
SC['s8'] = HERO("고영표", "고영표", "KT", "2026 삼성전 · 네 경기", [ST("승패", "3승 1패", 2.0, True), ST("평균자책점", "2.25", 3.0, True)], focus="50% 20%", imgAt=1.0)
SC['s9'] = TL("마지막 세 번의 맞대결", [dict(d="", t="KT 승리", c="good", at=1.0), dict(d="", t="KT 승리", c="good", at=1.4), dict(d="", t="KT 승리", c="good", at=1.8)])
SC['s10'] = RL("삼성 타선 · 플레이오프", [PL("디아즈", "디아즈", "삼성", "삼성 거포", "run", 1.0), PL("최형우", "최형우", "삼성", "삼성 거포", "run", 1.15)], [TA("두 선수 플레이오프 홈런", 4, 3.0, True)])
SC['s11'] = SCALE("삼성이 오면", dict(label="상대전적 열세"), dict(label="선발 셋 · 사흘 휴식", chips=["열세를 메움"]), -3)
SC['a1'] = Q("두 번째 경우", ["KIA"], logoSize=220, size=104)
SC['a2'] = BOARD("2026 정규시즌 상대전적", big=BIG("KT", 10, "KIA", 6, 1.0, note="KT 기준 승 : 패"), chain="kia")
SC['a2b'] = BOARD("2026 정규시즌 상대전적", big=BIG("KT", 10, "KIA", 6, -1, note="KT 기준 승 : 패"), foot=dict(t="기록만큼 편하진 않은 상대", at=1.0), chain="kia", cont=True)
SC['a2c'] = S(0, "faces", items=[FC("네일B", "네일", "KIA", "", 0), FC("올러C", "올러", "KIA", "", 0.2), FC("시라카와", "시라카와", "KIA", "", 0.4)], noCenter=True)
SC['a4'] = HERO("양현종", "양현종", "KIA", "KIA · 네 번째 선발", [ST("플레이오프 4차전까지", "등판 없음", 0.5, True)], stamp=dict(t="1차전 카드?", at=2.5))
SC['a3'] = TL("KT vs KIA · 광주", [dict(d="9월 초 3연전", t="KIA 싹쓸이", c="bad", at=1.0), dict(d="한국시리즈 3~5차전", t="광주", c="gold", at=3.0)])
SC['a5'] = HERO("김도영", "김도영", "KIA", "KIA 타선", [ST("KT전 타율", "3할 6푼 8리", 2.0, True), ST("플레이오프", "16타수 7안타", 3.0, True)], stamp=dict(t="4차전부터 타순 두 번째", at=4.3))
SC['a6'] = BARS("2026 팀 홈런", [dict(label="KIA · 2위", value=174, unit="개", at=1.0, color=TC("KIA")), dict(label="KT · 7위", value=121, unit="개", at=2.0, color=TC("KT"))], 180, text="53개 차이", textAt=2.5)
SC['a6b'] = PLOG("네일", "네일", "KIA", "2026 KT전", [LN(["평균자책점", "4.67", True], at=1.0)])
SC['a7'] = PLOG("힐리어드B", "힐리어드", "KT", "2026 KIA전", [LN(["타율", "3할 4푼 8리", True], at=1.0), LN(["홈런", "6개", True], at=2.0)])
SC['a8'] = SCALE("KIA가 오면", dict(label="수원 네 경기"), dict(label="광주 3연전", chips=["분수령"]), -8)
SC['v1'] = S(0, "toc", on=3)
SC['v2'] = BARS("첫 번째 변수 · 공식 경기 공백", [dict(label="마지막 경기 → 1차전", value=22, unit="일", at=1.0, hi=True, color=RED)], 25)
SC['v3'] = S(0, "faces", items=[dict(img=P["이강철"], name="이강철", team="KT", role="감독 · 10월 27일", at=0, say="“유지가 아니라\n찾으라는 것이다”", sayAt=2.0)], noCenter=True)
SC['v4'] = TL("KT 연습경기", [dict(d="10월 27일", t="상무", at=0.2), dict(d="7대0", t="승리", c="good", at=1.0), dict(d="10월 28일", t="23세 이하 대표팀", at=2.2), dict(d="8대2", t="승리", c="good", at=3.6)])
SC['v4b'] = HERO("카드/G18_소형준_B", "소형준", "KT", "10월 30일 · 마지막 연습경기", [ST("역할", "선발 등판", 1.0)])
SC['v5'] = SCALE("휴식 길이와 시리즈 우승", dict(label="오래 쉬고 나온 1위 팀", chips=["대부분 우승"]), dict(label="짧게 쉬고 나온 1위 팀", chips=["마찬가지"]), 0)
SC['v5b'] = BARS("최근 11년 1위 팀의 승리", [dict(label="1차전", value=7, max=11, unit="/11번", at=1.8, color=RED), dict(label="2차전", value=9, max=11, unit="/11번", at=1.0, hi=True)], 11, text="1차전 승리가 더 적어요", textAt=2.0)
SC['v6'] = S(0, "faces", items=[dict(img=P["이강철B"], name="이강철", team="KT", role="감독 · 10월 27일", at=0, say="“두 경기 정도 … 타자들이 못 치면\n투수들로 버티는 것”", sayAt=1.5)], noCenter=True)
SC['v7'] = SCALE("두 번째 변수 · KT 마운드", dict(label="마무리", chips=["단단"]), dict(label="중간 불펜", chips=["약점"]), -8)
SC['v7b'] = HERO("스기모토", "스기모토", "KT", "2026 정규시즌 · 홀드왕", [ST("홀드", "25개", 0.3), ST("평균자책점", "5.90", 1.0, True)])
SC['v7c'] = TL("KT가 이기는 길", [dict(d="선발", t="길게 버티기", c="good", at=1.0), dict(d="마무리", t="바로 잇기", c="good", at=2.0)])
SC['v8'] = Q("세 번째 변수\n큰 경기 경험", ["KT"], logoSize=200, size=100)
SC['v8b'] = HERO("대니엘", "대니엘", "KT", "세 번째 변수 · 큰 경기 경험", [ST("포스트시즌", "처음", 1.0, True)], stamp=dict(t="첫 무대 변수", at=3.5))
SC['v8c'] = HERO("김현수", "김현수", "KT", "KT 위즈", [ST("한국시리즈 우승 반지", "세 개", 1.0, True)])
SC['v8d'] = BARS("상대의 큰 경기 경험", [dict(label="KIA 한국시리즈 우승", value=12, max=12, unit="/12번", at=1.0, color=TC("KIA"))], 12, text="삼성 · 2024년 한국시리즈", textAt=3.0)
SC['v8e'] = SCALE("세 번째 변수 · 큰 경기 경험", dict(label="KT", chips=["김현수"]), dict(label="상대", chips=["KIA · 삼성"]), 0)
SC['w1'] = Q("마지막 변수\n역대 기록 속 공통점", ["KT"], logoSize=200, size=96)
_wl = lambda ats, **k: TL("우승 놓친 두 번의 상대 · 5차전 뒤 하루 휴식", [dict(d="2015년 · 삼성", t="상대 두산", c="bad", at=ats[0]), dict(d="2018년 · 두산", t="상대 SK", c="bad", at=ats[1]),
                                                         dict(d="2026년 · KT", t="상대도\n같은 길", c="gold", at=ats[2], big=True)], chain="wl", **k)
SC['w2'] = _wl([2.0, 2.2, 50])
SC['w3'] = _wl([-1, -1, 0.3], cont=True)
SC['w4'] = BARS("2005년부터 · 5차전까지 치른 팀", [dict(label="5차전 치른 팀 우승", value=2, max=8, unit="/8번", at=2.0, color=GRAY)], 8, text="1위 팀을 꺾은 건 이 팀들뿐", textAt=3.0)
SC['w5'] = TL("1위 팀 안방 1·2차전", [dict(d="2015년 삼성", t="1승 1패", c="bad", at=1.0), dict(d="2018년 두산", t="1승 1패", c="bad", at=1.2)])
SC['w6'] = BARS("1·2차전 모두 잡은 1위 팀", [dict(label="우승", value=5, max=5, unit="/5번", at=1.0, color=GREEN)], 5)
SC['p1'] = Q("제 계산", ["KT"], logoSize=200, size=110)
SC['p2'] = TL("차전마다 KT 승리 확률", [dict(d=f"{i}차전", t="?", at=1.0 + (i - 1) * .12) for i in range(1, 8)])
SC['p2b'] = BARS("출발점 · 정규시즌 맞대결 승률", [dict(label="삼성전 7승 9패", value=43.75, dec=2, unit="%", at=1.0, color=TC("삼성")), dict(label="KIA전 10승 6패", value=62.5, dec=1, unit="%", at=3.0, color=TC("KIA"))], 100)
def _wS(steps, endv, end_at, title, **k):
    return S(0, "water", title=title, team="KT", min=35, max=55, dec=2, base=dict(v=43.75, k="출발점\n삼성전 맞대결", at=-1), steps=steps, end=dict(v=endv, k=title.split(" · ")[-1], at=end_at), noCenter=True, **k)
_g1 = lambda ats, end_at=50, **k: _wS([dict(k="수원 경기", d=4, at=ats[0]), dict(k="1차전 공백", d=-5, at=ats[1]), dict(k="상대 불펜 피로", d=3, at=ats[2]), dict(k="삼성 마무리 공백", d=3, at=ats[3])], 48.75, end_at, "예시 · 삼성 1차전", chain="wg1", **k)
SC['p3'] = _g1([0.2, 2.5, 50, 50])
SC['p3b'] = _g1([-1, -1, 0.5, 50], cont=True)
SC['p4'] = _g1([-1, -1, -1, 1.0], end_at=3.0, cont=True)
SC['p5'] = _wS([dict(k="원정", d=-4, at=-1), dict(k="삼성 마무리 공백", d=3, at=-1), dict(k="삼성 선발 사흘 휴식", d=6, at=1.0)], 48.75, 2.0, "예시 · 삼성 4차전")
NS = lambda n: dict(name=n)
def _mt(opp, rows, pcts, ats, res_at, ch_, **k):
    R_ = [dict(g=g_, v=v, L=NS(L_), R=NS(R2), pct=pc, at=a, vAt=b) for (g_, v, L_, R2), pc, (a, b) in zip(rows, pcts, ats)]
    return S(0, "matchtbl", l="KT", r=opp, title=("삼성이 오면 · 예상 선발" if opp == "삼성" else "KIA가 오면 · 예상 선발"), rows=R_,
             res=dict(t="KT 우승 확률", v=(53.84 if opp == "삼성" else 77.06), at=res_at, dec=2), chain=ch_, **k)
_MS = [("1차전", "수원", "대니엘", "최원태"), ("2차전", "수원", "고영표", "페덱"), ("3차전", "대구", "KT 선발", "후라도"), ("4차전", "대구", "KT 선발", "최원태 · 사흘"),
       ("5차전", "대구", "대니엘", "페덱 · 사흘"), ("6차전", "수원", "고영표", "후라도 · 사흘"), ("7차전", "수원", "KT 선발", "최원태 · 사흘")]
_PS = ["48.75", "56.75", "42.75", "48.75", "48.75", "59.75", "56.75"]
_MK = [("1차전", "수원", "대니엘", "양현종"), ("2차전", "수원", "고영표", "네일"), ("3차전", "광주", "KT 선발", "올러"), ("4차전", "광주", "KT 선발", "시라카와"),
       ("5차전", "광주", "대니엘", "양현종"), ("6차전", "수원", "고영표", "네일"), ("7차전", "수원", "KT 선발", "올러")]
_PK = ["64.5", "69.5", "58.5", "58.5", "58.5", "66.5", "66.5"]
SC['p6'] = _mt("삼성", _MS, [float(x) for x in _PS], [(0.1, 0.4), (0.15, 3.6), (0.2, 3.0), (0.25, 0.4), (0.3, 0.4), (0.35, 3.6), (0.4, 3.6)], 50, "mS")
SC['p6']['rows'] = [dict(r, pct=p_) for r, p_ in zip(SC['p6']['rows'], _PS)]
SC['p6b'] = _mt("삼성", _MS, _PS, [(-1, -1)] * 7, 1.0, "mS", cont=True)
SC['p7'] = _mt("KIA", _MK, _PK, [(0.1, 50), (0.15, 50), (0.2, 2.0), (0.25, 2.0), (0.3, 2.0), (0.35, 50), (0.4, 50)], 50, "mK")
SC['p8'] = _mt("KIA", _MK, _PK, [(-1, -1)] * 2 + [(-1, -1)] * 3 + [(-1, -1)] * 2, 50, "mK", cont=True)
for i in (0, 1, 5, 6): SC['p8']['rows'][i]['vAt'] = 1.0 if i in (0, 5, 6) else 2.0
SC['p8']['rows'][0]['vAt'] = 1.0
SC['p9b'] = _mt("KIA", _MK, _PK, [(-1, -1)] * 7, 1.0, "mK", cont=True)
SC['p10'] = S(0, "probpair", title="KT 통합 우승 확률", team="KT", items=[dict(team="삼성", label="삼성이 오면", v=53.84, at=-1, hi=True), dict(team="KIA", label="KIA가 오면", v=77.06, at=-1)], dec=2,
              text="최근 11년 1위 팀 81.8%보다 낮음", textAt=1.0, size=56, noCenter=True)
SC['p12'] = S(0, "ring10", title="삼성이 오면 · 가장 가능성 높은 결과", items=[dict(team="KT", w=4, l=2, at=3.0)], noCenter=True)
SC['p13'] = TL("삼성이 오면 · 분수령", [dict(d="3차전 · 대구", t="삼성 우세", c="bad", at=0.3, big=True), dict(d="4차전부터", t="삼성 선발 사흘 휴식", c="good", at=2.5)])
SC['p14'] = S(0, "ring10", title="KIA가 오면 · 가장 가능성 높은 결과", items=[dict(team="KT", w=4, l=2, at=1.5)], noCenter=True)
SC['p15'] = TL("KIA가 오면 · 분수령 광주 3연전", [dict(d=f"{i}차전", t="KT 58.5%", c="#8A93A3", at=1.0 + (i - 3) * .1, big=True) for i in (3, 4, 5)])
SC['q1'] = Q("공백 뒤 KT 통합 우승?\n아니면 플레이오프 승자?", ["KT", "삼성", "KIA"], logoSize=160, size=84, chain="q")   # 11/1 사용자 "뚝 끊기며 바뀌지 않게" — q1·q2 같은 화면 그대로
SC['q2'] = Q("공백 뒤 KT 통합 우승?\n아니면 플레이오프 승자?", ["KT", "삼성", "KIA"], logoSize=160, size=84, chain="q", cont=True)
for _k in list(SC): SC[_k] = dict(SC[_k], minDur=0.8)

for _k in [k for k in SC if k not in KEYS]: SC.pop(_k)
missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing and not extra, (missing, extra)
lines, scenes = [], []
for j, (k, narr, sub) in enumerate(_t.LINES):
    sc = dict(SC[k]); sc['startLine'] = j
    lines.append(L(narr, sub)); scenes.append(sc)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})

def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
CH = [ch("최근 11년 1위 팀", "h1", "h11"), ch("2026년 KT", "k1", "k13"), ch("삼성이 오면 · KIA가 오면", "c1", "a8"), ch("변수와 계산", "v1", "q2")]
DESC = ("정규시즌 1위 KT가 22일 만에, 11월 3일 수원에서 한국시리즈 1차전을 치러요. 상대는 11월 1일 대구 플레이오프 5차전(삼성 후라도 vs 기아 올러)의 승자예요.\n"
        "최근 11년 정규시즌 1위 팀은 11번 중 9번 우승(81.8%)했어요. 그런데 우승을 놓친 두 번(2015년 삼성·2018년 두산)은 모두 상대가 플레이오프 5차전을 치르고 하루만 쉬고 올라온 해였고, 2026년 KT의 상대도 같은 길로 올라와요.\n\n"
        "지금 상황: 4차전까지 삼성은 투수를 21번, 기아는 25번 마운드에 올렸어요. 5차전 선발 후라도·올러는 빨라야 한국시리즈 3차전, 4차전 선발 페덱·네일은 1차전이면 사흘 휴식이에요. KT는 1차전부터 선발이 정상 순서로 돌아가요.\n"
        "삼성이 오면: 정규시즌 KT 7승 9패(유일한 열세)지만 세이브왕 김재윤이 빠져 원태인이 뒷문으로 갔고, 남은 선발은 후라도·페덱·최원태 셋. 3~5차전이 사흘 연속이라 4차전부터는 선발 셋이 사흘씩만 쉬고 돌아가야 해요. 후라도 KT전 평균자책점 5.17, 고영표 삼성전 3승 1패 2.25. 다만 디아즈·최형우가 플레이오프 홈런 4개.\n"
        "기아가 오면: 정규시즌 KT 10승 6패지만 기아는 선발 카드가 네 장(네일·올러·시라카와·양현종)이고, 양현종은 4차전까지 플레이오프 등판이 없어요. 9월 초 광주 3연전은 기아 싹쓸이, 한국시리즈 3~5차전이 광주예요. 김도영 KT전 3할 6푼 8리·플레이오프 16타수 7안타.\n\n"
        "변수: 휴식 길이는 우승을 가르지 못했지만 첫 경기는 조금 달라요(최근 11년 1위 팀 1차전 11번 중 7승, 2차전 9승). KT 마무리는 단단하지만 그 앞 불펜이 약점(홀드왕 스기모토 평균자책점 5.90). 큰 경기 경험은 양쪽 다 있어 중립.\n"
        "제 계산: 차전마다 KT가 이길 확률을 따로 셌어요. 출발점은 올해 정규시즌 맞대결 승률(삼성전 7승 9패 43.75%, 기아전 10승 6패 62.5%)이고, 수원 경기 +4·원정 −4, 1차전 공백 −5, 상대 불펜이 지친 1·2차전 +3, 삼성 마무리 공백 +3, 삼성에 강했던 KT 2선발이 나설 2·6차전 +3, 삼성 선발이 사흘만 쉬고 나오는 4차전부터 +6을 더하고 빼서 7전 4선승을 계산했어요.\n"
        "→ 삼성이 오면 KT 우승 확률 53.84%(1·4·5차전 48.75%, 대구 3차전 42.75%로 오히려 삼성이 앞섬), 기아가 오면 77.06%. 둘 다 최근 11년 1위 팀 우승 비율 81.8%보다 낮고, 삼성이 오면 1위 팀인데도 사실상 반반 승부예요.\n"
        "제 예상: 삼성이 오면 가장 가능성 높은 결과는 KT 4승 2패지만 7차전까지 갈 확률 31.46%(분수령 대구 3차전), 기아가 오면 KT 4승 2패(분수령 광주 3연전, 세 경기 모두 KT 58.5%).\n\n"
        "KT가 22일 만의 실전을 딛고 통합 우승을 할까요? 아니면 플레이오프를 뚫고 온 팀이 KT를 넘을까요? 댓글로 알려 주세요.\n\n"
        "#한국시리즈 #KT위즈 #삼성라이온즈 #기아타이거즈 #통합우승 #프로야구 #KBO #야구자판기\n\n"
        "기록 출처: KBO 기록실(2026 정규시즌 팀·선수 기록, 팀간 승패, 역대 한국시리즈)\n"
        "기사 출처: OSEN·아주경제·미디어펜 10/31(한국시리즈 일정), 데일리안 10/31·청년일보 10/30(플레이오프 투수 운용), 스포티비 10/31(이승민), 일간스포츠 10/28·한국아이닷컴 10/30(원태인), OSEN 10/31·MK스포츠 10/29(기아 불펜), 일간스포츠 10/31·데일리안 10/31(한국시리즈 선발 전망), 스포티비 10/30(삼성 4차전 실책), 일간스포츠 10/30·한국아이닷컴 10/30(양현종 대기), 일간스포츠 10/31(김도영), 스타뉴스·뉴스핌 10/27(상무 연습경기), 엑스포츠뉴스 10/28·스포츠경향 10/30(연습경기·선발 구상), 머니투데이 10/27(이강철 감독), 엑스포츠뉴스 10/16·파이낸셜뉴스 10/8(스기모토), 트위그 9/7(9월 광주 3연전), 스포츠월드 10/23(김현수), 뉴스1·머니투데이 10/24(김재윤)\n"
        "사진 출처: KT 위즈 제공, 삼성 라이온즈 제공, 기아 타이거즈 제공, 스포츠경향, 스포츠조선, 스타뉴스, 연합뉴스, KBO")
TAGS = ["한국시리즈", "한국시리즈 1차전", "KT 위즈", "삼성 라이온즈", "기아 타이거즈", "통합우승", "한국시리즈 예측", "한국시리즈 분석", "플레이오프 5차전", "대니엘", "고영표", "후라도", "원태인", "김재윤", "양현종", "올러", "네일", "김도영", "이강철", "프로야구", "KBO", "야구자판기"]
SOURCE = "사실 출처 = KBO 기록실 + 기사 원문 — claude/1101-롱폼35-KT한국시리즈-근거모음.md"
EP = {"introChapter": "오프닝", "date": "2026-11-01", "gameDate": "2026-10-30", "series": "야구롱폼", "focusTeam": "KT", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.15,
      "rev": "1101-long35-v1", "topic": "한국시리즈KT우승확률", "endcardSec": 10, "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "한국시리즈 KT | 22일 쉰 1위팀, 통합우승 확률은? 삼성이면 / 기아면 #한국시리즈 #KT #삼성 #기아", "description": DESC, "tags": TAGS, "hashtags": ["#한국시리즈", "#KT위즈", "#삼성라이온즈", "#기아타이거즈", "#통합우승", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'q1', 'q2')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    _gf = os.path.join(HERE, 'gapfix_1101_long35.json')
    if os.path.exists(_gf):
        for _k, _g in json.load(open(_gf, encoding='utf-8')).items(): EP['lines'][KEYS.index(_k)]['gapAfter'] = max(EP['lines'][KEYS.index(_k)].get('gapAfter', 0.25), _g)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-01_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
