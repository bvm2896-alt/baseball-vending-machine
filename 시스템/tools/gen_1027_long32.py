# -*- coding: utf-8 -*-
"""10/27 롱폼㉜ 「플레이오프 2차전 리뷰 · 3차전 승부예측」 콘티 — 경기 전 준비판(3차전 예상 장). 아래 설명은 롱폼㉛에서 이어 온 틀.
(이전: 10/26 롱폼㉛ 콘티 v2 (가로 16:9 · 집 PC template_long.html 10/25판).
대사 = tools/text_1026_long31.py. 근거 = 프로젝트 claude/1026-롱폼31-PO1차전리뷰-근거모음-경기뒤.md(기사 본문 2곳 이상).
화면: 득점 장면은 다이아몬드(diamond)·홈런 카메라(hrcam), 한 사람 구간은 한 사진 묶음(chain), 기록은 칸(stats)·줄(steps).
사진: 사진 은행(카드/P17·P18·P20·P22·P31·FA9·FA10, 경기/구자욱_세리머니) — 이날 경기 사진은 없음(집 PC 연결 뒤 크롬으로 받으면 교체).
사진 없는 선수(정해영·이의리·조상우·곽도규·박승규·김영웅·강민호·이재현·김성윤)는 다이아몬드·팀 카드로만 — 얼굴 칸을 비우지 않는다.
썸네일 = 썸네일러가 미리 만듦(사용자 10/26 21:50) → thumb 없음, thumbFile 은 PC 넣을 때 사용자 파일 이름으로."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('\ndef sub_of')].replace("'text_1015_long15.py'", "'text_1027_long32.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]; KEYS = [x[1] for x in LINES]
import narr_1020
_NU = ['', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉']; _NT = ['', '열', '스물', '서른', '마흔', '쉰', '예순', '일흔', '여든', '아흔']
def _native(n): n = int(n); return _NT[n // 10] + _NU[n % 10] if 0 < n < 100 else None
def narr_of(t):
    t = t.replace('오후 6시 반', '오후 여섯 시 반').replace('8번뿐', '여덟 번뿐').replace('26일 월요일', '이십육 일 월요일')
    if t.startswith('2, / '): t = '둘, / ' + t[5:]
    t = t.replace('MVP', '엠브이피').replace('77.1%', '칠십칠 점 일 퍼센트').replace('5.25', '오 점 이오').replace('3.13', '삼 점 일삼').replace('1.17', '일 점 일칠')
    t = t.replace('2아웃', '투 아웃').replace('1아웃', '원 아웃').replace('3·4차전', '삼, 사차전').replace('2만 3550석', '이만 삼천오백오십 석').replace('146km', '백사십육 킬로').replace('120m', '백이십 미터')
    t = t.replace('2할 1푼 4리', '이할 일푼 사리').replace('1할 9푼', '일할 구푼')
    t = t.replace('8점대', '팔 점대').replace('3과 3분의 1이닝', '삼과 삼분의 일 이닝').replace('8.10', '팔 점 일영').replace('11.16', '십일 점 일육').replace('3.68', '삼 점 육팔').replace('4.75', '사 점 칠오')
    t = t.replace('4.19', '사 점 일구').replace('4.52', '사 점 오이').replace('5와 3분의 2이닝', '오와 삼분의 이 이닝').replace('5와 3분의 1이닝', '오와 삼분의 일 이닝')
    for a_, b_ in (('4와 3분의 2이닝', '사와 삼분의 이 이닝'), ('4와 3분의 1이닝', '사와 삼분의 일 이닝'), ('1과 3분의 1이닝', '일과 삼분의 일 이닝'), ('3분의 1이닝', '삼분의 일 이닝'), ('11월 1일', '십일월 일일')):
        t = t.replace(a_, b_)
    _S = '영 일 이 삼 사 오 육 칠 팔 구 십'.split()
    t = re.sub(r'(?<!\d)(\d)대(\d)(?!\d)', lambda m: _S[int(m.group(1))] + ' 대 ' + _S[int(m.group(2))], t)
    t = re.sub(r'(?<![\d.])(\d{1,2})(경기|명|개)', lambda m: (_native(m.group(1)) + ' ' + m.group(2)) if _native(m.group(1)) else m.group(0), t)
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타|타점|득점|볼넷|구째|구)(?![가-힣]*차전)', r'\1\2', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오) (차전|연승|연패)', r'\1\2', n)
    n = n.replace('분의 이이닝', '분의 이 이닝').replace('분의 일이닝', '분의 일 이닝')
    n = n.replace('KT', '케이티').replace('KIA', '기아').replace('LG', '엘지').replace('SK', '에스케이')
    n = n.replace('십일 월', '십일월').replace('십이 월', '십이월')
    n = n.replace('삼십오 번 중 이십칠 번', '서른다섯 번 중 스물일곱 번').replace('쩜', ' 점 ').replace('사 분의 일', '사분의 일').replace('십삼 대일', '십삼 대 일')
    n = re.sub(r'(?<![가-힣])(일|이|삼) 루', r'\1루', n)
    n = re.sub(r'(?<![가-힣])((?:[이삼사오육칠팔구]?십)?[일이삼사오육칠팔구]) (위|승)(?![가-힣])', r'\1\2', n)
    n = re.sub(r'(?<![가-힣])((?:[이삼사오육칠팔구]?십)?[일이삼사오육칠팔구]) (승|위)(?=[ ,으을이])', r'\1\2', n)
    for d in ('이십오', '십이', '이십칠', '이십팔', '이십구', '삼십', '이십'):
        n = re.sub('(?<![가-힣])' + d + r' 일(?=[ 이과,은에]|$)', d + '일', n)
    n = re.sub(r'(?<![가-힣])((?:[이삼사오육칠팔구]?십)?[일이삼사오육칠팔구]) 위', r'\1위', n)
    n = n.replace('일월요일', '일 월요일')
    n = re.sub(r'(?<![가-힣])([일이삼사오육칠팔구])회말', r'\1회 말', n)  # 10/27 사용자: 오회말→'오휘말'로 들림
    n = n.replace('볼넷', '볼 넷')   # 10/27 사용자: '뽈넷'으로 읽혀서 띄어 씀
    return n
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / ')).replace('3과 3분의 1이닝', '3⅓이닝').replace('5와 3분의 2이닝', '5⅔이닝').replace('5와 3분의 1이닝', '5⅓이닝').replace('4와 3분의 2이닝', '4⅔이닝').replace('4와 3분의 1이닝', '4⅓이닝').replace('1과 3분의 1이닝', '1⅓이닝').replace('3분의 1이닝', '⅓이닝')

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vq(date, text, at, src=True, **k): return dict(type="quote", date=date, text=text, at=at, src=src, **k)
def vduo(items, **k): return dict(type="duo", items=items, **k)
def toc(on, **k): return S(0, "toc", on=on, **k)
def g5(**k): return dict(**k)
def hide(xs): return [dict(x, at=-1) for x in xs]
C = '카드/'
NAIL, FED, KDY, CAS, NA, HJS = C + "P17_네일_역투C", C + "P22_페덱_투구", C + "P17_김도영_질주", C + "P18_카스트로_환호", C + "P18_나성범_적시타", C + "P22_한준수_솔로"
JSH, OLLER, HUR, ISM, DIAZ, CHOI = C + "P18_전상현_역투", C + "P18_올러_투구", C + "P20_후라도_투구", C + "P31_이승민_삼성제공", C + "FA9_디아즈_경기", C + "FA10_최형우_100타점"
GJU = "경기/구자욱_세리머니_0827_삼성제공"
NAIL2, FED2, KDY2, KDY3, CAS2, HJS2 = C + "P17_네일_투구", C + "FA9_페덱_환호", C + "P22_김도영_만루포환호", "경기/김도영_세리머니_1017_KIA제공", C + "P18_카스트로_엄지", C + "P18_한준수_세리머니"
OLLER2, HUR2, KJY = C + "P18_올러_포효", "경기/후라도_경기_1019_삼성제공", C + "T12_김재윤"
PJM, WTI = C + "P22_박진만_더그아웃", C + "P29_원태인_2026"
SSB, KIAC = "#074CA1", "#C70125"
def pv(img, name, sub, viz=(), stats=(), team="KIA", **k): return S(0, "pstat", img=img, team=team, name=name, sub=sub, viz=list(viz), stats=list(stats), **k)
def tm(team, name, sub, viz=(), stats=(), **k): return pv(None, name, sub, viz, stats, team=team, **k)
def dm(title, bat, score, outs, steps, **k): return S(0, "diamond", title=title, bat=bat, batIdx=(1 if bat == "삼성" else 0), score=score, outs=outs, steps=steps, away="KIA", home="삼성", **k)
N3 = [None, None, None]
BOX = [{"team": "KIA", "runs": [2, 0, 2, 1, 0, 0, 0, 0, 0], "r": 5, "hi": True}, {"team": "삼성", "runs": [0, 0, 0, 0, 1, 0, 0, 0, 0], "r": 1}]
PO1 = [g5(n="1차전 · 26일", venue="대구", home="삼성", win="KIA", at=0), g5(n="2차전 · 27일", venue="대구", home="삼성", at=0),
       g5(n="3차전 · 29일", venue="광주", home="KIA", at=0), g5(n="4차전 · 30일", venue="광주", home="KIA", at=0), g5(n="5차전 · 11월 1일", venue="대구", home="삼성", at=0)]


K = {}
R2 = getattr(_g['_t'], 'R2', 'KIA'); KW = R2 == 'KIA'
TODO = lambda: tm("KIA", "TODO", "경기 뒤 채움", [], [])
YHJ, WTI2, LBH = "경기/양현종_글러브_1012_KIA제공", "경기/원태인_역투_삼성제공", C + "P22_이범호_기자회견"
# ── 오프닝·1장·2장 (경기 뒤 채움) ──
K['o0'] = TODO(); K['o1'] = TODO()
K['o6'] = toc(-1)
K['g0'] = toc(0); K['g1'] = TODO()
K['r0'] = toc(1); K['r1'] = TODO()
# ── 3장 · 3차전 예상 (경기 전 준비 · R2 두 벌) ──
K['c0'] = toc(2)
G3 = [dict(PO1[0]), dict(PO1[1], win=R2), dict(PO1[2], tag=("이기면 한국시리즈" if KW else "먼저 2승"), at=(3.0 if KW else 4.0), **({"glow": "KIA", "glowAt": 3.0} if KW else {})), dict(PO1[3]), dict(PO1[4])]
K['c1'] = S(0, "series5", tc={"삼성": SSB}, title=("플레이오프 · KIA 2승" if KW else "플레이오프 · 1승 1패"), games=G3, pills=[dict(label="3차전 · 10월 29일(목) 오후 6시 30분 · 광주", at=1.0, c="#12161F")])
if KW:
    K['c2'] = S(0, "tline", title="플레이오프 2연패 뒤 3연승 · 역대 3번", items=[dict(d="1996년", t="현대", at=2.0), dict(d="2009년", t="SK", at=3.0), dict(d="2023년", t="KT", at=4.0, c="bad", big=True)])
else:
    K['c2'] = S(0, "tline", title="역대 5전 3선승제 플레이오프", items=[dict(d="1차전 · 2차전", t="1승 1패", at=1.0), dict(d="3차전", t="승리", at=1.4), dict(d="한국시리즈 진출", t="절반 조금 넘게", at=2.0, c="gold", big=True)])
SRK, CWT = C + "P22_시라카와_투구", "상황별/최원태_KIA전_0908_삼성제공"
K['c3'] = S(0, "people", title="3차전 선발 후보 · 10월 28일 발표", items=[dict(img=YHJ, name="양현종", note="KIA", at=3.0), dict(img=SRK, name="시라카와", note="KIA", at=3.4),
              dict(img=WTI2, name="원태인", note="삼성 · 유력", at=5.0), dict(img=CWT, name="최원태", note="삼성", at=6.0)], chain="c3")
K['c3b'] = dict(K['c3'], items=[dict(x, at=-1) for x in K['c3']['items']])
def card(P, viz=(), stats=()):
    """후보 한 명 = '○○가 나오면' 카드. 장면마다 그 줄에서 새로 생기는 칸만 적는다 — 앞 줄 칸은 -1, 뒤 줄 칸은 자리만(50)으로 아래 묶음 처리가 채운다"""
    return pv(P[0], P[1], P[3], list(viz), list(stats), team=P[2])
def good(k, v, at): return vduo([dict(k=k, v=v, at=at, c="good")])
def bad(k, v, at): return vduo([dict(k=k, v=v, at=at, c="bad")])
PA = (YHJ, "양현종", "KIA", "3차전 후보 · KIA")
K['cA1'] = card(PA, [], [])
K['cA2'] = card(PA, [good("올해 정규시즌 삼성전 2경기 · 모두 광주", "두 번 다 1실점 이하", 0.3), vstamp("삼성전 강세", 1.0, "gold", size=50)])
K['cA3'] = card(PA, [bad("2024 한국시리즈 5차전 · 광주", "홈런 3방 · 5실점", 2.0)], [st("2024 한국시리즈 2차전 · 광주", "5⅓이닝 1자책 승", 1.0)])
K['cA4'] = card(PA, [], [st("정규시즌 통산", "198승 · 200승까지 2승", 1.0, hi=True)])
PB = (SRK, "시라카와", "KIA", "3차전 후보 · KIA")
K['cB1'] = card(PB, [vstamp("가을 기세", 1.0, "gold", size=50)])
K['cB2'] = card(PB, [good("준PO 3차전 · 5이닝 1실점 · 삼진 9개", "아시아쿼터 첫 PS 승", 0.3)], [st("올해 정규시즌 삼성전", "평균자책점 3.68", 4.0, hi=True)])
K['cB3'] = card(PB, [bad("올해 정규시즌 전체 · 4승 5패", "평균자책점 4.75", 1.0)])
PC = (WTI2, "원태인", "삼성", "3차전 후보 · 삼성")
K['cC0'] = card(PC, [vq("박진만 감독", "2차전 불펜으로 안 나가면 3차전 선발", 3.0)], [])
K['cC1'] = card(PC, [bad("올해 정규시즌 KIA전 · 광주", "5⅔이닝 6실점", 2.0), vstamp("KIA 타선과 재대결", 1.0, "gold", size=50)])
K['cC2'] = card(PC, [good("2024 한국시리즈 1차전 · 광주 · 비로 멈추기 전", "5이닝 무실점", 0.3)])
PD = (CWT, "최원태", "삼성", "3차전 후보 · 삼성")
K['cD1'] = card(PD, [bad("올해 정규시즌 KIA전", "평균자책점 8점대", 2.0)], [])
K['cD2'] = card(PD, [good("2025 준PO · PO 2차전", "6이닝 무실점 · 7이닝 1실점", 3.6)], [st("2024년까지 가을", "평균자책점 11.16", 1.0)])
K['cD3'] = card(PD, [vstamp("가을엔 기복", 0.4, "gold", size=50)], [st("2025 PO 5차전", "3⅓이닝 5실점", 0.3)])
K['c12'] = S(0, "gamestrip", gat=[3.0, 3.2, 3.4, 4.0, 4.2], teams={"K": "KIA"}, games=[["1차전", "K"], ["2차전", "K"], ["5차전", "K"], ["1차전", "K"], ["2차전", "K"]], sw=240, title="KIA · 광주 가을야구",
             groups=[{"from": 0, "to": 2, "label": "2024 한국시리즈 · 광주", "team": "KIA", "at": 2.0}, {"from": 3, "to": 4, "label": "2026 준PO · 광주", "team": "KIA", "at": 4.0}])
# ── 4장 · 3차전 키플레이어 (경기 뒤) ──
K['c13'] = TODO()
K['k0'] = toc(3); K['k1'] = TODO()
K['z0'] = TODO()
K['z1'] = S(0, "question", text=("3차전 광주\nKIA 끝낼까? 삼성 반격?" if KW else "3차전\n먼저 2승은 누구?"), logos=["KIA", "삼성"], logoSize=230, size=104)
missing = [k for k in KEYS if k not in K]; extra = [k for k in K if k not in KEYS]
assert not missing and not extra, (missing, extra)
SC = [K[k] for k in KEYS]
IDX = {k: i for i, k in enumerate(KEYS)}

CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
SLOW = set()
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    if sc.get('type') == 'hrcam' and j > 0 and SC[j - 1].get('type') == 'hrcam' and SC[j - 1].get('chain') == sc.get('chain'): sc['launchLine'] = scenes[-1].get('launchLine', j - 1)
    if j > 0 and sc.get('chain') and SC[j - 1].get('chain') == sc['chain']: sc['cont'] = True
    l = L(narr_of(t), sub_of(t))
    if j in SLOW: l['pace'] = 'slow'
    lines.append(l); scenes.append(sc)
lines.append(dict(CTA_LINE))

# 10/27 사용자("같은 장면인데 틀 크기도 바꿔서 뚝뚝 끊기는 느낌 — 한 장면에서 다 보여줘도 되는 건데"):
# 같은 사람 pstat 이 이어지면 한 장면으로 묶는다 — 사진·소개 줄은 첫 장면 것, 모든 칸은 처음부터 자리를 잡고(뒤 칸은 at 50) 말할 때 생긴다.
def _norm(x):
    if isinstance(x, dict): return {k: _norm(v) for k, v in x.items() if k not in ('at', 'hi', 'tagAt')}
    if isinstance(x, list): return [_norm(v) for v in x]
    return x
def _setat(x, v):
    if isinstance(x, dict): return {k: (v if k == 'at' else _setat(w, v)) for k, w in x.items()}
    if isinstance(x, list): return [_setat(w, v) for w in x]
    return x
MERGE_LOG = []
i = 0
while i < len(scenes):
    j = i
    while j + 1 < len(scenes) and scenes[j + 1].get('type') == 'pstat' == scenes[i].get('type') and scenes[j + 1].get('name') == scenes[i].get('name') and scenes[j + 1].get('team') == scenes[i].get('team'): j += 1
    if j > i:
        run = scenes[i:j + 1]
        for fld in ('viz', 'stats'):
            U = []
            for k, sc in enumerate(run):
                for x in sc.get(fld, []):
                    key = json.dumps(_norm(x), ensure_ascii=False, sort_keys=True)
                    if key not in [u[0] for u in U]: U.append((key, k))
            for k, sc in enumerate(run):
                own = {json.dumps(_norm(x), ensure_ascii=False, sort_keys=True): x for x in sc.get(fld, [])}
                new = []
                for key, first in U:
                    src = next(r for r in run if any(json.dumps(_norm(x), ensure_ascii=False, sort_keys=True) == key for x in r.get(fld, [])))
                    proto = next(x for x in src.get(fld, []) if json.dumps(_norm(x), ensure_ascii=False, sort_keys=True) == key)
                    new.append(own[key] if key in own else _setat(proto, -1 if first < k else 50))
                sc[fld] = new
        for sc in run[1:]:
            for fld in ('img', 'sub', 'focus'):
                if fld in run[0]: sc[fld] = run[0][fld]
                elif fld in sc: del sc[fld]
            sc['cont'] = True
        MERGE_LOG.append((i, j, scenes[i].get('name'), len(run[0].get('viz', [])), len(run[0].get('stats', []))))
    i = j + 1

def _ch(key, title, a, b): return {"key": key, "title": title, "from": IDX[a], "to": IDX[b]}
CH = [_ch("2차전 흐름", "2차전 흐름", "g0", "g1"), _ch("승부를 가른 이유", "승부를 가른 이유", "r0", "r1"), _ch("3차전 예상", "3차전 예상", "c0", "c13"), _ch("3차전 키플레이어", "3차전 키플레이어", "k0", "z1")]

TAGS = ["플레이오프", "플레이오프 2차전", "플레이오프 3차전", "KIA 삼성", "기아 삼성", "KIA 타이거즈", "삼성 라이온즈", "양현종", "원태인", "3차전 선발", "올러", "후라도", "프로야구", "KBO", "야구자판기"]
DESC = ("TODO 경기 뒤 — 2차전 결과 요약 두 줄\n\n"
        "3차전: 10월 29일(목) 오후 6시 30분 광주 기아챔피언스필드. 선발 공식 발표는 10월 28일 — 유력 KIA 양현종(정규시즌 12승 6패·4.19, 통산 198승) vs 삼성 원태인(7승 9패·4.52).\n"
        "이범호 감독: 양현종은 대구보다 광주 3·4차전에. 박진만 감독: 원태인은 2차전에 안 나가면 3차전 선발.\n"
        "올해 맞대결: 양현종 삼성전 2경기 모두 광주·1실점 이하, 원태인 KIA전 1경기(광주) 5⅔이닝 6실점. 2024 한국시리즈 광주: 원태인 1차전 5이닝 무실점, 양현종 2차전 5⅓이닝 1자책.\n\n"
        "기록 출처: 일간스포츠·스포티비뉴스·스포츠한국·머니투데이·세계일보·마이데일리·스포츠경향·뉴스핌·톱스타뉴스·이투데이(2026/10), OSEN·더팩트·MK스포츠·스포츠월드(2024 한국시리즈)\n"
        "사진 출처: 구단 제공")
SOURCE = "사실 출처 = 프로젝트 claude/1027-롱폼32-PO2차전리뷰-3차전예측-근거모음.md(기사 본문 2곳 이상)."
PINNED = "TODO 경기 뒤 — 3차전 질문 👇 댓글로 남겨 주세요!\n매일 야구 이슈 받아보려면 구독 + 알림 설정 부탁드려요 ⚾"

EP = {"introChapter": "오프닝", "date": "2026-10-27", "gameDate": "2026-10-27", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.15,
      "rev": "1027-long32-pre", "topic": "PO2차전리뷰", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 9000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "TODO 플레이오프 2차전 리뷰 | 3차전 승부예측 양현종 vs 원태인 #KIA #삼성",
                  "description": DESC, "tags": TAGS, "pinned": PINNED,
                  "hashtags": ["#KIA타이거즈", "#삼성라이온즈", "#플레이오프", "#김도영", "#카스트로", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {c["from"] - 1: 0.35 for c in CH if c["from"] > 0}   # 10/27: 장이 시작하기 바로 앞 줄(= 앞 장·오프닝의 마지막 줄)에서만 짧게 — 경기 뒤 줄이 늘어도 자동. 훅·문장 중간 쉼 없음(사용자 10/26)
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = min(0.65, HOLD[i])
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-27_롱폼.json')
    todo = [i for i, x in enumerate(LINES) if 'TODO' in x[0] or x[2] == 'TODO']
    if todo and not os.environ.get('PREVIEW'): sys.exit(f'경기 뒤 채울 줄이 남음: {todo} — 미리보기는 PREVIEW=1')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    for m in MERGE_LOG: print('묶음', m)
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
