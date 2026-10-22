# 10/22 밤 사용자 "롯데 삼성 롱폼도 숏폼으로 쪼개줘" → 롱폼㉔ 롯데(episodes/2026-10-22_롱폼.json) 3편 + 롱폼㉕ 삼성(2026-10-22_롱폼2.json) 3편
#   = 2026-10-22_롱폼컷4~9.json (컷1~3 은 SSG, gen_1022_cuts_ssg.py). 세로 1080x1920. 원본 줄은 롱폼 음성 재사용(voiceFrom),
#   끝은 질문 대신 '전체는 하단 관련 영상' 새 줄(API) → 구독 멘트(사용자 10/21 "롱폼에서 쪼갠 건 롱폼으로 유도").
# 실행: python -X utf8 tools/gen_1022_cuts_ls.py
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = '2026-10-22'
SRCS = {}
for key, f in (('L', '2026-10-22_롱폼'), ('S', '2026-10-22_롱폼2')):
    ep = json.load(io.open(os.path.join(HERE, 'episodes', f + '.json'), encoding='utf-8'))
    scn = {}
    for s in ep['scenes']: scn.setdefault(s['startLine'], s)
    SRCS[key] = dict(f=f, ep=ep, LN=ep['lines'], SCN=scn)
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
    pcs = [wrap16(x + ('?' if re.search(r'(까요|나요)$', x) else '')) for x in sub.split('|')]
    assert len(pcs) == len(narr.split(' / ')), (narr, sub)
    d = {'narr': narr, 'sub': '|'.join(pcs)}
    if slow: d['pace'] = 'slow'
    return (None, d, scene)

def OLD(i, scene=None):
    d = copy.deepcopy(CUR['LN'][i]); d.pop('gapAfter', None)
    sc = copy.deepcopy(scene if scene is not None else CUR['SCN'].get(i))
    return (i, d, sc)

def ppx(i, **kw):
    s = copy.deepcopy(CUR['SCN'][i]); [s.pop(k, None) for k in ('chain', 'cont')]; s.update(kw); return s

def Qs(narr, sub, text, faces=None, logos=None):
    sc = {"type": "question", "text": text}
    if faces: sc["faces"] = ['카드/' + x for x in faces]
    if logos: sc["logos"] = logos
    return NEW(narr, sub, sc, slow=True)


META = {
  'L': dict(th='상황별/썸네일_롱폼24_롯데방출', point=('롯데 방출 열여섯 명 전체 이야기는 / 하단 관련 영상에 있어요', '롯데 방출 16명 전체 이야기는|하단 관련 영상에 있어요'),
            cta=48, tail='\n롯데 방출 16명 전체 이야기는 하단 관련 영상에 있어요.', game='2026-10-07',
            rec='기록: KBO 기록실·선수 조회(10월 22일 조회). 기사: SPOTV·재경일보·연합뉴스·OSEN(머니투데이)·마이데일리·스포츠경향·스포츠월드·톱스타뉴스·FT스포츠(10/7), 매일신문(2025/11/19), OSEN(2025/11/20·2026/2/3), 헤럴드경제(4/12), YTN(4/13), 재경일보(10/17), 머니투데이·SPOTV(10/20~21), 마이데일리(10/21), 파이낸셜뉴스·부산일보(10/12~13), 엑스포츠뉴스·일간스포츠(10/19)',
            cred='OSEN, SPOTV(롯데 자이언츠 제공), 구단 공식 프로필', tags=['롯데 방출', '재계약 불가', '롯데 자이언츠', '프로야구 방출', '2026 방출', '프로야구', 'KBO', '야구자판기']),
  'S': dict(th='상황별/썸네일_롱폼25_삼성방출', point=('삼성 방출 열 명 전체 이야기는 / 하단 관련 영상에 있어요', '삼성 방출 10명 전체 이야기는|하단 관련 영상에 있어요'),
            cta=46, tail='\n삼성 방출 10명 전체 이야기는 하단 관련 영상에 있어요.', game='2026-10-19',
            rec='기록: KBO 기록실(10월 22일 조회). 기사: 뉴스핌·스타뉴스·SBS·스포츠경향·이데일리·재경일보·SPOTV·OSEN·이투데이(10/19), 노컷뉴스(2022/7/25), 강원일보·SPOTV(2015/11/27), 매일신문(2023/11/22), OSEN(2024/6/28), 시대일보(2024/10/10), 뉴스핌·서울신문·위키트리(10/21), 일간스포츠(10/13), 경북매일·SBS(2025/11/3), 세계일보(9/7)·영남일보(1/26)·대구신문(10/7)',
            cred='OSEN, SPOTV, 삼성 라이온즈 제공, 구단 공식 프로필', tags=['삼성 방출', '재계약 불가', '삼성 라이온즈', '프로야구 방출', '2026 방출', '프로야구', 'KBO', '야구자판기']),
}
def POINT(k):
    m = META[k]; return NEW(m['point'][0], m['point'][1], {"type": "photo", "img": m['th'], "fit": "cover", "text": "", "relArrow": True, "chain": "relvid"})
def CTA(k):
    m = META[k]; return OLD(m['cta'], {"type": "photo", "img": m['th'], "fit": "cover", "text": "", "chain": "relvid", "cont": True})
TB = dict(halo=18, cutout=True, cutoutCrop=0.6, cutoutLift=180, cutoutOverlap=330, cutoutFade=0.62, ph=1000, logos=False, noPills=True, top='', perLine=True)
def TH_(img, big, color, teams, **kw):
    t = dict(TB); t.update(img=img, big=big, color=color, teams=teams); t.update(kw); return t
CUTS = []
def CUT(k, idx, **c):
    CUR.update(SRCS[k]); c['src'] = k
    c['lines'] = [OLD(i) for i in idx] + [POINT(k), CTA(k)]
    CUTS.append(c)

# ── 4 최충연 2억 원의 1이닝 (롯데) ─────────────────
CUT('L', [0, 1, 2, 3, 18, 20, 21, 22, 23, 24], topic='최충연2억1이닝방출', vtitle=['최충연 방출', '2억 주고 1이닝'],
  thumb=TH_('카드/P24_최충연_롯데', '최충연 방출\n2억 주고 1이닝', '#041E42', ['롯데'], cutoutCrop=0.85),
  yt=dict(title='최충연 방출 | 롯데가 2억 주고 데려왔는데 1군 1경기 1이닝 #최충연 #롯데자이언츠',
    desc='롯데 자이언츠가 10월 7일 선수 16명에게 재계약 불가를 통보했어요. 명단에는 2018년 아시안게임 금메달리스트 최충연도 있었어요.\n롯데는 지난해 11월 2차 드래프트 3라운드에서 최충연을 뽑으며 삼성에 양도금 2억 원을 냈어요. 올해 첫 1군 등판인 4월 7일 KT전에서 1이닝 3피안타 2실점을 했고, 며칠 뒤 팬에게 한 외모 비하 발언이 영상으로 퍼져 사과한 뒤 2군으로 내려갔어요. 2군에선 5경기 평균자책점 1.29를 기록했지만 4월 13일 이후로는 다시 마운드에 서지 못했어요.',
    tags=['최충연', '최충연 방출', '2차 드래프트', '양도금 2억'], hashtags=['#Shorts', '#최충연', '#롯데자이언츠', '#방출', '#야구자판기']))

# ── 5 최충연 금메달에서 방출까지 (롯데) ──────────────
CUT('L', [0, 11, 12, 13, 14, 15, 16, 17, 25], topic='최충연금메달에서방출까지', vtitle=['최충연', '금메달에서 방출까지'],
  thumb=TH_('카드/P24_최충연_대표팀', '최충연\n금메달에서 방출까지', '#1D4ED8', ['롯데'], cutoutCrop=0.85),
  yt=dict(title='최충연 | 2018 홀드·세이브 필승조, 아시안게임 금메달에서 방출까지 #최충연 #방출',
    desc='최충연은 경북고를 졸업하고 2016년 삼성의 1차 지명을 받았어요. 2018년엔 70경기 85이닝 16홀드 8세이브 평균자책점 3.60을 기록했고, 그해 아시안게임 대표팀에 뽑혀 금메달을 땄어요.\n하지만 2020년 1월 음주운전으로 150경기 출장정지 징계를 받았고, 그해 11월 오른쪽 팔꿈치 인대 접합 수술을 받아 2021년을 통째로 쉬었어요. 지난해 삼성에선 1군 4경기 평균자책점 37.80에 그쳤고, 1군 통산 성적은 199경기 5승 19패 9세이브 23홀드 평균자책점 6.14예요. 10월 7일 롯데에서 재계약 불가 통보를 받았어요.',
    tags=['최충연', '최충연 방출', '아시안게임 금메달', '최충연 삼성'], hashtags=['#Shorts', '#최충연', '#롯데자이언츠', '#방출', '#야구자판기']))

# ── 6 롯데 감독 미정 · 3년 연속 7위 (롯데) ────────────
CUT('L', [5, 6, 36, 37, 38, 39, 40, 41], topic='롯데감독미정3년연속7위', vtitle=['롯데 감독 미정', '3년 연속 7위'],
  thumb=TH_('KBO프로필/김태형_감독', '롯데 감독 미정\n3년 연속 7위', '#041E42', ['롯데'], cutoutCrop=0.85),
  yt=dict(title='롯데 감독 미정 | 김태형 3년 계약 끝, 3년 모두 7위·외부 FA 0명 #롯데자이언츠 #김태형',
    desc='롯데 자이언츠는 올해 64승 3무 77패로 7위에 그쳤어요. 2023년부터 4년 연속 7위, 가을야구는 9년 연속 실패로 구단 역사상 가장 긴 기록이에요.\n김태형 감독의 3년 계약이 올해로 끝났고, 3년 동안 순위는 모두 7위, 밖에서 데려온 FA는 한 명도 없었어요. 롯데는 감독 선임 절차를 진행 중이라고 했고 10월 22일까지 결과는 발표되지 않았어요. 김태형 감독 재신임과 함께 이동욱 전 NC 감독, 조성환 해설위원 등이 거론되고 있어요. 박준혁 단장도 11월에 3년 계약이 끝나고, 롯데는 11월 4일 일본 미야자키로 마무리 캠프를 떠나요.',
    tags=['롯데 감독', '김태형 감독', '롯데 감독 선임', '롯데 7위'], hashtags=['#Shorts', '#롯데자이언츠', '#김태형', '#야구자판기']))

# ── 7 허윤동 13연패를 끊은 1라운더 (삼성) ─────────────
CUT('S', [0, 2, 3, 15, 16, 17, 19, 20, 21, 22, 23], topic='허윤동13연패끊은1라운더방출', vtitle=['허윤동 방출', '13연패 끊은 1라운더'],
  thumb=TH_('누끼/경기_허윤동_SPOTV', '허윤동 방출\n13연패 끊은 1라운더', '#074CA1', ['삼성']),
  yt=dict(title='허윤동 방출 | 구단 최다 13연패를 끊은 1라운더, 3년째 1군 기록 없이 #허윤동 #삼성라이온즈',
    desc='삼성 라이온즈가 10월 19일 선수 10명에게 재계약 불가를 통보했어요. 명단에는 2020년 1라운드 전체 5순위 왼손 투수 허윤동도 있었어요.\n허윤동은 2022년 7월 24일 고척 키움전에 선발로 나와 6이닝 2피안타 7탈삼진 무실점으로 막았고, 삼성은 8대 0으로 이겨 구단 역사상 가장 긴 13연패를 끊었어요. 하지만 2023년 7경기를 끝으로 1군 기록이 없고, 2024년 상무에 입대했다가 지난해 돌아왔지만 올해도 1군에 오르지 못했어요. 올해 2군 33경기 6승 1패 3홀드 평균자책점 5.05, 1군 통산 31경기 6승 6패 평균자책점 6.38이에요.',
    tags=['허윤동', '허윤동 방출', '삼성 13연패', '1라운더'], hashtags=['#Shorts', '#허윤동', '#삼성라이온즈', '#방출', '#야구자판기']))

# ── 8 홍현빈 오승환 초구 끝내기, 그 삼성에서 방출 (삼성) ──
CUT('S', [0, 32, 33, 34, 35], topic='홍현빈오승환끝내기그삼성에서방출', vtitle=['홍현빈 방출', '오승환 울린 끝내기'],
  thumb=TH_('카드/P25_홍현빈_KT끝내기', '홍현빈 방출\n오승환 울린 끝내기', '#074CA1', ['삼성'], cutoutCrop=0.85),
  yt=dict(title='홍현빈 방출 | 오승환 초구 끝내기 역전 3루타, 그 삼성에 와서 2년 만에 방출 #홍현빈 #삼성라이온즈',
    desc='홍현빈은 2017년 KT에 입단한 외야수예요. 2024년 6월 28일 KT 유니폼을 입고 삼성 마무리 오승환의 초구를 쳐 끝내기 역전 3루타를 날렸어요.\n그런데 그해 10월 KT에서 방출됐고, 시즌이 끝난 뒤 바로 그 삼성에 입단했어요. 1군 통산 성적은 281경기 타율 1할 9푼 2리, 그리고 10월 19일 삼성에서도 2년 만에 방출됐어요.',
    tags=['홍현빈', '홍현빈 방출', '오승환', '끝내기 3루타'], hashtags=['#Shorts', '#홍현빈', '#삼성라이온즈', '#오승환', '#야구자판기']))

# ── 9 삼성의 겨울 · 구자욱 원태인 FA (삼성) ────────────
CUT('S', [0, 1, 9, 37, 38, 39, 40, 41], topic='삼성의겨울구자욱원태인FA', vtitle=['삼성의 겨울', '구자욱·원태인 FA'],
  thumb=TH_('누끼/경기_구자욱_세리머니_0827_삼성제공', '삼성의 겨울\n구자욱·원태인 FA', '#074CA1', ['삼성'], cutoutCrop=0.75),
  yt=dict(title='삼성의 겨울 | PO 엿새 앞두고 10명 방출, 시즌 뒤엔 구자욱·원태인 FA #삼성라이온즈 #구자욱 #원태인',
    desc='삼성 라이온즈는 플레이오프를 엿새 앞둔 10월 19일 선수 10명에게 재계약 불가를 통보했어요. 플레이오프 1차전은 10월 25일 대구에서 열려요.\n삼성의 겨울은 플레이오프가 끝난 뒤 본격적으로 시작돼요. 박진만 감독은 지난해 11월 최대 23억 원에 재계약했고 올해가 새 계약의 첫해였어요. 구자욱은 5년 120억 원 비FA 다년계약이 올해로 끝나 생애 첫 FA가 되고, 원태인도 이번 시즌 뒤 FA 자격을 얻어요. 원태인은 올해 연봉 10억 원을 받았고 7승 9패 평균자책점 4.52를 기록했어요.',
    tags=['삼성 FA', '구자욱 FA', '원태인 FA', '박진만 감독'], hashtags=['#Shorts', '#삼성라이온즈', '#구자욱', '#원태인', '#야구자판기']))

out = []
for n, c in enumerate(CUTS, 4):
    m = META[c['src']]; sep = SRCS[c['src']]
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
        'date': DATE, 'gameDate': m['game'], 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': sep['ep'].get('ttsTempo', 1.3), 'ttsTempoSlow': sep['ep'].get('ttsTempoSlow', 1.3),
        'rev': f'1022-cut{n}-ls-v1', 'mascot': False, 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'voiceFrom': {'ep': sep['f'], 'lines': vmap},
        'source': f"롱폼 episodes/{sep['f']}.json 에서 잘라 세로로 다시 짬(컷 {n}). " + sep['ep'].get('source', ''),
        'lines': lines, 'scenes': scenes,
        'thumb': c['thumb'],
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'] + m['tail'] + f"\n\n{m['rec']}\n사진: {m['cred']}", 'tags': c['yt']['tags'] + m['tags'], 'hashtags': c['yt']['hashtags']},
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
