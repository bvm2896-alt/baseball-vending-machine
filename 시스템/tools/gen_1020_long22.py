# -*- coding: utf-8 -*-
"""10/20 롱폼㉒ 「준PO 3차전 리뷰 · 승부를 가른 이유 · 플레이오프 1차전 예상」 (음성 API · 줄별 배속).
대사 = tools/text_1020_long22.py (v1.4). 근거 = KBO 게임센터 박스스코어(20261020HTLG0) 10/20 직접 조회 + 기사 본문
— 프로젝트 claude/1020-롱폼22-준PO3리뷰-PO1-팩트체크.md. 체인지업 애니메이션 = tools/scenes_cpitch_1020.js (inject_cpitch_1020.py).
같은 날짜 두 번째 롱폼 → episodes/2026-10-20_롱폼2.json (롱폼㉑ 두산방출 = 2026-10-20_롱폼.json).
사진 = 사진 은행(카드/P18_* 등 준PO 2차전 사진) — 오늘 경기 사진은 사용자 허락 뒤 교체."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1020_long22.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]

def pre(t):
    for a, b in (('12개', '열두 개'), ('13대1', '십삼 대 일'), ('9대0', '구 대 영'), ('1대0', '일 대 영'), ('7대0', '칠 대 영')): t = t.replace(a, b)
    t = t.replace('1과 3분의 1이닝', '일과 삼분의 일 이닝').replace('145m', '백사십오 미터').replace('16cm', '십육 센티미터')
    t = t.replace('42.9%', '사십이 쩜 구 퍼센트').replace('11.1%', '십일 쩜 일 퍼센트').replace('7.71', '칠 쩜 칠일').replace('3.24', '삼 쩜 이사').replace('5.25', '오 쩜 이오')
    t = t.replace('MVP', '엠브이피').replace('1사', '일사').replace('2회초', '이회초').replace('6회말', '육회말')
    t = t.replace('4번 올라', '네 번 올라').replace('4번 모두', '네 번 모두').replace('3번째', '세 번째')
    t = t.replace('7명', '일곱 명').replace('4경기', '네 경기').replace('9개', '아홉 개').replace('2개', '두 개')
    t = t.replace('76개', '칠십육 개').replace('7점', '칠 점').replace('1점', '일 점').replace('112승', '백십이 승')
    t = t.replace('12일 동안', '십이 일 동안').replace('7일을', '칠 일을').replace('7일 쉰', '칠 일 쉰').replace('2년 만', '이 년 만').replace('37년 만', '삼십칠 년 만')
    t = t
    for a, b in (('2만 3650명', '이만 삼천육백오십 명'), ('23살 18일', '스물세 살 십팔 일'), ('16경기', '열여섯 경기'), ('41경기', '마흔한 경기'), ('4경기', '네 경기'), ('2경기', '두 경기'),
                 ('안타 16개', '안타 열여섯 개'), ('안타 3개', '안타 세 개'), ('9명', '아홉 명'), ('5년 동안', '오 년 동안'), ('23년 만', '이십삼 년 만'), ('오후 2시', '오후 두 시'),
                 ('1, 2회', '일, 이 회'), ('1, 2차전', '일, 이차전'), ('세이브 2개', '세이브 두 개'), ('12타수 7안타', '십이 타수 칠 안타'), ('9타수 3안타', '구 타수 삼 안타'), ('8타점', '팔 타점')):
        t = t.replace(a, b)
    t = t.replace('KBO', '케이비오')
    return t
def narr_of(t):
    n = narr_of15(pre(t))
    n = n.replace('십 월', '시월')
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|칠|팔|구) 월', r'\1월', n)
    n = re.sub(r'(일|이|삼|사|오|육|칠|팔|구) (차전|연승|연패)', r'\1\2', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타|타점|루타)(?![가-힣]*차전)', r'\1\2', n)
    return n.replace('사이닝', '사 이닝')
def sub_of(t): return re.sub(r'\.(?= / )', '', t).replace('1과 3분의 1이닝', '1⅓이닝')

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
KIAC, LGB, SSB = "#C70125", "#2563EB", "#074CA1"
TCKL = {"LG": LGB}
C, G, N = '카드/', '경기/', '누끼/'
def pv(img, name, sub, viz=(), team="KIA", **k): return S(0, "pstat", img=img, team=team, name=name, sub=sub, stats=k.pop("stats", []), viz=list(viz), **k)
def sp(img, name, sub, bubbles, team="KIA", **k): return S(0, "speech", img=img, team=team, name=name, sub=sub, bubbles=bubbles, **k)
def dm(title, score, outs, steps, **k):   # 원정 KIA(위) · 홈 LG — score = [KIA, LG]
    return S(0, "diamond", title=title, bat="KIA", batIdx=0, score=score, outs=outs, steps=steps, away="KIA", home="LG", **k)
def g5(**k): return dict(**k)
N3 = [None, None, None]
SHI, KAR, KEN = C + "P18_시라카와_투구B", C + "P18_카라스코_투구", C + "P18_케네디_투구"
NA, KDY, BJW, BJH, HJS = C + "P18_나성범_적시타", C + "P17_김도영_질주", C + "P18_박정우", C + "P18_박재현_득점", C + "P18_한준수_세리머니"
LBH, NAIL, HUR = C + "P18_이범호", C + "P17_네일_역투", C + "P20_후라도_투구"
FED, KOO = N + "경기_페덱", N + "경기_구자욱_세리머니_0827_삼성제공"

SC = []
P22 = C + 'P22_'
def fg(**k): return S(0, "facegrid", **k)
def tl(img, name, sub, items, team="KIA", **k):   # 연표는 사진(또는 로고) 옆 viz steps — 글자만 있는 장면 금지(10/13)
    return pv(img, name, sub, [vsteps([stp(d, x, a, c=("good" if h else None)) for d, x, a, h in items])], team=team, **k)
# ── 훅 ── 0~3
SER = [g5(n="1차전", venue="광주", home="KIA", win="KIA", at=0), g5(n="2차전", venue="광주", home="KIA", win="KIA", at=0),
       g5(n="3차전", venue="잠실", home="LG", win="KIA", at=0.3), g5(n="4차전", venue="잠실", home="LG", at=0), g5(n="5차전", venue="광주", home="KIA", at=0)]
SC.append(S(0, "matchup", left="KIA", right="LG", score="13 : 1", tag="준플레이오프 3차전 · 10월 20일 잠실", text="3연승 · 플레이오프 진출", size=84))   # 1
SC.append(S(0, "series5", tc=TCKL, title="준플레이오프 · KIA 3승 0패", games=SER, pills=[dict(label="해태 시절 포함 · 첫 통과", at=1.2, c=KIAC)]))   # 2
SC.append(S(0, "photo", img=G + "KIA_잠실마지막승리_1020_연합", fit="cover", text="잠실야구장\n마지막 프로야구 경기", size=92, h=500))         # 3
SC.append(S(0, "toc", on=-1, itemFrom=99))                                                                                     # 4
# ── 1장 · 3차전 흐름 ── 4~23
SC.append(S(0, "duel", title="준플레이오프 3차전 선발", left={"img": P22 + "시라카와_투구", "name": "시라카와", "team": "KIA", "role": "KIA 선발", "at": 0},
            right={"img": C + "P18_카라스코_투구", "name": "카라스코", "team": "LG", "role": "LG 선발", "at": 0.6}, vsAt=0.3))        # 5
_LU = [("박정우", P22 + "박정우_적시타", "1번 중견수", 1), ("박재현", C + "P18_박재현_득점", "2번 좌익수", 1), ("김도영", C + "P17_김도영_질주", "3번 3루수", 0),
       ("카스트로", C + "P18_카스트로_엄지", "4번 1루수", 1), ("나성범", C + "P18_나성범_적시타", "5번 우익수", 1), ("김선빈", C + "P18_김선빈_2루타", "6번 지명타자", 0),
       ("한준수", P22 + "한준수_솔로", "7번 포수", 1), ("김규성", P22 + "김규성_주루전신", "8번 2루수", 1), ("하주석", P22 + "하주석_타격", "9번 유격수", 1)]
SC.append(fg(title="KIA 선발 · 왼손 타자 7명", cols=5, card=True, items=[dict(name=n, img=im, team="KIA", pos=ps, at=0.1 + i * 0.04, **({"hi": True} if l else {"dim": True})) for i, (n, im, ps, l) in enumerate(_LU)]))   # 6
SC.append(sp(P22 + "이범호_기자회견", "이범호", "KIA 감독 · 10월 20일 경기 전", [bb("한국아이닷컴", "“왼쪽 타자들이 훨씬\n공략을 잘했던 부분”", 1.0)]))   # 7
SC.append(S(0, "hrcam", img=P22 + "나성범_솔로홈런", name="나성범", team="KIA", bug=dict(inn="2회초", score=[0, 0], outs=0, bases=N3), launchAt=1, dir="center", burst="솔로 홈런", runners=["나성범"], scoreTo=[1, 0]))   # 8
SC.append(S(0, "rally", bug=dict(inn="2회초", score=[1, 0], outs=0, bases=N3), plays=[
    dict(name="김선빈", img=C + "P18_김선빈_2루타", res="뜬공 아웃", kind="out", at=0, bases=N3, outs=1, score=[1, 0]),
    dict(name="한준수", img=P22 + "한준수_솔로", res="실책 출루", kind="on", at=1, bases=["한준수", None, None], outs=1, score=[1, 0]),
    dict(name="김규성", img=P22 + "김규성_주루전신", res="안타", kind="on", at=2, bases=["김규성", "한준수", None], outs=1, score=[1, 0]),
    dict(name="하주석", img=P22 + "하주석_타격", res="볼넷", kind="on", at=2.45, bases=["하주석", "김규성", "한준수"], outs=1, score=[1, 0]),
    dict(name="박정우", img=P22 + "박정우_적시타", res="적시타", kind="run", at=4, bases=["박정우", "하주석", "김규성"], outs=1, score=[2, 0], rbi="+1")]))   # 9
SC.append(S(0, "plog", img=C + "P15_카라스코_WC", name="카라스코", team="LG", sub="LG 선발 · 2회초 강판", stamp=dict(t="메이저리그 112승", at=1),
            blocks=[dict(type="inn", ip=4 / 3, at=2), dict(type="runs", n=5, at=2.3), dict(type="line", items=[["투구 수", "45개", 0, 3], ["피안타", "3개", 0, 4], ["볼넷", "2개", 0, 4.4], ["삼진", "0개", 1, 5]], at=3)]))   # 10
SC.append(pv(C + "P18_케네디_투구", "케네디", "LG 두 번째 투수", [vsteps([stp("2회초", "원 아웃 만루 · 투수 교체", 0.1), stp("2회초", "박재현 적시타 · 3대0", 1.0, c="bad")])], team="LG"))   # 11
SC.append(S(0, "hrcam", img=P22 + "김도영_만루포전신", name="김도영", team="KIA", bug=dict(inn="2회초", score=[3, 0], outs=1, bases=["박재현", "박정우", "하주석"]), launchAt=1.6, dir="lc", dist="145m", burst="만루 홈런",
            runners=["하주석", "박정우", "박재현", "김도영"], scoreTo=[7, 0]))   # 12
SC.append(S(0, "bars", title="준플레이오프 가장 긴 홈런", items=[dict(label="2026년 김도영", value=145, unit="m", at=0, hi=True), dict(label="2019년 준플레이오프", value=135, unit="m", at=1.0)],
            max=150, text="2001년 한국시리즈 기록과 포스트시즌 최장 타이", textAt=2.0, size=52))                                       # 13
SC.append(pv(P22 + "김도영_만루포환호", "김도영", "KIA 3루수 · 2회초 만루 홈런", [], stats=[st("KIA 2회초", "7점", 0.1), st("23살 18일", "최연소 만루 홈런", 1.0, hi=True)], chain="kdy"))   # 14
SC.append(pv(P22 + "김도영_만루포환호", "김도영", "준플레이오프 MVP", [vstamp("기자단 97표 중 84표", 3.0, "gold", size=46)],
             stats=[st("3경기", "9타수 3안타", 0.2), st("안타 3개", "모두 홈런", 1.4, hi=True), st("타점", "8개", 3.0)], chain="kdy", cont=True))   # 15
SC.append(pv(P22 + "김도영_만루포환호", "김도영", "10월 20일 경기 뒤 · 국민일보", [vstamp("“손맛만큼은 오늘이 좋았다”", 1.0, "gold", size=58)], chain="kdy", cont=True))   # 16
SC.append(S(0, "plog", img=P22 + "시라카와_투구", name="시라카와", team="KIA", sub="KIA 선발 · 3차전",
            blocks=[dict(type="inn", ip=5, tag1="삼자범퇴", at=1), dict(type="runs", n=1, at=2), dict(type="k", n=9, at=2.3)]))   # 17
SC.append(pv(P22 + "시라카와_인사", "시라카와", "KIA 선발 · 3차전", [vtrend([dict(x="정규시즌 LG전", v=7.71, vt="7.71", c="bad", at=0.2)], title="평균자책점"),
                                                       vstamp("포스트시즌 첫 승 · 데일리 MVP", 2.4, "gold", size=46)], chain="s17", cont=True))   # 18
SC.append(pv(P22 + "시라카와_인사", "시라카와", "10월 20일 경기 뒤 · 일간스포츠", [vstamp("“도망가는 것이 아니라\n더 공격적으로”", 1.0, "gold", size=54)], chain="s17", cont=True))   # 19
SC.append(S(0, "scoreboard", title="준플레이오프 3차전 · 6회초까지", rows=[{"team": "KIA", "runs": [0, 7, 0, 0, 1, 1], "r": 9, "hi": True}, {"team": "LG", "runs": [0, 0, 0, 0, 0], "r": 0}],
            hi=[5, 6], label="5회 적시타 · 6회 솔로 · 9대0", labelAt=1.0))                                                           # 20
SC.append(pv(P22 + "한준수_솔로", "한준수", "KIA 포수 · 7회초", [vsteps([stp("6회말", "LG 1점", 0.1), stp("7회초", "한준수 솔로 홈런", 1.0, c="good"), stp("8회초", "KIA 3점 · 13대1", 2.0, c="good")])]))   # 21
SC.append(S(0, "scoreboard", title="준플레이오프 3차전", rows=[{"team": "KIA", "runs": [0, 7, 0, 0, 1, 1, 1, 3, 0], "r": 13, "hi": True}, {"team": "LG", "runs": [0, 0, 0, 0, 0, 1, 0, 0, 0], "r": 1}],
            label="안타 16개 · 선발 9명 안타·득점", labelAt=1.4))                                                                     # 22
SC.append(sp(C + "F16_이범호", "이범호", "KIA 감독 · 10월 20일 경기 뒤", [bb("스포츠경향 · 뉴스핌", "“시리즈 3연승은\n예상하지 못했다”", 0.6), bb("", "“나흘이라는 시간을 얻은 건\n힘이 된다”", 2.0)]))   # 23
SC.append(S(0, "matchup", left="KIA", right="LG", score="7 : 0", tag="2회초가 끝났을 때", text="일찍 기운 승부", size=84))           # 24 결론
# ── 2장 · 3차전의 의미 ── 24~34
SC.append(S(0, "toc", on=1))                                                                                                   # 25
SC.append(S(0, "photo", img="상황별/망상포스터_롱폼20", fit="contain", text="망상회 예측\n3연승 · 결승타는 카스트로나 나성범", size=72, h=500))   # 26
SC.append(pv(P22 + "나성범_솔로홈런", "나성범", "3차전 결승타", [vstamp("망상 적중", 2.0, "gold", size=50)], stats=[st("2회초 무사", "솔로 홈런", 0.4, hi=True)]))   # 27
SC.append(tl(None, "KIA 타이거즈", "준플레이오프 도전", [("1994년", "해태 · 탈락", 2.0, 0), ("2004년", "탈락", 2.3, 0), ("2006년", "탈락", 3.0, 0), ("2011년", "탈락", 3.3, 0)]))   # 28
SC.append(tl(None, "KIA 타이거즈", "한국시리즈 제외 · 시리즈 승리", [("1989년", "해태 · 플레이오프 승리", 0.4, 0), ("2026년", "37년 만의 시리즈 승리", 1.6, 1), ("2026년", "23년 만의 플레이오프", 3.0, 1)]))   # 29
SC.append(tl(None, "KIA 타이거즈", "준플레이오프 3연승 통과", [("2008년", "삼성", 0.6, 0), ("2023년", "NC", 1.0, 0), ("2026년", "KIA · 역대 세 번째", 2.0, 1)]))   # 30
SC.append(S(0, "photo", img=G + "잠실_마지막인사_1020_일간스포츠", fit="cover", text="2만 3650명 매진\n포스트시즌 41경기 연속", size=80, h=500))   # 31
SC.append(sp(P22 + "염경엽_더그아웃", "염경엽", "LG 감독 · 10월 20일 경기 뒤", [bb("머니투데이 · 스포츠경향", "“KIA에 타격에서 밀리면서\n힘든 시리즈가 됐다”", 0.6), bb("", "“기대만큼 성적을 내지 못해서\n죄송하다”", 2.2)], team="LG"))   # 32
SC.append(sp(C + "P18_박해민_견제사", "박해민", "LG 주장 · 10월 20일 경기 뒤", [bb("스포츠월드 · SPOTV", "“기대에 보답하지 못해\n정말 죄송하다”", 2.2)], team="LG"))   # 33
SC.append(tl(None, "잠실야구장", "LG · 두산 홈구장", [("1982년", "개장", 0.2, 0), ("2026년", "10월 20일 마지막 경기", 1.0, 1), ("2027년", "5년 동안 임시 구장", 2.4, 0), ("2032년", "새 돔구장 목표", 3.2, 0)], team="LG"))   # 34
SC.append(S(0, "matchup", left="KIA", right="LG", tag="10월 20일 · 잠실", text="KIA는 구단 첫 준PO 통과\nLG는 잠실과 작별", size=72))   # 35 결론
# ── 3장 · 승부를 가른 이유 ── 35~47
SC.append(S(0, "toc", on=2))                                                                                                   # 36
SC.append(S(0, "bars", title="카라스코 · 2026 KBO 피안타율", items=[dict(label="오른손 타자 상대", value=.185, dec=3, at=4), dict(label="왼손 타자 상대", value=.267, dec=3, at=6, hi=True)],
            max=.3, text="이유 하나 · 왼손 타자 7명", textAt=0.2, size=56))                                                             # 37
P0 = dict(tag="보통 오른손 투수 체인지업", brk=1, res="miss"); P1 = dict(tag="카라스코 체인지업", brk=.18, res="hit", hi=True)
GAP = dict(panel=1, text="메이저리그 평균보다\n약 16cm 덜 휨", at=2)
STATS = dict(title="카라스코 체인지업 헛스윙률", src="", at=0, max=50,
             rows=[dict(k="오른손 타자", v=42.9, at=4), dict(k="왼손 타자", v=11.1, at=5, hi=True)])
SC.append(S(0, "cpitch", panels=[dict(P0, enterAt=0), dict(P1, enterAt=0.5)], chain="cp"))                                      # 38
SC.append(S(0, "cpitch", panels=[dict(P0, at=1), P1], chain="cp", cont=True))                                                   # 39
SC.append(S(0, "cpitch", panels=[dict(P0, done=True), dict(P1, at=0)], gap=GAP, chain="cp", cont=True))                         # 40
SC.append(S(0, "cpitch", panels=[dict(P0, done=True), dict(P1, done=True)], gap=dict(GAP, at=None), chain="cp", cont=True))     # 41
SC.append(S(0, "cpitch", panels=[dict(P0, done=True), dict(P1, done=True)], gap=dict(GAP, at=None), stats=STATS, chain="cp", cont=True))   # 42
SC.append(pv(C + "P15_카라스코_WC", "카라스코", "3차전 · 2회초 강판", [vsteps([stp("결과", "카라스코 1⅓이닝 강판", 0.2, c="bad"), stp("승부수", "KIA 왼손 타자 7명", 1.0), stp("2회초", "KIA 7점", 2.0, c="good")])], team="LG"))   # 43
SC.append(pv(P22 + "나성범_6회홈런", "나성범", "이유 둘 · KIA 우익수", [], stats=[st("3차전", "4타수 2안타", 0.2), st("홈런", "2개", 2.0, hi=True), st("타점", "2점", 3.0)], chain="nsb"))   # 44
SC.append(pv(P22 + "나성범_6회홈런", "나성범", "10월 20일 경기 뒤 · 스포츠경향", [vstamp("“단기전은 분위기 싸움”", 0.4, "gold", size=58)], chain="nsb", cont=True))   # 45
SC.append(S(0, "plog", img=P22 + "시라카와_투구", name="시라카와", team="KIA", sub="이유 셋 · KIA 선발",
            blocks=[dict(type="zero", k="볼넷", stamp="볼넷 없음", at=2), dict(type="pitch", n=76, k="5이닝 투구 수", at=3)]))   # 46
SC.append(sp(P22 + "이범호_박수", "이범호", "KIA 감독 · 10월 20일 경기 뒤", [bb("스포츠경향 · 뉴스핌", "“1~2회 조금이라도 흔들리면\n교체할 생각이었다”", 0.4), bb("", "“너무 완벽했다”", 3.0)]))   # 47
SC.append(S(0, "people", ph=420, title="망상회 예측 · 두 선발 모두 초반에 흔들린다", items=[dict(img=C + "P15_카라스코_WC", name="카라스코", team="LG", note="2회 강판 · 적중", at=1, noteAt=3), dict(img=P22 + "시라카와_투구", name="시라카와", note="5이닝 버팀 · 빗나감", at=1, noteAt=4)], text="망상 반만 적중", textAt=5, size=84))   # 47-2 (10/21 사용자 제안)
SC.append(S(0, "people", ph=420, title="13대1 · 승부를 가른 이유", items=[dict(img=P22 + "이범호_기자회견", name="왼손 7명", note="이범호 감독의 승부수", at=0.6, noteAt=0.6),
            dict(img=P22 + "나성범_솔로홈런", name="나성범", note="홈런 2개", at=1.4, noteAt=1.4), dict(img=P22 + "시라카와_인사", name="시라카와", note="볼넷 0개", at=2.4, noteAt=2.4)]))   # 48 결론
# ── 4장 · 플레이오프 1차전 예상 ── 48~69
SC.append(S(0, "toc", on=3))                                                                                                   # 49
SC.append(S(0, "matchup", left="KIA", right="삼성", tag="10월 25일(일) 오후 2시 · 대구", text="플레이오프 1차전", size=84))         # 50
SC.append(tl(None, "삼성 라이온즈", "정규시즌 막판", [("정규시즌", "2위 · 플레이오프 직행", 0.2, 0), ("시즌 막판", "4경기 모두 패", 2.0, 0)], team="삼성"))   # 51
SC.append(tl(None, "삼성 라이온즈", "KIA 나흘 · 삼성 12일 휴식", [("10월 12일", "정규시즌 끝", 0.2, 0), ("10월 19일", "청백전", 1.0, 0), ("10월 25일", "플레이오프 1차전", 1.6, 1)], team="삼성"))   # 52
SC.append(S(0, "matchup", left="KIA", right="삼성", score="9승 7패", tag="2026 정규시즌 맞대결", text="KIA 우세", size=80))       # 53
SC.append(pv(P22 + "김도영_만루포전신", "김도영", "KIA 3루수 · 2026 홈런왕", [], stats=[st("시즌", "45홈런", 0.4), st("삼성전 · 16경기", "홈런 9개", 2.0, hi=True)]))   # 54
SC.append(S(0, "people", ph=420, title="삼성 중심 타자 · 올해 KIA전", items=[dict(img=C + "FA9_디아즈_경기", name="디아즈", team="삼성", note="타율 0.214 · 홈런 1개", at=0.2, noteAt=1), dict(img=C + "FA10_최형우_100타점", name="최형우", team="삼성", note="타율 0.190", at=0.2, noteAt=1)]))   # 10/21 추가 · KBO 기록실
SC.append(pv(C + "FA9_디아즈_경기", "디아즈", "삼성 · 올해 26홈런", [vtrend([dict(x="NC전", v=6, vt="6개", at=1), dict(x="키움전", v=5, vt="5개", at=1.3), dict(x="KIA전", v=1, vt="1개", c="bad", at=2)], title="상대 팀별 홈런")], team="삼성",
            stats=[st("KIA전 16경기", "타율 2할 1푼 4리", 1, hi=True)]))
SC.append(pv(C + "FA10_최형우_100타점", "최형우", "삼성 · 전 KIA 4번 타자", [vstamp("KIA에서 9시즌", 0.4, "gold", size=46)], team="삼성",
            stats=[st("KIA전 타율", "1할 9푼", 2, hi=True), st("볼넷", "11개", 3), st("타점", "12개", 3.3)]))
SC.append(sp(P22 + "김도영_MVP", "김도영", "10월 20일 경기 뒤 · 한국아이닷컴", [bb("", "“형우 선배 앞에 주자를\n없도록 만드는 것이 주요 포인트”", 1)]))
SC.append(pv(C + "G18_디아즈_B", "디아즈", "변수 · 1·2차전 대구", [vstamp("홈 대구", 3, "gold", size=50)], team="삼성",
            stats=[st("대구 71경기", "홈런 16개", 1.5, hi=True), st("KIA전", "홈런 1개", 2.2)]))
SC.append(sp(P22 + "박진만_더그아웃", "박진만", "삼성 감독 · 10월 20일", [bb("스포츠경향 · 톱스타뉴스", "“KIA가 전반적으로 선수층이\n잘 준비되어 있다”", 0.4), bb("", "“대처할 수 있는 능력을\n충분히 갖췄다”", 4.0)], team="삼성"))   # 55
SC.append(S(0, "people", ph=420, title="KIA 선발 · 준플레이오프", items=[dict(img=C + "P17_네일_역투C", name="네일", note="7이닝 1실점", at=0.6, noteAt=0.6), dict(img=C + "P18_올러_투구", name="올러", note="6이닝 2실점", at=1.2, noteAt=1.2), dict(img=C + "FA9_시라카와_투구", name="시라카와", note="5이닝 1실점", at=2.0, noteAt=2.0)]))   # 56
SC.append(pv(NAIL, "네일", "KIA 1차전 선발 예상", [vstamp("공식 발표 전", 0.2, "bad", size=42)], stats=[st("1차전", "네일", 1.0, hi=True), st("2차전", "올러", 1.4)], chain="n51"))   # 57
SC.append(pv(NAIL, "네일", "KIA 1차전 선발 예상", [vstamp("공식 발표 전", -1, "bad", size=42)], stats=[st("10월 18~24일", "7일 휴식", 0.2, hi=True), st("올해 삼성전 · 4경기", "평균자책점 3.24", 1.0)], chain="n51", cont=True))   # 58
SC.append(pv(P22 + "후라도_청백전", "후라도", "삼성 1차전 선발 예상", [vstamp("공식 발표 전", 0.2, "bad", size=42)], team="삼성", stats=[st("삼성 선발", "4명", 1.0), st("순서", "당일 컨디션", 2.4, hi=True)], chain="hur"))   # 59
SC.append(pv(P22 + "후라도_청백전", "후라도", "삼성 1차전 선발 예상", [vstamp("공식 발표 전", -1, "bad", size=42)], team="삼성", stats=[st("19일 청백전 · 90구", "5이닝 1실점", 0.4), st("올해 KIA전 · 1경기", "7이닝 3실점", 2.4, hi=True)], chain="hur", cont=True))   # 60
SC.append(pv(P22 + "페덱_투구", "페덱", "삼성 2차전 선발 예상", [vstamp("제 예상", 4.0, "gold", size=44)], team="삼성", stats=[st("19일 청백전", "4이닝 무실점", 0.2), st("올해 KIA전 · 2경기", "2패 · 평균자책점 5.25", 2.4, hi=True)]))   # 61
SC.append(pv(P22 + "구자욱_세리머니전신", "구자욱", "변수 · 삼성 외야수", [], team="삼성", stats=[st("타율", "3할 7푼 1리 · 타격왕", 0.8), st("9월 30일", "햄스트링 힘줄 부상", 2.0, hi=True)], chain="k"))   # 62
SC.append(pv(P22 + "구자욱_세리머니전신", "구자욱", "변수 · 삼성 외야수", [], team="삼성", stats=[st("19일 청백전 · 지명타자", "안타 하나 · 볼넷 하나", 0.4), st("수비", "아직", 2.2, hi=True)], chain="k", cont=True))   # 63
SC.append(pv(P22 + "구자욱_세리머니전신", "구자욱", "변수 · 삼성 외야수", [vstamp("제 예상 · 1차전 지명타자", 2.4, "gold", size=44)], team="삼성",
             stats=[st("박진만 감독", "지명타자 선발이 최상", 0.4), st("최종 결정", "다음 청백전 뒤", 4.0)], chain="k", cont=True))         # 64
SC.append(pv(C + "P18_전상현_역투", "전상현", "KIA 마무리", [], stats=[st("준플레이오프 1·2차전", "무실점", 0.6), st("세이브", "2개", 1.6, hi=True)]))   # 65
SC.append(pv(None, "KIA 타이거즈", "준플레이오프 3경기", [dict(type="duo", items=[dict(k="득점", v="24점", c="good", at=0.6), dict(k="실점", v="5점", at=1.2)]), vstamp("가장 좋을 때 대구로", 3, "gold", size=50)]))   # 10/21 추가
SC.append(S(0, "matchup", left="KIA", right="삼성", score="4승 1패", tag="2024년 한국시리즈", text="KIA 우승 · 2년 만의 재대결", size=80))   # 66
SC.append(sp(P22 + "이범호_기자회견", "이범호", "KIA 감독 · 10월 20일 경기 뒤", [bb("스포츠경향 · 뉴스핌", "“삼성은 우리보다 강팀,\n우리는 도전자 입장”", 0.6), bb("", "“두려울 것은 없다”", 3.0)]))   # 67
SC.append(S(0, "duel", title="제 예상 · 플레이오프 1차전 KIA", left={"img": C + "P17_네일_투구", "name": "네일", "team": "KIA", "role": "7일 휴식", "at": 0.4},
            right={"img": C + "P20_후라도_투구", "name": "후라도", "team": "삼성", "role": "19일 청백전 5이닝", "at": 1.6}, vsAt=1.0))   # 68
PO = [g5(n="1차전", venue="대구", home="삼성", win="KIA", at=1.0), g5(n="2차전", venue="대구", home="삼성", win="삼성", at=1.25), g5(n="3차전", venue="광주", home="KIA", win="KIA", at=1.5),
      g5(n="4차전", venue="광주", home="KIA", win="KIA", at=1.75), g5(n="5차전", venue="대구", home="삼성", at=0)]   # 10/21 사용자 "3승 1패로 예측했는데 원 안에 구단 로고가 없네" — 망상회 v17 예측(1·3·4차전 KIA, 2차전 삼성)
SC.append(S(0, "series5", tc={"삼성": SSB}, title="플레이오프 · 5전 3선승제", games=PO, pills=[dict(label="망상회 예측 · KIA 3승 1패", at=0.4, c=KIAC), dict(label="시작 · 25일 대구", at=2.0, c="#12161F")]))   # 69
SC.append(S(0, "people", ph=420, title="정리", items=[dict(img=P22 + "박정우_적시타", name="왼손 7명", note="카라스코 공략", at=0.2, noteAt=0.2), dict(img=P22 + "나성범_6회홈런", name="나성범", note="3차전 홈런 2개", at=0.6, noteAt=0.6),
            dict(img=P22 + "시라카와_투구", name="시라카와", note="5이닝 1실점", at=1.0, noteAt=1.0), dict(img=NAIL, name="네일", note="1차전 예상 선발", at=2.4, noteAt=2.4)]))   # 70
SC.append(S(0, "question", text="플레이오프\n어느 팀이 올라갈까?", logos=["KIA", "삼성"], logoSize=230, size=110))                    # 71

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
_AC = 0
for j in range(1, len(SC)):
    A, Bq = SC[j - 1], SC[j]
    if A['type'] == Bq['type'] == 'pstat' and A.get('img') == Bq.get('img') and A.get('team') == Bq.get('team') and A.get('name') == Bq.get('name'):
        if not A.get('chain'): _AC += 1; A['chain'] = 'auto%d' % _AC
        if Bq.get('chain') != A['chain']: Bq['chain'] = A['chain']; Bq['cont'] = True
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "3차전 흐름", "title": "준플레이오프 3차전 · 13대1", "from": 4, "to": 23},
      {"key": "3차전의 의미", "title": "3차전의 의미", "from": 24, "to": 34},
      {"key": "승부를 가른 이유", "title": "승부를 가른 이유", "from": 35, "to": 48},
      {"key": "플레이오프 1차전", "title": "플레이오프 1차전 예상", "from": 49, "to": 76}]

TAGS = ["준플레이오프 3차전", "기아 엘지", "KIA LG", "김도영 만루홈런", "김도영", "나성범", "시라카와", "카라스코", "준플레이오프", "플레이오프", "KIA 삼성",
        "플레이오프 1차전", "네일", "후라도", "구자욱", "잠실야구장 마지막 경기", "케네디", "페덱", "카스트로", "올러", "우즈", "박진만", "이범호", "염경엽", "전상현", "박해민", "기아 타이거즈", "삼성 라이온즈", "LG 트윈스", "프로야구", "KBO", "야구자판기"]
DESC = ("기아(KIA)가 10월 20일 잠실 준플레이오프 3차전에서 LG를 13대1로 꺾고 3연승으로 플레이오프에 올랐어요. 해태 시절을 포함해 구단 첫 준플레이오프 통과이고, 이 경기는 잠실야구장의 마지막 프로야구 경기가 됐어요.\n\n"
        "2회초 나성범의 솔로 홈런(결승타)으로 시작해 박정우·박재현의 적시타, 김도영의 비거리 145m 만루 홈런으로 2회에만 7점을 냈어요. 시라카와는 5이닝 1실점 삼진 9개로 포스트시즌 첫 승을 거뒀어요.\n\n"
        "김도영은 준플레이오프 3경기에서 안타 3개를 모두 홈런으로 치고 8타점, 준플레이오프 MVP에 뽑혔어요. 23살 18일로 포스트시즌 최연소 만루 홈런 기록도 세웠어요.\n\n승부를 가른 이유 세 가지: ① 왼손 타자 7명 — 카라스코 체인지업 애니메이션으로 설명 ② 나성범 홈런 2개 ③ 볼넷 없는 시라카와\n\n"
        "플레이오프 1차전(10월 25일 대구) 예상: KIA 네일 vs 삼성 후라도(공식 선발 발표 전 · 채널 예상), 변수는 구자욱의 지명타자 출전. 제 예상은 1차전 KIA예요.\n\n"
        "여러분은 플레이오프, 어느 팀이 올라갈 거라고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록: KBO 게임센터 박스스코어·기록실(10월 20일 조회). 분석: 야구공작소 카라스코 스카우팅 리포트. 기사: 한국아이닷컴·일간스포츠·머니투데이·OSEN·스포츠경향·스포티비·파이낸셜뉴스·국민일보·연합뉴스·뉴스핌·톱스타뉴스·스포츠월드·서울신문·세계일보·뉴스1·아이뉴스24·스페셜타임스·MHN·뉴시스·MK스포츠·오마이스타(10/20 전후)\n"
        "사진: 연합뉴스, 일간스포츠, 머니투데이, KIA 타이거즈 제공, LG 트윈스 제공, 삼성 라이온즈 제공 · 그 밖의 선수 카드는 구단 제공·언론사 경기 사진")
SOURCE = "사실 출처 = 프로젝트 claude/1020-롱폼22-준PO3리뷰-PO1-팩트체크.md (KBO 박스스코어 + 기사 본문, 검수 에이전트 주장 75개 대조)."

EP = {"introChapter": "오프닝", "date": "2026-10-20", "gameDate": "2026-10-20", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.25, "ttsTempoSlow": 1.2,
      "rev": "1020-long22-v1", "topic": "준PO3리뷰", "endcardSec": 10, "totalSec": 481.5, "gapScale": 1.0, "pauseMax": 0.5, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼22_준PO3.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "준플레이오프 3차전 기아 13대1, 해태 포함 첫 통과 | 김도영 145m 만루포 · 카라스코가 왼손에 약한 이유 · 플레이오프 1차전 예상 #기아 #김도영",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#기아타이거즈", "#김도영", "#준플레이오프", "#플레이오프", "#나성범", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    NI = lambda i: i + (5 if i >= 55 else 0) + (1 if i >= 66 else 0)   # 10/21: 54번 뒤 5줄, 65번 뒤 1줄 추가 → 옛 번호를 새 번호로
    SLOW = {NI(i) for i in (0, 12, 13, 28, 36, 41, 48, 68, 70)} | {56, 57}
    # 10/21 사용자: '왼손 타자 상대 / 2할' 로 끊어 읽기(타자와 상대 사이에서 끊기지 않게 붙여 씀)
    EP['lines'][36]['narr'] = EP['lines'][36]['narr'].replace('타자 상대 /', '타자상대 /')
    HOLD = {0: 0.35, 2: 0.35, 3: 0.6, 6: 0.45, 7: 0.4, 8: 0.4, 9: 0.45, 11: 0.5, 15: 0.5, 18: 0.45, 21: 0.45, 22: 0.45, 23: 0.7, 24: 0.45, 26: 0.5, 29: 0.5, 32: 0.45, 34: 0.7, 35: 0.45,
            41: 0.45, 42: 0.55, 44: 0.55, 47: 0.5, 48: 0.7, 49: 0.45, 52: 0.45, 54: 0.45, 55: 0.5, 58: 0.5, 61: 0.55, 64: 0.5, 65: 0.45, 67: 0.55, 69: 0.55, 70: 0.6}   # 10/21 검수: 이야기가 바뀌는 자리마다 쉼
    # 10/21: 47번 뒤에 줄 하나 넣음 → 옛 음성(47~71번)을 새 번호(48~72번)로 옮김(재합성 없음)
    _old = {NI(i): i for i in range(len(EP['lines']) - 6)}   # 지금 PC 에 있는 음성 번호(47번 추가 반영된 상태) → 새 번호
    EP['voiceRemap'] = [_old.get(i) for i in range(len(EP['lines']))]
    HOLD = {NI(i): v for i, v in HOLD.items()}; HOLD.update({59: 0.5, 54: 0.45, 71: 0.5})
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-20_롱폼2.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i + 1, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
