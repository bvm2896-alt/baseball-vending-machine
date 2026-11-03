# 11/3 「기아 2027 스토브리그」 롱폼(episodes/2026-11-02_롱폼2.json) → 컷 쇼츠 7편(세로 1080x1920)
# 사용자 11/3 "기아 스토브리그 숏츠로 쪼개보자" + "이호민편 추가" + "쇼츠는 넘기다 보는 비율이 높으니 무슨 내용인지 먼저 인지"(F-151)
#  → 첫 호흡 = 팀+선수+주제 낱말, 0초부터 제목줄(vtitle)·선수 사진·이름. 결론이 마지막 줄 → 질문 → 관련 영상 → 구독.
# 롱폼 장면은 rf_* (가로 틀 전용)라 세로 틀 장면(pstat·speech·slotboard·capbar·quote·question·photo)으로 새로 짬.
# 음성: voiceFrom 줄 번호는 '회사 PC' work\voice_2026-11-02_롱폼2 의 번호(그 폴더는 91줄판이라 롱폼 v4 줄 번호와 2칸 어긋남 — 대사 글이 같은 파일 번호로 맞춤).
#       → 회사 PC 에서 롱폼_숏츠만들기.cmd 로 만든다(집 PC 에서 누르면 줄 번호가 안 맞아 새로 합성됨).
import json, io, os, copy, re, sys
HERE = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/bvm/시스템'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'episodes')
SRC = 'episodes/2026-11-02_롱폼2.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN = ep['lines']; SCN = {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
VI = {int(k): v for k, v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vi.json'))).items()}
TH = '상황별/썸네일_롱폼_기아2027스토브리그'
DATE = '2026-11-02'

def wrap16(s, n=16):
    if '\n' in s or len(s) <= n: return s
    w = s.split(' '); best = None
    for k in range(1, len(w)):
        a, b = ' '.join(w[:k]), ' '.join(w[k:])
        sc = max(len(a), len(b))
        if re.match(r'^(게|것|수|억|원|점|개|번|명|위|년|월|일|경기|타점|홈런|세이브|타석|이닝|달러)', b) or re.search(r'\d$', a): sc += 20
        if len(a) > n or len(b) > n: sc += 5
        if best is None or sc < best[0]: best = (sc, a + '\n' + b)
    return best[1]

def NEW(narr, sub, scene, slow=False):
    pcs = [wrap16(x) for x in sub.split('|')]
    assert len(pcs) == len(narr.split(' / ')), (narr, sub)
    d = {'narr': narr, 'sub': '|'.join(pcs)}
    if slow: d['pace'] = 'slow'
    return (None, d, scene)

def OLD(i, scene, sub=None):
    d = copy.deepcopy(LN[i]); d.pop('gapAfter', None)
    d['sub'] = sub if sub else '|'.join(wrap16(x.replace('\n', ' ')) for x in d['sub'].split('|'))   # 쇼츠 자막 16자
    assert i in VI, ('회사 PC 음성 없음', i)
    return (VI[i], d, scene)

K = 'KIA'
def PST(img, name, stats=(), viz=(), sub=None, chain=None, cont=False, text=None, textAt=None, focus=None, team=K):
    s = {'type': 'pstat', 'img': img, 'team': team, 'name': name, 'viz': list(viz), 'stats': [dict(zip(('k', 'v', 'at', 'hi'), x)) if isinstance(x, tuple) else x for x in stats], 'noCenter': True}
    for k_, v_ in (('sub', sub), ('chain', chain), ('text', text), ('textAt', textAt), ('focus', focus)):
        if v_ is not None: s[k_] = v_
    if cont: s['cont'] = True
    return s
def SAL(hi, at=(1, 2, 2), title='2026년 총액(달러)'):   # 외국인 세 명 총액 막대
    o = [('카스트로', 100, '100만'), ('올러', 120, '120만'), ('네일', 200, '200만')]
    return {'type': 'trend', 'title': title, 'items': [{'x': x, 'v': v, 'vt': t, 'at': a, 'hi': x == hi, **({'c': '#FF5A63'} if x == hi else {})} for (x, v, t), a in zip(o, at)]}
def STEPS(*its): return {'type': 'steps', 'items': [dict(zip(('d', 't', 'at', 'c'), x)) for x in its]}
def STAMP(t, at, c='gold'): return {'type': 'stamp', 't': t, 'at': at, 'c': c}
PROF = {'카스트로': 'KBO프로필/카스트로', '네일': 'KBO프로필/네일', '올러': 'KBO프로필/올러'}
def SLOT3(title, chain, tags=None, at=(-1, -1, -1), cont=False, money=None):
    sl = []
    for (n, a) in zip(('카스트로', '네일', '올러'), at):
        x = {'img': PROF[n], 'name': n, 'pos': '', 'at': a}
        if money: x['money'] = money[n]
        if tags and n in tags: x.update(tag=tags[n][0], tagAt=tags[n][1], tc=tags[n][2])
        sl.append(x)
    s = {'type': 'slotboard', 'title': title, 'team': K, 'slots': sl, 'noCenter': True, 'profile': True, 'chain': chain}
    if cont: s['cont'] = True
    return s
def SLOTN(title, chain, names, tags=None, at=None, cont=False):
    s = SLOT3(title, chain, tags=tags, cont=cont); s['slots'] = [x for x in s['slots'] if x['name'] in names]
    for x, a in zip(s['slots'], at or [-1] * len(names)): x['at'] = a
    return s
def SLOT(title, slots, chain=None, cont=False, bracket=None):
    s = {'type': 'slotboard', 'title': title, 'team': K, 'slots': slots, 'noCenter': True, 'profile': False}
    if chain: s['chain'] = chain
    if cont: s['cont'] = True
    if bracket: s['bracket'] = bracket
    return s
def SP(img, name, bubbles, chain=None, cont=False, sub=None, who='', mini=None):   # 말풍선(speech)은 세로에서 깨알 → pstat + 인용 칸(10/26 컷 방식)
    return PST(img, name, viz=[{'type': 'quote', 'date': who, 'text': t, 'at': a, **({'src': True} if who else {}), **({'hi': True} if hi else {})} for t, a, hi in bubbles] + ([{'type': 'mini', 'items': [{'img': PROF[mini], 'name': mini, 'team': K, 'at': 0}]}] if mini else []), chain=chain, cont=cont, sub=sub)
def Q(narr, sub, text, faces=None, logos=None):
    sc = {'type': 'question', 'text': text, 'mood': 'wave', 'revealAt': 1, 'vsize': 96}
    if faces: sc['faces'] = faces
    if logos: sc['logos'] = logos
    return NEW(narr, sub, sc, slow=True)
POINT = lambda: NEW('기아 이천이십칠 스토브리그 / 전체 이야기는 / 하단 관련 영상에 있어요', '기아 2027 스토브리그|전체 이야기는|하단 관련 영상에 있어요',
                    {'type': 'photo', 'img': TH, 'fit': 'cover', 'text': '', 'relArrow': True, 'chain': 'relvid', 'mood': 'wave'})
CTA = lambda: (None, {'narr': '채널 구독하고 매일 야구 이슈 받아보세요', 'sub': '채널 구독하고\n매일 야구 이슈 받아보세요!', 'rate': 1.0},
               {'type': 'photo', 'img': TH, 'fit': 'cover', 'text': '', 'chain': 'relvid', 'cont': True, 'mood': 'cheer'})
F3 = [PROF[x] for x in ('카스트로', '네일', '올러')]
CUTS = []
def EX(s, tag=None):
    s = copy.deepcopy(s)
    for x in s['slots']:
        if x['name'] == '카스트로': x['money'] = '100만→150만 달러'
        if tag and x['name'] == '올러': x['tag'] = tag
    return s

# ① 카스트로 ─────────────────────────────────────────
CUTS.append(dict(topic='기아카스트로재계약', vtitle=['카스트로 재계약', '기아 2027'], lines=[
  NEW('기아 외국인 타자 카스트로, / 이천이십칠 년 재계약할까요?', '기아 외국인 타자 카스트로|2027년 재계약할까요?',
      PST('경기/카스트로_홈런세리머니_1010_KIA제공', '카스트로', chain='c1')),
  OLD(25, PST('경기/카스트로_홈런세리머니_1010_KIA제공', '카스트로', [('출전', '99경기', 3, False), ('타율', '3할 2푼 7리', 4, True), ('홈런 · 타점', '21홈런 88타점', 5, False)], sub='2026 정규시즌', chain='c1', cont=True)),
  OLD(31, PST('경기/카스트로_홈런세리머니_1010_KIA제공', '카스트로', [('출전', '99경기', -1, False), ('2026년', '시즌 초 부상', 0, True)], chain='c1', cont=True)),
  OLD(26, PST('카드/FA9_카스트로_홈런', '카스트로', [('홈런', '투런', 2, False), ('1차전 기록', '3안타 3타점', 2.5, True)], chain='c1', cont=True)),
  OLD(27, PST('경기/카스트로_엄지_0810_KIA제공', '카스트로', viz=[SAL('카스트로', at=(1, 2, 2))], chain='c1', cont=True)),
  OLD(28, SP('경기/김도영_덕아웃_KIA제공', '김도영', [('카스트로가 빨리\n계약하면 좋겠다', 2, True)], chain='kd', who='10월 말 인터뷰')),
  OLD(29, SP('카드/P18_카스트로_환호', '카스트로', [('카스트로가\n너무 고맙다', 1, True)], chain='kq', who='김도영')),
  OLD(30, {'type': 'slotboard', 'title': '카스트로도 남고 싶다', 'team': K, 'noCenter': True, 'profile': True, 'slots': [
      {'img': PROF['카스트로'], 'name': '카스트로', 'pos': '', 'at': 0, 'tag': '재계약 부탁', 'tagAt': 1, 'tc': 'gold'},
      {'img': 'KBO프로필/김도영', 'name': '김도영', 'pos': '', 'at': 0}]}),
  OLD(54, SLOTN('외국인 재계약 전망', 'vd', ['카스트로', '네일'], tags={'카스트로': ('잔류 유력', 1, 'good')}, at=(0, 2))),
  Q('카스트로, / 이천이십칠 년에도 기아에 남을까요? / 아니면 떠날까요?', '카스트로|2027년에도 기아에 남을까요?|아니면 떠날까요?', '카스트로\n남을까? 떠날까?', faces=[PROF['카스트로']]),
  POINT(), CTA()],
  yt=dict(title='카스트로 재계약 | 기아 2027, 김도영 "빨리 계약하면 좋겠다"')))

# ② 네일 ─────────────────────────────────────────────
CUTS.append(dict(topic='기아네일재계약', vtitle=['네일 재계약', '기아 2027'], lines=[
  NEW('기아 외국인 투수 네일, / 이천이십칠 년 재계약할까요?', '기아 외국인 투수 네일|2027년 재계약할까요?',
      PST('경기/네일_주먹환호_KIA제공', '네일', chain='n1')),
  OLD(33, PST('경기/네일_주먹환호_KIA제공', '네일', viz=[STEPS(('2025년 겨울', '메이저리그 구단 관심', 2, None), ('2026년', '기아 잔류', 3.4, 'good'))], chain='n1', cont=True)),
  OLD(34, PST('카드/P17_네일_포효', '네일', [('출전', '31경기', 1, False), ('승리', '13승', 2, False), ('평균자책점', '3.49', 3, True)], chain='n1', cont=True)),
  OLD(35, PST('카드/P17_네일_역투', '네일', viz=[STEPS(('4회까지', '1안타', 1, 'good'), ('다음 이닝', '헤드샷 퇴장', 2, 'bad'))], chain='n1', cont=True)),
  OLD(36, PST('경기/네일_포효_엑스포츠뉴스', '네일', [('플레이오프', '1승 2패', 0, False), ('4차전 선발', '4대2 역전승', 2, True)], chain='n1', cont=True)),
  OLD(37, PST('경기/네일_포효_엑스포츠뉴스', '네일', viz=[SAL('네일', at=(3, 3, 3))], chain='n1', cont=True)),
  OLD(56, PST('경기/네일_역투_KIA제공', '네일', [('플레이오프 4차전', '탈락 위기 선발', 0, True)], chain='n9')),
  Q('네일, / 이천이십칠 년에도 기아에 남을까요? / 아니면 떠날까요?', '네일|2027년에도 기아에 남을까요?|아니면 떠날까요?', '네일\n남을까? 떠날까?', faces=[PROF['네일']]),
  POINT(), CTA()],
  yt=dict(title='네일 재계약 | 기아 2027, 13승 에이스 몸값이 관건')))

# ③ 올러 ─────────────────────────────────────────────
CUTS.append(dict(topic='기아올러재계약', vtitle=['올러 재계약', '기아 2027'], lines=[
  NEW('기아 외국인 투수 올러, / 이천이십칠 년 재계약할까요?', '기아 외국인 투수 올러|2027년 재계약할까요?',
      PST('카드/P18_올러_투구', '올러', chain='o1')),
  OLD(39, PST('카드/P18_올러_투구', '올러', [('승리', '11승', 2, False), ('평균자책점', '3.13', 3, True)], chain='o1', cont=True)),
  OLD(40, sub='2025년에도 11승을 올려|두 시즌 연속\n두 자릿수 승리를 거뒀죠', scene=PST('카드/P18_올러_투구', '올러', viz=[{'type': 'trend', 'title': '시즌 승수', 'items': [{'x': '2025년', 'v': 11, 'vt': '11승', 'at': 0}, {'x': '2026년', 'v': 11, 'vt': '11승', 'at': 1, 'hi': True}]}], chain='o1', cont=True)),
  OLD(41, PST('경기/올러_경기_KIA제공_세로', '올러', viz=[STAMP('두 경기 모두 조기 강판', 2, 'bad')], chain='o2')),
  OLD(42, PST('경기/올러_경기_KIA제공_세로', '올러', viz=[{'type': 'ip', 'items': [{'d': '2차전', 'ip': 4.667, 'r': 5, 'at': 1}, {'d': '5차전', 'ip': 2, 'r': 4, 'at': 2}]}], chain='o2', cont=True)),
  OLD(43, PST('경기/올러_하이파이브_1018', '올러', viz=[SAL('올러', at=(1, 1, 1))], chain='o3')),
  OLD(57, PST('카드/P18_올러_포효', '올러', [('정규시즌', '11승', 2, False), ('큰 경기', '두 번 무너짐', 3, True)], chain='o4')),
  NEW('올러가 몸값을 크게 올려 달라면 / 첫해 백만 달러로 묶인 / 새 외국인 투수가 더 쌀 수 있거든요', '올러가 몸값을 크게 올려 달라면|첫해 100만 달러로 묶인|새 외국인 투수가 더 쌀 수 있거든요',
      PST('카드/P18_올러_포효', '올러', viz=[{'type': 'trend', 'title': '총액(달러)', 'items': [{'x': '올러 2026', 'v': 120, 'vt': '120만', 'at': 0}, {'x': '새 선수 첫해', 'v': 100, 'vt': '최대 100만', 'at': 1, 'hi': True, 'c': '#3BB273'}]}], chain='o4', cont=True)),
  OLD(88, PST('카드/P18_올러_포효', '올러', viz=[STAMP('교체 1순위', 1, 'bad')], chain='o4', cont=True)),
  Q('올러, / 이천이십칠 년에도 기아에 남을까요? / 아니면 바뀔까요?', '올러|2027년에도 기아에 남을까요?|아니면 바뀔까요?', '올러\n남을까? 바뀔까?', faces=[PROF['올러']]),
  POINT(), CTA()],
  yt=dict(title='올러 재계약 | 기아 2027, 두 시즌 연속 11승에도 가장 먼저 바뀔 수 있는 이유')))

# ④ 외국인 한도 ───────────────────────────────────────
CUTS.append(dict(topic='기아외국인선수한도', vtitle=['기아 외국인 한도', '셋 다 잡으면?'], lines=[
  NEW('기아 외국인 선수 한도, / 셋 다 재계약하면 / 돈이 남을까요?', '기아 외국인 선수 한도|셋 다 재계약하면|돈이 남을까요?',
      SLOT3('2026 외국인 선수', 'f0', at=(-1, -1, -1))),
  OLD(45, copy.deepcopy(SCN[45])), OLD(46, copy.deepcopy(SCN[46])), OLD(47, copy.deepcopy(SCN[47])),
  OLD(48, copy.deepcopy(SCN[48])), OLD(49, dict(copy.deepcopy(SCN[49]), text='', textAt=-1)), OLD(50, copy.deepcopy(SCN[50])),
  OLD(51, EX(SCN[51])), OLD(52, EX(SCN[52], tag='2026년 120만보다 적음')),
  NEW('그래서 셋 다 잡으려면 / 누군가는 몸값을 / 덜 올려 받아야 해요', '그래서 셋 다 잡으려면|누군가는 몸값을|덜 올려 받아야 해요', EX(SCN[52], tag='2026년 120만보다 적음') | {'cont': True, 'bracket': {'a': 0, 'b': 2, 'label': '셋 다 잡으려면 양보 필요', 'at': 1, 'c': 'gold'}}),
  Q('셋 다 잡아야 할까요? / 아니면 한 명은 바꿔야 할까요?', '셋 다 잡아야 할까요?|아니면 한 명은 바꿔야 할까요?', '셋 다 잡을까?\n한 명 바꿀까?', faces=F3),
  POINT(), CTA()],
  yt=dict(title='기아 외국인 선수 한도 | 카스트로·네일·올러 셋 다 잡으면 460만 달러로 될까')))

# ⑤ 김도영 메이저리그 ─────────────────────────────────
CUTS.append(dict(topic='김도영메이저리그', vtitle=['김도영 메이저리그', '언제 갈 수 있나'], lines=[
  NEW('기아 김도영의 메이저리그 도전, / 언제 가능할까요?', '기아 김도영의 메이저리그 도전|언제 가능할까요?',
      PST('경기/김도영_45호_타격_1012_KIA제공', '김도영', chain='k1')),
  OLD(73, PST('경기/김도영_45호_타격_1012_KIA제공', '김도영', [('2026 홈런왕', '45홈런', 0, False)], viz=[STEPS(('2026년 겨울', '도전 불가', 2, 'bad'), ('빠르면', '2028시즌 뒤', 4, 'good'))], chain='k1', cont=True)),
  OLD(74, PST('경기/김도영_포효_스포츠조선', '김도영', [('2026 아시안게임', '금메달', 1, False), ('병역', '해결', 1, True), ('메이저리그', '여러 구단 관심', 2, False)], chain='k1', cont=True)),
  OLD(75, PST('경기/김도영_포효_스포츠조선', '김도영', viz=[{'type': 'seasons', 'title': '김도영과 함께 우승을 노릴 시즌', 'items': [{'t': '2027', 'at': 1, 'hi': True}, {'t': '2028', 'at': 2, 'hi': True}]}], chain='k1', cont=True)),
  OLD(78, PST('경기/나성범_세리머니_KIA제공', '나성범', [('2027년', '계약 마지막 해', 1, True), ('계약', '6년 150억', 2, False)])),
  OLD(79, {'type': 'photo', 'img': '경기/KIA_잠실마지막승리_1020_연합', 'fit': 'cover', 'text': '2027년\n우승 도전', 'vsize': 92}),
  Q('김도영은 / 이천이십팔 시즌 뒤 메이저리그에 갈까요? / 아니면 기아에 남을까요?', '김도영은|2028시즌 뒤 메이저리그에 갈까요?|아니면 기아에 남을까요?', '김도영\n메이저? 기아?', faces=['KBO프로필/김도영']),
  POINT(), CTA()],
  yt=dict(title='김도영 메이저리그 언제? 빠르면 2028시즌 뒤, 기아 우승 기회는 두 시즌')))

# ⑥ 김호령 FA ────────────────────────────────────────
HR = '경기/김호령_만루포_0821_KIA제공_세로'; TG = '경기/김태군_덕아웃_0729_KIA제공'
LFA = lambda a, b, c, t1, t2, t3, cont: SLOT('2025년 겨울 떠난 내부 FA', [
    {'img': '경기/박찬호_타격_0922_두산제공', 'name': '박찬호', 'pos': '두산', 'at': a, 'tag': '4년 80억', 'tagAt': t1, 'tc': 'bad'},
    {'img': '경기/최형우_만루포미소_0826_삼성제공_세로', 'name': '최형우', 'pos': '삼성', 'at': b, 'tag': '2년 26억', 'tagAt': t2, 'tc': 'bad'},
    {'img': '경기/한승택_세리머니_0915_KT제공', 'name': '한승택', 'pos': 'KT', 'at': c, 'tag': '4년 10억', 'tagAt': t3, 'tc': 'bad'}], chain='lf', cont=cont)
CUTS.append(dict(topic='기아김호령FA', vtitle=['김호령 FA', '기아 첫 숙제'], lines=[
  NEW('기아 김호령 에프에이, / 플레이오프 무안타에도 / 잡아야 할까요?', '기아 김호령 FA|플레이오프 무안타에도|잡아야 할까요?',
      PST('카드/F16_김호령_A', '김호령', [('플레이오프', '무안타', 1, True)], chain='h0')),
  NEW('이천이십육 년 겨울엔 / 포수 김태군과 중견수 김호령이 / 에프에이 자격을 얻을 것으로 보여요', '2026년 겨울엔|포수 김태군과 중견수 김호령이|FA 자격을 얻을 것으로 보여요', SLOT('2026년 겨울 FA 유력', [{'img': TG, 'name': '김태군', 'pos': '포수', 'at': 1}, {'img': HR, 'name': '김호령', 'pos': '중견수', 'at': 1}])),
  OLD(11, PST('경기/김호령_환호_연합뉴스', '김호령', [('3차전', '삼진 4개', 2, False), ('5차전', '선발 제외', 3, True)], chain='h1')),
  OLD(14, PST('경기/김호령_환호_연합뉴스', '김호령', [('3차전', '삼진 4개', -1, False), ('5차전', '선발 제외', -1, True)], viz=[STAMP('FA 몸값 ↓?', 1, 'bad')], chain='h1', cont=True)),
  NEW('기아는 이천이십오 년 겨울에도 / 박찬호, 최형우, 한승택 / 내부 에프에이 세 명을 / 다른 팀에 보냈는데요', '기아는 2025년 겨울에도|박찬호 최형우 한승택|내부 FA 세 명을|다른 팀에 보냈는데요', LFA(1, 1, 1, 50, 50, 50, False)),
  OLD(17, LFA(-1, -1, -1, 1, 3, 50, True)),
  OLD(18, LFA(-1, -1, 0, -1, -1, 1, True)),
  OLD(21, SLOT('2026년 겨울 첫 숙제', [{'img': HR, 'name': '김호령', 'pos': '중견수', 'at': 2}, {'img': TG, 'name': '김태군', 'pos': '포수', 'at': 2}],
                bracket={'a': 0, 'b': 1, 'label': '내부 FA 잡기', 'at': 2, 'c': 'gold'})),
  Q('김호령, / 기아가 붙잡을까요? / 아니면 놓칠까요?', '김호령|기아가 붙잡을까요?|아니면 놓칠까요?', '김호령\n잡을까? 놓칠까?', faces=['KBO프로필/김호령']),
  POINT(), CTA()],
  yt=dict(title='김호령 FA, 플레이오프 무안타에도 기아가 꼭 잡아야 하는 이유')))

# ⑦ 이호민 ───────────────────────────────────────────
HM = '경기/이호민_드래프트_0921_KIA제공'
CUTS.append(dict(topic='기아이호민신인', vtitle=['이호민 기아', '1라운드 3순위'], lines=[
  NEW('기아 일라운드 신인 이호민, / 구단이 키우려는 / 차세대 삼루수예요', '기아 1라운드 신인 이호민|구단이 키우려는|차세대 3루수예요',
      PST(HM, '이호민', sub='경남고 내야수', chain='m1')),
  OLD(62, PST(HM, '이호민', [('2027 신인 드래프트', '1라운드', 1, False), ('전체', '3순위', 3, True)], sub='경남고 내야수', chain='m1', cont=True)),
  OLD(63, PST(HM, '이호민', [('2026 고교 20경기 타율', '4할 2푼', 2, True), ('홈런 · 타점', '2홈런 19타점', 3, False)], sub='경남고 내야수', chain='m1', cont=True)),
  OLD(64, PST(HM, '이호민', [('일본전', '홈런 · 2루타', 1, False), ('청소년 아시아 선수권', '7타점', 2, True)], sub='경남고 내야수', chain='m1', cont=True)),
  OLD(65, SP(HM, '이호민', [('1년에 한두 명 나올 만한\n우타 거포형 재목', 1, False)], chain='m1', cont=True, sub='경남고 내야수', who='기아 스카우트')),
  OLD(66, SP(HM, '이호민', [('최근 몇 년 이만한 장타력\n고교 선수는 없었다', 1, False)], chain='m1', cont=True, sub='경남고 내야수', who='기아 단장')),
  NEW('스카우트는 수비만 잘 다듬으면 / 이범호 감독급 삼루수가 / 될 거라고 봤어요', '스카우트는 수비만 잘 다듬으면|이범호 감독급 3루수가|될 거라고 봤어요', SP(HM, '이호민', [('이범호 감독급\n3루수가 될 것', 0, False)], chain='m1', cont=True, sub='경남고 내야수', who='기아 스카우트')),
  OLD(68, SLOT('3루 계획', [{'img': '경기/김도영_45호_덕아웃_1012_KIA제공', 'name': '김도영', 'pos': '유격수 검토', 'at': 0}, {'img': HM, 'name': '이호민', 'pos': '3루수', 'at': 2}])),
  NEW('이호민, / 이범호 감독급 삼루수가 될까요? / 아니면 시간이 더 걸릴까요?', '이호민|이범호 감독급 3루수가 될까요?|아니면 시간이 더 걸릴까요?', {'type': 'question', 'text': '이호민\n이범호급 3루수?', 'mood': 'wave', 'revealAt': 1, 'vsize': 96, 'img': HM, 'fit': 'cover'}, slow=True),
  POINT(), CTA()],
  yt=dict(title='이호민 기아 1라운드 3순위 신인은 김도영 뒤를 이을 3루수')))


TAILCH = '\n\n야구자판기는 매일 프로야구 이슈를 짧고 정확하게 정리해요.'
YTD = {
 1: dict(desc='기아 외국인 타자 카스트로의 2027 재계약 전망이에요. 카스트로는 2026년 99경기에서 타율 3할 2푼 7리, 21홈런 88타점을 기록했어요.\n카스트로는 2027년에도 기아에 남을까요?\n해럴드 카스트로는 시즌 초 부상으로 한동안 빠졌는데도 기아 첫 시즌에 중심 타선을 지켰고, 플레이오프 1차전에서도 투런 홈런을 포함해 3안타 3타점을 쳤어요. 그런데 2026년 총액은 100만 달러로 외국인 세 명 중 가장 적었어요.\n김도영은 10월 말 인터뷰에서 카스트로가 빨리 계약하면 좋겠다, 너무 고맙다고 했고, 카스트로도 김도영에게 단장님께 말해 달라고 한대요. 이 채널의 예상은 세 명 중 카스트로가 남을 가능성이 가장 크다는 거예요.',
   q='카스트로, 2027년에도 기아에 남을까요? 아니면 떠날까요?',
   tags=['카스트로 재계약', '카스트로', '기아 카스트로', '해럴드 카스트로', '네일', '기아 외국인 선수', '기아 타이거즈', 'KIA 타이거즈', '김도영', '기아 스토브리그', '2027 스토브리그', '프로야구', 'KBO'],
   hashtags=['#카스트로', '#기아타이거즈', '#카스트로재계약', '#김도영', '#스토브리그', '#Shorts']),
 2: dict(desc='기아 외국인 투수 네일의 2027 재계약 전망이에요. 네일은 2026년 31경기에서 13승, 평균자책점 3.49를 남겼고 총액은 200만 달러였어요.\n네일은 2027년에도 기아에 남을까요?\n제임스 네일은 2025년 겨울 메이저리그 구단의 관심이 있었다고 인정했지만 기아에 남아 세 번째 시즌을 보냈어요. 플레이오프 1차전에선 4회까지 1안타로 막다가 헤드샷으로 퇴장당했고, 1승 2패로 몰린 4차전엔 다시 선발로 나서 기아가 4대2로 역전승했어요.\n문제는 몸값이에요. 200만 달러는 외국인 세 명 중 가장 많아 더 올려 주기는 어려워 보여요. 이 채널은 그래도 큰 경기에서 믿는 투수라 기아가 쉽게 놓지는 않을 거라고 봐요.',
   q='네일, 2027년에도 기아에 남을까요? 아니면 떠날까요?',
   tags=['네일 재계약', '네일', '제임스 네일', '기아 네일', '기아 외국인 선수', '기아 타이거즈', 'KIA 타이거즈', '기아 스토브리그', '2027 스토브리그', '프로야구', 'KBO'],
   hashtags=['#네일', '#기아타이거즈', '#네일재계약', '#스토브리그', '#Shorts']),
 3: dict(desc='기아 외국인 투수 올러의 2027 재계약 전망이에요. 올러는 2026년 정규시즌 11승, 평균자책점 3.13으로 두 시즌 연속 두 자릿수 승리를 거뒀어요.\n올러는 2027년에도 기아에 남을까요?\n아담 올러는 플레이오프 대구 두 경기에서 모두 일찍 무너졌어요. 2차전 4와 3분의 2이닝 5실점, 5차전 2이닝 4실점이었어요. 2026년 총액은 120만 달러였어요.\n올러가 몸값을 크게 올려 달라면, 첫해 100만 달러로 묶인 새 외국인 투수가 더 쌀 수 있어요. 이 채널은 세 명 중 한 명만 바뀐다면 올러일 가능성이 가장 크다고 봐요.',
   q='올러, 2027년에도 기아에 남을까요? 아니면 바뀔까요?',
   tags=['올러 재계약', '올러', '아담 올러', '기아 올러', '기아 외국인 선수', '기아 타이거즈', 'KIA 타이거즈', '기아 스토브리그', '2027 스토브리그', '프로야구', 'KBO'],
   hashtags=['#올러', '#기아타이거즈', '#올러재계약', '#스토브리그', '#Shorts']),
 4: dict(desc='기아 외국인 선수 총액 한도로 카스트로, 네일, 올러를 셋 다 잡을 수 있는지 계산해 봤어요. 세 명의 2026년 총액 합계는 420만 달러예요.\n셋 다 재계약하면 한도 안에서 돈이 얼마나 남을까요?\n해럴드 카스트로, 제임스 네일, 아담 올러 세 명의 계약 총액 합계는 400만 달러를 넘을 수 없고, 재계약한 선수가 있으면 연차에 따라 한도가 10만 달러씩 늘어나요. 규정대로 따지면 2026년 한도는 430만 달러였고, 같은 방식으로 계산하면 셋 다 재계약할 때 2027년 한도는 460만 달러예요.\n2026년 총액보다 40만 달러 여유가 생기지만, 카스트로를 150만 달러, 네일을 200만 달러에 붙잡으면 올러에게 남는 돈은 110만 달러로 2026년 총액 120만 달러보다 적어요.',
   q='셋 다 잡아야 할까요? 아니면 한 명은 바꿔야 할까요?',
   tags=['기아 외국인 선수', '기아 외국인 한도', '외국인 선수 샐러리캡', '카스트로', '네일', '올러', '기아 타이거즈', 'KIA 타이거즈', '기아 스토브리그', '2027 스토브리그', '프로야구', 'KBO'],
   hashtags=['#기아외국인선수', '#외국인선수한도', '#기아타이거즈', '#카스트로', '#네일', '#올러', '#Shorts']),
 5: dict(desc='기아 김도영의 메이저리그 도전 시기를 정리했어요. 45홈런으로 홈런왕에 오른 김도영은 빠르면 2028시즌 뒤에 메이저리그에 도전할 수 있어요.\n김도영은 메이저리그에 언제 갈 수 있을까요?\n김도영은 해외 진출 자격이 모자라 2026년 겨울엔 도전할 수 없어요. 병역 문제는 2026 아시안게임 금메달로 풀었고, 메이저리그 여러 구단이 관심을 보인다는 보도도 나왔어요.\n그래서 이 채널은 2027년과 2028년이 김도영과 함께 우승을 노릴 가장 확실한 두 시즌이라고 봐요. 주장 나성범도 2027년이 6년 150억 원 계약의 마지막 해예요.',
   q='김도영은 2028시즌 뒤 메이저리그에 갈까요? 아니면 기아에 남을까요?',
   tags=['김도영 메이저리그', '김도영', '김도영 해외진출', '나성범', '기아 타이거즈', 'KIA 타이거즈', '기아 스토브리그', '2027 스토브리그', '프로야구', 'KBO'],
   hashtags=['#김도영', '#기아타이거즈', '#김도영메이저리그', '#메이저리그', '#Shorts']),
 6: dict(desc='기아 김호령의 FA 이야기예요. 김호령은 플레이오프에서 안타를 치지 못했고, 3차전 삼진 4개 뒤 5차전엔 선발에서 빠졌어요.\n플레이오프 무안타에도 기아는 김호령을 잡아야 할까요?\n2026년 겨울엔 포수 김태군과 중견수 김호령이 FA 자격을 얻을 것으로 보여요. 가을 부진이 김호령의 FA 몸값을 끌어내릴 수도 있어요.\n기아는 2025년 겨울에도 내부 FA 세 명을 다른 팀에 보냈어요. 박찬호는 두산과 4년 80억 원, 최형우는 삼성과 2년 26억 원, 한승택은 KT와 4년 10억 원에 계약했어요. 이 채널은 2026년 겨울 기아의 첫 숙제가 김호령과 김태군을 잡는 거라고 봐요. 중견수와 포수는 영입으로 메우기 어렵거든요.',
   q='김호령, 기아가 붙잡을까요? 아니면 놓칠까요?',
   tags=['김호령 FA', '김호령', '김태군', '기아 FA', '기아 내부 FA', '박찬호', '최형우', '한승택', '기아 타이거즈', 'KIA 타이거즈', '기아 스토브리그', '프로야구', 'KBO'],
   hashtags=['#김호령', '#기아타이거즈', '#FA', '#김태군', '#스토브리그', '#Shorts']),
 7: dict(desc='기아가 2027 신인 드래프트 1라운드 전체 3순위로 뽑은 경남고 내야수 이호민 이야기예요. 이호민은 2026년 고교 20경기에서 타율 4할 2푼, 홈런 2개 19타점을 기록했어요.\n이호민은 이범호 감독급 3루수가 될까요?\n이호민은 청소년 아시아 선수권에서 일본전 홈런과 2루타를 포함해 7타점을 올렸어요. 기아 스카우트는 1년에 한두 명 나올 만한 우타 거포형 재목이라고 했고, 기아 단장도 최근 몇 년 동안 이만한 장타력을 갖춘 고교 선수는 없었다고 했어요.\n김도영이 유격수로 옮기는 것도 검토되고 있어서, 기아는 이호민을 김도영의 뒤를 이을 3루수로 키우려고 해요.',
   q='이호민, 이범호 감독급 3루수가 될까요? 아니면 시간이 더 걸릴까요?',
   tags=['이호민', '이호민 기아', '기아 신인', '2027 신인 드래프트', '기아 1라운드', '경남고 이호민', '김도영', '이범호', '기아 타이거즈', 'KIA 타이거즈', '프로야구', 'KBO'],
   hashtags=['#이호민', '#기아타이거즈', '#신인드래프트', '#김도영', '#Shorts']),
}

out = []
for n, c in enumerate(CUTS, 1):
    lines, scenes, vmap = [], [], []
    for j, (src, d, sc) in enumerate(c['lines']):
        lines.append(d); vmap.append(src)
        if sc is not None:
            sc = copy.deepcopy(sc); sc['startLine'] = j
            if sc['type'] == 'pstat' and sc.get('chain'): sc['chain'] = sc['chain'] + '_' + re.sub(r'\W', '', sc['img'])[-12:]
            if sc.get('cont') and not (scenes and sc.get('chain') and scenes[-1].get('chain') == sc.get('chain')): sc.pop('cont')
            if sc.get('textAt') is None: sc.pop('textAt', None)
            sc.pop('bg', None)
            scenes.append(sc)
    e = {'date': DATE, 'gameDate': DATE, 'series': '야구롱폼', 'vertical': True, 'theme': 'dark', 'railTitle': '', 'focusTeam': 'KIA', 'speed': 1.0, 'ttsApi': True,
         'ttsTempo': ep.get('ttsTempo', 1.2), 'ttsTempoSlow': ep.get('ttsTempoSlow', 1.15), 'rev': f'1103-kia27-cut{n}-v1', 'mascot': False,
         'topic': c['topic'], 'vtitle': c['vtitle'], 'gapScale': 0.6, 'pauseMax': 0.18,
         'voiceFrom': {'ep': '2026-11-02_롱폼2', 'lines': vmap},
         'source': f'롱폼 {SRC} 에서 잘라 세로로 다시 짬(기아 2027 컷 {n}). 사실 출처 = 롱폼 근거(kia27 facts_A·facts_B, 기사 본문 2곳 이상) 그대로.',
         'lines': lines, 'scenes': scenes,
         'youtube': {'title': c['yt']['title'], 'description': YTD[n]['desc'] + TAILCH + '\n' + YTD[n]['q'] + '\n\n전체 이야기는 하단 관련 영상 「기아 2027 스토브리그」에 있어요.', 'tags': YTD[n]['tags'], 'hashtags': YTD[n]['hashtags']}}
    e['youtube']['description'] = e['youtube']['description'].replace('기아', 'KIA 타이거즈(기아)', 1)
    p = os.path.join(OUT, f"{DATE}_롱폼컷{n}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    newc = sum(len(re.sub(r'[\s/,?+]', '', l['narr'])) for s, l in zip(vmap, lines) if s is None and not l['narr'].startswith('채널 구독하고'))
    out.append((n, c['topic'], len(lines), len(scenes), newc))
    for b in (x for l in lines for x in l['narr'].split(' / ')):
        if len(re.sub(r'[\s,?+]', '', b)) > 22: print('호흡 초과', n, b)
for r in out: print(r)
print('새로 합성 합계(구독 멘트 빼고)', sum(r[4] for r in out), '자')
