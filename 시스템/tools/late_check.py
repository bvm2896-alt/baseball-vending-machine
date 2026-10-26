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
    return [(a, b) for a, b in r if 0 <= b < 50]   # 10/24: at < 0 = 앞 장면에서 이미 보이던 것(템플릿 bp·P 가 1로 처리) → 늦게 뜨는 게 아니다

def main(ep_path, zp=None):
    ep = json.load(open(ep_path, encoding='utf-8'))
    lines, scenes = ep['lines'], ep['scenes']
    N = len(scenes)
    vf = (ep.get('voiceFrom') or {}).get('lines')
    if zp and vf:   # 컷 쇼츠: 롱폼 음성 zip 을 주면 voiceFrom 줄 번호로 길이를 가져온다(새 줄은 어림)
        LD = durs_from_zip(zp, max(x for x in vf if x is not None) + 1); D = [LD[x] if x is not None else None for x in vf]
    else: D = durs_from_zip(zp, N) if zp else [None] * N
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
    # 10/23 밤 실수 학습: 타입캐스트 화면의 전체 길이(문장 사이 빈 시간 포함)를 믿고 8분이 넘는다고 했다가 실제 6분 35초. → 롱폼은 음성 파일 길이 합으로 영상 길이를 어림해 8분 미만이면 막는다
    if zp and not ep.get('vertical') and all(x is not None for x in D[:len(lines) - 1]):
        est = sum(x for x in D if x) + float(ep.get('endcardSec') or 10) + 3
        mm = f'{int(est // 60)}분 {int(est % 60)}초'
        if est < 460:
            bad += 1; print(f'X 영상 길이 어림 {mm} — 롱폼 8분(480초)에 {480 - est:.0f}초 모자람. 대사를 늘리거나(근거 확정 사실) 콘티를 다시 짠다')
        elif est < 480: print(f'! 영상 길이 어림 {mm} — 8분에 살짝 모자람. 엔딩을 늘려 8분에 맞춘다(10/17 규칙)')
        else: print(f'영상 길이 어림 {mm} (8분 이상)')
    print(f'늦게 뜨는 요소 {bad}개' if bad else '늦게 뜨는 요소 없음 (모두 {:.1f}초 이상 보임)'.format(MIN_SHOW))
    return bad

# 10/25 사용자(롱폼㉙ 원태인 "이 장면 너무 금방 지나가서 다 읽기도 전에 다음 화면으로 넘어가" / "여기도 마찬가지야"):
# 같은 묶음이라도 다음 장면이 내용을 바꾸면 그 글은 거기서 사라진다 — 묶음 전체 길이를 더하던 계산이 이걸 놓쳤다.
# → 빌드가 남긴 work\timeline.json(실제 줄 시작·호흡 시각)으로, 글마다 '뜬 시각 → 그 글이 없는 장면이 들어오는 시각'을 잰다.
#   글 하나는 최소 MIN_READ 초(+ 14자당 1초 넘으면 그만큼) 보여야 한다. 장면 enterAt(앞 장면을 그 호흡까지 유지)도 계산한다.
MIN_READ = 2.5   # 10/25 2차 사용자("너무 읽을 시간이 짧아.. 시각 자료도 읽을 시간을 충분히 — 나레이션을 멈추라는 건 아니야"): 2.0 → 2.5, 글자 10자당 1초 + 1초
SCENE_CPS = 9    # 장면 전체(표·여러 칸)는 마지막 칸이 뜬 뒤 '장면 글 전체 ÷ 9자/초' 만큼 더 보여야
def keys(sc):
    """장면에 보이는(at<50) 글 → {열쇠: (이름, at, 글자)}"""
    r = {}
    def put(k, name, at, txt):
        if at is None: at = 0
        if at < 50: r[k] = (name, at, txt)
    for s in sc.get('stats') or []: put(('stat', s.get('k'), s.get('v')), f"stat '{s.get('k')}: {s.get('v')}'", s.get('at'), f"{s.get('k')}{s.get('v')}")
    for v in sc.get('viz') or []:
        t = v.get('type')
        if t in ('steps', 'seasons', 'mini', 'hops'):
            for x in v.get('items') or []:
                lab = x.get('name') or x.get('t') or ''
                put((t, x.get('d'), lab), f"{t} '{(x.get('d') or '') + ' ' + lab}'", x.get('at'), f"{x.get('d') or ''}{lab}{x.get('k') or ''}")
        elif t == 'quote': put(('quote', v.get('text')), f"quote '{v.get('text')}'", v.get('at'), f"{v.get('date') or ''}{v.get('text')}")
        elif t in ('stamp', 'note'): put((t, v.get('t')), f"{t} '{v.get('t')}'", v.get('at'), v.get('t') or '')
    for b in sc.get('bubbles') or []: put(('bubble', b.get('text')), f"bubble '{b.get('text')}'", b.get('at'), b.get('text') or '')
    for it in sc.get('items') or []:
        lab = it.get('name') or it.get('label') or it.get('v') or it.get('k')
        put(('item', lab, it.get('note') or it.get('k')), f"item '{lab}'", it.get('at'), f"{lab}{it.get('note') or ''}")
    if sc.get('text'): put(('text', sc['text']), f"text '{sc['text']}'", sc.get('textAt'), sc['text'])
    return r

def tl_check(ep_path, tl_path):
    ep = json.load(open(ep_path, encoding='utf-8')); tl = json.load(open(tl_path, encoding='utf-8'))
    sc, segT, starts, durs = ep['scenes'], tl['segT'], tl['starts'], tl['durs']
    N = len(sc)
    def tat(j, at):   # 줄 j 의 at 호흡 → 초
        sg = segT[j] if j < len(segT) else [starts[j]]
        end = starts[j] + durs[j]
        i = int(max(0, at)); f = max(0, at) - i
        if i >= len(sg): return end
        a1 = sg[i + 1] if i + 1 < len(sg) else end
        return sg[i] + (a1 - sg[i]) * f
    enter = [starts[j] if (sc[j].get('enterAt') is None or j == 0) else tat(j, sc[j]['enterAt']) for j in range(N)]
    bad = 0
    for j in range(N):
        K = keys(sc[j])
        for k, (name, at, txt) in K.items():
            if at < 0 and j: continue                       # 앞 장면에서 이어받은 글
            t0 = max(enter[j], tat(j, at))
            j2 = j + 1
            while j2 < N and sc[j2].get('chain') and sc[j2].get('chain') == sc[j].get('chain') and k in keys(sc[j2]): j2 += 1
            t1 = enter[j2] if j2 < N else tl['total']
            need = max(MIN_READ, len(re.findall(r'[가-힣A-Za-z0-9]', txt)) / 10 + 1.0)
            if t1 - t0 < need:
                bad += 1
                print(f'X 줄 {j:3d} · {name} · {t0:.1f}초에 떠서 {t1 - t0:.1f}초만 보임(필요 {need:.1f}초) · 대사: {ep["lines"][j]["narr"]}')
    # 장면 전체: 장면이 다 그려진 뒤(마지막 칸이 뜬 뒤) 장면 글 전체를 읽을 시간
    for j in range(N):
        K = {k: v for k, v in keys(sc[j]).items() if v[1] >= 0 or j == 0}   # 이 장면에서 새로 뜬 칸만(앞 장면에서 이어받은 칸은 이미 읽었다)
        if len(K) < 3: continue
        txt = ''.join(v[2] for v in K.values()); last = max(max(enter[j], tat(j, v[1])) for v in K.values())
        j2 = j + 1
        while j2 < N and sc[j2].get('chain') and sc[j2].get('chain') == sc[j].get('chain') and all(k in keys(sc[j2]) for k in K): j2 += 1
        t1 = enter[j2] if j2 < N else tl['total']
        need = max(MIN_READ, len(re.findall(r'[가-힣A-Za-z0-9]', txt)) / SCENE_CPS * 0.5)
        if t1 - last < need:
            bad += 1; print(f'X 장면 {j:3d} 전체({len(K)}칸) · 다 그려진 뒤 {t1 - last:.1f}초만 보임(필요 {need:.1f}초) · 대사: {ep["lines"][j]["narr"]}')
    print(f'금방 지나가는 글 {bad}개' if bad else f'금방 지나가는 글 없음 (모두 {MIN_READ}초 이상)')
    return bad

if __name__ == '__main__':
    if len(sys.argv) > 3 and sys.argv[2] == '--timeline': sys.exit(1 if tl_check(sys.argv[1], sys.argv[3]) else 0)
    sys.exit(1 if main(*sys.argv[1:3]) else 0)
