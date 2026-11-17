# -*- coding: utf-8 -*-
"""11/13 롱폼 「2027 FA 공시 총정리 — 10개 구단 FA 손익」 콘티 (틀).
명단·등급·구분 = fa_data.json(공시 날 KBO 공식 명단으로 채움). 없으면 fa_data_pred.json(미리보기용 예상 — 올리지 않음).
근거 = /home/claude/fabig/research_teams.md · research/quotes_A,B.md · 남은 돈 = /home/claude/cap27(11/13 공식 명단으로 다시 계산: 박세혁·이형종은 FA 아님 → 포함)
실행: python -X utf8 tools/gen_1113_fa.py [fa_data.json] → episodes/2026-11-13_롱폼.json"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from helpers_1113 import *          # S, wrap2, L, BAND, DUOT, DCT, SP, BB, PS, VST, VSTEPS, STP, Q, TBG, BG_NEU, KEEP, TEAMN, END
from gen_rank_0923 import END, OUT
import helpers_1113 as _H
_H.WRAP.update({w.replace('\n', ' '): w for w in ['8년 동안\n75승을 올린 선발인데', '양의지 때문에\n변수가 가장 큰 포지션이죠', '그리고\n프랜차이즈 선수 한 명의', '최근 3시즌\n평균 연봉으로 정해져요', 'FA로 풀리는 선수 연봉은\n계산에서 뺐고', 'FA 자격을 얻은 선수는\n3명인데', '그럼 삼성이\n쓸 수 있는 돈은 얼마일까요?', '그래서\n데려가는 팀이 내는 보상금은', '한화가 정작 오래\n고민해 온 자리는', '2025년엔\n외국인 선수로 메웠고', '2026년엔\n신인 오재원을 비롯해', '이 돈을\n써야만 하는 이유까지 있어요', '집토끼부터\n잡아야 하는 팀이에요', '구단의\n다년계약 제안을 거절했어요']})   # 11/14 검수: 꾸미는 말과 꾸밈 받는 말 사이에서 자막이 꺾이지 않게 직접 정한 곳

DATA = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].endswith('.json') and 'episodes' not in sys.argv[1] else os.path.join(HERE, 'fa_data.json')
if not os.path.exists(DATA): DATA = os.path.join(HERE, 'fa_data_pred.json')
D = json.load(open(DATA, encoding='utf-8'))
PRED = bool(D.get('predicted'))
T = {t['team']: t for t in D['teams']}
ALL = [p for t in D['teams'] for p in t['players']]
def P_(n): return next((p for p in ALL if p['name'] == n), None)
def has(*ns): return all(P_(n) for n in ns)
N = len(ALL); GA = sum(p['grade'] == 'A' for p in ALL); GB = sum(p['grade'] == 'B' for p in ALL); GC = sum(p['grade'] == 'C' for p in ALL)

# ── 읽기 ──
def jong(w):   # 받침 있음?
    c = w.strip()[-1]
    if '가' <= c <= '힣': return (ord(c) - 0xAC00) % 28 != 0
    return c in '013678LMNlmn'
def ga(w): return w + ('이' if jong(w) else '가')
def wa(w): return w + ('과' if jong(w) else '와')
def eun(w): return w + ('은' if jong(w) else '는')
from ref_narr import narr_of
FIX = [('FA', '에프에이'), ('KBO', '케이비오'), ('MVP', '엠브이피'), ('MLB', '엠엘비'), ('A등급', '에이 등급'), ('B등급', '비 등급'), ('C등급', '씨 등급'), ('%', ' 퍼센트')]
def NARR(sub):
    n = sub
    for a, b in FIX: n = n.replace(a, b)
    n = re.sub(r'(?<=[가-힣])·(?=[가-힣])', ', ', n)   # 이름을 잇달아 부를 땐 짧은 텀(11/2)
    n = narr_of(n)
    n = re.sub(r'([일이삼사오육칠팔구십]+) 월 ([일이삼사오육칠팔구십]+) 일', r'\1월 \2일', n)
    n = re.sub(r'(?<![가-힣])((?:[이삼]?십)?[일이삼사오육칠팔구]?|[이삼]?십) 일(?=까지|에|부터|엔| )', lambda m: m.group(1) + '일' if m.group(1) else m.group(0), n)
    n = n.replace('삼시즌', '세 시즌').replace('삼십오세', '삼십오 세').replace('네 번 타자', '사번 타자')
    n = n.replace(' 퍼센트', '퍼센트').replace('  ', ' ')
    n = re.sub(r'년 약 ', '년, 약 ', n)
    n = re.sub(r'(?<![가-힣])([일이삼사오육칠팔구십]+) 위(?=[ 는에예,면로]|$)', r'\1위', n)   # '삼 위' → '삼위'(띄어쓰기대로 쉼 ✗)
    n = re.sub(r'(?<![가-힣])([일이삼사오육칠팔구십백천]+) (할|푼|년|승|안타|홈런|개)', r'\1\2', n)
    n = re.sub(r'(?<![가-힣])([일이삼사오육칠팔구]) 리(?=[로에 ,]|$)', r'\1리', n)
    n = n.replace('그 전엔', '그전엔').replace('사+이년', '사 플러스 이년').replace('일승인', '일 승인').replace('삼십오 세', '삼십오세').replace('억 일천만', '억 천만')
    n = re.sub(r'(?<![가-힣])(십이|십일|십|[일이삼사오육칠팔구]) 월', r'\1월', n)
    n = n.replace('사+이 년', '사 플러스 이 년')
    n = re.sub(r'(?<=[가-힣])·(?=[가-힣])', ', ', n)   # 이름을 잇달아 부를 땐 짧은 텀(11/2)
    # 11/13 사용자 "이십육명=스물여섯명": 사람 수는 고유어(스무 명·스물다섯 명)
    _T = {'': '', '십': '열', '이십': '스물', '삼십': '서른', '사십': '마흔', '오십': '쉰'}
    _U = {'': '', '일': '한', '이': '두', '삼': '세', '사': '네', '오': '다섯', '육': '여섯', '칠': '일곱', '팔': '여덟', '구': '아홉'}
    def _cnt(m):
        t, u = m.group(1) or '', m.group(2) or ''
        return ('스무' if t == '이십' and not u else _T[t] + _U[u]) + ' ' + m.group(3)
    n = re.sub(r'(?<![가-힣])((?:[이삼사오])?십)?([일이삼사오육칠팔구])? (명)', lambda m: _cnt(m) if (m.group(1) or m.group(2)) else m.group(0), n)
    return n

# ── 이름 부르기: 등급별로 묶어 한 줄 ──
def names_line(team):
    ps = T[team]['players']
    if not ps: return f"{team}에선 / FA 자격을 얻은 선수가 / 한 명도 없어요"
    seg = []
    for g in 'ABC':
        xs = [p['name'] for p in ps if p['grade'] == g]
        if not xs: continue
        if len(xs) == 1: who = ga(xs[0])
        elif len(xs) == 2: who = wa(xs[0]) + ' ' + ga(xs[1])
        else: who = f"{xs[0]}·{xs[1]} 등 {len(xs)}명이"
        seg.append(f"{who} {g}등급")
    s = ', / '.join(seg)
    return s + '이에요'

# ── 사진 ──
PROF = set("구자욱 원태인 박동원 홍창기 김호령 정수빈 양의지 박치국 최재훈 박상원 권희동 김상수 오윤석 한승혁 최지훈".split())
PROFX = {"배정대": "KBO프로필/배정대_2024KT"}
def prof(n): return PROFX.get(n) or ("KBO프로필/" + n if n in PROF else None)
TEAMLOGO = {"KIA": "KIA"}
def rows_of(team, at0=0.0):
    return [dict(name=p['name'], pos=p['pos'], grade=p['grade'], kind=p['kind'], img=prof(p['name']), at=at0 + i * .22) for i, p in enumerate(T[team]['players'])]

# 남은 돈(2027 상한 151억 1709만 − 2027년에 이미 정해진 연봉, FA 대상 연봉 뺌·옵션·인상·특례 뺀 추정) — 11/13 공식 명단 기준(cap27/model10.py)
ROOM = {"한화": "13억 2천만", "LG": "42억 4천만", "두산": "49억 7천만", "KT": "54억 8천만", "삼성": "53억 4천만", "KIA": "59억 5천만",
        "SSG": "62억 2천만", "롯데": "65억 4천만", "NC": "70억 4천만", "키움": "103억 7천만"}
ROOMV = {"한화": 13.2, "LG": 42.4, "두산": 49.7, "KT": 54.8, "삼성": 53.4, "KIA": 59.5, "SSG": 62.2, "롯데": 65.4, "NC": 70.4, "키움": 103.7}
RANKN = {1: "우승", 2: "2위", 3: "3위", 4: "4위", 5: "5위", 6: "6위", 7: "7위", 8: "8위", 9: "9위", 10: "10위"}
KN = {"KIA": "기아"}
def kn(t): return KN.get(t, t)
def RKT(team): r_ = T[team]['rank']; return '우승' if r_ == 1 else ('정규 1위 · 준우승' if team == 'KT' else '준우승') if r_ == 2 else RANKN[r_]
def BOARD(team, chain, rowsAt=0.0, hl=(), hlAt=-1, room=None, roomAt=50, verdict=None, verdictAt=50, **k):
    t = T[team]
    rows = rows_of(team, rowsAt) if rowsAt >= 0 else [dict(r, at=-1) for r in rows_of(team)]
    return S(0, "fa_board", team=team, title=f"2026 {RKT(team)} · {TEAMN.get(team, team)}",
             rows=rows, hl=list(hl), hlAt=hlAt, room=dict(txt=ROOM[team], v=ROOMV[team], at=roomAt) if room else None,
             verdict=verdict, verdictAt=verdictAt, pred=PRED, chain=chain, bg=TBG(team), noCenter=True, **k)
def POSB(title, items, chain, **k):   # 포지션판: 팀 다른 선수들
    rows = []
    for i, (n, team, at) in enumerate(items):
        p = P_(n)
        if not p: continue
        rows.append(dict(name=n, pos=p['pos'], grade=p['grade'], kind=kn(team), team=team, img=prof(n), at=at))
    return S(0, "fa_board", team="", title=title, rows=rows, hl=[], hlAt=-1, room=None, verdict=None, pos=True, pred=PRED, chain=chain, bg=BG_NEU, noCenter=True, **k)

def ND(id, x, y, ic, lab="", sub="", at=0, **k): return dict(id=id, x=x, y=y, ic=ic, lab=lab, sub=sub, at=at, **k)
def ED(a, b, lab="", at=0, **k): return dict(a=a, b=b, lab=lab, at=at, **k)
def FL(nodes, edges=(), cap=None, **k): return S(0, "lo_flow", title="", nodes=list(nodes), edges=list(edges), wall=None, boxes=[], cap=cap, noCenter=True, **k)
def PSS(img, name, team, sub, stats, **k): sc = PS(img, name, sub, [], stats=list(stats), team=team, **k); sc['bg'] = TBG(team); return sc
def TLn(items, **k): return S(0, "tline", title="", items=items, noCenter=True, uni=True, **k)
def I(d, t, at, c=None): return dict(dict(d=d, t=t, at=at), **({"c": c} if c else {}))
LN = []   # (key, sub, scene)
def A(key, sub, sc, **x): LN.append((key, sub, sc, x))

# ════ ① 오프닝 ════
FC = dict(type="fa_count", n=N, label="2027 FA 자격 선수", grades=[dict(g="A", n=GA), dict(g="B", n=GB), dict(g="C", n=GC)], gradesAt=50,
          faces=[dict(img="경기/구자욱_KSMVP_1108", name="구자욱", team="삼성"), dict(img="경기/원태인_KS5차전_1108", name="원태인", team="삼성")], facesAt=50,
          pred=PRED, chain="fc", bg=BG_NEU, noCenter=True)
A('o1', f"2027 FA 자격 선수 {N}명이 / 11월 13일 공시됐어요", dict(FC))
A('o2', f"삼성 구자욱과 원태인을 포함해 / A등급 {GA}명, B등급 {GB}명, / C등급 {GC}명이에요", dict(FC, nAt=-1, facesAt=50, gradesAt=0.2, cont=True))
# ── 28명 소개(11/14 사용자 "맨 처음에 FA 선수들이 누가 있는지 소개부터 해주고 팀별로") — 등급별 명단판, 부르는 순서대로 한 줄씩 ──
def _RB(title, rows, chain, **k): return POSB(title, rows, chain, **k)
A('i1', "A등급은 / 삼성 원태인과 구자욱, / LG 홍창기, / KT 김민혁과 배정대, / 한화 박상원이에요",
  _RB("A등급 6명", [("원태인", "삼성", 1.1), ("구자욱", "삼성", 1.35), ("홍창기", "LG", 2.1), ("김민혁", "KT", 3.1), ("배정대", "KT", 3.35), ("박상원", "한화", 4.1)], "ia"))
A('i2', "B등급은 14명으로 가장 많아요 / 기아 김태군, / LG 박동원, / 두산 박치국과 정수빈, / 한화 이재원과 최재훈, / 키움 최주환이 있고",
  _RB("B등급 14명", [("김태군", "KIA", 1.1), ("박동원", "LG", 2.1), ("박치국", "두산", 3.1), ("정수빈", "두산", 3.35), ("이재원", "한화", 4.1), ("최재훈", "한화", 4.35), ("최주환", "키움", 5.1)], "ib"), gapAfter=0.15)
A('i3', "KT에서 김민수와 한승혁, 오윤석, / SSG에서 최지훈과 서진용, 김성현, / 그리고 NC 권희동까지 B등급이에요",
  _RB("B등급 14명", [("김민수", "KT", 0.1), ("한승혁", "KT", 0.3), ("오윤석", "KT", 0.5), ("최지훈", "SSG", 1.1), ("서진용", "SSG", 1.3), ("김성현", "SSG", 1.5), ("권희동", "NC", 2.1)], "ib", cont=True))
A('i4', "C등급은 8명이에요 / 삼성 전병우, / KT 김상수, / 기아 김호령, / 두산 양의지, / 롯데 박승욱, / 그리고 SSG에서 / +문승원과 오태곤, 한유섬이 나왔어요",
  _RB("C등급 8명", [("전병우", "삼성", 1.1), ("김상수", "KT", 2.1), ("김호령", "KIA", 3.1), ("양의지", "두산", 4.1), ("박승욱", "롯데", 5.1), ("문승원", "SSG", 7.0), ("오태곤", "SSG", 7.2), ("한유섬", "SSG", 7.4)], "ic"))
A('o3', "그럼 10개 구단은 / 누구를 지키고 / 누구를 노릴까요?",
  Q("10개 구단 · 누굴 지키고 누굴 노릴까?", ["삼성", "KT", "KIA", "LG", "두산", "SSG", "롯데", "NC", "한화", "키움"], logoSize=150, size=84, logoAt=0.3, textAt=2, bg=BG_NEU))
A('o4', "FA 등급을 짧게 보고, / 우승팀 삼성에서 10위 키움까지 / 구단마다 본 뒤 / 포지션별로 다시 묶어 볼게요",
  S(0, "tline", title="목차", items=[dict(STP("1", "FA 등급과 남은 돈", 0), hl=1), dict(STP("2", "10개 구단 한 팀씩", 0.15), hl=3), dict(STP("3", "포수·외야 FA", 0.3), hl=4)], noCenter=True, uni=True, bg=BG_NEU))

# ════ ② FA 등급 ════
GR = dict(type="fa_grade", cards=[
    dict(g="A", head="A등급", crit=["팀 연봉 3위 안", "리그 연봉 30위 안"], comp=["보상선수 1명 (보호 20명 외)", "+ 직전 연봉 200%", "또는 연봉 300%"], zone=0, team="3위 안", lg="30위 안", prot="보호선수 20명 외", p1=200, p2=300, at=0, critAt=50, compAt=50),
    dict(g="B", head="B등급", crit=["팀 연봉 4~10위", "리그 연봉 31~60위"], comp=["보상선수 1명 (보호 25명 외)", "+ 직전 연봉 100%", "또는 연봉 200%"], zone=1, team="4~10위", lg="31~60위", prot="보호선수 25명 외", p1=100, p2=200, at=0.3, critAt=50, compAt=50),
    dict(g="C", head="C등급", crit=["그보다 연봉이 낮거나", "만 35세 이상 첫 FA · 세 번째 FA"], comp=["보상선수 없음", "직전 연봉 150%"], zone=2, team="11위 이하", lg="61위 이하", extra="+ 만 35세 이상 첫 FA · 세 번째 FA", prot=None, p1=150, p2=None, at=0.6, critAt=50, compAt=50)],
    hi=-1, note="등급 기준은 최근 3시즌 평균 연봉", noteAt=50, chain="gr", bg=BG_NEU, noCenter=True)
import copy
def GRs(hi, crit=(), comp=(), note=-1, **k):
    g = copy.deepcopy(GR); g['hi'] = hi; g['cont'] = True
    for i, c in enumerate(g['cards']):
        c['at'] = -1
        if i in crit: c['critAt'] = crit[i]
        if i in comp: c['compAt'] = comp[i]
    g['noteAt'] = note; g.update(k); return g
A('g1', "FA를 데려올 때 드는 돈은 / 몸값만이 아니에요 / 등급에 따라 / 원래 팀에 줘야 하는 보상이 달라지거든요", dict(GR))
A('g2', "등급은 최근 3시즌 평균 연봉으로 정해요 / 팀 안에서 3위 안, / 리그 전체에서 30위 안이면 A등급이죠", GRs(0, crit={0: 1.2}, note=0))
A('g3', "A등급 선수를 데려가면 / 보호선수 20명 밖에서 1명과 / 직전 연봉의 200%를 주거나, / 선수 대신 연봉의 300%를 줘야 돼요", GRs(0, crit={0: -1}, comp={0: 1}))
A('g4', "팀 안에서 4위에서 10위, / 리그에서 31위에서 60위면 B등급이고, / 보호선수 25명 밖에서 1명과 연봉의 100%, / 또는 연봉의 200%를 줘요",
  GRs(1, crit={0: -1, 1: 0.2}, comp={0: -1, 1: 2}))
A('g5', "C등급은 그보다 연봉이 낮은 선수, / 만 35세 이상에 처음 FA가 된 선수, / 세 번째 FA인 선수 등이에요", GRs(2, crit={0: -1, 1: -1, 2: 0.2}, comp={0: -1, 1: -1}))
A('g6', "C등급은 보상선수 없이 / 연봉의 150%만 주면 돼서 / 데려가는 팀 부담이 가장 적어요", GRs(2, crit={0: -1, 1: -1, 2: -1}, comp={0: -1, 1: -1, 2: 0.3}))
SCH = [STP("11월 13일", "FA 자격 선수 공시", -1), STP("15일", "FA 신청 마감", 2), STP("16일", "승인 선수 공시", 3), STP("17일", "모든 구단과 협상", 50)]
A('g7', "다만 11월 13일에 / 공시된 선수가 / 모두 FA가 되는 건 아니에요 / 15일까지 신청한 선수만 / 16일 FA 승인 선수로 공시돼요",
  S(0, "tline", title="2027 FA 일정", items=[dict(x) for x in SCH], noCenter=True, uni=True, bg=BG_NEU, chain="sch"))
CAPX = dict(type="rf_capbar", who="", team="", cap=151.17, capLab="2027 상한 151억 1천만", total=95, totalLab="", totalTxt="이미 정해진 연봉",
            leftLab="", leftTxt="남은 돈", totalAt=0, leftAt=3, capAt=0, noCenter=True, bg=BG_NEU, chain="capx")
A('g8', "구단마다 제재금 없이 / FA에 쓸 수 있는 돈도 / 같이 볼게요 / 11월 13일 공시 명단으로 / 계산한 2027년 남은 돈이에요", dict(CAPX, capAt=2, totalAt=50, leftAt=50))
A('g9', "남은 돈은 2027년 샐러리캡 상한 151억 1천만 원에서 / 2027년에 나갈 연봉을 뺀 돈이에요", dict(CAPX, totalAt=0.2, capAt=-1, leftAt=1.2, cont=True))
A('g10', "FA 선수 연봉과 / 옵션·연봉 인상, / 프랜차이즈 특례는 빼고 / 계산한 추정이라 / 실제로는 조금 달라질 수 있어요", dict(CAPX, totalAt=-1, capAt=-1, leftAt=-1, cont=True, tag="옵션·연봉 인상·래리 버드 룰은 뺀 추정치", tagAt=3))

# ════ ③ 10개 구단 ════
def team_open(team, key, lead, lead2=None):
    n = len(T[team]['players'])
    if lead2 and 0 < n <= 2:
        seg = []
        for g in 'ABC':
            xs = [p['name'] for p in T[team]['players'] if p['grade'] == g]
            if xs: seg.append(f"{ga(xs[0]) if len(xs) == 1 else wa(xs[0]) + ' ' + ga(xs[1])} {g}등급")
        A(key + '0', f"{lead2} / " + ', / '.join(seg) + "으로 / FA 자격을 얻었어요", BOARD(team, "b" + team, rowsAt=0.3, hl=[p["name"] for p in T[team]["players"]], hlAt=1))
        return
    A(key + '0', f"{lead} / FA 자격 선수가 {n}명이에요" if n else f"{lead} / FA 자격 선수가 없어요", BOARD(team, "b" + team, rowsAt=0.3))
    if n: A(key + '1', names_line(team), BOARD(team, "b" + team, rowsAt=-1, hl=[p["name"] for p in T[team]["players"]], hlAt=0, cont=True))
def team_room(team, key, sub, verdict=None, extra=None, alt=None, ek=None):
    def bd(**k):
        b = BOARD(team, "r" + team, rowsAt=-1, room=True, verdict=verdict, **k)
        if alt and b.get('room'): b['room']['alt'] = dict(txt=alt[0], at=alt[1] if not k.get('cont') else -1)
        return b
    _pv = LN[-1][2] if LN else {}
    if _pv.get('type') == 'fa_board' and _pv.get('team') == team and _pv.get('chain') == "b" + team:   # 바로 앞이 같은 팀 명단판이면 이어받기(깜빡임 ✗)
        _b = bd(roomAt=1 if not alt else 0.2, verdictAt=50); _b['chain'] = "b" + team; _b['cont'] = True
        A(key, sub, _b)
        if extra: _e = bd(roomAt=-1, verdictAt=0.4, cont=True, **(ek or {})); _e['chain'] = "b" + team; A(key + 'v', extra, _e)
        return
    A(key, sub, bd(roomAt=1 if not alt else 0.2, verdictAt=50))
    if extra: A(key + 'v', extra, bd(roomAt=-1, verdictAt=0.4, cont=True, **(ek or {})))
SB = TBG("삼성")
def PSx(img, name, team, sub, viz, **k): sc = PS(img, name, sub, viz, team=team, **k); sc['bg'] = TBG(team); return sc
def SPx(img, name, team, bubbles, **k): sc = SP(img, name, bubbles, **k); sc['bg'] = TBG(team); sc['team'] = team; return sc
def _Y(d): return ("2026년 " + d) if re.match(r"\d+월", d or "") else d
def VQt(date, text, at): return dict(type="quote", date=_Y(date), text=text, at=at)
_BB0 = BB
def BB(date, text, at, hi=False): return _BB0(_Y(date), text, at, hi)

SAL = {"원태인": 10, "구자욱": 5}   # 2026 연봉(억) — 원태인 아시아투데이 11/9, 구자욱 서울신문 11/10
def comp_txt(n):   # 등급별 보상(공식 등급 기준으로 자동)
    p = P_(n); s_ = SAL.get(n)
    if not p or not s_: return None
    if p['grade'] == 'A': return f"보상선수 1명과 {s_ * 2}억 원, / 또는 {s_ * 3}억 원"
    if p['grade'] == 'B': return f"보상선수 1명과 {s_}억 원, / 또는 {s_ * 2}억 원"
    if p['grade'] == 'C': return f"{s_ * 1.5:g}억 원"
def FAN(team, bubbles, **k): return S(0, "fa_fans", team=team, title="팬 반응", sub=TEAMN.get(team, team), bubbles=[dict(t=t, at=a, c=c) for t, a, c in bubbles], bg=TBG(team), noCenter=True, **k)
def FQ(name, role, team, date, text, img=None, at=0.6, **k): return S(0, "fa_quote", name=name, role=role, team=team, date=_Y(date), text=text, img=img, at=at, bg=TBG(team), noCenter=True, **k)

# 삼성 — 근거: 삼성2027-근거-1109.md (경향 11/8 · 스타뉴스 10/13 · 국민일보 11/9 · 파이낸셜뉴스·마이데일리 11/9 · 아시아투데이 11/9), 서울신문 11/10(구자욱 연봉 5억), 남은 돈 53억 4천만(박세혁 포함) · 옵션 절반+15% 인상이면 42.7억
team_open("삼성", "s", "우승팀 삼성은")
if has("구자욱"):
    A('s2', "구자욱은 2026년 타율 3할 7푼 1리로 / 첫 타격왕에 올랐고 / 한국시리즈 MVP까지 받았어요",
      PSx("경기/구자욱_KSMVP_1108", "구자욱", "삼성", "생애 첫 FA · 외야수", [VST("2026 타격왕 · 타율 3할 7푼 1리", 0.2, size=54), VST("한국시리즈 MVP", 2, size=60)], chain="kjw"))
    A('s2b', "그런데 우승 직후 인터뷰에서 / 뜻밖의 말이 나왔어요 / 진심으로 미국에 가고 싶다, / 해외 에이전트가 있으면 연락 달라고 한 거예요 / 농담처럼 들렸는데 / 11월 13일, / 정말로 미국 에이전트를 선임했다는 소식이 나왔죠",
      PSx("경기/구자욱_KSMVP_1108", "구자욱", "삼성", "생애 첫 FA · 외야수", [VQt("11월 8일 · 우승 직후", "나도 미국 무대에 꼭 가고 싶다. 진심이다", 2.1), VQt("", "혹시 해외 에이전트 있으시면 연락 바란다", 3.1), VST("11월 13일 · 미국 에이전트 선임", 6.1, size=50)], chain="kjw", cont=True))
    if comp_txt("구자욱"): A('s2c', f"그럼 구자욱을 데려가는 팀은 / 얼마를 줘야 할까요? / 2026년 연봉이 5억 원이고 / {P_('구자욱')['grade']}등급이라 " + comp_txt("구자욱") + "을 주면 돼서 / 보상 부담은 크지 않아요",
      PSx("경기/구자욱_KSMVP_1108", "구자욱", "삼성", f"{P_('구자욱')['grade']}등급 · 2026 연봉 5억", [VST("타 구단 영입 시 보상", 0.6, size=50), VST(comp_txt("구자욱").replace(' / ', ' '), 3, size=50)], chain="kjw", cont=True))
if has("원태인"):
    A('s3', "원태인은 8년 동안 75승을 거둔 선발이고 / 해외 진출을 위해 / 에이전트를 이미 선임했다고 밝혔어요",
      PSx("경기/원태인_KS5차전_1108", "원태인", "삼성", "생애 첫 FA · 선발 투수", [VST("8년 75승", 0.2, size=60), VQt("11월 8일", "해외 진출을 위해 에이전트를 이미 선임해 둔 상태다", 1.2)]))
    if comp_txt("원태인"): A('s3b', f"원태인은 2026년 연봉이 10억 원이라 / 국내 팀이 데려가려면 / " + comp_txt("원태인") + "을 줘야 돼요",
      PSx("경기/원태인_KS5차전_1108", "원태인", "삼성", f"{P_('원태인')['grade']}등급 · 2026 연봉 10억", [VST("타 구단 영입 시 보상", 0.6, size=50), VST(comp_txt("원태인").replace(' / ', ' '), 1.6, size=50)], cont=True))
A('s4', "삼성 구단의 생각은 분명해요 / 이종열 단장은 우승 다음 날 / 두 선수에게 / 어디 가려고 하니, 빨리 계약하자고 했어요",
  PSx("경기/이종열_단장_삼성", "이종열", "삼성", "삼성 단장", [VQt("11월 9일", "태인아, 자욱아, 어디 가려고 하니. 빨리 계약하자", 2.6)]))
A('sf', "삼성 팬들 사이에선 / 원태인에겐 해외 진출이 꿈이니 / 한번 도전해 보라는 글도 올라왔어요",
  FAN("삼성", [("원태인은 해외 진출이 꿈", 1, ""), ("일본이라도 한번 다녀와라", 2, "")]))
team_room("삼성", "s5", "삼성의 남은 돈은 53억 4천만 원인데 / 옵션과 연봉 인상을 어느 정도 넣으면 / 40억 원대 초반까지 줄어요",
          verdict="구자욱·원태인 잔류가 최우선", alt=("옵션·인상까지 치면 40억 원대 초반", 1.6), extra="업계에서는 두 사람 협상이 / 4년 100억 원대 중후반에서 / 시작될 거라고 봐요 / 그러면 한 해 40억 원 안팎씩이라 / 한 명은 프랜차이즈 특례로 / 절반만 넣어도 / 둘이면 60억 원 가까이 돼요 / 그래서 삼성은 데려올 선수보다 / 지킬 선수가 먼저예요", ek=dict(tag="둘 다 잡으면 샐러리캡이 빠듯하다", tagAt=6, tagPos="right"))

# KT — 근거: MHN 2026-11-11(나도현 단장 "현재로서는 FA 영입에 나서지 않는다는 방침", 김현수 OPS .947·최원준 208안타), 뉴스핌 11/11(김상수 C등급 전망)
team_open("KT", "k", "정규시즌 1위, 한국시리즈 준우승 KT는")
if len(T["KT"]['players']) >= max(len(t['players']) for t in D['teams']):
    A('k2', ("SSG와 함께 / FA 자격 선수가 가장 많아요" if len(T["SSG"]["players"]) == len(T["KT"]["players"]) else "10개 구단 가운데 / FA 자격 선수가 가장 많아요"), BOARD("KT", "bKT", rowsAt=-1, cont=True, tag=("SSG와 함께 최다 6명" if len(T["SSG"]["players"]) == len(T["KT"]["players"]) else "10개 구단 최다"), tagAt=0.3))
_KT3 = [ND("p1", 460, 320, "player", "김현수", at=2, img="KBO프로필/김현수_2026프로필"), ND("p2", 960, 320, "player", "최원준", "208안타 · 국내 선수 한 시즌 최다", at=2.05, hiAt=4, img="KBO프로필/최원준_2026프로필"), ND("p3", 1460, 320, "player", "한승택", at=2.1, img="KBO프로필/한승택_2026FA10"), ND("kt", 960, 660, "kbo", "KT 위즈", logo="KT", at=0)]
A('k3', "KT는 바깥 FA에도 적극적인 팀이었어요 / 2025년 겨울엔 / 김현수·최원준·한승택을 / 데려왔고, / 최원준은 208안타로 / 국내 선수 한 시즌 최다 안타 기록을 새로 썼죠",
  FL(_KT3, [ED("p1", "kt", "", 3, c="gold"), ED("p2", "kt", "", 3.1, c="gold", r0=210), ED("p3", "kt", "", 3.2, c="gold")], bg=TBG("KT"), chain="kt3"))
A('k3q', "그럼 2026년 겨울에도 / 바깥 FA를 데려올까요?", FL(_KT3, [ED("p1", "kt", "", -1, c="gold"), ED("p2", "kt", "", -1, c="gold", r0=210), ED("p3", "kt", "", -1, c="gold")], bg=TBG("KT"), chain="kt3", cont=True))
A('k3b', "그런데 나도현 단장은 / 매력적인 FA가 생각보다 많지 않다며 / 현재로서는 FA 영입에 나서지 않는다고 했어요",
  FQ("나도현 단장", "KT 위즈", "KT", "11월", "매력적인 FA 선수들이 생각보다 많지 않다 … 현재로서는 FA 영입에 나서지 않는다는 방침", at=1))
team_room("KT", "k4", f"KT의 남은 돈은 54억 8천만 원이에요", verdict="외부 FA 영입은 없다",
          extra="돈은 남아 있어도 / 2026년 겨울 / KT는 / 바깥보다 집토끼 정리에 / 힘을 쏟을 것으로 보여요")

# KIA — 근거: MHN 7/29(이범호 발언), 파이낸셜뉴스 10/21(박정우 분석), 스포츠조선 11/10(김태군·한준수)
team_open("KIA", "a", "3위 기아는", "3위 기아에선")
if has("김호령"):
    A('a2', "김호령은 생애 첫 FA인 중견수인데 / 리그 연봉 61위로 / 한 끗 차이로 C등급이 됐어요 / 보상금은 3억 7500만 원뿐이죠",
      PSx("경기/김호령_만루포_0821_KIA제공", "김호령", "KIA", "생애 첫 FA · 중견수", [VST("리그 연봉 61위 → C등급", 1, size=54), VST("보상금 3억 7500만", 3, size=54)]))
    A('a2b', "시즌 중반인 7월엔 / 이범호 감독이 / 최고의 시즌인 건 분명하다고 했지만, / 후반엔 부진했어요",
      SPx("카드/F16_이범호", "이범호 감독", "KIA", [BB("7월 29일", "올 시즌 김호령이 최고의 시즌을 보내고 있는 것은 분명하다", 2, True)]))
    A('a3', "게다가 기아엔 / 중견수 박정우도 있어서, / 언론에서는 박정우가 주전으로 자리 잡으면 / 김호령에게 큰 계약은 필요 없다고 봤어요",
      FL([ND("pj", 460, 520, "player", "박정우", "중견수", at=0.2), ND("kh", 1420, 520, "player", "김호령", "생애 첫 FA · 중견수", at=0, img="KBO프로필/김호령")],
         [ED("pj", "kh", "주전으로 자리 잡으면", 1.0, c="gold")], cap="큰 계약까지는 필요 없다는 분석", capAt=2.2, capY=760, bg=TBG("KIA")))
if has("김태군"):
    A('a3b', "포수 김태군은 2026년엔 / 한준수와 마스크를 / 거의 반씩 나눠 썼어요",
      PSS("경기/김태군_덕아웃_0729_KIA제공", "김태군", "KIA", "포수", [STT("2026년 포수 출전", "한준수와 반반", 0.6), STT("기아", "다년계약 다시 제안", 50), STT("김태군", "시장 평가 받겠다", 50, True)], chain="ktg"))
    A('a3c', "기아는 다시 다년계약을 제안했지만 / 김태군은 FA 시장에서 / 평가를 받아 보기로 한 것으로 알려졌어요",
      PSS("경기/김태군_덕아웃_0729_KIA제공", "김태군", "KIA", "포수", [STT("2026년 포수 출전", "한준수와 반반", -1), STT("기아", "다년계약 다시 제안", 0.2), STT("김태군", "시장 평가 받겠다", 1.2, True)], chain="ktg", cont=True))
if has("김호령", "김태군"): A('af', "기아 팬 커뮤니티에는 / 두 가지 반응이 같이 올라왔어요 / 두 선수를 비싸게 잡지는 않을 것 같아 / +다행이라는 글이 있는가 하면 / 둘 다 나가면 / 오른손 타자가 모자란다는 걱정도 있었죠",
  FAN("KIA", [("비싸게 안 잡을 것 같아 다행", 0.4, ""), ("둘 다 나가면 주전 오른손 타자 둘뿐", 4.2, "bad")]))
team_room("KIA", "a4", "기아의 남은 돈은 59억 5천만 원이에요", verdict="관건은 박정우",
          extra="이 돈을 김호령에게 얼마나 쓸지는 / 박정우를 주전 중견수로 / 얼마나 믿느냐에 달려 있어요")

# LG — 근거: 재경일보 11/5(다년계약 거절, 차명석 "지금 아무런 얘기를 못 한다"), 스포츠조선 11/10(박동원 14홈런·타율 .225, "무조건 잡겠다" 나서기 어려운 상황), 머니투데이 9/21(홍창기 허리 근육통 첫 말소)
team_open("LG", "l", "4위 LG는", "4위 LG에선")
def _PDW(at, sat):   # 박동원 사진은 전신이 작게 찍힘 → 홍창기와 크기가 맞게 당겨 씀
    c = DCT("경기/박동원_세리머니_LG제공", "박동원", "LG", at, [dict(k="2026년 14홈런 · 타율", v="2할 2푼 5리", at=sat)]); c['zoom'] = 1.55; c['zo'] = '50% 22%'; return c
if has("홍창기", "박동원"):
    A('l2', "홍창기와 박동원은 / 시즌 전 다년계약 제안을 거절하고 / FA 시장을 택했어요",
      DUOT("", [DCT("경기/홍창기_상체_0921_LG제공", "홍창기", "LG", 0, [dict(k="2026년 타율", v="2할 3푼 9리", at=50)]), _PDW(0, 50)]))
    A('l2b', "그런데 2026년엔 / 박동원이 3년 연속 20홈런을 치다가 / 14홈런, 타율 2할 2푼 5리로 떨어졌고, / 홍창기도 타율 2할 3푼 9리에 그쳤어요",
      DUOT("", [DCT("경기/홍창기_상체_0921_LG제공", "홍창기", "LG", -1, [dict(k="2026년 타율", v="2할 3푼 9리", at=3)]), _PDW(-1, 1.2)], cont=True))
    A('l3', "차명석 단장은 11월 초 / 두 선수를 다 잡는다는 방침은 서 있다면서도 / 시장 가격이 어떻게 형성될지는 / 좀 더 살펴봐야 한다고 했어요",
      SPx("카드/F16_차명석", "차명석 단장", "LG", [BB("11월 초", "두 선수 다 잡는다는 방침은 서 있다", 1), BB("", "시장 가격이 어떻게 형성될지는 좀 더 살펴봐야", 2.2, True)]))
if has("홍창기", "박동원"): A('lf', "LG 팬 커뮤니티에는 / 이런 글이 올라왔어요 / 성적이 떨어진 데다 / 보상 부담까지 있으니 / 다른 팀이 크게 달려들진 않을 거고 / 적당한 값에 남을 거라는 얘기였죠",
  FAN("LG", [("A등급 보상 주고 누가 데려가?", 0.4, ""), ("박동원 갈 팀이 없다", 4.1, ""), ("적당한 값에 잔류", 5.1, "")]))
team_room("LG", "l4", "LG의 남은 돈은 42억 4천만 원으로 / 10개 구단 가운데 두 번째로 적어요", verdict="잡긴 잡는데, 가격이 문제",
          extra="돈이 넉넉하지 않은 데다 / 두 선수 성적까지 떨어져서 / 언론에서는 LG도 무조건 잡겠다고 / 나서기 어렵다고 봤어요")

# 두산 — 근거: 스포츠조선 11/10(양의지 4+2년 중 4년, 선수 의지로 방출 요구 가능 → 사실상 보상 없는 FA), 엑스포츠 10/16(구자욱 영입 후보), 노컷 10/15(김원형 발언)
team_open("두산", "d", "5위 두산은", "5위 두산에선")
if not has("양의지"): A('d2a', "그런데 두산엔 / 이번 명단엔 없지만 / 큰 변수가 하나 있어요 / 바로 포수 양의지인데요",
  PSS("경기/양의지_300호_두산제공_HQ", "양의지", "두산", "포수 · 4+2년 계약", [STT("세 번째 FA", "C등급", 50), STT("2026년 연봉", "42억", 50), STT("보상금 150%", "63억", 50, True), STT("옵트아웃하면", "보상 없음", 50, True)], chain="yej"))
A('d2', "양의지는 4+2년 계약 가운데 / 4년을 채우고 / 세 번째 FA 자격을 얻었어요",
  PSS("경기/양의지_300호_두산제공_HQ", "양의지", "두산", "포수 · 4+2년 계약", [STT("세 번째 FA", "C등급", 1.4), STT("2026년 연봉", "42억", 50), STT("보상금 150%", "63억", 50, True), STT("옵트아웃하면", "보상 없음", 50, True)], chain="yej", cont=not has("양의지")))
A('d2b', "그런데 양의지는 2026년 연봉이 42억 원이라 / C등급이어도 데려가는 팀은 / 보상금만 63억 원을 줘야 돼요",
  PSS("경기/양의지_300호_두산제공_HQ", "양의지", "두산", "포수 · 4+2년 계약", [STT("세 번째 FA", "C등급", -1), STT("2026년 연봉", "42억", 0.3), STT("보상금 150%", "63억", 1.4, True), STT("옵트아웃하면", "보상 없음", 50, True)], chain="yej", cont=True))
A('d2c', "다만 계약에 / 조건 없이 풀려날 수 있는 조항이 있다고 알려져, / 그 길이면 보상 없이 데려갈 수 있어서 / 언론에서는 포수 시장이 크게 흔들릴 수 있다고 봤어요",
  PSS("경기/양의지_300호_두산제공_HQ", "양의지", "두산", "포수 · 4+2년 계약", [STT("세 번째 FA", "C등급", -1), STT("2026년 연봉", "42억", -1), STT("보상금 150%", "63억", -1, True), STT("옵트아웃하면", "보상 없음", 1.2, True)], chain="yej", cont=True))
A('d3', "두산은 타선 고민도 커요 / 김원형 감독은 / 1년 내내 공격 쪽에서 / 활로가 나오지 않았다고 했어요",
  SPx("카드/P21_김원형_박수", "김원형 감독", "두산", [BB("10월 14일", "1년 내내, (…) 공격 쪽에서 활로가 나오지 않았다", 2, True)]))
A('d4', "그래서 두산은 / 구자욱 영입 후보로도 거론돼요",
  DUOT("두산, 구자욱 영입 후보로 거론", [DCT("경기/구자욱_세리머니_0827_삼성제공", "구자욱", "삼성", 0.2)]))
team_room("두산", "d5", "두산의 남은 돈은 49억 7천만 원인데 / 양의지 계약의 남은 2년 몫까지 넣은 돈이에요 / 양의지가 떠나면 / 70억 3천만 원까지 늘어나요", verdict="양의지 잔류가 먼저", alt=("양의지가 떠나면 70억 3천만 원", 2.6),
          extra="두산은 양의지를 잡는 게 먼저지만, / 놓치면 늘어난 돈으로 / 바깥의 큰 타자를 노려 볼 수 있어요")

# SSG — 근거: SPOTV 10/17(다년계약 거절·잡기로), 엑스포츠 4/4(최지훈 발언)
team_open("SSG", "x", "6위 SSG는")
A('x1b', "다만 김성현은 2026 시즌을 끝으로 은퇴해서 / FA를 신청하지 않을 거예요", BOARD("SSG", "bSSG", rowsAt=-1, cont=True, hl=["김성현"], hlAt=0.2))
if has("최지훈"):
    A('x2', "최지훈은 생애 첫 FA인 중견수로 / 시즌 전 다년계약 제안을 거절했어요",
      PSx("경기/최지훈_5타점_0920_SSG제공", "최지훈", "SSG", "생애 첫 FA · 중견수", [VST("다년계약 제안 거절", 0.4, size=54)], chain="cjh"))
    A('x3', "2026년 4월엔 / 잘하면 좋은 계약을 하고 / 못하면 그에 맞는 대우를 받을 거라고 했는데, / 시즌은 타율 2할 5푼대로 마쳤어요",
      PSx("경기/최지훈_5타점_0920_SSG제공", "최지훈", "SSG", "생애 첫 FA · 중견수", [VQt("4월 3일", "올해 잘하면 좋은 계약을 할 것이고, 못하면 그에 맞는 대우를 받지 않을까", 0.2), VST("2026년 타율 2할 5푼대", 3, size=54)], chain="cjh", cont=True))
if has("최지훈"): A('x3b', "그래도 SSG는 / 최지훈을 잡기로 방향을 정했어요",
  PSx("경기/최지훈_5타점_0920_SSG제공", "최지훈", "SSG", "생애 첫 FA · 중견수", [VST("2026년 타율 2할 5푼대", -1, size=54), VST("SSG는 잡는다는 방침", 1, size=54)], chain="cjh", cont=True))
team_room("SSG", "x4", "SSG의 남은 돈은 62억 2천만 원이에요", verdict="최지훈부터 잡는다",
          extra="언론에서는 / 시즌 전 제안보다 깎이진 않고 / 오를 거라고 봐서, / SSG는 이 돈의 상당 부분을 / 최지훈에게 써야 할 수 있어요")

# 롯데 — 근거: 엑스포츠 10/23(팀 홈런 113 최하위·외야 보강), OSEN 10/11(그룹 승인 없음·2022 170억 실패가 운영 제약)
team_open("롯데", "r", "7위 롯데는", "7위 롯데에선")
A('r2', "롯데는 / 누가 나가느냐보다 / 누굴 데려오느냐가 더 관심이에요 / 2026년 팀 홈런이 113개로 / 리그에서 가장 적었고 / 외야를 보강해야 한다는 분석도 나왔거든요",
  FL([ND("lt", 520, 500, "kbo", "롯데", logo="롯데", at=0), ND("of", 1400, 500, "player", "외야수", at=5)], [ED("of", "lt", "보강이 필요한 자리", 5.2, c="gold")], cap="2026년 팀 홈런 113개 · 리그 최하위", capAt=3.1, capY=770, bg=TBG("롯데")))
A('r3', "그런데 롯데는 / FA 시장에서 크게 데인 적이 있어요 / 2022년 겨울, / 유강남과 노진혁, 한현희 / +세 명에게 들인 170억 원이 / +실패로 평가받았거든요 / 그 뒤로 3년 연속 / 외부 FA를 한 명도 데려오지 않았고 / 2025년 겨울엔 / 그룹이 영입을 승인하지 않았어요",
  TLn([I("2022년 겨울", "FA 3명 · 170억", 2.2), I("그 뒤", "실패로 평가", 5, "bad"), I("3년 연속", "외부 FA 0명", 6.2, "bad"), I("2025년 겨울", "그룹 승인 불발", 8.2, "bad")], bg=TBG("롯데")))
A('rf', "롯데 팬 커뮤니티에는 / 아무나 사자는 글도 있었고 / 유강남 때를 겪고도 그러냐며 / 팀에 맞는 선수만 사야 한다는 글도 올라왔어요",
  FAN("롯데", [("아무나 사자", 0.4, ""), ("유강남 겪고도?", 2.1, "bad"), ("팀에 맞는 선수만 사야 한다", 3.1, "")]))
team_room("롯데", "r4", "롯데의 남은 돈은 65억 4천만 원으로 / 세 번째로 많아요", verdict="그룹 승인이 나야 움직인다",
          extra="외야 보강이 필요하고 돈도 있지만 / 롯데의 2026년 겨울은 / 결국 그룹 승인에 달렸어요")

# NC — 근거: 경향 10/27(임선남 단장 "내부 논의를 거쳐 FA 시장에서 구단 기조를 결정할 것", 마지막 외부 FA 2022년 11월 박세혁, 불펜 부진)
team_open("NC", "n", "8위 NC는", "8위 NC에선")
_NC = [I("2022년 11월", "마지막 외부 FA · 박세혁", 1), I("2026년", "불펜 부진·부상", 50, "bad")]
A('n2', "NC는 바깥 FA 시장에선 / 오래 조용했어요 / 마지막이 2022년 11월 포수 박세혁이에요",
  TLn([dict(x) for x in _NC], bg=TBG("NC"), chain="nct"))
_NC2 = [dict(x) for x in _NC]; _NC2[0]['at'] = -1; _NC2[1]['at'] = 0.3
A('n2c', "그리고 2026년엔 / 불펜이 부진과 부상으로 / 흔들렸어요", TLn(_NC2, bg=TBG("NC"), chain="nct", cont=True))
A('n2b', "그럼 NC는 2026년 겨울엔 / 지갑을 열까요? / 임선남 단장은 / 내부 논의를 거쳐 / FA 시장에서 구단 기조를 정하겠다고 했어요",
  FQ("임선남 단장", "NC 다이노스", "NC", "10월 27일", "내부 논의를 거쳐 FA 시장에서 구단 기조를 결정할 것", at=1.2))
team_room("NC", "n3", "NC의 남은 돈은 70억 4천만 원으로 / 키움 다음으로 많아요", verdict="돈은 있다, 결정만 남았다",
          extra="그래서 기조만 정해지면 / 큰손이 될 수 있는 팀이에요")

# 한화 — 근거: 스포츠조선 11/10(최재훈 허인서에 밀림), 엑스포츠 11/1(류지현 발언 두 개), cap27 노시환 경우
team_open("한화", "h", "9위 한화는", "9위 한화에선")
A('h1b', "이재원은 플레잉코치라 / 실제로 FA를 신청하지는 않을 전망이에요", BOARD("한화", "b한화", rowsAt=-1, cont=True, hl=["이재원"], hlAt=0.2))
if has("최재훈"): A('h2', "최재훈은 2025년까지 주전이었지만 / 2026년엔 신예 허인서에게 밀렸어요",
                  PSS("경기/최재훈_세리머니_한화제공", "최재훈", "한화", "포수", [STT("2025년까지", "주전 포수", 0.3), STT("2026년", "허인서에게 밀림", 1.2, True)]))
A('h3a', "한화가 정작 오래 고민해 온 자리는 / 중견수예요 / 2025년엔 외국인 선수로 메웠고 / 2026년엔 신인 오재원을 비롯해 / +여러 선수를 돌려 썼죠",
  TLn([I("한화 중견수", "몇 년째 고민", 0.3), I("2025년", "외국인 선수로 메움", 2), I("2026년", "신인 오재원 등 여러 명", 3)], bg=TBG("한화")))
A('h3', "한화의 더 큰 고민은 중견수예요 / 2025년엔 외국인 선수로 메웠고 / 2026년엔 신인 오재원 등을 돌려 썼는데, / 10월에 새로 온 류지현 감독은 / 오자마자 중견수 FA 얘기부터 하고 싶지 않다며 / 첫 번째 시선은 지금 있는 선수들 안에 있다고 했어요",
  SPx("카드/H14_류지현_한화_A", "류지현 감독", "한화", [BB("11월 1일", "내가 오자마자 '중견수 FA' 이러고 싶지 않다", 3.2, True), BB("", "첫 번째 시선은 우리 선수들 안에 있다", 5, True)]))
team_room("한화", "h4", "한화의 남은 돈은 13억 2천만 원으로 / 10개 구단 가운데 가장 적어요", verdict="노시환 결과 전엔 큰돈 못 쓴다",
          extra="변수는 노시환이에요 / 노시환의 11년 307억 계약이 / 2027년부터 시작되는데 / 메이저리그 포스팅 절차에 들어갔죠 / 노시환이 떠나면 그 몫이 빠져서 / 남은 돈이 40억 8천만 원으로 늘지만, / 그전엔 큰돈을 쓰기 어려워요")
for _k, _s, _sc, _x in LN:   # 노시환 줄에서만 '떠나면 40억 8천만' 칸(앞 줄엔 ✗)
    if _k == 'h4v' and isinstance(_sc.get('room'), dict): _sc['room']['alt'] = dict(txt="노시환이 떠나면 40억 8천만 원", at=5)

# 키움 — 근거: OSEN 2025-12-20(하한제 60억 6538만·30%, 송성문 계약금으로 타자 대형 FA 영입 전망), cap27(47억 4천·103억 7천, 이형종 포함)
team_open("키움", "w", "10위 키움은", "10위 키움에선")
team_room("키움", "w2", "키움의 남은 돈은 103억 7천만 원으로 / 10개 구단 가운데 압도적인 1위예요", verdict="이번 FA 시장 큰손 1순위")
A('w3', "게다가 키움은 / 이 돈을 써야만 하는 이유까지 있어요 / 2027년부터 샐러리캡에 하한이 생기는데 / 연봉 합계가 60억 6천만 원에 못 미치면 / 모자란 돈의 30%를 / +내야 하거든요 / 지금 키움은 47억 4천만 원이라 / 13억 원쯤 모자라요",
  BOARD("키움", "b키움", rowsAt=-1, room=True, roomAt=-1, verdict="이번 FA 시장 큰손 1순위", verdictAt=50, floor=dict(txt="샐러리캡 하한 60억 6천만", at=2.2), tag="지금 연봉 합계 47억 4천만 · 13억쯤 모자람", tagAt=6.2, tagPos="right", tagY=330, cont=True))
A('w3b', "그래서 2025년 말엔 / 송성문에게 주려던 120억 원 계약이 없어지면서 / 그 돈으로 타자 대형 FA를 / 데려올 수 있다는 전망도 나왔어요",
  BOARD("키움", "b키움", rowsAt=-1, room=True, roomAt=-1, verdict="이번 FA 시장 큰손 1순위", verdictAt=50, floor=dict(txt="샐러리캡 하한 60억 6천만", at=-1), tag="대형 타자 FA 영입 전망", tagAt=0.8, cont=True))
A('wf', "키움 팬 커뮤니티에는 / 중견수 수비가 약하니 / 김호령이라도 데려오자는 글이 / +올라왔죠",
  FAN("키움", [("중견수 수비가 약하다", 0.4, "bad"), ("김호령이라도 데려오자", 2.1, "")]))
A('w4', "돈이 가장 많은 데다 쓸 이유까지 있는 키움이 / 2027 FA 시장의 첫 번째 큰손 후보예요",
  BOARD("키움", "b키움", rowsAt=-1, room=True, roomAt=-1, verdict="이번 FA 시장 큰손 1순위", verdictAt=0.4, floor=dict(txt="샐러리캡 하한 60억 6천만", at=-1), cont=True))

# ════ ④ 포지션별 ════
CATCH = [x for x in [("박동원", "LG", 2.0), ("김태군", "KIA", 2.2), ("최재훈", "한화", 2.4), ("양의지", "두산", 50)] if P_(x[0])]
OF = [x for x in [("구자욱", "삼성", 1.0), ("홍창기", "LG", 1.1), ("김민혁", "KT", 2.0), ("배정대", "KT", 2.1), ("최지훈", "SSG", 0.3), ("정수빈", "두산", 0.35), ("김호령", "KIA", 0.4), ("권희동", "NC", 0.45), ("한유섬", "SSG", 0.5)] if P_(x[0])]
A('p1', "이제 팀이 아니라 / 포지션으로 다시 묶어 볼게요 / 먼저 포수예요 / 양의지 때문에 변수가 가장 큰 포지션이죠", POSB("포수 FA", [(n, t, 2.1 + 0.15 * i) for i, (n, t, a) in enumerate(CATCH)], "pc"))
def _lst(xs): return ', '.join(f"{kn(t)} {n}" for n, t, a in xs)
def _chunks(xs, k=2): return [xs[i:i + k] for i in range(0, len(xs), k)]
def _ga_last(xs): return ('이' if jong(xs[-1][0]) else '가')
_c1 = [x for x in CATCH if x[0] != '양의지']
_b1 = len(_chunks(_c1, 3))
_grp = {}
for n, t, a_ in _c1: _grp.setdefault(t, []).append(n)
_p2 = ', '.join(f"{kn(t)} {'·'.join(ns)}" for t, ns in _grp.items())
_p2 = _p2.replace(', ', ', / ', 1) + _ga_last(_c1) + ' 나왔고 / 두산 양의지도 / C등급으로 나왔어요'
A('p2', _p2, dict(POSB("포수 FA", [(n, t, -1) for n, t, a in CATCH], "pc", cont=True), hl=[n for n, t, a in _c1], hlAt=0.1))
_gb = [n for n, t, a in _c1 if P_(n)['grade'] in 'AB']
if _gb:
    _who = (wa(_gb[0]) + ' ' + _gb[1] if len(_gb) == 2 else '·'.join(_gb[:-1]) + '·' + _gb[-1]) if len(_gb) > 1 else _gb[0]
    _gr = sorted({P_(n)['grade'] for n in _gb})
    A('p2b', f"{'이 셋은' if len(_gb) == 3 else _who + ('은' if jong(_gb[-1]) else '는')} {'·'.join(_gr)}등급이라 / 데려가는 팀은 보상선수까지 내줘야 할 수 있어서, / 언론에서는 구단들이 주판알을 튀길 거라고 봤어요",
      dict(POSB("포수 FA", [(n, t, -1) for n, t, a in CATCH], "pc", cont=True), hl=[n for n, t, a in _c1], hlAt=0))
A('p3', f"외야는 {len(OF)}명으로 가장 많아요 / 삼성 구자욱, LG 홍창기, / KT 김민혁·배정대까지 / A등급만 네 명이에요", POSB("외야 FA", OF, "po"))
A('p4b', "그럼 이 외야수들을 / 누가 데려갈 수 있을까요? / 외야 보강이 필요하다는 분석이 나온 롯데, / 구자욱 영입 후보로 거론된 두산, / 그리고 하한을 채워야 하는 키움이 / 외야 FA에 관심을 가질 만한 팀이에요",
  S(0, "lo_flow", title="", nodes=[ND("lt", 480, 540, "kbo", "롯데", "외야 보강 필요", logo="롯데", at=2), ND("ds", 960, 540, "kbo", "두산", "구자욱 영입 후보로 거론", logo="두산", at=3), ND("kw", 1440, 540, "kbo", "키움", "하한을 채워야 하는 팀", logo="키움", at=4)], edges=[],
    wall=None, boxes=[dict(x=200, y=262, w=1520, h=560, lab="외야 FA를 노릴 만한 팀", at=0)], cap=None, noCenter=True, bg=BG_NEU))

# ════ ⑤ 마무리 ════
A('e0', "정리해 볼게요 / 삼성과 SSG, KT는 / 집토끼부터 잡아야 하는 팀이에요 / LG와 기아는 / 가격을 보면서 잡겠다는 쪽이고요 / 외부 FA를 노려 볼 만한 팀은 / 돈이 가장 많은 키움, / 그리고 양의지를 놓치면 / +돈이 늘어나는 두산이에요 / NC는 구단이 결정만 하면, / 롯데는 그룹이 승인하면 / 여기에 뛰어들 수 있고 / 한화는 노시환 결과를 기다려야 해요",
  S(0, "lo_flow", title="", nodes=[ND("ss", 230, 420, "kbo", "삼성", logo="삼성", at=1, lsz=0.6, fs=44), ND("sg", 460, 420, "kbo", "SSG", logo="SSG", at=1.05, lsz=0.6, fs=44), ND("kt", 690, 420, "kbo", "KT", logo="KT", at=1.1, lsz=0.6, fs=44),
        ND("lg", 340, 672, "kbo", "LG", "가격을 보면서", logo="LG", at=3, lsz=0.6, fs=44), ND("ki", 580, 672, "kbo", "기아", "가격을 보면서", logo="KIA", at=3.1, lsz=0.6, fs=44),
        ND("kw", 1050, 420, "kbo", "키움", "남은 돈 1위", logo="키움", at=6, lsz=0.6, fs=44), ND("ds", 1370, 420, "kbo", "두산", "양의지 놓치면", logo="두산", at=7, lsz=0.6, fs=44),
        ND("nc", 1050, 672, "kbo", "NC", "구단이 결정하면", logo="NC", at=9, lsz=0.6, fs=44), ND("lt", 1370, 672, "kbo", "롯데", "그룹이 승인하면", logo="롯데", at=10, lsz=0.6, fs=44), ND("hh", 1730, 546, "kbo", "한화", "노시환 결과 뒤", logo="한화", at=12, lsz=0.6, fs=44)], edges=[],
        wall=None, boxes=[dict(x=90, y=262, w=740, h=600, lab="집토끼 단속이 먼저", at=0), dict(x=870, y=262, w=700, h=600, lab="외부 FA 노릴 만한 팀", at=5, c="gold")], cap=None, noCenter=True, isz=1.1, bg=BG_NEU))
A('e1', "FA 승인 선수는 11월 16일에 공시되고 / 17일부터는 / 모든 구단과 협상할 수 있어요",
  S(0, "tline", title="2027 FA 일정", items=[STP("11월 13일", "FA 자격 선수 공시", -1), STP("15일", "FA 신청 마감", -1), STP("16일", "승인 선수 공시", -1), STP("17일", "모든 구단과 협상", 1)], noCenter=True, uni=True, bg=BG_NEU, chain="sch2"))
A('e2', "계약 소식이 나오면 / 바로 정리해 드릴게요", S(0, "tline", title="2027 FA 일정", items=[STP("11월 13일", "FA 자격 선수 공시", -1), STP("15일", "FA 신청 마감", -1), STP("16일", "승인 선수 공시", -1), STP("17일", "모든 구단과 협상", -1)], noCenter=True, uni=True, bg=BG_NEU, chain="sch2", cont=True))
_QE = dict(logoSize=150, size=84, bg=BG_NEU)
_QL = ["삼성", "KT", "KIA", "LG", "두산", "SSG", "롯데", "NC", "한화", "키움"]
A('e3', "2027 FA 시장에서 / 가장 크게 움직일 팀은 / 돈이 가장 많은 키움일까요?", Q("2027 FA 시장 · 가장 크게 움직일 팀은?", _QL, logoAt=0.2, **_QE), pace='slow')
A('e3b', "아니면 다른 팀일까요?", Q("2027 FA 시장 · 가장 크게 움직일 팀은?", _QL, logoAt=-1, cont=True, **_QE), pace='slow')
A('e3c', "여러분은 어떻게 보세요?", Q("2027 FA 시장 · 가장 크게 움직일 팀은?", _QL, logoAt=-1, cont=True, **_QE), pace='slow')

# ── 조립 ──

# 11/14 사용자: 팀 순서 = 기아 첫 번째 · 삼성 네 번째(나머지는 자유). 순서를 어떻게 정했는지는 대사에서 말하지 않는다
_ORD = ["KIA", "LG", "한화", "삼성", "KT", "두산", "SSG", "롯데", "NC", "키움"]
_PRE = {"삼성": "s", "KT": "k", "KIA": "a", "LG": "l", "두산": "d", "SSG": "x", "롯데": "r", "NC": "n", "한화": "h", "키움": "w"}
def _tm_of(k): return next((t_ for t_, p_ in _PRE.items() if re.match(p_ + r'(\d|f$)', k)), None)
_ti = [i for i, x in enumerate(LN) if _tm_of(x[0])]
assert _ti == list(range(_ti[0], _ti[-1] + 1)), '팀 줄 사이에 다른 줄이 끼어 있음'
_blk = {t_: [x for x in LN[_ti[0]:_ti[-1] + 1] if _tm_of(x[0]) == t_] for t_ in _ORD}
LN[_ti[0]:_ti[-1] + 1] = [x for t_ in _ORD for x in _blk[t_]]
KEYS = [x[0] for x in LN]
lines, scenes = [], []
# ── 11/13 밤 대사 v7: text_1113_fa.T2 가 줄 글을 덮어쓴다. 화면 요소의 등장 시각(at = 호흡 번호.진행)은 옛 호흡의 낱말을 새 글에서 찾아 그 호흡으로 옮긴다
from text_1113_fa import T2, GAP
TPRE = {"삼성": "s", "KT": "k", "KIA": "a", "LG": "l", "두산": "d", "SSG": "x", "롯데": "r", "NC": "n", "한화": "h", "키움": "w"}
TCOL = {"삼성": ("#1E5BE0", "#7B3BFF"), "KT": ("#C8232C", "#3B3F68"), "KIA": ("#D81E37", "#6A2BD8"), "LG": ("#C30452", "#5B2BD8"), "두산": ("#2A3AA8", "#B0183C"),
        "SSG": ("#CE0E2D", "#B5821E"), "롯데": ("#0E46B0", "#D00F31"), "NC": ("#1D5FB8", "#B58A3C"), "한화": ("#F37321", "#8A2E5E"), "키움": ("#A3123A", "#5A2A9E")}
import copy
def _br(t): return [re.sub(r'^\+', '', b_).strip() for b_ in t.split(' / ')]
REMAP_LOG = []
_CONT = [False]
# 낱말 찾기로 안 맞는 줄은 '옛 호흡 → 새 호흡'을 직접 적는다
BMAP = {'o4': {0: 0, 1: 1, 3: 3}, 'g8': {0: 0, 2: 3, 4: 4}, 'k0': {0: 0, 1: 1}, 'd2b': {0: 2, 1: 4}, 'n2': {1: 3},
        'g7': {2: 3, 3: 4}, 'o3': {0: 0, 2: 2}, 's5v': {6: 5}, 'g9': {0: 0, 1: 2}, 'a3': {0: 0, 1: 3, 2: 4}, 'sf': {1: 0, 2: 2}, 'x2': {0: 3}, 'x3': {0: 0, 3: 4}, 'w3b': {0: 5}, 'd2c': {1: 4}, 'd3': {2: 2}, 'h3': {3: 2, 5: 4}, 's3b': {0: 0, 1: 3}, 'n2b': {1: 1}, 'l2': {0: 0}, 'l2b': {0: 3, 1: 5, 3: 6}, 'p3': {0: 1, 1: 1, 2: 1, 3: 5}}
def _newat(a, ob, nb, key):
    if isinstance(a, bool) or not isinstance(a, (int, float)) or a < 0 or a >= 50: return a
    bi, fr = int(a), a - int(a)
    if bi >= len(ob): return -1 if _CONT[0] else a
    if key in BMAP: v = BMAP[key].get(bi, bi) + fr; REMAP_LOG.append((key, a, round(v, 2), '지정')); return round(v, 2)
    best = None
    for j_ in [bi] + [q for d_ in (1, 2) for q in (bi + d_, bi - d_) if 0 <= q < len(ob)]:
        for w in ob[j_].split():
            w = re.sub(r'[^0-9A-Za-z가-힣%]', '', w)
            for n_ in range(len(w), 1, -1):
                hit = [i_ for i_, t_ in enumerate(nb) if w[:n_] in re.sub(r'[^0-9A-Za-z가-힣% ]', '', t_)]
                if hit:
                    if not best or n_ > best[0]: best = (n_, min(hit, key=lambda i_: abs(i_ - bi * len(nb) / len(ob))), j_, w[:n_])
                    break
        if best: break
    if best:
        v = best[1] + (fr if best[2] == bi else (.05 if best[2] > bi else .8))
        REMAP_LOG.append((key, a, round(v, 2), best[3])); return round(v, 2)
    v = round(a * len(nb) / len(ob), 2); REMAP_LOG.append((key, a, v, '비례')); return v
def _walk(o, ob, nb, key):
    if isinstance(o, dict): return {k_: (_newat(v_, ob, nb, key) if re.search(r'(^at$|At$)', k_) and not isinstance(v_, (dict, list)) else _walk(v_, ob, nb, key)) for k_, v_ in o.items()}
    if isinstance(o, list): return [_walk(v_, ob, nb, key) for v_ in o]
    return o
for j, (k, sub, sc, x) in enumerate(LN):
    if k in T2 and T2[k] != sub:
        _CONT[0] = bool(sc.get('cont')); sc = _walk(copy.deepcopy(sc), _br(sub), _br(T2[k]), k); sub = T2[k]
    _nb = _br(sub)
    if isinstance(sc.get('room'), dict) and isinstance(sc['room'].get('at'), (int, float)) and 0 <= sc['room']['at'] < 50:   # 남은 돈 카드는 '남은 돈'을 말하는 호흡에
        sc = copy.deepcopy(sc); sc['room']['at'] = next((i_ for i_, t_ in enumerate(_nb) if '남은 돈' in t_), 0) + 0.1
    if sc.get('verdict') and isinstance(sc.get('verdictAt'), (int, float)) and 0 <= sc['verdictAt'] < 50:   # 결론 띠는 결론을 말할 때(줄 끝 두 호흡 앞)
        sc = dict(sc); sc['verdictAt'] = max(0.4, len(_nb) - 2 + 0.2)
    LN[j] = (k, sub, sc, x)
    if k in GAP: x = dict(x, gapAfter=GAP[k])
    l = L(NARR(sub), re.sub(r' / \+', ' / ', sub).replace(',', '')); l.update(x); lines.append(l)
    s2 = dict(sc); s2['startLine'] = j; s2.setdefault('bg', BG_NEU)
    _tm = next((t_ for t_, pre_ in TPRE.items() if re.match(pre_ + r'(\d|f$)', k)), None)   # 팀 장(章)이면 바탕 빛을 그 팀 색으로
    if _tm: s2['tc'], s2['tc2'] = TCOL[_tm]
    scenes.append(s2)
def _pics_of(o, acc, top=True):   # PC build.py 는 img·img2·faces 만 모은다 → rows·faces 안 사진은 _pics 로 넘긴다
    if isinstance(o, dict):
        for k_, v_ in o.items():
            if top and k_ in ('img', 'img2', 'bg', '_pics'): continue
            if isinstance(v_, str) and (v_.startswith('경기/') or v_.startswith('KBO프로필/')): acc.append(v_)
            else: _pics_of(v_, acc, False)
    elif isinstance(o, list):
        for v_ in o: _pics_of(v_, acc, False)
for _s in scenes:
    _a = []; _pics_of(_s, _a)
    if _a: _s['_pics'] = [{'img': x} for x in dict.fromkeys(_a)]
for _i in range(1, len(scenes)):
    _a, _b = scenes[_i - 1], scenes[_i]
    if _b.get('cont') and _a['type'] == _b['type'] and not (_a.get('chain') and _a.get('chain') == _b.get('chain')):
        _a.setdefault('chain', 'ck%d' % _i); _b['chain'] = _a['chain']
END_SC = Q("야구자판기 · 매일 야구 이슈", _QL, logoSize=150, size=72, noQ=True, logoAt=-1)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})
scenes.append(dict(END_SC, startLine=len(lines) - 1, bg=BG_NEU))
CHT = {"삼성": "삼성, 구자욱과 원태인을 지킬 수 있을까", "KT": "KT, 이번엔 외부 FA 없다", "KIA": "기아, 김호령과 김태군", "LG": "LG, 홍창기와 박동원의 가격", "두산": "두산, 양의지라는 변수", "SSG": "SSG, 숙제는 최지훈", "롯데": "롯데, 그룹 승인이 관건", "NC": "NC, 돈은 있는데 움직일까", "한화": "한화, 노시환 결과가 먼저", "키움": "키움, 남은 돈 1위"}
CHN = {"삼성": ["구자욱", "원태인"], "KT": ["김민혁", "배정대"], "KIA": ["김호령", "김태군"], "LG": ["홍창기", "박동원"], "두산": ["양의지", "정수빈"], "SSG": ["최지훈"], "롯데": ["박승욱"], "NC": ["권희동"], "한화": ["최재훈", "박상원"], "키움": ["최주환"]}
def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
def first(prefix): return next(k for k in KEYS if k.startswith(prefix) and k[len(prefix):len(prefix) + 1].isdigit())
def last(prefix): return [k for k in KEYS if k.startswith(prefix) and k[len(prefix):len(prefix) + 1].isdigit()][-1]
CH = [{"key": "오프닝", "title": "2027 FA 28명 명단", "short": "FA 28명 명단", "from": KEYS.index("o1"), "to": KEYS.index("i4")}, ch("FA 등급과 남은 돈", "o3", "g10")]
for tm, pre in (("삼성", "s"), ("KT", "k"), ("KIA", "a"), ("LG", "l"), ("두산", "d"), ("SSG", "x"), ("롯데", "r"), ("NC", "n"), ("한화", "h"), ("키움", "w")):
    ks = [k for k in KEYS if re.match(pre + r'\d', k)]
    CH.append({"key": kn(tm), "title": CHT[tm], "short": kn(tm), "from": KEYS.index(ks[0]), "to": KEYS.index(ks[-1])})
CH += [ch("포수 FA와 외야 FA", "p1", "p4b"), ch("정리", "e0", "e3c")]
# 챕터 이음 판 칸: g7x 같은 SSG 키 충돌 방지 확인
CH.sort(key=lambda c: c['from'])
assert all(c['from'] <= c['to'] for c in CH) and all(CH[i]['to'] + 1 == CH[i + 1]['from'] for i in range(len(CH) - 1)), [(c['key'], c['from'], c['to']) for c in CH]

DESC = (f"KBO가 2026년 11월 13일 2027 FA 자격 선수 {N}명을 공시했어요. 삼성 구자욱·원태인을 포함해 A등급 {GA}명, B등급 {GB}명, C등급 {GC}명이에요. "
        "FA 등급별 보상 규칙(A·B·C)을 짧게 정리하고, 10개 구단마다 누가 FA 자격을 얻었는지, 꼭 잡아야 할 선수와 데려올 만한 선수, "
        "2027년 남은 돈(11월 13일 공시 명단 기준, 옵션·연봉 인상·래리 버드 룰은 뺀 추정)을 함께 봤어요. 마지막엔 포수·외야 FA를 포지션별로 묶었어요.\n"
        "FA 신청은 11월 15일까지, 승인 선수 공시는 11월 16일, 협상은 11월 17일부터예요.")
TAGS = ["2027 FA", "FA 명단", "FA 공시", "KBO FA", "FA 등급", "구자욱", "원태인", "최지훈", "홍창기", "박동원", "김호령", "양의지", "스토브리그", "프로야구", "KBO"]
PLAYERS = [p['name'] for p in ALL] + ["박정우", "허인서", "노시환", "김현수", "최원준", "한승택", "한준수", "박세혁", "오재원", "송성문", "유강남", "노진혁", "한현희"]
EP = {"theme": "mg", "introChapter": "오프닝", "date": "2026-11-13", "gameDate": "2026-11-13", "series": "야구롱폼", "focusTeam": "", "speed": 1.0,
      "ttsApi": True, "ttsVoice": "A", "ttsTempo": 1.2, "ttsTempoSlow": 1.15, "rev": "1113-fa-v1" + ("-PRED" if PRED else ""), "topic": "2027FA공시총정리", "endcardSec": 10,
      "gapScale": 1.45, "pauseMax": 0.55, "sentPauseMin": 0.5, "ttsCharsOk": 7000, "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False,
      "source": "명단 = " + os.path.basename(DATA) + " · 근거 = fabig/research_teams.md · 남은 돈 = cap27(11/13 공식 명단 기준)",
      "youtube": {"title": f"2027 FA 명단 공시 | {N}명 등급 총정리, 10개 구단은 누굴 지키고 누굴 노릴까?", "description": DESC,
                  "cta": "2027 FA 시장에서 가장 크게 움직일 팀은 돈이 가장 많은 키움일까요? 아니면 다른 팀일까요? 여러분은 어떻게 보세요?", "prev": "MLB 직장폐쇄 롱폼(11/13)",
                  "tags": TAGS, "hashtags": ["#2027FA", "#FA공시", "#FA명단", "#FA등급", "#스토브리그", "#KBO"],
                  "teams": ["삼성", "KT", "기아", "LG", "두산", "SSG", "롯데", "NC", "한화", "키움"], "players": PLAYERS}}
if PRED: EP['stale'] = "미리보기용 예상 명단 — 빌드·업로드 금지"

if __name__ == '__main__':
    for l in EP['lines'][:-1]:
        if len(l['narr'].split(' / ')) > 1 and len(l['sub'].split('|')[0]) <= 4: l['noMerge'] = True
    _chs = {c['from'] for c in CH}
    for i, l in enumerate(EP['lines'][:-1]):
        if l.get('gapAfter') is None and (i + 1) in _chs: l["gapAfter"] = 0.75
    out = sys.argv[-1] if sys.argv[-1].endswith('_롱폼.json') else os.path.join(HERE, 'episodes', '2026-11-13_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    json.dump(REMAP_LOG, open(os.path.join(HERE, 'remap_log.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot, '예상명단' if PRED else '공식명단')
