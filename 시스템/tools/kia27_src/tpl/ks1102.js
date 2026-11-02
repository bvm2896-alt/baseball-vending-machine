/* @@KS1102 11/2 롱폼㉟ 「한국시리즈 KT 우승 예측」 새 그림 장면
   ks_sched(한국시리즈 일정 + 삼성 선발 휴식) · ks_prob7(7경기 확률 막대가 변수마다 오르내림) · ks_outs(시리즈 결과 8가지 막대) */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  const LG = (n, px) => { const tt = T(n); return tt && LOGO[tt.code] ? `<img src="${LOGO[tt.code]}" style="width:${px}px;height:${px}px;object-fit:contain;flex:0 0 auto">` : ''; };
  const card = (inner, extra = '') => `<div style="background:#fff;border-radius:26px;box-shadow:0 14px 36px rgba(18,22,31,.08);border:2px solid #EDF0F5;${extra}">${inner}</div>`;
  const POPQ = q => `opacity:${c01(q * 1.6)};transform:scale(${.7 + .3 * eo(q)})`;
  const MOON = (px, c = '#9AA3B2') => `<svg width="${px}" height="${px}" viewBox="0 0 40 40"><path d="M26 6a15 15 0 1 0 8 25A13 13 0 0 1 26 6z" fill="${c}"/></svg>`;
  const BALL = px => `<svg width="${px}" height="${px}" viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill="#fff" stroke="#D9DEE6" stroke-width="2.5"/><path d="M11 7c5 6 5 20 0 26M29 7c-5 6-5 20 0 26" fill="none" stroke="#E5484D" stroke-width="2.4" stroke-dasharray="3 2.6"/></svg>`;
  const prevArr = (s, key, i) => (s._same && s._prev && (s._prev[key] || [])[i]) || null;
  const wasOn = (s, key, i, f = 'at') => { const p = prevArr(s, key, i); return !!(p && p[f] != null && p[f] < 50); };

  /* 일정: days=[{d:'11/3', g:1, venue:'KT'|'삼성'} | {d:'11/5', off:true}], sp=[{g, name, rest, bad, at}], spAt, brackets=[{from,to,lab,at,c}] */
  SCENE.ks_sched = (lt, s) => {
    const K = s._same, D = s.days || [], W = 168, GAP = 12;
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    const dq = K ? 1 : AT(s, s.dayAt, .5, seg(lt, .05, .45));
    const cells = D.map((d, i) => {
      const q = c01(dq * 2 - i * .08), col = d.venue ? TC_(d.venue) : '#C9D0DA';
      const body = d.off ? `<div class="col" style="align-items:center;gap:6px">${MOON(54)}<div style="font-size:26px;font-weight:800;color:#9AA3B2">쉬는 날</div></div>`
        : `<div class="col" style="align-items:center;gap:8px">${BALL(46)}<div style="font-size:36px;font-weight:900">${d.g}차전</div><div style="padding:3px 16px;border-radius:12px;background:${col};color:#fff;font-size:26px;font-weight:900">${esc(d.place || '')}</div></div>`;
      return `<div class="col" style="align-items:center;gap:10px;width:${W}px;opacity:${q.toFixed(3)}"><div class="num" style="font-size:34px;font-weight:800;color:#6A7382">${esc(d.d)}</div>
        ${card(`<div class="col" style="height:220px;align-items:center;justify-content:center">${body}</div>`, `width:${W}px;${d.off ? 'background:#F4F6F9;' : ''}`)}</div>`; }).join('');
    const spBy = {}; (s.sp || []).forEach((x, i) => spBy[x.g] = Object.assign({ i }, x));
    const sps = D.map((d, i) => { const x = d.off ? null : spBy[d.g];
      if (!x) return `<div style="width:${W}px"></div>`;
      const q = wasOn(s, 'sp', x.i) ? 1 : AT(s, x.at, .45, 0), c = x.bad ? RED : '#3B4A63';
      return `<div class="col" style="width:${W}px;align-items:center;gap:8px;${POPQ(q)}"><div style="font-size:40px;font-weight:900;white-space:nowrap">${esc(x.name)}</div>
        ${x.rest ? `<div style="width:110px;height:12px;border-radius:6px;background:${x.bad ? RED : '#16A34A'}"></div>` : '<div style="height:12px"></div>'}</div>`; }).join('');
    const brk = (s.brackets || []).map((b, i) => { const q = wasOn(s, 'brackets', i) ? 1 : AT(s, b.at, .45, 0); const x0 = b.from * (W + GAP), w = (b.to - b.from + 1) * (W + GAP) - GAP, c = b.c || RED;
      return `<div style="position:absolute;left:${x0}px;top:0;width:${w}px;opacity:${c01(q * 2).toFixed(3)}"><div style="height:18px;border:5px solid ${c};border-top:0;border-radius:0 0 14px 14px"></div>
        <div style="text-align:center;margin-top:8px"><span style="padding:4px 18px;border-radius:14px;background:${c};color:#fff;font-size:28px;font-weight:900;white-space:nowrap">${esc(b.lab)}</span></div></div>`; }).join('');
    const spLab = s.sp && s.sp.length ? `<div class="row" style="gap:10px;align-items:center;width:150px;justify-content:flex-end;opacity:${c01(AT(s, s.spAt, .45, 0) * 2)}">${LG(s.spTeam || '삼성', 54)}<div style="font-size:28px;font-weight:900;color:#3B4A63">선발</div></div>` : '';
    h += `<div class="col" style="gap:22px;align-items:flex-start">
      <div class="row" style="gap:${GAP}px;margin-left:${s.sp ? 160 : 0}px">${cells}</div>
      <div style="position:relative;margin-left:${s.sp ? 160 : 0}px;height:70px;width:${D.length * (W + GAP)}px">${brk}</div>
      ${s.sp ? `<div class="row" style="gap:${GAP}px;align-items:flex-start">${spLab}<div style="width:0"></div>${sps}</div>` : ''}</div>`;
    wrapC(`<div class="col" style="zoom:${s.z || 1.0};width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 7경기 확률 막대: games=[{g, place, venue}], base, steps=[{lab, d:[7개], at}], valAt, hi=[{g, at, c}], baseLabAt */
  SCENE.ks_prob7 = (lt, s) => {
    const K = s._same, G = s.games || [], st = s.steps || [], H = 400, MX = 70, BW = 124;
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    const vals = G.map((g, i) => { let v = s.base; st.forEach((x, j) => { const q = wasOn(s, 'steps', j) ? 1 : AT(s, x.at, .7, 0); v += (x.d[i] || 0) * eo(q); }); return v; });
    const vq = Array.isArray(s.valAt) ? 0 : AT(s, s.valAt, .45, 0), vqi = i => Array.isArray(s.valAt) ? AT(s, s.valAt[i], .45, 0) : vq, bq = AT(s, s.baseLabAt, .45, 0);
    const y50 = H - H * 50 / MX;
    const cols = G.map((g, i) => { const v = vals[i], bh = Math.round(H * v / MX), hiX = (s.hi || []).find(x => x.g === g.g), hq = hiX ? AT(s, hiX.at, .45, 0) : 0;
      const col = v >= 50 ? '#12161F' : '#9AA3B2', ring = hq > 0 ? `box-shadow:0 0 0 ${Math.round(6 * hq)}px ${hiX.c || GOLD};` : '';
      const fin = (s.final || [])[i];
      return `<div class="col" style="align-items:center;gap:10px;width:${BW + 40}px">
        <div style="position:relative;width:${BW}px;height:${H}px">
          <div style="position:absolute;left:0;right:0;bottom:0;height:${bh}px;border-radius:16px 16px 6px 6px;background:${col};${ring}transition:none"></div>
          <div class="num" style="position:absolute;left:-20px;right:-20px;bottom:${bh + 10}px;text-align:center;font-size:36px;font-weight:900;color:${v >= 50 ? TXT : '#6A7382'};opacity:${c01(vqi(i) * 2).toFixed(3)}">${fin != null ? esc(fin) : ''}</div></div>
        <div style="font-size:34px;font-weight:900">${g.g}차전</div>
        <div style="padding:3px 16px;border-radius:12px;background:${TC_(g.venue)};color:#fff;font-size:26px;font-weight:900">${esc(g.place)}</div></div>`; }).join('');
    const chips = st.map((x, j) => { const q = wasOn(s, 'steps', j) ? 1 : AT(s, x.at, .45, 0); const c = x.neg ? RED : '#16A34A';
      return `<div style="padding:6px 18px;border-radius:14px;background:#fff;border:3px solid ${x.mix ? '#3B4A63' : c};color:${x.mix ? '#3B4A63' : c};font-size:30px;font-weight:900;white-space:nowrap;${POPQ(q)}">${esc(x.lab)}</div>`; }).join('');
    const legend = `<div class="row" style="gap:14px;align-items:center;justify-content:center;min-height:56px;flex-wrap:nowrap">${chips}</div>`;
    const axis = `<div style="position:absolute;left:-90px;right:-20px;top:${y50}px;border-top:4px dashed #C3CAD5"></div><div style="position:absolute;left:-150px;top:${y50 - 22}px;font-size:28px;font-weight:900;color:#8A93A3">50%</div>
      <div class="num" style="position:absolute;left:-190px;top:${H - H * s.base / MX - 22}px;font-size:30px;font-weight:900;color:#6A7382;opacity:${c01(bq * 2).toFixed(3)}">${esc(String(s.base))}%</div>`;
    h += legend + `<div style="position:relative;margin-top:16px;margin-left:150px">${axis}<div class="row" style="gap:6px;align-items:flex-end">${cols}</div></div>`;
    wrapC(`<div class="col" style="zoom:${s.z || 1.12};width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 시리즈 결과: rows=[{team, outs:[{k:'4승 0패', v}]}], his=[{team, i, lab, at}], bracket={lab, at} (두 팀의 4승 3패 칸 묶음) */
  SCENE.ks_outs = (lt, s) => {
    const K = s._same, R = s.rows || [], MX = s.max || 20, BH = 150;
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    const rq = K ? 1 : AT(s, s.at, .5, seg(lt, .05, .45));
    const row = (r, ri) => `<div class="row" style="gap:22px;align-items:flex-end"><div class="col" style="width:140px;align-items:center;gap:6px">${LG(r.team, 96)}</div>` + r.outs.map((o, i) => {
      const hi = (s.his || []).find(x => x.team === r.team && x.i === i), hq = hi ? (wasOn(s, 'his', (s.his || []).indexOf(hi)) ? 1 : AT(s, hi.at, .45, 0)) : 0;
      const bh = Math.round(BH * o.v / MX * eo(rq)), c = hq > 0 ? (hi.c || '#E8A100') : TC_(r.team);
      const bq7 = s.bracket && i === 3 ? AT(s, s.bracket.at, .45, 0) : 0, ol = bq7 > 0 ? `outline:${Math.round(6 * bq7)}px solid ${RED};outline-offset:6px;` : '';
      return `<div class="col" style="align-items:center;gap:8px;width:170px">
        <div style="height:56px;display:flex;align-items:flex-end">${hi && hi.lab ? `<span style="padding:4px 14px;border-radius:12px;background:${hi.c || GOLD};color:#fff;font-size:28px;font-weight:900;white-space:nowrap;${POPQ(hq)}">${esc(hi.lab)}</span>` : ''}</div>
        <div style="height:${BH}px;display:flex;align-items:flex-end"><div style="width:110px;height:${bh}px;border-radius:14px 14px 4px 4px;background:${c};${ol}"></div></div>
        <div style="font-size:30px;font-weight:900;white-space:nowrap;color:#3B4A63">${esc(o.k)}</div></div>`; }).join('') + `</div>`;
    const bq = s.bracket ? AT(s, s.bracket.at, .45, 0) : 0;
    h += `<div class="col" style="gap:26px;align-items:flex-start;position:relative">${R.map(row).join('')}</div>`;
    if (s.bracket) h += `<div style="position:relative;width:${140 + 22 * 4 + 170 * 4}px;height:74px"><div style="position:absolute;left:${140 + 22 * 4 + 170 * 3 + 85}px;top:14px;transform:translateX(-50%);white-space:nowrap;padding:8px 26px;border-radius:16px;border:4px solid ${RED};color:${RED};font-size:34px;font-weight:900;${POPQ(bq)}">${esc(s.bracket.lab)}</div></div>`;
    else h += `<div style="height:70px"></div>`;
    wrapC(`<div class="col" style="zoom:${s.z || 1.0};width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };
  /* 순위 칸: n칸에 순위 숫자, 우리 팀 칸에만 로고 */
  SCENE.ks_rank = (lt, s) => {
    const K = s._same, n = s.n || 10, q = K ? 1 : AT(s, s.at, .6, 0), sq = K ? 1 : seg(lt, .05, .45);
    let h = titleH(lt, s, 56, 40, K && s._prev.title === s.title);
    h += `<div class="row" style="gap:14px">` + Array.from({ length: n }, (_, i) => { const me = i + 1 === s.rank, mq = me ? q : 0;
      return `<div class="col" style="width:150px;height:240px;border-radius:24px;align-items:center;justify-content:center;gap:10px;opacity:${c01((sq - i * .03) * 2.4).toFixed(3)};
        background:${me && mq > .02 ? '#12161F' : '#fff'};border:3px solid ${me && mq > .02 ? '#12161F' : '#E3E7EE'};box-shadow:0 10px 26px rgba(18,22,31,.07)">
        <div style="height:96px;display:flex;align-items:center">${me ? `<div style="${POPQ(mq)}">${LG(s.team, 96)}</div>` : ''}</div>
        <div class="num" style="font-size:42px;font-weight:900;color:${me && mq > .02 ? '#fff' : '#9AA3B2'}">${i + 1}위</div>${me && s.note ? `<div class="num" style="font-size:34px;font-weight:900;color:#fff;opacity:${c01(mq * 2)}">${esc(s.note)}</div>` : ''}</div>`; }).join('') + `</div>`;
    wrapC(`<div class="col" style="zoom:1.05;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };
  Object.assign(MOTION, { ks_rank: s => .8, ks_sched: s => .8, ks_prob7: s => .8, ks_outs: s => .8 });
})();
/* @@KS1102END */
