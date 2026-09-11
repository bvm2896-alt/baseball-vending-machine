#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
사진 폴더 ↔ 깃 저장소 동기화.  python -X utf8 sync_assets.py
깃 저장소는 시스템\ 이라 그 밖의 사진 폴더(야구자판기\선수이미지\, 야구이슈\재료\사진\)는 깃허브에 안 올라간다.
그래서 시스템\assets\ 안에 사본을 두고 깃으로 주고받는다.
  야구자판기\선수이미지\            <->  시스템\assets\선수이미지\
  야구자판기\야구이슈\재료\사진\    <->  시스템\assets\이슈사진\
양방향, 새 파일·더 최신 파일이 이기고, 삭제는 옮기지 않는다(한쪽에서 지워도 다른 쪽엔 남음 — 실수 방지).
깃저장.cmd 는 커밋 전에, 지금실행.cmd / run_daily 는 pull 뒤에 이 스크립트를 부른다.
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.txt')
PAIRS = [
    (os.path.join(ROOT, '선수이미지'), os.path.join(HERE, 'assets', '선수이미지')),
    (os.path.join(ROOT, '야구이슈', '재료', '사진'), os.path.join(HERE, 'assets', '이슈사진')),
]

def _files(root):
    out = {}
    if not os.path.isdir(root): return out
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.lower().endswith(EXTS):
                p = os.path.join(dp, f)
                out[os.path.relpath(p, root)] = os.path.getmtime(p)
    return out

def _copy(src_root, dst_root, rel):
    s, d = os.path.join(src_root, rel), os.path.join(dst_root, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)

def sync_pair(a, b):
    fa, fb = _files(a), _files(b)
    n = 0
    for rel, t in fa.items():
        if rel not in fb or t > fb[rel] + 1: _copy(a, b, rel); n += 1
    for rel, t in fb.items():
        if rel not in fa or t > fa[rel] + 1: _copy(b, a, rel); n += 1
    return n

def main():
    total = 0
    for a, b in PAIRS:
        if not os.path.isdir(a) and not os.path.isdir(b): continue
        os.makedirs(a, exist_ok=True); os.makedirs(b, exist_ok=True)
        n = sync_pair(a, b); total += n
        if n: print(f'사진 동기화 {n}개: {os.path.basename(a)}')
    if total == 0: print('사진 동기화: 바뀐 것 없음')
    return total

if __name__ == '__main__':
    try: main()
    except Exception as e:
        print('사진 동기화 실패:', e); sys.exit(0)   # 동기화 실패로 제작이 멈추지 않게
