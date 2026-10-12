# -*- coding: utf-8 -*-
"""10/11 롱폼⑪ 「MLB 직장폐쇄, KBO 외국인 재계약 셈법」 (음성 API · 타입캐스트 줄별 배속 1.2 / 숫자·결론·질문 1.15)
대사 = tools/text_1011_long11.py. 근거 모음 = 프로젝트 claude/1011-롱폼11-직장폐쇄-근거모음.md (대사의 모든 사실은 이 문서의 표에서만).
사진: 롱폼⑨ 카드(카드/FA9_*, 구단 공식 프로필 + 구단 제공 경기 사진) + 노시환 2026 한화 공식 프로필(카드/FA11_노시환, person_card 0.774).
2021년 선수(푸이그·노바·루이즈…)는 출처 있는 사진이 없어 구단 로고 카드(tiles)로.
새 아이콘(icontiles): lock·doc·plane·pause·play — template_long.html·template_long_v.html·tools/scenes_draft_1005.js DICON 에 10/11 추가."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import wrap, S, END, OUT
from text_1011_long11 import TEXT
from gen_1010_long10 import wrap2, L, CTA_LINE, st, bb, stp, vsteps, vtrend, vpoll, vsplit, vstamp, vduo

RED, GOLD, GRAY, GREEN, NAVY = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55", "#3B4A63"
C9 = "카드/FA9_"
P = {k: C9 + k for k in ["페덱", "페덱_환호", "아빌라", "아빌라_완투", "아빌라_포효", "와이스_MLB", "와이스_한화", "이숭용", "이범호", "네일", "올러", "카스트로", "카스트로_홈런"]}
P.update({"노시환": "카드/FA11_노시환", "노시환_한화": "카드/FA11_노시환_한화"})
FACE = {"페덱": "카드/FA9원_페덱P", "아빌라": "카드/FA9원_아빌라", "와이스": "카드/FA9원_와이스", "네일": "카드/FA9원_네일", "올러": "카드/FA9원_올러", "카스트로": "카드/FA9원_카스트로"}
THUMB9 = "상황별/썸네일_롱폼9_외인재계약"
TEAMS10 = ["KT", "삼성", "KIA", "LG", "두산", "SSG", "한화", "롯데", "NC", "키움"]

def prof(i, img, name, sub, stats, **k): return S(i, "profile", img=P[img], name=name, sub=sub, stats=stats, **k)
def pv(i, img, name, sub, viz, **k): return S(i, "profile", img=P[img], name=name, sub=sub, stats=k.pop("stats", []), viz=viz, **k)
def sp(i, img, name, sub, bubbles, **k): return S(i, "speech", img=P[img], name=name, sub=sub, bubbles=bubbles, **k)
def ppl(i, items, **k): return S(i, "people", full=True, items=items, **k)
def pc(img, name, note="", **x): return dict({"img": P[img], "name": name, "note": note}, **x)
def tiles(i, items, **k): return S(i, "tiles", items=items, **k)
def icons(i, items, **k): return S(i, "icontiles", items=items, **k)
def bars(i, items, **k): return S(i, "bars", items=items, **k)
def steps(i, items, **k): return S(i, "steps", items=items, **k)
def toc(i, on, **k): return S(i, "toc", on=on, **k)
def quote(i, text, who, **k): return S(i, "quote", text=text, who=who, **k)
def debate(i, title, left, right, **k): return S(i, "debate", title=title, left=left, right=right, **k)
def it(icon, v, k="", at=0, **x): return dict({"icon": icon, "v": v, "k": k, "at": at}, **x)
def tl(team, v, k="", at=0, **x): return dict({"team": team, "v": v, "k": k, "at": at}, **x)
def sd(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vbranch(frm, items, **k): return dict(type="branch", **{"from": frm}, items=items, **k)
A9, A5 = "10월 9일 기준", "10월 5일 기준"

SC = {}
# ── 훅 0~4
SC[0] = ppl(0, [pc("페덱", "페덱", "삼성 투수", noteAt=1), pc("아빌라", "아빌라", "SSG 투수", noteAt=1), pc("와이스_한화", "와이스", "2025년 한화", noteAt=1), pc("노시환", "노시환", "한화 3루수", noteAt=1)],
            title="MLB 직장폐쇄 → KBO 셈법")
SC[1] = icons(1, [it("calendar", "12월 2일 오후 2시쯤", "노사협약 만료 · 한국 시간", 0, n="12/2", hi=True)], title="메이저리그 노사협약")
SC[2] = bars(2, [{"label": "직장폐쇄 예상", "value": 80, "unit": "명", "hi": True, "at": 0}, {"label": "그 외", "value": 21, "unit": "명", "color": GRAY, "at": 0}], max=101, title="메이저리그 선수 101명 설문")
SC[3] = icons(3, [it("doc", "34쪽 지침", "30개 구단에 발송", 0, n="34", hi=True)], title="직장폐쇄 대응 지침")
SC[4] = S(4, "photo", img=THUMB9, fit="contain", h=600, text="")
# ── 목차 5
SC[5] = toc(5, -1, itemFrom=0)
# ── 1장 직장폐쇄란 6~17
SC[6] = toc(6, 0)
SC[7] = S(7, "lockout", mode="cba", title="메이저리그는 이렇게 굴러간다")
SC[8] = S(8, "lockout", mode="lock", title="직장폐쇄란 — 파업과 반대")
SC[9] = S(9, "lockout", mode="branch", title="협약이 끝나면 두 갈래")
SC[10] = icons(10, [it("lock", "직장폐쇄 쪽", "분위기", 0, color=RED, hi=True)], title="분위기는?")
SC[11] = bars(11, [{"label": "직장폐쇄 예상", "value": 80, "unit": "명", "hi": True, "at": 1}, {"label": "그 외", "value": 21, "unit": "명", "color": GRAY, "at": 1}], max=101, title="선수 101명 설문 · 2026년 6월")
SC[12] = quote(12, "무조건 직장폐쇄를\n원한다", "한 구단 임원 · 10월 7일", fs=72, mark="무조건")
SC[13] = icons(13, [it("doc", "34쪽 지침", "10월 1일 · 30개 구단", 0, n="34", hi=True)], title="직장폐쇄 대응 지침")
SC[14] = icons(14, [it("bills", "샐러리캡", "한 팀 연봉 총액의 상한", 0, n=3, hi=True)], title="가장 큰 쟁점")
SC[15] = debate(15, "샐러리캡", {"label": "구단주", "t": "상한 + 하한\n같이 넣자", "c": "bad", "at": 0}, {"label": "선수노조", "t": "상한은\n안 된다", "c": "good", "at": 1})
SC[16] = icons(16, [it("trophy", "NFL", "샐러리캡 있음", 0), it("trophy", "NBA", "샐러리캡 있음", 0), it("trophy", "NHL", "샐러리캡 있음", 0), it("ball", "MLB", "없음", 1, color=RED, hi=True)], title="북미 4대 프로리그")
SC[17] = steps(17, [sd("2021년 12월 2일", "직장폐쇄\n시작", 1), sd("2022년 3월 10일", "99일 만에\n끝", 2, hi=True)], title="직장폐쇄 · 처음이 아니다")
# ── 2장 멈추는 것 · 안 멈추는 것 18~27
SC[18] = toc(18, 1)
SC[19] = icons(19, [it("doc", "40인 로스터", "메이저 계약 선수 40명", 0, n="40"), it("pause", "FA 계약", "멈춤", 3, color=RED), it("pause", "트레이드", "멈춤", 3, color=RED), it("pause", "구단 ↔ 40인 선수", "야구 얘기 금지", 4, color=RED)], title="멈추는 것 — 40인 로스터 선수의 일")
SC[20] = steps(20, [sd("포스팅", "소속 구단이\n메이저에 내놓음", 1), sd("입찰", "30개 구단\n협상 30일", 3), sd("11월 22일", "히로시마\n포스팅", 5), sd("12월 2일", "MLB·일본 합의\n30일 멈춤", 99, bad=True), sd("3월 18일", "컵스 계약", 99, hi=True)], title="포스팅이란 · 2021년 스즈키 세이야")   # at 99 = 자리만(다음 줄에서 뜸)
SC[21] = steps(21, [sd("포스팅", "소속 구단이\n메이저에 내놓음", 0), sd("입찰", "30개 구단\n협상 30일", 0), sd("11월 22일", "히로시마\n포스팅", 0), sd("12월 2일", "MLB·일본 합의\n30일 멈춤", 0, bad=True), sd("3월 18일", "컵스 계약", 2, hi=True)], title="포스팅이란 · 2021년 스즈키 세이야", cont=True)
SC[22] = icons(22, [it("play", "마이너리그", "그대로 운영", 1, color=GREEN), it("play", "마이너 계약", "40인 밖 선수", 0, color=GREEN, ghost=True), it("plane", "다른 리그 출전", "일본 · 윈터리그", 0, color=GREEN, ghost=True)], title="안 멈추는 것", chain="go")
SC[23] = icons(23, [it("play", "마이너리그", "그대로 운영", 0, color=GREEN), it("play", "마이너 계약", "40인 밖 선수", 1, color=GREEN), it("plane", "다른 리그 출전", "일본 · 윈터리그", 0, color=GREEN, ghost=True)], title="안 멈추는 것", chain="go")
SC[24] = icons(24, [it("play", "마이너리그", "그대로 운영", 0, color=GREEN), it("play", "마이너 계약", "40인 밖 선수", 0, color=GREEN), it("plane", "다른 리그 출전", "일본 · 윈터리그", 1, color=GREEN, hi=True)], title="안 멈추는 것", chain="go")
SC[25] = tiles(25, [tl(t, "", "", 0) for t in TEAMS10[:5]] , title="여기서 KBO가 등장")
SC[26] = icons(26, [it("plane", "메이저 돈 노리던 선수", "밖으로 눈 돌림", 1, color=GREEN), it("lock", "메이저 계약", "KBO 선수 못 데려감", 3, color=RED)], title="메이저리그가 멈추면", chain="start")
SC[27] = icons(27, [it("plane", "메이저 돈 노리던 선수", "밖으로 눈 돌림", 0, color=GREEN), it("lock", "메이저 계약", "KBO 선수 못 데려감", 0, color=RED)], title="메이저리그가 멈추면", chain="start", text="올겨울 셈법의 출발점", textAt=0, size=72)
# ── 3장 2021년 겨울의 KBO 28~44
SC[28] = toc(28, 2)
SC[29] = steps(29, [sd("12월 2일", "직장폐쇄\n시작", 1), sd("2022년 3월 10일", "끝 · 99일", 2, hi=True)], title="2021년 직장폐쇄 · 미국 시간")
SC[30] = icons(30, [it("bills", "14억 달러", "12월 1일 하루 계약", 0, n=5, hi=True)], title="직장폐쇄 직전 계약 러시")
SC[31] = tiles(31, [tl("키움", "푸이그", "", 1)], title="키움 · 푸이그", text="12월 8일 고형욱 단장\n협상 중이라 조심스럽다", textAt=2, size=60)
SC[32] = tiles(32, [tl("키움", "푸이그", "", 1)], title="키움 · 푸이그", cont=True, text="12월 9일\n100만 달러 계약 발표", textAt=1, size=60)   # 이어지는 카드는 dict 를 똑같이(at 포함) — 다르면 다시 뜬다
SC[33] = tiles(33, [tl("키움", "푸이그", "", 1)], title="키움 · 푸이그", cont=True, text="직장폐쇄로 미국 길이 막힌 게\n한국행 배경", textAt=0, size=60)
SC[34] = tiles(34, [tl("SSG", "이반 노바", "MLB 90승 · 100만 달러", 1, hi=True)], title="12월 21일")
SC[35] = icons(35, [it("plane", "일본 · 한국으로", "직장폐쇄로 FA 멈춤", 1, color=GREEN, hi=True)], title="12월 28일 · 미국 보도")
SC[36] = tiles(36, [tl("키움", "푸이그", "한국", 1, hi=True), tl("SSG", "노바", "한국", 1, hi=True), tl("LG", "루이즈", "한국", 1, hi=True), {"v": "기튼스", "k": "일본", "at": 2, "color": GRAY}, {"v": "갈비스", "k": "일본", "at": 2, "color": GRAY}, {"v": "폴랑코", "k": "일본", "at": 2, "color": GRAY}], vsize=56, title="기사에 이름이 나온 선수")
SC[37] = quote(37, "최상급 FA는 직장폐쇄 중에도\n쫓는 구단이 있고\n애매한 선수만 버틸 힘이 없다", "한 에이전트 · 2021년 12월", fs=64, mark="애매한 선수만")
SC[38] = bars(38, [{"label": "100만 달러", "value": 7, "unit": "명", "hi": True, "at": 2}, {"label": "그 외", "value": 10, "unit": "명", "color": GRAY, "at": 2}], max=17, title="2022년 새 외국인 17명")
RES = [("키움", "푸이그", "홈런 21개\n한국시리즈 진출", "hi"), ("KIA", "브리토", "제 몫", "hi"), ("SSG", "노바", "시즌 중 교체", "bad"), ("LG", "루이즈", "27경기 · 퇴출", "bad"),
       ("KT", "라모스", "다친 뒤 방출", "bad"), ("롯데", "피터스", "시즌 중 방출", "bad")]
RES_AT = [1, 0, 0, 1, 0, 1]   # 처음 뜨는 호흡(그 뒤 장면에서도 같은 값 → dict 동일 → 다시 안 뜸)
def res(i, shown, **k):   # shown: 칸별 True/False(False = 이름만, 설명 없음)
    out = []
    for (team, v, kk, c), a, on in zip(RES, RES_AT, shown):
        if not on: out.append(tl(team, v, "", 0))
        else: out.append(tl(team, v, kk, a, **({"hi": True} if c == "hi" else {"color": RED})))
    return tiles(i, out, vsize=56, title="2022년 결과", **k)
SC[39] = res(39, [1, 0, 0, 0, 0, 0])
SC[40] = res(40, [1, 1, 0, 0, 0, 0], cont=True)
SC[41] = res(41, [1, 1, 1, 1, 0, 0], cont=True)
SC[42] = res(42, [1, 1, 1, 1, 1, 1], cont=True)
SC[43] = res(43, [1, 1, 1, 1, 1, 1], cont=True, text="MLB 경력 ≠ 성공", textAt=0, size=72)
SC[44] = toc(44, 3)
# ── 4장 올겨울 셈법 45~80
THREE = lambda a, b, c, hi=None: [it("ball", "붙잡는 팀", "", a, color=GREEN, hi=hi == 0), it("search", "새 선수를 찾는 팀", "", b, hi=hi == 1), it("lock", "위험 요소", "", c, color=RED, hi=hi == 2)]
SC[45] = icons(45, THREE(1, 2, 3), title="올겨울 셈법 · 세 갈래", chain="three")
SC[46] = icons(46, THREE(0, 0, 0, 0), title="올겨울 셈법 · 세 갈래", chain="three", text="12월 2일 넘기면 붙잡는 팀에 유리", textAt=1, size=64)
SC[47] = icons(47, [it("lock", "메이저 계약", "길이 막힌다", 0, color=RED), it("ball", "KBO 잔류", "이유가 커진다", 1, color=GREEN, hi=True), it("plane", "일본 구단", "변수는 남는다", 2, color=GRAY)], title="직장폐쇄가 되면")
SC[48] = prof(48, "페덱", "페덱", "삼성 투수", [st("7월 11일", "삼성 영입", 1), st("13경기", "7승 3패", 2, hi=True), st("평균자책점", "2.95", 3, hi=True)], asof=A9)
SC[49] = pv(49, "페덱", "페덱", "삼성 투수", [vduo([dict(icon="money", v="400만 달러", k="마이애미 1년 보장", at=1), dict(icon="money", v="+ 삼성 연봉", k="방출돼도 둘 다 받는다", c="good", at=3)])])
SC[50] = sp(50, "페덱_환호", "페덱", "삼성 투수", [bb("영입 때 · 이종열 단장", "고를 수 있는 투수 중\n가장 센 카드", 1), bb("9월 5일 · 언론", "재계약 0순위", 3, hi=True)])
SC[51] = pv(51, "페덱_환호", "페덱", "삼성 투수", [vsteps([stp("10월 4일", "담 증세", 0, "bad"), stp("10월 9일", "불펜 3이닝 복귀", 1, "good")], h=220)], asof=A9)
SC[52] = prof(52, "아빌라", "아빌라", "SSG 투수", [st("7월 8일", "40만 달러", 1), st("14경기", "9승 2패", 2, hi=True), st("평균자책점", "1.44", 3, hi=True)], asof=A5)
SC[53] = sp(53, "아빌라_포효", "아빌라", "SSG 투수", [bb("9월 29일", "지금은 SSG에 전념\n나중 일은 그때 가서", 1)])
SC[54] = sp(54, "이숭용", "이숭용", "SSG 감독", [bb("9월 30일", "수단과 방법을 가리지 말고\n잡아 달라", 1, hi=True)])
SC[55] = pv(55, "아빌라_완투", "아빌라", "SSG 투수", [vduo([dict(icon="scout", v="MLB 스카우트", k="8월 · 관전 보도", at=0)])])
SC[56] = pv(56, "아빌라", "아빌라", "SSG 투수", [vbranch("12월 2일 전 메이저 제안 없으면", [dict(t="메이저 계약 길 닫힘", c="bad", at=2), dict(t="SSG가 붙잡기 쉬워진다", c="good", at=3), dict(t="마이너 계약은 열려 있음", c="navy", at=4), dict(t="스트레일리도 2022년 2월 마이너 계약", c="navy", at=6)], fc="bad")])
SC[57] = ppl(57, [pc("네일", "네일", "KIA 투수", noteAt=0), pc("올러", "올러", "KIA 투수", noteAt=0), pc("카스트로", "카스트로", "KIA 타자", noteAt=0)], text="셋 다 붙잡는 쪽", textAt=1, size=64)
SC[58] = ppl(58, [pc("네일", "네일", "가장 안정적", noteAt=1), pc("올러", "올러", "가장 안정적", noteAt=1), pc("카스트로", "카스트로", "KIA에서 뛰고 싶다", noteAt=3)], text="셋 다 붙잡는 쪽", textAt=0, size=64, cont=True)
SC[59] = bars(59, [{"label": "네일", "value": 200, "unit": "만 달러", "at": 0, "img": FACE["네일"]}, {"label": "올러", "value": 120, "unit": "만 달러", "at": 0, "img": FACE["올러"]}, {"label": "카스트로", "value": 100, "unit": "만 달러", "at": 0, "img": FACE["카스트로"]}],
               max=460, title="KIA 3명 몸값 420만 달러 · 한도 460만", text="400만 + 네일 30만 + 올러 20만 + 카스트로 10만", textAt=1, size=52)
SC[60] = prof(60, "와이스_한화", "와이스", "2025년 한화 투수", [st("2025년", "한화", 1), st("2026년", "휴스턴", 1)])
SC[61] = pv(61, "와이스_MLB", "와이스", "휴스턴 투수", [vsteps([stp("2026년", "보장 260만 달러", 1), stp("2027년", "구단 옵션 500만 달러", 2)], h=220)])
SC[62] = prof(62, "와이스_MLB", "와이스", "휴스턴 투수", [st("MLB 9경기", "7.62", 0, bad=True), st("6월 13일", "방출 대기", 2, bad=True), st("트리플A", "5점대", 3, bad=True)], asof=A9)
SC[63] = pv(63, "와이스_MLB", "와이스", "휴스턴 투수", [vduo([dict(icon="pause", v="2027 옵션 포기", k="휴스턴 전망", c="bad", at=1), dict(icon="money", v="바이아웃 50만 달러", k="결별 전망", c="bad", at=2)])])
SC[64] = pv(64, "와이스_MLB", "와이스", "휴스턴 투수", [vsteps([stp("월드시리즈 끝", "5일 안에 옵션 결정", 0), stp("거절되면", "바로 FA", 2, "good"), stp("12월 2일", "협약 만료", 3, "bad")], h=220)])
SC[65] = sp(65, "와이스_한화", "와이스", "2025년 한화 투수", [bb("1월 · 미국 라디오", "언젠가 분명 한국에 다시 갈 것", 1)])
SC[66] = sp(66, "와이스_한화", "와이스", "2025년 한화 투수", [bb("1월 · 미국 라디오", "언젠가 분명 한국에 다시 갈 것", 0), bb("7월 · 아내 헤일리 SNS", "한국이 그립다\n사람 · 음식 · 문화", 1, hi=True)], cont=True)
SC[67] = pv(67, "와이스_한화", "와이스", "2025년 한화 투수", [vduo([dict(icon="money", v="보류권 5년", k="한국 복귀 땐 한화와만", at=0), dict(icon="money", v="100만 달러 상한", k="한화 출신이라 안 받음", c="good", at=3)])])
SC[68] = pv(68, "와이스_한화", "와이스", "2025년 한화 투수", [vbranch("12월 2일 전", [dict(t="메이저 계약 받으면 → 미국", c="bad", at=0), dict(t="못 받으면 → 마이너 or 한국", c="navy", at=2), dict(t="본인 말대로면 → 한화", c="good", at=3)], fc="navy")])
SC[69] = icons(69, THREE(0, 0, 0, 1), title="올겨울 셈법 · 세 갈래", chain="three2")
SC[70] = icons(70, [it("ticket", "조회 1만 2천+", "직장폐쇄라니까 설레네요", 0, hi=True)], title="팬 커뮤니티 글 · 10월 8일")
SC[71] = debate(71, "댓글", {"label": "기대", "t": "오타니 원한다\n(농담)", "c": "good", "at": 0}, {"label": "회의", "t": "계약 중인 선수는 안 온다\nFA도 일본 먼저", "c": "bad", "at": 1})
SC[72] = debate(72, "다른 글 댓글", {"label": "특급", "t": "안 온다", "c": "bad", "at": 0}, {"label": "애매한 급", "t": "200만 달러 받고\n일본으로", "c": NAVY, "at": 1})
SC[73] = quote(73, "최상급 FA는 직장폐쇄 중에도\n쫓는 구단이 있고\n애매한 선수만 버틸 힘이 없다", "한 에이전트 · 2021년 12월", fs=64, mark="최상급 FA는 직장폐쇄 중에도")
SC[74] = icons(74, [it("lock", "윈터미팅 없음", "", 0, color=RED), it("pause", "로스터 그대로", "40인 끝자락도 못 데려옴", 2, color=RED)], title="팬 커뮤니티 글")
SC[75] = icons(75, THREE(0, 0, 0, 2), title="올겨울 셈법 · 세 갈래", chain="three3")
SC[76] = steps(76, [sd("직장폐쇄 중", "KBO 계약", 0), sd("중간 타결", "메이저 복귀\n조항?", 1, bad=True), sd("에이전트", "그 조건을\n넣으려 할 것", 2)], title="팬이 짚은 위험", text="조항 없으면 선수도 안 온다", textAt=99, size=64)   # textAt 99 = 자리만
SC[77] = steps(77, [sd("직장폐쇄 중", "KBO 계약", 0), sd("중간 타결", "메이저 복귀\n조항?", 0, bad=True), sd("에이전트", "그 조건을\n넣으려 할 것", 0)], title="팬이 짚은 위험", cont=True, text="조항 없으면 선수도 안 온다", textAt=1, size=64)
SC[78] = icons(78, [it("bills", "100만 달러 상한", "검증된 선수를 못 데려온다", 1, n=1), it("bills", "교체하면", "한 자리 비용 두 배 가까이", 4, n=2, color=RED)], title="신규 외국인 상한")
SC[79] = icons(79, [it("doc", "보유 제한 완화", "단계적 추진", 1, hi=True), it("calendar", "몇 명 · 언제", "아직 미정", 4, n="?", color=GRAY)], title="KBO 이사회 · 10월 7일")
SC[80] = icons(80, [it("ticket", "외국인 +1?", "팬 제안 · 결정 없음", 1, color=GRAY)], title="팬 커뮤니티 글")
# ── 5장 노시환 포스팅 81~89
SC[81] = toc(81, 4)
SC[82] = prof(82, "노시환", "노시환", "한화 3루수", [st("2월 23일", "한화 계약", 0), st("11년", "최대 307억", 1, hi=True), st("비FA", "다년 계약", 2)])
SC[83] = pv(83, "노시환", "노시환", "한화 3루수", [vsteps([stp("2026시즌 뒤", "포스팅 허용 조항", 0, "good"), stp("한화", "MLB에 내놓을 수 있다", 2), stp("MLB 계약 땐", "11년 계약 파기", 4, "bad")], h=220)])
SC[84] = sp(84, "노시환_한화", "노시환", "한화 3루수", [bb("2월 23일", "한국에서 최고의 선수가 됐을 때\n도전해 보고 싶다", 1)])
SC[85] = sp(85, "노시환_한화", "노시환", "한화 3루수", [bb("2월 23일", "한국에서 최고의 선수가 됐을 때\n도전해 보고 싶다", 0), bb("10월 8일 · 보도", "구단은 동의 · 남은 건 본인 선택", 1, hi=True)], cont=True)
SC[86] = icons(86, [it("pause", "FA", "멈춤", 1, color=RED), it("pause", "트레이드", "멈춤", 1, color=RED), it("pause", "포스팅", "2021년 합의로 멈춤\n한국도 같은 길?", 2, color=RED, hi=True)], title="직장폐쇄가 되면")
SC[87] = steps(87, [sd("11월 1일 ~ 12월 5일", "KBO 포스팅 창", 0, hi=True), sd("11월 22일", "스즈키\n히로시마 포스팅", 2), sd("12월 2일", "MLB·일본 합의\n30일 멈춤", 3, bad=True), sd("3월 18일", "컵스 계약", 4)], title="포스팅 창 · 2021년 스즈키 세이야")
SC[88] = icons(88, [it("ticket", "잔류 유력", "직장폐쇄가 유력하면", 0), it("ticket", "무응찰 가능성", "높다", 1)], title="팬 커뮤니티 글 · 10월 8일")
SC[89] = pv(89, "노시환", "노시환", "한화 3루수", [vbranch("노시환 포스팅", [dict(t="11월 초 포스팅 + 빨리 끝나면 → 진행", c="good", at=1), dict(t="직장폐쇄 길어지면 → 멈춤", c="bad", at=2)], fc="navy")])
# ── 결 90~95
SC[90] = icons(90, [it("pause", "메이저 계약", "", 1, color=RED), it("pause", "트레이드", "", 1, color=RED), it("pause", "포스팅", "", 1, color=RED), it("play", "마이너 계약", "", 3, color=GREEN), it("plane", "다른 리그 출전", "직장폐쇄 기간만", 4, color=GREEN)], title="직장폐쇄가 되면", vsize=64)
SC[91] = icons(91, [it("ball", "붙잡는 팀", "유리해질 수 있다", 0, color=GREEN), it("search", "새 선수 풀", "커질 수 있지만\n특급은 어렵다", 1), it("lock", "중간 타결 조항", "위험", 3, color=RED)], title="올겨울 셈법 · 세 갈래", text="12월 2일 전에 타결되면 원점", textAt=4, size=60)
SC[92] = steps(92, [sd("10월 24일", "월드시리즈\n시작", 1), sd("끝나고 5일 안에", "FA 시장", 2), sd("11월 1일", "KBO 포스팅 창\n시작", 3), sd("11월 30일", "보류선수 명단\n외국인 보류권", 4), sd("12월 2일", "협약 만료", 6, hi=True)], title="앞으로의 날짜")
SC[93] = steps(93, [sd("12월 2일", "직장폐쇄?", 0, bad=True), sd("3월 10일쯤", "99일이면\n여기까지", 1, hi=True), sd("3월 24일", "MLB 개막", 2)], title="2021년처럼 99일이면")
SC[94] = S(94, "question", text="직장폐쇄는 KBO에\n좋은 일일까요? 나쁜 일일까요?", logos=TEAMS10, size=84)
SC[95] = S(95, "question", text="10개 구단 외국인 재계약\n여기를 눌러 확인", img=THUMB9, ph=495, size=72, arrow="left")   # 10/11 사용자: 질문 뒤에, 썸네일을 가리키는 화살표(유튜브 카드 자리)

lines, scenes = [], []
for i, (narr, sub) in enumerate(TEXT):
    lines.append(L(narr, sub))
    sc = SC[i]; assert sc['startLine'] == i, i; scenes.append(sc)
lines[-1]['gapAfter'] = 0.5
lines.append(dict(CTA_LINE))

CH = [("직장폐쇄란", 6, 17), ("멈추는 것 · 안 멈추는 것", 18, 27), ("2021년 겨울의 KBO", 28, 44), ("올겨울 셈법", 45, 80), ("노시환 포스팅", 81, 89)]

TAGS = ["MLB 직장폐쇄", "메이저리그 직장폐쇄", "MLB 파업", "KBO 외국인 선수", "외국인 선수 재계약", "페덱", "아빌라", "와이스", "노시환", "노시환 포스팅", "네일", "카스트로", "푸이그",
        "삼성 라이온즈", "SSG 랜더스", "한화 이글스", "KIA 타이거즈", "프로야구", "KBO", "야구자판기", "2026 프로야구"]
_tl = sum(len(t) + (2 if " " in t else 0) for t in TAGS) + len(TAGS) - 1
assert _tl <= 500, _tl
DESC = ("MLB 직장폐쇄 — 메이저리그 노사협약이 한국 시간 12월 2일 오후 2시쯤 끝나고, 선수 101명 중 80명이 직장폐쇄를 예상했어요. 그러면 KBO 외국인 선수 재계약 셈법은 어떻게 바뀔까요?\n"
        "지난 외국인 재계약 영상에 '직장폐쇄에 따라 셈법이 복잡해 보인다'는 댓글이 있어서 그 부분을 따로 정리했어요.\n\n"
        "먼저 직장폐쇄가 무엇인지(샐러리캡 쟁점, 34쪽 대응 지침, 2021년 99일 직장폐쇄), 직장폐쇄가 되면 무엇이 멈추고 무엇이 안 멈추는지(40인 로스터 선수의 FA·트레이드·포스팅은 멈추고, "
        "마이너리그 계약과 다른 리그 출전은 가능) 설명해요. 2021년 겨울 스즈키 세이야의 포스팅이 멈췄던 일도 함께요.\n\n"
        "그다음 2021년 겨울에 KBO에 실제로 벌어진 일을 봤어요. 키움 히어로즈 푸이그, SSG 랜더스 이반 노바, KIA 타이거즈 브리토, LG 트윈스 루이즈 등이 직장폐쇄 겨울에 한국에 왔고, 2022년 결과는 엇갈렸어요.\n\n"
        "올겨울 셈법은 세 갈래로 봤어요. 붙잡는 팀(삼성 라이온즈 페덱, SSG 랜더스 아빌라, KIA 타이거즈 네일·올러·카스트로), 돌아오는 선수(한화 이글스에서 뛰었던 와이스), 새 선수를 찾는 팀과 위험 요소(팬 커뮤니티 여론, 중간 타결 조항, 100만 달러 상한, KBO 외국인 보유 제한 완화). "
        "마지막으로 한화 이글스 노시환의 포스팅 조항이 직장폐쇄와 어떻게 얽히는지 봤어요.\n\n"
        "야구자판기는 매일 오늘의 야구 이슈를 정리해 드려요.\n\n"
        "직장폐쇄는 KBO에 좋은 일일까요? 나쁜 일일까요? 댓글로 알려 주세요.\n\n"
        "사진: 구단 공식 선수 프로필 — 삼성 라이온즈·SSG 랜더스·KIA 타이거즈·한화 이글스 / 경기 사진 — 삼성 라이온즈 제공(페덱), SSG 랜더스 제공(아빌라), KIA 타이거즈 제공(네일·올러·카스트로), 한화 이글스 제공(와이스) / MLB 공식 헤드샷(와이스) / 썸네일 — SSG 랜더스 제공(아빌라), KIA 타이거즈 제공(올러·카스트로), 한화 이글스 제공(와이스), 네일·페덱 사진은 채널 운영자 제공")
SOURCE = ("사실 출처 = 프로젝트 claude/1011-롱폼11-직장폐쇄-근거모음.md. 협약 만료·지침: Forbes 10/8·theScore 10/7·MHN 10/9 / 설문 80%: 이투데이 6/19(디 애슬레틱) / ABC7 10/7 / "
          "2021 직장폐쇄 99일·12/1 14억 달러: 위키·AP 2021-12-02 / 스즈키: 영문 위키(11/22 포스팅, 3/18 계약)·CBS / 2021 KBO: OSEN 12/8·세계일보 12/9·이데일리 12/21·스포티비 12/28·시사저널 2022-02-07 / "
          "2022 결과: 뉴스1 2022-10-10·노컷뉴스 2022-05-30(루이즈 27경기)·스포니치(푸이그 21홈런) / 페덱: IS 7/11·스포츠조선 9/5·MLBTR / 아빌라: 본인 9/29·이숭용 9/30·스포티비 8/22 / "
          "와이스: 스포티비 10/7(MLBTR)·2/1 팟캐스트·7/23 헤일리 SNS / KIA: 스포츠경향 9/29·9/6 / 노시환: OSEN 2/23·스포티비 10/8·스포츠동아 2/25 / KBO 이사회: 마이데일리 10/8 / 상한: 스타뉴스 9/2 / 엠팍 글 6개(10/7~10/9).")

EP = {"date": "2026-10-12", "gameDate": "2026-10-09", "series": "야구롱폼", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1011-long11-v1", "voiceRemap": [None]*94 + [95, 94], "topic": "MLB직장폐쇄",
      "gapScale": 1.05, "pauseMax": 0.4,
      "chapters": [{"key": t, "title": t, "from": a, "to": b} for t, a, b in CH],
      "lines": lines, "scenes": scenes, "thumb": {}, "source": SOURCE,
      "youtube": {"title": "MLB 직장폐쇄 | KBO 외국인 선수 재계약 셈법 페덱 아빌라 와이스 노시환 #프로야구 #직장폐쇄",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#MLB직장폐쇄", "#직장폐쇄", "#외국인선수", "#프로야구", "#KBO", "#페덱", "#아빌라", "#와이스", "#노시환", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {0, 1, 2, 5, 14, 17, 21, 26, 27, 29, 38, 43, 46, 48, 52, 56, 59, 62, 68, 73, 79, 82, 83, 89, 90, 91, 92, 93, 94}
    HOLD = {4: 0.6, 5: 0.6, 17: 0.6, 27: 0.7, 37: 0.6, 43: 0.7, 44: 0.6, 47: 0.5, 56: 0.6, 68: 0.6, 73: 0.6, 80: 0.6, 89: 0.6, 91: 0.6, 93: 0.6, 95: 0.6}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
        if i in HOLD: l['gapAfter'] = HOLD[i]
    th = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'thumb_1011_long11.json')
    if os.path.exists(th): EP['thumb'] = json.load(open(th, encoding='utf-8'))
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-12_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for b in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', b)) > 22: print('호흡 초과', i, b)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
