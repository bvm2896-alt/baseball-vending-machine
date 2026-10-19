# -*- coding: utf-8 -*-
"""10/19 롱폼⑳ 「기아 우승 시나리오 — 채널 주인장의 망상」 (음성 API · 줄별 배속).
대사 = tools/text_1019_long20.py (v5, 사용자 승인). 근거 = 프로젝트 claude/1019-롱폼20-기아우승망상-대사v5.md.
우승 확률 약 17% = 이 채널 계산(득점·실점 피타고리안 1.83 + log5 + 홈 ±2%p)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1019_long20.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]

SCORE = {'5대2': '오 대 이', '6대3': '육 대 삼', '4대2': '사 대 이', '4대1': '사 대 일', '7대5': '칠 대 오', '3대1': '삼 대 일',
         '8대6': '팔 대 육', '5대2.': '오 대 이.', '4대3': '사 대 삼', '6대3 /': '육 대 삼 /', '8대3': '팔 대 삼'}
ORD = ['첫', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열', '열한', '열두']
def pre(t):
    t = re.sub(r'망상 (\d+)경기', lambda m: f'망상 {ORD[int(m.group(1)) - 1]} 번째 경기', t)
    for a, b in sorted(SCORE.items(), key=lambda x: -len(x[0])): t = t.replace(a, b)
    for a, b in (('92%', '구십이 퍼센트'), ('46%', '사십육 퍼센트'), ('40%', '사십 퍼센트'), ('57%', '오십칠 퍼센트'), ('48%', '사십팔 퍼센트'), ('17%', '십칠 퍼센트'),
                 ('6번 중 1번', '여섯 번 중 한 번'), ('3·4·5차전', '삼 사 오 차전'), ('31과 3분의 1이닝', '삼십일과 삼분의 일 이닝'),
                 ('플러스 105', '플러스 백오'), ('마이너스 3', '마이너스 삼'), ('0승 2패', '영승 이패'), ('9월 4일부터 6일까지', '구월 사일부터 육일까지'),
                 ('9월 30일', '구월 삼십일'), ('15일부터', '십오일부터'), ('7월 말', '칠월 말'), ('9월 이후', '구월 이후'), ('9회.', '구회.'),
                 ('1992년', '천구백구십이 년'), ('2001년', '이천일 년'), ('2015년', '이천십오 년'), ('10경기', '열 경기'), ('6경기', '여섯 경기'), ('18경기', '열여덟 경기'),
                 ('90승', '구십 승'), ('20번', '스무 번'), ('34개', '서른네 개'), ('53개', '쉰세 개'), ('54개', '쉰네 개'), ('6개', '여섯 개'), ('2개', '두 개'),
                 ('174개', '백칠십사 개'), ('121개', '백이십일 개'), ('180개', '백팔십 개'), ('55이닝', '오십오 이닝'), ('39이닝', '삼십구 이닝'),
                 ('7이닝 1실점', '칠 이닝 일 실점'), ('6이닝 9삼진', '육 이닝 아홉 삼진'), ('5승 1패', '오승 일패'), ('4승 무패', '사승 무패'),
                 ('4선발', '사 선발'), ('3패', '삼 패')):
        t = t.replace(a, b)
    return t
def narr_of(t):
    t = narr_of15(pre(t))
    t = re.sub(r'(일|이|삼|사|오|육|칠|팔|구|십) (연승|연패|차전)', r'\1\2', t)
    return re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝)(?![가-힣]*차전)', r'\1\2', t)
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
RED, GOLD, GRAY, GREEN, NAVY = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55", "#3B4A63"
KIAC, LGB, SSB, KTK = "#C70125", "#2563EB", "#074CA1", "#12161F"
TC = {"LG": LGB, "삼성": SSB, "KT": KTK}
C = '카드/'
IMG = {   # 10/19: PC 사진 폴더 확인 뒤 확정(없는 사람은 KBO 프로필)
    "네일": C + "P17_네일_역투C", "올러": C + "P18_올러_투구", "양현종": "누끼/경기_양현종_글러브_1012_KIA제공", "시라카와": C + "P18_시라카와_투구B",
    "카라스코": C + "P18_카라스코_투구", "후라도": "경기/후라도_경기_1019_삼성제공", "페덱": "누끼/경기_페덱", "원태인": "누끼/경기_원태인_투구_0828_삼성제공",
    "구자욱": "누끼/경기_구자욱_세리머니_0827_삼성제공", "대니엘": "경기/대니엘_주먹_KT제공", "고영표": "누끼/경기_고영표_상체_1011_KT제공",
    "소형준": "누끼/경기_소형준_투구_1012_KT제공_center", "로건": "경기/로건_경기_1019_KT제공", "김도영": C + "P17_김도영_질주"}
TEAM = {"네일": "KIA", "올러": "KIA", "양현종": "KIA", "시라카와": "KIA", "김도영": "KIA", "카라스코": "LG", "후라도": "삼성", "페덱": "삼성", "원태인": "삼성", "구자욱": "삼성",
        "대니엘": "KT", "고영표": "KT", "소형준": "KT", "로건": "KT"}
def pv(name, sub, viz=None, stats=None, **k): return S(0, "pstat", img=IMG[name], name=name, team=TEAM[name], sub=sub, stats=stats or [], viz=viz or [], noCenter=True, **k)
def duel(title, a, b, ra, rb, **k):
    return S(0, "duel", title=title, left={"img": IMG[a], "name": a, "team": TEAM[a], "role": ra, "at": 0}, right={"img": IMG[b], "name": b, "team": TEAM[b], "role": rb, "at": 0.5}, vsAt=0.3, **k)
def fo(title, a, b, rows, **k):
    return S(0, "faceoff", title=title, tc=TC, left={"img": IMG.get(a), "name": a, "team": TEAM.get(a, a)}, right={"img": IMG.get(b), "name": b, "team": TEAM.get(b, b)},
             leftColor=KIAC if TEAM.get(a, a) == "KIA" else TC.get(TEAM.get(a, a), NAVY), rightColor=KIAC if TEAM.get(b, b) == "KIA" else TC.get(TEAM.get(b, b), NAVY), pw=300, rows=rows, **k)
def row(k, l, r, lv, rv, at=0, low=False, w=None): return dict(k=k, l=l, r=r, lv=lv, rv=rv, at=at, low=low, **({"w": w} if w else {}))
def mang(n, left, right, score, game, venue, text=None):
    return S(0, "matchup", left=left, right=right, score=score, tag=f"망상 {n}경기 · {game} · {venue} · 망상 스코어", **({"text": text, "size": 84} if text else {}))
def g(n, venue, home, win=None, at=0, **k): return dict(n=n, venue=venue, home=home, **({"win": win} if win else {}), at=at, **k)
PH = "상황별/"

SC = []
# ── 오프닝 ──
SC.append(S(0, "photo", img=PH + "망상경고_롱폼20", fit="cover", text="", h=760))                                       # 0
SC.append(S(0, "photo", img=PH + "망상포스터_롱폼20", fit="cover", text="", h=760))                                     # 1
YRS = [("1992", "롯데"), ("2001", "두산"), ("2015", "두산")]
SC.append(S(0, "big", text="준플레이오프부터 올라와\n한국시리즈 우승\n역대 세 번뿐", size=100))                   # 2
SC.append(S(0, "steps", title="준플레이오프부터 올라와 우승", items=[dict(date=y, text=t, at=0.1 + k * 0.6, hi=True) for k, (y, t) in enumerate(YRS)]))   # 3
SC.append(S(0, "big", team="KIA", text="그런데\n계산해 보니…", size=120))                                                 # 4
SC.append(S(0, "bars", term="기대 승률", title="2026 정규시즌 득점·실점으로 계산 · 피타고리안",
            items=[dict(label="KT", team="KT", value=60.8, unit="%", dec=1, at=0.6), dict(label="삼성", team="삼성", value=58.4, unit="%", dec=1, at=0.9),
                   dict(label="KIA", team="KIA", value=56.7, unit="%", dec=1, at=1.2, hi=True), dict(label="LG", team="LG", value=49.8, unit="%", dec=1, at=1.5)], max=70))   # 5
SC.append(S(0, "bars", term="KIA 시리즈 통과 확률", title="야구자판기 계산 · 준PO는 2승 0패에서",
            items=[dict(label="준PO", team="LG", value=92, unit="%", at=0, hi=True), dict(label="PO", team="삼성", value=46, unit="%", at=0.8),
                   dict(label="KS", team="KT", value=40, unit="%", at=1.5)], max=100))                                         # 6
SC.append(S(0, "big", team="KIA", text="우승 확률 약 17%\n6번 중 1번", size=110))      # 7
SC.append(S(0, "toc", on=-1, itemFrom=1))                                                                                     # 8
SC.append(S(0, "big", text="몇 경기 맞대결 기록은\n다음 경기를 보장하지 않는다", size=88))                    # 9
SC.append(S(0, "big", text="그래서 이 망상은\n시즌 기록 + 최근 흐름", size=96))                                # 10
# ── 1막 준PO 3차전 ──
SC.append(duel("망상 1경기 · 준플레이오프 3차전 · 잠실", "시라카와", "카라스코", "KIA 선발", "LG 선발"))                    # 11
SC.append(fo("3차전 선발 · 평균자책점", "카라스코", "시라카와", [row("시즌", "4.05", "4.75", 4.05, 4.75, 0.3, True, "l")], chain="f12"))   # 12
SC.append(pv("카라스코", "LG 선발", [vstamp("막판 세 경기 평균자책점 6.28", 0.8, "bad", size=46)], [st("시즌", "평균자책점 4.05", 0)]))   # 13
SC.append(fo("팀 흐름 · KIA vs LG", "KIA", "LG", [row("시즌 마지막\n10경기", "7승 3패", "3승 7패", 7, 3, 0.6, False, "l")], chain="f14"))  # 14
SC.append(fo("팀 흐름 · KIA vs LG", "KIA", "LG", [row("시즌 마지막\n10경기", "7승 3패", "3승 7패", 7, 3, -1, False, "l"),
                                                 row("득실 차", "+105", "−3", 105, -3, 0.2, False, "l"), row("한 경기\n승리 확률", "57%", "43%", 57, 43, 2.0, False, "l")], chain="f14", cont=True))   # 15
SC.append(mang(1, "KIA", "LG", "5 : 2", "준플레이오프 3차전", "잠실", "3연승으로 끝"))                                       # 16
SER0 = [g("1차전", "광주", "KIA", "KIA"), g("2차전", "광주", "KIA", "KIA"), g("3차전", "잠실", "LG", "KIA", maybe=True, tag="망상"), g("4차전", "잠실", "LG", off=True), g("5차전", "광주", "KIA", off=True)]
SC.append(S(0, "series5", tc=TC, title="준플레이오프 · 망상 3연승", games=SER0, pills=[dict(label="며칠 쉬고 플레이오프로", at=0.8, c=KIAC)]))   # 17
# ── 2막 PO 삼성 ──
SERP = lambda wins, **k: S(0, "series5", tc=TC, title="플레이오프 · 망상", games=[g(f"{i+1}차전", v, h, (wins[i] if i < len(wins) else None), maybe=bool(i < len(wins)), at=0.3 if i == len(wins) - 1 else 0)
                                                                              for i, (v, h) in enumerate([("대구", "삼성"), ("대구", "삼성"), ("광주", "KIA"), ("광주", "KIA"), ("대구", "삼성")])], chain="sp", **k)
SC.append(SERP([], pills=[dict(label="한 경기 승률 KIA 48%", at=0.8, c=KIAC)]))                                               # 18
SC.append(fo("팀 흐름 · 시즌 마지막 10경기", "KIA", "삼성", [row("마지막\n10경기", "7승 3패", "4승 6패", 7, 4, 0.6, False, "l")], text="삼성 · 4연패로 시즌 끝", textAt=1.8))   # 19
SC.append(duel("망상 2경기 · 플레이오프 1차전 · 대구", "네일", "후라도", "KIA 선발", "삼성 선발"))                          # 20
SC.append(fo("1차전 선발 · 평균자책점", "네일", "후라도", [row("시즌", "3.49", "3.54", 3.49, 3.54, 0.4, True)], chain="f21"))  # 21
SC.append(fo("1차전 선발 · 평균자책점", "네일", "후라도", [row("시즌", "3.49", "3.54", 3.49, 3.54, -1, True), row("9월 이후", "2.76", "4.60", 2.76, 4.60, 0.6, True, "l")], chain="f21", cont=True))   # 22
SC.append(pv("네일", "KIA 선발", [vstamp("준PO 1차전 7이닝 1실점 승", 0.6, "gold", size=46)], [st("9월 이후", "평균자책점 2.76", 0.2)]))   # 23
SC.append(pv("김도영", "KIA 3루수 · 홈런왕", [], [st("9월 이후", "타율 .343", 0.4), st("9월 이후", "홈런 6개", 1.4), st("준PO 1차전", "홈런 2개", 2.4, hi=True)]))   # 24
SC.append(mang(2, "KIA", "삼성", "6 : 3", "플레이오프 1차전", "대구", "김도영 결승 투런"))                                 # 25
SC.append(duel("망상 3경기 · 플레이오프 2차전 · 대구", "양현종", "페덱", "KIA 선발", "삼성 선발"))                          # 26
SC.append(pv("페덱", "삼성 선발", [], [st("평균자책점", "2.95", 0.2, hi=True), st("이닝당 출루 허용", "0.96", 1.4)]))         # 27
SC.append(pv("양현종", "KIA 선발", [], [st("퀄리티스타트", "2번", 0.6, hi=True)]))                                           # 28
SC.append(mang(3, "KIA", "삼성", "2 : 4", "플레이오프 2차전", "대구", "1승 1패"))                                           # 29
SC.append(duel("망상 4경기 · 플레이오프 3차전 · 광주", "올러", "원태인", "KIA 선발", "삼성 선발", text="KIA가 가장 유리한 경기", textAt=2.6))   # 30
SC.append(pv("올러", "KIA 선발", [], [st("피안타율", ".204", 0.2), st("삼진", "180개", 1.0), st("광주 18경기", "평균자책점 2.28", 1.8, hi=True)]))   # 31
SC.append(pv("원태인", "삼성 선발", [vstamp("9월 이후 0승", 1.0, "bad", size=50)], [st("9월 이후 6경기", "3패", 0.2), st("평균자책점", "5.23", 1.6, hi=True)]))   # 32
SC.append(mang(4, "KIA", "삼성", "4 : 1", "플레이오프 3차전", "광주", "2승 1패"))                                           # 33
SC.append(S(0, "big", team="KIA", text="망상 5경기\n플레이오프 4차전 · 광주\n양 팀 4선발", size=84))                       # 34
SC.append(S(0, "bars", term="팀 홈런", title="2026 정규시즌", items=[dict(label="KIA", team="KIA", value=174, unit="개", at=0.4, hi=True), dict(label="삼성", team="삼성", value=140, unit="개", at=0.8)], max=180))   # 35
SC.append(pv("구자욱", "삼성 · 변수", [], [st("9월 30일", "햄스트링 부상", 0.4, hi=True), st("10월 15일", "타격 훈련 시작", 1.8)]))   # 36
SC.append(SERP(["KIA", "삼성", "KIA", "KIA"], text="망상 스코어 7 : 5 · 3승 1패", size=60, textAt=0.6))                                 # 37
# ── 3막 KS KT ──
SERK = lambda wins, **k: S(0, "series5", tc=TC, sw=250, title="한국시리즈 · 망상", games=[g(f"{i+1}차전", v, h, (wins[i] if i < len(wins) else None), maybe=bool(i < len(wins)), at=0.3 if i == len(wins) - 1 else 0)
                                                                                     for i, (v, h) in enumerate([("수원", "KT")] * 2 + [("광주", "KIA")] * 3 + [("수원", "KT")] * 2)], chain="sk", **k)
SC.append(S(0, "big", team="KT", text="정규시즌 90승\nKT", size=120))                                                        # 38
SC.append(SERK([], pills=[dict(label="한 경기 46% · 시리즈 40%", at=0.6, c=KIAC)]))                                         # 39
SC.append(S(0, "big", team="KT", text="10연승으로\n시즌 끝", size=110))                                                     # 40
SC.append(pv("대니엘", "KT 선발 · 9월 이후 평균자책점", [vtrend([dict(x="대니엘", v=1.85, vt="1.85", c="bad", at=0.4), dict(x="고영표", v=2.30, vt="2.30", c="bad", at=0.9), dict(x="소형준", v=2.57, vt="2.57", c="bad", at=1.4)], max=4)]))   # 41
SC.append(duel("망상 6경기 · 한국시리즈 1차전 · 수원", "네일", "대니엘", "KIA 선발", "KT 선발"))                            # 42
SC.append(pv("대니엘", "KT 선발", [], [st("9월 이후", "39 이닝", 0.2), st("삼진", "54개", 1.2, hi=True)]))                      # 43
SC.append(duel("망상 7경기 · 한국시리즈 2차전 · 수원", "양현종", "고영표", "KIA 선발", "KT 선발"))                          # 44
SC.append(SERK(["KT", "KT"], text="고영표 9월 이후 5승 1패 · 0승 2패", size=56, textAt=0.4))                                           # 45
SC.append(S(0, "big", team="KIA", text="여기서 끝?\n망상은 지금부터", size=120))                                             # 46
_s47 = SERK(["KT", "KT"], text="3·4·5차전은 KIA 홈 광주", size=60, textAt=0.2, cont=True)
for _i in (2, 3, 4): _s47["games"][_i].update(glow="KIA", glowAt=0.3)
SC.append(_s47)                                            # 47
_GS = [("9/4", "K"), ("9/5", "K"), ("9/6", "K")]
SC.append(S(0, "matchup", left="KIA", right="KT", score="3 : 0", tag="9월 4~6일 · 광주 3연전 · 망상의 양념", chain="m48"))     # 48
SC.append(S(0, "matchup", left="KIA", right="KT", score="3 : 0", tag="9월 4~6일 · 광주 3연전 · 망상의 양념", text="4:3 · 6:3 · 8:3", size=96, chain="m48"))   # 49
SC.append(duel("망상 8경기 · 한국시리즈 3차전 · 광주", "올러", "소형준", "KIA 선발", "KT 선발"))                            # 50
SC.append(pv("올러", "KIA 선발 · 상대 소형준 9월 이후 4승 무패", [], [st("광주 18경기", "평균자책점 2.28", 1.4, hi=True), st("준PO 2차전", "6이닝 9삼진", 3.2)]))   # 51
SC.append(mang(8, "KIA", "KT", "3 : 1", "한국시리즈 3차전", "광주", "1승 2패"))                                             # 52
SC.append(duel("망상 9경기 · 한국시리즈 4차전 · 광주", "시라카와", "로건", "KIA 선발", "KT 선발"))                          # 53
SC.append(pv("로건", "KT 선발", [vstamp("9월 이후 피홈런 6개", 1.2, "bad", size=48)], [st("9월 이후", "31⅓이닝", 0.2)]))       # 54
SC.append(S(0, "bars", term="팀 홈런", title="2026 정규시즌", items=[dict(label="KIA", team="KIA", value=174, unit="개", at=0.6, hi=True), dict(label="KT", team="KT", value=121, unit="개", at=1.0)], max=180, text="53개 차이", textAt=2.0))   # 55
SC.append(mang(9, "KIA", "KT", "8 : 6", "한국시리즈 4차전", "광주", "2승 2패"))                                             # 56
SC.append(duel("망상 10경기 · 한국시리즈 5차전 · 광주", "네일", "대니엘", "KIA 선발", "KT 선발"))                           # 57
SC.append(pv("대니엘", "KT 선발 · 7월 말 합류", [], [st("한국 무대", "55 이닝", 0.6, hi=True)]))                                # 58
SC.append(pv("네일", "KIA 선발", [], [st("9월 이후", "평균자책점 2.76", 1.6), st("퀄리티스타트", "20번", 2.6, hi=True)]))         # 59
SC.append(mang(10, "KIA", "KT", "4 : 2", "한국시리즈 5차전", "광주", "3승 2패"))                                             # 60
SC.append(duel("망상 11경기 · 한국시리즈 6차전 · 수원", "양현종", "고영표", "KIA 선발", "KT 선발"))                          # 61
SC.append(mang(11, "KIA", "KT", "2 : 5", "한국시리즈 6차전", "수원", "3승 3패"))                                             # 62
SC.append(duel("망상 12경기 · 한국시리즈 7차전 · 수원", "올러", "소형준", "KIA 선발", "KT 선발"))                           # 63
SC.append(fo("7차전 선발 · 평균자책점", "올러", "소형준", [row("시즌", "3.13", "3.15", 3.13, 3.15, 0.3, True)]))                # 64
SC.append(S(0, "big", team="KIA", text="이런 경기는\n한 방이 끝낸다", size=110))                                              # 65
SC.append(S(0, "photo", img="경기/김도영_4회홈런_1017_KIA제공", fit="cover", text="9회 역전 투런\n망상 스코어 4 : 3", size=96, h=560))   # 66
SC.append(SERK(["KT", "KT", "KIA", "KIA", "KIA", "KT", "KIA"], text="망상 한국시리즈 우승 · 4승 3패", size=72, textAt=1.0))                        # 67
SC.append(S(0, "steps", title="망상 정리", items=[dict(date="준플레이오프", text="3연승", at=0.2), dict(date="플레이오프", text="3승 1패", at=0.8), dict(date="한국시리즈", text="0승 2패 → 4승 3패", at=1.6, hi=True)]))   # 68
SC.append(S(0, "big", team="KIA", text="우승 확률 약 17%\n6번 중 1번", size=110))                 # 69
SC.append(S(0, "photo", img=PH + "망상경고_롱폼20", fit="cover", text="", h=760))                                         # 70
SC.append(S(0, "question", text="KIA 우승 망상\n몇 퍼센트쯤\n현실이 될까요?", logos=["KIA"], size=96))                       # 71

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "준플레이오프 3차전", "title": "1막 · 준플레이오프 3차전", "from": 11, "to": 17},
      {"key": "플레이오프 삼성", "title": "2막 · 플레이오프 삼성", "from": 18, "to": 37},
      {"key": "한국시리즈 KT", "title": "3막 · 한국시리즈 KT", "from": 38, "to": 67},
      {"key": "망상 결말", "title": "결말 · 우승 확률 17%", "from": 68, "to": 71}]

TAGS = ["KIA 우승", "기아 우승", "KIA 타이거즈", "기아타이거즈", "한국시리즈", "2026 한국시리즈", "플레이오프", "준플레이오프", "가을야구", "KIA 한국시리즈",
        "김도영", "네일", "올러", "양현종", "시라카와", "삼성 라이온즈", "KT 위즈", "LG 트윈스", "후라도", "대니엘", "고영표", "소형준", "프로야구", "KBO", "야구자판기"]
DESC = ("이 영상은 채널 주인장의 망상이에요. 그런데 숫자로 계산해 보니 KIA 타이거즈의 2026 한국시리즈 우승 확률은 약 17%, 6번 중 1번이었어요.\n\n"
        "올해 정규시즌 득점과 실점으로 팀마다 기대 승률을 구하고(피타고리안), 경기마다 승리 확률을 계산했어요. KIA의 통과 확률은 준플레이오프(2승 0패에서) 92%, 플레이오프 46%, 한국시리즈 40%예요.\n\n"
        "그 한 번이 어떻게 오는지, 선발 투수의 시즌 기록과 9월 이후 흐름으로 경기별 망상을 짰어요. 준플레이오프 3연승 → 플레이오프 삼성 3승 1패 → 한국시리즈 KT 0승 2패에서 4승 3패.\n\n"
        "※ 망상 스코어는 지어낸 점수예요. 몇 경기 맞대결 기록은 다음 경기를 보장하지 않아 시즌 전체 기록과 최근 흐름을 근거로 썼어요. 우승 확률은 이 채널이 직접 계산한 추정치로, 홈 이점 가정에 따라 조금 달라질 수 있어요.\n\n"
        "여러분이 보기엔 KIA 우승 망상, 몇 퍼센트쯤 현실이 될 것 같나요? 댓글로 알려 주세요.\n\n"
        "기록: KBO 기록실(2026 정규시즌 팀·선수 기록, 월별·경기별 기록, 경기 일정·결과). 역대 기록: 데일리안, 디지털타임스. 부상: 머니투데이. 포스트시즌 방식: 머니투데이 [오피셜]. 준PO 2차전: 서울신문\n"
        "사진: KIA 타이거즈 제공, 삼성 라이온즈 제공, KT 위즈 제공, LG 트윈스 제공, 스포츠조선, 각 구단 공식 프로필")
SOURCE = "사실 출처 = KBO 기록실 직접 조회(10/19) + 기사 — 프로젝트 claude/1019-롱폼20-기아우승망상-대사v5.md. 우승 확률 = 채널 계산."

EP = {"date": "2026-10-19", "gameDate": "2026-10-19", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.25, "ttsTempoSlow": 1.2,
      "rev": "1019-long20-v1", "topic": "기아우승망상", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼20_기아우승망상.jpg", "source": SOURCE,
      "youtube": {"title": "기아 우승 시나리오 | 망상인 줄 알았는데 계산하니 17%, 삼성·KT 넘는 12경기 #KIA #한국시리즈",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#KIA타이거즈", "#한국시리즈", "#가을야구", "#김도영", "#플레이오프", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 7, 69, 71}
    HOLD = {0: 0.35, 3: 0.3, 7: 0.35, 10: 0.3, 16: 0.35, 25: 0.35, 29: 0.3, 33: 0.3, 37: 0.35, 45: 0.35, 46: 0.3, 52: 0.3, 56: 0.3, 60: 0.3, 62: 0.3, 66: 0.35, 67: 0.35, 69: 0.35}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-19_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    import subprocess; subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mang_fx_1019.py'), out], check=True)   # 10/19 망상 극장(망냥이·효과·어두운 톤)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
