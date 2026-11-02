/* @@STYLE1101 11/1 롱폼㉟ — 사용자 "모션그래픽·인포그래픽·애니메이션 너무 같은 스타일로만 해서 식상해 — 다른 스타일로도, 전부 적절히 섞어서
   지루하지 않고 직관적이고 한눈에". 새 장면 네 종류(같은 chain 의 cont 장면이면 사진·틀은 그대로, 새 요소만 뜬다):
   hero  : 사진 중심 다큐 톤 — 흐린 같은 사진 배경 + 왼쪽 큰 인물 사진(천천히 확대) + 오른쪽 이름·큰 숫자 2~3개
           {img, name, team, kicker, stats:[{k, v, at, hi}], quote:{t, at}, stamp:{t, at}, focus}
   board : 야구장 전광판(검은 LED 판·점 무늬·호박색 숫자) — 큰 점수 한 줄 + 표 한 줄
           {title, big:{l:{team, v}, r:{team, v}, at, note}, cols:[..], rows:[{k, cells:[{t, team, at}]}], foot:{t, at}}
   clip  : 신문 스크랩 — 종이 조각이 기울어 떨어지며 붙는다(제목·날짜·짧은 본문·흑백 사진·따옴표 발언)
           {clips:[{date, head, body, quote, img, name, src, at, rot}]}
   chalk : 감독 작전판 — 짙은 초록 칠판에 분필 글씨가 왼쪽부터 써진다(계산·예상)
           {title, lines:[{t, at, c:'w'|'y'|'g'|'r', size, ind, rule}], circle:{line, at}} */
(() => {
  const e3 = x => 1 - Math.pow(1 - c01(x), 3);
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  const LG_ = (n, px, st = '') => { const c_ = (T(n) || {}).code; return LOGO[c_] ? `<img src="${LOGO[c_]}" style="width:${px}px;height:${px}px;object-fit:contain;display:block;${st}">` : ''; };
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  const wasIn = (s, key, x, keyf) => s._same && ((s._prev[key] || []).some(o => keyf(o) === keyf(x)));

  /* ── hero ── */
  SCENE.hero = (lt, s) => {
    const src = photoSrc(s.img), K = s._same, W = 1808, H = 700, PW = 760;
    const zin = K ? 1 : e3(seg(lt, 0, .6)), pim = (K || s.imgAt == null) ? 1 : c01(AT(s, s.imgAt, .5, 0) * 1.4), zoom = 1;   /* 11/1 사용자 "갈수록 사진 크기가 바뀌는 게 안 바뀌게" — 천천히 확대 없앰 */
    const tc = TC_(s.team || 'KT');
    const sts = s.stats || [];
    const statH = sts.map((x, i) => {
      const p = wasIn(s, 'stats', x, o => o.k + '|' + o.v) ? 1 : AT(s, x.at, .55, seg(lt, .5 + i * .3, .55));
      return `<div style="display:flex;flex-direction:column;align-items:flex-start;gap:2px;opacity:${c01(p * 1.6).toFixed(3)};transform:translateX(${((1 - e3(p)) * 60).toFixed(1)}px)">
        <div style="font-size:34px;font-weight:800;color:#AEB8C8;letter-spacing:-.5px;white-space:nowrap">${esc(x.k)}</div>
        <div class="num" style="font-size:${x.size || 104}px;font-weight:900;line-height:1;letter-spacing:-3px;white-space:nowrap;color:${x.hi ? '#FFD43B' : '#fff'}">${esc(x.v)}</div></div>`; }).join('');
    const q = s.quote ? AT(s, s.quote.at, .6, seg(lt, .8, .6)) : 0;
    const sp = s.stamp ? AT(s, s.stamp.at, .45, seg(lt, 1, .45)) : 0;
    const h = `<div style="position:relative;width:${W}px;height:${H}px;border-radius:36px;overflow:hidden;background:#0E1219;box-shadow:0 30px 60px rgba(10,14,24,.35);opacity:${zin.toFixed(3)}">
      ${src ? `<img src="${src}" style="position:absolute;inset:-40px;width:calc(100% + 80px);height:calc(100% + 80px);object-fit:cover;filter:blur(28px) brightness(.38) saturate(1.2)">` : ''}
      <div style="position:absolute;inset:0;background:linear-gradient(90deg, rgba(14,18,25,0) 30%, rgba(14,18,25,.75) 62%, rgba(14,18,25,.92))"></div>
      <div style="position:absolute;left:0;top:0;width:${PW}px;height:${H}px;overflow:hidden;opacity:${pim.toFixed(3)}">${src ? `<img src="${src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${esc(s.focus || '50% 18%')};transform:scale(${zoom.toFixed(4)});transform-origin:50% 30%">` : ''}
        <div style="position:absolute;inset:0;background:linear-gradient(90deg, rgba(14,18,25,0) 70%, rgba(14,18,25,.9))"></div>
        <div style="position:absolute;left:0;right:0;bottom:0;height:160px;background:linear-gradient(180deg, rgba(14,18,25,0), rgba(14,18,25,.85))"></div></div>
      <div style="position:absolute;left:0;top:0;width:12px;height:${H}px;background:${tc}"></div>
      <div style="position:absolute;left:${PW + 40}px;top:56px;right:56px;display:flex;flex-direction:column;align-items:flex-start;gap:26px;text-align:left">
        <div style="display:flex;align-items:center;gap:16px">${s.kicker ? `<span style="font-size:34px;font-weight:800;color:#fff;background:${tc};padding:6px 20px;border-radius:12px;white-space:nowrap">${esc(s.kicker)}</span>` : ''}</div>
        <div style="font-size:112px;font-weight:900;color:#fff;letter-spacing:-4px;line-height:1;opacity:${pim.toFixed(3)}">${esc(s.name || '')}</div>
        <div style="display:flex;gap:64px;align-items:flex-end;flex-wrap:wrap;margin-top:6px">${statH}</div>
        ${s.quote ? `<div style="max-width:880px;font-size:50px;font-weight:800;color:#FFE8A3;line-height:1.3;letter-spacing:-1px;opacity:${c01(q * 1.5).toFixed(3)};transform:translateY(${((1 - e3(q)) * 24).toFixed(1)}px)">${br(s.quote.t)}</div>` : ''}
      </div>
      ${s.stamp ? `<div style="position:absolute;right:56px;bottom:52px;border:6px solid #FFD43B;color:#FFD43B;border-radius:16px;padding:6px 22px;font-size:46px;font-weight:900;white-space:nowrap;transform:rotate(-4deg) scale(${sp <= 0 ? 1.5 : (1.5 - .5 * e3(sp)).toFixed(3)});opacity:${c01(sp * 2).toFixed(3)}">${esc(s.stamp.t)}</div>` : ''}
    </div>`;
    B(h);
  };

  /* ── board (전광판) ── */
  SCENE.board = (lt, s) => {
    const K = s._same, AMB = '#FFB020', W = 1640;
    const led = `background-color:#07090D;background-image:radial-gradient(rgba(255,255,255,.07) 1.4px, transparent 1.6px);background-size:9px 9px`;
    const glow = c => `color:${c};text-shadow:0 0 14px ${c}AA, 0 0 2px ${c}`;
    const pin = K ? 1 : e3(seg(lt, 0, .45));
    let inner = '';
    if (s.big) {
      const p = K && s._prev.big && JSON.stringify(s._prev.big) === JSON.stringify(s.big) ? 1 : AT(s, s.big.at, .6, seg(lt, .3, .6));
      const side = (x, al) => `<div style="display:flex;align-items:center;gap:26px;flex-direction:${al === 'r' ? 'row-reverse' : 'row'}">
          <div style="font-size:84px;font-weight:900;${glow('#fff')};white-space:nowrap">${esc(x.label || x.team)}</div></div>`;
      const roll = v => { const n = parseFloat(v); if (isNaN(n) || String(v).match(/[^\d.]/)) return esc(v); if (p <= 0) return '–'; return String(Math.round(n * e3(p))); };
      const bv = s.big.at != null && s.big.at >= 50 ? 0 : 1;
      inner += `<div style="display:flex;align-items:center;justify-content:space-between;width:${W - 120}px;margin:10px 0 6px;opacity:${bv}">
          ${side(s.big.l, 'l')}
          <div class="num" style="display:flex;align-items:center;gap:30px;font-size:190px;font-weight:900;line-height:1;${glow(AMB)}">
            <span>${roll(s.big.l.v)}</span><span style="font-size:120px;opacity:.7">:</span><span>${roll(s.big.r.v)}</span></div>
          ${side(s.big.r, 'r')}</div>`;
      if (s.big.note) inner += `<div style="font-size:44px;font-weight:800;${glow('#7CF29A')};opacity:${c01(p * 1.5).toFixed(3)};white-space:nowrap">${esc(s.big.note)}</div>`;
    }
    if (s.cols && s.cols.length) {
      const cw = Math.floor((W - 380) / s.cols.length);
      inner += `<div style="display:flex;flex-direction:column;gap:8px;margin-top:${s.big ? 26 : 6}px;border-top:3px solid rgba(255,176,32,.35);padding-top:20px">
        <div style="display:flex"><div style="width:300px"></div>${s.cols.map(c => `<div style="width:${cw}px;text-align:center;font-size:40px;font-weight:800;${glow('#C9D3E3')};white-space:nowrap">${esc(c)}</div>`).join('')}</div>` +
        (s.rows || []).map(r => `<div style="display:flex;align-items:center;height:${s.big ? 110 : 150}px">
          <div style="width:300px;text-align:left;font-size:46px;font-weight:900;${glow('#fff')};white-space:nowrap">${esc(r.k || '')}</div>
          ${(r.cells || []).map((c, j) => { const pv = K ? (((s._prev.rows || [])[0] || {}).cells || [])[j] : null, same = pv && pv.t === c.t && pv.team === c.team;
            const p = same ? 1 : AT(s, c.at, .4, seg(lt, .4 + j * .15, .4)), col = c.team ? TC_(c.team) : AMB;
            return `<div style="width:${cw}px;display:flex;justify-content:center">${c.team && LOGO[(T(c.team) || {}).code]
              ? `<div style="width:${s.big ? 96 : 128}px;height:${s.big ? 96 : 128}px;display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 0 3px #fff) drop-shadow(0 0 12px ${col});opacity:${c01(p * 1.6).toFixed(3)};transform:scale(${(.6 + .4 * eb(p)).toFixed(3)})">${LG_(c.team, s.big ? 74 : 100)}</div>`
              : `<div class="num" style="font-size:${s.big ? 64 : 84}px;font-weight:900;${glow(c.c || AMB)};opacity:${c01(p * 1.6).toFixed(3)}">${esc(c.t || '')}</div>`}</div>`; }).join('')}</div>`).join('') + `</div>`;
    }
    if (s.foot) { const p = K && s._prev.foot && s._prev.foot.t === s.foot.t ? 1 : AT(s, s.foot.at, .5, seg(lt, 1, .5));
      inner += `<div style="margin-top:18px;font-size:50px;font-weight:900;${glow('#7CF29A')};opacity:${c01(p * 1.6).toFixed(3)};white-space:nowrap">${esc(s.foot.t)}</div>`; }
    const h = `<div style="position:relative;width:${W}px;padding:28px 60px 36px;border-radius:26px;${led};border:10px solid #23272F;box-shadow:0 0 0 4px #3A3F48, 0 30px 60px rgba(10,14,24,.4);display:flex;flex-direction:column;align-items:center;opacity:${pin.toFixed(3)};transform:translateY(${((1 - pin) * 30).toFixed(1)}px)">
        ${s.title ? `<div style="align-self:stretch;display:flex;justify-content:center;border-bottom:3px solid rgba(255,176,32,.35);padding-bottom:14px;margin-bottom:10px;font-size:48px;font-weight:900;${glow(AMB)};letter-spacing:2px;white-space:nowrap">${esc(s.title)}</div>` : ''}
        ${inner}</div>`;
    B(h);
  };

  /* ── clip (신문 스크랩) ── */
  SCENE.clip = (lt, s) => {
    const cs = s.clips || [], n = cs.length, CW = n >= 2 ? 820 : 1180;
    const one = (c, i) => {
      const p = wasIn(s, 'clips', c, o => o.head + '|' + (o.quote || '')) ? 1 : AT(s, c.at, .55, seg(lt, .2 + i * .4, .55));
      const src = photoSrc(c.img), rot = c.rot != null ? c.rot : (i % 2 ? 1.6 : -1.8);
      const paper = `background:#F4EEE1;background-image:linear-gradient(rgba(60,50,30,.05) 1px, transparent 1px);background-size:100% 46px`;
      return `<div style="position:relative;width:${CW}px;flex:0 0 auto;padding:36px 44px 42px;${paper};border-radius:6px;box-shadow:0 22px 44px rgba(20,16,8,.28);text-align:left;
          opacity:${c01(p * 2).toFixed(3)};transform:translateY(${((1 - e3(p)) * -70).toFixed(1)}px) rotate(${(rot * (1 + (1 - e3(p)) * 2)).toFixed(2)}deg);clip-path:polygon(0 1%,4% 0,9% 1.2%,15% .2%,22% 1%,30% 0,38% 1.3%,47% .3%,55% 1%,64% 0,72% 1.1%,81% .2%,89% 1.2%,96% 0,100% 1%,100% 99%,95% 100%,88% 98.8%,80% 99.8%,71% 98.9%,62% 100%,53% 99%,44% 99.9%,35% 98.8%,26% 99.8%,17% 99%,9% 100%,3% 98.9%,0 99.6%)">
        <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:4px double #2A2418;padding-bottom:8px;margin-bottom:20px;font-size:34px;font-weight:800;color:#5A4E38">
          <span>${esc(c.date || '')}</span><span>${esc(c.src || '')}</span></div>
        <div style="display:flex;gap:26px;align-items:flex-start">
          ${src ? `<div style="flex:0 0 auto;width:${n >= 2 ? 250 : 340}px">
              <div style="position:relative;width:100%;height:${n >= 2 ? 320 : 430}px;overflow:hidden;border:3px solid #2A2418">${faceImg(src, c, '50% 15%').replace('object-fit:cover', 'object-fit:cover;filter:grayscale(1) contrast(1.15) sepia(.18)')}</div>
              ${c.name ? `<div style="margin-top:8px;font-size:36px;font-weight:900;color:#2A2418;text-align:center">${esc(c.name)}</div>` : ''}</div>` : ''}
          <div style="flex:1;display:flex;flex-direction:column;gap:14px;min-width:0">
            <div style="font-size:${c.hsize || (n >= 2 ? 64 : 84)}px;font-weight:900;color:#17130B;line-height:1.16;letter-spacing:-2px;word-break:keep-all">${br(c.head)}</div>
            ${c.body ? `<div style="font-size:${n >= 2 ? 38 : 46}px;font-weight:600;color:#3D3524;line-height:1.4;word-break:keep-all">${br(c.body)}</div>` : ''}
            ${c.quote ? `<div style="position:relative;margin-top:6px;padding-left:58px;font-size:${n >= 2 ? 50 : 64}px;font-weight:900;color:#8A1F11;line-height:1.3;word-break:keep-all"><span style="position:absolute;left:0;top:-18px;font-size:110px;line-height:1;color:#C8B48A">“</span>${br(c.quote)}</div>` : ''}
          </div></div></div>`; };
    B(`<div style="display:flex;gap:${n >= 2 ? 46 : 0}px;align-items:center;justify-content:center;width:1760px;height:690px">${cs.map(one).join('')}</div>`);
  };

  /* ── chalk (작전판) ── */
  SCENE.chalk = (lt, s) => {
    const L = s.lines || [], K = s._same, W = 1640, H = 690;
    const COL = { w: '#F3F4EE', y: '#FFE27A', g: '#9EF0B0', r: '#FF9C8F', b: '#9CD3FF' };
    const done = (x, i) => K && (s._prev.lines || []).some(o => o.t === x.t && (o.ind || 0) === (x.ind || 0));
    let rows = '';
    L.forEach((x, i) => {
      const p = done(x, i) ? 1 : AT(s, x.at, .7, seg(lt, .3 + i * .35, .7)), col = COL[x.c || 'w'] || x.c, fs = x.size || (x.big ? 104 : 62);
      const tilt = ((i * 37) % 7 - 3) * .25;
      rows += `<div style="position:relative;align-self:${x.center ? 'center' : 'flex-start'};margin-left:${(x.ind || 0) * 70}px;transform:rotate(${tilt}deg)">
        <div style="font-size:${fs}px;font-weight:900;color:${col};letter-spacing:${x.big ? -2 : 0}px;line-height:1.12;white-space:nowrap;
          text-shadow:0 0 1px ${col}, 1px 1px 0 rgba(255,255,255,.12), 0 0 8px rgba(255,255,255,.18);opacity:.95;
          clip-path:inset(-20px ${(100 - 100 * c01(p)).toFixed(1)}% -20px -20px)">${esc(x.t)}</div>
        ${x.rule ? `<div style="height:5px;margin-top:8px;border-radius:3px;background:${COL.w};opacity:.75;width:${(100 * c01((p - .5) * 2)).toFixed(1)}%"></div>` : ''}</div>`;
    });
    let circ = '';
    if (s.circle) { const p = K && s._prev.circle && s._prev.circle.line === s.circle.line ? 1 : AT(s, s.circle.at, .7, 0);
      circ = `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0;pointer-events:none;overflow:visible"><ellipse cx="${s.circle.x || W / 2}" cy="${s.circle.y || H - 120}" rx="${s.circle.rx || 360}" ry="${s.circle.ry || 90}" fill="none" stroke="#FFE27A" stroke-width="7" stroke-linecap="round"
        stroke-dasharray="2400" stroke-dashoffset="${(2400 * (1 - e3(p))).toFixed(0)}" transform="rotate(-3 ${s.circle.x || W / 2} ${s.circle.y || H - 120})" opacity=".9"/></svg>`; }
    let tot = '';
    if (s.total) { const pv = K && s._prev.total ? s._prev.total.v : null, same = pv === s.total.v, p = same ? 1 : AT(s, s.total.at, .7, 0);
      const big = (v, op, clip, rot) => `<div class="num" style="position:absolute;right:70px;top:${s.title ? 120 : 60}px;font-size:170px;font-weight:900;color:#FFE27A;letter-spacing:-5px;line-height:1;white-space:nowrap;opacity:${op};transform:rotate(${rot}deg);text-shadow:0 0 2px #FFE27A, 0 0 12px rgba(255,226,122,.35);clip-path:inset(-30px ${clip}% -30px -30px)">${esc(v)}</div>`;
      if (pv && !same) tot += big(pv, (1 - c01(p * 2.2)).toFixed(3), 0, -2);
      tot += big(s.total.v, (p > 0 ? .97 : 0), (100 - 100 * c01(p)).toFixed(1), -2);
      if (s.total.k) tot += `<div style="position:absolute;right:76px;top:${(s.title ? 120 : 60) + 180}px;font-size:40px;font-weight:900;color:#F3F4EE;opacity:${(.85 * c01(Math.max(p, same ? 1 : 0) * 2)).toFixed(3)};white-space:nowrap">${esc(s.total.k)}</div>`; }
    const logo = s.logo ? `<div style="position:absolute;right:46px;top:24px;width:86px;height:86px;border-radius:18px;background:#F3F4EE;display:flex;align-items:center;justify-content:center;opacity:.95">${LG_(s.logo, 70)}</div>` : '';
    const pin = K ? 1 : e3(seg(lt, 0, .4));
    B(`<div style="position:relative;width:${W}px;height:${H}px;border-radius:22px;border:22px solid #6B4A2B;box-shadow:inset 0 0 0 4px #4A321C, 0 26px 50px rgba(10,14,24,.35);
        background:radial-gradient(ellipse at 30% 20%, #2F5A45 0%, #234836 55%, #1B3A2B 100%);overflow:hidden;opacity:${pin.toFixed(3)}">
        <div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.035) 1px, transparent 1.5px);background-size:7px 7px"></div>
        ${s.title ? `<div style="position:absolute;left:46px;top:30px;font-size:46px;font-weight:900;color:#F3F4EE;opacity:.9;border-bottom:4px solid rgba(243,244,238,.6);padding-bottom:6px;white-space:nowrap">${esc(s.title)}</div>` : ''}
        <div style="position:absolute;left:70px;right:70px;top:${s.title ? 118 : 50}px;bottom:40px;display:flex;flex-direction:column;justify-content:center;gap:${s.gap || 14}px">${rows}</div>
        ${tot}${logo}
        ${circ}
        <div style="position:absolute;right:40px;bottom:18px;width:120px;height:26px;border-radius:6px;background:#E9E6DD;opacity:.85;transform:rotate(-6deg)"></div></div>`);
  };
  Object.assign(MOTION, { hero: () => 1.0, board: () => 1.0, clip: s => .7 + (s.clips || []).length * .4, chalk: s => .6 + (s.lines || []).length * .35 });
})();
/* @@STYLE1101END */
/* @@WATER1101 11/1 02:48 사용자 "텍스트만 있는 것들이 잘 읽히지 않으니 그래픽으로 설명하라"(작전판 글씨 계산 화면) →
   water: 확률 계단 막대(폭포 차트). 출발 막대 → 더하기(초록 계단 위로)·빼기(빨강 계단 아래로) → 마지막 막대. 칸 자리는 처음부터 고정(아직 안 나온 칸은 at 50).
   {title, min, max, base:{v, k, at}, steps:[{k, d, at, team}], end:{v, k, at}, team} */
(() => {
  const e3 = x => 1 - Math.pow(1 - c01(x), 3);
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  const LG_ = (n, px) => { const c_ = (T(n) || {}).code; return LOGO[c_] ? `<img src="${LOGO[c_]}" style="width:${px}px;height:${px}px;object-fit:contain;display:block">` : ''; };
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  SCENE.water = (lt, s) => {
    const K = s._same, st = s.steps || [], n = st.length + 2, W = 1640, H = 470, MIN = s.min ?? 70, MAX = s.max ?? 92;
    const y = v => H - (v - MIN) / (MAX - MIN) * H, CW = W / n, BW = Math.min(150, CW * .62), tc = TC_(s.team || 'KT');
    const prevSt = K ? (s._prev.steps || []) : [];
    const pOf = (x, i, key) => { if (K && key === 'base' && s._prev.base && s._prev.base.at != null && AT(s._prev, s._prev.base.at, .1, 1) >= 0 && (s._prev.base.at < 50)) return 1;
      return AT(s, x.at, .7, 0); };
    let svg = '', lab = '', run = s.base.v;
    const pb = K && s._prev.base && s._prev.base.at < 50 ? 1 : AT(s, s.base.at, .7, seg(lt, .2, .7));
    const col = (i, top, bot, c, p, txt, big) => { const x = CW * i + (CW - BW) / 2, h = (bot - top) * e3(p);
      svg += `<rect x="${x.toFixed(1)}" y="${(bot - h).toFixed(1)}" width="${BW.toFixed(1)}" height="${Math.max(0, h).toFixed(1)}" rx="10" fill="${c}"/>`;
      if (txt) lab += `<div class="num" style="position:absolute;left:${(CW * i).toFixed(1)}px;width:${CW.toFixed(1)}px;top:${(top - (big ? 92 : 64)).toFixed(1)}px;text-align:center;font-size:${big ? 76 : 54}px;font-weight:900;letter-spacing:-2px;color:${big ? c : (c === '#1F9D55' ? '#1F9D55' : '#E5484D')};opacity:${c01(p * 1.6).toFixed(3)};white-space:nowrap">${esc(txt)}</div>`; };
    col(0, y(s.base.v), H, '#9AA3B2', pb, s.base.v.toFixed(s.dec ?? 1) + '%', true);
    const foot = (i, k, team, p) => `<div style="position:absolute;left:${(CW * i).toFixed(1)}px;width:${CW.toFixed(1)}px;top:${H + 18}px;display:flex;flex-direction:column;align-items:center;gap:6px;opacity:${c01(p * 1.6).toFixed(3)}">
        <div style="font-size:38px;font-weight:900;color:#12161F;line-height:1.15;text-align:center;word-break:keep-all">${br(k)}</div></div>`;
    lab += foot(0, s.base.k || '출발점', s.base.team || '', pb);
    st.forEach((x, i) => {
      const was = prevSt.some(o => o.k === x.k && o.d === x.d && o.at != null && o.at < 50);
      const p = was ? 1 : AT(s, x.at, .7, 0), a = run, b = run + x.d, up = x.d > 0, c = up ? '#1F9D55' : '#E5484D';
      const top = y(Math.max(a, b)), bot = y(Math.min(a, b)), xx = CW * (i + 1) + (CW - BW) / 2;
      /* 계단 잇는 점선 */
      svg += `<line x1="${(CW * i + (CW + BW) / 2).toFixed(1)}" x2="${xx.toFixed(1)}" y1="${y(a).toFixed(1)}" y2="${y(a).toFixed(1)}" stroke="#AAB2BF" stroke-width="3" stroke-dasharray="8 7" opacity="${c01(p * 2).toFixed(3)}"/>`;
      const h = (bot - top) * e3(p), ry = up ? bot - h : top;
      svg += `<rect x="${xx.toFixed(1)}" y="${ry.toFixed(1)}" width="${BW.toFixed(1)}" height="${Math.max(0, h).toFixed(1)}" rx="8" fill="${c}"/>`;
      lab += `<div class="num" style="position:absolute;left:${(CW * (i + 1)).toFixed(1)}px;width:${CW.toFixed(1)}px;top:${(up ? top - 66 : bot + 6).toFixed(1)}px;text-align:center;font-size:54px;font-weight:900;color:${c};opacity:${c01(p * 1.6).toFixed(3)}">${up ? '+' : '−'}${Math.abs(x.d)}</div>`;
      if (x.tot) lab += `<div class="num" style="position:absolute;left:${(CW * (i + 1)).toFixed(1)}px;width:${CW.toFixed(1)}px;top:${(up ? top - 116 : bot + 58).toFixed(1)}px;text-align:center;font-size:38px;font-weight:900;color:#3B4A63;opacity:${(x.totAt != null ? (was ? 1 : c01(AT(s, x.totAt, .5, 0) * 1.6)) : c01((p - .5) * 3)).toFixed(3)}">${esc(x.tot)}</div>`;
      lab += foot(i + 1, x.k, x.team || '', x.kAt != null ? (was ? 1 : AT(s, x.kAt, .5, 0)) : p);
      run = b;
    });
    if (s.end) { const pe = K && s._prev.end && s._prev.end.at < 50 && s._prev.end.v === s.end.v ? 1 : AT(s, s.end.at, .7, 0), i = n - 1, xx = CW * i + (CW - BW) / 2;
      svg += `<line x1="${(CW * (i - 1) + (CW + BW) / 2).toFixed(1)}" x2="${xx.toFixed(1)}" y1="${y(run).toFixed(1)}" y2="${y(run).toFixed(1)}" stroke="#AAB2BF" stroke-width="3" stroke-dasharray="8 7" opacity="${c01(pe * 2).toFixed(3)}"/>`;
      col(i, y(s.end.v), H, tc, pe, s.end.v.toFixed(s.dec ?? 1) + '%', true);
      lab += foot(i, s.end.k || '결과', s.end.team || s.team || '', pe); }
    const grid = [MIN, (MIN + MAX) / 2, MAX].map(v => `<line x1="0" x2="${W}" y1="${y(v)}" y2="${y(v)}" stroke="#E3E7EE" stroke-width="2"/>`).join('');
    const ttl = s.title ? `<div class="title" style="font-size:54px;font-weight:900;margin-bottom:18px;${K && s._prev.title === s.title ? '' : pop(seg(lt, 0, .4))}">${esc(s.title)}</div>` : '';
    B(`<div class="col" style="align-items:center">${ttl}<div style="position:relative;width:${W}px;height:${H + 170}px;margin-top:80px">
        <svg width="${W}" height="${H}" style="position:absolute;left:0;top:0;overflow:visible">${grid}<line x1="0" x2="${W}" y1="${H}" y2="${H}" stroke="#12161F" stroke-width="4"/>${svg}</svg>${lab}</div></div>`);
  };
  Object.assign(MOTION, { water: s => .8 + (s.steps || []).length * .3 });
})();
/* @@WATER1101END */
