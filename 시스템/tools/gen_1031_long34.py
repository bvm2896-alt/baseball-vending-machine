# -*- coding: utf-8 -*-
"""10/31 롱폼㉞ 「플레이오프 4차전 리뷰 · 5차전 승부예측」 콘티 (노트북 · 음성 API · GPU 없음).
대사 = tools/text_1031_long34.py (독립 검수 통과본). 근거 = KBO 기록실(4차전 박스스코어·선수 일자별·팀 수비) + 기사 원문.
화면: 글자만 장면 ✗ — 점수 흐름은 scoreboard, 선발 비교는 duel/bars, 구장별 성적은 bars, 실책은 cells, 투수 이어 던지기는 people.
실행: python -X utf8 tools/gen_1031_long34.py → episodes/2026-10-31_롱폼.json"""
import json, os, re, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t34', os.path.join(HERE, 'text_1031_long34.py'))
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

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
RED, GOLD, GRAY, GREEN = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55"

# ── 사진 (노트북 선수이미지 은행에서 확인한 파일만) ──
P = {
    "한준수": "카드/P18_한준수_세리머니", "한준수B": "카드/P22_한준수_솔로", "김도영": "카드/P17_김도영_질주", "김도영B": "카드/P22_김도영_포효_중앙",
    "최형우": "경기/최형우_만루포미소_0826_삼성제공_세로", "최형우B": "경기/최형우_100타점_0918_삼성제공_중앙_세로",
    "후라도": "경기/후라도_박수_삼성제공_세로", "후라도B": "카드/P20_후라도_투구", "올러": "경기/올러_경기_KIA제공_세로", "올러B": "카드/P18_올러_투구",
    "페덱": "카드/P22_페덱_투구", "네일": "카드/P17_네일_역투", "사토시": "카드/FA9끝_미야모리", "김영웅": "상황별/김영웅_적시타_1026_삼성제공", "박승규": "상황별/박승규_타격_0830_삼성제공", "이승민": "카드/P31_이승민_삼성제공", "원태인": "경기/원태인_투구_0828_삼성제공_세로", "김태훈": "카드/FA10_김태훈", "배찬승": "KBO프로필/배찬승",
    "류지혁": "카드/G18_류지혁_A", "강민호": "상황별/강민호_3점포_중앙", "디아즈": "카드/FA9_디아즈_경기", "나성범": "카드/P18_나성범_적시타",
    "카스트로": "카드/P18_카스트로_환호", "김선빈": "카드/P17_김선빈", "하주석": "카드/P22_하주석_타격",
    "조상우": "카드/FA10_조상우", "전상현": "카드/P18_전상현_역투", "박진만": "경기/박진만_박수_0908_삼성제공_세로", "최원태": "경기/최원태_경기_삼성제공_세로",
}
def pv(img, name, sub, viz, **k): return S(0, "pstat", img=P.get(img, img), name=name, sub=sub, stats=k.pop("stats", []), viz=viz, noCenter=True, **k)
def pvt(team, name, sub, viz, **k): return S(0, "pstat", img=None, team=team, name=name, sub=sub, stats=k.pop("stats", []), viz=viz, noCenter=True, **k)
def pc(img, name, team, note="", **x): return dict({"img": P.get(img, img), "name": name, "team": team, "note": note}, **x)

# 4차전 점수판 — 이어지는 장면은 같은 틀(chain)에서 강조 이닝·표시만 바뀜
SS4 = [0, 1, 0, 0, 0, 1, 0, 0, 0]; KIA4 = [0, 0, 0, 1, 0, 0, 3, 0, None]
def box(hi=(), marks=(), upto=9, label=None, labelAt=0.5, text=None, textAt=0.5, cont=True, **k):
    sr = [v if j < upto else None for j, v in enumerate(SS4)]; kr = [v if j < upto else None for j, v in enumerate(KIA4)]
    rs = sum(v for v in sr if v); rk = sum(v for v in kr if v)
    d = dict(title="플레이오프 4차전 · 광주", rows=[{"team": "삼성", "runs": sr, "r": rs}, {"team": "KIA", "runs": kr, "r": rk, "hi": True}], hi=list(hi), marks=list(marks), chain="box4")
    if label: d.update(label=label, labelAt=labelAt)
    if text: d.update(text=text, textAt=textAt)
    if cont: d['cont'] = True
    d.update(k)
    return S(0, "scoreboard", **d)

SC = {}
# ── 오프닝 ──
SC['o1'] = box(cont=False, label="KIA 4대2 승 · 시리즈 2승 2패", labelAt=2.0)
SC['o2'] = S(0, "matchup", left="삼성", right="KIA", score="2 : 2", text="플레이오프 5차전 · 대구", tag="한국시리즈행 마지막 경기")
SC['o3'] = S(0, "matchup", left="삼성", right="KIA", score="2 : 2", text="이긴 팀 → 한국시리즈 vs KT", tag="한국시리즈행 마지막 경기", cont=True)
SC['o4'] = S(0, "toc", on=-1, itemFrom=1)
# ── ① 4차전 승부처 ──
SC['g1'] = box(hi=[2], upto=2, cont=False, marks=[dict(row=0, inn=2, label="선취점", at=1.0)])
SC['g2'] = S(0, "people", title="2회 · 삼성 공격", items=[pc("강민호", "강민호", "삼성", "연속 안타", at=1.0), pc("류지혁", "류지혁", "삼성", "우전 적시타", at=50)], size=110, chain="g2p")
SC['g3'] = S(0, "people", title="2회 · 삼성 공격", items=[pc("강민호", "강민호", "삼성", "연속 안타", at=-1), pc("류지혁", "류지혁", "삼성", "우전 적시타", at=0.3)], size=110, chain="g2p", cont=True, text="삼성 1대0", textAt=1.0)
SC['g4'] = box(hi=[4], upto=4, marks=[dict(row=0, inn=2, label="선취점", at=-1), dict(row=1, inn=4, label="동점", at=1.0)])
SC['g5'] = S(0, "people", title="4회 · KIA 공격", items=[pc("김도영", "김도영", "KIA", "우중간 2루타", at=0.3), pc("나성범", "나성범", "KIA", "몸에 맞는 공", at=1.0), pc("한준수", "한준수", "KIA", "좌익선상 적시타", at=50)], size=100, chain="g5p")
SC['g6'] = S(0, "people", title="4회 · KIA 공격", items=[pc("김도영", "김도영", "KIA", "우중간 2루타", at=-1), pc("나성범", "나성범", "KIA", "몸에 맞는 공", at=-1), pc("한준수", "한준수", "KIA", "좌익선상 적시타", at=0.2)], size=100, chain="g5p", cont=True, text="1대1", textAt=1.0)
SC['g7'] = box(hi=[6], upto=6, marks=[dict(row=1, inn=4, label="동점", at=-1), dict(row=0, inn=6, label="홈런", at=1.0)])
SC['g8'] = pv("최형우", "최형우", "삼성 좌익수 · 6회", [vstamp("솔로 홈런", 1.0, "gold", size=56)], stats=[st("상대 투수", "곽도규", 0.3)])
SC['g9'] = pv("최형우", "최형우", "삼성 좌익수 · 6회", [vstamp("솔로 홈런", -1, "gold", size=56)], stats=[st("상대 투수", "곽도규", -1), st("이번 플레이오프", "2호 홈런", 1.0, hi=True)], cont=True)
SC['g10'] = box(hi=[6], upto=6, marks=[dict(row=0, inn=6, label="홈런", at=-1)], text="삼성 2대1", textAt=0.3)
SC['g11'] = box(hi=[7], upto=6, marks=[dict(row=0, inn=6, label="홈런", at=-1)], text="마지막 승부처", textAt=1.0)
SC['g11b'] = box(hi=[7], upto=6, marks=[dict(row=0, inn=6, label="홈런", at=-1)], text="7회 · KIA 공격", textAt=0.3)
SC['g12'] = S(0, "rally", title="7회말 · KIA 공격", team="KIA", bug=dict(score=[1, 2], outs=0), plays=[dict(t="김영웅 실책 · 김도영 출루", at=50), dict(t="카스트로 안타 · 동점", at=50), dict(t="김선빈 중전 안타", at=50), dict(t="한준수 우전 적시타 · 역전", at=50), dict(t="하주석 안타 · 4대2", at=50)], chain="r7")
SC['g13'] = S(0, "rally", title="7회말 · KIA 공격", team="KIA", bug=dict(score=[1, 2], outs=0), plays=[dict(t="김영웅 실책 · 김도영 출루", at=1.0), dict(t="카스트로 안타 · 동점", at=50), dict(t="김선빈 중전 안타", at=50), dict(t="한준수 우전 적시타 · 역전", at=50), dict(t="하주석 안타 · 4대2", at=50)], chain="r7", cont=True)
SC['g14'] = S(0, "rally", title="7회말 · KIA 공격", team="KIA", bug=dict(score=[2, 2], outs=0), plays=[dict(t="김영웅 실책 · 김도영 출루", at=-1), dict(t="카스트로 안타 · 동점", at=0.3), dict(t="김선빈 중전 안타", at=50), dict(t="한준수 우전 적시타 · 역전", at=50), dict(t="하주석 안타 · 4대2", at=50)], chain="r7", cont=True)
SC['g15'] = S(0, "rally", title="7회말 · KIA 공격", team="KIA", bug=dict(score=[3, 2], outs=2), plays=[dict(t="김영웅 실책 · 김도영 출루", at=-1), dict(t="카스트로 안타 · 동점", at=-1), dict(t="김선빈 중전 안타", at=0.2), dict(t="한준수 우전 적시타 · 역전", at=2.0), dict(t="하주석 안타 · 4대2", at=50)], chain="r7", cont=True)
SC['g16'] = S(0, "rally", title="7회말 · KIA 공격", team="KIA", bug=dict(score=[4, 2], outs=2), plays=[dict(t="김영웅 실책 · 김도영 출루", at=-1), dict(t="카스트로 안타 · 동점", at=-1), dict(t="김선빈 중전 안타", at=-1), dict(t="한준수 우전 적시타 · 역전", at=-1), dict(t="하주석 안타 · 4대2", at=1.0)], chain="r7", cont=True)
SC['g17'] = box(hi=[7], upto=9, cont=False, marks=[dict(row=1, inn=7, label="3득점", at=1.0)])
SC['g18'] = pv("사토시", "사토시", "삼성 투수 · 7회", [], stats=[st("앞 투수", "배찬승", 0.3), st("7회", "3실점", 2.0, hi=True), st("자책점", "0", 50, hi=True)])
SC['g19'] = pv("사토시", "사토시", "삼성 투수 · 7회", [], stats=[st("앞 투수", "배찬승", -1), st("7회", "3실점", -1, hi=True), st("자책점", "0", 0.8, hi=True)], cont=True)
SC['g20'] = S(0, "tiles", title="4차전 · 삼성 실점", items=[dict(v="4점", k="실점", at=0.2), dict(v="1점", k="자책점", at=1.2, hi=True)])
SC['g21'] = S(0, "tiles", title="4차전 · 삼성 실점", items=[dict(v="4점", k="실점", at=-1), dict(v="1점", k="자책점", at=-1, hi=True)], cont=True, text="실책이 점수로", textAt=0.5)
SC['g22'] = S(0, "tiles", title="4차전 · 삼성 수비", items=[dict(v="3개", k="실책", at=0.5, color=RED, hi=True)])
SC['g22b'] = S(0, "cells", title="4차전 · 삼성 실책 3개", cols=3, cw=420, ch=150, items=[dict(t="5회 디아즈", bad=True, at=0.3, fs=44), dict(t="6회 류지혁", bad=True, at=0.6, fs=44), dict(t="7회 김영웅", bad=True, at=0.9, fs=44)])
SC['g23'] = S(0, "faces", items=[dict(img=P["박진만"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤", at=0, say="“실책 후 실점하고\n역전당했다”", sayAt=1.0)], chain="pjm")
SC['g24'] = S(0, "faces", items=[dict(img=P["박진만"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤", at=-1, say="“제가 운영을\n잘못한 탓”", sayAt=3.0)], chain="pjm", cont=True)
SC['g25'] = S(0, "people", title="KIA 불펜 · 4차전", items=[pc("조상우", "조상우", "KIA", "1⅔이닝 · 승리", at=50), pc("전상현", "전상현", "KIA", "2이닝 무안타 · 세이브", at=50)], size=110, chain="kbp")
SC['g26'] = S(0, "people", title="KIA 불펜 · 4차전", items=[pc("조상우", "조상우", "KIA", "1⅔이닝 · 승리", at=0.2), pc("전상현", "전상현", "KIA", "2이닝 무안타 · 세이브", at=1.0)], size=110, chain="kbp", cont=True)
SC['g27'] = S(0, "bars", title="4차전 · 안타", items=[dict(label="KIA", team="KIA", value=10, unit="안타", at=0.2, hi=True), dict(label="삼성", team="삼성", value=7, unit="안타", at=1.0, color=GRAY)], max=12)
SC['g28'] = S(0, "cells", title="4차전 7회 · KIA 공격", cols=5, cw=300, ch=140, items=[dict(t="실책 출루", bad=True, at=0.2, fs=36), dict(t="카스트로 안타", hi=True, at=1.0, fs=36), dict(t="김선빈 안타", hi=True, at=1.2, fs=36), dict(t="한준수 안타", hi=True, at=1.4, fs=36), dict(t="하주석 안타", hi=True, at=1.6, fs=36)], label="실책 뒤 안타 4개", labelAt=2.0)
# ── ② 5차전 선발 ──
SC['s1'] = S(0, "matchup", left="삼성", right="KIA", score="2 : 2", text="플레이오프 5차전 · 대구", tag="5차전")
SC['s1b'] = S(0, "duel", title="플레이오프 5차전 · 대구 · 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="삼성 선발", at=1.0), right=dict(img=P["올러"], name="올러", team="KIA", role="KIA 선발", at=2.0), vsAt=1.5)
SC['s2'] = S(0, "duel", title="플레이오프 2차전 · 대구", left=dict(img=P["후라도"], name="후라도", team="삼성", role="2차전 선발", at=-1), right=dict(img=P["올러"], name="올러", team="KIA", role="2차전 선발", at=-1), vsAt=-1, cont=True)
SC['s3'] = S(0, "duel", title="플레이오프 2차전 · 대구", left=dict(img=P["후라도"], name="후라도", team="삼성", role="6⅔이닝 2실점 · 승", at=0.3), right=dict(img=P["올러"], name="올러", team="KIA", role="2차전 선발", at=-1), vsAt=-1, cont=True)
SC['s4'] = S(0, "duel", title="플레이오프 2차전 · 대구", left=dict(img=P["후라도"], name="후라도", team="삼성", role="6⅔이닝 2실점 · 승", at=-1), right=dict(img=P["올러"], name="올러", team="KIA", role="4⅔이닝 5실점 · 패", at=0.3), vsAt=-1, cont=True)
SC['s5'] = S(0, "scoreboard", title="플레이오프 2차전 · 대구", rows=[{"team": "KIA", "runs": [0, 0, 1, 0, 0, 0, 1, 1, 0], "r": 3}, {"team": "삼성", "runs": [0, 0, 4, 0, 1, 2, 1, 0, None], "r": 8, "hi": True}], hi=[], label="삼성 8대3 승", labelAt=1.0, chain="box2")
SC['s6'] = S(0, "tline", title="두 선발의 휴식", items=[dict(d="10월 27일", t="2차전 선발", at=0.3), dict(d="4일 휴식", t="10월 28~31일", at=1.0), dict(d="11월 1일", t="5차전 선발", c="good", at=1.8)])
SC['s7'] = S(0, "bars", title="2026 정규시즌 평균자책점 · 낮을수록 좋음", items=[dict(label="올러", team="KIA", value=3.13, unit="", at=1.0, hi=True), dict(label="후라도", team="삼성", value=3.54, unit="", at=2.0, color=GRAY)], max=5, chain="era")
SC['s8'] = pv("올러", "올러", "KIA 선발 · 5차전", [vstamp("변수는 대구", 50, "bad", size=56)], stats=[st("5차전 구장", "대구 삼성라이온즈파크", 0.5)])
SC['s8b'] = pv("올러", "올러", "KIA 선발 · 5차전", [vstamp("변수는 대구", 0.3, "bad", size=56)], stats=[st("5차전 구장", "대구 삼성라이온즈파크", -1)], cont=True)
SC['s9'] = S(0, "tiles", title="올러 · 2026 정규시즌 삼성전", items=[dict(v="세 번", k="등판", at=0.2), dict(v="14이닝", k="이닝", at=1.0), dict(v="5.79", k="평균자책점", at=2.0, hi=True)])
SC['s10'] = S(0, "bars", title="올러 · 2026 삼성전 구장별 실점", items=[dict(label="광주 두 경기", sub="13이닝", value=1, unit="실점", at=1.0, color=GREEN), dict(label="대구 정규시즌", sub="7월 28일 · 1이닝", value=8, unit="실점", at=50, color=RED), dict(label="대구 플레이오프 2차전", sub="10월 27일 · 4⅔이닝", value=5, unit="실점", at=50, color=RED)], max=14, chain="olr")
SC['s11'] = S(0, "bars", title="올러 · 2026 삼성전 구장별 실점", items=[dict(label="광주 두 경기", sub="13이닝", value=1, unit="실점", at=-1, color=GREEN), dict(label="대구 정규시즌", sub="7월 28일 · 1이닝", value=8, unit="실점", at=1.5, color=RED), dict(label="대구 플레이오프 2차전", sub="10월 27일 · 4⅔이닝", value=5, unit="실점", at=50, color=RED)], max=14, chain="olr", cont=True)
SC['s12'] = S(0, "bars", title="올러 · 2026 삼성전 구장별 실점", items=[dict(label="광주 두 경기", sub="13이닝", value=1, unit="실점", at=-1, color=GREEN), dict(label="대구 정규시즌", sub="7월 28일 · 1이닝", value=8, unit="실점", at=-1, color=RED), dict(label="대구 플레이오프 2차전", sub="10월 27일 · 4⅔이닝", value=5, unit="실점", at=0.3, color=RED)], max=14, chain="olr", cont=True, text="대구 두 경기 13실점", textAt=2.0)
SC['s13'] = pv("후라도B", "후라도", "삼성 선발 · 5차전", [vstamp("불안한 숫자도", 0.5, "bad", size=56)])
SC['s14'] = pv("후라도B", "후라도", "삼성 선발 · 2026 정규시즌 KIA전", [], stats=[st("KIA전 등판", "5월 15일 대구 · 한 경기", 1.0, hi=True), st("결과", "7이닝 3실점", 50), st("맞은 안타", "10개", 50, hi=True)])
SC['s15'] = pv("후라도B", "후라도", "삼성 선발 · 2026 정규시즌 KIA전", [], stats=[st("KIA전 등판", "5월 15일 대구 · 한 경기", -1, hi=True), st("결과", "7이닝 3실점", 1.0), st("맞은 안타", "10개", 2.0, hi=True)], cont=True)
SC['s16'] = S(0, "tline", title="후라도 · 정규시즌 마지막 두 경기", items=[dict(d="10월 5일 두산전", t="6⅓이닝\n6실점", c="bad", at=50), dict(d="10월 11일 KT전", t="4이닝\n6실점", c="bad", at=50)], chain="hrd", text="12실점", textAt=1.8)
SC['s17'] = S(0, "tline", title="후라도 · 정규시즌 마지막 두 경기", items=[dict(d="10월 5일 두산전", t="6⅓이닝\n6실점", c="bad", at=0.3), dict(d="10월 11일 KT전", t="4이닝\n6실점", c="bad", at=1.3)], chain="hrd", cont=True)
SC['s18'] = S(0, "tline", title="후라도 · 정규시즌 마지막 두 경기", items=[dict(d="10월 5일 두산전", t="6⅓이닝\n6실점", c="bad", at=-1), dict(d="10월 11일 KT전", t="4이닝\n6실점", c="bad", at=-1), dict(d="플레이오프 2차전", t="6⅔이닝\n2실점 · 승", c="good", at=0.8)], chain="hrd", cont=True)
SC['s19'] = S(0, "duel", title="정리 · 5차전 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="이번 시리즈 KIA 상대 승", at=2.5), right=dict(img=P["올러"], name="올러", team="KIA", role="대구 두 경기 13실점", at=0.5), vsAt=1.5)
# ── ③ 불펜 ──
SC['b1'] = S(0, "question", text="5차전 불펜 운용", logos=["삼성", "KIA"], logoSize=200, size=100)
SC['b1b'] = S(0, "tiles", title="플레이오프 5차전", items=[dict(v="마지막 경기", k="지면 끝", at=0.3, hi=True), dict(v="불펜 총력전", k="두 팀 모두", at=1.2)])
SC['b2'] = S(0, "faces", items=[dict(img=P["박진만"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤", at=0, say="“페덱과 최원태 빼고는\n불펜을 다 쓸 수 있게”", sayAt=1.0)])
SC['b3'] = S(0, "people", title="5차전에서 빠지는 삼성 선발", items=[pc("페덱", "페덱", "삼성", "4차전 선발", at=0.3), pc("최원태", "최원태", "삼성", "3차전 선발", at=1.0)], size=110, chain="sout")
SC['b4'] = S(0, "people", title="5차전에서 빠지는 삼성 선발", items=[pc("페덱", "페덱", "삼성", "4차전 선발", at=-1), pc("최원태", "최원태", "삼성", "3차전 선발", at=-1)], size=110, chain="sout", cont=True, text="나머지 투수는 모두 대기", textAt=0.5)
SC['b5'] = pv("후라도", "후라도", "삼성 선발 · 5차전", [vstamp("흔들리면 바로 불펜", 1.0, "gold", size=52)])
SC['b5b'] = S(0, "cells", title="4차전 · 삼성 불펜 다섯 명", cols=5, cw=300, ch=130, items=[dict(t=n, at=0.6 + 0.2 * j, fs=40) for j, n in enumerate(["이승민", "배찬승", "사토시", "이재희", "김태훈"])])
SC['b6'] = S(0, "people", title="KIA 마운드 · 4차전", items=[pc("네일", "네일", "KIA", "선발 5이닝", at=0.3), pc("조상우", "조상우", "KIA", "1⅔이닝", at=50), pc("전상현", "전상현", "KIA", "2이닝", at=50)], size=100, chain="kia4")
SC['b7'] = S(0, "people", title="KIA 마운드 · 4차전", items=[pc("네일", "네일", "KIA", "선발 5이닝", at=-1), pc("조상우", "조상우", "KIA", "1⅔이닝", at=0), pc("전상현", "전상현", "KIA", "2이닝 · 22구", at=0.3)], size=100, chain="kia4", cont=True)
SC['b7b'] = S(0, "tline", title="두 팀 불펜 일정", items=[dict(d="10월 30일", t="4차전", at=0), dict(d="10월 31일", t="휴식", c="good", at=0.8), dict(d="11월 1일", t="5차전", at=1.4)])
SC['b8'] = pv("올러B", "올러", "KIA 선발 · 5차전", [vstamp("일찍 내려가면 불펜 총동원", 1.0, "bad", size=48)])
# ── ④ 키플레이어 ──
SC['k0'] = S(0, "question", text="두 팀 키플레이어", logos=["KIA", "삼성"], logoSize=200, size=100)
SC['k1'] = pv("한준수", "한준수", "KIA 지명타자", [vstamp("KIA 키플레이어", 0.8, "gold", size=56)], imgAt=0.8)
SC['k2'] = pv("한준수", "한준수", "KIA 지명타자 · 플레이오프", [], stats=[st("네 경기", "12타수 5안타", 1.0, hi=True), st("1차전", "홈런", 50), st("4차전", "동점타 · 결승타", 50, hi=True)])
SC['k3'] = pv("한준수", "한준수", "KIA 지명타자 · 플레이오프", [], stats=[st("네 경기", "12타수 5안타", -1, hi=True), st("1차전", "홈런", 0.3), st("4차전", "동점타 · 결승타", 1.0, hi=True)], cont=True)
SC['k4'] = pv("김도영", "김도영", "KIA 3루수 · 플레이오프", [], stats=[st("네 경기", "16타수 7안타", 1.0, hi=True), st("3차전", "홈런", 50)])
SC['k5'] = pv("김도영", "김도영", "KIA 3루수 · 플레이오프", [], stats=[st("네 경기", "16타수 7안타", -1, hi=True), st("3차전", "홈런", 0.3)], cont=True)
SC['k6'] = S(0, "people", title="5차전 · KIA 타선의 숙제", items=[pc("김도영B", "김도영", "KIA", "출루", at=0.3), pc("한준수B", "한준수", "KIA", "연결", at=1.0), pc("후라도B", "후라도", "삼성", "삼성 선발", at=2.0)], size=100)
SC['k7'] = pv("최형우B", "최형우", "삼성 좌익수", [vstamp("삼성 키플레이어", 0.8, "gold", size=56)], imgAt=0.8)
SC['k8'] = S(0, "tline", title="최형우 · 이번 플레이오프 홈런", items=[dict(d="2차전 · 대구", t="홈런", c="good", at=1.0), dict(d="4차전 · 광주", t="홈런", c="good", at=1.6)])
SC['k9'] = S(0, "tiles", title="4차전 · 삼성 득점", items=[dict(v="2점", k="삼성 득점", at=0.2), dict(v="1점", k="최형우 홈런", at=1.2, hi=True)])
SC['k10'] = S(0, "duel", title="5차전 · 삼성 타선의 숙제", left=dict(img=P["최형우B"], name="최형우", team="삼성", role="먼저 앞서 줄까", at=1.0), right=dict(img=P["올러B"], name="올러", team="KIA", role="KIA 선발", at=0.3), vsAt=0.6)
# ── ⑤ 제 예상 ──
SC['z1'] = pvt("삼성", "5차전 예상", "플레이오프 5차전 · 대구", [vstamp("삼성 승리", 50, "gold", size=60)], stats=[st("이유", "세 가지", 50)], chain="zz")
SC['z1b'] = pvt("삼성", "5차전 예상", "플레이오프 5차전 · 대구", [vstamp("삼성 승리", 0.5, "gold", size=60)], stats=[st("이유", "세 가지", 50)], chain="zz", cont=True)
SC['z1c'] = pvt("삼성", "5차전 예상", "플레이오프 5차전 · 대구", [vstamp("삼성 승리", -1, "gold", size=60)], stats=[st("이유", "세 가지", 0.3)], chain="zz", cont=True)
SC['z2'] = S(0, "tiles", title="이유 셋 · 5차전", items=[dict(v="첫째", k="올러의 대구 성적", at=0.2, hi=True), dict(v="둘째", k="후라도", at=50), dict(v="셋째", k="정규시즌 수비", at=50)], chain="z3")
SC['z3'] = S(0, "bars", title="올러 · 2026 대구 성적", items=[dict(label="7월 28일 정규시즌", value=8, unit="실점", at=0.3, color=RED), dict(label="10월 27일 플레이오프", value=5, unit="실점", at=0.8, color=RED)], max=10)
SC['z4'] = S(0, "tiles", title="이유 셋 · 5차전", items=[dict(v="첫째", k="올러의 대구 성적", at=-1), dict(v="둘째", k="후라도", at=0.2, hi=True), dict(v="셋째", k="정규시즌 수비", at=50)], chain="z3")
SC['z5'] = pv("후라도", "후라도", "삼성 선발 · 플레이오프 2차전", [], stats=[st("KIA 상대", "6⅔이닝 2실점 · 승", 0.5, hi=True)])
SC['z6'] = S(0, "tiles", title="이유 셋 · 5차전", items=[dict(v="첫째", k="올러의 대구 성적", at=-1), dict(v="둘째", k="후라도", at=-1), dict(v="셋째", k="정규시즌 수비", at=0.2, hi=True)], chain="z3")
SC['z7'] = S(0, "bars", title="2026 정규시즌 팀 실책 · 적을수록 좋음", items=[dict(label="삼성", team="삼성", value=85, unit="개", at=0.5, hi=True), dict(label="SSG", team="SSG", value=85, unit="개", at=0.8, color=GRAY), dict(label="KT", team="KT", value=87, unit="개", at=1.1, color=GRAY), dict(label="KIA", team="KIA", value=98, unit="개", at=1.4, color=GRAY)], max=120, chain="err")
SC['z8'] = S(0, "tline", title="플레이오프 · 삼성 실책", items=[dict(d="3차전", t="실책 · 삼성 승", at=0.3), dict(d="4차전", t="실책 3개 · 삼성 패", c="bad", at=1.0)])
SC['z8b'] = S(0, "bars", title="2026 정규시즌 팀 실책 · 적을수록 좋음", items=[dict(label="삼성", team="삼성", value=85, unit="개", at=0, hi=True), dict(label="SSG", team="SSG", value=85, unit="개", at=0, color=GRAY), dict(label="KT", team="KT", value=87, unit="개", at=0, color=GRAY), dict(label="KIA", team="KIA", value=98, unit="개", at=0, color=GRAY)], max=120, text="정규시즌 실책 최소", textAt=1.5)
SC['z9'] = S(0, "question", text="뒤집힐 조건", logos=["KIA"], logoSize=180, size=100)
SC['z10'] = pv("올러B", "올러", "KIA 선발 · 5차전", [vstamp("5이닝 이상 버티면", 0.8, "gold", size=52)])
SC['z11'] = S(0, "cells", title="4차전 · 삼성 실책 3개", cols=3, cw=420, ch=150, items=[dict(t="5회 디아즈", bad=True, at=0, fs=44), dict(t="6회 류지혁", bad=True, at=0, fs=44), dict(t="7회 김영웅", bad=True, at=0, fs=44)], label="또 나오면", labelAt=0.5)
SC['z12'] = S(0, "tline", title="후라도 · 정규시즌 마지막 두 경기", items=[dict(d="10월 5일 두산전", t="6⅓이닝\n6실점", c="bad", at=0), dict(d="10월 11일 KT전", t="4이닝\n6실점", c="bad", at=0)], text="또 흔들리면", textAt=1.0)
SC['z13'] = S(0, "question", text="예상 점수\n삼성 5대3 승", logos=["삼성", "KIA"], logoSize=200, size=104)
SC['z14'] = S(0, "question", text="한국시리즈에 가는 팀은?\n삼성? KIA?", logos=["삼성", "KIA"], logoSize=200, size=96)


# ── 10/31 사전검사(precheck·late_check) 반영: 이름을 말하는 줄엔 그 사람 사진, 말하지 않은 숫자는 화면에서 뺌 ──
SC['g7'] = pv("최형우", "최형우", "삼성 좌익수 · 6회", [vstamp("세 번째 승부처", 0.3, "gold", size=52)], stats=[st("6회", "홈런", 1.0, hi=True)], imgAt=2.0)
SC['g8'] = pv("최형우", "최형우", "삼성 좌익수 · 6회", [vstamp("솔로 홈런", 1.0, "gold", size=56)], stats=[st("6회", "홈런", -1, hi=True), st("상대 투수", "곽도규", 0.3)], cont=True)
SC['g9'] = pv("최형우", "최형우", "삼성 좌익수 · 6회", [vstamp("솔로 홈런", -1, "gold", size=56)], stats=[st("6회", "홈런", -1, hi=True), st("상대 투수", "곽도규", -1), st("플레이오프", "두 번째 홈런", 1.0, hi=True)], cont=True)
_r7 = lambda a, b, c, d, txt=None, **k: S(0, "people", title="7회 · KIA 공격", items=[pc("김도영B", "김도영", "KIA", "실책으로 출루", at=a), pc("카스트로", "카스트로", "KIA", "동점 안타", at=b), pc("김선빈", "김선빈", "KIA", "중전 안타", at=c), pc("한준수", "한준수", "KIA", "역전 적시타", at=d)], size=90, chain="r7", **(dict(text=txt, textAt=k.pop("textAt", 1.0)) if txt else {}), **k)
SC['g12'] = box(hi=[7], upto=6, marks=[dict(row=0, inn=6, label="홈런", at=-1)], text="KIA 1대2로 뒤진 채", textAt=0.5)
SC['g13'] = _r7(1.0, 50, 50, 50)
SC['g14'] = _r7(-1, 0.2, 50, 50, txt="2대2", textAt=1.0, cont=True)
SC['g15'] = _r7(-1, -1, 0.2, 1.0, cont=True)
SC['g16'] = S(0, "people", title="7회 · KIA 공격", items=[pc("한준수", "한준수", "KIA", "3대2 역전", at=0), pc("하주석", "하주석", "KIA", "4대2 안타", at=1.0)], size=110, text="KIA 4대2", textAt=2.0)
SC['g18'] = pv("사토시", "사토시", "삼성 투수 · 7회", [], stats=[st("앞 투수", "배찬승", 1.0), st("7회", "3실점", 2.0, hi=True), st("자책점", "0", 50, hi=True)])
SC['g19'] = pv("사토시", "사토시", "삼성 투수 · 7회", [], stats=[st("앞 투수", "배찬승", -1), st("7회", "3실점", -1, hi=True), st("자책점", "0", 0.5, hi=True)], cont=True)
SC['g22'] = S(0, "tiles", title="4차전 · 삼성 수비", items=[dict(v="3개", k="실책", at=0.3, color=RED, hi=True)])
SC['g22b'] = S(0, "people", title="4차전 · 삼성 실책", items=[pc("디아즈", "디아즈", "삼성", "실책", at=0.1), pc("류지혁", "류지혁", "삼성", "실책", at=0.5), pc("김영웅", "김영웅", "삼성", "실책", at=0.8)], size=100)
_pj = dict(img=P["박진만"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤")
SC['g23'] = S(0, "faces", items=[dict(_pj, at=0, say="“실책 후 실점하고\n역전당했다”", sayAt=1.0), dict(img=P["사토시"], name="사토시", team="삼성", role="삼성 투수", at=50), dict(img=P["김도영B"], name="김도영", team="KIA", role="KIA 타자", at=50)], chain="pjm")
SC['g24'] = S(0, "faces", items=[dict(_pj, at=-1, say="“제가 운영을\n잘못한 탓”", sayAt=3.0), dict(img=P["사토시"], name="사토시", team="삼성", role="삼성 투수", at=0.3), dict(img=P["김도영B"], name="김도영", team="KIA", role="KIA 타자", at=1.2)], chain="pjm", cont=True)
SC['g25'] = S(0, "people", title="KIA 불펜 · 4차전", items=[pc("조상우", "조상우", "KIA", "승리투수", at=50), pc("전상현", "전상현", "KIA", "2이닝 무안타 · 세이브", at=50)], size=110, chain="kbp", text="KIA 4대2 지킴", textAt=1.0)
SC['g26'] = S(0, "people", title="KIA 불펜 · 4차전", items=[pc("조상우", "조상우", "KIA", "승리투수", at=0.2), pc("전상현", "전상현", "KIA", "2이닝 무안타 · 세이브", at=1.0)], size=110, chain="kbp", cont=True, text="KIA 4대2 지킴", textAt=-1)
SC['g28'] = S(0, "cells", title="4차전 7회 · 실책 뒤 안타", cols=4, cw=340, ch=140, items=[dict(t="카스트로", hi=True, at=1.0, fs=40), dict(t="김선빈", hi=True, at=1.2, fs=40), dict(t="한준수", hi=True, at=1.4, fs=40), dict(t="하주석", hi=True, at=1.6, fs=40)])
SC['s1b'] = S(0, "duel", title="플레이오프 5차전 · 대구 · 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="삼성 선발", at=0.6), right=dict(img=P["올러"], name="올러", team="KIA", role="KIA 선발", at=1.2), vsAt=0.9)
SC['s6'] = S(0, "tline", title="두 선발의 휴식", items=[dict(d="2차전", t="선발", at=0.3), dict(d="나흘", t="휴식", at=1.0), dict(d="5차전", t="다시 선발", c="good", at=1.6)])
SC['s7'] = S(0, "duel", title="2026 정규시즌 평균자책점", left=dict(img=P["올러"], name="올러", team="KIA", role="평균자책점 3.13", at=1.0), right=dict(img=P["후라도"], name="후라도", team="삼성", role="평균자책점 3.54", at=2.0), vsAt=1.5)
SC['s8'] = S(0, "tiles", title="플레이오프 5차전", items=[dict(v="대구", k="장소 · 삼성 홈", at=0.4, hi=True)])
SC['s9'] = pv("올러", "올러", "KIA 선발 · 2026 정규시즌 삼성전", [], stats=[st("등판", "세 번 · 14이닝", 1.0), st("평균자책점", "5.79", 3.0, hi=True)])
SC['s10'] = S(0, "bars", title="올러 · 2026 삼성전 실점", items=[dict(label="광주 두 경기", sub="13이닝", value=1, unit="실점", at=1.0, color=GREEN), dict(label="대구 정규시즌", sub="7월 28일 · 1이닝", value=8, unit="실점", at=50, color=RED)], max=10, chain="olr")
SC['s11'] = S(0, "bars", title="올러 · 2026 삼성전 실점", items=[dict(label="광주 두 경기", sub="13이닝", value=1, unit="실점", at=-1, color=GREEN), dict(label="대구 정규시즌", sub="7월 28일 · 1이닝", value=8, unit="실점", at=1.0, color=RED)], max=10, chain="olr", cont=True)
SC['s12'] = pv("올러B", "올러", "KIA 선발 · 2026 대구", [vstamp("대구 두 경기 13실점", 2.0, "bad", size=52)], stats=[st("플레이오프 2차전", "포함", 0.3)], imgAt=1.0)
SC['s16'] = pv("후라도B", "후라도", "삼성 선발 · 정규시즌 마지막 두 경기", [vstamp("12실점", 2.0, "bad", size=60)])
SC['s17'] = S(0, "tline", title="후라도 · 정규시즌 마지막 두 경기", items=[dict(d="10월 5일 두산전", t="6실점", c="bad", at=0.3), dict(d="10월 11일 KT전", t="6실점", c="bad", at=1.3)], chain="hrd")
SC['s18'] = pv("후라도", "후라도", "삼성 선발 · 플레이오프 2차전", [vstamp("흐름을 끊고 승리", 1.0, "gold", size=52)])
SC['s19'] = S(0, "duel", title="정리 · 5차전 선발", left=dict(img=P["올러"], name="올러", team="KIA", role="대구 두 경기 모두 무너짐", at=0.5), right=dict(img=P["후라도"], name="후라도", team="삼성", role="2차전 KIA 상대 승", at=2.5), vsAt=1.5)
SC['b1b'] = S(0, "tiles", title="플레이오프 5차전", items=[dict(v="마지막 경기", k="지면 끝", at=0.3, hi=True), dict(v="불펜 운용", k="달라짐", at=1.0)])
SC['b2'] = S(0, "faces", items=[dict(_pj, role="삼성 감독 · 4차전 뒤", at=0, say="“페덱·최원태 빼고\n불펜 다 쓸 수 있게”", sayAt=1.0), dict(img=P["페덱"], name="페덱", team="삼성", role="4차전 선발", at=0.3), dict(img=P["최원태"], name="최원태", team="삼성", role="3차전 선발", at=0.6)])
SC['b5b'] = S(0, "cells", title="4차전 · 삼성 불펜", cols=5, cw=300, ch=130, items=[dict(t=n, at=0.6 + 0.1 * j, fs=40) for j, n in enumerate(["이승민", "배찬승", "사토시", "이재희", "김태훈"])], label="다섯 명", labelAt=1.0)
SC['b6'] = S(0, "people", title="KIA 마운드 · 4차전", items=[pc("네일", "네일", "KIA", "선발 5이닝", at=0.3), pc("조상우", "조상우", "KIA", "불펜", at=1.0), pc("전상현", "전상현", "KIA", "불펜", at=1.3)], size=100, chain="kia4")
SC['b7'] = S(0, "people", title="KIA 마운드 · 4차전", items=[pc("네일", "네일", "KIA", "선발 5이닝", at=-1), pc("조상우", "조상우", "KIA", "불펜", at=-1), pc("전상현", "전상현", "KIA", "불펜 · 22구", at=0.3)], size=100, chain="kia4", cont=True)
SC['b7b'] = S(0, "tline", title="두 팀 불펜 일정", items=[dict(d="4차전", t="경기", at=0), dict(d="하루", t="휴식", c="good", at=0.5), dict(d="5차전", t="경기", at=1.0)])
SC['k1'] = pv("한준수", "한준수", "KIA 지명타자", [vstamp("KIA 키플레이어", 0.3, "gold", size=56)], imgAt=0.2)
SC['k2'] = pv("한준수", "한준수", "KIA 지명타자 · 플레이오프", [], stats=[st("네 경기", "12타수 5안타", 1.5, hi=True), st("1차전", "홈런", 50), st("4차전", "동점타 · 결승타", 50, hi=True)])
SC['k3'] = pv("한준수", "한준수", "KIA 지명타자 · 플레이오프", [], stats=[st("네 경기", "12타수 5안타", -1, hi=True), st("1차전", "홈런", 1.0), st("4차전", "동점타 · 결승타", 2.0, hi=True)], cont=True)
SC['k4'] = pv("김도영", "김도영", "KIA 3루수 · 플레이오프", [], stats=[st("네 경기", "16타수 7안타", 1.0, hi=True), st("3차전", "홈런", 50)])
SC['k5'] = pv("김도영", "김도영", "KIA 3루수 · 플레이오프", [], stats=[st("네 경기", "16타수 7안타", -1, hi=True), st("3차전", "홈런", 1.0)], cont=True)
SC['k7'] = pv("최형우B", "최형우", "삼성 좌익수", [vstamp("삼성 키플레이어", 0.3, "gold", size=56)], imgAt=0.2)
SC['k9'] = pv("최형우B", "최형우", "삼성 좌익수 · 4차전", [], stats=[st("삼성 득점", "2점", 0.3), st("최형우 홈런", "1점", 1.0, hi=True)])
SC['k10'] = pv("최형우B", "최형우", "삼성 좌익수 · 5차전", [vstamp("먼저 점수를 내면", 1.0, "gold", size=52)])
SC['z2'] = pv("올러", "올러", "KIA 선발 · 5차전", [vstamp("첫째 · 대구 성적", 0.3, "bad", size=52)])
SC['z3'] = pv("올러", "올러", "KIA 선발 · 2026 대구", [vstamp("첫째 · 대구 성적", -1, "bad", size=52)], stats=[st("대구 두 경기", "모두 무너짐", 1.0, hi=True)], cont=True)
SC['z4'] = pv("후라도", "후라도", "삼성 선발 · 5차전", [vstamp("둘째 · 후라도", 0.2, "gold", size=52)])
SC['z5'] = pv("후라도", "후라도", "삼성 선발 · 5차전", [vstamp("둘째 · 후라도", -1, "gold", size=52)], stats=[st("플레이오프 2차전", "KIA 상대 승리", 1.0, hi=True)], cont=True)
SC['z6'] = S(0, "tiles", title="이유 셋 · 5차전", items=[dict(v="셋째", k="정규시즌 수비", at=0.2, hi=True)])
SC['z11'] = pvt("삼성", "삼성 수비", "플레이오프 5차전", [vstamp("또 실책 뒤 실점하면", 0.5, "bad", size=52)])
SC['z12'] = pv("후라도B", "후라도", "삼성 선발 · 5차전", [vstamp("또 크게 흔들리면", 1.0, "bad", size=52)])
for _k in ('z2', 'z4', 'z6'): pass

# 10/31 사전검사 2차
SC['g2'] = S(0, "people", title="2회 · 삼성 공격", items=[pc("김영웅", "김영웅", "삼성", "안타", at=1.0), pc("강민호", "강민호", "삼성", "연속 안타", at=1.3), pc("류지혁", "류지혁", "삼성", "우전 적시타", at=50)], size=100, chain="g2p")
SC['g3'] = S(0, "people", title="2회 · 삼성 공격", items=[pc("김영웅", "김영웅", "삼성", "안타", at=-1), pc("강민호", "강민호", "삼성", "연속 안타", at=-1), pc("류지혁", "류지혁", "삼성", "우전 적시타", at=0.2)], size=100, chain="g2p", cont=True, text="삼성 1대0", textAt=1.0)
_r7 = lambda a, b, c, d, e, txt=None, **k: S(0, "people", title="7회 · KIA 공격", items=[pc("김영웅", "김영웅", "삼성", "3루수 실책", at=a), pc("김도영B", "김도영", "KIA", "출루 · 득점", at=b), pc("카스트로", "카스트로", "KIA", "동점 안타", at=c), pc("김선빈", "김선빈", "KIA", "중전 안타", at=d), pc("한준수", "한준수", "KIA", "역전 적시타", at=e)], size=80, chain="r7", **(dict(text=txt, textAt=k.pop("textAt", 1.0)) if txt else {}), **k)
SC['g13'] = _r7(0.2, 1.0, 50, 50, 50)
SC['g14'] = _r7(-1, -1, 0.2, 50, 50, txt="2대2", textAt=1.0, cont=True)
SC['g15'] = _r7(-1, -1, -1, 0.2, 1.0, cont=True)
SC['b2'] = S(0, "faces", items=[dict(_pj, at=0, say="“페덱·최원태 빼고\n불펜 다 쓸 수 있게”", sayAt=1.0), dict(img=P["페덱"], name="페덱", team="삼성", role="4차전 선발", at=0.3), dict(img=P["최원태"], name="최원태", team="삼성", role="3차전 선발", at=0.6)])
SC['b3'] = S(0, "people", title="5차전에서 빠지는 삼성 선발", items=[pc("페덱", "페덱", "삼성", "4차전 선발", at=-1), pc("최원태", "최원태", "삼성", "3차전 선발", at=-1)], size=110, chain="sout")
_k9 = [st("삼성 득점", "2점", 0.3), st("최형우 홈런", "1점", 1.0, hi=True)]
SC['k9'] = pv("최형우B", "최형우", "삼성 좌익수", [vstamp("먼저 점수를 내면", 50, "gold", size=52)], stats=_k9, imgAt=1.0, chain="k9")
SC['k10'] = pv("최형우B", "최형우", "삼성 좌익수", [vstamp("먼저 점수를 내면", 1.0, "gold", size=52)], stats=[dict(x, at=-1) for x in _k9], chain="k9", cont=True)

# 10/31 rule_check R4: 이어지는 장면에서 생길 글 자리를 첫 장면부터 비워 둠(textAt 50 = 자리만)
for _k in ('g3', 'g6'): SC[_k] = {k_: v_ for k_, v_ in SC[_k].items() if k_ not in ('text', 'textAt')}
for _a, _b in (('g13', 'g14'), ('g20', 'g21'), ('b3', 'b4')):
    SC[_a] = dict(SC[_a], text=SC[_b]['text'], textAt=50)
for _k in ('g15',): SC[_k] = dict(SC[_k], text='2대2', textAt=-1)

# ── 10/31 v6 보강(사용자 "8분 넘게 보강"): 1~3차전 흐름 · 페덱/네일 · 불펜 사용 · 장타 · 실책 비교 ──
SC['o2b'] = S(0, "duel", title="플레이오프 5차전 · 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="삼성 선발", at=1.0), right=dict(img=P["올러"], name="올러", team="KIA", role="KIA 선발", at=2.0), vsAt=1.5)
SC['s2'] = S(0, "duel", title="플레이오프 2차전 · 대구", left=dict(img=P["후라도"], name="후라도", team="삼성", role="2차전 선발", at=0.2), right=dict(img=P["올러"], name="올러", team="KIA", role="2차전 선발", at=0.2), vsAt=0.5)
GM = [("1차전", "대구", "삼성", "KIA"), ("2차전", "대구", "삼성", "삼성"), ("3차전", "광주", "KIA", "삼성"), ("4차전", "광주", "KIA", "KIA")]
def ser(done, new_at=0.5, **k):
    g = [dict(n=n, venue=v, home=h, win=(w if j < done else None), at=(new_at if j == done - 1 else (-1 if j < done - 1 else 0))) for j, (n, v, h, w) in enumerate(GM)]
    return S(0, "series5", title="플레이오프 · 삼성 vs KIA", games=g, chain="ser", **k)
SC['f1'] = S(0, "toc", on=0)
SC['f2'] = ser(1, 1.0)
SC['f3'] = pv("카스트로", "카스트로", "KIA 1루수 · 1차전", [], stats=[st("1차전", "투런 홈런", 1.0, hi=True), st("타점", "3타점", 2.0)])
SC['f4'] = pvt("삼성", "삼성 타선", "플레이오프 1차전", [vstamp("안타 두 개", 1.0, "bad", size=60)])
SC['f5'] = ser(2, 1.0)
SC['f6'] = S(0, "people", title="2차전 · 삼성 홈런", items=[pc("디아즈", "디아즈", "삼성", "3회 투런 홈런", at=0.2), pc("최형우B", "최형우", "삼성", "7회 솔로 홈런", at=1.0)], size=110)
SC['f7'] = ser(3, 1.0)
SC['f8'] = S(0, "tiles", title="3차전 · 광주", items=[dict(v="네 개", k="홈런", at=1.0, hi=True)])
SC['f9'] = S(0, "people", title="3차전 홈런", items=[pc("디아즈", "디아즈", "삼성", "삼성", at=0.1), pc("류지혁", "류지혁", "삼성", "삼성", at=0.4), pc("김도영B", "김도영", "KIA", "KIA", at=1.1), pc("나성범", "나성범", "KIA", "KIA", at=1.4)], size=85)
SC['f10'] = pv("박승규", "박승규", "삼성 외야수 · 3차전", [vstamp("결승 2루타", 2.0, "gold", size=56)], stats=[st("7회", "결승타", 1.0, hi=True)], imgAt=2.0)
SC['f11'] = S(0, "bars", title="플레이오프 네 경기 · 득점", items=[dict(label="삼성", team="삼성", value=17, unit="점", at=1.0, hi=True), dict(label="KIA", team="KIA", value=16, unit="점", at=2.0, color=GRAY)], max=20)
SC['f12'] = S(0, "bars", title="플레이오프 네 경기 · 안타", items=[dict(label="KIA", team="KIA", value=32, unit="개", at=0.3, hi=True), dict(label="삼성", team="삼성", value=28, unit="개", at=1.0, color=GRAY)], max=40)
SC['f13'] = ser(4, 0, text="대구 1승 1패", textAt=3.0)
SC['f14'] = ser(4, -1, text="대구 1승 1패", textAt=-1, cont=True)
SC['p1'] = pv("페덱", "페덱", "삼성 선발 · 4차전", [], stats=[st("4차전", "5⅓이닝 1실점", 1.0, hi=True), st("1차전", "4⅔이닝 5실점", 50)], chain="fdk")
SC['p2'] = pv("페덱", "페덱", "삼성 선발 · 4차전", [], stats=[st("4차전", "5⅓이닝 1실점", -1, hi=True), st("1차전", "4⅔이닝 5실점", 2.0)], chain="fdk", cont=True)
SC['p3'] = pv("네일", "네일", "KIA 선발 · 4차전", [], stats=[st("4차전", "5이닝 1실점", 1.0, hi=True)])
SC['b9'] = pv("이승민", "이승민", "삼성 불펜", [vstamp("네 경기 모두 등판", 1.0, "gold", size=52)])
SC['b10'] = S(0, "people", title="삼성 불펜 · 세 경기씩", items=[pc("김태훈", "김태훈", "삼성", "세 경기", at=0), pc("사토시", "사토시", "삼성", "세 경기", at=0)], size=110, text="배찬승도 세 경기", textAt=1.0)
SC['b13'] = pv("원태인", "원태인", "삼성 투수 · 플레이오프", [], stats=[st("2차전", "마지막 이닝 등판", 1.0), st("3차전", "불펜 등판", 1.5), st("3차전 결과", "1⅔이닝 · 승리투수", 50, hi=True)], chain="wti")
SC['b14'] = pv("원태인", "원태인", "삼성 투수 · 플레이오프", [], stats=[st("2차전", "마지막 이닝 등판", -1), st("3차전", "불펜 등판", -1), st("3차전 결과", "1⅔이닝 · 승리투수", 1.0, hi=True)], chain="wti", cont=True)
SC['b15'] = pv("원태인", "원태인", "삼성 투수 · 5차전", [vstamp("뒤쪽에서 대기?", 1.0, "gold", size=52)])
SC['b11'] = pv("전상현", "전상현", "KIA 불펜 · 플레이오프", [], stats=[st("세 경기", "4⅔이닝 무실점", 2.0, hi=True)])
SC['b12'] = pv("조상우", "조상우", "KIA 불펜 · 플레이오프", [], stats=[st("세 경기", "4⅓이닝", 1.0), st("3차전", "2실점 · 패", 2.0, hi=True)])
SC['z6'] = S(0, "tiles", title="이유 셋 · 5차전", items=[dict(v="셋째", k="장타", at=0.2, hi=True)])
SC['z7'] = S(0, "people", title="삼성 플레이오프 홈런 다섯 개", items=[pc("디아즈", "디아즈", "삼성", "홈런 두 개", at=2.0), pc("최형우B", "최형우", "삼성", "홈런 두 개", at=2.3)], size=110)
SC['z8'] = pv("디아즈", "디아즈", "삼성 1루수 · 2차전", [vstamp("올러 상대 투런 홈런", 1.5, "gold", size=52)])
SC['z11'] = S(0, "bars", title="플레이오프 네 경기 · 실책", items=[dict(label="삼성", team="삼성", value=7, unit="개", at=2.0, color=RED, hi=True), dict(label="KIA", team="KIA", value=1, unit="개", at=3.0, color=GRAY)], max=10)
SC['z11b'] = pvt("삼성", "삼성 수비", "플레이오프 5차전", [vstamp("또 실책이 나오면", 0.5, "bad", size=52)])

SC['s2'] = S(0, "duel", title="플레이오프 2차전 · 대구", left=dict(img=P["후라도"], name="후라도", team="삼성", role="2차전 선발", at=0.1), right=dict(img=P["올러"], name="올러", team="KIA", role="2차전 선발", at=0.4), vsAt=0.6)
SC['b15'] = pv("원태인", "원태인", "삼성 투수 · 플레이오프", [vstamp("5차전도 뒤쪽에서 대기?", 1.0, "gold", size=48)], stats=[st("2차전", "마지막 이닝 등판", -1), st("3차전", "불펜 등판", -1), st("3차전 결과", "1⅔이닝 · 승리투수", -1, hi=True)], chain="wti", cont=True)
SC['z8'] = S(0, "people", title="플레이오프 2차전 · 3회", items=[pc("디아즈", "디아즈", "삼성", "투런 홈런", at=0), pc("올러B", "올러", "KIA", "KIA 선발", at=1.0)], size=110)

# ── 10/31 v7(검수 r3) ──
SC['f13'] = ser(4, 0, text="대구 1승 1패", textAt=3.0)
SC['f14'] = ser(4, -1, text="팽팽한 시리즈", textAt=0.5)
SC['s8'] = S(0, "tiles", title="플레이오프 5차전", items=[dict(v="대구", k="11월 1일 · 삼성 홈", at=1.0, hi=True)])
SC['s11'] = pv("올러B", "올러", "KIA 선발 · 2026 정규시즌", [], stats=[st("7월 28일 · 대구", "1이닝 8실점", 2.0, hi=True)])
SC['s14'] = pv("후라도B", "후라도", "삼성 선발 · 2026 정규시즌 KIA전", [], stats=[st("KIA전 등판", "5월 15일 대구 · 한 경기", 1.0, hi=True), st("결과", "7이닝", 50), st("맞은 안타", "10개", 50, hi=True)])
SC['s15'] = pv("후라도B", "후라도", "삼성 선발 · 2026 정규시즌 KIA전", [], stats=[st("KIA전 등판", "5월 15일 대구 · 한 경기", -1, hi=True), st("결과", "7이닝", 1.0), st("맞은 안타", "10개", 2.0, hi=True)], cont=True)
SC['b10b'] = pv("이승민", "이승민", "삼성 불펜 · 5차전", [vstamp("피로가 쌓였을 수도", 1.0, "bad", size=52)], imgAt=1.0)
SC['b5'] = pv("후라도", "후라도", "삼성 선발 · 5차전", [vstamp("흔들리면 바로 불펜", 2.0, "gold", size=52)], imgAt=1.0)
SC['b12b'] = S(0, "people", title="KIA 불펜 · 5차전 전", items=[pc("전상현", "전상현", "KIA", "하루 휴식", at=1.0), pc("조상우", "조상우", "KIA", "하루 휴식", at=1.3)], size=110)
SC['z6'] = S(0, "people", title="이유 셋 · 5차전", items=[pc("디아즈", "디아즈", "삼성", "셋째 이유", at=1.0), pc("최형우B", "최형우", "삼성", "셋째 이유", at=1.3)], size=110, chain="z6p")
SC['z7'] = S(0, "people", title="이유 셋 · 5차전", items=[pc("디아즈", "디아즈", "삼성", "홈런 두 개", at=2.0), pc("최형우B", "최형우", "삼성", "홈런 두 개", at=2.2)], size=110, chain="z6p", cont=True)
SC['z11c'] = S(0, "bars", title="2026 정규시즌 팀 실책 · 적을수록 좋음", items=[dict(label="삼성", team="삼성", value=85, unit="개", at=0.5, hi=True), dict(label="SSG", team="SSG", value=85, unit="개", at=2.0, color=GRAY), dict(label="KT", team="KT", value=87, unit="개", at=2.3, color=GRAY), dict(label="KIA", team="KIA", value=98, unit="개", at=2.5, color=GRAY)], max=120)
SC['z12b'] = S(0, "people", title="뒤집힐 조건", items=[pc("디아즈", "디아즈", "삼성", "막히면", at=0), pc("최형우B", "최형우", "삼성", "막히면", at=0.2)], size=110)

# ── 10/31 v7b ──
SC['g0'] = S(0, "toc", on=1)
SC['z9'] = S(0, "question", text="뒤집힐 조건 네 가지", logos=["KIA"], logoSize=180, size=96)
SC['z11'] = S(0, "bars", title="플레이오프 네 경기 · 실책", items=[dict(label="삼성", team="삼성", value=7, unit="개", at=2.0, color=RED, hi=True), dict(label="KIA", team="KIA", value=1, unit="개", at=3.0, color=GRAY)], max=10)
SC['z11c'] = S(0, "bars", title="2026 정규시즌 팀 실책 · 적을수록 좋음", items=[dict(label="삼성", team="삼성", value=85, unit="개", at=0.3, hi=True), dict(label="SSG", team="SSG", value=85, unit="개", at=1.0, color=GRAY), dict(label="KT", team="KT", value=87, unit="개", at=1.3, color=GRAY), dict(label="KIA", team="KIA", value=98, unit="개", at=1.5, color=GRAY)], max=120)
SC['z10'] = pv("올러B", "올러", "KIA 선발 · 5차전", [vstamp("첫째 · 5이닝 이상 버티면", 1.0, "gold", size=48)], imgAt=1.0)
SC['z11b'] = pvt("삼성", "삼성 수비", "플레이오프 5차전", [vstamp("둘째 · 또 실책이 나오면", 1.0, "bad", size=48)])
SC['z12'] = pv("후라도B", "후라도", "삼성 선발 · 5차전", [vstamp("셋째 · 크게 흔들리면", 1.5, "bad", size=48)], imgAt=1.0)
SC['z12b'] = S(0, "people", title="넷째 조건", items=[pc("디아즈", "디아즈", "삼성", "막히면", at=1.0), pc("최형우B", "최형우", "삼성", "막히면", at=1.2)], size=110)
SC['p2'] = pv("페덱", "페덱", "삼성 선발 · 4차전", [vstamp("반등", 2.0, "gold", size=60)], stats=[st("4차전", "5⅓이닝 1실점", -1, hi=True), st("1차전", "4⅔이닝 5실점", 1.0)], chain="fdk", cont=True)

# ════ 10/31 01:40 v8: 사용자 "문장 사이가 이상해" → 대사 흐름 다시 씀 + 영상 화면 검수(사진 종류 통일·얼굴 가운데·빈 화면·로고 먼저 노출) 반영 ════
P.update({"류지혁": "카드/G18_류지혁_A_중앙", "디아즈": "카드/G18_디아즈_B_중앙", "최형우G": "카드/G18_최형우_미소_중앙", "김영웅": "상황별/김영웅_적시타_1026_삼성제공_중앙",
          "김선빈": "카드/P17_김선빈_중앙", "네일": "카드/P17_네일_역투_중앙", "전상현": "카드/P18_전상현_역투_중앙", "나성범": "카드/G18_나성범_A",
          "박진만F": "KBO프로필/박진만_감독", "사토시F": "KBO프로필/미야모리", "김도영F": "KBO프로필/김도영", "페덱F": "KBO프로필/페덱", "최원태F": "KBO프로필/최원태_2026삼성"})
SC.clear()
SC['o1'] = box(cont=False, label="KIA 4대2 승 · 시리즈 2승 2패", labelAt=2.0)
SC['o2'] = S(0, "matchup", left="삼성", right="KIA", score="2 : 2", text="플레이오프 5차전 · 11월 1일 대구", tag="한국시리즈행 마지막 경기")
SC['o2b'] = S(0, "duel", title="플레이오프 5차전 · 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="삼성 선발", at=1.0), right=dict(img=P["올러"], name="올러", team="KIA", role="KIA 선발", at=1.4), vsAt=1.2)
SC['o3'] = S(0, "matchup", left="삼성", right="KIA", score="2 : 2", text="이긴 팀 → 한국시리즈 vs KT", tag="한국시리즈행 마지막 경기")
SC['o3b'] = S(0, "question", text="한국시리즈에 가는 팀은?", logos=["삼성", "KIA"], logoSize=200, size=96)
SC['o4'] = S(0, "toc", on=-1, itemFrom=1)
SC['f1'] = S(0, "toc", on=0)
SC['f2'] = ser(1, 1.0)
SC['f3'] = pv("카스트로", "카스트로", "KIA 타자 · 1차전", [], stats=[st("1차전", "투런 홈런", 1.0, hi=True), st("타점", "3타점", 1.5), st("삼성 타선", "안타 두 개", 3.0)])
SC['f5'] = ser(2, 1.0)
SC['f6'] = S(0, "people", title="2차전 · 삼성 홈런", items=[pc("디아즈", "디아즈", "삼성", "3회 투런 홈런", at=0.1), pc("최형우G", "최형우", "삼성", "7회 솔로 홈런", at=1.0)], size=110)
SC['f7'] = ser(3, 1.0)
SC['f9'] = S(0, "people", title="3차전 홈런", items=[pc("디아즈", "디아즈", "삼성", "삼성", at=1.0), pc("류지혁", "류지혁", "삼성", "삼성", at=1.3), pc("김도영B", "김도영", "KIA", "KIA", at=2.0), pc("나성범", "나성범", "KIA", "KIA", at=2.3)], size=85)
SC['f10'] = pv("박승규", "박승규", "삼성 타자 · 3차전", [vstamp("결승 2루타", 1.0, "gold", size=56)], stats=[st("7회", "결승타", 1.0, hi=True)], imgAt=1.0)
SC['f10b'] = ser(3, -1, text="KIA 1승 2패", textAt=1.0)
SC['g0'] = S(0, "toc", on=1)
SC['g1'] = box(hi=[2], upto=2, cont=False, marks=[dict(row=0, inn=2, label="선취점", at=2.0)])
SC['g2'] = S(0, "people", title="2회 · 삼성 공격", items=[pc("김영웅", "김영웅", "삼성", "안타", at=0), pc("강민호", "강민호", "삼성", "연속 안타", at=0.3), pc("류지혁", "류지혁", "삼성", "우전 적시타", at=1.0)], size=100)
SC['g4'] = box(hi=[4], upto=4, cont=False, marks=[dict(row=0, inn=2, label="선취점", at=-1), dict(row=1, inn=4, label="반격", at=2.0)])
SC['g5'] = S(0, "people", title="4회 · KIA 공격", items=[pc("김도영B", "김도영", "KIA", "우중간 2루타", at=0), pc("나성범", "나성범", "KIA", "몸에 맞는 공", at=1.0), pc("한준수", "한준수", "KIA", "동점 적시타", at=3.0)], size=100)
SC['p0'] = S(0, "duel", title="4차전 · 두 선발", left=dict(img=P["페덱"], name="페덱", team="삼성", role="삼성 선발", at=0.2), right=dict(img=P["네일"], name="네일", team="KIA", role="KIA 선발", at=0.4), vsAt=0.3)
SC['p1'] = pv("페덱", "페덱", "삼성 선발 · 4차전", [vstamp("반등", 2.0, "gold", size=60)], stats=[st("4차전", "5⅓이닝 1실점", 1.0, hi=True), st("1차전", "5실점", 2.0)])
SC['p3'] = pv("네일", "네일", "KIA 선발 · 4차전", [], stats=[st("4차전", "5이닝 1실점", 1.0, hi=True)])
SC['g7'] = pv("최형우G", "최형우", "삼성 · 4차전", [vstamp("세 번째 승부처", 0.3, "gold", size=52)], stats=[st("6회", "솔로 홈런", 1.0, hi=True)], imgAt=2.0, chain="chw")
SC['g8'] = pv("최형우G", "최형우", "삼성 · 4차전", [vstamp("삼성 2대1", 2.0, "gold", size=56)], stats=[st("6회", "솔로 홈런", -1, hi=True), st("상대 투수", "곽도규", 0.2)], chain="chw", cont=True)
SC['g9'] = pv("최형우G", "최형우", "삼성 · 4차전", [vstamp("삼성 2대1", -1, "gold", size=56)], stats=[st("6회", "솔로 홈런", -1, hi=True), st("상대 투수", "곽도규", -1), st("이번 플레이오프", "두 번째 홈런", 0.5, hi=True)], chain="chw", cont=True)
SC['g11'] = box(hi=[7], upto=6, cont=False, marks=[dict(row=0, inn=6, label="홈런", at=-1)], text="마지막 승부처 · 7회", textAt=1.0)
SC['g12'] = box(hi=[7], upto=6, marks=[dict(row=0, inn=6, label="홈런", at=-1)], text="시작은 실책", textAt=0.2)
_r7 = lambda a, b, c, d, e, txt, ta, **k: S(0, "people", title="7회 · KIA 공격", items=[pc("김영웅", "김영웅", "삼성", "3루수 실책", at=a), pc("김도영B", "김도영", "KIA", "출루 · 득점", at=b), pc("카스트로", "카스트로", "KIA", "동점 안타", at=c), pc("김선빈", "김선빈", "KIA", "중전 안타", at=d), pc("한준수", "한준수", "KIA", "역전 적시타", at=e)], size=80, chain="r7", text=txt, textAt=ta, **k)
SC['g13'] = _r7(0.2, 1.0, 50, 50, 50, "2대2", 50)
SC['g14'] = _r7(-1, -1, 0.2, 3.0, 50, "2대2", 2.0, cont=True)
SC['g15'] = _r7(-1, -1, -1, -1, 1.0, "3대2", 3.0, cont=True)
SC['g16'] = S(0, "people", title="7회 · KIA 공격", items=[pc("한준수", "한준수", "KIA", "3대2 역전", at=0), pc("하주석", "하주석", "KIA", "추가 안타", at=0.2)], size=110, text="KIA 4대2", textAt=1.0)
SC['g17'] = box(hi=[7], upto=9, cont=False, marks=[dict(row=1, inn=7, label="3점", at=0.3)], text="모두 비자책", textAt=1.0)
SC['g18'] = pv("사토시", "사토시", "삼성 투수 · 7회", [], stats=[st("앞 투수", "배찬승", 1.0), st("7회", "3실점", 2.0, hi=True), st("자책점", "0", 2.5, hi=True)])
SC['g20'] = S(0, "people", title="4차전 · 삼성 실책 3개", items=[pc("디아즈", "디아즈", "삼성", "실책", at=1.0), pc("류지혁", "류지혁", "삼성", "실책", at=1.2), pc("김영웅", "김영웅", "삼성", "실책", at=1.4)], size=100, text="4실점 중 자책점 1점", textAt=3.0)
_pjf = dict(img=P["박진만F"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤")
SC['g23'] = S(0, "faces", items=[dict(_pjf, at=0, say="“실책 후 실점하고\n역전당했다”", sayAt=1.0), dict(img=P["사토시F"], name="사토시", team="삼성", role="삼성 투수", at=50), dict(img=P["김도영F"], name="김도영", team="KIA", role="KIA 타자", at=50)], chain="pjm")
SC['g24'] = S(0, "faces", items=[dict(_pjf, at=-1, say="“제가 운영을\n잘못한 탓”", sayAt=2.0), dict(img=P["사토시F"], name="사토시", team="삼성", role="삼성 투수", at=0.3), dict(img=P["김도영F"], name="김도영", team="KIA", role="KIA 타자", at=1.0)], chain="pjm", cont=True)
SC['g26'] = S(0, "people", title="KIA 마운드 · 4차전 마지막", items=[pc("전상현", "전상현", "KIA", "2이닝 무안타 · 세이브", at=0)], size=120, text="승리투수 조상우", textAt=1.0)
SC['f11'] = S(0, "tiles", title="플레이오프 네 경기", items=[dict(v="17 : 16", k="득점 · 삼성 : KIA", at=1.0, hi=True), dict(v="32 : 28", k="안타 · KIA : 삼성", at=2.0)])
SC['f13'] = ser(4, 0, text="대구 1승 1패", textAt=1.0)
SC['f14'] = ser(4, -1, text="알 수 없는 5차전", textAt=0.5, cont=True)
SC['s1'] = S(0, "toc", on=2)
SC['s2'] = S(0, "duel", title="플레이오프 2차전 · 대구", left=dict(img=P["후라도"], name="후라도", team="삼성", role="2차전 선발", at=0), right=dict(img=P["올러"], name="올러", team="KIA", role="2차전 선발", at=0.2), vsAt=0.1)
SC['s3'] = S(0, "tiles", title="플레이오프 2차전 · 선발 결과", items=[dict(v="6⅔이닝 2실점", k="후라도 · 승", at=1.0, hi=True), dict(v="4⅔이닝 5실점", k="올러 · 패", at=4.0, color=RED)])
SC['s6'] = S(0, "tline", title="두 선발의 휴식", items=[dict(d="2차전", t="선발", at=0.3), dict(d="나흘", t="휴식", at=1.0), dict(d="5차전", t="다시 선발", c="good", at=1.5)])
SC['s7'] = S(0, "duel", title="2026 정규시즌 평균자책점", left=dict(img=P["후라도"], name="후라도", team="삼성", role="평균자책점 3.54", at=2.0), right=dict(img=P["올러"], name="올러", team="KIA", role="평균자책점 3.13", at=1.0), vsAt=1.5)
SC['s8'] = S(0, "tiles", title="플레이오프 5차전", items=[dict(v="대구", k="5차전 장소", at=0.3, hi=True)])
SC['s8b'] = pv("올러", "올러", "KIA 선발 · 5차전", [vstamp("대구에서 약했다", 1.0, "bad", size=52)], imgAt=1.0)
_ol = [st("삼성전 평균자책점", "5.79", 1.0), st("광주 두 경기", "13이닝 1실점", 3.0, color=GREEN), st("7월 28일 대구", "1이닝 8실점", 50, hi=True), st("대구 두 경기", "13실점", 50, hi=True)]
SC['s9'] = pv("올러B", "올러", "KIA 선발 · 2026 삼성전", [], stats=_ol, chain="olr2")
SC['s11'] = pv("올러B", "올러", "KIA 선발 · 2026 삼성전", [], stats=[dict(_ol[0], at=-1), dict(_ol[1], at=-1), dict(_ol[2], at=0.5), dict(_ol[3], at=3.0)], chain="olr2", cont=True)
_hr = [st("KIA전 등판", "5월 15일 대구", 1.0), st("던진 이닝", "7이닝", 2.0), st("맞은 안타", "10개", 3.0, hi=True)]
SC['s13'] = pv("후라도B", "후라도", "삼성 선발 · 2026 정규시즌", [vstamp("불안한 구석", 1.0, "bad", size=52)], stats=[dict(x, at=50) for x in _hr], chain="hr2")
SC['s14'] = pv("후라도B", "후라도", "삼성 선발 · 2026 정규시즌", [vstamp("불안한 구석", -1, "bad", size=52)], stats=_hr, chain="hr2", cont=True)
SC['s16'] = S(0, "tline", title="후라도 · 정규시즌 마지막 두 경기", items=[dict(d="10월 5일 두산전", t="6실점", c="bad", at=1.0), dict(d="10월 11일 KT전", t="6실점", c="bad", at=2.0)])
SC['s18'] = pv("후라도", "후라도", "삼성 선발 · 플레이오프 2차전", [vstamp("흐름을 끊은 2차전", 1.0, "gold", size=52)])
SC['s19'] = S(0, "duel", title="정리 · 5차전 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="대구 · 이번 시리즈 우위", at=3.0), right=dict(img=P["올러"], name="올러", team="KIA", role="정규시즌 기록 우위", at=1.0), vsAt=2.0)
SC['b1'] = S(0, "toc", on=3)
SC['b1b'] = S(0, "tiles", title="플레이오프 5차전", items=[dict(v="마지막 경기", k="지면 끝", at=0.5, hi=True)])
SC['b2'] = S(0, "faces", items=[dict(_pjf, at=0, say="“페덱·최원태 빼고\n불펜 다 쓸 수 있게”", sayAt=2.0), dict(img=P["페덱F"], name="페덱", team="삼성", role="4차전 선발", at=1.0), dict(img=P["최원태F"], name="최원태", team="삼성", role="3차전 선발", at=1.3)], chain="b2f")
SC['b3'] = S(0, "faces", items=[dict(_pjf, at=-1, say="“페덱·최원태 빼고\n불펜 다 쓸 수 있게”", sayAt=-1), dict(img=P["페덱F"], name="페덱", team="삼성", role="4차전 선발", at=-1), dict(img=P["최원태F"], name="최원태", team="삼성", role="3차전 선발", at=-1)], chain="b2f", cont=True)
SC['b5'] = pv("후라도", "후라도", "삼성 선발 · 5차전", [vstamp("흔들리면 바로 불펜", 1.0, "gold", size=52)])
SC['b13'] = pv("원태인", "원태인", "삼성 투수 · 플레이오프", [vstamp("5차전도 대기?", 3.0, "gold", size=52)], stats=[st("3차전", "불펜 등판", 0.3), st("3차전 결과", "1⅔이닝 · 승리투수", 1.0, hi=True)], imgAt=2.0)
SC['b9'] = S(0, "cells", title="삼성 불펜 · 플레이오프 등판", cols=4, cw=330, ch=130, items=[dict(t="이승민 · 네 경기", hi=True, at=0.3, fs=36), dict(t="배찬승 · 세 경기", at=2.0, fs=36), dict(t="김태훈 · 세 경기", at=2.2, fs=36), dict(t="사토시 · 세 경기", at=2.4, fs=36)], label="피로 누적?", labelAt=4.0)
SC['b6'] = pvt("KIA", "KIA 불펜", "플레이오프 5차전", [vstamp("사정은 비슷", 0.3, "bad", size=56)])
SC['b11'] = pv("전상현", "전상현", "KIA 불펜 · 플레이오프", [], stats=[st("세 경기", "4⅔이닝", 1.0), st("실점", "없음", 2.0, hi=True), st("4차전", "22구", 3.0)])
SC['b12'] = pv("조상우", "조상우", "KIA 불펜 · 플레이오프", [], stats=[st("세 경기", "4⅓이닝", 1.0), st("3차전", "2실점 · 패", 2.0, hi=True)])
SC['b7b'] = S(0, "tline", title="두 팀 불펜 일정", items=[dict(d="4차전", t="경기", at=1.0), dict(d="하루", t="휴식", c="good", at=2.0), dict(d="5차전", t="경기", at=2.5)])
SC['b8'] = pv("올러B", "올러", "KIA 선발 · 5차전", [vstamp("일찍 내려가면 불펜 부담", 2.0, "bad", size=48)], imgAt=1.0)
SC['k0'] = S(0, "toc", on=4)
SC['k1'] = pv("한준수", "한준수", "KIA 지명타자", [vstamp("KIA 키플레이어", 0.3, "gold", size=56)], imgAt=0.2, chain="hjs")
SC['k2'] = pv("한준수", "한준수", "KIA 지명타자 · 플레이오프", [], stats=[st("네 경기", "12타수 5안타", 1.5, hi=True), st("1차전", "홈런", 2.0), st("4차전", "동점타 · 결승타", 3.0, hi=True)])
SC['k4'] = pv("김도영", "김도영", "KIA 타자 · 플레이오프", [], stats=[st("네 경기", "16타수 7안타", 1.0, hi=True), st("3차전", "홈런", 2.0)])
SC['k6'] = S(0, "people", title="5차전 · KIA 타선의 숙제", items=[pc("김도영B", "김도영", "KIA", "출루", at=1.0), pc("한준수B", "한준수", "KIA", "불러들이기", at=2.0), pc("후라도B", "후라도", "삼성", "삼성 선발", at=4.0)], size=100)
SC['k7'] = pv("최형우G", "최형우", "삼성 타자", [vstamp("삼성 키플레이어", 0.3, "gold", size=56)], imgAt=0.2, chain="chk")
SC['k8'] = pv("최형우G", "최형우", "삼성 타자 · 플레이오프", [], stats=[st("홈런", "2차전 · 4차전", 1.0, hi=True), st("4차전 삼성 2득점 중", "1점", 2.0)], chain="chk2")
SC['k10'] = pv("최형우G", "최형우", "삼성 타자 · 플레이오프", [vstamp("먼저 타점을 올리면", 1.0, "gold", size=52)], stats=[st("홈런", "2차전 · 4차전", -1, hi=True), st("4차전 삼성 2득점 중", "1점", -1)], chain="chk2", cont=True)
SC['z1'] = S(0, "toc", on=5)
SC['z1b'] = pvt("삼성", "5차전 예상", "플레이오프 5차전 · 대구", [vstamp("삼성 승리", 0.5, "gold", size=60)], stats=[st("이유", "세 가지", 50)], chain="zz")
SC['z1c'] = pvt("삼성", "5차전 예상", "플레이오프 5차전 · 대구", [vstamp("삼성 승리", -1, "gold", size=60)], stats=[st("이유", "세 가지", 0.3)], chain="zz", cont=True)
SC['z2'] = pv("올러", "올러", "KIA 선발 · 5차전", [vstamp("첫째 · 대구 성적", 0.3, "bad", size=52)], chain="zo")
SC['z3'] = pv("올러", "올러", "KIA 선발 · 5차전", [vstamp("첫째 · 대구 성적", -1, "bad", size=52)], stats=[st("대구 두 경기", "모두 무너짐", 1.0, hi=True)], chain="zo", cont=True)
SC['z4'] = pv("후라도", "후라도", "삼성 선발 · 5차전", [vstamp("둘째 · 후라도", 0.2, "gold", size=52)], chain="zh")
SC['z5'] = pv("후라도", "후라도", "삼성 선발 · 5차전", [vstamp("둘째 · 후라도", -1, "gold", size=52)], stats=[st("이번 시리즈", "KIA 상대 승리", 1.5, hi=True)], chain="zh", cont=True)
SC['z6'] = S(0, "people", title="셋째 · 삼성 중심 타선", items=[pc("디아즈", "디아즈", "삼성", "홈런 두 개", at=0.3), pc("최형우G", "최형우", "삼성", "홈런 두 개", at=0.5)], size=110)
SC['z7'] = S(0, "people", title="플레이오프 2차전 · 3회", items=[pc("디아즈", "디아즈", "삼성", "투런 홈런", at=2.0), pc("올러B", "올러", "KIA", "KIA 선발", at=3.0)], size=110)
SC['z9'] = S(0, "question", text="뒤집힐 조건 네 가지", logos=["KIA"], logoSize=180, size=96)
SC['z10'] = pv("올러B", "올러", "KIA 선발 · 5차전", [vstamp("첫째 · 5이닝 이상 버티면", 1.0, "gold", size=48)], imgAt=1.0)
SC['z11b'] = pvt("삼성", "삼성 수비", "플레이오프 5차전", [vstamp("둘째 · 또 실책이 나오면", 1.0, "bad", size=48)])
SC['z11'] = S(0, "tiles", title="삼성 실책", items=[dict(v="최소", k="정규시즌 · SSG와 공동", at=1.0), dict(v="7개", k="플레이오프 네 경기", at=3.0, color=RED, hi=True), dict(v="1개", k="KIA 플레이오프", at=4.0)])
SC['z12'] = pv("후라도B", "후라도", "삼성 선발 · 5차전", [vstamp("셋째 · 크게 흔들리면", 2.0, "bad", size=48)], imgAt=1.0)
SC['z12b'] = S(0, "people", title="넷째 조건", items=[pc("디아즈", "디아즈", "삼성", "막히면", at=1.0), pc("최형우G", "최형우", "삼성", "막히면", at=1.2)], size=110)
SC['z13'] = S(0, "question", text="예상 점수\n삼성 5대3 승", logos=["삼성", "KIA"], logoSize=200, size=104)
SC['z14'] = S(0, "question", text="한국시리즈에 가는 팀은?\n삼성? KIA?", logos=["삼성", "KIA"], logoSize=200, size=96)

# ── 10/31 v8b 8분 보강(사용자 "8분에 맞춰줘"): 정규시즌 맞대결·막판 흐름, 1~3차전 선발, 시즌 기록, KIA 총력전, 1번 타자, 카스트로·디아즈 ──
P.update({"이의리": "경기/이의리_상체_KIA제공_세로", "구자욱": "카드/P22_구자욱_세리머니", "시라카와": "경기/시라카와_투구_KIA제공_세로", "양현종": "경기/양현종_글러브_1012_KIA제공_세로",
          "박재현": "경기/박재현_주루_KIA제공_세로", "김지찬": "상황별/김지찬_상체", "이범호": "경기/이범호_박수_0915_KIA제공_세로"})
SC['r1'] = S(0, "matchup", left="삼성", right="KIA", score="7 : 9", text="2026 정규시즌 상대전적 · KIA 9승 7패", tag="정규시즌")
SC['r2'] = S(0, "tiles", title="2026 정규시즌 최종 순위", items=[dict(v="2위", k="삼성", at=0.3), dict(v="3위", k="KIA", at=0.6)])
SC['r3'] = S(0, "bars", title="정규시즌 마지막 10경기 · 승수", items=[dict(label="삼성", team="삼성", sub="4승 6패 · 마지막 4연패", value=4, unit="승", at=0.3, color=RED), dict(label="KIA", team="KIA", sub="7승 3패", value=7, unit="승", at=2.0, hi=True)], max=10)
SC['r4'] = S(0, "series5", title="2026 준플레이오프 · KIA vs LG", games=[dict(n="1차전", venue="광주", home="KIA", win="KIA", at=1.0), dict(n="2차전", venue="광주", home="KIA", win="KIA", at=1.3), dict(n="3차전", venue="잠실", home="LG", win="KIA", at=1.6)])
SC['f3b'] = S(0, "people", title="1차전 · KIA 마운드", items=[pc("네일", "네일", "KIA", "선발 4⅓이닝 1실점", at=0), pc("이의리", "이의리", "KIA", "불펜 · 승리투수", at=2.0)], size=110)
SC['f6b'] = S(0, "people", title="2차전 · 삼성", items=[pc("구자욱", "구자욱", "삼성", "3회 결승 적시타", at=1.0), pc("후라도", "후라도", "삼성", "6⅔이닝 2실점", at=2.0)], size=110)
SC['f7b'] = pv("최원태", "최원태", "삼성 선발 · 3차전", [vstamp("불펜이 버텼다", 3.0, "gold", size=52)], stats=[st("3차전", "1⅔이닝 강판", 2.0, hi=True)], imgAt=1.0)
SC['f7c'] = pv("시라카와", "시라카와", "KIA 선발 · 3차전", [], stats=[st("3차전", "4⅓이닝 4실점", 1.0, hi=True)])
SC['s1b'] = S(0, "duel", title="2026 정규시즌 · 두 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="24경기 9승 3패", at=1.0), right=dict(img=P["올러"], name="올러", team="KIA", role="30경기 11승 10패", at=2.0), vsAt=1.5)
SC['s1c'] = S(0, "tiles", title="2026 정규시즌 · 두 선발", items=[dict(v="150 : 178", k="이닝 · 후라도 : 올러", at=1.0), dict(v="17 : 19", k="퀄리티스타트", at=3.0, hi=True)])
SC['b6b'] = S(0, "faces", items=[dict(img=P["이범호"], name="이범호", team="KIA", role="KIA 감독 · 4차전 뒤", at=0, say="“모든 선수가\n대기해야 하는 상황”", sayAt=2.0)])
SC['b6c'] = pv("양현종", "양현종", "KIA 투수 · 5차전", [vstamp("불펜 대기", 1.0, "gold", size=56)], imgAt=0.5, chain="yhj")
SC['b6d'] = pv("양현종", "양현종", "KIA 투수 · 5차전", [vstamp("불펜 대기", -1, "gold", size=56)], stats=[st("이번 플레이오프", "등판 없음", 1.0, hi=True)], chain="yhj", cont=True)
SC['t1'] = S(0, "duel", title="두 팀 1번 타자", left=dict(img=P["김지찬"], name="김지찬", team="삼성", role="삼성 1번", at=1.0), right=dict(img=P["박재현"], name="박재현", team="KIA", role="KIA 1번", at=1.0), vsAt=1.0, chain="lead")
SC['t2'] = S(0, "duel", title="두 팀 1번 타자 · 플레이오프", left=dict(img=P["김지찬"], name="김지찬", team="삼성", role="17타수 3안타", at=2.0), right=dict(img=P["박재현"], name="박재현", team="KIA", role="18타수 2안타", at=1.0), vsAt=0.5)
SC['t3'] = pvt("KIA", "5차전 타선", "플레이오프 5차전", [vstamp("승부는 뒤에서 치는 타자들", 1.0, "gold", size=48)])
SC['k5'] = pv("카스트로", "카스트로", "KIA 타자 · 플레이오프", [], stats=[st("네 경기", "15타수 5안타", 1.0), st("타점", "5개", 2.0, hi=True)])
SC['k8b'] = pv("디아즈", "디아즈", "삼성 타자 · 플레이오프", [], stats=[st("네 경기", "14타수 3안타", 1.0), st("홈런", "2개", 2.0, hi=True), st("타점", "4개", 3.0)])

# 10/31 사전검사(v8b)
SC['p0'] = box(upto=5, cont=False, marks=[dict(row=0, inn=2, label="선취점", at=-1), dict(row=1, inn=4, label="반격", at=-1)], text="선발 싸움 팽팽", textAt=0.5)
SC['g13'] = _r7(0.2, 1.0, 50, 50, 50, "실책 출루", 0.5)
SC['g18'] = pv("사토시", "사토시", "삼성 투수 · 7회", [], stats=[st("앞 투수", "배찬승", 1.0), st("7회", "3실점", 2.0, hi=True), st("자책점", "0", 2.5, hi=True)], imgAt=1.0)
SC['g23'] = S(0, "faces", items=[dict(img=P["박진만"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤", at=0, say="“실책 후 실점하고\n역전당했다”", sayAt=1.0)], chain="pjm")
SC['g24'] = S(0, "faces", items=[dict(img=P["박진만"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤", at=-1, say="“제가 운영을\n잘못한 탓”", sayAt=1.0)], chain="pjm", cont=True)
SC['g26'] = S(0, "people", title="KIA 마운드 · 4차전 마지막", items=[pc("전상현", "전상현", "KIA", "2이닝 무안타 · 세이브", at=1.0)], size=120)
_pj3 = dict(img=P["박진만"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤")
SC['b2'] = S(0, "faces", items=[dict(_pj3, at=0, say="“페덱·최원태 빼고\n불펜 다 쓸 수 있게”", sayAt=2.0), dict(img=P["페덱"], name="페덱", team="삼성", role="4차전 선발", at=1.0), dict(img=P["최원태"], name="최원태", team="삼성", role="3차전 선발", at=1.3)], chain="b2f")
SC['b3'] = S(0, "faces", items=[dict(_pj3, at=-1, say="“페덱·최원태 빼고\n불펜 다 쓸 수 있게”", sayAt=-1), dict(img=P["페덱"], name="페덱", team="삼성", role="4차전 선발", at=-1), dict(img=P["최원태"], name="최원태", team="삼성", role="3차전 선발", at=-1)], chain="b2f", cont=True)
SC['b13'] = pv("원태인", "원태인", "삼성 투수 · 플레이오프", [vstamp("5차전도 대기?", 4.0, "gold", size=52)], stats=[st("3차전", "불펜 등판", 0.3), st("3차전 결과", "1⅔이닝 · 승리투수", 1.0, hi=True)], imgAt=3.0)

SC['f6b'] = S(0, "people", title="2차전 · 삼성", items=[pc("구자욱", "구자욱", "삼성", "3회 결승 적시타", at=1.0), pc("후라도", "후라도", "삼성", "7회 2아웃까지 2실점", at=2.0)], size=110)
SC['b6b'] = S(0, "faces", items=[dict(img=P["이범호"], name="이범호", team="KIA", role="KIA 감독 · 4차전 뒤", at=0, say="“모든 선수가\n대기해야 하는 상황”", sayAt=3.0), dict(img=P["올러"], name="올러", team="KIA", role="5차전 선발", at=1.0), dict(img=P["네일"], name="네일", team="KIA", role="대기 제외", at=2.0)])
SC['t1'] = S(0, "question", text="두 팀 1번 타자", logos=["삼성", "KIA"], logoSize=180, size=96)
SC['t2'] = S(0, "duel", title="두 팀 1번 타자 · 플레이오프", left=dict(img=P["김지찬"], name="김지찬", team="삼성", role="17타수 3안타", at=2.0), right=dict(img=P["박재현"], name="박재현", team="KIA", role="18타수 2안타", at=0), vsAt=1.0)
SC['s1c'] = S(0, "tiles", title="2026 정규시즌 · 던진 이닝", items=[dict(v="150이닝", k="후라도", at=1.0), dict(v="178이닝", k="올러", at=2.0, hi=True)])
SC['s1d'] = S(0, "tiles", title="2026 정규시즌 · 퀄리티스타트", items=[dict(v="17번", k="후라도", at=1.0), dict(v="19번", k="올러", at=2.0, hi=True)])

SC['s1b'] = S(0, "duel", title="2026 정규시즌 · 두 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="24경기 9승 3패", at=1.0), right=dict(img=P["올러"], name="올러", team="KIA", role="30경기 11승 10패", at=2.0), vsAt=1.5, chain="sd")
SC['s1c'] = S(0, "duel", title="2026 정규시즌 · 두 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="150이닝", at=-1), right=dict(img=P["올러"], name="올러", team="KIA", role="178이닝", at=-1), vsAt=-1, chain="sd", cont=True)
SC['s1d'] = S(0, "duel", title="2026 정규시즌 · 두 선발", left=dict(img=P["후라도"], name="후라도", team="삼성", role="퀄리티스타트 17경기", at=-1), right=dict(img=P["올러"], name="올러", team="KIA", role="퀄리티스타트 19경기", at=-1), vsAt=-1, chain="sd", cont=True)

# ── 10/31 v9 보강(사용자 "넣을만한거라면 다 넣자"): 두 감독 각오·홈/원정·김도영 2번·병살타·KT 상대전적 ──
SC['p3'] = pv("네일", "네일", "KIA 선발 · 4차전", [], stats=[st("휴식", "사흘", 1.0), st("4차전", "5이닝 1실점", 2.0, hi=True)])
SC['f15'] = S(0, "faces", items=[dict(img=P["박진만"], name="박진만", team="삼성", role="삼성 감독 · 4차전 뒤", at=0, say="“선수들은 어려울 때\n잘 이겨 냈다”", sayAt=1.0)])
SC['f16'] = S(0, "faces", items=[dict(img=P["이범호"], name="이범호", team="KIA", role="KIA 감독 · 4차전 뒤", at=0, say="“광주에서 한국시리즈를\n팬들에게 보여 주고 싶다”", sayAt=2.0)])
SC['h1'] = S(0, "bars", title="2026 정규시즌 · 홈과 원정", items=[dict(label="삼성 홈", team="삼성", sub="43승 1무 29패", value=43, unit="승", at=1.0, hi=True), dict(label="KIA 원정", team="KIA", sub="37승 34패", value=37, unit="승", at=50)], max=50, chain="ha")
SC['h2'] = S(0, "bars", title="2026 정규시즌 · 홈과 원정", items=[dict(label="삼성 홈", team="삼성", sub="43승 1무 29패", value=43, unit="승", at=-1, hi=True), dict(label="KIA 원정", team="KIA", sub="37승 34패", value=37, unit="승", at=0.5)], max=50, chain="ha", cont=True)
SC['k4b'] = S(0, "faces", items=[dict(img=P["이범호"], name="이범호", team="KIA", role="KIA 감독", at=0, say="“한 타석이라도\n더 내보내려고”", sayAt=2.0), dict(img=P["김도영B"], name="김도영", team="KIA", role="2번 타자", at=1.0)])
SC['z11d'] = S(0, "bars", title="플레이오프 네 경기 · 병살타", items=[dict(label="삼성", team="삼성", value=4, unit="개", at=2.0, color=RED, hi=True), dict(label="KIA", team="KIA", value=0, unit="개", at=3.0, color=GRAY)], max=5)
SC['x1'] = S(0, "question", text="한국시리즈 상대\n정규시즌 1위 KT", logos=["KT"], logoSize=220, size=96)
SC['x2'] = S(0, "tiles", title="2026 정규시즌 · KT 상대전적", items=[dict(v="7승 9패", k="KT vs 삼성", at=1.0, color=RED), dict(v="10승 6패", k="KT vs KIA", at=2.0)])
SC['x3'] = S(0, "tiles", title="2026 정규시즌 · KT 상대전적", items=[dict(v="7승 9패", k="KT vs 삼성", at=-1, color=RED, hi=True), dict(v="10승 6패", k="KT vs KIA", at=-1)])

# ── 10/31 v9b 대사 검수(X 32) 반영: 반복·주어·끝말 정리에 맞춘 장면 ──
SC['f6b'] = S(0, "people", title="2차전 · 결승타", items=[pc("구자욱", "구자욱", "삼성", "3회 결승 적시타", at=1.0)], size=120)
SC['f7b'] = pv("최원태", "최원태", "삼성 선발 · 3차전", [], stats=[st("3차전", "1⅔이닝 강판", 2.0, hi=True)], imgAt=1.0)
SC['g8'] = pv("최형우G", "최형우", "삼성 · 4차전", [vstamp("삼성 2대1", 2.0, "gold", size=56)], stats=[st("6회", "솔로 홈런", -1, hi=True)], chain="chw", cont=True)
SC['g18'] = pv("사토시", "사토시", "삼성 투수 · 7회", [], stats=[st("7회 3점", "모두 실책 뒤", 1.0), st("앞 투수", "배찬승", 2.0), st("자책점", "0", 3.0, hi=True)], imgAt=2.0)
SC['b13'] = pv("원태인", "원태인", "삼성 투수 · 플레이오프", [vstamp("5차전도 대기?", 4.0, "gold", size=52)], stats=[st("3차전", "불펜 등판", 1.0), st("3차전 결과", "1⅔이닝 · 승리투수", 3.0, hi=True)], imgAt=3.0)
SC['k6'] = S(0, "people", title="4차전 4회처럼", items=[pc("김도영B", "김도영", "KIA", "출루", at=2.0), pc("한준수B", "한준수", "KIA", "불러들이기", at=3.0), pc("후라도B", "후라도", "삼성", "삼성 선발", at=4.0)], size=100)
SC['k8'] = pv("최형우G", "최형우", "삼성 타자 · 플레이오프", [], stats=[st("홈런", "2차전 · 4차전", 1.0, hi=True)], chain="chk2")
SC['z7'] = S(0, "people", title="플레이오프 · 삼성 홈런 5개", items=[pc("디아즈", "디아즈", "삼성", "홈런 2개", at=1.0), pc("최형우G", "최형우", "삼성", "홈런 2개", at=1.2), pc("올러B", "올러", "KIA", "2차전 투런 허용", at=4.0)], size=100)
SC['s16'] = S(0, "tline", title="후라도 · 정규시즌 마지막 두 경기", items=[dict(d="10월 5일 두산전", t="6실점", c="bad", at=2.0), dict(d="10월 11일 KT전", t="6실점", c="bad", at=3.0)])
SC['z5'] = pv("후라도", "후라도", "삼성 선발 · 5차전", [vstamp("둘째 · 후라도", -1, "gold", size=52)], stats=[st("이번 시리즈", "KIA 상대 승리", 3.0, hi=True)], chain="zh", cont=True)
SC['z7'] = S(0, "people", title="플레이오프 · 삼성 홈런 5개", items=[pc("최형우G", "최형우", "삼성", "홈런 2개", at=0), pc("디아즈", "디아즈", "삼성", "홈런 2개", at=3.0), pc("올러B", "올러", "KIA", "2차전 투런 허용", at=4.0)], size=100)
# 10/31 02:40 사용자 "시작은 실책이었죠 하고 텀이 너무 길어" → 짧은 줄에 새 글이 늦게 떠서 생긴 텀: 새 요소 없이 앞 장면 유지 / 바로 뜨게
SC['g12'] = box(hi=[7], upto=6, marks=[dict(row=0, inn=6, label="홈런", at=-1)], text="마지막 승부처 · 7회", textAt=-1)
SC['s8'] = S(0, "tiles", title="플레이오프 5차전", items=[dict(v="대구", k="5차전 장소", at=0, hi=True)])
SC['z6'] = S(0, "people", title="셋째 · 삼성 중심 타선", items=[pc("디아즈", "디아즈", "삼성", "홈런 2개", at=0), pc("최형우G", "최형우", "삼성", "홈런 2개", at=0)], size=110, chain="z67")
SC['z7'] = S(0, "people", title="셋째 · 삼성 중심 타선", items=[pc("디아즈", "디아즈", "삼성", "홈런 2개", at=-1), pc("최형우G", "최형우", "삼성", "홈런 2개", at=-1), pc("올러B", "올러", "KIA", "2차전 투런 허용", at=4.0)], size=110, chain="z67", cont=True)
SC['s8'] = S(0, "tiles", title="플레이오프 5차전", items=[dict(v="대구", k="5차전 장소", at=1.0, hi=True)])
SC['s8b'] = pv("올러", "올러", "KIA 선발 · 5차전", [vstamp("대구에서 약했다", 1.0, "bad", size=52)], imgAt=0)
SC['z6'] = S(0, "people", title="셋째 · 삼성 중심 타선", items=[pc("디아즈", "디아즈", "삼성", "삼성 타자", at=0), pc("최형우G", "최형우", "삼성", "삼성 타자", at=0), pc("올러B", "올러", "KIA", "2차전 투런 허용", at=50)], size=110, chain="z67")
SC['z7'] = S(0, "people", title="플레이오프 · 삼성 홈런 5개 중 4개", items=[pc("디아즈", "디아즈", "삼성", "홈런 2개", at=-1), pc("최형우G", "최형우", "삼성", "홈런 2개", at=-1), pc("올러B", "올러", "KIA", "2차전 투런 허용", at=4.0)], size=110, chain="z67", cont=True)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scenes_v10.py'), encoding='utf-8').read())
for _k in [k for k in SC if k not in KEYS]: SC.pop(_k)
missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing and not extra, (missing, extra)
lines, scenes = [], []
for j, (k, narr, sub) in enumerate(_t.LINES):
    sc = dict(SC[k]); sc['startLine'] = j
    lines.append(L(narr, sub)); scenes.append(sc)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})
for s in scenes:
    if s.get('type') in ('tline', 'bars', 'cells', 'tiles', 'faces', 'rally', 'steps', 'pgroup', 'people', 'scoreboard'): s['noCenter'] = True

def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
CH = [ch("1~3차전 흐름", "f1", "f10b"), ch("4차전 승부처", "g0", "f16"), ch("5차전 선발 맞대결", "s1", "s19"), ch("5차전 불펜 운용", "b1", "b8"), ch("두 팀 키플레이어", "k0", "k10"), ch("5차전 예상", "z1", "z14")]

DESC = ("플레이오프 4차전 리뷰와 5차전 승부예측 — KIA가 삼성을 4대2로 꺾고 시리즈 2승 2패, 11월 1일 대구 5차전에서 한국시리즈 티켓이 갈려요.\n"
        "삼성 후라도와 KIA 올러, 다시 만나는 두 선발 중 누가 웃을까요? 1~3차전 흐름, 4차전 승부처(7회 실책 뒤 3점), 선발·불펜·키플레이어와 제 예상까지 정리했어요.\n\n"
        "4차전은 2회 삼성 선취점, 4회 한준수 동점타, 6회 최형우 솔로 홈런, 7회 김영웅 실책 뒤 카스트로·김선빈·한준수·하주석 안타로 KIA가 뒤집었어요. 삼성 4실점 중 자책점은 1점뿐이었어요.\n\n"
        "올러는 2026년 대구 두 경기(플레이오프 2차전 포함)에서 13실점, 광주 두 경기에선 13이닝 1실점이에요. 후라도는 플레이오프 2차전에서 6⅔이닝 2실점으로 KIA를 눌렀어요.\n\n"
        "제 예상은 삼성의 5대3 승리예요. 뒤집힐 조건은 올러의 5이닝 이상 호투, 삼성 실책(플레이오프 4경기 7개), 후라도 부진, 디아즈·최형우 침묵이에요.\n\n"
        "삼성이 한국시리즈에 갈까요? 아니면 KIA가 한국시리즈에 갈까요? 댓글로 알려 주세요.\n\n"
        "기록 출처: KBO 기록실(2026 플레이오프 1~4차전 박스스코어, 선수 일자별·시즌 기록, 팀 순위·팀간 승패, 팀 수비)\n"
        "기사 출처: 스포츠경향·일간스포츠 10/30(박진만 감독), 일간스포츠·뉴스1 10/30(이범호 감독), 한국일보·스타뉴스 10/30\n"
        "사진 출처: 삼성 라이온즈 제공, KIA 타이거즈 제공, KBO")
TAGS = ["플레이오프", "플레이오프 4차전", "플레이오프 5차전", "삼성 KIA", "삼성 라이온즈", "KIA 타이거즈", "PO 5차전 예측", "한국시리즈", "후라도", "올러", "한준수", "김도영", "최형우",
        "박진만", "이범호", "사토시", "미야모리", "네일", "페덱", "전상현", "조상우", "프로야구", "KBO", "야구자판기"]
SOURCE = "사실 출처 = KBO 기록실(4차전 박스스코어·선수 일자별·팀 수비, 10/30~31 조회) + 기사 원문(스포츠경향·일간스포츠·한국일보·스타뉴스) — scratchpad audit/1030_po45/facts/근거모음.md"
EP = {"introChapter": "오프닝", "date": "2026-10-31", "gameDate": "2026-10-30", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.15,
      "rev": "1031-long34-v1", "topic": "PO4차전리뷰5차전예측", "endcardSec": 30, "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 5000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE, "youtube": {"title": "플레이오프 5차전 예측 | 삼성 후라도 vs KIA 올러, 한국시리즈 가는 팀은? #플레이오프 #삼성 #KIA",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#플레이오프", "#플레이오프5차전", "#삼성라이온즈", "#KIA타이거즈", "#후라도", "#올러", "#한국시리즈", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'z13', 'z14')}
    HOLD = {KEYS.index(k): 0.35 for k in ('o4', 'r4', 'f10b', 'f14', 's19', 'b8', 'k10')}
    pass
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
        pass  # 10/31 사용자 '텀 너무 길게 하지 마' → 키플레이어 뒤 정지(holdAfter) 없앰
    lines[-2]['gapAfter'] = 0.4
    _gf = os.path.join(HERE, 'gapfix_1031_long34.json')
    if os.path.exists(_gf):
        for _k, _g in json.load(open(_gf, encoding='utf-8')).items(): EP['lines'][KEYS.index(_k)]['gapAfter'] = max(EP['lines'][KEYS.index(_k)].get('gapAfter', 0.25), _g)
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-31_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
