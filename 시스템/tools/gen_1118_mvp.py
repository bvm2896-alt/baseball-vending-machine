# -*- coding: utf-8 -*-
"""11/18 롱폼 「2026 MVP 누가 받을까」 — 글래스 빠른판, 목소리 A(장운). 대사 = mvp18/script_v2.txt
대사 = /home/claude/mvp18/script_v2.txt (사용자 확인본: 139줄 엔딩 · '최대' 범위 ✗).  근거 = claude/주제전달-1117-FA첫날-10개구단지갑.md · fa13 래리 버드 룰 값.
실행: python3 gen_1117_long.py → episodes/2026-11-17_롱폼.json"""
import json, os, re, sys, io, copy
sys.path.insert(0, '/home/claude/fa13')
from helpers_1113 import *          # S, wrap2, L, DUOT, DCT, PS, VST, VQ, STT, STP, Q, TBG, BG_NEU, KEEP, CB, TEAMN, END
from gen_rank_0923 import END
import helpers_1113 as _H
sys.path.insert(0, '/home/claude/fa17'); from tight import tight
_H.WRAP.update({'두산에겐 시작일 뿐이지 않을까 싶습니다': '두산에겐\n시작일 뿐이지 않을까 싶습니다', '인센티브 1억 6천만 원이라고 합니다': '인센티브\n1억 6천만 원이라고 합니다'})
HERE = os.path.dirname(os.path.abspath(__file__))

# ── 대사 ──
SEC = []
for l in io.open('/home/claude/mvp18/script_v2.txt', encoding='utf-8'):
    l = l.rstrip('\n')
    if l.startswith('## '): SEC.append([l[3:], []])
    elif l.strip(): SEC[-1][1].append(l.strip())

# ── 자막(숫자·영문으로) ──
REP = [('이천이십육년', '2026년'), ('이천이십오년', '2025년'), ('이천이십사년', '2024년'), ('이천이십삼년', '2023년'), ('이천십칠년', '2017년'), ('이천십사년', '2014년'),
       ('이천십이년', '2012년'), ('이천십구년', '2019년'), ('이천십년', '2010년'), ('천구백팔십구년', '1989년'), ('천구백팔십이년', '1982년'),
       ('시월 십이일', '10월 12일'), ('팔월 이십구일', '8월 29일'), ('십일월 십일일', '11월 11일'), ('십일월 이십사일', '11월 24일'), ('십일월 이십육일', '11월 26일'),   # 11/19 시상식 11/26(목) 14시 롯데호텔 월드(11/18 17:03 KBO 수비상 발표)
       ('십이월', '12월'), ('시월', '10월'), ('팔월', '8월'), ('구월', '9월'),
       ('기록사이트', '기록 사이트'), ('케이비오', 'KBO'), ('엠브이피', 'MVP'), ('케이티', 'KT'), ('엘지', 'LG'), ('에스에스지', 'SSG'), ('오피에스', 'OPS'), ('이브이파이브', 'EV5'),
       ('월드베이스볼클래식', 'WBC'),
       ('사십오 홈런', '45홈런'), ('사십사 홈런', '44홈런'), ('사십오 호', '45호'), ('마흔네 개', '44개'), ('이십칠 홈런', '27홈런'), ('오십이 홈런', '52홈런'), ('오십 홈런', '50홈런'),
       ('이십 홈런', '20홈런'), ('십구 홈런', '19홈런'), ('삼 홈런', '3홈런'), ('삼십팔 홈런', '38홈런'), ('사십 도루', '40도루'),
       ('이백십일 안타', '211안타'), ('이백이 안타', '202안타'), ('이백팔 안타', '208안타'), ('이백일 안타', '201안타'), ('이백 안타', '200안타'), ('이백안타', '200안타'),   # 11/18 23:18 '이이이백' 기계음 → 붙여 써서 다시 합성
       ('삼 안타', '3안타'), ('사 안타', '4안타'),
       ('안타 쉰일곱 개', '안타 57개'), ('육백 개', '600개'),
       ('백일 표', '101표'), ('구십오 표', '95표'), ('백이십오 표', '125표'), ('구십육 표', '96표'), ('백십 표', '110표'),
       ('평균자책점 이쩜이사', '평균자책점 2.24'), ('탈삼진 백구십칠 개', '탈삼진 197개'), ('백팔십구 개', '189개'), ('열한 개씩', '11개씩'), ('서른아홉 개', '39개'),
       ('백육십쩜삼 킬로미터', '160.3km'), ('백오십이닝', '150이닝'), ('백육십일이닝', '161이닝'), ('육이닝', '6이닝'), ('육과 삼분의 일이닝 일 실점', '6⅓이닝 1실점'),
       ('십오 승', '15승'), ('십일 승 칠 패', '11승 7패'), ('이십 승', '20승'), ('십칠 승', '17승'), ('구십 승', '90승'), ('구 승', '9승'),
       ('타율 삼 할 팔 리', '타율 3할 8리'), ('삼 할 사 푼 칠 리', '3할 4푼 7리'), ('삼 할 칠 푼 일 리', '3할 7푼 1리'), ('백십팔 타점', '118타점'), ('백삼십구 타점', '139타점'),
       ('삼십오 세이브', '35세이브'), ('삼십 경기', '30경기'), ('통산 백 호', '통산 100호'),
       ('이 대 이', '2대2'), ('팔 회 말', '8회 말'), ('팔 회', '8회'), ('삼 위', '3위'), ('오 위', '5위'), ('칠 위', '7위'), ('일 위', '1위'),
       ('삼 년 연속', '3년 연속'), ('삼 년 동안', '3년 동안'), ('십육 년 만의', '16년 만의'), ('구 년 만의', '9년 만의'), ('일 년 만에', '1년 만에'),
       ('팔 라운드 칠십칠 순위', '8라운드 77순위'), ('일 라운드 오 순위', '1라운드 5순위'), ('일 라운드', '1라운드'), ('오 순위', '5순위'),
       ('이관왕', '2관왕'), ('삼관왕', '3관왕'), ('사관왕', '4관왕'), ('열네 명', '14명'), ('열한 명', '11명'), ('아홉 명', '9명'), ('다섯 명', '5명'), ('세 명', '3명'), ('두 명', '2명'), ('한 명', '1명'),
       ('세 표', '3표'), ('여섯 표', '6표'), ('스물여섯 번', '26번'), ('스무 번', '20번'), ('스물일곱 번', '27번'), ('열 번', '10번'), ('여덟 번', '8번'), ('세 번', '3번'), ('두 번 이상', '2번 이상'), ('이쩜 대', '2점대'),   # 11/19 '이쩜대' → '이쩌대'로 들림 → 띄어 씀
         # 11/18 23:21 사용자 "이쩜이사라고 발음해야 한다니까" → 소수점·점대는 TTS 글에 '쩜'(자막은 숫자)
       ('다섯 개 구단', '5개 구단'), ('두 개 차이', '2개 차이'), ('아홉이닝', '9이닝'), ('타이틀 두 개', '타이틀 2개'), ('타이틀이 두 개', '타이틀이 2개')]
REP.sort(key=lambda x: -len(x[0]))
def SUBTXT(n):
    pcs = []
    for p in n.split(' / '):
        p = p.lstrip('+').strip()
        for a, b in REP: p = p.replace(a, b)
        p = p.replace('3번째', '세 번째')
        pcs.append(p)
    return pcs
# ── 장면 도구 ──
SEG_BG = BG_NEU
def ph(k): return k
FOCUS = {"경기/박찬호_홈쇄도_1005_두산제공": "6% 45%", "경기/오태곤_SSG_뉴스1": "18% 30%", "경기/오태곤_FA계약_1117_SSG제공": "32% 22%", "경기/권희동_끝내기_0820_NC제공": "62% 8%"}
def PSX(img, name, team, sub, viz=(), stats=(), **k):
    if img in FOCUS: k.setdefault("focus", FOCUS[img])
    sc = S(0, "pstat", img=img, name=name, team=team, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, bg=k.pop("bg", TBG(team)), **k); return sc
def DU(cards, title="", **k): return DUOT(title, cards, **k)
def FQ(name, role, team, date, text, img=None, at=0.6, **k): return S(0, "fa_quote", name=name, role=role, team=team, date=date, text=text, img=img, at=at, bg=TBG(team), noCenter=True, **k)
def ND(id, x, y, ic, lab="", sub="", at=0, **k): return dict(id=id, x=x, y=y, ic=ic, lab=lab, sub=sub, at=at, **k)
def ED(a, b, lab="", at=0, **k): return dict(a=a, b=b, lab=lab, at=at, **k)
def FL(nodes, edges=(), cap=None, **k): return S(0, "lo_flow", title="", nodes=list(nodes), edges=list(edges), wall=None, boxes=[], cap=cap, noCenter=True, **k)
def TLN(title, items, **k): k.setdefault('bg', BG_NEU); return S(0, "tline", title=title, items=items, noCenter=True, uni=True, **k)
def QQ(text, logos=(), **k): k.setdefault('bg', BG_NEU); k.setdefault('logoSize', 170); k.setdefault('size', 90); return Q(text, list(logos), **k)

# 사진
RY, RY2, CWJ, KTH = "경기/레이예스_211안타_1012_롯데제공", "경기/레이예스_세리머니_롯데제공", "경기/최원준_KT제공_상체", "KBO프로필/김태형_감독"
KB, KB2, KB3 = "경기/곽빈_포효0823_두산제공", "경기/곽빈_박수_1006_두산제공", "경기/곽빈_WC포효_1014_두산제공"
KDY, KDY2, KDY3 = "경기/김도영_45호_1012_KIA제공", "경기/김도영_45호_덕아웃_1012_KIA제공", "경기/김도영_4회홈런_1017_KIA제공"
HIL, AUS, KJW, KJY = "경기/힐리어드_포효_KT제공_1280", "경기/오스틴_포효_LG제공", "경기/구자욱_KSMVP_1108", "경기/김재윤_투구_1007_삼성제공"
KYP, ICG, SHJ, SGM = "경기/고영표_상체_1011_KT제공", "경기/임찬규_1012_LG제공", "경기/소형준_투구_1012_KT제공", "KBO프로필/스기모토"
# 11/18: 이병규는 주니치 사진 → LG 시절 사진(2016-10-08 시즌 최종전, LG 트윈스 제공·노컷뉴스 게재)
PON, DIA, LBG, YHJ = "상황별/폰세_한화2025", "경기/디아즈_만루포세리머니_삼성제공", "은퇴선수/이병규_LG_2016_LG제공", "경기/양현종_글러브_1012_KIA제공"
# 11/18 사용자 "허인서 사진 왜이래?" → 흰 배경 프로필 대신 한화 경기 사진(위 노란 띠 잘라 냄)
HIS, MJB, KMJ, AHM = "경기/APBC_허인서_사진_crop", "경기/문정빈_하이파이브_LG제공", "경기/APBC_김민준_사진", "경기/APBC_안현민_사진"   # 11/18 사용자 "안현민 사진 이상하니까 바꿔" → 검은 배경 프로필 대신 KT 경기 사진
def BARS(title, items, mx, note=None, noteAt=0, **k):   # 이 템플릿엔 bars 가 없어 rf_bars 로(제목 ' · ' 뒤는 작은 글)
    its = []
    for x in items:
        lab = x['label'] + (' · ' + x['sub'] if x.get('sub') else '')
        v = x['value']; txt = (('%g' % v) if isinstance(v, float) else str(v)) + x.get('unit', '')
        its.append(dict(label=lab, v=v, txt=txt, hi=x.get('hi', False), at=x.get('at', 0)))
    if note: title = title + ' · ' + note
    k.setdefault('bg', BG_NEU)
    return S(0, "rf_bars", title=title, items=its, max=mx, glass=True, noCenter=True, **k)
# 11/18 11:45 사용자 "같은 사진을 몇 번 돌려 쓰는 거야" → 사람마다 사진을 나눠 씀(같은 묶음 안에서만 같은 사진)
RYH, RYF, RYB, RYM, RYD, RYT, RY204 = "경기/레이예스_하이파이브_롯데제공", "경기/레이예스_손가락_1011_롯데제공", "경기/레이예스_양손가리키기_롯데제공", "경기/레이예스_미소_1006_롯데제공", "경기/레이예스_두손_1007_롯데제공", "경기/레이예스_타격_1012_롯데제공", "경기/레이예스_204안타_1009_롯데제공"
KBS, KBT = "경기/곽빈_포효_스타뉴스", "경기/곽빈_WC투구_1014_두산제공"
KBU, KBY = "경기/곽빈_사용자제공_1004", "경기/곽빈_역투_두산제공_crop"   # 11/18 사용자 "같은 장면 다시 등장" → 곽빈 카드가 같은 사진으로 다시 뜨지 않게
KDY4, KDY5 = "경기/김도영_45호_포효_1012_연합뉴스", "경기/김도영_덕아웃_KIA제공"   # 11/18 검수: 덕아웃 사진은 얼굴이 위에 붙음 → 교체
KDP, KD41, KD43, KDR = "경기/김도영_45호_포효_1012_스포츠조선", "경기/김도영_41호_KIA제공_HQ", "경기/김도영_43호_KIA제공_up", "경기/김도영_45호_주루_1012_KIA제공"
HIL2, HIL3, HIL4 = "경기/힐리어드_포효_KT제공_HQ", "경기/힐리어드_하이파이브_KT제공", "경기/힐리어드_40호_상체"
CWJ2, CWJ3, SGM2, AUS2 = "경기/최원준_두검지_1006_KT제공", "경기/최원준_웃음_KT제공_up", "경기/스기모토_포효_crop", "경기/오스틴_락손세리머니_LG제공"
T10 = ["SSG", "KT", "키움", "롯데", "한화", "KIA", "LG", "두산", "NC", "삼성"]

def SILX(img, at=None):
    k = "실루엣/" + img.split("/")[-1] + "_실루엣"; d = dict(sil=k, img2=k)
    if at is not None: d["revealAt"] = at
    return d
LS = []
def A(sc, **x): LS.append([sc, x])
def KP(sc, **k): return KEEP(sc, **k)
def ADD(sc, *v, **k):
    s2 = KEEP(sc, **k); s2['viz'] = s2.get('viz', []) + list(v); return s2
def ADS(sc, i, *st, **k):   # 듀오 카드 i 에 기록 더하기
    s2 = KEEP(sc, **k); s2['cards'][i]['stats'] = s2['cards'][i].get('stats', []) + list(st); return s2
def SK(k, v, at, hi=False): return dict(k=k, v=v, at=at, hi=hi)
def PR(cards, cap=None, capAt=0, chain="pr", **k):   # 11/18 11:04 사용자 "작은 원 말고 사진 크게" → 큰 사진 액자 나란히
    k.setdefault('bg', BG_NEU); return S(0, "photo_row", cards=cards, cap=cap, capAt=capAt, chain=chain, noCenter=True, **k)
def PC(img, name, sub="", at=0, **k): return dict(img=img, name=name, sub=sub, at=at, **k)
# 11/18 23:11 사용자가 준 서부 콘셉트 그림 3장(김도영·곽빈·레이예스) → 맨 처음 세 사람 장면
KDW, KBW, RYW = "연출/김도영_서부_사용자제공_1118", "연출/곽빈_서부_사용자제공_1118", "연출/레이예스_서부_사용자제공_1118"
TRIOS = {"A": (KDW, RYW, KBW), "B": (KD41, RYB, KBS), "C": (KD43, RYH, KB3), "D": (KDY4, RY204, KBT)}
def TRIO(at=(0.1, 0.9, 1.8), cap=None, capAt=0, chain="trio", set="A", **k):
    a, b, c = TRIOS[set]
    return PR([PC(a, "김도영", "KIA · 45홈런", at[0]), PC(b, "레이예스", "롯데 · 211안타", at[1]), PC(c, "곽빈", "두산 · 투수 2관왕", at[2])], cap=cap, capAt=capAt, chain=chain, **k)
def KT5(at=0.3, cap=None, capAt=0, chain="kt5"):
    return PR([PC(HIL4, "힐리어드", "타점왕", at), PC(CWJ3, "최원준", "208안타", at + .15), PC(KYP, "고영표", "15승", at + .3), PC(SHJ, "소형준", "승률왕", at + .45), PC(SGM2, "스기모토", "홀드왕", at + .6)],
              cap=cap, capAt=capAt, chain=chain, bg=TBG("KT"))

# ════ 오프닝 (9) ════
O1 = TRIO(chain="o1")
A(O1)
A(KP(O1, cap="2026 MVP · 3파전", capAt=0.6))
B24 = BARS("2024 MVP 투표 · 101표", [dict(label="김도영", sub="KIA", value=95, unit="표", at=0.9, hi=True)], 101, chain="b24", bg=BG_NEU); A(B24)
A(BARS("2024 MVP 투표 · 101표", [dict(label="김도영", sub="KIA", value=95, unit="표", at=-1, hi=True), dict(label="다른 선수", sub="만장일치까지", value=6, unit="표", at=0.5)], 101, chain="b24", cont=True))
A(QQ("MVP 만장일치 · 1982년 박철순 한 명", ["두산"], textAt=0.2))
O2 = TRIO(at=(0.05, 0.15, 0.25), cap="올해는 표가 갈린다?", capAt=0.5, chain="o2", set="B"); A(O2)
A(KP(O2, cap="받을 이유 · 걸리는 점 하나씩", capAt=0.3))
O3 = TLN("", [STP("하나", "기록", 0.5), STP("둘", "약점", 1.3), STP("셋", "역대 투표", 2.2), STP("넷", "제 예상", 3.4, c="gold")], chain="o3"); A(O3)
A(KP(O3))

# ════ 레이예스 (27) ════
R1 = PSX(RY, "레이예스", "롯데", "외야수 · 2026 시즌", [VST("2026년 10월 12일 · 잠실", 0.3, size=56)], chain="r1", bg=BG_NEU, **SILX(RY, 99)); A(R1)
R1b = ADD(R1, VST("안타 2개 차이로 쫓기던 타자", 0.9, size=52)); A(R1b)
R1c = ADD(R1b, VST("추격자 · 그날 3안타", 0.9, size=52)); A(R1c)
R1d = ADD(R1c, VST("이 타자 · 4안타", 0.7, size=60)); A(R1d)
A(KP(R1d, revealAt=0.1, bg=TBG("롯데")))
R2 = PSX(RY, "레이예스", "롯데", "외야수 · 2026 시즌", [VST("211안타", 0.6, size=76)], chain="r2"); A(R2)
A(ADD(R2, VST("KBO 한 시즌 최다 안타 신기록", 0.4, size=52)))
A(TLN("레이예스 한 시즌 안타", [STP("2024년", "202안타 · 신기록", 0.4), STP("2026년", "211안타 · 신기록", 1.6, c="gold")], chain="rt", bg=TBG("롯데")))
A(PSX(RYT, "레이예스", "롯데", "10월 12일 · 8회 마지막 안타", [VST("두산 팬들에게도 허리 숙여 인사", 1.6, size=50)], chain="r18"))
A(DU([DCT(RYH, "레이예스", "롯데", 0), DCT(KTH, "김태형", "롯데", 0.5, [SK("롯데 감독", "더그아웃 포옹", 0.9)])], title="더그아웃에서"))
# 11/18 검수: 기록이 붙을 때 카드가 줄어들며 움직임 → 처음부터 기록 자리를 잡아 두고(at=50 = 안 보임) 시각만 바꾼다
R20 = DU([DCT(RYH, "레이예스", "롯데", 0, [SK("최종", "211안타", 50, True)]), DCT(CWJ2, "최원준", "KT", 0.5, [SK("9월~시즌 끝", "57안타", 50), SK("최종", "208안타", 50)])], title="최다 안타 경쟁", chain="r20"); A(R20)
R21 = KEEP(R20); R21['cards'][1]['stats'][0]['at'] = 1.6; A(R21)
R22 = KEEP(R21); R22['cards'][1]['stats'][1]['at'] = 0.6; R22['cards'][0]['stats'][0]['at'] = 0.2; A(R22)
A(BARS("한 시즌 200안타", [dict(label="서건창", sub="2014년", value=201, unit="안타", at=0.2), dict(label="레이예스", sub="2024년", value=202, unit="안타", at=0.4),
                          dict(label="최원준", sub="2026년", value=208, unit="안타", at=1.4, hi=True), dict(label="레이예스", sub="2026년", value=211, unit="안타", at=1.6, hi=True)], 265,
       note="한 시즌 두 명은 처음", noteAt=2.6, chain="b200", bg=TBG("롯데")))
R24 = PSX(RYF, "레이예스", "롯데", "외야수", [VST("3년 연속 안타왕", 0.5, size=64)], chain="r24"); A(R24)
A(DU([DCT(LBG, "이병규", "LG", 0, [SK("1999~2001년", "3년 연속", 0.3)]), DCT(RYB, "레이예스", "롯데", 0.8, [SK("외국인 타자", "처음", 1.6, True)])], title="3년 연속 안타왕"))
A(TLN("레이예스 3년", [STP("2024년", "202안타", 0.1), STP("2025년", "187안타", 0.3), STP("2026년", "211안타", 0.5), STP("3년 합계", "600안타", 0.9, c="gold")], chain="r600", bg=TBG("롯데")))
Q27 = FQ("레이예스", "롯데 외야수", "롯데", "2026년 10월 12일", "이 기록이 비시즌을 잘 준비한 증거", img=RYM, at=0.6, chain="rq"); A(Q27)
A(FQ("레이예스", "롯데 외야수", "롯데", "2026년 10월 12일", "최원준에게 · 정말 고생했다", img=RYM, at=0.6, chain="rq"))
A(FQ("레이예스", "롯데 외야수", "롯데", "2026년 10월 12일", "내년에도 롯데에서 뛰고 싶다", img=RYM, at=0.4, chain="rq"))
A(TLN("롯데 MVP", [STP("2010년", "이대호", 0.6), STP("2026년", "레이예스?", 1.8, c="gold")], chain="rlm", bg=TBG("롯데")))
A(QQ("근데 · 2024년 투표", ["롯데", "KIA"], textAt=0.2))
A(PSX(RYD, "레이예스", "롯데", "2024년", [VST("202안타 · 당시 신기록", 0.6, size=56)], chain="r32"))
B24b = BARS("2024 MVP 투표 · 101표", [dict(label="레이예스", sub="202안타 신기록", value=3, unit="표", at=0.5, hi=True)], 101, chain="b24b", bg=BG_NEU); A(B24b)
A(BARS("2024 MVP 투표 · 101표", [dict(label="레이예스", sub="202안타 신기록", value=3, unit="표", at=-1, hi=True), dict(label="김도영", sub="38홈런 · 40도루", value=95, unit="표", at=1.4)], 101, chain="b24b", cont=True))
A(QQ("롯데 · 2026 정규시즌 7위", ["롯데"], textAt=0.2))
A(PSX(RY204, "레이예스", "롯데", "제 생각", [VST("안타 기록 하나로는 쉽지 않다", 1.4, size=52, c="bad")], chain="r36"))

# ════ 곽빈 (26) ════
K1 = PSX(KB, "곽빈", "두산", "투수 · 2026 시즌", [], chain="k1", bg=BG_NEU, **SILX(KB, 99)); A(K1)
K1b = ADD(K1, VST("2026년 8월 29일", 0.3, size=52), VST("MLB 5개 구단 스카우트 앞", 1.4, size=50), VST("시속 160.3km", 3.0, size=72)); A(K1b)
A(KP(K1b, revealAt=0.1, bg=TBG("두산")))
K2 = PSX(KB, "곽빈", "두산", "2026 시즌", [VST("평균자책점 2.24", 0.6, size=58), VST("탈삼진 197개", 1.7, size=58), VST("두 부문 1위", 2.8, size=60)], chain="k2"); A(K2)
K2b = ADD(K2, VST("규정이닝 투수 중 유일한 2점대", 1.4, size=46)); A(K2b)
A(PSX(KBT, "곽빈", "두산", "2026 시즌", [VST("퀄리티스타트", 0.2, size=52), VST("선발 27번 중 20번", 1.2, size=60)], chain="k42"))
K3 = PSX(KB2, "곽빈", "두산", "9이닝당 탈삼진", [VST("11.01개", 0.9, size=76)], chain="k3"); A(K3)
A(ADD(K3, VST("150이닝 넘긴 국내 투수 중 역대 1위", 0.6, size=46)))
A(BARS("9이닝당 탈삼진 · 국내 투수 150이닝 이상", [dict(label="선동열", sub="1989년", value=10.54, unit="개", at=0.05), dict(label="류현진", sub="2012년", value=10.35, unit="개", at=0.85),   # 11/18 23:22 사용자 "막대 순서대로(위→아래)" → 말하는 순서·연도 순으로 위에서부터
                                             
                                              dict(label="곽빈", sub="2026년", value=11.01, unit="개", at=1.6, hi=True)], 13.5, chain="bk9", bg=TBG("두산")))
A(TLN("곽빈 · 2026 WBC", [STP("8강 도미니카공화국전", "볼넷 연속 · 밀어내기", 1.2, c="bad")], chain="k46", bg=TBG("두산")))
A(FQ("곽빈", "두산 투수", "두산", "2026년 3월 23일", "너무 도망간 모습이 창피했다", img=KBS, at=0.5, chain="kq"))
A(PSX(KB3, "곽빈", "두산", "2026 시즌", [VST("161이닝 · 볼넷 39개", 1.4, size=58)], chain="k48"))
A(TLN("두산 우완 한 시즌 탈삼진", [STP("2019년", "린드블럼 189개", 0.6), STP("2026년", "곽빈 197개", 2.85, c="gold")], chain="kld", bg=TBG("두산")))
A(TLN("2026 아시안게임", [STP("대만전", "6이닝 노히트", 0.8), STP("일본 결승", "6⅓이닝 1실점", 2.4, c="gold")], chain="kag", bg=TBG("두산")))
A(PSX(KBU, "곽빈", "두산", "2026년 11월 11일", [VST("최동원상", 0.6, size=76)], chain="k51"))
A(DU([DCT(YHJ, "양현종", "KIA", 0, [SK("2017년", "MVP", 0.4)]), DCT(KBS, "곽빈", "두산", 1.0, [SK("2026년", "9년 만?", 1.6, True)])], title="국내 투수 MVP"))
K53 = QQ("곽빈의 약점 · 하나", ["두산"], textAt=0.2, chain="k53"); A(K53)
A(QQ("곽빈의 약점 · 승수", ["두산"], textAt=0.1, chain="k53", cont=True))
K55 = TLN("곽빈 승수", [STP("2024년", "15승 · 공동 다승왕", 0.6)], chain="kw", bg=TBG("두산")); A(K55)
A(KP(K55, items=[STP("2024년", "15승 · 공동 다승왕", -1), STP("2026년", "11승 7패", 0.5, c="bad")]))
A(PSX(KBS, "곽빈", "두산", "2026 시즌", [VST("승리가 줄어든 이유 · 타선 지원", 0.9, size=48)], chain="k57"))
A(DU([DCT(KYP, "고영표", "KT", 0, [SK("다승 공동 1위", "15승", 0.6)]), DCT(ICG, "임찬규", "LG", 0.3, [SK("다승 공동 1위", "15승", 0.6)])], title="2026 다승 1위"))
A(BARS("최근 투수 MVP 승수", [dict(label="페디", sub="2023년 · NC", value=20, unit="승", at=0.9), dict(label="폰세", sub="2025년 · 한화", value=17, unit="승", at=2.3)], 22, chain="bkw", bg=TBG("두산")))
A(TLN("최근 투수 MVP", [STP("2023년 페디", "다승 포함 3관왕", 0.3), STP("2025년 폰세", "다승 포함 4관왕", 1.0, c="gold")], chain="kpm", bg=TBG("두산")))
A(QQ("두산 · 정규시즌 5위 · 와일드카드에서 끝", ["두산", "LG"], textAt=0.2))
A(PSX(KBY, "곽빈", "두산", "제 생각", [VST("기록의 질은 최고", 0.8, size=56), VST("승수가 발목?", 2.6, size=60, c="bad")], chain="k62"))

# ════ 김도영 (24) ════
D1 = PSX(KDY, "김도영", "KIA", "내야수 · 2026 시즌", [VST("마지막 날 홈런 순위를 뒤집은 타자", 0.6, size=48)], chain="d1", bg=BG_NEU, **SILX(KDY, 99)); A(D1)
D1b = ADD(D1, VST("2026년 10월 12일 · 광주", 0.3, size=52)); A(D1b)
D1c = ADD(D1b, VST("3위가 걸린 시즌 최종전", 0.3, size=52)); A(D1c)
D4 = PSX(KDY, "김도영", "KIA", "내야수 · 2026 시즌", [VST("그때까지 홈런 공동 1위 · 44개", 0.6, size=52)], chain="d4", bg=BG_NEU, **SILX(KDY, 99)); A(D4)
D4b = ADD(D4, VST("8회 말 2대2 · 투런 홈런", 2.6, size=56)); A(D4b)
A(KP(D4b, revealAt=0.1, bg=TBG("KIA")))
D2 = PSX(KDY, "김도영", "KIA", "2026년 10월 12일", [VST("시즌 45호", 0.5, size=76)], chain="d2"); A(D2)
A(DU([DCT(KDR, "김도영", "KIA", 0, [SK("홈런", "45개", 0.2, True)]), DCT(HIL3, "힐리어드", "KT", 0.3, [SK("홈런", "44개", 0.5)])], title="단독 홈런왕"))
A(TLN("한 방으로", [STP("홈런", "단독 1위", 0.3), STP("팀", "3위 확정", 0.8), STP("통산", "100호", 1.3, c="gold")], chain="d71", bg=TBG("KIA")))
D3 = PSX(KDY4, "김도영", "KIA", "2026 시즌", [VST("타율 3할 8리", 1.0, size=56), VST("45홈런", 1.8, size=56), VST("118타점", 2.4, size=56)], chain="d3"); A(D3)
A(ADD(D3, VST("홈런 · 장타율 2관왕", 0.5, size=56)))
A(TLN("김도영 홈런", [STP("전반기", "27홈런 · 오스틴과 공동 1위", 0.7), STP("시즌 끝", "45홈런 · 단독 1위", 3.0, c="gold")], chain="d74", bg=TBG("KIA")))
A(PSX(KD41, "김도영", "KIA", "한 기록 사이트 계산", [VST("승리 기여도 리그 1위", 1.4, size=56)], chain="d75"))
D76 = TLN("김도영", [STP("2025년", "햄스트링 3번 · 30경기", 0.8, c="bad")], chain="d76", bg=TBG("KIA")); A(D76)
A(KP(D76, items=[STP("2025년", "햄스트링 3번 · 30경기", -1, c="bad"), STP("2026년", "홈런왕", 0.4, c="gold")]))
A(QQ("김도영도 · 걸리는 게 있다", ["KIA"], textAt=0.2))
A(TLN("김도영 타율", [STP("2024년 · MVP", "3할 4푼 7리", 0.8), STP("2026년", "3할 8리", 2.6, c="bad")], chain="d79", bg=TBG("KIA")))
A(DU([DCT(AUS, "오스틴", "LG", 0.6, [SK("OPS", "1.062", 1.4, True)]), DCT(KD43, "김도영", "KIA", 0.6, [SK("OPS", "1.060", 1.4)])], title="OPS 1위 · 오스틴"))
A(QQ("김도영이 받으면 · 두 번째 MVP", ["KIA"], textAt=0.2))
A(TLN("MVP 2번 이상", [STP("이승엽", "5번", 0.6), STP("선동열", "3번", 0.9), STP("김성한", "2번", 1.2), STP("장종훈", "2번", 1.5), STP("박병호", "2번", 1.8)], chain="d82"))
D83 = PSX(KDY3, "김도영", "KIA", "2026 준플레이오프", [VST("3홈런 · 시리즈 MVP", 1.4, size=56)], chain="d83"); A(D83)
D84 = ADD(D83, VST("이번 투표엔 안 들어감", 0.2, size=52, c="bad")); A(D84)
A(ADD(D84, VST("투표는 정규시즌 끝나자마자", 0.3, size=48)))
A(FQ("김도영", "KIA 내야수", "KIA", "2026년 8월 26일", "할 것만 하면 · 상은 따라온다", img=KDP, at=0.6, chain="dq"))

# ════ 다른 후보 (9) ════
A(QQ("MVP 후보 14명 · 투수 7 · 타자 7", ["KT", "삼성", "LG", "두산", "KIA", "롯데"], textAt=0.2, logoSize=130))
A(PSX(HIL2, "힐리어드", "KT", "2026 시즌", [VST("44홈런", 0.9, size=60), VST("139타점 · 타점왕", 1.8, size=56)], chain="g88"))
G89 = PSX(KJW, "구자욱", "삼성", "2026 시즌", [VST("3할 7푼 1리", 0.8, size=60), VST("타율 · 출루율 1위", 1.6, size=56)], chain="g89"); A(G89)
A(ADD(G89, VST("한국시리즈 MVP · 투표엔 안 들어감", 0.6, size=46, c="bad")))
A(DU([DCT(AUS2, "오스틴", "LG", 0, [SK("OPS", "1위", 0.6, True)]), DCT(KJY, "김재윤", "삼성", 1.1, [SK("세이브왕", "35세이브", 2.0, True)])], title="다른 후보"))
A(QQ("KT · 정규시즌 1위 · 90승", ["KT"], textAt=0.2))
K5 = KT5(at=0.3, chain="kt5"); A(K5)
A(KP(K5, cap="KT에서만 후보 5명", capAt=0.3))
A(KP(K5, cap="한 팀 안에서 표가 나뉜다", capAt=0.6))

# ════ 역대 투표 (16) ════
A(QQ("역대 MVP 투표", T10, textAt=0.2, logoSize=130, logoAt=0.6))
V1 = TLN("MVP 뽑는 법", [STP("투표", "취재 기자 한 사람 한 표", 0.8)], chain="v1"); A(V1)
V2 = KP(V1, items=[STP("투표", "취재 기자 한 사람 한 표", -1), STP("수상", "가장 많은 표", 0.4)]); A(V2)
A(KP(V2, items=[STP("투표", "취재 기자 한 사람 한 표", -1), STP("수상", "가장 많은 표", -1), STP("부상", "트로피 + 기아 EV5", 0.6, c="gold")]))
A(QQ("역대 투표 · 흐름이 있다", ["KIA", "롯데", "두산"], textAt=0.2))
A(BARS("역대 타자 MVP · 26번", [dict(label="홈런왕", value=20, unit="번", at=1.85, hi=True), dict(label="그 밖", value=6, unit="번", at=2.3)], 26, chain="bh"))
A(BARS("역대 타자 MVP · 26번 중 20번 · 10번 중 8번꼴", [dict(label="홈런왕", value=20, unit="번", at=-1, hi=True), dict(label="그 밖", value=6, unit="번", at=-1)], 26, chain="bh", cont=True))
V3 = TLN("2014년 MVP", [STP("넥센 서건창", "201안타 · 신기록", 1.0, c="gold")], chain="v3", bg=TBG("키움")); A(V3)
V4 = KP(V3, items=[STP("넥센 서건창", "201안타 · 신기록", -1, c="gold"), STP("넥센 박병호", "52홈런", 0.6)]); A(V4)
A(KP(V4, items=[STP("넥센 서건창", "201안타 · 신기록", -1, c="gold"), STP("넥센 박병호", "52홈런", -1), STP("서건창", "타격왕 + 득점왕", 0.6, c="gold")]))
A(PSX(RY2, "레이예스", "롯데", "2024년 · 202안타 신기록", [VST("MVP 투표 3표", 1.8, size=64, c="bad")], chain="b24c"))   # 11/18: 레이예스 장의 2024 투표 막대가 그대로 다시 나오던 것 → 사진 카드
A(QQ("외국인 타자 MVP · 우즈 · 테임즈 · 로하스", ["두산", "NC", "KT"], textAt=0.2, logoAt=1.0))
V8 = DU([DCT(PON, "폰세", "한화", 0.6, [SK("2025년", "투수 4관왕", 1.4, True)])], title="투수 쪽은 · 2025년 폰세", chain="v8"); A(V8)
V9 = KP(V8); V9['cards'].append(DCT(DIA, "디아즈", "삼성", 0.9, [SK("2025년", "50홈런", 1.6)])); A(V9)
A(BARS("2025 MVP 투표 · 125표", [dict(label="폰세", sub="한화 · 투수 4관왕", value=96, unit="표", at=0.1, hi=True), dict(label="디아즈", sub="삼성 · 50홈런", value=23, unit="표", at=0.1)], 125, chain="b25", bg=BG_NEU))
A(TLN("역대 결과", [STP("하나", "홈런왕", 1.6), STP("둘", "타이틀 여러 개", 2.8, c="gold")], chain="v11"))

# ════ 전망 (8) ════
P1 = TRIO(at=(0.1, 0.25, 0.4), chain="p1", set="D"); A(P1)   # 11/18: '전망' 알약은 두 줄 자막과 겹쳐서 뺌(위 칸에 장 이름 있음)   # 11/18: 오프닝 세 사람(B)이 전망에서 그대로 다시 나오던 것
# 11/18 17:00 사용자 "다음 장면을 없애고 저 장면에서 설명을 해, 곽빈과 김도영만 이야기하니까 레이예스는 잠시 흑백" → 세 사람 줄 그대로, 레이예스 흑백, 곽빈·김도영 아래 글만 바뀜
P2 = KEEP(P1); P2['cards'][1]['gray'] = True; P2['cards'][2].update(sub="가장 유력 기사", subAt=1.5, hi=True); A(P2)
P3 = KEEP(P2); P3['cards'][0].update(sub="근소하게 앞선다", subAt=1.0, hi=True); A(P3)
P4 = PSX(KDY5, "김도영", "KIA", "제 예상", [VST("기록은 셋 다 받을 만", 0.6, size=52), VST("흐름까지 보면 · 김도영", 3.0, size=60)], chain="p4"); A(P4)
A(ADD(P4, VST("홈런왕 포함 2관왕 + 마지막 날 한 방", 0.6, size=46)))
A(PSX(KB2, "곽빈", "두산", "곽빈이 받는다면", [VST("승수보다 평균자책점 · 탈삼진", 1.4, size=50)], chain="p6"))
A(PSX(RYB, "레이예스", "롯데", "레이예스는", [VST("2024년 3표 → 2026년은?", 1.2, size=56)], chain="p7"))
A(PSX(KD43, "김도영", "KIA", "김도영이 받더라도", [VST("2024년처럼 압도적이진 않을 듯", 1.6, size=50)], chain="p8"))

# ════ 신인상 (11) ════
A(QQ("신인상도 · 같은 날 발표", ["한화", "LG", "SSG"], textAt=0.2))
A(QQ("신인상 후보 · 9명", ["한화", "LG", "SSG"], textAt=0.1, cont=True))
N1 = PSX(HIS, "허인서", "한화", "포수", [VST("20홈런", 1.2, size=64), VST("가장 앞서 있다", 2.4, size=52)], chain="n1"); A(N1)
N2 = ADD(N1, VST("올스타전 MVP", 0.3, size=50), VST("도루 저지율 상위권", 1.6, size=50)); A(N2)
A(PSX(HIS, "허인서", "한화", "포수", [VST("2010년 양의지 이후", 0.6, size=50), VST("16년 만의 포수 신인왕?", 1.6, size=56)], chain="n3"))
def RK(a1, a2, cap=None, capAt=0, s1="LG", s2="SSG", sa1=None, sa2=None): return PR([PC(MJB, "문정빈", s1, a1, subAt=sa1), PC(KMJ, "김민준", s2, a2, subAt=sa2)], cap=cap, capAt=capAt, chain="n4")
A(RK(0.2, 0.4, cap="대항마 둘", capAt=0.3))
A(RK(-1, -1, cap="대항마 둘", capAt=-1, s1="LG · 8라운드 77순위\n19홈런", sa1=0.9))
A(RK(-1, -1, cap="대항마 둘", capAt=-1, s1="LG · 8라운드 77순위\n19홈런", s2="SSG · 1라운드 5순위 고졸\n9승", sa2=1.0))
N7 = PSX(AHM, "안현민", "KT", "2025년 신인상", [VST("125표 중 110표", 1.4, size=60)], chain="n7"); A(N7)
A(ADD(N7, VST("올해는 표가 갈릴 듯", 0.4, size=52)))
A(QQ("감독상 · 2025년엔 12월 골든글러브 시상식에서", T10, textAt=0.2, logoSize=120, logoAt=0.8))

# ════ 엔딩 (7) ════
# 11/18 23:32 사용자 "김도영 두 번째 MVP·이변 장면 없애고 세 사람 장면 바로, 김도영 얘기할 땐 김도영만, 그다음 나머지 둘" → 같은 세 사람 줄에서 카드만 차례로
E1 = TRIO(at=(0.1, 50, 50), chain="e3", set="C"); A(E1)
E2 = KEEP(E1); E2['cards'][1]['at'] = 0.05; E2['cards'][2]['at'] = 0.15; A(E2)
E3 = KEEP(E2); A(E3)
E4 = TLN("KBO 시상식", [STP("2025년", "11월 24일", 0.8)], chain="e4"); A(E4)
E5 = KP(E4, items=[STP("2025년", "11월 24일", -1), STP("2026년", "11월 26일", 0.85, c="gold")]); A(E5)
A(KP(E5, items=[STP("2025년", "11월 24일", -1), STP("2026년", "11월 26일", -1, c="gold"), STP("결과 나오면", "바로 정리", 1.4)]))
A(QQ("채널 구독하고 · 시상식 결과 받아보세요", T10, logoSize=150, size=84, logoAt=0.6, noQ=True, chain="e7"))
# ── 조립 ──
NS = [x for _, ls in SEC for x in ls]
assert len(NS) == len(LS), (len(NS), len(LS), [(s[0], len(s[1])) for s in SEC])
lines, scenes = [], []
CHK = {"오프닝": "오프닝", "레이예스": "레이예스", "곽빈": "곽빈", "김도영": "김도영", "다른 후보": "다른 후보", "역대 투표": "역대 투표", "전망": "전망", "신인상": "신인상", "엔딩": "정리"}
CHT = {"오프닝": "2026 MVP 3파전", "레이예스": "레이예스, 211안타 신기록", "곽빈": "곽빈, 투수 2관왕", "김도영": "김도영, 45홈런 홈런왕", "다른 후보": "힐리어드·구자욱·KT 후보 5명", "역대 투표": "역대 투표 흐름", "전망": "제 예상", "신인상": "신인상 허인서·문정빈·김민준", "정리": "누가 받을까?"}
TCOL = {"롯데": ("#0E46B0", "#D00F31"), "두산": ("#2A3AA8", "#B0183C"), "기아": ("#D81E37", "#6A2BD8"), "KT": ("#C8232C", "#3B3F68"), "삼성": ("#1E5BE0", "#7B3BFF"), "LG": ("#C30452", "#5B2BD8"), "한화": ("#F37321", "#8A2E5E"), "SSG": ("#CE0E2D", "#B5821E"), "키움": ("#A3123A", "#5A2A9E"),
        "레이예스": ("#0E46B0", "#D00F31"), "곽빈": ("#2A3AA8", "#B0183C"), "김도영": ("#D81E37", "#6A2BD8")}
CH, i = [], 0
# 11/17 검수: 팀을 숨기는 줄(공개 전)엔 장 칩·팀 색으로 팀을 미리 알리지 않는다 → 숨기는 줄은 따로 '다음 팀' 장으로, 팀 색은 공개 줄부터
HID = {"레이예스": (4, "안타 두 개 차이로 쫓기던 타자"), "곽빈": (2, "시속 160.3km를 던진 투수"), "김도영": (5, "마지막 날 홈런 순위를 뒤집은 타자")}
TEAMK = {"SSG": "SSG", "KT": "KT", "키움": "키움", "롯데": "롯데", "한화": "한화", "KIA": "기아", "LG": "LG", "두산": "두산", "삼성": "삼성"}
def _punct(t):   # 11/17 검수: 자막엔 쉼표·마침표 ✗(천 단위 쉼표는 둠)
    t = re.sub(r'(?<!\d),|,(?!\d)', '', t); t = re.sub(r'\.(?=$|\n)', '', t); return t
for name, ls in SEC:
    key = CHK[name]; hid = HID.get(name)
    if hid:
        CH.append({"key": key + "?", "title": CHT[key], "short": "다음 후보", "from": i, "to": i + hid[0] - 1})   # 설명란엔 이 칸(팀 제목)만
        CH.append({"key": key, "title": CHT[key], "short": key, "from": i + hid[0], "to": i + len(ls) - 1, "ytSkip": True})
    else: CH.append({"key": key, "title": CHT[key], "short": key if key != "오프닝" else "MVP", "from": i, "to": i + len(ls) - 1})
    for jn, n in enumerate(ls):
        sc, x = LS[i]; pcs = [_punct(p) for p in SUBTXT(n)]
        l = {"narr": tight(n), "sub": "|".join(wrap2(p) for p in pcs)}   # 11/17 사용자: 마디마다 끊지 않게(tight)
        l.update(x); lines.append(l)
        s2 = copy.deepcopy(sc); s2['startLine'] = i; s2.setdefault('bg', BG_NEU)
        _tk = TEAMK.get(s2.get('team') or '') if s2['type'] in ('pstat', 'rf_capbar', 'fa_board', 'fa_quote') and s2.get('team') else None
        if hid and jn < hid[0]: s2.pop('tc', None); s2['bg'] = BG_NEU
        elif _tk in TCOL: s2['tc'], s2['tc2'] = TCOL[_tk]
        elif key in TCOL: s2['tc'], s2['tc2'] = TCOL[key]
        scenes.append(s2); i += 1
# 이어지는 장면 묶음
for j in range(1, len(scenes)):
    a, b = scenes[j - 1], scenes[j]
    if b.get('cont') and a['type'] == b['type'] and not (a.get('chain') and a.get('chain') == b.get('chain')):
        a.setdefault('chain', 'ck%d' % j); b['chain'] = a['chain']
def _pics_of(o, acc, top=True):
    if isinstance(o, dict):
        for k_, v_ in o.items():
            if top and k_ in ('img', 'img2', 'bg', '_pics'): continue
            if isinstance(v_, str) and v_.startswith(('경기/', 'KBO프로필/', '카드/', '상황별/', '은퇴선수/', '레전드/')): acc.append(v_)
            else: _pics_of(v_, acc, False)
    elif isinstance(o, list):
        for v_ in o: _pics_of(v_, acc, False)
for _s in scenes:
    _a = []; _pics_of(_s, _a)
    if _a: _s['_pics'] = [{'img': x} for x in dict.fromkeys(_a)]
_QL = ["SSG", "KT", "키움", "롯데", "한화", "KIA", "LG", "두산", "NC", "삼성"]
# 11/17 22:44 사용자: 끝줄을 "구독하시고 FA 소식 받아보세요"로 → 고정 구독 멘트(END)와 겹쳐서 END 는 뺌
for l in lines[:-1]:
    if len(l['narr'].split(' / ')) > 1 and len(l['sub'].split('|')[0]) <= 4: l['noMerge'] = True
for k_, l in enumerate(lines[:-1]):   # 11/17 검수: 질문 줄 뒤 0.55초, '예.' 공개 앞 줄 뒤 0.5초
    if l.get('gapAfter') is None and l['narr'].rstrip().endswith('?'): l['gapAfter'] = 0.4
    elif l.get('gapAfter') is None and lines[k_ + 1]['narr'].startswith(('예.', '네.')): l['gapAfter'] = 0.5
for l in lines:   # 11/18 00:28 사용자 "돈이 들 텐데요... 이렇게 자막 나오게" — 말끝을 흐리는 '-텐데요'는 자막 끝에 말줄임표
    if l['sub'].rstrip().endswith('텐데요'): l['sub'] = l['sub'].rstrip() + '...'
# (11/18 00:25 사용자 "텀을 두라는 말이 아니야. 흐름이 깨지잖아" → 공개 줄 1초 잡기 뺌)
_chs = {c['from'] for c in CH}
# (11/18 17:00 사용자 "잡아두지 말고" → 전망 세 사람 줄 1초 잡기 뺌, 다음 두 줄도 같은 장면에서)
for k_, l in enumerate(lines[:-1]):
    if l.get('gapAfter') is None and (k_ + 1) in _chs: l["gapAfter"] = 0.45


# 11/18 23:15 사용자 "자막에는 마침표나 쉼표는 넣지 마, 물음표는 넣어도 돼" → 숫자 사이(2.24·1,000)만 남기고 지움
for _l in lines:
    _l['sub'] = re.sub(r'(?<!\d)[.,]|[.,](?!\d)', '', _l['sub']).replace('  ', ' ')
# 11/18 23:25 사용자 "45홈런 118타점 너무 정직하게 발음해 — 사.십.오.홈.런, 백.십.팔.타.점" → 합성 글(narr)에서 숫자와 단위를 붙인다(자막은 위에서 이미 만듦)
_NU = r'(?<![가-힣])([일이삼사오육칠팔구십백천]{2,}|[삼사오육칠팔구십백천]) (홈런|안타|타점|세이브|도루|승|패|표|할|푼|리|호)'
for _l in lines:
    _t = _l['narr']
    if '놈' in _t: continue   # 11/19 첫 줄은 붙이면 '사십오 할런'으로 들림 → 띄어 둠(썸네일러 채팅이 고친 것 이어받음)
    for _ in range(3):
        _t = re.sub(_NU, r'\1\2', _t)
        _t = re.sub(r'(할|푼) ([일이삼사오육칠팔구])', r'\1\2', _t)
        _t = re.sub(r'((?:할|푼)[일이삼사오육칠팔구]) (리|푼)', r'\1\2', _t)
    _l['narr'] = _t
# 11/18 23:30 사용자 "대항마 둘 알약 없애고, 이런 건 필요 없어 — 나레이션으로만 설명하면 돼" → 사진 줄 장면의 알약(cap) 전부 뺌
for _sc in scenes:
    if _sc.get('type') == 'photo_row': _sc['cap'] = None
# 11/19 사용자 "홈런을 할런이라고 발음"(김도영 시즌 기록 줄) + "고쳐 달라고 한 부분만 재합성, 나머지는 그대로" → 그 줄만 띄움
for _l in lines:
    if _l['narr'].startswith('김도영은 올해'): _l['narr'] = _l['narr'].replace('사십오홈런', '사십오 홈런')
lines[0]['sub'] = '45홈런 친 홈런놈|211안타 친 안타놈|그리고 투수 2관왕한 삼진놈|그리고 투수 2관왕한 삼진놈'; lines[0]['noMerge'] = True   # 11/19 01:37 대사는 이미 만든 음성(4마디) 그대로 — 셋째·넷째 마디에 같은 자막을 이어 붙여 한 덩이로 보이게
lines[0]['narr'] = '사십오 홈런 친 홈런놈, / 이백십일 안타 친 안타놈, / 그리고 투수 이관왕한 / 삼진놈'   # 11/19 이미 합성된 음성 글과 같게(재합성 없음)
# ── 11/18 17:02 사용자 "나레이션에서 가장 앞서 있다라고 할 때 그 카드가 맞춰서 나와야 하는데 싱크가 안 맞아. 다른 카드들도" ──
# 화면 글(도장·기록·막대·카드 아래 글)을 그 말이 들어 있는 자막 덩이에 맞춘다: 덩이 시작 0.15 앞(at = 덩이번호 - 0.15)
import re as _re
def _nm(t): return _re.sub(r'[\s·,.?!\'"“”()~→\-]', '', t or '')
def _bi(t): t = _nm(t); return {t[i:i + 2] for i in range(len(t) - 1)} | ({t} if len(t) == 1 else set())
def _sync_items(sc):
    for v in sc.get('viz', []) or []: yield v, 'at', v.get('t', '')
    for v in sc.get('stats', []) or []: yield v, 'at', v.get('k', '') + ' ' + str(v.get('v', ''))
    for c in sc.get('cards', []) or []:
        if c.get('subAt') is not None: yield c, 'subAt', c.get('sub', '')
        for v in c.get('stats', []) or []: yield v, 'at', v.get('k', '') + ' ' + str(v.get('v', ''))
    for v in sc.get('items', []) or []: yield v, 'at', ' '.join(str(v.get(k, '')) for k in ('label', 'd', 't', 'txt', 'sub'))
SYNC_LOG = []
for _i, _sc in enumerate(scenes):
    _ch = lines[_i]['sub'].replace('\n', ' ').split('|')
    _cand = []
    for _o, _key, _txt in _sync_items(_sc):
        _at = _o.get(_key)
        if _at is None or _at < 0 or _at >= 50: continue
        _b = _bi(_txt)
        if not _b: continue
        _sc_ = [len(_b & _bi(c)) / len(_b) for c in _ch]
        _k = max(range(len(_ch)), key=lambda x: _sc_[x])
        if _sc_[_k] < 0.5: continue
        _cand.append((_o, _key, _txt, _at, _k))
    for _o, _key, _txt, _at, _k in _cand:
        _fk, _fr = int(_at), _at - int(_at)
        _same = sum(1 for c in _cand if int(c[3]) == _k and c[4] == _k)
        if _fk == _k and _same >= 2: continue   # 한 덩이 안에서 이름을 차례로 부르는 목록(이승엽·선동열…)은 원래 순서 그대로
        if _fk > _k or (_fk == _k and _fr > 0.25) or _fk < _k - 1:
            _new = round(_k - 0.15, 2) if _k > 0 else 0.05
            SYNC_LOG.append((_i, _txt.strip(), _at, _new, _ch[_k])); _o[_key] = _new
TITLE = "2026 MVP 누가 받을까? | 김도영 45홈런 vs 레이예스 211안타 vs 곽빈 2관왕"
DESC = ("2026 KBO 정규시즌 MVP는 누가 받을까요? 홈런왕 김도영(KIA, 45홈런·장타율 1위), 한 시즌 최다 안타 신기록 레이예스(롯데, 211안타), 투수 2관왕 곽빈(두산, 평균자책점 2.24·탈삼진 197개)의 3파전을 기록·약점·역대 투표 흐름으로 정리했어요.\n"
        "MVP는 2026 KBO 리그를 취재한 기자들이 한 사람씩 투표해 가장 많은 표를 받은 선수가 받아요(투표는 정규시즌이 끝난 10월 13일부터). 가을야구 기록은 들어가지 않아요. "
        "역대 타자 MVP 26번 중 20번이 홈런왕이었고, 2014년 서건창은 201안타 신기록으로 MVP를 받았어요. 신인상 후보 허인서(한화)·문정빈(LG)·김민준(SSG)도 함께 봤어요. "
        "2025년 시상식은 11월 24일이었고, 2026년 시상식은 11월 26일(목) 오후 2시 서울 롯데호텔 월드에서 열려요. 결과 예상은 제 생각이에요.")
EP = {"theme": "mg", "date": "2026-11-18", "gameDate": "2026-10-12", "series": "야구롱폼", "focusTeam": "", "speed": 1.0,
      "ttsApi": True, "ttsVoice": "A", "ttsWhole": False, "ttsTempo": 1.2, "ttsTempoSlow": 1.15, "rev": "1118-mvp-v1", "topic": "2026MVP예상", "endcardSec": 10,
      "gapScale": 1.25, "pauseMax": 0.45, "sentPauseMin": 0.4, "clausePauseMin": 0.3,
      "ttsCharsOk": 7000, "totalSec": 481,   # 11/18 10:37 사용자 "엔딩 늘리고" → build 가 엔딩 카드를 늘려 전체 8분 1초
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False,
      "source": "대사 mvp18/script_v2.txt · 근거 = 주제전달-1118 · claude/MVP예상-대본v1-1118.md 출처",
      "youtube": {"title": TITLE, "description": DESC,
                  "cta": "김도영의 두 번째 MVP일까요? 아니면 곽빈이나 레이예스가 이변을 만들까요? 여러분은 누가 받아야 한다고 보세요?", "prev": "FA 첫날 10개 구단 지갑",
                  "tags": ["MVP", "2026 MVP", "KBO MVP", "김도영", "레이예스", "곽빈", "신인상", "허인서", "문정빈", "김민준", "힐리어드", "구자욱", "KBO 시상식", "프로야구", "KBO"],
                  "hashtags": ["#MVP", "#김도영", "#레이예스", "#곽빈", "#KBO"],
                  "teams": ["기아 타이거즈", "롯데 자이언츠", "두산 베어스", "KT 위즈", "삼성 라이온즈", "LG 트윈스", "한화 이글스", "SSG 랜더스"],
                  "players": ["김도영", "레이예스", "곽빈", "최원준", "김태형", "이병규", "양현종", "고영표", "임찬규", "페디", "폰세", "힐리어드", "오스틴", "구자욱", "김재윤", "소형준", "스기모토", "서건창", "박병호", "디아즈", "허인서", "문정빈", "김민준", "안현민"]}}
if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'episodes'), exist_ok=True)
    out = os.path.join(HERE, 'episodes', '2026-11-18_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for l in lines)
    print('ok', out, len(lines), '줄', len(scenes), '장면', '합성 글자', tot)
    for x in SYNC_LOG: print('싱크', x)
