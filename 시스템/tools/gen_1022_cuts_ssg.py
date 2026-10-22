# 10/22 밤 롱폼㉓ 「SSG 방출 8명」(episodes/2026-10-21_롱폼.json) → 컷 쇼츠 3편(2026-10-22_롱폼컷1~3). 세로(1080x1920). gen_1021_cuts_doosan.py 와 같은 틀.
# 원본 줄은 롱폼 음성 재사용(voiceFrom). 10/21 밤 사용자(롱폼에서 쪼갠 건 롱폼으로 유도): 끝 질문 줄을 빼고 '전체는 하단 관련 영상' 새 줄(API) → 구독 멘트.
# 실행: python -X utf8 tools/gen_1022_cuts_ssg.py  → episodes/2026-10-22_롱폼컷1~3.json
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'episodes/2026-10-21_롱폼.json'
ep = json.load(io.open(os.path.join(HERE, SRC), encoding='utf-8'))
LN, SCN = ep['lines'], {}
for s in ep['scenes']: SCN.setdefault(s['startLine'], s)
TH = '상황별/썸네일_롱폼23_SSG방출'
DATE = '2026-10-22'

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

POINT = lambda: NEW('에스에스지 방출 여덟 명 전체 이야기는 / 하단 관련 영상에 있어요', 'SSG 방출 8명 전체 이야기는|하단 관련 영상에 있어요',
                    {"type": "photo", "img": TH, "fit": "cover", "text": "", "relArrow": True, "chain": "relvid"})
CTA = lambda: OLD(42, {"type": "photo", "img": TH, "fit": "cover", "text": "", "chain": "relvid", "cont": True})
YT_TAIL = '\nSSG 방출 8명 전체 이야기는 하단 관련 영상에 있어요.'
REC = '기록: KBO 기록실(10월 21일 조회). 기사: 스포츠경향·파이낸셜뉴스(뉴시스)·일간스포츠·스포츠월드·MK스포츠·미디어펜·머니투데이·OSEN(10/10), 일간스포츠·MHN(10/12), 일간스포츠·경인일보(10/11~12), OSEN·이투데이(10/15), 스포츠경향·머니투데이(10/16), 아이뉴스24(2021/12/14), OSEN·노컷뉴스(2022/11/5), 스포티비뉴스(4/13)'
CRED = 'OSEN, 연합뉴스, 스포츠동아, 스포츠서울, SSG 랜더스 제공, 구단 공식 프로필'
TB = dict(halo=18, cutout=True, cutoutCrop=0.6, cutoutLift=180, cutoutOverlap=330, cutoutFade=0.62, ph=1000, logos=False, noPills=True, top='', perLine=True)
def TH_(img, big, color, teams, **kw):
    t = dict(TB); t.update(img=img, big=big, color=color, teams=teams); t.update(kw); return t
TAGS0 = ['SSG 방출', '재계약 불가', 'SSG 랜더스', '프로야구 방출', '2026 방출', '프로야구', 'KBO', '야구자판기']
CUTS = []

# ── 1 박종훈 65억 마지막 해 ─────────────────────────
CUTS.append(dict(topic='박종훈65억마지막해방출', vtitle=['박종훈 방출', '65억 마지막 해'],
  lines=[OLD(0), OLD(1), OLD(2), OLD(3), OLD(15), OLD(16), OLD(22), OLD(23), OLD(24), POINT(), CTA()],
  thumb=TH_('누끼/경기_박종훈_포효_0628_OSEN', '박종훈 방출\n65억 마지막 해', '#CE0E2D', ['SSG']),
  yt=dict(title='박종훈 방출 | 5년 65억 국내 첫 비FA 다년계약, 마지막 해 1군 0경기 #박종훈 #SSG랜더스',
    desc='SSG 랜더스가 10월 10일 박종훈과 합의해 계약을 해지했어요. 같은 날 선수 8명에게 재계약 불가를 알렸어요.\n박종훈은 2021년 6월 팔꿈치 인대 접합 수술을 받았고, SSG는 그해 12월 수술을 받은 박종훈과 5년 65억 원에 계약했어요. 국내 첫 비FA 다년계약이었어요. 계약 마지막 해인 올해는 1군에서 한 번도 던지지 못했고, 2군에선 21경기 평균자책점 3.51을 기록했어요. 구단은 두 번의 우승에 기여한 공로를 평가해 새 팀을 빨리 찾을 수 있게 일찍 결정했다고 설명했어요.' + YT_TAIL,
    tags=['박종훈', '박종훈 방출', '비FA 다년계약', '65억'] + TAGS0,
    hashtags=['#Shorts', '#박종훈', '#SSG랜더스', '#방출', '#야구자판기'])))

# ── 2 박종훈 72승 잠수함 ─────────────────────────────
CUTS.append(dict(topic='박종훈72승우승두번잠수함', vtitle=['박종훈 72승', '우승 두 번의 잠수함'],
  lines=[OLD(0), OLD(9), OLD(10), OLD(11), OLD(12), OLD(13), OLD(14), OLD(18), OLD(25), OLD(26), POINT(), CTA()],
  thumb=TH_('카드/P23_박종훈_KS2022', '박종훈 72승\n우승 두 번', '#B91C1C', ['SSG'], cutoutCrop=0.85),
  yt=dict(title='박종훈 통산 72승 | 땅에 닿을 듯 던지는 잠수함, 우승 두 번 함께하고 SSG 떠난다 #박종훈 #방출',
    desc='SSG 랜더스가 10월 10일 재계약 불가를 알린 8명 가운데 가장 눈에 띄는 이름은 잠수함 투수 박종훈이에요.\n2010년 2라운드로 SK에 입단해 2017년 12승, 2018년 14승, 2020년 13승으로 두 자릿수 승리를 세 번 거뒀어요. 2018년 SK 한국시리즈 우승, 아시안게임 금메달을 함께했고, 2022년 한국시리즈 3차전 8회 무사 2루에 올라와 1이닝을 무실점으로 막으며 통합 우승에 힘을 보탰어요. 통산 성적은 245경기 72승 79패 평균자책점 4.85. 박종훈은 지금 35살이고 현역을 이어 가겠다고 했어요.' + YT_TAIL,
    tags=['박종훈', '박종훈 방출', '잠수함 투수', '박종훈 72승'] + TAGS0,
    hashtags=['#Shorts', '#박종훈', '#SSG랜더스', '#잠수함', '#야구자판기'])))

# ── 3 SSG 후반기 2위, 아빌라는 잡고 8명 방출 ─────────────
CUTS.append(dict(topic='SSG후반기2위겨울', vtitle=['SSG 8명 방출', '아빌라는 잡았다'],
  lines=[OLD(5), OLD(6), OLD(7), OLD(8), OLD(29), OLD(36), OLD(37), POINT(), CTA()],
  thumb=TH_('누끼/경기_아빌라_박수_0929_SSG제공', 'SSG 8명 방출\n아빌라는 잡았다', '#CE0E2D', ['SSG'], cutoutCrop=0.75),
  yt=dict(title='SSG 8명 방출 | 후반기 2위 성적에도 6위, 아빌라는 최대 2년 재계약 #SSG랜더스 #아빌라',
    desc='SSG 랜더스는 올해 정규시즌을 65승 5무 74패, 6위로 마쳤어요. 전반기 9위였지만 후반기엔 34승 2무 22패로 10개 구단 중 두 번째 성적을 냈어요. 그래도 가을야구에는 닿지 못했고, 10월 10일 투수 6명·야수 2명에게 재계약 불가를 알렸어요.\n10월 15일엔 박정권 2군 감독과 계약을 끝냈고, 10월 16일엔 외국인 투수 아빌라(올해 14경기 9승 2패 평균자책점 1.44)와 최대 2년 재계약에 합의했어요.' + YT_TAIL,
    tags=['SSG 랜더스', '아빌라', '아빌라 재계약', 'SSG 후반기'] + TAGS0,
    hashtags=['#Shorts', '#SSG랜더스', '#아빌라', '#방출', '#야구자판기'])))

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
        'date': DATE, 'gameDate': '2026-10-10', 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': ep.get('ttsTempo', 1.25), 'ttsTempoSlow': ep.get('ttsTempoSlow', 1.2),
        'rev': f'1022-cut{n}-ssg-v1', 'mascot': False, 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': '2026-10-21_롱폼', 'lines': vmap},
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
