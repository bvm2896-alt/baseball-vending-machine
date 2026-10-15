# 10/15 롱폼⑮(준플레이오프 예측 + 와일드카드 리뷰) → 컷 쇼츠 5편. 세로(1080x1920) — template_long_v.
# 원본 줄은 롱폼 음성을 그대로 쓰고(build.py prep 이 voiceFrom 으로 복사 — .tempo 도), 새 줄(훅·질문·관련 영상)만 API 합성.
# 준플레이오프 1차전이 10/17 광주라 컷은 전부 10/16 업로드(date). 같은 날 제목 앞 검색어가 겹치지 않게 앞머리를 다르게 둠
#   (와일드카드 / 김도영 / 톨허스트 vs 네일 / 전상현 / KIA vs LG).
# ※ 46·55·62 번 줄은 '10월 15일까지 발표·결정되지 않았다'는 말 — 올리기 전에 선발 발표·손주영 합류를 다시 확인하고 바뀌었으면 그 줄을 고친다.
# 실행: python -X utf8 tools/gen_1015_cuts.py  → episodes/2026-10-16_롱폼컷1~5.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-15_롱폼.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
TH = '상황별/썸네일_롱폼15_준PO'   # 롱폼⑮ 실제 썸네일
DATE = '2026-10-16'

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
    pcs = [wrap16(x + ('?' if re.search(r'(까요|나요)$', x) else '')) for x in sub.split('|')]   # 10/15 사용자: 질문 자막에 물음표
    assert len(pcs) == len(narr.split(' / ')), (narr, sub)
    d = {'narr': narr, 'sub': '|'.join(pcs)}
    if slow: d['pace'] = 'slow'
    return (None, d, scene)

def OLD(i, scene=None):
    d = copy.deepcopy(LN[i]); d.pop('gapAfter', None)
    sc = copy.deepcopy(scene if scene is not None else SCN.get(i))
    return (i, d, sc)

def ppx(i, **kw):
    s = copy.deepcopy(SCN[i]); [s.pop(k, None) for k in ('chain', 'cont')]; s.update(kw); return s

def Qs(narr, sub, text, faces=None, logos=None):
    sc = {"type": "question", "text": text}
    if faces: sc["faces"] = ['카드/' + x for x in faces]
    if logos: sc["logos"] = logos
    return NEW(narr, sub, sc, slow=True)

POINT = lambda: NEW('기아와 엘지 준플레이오프 예측 전체는 / 하단 관련 영상에 있어요', 'KIA와 LG 준플레이오프 예측 전체는|하단 관련 영상에 있어요',
                    {"type": "photo", "img": TH, "fit": "cover", "text": "", "relArrow": True})
CTA = lambda: OLD(85, {"type": "photo", "img": TH, "fit": "cover", "text": ""})
YT_TAIL = '\nKIA와 LG 준플레이오프 예측 전체는 하단 관련 영상에 있어요.'
REC = '기록: KBO 기록실(2026 정규시즌 최종 기록, 투수 vs 타자, 팀간 승패, 와일드카드 박스스코어)'
CUTS = []

# ── 1 와일드카드 리뷰 ───────────────────────────────────
CUTS.append(dict(topic='와일드카드리뷰LG4대1두산', vtitle=['와일드카드 결정전', 'LG 4-1 두산'],
  lines=[
    NEW('엘지가 두산을 사 대 일로 꺾고 / 준플레이오프에 올라갔어요', 'LG가 두산을 4대1로 꺾고|준플레이오프에 올라갔어요', ppx(1)),
    OLD(6), OLD(8), OLD(9), OLD(14), OLD(16), OLD(17), OLD(18), OLD(19),
    NEW('팔 회말엔 신민재의 스퀴즈와 / 이영하의 폭투 두 개로 / 사 대 일이 됐어요', '8회말엔 신민재의 스퀴즈와|이영하의 폭투 두 개로|4대1이 됐어요', ppx(26, labelAt=99)),
    Qs('이날 엘지의 영웅은 / 오스틴일까요? / 박해민일까요?', '이날 LG의 영웅은|오스틴일까요|박해민일까요', '와일드카드 영웅\n오스틴? 박해민?', ['P15_오스틴_WC', 'P15_박해민_WC']),
    POINT(), CTA()],
  yt=dict(title='와일드카드 결정전 리뷰 | LG 4-1 두산, 오스틴 결승 홈런·박해민 워닝트랙 캐치 #LG트윈스 #와일드카드',
    desc='2026 프로야구 와일드카드 결정전에서 LG 트윈스가 두산 베어스를 4대1로 꺾고 준플레이오프에 올라갔어요. 10월 14일 잠실, 정규시즌 4위 LG는 1승을 안고 시작해 한 경기 만에 끝냈어요.\n1회말 1사 1루에서 오스틴이 곽빈의 커브를 받아쳐 왼쪽 담장을 넘긴 2점 홈런이 결승타였어요.\n\n두산 곽빈은 2회 무사 만루에서 홍창기·박해민·오스틴을 세 타자 연속 삼진으로 잡는 등 6이닝 동안 삼진 10개를 잡아 와일드카드 한 경기 최다 탈삼진 타이 기록을 세웠어요. 7회초 두산은 무사 2·3루에서 1사 만루까지 만들었고, 대타 양석환의 우중간 깊은 타구를 중견수 박해민이 워닝트랙에서 잡아내 1점만 주고 2대1 리드를 지켰어요. 8회말 LG는 신민재의 스퀴즈 번트와 이영하의 폭투 두 개로 4대1을 만들었고, 9회는 김강률이 세 타자로 끝냈어요.\n\n이날 LG의 영웅은 오스틴일까요? 박해민일까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['와일드카드 결정전', '와일드카드', 'LG 두산', 'LG 트윈스', '두산 베어스', '오스틴', '박해민', '곽빈', '신민재', '준플레이오프', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#와일드카드', '#LG트윈스', '#두산베어스', '#오스틴', '#프로야구', '#야구자판기']),
  credit='LG 트윈스 제공, 두산 베어스 제공, KIA 타이거즈 제공, 스포츠서울·스타뉴스(롱폼 썸네일)'))

# ── 2 김도영 LG전 ───────────────────────────────────────
CUTS.append(dict(topic='김도영LG전7연승', vtitle=['김도영 LG전', '타율은 낮은데…'],
  lines=[
    NEW('엘지는 기아에 / 일곱 경기 연속 졌어요', 'LG는 KIA에|일곱 경기 연속 졌어요', ppx(2, games=SCN[2]['games'][9:], rows=[[0, 6]], dimTo=0, groups=[dict(SCN[2]['groups'][0], **{'from': 0, 'to': 6}, at=0.5)])),
    OLD(32), OLD(33), OLD(34), OLD(35), OLD(36), OLD(37), OLD(38),
    Qs('준플레이오프에서도 김도영이 / 엘지 마운드를 넘을까요? / 막힐까요?', '준플레이오프에서도 김도영이|LG 마운드를 넘을까요|막힐까요', '김도영\n넘을까? 막힐까?', ['김도영_MVP_41호']),
    POINT(), CTA()],
  yt=dict(title='김도영 LG전 | 타율 2할 8리인데 홈런 4개, LG전 결승포 두 방 #KIA타이거즈 #김도영',
    desc='KIA 타이거즈 김도영은 LG 트윈스를 상대로 타율이 낮았어요. 2026 정규시즌 LG전 48타수 10안타, 타율 0.208이에요.\n그런데 그 10안타 중 4개가 홈런이었고 볼넷을 12개 골랐어요. 10월 5일엔 9회 2사 후 역전 3점 홈런, 10월 12일엔 8회 결승 2점 홈런을 쳤어요. KIA는 6월 17일부터 LG전 7경기를 내리 이겼어요.\n\nLG 오스틴도 비슷해요. 41홈런 타자지만 KIA전 타율은 0.228, 홈런은 4개였어요. 타점은 김도영 12개, 오스틴 8개예요. 염경엽 감독은 결정적일 때마다 김도영에게 맞았다며 이번 준플레이오프의 초점은 김도영을 막는 거라고 했어요.\n\n준플레이오프에서도 김도영이 LG 마운드를 넘을까요? 막힐까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['김도영', '김도영 LG', '김도영 홈런', 'KIA 타이거즈', '기아 타이거즈', 'LG 트윈스', '오스틴', '염경엽', '준플레이오프', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#김도영', '#KIA타이거즈', '#LG트윈스', '#준플레이오프', '#프로야구', '#야구자판기']),
  credit='KIA 타이거즈 제공, LG 트윈스 제공, 스포츠서울·스타뉴스(롱폼 썸네일)'))

# ── 3 1차전 선발 톨허스트 vs 네일 ───────────────────────
CUTS.append(dict(topic='톨허스트네일1차전선발', vtitle=['준플레이오프 1차전', '톨허스트 vs 네일'],
  lines=[
    NEW('준플레이오프 일 차전 / 톨허스트와 네일이 / 맞붙을 가능성이 커요', '준플레이오프 1차전|톨허스트와 네일이|맞붙을 가능성이 커요',
        {"type": "duel", "left": {"team": "LG", "img": "카드/FA9_톨허스트_상체", "name": "톨허스트", "role": "LG 선발", "at": 1}, "right": {"team": "KIA", "img": "카드/FA9_네일", "name": "네일", "role": "KIA 선발", "at": 1}, "vsAt": 1.5}),
    OLD(43), OLD(44), OLD(45), OLD(46), OLD(47), OLD(48), OLD(49),
    Qs('일 차전 승리 투수는 / 톨허스트일까요? / 네일일까요?', '1차전 승리 투수는|톨허스트일까요|네일일까요', '1차전 승리 투수\n톨허스트? 네일?', ['FA9원_톨허스트', 'FA9원_네일']),
    POINT(), CTA()],
  yt=dict(title='톨허스트 vs 네일 | 준플레이오프 1차전 유력 선발, KIA전 평균자책점 6.20 vs LG전 4.58 #준플레이오프 #톨허스트',
    desc='KIA와 LG의 준플레이오프 1차전 선발은 LG 톨허스트와 KIA 네일이 유력해요. 톨허스트는 와일드카드 직후 염경엽 감독이 1차전 선발로 밝혔고, KIA 1차전 선발은 10월 15일까지 발표되지 않았어요.\n톨허스트는 2026년 12승, 평균자책점 4.24예요. KIA전 다섯 경기 평균자책점은 6.20, 피안타율은 0.307이었어요. 다만 시즌 첫 KIA전 7실점이 컸고, 5월엔 1회에 퇴장당한 경기도 있었어요. 정상적으로 던진 나머지 세 경기는 17이닝 6실점이에요.\n\n네일은 정규시즌 183이닝으로 리그에서 가장 많이 던졌고 9월 이후 평균자책점은 2.76이에요. 다만 LG전 세 경기 평균자책점은 4.58이었어요. 9월 이후만 보면 톨허스트도 3.60이라 1차전은 팽팽한 경기로 봤어요.\n\n1차전 승리 투수는 톨허스트일까요? 네일일까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['톨허스트', '네일', '준플레이오프 1차전', '준플레이오프 선발', 'KIA LG', 'KIA 타이거즈', 'LG 트윈스', '준플레이오프', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#준플레이오프', '#톨허스트', '#네일', '#KIA타이거즈', '#LG트윈스', '#야구자판기']),
  credit='구단 공식 선수 프로필(KIA 타이거즈·LG 트윈스), 썸네일 엑스포츠뉴스·스포츠조선, 스포츠서울·스타뉴스(롱폼 썸네일)'))

# ── 4 뒷문 전상현 vs LG 마무리 공백 ─────────────────────
CUTS.append(dict(topic='전상현손주영뒷문', vtitle=['준플레이오프 뒷문', 'KIA vs LG'],
  lines=[
    NEW('준플레이오프는 뒷문 싸움이에요 / 기아엔 십 월 무피안타 전상현 / 엘지는 마무리가 불투명해요', '준플레이오프는 뒷문 싸움이에요|KIA엔 10월 무피안타 전상현|LG는 마무리가 불투명해요',
        {"type": "duel", "left": {"team": "KIA", "img": "카드/P15_전상현", "name": "전상현", "role": "10월 피안타 0", "at": 1}, "right": {"team": "LG", "img": "카드/R13_손주영_포효", "name": "손주영", "role": "합류 미정", "at": 2}, "vsAt": 1.5}),
    OLD(60), OLD(61), OLD(62), OLD(63), OLD(64),
    Qs('준플레이오프 뒷문은 / 기아가 셀까요? / 엘지가 셀까요?', '준플레이오프 뒷문은|KIA가 셀까요|LG가 셀까요', '뒷문 싸움\nKIA? LG?', logos=['KIA', 'LG']),
    POINT(), CTA()],
  yt=dict(title='전상현 10월 무피안타 | 준플레이오프 뒷문, LG는 손주영 합류 미정·유영찬 수술 #준플레이오프 #전상현',
    desc='KIA와 LG의 준플레이오프는 뒷문 싸움이에요. 두 팀 모두 2026 정규시즌 블론세이브가 22개로 뒷문이 불안했던 팀이에요.\n그런데 10월엔 KIA 마무리 전상현이 6경기 8과 3분의 2이닝 동안 안타를 하나도 맞지 않았어요. 올 시즌 오스틴과 문보경 등 LG 타자 11명은 전상현을 상대로 합쳐서 21타수 1안타였어요.\n\nLG는 선발에서 마무리로 옮겨 31세이브를 올린 손주영이 목 부상으로 준플레이오프 합류가 10월 15일까지 정해지지 않았고, 유영찬은 팔꿈치 수술로 시즌을 마쳤어요. 그래서 와일드카드에선 케네디·김진수·이우찬·김강률 네 명이 3이닝을 나눠 막았어요. 다섯 경기를 이렇게 버틸 수 있을지가 관건이에요.\n\n준플레이오프 뒷문은 KIA가 셀까요? LG가 셀까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['전상현', '손주영', '유영찬', 'KIA 마무리', 'LG 마무리', '블론세이브', 'KIA 타이거즈', 'LG 트윈스', '준플레이오프', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#전상현', '#준플레이오프', '#KIA타이거즈', '#LG트윈스', '#프로야구', '#야구자판기']),
  credit='KIA 타이거즈 제공, LG 트윈스 제공, 스포츠서울·스타뉴스(롱폼 썸네일)'))

# ── 5 예측 KIA 3승 1패 ──────────────────────────────────
# 10/15 사용자 "3승 1패가 몇 개 써져 있는 거야 — 파란색 텍스트 둘 다 지워": 위 제목 둘째 줄과 3:1 장면 아래 큰 글씨를 뺀다(3:1 숫자판만)
CUTS.append(dict(topic='준플레이오프예측KIA3승1패', vtitle=['KIA vs LG'],
  lines=[
    OLD(0), OLD(75), OLD(76), OLD(77), OLD(78), OLD(79), OLD(80, {k: v for k, v in SCN[80].items() if k not in ('text', 'size')}), OLD(81), OLD(82), OLD(84),
    POINT(), CTA()],
  yt=dict(title='KIA vs LG 준플레이오프 | 야구자판기 예상은 KIA 3승 1패, 근거 다섯 가지 #KIA타이거즈 #LG트윈스',
    desc='KIA 타이거즈와 LG 트윈스의 준플레이오프, 야구자판기 예상은 KIA 3승 1패예요.\n2026 정규시즌 상대 전적은 KIA가 9승 7패로 앞서고 최근 일곱 경기도 KIA가 다 이겼어요. 1차전은 반반으로 봤고, 2차전은 올러가 나서면 KIA가 앞서요. 뒷문은 마무리 손주영의 합류가 불투명한 LG가 더 불안하고, 1·2·5차전이 열리는 광주에서 KIA는 LG를 상대로 5승 2패였어요. LG 쪽엔 2025년 우승 경험과 와일드카드 기세가 있어요.\n\n잠실 맞대결은 LG가 5승 4패로 앞섰지만 최근 세 경기는 KIA가 다 이겼어요. 그래도 LG는 홈에서 5할 넘게 이긴 팀이라 잠실 3·4차전 중 한 경기는 LG가 가져갈 수 있다고 봤어요. 다만 LG가 1차전을 잡으면 이야기가 달라져요.\n\n준플레이오프를 통과할 팀은 KIA일까요? LG일까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['준플레이오프', '준플레이오프 예측', 'KIA LG', 'KIA 타이거즈', 'LG 트윈스', '가을야구', '포스트시즌', '프로야구 포스트시즌', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#준플레이오프', '#KIA타이거즈', '#LG트윈스', '#가을야구', '#프로야구', '#야구자판기']),
  credit='KIA 타이거즈 제공, LG 트윈스 제공, 썸네일 뉴스1, 스포츠서울·스타뉴스(롱폼 썸네일)'))

THUMBS = {}
THUMB_FILE = os.path.join(HERE, 'tools', 'thumb_1015_cuts.json')
if os.path.exists(THUMB_FILE): THUMBS = {int(k): v for k, v in json.load(io.open(THUMB_FILE, encoding='utf-8')).items()}

out = []
for n, c in enumerate(CUTS, 1):
    lines, scenes, vmap = [], [], []; prev0 = None
    for j, (src, d, sc) in enumerate(c['lines']):
        lines.append(d); vmap.append(src)
        if sc is not None:
            o0 = sc.get('startLine'); sc = dict(sc); sc['startLine'] = j
            if sc.get('cont') and not (j and src is not None and (vmap[j - 1] == src - 1 or prev0 == src - 1)): sc.pop('cont')
            prev0 = o0
            scenes.append(sc)
    t = THUMBS.get(n)
    e = {
        'date': DATE, 'gameDate': '2026-10-14', 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': 1.2, 'ttsTempoSlow': 1.15,
        'rev': f'1015-cut{n}-v1' + ('-b' if n == 5 else ''), 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': '2026-10-15_롱폼', 'lines': vmap},
        'source': f'롱폼 {SRC} 에서 잘라 세로로 다시 짬(컷 {n}). ' + ep.get('source', ''),
        'lines': lines, 'scenes': scenes,
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'] + f"\n\n{REC}\n사진: {c['credit']}", 'tags': c['yt']['tags'], 'hashtags': c['yt']['hashtags']},
    }
    if t: e['thumb'] = t
    p = os.path.join(HERE, 'episodes', f"{DATE}_롱폼컷{n}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    est = sum(len(l['narr'].replace(' / ', ' ')) * 0.15 + 0.3 * 0.6 * l['narr'].count(' / ') + 0.45 * 0.6 for l in lines) + 1.0
    newc = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for s, l in zip(vmap, lines) if s is None)
    out.append((n, c['topic'], len(lines), len(scenes), round(est), newc, 'thumb' if t else '-'))
    for b in (x for l in lines for x in l['narr'].split(' / ')):
        if len(re.sub(r'[\s,?+]', '', b)) > 22: print('호흡 초과', n, b)
for r in out: print(r)
print('새로 합성 합계(구독 멘트 빼고)', sum(r[5] for r in out), '자')
