
for _k in [k for k in SC if k not in KEYS]: SC.pop(_k)
missing = [k for k in KEYS if k not in SC]; extra = [k for k in SC if k not in KEYS]
assert not missing and not extra, (missing, extra)
lines, scenes = [], []
for j, (k, narr, sub) in enumerate(_t.LINES):
    sc = dict(SC[k]); sc['startLine'] = j
    lines.append(L(narr, sub)); scenes.append(sc)
lines.append({"narr": END, "sub": "채널 구독하고\n매일 야구 이슈 받아보세요!", "rate": 1.0})
scenes.append(dict(END_SC, startLine=len(lines) - 1))

def ch(title, a, b): return {"key": title, "title": title, "from": KEYS.index(a), "to": KEYS.index(b)}
CH = [ch("역대 1위 팀의 한국시리즈", "h1", "h15"), ch("2026년 KT", "k1", "k17"), ch("삼성의 남은 힘", "s1", "s17"), ch("차전별 맞대결", "v1", "v12"), ch("KT 우승 확률", "p1", "q2")]
DESC = ("2026 한국시리즈 KT 삼성 우승 예측 — 1차전부터 7차전까지 경기별 KT 승리 확률로 계산한 KT 통합 우승 확률은 51.33%예요.\n"
        "정규시즌 1위 KT는 22일 만의 공식 경기를 딛고 통합 우승을 할 수 있을까요? 플레이오프 5차전을 뚫고 온 삼성은 1위 팀을 넘을 수 있을까요?\n\n"
        "역대 1위 팀의 한국시리즈: 2005~2025년 정규시즌 1위 팀은 21번 중 19번 우승. 우승을 놓친 2015년 삼성·2018년 두산은 모두 플레이오프 5차전을 치르고 하루 쉰 상대에게 안방 1·2차전을 1승 1패로 나눴고 3차전부터 무너졌어요. 안방 1·2차전을 다 이긴 1위 팀은 10번 모두 우승.\n\n"
        "2026년 KT: 90승 5무 49패 구단 최다승, 팀 타율·득점 1위, 팀 평균자책점 2위, 팀 홈런은 7위, 홀드 1위 스기모토 평균자책점 5.90. 고영표 다승 1위·소형준 승률 1위, 1차전 선발 유력 대니엘은 첫 포스트시즌. 선발 넷이 나흘씩 쉬며 7차전까지 돌 수 있는 일정. 큰 경기 경험은 김현수(한국시리즈 반지 세 개).\n\n"
        "삼성의 남은 힘: 정규시즌 맞대결 삼성 9승 7패. 세이브왕 김재윤 부상으로 원태인이 마무리, 선발은 최원태·페덱·후라도 셋 — 대구 3~5차전 사흘 연속이라 4차전부터 사흘 휴식.\n\n"
        "차전별 맞대결: 대니엘은 삼성전 등판 없음, 최원태 KT전 평균자책점 6.94, 삼성 중심 타선(구자욱·디아즈·최형우) 모두 왼손 — 사이드암 고영표 삼성전 3승 1패 2.25, 페덱 8월 29일 KT전 6이닝 무실점. 후라도 KT전 5.17, 힐리어드 삼성전 3할 4리 5홈런.\n\n"
        "제 계산: 출발점 43.75%(맞대결 7승 9패)에 수원 +4·대구 −4, 1차전 공백 −5, 삼성 불펜 피로 +2(1·2차전), 세이브왕 공백 +3, 삼성 선발 사흘 휴식 +6(4차전부터).\n"
        "1차전 47.75% · 2차전 52.75% · 3차전 42.75% · 4·5차전 48.75% · 6·7차전 56.75% → KT 우승 51.33%, 삼성 48.66%. 가장 가능성 높은 결과는 KT 4승 3패. 수원 2연승이면 82.35%, 1승 1패면 51.41%, 2연패면 19.52%.\n\n"
        "KT가 22일 만의 공식 경기를 딛고 통합 우승을 할까요? 아니면 플레이오프를 뚫고 올라온 삼성이 KT를 넘을까요? 댓글로 알려 주세요.\n\n▶ 지난 영상: 한국시리즈 1차전 예측 KT 삼성 · 플레이오프 5차전 리뷰\n\n"
        "#한국시리즈 #한국시리즈예측 #KT위즈 #삼성라이온즈 #KT우승 #고영표 #프로야구 #야구자판기\n")
TAGS = ["한국시리즈 예측", "한국시리즈 우승", "한국시리즈", "KT 위즈", "삼성 라이온즈", "KT 우승 확률", "이강철", "힐리어드", "대니엘", "고영표", "후라도", "원태인", "김현수", "프로야구", "KBO"]
SOURCE = "사실 출처 = KBO 기록실 + 기사 원문 — /home/claude/ks35/research, /home/claude/g5/research_*.md, 롱폼㉝ 근거모음"
EP = {"introChapter": "오프닝", "date": "2026-11-02", "gameDate": "2026-11-03", "series": "야구롱폼", "focusTeam": "KT", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1102-long35-v3", "topic": "KS예측_KT우승확률", "endcardSec": 20, "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "2026 한국시리즈 예측 KT 삼성 우승 확률 | 후라도·힐리어드, 경기별로 계산해 보니", "description": DESC, "tags": TAGS, "hashtags": ["#한국시리즈", "#한국시리즈예측", "#KT위즈", "#삼성라이온즈", "#KT우승", "#고영표", "#프로야구", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'q1', 'q2')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-02_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
