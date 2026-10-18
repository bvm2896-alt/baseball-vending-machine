# -*- coding: utf-8 -*-
"""10/18 롱폼⑱ 「2026 골든글러브 예상 — 외야 4명 중 1명은 떨어진다」 (음성 API · 줄별 배속).
대사 = tools/text_1018_long18.py (검수 3회 + 이대호 본문 확인). 나레이션 앞처리 = narr_1018.pre → narr_1016.pre → gen_1015_long15.narr_of.
근거 = KBO 보도자료 별첨(10/17, 후보 79명·정규시즌 기록) + 기사 본문 — 프로젝트 claude/1018-롱폼18-골든글러브-대사v4.md.
사진: 인물 사진은 영상 전체 경기(플레이) 사진으로 통일(10/18 사용자 "누구는 프로필이고 누구는 플레이 사진이야? 하나로 통일") — 막대 얼굴 원도 경기 사진 카드.
10/18 밤 v6(검수 에이전트 1라운드): 대사 v6, 인터뷰 말풍선 10명·팬 반응, 글자만 장면 → 사진 판, 막대 얼굴 원(G18원_), 배트 투척·45호 사진, 목차 강조·후보 수, 가운데 정렬.
10/18 수정: 소형준 카드 새로 자름(얼굴 가운데), 강민호·신민재·최형우·노시환·이숭용·류현진(한화 시절) 프로필 → 경기 사진, 후보 기준 카드 높이 고정(khide)·아이콘(야구공·글러브·방망이)·줄바꿈."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1018_long18.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
import narr_1016, narr_1018
def narr_of(t):
    t = narr_of15(narr_1016.pre(narr_1018.pre(t)))
    t = t.replace('십자리', '열 자리').replace('백십사 경기', '백열네 경기').replace('이백탈삼진', '이백 탈삼진')                                           # 10/18 밤: '10자리' → 열 자리
    t = re.sub(r'(일|이|삼) 루', r'\1루', t)                                   # 일루·이루·삼루(숫자와 '루' 사이 쉼 방지)
    return re.sub(r'(일|이|삼|사|오|칠|팔) (차전|연승|연패)', r'\1\2', t)        # 일차전
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
RED, GOLD, GRAY = "#E5484D", "#E8A100", "#8A93A3"
C, G, F = '카드/', '경기/', 'KBO프로필/'
P = {  # 인물 카드(경기 사진) — 같은 사람은 흐름마다 다른 사진
    "곽빈A": C + "곽빈_MVP_포효", "곽빈B": C + "P15_곽빈_WC", "곽빈C": C + "G18_곽빈_C",
    "고영표": C + "R13_고영표_상체", "임찬규": C + "P17_임찬규_1012", "올러": C + "P15_올러_포효", "네일": C + "P17_네일_환호",
    "김재윤": C + "T12_김재윤", "소형준": C + "G18_소형준_B",
    "양의지": C + "F16_양의지_A", "강민호": C + "G18_강민호_포수",
    "허인서A": C + "G18_허인서_A", "허인서B": C + "G18_허인서_B", "허인서C": C + "G18_허인서_C", "김형준": C + "G18_김형준_A",
    "오스틴A": C + "오스틴_MVP_포효", "오스틴B": C + "P15_오스틴_WC", "오스틴C": C + "오스틴_41호_사진",
    "디아즈A": C + "FA9_디아즈_경기", "디아즈B": C + "G18_디아즈_B",
    "신민재": C + "G18_신민재_A", "박민우A": C + "G18_박민우_A", "박민우B": C + "G18_박민우_B", "류지혁": C + "G18_류지혁_A",
    "김도영A": C + "김도영_43호_사진", "김도영B": C + "R13_김도영", "김도영C": C + "P17_김도영_질주", "노시환": C + "G18_노시환_A",
    "박성한A": C + "G18_박성한_A", "박성한B": C + "G18_박성한_B", "이숭용": C + "G18_이숭용_덕아웃",
    "김주원A": C + "G18_김주원_A", "김주원B": C + "G18_김주원_B", "박찬호": C + "G18_박찬호_E",
    "황성빈": C + "G18_황성빈_A", "나성범": C + "G18_나성범_A",
    "구자욱A": C + "F16_구자욱_H", "구자욱B": C + "F16_구자욱_A", "구자욱C": C + "F16_구자욱_B",
    "레이예스A": C + "R13_레이예스", "레이예스B": C + "레이예스_MVP_세리머니", "레이예스C": C + "T12_레이예스_미소",
    "최원준A": C + "FA10_최원준_204", "최원준B": C + "R13_최원준_미소", "최원준C": C + "FA10_최원준_204", "최원준D": C + "G18_최원준_원",
    "힐리어드A": C + "힐리어드_MVP_포효", "힐리어드B": C + "T12_힐리어드_하이파이브", "힐리어드C": C + "FA9_힐리어드_하늘",
    "강백호A": C + "FA10_강백호_30호", "강백호B": C + "FA10_강백호_환대", "최형우A": C + "FA10_최형우_100타점", "최형우B": C + "G18_최형우_미소",
    "김재환": C + "FA10_김재환_결승포", "이대호": C + "G18_이대호",
    "김도영D": C + "G18_김도영_45호", "최원준T": C + "G18_최원준_배트투척",
}
W = lambda n: C + "G18원_" + n   # 10/18 밤: 얼굴 원 전용 정사각 얼굴 컷(같은 얼굴 크기) — 막대·얼굴판 원
PF = lambda n: C + "G18P_" + n   # 10/18 밤 사용자 "원 안에 사진은 프로필 사진으로": 얼굴 원은 전부 구단 프로필(얼굴 가운데)
GP = {n: PF(n) for n in ("구자욱", "레이예스", "최원준", "힐리어드")}   # 외야 4명 얼굴 원 — 같은 얼굴 크기·정면
GP2 = GP
PR = {"곽빈": PF("곽빈"), "선동열": W("선동열"), "류현진": PF("류현진"), "김도영": PF("김도영"), "힐리어드": PF("힐리어드")}   # 선동열은 프로필 없음(1989년 사진)   # 10/18: 막대 얼굴 원도 경기 사진(프로필 금지)
TM = {"곽빈": "두산", "고영표": "KT", "임찬규": "LG", "올러": "KIA", "네일": "KIA", "김재윤": "삼성", "소형준": "KT", "양의지": "두산", "강민호": "삼성",
      "허인서": "한화", "김형준": "NC", "오스틴": "LG", "디아즈": "삼성", "신민재": "LG", "박민우": "NC", "류지혁": "삼성", "김도영": "KIA", "노시환": "한화",
      "박성한": "SSG", "이숭용": "SSG", "김주원": "NC", "박찬호": "두산", "황성빈": "롯데", "나성범": "KIA", "구자욱": "삼성", "레이예스": "롯데",
      "최원준": "KT", "힐리어드": "KT", "강백호": "한화", "최형우": "삼성", "김재환": "SSG", "선동열": None, "류현진": "한화"}
def nm(k): return re.sub(r'[A-Z]$', '', k)
def pv(img, sub, viz=(), stats=(), **k): n = nm(img); return S(0, "pstat", img=P[img], team=TM.get(n), name=n, sub=sub, viz=list(viz), stats=list(stats), **k)   # 10/18 밤: noCenter 해제 — 묶음 가운데 맞춤(사진 고정)
def sp(img, sub, bubbles, **k): n = nm(img); return S(0, "speech", img=P[img], name=n, sub=sub, bubbles=bubbles, **k)
def bub(date, text, at, src=False): return dict(date=date, text=text, at=at, src=src)
def side(img, role): n = nm(img); return {"img": P[img], "name": n, "team": TM.get(n), "role": role}
def fo(title, L_, R_, rows, **k): return S(0, "faceoff", title=title, left=L_, right=R_, rows=rows, **k)
def duel(title, a, ra, b, rb): return S(0, "duel", title=title, left=dict(side(a, ra), at=0), right=dict(side(b, rb), at=0.6), vsAt=0.3)
def ppl(title, items, ats=None, **k): return S(0, "people", ph=420, title=title, items=[dict(img=P[i], name=nm(i), note=n, at=(ats[j] if ats else 0.3 + j * 0.8)) for j, (i, n) in enumerate(items)], **k)
def toc(on, **k): return S(0, "toc", on=on, noNum=True, colMajor=True, **k)
def hid(d): return dict(d, at=-1)
AS = "2026 정규시즌 최종"


OF4 = [("구자욱", "타격왕"), ("레이예스", "최다 안타 신기록"), ("최원준", "득점왕"), ("힐리어드", "타점왕")]
OFT = "2026 외야수 · 타이틀 4명"
def of4(say=False, sayAt=None, **k): return S(0, "facegrid", title=OFT, cols=4, items=[dict(img=GP[n], name=n, team=TM[n], **({"say": t, "sayAt": (j * 0.5 if sayAt is None else sayAt)} if say else {})) for j, (n, t) in enumerate(OF4)], chain="of4", size=60, **k)
SUM10 = [dict(img="카드/G18P_" + n, name=n, team=tm, pos=ps) for n, tm, ps in [("곽빈", "두산", "투수"), ("허인서", "한화", "포수"), ("오스틴", "LG", "1루수"), ("박민우", "NC", "2루수"), ("김도영", "KIA", "3루수"),
         ("박성한", "SSG", "유격수"), ("구자욱", "삼성", "외야수"), ("레이예스", "롯데", "외야수"), ("힐리어드", "KT", "외야수"), ("강백호", "한화", "지명타자")]]
SLOT = [dict(name=x["name"], pos=x["pos"], ph=True) for x in SUM10]   # 10/18 밤: 8개 포지션·10자리 빈 판('?' 원 + 포지션 이름표, 사진 없음)
GGT = "골든글러브 · 8개 포지션 10자리"
def slots(text, **k): return S(0, "facegrid", title=GGT, cols=5, items=SLOT, chain=k.pop("chain", "slot"), size=56, text=text, textAt=k.pop("textAt", 0.3), **k)

import base64 as _b64
def _icon(name):   # 10/18: 이모지 대신 같은 스타일 아이콘(🧤 겨울 장갑·🏏 크리켓 배트 금지) — 시스템/assets/icons/*.png
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'icons', name + '.png')
    return f'<img src="data:image/png;base64,{_b64.b64encode(open(f, "rb").read()).decode()}" style="display:block;margin:0 auto;height:150px;width:150px;object-fit:contain">'
CRIT = [(_icon("ball"), "투수", "144이닝 · 10승\n30세이브 · 30홀드\n중 하나 이상"), (_icon("glove"), "포수 · 야수", "그 포지션 수비\n720이닝 이상"), (_icon("bat"), "지명타자", "지명타자로\n297타석 이상")]
# 10/18 사용자("뚝 끊기며 갑자기 카드가 커져"): 설명 글은 처음부터 자리를 잡고(khide) 차례가 되면 그 자리에서 뜬다 — 카드·제목 크기·위치 고정
def crit(show_k, **k): return S(0, "tiles", title="골든글러브 후보 기준", items=[dict(emoji=e, v=v, k=kk, khide=(j >= show_k), vhide=(j >= show_k), at=(0 if j == show_k - 1 else -1) if show_k else j * 0.3) for j, (e, v, kk) in enumerate(CRIT)], vsize=64, chain="crit", **k)   # 10/18 밤: 차례 전 카드는 틀만(제목·설명 숨김)

KB = "두산 투수"
def vq(date, text, at=0.4, src=False, **k): return dict(type="quote", date=date, text=text, at=at, src=src, **k)   # 10/18 밤: 인터뷰 한마디를 같은 인물 카드 안에(사진·이름 고정)
K1 = [st("평균자책점", "2.24 · 1위", 0, hi=True), st("탈삼진", "197개 · 1위", 1, hi=True)]
K2 = [st("던진 이닝", "161이닝", 0), st("9이닝당 삼진", "11.01개", 1)]
HIS = "한화 포수"
OS = "LG 1루수"
DZ = "삼성 1루수 · 지난해 수상"
PMW = "NC 2루수 · 주장"
KDY = "KIA 3루수"
PSH = "SSG 유격수"
NV = "#3B4A63"
def q(img, sub, date, text, at=0.4, **k): return sp(img, sub, [bub(date, text, at)], **k)   # 인터뷰 한마디(본인 발언 = 꼬리 달린 말풍선, 날짜·언론사)

SCN = [
 # 0~4 훅
 ("타격왕, 최다 안타", of4(say=True)),
 ("그런데 외야 골든글러브는", of4(say=True, cont=True, text="자리는 3개 · 1명은 탈락", textAt=1)),
 ("동점이 나와", of4(say=True, cont=True, text="동점이면 공동 수상 · 2004년 단 한 번", textAt=0.3)),
 ("10월 17일 KBO가", slots("10월 17일 · 후보 79명 발표", textAt=1)),
 ("오늘은 8개 포지션", slots("투수부터 지명타자까지", cont=True, textAt=1)),
 # 5~14 뽑는 법
 ("먼저 골든글러브를", toc(0)),
 ("투수는 규정이닝", crit(1)),
 ("포수와 야수는", crit(2, cont=True)),
 ("지명타자는 지명타자로", crit(3, cont=True)),
 ("대신 개인 타이틀", crit(3, cont=True, text="개인 타이틀 1위 = 자동 후보", textAt=0)),
 ("투표는 미디어", slots("투표 · 올 시즌 취재한 미디어 관계자", chain="slot2", textAt=0)),
 ("포스트시즌 도중에", slots("포스트시즌 중 투표 · 정규시즌 성적만", chain="slot2", cont=True, textAt=0)),
 ("후보는 투수 25명", S(0, "bars", title="포지션별 후보 · 79명", items=[dict(label=k, value=v, unit="명", at=a, hi=(k == "투수")) for k, v, a in [("투수", 25, 0), ("외야수", 21, 0.5), ("포수", 7, 1), ("유격수", 7, 1.3), ("2루수", 6, 2), ("1루수", 5, 3), ("3루수", 5, 3.3), ("지명타자", 3, 4)]], max=25)),
 ("LG, 삼성, KT가", S(0, "bars", title="구단별 후보 수", items=[dict(label=t, team=t, value=v, unit="명", at=(0 if v == 10 else 1), hi=(v == 10), color=(None if v == 10 else NV)) for t, v in [("LG", 10), ("삼성", 10), ("KT", 10), ("한화", 9), ("롯데", 9), ("KIA", 7), ("두산", 7), ("SSG", 6), ("NC", 6), ("키움", 5)]], max=10, text="한화 · 8개 포지션 모두 후보", textAt=1)),
 ("수상자는 12월 8일 / 시상식 당일", slots("12월 8일 시상식 · 수상자 10명 공개", chain="slot3", textAt=0)),
 ("그럼 첫 포지션", toc(1, text="투수 후보 25명")),
 # 16~27 투수
 ("두산 곽빈이", pv("곽빈A", KB, chain="kb")),
 ("평균자책점 2.24", pv("곽빈A", KB, stats=K1, chain="kb", cont=True, asof=AS)),
 ("161이닝을 던졌는데", pv("곽빈A", KB, stats=[hid(x) for x in K1] + K2, chain="kb", cont=True, asof=AS)),
 ("이 숫자는", S(0, "bars", title="9이닝당 삼진 · 국내 투수", items=[
     dict(label="곽빈", sub="2026년", img=PR["곽빈"], team="두산", value=11.01, unit="개", at=0, hi=True),
     dict(label="선동열", sub="1989년", img=PR["선동열"], value=10.54, unit="개", at=3, color=NV),
     dict(label="류현진", sub="2012년", img=PR["류현진"], team="한화", value=10.35, unit="개", at=3.3, color=NV)], max=12, text="150이닝 넘게 던진 국내 투수 역대 1위", textAt=2, size=48)),
 ("이닝당 출루 허용도", pv("곽빈B", KB, stats=[st("이닝당 출루 허용", "1.04 · 1위", 1, hi=True)], chain="kb2", asof=AS)),
 ("다만 승리는 11승", pv("곽빈B", KB, stats=[hid(st("이닝당 출루 허용", "1.04 · 1위", 1, hi=True)), st("승리", "11승 7패", 0)], chain="kb2", cont=True, asof=AS)),
 ("곽빈은 8월에", pv("곽빈B", KB, [vq("8월 8일 · KBS · 요약", "“타이틀 욕심은 진짜 하나도 없고요”", 1)], [hid(st("이닝당 출루 허용", "1.04 · 1위", 1, hi=True)), hid(st("승리", "11승 7패", 0))], chain="kb2", cont=True, asof=AS)),
 ("다승왕은", ppl("다승왕 · 15승 공동", [("고영표", "KT 선발"), ("임찬규", "LG 선발")], ats=[0, 0.3])),
 ("고영표는 평균자책점", pv("고영표", "KT 선발 · 다승왕", [vstamp("정규시즌 1위 KT", 2, "gold", size=50)], [st("평균자책점", "3.28", 0), st("탈삼진", "183개", 1)], asof=AS)),
 ("KIA 올러는", ppl("KIA 선발 두 명", [("올러", "평균자책점 3.13 · 2위"), ("네일", "183이닝 · 가장 많이")], ats=[0, 1])),
 ("세이브왕은 35세이브", ppl("다른 타이틀 1위", [("김재윤", "세이브왕 · 35세이브"), ("소형준", "승률왕 · 10승 3패")], ats=[0, 1])),
 ("그래도 제 예상은 곽빈", pv("곽빈C", "제 예상 · 투수", [vstamp("평균자책점 · 탈삼진 1위", 2, "gold", size=48)], [st("평균자책점", "2.24", 1), st("탈삼진", "197개", 1)], asof=AS)),
 # 28~38 포수
 ("다음은 포수", toc(2, text="포수 후보 7명")),
 ("2011년부터 지난해까지", S(0, "facegrid", title="포수 골든글러브 · 2011~2025", cols=2, items=[dict(img=PF("양의지"), name="양의지"), dict(img=PF("강민호"), name="강민호")], chain="yk", size=60)),
 ("그런데 올해는", S(0, "facegrid", title="포수 골든글러브 · 2011~2025", cols=2, items=[dict(img=PF("양의지"), name="양의지"), dict(img=PF("강민호"), name="강민호")], chain="yk", cont=True, size=60, text="2026 · 둘 다 후보 없음\n포수 수비 720이닝 못 채움", textAt=1)),
 ("15년 이어진", S(0, "facegrid", title="포수 골든글러브 · 2011~2025", cols=2, items=[dict(img=PF("양의지"), name="양의지"), dict(img=PF("강민호"), name="강민호")], chain="yk", cont=True, size=60, text="15년 시대 끝\n2026년엔 새 얼굴", textAt=0)),
 ("가장 앞선 선수는 한화 허인서", pv("허인서A", HIS, stats=[st("타율", "2할 8푼 3리", 1), st("홈런", "20개", 2, hi=True), st("타점", "79개", 2, hi=True)], chain="hsa", asof=AS)),
 ("홈런과 타점 모두", pv("허인서A", HIS, stats=[st("타율", "2할 8푼 3리", -1), st("홈런", "20개 · 포수 1위", 0, hi=True), st("타점", "79개 · 포수 1위", 0, hi=True)], chain="hsa", cont=True, asof=AS)),
 ("이글스 포수의", pv("허인서B", HIS, [vstamp("1989년 이후 처음", 1, "gold", size=50)], stats=[st("이글스 포수 홈런", "20개", 0, hi=True)], chain="hs2")),
 ("아직 신인 자격도", S(0, "tiles", title="허인서 · 아직 신인 자격", items=[dict(emoji=_icon("sprout"), v="신인왕", at=1), dict(emoji=_icon("glove_gold"), v="골든글러브", at=1.3)], vsize=84, text="둘 다 받으면 · 포수로는 36년 만", textAt=2)),
 ("허인서는 시즌 전", pv("허인서A", HIS, [vq("10월 13일 · 서울신문 · 요약", "“첫 홈런이 목표였는데\n20개까지 오게 됐다”", 1)])),
 ("경쟁자는 NC 김형준", fo("포수 골든글러브 경쟁", side("허인서C", "한화 포수"), side("김형준", "NC 포수"),
     [dict(k="홈런", l="20개", r="17개", lv=20, rv=17, at=1), dict(k="타점", l="79개", r="66개", lv=79, rv=66, at=1.3), dict(k="도루 저지율", l="32.9%", r="31.9%", lv=32.9, rv=31.9, at=3)], chain="hk")),
 ("그래도 제 예상은 허인서", fo("포수 골든글러브 경쟁", side("허인서C", "한화 포수"), side("김형준", "NC 포수"),
     [dict(k="홈런", l="20개", r="17개", lv=20, rv=17, at=-1), dict(k="타점", l="79개", r="66개", lv=79, rv=66, at=-1), dict(k="도루 저지율", l="32.9%", r="31.9%", lv=32.9, rv=31.9, at=-1)], chain="hk", cont=True, text="제 예상 · 허인서", textAt=0)),
 # 39~49 1루수
 ("다음은 1루", toc(3, text="1루수 후보 5명")),
 ("1루는 LG 오스틴과", duel("1루수 골든글러브", "오스틴A", "LG 1루수", "디아즈A", "삼성 · 지난해 수상")),
 ("LG 오스틴은", pv("오스틴B", OS, stats=[st("타율", "3할 3푼 1리", 0), st("홈런", "41개", 1), st("타점", "127개", 1), st("OPS(출루율+장타율)", "1.062 · 1위", 3, hi=True)], chain="os", asof=AS)),
 ("오스틴은 41호를", pv("오스틴B", OS, [vq("10월 7일 · SPOTV뉴스", "“100홈런도 칠 수 있을 줄 알았다”", 1)], [hid(st("타율", "3할 3푼 1리", 0)), hid(st("홈런", "41개", 1)), hid(st("타점", "127개", 1)), hid(st("OPS(출루율+장타율)", "1.062 · 1위", 3, hi=True))], chain="os", cont=True, asof=AS)),
 ("그런데 공식 타이틀은", S(0, "rankstrip", team="LG", title="오스틴 · 공식 타이틀 0개", rows=[dict(k="홈런", v="41개", rank=3, at=1), dict(k="타점", v="127개", rank=3, at=1.3)])),
 ("1루 수비는 723이닝", S(0, "bars", title="1루 수비 이닝 · 2026", items=[dict(label="오스틴", img=PF("오스틴"), team="LG", value=723, note="723이닝", at=0, hi=True), dict(label="후보 기준", value=720, note="720이닝", at=1, color=GRAY)], max=1200, chain="fb", asof=AS)),
 ("맞서는 선수는", pv("디아즈A", DZ, chain="dz")),
 ("타율 3할 5리", pv("디아즈A", DZ, [vstamp("2년 연속 120타점", 2, "gold", size=50)], [st("타율", "3할 5리", 0), st("홈런", "26개", 0), st("타점", "129개 · 2위", 1, hi=True)], chain="dz", cont=True, asof=AS)),
 ("1루 수비는 1,200이닝", S(0, "bars", title="1루 수비 이닝 · 2026", items=[dict(label="오스틴", img=PF("오스틴"), team="LG", value=723, note="723이닝", at=-1, hi=True), dict(label="후보 기준", value=720, note="720이닝", at=-1, color=GRAY), dict(label="디아즈", img=PF("디아즈"), team="삼성", value=1200, note="1,200이닝", at=0, color=NV)], max=1200, chain="fb", cont=True, asof=AS)),
 ("제 예상은 오스틴이에요", fo("제 예상 · 1루수", side("오스틴C", "LG 1루수"), side("디아즈B", "삼성 1루수"),
     [dict(k="홈런", l="41개", r="26개", lv=41, rv=26, at=2)], chain="1b", text="오스틴 · OPS 리그 1위", textAt=1)),
 ("다만 투표인단이", fo("제 예상 · 1루수", side("오스틴C", "LG 1루수"), side("디아즈B", "삼성 1루수"),
     [dict(k="홈런", l="41개", r="26개", lv=41, rv=26, at=-1), dict(k="1루 수비", l="723이닝", r="1,200이닝", lv=723, rv=1200, at=1, w="r")], chain="1b", cont=True, text="오스틴 · OPS 리그 1위")),
 # 50~57 2루수
 ("이어서 2루로", toc(4, text="2루수 후보 6명")),
 ("지난해 수상자 LG 신민재", pv("신민재", "LG 2루수 · 지난해 수상", [vstamp("올해 주춤", 1, "bad", size=54)], [st("2026 타율", "2할 5푼 1리", 1)], asof=AS)),
 ("NC 캡틴 박민우가", pv("박민우B", PMW, chain="pmw")),
 ("타율 3할 2푼", pv("박민우B", PMW, stats=[st("타율", "3할 2푼", 0), st("출루율", "4할 5리", 1), st("도루", "50개", 2, hi=True)], chain="pmw", cont=True, asof=AS)),
 ("21살이던 2014년", pv("박민우B", PMW, [vtrend([dict(x="2014년 · 21살", v=50, vt="50도루", at=0), dict(x="2026년 · 33살", v=50, vt="50도루", c="good", at=1)], title="한 시즌 50도루")], [hid(st("타율", "3할 2푼", 0)), hid(st("출루율", "4할 5리", 1)), hid(st("도루", "50개", 2, hi=True))], chain="pmw", cont=True, asof=AS)),
 ("박민우는 9월에", pv("박민우B", PMW, [vq("9월 10일 · 스포츠경향", "“올해가 아니면 못 받을 것 같다”", 1)], [hid(st("타율", "3할 2푼", 0)), hid(st("출루율", "4할 5리", 1)), hid(st("도루", "50개", 2, hi=True))], chain="pmw", cont=True, asof=AS)),
 ("경쟁자 삼성 류지혁", fo("2루수 비교", side("박민우A", "NC 2루수"), side("류지혁", "삼성 2루수"),
     [dict(k="타율", l="3할 2푼", r="2할 8푼", lv=.320, rv=.280, at=1), dict(k="도루", l="50개", r="29개", lv=50, rv=29, at=2)], chain="2b")),
 ("제 예상은 박민우", fo("2루수 비교", side("박민우A", "NC 2루수"), side("류지혁", "삼성 2루수"),
     [dict(k="타율", l="3할 2푼", r="2할 8푼", lv=.320, rv=.280, at=-1), dict(k="도루", l="50개", r="29개", lv=50, rv=29, at=-1)], chain="2b", cont=True, text="제 예상 · 박민우", textAt=0)),
 # 58~66 3루수
 ("3루는 고민이", toc(5, text="3루수 후보 5명")),
 ("KIA 김도영 / 45홈런", pv("김도영A", KDY, stats=[st("홈런", "45개 · 1위", 1, hi=True), st("장타율", "6할 4푼 7리 · 1위", 2, hi=True)], chain="kdy", asof=AS)),
 ("타율 3할 8리", pv("김도영A", KDY, stats=[st("홈런", "45개 · 1위", -1, hi=True), st("장타율", "6할 4푼 7리 · 1위", -1, hi=True), st("타율", "3할 8리", 0), st("타점", "118개", 0), st("득점", "120개", 1)], chain="kdy", cont=True, asof=AS)),
 ("시즌 마지막 날", S(0, "bars", title="2026 홈런왕 · 마지막 날", items=[dict(label="김도영", img=PR["김도영"], team="KIA", value=45, unit="개", at=1, hi=True), dict(label="힐리어드", img=PR["힐리어드"], team="KT", value=44, unit="개", at=0, color=NV)], max=45, text="8회 결승 투런 · 45호", textAt=1.3)),
 ("이 한 방이", pv("김도영D", KDY, [vstamp("프로 통산 100호 홈런", 1, "gold", size=50)], chain="kdyd")),
 ("김도영은 경기 뒤", pv("김도영D", KDY, [hid(vstamp("프로 통산 100호 홈런", 1, "gold", size=50)), vq("10월 12일 · 스포츠경향", "“나 올해 진짜 왜 이러지?”", 1)], chain="kdyd", cont=True)),
 ("한화 노시환도", pv("노시환", "한화 3루수", stats=[st("홈런", "29개", 0), st("타점", "96개", 0)], asof=AS)),
 ("제 예상은 당연히 김도영", pv("김도영C", "제 예상 · 3루수", [vstamp("준플레이오프 1차전 홈런 2개", 1, "gold", size=44)], chain="kdy2")),
 ("물론 골든글러브는", pv("김도영C", "제 예상 · 3루수", [vstamp("투표는 정규시즌 성적만", 0, "gold", size=46)], chain="kdy2", cont=True)),
 # 67~78 유격수
 ("유격수는 후보 7명", toc(6, text="유격수 후보 7명")),
 ("SSG 박성한은", pv("박성한A", PSH, stats=[st("타율", "3할 3푼", 1, hi=True), st("안타", "175개", 1), st("출루율", "4할 2푼 9리", 2), st("출장", "전 경기", 0, hi=True, hold=True)], chain="psh", asof=AS)),
 ("개막하고 22경기", pv("박성한A", PSH, [vstamp("개막 뒤 22경기 연속 안타", 0, "gold", size=46)], [st("타율", "3할 3푼", -1, hi=True), st("안타", "175개", -1), st("출루율", "4할 2푼 9리", -1), st("출장", "전 경기", 0, hi=True, hold=True)], chain="psh", cont=True, asof=AS)),
 ("박성한은 9월 말", pv("박성한A", PSH, [hid(vstamp("개막 뒤 22경기 연속 안타", 0, "gold", size=46)), vq("9월 30일 · 엑스포츠뉴스", "“다치지 않고 전 경기에\n출전하는 것이 목표다”", 1)], [st("타율", "3할 3푼", -1, hi=True), st("안타", "175개", -1), st("출루율", "4할 2푼 9리", -1), st("출장", "전 경기", 2, hi=True)], chain="psh", cont=True, asof=AS)),
 ("한 시즌 269번", S(0, "bars", title="유격수 한 시즌 출루", items=[dict(label="박성한", sub="2026년", img=PF("박성한"), team="SSG", value=269, unit="번", at=0, hi=True)], max=270, chain="ob", text="유격수 한 시즌 최다", textAt=1)),
 ("이전 기록은", S(0, "bars", title="유격수 한 시즌 출루", items=[dict(label="박성한", sub="2026년", img=PF("박성한"), team="SSG", value=269, unit="번", at=-1, hi=True),
     dict(label="이전 1위", sub="1994년", value=253, unit="번", at=1, color=NV)], max=270, chain="ob", cont=True, text="유격수 한 시즌 최다")),
 ("이숭용 감독도", sp("이숭용", "SSG 감독", [bub("10월 11일 · 엑스포츠뉴스 · 요약", "“올해는 성한이가 꼭\n받아야 하지 않을까”", 1)])),
 ("NC 김주원은", pv("김주원A", "NC 유격수 · 지난해 수상", stats=[st("홈런", "18개", 1, hi=True), st("도루", "30개", 1, hi=True)], chain="kjw", asof=AS)),
 ("다만 타율은 2할 8푼", fo("유격수 비교", side("박성한B", "SSG 유격수"), side("김주원B", "NC 유격수"),
     [dict(k="타율", l="3할 3푼", r="2할 8푼", lv=.330, rv=.280, at=0)], chain="ss")),
 ("김주원은 /", pv("김주원A", "NC 유격수 · 지난해 수상", [vq("9월 29일 · 일간스포츠 · 요약", "“성한이 형이 잘하고 있어서\n하늘에 맡기겠다”", 1)])),
 ("2024년 수상자 두산 박찬호", pv("박찬호", "두산 유격수 · 2024년 KIA에서 수상", stats=[st("타율", "2할 8푼 3리", 1), st("도루", "33개", 1)], asof=AS)),
 ("제 예상은 박성한", fo("유격수 비교", side("박성한B", "SSG 유격수"), side("김주원B", "NC 유격수"),
     [dict(k="타율", l="3할 3푼", r="2할 8푼", lv=.330, rv=.280, at=-1), dict(k="골든글러브", l="아직 없음", r="2025년 수상", at=1)], chain="ss", cont=True, text="제 예상 · 박성한", textAt=0)),
 # 79~102 외야수
 ("이제 오늘의 메인", toc(7, text="외야수 후보 21명")),
 ("55도루로", ppl("외야수 후보 21명 중", [("황성빈", "롯데 · 도루왕 55개"), ("나성범", "KIA · 31홈런")], ats=[0, 1])),
 ("올해는 네 명의 기록이", of4(say=True, sayAt=0)),
 ("첫 번째는", pv("구자욱A", "삼성 외야수", [vstamp("생애 첫 타격왕", 3, "gold", size=50)], [st("타율", "3할 7푼 1리", 2, hi=True)], chain="kja", asof=AS)),
 ("출루율도", pv("구자욱A", "삼성 외야수", [vstamp("생애 첫 타격왕", -1, "gold", size=50)], [st("출루율", "4할 5푼 8리 · 1위", 0, hi=True), st("홈런", "15개", 1), st("타점", "102개", 1)], chain="kja", cont=True, asof=AS)),
 ("구자욱은 타격왕 경쟁", pv("구자욱A", "삼성 외야수", [hid(vstamp("생애 첫 타격왕", -1, "gold", size=50)), vq("9월 7일 · 스포츠경향 · 요약", "“타율 꼴찌라도\n팀이 1위인 게 맞다”", 1)], [hid(st("출루율", "4할 5푼 8리 · 1위", 0, hi=True)), hid(st("홈런", "15개", 1)), hid(st("타점", "102개", 1))], chain="kja", cont=True, asof=AS)),
 ("두 번째는", pv("레이예스A", "롯데 외야수", [vstamp("한 시즌 최다 안타 신기록", 3, "gold", size=46)], [st("안타", "211개", 2, hi=True)], chain="ry", asof=AS)),
 ("타율도 3할 6푼 3리", pv("레이예스A", "롯데 외야수", [vstamp("한 시즌 최다 안타 신기록", -1, "gold", size=46)], [st("타율", "3할 6푼 3리", 0), st("홈런", "18개", 1), st("타점", "109개", 1)], chain="ry", cont=True, asof=AS)),
 ("레이예스는 신기록을", pv("레이예스A", "롯데 외야수", [hid(vstamp("한 시즌 최다 안타 신기록", -1, "gold", size=46)), vq("10월 12일 · 일간스포츠 · 요약", "“최원준 선수에게\n고생했다고 전하고 싶다”", 2)], [hid(st("타율", "3할 6푼 3리", 0)), hid(st("홈런", "18개", 1)), hid(st("타점", "109개", 1))], chain="ry", cont=True, asof=AS)),
 ("세 번째는", pv("최원준A", "KT 외야수", [vstamp("득점왕", 2, "gold", size=54)], [st("안타", "208개", 2), st("득점", "125개", 2, hi=True)], chain="cwj", asof=AS)),
 ("208안타는", pv("최원준A", "KT 외야수", [vstamp("국내 선수 한 시즌 최다 안타", 1, "gold", size=44)], [st("안타", "208개", -1), st("득점", "125개", -1, hi=True), st("타율", "3할 5푼 6리", 2)], chain="cwj", cont=True, asof=AS)),
 ("네 번째는", pv("힐리어드A", "KT 외야수", [vstamp("타점왕", 3, "gold", size=54)], [st("홈런", "44개", 2), st("타점", "139개", 2, hi=True)], chain="hl", asof=AS)),
 ("홈런왕 경쟁도", pv("힐리어드A", "KT 외야수", [vstamp("정규시즌 1위 KT", 1, "gold", size=50)], [st("홈런", "44개 · 2위", 0), st("타점", "139개", -1, hi=True)], chain="hl", cont=True, asof=AS)),
 ("힐리어드는 마지막 경기를", pv("힐리어드A", "KT 외야수", [hid(vstamp("정규시즌 1위 KT", 1, "gold", size=50)), vq("10월 11일 · 스포츠경향 · 요약", "“김도영이 홈런왕이 돼도\n진심으로 축하할 것”", 1)], [hid(st("홈런", "44개 · 2위", 0)), hid(st("타점", "139개", -1, hi=True))], chain="hl", cont=True, asof=AS)),
 ("그런데 자리는 셋", of4(say=True, sayAt=0, text="자리는 3개 · 1명은 탈락", textAt=0.5)),
 ("약점도 하나씩", S(0, "bars", title="출장 경기 · 2026", items=[dict(label=n, img=GP[n], team=TM[n], value=v, unit="경기", at=0, hi=(n == "구자욱"), color=(RED if n == "구자욱" else NV)) for n, v in [("레이예스", 144), ("힐리어드", 142), ("최원준", 140), ("구자욱", 114)]], max=144, chain="ofw", asof=AS)),
 ("힐리어드는 타율", S(0, "bars", title="타율 · 2026", items=[dict(label=n, img=GP[n], team=TM[n], value=v, note=t, at=0, hi=(n == "힐리어드"), color=(RED if n == "힐리어드" else NV)) for n, v, t in [("레이예스", .363, "3할 6푼 3리"), ("힐리어드", .304, "3할 4리"), ("최원준", .356, "3할 5푼 6리"), ("구자욱", .371, "3할 7푼 1리")]], max=.371, chain="ofw", cont=True, asof=AS)),   # 10/18 사용자: 같은 4명이면 사진·이름 그대로, 막대·숫자만
 ("최원준은 홈런이 9개", pv("최원준T", "KT 외야수", stats=[st("홈런", "9개 · 4명 중 가장 적음", 0)], chain="bat", asof=AS)),
 ("시즌 막판엔 볼넷", pv("최원준T", "KT 외야수", [vq("10월 11일 삼성전 · 뉴스1 사진", "볼넷 뒤 방망이 투척", 0, src=True)], chain="bat", cont=True)),
 ("팬들은 /", pv("최원준T", "KT 외야수", [vq("10월 11일 삼성전 · 뉴스1 사진", "볼넷 뒤 방망이 투척", 0, src=True), vq("10월 11일 · 노컷뉴스 · 팬 반응 · 요약", "“개인 기록에 연연하는\n모습이 아쉽다”", 1, src=True)], chain="bat", cont=True)),
 ("제 예상은 / 구자욱", S(0, "facegrid", title="제 예상 · 외야수 3명", cols=4, items=[dict(img=GP2["구자욱"], name="구자욱", team="삼성", hi=True, at=1), dict(img=GP2["레이예스"], name="레이예스", team="롯데", hi=True, at=1.3), dict(img=GP2["힐리어드"], name="힐리어드", team="KT", hi=True, at=1.6), dict(img=GP2["최원준"], name="최원준", team="KT", dim=True, at=1)], chain="ofp", size=60)),
 ("득점왕보다는", S(0, "facegrid", title="제 예상 · 외야수 3명", cols=4, items=[dict(img=GP2["구자욱"], name="구자욱", team="삼성", hi=True, say="타격왕", sayAt=1), dict(img=GP2["레이예스"], name="레이예스", team="롯데", hi=True, say="최다 안타 신기록", sayAt=1.3), dict(img=GP2["힐리어드"], name="힐리어드", team="KT", hi=True, say="타점왕", sayAt=1.6), dict(img=GP2["최원준"], name="최원준", team="KT", dim=True, say="득점왕", sayAt=0)], chain="ofp", cont=True, size=60)),
 ("최원준에게는", pv("최원준C", "KT 외야수", [vstamp("208안타에도 탈락?", 2, "bad", size=54)])),
 ("이대호도 자기 유튜브에서", sp("이대호", "KBO 레전드 · 예측", [bub("10월 6일 · 유튜브 ‘이대호 [RE:DAEHO]’", "외야 예상\n힐리어드 · 레이예스 · 최원준", 1, src=True)])),
 # 103~112 지명타자
 ("마지막 지명타자", toc(8, text="지명타자 후보 3명")),
 ("삼성 최형우, 한화 강백호", S(0, "people", ph=420, title="지명타자 후보 3명", items=[dict(img=P["최형우A"], name="최형우", note="삼성", at=0), dict(img=P["강백호A"], name="강백호", note="한화", at=0.5), dict(img=P["김재환"], name="김재환", note="SSG · 24홈런", at=1)])),
 ("한화 강백호는", pv("강백호B", "한화 지명타자", stats=[st("홈런", "34개 · 4위", 0, hi=True), st("타점", "118개 · 공동 4위", 0, hi=True)], chain="kbh", asof=AS)),
 ("강백호는 9월에", pv("강백호B", "한화 지명타자", [vq("9월 9일 · 머니투데이", "“아직 전성기는 안 왔다고 생각한다”", 1)], [hid(st("홈런", "34개 · 4위", 0, hi=True)), hid(st("타점", "118개 · 공동 4위", 0, hi=True))], chain="kbh", cont=True, asof=AS)),
 ("삼성 최형우는", pv("최형우B", "삼성 지명타자 · 지난해 수상", stats=[st("타율", "3할 1리", 0), st("홈런", "18개", 1), st("타점", "106개", 1)], chain="chw", asof=AS)),
 ("올해도 받으면", pv("최형우B", "삼성 지명타자 · 지난해 수상", [vstamp("또 받으면 최고령 수상 기록 경신", 1, "gold", size=44)], [st("타율", "3할 1리", -1), st("홈런", "18개", -1), st("타점", "106개", -1)], chain="chw", cont=True, asof=AS)),
 ("통산 9번째", pv("최형우B", "삼성 지명타자 · 지난해 수상", [vstamp("통산 9번째 · 역대 단독 3위", 0, "gold", size=46)], [st("타율", "3할 1리", -1), st("홈런", "18개", -1), st("타점", "106개", -1)], chain="chw", cont=True, asof=AS)),
 ("제 예상은 강백호", fo("지명타자 비교", side("강백호A", "한화 지명타자"), side("최형우A", "삼성 지명타자"),
     [dict(k="홈런", l="34개", r="18개", lv=34, rv=18, at=1), dict(k="타점", l="118개", r="106개", lv=118, rv=106, at=1)], chain="dh", text="제 예상 · 강백호", textAt=0)),
 ("강백호는 2020년과", pv("강백호B", "한화 지명타자", [vstamp("지명타자로는 첫 수상 도전", 2, "gold", size=46)], [st("골든글러브", "2020 · 2021년 1루수(KT)", 0)])),
 ("그래도 최형우의", pv("최형우A", "삼성 지명타자", [vstamp("최고령 수상 기록 도전", 0, "gold", size=50)])),
 # 113~119 정리
 ("마지막으로 정리해", toc(9)),
 # 10/18 사용자 "여기는 전부 프로필 사진으로 해줘. 그리고 포지션별로 나눠줘" → 요약판만 구단 프로필 + pos 이름표(외야 3명 한 이름표). 10/18 밤: 이름을 부르는 호흡에 그 사람이 뜬다(at)
 ("투수 곽빈, 포수 허인서", S(0, "facegrid", title="제 예상 · 2026 골든글러브", cols=5, profile=True, items=[dict(x, at=a) for x, a in zip(SUM10[:4], [0, 0.5, 1, 1.5])], chain="sum", size=44)),
 ("3루 김도영, 유격 박성한", S(0, "facegrid", title="제 예상 · 2026 골든글러브", cols=5, profile=True, items=[dict(x, at=-1) for x in SUM10[:4]] + [dict(x, at=a) for x, a in zip(SUM10[4:6], [0, 0.5])], chain="sum", cont=True, size=44)),
 ("외야 구자욱, 레이예스", S(0, "facegrid", title="제 예상 · 2026 골든글러브", cols=5, profile=True, items=[dict(x, at=-1) for x in SUM10[:6]] + [dict(x, at=a) for x, a in zip(SUM10[6:], [0, 0.3, 0.6, 1])], chain="sum", cont=True, size=44)),
 ("수상자는 12월 8일 / 시상식에서", S(0, "facegrid", title="제 예상 · 2026 골든글러브", cols=5, profile=True, items=[dict(x, at=-1) for x in SUM10], chain="sum", cont=True, size=44, text="12월 8일 시상식에서 공개", textAt=0)),
 ("여러분 예상은", of4(say=True, sayAt=0, text="외야수 · 누가 떨어질까요?", textAt=1)),
 ("구자욱, 레이예스, 최원준, 힐리어드 / 한 명만", of4(say=True, sayAt=0, text="외야수 · 누가 떨어질까요?", textAt=0.3, cont=True)),   # 9/27 규칙: 화면에 '댓글로…' 문구 금지(나레이션만) — 앞 장면 문구 그대로
]
assert len(SCN) == len(LINES) - 1, (len(SCN), len(LINES))
for j, (pre, sc) in enumerate(SCN):
    assert LINES[j][0].startswith(pre) or pre in LINES[j][0][:60], (j, pre, LINES[j][0][:40])

CH = [{"key": "뽑는 법", "title": "뽑는 법", "from": 5, "to": 14},
      {"key": "투수", "title": "투수", "from": 15, "to": 27},
      {"key": "포수", "title": "포수", "from": 28, "to": 38},
      {"key": "1루수", "title": "1루수", "from": 39, "to": 49},
      {"key": "2루수", "title": "2루수", "from": 50, "to": 57},
      {"key": "3루수", "title": "3루수", "from": 58, "to": 66},
      {"key": "유격수", "title": "유격수", "from": 67, "to": 78},
      {"key": "외야수", "title": "외야수", "from": 79, "to": 102},
      {"key": "지명타자", "title": "지명타자", "from": 103, "to": 112},
      {"key": "정리", "title": "정리", "from": 113, "to": 119}]

lines, scenes = [], []
for j, (t, _, _) in enumerate(LINES[:-1]):
    sc = dict(SCN[j][1]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})

TAGS = ["골든글러브", "2026 골든글러브", "골든글러브 예상", "골든글러브 후보", "KBO 골든글러브", "프로야구 골든글러브", "외야수 골든글러브", "구자욱", "레이예스", "최원준", "힐리어드",
        "김도영", "곽빈", "허인서", "오스틴", "디아즈", "박민우", "박성한", "김주원", "강백호", "최형우", "올러", "네일", "이대호", "프로야구", "KBO", "2026 프로야구", "야구자판기"]
DESC = ("2026 KBO 골든글러브 후보 79명이 10월 17일 발표됐어요. 투수부터 지명타자까지 8개 포지션(수상자 10명, 외야수 3명)의 후보와 기록을 정리하고, 포지션마다 누가 받을지 예상했어요.\n\n"
        "가장 뜨거운 자리는 외야수예요. 타격왕 구자욱(삼성), 한 시즌 최다 안타 신기록 211안타 레이예스(롯데), 득점왕 최원준(KT), 타점왕 힐리어드(KT) 네 명이 모두 타이틀을 가져갔지만 외야 골든글러브는 세 자리뿐이에요.\n\n"
        "포수는 2011년부터 이어진 양의지·강민호 시대가 끝나고, 20홈런을 친 한화 허인서가 새 주인을 노려요. 1루는 OPS 1위 오스틴과 지난해 수상자 디아즈, 유격수는 박성한과 김주원의 싸움이에요.\n\n"
        "영상 속 수상자 예상은 모두 야구자판기의 예상이에요. 수상자는 12월 8일 시상식에서 공개돼요.\n\n"
        "야구자판기는 매일 오늘의 야구 이슈를 정리해 드려요.\n\n"
        "외야수 네 명 중 누가 떨어질까요? 한 명만 댓글로 골라 주세요.\n\n"
        "기록 출처: KBO 보도자료 「2026 신한 SOL KBO 골든글러브 후보 발표」(10/17, 후보 명단·정규시즌 기록), 스포티비뉴스·MHN·뉴스1·서울신문·세계일보·파이낸셜뉴스·엑스포츠뉴스·스포츠경향·OSEN·일간스포츠·데일리안·오마이스타·아주경제·스포탈코리아 기사\n인터뷰·반응 출처: KBS(곽빈 8/8), 서울신문(허인서 10/13), SPOTV뉴스(오스틴 10/7), 스포츠경향(박민우 9/10·김도영 10/12·구자욱 9/7·힐리어드 10/11), 일간스포츠(레이예스 10/12·김주원 9/29), 엑스포츠뉴스(박성한 9/30·이숭용 감독 10/11), 머니투데이(강백호 9/9), 노컷뉴스(팬 반응 10/11), 유튜브 '이대호 [RE:DAEHO]'(10/6)\n"
        "사진 출처: SSG 랜더스 제공, 한화 이글스 제공, NC 다이노스 제공, 삼성 라이온즈 제공, 롯데 자이언츠 제공, KIA 타이거즈 제공, KT 위즈 제공, LG 트윈스 제공, 두산 베어스 제공, 스타뉴스, 엑스포츠뉴스, 스포츠투데이, 스포티비뉴스, 스포츠서울, 일간스포츠, 노컷뉴스, 스포츠조선, 스포츠경향, 동아일보, OSEN, 뉴시스, 연합뉴스, 뉴스1, 각 구단 공식 프로필")
SOURCE = ("사실 출처 = KBO 보도자료 「2026 신한 SOL KBO 골든글러브 후보 발표」 별첨(10/17, 후보 명단·정규시즌 기록) + 기사 본문(스포티비뉴스·MHN·뉴스1·서울신문·엑스포츠뉴스·스포츠경향·OSEN·일간스포츠·다음 야구기록소) — "
          "근거 표·검수 3회 기록: 프로젝트 claude/1018-롱폼18-골든글러브-대사v4.md. "
          "기록 출처: KBO 보도자료(2026 골든글러브 후보·정규시즌 기록) / 사진 출처: SSG 랜더스 제공, 한화 이글스 제공, NC 다이노스 제공, 삼성 라이온즈 제공, 롯데 자이언츠 제공, KIA 타이거즈 제공, KT 위즈 제공, LG 트윈스 제공, 두산 베어스 제공, 스타뉴스, 엑스포츠뉴스, 스포츠투데이, 스포티비뉴스, 스포츠서울, 일간스포츠, 노컷뉴스, 스포츠조선, 스포츠경향, 동아일보, OSEN, 뉴시스, 연합뉴스, 각 구단 공식 프로필")

EP = {"date": "2026-10-18", "gameDate": "2026-10-17", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1018-long18-v8", "topic": "골든글러브예상", "endcardSec": 10, "chapNoNum": True, "introChapter": "외야 4명 중 1명 탈락",
      "gapScale": 1.05, "pauseMax": 0.4, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "source": SOURCE,
      "youtube": {"title": "2026 골든글러브 예상 | 외야 4명 중 1명은 떨어진다, 구자욱 레이예스 최원준 힐리어드 #골든글러브 #프로야구",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#골든글러브", "#프로야구", "#KBO", "#구자욱", "#레이예스", "#최원준", "#힐리어드", "#김도영", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 27, 38, 49, 57, 66, 78, 101, 112, 118, 119}
    HOLD = {1: 0.45, 4: 0.5, 14: 0.6, 27: 0.6, 38: 0.6, 49: 0.6, 57: 0.6, 66: 0.6, 78: 0.6, 102: 0.6, 112: 0.6, 117: 0.5}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-18_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
    # 10/18 사용자 규칙(사진 종류 통일·이모지 대신 그림·줄바꿈·같은 틀 안 움직임·소형준 가운데) 자동 검사 — 위반이 있으면 렌더하지 말 것
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import rule_check
    _b = rule_check.check(EP)
    for _i, _r, _m in _b: print(('확인 필요' if _r.startswith('R4') else '규칙 위반'), '장면', _i, _r, '|', _m)
    print('규칙 검사', '통과' if not [x for x in _b if not x[1].startswith('R4')] else '위반 있음 — 렌더 금지')
