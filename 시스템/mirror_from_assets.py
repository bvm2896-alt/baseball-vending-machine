#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""(1회용) 이 PC 의 사진 폴더를 깃허브 assets 사본과 똑같이 맞춘다 — 깃구조변경.cmd 를 돌리기 전에.
  시스템\assets\선수이미지\   →  야구자판기\선수이미지\          (assets 에 없는 파일은 지움 = 다른 PC 에서 지운 것)
  시스템\assets\이슈사진\     →  야구자판기\야구이슈\재료\사진\  (같음)
  시스템\assets\음성\<시리즈>\ →  야구자판기\<시리즈>\음성\       (복사만, 지우지 않음)
먼저 `git checkout -- assets` 로 assets 를 깃허브 상태로 되돌린다(옛 sync_assets 가 지웠을 수 있어서).
"""
import os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
A = os.path.join(HERE, 'assets')
EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.txt', '.zip')
if os.path.isdir(os.path.join(ROOT, '.git')):
    print('저장소 루트가 이미 야구자판기\\ 입니다 — 이 단계는 필요 없어요'); sys.exit(0)
subprocess.run(['git', 'checkout', '-q', '--', 'assets'], cwd=HERE)
def files(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.lower().endswith(EXTS): out[os.path.relpath(os.path.join(dp, f), root)] = os.path.join(dp, f)
    return out
def mirror(src, dst, delete):
    if not os.path.isdir(src): print(f'  (없음) {src}'); return
    os.makedirs(dst, exist_ok=True)
    fs, fd = files(src), files(dst); n = m = 0
    for rel, p in fs.items():
        q = os.path.join(dst, rel); os.makedirs(os.path.dirname(q), exist_ok=True)
        if rel not in fd or abs(os.path.getmtime(p) - os.path.getmtime(q)) > 1 or os.path.getsize(p) != os.path.getsize(q):
            shutil.copy2(p, q); n += 1
    if delete:
        for rel, q in fd.items():
            if rel not in fs:
                os.remove(q); m += 1
                d = os.path.dirname(q)
                while os.path.abspath(d) != os.path.abspath(dst):
                    try: os.rmdir(d)
                    except OSError: break
                    d = os.path.dirname(d)
    print(f'  {os.path.relpath(dst, ROOT)}: 복사 {n}개, 삭제 {m}개')
print('깃허브 assets 기준으로 사진·음성 폴더 맞추는 중...')
mirror(os.path.join(A, '선수이미지'), os.path.join(ROOT, '선수이미지'), True)
mirror(os.path.join(A, '이슈사진'), os.path.join(ROOT, '야구이슈', '재료', '사진'), True)
for s in ('야구이슈', '야구순위'):
    mirror(os.path.join(A, '음성', s), os.path.join(ROOT, s, '음성'), False)
print('완료. 이제 깃구조변경.cmd 를 실행하세요.')
