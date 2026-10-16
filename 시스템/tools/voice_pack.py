# -*- coding: utf-8 -*-
"""롱폼 음성을 깃으로 옮기기 (10/16 사용자: "음성도 같이 깃저장할 때 옮기는 방법 없어?")

work\ 와 *.mp3 는 깃에 안 올라가서, 집에서 API 로 뽑은 롱폼 음성이 회사 PC 에 없었다.
  pack   : 깃저장.cmd 가 부른다. 최근 7일 안에 바뀐 work\voice_<날짜>_* 폴더(전 시리즈)를
           <시리즈>\음성\<콘티이름>_음성.zip 으로 묶는다(내용이 같으면 그대로 둔다).
  unpack : 깃가져오기.cmd 가 부른다. 그 zip 을 work\voice_<콘티이름>\ 로 푼다.
           이 PC 에 없는 파일은 넣고, 있는 파일은 zip 쪽이 더 새것일 때만 바꾼다.
fresh.flag 같은 신호 파일과 wav 는 옮기지 않는다.
"""
import hashlib
import json
import os
import sys
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # 시스템\
ROOT = HERE.parent                                     # 야구자판기\
WORK = HERE / 'work'
OUT = ROOT / '야구롱폼' / '음성'
DATE_RE = __import__('re').compile(r'^\d{4}-\d{2}-\d{2}_')


def out_dir(name):
    for k, d in (('롱폼', '야구롱폼'), ('순위', '야구순위'), ('분석', '야구분석')):
        if k in name:
            return ROOT / d / '음성'
    return ROOT / '야구이슈' / '음성'
EXTS = {'.mp3', '.txt', '.json', '.tempo', '.keep'}
DAYS = 7
SUFFIX = '_음성.zip'


def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def files_of(d):
    return sorted(p for p in d.iterdir() if p.is_file() and p.suffix.lower() in EXTS)


def read_manifest(z):
    try:
        with zipfile.ZipFile(z) as zf:
            return json.loads(zf.read('manifest.json').decode('utf-8'))
    except Exception:
        return None


def pack():
    if not WORK.exists():
        print('[음성 묶기] work 폴더 없음 - 건너뜀')
        return
    now = time.time()
    n = 0
    for d in sorted(WORK.glob('voice_*')):
        name = d.name[len('voice_'):]
        if not d.is_dir() or not DATE_RE.match(name):
            continue          # 10/16: 전 시리즈(날짜 이름 콘티) — 7일 지나면 깃_구글드라이브가 보관함으로 옮긴다
        fs = files_of(d)
        if not fs or not any(p.suffix.lower() == '.mp3' for p in fs):
            continue
        if now - max(p.stat().st_mtime for p in fs) > DAYS * 86400:
            continue
        man = {p.name: {'sha1': sha1(p), 'mtime': p.stat().st_mtime} for p in fs}
        out = out_dir(name)
        out.mkdir(parents=True, exist_ok=True)
        z = out / (name + SUFFIX)
        old = read_manifest(z) if z.exists() else None
        if old and {k: v['sha1'] for k, v in old.items()} == {k: v['sha1'] for k, v in man.items()}:
            print(f'[음성 묶기] {name}: 바뀐 것 없음')
            continue
        tmp = z.with_name(z.name + '.part')
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_STORED) as zf:
            for p in fs:
                zf.write(p, p.name)
            zf.writestr('manifest.json', json.dumps(man, ensure_ascii=False, indent=0))
        os.replace(tmp, z)
        n += 1
        print(f'[음성 묶기] {name}: 파일 {len(fs)}개 -> {out.parent.name}\\음성\\{z.name} ({z.stat().st_size // 1024} KB)')
    print(f'[음성 묶기] 새로 묶은 편 {n}개')


def unpack():
    n = 0
    zs = []
    for d in ('야구롱폼', '야구이슈', '야구순위', '야구분석'):
        if (ROOT / d / '음성').exists():
            zs += sorted((ROOT / d / '음성').glob('*' + SUFFIX))
    for z in zs:
        name = z.name[:-len(SUFFIX)]
        man = read_manifest(z)
        if not man:
            print(f'[음성 풀기] {z.name}: 목록 없음 - 건너뜀')
            continue
        d = WORK / ('voice_' + name)
        d.mkdir(parents=True, exist_ok=True)
        put = 0
        with zipfile.ZipFile(z) as zf:
            for fn, info in man.items():
                dst = d / fn
                if dst.exists():
                    if sha1(dst) == info['sha1']:
                        continue
                    if dst.stat().st_mtime >= info['mtime']:
                        continue          # 이 PC 쪽이 더 새것 - 그대로 둔다
                tmp = dst.with_name(dst.name + '.part')
                with open(tmp, 'wb') as f:
                    f.write(zf.read(fn))
                os.replace(tmp, dst)
                os.utime(dst, (info['mtime'], info['mtime']))
                put += 1
        if put:
            n += 1
            print(f'[음성 풀기] {name}: 파일 {put}개 -> work\\voice_{name}\\')
    print(f'[음성 풀기] 넣은 편 {n}개')


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    try:
        if mode == 'pack':
            pack()
        elif mode == 'unpack':
            unpack()
        else:
            print('사용법: voice_pack.py pack|unpack')
    except Exception as e:          # 깃 저장·가져오기를 막지 않는다
        print('[음성 옮기기] 오류(깃 작업은 계속):', e)
