# -*- coding: utf-8 -*-
"""11/11 쇼츠 「2027 FA 일정」 콘티 (세로 · 모션그래픽 v_ 장면).
근거: KBO FA 절차(2025.11.5 공시 기사: 공시 → 2일 이내 신청 → 마감 다음 날 승인 공시 → 그다음 날 협상),
일간스포츠 11/10(13일 공시·16일 승인), 서울신문 11/10(FA 선수 명단·MLB 직장폐쇄), 뉴스핌 11/3(노시환 12/3 07:00 마감)."""
import json, re, sys
src = open('/home/claude/kt_ks/gen_1028_long33.py', encoding='utf-8').read()
ns = {'re': re}; exec(src[src.index('DIG = '):src.index('def sub_of')], ns); narr_of = ns['narr_of']
sys.path.insert(0, '/home/claude/ss27')
from gen_rank_0923 import wrap
def W(t):
    if len(t) <= 16: return t
    return wrap(t, 16)
LINES = [
 ('2027 FA 일정 / 구자욱과 원태인을 포함한 FA 선수들은 / 언제부터 계약할 수 있을까요?', None),
 ('11월 13일 금요일에 / KBO가 FA 자격 선수 명단을 공시해요', None),
 ('자격을 얻은 선수는 / 이틀 안인 15일까지 / FA 신청을 하고', None),
 ('KBO는 신청 마감 다음 날인 16일에 / 승인 선수를 공시해요', None),
 ('그리고 17일부터 / 해외 구단을 포함한 모든 구단과 / 협상할 수 있어요', None),
 ('삼성은 구자욱과 원태인을 / 둘 다 잡겠다는 목표지만 / 샐러리캡이 빠듯해요', None),
 ('포수 시장엔 LG 박동원, / KIA 김태군, / 한화 최재훈이 나오고', None),
 ('두산 양의지는 / 본인 옵션에 따라 / 시장에 나올지가 정해져요', None),
 ('외야에선 LG 홍창기, / SSG 최지훈, / KIA 김호령, / 두산 정수빈이 관심을 받고 있어요', None),
 ('같은 시기 한화 노시환의 / 메이저리그 포스팅 협상은 / 12월 3일 오전 7시에 마감돼요', None),
 ('MLB 노사협약도 12월 1일에 끝나는데 / 직장폐쇄가 되면 / KBO 구단들의 외국인 선수 영입도 / 막힐 수 있어요', None),
 ('여러분 팀이 / 이번 FA에서 꼭 잡아야 할 선수는 누구인가요?', None),
]
def NARR(sub):
    n = narr_of(sub).replace('%', ' 퍼센트')
    n = re.sub(r'([일이삼사오육칠팔구십]+) 월 ([일이삼사오육칠팔구십]+) 일', r'\1월 \2일', n)
    n = re.sub(r'(?<![가-힣])([이삼사오육칠팔구십]?십?[일이삼사오육칠팔구]) 일(까지|에|부터)', r'\1일\2', n)
    n = n.replace('오전 칠시', '오전 일곱 시').replace('FA', '에프에이').replace('KBO', '케이비오').replace('MLB', '엠엘비').replace('SSG', '에스에스지')
    n = n.replace('이천이십칠 에프에이', '이천이십칠, 에프에이')   # 11/4 '기아, 역대'처럼 첫 낱말 뒤 살짝 쉼
    return n
lines = []
for sub, nar in LINES:
    n = nar or NARR(sub)
    lines.append({"narr": n, "sub": "|".join(W(p.strip()) for p in sub.split(' / '))})
lines[-1]['pace'] = 'slow'
lines.append({"narr": "채널 구독하고 매일 야구 이슈 받아보세요", "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})

G = lambda n: '경기/' + n
GU, WT = G('구자욱_KSMVP_1108'), G('원태인_KS5차전_1108')
def C(name, img, team, at, **k): return dict(dict(name=name, img=img, team=team, at=at), **k)
TL_ITEMS = [dict(d='11월 13일 (금)', t='FA 자격 선수 공시'), dict(d='11월 15일 (일)', t='FA 신청 마감', s='공시 뒤 이틀 안'),
            dict(d='11월 16일 (월)', t='승인 선수 공시'), dict(d='11월 17일 (화)', t='협상 시작', s='해외 구단 포함 모든 구단', hi=True)]
def TLs(ats, chain=True):
    its = []
    for i, it in enumerate(TL_ITEMS):
        x = dict(it); x['at'] = ats[i]; its.append(x)
    return dict(type='v_tline', items=its, chain='tl' if chain else None)
SC = [
 dict(type='v_duo', cards=[C('구자욱', GU, '삼성', -1), C('원태인', WT, '삼성', -1)], tag='협상은 언제부터?', tagAt=2),   # 첫 프레임부터 제목·사진·이름
 TLs([0, 50, 50, 50]),
 TLs([-1, 1, 50, 50]),
 TLs([-1, -1, 0, 50]),
 TLs([-1, -1, -1, 0]),
 dict(type='v_duo', cards=[C('구자욱', GU, '삼성', 0), C('원태인', WT, '삼성', 0)], tag='삼성 · 둘 다 잡는 게 목표', tagAt=1, stamp='샐러리캡 빠듯', stampAt=2),
 dict(type='v_grid', title='포수', cards=[C('박동원', G('박동원_세리머니_LG제공'), 'LG', 0), C('김태군', G('김태군_덕아웃_0729_KIA제공'), 'KIA', 1), C('최재훈', G('최재훈_세리머니_한화제공'), '한화', 2), C('양의지', G('양의지_300호_두산제공_HQ'), '두산', 50)], chain='g1'),
 dict(type='v_grid', title='포수', cards=[C('박동원', G('박동원_세리머니_LG제공'), 'LG', -1), C('김태군', G('김태군_덕아웃_0729_KIA제공'), 'KIA', -1), C('최재훈', G('최재훈_세리머니_한화제공'), '한화', -1), C('양의지', G('양의지_300호_두산제공_HQ'), '두산', 0, tag='본인 옵션에 따라', tagAt=1)], chain='g1'),
 dict(type='v_grid', title='외야', cards=[C('홍창기', G('홍창기_상체_0921_LG제공'), 'LG', 0), C('최지훈', G('최지훈_5타점_0920_SSG제공'), 'SSG', 1), C('김호령', G('김호령_환호_연합뉴스'), 'KIA', 2), C('정수빈', G('정수빈_환영_0929_두산제공'), '두산', 3)], chain='g1'),
 dict(type='v_cal', month='2026년 12월', marks=[dict(day=3, lab='노시환 포스팅 마감', sub='12월 3일 오전 7시', img=G('노시환_손하트_1010_한화제공'), team='한화', at=0, sAt=2, c='gold'), dict(day=1, lab='MLB 노사협약 만료', sub='직장폐쇄되면 외국인 영입도 막힘', at=50, c='red')], chain='cal'),
 dict(type='v_cal', month='2026년 12월', marks=[dict(day=3, lab='노시환 포스팅 마감', sub='12월 3일 오전 7시', img=G('노시환_손하트_1010_한화제공'), team='한화', at=-1, c='gold'), dict(day=1, lab='MLB 노사협약 만료', sub='직장폐쇄되면 외국인 영입도 막힘', at=0, sAt=1, c='red')], chain='cal'),
 dict(type='v_q', text=['여러분 팀이 꼭', '잡아야 할 FA는?'], chain='q'),
 dict(type='v_q', text=['여러분 팀이 꼭', '잡아야 할 FA는?'], chain='q'),
]
for i, s in enumerate(SC):
    s['startLine'] = i
    if s.get('chain') is None: s.pop('chain', None)
assert len(SC) == len(lines)
EP = {"date": "2026-11-11", "gameDate": "2026-11-11", "series": "야구롱폼", "vertical": True, "theme": "mg", "railTitle": "", "focusTeam": "",
      "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15, "rev": "1111-fasched-v1", "mascot": False, "topic": "2027FA일정",
      "vtitle": ["2027 FA 일정"], "gapScale": 0.6, "pauseMax": 0.18,
      "chapters": [dict(from_=0, to=0, short='2027 FA'), dict(from_=1, to=4, short='FA 일정'), dict(from_=5, to=8, short='FA 시장 큰 이름'), dict(from_=9, to=10, short='같이 볼 마감'), dict(from_=11, short='여러분 생각은?')],
      "source": "KBO FA 절차(2025.11.5 공시 기사) · 일간스포츠 2026.11.10 · 서울신문 2026.11.10 · 뉴스핌 2026.11.3",
      "lines": lines, "scenes": SC}
EP['mgChapters'] = [{('from' if k == 'from_' else k): v for k, v in c.items()} for c in EP.pop('chapters')]   # 쇼츠는 설명란 챕터 없음 — 이음 판 칸 이름만
PREV = json.load(open('/mnt/user-data/outputs/ss27_mg10/2026-11-10_롱폼.json', encoding='utf-8'))['youtube']['title'].split(' | ')[0]   # 지난 영상 = 삼성 2027편
EP['youtube'] = {
 "title": "2027 FA 일정 | 11월 13일 명단 공개, 구자욱·원태인 협상은 17일부터",
 "description": "2027 프로야구 FA 일정을 한 번에 정리했어요. KBO는 11월 13일 FA 자격 선수 명단을 공시하고, 선수들은 15일까지 신청, 16일 승인 선수 공시, 17일부터 해외 구단을 포함한 모든 구단과 협상할 수 있어요(KBO 공식 공지 전 예정 일정).\n삼성은 구자욱과 원태인을 둘 다 잡겠다는 목표지만 샐러리캡이 빠듯해요. 포수 시장엔 LG 박동원, KIA 김태군, 한화 최재훈이 나오고, 두산 양의지는 본인 옵션에 따라 시장에 나올지가 정해져요. 외야에선 LG 홍창기, SSG 최지훈, KIA 김호령, 두산 정수빈이 관심을 받고 있어요.\n같은 시기 한화 노시환의 메이저리그 포스팅 협상은 12월 3일 오전 7시에 마감되고, MLB 노사협약도 12월 1일 끝나 직장폐쇄가 되면 KBO 구단들의 외국인 선수 영입도 막힐 수 있어요.",
 "cta": "여러분 팀이 이번 FA에서 꼭 잡아야 할 선수는 누구인가요? 댓글로 남겨 주세요.",
 "prev": PREV,
 "teams": ["삼성", "LG", "KIA", "한화", "두산", "SSG"],
 "players": ["구자욱", "원태인", "박동원", "김태군", "최재훈", "양의지", "홍창기", "최지훈", "김호령", "정수빈", "노시환"],
 "tags": ["2027 FA", "FA 일정", "프로야구 FA", "KBO FA", "FA 공시", "구자욱 FA", "원태인 FA", "구자욱", "원태인", "박동원", "김태군", "최재훈", "양의지", "홍창기", "최지훈", "김호령", "정수빈", "노시환 포스팅", "MLB 직장폐쇄", "스토브리그", "야구자판기"],
 "hashtags": ["#FA", "#스토브리그", "#야구자판기"]}
out = sys.argv[1] if len(sys.argv) > 1 else 'episodes/2026-11-11_롱폼컷1.json'
json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
tot = sum(len(l['narr'].replace(' / ', ' ')) for l in lines[:-1])
print('ok', out, len(lines), '줄 합성 글자', tot)
for l in lines: print(l['narr'])
