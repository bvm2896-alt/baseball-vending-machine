# 두 줄 자막과 판 아래 요소가 붙는 곳 찾기(11/24) — 두 줄 자막 위 끝 y885, 한 줄 y958. 가로로 겹치고 세로 틈이 MIN 보다 작으면 표시
import json, io, sys
import gapchk
MIN = 36; TOP2 = 885; TOP1 = 958
def check(ep):
    bad = []
    for i, (ln, s) in enumerate(zip(ep['lines'], ep['scenes'])):
        els = s.get('els') or []
        for c, ch in enumerate(ln['sub'].split('|')):
            rows = ch.split('\n'); w = max(gapchk.WL(r) for r in rows) * 47 + 44; x0, x1 = 960 - w / 2, 960 + w / 2; top = TOP2 if len(rows) > 1 else TOP1
            for e in els:
                if e['at'] > c: continue
                b = gapchk.box(e)
                if e['k'] in ('tile', 'q', 'hd', 'cal'): b = (b[0], b[1], b[2], b[3] + 6)   # 지금 줄 표시(금색 테 6px)는 칸 밖으로 나온다
                if min(b[2], x1) - max(b[0], x0) <= 0: continue
                if top - b[3] < MIN: bad.append((i + 1, c, round(top - b[3]), e['k'], (e.get('t') or e.get('v') or e.get('l') or '')[:16], ch.replace('\n', '/')))
    return bad
if __name__ == '__main__':
    ep = json.load(io.open(sys.argv[1], encoding='utf-8')); bad = check(ep)
    for b in bad: print(b)
    print('자막과 가까운 곳', len(bad))
    # 판마다 필요한 줄임 비율
    need = {}
    for b in bad: 
        key = (ep['scenes'][b[0] - 1].get('bk') or ep['scenes'][b[0] - 1].get('key')); need[key] = max(need.get(key, 0), MIN - b[2])
    for key, d in need.items():
        ys = [gapchk.box(e) for s in ep['scenes'] if (s.get('bk') or s.get('key')) == key for e in s.get('els') or []]
        top = min(e['y'] for s in ep['scenes'] if (s.get('bk') or s.get('key')) == key for e in s.get('els') or [] if e['k'] != 'vb'); bot = max(b[3] for b in ys)
        print(key, 'top', top, 'bot', round(bot), 'need', d, 'k', round((bot - d - top) / (bot - top), 3))
