# ════ 10/31 03:10 v10: 사용자 "텍스트로 떼우지 말고 모션그래픽·인포그래픽·애니메이션으로 싹 갈아엎어" + "같은 장면이면 사라졌다 다시 나타나지 마" ════
# 글 카드(pstat 기록 글·tiles·이름 카드) → rally(카드가 뒤집히며 나오는 공격 흐름+숫자 띠), hrcam(타구 비행), plog(이닝 칸·실점 공),
# faceoff(두 사진 고정 + 막대가 자라는 비교), wdl(승패 칸), statbars(양쪽 막대), podium(순위 단상). 같은 틀이 이어지는 곳은 chain+cont 로 사진·틀 고정.
def PL(img, name, team, res, kind, at, **k): return dict(dict(name=name, img=P.get(img, img), team=team, res=res, kind=kind, at=at), **k)
def TA(k, v, at, hi=False): return dict(k=k, v=v, at=at, hi=hi)
def RL(title, plays, tally, **k): return S(0, "rally", title=title, plays=plays, tally=tally, noCenter=True, **k)
def PLOG(img, name, team, sub, blocks, **k): return S(0, "plog", img=P.get(img, img), name=name, team=team, sub=sub, blocks=blocks, noCenter=True, **k)
def WDL(title, rows, **k): return S(0, "wdl", title=title, rows=rows, noCenter=True, **k)
def SB(title, rows, **k): return S(0, "statbars", title=title, left="삼성", right="KIA", rows=rows, noCenter=True, **k)
GM5 = GM + [('5차전', '대구', '삼성', None)]
def ser5(done, at5=0.5, **k):
    g = [dict(n=n, venue=v, home=h, win=(w if j < done else None), at=-1) for j, (n, v, h, w) in enumerate(GM5)]
    g[4]['at'] = at5
    return S(0, "series5", title="플레이오프 · 삼성 vs KIA", games=g, chain="ser5", noCenter=True, **k)

# ── 오프닝: 2:2 장면 두 개는 같은 틀로 이어 붙임(글만 교체) ──
SC['o2'] = S(0, "matchup", left="삼성", right="KIA", score="2 : 2", text="플레이오프 5차전 · 11월 1일 대구", tag="한국시리즈행 마지막 경기")
SC['o3'] = S(0, "matchup", left="삼성", right="KIA", score="2 : 2", text="이긴 팀 → 한국시리즈 vs KT", tag="한국시리즈행 마지막 경기")

# ── 1~3차전 흐름 ──
SC['r1'] = WDL("2026 정규시즌 · KIA의 삼성전", [dict(team="KIA", w=9, l=7, at=1.0, c="good", tag="KIA 우세", tagAt=2.0)])
SC['r2'] = S(0, "podium", title="2026 정규시즌 최종 순위", items=[dict(medal="금", team="KT"), dict(medal="은", team="삼성", hi=True), dict(medal="동", team="KIA", hi=True)], noCenter=True)
SC['r3'] = WDL("정규시즌 마지막 10경기", [dict(team="삼성", w=4, l=6, at=0, c="bad", tag="4연패로 마감", tagAt=1.0), dict(team="KIA", w=7, l=3, at=2.0, c="good")])
SC['f3'] = RL("1차전 · 대구", [PL("카스트로", "카스트로", "KIA", "투런 홈런", "run", 0.1)], [TA("카스트로 타점", 3, 2.0, True), TA("삼성 안타", 2, 4.0)])
SC['f3b'] = RL("1차전 · KIA 마운드", [PL("네일", "네일", "KIA", "선발 · 1실점", "def", 0.1), PL("이의리", "이의리", "KIA", "승리투수", "def", 2.0)], [TA("네일 실점", 1, 1.0)])
SC['f6'] = RL("2차전 · 삼성 공격", [PL("구자욱", "구자욱", "삼성", "결승 적시타", "run", 50), PL("디아즈", "디아즈", "삼성", "투런 홈런", "run", 0.2), PL("최형우G", "최형우", "삼성", "솔로 홈런", "run", 1.0)], [TA("삼성 득점", 8, 0.5, True)], chain="r2g")
SC['f6b'] = RL("2차전 · 삼성 공격", [PL("구자욱", "구자욱", "삼성", "결승 적시타", "run", 1.0), PL("디아즈", "디아즈", "삼성", "투런 홈런", "run", -1), PL("최형우G", "최형우", "삼성", "솔로 홈런", "run", -1)], [TA("삼성 득점", 8, -1, True)], chain="r2g", cont=True)
SC['f7b'] = PLOG("최원태", "최원태", "삼성", "삼성 선발 · 3차전", [dict(type="inn", ip=5 / 3, at=2.0)], stamp=dict(t="조기 강판", at=3.0), imgAt=1.0)
SC['f7c'] = PLOG("시라카와", "시라카와", "KIA", "KIA 선발 · 3차전", [dict(type="inn", ip=13 / 3, at=1.0), dict(type="runs", n=4, at=1.3)], imgAt=0)
SC['f9'] = RL("3차전 · 홈런", [PL("디아즈", "디아즈", "삼성", "홈런", "run", 1.0), PL("류지혁", "류지혁", "삼성", "홈런", "run", 1.2), PL("김도영B", "김도영", "KIA", "홈런", "run", 2.0), PL("나성범", "나성범", "KIA", "홈런", "run", 2.2)], [TA("삼성 홈런", 2, 1.4), TA("KIA 홈런", 2, 2.4)])
SC['f10'] = S(0, "rally", bug=dict(inn="7회초", score=[4, 4], outs=2, bases=[None, "주자", None], away="삼성", home="KIA"),
              plays=[PL("박승규", "박승규", "삼성", "결승 2루타", "run", 1.0, bases=[None, "박승규", None], outs=2, score=[5, 4], rbi="+1")], noCenter=True)

# ── 4차전 승부처 ──
SC['g2'] = RL("2회초 · 삼성 공격", [PL("김영웅", "김영웅", "삼성", "안타", "on", 0.1), PL("강민호", "강민호", "삼성", "연속 안타", "on", 0.4), PL("류지혁", "류지혁", "삼성", "우전 적시타", "run", 1.0)], [TA("삼성", 1, 2.0, True), TA("KIA", 0, 2.0)])
SC['g5'] = RL("4회말 · KIA 공격", [PL("김도영B", "김도영", "KIA", "2루타", "on", 0.1), PL("나성범", "나성범", "KIA", "몸에 맞는 공", "on", 1.0), PL("한준수", "한준수", "KIA", "동점 적시타", "run", 3.0)], [TA("삼성", 1, -1), TA("KIA", 1, 4.0, True)])
SC['p1'] = PLOG("페덱", "페덱", "삼성", "삼성 선발 · 4차전", [dict(type="inn", ip=16 / 3, at=1.0), dict(type="runs", n=1, at=1.3), dict(type="line", items=[["1차전", "5실점", True]], at=2.0)])
SC['p3'] = PLOG("네일", "네일", "KIA", "KIA 선발 · 4차전", [dict(type="line", items=[["휴식", "사흘", False]], at=1.0), dict(type="inn", ip=5, at=2.0), dict(type="runs", n=1, at=2.3)])
_hr6 = dict(img=P["최형우G"], name="최형우", team="삼성", bug=dict(inn="6회초", score=[1, 1], outs=1, bases=[None, None, None], away="삼성", home="KIA"), burst="솔로 홈런", runners=["최형우"], scoreTo=[2, 1], chain="hr6", noCenter=True)
SC['g7'] = S(0, "hrcam", launchAt=2.0, **_hr6)
SC['g8'] = S(0, "hrcam", launchAt=2.0, launchLine=KEYS.index('g7') if 'g7' in KEYS else 31, cont=True, **_hr6)
SC['g9'] = S(0, "hrcam", launchAt=2.0, launchLine=KEYS.index('g7') if 'g7' in KEYS else 31, cont=True, **_hr6)
_r7a = lambda a, b, c, d, e, ks: RL("7회말 · KIA 공격", [PL("김영웅", "김영웅", "삼성", "3루수 실책", "out", a), PL("김도영B", "김도영", "KIA", "실책 출루", "on", b), PL("카스트로", "카스트로", "KIA", "동점 안타", "run", c), PL("김선빈", "김선빈", "KIA", "안타", "on", d)], [TA("삼성", 2, -1), TA("KIA", 2, ks, True)], chain="r7a", **e)
SC['g13'] = _r7a(0.1, 0.6, 50, 50, {}, 50)
SC['g14'] = _r7a(-1, -1, 0.2, 3.0, dict(cont=True), 2.0)
_r7b = lambda a, b, k3, k4, e: RL("7회말 · 투 아웃 1·3루", [PL("한준수", "한준수", "KIA", "역전 적시타", "run", a), PL("하주석", "하주석", "KIA", "적시타", "run", b)], [TA("삼성", 2, -1), TA("KIA", 3, k3, True)] if k4 is None else [TA("삼성", 2, -1), TA("KIA", 4, k4, True)], chain="r7b", **e)
SC['g15'] = _r7b(1.0, 50, 3.0, None, {})
SC['g16'] = _r7b(-1, 0.1, None, 1.0, dict(cont=True))
SC['g18'] = PLOG("사토시", "사토시", "삼성", "삼성 투수 · 7회", [dict(type="runs", n=3, at=2.2), dict(type="zero", k="자책점", stamp="비자책", at=3.0)], imgAt=2.0)
SC['g20'] = RL("4차전 · 삼성 수비", [PL("디아즈", "디아즈", "삼성", "실책", "out", 1.0), PL("류지혁", "류지혁", "삼성", "실책", "out", 1.2), PL("김영웅", "김영웅", "삼성", "실책", "out", 1.5)], [TA("실책", 3, 2.0, True), TA("실점", 4, 3.0), TA("자책점", 1, 3.3)])
SC['g26'] = PLOG("전상현", "전상현", "KIA", "KIA 투수 · 4차전", [dict(type="inn", ip=2, at=1.0), dict(type="zero", k="피안타", stamp="세이브", at=2.0)], imgAt=1.0)
SC['f11'] = SB("플레이오프 네 경기", [dict(k="득점", l="17", r="16", lv=17, rv=16, lAt=1.0, rAt=1.2), dict(k="안타", l="28", r="32", lv=28, rv=32, lAt=3.0, rAt=2.0)])
SC['f13'] = ser5(4, 50, text="대구 1승 1패", textAt=1.0)
SC['f14'] = ser5(4, 0.3, text="대구 1승 1패", textAt=-1, cont=True)

# ── 5차전 선발: 후라도·올러 사진은 한 번 뜬 뒤 끝까지 고정, 줄만 늘어난다 ──
_FL = dict(img=P["후라도"], name="후라도", team="삼성", role="삼성 선발")
_FR = dict(img=P["올러"], name="올러", team="KIA", role="KIA 선발")
_ROWS = [dict(k="정규시즌", l="24경기\n9승 3패", r="30경기\n11승 10패"),
         dict(k="이닝", l="150", r="178", lv=150, rv=178),
         dict(k="퀄리티\n스타트", l="17경기", r="19경기", lv=17, rv=19),
         dict(k="평균자책점", l="3.54", r="3.13", lv=3.54, rv=3.13, low=True),
         dict(k="2차전 이닝", l="6⅔", r="4⅔", lv=6.67, rv=4.67),
         dict(k="2차전 실점", l="2실점 · 승", r="5실점 · 패", lv=2, rv=5, low=True)]
def FO(show, new_at, cont=True):
    rows = []
    for i, r in enumerate(_ROWS):
        if i < show: rows.append(dict(r, at=-1))
        elif i in new_at: rows.append(dict(r, at=new_at[i]))
        else: rows.append(dict(r, at=50, hide=True))
    return S(0, "faceoff", title="후라도 vs 올러", left=_FL, right=_FR, rows=rows, chain="fo5", noCenter=True, **(dict(cont=True) if cont else {}))
SC['s1b'] = FO(0, {0: 1.0}, cont=False)
SC['s1c'] = FO(1, {1: 1.0})
SC['s1d'] = FO(2, {2: 1.0})
SC['s7'] = FO(3, {3: 1.0})
SC['s2'] = FO(4, {})
SC['s3'] = FO(4, {4: 1.0, 5: 4.0})
SC['s8'] = ser5(4, 1.0, text="5차전 · 대구", textAt=1.0)
SC['s8b'] = PLOG("올러B", "올러", "KIA", "KIA 선발 · 대구", [dict(type="line", items=[["대구 두 경기", "13실점", True]], at=1.0)], chain="olr")
SC['s9'] = PLOG("올러B", "올러", "KIA", "정규시즌 삼성전", [dict(type="line", items=[["평균자책점", "5.79", True]], at=0.3), dict(type="line", items=[["광주 두 경기", "13이닝", False, 2.0], ["실점", "1", False, 3.0]], at=2.0)], chain="olr")
SC['s11'] = PLOG("올러B", "올러", "KIA", "대구 성적", [dict(type="line", items=[["7월 28일 · 1이닝", "8실점", True, 0.3]], at=0.3), dict(type="runs", n=8, at=1.0), dict(type="line", items=[["플레이오프 2차전까지", "13실점", True, 3.0]], at=3.0)], chain="olr")
SC['h1'] = SB("2026 정규시즌", [dict(k="승패", l="삼성 홈\n43승 29패", r="KIA 원정\n37승 34패", lv=43, rv=37, lAt=1.0, rAt=50)], chain="ha")
SC['h2'] = SB("2026 정규시즌", [dict(k="승패", l="삼성 홈\n43승 29패", r="KIA 원정\n37승 34패", lv=43, rv=37, lAt=-1, rAt=1.0)], chain="ha", cont=True)
_HR = [dict(type="line", items=[["정규시즌 KIA전", "5월 15일 · 대구", False, 1.0]], at=1.0), dict(type="inn", ip=7, at=3.0), dict(type="line", items=[["피안타", "10개", True, 3.2]], at=3.2)]
SC['s13'] = PLOG("후라도B", "후라도", "삼성", "삼성 선발 · 5차전", [dict(type="line", items=[["불안한 구석", "", False]], at=50)], stamp=dict(t="불안한 구석", at=1.0), chain="hrd")
SC['s14'] = PLOG("후라도B", "후라도", "삼성", "정규시즌 KIA전", _HR, chain="hrd")
SC['s16'] = PLOG("후라도B", "후라도", "삼성", "정규시즌 마지막 두 경기", [dict(type="line", items=[["10월 5일 두산전", "6실점", True, 2.0], ["10월 11일 KT전", "6실점", True, 3.0]], at=2.0), dict(type="runs", n=12, at=4.0)], chain="hrd")
SC['s18'] = PLOG("후라도B", "후라도", "삼성", "플레이오프 2차전", [dict(type="inn", ip=20 / 3, at=1.0), dict(type="runs", n=2, at=2.0)], stamp=dict(t="KIA 타선 봉쇄", at=2.5), chain="hrd")
SC['s19'] = FO(6, {}, cont=False)
# 고침: 나레이션에 없는 숫자 빼기 / 말한 숫자는 화면에
SC['f3b'] = RL("1차전 · KIA 마운드", [PL("네일", "네일", "KIA", "4⅓이닝 1실점", "def", 0.1), PL("이의리", "이의리", "KIA", "승리투수", "def", 2.0)], [TA("네일 실점", 1, 1.0)])
SC['f6'] = RL("2차전 · 삼성 공격", [PL("구자욱", "구자욱", "삼성", "3회 결승 적시타", "run", 50), PL("디아즈", "디아즈", "삼성", "3회 투런 홈런", "run", 0.2), PL("최형우G", "최형우", "삼성", "7회 솔로 홈런", "run", 1.0)], [TA("홈런", 2, 1.2, True)], chain="r2g")
SC['f6b'] = RL("2차전 · 삼성 공격", [PL("구자욱", "구자욱", "삼성", "3회 결승 적시타", "run", 1.0), PL("디아즈", "디아즈", "삼성", "3회 투런 홈런", "run", -1), PL("최형우G", "최형우", "삼성", "7회 솔로 홈런", "run", -1)], [TA("홈런", 2, -1, True)], chain="r2g", cont=True)
SC['s8b'] = PLOG("올러B", "올러", "KIA", "KIA 선발 · 5차전", [], stamp=dict(t="대구에서 약했다", at=1.0), chain="olr")
SC['s9'] = PLOG("올러B", "올러", "KIA", "정규시즌 삼성전", [dict(type="line", items=[["평균자책점", "5.79", True, 1.0]], at=1.0), dict(type="line", items=[["광주 두 경기", "13이닝", False, 2.0], ["실점", "1", False, 3.0]], at=2.0)], chain="olr")
SC['s13'] = PLOG("후라도B", "후라도", "삼성", "삼성 선발 · 5차전", [], stamp=dict(t="불안한 구석", at=1.0), chain="hrd")
SC['s16'] = PLOG("후라도B", "후라도", "삼성", "정규시즌 마지막 두 경기", [dict(type="line", items=[["10월 5일 두산전", "6실점", True, 2.0], ["10월 11일 KT전", "6실점", True, 3.0]], at=2.0)], chain="hrd")
SC['s18'] = PLOG("후라도B", "후라도", "삼성", "플레이오프 2차전", [dict(type="line", items=[["2차전", "승리투수", False, 1.0]], at=1.0)], stamp=dict(t="KIA 타선 봉쇄", at=2.0), chain="hrd")

# ── 불펜 운용 ──
SC['b1b'] = ser5(4, 0.3, text="지면 탈락", textAt=1.0)
_sb = lambda a, b, c, t, e: RL("5차전 · 삼성 마운드", [PL("후라도B", "후라도", "삼성", "선발", "def", a), PL("원태인", "원태인", "삼성", "3차전 1⅔이닝 · 승", "on", b), PL("이승민", "이승민", "삼성", "네 경기 모두 등판", "on", c)], t, chain="sbp", **e)
SC['b5'] = _sb(0.2, 50, 50, [TA("불펜 대기", 0, 50)], {})
SC['b13'] = _sb(-1, 3.0, 50, [TA("불펜 대기", 0, 50)], dict(cont=True))
SC['b9'] = _sb(-1, -1, 0.2, [TA("세 경기씩 던진 투수", 3, 2.0, True)], dict(cont=True))
SC['b6'] = S(0, "question", text="KIA 불펜은?", logos=["KIA"], logoSize=200, size=96)
SC['b6c'] = PLOG("양현종", "양현종", "KIA", "KIA 투수 · 5차전", [], stamp=dict(t="불펜 대기", at=1.0), chain="yhj")
SC['b6d'] = PLOG("양현종", "양현종", "KIA", "이번 플레이오프", [dict(type="zero", k="등판", stamp="아직 없음", at=1.0)], stamp=dict(t="불펜 대기", at=-1), chain="yhj")
SC['b11'] = PLOG("전상현", "전상현", "KIA", "KIA 불펜 · 플레이오프", [dict(type="line", items=[["플레이오프", "세 경기", False, 1.0]], at=1.0), dict(type="inn", ip=14 / 3, at=2.0), dict(type="zero", k="실점", stamp="무실점", at=3.0), dict(type="pitch", n=22, k="4차전 투구 수", at=4.0)])
SC['b12'] = PLOG("조상우", "조상우", "KIA", "KIA 불펜 · 플레이오프", [dict(type="line", items=[["플레이오프", "세 경기", False, 1.0]], at=1.0), dict(type="inn", ip=13 / 3, at=2.0), dict(type="line", items=[["3차전", "2실점 · 패전", True, 3.0]], at=3.0)])
SC['b8'] = PLOG("올러B", "올러", "KIA", "KIA 선발 · 5차전", [dict(type="line", items=[["올러가 일찍 내려가면", "불펜 부담 ↑", True, 1.0]], at=1.0)], stamp=dict(t="길어지는 불펜", at=2.0), imgAt=1.0)

# ── 키플레이어 ──
_lead = lambda e: S(0, "faceoff", title="1번 타자 · 플레이오프 네 경기", left=dict(img=P["김지찬"], name="김지찬", team="삼성", role="삼성 1번", at=2.0), right=dict(img=P["박재현"], name="박재현", team="KIA", role="KIA 1번", at=0), rows=[dict(k="타수", l="17", r="18", lv=17, rv=18, at=e.pop('a1', 1.0)), dict(k="안타", l="3", r="2", lv=3, rv=2, at=e.pop('a2', 2.0))], chain="lead", noCenter=True, **e)
SC['t2'] = _lead({})
SC['t3'] = _lead(dict(a1=-1, a2=-1, cont=True))
SC['k1'] = PLOG("한준수", "한준수", "KIA", "KIA 키플레이어", [], stamp=dict(t="KIA 키플레이어", at=0.5), chain="hjs")
SC['k2'] = PLOG("한준수", "한준수", "KIA", "플레이오프 네 경기", [dict(type="line", items=[["타수", "12", False, 2.0], ["안타", "5", True, 2.0]], at=2.0), dict(type="line", items=[["1차전", "홈런", False, 3.0], ["4차전", "동점타 · 결승타", True, 5.0]], at=3.0)], stamp=dict(t="KIA 키플레이어", at=-1), chain="hjs")
SC['k4'] = PLOG("김도영B", "김도영", "KIA", "플레이오프 네 경기", [dict(type="line", items=[["타수", "16", False, 1.0], ["안타", "7", True, 1.0]], at=1.0), dict(type="line", items=[["3차전", "홈런", False, 2.0]], at=2.0)])
SC['k5'] = PLOG("카스트로", "카스트로", "KIA", "플레이오프 네 경기", [dict(type="line", items=[["타수", "15", False, 1.0], ["안타", "5", False, 1.0], ["타점", "5", True, 2.0]], at=1.0)])
SC['k6'] = RL("4차전 4회처럼", [PL("김도영B", "김도영", "KIA", "출루", "on", 2.0), PL("한준수", "한준수", "KIA", "불러들이기", "run", 3.0), PL("후라도B", "후라도", "삼성", "삼성 선발", "def", 4.0)], [TA("KIA 득점", 1, 3.2, True)])
SC['k7'] = PLOG("최형우G", "최형우", "삼성", "삼성 키플레이어", [], stamp=dict(t="삼성 키플레이어", at=0.5), chain="chw2")
SC['k8'] = PLOG("최형우G", "최형우", "삼성", "플레이오프", [dict(type="line", items=[["2차전", "홈런", True, 1.0], ["4차전", "홈런", True, 1.0]], at=1.0)], stamp=dict(t="삼성 키플레이어", at=-1), chain="chw2")
SC['k8b'] = PLOG("디아즈", "디아즈", "삼성", "플레이오프 네 경기", [dict(type="line", items=[["타수", "14", False, 1.0], ["안타", "3", False, 1.0]], at=1.0), dict(type="line", items=[["홈런", "2", True, 2.0], ["타점", "4", True, 3.0]], at=2.0)])
SC['k10'] = PLOG("최형우G", "최형우", "삼성", "5차전", [dict(type="line", items=[["최형우 선제 타점", "→ 불펜 여유", True, 1.0]], at=1.0)], imgAt=1.0)

# ── 예상 ──
SC['z1b'] = S(0, "question", text="삼성 승", logos=["삼성"], logoSize=220, size=110)
SC['z1c'] = S(0, "question", text="이유 세 가지", logos=["삼성"], logoSize=220, size=110)
SC['z2'] = PLOG("올러B", "올러", "KIA", "이유 1 · 올러의 대구", [], stamp=dict(t="첫째", at=0.3), chain="z2o")
SC['z3'] = PLOG("올러B", "올러", "KIA", "이유 1 · 올러의 대구", [dict(type="line", items=[["대구 두 번", "모두 붕괴", True, 1.0]], at=1.0)], stamp=dict(t="첫째", at=-1), chain="z2o")
SC['z4'] = PLOG("후라도B", "후라도", "삼성", "이유 2 · 후라도", [], stamp=dict(t="둘째", at=0.3), chain="z4h")
SC['z5'] = PLOG("후라도B", "후라도", "삼성", "이유 2 · 후라도", [dict(type="line", items=[["정규시즌 막판", "흔들림", False, 1.0], ["이번 시리즈", "KIA 제압", True, 3.0]], at=1.0)], stamp=dict(t="둘째", at=-1), chain="z4h")
SC['z10'] = PLOG("올러B", "올러", "KIA", "뒤집힐 조건 1", [dict(type="inn", ip=5, at=2.0)], stamp=dict(t="5이닝 이상 버티면", at=2.0), imgAt=1.0)
SC['z11b'] = RL("뒤집힐 조건 2 · 삼성 실책", [PL("디아즈", "디아즈", "삼성", "4차전 실책", "out", 50), PL("류지혁", "류지혁", "삼성", "4차전 실책", "out", 50), PL("김영웅", "김영웅", "삼성", "4차전 실책", "out", 50)], [TA("또 실책이 나오면", 0, 50)], chain="z11")
SC['z11'] = SB("실책", [dict(k="정규시즌", l="85개 · 최소", r="98개", lv=85, rv=98, lAt=1.0, rAt=50), dict(k="플레이오프", l="7개", r="1개", lv=7, rv=1, lAt=3.0, rAt=4.0)])
SC['z11d'] = SB("병살타 · 플레이오프", [dict(k="병살타", l="4개", r="0개", lv=4, rv=0, lAt=2.0, rAt=3.0)])
SC['z12'] = PLOG("후라도B", "후라도", "삼성", "뒤집힐 조건 3", [], stamp=dict(t="크게 흔들리면", at=2.0), imgAt=1.0)
SC['x1'] = S(0, "question", text="한국시리즈 상대\n정규시즌 1위 KT", logos=["KT"], logoSize=220, size=96)
SC['x2'] = WDL("2026 정규시즌 · KT 상대전적", [dict(team="삼성", w=9, l=7, at=1.0, c="good", tag="삼성 우세", tagAt=1.3), dict(team="KIA", w=6, l=10, at=2.0, c="bad")])
SC['x3'] = WDL("2026 정규시즌 · KT 상대전적", [dict(team="삼성", w=9, l=7, at=-1, c="good", tag="삼성 우세", tagAt=-1), dict(team="KIA", w=6, l=10, at=-1, c="bad")], cont=True)
SC['x2'] = WDL("2026 정규시즌 · KT 상대전적", [dict(team="KT", w=7, l=9, at=1.0, c="bad", tag="vs 삼성", tagAt=1.0), dict(team="KT", w=10, l=6, at=2.0, c="good", tag="vs KIA", tagAt=2.0)], chain="kt")
SC['x3'] = WDL("2026 정규시즌 · KT 상대전적", [dict(team="KT", w=7, l=9, at=-1, c="bad", tag="vs 삼성", tagAt=-1), dict(team="KT", w=10, l=6, at=-1, c="good", tag="vs KIA", tagAt=-1)], chain="kt", cont=True)
SC['z11'] = SB("실책 · 정규시즌 최소였던 삼성", [dict(k="플레이오프\n네 경기", l="7개", r="1개", lv=7, rv=1, lAt=3.0, rAt=4.0)])
# precheck 반영: 사진은 이름 부르는 호흡에, 같은 사람 plog 는 이어받기(cont)
_FL0, _FR0 = dict(_FL, at=1.0), dict(_FR, at=2.0)
SC['s1b'] = dict(SC['s1b'], left=_FL0, right=_FR0)
for _k in ('s1c', 's1d', 's7', 's2', 's3'): SC[_k] = dict(SC[_k], left=dict(_FL, at=-1), right=dict(_FR, at=-1))
SC['s19'] = dict(SC['s19'], left=dict(_FL, at=3.0), right=dict(_FR, at=1.0))
SC['g13'] = _r7a(0.1, 1.0, 50, 50, {}, 50)
SC['z11b'] = RL("뒤집힐 조건 · 둘째", SC['z11b']['plays'], SC['z11b']['tally'], chain="z11")
for _k in ('s9', 's11', 's14', 's16', 's18', 'b6d', 'k2', 'k8', 'z3', 'z5'): SC[_k] = dict(SC[_k], cont=True)
SC['g7'] = box(hi=[6], upto=6, cont=False, marks=[dict(row=0, inn=6, label="홈런", at=2.0)], text="세 번째 승부처 · 6회", textAt=1.0)
SC['g8'] = S(0, "hrcam", launchAt=0.5, **_hr6)
SC['g9'] = S(0, "hrcam", launchAt=0.5, launchLine=KEYS.index('g8'), cont=True, **_hr6)
SC['s6'] = S(0, "tline", title="두 선발의 휴식", items=[dict(d="2차전", t="선발", at=0.1), dict(d="나흘", t="휴식", at=0.6), dict(d="5차전", t="다시 선발", c="good", at=1.0)])
SC['b7b'] = S(0, "tline", title="두 팀 불펜 일정", items=[dict(d="4차전", t="경기", at=0.6), dict(d="하루", t="휴식", c="good", at=1.4), dict(d="5차전", t="경기", at=1.0)])
# ── 미리보기 1차 반영: 빈 기록판 채우기, 이름 카드 → 뒤집히는 카드, 0 단위, 선발 비교 5줄로 크게 ──
_ROWS[:] = [dict(k="승패", l="9승 3패", r="11승 10패", lv=9, rv=11),
            dict(k="이닝", l="150", r="178", lv=150, rv=178),
            dict(k="퀄리티\n스타트", l="17경기", r="19경기", lv=17, rv=19),
            dict(k="평균자책점", l="3.54", r="3.13", lv=3.54, rv=3.13, low=True),
            dict(k="2차전", l="6⅔이닝\n2실점 · 승", r="4⅔이닝\n5실점 · 패", lv=2, rv=5, low=True)]
_FL['role'] = "정규시즌 24경기"; _FR['role'] = "정규시즌 30경기"
SC['s1b'] = dict(FO(0, {0: 1.0}, cont=False), left=dict(_FL, at=1.0), right=dict(_FR, at=2.0))
for _k, _sh, _na in (('s1c', 1, {1: 1.0}), ('s1d', 2, {2: 1.0}), ('s7', 3, {3: 1.0}), ('s2', 4, {}), ('s3', 4, {4: 1.0})):
    SC[_k] = dict(FO(_sh, _na), left=dict(_FL, at=-1), right=dict(_FR, at=-1))
SC['s19'] = dict(FO(5, {}, cont=False), left=dict(_FL, at=3.0), right=dict(_FR, at=1.0))
SC['g18'] = PLOG("사토시", "사토시", "삼성", "삼성 투수 · 7회", [dict(type="runs", n=3, at=2.2), dict(type="zero", k="자책점", u="점", stamp="비자책", at=3.0)], imgAt=2.0)
SC['b6d'] = PLOG("양현종", "양현종", "KIA", "이번 플레이오프", [dict(type="line", items=[["5차전", "불펜 대기", True]], at=-1), dict(type="zero", k="등판", u="번", stamp="아직 없음", at=1.0)], chain="yhj", cont=True)
SC['b6c'] = PLOG("양현종", "양현종", "KIA", "KIA 투수 · 5차전", [dict(type="line", items=[["5차전", "불펜 대기", True]], at=1.0)], chain="yhj")
SC['b11'] = PLOG("전상현", "전상현", "KIA", "KIA 불펜 · 플레이오프", [dict(type="line", items=[["플레이오프", "세 경기", False, 1.0]], at=1.0), dict(type="inn", ip=14 / 3, at=2.0), dict(type="zero", k="실점", u="점", stamp="무실점", at=3.0), dict(type="pitch", n=22, k="4차전 투구 수", at=4.0)])
SC['s8b'] = PLOG("올러B", "올러", "KIA", "KIA 선발 · 5차전", [dict(type="line", items=[["5차전 장소", "대구", True]], at=0.5)], stamp=dict(t="대구에서 약했다", at=1.0), chain="olr")
SC['s13'] = PLOG("후라도B", "후라도", "삼성", "삼성 선발 · 5차전", [dict(type="line", items=[["후라도의", "불안한 구석", True]], at=0.8)], chain="hrd")
SC['s16'] = PLOG("후라도B", "후라도", "삼성", "정규시즌 마지막 두 경기", [dict(type="line", items=[["10월 5일 두산전", "6실점", True, 2.0], ["10월 11일 KT전", "6실점", True, 3.0]], at=2.0), dict(type="runs", n=6, at=2.2), dict(type="runs", n=6, at=3.2)], chain="hrd", cont=True)
SC['k1'] = PLOG("한준수", "한준수", "KIA", "플레이오프 네 경기", [dict(type="line", items=[["KIA 키플레이어", "한준수", True]], at=0.3)], chain="hjs")
SC['k2'] = PLOG("한준수", "한준수", "KIA", "플레이오프 네 경기", [dict(type="line", items=[["KIA 키플레이어", "한준수", True]], at=-1), dict(type="line", items=[["타수", "12", False, 2.0], ["안타", "5", True, 2.0]], at=2.0), dict(type="line", items=[["1차전", "홈런", False, 3.0], ["4차전", "동점타 · 결승타", True, 5.0]], at=3.0)], chain="hjs", cont=True)
SC['k7'] = PLOG("최형우G", "최형우", "삼성", "플레이오프", [dict(type="line", items=[["삼성 키플레이어", "최형우", True]], at=0.3)], chain="chw2")
SC['k8'] = PLOG("최형우G", "최형우", "삼성", "플레이오프", [dict(type="line", items=[["삼성 키플레이어", "최형우", True]], at=-1), dict(type="line", items=[["2차전", "홈런", True, 1.0], ["4차전", "홈런", True, 1.0]], at=1.0)], chain="chw2", cont=True)
SC['z2'] = PLOG("올러B", "올러", "KIA", "삼성이 이길 이유", [dict(type="line", items=[["첫째", "올러의 대구 성적", True]], at=0.3)], chain="z2o")
SC['z3'] = PLOG("올러B", "올러", "KIA", "삼성이 이길 이유", [dict(type="line", items=[["첫째", "올러의 대구 성적", True]], at=-1), dict(type="line", items=[["대구 두 번", "모두 붕괴", True, 1.0]], at=1.0)], chain="z2o", cont=True)
SC['z4'] = PLOG("후라도B", "후라도", "삼성", "삼성이 이길 이유", [dict(type="line", items=[["둘째", "후라도", True]], at=0.3)], chain="z4h")
SC['z5'] = PLOG("후라도B", "후라도", "삼성", "삼성이 이길 이유", [dict(type="line", items=[["둘째", "후라도", True]], at=-1), dict(type="line", items=[["정규시즌 막판", "흔들림", False, 1.0], ["이번 시리즈", "KIA 제압", True, 3.0]], at=1.0)], chain="z4h", cont=True)
SC['z12'] = PLOG("후라도B", "후라도", "삼성", "뒤집힐 조건", [dict(type="line", items=[["셋째", "후라도가 크게 흔들리면", True]], at=1.0)], imgAt=1.0)
SC['z10'] = PLOG("올러B", "올러", "KIA", "뒤집힐 조건", [dict(type="line", items=[["첫째", "올러가 버티면", True]], at=1.0), dict(type="inn", ip=5, at=2.0)], stamp=dict(t="5이닝 이상", at=2.0), imgAt=1.0)
_z67 = lambda a, b, c, r, t, e: RL("셋째 · 삼성 중심 타선", [PL("디아즈", "디아즈", "삼성", r, "def", a), PL("최형우G", "최형우", "삼성", r, "def", b), PL("올러B", "올러", "KIA", "2차전 투런 허용", "out", c)], t, chain="z67", **e)
SC['z6'] = _z67(0.1, 0.1, 50, "삼성 타자", [TA("삼성 홈런", 5, 50), TA("두 선수", 4, 50, True)], {})
SC['z7'] = _z67(-1, -1, 4.0, "홈런 2개", [TA("삼성 홈런", 5, 1.0), TA("두 선수", 4, 2.0, True)], dict(cont=True))
SC['z11b'] = S(0, "question", text="또 실책이 나오면?", logos=["삼성"], logoSize=200, size=96)
SC['z12b'] = RL("넷째 조건", [PL("디아즈", "디아즈", "삼성", "막히면", "out", 1.0), PL("최형우G", "최형우", "삼성", "막히면", "out", 1.2)], [TA("넷째 조건", 4, 0.2, True)])
SC['h1'] = S(0, "statbars", title="2026 정규시즌", left="삼성", right="KIA", leftName="삼성 홈", rightName="KIA 원정", rows=[dict(k="승", l="43", r="37", lv=43, rv=37, lAt=1.0, rAt=50), dict(k="패", l="29", r="34", lv=29, rv=34, lAt=1.0, rAt=50)], chain="ha", noCenter=True)
SC['h2'] = S(0, "statbars", title="2026 정규시즌", left="삼성", right="KIA", leftName="삼성 홈", rightName="KIA 원정", rows=[dict(k="승", l="43", r="37", lv=43, rv=37, lAt=-1, rAt=1.0), dict(k="패", l="29", r="34", lv=29, rv=34, lAt=-1, rAt=1.0)], chain="ha", cont=True, noCenter=True)
SC['s19'] = dict(SC['s19'], left=dict(_FL, role="삼성 선발", at=3.0), right=dict(_FR, role="KIA 선발", at=1.0))
SC['b11'] = PLOG("전상현", "전상현", "KIA", "플레이오프 세 경기", [dict(type="inn", ip=14 / 3, at=2.0), dict(type="zero", k="실점", u="점", stamp="무실점", at=3.0), dict(type="pitch", n=22, k="4차전 투구 수", at=4.0)])
# 10/31 사용자 "텀 너무 길게 하지 마": 짧은 줄 장면도 최소 길이 때문에 뒤에 쉼이 붙지 않게(장면 최소 길이 0.8초 — 모션은 장면 길이에 맞춰 빨라짐)
for _k in list(SC): SC[_k] = dict(SC[_k], minDur=0.8)
