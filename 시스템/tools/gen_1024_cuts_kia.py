# 10/24 0시 사용자 "숏폼으로 쪼개줘 이제" → 롱폼㉘ 기아 방출(episodes/2026-10-23_롱폼3.json) 6편
#   = 2026-10-23_롱폼컷8~13.json (컷1~7은 LG·KT). gen_1023_cuts.py 와 같은 틀. 세로 1080x1920. 원본 줄은 롱폼 음성 재사용(voiceFrom),
#   끝은 질문 대신 '전체는 하단 관련 영상' 새 줄(API) → 구독 멘트(사용자 10/21 "롱폼에서 쪼갠 건 롱폼으로 유도").
#   컷 첫 줄은 지시어로 시작하지 않고(10/21), 줄마다 가리키는 앞 내용이 컷 안에 있다.
# 실행: python -X utf8 tools/gen_1024_cuts_kia.py
import json, io, os, copy, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = '2026-10-23'
SRCS = {}
for key, f in (('A', '2026-10-23_롱폼3'),):
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
  'A': dict(th='상황별/썸네일_롱폼28_기아방출', point=('기아 방출 여섯 명 전체 이야기는 / 하단 관련 영상에 있어요', 'KIA 방출 6명 전체 이야기는|하단 관련 영상에 있어요'),
            cta=120, tail='\nKIA 방출 6명 전체 이야기는 하단 관련 영상에 있어요.', game=DATE,
            cred='SPOTV(KIA 타이거즈 제공), 엑스포츠뉴스, 구단 공식 프로필', tags=['기아 방출', 'KIA 방출', '재계약 불가', '기아 타이거즈', '프로야구 방출', '2026 방출', '프로야구', 'KBO', '야구자판기']),
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


# ── 8 홍건희 · 2년 15억 포기, 1년 만에 방출 ─────────────
CUT('A', [0, 2, 3, 30, 34, 36, 38, 39, 40, 41, 42, 51, 54],
  ov={30: dict(sub='2024년 1월 · 두산 첫 FA', stats=[{"k": "첫 2년", "v": "9억 5천만 원", "at": 0.2}, {"k": "뒤 2년 · 홍건희 선택", "v": "15억 원", "at": 1.2, "hi": True}]),
      34: dict(sub='2025년', stats=[{"k": "2025년 · 팔꿈치 부상", "v": "20경기", "at": 0.4}, {"k": "평균자책점", "v": "6.19", "at": 1.4, "hi": True}])},
  topic='홍건희2년15억포기1년만에방출', vtitle=['홍건희 방출', '15억 포기, 1년 만에'],
  thumb=TH_('카드/P28_홍건희_KIA투구', '홍건희 방출\n15억 포기 1년 만에', '#D6002A', ['KIA'], cutoutCrop=0.85),
  yt=dict(title='홍건희 방출 | 두산 2년 15억 포기하고 친정 KIA로, 1년 만에 방출 #홍건희 #기아타이거즈',
    desc='기아 타이거즈가 플레이오프 1차전을 이틀 앞둔 10월 23일 선수 6명과 재계약하지 않기로 했어요. 명단에는 올해 1월 6년 만에 친정으로 돌아온 투수 홍건희가 있었어요.\n홍건희는 2024년 1월 두산과 2+2년 최대 24억 5천만 원에 첫 FA 계약을 맺었어요. 첫 2년은 9억 5천만 원, 뒤 2년 15억 원은 홍건희가 고를 수 있는 옵션이었어요. 지난해 팔꿈치 부상으로 20경기 평균자책점 6.19에 그친 뒤 남은 2년 15억 원을 포기하고 FA 시장에 나왔어요(옵트아웃). 홍건희는 돈 욕심보다 계약 기간을 더 길게 하고 싶었다고 했지만, 다른 구단의 관심은 크지 않았고 계약하지 못한 채 해를 넘겼어요. 올해 1월 21일 친정 기아와 1년 연봉 6억 5천만 원, 인센티브 포함 최대 7억 원에 계약했지만, 1군 4경기 4이닝 1홀드 평균자책점 4.50에 그쳤어요.',
    tags=['홍건희', '홍건희 방출', '홍건희 옵트아웃', '옵트아웃'], hashtags=['#Shorts', '#홍건희', '#기아타이거즈', '#방출', '#야구자판기']))

# ── 9 홍건희 · 기아 → 두산 마무리 → 다시 기아 ─────────────
CUT('A', [0, 2, 18, 19, 20, 21, 23, 24, 26, 53, 54],
  ov={26: dict(stats=[{"k": "세이브", "v": "44", "at": 0.6, "hi": True}, {"k": "홀드", "v": "39", "at": 0.8, "hi": True}])},   # 다음 줄(경기·승패·평균자책점)은 이 컷에 없다 → 빈 자리 표시 칸 빼기
  topic='홍건희류지혁트레이드두산마무리', vtitle=['홍건희 방출', '두산 마무리, 다시 기아'],
  thumb=TH_('카드/P28_홍건희_두산', '홍건희 방출\n두산 44세이브 투수', '#131230', ['KIA'], cutoutCrop=0.85),
  yt=dict(title='홍건희 방출 | 류지혁 트레이드로 두산 마무리, 친정 KIA 돌아와 1년 만에 이별 #홍건희 #기아타이거즈 #두산베어스',
    desc='기아 타이거즈가 10월 23일 선수 6명과 재계약하지 않기로 했어요. 명단에는 올해 1월 6년 만에 친정으로 돌아온 투수 홍건희가 있었어요.\n홍건희는 화순고를 졸업하고 2011년 기아에 2라운드 전체 9순위로 입단했지만, 첫 기아 시절 166경기 평균자책점 6.30에 머물렀어요. 2020년 6월 7일 내야수 류지혁과의 1대1 트레이드로 두산에 간 뒤 달라졌어요. 2021년 65경기 17홀드 평균자책점 2.78로 커리어 하이를 찍었고, 2022년 시즌 중 마무리를 맡아 18세이브, 2023년 22세이브를 올렸어요. 두산 첫 네 시즌 44세이브 39홀드. 1군 통산 492경기 27승 48패 58세이브 56홀드 평균자책점 4.92.',
    tags=['홍건희', '홍건희 방출', '류지혁 트레이드', '두산 마무리'], hashtags=['#Shorts', '#홍건희', '#기아타이거즈', '#두산베어스', '#야구자판기']))

# ── 10 고종욱 · 통산 타율 3할 ─────────────
CUT('A', [0, 15, 56, 57, 59, 60, 62, 63, 64, 66, 69, 70, 72],
  ov={64: dict(stats=[{"k": "역할", "v": "주로 대타", "at": 0.2}, {"k": "2023년", "v": "114경기 · 타율 .296", "at": 2.0, "hi": True}, {"k": "2023시즌 뒤 FA", "v": "2년 최대 5억 원", "at": 50}]),
      66: dict(stats=[{"k": "역할", "v": "주로 대타", "at": 0}, {"k": "2023년", "v": "114경기 · 타율 .296", "at": 0}, {"k": "2023시즌 뒤 FA", "v": "2년 최대 5억 원", "at": 0.6, "hi": True}]),
      70: dict(stats=[{"k": "경기", "v": "1,133경기", "at": 0.6}, {"k": "타율", "v": ".300", "at": 1.0, "hi": True}, {"k": "안타 · 홈런", "v": "992안타 · 50홈런", "at": 2.0}]),
      72: dict(stats=[{"k": "경기", "v": "1,133경기", "at": 0}, {"k": "타율", "v": ".300", "at": 0, "hi": True}, {"k": "안타 · 홈런", "v": "992안타 · 50홈런", "at": 0}])},   # 홈런·타점(65줄)·통산 타점(71줄)은 이 컷에서 말하지 않는다
  topic='고종욱통산타율3할방출', vtitle=['고종욱 방출', '통산 타율 3할'],
  thumb=TH_('카드/P28_고종욱_KIA', '고종욱 방출\n통산 타율 3할', '#B45309', ['KIA'], cutoutCrop=0.85),
  yt=dict(title='고종욱 방출 | 통산 타율 3할, SSG 방출 뒤 KIA에서 버틴 다섯 시즌 #고종욱 #기아타이거즈',
    desc='기아 타이거즈가 10월 23일 선수 6명과 재계약하지 않기로 했어요. 명단에는 외야수 고종욱도 있었어요.\n고종욱은 한양대를 졸업하고 2011년 넥센에 3라운드 전체 19순위로 입단했고, 2015년부터 3년 연속 3할, 2016년엔 타율 .334 176안타를 기록했어요. 2018년 12월 넥센·SK·삼성이 고종욱·김동엽·이지영을 맞바꾼 KBO 최초의 삼각 트레이드로 SK 유니폼을 입었고, 2021시즌 뒤 SSG에서 방출됐어요. 2022년 연봉 7천만 원에 기아로 와 주로 대타로 나섰고, 2023년 114경기 타율 .296을 기록한 뒤 2년 최대 5억 원에 FA 계약을 맺었어요. 올해는 27경기 32타수 3안타 타율 .094에 그쳤어요. 1군 통산 1,133경기 타율 .300 992안타 50홈런 417타점.',
    tags=['고종욱', '고종욱 방출', '삼각 트레이드', '통산 타율 3할'], hashtags=['#Shorts', '#고종욱', '#기아타이거즈', '#방출', '#야구자판기']))

# ── 11 이창진 · 2024 한국시리즈 4차전 선발 ─────────────
CUT('A', [0, 15, 74, 75, 76, 77, 79, 80, 81, 82, 83, 84, 85, 86],
  topic='이창진2024한국시리즈4차전선발방출', vtitle=['이창진 방출', '2024 KS 4차전 선발'],
  thumb=TH_('카드/P28_이창진_KS4', '이창진 방출\nKS 4차전 선발', '#1F2937', ['KIA'], cutoutCrop=0.85),
  yt=dict(title='이창진 방출 | 2024 한국시리즈 4차전, 최형우 대신 선발 나선 외야수 #이창진 #기아타이거즈',
    desc='기아 타이거즈가 10월 23일 선수 6명과 재계약하지 않기로 했어요. 명단에는 외야수 이창진도 있었어요.\n이창진은 인천고와 건국대를 졸업하고 2014년 롯데에 2차 6라운드로 입단했고, 2015년 롯데와 KT의 4대 5 트레이드로 KT, 2018년 6월 오준혁과의 1대1 트레이드로 기아에 왔어요. 2019년 첫 풀타임 시즌에 133경기 타율 .270으로 신인왕 후보에 올랐고, 2021~2024년 4년 연속 100경기 넘게 나섰어요. 2024년 한국시리즈 4차전엔 허리 통증으로 빠진 최형우 대신 7번 좌익수로 선발 출전해 4타수 2안타 1볼넷을 기록했고, 3회 그 볼넷으로 만든 만루에서 김태군의 만루홈런이 나왔어요. 기아는 그해 통합우승. 하지만 지난해 37경기, 올해 3경기(4타수 무안타)에 그쳤어요. 1군 통산 655경기 타율 .260 433안타 22홈런 192타점 29도루.',
    tags=['이창진', '이창진 방출', '한국시리즈 4차전', '김태군 만루홈런'], hashtags=['#Shorts', '#이창진', '#기아타이거즈', '#방출', '#야구자판기']))

# ── 12 김대유 · 박동원 FA 보상선수 ─────────────
CUT('A', [0, 15, 88, 89, 92, 93, 94, 95, 96, 97, 98],
  topic='김대유박동원보상선수방출', vtitle=['김대유 방출', '박동원 FA 보상선수'],
  thumb=TH_('KBO프로필/김대유_KIA', '김대유 방출\n박동원 보상선수', '#7C2D12', ['KIA'], cutoutCrop=0.85),
  yt=dict(title='김대유 방출 | LG 2년 37홀드, 박동원 FA 보상선수로 KIA에 온 왼손 투수 #김대유 #기아타이거즈',
    desc='기아 타이거즈가 10월 23일 선수 6명과 재계약하지 않기로 했어요. 명단에는 왼손 투수 김대유도 있었어요.\n김대유는 부산고를 졸업하고 2010년 넥센에 3라운드 전체 18순위로 입단했고, SK와 KT를 거쳐 LG에서 전성기를 보냈어요. 2021년 64경기 24홀드 평균자책점 2.13, 2022년 13홀드 평균자책점 2.04. 2022년 11월 LG가 FA 포수 박동원을 데려가자 기아가 보상선수로 김대유를 지명했어요. 기아에선 2023년 평균자책점 5.11, 2024년 8.28, 지난해 15경기 9.72였고 올해는 1군 등판이 없었어요. 그래도 2024년 37경기 8홀드로 기아 통합우승 멤버였어요. 1군 통산 255경기 6승 6패 50홀드 평균자책점 4.55.',
    tags=['김대유', '김대유 방출', '박동원 보상선수', 'FA 보상선수'], hashtags=['#Shorts', '#김대유', '#기아타이거즈', '#방출', '#야구자판기']))

# ── 13 기아 · 플레이오프 이틀 앞두고 16명 정리 ─────────────
CUT('A', [6, 7, 8, 10, 11, 14, 15, 1, 112, 113, 114, 115],
  topic='기아플레이오프이틀앞두고16명정리', vtitle=['KIA 플레이오프 이틀 전', '16명 정리'],
  thumb=TH_('카드/P22_이범호_박수', 'KIA PO 이틀 전\n16명 정리', '#1D4ED8', ['KIA'], cutoutCrop=0.85),
  yt=dict(title='기아 방출 | 플레이오프 1차전 이틀 앞두고 16명 정리, 홍건희 1년 만에 이별 #기아타이거즈 #이범호',
    desc='기아 타이거즈는 2024년 통합우승 뒤 지난해 8위로 가을야구에 나가지 못했고, 올해는 정규시즌 3위로 준플레이오프에서 LG를 5대 1, 6대 3, 13대 1로 꺾었어요. 10월 25일 대구에서 정규시즌 2위 삼성과 플레이오프 1차전을 치러요.\n그 1차전을 이틀 앞둔 10월 23일 오후, 기아는 외야수 고종욱·이창진, 투수 홍건희·김사윤·김대유·윤중현 6명과 재계약하지 않기로 했어요. 육성선수 10명의 말소 요청까지 더하면 16명이 팀을 떠나요.\n이범호 감독은 2024년 11월 3년 총액 26억 원에 재계약했고 계약은 2027년까지예요. 지난겨울 기아는 외부 FA 김범수와 3년 총액 20억 원에 계약했고, 같은 겨울 데려온 홍건희는 1년 만에 팀을 떠나게 됐어요.',
    tags=['기아 플레이오프', '이범호', '홍건희', '김범수'], hashtags=['#Shorts', '#기아타이거즈', '#이범호', '#야구자판기']))

out = []
for n, c in enumerate(CUTS, 8):   # 컷1~7 = LG·KT
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
        'rev': f'1024-kiacut{n}-v1', 'mascot': False, 'topic': c['topic'], 'vtitle': c['vtitle'],
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
