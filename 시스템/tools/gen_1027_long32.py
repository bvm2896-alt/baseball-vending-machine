# -*- coding: utf-8 -*-
"""10/27 롱폼㉜ 「플레이오프 2차전 리뷰 · 3차전 승부예측」 콘티 — 경기 전 준비판(3차전 예상 장). 아래 설명은 롱폼㉛에서 이어 온 틀.
(이전: 10/26 롱폼㉛ 콘티 v2 (가로 16:9 · 집 PC template_long.html 10/25판).
대사 = tools/text_1026_long31.py. 근거 = 프로젝트 claude/1026-롱폼31-PO1차전리뷰-근거모음-경기뒤.md(기사 본문 2곳 이상).
화면: 득점 장면은 다이아몬드(diamond)·홈런 카메라(hrcam), 한 사람 구간은 한 사진 묶음(chain), 기록은 칸(stats)·줄(steps).
사진: 사진 은행(카드/P17·P18·P20·P22·P31·FA9·FA10, 경기/구자욱_세리머니) — 이날 경기 사진은 없음(집 PC 연결 뒤 크롬으로 받으면 교체).
10/27 사진 보강: 이호연·김태군·이의리·하주석·박재현·나성범·한준수 KIA 제공(스포츠경향 게재본, 워터마크 없음), 김성윤·페덱 사용자 제공.
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
    t = t.replace('경기 전 수 싸움,', '경기 전, 수 싸움,').replace('2번에 선', '이 번에 선').replace('경기 전 두 감독의', '경기 전, 두 감독의')   # 10/28 사용자: '경기 전 / 수 싸움' 끊어 읽기
    t = t.replace('42살 10개월 11일', '마흔두 살 십 개월 십일 일').replace('42살', '마흔두 살')
    t = t.replace('광주-기아', '광주 기아').replace('1번 타자와 2번 타자', '일 번 타자와 이 번 타자').replace('2번 지명타자', '이 번 지명타자').replace('2025시즌', '2025 시즌').replace('125m', '백이십오 미터').replace('41살 8개월 13일', '마흔한 살 팔 개월 십삼 일').replace('151km', '백오십일 킬로').replace('16번 중 9번', '열여섯 번 중 아홉 번').replace('56.3%', '오십육 점 삼 퍼센트').replace('108개', '백여덟 개').replace('5전 3선승제', '오 전 삼선승제').replace('오후 6시 반', '오후 여섯 시 반').replace('8번뿐', '여덟 번뿐').replace('26일 월요일', '이십육 일 월요일')
    if t.startswith('2, / '): t = '둘, / ' + t[5:]
    t = t.replace('MVP', '엠브이피').replace('77.1%', '칠십칠 점 일 퍼센트').replace('5.25', '오 점 이오').replace('3.13', '삼 점 일삼').replace('1.17', '일 점 일칠')
    t = t.replace('2아웃', '투 아웃').replace('1아웃', '원 아웃').replace('3·4차전', '삼, 사차전').replace('2만 3550석', '이만 삼천오백오십 석').replace('146km', '백사십육 킬로').replace('120m', '백이십 미터')
    t = t.replace('2할 1푼 4리', '이할 일푼 사리').replace('1할 9푼', '일할 구푼')
    t = t.replace('8점대', '팔 점대').replace('3과 3분의 1이닝', '삼과 삼분의 일 이닝').replace('8.10', '팔 점 일영').replace('11.16', '십일 점 일육').replace('3.68', '삼 점 육팔').replace('4.75', '사 점 칠오')
    t = t.replace('4.19', '사 점 일구').replace('4.52', '사 점 오이').replace('5와 3분의 2이닝', '오와 삼분의 이 이닝').replace('5와 3분의 1이닝', '오와 삼분의 일 이닝')
    for a_, b_ in (('6과 3분의 2이닝', '육과 삼분의 이 이닝'), ('4와 3분의 2이닝', '사와 삼분의 이 이닝'), ('4와 3분의 1이닝', '사와 삼분의 일 이닝'), ('1과 3분의 1이닝', '일과 삼분의 일 이닝'), ('3분의 1이닝', '삼분의 일 이닝'), ('11월 1일', '십일월 일일')):
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
    n = re.sub(r'대 ([영일이삼사오육칠팔구])승리', r'대 \1 승리', n)
    n = n.replace('볼넷', '볼 넷')   # 10/27 사용자: '뽈넷'으로 읽혀서 띄어 씀
    return n
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / ')).replace('6과 3분의 2이닝', '6⅔이닝').replace('3과 3분의 1이닝', '3⅓이닝').replace('5와 3분의 2이닝', '5⅔이닝').replace('5와 3분의 1이닝', '5⅓이닝').replace('4와 3분의 2이닝', '4⅔이닝').replace('4와 3분의 1이닝', '4⅓이닝').replace('1과 3분의 1이닝', '1⅓이닝').replace('3분의 1이닝', '⅓이닝')

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
NAIL, FED, KDY, CAS, NA, HJS = C + "P17_네일_역투C", "경기/페덱_사용자제공_1004", C + "P17_김도영_질주", C + "P18_카스트로_환호", "경기/나성범_세리머니_KIA제공", "경기/한준수_주루_KIA제공"
JSH, OLLER, HUR, ISM, DIAZ, CHOI = C + "P18_전상현_역투", C + "P18_올러_투구", C + "P20_후라도_투구", C + "P31_이승민_삼성제공", C + "FA9_디아즈_경기", C + "FA10_최형우_100타점"
GJU = "경기/구자욱_세리머니_0827_삼성제공"
NAIL2, FED2, KDY2, KDY3, CAS2, HJS2 = C + "P17_네일_투구", C + "FA9_페덱_환호", C + "P22_김도영_만루포환호", "경기/김도영_세리머니_1017_KIA제공", C + "P18_카스트로_엄지", C + "P18_한준수_세리머니"
OLLER2, HUR2, KJY = C + "P18_올러_포효", "경기/후라도_박수_삼성제공", C + "T12_김재윤"
PJM, WTI = C + "P22_박진만_더그아웃", C + "P29_원태인_2026"
SSB, KIAC = "#074CA1", "#C70125"
def pv(img, name, sub, viz=(), stats=(), team="KIA", **k): return S(0, "pstat", img=img, team=team, name=name, sub=sub, viz=list(viz), stats=list(stats), **k)
def tm(team, name, sub, viz=(), stats=(), **k): return pv(None, name, sub, viz, stats, team=team, **k)
def dm(title, bat, score, outs, steps, **k): return S(0, "diamond", title=title, bat=bat, batIdx=(1 if bat == "삼성" else 0), score=score, outs=outs, steps=steps, away="KIA", home="삼성", **k)
N3 = [None, None, None]
BOX = [{"team": "KIA", "runs": [2, 0, 2, 1, 0, 0, 0, 0, 0], "r": 5, "hi": True}, {"team": "삼성", "runs": [0, 0, 0, 0, 1, 0, 0, 0, 0], "r": 1}]
PO1 = [g5(n="1차전", venue="대구", home="삼성", win="KIA", at=0), g5(n="2차전", venue="대구", home="삼성", at=0),
       g5(n="3차전", venue="광주", home="KIA", at=0), g5(n="4차전", venue="광주", home="KIA", at=0), g5(n="5차전", venue="대구", home="삼성", at=0)]


K = {}
R2 = getattr(_g['_t'], 'R2', 'KIA'); KW = R2 == 'KIA'
SPW = '3차전 선발' if getattr(_g['_t'], 'SP', '유력') == '확정' else '3차전 선발 유력'
TODO = lambda: tm("KIA", "TODO", "경기 뒤 채움", [], [])
YHJ, WTI2, LBH = "경기/양현종_글러브_1012_KIA제공", "경기/원태인_역투_삼성제공", C + "P22_이범호_기자회견"
# ── 오프닝·1장·2장 (경기 뒤 채움) ──
HUR3, OLL, DIA, CHW, CHW2, LER, KJC, WTI3, CASK = "경기/후라도_박수_삼성제공", "경기/올러_경기_KIA제공", "경기/디아즈_경기_삼성제공", "경기/최형우_만루포미소_0826_삼성제공", "경기/최형우_100타점_0918_삼성제공_중앙", "경기/이의리_상체_KIA제공", "상황별/김지찬_상체", "경기/원태인_투구_0828_삼성제공", C + "P18_카스트로_환호"
PSG2 = "상황별/박승규_타격_0830_삼성제공"
K['o0'] = S(0, "matchup", left="삼성", right="KIA", score="8 : 3", tag="플레이오프 2차전")
K['o1'] = pv(CHW, "최형우", "42살 · 삼성 좌익수", [], [st("포스트시즌", "역대 최고령 홈런", 1.0, hi=True), st("시리즈", "1승 1패", 3.0)], team="삼성")
K['o6'] = toc(-1)
K['g0'] = toc(1)
K['g1'] = S(0, "duel", title="플레이오프 2차전 선발", left=dict(img=HUR3, name="후라도", team="삼성", role="삼성 선발", at=1.0), right=dict(img=OLL, name="올러", team="KIA", role="KIA 선발", at=2.0), vsAt=1.5)
def sb2(kia, sam, hi, label, la): return S(0, "scoreboard", title="플레이오프 2차전", rows=[{"team": "KIA", "runs": kia, "r": sum(kia)}, {"team": "삼성", "runs": sam, "r": sum(sam), "hi": True}], hi=hi, label=label, labelAt=la, chain="box2")
K['g2'] = sb2([0, 0, 1], [0, 0], [3], "3회초 · 이호연 희생플라이", 2.5)
G3I = [dict(img=PSG2, name="박승규", team="삼성", note="동점 2루타"), dict(img=GJU, name="구자욱", team="삼성", note="역전 적시타"), dict(img=DIA, name="디아즈", team="삼성", note="투런 홈런")]
K['g3'] = S(0, "people", title="3회말 · 삼성 반격", items=[dict(x, at=a) for x, a in zip(G3I, [1.0, 2.0, 3.0])], chain="g3")
K['g4'] = S(0, "people", title="3회말 · 삼성 반격", items=[dict(x, at=-1) for x in G3I], text="4대1", textAt=1.0, size=110, chain="g3")
K['g5'] = S(0, "plog", img=OLL, name="올러", team="KIA", sub="KIA 선발", stamp=dict(t="5회말 2아웃 강판", at=1), blocks=[dict(type="inn", ip=4.667, at=2), dict(type="runs", n=5, at=2.5)])
K['g6'] = S(0, "people", title="5회말 · 바뀐 투수 이의리", items=[dict(img=LER, name="이의리", team="KIA", note="볼넷 · 몸에 맞는 공", at=1.0), dict(img=CHW2, name="최형우", team="삼성", note="밀어내기 볼넷", at=2.0)], text="5대1", textAt=3.0, size=110)
K['g7'] = S(0, "people", title="6회말 · 삼성 추가점", items=[dict(img=KJC, name="김지찬", team="삼성", note="1타점 2루타", at=1.0), dict(img=PSG2, name="박승규", team="삼성", note="희생플라이", at=2.0)], text="7대1", textAt=3.0, size=110)
K['g8'] = sb2([0, 0, 1, 0, 0, 0, 1], [0, 0, 4, 0, 1, 2], [7], "7회초 · 폭투로 1점", 1.0)
K['g9'] = pv(CHW, "최형우", "삼성 좌익수 · 7회말", [vstamp("솔로 홈런", 1.0, "gold", size=56)], [st("점수", "8대2", 2.0, hi=True)], team="삼성")
K['g10'] = pv(CHW, "최형우", "삼성 좌익수 · 7회말", [], [st("포스트시즌 역대 최고령 홈런", "42살 10개월 11일", 1.0, hi=True)], team="삼성")
K['g11'] = S(0, "people", title="8회초 · 9회초", items=[dict(img=CASK, name="카스트로", team="KIA", note="땅볼 타점", at=1.0), dict(img=WTI2, name="원태인", team="삼성", note="9회 · 1이닝 무실점", at=3.0)])
K['g12'] = sb2([0, 0, 1, 0, 0, 0, 1, 1, 0], [0, 0, 4, 0, 1, 2, 1, 0], [], "삼성 8대3 승리", 1.0)
PJM2 = "경기/박진만_박수_0908_삼성제공"
K['r0'] = toc(2)
K['r1'] = pv(CHW2, "최형우", "이유 하나 · 삼성 좌익수", [vstamp("좌익수 최형우", 1.0, "gold", size=56)], [], team="삼성")
K['r2'] = pv(CHW2, "최형우", "이유 하나 · 삼성 좌익수", [vq("박진만 감독", "공격력 극대화 필요", 1.0)], [], team="삼성")
K['r3'] = pv(CHW2, "최형우", "이유 하나 · 삼성 좌익수", [], [st("2차전", "3타수 2안타 2타점", 1.0), st("7회말", "솔로 홈런", 1.0, hi=True)], team="삼성")
K['r4'] = pv(CHW2, "최형우", "이유 하나 · 삼성 좌익수", [], [st("6회초 수비", "2루 송구로 카스트로 아웃", 1.0, hi=True)], team="삼성")
K['r5'] = S(0, "plog", img=HUR3, name="후라도", team="삼성", sub="이유 둘 · 삼성 선발", blocks=[dict(type="pitch", n=108, k="투구 수", at=2), dict(type="inn", ip=6.667, at=3), dict(type="runs", n=2, at=3.3)])
# ── 3장 · 3차전 예상 (경기 전 준비 · R2 두 벌) ──
K['c0'] = toc(3)
G3 = [dict(PO1[0]), dict(PO1[1], win=R2), dict(PO1[2], tag=("이기면 한국시리즈" if KW else "먼저 2승"), at=(3.0 if KW else 4.0), **({"glow": "KIA", "glowAt": 3.0} if KW else {})), dict(PO1[3]), dict(PO1[4])]
K['c1'] = S(0, "series5", tc={"삼성": SSB}, title=("플레이오프 · KIA 2승" if KW else "플레이오프 · 1승 1패"), games=G3, pills=[dict(label="3차전 · 10월 29일(목) 오후 6시 30분 · 광주", at=1.0, c="#12161F")])
if KW:
    K['c2'] = S(0, "tline", title="플레이오프 2연패 뒤 3연승 · 역대 3팀", items=[dict(d="1996년", t="현대", at=2.0), dict(d="2009년", t="SK", at=3.0), dict(d="2023년", t="KT", at=4.0, c="bad", big=True)])
else:
    K['c2'] = S(0, "tline", title="역대 5전 3선승제 플레이오프", items=[dict(d="1차전 · 2차전", t="1승 1패", at=1.0), dict(d="3차전", t="승리", at=1.4), dict(d="한국시리즈 진출", t="16번 중 9번 · 56.3%", at=2.0, c="gold", big=True)])
SRK, CWT = "경기/시라카와_투구_KIA제공", "경기/최원태_경기_삼성제공"
K['c3'] = S(0, "people", title=SPW, items=[dict(img=SRK, name="시라카와", note="KIA", at=1.0), dict(img=CWT, name="최원태", note="삼성", at=2.0)], chain="c3")
K['c3a'] = pv(WTI2, "원태인", "삼성 투수", [vq("박진만 감독 · 2차전 전", "태인이가 출전한다면 3차전은 최원태", 4.0)], [st("2차전", "9회 등판", 1.0, hi=True)], team="삼성")
def card(P, viz=(), stats=()):
    """후보 한 명 = '○○가 나오면' 카드. 장면마다 그 줄에서 새로 생기는 칸만 적는다 — 앞 줄 칸은 -1, 뒤 줄 칸은 자리만(50)으로 아래 묶음 처리가 채운다"""
    return pv(P[0], P[1], P[3], list(viz), list(stats), team=P[2])
def good(k, v, at): return vduo([dict(k=k, v=v, at=at, c="good")])
def bad(k, v, at): return vduo([dict(k=k, v=v, at=at, c="bad")])
PB = (SRK, "시라카와", "KIA", SPW + " · KIA")
K['cB1'] = card(PB, [vstamp("가을 기세", 1.0, "gold", size=50)])
K['cB2'] = card(PB, [good("준PO 3차전 · 볼넷 없이 1실점 · 삼진 9개", "아시아쿼터 첫 PS 승", 0.3)])
K['cB3'] = card(PB, [bad("올해 정규시즌 전체 · 18경기 4승 5패", "평균자책점 4.75", 1.0)])
PD = (CWT, "최원태", "삼성", SPW + " · 삼성")
K['cD1'] = card(PD, [bad("올해 정규시즌 KIA전", "평균자책점 8점대", 2.0)], [])
K['cD2'] = card(PD, [good("2025 준PO · PO 2차전", "6이닝 무실점 · 7이닝 1실점", 3.6)], [st("2024년까지 가을", "평균자책점 11.16", 1.0)])
K['cD3'] = card(PD, [vstamp("5차전엔 흔들림", 0.4, "gold", size=50)], [st("2025 PO 5차전", "3⅓이닝 5실점", 0.3)])
K['c12'] = S(0, "gamestrip", gat=[3.0, 3.2, 3.4, 4.0, 4.2], teams={"K": "KIA"}, games=[["1차전", "K"], ["2차전", "K"], ["5차전", "K"], ["1차전", "K"], ["2차전", "K"]], sw=240, title="KIA · 광주 가을야구",
             groups=[{"from": 0, "to": 2, "label": "2024 한국시리즈 · 광주", "team": "KIA", "at": 2.0}, {"from": 3, "to": 4, "label": "2026 준PO · 광주", "team": "KIA", "at": 4.0}])
# ── 4장 · 3차전 키플레이어 (경기 뒤) ──
K['k0'] = toc(4)
K['k1'] = pv(WTI3, "원태인", "삼성 투수", [vstamp("삼성 키플레이어", 0.3, "gold", size=56)], [], team="삼성")
K['k4'] = pv(CASK, "카스트로", "KIA 타자", [vstamp("KIA 키플레이어", 0.3, "gold", size=56)], [])
K['k5'] = pv(CASK, "카스트로", "KIA 타자", [], [st("1차전", "4타수 3안타 3타점", 1.0, hi=True), st("1차전 3회", "투런 홈런", 2.0), st("2차전", "8회 타점", 5.0)])
K['k6'] = pv(CASK, "카스트로", "KIA 타자", [], [st("3차전 · 광주", "카스트로가 터지면", 1.0)])
K['z0'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("광주", "KIA 강세", 3.0), st("올해 정규시즌 맞대결 평균자책점", "시라카와가 더 낮음", 4.0), st("삼성 변수", "뒤에 나올 원태인", 7.0, hi=True)])
K['z1'] = S(0, "question", text=("3차전 광주\nKIA 끝낼까? 삼성 반격?" if KW else "3차전\n먼저 2승은 누구?"), logos=["KIA", "삼성"], logoSize=230, size=104)
# ── 10/27 22:50 사용자 "8분 넘어야돼" — 2차전 흐름·이유·3차전 예상·키플레이어 늘림 ──
HJS_, KHR, PJH, RJH, LJH, NSB, HJS3 = "경기/하주석_인사_KIA제공", "경기/김호령_만루포_0821_KIA제공", "경기/박재현_주루_KIA제공", C + "G18_류지혁_A", "상황별/이재현_상체", "경기/나성범_세리머니_KIA제공", "경기/한준수_주루_KIA제공"
KDYb = "경기/김도영_세리머니_1017_KIA제공"
K['o1a'] = tm("삼성", "삼성 타선", "플레이오프 1·2차전", [], [st("1차전", "안타 2개", 1.0), st("2차전", "8점", 2.0, hi=True)])
B3a = dict(inn="3회초", score=[0, 0], outs=0, bases=N3, away="KIA", home="삼성")
R3a = [dict(name="하주석", img=HJS_, team="KIA", res="안타", kind="on", bases=["하주석", None, None], outs=0, score=[0, 0]),
       dict(name="김호령", img=KHR, team="KIA", res="희생번트", kind="out", bases=[None, "하주석", None], outs=1, score=[0, 0]),
       dict(name="박재현", img=PJH, team="KIA", res="내야안타", kind="on", bases=["박재현", None, "하주석"], outs=1, score=[0, 0]),
       dict(name="이호연", img="경기/이호연_세리머니_KIA제공", team="KIA", res="희생플라이", kind="run", bases=["박재현", None, None], outs=2, score=[1, 0], rbi="+1")]
def r3a(ats): return S(0, "rally", bug=B3a, plays=[dict(x, at=a) for x, a in zip(R3a, ats)], chain="r3a")
K['g2'] = r3a([50, 50, 50, 50]); K['g2b'] = r3a([0.3, 1.0, 2.0, 50]); K['g2c'] = r3a([-1, -1, -1, 0.3])
B3b = dict(inn="3회말", score=[1, 0], outs=0, bases=N3, away="KIA", home="삼성")
R3b = [dict(name="류지혁", img=RJH, team="삼성", res="볼넷", kind="on", bases=["류지혁", None, None], outs=0, score=[1, 0]),
       dict(name="이재현", img=LJH, team="삼성", res="희생번트", kind="out", bases=[None, "류지혁", None], outs=1, score=[1, 0]),
       dict(name="김지찬", img=KJC, team="삼성", res="뜬공", kind="out", bases=[None, "류지혁", None], outs=2, score=[1, 0]),
       dict(name="박승규", img=PSG2, team="삼성", res="동점 2루타", kind="run", bases=[None, "박승규", None], outs=2, score=[1, 1], rbi="+1")]
def r3b(ats): return S(0, "rally", bug=B3b, plays=[dict(x, at=a) for x, a in zip(R3b, ats)], chain="r3b")
K['g3'] = r3b([50, 50, 50, 50]); K['g3b'] = r3b([0.3, 1.0, 50, 50]); K['g3c'] = r3b([-1, -1, 0.3, 1.0])
B3c = dict(inn="3회말", score=[1, 1], outs=2, bases=[None, "박승규", None], away="KIA", home="삼성")
R3c = [dict(name="구자욱", img=GJU, team="삼성", res="역전 적시타", kind="run", bases=["구자욱", None, None], outs=2, score=[1, 2], rbi="+1"),
       dict(name="디아즈", img=DIA, team="삼성", res="투런 홈런 · 6구째 151km 직구", kind="run", bases=N3, outs=2, score=[1, 4], rbi="+2")]
def r3c(ats): return S(0, "rally", bug=B3c, plays=[dict(x, at=a) for x, a in zip(R3c, ats)], chain="r3c")
K['g3d'] = r3c([0.4, 50]); K['g3e'] = r3c([-1, 1.0])
K['g4'] = sb2([0, 0, 1], [0, 0, 4], [3], "3회말 · 4대1", 1.0)
K['g5'] = pv(OLL, "올러", "KIA 선발 · 5회말", [vstamp("5회말 2아웃 강판", 2.0, "bad", size=52)], [st("5회말 2아웃", "박승규 내야안타", 1.0)])
B5 = dict(inn="5회말", score=[1, 4], outs=2, bases=["박승규", None, None], away="KIA", home="삼성")
R5 = [dict(name="이의리", img=LER, team="KIA", res="등판", kind="on", bases=["박승규", None, None], outs=2, score=[1, 4]),
      dict(name="구자욱", img=GJU, team="삼성", res="볼넷", kind="on", bases=["구자욱", "박승규", None], outs=2, score=[1, 4]),
      dict(name="디아즈", img=DIA, team="삼성", res="몸에 맞는 공", kind="on", bases=["디아즈", "구자욱", "박승규"], outs=2, score=[1, 4]),
      dict(name="최형우", img=CHW2, team="삼성", res="밀어내기 볼넷", kind="run", bases=["최형우", "디아즈", "구자욱"], outs=2, score=[1, 5], rbi="+1")]
def r5(ats): return S(0, "rally", bug=B5, plays=[dict(x, at=a) for x, a in zip(R5, ats)], chain="r5")
K['g6'] = r5([0.3, 1.0, 2.0, 50]); K['g6b'] = r5([-1, -1, -1, 1.0])
K['g6c'] = S(0, "plog", img=OLL, name="올러", team="KIA", sub="KIA 선발 · 2차전 기록", blocks=[dict(type="inn", ip=4.667, at=2), dict(type="runs", n=5, at=2.5)])
K['g7'] = S(0, "people", title="6회말 · 삼성 추가점", items=[dict(img=KJC, name="김지찬", team="삼성", note="1타점 2루타", at=1.0), dict(img=PSG2, name="박승규", team="삼성", note="희생플라이", at=2.0)], text="7대1", textAt=3.0, size=110)
TL7 = [dict(k="7회초 득점", v=1, at=50, hi=True)]
R7 = [dict(name="나성범", img=NSB, team="KIA", res="볼넷", kind="on"), dict(name="한준수", img=HJS3, team="KIA", res="안타 · 2아웃 1·3루", kind="on"),
      dict(name="후라도", img=HUR3, team="삼성", res="폭투 · 1실점", kind="run"), dict(name="김호령", img=KHR, team="KIA", res="실책 · 다시 1·3루", kind="on"),
      dict(name="박재현", img=PJH, team="KIA", res="이승민에게 삼진", kind="out")]
def r7(tat, pat): return S(0, "rally", title="KIA · 7회초", tally=[dict(x, at=a) for x, a in zip(TL7, tat)], plays=[dict(x, at=a) for x, a in zip(R7, pat)], chain="r7")
K['g8'] = r7([50], [50] * 5); K['g8b'] = r7([50], [0.3, 1.0, 50, 50, 50]); K['g8c'] = r7([2.0], [-1, -1, 0.3, 50, 50]); K['g8d'] = r7([-1], [-1, -1, -1, 0.3, 3.0])
K['g9'] = pv(CHW, "최형우", "삼성 좌익수 · 7회말", [vstamp("125m 솔로 홈런", 3.0, "gold", size=56)], [st("상대", "김범수 슬라이더", 1.0), st("점수", "8대2", 4.0, hi=True)], team="삼성")
K['g10'] = pv(CHW, "최형우", "삼성 좌익수 · 7회말", [], [st("포스트시즌 역대 최고령 홈런", "42살 10개월 11일", 1.0, hi=True)], team="삼성")
K['g10b'] = pv(CHW, "최형우", "삼성 좌익수 · 7회말", [], [st("포스트시즌 최고령", "출장 · 안타 · 타점", 1.0)], team="삼성")
TL8 = [dict(k="8회초 득점", v=1, at=50, hi=True)]
R8 = [dict(name="김태군", img="경기/김태군_덕아웃_0729_KIA제공", team="KIA", res="대타 2루타", kind="on"), dict(name="카스트로", img=CASK, team="KIA", res="땅볼 타점", kind="run")]
K['g11'] = S(0, "rally", title="KIA · 8회초", tally=[dict(TL8[0], at=3.0)], plays=[dict(R8[0], at=1.0), dict(R8[1], at=2.0)])
K['g11b'] = pv(WTI2, "원태인", "삼성 투수 · 9회초", [], [st("2차전 9회", "1이닝 무실점", 3.0, hi=True), st("탈삼진", "2개", 2.0)], team="삼성")
K['r1'] = pv(CHW2, "최형우", "이유 하나 · 삼성 좌익수", [vstamp("좌익수 최형우", 1.0, "gold", size=56)], [], team="삼성")
K['r2'] = pv(CHW2, "최형우", "이유 하나 · 삼성 좌익수", [vq("박진만 감독", "공격력 극대화 필요", 1.0)], [st("좌익수 카드", "적중", 2.0, hi=True)], team="삼성")
K['r3'] = pv(CHW2, "최형우", "이유 하나 · 삼성 좌익수", [], [st("2차전", "3타수 2안타 2타점 · 홈런", 1.0, hi=True), st("볼넷", "1개", 2.0)], team="삼성")
K['r4'] = pv(CHW2, "최형우", "이유 하나 · 삼성 좌익수", [], [st("6회초 수비", "2루 송구로 카스트로 아웃", 1.0, hi=True)], team="삼성")
K['r5'] = S(0, "plog", img=HUR3, name="후라도", team="삼성", sub="이유 둘 · 삼성 선발", blocks=[dict(type="pitch", n=108, k="투구 수", at=2), dict(type="inn", ip=6.667, at=3), dict(type="runs", n=2, at=3.3)])
K['r6'] = pv(PSG2, "박승규", "이유 셋 · 삼성 외야수", [vstamp("이유 셋", 0.3, "gold", size=56)], [], team="삼성")
K['r7'] = pv(PSG2, "박승규", "이유 셋 · 삼성 외야수", [], [st("2차전", "3타수 2안타 2타점", 1.0, hi=True), st("3회", "동점 2루타", 3.0), st("5회", "내야안타 · 올러 강판", 5.0), st("6회", "희생플라이", 7.0)], team="삼성")
K['r8'] = pv(PSG2, "박승규", "이유 셋 · 삼성 외야수", [], [st("1차전", "헤드샷 맞음", 0.3), st("2차전", "승리 이끔", 2.0)], team="삼성")
K['r9'] = tm("KIA", "KIA 타선", "플레이오프 2차전", [], [st("1차전", "5점", 0.3), st("2차전 안타", "6개", 2.0), st("2차전 득점", "3점", 3.0, hi=True)])
K['r10'] = tm("KIA", "KIA 타선", "플레이오프 2차전", [], [st("7회 2아웃 1·3루", "두 번 · 1점", 2.0)])
K['c3c'] = pv(PJM2, "박진만", "삼성 감독 · 2차전 전", [vq("박진만 감독 · 2차전 전", "페덱이 좀 더 빨리 출전할 수도", 2.0)], [], team="삼성")
K['c3d'] = pv(CWT, "최원태", SPW + " · 삼성", [], [st("3차전 변수", "최원태가 흔들리면 삼성 마운드 조기 가동", 0.3)], team="삼성")
K['cB2b'] = card(PB, [], [st("올해 정규시즌 삼성전", "3경기 1승 1패", 1.0), st("평균자책점", "3.68", 2.0, hi=True)])
K['c12b'] = tm("KIA", "KIA 불펜", "플레이오프 1·2차전", [vstamp("불펜도 변수", 1.0, "gold", size=56)], [])
K['c12c'] = tm("KIA", "KIA 불펜", "플레이오프 1·2차전", [], [st("1차전 · 네일 퇴장 뒤", "5명 4⅔이닝 무실점", 1.0, hi=True), st("2차전 · 6회부터", "3점 더 내줌", 5.0)])
K['k3b'] = pv(DIA, "디아즈", "삼성 타자", [vstamp("지켜볼 타자", 1.0, "gold", size=56)], [], team="삼성")
K['k3c'] = pv(DIA, "디아즈", "삼성 타자", [], [st("2차전 3회", "투런 홈런", 0.3, hi=True), st("5회", "몸에 맞는 공 · 만루", 1.0)], team="삼성")
K['k3d'] = pv(DIA, "디아즈", "삼성 타자", [], [st("광주에서도", "한 방이 나오면", 1.0)], team="삼성")
K['k7'] = pv(KDYb, "김도영", "KIA 타자", [vstamp("깨어나야 할 타자", 1.0, "gold", size=52)], [])
K['k8'] = pv(KDYb, "김도영", "KIA 타자", [], [st("1차전", "3타수 2안타 · 도루 1 · 2득점", 1.0, hi=True), st("2차전", "1차전만큼은 아님", 4.0)])
K['k9'] = pv(KDYb, "김도영", "KIA 타자", [], [st("3차전 · 광주", "방망이와 발", 1.0)])
K['z0'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("3차전", "KIA 조금 유리", 2.0, hi=True), st("광주", "KIA 강세", 3.0), st("상대 팀전 정규시즌 기록", "시라카와가 더 좋음", 5.0)])
K['z0b'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("삼성 변수", "2차전에서 살아난 타선", 1.0, hi=True)])
K['z0c'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("승부처", "시라카와의 초반", 1.0, hi=True)])
# ── 10/27 23시 — 경기 전 수 싸움 장 · 최형우 기록 · 3차전 관전 포인트 ──
PJMc, KSY = "경기/박진만_박수_0908_삼성제공", "경기/이범호_박수_0915_KIA제공"
K['p0'] = toc(0)
K['p1'] = tm("삼성", "삼성 타선", "플레이오프 1차전", [], [st("1차전", "막힌 타선", 1.0, hi=True)])
K['p2'] = S(0, "duel", title="삼성 · 2차전 좌익수", left=dict(img="상황별/김성윤_투런", name="김성윤", team="삼성", role="벤치로", at=1.0), right=dict(img=CHW2, name="최형우", team="삼성", role="좌익수 선발", at=2.0), vsAt=1.5)
K['p3'] = pv(WTI2, "원태인", "삼성 투수 · 2차전", [vstamp("불펜 대기", 1.0, "gold", size=56)], [st("마무리 김재윤", "부상으로 빠짐", 0.3), st("원래 예상", "3차전 선발", 1.0)], team="삼성")
K['p4'] = pv(WTI2, "원태인", "삼성 투수 · 2차전", [vq("박진만 감독 · 2차전 전", "이기고 있으면 무조건 출전", 1.0)], [], team="삼성")
K['p5'] = tm("KIA", "KIA 라인업", "플레이오프 2차전", [], [])
K['p6'] = tm("KIA", "KIA 라인업", "플레이오프 2차전", [], [st("빠짐", "박정우", 0.3), st("2번 지명타자", "이호연", 1.0, hi=True), st("중견수", "김호령", 2.0)])
K['p7'] = pv(KSY, "이범호", "KIA 감독 · 2차전 전", [vq("이범호 감독 · 2차전 전", "원태인이 안 올라오게 만드는 게 중요", 1.0)], [])
K['p8'] = pv(WTI2, "원태인", "삼성 투수 · 2차전", [vstamp("박진만 감독의 수 적중", 1.0, "gold", size=52)], [st("등판", "9회 · 5점 앞선 상황", 3.0, hi=True)], team="삼성")
K['g1b'] = pv(CHW, "최형우", "삼성 좌익수 · 2회말", [], [st("첫 타석", "오른쪽 안타", 1.0, hi=True)], team="삼성")
K['g7a'] = pv(CHW2, "최형우", "삼성 좌익수 · 6회초", [vstamp("수비", 1.0, "gold", size=56)], [], team="삼성")
K['g7b'] = pv(CHW2, "최형우", "삼성 좌익수 · 6회초", [], [st("카스트로 타구", "왼쪽 담장 맞음", 1.0), st("최형우 송구", "2루에서 아웃", 2.0, hi=True)], team="삼성")
K['g10c'] = pv(CHW, "최형우", "삼성 좌익수 · 7회말", [], [st("최고령 출장 · 종전", "2017 이호준 41살 8개월 13일", 1.0)], team="삼성")
K['g10d'] = pv(CHW, "최형우", "삼성 좌익수 · 7회말", [], [st("최고령 홈런 · 종전", "2024 한국시리즈 5차전 · KIA 시절", 1.0)], team="삼성")
K['r11'] = S(0, "bars", title="플레이오프 1·2차전 합계 득점", items=[dict(label="KIA", value=8, unit="점", at=1.0), dict(label="삼성", value=9, unit="점", at=3.0, hi=True)])
K['cB1b'] = card(PB, [vq("이범호 감독 · 준PO 3차전 전", "시라카와 빠른 교체도 가능", 2.0)], [])
K['cB1c'] = card(PB, [], [st("준PO 3차전", "5이닝 버팀", 1.0, hi=True)])
K['cD4'] = card(PD, [], [st("2024년 겨울", "4년 최대 70억 원 · 삼성 이적", 1.0)])
K['cD5'] = card(PD, [vstamp("증명의 무대", 2.0, "gold", size=56)], [])
K['c12a'] = S(0, "gamestrip", gat=[2.0, 2.0, 2.0, 2.0, 2.0], teams={"K": "KIA", "S": "삼성"}, games=[["1차전", "K"], ["2차전", "K"], ["3차전", "S"], ["4차전", "K"], ["5차전", "K"]], sw=240, title="2024 한국시리즈 · KIA 4승 1패 우승",
              groups=[{"from": 0, "to": 4, "label": "2024 한국시리즈", "team": "KIA", "at": 0.3}])
K['c13'] = tm("KIA", "3차전 관전 포인트", "10월 29일 · 광주", [], [st("하나", "시라카와의 초반", 50), st("둘", "최원태의 KIA전 약세", 50), st("셋", "원태인이 나올 수 있는 9회", 50)])
K['c14'] = tm("KIA", "3차전 관전 포인트", "10월 29일 · 광주", [], [st("하나", "시라카와의 초반", 0.3), st("둘", "최원태의 KIA전 약세", 1.0), st("셋", "원태인이 나올 수 있는 9회", 2.0, hi=True)])
K['r5b'] = pv(FED, "페덱", "삼성 선발 · 1차전", [], [st("1차전", "4⅔이닝 5실점", 1.0, hi=True)], team="삼성")
K['k2a'] = pv(WTI3, "원태인", "삼성 투수", [vstamp("광주 기억은 엇갈림", 1.0, "gold", size=50)], [], team="삼성")
K['k2b'] = pv(WTI3, "원태인", "삼성 투수", [], [st("올해 정규시즌 KIA전 · 광주", "5⅔이닝 6실점", 1.0)], team="삼성")
K['k2c'] = pv(WTI3, "원태인", "삼성 투수", [], [st("2024 한국시리즈 1차전 · 광주", "5이닝 무실점", 0.3)], team="삼성")
K['k8b'] = pv(KDYb, "김도영", "KIA 타자", [], [st("1차전 5회", "페덱과 13구 승부", 1.0)])
K['o1b'] = pv(CHW, "최형우", "42살 · 삼성 좌익수", [vstamp("공격 · 수비 모두", 1.0, "gold", size=56)], [], team="삼성")
K['p9'] = tm("KIA", "KIA 라인업", "바꾼 카드의 결과", [], [st("3회", "첫 점수에 힘", 1.0, hi=True)])
K['r10b'] = tm("KIA", "KIA 불펜", "플레이오프 2차전", [], [st("이의리 · 5회", "밀어내기 볼넷", 1.0), st("김범수 · 7회", "솔로 홈런", 2.0, hi=True)])
K['z0e'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("시라카와 5회까지", "KIA 쪽", 0.3), st("최원태 긴 이닝", "삼성 쪽", 1.0)])
K['r8b'] = pv(GJU, "구자욱", "삼성 외야수 · 3회말", [vstamp("결승타", 1.0, "gold", size=56)], [st("3회말", "역전 적시타", 1.0)], team="삼성")
K['k2d'] = pv(WTI3, "원태인", "삼성 투수", [], [st("3차전", "불펜?", 0.3), st("4차전", "선발?", 1.0, hi=True)], team="삼성")
K['z0f'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("예상", "한두 점 차 접전", 1.0, hi=True)])
K['o1c'] = S(0, "duel", title="두 감독의 승부수", left=dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독", at=0.3), right=dict(img=KSY, name="이범호", team="KIA", role="KIA 감독", at=0.6), vsAt=1.0)
K['p6b'] = tm("KIA", "KIA 라인업", "플레이오프 2차전", [], [st("1번", "박재현", 3.0)])
K['p7b'] = pv(KSY, "이범호", "KIA 감독 · 2차전 전", [], [st("원태인 등판", "KIA가 지고 있거나 비슷한 상황", 1.0)])
K['g10f'] = pv(CHW, "최형우", "삼성 좌익수", [], [st("2025시즌 뒤 FA", "친정팀 삼성 복귀", 1.0), st("복귀 첫 가을", "최고령 기록", 3.0, hi=True)], team="삼성")
K['g12b'] = sb2([0, 0, 1, 0, 0, 0, 1, 1, 0], [0, 0, 4, 0, 1, 2, 1, 0], [], "1차전 설욕", 1.0)
K['c15'] = tm("KIA", "3차전 관전 포인트", "10월 29일 · 광주", [], [st("세 가지", "3차전 흐름 좌우", 1.0, hi=True)])
K['p3b'] = pv(KJY, "김재윤", "삼성 마무리", [], [st("2026 정규시즌", "35세이브", 1.0, hi=True)], team="삼성")
K['z0g'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("2차전 올러", "3회 4실점", 0.3)])
K['zt'] = toc(5)
K['r12'] = S(0, "people", title="플레이오프 데일리 MVP", items=[dict(img=CASK, name="카스트로", team="KIA", note="1차전", at=2.0), dict(img=HUR3, name="후라도", team="삼성", note="2차전", at=4.0)])
K['z0h'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("3차전", "끝까지 지켜봐야", 3.0)])
K['z0i'] = tm("KIA", "제 생각 · 3차전", "야구자판기 예상", [], [st("3차전 뒤", "4차전 예상 바로", 2.0)])
K['c12c2'] = tm("삼성", "삼성 불펜", "플레이오프 1·2차전", [], [st("1차전 · 페덱 강판 뒤", "무실점", 2.0, hi=True), st("2차전", "8회 1실점", 4.0)])
K['o1d'] = S(0, "series5", tc={"삼성": SSB}, title="플레이오프 · 1승 1패", games=[dict(PO1[0]), dict(PO1[1], win=R2), dict(PO1[2]), dict(PO1[3]), dict(PO1[4])], pills=[dict(label="3차전 · 광주", at=1.0, c="#12161F")])
# ── 10/28 0시 사용자 지적 반영: 2차전 흐름 = 승부처 다섯 장면, 랠리 카드는 한 장면 안에서만 나온다(빈 자리 숨김 금지 — 카드가 왼쪽에 치우침), 경기 뒤 발언 ──
HYO = "경기/이호연_세리머니_KIA제공"
for _k in ('g1b', 'g2b', 'g2c', 'g3b', 'g3d', 'g12b', 'r8b', 'r10'): K.pop(_k, None)
K['p9'] = S(0, "people", title="KIA가 바꾼 카드 · 3회", items=[dict(img=KHR, name="김호령", team="KIA", note="희생번트", at=2.0), dict(img=HYO, name="이호연", team="KIA", note="희생플라이 · 선제 타점", at=3.0)], text="1대0", textAt=1.0, size=110)
K['g2'] = S(0, "rally", bug=dict(inn="3회초", score=[0, 0], outs=1, bases=["박재현", None, "하주석"], away="KIA", home="삼성"), plays=[dict(R3a[3], at=3.0)])
K['g3'] = S(0, "rally", bug=B3b, plays=[dict(R3b[0], at=0.2), dict(R3b[1], at=0.6), dict(R3b[2], at=1.0)])
K['g3c'] = S(0, "rally", bug=dict(inn="3회말", score=[1, 0], outs=2, bases=[None, "류지혁", None], away="KIA", home="삼성"), plays=[dict(R3b[3], at=0.3), dict(R3c[0], res="역전 결승타", at=2.0)])
K['g3e'] = S(0, "rally", bug=dict(inn="3회말", score=[1, 2], outs=2, bases=["구자욱", None, None], away="KIA", home="삼성"), plays=[dict(R3c[1], res="투런 홈런 · 151km 직구", at=3.0)])
K['g4'] = pv(OLL, "올러", "KIA 선발 · 3회말", [vstamp("2아웃 뒤 4실점", 0.3, "bad", size=52)], [st("3회말", "1대0 → 1대4", 2.0, hi=True)])
K['g5'] = tm("KIA", "KIA 불펜", "두 번째 장면 · 5회말", [], [st("5회말", "KIA 불펜", 0.3, hi=True)])
K['g6'] = S(0, "rally", bug=B5, plays=[dict(R5[0], at=1.0), dict(R5[1], at=2.0), dict(R5[2], at=2.5), dict(R5[3], at=3.0)])
K['g6b'] = pv(KSY, "이범호", "KIA 감독", [vq("이범호 감독 · 2차전 전", "원태인이 안 올라오게 만드는 게 중요", 1.0)], [st("5회말 뒤", "1대5 · 4점 차", 3.0, hi=True)])
K['g7a'] = pv(CHW2, "최형우", "삼성 좌익수 · 6회초", [vstamp("세 번째 장면", 0.3, "gold", size=52)], [], team="삼성")
K['g7b'] = pv(CHW2, "최형우", "삼성 좌익수 · 6회초", [], [st("카스트로 타구", "왼쪽 담장 맞음", 1.0), st("최형우 송구", "2루에서 아웃", 3.0, hi=True)], team="삼성")
K['g7c'] = pv(CHW2, "최형우", "삼성 좌익수 · 6회초", [], [st("결과", "KIA 추격 차단", 1.0, hi=True)], team="삼성")
K['g8'] = tm("KIA", "KIA 타선", "네 번째 장면 · 7회초", [], [st("7회초", "놓친 기회", 1.0, hi=True)])
R7a = [dict(R7[0], at=0.2), dict(R7[1], res="안타 · 2아웃 1·3루", at=0.7), dict(R7[2], at=2.0)]
K['g8b'] = S(0, "rally", title="KIA · 7회초", tally=[dict(TL7[0], at=2.3)], plays=R7a)
K['g8c'] = S(0, "rally", title="KIA · 7회초", tally=[dict(TL7[0], at=-1)], plays=[dict(R7[3], res="실책 · 다시 2아웃 1·3루", at=0.3), dict(R7[4], at=3.0)])
K['g8d'] = tm("KIA", "KIA 타선", "7회초", [], [st("2아웃 1·3루", "두 번", 0.3), st("득점", "1점", 1.0, hi=True)])
K['g9'] = pv(CHW, "최형우", "삼성 좌익수 · 7회말", [vstamp("솔로 홈런", 2.0, "gold", size=56)], [st("상대", "김범수 슬라이더", 1.0), st("점수", "8대2", 3.0, hi=True)], team="삼성")
K['g7'] = S(0, "people", title="6회말 · 삼성 추가점", items=[dict(img=KJC, name="김지찬", team="삼성", note="1타점 2루타", at=1.0), dict(img=PSG2, name="박승규", team="삼성", note="희생플라이", at=1.5)], text="7대1", textAt=1.8, size=110)
K['r4b'] = S(0, "faces", items=[dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤", at=0, say="“최형우의 호수비로\n팀 분위기가 확실하게 올라갔다”", sayAt=1.0)])
K['r4c'] = S(0, "faces", items=[dict(img=CHW, name="최형우", team="삼성", role="삼성 좌익수 · 경기 뒤", at=0, say="“보살이 백 배는 좋았다”", sayAt=1.0)], chain="r4q")
K['r4d'] = S(0, "faces", items=[dict(img=CHW, name="최형우", team="삼성", role="삼성 좌익수 · 경기 뒤", at=-1, say="“말도 안 되게 잘 갔다\n운 좋게 잡았다”", sayAt=1.0)], chain="r4q")
K['c3e'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(img=CHW2, name="최형우", team="삼성", role="삼성 좌익수", at=1.0)], chain="c3q")
K['c3f'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤", at=0, say="“3차전에도\n좌익수로 나가야 한다”", sayAt=1.0), dict(img=CHW2, name="최형우", team="삼성", role="삼성 좌익수", at=-1)], chain="c3q")
K['c3g'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤", at=-1), dict(img=CHW2, name="최형우", team="삼성", role="삼성 좌익수", at=-1, say="“전화 한번 드려야겠다”", sayAt=1.0)], chain="c3q")
K['c3h'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤", at=-1), dict(img=CHW2, name="최형우", team="삼성", role="삼성 좌익수", at=-1, say="“단기전은 실수 하나로\n승패가 갈린다”", sayAt=1.0)], chain="c3q")

# ── 10/28 자체 검수: 이름 부르는 선수는 사진(라인업·불펜), 긴 한 사람 묶음은 나눠 글씨가 작아지지 않게, '제 생각'은 글만 있는 카드 대신 사진·대결 ──
PJW, KBS, SRK2, CWT2 = C + "P22_박정우_적시타", "경기/김범수_투구_0729_KIA제공", "경기/시라카와_투구_KIA제공", "경기/최원태_경기_삼성제공"
K['p6'] = S(0, "people", title="KIA 라인업 · 2차전", items=[dict(img=PJW, name="박정우", team="KIA", note="빠짐", at=0.3), dict(img=HYO, name="이호연", team="KIA", note="2번 지명타자", at=1.0), dict(img=KHR, name="김호령", team="KIA", note="중견수", at=2.0)], size=110)
K['p6b'] = S(0, "people", title="이범호 감독 · 1·2번 타자", items=[dict(img=KSY, name="이범호", team="KIA", note="KIA 감독", at=0), dict(img=PJH, name="박재현", team="KIA", note="1번", at=3.0), dict(img=HYO, name="이호연", team="KIA", note="2번", at=3.2)], size=110)
K['r10b'] = S(0, "people", title="KIA 불펜 · 2차전", items=[dict(img=LER, name="이의리", team="KIA", note="5회 밀어내기 볼넷", at=1.0), dict(img=KBS, name="김범수", team="KIA", note="7회 솔로 홈런", at=2.0)], size=110)
# 최형우 홈런·기록: g9~g10b 한 묶음, g10c~g10d 기록 묶음(이름 칸 다르게), g10f 따로 — 칸이 6개 쌓여 사진·글씨가 줄던 것
K['g10c'] = pv(CHW2, "최형우 · 최고령 기록", "포스트시즌", [], [st("최고령 출장 · 종전", "2017 이호준 41살 8개월 13일", 1.0)], team="삼성")
K['g10d'] = pv(CHW2, "최형우 · 최고령 기록", "포스트시즌", [], [st("최고령 홈런 · 종전", "2024 한국시리즈 5차전 · KIA 시절", 1.0, hi=True)], team="삼성")
K['g10f'] = pv(CHW, "최형우", "2025시즌 뒤 FA", [], [st("친정팀", "삼성 복귀", 2.0), st("복귀 첫 가을", "최고령 기록", 3.0, hi=True)], team="삼성")
# 김도영: 긴 칸을 둘로
K['k8'] = pv(KDYb, "김도영", "KIA 타자", [], [st("1차전", "3타수 2안타", 1.0, hi=True), st("1차전", "도루 1 · 2득점", 2.0), st("2차전", "1차전만큼은 아님", 4.0)])
# 제 생각
K['z0'] = S(0, "gamestrip", gat=[4.0, 4.1, 4.2, 4.3, 4.4], teams={"K": "KIA"}, games=[["1차전", "K"], ["2차전", "K"], ["5차전", "K"], ["1차전", "K"], ["2차전", "K"]], sw=240, title="제 생각 · 3차전 KIA 조금 유리",
             groups=[{"from": 0, "to": 2, "label": "2024 한국시리즈 · 광주", "team": "KIA", "at": 3.0}, {"from": 3, "to": 4, "label": "2026 준PO · 광주", "team": "KIA", "at": 5.0}])
K['z0a'] = S(0, "duel", title="선발 맞대결 · 올해 정규시즌", left=dict(img=SRK2, name="시라카와", team="KIA", role="삼성전 평균자책점 3.68", at=1.0), right=dict(img=CWT2, name="최원태", team="삼성", role="KIA전 평균자책점 8점대", at=2.0), vsAt=1.5)
K['z0b'] = tm("삼성", "삼성 타선", "제 생각 · 3차전 변수", [], [st("1차전", "안타 2개", 0.5), st("2차전", "8점", 1.0, hi=True)])
K['z0c'] = pv(SRK2, "시라카와", "제 생각 · 3차전 승부처", [vstamp("초반이 승부처", 1.0, "gold", size=52)], [])
K['z0g'] = pv(OLL, "올러", "2차전 · 3회말", [], [st("3회말", "4실점 · 흐름 넘어감", 1.0, hi=True)])
K['z0e'] = S(0, "duel", title="제 생각 · 흐름의 열쇠", left=dict(img=SRK2, name="시라카와", team="KIA", role="5회까지 버티면 KIA 쪽", at=0.2), right=dict(img=CWT2, name="최원태", team="삼성", role="길게 던지면 삼성 쪽", at=1.0), vsAt=0.6)
K['z0f'] = S(0, "question", text="한두 점 차\n접전 예상", logos=["KIA", "삼성"], logoSize=200, size=104)
K['z0h'] = S(0, "series5", tc={"삼성": SSB}, title="플레이오프 · 1승 1패", games=[dict(PO1[0]), dict(PO1[1], win=R2), dict(PO1[2]), dict(PO1[3]), dict(PO1[4])], pills=[dict(label="3차전 · 끝까지 지켜보기", at=1.0, c="#12161F")])
K['z0i'] = S(0, "series5", tc={"삼성": SSB}, title="플레이오프 · 1승 1패", games=[dict(PO1[0]), dict(PO1[1], win=R2), dict(PO1[2]), dict(PO1[3]), dict(PO1[4])], pills=[dict(label="3차전 뒤 · 4차전 예상", at=2.0, c="#12161F")])

# ── 10/28 1시 검수 에이전트 X 34 반영: 이름 부르는 순간 사진, 말 안 한 숫자 화면 금지, 텀 ──
K.pop('c3c', None)
ISMc, WTIc = C + "P31_이승민_삼성제공", "경기/원태인_역투_삼성제공"
K['p2'] = S(0, "duel", title="삼성 · 2차전 좌익수", left=dict(img="상황별/김성윤_투런", name="김성윤", team="삼성", role="벤치로", at=1.0), right=dict(img=CHW2, name="최형우", team="삼성", role="좌익수 선발", at=3.0), vsAt=2.5)
K['p3'] = S(0, "people", title="삼성 뒷문 · 2차전", items=[dict(img=KJY, name="김재윤", team="삼성", note="부상으로 빠짐", at=0), dict(img=WTIc, name="원태인", team="삼성", note="불펜 대기", at=1.0)], size=110)
K['p4'] = S(0, "faces", items=[dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 2차전 전", at=0, say="“이기고 있으면\n무조건 출전”", sayAt=1.0), dict(img=WTIc, name="원태인", team="삼성", role="삼성 투수", at=2.0)])
K['p7'] = S(0, "faces", items=[dict(img=KSY, name="이범호", team="KIA", role="KIA 감독 · 2차전 전", at=0, say="“원태인이 안 올라오게\n만드는 게 중요”", sayAt=1.5), dict(img=WTIc, name="원태인", team="삼성", role="삼성 투수", at=1.0)])
K['p7b'] = pv(WTI2, "원태인", "삼성 투수 · 2차전", [], [st("원태인 등판", "KIA가 지고 있거나 비슷한 상황", 1.0)], team="삼성")
K['p8'] = pv(WTI2, "원태인", "삼성 투수 · 2차전", [vstamp("삼성의 수 적중", 1.0, "gold", size=52)], [st("등판", "9회 · 5점 앞선 상황", 3.0, hi=True)], team="삼성")
K['p9'] = S(0, "people", title="KIA가 바꾼 카드 · 3회", items=[dict(img=KHR, name="김호령", team="KIA", note="희생번트", at=2.0), dict(img=HYO, name="이호연", team="KIA", note="희생플라이 · 선제 타점", at=3.0)], text="3회 첫 점수", textAt=1.0, size=110)
K['g2a'] = tm("삼성", "삼성 타선", "첫 번째 장면 · 3회말", [], [st("3회말", "삼성 공격", 0.3, hi=True)])
K['g2'] = S(0, "rally", bug=dict(inn="3회초", score=[0, 0], outs=1, bases=["박재현", None, "하주석"], away="KIA", home="삼성"), plays=[dict(R3a[3], at=1.0)])
K['g3e'] = S(0, "rally", bug=dict(inn="3회말", score=[1, 2], outs=2, bases=["구자욱", None, None], away="KIA", home="삼성"), plays=[dict(R3c[1], res="투런 홈런 · 151km 직구", at=0.3)])
K['g4'] = pv(OLL, "올러", "KIA 선발 · 3회말", [vstamp("2아웃 뒤 4실점", 0.3, "bad", size=52)], [st("3회말", "0대1 → 4대1", 1.0, hi=True)])
OLLp = dict(name="올러", img=OLL, team="KIA", res="2아웃 강판", kind="out", bases=["박승규", None, None], outs=2, score=[1, 4])
K['g6'] = S(0, "rally", bug=B5, plays=[dict(OLLp, at=0.2), dict(R5[0], at=1.0), dict(R5[1], at=2.0), dict(R5[2], at=3.0), dict(R5[3], at=5.0)])
K['g6b'] = S(0, "people", title="이범호 감독의 계산", items=[dict(img=KSY, name="이범호", team="KIA", note="KIA 감독", at=0), dict(img=WTIc, name="원태인", team="삼성", note="안 나오게", at=1.0)], text="4점 차로 벌어짐", textAt=3.0, size=110)
K['g6c'] = S(0, "plog", img=OLL, name="올러", team="KIA", sub="KIA 선발 · 2차전 기록", blocks=[dict(type="inn", ip=4.667, at=1.0), dict(type="runs", n=5, at=1.5)])
K['g7b'] = S(0, "people", title="6회초 · 최형우의 송구", items=[dict(img=CASK, name="카스트로", team="KIA", note="담장 맞힌 타구", at=0), dict(img=CHW2, name="최형우", team="삼성", note="2루 송구 · 아웃", at=2.0)], size=110)
K['g7'] = S(0, "people", title="6회말 · 삼성 추가점", items=[dict(img=KJC, name="김지찬", team="삼성", note="1타점 2루타", at=2.0), dict(img=PSG2, name="박승규", team="삼성", note="희생플라이", at=2.5)], text="7대1", textAt=3.0, size=110)
K['g8b'] = S(0, "rally", title="KIA · 7회초", tally=[dict(TL7[0], at=2.3)], plays=[dict(R7[0], at=0.2), dict(R7[1], res="안타 · 2아웃 1·3루", at=0.7), dict(R7[2], res="폭투 · 7대2", at=2.0)])
K['g8c'] = S(0, "rally", title="KIA · 7회초", tally=[dict(TL7[0], at=-1)], plays=[dict(R7[3], res="실책 · 다시 2아웃 1·3루", at=0.3), dict(name="이승민", img=ISMc, team="삼성", res="구원 등판", kind="def", at=2.0), dict(R7[4], at=3.0)])
K['g9'] = S(0, "people", title="다섯 번째 장면 · 7회말", items=[dict(img=CHW, name="최형우", team="삼성", note="솔로 홈런", at=1.0), dict(img=KBS, name="김범수", team="KIA", note="슬라이더", at=2.0)], text="8대2", textAt=4.0, size=110)
K['g10c'] = pv(CHW2, "최형우 · 최고령 기록", "포스트시즌", [], [st("최고령 출장 · 종전", "2017년 41살 8개월 13일", 1.0)], team="삼성")
K['r4b'] = S(0, "faces", items=[dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤", at=0, say="“최형우 선수의 호수비로\n팀 전체 분위기가 확실하게 올라갔다”", sayAt=2.0), dict(img=CHW, name="최형우", team="삼성", role="삼성 좌익수", at=1.0)])
K['r4d'] = S(0, "faces", items=[dict(img=CHW, name="최형우", team="삼성", role="삼성 좌익수 · 경기 뒤", at=-1, say="“말도 안 되게 잘 갔다\n운 좋게 잡았다”", sayAt=2.0)], chain="r4q")
K['c2'] = S(0, "tline", title="역대 5전 3선승제 플레이오프", items=[dict(d="1차전 · 2차전", t="1승 1패", at=1.0), dict(d="3차전", t="승리", at=1.4), dict(d="한국시리즈 진출", t="16번 중 9번", at=2.0, c="gold", big=True)])
K['c3a'] = S(0, "faces", items=[dict(img=WTIc, name="원태인", team="삼성", role="2차전 9회 등판", at=1.0), dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 2차전 전", at=3.0, say="“태인이가 출전한다면\n3차전은 최원태”", sayAt=4.0), dict(img=CWT2, name="최원태", team="삼성", role="3차전 선발", at=6.0)])
K['c3f'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤", at=0, say="“3차전에도\n좌익수로 나가야 한다”", sayAt=2.0), dict(img=CHW2, name="최형우", team="삼성", role="삼성 좌익수", at=-1)], chain="c3q")
K['c12c'] = tm("KIA", "KIA 불펜", "플레이오프 1·2차전", [], [st("1차전 · 선발 강판 뒤", "5명 4⅔이닝 무실점", 1.0, hi=True), st("2차전 · 6회부터", "3점 더 내줌", 5.0)])
K['c12c2'] = tm("삼성", "삼성 불펜", "플레이오프 1·2차전", [], [st("1차전 · 선발 강판 뒤", "무실점", 2.0, hi=True), st("2차전", "8회 1실점", 4.0)])
K['c13'] = tm("KIA", "3차전 관전 포인트", "10월 29일 · 광주", [], [st("관전 포인트", "세 가지", 1.0, hi=True)])
CP3 = [dict(img=SRK2, name="시라카와", team="KIA", note="초반"), dict(img=CWT2, name="최원태", team="삼성", note="KIA전 약세"), dict(img=WTIc, name="원태인", team="삼성", note="9회")]
K['c14'] = S(0, "people", title="3차전 관전 포인트", items=[dict(x, at=a) for x, a in zip(CP3, [0, 1.0, 2.0])], chain="cp3", size=110)
K['c15'] = S(0, "people", title="3차전 관전 포인트", items=[dict(x, at=-1) for x in CP3], text="3차전 흐름 좌우", textAt=1.0, chain="cp3", size=110)
K['k3c'] = pv(DIA, "디아즈", "삼성 타자", [], [st("2차전 3회", "투런 홈런", 1.0, hi=True), st("5회", "몸에 맞는 공 · 만루", 2.0)], team="삼성")
K['k8b'] = S(0, "people", title="1차전 5회 · 13구 승부", items=[dict(img=KDYb, name="김도영", team="KIA", note="13구 승부", at=0), dict(img=FED, name="페덱", team="삼성", note="그 타석 뒤 강판", at=1.0)], size=110)

# ── 10/28 2시 3라운드 X 26 반영 ──
K['g2a'] = tm("삼성", "삼성 타선", "첫 번째 장면", [], [st("3회말", "삼성 공격", 1.0, hi=True)])
K['g5'] = tm("KIA", "KIA 불펜", "두 번째 장면", [], [st("5회말", "KIA 불펜", 1.0, hi=True)])
K['g8'] = tm("KIA", "KIA 타선", "네 번째 장면", [], [st("7회초", "놓친 기회", 1.0, hi=True)])
K['g3e'] = pv(DIA, "디아즈", "삼성 타자 · 3회말", [vstamp("투런 홈런", 3.0, "gold", size=56)], [st("볼카운트", "풀카운트", 1.0), st("받아친 공", "151km 직구", 2.0, hi=True)], team="삼성")
K['g4'] = pv(OLL, "올러", "KIA 선발 · 3회말", [vstamp("2아웃 뒤 4실점", 1.0, "bad", size=52)], [st("3회말", "4대1 역전", 2.0, hi=True)])
K['g7'] = S(0, "people", title="6회말 · 삼성 추가점", items=[dict(img=KJC, name="김지찬", team="삼성", note="1타점 2루타", at=2.0), dict(img=PSG2, name="박승규", team="삼성", note="희생플라이", at=2.5)], text="7대1", textAt=3.0, size=110)
K['g11'] = S(0, "rally", title="KIA · 8회초", tally=[dict(TL8[0], at=3.0)], plays=[dict(R8[0], at=1.0), dict(R8[1], at=2.0)])
K['g11b'] = pv(WTI2, "원태인", "삼성 투수 · 9회초", [vstamp("박진만 감독 계산대로", 4.0, "gold", size=50)], [st("탈삼진", "2개", 2.0), st("2차전 9회", "1이닝 무실점", 3.0, hi=True)], team="삼성")
K['r7'] = pv(PSG2, "박승규", "이유 셋 · 삼성 외야수", [], [st("2차전", "3타수 2안타 2타점", 1.0, hi=True), st("3회", "동점 2루타", 3.0), st("5회", "내야안타 · 선발 강판", 5.0), st("6회", "희생플라이", 7.0)], team="삼성")
K['c3g'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤", at=-1), dict(img=CHW2, name="최형우", team="삼성", role="삼성 좌익수", at=-1, say="“전화 한번 드려야겠다”", sayAt=1.0)], chain="c3q")
K['c13'] = tm("KIA", "3차전 관전 포인트", "3차전 · 광주", [], [st("관전 포인트", "세 가지", 1.0, hi=True)])
K['z0a'] = S(0, "duel", title="선발 맞대결 · 올해 정규시즌", left=dict(img=SRK2, name="시라카와", team="KIA", role="삼성전 평균자책점 3.68", at=1.0), right=dict(img=CWT2, name="최원태", team="삼성", role="KIA전 평균자책점 8점대", at=2.0), vsAt=1.5)
K['z0b'] = tm("삼성", "삼성 타선", "제 생각 · 3차전 변수", [], [st("1차전", "안타 2개", 1.0), st("2차전", "8점", 1.0, hi=True)])
for _k, _a in {'g7a': 1.0, 'g11b': 1.0, 'r1': 1.0, 'r5': 1.0, 'r6': 1.0, 'k1': 1.0, 'k3b': 1.0, 'k4': 1.0, 'k7': 1.0, 'k9': 1.0, 'z0c': 2.0}.items(): K[_k]['imgAt'] = _a   # 사진·이름은 이름을 말하는 호흡에
for _k in ('g7a', 'g11b', 'r1', 'r5', 'r6', 'k1', 'k3b', 'k4', 'k7', 'k9', 'z0c'):
    _a = K[_k]['imgAt']
    for _f in ('viz', 'stats', 'blocks'):
        for _x in K[_k].get(_f, []):
            if isinstance(_x, dict) and 0 <= (_x.get('at') or 0) < _a: _x['at'] = _a   # 도장·칸이 사진보다 먼저 혼자 뜨지 않게

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
CH = [_ch("경기 전 수 싸움", "경기 전 수 싸움", "p0", "p9"), _ch("2차전 흐름", "2차전 흐름", "g0", "g12"), _ch("승부를 가른 이유", "승부를 가른 이유", "r0", "r12"), _ch("3차전 예상", "3차전 예상", "c0", "c15"), _ch("3차전 키플레이어", "3차전 키플레이어", "k0", "k9"), _ch("제 생각", "제 생각", "zt", "z1")]

TAGS = ["플레이오프", "플레이오프 2차전", "플레이오프 3차전", "KIA 삼성", "기아 삼성", "KIA 타이거즈", "삼성 라이온즈", "시라카와", "최원태", "원태인", "3차전 선발", "올러", "후라도", "최형우", "디아즈", "박승규", "카스트로", "김도영", "프로야구", "KBO", "야구자판기"]
DESC = ("삼성이 KIA를 8대3으로 꺾고 플레이오프를 1승 1패로 만들었습니다. 3회말 박승규 동점 2루타·구자욱 역전 적시타·디아즈 투런, 7회말 최형우 솔로(포스트시즌 역대 최고령 홈런 · 42살 10개월 11일). 삼성 선발 후라도 6⅔이닝 2실점, 9회 원태인 1이닝 무실점.\n\n"
        "3차전: 10월 29일(목) 오후 6시 30분 광주-기아 챔피언스 필드 · " + SPW.replace("3차전 ", "") + " KIA 시라카와(정규시즌 4승 5패·4.75, 삼성전 3.68) vs 삼성 최원태(정규시즌 KIA전 평균자책점 8점대).\n"
        "시라카와: 준PO 3차전 5이닝 1실점 9탈삼진, 아시아쿼터 첫 포스트시즌 승. 최원태(2025 가을): 준PO 6이닝 무실점 · PO 2차전 7이닝 1실점 · PO 5차전 3⅓이닝 5실점.\n"
        "KIA 광주 가을야구: 2024 한국시리즈 광주 3경기, 2026 준PO 광주 2경기 모두 승리.\n\n"
        "기록 출처: 스타뉴스·MK스포츠·서울경제·서울신문·세계일보·뉴스핌·뉴스1·마이데일리·스포츠경향·한스경제(2차전 10/27), 일간스포츠·엑스포츠뉴스·OSEN·스포티비뉴스·마이데일리·톱스타뉴스·이투데이·경북도민일보·전남일보·세계일보(2026/10), 뉴시스·뉴스1·스포츠경향·뉴스핌(2025 가을), 연합뉴스·데일리안·더팩트·OSEN(2024 한국시리즈), " + ("OSEN·스포티비뉴스(2023)" if KW else "서울신문·스포츠춘추·세계일보(2025)") + "\n"
        "사진 출처: 구단 제공")
SOURCE = "사실 출처 = 프로젝트 claude/1027-롱폼32-PO2차전리뷰-3차전예측-근거모음.md(기사 본문 2곳 이상)."
PINNED = "3차전, 먼저 2승을 가져갈 팀은 어디일까요? 👇 댓글로 남겨 주세요!\n매일 야구 이슈 받아보려면 구독 + 알림 설정 부탁드려요 ⚾"

EP = {"introChapter": "오프닝", "date": "2026-10-27", "gameDate": "2026-10-27", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.15,
      "rev": "1027-long32-v1", "topic": "PO2차전리뷰", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 9000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "삼성 반격! 최형우 가을 최고령 홈런 | 플레이오프 2차전 리뷰 · 3차전 선발 시라카와 vs 최원태 #KIA #삼성",
                  "description": DESC, "tags": TAGS, "pinned": PINNED,
                  "hashtags": ["#KIA타이거즈", "#삼성라이온즈", "#플레이오프", "#최형우", "#원태인", "#프로야구", "#KBO", "#야구자판기"]}}

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
