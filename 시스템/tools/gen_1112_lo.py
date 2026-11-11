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

FIX = [('FA', '에프에이'), ('KBO', '케이비오'), ('MVP', '엠브이피'), ('MLB', '엠엘비'), ('%', ' 퍼센트'), ('LG', '엘지'), ('km', '킬로')]
def NARR(sub):
    n = sub
    for a, b in FIX: n = n.replace(a, b)
    n = narr_of(n)
    n = re.sub(r'([일이삼사오육칠팔구십]+) 월 ([일이삼사오육칠팔구십]+) 일', r'\1월 \2일', n)
    n = re.sub(r'(?<![가-힣])((?:[이삼]?십)?[일이삼사오육칠팔구]?|[이삼]?십) 일(?=까지|에|부터|엔|에도| )', lambda m: m.group(1) + '일' if m.group(1) else m.group(0), n)
    NAT = {'일': '한', '이': '두', '삼': '세', '사': '네', '오': '다섯', '육': '여섯', '칠': '일곱', '팔': '여덟', '구': '아홉', '십': '열', '십일': '열한', '십이': '열두'}
    n = re.sub(r'(?<![가-힣])(십이|십일|십|[일이삼사오육칠팔구])시(?=간|부터|까지|엔|예요|보다|를|에|이|가|는|$| )', lambda m: NAT[m.group(1)] + ' 시', n)
    n = re.sub(r'(?<![가-힣])(십이|십일|십|[일이삼사오육칠팔구]) 월', r'\1월', n)
    n = n.replace('삼십사쪽', '삼십사 쪽').replace('팔일 뒤', '팔 일 뒤').replace('삼진으로', ' 삼진으로').replace('삼 루수', '삼루수').replace('삼 루 ', '삼루 ').replace('삼주', '삼 주')
    n = n.replace(' 퍼센트', '퍼센트').replace('  ', ' ')
    return n
KEYS = [k for k, _ in LINES]
ALL10 = ["KIA", "KT", "LG", "NC", "SSG", "두산", "롯데", "삼성", "키움", "한화"]
P.update({"노시환": "카드/FA11_노시환_한화", "노시환2": "카드/FA11_노시환_한화", "와이스2": "카드/FA9_와이스_한화", "김하성": "MLB/김하성", "류지현": "경기/류지현_취임_한화_사용자제공",
          "염경엽": "경기/염경엽_덕아웃_1014_LG제공", "차명석": "인물/차명석_스포츠서울", "와이스": "경기/와이스_모자_0423_한화제공",
          "벡": "경기/벡_계약_1105_LG제공", "왓슨": "경기/왓슨_계약_1111_한화제공"})
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
SC = {}
# 11/12 02:30 영상 검수 1차(내용 A·B·C + 규칙) 반영판: 말하는 호흡에 그 값, 첫 호흡에도 그 호흡의 값, 이름 부르면 사진, 글만 있는 띠 → 흐름 그림(steps)·연표·막대·시계
P.update({"김혜성": "카드/P29c_김혜성_다저스", "송성문": "카드/P29c_송성문_SD", "페라자": "카드/FA9_페라자", "스즈키": "카드/P29w_스즈키_컵스", "사토": "일본대표/사토"})
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
SC['o2'] = KEEP(SC['o1'], title="미국 동부 12월 1일 밤 = 한국 12월 2일 오후 2시")
SC['o3'] = KEEP(SC['o2'], title="한국 시간 · 12월 2일"); SC['o3']['marks'][0]['at'] = 1
SC['o4'] = DUOT("12월 2일 · 한국 야구의 마감", [DCT("노시환", "노시환", "한화", 0, [dict(k="아침 7시", v="포스팅 협상 마감", at=0.2, hi=True)]), DCT("김하성", "김하성", "", 1, [dict(k="오후 2시", v="FA 시장", at=1, hi=True)])])
SC['o4b'] = CLK("한국 시간 · 12월 2일 오후 2시", [MK(7, "오전 7시", "노시환 협상 마감", 0), MK(14, "오후 2시 무렵", "KBO 외국인 영입 창구", 0.2, "bad")])
SC['o5'] = CD("마감 · 시간 순서대로", ats=[-1, -1, 1, 1.4], chain="cd0")
# ── 직장폐쇄가 뭐길래
SC['l1'] = BF("노사협약", [it("구단주", 0.2), it("선수노조", 0.5, join="+"), it("리그 운영 규칙", 1, join="=", hi=True, w=420)])
SC['l2'] = BF("노사협약이 끝나면", [it("노사협약 만료", 0.2, w=300), it("새 협약 없음", 0.6, w=270), it("구단주 문 닫음", 1, hi=True, w=300)], chain="lk")
SC['l3'] = KEEP(SC['l2']); SC['l3']['fig']['items'][2]['hi'] = False; SC['l3']['fig']['items'].append(dict(lab="직장폐쇄", at=0.2, join="=", hi=True, w=250))
SC['l3b'] = BN("직장폐쇄와 파업", [V("파업", "선수 쪽", 0.2, size=120), V("직장폐쇄", "구단주 쪽", 1, hi=True, size=120)])
SC['l3c'] = TLn("1994년 · 선수 파업", [I("8월 12일", "선수 파업 시작", 0.2, "bad"), I("9월 14일", "월드시리즈 취소", 1, "bad")])
SC['l4'] = ROS("직장폐쇄가 되면 · 멈추는 것", "메이저리그 구단 40인 로스터", cap="FA 계약 · 트레이드 멈춤", capC="bad", capAt=0.6, chain="ros1")
SC['l5'] = dict(SC['l4'], title="직장폐쇄가 되면 · 멈추는 범위", cap="선수 전부는 아님", capC=None, capAt=1)
SC['l5y'] = dict(SC['l5'], cap="기준은 40인 로스터", capAt=0.2)
SC['l5x'] = dict(SC['l5y'], title="40인 로스터 · 구단이 계약해 둔 40명", cap=None, capAt=None)
SC['l5a'] = dict(SC['l5x'], title="40인 로스터 · 경기에 나서는 26명도 이 안에서", hiN=26, hiAt=0.4, cap="메이저리그 경기 26명", capAt=0.6)
SC['l5b'] = dict(SC['l5a'], title="40인 로스터 · 선수노조 조합원", hiN=0, hiAt=-1, mode="lock", at=0.6, cap="직장폐쇄 대상", capC="bad", capAt=1)
SC['l5c'] = dict(SC['l5b'], title="40인 로스터 · 거래가 모두 멈춤", at=-1, cap="트레이드 · 웨이버 · 방출 멈춤", capAt=0.6)
SC['l5d'] = BF("40인 로스터 밖", [it("마이너리그 선수", 0.2, w=360), it("직장폐쇄 대상 아님", 2, hi=True, w=400), it("마이너 계약 가능", 3, w=360)])
SC['l5e'] = BF("뒤에서 다시", [it("40인 로스터", 0.2), it("KBO 외국인 영입", 1, hi=True, w=420)])
SC['l6'] = BF("직장폐쇄 지침", [it("구단 직원", 0.2), it("선수", 0.5), it("크리스마스 카드 금지", 1, hi=True, w=460)], vals=[V("34쪽", "지침", 2, size=110)])
SC['l6b'] = BF("직장폐쇄 중에는", [it("구단 시설 훈련 금지", 0.2, w=440), it("홈페이지 선수 사진 · 영상 내림", 1.7, join="·", hi=True, w=620)])
SC['l6c'] = BF("직장폐쇄 중에도", [it("일본 리그 등", 0.2, w=320), it("다른 리그 출전 가능", 2, hi=True, w=420)])
SC['l7'] = TLn("지난 직장폐쇄 · 2021~22년", [I("2021년 12월 2일", "직장폐쇄 시작", 0.7, "bad"), I("2022년 3월 10일", "직장폐쇄 끝", 50), I("99일", "멈춘 기간", 50, "gold")], chain="tl21")
SC['l7b'] = BF("2021년 · 구단주 결정", [it("구단주 투표", 0.2), it("만장일치", 1, hi=True), it("직장폐쇄", 1.4)])
SC['l8'] = KEEP(SC['l7']); SC['l8']['items'][1]['at'] = 0.2; SC['l8']['items'][2]['at'] = 1
# ── 2026년엔 왜 멈추나
SC['l9'] = BN("2026년 협상 쟁점", [V("샐러리캡", "팀 연봉 상한", 0.3, hi=True)])
SC['l9b'] = BF("롭 맨프레드 커미셔너 · 7월", [it("최다 팀 연봉", 1, w=320), it("최소 팀 연봉", 2, join="−", w=320), it("4억 4100만 달러", 3, join="=", hi=True, w=400)])
SC['l10'] = S(0, "rf_bars", title="구단주 제안 · 10월 8일 · 한 팀 연봉", items=[dict(label="상한", v=245, txt="2억 4500만 달러", at=1.8), dict(label="하한", v=171, txt="1억 7100만 달러", at=3)], max=340, noCenter=True)
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
SC['n14'] = PSt("노시환2", "노시환", "한화", "마감 전에 계약하면", STPS(("마감 전 계약", "메이저리그행", 1, "gold"), ("한화 11년 307억", "없던 일", 2.6, "bad")))
SC['n16'] = PSt("노시환", "노시환", "한화", "계약을 못 하면", STPS(("포스팅", "끝", 0.5, "bad"), ("한화 복귀", "원래 계약 이어 감", 50, None), ("2027년 11월 1일까지", "다시 포스팅 못 함", 50, "bad")), chain="nc2")
SC['n17'] = KEEP(SC['n16']); SC['n17']['viz'][0]['items'][1]['at'] = 0.3
SC['n18'] = KEEP(SC['n17']); SC['n18']['viz'][0]['items'][2]['at'] = 0.3
SC['n18b'] = BF("계약이 되면 · 한화가 받는 이적료", [it("한화 이적료", 0.2, w=320), it("노시환 보장 금액", 1, join="=", w=380), it("20%", 1.4, join="×", hi=True, w=200)], team="한화", chain="fee")
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
SC['k10'] = PSt("김하성", "김하성", "", "직장폐쇄가 3월까지 가면", STPS(("3월까지", "직장폐쇄", 0.2, "bad"), ("팀 못 찾은 FA", "김하성처럼", 1, None), ("새 팀 캠프", "짧게", 2, "bad")))
# ── 날짜 정리
SC['e0'] = CD("날짜로 다시 정리")
SC['e0b'] = CLK("날짜로 정리 · 한국 시간 12월 2일", [MK(7, "오전 7시", "노시환 협상 마감", 0.3), MK(14, "오후 2시 무렵", "FA · 40인 이적 멈출 수도", 50, "bad")], chain="clk3")
SC['e0c'] = KEEP(SC['e0b']); SC['e0c']['marks'][1]['at'] = 0.6
SC['e0e'] = CD("멈추면 · 남는 시간", hl=(2, 3))
SC['e1'] = BN("노사협약 만료까지", [V("12월 2일", "오후 2시", 0.2, size=110), V("3주도 안 남음", "", 1, hi=True, size=110)])
SC['e2'] = Q("12월 1일 전 새 협약? · 아니면 직장폐쇄?", [], chain="eq")
SC['e3'] = KEEP(SC['e2'])
SC['e4'] = BN("다음 영상", [V("KBO FA 공시 총정리", "10개 구단별로", 1, hi=True)])
# 11/12 00:28 사용자: 목차는 말로 읽지 않고 화면으로 — 오프닝 끝에 전체, 챕터가 바뀔 때마다 지금 칸 강조(말 없는 holdAfter 동안)
TOC = ["직장폐쇄가 뭐길래", "2026년엔 왜 멈추나", "아침 7시 · 노시환 협상 마감", "오후 2시 · FA 시장과 김하성", "오후 2시 · KBO 외국인 영입 창구", "멈춘 뒤 · 2월 1일과 3월 중순", "날짜 정리"]
TOCAT = {'o5': (0, 3.0, 1.5), 'l8': (1, 2.4, .35), 'l12': (2, 2.4, .35), 'nf4': (3, 2.4, .35), 'k11': (4, 2.4, .35), 'fh4': (5, 2.4, .35), 'k10': (6, 2.4, .35)}
for _k, (_hi, _sec, _ha) in TOCAT.items(): SC[_k] = dict(SC[_k], toc=dict(hi=_hi, sec=_sec, hiAt=_ha))
missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing, missing
for _k in extra: SC.pop(_k)
lines, scenes = [], []
for j, (k, sub) in enumerate(LINES):
    sc = copy.deepcopy(SC[k]); sc['startLine'] = j; sc.setdefault('bg', BG_NEU)
    lines.append(L(NARR(sub), sub)); scenes.append(sc)
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
      "chapters": CH, "toc": TOC, "tocTitle": "영상 순서", "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": "근거 = 프로젝트 claude/MLB직장폐쇄-근거-1112.md",
      "youtube": {"title": "MLB 직장폐쇄 12월 2일 멈추나 | 노시환·김하성·KBO 외국인 영입까지", "description": DESC, "tags": TAGS,
                  "cta": "메이저리그는 12월 1일 전에 새 협약을 맺을까요, 아니면 직장폐쇄로 멈출까요? 댓글로 남겨 주세요.",
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
    _k1 = EP['lines'][KEYS.index('k1')]; _b = _k1['narr'].split(' / '); _b[0] += '..'; _k1['narr'] = ' / '.join(_b); _k1['pauseMax'] = 0.8
    for _k, (_hi, _sec, _ha) in TOCAT.items(): EP['lines'][KEYS.index(_k)]["holdAfter"] = _sec
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
