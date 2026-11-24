# -*- coding: utf-8 -*-
"""11/24 「김호령, 기아 떠날까? | 기아 스토브리그 중간 점검」 롱폼(2026-11-23_롱폼) → 컷 쇼츠 5편(세로 vglass vF — 11/17 틀).
사용자 14:37 "숏폼으로 쪼개자" · 14:39 "너무 김호령만 3개" → 김호령 2편(떠날까·몸값) + 김태군 + 홍창기 + 외국인 3명.
첫 줄 = 관련 영상 안내(빠르게) → 훅 → 롱폼 줄(음성 재사용 voiceFrom) → 구독(저장 음성)."""
import json, io, os, copy, re, sys
sys.path.insert(0, '/home/claude/fa3s'); from wrap16 import wrap16
SRC = '/home/claude/kia23/episodes/2026-11-23_롱폼.json'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/kia23/cut/episodes'
DATE = '2026-11-24'
LONG = json.load(io.open(SRC, encoding='utf-8')); LN = LONG['lines']
REL_IMG = '상황별/썸네일_롱폼_기아스토브리그중간점검'

def NEW(narr, sub, scene, **k):
    narr = narr.replace(' /+ ', ' / +')
    pcs = [wrap16(x) for x in sub.split('|')]
    assert len(pcs) == len(narr.split(' / ')), (narr, sub)
    d = {'narr': narr, 'sub': '|'.join(pcs)}; d.update(k)
    return (None, d, scene)
def OLD(n, scene):   # n = 롱폼 대본 줄 번호(1부터)
    i = n - 1
    d = {'narr': LN[i]['narr'], 'sub': '|'.join(wrap16(x.replace('\n', ' ')) for x in LN[i]['sub'].split('|'))}
    for k in ('pauseMax',):
        if k in LN[i]: d[k] = LN[i][k]
    assert len(d['sub'].split('|')) == len(d['narr'].split(' / ')), n
    return (i, d, scene)
def T(l, v, at): return dict(l=l, v=v, at=at)
G = lambda n: '경기/' + n
KHR, NSH, KTG, HCG = G('김호령_만루포_0821_KIA제공_세로'), G('노시환_타격_세로_뉴시스'), G('김태군_덕아웃_0729_KIA제공'), G('홍창기_상체_0921_LG제공')
CJH, JSB = G('최지훈_타격_0920_SSG제공'), G('정수빈_타격_1004_두산제공')
NAIL, OLR, CAS = G('네일_주먹환호_KIA제공'), G('올러_포효_0929_KIA제공'), G('카스트로_홈런세리머니_1010_KIA제공')
FOC = {KHR: '50% 20%', NSH: '50% 18%', KTG: '50% 25%', HCG: '50% 22%', CJH: '50% 22%', JSB: '50% 22%', NAIL: '50% 22%', OLR: '50% 22%', CAS: '50% 22%'}
def CARD(img, team, name, eyebrow, cells):   # 칸은 2개까지(3개면 글이 너무 작아짐) — 새 칸이 오면 가장 오래된 칸을 뺀다
    cells = cells[-2:]
    return dict(type='v_card', img=img, team=team, name=name, eyebrow=eyebrow, cells=cells, focus=FOC.get(img, '50% 22%'))
def DUO(a, b, tag=None, tagAt=None):
    s = dict(type='v_duo', cards=[dict(c) for c in (a, b)])
    if tag: s.update(tag=tag, tagAt=tagAt)
    return s
def TALK(title, bubbles): return dict(type='v_talk', team='KIA', title=title, bubbles=[dict(t=t, at=a) for t, a in bubbles])
REL = dict(type='v_rel', img=REL_IMG, text='「기아 스토브리그 중간 점검」', chain='rel', relArrow=True)   # 11/24 14:48 사용자: 하단 화살표도
INTRO = NEW('기아 스토브리그 중간 점검은 / 아래 관련 영상에서 볼 수 있어요', '기아 스토브리그 중간 점검은|아래 관련 영상에서 볼 수 있어요', REL, ttsTempo=1.4)
# 11/24 14:48 사용자: 끝에 '기아 프론트는 잘하고 있을까요?'(롱폼 2번 줄 음성) + 관련 영상 유입 멘트 + 하단 화살표
END = [OLD(2, dict(REL)),
       NEW('전체 이야기는 / 아래 관련 영상을 /+ 눌러서 확인해 보세요', '전체 이야기는|아래 관련 영상을|눌러서 확인해 보세요', 'SAME')] + \
      [(None, {'narr': '채널 구독하고 매일 야구 이슈 받아보세요', 'sub': '채널 구독하고\n매일 야구 이슈 받아보세요!', 'rate': 1.0}, 'SAME')]
EK = '기아 · 중견수 · FA'

CUTS = []
# ── 1. 김호령, 기아 떠날까 ──
c = [NEW('김호령은 /+ 정말 기아를 떠날까요?', '김호령은|정말 기아를 떠날까요?', CARD(KHR, 'KIA', '김호령', EK, [T('기아 FA 계약', '아직 0건', 0)])),
     OLD(6, CARD(KHR, 'KIA', '김호령', EK, [T('처음 이름이 나온 팀', '롯데', 0)])),
     OLD(10, CARD(KHR, 'KIA', '김호령', EK, [T('처음 이름이 나온 팀', '롯데', -1), T('임지열 · 타케다로', '외야 채우는 중', 0), T('롯데 영입전', '가능성 높지 않다', 1)])),
     OLD(11, CARD(KHR, 'KIA', '김호령', EK, [T('주전 중견수가 빈 팀', '한화', 0)])),
     OLD(12, CARD(NSH, '한화', '노시환', '한화 · 3루수', [T('한화와 계약', '11년 307억', 1), T('외부 FA 데려올 여유', '없어짐', 2)])),
     OLD(13, CARD(NSH, '한화', '노시환', '한화 · 3루수', [T('메이저리그 포스팅', '마감 12월 2일', 1), T('미국행이면 한화', '한 해 28억쯤 여유', 3)])),
     OLD(14, CARD(NSH, '한화', '노시환', '한화 · 3루수', [T('메이저리그 포스팅', '마감 12월 2일', -1), T('미국행이면 한화', '한 해 28억쯤 여유', -1), T('한화는', '포스팅 결과를 기다림', 0)])),
     OLD(32, CARD(KHR, 'KIA', '김호령', EK, [T('기아', '조건 올려 다시 제안', 1), T('김호령', '일주일 넘게 싸인 안 함', 1)])),
     OLD(33, CARD(KHR, 'KIA', '김호령', EK, [T('기아', '조건 올려 다시 제안', -1), T('김호령', '일주일 넘게 싸인 안 함', -1), T('봐야 할 것', '다른 팀 제안 기다림', 1)])),
     OLD(36, CARD(KHR, 'KIA', '김호령', EK, [T('기아 외야 후보', '김민규 · 박재현 · 박정우', 0), T('기아가 더 올릴 가능성', '높지 않다', 1)])),
     OLD(37, DUO(dict(name='김호령', img=KHR, team='KIA', at=0), dict(name='노시환', img=NSH, team='한화', at=1.2), '노시환 미국행이면 한화가 들어올 수도', 3)),
     OLD(38, DUO(dict(name='김호령', img=KHR, team='KIA', at=-1), dict(name='노시환', img=NSH, team='한화', at=-1), '한화가 더 부르면 떠날 가능성 높다', 1))] + END
CUTS.append(dict(n=1, vtitle=['김호령', '기아 떠날까?'], lines=c, chap='김호령',
    title='김호령, 기아 떠날까? | 한화는 12월 2일 노시환 결과 기다린다', tags=['김호령', '김호령 FA', '기아 FA', 'KIA', '기아 타이거즈', '한화', '노시환', '롯데', 'FA', '스토브리그']))
# ── 2. 김호령 몸값 ──
c = [NEW('김호령 몸값은 /+ 얼마가 맞을까요?', '김호령 몸값은|얼마가 맞을까요?', CARD(KHR, 'KIA', '김호령', EK, [T('기아 제시 금액', '공개 안 됨', 0)])),
     OLD(17, CARD(KHR, 'KIA', '김호령', EK, [T('기아', '시즌 뒤 조건 올려 다시 제안', 1)])),
     OLD(18, CARD(KHR, 'KIA', '김호령', EK, [T('기아 제시 금액', '공개 안 됨', 0), T('업계 반응', '합리적 · 많이 불렀다', 1)])),
     OLD(19, CARD(KHR, 'KIA', '김호령', EK, [T('기아 제시 금액', '공개 안 됨', -1), T('업계 반응', '합리적 · 많이 불렀다', -1), T('예상 몸값', '40억 원대', 1)])),
     OLD(20, CARD(CJH, 'SSG', '최지훈', 'SSG · 중견수', [T('SSG와 계약', '4년 총액 67억', 1)])),
     OLD(21, CARD(KHR, 'KIA', '김호령', EK, [T('2027년', '35살', 1), T('풀타임 주전', '2026년 한 해', 2)])),
     OLD(22, CARD(KHR, 'KIA', '김호령', EK, [T('2027년', '35살', -1), T('풀타임 주전', '2026년 한 해', -1), T('시즌 막판', '타격 하락', 0), T('최지훈만큼은', '어렵다는 시각', 1)])),
     OLD(23, CARD(JSB, '두산', '정수빈', 'FA로 나온 두산 외야수', [T('김호령이 50억까지 오르면', '기아는 플랜 B', 0), T('다른 외야수에게', '돈을 더 쓸 수도', 2), T('후보', '정수빈', 4)]))] + END
CUTS.append(dict(n=2, vtitle=['김호령 몸값', '40억 맞아?'], lines=c, chap='김호령',
    title='김호령 몸값 40억대? | 최지훈 67억과 비교하면', tags=['김호령', '김호령 FA', '김호령 몸값', '기아 FA', 'KIA', '최지훈', '정수빈', 'FA', '스토브리그']))
# ── 3. 김태군 ──
c = [NEW('기아 포수 김태군은 /+ 에프에이 시장에서 /+ 어디로 갈까요?', '기아 포수 김태군은|FA 시장에서|어디로 갈까요?', CARD(KTG, 'KIA', '김태군', '기아 · 포수 · FA', [T('기아 FA 계약', '아직 0건', 0)])),
     OLD(40, CARD(KTG, 'KIA', '김태군', '기아 · 포수 · FA', [T('노리는 팀', '아직 없음', 0)])),
     OLD(41, CARD(KTG, 'KIA', '김태군', '기아 · 포수 · FA', [T('노리는 팀', '아직 없음', -1), T('주전 포수가 급한 팀', '지금은 없다', 0)])),
     OLD(42, CARD(G('양의지_FA계약_1117_두산제공'), '두산', '양의지', '두산 · 포수', [T('협상 첫날', '두산 잔류', 0)])),
     OLD(43, CARD(G('박동원_포수_LG제공'), 'LG', '박동원', 'LG · 포수 · FA', [T('차명석 단장', '놓쳐도 지금 포수들로', 2)])),
     OLD(44, CARD(G('박동원_포수_LG제공'), 'LG', '박동원', 'LG · 포수 · FA', [T('차명석 단장', '놓쳐도 지금 포수들로', -1), T('LG 백업', '김민식 계약 가깝다', 1), T('한화', '23살 허인서가 주전', 3)])),
     OLD(45, CARD(KTG, 'KIA', '김태군', '기아 · 포수 · FA', [T('김태군 본인', '기아에 남고 싶다', 0)])),
     OLD(46, CARD(KTG, 'KIA', '김태군', '기아 · 포수 · FA', [T('김태군 본인', '기아에 남고 싶다', -1), T('기아가 보는 자리', '한준수 뒤 백업', 1), T('김태군이 원하는 평가', '주전 포수', 2)])),
     OLD(50, CARD(NAIL, 'KIA', '네일', '183이닝 중 133이닝을 김태군과', [T('김태군과 던지면', '평균자책점 2.83', 2), T('한준수와 던지면', '평균자책점 4.70', 3)])),
     OLD(51, CARD(KTG, 'KIA', '김태군', '기아 · 포수 · FA', [T('제가 봤을 때', '기아에 남을 가능성 높다', 1)])),
     OLD(52, CARD(KTG, 'KIA', '김태군', '기아 · 포수 · FA', [T('제가 봤을 때', '기아에 남을 가능성 높다', -1), T('남은 것', '백업이냐 주전이냐', 3)]))] + END
CUTS.append(dict(n=3, vtitle=['김태군 노리는 팀', '왜 없을까?'], lines=c, chap='김태군',
    title='김태군 노리는 팀, 왜 없을까? | 기아 남을 가능성', tags=['김태군', '김태군 FA', '기아 FA', 'KIA', '기아 타이거즈', '포수 FA', '네일', '한준수', 'FA', '스토브리그']))
# ── 4. 홍창기 ──
HK = 'LG · 외야수 · FA A등급'
c = [NEW('기아 팬들 사이에서 /+ 엘지 홍창기 이름이 나오는데요', '기아 팬들 사이에서|LG 홍창기 이름이 나오는데요', CARD(HCG, 'LG', '홍창기', HK, [T('기아 팬들 사이에서', '이름이 나오는 선수', 0)])),
     OLD(55, CARD(HCG, 'LG', '홍창기', HK, [T('기아 팬 커뮤니티', '홍창기가 올 게 유력하다', 0)])),
     OLD(56, CARD(HCG, 'LG', '홍창기', HK, [T('2026년 타율', '2할 3푼 9리', 1), T('홈런', '0개', 1)])),
     OLD(57, CARD(HCG, 'LG', '홍창기', HK, [T('그래도 이름이 나오는 이유', '출루', 0)])),
     OLD(58, CARD(HCG, 'LG', '홍창기', HK, [T('그래도 이름이 나오는 이유', '출루', -1), T('볼넷 고르기', '리그 2위', 1), T('출루율', '3할 7푼 8리 · 17위', 2)])),
     OLD(59, CARD(HCG, 'LG', '홍창기', HK, [T('기아 2026년', '1번 타순 출루율 꼴찌', 1)])),
     OLD(60, CARD(HCG, 'LG', '홍창기', HK, [T('기아 2026년', '1번 타순 출루율 꼴찌', -1), T('기아 팬들', '1번 타자로 데려오자', 1)])),
     OLD(64, CARD(HCG, 'LG', '홍창기', HK, [T('A등급', 'LG에 보상선수까지', 0), T('기아 관심', '구단 쪽 말은 아직 없음', 2)])),
     NEW('김호령 계약이 어떻게 끝나느냐에 따라 /+ 홍창기 얘기도 달라질 수 있어요', '김호령 계약이 어떻게 끝나느냐에 따라|홍창기 얘기도 달라질 수 있어요',
         DUO(dict(name='김호령', img=KHR, team='KIA', at=0), dict(name='홍창기', img=HCG, team='LG', at=0), '김호령 계약 결과에 따라', 0.6))] + END
CUTS.append(dict(n=4, vtitle=['홍창기', '기아 올까?'], lines=c, chap='홍창기',
    title='홍창기, 기아 올까? | 기아 팬들이 원하는 이유', tags=['홍창기', '홍창기 FA', 'LG', 'LG 트윈스', '기아 FA', 'KIA', '출루율', '김호령', 'FA', '스토브리그']))
# ── 5. 외국인 3명 ── (11/24 16:28 사용자 "구성이 별로, 알차지 않고 궁금하지 않다" → 한 명씩 기록·몸값을 쌓는 구성
#     16:35 사용자: 첫 줄은 "기아 프론트는 외국인 선수와 협상을 잘하고 있을까요?", 끝은 "기아 스토브리그 중간 점검은 / 아래 관련 영상에서 볼 수 있어요")
def TRI3(tag, tagAt, stamp=None, stampAt=0, on=None, at=-1):
    cs = [dict(name=n, img=i, team='KIA', at=(at if at == -1 else k * .25)) for k, (n, i) in enumerate((('네일', G('네일_주먹환호_KIA제공_세로3')), ('올러', G('올러_포효_0929_KIA제공_세로3')), ('카스트로', G('카스트로_홈런세리머니_1010_KIA제공_세로3'))))]   # 16:37 사용자 '사진 가운데' → 얼굴 가운데로 세로 자른 판
    if on:
        for c_ in cs: c_['dim'] = c_['name'] != on
    s_ = dict(type='v_duo', cards=cs, tag=tag, tagAt=tagAt)
    if stamp: s_.update(stamp=stamp, stampAt=stampAt)
    return s_
# 17:07 사용자: 첫 두 줄은 중간 점검 썸네일을 보여 주며 말하고(관련 영상 안내) 본 영상으로
c = [NEW('기아 프론트는 / 외국인 선수와 협상을 /+ 잘하고 있을까요?', '기아 프론트는|외국인 선수와 협상을|잘하고 있을까요?', dict(REL)),
     NEW('전체 영상은 / 아래 관련 영상에서 볼 수 있어요', '전체 영상은|아래 관련 영상에서 볼 수 있어요', 'SAME'),
     NEW('기아가 외국인 선수 세 명을 /+ 다 잡으려면 / 올려 줄 수 있는 돈이 /+ 사십만 달러뿐이에요', '기아가 외국인 선수 세 명을|다 잡으려면|올려 줄 수 있는 돈이|40만 달러뿐이에요', TRI3('세 명 다 잡으려면 올려 줄 수 있는 돈', 1, '40만 달러', 3, at=0)),
     NEW('네일은 / 이천이십육년에 /+ 백팔십삼 이닝을 던져 /+ 리그 일위였고 / 몸값은 /+ 이백만 달러였어요', '네일은|2026년에|183이닝을 던져|리그 1위였고|몸값은|200만 달러였어요', TRI3('네일 · 2026년 183이닝 리그 1위', 1, '몸값 200만 달러', 2, on='네일')),
     NEW('올러는 / 십일승 일패에 /+ 평균자책점 삼 점 일삼을 기록했고 / 몸값은 /+ 백이십만 달러였어요', '올러는|11승 1패에|평균자책점 3.13을 기록했고|몸값은|120만 달러였어요', TRI3('올러 · 11승 1패 · 평균자책점 3.13', 1, '몸값 120만 달러', 2, on='올러')),
     NEW('카스트로는 / 타율 삼할 이푼 칠리에 /+ 홈런 스물한 개를 쳤고 / 몸값은 /+ 백만 달러였어요', '카스트로는|타율 3할 2푼 7리에|홈런 21개를 쳤고|몸값은|100만 달러였어요', TRI3('카스트로 · 타율 .327 · 21홈런', 1, '몸값 100만 달러', 2, on='카스트로')),
     OLD(68, TRI3('세 명 2026 몸값 합계', 0, '420만 달러', 2)),
     OLD(69, TRI3('세 명 다 잡으면 한도 460만 달러', 1, '올려 줄 폭 40만 달러', 3)),
     OLD(71, TRI3('올러 몸값은 올려 줄 수밖에', 0, '40만 달러를 어떻게 나눌까', 1, on='올러')),
     NEW('사십만 달러로 /+ 세 명을 다 잡을까요? / 한 명을 바꿀까요?', '40만 달러로|세 명을 다 잡을까요?|한 명을 바꿀까요?', TRI3('40만 달러로', 0, '세 명 다? 한 명 교체?', 0)),
     NEW('기아 스토브리그 중간 점검은 / 아래 관련 영상에서 볼 수 있어요', '기아 스토브리그 중간 점검은|아래 관련 영상에서 볼 수 있어요', dict(REL))]
CUTS.append(dict(n=5, vtitle=['네일·올러·카스트로', '40만 달러로 잡을까?'], lines=c, chap='외국인', intro=False, remap=[0, None, 1, 2, 3, 4, None, None, None, 8, 9],   # 17:07 2번 줄을 끼워 넣음 → 16:40에 만든 음성을 새 번호로(재합성 0)
    title='네일·올러·카스트로, 40만 달러로 다 잡을까? | 기아 외국인 재계약', tags=['네일', '올러', '카스트로', '기아 외국인', 'KIA', '기아 타이거즈', '외국인 재계약', '외국인 샐러리캡', '스토브리그']))

PREV = '김호령, 기아 떠날까? | 기아 스토브리그 중간 점검'
tot = 0
for cu in CUTS:
    rows = ([INTRO] if cu.get('intro', True) else []) + cu['lines']; lines, scenes, vf = [], [], []
    for i, (src, d, sc) in enumerate(rows):
        sc = copy.deepcopy(scenes[-1] if sc == 'SAME' else sc); sc['startLine'] = i; sc.pop('cont', None)
        lines.append(d); scenes.append(sc); vf.append(src)
    for i in range(1, len(scenes)):
        a, b = scenes[i - 1], scenes[i]
        if a['type'] == b['type'] and (a.get('img') == b.get('img') or a['type'] == 'v_rel' or (a['type'] == 'v_duo' and [x['name'] for x in a['cards']] == [x['name'] for x in b['cards']])):
            if b['type'] == 'v_duo':
                for x in b['cards']: x['at'] = -1
            b['cont'] = True; b.setdefault('chain', a.get('chain') or f"c{i}"); a.setdefault('chain', b['chain'])
    nc = sum(len(d['narr'].replace(' / ', ' ').replace('+', '')) for s_, d, _ in rows if s_ is None and 'rate' not in d); tot += nc
    EP = {"date": DATE, "gameDate": DATE, "series": "야구롱폼", "vertical": True, "theme": "mg", "vglass": True, "vF": True, "vtc": "#D81E37", "vtc2": "#B8892B",
          "railTitle": "", "focusTeam": "", "speed": 1.0, "ttsApi": True, "ttsTempo": LONG['ttsTempo'], "ttsTempoSlow": LONG.get('ttsTempoSlow', 1.15), "ttsVoice": LONG.get('ttsVoice', 'A'), "ttsWhole": False,
          "rev": f"1124-kiacut{cu['n']}-v1", "mascot": False, "topic": ' '.join(cu['vtitle']), "vtitle": cu['vtitle'],
          "gapScale": 1.1, "pauseMax": 0.4, "sentPauseMin": 0.4, "clausePauseMin": 0.3,
          "voiceFrom": {"ep": "2026-11-23_롱폼", "lines": vf},
          **({"voiceRemap": cu['remap']} if cu.get('remap') else {}),
          "mgChapters": [{"from": 0, "short": cu['chap']}],
          "source": LONG.get('source', ''), "lines": lines, "scenes": scenes,
          "youtube": {"title": cu['title'], "prev": PREV, "tags": cu['tags'], "hashtags": ["#기아타이거즈", "#스토브리그", "#야구자판기"],
                      "description": f"{cu['title']} — 2026년 11월 24일 기준이고, 전망은 제 판단이에요. 전체 이야기는 관련 영상 「{PREV}」에서 볼 수 있어요."}}
    fn = os.path.join(OUT, f"{DATE}_롱폼컷{cu['n']}.json")
    json.dump(EP, io.open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"컷{cu['n']} {' '.join(cu['vtitle'])} · {len(lines)}줄 · 롱폼 음성 {sum(1 for x in vf if x is not None)}줄 · 새 합성 {nc}자")
print('새 합성 합계', tot, '자')
