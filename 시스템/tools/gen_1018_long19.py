# -*- coding: utf-8 -*-
"""10/18 롱폼⑲ 「준플레이오프 2차전 리뷰 · 승부를 가른 이유 · 3차전 예측」 (음성 API · 줄별 배속).
대사 = tools/text_1018_long19.py. 근거 = KBO 게임센터 박스스코어(20261018LGHT0) 10/18 직접 조회 + KBO 기록실(시라카와·카라스코 팀별·구장별)
+ 기사 본문 — 프로젝트 claude/1018-롱폼19-준PO2차전-근거모음.md.
같은 날짜 두 번째 롱폼이라 파일 이름 = episodes/2026-10-18_롱폼2.json (롱폼검수·롱폼만들기는 정렬상 이 파일을 고른다 — '롱폼.' < '롱폼2').
사진 = 오늘 경기 사진(카드/P18_* · 경기/*_1018) + 기존 카드."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1018_long19.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES, sino = _g['L'], _g['narr_of'], _g['_t'].LINES, _g['sino']
TEXT = [x[0] for x in LINES]

BAT = {'1번 홍창기': '일 번 홍창기', '1번에': '일 번에', '2번 송찬의': '이 번 송찬의', '4번 문정빈': '사 번 문정빈', '6번 이재원': '육 번 이재원', '2번으로': '이 번으로'}
def pre(t):
    t = t.replace('1만 8,900석', '만 팔천구백 석')
    for a, b in (('6대3', '육 대 삼'), ('5대0', '오 대 영'), ('5대1', '오 대 일'), ('5대2', '오 대 이'), ('6대2', '육 대 이'), ('1대0', '일 대 영')): t = t.replace(a, b)
    for a, b in BAT.items(): t = t.replace(a, b)
    t = t.replace('6시 반', '여섯 시 반').replace('5전 3선승제', '오 전 삼 선승제').replace('MVP', '엠브이피').replace('77.8%', '칠십칠쩜팔 퍼센트')
    t = t.replace('9와 3분의 1이닝', '구와 삼분의 일 이닝').replace('4와 3분의 1이닝', '사와 삼분의 일 이닝')
    t = t.replace('10과 3분의 2이닝', '십과 삼분의 이 이닝').replace('1과 3분의 1이닝', '일과 삼분의 일 이닝')
    t = t.replace('7과 3분의 2이닝', '칠과 삼분의 이 이닝').replace('3.5개꼴', '삼쩜오 개꼴').replace('4번부터 6번', '사 번부터 육 번')
    t = t.replace('MLB파크', '엠엘비파크').replace('6월 17일', '유월 십칠 일').replace('10월 20일', '시월 이십 일')
    return t
def narr_of(t):
    t = re.sub(r'(일|이|삼) 루', r'\1루', narr_of15(pre(t)))
    t = t.replace('팔 월', '팔월')
    t = re.sub(r'(일|이|삼|사|오|육|칠|팔|구|십) (연승|연패)', r'\1\2', t)   # 10/18 검수: 구 연승 → 구연승
    t = re.sub(r'(일|이|삼|사|오|칠|팔) (차전|연승|연패)', r'\1\2', t)
    return re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|타수|안타|이닝|타점)(?![가-힣]*차전)', r'\1\2', t)   # 10/18 '이 회'·'이 승'이 지시어로 들림
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
def dm(i, title, bat, score, outs, steps, **k):
    return S(i, "diamond", title=title, bat=bat, batIdx=(0 if bat == "LG" else 1), score=score, outs=outs, steps=steps, away="LG", home="KIA", **k)
N3 = [None, None, None]
def g5(**k): return dict(**k)

SC = {}
# ── 훅 ──
SC[0] = S(0, "matchup", left="KIA", right="LG", score="6 : 3", tag="준플레이오프 2차전 · 광주")
SC[1] = S(0, "scoreboard", title="준플레이오프 2차전 · 1회", rows=[{"team": "LG", "runs": [0], "r": ""}, {"team": "KIA", "runs": [5], "r": "", "hi": True}],
          hi=[1], label="1회말 · 안타 6개로 5점", labelAt=1.2)
SER0 = [g5(n="1차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="2차전", venue="광주", home="KIA", win="KIA", at=0.4),
        g5(n="3차전", venue="잠실", home="LG", at=0), g5(n="4차전", venue="잠실", home="LG", at=0), g5(n="5차전", venue="광주", home="KIA", at=0)]
SC[2] = S(0, "series5", tc=TCKL, title="준플레이오프 · 5전 3선승제", games=SER0, pills=[dict(label="플레이오프까지 1승", at=1.2, c=KIAC)])
SC[3] = S(0, "toc", on=-1, itemFrom=99)
# ── 1장 경기 흐름 (10/18 19:18 사용자 "주요장면만" → 18장면) ──
SC[4] = S(0, "duel", title="준플레이오프 2차전 선발", left={"img": C + "P18_올러_투구", "name": "올러", "team": "KIA", "role": "KIA 선발", "at": 0},
          right={"img": C + "R13_임찬규_투구", "name": "임찬규", "team": "LG", "role": "LG 선발", "at": 0.6}, vsAt=0.3)
_P7 = [("F16_홍창기_C", "홍창기", "1번 타자\n선발 제외"), ("F16_박해민", "박해민", "새 1번 타자"), ("P18_이재원", "이재원", "우익수\n포스트시즌 첫 선발")]
SC[5] = S(0, "people", ph=420, title="LG 2차전 라인업 변화", items=[dict(img=C + i, name=n, note=v, at=0.1 + j * 0.9, noteAt=0.1 + j * 0.9, bad=(j == 0)) for j, (i, n, v) in enumerate(_P7)])
SC[6] = photo(G + "임찬규_강판_1018")
SC[7] = dm(0, "1회말 · KIA 공격", "KIA", [0, 0], 1, [dict(at=0.2, who="박재현", bases=["박재현", None, None], outs=1, label="박재현 좌전 안타"),
                                                 dict(at=1.0, bases=[None, "박재현", None], outs=1, label="박재현 2루 도루"),
                                                 dict(at=2.0, who="김도영", bases=["김도영", "박재현", None], outs=1, label="김도영 볼넷 · 원 아웃 1·2루")], chain="d1")
SC[8] = dm(0, "1회말 · KIA 공격", "KIA", [0, 0], 1, [dict(at=-1, bases=["김도영", "박재현", None], outs=1, label="원 아웃 1·2루"),
                                                 dict(at=0.6, who="카스트로", bases=["카스트로", None, "김도영"], scored=["박재현"], runs=1, outs=1, label="카스트로 적시타 · 결승타")], chain="d1", cont=True)
SC[9] = dm(0, "1회말 · KIA 공격", "KIA", [0, 1], 1, [dict(at=-1, bases=["카스트로", None, "김도영"], outs=1, label="원 아웃 1·3루"),
                                                 dict(at=0.2, who="나성범", bases=[None, "나성범", "카스트로"], scored=["김도영"], runs=1, outs=1, label="나성범 적시 2루타"),
                                                 dict(at=0.9, who="김선빈", bases=[None, "김선빈", None], scored=["카스트로", "나성범"], runs=2, outs=1, label="김선빈 2타점 2루타"),
                                                 dict(at=1.6, who="한준수", bases=[None, "한준수", None], scored=["김선빈"], runs=1, outs=1, label="한준수 적시 2루타 · 5대0")], chain="d1", cont=True)
SC[10] = pv(0, C + "R13_임찬규_투구", "임찬규", "LG 선발 · 1회말", [vstamp("1회도 못 채우고 강판", 2.0, "bad", size=52)],
            stats=[st("아웃", "1개", 0.2), st("실점", "5점", 1.0, hi=True)])
_REC = [("5점", "1회말 득점", 5), ("6개", "이닝 안타", 6), ("5명", "연속 안타", 5), ("7명", "연속 출루", 7)]
SC[11] = pv(0, C + "P18_박재현_득점", "KIA 1회말", "아래 4개 모두 가을야구 타이 기록", [vstamp("모두 타이 기록", 1.4, "gold", size=50)],
           stats=[st("득점", "5점", 0.2, hi=True), st("안타", "6개", 0.4), st("연속 안타", "5명", 0.6), st("연속 출루", "박재현부터 7명", 0.8)])
_RL = dict(title="LG 불펜 · 2회부터 6회까지", team="LG", inn=[2, 3, 4, 5, 6], cw=104, gap=26, colors=[LGB, NAVY, GOLD, GREEN])
SC[12] = S(0, "relay", **_RL, pitchers=[dict(name="케네디", outs=3, at=0.1), dict(name="이우찬", outs=5, at=0.4), dict(name="우강훈", outs=4, at=0.7), dict(name="손주영", outs=3, at=1.0)],
           brace=dict(label="KIA 0점", at=1.3))
SC[13] = dm(0, "3회초 · LG 공격", "LG", [0, 5], 1, [dict(at=0.5, who="박동원", bases=[None, "박동원", None], outs=1, label="박동원 2루타"),
                                                 dict(at=1.3, who="_구본혁", bases=["_구본혁", None, None], scored=["박동원"], runs=1, outs=1, label="적시타 · 5대1")], chain="d3")
SC[14] = dm(0, "3회초 · LG 공격", "LG", [1, 5], 1, [dict(at=-1, bases=["_구본혁", None, None], outs=1, label="적시타 · 5대1"),
                                                 dict(at=0, who="박해민", bases=["박해민", "_구본혁", None], outs=2, label="투 아웃 1·2루"),
                                                 dict(at=1.4, out=["박해민"], pick=["박해민"], bases=[None, "_구본혁", None], outs=3, label="한준수 견제 · 박해민 아웃")], chain="d3", cont=True)
SC[15] = pv(0, C + "F16_박해민", "박해민", "LG 1번 타자", [vsteps([stp("5회초", "투 아웃 1·2루", 0.2), stp("", "박해민 적시타 · 5대2", 1.0, c="good")])])
SC[16] = pv(0, C + "P18_올러_투구", "올러", "KIA 선발 · 6회", [vsteps([stp("오스틴", "헛스윙 삼진", 0.1, c="good"), stp("문정빈", "헛스윙 삼진", 0.9, c="good"), stp("이재원", "헛스윙 삼진", 1.2, c="good")])], stats=[st("2차전", "6이닝 2실점", 3)])   # 10/18 검수: 1장은 올러 카드(타자 사진은 2장에서)
SC[17] = dm(0, "7회말 · KIA 공격", "KIA", [2, 5], 1, [dict(at=-1, bases=["카스트로", None, "박재현"], outs=1, label="원 아웃 1·3루"),
                                                  dict(at=0.8, who="나성범", bases=["카스트로", None, None], scored=["박재현"], runs=1, outs=2, label="나성범 희생플라이 · 6대2")])
SC[18] = dm(0, "8회초 · LG 공격", "LG", [2, 6], 0, [dict(at=0.2, who="박해민", bases=[None, "박해민", None], outs=2, label="박해민 안타 뒤 투 아웃 2루"),
                                                 dict(at=1.0, who="문정빈", bases=["문정빈", None, None], scored=["박해민"], runs=1, outs=2, label="문정빈 적시타 · 6대3"),
                                                 dict(at=2.0, who="문보경", bases=["문보경", "문정빈", None], outs=2, label="문보경 안타 · 투 아웃 1·2루")], chain="d8", cont=True)
SC[19] = dm(0, "8회초 · LG 공격", "LG", [3, 6], 2, [dict(at=-1, bases=["문보경", "문정빈", None], outs=2, label="투수 전상현 · 타석에 이재원"),
                                                 dict(at=1.6, who="이재원", bases=N3, outs=3, label="이재원 3구 삼진")], chain="d8", cont=True)
SC[20] = S(0, "scoreboard", title="준플레이오프 2차전", rows=[{"team": "LG", "runs": [0, 0, 1, 0, 1, 0, 0, 1, 0], "r": 3},
                                                                  {"team": "KIA", "runs": [5, 0, 0, 0, 0, 0, 1, 0, "X"], "r": 6, "hi": True}],
           hi=[], label="KIA 6대3 승리", labelAt=1.0)
SC[21] = pv(0, C + "P15_전상현", "전상현", "KIA 마무리", [vstamp("2차전 데일리 MVP", 1.0, "gold", size=52)],
            stats=[st("1차전", "세이브", 0), st("2차전", "세이브", 0.3, hi=True)])
# ── 2장 승부를 가른 이유 ──
SC[51] = S(0, "toc", on=1)
SC[52] = pv(0, C + "P17_임찬규_1012", "임찬규", "이유 1", [vtrend([dict(x="KIA 상대", v=6.23, vt="6.23", c="bad", at=99)], title="평균자책점 · 정규시즌", titleAt=99, at=99, max=8)],
            stats=[st("KIA전", "두 경기 1패", 99)], chain="i52")
SC[53] = pv(0, C + "P17_임찬규_1012", "임찬규", "이유 1", [vtrend([dict(x="KIA 상대", v=6.23, vt="6.23", c="bad", at=1.4)], title="평균자책점 · 정규시즌", titleAt=1.2, max=8)],
            stats=[st("KIA전", "두 경기 1패", 0.3)], chain="i52", cont=True)
SC[54] = sp(0, C + "F16_이범호", "이범호", "KIA 감독 · 경기 뒤", [bb("", "“근래 임찬규 공을 많이 치기도 했고”", 0.4), bb("", "“공격적으로 타자들이 나간 게 도움이 됐다”", 3.2), bb("", "카운트 잡는 공을 안타로 만드는 싸움", 99, src=True)], chain="b54")
SC[54.5] = sp(0, C + "F16_이범호", "이범호", "KIA 감독 · 경기 뒤", [bb("", "“근래 임찬규 공을 많이 치기도 했고”", -1), bb("", "“공격적으로 타자들이 나간 게 도움이 됐다”", -1), bb("", "카운트 잡는 공을 안타로 만드는 싸움", 0.6, src=True)], chain="b54", cont=True)
SC[55] = pv(0, C + "P18_카스트로_환호", "카스트로", "KIA 1루수 · 1회말", [], stats=[st("결승타", "2구째 적시타", 0.2, hi=True), st("임찬규 1회", "타자 8명 · 공 28개", 2.4)], chain="c55")
SC[55.2] = pv(0, C + "P18_카스트로_환호", "카스트로", "KIA 1루수 · 1회말", [], stats=[st("결승타", "2구째 적시타", -1, hi=True), st("임찬규 1회", "타자 한 명에 공 3.5개", 0.2)], chain="c55", cont=True)
SC[55.4] = S(0, "people", ph=420, title="KIA 4~6번 · 타점 5개", items=[dict(img=C + i, name=n, note=v, at=0.2 + k * 0.5, noteAt=0.4 + k * 0.5) for k, (i, n, v) in enumerate([("P18_카스트로_엄지", "카스트로", "4번\n결승타 · 1타점"), ("P18_나성범_적시타", "나성범", "5번\n2타점"), ("P18_김선빈_2루타", "김선빈", "6번\n2타점")])])
SC[56] = S(0, "bars", title="KIA 안타 8개", items=[dict(label="1회", value=6, unit="개", at=0, hi=True), dict(label="2회부터", value=2, unit="개", at=0.6)], max=6)
SC[56.2] = sp(0, C + "F16_이범호", "이범호", "KIA 감독 · 경기 뒤", [bb("", "“올러가 부담을\n덜 느낄 수 있었다”", 3.2)])
SC[56.4] = pv(0, C + "P18_케네디_투구", "케네디", "LG 불펜 · 임찬규 다음 등판", [], stats=[st("임찬규 다음", "불펜 6명", 0.4), st("2차전 불펜", "7⅔이닝 1실점", 1.6, hi=True)])
SC[56.6] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 경기 뒤", [bb("", "“롱릴리프가 없어서\n1이닝씩 끊어서”", 0.6), bb("", "“추격하는 점수를\n만들지 못하면서”", 2.8)])
SC[57] = pv(0, C + "P15_올러_포효", "올러", "이유 2", [])
SC[57.1] = S(0, "speedgun", title="올러 · 2차전 가장 빠른 공", pitcher={"img": C + "P18_올러_환호", "name": "올러", "team": "KIA", "role": "KIA 선발"},
           items=[{"vs": "가장 빠른 공", "v": 154, "at": 0}], unit="킬로")
SC[57.2] = S(0, "bars", title="올러 2차전 주요 구종", items=[dict(label="빠른 공", value=38, unit="개", at=0, hi=True), dict(label="슬라이더", value=37, unit="개", at=0.6)], max=40)
SC[57.3] = pv(0, C + "FA9_올러_경기", "올러", "KIA 선발 · 2차전", [vsteps([stp("1회·2회", "세 타자로 끝", 0, c="good"), stp("4회", "세 타자로 끝", 0.6, c="good"), stp("5회까지", "공 72개", 1.6)])], chain="o57")
SC[57.4] = pv(0, C + "FA9_올러_경기", "올러", "KIA 선발 · 2차전", [vtrend([dict(x="LG 상대", v=2.40, vt="2.40", c="good", at=1.2)], title="평균자책점 · 정규시즌", max=8)],
              stats=[st("정규시즌 LG전", "5경기 2승 1패", 0.2), st("포스트시즌", "한국 첫 승", 2.4, hi=True)], chain="o57", cont=True)
SC[57.5] = sp(0, C + "F16_이범호", "이범호", "KIA 감독 · 경기 뒤", [bb("", "“공 개수가\n90개를 넘어서서”", 1.4)], chain="b57")
SC[57.6] = sp(0, C + "F16_이범호", "이범호", "KIA 감독 · 경기 뒤", [bb("", "“공 개수가\n90개를 넘어서서”", -1), bb("", "6이닝 뒤 3이닝은\n불펜으로", 0.6, src=True)], chain="b57", cont=True)
_P58 = [("P18_오스틴_타격", "오스틴", "3타수 무안타\n삼진 1개", "1·2차전\n7타수 1안타"), ("P17_문정빈_타격", "문정빈", "3타수 무안타\n삼진 3개", "1·2차전\n8타수 1안타"),
        ("P17_문보경_10호", "문보경", "2타수 무안타\n볼넷 1개", "1·2차전\n7타수 1안타")]
SC[58] = S(0, "people", ph=420, title="올러 상대 LG의 중심 타선", items=[dict(img=C + i, name=n, note=a, at=0.2 + j * 0.3, noteAt=0.4 + j * 0.3, bad=True) for j, (i, n, a, b) in enumerate(_P58)],
           text="8타수 무안타 · 삼진 4개", textAt=2.4, chain="pp58")
SC[59] = S(0, "people", ph=420, title="LG의 중심 타선 · 1·2차전 합계", items=[dict(img=C + i, name=n, note=b, noteAt=2 + j, bad=True) for j, (i, n, a, b) in enumerate(_P58)],
           text="1·2차전 합계 22타수 3안타", textAt=5, chain="pp58", cont=True)
SC[59.5] = S(0, "people", ph=420, title="LG 타선 · KIA 선발 상대", items=[dict(img=C + "P17_네일_역투C", name="네일", note="1차전 7이닝 1실점", at=0.3, noteAt=0.5, bad=False), dict(img=C + "P18_올러_환호", name="올러", note="2차전 6이닝 2실점", at=0.7, noteAt=0.9, bad=False)],
             text="13이닝 · 3점", textAt=1.8)
SC[60] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 경기 전", [bb("", "“결국 중심타선이다”", 0.6), bb("", "“보경이가\n자기 역할을 해줘야”", 2.2)])
_H3 = [dict(k="안타", l="9개", r="8개", lv=9, rv=8), dict(k="2루타", l="1개 · 박동원", r="4개", lv=1, rv=4)]
def h3(ats, **k): return S(0, "faceoff", title="이유 3 · 안타는 LG가 더 많았다", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=300,
                         rows=[dict(r, at=t) for r, t in zip(_H3, ats)], chain="h3", **k)
SC[61] = h3([1.0])   # 10/18 23:22 사용자: 줄이 동시에 툭 뜸 → 앞 장면엔 줄을 안 두고(자리만 템플릿이 잡음) 한 줄씩 등장
SC[61.5] = h3([0, 2.0], cont=True)
SC[61.6] = S(0, "people", ph=420, title="LG 주자가 사라진 장면", items=[dict(img=C + "P18_박해민_견제사", name="박해민", note="3회 · 견제사", at=0, noteAt=0.2, bad=True), dict(img=C + "F16_박동원_A", name="박동원", note="7회 · 병살타", at=0.9, noteAt=1.1, bad=True)])
SC[61.7] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 1차전 뒤", [bb("", "선발 라인업 변화\n“있을 것 같다”", 0.6, src=True)])
_P617 = [("F16_홍창기_A", "홍창기", "선발 제외\n정규시즌 타율 0.239", 0.1), ("P18_박해민_견제사", "박해민", "1번 타자\n1차전 팀 7안타 중 3안타", 3.0), ("P18_이재원", "이재원", "우익수 선발\n정규시즌 9홈런", 5.0)]
SC[61.8] = S(0, "people", ph=420, title="LG가 바꾼 이유", items=[dict(img=C + i, name=n, note=v, at=t, noteAt=t + 0.2, bad=(j == 0)) for j, (i, n, v, t) in enumerate(_P617)])
SC[61.9] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 2차전 전", [bb("이재원 선발 이유", "“언젠가는 쓸 건데\n빨리 쓰시죠”", 3.0)])
SC[62] = pv(0, C + "P18_박해민_견제사", "박해민", "LG 1번 타자 · 2차전", [vstamp("라인업 변화 · 1번 자리만 성공", 0.6, "gold", size=48)], stats=[st("2차전", "4타수 3안타", 2.4, hi=True), st("1·2차전", "이틀 연속 3안타", 3.4)])
_P63 = [("P18_송찬의_상체", "송찬의", "6번 → 2번\n4타수 무안타"), ("P18_이재원", "이재원", "새 선발\n4타수 4삼진")]
SC[63] = S(0, "people", ph=420, title="LG가 바꾼 자리 · 2차전", items=[dict(img=C + i, name=n, note=v, at=0.2 + j * 0.5, noteAt=0.3 + j * 0.6, bad=True) for j, (i, n, v) in enumerate(_P63)],
           text="8타수 무안타 · 삼진 4개", textAt=3.0)
SC[64] = pv(0, C + "P18_이재원", "이재원", "LG 우익수 · 2차전", [vstamp("네 타석 모두 삼진", 1.2, "bad", size=54)], stats=[st("포스트시즌", "첫 선발", 0.3)], chain="j64")
SC[64.5] = pv(0, C + "P18_이재원", "이재원", "LG 우익수 · 2차전", [vstamp("네 타석 모두 삼진", -1, "bad", size=54)], stats=[st("포스트시즌", "첫 선발", -1), st("방망이에 맞힌 공", "파울 1개", 0.6, hi=True)], chain="j64", cont=True)
SC[65] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 경기 뒤", [bb("", "8회 투 아웃 1·2루 · 대타 없이 이재원", 0.2, src=True), bb("", "이재원의 한 방을 봤다", 2.8, src=True), bb("", "“이재원도 경험하는 단계”", 99)], chain="s65")
SC[66] = sp(0, C + "P15_염경엽_더그아웃", "염경엽", "LG 감독 · 경기 뒤", [bb("", "8회 투 아웃 1·2루 · 대타 없이 이재원", -1, src=True), bb("", "이재원의 한 방을 봤다", -1, src=True), bb("경기 뒤", "“이재원도 경험하는 단계”", 1.0)], chain="s65", cont=True)
SC[67] = pv(0, C + "P18_한준수_세리머니", "한준수", "KIA 포수 · 2차전", [], chain="j67")
SC[68] = pv(0, C + "P18_한준수_세리머니", "한준수", "KIA 포수 · 2차전", [],
            stats=[st("공격", "1회 적시 2루타", 0.2, hi=True), st("수비", "3회 견제사", 1.2, hi=True)], chain="j67", cont=True)
SC[68.3] = sp(0, C + "F16_이범호", "이범호", "KIA 감독", [bb("경기 전", "한준수와 할 때\nLG전 성적이 훨씬 좋아", 1.4, src=True), bb("경기 뒤", "1루 코치 콜이 안 들리는\n빈틈을 파고들자", 99, src=True)], chain="b68")
SC[68.6] = sp(0, C + "F16_이범호", "이범호", "KIA 감독", [bb("경기 전", "한준수와 할 때\nLG전 성적이 훨씬 좋아", -1, src=True), bb("경기 뒤", "1루 코치 콜이 안 들리는\n빈틈을 파고들자", 3.0, src=True)], chain="b68", cont=True)
SC[69] = sp(0, C + "P18_한준수_세리머니", "한준수", "KIA 포수 · 경기 뒤", [bb("", "“팀에 민폐만\n끼치지 말자는 생각”", 0.4)], chain="h69")
SC[69.5] = sp(0, C + "P18_한준수_세리머니", "한준수", "KIA 포수 · 경기 뒤", [bb("", "“팀에 민폐만\n끼치지 말자는 생각”", -1), bb("", "“올러가 리드대로\n잘 따라와 줘서”", 0.2)], chain="h69", cont=True)
SC[69.7] = S(0, "people", ph=420, title="2차전 승부 정리", items=[dict(img=C + "P18_올러_포효", name="올러", note="6이닝 2실점\n중심 타선 8타수 무안타", at=0, noteAt=0.2, bad=False), dict(img=C + "P18_한준수_세리머니", name="한준수", note="1회 적시 2루타\n3회 견제사", at=0.1, noteAt=0.3, bad=False)], text="1회에 5점", textAt=1)   # 10/18 검수: 챕터 결론 한 줄
# ── 3장 3차전 예측 ──
SC[70] = S(0, "toc", on=2)
SER1 = [g5(n="1차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="2차전", venue="광주", home="KIA", win="KIA", at=0),
        g5(n="3차전", venue="잠실", home="LG", at=0, glow="LG", glowAt=0.6), g5(n="4차전", venue="잠실", home="LG", at=0), g5(n="5차전", venue="광주", home="KIA", at=0)]
SC[71] = S(0, "series5", tc=TCKL, title="3차전 20일(화) 6시 반 잠실", games=SER1, chain="s71")
SC[72] = S(0, "duel", title="3차전 선발 · 경기 뒤 예고", left={"img": C + "P18_시라카와_투구B", "name": "시라카와", "team": "KIA", "role": "이범호 감독 예고", "at": 0},
           right={"img": C + "P18_카라스코_투구", "name": "카라스코", "team": "LG", "role": "염경엽 감독 예고", "at": 0.5}, vsAt=0.3)
SC[73] = pv(0, C + "FA9_시라카와_투구", "시라카와", "KIA 3차전 선발", [vtrend([dict(x="시즌 전체", v=4.75, vt="4.75", at=1.6)], title="평균자책점 · 정규시즌")], stats=[st("정규시즌", "18경기 4승 5패", 0.2)], chain="w73")
SC[74] = pv(0, C + "FA9_시라카와_투구", "시라카와", "KIA 3차전 선발", [vtrend([dict(x="시즌 전체", v=4.75, vt="4.75", at=-1), dict(x="LG 상대", v=7.71, vt="7.71 · 2경기", c="bad", at=1.4)], title="평균자책점 · 정규시즌")],
            stats=[st("LG전 2경기 1패", "피홈런 4개 · 9⅓이닝", 0.6, hi=True)], chain="w73", cont=True)
SC[75] = pv(0, C + "FA9_시라카와_투구", "시라카와", "KIA 3차전 선발", [vtrend([dict(x="시즌 전체", v=4.75, vt="4.75", at=-1), dict(x="LG 상대", v=7.71, vt="7.71 · 2경기", c="bad", at=-1),
                                                                     dict(x="잠실", v=4.32, vt="4.32 · 2경기", at=0.6)], title="평균자책점 · 정규시즌")],
            stats=[st("LG전 2경기 1패", "피홈런 4개 · 9⅓이닝", -1, hi=True)], chain="w73", cont=True)
SC[76] = pv(0, C + "P15_카라스코_WC", "카라스코", "LG 3차전 선발", [vtrend([dict(x="시즌 전체", v=4.05, vt="4.05", at=1.6)], title="평균자책점 · 정규시즌")], stats=[st("정규시즌", "11경기 6승 3패", 0.2)], chain="c76")
SC[77] = pv(0, C + "P15_카라스코_WC", "카라스코", "LG 3차전 선발", [vtrend([dict(x="시즌 전체", v=4.05, vt="4.05", at=-1), dict(x="KIA 상대", v=8.31, vt="8.31 · 1경기", c="bad", at=3.2)], title="평균자책점 · 정규시즌")], stats=[st("KIA전", "4⅓이닝 7안타 4점", 1.0, hi=True)], chain="c76", cont=True)
SC[77.5] = pv(0, C + "P15_카라스코_WC", "카라스코", "LG 3차전 선발", [vtrend([dict(x="시즌 전체", v=4.05, vt="4.05", at=-1), dict(x="KIA 상대", v=8.31, vt="8.31 · 1경기", c="bad", at=-1), dict(x="잠실", v=4.88, vt="4.88 · 5경기", at=0.6)], title="평균자책점 · 정규시즌")],
            stats=[st("KIA전", "4⅓이닝 7안타 4점", -1, hi=True)], chain="c76", cont=True)
SC[78] = pv(0, C + "P15_카라스코_WC", "카라스코", "LG 3차전 선발", [vtrend([dict(x="시즌 전체", v=4.05, vt="4.05", at=-1), dict(x="KIA 상대", v=8.31, vt="8.31 · 1경기", c="bad", at=-1), dict(x="잠실", v=4.88, vt="4.88 · 5경기", at=-1)], title="평균자책점 · 정규시즌")],
            stats=[st("와일드카드 vs 두산", "6이닝 1실점", 0.3, hi=True)], chain="c76", cont=True)
_CT = [dict(x="시즌 전체", v=4.05, vt="4.05", at=-1), dict(x="KIA 상대", v=8.31, vt="8.31 · 1경기", c="bad", at=-1), dict(x="잠실", v=4.88, vt="4.88 · 5경기", at=-1)]
SC[78.2] = pv(0, C + "P15_카라스코_WC", "카라스코", "LG 3차전 선발", [vtrend(_CT, title="평균자책점 · 정규시즌")], stats=[st("8월 잠실 데뷔전 vs 두산", "7이닝 퍼펙트", 0.3, hi=True), st("염경엽 · 데뷔전 뒤", "“완벽하게 던졌다”", 3.6)], chain="c76", cont=True)
SC[78.4] = pv(0, C + "P15_카라스코_WC", "카라스코", "LG 3차전 선발", [vtrend(_CT, title="평균자책점 · 정규시즌")], stats=[st("막판 세 경기", "평균자책점 6.38", 0.4)], chain="c76", cont=True)
_BP = [dict(k="불펜\n이닝", l="10⅔이닝", r="5이닝", lv=10.67, rv=5), dict(k="이틀 연속\n던진 투수", l="3명", r="3명", lv=3, rv=3)]
SC[79] = S(0, "faceoff", title="1·2차전 불펜 사정", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=300,
           rows=[dict(r, at=0.3) for r in _BP], chain="bp")
SC[80] = S(0, "faceoff", title="1·2차전 불펜 사정", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=300,
           rows=[dict(r, at=0) for r in _BP], chain="bp", cont=True)
SC[80.5] = S(0, "faceoff", title="1·2차전 불펜 사정", left={"team": "LG", "name": "LG"}, right={"team": "KIA", "name": "KIA"}, leftColor=LGB, rightColor=KIAC, pw=300,
             rows=[dict(r, at=0) for r in _BP], chain="bp", cont=True)
SC[81] = sp(0, C + "P18_이범호_C", "이범호", "KIA 감독 · 경기 뒤", [bb("", "전상현\n이틀 연속 1⅓이닝", 0, src=True), bb("", "“감독으로서\n미안한 마음”", 0.6)])
SC[81.3] = sp(0, C + "P18_전상현_역투", "전상현", "KIA 마무리 · 경기 뒤", [bb("", "“매 경기 등판도\n할 수 있다”", 1.0), bb("", "“3차전에\n끝내도록 하겠다”", 2.8)])
SC[81.5] = S(0, "duel", title="3차전 열쇠 · 선발이 얼마나 버티나", left={"img": C + "FA9_시라카와_투구", "name": "시라카와", "team": "KIA", "role": "KIA 선발 · 불펜 3명 연투", "at": 0},
             right={"img": C + "P18_카라스코_투구", "name": "카라스코", "team": "LG", "role": "LG 선발 · 롱릴리프 없음", "at": 0}, vsAt=0)
SC[81.7] = pv(0, C + "P18_손주영", "손주영", "LG 투수", [vstamp("목 담 증세 뒤 복귀", 0.6, "gold", size=50)], stats=[st("2차전 6회", "1이닝 무실점", 2.2, hi=True), st("1차전 전 · 염경엽", "“중간에서 한 번 투입”", 4.4)])
SC[82] = S(0, "series5", tc=TCKL, title="3차전 20일(화) 6시 반 잠실", games=SER1, chain="s71x", pills=[dict(label="19일 하루 휴식 · LG에 더 반가워", at=0.6, c=LGB)])
SC[83] = S(0, "cells", title="역대 5전 3선승제 준플레이오프 · 1·2차전 연승 팀", cols=9, cw=150, ch=110, chain="c83",
           items=[dict(t="", hi=(k < 7), c=GOLD, at=0.1 + k * 0.08) for k in range(9)], text="9번 중 7번 플레이오프 · 77.8%", textAt=3)
SC[83.5] = S(0, "cells", title="역대 5전 3선승제 준플레이오프 · 1·2차전 연승 팀", cols=9, cw=150, ch=110, chain="c83", cont=True,
             items=[dict(t="", hi=True, c=(GOLD if k < 7 else GRAY), at=(-1 if k < 7 else 0.3 + (k - 7) * 0.2)) for k in range(9)], text="2번은 0승 2패 팀이 뒤집었다", textAt=0.8)
_GS = [("3/31", "K"), ("4/1", "L"), ("4/2", "L"), ("5/19", "K"), ("5/21", "L"), ("5/29", "L"), ("5/30", "L"), ("5/31", "L"), ("6/16", "L"),
       ("6/17", "K"), ("6/18", "K"), ("9/26", "K"), ("10/3", "K"), ("10/4", "K"), ("10/5", "K"), ("10/12", "K"), ("10/17", "K"), ("10/18", "K")]
SC[84] = S(0, "gamestrip", tc=TCKL, title="2026 KIA vs LG 맞대결", teams={"K": "KIA", "L": "LG"}, games=[list(x) for x in _GS], rows=[[0, 8], [9, 17]],
           at=0.2, step=0.04, dimTo=9, groups=[{"from": 9, "to": 17, "label": "6월 17일부터 · KIA 9연승", "team": "KIA", "at": 1.6}])
SC[84.3] = sp(0, C + "P18_이범호_C", "이범호", "KIA 감독 · 경기 뒤", [bb("", "타자 컨디션 올라와\n3차전 앞두고 고무적", 1.4, src=True)])
SC[84.5] = pv(0, C + "P17_김도영_질주", "김도영", "KIA 3루수", [], stats=[st("1차전", "홈런 2개", 0.2, hi=True), st("2차전", "무안타 · 두 번 출루", 1.4)])
SC[84.7] = sp(0, C + "P18_염경엽", "염경엽", "LG 감독 · 1차전 뒤", [bb("", "“김도영이 실투들을\n놓치지 않았다”", 0.8)])
SC[84.8] = S(0, "debate", title="MLB파크 · 경기 뒤 글", noVS=True, icons=1, left=dict(label="KIA 말머리", c="bad", t="“시라카와 안좋으면\n불펜데이로..”", size=46, at=0.6), right=dict(label="오늘의 베스트", c=LGB, t="“3,4 차전은 엘지가\n이길 가능성이 높죠”", size=46, at=2.4))   # 10/18 검수: 판단 편은 팬 여론도(MLB파크 글 제목)
SC[85] = S(0, "matchup", left="LG", right="KIA", score="3차전", tag="야구자판기 예상", text="3차전은 LG", size=96)
SC[86] = S(0, "faceoff", title="3차전 · LG로 본 이유", left={"img": C + "P18_카라스코_투구", "name": "카라스코", "team": "LG", "role": "LG 선발"}, right={"img": C + "FA9_시라카와_투구", "name": "시라카와", "team": "KIA", "role": "KIA 선발"}, leftColor=LGB, rightColor=KIAC, pw=300,
           rows=[dict(k="잠실\n평균자책점", l="4.88", r="4.32", lv=4.88, rv=4.32, low=True, w="r", at=0.3), dict(k="상대 팀에게\n맞은 홈런", l="0개 · 4⅓이닝", r="4개 · 9⅓이닝", lv=0, rv=4, low=True, w="l", at=2.2)])
SER2 = [g5(n="1차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="2차전", venue="광주", home="KIA", win="KIA", at=0),
        g5(n="3차전", venue="잠실", home="LG", win="LG", at=0.4), g5(n="4차전", venue="잠실", home="LG", win="KIA", at=1.2), g5(n="5차전", venue="광주", home="KIA", off=True, at=0)]
SC[87] = S(0, "series5", tc=TCKL, title="야구자판기 예상 · KIA 3승 1패", games=SER2, chain="ser", pills=[dict(label="중심 타선이 계속 막히면", at=99, c=LGB), dict(label="3차전에서 바로 끝날 수도", at=99, c="#12161F")])   # 10/18 검수: 다음 장면과 표 높이 같게(알약 자리만 잡음)
SER3 = [g5(n="1차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="2차전", venue="광주", home="KIA", win="KIA", at=0),
        g5(n="3차전", venue="잠실", home="LG", win="KIA", maybe=True, tag="만약", at=2.6), g5(n="4차전", venue="잠실", home="LG", off=True, at=0), g5(n="5차전", venue="광주", home="KIA", off=True, at=0)]
SC[88] = S(0, "series5", tc=TCKL, title="변수 · LG의 중심 타선", games=SER3, chain="ser", cont=True, pills=[dict(label="중심 타선이 계속 막히면", at=0.3, c=LGB), dict(label="3차전에서 바로 끝날 수도", at=2.6, c="#12161F")])
SC[89] = S(0, "question", text="3차전\nLG가 잠실에서 반격할까요?\nKIA가 3연승으로 끝낼까요?", logos=["LG", "KIA"], size=88)

KEYS = sorted(SC); IDX = {k: i for i, k in enumerate(KEYS)}
SC = {IDX[k]: v for k, v in SC.items()}
N = len(TEXT)
assert sorted(SC) == list(range(N)), (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "경기 흐름", "title": "경기 흐름", "from": IDX[4], "to": IDX[21]},
      {"key": "승부를 가른 이유", "title": "승부를 가른 이유", "from": IDX[51], "to": IDX[69.7]},
      {"key": "3차전 예측", "title": "3차전 예측", "from": IDX[70], "to": IDX[89]}]

TAGS = ["2026 준PO", "준플레이오프", "준PO 2차전", "준플레이오프 2차전", "준플레이오프 3차전", "준PO 3차전 예측", "KIA LG 준플레이오프", "KIA 타이거즈", "LG 트윈스",
        "가을야구", "올러", "임찬규", "전상현", "카스트로", "나성범", "김선빈", "한준수", "이재원", "박해민", "시라카와", "카라스코", "김도영", "염경엽", "이범호",
        "프로야구", "KBO", "2026 프로야구", "야구자판기", "오스틴", "네일", "케네디"]
DESC = ("2026 프로야구 준플레이오프 2차전, KIA 타이거즈가 LG 트윈스를 6대3으로 이기고 2연승을 했어요. 1회말 5점 빅이닝 등 주요 장면을 돌아보고, 왜 이런 결과가 나왔는지 세 가지로 분석한 뒤 잠실 3차전을 예측했어요.\n\n"
        "KIA는 1회말 박재현의 안타와 도루, 김도영의 볼넷 뒤 카스트로의 결승 적시타로 앞서갔고, 나성범·김선빈·한준수의 세 타자 연속 2루타로 5대0을 만들었어요. "
        "LG 선발 임찬규는 아웃 하나만 잡고 28구 6피안타 1볼넷 5실점으로 내려갔어요. 1회말 5점은 포스트시즌 1회말 최다 득점 타이 기록이에요.\n\n"
        "KIA 올러는 6이닝 94구 6피안타 8탈삼진 2실점으로 승리 투수가 됐고, 마무리 전상현은 이틀 연속 4아웃 세이브로 데일리 MVP에 뽑혔어요. "
        "LG는 홍창기를 빼고 박해민 1번, 이재원 우익수로 라인업을 바꿨지만 오스틴·문정빈·문보경 중심 타선은 1·2차전 22타수 3안타에 그쳤어요.\n\n"
        "3차전은 10월 20일 화요일 저녁 6시 30분 잠실에서 KIA 시라카와와 LG 카라스코의 선발 맞대결이에요. 야구자판기의 예상은 3차전 LG, 시리즈는 KIA 3승 1패예요.\n\n"
        "야구자판기는 매일 오늘의 야구 이슈를 정리해 드려요.\n\n"
        "3차전, LG가 잠실에서 반격할까요? KIA가 3연승으로 끝낼까요? 댓글로 알려 주세요.\n\n"
        "기록: KBO 게임센터 준플레이오프 2차전 박스스코어, KBO 기록실(2026 정규시즌 투수 팀별·구장별 기록). 발언: 경기 전후 양 팀 감독·선수 인터뷰(스포츠경향, 스포츠월드, 뉴스핌, 뉴스엔, 머니투데이, SPOTV, 한국일보, 일간스포츠). 경기 내용·기록 기사: 톱스타뉴스, 데일리안, 세계일보, 마이데일리, 전남일보, 서울신문, 이코노믹리뷰, 한겨레. 팬 반응: MLB파크 한국야구타운. 역대 기록: 아주경제, 스포츠조선\n"
        "사진: KIA 타이거즈 제공, LG 트윈스 제공, MK스포츠, 스포츠조선, 스타뉴스, 스포츠경향, 연합뉴스, 스포티비뉴스, 각 구단 공식 프로필")
SOURCE = "사실 출처 = KBO 게임센터 박스스코어(10/18 직접 조회) + KBO 기록실 + 기사 원문 — 프로젝트 claude/1018-롱폼19-준PO2차전-근거모음.md."

EP = {"date": "2026-10-18", "gameDate": "2026-10-18", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.25, "ttsTempoSlow": 1.2,
      "rev": "1018-long19-v1", "topic": "준PO2차전리뷰", "endcardSec": 10, "totalSec": 481,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "야구롱폼/영상/2026-10-18/롱폼_준PO2차전_썸네일.jpg", "source": SOURCE,
      "youtube": {"title": "2026 준PO 2차전 리뷰 | 1회 5점 빅이닝, KIA가 LG 또 잡은 이유와 3차전 예측 #준플레이오프 #KIA #LG",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#준플레이오프", "#가을야구", "#KIA타이거즈", "#LG트윈스", "#올러", "#전상현", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {20, 69.7, 89}   # 10/18 23:16 사용자 "흐름이 너무 느려" — 챕터 끝·질문만
    HOLD = {0: 0.3, 3: 0.5, 9: 0.6, 10: 0.6, 11: 0.6, 12: 0.6, 14: 0.6, 16: 0.6, 20: 0.6, 21: 0.5, 56: 0.6, 59: 0.6, 63: 0.6, 69.5: 0.5, 69.7: 0.6, 75: 0.6, 78.4: 0.6, 80: 0.6, 83.5: 0.6, 85: 0.5}
    for i, l in enumerate(EP['lines'][:-1]):
        k = KEYS[i]
        if k in SLOW: l['pace'] = 'slow'
        if k in HOLD: l['gapAfter'] = min(HOLD[k], 0.35)
    EP['lines'][0]['pauseMax'] = 0.12
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-18_롱폼2.json')
    SUBFIX = {'KIA는 마무리\n전상현을 올렸고': 'KIA는\n마무리 전상현을 올렸고', '타자들도 공격적으로\n나갔다고 했어요': '타자들도\n공격적으로 나갔다고 했어요',
              '1이닝씩 끊어서\n막았다고 했어요': '1이닝씩\n끊어서 막았다고 했어요', '불펜으로 막을 수\n있다고 봤대요': '불펜으로\n막을 수 있다고 봤대요',
              '하지만 2번으로\n올라간 송찬의와': '하지만\n2번으로 올라간 송찬의와', '팀에 민폐만 끼치지\n말자는 생각이었대요': '팀에 민폐만\n끼치지 말자는 생각이었대요',
              '리드대로 잘 따라와\n줘서 고맙다고 했고요': '리드대로 잘 따라와 줘서\n고맙다고 했고요', '10과 3분의\n2이닝을 던졌어요': '10과 3분의 2이닝을\n던졌어요',
              '감독으로서 미안한\n마음이라고 했어요': '감독으로서\n미안한 마음이라고 했어요', '김도영이 실투를\n놓치지 않았다고 했죠': '김도영이\n실투를 놓치지 않았다고 했죠', '카운트 잡는 공을 안타로\n만드는 싸움이었대요': '카운트 잡는 공을\n안타로 만드는 싸움이었대요', '올러는 오스틴 문정빈\n문보경을 상대로': '올러는\n오스틴 문정빈 문보경을 상대로', '라인업 변화가 있을\n거라고 답했는데요': '라인업 변화가\n있을 거라고 답했는데요', '이재원을 3구 삼진으로\n잡았어요': '이재원을\n3구 삼진으로 잡았어요'}   # 10/18 검수: 자막 줄바꿈은 뜻 단위
    for l in EP['lines']:
        l['sub'] = '|'.join(SUBFIX.get(x, x) for x in l['sub'].split('|'))
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
