# -*- coding: utf-8 -*-
"""깃 ↔ 구글 드라이브 보관 (10/16 사용자 지시)

  깃 저장         = 영상(mp4) 빼고 전부 저장
  깃 가져오기     = 깃에 있는 걸 이 컴퓨터에 맞춤
  깃_구글드라이브 = 완성된 영상의 파일을 구글 드라이브로 옮기고, 깃에서 지운 뒤 깃 기록에서도 지운다
                   (작업 중인 것은 옮기지 않는다)

모드
  archive   : 깃_구글드라이브.cmd (구글 드라이브 폴더가 있는 PC — 집)
  pullcheck : 깃저장·깃가져오기.cmd 가 pull 전에 부른다. 다른 PC 가 기록을 정리했으면
              이 PC 의 변경분을 백업 → 새 기록에 맞춤 → 변경분을 다시 넣는다.

'완성된 영상' = 콘티 날짜(파일·폴더 이름 앞 YYYY-MM-DD)가 ARCHIVE_DAYS(기본 7)일 지난 것.
옮기는 것: 시스템\\episodes 콘티 · <시리즈>\\음성 의 대본·음성 zip · <시리즈>\\영상\\<날짜> 폴더 ·
          선수이미지\\누끼 (썸네일 전용 — 마지막 커밋이 7일 지난 것)
작업 중인 콘티(7일 안)가 이름을 가리키는 파일은 옮기지 않는다.
경기 사진·카드·프로필·폰트·로고·시스템 코드는 회사 PC 에서도 써야 하므로 옮기지 않는다.
"""
import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent           # 시스템\
ROOT = HERE.parent                                      # 야구자판기\ (저장소 맨 위)
DOCS = HERE / 'docs'
MARK = DOCS / 'git_rewrite_id.txt'                      # 기록 정리 표시(바뀌면 다른 PC 가 알아챔)
ARCH_LIST = DOCS / 'git_archived_paths.txt'            # 드라이브로 옮긴 파일 목록(누적)
HASHES = DOCS / 'archived_thumb_hashes.json'           # 옮긴 사진의 dHash (썸네일 재사용 검사용)
BACKUP_DIR = ROOT / '_깃정리_백업'
SERIES = ['야구롱폼', '야구이슈', '야구순위', '야구분석']
DAYS = int(os.environ.get('ARCHIVE_DAYS', '7'))
DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})')


def rel(p):
    return Path(p).resolve().relative_to(ROOT).as_posix()


def git(*a, check=True):
    r = subprocess.run(['git', '-c', 'core.quotepath=false', *a], cwd=ROOT,
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if check and r.returncode != 0:
        raise RuntimeError(f'git {a[0]} 실패: ' + (r.stderr or r.stdout or '').strip()[-400:])
    return r


def branch():
    return git('rev-parse', '--abbrev-ref', 'HEAD').stdout.strip()


def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def pdate(s):
    m = DATE_RE.match(s)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), '%Y-%m-%d').date()
    except ValueError:
        return None


def drive_root():
    """설정.txt 의 OUTPUT_DIR(구글 드라이브 결과물 폴더) 옆에 '야구자판기_보관' 폴더."""
    out = os.environ.get('OUTPUT_DIR', '')
    cfg = HERE / '설정.txt'
    if not out and cfg.exists():
        for line in cfg.read_text(encoding='utf-8', errors='replace').splitlines():
            m = re.match(r'\s*OUTPUT_DIR\s*=\s*(.+?)\s*$', line)
            if m:
                out = m.group(1).strip().strip('"')
    if not out or not Path(out).exists():
        return None
    return Path(out).parent / '야구자판기_보관'


# ───────────────────────── pullcheck ─────────────────────────
def pullcheck():
    try:
        br = branch()
        old = git('rev-parse', '--verify', '-q', f'refs/remotes/origin/{br}', check=False).stdout.strip()
        f = git('fetch', '-q', 'origin', check=False)
        if f.returncode != 0:
            print('[기록 확인] 인터넷/깃허브 연결 실패 - 확인 건너뜀')
            return 0
        rm = git('show', f'origin/{br}:시스템/docs/git_rewrite_id.txt', check=False)
        remote_mark = rm.stdout.strip() if rm.returncode == 0 else ''
        local_mark = MARK.read_text(encoding='utf-8').strip() if MARK.exists() else ''
        if not remote_mark or remote_mark == local_mark:
            print('[기록 확인] 다른 PC 에서 기록 정리 없음')
            return 0
        print('[기록 확인] 다른 PC 가 깃 기록을 정리했어요 → 이 PC 를 새 기록에 맞춥니다')
        al = git('show', f'origin/{br}:시스템/docs/git_archived_paths.txt', check=False)
        archived = set()
        if al.returncode == 0:
            for line in al.stdout.splitlines():
                if '\t' in line:
                    archived.add(line.split('\t', 1)[1].strip())
        base = old if old else f'origin/{br}'
        d = git('diff', '--name-only', '--diff-filter=AMR', '-z', base, 'HEAD', check=False).stdout
        changed = [p for p in d.split('\0') if p and p not in archived and (ROOT / p).is_file()]
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        bak = BACKUP_DIR / ts
        for p in changed:
            dst = bak / p
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / p, dst)
        git('reset', '-q', '--hard', f'origin/{br}')
        for p in changed:
            dst = ROOT / p
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(bak / p, dst)
        git('reflog', 'expire', '--expire=now', '--all', check=False)
        git('gc', '--prune=now', '-q', check=False)
        print(f'[기록 확인] 새 기록으로 맞춤 완료. 이 PC 에서 바꾼 파일 {len(changed)}개는 다시 넣었고,'
              f' 사본은 _깃정리_백업\\{ts}\\ 에 있어요.')
        return 3
    except Exception as e:
        print('[기록 확인] 오류:', e)
        return 1


# ───────────────────────── archive ─────────────────────────
def last_commit_times():
    """경로 → 마지막 커밋 시각(초)."""
    out = git('log', '--format=%x01%ct', '--name-only', '-z').stdout
    t, seen = 0, {}
    for tok in out.replace('\n', '\0').split('\0'):
        if not tok:
            continue
        if tok.startswith('\x01'):
            t = int(tok[1:])
        elif tok not in seen:
            seen[tok] = t
    return seen


def plan():
    today = date.today()
    cut = today - timedelta(days=DAYS)
    files = [p for p in git('ls-files', '-z').stdout.split('\0') if p]
    # 작업 중(7일 안) 콘티 글 — 이름이 여기에 나오면 옮기지 않는다
    refs = []
    for p in files:
        if p.startswith('시스템/episodes/') and p.endswith('.json'):
            d = pdate(Path(p).name)
            if d and d > cut:
                try:
                    refs.append((ROOT / p).read_text(encoding='utf-8', errors='replace'))
                except OSError:
                    pass
    for p in files:   # 최근에 바꾼 썸네일 설정(tools\*.json)도 작업 중으로 본다
        if p.startswith('시스템/tools/') and p.endswith('.json'):
            q = ROOT / p
            if q.exists() and q.stat().st_mtime > (datetime.now() - timedelta(days=DAYS)).timestamp():
                refs.append(q.read_text(encoding='utf-8', errors='replace'))
    reftext = '\n'.join(refs)

    def used(p):
        stem = Path(p).stem
        for s in (stem, re.sub(r'_(대본|음성)$', '', stem)):
            if s and s in reftext:
                return True
        return False

    lct = None
    pick = {}
    for p in files:
        parts = p.split('/')
        cat = None
        if p.startswith('시스템/episodes/') and p.endswith('.json') and '/_샘플/' not in p:
            d = pdate(parts[-1])
            if d and d <= cut and not used(p):
                cat = '콘티'
        elif parts[0] in SERIES and len(parts) >= 3 and parts[1] == '영상':
            d = pdate(parts[2])
            if d and d <= cut:
                cat = '영상 폴더(썸네일·유튜브.txt)'
        elif parts[0] in SERIES and len(parts) == 3 and parts[1] == '음성':
            d = pdate(parts[2])
            if d and d <= cut and not used(p):
                cat = '음성·대본'
        elif p.startswith('선수이미지/누끼/'):
            if lct is None:
                lct = last_commit_times()
            t = lct.get(p, 0)
            if t and datetime.fromtimestamp(t).date() <= cut and not used(p):
                cat = '썸네일 누끼'
        if cat:
            pick[p] = cat
    return pick


def dhash(p):
    try:
        from PIL import Image
        im = Image.open(p).convert('L').resize((9, 8))
        px = list(im.getdata())
        bits = ''.join('1' if px[r * 9 + c] > px[r * 9 + c + 1] else '0' for r in range(8) for c in range(8))
        return '%016x' % int(bits, 2)
    except Exception:
        return None


def rewrite_history(paths, dest):
    br = branch()
    url = git('remote', 'get-url', 'origin').stdout.strip()      # 화면에 찍지 않는다
    print('  · 정리 전 전체 백업(번들)을 드라이브에 만드는 중 …')
    bundle = dest / '_깃백업_정리직전.bundle'
    tmp = dest / '_깃백업_정리직전.bundle.part'
    git('bundle', 'create', str(tmp), '--all')
    os.replace(tmp, bundle)
    print(f'    {bundle} ({bundle.stat().st_size // (1 << 20)} MB)')
    lst = ROOT / '.git' / 'archive_paths.lst'
    lst.write_bytes(b'\0'.join(p.encode('utf-8') for p in paths) + b'\0')
    print('  · 깃 기록에서 지우는 중(몇 분 걸려요) …')
    env = dict(os.environ, FILTER_BRANCH_SQUELCH_WARNING='1', GA_LIST=str(lst))
    flt = 'git rm -r -q --cached --ignore-unmatch --pathspec-from-file="$GA_LIST" --pathspec-file-nul'
    r = subprocess.run(['git', 'filter-branch', '-f', '--prune-empty', '--index-filter', flt,
                        '--tag-name-filter', 'cat', '--', '--all'],
                       cwd=ROOT, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode != 0:
        raise RuntimeError('기록 정리 실패: ' + (r.stderr or '')[-400:])
    for ref in git('for-each-ref', '--format=%(refname)', 'refs/original/').stdout.split():
        git('update-ref', '-d', ref, check=False)
    if 'origin' not in git('remote').stdout.split():
        git('remote', 'add', 'origin', url)
    MARK.parent.mkdir(parents=True, exist_ok=True)
    MARK.write_text(f'{datetime.now():%Y-%m-%d %H:%M:%S} {socket.gethostname()}\n', encoding='utf-8')
    git('add', rel(MARK))
    git('commit', '-q', '-m', '깃 기록 정리 표시')
    print('  · 깃허브에 덮어쓰는 중 …')
    p = git('push', '--force', '-u', 'origin', f'HEAD:{br}', check=False)
    if p.returncode != 0:
        raise RuntimeError('깃허브 덮어쓰기 실패 — 인터넷 확인 후 깃_구글드라이브를 다시 실행하세요')
    git('reflog', 'expire', '--expire=now', '--all', check=False)
    git('gc', '--prune=now', '-q', check=False)
    lst.unlink(missing_ok=True)


def size_of_repo():
    r = git('count-objects', '-vH', check=False).stdout
    m = re.search(r'size-pack:\s*(.+)', r)
    return m.group(1).strip() if m else '?'


def archive():
    dest = drive_root()
    if not dest:
        print('이 PC 엔 구글 드라이브 결과물 폴더(설정.txt OUTPUT_DIR)가 없어요 → 집 PC 에서 실행하세요.')
        return 1
    print('1) 먼저 이 PC 를 깃허브와 맞춥니다 …')
    git('add', '-A')
    git('commit', '-q', '-m', 'pc update', check=False)
    pullcheck()
    git('add', '-A')
    git('commit', '-q', '-m', 'pc update', check=False)
    r = git('pull', '-q', '--rebase', '-X', 'theirs', check=False)
    if r.returncode != 0:
        git('rebase', '--abort', check=False)
        print('깃허브에서 받기 실패 — 인터넷 확인 후 다시 실행하세요.')
        return 1
    print(f'   지금 저장소 크기: {size_of_repo()}')

    pick = plan()
    if not pick:
        print(f'옮길 완성 영상 파일이 없어요({DAYS}일 지난 것 기준).')
        git('push', '-q', check=False)
        return 0
    by = {}
    for p, c in pick.items():
        s = (ROOT / p).stat().st_size
        n, t = by.get(c, (0, 0))
        by[c] = (n + 1, t + s)
    total = sum(t for _, t in by.values())
    print(f'\n2) 구글 드라이브로 옮길 것 ({DAYS}일 지난 완성 영상, 작업 중인 콘티가 쓰는 건 제외)')
    for c, (n, t) in by.items():
        print(f'   - {c}: {n}개 {t / 1e6:.1f} MB')
    print(f'   합계 {len(pick)}개 {total / 1e6:.1f} MB → {dest}')
    print('   옮긴 뒤 깃에서 지우고, 깃 기록에서도 지워서 깃허브 용량을 줄입니다.')
    print('   (다른 PC 는 다음 깃가져오기 때 자동으로 맞춰지고, 그 PC 에서도 이 파일들이 빠져요)')
    ans = input('\n   계속할까요? Y 를 누르고 Enter (다른 키 = 취소): ').strip().lower()
    if ans != 'y':
        print('취소했어요. 아무것도 바꾸지 않았어요.')
        return 0

    print('\n3) 구글 드라이브로 복사하고 같은지 확인 …')
    dest.mkdir(parents=True, exist_ok=True)
    paths = sorted(pick)
    for i, p in enumerate(paths, 1):
        src, dst = ROOT / p, dest / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        h = sha1(src)
        if not (dst.exists() and sha1(dst) == h):
            tmp = dst.with_name(dst.name + '.part')
            shutil.copy2(src, tmp)
            os.replace(tmp, dst)
            if sha1(dst) != h:
                raise RuntimeError(f'복사 확인 실패: {p} — 아무것도 지우지 않고 멈춰요')
        if i % 50 == 0 or i == len(paths):
            print(f'   {i}/{len(paths)}')

    hashes = json.loads(HASHES.read_text(encoding='utf-8')) if HASHES.exists() else {}
    for p in paths:
        if Path(p).suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp'):
            h = dhash(ROOT / p)
            if h:
                hashes[p] = h
    HASHES.parent.mkdir(parents=True, exist_ok=True)
    HASHES.write_text(json.dumps(hashes, ensure_ascii=False, indent=0), encoding='utf-8')
    with open(ARCH_LIST, 'a', encoding='utf-8') as f:
        for p in paths:
            f.write(f'{date.today():%Y-%m-%d}\t{p}\n')

    print('\n4) 깃에서 지우기 …')
    lst = ROOT / '.git' / 'archive_rm.lst'
    lst.write_bytes(b'\0'.join(p.encode('utf-8') for p in paths) + b'\0')
    git('rm', '-r', '-q', '--pathspec-from-file', str(lst), '--pathspec-file-nul')
    lst.unlink(missing_ok=True)
    git('add', rel(ARCH_LIST), rel(HASHES))
    git('commit', '-q', '-m', f'구글 드라이브로 보관: {len(paths)}개')

    print('\n5) 깃 기록에서도 지우기 …')
    rewrite_history(paths, dest)
    print(f'\n완료: {len(paths)}개를 구글 드라이브 {dest} 로 옮겼어요. 지금 저장소 크기: {size_of_repo()}')
    print('깃허브 쪽 용량 숫자는 깃허브가 정리할 때까지 며칠 걸릴 수 있어요.')
    print('다른 PC 는 다음 깃가져오기(또는 깃저장) 때 자동으로 새 기록에 맞춰져요.')
    return 0


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'pullcheck':
        sys.exit(pullcheck())
    if mode == 'archive':
        try:
            sys.exit(archive())
        except Exception as e:
            print('\n오류로 멈췄어요:', e)
            sys.exit(1)
    if mode == 'plan':
        pk = plan()
        for p, c in sorted(pk.items()):
            print(c, p)
        print(len(pk), '개')
        sys.exit(0)
    print('사용법: git_archive.py archive|pullcheck|plan')
