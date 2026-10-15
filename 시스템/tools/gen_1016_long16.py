# -*- coding: utf-8 -*-
"""10/16 롱폼⑯ 「프로야구 FA 2026 — 올겨울 FA 대어 몸값 예상 순위」 (음성 API · 줄별 배속).
대사 = tools/text_1016_long16.py (1차 원문 대조 · 2차 반박 검수 · 3차 재검 반영). 나레이션 앞처리 = tools/narr_1016.py.
근거 = 프로젝트 claude/1014-롱폼15-FA몸값예상-최종확정·KBO기록실 + 10/15 밤 조사(검수 기록: claude/1016-롱폼16-FA대어몸값-대사.md).
장면: 몸값 눈금(pricebar)·정리 표(pricerows)·보상 등급(compgrade)·보상 흐름(comptrans)·날짜 줄(tline) = tools/scenes_fa_1016.js(inject_fa_1016.py).
사진: 인물 카드는 전부 경기 사진(카드/F16_*, person_card 0.774), 몸값 눈금의 얼굴 원은 전부 구단 공식 프로필(KBO프로필)."""
import json, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1016_long16.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
import narr_1016
def narr_of(t): return narr_of15(narr_1016.pre(t))
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vduo(items, **k): return dict(type="duo", items=items, **k)
RED, GOLD, GRAY = "#E5484D", "#E8A100", "#8A93A3"
K, F = '카드/F16_', 'KBO프로필/'
P = {  # 경기 사진 카드 — 같은 선수는 장면마다 다른 사진(같은 사람 묶음 안에서만 이어 씀)
    "정수빈A": K + "정수빈_A", "정수빈B": K + "정수빈_B", "박해민": K + "박해민",
    "박동원A": K + "박동원_A", "박동원B": K + "박동원_B", "장성우": K + "장성우",
    "김호령A": K + "김호령_A", "김호령B": K + "김호령_B", "이범호": K + "이범호",
    "홍창기A": K + "홍창기_A", "홍창기B": K + "홍창기_B", "홍창기C": K + "홍창기_C", "차명석": K + "차명석",
    "최원준A": "카드/R13_최원준_미소", "최원준B": "카드/FA10_최원준_204",
    "최지훈A": K + "최지훈_A", "최지훈B": K + "최지훈_B", "배정대": K + "배정대",
    "원태인A": K + "원태인_A", "원태인C": K + "원태인_C", "원태인D": K + "원태인_D", "박진만": K + "박진만", "최원태": K + "최원태",
    "구자욱A": K + "구자욱_A", "구자욱H": K + "구자욱_H", "구자욱B": K + "구자욱_B", "구자욱C": K + "구자욱_C", "김재환": "카드/FA10_김재환_결승포",
    "양의지A": K + "양의지_A", "양의지B": K + "양의지_B",
}
PR = {  # 공식 프로필(얼굴 원)
    "강백호": F + "강백호_2026FA10", "박해민": F + "박해민_2026FA10", "김현수": F + "김현수_2026프로필", "강민호": F + "강민호_2026FA10",
    "장성우": F + "장성우_2026KT", "최원준": F + "최원준_2026프로필", "최원태": F + "최원태_2026삼성", "엄상백": F + "엄상백", "고영표": F + "고영표_2024KT",
    "김재환": F + "김재환_2026FA10", "최정": F + "최정_상체",
    "정수빈": F + "정수빈", "박동원": F + "박동원", "김호령": F + "김호령", "홍창기": F + "홍창기", "최지훈": F + "최지훈", "원태인": F + "원태인", "구자욱": F + "구자욱",
}
TM = {"강백호": "한화", "박해민": "LG", "김현수": "KT", "강민호": "삼성", "장성우": "KT", "최원준": "KT", "최원태": "삼성", "엄상백": "한화", "고영표": "KT", "김재환": "SSG", "최정": "SSG",
      "정수빈": "두산", "박동원": "LG", "김호령": "KIA", "홍창기": "LG", "최지훈": "SSG", "원태인": "삼성", "구자욱": "삼성", "양의지": "두산"}
def mk(name, v, at, row=0, sub="", **x): return dict(dict(v=v, name=name, img=PR[name], team=TM[name], at=at, row=row, sub=sub), **x)
def gh(name, v, at, row=0, vt=None): return dict(v=v, name=name, vt=vt or f"{v}억", at=at, row=row, ghost=True)
def bd(name, a, b, tag, at): return dict(name=name, img=PR[name], team=TM[name], **{"from": a, "to": b}, tag=tag, label=f"{a}억~{b}억", at=at)
def pb(chain, title, marks=(), bands=(), **k): return S(0, "pricebar", title=title, marks=list(marks), bands=list(bands), chain=chain, max=150, **k)
def pv(img, name, sub, viz=(), stats=(), **k): return S(0, "pstat", img=P[img], team=TM.get(name), name=name, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, **k)
def sp(img, name, sub, bubbles, **k): return S(0, "speech", img=P[img], name=name, sub=sub, bubbles=bubbles, **k)
def bub(date, text, at, src=False): return dict(date=date, text=text, at=at, src=src)
def fo(title, L_, R_, rows, **k): return S(0, "faceoff", title=title, left=L_, right=R_, rows=rows, **k)
def side(img, name, role): return {"img": P[img], "name": name, "team": TM.get(name), "role": role}
AS = "2026 정규시즌 최종"
GA = dict(g="A", opt=[dict(bills=2, person=True), dict(bills=3)])
GB = dict(g="B", opt=[dict(bills=1, person=True), dict(bills=2)])
GC = dict(g="C", opt=[dict(bills=1.5)])
def hid(d): return dict(d, hide=True)
RANK = [("1위", "구자욱", 110, 140), ("2위", "원태인", 70, 100), ("3위", "최지훈", 55, 75), ("4위", "홍창기", 40, 60), ("5위", "김호령", 25, 40), ("6위", "박동원", 20, 36), ("7위", "정수빈", 15, 30)]
def rows7(show, at0=0.0, step=1.0):
    out = []
    for j, (r, n, a, b) in enumerate(RANK):
        d = dict(rank=r, name=n, img=PR[n], team=TM[n], **{"from": a, "to": b}, label=f"{a}~{b}억")
        if j < show[0]: d["at"] = -1
        elif j < show[1]: d["at"] = at0 + (j - show[0]) * step
        else: d["hide"] = True
        out.append(d)
    return out

SCN = [
 # 0 훅
 ("올겨울 FA 대어들", S(0, "faces", items=[dict(img=P["구자욱H"], name="구자욱", team="삼성", note="?억", at=0), dict(img=P["원태인C"], name="원태인", team="삼성", note="?억", at=0.2), dict(img=P["최지훈A"], name="최지훈", team="SSG", note="?억", at=0.4), dict(img=P["홍창기B"], name="홍창기", team="LG", note="?억", at=0.6)])),
 ("지난겨울 100억 이상", pb("pb0", "지난겨울 100억 이상 FA 계약", [mk("강백호", 100, 1, sub="4년")], line=dict(v=100, label="100억", at=0))),
 ("해를 넘기자", pb("pb0", "지난겨울 100억 이상 FA 계약", [mk("강백호", 100, 1, sub="4년")], line=dict(v=100, label="100억", at=0), text="“이제 칼자루는 구단이”", textAt=1, cont=True)),
 ("이 영상에선", S(0, "toc", on=-1, itemFrom=99)),
 # 기본 규칙
 ("먼저 FA가", S(0, "icontiles", title="FA = 자유계약선수", items=[dict(icon="calendar", v="정해진 기간", k="다 채우면", at=1), dict(icon="search", v="10개 구단", k="누구와도 계약", at=2)])),
 ("FA 명단은", S(0, "tline", title="FA 명단이 나오기까지", items=[dict(d="지금", t="정규시즌 끝", at=0), dict(d="11월 2일", t="한국시리즈 시작", at=2, c="gold"), dict(d="끝나고 5일 안", t="FA 명단 공시", at=0.6, c="good", big=True)], text="지금은 예비 FA", textAt=4)),
 ("FA 몸값을 볼 때", S(0, "comptrans", title="FA 보상", moveAt=3, backAt=4)),
 ("보상은 등급마다", S(0, "compgrade", title="FA 보상 등급", cols=[dict(GA, at=1), hid(GB), hid(GC)], chain="cg", hi="A")),
 ("B등급은 연봉만큼과", S(0, "compgrade", title="FA 보상 등급", cols=[dict(GA, at=-1), dict(GB, at=0), dict(GC, at=2)], chain="cg", cont=True)),
 ("등급은 아직 공시 전", S(0, "compgrade", title="FA 보상 등급", cols=[dict(GA, at=-1), dict(GB, at=-1), dict(GC, at=-1)], chain="cg", cont=True, text="등급 · 몸값 = 전부 예상", textAt=2)),
 # 7위 정수빈
 ("일곱 번째는", pv("정수빈A", "정수빈", "두산 중견수 · 7위", [])),
 ("정수빈은 2026년", pv("정수빈A", "정수빈", "두산 중견수 · 7위", [], [st("2026 정규시즌", "142경기", 0), st("타율", "2할 5푼 3리", 1), st("도루", "20개", 2), st("중견수 선발", "129경기", 3, hi=True)], asof=AS)),
 ("정수빈 몸값의 기준은", fo("1990년생 중견수 두 명", side("정수빈B", "정수빈", "두산 · 예비 FA"), side("박해민", "박해민", "LG · 지난겨울 FA"),
     [dict(k="나이", l="1990년생", r="1990년생", at=3), dict(k="포지션", l="중견수", r="중견수", at=4), dict(k="지난겨울 계약", l="?", r="4년 65억", at=1, w="r")], chain="jsb")),
 ("다만 박해민은", pb("pb1", "박해민 · 지난겨울 FA", [mk("박해민", 65, 0, sub="4년"), gh("KT 제안", 75, 1, row=1, vt="65억 + 10억 이상")])),
 ("보상 등급은 같아요", fo("1990년생 중견수 두 명", side("정수빈B", "정수빈", "두산 · 예비 FA"), side("박해민", "박해민", "LG · 지난겨울 FA"),
     [dict(k="FA", l="두 번째", r="두 번째", at=2), dict(k="보상 등급", l="B등급(예상)", r="B등급", at=3)])),
 ("하지만 박해민은 계약 직전", S(0, "bars", title="도루 개수", items=[dict(label="박해민", sub="2025년 · 도루왕 · 수비상", img=PR["박해민"], team="LG", value=49, unit="개", at=0, hi=True),
     dict(label="정수빈", sub="2024년", img=PR["정수빈"], team="두산", value=52, unit="개", at=4, color="#3B4A63"), dict(label="정수빈", sub="2025년", img=PR["정수빈"], team="두산", value=26, unit="개", at=5, color="#8A93A3"),
     dict(label="정수빈", sub="2026년", img=PR["정수빈"], team="두산", value=20, unit="개", at=6, color=RED)], max=55)),
 ("정수빈은 10월에", sp("정수빈A", "정수빈", "두산 중견수", [bub("10월", "“여유 있게 4년 계약해주시면\n감사하겠다”", 1)])),
 ("박해민은 도루왕과 수비상으로", pb("pb2", "30대 FA · 지난겨울 계약 기간", [mk("박해민", 65, 0, row=0, sub="4년"), mk("김현수", 50, 3, row=1, sub="3년 · 만 37"), mk("강민호", 20, 4, row=0, sub="2년 · 만 40")])),
 ("그래서 제 예상은 / 2~3년 계약에 / 15억", pb("pb2", "30대 FA · 지난겨울 계약 기간", [mk("박해민", 65, 0, row=0, sub="4년"), mk("김현수", 50, 3, row=1, sub="3년 · 만 37"), mk("강민호", 20, 4, row=0, sub="2년 · 만 40")],
     [bd("정수빈", 15, 30, "7위", 1)], cont=True)),
 # 6위 박동원
 ("여섯 번째는", pv("박동원A", "박동원", "LG 포수 · 6위", [])),
 ("박동원은 2024년", pv("박동원A", "박동원", "LG 포수 · 6위", [vtrend([dict(x="2024년", v=20, vt="20홈런", at=0), dict(x="2025년", v=22, vt="22홈런", at=1), dict(x="2026년", v=14, vt="14홈런", c="bad", at=4)], title="홈런")],
     [st("2026 타율", "2할 2푼 5리", 3)], asof=AS)),
 ("그래도 LG에서", pv("박동원A", "박동원", "LG 포수 · 6위", [vtrend([dict(x="2024년", v=20, vt="20홈런", at=-1), dict(x="2025년", v=22, vt="22홈런", at=-1), dict(x="2026년", v=14, vt="14홈런", c="bad", at=-1)], title="홈런")],
     [st("2026 타율", "2할 2푼 5리", -1), st("포수 선발 · LG 1위", "102경기", 0.5, hi=True)], asof=AS)),
 ("비교할 계약은 / 지난겨울 만 36살", pb("pb3", "30대 포수 · 지난겨울 FA", [mk("장성우", 16, 2, row=0, sub="2년 · 만 36"), mk("강민호", 20, 4, row=1, sub="2년 · 만 40")])),
 ("장성우는 계약 직전", fo("장성우 계약 직전 vs 박동원 2026", side("장성우", "장성우", "KT · 2025년"), side("박동원B", "박동원", "LG · 2026년"),
     [dict(k="타율", l="2할 4푼 7리", r="2할 2푼 5리", lv=.247, rv=.225, at=1), dict(k="홈런", l="14개", r="14개", lv=14, rv=14, at=1.5), dict(k="나이", l="만 36", r="만 36", at=3)])),
 ("그리고 포수는", S(0, "tiles", title="포수 한 명이 90경기 이상 선발 · 2026", items=[dict(team=t, v=v, k="", dim=(t in ("두산", "KIA")), at=(2 if t not in ("두산", "KIA") else 4)) for t, v in
     [("KT", "104"), ("삼성", "90"), ("LG", "102"), ("SSG", "103"), ("롯데", "112"), ("NC", "105"), ("한화", "104"), ("키움", "93"), ("두산", "78"), ("KIA", "74")]], vsize=60, text="10개 구단 중 8곳", textAt=4)),
 ("그래서 제 예상은 / 2~3년 계약에 / 20억", pb("pb3", "30대 포수 · 지난겨울 FA", [mk("장성우", 16, -1, row=0, sub="2년 · 만 36"), mk("강민호", 20, -1, row=1, sub="2년 · 만 40")], [bd("박동원", 20, 36, "6위", 1)], cont=True)),
 # 5위 김호령
 ("다섯 번째는", pv("김호령A", "김호령", "KIA 중견수 · 5위", [])),
 ("김호령은 2024년", pv("김호령A", "김호령", "KIA 중견수 · 5위", [vtrend([dict(x="2024년", v=64, vt="64경기", c="bad", at=1), dict(x="2026년", v=141, vt="141경기", c="good", at=4)], title="출장 경기")],
     [st("2024 타율", "1할 3푼 6리", 2), st("2026", "13홈런 17도루", 5, hi=True)], asof=AS)),
 ("이범호 감독은", S(0, "faces", items=[dict(img=P["이범호"], name="이범호", team="KIA", role="KIA 감독", at=0), dict(img=P["김호령B"], name="김호령", team="KIA", role="KIA 중견수", at=2, say="“감독님이 하루에 한 번씩은\n무조건 하신다”", sayAt=3)])),
 ("하지만 김호령은 에이전트가", sp("김호령B", "김호령", "KIA 중견수", [bub("보도", "에이전트가 없어서\n비FA 다년계약은 쉽지 않을 전망", 0, src=True)])),
 ("비교 대상은 / 박해민의 65억과", pb("pb4", "중견수 · 지난겨울 FA", [mk("박해민", 65, 1, row=1, sub="4년 · 만 35"), mk("최원준", 48, 2, row=0, sub="4년 · 만 28")])),
 ("대신 보상 부담이 작아요", pv("김호령A", "김호령", "KIA 중견수 · 5위", [vduo([dict(k="2026 연봉", v="2억 5천만", at=3), dict(k="보상금 최대", v="5억", at=4, c="good")])], [st("예상 등급", "B 또는 C", 0)])),
 ("그래서 제 예상은 / 3년 안팎", pb("pb4", "중견수 · 지난겨울 FA", [mk("박해민", 65, -1, row=1, sub="4년 · 만 35"), mk("최원준", 48, -1, row=0, sub="4년 · 만 28")], [bd("김호령", 25, 40, "5위", 1)], cont=True)),
 # 4위 홍창기
 ("네 번째는", pv("홍창기A", "홍창기", "LG 외야수 · 4위", [])),
 ("홍창기는 2024년", pv("홍창기A", "홍창기", "LG 외야수 · 4위", [], [st("2024 출루율", "4할 4푼 7리", 1, hi=True), st("2024", "출루왕", 2), st("시즌 전 기자 전망", "5년 100억대", 3)])),
 ("그런데 2026년엔 / 타율 2할 3푼 9리", pv("홍창기B", "홍창기", "LG 외야수 · 4위", [vduo([dict(k="2026 타율", v="2할 3푼 9리", at=1, c="bad"), dict(k="홈런", v="0개", at=2, c="bad")])],
     [st("9월 18일 뒤 정규시즌", "16타수 0안타", 4), st("와일드카드", "4타수 0안타", 5, hi=True)], asof=AS)),
 ("비교할 계약은 / 최원준의 4년 48억", fo("최원준 계약 직전 vs 홍창기 2026", side("최원준A", "최원준", "2025년 · 4년 48억"), side("홍창기C", "홍창기", "2026년"),
     [dict(k="계약", l="4년 48억", r="?", at=1), dict(k="타율", l="2할 4푼 2리", r="2할 3푼 9리", lv=.242, rv=.239, at=3)])),
 ("다만 홍창기는 2026년에도", pv("홍창기A", "홍창기", "LG 외야수 · 4위", [vtrend([dict(x="타율", v=239, vt="2할 3푼 9리", c="bad", at=0), dict(x="출루율", v=375, vt="3할 7푼 5리", c="good", at=1)], title="2026 정규시즌")], asof=AS)),
 ("LG 차명석 단장은", sp("차명석", "차명석", "LG 단장", [bub("1월", "“홍창기를 반드시\n붙잡을 것”", 1)])),
 ("그래서 제 예상은 / 4년에 40억", pb("pb5", "외야수 · 지난겨울 FA", [mk("최원준", 48, 0, row=0, sub="4년")], [bd("홍창기", 40, 60, "4위", 1)])),
 # 3위 최지훈
 ("세 번째는", pv("최지훈A", "최지훈", "SSG 중견수 · 3위", [])),
 ("최지훈은 2026년", pv("최지훈A", "최지훈", "SSG 중견수 · 3위", [vstamp("데뷔 뒤 최다 홈런", 2, "gold", size=50)], [st("2026 정규시즌", "141경기", 0), st("홈런", "13개", 1, hi=True), st("도루", "21개", 1.3)], asof=AS)),
 ("그리고 중견수로 137경기에", S(0, "bars", title="SSG 중견수 선발 경기 · 2026", items=[dict(label="최지훈", img=PR["최지훈"], team="SSG", value=137, unit="경기", at=0, hi=True), dict(label="다음 선수", team="SSG", value=5, unit="경기", at=3, color=GRAY)], max=140, asof=AS)),
 ("비교 대상은 / 비슷한 나이의", fo("최원준 계약 직전 vs 최지훈 2026", side("최원준B", "최원준", "2025년 · 4년 48억"), side("최지훈B", "최지훈", "2026년"),
     [dict(k="타율", l="2할 4푼 2리", r="2할 5푼", lv=.242, rv=.250, at=3), dict(k="홈런", l="6개", r="13개", lv=6, rv=13, at=3.3)], chain="cjh", text="홈런 · 도루 · 중견수 수비", textAt=99)),
 ("최지훈은 홈런과 도루에", fo("최원준 계약 직전 vs 최지훈 2026", side("최원준B", "최원준", "2025년 · 4년 48억"), side("최지훈B", "최지훈", "2026년"),
     [dict(k="타율", l="2할 4푼 2리", r="2할 5푼", lv=.242, rv=.250, at=-1), dict(k="홈런", l="6개", r="13개", lv=6, rv=13, at=-1)], chain="cjh", cont=True, text="홈런 · 도루 · 중견수 수비", textAt=0)),
 ("최원준이 뛰는 KT의", pv("배정대", "배정대", "KT 외야수 · 예비 FA", [vstamp("이번 순위에서 제외", 3, "bad", size=50)], [st("2026 중견수 선발", "19경기", 1, hi=True)], asof=AS)),
 ("수요도 있어요", S(0, "bars", title="팀에서 중견수 선발이 가장 많은 선수 · 2026", items=[dict(label="NC", team="NC", value=53, unit="경기", at=1, color=RED), dict(label="한화", team="한화", value=40, unit="경기", at=1, color=RED),
     dict(label="키움", team="키움", value=38, unit="경기", at=1, color=RED), dict(label="KT", team="KT", value=63, unit="경기", at=4, color=GRAY, sub="최원준 4년 계약")], max=140, text="100경기도 못 채운 팀 3곳", textAt=3, asof=AS)),
 ("실제로 한화의 중견수", S(0, "speech", team="한화", name="한화", sub="중견수 고민", bubbles=[bub("보도", "중견수 FA 영입설", 0, src=True), bub("보도", "시즌 막판 팀 안의 외야수가\n새 선택지로", 3, src=True)])),
 ("그래서 제 예상은 / 4년에 55억", pb("pb6", "중견수 · 지난겨울 FA", [mk("최원준", 48, 2, row=0, sub="4년 · 만 28"), mk("박해민", 65, 3, row=1, sub="4년 · 만 35"), gh("KT 제안", 75, 3.5, row=0, vt="65억 + 10억 이상")], [bd("최지훈", 55, 75, "3위", 1)])),
 # 2위 원태인
 ("두 번째는", pv("원태인C", "원태인", "삼성 투수 · 2위", [])),
 ("원태인은 2024년 15승", pv("원태인C", "원태인", "삼성 투수 · 2위", [vtrend([dict(x="2024년", v=15, vt="15승", c="good", at=0), dict(x="2025년", v=12, vt="12승", c="good", at=1)], title="승수")], [st("2026 평균자책점", "4.52", 50, hi=True)])),
 ("그런데 2026년엔 시즌 전", pv("원태인C", "원태인", "삼성 투수 · 2위", [vtrend([dict(x="2024년", v=15, vt="15승", c="good", at=-1), dict(x="2025년", v=12, vt="12승", c="good", at=-1), dict(x="2026년", v=7, vt="7승 9패", c="bad", at=2)], title="승수")],
     [st("2026 평균자책점", "4.52", 3, hi=True)], asof=AS)),

 ("박진만 감독은", sp("박진만", "박진만", "삼성 감독", [bub("10월", "“시즌 초부터 몸 상태가\n정상과 거리가 멀었다”", 1)])),
 ("비교할 계약은 세 개예요", pb("pb7", "선발 투수 · 최근 계약", [mk("최원태", 70, 1.5, row=0, sub="4년 · FA"), mk("엄상백", 78, 3, row=1, sub="4년 · FA"), mk("고영표", 107, 5, row=0, sub="5년 · 비FA")])),
 ("최원태는 계약 직전", fo("평균자책점 · 낮을수록 좋음", side("최원태", "최원태", "계약 직전 · 2024년"), side("원태인D", "원태인", "2026년"),
     [dict(k="평균자책점", l="4.26", r="4.52", lv=4.26, rv=4.52, low=True, at=1)], text="70억이 바닥이라고 단정하기 어렵다", textAt=4, size=56)),
 ("하지만 원태인은 최근 3년 중", pv("원태인A", "원태인", "삼성 투수 · 2위", [vtrend([dict(x="2024년", v=15, vt="15승", c="good", at=0), dict(x="2025년", v=12, vt="12승", c="good", at=0), dict(x="2026년", v=7, vt="7승", c="bad", at=0)], title="승수"),
     vstamp("10승 넘게 두 번", 1, "gold", size=50)])),
 ("A등급으로 나온다면", S(0, "compgrade", title="원태인이 A등급이라면", cols=[dict(g="A", opt=[dict(bills=3)], at=0)], hi="A", text="연봉 10억 × 3배 = 보상금 최대 30억", textAt=1, size=58)),
 ("부진하기 전엔", pb("pb8", "원태인 몸값", [mk("최원태", 70, 0, sub="4년"), mk("엄상백", 78, 0, sub="4년"), gh("부진 전 전망", 100, 1, vt="100억 안팎")])),
 ("그래서 제 예상은 / 국내에", pb("pb8", "원태인 몸값", [mk("최원태", 70, -1, sub="4년"), mk("엄상백", 78, -1, sub="4년"), gh("부진 전 전망", 100, -1, vt="100억 안팎")], [bd("원태인", 70, 100, "2위", 2)], cont=True)),
 ("해외 진출은", sp("원태인A", "원태인", "삼성 투수", [bub("2025년 12월", "“무조건 가겠다는 것은 아니다”", 2), bub("8월 보도", "메이저리그 스카우트\n시즌 뒤 접촉할 뜻", 3.5, src=True)])),
 # 1위 구자욱
 ("그리고 첫 번째", pv("구자욱A", "구자욱", "삼성 외야수 · 1위", [])),
 ("구자욱은 2026년 / 타율", pv("구자욱A", "구자욱", "삼성 외야수 · 1위", [], [st("타율 · 타격왕", "3할 7푼 1리", 1, hi=True), st("출루율 · 출루왕", "4할 5푼 8리", 2.5, hi=True)], asof=AS)),
 ("출루율과 장타율을 더한", pv("구자욱B", "구자욱", "삼성 외야수 · 1위", [vtrend([dict(x="2024년", v=1.044, vt="1.044", c="good", at=3), dict(x="2025년", v=0.918, vt="0.918", at=4), dict(x="2026년", v=1.039, vt="1.039", c="good", at=1)], title="출루율 + 장타율"),
     vstamp("3년 연속 0.9 넘김", 6, "gold", size=50)], asof=AS)),
 ("구자욱의 지금 계약은", pb("pb9", "구자욱 몸값", [mk("구자욱", 120, 2, row=0, sub="5년 · 2022년 비FA"), gh("기자 전망", 150, 4, row=1, vt="150억 이상")])),
 ("비교 계약은 / 30대 강타자들", pb("pb10", "30대 강타자 · 큰 계약", [dict(v=115, name="김재환·김현수", vt="115억", sub="2021년 겨울", imgs=[dict(img=PR["김재환"], team="SSG"), dict(img=PR["김현수"], team="KT")], at=2, row=1),
     mk("최정", 110, 5, row=0, sub="4년 전액 보장")])),
 ("구자욱은 이번 겨울 만 33살", fo("FA 계약할 때 나이", {"team": "두산", "name": "김재환", "role": "2021년 겨울 · 두산과 115억"}, side("구자욱B", "구자욱", "2026년 겨울"), [dict(k="나이", l="만 33살", r="만 33살", at=0.5)])),
 ("다만 변수가 있어요", pv("구자욱C", "구자욱", "삼성 외야수 · 1위", [vsteps([stp("9월 30일", "왼쪽 햄스트링 부상", 1, "bad")])])),
 ("10월 15일 나온 재검사", pv("구자욱C", "구자욱", "삼성 외야수 · 1위", [vsteps([stp("9월 30일", "왼쪽 햄스트링 부상", -1, "bad"), stp("10월 15일 발표", "출혈·부종 잡힘", 1, "good"), stp("지금", "주루·수비는 아직 제한", 3, "bad")])])),
 ("그리고 김재환과 김현수의 115억은", S(0, "bars", title="100억 이상 FA 계약 수", items=[dict(label="2021년 겨울", value=5, unit="건", at=3, hi=True), dict(label="지난겨울", value=1, unit="건", at=5, color=GRAY)], max=5)),
 ("대신 보상 부담은", S(0, "bars", title="A등급이면 보상금 최대(연봉 × 3)", items=[dict(label="원태인", img=PR["원태인"], team="삼성", value=30, unit="억", at=1, color=GRAY, sub="연봉 10억"), dict(label="구자욱", img=PR["구자욱"], team="삼성", value=15, unit="억", at=1.5, hi=True, sub="연봉 5억")], max=30)),
 ("한 구단 단장도 익명으로", pb("pb11", "구자욱 몸값", [mk("구자욱", 120, -1, row=0, sub="지금 계약 5년")], line=dict(v=100, label="100억", at=0), text="익명 단장 “총액 100억 원은\n당연히 넘길 것 같다”", textAt=1, size=56)),
 ("그래서 제 예상은 / 4년에 110억", pb("pb11", "구자욱 몸값", [mk("구자욱", 120, -1, row=0, sub="지금 계약 5년"), gh("기자 전망", 150, 2, row=1, vt="150억 이상")], [bd("구자욱", 110, 140, "1위", 1)], line=dict(v=100, label="100억", at=-1), cont=True)),
 # 번외 양의지
 ("번외로 한 명 더", pv("양의지A", "양의지", "두산 포수 · 번외", [])),
 ("양의지는 FA로 나오는 게", pv("양의지A", "양의지", "두산 포수 · 번외", [], [st("선수 옵션", "2년 최대 42억", 1.5, hi=True)])),
 ("옵션을 버리고 나오면", S(0, "compgrade", title="양의지가 FA로 나온다면", cols=[dict(GC, at=1)], hi="C", text="연봉 42억 × 1.5배 = 보상금 63억", textAt=3, size=58)),
 ("양의지는 1월에", sp("양의지B", "양의지", "두산 포수", [bub("1월", "“길어봤자 3~4년 뒤\n야구를 그만할 생각”", 1.5)])),
 # 정리
 ("다시 정리해 볼게요", S(0, "pricerows", title="올겨울 FA 대어 몸값 · 야구자판기 예상", rows=rows7((0, 3), 1, 1), chain="pr", max=150)),
 ("4위 홍창기", S(0, "pricerows", title="올겨울 FA 대어 몸값 · 야구자판기 예상", rows=rows7((3, 7), 0, 1), chain="pr", cont=True, max=150)),
 ("제 예상대로라면", S(0, "pricerows", title="올겨울 FA 대어 몸값 · 야구자판기 예상", rows=rows7((7, 7)), chain="pr", cont=True, max=150, line=dict(v=100, label="100억", at=1), text="100억을 넘는 선수 = 구자욱", textAt=2, size=56)),
 ("샐러리캡도 변수예요", S(0, "bars", term="샐러리캡", title="2025 연봉 상위 40명 합계 · 상한 137억", items=[dict(label="삼성", team="삼성", value=132.07, note="132억", at=2, hi=True, sub="남은 여유 5억"), dict(label="LG", team="LG", value=131.55, note="131억", at=3, color="#C30452", sub="남은 여유 5억")], max=137.12, text="상한 2027년 151억까지 오름", textAt=6)),
 ("그리고 몸값은 / 포스트시즌", S(0, "tiles", title="아직 가을야구 중", items=[dict(team="삼성", v="구자욱\n원태인", at=2), dict(team="LG", v="홍창기\n박동원", at=3), dict(team="KIA", v="김호령", at=4)], vsize=64)),
 ("여러분이 보기엔", S(0, "duel", title="올겨울 가장 비싼 FA는?", left={"img": P["구자욱B"], "name": "구자욱", "team": "삼성", "role": "삼성 외야수", "at": 2}, right={"img": P["원태인D"], "name": "원태인", "team": "삼성", "role": "삼성 투수", "at": 3}, vsAt=2.5)),
 ("지난겨울 FA 계약 선수들은", S(0, "question", text="지난겨울 FA\n돈값 순위\n여기를 눌러 확인", img="상황별/썸네일_롱폼10_FA돈값", ph=495, size=72, arrow="left")),
]
assert len(SCN) == len(LINES) - 1, (len(SCN), len(LINES))
for j, (pre, sc) in enumerate(SCN):
    assert LINES[j][0].startswith(pre) or pre in LINES[j][0][:40], (j, pre, LINES[j][0][:40])

CH = [{"key": "기본 규칙", "title": "기본 규칙", "from": 4, "to": 9},
      {"key": "7위 정수빈", "title": "7위 정수빈", "from": 10, "to": 18},
      {"key": "6위 박동원", "title": "6위 박동원", "from": 19, "to": 25},
      {"key": "5위 김호령", "title": "5위 김호령", "from": 26, "to": 32},
      {"key": "4위 홍창기", "title": "4위 홍창기", "from": 33, "to": 39},
      {"key": "3위 최지훈", "title": "3위 최지훈", "from": 40, "to": 48},
      {"key": "2위 원태인", "title": "2위 원태인", "from": 49, "to": 59},
      {"key": "1위 구자욱", "title": "1위 구자욱", "from": 60, "to": 71},
      {"key": "번외 양의지", "title": "번외 양의지", "from": 72, "to": 75},
      {"key": "정리", "title": "정리", "from": 76, "to": 82}]

lines, scenes = [], []
for j, (t, _, _) in enumerate(LINES[:-1]):
    sc = dict(SCN[j][1]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})

TAGS = ["프로야구 FA", "2026 FA", "FA 대어", "FA 몸값", "FA 몸값 예상", "프로야구 FA 2026", "구자욱 FA", "원태인 FA", "최지훈 FA", "홍창기 FA", "김호령 FA", "박동원 FA", "정수빈 FA", "양의지",
        "FA 보상 등급", "프로야구", "KBO", "2026 프로야구", "야구자판기"]
DESC = ("2026 프로야구 FA, 올겨울 FA 대어들의 몸값은 얼마일까요? 구자욱·원태인·최지훈·홍창기·김호령·박동원·정수빈 일곱 명의 몸값을 비슷한 선수들이 실제로 받은 계약과 비교해 예상했어요.\n"
        "FA 보상 등급(A·B·C)과 보상금, 2026 정규시즌 기록, 감독·단장·본인 발언까지 같이 따졌어요.\n\n"
        "지난겨울 100억 원 이상 FA 계약은 강백호의 4년 100억 한 건뿐이었어요. 올겨울 1위 후보는 타격왕·출루왕을 차지한 삼성 구자욱이에요. 다만 9월 30일 왼쪽 햄스트링을 다쳤고, 10월 15일 재검사에서는 주루와 수비에 아직 제한을 두는 게 좋다는 결과가 나왔어요.\n\n"
        "삼성 원태인은 2024년 15승·2025년 12승을 거둔 토종 에이스지만 2026년엔 팔 부상으로 늦게 시작해 7승 9패, 평균자책점 4.52에 그쳤어요. SSG 최지훈은 데뷔 뒤 가장 많은 13홈런을 쳤고, LG 홍창기는 타율이 2할 3푼 9리로 떨어졌지만 출루율은 3할 7푼 5리였어요.\n\n"
        "영상 속 몸값과 등급은 모두 야구자판기의 예상이에요. FA 명단은 한국시리즈가 끝나고 5일 안에 공시돼요.\n\n"
        "야구자판기는 매일 오늘의 야구 이슈를 정리해 드려요.\n\n"
        "올겨울 가장 비싼 FA는 구자욱일까요, 원태인일까요? 댓글로 알려 주세요.\n\n"
        "기록: KBO 기록실(2026 정규시즌 최종 선수·수비 기록), 계약 금액은 각 구단 발표 기사\n"
        "사진: SSG 랜더스 제공, 두산 베어스 제공, LG 트윈스 제공, 삼성 라이온즈 제공, KIA 타이거즈 제공, KT 위즈 제공, 스타뉴스, 연합뉴스, 스포츠서울, 각 구단 공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1016-롱폼16-FA대어몸값-대사.md(근거 표·검수 3회 기록)."

EP = {"date": "2026-10-16", "gameDate": "2026-10-12", "series": "야구롱폼", "focusTeam": "삼성", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1016-long16-v1", "topic": "FA대어몸값", "totalSec": 481.4,
      "gapScale": 1.05, "pauseMax": 0.4, "ttsCharsOk": 8000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "source": SOURCE,
      "youtube": {"title": "프로야구 FA 2026 | 올겨울 FA 대어 몸값 예상 순위, 구자욱 원태인 얼마 받을까 #FA #프로야구",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#프로야구FA", "#FA대어", "#구자욱", "#원태인", "#최지훈", "#홍창기", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 18, 25, 32, 39, 48, 58, 71, 76, 77, 78, 81}
    HOLD = {3: 0.5, 9: 0.6, 18: 0.6, 25: 0.6, 32: 0.6, 39: 0.6, 48: 0.6, 59: 0.6, 71: 0.6, 75: 0.6, 78: 0.5}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-16_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
