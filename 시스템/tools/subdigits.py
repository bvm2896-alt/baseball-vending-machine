# -*- coding: utf-8 -*-
"""나레이션(한글 숫자 읽기) → 자막(아라비아 숫자). 9/22 사용자 지시 '자막은 나레이션대로' 의 자막 쪽.
규칙: 나레이션 문장은 그대로 두고 숫자 읽기만 숫자로 바꾼다. 애매한 건(이 경기, 이 대회…) 바꾸지 않는다."""
import re

SINO = {'영': 0, '일': 1, '이': 2, '삼': 3, '사': 4, '오': 5, '육': 6, '칠': 7, '팔': 8, '구': 9}
def sino(s):
    """'이십육' → 26, '십삼' → 13, '백이십팔' → 128"""
    total, cur = 0, 0
    for ch in s:
        if ch in SINO: cur = SINO[ch]
        elif ch == '십': total += (cur or 1) * 10; cur = 0
        elif ch == '백': total += (cur or 1) * 100; cur = 0
        elif ch == '천': total += (cur or 1) * 1000; cur = 0
        else: return None
    return total + cur
NAT10 = {'열': 10, '스물': 20, '스무': 20, '서른': 30, '마흔': 40, '쉰': 50, '예순': 60, '일흔': 70, '여든': 80, '아흔': 90}
NAT1 = {'영': 0, '한': 1, '하나': 1, '두': 2, '둘': 2, '세': 3, '셋': 3, '네': 4, '넷': 4, '다섯': 5, '여섯': 6, '일곱': 7, '여덟': 8, '아홉': 9}
def native(s):
    """'열다섯' → 15, '스물한' → 21, '서른네' → 34, '두' → 2"""
    for k, v in sorted(NAT10.items(), key=lambda kv: -len(kv[0])):
        if s.startswith(k):
            rest = s[len(k):]
            if rest == '': return v
            if rest in NAT1: return v + NAT1[rest]
            return None
    return NAT1.get(s)

SINO_RE = r'[영일이삼사오육칠팔구십백천]+'
NAT_RE = r'(?:열|스물|스무|서른|마흔|쉰|예순|일흔|여든|아흔)?(?:영|한|하나|두|둘|세|셋|네|넷|다섯|여섯|일곱|여덟|아홉)?'
SINO_UNITS = '회|승|패|무|위|이닝|년|일|월|구|점|실점|득점|타점|연승|연패|연전|라운드|번째|시즌|호|번|개'
NAT_UNITS = '개|명|점|타점|안타|타수|경기|시|번|살|방|가지|게임|장|이닝|골|타석'

def to_digits(t):
    # 0) 고유명사
    t = t.replace('케이비오', 'KBO').replace('에이조', 'A조').replace('비조', 'B조').replace('에네오스', 'ENEOS').replace('엘지', 'LG').replace('케이티', 'KT').replace('엔씨', 'NC').replace('에스에스지', 'SSG')
    # 1) 점수 'X 대 Y' (둘 다 한자어) — '이 대회' 를 피하려고 뒤에도 숫자 읽기가 있어야 한다
    def score(m):
        g2, tail = m.group(2), ''
        if len(g2) > 1 and g2[-1] == '이' and g2[-2] not in '십백천' and sino(g2[:-1]) is not None:  # '영이 슈퍼라운드' 의 '이' 는 조사(십이=12 는 숫자)
            g2, tail = g2[:-1], '이'
        a, b = sino(m.group(1)), sino(g2)
        return f'{a}-{b}{tail}' if a is not None and b is not None else m.group(0)
    t = re.sub(rf'(?<![가-힣])({SINO_RE}) 대 ({SINO_RE})', score, t)
    # 2) 고유어 수 + 단위 (열다섯 점, 스물한 명, 두 개, 세 점)
    def nat(m):
        n = native(m.group(1))
        if n is None or m.group(1) == '': return m.group(0)
        if m.group(1) == '한' and m.group(2) == '번': return m.group(0)
        if m.group(2) == '번' and t[m.end():m.end() + 1] == '째': return m.group(0)  # '두 번째' 는 그대로
        return f'{n}{m.group(2)}'
    t = re.sub(rf'(?<![가-힣])({NAT_RE}) ({NAT_UNITS})', nat, t)
    # 3) 한자어 수 + 단위 (칠 회, 이십오 일, 사 이닝, 십사 승)
    def sn(m):
        n = sino(m.group(1))
        if n is None: return m.group(0)
        nxt = t[m.end():m.end() + 1]
        if m.group(2) == '일' and nxt and '가' <= nxt <= '힣' and nxt not in '에까부이': return m.group(0)  # '이 일본' 보호
        return f'{n}{m.group(2)}'
    t = re.sub(rf'(?<![가-힣])({SINO_RE}) ({SINO_UNITS})', sn, t)
    # 3-2) 매직넘버 뒤 한자어 수 (9/23 사용자 지시: 매직넘버는 '십일'로 읽는다) — 십일이에요 → 11이에요, 구예요 → 9예요
    t = re.sub(r'(매직넘버(?:는|가|도)? )([영일이삼사오육칠팔구십]+?)(이에요|예요|이면|면)(?![가-힣])',
               lambda m: m.group(1) + (str(sino(m.group(2))) if sino(m.group(2)) is not None else m.group(2)) + m.group(3), t)
    # 4) 달 이름 (구월 → 9월, 시월 → 10월)
    MONTH = {'일월': 1, '이월': 2, '삼월': 3, '사월': 4, '오월': 5, '유월': 6, '칠월': 7, '팔월': 8, '구월': 9, '시월': 10, '십일월': 11, '십이월': 12}
    t = re.sub(r'(?<![가-힣])(십일월|십이월|일월|이월|삼월|사월|오월|유월|칠월|팔월|구월|시월)(?![가-힣])', lambda m: f'{MONTH[m.group(1)]}월', t)
    # 5) 단위 없이 문장을 맺는 고유어 수 (매직넘버가 열하나예요 → 11이에요, 아홉이면 → 9면)
    def bare(m):
        n = native(m.group(1))
        if n is None or n < 2: return m.group(0)
        suf = m.group(2).replace('예요', '이에요')
        return f'{n}{suf}'
    t = re.sub(rf'(?<![가-힣])({NAT_RE})(이에요|예요|이면|이라|이고|이니|이었|이지|이야)', bare, t)
    return t

if __name__ == '__main__':
    import sys
    for line in sys.stdin.read().split('\n'):
        print(to_digits(line))
