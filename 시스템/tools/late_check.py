# -*- coding: utf-8 -*-
"""늦게 뜨는 글·카드 검사 (10/23 사용자: "마무리 훈련부터 잘 준비 카드가 너무 늦게 떠서 나오자마자 다음 장면으로 넘어가. 이런 거 안 나오게").
장면 안 요소의 at(= 호흡 구간 번호 + 비율, 템플릿 brP 와 같은 뜻)를 실제 음성 길이로 초로 바꿔,
'뜬 뒤 화면에 남는 시간'이 MIN_SHOW 초보다 짧으면 실패로 낸다. 다음 장면이 같은 묶음(chain + cont)이면 그 장면 길이까지 더한다.
사용: python tools/late_check.py episodes/<콘티>.json [음성 zip(타입캐스트 문장별)]   (zip 없으면 글자 수로 길이를 어림)
- 요소: stats[].at, viz steps items[].at, viz stamp.at, bubbles[].at, items[].at, textAt
- 호흡 구간 시작 시각은 음절 수 비례(+1)로 어림한다(tts.py seg_bounds 의 쉼 없는 경계와 같은 방식)."""
import sys, json, re, zipfile, io, os, subprocess, tempfile
MIN_SHOW = 1.5      # 뜬 뒤 최소 이만큼(초)은 보여야 한다 — 글 한 줄 읽는 시간
SPS = 0.12          # zip 없을 때 음절당 초(1.3배속 어림)

def syl(t): return len(re.findall(r'[가-힣A-Za-z0-9]', t))

def durs_from_zip(zp, n):
    out = {}
    with zipfile.ZipFile(zp) as z:
        for nm in z.namelist():
            m = re.match(r'audio_(\d+)_', os.path.basename(nm))
            if not m: continue
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f: f.write(z.read(nm)); p = f.name
            r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
            os.unlink(p)
            try: out[int(m.group(1))] = float(r.stdout.strip())
            except ValueError: pass
    return [out.get(i) for i in range(n)]

def ats(sc):
    """(이름, at) 목록"""
    r = []
    for k, s in enumerate(sc.get('stats') or []):
        if s.get('at') is not None: r.append((f"stat '{s.get('k')}: {s.get('v')}'", s['at']))
    for v in sc.get('viz') or []:
        if v.get('type') == 'steps':
            for s in v.get('items') or []:
                if s.get('at') is not None and s['at'] >= 0: r.append((f"step '{s.get('d')} {s.get('t')}'", s['at']))
        elif v.get('at') is not None: r.append((f"{v.get('type')} '{v.get('t', '')}'", v['at']))
    for b in sc.get('bubbles') or []:
        if b.get('at') is not None: r.append((f"bubble '{b.get('text')}'", b['at']))
    for it in sc.get('items') or []:
        if it.get('at') is not None: r.append((f"item '{it.get('name') or it.get('label') or it.get('v') or it.get('k')}'", it['at']))
    if sc.get('text') and sc.get('textAt') is not None: r.append((f"text '{sc['text']}'", sc['textAt']))
    return [(a, b) for a, b in r if b < 50]

def main(ep_path, zp=None):
    ep = json.load(open(ep_path, encoding='utf-8'))
    lines, scenes = ep['lines'], ep['scenes']
    N = len(scenes)
    D = durs_from_zip(zp, N) if zp else [None] * N
    gap = [float(l.get('gapAfter') or 0.25) for l in lines]
    bad = 0
    for j, sc in enumerate(scenes):
        segs = lines[j]['narr'].split(' / ')
        dur = D[j] or sum(syl(s) for s in segs) * SPS
        w = [syl(s) + 1 for s in segs]; W = sum(w)
        starts = [dur * sum(w[:k]) / W for k in range(len(segs))]
        # 같은 묶음으로 이어지는 다음 장면들 길이(요소가 그대로 남는다)
        extra, k2 = 0.0, j + 1
        while k2 < N and sc.get('chain') and scenes[k2].get('chain') == sc.get('chain') and scenes[k2].get('cont'):
            extra += (D[k2] or sum(syl(s) for s in lines[k2]['narr'].split(' / ')) * SPS) + gap[k2 - 1]; k2 += 1
        for name, at in ats(sc):
            i, f = int(at), at - int(at)
            if i >= len(segs):
                t = starts[-1] + 1.5 * (at - (len(segs) - 1))
                note = f'구간 {i}번이 없음(이 줄은 {len(segs)}구간)'
            else:
                t1 = starts[i + 1] if i + 1 < len(segs) else dur
                t = starts[i] + (t1 - starts[i]) * f; note = ''
            show = dur + gap[j] + extra - t
            if show < MIN_SHOW:
                bad += 1
                print(f'X 줄 {j:2d} · {name} · at {at} → {t:.1f}초에 뜸 · 화면에 {show:.1f}초만 남음 (줄 {dur:.1f}초) {note}')
                print(f'      대사: {lines[j]["narr"]}')
    # 10/23 사용자("이 장면도 너무 금방 지나가"): 장면 전체가 새 글을 읽을 시간보다 짧으면 실패 — 새 글 14자당 1초, 최소 2초
    for j, sc in enumerate(scenes):
        if sc.get('cont') and j and scenes[j - 1].get('chain') == sc.get('chain'): continue
        k2, tot = j, 0.0
        while True:
            segs_ = lines[k2]['narr'].split(' / ')
            tot += (D[k2] or sum(syl(x) for x in segs_) * SPS) + gap[k2]; k2 += 1
            if not (k2 < N and sc.get('chain') and scenes[k2].get('chain') == sc.get('chain') and scenes[k2].get('cont')): break
        txt = ''.join(n for k in range(j, k2) for n, _ in ats(scenes[k]))
        need = max(2.0, len(re.findall(r'[가-힣A-Za-z0-9]', txt)) / 14)
        if sc.get('type') in ('pstat', 'tiles', 'bars', 'speech') and tot < need:
            bad += 1
            print(f'X 줄 {j:2d}~{k2 - 1} · 장면이 {tot:.1f}초뿐 — 새 글 읽는 데 {need:.1f}초 필요 · 대사: {lines[j]["narr"]}')
    print(f'늦게 뜨는 요소 {bad}개' if bad else '늦게 뜨는 요소 없음 (모두 {:.1f}초 이상 보임)'.format(MIN_SHOW))
    return bad

if __name__ == '__main__':
    sys.exit(1 if main(*sys.argv[1:3]) else 0)
