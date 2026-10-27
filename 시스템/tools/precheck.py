# -*- coding: utf-8 -*-
"""콘티 자동 사전검사 (10/28 사용자: "영상을 만들수록 검수가 금방 끝나야 하는거 아니야? 학습이라는걸 안하니?")
검수 에이전트가 라운드마다 반복해서 잡던 X 를 콘티를 만들자마자 기계로 잡는다. X 가 0 이 될 때까지 PC 에 넣지 않는다.
  ① 이름-사진 시점: 대사에서 사람 이름을 처음 말하는 호흡 = 그 사람 사진(카드·pstat·faces·rally·duel)이 뜨는 호흡
     (미리 뜸 / 늦게 뜸 / 사진 없음). 바로 앞 줄 화면에 이미 있던 사람은 통과.
  ② 화면 숫자: 화면에 뜨는 숫자가 이 줄이나 앞 줄 대사에 없으면 X (장면 부제·경기 순서 칸 이름은 제외).
  ③ 텀: 줄 첫 말이 주제어(-은/-는/-엔)인데 뒤에 텀이 없음, 호흡이 목적어(-을/-를)로 끝나 동사와 갈라짐.
사용: python3 tools/precheck.py episodes/<에피소드>.json
"""
import json, re, sys

ep = json.load(open(sys.argv[1], encoding='utf-8'))
L, SC = ep['lines'], ep['scenes']
N = len(L)
def breaths(i): return [b.replace('\n', ' ') for b in (L[i].get('sub') or '').split('|')]
def scene_of(i):
    k = 0
    for j, s in enumerate(SC):
        if s['startLine'] <= i: k = j
    return k

def people(s):
    """장면에서 사진이 있는 사람 → 뜨는 호흡(at). -1 = 이미 보임"""
    out = {}
    t = s.get('type')
    if t in ('pstat', 'plog') and s.get('img') and s.get('name'):
        nm = s['name'].split(' · ')[0]
        out[nm] = -1 if s.get('cont') else s.get('imgAt', 0)
    for key in ('items', 'plays'):
        for x in s.get(key, []) or []:
            if isinstance(x, dict) and x.get('name') and x.get('img'):
                out.setdefault(x['name'], x.get('at', 0) if x.get('at') is not None else 0)
    for side in ('left', 'right'):
        x = s.get(side)
        if isinstance(x, dict) and x.get('name') and x.get('img'):
            out[x['name']] = x.get('at', 0)
    return out

ALL = set()
for s in SC: ALL |= set(people(s))
ALL = {n for n in ALL if len(n) >= 2}
# 감독은 사용자 규칙('이름 부르는 선수는 사진')에서 제외 — 역할·부제에 '감독'이 붙은 사람
MGR = set()
def _mg(o):
    if isinstance(o, dict):
        if o.get('name') and any('감독' in str(o.get(k, '')) for k in ('role', 'note', 'sub')): MGR.add(o['name'].split(' · ')[0])
        for v in o.values(): _mg(v)
    elif isinstance(o, list):
        for v in o: _mg(v)
for s_ in SC: _mg(s_)
ALL -= MGR

X = []
prev_people = {}
for i in range(N):
    j = scene_of(i); s = SC[j]
    here = people(s) if s['startLine'] == i else {}
    if s['startLine'] != i:   # 장면이 이어지는 줄 — 이미 보이는 사람
        here = {k: -1 for k in people(s)}
    B = breaths(i)
    said = set()
    for b, txt in enumerate(B):
        for n in ALL:
            if n in said or n not in txt: continue
            said.add(n)
            at = here.get(n)
            if at is None:
                if n in prev_people: continue
                X.append((i, f"① '{n}' 이름을 말하는데(호흡 {b}) 사진 없음"))
            elif at >= 50:
                X.append((i, f"① '{n}' 사진이 숨김(at≥50)"))
            elif at >= 0 and at < b and int(at) != b:
                X.append((i, f"① '{n}' 사진이 호흡 {at}에 미리 뜸(이름은 호흡 {b})"))
            elif at >= 0 and int(at) > b:
                X.append((i, f"① '{n}' 사진이 호흡 {at}에 늦게 뜸(이름은 호흡 {b})"))
    # 이름 안 말했는데 사진만 뜨는 사람(앞 줄에서 이어진 것 제외)
    for n, at in here.items():
        if at is not None and at >= 0 and at < 50 and n not in said and n not in prev_people and not any(n in x for x in B):
            X.append((i, f"① '{n}' 사진이 뜨는데 이 줄에서 이름을 말하지 않음"))
    prev_people = {**people(s)}
    # ② 화면 숫자
    vis = []
    def walk(o, key=None):
        if isinstance(o, dict):
            if (o.get('at') is not None and (o.get('at') >= 50 or o.get('at') < 0)): return   # 숨김·이미 보인 칸 제외
            for k, v in o.items():
                if k in ('sub', 'n', 'date', 'startLine', 'at', 'imgAt', 'textAt', 'sayAt', 'noteAt', 'vsAt', 'size', 'logoSize', 'sw', 'gat', 'labelAt', 'score', 'outs', 'bases', 'runs', 'r', 'hi', 'ip', 'from', 'to', 'win', 'img', 'team', 'home', 'away', 'inn', 'chain'): continue
                walk(v, k)
        elif isinstance(o, list):
            for v in o: walk(v, key)
        elif isinstance(o, str) and key in ('v', 'k', 't', 'text', 'note', 'res', 'role', 'say', 'label', 'title', 'd'):
            vis.append(o)
    if s['startLine'] == i: walk(s)
    spoken = ' '.join(breaths(i) + (breaths(i - 1) if i else []))
    for v in vis:
        v2 = re.sub(r'\d+(·\d+)*(차전|회초|회말|회|번|위)', '', v)   # 경기·이닝 이름표는 제외
        for num in re.findall(r'\d+(?:\.\d+)?', v2):
            if num == '1' and ('하나' in spoken or '한 ' in spoken): continue
            if num not in spoken and not re.search(r'(19|20)\d\d', num):
                X.append((i, f"② 화면 '{v}' 의 숫자 {num} 을 대사로 말하지 않음"))
                break
    # ③ 텀
    w0 = B[0].split()[0] if B and B[0].split() else ''
    if B and len(B[0].split()) >= 2 and (re.search(r'(회초|회말|회|차전)(엔|에선|에는)$', w0) or (re.sub(r'(은|는|이는|가)$', '', w0) in ALL and re.search(r'(은|는)$', w0))):
        X.append((i, f"③ 주제어 '{B[0].split()[0]}' 뒤에 텀 없음"))
    for b in range(len(B) - 1):
        last = B[b].strip().split()[-1] if B[b].strip() else ''
        if re.search(r'(을|를)$', last) and len(B[b + 1].split()) <= 2 and re.search(r'(요|죠|다|고|며|서)$', B[b + 1].strip()):
            X.append((i, f"③ 목적어 '{last}' 와 동사 '{B[b + 1].strip()}' 사이 텀"))

for i, m in X: print(f"X 줄 {i:3d} · {m} · 자막: {(L[i].get('sub') or '')[:50]}")
print(f"사전검사 X {len(X)}")
sys.exit(1 if X else 0)
