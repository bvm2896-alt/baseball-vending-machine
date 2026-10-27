# -*- coding: utf-8 -*-
"""10/26 롱폼㉛ 「플레이오프 1차전 리뷰 · KIA 5-1 삼성 · 2차전 예상」 콘티 v2 (가로 16:9 · 집 PC template_long.html 10/25판).
대사 = tools/text_1026_long31.py. 근거 = 프로젝트 claude/1026-롱폼31-PO1차전리뷰-근거모음-경기뒤.md(기사 본문 2곳 이상).
화면: 득점 장면은 다이아몬드(diamond)·홈런 카메라(hrcam), 한 사람 구간은 한 사진 묶음(chain), 기록은 칸(stats)·줄(steps).
사진: 사진 은행(카드/P17·P18·P20·P22·P31·FA9·FA10, 경기/구자욱_세리머니) — 이날 경기 사진은 없음(집 PC 연결 뒤 크롬으로 받으면 교체).
사진 없는 선수(정해영·이의리·조상우·곽도규·박승규·김영웅·강민호·이재현·김성윤)는 다이아몬드·팀 카드로만 — 얼굴 칸을 비우지 않는다.
썸네일 = 썸네일러가 미리 만듦(사용자 10/26 21:50) → thumb 없음, thumbFile 은 PC 넣을 때 사용자 파일 이름으로."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('\ndef sub_of')].replace("'text_1015_long15.py'", "'text_1026_long31.py'")
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
    for d in ('이십오', '십이', '이십칠', '이십구', '삼십', '이십'):
        n = re.sub('(?<![가-힣])' + d + r' 일(?=[ 이과,은에]|$)', d + '일', n)
    n = re.sub(r'(?<![가-힣])((?:[이삼사오육칠팔구]?십)?[일이삼사오육칠팔구]) 위', r'\1위', n)
    n = n.replace('일월요일', '일 월요일')
    n = re.sub(r'(?<![가-힣])([일이삼사오육칠팔구])회말', r'\1회 말', n)  # 10/27 사용자: 오회말→'오휘말'로 들림
    n = n.replace('볼넷', '볼 넷')   # 10/27 사용자: '뽈넷'으로 읽혀서 띄어 씀
    return n
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / ')).replace('4와 3분의 2이닝', '4⅔이닝').replace('4와 3분의 1이닝', '4⅓이닝').replace('1과 3분의 1이닝', '1⅓이닝').replace('3분의 1이닝', '⅓이닝')

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
QS = "10월 26일 · 경기 뒤 · 요약"
def ss(*a): return dict(zip(['at'], a))
# ── 오프닝 ──
K['o0'] = S(0, "matchup", left="KIA", right="삼성", score="5 : 1", tag="플레이오프 1차전")
K['o1'] = S(0, "matchup", left="KIA", right="삼성", score="5 : 1", tag="플레이오프 1차전")
K['o2'] = S(0, "bars", title="5전 3선승제 플레이오프 · 1차전 이긴 팀", items=[dict(label="한국시리즈 진출", value=27, unit="번", at=3.2, hi=True), dict(label="탈락", value=8, unit="번", at=4.3)],
            max=35, text="35번 중 27번", textAt=3.0, size=60)
K['o3'] = tm("KIA", "KIA 타이거즈", "플레이오프 1차전 승리", [], [st("한국시리즈 진출 확률", "77.1%", 0.1, hi=True)])
K['o4'] = tm("KIA", "플레이오프 1차전", "10월 26일 · 대구", [], [st("플레이오프 역사상", "처음 나온 장면", 1.2, hi=True)])
K['o5'] = pv(NAIL, "네일", "KIA 선발", [], [st("5회말", "헤드샷 퇴장", 1.0, hi=True)])
K['o6'] = toc(-1, itemSeg=[0.15, 0.6, 1.05, 1.6, 2.0, 3.1])
# ── 0장 · 경기 전 상황 ──
K['p0'] = toc(0)
K['p1'] = S(0, "tline", title="플레이오프 1차전 · 대구", items=[dict(d="10월 25일", t="비로 취소", c="bad", at=0.3), dict(d="10월 26일 월요일", t="1차전 열림", c="good", big=True, at=1.6)])
K['p2'] = S(0, "duel", title="플레이오프 1차전 선발", left=dict(img=NAIL, name="네일", team="KIA", role="KIA 선발", at=0.6), right=dict(img=FED, name="페덱", team="삼성", role="삼성 선발", at=2.0), vsAt=1.3)
FOL = dict(img=NAIL2, name="네일", team="KIA", role="KIA 선발"); FOR = dict(img=FED2, name="페덱", team="삼성", role="삼성 선발")
FROWS = [dict(k="정규시즌 승패", l="13승 7패", r="7승 3패"), dict(k="평균자책점", l="3.49", r="2.95", lv=3.49, rv=2.95, low=True),
         dict(k="눈여겨볼 기록", l="준PO 1차전 · LG전\n7이닝 1실점 승", r="올해 KIA전 2경기\n2패 · 5.25")]   # 10/27 사용자: 한쪽만 있던 두 줄을 한 줄로
def fo2(ats, rAt=None): return S(0, "faceoff", title="1차전 선발 비교", left=FOL, right=FOR, chain="fo1", rows=[dict(x, at=a, **({"rAt": rAt} if i == 2 and rAt is not None else {})) if a is not None else dict(x, at=50, hide=True) for i, (x, a) in enumerate(zip(FROWS, ats))])
K['p3'] = fo2([1.0, None, None])
K['p4'] = fo2([-1, 1.0, None])
K['p5'] = fo2([-1, -1, 1.0], rAt=50)
K['p6'] = fo2([-1, -1, -1], rAt=0.5)
KJ_ = [st("플레이오프 엔트리", "제외", 1.0, hi=True), st("2026 정규시즌", "35세이브", 2.0), st("부상", "오른쪽 전거근", 50), st("회복", "2주쯤 · 플레이오프 못 뜀", 50)]
K['p7'] = pv(KJY, "김재윤", "삼성 마무리", [], KJ_, team="삼성", chain="kj")
K['p8'] = pv(KJY, "김재윤", "삼성 마무리", [], hide(KJ_[:2]) + [dict(KJ_[2], at=0.3), dict(KJ_[3], at=1.0)], team="삼성", chain="kj")
K['p9'] = pv(GJU, "구자욱", "삼성 외야수", [], [st("2026", "타격왕", 0.2), st("플레이오프 엔트리", "복귀", 1.0, hi=True)], team="삼성")
K['p10'] = S(0, "tline", title="KIA · 1차전 전 일정", items=[dict(d="10월 20일", t="준PO 3연승", at=0.4), dict(d="21~25일", t="닷새 휴식", c="good", big=True, at=1.0), dict(d="10월 26일", t="PO 1차전", at=1.1)])
K['p11'] = S(0, "tline", title="삼성 · 1차전 전 일정", items=[dict(d="10월 12일", t="정규시즌 끝", at=1.0), dict(d="2주", t="공식 경기 없음", c="bad", big=True, at=2.0), dict(d="10월 26일", t="PO 1차전", at=2.0)])
K['p12'] = tm("삼성", "대구 삼성라이온즈파크", "플레이오프 1차전", [], [st("관중", "2만 3550석 매진", 0.5, hi=True), st("포스트시즌", "42경기 연속 매진", 1.0)])
# ── 1장 · 1차전 흐름 ──
K['g0'] = toc(1)
NA_, JHY, KMH = C + "P18_나성범_적시타", C + "R13_정해영_마운드", "상황별/강민호_3점포"
B1 = dict(inn="1회초", score=[0, 0], outs=2, bases=N3, away="KIA", home="삼성")
R1 = [dict(name="김도영", img=KDY, team="KIA", res="볼넷", kind="on", bases=["김도영", None, None], outs=2, score=[0, 0]),
      dict(name="김도영", img=KDY2, team="KIA", res="2루 도루", kind="on", bases=[None, "김도영", None], outs=2, score=[0, 0]),
      dict(name="카스트로", img=CAS, team="KIA", res="적시타", kind="run", bases=["카스트로", None, None], outs=2, score=[1, 0], rbi="+1"),
      dict(name="카스트로", img=CAS2, team="KIA", res="송구 실책 · 3루", kind="on", bases=[None, None, "카스트로"], outs=2, score=[1, 0]),
      dict(name="나성범", img=NA_, team="KIA", res="2루타", kind="run", bases=[None, "나성범", None], outs=2, score=[2, 0], rbi="+1")]
def r1(ats): return S(0, "rally", bug=B1, plays=[dict(x, at=a) for x, a in zip(R1, ats)], chain="r1")
K['g1'] = r1([1.0, 50, 50, 50, 50])
K['g2'] = r1([-1, 1.0, 50, 50, 50])
K['g3'] = r1([-1, -1, 1.2, 50, 50])
K['g4'] = r1([-1, -1, -1, 1.4, 50])
K['g5'] = r1([-1, -1, -1, -1, 1.4])
K['g6'] = S(0, "rally", bug=dict(inn="3회초", score=[2, 0], outs=2, bases=N3, away="KIA", home="삼성"),
            plays=[dict(name="김도영", img=KDY3, focus="28% 20%", team="KIA", res="좌전 안타", kind="on", bases=["김도영", None, None], outs=2, score=[2, 0], at=1.0)])
K['g7'] = S(0, "hrcam", img=CAS, name="카스트로", team="KIA", bug=dict(inn="3회초", score=[2, 0], outs=2, bases=["김도영", None, None], away="KIA", home="삼성"), launchAt=0.6, burst="투런 홈런", _cx=0, chain="hr7", runners=["김도영", "카스트로"], scoreTo=[4, 0])
K['g8'] = dict(K['g7'], launchAt=0.6)   # 앞 줄(g7)의 홈런을 이 줄까지 이어서 — launchLine 은 아래에서
K['g9'] = S(0, "hrcam", img=HJS, name="한준수", team="KIA", bug=dict(inn="4회초", score=[4, 0], outs=0, bases=N3, away="KIA", home="삼성"), launchAt=1.0, dist="120", burst="솔로 홈런", _cx=0, chain="hr9", runners=["한준수"], scoreTo=[5, 0])
H2 = [st("비거리", "120m", 0.1), st("점수", "5대0", 1.0, hi=True)]
K['g10'] = dict(K['g9'])
K['g11'] = pv(HJS2, "한준수", "KIA 지명타자 · 4회초", [vsteps([stp("10월 20일", "준플레이오프 3차전 · 홈런", 0.3), stp("10월 26일", "플레이오프 1차전 · 홈런", 0.8, c="good")])], hide(H2), chain="hj")
N1 = [st("상대", "삼성 타선", 1.0), st("4회까지 피안타", "1개", 50), st("4회까지 실점", "0", 50, hi=True)]
K['g12'] = pv(NAIL, "네일", "KIA 선발", [], N1, chain="n1")
K['g13'] = pv(NAIL, "네일", "KIA 선발", [], hide(N1[:1]) + [dict(N1[1], at=0.5), dict(N1[2], at=1.0)], chain="n1")
K['g14'] = S(0, "duel", title="5회초 1아웃 · 김도영 vs 페덱", left=dict(img=KDY, name="김도영", team="KIA", role="KIA 3루수", at=0.6), right=dict(img=FED, name="페덱", team="삼성", role="삼성 선발", at=1.2), vsAt=0.9)
K13 = [st("투구 수", "13구", 0.3, hi=True), st("결과", "우익수 플라이", 50)]
K['g15'] = pv(KDY, "김도영", "5회초 1아웃 · 페덱과 승부", [vstamp("플레이오프 한 타자 최다 투구 타이", 50, "gold", size=46)], K13, chain="k13")
K['g16'] = pv(KDY, "김도영", "5회초 1아웃 · 페덱과 승부", [vstamp("플레이오프 한 타자 최다 투구 타이", 1.0, "gold", size=46)], hide(K13[:1]) + [dict(K13[1], at=0.2)], chain="k13")
F1 = [st("이닝", "4⅔이닝", 50), st("볼넷 · 피홈런", "2개 · 2개", 50), st("실점", "5점", 50, hi=True), st("94구 중 김도영에게", "24구", 50)]
K['g17'] = pv(FED, "페덱", "삼성 선발", [vstamp("5회초 2아웃 강판", 1.0, "bad", size=50)], F1, team="삼성", chain="fd")
K['g18'] = pv(FED, "페덱", "삼성 선발", [vstamp("5회초 2아웃 강판", -1, "bad", size=50)], [dict(F1[0], at=0.2), dict(F1[1], at=1.0), dict(F1[2], at=2.0), F1[3]], team="삼성", chain="fd")
K['g19'] = pv(FED, "페덱", "삼성 선발", [vstamp("5회초 2아웃 강판", -1, "bad", size=50)], hide(F1[:3]) + [dict(F1[3], at=1.0)], team="삼성", chain="fd")
NH = [st("5회말", "5대0 리드", 0.4), st("1아웃 뒤", "박승규 타석", 50), st("볼카운트", "풀카운트", 50), st("6구째", "146km 투심", 50, hi=True)]
def nh(ats, stamp=None): return pv(NAIL, "네일", "KIA 선발 · 5회말", [stamp] if stamp else [], [dict(x, at=a) for x, a in zip(NH, ats)], chain="nh")
K['g20'] = nh([0.4, 50, 50, 50])
K['g21'] = nh([-1, 1.0, 1.5, 50])
K['g22'] = nh([-1, -1, -1, 0.2], vstamp("헬멧에 맞음", 1.0, "bad", size=56))
K['g23'] = nh([-1, -1, -1, -1], vstamp("헤드샷 퇴장", 0.6, "bad", size=60))
PSG = "상황별/박승규_타격_0830_삼성제공"
K['g24'] = pv(PSG, "박승규", "삼성 외야수 · 5회말", [], [st("헤드샷 뒤", "큰 부상 없이 1루로", 1.0, hi=True)], team="삼성")
K['g24b'] = pv(NAIL, "네일", "KIA 선발 · 5회말", [], [st("퇴장하며", "박승규에게 미안함 표시", 1.0, hi=True)])
B5 = dict(inn="5회말", score=[5, 0], outs=1, bases=["박승규", None, None], away="KIA", home="삼성")
R5 = [dict(name="정해영", img=JHY, team="KIA", res="급히 등판", kind="on", bases=["박승규", None, None], outs=1, score=[5, 0]),
      dict(name="강민호", img=KMH, team="삼성", res="중견수 뜬공", kind="out", bases=["박승규", None, None], outs=2, score=[5, 0]),
      dict(name="박승규", img=PSG, team="삼성", res="2루 도루", kind="on", bases=[None, "박승규", None], outs=2, score=[5, 0]),
      dict(name="김영웅", img="상황별/김영웅_적시타_1026_삼성제공", focus="50% 12%", team="삼성", res="적시타", kind="run", bases=["김영웅", None, None], outs=2, score=[5, 1], rbi="+1")]
def r5(ats): return S(0, "rally", bug=B5, plays=[dict(x, at=a) for x, a in zip(R5, ats)], chain="r5")
K['g25'] = r5([1.0, 50, 50, 50])
K['g26'] = r5([-1, 1.0, 50, 50])
K['g27'] = r5([-1, -1, 0.3, 1.2])
B5b = dict(inn="5회말", score=[5, 1], outs=2, bases=["김영웅", None, None], away="KIA", home="삼성")
R5b = [dict(name="네일", img=NAIL, team="KIA", res="1실점 기록", kind="out", bases=["김영웅", None, None], outs=2, score=[5, 1]),
       dict(name="이재현", img="상황별/이재현_상체", team="삼성", res="11구 끝 삼진", kind="out", bases=["김영웅", None, None], outs=3, score=[5, 1]),
       dict(name="정해영", img=JHY, team="KIA", res="이닝 끝", kind="on", bases=["김영웅", None, None], outs=3, score=[5, 1])]
def r5b(ats): return S(0, "rally", bug=B5b, plays=[dict(x, at=a) for x, a in zip(R5b, ats)], chain="r5b")
K['g28'] = r5b([2.0, 50, 50])
K['g29'] = r5b([-1, 1.4, 50])
K['g29b'] = r5b([-1, -1, 1.2])
RP = [("네일", 1), ("정해영", 2), ("이의리", 4), ("조상우", 4), ("곽도규", 1), ("전상현", 3)]
def bpv(ats): return S(0, "relay", title="KIA 마운드 · 5회말~9회", team="KIA", inn=[5, 6, 7, 8, 9], cw=110, gap=30, colors=["#9AA3B2", "#C30452", "#E8A100", "#1F9D55", "#2563EB", "#7C3AED"],
                         pitchers=[dict(name=n, outs=o, at=a) for (n, o), a in zip(RP, ats)], chain="bp")
K['g30'] = bpv([-1, 0.2, 50, 50, 50, 50])
K['g31'] = bpv([-1, -1, 0.3, 50, 50, 50])
K['g33'] = bpv([-1, -1, -1, 0.2, 1.0, 50])
K['g34'] = bpv([-1, -1, -1, -1, -1, 0.3])
K['g35'] = tm("삼성", "삼성 불펜", "5회초 2아웃부터", [], [st("페덱 강판 뒤", "무실점", 1.6, hi=True)])
K['g37'] = S(0, "scoreboard", title="플레이오프 1차전", rows=[dict(r) for r in BOX], label="삼성 안타 2개", labelAt=1.0, chain="box")
K['g38'] = S(0, "scoreboard", title="플레이오프 1차전", rows=[dict(r) for r in BOX], hi=[6, 7, 8, 9], label="KIA 5대1 승리", labelAt=2.0, chain="box")
# ── 2장 · 승부를 가른 이유 ──
K['r0'] = toc(2)
KA = [st("정규시즌", "홈런왕 · 45개", 50), st("준플레이오프", "MVP · 홈런 3개", 50), st("1차전", "홈런 없음", 50, hi=True)]
def ka(ats, sa): return pv(KDY2, "김도영", "이유 하나 · KIA 3루수", [vstamp("눈과 발", sa, "gold", size=56)], [dict(x, at=a) for x, a in zip(KA, ats)], chain="kd0")
K['r1'] = ka([50, 50, 50], 1.0)
K['r2'] = ka([1.0, 3.0, 50], -1)
K['r3'] = ka([-1, -1, 1.0], -1)
# 10/27 사용자: 8회 2루타(홈런인 줄 알고 안 뜀) · 양현종에게 한 소리(중계, 사용자 확인) — 물세례 사진은 사용자 제공
KDW = "상황별/김도영_물세례_1026_사용자제공"
K['r3a'] = S(0, "hrcam", img=KDY, name="김도영", team="KIA", bug=dict(inn="8회초", score=[5, 1], outs=0, bases=N3, away="KIA", home="삼성"), launchAt=3.0, fl=3.4, wall=True, burst="2루타", _cx=0, chain="hr8", runners=[])
K['r3b'] = dict(K['r3a'])   # 앞 줄에서 친 타구를 이 줄까지 — 담장 맞고 2루타
K['r3c'] = pv(KDW, "김도영", "8회 2루타 뒤", [], [st("중계 화면", "양현종에게 한 소리", 1.0, hi=True)], focus="74% 22%")
K['r3d'] = pv(KDY2, "김도영", "경기 뒤 인터뷰", [vq("10월 26일 · 경기 뒤", "넘어갈 줄 알았는데 제일 깊은 곳이라 안 넘어갔다", 1.0)], [])
# 10/27 사용자("이런 기록들도 텍스트 말고 인포그래픽과 모션그래픽으로"): 김도영 타석 카드 + 숫자 띠
KTL = [dict(k="안타", v=2, at=50), dict(k="볼넷", v=1, at=50), dict(k="도루", v=1, at=50), dict(k="득점", v=2, at=50, hi=True)]
KPL = [dict(name="1회", img=KDY, team="KIA", res="볼넷", kind="on"),
       dict(name="1회", img=C + "P17_김도영_하이파이브", team="KIA", res="도루 · 홈인", kind="run"),
       dict(name="3회", img=C + "P22_김도영_포효", team="KIA", res="안타 · 홈인", kind="run"),
       dict(name="5회", img="상황별/김도영_42호_타구_잠실", team="KIA", res="13구 뜬공", kind="out"),
       dict(name="8회", img="경기/김도영_43호_타격_KIA제공", team="KIA", res="2루타", kind="on")]
def kd(tat, pat): return S(0, "rally", title="김도영 · 1차전", tally=[dict(x, at=a) for x, a in zip(KTL, tat)], plays=[dict(x, at=a) for x, a in zip(KPL, pat)], chain="kd")
K['r4'] = kd([1.0, 1.4, 2.0, 2.4], [50, 50, 50, 50, 50])
K['r5'] = kd([-1] * 4, [0.0, 1.0, 50, 50, 50])
K['r6'] = kd([-1] * 4, [-1, -1, 0.2, 50, 50])
K['r7'] = kd([-1] * 4, [-1, -1, -1, 0.2, 50])
K['r7b'] = kd([-1] * 4, [-1, -1, -1, -1, 0.2])
CTL = [dict(k="안타", v=3, at=50), dict(k="타점", v=3, at=50, hi=True), dict(k="득점", v=2, at=50), dict(k="홈런", v=1, at=50)]
CPL = [dict(name="1회", img="상황별/카스트로_홈런", team="KIA", res="적시타 · 1타점", kind="on"),
       dict(name="1회", img=CAS2, team="KIA", res="홈인", kind="run"),
       dict(name="3회", img=CAS, team="KIA", res="투런 홈런", kind="run")]
def cs(tat, pat): return S(0, "rally", title="카스트로 · 1차전", tally=[dict(x, at=a) for x, a in zip(CTL, tat)], plays=[dict(x, at=a) for x, a in zip(CPL, pat)], chain="cs")
K['r8'] = cs([50] * 4, [50, 50, 50])
K['r9'] = cs([0.1, 0.4, 0.6, 1.2], [50, 50, 50])
K['r10'] = cs([-1] * 4, [0.0, 0.5, 1.0])
K['r10b'] = tm("KIA", "KIA 홈런 두 방", "플레이오프 1차전", [vsteps([stp("3회", "카스트로 투런 · 2점", 0.1), stp("4회", "한준수 솔로 · 1점", 1.0)])], [st("홈런으로만", "3점", 2.0, hi=True)])
B3 = [st("이어 던진 투수", "5명", 50), st("이닝", "4⅔이닝", 50), st("김영웅 적시타 뒤", "무실점", 50, hi=True)]
RS = [stp("2026 시즌", "뒷문이 고민", 50, c="bad"), stp("개막", "마무리 정해영", 50), stp("시즌 중", "마무리 여러 번 바뀜", 50), stp("시즌 막판", "곽도규 · 전상현", 50)]
def b3(sat, rat): return tm("KIA", "KIA 불펜", "이유 셋", [vsteps([dict(x, at=a) for x, a in zip(RS, rat)])], [dict(x, at=a) for x, a in zip(B3, sat)], chain="b3")
K['r11'] = b3([50, 50, 50], [50, 50, 50, 50])
K['r12'] = b3([0.6, 50, 50], [50, 50, 50, 50])
K['r13'] = b3([-1, 50, 50], [1.0, 50, 50, 50])
K['r14'] = b3([-1, 50, 50], [-1, 0.3, 1.0, 2.3])
K['r15'] = b3([-1, 1.0, 2.0], [-1, -1, -1, -1])
SST = [stp("10월 12일", "정규시즌 마지막 경기", 50), stp("2주", "공식 경기 없음", 50, c="bad")]
def sb(ats, sat): return tm("삼성", "삼성 타선", "플레이오프 1차전", [vsteps([dict(x, at=a) for x, a in zip(SST, ats)])], [st("1차전 팀 안타", "2개", sat, hi=True)], chain="sb")
# 10/27 사용자("수비에서 박재현도 한몫했는데 언급 한번"): 7회말 2사 1루 강민호 타구 → 좌익수 박재현 호수비
K['r15b'] = S(0, "rally", bug=dict(inn="7회말", score=[5, 1], outs=2, bases=["디아즈", None, None], away="KIA", home="삼성"),
              plays=[dict(name="강민호", img=KMH, team="삼성", res="날카로운 타구", kind="on", bases=["디아즈", None, None], outs=2, score=[5, 1], at=2.0),
                     dict(name="박재현", img="상황별/박재현_호수비_1026_사용자제공", focus="62% 10%", team="KIA", res="호수비 · 이닝 끝", kind="def", bases=N3, outs=3, score=[5, 1], at=3.0)])
K['r16'] = sb([50, 50], 50)
K['r17'] = sb([1.0, 1.1], 0.3)
K['r18'] = pv(FED, "페덱", "삼성 선발", [], [st("정규시즌 KIA전", "2경기 2패", 1.0), st("플레이오프 1차전", "패전", 2.0, hi=True)], team="삼성")
# ── 3장 · 네일의 헤드샷 퇴장 ──
K['r18b'] = pv(PJM, "박진만", "삼성 감독", [vq(QS, "페덱 초반 공은 좋았다", 1.0), vq(QS, "KIA 중심 타선이 잘 대처했다", 2.0)], [], team="삼성", chain="pj1")
K['r18c'] = pv(PJM, "박진만", "삼성 감독", [vq(QS, "페덱 초반 공은 좋았다", -1), vq(QS, "KIA 중심 타선이 잘 대처했다", -1), vq(QS, "2아웃 뒤 실점이 아쉽다", 0.3)], [], team="삼성", chain="pj1")
K['h0'] = toc(3)
K['h1'] = pv(NAIL, "네일", "헤드샷 퇴장 규정", [vsteps([stp("규정", "직구가 머리에 맞으면", 1.0), stp("고의 여부", "상관없이", 2.0), stp("결과", "바로 퇴장", 3.0, c="bad")])])
def tl(title, items, **k): return S(0, "steps", title=title, items=[dict(date=d, text=x, at=a_, **({"hi": True} if h else {}), **({"hide": True} if a_ is None else {})) for d, x, a_, h in items], chain=k.pop("chain", None), **k)
K['h2'] = tl("KBO 헤드샷 퇴장 규정", [("2003~2004년", "모든 공\n머리에 맞히면 퇴장", 0.1, False), ("2014년부터", "직구만\n머리에 맞히면 퇴장", None, True)], chain="hr")
K['h3'] = tl("KBO 헤드샷 퇴장 규정", [("2003~2004년", "모든 공\n머리에 맞히면 퇴장", -1, False), ("2014년부터", "직구만\n머리에 맞히면 퇴장", 0.1, True)], chain="hr")
K['h4'] = pv(NAIL, "네일", "KIA 선발 · 5회말", [], [st("네일의 공", "146km 투심", 0.2), st("투심", "직구 계열", 1.0, hi=True)])
K['h5'] = pv(NAIL, "네일", "포스트시즌 헤드샷 퇴장", [], [st("포스트시즌", "세 번째", 1.0), st("플레이오프에선", "처음", 2.0, hi=True)])
K['h6'] = tl("포스트시즌 헤드샷 퇴장", [("2003년", "한국시리즈 4차전\nSK 김정수", 1.0, False), ("2014년", "준플레이오프 1차전\nLG 류제국", 3.0, False), ("2026년", "플레이오프 1차전\nKIA 네일", 0.0, True)])
NL = [st("투구 수", "57개", 1.0), st("이닝", "4⅓이닝", 2.0), st("피안타", "1개", 3.0, hi=True)]
K['h7'] = pv(NAIL, "네일", "KIA 선발 · 1차전", [], NL, chain="nl")
NB = [st("탈삼진", "3개", 0.3), st("볼넷", "0개", 1.0, hi=True)]
K['h7b'] = pv(NAIL, "네일", "KIA 선발 · 1차전", [], NB, chain="nl")
K['h8'] = pv(NAIL, "네일", "KIA 선발 · 1차전", [vstamp("공 하나에 퇴장", 1.0, "bad", size=56)], hide(NB), chain="nl")
K['h9'] = tm("KIA", "KIA 타이거즈", "플레이오프 1차전 · 5대1 승리", [], [st("불펜", "끝까지 버팀", 0.5, hi=True), st("네일 퇴장 변수", "이겨 냄", 50)], chain="h9")
K['h9b'] = tm("KIA", "KIA 타이거즈", "플레이오프 1차전 · 5대1 승리", [], [st("불펜", "끝까지 버팀", -1, hi=True), st("네일 퇴장 변수", "이겨 냄", 1.0)], chain="h9")
# ── 4장 · 2차전 예상 ──
K['n0'] = toc(4)
K['n1'] = S(0, "series5", tc={"삼성": SSB}, title="플레이오프 · KIA 1승", games=PO1[:2] + [dict(g, appear=50) for g in PO1[2:]], pills=[dict(label="2차전 · 27일 오후 6시 30분 · 대구", at=0.5, c="#12161F"), dict(label="5차전까지 가면 · 11월 1일 대구", at=50, c="#12161F")], chain="s5")
K['n2'] = S(0, "series5", tc={"삼성": SSB}, title="플레이오프 · KIA 1승", games=PO1[:2] + [dict(g, appear=a_) for g, a_ in zip(PO1[2:], [0.1, 0.4, 1.5])], pills=[dict(label="2차전 · 27일 오후 6시 30분 · 대구", at=-1, c="#12161F"), dict(label="5차전까지 가면 · 11월 1일 대구", at=1.6, c="#12161F")], chain="s5")
GS = dict(teams={"K": "KIA"}, games=[["5대1", "K"], ["6대3", "K"], ["13대1", "K"], ["5대1", "K"]], sw=260, chain="gs", title="KIA 2026 가을야구")
K['n5'] = S(0, "gamestrip", at=0.1, step=.25, groups=[{"from": 0, "to": 2, "label": "준플레이오프 · LG전 3연승", "team": "KIA", "at": 0.6}, {"from": 3, "to": 3, "label": "PO 1차전 · 4연승", "team": "KIA", "at": 2.0}], **GS)
K['n6'] = S(0, "duel", title="플레이오프 2차전 선발", left=dict(img=OLLER, name="올러", team="KIA", role="KIA 선발", at=0.5), right=dict(img=HUR, name="후라도", team="삼성", role="삼성 선발", at=2.0), vsAt=1.3)
K['n7'] = pv(OLLER, "올러", "KIA 2차전 선발", [], [st("2026 정규시즌", "11승", 0.4), st("평균자책점 2위", "3.13", 1.0, hi=True)])
OL2 = [st("삼진", "180개", 0.3), st("준플레이오프 2차전", "6이닝 2실점", 2.0), st("올해 삼성전 · 3경기", "평균자책점 5.79", 50, hi=True)]
K['n8'] = pv(OLLER2, "올러", "KIA 2차전 선발", [], OL2, chain="ol2")
K['n8b'] = pv(OLLER2, "올러", "KIA 2차전 선발", [], hide(OL2[:2]) + [dict(OL2[2], at=1.0)], chain="ol2")
K['n11'] = pv(HUR2, "후라도", "삼성 2차전 선발", [], [st("올해 KIA전 · 1경기", "7이닝 3실점", 0.6, hi=True)])
V1 = [st("1차전 등판", "5명", 50), st("가장 길게 던진 투수", "1⅓이닝", 50, hi=True), st("선발이 일찍 내려가면", "불펜 부담", 50)]
K['n12'] = tm("KIA", "KIA 불펜", "변수 하나", [], V1, chain="v1")
K['n13'] = tm("KIA", "KIA 불펜", "변수 하나", [], [dict(V1[0], at=0.5), dict(V1[1], at=2.0), V1[2]], chain="v1")
K['n13b'] = tm("KIA", "KIA 불펜", "변수 하나", [], hide(V1[:2]) + [dict(V1[2], at=0.3)], chain="v1")
K['n14'] = tm("삼성", "삼성 타선", "변수 둘", [], [st("1차전 팀 안타", "2개", -1), st("2차전", "언제 깨어날까", 0.6, hi=True)])
def ppl(items, **k): return S(0, "people", ph=420, title="삼성 중심 타자", items=items, chain="pp", **k)
K['n15'] = pv(GJU, "구자욱", "삼성 외야수 · 2026 타격왕", [], [st("타율 1위", "0.371", 0.3, hi=True), st("출루율 1위", "0.458", 1.0, hi=True)], team="삼성")
K['n16'] = ppl([dict(img=DIAZ, name="디아즈", team="삼성", note="129타점 · 2위", at=0.0, noteAt=0.3), dict(img=CHOI, name="최형우", team="삼성", note="106타점", at=1.0, noteAt=1.3)])
K['n17'] = ppl([dict(img=DIAZ, name="디아즈", team="삼성", note="KIA전 타율 0.214", at=-1, noteAt=1.0), dict(img=CHOI, name="최형우", team="삼성", note="KIA전 타율 0.190", at=-1, noteAt=2.0)])
K['n18'] = tm("삼성", "삼성 라이온즈", "공식 경기", [vsteps([stp("정규시즌 마지막", "4연패", 1.0), stp("플레이오프 1차전", "패배", 2.0), stp("공식 경기", "5연패", 3.0, c="bad")])])
K3 = [st("올해 삼성전 · 16경기", "홈런 9개", 50, hi=True), st("타점", "20", 50), st("1차전", "홈런 없음", 50)]
def k3(ats): return pv(KDY3, "김도영", "변수 셋 · KIA 3루수", [], [dict(x, at=a) for x, a in zip(K3, ats)], chain="k3", focus="28% 20%")
K['n19'] = k3([50, 50, 50])
K['n20'] = k3([1.0, 1.4, 50])
K['n21'] = k3([-1, -1, 0.4])
IS = [st("경기 전 삼성 계획", "위기 땐 이승민", 1.0), st("올해 KIA전 · 8경기", "평균자책점 1.17", 50, hi=True)]
K['n22'] = pv(ISM, "이승민", "삼성 좌완 불펜", [], IS, team="삼성", chain="is")
K['n23'] = pv(ISM, "이승민", "삼성 좌완 불펜", [], hide(IS[:1]) + [dict(IS[1], at=1.0)], team="삼성", chain="is")
K['n17b'] = pv(PJM, "박진만", "삼성 감독", [vq(QS, "주자가 없어 최형우 쓸 기회 없었다", 1.0)], [], team="삼성")
K['n21b'] = tm("삼성", "삼성 뒷문", "변수 넷", [], [st("마무리 김재윤", "부상 이탈", 1.0, hi=True)])
K['n23b'] = pv(PJM, "박진만", "삼성 감독", [vq(QS, "원태인은 후반 비밀 카드였다", 1.0)], [], team="삼성")
K['n23c'] = pv(WTI, "원태인", "삼성 투수", [], [st("2차전", "불펜 대기", 0.5), st("2차전에 안 나오면", "3차전 선발", 1.0, hi=True)], team="삼성")
K['n23d'] = pv(PJM, "박진만", "삼성 감독", [vq(QS, "타선 전체가 처져 있었다", 1.0), vq(QS, "2차전엔 자세가 달라야", 3.0)], [st("2차전", "타순 변화 예고", 2.0)], team="삼성")
K['n24'] = S(0, "wdl", title="KIA의 삼성전 성적", rows=[dict(team="KIA", w=9, l=7, at=1.0, tag="2026 정규시즌", tagAt=1.2), dict(team="KIA", w=4, l=1, at=3.0, tag="2024 한국시리즈", tagAt=3.2)])
P2 = [st("2차전", "삼성 반격?", 1.0, hi=True), st("삼성", "1차전 뒤 실전 감각", 50), st("선발 후라도", "안방 대구", 50)]
K['n25'] = tm("삼성", "2차전 예상", "10월 27일 · 대구", [], P2, chain="p2")
K['n26'] = tm("삼성", "2차전 예상", "10월 27일 · 대구", [], [dict(P2[0], at=-1), dict(P2[1], at=0.5), dict(P2[2], at=1.0)], chain="p2")
K['n26b'] = tm("KIA", "2차전 예상", "KIA 쪽에서 보면", [], [st("올러", "6회까지 버티면?", 1.0), st("그다음", "불펜 싸움", 2.0, hi=True)])
G2 = lambda win, at: [dict(PO1[0]), dict(PO1[1], win=win, maybe=True, at=at), dict(PO1[2]), dict(PO1[3]), dict(PO1[4])]
K['n27'] = S(0, "series5", tc={"삼성": SSB}, title="2차전 결과에 따라", games=G2("KIA", 0.4), pills=[dict(label="KIA · 광주에서 끝낼 기회", at=1.6, c=KIAC)], chain="s5b")
K['n28'] = S(0, "series5", tc={"삼성": SSB}, title="2차전 결과에 따라", games=G2("삼성", 0.3), pills=[dict(label="1승 1패로 광주", at=1.0, c=SSB)], chain="s5b")
# ── 5장 · 숫자로 본 1차전 ──
K['m0'] = toc(5)
# 10/27 사용자("숫자로 본 1차전은 영양가 없음 — 2차전 양 팀 키플레이어 예상을 넣는 게 나을 것"): 6장 = 2차전 키플레이어
PJH = C + "P15_박재현"
KPL_ = dict(img=PJH, name="박재현", team="KIA", role="KIA 2번 · 좌익수"); KPR_ = dict(img=GJU, name="구자욱", team="삼성", role="삼성 · 2026 타격왕")
KROWS = [dict(k="삼성라이온즈파크 7경기", l="타율 .444 · 3홈런", r=""), dict(k="삼성전 16경기", l="타율 .338 · 13타점", r=""),
         dict(k="2차전 선발 후라도 상대", l="4타수 1안타", r=""), dict(k="2026 정규시즌", l="", r="타율 .371 · 1위"),
         dict(k="2차전 선발 올러 상대", l="", r="7타수 3안타 · 2타점")]
def kp(ats): return S(0, "faceoff", title="2차전 키플레이어", left=KPL_, right=KPR_, chain="kp", rows=[dict(x, at=a) if a is not None else dict(x, at=50, hide=True) for x, a in zip(KROWS, ats)])
K['m1'] = kp([None] * 5)
K['m2'] = kp([1.0, None, None, None, None])
K['m3'] = kp([-1, 1.0, None, None, None])
K['m4'] = kp([-1, -1, None, None, None])
K['m5'] = kp([-1, -1, 0.5, None, None])
K['m6'] = kp([-1, -1, -1, 0.6, None])
K['m7'] = kp([-1, -1, -1, -1, 0.6])
K['m8'] = tm("삼성", "올러 상대 삼성 타자", "2026 정규시즌", [], [st("이재현", "3타수 2안타 · 1홈런", 0.4), st("최형우", "7타수 1안타 · 삼진 5", 2.4, hi=True)])
K['m9'] = pv(NA, "나성범", "KIA 우익수", [], [st("2차전 선발 후라도 상대", "3타수 2안타", 1.0, hi=True)])
ZS = [stp("김도영", "눈과 발", 1.0), stp("카스트로", "3타점", 2.0), stp("불펜", "무실점", 3.0, c="good")]
K['z0'] = tm("KIA", "1차전 정리", "KIA 5대1 승리", [vsteps(ZS)], [st("한국시리즈 진출 확률", "77.1%", 50, hi=True)], chain="z0")
K['z0b'] = tm("KIA", "1차전 정리", "KIA 5대1 승리", [vsteps([dict(x, at=-1) for x in ZS])], [st("한국시리즈 진출 확률", "77.1%", 1.6, hi=True)], chain="z0")
K['z1'] = S(0, "question", text="2차전\n삼성 반격? KIA 2연승?", logos=["삼성", "KIA"], logoSize=230, size=104)
missing = [k for k in KEYS if k not in K]; extra = [k for k in K if k not in KEYS]
assert not missing and not extra, (missing, extra)
SC = [K[k] for k in KEYS]
IDX = {k: i for i, k in enumerate(KEYS)}

CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
SLOW = {IDX[k] for k in ('o2', 'o3', 'g16', 'g23', 'h5', 'n25')}
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
CH = [_ch("경기 전 상황", "경기 전 상황", "p0", "p12"), _ch("1차전 흐름", "1차전 흐름", "g0", "g38"), _ch("승부를 가른 이유", "승부를 가른 이유", "r0", "r18c"),
      _ch("네일 헤드샷 퇴장", "네일의 헤드샷 퇴장", "h0", "h9b"), _ch("2차전 예상", "2차전 예상", "n0", "n28"), _ch("2차전 키플레이어", "2차전 키플레이어", "m0", "z1")]

TAGS = ["플레이오프", "플레이오프 1차전", "KIA 삼성", "기아 삼성", "KIA 타이거즈", "삼성 라이온즈", "김도영", "카스트로", "네일", "네일 헤드샷", "헤드샷 퇴장",
        "한준수", "페덱", "플레이오프 2차전", "올러", "후라도", "박진만", "원태인", "프로야구", "KBO", "야구자판기"]
DESC = ("KIA가 10월 26일 대구에서 열린 플레이오프 1차전에서 삼성을 5대1로 이겼어요. 역대 5전 3선승제 플레이오프에서 1차전 승리 팀이 한국시리즈에 오른 것은 35번 중 27번(77.1%)이에요.\n\n"
        "경기 전 상황: 25일 1차전이 비로 하루 밀려 26일 열림. 선발 KIA 네일(정규시즌 13승 7패·3.49) vs 삼성 페덱(7승 3패·2.95, KIA전 2패·5.25). 삼성 마무리 김재윤 부상으로 엔트리 제외, 타격왕 구자욱 복귀. 2만 3550석 매진(포스트시즌 42경기 연속).\n\n"
        "1차전 흐름: 1회 김도영 볼넷·도루 뒤 카스트로 우전 적시타(우익수 송구 실책으로 카스트로 3루), 나성범 1타점 2루타. 3회 2사 뒤 김도영 안타, 카스트로 투런 홈런(페덱 9구째 커터). "
        "4회 한준수 솔로 홈런(120m, 포스트시즌 두 경기 연속). 5회 김도영-페덱 13구 승부(플레이오프 한 타자 최다 투구 타이), 페덱 4⅔이닝 94구 5실점 강판. "
        "5회말 1사 네일이 박승규에게 146km 투심 헤드샷 퇴장(포스트시즌 세 번째·플레이오프 처음), 김영웅 적시타로 1점(네일 실점). 이후 정해영-이의리-조상우-곽도규-전상현 무실점. 삼성 2안타.\n\n"
        "경기 뒤 박진만 감독(요약): 원태인은 후반 비밀 카드였다, 2차전에 안 나가면 3차전 선발 가능, 타선 전체가 처져 있었다.\n\n"
        "2차전: 10월 27일 오후 6시 30분 대구, KIA 올러 vs 삼성 후라도. 3·4차전 10월 29·30일 광주, 5차전 11월 1일 대구.\n\n"
        "2차전 키플레이어: KIA 박재현(삼성라이온즈파크 7경기 타율 .444·3홈런, 삼성전 .338·13타점, 후라도 상대 4타수 1안타), 삼성 구자욱(타율 .371 타격왕, 올러 상대 7타수 3안타 2타점). 올러 상대 이재현 3타수 2안타 1홈런·최형우 7타수 1안타 5삼진, 후라도 상대 나성범 3타수 2안타.\n\n"
        "여러분은 2차전, 삼성이 반격할 거라고 보시나요? KIA가 2연승을 할 거라고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록 출처: MK스포츠·스포츠경향·서울신문·세계일보·SPOTV뉴스·마이데일리·뉴스1·뉴스엔·스포츠월드·톱스타뉴스·뉴스핌·일간스포츠·한국아이닷컴·뉴시스·재경일보·이데일리(2026/10/26), 일간스포츠·마이데일리·중앙일보(2026/10/27), 머니투데이·MHN·위키트리·대경일보·뉴스Q·더팩트(2026/10), OSEN·스포츠경향·뉴스토마토(2014, 헤드샷 규정·사례), KBO 기록실\n"
        "사진 출처: 구단 제공·연합뉴스·일간스포츠·머니투데이(사진 기사)")
SOURCE = "사실 출처 = 프로젝트 claude/1026-롱폼31-PO1차전리뷰-근거모음-경기뒤.md(기사 본문 2곳 이상)."
PINNED = "2차전, 삼성이 반격할까요? KIA가 2연승을 할까요? 👇 댓글로 남겨 주세요!\n매일 야구 이슈 받아보려면 구독 + 알림 설정 부탁드려요 ⚾"

EP = {"introChapter": "오프닝", "date": "2026-10-26", "gameDate": "2026-10-26", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.15,
      "rev": "1026-long31-v2", "topic": "PO1차전리뷰", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 9000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "플레이오프 1차전 리뷰 KIA 5대1 삼성 | 김도영 13구·카스트로 3타점·네일 헤드샷 퇴장, 2차전은? #KIA #삼성",
                  "description": DESC, "tags": TAGS, "pinned": PINNED,
                  "hashtags": ["#KIA타이거즈", "#삼성라이온즈", "#플레이오프", "#김도영", "#카스트로", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {IDX[k]: 0.35 for k in ("o6", "p12", "g38", "r18c", "h9b", "n28")}   # 장 끝에서만 짧게 — 훅·문장 중간 쉼 없음(사용자 10/26)
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = min(0.65, HOLD[i])
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-26_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    for m in MERGE_LOG: print('묶음', m)
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
