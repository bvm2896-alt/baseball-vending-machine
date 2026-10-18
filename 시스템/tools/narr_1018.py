# -*- coding: utf-8 -*-
"""롱폼⑱ 나레이션 앞처리 — narr_1016.pre 다음, gen_1015_long15.narr_of 앞에 돌린다."""
import re
NA = {1: '한', 2: '두', 3: '세', 4: '네', 5: '다섯', 6: '여섯', 7: '일곱', 8: '여덟', 9: '아홉'}
TN = {1: '열', 2: '스물', 3: '서른', 4: '마흔'}
def nat(n):
    n = int(n); t, u = divmod(n, 10)
    if n == 20: return '스무'
    return TN.get(t, '') + NA.get(u, '')
def pre(t):
    t = t.replace('10월', '시월')
    t = t.replace('3,600만 원', '삼천육백만 원').replace('1,200이닝', '천이백 이닝')
    t = re.sub(r'(\d+(?:\.\d+)?)%', r'\1 퍼센트', t)
    t = re.sub(r'(\d+)(홀드|타석|호|득점)', r'\1 \2', t)
    t = re.sub(r'(\d+)경기', lambda m: (nat(m.group(1)) if int(m.group(1)) < 50 else m.group(1)) + ' 경기', t)   # 22경기 = 스물두 경기
    t = t.replace('OPS', '오피에스')
    t = t.replace('KBO', '케이비오')
    return t
