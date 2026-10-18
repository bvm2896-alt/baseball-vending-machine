# 10/18 밤 롱폼 「준PO 2차전 리뷰 · 승부를 가른 이유 · 3차전 예측」(episodes/2026-10-18_롱폼2.json) → 컷 쇼츠 5편. 세로(1080x1920).
# 원본 줄은 롱폼 음성을 그대로 쓰고(voiceFrom), 새 줄(훅·질문·관련 영상)만 API 합성. 3차전이 10/20(화)이라 컷은 10/19 업로드(date).
# 실행: python -X utf8 tools/gen_1018_cuts.py  → episodes/2026-10-19_롱폼컷1~5.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-18_롱폼2.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
TH = '상황별/썸네일_롱폼19_준PO2'   # 롱폼 썸네일
DATE = '2026-10-19'

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
CUTS = []

# ── 1 2차전 리뷰: 1회 5점 ─────────────────────────────
CUTS.append(dict(topic='준PO2차전리뷰1회5점', vtitle=['준PO 2차전', 'KIA 6-3 LG'],
  lines=[OLD(0), OLD(1), OLD(7), OLD(8), OLD(9), OLD(10), OLD(11), OLD(20), QFINAL(), POINT(), CTA()],
  yt=dict(title='준플레이오프 2차전 | KIA 6-3 LG, 1회 안타 6개로 5점 빅이닝 #KIA타이거즈 #준플레이오프',
    desc='2026 준플레이오프 2차전에서 KIA 타이거즈가 LG 트윈스를 6대3으로 이겼어요. 승부는 1회말에 갈렸어요.\n원 아웃에서 박재현이 안타와 도루로 2루에 갔고 김도영이 볼넷을 고른 뒤 카스트로가 결승 적시타를 쳤어요. 이어 나성범·김선빈·한준수가 세 타자 연속 2루타를 쳐 5대0을 만들었고, LG 선발 임찬규는 아웃 하나만 잡고 내려갔어요. KIA는 1회에만 가을야구 타이 기록을 네 개 남겼어요.\n\n3차전, LG가 잠실에서 반격할까요? KIA가 3연승으로 끝낼까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['준플레이오프 2차전', '준플레이오프', 'KIA LG', 'KIA 타이거즈', 'LG 트윈스', '카스트로', '임찬규', '나성범', '김선빈', '한준수', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#준플레이오프', '#KIA타이거즈', '#LG트윈스', '#가을야구', '#프로야구', '#야구자판기'])))

# ── 2 올러, LG의 중심 타선 봉쇄 ───────────────────────
CUTS.append(dict(topic='올러LG중심타선봉쇄', vtitle=['올러', 'LG의 중심 타선 봉쇄'],
  lines=[
    NEW('올러가 / 엘지의 중심 타선을 / 팔타수 무안타로 막았어요', '올러가|LG의 중심 타선을|8타수 무안타로 막았어요', ppx(16)),
    OLD(35), OLD(36), OLD(37), OLD(41), OLD(42), OLD(39), OLD(40),
    Qs('삼차전에서 엘지의 중심 타선은 / 살아날까요? / 또 막힐까요?', '3차전에서 LG의 중심 타선은|살아날까요|또 막힐까요', 'LG의 중심 타선\n살아날까? 또 막힐까?', ['P18_오스틴_타격', 'P17_문보경_10호']),
    POINT(), CTA()],
  yt=dict(title='올러 6이닝 2실점 | LG의 중심 타선 8타수 무안타, 최고 154km #올러 #KIA타이거즈',
    desc='KIA 타이거즈 올러가 준플레이오프 2차전에서 6이닝 2실점으로 승리 투수가 됐어요. 오스틴·문정빈·문보경 LG의 중심 타선은 올러를 상대로 8타수 무안타, 삼진 4개였어요.\n올러의 가장 빠른 공은 154km였고 빠른 공 38개와 슬라이더 37개를 중심으로 던졌어요. 1·2차전을 합치면 LG의 중심 타선은 22타수 3안타예요. 이범호 감독은 공이 90개를 넘어 바꿨고, 남은 3이닝은 불펜으로 막을 수 있다고 봤다고 했어요.\n\n3차전에서 LG의 중심 타선은 살아날까요? 또 막힐까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['올러', 'KIA 올러', '오스틴', '문보경', '문정빈', 'LG 중심타선', '준플레이오프 2차전', 'KIA 타이거즈', 'LG 트윈스', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#올러', '#KIA타이거즈', '#LG트윈스', '#준플레이오프', '#프로야구', '#야구자판기'])))

# ── 3 LG 라인업 변화 · 이재원 4삼진 ────────────────────
CUTS.append(dict(topic='LG라인업변화이재원', vtitle=['LG 라인업 변화', '한 자리만 통했다'],
  lines=[
    NEW('엘지가 꺼낸 / 라인업 변화는 / 한 자리만 통했어요', 'LG가 꺼낸|라인업 변화는|한 자리만 통했어요', ppx(5)),
    OLD(50), OLD(51), OLD(52), OLD(53), OLD(55), OLD(56),
    Qs('삼차전 엘지 라인업 / 또 바꿀까요? / 그대로 갈까요?', '3차전 LG 라인업|또 바꿀까요|그대로 갈까요', 'LG 3차전 라인업\n또 바꿀까? 그대로?', ['P18_박해민_견제사', 'P18_이재원']),
    POINT(), CTA()],
  yt=dict(title='LG 라인업 변화 | 박해민 1번 3안타, 이재원 첫 선발 4삼진 #LG트윈스 #준플레이오프',
    desc='LG 트윈스는 준플레이오프 2차전에서 1번 홍창기를 빼고 박해민을 1번, 이재원을 우익수 선발로 넣었어요. 염경엽 감독은 회의를 해 보니 언젠가 쓸 거면 빨리 쓰자는 의견이 많아 이재원을 선발로 냈다고 했어요.\n박해민은 1차전에 이어 이틀 연속 3안타를 쳤지만, 2번으로 올라온 송찬의와 이재원은 8타수 무안타·삼진 4개였어요. 이재원은 포스트시즌 첫 선발에서 네 타석 모두 삼진이었고, 8회 투 아웃 1·2루에서도 대타 없이 나섰어요. 염경엽 감독은 이재원도 지금은 경험하는 단계라고 했어요.\n\n3차전 LG 라인업, 또 바꿀까요? 그대로 갈까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['이재원', '박해민', '송찬의', '홍창기', '염경엽', 'LG 라인업', 'LG 트윈스', '준플레이오프 2차전', '준플레이오프', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#LG트윈스', '#이재원', '#박해민', '#준플레이오프', '#프로야구', '#야구자판기'])))

# ── 4 한준수 견제사 ───────────────────────────────────
CUTS.append(dict(topic='한준수견제사', vtitle=['포수 한준수', '공격·수비 다 했다'],
  lines=[OLD(57), OLD(14), OLD(58), OLD(59), OLD(60), OLD(61), OLD(62),
    Qs('이차전 숨은 엠브이피는 / 한준수일까요? / 올러일까요?', '2차전 숨은 MVP는|한준수일까요|올러일까요', '2차전 숨은 MVP\n한준수? 올러?', ['P18_한준수_세리머니', 'P18_올러_포효']),
    POINT(), CTA()],
  yt=dict(title='한준수 1회 적시 2루타·3회 견제사 | KIA 포수가 끊은 LG 흐름 #KIA타이거즈 #한준수',
    desc='KIA 타이거즈 포수 한준수가 준플레이오프 2차전에서 공격과 수비 모두 제 몫을 했어요. 1회 세 타자 연속 2루타의 마지막 적시 2루타를 쳤고, 3회 투 아웃 1·2루에서는 1루로 공을 던져 리드가 길었던 박해민을 잡아냈어요.\n이범호 감독은 경기 전 올러가 한준수와 할 때 LG전 성적이 훨씬 좋았다고 했고, 관중이 많아 1루 코치의 콜이 잘 안 들릴 수 있으니 그 빈틈을 파고들자고 했대요. 한준수는 팀에 민폐만 끼치지 말자는 생각이었다고 했어요.\n\n2차전 숨은 MVP는 한준수일까요? 올러일까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['한준수', 'KIA 포수', '견제사', '올러', '박해민', '이범호', 'KIA 타이거즈', '준플레이오프 2차전', '준플레이오프', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#한준수', '#KIA타이거즈', '#준플레이오프', '#가을야구', '#프로야구', '#야구자판기'])))

# ── 5 3차전 예측 시라카와 vs 카라스코 ──────────────────
CUTS.append(dict(topic='3차전시라카와카라스코', vtitle=['3차전 선발', '시라카와 vs 카라스코'],
  lines=[OLD(66), OLD(67), OLD(68), OLD(70), OLD(71), OLD(91), OLD(92), QFINAL(), POINT(), CTA()],
  yt=dict(title='준플레이오프 3차전 예측 | 시라카와 vs 카라스코, LG전 피홈런 4개 #준플레이오프 #시라카와',
    desc='10월 20일 잠실에서 열리는 준플레이오프 3차전 선발은 KIA 시라카와, LG 카라스코예요.\n시라카와는 정규시즌 18경기 4승 5패, 평균자책점 4.75였지만 LG전 두 경기에서는 1패, 평균자책점 7.71에 9와 3분의 1이닝 동안 홈런 4개를 맞았어요. 카라스코는 11경기 6승 3패, 평균자책점 4.05였고 KIA전 한 경기는 4와 3분의 1이닝 4실점이었지만 홈런은 맞지 않았어요. 와일드카드 결정전에서는 두산을 6이닝 1실점으로 막았어요.\n\n야구자판기의 예상은 3차전 LG예요. 3차전, LG가 잠실에서 반격할까요? KIA가 3연승으로 끝낼까요? 댓글로 알려 주세요.' + YT_TAIL,
    tags=['준플레이오프 3차전', '3차전 예측', '시라카와', '카라스코', 'KIA LG', 'KIA 타이거즈', 'LG 트윈스', '준플레이오프', '가을야구', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#준플레이오프', '#시라카와', '#카라스코', '#KIA타이거즈', '#LG트윈스', '#야구자판기'])))

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
    e = {
        'date': DATE, 'gameDate': '2026-10-18', 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': ep.get('ttsTempo', 1.25), 'ttsTempoSlow': ep.get('ttsTempoSlow', 1.2),
        'rev': f'1018-cut{n}-v1', 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': '2026-10-18_롱폼2', 'lines': vmap},
        'source': f'롱폼 {SRC} 에서 잘라 세로로 다시 짬(컷 {n}). ' + ep.get('source', ''),
        'lines': lines, 'scenes': scenes,
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
