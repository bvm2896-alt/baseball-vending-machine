# -*- coding: utf-8 -*-
"""11/21 롱폼 「10개 구단 외국인 현황」 — 스포츠 중계 플랫(EP.sb), 목소리 A(장운).
대사 = fx21/script_v3.txt (사용자 11/21 01:38 확정). 근거 = claude/외국인현황-대본v3-1121.md 확인 표 · claude/외국인-리서치-1121.md
실행: python3 gen_1121_fx.py → episodes/2026-11-21_롱폼.json"""
import json, os, re, sys, io, copy
sys.path.insert(0, '/home/claude/fa13'); sys.path.insert(0, '/home/claude/fa17')
from helpers_1113 import wrap2
import helpers_1113 as _H
from tight import tight
HERE = os.path.dirname(os.path.abspath(__file__))
SEC, GAPS = [], {}
n = 0
for l in io.open(os.path.join(HERE, 'script_v3.txt'), encoding='utf-8'):
    l = l.strip()
    if not l: continue
    if l.startswith('## '): SEC.append([l[3:], []])
    elif l.startswith('⏸'): GAPS[n - 1] = float(l[1:])
    else: SEC[-1][1].append(l); n += 1
ALL = [x for _, ls in SEC for x in ls]
assert len(ALL) == 99, len(ALL)
# ── 자막(숫자·영문으로) ──
REP = [('이천이십육년', '2026년'), ('이천이십칠년', '2027년'), ('이천이십오년', '2025년'), ('십일월 이십오일', '11월 25일'), ('십일월 이십일', '11월 20일'), ('십일월 삼십일', '11월 30일'), ('십이월 이일', '12월 2일'), ('칠월', '7월'),
       ('에스에스지', 'SSG'), ('에스엔에스', 'SNS'), ('케이비오', 'KBO'), ('케이티', 'KT'), ('엘지', 'LG'), ('엔씨', 'NC'),
       ('일 년 이백만 달러', '1년 200만 달러'), ('이 년 총액 삼백십만 달러', '2년 총액 310만 달러'), ('팔십칠만 팔천 달러', '87만 8천 달러'), ('네일 이백만, 올러 백이십만, 카스트로 백만 달러라', '네일 200만 올러 120만 카스트로 100만 달러라'),
       ('사백육십만 달러', '460만 달러'), ('사백이십만 달러', '420만 달러'), ('사백만 달러', '400만 달러'), ('삼백만 달러', '300만 달러'), ('이백만 달러', '200만 달러'), ('백사십만 달러', '140만 달러'), ('백삼십만 달러', '130만 달러'),
       ('백십만 달러', '110만 달러'), ('백만 달러', '100만 달러'), ('팔십만 달러', '80만 달러'), ('사십칠만 달러', '47만 달러'), ('사십만 달러', '40만 달러'), ('삼십만 달러', '30만 달러'), ('이십이만 달러', '22만 달러'), ('이십만 달러', '20만 달러'),
       ('열 개 구단', '10개 구단'), ('열두 경기', '12경기'), ('서른아홉 경기', '39경기'), ('일흔두 경기', '72경기'),
       ('오승 삼패', '5승 3패'), ('십일 승 육패', '11승 6패'), ('구승 이패', '9승 2패'), ('오승 이패', '5승 2패'), ('삼승 일패, 팔 홀드', '3승 1패 8홀드'), ('팔승 일패', '8승 1패'), ('칠승 삼패', '7승 3패'), ('구승 구패', '9승 9패'),
       ('팔승', '8승'), ('십이 승', '12승'), ('십 승', '10승'),
       ('평균자책점 사쩜삼사', '평균자책점 4.34'), ('평균자책점 삼쩜구칠', '평균자책점 3.97'), ('평균자책점 일쩜사사', '평균자책점 1.44'), ('평균자책점 이쩜일삼', '평균자책점 2.13'), ('평균자책점 이쩜육구', '평균자책점 2.69'),
       ('평균자책점 이쩜구오', '평균자책점 2.95'), ('평균자책점 삼쩜팔칠', '평균자책점 3.87'), ('영쩜팔이였는데', '0.82였는데'), ('영쩜팔이였어요', '0.82였어요'), ('사쩜 대', '4점대'),
       ('볼넷 구십일 개', '볼넷 91개'), ('공동 일위', '공동 1위'), ('리그 일위', '리그 1위'), ('정규시즌 일위', '정규시즌 1위'), ('이위였는데', '2위였는데'), ('이위였어요', '2위였어요'), ('이할 사푼', '2할 4푼'),
       ('안타 이백십일 개', '안타 211개'), ('안타 육백 개', '안타 600개'), ('삼 년 동안', '3년 동안'), ('삼 년 연속', '3년 연속'), ('사 년 동안', '4년 동안'), ('이 년 계약', '2년 계약'),
       ('스물여섯 살', '26살'), ('백 홈런', '100홈런'), ('사십사 홈런', '44홈런'), ('백삼십구 타점', '139타점'), ('이십팔 홈런', '28홈런'), ('십삼 홈런', '13홈런'),
       ('백팔십삼 이닝', '183이닝'), ('백칠십팔 이닝', '178이닝'), ('네 시즌', '4시즌'), ('시속 백오십팔 킬로미터', '시속 158킬로미터'),
       ('네 명 가운데', '4명 가운데'), ('두 명이 바뀌어요', '2명이 바뀌어요'), ('외국인 세 명', '외국인 3명'), ('세 명', '3명'), ('투수 두 명', '투수 2명'), ('타자 한 명', '타자 1명'), ('라일리 한 명만', '라일리 1명만')]
REP.sort(key=lambda x: -len(x[0]))
def _punct(t): t = re.sub(r'(?<!\d),|,(?!\d)', '', t); return re.sub(r'\.(?=$|\n)', '', t)
def SUBTXT(nr):
    pcs = []
    for p in re.split(r' /\+? ', nr):
        p = p.strip()
        for a, b in REP: p = p.replace(a, b)
        p = re.sub(r'(?<=[가-힣]), (?=[가-힣])', '·', p)   # 이름 나열은 가운뎃점(자막에 쉼표 ✗)
        pcs.append(re.sub(r' +', ' ', _punct(p)).strip())
    return pcs
_H.WRAP.update({'좋은 투수인 건 틀림없다고 했지만': '좋은 투수인 건\n틀림없다고 했지만', '그래서 8승을 올린 오웬 화이트와': '그래서 8승을 올린\n오웬 화이트와', '아직 계약을 맺은 건 아니라고 했어요': '아직 계약을 맺은 건\n아니라고 했어요', '시즌 때 네일과 올러가 없었으면': '시즌 때\n네일과 올러가 없었으면'})
# ── 색(팀 색을 채도·밝기 낮춰서) ──
TCOL = {'오프닝': ('#1E3B36', '#173029'), '한화': ('#8F4A1E', '#763C17'), '롯데': ('#1F3352', '#182842'), 'SSG': ('#7A2420', '#621B18'), 'KT': ('#3A3D46', '#2D3037'), '두산': ('#262A52', '#1C1F40'),
        'NC': ('#2B4A73', '#213B5D'), '삼성': ('#1F4A80', '#183B68'), '기아': ('#7C2230', '#64192A'), 'LG': ('#7A1F45', '#621737'), '키움': ('#5E2030', '#4A1825'), '정리': ('#1E3B36', '#173029')}
# ── 사진 ──
P = {'오스틴': '경기/오스틴_포효_LG제공', '벡': '경기/벡_계약_1105_LG제공', '염경엽': '경기/염경엽_덕아웃_1014_LG제공', '차명석': '인물/차명석_스포츠서울', '알칸타라': '경기/알칸타라_주먹_키움제공', '데이비슨': '경기/데이비슨_손짓_키움제공',
     '히우라': '경기/히우라_세리머니_키움제공', '왓슨': '경기/왓슨_계약_1111_한화제공_c', '와이스': '경기/와이스_정면_0813_한화제공', '페라자': 'KBO프로필/페라자_2026프로필', '레이예스': '경기/레이예스_211안타_1012_롯데제공',
     '이동욱': '경기/이동욱_취임_1031_롯데제공', '이택근': '경기/이택근_단장_1026_롯데제공', '로드리게스': 'KBO프로필/로드리게스_2026프로필', '비슬리': '경기/비슬리_박수_롯데제공', '스기모토': '경기/스기모토_포효_crop',
     '힐리어드': '경기/힐리어드_포효_KT제공_1280', '대니엘': '경기/대니엘_주먹_KT제공', '라일리': '경기/라일리_포효_NC제공', '후라도': '경기/후라도_박수_삼성제공', '디아즈': '경기/디아즈_만루포세리머니_삼성제공',
     '페덱': '경기/페덱_환호_삼성제공', '이종열': '경기/이종열_단장_삼성', '네일': '경기/네일_주먹환호_KIA제공', '올러': '경기/올러_포효_0929_KIA제공', '카스트로': '경기/카스트로_홈런세리머니_1010_KIA제공',
     '이범호': '경기/이범호_박수_0915_KIA제공_세로', '시라카와': '경기/시라카와_투구_KIA제공'}
# 아직 못 받은 사진(받으면 여기에 파일 이름을 넣는다): 톨허스트 케네디 아빌라 리차드슨 하인즈 에레디아 후쿠타니 유토 숄텐스 화이트 왕옌청 로건 나도현 잭로그 세베리노 벤자민 김원형 타카다 테일러 도다 심재학
P.update(json.load(io.open(os.path.join(HERE, 'photos_new.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'photos_new.json')) else {})
SIL = json.load(io.open(os.path.join(HERE, 'sil.json'), encoding='utf-8'))   # 공개 전 화면에 쓰는 그 선수 실루엣(사용자 11/21 02:57 '빈화면은 실루엣으로')
P.update({'숄텐스?': SIL['숄텐스'], '레이예스?': SIL['레이예스'], '레이예스P': 'KBO프로필/레이예스_롯데', '로드리게스P': 'KBO프로필/로드리게스_2026프로필', '비슬리P': 'KBO프로필/비슬리_2026프로필'})   # 사용자 11/21 03:05 '같이 나오면 둘 다 프로필이거나 둘 다 플레이 사진'
def ph(k): return P.get(k)
# 카드 줄 사진의 얼굴 자리(눈으로 잼): [얼굴 가운데 x, y, 머리 높이(모자 위~턱), 머리가 칸에서 차지할 몫] — 사용자 11/21 03:18 '사진 가운데'
FC = {'경기/왓슨_계약_1111_한화제공_c': [.64, .29, .32], '경기/벡_계약_1105_LG제공': [.515, .515, .35, .5], '경기/리차드슨_계약_1112_SSG제공': [.525, .39, .27, .5],
      '경기/알칸타라_주먹_키움제공': [.65, .19, .27], '경기/데이비슨_손짓_키움제공': [.58, .25, .35], '경기/히우라_세리머니_키움제공': [.655, .28, .32],
      '경기/네일_주먹환호_KIA제공': [.495, .18, .19], '경기/올러_포효_0929_KIA제공': [.57, .21, .24], '경기/유토_0722_뉴스1': [.50, .18, .19],
      '경기/후쿠타니_영입_1119_키움제공_c': [.39, .435, .38]}
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
    if d.get('sil'): d['img2'] = d['sil']   # build.py 는 img·img2 만 사진으로 모은다
    if d['img'] in FC: d['fc'] = FC[d['img']]
    if val: d['val'] = val
    if st: d['st'] = st; d['sc'] = sc
    if team: d['team'] = team
    return d
def BOARD(key, team, title, sub, rows, band=None, wide=False, **k):
    s = dict(type='sb_board', key=key, chain=key, team=team, title=title, sub=sub, rows=list(rows), wide=wide, **k)
    if band: s['band'] = dict(t=band[0], at=band[1])
    return s
def CARDS(key, title, sub, cards, **k): return dict(type='sb_cards', key=key, chain=key, title=title, sub=sub, cards=list(cards), **k)
def CAP(key, sub, title, cap, capLab=None, capAt=0, segs=(), left=None, note=None, band=None, **k):
    s = dict(type='sb_cap', key=key, chain=key, sub=sub, title=title, cap=cap, capLab=capLab, capAt=capAt, segs=list(segs), **k)
    if left: s['left'] = dict(l=left[0], t=left[1], at=left[2])
    if note: s['note'] = dict(t=note[0], at=note[1])
    if band: s['band'] = dict(t=band[0], at=band[1])
    return s
def BIG(key, sub, title, items, **k): return dict(type='sb_big', key=key, chain=key, sub=sub, title=title, items=list(items), **k)
def QQ(text, logos=(), key=None, ats=None, hl=(), logoAt=0, **k):
    s = dict(type='sb_q', text=text, logos=list(logos), ats=ats or [0] * (text.count('\n') + 1), hl=list(hl), logoAt=logoAt, **k)
    if key: s['key'] = key; s['chain'] = key
    return s
ALL10 = ['한화', '롯데', 'SSG', 'KT', '두산', 'NC', '삼성', 'KIA', 'LG', '키움']
Y, W_, G, RD = 'y', 'w', 'g', 'r'
def kia_rows(a=-1, na=-1, sa=-1, sira=50, siraSt=50):
    return [R('네일', '투수', '네일', st='재계약 목표', sc=W_, at=a, nameAt=na, stAt=sa, team='KIA'), R('올러', '투수', '올러', st='재계약 목표', sc=W_, at=a, nameAt=na, stAt=sa, team='KIA'),
            R('카스트로', '타자', '카스트로', st='재계약 목표', sc=W_, at=a, nameAt=na, stAt=sa, team='KIA'), R('시라카와', '아시아쿼터', '시라카와', st='재계약 대상', sc=W_, at=sira, stAt=siraSt, team='KIA')]
def kt_rows(a=-1, s1=50, s2=50):
    return [R('힐리어드', '타자', '힐리어드', at=a), R('대니엘', '투수', '대니엘', at=a), R('로건', '투수', '로건', st='재계약 않는 쪽', sc=RD, at=a, stAt=s2, team='KT'),
            R('스기모토', '아시아쿼터', '스기모토', st='소프트뱅크행', sc=RD, at=a, stAt=s1)]
def ds_rows(a=-1, j=50, jv=50, sv=50, bj=50):
    return [R('잭로그', '투수', '잭로그', val='8승', st='재계약 안 함', sc=RD, at=a, valAt=jv, stAt=j, team='두산'), R('벤자민', '투수', '벤자민', st='더 좋은 투수 찾으면 교체', sc=G, at=a, stAt=bj, team='두산'),
            R('세베리노', '타자', '세베리노', st='재계약 안 함', sc=RD, at=a, stAt=sv, team='두산'), R('타카다', '아시아쿼터', '타카다', at=a, team='두산')]
def nc_rows(a=-1, ry=-1, tx=50, doda=50, dodaSt=50):
    return [R('라일리', '투수', '라일리', st='재계약 추진', sc=W_, at=a, stAt=ry), R('테일러', '투수', '테일러', st='교체 방향', sc=RD, at=a, stAt=tx, team='NC'),
            R('블레인', '타자', '블레인', st='교체 방향', sc=RD, at=a, stAt=tx, team='NC'), R('도다', '아시아쿼터', '도다', st='재계약 추진', sc=W_, at=doda, stAt=dodaSt, team='NC')]
def lg_rows(a=-1, b=-1, ken=50, kenSt=50):
    return [R('오스틴', '타자', '오스틴', val='200만 달러', st='계약', sc=Y, at=b), R('벡', '투수', '벡', val='87만 8천 달러', st='계약', sc=Y, at=b), R(None, '투수', '미정', at=b, team='LG', dim=True),
            R('케네디', '아시아쿼터', '케네디', st='재계약 최우선', sc=W_, at=ken, stAt=kenSt, team='LG')]
def kw_rows(a=-1, n0=-1, n1=-1, sa=-1):
    return [R('알칸타라', '투수', '알칸타라', val='110만 달러', st='재계약', sc=Y, at=a, nameAt=n0, valAt=sa, stAt=sa, team='키움'), R('데이비슨', '타자', '데이비슨', val='110만 달러', st='재계약', sc=Y, at=a, nameAt=n1, valAt=sa, stAt=sa, team='키움'),
            R('히우라', '타자', '히우라', val='80만 달러', st='재계약', sc=Y, at=a, nameAt=n1, valAt=sa, stAt=sa, team='키움')]
SCH = '숄텐스'
SC = [
 # ── 오프닝 1~7
 CARD('오스틴', 'LG', 'LG · 타자 · 재계약', '오스틴', [T('기간', '1년', 1), T('금액', '200만 달러', 1, True)]),
 CARD('아빌라', 'SSG', 'SSG · 투수 · 재계약', '아빌라', [T('기간', '2년', 1), T('총액', '310만 달러', 1, True)]),
 CARDS('opkw', '키움 재계약', '2027 시즌', [R('알칸타라', '투수', '알칸타라', val='110만 달러', at=0, valAt=1), R('데이비슨', '타자', '데이비슨', val='110만 달러', at=0, valAt=1), R('히우라', '타자', '히우라', val='80만 달러', at=2, valAt=2)]),
 CARDS('opnew', '새로 계약한 선수', '2027 시즌 새 외국인 투수', [R('왓슨', '한화', '왓슨', val='100만 달러', at=0, nameAt=50, valAt=50, sil=SIL['왓슨']), R('벡', 'LG', '벡', val='87만 8천 달러', at=0, nameAt=50, valAt=50, sil=SIL['벡']), R('리차드슨', 'SSG', '리차드슨', val='100만 달러', at=0, nameAt=50, valAt=50, sil=SIL['리차드슨'])]),
 CARDS('opnew', '새로 계약한 선수', '2027 시즌 새 외국인 투수', [R('왓슨', '한화', '왓슨', val='100만 달러', at=-1, nameAt=0, valAt=1, sil=SIL['왓슨']), R('벡', 'LG', '벡', val='87만 8천 달러', at=-1, nameAt=2, valAt=3, sil=SIL['벡']), R('리차드슨', 'SSG', '리차드슨', val='100만 달러', at=-1, nameAt=4, valAt=5, sil=SIL['리차드슨'])]),
 QQ('다른 팀 외국인들은\n어떻게 되고 있을까요?', ['롯데', 'KT', '두산', 'NC', '삼성', 'KIA'], ats=[0, 0]),
 QQ('10개 구단\n외국인 현황', ALL10, ats=[0, 0], hl=[1], logoAt=0),
 # ── 한화 8~20
 BOARD('hh', '한화', '한화', '2027 외국인', [R('왓슨', '투수', '왓슨', val='100만 달러', st='계약', sc=Y, at=1), R(None, '투수', '거의 정해짐', at=2, nameAt=4, team='한화')]),
 CARD('와이스', '한화', '전 한화 투수', '와이스', [T('한화 복귀 추진', '무산', 3), T('새 팀', '샌디에이고', 3, True)]),
 CARD('화이트', '한화', '한화 · 투수', '화이트', [T('2026 시즌', '8승', 0), T('재계약', '검토', 1, c='c')]),
 CARD('숄텐스?', '한화', '한화가 찾은 투수', '메이저리그 현역 투수', nameAt=1, chain='rev_sch'),
 CARD(SCH, '한화', '전 탬파베이 · 투수', '제시 숄텐스', sil0=SIL['숄텐스'], img2=SIL['숄텐스'], chain='rev_sch'),
 CARD(SCH, '한화', '전 탬파베이 · 투수', '제시 숄텐스', [T('탬파베이 발표', '11월 20일', 0), T('방출 이유', 'KBO에서 뛸 기회', 1, c='c')]),
 CARD(SCH, '한화', '전 탬파베이 · 투수', '제시 숄텐스', [T('2026 메이저리그', '12경기', 1), T('승패', '5승 3패', 2), T('평균자책점', '4.34', 3, True)]),
 CARD(SCH, '한화', '전 탬파베이 · 투수', '제시 숄텐스', [T('행선지로 전해진 팀', '한화', 0, True), T('남았다는 절차', '메디컬 테스트', 1, c='c')], band=('한화 공식 발표는 아직', 3)),
 CARD('페라자', '한화', '한화 · 타자', '페라자', [T('2027 시즌', '새 타자 전망', 2)], nameAt=1),
 CARD('페라자', '한화', '한화 · 타자', '페라자', [T('볼넷', '91개', 0), T('볼넷 순위', '공동 1위', 1), T('후반기 타율', '2할 4푼', 3, True)]),
 QUOTE(None, '한화', '한화', '구단 관계자', '노시환의 포스팅도 있어서 외국인 시장을 계속 살피고 있다', at=1),
 CARD('왕옌청', '한화', '한화 · 아시아쿼터 · 투수', '왕옌청', [T('2026 시즌', '11승 6패', 1), T('평균자책점', '3.97', 2), T('재계약', '30만 달러', 3, True)]),
 # ── 롯데 21~29
 BOARD('lt', '롯데', '롯데', '2027 외국인', [R(None, '타자', '협상 막바지', at=1, nameAt=2, team='롯데'), R('로드리게스P', '투수', '로드리게스', at=1, team='롯데'), R('비슬리P', '투수', '비슬리', at=1, team='롯데')], profile=True),
 CARD('레이예스?', '롯데', '롯데 · 타자', '', [T('2026 안타', '211개', 1, True), T('한 시즌 최다 안타', '신기록', 2, c='c')], chain='rev_rey'),
 CARD('레이예스', '롯데', '롯데 · 타자', '빅터 레이예스', [T('2026 안타', '211개', -1, True), T('한 시즌 최다 안타', '신기록', -1, c='c')], sil0=SIL['레이예스'], img2=SIL['레이예스'], chain='rev_rey'),
 CARD('레이예스', '롯데', '롯데 · 타자', '빅터 레이예스', [T('3년 동안 안타', '600개', 1), T('안타왕', '3년 연속', 2, c='c')]),
 QUOTE('이동욱', '롯데', '롯데 감독', '이동욱', '재계약을 안 하면 안 되는 상황', at=1),
 CARD('레이예스', '롯데', '롯데 · 타자', '빅터 레이예스', [T('2026 몸값', '140만 달러', 1), T('오스틴 (LG)', '200만 달러', 2, c='c')], band=('오스틴을 넘을까?', 3)),
 BOARD('lt', '롯데', '롯데', '2027 외국인', [R('레이예스P', '타자', '레이예스', st='협상 막바지', sc=W_, at=-1), R('로드리게스P', '투수', '로드리게스', st='미정', sc=G, at=-1, stAt=1), R('비슬리P', '투수', '비슬리', st='미정', sc=G, at=-1, stAt=1)], profile=True),
 CARDS('lt2', '롯데 투수 두 명', '2026 성적', [R('로드리게스P', '', '로드리게스', val='10승', st='평균자책점 4.28', sc=G, at=0, valAt=1, stAt=3), R('비슬리P', '', '비슬리', val='10승', st='평균자책점 4.96', sc=G, at=0, valAt=1, stAt=3)], profile=True),
 QUOTE('이택근', '롯데', '롯데 단장', '이택근', '두 선수 모두 좋은 투수인 건 틀림없다', at=1, band=dict(t='재계약은 아직 미정', at=4)),
 # ── SSG 30~36
 CARD('하인즈', 'SSG', '볼티모어 · 외야수', '리스 하인즈', [T('SSG와', '협상 중', 2, True)], nameAt=1),
 CARD('하인즈', 'SSG', '볼티모어 · 외야수', '리스 하인즈', [T('SSG와', '협상 중', -1, True), T('나이', '26살', 0, c='c'), T('마이너리그', '100홈런', 2)]),
 CARD('하인즈', 'SSG', '볼티모어 · 외야수', '리스 하인즈', [T('SSG와', '협상 중', -1, True), T('나이', '26살', -1, c='c'), T('마이너리그', '100홈런', -1)], band=('구단도 인정', 2)),
 CARD('에레디아', 'SSG', 'SSG · 타자 · 2023~2026', '에레디아', [T('SNS에', '작별 인사', 2)]),
 BOARD('ssg', 'SSG', 'SSG', '2027 외국인', [R('아빌라', '투수', '아빌라', val='2년 310만 달러', st='계약', sc=Y, at=1, team='SSG'), R('리차드슨', '투수', '리차드슨', val='100만 달러', st='계약', sc=Y, at=1, team='SSG'),
        R('하인즈', '타자', '하인즈', st='협상 중', sc=W_, at=0, team='SSG')]),
 CARD('아빌라', 'SSG', 'SSG · 투수 · 7월 대체 선수', '아빌라', [T('2026 시즌', '9승 2패', 1), T('평균자책점', '1.44', 2, True)]),
 CARD('아빌라', 'SSG', 'SSG · 투수 · 7월 대체 선수', '아빌라', [T('2026 시즌', '9승 2패', -1), T('평균자책점', '1.44', -1, True)], band=('외국인 투수 2년 계약은 처음', 2)),
 # ── KT 37~43
 BOARD('kt', 'KT', 'KT', '정규시즌 1위', kt_rows(a=1)),
 BOARD('kt', 'KT', 'KT', '정규시즌 1위', kt_rows(s1=1)),
 BOARD('kt', 'KT', 'KT', '정규시즌 1위', kt_rows(s1=-1, s2=1)),
 CARD('힐리어드', 'KT', 'KT · 타자', '힐리어드', [T('2026 몸값', '100만 달러', 2), T('홈런', '44개', 3, c='c'), T('타점', '139개', 4)], nameAt=4),
 QUOTE('나도현', 'KT', 'KT 단장', '나도현', '힐리어드를 잡기 위해 최선을 다하겠다', at=1),
 QUOTE('힐리어드', 'KT', 'KT · 타자 · 2026년 9월', '힐리어드', '가능하다면 내년에도 KT에서 뛰고 싶다', at=1),
 CARD('대니엘', 'KT', 'KT · 투수 · 시즌 중 대체 선수', '대니엘', [T('2026 시즌', '5승 2패', 1), T('평균자책점', '2.13', 2), T('KT 방침', '재계약', 3, True)], nameAt=2),
 # ── 두산 44~48
 BOARD('ds', '두산', '두산', '2027 외국인', ds_rows(a=0)),
 BOARD('ds', '두산', '두산', '2027 외국인', ds_rows(jv=0, j=1, sv=3)),
 BOARD('ds', '두산', '두산', '2027 외국인', ds_rows(jv=-1, j=-1, sv=-1, bj=1)),
 QUOTE('김원형', '두산', '두산 감독', '김원형', '무조건 잘 치는 선수가 필요하다', at=2, nameAt=1),
 CARD('타카다', '두산', '두산 · 아시아쿼터 · 투수', '타카다', [T('2026 시즌', '39경기', 1), T('성적', '3승 1패 8홀드', 2, c='c'), T('재계약', '22만 달러', 3, True)]),
 # ── NC 49~52
 BOARD('nc', 'NC', 'NC', '2027 외국인', nc_rows(a=1, ry=3)),
 CARD('라일리', 'NC', 'NC · 투수 · 2025 다승왕', '라일리', [T('2026 시즌', '8승 1패', 2), T('평균자책점', '2.69', 3, True)]),
 BOARD('nc', 'NC', 'NC', '2027 외국인', nc_rows(tx=2)),
 BOARD('nc', 'NC', 'NC', '2027 외국인', nc_rows(tx=-1, doda=0, dodaSt=1)),
 # ── 삼성 53~63
 QQ('잡고 싶다고\n다 잡을 수 있는 게 아니다', ['삼성', 'KIA'], ats=[1, 1], logoSize=170),
 BIG('rule', 'KBO 규정', '외국인 연봉 한도', [dict(l='외국인 세 명 합계', big='한 해 400만 달러', at=0, bigAt=2)]),
 BOARD('ss', '삼성', '삼성', '한국시리즈 우승', [R('후라도', '투수', '후라도', st='재계약 목표', sc=W_, at=2, stAt=3), R('디아즈', '타자', '디아즈', st='재계약 목표', sc=W_, at=2, stAt=3), R('페덱', '투수', '페덱', st='재계약 목표', sc=W_, at=2, stAt=3)], band=('아직 계약한 선수 없음', 1)),
 CARD('페덱', '삼성', '삼성 · 투수 · 7월 대체 선수', '페덱', [T('2026 시즌', '7승 3패', 3), T('평균자책점', '2.95', 4, True)]),
 CARD('페덱', '삼성', '삼성 · 투수 · 7월 대체 선수', '페덱', [T('2026 시즌', '7승 3패', -1), T('평균자책점', '2.95', -1, True)], band=('한국시리즈 평균자책점 0.82', 1)),
 CARD('페덱', '삼성', '삼성 · 투수 · 7월 대체 선수', '페덱', [T('2026년에 받은 돈', '47만 달러', 1, True)]),
 CAP('sscap', '삼성 · 세 명을 다 잡으면', '2027 한도', 460, capLab='460만 달러', capAt=3, segs=[dict(l='후라도 + 디아즈', t='2026 몸값 그대로', v=330, at=4)], left=('페덱에게 줄 수 있는 돈 최대', '130만 달러', 7)),
 CARD('페덱', '삼성', '삼성 · 투수', '페덱', [T('미국 · 일본 구단도', '관심', 1)]),
 CARD('페덱', '삼성', '삼성 · 투수', '페덱', [T('미국 · 일본 구단도', '관심', -1), T('일본 리그 연봉 상한', '없음', 1, c='c')]),
 QUOTE('이종열', '삼성', '삼성 단장', '이종열', '경쟁은 항상 있다', at=1),
 CARD('페덱', '삼성', '삼성 · 투수', '페덱', [T('삼성이 줄 수 있는 돈', '최대 130만 달러', 0, True)], band=('페덱을 잡을 수 있을까?', 1)),
 # ── 기아 64~77
 BOARD('kia', 'KIA', 'KIA', '2027 외국인', kia_rows(a=0, na=0, sa=50), rb=True, band=('아직 계약한 선수 없음', 1)),
 BOARD('kia', 'KIA', 'KIA', '2027 외국인', kia_rows(sa=1), rb=True, band=('아직 계약한 선수 없음', -1)),
 BOARD('kia', 'KIA', 'KIA', '2027 외국인', kia_rows(), rb=True, band=('협상은 이제 들어가는 단계', 0)),
 QUOTE('이범호', 'KIA', 'KIA 감독', '이범호', '시즌 때 네일과 올러가 없었으면 안 됐다', at=1),
 QUOTE('이범호', 'KIA', 'KIA 감독', '이범호', '계약하면 스프링캠프를 일주일이나 열흘 늦게 부르겠다', at=1),
 CARDS('kia2', '2026 이닝', 'KIA 투수', [R('네일', '', '네일', val='183이닝', st='리그 1위', sc=Y, at=0, valAt=1, stAt=2), R('올러', '', '올러', val='178이닝', st='리그 2위', sc=W_, at=3, valAt=3, stAt=4)]),
 CAP('kiacap', 'KIA · 2026 몸값', '세 명 합계', 460, capLab='2027 한도 460만 달러', capAt=50, segs=[dict(l='네일', t='200만', v=200, at=1), dict(l='올러', t='120만', v=120, at=1), dict(l='카스트로', t='100만', v=100, at=1)], note=('420만 달러', 2)),
 CAP('kiacap', 'KIA · 2026 몸값', '세 명 합계', 460, capLab='2027 한도 460만 달러', capAt=2, segs=[dict(l='네일', t='200만', v=200, at=-1), dict(l='올러', t='120만', v=120, at=-1), dict(l='카스트로', t='100만', v=100, at=-1)], note=('420만 달러', -1)),
 CAP('kiacap', 'KIA · 2026 몸값', '세 명 합계', 460, capLab='2027 한도 460만 달러', capAt=-1, segs=[dict(l='네일', t='200만', v=200, at=-1), dict(l='올러', t='120만', v=120, at=-1), dict(l='카스트로', t='100만', v=100, at=-1)], note=('420만 달러', -1), left=('남는 돈', '40만 달러', 3)),
 CAP('kiacap', 'KIA · 2026 몸값', '세 명 합계', 460, capLab='2027 한도 460만 달러', capAt=-1, segs=[dict(l='네일', t='200만', v=200, at=-1), dict(l='올러', t='120만', v=120, at=-1), dict(l='카스트로', t='100만', v=100, at=-1)], note=('420만 달러', -1), left=('남는 돈', '40만 달러', -1),
     band=('한도 안에서 세 명을 다 잡기는 쉽지 않다는 전망', 1)),
 CARD('올러', 'KIA', 'KIA · 투수', '올러', [T('시즌 내내', '메이저리그 관심', 1)]),
 BOARD('kia', 'KIA', 'KIA', '2027 외국인', kia_rows(), rb=True, band=('되도록 한도 안에서 계약하겠다', 1)),
 QUOTE('심재학', 'KIA', 'KIA 단장', '심재학', '심사숙고하겠다', at=1),
 BOARD('kia', 'KIA', 'KIA', '2027 외국인', kia_rows(sira=0, siraSt=1), rb=True),
 # ── LG 78~86
 BOARD('lg', 'LG', 'LG', '2027 외국인', lg_rows(b=1)),
 CARD('오스틴', 'LG', 'LG · 타자', '오스틴', [T('2027 계약', '200만 달러', 0, True), T('외국인 타자', '역대 최고 금액', 1, c='c')]),
 CARD('벡', 'LG', 'LG · 새 투수', '벡', [T('메이저리그', '4시즌', 2), T('최고 구속', '시속 158km', 4, True)]),
 QUOTE('염경엽', 'LG', 'LG 감독', '염경엽', 'LG 감독을 하면서 뽑은 외국인 투수 가운데 제일 좋다', at=1),
 BOARD('lg', 'LG', 'LG', '2027 외국인', lg_rows(), rb=False),
 CARD('톨허스트', 'LG', 'LG · 투수', '톨허스트', [T('2026 시즌', '12승', 0), T('남은 투수 한 자리', '재계약', 1, c='c', vs='새 투수', vsAt=2)]),
 QUOTE('염경엽', 'LG', 'LG 감독', '염경엽', '외국인 투수 두 명을 모두 바꿀 수도 있다', at=1),
 BOARD('lg', 'LG', 'LG', '2027 외국인', lg_rows(ken=1, kenSt=2)),
 QUOTE('차명석', 'LG', 'LG 단장', '차명석', '아직 계약을 맺은 건 아니다', at=1),
 # ── 키움 87~92
 BOARD('kw', '키움', '키움', '2027 외국인', kw_rows(a=2, n0=2, n1=2, sa=50), rb=True, band=('10개 구단 중 가장 먼저 완료', 2)),
 BOARD('kw', '키움', '키움', '2027 외국인', kw_rows(sa=2), rb=True, band=('10개 구단 중 가장 먼저 완료', -1)),
 CARDS('kw2', '2026 성적', '키움 외국인 세 명', [R('알칸타라', '투수', '알칸타라', val='9승 9패', st='평균자책점 3.87', sc=G, at=0, valAt=1, stAt=2), R('데이비슨', '타자', '데이비슨', val='28홈런', st='시즌 합계', sc=G, at=3, valAt=3, stAt=3),
        R('히우라', '타자', '히우라', val='13홈런', st='72경기', sc=G, at=4, stAt=4, valAt=5)]),
 CAP('kwcap', '키움 · 2027 계약', '세 명 합계', 400, capLab='기본 한도 400만 달러', capAt=2, segs=[dict(l='알칸타라', t='', v=110, at=1), dict(l='데이비슨', t='', v=110, at=1), dict(l='히우라', t='', v=80, at=1)],
     note=('300만 달러', 1), left=('한도까지', '100만 달러', 3)),
 CARDS('kw3', '키움 아시아쿼터', '2027 시즌', [R('유토', '2026 시즌', '유토', st='결별', sc=RD, at=1), R('후쿠타니', '새로 영입 · 일본 투수', '후쿠타니', val='20만 달러', st='영입', sc=Y, at=2, valAt=3, stAt=3)]),
 CARDS('kw3', '키움 아시아쿼터', '2027 시즌', [R('유토', '2026 시즌', '유토', st='다른 KBO 팀과 계약 가능', sc=W_, st0='결별', sc0=RD, stAt=1, at=-1), R('후쿠타니', '새로 영입 · 일본 투수', '후쿠타니', val='20만 달러', st='영입', sc=Y, at=-1)]),
 # ── 정리 93~100
 QQ('세 명을 다 잡는다고 했을 때\n한도가 빠듯한 팀', ['KIA', '삼성'], ats=[0, 0], hl=[1], logoAt=2, logoSize=170),
 BIG('sum', '세 명을 다 잡는다고 했을 때', '한도가 빠듯한 두 팀', [dict(logo='KIA', name='KIA', l='몸값을 그대로 묶어도', big='남는 돈 40만 달러', at=0, bigAt=1), dict(logo='삼성', name='삼성', l='페덱에게 줄 수 있는 돈', big='최대 130만 달러', at=2, bigAt=3)]),
 BIG('cal', '2026년', '남은 일정', [dict(l='재계약할 선수 결정', big='11월 25일까지', at=0, lAt=1), dict(l='보류선수 명단 공시', big='11월 30일', at=2, bigAt=3), dict(l='메이저리그 직장폐쇄 가능', big='12월 2일', at=50)], stack=True),
 BIG('cal', '2026년', '남은 일정', [dict(l='재계약할 선수 결정', big='11월 25일까지', at=-1), dict(l='보류선수 명단 공시', big='11월 30일', at=-1), dict(l='메이저리그 직장폐쇄 가능', big='12월 2일', at=0, lAt=1)], stack=True),
 CARD('페덱', '삼성', '삼성 · 투수', '페덱', [T('', '지킬 수 있을까?', 0, True)]),
 CARD('페덱', '삼성', '삼성 · 투수', '페덱', [T('', '지킬 수 있을까?', -1, True), T('', '뺏길까?', 0, c='c')]),
 QQ('여러분은\n어떻게 보세요?', ['삼성'], hl=[1], logoSize=170),
 QQ('채널 구독하고\n외국인 계약 소식 받아보세요', ALL10, ats=[2, 2]),
]
assert len(SC) == 99, len(SC)
CHT = {'오프닝': '이미 계약한 선수들', '한화': '한화 — 숄텐스·페라자', '롯데': '롯데 — 레이예스 협상 막바지', 'SSG': 'SSG — 새 타자 하인즈', 'KT': 'KT — 힐리어드를 잡아라', '두산': '두산 — 거의 다 바꾼다', 'NC': 'NC — 라일리·도다 재계약 추진',
       '삼성': '삼성 — 페덱에게 줄 수 있는 돈', '기아': 'KIA — 남는 돈 40만 달러', 'LG': 'LG — 남은 투수 한 자리', '키움': '키움 — 가장 먼저 완료', '정리': '정리 — 남은 일정'}
CHS = {'오프닝': '외국인 현황', '기아': 'KIA'}
lines, scenes, CH = [], [], []
i = 0
for name, ls in SEC:
    CH.append({"key": name, "title": CHT[name], "short": CHS.get(name, name), "from": i, "to": i + len(ls) - 1})
    for nr in ls:
        narr = tight(nr.replace(' /+ ', ' / +'))
        pcs = SUBTXT(nr)
        assert len(pcs) == len(narr.split(' / ')), nr
        l = {"narr": narr, "sub": "|".join(wrap2(p) for p in pcs)}
        if i in GAPS: l['gapAfter'] = GAPS[i]
        lines.append(l)
        s2 = copy.deepcopy(SC[i]); s2['startLine'] = i; s2['tc'], s2['tc2'] = TCOL[name]; s2['noCenter'] = True
        # 줄의 호흡 수보다 큰 at 은 잘못(50 = 안 보임, 음수 = 이미 보임)
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
        if scenes and scenes[-1].get('chain') and scenes[-1].get('chain') == s2.get('chain') and scenes[-1]['type'] == s2['type']: s2['cont'] = True   # 이어받기 표시(rule_check R8)
        scenes.append(s2); i += 1
# 같은 사람 카드에서 같은 기록 칸이 다음 장면까지 이어질 때, 칸 수가 늘어도 크기가 안 바뀌게 가장 많은 칸 수에 맞춘다(사용자 11/21 03:22 '협상 중 카드는 처음부터 작게')
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
TITLE = "삼성, 130만 달러로 페덱 지킬 수 있나 | 10개 구단 외국인 현황"
DESC = ("2027 시즌 KBO 10개 구단 외국인 선수 계약이 어디까지 왔는지 한 번에 정리했어요.\n"
        "이미 계약한 선수: LG 오스틴(1년 200만 달러)·벡(87만 8천 달러), SSG 아빌라(2년 총액 310만 달러)·리차드슨(100만 달러), 키움 알칸타라·데이비슨(각 110만 달러)·히우라(80만 달러), 한화 왓슨(100만 달러). 아시아쿼터는 한화 왕옌청(30만 달러)·두산 타카다(22만 달러) 재계약, 키움 후쿠타니(20만 달러) 영입.\n"
        "진행 중: 한화 숄텐스(탬파베이가 KBO에서 뛸 기회를 위해 방출, 한화 공식 발표 전), 롯데 레이예스 재계약 협상, SSG 새 타자 하인즈 협상, KT 힐리어드·대니엘 재계약 방침, LG 남은 투수 한 자리, 두산은 교체 방향, NC는 라일리·도다만 재계약 추진.\n"
        "삼성과 KIA는 외국인 연봉 한도(세 명 합계 한 해 400만 달러, 재계약하면 늘어남)가 문제예요. 2027 한도 460만 달러 기준으로 KIA는 세 명 몸값을 그대로 묶어도 40만 달러가 남고, 삼성은 페덱에게 최대 130만 달러를 줄 수 있어요.\n"
        "구단은 11월 25일까지 재계약할 선수를 정하고, 보류선수 명단은 11월 30일에 나와요. 영상 내용은 2026년 11월 21일 기준이에요.")
EP = {"theme": "mg", "sb": True, "date": "2026-11-21", "gameDate": "2026-11-21", "series": "야구롱폼", "focusTeam": "", "speed": 1.0,
      "ttsApi": True, "ttsVoice": "A", "ttsWhole": False, "ttsTempo": 1.2, "ttsTempoSlow": 1.15, "rev": "1121-fx-v1", "topic": "10개구단외국인현황", "endcardSec": 10,
      "gapScale": 1.25, "pauseMax": 0.45, "sentPauseMin": 0.4, "clausePauseMin": 0.3, "ttsCharsOk": 7000, "totalSec": 485,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False,
      "source": "대사 fx21/script_v3.txt · 근거 = claude/외국인현황-대본v3-1121.md 확인 표 · claude/외국인-리서치-1121.md",
      "youtube": {"title": TITLE, "description": DESC, "cta": "삼성은 페덱을 지킬 수 있을까요? 아니면 미국이나 일본에 뺏길까요? 여러분은 어떻게 보세요?", "prev": "2026 MVP 누가 받을까",
                  "tags": ["외국인 선수", "KBO 외국인", "외국인 재계약", "페덱", "숄텐스", "레이예스", "오스틴", "힐리어드", "네일", "올러", "아빌라", "하인즈", "외국인 연봉 상한", "아시아쿼터", "스토브리그", "프로야구", "KBO"],
                  "hashtags": ["#KBO", "#외국인선수", "#페덱", "#숄텐스", "#스토브리그"],
                  "teams": ["한화 이글스", "롯데 자이언츠", "SSG 랜더스", "KT 위즈", "두산 베어스", "NC 다이노스", "삼성 라이온즈", "기아 타이거즈", "LG 트윈스", "키움 히어로즈"],
                  "players": ["오스틴", "벡", "톨허스트", "케네디", "아빌라", "리차드슨", "하인즈", "에레디아", "알칸타라", "데이비슨", "히우라", "후쿠타니", "유토", "왓슨", "숄텐스", "와이스", "화이트", "페라자", "왕옌청", "레이예스", "로드리게스", "비슬리",
                              "스기모토", "로건", "힐리어드", "대니엘", "잭로그", "세베리노", "벤자민", "타카다", "라일리", "테일러", "도다", "후라도", "디아즈", "페덱", "네일", "올러", "카스트로", "시라카와"]}}
if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'episodes'), exist_ok=True)
    out = os.path.join(HERE, 'episodes', '2026-11-21_롱폼.json')
    json.dump(EP, io.open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for l in lines)
    print('ok', out, len(lines), '줄', len(scenes), '장면', '합성 글자', tot)
    if '--subs' in sys.argv:
        for k, l in enumerate(lines): print(k + 1, l['sub'].replace('\n', '⏎'), '|GAP %s' % l['gapAfter'] if 'gapAfter' in l else '')
