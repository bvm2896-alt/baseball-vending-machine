# -*- coding: utf-8 -*-
"""10/26 단독 쇼츠(세로 1080x1920) — 주제전달-1026 ②③.
 컷1 = 김재윤 플레이오프 이탈(12:00) · 컷2 = 구자욱 복귀(15:30). 전 줄 새 합성(API). 파일 episodes/2026-10-26_롱폼컷N.json
 → 사용자 `야구롱폼\\롱폼_숏츠만들기.cmd`.
 근거: 기사 본문 2곳 이상(아래 SRC). 근거모음의 '이승민 94경기'는 오류 — MK스포츠·SPOTV·머니투데이 본문 모두 74경기.
실행: python -X utf8 tools/gen_1026_shorts.py"""
import json, io, os, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATE = '2026-10-26'

def S(i, t, **k): d = {"type": t, "startLine": i}; d.update(k); return d
def st(k, v, at=0, **x): return dict({"k": k, "v": v, "at": at}, **x)
def vstamp(t, at=0, c="gold", **k): return dict(type="stamp", t=t, at=at, c=c, **k)
def vq(date, text, at, src=True, **k): return dict(type="quote", date=date, text=text, at=at, src=src, **k)
def pv(i, img, name, sub, viz=(), stats=(), team="삼성", **k):
    return S(i, "pstat", img=img, team=team, name=name, sub=sub, viz=list(viz), stats=list(stats), **k)

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

CTA = {'narr': '채널 구독하고 매일 야구 이슈 받아보세요', 'sub': '채널 구독하고\n매일 야구 이슈 받아보세요!', 'rate': 1.0}

def L(narr, sub):
    assert len(narr.split(' / ')) == len(sub.split('|')), (narr, sub)
    return {'narr': narr, 'sub': '|'.join(wrap16(x) for x in sub.split('|'))}

def stp(d, t, at=0, c=None): return dict(d=d, t=t, at=at, **({"c": c} if c else {}))
def vsteps(items): return dict(type="steps", items=items)
KJY, PJM, ISM = '경기/김재윤_투구_1007_삼성제공', '경기/박진만_박수_0908_삼성제공', '카드/P31_이승민_삼성제공'
EPS = []

# ── 컷1 김재윤 이탈 ─────────────────────────────
lines = [
  dict(L('삼성 구회가 비었어요 / +마무리가 빠졌거든요', '삼성 9회가 비었어요|마무리가 빠졌거든요'), gapAfter=0.65),
  L('세이브 일 위 김재윤이 / +플레이오프 엔트리에서 빠졌어요', '세이브 1위 김재윤이|플레이오프 엔트리에서 빠졌어요'),
  dict(L('김재윤은 갈비뼈 옆 근육인 오른쪽 전거근을 다쳐 / +약 이 주 동안 쉬어야 돼요', '김재윤은 갈비뼈 옆 근육인\n오른쪽 전거근을 다쳐|약 2주 동안 쉬어야 돼요'), gapAfter=0.65),
  dict(L('김재윤은 올해 예순네 경기에 나와 / 삼십오 세이브를 올렸고, / +평균자책점은 삼쩜이이였어요', '김재윤은 올해 64경기에 나와|35세이브를 올렸고|평균자책점은 3.22였어요'), gapAfter=0.65),
  L('기아와의 플레이오프 일차전은 / 이십육 일 저녁 여섯 시 반, / +대구에서 열려요', '기아와의 플레이오프 1차전은|26일 저녁 6시 반|대구에서 열려요'),
  L('박진만 감독은 / 마무리를 딱 정해 두지 않고 / +상황에 따라 쓸 수 있는 투수를 다 쓰겠다고 했어요', '박진만 감독은|마무리를 딱 정해 두지 않고|상황에 따라 쓸 수 있는 투수를 다 쓰겠다고 했어요'),
  dict(L('그래도 위기 상황엔 박진만 감독이 / +가장 믿음직스러운 이승민을 내겠대요', '그래도 위기 상황엔\n박진만 감독이|가장 믿음직스러운\n이승민을 내겠대요'), gapAfter=0.65),
  dict(L('이승민은 올해 일흔네 경기에서 / 육십팔 이닝을 던져 이십삼 홀드를 올렸고, / +평균자책점은 이쩜육오예요', '이승민은 올해 74경기에서|68이닝을 던져 23홀드를 올렸고|평균자책점은 2.65예요'), gapAfter=0.65),
  dict(L('기아전에선 이승민이 더 강했어요. / +여덟 경기 평균자책점이 일쩜일칠이에요', '기아전에선 이승민이 더 강했어요|8경기 평균자책점이\n1.17이에요'), gapAfter=0.65),
  dict(L('이승민은 / +우리 불펜 투수들은 항상 강하다고 했어요', '이승민은|우리 불펜 투수들은 항상 강하다고 했어요'), gapAfter=0.65),
  L('삼성의 구회, / 이승민이 지킬까요? / +아니면 다른 투수가 지킬까요?', '삼성의 9회|이승민이 지킬까요?|아니면 다른 투수가 지킬까요?'),
  L('여러분 생각은 / +댓글로 남겨 주세요', '여러분 생각은|댓글로 남겨 주세요'),
  dict(CTA),
]
K1 = [st("2026 세이브", "1위", 0.0, hi=True)]
K2 = [st("10월 24일 · 삼성 발표", "오른쪽 전거근 손상", 0.0), st("휴식", "약 2주", 0.6)]
K3 = [st("2026년", "64경기", 0.0), st("세이브", "35", 1.0, hi=True), st("평균자책점", "3.22", 1.6)]
I1 = [st("2026년", "74경기", 0.0), st("이닝", "68", 1.0), st("홀드", "23", 1.0), st("평균자책점", "2.65", 2.0, hi=True)]
I2 = [dict(x, at=-1) for x in I1]
KS = [stp("KIA전 8경기", "평균자책점 1.17", c="good")]
def KV(ats): return vsteps([dict(t, at=a) for t, a in zip(KS, ats)])
Q1 = vq("10월 25일 · 박진만 감독", "마무리는 딱 정해 놓진 않았다", 1.0)
Q2 = vq("10월 25일 · 박진만 감독 · 요약", "이승민이 위기 상황에 나가게 될 것 같다", 1.0)
STP = vstamp("플레이오프 엔트리 제외", 1.0, "gold", size=46)
scenes = [
  pv(0, None, "삼성 라이온즈", "플레이오프", [vstamp("마무리 이탈", 0.5, "gold", size=52)], []),
  pv(1, KJY, "김재윤", "삼성 마무리", [STP], K1, chain="kjy", enterAt=0.0),
  pv(2, KJY, "김재윤", "삼성 마무리", [dict(STP, at=-1)], K2, chain="kjy"),
  pv(3, KJY, "김재윤", "삼성 마무리", [dict(STP, at=-1)], K3, chain="kjy"),
  S(4, "matchup", left="KIA", right="삼성", score="VS", tag="플레이오프 1차전 · 10월 26일 대구", text="저녁 6시 반", size=84),
  pv(5, PJM, "박진만", "삼성 감독", [Q1], [], chain="pjm", enterAt=0.0),
  pv(6, PJM, "박진만", "삼성 감독", [Q2], [], chain="pjm"),
  pv(7, ISM, "이승민", "삼성 좌완 불펜", [KV([50])], I1, chain="ism", enterAt=0.0),
  pv(8, ISM, "이승민", "삼성 좌완 불펜", [KV([1.0])], I2, chain="ism"),
  pv(9, ISM, "이승민", "삼성 좌완 불펜", [vq("10월 25일 · 이승민 · 요약", "우리 불펜 투수들은 항상 강하다", 1.0)], [], chain="ism"),
  S(10, "question", text="삼성의 9회\n이승민? 다른 투수?", mood="wave", revealAt=1, img=ISM, size=96),
]
SRC1 = ("기록 출처: 머니투데이(2026/10/24·10/26)·서울신문(2026/10/24)·OSEN(2026/10/24)·스포츠경향(2026/10/25)·MK스포츠(2026/10/26)·SPOTV뉴스(2026/10/25)·뉴스1(2026/10/25)\n"
        "사진: 삼성 라이온즈 제공")
EPS.append(dict(n=1, topic='김재윤플레이오프이탈9회는누가', vtitle=['김재윤 플레이오프 이탈', '삼성 9회는 누가?'], lines=lines, scenes=scenes,
  thumb=dict(halo=18, cutout=True, cutoutCrop=0.85, cutoutLift=180, cutoutOverlap=330, cutoutFade=0.62, ph=1000, logos=False, noPills=True, top='', perLine=True,
             img=KJY, big='삼성 9회가\n비었다', color='#1E5BB8', teams=['삼성']),
  yt=dict(title='김재윤 플레이오프 이탈 | 35세이브 마무리 없는 삼성, 9회는 누가? #김재윤 #삼성라이온즈',
    desc=('삼성 마무리 김재윤이 기아와의 플레이오프 엔트리에서 빠졌어요. 오른쪽 전거근(갈비뼈 옆 근육) 근육·근막 손상으로 약 2주 휴식이 필요해요. 김재윤은 올해 64경기 7승 5패 35세이브, 평균자책점 3.22로 세이브 1위였어요.\n'
          '박진만 감독은 마무리를 딱 정해 두지 않고 상황에 따라 쓸 수 있는 투수를 다 활용하겠다면서, 가장 믿음직스러운 이승민을 위기 상황에 내겠다고 했어요. 이승민은 올해 74경기 68이닝 6승 2패 2세이브 23홀드, 평균자책점 2.65였고, 기아전 8경기 평균자책점은 1.17이에요.\n'
          '플레이오프 1차전은 10월 26일 오후 6시 30분 대구에서 열려요. 삼성의 9회, 이승민이 지킬까요? 아니면 다른 투수가 지킬까요? 여러분 생각을 댓글로 남겨 주세요.\n\n' + SRC1),
    tags=['김재윤', '삼성 라이온즈', '삼성', '김재윤 부상', '이승민', '박진만', '삼성 마무리', '플레이오프', '기아 삼성', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#프로야구', '#KBO', '#야구', '#삼성라이온즈', '#김재윤', '#이승민', '#플레이오프', '#야구자판기'])))

# ── 컷2 구자욱 복귀 ─────────────────────────────
GJU = '경기/구자욱_세리머니_0827_삼성제공'
lines2 = [
  dict(L('타격왕 구자욱이 돌아왔어요 / +타율 삼할 칠푼 일리예요', '타격왕 구자욱이 돌아왔어요|타율 3할 7푼 1리예요'), gapAfter=0.65),
  L('구자욱은 구월 삼십일에 / +왼쪽 햄스트링을 다쳤어요', '구자욱은 9월 30일에|왼쪽 햄스트링을 다쳤어요'),
  L('허벅지 뒤쪽 힘줄이 손상돼 / +정규시즌 남은 경기엔 나서지 못했죠', '허벅지 뒤쪽 힘줄이 손상돼|정규시즌 남은 경기엔\n나서지 못했죠'),
  L('재검진에서는 / +출혈과 부종이 가라앉았다는 소견을 받았어요', '재검진에서는|출혈과 부종이\n가라앉았다는 소견을 받았어요'),
  L('자체 청백전엔 / 수비 없이 타격만 하는 지명타자로 나와 / +안타를 쳤고요', '자체 청백전엔|수비 없이 타격만 하는\n지명타자로 나와|안타를 쳤고요'),
  L('+플레이오프 서른 명 엔트리에 이름을 올렸어요', '플레이오프 30명 엔트리에\n이름을 올렸어요'),
  L('다만 주루와 수비를 정상적으로 할 수 있을지는 / +지켜봐야 돼요', '다만 주루와 수비를\n정상적으로 할 수 있을지는|지켜봐야 돼요'),
  L('그래서 / +수비 부담이 없는 지명타자로 나설 가능성이 거론돼요', '그래서|수비 부담이 없는 지명타자로\n나설 가능성이 거론돼요'),
  dict(L('+대타로 기다리는 방안도 있어요', '대타로 기다리는 방안도 있어요'), gapAfter=0.65),
  L('이번 가을이 끝나면 / +구자욱은 에프에이 자격을 얻어요', '이번 가을이 끝나면|구자욱은 FA 자격을 얻어요'),
  dict(L('이천이십이 년에 맺은 오 년 백이십억 원 계약이 / +올해로 끝나요', '2022년에 맺은\n5년 120억 원 계약이|올해로 끝나요'), gapAfter=0.65),
  L('다시 이번 가을로 돌아가면 / 구자욱이 나설 수 있는 첫 경기는 / +기아와의 플레이오프 일차전이에요', '다시 이번 가을로 돌아가면|구자욱이 나설 수 있는\n첫 경기는|기아와의 플레이오프\n1차전이에요'),
  dict(L('경기는 이십육 일 저녁 여섯 시 반에 / +대구에서 열려요', '경기는 26일 저녁 6시 반에|대구에서 열려요'), gapAfter=0.65),
  L('구자욱, 지명타자로 선발 출전할까요? / +대타로 기다릴까요?', '구자욱 지명타자로\n선발 출전할까요?|대타로 기다릴까요?'),
  L('여러분 생각은 / +댓글로 남겨 주세요', '여러분 생각은|댓글로 남겨 주세요'),
  dict(CTA),
]
T = [stp("부상", "9월 30일 · 왼쪽 햄스트링", c="bad"), stp("결장", "정규시즌 남은 경기", c="bad"),
     stp("재검진", "출혈·부종 가라앉음", c="good"), stp("청백전", "지명타자 · 안타", c="good"),
     stp("엔트리", "플레이오프 30명 합류", c="gold")]
def TL(ats): return vsteps([dict(t, at=a) for t, a in zip(T, ats)])
G0 = [st("2026 시즌 타율", ".371", 1.0, hi=True)]
def g(i, viz=(), stats=(), **k): return pv(i, GJU, "구자욱", "삼성 외야수", viz, stats, chain="gju", **k)
P = [stp("주루·수비", "정상 여부 미정", c="bad"), stp("방안 1", "지명타자", c="gold"), stp("방안 2", "대타 대기", c="gold")]
def PL(ats): return vsteps([dict(t, at=a) for t, a in zip(P, ats)])
C = [stp("2022년", "5년 120억 원 · 올해 끝", c="good"), stp("2026년", "시즌 뒤 FA 자격", c="gold")]
def CL(ats): return vsteps([dict(t, at=a) for t, a in zip(C, ats)])
E1 = st("첫 경기", "플레이오프 1차전 · KIA전", 1.5, hi=True)
E2 = st("10월 26일", "저녁 6시 반 · 대구", 0.0)
scenes2 = [
  g(0, [], G0),
  g(1, [TL([0.0, 50, 50, 50, 50])], []),
  g(2, [TL([-1, 1.0, 50, 50, 50])], []),
  g(3, [TL([-1, -1, 0.5, 50, 50])], []),
  g(4, [TL([-1, -1, -1, 0.5, 50])], []),
  g(5, [TL([-1, -1, -1, -1, 0.0])], []),
  g(6, [PL([0.3, 50, 50])], []),
  g(7, [PL([-1, 0.6, 50])], []),
  g(8, [PL([-1, -1, 0.0])], []),
  g(9, [CL([50, 0.5])], []),
  g(10, [CL([0.0, -1])], []),
  g(11, [], [E1]),
  g(12, [], [dict(E1, at=-1), E2]),
  S(13, "question", text="구자욱 1차전\n지명타자? 대타?", mood="wave", revealAt=1, faces=["카드/T12_구자욱"]),
]
SRC2 = ("기록 출처: 머니투데이(2026/10/24·10/26)·마이데일리(2026/10/25)·MHN(2026/10/25)·데일리안(2026/7/30)·세계일보(2026/9/7)·매일신문(2026/10/18)·뉴스1(2026/10/25)·스포츠경향(2026/10/25)\n"
        "사진: 삼성 라이온즈 제공")
EPS.append(dict(n=2, topic='구자욱복귀타격왕플레이오프', vtitle=['구자욱 돌아왔다', '타격왕 플레이오프 합류'], lines=lines2, scenes=scenes2,
  thumb=dict(halo=18, cutout=True, cutoutCrop=0.85, cutoutLift=180, cutoutOverlap=330, cutoutFade=0.62, ph=1000, logos=False, noPills=True, top='', perLine=True,
             img=GJU, big='타격왕\n복귀', color='#1E5BB8', teams=['삼성']),
  yt=dict(title='구자욱 돌아왔다 | 타율 .371 타격왕, 햄스트링 딛고 플레이오프 #구자욱 #삼성라이온즈',
    desc=('삼성 구자욱이 플레이오프 엔트리에 들어왔어요. 구자욱은 올해 타율 .371로 타격왕에 올랐지만, 9월 30일 왼쪽 햄스트링(허벅지 뒤쪽 근육) 힘줄을 다쳐 정규시즌 남은 경기에 나서지 못했어요.\n'
          '재검진에서 출혈과 부종이 가라앉았다는 소견을 받았고, 자체 청백전에 지명타자로 나와 안타를 쳤어요. 다만 정상적인 수비와 주루가 가능할지는 지켜봐야 돼서, 지명타자로 나설 가능성이 거론되고, 대타로 기다리는 방안도 있어요.\n'
          '구자욱은 2022년 맺은 5년 120억 원 계약이 올해로 끝나, 올 시즌이 끝나면 FA 자격을 얻어요. 기아와의 플레이오프 1차전은 10월 26일 오후 6시 30분 대구에서 열려요. 돌아온 타격왕, 1차전에 지명타자로 선발 출전할까요? 대타로 기다릴까요? 여러분 생각을 댓글로 남겨 주세요.\n\n' + SRC2),
    tags=['구자욱', '삼성 라이온즈', '삼성', '구자욱 복귀', '구자욱 부상', '구자욱 FA', '타격왕', '플레이오프', '기아 삼성', '프로야구', 'KBO', '야구자판기'],
    hashtags=['#Shorts', '#프로야구', '#KBO', '#야구', '#삼성라이온즈', '#구자욱', '#플레이오프', '#야구자판기'])))

out = []
for c in EPS:
    sc = [dict(s) for s in c['scenes']]
    for a, b in zip(sc, sc[1:]):
        if b.get('chain') and a.get('chain') == b.get('chain'): b['cont'] = True
    assert sc[0]['startLine'] == 0
    e = {
        'date': DATE, 'gameDate': DATE, 'series': '야구롱폼', 'vertical': True,
        'railTitle': '', 'focusTeam': '', 'speed': 1.0, 'ttsApi': True, 'ttsTempo': 1.3, 'ttsTempoSlow': 1.15,
        'rev': f'1026-short{c["n"]}-v1', 'mascot': False, 'topic': c['topic'], 'vtitle': c['vtitle'],
        'gapScale': 0.6, 'pauseMax': 0.18,
        'source': '단독 쇼츠(주제전달-1026). 사실 출처 = 기사 본문 2곳 이상, 프로젝트 claude/1026-롱폼31-PO1차전리뷰-근거모음.md + 본문 재대조.',
        'lines': c['lines'], 'scenes': sc, 'thumb': c['thumb'],
        'youtube': {'title': c['yt']['title'], 'description': c['yt']['desc'], 'tags': c['yt']['tags'], 'hashtags': c['yt']['hashtags']},
    }
    p = os.path.join(HERE, 'episodes', f"{DATE}_롱폼컷{c['n']}.json")
    json.dump(e, io.open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    est = sum(len(l['narr'].replace(' / ', ' ')) * 0.14 + 0.3 * 0.6 * l['narr'].count(' / ') + 0.45 * 0.6 for l in c['lines']) + 1.0
    chars = sum(len(l['narr'].replace(' / ', ' ').replace('+', '')) for l in c['lines'][:-1])
    for b in (x for l in c['lines'] for x in l['narr'].split(' / ')):
        if len(re.sub(r'[\s,?+.]', '', b)) > 22: print('호흡 초과', c['n'], b)
    for li, l in enumerate(c['lines']):
        for pc in l['sub'].split('|'):
            ls = pc.split('\n')
            if any(len(x) > 16 for x in ls) or (len(ls) > 1 and len(ls[0].split()) < 2): print('자막 X', c['n'], li, repr(pc))
    out.append((c['n'], c['topic'], len(c['lines']), len(sc), round(est), chars, len(c['yt']['title'])))
for r in out: print(r)
