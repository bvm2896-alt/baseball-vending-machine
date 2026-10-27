# -*- coding: utf-8 -*-
"""10/28 새벽 롱폼㉜ 새판 콘티 — 사용자 "니가 영상 만들어 그냥"(Claude 분석 채팅). 영상 편집자 판(gen_1027_long32.py)을 그대로 실행하되
대사만 tools/text_1028_long32b.py 로 바꾸고, 새 줄 장면을 더하고, 안 쓰는 장면을 뺀다. 영상 편집자 판 파일은 건드리지 않는다.
바뀌지 않은 줄은 voiceFrom 으로 영상 편집자 판(2026-10-27_롱폼) 음성을 그대로 복사(새 줄만 합성).
실행: python -X utf8 tools/gen_1028_long32b.py  → episodes/2026-10-27_롱폼2.json"""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'gen_1027_long32.py'), encoding='utf-8').read()
src = src.replace("'text_1027_long32.py'", "'text_1028_long32b.py'")
_bn = "n = n.replace('볼넷', '볼 넷')"; assert _bn in src
src = src.replace(_bn, "n = n.replace('한 이닝', '한이닝')  # 10/28 사용자: '볼 넷'으로 끊지 말고 '볼넷' 붙여 읽기 · '한/이닝' 아니라 '한이닝'")
ADD = r'''
# ── 10/28 새판(Claude): 새 줄 장면 ──
K['h0'] = pv(CHW, "최형우", "42살 · 삼성 좌익수", [vstamp("홈런보다 송구", 3.0, "gold", size=56)], [st("포스트시즌", "역대 최고령 홈런", 1.0, hi=True)], team="삼성")
K['g6d'] = pv(OLL, "올러", "KIA 선발 · 2차전", [], [st("강판", "5회 도중", 0.3), st("남은 이닝", "불펜이 버팀", 2.0, hi=True)])
K['r13'] = tm("삼성", "2아웃 이후", "승부를 가른 순간", [], [st("삼성 · 3회말", "2아웃 뒤 4점", 2.0, hi=True), st("KIA · 7회초", "2아웃 1·3루 두 번 · 1점", 3.0)])
K['cB4'] = S(0, "faces", items=[dict(img=SRK2, name="시라카와", team="KIA", role="3차전 KIA 선발", at=0, say="5이닝만 버티면\n불펜 여유", sayAt=1.0)])
K['c12d'] = tm("KIA", "KIA 불펜", "3차전 변수", [vstamp("1차전처럼? 2차전처럼?", 1.0, "gold", size=50)], [])
K['c4a'] = pv(YHJ, "양현종", "KIA 투수 · 4차전", [vstamp("4차전 준비", 2.0, "gold", size=52)], [], imgAt=2.0)
K['c4b'] = pv(YHJ, "양현종", "KIA 투수 · 4차전", [], [st("올해 삼성전 · 광주", "두 번 다 1실점 이하", 3.0, hi=True)])
K['c4b2'] = pv(YHJ, "양현종", "KIA 투수 · 4차전", [], [st("2024 한국시리즈 2차전 · 광주", "5⅓이닝 1자책 승", 3.0)])
K['c4c2'] = pv(WTI3, "원태인", "삼성 투수", [], [st("올해 정규시즌", "7승 9패 · 평균자책점 4.52", 1.0)], team="삼성")
K['zT'] = pv(YHJ, "양현종", "KIA 투수 · 4차전", [vstamp("광주에서 끝낼 기회", 2.0, "gold", size=52)], [], imgAt=1.0)
K['c4c'] = pv(WTI3, "원태인", "삼성 투수", [], [st("4차전", "선발 복귀 가능", 1.0, hi=True)], team="삼성")
K['c4d'] = S(0, "duel", title="4차전 · 광주 맞대결?", left=dict(img=YHJ, name="양현종", team="KIA", role="4차전 KIA 선발", at=1.0), right=dict(img=WTI3, name="원태인", team="삼성", role="4차전 선발 가능", at=0), vsAt=1.2)
K['kS1'] = pv(ISMc, "이승민", "삼성 투수", [vstamp("삼성 키플레이어", 1.0, "gold", size=56)], [], team="삼성", imgAt=1.0)
K['kS3'] = S(0, "people", title="삼성 뒷문 · 3차전", items=[dict(img=KJY, name="김재윤", team="삼성", note="부상으로 빠짐", at=0), dict(img=WTIc, name="원태인", team="삼성", note="4차전 선발이면", at=1.0)], size=110)
K['kS2'] = pv(ISMc, "이승민", "삼성 투수", [], [st("2차전 7회", "2아웃 1·3루 · 삼진", 3.0, hi=True)], team="삼성", imgAt=3.0)
K['kS4'] = pv(ISMc, "이승민", "삼성 투수", [], [st("3차전 접전이면", "7회 · 8회", 2.0, hi=True)], team="삼성")
K['kK1'] = pv(PJH, "박재현", "KIA 1번 타자", [vstamp("KIA 키플레이어", 1.0, "gold", size=56)], [], imgAt=1.0)
K['kK2'] = pv(PJH, "박재현", "KIA 1번 타자", [], [st("삼성 선발 상대", "1회부터 출루", 2.0, hi=True)])
K['kK3'] = pv(PJH, "박재현", "KIA 1번 타자", [], [st("2차전 3회", "내야안타 · 첫 점 출발", 1.0), st("2차전 7회", "삼진", 3.0)])
K['kK4'] = S(0, "duel", title="3차전 1회 · 첫 승부", left=dict(img=PJH, name="박재현", team="KIA", role="1번 타자", at=1.0), right=dict(img=CWT2, name="최원태", team="삼성", role="삼성 선발", at=1.0), vsAt=1.2)
K['zP'] = tm("KIA", "제 예상", "3차전", [vstamp("KIA 승리", 1.0, "gold", size=60)], [st("이유", "세 가지", 2.0)])
K['z0'] = dict(K['z0'], title="둘째 · KIA 광주 가을야구", gat=[3.0, 3.1, 3.2, 3.3, 3.4], groups=[dict(g, at=(2.0 if i == 0 else 3.0)) for i, g in enumerate(K['z0']['groups'])])
K['z0a'] = S(0, "duel", title="첫째 · 선발 맞대결", left=dict(img=SRK2, name="시라카와", team="KIA", role="삼성에 강했던 선발", at=3.0), right=dict(img=CWT2, name="최원태", team="삼성", role="KIA에 약했던 선발", at=4.0), vsAt=3.5)
K['z0i'] = dict(K['z0i'], title="플레이오프 3차전 뒤")
K['zC'] = S(0, "people", title="셋째 · 삼성 뒷문", items=[dict(img=KJY, name="김재윤", team="삼성", note="부상으로 빠짐", at=2.0), dict(img=WTIc, name="원태인", team="삼성", note="3차전에 또 쓰면 4차전 부담", at=3.0)], size=110)
K['z0g'] = S(0, "duel", title="뒤집힐 조건", left=dict(img=SRK2, name="시라카와", team="KIA", role="초반에 흔들리면", at=1.0), right=dict(img=OLL, name="올러", team="KIA", role="2차전 3회말 4실점", at=3.0), vsAt=2.0)
K['zS'] = S(0, "question", text="제 예상\nKIA 4대2 승", logos=["KIA", "삼성"], logoSize=200, size=104)
for _k in [k for k in K if k not in KEYS]: K.pop(_k)
# 10/28 '2번에 선 / 이호연이' 로 끊으면서 이름 숨이 4로 밀림 → 사진도 4
K['p9']['items'][1]['at'] = 4.0

# 10/28 목차 읽기(오프닝 끝) — 첫 호흡부터 칸이 하나씩 켜짐
K['o6t'] = toc(-1, itemFrom=0)
# 10/28 사용자: 최형우 홈런 장면은 문장마다 쉬게 → 세 줄로 나누고 카드는 그대로 이어 감(cont)
_g9t = "다섯 번째 장면 · 7회말"
K['g9'] = S(0, "people", title=_g9t, items=[dict(img=CHW, name="최형우", team="삼성", note="솔로 홈런", at=1.0), dict(img=KBS, name="김범수", team="KIA", note="슬라이더", at=50)], size=110)
K['g9b'] = S(0, "people", title=_g9t, items=[dict(img=CHW, name="최형우", team="삼성", note="솔로 홈런", at=1.0), dict(img=KBS, name="김범수", team="KIA", note="슬라이더", at=0.0)], size=110, cont=True)
K['g9c'] = S(0, "people", title=_g9t, items=[dict(img=CHW, name="최형우", team="삼성", note="솔로 홈런", at=1.0), dict(img=KBS, name="김범수", team="KIA", note="슬라이더", at=0.0)], text="8대2", textAt=0.0, size=110, cont=True)
K['r10b'] = S(0, "people", title="KIA 불펜 · 2차전", items=[dict(img=LER, name="이의리", team="KIA", note="밀어내기 볼넷", at=1.0), dict(img=KBS, name="김범수", team="KIA", note="솔로 홈런", at=2.0)], size=110)

# ── 10/28 사용자 "텍스트로 구구절절 하지 말고 인포그래픽·모션으로": 글 카드(pstat) 구간을 그림 장면으로 ──
_RED, _GRY, _GRN = "#E0393E", "#AAB2BF", "#1F9D55"
# 시라카와
K['cB1'] = pv(SRK, "시라카와", "3차전 KIA 선발", [vstamp("가을 기세", 1.0, "gold", size=56)], [])
K['cB1b'] = S(0, "faces", items=[dict(img=KSY, name="이범호", team="KIA", role="KIA 감독 · 준PO 3차전 전", at=1.0, say="“빨리\n바꿀 수도”", sayAt=2.0)])
K['cB1c'] = S(0, "cells", title="준PO 3차전 · 시라카와", cols=9, cw=150, ch=120, items=[dict(t=f"{i}회", hi=i <= 5, on=i <= 5, at=(1.0 + (i - 1) * .12) if i <= 5 else 0, fs=40) for i in range(1, 10)], chain="srk9", center=None)
K['cB2'] = S(0, "tiles", title="준PO 3차전 · 아시아쿼터 첫 포스트시즌 승", items=[dict(v="없음", k="볼넷", at=0.0), dict(v="1", k="실점", at=0.4), dict(v="9", k="삼진", at=1.0, hi=True)])
K['cB2b'] = S(0, "bars", title="시라카와 평균자책점 · 낮을수록 좋음", items=[dict(label="올해 삼성전", sub="3경기 1승 1패", value=3.68, unit="", at=2.0, hi=True)], max=6, chain="srkb")
K['cB3'] = S(0, "bars", title="시라카와 평균자책점 · 낮을수록 좋음", items=[dict(label="올해 삼성전", sub="3경기 1승 1패", value=3.68, unit="", at=-1, hi=True), dict(label="정규시즌 전체", sub="18경기 4승 5패", value=4.75, unit="", at=2.0, color=_GRY)], max=6, chain="srkb", cont=True)
# 최원태
K['cD1'] = pv(CWT2, "최원태", "3차전 삼성 선발", [vstamp("KIA전 평균자책점 8점대", 3.0, "bad", size=50)], [], team="삼성")
_cw = [dict(d="2024년까지 가을", t="평균자책점\n11.16", c="bad"), dict(d="2025 준PO", t="6이닝\n무실점", c="good"), dict(d="2025 PO 2차전", t="7이닝\n1실점", c="good"), dict(d="2025 PO 5차전", t="3⅓이닝\n5실점", c="bad")]
K['cD2'] = S(0, "tline", title="최원태의 가을", items=[dict(_cw[0], at=2.0), dict(_cw[1], at=4.0), dict(_cw[2], at=6.0), dict(_cw[3], at=50)], chain="cwt")
K['cD3'] = S(0, "tline", title="최원태의 가을", items=[dict(_cw[0], at=-1), dict(_cw[1], at=-1), dict(_cw[2], at=-1), dict(_cw[3], at=1.0)], chain="cwt", cont=True)
# 최형우 말풍선: 카드 폭 안으로(말풍선이 넓으면 생겼다 사라질 때 카드가 옆으로 밀림) + 앞 말풍선은 그대로 남김
_pj = dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤")
_ch = dict(img=CHW2, name="최형우", team="삼성", role="삼성 좌익수")
_pjs = "“3차전에도\n좌익수로\n나가야 한다”"
# 10/28: 박진만 말 → 최형우 말로 넘어갈 때 박진만 카드가 사라지며 최형우 카드가 옆으로 미끄러지던 것 → 두 카드 그대로, 말풍선만 추가
_pj4 = dict(img=PJMc, name="박진만", team="삼성", role="삼성 감독 · 경기 뒤"); _pjs4 = "“최형우 선수의 호수비로\n팀 전체 분위기가\n확실하게 올라갔다”"
_ch4 = dict(img=CHW, name="최형우", team="삼성", role="삼성 좌익수 · 경기 뒤")
K['r4b'] = S(0, "faces", items=[dict(_pj4, at=0, say=_pjs4, sayAt=2.0), dict(_ch4, at=1.0)], chain="r4q")
K['r4d'] = S(0, "faces", items=[dict(_pj4, at=-1, say=_pjs4, sayAt=-1), dict(_ch4, at=-1, say="“말도 안 되게\n잘 갔다\n운 좋게 잡았다”", sayAt=2.0)], chain="r4q", cont=True)
K['c3e'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(_pj, at=50, say=_pjs, sayAt=50), dict(_ch, at=1.0)], chain="c3q")   # 10/28: 다음 장면 박진만 자리를 미리 잡아 둠 → 제목·최형우 카드가 안 움직임
K['c3f'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(_pj, at=0, say=_pjs, sayAt=2.0), dict(_ch, at=-1)], chain="c3q")
K['c3g'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(_pj, at=-1, say=_pjs, sayAt=-1), dict(_ch, at=-1, say="“감독님께\n전화 한번\n드려야겠다”", sayAt=1.0)], chain="c3q", cont=True)
K['c3h'] = S(0, "faces", title="3차전 · 삼성 쪽 변수", items=[dict(_pj, at=-1, say=_pjs, sayAt=-1), dict(_ch, at=-1, say="“단기전은\n실수 하나로\n승패가 갈린다”", sayAt=1.0)], chain="c3q", cont=True)
# 불펜
_bp = [dict(label="KIA · 1차전", team="KIA", sub="5명 4⅔이닝", value=0, unit="점", color=_GRN), dict(label="KIA · 2차전", team="KIA", sub="6회부터", value=3, unit="점", color=_RED), dict(label="삼성 · 1차전", team="삼성", sub="선발 강판 뒤", value=0, unit="점", color=_GRN), dict(label="삼성 · 2차전", team="삼성", sub="8회", value=1, unit="점", color=_RED)]
K['c12b'] = S(0, "question", text="불펜도 변수", logos=["KIA", "삼성"], logoSize=200, size=104)
K['c12c'] = S(0, "bars", title="불펜 실점 · 플레이오프", items=[dict(_bp[0], at=3.0), dict(_bp[1], at=5.0)], max=4, chain="bp")
K['c12c2'] = S(0, "bars", title="불펜 실점 · 플레이오프", items=[dict(_bp[0], at=-1), dict(_bp[1], at=-1), dict(_bp[2], at=2.0), dict(_bp[3], at=4.0)], max=4, chain="bp", cont=True)
K['c12d'] = S(0, "bars", title="불펜 실점 · 플레이오프", items=[dict(x, at=-1) for x in _bp], max=4, chain="bp", cont=True, text="1차전처럼? 2차전처럼?", textAt=0.5)
# 양현종
K['c4a'] = pv(YHJ, "양현종", "KIA 투수 · 4차전", [vstamp("4차전 준비", 2.0, "gold", size=52)], [], imgAt=2.0)
_yh = [dict(d="2024 한국시리즈 2차전", t="5⅓이닝\n1자책 승", c="good"), dict(d="올해 정규시즌", t="두 번 다\n1실점 이하", c="good")]
K['c4b'] = S(0, "tline", title="양현종 · 광주에서 삼성 상대", items=[dict(_yh[0], at=50), dict(_yh[1], at=3.0)], chain="yhj")
K['c4b2'] = S(0, "tline", title="양현종 · 광주에서 삼성 상대", items=[dict(_yh[0], at=2.0), dict(_yh[1], at=-1)], chain="yhj", cont=True)
# 원태인
K['c4c'] = pv(WTI3, "원태인", "삼성 투수", [vstamp("4차전 선발 복귀?", 1.0, "gold", size=52)], [], team="삼성")
K['c4c2'] = S(0, "tiles", title="원태인 · 올해 정규시즌", items=[dict(v="7승 9패", k="성적", at=1.0), dict(v="4.52", k="평균자책점", at=2.0)])
_wt = [dict(d="2024 한국시리즈 1차전", t="5이닝 무실점\n(비로 중단)", c="good"), dict(d="올해 KIA전", t="5⅔이닝\n6실점", c="bad")]
# 10/28: '광주에선 / 잘 던진 날도, / 무너진 날도 있었어요' — 말하는 호흡에 두 칸이 뜨고, 다음 두 줄은 그 칸을 짚기만
K['k2a'] = S(0, "tline", title="원태인 · 광주 등판", items=[dict(_wt[0], t="잘 던진 날", at=1.0), dict(_wt[1], t="무너진 날", at=2.0)], chain="wti")
K['k2b'] = S(0, "tline", title="원태인 · 광주 등판", items=[dict(_wt[0], t="잘 던진 날", at=-1), dict(_wt[1], at=2.0)], chain="wti", cont=True)
K['k2c'] = S(0, "tline", title="원태인 · 광주 등판", items=[dict(_wt[0], at=2.0), dict(_wt[1], at=-1)], chain="wti", cont=True)
'''
marker = "missing = [k for k in KEYS if k not in K]"
assert marker in src
src = src.replace(marker, ADD + marker, 1)
old_ch = src[src.index('CH = [_ch('):src.index('\n', src.index('CH = [_ch('))]
src = src.replace(old_ch, 'CH = [_ch("경기 전 수 싸움", "경기 전 수 싸움", "p0", "p9"), _ch("2차전 흐름", "2차전 흐름", "g0", "g12"), _ch("승부를 가른 이유", "승부를 가른 이유", "r0", "r13"), _ch("3차전 예상", "3차전 예상", "c0", "c4d"), _ch("3차전 키플레이어", "3차전 키플레이어", "k0", "kK4"), _ch("제 생각", "제 생각", "zt", "z1")]')
src = src.replace('"rev": "1027-long32-v1", "topic": "PO2차전리뷰", "endcardSec": 10,', '"rev": "1028-long32b-v1", "topic": "PO2차전리뷰새판", "endcardSec": 20,')
assert '"topic": "PO2차전리뷰새판"' in src
src = src.replace("os.path.join(OUT, '2026-10-27_롱폼.json')", "os.path.join(OUT, '2026-10-27_롱폼2.json')")
# voiceFrom: 영상 편집자 판과 대사가 같은 줄은 그 음성을 복사
VF = r'''
_so = importlib.util.spec_from_file_location('t32o', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'text_1027_long32.py'))
_oo = importlib.util.module_from_spec(_so); _so.loader.exec_module(_oo)
_old = {x[0]: i for i, x in enumerate(_oo.LINES)}
EP['voiceFrom'] = {'ep': '2026-10-27_롱폼', 'lines': [_old.get(t) for t in TEXT] + [len(_oo.LINES)]}
# 10/28 사용자("카드 안 인물을 가운데로", "사진 배치"): 가로 사진은 인물 중심으로 자른 세로 사진(_세로)을 쓴다 — 원본은 그대로
_V = ['김호령_만루포_0821_KIA제공', '박재현_주루_KIA제공', '박진만_박수_0908_삼성제공', '시라카와_투구_KIA제공', '양현종_글러브_1012_KIA제공', '올러_경기_KIA제공', '원태인_투구_0828_삼성제공', '이범호_박수_0915_KIA제공', '이의리_상체_KIA제공', '이호연_세리머니_KIA제공', '최원태_경기_삼성제공', '최형우_100타점_0918_삼성제공_중앙', '최형우_만루포미소_0826_삼성제공', '후라도_박수_삼성제공']
def _vert(o):
    if isinstance(o, dict): return {k_: _vert(v_) for k_, v_ in o.items()}
    if isinstance(o, list): return [_vert(v_) for v_ in o]
    if isinstance(o, str) and o.startswith('경기/') and o[3:] in _V: return o + '_세로'
    return o
EP['scenes'] = _vert(EP['scenes'])
# 10/28 사용자("가만히 있는 게 왜 움직여"): 템플릿이 장면마다 '보이는 내용 왼쪽 끝' 기준으로 가운데를 다시 맞춰서, 숨은 칸이 나타나면 전체가 옆으로 밀렸다 → 그림 장면은 그 재계산을 끈다(틀 자체가 가운데 정렬)
for _s in EP['scenes']:
    if _s.get('type') in ('tline', 'bars', 'cells', 'tiles', 'faces', 'rally'): _s['noCenter'] = True
# 10/28 사용자("이승민이에요 끝나자마자 다음 장면"): 키플레이어를 밝히는 줄 뒤엔 화면을 잠깐 잡아 둔다
for _i, _t in enumerate(TEXT):
    if _t.startswith(('삼성 키플레이어는', 'KIA 키플레이어는')): EP['lines'][_i]['holdAfter'] = 1.2
'''
src = src.replace("\nif __name__ == '__main__':", "\nimport importlib.util\n" + VF + "\nif __name__ == '__main__':", 1)
__file__ = os.path.join(HERE, 'gen_1027_long32.py')
exec(compile(src, os.path.join(HERE, 'gen_1028_long32b.py'), 'exec'), {'__name__': '__main__', '__file__': os.path.join(HERE, 'gen_1027_long32.py')})
