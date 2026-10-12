# 10/8 밤 롱폼⑨(KBO 외국인 선수 재계약 10개 구단) → 컷 쇼츠 11편(사용자 "11편, 규칙 편 추가"). 세로(1080x1920) — template_long_v.
# 원본 줄은 롱폼 음성을 그대로 쓰고(build.py prep 이 voiceFrom 으로 복사, 대사가 같은 줄만 — .tempo 도 복사),
# 새 줄(훅·질문·관련 영상·롱폼 연결어를 고친 줄)만 API 합성. 롱폼 줄의 pace(slow=1.15배)는 그대로 둔다(배속이 달라지면 다시 합성되므로).
# 쇼츠 규칙(10/8): 처음 나오는 사람은 한 마디로 소개 / 판단은 '제 생각엔' / 롱폼 연결어("처음에 말한", "여기까지가", "~와 달리")는 고쳐 새로 녹음 /
#   10팀 칸(tiers) 장면은 그 팀 장면으로 / 마지막 질문은 롱폼과 같은 틀(사용자 문구)을 팀 이름으로 / 관련 영상 줄 = 롱폼 실제 썸네일 + relArrow.
# 실행: python -X utf8 tools/gen_1008_cuts.py  → episodes/2026-10-08_롱폼컷1~11.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-08_롱폼.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
TH = '상황별/썸네일_롱폼9_외인재계약'   # 롱폼⑨ 실제 업로드 썸네일(포스터 v4)
E = lambda n: '카드/FA9끝_' + n          # 얼굴 원(롱폼 마지막 장면과 같은 것)
TEAM4 = {'KT': ['로건', '대니엘', '힐리어드', '스기모토'], '삼성': ['후라도', '페덱', '디아즈', '미야모리'], 'KIA': ['네일', '올러', '카스트로', '시라카와'],
         'LG': ['톨허스트', '카라스코', '오스틴', '케네디'], '두산': ['벤자민', '잭로그', '세베리노', '타카다'], 'SSG': ['아빌라', '해치', '에레디아', '타케다'],
         '한화': ['화이트', '짐머맨', '페라자', '왕옌청'], '롯데': ['로드리게스', '비슬리', '레이예스', '이이무라'], 'NC': ['라일리', '테일러', '크림', '토다'],
         '키움': ['알칸타라', '데이비슨', '히우라', '유토']}
NARR_TEAM = {'KT': '케이티', '삼성': '삼성', 'KIA': '기아', 'LG': '엘지', '두산': '두산', 'SSG': '에스에스지', '한화': '한화', '롯데': '롯데', 'NC': '엔씨', '키움': '키움'}

def wrap16(s, n=16):
    """자막 한 조각을 16자 안쪽 두 줄로(낱말 단위)"""
    if '\n' in s or len(s) <= n: return s
    w = s.split(' '); best = None
    for k in range(1, len(w)):
        a, b = ' '.join(w[:k]), ' '.join(w[k:])
        sc = max(len(a), len(b))
        if re.match(r'^(게|것|수|달러|원|점|개|번|명|위|년|월|일|경기|퍼센트|타석|이닝|홈런)', b) or re.search(r'\d$', a): sc += 20
        if len(a) > n or len(b) > n: sc += 5
        if best is None or sc < best[0]: best = (sc, a + '\n' + b)
    return best[1]

def _shift(o, k):
    """호흡을 앞에서 k개 뺐을 때 장면 at·○○At 을 k 만큼 당긴다(0 아래로는 0)"""
    if isinstance(o, dict):
        for key, v in list(o.items()):
            if (key == 'at' or key.endswith('At')) and isinstance(v, (int, float)) and not isinstance(v, bool): o[key] = max(0, round(v - k, 3))
            else: _shift(v, k)
    elif isinstance(o, list):
        for v in o: _shift(v, k)

def NEW(narr, sub, scene, slow=False):
    pcs = [wrap16(x) for x in sub.split('|')]
    assert len(pcs) == len(narr.split(' / ')), (narr, sub)
    d = {'narr': narr, 'sub': '|'.join(pcs)}
    if slow: d['pace'] = 'slow'
    return (None, d, scene)

def OLD(i, scene=None, narr=None, sub=None, drop=0):
    """롱폼 i번 줄 그대로(음성 재사용). narr/sub 를 주거나 drop(앞 호흡 몇 개 빼기)이면 그 줄만 새로 합성."""
    d = copy.deepcopy(LN[i]); d.pop('gapAfter', None)
    sc = copy.deepcopy(scene if scene is not None else SCN.get(i))
    if drop:
        narr = ' / '.join(d['narr'].split(' / ')[drop:]); sub = '|'.join(d['sub'].split('|')[drop:])
        if sc is not None and scene is None: _shift(sc, drop)
    if narr: d['narr'] = narr
    if sub: d['sub'] = '|'.join(wrap16(x) for x in sub.split('|'))
    assert len(d['sub'].split('|')) == len(d['narr'].split(' / ')), (i, d)
    return (i if not narr else None, d, sc)

def Q(team, text=None):
    """마지막 질문 — 롱폼 질문(사용자 문구)과 같은 틀을 팀 이름으로"""
    nt, faces = NARR_TEAM[team], [E(x) for x in TEAM4[team]]
    return NEW(f'{nt}에 남았으면 하는 외국인 선수와 / 떠났으면 하는 선수는 누구인가요?', f'{team}에 남았으면 하는 외국인 선수와|떠났으면 하는 선수는 누구인가요?',
               {"type": "question", "text": text or f"{team}에 남았으면\n하는 선수는?", "faces": faces}, slow=True)
POINT = lambda: NEW('열 개 구단 외국인 재계약 전체 정리는 / 하단 관련 영상에 있어요', '10개 구단 외국인 재계약 전체 정리는|하단 관련 영상에 있어요',
                    {"type": "photo", "img": TH, "fit": "cover", "text": "", "relArrow": True})
CTA = lambda: OLD(144, {"type": "photo", "img": TH, "fit": "cover", "text": ""})   # 구독 멘트 — 장면을 따로 둬 화살표는 관련 영상 줄에서만
def sbx(i, **kw):
    """롱폼 slotboard 장면을 판단 줄용으로(글·체인 없이 도장까지 다 보이게)"""
    s = copy.deepcopy(SCN[i]); [s.pop(k, None) for k in ('text', 'textAt', 'size', 'chain', 'cont')]
    for sl in s.get('slots', []):
        for k in ('at', 'tagAt', 'noteAt', 'insetAt', 'xAt'):
            if k in sl: sl[k] = 0
    if 'bracket' in s: s['bracket']['at'] = 0
    s.update(kw); return s
def ppx(i, **kw):
    s = copy.deepcopy(SCN[i]); [s.pop(k, None) for k in ('chain', 'cont')]; s.update(kw); return s

YT_TAIL = '\n10개 구단 외국인 재계약 전체 정리는 하단 관련 영상에 있어요.'
CUTS = []
# ── 1 규칙 ────────────────────────────────────────────────
CUTS.append(dict(topic='외국인선수몸값규칙', team='', vtitle=['KBO 외국인 선수', '몸값 규칙'],
  lines=[
    NEW('케이비오 구단은 / 외국인 선수 몸값을 / 마음대로 못 줘요', 'KBO 구단은|외국인 선수 몸값을|마음대로 못 줘요', ppx(5)),
    OLD(6), OLD(7), OLD(8), OLD(9), OLD(10), OLD(11), OLD(12), OLD(13), OLD(14),
    NEW('여러분은 외국인 선수를 / 더 많이 쓰게 해야 한다고 보세요?', '여러분은 외국인 선수를|더 많이 쓰게 해야 한다고 보세요?',
        {"type": "question", "text": "외국인 선수\n더 많이 써야 할까?", "faces": [E('힐리어드'), E('아빌라'), E('왕옌청'), E('오스틴')]}, slow=True),
    POINT(), CTA()],
  yt=dict(title='KBO 외국인 선수 몸값 규칙 | 새로 오면 100만 달러, 3명 합쳐 400만 달러 #외국인선수 #프로야구',
    desc='KBO 외국인 선수 몸값에는 한도가 있어요.\n새로 데려오는 외국인 선수는 100만 달러까지, 외국인 세 명 몸값은 합쳐서 400만 달러까지예요. 재계약한 선수가 있으면 합계 한도가 10만 달러씩 늘어나요. 아시아쿼터 선수 한 명은 따로 뽑고 첫해엔 20만 달러 안에서 데려와요.\n\n2026년 겨울엔 변수가 두 개 더 있어요. KBO는 10월 7일 이사회에서 외국인 선수 보유 제한을 단계적으로 완화하는 방안을 추진하겠다고 했고(몇 명까지·언제부터인지는 아직 미정), 메이저리그는 노사협약이 12월 초에 끝나 직장폐쇄 우려가 나와요.\n\n여러분은 외국인 선수를 더 많이 쓰게 해야 한다고 보세요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['외국인 선수 몸값', '외국인 선수 연봉 상한', 'KBO 외국인 선수 규정', '외국인 선수 재계약', '아시아쿼터', '외국인 보유 제한', '샐러리캡', 'MLB 노사협약', '직장폐쇄', '힐리어드', '아빌라', '왕옌청', '오스틴', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#외국인선수', '#아시아쿼터', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='롯데 자이언츠·키움 히어로즈 제공, KBO·구단 발표, 뉴시스·MK·스포츠경향·스포티비 보도, 구단 공식 선수 프로필'))

# ── 2 KT ──────────────────────────────────────────────────
CUTS.append(dict(topic='KT외국인재계약힐리어드', team='KT', vtitle=['KT 외국인 선수', '재계약할까?'],
  lines=[
    OLD(0),   # 4월 퇴출 거론 → 타점 1위(사용자 훅 문구, 롱폼 음성 그대로)
    NEW('그 주인공은 / 케이티 외국인 타자 힐리어드예요', '그 주인공은|KT 외국인 타자 힐리어드예요', ppx(19)),
    OLD(20), OLD(21), OLD(22), OLD(23), OLD(25), OLD(26),
    OLD(27, scene=sbx(18)),
    Q('KT'), POINT(), CTA()],
  yt=dict(title='KT 외국인 선수 재계약 | 퇴출 거론되던 힐리어드, 타점 1위로 반전 #KT위즈 #힐리어드',
    desc='KT 위즈 힐리어드는 4월까지 타율 0.232에 그쳐 가장 먼저 퇴출 대상으로 거론됐어요. 이강철 감독은 퇴출 걱정은 하지 말라며 기다렸고, 힐리어드는 10월 7일까지 홈런 42개·타점 134개로 타점 1위에 올랐어요(KBO 기록). 걸리는 건 삼진 173개로 역대 한 시즌 최다 기록과 같아졌다는 점이에요.\n\n이강철 감독은 9월 23일 힐리어드가 삼진이 많긴 해도 팀 구성과 잘 어울린다고 했고, 힐리어드 본인도 2027년에도 KT에서 뛰고 싶다고 했어요. 6월 부상 대체로 왔다가 정식 계약을 따낸 투수 로건도 KT에 오랫동안 남고 싶다고 했고요.\n\nKT에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['KT 위즈', 'KT 외국인 선수', '힐리어드', '힐리어드 재계약', '로건', '대니엘', '스기모토', '이강철', '타점 1위', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#KT위즈', '#힐리어드', '#외국인선수', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='KT 위즈 제공, KT 위즈 2026 공식 프로필'))

# ── 3 삼성 ────────────────────────────────────────────────
CUTS.append(dict(topic='삼성외국인재계약디아즈페덱', team='삼성', vtitle=['삼성 외국인 선수', '재계약할까?'],
  lines=[
    NEW('삼성은 외국인 셋 다 / 남길 분위기인데요 / 속사정은 조금 달라요', '삼성은 외국인 셋 다|남길 분위기인데요|속사정은 조금 달라요', ppx(29)),
    OLD(30), OLD(31), OLD(32), OLD(33), OLD(34), OLD(35), OLD(36), OLD(37),
    OLD(39, scene=ppx(29)),
    Q('삼성'), POINT(), CTA()],
  yt=dict(title='삼성 외국인 선수 재계약 | 디아즈 홈런 50개→26개, 페덱은 재계약 0순위 #삼성라이온즈 #디아즈',
    desc='삼성 라이온즈는 외국인 세 명 모두 남길 분위기지만 속사정은 조금 달라요.\n디아즈는 2025년 홈런 50개를 쳤는데 2026년엔 10월 7일까지 26개로 줄었어요. 대신 타점은 128개로 리그 2위예요. 박진만 감독은 계약하지 않을 이유가 없다고 했고, 팬 커뮤니티에선 연봉을 깎고 재계약하자는 의견이 가장 많아요.\n\n7월에 들어온 페덱은 10월 4일까지 12경기 7승 3패, 평균자책점 2.95. 스포츠조선은 페덱을 삼성의 재계약 0순위로 꼽았지만, 대체 선수라 47만 달러 남짓을 받은 만큼 일본 진출이나 메이저리그 복귀도 선택지로 거론돼요.\n\n삼성에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['삼성 라이온즈', '삼성 외국인 선수', '디아즈', '디아즈 재계약', '페덱', '후라도', '사토시', '미야모리', '박진만', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#삼성라이온즈', '#디아즈', '#페덱', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='삼성 라이온즈 제공, 삼성 라이온즈 2026 공식 프로필'))

# ── 4 KIA ─────────────────────────────────────────────────
CUTS.append(dict(topic='KIA외국인재계약네일연봉', team='KIA', vtitle=['KIA 외국인 선수', '셋 다 잡을까?'],
  lines=[
    NEW('기아는 외국인 셋 다 잡고 싶은데 / 돈이 문제예요', 'KIA는 외국인 셋 다 잡고 싶은데|돈이 문제예요', ppx(41)),
    OLD(42), OLD(44), OLD(46), OLD(48), OLD(49), OLD(50), OLD(51), OLD(52),
    OLD(54, scene=ppx(51)),
    Q('KIA'), POINT(), CTA()],
  yt=dict(title='KIA 외국인 선수 재계약 | 네일·올러·카스트로 몸값 420만 달러, 셋 다 잡을까 #KIA타이거즈 #네일',
    desc='KIA 타이거즈는 외국인 세 명을 다 잡고 싶은데 돈이 문제예요.\n네일은 2026년 총액 200만 달러에 재계약해 30경기에서 리그 최다 176이닝을 던졌고, 올러는 120만 달러를 받고 10월 6일까지 평균자책점 3.03으로 리그 2위예요. 타자 카스트로는 100만 달러에 처음 KBO에 와서 햄스트링 부상으로 54일을 빠지고도 10월 1일까지 타율 3할 2푼대·홈런 18개를 쳤어요.\n\n세 명 몸값을 더하면 420만 달러로 400만 달러보다 많은데, 재계약 선수가 있어 한도가 늘어난 덕분에 가능했어요. 스포티비는 올러와 카스트로를 잡으려면 네일의 연봉 인상 폭은 제한될 수밖에 없다고 봤어요.\n\nKIA에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['KIA 타이거즈', '기아 타이거즈', 'KIA 외국인 선수', '네일', '네일 연봉', '올러', '카스트로', '시라카와', '이범호', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#KIA타이거즈', '#네일', '#카스트로', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='KIA 타이거즈 제공, KIA 타이거즈 2026 공식 프로필'))

# ── 5 LG ──────────────────────────────────────────────────
CUTS.append(dict(topic='LG외국인재계약오스틴계약기간', team='LG', vtitle=['LG 외국인 선수', '오스틴 몇 년?'],
  lines=[
    NEW('엘지는 외국인 재계약에서 / 계약 기간이 문제예요', 'LG는 외국인 재계약에서|계약 기간이 문제예요',
        {"type": "profile", "img": "카드/오스틴_MVP_포효", "name": "오스틴", "sub": "LG 외국인 타자", "stats": [], "viz": [{"type": "stamp", "t": "계약 기간?", "at": 1, "c": "gold"}]}),
    OLD(56), OLD(57), OLD(58), OLD(60), OLD(61), OLD(62), OLD(63), OLD(64),
    OLD(65, scene=ppx(61)),
    Q('LG'), POINT(), CTA()],
  yt=dict(title='LG 외국인 선수 재계약 | 오스틴 LG 첫 40홈런, 다년 계약 할까 #LG트윈스 #오스틴',
    desc='LG 트윈스는 외국인 재계약에서 계약 기간이 문제예요.\n오스틴은 2026년 홈런 41개를 쳐 LG 선수 최초로 한 시즌 40홈런을 넘겼어요. 8월엔 미국에 돌아가지 않아도 되도록 좋은 조건을 제안해 주면 좋겠다고 했고, 염경엽 감독도 6월에 오스틴은 한국에서 은퇴하는 게 가장 낫다고 했어요. 9월 말 해설위원 방송에선 다년 계약까지 검토할 선수로 꼽혔지만, 팬 커뮤니티에선 2년을 넘기면 안 된다는 말도 나와요.\n\n투수 쪽은 더 복잡해요. 톨허스트는 2026년 12승을 거뒀지만 평균자책점이 4점대로 올랐고, 7월에 들어온 39세 카라스코는 6승 2패를 거뒀지만 팬 커뮤니티에선 재계약 찬반이 엇갈려요.\n\nLG에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['LG 트윈스', 'LG 외국인 선수', '오스틴', '오스틴 재계약', '오스틴 다년계약', '톨허스트', '카라스코', '케네디', '염경엽', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#LG트윈스', '#오스틴', '#외국인선수', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='LG 트윈스 제공, LG 트윈스 2026 공식 프로필'))

# ── 6 두산 ────────────────────────────────────────────────
CUTS.append(dict(topic='두산외국인재계약벤자민잭로그', team='두산', vtitle=['두산 외국인 선수', '누가 남을까?'],
  lines=[
    OLD(67), OLD(68), OLD(69), OLD(71), OLD(72), OLD(73), OLD(74), OLD(76),
    OLD(78, scene=ppx(67)),
    Q('두산'), POINT(), CTA()],
  yt=dict(title='두산 외국인 선수 재계약 | 6주 대체 벤자민은 남고 110만 달러 잭로그는 떠날까 #두산베어스 #벤자민',
    desc='두산 베어스는 6주짜리 대체 선수가 남고 110만 달러를 받은 투수가 떠날 수도 있는 팀이에요.\n개막 때 100만 달러에 6년 만에 돌아온 플렉센이 4월 어깨를 다쳐 결국 팀을 떠났고, 그 자리를 6주 계약으로 채운 벤자민이 7월 45만 달러에 정식 계약까지 따냈어요. 벤자민은 10월 4일까지 9승 7패, 평균자책점 2점대예요.\n\n반대로 110만 달러를 받은 잭로그는 8승 7패, 평균자책점 4.27로 기복이 커서 로그인·로그아웃이라는 말까지 나왔어요. 7월 20만 달러에 들어온 세베리노는 첫 100타석 타율 0.230에서 그 뒤 18경기 타율 0.397·홈런 6개로 막판 반전을 쓰고 있어요.\n\n두산에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['두산 베어스', '두산 외국인 선수', '벤자민', '잭로그', '세베리노', '타카다', '플렉센', '김원형', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#두산베어스', '#벤자민', '#잭로그', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='두산 베어스 제공, 두산 베어스 2026 공식 프로필'))

# ── 7 SSG ─────────────────────────────────────────────────
CUTS.append(dict(topic='SSG외국인재계약아빌라', team='SSG', vtitle=['SSG 아빌라', '붙잡을까?'],
  lines=[
    OLD(80),
    OLD(81, drop=1),   # "처음에 말한 그 투수인데요" 빼기(롱폼 연결어)
    OLD(82), OLD(83), OLD(84), OLD(85), OLD(86), OLD(87),
    OLD(89, scene=sbx(87)),
    Q('SSG'), POINT(), CTA()],
  yt=dict(title='SSG 외국인 선수 재계약 | 40만 달러 대체 아빌라 9승 2패 1.44, 붙잡을 수 있을까 #SSG랜더스 #아빌라',
    desc='SSG 랜더스 아빌라는 7월에 40만 달러를 받고 들어와 10월 5일까지 14경기에서 9승 2패, 평균자책점 1.44를 기록했어요.\n이숭용 감독은 9월 30일 프런트에 수단과 방법을 가리지 않고 잡아 달라고 했다고 밝혔어요. 아빌라는 9월 10일 2년 정도 남고 싶다는 생각은 변치 않았다고 했지만, 9월 29일엔 지금은 SSG에 전념하겠다면서도 나중 일은 그때 가서 생각하겠다고 했어요. 스포티비는 8월에 메이저리그 스카우트들이 아빌라를 지켜봤다고 보도했고요.\n\nSSG에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['SSG 랜더스', 'SSG 외국인 선수', '아빌라', '아빌라 재계약', '해치', '에레디아', '타케다', '이숭용', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#SSG랜더스', '#아빌라', '#외국인선수', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='SSG 랜더스 제공, SSG 랜더스 2026 공식 프로필'))

# ── 8 한화 ────────────────────────────────────────────────
CUTS.append(dict(topic='한화외국인재계약왕옌청와이스', team='한화', vtitle=['한화 왕옌청·와이스', '둘 다 잡을까?'],
  lines=[
    OLD(91), OLD(92), OLD(93), OLD(94), OLD(95), OLD(97), OLD(98), OLD(100),
    OLD(106, scene=sbx(100)),
    Q('한화'), POINT(), CTA()],
  yt=dict(title='한화 외국인 선수 재계약 | 와이스 복귀설에 10만 달러 11승 왕옌청까지, 둘 다 잡을까 #한화이글스 #와이스',
    desc='한화 이글스의 가장 큰 고민은 아시아쿼터 선수 왕옌청이에요.\n대만 출신 왕옌청은 연봉 10만 달러를 받고 11승을 거뒀어요. 그런데 아시아쿼터로 재계약하면 1년에 올릴 수 있는 폭이 10만 달러로 정해져 있어요. 정식 외국인 선수로 바꾸면 신규 상한인 100만 달러 안에서 줄 수 있어서, 외국인 한 자리를 왕옌청에게 내줄지가 거론돼요.\n\n여기에 2025년 한화에서 뛴 와이스가 휴스턴과의 2027년 옵션이 실행되지 않을 거라는 전망이 나오면서, 보류권을 가진 한화로 돌아올 수 있다는 얘기가 나와요. 정식 외국인 자리는 세 개뿐이라 왕옌청을 정식 외국인으로 돌리고 와이스까지 잡으면 지금 외국인 가운데 두 명은 빠져야 해요.\n\n한화에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['한화 이글스', '한화 외국인 선수', '왕옌청', '왕옌청 재계약', '와이스', '와이스 복귀', '화이트', '짐머맨', '페라자', '아시아쿼터', '김경문', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#한화이글스', '#왕옌청', '#와이스', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='한화 이글스 제공, 한화 이글스 2026 공식 프로필, MLB 공식 헤드샷(와이스)'))

# ── 9 롯데 ────────────────────────────────────────────────
CUTS.append(dict(topic='롯데외국인재계약로드리게스비슬리', team='롯데', vtitle=['롯데 외국인 투수', '바꿀까?'],
  lines=[
    OLD(109), OLD(108),
    OLD(110, drop=2),   # "처음에 말한 투수들이 / 바로 이 두 명이에요" 빼기(롱폼 연결어)
    OLD(111), OLD(112), OLD(113), OLD(114),
    OLD(116, scene=sbx(108)),
    Q('롯데'), POINT(), CTA()],
  yt=dict(title='롯데 외국인 선수 재계약 | 100만 달러 투수 로드리게스·비슬리, 폰세·와이스급 기대는 #롯데자이언츠 #레이예스',
    desc='롯데 자이언츠는 시즌 전 100만 달러씩 준 투수 로드리게스와 비슬리가 2025년 한화 원투펀치였던 폰세·와이스급이라는 기대를 받았어요. 롯데는 2026년 외국인 세 명을 한 번도 바꾸지 않았는데요, 해설위원 방송 평가는 두 투수 모두 뚜렷한 강점을 보여 주지 못했다고 봤어요.\n\n로드리게스는 10승 11패, 평균자책점 4.28을 기록한 뒤 9월 말 경기 도중 팔 저림으로 내려가 오른팔 신경 염증 진단을 받고 시즌을 마쳤어요(구단: 약 2주 재활). 반면 타자 레이예스는 해설위원 방송 평가에서 필요한 선수로 꼽혔고 팬 커뮤니티에서도 재계약 찬성이 많아요.\n\n롯데에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['롯데 자이언츠', '롯데 외국인 선수', '로드리게스', '비슬리', '레이예스', '레이예스 재계약', '이이무라', '김태형', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#롯데자이언츠', '#레이예스', '#외국인선수', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='롯데 자이언츠 제공, 롯데 자이언츠 2026 공식 프로필'))

# ── 10 NC ─────────────────────────────────────────────────
CUTS.append(dict(topic='NC외국인재계약라일리크림', team='NC', vtitle=['NC 외국인 선수', '라일리만 남을까?'],
  lines=[
    OLD(118), OLD(119), OLD(120), OLD(121), OLD(122), OLD(123), OLD(124), OLD(125),
    OLD(126, scene=sbx(125)),
    Q('NC'), POINT(), CTA()],
  yt=dict(title='NC 외국인 선수 재계약 | 12경기 연속 QS 라일리는 잡고, 나머지 두 자리는 #NC다이노스 #라일리',
    desc='NC 다이노스는 에이스 라일리를 잡는 게 먼저예요. 라일리는 7월부터 12경기 연속 퀄리티스타트(선발 6이닝 이상, 자책점 3점 이하)를 했어요. 머니투데이는 NC가 라일리 재계약을 최우선으로 둘 거라고 봤고, 이호준 감독은 라일리가 많이 던진 점 등을 고려해 남은 등판 일정에서 뺐다고 했어요.\n\nNC는 6월 말 2024년 홈런왕 출신 데이비슨을 내보내고 7월 1일 블레인 크림을 데려왔는데, 데이비슨은 키움으로 옮겨 홈런 20개를 더 쳤고 해설위원 방송 평가는 블레인을 교체 대상에 오를 선수로 꼽았어요. 외국인 투수 테일러도 8월 말 등판 뒤 어깨를 다쳐 6주짜리 대체 선수 클레빈저가 자리를 메웠어요.\n\nNC에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['NC 다이노스', 'NC 외국인 선수', '라일리', '라일리 재계약', '블레인 크림', '크림', '테일러', '클레빈저', '토다', '데이비슨', '이호준', '퀄리티스타트', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#NC다이노스', '#라일리', '#외국인선수', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='NC 다이노스 제공, NC 다이노스·키움 히어로즈 2026 공식 프로필'))

# ── 11 키움 ───────────────────────────────────────────────
CUTS.append(dict(topic='키움외국인재계약데이비슨히우라', team='키움', vtitle=['키움 외국인 타자', '누가 남을까?'],
  lines=[
    OLD(127, scene=ppx(123)), OLD(128), OLD(129), OLD(130), OLD(131), OLD(132), OLD(133), OLD(134), OLD(135),
    OLD(136, scene=sbx(135)),
    Q('키움'), POINT(), CTA()],
  yt=dict(title='키움 외국인 선수 재계약 | 티머니 데이비슨 vs 히우라, 한 명은 떠나야 #키움히어로즈 #데이비슨',
    desc='NC가 내보낸 2024년 홈런왕 출신 데이비슨은 이제 키움 히어로즈의 고민이 됐어요.\n키움은 에이스 알칸타라와 2027년에도 함께하기로 큰 틀에서 합의했어요(9월 팔꿈치 뼛조각 제거 수술 전). 6월 말 외국인 투수 한 명을 내보내고 데이비슨을 데려와 외국인 타자 두 명으로 시즌을 치렀는데, 데이비슨은 2026년 두 팀에서 홈런 28개, 히우라는 72경기에서 홈런 13개를 쳤어요.\n\n버스로 출퇴근해 스스로를 티머니 선수라고 부르는 데이비슨은 구단이 원한다면 2027년에도 꼭 돌아오고 싶다고 했어요. 하지만 2027년에 외국인 투수를 두 명 쓰려면 두 타자 가운데 한 명은 떠나야 하고, 해설위원 방송 평가는 히우라를 교체 대상에 오를 선수로 꼽았어요.\n\n키움에 남았으면 하는 외국인 선수와 떠났으면 하는 선수는 누구인가요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['키움 히어로즈', '키움 외국인 선수', '데이비슨', '데이비슨 티머니', '히우라', '알칸타라', '유토', '외국인 선수 재계약', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#키움히어로즈', '#데이비슨', '#히우라', '#프로야구', '#KBO', '#야구자판기']),
  thumb=None, credit='키움 히어로즈 제공, 키움 히어로즈 2026 공식 프로필'))

THUMBS = {   # 10/8 밤: 컷 썸네일 = 채널 썸네일에 안 쓴 구단 제공 사진(누끼 → KBO 보정 0.75 → 가운데 맞춤). 같은 세트 안에서도 겹치지 않게
  1: dict(teams=[], img='누끼/그룹_컷1_알칸타라_레이예스', crop=0.8, lift=180, overlap=280, ph=880, big='외국인 선수\n몸값 규칙'),
  2: dict(teams=['KT'], img='누끼/KBO스타일_경기_힐리어드_하이파이브_KT제공_center', crop=0.68, lift=180, overlap=330, ph=880, big='힐리어드\n남을까?'),
  3: dict(teams=['삼성'], img='누끼/KBO스타일_경기_디아즈_만루포세리머니_삼성제공_center', crop=0.68, lift=180, overlap=330, ph=880, big='디아즈\n재계약?'),
  4: dict(teams=['KIA'], img='누끼/KBO스타일_경기_네일_역투_KIA제공_center', crop=0.68, lift=180, overlap=330, ph=880, big='네일\n잡을 돈 있나?'),
  5: dict(teams=['LG'], img='누끼/KBO스타일_경기_오스틴_동료축하_LG제공_center', crop=0.68, lift=180, overlap=330, ph=880, big='오스틴\n몇 년 계약?'),
  6: dict(teams=['두산'], img='누끼/KBO스타일_경기_벤자민_투구후_두산제공_center', crop=0.68, lift=180, overlap=330, ph=880, big='벤자민\n남을까?'),
  7: dict(teams=['SSG'], img='누끼/KBO스타일_경기_아빌라_글러브공_SSG제공_center', crop=0.68, lift=180, overlap=330, ph=880, big='아빌라\n붙잡을까?'),
  8: dict(teams=['한화'], img='누끼/그룹_컷8_왕옌청_와이스', crop=0.8, lift=180, overlap=280, ph=800, big='왕옌청·와이스\n둘 다 잡을까?'),   # 10/9 사용자: 왕옌청·와이스 같이
  9: dict(teams=['롯데'], img='누끼/KBO스타일_경기_비슬리_박수_롯데제공_center', crop=0.68, lift=180, overlap=330, ph=880, big='비슬리\n바꿀까?'),
  10: dict(teams=['NC'], img='누끼/KBO스타일_경기_라일리_투구_NC제공_center', crop=0.68, lift=180, overlap=330, ph=880, big='라일리\n재계약?'),
  11: dict(teams=['키움'], img='누끼/그룹_컷11_데이비슨_히우라', crop=0.8, lift=180, overlap=280, ph=800, big='데이비슨·히우라\n누가 남을까?'),
}

out = []
for n, c in enumerate(CUTS, 1):
    lines, scenes, vmap = [], [], []
    for j, (src, d, sc) in enumerate(c['lines']):
        lines.append(d); vmap.append(src)
        if sc is not None:
            sc = dict(sc); sc['startLine'] = j
            if sc.get('type') == 'slotboard': [sc.pop(k, None) for k in ('text', 'textAt', 'size')]   # 10/8 밤 사용자: 자리판 가운데 파란 설명 글 없앰(괄호·도장으로)
            if sc.get('cont') and not (j and src is not None and vmap[j - 1] == src - 1): sc.pop('cont')
            scenes.append(sc)
    t = THUMBS.get(n) or c['thumb']
    thumb = None
    if t:
        thumb = {"teams": t['teams'], "img": t['img'], "cutout": True, "cutoutCrop": t['crop'], "cutoutLift": t.get('lift', 120), "cutoutOverlap": t.get('overlap', 220),
                 "cutoutFade": 0.62, "logos": False, "top": t.get('top', ''), "big": t['big'], "perLine": True,
                 **{k: t[k] for k in ('color', 'barColor') if k in t}, **({'ph': t['ph']} if 'ph' in t else {})}
    e = {
        'date': '2026-10-08', 'gameDate': '2026-10-08', 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': c['team'], 'speed': 1.0, 'ttsApi': True, 'ttsTempo': 1.2, 'ttsTempoSlow': 1.15,   # 롱폼⑨와 같은 줄별 배속(음성 그대로 재사용)
        'rev': f'1008-cut{n}-v1', 'topic': c['topic'],
        'vtitle': c['vtitle'], 'vbasis': '',
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': '2026-10-08_롱폼', 'lines': vmap},
        'source': f'롱폼 {SRC} 에서 잘라 세로로 다시 짬(컷 {n}). ' + ep.get('source', ''),
        'lines': lines, 'scenes': scenes,
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'] + f"\n\n사진: {c['credit']}", 'tags': c['yt']['tags'], 'hashtags': c['yt']['hashtags']},
    }
    if thumb: e['thumb'] = thumb
    p = os.path.join(HERE, 'episodes', f"2026-10-08_롱폼컷{n}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    est = sum(len(l['narr'].replace(' / ', ' ')) * 0.175 + 0.3 * 0.6 * l['narr'].count(' / ') + 0.45 * 0.6 for l in lines) + 1.0
    newc = sum(len(l['narr']) for s, l in zip(vmap, lines) if s is None)
    out.append((n, c['topic'], len(lines), len(scenes), round(est), newc))
    for b in (x for l in lines for x in l['narr'].split(' / ')):
        if len(re.sub(r'[\s,?]', '', b)) > 22: print('호흡 초과', n, b)
for r in out: print(r)
print('새로 합성 합계', sum(r[5] for r in out), '자')
