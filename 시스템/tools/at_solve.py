# 10/25 04시 사용자("첫 번째 대사를 할 때 이미 두 번째 이미지가 나와 있어야 — 그렇다고 첫 번째 이미지가 빨리 넘어가 읽을 시간이 없어서도 안 돼"):
# 다음 장면은 그 문장 시작에 바로 들어오고(enterAt 없음), 읽을 시간이 모자란 글은 '그 문장 안에서' 조금씩 일찍 띄운다.
# 같은 장면 앞 글보다 먼저 뜨지 않게(순서 유지), 말하는 호흡보다 0.75호흡 넘게 앞서지 않게(미리 뜨기 금지) 한계를 둔다.
# 사용: python tools/at_solve.py 콘티.json work/timeline.json(또는 어림 timeline) 결과.json
import json, re, sys, os, copy, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import late_check as LC

def refs(sc):
    """keys() 와 같은 열쇠 → (담은 dict, 'at' 또는 'textAt')"""
    r = {}
    for s in sc.get('stats') or []: r[('stat', s.get('k'), s.get('v'))] = (s, 'at')
    for v in sc.get('viz') or []:
        t = v.get('type')
        if t in ('steps', 'seasons', 'mini', 'hops'):
            for x in v.get('items') or []: r[(t, x.get('d'), x.get('name') or x.get('t') or '')] = (x, 'at')
        elif t == 'quote': r[('quote', v.get('text'))] = (v, 'at')
        elif t in ('stamp', 'note'): r[(t, v.get('t'))] = (v, 'at')
    for b in sc.get('bubbles') or []: r[('bubble', b.get('text'))] = (b, 'at')
    for it in sc.get('items') or []:
        lab = it.get('name') or it.get('label') or it.get('v') or it.get('k'); r[('item', lab, it.get('note') or it.get('k'))] = (it, 'at')
    if sc.get('text'): r[('text', sc['text'])] = (sc, 'textAt')
    return r

def fails(ep, tl):
    """(장면, 열쇠 또는 None(장면 전체)) 목록"""
    out = []
    p = '/tmp/_at_solve_ep.json'; json.dump(ep, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): LC.tl_check(p, tl)
    for l in buf.getvalue().splitlines():
        m = re.match(r'X 줄\s+(\d+) · (.+?) · ', l)
        if m: out.append((int(m.group(1)), m.group(2))); continue
        m = re.match(r'X 장면\s+(\d+) 전체', l)
        if m: out.append((int(m.group(1)), None))
    return out, buf.getvalue()

def solve(ep, tl, rounds=40):
    ep = copy.deepcopy(ep); moved = {}
    for _ in range(rounds):
        F, _txt = fails(ep, tl)
        if not F: break
        changed = False
        for j, name in F:
            sc = ep['scenes'][j]; K = LC.keys(sc); R = refs(sc)
            cand = [k for k, v in K.items() if (name is None or v[0] == name) and v[1] >= 0 and k in R]
            if name is None and cand: cand = [max(cand, key=lambda k: K[k][1])]   # 장면 전체 → 마지막에 뜨는 칸
            for k in cand:
                if k[0] in ('item', 'mini') and sc.get('type') in ('facegrid', 'pstat', 'faces', 'bars'): continue   # 10/25: 이름·얼굴 칸은 이름을 부르기 전에 띄우지 않는다
                d, f = R[k]; at = d.get(f)
                if at is None: at = 0
                orig = moved.get((j, k), at)
                others = sorted(v[1] for kk, v in K.items() if kk != k and 0 <= v[1] < at)
                floor = max(0.0, (others[-1] + 0.25) if others else 0.0, int(orig) - 0.75)
                new = round(max(floor, at - 0.25), 2)
                if new < at:
                    moved.setdefault((j, k), at); d[f] = new; changed = True
        if not changed: break
    F, txt = fails(ep, tl)
    return ep, moved, txt

if __name__ == '__main__':
    ep = json.load(open(sys.argv[1], encoding='utf-8')); tl = sys.argv[2]
    ep2, moved, txt = solve(ep, tl)
    json.dump(ep2, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for (j, k), a in sorted(moved.items(), key=lambda x: x[0][0]):
        sc = ep2['scenes'][j]; d, f = refs(sc)[k]; print(f'장면 {j}: {k[0]} {k[1:]} at {a} → {d[f]}')
    print(txt.strip().splitlines()[-1] if txt.strip() else '')
    rest = [l for l in txt.splitlines() if l.startswith('X')]
    print('\n'.join(rest))
