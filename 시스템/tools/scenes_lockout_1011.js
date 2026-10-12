/* @@LOCK1011 */
/* lockout (10/11 롱폼⑪, 사용자 "직장폐쇄가 뭔지 그림이 이해 안 돼 · 예시를 모션그래픽으로"):
   mode "cba"    — 구단주 카드 ↔ 노사협약 계약서(규칙 칩 연봉·FA·트레이드) ↔ 선수노조 카드, 아래 체결·만료 타임라인.
   mode "lock"   — 위: 파업(선수가 나감) vs 직장폐쇄(구단주가 문 잠금) 비교 / 아래: FA 투수가 구장으로 걸어가다 자물쇠에 막힘 → 전화 ✗ 사인 ✗ → '새 협약 서명' 도장 → 문 열림.
   mode "branch" — 협약 만료 → ① 옛 협약대로 협상 계속 ② 직장폐쇄(구단주의 선택 · 협상 카드), '자동 ✗'.
   콘티: {"type":"lockout","mode":"cba|lock|branch","title":"…","at":{키:호흡}} — at 이 없으면 아래 기본값. 시간은 lt(장면 시작 기준 초)·호흡(pk)으로만. */
(() => {
  const V = () => !!EP.vertical;
  const bld = c => `<svg viewBox="0 0 120 100" width="100%" height="100%"><rect x="10" y="30" width="100" height="66" rx="8" fill="${c}"/><rect x="26" y="12" width="68" height="24" rx="6" fill="${c}"/>${[0, 1, 2].map(i => [0, 1].map(j => `<rect x="${24 + i * 28}" y="${42 + j * 24}" width="16" height="14" rx="3" fill="#fff" opacity=".9"/>`).join('')).join('')}</svg>`;
  const gate = (c, open) => `<svg viewBox="0 0 260 200" width="100%" height="100%"><path d="M10,196 v-110 q120,-80 240,0 v110 z" fill="${c}"/><rect x="20" y="40" width="220" height="22" rx="8" fill="#fff" opacity=".25"/><path d="M95,196 v-70 a35,35 0 0 1 70,0 v70 z" fill="${open ? '#CFF5DA' : '#12161F'}" opacity="${open ? 1 : .85}"/>${open ? '' : `<rect x="128" y="130" width="4" height="60" fill="#fff" opacity=".35"/>`}</svg>`;
  const lockSvg = (c, open) => `<svg viewBox="0 0 200 150" width="100%" height="100%"><path d="${open ? 'M62,70 v-22 a38,38 0 0 1 76,0 v8' : 'M62,70 v-22 a38,38 0 0 1 76,0 v22'}" fill="none" stroke="${c}" stroke-width="12" stroke-linecap="round"/><rect x="44" y="66" width="112" height="76" rx="16" fill="${c}"/><circle cx="100" cy="100" r="11" fill="#fff"/><rect x="95" y="104" width="10" height="20" rx="4" fill="#fff"/></svg>`;
  const key = c => `<svg viewBox="0 0 120 60" width="100%" height="100%"><circle cx="24" cy="30" r="18" fill="none" stroke="${c}" stroke-width="10"/><rect x="40" y="25" width="70" height="10" rx="4" fill="${c}"/><rect x="84" y="33" width="8" height="16" rx="3" fill="${c}"/><rect x="100" y="33" width="8" height="20" rx="3" fill="${c}"/></svg>`;
  const phone = c => `<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M30,10 q-14,2 -16,16 q4,40 44,60 q14,6 30,-6 l-14,-18 q-6,-4 -12,0 l-6,6 q-16,-10 -22,-28 l8,-6 q4,-6 0,-12 z" fill="${c}"/></svg>`;
  const pen = c => `<svg viewBox="0 0 100 100" width="100%" height="100%"><path d="M18,82 l8,-26 l46,-46 l18,18 l-46,46 z" fill="${c}"/><path d="M18,82 l26,-8 l-18,-18 z" fill="#fff" opacity=".6"/><rect x="10" y="88" width="80" height="6" rx="3" fill="${c}"/></svg>`;
  const chip = (t, c, p, sz = 36) => `<div class="badge" style="background:${c};color:#fff;font-size:${sz}px;padding:10px 26px;white-space:nowrap;${pop(p)}">${esc(t)}</div>`;
  const xmark = (p, sz = 90) => `<div style="position:absolute;left:50%;top:50%;width:${sz}px;height:${sz}px;translate:-50% -50%;${pop(p)}"><svg viewBox="0 0 100 100" width="100%" height="100%"><circle cx="50" cy="50" r="46" fill="${RED}"/><path d="M30,30 L70,70 M70,30 L30,70" stroke="#fff" stroke-width="14" stroke-linecap="round"/></svg></div>`;
  const label = (t, c, p, sz = 44) => `<div style="font-size:${sz}px;font-weight:900;letter-spacing:-1.5px;line-height:1.22;text-align:center;color:${c};white-space:nowrap;${pop(p)}">${br(t)}</div>`;
  const card = (inner, c, p, w) => `<div class="col" style="width:${w}px;background:${c}10;border:5px solid ${c};border-radius:36px;padding:26px 24px 28px;gap:14px;align-items:center;${pop(p)}">${inner}</div>`;
  const persons = (n, c, p, w = 52, h = 78) => `<div class="row" style="gap:6px;justify-content:center">${Array.from({ length: n }, (_, m) => `<div style="width:${w}px;height:${h}px;${pop(c01(p * 3 - m * .25))}">${ICON.person(c)}</div>`).join('')}</div>`;
  const P = (s, k, lt, fb) => pk(s, (s.at || {})[k] != null ? s.at[k] : fb, .45, seg(lt, .2 + fb * .35, .45));

  SCENE.lockout = (lt, s) => {
    const mode = s.mode || 'lock', CW = V() ? 300 : 440;
    let h = titleH(lt, s, 52, 24);
    if (mode === 'cba') {
      const pO = P(s, 'owners', lt, 0), pU = P(s, 'union', lt, 0), pD = P(s, 'doc', lt, 1), pR = P(s, 'rules', lt, 3), p1 = P(s, 'made', lt, 4), p2 = P(s, 'end', lt, 5);
      const owners = card(`<div style="width:150px;height:120px">${bld(TXT)}</div>${persons(3, TXT, pO, 46, 70)}${label('구단주\n30개 구단', TXT, pO, 42)}`, TXT, pO, CW);
      const union = card(`${persons(5, ACC, pU, 52, 80)}${label('선수노조\n(메이저리그 선수)', ACC, pU, 42)}`, ACC, pU, CW);
      const rules = ['연봉', 'FA', '트레이드', '드래프트'].map((t, i) => chip(t, GREEN, c01(pR * 2 - i * .25), 32)).join('');
      const doc = `<div class="col" style="align-items:center;gap:14px;width:${V() ? 360 : 520}px"><div style="width:230px;height:172px;${pop(pD)}">${DICON.doc('', ACC)}</div>${label('노사협약 = 리그 운영 계약서', TXT, pD, 42)}<div class="row" style="gap:10px;flex-wrap:wrap;justify-content:center;min-height:62px">${rules}</div></div>`;
      const arr = p => `<div style="font-size:72px;font-weight:900;color:${GRAY};${pop(p)}">↔</div>`;
      h += `<div class="row" style="gap:24px;align-items:center;flex-wrap:nowrap">${owners}${arr(pD)}${doc}${arr(pD)}${union}</div>`;
      h += `<div class="row" style="gap:28px;align-items:center;margin-top:30px;min-height:70px">${chip('2022년 3월 체결', TXT, p1, 40)}<div style="width:120px;height:8px;border-radius:4px;background:${LINE};${pop(p2)}"></div>${chip('2026년 12월 1일 만료 (미국 시간)', RED, p2, 40)}</div>`;
      wrapC(h); return;
    }
    if (mode === 'branch') {
      const p0 = P(s, 'end', lt, 0), pA = P(s, 'keep', lt, 4), pB = P(s, 'lock', lt, 1), pX = P(s, 'auto', lt, 1), pC = P(s, 'card', lt, 2);
      const node = (inner, c, p) => `<div class="col" style="width:${V() ? 420 : 640}px;background:${c}10;border:5px solid ${c};border-radius:36px;padding:24px 28px;gap:12px;align-items:center;position:relative;${pop(p)}">${inner}</div>`;
      const A = node(`<div class="row" style="gap:18px;align-items:center"><div style="width:120px;height:90px">${DICON.doc('', ACC)}</div>${persons(2, TXT, pA, 44, 66)}<div style="font-size:54px;font-weight:900;color:${GRAY}">🤝</div>${persons(2, ACC, pA, 44, 66)}</div>${label('옛 협약 그대로 두고\n협상을 이어 간다', ACC, pA, 44)}`, ACC, pA);
      const B_ = node(`<div style="width:150px;height:112px">${lockSvg(RED, false)}</div>${label('직장폐쇄', RED, pB, 58)}${label('구단주가 고를 때만 — 협상에서\n밀어붙이려고 쓰는 카드', TXT, pC, 36)}${xmark(0)}<div style="position:absolute;right:-26px;top:-26px;${pop(pX)}">${chip('자동 ✗', TXT, 1, 34)}</div>`, RED, pB);
      const fork = `<svg width="150" height="420" viewBox="0 0 150 420" style="flex:0 0 auto"><path d="M0,210 C70,210 70,80 150,80" fill="none" stroke="${ACC}" stroke-width="10" stroke-linecap="round" stroke-dasharray="520" stroke-dashoffset="${(520 * (1 - eo(pA))).toFixed(0)}"/><path d="M0,210 C70,210 70,340 150,340" fill="none" stroke="${RED}" stroke-width="10" stroke-linecap="round" stroke-dasharray="520" stroke-dashoffset="${(520 * (1 - eo(pB))).toFixed(0)}"/></svg>`;
      h += `<div class="row" style="gap:16px;align-items:center;flex-wrap:nowrap">${chip('12월 1일\n협약 만료', TXT, p0, 44).replace('white-space:nowrap', 'white-space:pre-line;text-align:center;line-height:1.2')}${fork}<div class="col" style="gap:40px">${A}${B_}</div></div>`;
      wrapC(h); return;
    }
    /* mode lock — 비교 두 칸 + 예시 모션 */
    const pS = P(s, 'strike', lt, 3), pL = P(s, 'lock', lt, 4), pEx = P(s, 'walk', lt, 5), pTry = P(s, 'try', lt, 6), pNo = P(s, 'no', lt, 7), pOpen = P(s, 'open', lt, 8);
    const mini = (inner, c, p, t) => `<div class="col" style="width:${V() ? 360 : 520}px;background:${c}10;border:5px solid ${c};border-radius:30px;padding:12px 20px;gap:6px;align-items:center;${pop(p)}">${inner}${label(t, c, p, 36)}</div>`;
    const strike = mini(`<div class="row" style="gap:14px;align-items:center"><div style="width:90px;height:70px">${bld(GRAY)}</div><div style="font-size:48px;font-weight:900;color:${RED}">←</div>${persons(3, RED, pS, 40, 60)}</div>`, RED, pS, '파업 = 선수가 안 뛴다');
    const lock = mini(`<div class="row" style="gap:14px;align-items:center"><div style="width:90px;height:70px;position:relative">${bld(TXT)}<div style="position:absolute;left:50%;top:50%;width:54px;height:40px;translate:-50% -50%">${lockSvg(RED, false)}</div></div><div style="font-size:48px;font-weight:900;color:${RED}">⊣</div>${persons(3, GRAY, pL, 40, 60)}</div>`, RED, pL, '직장폐쇄 = 구단주가 문을 잠근다');
    h += `<div class="row" style="gap:30px;align-items:stretch;flex-wrap:nowrap;margin-bottom:26px">${strike}${lock}</div>`;
    /* 예시 무대 */
    const W = V() ? 880 : 1380, H_ = 270, gx = W - 330;
    const walk = eo(pEx), bounce = pNo > 0 ? Math.sin(c01(pNo * 1.2) * Math.PI) * 130 : 0;
    const px = 40 + (gx - 260 - 40) * walk - bounce + 150 * eo(pOpen);   /* 문이 열리면 안으로 */
    const locked = pL > 0 && pOpen < .6, opened = pOpen >= .6;
    const stage = `<div style="position:relative;width:${W}px;height:${H_}px;border-radius:30px;background:linear-gradient(180deg,#F7F9FC,#E9EEF6);border:4px solid ${LINE};overflow:hidden;${pop(c01(Math.max(pL, pEx) * 2))}">
      <div style="position:absolute;left:0;right:0;bottom:0;height:40px;background:${GREEN}22"></div>
      <div style="position:absolute;left:${gx}px;bottom:18px;width:300px;height:230px">${gate(TXT, opened)}</div>
      <div style="position:absolute;left:${gx + 150 - 44}px;bottom:150px;width:88px;height:66px;transform:scale(${(0.6 + 0.4 * eo(pL)).toFixed(2)});opacity:${locked ? 1 : 0}">${lockSvg(RED, false)}</div>
      <div style="position:absolute;left:${gx + 150 - 44}px;bottom:150px;width:88px;height:66px;opacity:${opened ? 1 : 0}">${lockSvg(GREEN, true)}</div>
      <div style="position:absolute;left:${gx + 50}px;top:14px;${pop(c01(Math.max(pL, pEx) * 2))}">${chip('구단 (메이저리그)', TXT, 1, 30)}</div>
      <div style="position:absolute;left:${px.toFixed(0)}px;bottom:52px;width:72px;height:110px;opacity:${c01(pEx * 3)}">${ICON.person(ACC)}</div>
      <div style="position:absolute;left:${(px - 24).toFixed(0)}px;bottom:14px;${pop(c01(pEx * 3))}">${chip('FA 투수', ACC, 1, 28)}</div>
      <div style="position:absolute;left:${(px + 70).toFixed(0)}px;bottom:150px;background:#fff;border:4px solid ${ACC};border-radius:22px;padding:8px 18px;font-size:32px;font-weight:900;color:${TXT};white-space:nowrap;${pop(pTry)};opacity:${(c01(pTry * 1.4) * (1 - c01(pNo * 2))).toFixed(2)}">계약할게요!</div>
      <div class="row" style="position:absolute;left:${(px + 60).toFixed(0)}px;top:30px;gap:14px;${pop(pNo)};opacity:${(c01(pNo * 1.4) * (1 - c01(pOpen * 2))).toFixed(2)}"><div style="position:relative;width:86px;height:86px">${phone(GRAY)}${xmark(pNo, 56)}</div><div style="position:relative;width:86px;height:86px">${pen(GRAY)}${xmark(pNo, 56)}</div></div>
      <div style="position:absolute;left:${(px + 40).toFixed(0)}px;top:124px;${pop(pNo)};opacity:${(c01(pNo * 1.4) * (1 - c01(pOpen * 2))).toFixed(2)}">${chip('전화 ✗ 사인 ✗', RED, 1, 30)}</div>
      <div style="position:absolute;left:${gx - 320}px;top:40px;transform:rotate(-12deg) scale(${(0.5 + 0.5 * eo(pOpen)).toFixed(2)});opacity:${pOpen > 0 ? 1 : 0};border:6px solid ${GREEN};color:${GREEN};border-radius:18px;padding:6px 20px;font-size:40px;font-weight:900;white-space:nowrap;background:#fff">새 협약 서명 ✔</div>
    </div>`;
    h += stage;
    wrapC(h);
  };
  MOTION.lockout = s => 1.2;
})();
/* @@LOCK1011END */
