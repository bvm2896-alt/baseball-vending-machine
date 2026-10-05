# 10/2 롱폼⑤(탈락 5팀) → 컷 쇼츠 6편. 세로(1080x1920) — template_long 을 세로 틀(EP.vertical)로 그린다.
# 원본 줄은 롱폼 음성을 그대로 쓰고(build.py prep 이 voiceFrom 으로 복사, 대사가 같은 줄만), 새 줄만 API 합성.
# 실행: python -X utf8 tools/gen_1002_cuts.py  → episodes/2026-10-02_롱폼컷1~6.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-01_롱폼.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)

def wrap16(s, n=16):
    """자막 한 조각을 16자 안쪽 두 줄로(낱말 단위)"""
    if '\n' in s or len(s) <= n: return s
    w = s.split(' '); best = None
    for k in range(1, len(w)):
        a, b = ' '.join(w[:k]), ' '.join(w[k:])
        sc = max(len(a), len(b))
        if re.match(r'^(게|것|수|달러|원|점|개|번|명|위|년|월|일|경기|퍼센트)', b) or re.search(r'\d$', a): sc += 20   # 숫자·단위·의존명사 앞에서 꺾지 않는다
        if len(a) > n or len(b) > n: sc += 5
        if best is None or sc < best[0]: best = (sc, a + '\n' + b)
    return best[1]

def NEW(narr, sub, scene, rate=None):
    pcs = [wrap16(x) for x in sub.split('|')]
    assert len(pcs) == len(narr.split(' / ')), (narr, sub)
    d = {'narr': narr, 'sub': '|'.join(pcs)}
    if rate: d['rate'] = rate
    return (None, d, scene)

def OLD(i, scene=None, narr=None, sub=None):
    d = copy.deepcopy(LN[i])
    if narr: d['narr'] = narr
    if sub: d['sub'] = '|'.join(wrap16(x) for x in sub.split('|'))
    assert len(d['sub'].split('|')) == len(d['narr'].split(' / ')), (i, d)
    sc = copy.deepcopy(scene if scene is not None else SCN.get(i))
    return (i if not narr else None, d, sc)

POINT = lambda: NEW('가을야구 탈락 다섯 팀 분석은 관련 영상에 있어요',
                    '가을야구 탈락 5팀 분석은|관련 영상에 있어요'.replace('|', '\n'),
                    {"type": "question", "text": "탈락 5팀 전체 분석\n관련 영상에서", "logos": ["SSG", "NC", "롯데", "한화", "키움"]})
CTA = lambda: OLD(77)

# statbars 롯데 득점 순위: 10/1 경기로 두산(653)이 롯데(649)를 넘어 롯데 득점 9위 (롱폼 화면은 9/30 의 8위가 남아 있었음)
def fix_lt(sc):
    sc = copy.deepcopy(sc)
    for r in sc.get('rows', []):
        if r.get('l') == '649 (8위)': r['l'] = '649 (9위)'
        if r.get('r') == '781 (1위)': r['r'] = '783 (1위)'; r['rv'] = 783   # 10/1 한화 득점 783 (롱폼 표는 9/30 의 781 이 남아 있었음)
    return sc

CUTS = []
# ── 컷1 롯데 ─────────────────────────────────────────────
CUTS.append(dict(slot='롱폼컷1', topic='롯데홈런꼴찌', team='롯데',
  vtitle=['롯데 타율 3위인데', '홈런은 꼴찌'],
  lines=[
    NEW('롯데는 타율 삼 위인데 홈런은 꼴찌예요', '롯데는 타율 3위인데 홈런은 꼴찌예요',
        {"type": "big", "team": "롯데", "text": "타율 3위\n홈런 꼴찌"}),
    OLD(33), OLD(34), OLD(35, fix_lt(SCN[35])), OLD(36, fix_lt(SCN[36])), OLD(37, fix_lt(SCN[37])), OLD(38, fix_lt(SCN[38])),
    OLD(39, narr='롯데가 유강남, 노진혁, 한현희와 맺은 / 최대 백칠십억 원 계약이 이번 시즌으로 끝나서 / 이번 겨울엔 지갑을 열 여유가 생겨요',
        sub='롯데가 유강남 노진혁\n한현희와 맺은|최대 170억 원 계약이\n이번 시즌으로 끝나서|이번 겨울엔 지갑을\n열 여유가 생겨요',
        scene=dict(SCN[39], cols=[dict(c, cards=[dict(x, img=f"KBO프로필/{x['n']}") for x in c['cards']]) for c in SCN[39]['cols']])),   # 10/2 밤 사용자: 선수 이야기면 선수 이미지
    OLD(41, scene=dict(SCN[41], items=[SCN[41]['items'][0], dict(SCN[41]['items'][1], t='유강남 자리\n포수', img='KBO프로필/유강남', fs=56)])),
    OLD(53),
    NEW('롯데는 내년 가을야구에 갈까요? / 못 갈까요?', '롯데는 내년 가을야구에 갈까요|못 갈까요?',
        {"type": "question", "text": "롯데\n내년엔 갈까?", "logos": ["롯데"]}),   # 팀 이야기 → 로고
    POINT(), CTA()],
  yt=dict(title='롯데 자이언츠 | 타율 3위인데 홈런 꼴찌, 9년 연속 가을야구 탈락 이유 #롯데자이언츠 #프로야구',
    desc='롯데 자이언츠는 팀 타율 3위인데 홈런은 리그 꼴찌예요. 안타는 치는데 점수가 안 나는 이유를 10월 1일 KBO 기록으로 짚었어요.\n롯데는 내년 가을야구에 갈 수 있을까요?\n\n롯데는 2017년 이후 9년 연속 가을야구에 못 갔어요. 롯데 팀 타율은 0.273으로 3위, 한화는 0.272로 4위라 거의 같아요. 그런데 득점은 한화 783점, 롯데 649점으로 134점 차이가 나요. 그 차이를 만든 건 홈런 — 한화 169개, 롯데 105개로 롯데 홈런은 리그 꼴찌예요.\n\n유강남·노진혁·한현희와 맺은 최대 170억 원 계약이 이번 시즌으로 끝나서, 롯데는 이번 겨울 한 방을 쳐 줄 타자와 포수를 찾을 여유가 생겨요.\n\n가을야구 탈락 5팀(SSG·NC·롯데·한화·키움) 전체 분석은 관련 동영상(롱폼)에서 볼 수 있어요.\n가능성(%)은 영상 제작자의 예상이에요.\n\n롯데는 내년 가을야구에 갈까요, 못 갈까요? 댓글로 알려 주세요.',
    tags=['롯데 자이언츠', '롯데', '롯데 홈런', '롯데 가을야구', '롯데 9년 연속', '김태형', '유강남', '롯데 FA', '프로야구 탈락 5팀', '2027 가을야구', '프로야구', 'KBO', '야구 쇼츠', '야구자판기'],
    hashtags=['#Shorts', '#프로야구', '#KBO', '#야구', '#롯데자이언츠', '#롯데', '#김태형', '#야구자판기']),
  thumb={"teams": ["롯데"], "top": "타율 3위인데", "big": "롯데\n홈런 꼴찌"}))

# ── 컷2 한화 ─────────────────────────────────────────────
CUTS.append(dict(slot='롱폼컷2', topic='한화타선1위9위', team='한화',
  vtitle=['한화 홈런 1위인데', '순위는 9위'],
  lines=[
    NEW('한화는 홈런 일 위인데 순위는 구 위예요', '한화는 홈런 1위인데 순위는 9위예요',
        {"type": "big", "team": "한화", "text": "홈런 1위\n순위 9위"}),
    OLD(55, narr='한화는 타선만 보면 가을야구 팀이에요 / 한화의 득점은 칠백팔십삼 점, 홈런은 백육십구 개 / 둘 다 리그 일 위예요',
        sub=('|'.join(LN[55]['sub'].split('|')[1:]))),
    OLD(56), OLD(58), OLD(59), OLD(60), OLD(61), OLD(63),
    NEW('한화는 내년 가을야구에 갈까요? / 못 갈까요?', '한화는 내년 가을야구에 갈까요|못 갈까요?',
        {"type": "question", "text": "한화\n내년엔 갈까?", "logos": ["한화"]}),
    POINT(), CTA()],
  yt=dict(title='한화 이글스 | 홈런 1위인데 9위, 감독도 아직 미정 #한화이글스 #프로야구',
    desc='한화 이글스는 득점·홈런 리그 1위인데 순위는 9위예요. 타선은 가을야구 팀인데 왜 떨어졌는지, 내년엔 갈 수 있는지 10월 1일 KBO 기록으로 짚었어요.\n한화의 다음 감독이 정해져야 숫자가 올라가요.\n\n한화 팀 평균자책점은 5.26으로 9위, 세이브는 16개로 리그 꼴찌, 실책은 106개로 가장 많아요. 외국인 투수 화이트는 7승 12패, 짐머맨은 9월 초 평균자책점이 14점대였어요.\n\n한화가 노릴 투수는 선발 원태인과 불펜 박치국이에요. 그런데 김경문 감독은 올해로 계약이 끝나고, 감독과 단장이 함께 물러날 거라는 설까지 나왔어요. 구단은 아직 아무것도 발표하지 않았어요.\n\n가을야구 탈락 5팀(SSG·NC·롯데·한화·키움) 전체 분석은 관련 동영상(롱폼)에서 볼 수 있어요.\n가능성(%)은 영상 제작자의 예상이에요.\n\n한화는 내년 가을야구에 갈까요, 못 갈까요? 댓글로 알려 주세요.',
    tags=['한화 이글스', '한화', '한화 감독', '김경문', '한화 가을야구', '한화 홈런', '원태인', '박치국', '프로야구 탈락 5팀', '2027 가을야구', '프로야구', 'KBO', '야구 쇼츠', '야구자판기'],
    hashtags=['#Shorts', '#프로야구', '#KBO', '#야구', '#한화이글스', '#한화', '#김경문', '#야구자판기']),
  thumb={"teams": ["한화"], "top": "타선 1위인데", "big": "한화\n순위는 9위"}))

# ── 컷3 하현승 ───────────────────────────────────────────
HHS = "경기/하현승_드래프트키움_HQ"
CUTS.append(dict(slot='롱폼컷3', topic='하현승양키스거절', team='키움',
  vtitle=['하현승', '양키스 300만 달러 거절'],
  lines=[
    NEW('하현승은 양키스의 삼백만 달러를 거절했어요', '하현승은 양키스의\n300만 달러를 거절했어요',
        {"type": "profile", "img": HHS, "name": "하현승", "sub": "키움 전체 1순위",
         "stats": [{"k": "양키스 제안", "v": "300만 달러 거절", "hi": True, "at": 0}]}),
    NEW('하현승은 키움에 전체 일 순위로 뽑혔어요 / 유퀴즈 예고에서는 / 한국 팬들 앞에서 뛰는 게 꿈이었다고 말했죠',
        '하현승은 키움에 전체 1순위로 뽑혔어요|유퀴즈 예고에서는|한국 팬들 앞에서 뛰는 게 꿈이었다고 말했죠',
        {"type": "profile", "img": HHS, "name": "하현승", "sub": "키움 전체 1순위",
         "stats": [{"k": "양키스 제안", "v": "300만 달러 거절", "hi": True}, {"k": "유퀴즈", "v": "10월 7일 방송", "at": 1}],
         "text": "“한국 팬들 앞에서\n뛰는 게 꿈”", "textSize": 80, "textAt": 2}),
    OLD(65, narr='그런데 하현승이 갈 키움은 / 올해 꼴찌예요 / 키움의 득점은 오백삼십칠 점으로 / 득점 구 위인 롯데보다 백십이 점 적어요',
        sub='그런데 하현승이 갈 키움은|올해 꼴찌예요|키움의 득점은 537점으로|득점 9위인 롯데보다 112점 적어요',
        scene=dict(SCN[65], items=[dict(SCN[65]['items'][0], label='롯데\n득점 9위'), dict(SCN[65]['items'][1], label='키움\n득점 10위')])),
    OLD(66), OLD(67), OLD(70),
    NEW('하현승이 올 키움은 / 내년에 꼴찌를 벗어날까요? / 못 벗어날까요?', '하현승이 올 키움은|내년에 꼴찌를 벗어날까요|못 벗어날까요?',
        {"type": "question", "text": "키움\n꼴찌 벗어날까?", "logos": ["키움"]}),
    POINT(), CTA()],
  yt=dict(title='하현승 유퀴즈 | 양키스 300만 달러 거절하고 키움 전체 1순위 #하현승 #키움히어로즈',
    desc='하현승은 미국 뉴욕 양키스의 300만 달러 제안을 거절하고 키움 히어로즈에 전체 1순위로 뽑혔어요. 유퀴즈 예고에서는 "한국 팬들 앞에서 뛰는 게 꿈"이라고 말했어요(10월 7일 방송).\n하현승이 갈 키움은 내년에 꼴찌를 벗어날 수 있을까요?\n\n키움의 올해 득점은 537점으로 리그 꼴찌, 득점 9위 롯데보다 112점 적어요(10월 1일 KBO 기록). 키움은 그동안 강정호·박병호·김하성·이정후·김혜성·송성문까지 6명을 메이저리그로 보내고 이적료 약 700억 원을 받았어요(2025년 12월 환율).\n\n2027년부터 샐러리캡 하한제가 시작돼서, 선수 연봉 총액이 약 60억 원에 못 미치면 모자란 금액의 30%를 유소년 발전기금으로 내야 해요. 키움도 이제 돈을 써야 해요.\n\n가을야구 탈락 5팀(SSG·NC·롯데·한화·키움) 전체 분석은 관련 동영상(롱폼)에서 볼 수 있어요.\n가능성(%)은 영상 제작자의 예상이에요.\n\n하현승이 올 키움, 내년엔 꼴찌를 벗어날까요? 댓글로 알려 주세요.',
    tags=['하현승', '하현승 유퀴즈', '하현승 양키스', '하현승 키움', '키움 히어로즈', '키움', '신인 드래프트', '샐러리캡 하한제', '프로야구 탈락 5팀', '프로야구', 'KBO', '야구 쇼츠', '야구자판기'],
    hashtags=['#Shorts', '#하현승', '#유퀴즈', '#키움히어로즈', '#키움', '#프로야구', '#KBO', '#야구', '#야구자판기']),
  thumb={"teams": ["키움"], "img": HHS, "top": "양키스 300만 달러 거절", "big": "하현승\n키움 1순위", "logos": False}))

# ── 컷4 SSG 아빌라 ───────────────────────────────────────
AV = "경기/아빌라_포효_SSG제공_HQ"
CUTS.append(dict(slot='롱폼컷4', topic='아빌라SSG내년', team='SSG',
  vtitle=['SSG 아빌라', '남을까 떠날까'],
  lines=[
    NEW('평균자책점 일 점 오 육의 아빌라가 떠날 수도 있어요', '평균자책점 1.56의\n아빌라가 떠날 수도 있어요',
        {"type": "profile", "img": AV, "name": "아빌라", "sub": "SSG 외국인 투수", "stats": [{"k": "평균자책점", "v": "1.56", "hi": True, "at": 0}]}),
    OLD(7, narr='에스에스지는 시월 일 일 기준 육 위예요 / 가을야구 막차인 오 위 두산과는 / 여덟 경기 반 차이가 나요 / 에스에스지의 발목을 잡은 건 선발이에요',
        sub='SSG는 10월 1일 기준 6위예요|가을야구 막차인 5위 두산과는|8경기 반 차이가 나요|SSG의 발목을 잡은 건 선발이에요',
        scene=dict(SCN[7], stats=[{"k": "5위 두산과", "v": "8.5경기 차", "at": 1}])),
    OLD(8),
    OLD(10, scene={"type": "speech", "img": "KBO프로필/아빌라", "name": "아빌라", "sub": "SSG 외국인 투수", "bubbles": [],   # 10/2 밤 사용자 "사라졌다 다시 생기지 말 것" → 다음 두 줄(발언)과 같은 틀
                   "stats": [{"k": "합류", "v": "7월", "at": 0}, {"k": "경기", "v": "13", "at": 1}, {"k": "승패", "v": "8승 2패", "at": 1.3}, {"k": "평균자책점", "v": "1.56", "hi": True, "at": 1.6}]}),
    OLD(11, scene=dict(SCN[11], cont=True)), OLD(12),
    OLD(19, scene=dict(SCN[19], items=[dict({k: v for k, v in it.items() if k != 'team'}, img="KBO프로필/아빌라", gray=(i == 1)) for i, it in enumerate(SCN[19]['items'])])),
    NEW('아빌라는 에스에스지에 남을까요? / 미국으로 갈까요?', '아빌라는 SSG에 남을까요|미국으로 갈까요?',
        {"type": "question", "text": "아빌라\n남을까 떠날까?", "faces": ["KBO프로필/아빌라"]}),
    POINT(), CTA()],
  yt=dict(title='SSG 아빌라 | 메이저리그? 잔류? SSG 내년이 아빌라에 달렸다 #SSG랜더스 #아빌라',
    desc='SSG 랜더스의 내년은 외국인 투수 아빌라가 남느냐에 달렸어요. 아빌라는 9월 10일 2년 잔류 생각에 변함이 없다고 했지만, 9월 29일 LG전 뒤에는 지금은 SSG에 전념하고, 메이저리그는 그때 가서 생각하겠다고 했어요.\nSSG의 내년 가을야구 가능성은 아빌라가 남으면 55%, 떠나면 30%예요.\n\nSSG는 퀄리티스타트(선발 6이닝 이상 3자책 이하)가 35번으로 리그 꼴찌예요. 실책은 81개로 리그에서 두 번째로 적어 수비는 탄탄했지만 선발이 버티지 못했어요. 7월에 합류한 아빌라는 13경기 8승 2패, 평균자책점 1.56이에요. 이숭용 감독은 구단에 "수단과 방법을 가리지 않고 잡아 달라"고 했어요.\n\n가을야구 탈락 5팀(SSG·NC·롯데·한화·키움) 전체 분석은 관련 동영상(롱폼)에서 볼 수 있어요.\n가능성(%)은 영상 제작자의 예상이에요(10월 1일 KBO 기록 기준).\n\n아빌라는 SSG에 남을까요, 미국으로 갈까요? 댓글로 알려 주세요.',
    tags=['SSG 아빌라', '아빌라', 'SSG 랜더스', 'SSG', '아빌라 메이저리그', '이숭용', 'SSG 선발', '퀄리티스타트', '프로야구 탈락 5팀', '2027 가을야구', '프로야구', 'KBO', '야구 쇼츠', '야구자판기'],
    hashtags=['#Shorts', '#아빌라', '#SSG랜더스', '#SSG', '#프로야구', '#KBO', '#야구', '#야구자판기']),
  thumb={"teams": ["SSG"], "img": "누끼/경기_아빌라_포효_SSG제공_HQ", "cutout": True, "cutoutCrop": 0.5, "cutoutLift": 120, "cutoutOverlap": 220, "cutoutFade": 0.62, "top": "메이저리그? 잔류?", "big": "아빌라\n남을까", "logos": False}))   # 10/2 밤 사용자: 카드 빼고 누끼 상체만

# ── 컷5 NC ───────────────────────────────────────────────
CUTS.append(dict(slot='롱폼컷5', topic='NC블론31박치국', team='NC',
  vtitle=['NC 블론세이브 31개', '리그 최다'],
  lines=[
    NEW('엔씨는 블론세이브 삼십일 개로 리그 최다예요', 'NC는 블론세이브 31개로 리그 최다예요',
        {"type": "big", "team": "NC", "text": "블론세이브\n31개 리그 최다"}),
    OLD(23, narr='이기던 경기를 불펜이 지키지 못하면 / 블론세이브라고 하는데요 / 리그 평균은 이십 개 정도예요',
        sub='이기던 경기를 불펜이\n지키지 못하면|블론세이브라고 하는데요|리그 평균은 20개 정도예요',
        scene=dict(SCN[23], items=[dict(SCN[23]['items'][0], at=0), dict(SCN[23]['items'][1], at=2)])),
    OLD(24),
    OLD(25), OLD(27),
    OLD(28, scene=dict({k: v for k, v in SCN[27].items() if k not in ('text', 'stats', 'textAt', 'startLine', 'textSize', 'size')},   # 10/2 밤: 앞 줄(박치국 프로필)과 같은 틀 — 사진·이름·배지 그대로, 글·칩만 바뀜
                   text="두 팀이 박치국을\n두고 경쟁?", textSize=88, textAt=2,
                   stats=[{"k": "NC 리그 최다", "v": "블론 31개", "at": 0}, {"k": "한화 리그 꼴찌", "v": "세이브 16개", "at": 1}])),
    OLD(31),
    NEW('박치국은 두산에 남을까요? / 새 팀으로 갈까요?', '박치국은 두산에 남을까요|새 팀으로 갈까요?',
        {"type": "question", "text": "박치국\n두산 잔류? 이적?", "faces": ["KBO프로필/박치국"]}),
    POINT(), CTA()],
  yt=dict(title='NC 다이노스 | 블론세이브 31개 리그 최다, 박치국 오면 달라질까 #NC다이노스 #박치국',
    desc='NC 다이노스는 블론세이브(이기던 경기를 불펜이 지키지 못한 횟수)가 31개로 리그에서 가장 많아요(리그 평균 19.7개, 10월 1일 KBO 기록). 9월 30일 두산전 9회 말 끝내기 역전패로 가을야구 탈락이 확정됐어요.\n마무리 투수 한 명만 바꿔도 NC의 순위는 달라질 수 있어요.\n\nNC의 득실차는 -40점으로 가을야구에 못 간 팀 가운데 한화 다음으로 작아요. 크게 밀린 팀이 아니라 뒷문이 문제였어요.\n\nNC가 노려 볼 불펜 투수는 두산 박치국이에요. 박치국은 올해 두산 역대 최다 홀드 기록을 세웠지만, 3월에 "FA가 된다면 1순위는 당연히 두산 잔류"라고 했어요. 세이브 리그 꼴찌 한화도 박치국을 원할 수 있어요. NC의 내년 가을야구 가능성은 45%예요.\n\n가을야구 탈락 5팀(SSG·NC·롯데·한화·키움) 전체 분석은 관련 동영상(롱폼)에서 볼 수 있어요.\n가능성(%)은 영상 제작자의 예상이에요.\n\n박치국은 두산에 남을까요, 새 팀으로 갈까요? 댓글로 알려 주세요.',
    tags=['NC 다이노스', 'NC', '블론세이브', 'NC 불펜', '박치국', '박치국 FA', '이호준', 'NC 두산 끝내기', '프로야구 탈락 5팀', '2027 가을야구', '프로야구', 'KBO', '야구 쇼츠', '야구자판기'],
    hashtags=['#Shorts', '#NC다이노스', '#NC', '#박치국', '#프로야구', '#KBO', '#야구', '#야구자판기']),
  thumb={"teams": ["NC"], "top": "", "big": "NC\n리그 최다\n블론세이브", "perLine": True, "lineScale": [0.55, 1, 1]}))   # 10/2 밤 사용자: "NC/리그 최다/블론세이브 이렇게 줄바꿈, 좌우 넓이만큼 키워서"

# ── 컷6 홍창기 ───────────────────────────────────────────
HCK = "KBO프로필/홍창기"
CUTS.append(dict(slot='롱폼컷6', topic='홍창기롯데키움', team='LG',
  vtitle=['홍창기 연봉 삭감', '롯데냐 키움이냐'],
  lines=[
    NEW('엘지 홍창기는 다년계약을 원했는데 연봉이 깎였어요', 'LG 홍창기는 다년계약을\n원했는데 연봉이 깎였어요',
        {"type": "profile", "img": HCK, "name": "홍창기", "sub": "LG · FA 예상", "stats": [{"k": "2026 연봉", "v": "5억 2천만 원", "hi": True, "at": 0}]}),
    OLD(48), OLD(49),
    NEW('홍창기는 이번 겨울 에프에이로 나올 것으로 예상돼요 / 홍창기를 노릴 만한 팀은 롯데와 키움이에요', '홍창기는 이번 겨울 FA로\n나올 것으로 예상돼요|홍창기를 노릴 만한 팀은\n롯데와 키움이에요',
        {"type": "matchup", "left": "롯데", "right": "키움", "score": "vs", "img": HCK, "imgTag": "홍창기", "text": "홍창기를 노릴 팀"}),
    NEW('롯데는 홈런이 리그 꼴찌라 / 한 방을 쳐 줄 타자가 필요해요 / 그런 타자를 못 데려오면 / 출루가 강점인 홍창기로 / 점수를 만드는 길도 있어요',
        '롯데는 홈런이 리그 꼴찌라|한 방을 쳐 줄 타자가 필요해요|그런 타자를 못 데려오면|출루가 강점인 홍창기로|점수를 만드는 길도 있어요',
        {"type": "tiles", "title": "롯데와 홍창기", "items": [{"team": "롯데", "top": "롯데 홈런", "v": "105개", "k": "리그 꼴찌", "color": "#E5484D", "at": 0},
                                                       {"img": HCK, "top": "홍창기 강점", "v": "출루", "k": "점수를 만드는 길", "color": "#1F9D55", "at": 3}]}),
    NEW('키움은 득점이 리그 꼴찌라 / 영입할 타자가 필요해요 / 키움이 돈을 쓰면 / 롯데와 홍창기를 두고 경쟁할 수 있어요',
        '키움은 득점이 리그 꼴찌라|영입할 타자가 필요해요|키움이 돈을 쓰면|롯데와 홍창기를 두고 경쟁할 수 있어요',
        dict(SCN[65], title='팀 득점', items=[dict(SCN[65]['items'][0], label='롯데', sub='득점 9위', at=0), dict(SCN[65]['items'][1], label='키움', sub='득점 10위', at=0)], text='홍창기를 두고 경쟁?', textImg=HCK, textAt=3, size=96)),
    NEW('홍창기는 엘지에 남을까요? / 팀을 옮길까요?', '홍창기는 LG에 남을까요|팀을 옮길까요?',
        {"type": "question", "text": "홍창기\nLG 잔류? 이적?", "faces": [HCK]}),
    POINT(), CTA()],
  yt=dict(title='홍창기 FA | 다년계약 원했는데 연봉 삭감, 롯데냐 키움이냐 #홍창기 #LG트윈스',
    desc='LG 트윈스 홍창기는 1월 6일 다년계약을 원한다고 했는데, 보름 뒤인 1월 22일 연봉이 5억 2천만 원으로 깎였다는 기사가 나왔어요. 이번 겨울 FA로 마음이 흔들릴 수 있는 대어예요.\n홍창기를 노릴 수 있는 팀은 롯데와 키움이에요.\n\n홍창기는 1월 6일 인터뷰에서 구단에 항상 다년계약을 원한다고 말해 왔다고 했어요. 1월 22일 연봉 삭감 기사가 나왔고, LG 차명석 단장은 다년계약을 제안했고 기다린다고만 했어요. FA 명단은 KBO 공시 전 예상이에요.\n\n롯데는 홈런이 리그 꼴찌라 한 방을 쳐 줄 타자가 필요해요. 그런 타자를 못 데려오면 출루가 강점인 홍창기로 점수를 만드는 길도 있어요. 득점 꼴찌 키움도 돈을 쓰면 롯데와 홍창기를 두고 경쟁할 수 있어요(10월 1일 KBO 기록).\n\n가을야구 탈락 5팀(SSG·NC·롯데·한화·키움) 전체 분석은 관련 동영상(롱폼)에서 볼 수 있어요.\n\n홍창기는 LG에 남을까요, 팀을 옮길까요? 댓글로 알려 주세요.',
    tags=['홍창기', '홍창기 FA', '홍창기 연봉', 'LG 트윈스', 'LG', '롯데 자이언츠', '키움 히어로즈', 'FA 예상', '프로야구 FA', '프로야구 탈락 5팀', '프로야구', 'KBO', '야구 쇼츠', '야구자판기'],
    hashtags=['#Shorts', '#홍창기', '#LG트윈스', '#FA', '#롯데자이언츠', '#키움히어로즈', '#프로야구', '#KBO', '#야구자판기']),
  thumb={"teams": ["LG"], "img": "누끼/경기_홍창기_뉴스엔", "cutout": True, "cutoutCrop": 0.5, "cutoutLift": 120, "cutoutOverlap": 220, "cutoutFade": 0.62, "top": "다년계약 원했는데", "big": "홍창기\n연봉 삭감", "logos": False}))   # 10/2 밤 사용자가 보낸 사진(뉴스엔)으로 교체, 상체까지만

# 10/2 사용자 "내 채널에 이미 있는 내용이면 빼": 한화(롱폼④·9/15 한화 7위 이유·9/15 감독 계약 마지막 해와 겹침),
#   하현승(9/13 양키스 41억 거절·9/16 키움 부진 이유·9/19 하현승 키움과 겹침) 은 뺀다 → 4편, 번호를 1~4 로
CUTS = [c for c in CUTS if c['slot'] not in ('롱폼컷2', '롱폼컷3')]
for n_, c in enumerate(CUTS, 1): c['slot'] = f'롱폼컷{n_}'
# ── 콘티로 ───────────────────────────────────────────────
TL = {}
try: TL = json.load(io.open(os.path.join(HERE, 'work', 'timeline_long5.json'), encoding='utf-8'))
except Exception: pass
out = []
CREDIT = {'롱폼컷2': 'SSG 랜더스 제공', '롱폼컷4': '뉴스엔'}   # 10/2 밤: 구단 제공 경기 사진을 쓴 편(아빌라 포효·홍창기 주루) — build.py 가 유튜브.txt 맨 밑 '사진 출처'로 옮김
for n, c in enumerate(CUTS, 1):
    lines, scenes, vmap = [], [], []
    for j, (src, d, sc) in enumerate(c['lines']):
        lines.append(d); vmap.append(src)
        if sc is not None:
            sc = dict(sc); sc['startLine'] = j
            if sc.get('cont') and not (j and src is not None and vmap[j - 1] == src - 1): sc.pop('cont')   # 앞 줄이 롱폼의 바로 앞 줄일 때만 이어 그리기
            scenes.append(sc)
    e = {
        'date': ['2026-10-02', '2026-10-03', '2026-10-03', '2026-10-04'][n - 1], 'gameDate': '2026-10-01', 'series': '야구롱폼', 'vertical': True,   # date = 올리는 날(썸네일·화면 날짜·제목 해시태그)
        'railTitle': '', 'focusTeam': c['team'], 'speed': round(1.2 / 1.1, 4), 'ttsApi': True, 'ttsTempo': 1.1,   # 10/2 사용자: 롱폼 음성(1.1배)을 다시 만들지 않고 렌더에서 ×1.0909 → 숏폼 1.2배. 새 줄도 1.1로 합성해 같은 배속
        'rev': f'1002-cut{n}-v1', 'topic': c['topic'],
        'vtitle': c['vtitle'], 'vbasis': '',   # 10/2 밤 사용자: 컷 쇼츠엔 기준 날짜 글자 없음
        'voiceFrom': {'ep': '2026-10-01_롱폼', 'lines': vmap},
        'source': f'롱폼 {SRC} 에서 잘라 세로로 다시 짬(컷 {n}). ' + ep.get('source', ''),
        'lines': lines, 'scenes': scenes, 'standings': ep.get('standings'),
        'thumb': c['thumb'],
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'] + (f"\n\n사진: {CREDIT[c['slot']]}" if c['slot'] in CREDIT else ''), 'tags': c['yt']['tags'], 'hashtags': c['yt']['hashtags']},
    }
    p = os.path.join(HERE, 'episodes', f"2026-10-02_{c['slot']}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    durs = TL.get('durs') or []
    est = sum((durs[s] if (s is not None and s < len(durs)) else len(l['narr'].replace(' / ', ' ')) * 0.19 + 0.3 * l['narr'].count(' / ')) / (1.0 if l.get('rate') else 1.2 / 1.1) + 0.45 for s, l in zip(vmap, lines)) + 1.0
    newc = sum(len(l['narr'].replace(' / ', ' ')) for s, l in zip(vmap, lines) if s is None and l['narr'] != LN[77]['narr'])
    out.append((p, len(lines), round(est), newc))
for r in out: print(r)
