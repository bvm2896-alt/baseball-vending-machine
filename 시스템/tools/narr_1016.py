# -*- coding: utf-8 -*-
"""롱폼⑯ 나레이션 앞처리 — gen_1015_long15.narr_of 앞에 돌린다.
나이(살)·명·건은 고유어 전부(스물여섯 살·스물두 명·다섯 건), 범위 '~' 는 '에서',
영문 약어는 한글 발음(에프에이·오피에스·에이 등급)."""
import re
U = {1: '한', 2: '두', 3: '세', 4: '네', 5: '다섯', 6: '여섯', 7: '일곱', 8: '여덟', 9: '아홉'}
T = {1: '열', 2: '스물', 3: '서른', 4: '마흔', 5: '쉰', 6: '예순', 7: '일흔', 8: '여든', 9: '아흔'}
def nat_full(n):
    n = int(n); t, u = divmod(n, 10)
    if n == 20: return '스무'
    return (T.get(t, '') + U.get(u, '')) if n < 100 else str(n)
def pre(t):
    D = '일이삼사오육칠팔구'
    t = re.sub(r'(\d)~(\d)년', lambda m: D[int(m.group(1)) - 1] + D[int(m.group(2)) - 1] + ' 년', t)   # 2~3년 → 이삼 년, 3~4년 뒤 → 삼사 년 뒤
    t = re.sub(r'(\d+)~(\d+)(년|억)', r'\1\3에서 \2\3', t)
    t = re.sub(r'(\d+)억~(\d+)억', r'\1억에서 \2억', t)
    t = t.replace('4+2년', '사 플러스 이 년')
    t = re.sub(r'(\d+)살', lambda m: nat_full(m.group(1)) + ' 살', t)
    t = re.sub(r'(\d+)(명|건)', lambda m: nat_full(m.group(1)) + ' ' + m.group(2), t)
    t = re.sub(r'(\d+)도루', r'\1 도루', t)
    t = t.replace('비FA', '비에프에이').replace('FA', '에프에이').replace('OPS', '오피에스')
    t = re.sub(r'([ABC])등급', lambda m: {'A': '에이', 'B': '비', 'C': '씨'}[m.group(1)] + ' 등급', t)
    return t
