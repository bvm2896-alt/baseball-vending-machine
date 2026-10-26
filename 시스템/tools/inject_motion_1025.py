# 10/25 롱폼㉙ 검수 — 사용자 "카드와 텍스트로 떼우지 말고 인포그래픽·모션그래픽·애니메이션으로 직관적이게" / "카드로 떼운 장면들 전부"
# 새 장면: roads(두 가지 길) · dayfill(1군 등록일수 막대 + 국가대표 포인트) · lockout(노사협약·직장폐쇄 5가지 그림) · feerule(입찰액 → 보장 금액 3구간)
# + duel 에 logos 줄(찾아온 스카우트 구단). template_long.html 의 function render 앞에 넣는다(다시 돌리면 바꿔 끼움).
import re, sys, io
BLOCK = r'''/* @@MOT1025 10/25 롱폼㉙ 모션 그래픽 — tools/inject_motion_1025.py 가 넣는다(이 파일을 고치면 다시 주입)
   공통: step(같은 그림이 이어지는 장면 번호) — 앞 step 에서 나온 건 다 그려진 채로 가만히, 이번 step 것만 움직인다 */
(function () {
  const LOGOI = (n, px, st = '') => { const c_ = (T(n) || {}).code, kb = c_ === 'KBO';   /* 10/25 KBO 공식 로고(엠블럼 + KBO, 가로 2.47:1 — 사용자가 보낸 공식 로고)는 넓게 */
    return `<img src="${LOGO[c_] || ''}" style="width:${kb ? Math.round(px * 1.85) : px}px;height:${kb ? Math.round(px * .75) : px}px;object-fit:contain;display:block;${st}">`; };
  const cl = (v, a, b) => Math.max(a, Math.min(b, v)), e3 = x => 1 - Math.pow(1 - cl(x, 0, 1), 3);
  const TT = (s, k) => { const segs = (EP.segT || [])[s.startLine] || []; if (!segs.length) return null;
    const i = Math.floor(k), f = k - i, t0 = segs[i] ?? segs[segs.length - 1], t1 = segs[i + 1] ?? (t0 + 1.5);
    const d = NOW - (t0 + (t1 - t0) * f); return d < 0 ? null : d; };
  const mkA = s => (step, k, d = .6) => { const st = s.step || 1; if (st > step) return 1; if (st < step) return 0; if (k != null && k < 0) return 1; const t = TT(s, k); return t == null ? 0 : cl(t / (d * SPD), 0, 1); };
  const BLUE = '#2F6BFF', GRN = '#1F9D55', RD = '#E5484D', GOLD = '#E8A100', INK = '#12161F', GRY = '#6A7382', LINEC = '#E3E8F0';
  const pill = (t, bg, fs = 30, st = '') => `<span style="background:${bg};color:#fff;border-radius:${fs * .7}px;padding:${fs * .15}px ${fs * .6}px;font-size:${fs}px;font-weight:900;white-space:nowrap;${st}">${t}</span>`;
  const person = (c, w = 90) => `<svg viewBox="0 0 40 60" width="${w}" height="${w * 1.25}"><circle cx="20" cy="11" r="9" fill="${c}"/><path d="M6,58 L6,32 Q6,22 20,22 Q34,22 34,32 L34,58 Z" fill="${c}"/></svg>`;
  const lockSvg = (c, open = 0, w = 70) => `<svg viewBox="0 0 40 48" width="${w}" height="${w * 1.2}"><path d="M10,22 V14 A10,10 0 0 1 30,14 V${22 - 10 * open}" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round" transform="translate(${open * 10} 0)"/><rect x="4" y="22" width="32" height="24" rx="5" fill="${c}"/><circle cx="20" cy="33" r="4" fill="#fff"/></svg>`;
  const at = (x, y, w, inner, st = '') => `<div style="position:absolute;left:${x}px;top:${y}px;${w ? `width:${w}px;` : ''}${st}">${inner}</div>`;
  const op = (v, st = '') => `opacity:${cl(v, 0, 1).toFixed(3)};${st}`;
  const rise_ = (v, px = 26) => `opacity:${cl(v * 1.5, 0, 1).toFixed(3)};transform:translateY(${((1 - e3(v)) * px).toFixed(1)}px)`;
  const popS = v => `opacity:${cl(v * 1.6, 0, 1).toFixed(3)};transform:scale(${(.75 + .25 * e3(v)).toFixed(3)})`;
  const frame = (s, lt, W, H, inner) => { s.noCenter = true; /* 10/25: 이 장면들은 처음부터 가운데로 설계 — 가로 자동 맞춤(_cx)이 묶음 장면마다 달라 밀리던 것 막음 */ const title = s.title ? `<div class="title" style="font-size:58px;font-weight:900;text-align:center;margin-bottom:40px;${s._same || s._chain ? '' : pop(seg(lt, 0, .4))}">${esc(s.title)}</div>` : '';
    B(`<div class="col" style="align-items:center;width:100%">${title}<div style="position:relative;width:${W}px;height:${H}px;flex:0 0 auto">${inner}</div></div>`); };
  const box = (x, y, w, h, inner, bg = '#fff', st = '') => at(x, y, w, `<div class="col" style="width:${w}px;height:${h}px;box-sizing:border-box;border-radius:28px;background:${bg};box-shadow:0 16px 36px rgba(18,22,31,.12);align-items:center;justify-content:center;gap:8px">${inner}</div>`, st);

  /* ── roads: KBO → 메이저리그 두 가지 길 ── step 1 길 두 개 · 2 포스팅 길(7시즌 칸 + 구단 허락 문) · 3 FA 길(허락 없이) · 4 해외 구단 어디든 · 5 정리 */
  SCENE.roads = (lt, s) => {
    const A = mkA(s), W = 1728, H = 600, st = s.step || 1;
    const R1 = 200, R2 = 470, X0 = 340, X1 = 1390, GX = 1250, BXS = X0 + 50;
    const road = A(1, 1, 1.0), l1 = A(1, 2.0, .5), l2 = A(1, 2.4, .5);
    const seas = A(2, 1, 1.4), gate = A(2, 2, .5), gopen = A(2, 3, .6);
    const fa = A(3, 1, 1.2), any = A(4, 0.6, .6), sum1 = A(5, 1, .5), sum2 = A(5, 2, .5);
    const dimP = st >= 3 && st <= 4 ? .35 : 1, dimF = st === 2 ? .35 : 1;
    const p1x = st < 2 ? -1 : X0 + (GX - 60 - X0) * e3(seas) + (X1 - (GX - 60)) * e3(gopen);
    const p2x = st < 3 ? -1 : X0 + (X1 - X0) * e3(fa);
    let h = '';
    h += box(0, 130, 320, 340, `${LOGOI('KBO', 100)}${person('#2B3445', 90)}<b style="font-size:42px;font-weight:900">선수</b>`, '#fff', rise_(A(1, 0, .5)));
    h += box(W - 320, 130, 320, 340, `<div class="col" style="align-items:center;gap:8px;opacity:${(1 - cl(any * 2, 0, 1)).toFixed(3)}">${LOGOI('MLB', 140)}<b style="font-size:44px;font-weight:900;color:#fff">메이저리그</b></div>`, '#0F1626', rise_(A(1, 0, .5)));
    let svg = '';
    const rw = (X1 - X0) * e3(road);
    svg += `<rect x="${X0}" y="${R1 - 18}" width="${rw.toFixed(1)}" height="36" rx="18" fill="${st >= 2 ? BLUE : '#C9D2E0'}" opacity="${dimP}"/>`;
    svg += `<rect x="${X0}" y="${R2 - 18}" width="${rw.toFixed(1)}" height="36" rx="18" fill="${st >= 3 ? GRN : '#C9D2E0'}" opacity="${dimF}"/>`;
    const dot = (x, y, c) => `<circle cx="${x}" cy="${y}" r="38" fill="#fff" stroke="${c}" stroke-width="8"/><circle cx="${x}" cy="${y - 8}" r="10" fill="${c}"/><path d="M${x - 17},${y + 24} q17,-28 34,0 z" fill="${c}"/>`;
    if (p1x > 0) svg += `<g opacity="${dimP}">${dot(p1x, R1, BLUE)}</g>`;
    if (p2x > 0) svg += dot(p2x, R2, GRN);
    h += `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0;overflow:visible">${svg}</svg>`;
    h += at(X0, R1 - 100, 0, pill('포스팅', BLUE, 46), `${popS(l1)};${dimP < 1 ? 'opacity:.45;' : ''}`);
    h += at(X0, R2 - 100, 0, pill('FA', GRN, 46), `${popS(l2)};${dimF < 1 ? 'opacity:.45;' : ''}`);
    /* 7시즌 칸 */
    if (st >= 2) { let c = ''; for (let i = 0; i < 7; i++) { const q = cl(seas * 8 - i - .3, 0, 1);
        c += `<div style="width:90px;height:76px;border-radius:14px;background:${q > 0 ? BLUE : '#E3E8F0'};color:#fff;display:flex;align-items:center;justify-content:center;font-size:36px;font-weight:900;transform:scale(${(.8 + .2 * e3(q)).toFixed(3)})">${q > .3 ? i + 1 : ''}</div>`; }
      h += at(BXS, R1 + 40, 0, `<div class="row" style="gap:10px;flex-wrap:nowrap">${c}</div>`, `opacity:${(cl(seas * 4, 0, 1) * dimP).toFixed(3)}`);
      if (st < 5) h += at(BXS + 230, R1 - 100, 0, pill('KBO 7시즌', '#0F1626', 40), `opacity:${(cl(seas * 3, 0, 1) * dimP).toFixed(3)}`); }
    /* 구단 허락 문 */
    if (gate > 0) { const oc = gopen > .5 ? GRN : RD;
      h += at(GX - 50, R1 - 120, 100, `<div class="col" style="align-items:center">${lockSvg(oc, e3(gopen), 80)}</div>`, `${popS(gate)};${dimP < 1 ? 'opacity:.4;' : ''}`);
      h += at(GX - 150, R1 + 46, 300, `<div style="text-align:center">${pill(gopen > .5 ? '구단 허락 ✓' : '구단 허락 필요', oc, 38)}</div>`, `${op(gate)};${dimP < 1 ? 'opacity:.4;' : ''}`); }
    if (fa > 0) h += at(GX - 270, R2 + 46, 400, `<div style="text-align:center;font-size:42px;font-weight:900;color:#1F9D55;white-space:nowrap">구단 허락 없이</div>`, popS(cl(fa * 2, 0, 1)));   /* 10/25 검수: 알약 → 글씨 */
    /* 10/25 검수(알약 3개가 상자 밑 오른쪽 끝에 몰리고 글씨 22px): 도착 상자 자체가 '메이저리그' → 'MLB·NPB 로고 + 해외 구단'으로 바뀐다(따로 꼬리표 없음) */
    if (any > 0) h += box(W - 320, 130, 320, 340, `<div class="row" style="gap:16px;align-items:center">${LOGOI('MLB', 96)}${LOGOI('NPB', 96)}</div><b style="font-size:44px;font-weight:900;color:#fff;margin-top:10px">해외 구단</b>`, '#0F1626', op(cl(any * 2 - 1, 0, 1)));
    if (sum1 > 0) h += at(BXS + 230, R1 - 100, 0, `<b style="font-size:42px;font-weight:900;color:${RD};white-space:nowrap">7시즌 + 구단 허락</b>`, popS(sum1));
    /* 10/25 검수(같은 화면에 '허락 없이' 두 번 · FA 장점이 빨간색): FA 줄은 위 '구단 허락 없이'(초록) 하나만 */   /* 10/25 사용자 "빨간 알약끼리 정렬 안 맞아": 위 알약과 같은 왼쪽 선 */
    frame(s, lt, W, H, h);
  };

  /* ── dayfill: 1군 등록일수 막대 ── step 1 0→145일 · 2 = 풀타임 · 3 모자란 시즌 + 국가대표 포인트 · 4 1포인트 = 1일 · 5 아시안게임 금 +25 · 6 병역 혜택이면 못 받음 */
  SCENE.dayfill = (lt, s) => {
    const A = mkA(s), W = 1680, H = 560, st = s.step || 1, BX = 40, BY = 200, BW = 1480, BH = 120, MAXD = 180, px = d => BX + BW * d / MAXD;
    const bIn = A(1, 0, .5), grow = A(1, 1, 1.6), ok = A(1, 3, .45), full = A(2, 1, .45);
    const drop = A(3, 1, .8), medal = A(3, 1, .5);
    const intl = A(4, 0, .5), coin = A(4, 1, .5), eq = A(4, 2, .5), add5 = A(4, 3, .8);
    const ag = A(5, 0.3, .5), add25 = A(5, 2, 1.0);
    const mil = A(6, 1, .5), out25 = A(6, 2.2, .9);
    /* 막대 값 */
    let base = st <= 2 ? 145 * e3(grow) : 145 - 25 * e3(drop), plus5 = 5 * e3(add5), plus25 = 25 * e3(add25) * (1 - e3(out25));
    const tot = base + plus5 + plus25, okNow = st <= 2 ? ok : (tot >= 145 - 1e-6 ? 1 : 0);
    let h = '';
    h += at(BX, BY - 74, 0, `<b style="font-size:46px;font-weight:900;white-space:nowrap">1군 등록일수</b>`, op(bIn));
    h += at(BX, BY, BW, `<div style="position:relative;width:${BW}px;height:${BH}px;border-radius:${BH / 2}px;background:${LINEC};overflow:hidden">
        <div style="position:absolute;left:0;top:0;bottom:0;width:${(BW * base / MAXD).toFixed(1)}px;background:${BLUE}"></div>
        <div style="position:absolute;left:${(BW * base / MAXD).toFixed(1)}px;top:0;bottom:0;width:${(BW * plus5 / MAXD).toFixed(1)}px;background:#3BB273"></div>
        <div style="position:absolute;left:${(BW * (base + plus5) / MAXD).toFixed(1)}px;top:0;bottom:0;width:${(BW * plus25 / MAXD).toFixed(1)}px;background:${GOLD}"></div>
        ${st >= 3 && tot < 145 ? `<div style="position:absolute;left:${(BW * tot / MAXD).toFixed(1)}px;top:0;bottom:0;width:${(BW * (145 - tot) / MAXD).toFixed(1)}px;background:repeating-linear-gradient(45deg,rgba(229,72,77,.25) 0 12px,transparent 12px 24px)"></div>` : ''}</div>`, op(bIn));
    /* 10/25 검수(초록 5일이 어디서 왔는지 라벨 없음): 더해진 칸에 '+5일'(아래) · '+25일'(칸 안) */
    if (plus5 > .5) h += at(px(base + plus5 / 2) - 60, BY + BH + 16, 120, `<div style="text-align:center;font-size:38px;font-weight:900;color:#1F9D55;white-space:nowrap">+5일</div>`, op(add5));
    if (plus25 > 3) h += at(px(base + plus5), BY, BW * plus25 / MAXD, `<div style="height:${BH}px;display:flex;align-items:center;justify-content:flex-start;padding-left:16px;box-sizing:border-box;font-size:42px;font-weight:900;color:#fff;white-space:nowrap;overflow:hidden">+25일</div>`, op(cl(add25 * 2, 0, 1) * (1 - e3(out25))));
    /* 145일 기준선 */
    h += at(px(145) - 3, BY - 20, 6, `<div style="width:6px;height:${BH + 40}px;background:${INK};border-radius:3px"></div>`, op(bIn));
    h += at(px(145) - 150, BY + BH + 20, 300, `<div style="text-align:center;font-size:38px;font-weight:900;white-space:nowrap">145일 = 1시즌</div>`, op(A(1, 2, .4)));   /* 10/25 검수: '145일'을 말할 때 */
    /* 지금 일수 */
    h += at(BX + 28, BY, 0, `<div class="num" style="height:${BH}px;display:flex;align-items:center;font-size:70px;line-height:1;font-weight:900;color:#fff;white-space:nowrap">${Math.round(tot)}일</div>`   /* 10/25 사용자 "알약 안에 145일이 너무 위에 있음 중앙에 맞춰" — 막대 높이 안 세로 가운데 */, op(cl(bIn * 2, 0, 1) * (tot > 30 ? 1 : 0)));
    if (st >= 3) h += at(BX + 330, BY - 68, 0, pill('예시', GRY, 32), op(drop));
    if (st >= 3 && tot < 145) h += at(px(tot) - 120, BY - 70, 0, `<div style="font-size:40px;font-weight:900;color:${RD};white-space:nowrap">${Math.round(145 - tot)}일 모자람</div>`, op(drop));
    /* 인정 도장 */
    /* 10/25: '= 풀타임' 이 화면 오른쪽 끝(1869px)까지 나가던 것 → 두 알약을 막대 오른쪽 끝에 맞춰 오른쪽 정렬 */
    h += at(px(145) - 520, BY - 84, BX + BW - (px(145) - 520), `<div class="row" style="gap:12px;align-items:center;justify-content:flex-end;flex-wrap:nowrap">${pill(okNow > 0 ? '1시즌 인정 ✓' : '', okNow > 0 ? GRN : 'transparent', 42)}${full > 0 ? pill('= 풀타임', '#0F1626', 42, `opacity:${full.toFixed(3)}`) : ''}</div>`, popS(okNow) + ';transform-origin:right center');
    if (st >= 3 && tot < 145 - 1e-6 && st < 6) {}
    if (st === 6 && out25 > .6) h += at(px(145) + 16, BY - 84, 0, pill('1시즌 인정 ✗', RD, 42), popS(cl(out25 * 2 - 1, 0, 1)));
    /* 국가대표 포인트 아이콘들 (아래 줄) */
    const MED = (c, t) => `<div style="width:110px;height:110px;border-radius:50%;background:${c};color:#fff;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;box-shadow:0 10px 24px rgba(18,22,31,.18)">${t}</div>`;
    const RY = 440;
    if (medal > 0) h += at(BX, RY, 0, `<div class="row" style="gap:16px;align-items:center;flex-wrap:nowrap">${MED('#0F1626', '★')}<b style="font-size:44px;font-weight:900;white-space:nowrap">국가대표 포인트</b></div>`, rise_(medal));
    if (intl > 0) h += at(BX + 470, RY + 14, 0, `<div class="row" style="gap:14px;align-items:center;flex-wrap:nowrap"><b style="font-size:44px;font-weight:900;color:#2F6BFF;white-space:nowrap">국제대회 출전</b>${coin > 0 ? `<span style="font-size:50px;font-weight:900;color:${GRY};${op(coin)}">→</span>${MED('#3BB273', '+1').replace('110px;height:110px', '84px;height:84px')}` : ''}${eq > 0 ? `<b style="font-size:44px;font-weight:900;white-space:nowrap;${op(eq)}">1포인트 = 1일</b>` : ''}</div>`, rise_(intl));
    /* 10/25 검수(오른쪽 끝에 금메달·글·빨간 줄·알약이 뭉쳐 읽기 어려움): 아시안게임 금은 아래 줄 왼쪽에 따로 · 병역 혜택이면 '+25포인트'에만 줄을 긋고 옆에 빨간 글 */
    if (ag > 0) h += at(BX, RY + 140, 0, `<div class="row" style="gap:18px;align-items:center;flex-wrap:nowrap">${MED(GOLD, '금')}<b style="font-size:44px;font-weight:900;white-space:nowrap">아시안게임 금메달</b><b style="font-size:50px;color:${GRY}">→</b><span style="position:relative;display:inline-block"><b class="num" style="font-size:56px;font-weight:900;color:${mil > .5 ? '#9AA6B8' : '#B07A00'};white-space:nowrap">+25포인트</b>${mil > 0 ? `<svg width="100%" height="20" style="position:absolute;left:-6px;top:calc(50% - 10px);overflow:visible"><line x1="0" y1="10" x2="${(270 * e3(mil)).toFixed(0)}" y2="10" stroke="${RD}" stroke-width="9" stroke-linecap="round"/></svg>` : ''}</span>${mil > 0 ? `<b style="font-size:44px;font-weight:900;color:${RD};white-space:nowrap;margin-left:12px;${popS(mil)};display:inline-block">병역 혜택 받으면 ✕</b>` : ''}</div>`, rise_(ag));
    frame(s, lt, W, H + 150, h);
  };

  /* ── lockout: 메이저리그 노사협약·직장폐쇄 ── mode: cba(step 1~4) · memo · freeze · past · winter(step 1 신청 창 2 관건) · alt */
  SCENE.lockout = (lt, s) => {
    const A = mkA(s), W = 1640, H = 560, st = s.step || 1, m = s.mode || 'cba';
    let h = '', svg = '';
    const bld = c => `<svg viewBox="0 0 60 60" width="110" height="110"><path d="M6,56 V22 L30,6 L54,22 V56 Z" fill="${c}"/><rect x="16" y="28" width="8" height="10" fill="#fff"/><rect x="36" y="28" width="8" height="10" fill="#fff"/><rect x="25" y="40" width="10" height="16" fill="#fff"/></svg>`;
    const grp = c => `<svg viewBox="0 0 80 60" width="130" height="98"><circle cx="20" cy="16" r="9" fill="${c}"/><path d="M6,58 V36 Q6,28 20,28 Q34,28 34,36 V58 Z" fill="${c}"/><circle cx="40" cy="12" r="10" fill="${c}"/><path d="M24,58 V32 Q24,24 40,24 Q56,24 56,32 V58 Z" fill="${c}"/><circle cx="60" cy="16" r="9" fill="${c}"/><path d="M46,58 V36 Q46,28 60,28 Q74,28 74,36 V58 Z" fill="${c}"/></svg>`;
    if (m === 'cba') {
      const doc = A(1, 1, .6), exp = A(2, 1, .5), fail = A(3, 0.4, .6), lock = A(3, 1, .5), block = A(4, 1, 1.2);
      h += box(20, 90, 330, 330, `${bld('#0F1626').replace(/110/g, '140')}<b style="font-size:46px;font-weight:900">구단</b>`, '#fff', rise_(A(1, 0.3, .5)));
      h += box(W - 350, 90, 330, 330, `${grp(BLUE).replace('width="130" height="98"', 'width="170" height="128"')}<b style="font-size:46px;font-weight:900">선수노조</b>`, '#fff', rise_(A(1, 0.6, .5)));
      svg += `<line x1="360" y1="255" x2="${360 + 420 * e3(doc)}" y2="255" stroke="${fail > .5 ? '#C9D2E0' : BLUE}" stroke-width="8" stroke-dasharray="16 12"/><line x1="${W - 360}" y1="255" x2="${W - 360 - 420 * e3(doc)}" y2="255" stroke="${fail > .5 ? '#C9D2E0' : BLUE}" stroke-width="8" stroke-dasharray="16 12"/>`;
      h += at(W / 2 - 200, 90, 400, `<div class="col" style="width:400px;height:330px;box-sizing:border-box;border-radius:24px;background:#fff;border:6px solid ${fail > .5 ? '#C9D2E0' : BLUE};align-items:center;justify-content:center;gap:10px;filter:grayscale(${fail.toFixed(2)})">
          <svg viewBox="0 0 40 48" width="80" height="96"><path d="M4,2 H26 L36,12 V46 H4 Z" fill="#fff" stroke="${BLUE}" stroke-width="4"/><path d="M10,20 h20 M10,28 h20 M10,36 h14" stroke="${BLUE}" stroke-width="4"/></svg>
          <b style="font-size:50px;font-weight:900">노사협약</b><b style="font-size:38px;font-weight:900;color:${GRY}">리그 규칙 약속</b></div>`, popS(doc));
      if (exp > 0) h += at(W / 2 - 300, 440, 600, `<div style="text-align:center">${pill('미국 시간 12월 1일 밤 · 끝', RD, 40)}</div>`, popS(exp));
      if (lock > 0) h += at(W / 2 - 90, 20, 180, `<div class="col" style="align-items:center">${lockSvg(RD, 0, 150)}</div>`, `opacity:${cl(lock * 1.6, 0, 1).toFixed(3)};transform:translateY(${(-120 * (1 - e3(lock))).toFixed(0)}px) scale(${(1.2 - .2 * e3(lock)).toFixed(3)})`);
      if (lock > 0) h += at(W / 2 - 300, 510, 600, `<div style="text-align:center">${pill('12월 2일부터 직장폐쇄 가능', '#0F1626', 40)}</div>`, popS(lock));
      if (block > 0) { const bx = W - 380 - 150 * Math.sin(Math.min(1, block) * Math.PI);
        h += at(bx - 50, 250, 0, person(BLUE, 90), op(block)); h += at(W - 380, 440, 380, `<div style="text-align:center;font-size:48px;font-weight:900;color:${RD};white-space:nowrap">🚫 활동 금지</div>`, popS(cl(block * 1.5 - .4, 0, 1)));   /* 10/25 검수: 나레이션 문장 대신 핵심어 */ }
    }
    if (m === 'memo') {
      const mb = A(1, 0, .5), fly = A(1, 1, 2.0), lab = A(1, 2, .5);   /* 10/25 사용자("화면이 멈춘것처럼 멈췄는데 나레이션은 그대로"): 예전 식(fly*1.3 - i/30)은 12번째 봉투부터 끝까지 못 가고 멈춰 있었다 → 모든 봉투가 fly=1 에 도착 */
      h += box(20, 150, 340, 220, `${LOGOI('MLB', 96)}<b style="font-size:36px;font-weight:900;color:#fff">메이저리그 사무국</b>`, '#0F1626', rise_(mb));
      h += at(20, 400, 340, `<div style="text-align:center">${pill('10월 초', GRY, 30)}</div>`, op(mb));
      let dots = ''; for (let i = 0; i < 30; i++) { const q = cl((fly - i / 30 * .55) / .45, 0, 1), x = 760 + (i % 10) * 82, y = 110 + Math.floor(i / 10) * 110;
        dots += at(x, y, 0, `<div style="width:66px;height:66px;border-radius:50%;background:${q > .9 ? '#0F1626' : LINEC};color:#fff;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:900">${q > .9 ? '✉' : ''}</div>`);
        if (q > 0 && q < .9) { const e = e3(q / .9); svg += `<g transform="translate(${360 + (x + 33 - 360) * e} ${260 + (y + 33 - 260) * e - Math.sin(e * Math.PI) * 60})"><rect x="-22" y="-15" width="44" height="30" rx="4" fill="#fff" stroke="${RD}" stroke-width="3"/><path d="M-22,-15 L0,4 L22,-15" fill="none" stroke="${RD}" stroke-width="3"/></g>`; } }
      h += dots + at(760, 450, 820, `<div style="text-align:center">${pill('30개 구단에 · 직장폐쇄 대비 지침', RD, 34)}</div>`, popS(lab));
    }
    if (m === 'freeze') {
      const its = [['FA 계약', 1.0], ['포스팅 계약', 1.4], ['트레이드', 2.0]], all = A(1, 3, .5);
      its.forEach(([t, k], i) => { const q = A(1, k, .6), x = 60 + i * 520, run = (NOW * 120) % 80;
        h += at(x, 120, 440, `<div class="col" style="width:440px;height:260px;box-sizing:border-box;border-radius:28px;background:${q > .5 ? '#DCE9F7' : '#fff'};box-shadow:0 16px 36px rgba(18,22,31,.12);align-items:center;justify-content:center;gap:16px;position:relative;overflow:hidden">
            <div class="row" style="gap:14px;align-items:center;flex-wrap:nowrap"><div style="width:${(66 * e3(q)).toFixed(1)}px;height:66px;flex:0 0 auto;overflow:hidden;${popS(q)}"><div style="width:66px;height:66px;border-radius:50%;background:rgba(229,72,77,.95);display:flex;align-items:center;justify-content:center;gap:10px"><div style="width:11px;height:30px;background:#fff;border-radius:3px"></div><div style="width:11px;height:30px;background:#fff;border-radius:3px"></div></div></div><b style="font-size:50px;font-weight:900;white-space:nowrap;color:${q > .5 ? '#3B5B80' : INK}">${t}</b></div>   <!-- 10/25 검수: 멈춤 표시가 글자를 덮던 것 → 글자 앞에 -->
            <div style="width:300px;height:22px;border-radius:11px;background:${LINEC};overflow:hidden;position:relative"><div style="position:absolute;top:0;bottom:0;left:${q > 0 ? 0 : -80 + run}px;width:${q > 0 ? 300 : 380}px;background:repeating-linear-gradient(90deg,${q > 0 ? '#9DB6D3' : GRN} 0 40px,transparent 40px 80px)"></div></div>
<div style="font-size:40px;font-weight:900;color:${RD};opacity:${q.toFixed(3)}">멈춤</div></div>`, rise_(A(1, 0, .5))); });
      h += at(W / 2 - 200, 430, 400, `<div style="text-align:center">${pill('모두 멈춤', RD, 44)}</div>`, popS(all));
    }
    if (m === 'past') {
      const x0 = 120, x1 = 1480, d = A(1, 1, 2.0), sIn = A(1, 0.4, .5), days = Math.round(99 * e3(d));
      h += at(x0, 120, 0, pill('2021년 12월 2일 · 시작', '#0F1626', 34), popS(sIn));
      h += at(x1 - 260, 120, 260, `<div style="text-align:right">${pill('2022년 3월 · 끝', GRN, 34)}</div>`, popS(cl(d * 3 - 2, 0, 1)));
      h += at(x0, 210, x1 - x0, `<div style="width:${x1 - x0}px;height:110px;border-radius:55px;background:${LINEC};overflow:hidden;position:relative"><div style="position:absolute;left:0;top:0;bottom:0;width:${((x1 - x0) * e3(d)).toFixed(1)}px;background:repeating-linear-gradient(45deg,${RD} 0 22px,#C7343A 22px 44px)"></div></div>`, op(sIn));
      h += at(x0 + (x1 - x0) * e3(d) - 120, 210, 0, `<div style="position:relative;left:${days > 20 ? -40 : 0}px">${lockSvg('#fff', 0, 70)}</div>`, `top:228px;${op(sIn)}`);
      h += at(W / 2 - 200, 360, 400, `<div class="num" style="text-align:center;font-size:120px;font-weight:900;color:${RD};letter-spacing:-4px">${days}일</div>`, op(sIn));
    }
    if (m === 'winter') {
      /* 10/25 사용자 "알약으로 하지 말고 다른걸로" · 검수(알약 5개·나레이션 되풀이): 11월~3월 달력 막대 하나 — 칸 이름은 칸 안에, 12월 2일은 막대 위 세로 금 하나 */
      const x0 = 40, x1 = 1600, D = 151, xd = n => x0 + (x1 - x0) * n / D, Y = 80, HH = 130, XD = xd(31);   /* n = 11월 1일부터 지난 날 · 31 = 12월 2일 */
      const T_ = (k, d) => s.t && s.t[k] != null ? s.t[k] : d;   /* 장면마다 호흡 번호를 바꿔 쓸 때 s.t = {win, lk, wait, key} */
      const win = A(1, T_('win', 0), .8), lk = A(1, T_('lk', 1), .6), wait = A(1, T_('wait', 2), .6), key = A(2, T_('key', 1), .5);
      const months = [['11월', 0], ['12월', 30], ['1월', 61], ['2월', 92], ['3월', 120]];
      h += months.map(([t, n]) => at(xd(n), Y + HH + 14, 0, `<b style="font-size:34px;font-weight:900;color:${GRY};white-space:nowrap">${t}</b>`)).join('');
      const lab = (t, q) => `<div style="display:flex;align-items:center;gap:12px;color:#fff;font-size:46px;font-weight:900;white-space:nowrap;opacity:${cl(q * 2 - .6, 0, 1).toFixed(3)}">${t}</div>`;
      h += at(x0, Y, x1 - x0, `<div style="position:relative;width:${x1 - x0}px;height:${HH}px;border-radius:26px;background:${LINEC};overflow:hidden">
          <div style="position:absolute;left:0;top:0;bottom:0;width:${((XD - x0) * e3(win)).toFixed(1)}px;background:${GRN};display:flex;align-items:center;justify-content:center;overflow:hidden">${lab('협상 가능', win)}</div>
          <div style="position:absolute;left:${XD - x0}px;top:0;bottom:0;width:${((x1 - XD) * e3(lk)).toFixed(1)}px;background:repeating-linear-gradient(45deg,${RD} 0 22px,#C7343A 22px 44px);overflow:hidden;display:flex;align-items:center;justify-content:space-between;padding:0 44px;box-sizing:border-box">${lab(`${lockSvg('#fff', 0, 46)}직장폐쇄 가능`, lk)}${lab('⏳ 기다림 길어짐', wait)}</div></div>`,
        key > 0 ? `border-radius:26px;box-shadow:0 0 0 0 transparent` : '');
      if (key > 0) h += at(x0, Y, XD - x0, `<div style="height:${HH}px;border-radius:26px 0 0 26px;box-shadow:inset 0 0 0 ${(9 * e3(key)).toFixed(1)}px ${GOLD}"></div>`, op(key));
      /* 12월 2일 금: 막대 위로 솟은 세로 금 + 날짜(왼쪽 정렬) */
      if (lk > 0) h += at(XD - 3, Y - 70, 6, `<div style="width:6px;height:${HH + 70}px;background:#12161F;border-radius:3px"></div>`, op(lk)) + at(XD + 16, Y - 78, 0, `<b style="font-size:46px;font-weight:900;color:${RD};white-space:nowrap">12월 2일</b>`, rise_(lk));
      if (key > 0 && !s.noKey) h += at(x0 + 4, Y - 70, 0, `<b style="font-size:40px;font-weight:900;color:#B07A00;white-space:nowrap">✓ 이 안에 계약</b>`, popS(key) + ';transform-origin:left center');
    }
    if (m === 'alt') {
      const blk = A(1, 0, .6), jp = A(1, 1, .6), kb = A(1, 2, .6), an = A(1, 3, .5);
      h += box(60, 150, 280, 260, `${LOGOI('KBO', 80)}${person('#2B3445', 70)}<b style="font-size:32px;font-weight:900">선수</b>`, '#fff', rise_(A(1, 0, .4)));
      svg += `<path d="M350,200 C700,120 900,120 1180,150" fill="none" stroke="#C9D2E0" stroke-width="12" stroke-dasharray="20 14" opacity="${blk.toFixed(2)}"/>`;
      h += box(1190, 60, 300, 180, `${LOGOI('MLB', 80)}<b style="font-size:32px;font-weight:900;color:#fff">메이저리그</b>`, '#0F1626', `${rise_(blk)};filter:grayscale(.6)`);
      h += at(820, 70, 0, lockSvg(RD, 0, 90), popS(blk));
      const arr = (y, c, q) => `<path d="M350,300 C600,300 800,${y} ${350 + 830 * e3(q)},${y}" fill="none" stroke="${c}" stroke-width="12" stroke-linecap="round"/>`;
      if (jp > 0) { svg += arr(330, RD, jp); h += box(1190, 280, 300, 110, `<div class="row" style="gap:12px;align-items:center">${LOGOI('NPB', 84)}<b style="font-size:36px;font-weight:900">일본 구단</b></div>`, '#fff', popS(cl(jp * 1.5 - .5, 0, 1))); }
      if (kb > 0) { svg += arr(470, BLUE, kb); h += box(1190, 420, 300, 110, `<div class="row" style="gap:12px;align-items:center">${LOGOI('KBO', 56)}<b style="font-size:36px;font-weight:900">잔류</b></div>`, '#fff', popS(cl(kb * 1.5 - .5, 0, 1))); }
      /* 10/25 사용자 "구구절절 설명 문구 넣지 마, 나레이션으로 말하잖아" — '분석' 꼬리표 뺌(제목이 같은 말) */   /* 10/25 검수: 꼬리표가 작고 선이 지나가던 것 → 아래 빈 곳에 크게 */
    }
    if (m === 'pause30') {
      /* {name, step 1: 이름(0) → 협상 시작(1) → 직장폐쇄로 멈춤(2) → 다시 이어짐(3) · step 2: 3월 계약(0.5)} */
      const nm = A(1, 0, .5), g1 = A(1, 1, .8), lkq = A(1, 2, .6), g2 = A(1, 3, .8), deal = A(2, 0.5, .6);
      /* 10/25 사용자 "이 장면 너무 보기 불편하다 배치가" — 위 한 줄: 왼쪽 누구 · 오른쪽 결과(막대 양끝에 맞춤), 막대 칸 안에 그 칸 이름(흩어진 꼬리표 없음) */
      const x0 = 40, x1 = 1600, Y = 150, HH = 170, a = x0 + 420, b = x0 + 1080;
      h += at(x0, 20, 0, `<div class="row" style="gap:16px;align-items:center;flex-wrap:nowrap;height:110px">${pill('일본', RD, 44)}<b style="font-size:68px;font-weight:900;white-space:nowrap">스즈키 세이야</b></div>`, rise_(nm));
      const seg = (l, w, bg, q, inner) => `<div style="position:absolute;left:${l}px;top:0;bottom:0;width:${(w * e3(q)).toFixed(1)}px;background:${bg};overflow:hidden;display:flex;align-items:center;justify-content:center"><div style="display:flex;align-items:center;gap:12px;color:#fff;font-size:50px;font-weight:900;white-space:nowrap;opacity:${cl(q * 2 - 1, 0, 1).toFixed(3)}">${inner}</div></div>`;
      h += at(x0, Y, x1 - x0, `<div style="position:relative;width:${x1 - x0}px;height:${HH}px;border-radius:28px;background:${LINEC};overflow:hidden">
          ${seg(0, a - x0, GRN, g1, '협상 30일 시작')}
          ${seg(a - x0, b - a, `repeating-linear-gradient(45deg,${RD} 0 22px,#C7343A 22px 44px)`, lkq, `${lockSvg('#fff', 0, 50)}직장폐쇄 · 협상 멈춤`)}
          ${seg(b - x0, x1 - b, GRN, g2, '다시 협상')}</div>`, op(nm));
      if (deal > 0) h += at(x1 - 900, 20, 900, `<div class="row" style="gap:14px;align-items:center;justify-content:flex-end;flex-wrap:nowrap;height:110px">${LOGOI('컵스', 84)}${pill('2022년 3월 · 컵스와 계약', '#0E3386', 44)}</div>`, popS(deal) + ';transform-origin:right center');
    }
    h = `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0;overflow:visible;pointer-events:none">${svg}</svg>` + h;   /* 선은 칸 뒤로 */
    frame(s, lt, W, m === 'pause30' ? 330 : m === 'winter' ? 270 : H + 30, h);   /* pause30: 내용 높이(이름 줄 + 막대)만큼만 → 화면 가운데 */
  };

  /* ── feerule: 이적료 계산법 (10/25 사용자 "포스팅 이적료 계산법에 대해서 좀만 더 자세히 — 모르는 사람은 무슨 말인지 모를 거 같아") ──
     step 1 2018년 규정 변경 전: 구단들이 금액을 써 냄(막대 3개) · 2 가장 높은 구단만 협상(왕관) + 입찰액 = 이적료 · 3 류현진 = 다저스 입찰액 2573만 달러+
     step 4 지금: 30개 구단 모두 · 30일 협상 · 5 이적료 = 보장 금액 기준(긴 막대) · 6 옵션은 빼고 반드시 받는 돈 · 7 보장 금액을 세 구간으로 나눠 구간마다 비율 */
  let _cv2 = null; const TW2 = (t, px, w = 900) => { _cv2 = _cv2 || document.createElement('canvas').getContext('2d'); _cv2.font = `${w} ${px}px ${getComputedStyle(document.body).fontFamily}`; return _cv2.measureText(String(t)).width; };
  SCENE.feerule = (lt, s) => {
    /* 10/25 사용자 "시청자가 보기 편하게 깔끔하게 정리" — 한 화면에 이야기 하나. 1~3 옛 방식 / 4 지금 30개 구단 / 5~7 보장 금액 → 구간
       화면 높이는 실제 내용 높이만큼만 잡아 화면 가운데에 온다(빈 자리를 아래에 남기지 않는다) */
    const A = mkA(s), st = s.step || 1;
    let h = '';
    if (st <= 3) {   /* 가운데 정렬: 막대 3개(입찰) → 왕관·나머지 흐림 → 아래 줄 설명 (류현진 때는 설명 줄이 류현진 입찰로 바뀜) */
      const BW0 = 250, GAP = 330, BH0 = 250, NB = 3, GW = (NB - 1) * GAP + BW0, W = 1500, X0 = (W - GW) / 2, CR = 92, TOP = 40, BASE = TOP + CR + BH0, LBY = BASE + 12, PY = LBY + 100, H = PY + 82;
      const bids = [['구단 A', 58, 0.6], ['구단 B', 100, 1.0], ['구단 C', 74, 1.4]];
      const crown = A(2, 0, .5), solo = A(2, 0.3, .5), eq = A(2, 2, .5), ryu = A(3, 0, .6), ryu2 = A(3, 1, .6);
      bids.forEach(([t, v, k], i) => { const q = A(1, k, .7), x = X0 + i * GAP, hh = BH0 * v / 100 * e3(q), win = i === 1, gone = win ? 0 : solo;
        const lab = win && ryu > 0 ? `<div class="row" style="gap:12px;justify-content:center;align-items:center;flex-wrap:nowrap">${LOGOI('다저스', 56)}<span>다저스</span></div>` : t;
        h += at(x, BASE - hh, BW0, `<div style="width:${BW0}px;height:${hh.toFixed(1)}px;border-radius:22px 22px 0 0;background:${win && crown > 0 ? GOLD : '#9DB0CC'};display:flex;align-items:flex-start;justify-content:center;padding-top:26px;box-sizing:border-box;color:#fff;font-size:46px;font-weight:900;line-height:1.1;text-align:center">${win && ryu2 > 0 ? `<span style="opacity:${ryu2.toFixed(3)}">2573만<br>달러 남짓</span>` : q > .6 ? `<span style="font-size:40px;opacity:${cl((q - .6) / .4, 0, 1).toFixed(3)}">입찰</span>` : ''}</div>`, `opacity:${(1 - .7 * gone).toFixed(3)}`);
        h += at(x - 40, LBY, BW0 + 80, `<div style="text-align:center;font-size:44px;font-weight:900;white-space:nowrap;color:${win && ryu > 0 ? '#1E5BB8' : INK}">${lab}</div>`, `opacity:${(cl(q * 2, 0, 1) * (1 - .7 * gone)).toFixed(3)}`);
        if (win && crown > 0) h += at(x + BW0 / 2 - 55, BASE - BH0 - CR - 4, 110, `<div style="font-size:88px;text-align:center;line-height:1">👑</div>`, popS(crown)); });
      /* 아래 줄 — 2단계: 한 곳만 협상 → 입찰액 = 이적료 / 3단계: 류현진 · 2012년 다저스 입찰액 */
      if (st === 2 && solo > 0) h += at(0, PY, W, `<div class="row" style="gap:22px;justify-content:center;align-items:center;flex-wrap:nowrap"><b style="font-size:50px;font-weight:900;white-space:nowrap">가장 많이 써낸 구단만 협상</b><b style="font-size:52px;color:${GRY};opacity:${eq.toFixed(3)}">→</b><b style="display:inline-block;font-size:54px;font-weight:900;color:#B07A00;white-space:nowrap;${popS(eq)}">입찰액 = 이적료</b></div>`, popS(solo));
      if (st === 3) h += at(0, PY, W, `<div class="row" style="gap:20px;justify-content:center;align-items:center;flex-wrap:nowrap"><b style="font-size:52px;font-weight:900;white-space:nowrap">류현진 · 2012년</b><b style="font-size:52px;font-weight:900;color:#B07A00;white-space:nowrap">다저스 입찰액 = 이적료</b></div>`, popS(ryu));
      return frame(s, lt, W, H, h);
    }
    if (st === 4) {
      const DS = 56, DG = 18, all30 = A(4, 0, 1.0), d30 = A(4, 1, .6), DW = 10 * DS + 9 * DG, DH = 3 * DS + 2 * DG, W = Math.ceil(DW + 70 + TW2('30개 구단 모두 협상', 58) + 8), H = DH;
      let dots = ''; for (let i = 0; i < 30; i++) { const q = cl(all30 * 1.3 - i / 30 * .3, 0, 1); dots += `<div style="width:${DS}px;height:${DS}px;border-radius:50%;background:${BLUE};opacity:${cl(q * 2, 0, 1).toFixed(3)};transform:scale(${(.5 + .5 * e3(q)).toFixed(3)})"></div>`; }
      h += at(0, 0, 0, `<div style="display:grid;grid-template-columns:repeat(10,${DS}px);gap:${DG}px">${dots}</div>`);
      h += at(DW + 70, 0, W - DW - 70, `<div class="col" style="align-items:flex-start;justify-content:center;gap:22px;height:${DH}px"><b style="font-size:58px;font-weight:900;white-space:nowrap;opacity:${cl(all30 * 2, 0, 1).toFixed(3)}">30개 구단 모두 협상</b><span style="${popS(d30)};transform-origin:left center;display:inline-block">${pill('30일 동안', '#0F1626', 50)}</span></div>`);
      return frame(s, lt, W, H, h);
    }
    /* 5~7 보장 금액 → 옵션 빼기 → 세 구간 */
    const W = 1600, BH = 160, BY = 76, PY = BY + BH + 44, H = PY + 76;
    const gbar = A(5, 0, .8), gl = A(5, 1, .5), opt = A(6, 1, .7), optX = A(6, 1.6, .5), cut = A(7, 0.3, 1.0), lab = A(7, 0.8, .5), mul = A(7, 1.6, .5);
    h += at(0, 0, W, `<div style="text-align:center;font-size:46px;font-weight:900;white-space:nowrap;color:${GRY}">선수가 맺은 계약</div>`, op(gbar * 2));
    const SW = W * (1 - .26 * e3(opt)), gap_ = 20 * e3(cut);
    const segs = [['구간 1', '#2F6BFF'], ['구간 2', '#3B6FD8'], ['구간 3', '#7A8BA8']];
    const inner = cut > 0 ? `<div class="row" style="gap:${gap_.toFixed(1)}px;flex-wrap:nowrap;width:100%;height:100%;align-items:stretch">${segs.map(([t, c]) => `<div style="flex:1;border-radius:20px;background:${c};color:#fff;display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:900;white-space:nowrap"><span style="opacity:${lab.toFixed(3)}">${t}</span></div>`).join('')}</div>`
      : `<div style="width:100%;height:100%;border-radius:20px;background:#2F6BFF;color:#fff;display:flex;align-items:center;justify-content:center;font-size:56px;font-weight:900;white-space:nowrap"><span style="opacity:${gl.toFixed(3)}">보장 금액</span></div>`;
    h += at(0, BY, W, `<div class="row" style="gap:14px;flex-wrap:nowrap;width:${W}px;height:${BH}px"><div style="width:${(SW * e3(gbar)).toFixed(1)}px;height:${BH}px;flex:0 0 auto">${inner}</div>${opt > 0 ? `<div style="flex:1;height:${BH}px;border-radius:20px;background:repeating-linear-gradient(45deg,#C9D2E0 0 14px,#E3E8F0 14px 28px);display:flex;align-items:center;justify-content:center;gap:12px;font-size:50px;font-weight:900;color:${GRY};white-space:nowrap;opacity:${cl(opt * 1.5, 0, 1).toFixed(3)}">옵션${optX > 0 ? `<span style="color:${RD};font-size:60px;${popS(optX)}">✕</span>` : ''}</div>` : ''}</div>`);
    /* 10/25 검수(알약 글이 나레이션 문장 되풀이 · 1초만 보임): 문장 알약 뺌 — 7단계 '곱해서'는 구간마다 '× 비율' 표시만 */
    if (st === 7 && mul > 0) { const sw = (SW - 2 * gap_) / 3;
      [0, 1, 2].forEach(k => { h += at(k * (sw + gap_), PY - 10, sw, `<div style="text-align:center;font-size:48px;font-weight:900;color:#B07A00;white-space:nowrap">× 비율</div>`, popS(cl(mul * 1.4 - k * .2, 0, 1))); }); }
    frame(s, lt, W, H, h);
  };

  /* ── feecalc: 이적료 구간 계산 (10/25 사용자 "계산한 것도 텍스트로 떼우는 게 아니라 다른 거랑 같이 모션그래픽으로") ──
     한 묶음(chain): zones(구간·비율) → 선수(보장 금액 막대가 구간 위로 차오름 → 구간마다 곱한 금액 + 사이에 '+' → 맨 위 오른쪽 '= 이적료') → cmp(보장 vs 이적료)
     10/25 사용자 "5천만 달러까지는 이야기하고 있는데 왜 막대에는 5천만 달러가 안 써져 있어 / 2500만 달러도" → 칸의 끝 금액은 그 칸과 같이 뜬다
     10/25 사용자 "전체적으로 너무 위로 올라가 있어" → 합계를 맨 아래 따로 두지 않고 이름 줄 오른쪽에(아래 빈 자리 없음), 높이 = 실제 내용 */
  const MAN = v => { v = Math.round(v * 10) / 10; const ek = Math.floor(v / 10000), m = Math.floor(v - ek * 10000), ch = Math.round((v - Math.floor(v)) * 10);
    return (ek ? ek + '억' + (m ? ' ' : '') : '') + (m ? m + '만' : (ek ? '' : '')) + (ch ? ' ' + ch + '천' : ''); };
  SCENE.feecalc = (lt, s) => {
    const A = mkA(s);
    const PR = s._prev && s._prev.type === 'feecalc' ? s._prev : null;
    let h = '';
    if (s.mode === 'cmp') {
      const pq = A(1, s.pctAt ?? 3, .5), rows = s.rows || [], MX = Math.max(...rows.map(r => r.amt)), RH = 210, W = 1640, LW = 400, BWm = 860, fq = A(1, s.feeAt ?? 1, .7), H = rows.length * RH - 50;
      rows.forEach((r, i) => { const q = A(1, r.at ?? 0, .6), y = i * RH, src = photoSrc(r.img);
        h += at(0, y + 10, 0, `<div class="row" style="gap:20px;align-items:center;flex-wrap:nowrap;width:${LW}px"><div style="position:relative;width:130px;height:130px;border-radius:50%;overflow:hidden;border:4px solid #fff;box-shadow:0 8px 20px rgba(18,22,31,.18);background:#E9EDF3;flex:0 0 auto">${src ? faceImg(src, r, '50% 18%') : ''}</div><b style="font-size:56px;font-weight:900;white-space:nowrap">${esc(r.name)}</b></div>`, rise_(q));
        const gw = BWm * r.amt / MX * e3(q), fw = Math.max(10, BWm * r.fee / MX) * e3(fq);
        h += at(LW, y, 0, `<div class="row" style="gap:18px;align-items:center;flex-wrap:nowrap"><div style="width:${gw.toFixed(1)}px;height:64px;border-radius:0 32px 32px 0;background:#9DB0CC"></div><b style="font-size:42px;font-weight:900;color:${GRY};white-space:nowrap;opacity:${cl(q * 2 - 1, 0, 1).toFixed(3)}">보장 ${MAN(r.amt)} 달러</b></div>`);
        h += at(LW, y + 82, 0, `<div class="row" style="gap:18px;align-items:center;flex-wrap:nowrap"><div style="width:${fw.toFixed(1)}px;height:64px;border-radius:0 32px 32px 0;background:${GOLD}"></div><b style="font-size:48px;font-weight:900;color:#B57800;white-space:nowrap;opacity:${cl(fq * 2 - .6, 0, 1).toFixed(3)}">이적료 ${MAN(r.fee)} 달러</b>${s.pct ? `<b style="font-size:44px;font-weight:900;color:#1B2433;white-space:nowrap;margin-left:10px;${popS(pq)}">= 보장의 ${String(+(100 * r.fee / r.amt).toFixed(1))}%</b>` : ''}</div>`);   /* 10/25 검수("20%를 넘지 않았어요"인데 화면에 비율 없음): 줄마다 보장 대비 비율 */
      });
      return frame(s, lt, W, H, h);
    }
    /* 10/25 사용자 "이런 거 눈에 하나도 안 들어와" → 글 대신 그림: 파란 계약 막대가 구간 덩어리로 → 덩어리마다 ↓ × 비율 → 그 비율만큼 작은 금색 조각 → 조각이 모여 이적료 */
    const W = 1620, TWD = 1620, M = 12000, px = v => TWD * Math.min(v, M) / M;
    const Z = [[0, 2500, .20, '20%', '#2F6BFF', '2500만 달러까지'], [2500, 5000, .175, '17.5%', '#4F7FE0', '5000만 달러까지'], [5000, M, .15, '15%', '#7F9AC9', '5000만 달러 넘는 부분']];
    const zAt = s.zAt || [-1, -1, -1], zq = i => zAt[i] < 0 ? 1 : A(1, zAt[i], .5);
    const p = s.p;
    if (!p) {   /* 구간만 — 같은 크기 카드 세 장(말하는 순간 그 카드가: 범위 + 비율) */
      const CW = 530, CG = 36, CH = 300, W2 = 3 * CW + 2 * CG;
      const RNG = ['2500만 달러까지', '2500만~5000만 달러', '5000만 달러 넘는 부분'];
      Z.forEach(([a, b, r, t, c], i) => { const q = zq(i), x = i * (CW + CG);
        h += at(x, 0, 0, `<div class="col" style="width:${CW}px;height:${CH}px;border-radius:28px;background:#fff;box-shadow:0 14px 34px rgba(18,22,31,.12);border:5px solid ${c};box-sizing:border-box;align-items:center;justify-content:center;gap:18px"><b style="font-size:40px;font-weight:900;color:${INK};white-space:nowrap">${RNG[i]}</b><span style="background:${c};color:#fff;border-radius:24px;padding:4px 40px;font-size:96px;font-weight:900;line-height:1.15">${t}</span></div>`, popS(q)); });
      return frame(s, lt, W2, CH, h);
    }
    const HD = 120, CAPY = HD + 24, TY = HD + 40, TH = 130, AY = TY + TH, GY = AY + 128, GH = 84, H = GY + GH + 72;
    const src = photoSrc(p.img), fin = A(1, p.fillAt ?? 0.2, .9), a0 = PR && PR.p ? PR.p.amt : 0, amt = a0 + (p.amt - a0) * e3(fin), keep = PR && PR.p && PR.p.name === p.name;
    h += at(0, 0, 0, `<div class="row" style="gap:20px;align-items:center;flex-wrap:nowrap;height:${HD}px">${src ? `<div style="position:relative;width:116px;height:116px;border-radius:50%;overflow:hidden;border:4px solid #fff;box-shadow:0 8px 20px rgba(18,22,31,.18);background:#E9EDF3;flex:0 0 auto">${faceImg(src, p, '50% 18%')}</div>` : ''}<b style="font-size:62px;font-weight:900;white-space:nowrap">${esc(p.name)}</b>${pill('보장 ' + MAN(p.amt) + ' 달러', '#2F6BFF', 44)}</div>`, keep ? '' : rise_(A(1, 0, .45)));
    /* 흐린 구간 칸(비율은 ↓ 표시에) */
    Z.forEach(([a, b, r, t, c], i) => { const x = px(a), w = px(b) - px(a);
      h += at(x, TY, 0, `<div style="width:${w - 8}px;height:${TH}px;border-radius:16px;background:${c}14;border:3px dashed ${c}88;box-sizing:border-box"></div>`); });
    /* 파란 계약 막대 — 구간 덩어리, 넓으면 금액을 안에 */
    const parts = Z.map(([a, b, r, t, c]) => ({ a, b, r, t, c, v: Math.max(0, Math.min(p.amt, b) - a) })).filter(z => z.v > 0);
    Z.forEach(([a, b, r, t, c], i) => { if (amt <= a) return; const e = Math.min(amt, b), w = Math.max(0, px(e) - px(a) - 8), full = Math.min(p.amt, b) - a;
      h += at(px(a), TY, 0, `<div style="width:${w.toFixed(1)}px;height:${TH}px;border-radius:16px;background:${c};display:flex;align-items:center;justify-content:center;color:#fff;font-size:50px;font-weight:900;white-space:nowrap;overflow:hidden">${w > 220 && fin >= 1 ? MAN(full) : ''}</div>`); });
    /* ↓ × 비율 → 금색 조각(덩어리 × 비율 만큼의 폭) */
    const pa = p.partAt || [], sq = A(1, p.sumAt ?? 2, .8), tot = parts.reduce((t, z) => t + z.v * z.r, 0);
    let bx = [], prevR = -1e9, prevLR = -1e9;
    parts.forEach((z, i) => { const sw = px(z.a + z.v) - px(z.a) - 8, c0 = px(z.a) + sw / 2, bt = (sw > 220 ? '' : MAN(z.v) + ' ') + '× ' + z.t, bw = TW2(bt, 42) + 52;
      let l = Math.max(0, c0 - bw / 2); if (l < prevR + 16) l = prevR + 16; prevR = l + bw;
      const lw = TW2(MAN(z.v * z.r), 50); let lc = c0; if (lc - lw / 2 < prevLR + 28) lc = prevLR + 28 + lw / 2; prevLR = lc + lw / 2;   /* 금액 글끼리 안 붙게 */
      bx.push({ c0, l, bw, bt, sw, lc }); });
    let acc = 0;
    parts.forEach((z, i) => { const q = A(1, pa[i] ?? 1, .7), B_ = bx[i], gw = Math.max(34, B_.sw * z.r), g0 = B_.c0 - gw / 2, gx = g0 + (acc - g0) * e3(sq), lab = MAN(z.v * z.r);
      acc += gw;
      const aq = cl(q * 2, 0, 1), gq = cl(q * 2 - .6, 0, 1);
      h += `<svg width="40" height="${GY - AY}" style="position:absolute;left:${(B_.c0 - 20).toFixed(1)}px;top:${AY}px;overflow:visible;opacity:${(aq * (1 - sq)).toFixed(3)}"><line x1="20" y1="6" x2="20" y2="${(6 + (GY - AY - 22) * e3(aq)).toFixed(1)}" stroke="${z.c}" stroke-width="6" stroke-linecap="round"/><path d="M8,${GY - AY - 22} L20,${GY - AY - 6} L32,${GY - AY - 22} Z" fill="${z.c}" opacity="${aq >= 1 ? 1 : 0}"/></svg>`;
      h += at(B_.l, AY + 30, B_.bw, `<div style="text-align:center">${pill(B_.bt, z.c, 42)}</div>`, `opacity:${(cl(aq * 1.6, 0, 1) * (1 - sq)).toFixed(3)}`);
      h += at(gx, GY, 0, `<div style="width:${gw.toFixed(1)}px;height:${GH}px;border-radius:12px;background:${GOLD};box-shadow:0 6px 14px rgba(232,161,0,.35)"></div>`, `opacity:${cl(gq * 2, 0, 1).toFixed(3)};transform:scale(${(.4 + .6 * e3(gq)).toFixed(3)})`);
      h += at(B_.lc - 140, GY + GH + 8, 280, `<div style="text-align:center;font-size:50px;font-weight:900;color:#B57800;white-space:nowrap">${lab}</div>`, `opacity:${(gq * (1 - sq)).toFixed(3)}`); });
    if (sq > 0) h += at(acc + 26, GY + GH / 2 - 44, 0, `<div class="row" style="gap:16px;align-items:center;flex-wrap:nowrap"><b style="font-size:56px;color:${GRY}">=</b><span style="background:${GOLD};color:#fff;border-radius:24px;padding:8px 34px;font-size:64px;font-weight:900;white-space:nowrap">이적료 ${MAN(tot)} 달러</span></div>`, popS(sq) + ';transform-origin:left center');
    frame(s, lt, W, H, h);
  };

  /* duel 아래 로고 줄: s.logos [{team, at}] — 같은 맞대결 장면이 이어지며 찾아온 구단 로고가 하나씩 */
  const _duel = SCENE.duel;
  SCENE.duel = (lt, s) => { _duel(lt, s);
    if (s.badge) { const q = (s.badge.at ?? 0) < 0 ? 1 : (() => { const t = TT(s, s.badge.at ?? 0); return t == null ? 0 : cl(t / (.45 * SPD), 0, 1); })();
      const col = document.getElementById('body').firstElementChild; if (col) col.insertAdjacentHTML('beforeend', `<div style="margin-top:40px;font-size:46px;font-weight:900;color:#1B2433;white-space:nowrap;${popS(q)}">${esc(s.badge.t)}</div>`); }
    if (!s.logos) return;
    const row = `<div class="row" style="gap:56px;justify-content:center;margin-top:20px;flex-wrap:nowrap">${s.logos.map(x => { const q = (x.at ?? 0) < 0 ? 1 : (() => { const t = TT(s, x.at ?? 0); return t == null ? 0 : cl(t / (.45 * SPD), 0, 1); })();
      return `<div class="col" style="align-items:center;gap:6px;${pop(q)}">${LOGOI(x.team, 104)}<b style="font-size:38px;font-weight:900;white-space:nowrap">${esc(x.t || x.team)}</b></div>`; }).join('')}</div>`;
    const body = document.getElementById('body'), col = body.firstElementChild; if (col) col.insertAdjacentHTML('beforeend', row); };
  Object.assign(MOTION, { roads: () => 1, dayfill: () => 1, lockout: () => 1, feerule: () => 1, feecalc: () => 1 });
})();
/* @@MOT1025END */
'''
for p in sys.argv[1:]:
    s = io.open(p, encoding='utf-8').read()
    s = re.sub(r'/\* @@MOT1025 .*?/\* @@MOT1025END \*/\n', '', s, flags=re.S)
    i = s.index('function render(t) {')
    s = s[:i] + BLOCK + s[i:]
    io.open(p, 'w', encoding='utf-8').write(s); print('injected', p)
