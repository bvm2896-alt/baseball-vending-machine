# -*- coding: utf-8 -*-
"""10/15 사용자 "이미 만들어진 영상에 뒤에 더 붙여줘, 처음부터 하면 너무 오래 걸려"
롱폼⑮ 결과물 mp4(본편 + 엔딩 12초)의 맨 끝에 같은 엔딩 화면을 더 붙여 전체를 콘티 totalSec(481.4초 = 8분 1초)로 맞춘다.
다시 렌더하지 않는다: 엔딩 화면 몇 초만 같은 코덱으로 만들어 concat 복사(1분 안쪽).
원본: work\\final_out.mp4 (마지막 렌더가 결과물 폴더에 복사한 것과 같은 파일). 결과는 결과물 폴더 mp4 를 .part → 교체(드라이브 충돌 사본 방지).
실행: 야구롱폼\\8분1초맞추기.cmd  (또는 시스템 폴더에서 python -X utf8 tools\\extend_tail_1015.py)"""
import os, sys, io, json, glob, shutil, subprocess, hashlib

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE); sys.path.insert(0, HERE)
import build

EPP = os.path.join('episodes', '2026-10-15_롱폼.json')
ep = json.load(io.open(EPP, encoding='utf-8'))
TOTAL = float(ep.get('totalSec') or 481.4)

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')

def dur(f): return build.dur_of(f)

# 1) 결과물 폴더의 mp4 찾기 (오늘 날짜 폴더 → 없으면 야구롱폼\*\ 에서 같은 이름 중 최신)
out, _, _ = build.out_paths(ep, EPP)
if not os.path.exists(out):
    name = os.path.basename(out)
    cands = sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(out)), '*', name)), key=os.path.getmtime)
    if not cands: sys.exit(f'결과물 영상을 못 찾았어요: {out}')
    out = cands[-1]
print('결과물:', out, f'({dur(out):.2f}초)')

src = build.W('final_out.mp4')
if not os.path.exists(src): sys.exit('work\\final_out.mp4 가 없어요 — 롱폼만들기를 다시 돌려야 합니다')
d0 = dur(src)
if abs(d0 - dur(out)) > 0.5:
    print(f'경고: work\\final_out.mp4({d0:.2f}초)와 결과물({dur(out):.2f}초) 길이가 다릅니다 — 결과물 쪽을 원본으로 씁니다')
    src = out; d0 = dur(src)
add = TOTAL - d0
if add <= 0.05: sys.exit(f'이미 {d0:.2f}초 — {TOTAL:.1f}초 이상이라 붙일 게 없어요')
print(f'지금 {d0:.2f}초 → 엔딩 화면 {add:.2f}초 더 붙여 {TOTAL:.1f}초로')

# 2) 붙일 그림 = 영상 마지막 프레임(엔딩 화면)
png = build.W('tail_last.png')
r = sh(['ffmpeg', '-y', '-loglevel', 'error', '-sseof', '-0.3', '-i', src, '-frames:v', '1', '-update', '1', png])
if r.returncode != 0 or not os.path.exists(png): sys.exit('마지막 화면 뽑기 실패: ' + r.stderr[-300:])

# 3) 본편과 같은 코덱으로 꼬리 영상 만들기 (append_endcard 와 같은 방식)
pr = sh(['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=width,height,profile,level,pix_fmt,r_frame_rate', '-of', 'default=nw=1', src]).stdout
kv = dict(l.split('=', 1) for l in pr.strip().splitlines() if '=' in l)
w_, h_ = kv.get('width', '2560'), kv.get('height', '1440'); pix = kv.get('pix_fmt', 'yuvj420p'); lvl = kv.get('level', '51'); prof = (kv.get('profile') or 'High').lower()
fps = kv.get('r_frame_rate', '60/1').split('/'); fps = str(int(round(float(fps[0]) / float(fps[1] or 1))))
lvl = f'{int(lvl) // 10}.{int(lvl) % 10}' if lvl.isdigit() else lvl
ar = sh(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=sample_rate,channels', '-of', 'default=nw=1', src]).stdout
akv = dict(l.split('=', 1) for l in ar.strip().splitlines() if '=' in l)
rate = akv.get('sample_rate', '44100'); ch = akv.get('channels', '1')
tail = build.W('tail_extra.mp4')
r = sh(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', fps, '-i', png, '-f', 'lavfi', '-i', f'anullsrc=r={rate}:cl={"mono" if ch == "1" else "stereo"}',
        '-t', f'{add:.3f}', '-vf', f'scale={w_}:{h_},format={pix}', '-c:v', 'libx264', '-profile:v', prof, '-level', lvl, '-pix_fmt', pix, '-r', fps, '-g', str(int(fps) * 2),
        '-preset', 'medium', '-crf', '20', '-c:a', 'aac', '-b:a', '192k', '-ar', rate, '-ac', ch, '-shortest', tail])
if r.returncode != 0: sys.exit('꼬리 영상 만들기 실패: ' + r.stderr[-300:])

# 4) 이어 붙이기(재인코딩 없음) → 길이 확인
lst = build.W('tail_list.txt'); joined = build.W('final_8m01.mp4')
io.open(lst, 'w', encoding='utf-8').write("file '" + os.path.abspath(src).replace("'", "'\\''") + "'\nfile '" + os.path.abspath(tail).replace("'", "'\\''") + "'\n")
r = sh(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', joined])
d1 = dur(joined) if os.path.exists(joined) else 0
if r.returncode != 0 or abs(d1 - TOTAL) > 0.3: sys.exit(f'이어 붙이기 실패(길이 {d1:.2f}초): ' + (r.stderr or '')[-300:])

# 5) 결과물 폴더 교체 (.part 로 복사 후 한 번에 바꿈) + work\final_out.mp4 도 같은 것으로
part = out + '.part'
shutil.copyfile(joined, part); os.replace(part, out)
shutil.copyfile(joined, src) if src != out else None
m, s = divmod(dur(out), 60)
print(f'완료: {os.path.basename(out)} = {int(m)}분 {s:.2f}초')

# 6) 롱폼만들기가 이 콘티를 '다시 만들 것'으로 보지 않게 기록(콘티 rev 만 바꿨으므로)
try:
    bp = os.path.join('work', 'long_built.json')
    b = json.load(io.open(bp, encoding='utf-8')) if os.path.exists(bp) else {}
    b['최종|' + os.path.basename(EPP)] = hashlib.sha1(open(EPP, 'rb').read()).hexdigest()[:16]
    io.open(bp, 'w', encoding='utf-8').write(json.dumps(b, ensure_ascii=False, indent=1))
except Exception as e:
    print('기록 실패(무시해도 됨):', e)
