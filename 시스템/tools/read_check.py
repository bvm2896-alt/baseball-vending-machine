# -*- coding: utf-8 -*-
"""10/24 사용자 "상황에 따라 읽는 방식이 다른데 이런걸 내가 하나하나 다 지적할 수 없어" / "저기 없는게 생길수도 있는데 없는건 어떻게 할거야?"
→ 나레이션(narr) 숫자 읽기 검사. 자막(sub)에 나온 숫자마다 뒤에 붙은 말(단위)을 보고
   한자어(일·이·삼…)로 읽어야 하는지 고유어(한·두·세…)로 읽어야 하는지 정한 뒤, 나레이션이 그렇게 읽는지 본다.
  X = 틀린 읽기(예: '일곱 번 좌익수', '세 차전', '이십오 살', '삼 명')
  ? = 규칙표에 없는 단위이거나 '번'처럼 문맥으로만 갈리는 곳 → 규칙표에 없는 건 통과시키지 않고 멈춘다.
      Claude 가 콘티 단계에서 하나씩 정해(표준 읽기) UNIT 표에 더하거나, 자막을 '1번 타자'처럼 분명하게 고친다. 표는 쌓일수록 커진다.
사용: python -X utf8 tools/read_check.py episodes/<콘티>.json [...]   (long_build 가 합성 전에 자동으로 부르고, X·? 가 있으면 멈춘다)"""
import json, io, re, sys

NAT_NUM = r'(?:한|두|세|네|다섯|여섯|일곱|여덟|아홉|열|스무|스물|서른|마흔|쉰|예순|일흔|여든|아흔)(?:한|두|세|네|다섯|여섯|일곱|여덟|아홉)?'
SINO_NUM = r'(?:[일이삼사오육칠팔구십백천만억영공]+)'

# 단위 → 'S'(한자어) / 'N'(고유어) / 'B'(둘 다 됨 — 검사 안 함). 앞에서부터 가장 긴 것이 이긴다.
UNIT = {
    # 날짜·시간
    '년대생': 'S', '년': 'S', '월': 'S', '일': 'S', '시즌': 'B', '개월': 'S', '주': 'S', '시간': 'N', '시': 'N', '분의': 'S', '분': 'S', '초': 'S',
    # 경기·순위·시리즈
    '경기': 'B', '차전': 'S', '전': 'S', '선승제': 'S', '위': 'S', '순위': 'S', '라운드': 'S', '차': 'S', '군': 'S', '관왕': 'S',
    '승': 'S', '패': 'S', '무': 'S', '연승': 'S', '연패': 'S', '대': 'S', '점': 'S', '실점': 'S', '자책점': 'S',
    # 타격·투구 기록
    '회': 'S', '이닝': 'S', '타수': 'S', '타석': 'B', '안타': 'S', '홈런': 'S', '타점': 'S', '득점': 'S', '도루': 'S', '볼넷': 'S', '삼진': 'S', '탈삼진': 'S',
    '세이브': 'S', '홀드': 'S', '할': 'S', '푼': 'S', '리': 'S', '루타': 'S', '루수': 'S', '루': 'S', '사': 'S', '구째': 'S', '구': 'S', '방': 'N',
    # 돈·비율·길이
    '억': 'S', '천만': 'S', '만': 'S', '천': 'S', '원': 'S', '달러': 'S', '%': 'S', '퍼센트': 'S', '포인트': 'S', '킬로': 'S', '미터': 'S', 'm': 'S', 'cm': 'S', '석': 'S',
    # 사람·물건 세기
    '살': 'N', '번째': 'N', '명': 'B', '개': 'B', '곳': 'N', '가지': 'N', '마리': 'N', '차례': 'N', '해': 'N', '달': 'N', '구단': 'B', '팀': 'B',
}
# 숫자 뒤에 단위 없이 조사·어미가 오면 수 그대로 = 한자어(평균자책점 3.24예요, 6대3으로)
PARTICLE = ('이에요', '예요', '이었', '였', '이고', '이라', '라', '로', '으로', '을', '를', '와', '과', '에', '에도', '에서', '까지', '이', '가', '은', '는', '도', '만', '의', '이게', '쩜')
# '번': 순서·타순·등번호는 한자어(칠번 좌익수), 횟수는 고유어(세 번 우승)
BEON_SINO = r'^번 ?(?:으로|에서|에|부터|까지)? ?(?:타자|타순|좌익수|우익수|중견수|지명타자|유격수|포수|투수|1루수|2루수|3루수|일루수|이루수|삼루수|배번)'
BEON_NAT = r'^번(?:째|뿐|꼴|씩| 중| 연속| 만에| 했| 우승| 올|이나| 이상|도| 다|을| 더| 받| 나|이었|이에요|은| 모두| 다시)'

NAMES = set()
def load_names(paths):
    """콘티들에 나오는 선수 이름(장면 name·items.name·사진 파일 이름 앞부분) — 'N번 박재현'(타순) 판정용"""
    import glob, os
    for p in paths:
        try: e = json.load(io.open(p, encoding='utf-8-sig'))
        except Exception: continue
        def walk(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k == 'name' and isinstance(v, str) and 2 <= len(v) <= 5 and re.fullmatch(r'[가-힣]+', v): NAMES.add(v)
                    if k == 'img' and isinstance(v, str):
                        b = re.split(r'[\\/]', v)[-1]
                        b = re.sub(r'^[A-Z]+\d*_', '', b).split('_')[0]
                        if 2 <= len(b) <= 4 and re.fullmatch(r'[가-힣]+', b): NAMES.add(b)
                    walk(v)
            elif isinstance(x, list):
                for v in x: walk(v)
        walk(e)

def cls_of(after, num=''):
    """자막에서 숫자 바로 뒤 글(after)로 읽는 법을 정한다. 반환: ('S'|'N'|'B'|'?', 단위)"""
    a = after
    big = num.replace(',', '').isdigit() and int(num.replace(',', '')) >= 20
    if a.startswith('번') and not a.startswith('번째'):
        if re.match(BEON_SINO, a) or re.match(r'^번 ?(?:으로|에서|에|부터|까지)(?![가-힣]*(?:중|만에))', a): return 'S', '번'     # 타순·포지션·순서
        nxt = a[1:].lstrip()
        if a[1:2] == ' ' and any(nxt.startswith(nm) for nm in NAMES): return 'S', '번'                                    # '1번 박재현'(타순)
        if re.match(BEON_NAT, a) or re.match(r'^번[ .,]*(?:\d|$)', a) or re.match(r'^번이 ', a) or re.match(r'^번 [가-힣]*(?:어|었|았|였|했|됐|쳤|났|뒀|왔|갔|냈|섰|졌|붙)', a): return ('B' if big else 'N'), '번'                  # 횟수
        return '?', '번'
    if a[:1] == ' ':                                                                                                     # 띄어 쓴 수(1대 1 트레이드, 2.76 삼성) → 단위 없음
        b = a.lstrip()
        if not any(b.startswith(u) for u in UNIT if len(u) >= 2): return 'S', ''
    a = a.lstrip()
    if a.startswith('시즌'):
        n_ = int(num.replace(',', '')) if num.replace(',', '').isdigit() else 0
        return ('S' if n_ >= 1900 else 'N'), '시즌'
    for u in sorted(UNIT, key=len, reverse=True):
        if a.startswith(u):
            c = UNIT[u]
            return (('B' if big and u in ('살', '번째') and False else c), u)
    if not a or not re.match(r'[가-힣A-Za-z%]', a): return 'S', ''          # 숫자만(쉼표·괄호·끝) → 한자어
    for p in sorted(PARTICLE, key=len, reverse=True):
        if a.startswith(p): return 'S', ''
    return '?', a[:4]

def narr_numeral_before(n, unit):
    """나레이션에서 그 단위 앞의 수사를 찾아 ('S'|'N', 조각) 목록으로"""
    if not unit: return []
    out = []
    for m in re.finditer(r'(?:(?<=^)|(?<=[ ,/]))(' + NAT_NUM + r'|' + SINO_NUM + r')( ?)' + re.escape(unit) + r'(?=$|[ ,./?!]|[은는이가을를에엔의도만과와로으까요째부중뿐꼴씩])', n):
        w, sp = m.group(1), m.group(2)
        nat = bool(re.fullmatch(NAT_NUM, w))
        if len(unit) == 1 and not sp and (nat or w in ('이', '일')): continue      # '네일'(이름), '이번엔'(지시어)
        out.append(('N' if nat else 'S', m.group(0)))
    return out

def check_line(sub, narr, read_ok=False):
    """read_ok: Claude 가 그 줄의 '?' 읽기를 직접 정했다는 표시(콘티 줄의 \"readOk\": true)"""
    res = []
    t = sub.replace('|', ' ').replace('\n', ' ')
    seen = set()
    for m in re.finditer(r'(?<![\d.])(\d[\d,]*(?:\.\d+)?)', t):
        after = t[m.end():m.end() + 12]
        c, u = cls_of(after, m.group(1))
        if c == '?' and not read_ok:
            res.append(('?', f"{m.group(1)}{after[:6]}", "규칙표에 없는 읽기 — 한자어/고유어를 정해 UNIT 표에 더하거나 자막을 분명하게(예: '1번 타자')"))
            continue
        if c in ('B', '?') or not u or u in seen: continue
        seen.add(u)
        for got, frag in narr_numeral_before(narr, u):
            if got != c:
                if c == 'N' and re.search('[백천만억]', frag): continue     # 큰 수는 고유어 단위라도 한자어
                res.append(('X', frag, f"'{u}' 앞은 {'한자어' if c == 'S' else '고유어'}로 읽음"))
    # 고유어 단위 앞 한 자리 한자어(삼 명, 오 개) / 나이·번째는 99까지 고유어
    for u in ('명', '개', '살', '번째', '곳', '가지', '시간'):
        for m in re.finditer(r'(?:(?<=^)|(?<=[ ,/]))((?:[이삼사오육칠팔구]?십)?[이삼사오육칠팔구]?) ?' + u + r'(?=$|[ ,./?!]|[은는이가을를에의도만과와로으까요째])', narr):
            num = m.group(1)
            if not num or num in ('이', '일'): continue
            if '십' in num and u not in ('살', '번째'): continue
            res.append(('X', m.group(0), f"'{u}' 앞은 고유어(세 명, 다섯 개, 스물다섯 살, 일곱 번째)"))
    if '%' in narr: res.append(('X', '%', "'%' 기호가 그대로 남음 → '퍼센트'로"))
    for m in re.finditer(r'(?:(?<=^)|(?<=[ ,/]))(?=[일이삼사오육칠팔구십백천]*[일이삼사오육칠팔구][십백천])[일이삼사오육칠팔구십백천만]+(?:한|두|세|네|다섯|여섯|일곱|여덟|아홉)(?= ?[가-힣])', narr):
        if re.fullmatch(r'(?:열|스물|서른|마흔|쉰|예순|일흔|여든|아흔)?(?:한|두|세|네|다섯|여섯|일곱|여덟|아홉)', m.group(0)): continue
        if re.fullmatch(r'[일이삼사오육칠팔구]', m.group(0)[:-1] if False else ''): continue
        res.append(('X', m.group(0), '한자어와 고유어가 섞인 수(예: 이백이여섯) — 숫자 바꾸기가 숫자 중간에 걸림'))
    # 타순·포지션·등번호 앞 고유어 '번'
    for m in re.finditer(r'(' + NAT_NUM + r') ?번 ?(?:으로|에서|에)? ?(?:타자|타순|좌익수|우익수|중견수|지명타자|유격수|포수|일루수|이루수|삼루수)', narr):
        res.append(('X', m.group(0), '타순·포지션 번호는 한자어(칠번 좌익수)'))
    return res

import os
DICT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'read_dict.json')
def pending_items(ep):
    """read_dict.json 의 '검수대기' 규칙이 이 콘티 자막에 쓰인 곳 → 사용자에게 한 번 확인받을 목록"""
    try: items = json.load(io.open(DICT, encoding='utf-8'))['items']
    except Exception: return []
    out = []
    for it in items:
        if it.get('status') != '검수대기': continue
        for i, l in enumerate(ep.get('lines', [])):
            sub = (l.get('sub') or '').replace('|', ' ').replace('\n', ' ')
            m = re.search(it['match'], sub)
            if m: out.append((it['id'], it['rule'], i, m.group(0), l.get('narr', '')))
    return out

def check(ep):
    out = []
    for i, l in enumerate(ep.get('lines', [])):
        for kind, frag, why in check_line(l.get('sub', '') or '', l.get('narr', '') or '', bool(l.get('readOk'))):
            out.append((i, kind, frag, why, l.get('narr', '')))
    return out

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    warn = '--warn' in sys.argv          # 10/24 사용자 "뭘 멈춰 진행계속 하고 그 부분만 나한테 검수받아" — 롱폼만들기에서는 멈추지 않고 목록만 보여 준다
    bad = unk = 0
    import glob
    load_names(args + glob.glob(os.path.join(os.path.dirname(os.path.abspath(args[0])) if args else '.', '2026-*.json')))
    pend = []
    for p in args:
        ep = json.load(io.open(p, encoding='utf-8-sig'))
        name = re.split(r"[\\/]", p)[-1]
        for i, kind, frag, why, n in check(ep):
            print(f'  [읽기 {kind}] {name} 줄 {i:02d}: "{frag}" — {why}\n      {n}')
            bad += kind == 'X'; unk += kind == '?'
        for pid, rule, i, frag, n in pending_items(ep): pend.append((name, pid, rule, i, frag, n))
    if pend:
        print('  [검수 받을 읽기 — 사용자 확인 전] (확인되면 read_dict.json 에서 확정으로 바꿔 다시 묻지 않음)')
        seen = set()
        for name, pid, rule, i, frag, n in pend:
            if (pid, frag) in seen: continue
            seen.add((pid, frag)); print(f'    · {rule}: "{frag}" ({name} 줄 {i:02d})')
    print('읽기 검사', '통과' if not (bad or unk) else f'틀린 읽기 {bad}곳 · 규칙표에 없는 읽기 {unk}곳', '/ 검수 받을 읽기 %d곳' % len(pend) if pend else '')
    sys.exit(0 if warn else (1 if (bad or unk) else 0))
