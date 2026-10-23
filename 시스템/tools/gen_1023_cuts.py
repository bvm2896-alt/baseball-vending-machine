# 10/23 아침 사용자 "lg랑 kt 숏폼으로 쪼개자" → 롱폼㉖ LG(episodes/2026-10-23_롱폼.json) 4편 + 롱폼㉗ KT(2026-10-23_롱폼2.json) 3편
#   = 2026-10-23_롱폼컷1~7.json. 세로 1080x1920. 원본 줄은 롱폼 음성 재사용(voiceFrom),
#   끝은 질문 대신 '전체는 하단 관련 영상' 새 줄(API) → 구독 멘트(사용자 10/21 "롱폼에서 쪼갠 건 롱폼으로 유도").
#   컷 첫 줄은 지시어로 시작하지 않고(10/21), 줄마다 가리키는 앞 내용이 컷 안에 있다.
# 실행: python -X utf8 tools/gen_1023_cuts.py
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = '2026-10-23'
SRCS = {}
for key, f in (('L', '2026-10-23_롱폼'), ('K', '2026-10-23_롱폼2')):
    ep = json.load(io.open(os.path.join(HERE, 'episodes', f + '.json'), encoding='utf-8'))
    scn = {}
    for s in ep['scenes']: scn.setdefault(s['startLine'], s)
    d = ep['youtube']['description'].split('\n')
    SRCS[key] = dict(f=f, ep=ep, LN=ep['lines'], SCN=scn, rec=next(l for l in d if l.startswith('기록:')))
CUR = {}
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
    pcs = [wrap16(x) for x in sub.split('|')]
    assert len(pcs) == len(narr.split(' / ')), (narr, sub)
    d = {'narr': narr, 'sub': '|'.join(pcs)}
    if slow: d['pace'] = 'slow'
    return (None, d, scene)

def OLD(i, scene=None):
    d = copy.deepcopy(CUR['LN'][i])
    if (d.get('gapAfter') or 0) < 0.8: d.pop('gapAfter', None)   # 롱폼에서 글 읽을 시간으로 잡아 둔 0.8초 쉼(R13)은 컷에서도 남긴다
    sc = copy.deepcopy(scene if scene is not None else CUR['SCN'].get(i))
    return (i, d, sc)

META = {
  'L': dict(th='상황별/썸네일_롱폼26_LG방출', point=('엘지 방출 열한 명 전체 이야기는 / 하단 관련 영상에 있어요', 'LG 방출 11명 전체 이야기는|하단 관련 영상에 있어요'),
            cta=47, tail='\nLG 방출 11명 전체 이야기는 하단 관련 영상에 있어요.', game=DATE,
            cred='뉴스1, SPOTV, 스타뉴스, 구단 공식 프로필', tags=['LG 방출', '재계약 불가', 'LG 트윈스', '프로야구 방출', '2026 방출', '프로야구', 'KBO', '야구자판기']),
  'K': dict(th='상황별/썸네일_롱폼27_KT방출', point=('케이티 방출 열 명 전체 이야기는 / 하단 관련 영상에 있어요', 'KT 방출 10명 전체 이야기는|하단 관련 영상에 있어요'),
            cta=45, tail='\nKT 방출 10명 전체 이야기는 하단 관련 영상에 있어요.', game=DATE,
            cred='SPOTV, 스타뉴스, KT 위즈 제공, 구단 공식 프로필', tags=['KT 방출', '재계약 불가', 'KT 위즈', '프로야구 방출', '2026 방출', '프로야구', 'KBO', '야구자판기']),
}
def POINT(k):
    m = META[k]; return NEW(m['point'][0], m['point'][1], {"type": "photo", "img": m['th'], "fit": "cover", "text": "", "relArrow": True, "chain": "relvid"})
def CTA(k):
    m = META[k]; return OLD(m['cta'], {"type": "photo", "img": m['th'], "fit": "cover", "text": "", "chain": "relvid", "cont": True})
TB = dict(halo=18, cutout=True, cutoutCrop=0.6, cutoutLift=180, cutoutOverlap=330, cutoutFade=0.62, ph=1000, logos=False, noPills=True, top='', perLine=True)
def TH_(img, big, color, teams, **kw):
    t = dict(TB); t.update(img=img, big=big, color=color, teams=teams); t.update(kw); return t
CUTS = []
def CUT(k, idx, ov=None, **c):
    CUR.update(SRCS[k]); c['src'] = k
    c['lines'] = [OLD(i) for i in idx] + [POINT(k), CTA(k)]
    for src, d, sc in c['lines']:   # 컷에서만 바꿀 장면(롱폼 앞 장면에서 이어받던 글을 덜어 내기 등)
        if ov and src in ov and sc is not None: sc.update(ov[src])
    CUTS.append(c)

# ── 1 장시환 · 현대 유니콘스 마지막 선수 (LG) ─────────────
CUT('L', [0, 12, 2, 17, 18, 19, 20, 21, 22, 23, 25], topic='장시환현대유니콘스마지막선수은퇴', vtitle=['장시환 은퇴', '현대 유니콘스 마지막 선수'],
  thumb=TH_('카드/P26_장시환_LG불펜', '장시환 은퇴\n현대 마지막 선수', '#A50034', ['LG'], cutoutCrop=0.85),
  yt=dict(title='장시환 은퇴 | 현대 유니콘스 출신 마지막 현역, LG에서 1군 한 번 못 서고 떠났다 #장시환 #LG트윈스',
    desc='LG 트윈스가 10월 22일 선수 11명과 재계약하지 않기로 했어요. 이 가운데 장시환과 송대현은 은퇴를 결정했어요.\n장시환은 현대 유니콘스 출신 마지막 현역 선수였어요. 지난해 시즌이 끝난 뒤 한화에서 방출됐고, 그 무렵 정훈·황재균·오재일 등 현대 출신 선수들이 줄줄이 은퇴했어요. LG가 연봉 1억 원에 장시환을 데려왔고, 장시환은 1군에서 박수받으며 떠나고 싶다고 했어요. 올해 1월 신년인사회에선 현대의 마지막 유산이라는 말을 2~3년은 더 들어야 할 것 같다고 했지만, 올해 1군에도 2군 공식 경기에도 서지 못했어요. 장시환의 은퇴로 현대 유니콘스 출신 현역은 이제 한 명도 없어요.',
    tags=['장시환', '장시환 은퇴', '현대 유니콘스', '현대 유니콘스 마지막'], hashtags=['#Shorts', '#장시환', '#LG트윈스', '#현대유니콘스', '#야구자판기']))

# ── 2 장시환 · KBO 최다 19연패 투수의 20년 (LG) ─────────────
CUT('L', [0, 12, 13, 14, 15, 16, 24, 3],
  ov={3: dict(stats=[{"k": "2026년 1군", "v": "0경기", "at": 1.0, "hi": True}, {"k": "2026년 2군 공식 경기", "v": "0경기", "at": 1.4, "hi": True}])},   # 롱폼 1~2줄에서 이어받던 '명단 맨 앞·마지막 현역'은 이 컷에서 말하지 않는다
  topic='장시환19연패투수의20년', vtitle=['장시환 은퇴', '19연패 투수의 20년'],
  thumb=TH_('카드/P26_장시환_한화투구', '장시환 은퇴\n19연패 투수의 20년', '#1F2937', ['LG'], cutoutCrop=0.85),
  yt=dict(title='장시환 은퇴 | KBO 최다 19연패, 다섯 팀을 거친 20년 #장시환 #LG트윈스 #은퇴',
    desc='LG 트윈스가 10월 22일 선수 11명과 재계약하지 않기로 했고, 장시환은 은퇴를 결정했어요.\n장시환은 2007년 현대 유니콘스의 2차 1라운드 전체 2순위로 입단했어요(당시 이름 장효훈). 현대가 사라진 뒤엔 히어로즈·KT·롯데·한화를 거쳤고, 2015년 KT 마무리로 12세이브, 2022년 한화에서 14세이브를 기록했어요. 2020년부터 2023년까지 이어진 KBO 최다 19연패를 겪은 투수이기도 해요. 1군 통산 416경기 787이닝 29승 74패 34세이브 35홀드 평균자책점 5.31. 올해 LG에선 1군은 물론 2군 공식 경기에도 한 번도 나서지 못했어요.',
    tags=['장시환', '장시환 은퇴', '19연패', '장효훈'], hashtags=['#Shorts', '#장시환', '#LG트윈스', '#은퇴', '#야구자판기']))

# ── 3 진우영 · 미국 방출에서 LG까지 (LG) ─────────────
CUT('L', [0, 27, 28, 29, 30, 31], topic='진우영미국방출에서LG까지', vtitle=['진우영 방출', '미국·독립리그 거쳐 LG'],
  thumb=TH_('카드/P26_진우영_LG', '진우영 방출\n미국 방출 뒤 LG', '#A50034', ['LG'], cutoutCrop=0.85),
  yt=dict(title='진우영 방출 | 캔자스시티 방출 → 독립리그 → LG 드래프트, 그리고 다시 방출 #진우영 #LG트윈스',
    desc='LG 트윈스가 10월 22일 선수 11명과 재계약하지 않기로 했어요. 명단에는 투수 진우영도 있었어요.\n진우영은 글로벌선진학교를 졸업하고 미국 캔자스시티 로열스와 계약했지만 2021년 미국에서 방출됐어요. 군 복무를 마친 뒤 독립리그 파주 챌린저스에서 다시 공을 던졌고, 2024년 드래프트에서 LG가 4라운드 전체 38순위로 뽑았어요. 그해 1군에선 6경기 평균자책점 4.70을 기록했고, 그 뒤 2년 동안은 1군에 오르지 못했어요.',
    tags=['진우영', '진우영 방출', '캔자스시티', '파주 챌린저스'], hashtags=['#Shorts', '#진우영', '#LG트윈스', '#방출', '#야구자판기']))

# ── 4 LG 통합우승 1년 뒤 · 기아에 10연패 (LG) ─────────────
CUT('L', [0, 5, 6, 7, 8, 9, 10, 39, 40, 41, 42],
  ov={9: dict(text="10월 20일\n잠실야구장 마지막 경기", vsize=88, vh=460, focus="50% 92%")},   # 세로: 사진 위·글씨 아래(템플릿 10/23), 두 줄
  topic='LG통합우승1년뒤기아에10연패', vtitle=['LG 통합우승 1년 뒤', '기아에 10연패'],
  thumb=TH_('카드/P26_염경엽_준PO1', 'LG 우승 1년 뒤\n기아에 10연패', '#A50034', ['LG'], cutoutCrop=0.85),
  yt=dict(title='LG 통합우승 1년 뒤 | 준PO 3연패·기아전 10연패, 탈락 이틀 만에 11명 방출 #LG트윈스 #염경엽',
    desc='LG 트윈스가 준플레이오프에서 떨어진 지 이틀 만인 10월 22일 선수 11명과 재계약하지 않기로 했어요.\nLG는 지난해 정규시즌 1위와 한국시리즈 우승으로 통합우승을 했지만, 올해는 정규시즌 4위로 마쳤고 마무리 유영찬은 4월 말 팔꿈치를 다쳐 수술로 시즌을 접었어요. 와일드카드 결정전에선 두산을 4대 1로 이겼지만, 준플레이오프에서 기아에 1대 5, 3대 6, 1대 13으로 세 판을 내리 졌어요. 3차전은 44년 동안 쓴 잠실야구장의 마지막 경기였고, 정규시즌 막판 기아전 7연패까지 더하면 기아에만 10연패예요.\n염경엽 감독은 지난해 11월 3년 최대 30억 원에 재계약했고, 탈락 뒤 마무리 훈련부터 잘 준비하겠다고 했어요. 이번 겨울엔 홍창기가 FA 자격을 얻어요.',
    tags=['LG 트윈스', '염경엽', '준플레이오프', '기아전 10연패', '홍창기 FA'], hashtags=['#Shorts', '#LG트윈스', '#염경엽', '#야구자판기']))

# ── 5 최동환 · LG에 방출 요청 2년 뒤 (KT) ─────────────
CUT('K', [0, 1, 16, 17, 18, 19, 20, 21, 22, 23, 3], topic='최동환LG에방출요청2년만에또방출', vtitle=['최동환 방출', '방출 요청 2년 만에 또'],
  thumb=TH_('카드/P27_최동환_KT', '최동환 방출\n2년 만에 또', '#1F2937', ['KT'], cutoutCrop=0.85),
  yt=dict(title='최동환 방출 | LG에 직접 방출 요청하고 KT로, 2년 만에 또 방출 #최동환 #KT위즈 #LG트윈스',
    desc='정규시즌 1위 KT 위즈가 10월 22일 선수 10명에게 재계약 불가를 통보했어요. 명단에는 LG에서 16년을 보낸 투수 최동환이 있었어요.\n최동환은 2023년 45경기 평균자책점 3.19를 기록했고, 그해 LG가 29년 만에 통합우승을 할 때 데뷔 후 처음으로 한국시리즈 마운드에 섰어요. 하지만 2024년엔 1군 26경기 평균자책점 6.95에 그쳤고(2군 평균자책점 1.08), 시즌을 마친 뒤 현역을 이어 가려고 구단에 직접 방출을 요청했어요. 12월 2일 KT가 불펜 보강을 위해 데려왔지만 지난해 1군 20경기 평균자책점 8.68, 올해는 1군 등판 없이 2군 36경기 평균자책점 6.11. 2년 만에 다시 방출 명단에 올랐어요.',
    tags=['최동환', '최동환 방출', '방출 요청', 'LG 통합우승'], hashtags=['#Shorts', '#최동환', '#KT위즈', '#방출', '#야구자판기']))

# ── 6 조이현 · 세 구단, 두 번째 방출 (KT) ─────────────
CUT('K', [0, 27, 28, 29, 30, 31, 32, 33, 34], topic='조이현세구단두번째방출', vtitle=['조이현 방출', '세 구단, 두 번째 방출'],
  thumb=TH_('카드/P27_조이현_KT원정', '조이현 방출\n두 번째 방출', '#1F2937', ['KT'], cutoutCrop=0.85),
  yt=dict(title='조이현 방출 | 정우람 보상선수·입단 테스트·2군 2관왕, 그리고 두 번째 방출 #조이현 #KT위즈',
    desc='정규시즌 1위 KT 위즈가 10월 22일 선수 10명에게 재계약 불가를 통보했어요. 명단에는 투수 조이현도 있었어요.\n조이현은 제주고를 졸업하고 2014년 한화에 2차 5라운드 전체 47순위로 입단했고, 2015년 말 정우람의 FA 보상선수로 SK로 옮겼어요. 상무를 다녀온 뒤 팔꿈치 부상과 부진이 겹쳐 2022시즌을 마치고 SSG에서 방출됐고, KT 입단 테스트를 통과해 2023시즌부터 KT 유니폼을 입었어요. 지난해엔 2군 남부리그에서 10승 평균자책점 3.60으로 다승·평균자책점 2관왕에 올랐지만, 올해는 1군 등판 없이 2군 24경기 평균자책점 5.67에 머물렀어요. 1군 통산 116경기 10승 18패 평균자책점 6.29.',
    tags=['조이현', '조이현 방출', '정우람 보상선수', '입단 테스트'], hashtags=['#Shorts', '#조이현', '#KT위즈', '#방출', '#야구자판기']))

# ── 7 KT 정규 1위 · 사흘 뒤 10명 방출 (KT) ─────────────
CUT('K', [5, 6, 7, 8, 9, 10, 11, 12, 37, 38, 39], topic='KT정규1위이강철최고대우사흘뒤10명방출', vtitle=['KT 정규 1위', '사흘 뒤 10명 방출'],
  thumb=TH_('카드/FA9_이강철_덕아웃', 'KT 정규 1위\n사흘 뒤 10명 방출', '#1F2937', ['KT'], cutoutCrop=0.85),
  yt=dict(title='KT 정규 1위 | 이강철 역대 최고 대우 재계약, 사흘 뒤 10명 방출 #KT위즈 #이강철',
    desc='KT 위즈는 올해 정규시즌을 90승 5무 49패, 1위로 마쳤어요. 10월 5일 롯데를 이기며 2021년 이후 5년 만에 정규시즌 우승을 확정했고, 한국시리즈엔 바로 올라갔어요. 1차전은 11월 2일 수원에서 열리고, 상대는 삼성과 기아의 플레이오프 승자예요.\n10월 19일엔 이강철 감독과 3년 총액 34억 원에 재계약했어요. KBO 감독 역대 최고 대우예요. 그리고 사흘 뒤인 10월 22일 선수 10명과 재계약하지 않기로 했고, 같은 날 문상철도 은퇴를 발표해 KT를 떠나는 선수는 모두 11명이에요.\n이강철 감독은 재계약 때 아직 시즌이 끝나지 않았다며 더 높은 곳에서 올 시즌을 마무리할 수 있도록 노력하겠다고 했어요. KT가 마지막으로 한국시리즈에서 우승한 건 2021년, 첫 통합우승을 차지한 해예요.',
    tags=['KT 위즈', '이강철', '이강철 재계약', '한국시리즈', '정규시즌 우승'], hashtags=['#Shorts', '#KT위즈', '#이강철', '#야구자판기']))

out = []
for n, c in enumerate(CUTS, 1):
    m = META[c['src']]; sep = SRCS[c['src']]
    lines, scenes, vmap = [], [], []
    for j, (src, d, sc) in enumerate(c['lines']):
        lines.append(d); vmap.append(src)
        if sc is not None:
            sc = dict(sc); sc['startLine'] = j
            same = bool(scenes) and sc.get('chain') and scenes[-1].get('chain') == sc.get('chain')
            # 이어받기는 바로 앞 장면이 같은 묶음일 때만(앞 장면이 다른 종류면 이어받을 것이 없다)
            if sc.get('cont') and not same: sc.pop('cont')
            if same and not sc.get('cont'): sc['cont'] = True   # 같은 사진·같은 묶음이 이어지면 사진 고정, 글만 바뀜
            scenes.append(sc)
    assert scenes[0]['startLine'] == 0
    e = {
        'date': DATE, 'gameDate': m['game'], 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': sep['ep'].get('ttsTempo', 1.3), 'ttsTempoSlow': sep['ep'].get('ttsTempoSlow', 1.3),
        'rev': f'1023-cut{n}-v1', 'mascot': False, 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': sep['f'], 'lines': vmap},
        'source': f"롱폼 episodes/{sep['f']}.json 에서 잘라 세로로 다시 짬(컷 {n}). " + sep['ep'].get('source', ''),
        'lines': lines, 'scenes': scenes,
        'thumb': c['thumb'],
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'] + m['tail'] + f"\n\n{sep['rec']}\n사진: {m['cred']}", 'tags': c['yt']['tags'] + m['tags'], 'hashtags': c['yt']['hashtags']},
    }
    p = os.path.join(HERE, 'episodes', f"{DATE}_롱폼컷{n}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    est = sum(len(l['narr'].replace(' / ', ' ')) * 0.14 + 0.3 * 0.6 * l['narr'].count(' / ') + 0.45 * 0.6 for l in lines) + 1.0
    newc = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for s, l in zip(vmap, lines) if s is None)
    out.append((n, c['topic'], len(lines), len(scenes), round(est), newc, len(c['yt']['title'])))
    for b in (x for l in lines for x in l['narr'].split(' / ')):
        if len(re.sub(r'[\s,?+]', '', b)) > 22: print('호흡 초과', n, b)
for r in out: print(r)
print('새로 합성 합계(구독 멘트 빼고)', sum(r[5] for r in out), '자')
