/* @@FACEX1101 11/1 20:17 사용자 "사진 무조건 가운데로 잘 맞춰" — 사진마다 얼굴 가로 위치(0~1)·원본 크기. cover 로 자를 때 얼굴이 칸 가운데 오게 object-position x 를 계산한다 */
const FACEX = {"경기/구자욱_적시타세리머니_스타뉴스": [0.45, 1200, 1557], "경기/김도영_덕아웃_KIA제공": [0.43, 1200, 800], "경기/김재윤_투구_1007_삼성제공": [0.48, 1200, 911], "경기/나성범_세리머니_KIA제공": [0.48, 1200, 800], "경기/대니엘_역투_스포츠경향": [0.55, 1200, 911], "경기/대니엘_주먹_KT제공": [0.41, 647, 911], "경기/디아즈_경기_삼성제공": [0.5, 1200, 825], "경기/박재현_주루_KIA제공": [0.42, 1200, 800], "경기/박진만_박수_0908_삼성제공": [0.38, 1200, 1100], "경기/스기모토_역투_스포츠경향": [0.28, 1200, 911], "경기/양현종_글러브_1012_KIA제공": [0.48, 1280, 853], "경기/올러_경기_KIA제공_세로": [0.46, 640, 801], "경기/원태인_역투_삼성제공": [0.68, 640, 911], "경기/원태인_투구_0828_삼성제공_세로": [0.5, 682, 853], "경기/원태인_포효_스타뉴스": [0.52, 1200, 911], "경기/이강철_덕아웃_KT제공": [0.45, 1200, 911], "경기/이강철_상체_스포츠조선": [0.41, 1200, 911], "경기/이범호_박수_0915_KIA제공_세로": [0.36, 588, 736], "경기/최원준_204안타_1007_KT제공": [0.45, 647, 967], "경기/최원준_역전타_KT제공": [0.62, 1200, 800], "경기/최원태_경기_삼성제공_세로": [0.44, 640, 800], "경기/최형우_100타점_0918_삼성제공_중앙_세로": [0.53, 852, 1066], "경기/최형우_만루포미소_0826_삼성제공_세로": [0.57, 640, 800], "경기/카스트로_엄지_0810_KIA제공": [0.45, 983, 1475], "경기/페덱_포효_연합뉴스": [0.47, 1200, 810], "경기/페덱_환호_삼성제공": [0.52, 1280, 1822], "경기/한준수_주루_KIA제공": [0.43, 1200, 800], "경기/후라도_경기_1019_삼성제공": [0.43, 1200, 800], "경기/후라도_경기_삼성제공": [0.7, 640, 427], "경기/후라도_박수_삼성제공_세로": [0.53, 729, 912], "경기/힐리어드_포효_KT제공_1280": [0.61, 1280, 853], "경기/힐리어드_하이파이브_1011_KT제공": [0.28, 1200, 800], "상황별/강민호_3점포_중앙": [0.5, 460, 500], "상황별/김지찬_상체": [0.59, 520, 728], "상황별/김지찬_홈충돌": [0.4, 1280, 853], "상황별/박승규_타격_0830_삼성제공": [0.47, 626, 911], "상황별/이재현_상체": [0.34, 520, 728], "상황별/최원태_KIA전_0908_삼성제공": [0.68, 465, 698], "카드/FA9_디아즈_경기": [0.54, 639, 825], "카드/FA9_후라도": [0.5, 325, 419], "카드/FA9원_대니엘": [0.5, 460, 460], "카드/G18_강민호_포수": [0.47, 780, 1000], "카드/G18_디아즈_B": [0.57, 330, 427], "카드/G18_류지혁_A": [0.5, 535, 691], "카드/G18_최형우_미소": [0.47, 624, 800], "카드/P17_김선빈": [0.61, 567, 733], "카드/P18_올러_투구": [0.61, 579, 747], "카드/P18_한준수_세리머니": [0.55, 558, 721], "카드/P20_후라도_투구": [0.6, 660, 854], "카드/P22_하주석_타격": [0.57, 420, 542], "카드/P31_이승민_삼성제공": [0.54, 1000, 1340], "경기/페덱_사용자제공_1004": [0.47, 620, 775], "경기/최원준_두검지_1006_KT제공": [0.36, 850, 900], "경기/힐리어드_하늘가리키기_KT제공": [0.47, 1200, 1799]};
let __FXS = null;
function __faceFix() {
  try {
    if (!__FXS) { __FXS = {}; Object.keys(FACEX).forEach(k => { const s_ = photoSrc(k); if (s_) __FXS[s_] = FACEX[k]; }); }
    document.querySelectorAll('img').forEach(im => {
      const f = __FXS[im.getAttribute('src')]; if (!f || im.dataset.nofx) return;
      const cs = getComputedStyle(im); if (cs.objectFit !== 'cover') return;
      const w = im.clientWidth, h = im.clientHeight; if (!w || !h) return;
      const [fx, W, H] = f, sc = Math.max(w / W, h / H), W2 = W * sc;
      if (W2 - w < 2) return;
      const px = Math.max(0, Math.min(1, (fx * W2 - w / 2) / (W2 - w)));
      const cur = (im.style.objectPosition || cs.objectPosition || '50% 12%').split(/\s+/);
      im.style.objectPosition = `${(px * 100).toFixed(1)}% ${cur[1] || '12%'}`;
    });
  } catch (e) {}
}
/* 11/1 22:04 사용자 "제목이 점점 위로 올라가" — 장면마다 본문 높이에 따라 가운데 맞춤되면서 제목 높이가 달라짐 → 장면 제목(s.title)을 언제나 같은 높이(TITLE_Y)에 둔다. 아래 자막 칸을 넘으면 그만큼만 덜 옮긴다 */
const TITLE_Y = 172, BOTTOM_MAX = 935;
function __titleFix(s) {
  try {
    if (!s || !s.title) return;
    const body = document.getElementById('body'); if (!body) return;
    const el = body.firstElementChild; if (!el) return;
    el.style.translate = '';
    const want = String(s.title).replace(/\s+/g, ' ').trim();
    const t = [...body.querySelectorAll('.title')].find(x => x.textContent.replace(/\s+/g, ' ').trim() === want);
    if (!t) return;
    const r = t.getBoundingClientRect(), br = el.getBoundingClientRect();
    let dy = TITLE_Y - r.top;
    let bottom = 0; el.querySelectorAll('*').forEach(c => { if (c.children.length && c.tagName !== 'svg') return; const q = c.getBoundingClientRect(); if (q.height > 0 && q.bottom > bottom && q.bottom < 1080) bottom = q.bottom; });
    if (Math.abs(dy) > 0.5) el.style.translate = `0 ${dy.toFixed(1)}px`;
  } catch (e) {}
}

/* 11/1 22:50 사용자 "한 장면에 같은 팀 로고는 한 번" — 그린 뒤 #body 안 같은 구단 로고는 문서 순서 첫 개만 남김(연도별 칸 grid·질문 장면 제외) */
function __logoDedup(s) {
  try {
    if (!s || ['grid', 'question', 'matchup', 'mu_blocks'].includes(s.type)) return;
    /* 11/3 0시 검수: 여러 사람 카드(faces·people)에서 첫 사람 이름 옆에만 로고가 남던 것(11/2 사용자 '카스트로 이름 옆에만 로고… 없애') → 같은 구단 로고가 두 개 이상이면 모두 뺀다 */
    if (s.type === 'faces' || s.type === 'people') { const L0 = Object.values(LOGO || {}), cnt = {}; const ims = [...document.querySelectorAll('#body img')].filter(e => L0.includes(e.getAttribute('src')));
      ims.forEach(e => { const k = e.getAttribute('src'); cnt[k] = (cnt[k] || 0) + 1; }); ims.forEach(e => { if (cnt[e.getAttribute('src')] > 1) e.style.display = 'none'; }); return; }
    const L = Object.values(LOGO || {}), seen = new Set();
    document.querySelectorAll('#body img').forEach(e => { const src = e.getAttribute('src'); if (!L.includes(src)) return;
      if (seen.has(src)) e.style.display = 'none'; else seen.add(src); });
  } catch (e) {}
}
