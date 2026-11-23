# 칸 안 글이 칸에 맞는지(11/24) — 칸(tile)·말 카드(q) 안에서 글이 넘치거나, 작은 글과 큰 글이 겹치거나, 글자가 너무 작아진 곳 찾기. 템플릿 sb_pan 의 계산을 그대로 옮김
import json, io, sys, math
from gapchk import WL
def FIT(t, base, w, mn=26): return max(mn, min(base, int(w * .93 / max(.1, WL(t)))))
def check(ep):
    bad = []
    for i, s in enumerate(ep['scenes']):
        for e in s.get('els') or []:
            k = e['k']
            if k == 'tile':
                v = e.get('v') if e.get('v') is not None else e.get('vz', ''); pad = e.get('pad', 30); iw = e['w'] - pad * 2
                lf = FIT(e['l'], e.get('lf') or 34, iw, 22) if e.get('l') else 0; vf = FIT(v, e.get('fz') or 76, iw, 30); th = lf + (round(lf * .35) if e.get('l') else 0) + vf * 1.08
                if (e['h'] - th) / 2 < 14: bad.append((i + 1, 'tile 넘침', v[:16], 'h', e['h'], '글', round(th)))
                if vf < 44: bad.append((i + 1, 'tile 글 작음', v[:16], vf))
                if WL(v) * vf > iw: bad.append((i + 1, 'tile 폭 넘침', v[:16], vf))
            elif k == 'q':
                iw = e['w'] - 56; fz0 = e.get('fz') or 46; one = WL(e['t']) * fz0 <= iw; fz = fz0 if one else max(30, min(fz0, int(iw * 2 / (WL(e['t']) + 1.5))))
                lines = 1 if one else max(2, math.ceil(WL(e['t']) * fz / iw)); room = e['h'] - ((max(46, (e.get('lf') or 28) + 19) + 10) if e.get('l') else 0)
                if lines * fz * 1.18 > room - 6: bad.append((i + 1, 'q 넘침', e['t'][:16], 'h', e['h'], '줄', lines, 'fz', fz, '필요', round(lines * fz * 1.18 + ((max(46, (e.get('lf') or 28) + 19) + 10) if e.get('l') else 0) + 6)))
                if fz < 36: bad.append((i + 1, 'q 글 작음', e['t'][:16], fz))
            elif k == 'tx' and e.get('w'):
                f = FIT(e['t'], e['fz'], e['w'], 26)
                if f < 30: bad.append((i + 1, 'tx 글 작음', e['t'][:16], f))
            elif k == 'band':
                f = FIT(e['t'], e.get('fz') or 52, (e.get('w') or 1680) - 60, 30)
                if f * 1.25 > (e.get('h') or 84): bad.append((i + 1, 'band 넘침', e['t'][:16], f, e.get('h')))
            elif k == 'hd':
                lw = min(e['h'] - 24, 110); f = FIT(e['t'], e.get('fz') or 48, e['w'] - lw - 70, 28)
                if f < 34: bad.append((i + 1, 'hd 글 작음', e['t'][:16], f))
    return bad
if __name__ == '__main__':
    ep = json.load(io.open(sys.argv[1], encoding='utf-8')); bad = check(ep); seen = set()
    for b in bad:
        key = b[1:]
        if key in seen: continue
        seen.add(key); print(b)
    print('칸 안 글 문제', len(seen))
