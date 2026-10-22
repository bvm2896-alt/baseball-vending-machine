# 10/21 롱폼⑱ 「2026 골든글러브 예상 | 외야 4명 중 1명은 떨어진다」(episodes/2026-10-18_롱폼.json) → 컷 쇼츠 6편(세로 1080x1920).
# 10/21 사용자 "골든글러브 숏츠로 쪼개줘" + "쪼개기 하고 골든글러브 전용 배치파일로 만들어줘"
#   → 파일 이름을 롱폼 날짜(2026-10-18_롱폼컷1~6.json)로 둬서 날마다 만드는 컷(가장 최근 날짜)과 섞이지 않게 하고,
#     야구롱폼\골든글러브_숏츠만들기.cmd 가 이 6편만 만든다(long_build.py --cuts 2026-10-18_롱폼컷).
# 원본 줄은 롱폼 음성을 그대로 쓰고(voiceFrom), 새 줄(훅·질문·관련 영상)만 API 합성. 구독 멘트는 고정음성.
# 편마다 챕터 하나: ① 외야 4명 중 1명 탈락 ② 포수 허인서 ③ 1루 오스틴 vs 디아즈 ④ 유격 박성한 vs 김주원 ⑤ 3루 김도영 ⑥ 지명 강백호 vs 최형우
# 원 안 사진은 프로필 사진(G18P_)만 — 프로필이 없는 선수(김형준·김주원·최형우)가 낀 질문은 구단 로고로.
# 실행: python -X utf8 tools/gen_1018_gg_cuts.py  → episodes/2026-10-18_롱폼컷1~6.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-18_롱폼.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
TH = '상황별/썸네일_롱폼18_골든글러브'   # 롱폼 썸네일(관련 영상 가리키기)
DATE = '2026-10-18'

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
    pcs = [wrap16(x + ('?' if re.search(r'(까요|(?<![\s만끝떠])나요)$', x) else '')) for x in sub.split('|')]
    assert len(pcs) == len(narr.split(' / ')), (narr, sub)
    d = {'narr': narr, 'sub': '|'.join(pcs)}
    if slow: d['pace'] = 'slow'
    return (None, d, scene)

def OLD(i, scene=None):
    d = copy.deepcopy(LN[i]); d.pop('gapAfter', None)
    sc = copy.deepcopy(scene if scene is not None else SCN.get(i))
    return (i, d, sc)

def ppx(i, drop=(), **kw):
    s = copy.deepcopy(SCN[i]); [s.pop(k, None) for k in ('chain', 'cont') + tuple(drop)]; s.update(kw); return s

def Qs(narr, sub, text, faces=None, logos=None):
    sc = {"type": "question", "text": text, "mood": "wave", "say": "댓글로 알려줘!", "revealAt": 1}
    if faces: sc["faces"] = ['카드/' + x for x in faces]
    if logos: sc["logos"] = logos
    return NEW(narr, sub, sc, slow=True)

POINT = lambda: NEW('2026 골든글러브 예상 전체는 / 하단 관련 영상에 있어요', '2026 골든글러브 예상 전체는|하단 관련 영상에 있어요',
                    {"type": "photo", "img": TH, "fit": "cover", "text": "", "relArrow": True, "chain": "relvid", "mood": "wave"})
CTA = lambda: (None, {'narr': '채널 구독하고 매일 야구 이슈 받아보세요', 'sub': '채널 구독하고\n매일 야구 이슈 받아보세요!', 'rate': 1.0},   # 고정음성(구독멘트)과 같은 글 → 합성 안 함
                  {"type": "photo", "img": TH, "fit": "cover", "text": "", "chain": "relvid", "cont": True, "mood": "cheer"})
YT_TAIL = ('\n\n영상 속 수상자 예상은 모두 야구자판기의 예상이에요. 수상자는 12월 8일 시상식에서 공개돼요.'
           '\n투수부터 지명타자까지 8개 포지션 10자리 예상 전체는 하단 관련 영상에 있어요.')
REC = '기록 출처: KBO 보도자료 「2026 신한 SOL KBO 골든글러브 후보 발표」(10/17, 후보 명단·정규시즌 기록)'
CRED = '사진 출처: 각 구단 제공, 스타뉴스, 엑스포츠뉴스, 스포티비뉴스, 스포츠서울, 일간스포츠, 노컷뉴스, 스포츠조선, 스포츠경향, OSEN, 뉴시스, 연합뉴스, 뉴스1, 각 구단 공식 프로필'
OF4 = ['G18P_구자욱', 'G18P_레이예스', 'G18P_최원준', 'G18P_힐리어드']
CUTS = []

# ── ① 외야 4명 중 1명 탈락 ─────────────────────────────────
CUTS.append(dict(topic='골든글러브외야4명중1명탈락', vtitle=['골든글러브 외야', '4명 중 1명 탈락'],
  lines=[
    NEW('외야 골든글러브는 세 자리, / 타이틀을 딴 네 명 중 / 한 명은 떨어져요', '외야 골든글러브는 3자리|타이틀을 딴 4명 중|1명은 떨어져요',
        ppx(1, chain='of4', textAt=2)),
    OLD(2), OLD(82), OLD(85), OLD(88), OLD(90), OLD(94), OLD(95), OLD(96), OLD(97), OLD(99), OLD(101),
    Qs('여러분은 / 네 명 중 누가 떨어질 것 같나요?', '여러분은|4명 중 누가 떨어질 것 같나요', '외야 4명 중\n누가 떨어질까?', faces=OF4),
    POINT(), CTA()],
  yt=dict(title='외야 골든글러브 예상 | 구자욱·레이예스·최원준·힐리어드, 4명 중 1명은 떨어진다 #골든글러브 #구자욱',
    desc='올해 외야수 네 명이 모두 타이틀을 가져갔어요. 타격왕 구자욱(삼성, 타율 0.371), KBO 한 시즌 최다 안타 신기록 레이예스(롯데, 211안타), 득점왕 최원준(KT, 208안타·125득점), 타점왕 힐리어드(KT, 44홈런·139타점).\n그런데 외야 골든글러브는 세 자리뿐이에요. 네 명이 함께 받은 건 동점이 나온 2004년 한 번뿐이었어요.\n약점도 하나씩 있어요. 구자욱은 114경기로 가장 적게 뛰었고, 힐리어드는 타율 0.304로 가장 낮고, 최원준은 홈런 9개로 가장 적고 시즌 막판 방망이 투척으로 비판도 받았어요.\n이 채널의 예상은 구자욱·레이예스·힐리어드예요.\n\n여러분은 네 명 중 누가 떨어질 것 같나요?',
    tags=['골든글러브', '외야 골든글러브', '골든글러브 예상', '구자욱', '레이예스', '최원준', '힐리어드', '2026 골든글러브', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#골든글러브', '#구자욱', '#레이예스', '#최원준', '#힐리어드', '#야구자판기'],
    src='인터뷰·반응 출처: 스포츠경향(구자욱 9/7·힐리어드 10/11), 일간스포츠(레이예스 10/12), 노컷뉴스(팬 반응 10/11)')))

# ── ② 포수: 15년 만에 새 주인, 허인서 ─────────────────────────
CUTS.append(dict(topic='골든글러브포수허인서', vtitle=['포수 골든글러브', '15년 만에 새 주인'],
  lines=[
    NEW('포수 골든글러브가 / 십오 년 만에 / 새 주인을 맞아요', '포수 골든글러브가|15년 만에|새 주인을 맞아요', ppx(29, chain='yk')),
    OLD(29, ppx(29, chain='yk', cont=True)), OLD(30), OLD(32), OLD(33), OLD(34), OLD(35), OLD(37), OLD(38),
    Qs('허인서가 / 첫 골든글러브를 받을까요? / 김형준이 뒤집을까요?', '허인서가|첫 골든글러브를 받을까요|김형준이 뒤집을까요', '포수 골든글러브\n허인서? 김형준?', logos=['한화', 'NC']),
    POINT(), CTA()],
  yt=dict(title='허인서 골든글러브 예상 | 양의지·강민호 시대 끝, 15년 만에 바뀌는 포수 주인 #허인서 #골든글러브',
    desc='2011년부터 지난해까지 포수 골든글러브는 양의지 아니면 강민호였어요. 올해는 두 선수 모두 포수 수비 720이닝을 못 채워 후보에 없어요.\n가장 앞선 선수는 한화 허인서예요. 타율 0.283, 20홈런, 79타점으로 홈런과 타점 모두 포수 후보 중 1위예요. 이글스 포수의 20홈런은 1989년 이후 처음이고, 신인왕까지 같이 받으면 포수로는 1990년 이후 36년 만이에요.\n경쟁자 NC 김형준은 17홈런, 66타점, 도루 저지율 31.9%예요. 이 채널의 예상은 허인서예요.\n\n허인서가 첫 골든글러브를 받을까요? 김형준이 뒤집을까요?',
    tags=['허인서', '포수 골든글러브', '골든글러브', '골든글러브 예상', '김형준', '양의지', '강민호', '한화 이글스', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#허인서', '#골든글러브', '#한화이글스', '#김형준', '#야구자판기'],
    src='인터뷰 출처: 서울신문(허인서 10/13)')))

# ── ③ 1루: 오스틴 vs 디아즈 ─────────────────────────────────
CUTS.append(dict(topic='골든글러브1루오스틴디아즈', vtitle=['1루 골든글러브', '오스틴 vs 디아즈'],
  lines=[
    NEW('오피에스 리그 일 위인데 / 타이틀은 하나도 없는 오스틴, / 골든글러브는 받을 수 있을까요?', 'OPS 리그 1위인데|타이틀은 하나도 없는 오스틴|골든글러브는 받을 수 있을까요',
        ppx(40)),
    OLD(41), OLD(43), OLD(44), OLD(45), OLD(46), OLD(47), OLD(48), OLD(49),
    Qs('일루 골든글러브 / 오스틴일까요? / 디아즈일까요?', '1루 골든글러브|오스틴일까요|디아즈일까요', '1루 골든글러브\n오스틴? 디아즈?', faces=['G18P_오스틴', 'G18P_디아즈']),
    POINT(), CTA()],
  yt=dict(title='오스틴 디아즈 | 1루 골든글러브 예상, OPS 1위 vs 지난해 수상자 #오스틴 #디아즈',
    desc='1루 골든글러브는 LG 오스틴과 삼성 디아즈, 사실상 두 명의 싸움이에요.\n오스틴은 타율 0.331, 41홈런, 127타점에 OPS 1.062로 리그 1위예요. 그런데 홈런과 타점 모두 3위라 공식 타이틀은 하나도 없고, 1루 수비는 723이닝으로 기준 720이닝을 겨우 넘겼어요.\n지난해 수상자 디아즈는 타율 0.305, 26홈런, 129타점(2위)으로 2년 연속 120타점을 넘겼고, 1루 수비는 1,200이닝이에요.\n이 채널의 예상은 OPS 1위에 홈런이 15개 많은 오스틴. 다만 투표인단이 수비를 크게 본다면 디아즈의 2년 연속 수상도 가능해요.\n\n1루 골든글러브, 오스틴일까요? 디아즈일까요?',
    tags=['오스틴', '디아즈', '1루 골든글러브', '골든글러브', '골든글러브 예상', 'LG 트윈스', '삼성 라이온즈', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#오스틴', '#디아즈', '#골든글러브', '#LG트윈스', '#삼성라이온즈', '#야구자판기'],
    src='인터뷰 출처: SPOTV뉴스(오스틴 10/7)')))

# ── ④ 유격: 박성한 vs 김주원 ─────────────────────────────────
CUTS.append(dict(topic='골든글러브유격박성한김주원', vtitle=['유격수 골든글러브', '박성한 vs 김주원'],
  lines=[
    NEW('유격수 최다 출루 신기록을 쓴 박성한, / 첫 골든글러브를 받을 차례예요', '유격수 최다 출루 신기록을 쓴 박성한|첫 골든글러브를 받을 차례예요',
        ppx(71, chain='ob')),
    OLD(72), OLD(68), OLD(70), OLD(73), OLD(74), OLD(75), OLD(76), OLD(78),
    Qs('유격수 골든글러브 / 박성한일까요? / 김주원일까요?', '유격수 골든글러브|박성한일까요|김주원일까요', '유격수 골든글러브\n박성한? 김주원?', logos=['SSG', 'NC']),
    POINT(), CTA()],
  yt=dict(title='박성한 김주원 | 유격수 골든글러브 예상, 최다 출루 신기록의 첫 수상? #박성한 #김주원',
    desc='SSG 박성한은 올해 타율 3할 3푼, 175안타, 출루율 0.429를 기록했고 한 경기도 빠지지 않았어요.\n한 시즌 269번 출루해 1994년의 253번을 넘어 유격수 최다 출루 기록을 새로 썼어요. 이숭용 감독도 올해는 박성한이 꼭 골든글러브를 받아야 하지 않겠냐며 힘을 실었어요.\n지난해 수상자 NC 김주원은 18홈런·30도루로 장타와 발을 다 갖췄지만 타율은 2할 8푼으로 박성한보다 5푼 낮아요. 김주원은 성한이 형이 정말 잘하고 있어서 하늘에 맡기겠다고 했어요.\n이 채널의 예상은 아직 골든글러브가 없는 박성한이에요.\n\n유격수 골든글러브, 박성한일까요? 김주원일까요?',
    tags=['박성한', '김주원', '유격수 골든글러브', '골든글러브', '골든글러브 예상', 'SSG 랜더스', 'NC 다이노스', '이숭용', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#박성한', '#김주원', '#골든글러브', '#SSG랜더스', '#NC다이노스', '#야구자판기'],
    src='인터뷰 출처: 엑스포츠뉴스(박성한 9/30·이숭용 감독 10/11), 일간스포츠(김주원 9/29)')))

# ── ⑤ 3루: 김도영 ─────────────────────────────────────────
CUTS.append(dict(topic='골든글러브3루김도영', vtitle=['3루 골든글러브', '김도영 45홈런'],
  lines=[
    NEW('홈런왕에 장타율왕까지, / 삼루 골든글러브는 / 고민할 게 없어요', '홈런왕에 장타율왕까지|3루 골든글러브는|고민할 게 없어요', ppx(59, chain='kdy')),
    OLD(59, ppx(59, chain='kdy', cont=True)), OLD(60), OLD(61), OLD(62), OLD(63), OLD(64), OLD(65), OLD(66),
    Qs('김도영 / 만장일치 수상까지 갈까요?', '김도영|만장일치 수상까지 갈까요', '김도영\n만장일치까지?', faces=['G18P_김도영']),
    POINT(), CTA()],
  yt=dict(title='김도영 골든글러브 예상 | 45홈런 홈런왕·장타율왕, 3루는 고민 없다 #김도영 #골든글러브',
    desc='KIA 김도영은 올해 45홈런으로 홈런왕, 장타율 0.647로 장타율왕까지 타이틀 두 개를 가져갔어요. 타율 0.308, 118타점, 120득점까지 빠지는 게 없어요.\n시즌 마지막 날 8회 결승 투런으로 45호를 쳐 힐리어드(44개)를 한 개 차로 따돌렸고, 이 한 방이 프로 통산 100호 홈런이었어요. 김도영은 경기 뒤 "나 올해 진짜 왜 이러지"라고 했대요.\n한화 노시환도 29홈런, 96타점을 쳤지만 김도영을 넘어서기는 어려워 보여요. 골든글러브는 정규시즌 성적만 봐요.\n\n김도영, 만장일치 수상까지 갈까요?',
    tags=['김도영', '3루 골든글러브', '골든글러브', '골든글러브 예상', '김도영 홈런왕', '김도영 45홈런', '노시환', 'KIA 타이거즈', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#김도영', '#골든글러브', '#KIA타이거즈', '#홈런왕', '#야구자판기'],
    src='인터뷰 출처: 스포츠경향(김도영 10/12)')))

# ── ⑥ 지명: 강백호 vs 최형우 ─────────────────────────────────
CUTS.append(dict(topic='골든글러브지명강백호최형우', vtitle=['지명타자 골든글러브', '강백호 vs 최형우'],
  lines=[
    NEW('지명타자 골든글러브는 / 강백호의 첫 수상이냐, / 최형우의 최고령 기록이냐예요', '지명타자 골든글러브는|강백호의 첫 수상이냐|최형우의 최고령 기록이냐예요',
        ppx(110, drop=('text', 'textAt'), rows=[dict(r, at=-1) for r in SCN[110]['rows']])),
    OLD(105), OLD(106), OLD(107), OLD(108), OLD(109), OLD(110), OLD(111),
    Qs('지명타자 골든글러브 / 강백호일까요? / 최형우일까요?', '지명타자 골든글러브|강백호일까요|최형우일까요', '지명타자 골든글러브\n강백호? 최형우?', logos=['한화', '삼성']),
    POINT(), CTA()],
  yt=dict(title='강백호 최형우 | 지명타자 골든글러브 예상, 첫 수상 vs 최고령 기록 #강백호 #최형우',
    desc='지명타자 골든글러브 후보는 삼성 최형우, 한화 강백호, SSG 김재환 세 명이에요.\n강백호는 34홈런(4위), 118타점(공동 4위). 2020·2021년 1루수로 두 번 받았지만 지명타자로는 아직 없어요.\n최형우는 타율 0.301, 18홈런, 106타점. 올해도 받으면 지난해 본인이 세운 최고령 수상 기록을 또 깨고, 통산 9번째 수상으로 역대 단독 3위가 돼요.\n이 채널의 예상은 홈런 16개·타점 12개 차이로 강백호예요.\n\n지명타자 골든글러브, 강백호일까요? 최형우일까요?',
    tags=['강백호', '최형우', '지명타자 골든글러브', '골든글러브', '골든글러브 예상', '한화 이글스', '삼성 라이온즈', '김재환', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#강백호', '#최형우', '#골든글러브', '#한화이글스', '#삼성라이온즈', '#야구자판기'],
    src='인터뷰 출처: 머니투데이(강백호 9/9)')))

# 10/21 사용자 "외야면 외야 후보 4명 넣고 1루도 그렇고 지명타자도 그래" → 컷1·3·6 은 누끼 여러 명을 합친 그룹 이미지(누끼/그룹_GG컷N_*.png, 합치기는 클라우드 compose.py)
# 10/21 사용자 "왜 썸네일은 안만들어?" → 컷마다 세로 썸네일(thumb_issue.html, 10/21 컷 형식: 사진 위 + 큰 제목 2줄 아래)
THUMB_BASE = {"halo": 18, "cutout": True, "cutoutLift": 180, "cutoutOverlap": 330, "cutoutFade": 0.62, "ph": 1000, "logos": False, "noPills": True, "top": "", "perLine": True}
THUMBS = {
 "1": {
  "img": "누끼/그룹_GG컷1_외야4명",
  "cutoutCrop": 0.8,
  "big": "외야 골든글러브\n4명 중 1명 탈락",
  "color": "#1F2937",
  "teams": [
   "삼성",
   "롯데",
   "KT"
  ]
 },
 "2": {
  "img": "카드/G18_허인서_A",
  "cutoutCrop": 1.0,
  "big": "허인서 20홈런\n포수 새 주인",
  "color": "#F37321",
  "teams": [
   "한화"
  ]
 },
 "3": {
  "img": "누끼/그룹_GG컷3_오스틴_디아즈",
  "cutoutCrop": 0.8,
  "big": "오스틴 vs 디아즈\n1루 주인은?",
  "color": "#C30452",
  "teams": [
   "LG",
   "삼성"
  ]
 },
 "4": {
  "img": "카드/G18_박성한_B",
  "cutoutCrop": 0.85,
  "big": "박성한 첫 수상?\n유격수 최다 출루",
  "color": "#CE0E2D",
  "teams": [
   "SSG"
  ]
 },
 "5": {
  "img": "누끼/경기_김도영_45호_포효_1012_스포츠조선_center_mid",
  "cutoutCrop": 0.6,
  "big": "김도영 45홈런\n3루는 고민 없다",
  "color": "#9F1239",
  "teams": [
   "KIA"
  ]
 },
 "6": {
  "img": "누끼/그룹_GG컷6_강백호_최형우",
  "cutoutCrop": 0.8,
  "big": "강백호 vs 최형우\n지명 골든글러브",
  "color": "#1E3A8A",
  "teams": [
   "한화",
   "삼성"
  ]
 }
}

out = []
for n, c in enumerate(CUTS, 1):
    lines, scenes, vmap = [], [], []; prev0 = None
    for j, (src, d, sc) in enumerate(c['lines']):
        lines.append(d); vmap.append(src)
        if sc is not None:
            o0 = sc.get('startLine'); sc = dict(sc); sc['startLine'] = j
            # cont 는 바로 앞 장면이 같은 묶음(chain)일 때만 남긴다(롱폼에서 사이 장면을 뺐어도 같은 묶음이면 이어짐)
            if sc.get('cont') and not (scenes and sc.get('chain') and scenes[-1].get('chain') == sc.get('chain')): sc.pop('cont')
            if sc.get('textAt') is None: sc.pop('textAt', None)
            prev0 = o0
            scenes.append(sc)
    e = {
        'date': DATE, 'gameDate': '2026-10-17', 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': ep.get('ttsTempo', 1.2), 'ttsTempoSlow': ep.get('ttsTempoSlow', 1.15),
        'rev': f'1021-gg-cut{n}-v1', 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': '2026-10-18_롱폼', 'lines': vmap},
        'source': f'롱폼 {SRC} 에서 잘라 세로로 다시 짬(골든글러브 컷 {n}). ' + ep.get('source', ''),
        'lines': lines, 'scenes': scenes,
        'thumb': dict(THUMB_BASE, **THUMBS[str(n)]),
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'] + YT_TAIL + f"\n\n{REC}\n{c['yt']['src']}\n{CRED}", 'tags': c['yt']['tags'], 'hashtags': c['yt']['hashtags']},
    }
    p = os.path.join(HERE, 'episodes', f"{DATE}_롱폼컷{n}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    est = sum(len(l['narr'].replace(' / ', ' ')) * 0.14 + 0.3 * 0.6 * l['narr'].count(' / ') + 0.45 * 0.6 for l in lines) + 1.0
    newc = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for s, l in zip(vmap, lines) if s is None and not l['narr'].startswith('채널 구독하고'))
    out.append((n, c['topic'], len(lines), len(scenes), round(est), newc, len(e['youtube']['title'])))
    for b in (x for l in lines for x in l['narr'].split(' / ')):
        if len(re.sub(r'[\s,?+]', '', b)) > 22: print('호흡 초과', n, b)
for r in out: print(r)
print('새로 합성 합계(구독 멘트 빼고)', sum(r[5] for r in out), '자')
