# -*- coding: utf-8 -*-
"""11/8 사용자 "자료 영상이 들어가면 좋겠다 · 그 장면을 실제 영상으로": 롱폼 영상 장면(bt_clip) 덮기.
렌더가 끝난 무음 영상(silent.mp4)에서 bt_clip 장면마다 템플릿이 비워 둔 자리(#clipbox)를 재고,
그 자리에 경기 영상을 소리 없이(무음) 둥근 모서리로 덮는다. 같은 클립이 이어지는 장면은 영상이 끊기지 않고 이어서 재생된다.
콘티 장면 값: clip(이름) · clipFile(선수이미지\\영상\\ 안 파일) · clipCuts([[시작, 끝], ...] 이어 붙일 구간) · clipHide([[x, y, w, h], ...] 흐리게 가릴 자리 — 대사에 없는 중계 점수판)
"""
import json, os, subprocess, io

def _run(cmd, what):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0: raise SystemExit(f'영상 덮기 실패({what}):\n' + (r.stderr or r.stdout or '')[-1200:])
    return r

def groups(ep, bounds, total):
    G = []
    for k, s in enumerate(ep.get('scenes', [])):
        if s.get('type') != 'bt_clip': continue
        a = bounds[k - 1] if k > 0 else 0.0
        b = bounds[k] if k < len(bounds) else total
        if G and G[-1]['clip'] == s.get('clip') and G[-1]['k'][-1] == k - 1:
            G[-1]['k'].append(k); G[-1]['win'].append([a, b])
        else:
            G.append(dict(clip=s.get('clip'), file=s.get('clipFile'), cuts=s.get('clipCuts') or [[float(s.get('clipFrom') or 0), None]],
                          hide=s.get('clipHide') or [], k=[k], win=[[a, b]]))
    return G

def apply(ep, EP, W, clip_dir, fps, sw, cw, ch, fenv, silent=None, t_shift=0.0, only=None):
    """W = 작업 폴더 함수(build.W). silent 기본 W('silent.mp4'). t_shift/only 는 시험용(구간만 렌더한 영상)."""
    silent = silent or W('silent.mp4'); total = float(EP.get('total') or 0); bounds = EP.get('bounds') or []
    G = groups(ep, bounds, total)
    if only: G = [g for g in G if g['clip'] in only]
    if not G: return
    cdir = W('clips'); os.makedirs(cdir, exist_ok=True)
    # 1) 자리 재기(장면마다 한 번, 들어오는 움직임이 끝난 뒤)
    times = [min(b - 0.15, a + 1.2) for g in G for a, b in g['win']]
    tf, of = os.path.join(cdir, 'times.json'), os.path.join(cdir, 'rects.json')
    json.dump(times, io.open(tf, 'w', encoding='utf-8'))
    here = os.path.dirname(os.path.abspath(__file__))
    _run(['node', os.path.join(here, 'clip_rects.js'), W('render.html'), tf, of], '자리 재기')
    rects = json.load(io.open(of, encoding='utf-8'))
    # 2) 클립 손질(구간 이어 붙이기 · 점수판 흐리게 · 길이 맞춤 — 끝나면 마지막 화면 멈춤)
    ins, fc, n_in, ri, made = ['-i', silent], [], 1, 0, 0
    last = '0:v'
    for gi, g in enumerate(G):
        src = os.path.join(clip_dir, g['file'] or '')
        glen = g['win'][-1][1] - g['win'][0][0] + 1.0
        if not os.path.exists(src):
            print(f"  경고: 경기 영상 없음 → 그 자리는 첫 화면 사진으로 남음: {src}"); ri += len(g['win']); continue
        gf = os.path.join(cdir, f'grp{gi:02d}.mp4')
        f = []
        for i, (a, b) in enumerate(g['cuts']):
            f.append(f"[0:v]trim=start={a}" + (f":end={b}" if b else '') + f",setpts=PTS-STARTPTS[c{i}]")
        f.append(''.join(f'[c{i}]' for i in range(len(g['cuts']))) + f"concat=n={len(g['cuts'])}:v=1:a=0[v0]")
        cur = 'v0'
        for j, (x, y, w, h) in enumerate(g['hide']):
            f.append(f"[{cur}]split[h{j}a][h{j}b];[h{j}b]crop={w}:{h}:{x}:{y},boxblur={max(4, min(w, h) // 6)}:2[h{j}c];[h{j}a][h{j}c]overlay={x}:{y}[h{j}]"); cur = f'h{j}'
        f.append(f"[{cur}]fps={fps},tpad=stop_mode=clone:stop_duration={glen + 2:.2f},trim=duration={glen:.2f},setpts=PTS-STARTPTS[out]")
        _run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-filter_complex', ';'.join(f), '-map', '[out]', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', gf], f"클립 손질 {g['clip']}")
        # 3) 장면마다 그 자리에 덮기(같은 클립이면 이어서 재생)
        for wi, (a, b) in enumerate(g['win']):
            r = rects[ri]; ri += 1
            if not r: print(f"  경고: {g['clip']} 장면 자리를 못 찾음({a:.2f}초)"); continue
            x, y, w, h = [int(round(v * sw)) for v in r[:4]]; w -= w % 2; h -= h % 2
            mk = os.path.join(cdir, f'mask_{w}x{h}.png')
            if not os.path.exists(mk):
                R = int(round(18 * sw))
                _run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', f'color=c=white:s={w}x{h}', '-frames:v', '1', '-vf',
                      f"format=gray,geq=lum='255*lte(hypot(max(0\\,abs(X-(W-1)/2)-(W/2-{R}))\\,max(0\\,abs(Y-(H-1)/2)-(H/2-{R})))\\,{R})'", mk], '모서리 틀')
            off = a - g['win'][0][0]
            ins += ['-ss', f'{off:.3f}', '-i', gf, '-loop', '1', '-i', mk]; vi, mi = n_in, n_in + 1; n_in += 2
            ta, tb = a - t_shift, b - t_shift
            last_w = wi == len(g['win']) - 1
            fade = (',fade=in:st=0:d=0.35:alpha=1' if wi == 0 else '') + (f',fade=out:st={tb - ta:.3f}:d=0.12:alpha=1' if last_w else '')
            if last_w: tb += 0.12   # 11/8 검수: 장면이 빠지는 0.1초 동안 액자 첫 화면(포스터)이 비쳐 '되감김'처럼 보임 → 영상이 같이 빠지게
            fc.append(f"[{vi}:v]scale={w}:{h},format=yuva420p[s{made}];[{mi}:v]scale={w}:{h},format=gray[m{made}];[s{made}][m{made}]alphamerge{fade},setpts=PTS-STARTPTS+{max(0, ta):.3f}/TB[o{made}];"
                      f"[{last}][o{made}]overlay={x}:{y}:enable='between(t,{ta:.3f},{tb:.3f})':eof_action=pass[b{made}]")
            last = f'b{made}'; made += 1
    if not made: return
    out = W('silent_clip.mp4')
    _run(['ffmpeg', '-y', '-v', 'error'] + ins + ['-filter_complex', ';'.join(fc), '-map', f'[{last}]', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16',
          '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', str(fps), '-movflags', '+faststart', out], '덮기')
    os.replace(out, silent)
    print(f'경기 영상 덮기 완료: 장면 {made}개 ({", ".join(g["clip"] for g in G)})')
