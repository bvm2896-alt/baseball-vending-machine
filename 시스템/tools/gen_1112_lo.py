# -*- coding: utf-8 -*-
"""11/12 롱폼 「MLB 직장폐쇄 — 노시환 마감은 7시간 전, 김하성·KBO 외국인 영입까지」 콘티.
대사 = lo_text.py(LINES). 근거 = 프로젝트 claude/MLB직장폐쇄-근거-1112.md
실행: python -X utf8 tools/gen_1112_lo.py → episodes/2026-11-12_롱폼.json"""
import json, os, re, sys, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from helpers_1113 import *
from gen_rank_0923 import END, OUT
from lo_text import LINES, CHAPS
from ref_narr import narr_of

FIX = [('FA', '에프에이'), ('KBO', '케이비오'), ('MVP', '엠브이피'), ('MLB', '엠엘비'), ('%', ' 퍼센트'), ('LG', '엘지'), ('km', '킬로'), ('그 뒤 ', '그뒤 '), ('뒤에서 볼 /', '뒤에서 볼.. /')]   # 11/13 02:49 "뒤에서볼 / KBO외국인 이렇게 텀 두라니까" — 슬래시만으론 타입캐스트가 '볼'을 뒤에 붙여 읽음 → '..'로 확실히 쉼   # 11/13 사용자: '그 / 뒤'로 끊어 읽지 않게 붙여 넣는다(화면 자막은 '그 뒤' 그대로)
def NARR(sub):
    n = sub
    for a, b in FIX: n = n.replace(a, b)
    n = narr_of(n)
    n = re.sub(r'([일이삼사오육칠팔구십]+) 월 ([일이삼사오육칠팔구십]+) 일', r'\1월 \2일', n)
    n = re.sub(r'(?<![가-힣])((?:[이삼]?십)?[일이삼사오육칠팔구]?|[이삼]?십) 일(?=까지|에|부터|엔|에도| )', lambda m: m.group(1) + '일' if m.group(1) else m.group(0), n)
    NAT = {'일': '한', '이': '두', '삼': '세', '사': '네', '오': '다섯', '육': '여섯', '칠': '일곱', '팔': '여덟', '구': '아홉', '십': '열', '십일': '열한', '십이': '열두'}
    n = re.sub(r'(?<![가-힣])(십이|십일|십|[일이삼사오육칠팔구])시(?=간|부터|까지|엔|예요|보다|를|에|이|가|는|$| )', lambda m: NAT[m.group(1)] + ' 시', n)
    n = re.sub(r'(?<![가-힣])(십이|십일|십|[일이삼사오육칠팔구]) 월', r'\1월', n)
    n = n.replace('삼십사쪽', '삼십사 쪽').replace('팔일 뒤', '팔 일 뒤').replace('삼진으로', ' 삼진으로').replace('삼 루수', '삼루수').replace('삼 루 ', '삼루 ').replace('삼 루를', '삼루를').replace('삼 루가', '삼루가').replace('삼주', '삼 주')
    n = n.replace(' 퍼센트', '퍼센트').replace('  ', ' ')
    n = re.sub(r'년 약 ', '년, 약 ', n)   # 11/13 00:56 사용자 "1년약 / 2315만 → 1년 / 약 2315만 달러로 텀"
    # 11/13 사용자("이십육명=스물여섯명"): 사람 수는 고유어로 — 이십육 명 → 스물여섯 명, 사십 명 → 마흔 명
    _T = {'': '', '십': '열', '이십': '스물', '삼십': '서른', '사십': '마흔', '오십': '쉰', '육십': '예순', '칠십': '일흔', '팔십': '여든', '구십': '아흔'}
    _U = {'': '', '일': '한', '이': '두', '삼': '세', '사': '네', '오': '다섯', '육': '여섯', '칠': '일곱', '팔': '여덟', '구': '아홉'}
    def _cnt(m):
        t, u = m.group(1) or '', m.group(2) or ''
        w = ('스무' if t == '이십' and not u else _T[t] + _U[u])
        return w + ' ' + m.group(3)
    # 11/13 02:50 사용자 "삼십사쪽=서른네쪽" → 쪽도 고유어
    n = re.sub(r'(?<![가-힣])((?:[이삼사오육칠팔구])?십)?([일이삼사오육칠팔구])? (명|쪽)', lambda m: _cnt(m) if (m.group(1) or m.group(2)) else m.group(0), n)
    return n
KEYS = [k for k, _ in LINES]
ALL10 = ["KIA", "KT", "LG", "NC", "SSG", "두산", "롯데", "삼성", "키움", "한화"]
P.update({"노시환": "카드/P29w_노시환_0512", "노시환2": "카드/P29w_노시환_0512", "와이스2": "카드/FA9_와이스_한화_c", "김하성": "카드/P29w_김하성_SD", "류지현": "경기/류지현_취임_한화_사용자제공",
          "염경엽": "경기/염경엽_덕아웃_1014_LG제공", "차명석": "인물/차명석_스포츠서울", "와이스": "경기/와이스_모자_0423_한화제공",
          "벡": "경기/벡_계약_1105_LG제공", "왓슨": "경기/왓슨_계약_1111_한화제공_c"})
def PSt(img, name, team, sub, viz, **k): sc = PS(img, name, sub, viz, team=team, **k); sc['bg'] = TBG(team) if team else BG_NEU; return sc
def SPt(img, name, team, bubbles, **k): sc = SP(img, name, bubbles, **k); sc['bg'] = TBG(team) if team else BG_NEU; sc['team'] = team; return sc
def BN(who, vals, team="", **k): return BAND(who, vals, team=team, **k)
def TLn(title, items, **k): return S(0, "tline", title=title, items=items, noCenter=True, **k)
def I(d, t, at, c=None, **x): return dict(dict(d=d, t=t, at=at), **({"c": c} if c else {}), **x)
def CLK(title, marks, gap=None, **k): return dict(dict(type="lo_clock", title=title, marks=marks, noCenter=True), **({"gap": gap} if gap else {}), **k)
def MK(h, sub, lab, at, c="gold"): return dict(h=h, sub=sub, lab=lab, at=at, c=c)
def ROS(title, sub, **k): return dict(type="lo_roster", title=title, sub=sub, noCenter=True, **k)
def FQn(name, role, date, text, img=None, team=None, mono=None, **k): return S(0, "fa_quote", name=name, role=role, team=team, date=date, text=text, img=img, mono=mono, at=0.6, noCenter=True, **k)
def QQ(text, logos=ALL10, **k): return Q(text, list(logos), **k)
CDI = [("12월 2일 아침 7시", "노시환\n협상 마감"), ("12월 2일 오후 2시", "노사협약\n만료"), ("2월 1일", "KBO\n캠프 시작"), ("3월 중순", "MLB 개막\n마지노선")]
def CD(title, hl=(), at=-1, ats=None, **k):
    k.setdefault("uni", True)
    its = []
    for n, (d, t) in enumerate(CDI):
        x = I(d, t, (ats[n] if ats else at), "gold" if n in hl else None)
        if n in hl: x['hl'] = 0.4
        its.append(x)
    return TLn(title, its, **k)
# 11/12 23:49 사용자 "이 장면 달력으로 보여주면 좋을 것 같아" → 마감 순서판(CD)을 달력 3장(lo_cal)으로
CALM = [dict(lab="12월", sub="2026", first=2, days=31), dict(lab="2월", sub="2027", first=1, days=28), dict(lab="3월", sub="2027", first=1, days=31)]
CALI = [dict(m=0, d=2, time="아침 7시", t="노시환 협상 마감"), dict(m=0, d=2, time="오후 2시", t="노사협약 만료"), dict(m=1, d=1, time="", t="KBO 캠프 시작"), dict(m=2, d=[10, 15], time="", t="MLB 개막 마지노선")]
def CD(title, hl=(), at=-1, ats=None, **k):
    k.pop("uni", None)
    its = [dict(CALI[n], at=(ats[n] if ats else at), hl=(n in hl)) for n in range(4)]
    return S(0, "lo_cal", title=title, months=CALM, items=its, noCenter=True, **k)
SC = {}
# 11/12 02:30 영상 검수 1차(내용 A·B·C + 규칙) 반영판: 말하는 호흡에 그 값, 첫 호흡에도 그 호흡의 값, 이름 부르면 사진, 글만 있는 띠 → 흐름 그림(steps)·연표·막대·시계
P.update({"김혜성": "카드/P29c_김혜성_다저스", "송성문": "카드/P29c_송성문_SD", "페라자": "카드/FA9_페라자", "스즈키": "카드/P29w_스즈키_컵스", "사토": "일본대표/사토"})
# 11/13 02:31 사용자가 준 새 사진(몸까지 나오는 경기 사진·지금 소속)
P.update({"김하성": "카드/P31_김하성_애틀랜타", "사토": "카드/P31_사토_한신", "벡": "카드/P31_벡_SF", "김혜성": "카드/P31_김혜성_반지", "노시환3": "카드/P31_노시환_하이파이브", "노시환4": "카드/P31_노시환_덕아웃"})
WRAP.update({'선수노조 브루스 마이어 위원장 대행은': '선수노조\n브루스 마이어 위원장 대행은', '메이저리그가 직장폐쇄에 들어갈 수 있어요': '메이저리그가\n직장폐쇄에 들어갈 수 있어요',
             '김하성은 오후 2시 전에 계약하지 못하면': '김하성은 오후 2시 전에\n계약하지 못하면', '새 타자로 40인 로스터 선수를 노린다면': '새 타자로\n40인 로스터 선수를 노린다면',
             '소속 선수를 못 데려온다던 구단 단장은': '소속 선수를 못 데려온다던\n구단 단장은', '그 뒤 시애틀이 40인 로스터에서 빼면서': '그 뒤 시애틀이\n40인 로스터에서 빼면서',
             '한화 팬들 사이에선 노시환이 빠지면': '한화 팬들 사이에선\n노시환이 빠지면', '새 외국인 계약을 마친 건': '새 외국인 계약을\n마친 건'})
def FIG(*items, at=0): return dict(type="steps", at=at, items=[dict(dict(lab=l, at=a), **x) for l, a, x in items])
def it(lab, at, **x): return (lab, at, x)
def BF(who, items, vals=(), team="", fat=0, **k): return BN(who, list(vals), team=team, fig=FIG(*items, at=fat), **k)
def STPS(*xs): return [VSTEPS([STP(d, t, a, c=c) for d, t, a, c in xs])]
# ── 오프닝
SC['o1'] = CLK("한국 시간 · 12월 2일", [MK(7, "오전 7시", "노시환 협상 마감", 50), MK(14, "오후 2시 무렵", "MLB 노사협약 만료", 0.6, "bad")], chain="clk1")
SC['o2'] = KEEP(SC['o1'], note=dict(h=14, t="미국 동부 시간으로는 12월 1일 밤", at=0.2))   # 11/12 23:50 같은 장면 제목을 바꾸지 않음 — 덧붙는 설명은 눈금 아래 작은 줄
SC['o3'] = KEEP(SC['o2']); SC['o3']['marks'][0]['at'] = 1
SC['o4'] = DUOT("12월 2일 · 한국 야구의 마감", [DCT("노시환", "노시환", "한화", 0, [dict(k="아침 7시", v="포스팅 협상 마감", at=0.2, hi=True)]), DCT("김하성", "김하성", "", 1, [dict(k="오후 2시", v="FA 시장", at=1, hi=True)])])
SC['o4b'] = CLK("한국 시간 · 12월 2일 오후 2시", [MK(7, "오전 7시", "노시환 협상 마감", 0), MK(14, "오후 2시 무렵", "KBO 외국인 영입 창구", 0.2, "bad")])
SC['o5'] = CD("마감 시간 순서", ats=[-1, -1, 1, 1.4], chain="cd0")
# ── 직장폐쇄가 뭐길래
SC['l1'] = BF("노사협약", [it("구단주", 0.2), it("선수노조", 0.5, join="+"), it("리그 운영 규칙", 1, join="=", hi=True, w=420)])
SC['l2'] = BF("노사협약이 끝나면", [it("노사협약 만료", 0.2, w=300), it("새 협약 없음", 0.6, w=270), it("구단주 문 닫음", 1, hi=True, w=300)], chain="lk")
SC['l3'] = KEEP(SC['l2']); SC['l3']['fig']['items'][2]['hi'] = False; SC['l3']['fig']['items'].append(dict(lab="직장폐쇄", at=0.2, join="=", hi=True, w=250))
SC['l3b'] = BN("직장폐쇄와 파업", [V("파업", "선수 쪽", 0.2, size=120), V("직장폐쇄", "구단주 쪽", 1, hi=True, size=120)])
SC['l3c'] = TLn("1994년 · 선수 파업", [I("8월 12일", "선수 파업 시작", 0.2, "bad"), I("9월 14일", "월드시리즈 취소", 1, "bad")])
SC['l4'] = ROS("직장폐쇄 · 멈추는 거래", "메이저리그 구단 40인 로스터", cap="FA 계약 · 트레이드 멈춤", capC="bad", capAt=0.6, chain="ros1")
# 11/13 사용자("선수 전부는 아님 — 너무 자주 많이 바껴서 이해가 잘 안돼"): 오른쪽 글 상자는 그림이 바뀔 때만(26명 강조 → 자물쇠) 두 번, 대사를 따라 읽는 글은 뺌
SC['l5'] = dict(SC['l4'], title="직장폐쇄 · 멈추는 범위", cap=None, capC=None, capAt=1)
SC['l5y'] = dict(SC['l5'])
SC['l5x'] = dict(SC['l5y'])
SC['l5a'] = dict(SC['l5x'], hiN=26, hiAt=0.4, cap="경기 출전 26명", capAt=0.5)
SC['l5b'] = dict(SC['l5a'], hiN=0, hiAt=-1, mode="lock", at=1, cap="직장폐쇄로 묶임", capC="bad", capAt=1.1)
SC['l5c'] = dict(SC['l5b'], at=-1)
SC['l5d'] = BF("40인 로스터 밖", [it("마이너리그 선수", 0.2, w=360), it("직장폐쇄 대상 아님", 2, hi=True, w=400), it("마이너 계약 가능", 3, w=360)])
SC['l5e'] = BF("뒤에서 다시", [it("40인 로스터", 0.2), it("KBO 외국인 영입", 1, hi=True, w=420)])
SC['l6'] = BF("직장폐쇄 지침", [it("구단 직원", 0.2), it("선수", 0.5), it("크리스마스 카드 금지", 1, hi=True, w=460)], vals=[V("34쪽", "지침", 2, size=110)])
SC['l6b'] = BF("직장폐쇄 중 금지", [it("구단 홈페이지", 0.2, w=360), it("선수 사진 · 영상 내림", 1, hi=True, w=500)])
SC['l6c'] = BF("직장폐쇄 중 허용", [it("일본 리그 등", 0.2, w=320), it("다른 리그 출전 가능", 2, hi=True, w=420)])
SC['l7'] = TLn("지난 직장폐쇄 · 2021~22년", [I("2021년 12월 2일", "직장폐쇄 시작", 0.7, "bad"), I("2022년 3월 10일", "직장폐쇄 끝", 50), I("99일", "멈춘 기간", 50, "gold")], chain="tl21")
SC['l7b'] = BF("2021년 · 구단주 결정", [it("구단주 투표", 0.2), it("만장일치", 1, hi=True), it("직장폐쇄", 1.4)])
SC['l8'] = KEEP(SC['l7']); SC['l8']['items'][1]['at'] = 0.2; SC['l8']['items'][2]['at'] = 1
# ── 2026년엔 왜 멈추나
SC['l9'] = BN("2026년 협상 쟁점", [V("샐러리캡", "팀 연봉 상한", 0.3, hi=True)])
SC['l9b'] = BF("롭 맨프레드 커미셔너 · 7월", [it("최다 팀 연봉", 1, w=320), it("최소 팀 연봉", 2, join="−", w=320), it("4억 4100만 달러", 3, join="=", hi=True, w=400)])
SC['l10'] = S(0, "rf_bars", title="구단주 제안 · 10월 8일 · 한 팀 연봉", items=[dict(label="상한", v=245, txt="2억 4500만 달러", at=1.8), dict(label="하한", v=171, txt="1억 7100만 달러", at=3)], max=420, noCenter=True)
SC['l10d'] = BN("구단주 제안", [V("계약 기간", "", 0.2, size=110), V("상한", "", 1, hi=True, size=110)])
SC['l10e'] = S(0, "rf_bars", title="구단주 제안 · 계약 기간 상한", items=[dict(label="다른 팀으로 갈 때", v=5, txt="5년", at=0.2), dict(label="원래 팀과 재계약", v=6, txt="6년", at=1)], max=7, noCenter=True)
SC['l10c'] = TLn("구단주 제안 · 상한제 시작", [I("10월 8일 제안", "곧바로 상한제", 0.2), I("그 뒤 수정안", "2028년부터", 1, "gold")])
SC['l11'] = BF("선수노조", [it("최저 연봉 인상", 50, w=360), it("적게 쓰는 구단 세금", 50, join="+", hi=True, w=440)], vals=[V("상한제 반대", "", 1, hi=True, size=110)], fat=50, chain="pa")
SC['l11d'] = KEEP(SC['l11']); SC['l11d']['fig']['at'] = 0.2; SC['l11d']['fig']['items'][0]['at'] = 0.2; SC['l11d']['fig']['items'][1]['at'] = 1.4
SC['l11b'] = FQn("롭 맨프레드", "MLB 커미셔너", "7월", "내 재임 기간 중 가장 단결된 구단주들"); SC['l11b']['at'] = 1
SC['l11c'] = FQn("브루스 마이어", "선수노조 위원장 대행", "7월", "샐러리캡은 경쟁하지 않으려는 핑계"); SC['l11c']['at'] = 1
SC['l12'] = BN("12월 1일 전 합의", [V("12월 1일 전", "새 협약", 0.2, size=110), V("가능성 낮음", "언론 전망", 1, hi=True, size=110)])
# ── 아침 7시 · 노시환
SC['c1'] = CD("첫 번째 마감 · 12월 2일 아침 7시", hl=(0,))
SC['n2'] = TLn("노시환 포스팅 · 한국 시간", [I("11월 2일 밤 10시", "협상 시작", 0.7), I("12월 2일 아침 7시", "협상 마감", 2, "gold"), I("규정상", "30일", 3)])
SC['n4'] = CLK("한국 시간 · 12월 2일", [MK(7, "오전 7시", "노시환 협상 마감", -1), MK(14, "오후 2시 무렵", "MLB 노사협약 만료", 0.3, "bad")], gap=dict(a=7, b=14, at=1, sub="노사협약 만료 7시간 전"))
_SZ = [("2021년 11월", "직장폐쇄 직전 포스팅", 1, "gold"), ("12월 2일 · 열흘 뒤", "직장폐쇄 시작", 50, "bad"), ("직장폐쇄 중", "협상 기간 멈춤", 50, "bad"), ("2022년 3월 10일", "직장폐쇄 끝", 50, None), ("3월 18일 · 컵스", "5년 8500만 달러", 50, "gold")]
SC['n6'] = PSt("스즈키", "스즈키 세이야", "", "2021년 · 일본 포스팅", STPS(*_SZ), chain="sz")
SC['n7'] = KEEP(SC['n6']); SC['n7']['viz'][0]['items'][1]['at'] = 1
SC['n8'] = KEEP(SC['n7']); SC['n8']['viz'][0]['items'][2]['at'] = 0.3
SC['n8b'] = KEEP(SC['n8']); SC['n8b']['viz'][0]['items'][3]['at'] = 1
SC['n9'] = KEEP(SC['n8b']); SC['n9']['viz'][0]['items'][4]['at'] = 1
SC['n21'] = PSt("사토", "사토 테루아키", "", "2026년 겨울 · 일본 포스팅", STPS(("일본", "2026년 겨울 포스팅", 0.2, None), ("3명", "사토 · 다이라 · 이토", 1, "gold")), imgAt=1)
SC['n10'] = TLn("포스팅 협상 기간 · 직장폐쇄 중", [I("2021년", "멈춤", 0, "bad"), I("2026년", "멈추지 않음 · 언론 전망", 1, "gold"), I("포스팅 선수", "일본 선수까지\n직장폐쇄 전 계약", 50)], chain="p26")
SC['n11'] = KEEP(SC['n10']); SC['n11']['items'][2]['at'] = 0.3
SC['n12'] = PSt("노시환", "노시환", "한화", "2026년 · 포스팅", STPS(("스즈키처럼", "기다릴 수 없음", 1, "bad")))
SC['n14'] = PSt("노시환2", "노시환", "한화", "마감 전 계약 시", STPS(("마감 전 계약", "메이저리그행", 1, "gold"), ("한화 11년 307억", "없던 일", 2.6, "bad")))
SC['n16'] = PSt("노시환", "노시환", "한화", "계약 실패 시", STPS(("포스팅", "끝", 0.5, "bad"), ("한화 복귀", "원래 계약 이어 감", 50, None), ("2027년 11월 1일까지", "다시 포스팅 못 함", 50, "bad")), chain="nc2")
SC['n17'] = KEEP(SC['n16']); SC['n17']['viz'][0]['items'][1]['at'] = 0.3
SC['n18'] = KEEP(SC['n17']); SC['n18']['viz'][0]['items'][2]['at'] = 0.3
SC['n18b'] = BF("한화가 받는 이적료", [it("한화 이적료", 0.2, w=320), it("노시환 보장 금액", 1, join="=", w=380), it("20%", 1.4, join="×", hi=True, w=200)], team="한화", chain="fee")
SC['n18c'] = KEEP(SC['n18b']); SC['n18c']['vals'] = [V("2500만 달러 이하", "보장 금액일 때", 0.2, size=100)]
SC['n23'] = PSt("노시환", "노시환", "한화", "2026년 성적", STPS(("127경기", "출전", 0.3, None), ("타율", "2할 8푼 3리", 1, None), ("29홈런", "96타점", 2, "gold")))
SC['n24b'] = DUOT("포스팅 선배들 · 보장 총액", [DCT("김혜성", "김혜성", "", 0, [dict(k="다저스 3년", v="1250만 달러", at=1, hi=True)]), DCT("송성문", "송성문", "", 2, [dict(k="샌디에이고 4년", v="1500만 달러", at=2, hi=True)])])
SC['n25'] = PSt("노시환2", "노시환", "한화", "미국 구단 제안 · 언론 전망", STPS(("미국 구단", "제안", 0.2, None), ("돈", "한화 계약보다 적게", 1, None), ("기간", "더 짧게", 2, "bad")), chain="nm")
SC['n25b'] = KEEP(SC['n25'], sub="2026년 겨울 FA 시장"); SC['n25b']['viz'] = STPS(("2026년 겨울", "FA 시장", 0.2, None), ("3루수", "주전감 부족", 1, None), ("노시환", "유리", 2, "gold"))
SC['n26'] = PSt("노시환", "노시환", "한화", "노시환 · 언론 전망", STPS(("한국 복귀 가능성", "더 높다", 0.4, "gold"), ("약점", "삼진", 50, "bad"), ("2026년", "147삼진 · 개인 최다", 50, "bad")), chain="n26")
SC['n27'] = KEEP(SC['n26']); SC['n27']['viz'][0]['items'][1]['at'] = 0.3
SC['n27b'] = KEEP(SC['n27']); SC['n27b']['viz'][0]['items'][2]['at'] = 0.2
SC['n28'] = SPt("류지현", "류지현 감독", "한화", [BB("11월 8일 감독이 전한 노시환 문자", "감독님, 죄송하다", 1.2, hi=True), BB("11월 8일", "지금까지는 노시환이 있다, 없다를 가지고 생각하고 싶지 않다", 50)], chain="ryu")
SC['n29'] = KEEP(SC['n28']); SC['n29']['bubbles'][1]['at'] = 0.4; SC['n29']['bubbles'][1]['hi'] = True; SC['n29']['bubbles'][0]['hi'] = False
def FANS(team, bubbles, **k): return S(0, "fa_fans", team=team, title="팬 반응", sub=TEAMN.get(team, team), bubbles=[dict(t=t, at=a, c=c) for t, a, c in bubbles], bg=TBG(team), noCenter=True, **k)
SC['nf2'] = FANS("한화", [("노시환 빠지면 공격도 3루 수비도 구멍", 0.5, None), ("3루는 누가? 대안 찾기", 50, None), ("진출 가능성? '어렵다' vs '간다'", 50, None)], chain="fan1")
SC['nf3'] = KEEP(SC['nf2']); SC['nf3']['bubbles'][1]['at'] = 0.5
SC['nf4'] = KEEP(SC['nf3']); SC['nf4']['bubbles'][2]['at'] = 0.15
# ── 오후 2시 · FA 시장과 김하성
SC['c2'] = CD("두 번째 마감 · 12월 2일 오후 2시", hl=(1,))
SC['c2b'] = CLK("한국 시간 · 12월 2일 오후 2시", [MK(7, "오전 7시", "노시환 협상 마감", 0), MK(14, "오후 2시 무렵", "넘기면 FA · 트레이드 멈춤", 0.4, "bad")])
SC['n20'] = TLn("2021년 · 직장폐쇄 직전", [I("12월 1일", "하루 계약\n14억 달러", 1.8, "gold"), I("12월 2일", "직장폐쇄 시작", 0.2, "bad")])
_KS = [("3년 연속", "FA", 50, "gold"), ("2026년 · 애틀랜타", "1년 2000만 달러", 50, None), ("1월", "빙판길 · 오른손 중지 수술", 50, "bad"), ("2026년", "51경기 · 타율 1할 1푼 6리", 50, "bad")]
SC['k1'] = PSt("김하성", "김하성", "", "오후 2시 마감 · FA 유격수", STPS(*_KS), imgAt=1, chain="kim")
SC['k2'] = KEEP(SC['k1']); SC['k2']['viz'][0]['items'][0]['at'] = 0.3
SC['k2c'] = KEEP(SC['k2']); SC['k2c']['viz'][0]['items'][1]['at'] = 1
SC['k3'] = KEEP(SC['k2c']); SC['k3']['viz'][0]['items'][2]['at'] = 0.6
SC['k4'] = KEEP(SC['k3']); SC['k4']['viz'][0]['items'][3]['at'] = 0.5
SC['k6'] = BN("퀄리파잉 오퍼", [V("구단 → FA", "1년짜리 제안", 1, size=110), V("약 2315만 달러", "1년", 2, hi=True, size=110)])
SC['k5'] = PSt("김하성", "김하성", "", "애틀랜타의 선택", STPS(("애틀랜타", "퀄리파잉 오퍼 안 줌", 1, "bad"), ("언론 전망", "순수한 재능은 최고의 FA", 50, None), ("예상 계약", "1년 1000만 달러", 50, "gold")), chain="kim3")
SC['k7'] = KEEP(SC['k5']); SC['k7']['viz'][0]['items'][1]['at'] = 1; SC['k7']['viz'][0]['items'][2]['at'] = 3
SC['k9'] = TLn("김하성 · 남은 시간", [I("12월 2일 오후 2시 전", "계약 가능", 0.5, "gold"), I("직장폐쇄 중", "계약 못 함", 1, "bad"), I("직장폐쇄 끝", "다시 협상", 2)])
SC['k9b'] = TLn("2021~22년 직장폐쇄 · 프레디 프리먼", [I("직장폐쇄 전", "팀 못 찾음", 0.3, "bad"), I("2022년 3월 중순", "다저스와 계약", 2, "gold")])
SC['k11'] = PSt("김하성", "김하성", "", "김하성 · 언론 전망", STPS(("직장폐쇄가 오면", "", 0.2, None), ("행선지 찾기", "길어질 수도", 1, "bad")))
# ── 오후 2시 · KBO 외국인 영입 창구
SC['c3'] = CLK("한국 시간 · 12월 2일 오후 2시", [MK(14, "오후 2시 무렵", "KBO 외국인 영입 창구", 0.6, "bad")])
SC['f2'] = QQ("메이저리그 일인데 · 왜 KBO 영입이 막힐까?")
SC['f3'] = ROS("KBO가 노리는 외국인 · 40인 로스터", "메이저리그 구단 40인 로스터", cap="40인 로스터에 든 선수도", capAt=1.5, chain="ros2")
SC['f4'] = dict(SC['f3'], title="40인 로스터 선수를 데려오려면", cap="원래 구단이 풀어 줘야", capAt=1)
SC['f5'] = dict(SC['f4'], title="직장폐쇄가 되면 · 40인 로스터는 잠김", mode="lock", at=0.5, cap="방출까지 멈춤", capC="bad", capAt=2)
SC['f6'] = FQn("한 구단 단장", "2021년 직장폐쇄 다음 날", "2021년 12월 3일", "소속이 있는 외국인 선수들을 데려올 수 없다"); SC['f6']['at'] = 2
SC['f7'] = TLn("2021년 · 롯데 피터스", [I("직장폐쇄 무렵", "텍사스 40인\n로스터에서 빠짐", 1, "bad"), I("12월 9일", "롯데와 계약", 50, "gold")], chain="pet")
SC['f8'] = KEEP(SC['f7']); SC['f8']['items'][1]['at'] = 0.3
SC['f9'] = TLn("KBO 외국인 영입 · 2026년", [I("미리 영입", "서두르는 팀", 0.6, "gold"), I("12월 2일 오후 2시", "노사협약 만료", 0.2, "bad")])
SC['f10'] = PSt("벡", "트리스탄 벡", "LG", "LG 트윈스 · 새 외국인 투수", STPS(("11월 5일", "LG와 계약", 0.2, None), ("총액", "87만 8천 달러", 2, "gold"), ("2026년", "샌프란시스코", 50, None), ("최고 구속", "158km", 50, "gold")), imgAt=1, chain="beck")
SC['f11'] = KEEP(SC['f10']); SC['f11']['viz'][0]['items'][2]['at'] = 0.3; SC['f11']['viz'][0]['items'][3]['at'] = 1.2
SC['f13'] = BN("LG가 서두른 이유", [V("LG 영입", "11월 5일", 0.2, size=110), V("직장폐쇄", "무관하지 않다 · 언론 분석", 1, hi=True, size=110)], team="LG")
SC['f14'] = PSt("왓슨", "트로이 왓슨", "한화", "한화 이글스 · 새 외국인 투수", STPS(("11월 11일", "한화와 계약", 0.2, None), ("총액", "100만 달러", 2, "gold"), ("2026년 7월", "한화 등 KBO 관심", 50, None)), imgAt=1, chain="wat0")
SC['f15'] = KEEP(SC['f14']); SC['f15']['viz'][0]['items'][2]['at'] = 0.3
SC['f16'] = ROS("트로이 왓슨 · 40인 로스터", "디트로이트 40인 로스터", img=ph("왓슨"), name="왓슨", cap="40인 로스터 등록 → 영입 막힘", capC="bad", capAt=2, mode="in", at=1, chain="wat")
SC['f17'] = dict(SC['f16'], sub="시애틀 40인 로스터", mode="out", at=1, toTeam="한화", cap="40인 로스터 제외 → 한화와 계약", capC=None, capAt=2)
SC['f18'] = dict(SC['f17'], at=-1, cap="40인 로스터 한 칸 · 막기도, 풀기도", capAt=0.3)
SC['f19'] = PSt("와이스2", "와이스", "한화", "전 한화 투수", STPS(("11월 11일", "샌디에이고 메이저리그 계약", 50, "gold"), ("1년 185만 달러", "2028년 구단 옵션", 50, None), ("직장폐쇄 전", "메이저리그 자리 잡음", 50, "gold")), chain="wei")
SC['f20'] = KEEP(SC['f19']); SC['f20']['viz'][0]['items'][0]['at'] = 0.3
SC['f21'] = KEEP(SC['f20']); SC['f21']['viz'][0]['items'][1]['at'] = 0.2
SC['f21b'] = KEEP(SC['f21']); SC['f21b']['viz'][0]['items'][2]['at'] = 0.2
SC['fh1'] = PSt("페라자", "페라자", "한화", "한화 외국인 타자", STPS(("한화", "결별", 1, "bad"), ("새 외국인 타자", "찾는 중", 1.5, None)))
SC['fh2'] = FQn("한화 관계자", "외국인 타자 영입", "11월 11일", "노시환 선수 포스팅 이슈도 있기에 전체적으로 외국인 시장을 계속 살피고 있다", team="한화"); SC['fh2']['at'] = 1
SC['fh3'] = CLK("한화 외국인 타자 · 12월 2일", [MK(7, "오전 7시", "노시환 포스팅 결과", 0.6), MK(14, "오후 2시 무렵", "40인 로스터 이적 멈춤", 50, "bad")], chain="fh")
SC['fh3b'] = KEEP(SC['fh3']); SC['fh3b']['marks'][1]['at'] = 0.4; SC['fh3b']['gap'] = dict(a=7, b=14, at=1, sub="40인 로스터 선수라면")
SC['fh4'] = FANS("한화", [("외국인 타자 결정, 포스팅 결과 뒤로?", 1, "bad")])
# ── 멈춘 뒤 · 2월 1일과 3월 중순
SC['c4'] = CD("멈춘 뒤 · 다음 마감 2월 1일", hl=(2,))
SC['f6b'] = BN("2021년 · 새 외국인 계약", [V("12월 3일까지", "직장폐쇄 다음 날", 0.2, size=100), V("10개 구단 중", "", 1, size=100), V("1명", "KT 라모스", 3, hi=True, size=100)])
SC['f6c'] = TLn("2021년 · KBO 구단의 마지노선", [I("12월 2일", "직장폐쇄 시작", 0.2, "bad"), I("2월 1일", "캠프 시작 · 마지노선", 0.8, "gold")])
SC['f22'] = BF("직장폐쇄의 다른 면", [it("메이저리그 FA", 50, w=340), it("갈 곳 없음", 50), it("아시아로", 50, hi=True)], vals=[V("기회", "", 0.6, hi=True, size=110)], fat=50, chain="opp")
SC['f23'] = KEEP(SC['f22']); SC['f23']['fig']['at'] = 0.2; SC['f23']['fig']['items'][0]['at'] = 0.2; SC['f23']['fig']['items'][1]['at'] = 0.6; SC['f23']['fig']['items'][2]['at'] = 1
SC['f24'] = FQn("한 구단 단장", "2021년 직장폐쇄 다음 날", "2021년 12월 3일", "일장일단이 있는 상황이다"); SC['f24']['at'] = 2
SC['f25'] = BF("새 외국인 선수 · 첫해", [it("계약금 · 연봉", 0.3, w=320), it("이적료", 1, join="+"), it("100만 달러 이하", 2, join="=", hi=True, w=380)])
SC['c5'] = CD("마지막 마감 · 3월 중순", hl=(3,))
SC['l13'] = TLn("2027 메이저리그 개막", [I("3월 중순", "162경기 마지노선", 2, "bad"), I("3월 25일", "개막 예정", 1, "gold")])
SC['l8b'] = TLn("2022년 개막 · 직장폐쇄 여파", [I("3월 1일", "개막 두 시리즈\n취소 발표", 1, "bad"), I("3월 10일", "새 협약\n일정 다시 짬", 3, "gold"), I("개막", "3월 31일\n→ 4월 7일", 50)], chain="op22")
SC['l8c'] = KEEP(SC['l8b']); SC['l8c']['items'][2]['at'] = 0.6
SC['k10'] = PSt("김하성", "김하성", "", "3월까지 직장폐쇄 시", STPS(("3월까지", "직장폐쇄", 0.2, "bad"), ("팀 못 찾은 FA", "김하성처럼", 1, None), ("새 팀 캠프", "짧게", 2, "bad")))
# ── 날짜 정리
SC['e0'] = CD("날짜 정리")
SC['e0b'] = CLK("날짜 정리 · 한국 시간 12월 2일", [MK(7, "오전 7시", "노시환 협상 마감", 0.3), MK(14, "오후 2시 무렵", "FA · 40인 이적 멈출 수도", 50, "bad")], chain="clk3")
SC['e0c'] = KEEP(SC['e0b']); SC['e0c']['marks'][1]['at'] = 0.6
SC['e0e'] = CD("직장폐쇄 시 · 남는 시간", hl=(2, 3))
SC['e1'] = BN("노사협약 만료까지 남은 시간", [V("12월 2일", "오후 2시", 0.2, size=110), V("3주도 안 남음", "", 1, hi=True, size=110)])
SC['e2'] = Q("12월 1일 전 새 협약? · 아니면 직장폐쇄?", [], chain="eq")
SC['e3'] = KEEP(SC['e2'])
SC['e4'] = BN("다음 영상", [V("KBO FA 공시 총정리", "10개 구단별로", 1, hi=True)])
# 11/12 00:28 사용자: 목차는 말로 읽지 않고 화면으로 — 오프닝 끝에 전체, 챕터가 바뀔 때마다 지금 칸 강조(말 없는 holdAfter 동안)
TOC = ["직장폐쇄?", "이번엔 왜 또?", "노시환 협상 마감", "FA 시장과 김하성", "KBO 외국인 영입은?", "멈추면 언제까지?", "날짜 정리"]   # 11/12 23:54 사용자 "명칭은 센스있게, AI 티 내지 말고" — 가운뎃점 나열 ✗
# ── 11/12 13:18 사용자 "어려운 설명은 단순 텍스트가 아니라 시각 자료로" → 그림 흐름도(lo_flow): 구단주·선수노조·협약 문서·문 닫힘, FA·트레이드 화살표 막힘, 40인 로스터 → KBO 영입 통로
def ND(id, x, y, ic, lab="", sub="", at=0, **k): return dict(id=id, x=x, y=y, ic=ic, lab=lab, sub=sub, at=at, **k)
def ED(a, b, lab="", at=0, **k): return dict(a=a, b=b, lab=lab, at=at, **k)
def FL(title, nodes, edges=(), wall=None, boxes=(), cap=None, **k): return S(0, "lo_flow", title=title, nodes=list(nodes), edges=list(edges), wall=wall, boxes=list(boxes), cap=cap, noCenter=True, **k)
def KEEPF(sc, **k):
    sc = KEEP(sc, **k)
    def f(o):
        if isinstance(o, dict):
            for kk in list(o):
                if kk in ('stopAt', 'expAt', 'goneAt', 'lockAt', 'okAt') and isinstance(o[kk], (int, float)) and o[kk] < 50: o[kk] = -1
                else: f(o[kk])
        elif isinstance(o, list):
            for v in o: f(v)
    f(sc); return sc
# 오프닝 · KBO 외국인 영입 창구 = 40인 로스터 → KBO 구단 통로가 막힐 수 있음
SC['o4b'] = FL("오후 2시 무렵 · KBO 외국인 영입 창구", [ND("ros", 560, 600, "roster", "메이저리그 40인 로스터", at=0.1), ND("kbo", 1360, 600, "kbo", "KBO 구단", at=0.2)], [ED("ros", "kbo", "외국인 영입", 0.3, c="gold", stopAt=1.1)])
# 1장 · 노사협약 = 구단주와 선수노조가 맺는 문서 → 만료 → 새 협약 없으면 구단주가 문을 닫음 = 직장폐쇄
_DEAL = [ND("own", 420, 620, "owner", "구단주", at=0.3), ND("doc", 960, 580, "doc", "노사협약", at=0.1, expAt=50, goneAt=50, stamp="만료"), ND("uni", 1500, 620, "union", "선수노조", at=0.5)]
SC['l1'] = FL("직장폐쇄가 뭐길래 · 노사협약과 직장폐쇄", _DEAL, [ED("own", "doc", "", 0.6, r1=90), ED("uni", "doc", "", 0.7, r1=90)], cap="리그 운영 규칙", capAt=1, capY=810, chain="deal")
SC['l2'] = KEEPF(SC['l1'], cap="새 협약 없음", capC="bad"); SC['l2']['nodes'][1]['expAt'] = 0.3; SC['l2']['capAt'] = 0.7
SC['l2']['edges'][0]['stopAt'] = 0.7; SC['l2']['edges'][1]['stopAt'] = 0.7
SC['l2']['nodes'][1]['goneAt'] = 1; SC['l2']['wall'] = dict(x=960, at=1)
SC['l3'] = KEEPF(SC['l2'], cap="구단주가 문을 닫음 = 직장폐쇄", capC="bad"); SC['l3']['capAt'] = 0.2
SC['l3b'] = FL("직장폐쇄와 파업", [ND("st1", 330, 640, "stadium", "구장", at=0.2), ND("pl1", 720, 640, "union", "선수", "스스로 멈춤", at=0.2, subC="bad"),
                                ND("st2", 1210, 640, "stadium", "구장", at=1, lockAt=1.3), ND("ow2", 1590, 640, "owner", "구단주", "문을 닫음", at=1, subC="bad")],
               [ED("st1", "pl1", "", 0.5, r0=130, r1=110)], boxes=[dict(x=120, y=320, w=800, h=540, lab="파업", at=0.2), dict(x=1000, y=320, w=800, h=540, lab="직장폐쇄", at=1, c="bad")])
# FA 계약·트레이드 화살표가 막힘
_MKT = [ND("fa", 420, 640, "player", "FA 선수", at=0), ND("ta", 960, 640, "team", "구단 A", at=0), ND("tb", 1500, 640, "team", "구단 B", at=0)]
SC['l4'] = FL("직장폐쇄 · 멈추는 거래", _MKT, [ED("fa", "ta", "FA 계약", 0, stopAt=0.4), ED("ta", "tb", "트레이드", 0, two=True, stopAt=1.1)])
SC['l5d'] = FL("40인 로스터 밖 · 마이너리그 선수", [ND("tm", 960, 400, "team", "메이저리그 구단", at=0), ND("ros", 420, 690, "roster", "40인 로스터", "직장폐쇄 대상", at=0, lockAt=0, subC="bad"), ND("min", 1500, 690, "union", "마이너리그 선수", "직장폐쇄 대상 아님", at=1, subC="gold")],
               [ED("tm", "ros", "", 0, stopAt=0.2, r0=170, r1=150), ED("tm", "min", "계약 이어 감", 2.6, okAt=3, r0=170, r1=150, labDy=-60)])
SC['l5e'] = FL("뒤에서 다시 · 40인 로스터와 KBO", [ND("ros", 560, 620, "roster", "40인 로스터", at=0.2), ND("kbo", 1360, 620, "kbo", "KBO 외국인 영입", at=1)], [ED("ros", "kbo", "", 1.3, c="gold")])
# 2시 · 넘기면 FA·트레이드 멈춤
SC['c2b'] = FL("오후 2시 이후", _MKT, [ED("fa", "ta", "FA 계약", 0, stopAt=1), ED("ta", "tb", "트레이드", 0, two=True, stopAt=1.4)])
# KBO 외국인 영입 통로
SC['c3'] = FL("같은 오후 2시 · KBO 외국인 영입 창구", [ND("ros", 560, 600, "roster", "메이저리그 40인 로스터", at=0.2), ND("kbo", 1360, 600, "kbo", "KBO 구단", at=0.2)], [ED("ros", "kbo", "외국인 영입", 0.6, c="gold", stopAt=2)])
_PIPE = [ND("kbo", 1440, 660, "kbo", "KBO 구단", at=0.2), ND("ros", 480, 660, "roster", "메이저리그 40인 로스터", "외국인 선수", at=1, subC="gold"), ND("org", 960, 420, "team", "원래 구단", "풀어 줘야 이적", at=50, subC="gold")]
SC['f3'] = FL("KBO 외국인 영입 · 40인 로스터", _PIPE, [ED("ros", "kbo", "영입", 1.6, c="gold", r0=140, r1=130, labDy=-62)], chain="pipe")
SC['f4'] = KEEPF(SC['f3']); SC['f4']['nodes'][2]['at'] = 1
SC['f5'] = KEEPF(SC['f4'], cap="직장폐쇄가 되면 방출까지 멈춤", capC="bad"); SC['f5']['nodes'][1]['lockAt'] = 1; SC['f5']['edges'][0]['stopAt'] = 2; SC['f5']['capAt'] = 2
# 11/12 23:55 사용자 "문을 닫으면 어떻게 되는지, 왜 닫는지 설명" → 왜(양쪽 말) + 어떻게(시설 출입 금지)
_WHY = [ND("own", 420, 620, "owner", "구단주", at=0), ND("uni", 1500, 620, "union", "선수노조", at=0)]
SC['l3w'] = FL("직장폐쇄 · 문을 닫는 이유", _WHY, [ED("own", "uni", "구단주 쪽 말: 협상 속도 · 시즌 지키기", 50, c="gold", bend=-230, r0=110, r1=110, labDy=24), ED("own", "uni", "선수노조 쪽 말: 선수 압박", 50, c="bad", bend=170, r0=110, r1=110, labDy=-64)],
               cap="왜?", capAt=0.6, capY=330, chain="why")
SC['l3x'] = KEEPF(SC['l3w'], cap="맨프레드 커미셔너 · 2021년 12월 2일"); SC['l3x']['edges'][0]['at'] = 1; SC['l3x']['capAt'] = 0.2
SC['l3y'] = KEEPF(SC['l3x'], cap="선수노조 · 같은 날"); SC['l3y']['edges'][1]['at'] = 1; SC['l3y']['capAt'] = 0.2
SC['l3h'] = FL("직장폐쇄 · 문이 닫히면", [ND("st", 560, 640, "stadium", "구단 시설", at=0, lockAt=0.3), ND("pl", 1360, 640, "union", "선수", at=0)], [ED("pl", "st", "출입", 0.5, r0=130, r1=150, stopAt=1)], cap="구단 시설 출입 금지", capC="bad", capAt=1.2)
# 11/13 00:00 사용자 "월드시리즈가 어떤 건지도 이야기해 줘"
SC['l3d'] = BN("", [V("월드시리즈", "메이저리그 우승을 가리는 마지막 무대", 0.2, hi=True, size=120), V("한국시리즈", "KBO로 치면", 2, size=120)])
SC['l3e'] = TLn("월드시리즈가 열리지 않은 해", [I("1904년", "", 0.3, "bad"), I("1994년", "90년 만에", 1, "bad")])
# 이적료·퀄리파잉 오퍼도 그림으로
SC['n18b'] = FL("한화가 받는 이적료", [ND("mlb", 420, 600, "team", "미국 구단", at=0.6), ND("nos", 1300, 400, "player", "노시환", at=1), ND("hh", 1300, 720, "team", "한화", at=0.2)],
                [ED("mlb", "nos", "보장 금액", 1, c="gold", r0=150, r1=120), ED("mlb", "hh", "보장 금액의 20% = 이적료", 1.6, c="gold", r0=150, r1=120, labDy=-56)], chain="fee")
SC['n18c'] = KEEPF(SC['n18b'], cap="보장 금액 2500만 달러 이하일 때", capX=560, capY=800); SC['n18c']['capAt'] = 0.2
SC['k6'] = FL("퀄리파잉 오퍼", [ND("tm", 520, 620, "team", "구단", at=0.3), ND("fa", 1400, 620, "player", "FA 선수", at=0.6)], [ED("tm", "fa", "1년 약 2315만 달러", 2, c="gold", r0=150, r1=130)], cap="1년짜리 제안", capAt=3)
# 11/12 13:15 사용자 "목차가 나올 때 나레이션이 아무 말도 안 하는데 인트로 대사는 있어야지 — 그 목차에 대해 자연스럽게 말하고 진행" → 챕터 첫 줄(질문형 다리 대사) 동안 목차판을 띄움(말 없는 쉼 ✗)
TOCAT = {'l0': (0, .4), 'w0': (1, .35), 'n0': (2, .35), 'k0': (3, .35), 'f0': (4, .35), 'g0': (5, .35), 'e0': (6, .35)}
_TOCPREV = {'l0': 'o5', 'w0': 'l8', 'n0': 'l12', 'k0': 'nf4', 'f0': 'k11', 'g0': 'fh4'}
for _k, _p in _TOCPREV.items(): SC[_k] = KEEP(SC[_p])
for _k, (_hi, _ha) in TOCAT.items(): SC[_k] = dict(SC[_k], toc=dict(hi=_hi, full=True, hiAt=_ha))
# 11/12 23:59 사용자 "같은 단어가 두 번(빨간 표시 + 왼쪽 위 제목) · 볼 게 너무 많아 시선 분산 · '노사협약이 끝나면' 같은 제목도 AI 같아"
# → 그림·표시가 말하는 장면은 제목을 없애고, 남기는 제목은 짧은 이름(날짜·사람)만. 표시와 같은 낱말 반복 ✗
# ── 11/13 00:39 사용자 "이런 텍스트만 나오게 하지 말라니까 좀.." → 글 상자(rf_band)만 있던 설명 장면을 전부 그림(lo_flow·lo_pay·lo_cal)으로
def PAY(bars, lines=(), **k): return S(0, "lo_pay", bars=list(bars), lines=list(lines), noCenter=True, **k)
def B(v, at=0, **k): return dict(v=v, at=at, **k)
def LN(v, lab, at=0, **k): return dict(v=v, lab=lab, at=at, **k)
def KEEPP(sc, **k):
    sc = KEEP(sc, **k)
    def f(o):
        if isinstance(o, dict):
            for kk in list(o):
                if kk in ('xAt', 'cutAt', 'moveAt') and isinstance(o[kk], (int, float)) and o[kk] < 50: o[kk] = -1
                else: f(o[kk])
        elif isinstance(o, list):
            for v in o: f(v)
    f(sc); return sc
_PV = [.95, .82, .66, .52, .4, .3]   # 구단별 연봉(모양만 — 숫자 없음)
# 월드시리즈 = KBO 한국시리즈
SC['l3d'] = FL("", [ND("ws", 640, 600, "trophy", "월드시리즈", "메이저리그 우승 결정전", at=0, c="gold", subC="gold"), ND("ks", 1300, 600, "trophy", "한국시리즈", "KBO 우승 결정전", at=2)],
               [ED("ws", "ks", "KBO로 치면", 2, r0=170, r1=170)])
# 34쪽 지침: 구단 직원 → 선수 크리스마스 카드도 막힘
SC['l6'] = FL("", [ND("st", 420, 620, "owner", "구단 직원", at=0), ND("ml", 960, 600, "mail", "크리스마스 카드", at=1), ND("pl", 1500, 620, "player", "선수", at=0.2)],
              [ED("st", "ml", "", 1, r1=130), ED("ml", "pl", "", 1.2, r0=130, stopAt=1.6)], cap="34쪽짜리 지침", capAt=2)
# 구단 홈페이지에서 선수 사진·영상이 내려감
SC['l6b'] = FL("", [ND("web", 640, 600, "web", "구단 홈페이지", at=0), ND("pl", 1280, 620, "player", "선수 사진 · 영상", at=0.2, goneAt=1.2)],
               [ED("pl", "web", "", 0.4, r0=130, r1=150, stopAt=1)], cap="홈페이지에서 내림", capC="bad", capAt=1.2)
# 다른 리그 출전은 막지 않음
SC['l6c'] = FL("", [ND("mlb", 420, 620, "stadium", "메이저리그 구단", at=0, lockAt=0), ND("pl", 960, 620, "player", "선수", at=0), ND("jp", 1500, 620, "jp", "일본 리그 등", at=0.3)],
               [ED("pl", "mlb", "", 0, stopAt=0, r0=110, r1=150), ED("pl", "jp", "뛸 수 있음", 1, okAt=2, r0=110, r1=150)])
# 2021년 구단주 만장일치
SC['l7b'] = FL("", [ND("o1", 330, 620, "owner", "", at=0), ND("o2", 600, 620, "owner", "", at=0.1), ND("o3", 870, 620, "owner", "", at=0.2), ND("st", 1500, 620, "stadium", "직장폐쇄", at=1, lockAt=1.5), ND("bx", 1030, 620, "player", "", at=50)],
               [ED("bx", "st", "", 1, c="gold", r0=10, r1=150)],
               boxes=[dict(x=170, y=400, w=860, h=420, lab="구단주 전원", at=0)], cap="만장일치", capAt=1, capX=1500, capY=830)
# 샐러리캡 = 한 팀 연봉 상한
SC['l9'] = PAY([B(v) for v in _PV], [LN(.7, "한 팀 연봉 상한", 0.4, cutAt=0.8)], cap="샐러리캡", capAt=0.4, chain="pay1", x0=220, x1=1250, capX=735)
# 맨프레드: 가장 많이 쓰는 팀 − 가장 적게 쓰는 팀 = 4억 4100만 달러 (상한선은 빼고 차이만)
SC['l9b'] = dict(KEEPP(SC['l9']), lines=[], cap=None, tags=[dict(i=0, lab="가장 많이 쓰는 팀", at=1), dict(i=5, lab="가장 적게 쓰는 팀", at=2)],
                 brk=dict(a=0, b=5, lab="차이\n4억 4100만 달러", at=3))
# 계약 기간에도 상한
SC['l10d'] = PAY([B(v, 0.05 * i) for i, v in enumerate([.95, .78, .62, .45, .3])], [LN(.55, "계약 기간 상한", 1, c="bad", cutAt=1.3)], cap="선수별 계약 기간", capAt=0)
# 선수노조: 상한제 반대 → 대신 최저 연봉↑ · 적게 쓰는 구단에 세금
SC['l11'] = PAY([B(v) for v in _PV], [LN(.7, "연봉 상한", 0, xAt=1)], cap="선수노조: 상한제 반대", capC="bad", capAt=1, chain="pay2")
SC['l11d'] = KEEPP(SC['l11']); SC['l11d']['lines'].append(LN(.2, "최저 연봉 ↑", 0, v0=.08, moveAt=0.4, c="grn"))
SC['l11d']['tags'] = [dict(i=4, lab="세금", c="bad", at=1.5), dict(i=5, lab="세금", c="bad", at=1.6)]
# 12월 1일 전 합의 가능성 낮음
SC['l12'] = FL("", [ND("own", 420, 620, "owner", "구단주", at=0), ND("doc", 960, 580, "ghost", "새 협약", at=0.2), ND("uni", 1500, 620, "union", "선수노조", at=0)],
               [ED("own", "doc", "", 0.3, r1=90), ED("uni", "doc", "", 0.3, r1=90)], cap="12월 1일 전 합의 가능성 낮음", capC="bad", capAt=1)
# LG 벡 계약(11월 5일) → 직장폐쇄 전에 먼저
SC['f13'] = FL("", [ND("pl", 420, 620, "player", "벡", at=0), ND("lg", 960, 620, "kbo", "LG", "11월 5일 계약", at=0, subC="gold"), ND("st", 1500, 620, "stadium", "직장폐쇄", "12월 2일", at=0.6, lockAt=1, subC="bad")],
               [ED("pl", "lg", "", 0, c="gold")], cap="직장폐쇄 전에 먼저", capAt=1, capY=200)
# 2021년 12월 3일까지 새 외국인 계약: 10개 구단 중 KT 하나
_T10 = ["KIA", "KT", "LG", "NC", "SSG", "두산", "롯데", "삼성", "키움", "한화"]
SC['f6b'] = FL("", [ND("t%d" % i, 360 + 300 * (i % 5), 380 if i < 5 else 620, "kbo", t, at=1 + 0.05 * i, dim=(t != "KT"), hiAt=(3 if t == "KT" else None)) for i, t in enumerate(_T10)],
               cap="KT 라모스 1명", capAt=3, capY=790, isz=1.0)
# 직장폐쇄의 다른 면: 갈 곳 없는 FA → 아시아로
SC['f22'] = FL("", [ND("pl", 440, 600, "player", "메이저리그 FA", at=0), ND("mlb", 1400, 430, "stadium", "메이저리그 구단", at=0, lockAt=0.2)],
               [ED("pl", "mlb", "", 0.2, stopAt=0.6, r0=110, r1=150)], cap="기회도 있다", capAt=1, capY=150, chain="opp")
SC['f23'] = KEEPF(SC['f22']); SC['f23']['nodes'].append(ND("kbo", 1400, 760, "kbo", "KBO · 아시아", at=2))
SC['f23']['edges'].append(ED("pl", "kbo", "아시아로", 2.4, c="gold", r0=110, r1=130))
# 새 외국인 첫해 100만 달러: 계약금·연봉 + 이적료 ≤ 상한
SC['f25'] = PAY([dict(v=.78, at=0, segs=[dict(f=.5, lab="계약금 · 연봉", at=0), dict(f=.28, lab="이적료", c="gold", at=1)])], [LN(.8, "첫해 100만 달러", 2, c="bad")], x0=760, x1=1160, bw=240)
# 노사협약 만료까지 3주도 안 남음
SC['e1'] = S(0, "lo_cal", title="", months=[dict(lab="11월", sub="2026", first=0, days=30), dict(lab="12월", sub="2026", first=2, days=31)],
             items=[dict(m=0, d=[13, 30], time="", t="3주도 안 남음", at=0.3), dict(m=1, d=2, time="오후 2시", t="노사협약 만료", at=0, hl=True)], noCenter=True)
# ── 11/13 00:46 사용자 "어떤 이야기를 하기 전에는 빌드업을 충분히" → 새 사례·인물·화제 앞에 이유 한 줄(빌드업) 장면
SC['l3bz'] = KEEPF(SC['l3b'])
SC['l3g'] = KEEPF(SC['l3y'], cap=None)
SC['l5f'] = FL("", [ND("tm", 520, 620, "team", "구단", at=0), ND("pl", 1400, 620, "player", "선수", at=0.1)], [ED("tm", "pl", "연락", 0.3, two=True, stopAt=1, r0=150, r1=120)])
SC['l9a'] = KEEPP(SC['l9'])
SC['l11a'] = KEEPP(SC['l11d'])
SC['n5'] = KEEP(SC['n4']); SC['n5b'] = KEEP(SC['n4'])
SC['n5c'] = copy.deepcopy(SC['n6']); SC['n5c']['viz'][0]['items'][0]['at'] = 50
SC['n6'] = KEEP(SC['n5c']); SC['n6']['viz'][0]['items'][0]['at'] = 0.2; SC['n6']['viz'][0]['items'][1]['at'] = 1
SC['n9b'] = KEEP(SC['n9'])
_o23 = copy.deepcopy(SC['n23']); SC['n22'] = copy.deepcopy(_o23); SC['n22']['chain'] = "ns23"
for _it in SC['n22']['viz'][0]['items']: _it['at'] = 50
SC['n23'] = KEEP(SC['n22'])
for _a, _b in zip(SC['n23']['viz'][0]['items'], _o23['viz'][0]['items']): _a['at'] = _b['at']
_o28 = copy.deepcopy(SC['n28']); _ch = _o28.get('chain') or "ryu"
SC['n27c'] = copy.deepcopy(_o28); SC['n27c']['chain'] = _ch
for _b in SC['n27c']['bubbles']: _b['at'] = 50
SC['n28'] = KEEP(SC['n27c'])
for _a, _b in zip(SC['n28']['bubbles'], _o28['bubbles']): _a['at'] = _b['at']
SC['n29']['chain'] = _ch
SC['k5a'] = KEEP(SC['k4'])
_o7 = copy.deepcopy(SC['f7']); SC['f6x'] = copy.deepcopy(_o7); SC['f6x']['items'][0]['at'] = 50; SC['f6x']['items'][1]['at'] = 1
SC['f7'] = KEEP(SC['f6x']); SC['f7']['items'][0]['at'] = 1
SC['f8'] = KEEP(SC['f7'])
SC['f18b'] = KEEPF(SC['f18'])
SC['fh0'] = FL("", [ND("pl", 520, 620, "player", "노시환", "12월 2일 포스팅 결과", at=0, subC="gold"), ND("hw", 1400, 620, "kbo", "한화", "새 외국인 타자", at=0.5)],
               [ED("pl", "hw", "", 1, c="gold", r0=130, r1=140)])
_o6b = copy.deepcopy(SC['f6b']); SC['f6a'] = copy.deepcopy(_o6b); SC['f6a']['capAt'] = 50; SC['f6a']['chain'] = "f6"
for _n in SC['f6a']['nodes']: _n['at'] = 0.4 + 0.04 * int(_n['id'][1:]); _n['hiAt'] = None; _n['dim'] = False
SC['f6b'] = KEEPF(SC['f6a']); SC['f6b']['capAt'] = 3
for _n in SC['f6b']['nodes']:
    if _n['lab'] == "KT": _n['hiAt'] = 3
    else: _n['dim'] = True
SC['l13b'] = KEEP(SC['l13'])
# ── 11/13 00:52 사용자 "빨간 표시한(작은 글 · 점 · 값 목록) 형식은 이 영상이랑 안 맞고 이해가 잘 안돼, 다른 식으로" → 목록(steps)을 전부 다른 그림으로
def PSS(img, name, team, sub, stats, viz=(), **k): return PSt(img, name, team, sub, list(viz), stats=list(stats), **k)
# 스즈키: 사진 소개 뒤 날짜 줄(tline)
SC['n5c']['viz'] = []
SC['n6'] = TLn("", [I("2021년 11월 22일", "포스팅", 0.2, "gold"), I("12월 2일", "직장폐쇄 시작", 1, "bad"), I("직장폐쇄 중", "협상 기간 멈춤", 50, "bad"), I("2022년 3월 10일", "직장폐쇄 끝", 50), I("3월 18일", "컵스와 5년\n8500만 달러", 50, "gold")], chain="szt")
SC['n8'] = KEEP(SC['n6']); SC['n8']['items'][2]['at'] = 0.3
SC['n8b'] = KEEP(SC['n8'])
SC['n9'] = KEEP(SC['n8b']); SC['n9']['items'][3]['at'] = 0.2; SC['n9']['items'][4]['at'] = 1
SC['n9b'] = KEEP(SC['n9'])
SC['n21'] = PSS("사토", "사토 테루아키", "", "2026년 겨울 · 일본 포스팅", [STT("함께 포스팅", "사토 등 3명", 1.2, True)], imgAt=1)
SC['n12'] = PSt("노시환", "노시환", "한화", "2026년 · 포스팅", [VST("스즈키처럼 기다릴 수 없음", at=0.6, c="bad")])
# 노시환 갈림길: 메이저리그 ↔ 한화
def _BR(at=0): return [ND("pl", 420, 610, "player", "노시환", at=at), ND("mlb", 1400, 400, "team", "메이저리그 구단", at=at), ND("hw", 1400, 780, "kbo", "한화", "11년 307억 계약", at=at)]
SC['n14'] = FL("", _BR(), [ED("pl", "mlb", "마감 전 계약", 1, c="gold", r0=120, r1=140)], isz=1.2, chain="nbr")
SC['n14']['nodes'][2].update(expAt=2.6, stamp="없던 일")
SC['n16'] = FL("", _BR(-1), [ED("pl", "mlb", "계약 실패", 0, stopAt=0.5, r0=120, r1=140)], isz=1.2, chain="nbr")
SC['n17'] = KEEPF(SC['n16']); SC['n17']['edges'].append(ED("pl", "hw", "복귀", 0.3, okAt=0.7, r0=120, r1=140))
SC['n18'] = KEEPF(SC['n17'], cap="2027년 11월 1일까지 다시 포스팅 못 함", capC="bad", capAt=0.3, capY=170)
# 노시환 성적: 기록 타일
SC['n22'] = PSS("노시환3", "노시환", "한화", "2026년 성적", [STT("경기", "127", 50), STT("타율", "2할 8푼 3리", 50), STT("홈런", "29", 50), STT("타점", "96", 50, True)], chain="ns23")
SC['n23'] = KEEP(SC['n22'])
for _i, _a in enumerate([0.2, 1, 2, 2.4]): SC['n23']['stats'][_i]['at'] = _a
# 미국 구단 제안 전망: 금액·기간 막대
SC['n25'] = PAY([B(.9, 0, lab="한화 · 금액", c="gold"), B(.5, 1, lab="미국 · 금액"), B(.9, 0, lab="한화 · 기간", c="gold"), B(.35, 2, lab="미국 · 기간")], [],
                tags=[dict(i=1, lab="더 적게", c="bad", at=1.2), dict(i=3, lab="더 짧게", c="bad", at=2.2)], cap="미국 구단 제안 · 언론 전망", capAt=0, x0=330, x1=1590)
# 3루수 부족 → 노시환에게 유리
SC['n25b'] = FL("", [ND("t1", 400, 380, "team", "", "주전 3루수?", at=0.8, subC="bad"), ND("t2", 400, 620, "team", "", "주전 3루수?", at=0.9, subC="bad"), ND("t3", 400, 860, "team", "", "주전 3루수?", at=1, subC="bad"), ND("pl", 1400, 620, "player", "노시환", at=0.2)],
                [ED("t1", "pl", "", 2, c="gold", r0=110, r1=120), ED("t2", "pl", "", 2.05, c="gold", r0=110, r1=120), ED("t3", "pl", "", 2.1, c="gold", r0=110, r1=120)], cap="노시환에게 유리 · 분석", capAt=2.2, capY=160, isz=1.0)
SC['n26'] = FL("", _BR(), [ED("pl", "mlb", "", 0.2, r0=120, r1=140), ED("pl", "hw", "더 높음", 0.6, c="gold", r0=120, r1=140)], isz=1.2, cap="한국 복귀 가능성 · 언론 전망", capAt=0.8, capY=170)
SC['n26']['nodes'][2]['hiAt'] = 0.8
SC['n27'] = PSS("노시환4", "노시환", "한화", "언론 분석", [STT("약점", "삼진", 0.3), STT("2026년", "147삼진 · 개인 최다", 50, True)], chain="n27")
SC['n27b'] = KEEP(SC['n27']); SC['n27b']['stats'][1]['at'] = 0.2
SC['n27c'] = SC['n27c']   # (빌드업 · 류지현 사진)
# 김하성: 기록 타일
SC['k1'] = PSS("김하성", "김하성", "", "오후 2시 마감 · FA 유격수", [STT("FA", "3년 연속", 50), STT("2026년 애틀랜타", "1년 2000만 달러", 50), STT("1월 부상", "오른손 중지 수술", 50), STT("2026년 · 51경기", "타율 1할 1푼 6리", 50)], chain="kim")   # 11/13 00:55 "목차에 다 있는데 김하성인걸 공개하는 것마냥 — 짜친다" → 공개 연출(imgAt) ✗, 처음부터 사진
SC['k2'] = KEEP(SC['k1']); SC['k2']['stats'][0]['at'] = 0.3
SC['k2c'] = KEEP(SC['k2']); SC['k2c']['stats'][1]['at'] = 1
SC['k3'] = KEEP(SC['k2c']); SC['k3']['stats'][2]['at'] = 0.6
SC['k4'] = KEEP(SC['k3']); SC['k4']['stats'][3]['at'] = 0.5
SC['k5a'] = KEEP(SC['k4'])
SC['k5'] = PSS("김하성", "김하성", "", "애틀랜타의 선택", [STT("애틀랜타", "퀄리파잉 오퍼 안 줌", 1), STT("언론", "재능은 최고의 FA", 50), STT("언론 예상", "1년 1000만 달러", 50, True)], chain="kim3")
SC['k7'] = KEEP(SC['k5']); SC['k7']['stats'][1]['at'] = 1; SC['k7']['stats'][2]['at'] = 3
SC['k11'] = FL("", [ND("pl", 420, 640, "player", "김하성", at=0), ND("st", 960, 640, "stadium", "직장폐쇄", at=0.2, lockAt=0.5), ND("gh", 1500, 640, "ghost", "새 팀", at=0.8)],
               [ED("pl", "gh", "행선지 찾기", 1, c="gold", bend=-230, r0=120, r1=110)], cap="길어질 수 있음 · 언론 전망", capAt=2, capC="bad", capY=860)
SC['k10'] = S(0, "rf_bars", title="", items=[dict(label="제때 계약한 FA", v=6, txt="캠프 다 치름", at=1), dict(label="3월에 계약한 FA", v=2, txt="캠프 짧게", at=2, hi=True)], max=8, noCenter=True)
# 벡·왓슨·와이스: 기록 타일
SC['f10'] = PSS("벡", "트리스탄 벡", "LG", "LG 트윈스 · 새 외국인 투수", [STT("LG 계약", "11월 5일", 0.2), STT("총액", "87만 8천 달러", 2, True), STT("2026년", "샌프란시스코", 50), STT("최고 구속", "158km", 50, True)], imgAt=1, chain="beck")
SC['f11'] = KEEP(SC['f10']); SC['f11']['stats'][2]['at'] = 0.3; SC['f11']['stats'][3]['at'] = 1.2
SC['f14'] = PSS("왓슨", "트로이 왓슨", "한화", "한화 이글스 · 새 외국인 투수", [STT("한화 계약", "11월 11일", 0.2), STT("총액", "100만 달러", 2, True), STT("2026년 7월", "한화 등 KBO 관심", 50)], imgAt=1, chain="wat0")
SC['f15'] = KEEP(SC['f14']); SC['f15']['stats'][2]['at'] = 0.3
SC['f19'] = PSS("와이스2", "와이스", "한화", "전 한화 투수", [STT("샌디에이고 계약", "11월 11일", 50, True), STT("계약", "1년 185만 달러", 50), STT("옵션", "2028년 구단 옵션", 50), STT("직장폐쇄 전", "메이저리그 자리", 50, True)], chain="wei")
SC['f20'] = KEEP(SC['f19']); SC['f20']['stats'][0]['at'] = 0.3
SC['f21'] = KEEP(SC['f20']); SC['f21']['stats'][1]['at'] = 0.2; SC['f21']['stats'][2]['at'] = 1
SC['f21b'] = KEEP(SC['f21']); SC['f21b']['stats'][3]['at'] = 0.2
# 페라자: 한화와 결별 → 새 타자 찾기
SC['fh1'] = FL("", [ND("pf", 420, 640, "player", "페라자", at=0), ND("hw", 960, 640, "kbo", "한화", at=0), ND("gh", 1500, 640, "ghost", "새 외국인 타자", at=1.2)],
               [ED("hw", "pf", "결별", 0.3, stopAt=0.9, r0=130, r1=110), ED("hw", "gh", "찾는 중", 1.5, c="gold", r0=130, r1=110)])
# 목차 장면은 바뀐 앞 장면을 다시 이어받음 · 다음 영상도 그림으로
SC['n0'] = dict(KEEP(SC['l12']), toc=SC['n0']['toc'])
SC['f0'] = dict(KEEPF(SC['k11']), toc=SC['f0']['toc'])
SC['e4'] = FL("다음 영상", [ND("doc", 960, 340, "doc", "KBO FA 공시 명단", at=0.2, c="gold")] + [ND("e%d" % i, 560 + 200 * (i % 5), 560 if i < 5 else 770, "kbo", t, at=1 + 0.05 * i) for i, t in enumerate(_T10)], isz=0.8)
# ── 11/13 01:20 검수본 #3 검수 에이전트 지적 반영
SC['l3c'] = TLn("", [I("1994년 8월 12일", "선수 파업 시작", 0.2, "bad"), I("9월 14일", "월드시리즈 취소", 1, "bad")])
SC['l2']['capY'] = 780; SC['l3']['capY'] = 780; SC['l1']['capY'] = 780
SC['l3x']['cap'] = "롭 맨프레드 커미셔너 · 2021년 12월 2일"
SC['l5d']['edges'] = [dict(e, r0=190, labDy=60) for e in SC['l5d']['edges']]
SC['l5d']['nodes'][0].update(lab="구단", y=340); SC['l5d']['edges'] = [dict(e, lab='') for e in SC['l5d']['edges']]; SC['l5d']['nodes'][1]['y'] = 720; SC['l5d']['nodes'][2]['y'] = 720
SC['l5d']['nodes'][1]['sub'] = "직장폐쇄로 묶임"; SC['l5d']['nodes'][2]['sub'] = "직장폐쇄와 상관없음"
SC['l5e'] = FL("", [ND("ros", 560, 620, "roster", "40인 로스터", at=0.2), ND("kbo", 1360, 620, "kbo", "KBO 외국인 영입", at=2)], [ED("ros", "kbo", "", 2.2, c="gold")])
SC['l7'] = TLn("", [I("2021년 12월 2일", "직장폐쇄 시작", 0.7, "bad"), I("2022년 3월 10일", "직장폐쇄 끝\n99일 동안 멈춤", 50, "gold")], chain="tl21")
SC['l8'] = KEEP(SC['l7']); SC['l8']['items'][1]['at'] = 0.2
SC['w0'] = dict(KEEP(SC['l8']), toc=SC['w0']['toc'])
# 샐러리캡 막대: 가장 적게 쓰는 팀은 가장 많이 쓰는 팀의 1/6 안팎(1억 달러 아래)
_PV2 = [.95, .78, .6, .44, .3, .15]
for _k in ('l9', 'l9a', 'l9b', 'l11'):
    for _b, _v in zip(SC[_k]['bars'], _PV2): _b['v'] = _v
SC['l9b']['cap'] = "롭 맨프레드 커미셔너 · 7월"; SC['l9b']['capAt'] = 0; SC['l9b']['capX'] = 735
SC['l10'] = S(0, "rf_bars", title="", items=[dict(label="상한", v=245, txt="2억 4500만 달러", at=1), dict(label="하한", v=171, txt="1억 7100만 달러", at=2)], max=420, noCenter=True)
SC['l10c'] = TLn("", [I("5월 제안", "상한제 바로", 0.2), I("11월 3일 수정안", "2028년부터", 1, "gold")])
# 선수노조 안: 선수 최저 연봉↑ · 적게 쓰는 구단에 세금 (팀 연봉 막대 위 선 ✗)
SC['l11d'] = FL("", [ND("uni", 420, 620, "union", "선수노조", at=0), ND("pl", 1400, 420, "player", "선수", "최저 연봉 ↑", at=0.2, subC="gold"), ND("tm", 1400, 790, "team", "적게 쓰는 구단", "세금", at=1.4, subC="bad")],
                [ED("uni", "pl", "", 0.3, c="gold", r0=140, r1=120), ED("uni", "tm", "", 1.5, c="bad", r0=140, r1=130)], isz=1.2)
SC['l11a'] = KEEPF(SC['l11d'])
SC['n2'] = TLn("", [I("11월 2일 밤 10시", "협상 시작", 0.7), I("12월 2일 아침 7시", "협상 마감\n규정상 30일", 2, "gold")])
SC['n4']['gap']['at'] = 2
SC['n10'] = TLn("", [I("2021년", "멈춤", 0, "bad"), I("2026년", "멈추지 않음 · 언론 전망", 1, "gold")], chain="p26")
SC['n11'] = KEEP(SC['n10']); SC['n11']['items'][1]['t'] = "멈추지 않음\n직장폐쇄 전에 계약해야"; SC['n11']['items'][1]['at'] = 0.3
SC['n12']['viz'][0]['at'] = 1
SC['n14']['nodes'][2]['expAt'] = 3
SC['n21'].pop('imgAt', None)
SC['n18b']['edges'] = [dict(e, r1=170, lab=e.get('lab', '').replace('→', '').strip()) for e in SC['n18b']['edges']]
for _e in SC['n18b']['edges']:
    if _e['b'] == 'hh': _e['labDy'] = -100; _e['lab'] = '보장 금액의 20% = 이적료'
SC['n18c'] = KEEPF(SC['n18b'], cap="2500만 달러 이하", capX=560, capY=780); SC['n18c']['capAt'] = 0.2
# 미국 구단 제안: 근거 있는 건 '더 적게·더 짧게'뿐 → 미국 막대는 점선(?)
for _i in (1, 3): SC['n25']['bars'][_i].update(ghost=True)
SC['n27c'] = KEEP(SC['n27b'])
SC['n28'] = copy.deepcopy(_o28)
SC['n20'] = TLn("", [I("2021년 12월 1일", "하루 계약\n14억 달러", 1, "gold"), I("12월 2일", "직장폐쇄 시작", 0.2, "bad")])
SC['k6'] = FL("퀄리파잉 오퍼", [ND("tm", 520, 620, "team", "원래 구단", at=0.3), ND("fa", 1400, 620, "player", "떠나는 FA 선수", at=0.6)], [ED("tm", "fa", "1년 약 2315만 달러", 2, c="gold", r0=150, r1=130)], cap="1년짜리 제안", capAt=3)
SC['k10'] = S(0, "rf_bars", title="", items=[dict(label="제때 계약한 FA", v=6, txt="캠프 다 치름", at=0.2), dict(label="3월에 계약한 FA", v=2, txt="캠프 짧게", at=1.5, hi=True)], max=8, noCenter=True)
# KBO 외국인 영입
SC['f3']['edges'] = [dict(e, labDy=-100) for e in SC['f3']['edges']]
SC['f4'] = KEEPF(SC['f3']); SC['f4']['nodes'][2]['at'] = 1
SC['f5'] = KEEPF(SC['f4'], cap="직장폐쇄가 되면 방출까지 멈춤", capC="bad"); SC['f5']['nodes'][1]['lockAt'] = 1; SC['f5']['edges'][0]['stopAt'] = 2; SC['f5']['capAt'] = 2
def _GM(cap, at=0.2):   # 익명 단장 인용: KBO 구단 그림 + 인용(글 상자만 ✗)
    return FL("", [ND("ros", 520, 600, "roster", "메이저리그 40인 로스터", at=0, lockAt=0), ND("kbo", 1400, 600, "kbo", "KBO 구단 단장", "2021년 12월 3일", at=0)], [ED("ros", "kbo", "", 0, stopAt=0)], cap=cap, capAt=at, capY=820)
SC['f6'] = _GM("“소속이 있는 외국인 선수들을 데려올 수 없다”", 2)
SC['f24'] = _GM("“일장일단이 있는 상황이다”", 2)
_P7 = [I("직장폐쇄 무렵", "텍사스 40인\n로스터에서 빠짐", 50, "bad"), I("12월 2일", "직장폐쇄 시작", 0.3, "bad"), I("12월 9일", "외국인 선수 계약", 1, "gold")]
SC['f6x'] = TLn("", _P7, chain="pet")
SC['f7'] = KEEP(SC['f6x'], title="2021년 · 롯데 피터스"); SC['f7']['items'][0]['at'] = 1
SC['f8'] = KEEP(SC['f7']); SC['f8']['items'][2]['t'] = "롯데와 계약"; SC['f8']['items'][2]['at'] = 1
SC['f18'] = dict(SC['f18'], cap=None)
SC['f18b'] = copy.deepcopy(SC['f19']); SC['f18b']['chain'] = "wei"
SC['f19'] = KEEP(SC['f18b'])
SC['f20'] = KEEP(SC['f19']); SC['f20']['stats'][0]['at'] = 0.3
SC['f21'] = KEEP(SC['f20']); SC['f21']['stats'][1]['at'] = 0.2; SC['f21']['stats'][2]['at'] = 1
SC['f21']['stats'] = SC['f21']['stats'][:3]; SC['f20']['stats'] = SC['f20']['stats'][:3]; SC['f19']['stats'] = SC['f19']['stats'][:3]; SC['f18b']['stats'] = SC['f18b']['stats'][:3]
SC['f21b'] = KEEP(SC['f21'])
SC['f6a']['cap'] = None
SC['f6b'] = KEEPF(SC['f6a'], cap="KT 라모스 1명", capC=None); SC['f6b']['capAt'] = 3
for _n in SC['f6b']['nodes']:
    if _n['lab'] == "KT": _n['hiAt'] = 3
    else: _n['dim'] = True
SC['f6c'] = TLn("", [I("12월 2일", "직장폐쇄 시작", 0.2, "bad"), I("2월 1일", "캠프 시작 · 마지노선", 1, "gold")])
SC['l8b'] = TLn("2022년 개막", [I("2022년 3월 1일", "개막 두 시리즈\n취소 발표", 1, "bad"), I("3월 10일", "새 협약\n일정 다시 짬", 2, "gold"), I("개막", "3월 31일\n→ 4월 7일", 50)], chain="op22")
SC['l13b'] = copy.deepcopy(SC['l8b'])
for _it in SC['l13b']['items']: _it['at'] = 50
SC['l13b']['items'][2]['at'] = 1
SC['l8b'] = KEEP(SC['l13b']); SC['l8b']['items'][0]['at'] = 1; SC['l8b']['items'][1]['at'] = 2
SC['l8c'] = KEEP(SC['l8b']); SC['l8c']['items'][2]['at'] = 0.6
# 규칙 검수 반영
SC['l3g'] = KEEPF(SC['l3y'])
SC['k5']['sub'] = "오후 2시 마감 · FA 유격수"; SC['k7']['sub'] = "오후 2시 마감 · FA 유격수"
SC['fh1'] = PSS("페라자", "페라자", "한화", "한화 외국인 타자", [STT("한화와", "결별", 0.8), STT("새 외국인 타자", "찾는 중", 1.4, True)])
SC['fh4']['bubbles'][0]['at'] = 0.3
SC['l13'] = TLn("2027년 개막", [I("3월 중순", "162경기 마지노선", 2, "bad"), I("3월 25일", "개막 예정", 1, "gold")])
for _k in ('f6a', 'f6b'):
    for _n in SC[_k]['nodes']: _n['logo'] = _n['lab']
for _n in SC['e4']['nodes'][1:]: _n['logo'] = _n['lab']
SC['e1']['items'][0]['t'] = "3주도 안 남음"
# 11/13 03:00 사용자 "자막이랑 텍스트 겹치지 않게" — 자막(두 줄 위 끝 y≈878)과 겹친 4곳을 위로 올림
for _k in ('f6', 'f24'):
    for _n in SC[_k]['nodes']: _n['y'] = 500
    SC[_k]['capY'] = 720
for _n, _y in zip(SC['n25b']['nodes'], (300, 520, 740, 520)): _n['y'] = _y
for _k in ('n14', 'n16', 'n17', 'n18', 'n26'):
    if SC.get(_k) and SC[_k].get('type') == 'lo_flow':
        for _n in SC[_k]['nodes']:
            if _n.get('id') in ('pl', 'mlb', 'hw'): _n['y'] = {'pl': 540, 'mlb': 340, 'hw': 700}[_n['id']]

for _k in ('k11', 'f0'):
    for _n in SC[_k]['nodes']: _n['y'] = 560
    SC[_k]['capY'] = 760

TITLES = {'o4': "12월 2일", 'o4b': "", 'l1': "", 'l2': "", 'l3': "", 'l3b': "", 'l3c': "1994년", 'l3w': "", 'l3x': "", 'l3y': "", 'l3h': "", 'l4': "",
          'l5': "", 'l5y': "", 'l5x': "", 'l5a': "", 'l5b': "", 'l5c': "", 'l5d': "", 'l5e': "", 'l6': "", 'l6b': "", 'l6c': "",
          'l7': "2021년 직장폐쇄", 'l8': "2021년 직장폐쇄", 'w0': "2021년 직장폐쇄", 'l7b': "", 'l9': "", 'l9b': "맨프레드 커미셔너 · 7월",
          'l10': "구단주 제안 · 10월 8일", 'l10e': "계약 기간 상한", 'l10c': "상한제 시작 시점", 'l12': "", 'n0': "",
          'c1': "12월 2일 아침 7시", 'c2': "12월 2일 오후 2시", 'c4': "2월 1일", 'c5': "3월 중순", 'e0': "", 'e0e': "",
          'n2': "노시환 협상 기간", 'n10': "직장폐쇄 중 협상 기간", 'n11': "직장폐쇄 중 협상 기간", 'n18b': "", 'n18c': "", 'n24b': "포스팅 선배들",
          'c2b': "", 'n20': "2021년 12월", 'k9': "김하성 계약 시간표", 'k9b': "프레디 프리먼 · 2021~22년", 'c3': "", 'f3': "", 'f4': "", 'f5': "",
          'f7': "롯데 피터스 · 2021년", 'f8': "롯데 피터스 · 2021년", 'f9': "2026년 겨울", 'f13': "", 'f16': "트로이 왓슨", 'f17': "트로이 왓슨", 'f18': "트로이 왓슨",
          'fh3': "한국 시간 · 12월 2일", 'fh3b': "한국 시간 · 12월 2일", 'f6b': "2021년 겨울", 'f6c': "2021년 겨울", 'f22': "", 'f23': "", 'f25': "새 외국인 선수 첫해",
          'l8b': "2022년 개막", 'l8c': "2022년 개막", 'e0b': "한국 시간 · 12월 2일", 'e0c': "한국 시간 · 12월 2일", 'e1': ""}
for _k, _t in TITLES.items():
    _s = SC[_k]
    if _s.get('type') == 'rf_band' or 'who' in _s: _s['who'] = _t
    else: _s['title'] = _t
SC['f5']['cap'] = "방출까지 멈춤"
# 11/13 00:01 사용자 "좌측 상단이 너무 자주 바뀌어 집중을 흐트러뜨림" → 장면 제목은 꼭 필요한 곳(시계 기준 시각·사람 이름·용어·팬 반응·다음 영상)만 남기고 모두 뺌
KEEP_T = {'l13', 'n5', 'n5b', 'l13b', 'l8b', 'l8c', 'o1', 'o2', 'o3', 'n4', 'fh3', 'fh3b', 'e0b', 'e0c', 'l9b', 'k9b', 'f7', 'f8', 'k6', 'e4', 'nf2', 'nf3', 'nf4', 'k0', 'fh4', 'g0'}
for _k, _s in SC.items():
    if _k in KEEP_T: continue
    if _s.get('type') in ('rf_band',) or 'who' in _s: _s['who'] = ""
    if 'title' in _s and _s.get('type') not in ('question',): _s['title'] = ""

missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing, missing
for _k in extra: SC.pop(_k)
lines, scenes = [], []
for j, (k, sub) in enumerate(LINES):
    sc = copy.deepcopy(SC[k]); sc['startLine'] = j; sc.setdefault('bg', BG_NEU)
    lines.append(L(NARR(sub), sub)); scenes.append(sc)
for _i in range(1, len(scenes)):   # 11/13 02:45 사용자 "같은 장면인데 깜빡인다" → 이어받는(cont) 그림 장면은 앞 장면과 같은 chain 으로 묶어 전환 없이
    _a, _b = scenes[_i - 1], scenes[_i]
    if _b.get('cont') and _a['type'] == _b['type'] and not (_a.get('chain') and _a.get('chain') == _b.get('chain')):
        _a.setdefault('chain', 'ck%d' % _i); _b['chain'] = _a['chain']
for _i in range(1, len(scenes)):   # 같은 로고 질문 장면은 이어받기
    _a, _b = scenes[_i - 1], scenes[_i]
    if _a['type'] == _b['type'] == 'question' and _a.get('logos') == _b.get('logos'):
        _a.setdefault('chain', 'lk%d' % _i); _b['chain'] = _a['chain']; _b['cont'] = True
def _extra_pics(o, acc):
    if isinstance(o, dict):
        for k_, v_ in o.items():
            if k_ in ('img', 'img2', 'faces', 'poster', '_pics', 'bg'): continue
            if isinstance(v_, str) and re.match(r'^(경기|KBO프로필|MLB|인물|카드)/', v_): acc.append(v_)
            else: _extra_pics(v_, acc)
    elif isinstance(o, list):
        for v_ in o: _extra_pics(v_, acc)
for _s in scenes:
    _a = []; _extra_pics(_s, _a)
    if _a: _s['_pics'] = [{'img': x} for x in dict.fromkeys(_a)]
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})
scenes.append(dict(END_SC, startLine=len(lines) - 1, bg=BG_NEU))

CH = [{"key": t, "title": t, "from": KEYS.index(a), "to": KEYS.index(b)} for t, a, b in CHAPS]
DESC = ("MLB가 12월 2일 직장폐쇄로 멈추면, 노시환·김하성과 KBO 외국인 영입은 어떻게 될까요?\n\n"
        "MLB 노사협약이 미국 동부 시간 12월 1일 밤(한국 시간 12월 2일 오후 2시 무렵) 끝나요. 새 협약이 없으면 구단주들이 직장폐쇄에 들어갈 수 있고, 그러면 FA 계약과 트레이드, 40인 로스터 선수의 이적이 모두 멈춰요.\n\n"
        "한화 노시환의 포스팅 협상 마감은 한국 시간 12월 2일 아침 7시로, 노사협약이 끝나기 7시간 전이에요. 2021년 스즈키 세이야 때는 협상 기간이 멈췄다가 직장폐쇄가 끝난 뒤 이어졌지만, 2026년엔 멈추지 않는다는 보도가 나왔어요. "
        "3년 연속 FA인 김하성은 노사협약이 끝나는 오후 2시 전에 계약하지 못하면 직장폐쇄가 끝날 때까지 기다려야 해요.\n\n"
        "KBO 구단의 외국인 선수 영입도 영향을 받아요. 메이저리그 40인 로스터 선수는 직장폐쇄 중 방출까지 멈추기 때문이에요. LG 트리스탄 벡, 한화 트로이 왓슨 영입 사례와 2021년 직장폐쇄 때 KBO 외국인 시장도 함께 정리했어요.")
TAGS = ["MLB 직장폐쇄", "직장폐쇄", "노사협약", "노시환 포스팅", "김하성 FA", "메이저리그 포스팅", "KBO 외국인 선수", "트로이 왓슨", "트리스탄 벡", "40인 로스터", "샐러리캡", "스토브리그", "프로야구", "야구자판기"]
EP = {"theme": "mg", "mgWord": "MLB LOCKOUT", "introChapter": "오프닝", "date": "2026-11-12", "gameDate": "2026-11-12", "series": "야구롱폼", "focusTeam": "한화", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1112-lo-v1", "topic": "MLB직장폐쇄", "endcardSec": 10, "gapScale": 1.15, "pauseMax": 0.35, "ttsCharsOk": 6000,
      "chapters": CH, "toc": TOC, "tocTitle": "목차", "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": "근거 = 프로젝트 claude/MLB직장폐쇄-근거-1112.md",
      "youtube": {"title": "MLB 직장폐쇄 12월 2일 멈추나 | 노시환·김하성·KBO 외국인 영입까지", "description": DESC, "tags": TAGS,
                  "cta": "메이저리그가 12월 1일 전에 새 협약을 맺을까요? 아니면 직장폐쇄로 멈출까요? 여러분은 어떻게 보세요?",
                  "prev": "삼성 2027 스토브리그 | 우승 주역 원태인·구자욱 남을까?",
                  "hashtags": ["#MLB직장폐쇄", "#노시환", "#김하성", "#포스팅", "#외국인선수", "#프로야구", "#KBO", "#야구자판기"],
                  "teams": ["한화 이글스", "LG 트윈스", "롯데 자이언츠", "KT 위즈"],
                  "players": ["노시환", "김하성", "트리스탄 벡", "트로이 왓슨", "와이스", "페라자", "류지현", "김혜성", "송성문", "스즈키 세이야", "사토 테루아키", "프레디 프리먼", "피터스", "라모스"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'o3', 'n4', 'n10', 'f2', 'e2', 'c1', 'c2', 'c4', 'c5')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    for l in EP['lines'][:-1]:
        if len(l['narr'].split(' / ')) > 1 and len(l['sub'].split('|')[0]) <= 4: l['noMerge'] = True
    for _k in ('n4', 'n9', 'f17'): EP['lines'][KEYS.index(_k)]["holdAfter"] = 0.8
    EP['lines'][KEYS.index('o4')]['gapAfter'] = 0.2; EP['lines'][KEYS.index('o4b')]['holdAfter'] = 0.8
    for _k in TOCAT: EP['lines'][KEYS.index(_k)]["holdAfter"] = 0.6
    _chs = {c['from'] for c in CH}
    for i, l in enumerate(EP['lines'][:-1]):
        sg_ = l['narr'].split(' / ')
        if any(x.rstrip().endswith('?') for x in sg_): l['pauseMax'] = 0.5
        if l.get('holdAfter') is None and l.get('gapAfter') is None and (i + 1) in _chs: l["gapAfter"] = 0.55
    _old = os.path.join(HERE, 'ep_v4_voice.json')   # 11/12 00:47 40인 로스터 줄 추가 → 대사가 같은 옛 줄 음성을 새 번호로(재합성 없음)
    if os.path.exists(_old):
        _on = [l['narr'] for l in json.load(open(_old, encoding='utf-8'))['lines']]
        _vr = []
        for l in EP['lines']:
            _vr.append(_on.index(l['narr']) if l['narr'] in _on else None)
        if any(x is not None and x != j for j, x in enumerate(_vr)): EP['voiceRemap'] = _vr
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-12_롱폼.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
