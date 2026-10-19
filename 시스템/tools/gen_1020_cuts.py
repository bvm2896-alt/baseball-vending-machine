# 10/20 롱폼⑳ 「KIA 한국시리즈 우승 망상회」(episodes/2026-10-19_롱폼.json) → 컷 쇼츠 4편. 세로(1080x1920), 어두운 화면 + 새 캐릭터(망냥이 2).
# 원본 줄은 롱폼 음성을 그대로 쓰고(voiceFrom), 새 줄(훅·질문·관련 영상)만 API 합성. 구독 멘트는 고정음성.
# 10/20 사용자: 4편 모두(① 준PO 3차전 예측 ② 김도영 피해도 점수 난다 ③ 준PO부터 우승 역대 3번 ④ 7차전 김도영이 끝낸다), 첫 줄은 롱폼처럼 망상 경고.
# ①은 10/20 18:30 준PO 3차전 전에 올려야 의미가 있다.
# 실행: python -X utf8 tools/gen_1020_cuts.py  → episodes/2026-10-20_롱폼컷1~4.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-19_롱폼.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
TH = '상황별/썸네일_롱폼20_기아우승망상'   # 롱폼 썸네일
DATE = '2026-10-20'

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

NODREAM = ('dreamNo', 'dreamLabel', 'dreamTitle')

def Qs(narr, sub, text, faces=None, logos=None):
    sc = {"type": "question", "text": text, "mood": "wave", "say": "댓글로 알려줘!", "revealAt": 1}
    if faces: sc["faces"] = ['카드/' + x for x in faces]
    if logos: sc["logos"] = logos
    return NEW(narr, sub, sc, slow=True)

POINT = lambda: NEW('기아 한국시리즈 우승 망상회 전체는 / 하단 관련 영상에 있어요', 'KIA 한국시리즈 우승 망상회 전체는|하단 관련 영상에 있어요',
                    {"type": "photo", "img": TH, "fit": "cover", "text": "", "relArrow": True, "chain": "relvid", "mood": "wave"})
CTA = lambda: (None, {'narr': '채널 구독하고 매일 야구 이슈 받아보세요', 'sub': '채널 구독하고\n매일 야구 이슈 받아보세요!', 'rate': 1.0},   # 고정음성(구독멘트)과 같은 글 → 합성 안 함
                  {"type": "photo", "img": TH, "fit": "cover", "text": "", "chain": "relvid", "cont": True, "mood": "cheer"})
YT_TAIL = '\n\n※ 이 영상은 채널 주인장의 망상이에요. 경기 결과는 모두 예측이에요.\nKIA 한국시리즈 우승 망상회 전체는 하단 관련 영상에 있어요.'
REC = '기록: KBO 기록실·KBO 영문 기록, mykbostats(경기 기록). 기사: 스포츠경향·데일리안·세계일보·MHN·마이데일리·OSEN·뉴스엔(10/14~19), 뉴시스(10/12), 데일리안 2015·디지털타임스 2018(역대 기록)'
CRED = 'KIA 타이거즈 제공, 삼성 라이온즈 제공, KT 위즈 제공, LG 트윈스 제공'
CUTS = []

# ── ① 준PO 3차전 예측: 시라카와 vs 카라스코 → KIA 3연승 ─────────────
CUTS.append(dict(topic='준PO3차전예측시라카와카라스코', vtitle=['준PO 3차전 예측', '시라카와 vs 카라스코'],
  lines=[OLD(0),
    NEW('오늘 준플레이오프 삼차전 선발은 / 기아 시라카와, / 엘지 카라스코예요', '오늘 준플레이오프 3차전 선발은|KIA 시라카와|LG 카라스코예요',
        ppx(8, title="준플레이오프 3차전 · 잠실 · 선발", text="", textAt=None)),
    OLD(9), OLD(10), OLD(11), OLD(13), OLD(14), OLD(19), OLD(30),
    Qs('삼차전 / 엘지가 잠실에서 반격할까요? / 기아가 삼연승으로 끝낼까요?', '3차전|LG가 잠실에서 반격할까요|KIA가 3연승으로 끝낼까요', '3차전\nLG 반격? KIA 3연승?', logos=['LG', 'KIA']),
    POINT(), CTA()],
  yt=dict(title='준플레이오프 3차전 예측 | 시라카와 vs 카라스코, KIA 3연승으로 끝낼까 #준플레이오프 #KIA타이거즈',
    desc='10월 20일 잠실 준플레이오프 3차전 선발은 KIA 시라카와, LG 카라스코예요.\n시라카와는 KBO 포스트시즌 첫 등판이고 LG전 2경기 9⅓이닝 8실점(평균자책점 7.71), 오스틴에게 4타수 3안타 홈런 2개를 맞았어요. 카라스코는 메이저리그 112승 투수로 와일드카드 결정전 6이닝 1실점이었지만, 10월 3일 KIA전에선 4⅓이닝 4실점이었어요.\n두 선발 모두 초반에 흔들리면 승부는 불펜에서 갈리고, 경기 후반 1점을 짜내는 쪽이 이길 공산이 커요. 이 채널의 예측은 접전 끝에 KIA 3연승, 결승타는 카스트로나 나성범 쪽이에요.\n\n여러분은 3차전 LG가 반격할 거라고 보시나요? KIA가 3연승으로 끝낼까요?',
    tags=['준플레이오프 3차전', '3차전 예측', '시라카와', '카라스코', 'KIA LG', 'KIA 타이거즈', 'LG 트윈스', '준플레이오프', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#준플레이오프', '#KIA타이거즈', '#LG트윈스', '#시라카와', '#가을야구', '#야구자판기'])))

# ── ② 김도영을 피해도 점수가 난다 ─────────────────────────────
CUTS.append(dict(topic='김도영피해도점수난다', vtitle=['김도영을 피해도', 'KIA는 점수가 난다'],
  lines=[OLD(0),
    NEW('엘지 염경엽 감독은 / 김도영을 어떻게 잡느냐가 / 중요하다고 했어요', 'LG 염경엽 감독은|김도영을 어떻게 잡느냐가|중요하다고 했어요',
        ppx(20, sub="LG 감독 · 10월 14일", stats=[], viz=[{"type": "stamp", "t": "김도영을 어떻게 잡느냐가 중요", "at": 1.0, "c": "gold", "size": 46}], say="견제…", revealAt=1)),
    OLD(21), OLD(22), OLD(23), OLD(24),
    Qs('삼차전에서도 김도영을 피하면 / 카스트로와 나성범이 / 해결할까요?', '3차전에서도 김도영을 피하면|카스트로와 나성범이|해결할까요', '김도영을 피하면\n카스트로·나성범이 해결?',
       faces=['P18_카스트로_환호', 'P18_나성범_적시타']),
    POINT(), CTA()],
  yt=dict(title='김도영을 피해도 점수가 난다 | 2차전 무안타에도 KIA가 이긴 이유 #김도영 #KIA타이거즈',
    desc='LG 염경엽 감독은 와일드카드 결정전을 이긴 10월 14일, 김도영을 어떻게 잡느냐가 중요하다고 했어요.\n실제로 준플레이오프 2차전 김도영은 안타 없이 볼넷 하나와 몸에 맞는 공 하나로만 나갔어요. 그런데도 KIA는 이겼어요. 1회 4번 카스트로가 결승타를 쳤고 나성범·김선빈·한준수가 연달아 2루타를 쳤어요. 7회엔 LG가 카스트로를 거르자 나성범이 희생플라이로 점수를 냈어요.\n김도영을 피해도 뒤에서 점수가 나는 것, 이번 가을 KIA의 숨은 무기예요.\n\n3차전에서도 김도영을 피하면 카스트로와 나성범이 해결할까요?',
    tags=['김도영', '카스트로', '나성범', '김도영 견제', '염경엽', '준플레이오프 2차전', 'KIA 타이거즈', 'LG 트윈스', '준플레이오프', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#김도영', '#카스트로', '#KIA타이거즈', '#준플레이오프', '#가을야구', '#야구자판기'])))

# ── ③ 준PO부터 올라와 우승한 팀은 역대 3번 ─────────────────────
CUTS.append(dict(topic='준PO부터우승역대3번', vtitle=['준PO부터 우승', '역대 3번뿐'],
  lines=[OLD(0), OLD(1), OLD(2), OLD(31), OLD(85), OLD(84), OLD(86),
    Qs('기아가 / 역대 네 번째 팀이 될까요?', 'KIA가|역대 4번째 팀이 될까요', 'KIA\n역대 4번째 팀 될까?', logos=['KIA']),
    POINT(), CTA()],
  yt=dict(title='준플레이오프부터 올라와 우승한 팀 역대 3번뿐 | KIA 우승 확률 약 17% #KIA타이거즈 #한국시리즈',
    desc='준플레이오프부터 올라와 한국시리즈에서 우승한 팀은 역대 3번뿐이에요. 1992년 롯데가 처음이었고 2001년과 2015년엔 두산이었어요.\nKIA는 해태 시절까지 합쳐 준플레이오프에 4번 올라 4번 모두 졌어요. 이번에 준플레이오프를 통과하면 처음이에요.\n이 채널의 예측은 준플레이오프 3연승, 플레이오프 3승 1패, 한국시리즈는 0승 2패에서 4승 3패로 뒤집는 것. 그러면 KIA는 역대 4번째 팀이 돼요.\n올해 정규시즌 득점과 실점으로 계산한 통과 확률은 준플레이오프 92%, 플레이오프 46%, 한국시리즈 40% — 곱하면 우승 확률 약 17%, 6번 중 1번꼴이에요(이 채널이 직접 계산한 추정치).\n\nKIA가 역대 4번째 팀이 될까요?',
    tags=['KIA 우승', '기아 우승', '준플레이오프', '한국시리즈', 'KIA 타이거즈', '우승 확률', '역대 기록', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#KIA타이거즈', '#한국시리즈', '#준플레이오프', '#가을야구', '#프로야구', '#야구자판기'])))

# ── ④ 한국시리즈 7차전: 피해 다닌 김도영이 끝낸다 ──────────────────
CUTS.append(dict(topic='7차전김도영이끝낸다', vtitle=['한국시리즈 7차전', '김도영이 끝낸다'],
  lines=[OLD(0),
    NEW('한국시리즈가 / 삼승 삼패로 칠차전까지 간다면 / 마지막 한 방은 누가 칠까요?', '한국시리즈가|3승 3패로 7차전까지 간다면|마지막 한 방은 누가 칠까요',
        {"type": "big", "team": "KIA", "text": "한국시리즈 7차전\n마지막 한 방은?", "size": 110, "mood": "think",
         "dreamNo": 11, "dreamLabel": "7차전 예측", "dreamTitle": "한국시리즈 · 수원"}),
    OLD(77, ppx(77, drop=NODREAM)), OLD(78), OLD(79), OLD(80), OLD(81), OLD(82), OLD(83),
    Qs('마지막 한 방 / 김도영일까요? / 다른 타자일까요?', '마지막 한 방|김도영일까요|다른 타자일까요', '마지막 한 방\n김도영? 다른 타자?', faces=['P17_김도영_질주']),
    POINT(), CTA()],
  yt=dict(title='한국시리즈 7차전 예측 | 시리즈 내내 피해 다닌 김도영이 끝낸다 #김도영 #한국시리즈',
    desc='이 채널의 예측대로 한국시리즈가 KIA와 KT의 3승 3패, 7차전까지 간다면 마지막 한 방은 누가 칠까요?\n7차전은 수원, 소형준(평균자책점 3.15)과 올러(3.13)라 선발로는 차이가 없어요. 승부는 막판 한 타석에서 갈릴 공산이 커요.\nKT는 시리즈 내내 김도영을 피하겠지만, 7차전 막판 만루라면 거르는 순간 점수를 줘서 더는 피할 수 없어요. 그때 마주할 투수는 30세이브 무패 마무리 박영현일 공산이 커요.\n김도영은 정규시즌 마지막 날 결승 투런으로 홈런왕을 확정했고, 준플레이오프 1차전에서도 홈런 2방을 쳤어요. 이 채널의 예측은 KIA 4승 3패 우승이에요.\n\n마지막 한 방, 김도영일까요? 다른 타자일까요?',
    tags=['김도영', '한국시리즈', '한국시리즈 7차전', '박영현', '올러', '소형준', 'KIA KT', 'KIA 타이거즈', 'KT 위즈', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#김도영', '#한국시리즈', '#KIA타이거즈', '#KT위즈', '#가을야구', '#야구자판기'])))

out = []
for n, c in enumerate(CUTS, 1):
    lines, scenes, vmap = [], [], []; prev0 = None
    for j, (src, d, sc) in enumerate(c['lines']):
        lines.append(d); vmap.append(src)
        if sc is not None:
            o0 = sc.get('startLine'); sc = dict(sc); sc['startLine'] = j
            if sc.get('cont') and sc.get('chain') != 'relvid' and not (j and src is not None and (vmap[j - 1] == src - 1 or prev0 == src - 1)): sc.pop('cont')
            if sc.get('textAt') is None: sc.pop('textAt', None)
            prev0 = o0
            scenes.append(sc)
    e = {
        'date': DATE, 'gameDate': '2026-10-20', 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': 'KIA', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': ep.get('ttsTempo', 1.25), 'ttsTempoSlow': ep.get('ttsTempoSlow', 1.2),
        'rev': f'1020-cut{n}-v1', 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18, 'mascot': True, 'theme': 'dark',
        'voiceFrom': {'ep': '2026-10-19_롱폼', 'lines': vmap},
        'source': f'롱폼 {SRC} 에서 잘라 세로로 다시 짬(컷 {n}). ' + ep.get('source', ''),
        'lines': lines, 'scenes': scenes,
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'] + YT_TAIL + f"\n\n{REC}\n사진: {CRED}", 'tags': c['yt']['tags'], 'hashtags': c['yt']['hashtags']},
    }
    p = os.path.join(HERE, 'episodes', f"{DATE}_롱폼컷{n}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    est = sum(len(l['narr'].replace(' / ', ' ')) * 0.14 + 0.3 * 0.6 * l['narr'].count(' / ') + 0.45 * 0.6 for l in lines) + 1.0
    newc = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for s, l in zip(vmap, lines) if s is None and not l['narr'].startswith('채널 구독하고'))
    out.append((n, c['topic'], len(lines), len(scenes), round(est), newc))
    for b in (x for l in lines for x in l['narr'].split(' / ')):
        if len(re.sub(r'[\s,?+]', '', b)) > 22: print('호흡 초과', n, b)
for r in out: print(r)
print('새로 합성 합계(구독 멘트 빼고)', sum(r[5] for r in out), '자')
