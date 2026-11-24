# -*- coding: utf-8 -*-
"""11/23 롱폼 「기아 스토브리그 중간 점검」 — 스포츠 중계 플랫(EP.sb), 목소리 A.
대사 = kia23/script_final.txt (사용자 11/23 14:17 확정). 근거 = claude/기아중간점검-대본확정-1123.md
실행: python3 gen_1123_kia.py → episodes/2026-11-23_롱폼.json"""
import json, os, re, sys, io, copy
sys.path.insert(0, '/home/claude/fa13'); sys.path.insert(0, '/home/claude/fa17')
from helpers_1113 import wrap2
import helpers_1113 as _H
from tight import tight
HERE = os.path.dirname(os.path.abspath(__file__))
SEC, GAPS = [], {}
n = 0
for l in io.open(os.path.join(HERE, 'script_final.txt'), encoding='utf-8'):
    l = l.strip()
    if not l: continue
    if l.startswith('## '): SEC.append([l[3:], []])
    elif l.startswith('⏸'): GAPS[n - 1] = float(l[1:])
    else: SEC[-1][1].append(l); n += 1
ALL = [x for _, ls in SEC for x in ls]
NL = len(ALL)
# ── 자막(숫자·영문으로) ──
REP = [('이십삼년과 이십사년에는', '23년과 24년에는'), ('이십육년', '26년'), ('이십칠년', '27년'),
       ('십일월 이십삼일', '11월 23일'), ('십일월 이십사일', '11월 24일'), ('십일월 이십오일', '11월 25일'), ('십일월 이십일', '11월 20일'), ('십이월 이일', '12월 2일'),
       ('에스에스지', 'SSG'), ('에프에이', 'FA'), ('엘지', 'LG'), ('엔씨', 'NC'), ('플랜 비', '플랜 B'), ('에이등급', 'A등급'),
       ('백칠십억원짜리', '170억 원짜리'), ('십일 년 삼백칠억 원', '11년 307억 원'), ('이십팔억 원쯤', '28억 원쯤'), ('사십억 원대', '40억 원대'), ('사 년 총액 육십칠억 원', '4년 총액 67억 원'),
       ('서른다섯 살', '35살'), ('오십억 원', '50억 원'), ('삼 년 계약', '3년 계약'), ('사 년 사십팔억 원', '4년 48억 원'), ('스물세 살', '23살'), ('이십억 원 미만', '20억 원 미만'),
       ('백팔십삼 이닝', '183이닝'), ('백삼십삼 이닝', '133이닝'), ('이쩜팔삼', '2.83'), ('사쩜칠공이었기', '4.70이었기'),
       ('타율 이할 삼푼 구리', '타율 2할 3푼 9리'), ('이할 삼푼대', '2할 3푼대'), ('삼할 칠푼 팔리', '3할 7푼 8리'), ('리그 십칠위', '리그 17위'), ('일 번 타순', '1번 타순'), ('일 번 타자', '1번 타자'),
       ('타율 삼할 삼푼', '타율 3할 3푼'), ('오십구억 오천만 원쯤', '59억 5천만 원쯤'), ('사백이십만 달러', '420만 달러'), ('사백육십만 달러', '460만 달러'), ('사십만 달러', '40만 달러'),
       ('계약한 네 명이', '계약한 4명이'), ('세 명', '3명'), ('한 명을 더', '1명을 더'),
       ('분석때문', '분석 때문'), ('네일.. 올러.. 카스트로를', '네일, 올러, 카스트로를'),   # 11/23 23:01 사용자 "네일올러/카스트로를 → 네일/올러/카스트로를": 읽는 글에만 '..'(짧은 쉼), 자막은 그대로
        ('있는걸로', '있는 걸로'), ('필요로하는', '필요로 하는'), ('뺏길것', '뺏길 것'), ('봤을때는', '봤을 때는'), ('박정우같은', '박정우 같은'), ('얻고있어요', '얻고 있어요')]
REP.sort(key=lambda x: -len(x[0]))
def _punct(t): t = re.sub(r'(?<!\d),|,(?!\d)', '', t); return re.sub(r'\.(?=$|\n)', '', t)
WRAPFIX = {'한 해에\n28억 원쯤 여유가 생기는데요': '한 해에 28억 원쯤\n여유가 생기는데요', '처음 이름이\n나온 곳은 롯데예요': '처음 이름이 나온 곳은\n롯데예요', '생각보다 많이\n불렀다는 반응도 있어요': '생각보다 많이 불렀다는\n반응도 있어요',
           '26년에도 시즌\n막판으로 갈수록': '26년에도\n시즌 막판으로 갈수록', '구단이 손을\n뗀 거냐는 말도 있어요': '구단이 손을 뗀 거냐는\n말도 있어요',
           '기아가 더 올려\n주지 않는 상황에서': '기아가 더 올려 주지 않는\n상황에서', '놓쳐도 지금 있는\n포수들로 가겠다고 했어요': '놓쳐도 지금 있는 포수들로\n가겠다고 했어요',
           '김태군과\n던졌을 때 평균자책점은': '김태군과 던졌을 때\n평균자책점은', '홍창기가\n올 게 유력하다는 글이': '홍창기가 올 게\n유력하다는 글이', '먼저 높게\n부른 건 잘한 일이고': '먼저 높게 부른 건\n잘한 일이고', '미리 매듭짓지\n못한 게 아쉬워요': '미리 매듭짓지 못한 게\n아쉬워요',
           '타율\n2할 3푼 9리·홈런 없이': '타율 2할 3푼 9리\n홈런 없이', '주전이\n된 뒤 가장 부진했는데요': '주전이 된 뒤\n가장 부진했는데요',
           '기아가 관심이 있다는 구단\n쪽 말도': '기아가 관심이 있다는\n구단 쪽 말도'}   # 11/23 규칙 검수: 자막이 뜻 덩어리 가운데서 꺾인 곳
def SUBTXT(nr):
    pcs = []
    for p in re.split(r' /\+? ', nr):
        p = p.strip()
        for a, b in REP: p = p.replace(a, b)
        p = p.replace('아까, ', '아까 ')   # 읽기용 쉼표(자막엔 안 씀)
        p = p.replace('아까말했다시피', '아까 말했다시피')   # 11/24 10:08 사용자: 65번 줄은 '아까말했다시피/+김호령이 떠나면'(붙여서 한 덩이로 읽기) — 자막만 띄어 씀
        p = re.sub(r'(?<=[가-힣]), (?=[가-힣])', '·', p)   # 이름 나열은 가운뎃점(자막에 쉼표 ✗)
        pcs.append(re.sub(r' +', ' ', _punct(p)).strip())
    return pcs
# ── 색(팀 색을 채도·밝기 낮춰서) ──
TCOL = {'기아': ('#7C2230', '#64192A'), '한화': ('#8F4A1E', '#763C17'), '롯데': ('#1F3352', '#182842'), 'SSG': ('#7A2420', '#621B18'), '두산': ('#262A52', '#1C1F40'),
        'NC': ('#2B4A73', '#213B5D'), 'LG': ('#7A1F45', '#621737'), '중립': ('#1E3B36', '#173029')}
# ── 사진(PC 선수이미지 폴더 기준 이름) ──
P = {'김호령': '경기/김호령_만루포_0821_KIA제공_세로', '김태군': '경기/김태군_덕아웃_0729_KIA제공', '한준수': '경기/한준수_주루_KIA제공', '황성빈': '경기/황성빈_도루_0715_OSEN',
     '노시환': '경기/노시환_손하트_1010_한화제공', '노시환2': '경기/노시환_타격_세로_뉴시스',   # 두 사람 카드엔 몸까지 보이는 사진(11/23 검수: 손하트 사진은 세로 칸에서 얼굴만 참)
      '홍창기': '경기/홍창기_상체_0921_LG제공', '차명석': '인물/차명석_스포츠서울', '이범호': '경기/이범호_박수_0915_KIA제공_세로',
     '정수빈': '경기/정수빈_타격_1004_두산제공', '최지훈': '경기/최지훈_타격_0920_SSG제공', '양의지': '경기/양의지_FA계약_1117_두산제공', '박동원': '경기/박동원_세리머니_LG제공',
     '네일': '경기/네일_주먹환호_KIA제공', '올러': '경기/올러_포효_0929_KIA제공', '카스트로': '경기/카스트로_홈런세리머니_1010_KIA제공',
     '유강남': 'KBO프로필/유강남', '노진혁': 'KBO프로필/노진혁', '한현희': 'KBO프로필/한현희'}
# 새로 받을 사진: 임지열 타케다 김민규 박정우 (받으면 photos_new.json 에 파일 이름)
_pn = os.path.join(HERE, 'photos_new.json')
P.update(json.load(io.open(_pn, encoding='utf-8')) if os.path.exists(_pn) else {})
def ph(k): return P.get(k)
# 카드 줄 사진의 얼굴 자리: [얼굴 가운데 x, y, 머리 높이, 머리가 칸에서 차지할 몫]
_fc = os.path.join(HERE, 'fc.json')
FC = json.load(io.open(_fc, encoding='utf-8')) if os.path.exists(_fc) else {}
# ── 장면 도구 ──
def T(l, v, at=0, hl=False, c=None, **k):
    d = dict(l=l, v=v, at=at, **k)
    if hl: d['hl'] = True
    if c: d['c'] = c
    return d
def CARD(who, team, eb, name, tiles=(), band=None, **k):
    s = dict(type='sb_card', img=ph(who), team=team, eb=eb, name=name, tiles=list(tiles), **k)
    if band: s['band'] = dict(t=band[0], at=band[1])
    return s
def QUOTE(who, team, eb, name, text, at=1, **k): return dict(type='sb_quote', img=ph(who), team=team, eb=eb, name=name, text=text, at=at, **k)
def R(who, slot, name, val=None, st=None, sc='w', at=0, team=None, **k):
    d = dict(img=ph(who) if who else None, slot=slot, name=name, at=at, **k)
    if d['img'] in FC: d['fc'] = FC[d['img']]
    if val: d['val'] = val
    if st: d['st'] = st; d['sc'] = sc
    if team: d['team'] = team
    return d
def CARDS(key, title, sub, cards, **k): return dict(type='sb_cards', key=key, chain=key, title=title, sub=sub, cards=list(cards), **k)
def BIG(key, sub, title, items, **k): return dict(type='sb_big', key=key, chain=key, sub=sub, title=title, items=list(items), **k)
def QQ(text, logos=(), key=None, ats=None, hl=(), logoAt=0, **k):
    s = dict(type='sb_q', text=text, logos=list(logos), ats=ats or [0] * (text.count('\n') + 1), hl=list(hl), logoAt=logoAt, **k)
    if key: s['key'] = key; s['chain'] = key
    return s
def I(l, big, at=0, **k): return dict(l=l, big=big, at=at, **k)
Y, W_, G, RD = 'y', 'w', 'g', 'r'
KH = ('김호령', 'KIA', 'FA · 중견수', '김호령')
KT = ('김태군', 'KIA', 'FA · 포수', '김태군')
NS = ('노시환', '한화', '한화 · 내야수', '노시환')
HC = ('홍창기', 'LG', 'LG · 외야수 · FA', '홍창기')
SC = [
 # 사용자 11/23 16:19 "처음 이름이 나온 팀 이런 건 나레이션에서 다 설명하니까 넣을 필요 없어 — 그냥 롯데만 크게. 불필요한 서브텍스트는 앞으로 넣지 마"
 #  → 칸의 작은 글(l)은 숫자가 무엇인지 가릴 때만. 나머지는 핵심 말 하나만 크게.
 # ── 오프닝 1~5
 BIG('op1', '', '기아가 발표한 계약', [I('', '0건', 0, logo='KIA', bigAt=4)], instant=True),
 QQ('기아 프론트는\n잘하고 있을까요?', ['KIA'], key='opq', ats=[0, 0], hl=[1], logoSize=240),
 QQ('지금\n어디까지 진행됐을까요?', ['KIA'], key='opq', ats=[0, 0], hl=[1], logoSize=240),
 BIG('op4', '', 'FA 시장', [I('계약', '4명', 1), I('잔류', '4명', 2), I('이적', '0명', 3, bigAt=4)], instant=True),   # 구독 영상 뒤 첫 화면 — 사선 띠가 지나가면 제목이 이미 있어야 한다
 BIG('toc', '', '정리할 것', [I('김호령·김태군을 노리는 팀', '1', 0), I('두 선수는 정말 떠날까?', '2', 1), I('기아가 데려올 선수', '3', 2)], stack=True),
 # ── 김호령을 노리는 팀 6~15
 CARD(*KH, [T('', '롯데', 1, True)]),
 CARDS('lt1', '롯데 외야 구상', '', [R('황성빈', '코너 외야', '황성빈', at=0), R('김호령', '중견수', '김호령', val='센터라인 강화', at=0, valAt=2)], tk='롯데'),
 BIG('lt2', '', '롯데 FA 계약 종료', [I('유강남 · 노진혁 · 한현희', '170억 원', 1, logo='롯데', bigAt=2)], tk='롯데'),
 CARD('임지열', '롯데', '롯데 · 외야수', '임지열', [T('', '트레이드 영입', 1, True), T('마무리캠프 테스트', '타케다 아이토', 3)], tk='롯데'),
 BIG('lt4', '', '김호령 영입전', [I('', '뛰어들 가능성 높지 않다', 0, logo='롯데', name='롯데', bigAt=3)], tk='롯데'),
 BIG('hh1', '', '주전 중견수가 없는 팀', [I('', '김호령이 필요하다', 0, logo='한화', name='한화', bigAt=2)], tk='한화'),
 CARD(*NS, [T('11년', '307억 원', 1, True)], band=('외부 FA 여유 없음', 2), tk='한화'),
 CARD(*NS, [T('11년', '307억 원', -1, True), T('포스팅 마감', '12월 2일', 2), T('미국행이면 한 해', '약 28억 원', 4, True)], tk='한화'),
 CARD(*NS, [T('11년', '307억 원', -1, True), T('포스팅 마감', '12월 2일', -1), T('미국행이면 한 해', '약 28억 원', -1, True)], band=('결과가 나와야 움직인다', 1), tk='한화'),
 BIG('ncw', '', '중견수가 필요한 다른 팀', [I('', '확실한 중견수 없음', 0, logo='NC', name='NC', bigAt=1), I('', '나설지는 미지수', 4, logo='키움', name='키움', bigAt=5)], tk='중립'),
 # ── 기아의 제안 16~23
 CARD(*KH, [T('', '먼저 높은 조건', 2, True)]),
 CARD(*KH, [T('', '먼저 높은 조건', -1, True), T('', '시즌 뒤 다시 제안', 1)]),
 BIG('ev', '', '업계 반응', [I('업계', '"합리적"', 1), I('다른 반응', '"많이 불렀다"', 2)]),
 BIG('val', '언론 · 팬 커뮤니티', '김호령 몸값', [I('예상', '40억 원대', 0, bigAt=2)]),
 CARDS('cmp', '같은 중견수', '', [R('김호령', '', '김호령', val='40억 원대', at=0), R('최지훈', '', '최지훈', val='4년 67억 원', at=1, valAt=2)]),
 CARDS('cmp', '같은 중견수', '', [R('김호령', '', '김호령', val='2027년 35살', st='풀타임 주전 한 해', at=-1, valAt=1, stAt=3), R('최지훈', '', '최지훈', val='4년 67억 원', at=-1)]),
 CARDS('cmp', '같은 중견수', '', [R('김호령', '', '김호령', val='막판 타격 하락', st='최지훈만큼은 어렵다', sc='y', at=-1, valAt=1, stAt=2), R('최지훈', '', '최지훈', val='4년 67억 원', at=-1)]),
 CARDS('cmp', '기아 플랜 B', '', [R('김호령', '', '김호령', val='50억 원까지 오르면', at=-1, valAt=1), R('정수빈', '', '정수빈', val='후보', at=5, valAt=6)]),
 # ── 팬 반응 24~27
 QQ('팬 반응도\n팀마다 갈려요', ['KIA', '롯데', '한화'], ats=[0, 0], hl=[1], logoSize=240),
 BIG('fan', '기아 팬 커뮤니티', '김호령', [I('', '"놓치면 야구 안 본다"', 1, bigAt=1), I('', '"3년 계약이 맞다"', 3), I('', '"다른 구단 4년 48억 원이면 손해"', 4, bigAt=5)], stack=True),
 BIG('fan', '롯데 팬 커뮤니티', '김호령', [I('', '"그냥 사자"', 1), I('', '"왜 사느냐"', 2), I('', '"구단이 손을 뗀 거냐"', 4)], stack=True, tk='롯데'),
 BIG('fan', '한화 팬 커뮤니티', '김호령', [I('', '"다른 팀에 뺏길 것 같다"', 1, bigAt=1), I('', '"데려와도 쓰기 어렵다"', 3, bigAt=4)], stack=True, tk='한화'),
 # ── 김호령은 떠날까 28~38
 CARD(*KH, [T('', '정말 떠날까?', 1, True)]),
 BIG('jd', '', '김호령 전망', [I('지금은', '기아가 유리', 1), I('늦어질수록', '떠날 가능성 커진다', 2, bigAt=3)]),
 BIG('adv', '', '기아가 유리한 이유', [I('', '다른 팀은 더 써야 한다', 1, logo='KIA', bigAt=3)]),
 BIG('adv', '', '기아가 유리한 이유', [I('', '외야수를 채우는 중', 0, logo='롯데', name='롯데'), I('', '노시환 결과 대기', 1, logo='한화', name='한화', bigAt=2)], tk='중립'),
 CARD(*KH, [T('', '일주일 넘게 미계약', 2, True)]),
 CARD(*KH, [T('', '일주일 넘게 미계약', -1, True)], band=('다른 팀 제안을 기다린다', 2)),
 BIG('fk2', '기아 팬 커뮤니티', '김호령', [I('', '"이적 확정"이라는 글', 1)], stack=True),
 CARD('이범호', 'KIA', '기아 감독', '이범호', [T('', '김민규를 더 쓴다', 2, True), T('', '박재현 · 박정우', 5)]),
 BIG('nr', '', '기아의 제안', [I('', '더 올릴 가능성 높지 않다', 1, logo='KIA', bigAt=2)]),
 CARDS('nh', '김호령 변수', '', [R('김호령', '', '김호령', val='기아 제안 그대로', at=0), R('노시환2', '', '노시환', val='미국행이면', st='한화가 영입전에', sc='y', at=2, valAt=3, stAt=5)]),
 CARDS('nh', '한화가 더 부르면', '', [R('김호령', '', '김호령', val='떠날 가능성 높다', at=-1, valAt=1), R('노시환2', '', '노시환', at=-1)]),
 # ── 김태군 39~52
 CARD(*KT, [T('', '어떨까?', 1, True)]),
 CARD(*KT, [T('', '노리는 팀이 안 나왔다', 1, True)]),   # 11/23 17:05 사용자가 40·41번을 다시 씀(이름 못 밝히는 구단 줄 삭제)
 CARD(*KT, [T('', '노리는 팀이 안 나왔다', -1, True), T('', '포수가 급한 팀이 없다', 1)]),
 CARD('양의지', '두산', '두산 · 포수', '양의지', [T('', '두산 잔류', 1, True)], tk='두산'),
 CARDS('lgc', 'LG 포수', '', [R('박동원', 'FA', '박동원', at=0), R('차명석', '단장', '차명석', val='"지금 포수들로"', at=1, valAt=2)], tk='LG'),
 BIG('bk', '', '다른 팀 포수', [I('백업 포수', '김민식과 계약 가까움', 0, logo='LG', name='LG', lAt=0, bigAt=1), I('주전 포수', '23살 허인서', 3, logo='한화', name='한화', lAt=4, bigAt=3)], tk='중립'),
 CARD(*KT, [T('', '기아에 남고 싶다', 1, True)]),
 CARD(*KT, [T('기아', '한준수의 백업', 2), T('본인', '주전 포수', 4, True)]),
 CARD(*KT, [T('', '제안 금액 비공개', 1, True)]),
 BIG('fkt', '기아 팬 커뮤니티', '김태군', [I('', '"20억 원 미만"', 1), I('', '"제시액이 너무 적다"', 2), I('', '"둘 다 잡자"', 3)], stack=True),
 CARD(*KT, [T('', '쉽게 놓기 어렵다', 1, True)]),
 CARD(*KT, [T('네일 183이닝 가운데', '133이닝', 1), T('김태군과 평균자책점', '2.83', 3, True), T('한준수와 평균자책점', '4.70', 5)]),
 CARD(*KT, [T('', '남을 가능성 높다', 1, True)]),
 CARD(*KT, [T('', '데려갈 팀 안 나옴', 0), T('', '본인도 남고 싶다', 1), T('', '평가 차이만 남았다', 3, True)]),
 # ── 홍창기 53~65
 QQ('기아가 다른 팀에서\n데려올 선수는?', ['KIA'], ats=[0, 0], hl=[1], logoSize=240),
 CARDS('hc0', '이름이 나오는 외야수', '', [R('정수빈', '두산', '정수빈', at=0), R('홍창기', 'LG', '홍창기', at=2)]),
 CARD(*HC, [T('', '"기아행 유력" 글 인기', 1, True)], tk='LG'),
 CARD(*HC, [T('타율', '2할 3푼 9리', 1), T('홈런', '없음', 1), T('주전 이후', '가장 부진', 2, True)], tk='LG'),
 CARD(*HC, [T('타율', '2할 3푼 9리', -1), T('홈런', '없음', -1), T('주전 이후', '가장 부진', -1, True)], band=('이유는 출루', 1), tk='LG'),
 CARD(*HC, [T('타율', '2할 3푼 9리', -1), T('볼넷 비율', '리그 2위', 1), T('출루율', '3할 7푼 8리', 2, True)], band=('리그 17위', 3), tk='LG'),
 CARD(*HC, [T('기아 1번 타순 출루율', '리그 꼴찌', 2, True)], tk='LG'),
 CARD(*HC, [T('', '"1번 타자로 데려오자"', 2, True)], tk='LG'),
 CARD(*HC, [T('23년 · 24년 타율', '3할 3푼 이상', 1), T('', '부활 기대', 2, True)], tk='LG'),
 BIG('fhc', '기아 팬 커뮤니티', '홍창기', [I('', '"데려오자"', 1), I('', '"하락세인데 왜 사느냐"', 2)], stack=True),
 BIG('cap', '한 해 연봉 기준', '기아 샐러리캡', [I('추정', '59억 5천만 원쯤 여유', 0, logo='KIA', bigAt=1)]),
 CARD(*HC, [T('', 'A등급', 0), T('', '보상선수 필요', 2), T('', '기아 구단 발언 없음', 4, True)], tk='LG'),
 CARDS('lnk', '김호령 계약과 홍창기', '', [R('김호령', '', '김호령', val='떠나면?', at=0, valAt=1), R('홍창기', '', '홍창기', val='달라질 수 있다', at=5, valAt=5)]),
 # ── 외국인 66~71
 QQ('FA 말고도\n남은 계약', ['KIA'], ats=[0, 0], hl=[1], logoSize=240),
 CARDS('fx', '재계약 발표 없음', '', [R('네일', '', '네일', at=0), R('올러', '', '올러', at=0), R('카스트로', '', '카스트로', at=0)]),
 CARDS('fx', '2026년에 받은 돈', '', [R('네일', '', '네일', at=-1), R('올러', '', '올러', at=-1), R('카스트로', '', '카스트로', at=-1)], big=dict(t='420만 달러', at=3)),
 BIG('fcap', '', '외국인 한도', [I('쓸 수 있는 돈', '460만 달러', 0, bigAt=2), I('올려 줄 수 있는 폭', '40만 달러', 3, bigAt=4)]),
 BIG('cal', '', '남은 일정', [I('재계약할 선수 결정', '11월 25일까지', 0, lAt=1)], stack=True),
 CARD('올러', 'KIA', '기아 · 투수', '올러', [T('', '몸값 인상', 1, True)], band=('남은 40만 달러', 2)),
 # ── 정리 72~79
 BIG('s1', '', '김호령 협상', [I('', '다른 팀이 끼어들기 어렵다', 1, logo='KIA', bigAt=3)]),
 CARDS('s2', '김호령 변수', '', [R('김호령', '', '김호령', val='미계약', at=0), R('노시환2', '', '노시환', val='12월 2일 결과', at=1)]),
 BIG('s3', '', '남은 계약', [I('김태군', '남을 가능성 높다', 0, bigAt=2), I('외국인 3명', '40만 달러 안에서', 3, bigAt=4)]),
 BIG('s4', '', '기아 프론트', [I('김호령에게 먼저 높게 부른 것', '잘한 일', 1, bigAt=2), I('김태군과 시즌 중에 못 끝낸 것', '아쉽다', 3, bigAt=4)]),
 CARDS('q', '잡을 수 있을까?', '', [R('김호령', '', '김호령', at=0), R('김태군', '', '김태군', at=0)]),
 CARDS('q', '다른 팀에게 뺏길까?', '', [R('김호령', '', '김호령', at=-1), R('김태군', '', '김태군', at=-1)]),
 QQ('여러분은\n어떻게 보세요?', ['KIA'], key='endq', hl=[1], logoSize=240),   # 11/23 23:04 사용자 "기아 로고 같은 장면인데 다시 뜬다 · 로고 너무 작다": 두 장면을 같은 key 로(로고 그대로), 로고 240
 QQ('계약이 발표되면 바로 정리해 드릴게요\n채널 구독하고\n기아 소식 받아보세요', ['KIA'], key='endq', ats=[0, 2, 2], hl=[1, 2], logoSize=240),
]
exec(io.open(os.path.join(HERE, 'boards_1123.py'), encoding='utf-8').read())   # 11/23 23:20 화면 구성 다시 짜기(한 단락 = 한 판) — 위 SC 는 옛 구성(참고용)
assert len(SC) == NL, (len(SC), NL)
CHT = {'오프닝': '기아 프론트는 잘하고 있을까', '김호령을 노리는 팀': '김호령을 노리는 팀', '기아의 제안': '기아가 내민 조건과 몸값', '팬 반응': '김호령을 보는 팬 반응',
       '김호령은 떠날까': '김호령은 정말 떠날까', '김태군': '김태군을 노리는 팀이 안 나오는 이유', '홍창기': '홍창기 이름이 나오는 이유', '외국인': '외국인 3명 재계약', '정리': '기아 프론트 평가'}
CHS = {'오프닝': '중간 점검', '김호령을 노리는 팀': '노리는 팀', '기아의 제안': '기아의 제안', '팬 반응': '팬 반응', '김호령은 떠날까': '떠날까?'}
lines, scenes, CH = [], [], []
# 11/23 22:53 사용자: "아까말했다/시피노시환이 이렇게 텀 두고 말해 → 아까말했다시피/노시환이 이렇게 해야 돼" — 이 자리는 자동으로 붙여 읽지 않고 쉰다
NOTIGHT = [('아까, 말했다시피 / +노시환이', '아까, 말했다시피 / 노시환이')]   # 37번 줄은 11/23 22:53 대로 '말했다시피' 뒤에서 쉼 · 11/24 02:21 사용자 "아까/말했다시피 라고 해야 한다 — 왜 자꾸 아까말했다/시피" · 02:26 65번 줄은 전부 /+ → 아까 뒤에 쉼표(아까, 말했다시피), 뒤는 대본 표시대로
# 11/23 줄 사이 쉼(사용자): 22:11 "보통 0.37초·가장 긴 곳 0.45초" → 22:52 "마침표가 들어간 대사 다음은 텀이 살짝 길어도" · 22:50 "기아 팬·롯데 팬·한화 팬 커뮤니티 같은 큰 단락을 넘어갈 땐 조금 길어도"
#   말이 이어지는 줄(~는데·~고·~서) 뒤 = 그대로(gapScale 0.5 → 0.16 + 말끝 여운 0.21 = 0.37초) / 문장이 끝나는 줄 뒤 = 0.24(→ 0.45초) / 큰 단락(장·팀이 바뀜) 앞 = 0.40(→ 0.6초)
GAP_SENT, GAP_PARA = 0.24, 0.40
SENT_FIN = re.compile(r'(요|죠|다|\?)$')
i = 0
for name, ls in SEC:
    CH.append({"key": name, "title": CHT[name], "short": CHS.get(name, name), "from": i, "to": i + len(ls) - 1})
    for nr in ls:
        narr = tight(nr.replace(' /+ ', ' / +'))
        for a_, b_ in NOTIGHT: narr = narr.replace(a_, b_)
        pcs = SUBTXT(nr)
        assert len(pcs) == len(narr.split(' / ')), nr
        l = {"narr": narr, "sub": "|".join(WRAPFIX.get(wrap2(p), wrap2(p)) for p in pcs)}
        if i in GAPS: l['gapAfter'] = GAPS[i]
        elif i < NL - 1:
            fin = bool(SENT_FIN.search(nr.strip().rstrip('.'))); lead = nr.strip().endswith('데요')   # '~데요'로 끝나면 다음 줄로 이어지는 말머리라 큰 단락으로 안 본다
            nx = ALL[i + 1]
            para = (nr is ls[-1]) or (fin and not lead and ('팬 커뮤니티' in nx[:12] or re.match(r'(한화|롯데|엔씨|키움|두산|엘지|삼성|케이티|에스에스지)[는도와]', nx)))
            if para: l['gapAfter'] = GAP_PARA
            elif fin: l['gapAfter'] = GAP_SENT
        lines.append(l)
        s2 = copy.deepcopy(SC[i]); s2['startLine'] = i; s2['tc'], s2['tc2'] = TCOL[s2.pop('tk', '기아')]; s2['noCenter'] = True
        nb = len(pcs)
        def chk(o):
            if isinstance(o, dict):
                for k_, v_ in o.items():
                    if k_.endswith('At') or k_ == 'at' or k_ == 'ats':
                        for vv in (v_ if isinstance(v_, list) else [v_]):
                            if isinstance(vv, (int, float)) and 0 <= vv < 50: assert vv < nb, (i + 1, k_, vv, nb, nr)
                    else: chk(v_)
            elif isinstance(o, list):
                for v_ in o: chk(v_)
        chk(s2)
        if scenes and scenes[-1].get('chain') and scenes[-1].get('chain') == s2.get('chain') and scenes[-1]['type'] == s2['type']: s2['cont'] = True
        scenes.append(s2); i += 1
# 같은 사람 카드에서 같은 기록 칸이 다음 장면까지 이어질 때, 칸 수가 늘어도 크기가 안 바뀌게 가장 많은 칸 수에 맞춘다
def _tk(s): return {t_['l'] + '|' + t_['v'] for t_ in (s.get('tiles') or [])}
_j = 0
while _j < len(scenes):
    _k = _j
    while (_k + 1 < len(scenes) and scenes[_k]['type'] == 'sb_card' and scenes[_k + 1]['type'] == 'sb_card' and all(scenes[_k + 1].get(x) == scenes[_k].get(x) for x in ('img', 'name', 'team'))
           and _tk(scenes[_k]) & _tk(scenes[_k + 1])): _k += 1
    if _k > _j:
        _ns = [len(scenes[x].get('tiles') or []) for x in range(_j, _k + 1)]
        if len(set(_ns)) > 1:
            for x in range(_j, _k + 1): scenes[x]['tn'] = max(_ns)
            print('tn', _j + 1, _k + 1, scenes[_j]['name'], _ns)
    _j = _k + 1
TITLE = "김호령, 기아 떠날까? | 기아 스토브리그 중간 점검"
DESC = ("FA 협상이 시작되고 일주일, 기아가 발표한 계약은 아직 없어요. 김호령과 김태군을 노리는 팀이 어디인지, 왜 노리는지, 팬들은 어떻게 보는지, 두 선수가 정말 기아를 떠날지 정리했어요.\n"
        "김호령: 롯데(임지열 트레이드·타케다 아이토 테스트로 외야 보강 중), 한화(노시환 포스팅 결과가 나와야 움직일 수 있음, 마감 12월 2일), NC·키움. 기아는 시즌 뒤 조건을 올려 다시 제안했고, 언론과 팬 커뮤니티에서는 몸값을 40억 원대로 봐요.\n"
        "김태군: 노리는 팀이 아직 나오지 않았고, 본인은 기아에 남고 싶다는 뜻을 밝혔어요.\n"
        "홍창기: 2026년 타율 2할 3푼 9리로 부진했지만 출루율 3할 7푼 8리. 기아 1번 타순 출루율이 리그 꼴찌라 팬들 사이에서 이름이 나와요.\n"
        "외국인: 네일·올러·카스트로 2026 몸값 합계 420만 달러, 세 명을 다 잡으면 2027 한도 460만 달러. 구단은 11월 25일까지 재계약할 선수를 정해야 해요.\n"
        "영상 내용은 2026년 11월 24일 기준이고, 전망은 제 판단이에요.")
EP = {"theme": "mg", "sb": True, "date": "2026-11-23", "gameDate": "2026-11-23", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0,
      "ttsApi": True, "ttsVoice": "A", "ttsWhole": False, "ttsTempo": 1.2, "ttsTempoSlow": 1.15, "rev": "1123-kia-v1", "topic": "기아스토브리그중간점검", "endcardSec": 12,
      "voiceRemap": [None] * 41 + [j + 1 for j in range(41, NL)],   # 11/23 17:05 옛 41번 줄을 빼서 뒤 줄 번호가 하나씩 당겨짐 → 옛 음성 재사용
      "insertClip": {"file": "구독영상_1124b.mp4",   # 11/24 13:43 사용자 구간별 배속(동전 1·레일 1.2·배트 2.3·버튼 1.5·기계 1.7·캔 1.2·마지막 1, 12.6초판)
                    "afterLine": 3, "vol": 0.9, "outHold": 0.7, "outWipe": 0.5},   # 11/23 22:43 사용자: "지금 어디까지 진행됐을까요? 다음에 나오는 게 나을 것 같아" · 22:42 "본 영상으로 넘어갈 때는 페이드 말고 다른 걸로 — 구독이 보이고 나서 너무 바로 넘어가"   # 11/23 오프닝 뒤 구독 유도 영상(시스템\\clips\\ 에 파일이 있을 때만 끼움)
      "gapScale": 0.5,   # 11/23 22:11 사용자 "보통을 0.37초로 하고 가장 긴 곳을 0.45초로" → 줄 사이 쉼 0.5배(장면 바뀜 0.16 + 말끝 여운 0.21 = 0.37, 화제 전환 0.19 + 0.21 = 0.40)
       "pauseMax": 0.45, "sentPauseMin": 0.4, "clausePauseMin": 0.3, "ttsCharsOk": 7000, "totalSec": 481,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False,
      "source": "대사 kia23/script_final.txt · 근거 = claude/기아중간점검-대본확정-1123.md",
      "youtube": {"title": TITLE, "description": DESC, "cta": "기아는 김호령과 김태군을 잡을 수 있을까요? 아니면 다른 팀에게 뺏길까요? 여러분은 어떻게 보세요?", "prev": "10개 구단 외국인 현황",
                  "tags": ["기아 타이거즈", "KIA", "김호령", "김태군", "홍창기", "노시환", "FA", "스토브리그", "기아 FA", "김호령 FA", "네일", "올러", "카스트로", "프로야구", "KBO"],
                  "hashtags": ["#기아타이거즈", "#김호령", "#김태군", "#스토브리그", "#KBO"],
                  "teams": ["기아 타이거즈", "롯데 자이언츠", "한화 이글스", "LG 트윈스", "두산 베어스", "NC 다이노스", "키움 히어로즈", "SSG 랜더스"],
                  "players": ["김호령", "김태군", "홍창기", "노시환", "황성빈", "유강남", "노진혁", "한현희", "임지열", "타케다 아이토", "최지훈", "정수빈", "양의지", "박동원", "김민식", "허인서", "최재훈", "한준수", "김민규", "박재현", "박정우", "네일", "올러", "카스트로"]}}
if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'episodes'), exist_ok=True)
    out = os.path.join(HERE, 'episodes', '2026-11-23_롱폼.json')
    for _ln in EP['lines']:   # 11/24 10:23 사용자: 37번 줄 '아까 말했다시피'와 '노시환이' 사이 텀 살짝만 줄여(0.44초 → 0.3초, 다시 합성 없음)
        if _ln['narr'].startswith('기아가 더 올려 주지 않는 상황에서 / 아까, 말했다시피 / 노시환이'): _ln['pauseMax'] = 0.3
    assert sum('pauseMax' in _ln for _ln in EP['lines']) == 1
    json.dump(EP, io.open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for l in lines)
    print('ok', out, len(lines), '줄', len(scenes), '장면', '합성 글자', tot)
    if '--subs' in sys.argv:
        for k, l in enumerate(lines): print(k + 1, l['sub'].replace('\n', '⏎'), '|GAP %s' % l['gapAfter'] if 'gapAfter' in l else '')
