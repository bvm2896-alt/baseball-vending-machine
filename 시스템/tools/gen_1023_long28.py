# -*- coding: utf-8 -*-
"""10/23 롱폼㉘ 「기아 방출 | 15억 포기하고 돌아온 홍건희, 1년 만에 방출」 (방출 시리즈 7편).
대사 = tools/text_1023_long28.py. 근거 = 프로젝트 claude/1023-롱폼28-기아방출-근거모음.md + KBO 기록실(10/23 조회).
사진: 인물 카드 = 카드/P28_* (0.774) · 경기/ (SPOTV·엑스포츠뉴스) · 얼굴판·프로필 = KBO프로필/<이름>_KIA (다음스포츠 2026 구단 프로필, 나무위키 인포박스).
넥센·SK·롯데·KT·LG 시절 이야기 장면은 그 시절 사진을 못 구해 KIA 사진·프로필로 둔다(사용자에게 알림)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_rank_0923 import S, END, OUT
_src = open(os.path.join(os.path.dirname(__file__), 'gen_1015_long15.py'), encoding='utf-8').read()
_src = _src[:_src.index('def sub_of')].replace("'text_1015_long15.py'", "'text_1023_long28.py'")
_g = {'__file__': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_1015_long15.py')}
exec(_src, _g)
L, narr_of15, LINES = _g['L'], _g['narr_of'], _g['_t'].LINES
TEXT = [x[0] for x in LINES]
import narr_1020
def narr_of(t):
    t = re.sub(r'(\d),(\d{3})', r'\1\2', t)
    n = narr_1020.post(narr_of15(narr_1020.pre(t)))
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) 월', r'\1월', n)
    n = re.sub(r'(?<![가-힣])(일|이|삼|사|오|육|칠|팔|구|십) (회|실점|승|패|할|푼|리|이닝|타수|안타)(?![가-힣]*차전)', r'\1\2', n)
    n = n.replace('KT', '케이티').replace('KIA', '기아').replace('LG', '엘지').replace('SSG', '에스에스지').replace('SK', '에스케이').replace('NC', '엔씨').replace('FA', '에프에이')
    n = n.replace('십일 월', '십일월').replace('십이 월', '십이월')
    n = re.sub(r'(일|이|삼|사|오|육|칠|팔|구|십) 연패', r'\1연패', n)
    return n
def sub_of(t): return re.sub(r'\.(?= / )', '', t.replace(' / +', ' / '))

def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def bb(date, text, at=0, **x): return dict({"date": date, "text": text, "at": at}, **x)
def vsteps(items, **k): return dict(type="steps", items=items, **k)
def stp(d, t, at=0, c=None, **k): return dict(d=d, t=t, at=at, **({"c": c} if c else {}), **k)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
C, K = '카드/P28_', 'KBO프로필/'
IMG = {None: None, "H": C + "홍건희_KIA", "HP": C + "홍건희_KIA투구", "HD": C + "홍건희_두산", "G": C + "고종욱_KIA", "LC": C + "이창진_KIA", "LK": C + "이창진_KS4"}
def pv(img, name, sub, viz=(), stats=(), **k): return S(0, "pstat", img=IMG.get(img, img), team=k.pop("team", "KIA"), name=name, sub=sub, viz=list(viz), stats=list(stats), noCenter=True, **k)
def sp(img, name, sub, bubbles, **k): return S(0, "speech", img=IMG.get(img, img), team=k.pop("team", "KIA"), name=name, sub=sub, bubbles=bubbles, **k)
def prof(n): return K + n + "_KIA"
def pp(n, sub, viz=(), stats=(), **k): return pv(prof(n), n, sub, viz, stats, profile=True, **k)
POS = [("고종욱", "외야수"), ("이창진", "외야수"), ("홍건희", "투수"), ("김사윤", "투수"), ("김대유", "투수"), ("윤중현", "투수")]
def F6(text=None, textAt=0.3, hi=(), **k):
    return S(0, "facegrid", title="KIA · 재계약 불가 6명", cols=6, card=True, chain="f6", profile=True,
             items=[dict(name=n, img=prof(n), team="KIA", pos=p, **({"hi": True} if n in hi else {}), **({"dim": True} if hi and n not in hi else {}),
                         **({"at": 0.2 + i * 0.06} if not k.get("cont") else {})) for i, (n, p) in enumerate(POS)],
             **({"text": text, "textAt": textAt, "size": 56} if text else {}), **k)

SC = []
# ── 오프닝 ──
SC.append(F6(text="플레이오프 1차전 이틀 전", textAt=2.4))                                                                     # 0
SC.append(pv(None, "KIA 타이거즈", "10월 23일 발표", [], [st("재계약 불가", "6명", 0.1), st("육성선수 말소 요청", "10명", 0.1), st("합계", "16명", 1.0, hi=True)]))   # 1
SC.append(pv("H", "홍건희", "KIA 투수", [], [st("2026년 1월", "6년 만에 친정 복귀", 1.6, hi=True)], chain="o2"))                      # 2
SC.append(pv("H", "홍건희", "KIA 투수", [], [st("2026년 1월", "6년 만에 친정 복귀", 0), st("지난겨울 포기", "2년 15억 원", 2.0, hi=True)], chain="o2", cont=True))   # 3
SC.append(pv("H", "홍건희", "KIA 투수", [], [st("2026년 1월", "6년 만에 친정 복귀", 0), st("지난겨울 포기", "2년 15억 원", 0), st("KIA 계약", "1년", 0.4),
                                           st("10월 23일", "재계약 불가", 1.4, hi=True)], chain="o2", cont=True))           # 4
SC.append(S(0, "toc", on=-1, itemFrom=99))                                                                                   # 5
# ── 1막 · 기아의 10월 ──
R24 = dict(k="2024년", v="통합우승", rank=1, at=0.6)
R25 = dict(k="2025년", v="가을야구 탈락", rank=8)
R26 = dict(k="2026년", v="정규시즌 3위", rank=3)
SC.append(S(0, "rankstrip", team="KIA", title="KIA 타이거즈", rows=[R24, dict(R25, at=50), dict(R26, at=50)], chain="r6"))                                          # 6
SC.append(S(0, "rankstrip", team="KIA", title="KIA 타이거즈", rows=[dict(R24, at=-1), dict(R25, at=0.5), dict(R26, at=50)], chain="r6", cont=True))   # 7
SC.append(S(0, "rankstrip", team="KIA", title="KIA 타이거즈", rows=[dict(R24, at=-1), dict(R25, at=-1), dict(R26, at=1.0)], chain="r6", cont=True))   # 8
SC.append(pv(None, "준플레이오프", "KIA vs LG", [vsteps([stp("1차전 · 광주", "5대 1 승", 0.6, c="good"), stp("2차전 · 광주", "6대 3 승", 1.3, c="good"), stp("3차전 · 잠실", "13대 1 승", 2.1, c="good")])]))   # 9
SC.append(pv(None, "플레이오프", "5전 3선승제", [], [st("1차전", "10월 25일 · 대구", 0.3), st("상대", "정규시즌 2위 삼성", 2.0, hi=True)]))   # 10
SC.append(pv(None, "한국시리즈", "7전 4선승제", [], [st("기다리는 팀", "정규시즌 1위 KT", 0.6, hi=True), st("KT 1위 확정", "10월 5일 · 5년 만", 50)], chain="ks11"))                              # 11
SC.append(F6(text="10월 23일 오후 발표", textAt=1.0, cont=True))                                                                # 12
SC.append(F6(text="외야수 2명 · 투수 4명", textAt=0.3, cont=True))                                                              # 13
SC.append(pv(None, "육성선수 10명", "KBO에 말소 요청", [], [st("투수", "3명", 0.1), st("포수", "2명", 0.4), st("내야수", "2명", 0.7), st("외야수", "3명", 0.9)]))   # 14
# ── 2막 · 홍건희 ──
SC.append(S(0, "photo", img="경기/홍건희_KIA투구_SPOTV", fit="cover", text="", h=760))                                           # 15
SC.append(pp("홍건희", "KIA 투수", [vsteps([stp("고교", "화순고", 0.3), stp("2011년", "KIA 2라운드 · 전체 9순위", 1.2, c="good")])], [st("첫 번째 KIA 시절", "166경기", 50), st("평균자책점", "6.30", 50, hi=True)], chain="h16"))   # 16
SC.append(pp("홍건희", "KIA 투수", [vsteps([stp("고교", "화순고", -1), stp("2011년", "KIA 2라운드 · 전체 9순위", -1, c="good")])],
             [st("첫 번째 KIA 시절", "166경기", 2.0), st("평균자책점", "6.30", 3.0, hi=True)], chain="h16", cont=True))          # 17
SC.append(pv("HD", "홍건희", "2020년 6월 7일 트레이드", [], [st("KIA → 두산", "홍건희", 1.0), st("두산 → KIA", "내야수 류지혁", 1.0, hi=True)], chain="d18"))   # 18
SC.append(pv("HD", "홍건희", "2020년 6월 7일 트레이드", [vstamp("두산에서 달라졌다", 0.3, "good", size=52)],
             [st("KIA → 두산", "홍건희", 0), st("두산 → KIA", "내야수 류지혁", 0, hi=True)], chain="d18", cont=True))         # 19
SC.append(pv("HD", "홍건희", "두산 시절", [], [st("2021년", "65경기 · 17홀드", 0.3), st("평균자책점", "2.78 · 커리어 하이", 1.0, hi=True)], chain="d20"))   # 20
SC.append(pv("HD", "홍건희", "두산 시절", [], [st("2021년", "65경기 · 17홀드", 0), st("평균자책점", "2.78 · 커리어 하이", 0), st("2022년 · 시즌 중 마무리", "18세이브", 0.6),
                                            st("2023년", "22세이브", 2.6, hi=True)], chain="d20", cont=True))             # 21
SC.append(pv("HD", "홍건희", "두산 첫 네 시즌 · 2020 ~ 2023년", [], [st("세이브", "44", 0.6, hi=True), st("홀드", "39", 0.8, hi=True), st("경기", "237경기", 50), st("승패", "12승 24패", 50), st("네 시즌 평균자책점", "3.46", 50)], chain="d22"))   # 22
SC.append(pv("HD", "홍건희", "2024년 1월 · 첫 FA", [], [st("계약", "두산 잔류 · 2+2년", 0.6)], chain="f23"))                          # 23
SC.append(pv("HD", "홍건희", "2024년 1월 · 첫 FA", [], [st("계약", "두산 잔류 · 2+2년", 0), st("최대", "24억 5천만 원", 2.0, hi=True)], chain="f23", cont=True))   # 24
SC.append(pv("HD", "홍건희", "2024년 1월 · 첫 FA", [], [st("계약", "두산 잔류 · 2+2년", 0), st("최대", "24억 5천만 원", 0), st("첫 2년", "9억 5천만 원", 0.2),
                                                      st("뒤 2년 · 홍건희 선택", "15억 원", 1.2, hi=True)], chain="f23", cont=True))   # 25
SC.append(pv("HD", "홍건희", "2024 ~ 2025년", [], [st("2024년 · 65경기", "평균자책점 2.73", 0.3), st("2024년 · 세이브 · 홀드", "9 · 11", 50), st("2025년 · 20경기 · 팔꿈치 부상", "평균자책점 6.19", 50)], chain="y26"))                       # 26
SC.append(pv("HD", "홍건희", "2024 ~ 2025년", [], [st("2024년 · 65경기", "평균자책점 2.73", 0), st("2024년 · 세이브 · 홀드", "9 · 11", 0), st("2025년 · 20경기 · 팔꿈치 부상", "평균자책점 6.19", 1.0, hi=True)], chain="y26", cont=True))   # 27
SC.append(pv("HD", "홍건희", "2025시즌 뒤", [vsteps([stp("포기", "남은 2년 15억 원", 1.0, c="bad"), stp("선택", "FA 시장", 1.5)])]))   # 28
SC.append(sp(prof("홍건희"), "홍건희", "2026년 1월 · KIA 입단 뒤", [bb("포기한 이유 · 요약", "돈 욕심보다 계약 기간을 길게", 0.6, src=True)], profile=True))       # 29
SC.append(pv("HD", "홍건희", "2025 ~ 2026년 겨울", [vsteps([stp("시장 반응", "다른 구단 관심 적음", 0.2, c="bad"), stp("해가 바뀔 때까지", "미계약", 2.2, c="bad")])]))   # 30
SC.append(pv("H", "홍건희", "2026년 1월 21일", [vsteps([stp("2026년 1월 21일", "친정 KIA와 계약", 1.0, c="good")])], [st("기간", "1년", 50), st("연봉", "6억 5천만 원", 50), st("인센티브 포함", "최대 7억 원", 50, hi=True)], chain="k31"))   # 31
SC.append(pv("H", "홍건희", "2026년 1월 21일", [vsteps([stp("2026년 1월 21일", "친정 KIA와 계약", -1, c="good")])],
             [st("기간", "1년", 0.1), st("연봉", "6억 5천만 원", 1.0), st("인센티브 포함", "최대 7억 원", 2.4, hi=True)], chain="k31", cont=True))   # 32
SC.append(pv("H", "홍건희", "2026년 1월 21일", [vsteps([stp("2026년 1월 21일", "친정 KIA와 계약", -1, c="good")])],
             [st("포기한 계약", "2년 15억 원", 0.1), st("받은 계약", "1년 최대 7억 원", 1.0, hi=True)], chain="k31", cont=True))   # 33
SC.append(sp(prof("홍건희"), "홍건희", "2026년 1월 · KIA 계약 뒤", [bb("친정 복귀 소감", "감회가 새롭다", 1.5, src=True)], profile=True))                             # 34
SC.append(pv("H", "홍건희", "2026 시즌", [vsteps([stp("4월", "1군 3경기 · 무실점", 0.6, c="good")])], chain="s35"))          # 35
# 35~37: 칸이 4줄까지 늘어나므로 처음부터 4줄 기준 크기(템플릿 nS)
SC.append(pv("H", "홍건희", "2026 시즌", [vsteps([stp("4월", "1군 3경기 · 무실점", -1, c="good"), stp("4월 17일 검진", "오른쪽 어깨 극상근 손상", 0.6, c="bad"),
                                           stp("4월 18일", "1군 말소", 2.0, c="bad")])], chain="s35", cont=True))           # 36
SC.append(pv("H", "홍건희", "2026 시즌", [vsteps([stp("4월", "1군 3경기 · 무실점", -1, c="good"), stp("4월 17일 검진", "오른쪽 어깨 극상근 손상", -1, c="bad"),
                                           stp("4월 18일", "1군 말소", -1, c="bad"), stp("9월 1일", "1군 복귀", 1.0, c="good")])], chain="s35", cont=True))   # 37
SC.append(pv("H", "홍건희", "2026년 9월", [vsteps([stp("9월 8일 · 삼성전", "1이닝 2실점", 0.3, c="bad"), stp("9월 14일", "다시 1군 말소", 2.0, c="bad")])], chain="s38"))   # 38
SC.append(pv("H", "홍건희", "2026년 9월", [vsteps([stp("9월 8일 · 삼성전", "1이닝 2실점", -1, c="bad"), stp("9월 14일", "다시 1군 말소", -1, c="bad"),
                                          stp("그 뒤", "1군 등판 없음", 0.6, c="bad")])], chain="s38", cont=True))           # 39
SC.append(pv("H", "홍건희", "2026년 1군 · KBO 기록", [], [st("경기", "4경기", 0.6), st("이닝", "4이닝", 1.0), st("홀드", "1", 2.0), st("평균자책점", "4.50", 2.4, hi=True)], chain="r40"))   # 40
SC.append(pv("H", "홍건희", "2026년 1군 · KBO 기록", [], [st("경기", "4경기", 0), st("이닝", "4이닝", 0), st("홀드", "1", 0), st("평균자책점", "4.50", 0),
                                                       st("팔꿈치", "뼛조각 제거 수술 이야기", 0.2, hi=True)], chain="r40", cont=True))   # 41
SC.append(pv("HD", "홍건희", "1군 통산 · KBO 기록", [], [st("경기", "492경기", 0.6), st("승패", "27승 48패", 1.3), st("세이브 · 홀드", "58세이브 56홀드", 2.0),
                                                     st("평균자책점", "4.92", 3.0, hi=True)]))                                 # 42
SC.append(pv("H", "홍건희", "2011 ~ 2026년", [vsteps([stp("2011년", "KIA 데뷔", 0.1), stp("2020 ~ 2025년", "두산", 0.8, c="good"),
                                                 stp("2026년", "KIA 복귀", 1.6), stp("10월 23일", "재계약 불가", 2.4, c="bad")])]))   # 43
# ── 3막 · 고종욱 ──
SC.append(S(0, "photo", img="경기/고종욱_KIA_엑스포츠", fit="cover", text="", h=760))                                              # 44
SC.append(pp("고종욱", "KIA 외야수", [vsteps([stp("대학", "한양대", 0.3), stp("2011년", "넥센 3라운드 · 전체 19순위", 1.2, c="good")])]))   # 45
SC.append(pv("G", "고종욱", "넥센 시절", [], [st("2015 ~ 2017년", "3년 연속 3할", 0.3), st("2016년", "타율 .334 · 176안타", 2.0, hi=True)]))   # 46
SC.append(pv("G", "고종욱", "2018년 12월", [vsteps([stp("2018년 12월", "KBO 최초 삼각 트레이드", 0.6), stp("이적", "넥센 → SK", 1.8, c="good")])]))   # 47
SC.append(S(0, "tiles", title="2018년 12월 · 세 구단 삼각 트레이드", items=[dict(top="넥센 → SK", v="고종욱", at=0.1), dict(top="SK → 삼성", v="김동엽", at=0.6),
                                                                      dict(top="삼성 → 넥센", v="이지영", at=0.9)]))   # 48
SC.append(pv("G", "고종욱", "2019년 · SK", [], [st("타율", ".323", 0.6), st("안타", "159개", 1.3), st("도루", "31개", 1.6, hi=True)]))   # 49
SC.append(pv("G", "고종욱", "2021 ~ 2022년", [vsteps([stp("2021시즌 뒤", "SSG에서 방출", 1.0, c="bad")])], chain="g50"))             # 50
SC.append(pv("G", "고종욱", "2021 ~ 2022년", [vsteps([stp("2021시즌 뒤", "SSG에서 방출", -1, c="bad"), stp("2022년", "KIA 입단 · 연봉 7천만 원", 0.6, c="good")])], chain="g50", cont=True))   # 51
SC.append(pv("G", "고종욱", "KIA 시절", [], [st("역할", "주로 대타", 0.2), st("2023년", "114경기 · 타율 .296", 2.0, hi=True), st("2023년 · 홈런 · 타점", "3홈런 · 39타점", 50), st("2023시즌 뒤 FA", "2년 최대 5억 원", 50)], chain="g52"))   # 52
SC.append(pv("G", "고종욱", "KIA 시절", [], [st("역할", "주로 대타", 0), st("2023년", "114경기 · 타율 .296", 0), st("2023년 · 홈런 · 타점", "3홈런 · 39타점", 0), st("2023시즌 뒤 FA", "2년 최대 5억 원", 0.6, hi=True)], chain="g52", cont=True))   # 53
SC.append(pv("G", "고종욱", "FA 계약 뒤", [], [st("2024년", "28경기 · 타율 .250", 0), st("2025년", "46경기 · 타율 .296", 0.2, hi=True)], chain="g54", cont=True))      # 54
SC.append(pv("G", "고종욱", "2026년 1군", [], [st("경기", "27경기", 0.6), st("타수 · 안타", "32타수 3안타", 1.3), st("타율", ".094", 2.6, hi=True)]))   # 55
SC.append(pv("G", "고종욱", "1군 통산 · KBO 기록", [], [st("경기", "1,133경기", 0.6), st("타율", ".300", 1.0, hi=True), st("안타 · 홈런", "992안타 · 50홈런", 2.0), st("타점", "417개", 50)], chain="g56"))   # 56
SC.append(pv("G", "고종욱", "1군 통산 · KBO 기록", [vstamp("KIA 5시즌 · 통산 타율 3할", 0.6, "gold", size=48)],
             [st("경기", "1,133경기", 0), st("타율", ".300", 0, hi=True), st("안타 · 홈런", "992안타 · 50홈런", 0), st("타점", "417개", 0)], chain="g56", cont=True))   # 57
# ── 4막 · 이창진 ──
SC.append(S(0, "photo", img="경기/이창진_KIA_엑스포츠", fit="cover", text="", h=760))                                              # 58
SC.append(pp("이창진", "KIA 외야수", [vsteps([stp("학교", "인천고 · 건국대", 0.3), stp("2014년", "롯데 2차 6라운드", 1.5, c="good")])], chain="c59"))   # 59
SC.append(pp("이창진", "KIA 외야수", [vsteps([stp("학교", "인천고 · 건국대", -1), stp("2014년", "롯데 2차 6라운드", -1, c="good"), stp("2015년", "롯데 ↔ KT 4대 5 트레이드", 0.6)])], chain="c59", cont=True))   # 60
SC.append(pp("이창진", "KIA 외야수", [vsteps([stp("학교", "인천고 · 건국대", -1), stp("2014년", "롯데 2차 6라운드", -1, c="good"), stp("2015년", "롯데 ↔ KT 4대 5 트레이드", -1),
                                          stp("2018년 6월", "오준혁과 1대 1 → KIA", 0.8, c="good")])], chain="c59", cont=True))   # 61
SC.append(pv("LC", "이창진", "KIA 시절", [], [st("2019년 · 첫 풀타임", "133경기 · 타율 .270", 0.8), st("그해", "신인왕 후보", 2.0, hi=True)], chain="c62"))   # 62
SC.append(pv("LC", "이창진", "KIA 시절", [], [st("2019년 · 첫 풀타임", "133경기 · 타율 .270", 0), st("그해", "신인왕 후보", 0, hi=True), st("2021 ~ 2024년", "4년 연속 100경기 넘게", 0.4),
                                            st("2022년", "타율 .301", 3.0, hi=True)], chain="c62", cont=True))          # 63
SC.append(pv("LK", "이창진", "2024 한국시리즈 4차전", [], [st("최형우 결장", "허리 통증", 1.0), st("이창진", "7번 좌익수 선발", 2.0, hi=True)], chain="c64"))   # 64
SC.append(pv("LK", "이창진", "2024 한국시리즈 4차전", [vstamp("그해 KIA 통합우승", 2.2, "gold", size=48)],
             [st("최형우 결장", "허리 통증", 0), st("이창진", "7번 좌익수 선발", 0, hi=True), st("기록", "4타수 2안타 · 볼넷 1", 0.2, hi=True)], chain="c64", cont=True))   # 65
SC.append(pv("LC", "이창진", "최근 두 시즌", [], [st("2025년", "37경기", 0.3), st("2026년", "3경기", 1.0, hi=True), st("원인", "부상 · 타격 부진", 50), st("올해 기록", "4타수 무안타", 50)], chain="c66"))                  # 66
SC.append(pp("이창진", "1군 통산 · KBO 기록", [], [st("경기", "655경기", 0.6), st("타율", ".260", 1.0), st("안타", "433개", 1.6, hi=True)], chain="c67"))   # 67
SC.append(pp("이창진", "1군 통산 · KBO 기록", [vstamp("KIA에서 9시즌", 0.3, "gold", size=52)],
             [st("홈런", "22개", 0), st("타점", "192개", 0), st("도루", "29개", 0)], chain="c67b", cont=True))    # 68
# ── 5막 · 김대유 · 김사윤 · 윤중현 · 육성 ──
DY = "김대유"
SC.append(pp(DY, "KIA 왼손 투수", [vsteps([stp("2010년", "넥센 3라운드 · 전체 18순위", 50), stp("그 뒤", "SK · KT", 50), stp("전성기", "LG", 50, c="good")])], chain="dy"))   # 69
SC.append(pp(DY, "KIA 왼손 투수", [vsteps([stp("2010년", "넥센 3라운드 · 전체 18순위", 1.2), stp("그 뒤", "SK · KT", 50), stp("전성기", "LG", 50, c="good")])], chain="dy", cont=True))   # 70
SC.append(pp(DY, "KIA 왼손 투수", [vsteps([stp("2010년", "넥센 3라운드 · 전체 18순위", -1), stp("그 뒤", "SK · KT", 0.2), stp("전성기", "LG", 1.0, c="good")])], chain="dy", cont=True))   # 71
SC.append(pp(DY, "LG 시절", [], [st("2021년 · 64경기 · 24홀드", "평균자책점 2.13", 0.2, hi=True), st("2022년 · 13홀드", "평균자책점 2.04", 2.0, hi=True), st("LG 2년 합계", "37홀드", 50)], chain="dy2"))   # 72
SC.append(pv(None, "2022년 11월", "FA 보상선수", [], [st("FA 포수 박동원", "KIA → LG", 1.0), st("보상선수", "김대유 · LG → KIA", 2.4, hi=True)], team="KIA"))   # 73
SC.append(pp(DY, "KIA 시절 · 평균자책점", [], [st("2023년", "5.11", 1.0), st("2024년", "8.28", 2.0, hi=True)], chain="dy3"))        # 74
SC.append(pp(DY, "KIA 시절 · 평균자책점", [], [st("2023년", "5.11", 0), st("2024년", "8.28", 0, hi=True), st("2025년", "15경기 · 9.72", 0.3), st("2026년", "1군 0경기", 2.0, hi=True)], chain="dy3", cont=True))   # 75
SC.append(pp(DY, "1군 통산 · KBO 기록", [], [st("경기", "255경기", 0.6), st("승패", "6승 6패", 1.2), st("홀드", "50", 1.6), st("평균자책점", "4.55", 2.0, hi=True)]))   # 76
SC.append(pp("김사윤", "KIA 왼손 투수", [], [st("개명 전 이름", "김정빈", 1.4, hi=True)], chain="ks"))                                  # 77
SC.append(pp("김사윤", "KIA 왼손 투수", [], [st("개명 전 이름", "김정빈", 0, hi=True), st("2022년 5월 · SSG와 트레이드", "김민식 ↔ 김정빈 · 임석진", 0.6)], chain="ks", cont=True))   # 78
SC.append(pp("김사윤", "KIA 시절", [], [st("2023년 · 팔꿈치 수술", "1군 0경기", 0), st("2024년 · 23경기", "평균자책점 4.62", 0.3), st("2025 ~ 2026년", "1군 0경기", 2.4, hi=True)], chain="ks3", cont=True))   # 79
SC.append(pp("윤중현", "KIA 사이드암", [vsteps([stp("대학", "성균관대", 0.6), stp("2018년", "2차 9라운드 · 전체 86순위", 2.0, c="good")])], [st("2021년", "30경기 · 5승", 50), st("1군 통산", "132경기 · 11승 8패", 50, hi=True)], chain="yj"))   # 80
SC.append(pp("윤중현", "KIA 사이드암", [vsteps([stp("대학", "성균관대", -1), stp("2018년", "2차 9라운드 · 전체 86순위", -1, c="good")])],
             [st("2021년", "30경기 · 5승", 0.3), st("1군 통산", "132경기 · 11승 8패", 2.4, hi=True)], chain="yj", cont=True))   # 81
SC.append(pv(None, "육성선수 10명", "KBO에 말소 요청", [], [st("투수", "장민기 · 강이준 · 정다훈", 0.6), st("포수", "김선우 · 이도훈", 1.6)], chain="u82"))   # 82
SC.append(pv(None, "육성선수 10명", "KBO에 말소 요청", [], [st("투수", "장민기 · 강이준 · 정다훈", 0), st("포수", "김선우 · 이도훈", 0), st("내야수", "오정환 · 장시현", 0.2),
                                                       st("외야수", "이준범 · 천정민 · 김민수", 1.0)], chain="u82", cont=True))   # 83
# ── 6막 · 기아의 겨울과 다른 구단 ──
SC.append(pv(None, "KIA 타이거즈", "이번 겨울", [vstamp("삼성과 플레이오프 먼저", 2.2, "gold", size=52)]))                              # 84
SC.append(pv(K + "이범호_감독", "이범호", "KIA 감독", [], [st("2024년 11월", "재계약", 0.3), st("조건", "3년 총액 26억 원", 1.0, hi=True), st("계약 기간", "2027년까지", 2.0)], profile=True))   # 85
SC.append(pv(prof("김범수"), "김범수", "KIA 투수 · 외부 FA", [], [st("지난겨울 계약", "3년 총액 20억 원", 1.4, hi=True)], profile=True))   # 86
SC.append(pv("H", "홍건희", "지난겨울 영입", [vstamp("1년 만에 이별", 1.0, "bad", size=56)]))                                          # 87
_RL = [dict(label="롯데", team="롯데", value=16, unit="명", at=0.6), dict(label="두산", team="두산", value=11, unit="명", at=0.6), dict(label="LG", team="LG", value=11, unit="명", at=0.6),
       dict(label="삼성", team="삼성", value=10, unit="명", at=0.6), dict(label="KT", team="KT", value=10, unit="명", at=0.6), dict(label="SSG", team="SSG", value=8, unit="명", at=0.6),
       dict(label="키움", team="키움", value=8, unit="명", at=0.6), dict(label="한화", team="한화", value=6, unit="명", at=0.6), dict(label="KIA", team="KIA", value=6, unit="명", at=0.6, hi=True)]
SC.append(S(0, "bars", title="재계약 불가 · 10월 23일 기준", items=_RL, max=16, chain="b88", text="9개 구단 합계 86명 · 육성선수 말소 제외", textAt=2.6, size=56))   # 88
SC.append(S(0, "bars", title="재계약 불가 · 10월 23일 기준", items=_RL, max=16, chain="b88", cont=True, text="9개 구단 합계 86명 · 육성선수 말소 제외", size=56))                          # 89
SC.append(S(0, "tiles", title="아직 발표 소식 없음", items=[dict(team="NC", k="10월 23일 기준", v="발표 소식 없음", at=0.1)]))           # 90
SC.append(S(0, "question", text="홍건희의 15억 포기\n옳은 선택이었을까?", img="경기/홍건희_KIA투구_SPOTV", size=88))                                 # 91

INS_SC = {
    8: [pv(None, "정규시즌 최종전", "10월 12일 · 광주", [], [st("결과", "LG에 4대 2 승", 0.6), st("순위", "LG보다 반 경기 앞선 3위", 2.2, hi=True)])],
    11: [pv(None, "한국시리즈", "7전 4선승제", [], [st("기다리는 팀", "정규시즌 1위 KT", 0, hi=True), st("KT 1위 확정", "10월 5일 · 5년 만", 0.6)], chain="ks11", cont=True)],
    19: [pv("HD", "홍건희", "2020년 · 두산 이적 첫해", [], [st("경기", "50경기", 0.8), st("평균자책점", "4.76", 2.0, hi=True)])],
    21: [pv("HD", "홍건희", "마무리 시절", [], [st("2022년 · 마무리", "58경기 · 평균자책점 3.48", 0.3), st("2023년 · 마무리", "64경기 · 평균자책점 3.06", 1.6)])],
    22: [pv("HD", "홍건희", "두산 첫 네 시즌 · 2020 ~ 2023년", [], [st("세이브", "44", 0, hi=True), st("홀드", "39", 0, hi=True), st("경기", "237경기", 0.4), st("승패", "12승 24패", 1.0), st("네 시즌 평균자책점", "3.46", 2.0, hi=True)], chain="d22", cont=True)],
    25: [pv("HD", "홍건희", "2024년 1월 25일 · 계약 구성", [], [st("계약금", "3억 원", 0.6), st("연봉 총액", "21억 원", 1.4), st("인센티브", "5천만 원", 2.4)])],
    26: [pv("HD", "홍건희", "2024 ~ 2025년", [], [st("2024년 · 65경기", "평균자책점 2.73", 0), st("2024년 · 세이브 · 홀드", "9 · 11", 0.2, hi=True), st("2025년 · 20경기 · 팔꿈치 부상", "평균자책점 6.19", 50)], chain="y26", cont=True)],
    27: [pv("HD", "홍건희", "2025년 · 팔꿈치 부상", [], [st("이닝", "16이닝", 0.6), st("승패", "2승 1패", 1.6, hi=True)])],
    28: [pv("HD", "홍건희", "옵트아웃", [vsteps([stp("남은 계약", "포기", 0.6, c="bad"), stp("신분", "FA", 1.2)])])],
    37: [pv("H", "홍건희", "2026년 9월 1일 복귀", [], [st("복귀 전 퓨처스리그", "2경기", 1.0, hi=True)]),
         sp(K + "이범호_감독", "이범호", "KIA 감독 · 9월 1일", [bb("홍건희 복귀", "연투는 웬만하면 안 시킨다", 1.5, src=True)], profile=True)],
    46: [pv("G", "고종욱", "넥센 시절 · 2016년", [], [st("홈런", "8개", 0.4), st("타점", "72개", 1.0, hi=True)])],
    52: [pv("G", "고종욱", "KIA 시절", [], [st("역할", "주로 대타", 0), st("2023년", "114경기 · 타율 .296", 0, hi=True), st("2023년 · 홈런 · 타점", "3홈런 · 39타점", 0.3), st("2023시즌 뒤 FA", "2년 최대 5억 원", 50)], chain="g52", cont=True)],
    53: [pv("G", "고종욱", "FA 계약 뒤", [], [st("2024년", "28경기 · 타율 .250", 0.6), st("2025년", "46경기 · 타율 .296", 50)], chain="g54")],
    56: [pv("G", "고종욱", "1군 통산 · KBO 기록", [], [st("경기", "1,133경기", 0), st("타율", ".300", 0, hi=True), st("안타 · 홈런", "992안타 · 50홈런", 0), st("타점", "417개", 0.3, hi=True)], chain="g56", cont=True)],
    65: [pv("LK", "이창진", "2024 한국시리즈 4차전 · 3회", [vsteps([stp("이창진", "볼넷 · 만루", 0.6, c="good"), stp("다음 타자 김태군", "만루홈런", 1.6, c="good")])])],
    66: [pv("LC", "이창진", "최근 두 시즌", [], [st("2025년", "37경기", 0), st("2026년", "3경기", 0, hi=True), st("원인", "부상 · 타격 부진", 0.2), st("올해 기록", "4타수 무안타", 1.0, hi=True)], chain="c66", cont=True)],
    67: [pp("이창진", "1군 통산 · KBO 기록", [], [st("홈런", "22개", 0.2), st("타점", "192개", 0.8), st("도루", "29개", 1.6)], chain="c67b")],
    71: [pp(DY, "1군 데뷔 · 이적", [vsteps([stp("2014년", "SK에서 1군 데뷔", 0.6), stp("LG 이적", "2차 드래프트", 50)])], chain="dy1"),
         pp(DY, "1군 데뷔 · 이적", [vsteps([stp("2014년", "SK에서 1군 데뷔", -1), stp("LG 이적", "2차 드래프트", 0.6, c="good")])], chain="dy1", cont=True)],
    72: [pp(DY, "LG 시절", [], [st("2021년 · 64경기 · 24홀드", "평균자책점 2.13", 0, hi=True), st("2022년 · 13홀드", "평균자책점 2.04", 0, hi=True), st("LG 2년 합계", "37홀드", 0.4)], chain="dy2", cont=True)],
    75: [pp(DY, "2024년", [vstamp("KIA 통합우승 멤버", 2.0, "gold", size=52)], [st("2024년", "37경기 · 8홀드", 0.3)])],
    78: [pp("김사윤", "SK 시절", [vsteps([stp("2013년", "SK 3라운드 · 전체 28순위", 0.6, c="good"), stp("2020년", "57경기 · 10홀드", 50)])], chain="ks2"),
         pp("김사윤", "SK 시절", [vsteps([stp("2013년", "SK 3라운드 · 전체 28순위", -1, c="good"), stp("2020년", "57경기 · 10홀드", 0.6)])], chain="ks2", cont=True),
         pp("김사윤", "KIA 이적 첫해 · 2022년", [], [st("경기", "31경기", 0.6), st("승리", "3승", 1.4, hi=True)]),
         pp("김사윤", "KIA 시절", [], [st("2023년 · 팔꿈치 수술", "1군 0경기", 0.6), st("2024년 · 23경기", "평균자책점 4.62", 50), st("2025 ~ 2026년", "1군 0경기", 50)], chain="ks3")],
    81: [pp("윤중현", "KIA 사이드암", [], [st("2022년", "47경기 · 3승", 0.6), st("2024년 · 11경기", "평균자책점 13.94", 50), st("2025년", "13경기 · 1승", 50)], chain="yj2"),
         pp("윤중현", "KIA 사이드암", [], [st("2022년", "47경기 · 3승", 0), st("2024년 · 11경기", "평균자책점 13.94", 0.6), st("2025년", "13경기 · 1승", 2.4, hi=True)], chain="yj2", cont=True)],
}
assert len(SC) == len(_g['_t'].V1), len(SC)
_SC = []
for _i, _sc in enumerate(SC):
    _SC.append(_sc); _SC.extend(INS_SC.get(_i, []))
for _k, _v in INS_SC.items(): assert len(_v) == len(_g['_t'].INS.get(_k, [])), _k
SC = _SC
NI = _g['_t'].NEWIDX
N = len(TEXT)
assert len(SC) == N, (N, len(SC))
CTA_LINE = {"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0}
lines, scenes = [], []
for j, t in enumerate(TEXT):
    sc = dict(SC[j]); sc['startLine'] = j
    lines.append(L(narr_of(t), sub_of(t))); scenes.append(sc)
lines.append(dict(CTA_LINE))

CH = [{"key": "기아의 10월", "title": "기아의 10월", "from": NI[6], "to": NI[15] - 1},
      {"key": "홍건희", "title": "홍건희 · 15억 포기와 1년 계약", "from": NI[15], "to": NI[44] - 1},
      {"key": "고종욱", "title": "고종욱 · 통산 타율 3할", "from": NI[44], "to": NI[58] - 1},
      {"key": "이창진", "title": "이창진 · 2024 통합우승 멤버", "from": NI[58], "to": NI[69] - 1},
      {"key": "김대유 · 김사윤 · 윤중현", "title": "김대유 · 김사윤 · 윤중현 · 육성선수", "from": NI[69], "to": NI[84] - 1},
      {"key": "다른 구단", "title": "기아의 겨울과 다른 구단", "from": NI[84], "to": N - 1}]

TAGS = ["기아 방출", "KIA 방출", "홍건희", "홍건희 방출", "홍건희 옵트아웃", "고종욱", "고종욱 방출", "이창진", "김대유", "김사윤", "윤중현", "KIA 타이거즈", "재계약 불가",
        "방출 명단", "프로야구 방출", "2026 방출", "플레이오프", "프로야구", "KBO", "야구자판기"]
DESC = ("기아 타이거즈가 플레이오프 1차전을 이틀 앞둔 10월 23일 선수 6명과 재계약하지 않기로 했어요. 육성선수 10명은 KBO에 말소를 요청해 모두 16명이 팀을 떠나요.\n\n"
        "홍건희는 2011년 기아에 입단했고, 2020년 6월 류지혁과의 트레이드로 두산에 가 2021년 17홀드 평균자책점 2.78, 2022년 18세이브, 2023년 22세이브를 기록했어요. "
        "2024년 1월 두산과 2+2년 최대 24억 5천만 원에 첫 FA 계약을 맺었지만, 지난해 팔꿈치 부상 뒤 남은 2년 15억 원을 포기하고 FA 시장에 나왔어요(본인: 돈 욕심보다 계약 기간을 더 길게 하고 싶었다). "
        "올해 1월 친정 기아와 1년 최대 7억 원(연봉 6억 5천만 원)에 계약했지만, 4월 어깨 극상근 손상으로 이탈했고 1군 4경기 4이닝 1홀드 평균자책점 4.50에 그쳤어요. 1군 통산 492경기 27승 48패 58세이브 56홀드 평균자책점 4.92.\n\n"
        "고종욱(1군 통산 1,133경기 타율 .300)·이창진(2024 한국시리즈 4차전 선발, 통산 655경기 타율 .260)·김대유(LG 시절 2021·2022 평균자책점 2점대, 박동원 FA 보상선수)·김사윤(개명 전 김정빈)·윤중현도 떠나요.\n\n"
        "재계약 불가 6명: 외야수 고종욱·이창진 / 투수 홍건희·김사윤·김대유·윤중현\n"
        "육성선수 말소 요청 10명: 투수 장민기·강이준·정다훈 / 포수 김선우·이도훈 / 내야수 오정환·장시현 / 외야수 이준범·천정민·김민수\n\n"
        "기아는 2024년 통합우승 뒤 지난해 8위, 올해 3위로 준플레이오프에서 LG를 3승 0패로 꺾었고, 10월 25일 대구에서 삼성과 플레이오프 1차전을 치러요. "
        "10월 23일 기준 9개 구단(롯데 16·두산 11·LG 11·삼성 10·KT 10·SSG 8·키움 8·한화 6·기아 6)의 재계약 불가 인원을 모두 더하면 86명이에요(기아 육성선수 10명 제외).\n\n"
        "여러분은 홍건희의 2년 15억 원 포기가 옳은 선택이었다고 보시나요? 댓글로 남겨 주세요.\n\n"
        "기록: KBO 기록실(10월 23일 조회). 기사: SPOTV·서울신문·전남일보·스포츠월드·스포츠경향·이투데이·위키트리·뉴스1·OSEN·MHN·톱스타뉴스(10/23), "
        "엑스포츠뉴스(2025/11/18·2026/1/21·9/1·9/4), OSEN(2024/2/1·2026/1/24), 일간스포츠(2026/1/23), 노컷뉴스(2020/6/7·2024/1/16·1/26), 서울신문(2024/1/26), "
        "아시아경제·SPOTV(2026/4/18), 스포츠경향(2025/11/18·2026/9/1), 뉴스핌·머니투데이(10/23), 뉴시스·SPOTV(2022/11/27), 경향신문·일간스포츠(10/12·10/21), "
        "고종욱: OSEN(2021/11/5·2023/11/19·2025/1/9), 매일신문·경기일보(2018/12), 엑스포츠뉴스(2026/1/30) / 이창진: 엑스포츠뉴스·OSEN(2024/10/27), 서울신문(2022/7/28), 다음스포츠(2020/3/3) / "
        "김대유: 마이데일리(2023/11/12), 엑스포츠뉴스(2025/6/21) / 김사윤: SPOTV(2025/2/8), MK스포츠(2024) / 윤중현: OSEN(2021/11/16) / 이범호 감독 계약: 스포츠서울(2024/11/3) / "
        "다른 구단 발표: 머니투데이(10/3·10/19·10/22), 충청투데이(10/3), SPOTV(10/7·10/22), MK스포츠(10/8), 일간스포츠(10/10·10/19·10/22), 뉴시스·톱스타뉴스(10/11), 엑스포츠뉴스(10/19)\n"
        "사진: SPOTV(KIA 타이거즈 제공), 엑스포츠뉴스, 구단 공식 프로필")
SOURCE = "사실 출처 = 프로젝트 claude/1023-롱폼28-기아방출-근거모음.md (기사 본문 2곳 이상) + KBO 기록실 정규시즌 통산·연도별(10/23 조회)."

EP = {"introChapter": "오프닝", "date": "2026-10-23", "gameDate": "2026-10-23", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.3, "ttsTempoSlow": 1.3,
      "rev": "1023-long28-v2", "topic": "기아방출", "endcardSec": 10,
      "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 9000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "thumbFile": "선수이미지/상황별/썸네일_롱폼28_기아방출.jpg", "mascot": False, "source": SOURCE,
      "youtube": {"title": "기아 방출 | 15억 포기하고 친정 돌아온 홍건희, 1년 만에 방출 #기아 #홍건희 #방출",
                  "description": DESC, "tags": TAGS,
                  "hashtags": ["#기아타이거즈", "#홍건희", "#고종욱", "#이창진", "#방출", "#재계약불가", "#프로야구", "#KBO", "#야구자판기"]}}

if __name__ == '__main__':
    HOLD = {NI[k]: v for k, v in {0: 0.35, 4: 0.35, 5: 0.35, 14: 0.35, 43: 0.8, 57: 0.8, 68: 0.4, 83: 0.35, 90: 0.35}.items()}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in HOLD: l['gapAfter'] = HOLD[i]
    lines[-2]['gapAfter'] = 0.5
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-10-23_롱폼3.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = 0
    for i, l in enumerate(EP['lines'][:-1]):
        for bq in l['narr'].split(' / '):
            if len(re.sub(r'[\s,?]', '', bq)) > 22: print('호흡 초과', i, bq)
        tot += len(l['narr'].replace(' / ', ' ').replace('+', ''))
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
