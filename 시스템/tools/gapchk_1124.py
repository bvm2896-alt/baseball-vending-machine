# 요소끼리 너무 가까운 곳 찾기(11/24 00:33 사용자 "텍스트끼리도 겹칠 것 같잖아 크기 조절 좀 잘해") — 가로로 겹치는 두 요소의 세로 틈이 MIN 보다 작으면 표시
import json, sys
MIN = 18
def WL(t): return sum(1.0 if ord(c) > 0x3000 else .32 if c == ' ' else .62 if c.isdigit() else .58 for c in str(t or ''))
def box(e):
    k = e['k']; x, y = e['x'], e['y']
    if k == 'tx':
        fz = e['fz']; w = WL(e['t']) * fz
        if e.get('w'):
            if w > e['w']: fz = max(26, int(e['w'] / max(.1, WL(e['t'])))); w = WL(e['t']) * fz
            x0 = x + (e['w'] - w) / 2 if e.get('al') == 'c' else x + e['w'] - w if e.get('al') == 'right' else x
        else: x0 = x
        if e.get('bg'): x0 -= 22; w += 44
        return (x0, y, x0 + w, y + fz * 1.12)
    if k == 'band': fz = min(e.get('fz', 52), int((e.get('w', 1680) - 60) / max(.1, WL(e['t'])))); return (x, y, x + WL(e['t']) * fz + 60, y + e.get('h', 84))
    if k == 'vb': bh = e['h'] * e['f']; tw = max(e['w'], WL(e.get('t', '')) * e.get('tf', 64), WL(e.get('l', '')) * e.get('lf', 36)); cx = x + e['w'] / 2; return (cx - tw / 2, y - bh - e.get('tf', 64) - 22, cx + tw / 2, y + (24 + e.get('lf', 36) * 1.15 if e.get('l') else 0))
    if k == 'scale': return (x, y + 46, x + e['w'], y + 150 + e.get('fz', 56) * 1.1)
    if k == 'pict': W = e['n'] * e['sz'] + (e['n'] - 1) * e.get('gap', 14); x0 = x + (e['w'] - W) / 2 if e.get('w') else x; return (x0, y, x0 + W, y + e['sz'] * 1.25)
    if k == 'logo': return (x, y, x + e['w'], y + e['w'])
    if k == 'ar': return (x, y, x + 50, y + e.get('fz', 60))
    if k == 'q': return (x, y, x + e['w'], y + e['h'] + (34 if e.get('tail') else 0))
    return (x, y, x + e.get('w', 0), y + e.get('h', 0))
def check(ep):
    bad = []
    for i, s in enumerate(ep['scenes']):
        els = s.get('els') or []
        bs = [(box(e), e) for e in els if e['at'] < 50]
        if s.get('title'): bs.append(((116, s.get('ty', 118), 116 + WL(s['title']) * 60, s.get('ty', 118) + 66), dict(k='title', t=s['title'])))
        for a in range(len(bs)):
            for b in range(a + 1, len(bs)):
                (x0, y0, x1, y1), ea = bs[a]; (u0, v0, u1, v1), eb = bs[b]
                if min(x1, u1) - max(x0, u0) <= 6: continue
                gap = max(v0 - y1, y0 - v1)
                inside = (x0 >= u0 - 2 and x1 <= u1 + 2 and y0 >= v0 - 2 and y1 <= v1 + 2) or (u0 >= x0 - 2 and u1 <= x1 + 2 and v0 >= y0 - 2 and v1 <= y1 + 2)
                if {ea['k'], eb['k']} == {'hb'} or ('ar' in (ea['k'], eb['k'])): continue
                if ea['k'] == eb['k'] == 'ph' and (x0, y0, x1, y1) == (u0, v0, u1, v1): continue   # 공개 전 실루엣 액자 위에 사진이 뜨는 자리
                if gap < MIN and not (inside and {ea['k'], eb['k']} & {'tile', 'field'}):
                    bad.append((i + 1, round(gap), ea['k'], (ea.get('t') or ea.get('v') or ea.get('vz') or ea.get('l') or '')[:14], eb['k'], (eb.get('t') or eb.get('v') or eb.get('vz') or eb.get('l') or '')[:14]))
    return bad
if __name__ == '__main__':
    ep = json.load(open(sys.argv[1], encoding='utf-8')); bad = check(ep); seen = set()
    for b in bad:
        key = b[1:]
        if key in seen: continue
        seen.add(key); print('줄 %d  틈 %dpx  %s[%s] ↔ %s[%s]' % b)
    print('너무 가까운 곳', len(seen))
