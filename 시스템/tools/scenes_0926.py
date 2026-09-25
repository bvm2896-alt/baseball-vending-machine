# -*- coding: utf-8 -*-
"""9/26 사용자 검수 반영 — 글자만 있는 장면을 전부 그림(표·점수판·눈금·갈림길·얼굴 격자·시상대·막대·픽토그램)으로.
gen_0926.py 가 편마다 SCENES[이름] 으로 장면 목록을 통째로 바꾸고, NARR[이름] 으로 바뀐 대사만 고친다(나머지 음성은 그대로 재사용)."""
def S(i, t, **k):
    d = {"type": t, "startLine": i}; d.update(k); return d

# ── 공통 그림 조각 ──
def standings(i, title, hi="한국", cut=2, cutLabel="지금 결승권", **k):
    rows = [{"team": "일본", "rec": "2승 0패", "sub": "한국 5-0 · 중국 11-3"},
            {"team": "한국", "rec": "1승 1패", "sub": "대만 5-0 · 일본 0-5"},
            {"team": "대만", "rec": "1승 1패", "sub": "한국 0-5 · 중국 9-1"},
            {"team": "중국", "rec": "0승 2패", "sub": "일본 3-11 · 대만 1-9", "out": hi != "중국"}]
    for r in rows:
        if r["team"] == hi: r["hi"] = True; r.pop("out", None)
    return S(i, "league", title=title, cut=cut, cutLabel=cutLabel, rows=rows, **k)
def if_korea_wins(i, text=None, **k):
    return S(i, "league", title="한국이 중국을 이기면", rows=[
        {"team": "한국", "rec": "2승 1패", "tag": "+1승", "hi": True},
        {"team": "일본", "rec": "2승 0패", "sub": "대만전 남음"},
        {"team": "대만", "rec": "1승 1패", "sub": "일본전 남음"},
        {"team": "중국", "rec": "0승 3패", "out": True}], **({"text": text, "size": 60} if text else {}), **k)
def branch3(i, text=None):
    return S(i, "branch", root={"left": "일본", "right": "대만", "label": "26일 18:30 오카자키"}, items=[
        {"cond": "일본 승", "final": ["한국", "일본"], "hi": True},
        {"cond": "대만 1~4점 차 승", "final": ["한국", "일본"]},
        {"cond": "대만 6점 차 이상 승", "final": ["한국", "대만"]}], **({"text": text, "size": 64} if text else {}))
ZONES = [{"a": 1, "b": 4, "label": "결승\n한국 vs 일본", "team": ["한국", "일본"]},
         {"a": 5, "b": 5, "label": "다음\n기준", "color": "#8A93A3"},
         {"a": 6, "b": 9, "label": "결승\n한국 vs 대만", "team": ["한국", "대만"], "color": "#E5484D"}]
def ruler(i, focus): return S(i, "ruler", title="대만이 일본을 몇 점 차로 이기면?", **{"from": 1}, to=9, focus=focus, zones=ZONES)
KJ = [{"team": "한국", "runs": [0, 0, 0, 0, 0, 0, 0, 0, 0], "r": 0}, {"team": "일본", "runs": [0, 0, 3, 0, 0, 2, 0, 0, "X"], "r": 5}]   # 스포츠나비 박스스코어(한국 선공)
def kj(i, title, hi=(), marks=(), text=None, **k):
    return S(i, "scoreboard", title=title, rows=KJ, hi=list(hi), marks=list(marks), **({"text": text} if text else {}), **k)
MIPIL = [("성영탁", "KIA"), ("김도영", "KIA"), ("박재현", "KIA"), ("조형우", "SSG"), ("정준재", "SSG"), ("배찬승", "삼성"), ("이재현", "삼성"), ("소형준", "KT"),
         ("오원석", "KT"), ("최준용", "롯데"), ("김진욱", "롯데"), ("최민석", "두산"), ("박준순", "두산"), ("김영우", "LG"), ("문현빈", "한화"), ("김건희", "키움")]
PIC = {"김도영": "국가대표프로필/김도영", "박재현": "국가대표프로필/박재현"}
def face(n, t, **k): d = {"img": PIC.get(n, "KBO프로필/" + n), "name": n, "team": t}; d.update(k); return d

NARR = {
  "2026-09-26_이슈3": {3: "월드베이스볼클래식 대표가 즐비한데 / 사회인에게 / 사 안타 영봉패를 당했다고요"},
  "2026-09-26_이슈4": {10: "대학을 나온 사회인 선수는 / 입사 이 년 차부터 / 프로 지명을 받을 수 있어요",
                     11: "히구치는 올해가 딱 이 년 차예요 / 제 예상은 시월 드래프트 지명이에요 / 한국전이 최고의 무대였어요"},
}

SCENES = {
 "2026-09-26_이슈": [
  S(0, "matchup", left="한국", right="일본", text="사회인에 완패", size=84, score="0-5", tag="9월 25일 슈퍼라운드"),
  S(1, "photo", img="상황별/일본_투수_22번", text="프로 0명\n전원 회사팀 선수", size=96, tag="일본 대표팀"),
  S(2, "compare", title="프로 선수 수", left={"team": "한국", "label": "24명 전원 프로", "n": 24, "of": 24}, right={"team": "일본", "label": "프로 0명", "n": 0, "of": 24}, text="20년 만의 사회인 패배", size=64),
  S(3, "people", title="병살타 3개", items=[{"img": "KBO프로필/노시환", "name": "노시환", "team": "한화", "note": "병살 2개"}, {"img": "KBO프로필/윤동희", "name": "윤동희", "team": "롯데", "note": "병살 1개"}], text="", size=80),
  kj(4, "주자가 나가면 병살", hi=[1, 4, 5], marks=[{"row": 0, "inn": 1, "label": "병살"}, {"row": 0, "inn": 4, "label": "병살"}, {"row": 0, "inn": 5, "label": "병살"}]),
  S(5, "photo", img="상황별/히구치", text="7이닝 4안타\n무실점", size=96, tag="일본 선발 히구치 신"),
  S(6, "photo", img="국가대표프로필/김도영", text="4타수 무안타\n삼진 2개", size=96, tag="1번 타자 김도영"),
  S(7, "photo", img="KBO프로필/소형준", text="3회 3실점\n3이닝 강판", size=96, team="KT", tag="선발 소형준"),
  kj(8, "6회 2점 더 · 8·9회 삼자범퇴", hi=[6, 8, 9], marks=[{"row": 1, "inn": 6, "label": "2실점"}, {"row": 0, "inn": 8, "label": "삼자범퇴", "color": "#6A7382"}, {"row": 0, "inn": 9, "label": "삼자범퇴", "color": "#6A7382"}]),
  S(9, "photo", img="국가대표프로필/류지현", text="경우의 수는\n생각도 안 했다", size=88, tag="류지현 감독 · 25일"),
  standings(10, "지금 슈퍼라운드 순위"),
  if_korea_wins(11, "계산상 결승 유력"),
  S(12, "question", text="결승에서 일본에", choices=[{"team": "한국", "label": "되갚는다"}, {"team": "일본", "label": "또 진다"}]),
 ],
 "2026-09-26_이슈2": None,   # gen_0926.py 의 2편 장면(9/26 1차 그림화)을 그대로 쓰고 아래 몇 개만 바꾼다
 "2026-09-26_이슈3": [
  S(0, "matchup", left="한국", right="일본", text="일본 언론 반응", size=84, score="0-5", tag="9월 25일 슈퍼라운드"),
  S(1, "upset", title="金星 금성", sub="스모에서 온 말", small={"team": "일본", "label": "약한 쪽", "sub": "사회인"}, big={"team": "한국", "label": "강한 쪽", "sub": "프로"}, text="약자가 강자를 잡았다"),
  S(2, "photo", img="상황별/데일리_한국전_보도", text="", size=96, fit="contain", h=880, tag="데일리스포츠 9월 25일"),
  S(3, "bars", title="WBC 대표가 즐비한데", items=[{"label": "한국 안타", "team": "한국", "value": 4, "unit": "개", "hi": True}, {"label": "일본 안타", "team": "일본", "value": 9, "unit": "개"}], text="4안타 영봉패", size=72),
  S(4, "photo", img="상황별/스포니치_한국전_보도", text="", size=96, fit="contain", h=880, tag="스포츠닛폰 9월 25일"),
  S(5, "people", title="일본이 콕 집은 선수", items=[{"img": "국가대표프로필/김도영", "name": "김도영", "team": "KIA", "note": "WBC 대표"}, {"img": "KBO프로필/문보경", "name": "문보경", "team": "LG", "note": "WBC 대표"}], text="", size=80),
  S(6, "photo", img="상황별/히구치", text="올가을 드래프트\n후보 좌완", size=96, tag="일본 선발 히구치 신"),
  S(7, "icons", title="한국 더그아웃", n=12, cols=6, label="경기 중반부터\n전원 기립", icon="person"),
  S(8, "steps", title="일본 4전 4승", items=[{"date": "11-3", "text": "중국"}, {"date": "15-0", "text": "팔레스타인"}, {"date": "7-0", "text": "필리핀"}, {"date": "5-0", "text": "한국", "hi": True}]),
  S(9, "steps", title="또 사회인에게 진 참사", items=[{"date": "2006", "text": "도하 참사", "sub": "일본에 7-10"}, {"date": "2026", "text": "도요하시 참사", "sub": "일본에 0-5", "hi": True}]),
  standings(10, "일본은 대만만 이기면 결승", hi="일본"),
  S(11, "steps", title="제 예상", items=[{"date": "26일", "text": "한국 vs 중국", "sub": "한국 승"}, {"date": "26일", "text": "일본 vs 대만", "sub": "일본 승"}, {"date": "27일", "text": "결승\n한국 vs 일본", "hi": True}]),
  S(12, "question", text="결승에서", choices=[{"team": "한국", "label": "한국이 되갚는다"}, {"team": "일본", "label": "일본이 또 웃는다"}]),
 ],
 "2026-09-26_이슈4": [
  S(0, "photo", img="상황별/히구치", text="한국 타선 7이닝 무실점\n회사팀 투수", size=88, tag="일본 선발 히구치 신"),
  S(1, "photo", img="상황별/히구치", text="24살 좌완\n제지회사 오지 소속", size=92, tag="히구치 신"),
  S(2, "steps", title="히구치 신의 길", items=[{"date": "대학", "text": "아이치공대"}, {"date": "2025", "text": "오지 입사", "sub": "평균자책점 1위 2.05"}, {"date": "2026", "text": "2년 차\n드래프트 후보", "hi": True}]),
  S(3, "matchup", left="일본", right="중국", text="히구치 6이닝 10K · 86구", size=84, score="11-3", tag="21일 조별리그"),
  S(4, "steps", title="86구 던지고 나흘 뒤", items=[{"date": "21", "text": "중국전", "sub": "86구"}, {"date": "22", "text": "휴식"}, {"date": "23", "text": "휴식"}, {"date": "24", "text": "휴식"}, {"date": "25", "text": "한국전\n?", "hi": True}], text="못 나온다고 봤는데", size=64),
  S(5, "steps", title="사흘 쉬고 선발", items=[{"date": "21", "text": "중국전", "sub": "86구"}, {"date": "22", "text": "휴식"}, {"date": "23", "text": "휴식"}, {"date": "24", "text": "휴식"}, {"date": "25", "text": "한국전\n선발", "hi": True}]),
  S(6, "scoreboard", title="히구치가 막은 7이닝", rows=[{"team": "한국", "runs": [0, 0, 0, 0, 0, 0, 0, None, None], "r": 0, "hi": True}], hi=[1, 2, 3, 4, 5, 6, 7], text="4안타 · 4K · 볼넷 0", size=64),
  S(7, "bars", title="투구 수", items=[{"label": "21일 중국전", "value": 86, "unit": "구"}, {"label": "25일 한국전", "sub": "사흘 쉬고", "value": 92, "unit": "구", "hi": True}], max=100, text="8·9회는 불펜 삼자범퇴", size=60),
  S(8, "people", title="병살타 3개", items=[{"img": "KBO프로필/노시환", "name": "노시환", "team": "한화", "note": "병살 2개"}, {"img": "KBO프로필/윤동희", "name": "윤동희", "team": "롯데", "note": "병살 1개"}], text="", size=80),
  S(9, "photo", img="상황별/스포니치_한국전_보도", text="", size=96, fit="contain", h=880, tag="스포츠닛폰 · 드래프트 후보 좌완의 압권 투구"),
  S(10, "steps", title="일본 사회인 선수 규정", items=[{"date": "입사", "text": "대학 졸업 뒤\n회사팀"}, {"date": "1년 차", "text": "지명 불가"}, {"date": "2년 차", "text": "프로 지명\n가능", "hi": True}]),
  S(11, "steps", title="제 예상: 프로 지명", items=[{"date": "9/25", "text": "한국전\n7이닝 무실점"}, {"date": "10/22", "text": "NPB\n드래프트", "sub": "사회인 No.1 좌완 평가", "hi": True}]),
  S(12, "question", text="결승에서 또 만나면", choices=[{"team": "한국", "label": "이번엔 친다"}, {"img": "상황별/히구치", "label": "또 막힌다"}]),
 ],
 "2026-09-26_이슈5": [
  S(0, "photo", img="상황별/린위민", text="린위민도\n믿기 어렵다", size=96, tag="대만 린위민 · 애리조나 산하"),
  S(1, "matchup", left="한국", right="대만", text="9회에야 첫 안타", size=84, score="5-0", tag="21일 조별리그"),
  S(2, "cards", title="린위민의 한일전 예상", items=[{"badge": "예상", "name": "2-1"}, {"badge": "예상", "name": "3-2"}, {"badge": "실제", "name": "0-5", "hi": True}], text="", size=76),
  S(3, "photo", img="상황별/ETtoday_린위민_보도", text="", size=96, fit="contain", h=880, tag="대만 이티투데이 9월 25일"),
  S(4, "matchup", left="대만", right="중국", text="선발 한화 왕옌청", size=84, score="9-1", tag="25일 슈퍼라운드"),
  S(5, "photo", img="KBO프로필/왕옌청", text="1회 무사 만루 탈출\n7이닝 1실점", size=88, team="한화", tag="대만 왕옌청 · 한화"),
  standings(6, "대만은 1승 1패", hi="대만"),
  ruler(7, 2),
  S(8, "steps", title="대만의 일본전 선발", items=[{"date": "원래", "text": "린위민"}, {"date": "지금", "text": "다시 고민", "hi": True}]),
  S(9, "photo", img="상황별/ETtoday_린위민_보도", text="", size=96, fit="contain", h=880, tag="린위민 · 대만 이티투데이 25일"),
  S(10, "photo", img="상황별/린위민", text="언제든\n준비는 됐다", size=100, tag="린위민 · 대만 이티투데이"),
  S(11, "matchup", left="대만", right="일본", text="린위민 선발", size=84, vsText="제 예상"),
  S(12, "question", text="26일 대만 vs 일본", choices=[{"team": "대만", "label": "대만이 대파"}, {"team": "일본", "label": "일본이 막는다"}]),
 ],
 "2026-09-26_이슈6": [
  S(0, "matchup", left="한국", right="중국", text="반드시 이겨야 한다", size=84, vsText="26일 18:30"),
  S(1, "league", title="한국이 중국에 지면", cut=2, cutLabel="결승권", rows=[
      {"team": "일본", "rec": "2승 0패", "sub": "대만전 남음"}, {"team": "대만", "rec": "1승 1패", "sub": "일본전 남음"},
      {"team": "한국", "rec": "1승 2패", "hi": True, "tag": "탈락 위기"}, {"team": "중국", "rec": "1승 2패", "out": True}]),
  S(2, "photo", img="KBO프로필/최민석", text="선발 최민석\n다승 1위 14승", size=96, team="두산", tag="두산 최민석"),
  S(3, "bars", title="스무 살 최민석", items=[{"label": "다승", "sub": "리그 1위", "value": 14, "unit": "승", "max": 16, "hi": True}, {"label": "평균자책점", "sub": "14승 4패", "value": 2.73, "dec": 2, "max": 5}]),
  S(4, "photo", img="KBO프로필/최민석", text="22일 홍콩전\n2이닝 무실점", size=96, team="두산", tag="대표팀 데뷔전"),
  S(5, "icons", title="홍콩 타자 21명", n=21, cols=7, mark="x", label="전부 아웃 · 13-0 7회 콜드"),
  S(6, "steps", title="같은 도요하시 구장", items=[{"date": "22일", "text": "홍콩전", "sub": "13-0 콜드"}, {"date": "26일", "text": "중국전", "hi": True}]),
  standings(7, "중국은 2패", hi="중국", cut=0),
  S(8, "cards", title="26일 선발 맞대결", items=[{"badge": "한국", "name": "최민석", "sub": "14승 · 2.73", "hi": True}, {"badge": "중국", "name": "우안쥔", "sub": "26일 예고"}], text="", size=76),
  kj(9, "25일 일본전", text="4안타 무득점", size=64),
  S(10, "people", title="살아나야 할 타자", items=[{"img": "국가대표프로필/김도영", "name": "김도영", "team": "KIA", "note": "4타수 무안타"}, {"img": "KBO프로필/노시환", "name": "노시환", "team": "한화", "note": "병살 2개"}], text="", size=80),
  S(11, "matchup", left="한국", right="중국", text="한국 대승", size=84, vsText="제 예상"),
  S(12, "question", text="중국전 한국 타선", choices=[{"img": "국가대표프로필/김도영", "label": "다시 깨어난다"}, {"img": "KBO프로필/노시환", "label": "또 막힌다"}]),
 ],
 "2026-09-26_이슈7": [
  S(0, "photo", img="국가대표프로필/김도영", text="흔들리는\n병역 혜택", size=100, tag="아시안게임 야구 대표팀"),
  S(1, "facegrid", title="대표팀 24명 중 미필 16명", items=[face(n, t) for n, t in MIPIL], cols=4),
  S(2, "steps", title="병역 혜택은 금메달만", items=[{"date": "금", "text": "병역 혜택", "hi": True}, {"date": "은", "text": "없음"}, {"date": "동", "text": "없음"}]),
  S(3, "steps", title="금메달을 따면", items=[{"date": "편입", "text": "예술체육요원"}, {"date": "훈련", "text": "기초군사훈련"}, {"date": "544시간", "text": "봉사활동", "sub": "2년 10개월 동안", "hi": True}]),
  S(4, "facegrid", title="금메달이 필요한 선수들", items=[face("김도영", "KIA", hi=True), face("소형준", "KT", hi=True), face("문현빈", "한화", hi=True), face("김영우", "LG", hi=True), face("조형우", "SSG", hi=True)], cols=3),
  S(5, "photo", img="KBO프로필/최민석", text="중국전 선발\n최민석도 미필", size=96, team="두산", tag="두산 최민석"),
  S(6, "photo", img="KBO프로필/김진욱", text="한일전 2이닝\n4K 무실점", size=96, team="롯데", tag="롯데 김진욱 · 미필"),
  if_korea_wins(7, "계산상 결승 유력"),
  branch3(8),
  S(9, "matchup", left="한국", right="대만", text="항저우 결승 금메달", size=84, score="2-0", tag="2023 항저우"),
  S(10, "photo", img="국가대표프로필/류지현", text="지금은\n중국전부터", size=100, tag="류지현 감독 · 25일"),
  S(11, "steps", title="제 예상은 금메달", items=[{"date": "25일", "text": "일본에 0-5"}, {"date": "26일", "text": "중국전"}, {"date": "27일", "text": "결승\n금메달", "hi": True}]),
  S(12, "question", text="미필 16명", choices=[{"team": "한국", "label": "금메달로 웃는다"}, {"img": "국가대표프로필/류지현", "label": "눈물을 흘린다"}]),
 ],
 "2026-09-26_이슈8": [
  S(0, "matchup", left="한국", right="일본", text="20년 전에도 졌다", size=84, score="7-10", tag="2006 도하 아시안게임"),
  S(1, "steps", title="2006년의 한국 야구", items=[{"date": "3월", "text": "WBC 4강", "hi": True}, {"date": "겨울", "text": "도하\n아시안게임"}]),
  S(2, "steps", title="2006년의 한국 야구", items=[{"date": "3월", "text": "WBC 4강"}, {"date": "겨울", "text": "도하\n대만·일본에 연패", "hi": True}]),
  S(3, "matchup", left="한국", right="대만", text="병살타에 발목", size=84, score="2-4", tag="2006 도하 첫 경기"),
  S(4, "cards", title="2006 도하 대진", items=[{"badge": "한국", "name": "프로 선수"}, {"badge": "일본", "name": "사회인\n+ 대학생", "hi": True}], text="", size=76),
  S(5, "matchup", left="한국", right="일본", text="9회말 끝내기 3점 홈런", size=84, score="7-10", tag="2006 도하"),
  S(6, "photo", img="오승환", text="9회말 7-7\n이미 55구", size=96, team="삼성", tag="오승환 · 2006 도하"),
  S(7, "facegrid", title="2006 도하 대표팀", items=[{"img": "KBO프로필/류현진", "name": "류현진", "team": "한화"}, {"img": "이대호", "name": "이대호", "team": "롯데"}, {"img": "손민한", "name": "손민한", "team": "롯데"}, {"img": "이병규", "name": "이병규", "team": "LG"}], cols=2),
  S(8, "podium", title="2006 도하 아시안게임 야구", items=[{"team": "대만", "medal": "금", "sub": "5전 전승"}, {"team": "일본", "medal": "은"}, {"team": "한국", "medal": "동", "hi": True, "sub": "도하 참사"}]),
  S(9, "matchup", left="한국", right="일본", text="이번엔 무득점", size=84, score="0-5", tag="2026 도요하시"),
  S(10, "steps", title="20년 전과 똑같은 병살", items=[{"date": "2006", "text": "대만전 병살", "sub": "2-4 패"}, {"date": "2026", "text": "일본전 병살 3개", "sub": "0-5 패", "hi": True}]),
  S(11, "steps", title="그때와 다른 점", items=[{"date": "2006", "text": "동메달", "sub": "결승 못 감"}, {"date": "2026", "text": "결승 길\n열려 있음", "sub": "중국만 잡으면", "hi": True}]),
  S(12, "question", text="도요하시의 끝은", choices=[{"team": "한국", "label": "금메달로 뒤집는다"}, {"team": "일본", "label": "참사로 끝난다"}]),
 ],
}
# 2편: 1차 그림화 장면에서 훅·질문만 그림으로
PATCH = {"2026-09-26_이슈2": {
  0: S(0, "matchup", left="일본", right="대만", text="이 경기가 한국 결승을 정한다?", size=72, vsText="26일"),
  12: S(12, "question", text="결승 상대는", choices=[{"team": "일본", "label": "일본"}, {"team": "대만", "label": "대만"}]),
}}

# 썸네일: 선수 사진만 쓰지 않고 편마다 다른 그림(점수판·얼굴 모음·맞대결·시상대·갈림길·보도 지면) — 9/26 사용자 "지루하고 뻔하다"
THUMB = {
 "2026-09-26_이슈": {"graphic": "score", "left": "한국", "right": "일본", "score": "0-5", "line": [0, 0, 3, 0, 0, 2, 0, 0, "X"], "lineHi": [3, 6], "gh": 760,
                    "top": "한일전 0-5", "big": "KBO 24명\n회사원에 참패", "teams": ["KT"], "color": "#E5484D"},
 "2026-09-26_이슈2": {"graphic": "branch", "root": ["일본", "대만"], "results": [{"cond": "일본 승", "final": ["한국", "일본"]}, {"cond": "대만 1~4점 차", "final": ["한국", "일본"]}, {"cond": "대만 6점 차 이상", "final": ["한국", "대만"]}], "gh": 860,
                    "top": "중국만 이기면", "big": "한국 결승\n경우의 수", "teams": ["KT"], "color": "#1E5EFF"},
 "2026-09-26_이슈3": {"img": "상황별/데일리_한국전_보도", "fit": "contain", "top": "일본 언론 반응", "big": "프로가\n회사원에 졌다", "teams": ["KT"], "logos": False, "color": "#E5484D"},
 "2026-09-26_이슈4": {"graphic": "versus", "left": {"img": "상황별/히구치", "label": "히구치"}, "right": {"img": "국가대표프로필/김도영", "label": "김도영"}, "gh": 700,
                    "top": "한국 타선 7이닝 무실점", "big": "히구치\n정체는 회사원", "teams": ["KT"], "color": "#E5484D"},
 "2026-09-26_이슈5": {"graphic": "versus", "left": {"img": "상황별/린위민", "label": "린위민"}, "right": {"team": "일본", "label": "26일 일본"}, "gh": 700,
                    "top": "대만 반응", "big": "린위민\n0-5 믿기 어렵다", "teams": ["HH"], "color": "#1E5EFF"},
 "2026-09-26_이슈6": {"graphic": "versus", "left": {"img": "KBO프로필/최민석", "label": "최민석"}, "right": {"team": "중국", "label": "중국"}, "gh": 700,
                    "top": "지면 끝 중국전", "big": "최민석\n다승 1위 출격", "teams": ["OB"], "color": "#1E5EFF"},
 "2026-09-26_이슈7": {"graphic": "faces", "faces": [{"img": PIC.get(n, "KBO프로필/" + n)} for n, _ in MIPIL], "cols": 4, "gh": 900,
                    "top": "한일전 패배 여파", "big": "병역 16명\n금메달 흔들", "teams": ["HT"], "color": "#E5484D"},
 "2026-09-26_이슈8": {"graphic": "podium", "items": [{"team": "대만", "medal": "금"}, {"team": "일본", "medal": "은"}, {"team": "한국", "medal": "동", "hi": True}], "gh": 760,
                    "top": "20년 전 도하 참사", "big": "또 사회인에\n졌다", "teams": ["KT"], "color": "#E5484D"},
}

# 사진 출처 표기가 필요한 것(자유 이용 사진은 저작자 표시 조건)
CREDIT = {"2026-09-26_이슈8": "사진: 이병규 — Cake6, CC BY-SA 3.0 (Wikimedia Commons) / 오승환·이대호 — MLB 공식 프로필"}
REV = {"2026-09-26_이슈8": "api-line-normal-1.2x+손민한사진+이대호축소"}   # 사진만 바뀌면 콘티 지문이 안 바뀌어 다시 안 만들어진다 → rev 로 다시
