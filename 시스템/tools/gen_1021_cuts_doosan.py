# 10/21 밤 롱폼 「두산 방출 11명」(episodes/2026-10-20_롱폼.json) → 컷 쇼츠 4편(컷6~9). 세로(1080x1920).
# 원본 줄은 롱폼 음성 재사용(voiceFrom). 10/21 밤 사용자(롱폼에서 쪼갠 건 롱폼으로 유도): 끝 질문 줄을 빼고 '전체는 하단 관련 영상' 새 줄(API) → 구독 멘트.
# 실행: python -X utf8 tools/gen_1021_cuts_doosan.py  → episodes/2026-10-21_롱폼컷6~9.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-20_롱폼.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
TH = '상황별/썸네일_롱폼21_두산방출'
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

POINT = lambda: NEW('두산 방출 열한 명 전체 이야기는 / 하단 관련 영상에 있어요', '두산 방출 11명 전체 이야기는|하단 관련 영상에 있어요',
                    {"type": "photo", "img": TH, "fit": "cover", "text": "", "relArrow": True, "chain": "relvid"})
CTA = lambda: OLD(55, {"type": "photo", "img": TH, "fit": "cover", "text": "", "chain": "relvid", "cont": True})
YT_TAIL = '\n두산 방출 11명 전체 이야기는 하단 관련 영상에 있어요.'
REC = '기록: KBO 기록실(10월 20일 조회). 기사: 머니투데이·마이데일리·뉴스핌·재경일보·스포츠월드·스포츠동아(10/19), SPOTV·스포탈코리아·OSEN(10/20), OSEN(4/15·5/21·5/22), 엑스포츠뉴스(4/14), 스포츠경향(4/14·5/3), 일간스포츠(10/15)'
CRED = '두산 베어스 제공, OSEN, 스포츠조선, 오마이뉴스, 스포티비뉴스, 마이데일리(한화 이글스 제공), MK스포츠, 구단 공식 프로필'
TB = dict(halo=18, cutout=True, cutoutCrop=0.6, cutoutLift=180, cutoutOverlap=330, cutoutFade=0.62, ph=1000, logos=False, noPills=True, top='', perLine=True)
def TH_(img, big, color, teams, **kw):
    t = dict(TB); t.update(img=img, big=big, color=color, teams=teams); t.update(kw); return t
TAGS0 = ['두산 방출', '재계약 불가', '두산 베어스', '프로야구 방출', '2026 방출', '프로야구', 'KBO', '야구자판기']
CUTS = []

# ── 6 손아섭 두산 6개월 ─────────────────────────────
CUTS.append(dict(topic='손아섭두산6개월방출', vtitle=['손아섭 방출', '두산 6개월 만'],
  lines=[OLD(0), OLD(1), OLD(2), OLD(21), OLD(22), OLD(23), OLD(24), OLD(25), OLD(26), OLD(30), OLD(32), POINT(), CTA()],
  thumb=TH_('누끼/경기_손아섭_결승타_0521_OSEN', '손아섭 방출\n두산 6개월 만', '#1E3A8A', ['두산']),
  yt=dict(title='손아섭 방출 | 두산 온 지 6개월, 2655안타 베테랑의 마지막 시즌 #손아섭 #두산베어스',
    desc='두산 베어스가 10월 19일 손아섭에게 재계약 불가를 통보했어요. 4월 14일 한화에서 트레이드로 데려온 지 6개월 만이에요.\n두산 데뷔전 SSG전에서 홈런을 치고 2타점을 올렸지만, 그 뒤 10경기 32타수 3안타에 그쳤고 두산에서만 3번 1군에서 말소됐어요. 올해 1군 성적은 54경기 타율 2할 3푼 6리, 홈런 1개예요. 방출된 선수는 바로 다른 구단과 계약할 수 있어요.' + YT_TAIL,
    tags=['손아섭', '손아섭 방출', '손아섭 두산'] + TAGS0,
    hashtags=['#Shorts', '#손아섭', '#두산베어스', '#방출', '#재계약불가', '#야구자판기'])))

# ── 7 손아섭 통산 2655안타 ──────────────────────────
CUTS.append(dict(topic='손아섭2655안타역대3위', vtitle=['손아섭 2655안타', '역대 3위'],
  lines=[OLD(0), OLD(1), OLD(28), OLD(14), OLD(15), OLD(16), OLD(17), OLD(29), OLD(30), POINT(), CTA()],
  thumb=TH_('카드/P21_손아섭_홈런_mid', '손아섭 2655안타\n역대 3위', '#B91C1C', ['두산'], cutoutCrop=0.85),
  yt=dict(title='손아섭 통산 2655안타 | 최다 안타 1위였던 타자가 방출되기까지 #손아섭 #방출',
    desc='손아섭의 통산 안타는 2655개, 최형우와 김현수에 이어 KBO 역대 3위예요. 3000안타까지는 345개가 남았어요.\n2007년 롯데에 입단해 2010년부터 주전으로 뛰었고, 최다안타 1위 4번, 골든글러브 6번, 2023년 NC에서 첫 타격왕에 올랐어요. 2024년 6월 20일 잠실 두산전에서 박용택을 넘어 통산 최다 안타 1위에 올랐지만, 2주 뒤 왼쪽 무릎 인대를 다쳤고 14년 연속 시즌 100안타 기록도 그해 끊겼어요. 손아섭은 지금 38살이고 10월 19일 두산에서 방출됐어요.' + YT_TAIL,
    tags=['손아섭', '손아섭 2655안타', '통산 최다안타', '3000안타'] + TAGS0,
    hashtags=['#Shorts', '#손아섭', '#2655안타', '#방출', '#야구자판기'])))

# ── 8 김명신 10년 원클럽맨 ──────────────────────────
CUTS.append(dict(topic='김명신10년원클럽방출', vtitle=['김명신 방출', '10년 원클럽맨'],
  lines=[OLD(0), OLD(1), OLD(33), OLD(34), OLD(35), OLD(36), OLD(37), OLD(38), OLD(39), OLD(40), POINT(), CTA()],
  thumb=TH_('카드/P21_김명신_역투', '김명신 방출\n10년 원클럽맨', '#0F766E', ['두산'], cutoutCrop=0.85),
  yt=dict(title='김명신 방출 | 두산에서만 10년, 297경기 45홀드 "야구선수 김명신은 조금 더" #김명신 #두산베어스',
    desc='두산 베어스 투수 김명신이 10월 19일 재계약 불가 통보를 받았어요. 2017년 2차 2라운드로 입단해 10년 동안 두산 한 팀에서만 뛰었어요.\n신인이던 2017년 4월 타구에 얼굴을 맞아 광대뼈 3곳이 부러졌지만 그해 39경기에 나섰고, 2023년엔 24홀드로 리그 홀드 3위에 올랐어요. 통산 성적은 297경기 15승 45홀드예요. 방출 뒤 SNS에는 "두산 베어스 김명신은 끝일지 몰라도 야구선수 김명신은 조금 더 이어가 볼 생각"이라고 남겼어요(SPOTV·스포탈코리아 10월 20일 보도).' + YT_TAIL,
    tags=['김명신', '김명신 방출', '원클럽맨'] + TAGS0,
    hashtags=['#Shorts', '#김명신', '#두산베어스', '#방출', '#야구자판기'])))

# ── 9 두산 단장 교체 ──────────────────────────────
CUTS.append(dict(topic='두산단장교체16년', vtitle=['두산 단장 교체', '16년 만에'],
  lines=[OLD(0), OLD(3), OLD(5), OLD(6), OLD(7), OLD(8), OLD(9), OLD(10), OLD(11), OLD(53), POINT(), CTA()],
  thumb=TH_('카드/P21_정재훈_단장', '두산 단장 교체\n16년 만에', '#7C3AED', ['두산'], cutoutCrop=0.85),
  yt=dict(title='두산 단장 교체 | 16년 김태룡 단장 물러나고 정재훈 새 단장, 같은 날 11명 방출 #두산베어스 #정재훈',
    desc='두산 베어스가 10월 19일 2011년부터 16년 동안 팀을 맡아 온 김태룡 단장을 구단 자문으로 옮기고, 정재훈 운영팀장을 새 단장에 앉혔어요. 같은 날 선수 11명에게 재계약 불가를 알렸어요.\n두산은 올해 정규시즌 5위로 마친 뒤 10월 14일 와일드카드 결정전에서 LG에 1대 4로 져 한 경기 만에 가을야구가 끝났어요. 김태룡 단장 시절 두산은 7년 연속 한국시리즈에 올랐고 3번 우승했어요. 새 단장 정재훈은 45살로, 2006년 두산에 선수로 입단했고 2011년부터 프런트에서 일했어요(마무리 투수로 뛴 정재훈과는 다른 사람이에요).' + YT_TAIL,
    tags=['두산 단장', '정재훈 단장', '김태룡 단장', '두산 단장 교체'] + TAGS0,
    hashtags=['#Shorts', '#두산베어스', '#정재훈', '#김태룡', '#야구자판기'])))
out = []
for n, c in enumerate(CUTS, 6):
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
        'date': DATE, 'gameDate': '2026-10-19', 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': ep.get('ttsTempo', 1.25), 'ttsTempoSlow': ep.get('ttsTempoSlow', 1.2),
        'rev': f'1021-cut{n}-doosan-v4', 'mascot': False, 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': '2026-10-20_롱폼', 'lines': vmap},
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
