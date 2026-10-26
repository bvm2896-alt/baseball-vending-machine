# -*- coding: utf-8 -*-
"""10/25 롱폼㉚ 「롯데 새 감독 이동욱, 9년 가을야구 탈락 끊을까?」 콘티 v1.
대사 = tools/text_1025_long30.py (마지막 구독 줄은 CTA_LINE). 근거 = 프로젝트 claude/1025-롱폼30-롯데새감독-근거모음.md.
화면: 한 사람 구간은 한 사진·한 묶음(chain) · 9년 순위는 막대 줄(trend) · 감독 교체는 연도 축(yearline) · 팀 기록은 순위 칸(rankstrip)
 · 감독 계약 비교는 얼굴 카드(faces) · 공식 발표 전 = 화면에도 '보도'·'미정' 표기.
사진: 카드/P30_*(10/25 크롬으로 받음 — 한겨레·스포츠경향·중앙·연합(워터마크 잘라냄)), 카드/H14_류지현_한화_A·FA9_이강철_덕아웃·T12_레이예스_미소·G18P_최원준."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('\ndef sub_of')].replace("'text_1015_long15.py'", "'text_1025_long30.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
assert LINES[-1][0].startswith('채널 구독하고')
TEXT = [x[0] for x in LINES[:-1]]
import narr_1020
_NU = ['', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉']; _NT = ['', '열', '스물', '서른', '마흔', '쉰', '예순', '일흔', '여든', '아흔']
def _native(n): n = int(n); return _NT[n // 10] + _NU[n % 10] if 0 < n < 100 else None
def narr_of(t):
    t = t.replace('코로나19', '코로나 일구').replace('OPS', '오피에스').replace('MVP', '엠브이피').replace('0.732', '영 점 칠삼이').replace('4.72', '사 점 칠이').replace('미리 한 재계약', '미리한 재계약')  # 10/25 사용자: '미리/한재계약' 끊김 → '미리한/재계약'
    t = re.sub(r'(\d),(\d{3})', r'\1\2', t)
    t = re.sub(r'(?<![\d.])(\d{1,2})(경기|명)', lambda m: (_native(m.group(1)) + ' ' + m.group(2)) if _native(m.group(1)) else m.group(0), t)
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)
    n = n.replace('KT', '케이티').replace('KIA', '기아').replace('LG', '엘지').replace('SSG', '에스에스지').replace('NC', '엔씨').replace('FA', '에프에이').replace('WBC', '더블유비씨')
    n = n.replace('십일 월', '십일월').replace('십이 월', '십이월').replace('구패배', '구 패배')
    return n
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vq(date, text, at, src=True, **k): return dict(type="quote", date=date, text=text, at=at, src=src, **k)
def vtrend(items, **k): return dict(type="trend", items=items, **k)
def mini(items): return dict(type="mini", items=items)
def toc(on, **k): return S(0, "toc", on=on, **k)
C = '카드/'
KT, LD, YJ, LT = C + "P30_김태형_롯데_1024_중앙", C + "P30_이동욱_NC_2021_한겨레", C + "P30_양의지_집행검_2020_연합", C + "P30_이택근_키움_2020_스포츠경향"
RY, RJ, LK = C + "T12_레이예스_미소", C + "H14_류지현_한화_A", C + "FA9_이강철_덕아웃"
def pv(img, name, sub, viz=(), stats=(), **k):
    return S(0, "pstat", img=img, team=k.pop("team", "롯데"), name=name, sub=sub, viz=list(viz), stats=list(stats), **k)
def kt(sub, viz=(), stats=(), **k): return pv(KT, "김태형", sub, viz, stats, **k)
def ld(sub, viz=(), stats=(), **k): return pv(LD, "이동욱", sub, viz, stats, team=k.pop("team", "NC"), **k)
def lotte(sub, viz=(), stats=(), **k): return pv(None, "롯데 자이언츠", sub, viz, stats, **k)
def hide(xs): return [dict(x, at=-1) for x in xs]

SC = []
# ── 오프닝 0~8 ──
SC.append(kt("롯데 감독 · 2024 ~ 2026년", [], [st("10월 24일 발표", "재계약 안 함", 0.4, hi=True)]))                       # 0
O1 = [st("2020년 · NC", "창단 첫 통합 우승", 50, hi=True), st("공식 발표", "아직 · 최종 절차 진행 중", 50), st("계약 기간 · 금액", "미정", 50)]
SC.append(ld("전 NC 감독", [vstamp("롯데 새 감독 후보 · 보도", 1.8, "gold", size=48)], [], chain="o1", enterAt=1.6))  # 1 (이름 부르는 호흡에 사진)
SC.append(ld("전 NC 감독", [vstamp("롯데 새 감독 후보 · 보도", -1, "gold", size=48)], [dict(O1[0], at=0.6)], chain="o1"))   # 2
SC.append(ld("전 NC 감독", [vq("10월 25일 · 롯데 · 요약", "후보군은 맞다, 최종 절차 진행 중", 1.0)], [dict(O1[0], at=-1)], chain="o1"))   # 3
SC.append(ld("전 NC 감독", [], [dict(O1[0], at=-1), dict(O1[1], at=0.0), dict(O1[2], at=1.2)], chain="o1"))                  # 4
SC.append(S(0, "yearcount", team="롯데", **{"from": 2018, "to": 2026}, countAt=0.2, countEnd=1.2, stamp="9년 연속 가을야구 탈락", stampAt=1.3, sub="구단 역사상 가장 긴 기록", subAt=3.0))   # 5
SC.append(ld("롯데 새 감독 후보", [vstamp("9년 기록 끊을까?", 0.6, "gold", size=60)], [], chain="o6"))                        # 6
SC.append(toc(-1, itemSeg=[0.0, 1.0, 2.0, None, None, None]))                                                          # 7
SC.append(toc(-1, itemSeg=[None, None, None, 0.0, 1.0, 2.0], cont=True))                                              # 8
# ── 1막 · 김태형 3년 9~31 ──
SC.append(toc(0))                                                                                                     # 9
K10 = [st("2023년 10월", "3년 총액 24억 원", 1.0, hi=True), st("계약금", "6억 원", 50), st("연봉", "6억 원", 50)]
SC.append(kt("롯데 감독", [], K10, chain="k10"))                                                                       # 10
SC.append(kt("롯데 감독", [], [dict(K10[0], at=-1), dict(K10[1], at=0.0), dict(K10[2], at=0.6)], chain="k10"))            # 11
SC.append(kt("롯데 감독", [], hide(K10) + [st("두산 · 2015 ~ 2021년", "7년 연속 한국시리즈", 0.4), st("한국시리즈 우승", "3번", 3.0, hi=True)], chain="k10"))   # 12
R1 = dict(k="2024년", v="66승 4무 74패", rank=7, at=0.6); R2 = dict(k="2025년 전반기", v="47승 3무 39패", rank=3, at=0.4)
R2b = dict(k="2025년 · 후반기 12연패", v="시즌 66승 6무 72패", rank=7, **{"from": 3}, at=0.95); R3 = dict(k="2026년", v="64승 3무 77패", rank=7, at=0.4)
RT = "롯데 · 김태형 감독 3년"
SC.append(S(0, "rankstrip", team="롯데", title=RT, rows=[R1, dict(R2, at=50), dict(R3, at=50)], chain="r13"))            # 13
SC.append(S(0, "rankstrip", team="롯데", title=RT, rows=[dict(R1, at=-1), R2, dict(R3, at=50)], chain="r13"))            # 14
SC.append(S(0, "rankstrip", team="롯데", title=RT, rows=[dict(R1, at=-1), dict(R2, at=-1), dict(R3, at=50)], chain="r13"))   # 15
SC.append(S(0, "rankstrip", team="롯데", title=RT, rows=[dict(R1, at=-1), R2b, dict(R3, at=50)], chain="r13"))           # 16
SC.append(S(0, "rankstrip", team="롯데", title=RT, rows=[dict(R1, at=-1), dict(R2b, at=-1), R3], chain="r13"))           # 17
L18 = [st("3년 승패", "196승 13무 223패", 1.0), st("승률", ".468", 2.0, hi=True), st("외부 FA 영입", "0명", 50, hi=True)]
SC.append(lotte("김태형 감독 3년 · 2024 ~ 2026년", [], L18, chain="t18"))                                                 # 18
SC.append(lotte("김태형 감독 3년 · 2024 ~ 2026년", [], hide(L18[:2]) + [dict(L18[2], at=1.0)], chain="t18"))             # 19
L20 = [st("규정이닝(팀 경기 수만큼 이닝) 채운 선발", "5명 전원", 50, hi=True), st("144경기 체제 · 2015년 이후", "처음", 50)]
SC.append(lotte("2026 정규시즌 · 남긴 기록", [], L20, chain="t20"))                                                        # 20
SC.append(lotte("2026 정규시즌 · 남긴 기록", [], [dict(L20[0], at=0.6), L20[1]], chain="t20"))                             # 21
SC.append(lotte("2026 정규시즌 · 남긴 기록", [], [dict(L20[0], at=-1), dict(L20[1], at=0.6)], chain="t20"))                # 22
Y23 = [st("2026년 안타", "211개 · 신기록", 0.6, hi=True), st("안타왕", "3년 연속", 50), st("종전 기록", "202개 · 2024년 본인", 50), st("타율", ".363", 50)]
def ry(stats, viz=()): return pv(RY, "레이예스", "롯데 외야수", viz, stats, chain="y23")
SC.append(ry(Y23))                                                                                                    # 23
SC.append(ry([dict(Y23[0], at=-1), dict(Y23[1], at=0.0)] + Y23[2:]))                                                   # 24
SC.append(ry(hide(Y23[:2]) + [dict(Y23[2], at=0.5), Y23[3]]))                                                          # 25
SC.append(ry(hide(Y23[:3]) + [Y23[3]], [mini([dict(img=C + "G18P_최원준", name="최원준", team="KT", k="208안타 · 2위", at=0.3)])]))   # 26
SC.append(ry(hide(Y23[:3]) + [dict(Y23[3], at=0.2)], [mini([dict(img=C + "G18P_최원준", name="최원준", team="KT", k="208안타 · 2위", at=-1)])]))   # 27
KQ = [("10월 · 기사 요약", "3년 안에 못 했으면 감독 책임"), ("시즌을 마치며 · 요약", "약속 못 지켜 죄송")]
SC.append(kt("롯데 감독", [vq(*KQ[0], 50), vq(*KQ[1], 50)], [st("김태형 감독", "책임에 대한 말", 0.3, hi=True)], chain="q28"))                                                 # 28
SC.append(kt("롯데 감독", [vq(*KQ[0], 0.2), vq(*KQ[1], 50)], [st("김태형 감독", "책임에 대한 말", -1, hi=True)], chain="q28"))                                                # 29
SC.append(kt("롯데 감독", [vq(*KQ[0], -1), vq(*KQ[1], 1.0)], [st("김태형 감독", "책임에 대한 말", -1, hi=True)], chain="q28"))                                                # 30
SC.append(kt("롯데 감독", [vsteps([stp("10월 24일", "롯데 · 재계약 안 함", 0.6, c="bad")])], chain="q31"))                  # 31
# ── 2막 · 롯데의 9년 32~53 ──
SC.append(toc(1))                                                                                                     # 32
P33 = [stp("2017년 정규시즌", "3위", 50, c="good"), stp("준플레이오프", "NC에 2승 3패", 50, c="bad"), stp("5차전", "0대 9 패배", 50, c="bad")]
SC.append(lotte("마지막 가을야구 · 2017년", [vsteps(P33)], chain="p33"))                                                  # 33
SC.append(lotte("마지막 가을야구 · 2017년", [vsteps([dict(P33[0], at=0.2), dict(P33[1], at=1.0), P33[2]])], chain="p33"))    # 34
SC.append(lotte("마지막 가을야구 · 2017년", [vsteps([dict(P33[0], at=-1), dict(P33[1], at=-1), dict(P33[2], at=0.3)])], chain="p33"))   # 35
RK = [(2018, 7), (2019, 10), (2020, 7), (2021, 8), (2022, 8), (2023, 7), (2024, 7), (2025, 7), (2026, 7)]
TA = [2.0, 2.3, 2.6, 3.0, 3.3, 3.6, 4.0, 4.3, 4.6]
def rk(ats, hi19=False): return [dict(x=f"{y}년", v=r, vt=f"{r}위", at=a, **({"c": "bad"} if (hi19 and y == 2019) else {})) for (y, r), a in zip(RK, ats)]
SC.append(lotte("2018 ~ 2026년 순위 · 10개 구단", [vtrend(rk(TA), title="롯데 순위", invert=True)], chain="p36"))            # 36
SC.append(lotte("2018 ~ 2026년 순위 · 10개 구단", [vtrend(rk([-1] * 9, True), title="롯데 순위", invert=True)], chain="p36"))   # 37
B38 = [dict(label="2001 ~ 2007년", team="롯데", value=7, note="7년 연속 탈락", at=1.2), dict(label="2018 ~ 2026년", team="롯데", value=9, note="9년 연속 탈락", at=50, hi=True)]
SC.append(S(0, "bars", title="롯데 · 가을야구 연속 탈락", max=10, items=B38, chain="b38"))                                   # 38
SC.append(S(0, "bars", title="롯데 · 가을야구 연속 탈락", max=10, items=[dict(B38[0], at=-1), dict(B38[1], at=0.3)], chain="b38"))   # 39
YLK = dict(title="롯데 감독 · 2018 ~ 2026년", **{"from": 2017, "to": 2027}, ticks=[2018, 2020, 2022, 2024, 2026], chain="yl40", wrapLabel=True)
YI = [dict(y=2018.8, team="롯데", label="조원우 · 2018.10\n경질 · 2년 남김", c="bad"), dict(y=2019.55, team="롯데", label="양상문(전 LG 단장)\n2019.7 사퇴 · 94경기", c="bad"),
      dict(y=2019.82, team="롯데", label="허문회 · 2019.10\n3년 10억 5천만 원", c="gold"), dict(y=2021.36, team="롯데", label="허문회 · 2021.5\n경질 · 12승 18패", c="bad"),
      dict(y=2023.65, team="롯데", label="서튼 · 2023.8\n사퇴 · 건강 문제", c="bad"), dict(y=2026.81, team="롯데", label="김태형\n계약 기간 채움", c="gold")]
BR = dict(a=2018.0, b=2026.9, label="2018 ~ 2026 · 9년", at=1.0); BR7 = dict(BR, label="9년 · 감독 5명 + 감독대행 2명")
def yl(n_new, at_new, brace=None, **k):
    its = [dict(x, at=-1) for x in YI[:n_new]] + ([dict(YI[n_new], at=at_new)] if at_new is not None else [])
    return S(0, "yearline", items=its, **({"brace": brace} if brace else {}), **YLK, **k)
SC.append(yl(0, None, brace=dict(BR, at=0.6)))                                                                        # 40
SC.append(yl(0, 0.6, brace=dict(BR, at=-1)))                                                                          # 41
SC.append(yl(1, None, brace=dict(BR, at=-1)))                                                                         # 42
SC.append(yl(1, 0.6, brace=dict(BR, at=-1)))                                                                          # 43
SC.append(yl(2, None, brace=dict(BR, at=-1)))                                                                         # 44
SC.append(yl(2, None, brace=dict(BR, at=-1)))                                                                         # 45
SC.append(yl(2, 0.5, brace=dict(BR, at=-1)))                                                                          # 46 허문회 부임
SC.append(yl(3, 0.5, brace=dict(BR, at=-1)))                                                                          # 47 허문회 경질
SC.append(yl(4, None, brace=dict(BR, at=-1)))                                                                         # 48
SC.append(yl(4, 0.9, brace=dict(BR, at=-1)))                                                                          # 49
SC.append(yl(5, None, brace=dict(BR7, at=0.3)))                                                                        # 50
SC.append(yl(5, None, brace=dict(BR7, at=-1)))                                                                        # 51
SC.append(yl(5, 1.8, brace=dict(BR7, at=-1)))                                                                          # 52
SC.append(yl(6, None, brace=dict(BR7, at=-1)))                                                                         # 53
# ── 3막 · 이동욱 54~94 ──
SC.append(toc(2))                                                                                                     # 54
D55 = [stp("학교", "동래고 · 동아대", 0.8), stp("1997년", "롯데 입단 · 2차 2라운드", 2.5, c="good"), stp("1군 통산", "143경기 · 타율 .221", 50), stp("2003시즌 뒤", "부상으로 은퇴", 50, c="bad")]
def ldp(sub, viz=(), **k): return pv(LD, "이동욱", sub, viz, [], team="롯데", **k)
SC.append(ldp("선수 시절 · 롯데", [vsteps(D55)], chain="d55"))                                                  # 55
SC.append(ldp("선수 시절 · 롯데", [vsteps(hide(D55[:2]) + [dict(D55[2], at=0.6), D55[3]])], chain="d55"))   # 56
SC.append(ldp("선수 시절 · 롯데", [vsteps(hide(D55[:3]) + [dict(D55[3], at=0.5)])], chain="d55"))   # 57
D58 = [stp("2004년", "롯데 2군 수비코치", 0.5), stp("2007년", "LG 수비코치", 50), stp("2011년", "NC 창단 코치", 50, c="good"), stp("2011 ~ 2018년", "NC 코치", 50)]
SC.append(ld("코치 시절", [vsteps(D58)], chain="d58"))                                                                     # 58
SC.append(ld("코치 시절", [vsteps([dict(D58[0], at=-1), dict(D58[1], at=0.6), dict(D58[2], at=3.0), D58[3]])], chain="d58"))   # 59
SC.append(ld("코치 시절", [vsteps(hide(D58[:3]) + [dict(D58[3], at=0.3)])], chain="d58"))                                    # 60
D61 = [st("2018년 10월", "NC 두 번째 감독", 0.6, hi=True), st("전임", "김경문 감독", 50), st("계약", "2년", 50)]
SC.append(ld("NC 감독", [], D61, chain="d61"))                                                                            # 61
SC.append(ld("NC 감독", [], [dict(D61[0], at=-1), dict(D61[1], at=1.0), D61[2]], chain="d61"))                              # 62
SC.append(ld("NC 감독", [], hide(D61[:2]) + [dict(D61[2], at=0.2)], chain="d61"))                                          # 63
N64 = dict(k="2018년", v="창단 첫 꼴찌", rank=10, at=1.0); N66 = dict(k="2019년 · 이동욱 첫해", v="가을야구 진출", rank=5, **{"from": 10}, at=0.5)
N68 = dict(k="2020년", v="정규시즌 우승", rank=1, at=0.5)
NT = "NC 다이노스 순위"
SC.append(S(0, "rankstrip", team="NC", title=NT, rows=[N64, dict(N66, at=50), dict(N68, at=50)]))                       # 64
SC.append(pv(YJ, "양의지", "NC 포수 · 2018시즌 뒤 FA (사진 2020년)", [], [st("2018시즌 뒤 · FA 계약", "4년 총액 125억 원", 1.6, hi=True)], team="NC", enterAt=0.8))      # 65
SC.append(S(0, "rankstrip", team="NC", title=NT, rows=[dict(N64, at=-1), N66, dict(N68, at=50)], chain="r66", text="와일드카드 결정전 · LG에 1대 3 패", textAt=50, size=48))           # 66
SC.append(S(0, "rankstrip", team="NC", title=NT, rows=[dict(N64, at=-1), dict(N66, at=-1), dict(N68, at=50)], chain="r66", text="와일드카드 결정전 · LG에 1대 3 패", textAt=0.6, size=48))   # 67
SC.append(S(0, "rankstrip", team="NC", title=NT, rows=[dict(N64, at=-1), dict(N66, at=-1), N68], chain="r66", text="와일드카드 결정전 · LG에 1대 3 패", textAt=50, size=48))           # 68
KS = [dict(team="NC", t="NC · 이동욱", at=0.2), dict(icon="VS", t="2020 한국시리즈", at=0.6, hi=True), dict(team="두산", t="두산 · 김태형", at=1.0)]
def ks(stats=(), viz2=(), hop_at=None, **k): return pv(LD, "이동욱", "NC 감독 · 2020 한국시리즈", [dict(type="hops", items=KS if hop_at is None else [dict(x, at=hop_at) for x in KS])] + list(viz2), list(stats), team="NC", chain="h69", **k)
SC.append(ks([st("결과", "NC 4승 2패 · 통합 우승", 50, hi=True)]))                                                # 69 (결과 자리 미리)
SC.append(ks([st("결과", "NC 4승 2패 · 통합 우승", 1.2, hi=True)], hop_at=-1))                                                       # 70
SC.append(ks([st("결과", "NC 4승 2패 · 통합 우승", -1, hi=True)], [vstamp("감독 맞대결 · 이동욱 승", 0.8, "gold", size=46)], hop_at=-1))   # 71
SC.append(pv(YJ, "양의지", "NC 포수 · 2020 한국시리즈", [], [st("한국시리즈", "MVP", 1.0, hi=True)], team="NC", chain="y72", enterAt=0.8))     # 72
SC.append(pv(YJ, "양의지", "NC 포수 · 2020 한국시리즈", [vstamp("우승 세리머니 · 집행검", 2.6, "gold", size=48)], [st("한국시리즈", "MVP", -1, hi=True)], team="NC", chain="y72"))   # 73
D74 = [st("2021년 5월 · 재계약", "3년 총액 21억 원", 1.2, hi=True), st("재계약 시점", "시즌 도중", 50), st("계약금 · 연봉", "6억 원 · 5억 원", 50)]
SC.append(ld("NC 감독", [], D74, chain="d74"))                                                                            # 74
SC.append(ld("NC 감독", [], [dict(D74[0], at=-1), dict(D74[1], at=0.3), D74[2]], chain="d74"))                              # 75
SC.append(ld("NC 감독", [], hide(D74[:2]) + [dict(D74[2], at=0.3)], chain="d74"))                                          # 76
DQ = [("2018년 10월 · 취임 · 요약", "지지 않는 야구를 하고 싶다"), ("스타일 · 기사 요약", "데이터·영상으로 선수 설득")]
SC.append(ld("NC 감독", [vstamp("데이터 야구", 1.2, "gold", size=56)], chain="d77"))                                        # 77
SC.append(ld("NC 감독", [vq(*DQ[0], 1.0), vq(*DQ[1], 50)], chain="d78"))                                                   # 78
SC.append(ld("NC 감독", [vq(*DQ[0], -1), vq(*DQ[1], 1.0)], chain="d78"))                                                   # 79
N80 = [stp("2021년 7월", "방역수칙 위반 술자리", 2.0, c="bad"), stp("선수", "일부 코로나19 확진", 50, c="bad"), stp("NC · 두산 확진자", "KBO 리그 중단", 50, c="bad")]
SC.append(pv(None, "NC 다이노스", "2021년 7월", [vsteps(N80)], team="NC", chain="n80"))                                      # 80
SC.append(pv(None, "NC 다이노스", "2021년 7월", [vsteps([dict(N80[0], at=-1), dict(N80[1], at=0.3), N80[2]])], team="NC", chain="n80"))   # 81
SC.append(pv(None, "NC 다이노스", "2021년 7월", [vsteps(hide(N80[:2]) + [dict(N80[2], at=0.3)])], team="NC", chain="n80"))   # 82
N83 = [st("선수 4명", "72경기 출장정지", 0.6, hi=True), st("이동욱 감독 · 구단 자체 징계", "10경기 출장정지", 2.6, hi=True), st("구단", "제재금 1억 원", 50), st("2021시즌", "7위", 50)]
SC.append(ld("2021년 · 징계", [], N83, chain="n83"))                                                                       # 83
SC.append(ld("2021년 · 징계", [], hide(N83[:2]) + [dict(N83[2], at=0.6), N83[3]], chain="n83"))                              # 84
SC.append(ld("2021년 · 징계", [], hide(N83[:3]) + [dict(N83[3], at=0.3)], chain="n83"))                                      # 85
SC.append(ld("NC 감독", [vsteps([stp("2022년 5월", "최하위 · 계약 해지", 1.0, c="bad")])], chain="d86"))                      # 86
SC.append(ld("NC 감독", [vsteps([stp("2022년 5월", "최하위 · 계약 해지", -1, c="bad")]), vq("NC 대표 · 요약", "우발적 결정 아니다, 기강 해이", 0.5)], chain="d86"))   # 87
D88 = [stp("2023년 2월 ~", "샌디에이고 산하 연수 · 약 6개월", 1.0), stp("2025년", "KBO 전력강화위원", 50), stp("2026년 · WBC", "대표팀 수비코치", 50, c="good"), stp("2026년 · 아시안게임", "대표팀 수비코치", 50, c="good")]
SC.append(ld("NC 감독 이후", [vsteps(D88)], team="KBO", chain="d88"))                                                      # 88
SC.append(ld("NC 감독 이후", [vsteps([dict(D88[0], at=-1)] + D88[1:])], team="KBO", chain="d88"))                           # 89
SC.append(ld("NC 감독 이후", [vsteps(hide(D88[:1]) + [dict(D88[1], at=0.2)] + D88[2:])], team="KBO", chain="d88"))          # 90
SC.append(ld("NC 감독 이후", [vsteps(hide(D88[:2]) + [dict(D88[2], at=0.6), dict(D88[3], at=1.0)])], team="KBO", chain="d88"))   # 91
SC.append(pv(RJ, "류지현", "2026 WBC 대표팀 감독", [], [st("2026년 10월", "한화 감독 선임", 1.6, hi=True)], team="한화", enterAt=1.2))                    # 92
SC.append(ld("2026 아시안게임 · 대표팀 수비코치", [vstamp("금메달 · 아시안게임 5연패", 1.2, "gold", size=48)], team="KBO"))       # 93
SC.append(ld("롯데로 돌아올까", [vsteps([stp("1997년", "롯데 입단", 0.4, c="good"), stp("2026년 10월", "롯데 새 감독 후보 · 보도", 1.4, c="gold")])], team="롯데"))   # 94
# ── 4막 · 새 단장 후보 95~107 ──
SC.append(toc(3))                                                                                                     # 95
SC.append(pv(C + "P30_박준혁_단장_2023_OSEN", "박준혁", "롯데 단장", [], [st("계약", "11월 만료", 0.6, hi=True)], focus="50% 12%"))   # 10/25 밤 사용자 "박준혁 단장 사진으로"                                            # 96
def tk(sub, viz=(), stats=(), **k): return pv(LT, "이택근", sub, viz, stats, team="키움", **k)
SC.append(tk("해설위원 · 전 키움 선수", [vstamp("10월 25일 · 롯데 새 단장 후보 보도", 1.0, "gold", size=46)], chain="t97"))              # 97
SC.append(tk("해설위원 · 전 키움 선수", [vstamp("10월 25일 · 롯데 새 단장 후보 보도", -1, "gold", size=46), vq("10월 25일 · 롯데 · 요약", "면접은 사실, 결정된 건 없다", 1.0)], chain="t97"))   # 98
T99 = [stp("1999년", "현대 · 2차 3라운드", 0.8, c="good"), stp("2010년", "LG 이적", 50), stp("2011시즌 뒤", "FA로 히어로즈 복귀", 50, c="good")]
SC.append(tk("선수 시절", [vsteps(T99)], chain="t99"))                                                                     # 99
SC.append(tk("선수 시절", [vsteps([dict(T99[0], at=-1), dict(T99[1], at=0.2), dict(T99[2], at=1.5)])], chain="t99"))           # 100
T101 = [st("통산", "1621안타 · 136홈런", 0.3), st("타율", ".302", 2.0, hi=True), st("은퇴", "2020시즌", 50), st("은퇴 뒤", "해설위원", 50)]
SC.append(tk("선수 시절 · 통산 기록", [], T101, chain="t101"))                                                             # 101
SC.append(tk("선수 시절 · 통산 기록", [], hide(T101[:2]) + [dict(T101[2], at=0.3), T101[3]], chain="t101"))                  # 102
SC.append(tk("선수 시절 · 통산 기록", [], hide(T101[:3]) + [dict(T101[3], at=0.1)], chain="t101"))                            # 103
T104 = [st("출신", "부산", 0.2), st("선수 시절 롯데", "인연 없음", 2.0, hi=True), st("지도자 경력", "없음", 50), st("단장 선임", "아직 미정", 50, hi=True)]
SC.append(tk("단장 후보", [], T104, chain="t104"))                                                                         # 104
SC.append(tk("단장 후보", [], hide(T104[:2]) + [dict(T104[2], at=0.3), T104[3]], chain="t104"))                              # 105
SC.append(tk("단장 후보", [], hide(T104[:3]) + [dict(T104[3], at=0.6)], chain="t104"))                                      # 106
SC.append(lotte("이번 겨울", [vsteps([stp("감독", "김태형 → 미정", 0.4, c="bad"), stp("단장", "박준혁 → 미정", 1.0, c="bad")])]))   # 107
# ── 5막 · 2027년 숙제 108~123 ──
SC.append(toc(4))                                                                                                     # 108
TB = [dict(k="팀 타율", v=".272", rank=4, at=0.0), dict(k="팀 홈런", v="113개", rank=10, at=0.5), dict(k="득점", v="679점", rank=9, at=0.5)]
TT = "롯데 · 2026 팀 타격"
def tb(n, at_new=None): return S(0, "rankstrip", team="롯데", title=TT, rows=[dict(x, at=-1) for x in TB[:n]] + ([dict(TB[n], at=at_new if at_new is not None else TB[n]['at'])] if n < len(TB) else []) + [dict(x, at=50) for x in TB[n + 1:]], chain="tb109", text="타율 4위 · 득점 9위 · 홈런 꼴찌", textAt=50, size=48)
SC.append(tb(0))                                                                                                      # 109
SC.append(tb(1))                                                                                                      # 110
SC.append(tb(2))                                                                                                      # 111
SC.append(S(0, "rankstrip", team="롯데", title=TT, rows=[dict(x, at=-1) for x in TB], chain="tb109", text="타율 4위 · 득점 9위 · 홈런 꼴찌", textAt=0.6, size=48))   # 112
SC.append(S(0, "rankstrip", team="롯데", title=TT, rows=[dict(x, at=-1) for x in TB], chain="tb109", text="타율 4위 · 득점 9위 · 홈런 꼴찌", textAt=-1, size=48))   # 113
SC.append(S(0, "rankstrip", team="롯데", title="롯데 · 2026 팀 투수", rows=[dict(k="팀 평균자책점", v="4.72", rank=5, at=0.6)]))   # 114
EI = [dict(x="2024년", v=123, vt="123개", at=1.0), dict(x="2025년", v=111, vt="111개", at=2.0), dict(x="2026년", v=107, vt="107개", at=0.2)]
SC.append(lotte("팀 실책", [vtrend(EI, title="롯데 팀 실책")], chain="e115"))                  # 115
SC.append(lotte("팀 실책", [vtrend([dict(EI[0], at=-1), dict(EI[1], at=-1), dict(EI[2], at=-1)], title="롯데 팀 실책"), vstamp("수비 · 여전히 약점", 1.0, "bad", size=48)], chain="e115"))   # 116
SC.append(ld("수비 전문가", [], [st("NC 창단 때부터", "수비코치", 1.6, hi=True)]))                                            # 117
SC.append(lotte("10월 7일", [], [st("재계약 불가", "16명", 1.0, hi=True)]))                                                  # 118
SC.append(S(0, "question", text="롯데 방출 16명 이야기는\n오른쪽 위 카드에서", img="상황별/썸네일_롱폼24_롯데방출", ph=495, arrow="ur", size=72))   # 119
C120 = [stp("11월 4일", "일본 미야자키 · 마무리 캠프 시작", 1.0, c="good"), stp("11월 24일", "캠프 끝", 50)]
SC.append(lotte("새 감독의 첫 일정", [vsteps(C120)], chain="c120"))                                                          # 120
SC.append(lotte("새 감독의 첫 일정", [vsteps([dict(C120[0], at=-1), dict(C120[1], at=0.6)])], chain="c120"))                  # 121
S122 = [stp("10월 13일", "한화 · 새 감독 선임", 50, c="good"), stp("10월 24일", "롯데 · 김태형 감독과 결별", 0.4, c="bad"), stp("10월 25일", "롯데 · 새 감독 발표 아직", 1.2, c="bad")]
SC.append(lotte("감독 선임 · 2026년 10월", [vsteps(S122)], chain="s122"))                                     # 122
SC.append(lotte("감독 선임 · 2026년 10월", [vsteps([dict(S122[0], at=0.6), dict(S122[1], at=-1), dict(S122[2], at=-1)]), vstamp("늦다는 지적", 1.6, "bad", size=48)], chain="s122"))   # 123
SC.append(lotte("2027년 숙제 · 정리", [vsteps([stp("타선", "장타 부족 · 홈런 꼴찌", 0.0, c="bad"), stp("수비", "실책 107개 · 약점", 0.5, c="bad"), stp("감독 · 단장", "선임 발표 전", 1.2, c="bad")])]))   # 124 (5막 결론)
# ── 6막 · 끊을 수 있을까 125~142 ──
SC.append(toc(5))                                                                                                     # 124
FC = [dict(img=RJ, name="류지현", team="한화", role="3년", note="20억"), dict(img=LK, name="이강철", team="KT", role="3년", note="34억"),
      dict(img=LD, name="이동욱", team="롯데", role="계약", note="발표 전"), dict(img=KT, name="김태형", team="롯데", role="3년", note="24억")]
FT = "감독 계약 총액 비교"
def fc(ats): return S(0, "faces", title=FT, items=[dict(x, at=a, noteAt=(a + 0.3 if a not in (-1, 50) else a)) for x, a in zip(FC, ats)], chain="fc125")
SC.append(S(0, "faces", title=FT, items=[dict(FC[0], at=0.6, noteAt=50), dict(FC[1], at=1.0, noteAt=50), dict(FC[2], at=50, noteAt=50), dict(FC[3], at=50, noteAt=50)], chain="fc125"))   # 125
SC.append(S(0, "faces", title=FT, items=[dict(FC[0], at=-1, noteAt=0.8), dict(FC[1], at=-1, noteAt=50), dict(FC[2], at=50, noteAt=50), dict(FC[3], at=50, noteAt=50)], chain="fc125"))   # 126
SC.append(S(0, "duel", title="2026 WBC 대표팀", left=dict(img=RJ, name="류지현", team="", at=0.1), right=dict(img=LD, name="이동욱", team="", at=0.4), vsAt=3.4, pw=300,
            badge=dict(t="감독 · 수비코치 → 한화 vs 롯데?", at=0.8)))                                                          # 127
K128 = [st("2026년 10월 · 재계약", "3년 총액 34억 원", 0.6, hi=True), st("감독 계약", "역대 최고 대우", 2.2, hi=True), st("계약금 · 연봉", "10억 원 · 8억 원", 50)]
SC.append(pv(LK, "이강철", "KT 감독", [], K128, team="KT", chain="k128"))                                  # 128
SC.append(pv(LK, "이강철", "KT 감독", [], hide(K128[:2]) + [dict(K128[2], at=0.3)], team="KT", chain="k128"))   # 129
SC.append(fc([-1, -1, 0.2, 50]))                                                                                      # 130
SC.append(fc([-1, -1, -1, 50]))                                                                                       # 131
SC.append(fc([-1, -1, -1, 0.6]))                                                                                      # 132
D133 = [st("2018년 · 부임 전", "NC 10위", 0.2), st("2019년 · 첫해", "5위 · 가을야구", 0.6, hi=True), st("롯데", "선수·코치 시작한 팀", 50), st("롯데의 약점 · 수비", "이동욱 전문 분야", 50, hi=True)]
SC.append(ld("NC 첫해에서 찾는 힌트", [], [dict(x, at=50) for x in D133], chain="d133"))                                                # 133
SC.append(ld("NC 첫해에서 찾는 힌트", [], D133[:2] + [dict(x, at=50) for x in D133[2:]], chain="d133"))                                  # 134
SC.append(ld("NC 첫해에서 찾는 힌트", [], hide(D133[:2]) + [dict(D133[2], at=1.0), dict(D133[3], at=50)], chain="d133"))                  # 135
SC.append(ld("NC 첫해에서 찾는 힌트", [], hide(D133[:3]) + [dict(D133[3], at=0.0)], chain="d133"))                                      # 136
V137 = [st("팀 홈런", "113개 · 최하위", 0.6), st("외부 FA 영입", "3년 동안 0명", 2.4, hi=True), st("참고 · NC 우승 전 · 2018년 겨울", "양의지 FA 125억 원", 50)]
SC.append(lotte("2027 변수", [], V137, chain="v137"))                                                                     # 137
SC.append(lotte("2027 변수", [], hide(V137[:2]) + [dict(V137[2], at=0.8)], chain="v137"))                                  # 138
SC.append(lotte("2027 변수", [vstamp("구단 지원도 필요", 2.0, "gold", size=50)], hide(V137), chain="v137"))                   # 139
SC.append(lotte("9년 기록을 끊으려면", [], [st("2027년", "5위 안 · 가을야구", 1.4, hi=True)]))                                 # 140
SC.append(ld("롯데 새 감독 후보 · 공식 발표 전", [vstamp("9년 기록 끊을까?", 0.4, "gold", size=60)], team="롯데"))                 # 141

N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
FAST = {1, 7, 8}
SLOW = {5, 18, 36, 39, 51, 70, 132, 141}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    if j > 0 and sc.get('chain') and SC[j - 1].get('chain') == sc['chain']: sc['cont'] = True
    l = L(narr_of(t), sub_of(t))
    if j in FAST: l['ttsTempo'] = 1.4
    if j in SLOW: l['pace'] = 'slow'
    lines.append(l); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "김태형 3년", "title": "김태형 감독의 3년", "from": 9, "to": 31},
      {"key": "롯데의 9년", "title": "롯데의 9년", "from": 32, "to": 53},
      {"key": "이동욱", "title": "이동욱은 누구인가", "from": 54, "to": 94},
      {"key": "새 단장 후보", "title": "새 단장 후보 · 이택근", "from": 95, "to": 107},
      {"key": "2027 숙제", "title": "2027년 숙제", "from": 108, "to": 124},
      {"key": "끊을 수 있을까", "title": "9년 기록을 끊을 수 있을까", "from": 125, "to": N - 1}]

TAGS = ["롯데 새 감독", "이동욱", "이동욱 감독", "롯데 감독", "롯데 자이언츠", "김태형", "김태형 결별", "이택근", "롯데 단장", "롯데 가을야구",
        "9년 연속 가을야구 탈락", "레이예스", "NC 다이노스", "2020 한국시리즈", "류지현", "이강철", "프로야구", "KBO", "야구자판기"]
DESC = ("▶ 지난 영상: 다음 메이저리거 언제 가? | 원태인·노시환은 이번 겨울, 곽빈·김주원은 1년 뒤\n\n"
        "롯데가 10월 24일 김태형 감독과 재계약하지 않기로 했고, 다음 날 새 감독 후보로 이동욱 전 NC 감독이 보도됐어요. "
        "롯데는 이동욱 전 감독이 후보군에 있는 것은 맞고, 최종 감독 선임 절차가 진행 중이라고 밝혔어요. 이 영상은 공식 발표 전(10월 25일 기준) 보도를 바탕으로 했고, 최종 결과와 계약 조건은 달라질 수 있어요.\n\n"
        "김태형 감독 3년(2024~2026): 3년 총액 24억 원, 3년 연속 7위, 196승 13무 223패(승률 .468), 외부 FA 영입 0명. 2026년 선발 5명 전원 규정이닝(144경기 체제 이후 처음), 레이예스 211안타 신기록.\n"
        "롯데의 9년: 마지막 가을야구 2017년 준플레이오프(NC에 2승 3패), 2018~2026 순위 7·10·7·8·8·7·7·7·7, 구단 최장 9년 연속 탈락(이전 7년). 이 9년 동안 계약 기간을 끝까지 채운 감독은 김태형 감독뿐(감독 5명·감독대행 2명).\n"
        "이동욱: 1997년 롯데 입단(2차 2라운드), 2004년 롯데 2군 수비코치로 지도자 시작, LG 수비코치, 2011년 NC 창단 코치, 2018년 10월 NC 감독. "
        "2019년 5위, 2020년 정규시즌 1위·한국시리즈에서 두산(김태형 감독)을 4승 2패로 꺾고 창단 첫 통합 우승, 2021년 5월 3년 21억 원 재계약, 2021년 방역수칙 위반 사태(구단 자체 징계 10경기 출장정지), 2022년 5월 계약 해지. 2026 WBC·아시안게임 대표팀 수비코치.\n"
        "새 단장 후보: 이택근 해설위원(롯데 '면접을 본 것은 사실, 결정된 사안은 없다').\n"
        "2027년 숙제: 팀 타율 4위(.272)인데 홈런 최하위(113개)·득점 9위, 실책 107개.\n썸네일의 이동욱 감독 롯데 옷차림은 AI로 합성한 이미지예요(공식 사진 아님).\n\n"
        "여러분은 이동욱 감독이 롯데의 9년 가을야구 탈락을 끊을 수 있다고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록 출처: 머니투데이(2026/10/7·10/23·10/24)·서울신문(2026/10/25)·뉴시스(2026/10/24, 2021/7/12, 2019/10/3)·STN(2026/10/24)·뉴스핌(2026/10/25)·스포츠경향(2026/10/7·10/15·10/18·10/25, 2020/11/24·11/26·12/10, 2019/10/27)·SPOTV(2026/9/17·10/25)·마이데일리(2026/10/23)·엑스포츠뉴스(2026/10/18·10/19, 2021/11/1)·OSEN(2026/10/11·10/13·10/17, 2024/3/7, 2023/10/11·10/21, 2023/8/30, 2022/5/11, 2021/7/26·9/1, 2020/11/24, 2018/10/25·11/26, 2017/10/15)·일간스포츠(2026/8/25·10/12·10/19, 2025/1/24, 2023/8/29)·톱스타뉴스(2026/10/14)·부산일보(2026/10/13)·MHN(2026/10/15)·파이낸셜뉴스(2026/10/12)·재경일보(2026/10/17·10/25)·뉴스1(2026/10/25)·더게이트·YTN(2026/10/13)·아이뉴스24(2021/5/4)·경향신문(2021/5/4)·노컷뉴스(2022/5/11, 2020/11)·더팩트(2020/11/25, 2021/7/16)·주간경향(2020/12/18)·데일리안(2022/11/9, 2021/7, 2020/11/17, 2019)·아주경제(2018/10/19)·한국일보(2018/10/19)·SBS(2021/5/11)·경북매일(2017/10/16)·뉴스서울·시대(2025/3/21)\n"
        "사진 출처: 한겨레·스포츠경향·중앙일보·연합뉴스·OSEN(사진 기사), 구단 제공·공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1025-롱폼30-롯데새감독-근거모음.md(기사 본문 2곳 이상)."
PINNED = ("이동욱 감독은 롯데의 9년 가을야구 탈락을 끊을 수 있을까요? 👇 댓글로 남겨 주세요!\n"
          "매일 야구 이슈 받아보려면 구독 + 알림 설정 부탁드려요 ⚾")

EP = {"introChapter": "오프닝", "date": "2026-10-25", "gameDate": "2026-10-25", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.15,
      "rev": "1025-long30-v2", "topic": "롯데새감독", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 9000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼30_롯데새감독.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "롯데 새 감독 이동욱, 9년 가을야구 탈락 끊을까? | 김태형 결별·이택근 단장설·2027 숙제 #롯데 #이동욱",
                  "description": DESC, "tags": TAGS, "pinned": PINNED,
                  "hashtags": ["#롯데", "#롯데자이언츠", "#이동욱", "#김태형", "#이택근", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {27: 0.4, 63: 0.4, 77: 0.4, 103: 0.45, 0: 0.35, 4: 0.35, 6: 0.4, 8: 0.5, 9: 0.3, 31: 0.5, 32: 0.3, 53: 0.5, 54: 0.3, 94: 0.5, 95: 0.3, 107: 0.5, 108: 0.3, 124: 0.5, 125: 0.3}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-25_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
