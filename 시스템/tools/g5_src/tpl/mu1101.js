/* @@MU1101 11/1 20:20 롱폼㊱ 「1차전 핵심 맞대결」 장 — 사용자 "텍스트로 떼우는 거 없이 다 그림과 그래픽으로, 진짜 직관적으로".
   mu_pgames(투수 경기별 이닝칸·실점공) · mu_hr2(타자 둘 · 홈런공) · mu_streak(연타석 홈런) · mu_abs(타수 칸) · mu_blocks(맞대결 칸·득점 막대)
   mu_closer(마무리 비교 · 이탈 도장) · mu_donut(구종 도넛) · mu_fly(나비 막대) · mu_choice(두 갈래 선택) */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  const LG = (n, px) => { const tt = T(n); return tt && LOGO[tt.code] ? `<img src="${LOGO[tt.code]}" style="width:${px}px;height:${px}px;object-fit:contain;flex:0 0 auto">` : ''; };
  const PH = (x, w, h, extra = '') => { const src = photoSrc(x.img);
    return `<div style="width:${w}px;height:${h}px;border-radius:28px;overflow:hidden;position:relative;background:#E9EDF3;flex:0 0 auto;box-shadow:0 18px 40px rgba(18,22,31,.16);${extra}">${src ? `<div class="pp" style="position:absolute;inset:0">${photoImg(x, src, w, h, x.focus || '50% 14%')}</div>` : ''}</div>`; };
  const NM = (x, fs = 50) => `<div class="row" style="gap:10px;align-items:center;justify-content:center;margin-top:14px">${LG(x.team, fs)}<div style="font-size:${fs}px;font-weight:900;letter-spacing:-1.5px">${esc(x.name)}</div></div>`;
  const BALL = (px, fill = '#fff', stroke = '#D9DEE6', seam = '#E5484D') => `<svg width="${px}" height="${px}" viewBox="0 0 40 40" style="flex:0 0 auto"><circle cx="20" cy="20" r="17" fill="${fill}" stroke="${stroke}" stroke-width="2.5"/><path d="M11 7c5 6 5 20 0 26M29 7c-5 6-5 20 0 26" fill="none" stroke="${seam}" stroke-width="2.4" stroke-dasharray="3 2.6"/></svg>`;
  const POPQ = (q) => `opacity:${c01(q * 1.6)};transform:scale(${.7 + .3 * eo(q)})`;
  const card = (inner, extra = '') => `<div style="background:#fff;border-radius:30px;box-shadow:0 14px 36px rgba(18,22,31,.08);border:2px solid #EDF0F5;${extra}">${inner}</div>`;
  const prevItem = (s, key, i) => (s._same && s._prev && (s._prev[key] || [])[i]) || null;
  const was = (s, key, i) => { const p = prevItem(s, key, i); return !!(p && p.at != null && p.at < 50); };

  /* 투수: 경기마다 [상대 로고·날짜] [이닝 칸 9개 중 던진 만큼 채움] [실점 = 빨간 공 n개] [결과] */
  SCENE.mu_pgames = (lt, s) => {
    const K = s._same, rows = s.rows || [], col = TC_(s.team);
    const pp = K ? 1 : AT(s, s.at, .45, seg(lt, .05, .45));
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    const rowsH = rows.map((r, i) => {
      const p0 = was(s, 'rows', i) ? 1 : AT(s, r.at, .5, 0), pv_ = prevItem(s, 'rows', i), p = r.detAt == null ? p0 : (pv_ && pv_.detAt != null && pv_.detAt < 50 ? 1 : AT(s, r.detAt, .5, 0));
      const inn = Array.from({ length: 9 }, (_, k) => { const on = r.inn != null && k < Math.ceil(r.inn), part = r.inn != null && k === Math.floor(r.inn) && r.inn % 1 > 0;
        const q = c01((p - k * .05) * 2);
        return `<div class="col" style="width:40px;gap:4px;align-items:center"><div style="width:40px;height:54px;border-radius:10px;background:${on ? col : '#EEF1F5'};${part ? 'opacity:.55;' : ''}opacity:${on ? c01(q * 1.5) : 1}"></div><div class="num" style="font-size:20px;font-weight:800;color:#9AA3B2">${k + 1}</div></div>`; }).join('');
      const balls = Array.from({ length: Math.max(r.runs || 0, 0) }, (_, k) => `<div style="${POPQ(c01((p - .3 - k * .08) * 2))}">${BALL(54, RED, RED, '#fff')}</div>`).join('');
      const zero = (r.runs || 0) === 0 ? `<div class="row" style="gap:10px;align-items:center;${POPQ(c01((p - .3) * 2))}"><svg width="60" height="60" viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="${GREEN}"/><path d="M11 20l6 6 12-13" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg><b class="num" style="font-size:54px;color:${GREEN}">무실점</b></div>` : '';
      const res = r.res ? `<div class="num" style="width:96px;height:96px;border-radius:24px;background:${r.res === '승' ? GREEN : r.res === '패' ? RED : '#C9CFD9'};color:#fff;font-size:52px;font-weight:900;display:flex;align-items:center;justify-content:center;${POPQ(c01((p - .6) * 2))}">${esc(r.res)}</div>` : '<div style="width:96px"></div>';
      return card(`<div class="row" style="gap:30px;align-items:center;padding:26px 34px">
        <div class="num" style="width:180px;text-align:center;font-size:44px;font-weight:900;color:#3B4A63;white-space:nowrap">${esc(r.d)}</div>
        <div class="row" style="gap:6px;visibility:${r.inn != null ? 'visible' : 'hidden'}">${inn}</div>
        <div class="row" style="gap:8px;align-items:center;width:400px">${balls}${zero}${r.rl ? `<b class="num" style="margin-left:10px;font-size:48px;color:${RED};white-space:nowrap;${POPQ(c01((p - .5) * 2))}">${esc(r.rl)}</b>` : ''}</div>
        ${res}</div>`, `${rise(Math.max(p0, p), 30)}`);
    }).join('');
    const sq = (K && s._prev.statAt != null && s._prev.statAt < 50) ? 1 : AT(s, s.statAt, .45, 0);
    const stH = (s.stats || []).length ? `${s.statsCap ? `<div style="margin-top:12px;padding:4px 18px;border-radius:14px;background:#3B4A63;color:#fff;font-size:28px;font-weight:900;white-space:nowrap;opacity:${c01(sq * 1.6)}">${esc(s.statsCap)}</div>` : ''}<div class="row" style="gap:22px;margin-top:10px;opacity:${c01(sq * 1.6)}">${s.stats.map(t => `<div class="col" style="align-items:center"><b class="num" style="font-size:52px;line-height:1.05;letter-spacing:-1.5px;white-space:nowrap">${esc(t.v)}</b><span style="font-size:24px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(t.k)}</span></div>`).join('')}</div>` : '';
    h += `<div class="row" style="gap:46px;align-items:center"><div class="col" style="align-items:center;${rise(pp, 30)}">${PH(s, 330, rows.length > 1 ? 360 : 400)}${NM(s)}${stH}</div><div class="col" style="gap:22px;align-items:stretch">${rowsH}</div></div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.0;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 타자 둘: 사진 + 정규시즌 숫자(홈런·타점) + 플레이오프 홈런 공 */
  SCENE.mu_hr2 = (lt, s) => {
    const K = s._same, its = s.items || [];
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    const sq0 = (() => { const x = its[0] || {}, pv = prevItem(s, 'items', 0); return pv && pv.statAt != null && pv.statAt < 50 ? 1 : AT(s, x.statAt, .45, 0); })();
    const mid = `<div class="col" style="align-items:center;justify-content:flex-start;padding-top:${360 + 64 + 16 + 20}px;gap:0;opacity:${c01(sq0 * 1.6)}"><div class="row" style="gap:36px">${((its[0] || {}).stats || []).map(t => `<span style="min-width:130px;text-align:center;font-size:34px;font-weight:900;color:${GRAY}">${esc(t.k)}</span>`).join('')}</div></div>`;
    h += `<div class="row" style="gap:40px;align-items:flex-start;justify-content:center">` + its.map((x, i) => {
      const p = was(s, 'items', i) ? 1 : AT(s, x.at, .45, 0);
      const pv = prevItem(s, 'items', i);
      const sq = pv && pv.statAt != null && pv.statAt < 50 ? 1 : AT(s, x.statAt, .45, 0);
      const bq = pv && pv.ballAt != null && pv.ballAt < 50 ? 1 : AT(s, x.ballAt, .5, 0);
      const stats = (x.stats || []).map(t => `<div class="col" style="align-items:center;gap:0;min-width:130px"><b class="num" style="font-size:82px;line-height:1;letter-spacing:-3px;color:${TXT}">${esc(t.v)}</b></div>`).join('');
      const balls = Array.from({ length: x.balls || 0 }, (_, k) => `<div style="${POPQ(c01((bq - k * .2) * 2))}">${BALL(84, '#FFF6DA', '#F2B705', '#E5484D')}</div>`).join('');
      return `<div class="col" style="align-items:center;gap:16px;${rise(p, 30)}">${PH(x, 330, 360)}${NM(x)}
        <div class="row" style="gap:36px;opacity:${c01(sq * 1.6)};height:116px">${stats}</div>
        <div class="row" style="gap:16px;align-items:center;height:100px;opacity:${bq > 0 ? 1 : 0}">${balls}${x.ballLab ? `<span style="font-size:32px;font-weight:900;color:#8A5A00;margin-left:6px;white-space:nowrap">${esc(x.ballLab)}</span>` : ''}</div></div>`;
    }).join(`<div style="width:80px"></div>`) + `</div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.12;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 연타석 홈런: 경기별 타석 칸(홈런은 금색 공) + 이어지는 타석을 묶는 괄호 */
  SCENE.mu_streak = (lt, s) => {
    const K = s._same, games = s.games || [], col = TC_(s.team);
    const pp = K ? 1 : AT(s, s.at, .45, seg(lt, .05, .45));
    const bq = (K && s._prev.bracketAt != null && s._prev.bracketAt < 50) ? 1 : AT(s, s.bracketAt, .5, 0);
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    const gH = games.map((g, i) => {
      const p = was(s, 'games', i) ? 1 : AT(s, g.at, .5, 0);
      const abs = (g.abs || []).map((a, k) => { const q = c01((p - .2 - k * .25) * 2), hr = a.k === 'hr';
        return `<div class="col" style="width:150px;height:170px;border-radius:26px;background:${hr ? '#FFF6DA' : '#EEF1F5'};border:${hr ? `6px solid #F2B705` : '0'};align-items:center;justify-content:center;gap:6px;${POPQ(q)};${a.streak && bq > 0 ? `box-shadow:0 0 0 ${Math.round(8 * bq)}px rgba(229,72,77,.35)` : ''}">
          ${hr ? BALL(74, '#fff', '#F2B705') : `<div style="font-size:40px;font-weight:900;color:#9AA3B2">${esc(a.t || '')}</div>`}
          <div style="font-size:34px;font-weight:900;color:${hr ? '#8A5A00' : '#9AA3B2'};white-space:nowrap">${esc(a.t || '홈런')}</div></div>`; }).join('');
      return card(`<div class="col" style="gap:16px;align-items:center;padding:24px 30px">
        <div class="row" style="gap:12px;align-items:center"><div class="num" style="font-size:36px;font-weight:900;color:#3B4A63">${esc(g.d)}</div></div>
        <div class="row" style="gap:16px">${abs}</div>
        <div style="height:56px;display:flex;align-items:center">${g.note ? `<div class="num" style="height:56px;padding:0 26px;border-radius:999px;background:${col};color:#fff;font-size:34px;font-weight:900;display:flex;align-items:center;${POPQ(c01((p - .6) * 2))}">${esc(g.note)}</div>` : ''}</div></div>`, rise(p, 30));
    }).join('');
    h += `<div class="row" style="gap:46px;align-items:center"><div class="col" style="align-items:center;${rise(pp, 30)}">${PH(s, 320, 380)}${NM(s)}</div>
      <div class="col" style="gap:20px;align-items:center"><div class="row" style="gap:28px;align-items:stretch">${gH}</div>
      <div style="height:80px;display:flex;align-items:center;opacity:${c01(bq * 1.6)};transform:translateY(${(1 - eo(bq)) * 16}px)"><div class="num" style="height:76px;padding:0 40px;border-radius:999px;background:${RED};color:#fff;font-size:44px;font-weight:900;display:flex;align-items:center;gap:14px">${BALL(46, '#fff', '#fff')}${esc(s.bracket || '')}</div></div></div></div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.2;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 타수 칸: 안타는 구단 색, 아웃은 회색 */
  SCENE.mu_abs = (lt, s) => {
    const K = s._same, col = TC_(s.team), abs = s.abs || [];
    const pp = K ? 1 : AT(s, s.at, .45, seg(lt, .05, .45)), aq = AT(s, s.absAt, .5, 0);
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    const cells = abs.map((a, k) => { const q = c01((aq - k * .18) * 2);
      return `<div class="col" style="width:190px;height:230px;border-radius:30px;background:${a ? col : '#EEF1F5'};align-items:center;justify-content:center;gap:10px;${POPQ(q)}">
        ${a ? BALL(90, '#fff', '#fff') : `<svg width="80" height="80" viewBox="0 0 40 40"><path d="M10 10l20 20M30 10L10 30" stroke="#AAB2BF" stroke-width="5" stroke-linecap="round"/></svg>`}
        <div style="font-size:42px;font-weight:900;color:${a ? '#fff' : '#9AA3B2'}">${a ? '안타' : '아웃'}</div></div>`; }).join('');
    const n = abs.filter(Boolean).length;
    h += `<div class="row" style="gap:60px;align-items:center"><div class="col" style="align-items:center;${rise(pp, 30)}">${PH(s, 330, 400)}${NM(s)}</div>
      <div class="col" style="gap:26px;align-items:center"><div class="row" style="gap:18px">${cells}</div>
      <div class="num" style="font-size:96px;font-weight:900;letter-spacing:-3px;opacity:${c01((aq - .6) * 2.5)}">${abs.length}<span style="font-size:48px">타수</span> <span style="color:${col}">${n}</span><span style="font-size:48px;color:${col}">안타</span></div></div></div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.2;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 맞대결 칸: 한 칸 = 한 경기(이긴 팀 색·로고) + 득점 막대 */
  SCENE.mu_blocks = (lt, s) => {
    /* 11/1 22:01 사용자 "같은 팀 로고를 한 장면에 두 개씩 써야 하나" → 경기 칸은 구단 색 네모만, 로고는 아래 팀 칸에 한 번씩. 승수·득점은 팀 칸 안에 */
    const K = s._same, gs = s.groups || [];
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    const cells = gs.map((g, gi) => { const p = was(s, 'groups', gi) ? 1 : AT(s, g.at, .6, 0);
      return Array.from({ length: g.n }, (_, k) => { const q = c01((p - k * .07) * 2.2);
        return `<div style="position:relative;width:76px;height:76px;border-radius:18px;background:#E3E7EE"><div style="position:absolute;inset:0;border-radius:18px;background:${TC_(g.team)};${POPQ(q)};${g.hi ? 'box-shadow:0 0 0 6px #F2B705' : ''}"></div></div>`; }).join(''); }).join('');
    h += `<div class="row" style="gap:12px;align-items:center;flex-wrap:nowrap;margin-bottom:40px">${cells}</div>`;
    const teams = (s.tally && s.tally.items) || (s.runs && s.runs.items) || [];
    const tq = s.tally ? ((K && s._prev.tally && s._prev.tally.at != null && s._prev.tally.at < 50) ? 1 : AT(s, s.tally.at, .5, 0)) : 0;
    const rq = s.runs ? ((K && s._prev.runs && s._prev.runs.at != null && s._prev.runs.at < 50) ? 1 : AT(s, s.runs.at, .6, 0)) : 0;
    const mx = s.runs ? Math.max(...s.runs.items.map(r => r.v)) : 1;
    const col = t => { const tl = ((s.tally || {}).items || []).find(x => x.team === t.team), rn = ((s.runs || {}).items || []).find(x => x.team === t.team), c = TC_(t.team);
      const rv = rn ? Math.round(rn.v * eo(rq)) : 0, w = rn ? Math.round(420 * rn.v / mx * eo(rq)) : 0;
      return card(`<div class="col" style="width:560px;padding:30px 0;align-items:center;gap:16px">
        <div class="row" style="gap:24px;align-items:center">${LG(t.team, 110)}<div style="opacity:${c01(tq * 1.6)}"><b class="num" style="font-size:110px;letter-spacing:-3px;line-height:1;color:${c}">${esc(tl ? tl.v : '')}</b><span style="font-size:46px;font-weight:900;color:${GRAY}"> ${esc(tl ? tl.u : '')}</span></div></div>
        <div class="col" style="gap:8px;align-items:center;height:70px;opacity:${c01(rq * 3)}">
          <div class="row" style="gap:14px;align-items:center"><div style="width:420px;height:44px;border-radius:14px;background:#EEF1F5;overflow:hidden"><div style="width:${w}px;height:44px;background:${c}"></div></div><b class="num" style="font-size:54px;color:${c}">${rv}<span style="font-size:30px">점</span></b></div></div></div>`, `opacity:${c01(Math.max(tq, rq) * 1.6)}`); };
    h += `<div class="row" style="gap:60px;align-items:stretch">${teams.map(col).join('')}</div>`;
    h += `<div style="margin-top:18px;height:44px;font-size:34px;font-weight:900;color:${GRAY};opacity:${c01(rq * 3)}">${esc((s.runs || {}).label || '')}</div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.0;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 마무리 비교: 왼쪽 KT(로고) / 오른쪽 사진 — out 이 뜨면 사진이 흐려지고 '이탈' 도장 */
  SCENE.mu_closer = (lt, s) => {
    const K = s._same, L = s.l || {}, R = s.r || {};
    const side = (x, key) => { const pv = K && s._prev[key]; const p = pv && pv.at != null && pv.at < 50 ? 1 : AT(s, x.at, .45, 0);
      const oq = x.out ? (pv && pv.outAt != null && pv.outAt < 50 && pv.out ? 1 : AT(s, x.outAt, .45, 0)) : 0;
      const head = x.img ? `<div style="position:relative">${PH(x, 300, 330, `filter:grayscale(${(oq * .9).toFixed(2)})`)}${oq > 0 ? `<div class="num" style="position:absolute;left:50%;top:78%;transform:translate(-50%,-50%) rotate(-12deg) scale(${1.4 - .4 * eo(oq)});opacity:${c01(oq * 1.6)};padding:10px 34px;border:8px solid ${RED};border-radius:20px;color:${RED};background:rgba(255,255,255,.88);font-size:70px;font-weight:900;white-space:nowrap">${esc(x.out)}</div>` : ''}</div>`
        : `<div style="width:300px;height:330px;border-radius:28px;background:#fff;border:2px solid #EDF0F5;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 40px rgba(18,22,31,.08)">${LG(x.team, 230)}</div>`;
      const st = (x.stats || []).map(t => `<div class="col" style="align-items:center;gap:2px;min-width:150px"><b class="num" style="font-size:70px;line-height:1;letter-spacing:-2px;color:${t.hi ? TC_(x.team) : TXT}">${esc(t.v)}</b><span style="font-size:28px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(t.k)}</span></div>`).join('');
      return `<div class="col" style="align-items:center;gap:16px;${rise(p, 30)}">${head}${x.name ? NM(x, 46) : `<div style="height:64px;display:flex;align-items:center;font-size:44px;font-weight:900">${esc(x.label || '')}</div>`}
        ${card(`<div class="col" style="gap:8px;align-items:center;padding:18px 26px"><div style="font-size:30px;font-weight:900;color:#3B4A63">${esc(x.cap || '')}</div><div class="row" style="gap:18px">${st}</div></div>`)}</div>`; };
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    h += `<div class="row" style="gap:110px;align-items:flex-start">${side(L, 'l')}${side(R, 'r')}</div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.15;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 구종 도넛 */
  SCENE.mu_donut = (lt, s) => {
    const K = s._same, its = s.items || [], tot = its.reduce((a, x) => a + x.v, 0);
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    const R = 210, C = 2 * Math.PI * R; let acc = 0;
    const arcs = its.map((x, i) => { const q = was(s, 'items', i) ? 1 : AT(s, x.at, .6, 0), len = C * x.v / tot * eo(q);
      const a = `<circle cx="260" cy="260" r="${R}" fill="none" stroke="${x.c}" stroke-width="86" stroke-dasharray="${len} ${C}" stroke-dashoffset="${-acc}" transform="rotate(-90 260 260)"/>`; acc += C * x.v / tot; return a; }).join('');
    const leg = its.map((x, i) => { if (x.noLeg) return ''; const q = was(s, 'items', i) ? 1 : AT(s, x.at, .5, 0);
      return `<div class="row" style="gap:20px;align-items:center;${rise(q, 16)}"><div style="width:44px;height:44px;border-radius:12px;background:${x.c}"></div><div style="width:200px;font-size:52px;font-weight:900">${esc(x.k)}</div><b class="num" style="font-size:80px;color:${x.c === '#D5DAE2' ? GRAY : x.c}">${esc(String(x.v))}</b><span style="font-size:40px;font-weight:900;color:${GRAY}">구</span></div>`; }).join('');
    h += `<div class="row" style="gap:90px;align-items:center"><div style="position:relative;width:520px;height:520px"><svg width="520" height="520"><circle cx="260" cy="260" r="${R}" fill="none" stroke="#EEF1F5" stroke-width="86"/>${arcs}</svg>
      <div class="col" style="position:absolute;inset:0;align-items:center;justify-content:center"><b class="num" style="font-size:110px;line-height:1">${tot}</b><span style="font-size:40px;font-weight:900;color:${GRAY}">${esc(s.center || '구')}</span></div></div>
      <div class="col" style="gap:30px;align-items:flex-start">${leg}</div></div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.0;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 나비 막대: 가운데 항목, 왼쪽 팀 ← → 오른쪽 팀. 나쁜 쪽(worse) 빨간 테두리 */
  SCENE.mu_fly = (lt, s) => {
    const K = s._same, rows = s.rows || [], cl = TC_(s.lt), cr = TC_(s.rt);
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    h += `<div class="row" style="width:1500px;justify-content:space-between;align-items:center;margin-bottom:20px">${LG(s.lt, 130)}${LG(s.rt, 130)}</div>`;
    h += rows.map((r, i) => { const q = was(s, 'rows', i) ? 1 : AT(s, r.at, .6, 0), mx = Math.max(r.l, r.r), e = eo(c01(q * 1.3));
      const wl = Math.round(520 * r.l / mx * e), wr = Math.round(520 * r.r / mx * e);
      const fmt = v => r.dec ? (v * e).toFixed(r.dec) : String(Math.round(v * e));
      return `<div class="row" style="width:1500px;gap:0;align-items:center;height:130px;opacity:${c01(q * 3)}">
        <div class="row" style="width:600px;justify-content:flex-end;align-items:center;gap:18px"><b class="num" style="font-size:66px;color:${r.worse === 'l' ? RED : cl}">${fmt(r.l)}</b><div style="flex:0 0 auto;width:${wl}px;height:80px;border-radius:20px 0 0 20px;background:${cl};${r.worse === 'l' ? `outline:6px solid ${RED};outline-offset:3px` : ''}"></div></div>
        <div style="width:300px;text-align:center;font-size:40px;font-weight:900;letter-spacing:-1px;color:#3B4A63;white-space:nowrap">${esc(r.k)}</div>
        <div class="row" style="width:600px;justify-content:flex-start;align-items:center;gap:18px"><div style="flex:0 0 auto;width:${wr}px;height:80px;border-radius:0 20px 20px 0;background:${cr};${r.worse === 'r' ? `outline:6px solid ${RED};outline-offset:3px` : ''}"></div><b class="num" style="font-size:66px;color:${r.worse === 'r' ? RED : cr}">${fmt(r.r)}</b></div></div>`; }).join('');
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.1;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 두 갈래 선택: 가운데 팀 로고, 양쪽 그림 카드 */
  const ICO = {
    rest: c => `<svg width="150" height="150" viewBox="0 0 64 64"><rect x="8" y="12" width="48" height="44" rx="8" fill="#fff" stroke="${c}" stroke-width="4"/><rect x="8" y="12" width="48" height="12" rx="6" fill="${c}"/><path d="M26 34h12l-12 12h12" fill="none" stroke="${c}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    record: c => `<svg width="150" height="150" viewBox="0 0 64 64"><rect x="10" y="34" width="10" height="20" rx="3" fill="${c}"/><rect x="27" y="22" width="10" height="32" rx="3" fill="${c}"/><rect x="44" y="12" width="10" height="42" rx="3" fill="${c}"/></svg>`,
  };
  SCENE.mu_choice = (lt, s) => {
    const K = s._same, its = s.items || [], col = TC_(s.team);
    const lq = K ? 1 : AT(s, s.at, .45, seg(lt, .05, .45)), qq = AT(s, s.qAt, .45, 0);
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    const side = (x, i) => { const q = was(s, 'items', i) ? 1 : AT(s, x.at, .5, 0);
      return card(`<div class="col" style="width:420px;padding:34px 0;align-items:center;gap:14px">${ICO[x.ic](col)}<div style="font-size:58px;font-weight:900">${esc(x.k)}</div><div style="display:flex;gap:10px;align-items:center">${(x.who || []).map(w => `<span style="font-size:34px;font-weight:900;color:${col}">${esc(w)}</span>`).join('')}</div></div>`, POPQ(q)); };
    h += `<div class="row" style="gap:70px;align-items:center">${side(its[0], 0)}
      <div class="col" style="align-items:center;gap:14px;${POPQ(lq)}">${LG(s.team, 200)}<div class="num" style="width:120px;height:120px;border-radius:50%;background:${col};color:#fff;font-size:80px;font-weight:900;display:flex;align-items:center;justify-content:center;${POPQ(qq)}">?</div></div>
      ${side(its[1], 1)}</div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.1;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };


  /* 이닝 띠: 사진 + 1~9회 칸(구간마다 색·이름) + 표시(교체 시점 등) + 아래 작은 그림 배지 */
  const BIC = {
    bat: c => `<svg width="70" height="70" viewBox="0 0 64 64"><path d="M14 52L46 14" stroke="${c}" stroke-width="9" stroke-linecap="round"/><circle cx="50" cy="48" r="7" fill="#fff" stroke="${c}" stroke-width="4"/></svg>`,
    run: c => `<svg width="70" height="70" viewBox="0 0 64 64"><circle cx="38" cy="12" r="7" fill="${c}"/><path d="M30 24l-10 14 12 6-6 14M30 24l12 6 8-6M32 44l14 4" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    bunt: c => `<svg width="70" height="70" viewBox="0 0 64 64"><path d="M10 26h44" stroke="${c}" stroke-width="9" stroke-linecap="round"/><circle cx="32" cy="46" r="8" fill="#fff" stroke="${c}" stroke-width="4"/></svg>`,
  };
  SCENE.mu_inn = (lt, s) => {
    const K = s._same, segs = s.segs || [], col = TC_(s.team);
    const pp = K ? 1 : AT(s, s.at, .45, seg(lt, .05, .45));
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    const cellOf = n => { const g = segs.find(x => n >= x.frm && n <= x.to); return g ? [g, segs.indexOf(g)] : [null, -1]; };
    const cells = Array.from({ length: 9 }, (_, k) => { const n = k + 1, [g, gi] = cellOf(n);
      const q = g ? (was(s, 'segs', gi) ? 1 : c01((AT(s, g.at, .6, 0) - (n - g.frm) * .08) * 2)) : 0;
      const bg = !g ? '#EEF1F5' : g.skip ? '#fff' : (g.c || col);
      return `<div class="col" style="width:112px;gap:8px;align-items:center"><div style="position:relative;width:112px;height:120px;border-radius:20px;background:#EEF1F5;overflow:hidden">
        <div style="position:absolute;inset:0;background:${bg};${g && g.skip ? `border:5px dashed ${RED};border-radius:20px;box-sizing:border-box;` : ''}opacity:${c01(q * 1.5)}"></div>
        ${g && g.skip && q > 0 ? `<svg style="position:absolute;inset:0;margin:auto;opacity:${c01(q * 1.5)}" width="70" height="70" viewBox="0 0 40 40"><path d="M10 10l20 20M30 10L10 30" stroke="${RED}" stroke-width="5" stroke-linecap="round"/></svg>` : ''}
        ${g && g.hi && q > 0 ? `<div style="position:absolute;inset:0;box-shadow:inset 0 0 0 6px #F2B705;border-radius:20px;opacity:${c01(q * 1.5)}"></div>` : ''}</div>
        <div class="num" style="font-size:28px;font-weight:900;color:#9AA3B2">${n}회</div></div>`; }).join('');
    const labs = segs.map((g, gi) => { const q = was(s, 'segs', gi) ? 1 : AT(s, g.at, .6, 0), w = (g.to - g.frm + 1) * 112 + (g.to - g.frm) * 12;
      return `<div style="position:absolute;left:${(g.frm - 1) * 124}px;width:${w}px;top:0;display:flex;flex-direction:column;align-items:center;opacity:${c01(q * 1.6)}"><div style="width:100%;height:14px;border:5px solid ${g.skip ? RED : g.c || col};border-top:0;border-radius:0 0 12px 12px;box-sizing:border-box"></div><div style="margin-top:8px;font-size:36px;font-weight:900;white-space:nowrap;color:${g.skip ? RED : TXT}">${esc(g.lab || '')}</div></div>`; }).join('');
    const marks = (s.marks || []).map((m, i) => { const pv = K && (s._prev.marks || [])[i], q = pv && pv.at != null && pv.at < 50 ? 1 : AT(s, m.at, .45, 0);
      return `<div style="position:absolute;left:${m.inn * 124 - 6}px;top:-30px;height:200px;border-left:6px dashed ${RED};opacity:${c01(q * 1.6)}"><div class="num" style="position:absolute;top:-56px;left:50%;transform:translateX(-50%);white-space:nowrap;height:52px;padding:0 20px;border-radius:999px;background:${RED};color:#fff;font-size:30px;font-weight:900;display:flex;align-items:center">${esc(m.lab)}</div></div>`; }).join('');
    const badges = (s.badges || []).map((b, i) => { const pv = K && (s._prev.badges || [])[i], q = pv && pv.at != null && pv.at < 50 ? 1 : AT(s, b.at, .45, 0);
      const lgo = b.team && b.team !== s.team && (s.badges || []).findIndex(z => z.team === b.team) === i;   /* 11/1 22:45 한 장면에 같은 팀 로고 한 번 */
      return card(`<div class="row" style="gap:14px;align-items:center;padding:12px 26px">${lgo ? LG(b.team, 56) : ''}${BIC[b.ic] ? BIC[b.ic](TC_(b.team || s.team)) : ''}<div style="font-size:40px;font-weight:900;white-space:nowrap">${esc(b.lab)}</div></div>`, POPQ(q)); }).join('');
    h += `<div class="row" style="gap:46px;align-items:center"><div class="col" style="align-items:center;${rise(pp, 30)}">${PH(s, 300, 360)}${NM(s)}</div>
      <div class="col" style="gap:20px;align-items:flex-start"><div style="position:relative;margin-top:60px"><div class="row" style="gap:12px">${cells}</div>${marks}</div>
      <div style="position:relative;height:80px;width:1100px">${labs}</div>
      <div class="row" style="gap:20px;min-height:90px">${badges}</div></div></div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.05;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };

  /* 사진 + 아이콘 개수(홀드 등) + 평균자책점 눈금(높을수록 빨강) */
  SCENE.mu_pstat = (lt, s) => {
    const K = s._same, col = TC_(s.team);
    const pp = K ? 1 : AT(s, s.at, .45, seg(lt, .05, .45)), iq = AT(s, s.iconAt, .6, 0), eq = AT(s, s.eraAt, .6, 0);
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    const icons = Array.from({ length: s.n || 0 }, (_, k) => `<div style="${POPQ(c01((iq - k * .02) * 2))}">${BALL(52, '#fff', col, col)}</div>`).join('');
    const mx = s.max || 7, v = s.era || 0, W = 900, x = Math.round(W * v / mx * eo(eq));
    const ticks = Array.from({ length: mx + 1 }, (_, k) => `<div class="num" style="position:absolute;left:${Math.round(W * k / mx) - 10}px;top:72px;font-size:26px;font-weight:800;color:#9AA3B2">${k}</div>`).join('');
    h += `<div class="row" style="gap:60px;align-items:center"><div class="col" style="align-items:center;${rise(pp, 30)}">${PH(s, 320, 390)}${NM(s)}</div>
      <div class="col" style="gap:40px;align-items:flex-start">
        <div class="col" style="gap:12px"><div class="row" style="gap:10px;flex-wrap:wrap;width:${W}px">${icons}</div><div class="num" style="font-size:60px;font-weight:900;opacity:${c01(iq * 2)}">${s.n}<span style="font-size:34px;color:${GRAY}"> ${esc(s.iconLab || '')}</span></div></div>
        <div class="col" style="gap:10px;opacity:${c01(eq * 3)}"><div style="font-size:36px;font-weight:900;color:#3B4A63">${esc(s.eraLab || '평균자책점')}</div>
          <div style="position:relative;width:${W}px;height:110px"><div style="position:absolute;left:0;top:20px;width:${W}px;height:44px;border-radius:22px;background:linear-gradient(90deg,#16A34A,#F2B705 55%,#E5484D)"></div>
          <div style="position:absolute;left:${x - 4}px;top:4px;width:8px;height:76px;border-radius:4px;background:${TXT}"></div>${ticks}
          <div class="num" style="position:absolute;left:${Math.min(x - 70, W - 150)}px;top:-78px;font-size:72px;font-weight:900;color:${RED}">${esc(String(v.toFixed ? v.toFixed(2) : v))}</div></div></div></div></div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.1;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };
  Object.assign(MOTION, { mu_inn: s => .8, mu_pstat: s => .8 });
  /* 11/1 22:40 불펜 싸움: 두 팀 불펜 카드(로고 한 번). KT = 평균자책점 게이지(경고 아이콘), 삼성 = 등판 사람 아이콘 n개(배터리 아이콘). VS 없음 */
  SCENE.mu_pen2 = (lt, s) => {
    const K = s._same, L = s.l || {}, R = s.r || {};
    const PERSON = (px, c) => `<svg width="${px}" height="${px}" viewBox="0 0 40 40" style="flex:0 0 auto"><circle cx="20" cy="11" r="7.5" fill="${c}"/><path d="M6 38c0-9 6-15 14-15s14 6 14 15z" fill="${c}"/></svg>`;
    const WARN = `<svg width="78" height="78" viewBox="0 0 40 40"><path d="M20 3 L38 35 H2 Z" fill="${RED}"/><rect x="18" y="13" width="4" height="12" rx="2" fill="#fff"/><circle cx="20" cy="30" r="2.4" fill="#fff"/></svg>`;
    const BATT = `<svg width="96" height="60" viewBox="0 0 48 30"><rect x="2" y="3" width="38" height="24" rx="5" fill="#fff" stroke="#E8730C" stroke-width="3"/><rect x="41" y="10" width="5" height="10" rx="2" fill="#E8730C"/><rect x="6" y="7" width="8" height="16" rx="2" fill="#E8730C"/></svg>`;
    const head = (x, ico) => `<div class="row" style="gap:18px;align-items:center;justify-content:space-between;width:100%"><div class="row" style="gap:16px;align-items:center">${LG(x.team, 96)}<div style="font-size:58px;font-weight:900;letter-spacing:-1.5px">${esc(x.label)}</div></div>${ico}</div>`;
    const lq = K ? 1 : AT(s, L.at, .45, 0), rq = K ? 1 : AT(s, R.at, .45, 0);
    const W = 600, mx = 7, v = +L.v || 0, gx = Math.round(W * v / mx * eo(lq));
    const ticks = Array.from({ length: mx + 1 }, (_, k) => `<div class="num" style="position:absolute;left:${Math.round(W * k / mx) - 8}px;top:66px;font-size:24px;font-weight:800;color:#9AA3B2">${k}</div>`).join('');
    const lBody = `<div class="col" style="gap:6px;align-items:center;width:${W}px"><div class="num" style="font-size:120px;font-weight:900;line-height:1;color:${RED}">${esc(String(L.v))}</div><div style="font-size:34px;font-weight:900;color:#3B4A63;margin-bottom:26px">${esc(L.cap)}</div>
      <div style="position:relative;width:${W}px;height:100px"><div style="position:absolute;left:0;top:18px;width:${W}px;height:40px;border-radius:20px;background:linear-gradient(90deg,#16A34A,#F2B705 55%,#E5484D)"></div><div style="position:absolute;left:${gx - 4}px;top:4px;width:8px;height:68px;border-radius:4px;background:${TXT}"></div>${ticks}</div></div>`;
    const n = +R.n || 0, ppl = Array.from({ length: n }, (_, k) => `<div style="${POPQ(c01((rq - k * .015) * 2))}">${PERSON(44, '#E8730C')}</div>`).join('');
    const rBody = `<div class="col" style="gap:6px;align-items:center;width:${W}px"><div class="num" style="font-size:120px;font-weight:900;line-height:1;color:#E8730C">${esc(String(R.v))}</div><div style="font-size:34px;font-weight:900;color:#3B4A63;margin-bottom:26px">${esc(R.cap)}</div>
      <div class="row" style="gap:4px;flex-wrap:wrap;width:${12 * 48}px;justify-content:center">${ppl}</div></div>`;
    const box = (x, q, ico, body) => `<div style="opacity:${c01(q * 2)};${rise(q, 24)}">${card(`<div class="col" style="gap:34px;align-items:center;padding:40px 50px;width:${W + 100}px;height:520px;box-sizing:border-box">${head(x, ico)}${body}</div>`)}</div>`;
    let h = titleH(lt, s, 56, 26, K && s._prev.title === s.title);
    h += `<div class="row" style="gap:70px;align-items:flex-start">${box(L, lq, WARN, lBody)}${box(R, rq, BATT, rBody)}</div>`;
    h += textH(lt, s, .8, 60); wrapC(`<div class="col" style="zoom:1.15;width:fit-content;margin:0 auto;align-items:center">${h}</div>`);
  };
  Object.assign(MOTION, { mu_pen2: s => .8 });


  Object.assign(MOTION, { mu_pgames: s => .8, mu_hr2: s => .8, mu_streak: s => .8, mu_abs: s => .8, mu_blocks: s => .8, mu_closer: s => .8, mu_donut: s => .8, mu_fly: s => .8, mu_choice: s => .8 });
})();
/* @@MU1101END */
