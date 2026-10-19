# -*- coding: utf-8 -*-
"""10/19~20 롱폼⑳ 「KIA 한국시리즈 우승 망상회」 v17 확정 대사(89줄)용 콘티 (음성 API · 줄별 배속).
대사 = tools/text_1019_long20.py (자막, 나레이션). 근거 = 프로젝트 claude/1019-롱폼20-기아우승망상-대사v17-확정.md.
화면 숫자는 대사 숫자와 같게(R9), 경기 스코어 없음(사용자 10/19), 사진은 전부 경기 사진(R1), 소형준은 카드/G18_소형준_B(R5·R7)."""
import json, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1019_long20.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L = _g['L']
_spec = importlib.util.spec_from_file_location('t20', os.path.join(os.path.dirname(__file__), 'text_1019_long20.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
LINES = _t.LINES

def narr_of(n):
    n = re.sub(r'([영일이삼사오육칠팔구십]+) 점 ([영일이삼사오육칠팔구공]+)(?=[가-힣 ,]|$)', r'\1쩜\2', n)   # 10/15 사용자: 4.24 = 사쩜이사
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (연승|연패)', r'\1\2', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)
    n = n.replace('삼 점대', '삼점대')
    return n
def sub_of(t):
    for a, b in (('1, 2차전', '1·2차전'), ('3, 4, 5차전', '3·4·5차전'), ('3, 4차전', '3·4차전')): t = t.replace(a, b)
    return re.sub(r'\.(?= / )', '', t)

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
KIAC, LGB, SSB, KTK, NAVY = "#C70125", "#2563EB", "#074CA1", "#12161F", "#3B4A63"
TC = {"LG": LGB, "삼성": SSB, "KT": KTK}
C = '카드/'
IMG = {"네일": C + "P17_네일_역투C", "올러": C + "P18_올러_투구", "양현종": "누끼/경기_양현종_글러브_1012_KIA제공", "시라카와": C + "P18_시라카와_투구B",
       "카라스코": C + "P18_카라스코_투구", "후라도": C + "P20_후라도_투구", "페덱": "누끼/경기_페덱", "원태인": "누끼/경기_원태인_투구_0828_삼성제공",
       "구자욱": "누끼/경기_구자욱_세리머니_0827_삼성제공", "대니엘": "경기/대니엘_주먹_KT제공", "고영표": "누끼/경기_고영표_상체_1011_KT제공",
       "소형준": C + "G18_소형준_B", "로건": "경기/로건_경기_1019_KT제공", "김도영": C + "P17_김도영_질주",
       "박재현": C + "P18_박재현_득점", "전상현": C + "P18_전상현_역투", "손주영": C + "P18_손주영", "염경엽": C + "P18_염경엽",
       "카스트로": C + "P18_카스트로_환호", "나성범": C + "P18_나성범_적시타", "김선빈": C + "P18_김선빈_2루타", "오스틴": C + "P18_오스틴_타격",
       "디아즈": C + "FA9_디아즈_경기", "최원준": C + "G18_최원준_배트투척", "힐리어드": C + "T12_힐리어드_하이파이브"}
TEAM = {"네일": "KIA", "올러": "KIA", "양현종": "KIA", "시라카와": "KIA", "김도영": "KIA", "박재현": "KIA", "전상현": "KIA", "카스트로": "KIA", "나성범": "KIA", "김선빈": "KIA",
        "카라스코": "LG", "손주영": "LG", "염경엽": "LG", "오스틴": "LG",
        "후라도": "삼성", "페덱": "삼성", "원태인": "삼성", "구자욱": "삼성", "디아즈": "삼성",
        "대니엘": "KT", "고영표": "KT", "소형준": "KT", "로건": "KT", "최원준": "KT", "힐리어드": "KT"}
def IPV(*g): return dict(type="ip", items=[dict(d=d, ip=ip, r=r, **({"k": k} if k else {}), at=at) for d, ip, r, k, at in g])   # 10/20 이닝 칸·실점 공·삼진 K
def pv(name, sub, viz=None, stats=None, **k): return S(0, "pstat", img=IMG[name], name=name, team=TEAM[name], sub=sub, stats=stats or [], viz=viz or [], noCenter=True, **k)
def duel(title, a, b, ra, rb, **k):
    return S(0, "duel", title=title, left={"img": IMG[a], "name": a, "team": TEAM[a], "role": ra, "at": 0}, right={"img": IMG[b], "name": b, "team": TEAM[b], "role": rb, "at": 0.5}, vsAt=0.3, **k)
def fo(title, a, b, rows, **k):
    return S(0, "faceoff", title=title, tc=TC, left={"img": IMG.get(a), "name": a, "team": TEAM.get(a, a)}, right={"img": IMG.get(b), "name": b, "team": TEAM.get(b, b)},
             leftColor=KIAC if TEAM.get(a, a) == "KIA" else TC.get(TEAM.get(a, a), NAVY), rightColor=k.pop("rightColor", None) or (KIAC if TEAM.get(b, b) == "KIA" else TC.get(TEAM.get(b, b), NAVY)), pw=300, rows=rows, **k)
def row(k, l, r, lv, rv, at=0, low=False, w=None): return dict(k=k, l=l, r=r, lv=lv, rv=rv, at=at, low=low, **({"w": w} if w else {}))
def g(n, venue, home, win=None, at=0, **k): return dict(n=n, venue=venue, home=home, **({"win": win} if win else {}), at=at, **k)
def steps(title, items, **k): return S(0, "steps", title=title, items=[dict(date=d, text=t, at=a, **({"hi": True} if h else {})) for d, t, a, h in items], **k)
PH = "상황별/"

SER0 = lambda w3=None, **k: S(0, "series5", tc=TC, title="준플레이오프 · KIA vs LG", chain="s0",
    games=[g("1차전", "광주", "KIA", "KIA"), g("2차전", "광주", "KIA", "KIA"), g("3차전", "잠실", "LG", w3, maybe=bool(w3), at=0.3 if w3 else 0), g("4차전", "잠실", "LG", off=True), g("5차전", "광주", "KIA", off=True)], **k)
SERP = lambda wins, who={}, **k: S(0, "series5", tc=TC, title="플레이오프 · KIA vs 삼성 · 예측", games=[g(f"{i+1}차전", v, h, (wins[i] if i < len(wins) else None), maybe=bool(i < len(wins)), at=0.3 if i == len(wins) - 1 else 0, **({"who": who[i]} if i in who else {}))
                                                                              for i, (v, h) in enumerate([("대구", "삼성"), ("대구", "삼성"), ("광주", "KIA"), ("광주", "KIA"), ("대구", "삼성")])], chain="sp", **k)
SERK = lambda wins, **k: S(0, "series5", tc=TC, sw=250, title="한국시리즈 · KIA vs KT · 예측", games=[g(f"{i+1}차전", v, h, (wins[i] if i < len(wins) else None), maybe=bool(i < len(wins)), at=0.3 if i == len(wins) - 1 else 0)
                                                                                     for i, (v, h) in enumerate([("수원", "KT")] * 2 + [("광주", "KIA")] * 3 + [("수원", "KT")] * 2)], chain="sk", **k)
HR = lambda opp, val, **k: S(0, "bars", term="팀 홈런", title="2026 정규시즌", items=[dict(label="KIA", team="KIA", value=174, unit="개", at=0.4, hi=True), dict(label=opp, team=opp, value=val, unit="개", at=0.8)], max=180, **k)

SC = []
# ── 오프닝 ──
SC.append(S(0, "warn"))                                                                                                     # 0 L1 (카드 없이 글만 — 10/20 사용자)
SC.append(S(0, "photo", img=PH + "망상포스터_롱폼20", fit="cover", text="", h=760))                                                          # 1 L2
SC.append(steps("준플레이오프부터 올라와 우승", [("1992", "롯데", 0.6, 1), ("2001", "두산", 1.6, 1), ("2015", "두산", 2.4, 1)], chain="y3"))           # 2 L3
SC.append(S(0, "dice", title="KIA 우승 확률 · 득점과 실점으로 계산", big="약 17%", sub="6번 중 1번"))                                         # 3 L4
SC.append(S(0, "big", team="KIA", text="경기마다 변수를 따져\n가능성이 높은 쪽으로", size=96))                                              # 4 L5
SC.append(S(0, "toc", on=-1, itemSeg=[0, 1, 1.46, None]))   # 10/20 사용자: 말하는 칸에 불 — 준PO3(1호흡)·플레이오프(2호흡 시작)·한국시리즈(2호흡 46%), 정리는 말 안 하므로 안 켬                                                                                                   # 5 L6
# ── 1막 준PO 3차전 ──
SC.append(SER0(pills=[dict(label="1차전 · 김도영 홈런 2방", at=1.0, c=KIAC), dict(label="2차전 · 1회 임찬규 강판", at=2.4, c=KIAC)]))           # 6 L7
SC.append(steps("준플레이오프 3차전 · 변수 4가지", [("변수 1", "선발", 1.0, 0), ("변수 2", "불펜", 1.5, 0), ("변수 3", "김도영 견제", 2.0, 0), ("변수 4", "잠실", 3.35, 0)]))   # 7 L8
SC.append(duel("변수 1 · 선발 · 준플레이오프 3차전 · 잠실", "시라카와", "카라스코", "KIA 선발", "LG 선발", text="경험보다 공의 힘 · 데일리안 10/19", textAt=3.0))   # 8 L9
SC.append(pv("시라카와", "KIA 선발 · KBO 포스트시즌 첫 등판", [IPV(("LG전 2경기 합계", 9.333, 8, None, 1.2))], [st("LG전 평균자책점", "7.71", 1.9, hi=True)], chain="p9"))   # 9 L10
SC.append(pv("시라카와", "KIA 선발 · KBO 포스트시즌 첫 등판", [IPV(("LG전 2경기 합계", 9.333, 8, None, -1))], [st("LG전 평균자책점", "7.71", -1, hi=True),
                                                                st("LG 오스틴 상대", "4타수 3안타 · 홈런 2개", 0.4, hi=True)], chain="p9", cont=True))        # 10 L11
SC.append(pv("카라스코", "LG 선발", [IPV(("와일드카드 결정전", 6, 1, None, 3.0))], [st("메이저리그", "112승", 0.8)], chain="p11"))            # 11 L12
SC.append(pv("카라스코", "LG 선발", [IPV(("와일드카드 결정전", 6, 1, None, -1))], [st("메이저리그", "112승", -1),
                                      st("김도영 상대", "3타수 무안타", 0.3), st("나성범 상대", "2타수 무안타", 1.4)], chain="p11", cont=True))            # 12 L13
SC.append(pv("박재현", "KIA 1번 타자 · 10월 3일", [IPV(("10월 3일 카라스코", 4.333, 4, None, 0.6)), vstamp("그날 안타 2개", 2.4, "gold", size=50)], []))   # 13 L14
SC.append(S(0, "big", text="두 선발 모두 초반에 흔들\n승부는 불펜에서", size=100))                                                       # 14 L15
SC.append(steps("변수 2 · KIA 불펜", [("긴 이닝", "황동하", 1.2, 0)], chain="bp"))                                                           # 15 L16
SC.append(steps("변수 2 · KIA 불펜", [("긴 이닝", "황동하", -1, 0), ("불펜", "성영탁 · 1, 2차전 무실점", 0.4, 0), ("마무리", "전상현 · 1, 2차전 무실점", 1.4, 1)], chain="bp", cont=True))   # 16 L17
SC.append(pv("전상현", "KIA 마무리", [vstamp("매 경기 던질 수 있다", 4.6, "gold", size=50)], [st("준플레이오프 1, 2차전", "이틀 연속 아웃 4개 세이브", 0.3), st("10월 정규시즌 6경기", "피안타 0", 2.4, hi=True)]))   # 17 L18
SC.append(pv("손주영", "LG 불펜", [], [st("2차전 임찬규 강판 뒤", "불펜 1실점", 1.2), st("부상 복귀 손주영", "무실점", 2.6, hi=True)]))                # 18 L19
SC.append(S(0, "big", text="경기 후반 1점을\n짜내는 쪽이 이긴다", size=104))                                                              # 19 L20
SC.append(pv("염경엽", "LG 감독 · 변수 3 김도영 견제", [vstamp("김도영을 어떻게 잡느냐가 중요", 1.6, "gold", size=46)], [st("10월 14일", "와일드카드 승리 뒤", 0.6)]))   # 20 L21
SC.append(pv("김도영", "KIA 3번 타자 · 홈런왕", [], [st("준플레이오프 2차전", "무안타", 0.3, hi=True), st("볼넷", "1개", 1.2), st("몸에 맞는 공", "1개", 1.8)]))   # 21 L22
SC.append(pv("카스트로", "KIA 4번 타자", [], [st("2차전 1회", "결승타", 0.3, hi=True), st("5번 나성범 · 6번 김선빈 · 7번 한준수", "연달아 2루타", 1.8)]))   # 22 L23
SC.append(pv("나성범", "KIA 5번 타자", [], [st("2차전 7회", "카스트로 거른 뒤", 1.0), st("나성범", "희생플라이 1점", 2.0, hi=True)]))   # 23 L24
SC.append(S(0, "big", team="KIA", text="김도영을 피해도\n뒤에서 점수가 난다", size=104))                                                  # 24 L25
SC.append(S(0, "big", team="LG", text="변수 4 · 잠실\n담장이 멀어 홈런이 적다", size=96))                                                   # 25 L26
SC.append(steps("KIA 공격 · 두 가지 무기", [("2026 정규시즌", "팀 홈런 174개", 0.3, 0), ("준플레이오프 2차전 1회", "2루타 3개 연달아", 1.3, 1)]))   # 10/20 사용자 "김선빈 사진에 팀 홈런이 — 김선빈이 174개 친 줄" → 팀 이야기는 선수 카드에 싣지 않는다                  # 26 L27
SC.append(S(0, "big", team="LG", text="잠실 · 올 시즌 뒤 철거\nLG가 지면 마지막 경기", size=92))                                            # 27 L28
SC.append(S(0, "photo", img=IMG["염경엽"], fit="cover", text="LG · 어느 때보다 절박", size=84, h=560))                                     # 28 L29
SC.append(pv("오스틴", "LG 타자", [], [st("준플레이오프 2경기", "7타수 1안타", 1.0, hi=True), st("LG 정규시즌 마지막 10경기", "3승 7패", 3.0)]))          # 29 L30
SC.append(SER0("KIA", pills=[dict(label="예측 · KIA 3연승", at=0.6, c=KIAC), dict(label="결승타 · 카스트로 또는 나성범", at=3.0, c=KIAC)], cont=True))   # 30 L31
SC.append(steps("KIA(해태 포함) 준플레이오프", [("1994", "탈락", 0.6, 0), ("2004", "탈락", 1.0, 0), ("2006", "탈락", 1.4, 0), ("2011", "탈락", 1.8, 0)]))   # 31 L32
# ── 2막 PO 삼성 ──
SC.append(SERP([], who={0: dict(img=IMG["네일"], name="네일", at=1.25, w=219, l=-31, t=-4), 1: dict(img=IMG["양현종"], name="양현종", at=2.2, w=350, l=-85, t=0), 2: dict(img=IMG["올러"], name="올러", at=3.3, w=543, l=-241, t=-34)}))   # 10/20 사용자: 말하는 순간 원 안에 선발 얼굴                                          # 32 L33
SC.append(pv("양현종", "KIA 선발", [], [st("준플레이오프", "등판 없음", 0.4), st("휴식", "열흘 넘게", 1.4, hi=True)], chain="p33"))              # 33 L34
SC.append(SERP([], pills=[dict(label="플레이오프 통과 확률 · 약 46%", at=1.0, c=KIAC)], text="거의 반반", size=64, textAt=2.6))               # 34 L35
SC.append(fo("올 시즌 맞대결 · KIA vs 삼성", "KIA", "삼성", [row("시즌", "9승 7패", "7승 9패", 9, 7, 0.4, False, "l"), row("광주", "5승 4패", "4승 5패", 5, 4, 1.6, False, "l"),
                                                          row("대구", "4승 3패", "3승 4패", 4, 3, 2.4, False, "l")]))                                       # 35 L36
SC.append(steps("플레이오프 · 변수 6가지", [("변수 1", "휴식", 1.0, 0), ("변수 2", "구자욱", 1.45, 0), ("변수 3", "1차전 선발", 2.0, 0), ("변수 4", "2차전 페덱", 2.5, 0),
                                       ("변수 5", "3차전 올러", 3.0, 0), ("변수 6", "장타", 3.6, 0)]))                                                         # 36 L37
SC.append(S(0, "big", team="삼성", text="변수 1 · 휴식\n삼성 · 2주 가까이 실전 없음", size=92))                                             # 37 L38
SC.append(fo("팀 흐름 · 정규시즌 마지막 10경기", "KIA", "삼성", [row("마지막\n10경기", "7승 3패", "4승 6패", 7, 4, 0.4, False, "l")], text="삼성 · 4연패로 시즌 끝 · 타선은 무딜 가능성", textAt=2.0))   # 38 L39
SC.append(pv("구자욱", "삼성 · 변수 2", [], [st("타율", ".371 · 타격왕", 1.0, hi=True), st("출루율", "리그 1위", 2.4)], chain="p39"))                    # 39 L40
SC.append(pv("구자욱", "삼성 · 변수 2", [], [st("타율", ".371 · 타격왕", -1, hi=True), st("출루율", "리그 1위", -1),
                                         st("9월 30일", "햄스트링 힘줄 부상", 0.4, hi=True), st("10월 15일", "티배팅 시작", 2.05)], chain="p39", cont=True))           # 40 L41
SC.append(pv("구자욱", "삼성 · 변수 2", [vstamp("지명타자나 대타 유력", 3.0, "gold", size=48)], [st("타율", ".371 · 타격왕", -1, hi=True), st("출루율", "리그 1위", -1),
                                         st("9월 30일", "햄스트링 힘줄 부상", -1, hi=True), st("10월 15일", "티배팅 시작", -1)], chain="p39", cont=True))             # 41 L42
SC.append(pv("디아즈", "삼성 타자 · 타점왕 경쟁", [vstamp("삼성 득점은 디아즈의 한 방?", 3.4, "gold", size=46)], []))                            # 42 L43
SC.append(fo("변수 3 · 플레이오프 1차전 선발 · 대구", "네일", "후라도", [row("9월 이후\n평균자책점", "2.76", "4.60", 2.76, 4.60, 1.2, True, "l")]))      # 43 L44
SC.append(pv("네일", "KIA 선발", [], [st("퀄리티스타트", "20번", 0.4, hi=True)]))               # 44 L45
SC.append(pv("페덱", "삼성 선발 · 변수 4", [], [st("시즌 평균자책점", "2.95", 1.0), st("KIA전 2경기", "2패 · 평균자책점 5.25", 2.6, hi=True)]))          # 45 L46
SC.append(pv("양현종", "KIA 선발", [], [st("휴식", "열흘 넘게", -1), st("퀄리티스타트", "2번", 0.6, hi=True)], chain="p33"))                         # 46 L47
SC.append(SERP(["KIA", "삼성"], pills=[dict(label="필승조는 아낀다", at=0.6, c=KIAC)]))                                                     # 47 L48
SC.append(pv("올러", "KIA 선발 · 변수 5", [], [st("광주", "8승 4패", 1.0), st("광주 평균자책점", "2.28", 1.8, hi=True), st("준플레이오프 2차전", "승리 투수", 3.0)]))   # 48 L49
SC.append(pv("원태인", "삼성 선발", [vstamp("3차전은 KIA 쪽", 3.6, "gold", size=50)], [st("후반기 평균자책점", "5.61", 1.0, hi=True)]))                 # 49 L50
SC.append(HR("삼성", 140, text="삼성 · 디아즈", textAt=2.6))                                                                                 # 50 L51
SC.append(S(0, "big", team="KIA", text="4차전 · KIA 시라카와\n삼성 4번째 선발 · 난타전", size=88))                                            # 51 L52
SC.append(SERP(["KIA", "삼성", "KIA", "KIA"], text="3승 1패 · 한국시리즈로", size=64, textAt=2.4))                                            # 52 L53
# ── 3막 KS KT ──
SC.append(SERK([], pills=[dict(label="시리즈를 이길 확률 · 약 40%", at=1.6, c=KIAC)]))                                                         # 53 L54
SC.append(fo("정규시즌 맞대결 · KIA vs KT", "KIA", "KT", [row("시즌", "6승 10패", "10승 6패", 6, 10, 0.4, False, "l")]))                          # 54 L55
SC.append(HR("KT", 121, text="KT · 팀 타율 1위", textAt=1.4))                                                                                # 55 L56
SC.append(S(0, "big", team="KT", text="KT는 이어 치는 팀\nKIA는 넘기는 팀", size=104))                                                       # 56 L57
SC.append(steps("한국시리즈 · 변수 6가지", [("변수 1", "3주 휴식", 1.0, 0), ("변수 2", "KIA의 피로", 1.5, 0), ("변수 3", "최원준", 2.0, 0), ("변수 4", "힐리어드", 2.5, 0),
                                        ("변수 5", "광주", 3.0, 0), ("변수 6", "대니엘 재대결", 3.4, 0)]))                                                   # 57 L58
SC.append(S(0, "big", team="KT", text="변수 1 · 3주 휴식\nKT · 10월 12일 시즌 끝", size=92))                                                  # 58 L59
SC.append(steps("오래 쉬면", [("투수", "득", 0.6, 1), ("타자", "실전 감각이 떨어지는 독", 1.6, 0)]))                                           # 59 L60
SC.append(S(0, "big", team="KIA", text="변수 2 · KIA의 피로\n플레이오프 뒤 사흘 휴식", size=92))                                               # 60 L61
SC.append(S(0, "mups", pairs=[dict(tag="1차전 · 수원", at=0, l=dict(img=IMG["네일"], name="네일", team="KIA", focus="53% 20%"), r=dict(img=IMG["대니엘"], name="대니엘", team="KT"),
                                     notes=[dict(t="9월 이후 39이닝", at=2.0), dict(t="삼진 54개", at=3.0, hi=True)]),
                                dict(tag="2차전 · 수원", at=1.0, l=dict(img=IMG["양현종"], name="양현종", team="KIA", focus="48% 30%"), r=dict(img=IMG["고영표"], name="고영표", team="KT", focus="50% 0%"),
                                     notes=[dict(t="15승 · 공동 다승왕", at=4.0, hi=True)])]))   # 10/20 사용자 "누구 대 누구 — 다 나오게"   # 61 L62
SC.append(S(0, "big", team="KT", text="KT · 10연승으로 시즌 끝\n마무리 박영현 · 30세이브 무패", size=84))                                     # 62 L63
SC.append(SERK(["KT", "KT"], pills=[dict(label="네일 vs 대니엘 · 광주 KIA 승 · 수원 KT 승", at=0.4, c=KTK)], text="0승 2패로 시작", size=60, textAt=5.0))   # 63 L64
SC.append(pv("최원준", "KT 1번 타자 · 변수 3", [], [st("이적", "KIA → NC → KT", 1.0), st("안타", "208개", 2.2, hi=True)], chain="p64"))            # 64 L65
SC.append(pv("최원준", "KT 1번 타자 · 변수 3", [vstamp("1번이 나가면 이어 치기", 0.8, "bad", size=48)], [st("이적", "KIA → NC → KT", -1), st("안타", "208개", -1, hi=True)], chain="p64", cont=True))   # 65 L66
SC.append(pv("힐리어드", "KT · 변수 4", [], [st("홈런", "44개", 2.2), st("타점", "타점왕", 3.0, hi=True)]))                                     # 66 L67
SC.append(duel("서로 상대 홈런 타자를 거르는 시리즈", "김도영", "힐리어드", "KIA 홈런왕", "KT 타점왕"))                                          # 67 L68
SC.append(fo("변수 5 · 광주 맞대결", "KIA", "KT", [row("광주", "4승 5패", "5승 4패", 4, 5, 4.0, False, "l")], rightColor="#8A93A6",
             chips=[dict(d="9월 4~6일", v="KIA 3연승", at=5.0, c="#C70125", tc="#FF5A63"), dict(d="9월 29일~10월 1일", v="KIA 3연패", at=6.0, c="#5A4A4E", tc="#BCA9A2")]))   # 10/20 사용자: 한 줄 흰 글 → 날짜·결과 칸 두 개   # 68 L69
SC.append(pv("카스트로", "KIA 4번 타자", [], [st("9월 6일 광주", "김도영 고의4구 뒤", 0.6), st("카스트로", "2타점 2루타", 1.8, hi=True)]))          # 69 L70
SC.append(duel("한국시리즈 3차전 · 광주", "올러", "소형준", "KIA 선발", "KT 선발", text="투수전 · 올러가 조금 앞선다", textAt=7.0))               # 70 L71
SC.append(pv("로건", "KT 4차전 선발", [], [st("9월 5경기", "평균자책점 5.79", 1.4, hi=True), st("10월 5일", "삼진 14개", 3.0)]))                    # 71 L72
SC.append(SERK(["KT", "KT", "KIA", "KIA"], text="난타전 · 2승 2패", size=60, textAt=3.0))                                                    # 72 L73
SC.append(pv("대니엘", "KT 5차전 선발 · 변수 6", [IPV(("9월 6일 광주", 3, 3, None, 3.0), ("9월 30일 광주", 6, 2, 13, 4.4))], []))   # 73 L74
SC.append(SERK(["KT", "KT", "KIA", "KIA", "KIA"], text="3승 2패", size=64, textAt=3.6))                                                     # 74 L75
SC.append(duel("한국시리즈 6차전 · 수원", "양현종", "고영표", "KIA 선발", "KT 선발", text="고영표 공동 다승왕 · 양현종 퀄리티스타트 2번", textAt=2.0))   # 75 L76
SC.append(SERK(["KT", "KT", "KIA", "KIA", "KIA", "KT"], text="3승 3패", size=64, textAt=2.6))                                                 # 76 L77
SC.append(fo("7차전 · 수원 · 시즌 평균자책점", "소형준", "올러", [row("시즌", "3.15", "3.13", 3.15, 3.13, 2.0, True)], text="수원 · 광주 강세는 소용없다", textAt=0.6))   # 77 L78
SC.append(S(0, "big", text="선발이 대등하면\n승부는 막판 한 타석", size=104))                                                               # 78 L79
SC.append(steps("7차전 막판 · 만루라면", [("거르면", "밀어내기 1점", 2.0, 0), ("그래서", "김도영과 정면 승부", 3.0, 1)]))                  # 79 L80
SC.append(S(0, "big", team="KT", text="KT 마무리 박영현\n30세이브 무패", size=100))                                                                          # 80 L81
SC.append(pv("김도영", "KIA 3번 타자 · 홈런왕", [], [st("정규시즌 마지막 날", "결승 투런 · 홈런왕 확정", 0.4, hi=True), st("준플레이오프 1차전", "홈런 2방", 2.4)]))     # 81 L82
SC.append(S(0, "big", team="KIA", text="피해 다닌 김도영이\n직접 끝낸다", size=110))                                                  # 82 L83
SC.append(SERK(["KT", "KT", "KIA", "KIA", "KIA", "KT", "KIA"], text="7차전 KIA · 4승 3패 우승", size=72, textAt=0.6))                           # 83 L84
SC.append(steps("준플레이오프부터 올라와 우승", [("1992", "롯데", -1, 0), ("2001", "두산", -1, 0), ("2015", "두산", -1, 0), ("2026", "KIA?", 1.2, 1)], chain="y3"))   # 84 L85
SC.append(steps("예측 정리", [("준플레이오프", "3연승", 0.6, 0), ("플레이오프", "3승 1패", 2.0, 0), ("한국시리즈", "0승 2패 → 4승 3패", 3.4, 1)]))           # 85 L86
SC.append(S(0, "gauge", title="KIA 우승 확률 · 단계마다 곱하기", steps=[{'label': '준PO', 'team': 'LG', 'pass': 92, 'at': 0.2}, {'label': 'PO', 'team': '삼성', 'pass': 46, 'at': 1.2},
                                                                   {'label': '한국시리즈', 'team': 'KT', 'pass': 40, 'at': 2.2}]))                              # 86 L87
SC.append(S(0, "warn"))                                                                                                     # 87 L88
SC.append(S(0, "question", text="올해 KIA 우승?\n댓글로 예측을 남겨 주세요", logos=["KIA"], size=96))                                          # 88 L89

N = len(LINES)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, (sub, nar) in enumerate(LINES):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(nar), sub_of(sub))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "준플레이오프 3차전", "title": "1막 · 준플레이오프 3차전 · 변수 4가지", "from": 6, "to": 31},
      {"key": "플레이오프 삼성", "title": "2막 · 플레이오프 삼성 · 변수 6가지", "from": 32, "to": 52},
      {"key": "한국시리즈 KT", "title": "3막 · 한국시리즈 KT · 변수 6가지", "from": 53, "to": 84},
      {"key": "예측 정리", "title": "정리 · 우승 확률 약 17%", "from": 85, "to": 88}]

TAGS = ["KIA 우승", "기아 우승", "KIA 타이거즈", "기아타이거즈", "한국시리즈", "2026 한국시리즈", "플레이오프", "준플레이오프", "가을야구", "KIA 한국시리즈",
        "김도영", "카스트로", "나성범", "네일", "올러", "양현종", "시라카와", "삼성 라이온즈", "KT 위즈", "LG 트윈스", "구자욱", "대니엘", "힐리어드", "최원준", "프로야구", "KBO", "야구자판기"]
DESC = ("이 영상은 채널 주인장의 망상이에요. KIA가 준플레이오프부터 올라와 한국시리즈에서 우승하려면 경기마다 어떤 변수가 KIA 쪽으로 굴러가야 할까요?\n\n"
        "준플레이오프 3차전(선발·불펜·김도영 견제·잠실), 플레이오프 삼성(휴식·구자욱·네일 대 후라도·페덱·올러·장타), 한국시리즈 KT(3주 휴식·KIA 피로·최원준·힐리어드·광주·대니엘 재대결)의 변수를 기록으로 따져 가능성이 높은 쪽을 골랐어요.\n\n"
        "올해 정규시즌 득점과 실점으로 계산한 KIA 통과 확률은 준플레이오프(2승 0패에서) 92%, 플레이오프 46%, 한국시리즈 40% — 곱하면 우승 확률 약 17%, 6번 중 1번꼴이에요.\n\n"
        "※ 경기 결과는 예측이에요. 우승 확률은 이 채널이 직접 계산한 추정치로, 홈 이점 가정에 따라 조금 달라질 수 있어요.\n\n"
        "여러분은 올해 KIA가 우승할 거라고 보시나요? 댓글로 예측을 남겨 주세요.\n\n"
        "기록: KBO 기록실·KBO 영문 기록, mykbostats(경기 기록). 기사: 스포츠경향·데일리안·세계일보·MHN·마이데일리·OSEN·뉴스엔(10/14~19), 엑스포츠뉴스(9/7·10/6), 머니투데이(9/12·10/7·10/15), 서울신문·일간스포츠(구자욱), 매일신문(페덱), 파이낸셜뉴스(10/1), 뉴시스(10/12), 데일리안 2015·디지털타임스 2018(역대 기록)\n"
        "사진: KIA 타이거즈 제공, 삼성 라이온즈 제공, KT 위즈 제공, LG 트윈스 제공")
SOURCE = "사실 출처 = 프로젝트 claude/1019-롱폼20-기아우승망상-대사v17-확정.md · 검수 claude/검수에이전트-1020-대사-기아우승망상.md. 우승 확률 = 채널 계산."

EP = {"introChapter": "오프닝", "date": "2026-10-19", "gameDate": "2026-10-19", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.25, "ttsTempoSlow": 1.2,
      "rev": "1019-long20-v17", "topic": "기아우승망상", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼20_기아우승망상.jpg", "source": SOURCE,
      "youtube": {"title": "KIA 한국시리즈 우승 망상회 | 변수 16개로 따져 본 우승 시나리오, 확률은 17% #KIA #한국시리즈",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#KIA타이거즈", "#한국시리즈", "#가을야구", "#김도영", "#플레이오프", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 3, 86, 87}
    HOLD = {0: 0.35, 3: 0.35, 5: 0.3, 31: 0.35, 52: 0.35, 63: 0.3, 72: 0.3, 74: 0.3, 76: 0.3, 83: 0.4, 86: 0.35}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-19_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    import subprocess; subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mang_fx_1019.py'), out], check=True)   # 망냥이·효과·어두운 톤
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
