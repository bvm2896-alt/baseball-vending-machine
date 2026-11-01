/* @@VISB1101 11/1 20:17 사용자 "텍스트로 떼우는 거 없이 다 그림과 그래픽으로, 진짜 직관적으로" — 1차전 승부 예측 장(p2~p19) 전용 그래픽 장면.
   공통: at = 말하는 호흡(그 호흡에 뜸), -1 = 앞 장면에서 이미 보임, 50 이상 = 이 장면에선 안 뜸. 글자는 6자 이내 이름표만. */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb == null ? 0 : fb);
  const C = x => x < 0 ? 0 : x > 1 ? 1 : x;
  const E = t => 1 - Math.pow(1 - C(t), 3);
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  const LG = (n, px, st = '') => { const tt = T(n); return tt && LOGO[tt.code] ? `<img src="${LOGO[tt.code]}" style="width:${px}px;height:${px}px;object-fit:contain;${st}">` : `<div style="width:${px}px;height:${px}px"></div>`; };
  const NV = '#12161F', SS = '#074CA1', SOFT = '#EEF1F5', MUTE = '#9AA3B2', ORG = '#F08C00';
  /* ── 그림(SVG) ── */
  const IC = {
    trophy: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M18 8h28v10c0 10-6 18-14 18S18 28 18 18z" fill="${c}"/><path d="M18 12H8c0 10 5 15 12 15M46 12h10c0 10-5 15-12 15" fill="none" stroke="${c}" stroke-width="5"/><rect x="28" y="36" width="8" height="10" fill="${c}"/><rect x="18" y="46" width="28" height="8" rx="3" fill="${c}"/></svg>`,
    x: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M18 18L46 46M46 18L18 46" stroke="${c}" stroke-width="9" stroke-linecap="round"/></svg>`,
    check: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M14 34L27 47L51 19" fill="none" stroke="${c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    mic: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><rect x="22" y="6" width="20" height="34" rx="10" fill="${c}"/><path d="M14 30c0 10 8 18 18 18s18-8 18-18" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round"/><rect x="29" y="48" width="6" height="8" fill="${c}"/><rect x="20" y="55" width="24" height="5" rx="2.5" fill="${c}"/></svg>`,
    cal: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><rect x="6" y="10" width="52" height="48" rx="8" fill="#fff" stroke="${c}" stroke-width="4"/><rect x="6" y="10" width="52" height="14" rx="6" fill="${c}"/><rect x="16" y="4" width="6" height="12" rx="3" fill="${c}"/><rect x="42" y="4" width="6" height="12" rx="3" fill="${c}"/></svg>`,
    play: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><rect x="4" y="12" width="56" height="40" rx="12" fill="${c}"/><path d="M27 22L42 32L27 42z" fill="#fff"/></svg>`,
    glove: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M14 30c0-6 2-14 6-18 2-2 5-1 5 2v12l2-16c0-3 4-4 5-1l1 15 2-14c0-3 4-3 5 0l0 15 3-10c1-3 5-2 5 1l-3 18c-1 9-7 16-16 16h-4c-9 0-13-8-13-20z" fill="${c}"/><path d="M14 34c-4 0-6 3-5 6l6 10" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round"/></svg>`,
    bat: (c, px) => `<div style="width:${px}px;height:${px}px">${ICON.bat(c)}</div>`,
    pen: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><circle cx="20" cy="16" r="8" fill="${c}"/><path d="M8 50c0-12 5-20 12-20s12 8 12 20z" fill="${c}"/><circle cx="44" cy="16" r="8" fill="${c}" opacity=".55"/><path d="M32 50c0-12 5-20 12-20s12 8 12 20z" fill="${c}" opacity=".55"/><rect x="4" y="52" width="56" height="6" rx="3" fill="${c}"/></svg>`,
    battery: (c, px, lv = .2) => `<svg width="${px}" height="${px * .6}" viewBox="0 0 64 38"><rect x="2" y="4" width="52" height="30" rx="6" fill="#fff" stroke="${c}" stroke-width="4"/><rect x="56" y="13" width="6" height="12" rx="2" fill="${c}"/><rect x="7" y="9" width="${Math.max(4, 42 * lv)}" height="20" rx="3" fill="${c}"/></svg>`,
    link: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><rect x="4" y="22" width="26" height="20" rx="10" fill="none" stroke="${c}" stroke-width="6"/><rect x="34" y="22" width="26" height="20" rx="10" fill="none" stroke="${c}" stroke-width="6" transform="rotate(14 47 32)"/><path d="M30 14l2 8M36 12l-2 9" stroke="${RED}" stroke-width="4" stroke-linecap="round"/></svg>`,
    home: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M8 30L32 10L56 30V56H8z" fill="${c}"/><rect x="26" y="38" width="12" height="18" rx="2" fill="#fff"/></svg>`,
    q: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="${c}"/><text x="32" y="45" text-anchor="middle" font-size="38" font-weight="900" fill="#fff" font-family="inherit">?</text></svg>`,
    warn: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M32 6L60 56H4z" fill="${c}"/><rect x="29" y="22" width="6" height="18" rx="3" fill="#fff"/><circle cx="32" cy="47" r="3.6" fill="#fff"/></svg>`,
    flag: (c, px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><rect x="10" y="4" width="5" height="56" rx="2" fill="${NV}"/><path d="M15 6h38l-9 11 9 11H15z" fill="${c}"/></svg>`,
  };
  const pill = (t, bg, fg = '#fff', fs = 34, extra = '') => `<div style="height:${Math.round(fs * 1.75)}px;padding:0 ${Math.round(fs * .75)}px;border-radius:999px;background:${bg};color:${fg};font-size:${fs}px;font-weight:900;display:inline-flex;align-items:center;gap:10px;white-space:nowrap;letter-spacing:-.5px;${extra}">${t}</div>`;
  const popS = (q, from = .6) => `opacity:${C(q * 2.5)};transform:scale(${from + (1 - from) * MK.E.outBack(C(q))})`;
  const sub = (lt, s) => s.sub ? `<div style="margin-top:6px;font-size:30px;font-weight:800;color:${MUTE};${pop(seg(lt, .05, .4))}">${esc(s.sub)}</div>` : '';

  /* ① vB_units: 팀 칸 N개 → 칸마다 그림이 채워짐(트로피/승/패/×). 큰 숫자 하나.
     {title, sub, n, slotAt, fillAt, fills:['trophy'|'win'|'loss'|'x'], big:{v, unit, at, c}} */
  SCENE.vB_units = (lt, s) => {
    const n = s.n || (s.fills || []).length, sq = AT(s, s.slotAt, .5, seg(lt, .1, .5)), fq = AT(s, s.fillAt, .8, 0);
    const W = n > 14 ? 74 : n > 10 ? 116 : 170, H = n > 14 ? 120 : n > 10 ? 170 : 200, G = n > 14 ? 8 : n > 10 ? 10 : 22;   /* 11/2 롱폼㉟: 21칸이 화면 밖으로 넘침 */
    let h = titleH(lt, s, 58, 6) + sub(lt, s);
    h += `<div class="row" style="gap:${G}px;margin-top:40px;justify-content:center">` + Array.from({ length: n }, (_, i) => {
      const f = (s.fills || [])[i] || '', a = C((sq - i * .03) * 2.2), b = C((fq * 1.4 - i * (.4 / n)) * 2.2);
      const col = f === 'trophy' ? GOLD : f === 'win' ? GREEN : f === 'loss' || f === 'outp' ? RED : '#C3CAD5';
      const bg = b > .02 ? (f === 'trophy' ? '#FFF6DA' : f === 'win' ? '#E6F6EC' : f === 'loss' || f === 'outp' ? '#FDECEC' : SOFT) : '#fff';
      const ic = f === 'trophy' ? IC.trophy(col, W * .62) : f === 'win' ? `<div style="font-size:${W * .5}px;font-weight:900;color:${col}">승</div>` : f === 'loss' ? `<div style="font-size:${W * .5}px;font-weight:900;color:${col}">패</div>` : f === 'outp' ? `<div style="position:relative;line-height:0"><svg width="${W * .7}" height="${W * .7}" viewBox="0 0 64 64"><circle cx="32" cy="17" r="10" fill="#9AA3B2"/><path d="M20 12 Q32 2 44 12 L46 15 L18 15Z" fill="#9AA3B2"/><path d="M14 60 Q14 32 32 32 Q50 32 50 60Z" fill="#9AA3B2"/></svg><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${IC.x(RED, W * .6)}</div></div>` : IC.x(col, W * .5);
      return `<div style="width:${W}px;height:${H}px;border-radius:24px;background:${bg};border:4px solid ${b > .02 ? col : LINE};display:flex;align-items:center;justify-content:center;box-shadow:0 10px 24px rgba(18,22,31,.07);opacity:${C(a * 2)};transform:translateY(${(1 - E(a)) * 30}px)">
        <div style="${popS(b, .3)}">${ic}</div></div>`;
    }).join('') + `</div>`;
    if (s.big) { const q = AT(s, s.big.at, .5, 0);
      h += `<div class="row" style="margin-top:46px;gap:18px;align-items:baseline;${popS(q, .7)}"><div class="num" style="font-size:150px;font-weight:900;letter-spacing:-5px;line-height:1;color:${s.big.c || NV}">${esc(s.big.v)}</div><div style="font-size:64px;font-weight:900;color:${s.big.c || NV}">${esc(s.big.unit || '')}</div></div>`; }
    wrapC(h);
  };

  /* ② vB_meter: 반원 저울 바늘 — 왼쪽 팀 ↔ 오른쪽 팀. 바늘 각도 from → to (−1 왼쪽 끝, +1 오른쪽 끝)
     {title, l, r, from, to, moveAt, lBadge:{t, at}, rBadge:{t, at}, crown:{side, at}} */
  SCENE.vB_meter = (lt, s) => {
    const K = s._same, mv = AT(s, s.moveAt, .9, 0), v = (s.from_ ?? 0) + ((s.to ?? 0) - (s.from_ ?? 0)) * MK.E.inOutCubic(mv);
    const R = 330, cx = 400, cy = 380, ang = v * 70 * Math.PI / 180, nx = cx + Math.sin(ang) * (R - 40), ny = cy - Math.cos(ang) * (R - 40);
    const cl = TC_(s.l), cr = TC_(s.r), wq = K ? 1 : seg(lt, .05, .6);
    const arc = (a0, a1, col, w) => { const p0 = [cx + Math.sin(a0) * R, cy - Math.cos(a0) * R], p1 = [cx + Math.sin(a1) * R, cy - Math.cos(a1) * R]; return `<path d="M${p0[0].toFixed(1)},${p0[1].toFixed(1)} A${R},${R} 0 0 1 ${p1[0].toFixed(1)},${p1[1].toFixed(1)}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`; };
    const r70 = 70 * Math.PI / 180;
    const svg = `<svg width="800" height="420" viewBox="0 0 800 420" style="overflow:visible;${K ? '' : MK.css.zoomIn(wq)}">
      ${arc(-r70, -0.03, cl, 54)}${arc(0.03, r70, cr, 54)}
      <line x1="${cx}" y1="${cy - R - 40}" x2="${cx}" y2="${cy - R + 40}" stroke="#fff" stroke-width="8"/>
      <line x1="${cx}" y1="${cy}" x2="${nx.toFixed(1)}" y2="${ny.toFixed(1)}" stroke="${NV}" stroke-width="16" stroke-linecap="round"/>
      <circle cx="${cx}" cy="${cy}" r="30" fill="${NV}"/><circle cx="${cx}" cy="${cy}" r="12" fill="#fff"/></svg>`;
    const side = (team, b, al) => { const bq = b ? (K && s._prev[al === 'l' ? 'lBadge' : 'rBadge'] && s._prev[al === 'l' ? 'lBadge' : 'rBadge'].t === b.t ? 1 : AT(s, b.at, .45, 0)) : 0;
      const cr_ = s.crown && s.crown.side === al ? AT(s, s.crown.at, .5, 0) : 0;
      return `<div class="col" style="width:300px;align-items:center;gap:18px;position:relative">
        <div style="position:absolute;top:-120px;${popS(cr_, .4)}">${IC.trophy(GOLD, 120)}</div>
        <div style="${K ? '' : MK.css.rise(seg(lt, .1, .5), 30)}">${LG(team, 210)}</div>
        <div style="height:66px">${b ? `<div style="${popS(bq)}">${pill(esc(b.t), b.bg || (al === 'l' ? cl : cr), '#fff', 36)}</div>` : ''}</div></div>`; };
    let h = titleH(lt, s, 58, 10, K && s._prev.title === s.title);
    h += `<div class="row" style="gap:10px;align-items:flex-end;margin-top:20px">${side(s.l, s.lBadge, 'l')}<div style="margin:0 -40px">${svg}</div>${side(s.r, s.rBadge, 'r')}</div>`;
    wrapC(h);
  };

  /* ③ vB_only: 한 팀(KT)의 상대 9팀 로고 — 다 흐리게, 한 팀만 크게 + 배지. {title, me, opps:[], hit, oppAt, hitAt, badge} */
  SCENE.vB_only = (lt, s) => {
    const oq = AT(s, s.oppAt, .6, seg(lt, .1, .5)), hq = AT(s, s.hitAt, .5, 0), opps = s.opps || [];
    let h = titleH(lt, s, 58, 30);
    h += `<div class="row" style="gap:40px;align-items:center">
      <div class="col" style="align-items:center;gap:10px;${MK.css.rise(seg(lt, .05, .5), 30)}">${LG(s.me, 220)}</div>
      <div style="width:6px;height:360px;border-radius:3px;background:${LINE}"></div>
      <div class="row" style="gap:26px;flex-wrap:wrap;width:1060px;justify-content:center;align-items:center">` +
      opps.map((t, i) => { const a = C((oq - i * .05) * 2.2), hit = t === s.hit;
        const dim = hit ? 1 - .0 : 1 - .65 * hq;
        return `<div class="col" style="width:190px;height:${hit ? 250 : 170}px;align-items:center;justify-content:center;gap:10px;opacity:${(C(a * 2) * dim).toFixed(3)};transform:scale(${(hit ? 1 + .35 * MK.E.outBack(hq) : 1).toFixed(3)});filter:grayscale(${hit ? 0 : hq})">
          ${LG(t, 140)}${hit ? `<div style="${popS(hq)}">${pill(`${IC.x('#fff', 34)}${esc(s.badge || '')}`, RED, '#fff', 34)}</div>` : ''}</div>`; }).join('') + `</div></div>`;
    wrapC(h);
  };

  /* ④ vB_rings: 원 게이지 여러 개(퍼센트). {title, sub, items:[{k, v, dec, c, at, down:{at}}]} */
  SCENE.vB_rings = (lt, s) => {
    let h = titleH(lt, s, 58, 6) + sub(lt, s);
    h += `<div class="row" style="gap:150px;margin-top:96px;align-items:flex-start">` + (s.items || []).map(x => {
      const q = AT(s, x.at, .9, 0), dq = x.down ? AT(s, x.down.at, .5, 0) : 0, v = +x.v;
      return `<div class="col" style="align-items:center;gap:18px;opacity:${C(q * 3)}">
        <div style="position:relative;width:480px;height:480px">${MK.gauge(v, q, 200, 40, x.c, '#E6EAF0')}
          <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center"><div class="num" style="font-size:96px;font-weight:900;letter-spacing:-4px;color:${x.c}">${MK.count(v, q, x.dec ?? 1)}<span style="font-size:52px">%</span></div></div>
          ${x.down ? `<div style="position:absolute;left:0;right:0;top:-74px;display:flex;justify-content:center;${popS(dq, .4)}">${pill(`<svg width="34" height="34" viewBox="0 0 64 64"><path d="M32 58L6 26h16V6h20v20h16z" fill="#fff"/></svg>${esc(x.down.t || '')}`, RED, '#fff', 36)}</div>` : ''}</div>
        <div style="font-size:60px;font-weight:900;letter-spacing:-1px">${esc(x.k)}</div></div>`; }).join('') + `</div>`;
    wrapC(h);
  };

  /* ⑤ vB_split: 두 팀 확률 막대(한 줄) — 가운데 50% 선, 경계가 from → to 로 밀림. {title, l, r, from, to, moveAt, push:{t, at}, label:{v, at}} */
  SCENE.vB_split = (lt, s) => {
    const W = 1500, mv = AT(s, s.moveAt, .9, 0), v = s.from_ + (s.to - s.from_) * MK.E.inOutCubic(mv), cl = TC_(s.l), cr = TC_(s.r);
    const pq = s.push ? AT(s, s.push.at, .45, 0) : 0, lq = s.label ? AT(s, s.label.at, .5, 0) : 0, x = W * v / 100;
    let h = titleH(lt, s, 58, 50);
    h += `<div class="row" style="width:${W}px;justify-content:space-between;margin-bottom:22px">${LG(s.l, 150)}${LG(s.r, 150)}</div>
      <div style="position:relative;width:${W}px;height:150px;border-radius:75px;overflow:hidden;background:${cr};box-shadow:0 14px 34px rgba(18,22,31,.12);${MK.css.zoomIn(seg(lt, .05, .5))}">
        <div style="position:absolute;left:0;top:0;bottom:0;width:${x.toFixed(1)}px;background:${cl}"></div>
        <div style="position:absolute;left:${W / 2 - 4}px;top:-10px;bottom:-10px;width:8px;background:#fff;opacity:.95"></div>
        ${s.label ? `<div class="num" style="position:absolute;left:44px;top:0;bottom:0;display:flex;align-items:center;font-size:84px;font-weight:900;color:#fff;letter-spacing:-3px;opacity:${C(lq * 2)}">${esc(s.label.v)}<span style="font-size:44px">%</span></div>` : ''}${s.rlabel ? `<div class="num" style="position:absolute;right:44px;top:0;bottom:0;display:flex;align-items:center;font-size:84px;font-weight:900;color:#fff;letter-spacing:-3px;opacity:${C(AT(s, s.rlabel.at, .5, 0) * 2)}">${esc(s.rlabel.v)}<span style="font-size:44px">%</span></div>` : ''}</div>
      <div style="position:relative;width:${W}px;height:150px">
        <div class="num" style="position:absolute;left:${W / 2 - 60}px;width:120px;top:16px;text-align:center;font-size:38px;font-weight:900;color:${MUTE}">반반</div>
        ${s.push ? `<div style="position:absolute;left:${(x - 150).toFixed(1)}px;top:56px;width:300px;display:flex;justify-content:center;${popS(pq, .4)}">${pill(`${IC.pen('#fff', 46)}${esc(s.push.t)}`, ORG, '#fff', 44)}</div>` : ''}</div>`;
    wrapC(h);
  };

  /* ⑥ vB_three: 번호 카드 3장(그림 + 짧은 이름표). {title, items:[{n, icon, team, k, at}], focus} — focus 있으면 그 카드만 밝게 */
  SCENE.vB_three = (lt, s) => {
    let h = titleH(lt, s, 58, 40);
    h += `<div class="row" style="gap:50px">` + (s.items || []).map((x, i) => { const q = AT(s, x.at, .5, seg(lt, .15 + i * .15, .5));
      return `<div class="col" style="width:440px;height:470px;border-radius:40px;background:#fff;border:6px solid ${LINE};box-shadow:0 18px 44px rgba(18,22,31,.10);align-items:center;justify-content:center;gap:26px;position:relative;${MK.css.rise(q, 50)}">
        <div style="position:absolute;top:-34px;${popS(q, .5)}">${pill(esc(x.n), NV, '#fff', 36)}</div>
        <div class="row" style="gap:10px;align-items:center">${x.team ? LG(x.team, 110) : ''}${IC[x.icon](x.c || NV, 150)}</div>
        <div style="font-size:58px;font-weight:900;letter-spacing:-1.5px;white-space:nowrap">${esc(x.k)}</div></div>`; }).join('') + `</div>`;
    wrapC(h);
  };

  /* ⑦ vB_inn: 이닝 띠 1~9 — 줄마다 선발(팀 색)·불펜(주황) 채움, 5회 깃발. {title, team, rows:[{k, icon, sp, pen, at, penAt, mark:'ok'|'bad', markAt}], line:{inn, at}} */
  SCENE.vB_inn = (lt, s) => {
    const CW = 132, col = TC_(s.team), rows = s.rows || [], lq = s.line ? AT(s, s.line.at, .5, 0) : 0;
    let h = titleH(lt, s, 58, 70);
    h += `<div class="col" style="gap:26px;position:relative">`;
    h += `<div class="row" style="gap:6px;margin-left:300px">` + Array.from({ length: 9 }, (_, k) => `<div class="num" style="width:${CW}px;text-align:center;font-size:40px;font-weight:900;color:${s.line && k + 1 === s.line.inn ? NV : MUTE}">${k + 1}회</div>`).join('') + `</div>`;
    rows.forEach((r, ri) => {
      const q = AT(s, r.at, .9, 0), pq = r.pen ? AT(s, r.penAt, .9, 0) : 0, mq = r.mark ? AT(s, r.markAt, .45, 0) : 0;
      const cells = Array.from({ length: 9 }, (_, k) => {
        const spF = C(r.sp - k), spQ = C(q * (r.sp + 1) - k), fillSp = Math.min(spF, spQ);
        const penF = r.pen && k + 1 > Math.floor(r.sp) ? C((pq * (9 - r.sp + 1)) - (k - r.sp)) : 0;
        return `<div style="position:relative;width:${CW}px;height:110px;border-radius:18px;background:${SOFT};overflow:hidden">
          <div style="position:absolute;left:0;top:0;bottom:0;width:${(fillSp * 100).toFixed(1)}%;background:${col}"></div>
          ${r.pen && k + 1 > r.sp - 1 ? `<div style="position:absolute;left:${(k < r.sp ? (r.sp - k) * 100 : 0).toFixed(1)}%;top:0;bottom:0;width:${(Math.min(1, penF) * (k < r.sp ? (1 - (r.sp - k)) : 1) * 100).toFixed(1)}%;background:${ORG}"></div>` : ''}</div>`; }).join('');
      h += `<div class="row" style="gap:20px;align-items:center;opacity:${C(q * 4)}">
        <div class="row" style="width:280px;gap:14px;align-items:center;justify-content:flex-end">${r.icon ? IC[r.icon](r.ic || col, 70) : ''}<div style="font-size:44px;font-weight:900;white-space:nowrap">${esc(r.k)}</div></div>
        <div class="row" style="gap:6px">${cells}</div>
        <div style="width:90px;${popS(mq, .4)}">${r.mark === 'ok' ? IC.check(GREEN, 84) : r.mark === 'bad' ? IC.x(RED, 84) : ''}</div></div>`;
      if (r.pen) h += `<div class="row" style="margin-left:${300 + (Math.floor(r.sp) + 2) * (CW + 6) + 30}px;margin-top:-14px;gap:12px;align-items:center;${popS(pq, .6)}">${IC.pen(ORG, 60)}${pill('불펜 조기 투입', ORG, '#fff', 32)}</div>`;
    });
    if (s.line) { const lx = 300 + 20 + s.line.inn * (CW + 6) - 6 + 3;
      h += `<div style="position:absolute;left:${lx}px;top:40px;bottom:-10px;width:8px;border-radius:4px;background:${NV};opacity:${C(lq * 2)}"></div>
        <div style="position:absolute;left:${lx - 10}px;top:-66px;${popS(lq, .4)}">${IC.flag(GOLD, 64)}</div>`; }
    h += `</div>`;
    wrapC(h);
  };

  /* ⑧ vB_pen: 7·8·9회 불펜 싸움 — 두 팀 줄. 칸마다 그림(crack=금 간 칸 · battery=배터리 부족 · ok=단단), 오른쪽 짧은 이름표, 마지막 호흡에 경고.
     {title, rows:[{team, cells:['crack'|'battery'|'ok'], t, at}], warnAt, warnT} */
  SCENE.vB_pen = (lt, s) => {
    const wq = AT(s, s.warnAt, .7, 0), shake = s.warnAt != null && wq > 0 && wq < 1 ? Math.sin(wq * Math.PI * 6) * 12 * (1 - wq) : 0;
    let h = titleH(lt, s, 58, 30);
    h += `<div class="col" style="gap:26px;align-items:center">`;
    h += `<div class="row" style="gap:16px;margin-right:${300 + 16}px;margin-left:250px">` + [7, 8, 9].map(n => `<div class="num" style="width:290px;text-align:center;font-size:52px;font-weight:900">${n}회</div>`).join('') + `</div>`;
    (s.rows || []).forEach(r => { const q = AT(s, r.at, .7, 0), cc = TC_(r.team);
      h += `<div class="row" style="gap:16px;align-items:center;opacity:${C(q * 3)};transform:translateX(${shake.toFixed(1)}px)">
        <div style="width:234px;display:flex;justify-content:center">${LG(r.team, 160)}</div>
        ${(r.cells || []).map((c, k) => { const cq = C((q - .2 - k * .15) * 2.5);
          const bad = c !== 'ok';
          return `<div style="position:relative;width:290px;height:160px;border-radius:26px;background:${cc};display:flex;align-items:center;justify-content:center;opacity:${C((q - k * .1) * 2.5)}">${IC.pen('rgba(255,255,255,.9)', 96)}
            <div style="position:absolute;right:-14px;top:-18px;${popS(cq, .4)}">${c === 'crack' ? `<div style="width:84px;height:84px;border-radius:50%;background:${RED};display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px rgba(229,72,77,.35)"><svg width="54" height="54" viewBox="0 0 64 64"><path d="M34 4L22 30h14L26 60" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>`
              : c === 'battery' ? `<div style="width:110px;height:84px;border-radius:22px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px rgba(18,22,31,.18)">${IC.battery(RED, 84, .2)}</div>`
              : `<div style="width:84px;height:84px;border-radius:50%;background:${GREEN};display:flex;align-items:center;justify-content:center">${IC.check('#fff', 60)}</div>`}</div></div>`; }).join('')}
        <div style="width:300px;display:flex;${popS(C((q - .5) * 2), .5)}">${pill(esc(r.t), RED, '#fff', 38)}</div></div>`; });
    h += `<div class="row" style="gap:18px;align-items:center;margin-top:16px;${popS(wq, .5)}">${IC.warn(GOLD, 80)}${pill(esc(s.warnT || ''), NV, '#fff', 40)}</div></div>`;
    wrapC(h);
  };

  /* ⑨ vB_branch: 1차전 → 위(삼성 승) / 아래(KT 승) 갈래. {title, up:{team, steps:[{icon|logo|txt, t, at}]}, dn:{team, steps}} */
  SCENE.vB_branch = (lt, s) => {
    const K = s._same;
    const node = (st, pvst) => { const was = !!(pvst && pvst.at != null && pvst.at < 50); const q = was ? 1 : AT(s, st.at, .5, 0);
      const ico = st.logo ? LG(st.logo, 120) : st.icon === 'home' ? IC.home(st.c || SS, 110) : st.icon === 'q' ? `<div style="position:relative"><div style="opacity:${(1 - .85 * (st.strike ? AT(s, st.strike, .5, 0) : 0)).toFixed(3)}">${IC.q(MUTE, 110)}</div>${st.strike ? `<div style="position:absolute;inset:-6px;${popS(AT(s, st.strike, .5, 0), .4)}">${IC.check(GREEN, 122)}</div>` : ''}</div>` : st.icon === 'score' ? `<div class="num" style="font-size:76px;font-weight:900;letter-spacing:-2px;color:${NV}">${esc(st.v)}</div>` : '';
      return `<div class="col" style="width:250px;height:230px;border-radius:30px;background:#fff;border:5px solid ${st.hi ? GOLD : LINE};box-shadow:0 14px 34px rgba(18,22,31,.09);align-items:center;justify-content:center;gap:12px;${MK.css.rise(q, 30)}">${ico}<div style="font-size:38px;font-weight:900;white-space:nowrap;letter-spacing:-1px">${esc(st.t || '')}</div></div>`; };
    const arrow = (q, c) => `<svg width="70" height="40" viewBox="0 0 70 40" style="opacity:${C(q * 3)}"><path d="M4 20H56M44 8L60 20L44 32" fill="none" stroke="${c}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    const lane = (ln, pv, key) => { if (!ln) return ''; const lq = (K && pv) ? 1 : AT(s, ln.steps[0].at, .5, 0);
      return `<div class="row" style="gap:14px;align-items:center;opacity:${C(lq * 3)}">` + ln.steps.map((st, i) => (i ? arrow(AT(s, st.at, .4, 0) || (pv && pv.steps[i] && pv.steps[i].at < 0 ? 1 : 0), TC_(ln.team)) : '') + node(st, pv && pv.steps[i])).join('') + `</div>`; };
    const sq = K ? 1 : seg(lt, .05, .5);
    let h = titleH(lt, s, 58, 30, K && s._prev.title === s.title);
    h += `<div class="row" style="gap:40px;align-items:center">
      <div class="col" style="width:240px;height:240px;border-radius:50%;background:${NV};align-items:center;justify-content:center;gap:4px;${MK.css.zoomIn(sq)}"><div style="font-size:30px;font-weight:800;color:#AFC0DA">${esc(s.hubTop || '한국시리즈')}</div><div style="font-size:58px;font-weight:900;color:#fff">${esc(s.hub || '1차전')}</div></div>
      <div class="col" style="gap:50px;align-items:flex-start">${lane(s.up, K && s._prev.up, 'up')}${lane(s.dn, K && s._prev.dn, 'dn')}</div></div>`;
    wrapC(h);
  };

  /* ⑩ vB_next: 그림 3단 흐름(트로피? → 달력+마이크 → 선발 발표 → 다음 영상). {title, steps:[{icon, big, t, at, c}]} */
  SCENE.vB_next = (lt, s) => {
    let h = titleH(lt, s, 58, 50);
    h += `<div class="row" style="gap:26px;align-items:center">` + (s.steps || []).map((x, i) => { const q = AT(s, x.at, .5, 0);
      const ic = x.icon === 'cal' ? `<div style="position:relative;width:200px;height:200px">${IC.cal(SS, 200)}<div class="num" style="position:absolute;left:0;right:0;top:78px;text-align:center;font-size:58px;font-weight:900;color:${NV}">${esc(x.big || '')}</div><div style="position:absolute;right:-30px;bottom:-14px">${IC.mic(RED, 96)}</div></div>`
        : x.icon === 'pitchers' ? `<div class="row" style="gap:6px">${IC.glove(TC_('KT'), 110)}${IC.glove(TC_('삼성'), 110)}</div>`
        : x.icon === 'trophy' ? `<div style="position:relative">${IC.trophy(GOLD, 200)}<div style="position:absolute;right:-20px;top:-10px">${IC.q(SS, 80)}</div></div>`
        : IC[x.icon](x.c || RED, 200);
      return (i ? `<svg width="60" height="40" viewBox="0 0 60 40" style="opacity:${C(q * 3)}"><path d="M4 20H48M36 8L52 20L36 32" fill="none" stroke="${MUTE}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>` : '') +
        `<div class="col" style="width:330px;height:380px;border-radius:36px;background:#fff;border:5px solid ${x.hi ? GOLD : LINE};box-shadow:0 16px 40px rgba(18,22,31,.09);align-items:center;justify-content:center;gap:26px;${MK.css.rise(q, 40)}">${ic}<div style="font-size:46px;font-weight:900;white-space:nowrap;letter-spacing:-1px">${esc(x.t)}</div></div>`; }).join('') + `</div>`;
    wrapC(h);
  };

  Object.assign(MOTION, { vB_units: s => .8, vB_meter: s => .8, vB_only: s => .8, vB_rings: s => .8, vB_split: s => .8, vB_three: s => .8, vB_inn: s => .8, vB_pen: s => .8, vB_branch: s => .8, vB_next: s => .8 });
})();
/* @@VISB1101END */
