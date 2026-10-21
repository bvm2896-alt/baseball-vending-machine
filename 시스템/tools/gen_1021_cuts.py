# 10/21 새벽 롱폼 「준PO 3차전 리뷰 · 승부를 가른 이유 · PO 1차전 예상」(episodes/2026-10-20_롱폼2.json) → 컷 쇼츠 5편. 세로(1080x1920).
# 원본 줄은 롱폼 음성 재사용(voiceFrom), 새 줄(훅·질문·관련 영상)만 API 합성. 썸네일은 콘티 thumb(thumb_issue 누끼형) → 빌드 때 영상 폴더에 같이 저장.
# 실행: python -X utf8 tools/gen_1021_cuts.py  → episodes/2026-10-21_롱폼컷1~5.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-20_롱폼2.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
TH = '상황별/썸네일_롱폼22_준PO3'
DATE = '2026-10-21'

def wrap16(s, n=16):
    if '\n' in s or len(s) <= n: return s
    w = s.split(' '); best = None
    for k in range(1, len(w)):
        a, b = ' '.join(w[:k]), ' '.join(w[k:])
        sc = max(len(a), len(b))
        if re.match(r'^(게|것|수|억|원|점|개|번|명|위|년|월|일|경기|타점|홈런|세이브|타석|이닝)', b) or re.search(r'\d$', a): sc += 20
        if len(a) > n or len(b) > n: sc += 5
        if best is None or sc < best[0]: best = (sc, a + '\n' + b)
    return best[1]

def NEW(narr, sub, scene, slow=False):
    pcs = [wrap16(x + ('?' if re.search(r'(까요|나요)$', x) else '')) for x in sub.split('|')]
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

POINT = lambda: NEW('준플레이오프 이차전 리뷰와 / 삼차전 예측 전체는 / 하단 관련 영상에 있어요', '준플레이오프 2차전 리뷰와|3차전 예측 전체는|하단 관련 영상에 있어요',
                    {"type": "photo", "img": TH, "fit": "cover", "text": "", "relArrow": True, "chain": "relvid"})   # 10/19: 다음 구독 장면과 한 묶음 — 썸네일이 사라지지 않게
CTA = lambda: OLD(96, {"type": "photo", "img": TH, "fit": "cover", "text": "", "chain": "relvid"})
YT_TAIL = '\n준플레이오프 2차전 리뷰와 3차전 예측 전체는 하단 관련 영상에 있어요.'
REC = '기록: KBO 게임센터 준플레이오프 2차전 박스스코어, KBO 기록실(2026 정규시즌). 발언: 스포츠경향, 스포츠월드, 뉴스핌, 뉴스엔, 머니투데이, 일간스포츠, SPOTV'
CRED = 'KIA 타이거즈 제공, LG 트윈스 제공, MK스포츠, 스포츠조선, 스타뉴스, 스포츠경향, 연합뉴스, 스포티비뉴스, 엑스포츠뉴스(롱폼 썸네일)'
QFINAL = lambda: Qs('삼차전 / 엘지가 잠실에서 반격할까요? / 기아가 삼연승으로 끝낼까요?', '3차전|LG가 잠실에서 반격할까요|KIA가 3연승으로 끝낼까요', '3차전\nLG 반격? KIA 3연승?', logos=['LG', 'KIA'])
POINT = lambda: NEW('준플레이오프 삼차전 리뷰와 / 플레이오프 일차전 예상 전체는 / 하단 관련 영상에 있어요', '준플레이오프 3차전 리뷰와|플레이오프 1차전 예상 전체는|하단 관련 영상에 있어요',
                    {"type": "photo", "img": TH, "fit": "cover", "text": "", "relArrow": True, "chain": "relvid"})
CTA = lambda: OLD(78, {"type": "photo", "img": TH, "fit": "cover", "text": "", "chain": "relvid", "cont": True})
YT_TAIL = '\n준플레이오프 3차전 리뷰와 플레이오프 1차전 예상 전체는 하단 관련 영상에 있어요.'
REC = '기록: KBO 게임센터 박스스코어·기록실(10월 20일 조회). 분석: 야구공작소 카라스코 스카우팅 리포트. 기사: 일간스포츠·머니투데이·OSEN·스포츠경향·국민일보·연합뉴스·뉴스핌·스포츠월드·뉴스1·MHN·뉴시스(10/20 전후)'
CRED = '연합뉴스, 일간스포츠, 머니투데이, KIA 타이거즈 제공, LG 트윈스 제공, 삼성 라이온즈 제공'
TB = dict(halo=18, cutout=True, cutoutCrop=0.6, cutoutLift=180, cutoutOverlap=330, cutoutFade=0.62, ph=1000, logos=False, noPills=True, top='', perLine=True)
def TH_(img, big, color, teams, **kw):
    t = dict(TB); t.update(img=img, big=big, color=color, teams=teams); t.update(kw); return t
QPO = lambda: Qs('플레이오프 / 기아가 올라갈까요? / 삼성이 올라갈까요?', '플레이오프|KIA가 올라갈까요|삼성이 올라갈까요', '플레이오프\nKIA? 삼성?', logos=['KIA', '삼성'])
CUTS = []

# ── 1 3차전 리뷰: KIA 13-1, 2회 7점 ─────────────────
CUTS.append(dict(topic='준PO3차전KIA13대1', vtitle=['준PO 3차전', 'KIA 13-1 LG'],
  lines=[OLD(0), OLD(4), OLD(7), OLD(8), OLD(9), OLD(11), OLD(13), OLD(21), QPO(), POINT(), CTA()],
  thumb=TH_('누끼/경기_김도영_45호_포효_1012_스포츠조선_center_mid', 'KIA 13-1 LG\n준PO 3연승', '#D6002A', ['KIA']),
  yt=dict(title='준플레이오프 3차전 | KIA 13-1 LG, 2회에만 7점 3연승 통과 #KIA타이거즈 #준플레이오프',
    desc='KIA 타이거즈가 준플레이오프 3차전에서 LG 트윈스를 13대1로 꺾고 3연승으로 준플레이오프를 통과했어요.\n2회초 나성범의 솔로 홈런으로 앞서간 뒤 실책·안타·볼넷으로 만든 만루에서 박정우가 적시타를 쳤고, LG 선발 카라스코는 1⅓이닝 5실점으로 내려갔어요. 이어진 1사 만루에서 김도영이 비거리 145m 만루 홈런을 쳐 2회에만 7점이 났어요. KIA는 안타 16개를 쳤고 선발 타자 9명이 모두 안타와 득점을 기록했어요.\n\n플레이오프, KIA가 올라갈까요? 삼성이 올라갈까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['준플레이오프 3차전', '준플레이오프', 'KIA LG', 'KIA 타이거즈', 'LG 트윈스', '김도영', '나성범', '카라스코', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#준플레이오프', '#KIA타이거즈', '#LG트윈스', '#김도영', '#가을야구', '#야구자판기'])))

# ── 2 김도영 안타 3개 전부 홈런 ───────────────────────
CUTS.append(dict(topic='김도영안타3개전부홈런', vtitle=['김도영 안타 3개', '전부 홈런'],
  lines=[OLD(14, ppx(14)), OLD(11), OLD(12), OLD(13), OLD(15),
    Qs('플레이오프에서도 / 김도영 홈런이 터질까요? / 삼성이 막을까요?', '플레이오프에서도|김도영 홈런이 터질까요|삼성이 막을까요', '플레이오프\n김도영 홈런? 삼성이 막는다?', faces=['P22_김도영_만루포환호']),
    POINT(), CTA()],
  thumb=TH_('누끼/경기_김도영_박수포효_one_mid', '김도영 안타 3개\n전부 홈런', '#1D4ED8', ['KIA']),
  yt=dict(title='김도영 준플레이오프 MVP | 9타수 3안타, 안타 3개가 모두 홈런 #김도영 #KIA타이거즈',
    desc='KIA 타이거즈 김도영이 준플레이오프 3경기에서 9타수 3안타를 쳤는데, 안타 3개가 모두 홈런이었어요. 8타점으로 준플레이오프 MVP에 뽑혔어요.\n3차전 2회 1사 만루에서는 케네디의 직구를 받아쳐 비거리 145m 만루 홈런을 쳤어요. 준플레이오프 역대 가장 긴 홈런이고, 포스트시즌 최장 타이 기록이에요. 23살 18일로 포스트시즌 최연소 만루 홈런 기록도 세웠어요. 김도영은 경기 뒤 손맛은 오늘이 더 좋았다고 했어요.\n\n플레이오프에서도 김도영 홈런이 터질까요? 삼성이 막을까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['김도영', '김도영 홈런', '김도영 만루홈런', '준플레이오프 MVP', '준플레이오프 3차전', 'KIA 타이거즈', '준플레이오프', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#김도영', '#KIA타이거즈', '#준플레이오프', '#가을야구', '#프로야구', '#야구자판기'])))

# ── 3 카라스코가 무너진 이유: 왼손 타자 7명 ─────────────
CUTS.append(dict(topic='카라스코왼손타자7명', vtitle=['카라스코가 무너진 이유', '왼손 타자 7명'],
  lines=[NEW('메이저리그 백십이 승 투수 카라스코가 / 이회도 못 버틴 이유, / 왼손 타자 일곱 명이었어요', '메이저리그 112승 투수 카라스코가|2회도 못 버틴 이유|왼손 타자 7명이었어요', ppx(5)),
    OLD(6), OLD(36), OLD(37), OLD(38), OLD(39), OLD(40), OLD(41), OLD(42),
    Qs('왼손 라인업, / 플레이오프에서도 통할까요? / 삼성은 다를까요?', '왼손 라인업|플레이오프에서도 통할까요|삼성은 다를까요', '왼손 라인업\n삼성에도 통할까?', logos=['KIA', '삼성']),
    POINT(), CTA()],
  thumb=TH_('카드/P15_카라스코_WC', '카라스코 강판\n왼손 타자 7명', '#7C3AED', ['LG'], cutoutCrop=0.85),
  yt=dict(title='카라스코 1⅓이닝 강판 이유 | KIA 왼손 타자 7명, 체인지업이 안 휘었다 #카라스코 #준플레이오프',
    desc='LG 트윈스 카라스코가 준플레이오프 3차전에서 1⅓이닝 5실점으로 강판됐어요. KIA 이범호 감독은 김도영과 김선빈을 뺀 선발 타자 7명을 모두 왼손 타자로 채웠어요.\n카라스코는 올해 KBO 피안타율이 오른손 타자 상대 1할 8푼 5리, 왼손 타자 상대 2할 6푼 7리였어요. 야구공작소 분석에 따르면 카라스코의 체인지업은 메이저리그 평균보다 옆으로 약 16cm 덜 휘어 왼손 타자의 스윙 궤적 안에 머물렀어요. KBO 입단 전 기록이라 표본은 적지만 체인지업 헛스윙률이 오른손 타자 상대 42.9%, 왼손 타자 상대 11.1%였어요.\n\n왼손 라인업, 플레이오프에서도 통할까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['카라스코', '카라스코 체인지업', '왼손 타자', 'KIA 라인업', '이범호', '준플레이오프 3차전', 'LG 트윈스', 'KIA 타이거즈', '준플레이오프', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#카라스코', '#LG트윈스', '#KIA타이거즈', '#준플레이오프', '#프로야구', '#야구자판기'])))

# ── 4 KIA 첫 준PO 통과 · 잠실의 마지막 밤 ─────────────
CUTS.append(dict(topic='KIA첫준PO통과잠실마지막', vtitle=['KIA 첫 준PO 통과', '잠실의 마지막 밤'],
  lines=[NEW('기아가 구단 역사상 처음으로 / 준플레이오프를 통과했어요', 'KIA가 구단 역사상 처음으로|준플레이오프를 통과했어요', ppx(1)),
    OLD(27), OLD(28), OLD(29), OLD(30), OLD(33), OLD(34),
    Qs('기아의 가을, / 한국시리즈까지 갈까요? / 플레이오프에서 멈출까요?', 'KIA의 가을|한국시리즈까지 갈까요|플레이오프에서 멈출까요', 'KIA의 가을\n한국시리즈까지?', logos=['KIA']),
    POINT(), CTA()],
  thumb=TH_('누끼/KBO스타일_경기_네일_주먹환호_KIA제공_center_mid', 'KIA 첫 준PO 통과\n37년 만에 승리', '#059669', ['KIA']),
  yt=dict(title='KIA 구단 첫 준플레이오프 통과 | 37년 만의 시리즈 승리, 잠실의 마지막 경기 #KIA타이거즈 #잠실야구장',
    desc='KIA 타이거즈가 해태 시절까지 합쳐 구단 역사상 처음으로 준플레이오프를 통과했어요. 그동안 1994년·2004년·2006년·2011년 네 번 올라 네 번 모두 떨어졌었어요.\n한국시리즈를 뺀 시리즈 승리는 1989년 플레이오프 이후 37년 만이고, 준플레이오프 3연승 통과는 2008년 삼성, 2023년 NC에 이어 역대 세 번째예요.\nLG에겐 쓰린 마지막이었어요. 2만 3650명이 꽉 찬 잠실에서 시즌을 마쳤고, 1982년 문을 연 잠실야구장은 올 시즌이 끝나면 철거돼요.\n\nKIA의 가을, 한국시리즈까지 갈까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['KIA 준플레이오프', 'KIA 타이거즈', '잠실야구장', '잠실야구장 철거', 'LG 트윈스', '준플레이오프 3차전', '준플레이오프', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#KIA타이거즈', '#잠실야구장', '#LG트윈스', '#준플레이오프', '#가을야구', '#야구자판기'])))

# ── 5 PO 1차전 예상: 네일 vs 후라도 ───────────────────
CUTS.append(dict(topic='PO1차전예상네일후라도', vtitle=['PO 1차전 예상', '네일 vs 후라도'],
  lines=[OLD(50), OLD(53), OLD(54), OLD(62), OLD(63), OLD(64), OLD(65), OLD(74),
    Qs('플레이오프 일차전 / 기아가 이길까요? / 삼성이 이길까요?', '플레이오프 1차전|KIA가 이길까요|삼성이 이길까요', '플레이오프 1차전\nKIA? 삼성?', logos=['KIA', '삼성']),
    POINT(), CTA()],
  thumb=TH_('누끼/경기_네일_주먹_1009NC_KIA제공_mid', '네일 vs 후라도\nPO 1차전 승자는?', '#EA580C', ['KIA', '삼성']),
  yt=dict(title='플레이오프 1차전 예상 | 네일 vs 후라도, 10월 25일 대구 #플레이오프 #KIA타이거즈',
    desc='KIA 타이거즈와 삼성 라이온즈의 플레이오프 1차전은 10월 25일 일요일 오후 2시 대구에서 열려요. 올해 맞대결은 KIA가 9승 7패로 앞섰고, 김도영은 삼성전 16경기에서 홈런 9개를 쳤어요.\n공식 선발 발표 전이지만 KIA는 1차전 네일, 2차전 올러를 낼 계획으로 알려졌어요. 네일은 7일을 쉬고 나오고 올해 삼성전 4경기 평균자책점은 3.24예요. 삼성 1차전 선발은 후라도로 예상해요. 후라도는 19일 청백전에서 공 90개로 5이닝 1실점했어요.\n이 채널의 예상은 1차전 KIA예요.\n\n플레이오프 1차전, KIA가 이길까요? 삼성이 이길까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['플레이오프 1차전', '플레이오프', 'KIA 삼성', '네일', '후라도', '김도영', 'KIA 타이거즈', '삼성 라이온즈', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#플레이오프', '#KIA타이거즈', '#삼성라이온즈', '#네일', '#가을야구', '#야구자판기'])))

out = []
for n, c in enumerate(CUTS, 1):
    lines, scenes, vmap = [], [], []; prev0 = None
    for j, (src, d, sc) in enumerate(c['lines']):
        lines.append(d); vmap.append(src)
        if sc is not None:
            o0 = sc.get('startLine'); sc = dict(sc); sc['startLine'] = j
            same = bool(scenes) and sc.get('chain') and scenes[-1].get('chain') == sc.get('chain')
            if sc.get('cont') and not same and not (j and src is not None and (vmap[j - 1] == src - 1 or prev0 == src - 1)): sc.pop('cont')
            if same and not sc.get('cont'): sc['cont'] = True   # 같은 사진이 이어지면 사진 고정, 글만 바뀜
            prev0 = o0
            scenes.append(sc)
    e = {
        'date': DATE, 'gameDate': '2026-10-20', 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': ep.get('ttsTempo', 1.25), 'ttsTempoSlow': ep.get('ttsTempoSlow', 1.2),
        'rev': f'1021-cut{n}-v1', 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': '2026-10-20_롱폼2', 'lines': vmap},
        'source': f'롱폼 {SRC} 에서 잘라 세로로 다시 짬(컷 {n}). ' + ep.get('source', ''),
        'lines': lines, 'scenes': scenes,
        'thumb': c['thumb'],
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'] + f"\n\n{REC}\n사진: {CRED}", 'tags': c['yt']['tags'], 'hashtags': c['yt']['hashtags']},
    }
    p = os.path.join(HERE, 'episodes', f"{DATE}_롱폼컷{n}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    est = sum(len(l['narr'].replace(' / ', ' ')) * 0.14 + 0.3 * 0.6 * l['narr'].count(' / ') + 0.45 * 0.6 for l in lines) + 1.0
    newc = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for s, l in zip(vmap, lines) if s is None)
    out.append((n, c['topic'], len(lines), len(scenes), round(est), newc))
    for b in (x for l in lines for x in l['narr'].split(' / ')):
        if len(re.sub(r'[\s,?+]', '', b)) > 22: print('호흡 초과', n, b)
for r in out: print(r)
print('새로 합성 합계(구독 멘트 빼고)', sum(r[5] for r in out), '자')
