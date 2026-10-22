# -*- coding: utf-8 -*-
"""10/20 롱폼㉑ 나레이션 앞·뒤처리 (gen_1015 narr_of 전후)."""
import re
AGE = {'45살': '마흔다섯 살', '38살': '서른여덟 살', '39살': '서른아홉 살', '33살': '서른세 살', '29살': '스물아홉 살',
       '22살': '스물두 살', '24살': '스물네 살', '26살': '스물여섯 살', '35살': '서른다섯 살', '25살': '스물다섯 살'}
def pre(t):
    for a, b in AGE.items(): t = t.replace(a, b)
    t = t.replace('6개월', '육 개월').replace('4개월', '사 개월').replace('2주', '이 주').replace('3곳', '세 곳').replace('6시즌', '여섯 시즌')
    t = t.replace('120경기', '백이십 경기').replace('297경기', '이백구십칠 경기').replace('54경기', '오십사 경기')
    t = re.sub(r'(\d+)(라운드|홀드)', lambda m: m.group(1) + ' ' + m.group(2), t)
    t = re.sub(r'(\d)군', r'\1 군', t)
    t = t.replace('KBO', '케이비오').replace('FA', '에프에이').replace('SNS', '에스엔에스')
    return t
def post(t):
    t = t.replace('육 월', '유월').replace('십 월', '시월')
    return t
