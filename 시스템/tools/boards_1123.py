# -*- coding: utf-8 -*-
# 11/23 23:20 사용자 OK("ㅇㅇ 좋아 이대로 하자") — 화면 구성 다시 짜기: 한 단락 = 한 판(sb_pan).
#   사용자 22:48 "화면이 너무 정적 — 이해가 잘 안 돼" · 22:49 "화면 활용을 너무 못해, 너무 작게 한쪽만" · 22:54 "카드가 너무 자주 바뀌고 많이 생겨서 읽기도 전에 지나가" · 23:02 "보기도 불편하고 깔끔하지도 않고"
#   23:49 사용자 "데려갈 팀으로, 계약이 끝나서 — 이렇게 말을 하다 마는 것 같은 서브텍스트는 넣지 마" → 칸의 작은 글은 '~으로·~서·~면·~는데도'로 끝나지 않는 이름꼴(명사로 끝남)만
#   11/24 00:31 사용자 "카드 안에 텍스트 정렬 제대로 다시 하고 \" 표시는 다 빼" → 화면 글에 큰따옴표 ✗, 말 카드 글은 가운데
#   규칙: 화면 전체(x120~1800 · y210~940) · 대사 한 줄에 하나씩 쌓임 · 앞에 나온 것은 그대로 · 이 줄에서 나온 칸만 노란 테 · 한 판에 큰 요소 3~4개 · 뜻을 가리는 작은 글은 넣는다
# gen_1123_kia.py 가 exec 로 읽는다(P·FC·QQ 를 그대로 쓴다). 여기서 SC 를 새로 만든다.
def _ph(who, x, y, w, h, cap=None):
    d = dict(k='ph', img=P[who], x=x, y=y, w=w, h=h)
    if cap: d['cap'] = cap
    if P[who] in FC: d['fc'] = FC[P[who]]
    return d
def _tx(t, x, y, fz, c='w', w=None, al=None, bg=False):
    d = dict(k='tx', t=t, x=x, y=y, fz=fz, c=c)
    if w: d['w'] = w
    if al: d['al'] = al
    if bg: d['bg'] = True
    return d
def _tile(l, v, x, y, w, h, vc='w', fz=76, vat=None, yl=False, al=None, big=False, lf=None):
    d = dict(k='tile', l=l, x=x, y=y, w=w, h=h, vc=vc, fz=fz); d['vz' if re.match(r'0(건|명)$', v) else 'v'] = v   # '없다'를 0으로 적는 칸(사용자 OK 시안)
    if vat is not None: d['vat'] = vat
    if yl: d['yl'] = True
    if al: d['al'] = al
    if big: d['big'] = True
    if lf: d['lf'] = lf
    return d
def _band(t, x, y, w=1680, h=84, fz=52): return dict(k='band', t=t, x=x, y=y, w=w, h=h, fz=fz)
def _logo(team, x, y, w): return dict(k='logo', team=team, x=x, y=y, w=w)
def _q(t, x, y, w, h, l=None, fz=46, tail=True):
    d = dict(k='q', t=t, x=x, y=y, w=w, h=h, fz=fz)
    if tail: d['tail'] = True
    if l: d['l'] = l
    return d
def _hd(team, t, x, y, w, h, bg='#16171C'): return dict(k='hd', team=team, t=t, x=x, y=y, w=w, h=h, bg=bg)
def _bar(x, y, w, h, f, fat=None):
    d = dict(k='bar', x=x, y=y, w=w, h=h, f=f)
    if fat is not None: d['fat'] = fat
    return d
def _ar(x, y, fz=60): return dict(k='ar', x=x, y=y, fz=fz)
# ── 그림 요소(11/23 23:56 사용자 "너무 텍스트로 떼운다" · 23:58 "텍스트만 나오는 비율은 영상의 20%까지만 허용한다") ──
def _cal(m, d, x, y, w, h): return dict(k='cal', m=m, d=d, x=x, y=y, w=w, h=h)
def _vb(x, y, w, h, f, t='', l='', c='w', fat=None, tf=64, lf=36):
    d = dict(k='vb', x=x, y=y, w=w, h=h, f=f, t=t, l=l, c=c, tf=tf, lf=lf)
    if fat is not None: d['fat'] = fat
    return d
def _hb(x, y, w, h, f, t='', c='w', tr=False, fat=None, tf=None):
    d = dict(k='hb', x=x, y=y, w=w, h=h, f=f, t=t, c=c)
    if tr: d['tr'] = True
    if fat is not None: d['fat'] = fat
    if tf: d['tf'] = tf
    return d
def _pict(n, x, y, sz=70, on=None, c='w', w=None, gap=14):
    d = dict(k='pict', n=n, x=x, y=y, sz=sz, c=c, gap=gap)
    if on is not None: d['on'] = on
    if w: d['w'] = w
    return d
def _field(x, y, w, h, pos): return dict(k='field', x=x, y=y, w=w, h=h, pos=pos)
def _scale(x, y, w, l, r, p0, p1, pat=None, rat=None, fz=56):
    d = dict(k='scale', x=x, y=y, w=w, h=170, l=l, r=r, p0=p0, p1=p1, fz=fz)
    if pat is not None: d['pat'] = pat
    if rat is not None: d['rat'] = rat
    return d
def _trend(x, y, w, h, pts, c='r', fat=None):
    d = dict(k='trend', x=x, y=y, w=w, h=h, pts=pts, c=c)
    if fat is not None: d['fat'] = fat
    return d
def _rank(x, y, w, h, n, hi): return dict(k='rank', x=x, y=y, w=w, h=h, n=n, hi=hi)
def _doc(t, x, y, w, h): return dict(k='doc', t=t, x=x, y=y, w=w, h=h)
def _sil(x, y, w, h): return dict(k='ph', img='', x=x, y=y, w=w, h=h)
P.update({'박재현': '경기/박재현_주루_KIA제공', '허인서': '경기/APBC_허인서_사진'})
VISUAL = ('ph', 'logo', 'hd', 'cal', 'vb', 'hb', 'bar', 'pict', 'field', 'scale', 'trend', 'rank', 'doc')   # 글이 아닌 요소(사진·로고·그림·도표)

def _bot(e):
    k = e['k']
    if k == 'vb': return e['y'] + (24 + e.get('lf', 36) * 1.15 if e.get('l') else 0)
    if k == 'scale': return e['y'] + 150 + e.get('fz', 56) * 1.1
    if k == 'pict': return e['y'] + e.get('sz', 70) * 1.25
    if k == 'logo': return e['y'] + e['w']
    if k == 'q': return e['y'] + e['h'] + (34 if e.get('tail') else 0)
    if k == 'tx': return e['y'] + e['fz'] * 1.15
    if k == 'ar': return e['y'] + e.get('fz', 60)
    return e['y'] + e.get('h', 0)
DY = 40   # 11/23 23:26 사용자 "전체적으로 너무 화면 상단에 붙어 있어.. 재생바랑 너무 가까워" → 제목·내용을 모두 40px 아래로(제목 y158, 내용 y250~934)
# 11/24 두 줄 자막(위 끝 y885)과 판 아래 요소가 붙는 판은 판 전체를 세로로 조금 줄인다(위 끝은 그대로, 자리·높이·글자 크기를 같은 비율로) — subchk.py 가 0 이 될 때까지 값 조정
SQ = {'toc': .935, 'lt': .933, 'jd': .932, 'wait': .918, 'of2': .94, 'tg2': .967, 'tg5': .948, 'tg6': .933, 'hc1': .946, 'hc2': .961, 'hc4': .935, 'fx': .952, 'sum': .952}
def _sq(e, k, T0):
    d = dict(e); kk = d['k']
    if kk == 'ph' and d['w'] >= 400 and d['h'] >= 600: return d   # 판의 기준 사진은 줄이지 않는다(이어지는 판끼리 자리·크기가 같아야 다시 뜨지 않는다)
    d['y'] = int(round(T0 + (d['y'] - T0) * k))
    def s(*keys):
        for key in keys:
            if d.get(key) is not None: d[key] = int(round(d[key] * k))
    if kk == 'tx': s('fz')
    elif kk == 'tile': s('h', 'fz', 'lf')
    elif kk in ('band', 'q'): s('h', 'fz')
    elif kk in ('hd', 'ph', 'cal', 'hb', 'bar', 'doc', 'trend', 'rank'): s('h')
    elif kk == 'logo': w0 = d['w']; s('w'); d['x'] += (w0 - d['w']) // 2
    elif kk == 'vb': s('h', 'tf', 'lf')
    elif kk == 'pict': s('sz')
    elif kk == 'field': w0 = d['w']; s('w', 'h'); d['x'] += (w0 - d['w']) // 2
    elif kk == 'ar': s('fz')
    return d
def _WL(t): return sum(1.0 if ord(c) > 0x3000 else .32 if c == ' ' else .62 if c.isdigit() else .58 for c in str(t or ''))
def _FIT(t, base, w, mn=26): return max(mn, min(base, int(w * .93 / max(.1, _WL(t)))))
def _fit_tile(d):   # 11/24 칸 안 글이 칸 위아래에 붙지 않게(위아래 여백 14px 이상): 작은 글 크기는 그대로(판 안에서 들쭉날쭉 ✗), 큰 글을 줄인다
    if d['k'] != 'tile': return d
    v = d.get('v') if d.get('v') is not None else d.get('vz', ''); iw = d['w'] - 60
    def th(lf0, fz0):
        lf = _FIT(d['l'], lf0, iw, 22) if d.get('l') else 0; return lf + (round(lf * .35) if d.get('l') else 0) + _FIT(v, fz0, iw, 30) * 1.08
    lf0, fz0 = d.get('lf') or 34, d.get('fz') or 76
    if d['h'] - th(lf0, fz0) >= 28: return d
    d = dict(d)
    while d['h'] - th(lf0, fz0) < 28 and fz0 > 30: fz0 -= 1
    d['fz'] = fz0; return d
def BOARD(key, n, items, title='', titles=None, tk=None, cont=False, **k):
    assert max(_bot(it[2]) for it in items) <= 852, (key, max(_bot(it[2]) for it in items))   # 두 줄 자막 위 끝(약 900) 위에서 끝낸다(여기 값 + DY 40)
    if SQ.get(key):
        T0 = min(it[2]['y'] for it in items if it[2]['k'] != 'vb')
        items = [tuple(it[:2]) + (_sq(it[2], SQ[key], T0),) + tuple(it[3:]) for it in items]
    # 11/24 검수: 한 판 안 이름표(칸의 작은 글·말 카드 이름표)는 한 크기로 — 폭에 맞춰 줄어든 가장 작은 값에 맞춘다
    _lfs = [_FIT(it[2]['l'], it[2].get('lf') or 34, it[2]['w'] - 60, 22) for it in items if it[2]['k'] == 'tile' and it[2].get('l') and not it[2].get('big')]
    if _lfs:
        _m = min(_lfs)
        items = [tuple(it[:2]) + ((dict(it[2], lf=_m) if (it[2]['k'] == 'tile' and it[2].get('l') and not it[2].get('big')) else dict(it[2], lf=min(_m, 34)) if (it[2]['k'] == 'q' and it[2].get('l')) else it[2]),) + tuple(it[3:]) for it in items]
    else:
        items = [tuple(it[:2]) + ((dict(it[2], lf=32) if (it[2]['k'] == 'q' and it[2].get('l')) else it[2]),) + tuple(it[3:]) for it in items]
    items = [tuple(it[:2]) + (_fit_tile(it[2]),) + tuple(it[3:]) for it in items]
    """items = [(줄(판 안에서 0부터), at(그 줄의 몇 번째 호흡), 요소, [마지막으로 보이는 줄])]"""
    out = []; base = len(B)   # 이 판이 시작하는 줄 번호(0부터)
    for j in range(n):
        els = []
        for it in items:
            ln, at, e = it[0], it[1], it[2]; until = it[3] if len(it) > 3 else n - 1
            if ln > j or j > until: continue
            d = dict(e); d['at'] = at if ln == j else -1; d['y'] = d['y'] + DY
            # 11/23 23:50 사용자 "나오고 금방 화면이 넘어갈 거라면 차라리 미리 텍스트 띄워": 이 줄이 끝나면 사라지는 요소가 마지막 호흡에 나오면 한 호흡 앞당기고, 큰 글도 같이 띄운다
            if ln == j and until == j:
                nb = len(re.split(r' /\+? ', ALL[base + j]))
                if d['at'] >= nb - 1 and nb >= 2: d['at'] = nb - 2
                if d.get('vat') is not None and d['vat'] >= nb - 1: d['vat'] = max(d['at'], nb - 2)   # 11/24 검수: 큰 글이 두 호흡 먼저 뜨지 않게(지우지 않고 한 호흡만 앞당김)
                for kk in ('fat', 'pat', 'rat'):
                    if d.get(kk) is not None and d[kk] >= nb - 1: d[kk] = max(d['at'], nb - 2)
                if 'pos' in d: d['pos'] = [dict(p_, at=min(p_['at'], nb - 2)) if p_.get('at') is not None and p_['at'] >= nb - 1 and nb >= 2 else p_ for p_ in d['pos']]
            if ln == j and d['k'] in ('tile', 'q', 'hd', 'cal'): d['cur'] = True
            if ln < j:
                for kk in ('vat', 'fat', 'pat', 'rat'): d.pop(kk, None)
                if d['k'] == 'scale': d['p0'] = d['p1']
                if 'pos' in d: d['pos'] = [dict(p_, at=-1) for p_ in d['pos']]
            els.append(d)
        sc = dict(type='sb_pan', key=key, chain=key, bk=key, title=(titles or {}).get(j, title), ty=118 + DY, els=els, **k)
        if tk: sc['tk'] = tk
        out.append(sc)
    if cont and B and B[-1].get('type') == 'sb_pan':   # 11/24 검수: 앞 판과 같은 사진이 같은 자리에 있으면 다시 뜨지 않고 이어받는다(같은 key 로 묶음)
        pv = B[-1]; sig = lambda e_: (e_['k'], e_.get('img'), e_.get('team'), e_['x'], e_['y'], e_.get('w'), e_.get('h'))
        have = set(sig(e_) for e_ in pv['els'])
        for sc in out: sc['key'] = sc['chain'] = pv['key']
        for d in out[0]['els']:
            if sig(d) in have: d['at'] = -1; d.pop('cur', None)
    return out

NAVY, ORNG, DSAN, LGC, NCC, KWC = '#1F3352', '#8F4A1E', '#262A52', '#7A1F45', '#2B4A73', '#5E1B2B'
RX, RW = 600, 1200          # 왼쪽에 사진·로고(x120~540)를 둔 판의 오른쪽 칸
C3 = (120, 690, 1260)       # 세 기둥(폭 540)
B = []
# ── 오프닝 1~5
B += BOARD('op1', 1, [(0, 0, _logo('KIA', 140, 300, 380)),
                      (0, 0, _tile('FA 협상 시작', '일주일', 600, 250, 570, 500, fz=150, vat=1, al='c', lf=44)),
                      (0, 3, _tile('26년 11월 23일 기준', '0건', 1200, 250, 600, 500, fz=300, vat=4, vc='y', al='c', big=True, lf=44))], title='기아가 발표한 계약', instant=True)
B += [QQ('기아 프론트는\n잘하고 있을까요?', ['KIA'], key='opq', ats=[0, 0], hl=[1], logoSize=240),
      QQ('지금\n어디까지 진행됐을까요?', ['KIA'], key='opq', ats=[0, 0], hl=[1], logoSize=240)]
B += BOARD('op4', 1, [(0, 1, _tile('계약', '4명', C3[0], 230, 540, 440, fz=230, al='c', big=True, lf=60)), (0, 1, _pict(4, C3[0], 700, 84, w=540)),
                      (0, 2, _tile('잔류', '4명', C3[1], 230, 540, 440, fz=230, al='c', big=True, lf=60)), (0, 2, _pict(4, C3[1], 700, 84, w=540)),
                      (0, 3, _tile('이적', '0명', C3[2], 230, 540, 440, fz=230, al='c', big=True, lf=60, yl=True, vat=4)), (0, 4, _pict(4, C3[2], 700, 84, on=0, c='y', w=540))], title='FA 시장', instant=True)
# 11/24 00:29 사용자 "로고 옆에 사진이랑 로고랑 다 빼 — 여긴 텍스트만 나오게 해"
B += BOARD('toc', 1, [(0, 0, _tile('', '김호령·김태군을 노리는 팀', 120, 230, 1680, 190, fz=90)),
                      (0, 1, _tile('', '두 선수는 정말 기아를 떠날까?', 120, 440, 1680, 190, fz=90)),
                      (0, 2, _tile('', '기아가 데려올 선수', 120, 650, 1680, 190, fz=90))], title='정리할 것')
# ── 김호령을 노리는 팀 6~15
B += BOARD('lt', 5, [(0, 1, _logo('롯데', 150, 250, 360)), (0, 1, _tx('롯데', 120, 640, 120, w=420, al='c')),
                     (1, 0, _field(RX, 230, 640, 480, [dict(p='LF', t='황성빈', at=0), dict(p='CF', t='김호령', hl=True, at=1)]), 1),
                     (1, 2, _tx('센터라인이', 1290, 360, 90), 1), (1, 2, _tx('강해진다', 1290, 490, 110, 'y'), 1),
                     (2, 1, _pict(3, RX, 300, 150, w=560, gap=44), 2), (2, 1, _tx('유강남', 591, 520, 46, w=190, al='c'), 2), (2, 1, _tx('노진혁', 785, 520, 46, w=190, al='c'), 2), (2, 1, _tx('한현희', 979, 520, 46, w=190, al='c'), 2),
                     (2, 2, _tile('끝난 계약', '170억 원', 1200, 270, 600, 330, fz=150, vc='y', al='c', lf=48), 2),
                     (3, 1, _ph('임지열', RX, 230, 230, 250)), (3, 0, _tile('11월 20일 · 트레이드', '임지열', 850, 230, 950, 250, fz=120, vat=1, lf=40)),
                     (3, 3, _ph('타케다', RX, 500, 230, 250)), (3, 2, _tile('일본 선수 · 마무리캠프 외야수 테스트', '타케다 아이토', 850, 500, 950, 250, fz=120, vat=3, lf=40)),
                     (4, 3, _band('김호령 영입전에 뛰어들 가능성은 높지 않다', RX, 772, w=RW, h=76, fz=48))], title='김호령을 노리는 팀', tk='롯데')
B += BOARD('hh', 4, [(0, 0, _logo('한화', 150, 250, 360)), (0, 0, _tx('한화', 120, 640, 120, w=420, al='c')),
                     (0, 1, _field(RX, 230, 600, 450, [dict(p='CF', t='빈자리', empty=True, l='주전 중견수', at=1)]), 0),
                     (0, 2, _tx('김호령이', 1250, 360, 90), 0), (0, 2, _tx('필요한 팀', 1250, 490, 110, 'y'), 0),
                     (1, 1, _ph('노시환2', RX, 230, 300, 400)),
                     (1, 1, _tile('노시환 계약', '11년 307억 원', 940, 230, 860, 190, fz=110, vc='y', lf=40), 1),
                     (1, 2, _tile('외부 FA를 데려올 여유', '없어졌다', 940, 440, 860, 190, fz=110, vat=3, lf=40), 1),
                     (2, 0, _tile('노시환', '메이저리그 포스팅', 940, 230, 860, 190, fz=100, vat=1, lf=40)),
                     (2, 2, _tile('포스팅 마감', '12월 2일', 940, 440, 320, 190, fz=72, lf=40)),
                     (2, 3, _tile('미국행일 때 생기는 여유', '한 해 28억 원쯤', 1280, 440, 520, 190, fz=72, vc='y', vat=4, lf=40)),
                     (3, 1, _band('포스팅 결과가 나와야 움직일 수 있다', RX, 720, w=RW, h=84))], title='김호령을 노리는 팀', tk='한화')
B += BOARD('ncw', 1, [(0, 0, _hd('NC', 'NC', 120, 230, 825, 130, NCC)), (0, 1, _tile('중견수', '확실한 선수가 없다', 120, 380, 825, 180, fz=84)),
                      (0, 2, _tile('외부 FA 영입', '적극적이지 않았다', 120, 580, 825, 180, fz=84, vat=3)),
                      (0, 4, _hd('키움', '키움', 975, 230, 825, 130, KWC)),
                      (0, 4, _tile('영입전', '나설지는 모른다', 975, 380, 825, 380, fz=84, vat=5))], title='중견수가 필요한 다른 팀', tk='중립')
# ── 기아의 제안 16~23
B += BOARD('of', 3, [(0, 0, _ph('김호령', 120, 220, 420, 620)),
                     (0, 1, _tile('김호령 계약', '기아가 먼저 높은 조건을 내밀었다', RX, 230, RW, 170, fz=96, vat=2, lf=38)),
                     (1, 0, _vb(760, 760, 220, 240, .7, t='처음', c='w', tf=64), 1), (1, 1, _ar(1060, 640), 1), (1, 1, _vb(1200, 760, 220, 240, 1.0, t='다시 제안', l='시즌 뒤', c='y', fat=2, tf=64, lf=40), 1),
                     (2, 1, _q('합리적', RX, 440, 590, 300, l='업계', fz=96)), (2, 2, _q('많이 불렀다', 1210, 440, 590, 300, l='다른 반응', fz=96))], title='김호령에게 내민 조건')
B += BOARD('cmp', 4, [(0, 0, _ph('김호령', 120, 220, 420, 620)),
                      (0, 0, _tile('김호령 · 언론·팬 전망', '40억 원대', RX, 230, 630, 190, fz=88, vc='y', vat=2), 1), (0, 2, _hb(1250, 295, 550, 60, 40 / 67.0, c='y', tr=True), 1),
                      (1, 1, _ph('최지훈', RX, 450, 190, 190), 1),
                      (1, 1, _tile('최지훈 · SSG와 4년 총액', '67억 원', 812, 450, 418, 190, fz=88, vc='y', vat=2), 1), (1, 2, _hb(1250, 515, 550, 60, 1.0, c='y', tr=True), 1),
                      (2, 0, _tile('김호령 · 27년', '35살', RX, 230, 590, 200, fz=110, vat=1, lf=40)), (2, 2, _tile('풀타임 주전', '26년 한 해', 1210, 230, 590, 200, fz=110, vat=3, lf=40)),
                      (3, 0, _tile('26년 시즌 막판', '타격 하락', RX, 450, RW, 200, fz=110, vat=1, lf=40)), (3, 1, _trend(1480, 475, 280, 150, [.95, .85, .8, .55, .35, .12])),
                      (3, 2, _band('최지훈만큼 받기는 어렵다는 시각', RX, 680, w=RW, h=110, fz=64))], titles={0: '김호령 몸값', 1: '같은 중견수', 2: '김호령이 최지훈과 다른 점', 3: '김호령이 최지훈과 다른 점'}, cont=True)
B += BOARD('planb', 1, [(0, 0, _tile('김호령 몸값이 오르는 경우', '50억 원', 120, 230, 560, 270, fz=110, vat=1, lf=40)), (0, 2, _ar(692, 325)),
                        (0, 2, _tile('전망', '다른 외야수에게 돈을 더 쓸 수 있다', 760, 230, 1040, 270, fz=84, vat=4, lf=40)),
                        (0, 5, _ph('정수빈', 120, 530, 330, 320)), (0, 5, _tile('두산에서 나온 외야수 · 후보', '정수빈', 480, 530, 1320, 320, fz=170, lf=40))], title='기아 플랜 B')
# ── 팬 반응 24~27
B += [QQ('팬 반응도\n팀마다 갈려요', ['KIA', '롯데', '한화'], ats=[0, 0], hl=[1], logoSize=240)]
QY = lambda i: 362 + i * 160
B += BOARD('fan', 3, [(0, 0, _hd('KIA', '기아 팬 커뮤니티', 120, 230, 1680, 120), 0),
                      (0, 1, _q('놓치면 야구 안 본다', C3[0], 400, 540, 300, fz=56), 0), (0, 3, _q('3년 계약이 맞다', C3[1], 400, 540, 300, fz=56), 0),
                      (0, 4, _q('4년 48억\u00a0원을 주는 팀이 손해', C3[2], 400, 540, 300, fz=56), 0),
                      (1, 0, _hd('롯데', '롯데 팬 커뮤니티', 120, 230, 1680, 120, NAVY), 1),
                      (1, 1, _q('그냥 사자', C3[0], 400, 540, 300, fz=60), 1), (1, 2, _q('왜 사느냐', C3[1], 400, 540, 300, fz=60), 1), (1, 4, _q('구단이 손을 뗀 거냐', C3[2], 400, 540, 300, fz=60), 1),
                      (2, 0, _hd('한화', '한화 팬 커뮤니티', 120, 230, 1680, 120, ORNG)),
                      (2, 2, _q('다른 팀에 뺏길 것 같다', 120, 400, 825, 300, fz=72)), (2, 4, _q('데려와도 쓰기 어렵다', 975, 400, 825, 300, fz=72))], title='김호령, 팬 커뮤니티 반응')
# ── 김호령은 떠날까 28~38
B += BOARD('kq', 1, [(0, 0, _ph('김호령', 120, 220, 420, 620)), (0, 0, _tx('김호령은', 660, 330, 130)),
                     (0, 1, _tx('정말 기아를 떠날까요?', 660, 500, 110, w=1000, bg=True))])
B += BOARD('jd', 3, [(0, 0, _scale(160, 380, 1600, '지금은 기아가 유리', '늦어질수록 떠날 가능성이 커진다', .22, .6, pat=2, rat=3, fz=64), 0),
                     (1, 0, _logo('KIA', 150, 240, 300)),
                     (1, 1, _tile('기아가 유리한 이유 · 먼저 제시한 높은 금액', '데려가려면 그보다 돈을 더 써야 한다', 500, 230, 1300, 320, fz=84, vat=3, lf=40)),
                     (2, 0, _hd('롯데', '롯데 · 외야를 이미 채우고 있다', 120, 580, 1680, 120, NAVY)),
                     (2, 1, _hd('한화', '한화 · 노시환 결과 전엔 움직이기 어렵다', 120, 722, 1680, 120, ORNG))], title='김호령 전망')
B += BOARD('wait', 3, [(0, 0, _ph('김호령', 120, 220, 420, 620)),
                       # 00:04 사용자 "일주일 넘게에 1234567 숫자 — 진짜 병신 같다": 뜻 없는 숫자 칸 ✗ → 싸인 칸이 비어 있는 계약서 그림
                       (0, 1, _doc('싸인', RX, 230, 240, 270)),
                       (0, 1, _tile('기아가 조건을 올린 뒤', '일주일 넘게 싸인하지 않았다', 870, 230, 930, 270, fz=76, vc='y', vat=2, lf=40)),
                       (1, 0, _tile('김호령', '다른 팀의 제안을 기다린다고 봐야 한다', RX, 520, RW, 140, fz=72, vat=2)),
                       (2, 1, _q('김호령 이적이 확정됐다는 글', RX, 680, RW, 138, l='기아 팬 커뮤니티', fz=52))], title='김호령 계약')
B += BOARD('of2', 2, [(0, 0, _ph('이범호', 120, 220, 420, 620)),
                      (0, 2, _q('김민규를 더 많이 쓴다', RX, 230, RW, 150, l='이범호 감독', fz=66)),
                      (0, 5, _tile('', '빈자리 후보', RX, 440, 380, 290, fz=72, al='c')),
                      (0, 5, _ph('박재현', 1000, 440, 390, 290, cap='박재현')), (0, 5, _ph('박정우', 1410, 440, 390, 290, cap='박정우')),
                      (1, 2, _band('기아가 돈을 더 올려 줄 가능성은 높지 않다', RX, 760, w=RW, h=84, fz=52))], title='기아 외야 후보')
B += BOARD('nh', 2, [(0, 0, _logo('KIA', 125, 222, 190)), (0, 0, _tile('기아 · 김호령 제안', '더 올려 주지 않는 상황', 340, 220, 1460, 195, fz=100, vc='y', lf=40)),
                     (0, 3, _logo('한화', 125, 437, 190)), (0, 3, _tile('노시환이 메이저리그로 가는 경우', '한화가 들어올 수 있다', 340, 435, 1460, 195, fz=100, vc='y', vat=5, lf=40)),
                     (1, 0, _tile('한화가 기아보다 많이 부르는 경우', '김호령은 떠날 가능성이 높다', 120, 650, 1680, 195, fz=100, yl=True, vat=1, lf=40))], title='김호령 변수')
# ── 김태군 39~52
B += BOARD('tgq', 1, [(0, 0, _ph('김태군', 120, 220, 420, 620)), (0, 0, _tx('그럼 김태군은', 660, 330, 120)), (0, 1, _tx('어떨까요?', 660, 500, 120, w=1000, bg=True))])
TEAMS9 = ['롯데', '한화', 'NC', '키움', '두산', 'LG', '삼성', 'KT', 'SSG']
B += BOARD('tg1', 2, [(0, 0, _ph('김태군', 120, 220, 420, 620)),
                      (0, 1, _tile('', '아직 나오지 않았다', RX, 230, RW, 290, fz=130)),
                      (1, 0, _tile('주전 포수를 급하게 찾는 팀', '지금은 없다', RX, 550, RW, 290, fz=130, vat=1, lf=44))], title='김태군을 노리는 팀', cont=True)
B += BOARD('tg2', 3, [(0, 0, _hd('두산', '두산', C3[0], 230, 540, 120, DSAN)), (0, 0, _hd('LG', 'LG', C3[1], 230, 540, 120, LGC)), (0, 0, _hd('한화', '한화', C3[2], 230, 540, 120, ORNG)),
                      (0, 1, _tile('양의지 · 협상 첫날 잔류', '포수 자리가 찼다', C3[0], 370, 540, 230, fz=56, vat=2, al='c')),
                      (1, 1, _q('박동원을 놓쳐도 지금 포수들로 간다', C3[1], 370, 540, 230, l='차명석 단장', fz=56, tail=False)),
                      (2, 1, _tile('백업 · SSG에서 나온 김민식', '계약이 가깝다', C3[1], 620, 540, 200, fz=56, vat=2, al='c')),
                      (2, 3, _tile('23살 허인서 주전 · 포수 영입', '이유가 크게 없다', C3[2], 370, 540, 230, fz=56, vat=6, al='c'))], title='주전 포수를 급하게 찾는 팀이 없는 이유')
B += BOARD('tg3', 2, [(0, 0, _ph('김태군', 120, 220, 420, 620)),
                      (0, 1, _q('기아에 남고 싶다', RX, 230, RW, 170, l='김태군 본인', fz=84)),
                      (1, 1, _tile('기아의 평가', '한준수 뒤 백업', RX, 470, 590, 250, fz=76, vat=2, lf=40)),
                      (1, 3, _tile('본인이 바라는 평가', '주전 포수', 1210, 470, 590, 250, fz=76, vc='y', vat=4, lf=40))], titles={0: '김태군의 뜻', 1: '계약이 늦어지는 이유'})
B += BOARD('tg4', 2, [(0, 0, _logo('KIA', 150, 300, 340), 0), (0, 0, _tile('기아가 제안한 금액', '공개되지 않았다', 520, 300, 1280, 340, fz=130, vat=1, lf=48), 0),
                      (1, 0, _hd('KIA', '기아 팬 커뮤니티', 120, 230, 1680, 120)),
                      (1, 1, _q('20억 원 미만이라는 말', C3[0], 400, 540, 300, fz=56)), (1, 2, _q('제시액이 너무 적다', C3[1], 400, 540, 300, fz=56)),
                      (1, 3, _q('김태군과 김호령을 다 잡자', C3[2], 400, 540, 300, fz=56))], title='김태군 계약')
B += BOARD('tg5', 2, [(0, 0, _ph('김태군', 120, 220, 420, 620)),
                      (0, 0, _tx('기아도 김태군을', 660, 330, 110), 0), (0, 1, _tx('쉽게 놓기 어렵다', 660, 490, 120, w=1000, bg=True), 0),
                      (1, 0, _tx('네일이 던진 183이닝', RX, 222, 50)), (1, 0, _bar(RX, 302, RW, 60, 133 / 183.0, fat=1)), (1, 1, _tx('133이닝을 김태군이 받았다', RX, 384, 52, 'y')),
                      (1, 2, _tx('네일 평균자책점', RX, 462, 48, 'm')),
                      (1, 2, _vb(900, 776, 210, 180, 2.83 / 4.70, t='2.83', l='포수 김태군', c='y', fat=3, tf=90, lf=34)),
                      (1, 4, _vb(1380, 776, 210, 180, 1.0, t='4.70', l='포수 한준수', c='w', fat=5, tf=90, lf=34))], titles={0: '', 1: '기아도 김태군을 쉽게 놓기 어려운 이유'})
B += BOARD('tg6', 2, [(0, 0, _ph('김태군', 120, 220, 420, 620)),
                      (0, 1, _tile('김태군', '기아에 남을 가능성이 높다', RX, 230, RW, 230, fz=96, yl=True, lf=40)),
                      (1, 0, _tile('', '데려가겠다는 팀이 나오지 않았다', RX, 484, RW, 106, fz=56)),
                      (1, 1, _tile('', '본인도 남고 싶어 한다', RX, 610, RW, 106, fz=56)),
                      (1, 2, _tile('', '백업이냐 주전이냐, 평가 차이만 남았다', RX, 736, RW, 106, fz=56))], title='김태군 전망', cont=True)
# ── 홍창기 53~65
B += [QQ('기아가 다른 팀에서\n데려올 선수는?', ['KIA'], ats=[0, 0], hl=[1], logoSize=240)]
# 11/24 02:24 사용자 "실루엣으로 나오게 해줘"(사람 모양 아이콘 ✗): 홍창기 사진에서 딴 진짜 실루엣(같은 사진·같은 자리라 사진으로 바뀔 때 모양이 그대로 맞는다)
_HCS = dict(k='ph', img='실루엣/홍창기_상체_0921_LG제공_실루엣_플랫', x=120, y=220, w=420, h=620, fc=FC[P['홍창기']])
B += BOARD('hc1', 4, [(0, 0, _HCS, 0), (0, 2, _ph('홍창기', 120, 220, 420, 620)), (0, 2, _tile('LG · 외야수', '홍창기', RX, 230, RW, 270, fz=170, lf=44)),
                      (1, 0, _q('홍창기가 올 게 유력하다', RX, 530, RW, 180, l='기아 팬 커뮤니티 · 엄청난 인기를 얻은 글', fz=76), 1),
                      (2, 1, _tile('26년 타율', '2할 3푼 9리', 600, 530, 386, 190, fz=62)), (2, 1, _tile('홈런', '없음', 1007, 530, 386, 190, fz=62)),
                      (2, 2, _tile('주전이 된 뒤', '가장 부진', 1414, 530, 386, 190, fz=62, vc='y')),
                      (3, 1, _band('이름이 나오는 이유는 출루', RX, 756, w=RW, h=84))], title='기아 팬들 사이에서 이름이 나오는 선수', tk='LG')
B += BOARD('hc2', 4, [(0, 0, _vb(200, 660, 240, 280, .632, t='2할 3푼대', l='26년 타율', c='w', tf=64, lf=44)), (0, 2, _vb(600, 660, 240, 280, 1.0, t='3할 7푼 8리', l='26년 출루율', c='y', tf=64, lf=44)),
                      (0, 3, _tx('리그 17위', 560, 762, 60, 'y', w=320, al='c')),
                      (0, 1, _tile('볼넷', '리그 두 번째', 1180, 250, 620, 290, fz=100, al='c', lf=48), 0),
                      (1, 0, _tile('기아 26년 1번 타순 출루율', '리그 꼴찌', 1180, 250, 620, 290, fz=110, vat=2, al='c', lf=40), 2),
                      (2, 2, _band('1번 타자로 데려오자', 1180, 580, w=620, h=110, fz=58), 2), (3, 2, _band('다시 살아날 거라는 기대', 1180, 580, w=620, h=110, fz=58)),
                      (3, 0, _tile('23년과 24년 타율', '3할 3푼 이상', 1180, 250, 620, 290, fz=100, vat=1, al='c', lf=44))], title='홍창기의 출루', tk='LG')
B += BOARD('hc3', 1, [(0, 0, _hd('KIA', '기아 팬 커뮤니티', 120, 230, 1680, 120)),
                      (0, 1, _q('홍창기를 데려오자', 120, 380, 825, 300, fz=80)), (0, 2, _q('하락세인 선수를 왜 사느냐', 975, 380, 825, 300, fz=80))], title='홍창기, 팬 반응')
B += BOARD('cap', 1, [(0, 0, _logo('KIA', 150, 232, 240)),
                      (0, 0, _tile('한 해 연봉 기준 · 추정', '59억 5천만 원쯤 여유', 470, 230, 1330, 250, fz=130, vc='y', vat=1, lf=44)),
                      (0, 2, _ph('김호령', 120, 500, 260, 350, cap='김호령')), (0, 2, _ph('김태군', 400, 500, 260, 350, cap='김태군')),
                      (0, 3, _tile('김호령·김태군을 잡은 뒤', '1명 더 데려올 수 있다', 690, 500, 1110, 350, fz=110, yl=True, lf=44))], title='기아 샐러리캡')
B += BOARD('hc4', 2, [(0, 0, _ph('홍창기', 120, 230, 290, 370)), (0, 0, _tile('FA 등급', 'A등급', 440, 230, 300, 175, fz=96, yl=True), 0),
                      (0, 1, _tile('데려올 때 LG에 내줘야 하는 것', '보상선수', 760, 230, 1040, 175, fz=96, vat=2), 0),
                      (0, 3, _tile('기아가 관심이 있다는 구단 쪽 말', '아직 없다', 440, 425, 1360, 175, fz=96, vat=4), 0),
                      (1, 1, _tile('김호령이 떠나는 경우 · 전망', '다른 외야수에게 돈을 더 쓸 수 있다', 440, 230, 1360, 370, fz=96, vat=3, lf=44)),
                      (1, 4, _tile('김호령 계약 결과', '홍창기 얘기도 달라질 수 있다', 120, 640, 1680, 200, fz=100, yl=True, vat=5, lf=44))], title='홍창기 영입에 걸리는 것', tk='LG')
# ── 외국인 66~71
B += [QQ('FA 말고도\n남은 계약', ['KIA'], ats=[0, 0], hl=[1], logoSize=240)]
FX, FW_ = 1050, 750
B += BOARD('fx', 5, [(0, 0, _ph('네일', 120, 220, 290, 440, cap='네일')), (0, 0, _ph('올러', 430, 220, 290, 440, cap='올러')), (0, 0, _ph('카스트로', 740, 220, 290, 440, cap='카스트로')),
                     (0, 1, _tx('아직 재계약 발표가 없다', 120, 706, 60, w=910, bg=True), 1),
                     (1, 2, _tile('3명이 26년에 받은 돈', '420만 달러', FX, 220, FW_, 190, fz=110, vat=3, lf=40), 2),
                     (2, 0, _tile('3명을 다 잡는 경우 쓸 수 있는 돈', '460만 달러', FX, 430, FW_, 190, fz=110, vat=2, lf=40), 3),
                     (2, 3, _tile('올려 줄 수 있는 폭', '40만 달러', FX, 640, FW_, 190, fz=110, yl=True, vat=4, lf=40), 3),
                     (3, 0, _tile('재계약할 선수를 정해야 하는 기한', '11월 25일', FX, 220, FW_, 190, fz=110, lf=38), 3),
                     (4, 0, _tile('올러 몸값', '올려 줄 수밖에 없다', FX, 220, FW_, 190, fz=84, vat=1, lf=40)),
                     (4, 2, _tile('남은 일', '40만 달러 나누기', FX, 430, FW_, 400, fz=96, yl=True, lf=40))], title='외국인 선수 재계약')
# ── 정리 72~79
B += BOARD('sum', 3, [(0, 1, _ph('김호령', 120, 220, 300, 400), 1),
                      (0, 2, _tile('기아 프론트 · 김호령에게 먼저 제시한 높은 금액', '다른 팀이 끼어들기 어렵다', 450, 220, 1350, 190, fz=90, vat=3, lf=40), 1),
                      (1, 0, _tile('싸인하지 않은 김호령 · 12월 2일 노시환 결과', '한화가 들어올 수 있다', 450, 430, 1350, 190, fz=90, vc='y', vat=2, lf=40), 1),
                      (2, 0, _ph('김태군', 135, 220, 270, 290)), (2, 1, _tile('김태군 · 데려가겠다는 팀이 나오지 않았다', '기아에 남을 가능성이 높다', 450, 220, 1350, 290, fz=100, vat=2, lf=44)),
                      (2, 3, _ph('네일', 135, 540, 270, 290)), (2, 3, _tile('외국인 3명', '40만 달러 안에서 풀어야 한다', 450, 540, 1350, 290, fz=100, vat=4, lf=44))], title='기아 프론트 중간 점검')
B += BOARD('sum2', 1, [(0, 1, _ph('김호령', 120, 250, 270, 360, cap='김호령')), (0, 1, _tile('먼저 높게 부른 것', '잘한 일', 410, 250, 535, 360, fz=120, yl=True, al='c', vat=2, lf=34)),
                       (0, 3, _ph('김태군', 975, 250, 270, 360, cap='김태군')), (0, 3, _tile('시즌 중에 매듭짓지 못한 것', '아쉽다', 1265, 250, 535, 360, fz=120, al='c', vat=4, lf=34))], title='기아 프론트 평가')
B += BOARD('ask', 2, [(0, 0, _ph('김호령', 540, 200, 380, 490, cap='김호령')), (0, 0, _ph('김태군', 1000, 200, 380, 490, cap='김태군')),
                      (0, 1, _tx('잡을 수 있을까요?', 120, 720, 100, w=1680, al='c', bg=True), 0),
                      (1, 1, _tx('다른 팀에게 뺏길까요?', 120, 720, 100, w=1680, al='c', bg=True))])
B += [QQ('여러분은\n어떻게 보세요?', ['KIA'], key='endq', hl=[1], logoSize=240),
      QQ('계약이 발표되면 바로 정리해 드릴게요\n채널 구독하고\n기아 소식 받아보세요', ['KIA'], key='endq', ats=[0, 0, 0], hl=[1, 2], logoSize=240)]
SC = B
# 11/24 00:51 사용자 "한 화면마다 들어있는 요소들이 너무 많아" — 한 화면 요소는 7개까지(대개 6개 아래)
_cnt = [(i + 1, len(s_['els'])) for i, s_ in enumerate(SC) if s_['type'] == 'sb_pan']
print('요소 수 가장 많은 화면:', sorted(_cnt, key=lambda z: -z[1])[:8])
assert max(n_ for _, n_ in _cnt) <= 7, [c_ for c_ in _cnt if c_[1] > 7]
# 23:58 사용자 "텍스트만 나오는 비율은 영상의 20%까지만 허용한다" — 글만 있는 줄(사진·로고·그림·도표가 하나도 없는 줄)의 글자 수 비율
_txt = [i for i, s_ in enumerate(SC) if s_['type'] == 'sb_pan' and not any(e_['k'] in VISUAL for e_ in s_['els'])]
_len = lambda i: len(re.sub(r'[ /+]', '', ALL[i]))
TEXT_ONLY = sum(_len(i) for i in _txt) / float(sum(_len(i) for i in range(len(SC))))
print('글만 나오는 줄:', [i + 1 for i in _txt], '비율 %.1f%%' % (TEXT_ONLY * 100))
assert TEXT_ONLY <= 0.20, TEXT_ONLY
