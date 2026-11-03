
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
CH = [ch("롯데를 떠나는 사람", "n1", "n17"), ch("외국인 세 명의 거취", "f1", "f33"), ch("롯데에 들어오는 사람", "i1", "i18"), ch("2027년 롯데 예상", "p1", "q1")]
DESC = ("롯데 자이언츠 2027 스토브리그 — 2026년 64승 3무 77패 7위, 9년 연속 가을야구에 실패한 롯데의 겨울. 외국인 선수 레이예스·로드리게스·비슬리 재계약 전망과 떠나는 사람·들어오는 사람을 정리했어요.\n"
        "레이예스·로드리게스·비슬리는 2027년에도 롯데에 남을까요?\n\n"
        "떠나는 사람: 롯데는 3년 계약이 끝난 김태형 감독과 10월 24일 재계약하지 않기로 했어요(세 시즌 모두 7위). 롯데는 10월 7일 최충연·정성종·이인한 등 16명에게 재계약 불가를 알렸고, 김민성은 은퇴 뒤 곧바로 1군 내야 수비코치를 맡을 예정이에요. 2022년 겨울 170억 원에 데려온 유강남(4년 80억 원)·노진혁(4년 50억 원)·한현희(최대 40억 원)의 계약은 2026년으로 끝났고, 세 명 모두 FA 재자격을 얻지 못해 남으려면 일반 연봉 계약을 해야 해요.\n\n"
        "빅터 레이예스·엘빈 로드리게스·제레미 비슬리: 레이예스는 144경기 타율 3할 6푼 3리 211안타(KBO 한 시즌 최다) 18홈런 109타점, 3년 연속 안타왕, 세 시즌 600안타에 2026년 총액 140만 달러. 로드리게스는 29경기 159⅔이닝 10승 11패 평균자책점 4.28, 비슬리는 27경기 147이닝 10승 8패 평균자책점 4.96으로 둘 다 총액 100만 달러였어요. 외국인 3명 총액 한도는 400만 달러이고 재계약 연차마다 10만 달러씩 늘어나요 — 셋 다 재계약하면 2027년 한도는 제 계산으로 450만 달러, 2026년 총액 340만 달러보다 110만 달러 여유가 있어요. 아시아쿼터 이이무라 쇼타는 6월 7만 달러에 합류했어요.\n\n"
        "들어오는 사람: 제22대 이동욱 감독(3년 총액 20억 원, 계약금·연봉 5억 원)은 2020년 NC 통합 우승 감독으로 '스마트한 야구'와 수비를 내세웠고, 마무리 캠프는 11월 4일부터 일본 미야자키에서 수비 강화 캠프로 열려요. 새 단장은 현대·LG·히어로즈에서 1,621안타를 기록한 이택근, 1군엔 이동욱 감독에 허문회 수석코치·조원우 외야 수비코치까지 감독 출신이 세 명이에요. 2027 신인 드래프트 1라운드 전체 4순위는 서울디자인고 왼손 투수 박근서(188cm, 최고 149km).\n\n"
        "제 예상: 레이예스는 잔류 유력, 로드리게스는 잔류 쪽, 비슬리는 반반. 레이예스를 붙잡고, 외국인 투수 한 자리를 더 강하게 바꾸고, 170억 원 계약이 끝나 생긴 돈으로 수비 좋은 FA를 데려온다면 10년 만의 가을야구도 노려 볼 만하다고 봐요.\n\n"
        "야구자판기는 매일 야구 이슈를 정리해요. 2027년 롯데는 10년 만에 가을야구에 갈까요? 아니면 한 해 더 기다려야 할까요? 댓글로 알려 주세요.\n\n▶ 지난 영상: 2026 한국시리즈 예측 KT 삼성 · 롯데 새 감독 이동욱\n\n"
        "#롯데자이언츠 #롯데스토브리그 #레이예스 #이동욱 #로드리게스 #비슬리 #프로야구 #야구자판기\n")
TAGS = ["롯데 스토브리그", "롯데 2027", "롯데 자이언츠", "롯데 외국인 선수", "레이예스", "로드리게스", "비슬리", "이이무라", "이동욱 감독", "이택근 단장", "유강남", "김태형", "박근서", "프로야구", "KBO"]
SOURCE = "사실 출처 = 기사 원문 2곳 이상 — lt27/facts/facts_A.md, facts_B.md (머니투데이·SPOTV·OSEN·스포츠경향·엑스포츠뉴스·일간스포츠·마이데일리·데일리안·부산일보·STN·이데일리·스타뉴스·SBS·뉴시스)"
EP = {"theme": "m3", "introChapter": "오프닝", "date": "2026-11-04", "gameDate": "2026-11-04", "series": "야구롱폼", "focusTeam": "롯데", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1104-lt27-v1", "topic": "롯데2027스토브리그", "endcardSec": 10, "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "롯데 2027 스토브리그 | 레이예스·로드리게스·비슬리 남을까? 떠나는 사람·들어오는 사람 총정리", "description": DESC, "tags": TAGS, "hashtags": ["#롯데자이언츠", "#롯데스토브리그", "#레이예스", "#이동욱", "#로드리게스", "#비슬리", "#프로야구", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'q0', 'q1')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    # 11/3 낮 대사 고침(F-154): 줄을 빼고 더해 번호가 밀림 → 같은 대사의 옛 음성을 새 번호로 옮긴다(voiceRemap, 재합성 0)
    _vo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voice_old_1104.json')
    if os.path.exists(_vo):
        _old = json.load(open(_vo, encoding='utf-8'))
        EP['voiceRemap'] = [(_old.index(l['narr']) if l['narr'] in _old else None) for l in EP['lines']]
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-04_롱폼.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
