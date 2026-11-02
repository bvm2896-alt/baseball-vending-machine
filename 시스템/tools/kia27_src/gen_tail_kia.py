
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
CH = [ch("기아를 떠나는 사람", "n1", "n16b"), ch("남을지 모르는 외국인 세 명", "f1", "f32b"), ch("기아에 들어오는 사람", "i1", "i9"), ch("2027년 기아 예상", "p1", "q1")]
DESC = ("기아 타이거즈 2027 스토브리그 — 2026년 플레이오프에서 삼성에 2승 3패로 탈락한 기아의 겨울, 외국인 선수 카스트로·네일·올러 재계약 전망과 떠나는 사람·들어오는 사람을 정리했어요.\n"
        "카스트로·네일·올러는 2027년에도 기아에 남을까요?\n\n"
        "떠나는 사람: 기아는 10월 23일 고종욱·이창진·홍건희·김사윤·김대유·윤중현과 2027년 재계약을 하지 않기로 했어요. 정해영·한재승·윤도현은 12월 상무에 입대해 2028년 6월 돌아오고, 포수 김태군·중견수 김호령은 FA 자격 취득이 유력해요. 김선빈의 3년 30억 원 계약도 2026년으로 끝나요. 2025년 겨울엔 박찬호(두산 4년 80억 원)·최형우(삼성 2년 26억 원)·한승택(KT 4년 10억 원)이 떠났어요.\n\n"
        "해럴드 카스트로·제임스 네일·아담 올러: 카스트로는 99경기 타율 3할 2푼 7리 21홈런 88타점에 2026년 총액 100만 달러. 네일은 31경기 13승 평균자책점 3.49에 총액 200만 달러, 올러는 11승 평균자책점 3.13에 총액 120만 달러. 외국인 3명 계약 총액 한도는 400만 달러이고 재계약 연차마다 선수당 10만 달러씩 늘어나요 — 규정대로 계산하면 2026년 한도는 430만 달러, 셋 다 재계약하면 2027년 한도는 최대 460만 달러예요. 아시아쿼터 시라카와 케이쇼도 재계약 대상이에요.\n\n"
        "들어오는 사람: 2027 신인 드래프트 1라운드 전체 3순위 경남고 내야수 이호민.\n\n"
        "제 예상: 카스트로는 잔류 유력, 네일은 몸값이 관건, 올러는 반반. 셋 중 한 명만 바뀐다면 올러일 가능성이 가장 커요. 김도영은 빠르면 2028시즌 뒤 메이저리그에 도전할 수 있어서, 2027·2028년이 김도영과 함께 우승을 노릴 가장 확실한 두 시즌이라고 봐요.\n\n"
        "야구자판기는 매일 야구 이슈를 정리해요. 카스트로·네일·올러, 셋 다 남을까요? 아니면 한 명 이상 바뀔까요? 댓글로 알려 주세요.\n\n▶ 지난 영상: \n\n"
        "#기아타이거즈 #기아스토브리그 #카스트로 #제임스네일 #올러 #김도영 #프로야구 #야구자판기\n")
TAGS = ["기아 스토브리그", "기아 2027", "기아 타이거즈", "KIA 타이거즈", "기아 외국인 선수", "카스트로", "제임스 네일", "올러", "김도영", "김호령", "김태군", "이호민", "이범호", "프로야구", "KBO"]
SOURCE = "사실 출처 = 기사 원문 2곳 이상 — /home/claude/kia27/facts_A.md, facts_B.md (일간스포츠·스포츠경향·OSEN·스타뉴스·엑스포츠뉴스·SPOTV·뉴시스·파이낸셜뉴스·데일리안·마이데일리)"
EP = {"theme": "m3", "introChapter": "오프닝", "date": "2026-11-02", "gameDate": "2026-11-02", "series": "야구롱폼", "focusTeam": "KIA", "speed": 1.0, "ttsApi": True, "ttsTempo": 1.2, "ttsTempoSlow": 1.15,
      "rev": "1102-kia27-v1", "topic": "기아2027스토브리그", "endcardSec": 20, "gapScale": 0.85, "pauseMax": 0.3, "ttsCharsOk": 6000,
      "chapters": CH, "lines": lines, "scenes": scenes, "thumb": {}, "mascot": False, "source": SOURCE,
      "youtube": {"title": "기아 2027 스토브리그 | 카스트로·네일·올러 남을까? 떠나는 사람·들어오는 사람 총정리", "description": DESC, "tags": TAGS, "hashtags": ["#기아타이거즈", "#기아스토브리그", "#카스트로", "#제임스네일", "#올러", "#김도영", "#프로야구", "#야구자판기"]}}

if __name__ == '__main__':
    SLOW = {KEYS.index(k) for k in ('o1', 'q1')}
    for i, l in enumerate(EP['lines'][:-1]):
        if i in SLOW: l['pace'] = 'slow'
    lines[-2]['gapAfter'] = 0.4
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(OUT, '2026-11-02_롱폼2.json')
    json.dump(EP, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tot = sum(len(l['narr'].replace(' / ', ' ')) for l in EP['lines'][:-1])
    print('ok', out, len(EP['lines']), '줄', len(EP['scenes']), '장면', '합성 글자', tot)
