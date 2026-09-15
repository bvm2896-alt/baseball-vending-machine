#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
사진 폴더 ↔ 깃 저장소 동기화.  python -X utf8 sync_assets.py
깃 저장소는 시스템\ 이라 그 밖의 사진 폴더(야구자판기\선수이미지\, 야구이슈\재료\사진\)는 깃허브에 안 올라간다.
그래서 시스템\assets\ 안에 사본을 두고 깃으로 주고받는다.
  야구자판기\선수이미지\            <->  시스템\assets\선수이미지\
  야구자판기\야구이슈\재료\사진\    <->  시스템\assets\이슈사진\
  야구자판기\야구이슈\음성\*.zip    <->  시스템\assets\음성\야구이슈\   (9/15 음성 zip 도 깃으로)
  야구자판기\야구순위\음성\*.zip    <->  시스템\assets\음성\야구순위\
양방향, 새 파일·더 최신 파일이 이긴다.
삭제: 지난번 동기화 때 양쪽에 다 있던 파일(work\sync_assets.json 에 기록)이 한쪽에서 사라지면 → 다른 쪽도 지운다.
      (예전엔 삭제를 안 옮겨서, 선수이미지\ 에서 지워도 assets\ 사본이 계속 되살아났다)
깃저장.cmd 는 커밋 전에, 지금실행.cmd / run_daily 는 pull 뒤에 이 스크립트를 부른다.
"""
import os, shutil, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
EXTS = ('.jpg', '.jpeg', '.png', '.webp', '.txt')
VOICE_EXTS = ('.zip',)   # 타입캐스트 음성 zip (mp3 는 .gitignore 라 zip 만 — 9/15: 회사·집 PC 사이에 음성도 깃으로 옮긴다)
PAIRS = [
    (os.path.join(ROOT, '선수이미지'), os.path.join(HERE, 'assets', '선수이미지'), EXTS),
    (os.path.join(ROOT, '야구이슈', '재료', '사진'), os.path.join(HERE, 'assets', '이슈사진'), EXTS),
    (os.path.join(ROOT, '야구이슈', '음성'), os.path.join(HERE, 'assets', '음성', '야구이슈'), VOICE_EXTS),
    (os.path.join(ROOT, '야구순위', '음성'), os.path.join(HERE, 'assets', '음성', '야구순위'), VOICE_EXTS),
]
SEEN_PATH = os.path.join(HERE, 'work', 'sync_assets.json')   # 지난 동기화 때 양쪽에 있던 파일 목록 (쌍 이름별)

def _files(root, exts=EXTS):
    out = {}
    if not os.path.isdir(root): return out
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.lower().endswith(exts):
                p = os.path.join(dp, f)
                out[os.path.relpath(p, root)] = os.path.getmtime(p)
    return out

def _copy(src_root, dst_root, rel):
    s, d = os.path.join(src_root, rel), os.path.join(dst_root, rel)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(s, d)

def _remove(root, rel):
    p = os.path.join(root, rel)
    try: os.remove(p)
    except FileNotFoundError: return
    d = os.path.dirname(p)   # 비게 된 하위 폴더는 정리 (루트는 남김)
    while d and os.path.abspath(d) != os.path.abspath(root):
        try: os.rmdir(d)
        except OSError: break
        d = os.path.dirname(d)

def _load_seen():
    try: return json.load(open(SEEN_PATH, encoding='utf-8'))
    except Exception: return {}

def _save_seen(seen):
    try:
        os.makedirs(os.path.dirname(SEEN_PATH), exist_ok=True)
        json.dump(seen, open(SEEN_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    except Exception: pass

def sync_pair(a, b, seen, first=False, exts=EXTS):
    """seen: 지난번 동기화 뒤 양쪽에 있던 rel 목록. 반환 (복사 수, 삭제 수, 이번에 양쪽에 남은 rel 목록)
       first: 기록이 아직 없는 첫 실행 → 바깥 폴더(a)를 기준으로 보고, assets(b)에만 있는 파일은 되살리지 않고 지운다"""
    fa, fb = _files(a, exts), _files(b, exts)
    n = m = 0
    if first:
        for rel in sorted(set(fb) - set(fa)): _remove(b, rel); fb.pop(rel, None); m += 1
    for rel in sorted(set(seen)):
        if rel in fa and rel not in fb: _remove(a, rel); fa.pop(rel, None); m += 1   # assets 쪽에서 지움 → 바깥도 지움
        elif rel in fb and rel not in fa: _remove(b, rel); fb.pop(rel, None); m += 1   # 바깥 폴더에서 지움 → assets 도 지움
    for rel, t in fa.items():
        if rel not in fb or t > fb[rel] + 1: _copy(a, b, rel); n += 1
    for rel, t in fb.items():
        if rel not in fa or t > fa[rel] + 1: _copy(b, a, rel); n += 1
    both = sorted(set(fa) | set(fb))
    return n, m, both

def main():
    if os.path.isdir(os.path.join(ROOT, '.git')):   # 9/15: 저장소 루트가 야구자판기\ 면 사진·음성이 그대로 깃에 들어가므로 assets 사본은 쓰지 않는다
        return 0
    total = 0
    seen_all = _load_seen()
    for a, b, exts in PAIRS:
        if not os.path.isdir(a) and not os.path.isdir(b): continue
        os.makedirs(a, exist_ok=True); os.makedirs(b, exist_ok=True)
        key = os.path.relpath(a, ROOT).replace('\\', '/')
        if key not in seen_all and os.path.basename(a) in seen_all: seen_all[key] = seen_all.pop(os.path.basename(a))   # 옛 기록 이름 이어받기
        first = key not in seen_all and bool(_files(a, exts))   # 기록 없는 첫 실행이라도 바깥 폴더가 비어 있으면(새 PC) assets 에서 그대로 받는다
        n, m, both = sync_pair(a, b, seen_all.get(key, []), first=first, exts=exts)
        seen_all[key] = both
        total += n + m
        if n or m: print(f'사진 동기화 {key}: 복사 {n}개, 삭제 {m}개')
    _save_seen(seen_all)
    if total == 0: print('사진 동기화: 바뀐 것 없음')
    return total

if __name__ == '__main__':
    try: main()
    except Exception as e:
        print('사진 동기화 실패:', e); sys.exit(0)   # 동기화 실패로 제작이 멈추지 않게
