# ══ 11/3 롯데 2027 스토브리그 — 기아 2027 편 틀(rf_card·rf_band·rf_duo·rf_gold·rf_bars·slotboard·capbar·말풍선), 색은 롯데(남색 + 빨강) ══
RED, GOLD, GRAY, GREEN = "#E5484D", "#E8A100", "#8A93A3", "#1F9D55"
P = {}
def ph(k): return P.get(k, k)
SC = {}
BG_LT = {"css": "linear-gradient(115deg,#060A14 0%,#0C1426 45%,#0A1E48 100%),repeating-linear-gradient(115deg,rgba(208,15,49,.10) 0 30px,rgba(0,0,0,0) 30px 90px)"}
BG_LTR = {"css": "linear-gradient(115deg,#0A0C14 0%,#141826 45%,#3A0A14 100%),repeating-linear-gradient(115deg,rgba(208,15,49,.09) 0 30px,rgba(0,0,0,0) 30px 90px)"}
BG_DK = {"css": "linear-gradient(115deg,#0B0C10 0%,#17181D 55%,#1C2232 100%),repeating-linear-gradient(115deg,rgba(208,15,49,.05) 0 30px,rgba(0,0,0,0) 30px 90px)"}
BG_GOLD = {"css": "radial-gradient(40% 60% at 22% 0%,rgba(255,200,90,.45),rgba(0,0,0,0) 70%),radial-gradient(40% 60% at 78% 0%,rgba(255,200,90,.40),rgba(0,0,0,0) 70%),radial-gradient(70% 50% at 50% 100%,rgba(120,80,20,.5),rgba(0,0,0,0) 70%),linear-gradient(180deg,#070A12,#17140C)"}
BAND_F = "contrast(1.2) saturate(1.1) brightness(.42)"
def BGI(k, f=BAND_F, pos="center 15%"): return dict(img=ph(k), pos=pos, f=f)
TEAM = "롯데"
def CARD(img, name, kicker, big=None, minor=None, team=TEAM, bg=None, **k):
    k.setdefault("focus", "50% 0%")   # 11/3 사용자 "머리 부분이 잘려" — 세로 사진은 맨 위부터
    return S(0, "rf_card", img=ph(img), name=name, team=team, kicker=kicker, big=big, minor=minor or [], bg=bg or BG_LT, noCenter=True, **k)
def BIGV(v, k, at, sub=None, size=None): return dict(dict(v=v, k=k, at=at), **({"sub": sub} if sub else {}), **({"size": size} if size else {}))
def MI(k, v, at): return dict(k=k, v=v, at=at)
def GOLD(img, name, en, profile, stats=None, team=TEAM, **k): return S(0, "rf_gold", img=ph(img), name=name, en=en, team=team, season="2026 SEASON", plist=profile, stats=stats or [], bg=BG_GOLD, noCenter=True, **k)
def BAND(who, vals, bgk=None, team=TEAM, bg=None, **k): return S(0, "rf_band", who=who, team=team, vals=vals, bg=bg or (BGI(bgk) if bgk else BG_LT), noCenter=True, **k)
def V(v, k, at, hi=False, size=None): return dict(dict(v=v, k=k, at=at, hi=hi), **({"size": size} if size else {}))
def DUO(title, cards, bgk=None, bg=None, **k): return S(0, "rf_duo", title=title, cards=cards, bg=bg or (BGI(bgk, "blur(22px) brightness(.4)") if bgk else BG_LT), noCenter=True, **k)
def DC(img, name, at, stats=None, team=TEAM, focus=None): return dict(dict(img=ph(img), name=name, team=team, at=at, stats=stats or []), **({"focus": focus} if focus else {}))
def DS(k, v, at, hi=False): return dict(k=k, v=v, at=at, hi=hi)
def RBARS(title, items, mx, bgk=None, glass=False, bg=None, **k): return S(0, "rf_bars", title=title, items=items, max=mx, glass=glass, bg=bg or (BGI(bgk, "blur(18px) brightness(.45) saturate(1.2)") if bgk else BG_LT), noCenter=True, **k)
def SLOT(title, slots, **k): return S(0, "slotboard", title=title, team=TEAM, slots=slots, noCenter=True, profile=k.pop("profile", True), **k)
def SL(img, name, pos, at=-1, **x): return dict(dict(img=ph(img) if img else None, name=name, pos=pos or "", at=at), **x)
def FG(title, items, **k): return S(0, "facegrid", title=title, items=items, noCenter=True, profile=True, whole=True, **k)
def FI(img, name, at, team=TEAM): return dict(img=ph(img), name=name, team=team, at=at)
def SP(img, name, bubbles, **k): return S(0, "speech", img=ph(img), name=name, bubbles=bubbles, **k)
def BB(date, text, at, hi=False): return dict(date=date, text=text, at=at, hi=hi)
def CAP(title, segs, **k): k.setdefault("chain", "cap"); return S(0, "capbar", title=title, segs=segs, max=500, **k)
def SEG(label, v, at, color=None): return dict(dict(label=label, v=v, at=at), **({"color": color} if color else {}))
def QQ(text, logos, **k): return S(0, "question", text=text, logos=logos, logoSize=k.pop('logoSize', 200), size=k.pop('size', 96), **k)
END_SC = QQ("야구자판기 · 매일 야구 이슈", ["KIA", "KT", "LG", "NC", "SSG", "두산", "롯데", "삼성", "키움", "한화"], logoSize=150, size=72)

P.update({
    "레이예스": "경기/레이예스_211안타_1012_롯데제공", "레이예스B": "경기/레이예스_세리머니_롯데제공_up", "레이예스C": "경기/레이예스_양손가리키기_롯데제공_up",
    "레이예스E": "경기/레이예스_타격_1012_롯데제공", "레이예스F": "경기/레이예스_하이파이브_롯데제공", "레이예스G": "경기/레이예스_미소_1006_롯데제공",
    "레이예스H": "경기/레이예스_두손_1007_롯데제공", "레이예스M": "카드/레이예스_MVP_세리머니", "레이예스T": "카드/T12_레이예스_미소", "레이예스R": "카드/R13_레이예스",
    "레이예스K": "KBO프로필/레이예스_롯데_원", "레이예스원": "카드/FA9원_레이예스",
    "로드리게스K": "KBO프로필/로드리게스_2026프로필_원", "로드리게스C": "카드/FA9_로드리게스", "로드리게스원": "카드/FA9원_로드리게스",
    "비슬리K": "KBO프로필/비슬리_2026프로필_원", "비슬리C": "카드/FA9_비슬리", "비슬리B": "경기/비슬리_박수_롯데제공", "비슬리원": "카드/FA9원_비슬리",
    "이이무라K": "KBO프로필/이이무라_2026롯데_원", "이이무라P": "KBO프로필/이이무라_2026롯데",
    "김태형": "카드/P30_김태형_롯데_1024_중앙", "김태형C": "카드/FA9_김태형",
    "이동욱": "카드/P30_이동욱_NC_2021_한겨레", "이동욱B": "카드/H14_이동욱", "이택근": "경기/이택근_단장_1026_롯데제공", "허문회": "카드/P30_허문회_롯데_2021_스포츠경향",
    "유강남K": "KBO프로필/유강남_원", "노진혁K": "KBO프로필/노진혁_원", "김진욱": "경기/김진욱_1011_롯데제공", "김진욱K": "KBO프로필/김진욱", "최준용K": "KBO프로필/최준용",
    "최충연K": "KBO프로필/최충연_롯데_원", "정성종K": "KBO프로필/정성종_롯데_원", "이인한K": "KBO프로필/이인한_롯데_원",
    "한동희": "경기/한동희_타격_0918_롯데제공", "전민재": "경기/전민재_세리머니_롯데제공", "황성빈": "경기/황성빈_도루_0715_OSEN",
    # ── 11/3 아침 다운로드(나무위키 KBO 프로필 얼굴 자르기 · SPOTV 9/21 드래프트, 워터마크 아래 잘라냄) ──
    "한현희K": "KBO프로필/한현희_롯데_원", "김민성K": "KBO프로필/김민성_롯데_원", "조원우": "경기/조원우_롯데코치_OSEN", "박근서": "경기/박근서_드래프트_0921_SPOTV",
})
def QT(src, text, **k): return S(0, "quote", src=src, text=text, **k)

# ── 오프닝 ──
SC['o1'] = DUO("롯데 2027 스토브리그", [DC("카드/FA9_레이예스", "레이예스", 0), DC("로드리게스C", "로드리게스", 0), DC("비슬리C", "비슬리", 0)])
SC['o2'] = BAND("2026 정규시즌", [V("64승 3무 77패", "승무패", 1, size=96), V("7위", "최종 순위", 2, hi=True, size=96)], bgk="전민재")
SC['o3'] = BAND("9월 30일", [V("9년 연속", "가을야구 탈락", 1), V("구단 최장", "2001~2007년 7년 연속 넘어", 2, hi=True)], bg=BG_LTR)
SC['o4'] = S(0, "toc", itemFrom=1)
# ── 1. 떠나는 사람 ──
SC['n1'] = BAND("떠나는 사람", [], bg=BG_LT)
SC['n2'] = CARD("김태형", "김태형", "감독", big=BIGV("3년", "계약 끝", 1, size=170), minor=[MI("10월 24일", "재계약 안 함", 2)], imgAt=1, nameAt=1)
SC['n3'] = BAND("김태형 감독 · 세 시즌", [V("7위", "2024년", 1), V("7위", "2025년", 1), V("7위", "2026년", 1, hi=True)], bg=BG_LTR)
REL = [FI("최충연K", "최충연", 0), FI("정성종K", "정성종", 0), FI("이인한K", "이인한", 1)]
SC['n4'] = BAND("10월 7일 · 재계약 불가 통보", [V("16명", "한꺼번에", 2, hi=True, size=120)], bg=BG_LTR)
SC['n5'] = FG("재계약 불가 16명 중", REL)
SC['n6a'] = QQ("은퇴하자마자 코치로", ["롯데"], size=84)
SC['n7'] = QQ("대형 FA 계약 세 개", ["롯데"], size=84)
FA3 = [SL("유강남K", "유강남", "포수"), SL("노진혁K", "노진혁", "내야수"), SL("한현희K", "한현희", "투수")]
def fa3(ats, tags, br, cont=True):
    sl = []
    for x, a, t in zip(FA3, ats, tags):
        d = dict(x, at=a)
        if t: d.update(tag=t[0], tagAt=t[1], tc="gold")
        sl.append(d)
    return SLOT("2022년 겨울 FA 영입", sl, chain="fa3", bracket=br, **({"cont": True} if cont else {}))
SC['n8'] = fa3([2, 2, 3], [None] * 3, dict(a=0, b=2, label="세 명 합계 170억 원", at=4, c="gold"), cont=False)
SC['n9'] = fa3([-1] * 3, [("4년 80억 원", 1), ("4년 50억 원", 2), ("최대 40억 원", 3)], dict(a=0, b=2, label="세 명 합계 170억 원", at=-1, c="gold"))
SC['n10'] = fa3([-1] * 3, [("4년 80억 원", -1), ("4년 50억 원", -1), ("최대 40억 원", -1)], dict(a=0, b=2, label="2026년 계약 끝", at=1, c="bad"))
SC['n11'] = BAND("유강남 · 노진혁 · 한현희", [V("부족", "1군 등록일수", 1), V("못 얻음", "FA 자격 재취득", 2, hi=True)], bg=BG_LTR)
SC['n12'] = BAND("세 명이 남으려면", [V("일반 연봉 계약", "새로 맺어야", 1, hi=True, size=110)])
SC['n13'] = BAND("세 FA 계약이 끝나면", [V("기회", "롯데에겐", 2), V("2027년부터", "쓸 수 있는 돈", 50, hi=True)], chain="n13")
SC['n13b'] = BAND("세 FA 계약이 끝나면", [V("기회", "롯데에겐", -1), V("2027년부터", "쓸 수 있는 돈", 0, hi=True)], chain="n13", cont=True, whoAt=-1)
SC['n14'] = CARD("김태형C", "김태형", "감독 · 3년 동안", big=BIGV("0명", "외부 FA 영입", 2, size=170), imgAt=0, nameAt=0)
SC['n14b'] = BAND("2026년 겨울 전망", [V("시장에 나선다", "외부 FA 영입", 1, hi=True, size=110)], bg=BG_LTR)
AGS = [SL("김진욱K", "김진욱", "투수"), SL("최준용K", "최준용", "투수")]
def ag(a, t, br=None, cont=True):
    sl = [dict(x, at=aa, tag="금메달", tagAt=tt, tc="gold") for x, aa, tt in zip(AGS, a, t)]
    return SLOT("2026 아시안게임 · 병역 해결", sl, chain="ag", **({"bracket": br} if br else {}), **({"cont": True} if cont else {}))
SC['n15a'] = ag([50, 50], [50, 50], cont=False)
SC['n15'] = ag([0, 0], [1, 1])
SC['n16'] = ag([-1, -1], [-1, -1], dict(a=1, b=1, label="상무 최종 합격 · 롯데 잔류", at=1, c="good"))
# ── 2. 외국인 세 명 ──
F3 = [SL("레이예스K", "레이예스", "타자"), SL("로드리게스K", "로드리게스", "투수"), SL("비슬리K", "비슬리", "투수")]
SC['f1'] = SLOT("2026 외국인 선수 세 명", [dict(x, at=50) for x in F3], chain="f3")
SC['f1b'] = SLOT("2026 외국인 선수 세 명", [dict(F3[0], at=0), dict(F3[1], at=1), dict(F3[2], at=1)], chain="f3", cont=True)
SC['f2'] = GOLD("레이예스R", "레이예스", "VICTOR REYES", ["외야수"], [dict(k="롯데에서", v="세 번째 시즌", at=1, hi=True, size=84)])
SC['f3'] = BAND("레이예스 · 2026 정규시즌", [V("144", "경기", 1, size=88), V("3할 6푼 3리", "타율", 2, hi=True, size=88), V("211", "안타", 3, size=88), V("18", "홈런", 3, size=88), V("109", "타점", 4, size=88)], bgk="레이예스E")
SC['f4'] = CARD("레이예스", "레이예스", "KBO 한 시즌 최다", big=BIGV("211", "안타", 0), minor=[MI("종전 기록", "2024년 202안타", 50)], chain="rec")
SC['f4a'] = CARD("레이예스", "레이예스", "KBO 한 시즌 최다", big=BIGV("211", "안타", -1), minor=[MI("종전 기록", "2024년 202안타", 1)], chain="rec", cont=True, imgAt=-1, nameAt=-1)
SC['f4b'] = BAND("레이예스 · 시즌 마지막 경기", [V("4안타", "몰아치기", 1), V("211개", "시즌 안타", 2, hi=True)], bgk="레이예스F")
SC['f5'] = CARD("레이예스M", "레이예스", "3년 연속 안타왕", big=BIGV("처음", "외국인 타자로는", 1, size=170))
SC['f6'] = BAND("레이예스 · 세 시즌", [V("600개", "안타 합계", 1, hi=True), V("전 경기", "빠짐없이 출전", 50)], bgk="레이예스C", chain="r600")
SC['f6b'] = BAND("레이예스 · 세 시즌", [V("600개", "안타 합계", -1, hi=True), V("전 경기", "빠짐없이 출전", 1)], bgk="레이예스C", chain="r600", cont=True, whoAt=-1)
SC['f7'] = SP("레이예스G", "레이예스", [BB("", "다음 시즌에도\n롯데에서 뛰고 싶다", 2, hi=True)])
SC['f8'] = QT("새 감독 이동욱", "3년 동안 600개의 안타를 친 선수와\n계약을 하지 않으면 안 된다", name="이동욱", role="감독")
SC['f9'] = CARD("레이예스T", "레이예스", "2026년 총액", big=BIGV("140만", "달러", 1), minor=[MI("2025년", "125만 달러", 50), MI("인상", "15만 달러", 50)], chain="f9")
SC['f9b'] = CARD("레이예스T", "레이예스", "2026년 총액", big=BIGV("140만", "달러", -1), minor=[MI("2025년", "125만 달러", 0), MI("인상", "15만 달러", 1)], chain="f9", cont=True, imgAt=-1, nameAt=-1)
SC['f10'] = BAND("외국인 투수", [V("2명", "재계약 고민", 1, hi=True, size=120)], bg=BG_LT)
SC['f10b'] = GOLD("로드리게스C", "로드리게스", "ELVIN RODRIGUEZ", ["투수"], [dict(k="일본 프로야구 거쳐", v="2026년 합류", at=1.5, size=72), dict(k="일본 프로야구 78이닝", v="평균자책점 2.77", at=50, size=72), dict(k="미국 마이너리그", v="747이닝", at=50, size=72)], chain="rod")
SC['f10c'] = GOLD("로드리게스C", "로드리게스", "ELVIN RODRIGUEZ", ["투수"], [dict(k="일본 프로야구 거쳐", v="2026년 합류", at=-1, size=72), dict(k="일본 프로야구 78이닝", v="평균자책점 2.77", at=0, size=72), dict(k="미국 마이너리그", v="747이닝", at=3, size=72)], chain="rod", cont=True)
SC['f11'] = BAND("로드리게스 · 2026 정규시즌", [V("29", "경기", 1), V("159⅔", "이닝", 2), V("10승 11패", "승패", 3), V("4.28", "평균자책점", 4, hi=True)], bg=BG_LT)
SC['f12'] = CARD("로드리게스C", "로드리게스", "롯데 선발 최다 이닝", big=BIGV("9월 30일", "시즌 조기 종료", 2, size=150), minor=[MI("오른쪽 척골", "신경 염증", 3)], imgAt=-1, nameAt=-1)
SC['f13'] = GOLD("비슬리C", "비슬리", "JEREMY BEASLEY", ["투수"], [dict(k="전 소속", v="한신 타이거스", at=50, hi=True, size=72)], chain="bea")
SC['f13b'] = GOLD("비슬리C", "비슬리", "JEREMY BEASLEY", ["투수"], [dict(k="전 소속", v="한신 타이거스", at=0, hi=True, size=72)], chain="bea", cont=True)
SC['f14'] = BAND("비슬리 · 2026 정규시즌", [V("27", "경기", 1), V("147", "이닝", 1), V("10승 8패", "승패", 2), V("4.96", "평균자책점", 3, hi=True)], bgk="비슬리B")
SC['f16'] = BAND("2026 선발 · 외국인 투수 두 명 포함", [V("다섯 명", "모두 규정이닝", 1, hi=True, size=120)], bg=BG_LT)
SC['f17'] = QT("이동욱 감독", "로드리게스, 비슬리가 괜찮은 활약\n단장님과 계속 소통하고 있다", name="이동욱", role="감독")
SEGS = [SEG("레이예스", 140, 0), SEG("로드리게스", 100, 0, "#3B4A63"), SEG("비슬리", 100, 0, "#E8A100")]
SC['f17q'] = CAP("외국인 선수 총액 한도", [], cap=400, capAt=50, capLabel="한도 400만 달러")
SC['f18'] = CAP("외국인 선수 총액 한도", [], cap=400, capAt=50, capLabel="한도 400만 달러", cont=True)
SC['f18b'] = CAP("외국인 선수 총액 한도", [], cap=400, capAt=1, capLabel="한도 400만 달러", cont=True)
SC['f19'] = CAP("외국인 선수 총액 한도", [], cap=400, capAt=-1, capLabel="한도 400만 달러", cont=True, text="재계약 연차마다 +10만 달러", textAt=2, size=60)
SC['f20'] = CAP("외국인 선수 총액 한도", [dict(x, at=1) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", cont=True, text="2026년 총액 합계 340만 달러", textAt=2, size=60)
SC['f21'] = CAP("외국인 선수 총액 한도", [dict(x, at=-1) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", ext=430, extAt=2, extLabel="레이예스 재계약 3년째 +30만 달러", cont=True, text="셋 다 재계약하면", textAt=0, size=60)
SC['f21a'] = CAP("외국인 선수 총액 한도", [dict(x, at=-1) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", ext=450, extAt=1, extLabel="두 투수 +10만 달러씩", cont=True, text="셋 다 재계약하면", textAt=-1, size=60)
SC['f21b'] = CAP("외국인 선수 총액 한도", [dict(x, at=-1) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", ext=450, extAt=-1, extLabel="2027년 한도 450만 달러", cont=True, text="셋 다 재계약하면", textAt=-1, size=60)
SC['f22'] = CAP("외국인 선수 총액 한도", [dict(x, at=-1) for x in SEGS], cap=400, capAt=-1, capLabel="한도 400만 달러", ext=450, extAt=-1, extLabel="2027년 한도 450만 달러", cont=True, text="여유 110만 달러", textAt=1, size=60)
EX = [SL("레이예스K", "레이예스", "타자", 1, tag="200만 달러", tagAt=1, tc="gold"), SL("로드리게스K", "로드리게스", "투수", 2, tag="100만 달러", tagAt=3, tc="gold"), SL("비슬리K", "비슬리", "투수", 2, tag="100만 달러", tagAt=3, tc="gold")]
SC['f23'] = SLOT("예시 · 2027년 한도 안에서", EX, bracket=dict(a=0, b=2, label="남는 돈 50만 달러", at=4, c="good"))
SC['f24'] = BAND("롯데의 고민", [V("실력", "돈보다", 2, hi=True, size=130)], bg=BG_LT)
SC['f24b'] = BAND("새 외국인 투수", [V("100만 달러", "첫해 최대", 1), V("같은 돈", "2026년 두 투수와", 2, hi=True)])
SC['f25a'] = QQ("아시아쿼터", ["롯데"], size=84)
SC['f27'] = BAND("아시아쿼터 재계약", [V("+10만 달러", "해마다 연봉 인상 가능", 2, hi=True, size=110)])
V3 = [SL("레이예스K", "레이예스", "타자"), SL("로드리게스K", "로드리게스", "투수"), SL("비슬리K", "비슬리", "투수")]
def verdict(sl_at, tags, cont=True, imgs=None):
    sl = [dict(x) for x in V3]
    if imgs: sl = [dict(x, img=ph(i)) for x, i in zip(sl, imgs)]
    for i, (a, t) in enumerate(zip(sl_at, tags)):
        sl[i]["at"] = a
        if t: sl[i].update(tag=t[0], tagAt=t[1], tc=t[2])
    return SLOT("2027 외국인 재계약 전망", sl, chain="vd" if not imgs else "vd2", **({"cont": True} if cont else {}))
SC['f28'] = verdict([50, 50, 50], [None] * 3, cont=False)
SC['f29'] = verdict([0, 50, 50], [("잔류 유력", 1, "good"), None, None])
SC['f29b'] = verdict([-1, 50, 50], [("잔류 유력", -1, "good"), None, None])
SC['f30'] = verdict([-1, 0, 50], [("잔류 유력", -1, "good"), ("잔류 쪽", 1, "good"), None])
SC['f30b'] = verdict([-1, -1, 50], [("잔류 유력", -1, "good"), ("잔류 쪽", -1, "good"), None])
SC['f31'] = verdict([-1, -1, 0], [("잔류 유력", -1, "good"), ("잔류 쪽", -1, "good"), ("반반", 1, "bad")])
SC['f31a'] = RBARS("평균자책점 · 2026", [dict(label="비슬리", v=4.96, at=0, dec=2, hi=True), dict(label="로드리게스", v=4.28, at=1, dec=2)], 6, brk=dict(a=0, b=1, lab="+0.68", at=2))
SC['f32'] = SLOT("아시아쿼터 재계약 전망", [SL("이이무라K", "이이무라", "투수", 0, tag="잔류 가능성", tagAt=2, tc="good")])
# ── 3. 들어오는 사람 ──
SC['i1'] = BAND("들어오는 사람", [], bg=BG_LT)
SC['i6c'] = BAND("새 단장", [], bg=BG_LT)
SC['i11'] = BAND("2027 신인 드래프트", [], bg=BG_LT)
SC['i3'] = BAND("이동욱 감독 · 계약", [V("3년", "기간", 0), V("20억 원", "총액", 0, hi=True), V("5억 원", "계약금", 2), V("5억 원", "연봉", 2)])
SC['i4'] = CARD("이동욱B", "이동욱", "감독", big=BIGV("2020년", "NC 통합 우승", 1, size=150), minor=[MI("1997년", "롯데 입단", 50), MI("친정", "복귀", 50)], chain="ldw")
SC['i4b'] = CARD("이동욱B", "이동욱", "감독", big=BIGV("2020년", "NC 통합 우승", -1, size=150), minor=[MI("1997년", "롯데 입단", 0), MI("친정", "복귀", 2)], chain="ldw", cont=True, imgAt=-1, nameAt=-1)
SC['i5'] = QT("10월 31일 · 이동욱 감독 취임식", "공격은 팬을 부르고\n수비는 승리를 부른다", name="이동욱", role="감독")
SC['i5a'] = BAND("이동욱 감독이 내건 말", [V("스마트한 야구", "새 야구 색깔", 1, hi=True, size=110)])
SC['i5b'] = BAND("스마트한 야구", [V("데이터", "준비", 0, size=96), V("기본기", "루틴", 1, size=96), V("원팀", "신뢰 · 소통", 2, hi=True, size=96)])
SC['i6'] = BAND("마무리 캠프 · 일본 미야자키", [V("11월 4일", "시작", 1), V("수비 강화", "훈련", 2, hi=True)], bg=BG_LTR)
SC['i8'] = QT("이택근 단장", "현장의 우려를\n충분히 안다", chain="ltq")
SC['i9'] = SP("이택근", "이택근", [BB("", "현장의 우려를\n충분히 안다", -1, hi=True), BB("", "좋은 선수가 있으면\n영입을 요청할 생각", 0)], chain="ltg", cont=True)
CO = [SL("이동욱", "이동욱", "감독"), SL("허문회", "허문회", "수석코치"), SL("조원우", "조원우", "외야 수비코치")]
SC['i10'] = SLOT("1군 · 감독 출신 세 명", [dict(x, at=50) for x in CO], chain="co", profile=False)
SC['i10b'] = SLOT("1군 · 감독 출신 세 명", [dict(CO[0], at=0), dict(CO[1], at=1), dict(CO[2], at=2)], chain="co", cont=True, profile=False)
SC['i12'] = CARD("박근서", "박근서", "서울디자인고 · 왼손 투수", big=BIGV("전체 4순위", "지명", 3, size=130), minor=[MI("2027 신인 드래프트", "1라운드", 1)], imgAt=2, nameAt=2, chain="pgs")
SC['i13'] = CARD("박근서", "박근서", "서울디자인고 · 왼손 투수", big=BIGV("149km", "최고 구속", 2), minor=[MI("키", "188cm", 1)], imgAt=-1, nameAt=-1, chain="pgs", cont=True)
SC['i14'] = BAND("2027 신인 드래프트", [V("11명", "지명", 1, hi=True, size=120)])
SC['i15'] = BAND("롯데가 노리는 외부 FA", [V("없음", "아직 보도 전", 1, hi=True, size=120)], bg=BG_LTR, chain="cf")   # 11/3 사용자 '이름 없음 말고 그냥 없음'
SC['i16'] = BAND("언론의 지적", [V("중견수 수비", "약점", 0, hi=True, size=120)], chain="cf2")
SC['i17'] = BAND("FA 한 명을 데려온다면", [V("수비 좋은 중견수", "가장 급함", 2, hi=True, size=104)], chain="cf3", ghost=dict(img="카드/F16_김호령_A", at=2, op=.3, focus="50% 8%", hold=2))   # 11/3 사용자 '농담하듯 김호령 사진을 은은하게'
# ── 4. 2027년 롯데 ──
SC['p1'] = BAND("2027년 예상", [], bgk="전민재")
SC['p1b'] = BAND("2026 상반기", [V("6승 14패", "4월 22일까지 · 꼴찌", 1), V("최하위", "6월 다시", 3, hi=True)], bg=BG_LTR)
GN = lambda a1, a2, s1, s2: [DC("한동희", "한동희", a1, [DS("홈런", "25개 · 개인 최다", s1)]), DC("황성빈", "황성빈", a2, [DS("도루", "55개 · 도루왕", s2)])]
SC['p3'] = BAND("2026 약점", [V("113개", "팀 홈런 · 10개 구단 최하위", 0), V("107개", "실책", 2, hi=True)], bg=BG_LTR)
SC['p4'] = CARD("이동욱B", "이동욱", "감독", big=BIGV("수비", "첫 과제", 1, size=170))
SC['p5'] = SP("이택근", "이택근", [BB("", "다음 시즌엔 되냐고 물으면\n할 수 있습니다", 1, hi=True)])
KEY = [SL("레이예스K", "레이예스", "잔류"), SL(None, "외국인 투수", "더 강하게"), SL(None, "FA", "수비 좋은 선수")]
SC['p6'] = SLOT("2027 열쇠 세 가지", [dict(x, at=50) for x in KEY], chain="key")
SC['p7'] = SLOT("2027 열쇠 세 가지", [dict(KEY[0], at=0), dict(KEY[1], at=1), dict(KEY[2], at=50)], chain="key", cont=True)
SC['p8'] = SLOT("2027 열쇠 세 가지", [dict(KEY[0], at=-1), dict(KEY[1], at=-1), dict(KEY[2], at=2, tag="170억 원 끝난 돈으로", tagAt=1, tc="gold")], chain="key", cont=True)
SC['p9'] = BAND("세 가지가 다 되면", [V("10년 만", "가을야구 도전", 1, hi=True, size=120)], bgk="레이예스B")
SC['p10'] = BAND("투수 그대로 · FA 없으면", [V("비슷함", "2026년과", 2, hi=True, size=120)], bg=BG_LTR)
SC['p11'] = QT("이동욱 감독", "부산에서 꼭\n가을잔치에 나가고 싶다", name="이동욱", role="감독")
SC['p12'] = verdict([1, 2, 3], [("잔류 유력", 1, "good"), ("잔류 쪽", 2, "good"), ("반반", 3, "bad")], cont=False)
SC['p12']['chain'] = "vd2"
SC['q1'] = QQ("2027 롯데\n10년 만의 가을야구?", ["롯데"], size=88)

SC['f19b'] = CAP("외국인 선수 총액 한도", [], cap=400, capAt=-1, capLabel="한도 400만 달러", cont=True, text="넘기면 · 처음엔 초과분의 50% 제재금", textAt=1, size=60)
SC['f27c'] = QQ("외국인 보유 확대 검토", ["KBO"], size=84)
SC['f27d'] = BAND("KBO 이사회 · 10월 7일", team=None, vals=[V("검토", "외국인 보유 제한 완화", 3, hi=True), V("미정", "규모 · 시기", 50)], bg=BG_LTR, chain="kbo")
SC['f27e'] = BAND("KBO 이사회 · 10월 7일", team=None, vals=[V("검토", "외국인 보유 제한 완화", -1, hi=True), V("미정", "규모 · 시기", 1)], bg=BG_LTR, chain="kbo", cont=True, whoAt=-1)
SC['i4c'] = QT("이동욱 감독 · 20년 만의 롯데 복귀", "강산이 두 번 변했다", name="이동욱", role="감독")
SC['i5']['chain'] = "q31"
SC['i5c'] = QT("10월 31일 · 이동욱 감독 취임식", "수비는 승리를 위해 팀 전체가 공유하는\n철학이자 기본이 되어야 한다", name="이동욱", role="감독", chain="q31", cont=True)
SC['i6b'] = BAND("이동욱 감독 · 취임 직후", [V("직접 지도", "선수들 수비", 3, hi=True, size=120)])
SC['i8b'] = QT("이택근 단장", "단장은 절대\n가벼운 자리가 아니다", chain="ltq", cont=True)
SC['i9'] = QT("이택근 단장", "좋은 선수가 있으면\n영입을 요청할 생각", chain="ltq", cont=True)
SC['i9c'] = QT("이택근 단장", "데이터 분석이 너무 잘돼 있어\n깜짝 놀랐다", chain="ltq", cont=True)
SC['i13b'] = BAND("2027 신인 드래프트 날", [V("라 밤바", "박근서 아버지의 노래", 2, hi=True, size=120)])
GN = lambda a1, a2, s1, s2: [DC("한동희", "한동희", a1, [DS("홈런", "25개 · 개인 최다", s1)]), DC("황성빈", "황성빈", a2, [DS("도루", "55개 · 도루왕", s2)])]
SC['f27f'] = BAND("보유 인원이 늘어나면", team=None, vals=[V("세 명 모두", "붙잡고도", 1), V("더 쓸 수 있음", "외국인 선수", 2, hi=True)], bg=BG_LTR)
SC['f33'] = BAND("레이예스 · 외국인 정리", [V("붙잡기", "당연", 0), V("선택", "두 투수", 1, hi=True)], bgk="레이예스C")
SC['f25'] = SLOT("아시아쿼터 · 6월 교체 영입", [SL("이이무라K", "이이무라", "투수", 2, tag="7만 달러", tagAt=3, tc="gold", note="일본 · 대만 실업팀 → 첫 프로 무대", noteAt=50)], chain="iim")
SC['f26'] = SLOT("아시아쿼터 · 6월 교체 영입", [SL("이이무라K", "이이무라", "투수", -1, tag="7만 달러", tagAt=-1, tc="gold", note="일본 · 대만 실업팀 → 첫 프로 무대", noteAt=1)], chain="iim", cont=True)
SC['f31b'] = BAND("비슬리", [V("교체 후보", "더 나은 투수가 보이면", 1, hi=True, size=110)], bgk="비슬리B")
SC['i2'] = CARD("이동욱", "이동욱", "제22대 감독", big=BIGV("10월 26일", "선임", 0, size=150), imgAt=1, nameAt=1, focus="50% 0%")
SC['i7'] = CARD("이택근", "이택근", "새 단장", big=BIGV("1,621안타", "선수 시절", 2, size=150), minor=[MI("소속", "현대 · LG · 히어로즈", 1)], imgAt=2, nameAt=2)
SC['i9b'] = QT("이택근 단장 · 2027년 계획", "사직구장보다\n2군을 더 챙기겠다", chain="ltq", cont=True)
SC['i18'] = BAND("들어오는 사람 정리", [V("수비", "새 감독 · 코치진", 1), V("외부 FA", "남은 숙제", 2, hi=True)], bg=BG_LTR)
GN = lambda a1, a2, s1, s2, s3, s4: [DC("한동희", "한동희", a1, focus="50% 6%", stats=[DS("개인 최다", "25홈런", s1), DS("2022년 이후 롯데", "첫 20홈런", s3)]), DC("황성빈", "황성빈", a2, focus="28% 40%", stats=[DS("도루왕", "55도루", s2), DS("데뷔 첫", "개인 타이틀", s4)])]
SC['p2a'] = DUO("2026 좋은 소식", GN(50, 50, 50, 50, 50, 50), chain="gn", reserveStats=True)
SC['p2'] = DUO("2026 좋은 소식", GN(0, 3, 1, 3, 50, 50), chain="gn", cont=True, reserveStats=True)
SC['p2b'] = DUO("2026 좋은 소식", GN(-1, -1, -1, -1, 50, 1), chain="gn", cont=True, reserveStats=True)
SC['p2c'] = DUO("2026 좋은 소식", GN(-1, -1, -1, -1, 1, -1), chain="gn", cont=True, reserveStats=True)
SC['q0'] = QQ("여러분은 어떻게 보세요?", ["롯데"], size=88)
SC['n17'] = BAND("떠나는 사람 정리", [V("자리", "새로 채울", 2), V("돈", "함께 생김", 3, hi=True)], bg=BG_LTR)
SC['f15'] = BAND("로드리게스 · 비슬리 2026년 총액", [V("100만 달러", "똑같이", 1, hi=True, size=120)])
SC['n6'] = SLOT("은퇴 · 코치 내정", [SL("김민성K", "김민성", "내야수", 0, tag="1군 내야 수비코치", tagAt=2, tc="gold", note="10월 9일 사직 은퇴식", noteAt=1)])
