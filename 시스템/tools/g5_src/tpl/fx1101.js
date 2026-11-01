/* @@FX1101 11/1 롱폼㊱ — 움직임 사전 #16 흔들림(부정 수치 1회). errs: 실책·부정 기록 카드가 뜬 직후 한 번만 좌우로 흔들린다.
   errs: {title, items:[{k, v, at}], text, textAt}  — 화면 전체가 아니라 카드만 흔들림(사전 금지 규칙). */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  SCENE.errs = (lt, s) => {
    const K = s._same, its = s.items || [];
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    h += `<div class="row" style="gap:60px;justify-content:center">` + its.map((x, i) => {
      const pv = K ? (s._prev.items || [])[i] : null, was = !!(pv && pv.at != null && pv.at < 50);   /* 이어지는 장면: 앞에서 이미 보인 카드만 그대로 */
      const p = was ? 1 : AT(s, x.at, .4, 0), sh = (was || x.shake === false) ? 1 : AT(s, (x.at != null && x.at >= 0 ? x.at : 0) + .35, .7, 0);
      return `<div style="width:640px;height:330px;border-radius:36px;background:#fff;border:8px solid ${RED};box-shadow:0 14px 36px rgba(229,72,77,.18);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;${rise(p, 40)}">
        <div style="${MK.css.shake(sh, 14)}" class="col">
        <div style="font-size:54px;font-weight:900;color:#3B4A63;letter-spacing:-1.5px;white-space:nowrap;text-align:center">${esc(x.k)}</div>
        <div class="num" style="font-size:150px;font-weight:900;color:${RED};letter-spacing:-5px;line-height:1.05;text-align:center">${esc(x.v)}</div></div></div>`; }).join('') + `</div>`;
    h += textH(lt, s, .8, 64);
    wrapC(h);
  };
  Object.assign(MOTION, { errs: s => .8 });
})();
/* @@FX1101END */
/* @@REST1101 11/1 20:13 사용자 "텍스트로만 떼운 장면 — 그림으로 한눈에". rest: 선발 후보별 날짜 달력(등판일·쉬는 날·1차전).
   rest: {title, days:['10/26',...], rows:[{img, name, team, at, cells:{'10/29':{k:'p', t:'3차전'}, ...}, chip, chipAt}]}
   k: p=등판(구단 색) · r=휴식(회색) · g=1차전(금색 테두리). 칸은 날짜축에 맞춰 줄을 세운다. */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  SCENE.rest = (lt, s) => {
    const K = s._same, days = s.days || [], rows = s.items || s.rows || [], n = days.length;
    const PW = 210, PH = 250, GAP = 10, CW = Math.min(150, Math.floor((1600 - PW - 60 - GAP * (n - 1)) / n)), CH = 128;
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    h += `<div class="col" style="gap:34px;align-items:flex-start">`;
    h += `<div class="row" style="gap:${GAP}px;margin-left:${PW + 60}px">` + days.map(d => `<div class="num" style="width:${CW}px;text-align:center;font-size:34px;font-weight:800;color:#7A8597">${esc(d)}</div>`).join('') + `</div>`;
    rows.forEach((r, ri) => {
      const pv = K ? (s._prev.items || s._prev.rows || [])[ri] : null, was = !!(pv && pv.at != null && pv.at < 50);
      const p = was ? 1 : AT(s, r.at, .45, 0), col = TC_(r.team), src = photoSrc(r.img);
      const cells = days.map((d, di) => {
        const c = (r.cells || {})[d]; if (!c) return `<div style="width:${CW}px;height:${CH}px"></div>`;
        const q = was ? 1 : c01((p - .15 - di * .06) * 2.2);
        const st = c.k === 'p' ? `background:${col};color:#fff;border:0` : c.k === 'g' ? `background:#FFF6DA;color:#8A5A00;border:6px solid #F2B705` : `background:#EEF1F5;color:#8D97A6;border:0`;
        return `<div class="col" style="width:${CW}px;height:${CH}px;border-radius:22px;${st};align-items:center;justify-content:center;gap:4px;box-shadow:0 8px 20px rgba(18,22,31,.06);opacity:${c01(q * 1.5)};transform:scale(${.85 + .15 * eo(q)})">
          ${c.k === 'r' ? `<svg width="54" height="54" viewBox="0 0 40 40"><path d="M26 6a14 14 0 1 0 8 24A12 12 0 0 1 26 6z" fill="#B8C1CE"/></svg>` : c.k === 'g' && !c.t ? `<svg width="66" height="66" viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill="#fff" stroke="#E2B100" stroke-width="2.5"/><path d="M11 7c5 6 5 20 0 26M29 7c-5 6-5 20 0 26" fill="none" stroke="#E5484D" stroke-width="2.4" stroke-dasharray="3 2.6"/></svg>` : `<div style="font-size:40px;font-weight:900;letter-spacing:-1px;white-space:nowrap">${esc(c.t || '')}</div>`}${c.sub ? `<div style="font-size:26px;font-weight:800;opacity:.9;white-space:nowrap">${esc(c.sub)}</div>` : ''}</div>`;
      }).join('');
      const cq = r.chip ? (was && pv.chip === r.chip && pv.chipAt != null && pv.chipAt < 50 ? 1 : AT(s, r.chipAt, .4, 0)) : 0;
      h += `<div class="row" style="gap:60px;align-items:center;${rise(p, 30)}">
        <div class="col" style="width:${PW}px;gap:10px;align-items:center">
          <div style="width:${PW}px;height:${PH - 60}px;border-radius:24px;overflow:hidden;position:relative;background:#E9EDF3">${src ? `<div class="pp" style="position:absolute;inset:0">${photoImg(r, src, PW, PH - 60, r.focus || '50% 14%')}</div>` : ''}</div>
          <div style="font-size:46px;font-weight:900;letter-spacing:-1px">${esc(r.name)}</div></div>
        <div class="col" style="gap:16px;align-items:flex-start"><div class="row" style="gap:${GAP}px">${cells}</div>
          ${r.chip ? `<div style="height:64px;padding:0 28px;border-radius:999px;background:${r.chipBad ? RED : '#12161F'};color:#fff;font-size:38px;font-weight:900;display:flex;align-items:center;white-space:nowrap;opacity:${c01(cq * 1.6)};transform:translateY(${(1 - eo(cq)) * 14}px)">${esc(r.chip)}</div>` : `<div style="height:64px"></div>`}</div></div>`;
    });
    h += `</div>` + textH(lt, s, .8, 64);
    wrapC(h);
  };
  Object.assign(MOTION, { rest: s => .8 });
})();
/* @@REST1101END */
/* @@GRID1101 11/1 20:14 사용자 "눈에 안 들어오게 만드는 것도 능력" (막대 3/4팀·4/4팀 + 연도 글자줄). grid: 팀(로고+연도) 열 × 결과 줄.
   grid: {title, cols:[{team, label}], colAt, rows:[{k, at, vals:[{t, c:'bad'|'good'|'', icon:'trophy'|''}]}], text, textAt}
   한 칸 = 한 팀의 결과 — 몇 팀 중 몇 팀을 막대로 말하지 않고 팀마다 바로 보이게. */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  const TROPHY = (px, c) => `<svg width="${px}" height="${px}" viewBox="0 0 64 64"><path d="M18 8h28v10c0 10-6 18-14 18S18 28 18 18z" fill="${c}"/><path d="M18 12H8c0 10 5 15 12 15M46 12h10c0 10-5 15-12 15" fill="none" stroke="${c}" stroke-width="5"/><rect x="28" y="36" width="8" height="10" fill="${c}"/><rect x="18" y="46" width="28" height="8" rx="3" fill="${c}"/></svg>`;
  SCENE.grid = (lt, s) => {
    const K = s._same, cols = s.cols || [], rows = s.rows || [], n = cols.length;
    const CW = Math.min(300, Math.floor(1300 / n)), LW = 230, RH = 150;
    const cp = K ? 1 : AT(s, s.colAt, .45, seg(lt, .1, .45));
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    h += `<div class="col" style="gap:18px;align-items:flex-start">`;
    h += `<div class="row" style="gap:0;margin-left:${LW}px">` + cols.map((c, i) => `<div class="col" style="width:${CW}px;align-items:center;gap:8px;${rise(c01((cp - i * .08) * 1.6), 26)}">
        ${(() => { const tt = T(c.team); return tt && LOGO[tt.code] ? `<img src="${LOGO[tt.code]}" style="width:120px;height:120px;object-fit:contain">` : ''; })()}<div class="num" style="font-size:40px;font-weight:900;letter-spacing:-1px;white-space:nowrap">${esc(c.label || '')}</div></div>`).join('') + `</div>`;
    rows.forEach((r, ri) => {
      const pv = K ? (s._prev.rows || [])[ri] : null, was = !!(pv && pv.at != null && pv.at < 50);
      const p = was ? 1 : AT(s, r.at, .5, 0);
      h += `<div class="row" style="gap:0;align-items:center;height:${RH}px;opacity:${c01(p * 3)}">
        <div style="width:${LW}px;font-size:48px;font-weight:900;letter-spacing:-1px;white-space:nowrap">${esc(r.k)}</div>` +
        (r.vals || []).map((v, i) => { const q = was ? 1 : c01((p - i * .1) * 1.8);
          const bg = v.c === 'bad' ? RED : v.c === 'good' ? GREEN : '#EEF1F5', fg = v.c ? '#fff' : '#8D97A6';
          return `<div style="width:${CW}px;display:flex;justify-content:center"><div class="row" style="width:${CW - 50}px;height:${RH - 24}px;border-radius:28px;background:${bg};color:${fg};justify-content:center;align-items:center;gap:10px;font-size:54px;font-weight:900;opacity:${c01(q * 1.5)};transform:scale(${.8 + .2 * eo(q)});box-shadow:0 10px 26px rgba(18,22,31,.10)">${v.icon === 'trophy' ? TROPHY(58, fg) : ''}${esc(v.t || '')}</div></div>`; }).join('') + `</div>`;
    });
    h += `</div>` + textH(lt, s, .8, 64);
    wrapC(h);
  };
  Object.assign(MOTION, { grid: s => .8 });
})();
/* @@GRID1101END */


