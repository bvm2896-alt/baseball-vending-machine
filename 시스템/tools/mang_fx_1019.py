# -*- coding: utf-8 -*-
"""10/19~20 롱폼⑳ 연출(v17 확정 대사 89장면) — 장면마다 망냥이 표정(mood)·말풍선(say)·효과(fx)·생각 구름(dreamNo/dreamLabel)을 얹는다.
gen_1019_long20.py 끝에서 부른다. 경기 스코어 장면(mscore)은 쓰지 않는다(사용자 10/19 "스코어는 넣지마")."""
import json, io, sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'episodes/2026-10-19_롱폼.json'
e = json.load(io.open(P, encoding='utf-8')); S = e['scenes']
M = {  # 장면 번호: (mood, say, fx)
 0: ('shock', '망상 주의!', None), 1: ('love', '두근두근', 'sparkle'), 2: ('sweat', '세 번뿐…?', None), 3: ('calc', '6번 중 1번', 'sparkle'),
 4: ('think', '따져 보자', None), 5: ('wave', '가보자고!', None),
 6: ('cheer', '2연승!', None), 7: ('calc', None, None), 9: ('sweat', None, None), 10: ('shock', '오스틴…', None),
 11: ('sweat', '112승?!', None), 12: ('think', None, None), 13: ('love', None, 'sparkle'), 14: ('think', '불펜 싸움', None),
 15: ('idle', None, None), 16: ('love', None, None), 17: ('love', '든든!', 'sparkle'), 18: ('sweat', None, None), 19: ('calc', None, None),
 20: ('sweat', '견제…', None), 21: ('sweat', None, None), 22: ('cheer', '카스트로!', 'confetti'), 23: ('cheer', None, None), 24: ('love', '숨은 무기', 'sparkle'),
 25: ('think', None, None), 26: ('calc', None, None), 27: ('shock', '마지막 잠실', None), 28: ('sweat', None, None), 29: ('calc', None, None),
 30: ('cheer', '3연승!', 'confetti'), 31: ('cry', '네 번 모두…', None),
 32: ('wave', None, None), 33: ('idle', None, None), 34: ('sweat', '반반이네', None), 35: ('love', '9승 7패', None), 36: ('calc', None, None),
 37: ('think', None, None), 38: ('love', None, None), 39: ('shock', '타격왕', None), 40: ('sweat', None, None), 41: ('think', None, None),
 42: ('sweat', None, None), 43: ('love', None, None), 44: ('cheer', '1차전 KIA', None), 45: ('think', None, None), 46: ('sweat', None, None),
 47: ('cry', '1승 1패', None), 48: ('love', None, 'sparkle'), 49: ('cheer', '2승 1패!', 'confetti'), 50: ('calc', None, None), 51: ('shock', '난타전!', None),
 52: ('cheer', '한국시리즈다!', 'fireworks'),
 53: ('sweat', '제일 어려워', None), 54: ('sweat', None, None), 55: ('calc', None, None), 56: ('think', None, None), 57: ('calc', None, None),
 58: ('shock', '3주 휴식', None), 59: ('think', None, None), 60: ('sweat', '지쳤어…', None), 61: ('shock', '삼진 54개', None), 62: ('sweat', None, None),
 63: ('cry', '0승 2패…', None), 64: ('sweat', '친정 팀', None), 65: ('sweat', None, None), 66: ('shock', '타점왕', None), 67: ('think', None, None),
 68: ('sweat', '4승 5패', None), 69: ('cheer', None, 'sparkle'), 70: ('think', '투수전', None), 71: ('calc', None, None), 72: ('cheer', '2승 2패!', 'confetti'),
 73: ('think', None, None), 74: ('cheer', '3승 2패!', 'confetti'), 75: ('sweat', None, None), 76: ('cry', '3승 3패…', None),
 77: ('sweat', '완전 반반', None), 78: ('think', None, None), 79: ('calc', None, None), 80: ('cheer', None, None), 81: ('love', None, 'sparkle'),
 82: ('cheer', '김도영!', 'sparkle'), 83: ('cheer', '우승이다!!', 'fireworks'), 84: ('love', None, 'sparkle'), 85: ('love', None, None),
 86: ('calc', '약 17%', 'sparkle'), 87: ('wave', '망상이에요~', None), 88: ('wave', '예측 남겨줘!', None),
}
for i, (mood, say, fx) in M.items():
    s = S[i]; s['mood'] = mood
    if say: s['say'] = say
    if fx: s['fx'] = fx
# 10/20 사용자: 결과(○승 ○패·폭죽·표정)는 그 결과를 말하는 호흡에서 — 그 전엔 생각하는 표정(think), 말풍선·폭죽 없음
REVEAL = {0: 2, 2: 1, 3: 1, 4: 1, 5: 2, 6: 1, 10: 1, 11: 1, 14: 2, 17: 3, 20: 1, 24: 1, 27: 3, 30: 1, 31: 2, 34: 3, 35: 1, 39: 2, 44: 1,
          47: 1, 49: 3, 51: 2, 52: 2, 53: 3, 58: 1, 60: 5, 61: 3, 63: 6, 64: 2, 66: 3, 68: 4, 70: 2, 72: 4, 74: 4, 76: 2, 77: 4, 82: 2, 83: 0.2,
          86: 4, 87: 1, 88: 2}   # 10/20 사용자 "캐릭터가 내용이 나오기 전에 먼저 말하지 않게" — 말풍선마다 그 말을 하는 호흡
for i, k in REVEAL.items():
    S[i]['revealAt'] = k
    if S[i]['type'] == 'series5':   # 이번에 새로 채우는 경기 결과 원·큰 글·예측 알약도 그 호흡 전엔 안 뜨게
        pv_ = next((S[j] for j in range(i - 1, -1, -1) if S[j].get('type') == 'series5' and S[j].get('chain') == S[i].get('chain')), None)   # 같은 줄(chain)의 바로 앞 시리즈 표
        for j_, g_ in enumerate(S[i]['games']):
            had_ = pv_ and j_ < len(pv_['games']) and pv_['games'][j_].get('win') == g_.get('win')
            if g_.get('win') and not had_: g_['at'] = max(g_.get('at') or 0, k)
        if S[i].get('text') and (S[i].get('textAt') or 0) < k: S[i]['textAt'] = k + .1
        for j_, at_ in {47: {0: 0}, 52: {2: 0}}.get(i, {}).items(): S[i]['games'][j_]['at'] = at_   # 앞 장면(선수 카드)에서 이미 말한 경기 결과는 처음부터
        for q in S[i].get('pills', []):
            if '예측' in q['label']: q['at'] = max(q.get('at') or 0, k)
# 생각 구름: 예측하는 경기의 첫 장면
DREAM = {8: (1, '준플레이오프 3차전 · 잠실'), 43: (2, '플레이오프 1차전 · 대구'), 45: (3, '플레이오프 2차전 · 대구'), 48: (4, '플레이오프 3차전 · 광주'),
         51: (5, '플레이오프 4차전 · 광주'), 61: (6, '한국시리즈 1·2차전 · 수원'), 70: (7, '한국시리즈 3차전 · 광주'), 71: (8, '한국시리즈 4차전 · 광주'),
         73: (9, '한국시리즈 5차전 · 광주'), 75: (10, '한국시리즈 6차전 · 수원'), 77: (11, '한국시리즈 7차전 · 수원')}
for i, (n, t) in DREAM.items():
    # 10/20 사용자 "나레이션은 변수 여섯인데 이미지는 예측 9 — 뭐가 맞는 거야?" → 경기 번호와 변수 번호가 섞여 헷갈림. 구름엔 '몇 차전 예측'만, 아래에 시리즈·장소
    sr, gm, pl = re.match(r'(.+?) (\S+차전) · (.+)', t).groups()
    S[i]['dreamNo'] = n; S[i]['dreamLabel'] = f'{gm} 예측'; S[i]['dreamTitle'] = f'{sr} · {pl}'; S[i].setdefault('mood', 'think')
# 10/19 15:19 사용자 "마스코트는 빼자 뿅망치 애니메이션도 빼고" → 구단 캐릭터(crew)·뿅망치(bonk) 없음
e['mascot'] = True; e['theme'] = 'dark'
io.open(P, 'w', encoding='utf-8').write(json.dumps(e, ensure_ascii=False, indent=1)); print('ok', len(M), 'moods')
