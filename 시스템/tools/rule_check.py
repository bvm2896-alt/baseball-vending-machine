# -*- coding: utf-8 -*-
"""롱폼·쇼츠 콘티 규칙 검사 (10/18 신설) — 사용자 피드백으로 정한 규칙을 사람이 아니라 스크립트가 막는다.
쓰기:  python tools/rule_check.py episodes/2026-10-18_롱폼.json      (생성 스크립트 끝에서도 자동 호출)
걸리면 '규칙 위반' 목록을 찍고 종료 코드 1 → 렌더 전에 고친다.

검사 항목 (사용자 지시 날짜)
 R1 사진 종류 통일(10/18 "왜 누구는 프로필이고 누구는 플레이 사진이야?"): 스튜디오·증명 사진 금지 → KBO프로필/·국가대표프로필/·STUDIO 목록
 R2 이모지 대신 그림(10/18 "이모지 글러브로 해야지"): 🧤🏏⚾🥎 같은 야구 이모지는 assets/icons 그림으로
 R3 줄바꿈(10/18 "줄바꿈 이따구로 할래"): 줄이 '·'로 시작·끝나면 안 됨, 한 줄에 한 글자·조사만 남으면 안 됨
 R4 같은 틀 안 움직임(10/18 "뚝 끊기면서 갑자기 카드가 커진다"): 같은 묶음(chain·cont) 안에서 뒤 장면에만 있는 칸(k·text·줄)은
    앞 장면에 자리(khide·hide)가 있어야 한다 — 템플릿(facegrid·faceoff·pstat)이 자동으로 자리를 잡는 종류는 통과.
    정적 검사로는 확정이 안 되므로 '확인 필요'로만 찍고, 렌더한 검수판의 이동 검사(끝 장면 → 다음 끝 장면 요소 위치 비교)로 확정한다
 R5 가운데 맞춤(10/18 "소형준 사진 나올때마다 가운데로"): CENTER_FIX 에 적힌 선수는 정해진 가운데 맞춤 카드만
 R6 같은 사람·같은 묶음은 같은 사진(묶음 안에서 사진이 바뀌면 깜빡임)
 R7 사용 금지 사진(10/18 "소형준 이 사진 절대 쓰지마"): BANNED 목록
 R8 이어받기 표시 누락(10/18 "사진은 다 그대로인데 한번 사라졌다가 다시 촤르륵 나타나게 한거야? 텍스트만 바뀌게 하라고 했잖아"): 바로 앞 장면과 같은 종류·같은 묶음(chain)이면 cont 필수
    (템플릿도 facegrid 는 같은 사람·사진이면 자동 처리하지만, 표시 누락은 여기서 렌더 전에 막는다)
 R1 예외(10/18 "여기는 전부 프로필 사진으로 해줘"): 장면에 profile=True 면 프로필 사진만 허용·전부 프로필(PROFILE_CARD)이어야 함. 그 밖 장면에 프로필 카드가 오면 R1
 (렌더 검수판) 장면 시작 깜빡임(10/18 "왼쪽 카드 내용이 잠깐 사라졌다 다시 생긴다"): 이어지는 장면 시작 0.03·0.15·0.3초에 앞 장면 글이 남아 있는지 — 검수판 flash 검사
"""
import json, re, sys

STUDIO_DIRS = ('KBO프로필/', '국가대표프로필/', '일본대표/', 'MLB/')   # 10/24: MLB/ = MLB 공식 헤드샷(프로필 사진)
STUDIO = {'카드/최원준_MVP_상체', '카드/FA9_염경엽', '카드/FA9_이범호', '카드/FA9_카라스코', '카드/R13_케네디_2026LG', '카드/T12_이범호', '카드/T12_임찬규', '카드/R13_임찬규'}   # 10/18 눈 검수로 찾은 흰 배경 스튜디오 카드
PROFILE_CARD = re.compile(r'^카드/G18P_')   # 10/18 요약판용 구단 프로필(누끼·같은 배경) — profile=True 장면 전용          # 확인된 스튜디오(검은 배경·미디어데이) 카드 — 새로 찾으면 여기에 더한다
CENTER_FIX = {'소형준': '카드/G18_소형준_B'}   # 원본이 한쪽에 치우친 선수 → 이 카드만(얼굴 정면·가운데, 10/18 교체)
CIRCLE_OK = {'카드/G18원_선동열', '카드/P29P_김하성'}   # 10/25: 김하성 샌디에이고 시절(2020 포스팅) 장면 — 그 시절 구단 프로필이 없어 얼굴 가운데 자른 샌디에이고 사진(사진 시절 일치 9/28)   # 프로필이 없는 옛 선수(1989년 사진)
BANNED = re.compile(r'소형준_투구|R13_소형준')   # 10/18 사용자 "소형준 이 사진 절대 쓰지마. 앞으로도" — 얼굴이 왼쪽 아래 구석에 나오는 투구 사진(원본·카드 전부)
EMOJI_BAN = re.compile('[\U0001F9E4\U0001F3CF⚾\U0001F94E]')   # 🧤 🏏 ⚾ 🥎
AUTO_RESERVE = {'facegrid', 'faceoff', 'pstat'}   # 템플릿이 묶음 전체를 보고 자리를 미리 잡는 종류


def walk(x, path=''):
    if isinstance(x, dict):
        for k, v in x.items(): yield from walk(v, f'{path}.{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from walk(v, f'{path}[{i}]')
    else:
        yield path, x


def check(ep):
    sc = ep.get('scenes', []); bad = []
    for i, s in enumerate(sc):
        for p, v in walk(s):
            if not isinstance(v, str): continue
            key = p.rsplit('.', 1)[-1]
            if key in ('img',) or p.endswith('.img') or re.search(r'\.imgs\[\d+\]$', p):
                isprof = v.startswith(STUDIO_DIRS) or v in STUDIO or bool(PROFILE_CARD.search(v))
                circle = s.get('type') in ('facegrid', 'bars') and not s.get('whole') and not s.get('card') and re.search(r'^\.?items\[\d+\]\.img$', p)
                circle = circle or (s.get('type') == 'pstat' and re.search(r'viz\[\d+\]\.items\[\d+\]\.img$', p) and any(z.get('type') == 'mini' for z in s.get('viz', [])))
                circle = circle or s.get('type') == 'feecalc'   # 10/25: 이적료 계산 장면의 얼굴은 전부 작은 원 → 프로필만   # 10/25: pstat 안 작은 얼굴 원(mini)도 원 → 프로필만
                if circle:   # 10/18 밤 사용자 "원 안에 사진은 프로필 사진으로 넣어줘"(얼굴이 빗나간 경기 사진 원 금지) — 원 안은 구단 프로필(G18P_), 프로필이 없는 옛 선수만 예외
                    if not PROFILE_CARD.search(v) and v not in CIRCLE_OK: bad.append((i, 'R1 원 안은 프로필 사진', f'{p} = {v}'))
                elif s.get('profile'):
                    if not isprof: bad.append((i, 'R1 프로필 장면에 플레이 사진', f'{p} = {v} (profile=True 장면은 전부 프로필)'))
                elif isprof: bad.append((i, 'R1 스튜디오·프로필 사진', f'{p} = {v}'))
                if BANNED.search(v): bad.append((i, 'R7 사용 금지 사진', f'{p} = {v} (사용자 금지)'))
                for who, card in CENTER_FIX.items():
                    if who in v and v != card: bad.append((i, 'R5 가운데 맞춤 카드 아님', f'{who}: {v} → {card}'))
                continue
            if v.startswith('data:') or v.startswith('<img'): continue
            if EMOJI_BAN.search(v): bad.append((i, 'R2 야구 이모지', f'{p} = {v!r} → assets/icons 그림'))
            if '\n' in v:
                ls = v.split('\n')
                for ln in ls:
                    t = ln.strip()
                    if t.startswith('·') or t.endswith('·'): bad.append((i, "R3 줄이 '·'로 시작·끝", f'{p} = {v!r}'))
                    if 0 < len(t.replace(' ', '')) <= 1: bad.append((i, 'R3 한 글자만 남은 줄', f'{p} = {v!r}'))
    # R4·R6: 묶음
    for i in range(1, len(sc)):
        a, b = sc[i - 1], sc[i]
        same = b.get('cont') and a.get('type') == b.get('type') or (b.get('chain') and b.get('chain') == a.get('chain'))
        if a.get('type') == b.get('type') and b.get('chain') and b.get('chain') == a.get('chain') and not b.get('cont'):
            bad.append((i, 'R8 이어받기 표시 없음', f"{b.get('type')} chain={b.get('chain')} {b.get('title') or b.get('name') or ''} → cont=True (사진 고정, 글만 바뀜)"))
        if not same: continue
        if b.get('name') and a.get('name') == b.get('name') and a.get('img') and b.get('img') and a['img'] != b['img']:
            bad.append((i, 'R6 같은 묶음에서 사진 바뀜', f"{a['img']} → {b['img']}"))
        if a.get('type') != b.get('type') or b['type'] in AUTO_RESERVE: continue
        if b.get('text') and not a.get('text'): bad.append((i, 'R4 앞 장면에 글 자리 없음', f"text {b['text']!r}"))
        ia, ib = a.get('items') or [], b.get('items') or []
        if len(ia) != len(ib): bad.append((i, 'R4 칸 수가 바뀜', f'{len(ia)} → {len(ib)} (앞 장면에 hide 칸)'))
        for j, (x, y) in enumerate(zip(ia, ib)):
            if isinstance(x, dict) and isinstance(y, dict):
                for k in ('k', 'v', 'sub', 'note'):
                    if y.get(k) and not x.get(k): bad.append((i, 'R4 칸 높이 바뀜', f'items[{j}].{k} 앞 장면에 없음 → 같은 글 + khide'))
    return bad


if __name__ == '__main__':
    ep = json.load(open(sys.argv[1], encoding='utf-8'))
    bad = check(ep)
    err = [b for b in bad if not b[1].startswith('R4')]; warn = [b for b in bad if b[1].startswith('R4')]
    for i, r, m in err: print(f'규칙 위반 장면 {i}: {r} | {m}')
    for i, r, m in warn: print(f'확인 필요 장면 {i}: {r} | {m}  → 렌더 검수판 이동 검사(move.js)로 확정')
    print('규칙 검사', '통과' if not err else f'위반 {len(err)}건', f'/ 확인 필요 {len(warn)}건' if warn else '')
    sys.exit(1 if err else 0)
