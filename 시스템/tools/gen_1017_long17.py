# -*- coding: utf-8 -*-
"""10/17 롱폼⑰ 「준플레이오프 1차전 리뷰 · 승부를 가른 이유 · 2차전 예측」 (음성 API · 줄별 배속).
대사 = tools/text_1017_long17.py. 근거 = KBO 게임센터 박스스코어(GetBoxScoreScroll srId=3, 20261017LGHT0) 10/17 직접 조회 + 기사 원문
(이범호·염경엽 일문일답 스포티비뉴스, 동아일보, 스포츠조선, MK스포츠, 이코노믹리뷰) + 롱폼⑮ 근거(KBO 기록실 10/15) — 프로젝트 claude/1017-롱폼17-준PO1차전-*.
경기 장면 = diamond(이닝별 결과는 박스스코어 타자 기록으로 재구성). 사진 = 오늘 경기 KIA 타이거즈 제공 사진(경기/*_1017_KIA제공 · 카드/P17_*) + 기존 카드."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1017_long17.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]

def pre(t):
    t = t.replace('1만 8,900석', '만 팔천구백 석')
    for a, b in (('5대1', '오 대 일'), ('3대1', '삼 대 일'), ('1대1', '일 대 일')): t = t.replace(a, b)
    t = t.replace('10월', '시월').replace('5전 3선승제', '오 전 삼 선승제').replace('MVP', '엠브이피').replace('75%', '칠십오 퍼센트')
    t = t.replace('1번 박재현', '일 번 박재현').replace('2번 김선빈', '이 번 김선빈').replace('1번 홍창기', '일 번 홍창기')
    t = t.replace('고의4구', '고의사구')   # 10/17 사용자: '고의 사구'(띄어 씀)는 타입캐스트가 '고에 사구'로 읽음 → 붙여서 '고의사구'로 읽게
    return t
def narr_of(t):
    # 10/17 사용자 "2루로/뛰다잡혔어요 → 2루로 뛰다/잡혔어요": '이 루로'처럼 숫자와 '루'가 떨어지면 타입캐스트가 그 사이에서 쉰다 → 붙여 쓴다(일루·이루·삼루)
    t = re.sub(r'(일|이|삼) 루', r'\1루', narr_of15(pre(t)))
    # 10/18 사용자 "이제 이/차전을 — 텀 없이 해야": '이 차전'처럼 수(이·일·삼…)와 '차전·연승'이 떨어지면 타입캐스트가 '이(this) / 차전'으로 끊어 읽는다 → 붙여 쓴다(이차전·이연승)
    return re.sub(r'(일|이|삼|사|오|칠|팔) (차전|연승|연패)', r'\1\2', t)
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vduo(items, **k): return dict(type="duo", items=items, **k)
RED, GOLD, GRAY, GREEN, NAVY = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55", "#3B4A63"
KIAC, LGB = "#C70125", "#2563EB"
TCKL = {"LG": LGB}
C = '카드/'
G = '경기/'
def pv(i, img, name, sub, viz, **k): return S(i, "pstat", img=img, name=name, sub=sub, stats=k.pop("stats", []), viz=viz, noCenter=True, **k)
def sp(i, img, name, sub, bubbles, **k): return S(i, "speech", img=img, name=name, sub=sub, bubbles=bubbles, **k)
def photo(img, **k): return S(0, "photo", img=img, fit="cover", text=k.pop("text", ""), h=k.pop("h", 760), **k)

# ── 1차전 다이아몬드(LG 원정 · KIA 홈) ──
def dm(i, title, bat, score, outs, steps, **k):
    return S(i, "diamond", title=title, bat=bat, batIdx=(0 if bat == "LG" else 1), score=score, outs=outs, steps=steps, away="LG", home="KIA", **k)
N3 = [None, None, None]

SC = {}
# 훅
SC[0] = S(0, "matchup", left="KIA", right="LG", score="5 : 1", tag="준플레이오프 1차전 · 10월 17일 광주")
SC[1] = photo(G + "김도영_세리머니_1017_KIA제공")
SC[2] = sp(0, C + "FA9_염경엽", "염경엽", "LG 감독 · 10월 14일", [bb("", "“초점은 김도영을\n어떻게 막는지다”", 1)])
SC[3] = S(0, "toc", on=-1, itemFrom=99)
# 1장 경기 흐름
SC[4] = photo(G + "광주_전경_1017_KIA제공", chain="crowd")
SC[5] = photo(G + "광주_관중_1017_KIA제공", chain="crowd", cont=True)
SC[6] = S(0, "cells", title="KIA 준플레이오프 · 해태 시절 포함", cols=4, cw=300, ch=140,
          items=[dict(t="1994", bad=True, at=1), dict(t="2004", bad=True, at=1.3), dict(t="2006", bad=True, at=1.6), dict(t="2011", bad=True, at=1.9)],
          label="네 번 모두 탈락", text="악연을 끊을 첫 경기", textAt=3)
SC[7] = S(0, "duel", title="준플레이오프 1차전 선발", left={"img": C + "P17_네일_투구", "name": "네일", "team": "KIA", "role": "KIA 선발", "at": 0},
          right={"img": C + "FA9_톨허스트_상체", "name": "톨허스트", "team": "LG", "role": "LG 선발", "at": 1}, vsAt=0.6)
SC[8] = S(0, "pgroup", title="LG 라인업 변화", items=[dict(img=C + "P15_오지환", name="오지환", team="LG", k="와일드카드 결장", v="선발 복귀", at=1, vAt=2),
                                                  dict(img=C + "P15_신민재", name="신민재", team="LG", k="2루수", v="선발 제외", at=3, vAt=3)])
SC[9] = dm(0, "1회초 · LG 공격", "LG", [0, 0], 0, [dict(at=0.5, who="홍창기", bases=N3, outs=1, label="홍창기 2루수 땅볼"),
                                              dict(at=2, who="박해민", bases=N3, outs=2, label="박해민 삼진"),
                                              dict(at=2.6, who="오스틴", bases=N3, outs=3, label="오스틴 삼진")])
SC[10] = dm(0, "2회초 · LG 공격", "LG", [0, 0], 2, [dict(at=1, bases=N3, outs=2, label="투 아웃"),
                                               dict(at=2.2, who="송찬의", hr=True, runs=1, bases=N3, outs=2, label="송찬의 솔로 홈런")])
SC[11] = dm(0, "2회말 · KIA 공격", "KIA", [1, 0], 0, [dict(at=1.4, who="카스트로", hr=True, runs=1, bases=N3, outs=0, label="카스트로 동점 솔로 홈런")])
SC[12] = dm(0, "3회초 · LG 공격", "LG", [1, 1], 0, [], lead="3회초 · 무사", chain="d3")
SC[13] = dm(0, "3회초 · LG 공격", "LG", [1, 1], 0, [dict(at=0, who="박동원", bases=["박동원", None, None], outs=0, label="박동원 볼넷"),
                                                  dict(at=2, out=["박동원"], bases=N3, outs=1, label="2루 도루 실패")], chain="d3", cont=True)
SC[14] = dm(0, "3회초 · LG 공격", "LG", [1, 1], 1, [dict(at=-1, bases=N3, outs=2, label="구본혁 유격수 땅볼"),
                                                  dict(at=0, who="홍창기", bases=["홍창기", None, None], outs=2, label="홍창기 안타"),
                                                  dict(at=0.7, who="박해민", bases=["박해민", "홍창기", None], outs=2, label="박해민 안타 · 2사 1·2루"),
                                                  dict(at=2, who="오스틴", bases=N3, outs=3, label="오스틴 유격수 뜬공")], chain="d3", cont=True)
SC[15] = dm(0, "3회말 · KIA 공격", "KIA", [1, 1], 1, [dict(at=1, who="하주석", bases=["하주석", None, None], outs=1, label="1사 · 하주석 안타"),
                                                    dict(at=2, who="박재현", out=["하주석"], bases=N3, outs=3, label="박재현 병살타")])
SC[16] = dm(0, "4회말 · KIA 공격", "KIA", [1, 1], 1, [dict(at=0, bases=N3, outs=1, label="원 아웃"),
                                                    dict(at=1.3, who="김도영", hr=True, runs=1, bases=N3, outs=1, label="김도영 역전 솔로 홈런")])
SC[17] = photo(G + "김도영_4회홈런_1017_KIA제공")   # 1차 검수: 오른쪽 글씨가 작고 치우침 → 글씨 빼고 큰 사진
SC[18] = S(0, "abdots", title="정규시즌 맞대결", left={"img": C + "FA9P_톨허스트", "name": "톨허스트", "team": "LG", "role": "LG 투수"},
           right={"img": C + "김도영_MVP_43호", "name": "김도영", "team": "KIA", "role": "KIA 3루수"}, total="9타수 2안타",
           groups=[dict(k="H", n=1, at=2, to="HR", toAt=2.4), dict(k="H", n=1, at=2), dict(k="O", n=7, at=2)], totalAt=2, cols=5,
           chips=[dict(label="1차전 · 역전 솔로 홈런", at=4, c=KIAC)])
SC[19] = pv(0, C + "FA9_톨허스트", "톨허스트", "LG 선발 · 1차전", [vduo([dict(v="3개", k="피안타", at=1), dict(v="2개", k="그중 홈런", at=3, c="bad")])],
            stats=[st("투구", "5이닝", 0)])
SC[20] = dm(0, "5회말 · KIA 공격", "KIA", [1, 2], 0, [dict(at=1, bases=["김태군", "김규성", None], outs=1, label="볼넷 · 희생번트 · 몸에 맞는 공"),
                                                    dict(at=2, who="하주석", out=["김태군"], bases=N3, outs=3, label="하주석 투수 앞 병살타")])
SC[21] = S(0, "scoreboard", title="5회까지", rows=[{"team": "LG", "runs": [0, 1, 0, 0, 0], "r": 1}, {"team": "KIA", "runs": [0, 1, 0, 1, 0], "r": 2}],
           hi=[6], label="승부처는 6회", labelAt=1)
SC[22] = dm(0, "6회초 · LG 공격", "LG", [1, 2], 0, [dict(at=1, who="박해민", bases=[None, "박해민", None], outs=0, label="박해민 2루타 · 무사 2루")], chain="d6")
SC[23] = dm(0, "6회초 · LG 공격", "LG", [1, 2], 0, [dict(at=-1, bases=[None, "박해민", None], outs=0, label="무사 2루"),
                                                  dict(at=0, who="오스틴", bases=[None, "박해민", None], outs=0, label="타석에 오스틴"),
                                                  dict(at=2, who="오스틴", bases=["오스틴", "박해민", None], outs=0, label="고의4구 · 무사 1·2루")], chain="d6", cont=True)
SC[24] = dm(0, "6회초 · LG 공격", "LG", [1, 2], 0, [dict(at=-1, bases=["오스틴", "박해민", None], outs=0, label="무사 1·2루"),
                                                  dict(at=1.5, bases=["오스틴", "박해민", None], outs=0, label="다음 타자 문정빈 · 문보경")], chain="d6", cont=True)
SC[25] = S(0, "pgroup", title="정규시즌 네일 상대 기록", items=[dict(img=C + "P15_문정빈", name="문정빈", team="LG", k="네일 상대", v="8타수 5안타", at=0, vAt=1),
                                                         dict(img=C + "문보경_LG홈런카드", name="문보경", team="LG", k="네일 상대", v="3타수 3안타", at=0.5, vAt=2)],
           text="가장 조심할 두 타자", textAt=3)
SC[26] = dm(0, "6회초 · LG 공격", "LG", [1, 2], 0, [dict(at=-1, bases=["오스틴", "박해민", None], outs=0, label="무사 1·2루"),
                                                  dict(at=1, who="문정빈", bases=["오스틴", "박해민", None], outs=1, label="문정빈 삼진"),
                                                  dict(at=2, who="문보경", out=["오스틴"], bases=N3, outs=3, label="문보경 병살타")])
SC[27] = pv(0, C + "P17_네일_포효", "네일", "KIA 선발 · 6회초", [vstamp("무사 1·2루 무실점", 1, "gold", size=54)], chain="n27")
SC[28] = pv(0, C + "P17_네일_포효", "네일", "KIA 선발 · 6회초", [vstamp("무사 1·2루 무실점", 1, "gold", size=54)], chain="n27", cont=True,
            stats=[st("문정빈", "삼진", 1), st("문보경", "병살타", 1.3, hi=True)])
SC[29] = sp(0, C + "F16_이범호", "이범호", "KIA 감독 · 경기 뒤", [], chain="s29")
SC[30] = sp(0, C + "F16_이범호", "이범호", "KIA 감독 · 경기 뒤", [bb("", "“공 하나라도\n아끼고 싶었던 것 같다”", 0), bb("", "“차라리 볼넷 주고\n다음 타자를 신중하게”", 1.5)], chain="s29", cont=True)
SC[31] = dm(0, "6회말 · KIA 공격", "KIA", [1, 2], 0, [], lead="6회말 · 무사", chain="d6b")
SC[32] = dm(0, "6회말 · KIA 공격", "KIA", [1, 2], 0, [dict(at=1, who="박재현", bases=["박재현", None, None], outs=0, label="좌익수 송찬의 실책"),
                                                    dict(at=3, who="김선빈", bases=["김선빈", None, "박재현"], outs=0, label="3루수 문보경 실책")], chain="d6b", cont=True)
SC[33] = dm(0, "6회말 · KIA 공격", "KIA", [1, 2], 0, [dict(at=-1, bases=["김선빈", None, "박재현"], outs=0, label="3루수 문보경 실책"),
                                                    dict(at=1, bases=["김선빈", None, "박재현"], outs=0, label="실책 두 개 · 무사 1·3루"),
                                                    dict(at=2.5, bases=["김선빈", None, "박재현"], outs=0, label="LG 투수 교체 · 우강훈")], chain="d6b", cont=True)
SC[34] = dm(0, "6회말 · KIA 공격", "KIA", [1, 2], 0, [dict(at=-1, bases=["김선빈", None, "박재현"], outs=0, label="무사 1·3루"),
                                                    dict(at=1, who="김도영", bases=["김선빈", None, None], scored=["박재현"], runs=1, outs=1, label="김도영 희생플라이 · 1점")], chain="d6b", cont=True)
SC[35] = pv(0, C + "송찬의_LG홈런카드", "송찬의", "LG 좌익수", [vsteps([stp("2회초", "솔로 홈런", 0, c="good"), stp("6회말", "포구 실책", 1, c="bad")])])
SC[36] = S(0, "cells", title="1차전 홈런 네 개", cols=4, cw=330, ch=130,
           items=[dict(t="송찬의 · 2회", hi=True, c=LGB, at=0.2, fs=38), dict(t="카스트로 · 2회", hi=True, c=KIAC, at=1, fs=38),
                  dict(t="김도영 · 4회", hi=True, c=KIAC, at=2, fs=38), dict(t="김도영 · 8회", hi=True, c=KIAC, at=2.3, fs=38)],
           text="네 개 모두 125미터", textAt=4)
SC[37] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 경기 뒤", [], chain="s37")
SC[38] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 경기 뒤", [bb("", "“6회 실책이 연달아 나오면서\n추가점을 내주면서\n경기 흐름을 넘겨줬다”", 0)], chain="s37", cont=True)
SC[39] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 경기 뒤", [bb("", "“6회 실책이 연달아 나오면서\n추가점을 내주면서\n경기 흐름을 넘겨줬다”", 0),
                                                                    bb("", "실책은 나올 수 있지만\n연속으로 나온 게 점수로 이어졌다", 1, src=True)], chain="s37", cont=True)
SC[40] = dm(0, "8회초 · LG 공격", "LG", [1, 3], 2, [dict(at=1, bases=["오스틴", "박해민", None], outs=2, label="박해민 · 오스틴 안타 · 2사 1·2루")])
SC[41] = S(0, "relay", title="8회초 · KIA 불펜 이어 던지기", team="KIA", inn=[8, 9], colors=[KIAC, NAVY, GOLD],
           pitchers=[dict(name="성영탁", outs=2, at=1), dict(name="전상현", outs=4, at=1.4)],
           note=dict(inn=0, label="사이에 곽도규 · 한 타자", at=1.2), text="문정빈 중견수 뜬공 · 또 0점", textAt=3, size=56)
SC[42] = dm(0, "8회말 · KIA 공격", "KIA", [1, 3], 2, [dict(at=1, who="김선빈", bases=["김선빈", None, None], outs=2, label="김선빈 안타 · 2사 1루"),
                                                    dict(at=2, who="김도영", bases=["김선빈", None, None], outs=2, label="타석에 김도영")], chain="d8b")
SC[43] = dm(0, "8회말 · KIA 공격", "KIA", [1, 3], 2, [dict(at=-1, who="김도영", bases=["김선빈", None, None], outs=2, label="타석에 김도영"),
                                                    dict(at=0.6, who="김도영", hr=True, runs=2, bases=N3, outs=2, label="김도영 2점 홈런")], chain="d8b", cont=True)
SC[44] = pv(0, C + "P17_김도영_질주", "김도영", "KIA 3루수 · 1차전", [], chain="k44",
            stats=[st("타격", "3타수 2안타", 0), st("홈런", "2개", 1, hi=True), st("희생플라이", "1개", 2), st("타점", "4개", 3, hi=True)])
SC[45] = pv(0, C + "P17_김도영_질주", "김도영", "KIA 3루수 · LG 상대", [vsteps([stp("10월 5일", "9회 역전 3점 홈런", 2, c="gold"), stp("10월 12일", "8회 결승 2점 홈런", 3, c="gold"),
                                                                    stp("10월 17일", "1차전 홈런 두 개", 4, c="gold")])], chain="k44", cont=True)
SC[46] = pv(0, C + "P17_김도영_질주", "김도영", "KIA 3루수 · 1차전", [vstamp("준플레이오프 한 경기 최다 홈런 타이", 2.5, "gold", size=44)], chain="k44", cont=True,
            stats=[st("포스트시즌 한 경기 홈런 두 개", "데뷔 처음", 0.5, hi=True)])
SC[47] = S(0, "scoreboard", title="10월 17일 광주 · 준플레이오프 1차전", rows=[{"team": "LG", "runs": [0, 1, 0, 0, 0, 0, 0, 0, 0], "r": 1},
                                                                  {"team": "KIA", "runs": [0, 1, 0, 1, 0, 1, 0, 2, "X"], "r": 5, "hi": True}],
           hi=[4, 6, 8], label="KIA 5대1 승리", labelAt=1)
SC[48] = S(0, "cells", title="1차전 6점은 어떻게 났나", cols=3, cw=420, ch=120,
           items=[dict(t=t_, hi=h_, c=c_, at=0.2 + j * 0.12, fs=38) for j, (t_, h_, c_) in enumerate([("2회 · 송찬의 홈런", True, LGB), ("2회 · 카스트로 홈런", True, KIAC), ("4회 · 김도영 홈런", True, KIAC),
                                                                                         ("6회 · 희생플라이", False, None), ("8회 · 김도영 홈런", True, KIAC), ("8회 · 김도영 홈런", True, KIAC)])],
           text="6점 중 5점이 홈런", textAt=2)
SC[49] = pv(0, C + "P15_전상현", "전상현", "KIA 마무리", [vstamp("세이브", 3, "gold")], chain="j49",
            stats=[st("10월 정규시즌", "피안타 0", 0), st("1차전", "2피안타 0실점", 2, hi=True)])
SC[50] = pv(0, C + "P15_전상현", "전상현", "KIA 마무리", [vstamp("2차전 등판은 점검", 2, "bad", size=52)], chain="j49", cont=True,
            stats=[st("1차전 투구 수", "26개", 0, hi=True)])
SC[51] = pv(0, C + "P17_네일_글러브", "네일", "KIA 선발 · 1차전", [], stats=[st("이닝", "7이닝", 0), st("투구 수", "92개", 1), st("피안타 · 실점", "4개 · 1점", 2, hi=True), st("삼진", "6개", 3)])
SC[52] = S(0, "bars", title="네일의 1차전 주요 구종 · 92구 중", items=[dict(label="투심", value=32, unit="개", at=0, hi=True), dict(label="스위퍼", value=26, unit="개", at=0.4),
                                                                dict(label="커터", value=24, unit="개", at=1)], max=40)
SC[53] = S(0, "speedgun", title="네일 투심 구속 · 1차전", pitcher={"img": C + "P17_네일_역투", "name": "네일", "team": "KIA", "role": "KIA 선발"},
           items=[{"vs": "가장 빠른 공", "v": 150, "at": 0}, {"vs": "평균", "v": 148, "at": 1}], unit="킬로")
SC[54] = pv(0, C + "P17_네일_글러브", "네일", "KIA 선발", [vtrend([dict(x="정규시즌", v=4.58, vt="4.58", c="bad", at=0), dict(x="1차전", v=1.29, vt="1.29", c="good", at=2)], title="LG 상대 평균자책점")])
SC[55] = pv(0, C + "P17_네일_환호", "네일", "준플레이오프 1차전", [vstamp("데일리 MVP", 2, "gold")], stats=[st("1차전", "7이닝 1실점 · 승리", 0, hi=True)])
# 2장 승부를 가른 이유
SC[56] = S(0, "toc", on=1)
SC[57] = pv(0, C + "R13_김도영", "김도영", "이유 1", [vstamp("김도영 앞에 주자", 1, "gold", size=56)], chain="k57")
SC[58] = pv(0, C + "R13_김도영", "김도영", "이유 1", [vstamp("김도영 앞에 주자", 1, "gold", size=56),
                                                  vtrend([dict(x="정규시즌", v=308, vt="3할 8리", at=-1), dict(x="LG전", v=208, vt="2할 8리", c="bad", at=0.5)], title="타율")], chain="k57", cont=True)
SC[59] = S(0, "pgroup", title="KIA 1·2번 타자 · 1차전", items=[dict(img=C + "P15_박재현", name="박재현", team="KIA", k="1번 타자", v="4타수 0안타", at=0, vAt=1),
                                                          dict(img=C + "P17_김선빈", name="김선빈", team="KIA", k="2번 타자", v="4타수 1안타", at=0.3, vAt=1)],
           text="둘이 8타수 1안타", textAt=2)
_ST60 = vsteps([stp("6회말", "실책 두 개 · 무사 1·3루", 0, c="bad"), stp("8회말", "투 아웃 뒤 안타 · 2사 1루", 1)])
SC[60] = pv(0, C + "P17_김도영_하이파이브", "김도영", "김도영 앞에 주자", [_ST60], chain="k60")
SC[61] = pv(0, C + "P17_김도영_하이파이브", "김도영", "김도영 앞에 주자", [_ST60, vduo([dict(v="1점", k="6회 희생플라이", at=2, c="good"), dict(v="2점", k="8회 홈런", at=2.3, c="good")])], chain="k60", cont=True)
SC[62] = pv(0, C + "P17_김도영_하이파이브", "김도영", "김도영 앞에 주자", [_ST60, vduo([dict(v="1점", k="6회 희생플라이", at=2, c="good"), dict(v="2점", k="8회 홈런", at=2.3, c="good")]),
                                                                  vstamp("LG 3점 허용", 2, "bad", size=50)], chain="k60", cont=True)
SC[63] = sp(0, C + "FA9_이범호", "이범호", "KIA 감독 · 경기 뒤", [bb("", "“박재현이 어떻게 하느냐에 따라\n김도영 앞에 기회가 만들어진다”", 1)])
SC[64] = sp(0, C + "P17_염경엽_덕아웃", "염경엽", "LG 감독 · 경기 뒤", [bb("", "“김도영이 실투들을\n놓치지 않았다”", 2), bb("", "“인정할 건\n인정해야 한다”", 3)])
_P65 = [("오스틴_MVP_포효", "오스틴", "3타수 1안타"), ("P17_문정빈_타격", "문정빈", "4타수 0안타"), ("P17_문보경_10호", "문보경", "4타수 0안타")]   # 1차 검수: pgroup 3명이 화면 양끝에 붙음 → people 카드 / 2차 검수: full=True 면 카드가 너무 작음 → 기본 폭 400 + 사진 높이 420
SC[65] = S(0, "people", ph=420, title="이유 2 · LG 중심 타선", items=[dict(img=C + i, name=n, note=" ", at=0.6 + j * 0.3) for j, (i, n, v) in enumerate(_P65)], chain="pg65")
SC[66] = S(0, "people", ph=420, title="이유 2 · LG 중심 타선", items=[dict(img=C + i, name=n, note=v, noteAt=0.2 + j * 0.25, bad=True) for j, (i, n, v) in enumerate(_P65)], chain="pg65", cont=True, text="셋이 11타수 1안타", textAt=2)
SC[67] = S(0, "cells", title="LG · 주자 두 명이 나간 기회", cols=3, cw=420, ch=140,
           items=[dict(t="3회 · 2사 1·2루", at=0, fs=40), dict(t="6회 · 무사 1·2루", at=0.3, fs=40), dict(t="8회 · 2사 1·2루", at=0.6, fs=40)],
           text="세 번 모두 0점", textAt=3)
SC[68] = S(0, "scoreboard", title="6회가 갈랐다", rows=[{"team": "LG", "runs": [0, 1, 0, 0, 0, 0], "r": 1}, {"team": "KIA", "runs": [0, 1, 0, 1, 0, 1], "r": 3}],
           hi=[6], label="6회초 무사 1·2루 0점 → 6회말 KIA 1점", labelAt=1.5, text="위기 뒤에 기회", textAt=3)
SC[69] = S(0, "faceoff", title="기회에서의 차이", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=260,
           rows=[dict(k="결정적 기회", l="세 번 · 0점", r="김도영 두 번 · 3점", w="r", at=1.5), dict(k="최종 점수", l="1점", r="5점", w="r", at=3.5)])
SC[70] = sp(0, "KBO프로필/염경엽_감독", "염경엽", "LG 감독 · 경기 뒤", [bb("", "“중심 타순에 기회가 걸렸는데\n잘 살리지 못했다”", 1), bb("", "“결국 점수를 내야 이긴다”", 3)])
_MD = [dict(k="선발이\n던진 이닝", l="톨허스트 5이닝", r="네일 7이닝", lv=5, rv=7), dict(k="불펜 투수", l="5명", r="3명", lv=5, rv=3, low=True)]
SC[71] = S(0, "faceoff", title="이유 3 · 마운드의 깊이", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=260,
           rows=[dict(r, at=0.3) for r in _MD], chain="md")   # 10/18 사용자: 처음부터 완성된 배치로 + 두 줄을 한 번에(하나씩 X)
SC[72] = S(0, "faceoff", title="이유 3 · 마운드의 깊이", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=260,
           rows=[dict(_MD[0], at=0), dict(_MD[1], at=0)], chain="md", cont=True)
SC[73] = S(0, "relay", title="1차전 · LG 불펜 이어 던지기", team="LG", inn=[6, 7, 8], colors=[LGB, NAVY, GOLD, GREEN, "#8B5CF6"],
           pitchers=[dict(name="우강훈", outs=1, at=0.6), dict(name="케네디", outs=3, at=1), dict(name="이우찬", outs=2, at=1.3), dict(name="장현식", outs=2, at=1.6), dict(name="김윤식", outs=1, at=1.9)],
           brace=dict(label="불펜 다섯 명이 3이닝", at=2))
SC[74] = S(0, "pstat", team="LG", name="우강훈", sub="LG 투수 · 6회말", stats=[st("상대", "김도영 한 타자", 1, hi=True)], viz=[vstamp("원 포인트 기용", 2, "gold"), vstamp("앞으로도 이렇게", 3.5, "bad", size=50)], noCenter=True)
SC[75] = S(0, "faceoff", title="2차전을 앞두고", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=260,
           rows=[dict(_MD[1], at=0), dict(k="2차전\n불펜 부담", l="크다", r="작다", w="r", at=0.3)])   # 10/17 사용자: 두 줄을 한 번에(볼 시간)
SC[76] = pv(0, C + "T12_임찬규", "임찬규", "LG 2차전 선발", [vstamp("길게 던져야 한다", 2, "gold")], stats=[st("1차전 LG 불펜", "5명 등판", 0.5, hi=True)])
# 3장 2차전 예측
SC[77] = S(0, "toc", on=2)
SC[78] = S(0, "duel", title="2차전 · 광주", left={"img": C + "P17_올러_포효0929", "name": "올러", "team": "KIA", "role": "KIA 선발", "at": 0},
           right={"img": C + "P17_임찬규_1012", "name": "임찬규", "team": "LG", "role": "LG 선발", "at": 0.5}, vsAt=0.3)   # 1차 검수: 앞 두 호흡 빈 화면
_OL = vtrend([dict(x="LG 상대", v=2.40, vt="2.40", c="good", at=1), dict(x="광주", v=2.28, vt="2.28", c="good", at=2)], title="평균자책점 · 정규시즌")
SC[79] = pv(0, C + "FA9_올러_경기", "올러", "KIA 2차전 선발", [_OL], chain="o79")
SC[80] = pv(0, C + "FA9_올러_경기", "올러", "KIA 2차전 선발", [_OL, vstamp("한국 첫 가을야구 등판", 1.5, "bad", size=50)], chain="o79", cont=True)
SC[81] = S(0, "pgroup", title="올러 상대 정규시즌 기록", items=[dict(img=C + "F16_홍창기_A", name="홍창기", team="LG", k="올러 상대", v="10타수 1안타", at=0, vAt=1),
                                                         dict(img=C + "오스틴_MVP_하트", name="오스틴", team="LG", k="올러 상대", v="12타수 2안타", at=0.3, vAt=2)])
SC[82] = pv(0, C + "R13_임찬규_투구", "임찬규", "LG 2차전 선발", [vtrend([dict(x="KIA 상대", v=6.23, vt="6.23", c="bad", at=4)], title="평균자책점 · 정규시즌")], chain="i82",
            stats=[st("2026 정규시즌", "15승", 0, hi=True), st("다승", "공동 1위", 1.5)])
SC[83] = pv(0, C + "R13_임찬규_투구", "임찬규", "LG 2차전 선발", [vtrend([dict(x="KIA 상대", v=6.23, vt="6.23", c="bad", at=4)], title="평균자책점 · 정규시즌")], chain="i82", cont=True,
            stats=[st("2026 정규시즌", "15승", 0, hi=True), st("다승", "공동 1위", 1.5), st("2024 준플레이오프 2차전", "데일리 MVP", 2, hi=True)])
SC[84] = sp(0, C + "FA9_염경엽", "염경엽", "LG 감독 · 1차전 뒤", [bb("", "2차전 선발 라인업 변화\n“있을 것 같다”", 3, src=True)])
SC[85] = pv(0, C + "F16_홍창기_B", "홍창기", "LG 1번 타자 · 1차전", [], stats=[st("1차전", "3타수 1안타", 1), st("8회", "대타로 교체", 2, hi=True)])
_PG86 = [dict(img="KBO프로필/문정빈_2026LG", name="문정빈", team="LG", k="KIA전 타율 · 정규시즌", v="3할 1푼 3리"), dict(img="KBO프로필/문보경_2026LG", name="문보경", team="LG", k="KIA전 타율 · 정규시즌", v="3할 1푼 3리")]
SC[86] = S(0, "pgroup", title="LG 반격의 열쇠", items=[dict(x, at=1 + j * 0.3, vAt=99) for j, x in enumerate(_PG86)], chain="pg86")
SC[87] = S(0, "pgroup", title="LG 반격의 열쇠", items=[dict(x, at=-1, vAt=1.5) for x in _PG86], chain="pg86", cont=True, text="1차전엔 둘이 8타수 0안타", textAt=4)
_GS = [("3/31", "K"), ("4/1", "L"), ("4/2", "L"), ("5/19", "K"), ("5/21", "L"), ("5/29", "L"), ("5/30", "L"), ("5/31", "L"), ("6/16", "L"),
       ("6/17", "K"), ("6/18", "K"), ("9/26", "K"), ("10/3", "K"), ("10/4", "K"), ("10/5", "K"), ("10/12", "K"), ("10/17", "K")]
SC[88] = S(0, "gamestrip", tc=TCKL, title="2026 KIA vs LG · 정규시즌 16경기 + 준플레이오프 1차전", teams={"K": "KIA", "L": "LG"}, games=[list(x) for x in _GS], rows=[[0, 8], [9, 16]],
           at=0.2, step=0.04, dimTo=9, groups=[{"from": 9, "to": 16, "label": "6월 17일부터 · KIA 8연승", "team": "KIA", "at": 3}])
SC[89] = sp(0, C + "T12_이범호", "이범호", "KIA 감독 · 경기 뒤", [bb("", "박재현이 1차전 부침을 2차전에서 회복하면\n자기 페이스를 찾을 것", 2, src=True)])
def g5(**k): return dict(**k)
SC[90] = S(0, "series5", tc=TCKL, title="준플레이오프 일정 · 5전 3선승제", games=[g5(n="1차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="2차전", venue="광주", home="KIA", at=0, glow="LG", glowAt=2.5),
                                                                    g5(n="3차전", venue="잠실", home="LG", at=0, glow="LG", glowAt=1), g5(n="4차전", venue="잠실", home="LG", at=0, glow="LG", glowAt=1),
                                                                    g5(n="5차전", venue="광주", home="KIA", at=0)])
SC[91] = S(0, "cells", title="역대 5전 3선승제 · 1차전 이긴 팀", cols=13, cw=96, ch=72,
           items=[dict(t="", hi=(k < 39), c=GOLD, at=0.3 + k * 0.03) for k in range(52)], text="52번 중 39번 통과 · 75%", textAt=3)
SC[92] = S(0, "matchup", left="KIA", right="LG", score="2차전", tag="야구자판기 예상", text="2차전도 KIA", size=96)
SC[93] = S(0, "faceoff", title="2차전 · KIA 쪽인 이유", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=260,
           rows=[dict(k="상대 팀\n평균자책점", l="임찬규 6.23", r="올러 2.40", w="r", at=0.5), dict(k="1차전 불펜", l="5명 등판", r="3명 등판", w="r", at=3)])
SER = [g5(n="1차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="2차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="3차전", venue="잠실", home="LG", win="?", at=0, glow="LG", glowAt=0),
       g5(n="4차전", venue="잠실", home="LG", win="?", at=0, glow="LG", glowAt=0), g5(n="5차전", venue="광주", home="KIA", off=True, at=0)]
SC[94] = S(0, "series5", tc=TCKL, title="준플레이오프 · 야구자판기 예상 KIA 3승 1패", games=SER, brace=dict(**{"from": 2, "to": 3}, label="두 경기 중 한 경기는 LG", team="LG", at=1.5), chain="ser")
SER2 = [dict(g) for g in SER]; SER2[1] = g5(n="2차전", venue="광주", home="KIA", win="?", at=1, glow="LG", glowAt=1)
SC[95] = S(0, "series5", tc=TCKL, title="변수 · LG 중심 타선이 터지면", games=SER2, pills=[dict(label="LG 중심 타선이 터지면", at=0.5, c=LGB), dict(label="시리즈는 다시 알 수 없다", at=3, c="#12161F")], chain="ser", cont=True)
SC[96] = S(0, "question", text="2차전\nLG가 반격할까요?\nKIA가 2연승할까요?", logos=["LG", "KIA"], size=92)

N = len(TEXT)
assert sorted(SC) == list(range(N)), (N, sorted(set(range(N)) - set(SC)))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "경기 흐름", "title": "경기 흐름", "from": 4, "to": 55},
      {"key": "승부를 가른 이유", "title": "승부를 가른 이유", "from": 56, "to": 76},
      {"key": "2차전 예측", "title": "2차전 예측", "from": 77, "to": 96}]

TAGS = ["2026 준PO", "준플레이오프", "준PO 1차전", "준플레이오프 1차전", "KIA LG 준플레이오프", "준플레이오프 2차전", "준PO 2차전 예측", "KIA 타이거즈", "LG 트윈스",
        "가을야구", "김도영", "김도영 홈런", "네일", "톨허스트", "올러", "임찬규", "송찬의", "카스트로", "염경엽", "이범호", "프로야구", "KBO", "2026 프로야구", "야구자판기"]
DESC = ("2026 프로야구 준플레이오프 1차전, KIA 타이거즈가 LG 트윈스를 5대1로 이겼어요. 김도영의 홈런 두 방과 네일의 7이닝 1실점 호투를 장면별로 돌아보고, 왜 이런 결과가 나왔는지 세 가지로 분석한 뒤 2차전을 예측했어요.\n\n"
        "김도영은 4회 역전 솔로 홈런, 6회 희생플라이, 8회 쐐기 2점 홈런으로 3타수 2안타 4타점을 기록했어요. 포스트시즌 한 경기 홈런 두 개는 프로 데뷔 후 처음이에요. "
        "데일리 MVP는 7이닝 92구 4피안타 6탈삼진 1실점의 네일이 받았어요. 6회초 무사 1·2루에서 문정빈을 삼진, 문보경을 병살타로 잡아낸 장면이 승부처였어요.\n\n"
        "LG는 6회말 실책 두 개로 추가점을 내줬고, 오스틴·문정빈·문보경 중심 타선이 11타수 1안타에 그쳤어요. 주자 두 명이 나간 기회 세 번(3회·6회·8회)이 모두 0점이었어요.\n\n"
        "2차전은 같은 광주에서 KIA 올러와 LG 임찬규의 선발 맞대결이에요. 야구자판기의 예상은 2차전도 KIA, 시리즈는 KIA 3승 1패예요. 다만 LG 중심 타선이 깨어나면 시리즈는 다시 알 수 없어요.\n\n"
        "야구자판기는 매일 오늘의 야구 이슈를 정리해 드려요.\n\n"
        "2차전, LG가 반격할까요? KIA가 2연승할까요? 댓글로 알려 주세요.\n\n"
        "기록: KBO 게임센터 준플레이오프 1차전 박스스코어, KBO 기록실(2026 정규시즌 투수 vs 타자·팀간 승패). 발언: 경기 뒤 양 팀 감독 인터뷰(스포티비뉴스). 비거리·구종: MK스포츠, 스포츠조선. 역대 기록: 동아일보\n"
        "사진: KIA 타이거즈 제공, LG 트윈스 제공, 각 구단 공식 프로필")
SOURCE = "사실 출처 = KBO 게임센터 박스스코어(10/17 직접 조회) + 기사 원문 + 롱폼⑮ 근거 — 프로젝트 claude/1017-롱폼17-준PO1차전-근거모음.md."

EP = {"date": "2026-10-17", "gameDate": "2026-10-17", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1017-long17-v6", "topic": "준PO1차전리뷰", "endcardSec": 10, "totalSec": 481.0,   # 10/17 검수판 본편+엔딩10초 = 7:57 → 8분 살짝 모자라서 엔딩을 늘려 8:01(사용자 규칙)
     
      "gapScale": 1.05, "pauseMax": 0.4, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "야구롱폼/영상/2026-10-17/롱폼_준PO1차전_썸네일.jpg", "source": SOURCE,
      "youtube": {"title": "2026 준PO 1차전 리뷰 | 김도영 홈런 두 방, KIA가 LG 잡은 이유와 2차전 예측 #준플레이오프 #김도영 #KIA",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#준플레이오프", "#가을야구", "#KIA타이거즈", "#LG트윈스", "#김도영", "#네일", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {1, 16, 17, 27, 43, 47, 55, 61, 91, 92, 96}
    HOLD = {0: 0.3, 3: 0.5, 11: 0.4, 16: 0.5, 17: 0.5, 27: 0.6, 43: 0.6, 47: 0.6, 55: 0.6, 76: 0.6, 92: 0.5}
    # 10/17 사용자 "나레이션 끝나면 너무 금방 넘어가": 마지막 호흡에 마지막 정보가 뜨는 줄은 0.6초 더 보여 준다
    for i in (18, 19, 36, 51, 64, 66, 67, 68, 70, 73, 75, 80, 85, 87, 88, 95): HOLD.setdefault(i, 0.6)
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    EP['lines'][0]['pauseMax'] = 0.12   # 10/18 사용자 "처음 'KIA가~5대1로 꺾었어요' 텀이 너무 길어": 훅 줄 안 쉼을 0.12초까지
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-17_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
