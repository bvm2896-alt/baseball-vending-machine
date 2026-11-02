# -*- coding: utf-8 -*-
"""11/2 야구이슈 쇼츠(세로 · template_issue) — 노시환 MLB 포스팅 협상 시작. 업로드 21:30(협상 22:00 직전).
 분석 전달서 11/2 ②: 사건 + 갈 수 있을지 해설. 10/24 롱폼·10/25 컷(2023 홈런왕·307억 포스팅 조항·직장폐쇄 설명·송성문/김혜성 계약·이적료)과 겹치는 문장은 뺐다.
 사실(기사 본문 2곳 이상):
  협상 한국시간 11/2 22:00 ~ 12/2 07:00, 30개 구단(스포츠경향 11/2 · MLBTR 11/1 · 한국일보·미디어펜 11/1 규정)
  2026 127경기 타율 .283 29홈런 96타점(한국일보·오마이스타·머니투데이·스포츠경향)
  2025 32홈런 개인 최다(노컷뉴스 2025/12/15 · 마이데일리 · MLBTR "career-best 32 homers")
  미국행 시 11년 307억 계약 백지화(한국일보·마이데일리) · 2026년 2월 계약(다음·OSEN)
  불발 시 한화 복귀 · 다음 해 11월 1일까지 재포스팅 불가(마이데일리·머니투데이·미디어펜)
  에이전시 "오랫동안 품어온 메이저리그 진출의 꿈"(한국일보·MHN·마이데일리)
  MLBTR "3루 수비 괜찮으면 가치↑" · SPOTV "주전 3루수 자원 많지 않은 시장"
  MLBTR "2300만 달러(한화 계약)보다 적게, 더 짧게 제시 가능"(MLBTR · SPOTV · 스포츠경향)
  협상 마감이 노사협약 만료 몇 시간 전(MLBTR "just hours before the CBA expires" · MHN 12/1 23:59 ET)
 의견(대사로 밝힘): 계약 가능성 크다 — 최근 2년 61홈런(32+29 계산) 3루수.
 안 쓴 것(한 곳 출처·충돌): 147삼진 · 관심 구단 · 수비 평가 단정 · 노사협약 만료 날짜.
실행: python -X utf8 tools/gen_1102_issue.py"""
import json, io, os, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = '2026-11-02'

def wrap16(s, n=16):
    if '\n' in s or len(s) <= n: return s
    w = s.split(' '); best = None
    for k in range(1, len(w)):
        a, b = ' '.join(w[:k]), ' '.join(w[k:])
        sc = max(len(a), len(b))
        if re.match(r'^(게|것|수|억|원|점|개|번|명|위|년|월|일|경기|타점|홈런|세이브|타석|이닝)', b) or re.search(r'\d$', a): sc += 20
        if len(a) > n or len(b) > n: sc += 5
        if len(a.split()) < 2: sc += 8
        if best is None or sc < best[0]: best = (sc, a + '\n' + b)
    return best[1]

def L(narr, sub, **k):
    assert len(narr.split(' / ')) == len(sub.split('|')), (narr, sub)
    return dict({'narr': narr, 'sub': '|'.join(wrap16(x) for x in sub.split('|'))}, **k)
CTA = {'narr': '채널 구독하고 매일 야구 이슈 받아보세요', 'sub': '채널 구독하고\n매일 야구 이슈 받아보세요!', 'rate': 1.0}
def S(i, t, **k): d = {"type": t, "startLine": i}; d.update(k); return d

NSH_BAT, NSH_PRO = '카드/P29c_노시환_경기_세로', 'KBO프로필/노시환_한화'
NSH_HEART, NSH_DUG = '카드/G18_노시환_A', '카드/P29w_노시환_0512'
NSH_FACE, NSH_PRO2 = '카드/FA11_노시환', 'KBO프로필/노시환'
T_IT = [dict(y='시작', t='11월 2일 밤 10시', at=0), dict(y='마감', t='12월 2일 아침 7시', hi=True, at=1)]

lines = [
  L('노시환이 / 메이저리그 협상에 들어가요 / 과연 계약을 따낼 수 있을까요?', '노시환이|메이저리그 협상에 들어가요|과연 계약을\n따낼 수 있을까요?'),
  L('협상 시작은 십일월 이 일 밤 열 시 / 마감은 십이월 이 일 아침 일곱 시예요', '협상 시작은\n11월 2일 밤 10시|마감은 12월 2일\n아침 7시예요'),
  L('노시환은 이 기간에 / 메이저리그 삼십 개 구단 어디와도 / 계약할 수 있어요', '노시환은 이 기간에|메이저리그 30개 구단\n어디와도|계약할 수 있어요'),
  L('노시환 측은 / 메이저리그 진출의 꿈을 향해 / 포스팅을 신청했다고 밝혔어요', '노시환 측은|메이저리그 진출의 꿈을 향해|포스팅을 신청했다고\n밝혔어요'),
  L('노시환은 이천이십육 년 사월 / 이군까지 다녀왔지만 / 백스물일곱 경기에서 / 이십구 홈런 구십육 타점을 쳤어요', '노시환은 2026년 4월|2군까지 다녀왔지만|127경기에서|29홈런 96타점을 쳤어요'),
  L('이천이십오 년엔 삼십이 홈런으로 / 개인 최다를 찍었고요', '2025년엔 32홈런으로|개인 최다를 찍었고요'),
  L('메이저리그 구단과 계약하면 / 이천이십육 년 이월 한화와 맺은 / 십일 년 삼백칠억 원 계약은 사라져요', '메이저리그 구단과 계약하면|2026년 2월 한화와 맺은|11년 307억 원 계약은\n사라져요'),
  L('계약을 못 하면 한화로 돌아오고 / 이천이십칠 년 십일월 일 일까지 / 다시 포스팅할 수 없어요', '계약을 못 하면\n한화로 돌아오고|2027년 11월 1일까지|다시 포스팅할 수 없어요'),
  L('관건은 삼루 수비예요', '관건은 3루 수비예요'),
  L('미국 야구 매체 / 엠엘비 트레이드 루머스는 / 삼루 수비가 괜찮다는 평가를 받으면 / 몸값이 오를 거라고 봤어요', '미국 야구 매체|MLB 트레이드 루머스는|3루 수비가 괜찮다는\n평가를 받으면|몸값이 오를 거라고 봤어요'),
  L('다만 한화 계약보다 / 적은 돈에 더 짧은 기간을 / 제시받을 수 있다는 전망도 있어요', '다만 한화 계약보다|적은 돈에 더 짧은 기간을|제시받을 수 있다는\n전망도 있어요'),
  L('제 생각엔 / 노시환은 계약을 따낼 가능성이 커요', '제 생각엔|노시환은 계약을 따낼\n가능성이 커요'),
  L('주전 삼루수가 귀한 / 이천이십육 년 겨울 시장에서 / 노시환은 / 이천이십오 년과 이천이십육 년 / 두 시즌 동안 육십일 홈런을 쳤거든요', '주전 3루수가 귀한|2026년 겨울 시장에서|노시환은|2025년과 2026년|두 시즌 동안 61홈런을 쳤거든요'),
  L('다만 미국에선 / 한국 리그를 일본보다 / 한 단계 아래로 본다는 평가가 있어서 / 몸값은 기대보다 낮을 수 있어요', '다만 미국에선|한국 리그를 일본보다|한 단계 아래로 본다는\n평가가 있어서|몸값은 기대보다\n낮을 수 있어요'),
  L('노시환 / 메이저리그 계약 따낼까요? / 한화로 돌아올까요?', '노시환|메이저리그 계약 따낼까요?|한화로 돌아올까요?'),
  dict(CTA),
]
R_IT = [dict(badge='계약하면', name='307억 계약\n사라짐', sub='2026년 2월 · 한화 11년', at=2),
        dict(badge='못 하면', name='한화 복귀', sub='2027년 11월 1일까지\n재포스팅 불가', hi=True, at=1, li=7)]
scenes = [
  S(0, 'photo', img=NSH_BAT, h=760, fit='cover', focus='35% 15%', text='메이저리그\n협상 시작', size=100, textAt=1),
  S(1, 'vtime', title='포스팅 협상 · 한국시간', items=T_IT, rh=190, reserve=True, text='메이저리그 30개 구단', size=72, textHide=True),
  S(2, 'vtime', cont=True, newFrom=2, title='포스팅 협상 · 한국시간', items=T_IT, rh=190, reserve=True, text='메이저리그 30개 구단', size=72, textAt=1),
  S(3, 'photo', img=NSH_HEART, h=760, fit='cover', focus='50% 30%', tag='에이전시 UA컴퍼니 발표', text='"메이저리그 진출의 꿈"', size=76, textAt=1),
  S(4, 'profile', img=NSH_PRO, name='노시환', text='2026년 4월 2군행', textAt=1, stats=[dict(k='2026년 경기', v='127', at=2), dict(k='홈런', v='29', hi=True, at=3), dict(k='타점', v='96', at=3)]),
  S(5, 'profile', img=NSH_PRO, name='노시환', text='개인 최다', textAt=1, stats=[dict(k='2025년 홈런', v='32', hi=True, at=0)]),
  S(6, 'cards', title='포스팅 결과는 둘 중 하나', items=R_IT),
  S(8, 'photo', img=NSH_FACE, h=760, fit='cover', focus='50% 22%', text='3루 수비', size=100, textAt=0),
  S(9, 'photo', img=NSH_FACE, h=760, fit='cover', focus='50% 22%', tag='MLB 트레이드 루머스 전망', text='수비 평가 = 몸값', size=90, textAt=2),
  S(10, 'photo', img=NSH_DUG, h=760, fit='cover', focus='40% 18%', tag='MLB 트레이드 루머스 전망', text='더 적은 돈\n더 짧은 기간', size=90, textAt=1),
  S(11, 'profile', img=NSH_PRO2, name='노시환'),
  S(12, 'bars', title='노시환 홈런', items=[dict(label='2025년', value=32, at=3), dict(label='2026년', value=29, at=3)], max=40, text='두 시즌 61홈런', size=80, textAt=4),
  S(13, 'profile', img=NSH_PRO2, name='노시환', text='미국 평가\nKBO는 일본 아래', textAt=1),
  S(14, 'question', text='노시환 메이저리그 계약?', size=84, choices=[dict(img=NSH_HEART, label='메이저리그\n계약'), dict(team='한화', label='한화\n복귀')]),
]
yt = dict(title='노시환 포스팅 | 11월 2일 밤 10시 메이저리그 협상 시작, 계약 따낼 수 있을까?',
  desc=('한화 노시환의 메이저리그 포스팅 협상이 한국시간 11월 2일 밤 10시에 시작돼 12월 2일 아침 7시에 끝나요.\n'
        '노시환은 메이저리그 30개 구단 중 한 곳과 계약을 따낼 수 있을까요?\n'
        '노시환은 2026년 4월 2군까지 다녀왔지만 127경기에서 29홈런 96타점을 쳤고, 2025년엔 개인 최다인 32홈런을 쳤어요. 에이전시는 노시환이 메이저리그 진출의 꿈을 향해 포스팅을 신청했다고 밝혔어요.\n'
        '메이저리그 구단과 계약하면 2026년 2월 한화와 맺은 11년 307억 원 계약은 사라지고, 계약을 못 하면 한화로 돌아와 2027년 11월 1일까지 다시 포스팅할 수 없어요.\n'
        '관건은 3루 수비예요. 미국 야구 매체 MLB 트레이드 루머스는 3루 수비가 괜찮다는 평가를 받으면 몸값이 오를 거라고 봤고, 한화 계약보다 적은 돈에 더 짧은 기간을 제시받을 수 있다는 전망도 있어요.\n'
        '제 생각엔 주전 3루수가 귀한 2026년 겨울 시장에서 2025년과 2026년 두 시즌 동안 61홈런을 친 노시환은 계약을 따낼 가능성이 커요. 다만 미국에선 한국 리그를 일본보다 한 단계 아래로 본다는 평가가 있어서 몸값은 기대보다 낮을 수 있어요. 노시환, 메이저리그 계약 따낼까요? 한화로 돌아올까요? 여러분 생각을 댓글로 남겨 주세요.\n\n'
        '지난 영상: 다음 메이저리거 언제 가? | 원태인·노시환은 이번 겨울, 곽빈·김주원은 1년 뒤'),
  tags=['노시환 포스팅', '노시환', '노시환 메이저리그', '노시환 MLB', '노시환 계약', '한화 노시환', '한화 이글스', '한화', 'KBO 포스팅', 'MLB 포스팅', '메이저리그', 'MLB', '포스팅', '프로야구', 'KBO'],
  hashtags=['#Shorts', '#프로야구', '#KBO', '#야구', '#한화이글스', '#노시환', '#메이저리그', '#야구자판기'])
e = {'speed': 1.0, 'gapScale': 0.6, 'pauseMax': 0.18, 'ttsApi': True, 'ttsTempo': 1.2, 'ttsCharsOk': 1400,
     'date': DATE, 'gameDate': DATE, 'series': '야구이슈', 'railTitle': 'KBO 이슈', 'focusTeam': '한화', 'topic': '노시환 포스팅 메이저리그 협상 시작',
     'rev': '1102-issue-v3',
     'thumb': {'teams': ['한화'], 'img': '누끼/경기_노시환_손하트_1010_한화제공', 'halo': 18, 'cutout': True, 'cutoutCrop': 1.0, 'cutoutLift': 120, 'cutoutOverlap': 380, 'cutoutFade': 0.7,
               'ph': 1000, 'logos': False, 'noPills': True, 'top': '협상 시작', 'big': '노시환\n메이저리그 도전', 'color': '#FF6600', 'perLine': True},
     'lines': lines, 'scenes': scenes,
     'youtube': {'title': yt['title'], 'description': yt['desc'], 'tags': yt['tags'], 'hashtags': yt['hashtags']},
     'source': '11/2 단독 쇼츠(야구이슈). 사실 = 기사 본문 2곳 이상(파일 머리말). 출처: 스포츠경향 11/2·MLBTR 11/1·한국일보 11/1·미디어펜 11/1·마이데일리 11/1·머니투데이 11/2·오마이스타 11/1·노컷뉴스 2025/12/15·SPOTV 11/1·MHN 11월'}
p = os.path.join(HERE, 'episodes', f'{DATE}_이슈.json')
os.makedirs(os.path.dirname(p), exist_ok=True)
json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for b in (x for l in lines for x in l['narr'].split(' / ')):
    if len(re.sub(r'[\s,?+.]', '', b)) > 22: print('호흡 초과', b)
for li, l in enumerate(lines):
    for pc in l['sub'].split('|'):
        ls = pc.split('\n')
        if any(len(x) > 16 for x in ls) or (len(ls) > 1 and len(ls[0].split()) < 2): print('자막 X', li, repr(pc))
print(p, len(lines), sum(len(l['narr'].replace(' / ', ' ')) for l in lines[:-1]), '자')
