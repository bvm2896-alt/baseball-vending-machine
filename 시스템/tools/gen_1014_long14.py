# -*- coding: utf-8 -*-
"""10/14 롱폼⑭ 「한화 감독은 왜 20년 가까이 재계약을 못 했을까」 (음성 API · 줄별 배속)
대사 = tools/text_1014_long14.py (v2.3, 3회 검수 끝 — 프로젝트 claude/1014-롱폼14-한화감독잔혹사-대사초안v2 · -3차재검).
근거 = 프로젝트 claude/1014-롱폼14-한화감독잔혹사-최종확정. 화면 글은 약어·기호·내부 줄임말 없이(10/14 규칙).
사진(그 시절, 장면마다 다른 사진): 선수이미지/카드/H14_*.jpg — 원본·출처는 아래 SRC_PHOTO."""
import json, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import wrap, S, END, OUT
_spec = importlib.util.spec_from_file_location('t14', os.path.join(os.path.dirname(__file__), 'text_1014_long14.py'))
_t = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_t)
TEXT = [x[0] for x in _t.LINES]

CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
# 10/14: 부사 '다·못·안'을 줄 끝에 홀로 두지 않음
BAD_A = re.compile(r'(\d+만|\d+월|\b한|\b두|\b세|\b첫|\d+억|(?:^| )다|(?:^| )못|(?:^| )안)$'); BAD_B = re.compile(r'^(달러|일|명|개|경기|원)')
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
    out = []
    for p in b:
        t = re.sub(r' +', ' ', re.sub(r'(?<!\d),\s*|,(?!\d)', ' ', p)).replace('?', '').strip()
        out.append(t if '\n' in t else wrap2(t))
    return {"narr": narr, "sub": "|".join(out)}

# ── 나레이션: 아라비아 숫자 → 한글 읽기, 영문 팀명 → 한글 발음 ──
DIG = '영일이삼사오육칠팔구'
def sino(n):
    n = int(n)
    if n == 0: return '영'
    out = ''
    for v, u in ((10000, '만'), (1000, '천'), (100, '백'), (10, '십')):
        q, n = divmod(n, v)
        if q: out += ('' if q == 1 else DIG[q]) + u
    return out + (DIG[n] if n else '')
NAT = {1: '한', 2: '두', 3: '세', 4: '네', 5: '다섯', 6: '여섯', 7: '일곱', 8: '여덟', 9: '아홉', 10: '열', 11: '열한', 12: '열두', 13: '열세', 14: '열네', 15: '열다섯', 16: '열여섯', 17: '열일곱', 18: '열여덟', 19: '열아홉', 20: '스무'}
def native(n):
    n = int(n); return NAT.get(n) or sino(n)
def narr_of(t):
    t = t.replace('12.55', '십이 점 오오')
    t = re.sub(r'(\d+)년', lambda m: sino(m.group(1)) + ' 년', t)
    t = re.sub(r'(\d+)월', lambda m: sino(m.group(1)) + ' 월', t)
    t = re.sub(r'(\d+)일(?![이곱])', lambda m: sino(m.group(1)) + ' 일', t)
    t = re.sub(r'(\d+)억', lambda m: sino(m.group(1)) + ' 억', t)
    t = re.sub(r'(\d+)(승|무|패|위|이닝|회|년)', lambda m: sino(m.group(1)) + ' ' + m.group(2), t)
    t = re.sub(r'(\d+)점', lambda m: sino(m.group(1)) + ' 점', t)   # 점은 항상 한자어
    t = re.sub(r'(\d+)(경기|번|명|개|가지)', lambda m: (native(m.group(1)) if (m.group(2) in ('경기', '가지') or int(m.group(1)) < 20) else sino(m.group(1))) + ' ' + m.group(2), t)
    t = re.sub(r'(\d+)일', lambda m: sino(m.group(1)) + ' 일', t)
    for en, ko in (("KIA", "기아"), ("SSG", "에스에스지"), ("LG", "엘지"), ("KT", "케이티"), ("NC", "엔씨")):
        t = re.sub(r'(?<![A-Za-z])' + en + r'(?![A-Za-z])', ko, t)
    t = re.sub(r'(\d+)', lambda m: sino(m.group(1)), t)
    t = re.sub(r' +', ' ', t).strip()
    return ' / '.join(re.sub(r'^이 (위|승)', r'이\1', b) for b in t.split(' / '))   # 호흡 첫머리 '이 위' → '이위'(끊어 읽지 않게)
def sub_of(t):   # 자막 = 대본 그대로(아라비아 숫자). 한글로 쓴 팀명은 영문으로
    for ko, en in (("케이티", "KT"), ("엔씨", "NC"), ("에스에스지", "SSG"), ("엘지", "LG"), ("기아", "KIA")):
        t = t.replace(ko, en)
    return t

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vduo(items, **k): return dict(type="duo", items=items, **k)
RED, GOLD, GRAY, GREEN, NAVY = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55", "#3B4A63"

C = '카드/'
P = {"김인식_06": C + "H14_김인식_2006B", "김인식_06B": C + "H14_김인식_2006", "김인식_09": C + "H14_김인식_2009", "한대화_A": C + "H14_한대화_A", "한대화_B": C + "H14_한대화_B", "한대화_C": C + "H14_한대화_C", "김응용_A": C + "H14_김응용_A", "김응용_B": C + "H14_김응용_B", "김응용_C": C + "H14_김응용_C",
     "김성근_A": C + "H14_김성근_A", "김성근_B": C + "H14_김성근_B", "김성근_C": C + "H14_김성근_C", "권혁": C + "H14_권혁_A",
     "한용덕_A": C + "H14_한용덕_A", "한용덕_B": C + "H14_한용덕_B", "수베로_A": C + "H14_수베로_A", "수베로_B": C + "H14_수베로_B",
     "최원호_A": C + "H14_최원호_A", "최원호_B": C + "H14_최원호_B", "최원호_C": C + "H14_최원호_C", "박찬혁": C + "H14_박찬혁",
     "김경문_프로필": C + "FA9_김경문", "김경문_A": C + "H14_김경문_A", "김경문_B": C + "H14_김경문_B", "김경문_C": C + "H14_김경문_C", "손혁": C + "H14_손혁",
     "폰세": "상황별/폰세_한화2025", "와이스": "상황별/와이스_한화2025", "에르난데스": C + "H14_에르난데스", "짐머맨": C + "H14_짐머맨", "왕옌청": C + "FA9_왕옌청_경기",
     "조원우": C + "H14_조원우", "이동욱": C + "H14_이동욱", "김원형": C + "H14_김원형",
     "류지현_AG": C + "H14_류지현_AG", "류지현_공항": C + "H14_류지현_공항", "류지현_한화_C": C + "H14_류지현_한화_C", "류지현_한화_A": C + "H14_류지현_한화_A", "류지현_한화_B": C + "H14_류지현_한화_B", "류지현_사인": C + "H14_류지현_한화_사인",
     "류지현_LG_A": C + "H14_류지현_LG_A", "류지현_LG_B": C + "H14_류지현_LG_B"}
THUMB4 = "상황별/썸네일_롱폼4_한화"   # 롱폼④ 실제 썸네일(9/30 업로드)

def pv(i, img, name, sub, viz, **k): return S(i, "profile", img=P.get(img, img), name=name, sub=sub, stats=k.pop("stats", []), viz=viz, **k)
def pvt(i, team, sub, viz, **k): return S(i, "profile", team=team, name=team, sub=sub, stats=k.pop("stats", []), viz=viz, **k)
_SRC_LBL = re.compile(r'보도|발표|관계자|커뮤니티|^20\d\d')
def sp(i, img, name, sub, bubbles, **k):
    for b in bubbles:
        if "src" not in b: b["src"] = bool(_SRC_LBL.search(b.get("date", ""))) or "“" not in b.get("text", "")
    return S(i, "speech", img=P.get(img, img), name=name, sub=sub, bubbles=bubbles, **k)
def spt(i, team, sub, bubbles, **k):
    for b in bubbles: b.setdefault("src", True)
    return S(i, "speech", team=team, name=team, sub=sub, bubbles=bubbles, **k)
def ppl(i, items, **k): return S(i, "people", full=True, items=items, **k)
def pc(img, name, note="", **x): return dict({"img": P.get(img, img), "name": name, "note": note}, **x)

# 감독 계약 막대(김인식 뒤 정식 감독 일곱 명). a 부임 · b 계약 끝 · x 중도 퇴진
FULL, CUT = "계약 끝까지", "계약 중 퇴진"
def rows7(tags=None):
    R = [dict(name="한대화", a=2009.75, b=2012.83, x=2012.66), dict(name="김응용", a=2012.78, b=2014.83), dict(name="김성근", a=2014.82, b=2017.83, x=2017.39),
         dict(name="한용덕", a=2017.83, b=2020.83, x=2020.43), dict(name="수베로", a=2020.9, b=2023.83, x=2023.36), dict(name="최원호", a=2023.36, b=2025.83, x=2024.40),
         dict(name="김경문", a=2024.42, b=2026.78)]
    for r in R:
        r["tag"] = (tags or {}).get(r["name"], CUT if r.get("x") else FULL)
        if not r.get("x"): r["tagColor"] = GREEN
    return R
TICKS = [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026]
def contracts(i, rows=None, **k): return S(i, "contracts", rows=rows or rows7(), **dict(dict({"from": 2009.4, "to": 2027.3, "ticks": TICKS}), **k))
YL = dict(ticks=[2006, 2010, 2014, 2018, 2022, 2026])
AS = "2026 정규시즌 최종"

SC = {}
SC[0] = S(0, "yearcount", team="한화", **{"from": 2006, "to": 2026}, countAt=1, countEnd=2, stamp="감독 재계약 0번", stampAt=3, sub="마지막 재계약 2006년 11월")
SC[1] = contracts(0, title="김인식 감독 뒤 · 한화 정식 감독 7명")
SC[2] = ppl(0, [pc("김경문_프로필", "김경문", "10월 10일 계약 만료", img2=P["류지현_한화_A"], name2="류지현", note2="10월 13일 새 감독", swapAt=2.2)], fullH=520)
SC[3] = spt(0, "한화", "언론 보도", [bb("언론 보도", "“감독의 무덤”\n20년간 재계약 없다", 1)])
SC[4] = S(0, "toc", on=-1, itemFrom=1)
# 1장
SC[5] = pv(0, "김인식_06", "김인식", "한화 감독 · 2006년", [vsteps([stp("정규시즌", "3위", 1), stp("준플레이오프", "통과", 1.6), stp("플레이오프", "통과", 2), stp("한국시리즈", "준우승", 3, c="gold")])])
SC[6] = pv(0, "김인식_06B", "김인식", "한화 감독 · 2006년", [vstamp("재계약", 2, "gold")], stats=[st("재계약 날짜", "2006년 11월 5일", 0), st("계약", "3년 14억 원", 2, hi=True)])
SC[7] = S(0, "yearline", title="한화 · 감독 재계약", **{"from": 2005, "to": 2027}, **YL, chain="yl7",
          items=[dict(y=2006.85, team="한화", label="2006년 11월", c="gold", at=0)], gaps=[dict(a=2007.3, b=2026.8, label="감독 재계약 없음", at=1, c="bad")])
SC[8] = pv(0, "김인식_09", "김인식", "한화 감독 · 2009년", [vstamp("계약 만료", 2, "navy")], stats=[st("2009년 · 8개 구단", "8위 · 꼴찌", 1, hi=True)])
SC[9] = S(0, "toc", on=1)
# 2장 — 일곱 명
SC[10] = pv(0, "한대화_A", "한대화", "한화 감독 · 2010~2012", [], stats=[st("선임", "2009년 9월", 1), st("계약", "3년", 2)])
SC[11] = pv(0, "한대화_A", "한대화", "한화 감독 · 2010~2012", [vtrend([dict(x="2010년", v=8, vt="8위", c="bad", at=1), dict(x="2011년", v=6, vt="공동 6위", at=1.5), dict(x="2012년", v=8, vt="8위", c="bad", at=2)], title="한화 순위 · 8개 구단", invert=True)])
SC[12] = pv(0, "한대화_B", "한대화", "한화 감독 · 2012년 8월", [vstamp("계약 마지막 해 · 시즌 중 물러남", 1, "bad", size=58)], stats=[st("물러난 때", "2012년 8월", 0)])
SC[13] = sp(0, "한대화_C", "한대화", "2012년 8월 · 떠나며", [bb("선수들에게", "“너희들은 야구할 날이\n앞으로도 많이 남아 있으니\n남은 경기를 잘해 줬으면 좋겠다”", 1)])
SC[14] = pv(0, "김응용_A", "김응용", "한화 감독 · 2013~2014", [], stats=[st("선임", "2012년 10월", 1), st("계약", "2년 9억 원", 2)])
SC[15] = pv(0, "김응용_B", "김응용", "한화 감독 · 2013~2014", [vstamp("2년 연속 꼴찌", 1, "bad")], stats=[st("2013년 · 9개 구단", "9위 · 꼴찌", 0, hi=True), st("2014년 · 9개 구단", "9위 · 꼴찌", 0.5, hi=True)])
SC[16] = pv(0, "김응용_B", "김응용", "한화 감독 · 2013~2014", [vstamp("계약 끝까지 · 재계약 없음", 1, "navy", size=60)], stats=[st("2013년 · 9개 구단", "9위 · 꼴찌", 0, hi=True), st("2014년 · 9개 구단", "9위 · 꼴찌", 0, hi=True)])   # 10/14 사용자: 15번 화면 그대로, 도장만 빨강→파랑
SC[17] = pv(0, "김성근_A", "김성근", "한화 감독 · 2015~2017", [], stats=[st("선임", "2014년 10월", 1), st("계약", "3년 20억 원", 2)])
SC[18] = pv(0, "김성근_A", "김성근", "한화 감독 · 2015~2017", [vtrend([dict(x="2014년", v=9, vt="9위", c="bad", at=0), dict(x="2015년", v=6, vt="6위", c="good", at=1), dict(x="2016년", v=7, vt="7위", at=2)], title="한화 순위 · 10개 구단", invert=True)])
SC[19] = sp(0, "김성근_B", "김성근", "한화 감독 · 2015년", [bb("언론 보도", "투수를 너무\n빨리 바꾼다", 1)])
SC[20] = sp(0, "김성근_B", "김성근", "한화 감독 · 2015년", [bb("언론 보도", "투수를 너무\n빨리 바꾼다", -1), bb("퀵후크란", "선발이 3점 이하로 막아도\n6회가 끝나기 전에 교체", 0)], cont=True)
SC[21] = S(0, "bars", term="퀵후크가 나온 경기", title="2015년 7월 말까지", items=[dict(label="한화", team="한화", value=52, unit="경기", at=1, hi=True), dict(label="KT", team="KT", value=38, unit="경기", at=3, color=GRAY)], max=60)
SC[22] = pv(0, "권혁", "권혁", "한화 불펜 투수 · 2015년", [], stats=[st("2015년 한 해", "78경기", 1, hi=True), st("던진 이닝", "112이닝", 2, hi=True)])
SC[23] = pv(0, "김성근_C", "김성근", "한화 감독 · 2017년 5월", [vstamp("계약 마지막 해 · 시즌 중 물러남", 2, "bad", size=58)], stats=[st("물러난 때", "2017년 5월", 0), st("부임하고", "941일 만", 3)])
SC[24] = pv(0, "한용덕_B", "한용덕", "한화 감독 · 2018~2020", [], stats=[st("선임", "2017년 10월", 1), st("계약", "3년 12억 원", 2)])
SC[25] = pv(0, "한용덕_B", "한용덕", "한화 감독 · 2018년", [vstamp("11년 만의 가을야구", 1, "gold")], stats=[st("2018년 · 10개 구단", "3위", 0, hi=True)])
SC[26] = pv(0, "한용덕_A", "한용덕", "한화 감독 · 2020년 6월", [vstamp("14연패 끝에 스스로 물러남", 2, "bad", size=58)], stats=[st("2018년 · 10개 구단", "3위", -1, hi=True), st("2019년 · 10개 구단", "9위", 0, hi=True)])
SC[27] = pv(0, "수베로_A", "수베로", "한화 감독 · 2021~2023", [], stats=[st("선임", "2020년 11월", 1), st("한화", "외국인 감독", 2)])
SC[28] = pv(0, "수베로_B", "수베로", "한화 감독 · 2023년 5월", [vstamp("구단이 계약 해지", 3, "bad")], stats=[st("2021년 · 10개 구단", "10위 · 꼴찌", 0, hi=True), st("2022년 · 10개 구단", "10위 · 꼴찌", 0.4, hi=True)])
SC[29] = pv(0, "최원호_A", "최원호", "한화 감독 · 2023~2024", [], stats=[st("선임", "2023년 5월", 2)])
SC[30] = ppl(0, [pc("최원호_B", "최원호", "감독"), pc("박찬혁", "박찬혁", "대표이사", at=2)], title="2024년 5월 27일 · 같은 날 물러남", noteAt=1, ph=540)
SC[31] = sp(0, "최원호_C", "최원호", "2024년 5월 · 떠나며", [bb("선수단에", "“밖에서 응원을 많이 할 테니\n우리가 목표로 하는 포스트시즌에\n꼭 가주길 진심으로 기원한다”", 1)])
SC[32] = pv(0, "김경문_C", "김경문", "한화 감독 · 2024~2026", [], stats=[st("선임", "2024년 6월", 1), st("계약", "3년 20억 원", 2)])
SC[33] = pv(0, "김경문_C", "김경문", "한화 감독 · 2025년", [vsteps([stp("정규시즌", "2위", 0), stp("플레이오프", "통과", 0.6), stp("한국시리즈", "1승 4패 준우승", 1, c="gold")])])
SC[34] = ppl(0, [pc("폰세", "폰세", "토론토 블루제이스", at=1), pc("와이스", "와이스", "휴스턴 애스트로스", at=1.4)], title="2025년 에이스 둘 · 시즌 전 메이저리그로", noteAt=3, ph=540)
SC[35] = S(0, "rankstrip", team="한화", title="2026 한화", asof=AS, rows=[dict(k="전반기", v="40승 2무 40패", rank=6, at=0), dict(k="최종", v="57승 4무 83패", rank=9, at=99)])
SC[36] = ppl(0, [pc("에르난데스", "에르난데스", "7월 19일\n방출", at=1), pc("짐머맨", "짐머맨", "9월 28일까지\n평균자책점 12.55", at=2)], title="외국인 투수 교체", noteAt=1, ph=540)
SC[37] = S(0, "rankstrip", team="한화", title="한화 불펜", asof=AS, rows=[dict(k="세이브", v="16개 · 최소", rank=10, at=1)])
SC[38] = pv(0, "왕옌청", "왕옌청", "한화 투수 · 대만", [vstamp("아시안게임 대만 대표", 2, "bad")], stats=[st("팀 내 최다", "11승", 0, hi=True)])
SC[39] = S(0, "rankstrip", team="한화", title="2026 한화", asof=AS, rows=[dict(k="전반기", v="40승 2무 40패", rank=6, at=0), dict(k="최종", v="57승 4무 83패", rank=9, at=0.5)])
SC[40] = sp(0, "김경문_A", "김경문", "2026년 10월 · 마지막 경기 앞두고", [bb("", "“팀을 좀 더 단단하게\n만들지 못하고 나가는 게\n감독으로서 죄송하다”", 1)])
SC[41] = ppl(0, [pc("김경문_B", "김경문", "감독\n계약 만료"), pc("손혁", "손혁", "단장\n계약 만료", at=2)], title="2026년 10월 10일 · 같은 날", noteAt=2, ph=540)
SC[42] = spt(0, "한화", "구단 발표", [bb("구단 발표", "계약 만료\n이유는 밝히지 않음", 0)])
SC[43] = contracts(0, title="김인식 감독 뒤 · 한화 정식 감독 7명", label="계약을 끝까지 채운 감독 2명")
_LAST = {n: "마지막 해 시즌 중 퇴진" for n in ("한대화", "김성근", "한용덕", "수베로")}
SC[44] = contracts(0, rows=rows7(_LAST), title="김인식 감독 뒤 · 한화 정식 감독 7명", label="4명 · 계약 마지막 해 시즌 중 퇴진", cont=True)
SC[45] = contracts(0, rows=rows7(_LAST), title="김인식 감독 뒤 · 한화 정식 감독 7명", label="김경문 · 계약은 채웠지만 재계약 없음", cont=True)
SC[46] = S(0, "toc", on=2)
# 3장
_I1 = [dict(y=2025.87, teams=["LG", "삼성"], label="2025년 11월", at=3, c="good"), dict(y=2025.7, team="SSG", label="2025년 9월", at=4, c="good"), dict(y=2024.87, team="KIA", label="2024년 11월", at=5, c="good")]
_I2 = _I1 + [dict(y=2023.8, team="KT", label="2023년", at=0), dict(y=2022.87, team="키움", label="2022년", at=1), dict(y=2021.6, teams=["NC", "롯데"], label="2021년", at=2), dict(y=2019.82, team="두산", label="2019년", at=3)]
_YL3 = dict(title="10개 구단 · 마지막 감독 재계약", **{"from": 2005, "to": 2027}, **YL, chain="yl3", asof="2026년 10월 14일 기준")
SC[47] = S(0, "yearline", items=_I1, ghost=True, **_YL3)
SC[48] = S(0, "yearline", items=_I2, cont=True, ghost=True, **_YL3)
SC[49] = S(0, "yearline", items=_I2 + [dict(y=2006.85, team="한화", label="2006년 11월", at=1, c="bad", row=0)], brace=dict(a=2006.85, b=2019.82, label="13년 가까이", at=3), cont=True, ghost=True, **_YL3)
SC[50] = pvt(0, "LG", "LG 트윈스 감독 재계약", [vsteps([stp("1999년", "재계약", 0), stp("26년 동안", "재계약 없음", 0.4, c="bad"), stp("2025년 11월", "재계약", 1, c="good")])])
_P3 = [pc("조원우", "조원우", "롯데\n2017년 재계약\n2018년 경질"), pc("이동욱", "이동욱", "NC\n2021년 연장\n2022년 경질"), pc("김원형", "김원형", "SSG\n2022년 재계약\n2023년 경질")]
SC[51] = ppl(0, [dict(x, at=99) for x in _P3], title="재계약하면 오래 갈까?", noteAt=99, ph=480)
SC[52] = ppl(0, [dict(x, at=k) for k, x in enumerate(_P3)], title="재계약하면 오래 갈까?", noteAt=3, cont=True, ph=480)
SC[53] = S(0, "icontiles", title="한화 감독들의 공통점", items=[dict(icon="calendar", v="계약을 다 못 채움", k="공통점 1", at=3), dict(icon="doc", v="윗선도 같이 바뀜", k="공통점 2", at=3.4)])
SC[54] = contracts(0, title="김인식 감독 뒤 · 한화 정식 감독 7명", label="7명 중 5명 · 계약 도중 퇴진", labelAt=3)
_D = [dict(y=2014.8, label="2014년", at=3), dict(y=2020.9, label="2020년", at=3.3), dict(y=2024.4, label="2024년", at=4), dict(y=2026.78, label="2026년", at=4.3)]   # 10/14: '둘째 /' 호흡이 하나 늘어 +1
_YL5 = dict(title="감독이 바뀔 때 · 대표이사나 단장도 한 달 안에", **{"from": 2013, "to": 2027}, ticks=[2014, 2016, 2018, 2020, 2022, 2024, 2026], chain="yl5")
SC[55] = S(0, "yearline", dots=_D, **_YL5)
SC[56] = S(0, "yearline", dots=_D[:2] + [dict(y=2024.4, label="2024년\n같은 날", at=0, big=True), dict(y=2026.78, label="2026년\n같은 날", at=0.5, big=True)], cont=True, **_YL5)
SC[57] = spt(0, "한화", "2024년 · 야구계 관계자", [bb("야구계 관계자", "“사람을 너무 자주 바꾼다”", 2)])
SC[58] = S(0, "toc", on=3)
# 4장 류지현
SC[59] = pv(0, "류지현_공항", "류지현", "야구 대표팀 감독 · 2026년 9월", [vstamp("아시안게임 금메달", 3, "gold")], stats=[st("아시안게임", "2026년 9월", 1)])
SC[60] = sp(0, "류지현_사인", "류지현", "한화 감독 · 2026년 10월 13일", [bb("계약", "3년 20억 원", 1, src=True), bb("구단 발표", "지속 가능한 강팀을 만들\n적임자", 2)])
SC[61] = sp(0, "류지현_사인", "류지현", "한화 감독 · 2026년 10월 13일", [bb("", "“한화 이글스라는 좋은 팀의\n감독을 맡겨주신 구단에\n감사드린다”", 1)])
SC[62] = pv(0, "류지현_LG_A", "류지현", "LG 감독 · 2021~2022", [vstamp("재계약 못 함", 1, "bad")])
SC[63] = pv(0, "류지현_LG_A", "류지현", "LG 감독 · 2022년", [vsteps([stp("2022년", "87승 · 정규시즌 2위", 1), stp("플레이오프", "1승 3패 탈락", 3, c="bad"), stp("그 뒤", "재계약 못 함", 4, c="bad")])])
SC[64] = sp(0, "류지현_LG_B", "류지현", "LG 감독 · 2022년 11월", [bb("", "“우승에 대한 약속을\n지키지 못한 점\n다시 한번 죄송하다”", 1)])
SC[65] = pv(0, "류지현_한화_B", "류지현", "한화 감독 · 2026년 10월부터", [vduo([dict(icon="person", v="재계약 못 함", k="LG · 2022년", at=0, c="bad"), dict(icon="person", v="재계약 0번", k="한화 · 2006년 이후", at=1, c="bad")])])
SC[66] = sp(0, "류지현_한화_B", "류지현", "한화 감독 · 2026년 10월부터", [bb("", "“마무리 훈련부터 내년 시즌\n도약을 위해 준비하겠다”", 1)])
# 마무리
_R8 = rows7() + [dict(name="류지현", a=2026.79, b=2029.8, empty=True)]
SC[67] = contracts(0, rows=_R8, **{"to": 2030.3}, ticks=TICKS + [2028, 2030], title="김인식 감독 뒤 · 한화 감독 8명째", label="7명 중 5명 · 계약 도중 퇴진")
SC[68] = S(0, "question", text="재계약 기록을 끊을까?\n재계약 없이 떠날까?", img=P["류지현_한화_C"], size=72)
SC[69] = S(0, "question", text="한화 순위 이야기\n여기를 눌러 확인", img=THUMB4, ph=495, size=72, arrow="left")

assert len(TEXT) == 71 and TEXT[-1] == '__CTA__', len(TEXT)
lines, scenes = [], []
for j, t in enumerate(TEXT[:-1]):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))
for s in scenes:   # 목차 소개 줄 검사 — itemFrom 부터 칸 수만큼 호흡이 있어야 함
    if s['type'] == 'toc' and s.get('on', -1) < 0 and s.get('itemFrom', 1) < 50:
        nbr = len(lines[s['startLine']]['narr'].split(' / ')); assert nbr >= s.get('itemFrom', 1) + 4, s

CH = [{"key": "마지막 재계약", "title": "마지막 재계약", "from": 5, "to": 8},
      {"key": "일곱 명의 감독", "title": "일곱 명의 감독", "from": 9, "to": 45},
      {"key": "왜 반복될까", "title": "왜 반복될까", "from": 46, "to": 57},
      {"key": "류지현은 다를까", "title": "류지현은 다를까", "from": 58, "to": 66}]

TAGS = ["한화 감독", "한화 감독 재계약", "한화 이글스", "류지현", "류지현 감독", "김경문", "김성근", "한용덕", "수베로", "최원호", "한대화", "김응용", "김인식",
        "프로야구 감독", "감독 재계약", "프로야구", "KBO", "2026 프로야구", "야구자판기"]
DESC = ("한화 이글스의 마지막 감독 재계약은 2006년 11월 김인식 감독(3년 14억 원)이에요. 그 뒤 한화를 맡은 정식 감독 일곱 명 가운데 재계약한 감독은 한 명도 없어요.\n"
        "한화 감독은 왜 20년 가까이 재계약을 못 했을까요? 일곱 명의 감독이 어떻게 떠났는지, 다른 구단과 비교하면 어떤지, 그리고 새 감독 류지현은 다를지 봤어요.\n\n"
        "한대화·김성근·한용덕·수베로 감독은 계약 마지막 해 시즌 도중에 물러났고, 최원호 감독은 1년 만에 물러났어요. 계약을 끝까지 채운 감독은 김응용·김경문 두 명뿐이에요. 김경문 감독은 2025년 정규시즌 2위·한국시리즈 준우승을 이끌었지만, 2026년 9위로 마친 뒤 10월 10일 계약 만료로 떠났어요.\n\n"
        "10개 구단의 마지막 감독 재계약(연장 포함)을 모아 보면 LG·삼성 2025년 11월, SSG 2025년 9월, KIA 2024년 11월, KT 2023년, 키움 2022년, NC·롯데 2021년, 두산 2019년이에요. 한화는 2006년으로, 두 번째로 오래된 두산보다도 13년 가까이 더 오래됐어요(2026년 10월 14일 기준).\n\n"
        "류지현 감독은 2026년 9월 아시안게임에서 야구 대표팀 금메달을 이끌었고, 10월 13일 한화와 3년 20억 원에 계약했어요. LG 감독이던 2022년엔 구단 최다 87승으로 정규시즌 2위를 했지만 플레이오프에서 탈락해 재계약하지 못했어요.\n\n"
        "야구자판기는 매일 오늘의 야구 이슈를 정리해 드려요.\n\n"
        "류지현 감독은 한화의 재계약 기록을 끊을까요, 아니면 앞선 감독들처럼 재계약 없이 떠나게 될까요? 댓글로 알려 주세요.\n\n"
        "기록: KBO 기록실 2026 정규시즌 최종(팀 세이브·순위), 퀵후크 집계 OSEN 2015-07-30\n"
        "사진: 한화 이글스 제공(김성근·한용덕·수베로·최원호·김경문·손혁·박찬혁·에르난데스·짐머맨·폰세·와이스·왕옌청·류지현), 롯데 자이언츠 제공(조원우), NC 다이노스 제공(이동욱), SSG 랜더스 제공(김원형), LG 트윈스 제공(류지현), 마이데일리(김인식 2006)·이데일리(김인식 2009·한대화 2010·김응용 2013)·일간스포츠(김응용), MK스포츠·마이데일리(한대화 2012), SPOTV NEWS(권혁 2015), 스포츠조선(류지현 2022), 연합뉴스(류지현 2026년 9월 귀국) / 썸네일: 한화 이글스 제공·이데일리·일간스포츠")
SOURCE = ("사실 출처 = 프로젝트 claude/1014-롱폼14-한화감독잔혹사-최종확정 · -3차재검. 사진 원본 = 다음 뉴스 게재 구단 제공 사진(캡션 '○○ 제공'), 게재 매체: 스포츠경향·국민일보·스타뉴스·대전일보·연합뉴스·스포츠동아·일간스포츠·조선일보·한겨레·MBC·OSEN.")

EP = {"date": "2026-10-14", "gameDate": "2026-10-12", "series": "야구롱폼", "focusTeam": "한화", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1014-long14-v1", "topic": "한화감독잔혹사", "gapScale": 1.05, "pauseMax": 0.4, "ttsCharsOk": 4500,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "source": SOURCE,
      "youtube": {"title": "한화 감독은 왜 20년 가까이 재계약을 못 했을까 | 김인식 뒤 7명, 그리고 류지현 #한화이글스 #프로야구",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#한화이글스", "#한화감독", "#류지현", "#김경문", "#김성근", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 1, 7, 43, 49, 54, 67, 68}
    HOLD = {j: 0.5 for j, s in enumerate(scenes) if s['type'] == 'toc' and j > 4}
    HOLD.update({0: 0.6, 7: 0.6, 49: 0.6, 68: 0.6})
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-14_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
