# 10/25 05:46 사용자 "쇼츠로 쪼개줘" + "방출편을 너무 많이 만들었나봐 MLB편만해"(중복 콘텐츠 수익 감소 알림) →
#   롱폼㉙ 「다음 메이저리거 언제 가?」(episodes/2026-10-24_롱폼.json) 6편 = 2026-10-24_롱폼컷14~19.json
#   (같은 영상 폴더의 10/23 방출 컷 1~13과 번호가 겹치지 않게 14부터). gen_1024_cuts_kia.py 와 같은 틀. 세로 1080x1920. 원본 줄은 롱폼 음성 재사용(voiceFrom),
#   끝은 질문 대신 '전체는 하단 관련 영상' 새 줄(API) → 구독 멘트(사용자 10/21 "롱폼에서 쪼갠 건 롱폼으로 유도").
#   컷 첫 줄은 지시어로 시작하지 않고(10/21), 줄마다 가리키는 앞 내용이 컷 안에 있다.
# 실행: python -X utf8 tools/gen_1024_cuts_kia.py
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = '2026-10-24'
SRCS = {}
for key, f in (('A', '2026-10-24_롱폼'),):
    ep = json.load(io.open(os.path.join(HERE, 'episodes', f + '.json'), encoding='utf-8'))
    scn = {}
    for s in ep['scenes']: scn.setdefault(s['startLine'], s)
    d = ep['youtube']['description'].split('\n')
    SRCS[key] = dict(f=f, ep=ep, LN=ep['lines'], SCN=scn, rec=next(l for l in d if l.startswith('기록 출처:')))
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
  'A': dict(th='상황별/썸네일_롱폼29_MLB누가갈까', point=('엠엘비 누가 갈까, 전체 이야기는 / 하단 관련 영상에 있어요', 'MLB 누가 갈까 전체 이야기는|하단 관련 영상에 있어요'),
            cta=153, tail='\nMLB 누가 갈까 — 전체 이야기는 하단 관련 영상에 있어요.', game=DATE,
            cred='구단 제공(삼성·한화·두산·기아), 스포츠조선, 연합뉴스, 구단 공식 프로필', tags=['다음 메이저리거', '메이저리그 포스팅', '포스팅', '메이저리그', '프로야구', 'KBO', '야구자판기']),
}
def POINT(k):
    m = META[k]; return NEW(m['point'][0], m['point'][1], {"type": "photo", "img": m['th'], "fit": "cover", "text": "", "relArrow": True, "chain": "relvid"})
def CTA(k):
    m = META[k]; return OLD(m['cta'], {"type": "photo", "img": m['th'], "fit": "cover", "text": "", "chain": "relvid", "cont": True})
TB = dict(halo=18, cutout=True, cutoutCrop=0.6, cutoutLift=180, cutoutOverlap=330, cutoutFade=0.62, ph=1000, logos=False, noPills=True, top='', perLine=True)
def TH_(img, big, color, teams, **kw):
    t = dict(TB); t.update(img=img, big=big, color=color, teams=teams); t.update(kw); return t
CUTS = []
def CUT(k, idx, ov=None, **c):   # ov: 컷에서 빠진 앞 줄의 기록을 이어받던 장면 → 이 컷에서 말하는 것만 남김(대사↔화면 1:1)
    CUR.update(SRCS[k]); c['src'] = k
    c['lines'] = [OLD(i) for i in idx] + [POINT(k), CTA(k)]
    for src, d, sc in c['lines']:   # 컷에서만 바꿀 장면(롱폼 앞 장면에서 이어받던 글을 덜어 내기 등)
        if ov and src in ov and sc is not None: sc.update(ov[src])
    CUTS.append(c)



# ── 14 김도영 · 아시안게임 금메달인데 2029시즌 뒤 ─────────────
CUT('A', [88, 89, 90, 91, 92, 93, 94, 95, 96],
  topic='김도영메이저리그2029시즌뒤', vtitle=['김도영 메이저리그', '언제 갈 수 있나'],
  thumb=TH_('경기/김도영_45호_포효_1012_스포츠조선', '김도영 MLB\n2029시즌 뒤?', '#D6002A', ['KIA'], cutoutCrop=0.85),
  yt=dict(title='김도영 메이저리그 언제 가? | 아시안게임 금메달인데 포스팅은 2029시즌 뒤 #김도영 #기아타이거즈',
    desc='기아 김도영은 올해 45홈런으로 홈런왕에 올랐고, 135경기 타율 .308 118타점 120득점을 기록했어요. 9월 아시안게임 금메달로 병역 문제도 해결했어요.\n하지만 이번 금메달로 병역 혜택을 받았기 때문에 그 대회 국가대표 포인트(1포인트 = 1군 등록일수 하루)는 받지 못해요. 지난해 부상으로 1군 등록일수가 145일에 못 미쳐 포스팅 자격(7시즌)이 1년 밀렸고, 계산대로면 2029시즌 뒤예요. 2028시즌 뒤라는 보도도 있어 정확한 시점은 기사마다 갈려요. 김도영은 지난해 1월 메이저리그 진출이라는 최종 목표는 가지고 있지만 아직 한참 남은 꿈이라고 했어요.',
    tags=['김도영', '김도영 메이저리그', '김도영 포스팅', '국가대표 포인트'], hashtags=['#Shorts', '#김도영', '#기아타이거즈', '#메이저리그', '#야구자판기']))

# ── 15 원태인 · 이번 겨울 FA ─────────────
CUT('A', [27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 39, 41],
  topic='원태인이번겨울FA메이저리그', vtitle=['원태인 메이저리그', '이번 겨울 FA'],
  thumb=TH_('경기/원태인_투구_0828_삼성제공', '원태인 이번 겨울\nFA로 MLB?', '#1E5BB8', ['삼성'], cutoutCrop=0.85),
  yt=dict(title='원태인 메이저리그 도전? | 이번 겨울 생애 첫 FA, 삼성은 못 막는다 #원태인 #삼성라이온즈',
    desc='삼성 원태인은 2019년 삼성에서 데뷔해 2024년 28경기 15승 6패 평균자책점 3.66으로 곽빈과 공동 다승왕에 올랐어요. 고졸 선수는 8시즌을 채우면 FA가 되는데, 원태인은 2019년부터 올해까지 8시즌을 채워 올 시즌이 끝나면 생애 첫 FA가 돼요. FA라서 삼성의 허락 없이도 해외 구단과 협상할 수 있어요.\n원태인은 2024년 12월 포스팅은 신청할 생각이 없다며, 2년 동안 더 발전한다면 FA가 되는 해에 도전하고 싶다고 했어요. 그 FA가 바로 이번 겨울이에요. 다만 올해는 부상으로 WBC에 나가지 못했고 7승 9패 평균자책점 4.52에 그쳤고, 8월 보도 기준으로 메이저리그 에이전트도 아직 정하지 않았어요.',
    tags=['원태인', '원태인 메이저리그', '원태인 FA', '삼성 라이온즈'], hashtags=['#Shorts', '#원태인', '#삼성라이온즈', '#메이저리그', '#야구자판기']))

# ── 16 노시환 · 11년 307억 + 포스팅 조항 ─────────────
CUT('A', [43, 44, 45, 46, 47, 48, 49, 50, 53, 54],
  topic='노시환11년307억포스팅조항', vtitle=['노시환 메이저리그', '307억 + 포스팅 조항'],
  thumb=TH_('카드/P29c_노시환_경기', '노시환 307억\n+ 포스팅 조항', '#FF6600', ['한화'], cutoutCrop=0.85),
  yt=dict(title='노시환 메이저리그 도전? | 11년 307억 계약에 붙은 포스팅 조항 #노시환 #한화이글스',
    desc='한화 노시환은 2023년 31홈런 101타점으로 홈런왕과 타점왕을 함께 차지했어요. 올해 2월 23일 한화와 2027~2037시즌 11년, 옵션 포함 총액 307억 원에 계약했어요.\n이 계약에는 2026시즌이 끝나면 포스팅으로 메이저리그에 도전할 수 있다는 조항이 붙어 있어요. 해외는 메이저리그로만 정했고, 돌아올 때는 한화 선수로 남기로 합의했어요. 11년 계약이 시작되기 전, 바로 이번 겨울이 그 조항을 쓸 수 있는 때예요. 10월 14일 보도 기준으로 포스팅 신청 발표는 아직 없었어요.',
    tags=['노시환', '노시환 메이저리그', '노시환 포스팅', '한화 이글스'], hashtags=['#Shorts', '#노시환', '#한화이글스', '#메이저리그', '#야구자판기']))

# ── 17 곽빈·김주원 · 빠르면 1년 뒤 ─────────────
CUT('A', [2, 74, 75, 76, 77, 80, 81, 82, 83, 84, 86],
  ov={2: dict({k: v for k, v in SRCS['A']['SCN'][73].items() if k != 'startLine'}, profile=False)},
  topic='곽빈김주원빠르면1년뒤메이저리그', vtitle=['곽빈 · 김주원', '빠르면 1년 뒤 MLB'],
  thumb=TH_('경기/곽빈_포효0823_두산제공_상체', '곽빈·김주원\n빠르면 1년 뒤', '#131230', ['두산'], cutoutCrop=0.85),
  yt=dict(title='곽빈·김주원 메이저리그 언제 가? | 아시안게임 포인트로 빠르면 1년 뒤 #곽빈 #김주원',
    desc='두산 곽빈과 NC 김주원은 빠르면 1년 뒤 메이저리그에 도전할 수 있어요. 두 선수는 2023년 항저우 아시안게임 금메달로 이미 병역 혜택을 받아, 올해 아시안게임 금메달로는 국가대표 포인트 25포인트(1포인트 = 1군 등록일수 하루)를 그대로 받았어요. 김주원은 신인 때 모자랐던 등록일수를 이 포인트로 채웠어요. 두 선수 모두 2027시즌을 풀타임으로 마치면 포스팅 자격이 생긴다는 보도예요.\n8월 29일 잠실 곽빈과 안우진의 맞대결엔 다저스·양키스·샌디에이고·토론토·캔자스시티 5개 구단 스카우트가 찾아왔어요. 곽빈은 아시안게임 결승 뒤 야구를 시작할 때부터 미국 도전을 꿈꿨다고 했고, 김주원은 올해 1월 미국 무대에 도전할 만한 선수가 되는 게 첫 번째라고 했어요.',
    tags=['곽빈', '김주원', '곽빈 메이저리그', '김주원 메이저리그', '국가대표 포인트'], hashtags=['#Shorts', '#곽빈', '#김주원', '#메이저리그', '#야구자판기']))

# (10/25: 직장폐쇄·이적료 계산 그림은 가로 1640px 인포그래픽이라 세로 컷에서 글씨가 너무 작아짐 → 이번 세트에서 뺌. 이적료는 인물 카드로 된 순위 부분만)
# ── 18 역대 포스팅 이적료 순위 ─────────────
CUT('A', [119, 120, 122, 124, 126, 128],
  topic='역대포스팅이적료순위류현진이정후', vtitle=['역대 포스팅 이적료', '1위 류현진'],
  thumb=TH_('카드/P29c_류현진_다저스', '역대 포스팅 이적료\n1위 류현진', '#B07A00', ['한화'], cutoutCrop=0.85),
  yt=dict(title='역대 포스팅 이적료 순위 | 류현진 2573만, 이정후 1882만 5천, 박병호·김하성·강정호 #류현진 #이정후',
    desc='KBO 선수가 포스팅으로 메이저리그에 가면 원래 구단은 이적료를 받아요. 가장 큰 이적료는 2012년 한화가 류현진을 보내고 받은 2573만 달러 남짓이에요. 류현진은 그때 다저스와 6년 3600만 달러에 계약했어요. 두 번째는 2023년 키움이 이정후를 보내고 받은 1882만 5천 달러, 2015년 박병호는 1285만 달러, 2020년 김하성은 552만 5천 달러, 2014년 강정호는 500만 달러 남짓이었어요.',
    tags=['포스팅 이적료', '류현진', '이정후', '박병호', '김하성', '강정호'], hashtags=['#Shorts', '#류현진', '#이정후', '#포스팅', '#야구자판기']))

out = []
for n, c in enumerate(CUTS, 14):   # 같은 영상 폴더의 방출 컷 1~13 다음 번호
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
        'rev': f'1025-mlbcut{n}-v1', 'mascot': False, 'topic': c['topic'], 'vtitle': c['vtitle'],
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
