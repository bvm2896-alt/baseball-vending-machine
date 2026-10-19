# -*- coding: utf-8 -*-
"""10/19 롱폼⑳ 망상 극장 연출 — 장면마다 망냥이 표정(mood)·말풍선(say)·효과(fx)·망상 구름(dreamNo)을 얹고,
확률 장면은 gauge·dice, 망상 스코어는 mscore(전광판)로 바꾼다. gen_1019_long20.py 끝에서 부른다."""
import json, io, sys
P = sys.argv[1] if len(sys.argv) > 1 else 'episodes/2026-10-19_롱폼.json'
e = json.load(io.open(P, encoding='utf-8')); S = e['scenes']
M = {  # 장면 번호: (mood, say, fx)
 0: ('shock', '망상 주의!', None), 1: ('love', '두근두근', 'sparkle'), 2: ('sweat', '세 번뿐…?', None), 3: ('think', None, None),
 4: ('calc', '잠깐만…', 'sparkle'), 5: ('calc', None, None), 6: ('calc', '곱하기…', None), 7: ('shock', '6번 중 1번!', 'sparkle'),
 8: ('wave', '가보자고!', None), 9: ('think', None, None), 10: ('wave', None, None),
 12: ('idle', None, None), 13: ('sweat', None, None), 14: ('love', None, None), 15: ('calc', '57%', None),
 16: ('cheer', '3연승!', 'confetti'), 17: ('cheer', None, None), 18: ('sweat', '반반이네', None), 19: ('love', None, None),
 21: ('think', None, None), 22: ('love', None, None), 23: ('cheer', None, None), 24: ('love', '김도영!', 'sparkle'),
 25: ('cheer', '결승 투런!', 'confetti'), 27: ('sweat', None, None), 28: ('sweat', None, None), 29: ('cry', '괜찮아…', 'rain'),
 31: ('love', None, None), 32: ('idle', None, None), 33: ('cheer', '2승 1패!', 'confetti'), 35: ('calc', None, None), 36: ('sweat', '변수…', None),
 37: ('cheer', '한국시리즈다!', 'fireworks'), 38: ('shock', '90승…', None), 39: ('sweat', None, None), 40: ('shock', '10연승?!', None), 41: ('sweat', None, None),
 43: ('shock', None, None), 45: ('cry', '0승 2패…', 'rain'), 46: ('shock', '지금부터!', 'sparkle'), 47: ('cheer', '광주 3연전!', None),
 48: ('love', None, 'sparkle'), 49: ('cheer', '스윕!', None), 51: ('love', None, None), 52: ('cheer', '1승 2패', 'confetti'),
 54: ('calc', None, None), 55: ('cheer', None, None), 56: ('cheer', '2승 2패!', 'confetti'), 58: ('think', None, None), 59: ('love', None, None),
 60: ('cheer', '3승 2패!', 'confetti'), 62: ('cry', '3승 3패…', 'rain'), 64: ('sweat', '완전 반반', None), 65: ('shock', '한 방…', None),
 66: ('faint', None, 'fireworks'), 67: ('cheer', '우승이다!!', 'fireworks'), 68: ('love', None, None), 69: ('calc', '약 17%', 'sparkle'),
 70: ('wave', '망상이에요~', None), 71: ('wave', '댓글로 알려줘!', None),
}
for i, (mood, say, fx) in M.items():
    s = S[i]; s['mood'] = mood
    if say: s['say'] = say
    if fx: s['fx'] = fx
# 망상 구름: 망상 n번째 경기 첫 장면
DREAM = {11: (1, '준플레이오프 3차전 · 잠실'), 20: (2, '플레이오프 1차전 · 대구'), 26: (3, '플레이오프 2차전 · 대구'), 30: (4, '플레이오프 3차전 · 광주'),
         34: (5, '플레이오프 4차전 · 광주'), 42: (6, '한국시리즈 1차전 · 수원'), 44: (7, '한국시리즈 2차전 · 수원'), 50: (8, '한국시리즈 3차전 · 광주'),
         53: (9, '한국시리즈 4차전 · 광주'), 57: (10, '한국시리즈 5차전 · 광주'), 61: (11, '한국시리즈 6차전 · 수원'), 63: (12, '한국시리즈 7차전 · 수원')}
for i, (n, t) in DREAM.items():
    S[i]['dreamNo'] = n; S[i]['dreamTitle'] = t; S[i].setdefault('mood', 'think')
# 망상 스코어 → 전광판
for i in (16, 25, 29, 33, 52, 56, 60, 62):
    s = S[i]; s['type'] = 'mscore'; s['size'] = 120; s['tag'] = s.get('tag', '').replace(' · 망상 스코어', '')
# 확률: 배터리·주사위
S[6] = dict(S[6], type='gauge', title='KIA 우승 확률 · 단계마다 곱하기', steps=[
    {'label': '준PO', 'team': 'LG', 'pass': 92, 'at': 0.1}, {'label': 'PO', 'team': '삼성', 'pass': 46, 'at': 1.4}, {'label': '한국시리즈', 'team': 'KT', 'pass': 40, 'at': 2.7}])
for i in (7, 69):
    S[i] = dict(S[i], type='dice', title='우승 확률 · 야구자판기 계산', big='약 17%', sub='6번 중 1번')

# 10/19 15:19 사용자 "마스코트는 빼자 뿅망치 애니메이션도 빼고" → 구단 캐릭터(crew)·뿅망치(bonk)는 넣지 않는다(템플릿 기능은 남겨 둠)
e['mascot'] = True; e['theme'] = 'dark'
io.open(P, 'w', encoding='utf-8').write(json.dumps(e, ensure_ascii=False, indent=1)); print('ok', len(M), 'moods')
