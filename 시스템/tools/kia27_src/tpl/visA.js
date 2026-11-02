/* @@VISA1101 11/1 20:17 사용자 "텍스트로 떼우는 거 없이 다 그림과 그래픽으로, 진짜 직관적으로" — 삼성이 치른 댓가·KT의 1차전 준비 장면 새 틀.
   모든 장면: 픽토그램(SVG)·단위 차트·날짜 칸·이닝 띠. 글자는 6자 안팎 이름표만, 숫자는 크게. 요소는 말하는 호흡(at)에 뜬다. */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb == null ? 0 : fb);
  const TCv = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#1B1F27' : c; };
  const LG = (n, px) => { const tt = T(n); return tt && LOGO[tt.code] ? `<img src="${LOGO[tt.code]}" style="width:${px}px;height:${px}px;object-fit:contain;display:block">` : ''; };
  const NAVY = '#0B2A5B', SOFT = '#EEF1F5', MUTE = '#9AA3B2', GOLD = '#F2B705', GOLDBG = '#FFF6DA';
  const ap = p => `opacity:${c01(p * 1.6)};transform:scale(${.7 + .3 * eo(p)})`;
  const up = (p, px = 24) => `opacity:${c01(p * 1.6)};transform:translateY(${(1 - eo(p)) * px}px)`;
  const prev = (s, key, i) => s._same ? ((s._prev[key] || [])[i]) : null;
  const shown = (pv) => !!(pv && pv.at != null && pv.at < 50);
  /* ── 아이콘 ── */
  const I = {
    pitcher: (px, c) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><circle cx="32" cy="17" r="10" fill="${c}"/><path d="M20 12 Q32 2 44 12 L46 15 L18 15Z" fill="${c}"/><rect x="40" y="13" width="12" height="3.5" rx="1.7" fill="${c}"/><path d="M14 60 Q14 32 32 32 Q50 32 50 60Z" fill="${c}"/></svg>`,
    ball: (px, c = '#fff', s = RED) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><circle cx="32" cy="32" r="28" fill="${c}" stroke="#D5DAE2" stroke-width="3"/><path d="M14 14 Q26 32 14 50" fill="none" stroke="${s}" stroke-width="3.5" stroke-dasharray="4 4"/><path d="M50 14 Q38 32 50 50" fill="none" stroke="${s}" stroke-width="3.5" stroke-dasharray="4 4"/></svg>`,
    glove: (px, c) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M14 30 L14 14 Q14 9 18.5 9 Q23 9 23 14 L23 26 L23 9 Q23 4 27.5 4 Q32 4 32 9 L32 25 L32 8 Q32 3.5 36.5 3.5 Q41 3.5 41 8 L41 26 L41 12 Q41 7.5 45.5 7.5 Q50 7.5 50 12 L50 34 Q56 28 59 31 Q61 34 56 40 Q47 58 32 59 Q16 59 14 44Z" fill="${c}"/><path d="M20 46 Q32 52 44 46" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="3" stroke-linecap="round"/></svg>`,
    x: (px) => `<svg width="${px}" height="${px}" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="${RED}" stroke="#fff" stroke-width="4"/><path d="M13 13 L27 27 M27 13 L13 27" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>`,
    zz: (px, c = MUTE) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M40 10 A24 24 0 1 0 54 44 A19 19 0 0 1 40 10Z" fill="${c}"/><text x="36" y="30" font-size="16" font-weight="900" fill="${c}" font-family="sans-serif">z</text><text x="46" y="20" font-size="12" font-weight="900" fill="${c}" font-family="sans-serif">z</text></svg>`,
    bat: (px, c) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M52 6 Q60 4 59 12 L26 47 L18 39Z" fill="${c}"/><rect x="9" y="43" width="14" height="7" rx="3" transform="rotate(-45 16 46)" fill="${c}"/><circle cx="11" cy="55" r="5" fill="${c}"/><circle cx="46" cy="50" r="8" fill="#fff" stroke="${c}" stroke-width="3"/></svg>`,
    medal: (px, c = GOLD) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M20 4 L30 26 L22 30 L12 6Z" fill="${RED}"/><path d="M44 4 L34 26 L42 30 L52 6Z" fill="#1E5EFF"/><circle cx="32" cy="42" r="19" fill="${c}" stroke="#D99A00" stroke-width="3"/><path d="M32 30 L35.5 38 L44 38.5 L37.5 44 L39.5 52.5 L32 48 L24.5 52.5 L26.5 44 L20 38.5 L28.5 38Z" fill="#fff"/></svg>`,
    shield: (px, c) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M32 4 L56 12 L56 30 Q56 50 32 60 Q8 50 8 30 L8 12Z" fill="${c}"/><path d="M21 32 L29 40 L44 24" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    crack: (px) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M32 4 L58 54 L6 54Z" fill="${RED}"/><rect x="29" y="22" width="6" height="18" rx="3" fill="#fff"/><circle cx="32" cy="46" r="3.6" fill="#fff"/></svg>`,
    star: (px, c) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M32 6 L39 24 L58 24 L43 36 L49 55 L32 44 L15 55 L21 36 L6 24 L25 24Z" fill="${c}"/></svg>`,
    q: (px) => `<div style="width:${px}px;height:${px}px;border-radius:50%;background:${RED};color:#fff;display:flex;align-items:center;justify-content:center;font-size:${Math.round(px * .7)}px;font-weight:900;border:5px solid #fff;box-shadow:0 6px 16px rgba(229,72,77,.35)">?</div>`,
    plus: (px) => `<div style="width:${px}px;height:${px}px;border-radius:50%;background:${GREEN};color:#fff;display:flex;align-items:center;justify-content:center;font-size:${Math.round(px * .7)}px;font-weight:900;border:5px solid #fff;box-shadow:0 6px 16px rgba(22,163,74,.35)">+</div>`,
  };
  const battery = (w, lvl, col, bolt) => `<div style="position:relative;width:${w}px;height:${Math.round(w * .5)}px;border:9px solid #2A3140;border-radius:22px;padding:8px;box-sizing:border-box;background:#fff">
      <div style="height:100%;width:${Math.round(lvl * 100)}%;border-radius:10px;background:${col}"></div>
      <div style="position:absolute;right:-26px;top:30%;width:16px;height:40%;border-radius:0 8px 8px 0;background:#2A3140"></div>
      ${bolt ? `<svg style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)" width="${Math.round(w * .2)}" height="${Math.round(w * .3)}" viewBox="0 0 20 30"><path d="M12 0 L0 17 L9 17 L7 30 L20 11 L11 11Z" fill="#fff" stroke="#2A3140" stroke-width="1.5"/></svg>` : ''}</div>`;
  const tag = (t, bg, fg = '#fff', fs = 36) => `<div style="height:${Math.round(fs * 1.65)}px;padding:0 ${Math.round(fs * .7)}px;border-radius:999px;background:${bg};color:${fg};font-size:${fs}px;font-weight:900;display:inline-flex;align-items:center;white-space:nowrap;letter-spacing:-.5px">${esc(t)}</div>`;
  const T0 = (lt, s) => titleH(lt, s, 60, 40, s._same && s._prev.title === s.title);
  const ZW = (lt, s, body, z) => wrapC(T0(lt, s) + `<div style="zoom:${s.z || z || 1.3}">${body}</div>`);

  /* ── vA_gap (o4): 1차전까지 쉬는 날을 칸으로 — 삼성 하루 vs KT 3주 넘게 ── */
  SCENE.vA_gap = (lt, s) => {
    const rows = s.rows || [];
    const goldSq = (px, q) => `<div style="width:${px}px;height:${px}px;border-radius:22px;background:${GOLDBG};border:7px solid ${GOLD};display:flex;flex-direction:column;align-items:center;justify-content:center;flex:0 0 auto;gap:2px;${ap(q)}">${I.ball(Math.round(px * .5))}<div style="font-size:24px;font-weight:900;color:#8A5A00">${esc(s.goal || '1차전')}</div></div>`;
    let h = `<div class="row" style="gap:90px;align-items:center;justify-content:center">`;
    rows.forEach((r, ri) => {
      const p = AT(s, r.at, .45), f = AT(s, r.fillAt != null ? r.fillAt : r.at, Math.max(.6, r.days * .05)), col = TCv(r.team);
      const SQ = 70, cols = Math.min(7, r.days);
      const sq = Array.from({ length: r.days }, (_, i) => { const q = c01((f * r.days - i) * 1.2);
        return `<div style="width:${SQ}px;height:${SQ}px;border-radius:14px;background:${SOFT};border:3px solid #D5DBE4;display:flex;align-items:center;justify-content:center;${ap(q)}">${I.zz(42)}</div>`; }).join('');
      h += `<div class="col" style="align-items:center;gap:22px;padding:36px 44px;border-radius:40px;background:#fff;box-shadow:0 16px 40px rgba(18,22,31,.08);${up(p)}">
        <div class="row" style="gap:18px;align-items:center">${LG(r.team, 110)}${tag(r.lab, col, '#fff', 46)}</div>
        <div class="row" style="gap:22px;align-items:center"><div style="display:grid;grid-template-columns:repeat(${cols},${SQ}px);gap:10px">${sq}</div>
          <svg width="46" height="40" viewBox="0 0 46 40" style="${ap(c01(f * 1.05))}"><path d="M4 20 H36 M24 6 L40 20 L24 34" fill="none" stroke="#B6BFCC" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>${goldSq(120, c01(f * 1.05))}</div></div>`;
    });
    h += `</div>`;
    h += `<div class="row" style="gap:14px;align-items:center;justify-content:center;margin-top:30px;opacity:.95;${up(AT(s, s.legendAt, .4))}"><div style="width:44px;height:44px;border-radius:10px;background:${SOFT};border:3px solid #D5DBE4;display:flex;align-items:center;justify-content:center">${I.zz(28)}</div><div style="font-size:34px;font-weight:800;color:#5B6576">${esc(s.legend || '공식 경기 없는 날')}</div></div>`;
    ZW(lt, s, h, 1.15);
  };

  /* ── vA_units (b2): 경기마다 투수 한 명 = 아이콘 하나 ── */
  SCENE.vA_units = (lt, s) => {
    const gs = s.groups || [], col = TCv(s.team || '삼성'), tot = gs.reduce((a, g) => a + g.n, 0);
    const p0 = AT(s, s.at, .45), f = AT(s, s.fillAt, 1.2), tq = AT(s, s.totAt, .45);
    let k = 0;
    let h = `<div class="row" style="gap:28px;align-items:flex-end;justify-content:center">` + gs.map((g, gi) => {
      const icons = Array.from({ length: g.n }, () => { const q = c01((f * tot - k++) * 1.3); return `<div style="width:64px;height:64px;line-height:0;${ap(q)}">${I.pitcher(64, col)}</div>`; }).join('');
      return `<div class="col" style="width:230px;align-items:center;gap:14px;${up(c01((p0 - gi * .08) * 1.5))}">
        <div style="width:230px;height:330px;border-radius:30px;background:#fff;box-shadow:0 12px 30px rgba(18,22,31,.08);display:flex;flex-wrap:wrap-reverse;align-content:flex-start;justify-content:center;gap:6px 10px;padding:22px 20px;box-sizing:border-box">${icons}</div>
        <div style="font-size:42px;font-weight:900;letter-spacing:-1px">${esc(g.g)}</div></div>`; }).join('') + `</div>`;
    h += `<div class="row" style="gap:20px;align-items:center;justify-content:center;margin-top:30px;${ap(tq)}">${I.pitcher(70, col)}<div class="num" style="font-size:110px;font-weight:900;color:${col};letter-spacing:-3px;line-height:1">${esc(s.v || '')}</div><div style="font-size:52px;font-weight:900;color:#3B4A63">${esc(s.vl || '')}</div></div>`;
    ZW(lt, s, h);
  };

  /* ── vA_errs (b6a·b6): 경기별 실책 = 공 놓친 글러브 아이콘 ── */
  SCENE.vA_errs = (lt, s) => {
    const its = s.items || [];
    let h = `<div class="row" style="gap:80px;justify-content:center;align-items:stretch">` + its.map((x, i) => {
      const pv = prev(s, 'items', i), was = shown(pv), p = was ? 1 : AT(s, x.at, .9);
      const gl = Array.from({ length: x.n }, (_, j) => { const q = was ? 1 : c01((p * x.n - j) * 1.4), sh = was ? 0 : Math.sin(c01(q) * Math.PI * 3) * (1 - c01(q)) * 14;
        return `<div style="position:relative;width:150px;height:150px"><div style="position:absolute;inset:0;opacity:${(.18 * (1 - c01(q * 2))).toFixed(2)}">${I.glove(150, '#9AA3B2')}</div><div style="position:absolute;inset:0;opacity:${c01(q * 1.6)};transform:translateX(${sh}px) scale(${.7 + .3 * eo(q)})">${I.glove(150, '#B9772F')}<div style="position:absolute;right:-6px;top:-6px">${I.x(62)}</div></div></div>`; }).join('');
      return `<div class="col" style="align-items:center;gap:22px">
        <div style="font-size:52px;font-weight:900;letter-spacing:-1px">${esc(x.g)}</div>
        <div class="row" style="gap:26px;min-width:${x.slots * 176}px;height:220px;justify-content:center;align-items:center;border-radius:36px;background:#fff;padding:20px 36px;box-shadow:0 14px 34px rgba(18,22,31,.08)">${gl}</div>
        <div class="num" style="font-size:96px;font-weight:900;color:${RED};letter-spacing:-3px;line-height:1;${ap(p)}">${esc(x.v)}</div></div>`; }).join('') + `</div>`;
    ZW(lt, s, h);
  };

  /* ── vA_battery (b7): 생각한 피로 vs 남은 힘 ── */
  SCENE.vA_battery = (lt, s) => {
    const its = s.items || [];
    let h = `<div class="row" style="gap:150px;justify-content:center;align-items:center">` + its.map((x, i) => {
      const p = AT(s, x.at, .5), lv = (x.frm != null ? x.frm + (x.lvl - x.frm) * eo(AT(s, x.at, 1.0)) : x.lvl);
      return `<div class="col" style="align-items:center;gap:30px;${up(p, 30)}">${battery(380, lv, x.c === 'good' ? GREEN : RED, x.bolt && p > .3)}
        ${tag(x.lab, x.c === 'good' ? GREEN : '#5B6576', '#fff', 44)}</div>`; }).join('') + `</div>`;
    ZW(lt, s, h);
  };

  /* ── vA_innings (b8): 5차전 마운드를 이닝 띠로 — 선발 7칸 + 불펜 2칸 ── */
  SCENE.vA_innings = (lt, s) => {
    const segs = s.segs || [], CW = 150, G = 10, team = s.team || '삼성', col = TCv(team);
    let h = '';
    h += `<div class="row" style="gap:${G}px">` + Array.from({ length: 9 }, (_, i) => `<div class="num" style="width:${CW}px;text-align:center;font-size:40px;font-weight:900;color:#7A8597">${i + 1}회</div>`).join('') + `</div>`;
    let cells = '', brk = '';
    segs.forEach(g => { const p = AT(s, g.at, .9);
      for (let i = g.frm; i <= g.to; i++) { const q = c01((p * (g.to - g.frm + 1) - (i - g.frm)) * 1.5);
        cells += `<div style="width:${CW}px;height:150px;border-radius:24px;background:${g.c || col};display:flex;align-items:center;justify-content:center;${ap(q)}">${I.pitcher(100, '#fff')}</div>`; }
      const w = (g.to - g.frm + 1) * CW + (g.to - g.frm) * G;
      brk += `<div class="col" style="width:${w}px;align-items:center;gap:10px;${up(c01(p * 1.2 - .2))}"><div style="width:${w - 20}px;height:20px;border:6px solid ${g.c || col};border-top:0;border-radius:0 0 16px 16px"></div>${tag(g.lab, g.c || col, '#fff', 40)}</div>`;
    });
    h += `<div class="row" style="gap:${G}px;margin-top:12px">${cells}</div><div class="row" style="gap:${G}px;margin-top:14px;align-items:flex-start">${brk}</div>`;
    if (s.v) h += `<div class="row" style="gap:18px;align-items:center;justify-content:center;margin-top:38px;${ap(AT(s, s.vAt, .45))}">${Array.from({ length: s.vn || 0 }, () => I.pitcher(84, s.vc || '#0E9384')).join('')}<div style="font-size:64px;font-weight:900;color:${s.vc || '#0E9384'}">${esc(s.v)}</div></div>`;
    ZW(lt, s, h);
  };

  /* ── vA_days (b9·b9b): 날짜 칸 — 등판·휴식·경기 ── */
  SCENE.vA_days = (lt, s) => {
    const ds = s.days || [], CW = s.cw || 210, CH = s.ch || 230;
    let h = `<div class="row" style="gap:16px;align-items:flex-end;justify-content:center">`;
    ds.forEach((d, i) => {
      const pv = prev(s, 'days', i), was = shown(pv), p = was ? 1 : AT(s, d.at, .45);
      const st = d.k === 'p' ? `background:${TCv(s.team || '삼성')};color:#fff` : d.k === 'g' ? `background:${GOLDBG};border:7px solid ${GOLD};color:#8A5A00` : d.k === 'bad' ? `background:#FDECEC;border:7px solid ${RED};color:${RED}` : `background:${SOFT};color:#7A8597`;
      const ic = d.k === 'p' ? I.pitcher(96, '#fff') : d.k === 'g' || d.k === 'bad' ? I.ball(96) : I.zz(92);
      const ex = d.ic === 'tired' ? `<div class="row" style="gap:4px;position:absolute;bottom:18px;left:0;right:0;justify-content:center"><div class="row" style="gap:4px;${ap(AT(s, d.icAt, .45))}">${[0, 1, 2].map(() => I.pitcher(70, RED)).join('')}</div></div>`
        : d.ic === 'pen' ? `<div class="row" style="gap:4px;position:absolute;bottom:18px;left:0;right:0;justify-content:center"><div class="row" style="gap:4px;${ap(AT(s, d.icAt, .45))}">${[0, 1, 2].map(() => I.pitcher(70, TCv(s.team || '삼성'))).join('')}</div></div>` : '';
      h += `<div class="col" style="align-items:center;gap:14px;${up(p)}">
        <div class="num" style="font-size:34px;font-weight:800;color:#7A8597">${esc(d.date || '')}</div>
        <div style="position:relative;width:${CW}px;height:${CH}px;border-radius:30px;box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:${ex ? 'flex-start' : 'center'};padding-top:${ex ? 22 : 0}px;gap:6px;${st}">${ic}<div style="font-size:${d.k === 'r' ? 34 : 40}px;font-weight:900;white-space:nowrap">${esc(d.lab || '')}</div>${ex}</div></div>`;
      if (d.arrow) h += `<div style="align-self:center;margin-top:48px;${ap(AT(s, d.arrowAt, .45))}"><svg width="90" height="60" viewBox="0 0 90 60"><path d="M4 30 H70 M52 10 L74 30 L52 50" fill="none" stroke="${d.arrowC || RED}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg></div>`;
    });
    h += `</div>`;
    (s.brackets || []).forEach(b => { const q = AT(s, b.at, .45);
      h += `<div class="row" style="justify-content:center;margin-top:20px;${up(q)}"><div class="col" style="align-items:center;gap:12px;margin-left:${b.ml || 0}px"><div style="width:${b.w}px;height:22px;border:7px solid ${b.c || GREEN};border-top:0;border-radius:0 0 18px 18px"></div>${tag(b.lab, b.c || GREEN, '#fff', 42)}</div></div>`; });
    ZW(lt, s, h);
  };

  /* ── vA_tiles (b17): 정리 — 아이콘 칸 + 물음표/플러스 배지 ── */
  SCENE.vA_tiles = (lt, s) => {
    const its = s.items || [];
    let h = `<div class="row" style="gap:40px;justify-content:center">` + its.map((x, i) => {
      const p = AT(s, x.at, .45), good = x.c === 'good', col = good ? GREEN : RED;
      const ic = x.ic === 'glove' ? I.glove(150, '#B9772F') : x.ic === 'bat' ? I.bat(150, '#3B4A63') : x.ic === 'pen' ? `<div class="row" style="gap:2px">${I.pitcher(78, TCv('삼성'))}${I.pitcher(78, TCv('삼성'))}</div>` : I.pitcher(150, TCv('삼성'));
      return `<div class="col" style="align-items:center;gap:20px;${up(p, 30)}"><div style="position:relative;width:300px;height:280px;border-radius:36px;background:${good ? '#EAF7EF' : '#FDECEC'};border:7px solid ${col};display:flex;align-items:center;justify-content:center">${ic}
        <div style="position:absolute;right:-22px;top:-22px;${ap(p)}">${good ? I.plus(84) : I.q(84)}</div></div>
        <div style="font-size:54px;font-weight:900;letter-spacing:-1px">${esc(x.lab)}</div></div>`; }).join('') + `</div>`;
    ZW(lt, s, h);
  };

  /* ── vA_games (k3): 연습경기 점수판 카드 ── */
  SCENE.vA_games = (lt, s) => {
    const gs = s.games || [];
    /* 11/1 21:54 사용자 "u23 마크 저거 맞아?" — 실제 엠블럼이 아닌 그림(별·태극)을 상대 표시로 쓰지 않는다 → 중립 야구공 표시 */
    const badge = (b) => `<div style="width:130px;height:130px;border-radius:30px;background:#EEF1F5;display:flex;align-items:center;justify-content:center"><svg width="84" height="84" viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill="#fff" stroke="#B8C1CE" stroke-width="2.5"/><path d="M11 7c5 6 5 20 0 26M29 7c-5 6-5 20 0 26" fill="none" stroke="#9AA3B2" stroke-width="2.4" stroke-dasharray="3 2.6"/></svg></div>`;
    let h = `<div class="row" style="gap:70px;justify-content:center">` + gs.map((g, i) => {
      const p = AT(s, g.at, .45), q = AT(s, g.scAt, .45);
      return `<div class="col" style="align-items:center;gap:20px;${up(p, 30)}">
        <div class="num" style="font-size:38px;font-weight:800;color:#7A8597">${esc(g.date || '')}</div>
        <div class="row" style="position:relative;gap:34px;align-items:center;padding:40px 54px;border-radius:40px;background:#fff;box-shadow:0 16px 40px rgba(18,22,31,.10)">
          <div class="col" style="align-items:center;gap:10px">${LG('KT', 130)}<div style="font-size:36px;font-weight:900;visibility:hidden">KT</div></div>
          <div class="num" style="font-size:130px;font-weight:900;letter-spacing:-4px;line-height:1;${ap(q)}"><span style="color:${GREEN}">${esc(g.a)}</span><span style="color:#B6BFCC;margin:0 18px">:</span><span style="color:#5B6576">${esc(g.b)}</span></div>
          <div class="col" style="align-items:center;gap:10px">${badge(g.badge)}<div style="font-size:36px;font-weight:900;white-space:nowrap">${esc(g.opp)}</div></div>
          <div style="position:absolute;top:-30px;right:-24px;${ap(q)}">${tag('승', GREEN, '#fff', 44)}</div></div></div>`; }).join('') + `</div>`;
    ZW(lt, s, h);
  };

  /* ── vA_rank (k7): 리그 1위 두 개 — 메달 + 종목 아이콘 ── */
  SCENE.vA_rank = (lt, s) => {
    const its = s.items || [];
    let h = `<div class="row" style="gap:60px;justify-content:center;align-items:center">`;
    h += `<div style="${ap(AT(s, s.logoAt, .45))}">${LG('KT', 230)}</div>`;
    h += its.map((x, i) => { const p = AT(s, x.at, .45);
      return `<div class="col" style="align-items:center;gap:18px;padding:36px 46px;border-radius:40px;background:#fff;box-shadow:0 16px 40px rgba(18,22,31,.10);${up(p, 30)}">
        <div class="row" style="gap:16px;align-items:center">${x.ic === 'bat' ? I.bat(110, '#3B4A63') : I.ball(110)}${I.medal(130)}</div>
        <div style="font-size:52px;font-weight:900;letter-spacing:-1px">${esc(x.lab)}</div>
        ${x.v ? tag(x.v, GOLD, '#4A3300', 48) : ''}</div>`; }).join('');
    h += `</div>`;
    ZW(lt, s, h);
  };

  /* ── vA_relay (k9): 선발 → 중간 → 마무리 이어달리기, 약한 고리 ── */
  SCENE.vA_relay = (lt, s) => {
    const ns = s.nodes || [];
    let h = `<div class="row" style="gap:0;align-items:center;justify-content:center">`;
    ns.forEach((n, i) => { const p = AT(s, n.at, .45), bad = n.c === 'bad', good = n.c === 'good', w = AT(s, n.warnAt, .45);
      const bc = bad ? RED : good ? GREEN : '#3B4A63';
      if (i) h += `<div style="width:110px;height:16px;background:${bad || ns[i - 1].c === 'bad' ? `repeating-linear-gradient(90deg,${RED} 0 16px,transparent 16px 28px)` : '#C8CFDA'};border-radius:8px;opacity:${c01(p * 1.6)}"></div>`;
      h += `<div class="col" style="align-items:center;gap:18px;${up(p, 30)}"><div style="position:relative;width:260px;height:260px;border-radius:50%;background:#fff;border:12px solid ${bc};display:flex;align-items:center;justify-content:center;box-shadow:0 14px 34px rgba(18,22,31,.10)">${I.pitcher(150, bc)}
        ${bad ? `<div style="position:absolute;right:-20px;top:-20px;${ap(w)}">${I.crack(96)}</div>` : good ? `<div style="position:absolute;right:-16px;top:-16px;${ap(w)}">${I.shield(90, GREEN)}</div>` : ''}</div>
        <div style="font-size:50px;font-weight:900;letter-spacing:-1px;color:${bad ? RED : TXT}">${esc(n.lab)}</div>${n.sub ? `<div style="font-size:34px;font-weight:800;color:#7A8597">${esc(n.sub)}</div>` : ''}</div>`; });
    h += `</div>`;
    ZW(lt, s, h);
  };

  /* ── vA_saves (k10): 세이브 30개 = 공 30개, 평균자책점 방패 ── */
  SCENE.vA_saves = (lt, s) => {
    const n = s.n || 30, f = AT(s, s.at, 1.0), q = AT(s, s.eraAt, .45), col = TCv('KT');
    const balls = Array.from({ length: n }, (_, i) => { const r = c01((f * n - i) * 1.2); return `<div style="${ap(r)}">${I.ball(64)}</div>`; }).join('');
    let h = `<div class="row" style="gap:80px;align-items:center;justify-content:center">
      <div class="col" style="align-items:center;gap:20px"><div style="display:grid;grid-template-columns:repeat(10,64px);gap:12px;padding:30px;border-radius:36px;background:#fff;box-shadow:0 14px 34px rgba(18,22,31,.08)">${balls}</div>
        <div class="row" style="gap:16px;align-items:baseline;${ap(c01(f * 1.2 - .2))}"><div class="num" style="font-size:100px;font-weight:900;color:${col};letter-spacing:-3px;line-height:1">${esc(s.v)}</div><div style="font-size:50px;font-weight:900;color:#3B4A63">${esc(s.vl)}</div></div></div>
      <div class="col" style="align-items:center;gap:16px;${ap(q)}"><div style="position:relative">${I.shield(300, GREEN)}</div>
        <div style="font-size:40px;font-weight:800;color:#5B6576">${esc(s.eraLab)}</div><div class="num" style="font-size:96px;font-weight:900;color:${GREEN};letter-spacing:-3px;line-height:1">${esc(s.era)}</div></div></div>`;
    ZW(lt, s, h);
  };

  /* ── vA_streak (k2c): 마지막 10경기 = 승 10개 칸 + 연승 불꽃 ── */
  SCENE.vA_streak = (lt, s) => {
    const n = s.n || 10, f = AT(s, s.at, 1.0), q = AT(s, s.tagAt, .45);
    let h = `<div class="row" style="gap:18px;align-items:center;justify-content:center">${LG('KT', 160)}<div style="width:20px"></div>` +
      Array.from({ length: n }, (_, i) => { const r = c01((f * n - i) * 1.3); return `<div style="width:118px;height:150px;border-radius:26px;background:${GREEN};color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;box-shadow:0 10px 24px rgba(22,163,74,.25);${ap(r)}">${I.ball(56)}<div style="font-size:48px;font-weight:900">승</div></div>`; }).join('') + `</div>`;
    h += `<div class="row" style="justify-content:center;margin-top:46px;${ap(q)}">${tag(s.lab || '', '#1B1F27', '#fff', 52)}</div>`;
    ZW(lt, s, h);
  };

  Object.assign(MOTION, { vA_gap: s => .8, vA_units: s => .8, vA_errs: s => .8, vA_battery: s => .8, vA_innings: s => .8, vA_days: s => .8, vA_tiles: s => .8, vA_games: s => .8, vA_rank: s => .8, vA_relay: s => .8, vA_saves: s => .8, vA_streak: s => .8 });
})();
/* @@VISA1101END */
