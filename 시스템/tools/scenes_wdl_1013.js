/* @@WDL1013 — 10/13 밤 사용자("이런 것도 눈에 너무 안 들어와" — 상대전적 글 카드): 상대전적을 칸 그림으로.
   rows:[{team, w, d, l, at, tag, tagAt, c}] — 로고 · 경기 수만큼 칸(승 파랑·무 회색·패 빨강, 호흡 at 에 왼쪽부터 채워짐) · "4승 1무 11패" 한 줄 · 꼬리표(tag) */
SCENE.wdl = (lt, s) => {
  const rows = s.rows || [], N = Math.max(...rows.map(r => (r.w || 0) + (r.d || 0) + (r.l || 0)), 1), CW = Math.min(52, Math.floor(880 / N) - 6);
  let h = s.title ? `<div class="title" style="font-size:56px;font-weight:900;margin-bottom:34px;${rise(seg(lt, 0, .4), 20)}">${br(s.title)}</div>` : '';
  h += `<div class="col" style="gap:30px;align-items:flex-start">` + rows.map((r, i) => {
    const p = pk(s, r.at, .9, seg(lt, .2 + i * .4, .9)), t = T(r.team || ''), n = (r.w || 0) + (r.d || 0) + (r.l || 0);
    const cells = Array.from({ length: n }, (_, k) => { const c = k < r.w ? ACC : k < r.w + (r.d || 0) ? '#A9B1BE' : RED;
      return `<div style="width:${CW}px;height:${CW + 18}px;border-radius:10px;background:${c};${pop(c01(p * 1.6 - k / n))}"></div>`; }).join('');
    const tp = r.tag ? pk(s, r.tagAt, .45, 0) : 0;
    return `<div class="row" style="gap:26px;align-items:center;${rise(c01(p * 3), 24)}">
      <div class="chip" style="width:120px;height:120px;flex:0 0 120px">${LOGO[t.code] ? `<img src="${LOGO[t.code]}">` : ''}</div>
      <div class="row" style="gap:6px;flex:0 0 ${N * (CW + 6)}px;width:${N * (CW + 6)}px;justify-content:flex-start">${cells}</div>
      <div class="num" style="font-size:60px;font-weight:900;letter-spacing:-2px;white-space:nowrap;color:${r.c === 'good' ? ACC : r.c === 'bad' ? RED : TXT};margin-left:10px;opacity:${c01(p * 1.6 - .6)}">${r.w}승${r.d ? ' ' + r.d + '무' : ''} ${r.l}패</div>
      ${r.tag ? `<div class="badge" style="background:${RED};font-size:38px;padding:10px 24px;white-space:nowrap;${pop(tp)}">${esc(r.tag)}</div>` : ''}</div>`;
  }).join('') + `</div>`;
  /* 10/13 밤 사용자("숫자의 위치가 들쑥날쑥"): 칸 영역 폭을 가장 긴 줄 기준으로 고정 → 모든 줄의 숫자가 같은 세로선에서 시작 */
  if (s.text) h += `<div class="big gold" style="margin-top:28px;font-size:${s.size || 52}px;${pop(pk(s, s.textAt, .5, seg(lt, .9, .5)))}">${br(s.text)}</div>`;
  h += `<div class="row" style="gap:28px;margin-top:30px;font-size:34px;font-weight:800;color:${GRAY};opacity:${c01(seg(lt, .4, .5))}">
    <span><span style="display:inline-block;width:26px;height:26px;border-radius:7px;background:${ACC};vertical-align:-3px;margin-right:8px"></span>승</span>
    <span><span style="display:inline-block;width:26px;height:26px;border-radius:7px;background:#A9B1BE;vertical-align:-3px;margin-right:8px"></span>무</span>
    <span><span style="display:inline-block;width:26px;height:26px;border-radius:7px;background:${RED};vertical-align:-3px;margin-right:8px"></span>패</span></div>`;
  B(LR('', h));
};
/* comeback — 10/13 밤 사용자("이런 것도 뭔지 한눈에 안 들어와" — 1위 싸움 글 흐름): 역전승 한 경기를 점수판으로.
   {date, home, away, from:[원정,홈], to:[원정,홈], scoreAt:[시작,끝], stamp, stampAt, pills:[{t,at,c}]} */
SCENE.comeback = (lt, s) => {
  const A = T(s.away || ''), H = T(s.home || ''), f = s.from || [0, 0], t = s.to || [0, 0], sa = s.scoreAt || [.2, .9];
  const q = (() => { const a = pk(s, sa[0], .01, 0), b = pk(s, sa[1], .01, 0); if (a <= 0) return 0; const segs = (EP.segT || [])[s.startLine] || []; const i0 = Math.floor(sa[0]), i1 = Math.floor(sa[1]);
    const T0 = (segs[i0] ?? 0) + ((segs[i0 + 1] ?? segs[i0] + 1.5) - (segs[i0] ?? 0)) * (sa[0] - i0), T1 = (segs[i1] ?? 0) + ((segs[i1 + 1] ?? segs[i1] + 1.5) - (segs[i1] ?? 0)) * (sa[1] - i1);
    return c01((NOW - T0) / Math.max(.3, T1 - T0)); })();
  const sc = (a, b) => Math.round(a + (b - a) * eo(q)), av = sc(f[0], t[0]), hv = sc(f[1], t[1]);
  const sp = s.stamp ? pk(s, s.stampAt, .35, 0) : 0;
  const logo = (tm, v, lead) => `<div class="col" style="gap:14px;align-items:center;width:420px">
      <div class="chip" style="width:200px;height:200px">${LOGO[tm.code] ? `<img src="${LOGO[tm.code]}">` : ''}</div>
      <div class="num" style="font-size:190px;font-weight:900;line-height:1;letter-spacing:-6px;color:${lead ? ACC : '#9AA3B2'}">${v}</div></div>`;
  let h = `<div class="badge" style="background:${VN};font-size:42px;padding:10px 30px;margin-bottom:26px;${pop(seg(lt, 0, .4))}">${esc(s.date || '')}</div>`;
  h += `<div class="row" style="gap:40px;align-items:flex-end;justify-content:center;position:relative">${logo(A, av, av > hv)}<div class="num" style="font-size:120px;font-weight:900;color:#C9D0DA;padding-bottom:30px">:</div>${logo(H, hv, hv > av)}
    ${s.stamp ? `<div style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%) rotate(-10deg) scale(${(1.8 - .8 * eo(sp)).toFixed(3)});opacity:${c01(sp * 3)};border:8px solid ${RED};border-radius:20px;padding:6px 34px;background:rgba(255,255,255,.9);color:${RED};font-size:76px;font-weight:900;white-space:nowrap">${esc(s.stamp)}</div>` : ''}</div>`;
  const pills = s.pills || [];
  if (pills.length) h += `<div class="row" style="gap:22px;margin-top:34px;justify-content:center;min-height:86px">` + pills.map(pl => `<div class="badge" style="background:${pl.c === 'navy' ? VN : ACC};font-size:46px;padding:12px 34px;white-space:nowrap;${pop(pk(s, pl.at, .4, 0))}">${esc(pl.t)}</div>`).join('') + `</div>`;
  B(LR('', h));
};
/* gradesort — 10/13 밤 사용자("흩어져 있는 팀을 등급별로 분류가 되는 모션그래픽"): 흩어진 로고가 등급을 말하는 호흡에 그 등급 줄로 날아가 자리 잡는다.
   rows:[{g, c, at, teams:[{team, note}]}] */
SCENE.gradesort = (lt, s) => {
  const rows = s.rows || [], W = 1100, RH = 128, H = rows.length * RH, LG = 100, SX = 190;
  const SCAT = [[120, 60], [560, 20], [900, 90], [300, 230], [760, 260], [60, 420], [480, 400], [940, 430], [220, 560], [700, 560], [380, 120], [620, 180]];
  const segs = (EP.segT || [])[s.startLine] || [];
  const tOf = k => { if (k == null) return null; const i = Math.floor(k), f = k - i, t0 = segs[i] ?? segs[segs.length - 1] ?? 0, t1 = segs[i + 1] ?? t0 + 1.5; return t0 + (t1 - t0) * f; };
  let idx = 0, h = `<div style="position:relative;width:${W}px;height:${H}px">`;
  rows.forEach((r, ri) => {
    const ta = tOf(r.at), q = ta == null ? 1 : c01((NOW - ta) / .7), col = r.c === 'good' ? GREEN : r.c === 'bad' ? RED : r.c === 'navy' ? '#3B4A63' : ACC, y = ri * RH;
    h += `<div style="position:absolute;left:0;top:${y + 10}px;width:108px;height:108px;border-radius:28px;background:${col};color:#fff;display:flex;align-items:center;justify-content:center;font-size:66px;font-weight:900;${pop(c01(q * 2))}">${esc(r.g)}</div>`;
    h += `<div style="position:absolute;left:130px;top:${y + RH - 6}px;width:${W - 130}px;height:3px;background:${LINE};opacity:${c01(q * 2)}"></div>`;
    (r.teams || []).forEach((tm, k) => {
      const t = T(tm.team || tm), sc = SCAT[idx % SCAT.length], ex = 150 + k * SX, ey = y + 4, e = eo(q);
      const appear = c01(seg(lt, .1 + idx * .06, .4)), wob = (1 - e) * Math.sin(NOW * 2.2 + idx) * 8;
      const x = sc[0] + (ex - sc[0]) * e, yy = sc[1] + (ey - sc[1]) * e + wob, rot = (1 - e) * ((idx % 2 ? 1 : -1) * 10);
      h += `<div class="col" style="position:absolute;left:${x.toFixed(1)}px;top:${yy.toFixed(1)}px;width:${LG + 60}px;margin-left:-30px;align-items:center;gap:2px;transform:rotate(${rot.toFixed(1)}deg) scale(${(0.6 + 0.4 * appear).toFixed(3)});opacity:${appear.toFixed(3)}">
        <div class="chip" style="width:${LG}px;height:${LG * .78}px">${LOGO[t.code] ? `<img src="${LOGO[t.code]}">` : ''}</div>
        <div style="font-size:30px;font-weight:900;color:${col};white-space:nowrap;opacity:${c01(q * 2 - 1)}">${esc(tm.note || '')}</div></div>`;
      idx++;
    });
  });
  h += `</div>`;
  B(LR('', h));
};
/* swing — 10/13 밤 사용자("한눈에 안 들어온다" — 글 카드 4장): 왼쪽 = 예상 순위 → 최종 순위 기울기선(로고가 선을 따라 이동),
   오른쪽 = 득실차로 본 기대 승수 → 실제 승수(숫자가 세지고 막대가 늘거나 줄어듦 + ±승 알약). 
   ranks:[{team, from, to, at, c, tag}] · wins:[{team, exp, act, at, c, tag}] · lt/rt = 두 칸 제목 */
SCENE.swing = (lt, s) => {
  const RH = 54, AX = 70, X0 = 180, X1 = 560, Y0 = 70, LW = 680, LG = 84;
  const colOf = c => c === 'bad' ? RED : GREEN;
  let L = `<div style="position:relative;width:${LW}px;height:${Y0 + RH * 10 + 20}px">`;
  L += `<div style="position:absolute;left:0;top:0;width:${LW}px;text-align:center;font-size:40px;font-weight:900;color:${TXT}">${esc(s.lt || '예상 순위 → 최종 순위')}</div>`;
  L += `<div style="position:absolute;left:${X0 - 80}px;top:${Y0 - 8}px;width:160px;text-align:center;font-size:28px;font-weight:800;color:${GRAY}">3월 예상</div>`;
  L += `<div style="position:absolute;left:${X1 - 80}px;top:${Y0 - 8}px;width:160px;text-align:center;font-size:28px;font-weight:800;color:${GRAY}">최종</div>`;
  for (let r = 1; r <= 10; r++) { const y = Y0 + 30 + (r - 1) * RH;
    L += `<div style="position:absolute;left:0;top:${y - 18}px;width:${AX}px;text-align:right;font-size:30px;font-weight:900;color:#9AA3B2">${r}위</div>`;
    L += `<div style="position:absolute;left:${AX + 20}px;top:${y}px;width:${LW - AX - 40}px;height:2px;background:${LINE}"></div>`; }
  let svg = `<svg style="position:absolute;left:0;top:0" width="${LW}" height="${Y0 + RH * 10 + 20}">`, logos = '';
  (s.ranks || []).forEach((r, i) => {
    const q = pk(s, r.at, 1.1, 1), e = eo(q), col = colOf(r.c), ya = Y0 + 30 + (r.from - 1) * RH, yb = Y0 + 30 + (r.to - 1) * RH;
    const x = X0 + (X1 - X0) * e, y = ya + (yb - ya) * e, vis = c01(q * 4);
    svg += `<line x1="${X0}" y1="${ya}" x2="${x.toFixed(1)}" y2="${y.toFixed(1)}" stroke="${col}" stroke-width="9" stroke-linecap="round" opacity="${vis}"/>`;
    svg += `<circle cx="${X0}" cy="${ya}" r="12" fill="#fff" stroke="${col}" stroke-width="6" opacity="${vis}"/>`;
    const t = T(r.team || '');
    logos += `<div class="chip" style="position:absolute;left:${(x - LG / 2).toFixed(1)}px;top:${(y - LG * .39).toFixed(1)}px;width:${LG}px;height:${LG * .78}px;opacity:${vis};background:#fff;border:4px solid ${col};border-radius:16px">${LOGO[t.code] ? `<img src="${LOGO[t.code]}">` : ''}</div>`;
    const tp = c01((q - .85) / .15);
    if (r.tag) logos += `<div class="badge" style="position:absolute;left:${X1 + 52}px;top:${yb - 26}px;background:${col};font-size:30px;padding:6px 16px;white-space:nowrap;${pop(tp)}">${esc(r.tag)}</div>`;
  });
  L += svg + `</svg>` + logos + `</div>`;
  /* 오른쪽: 기대 승수 → 실제 승수 */
  const RW = 700, BX = 150, BW = 500, MX = 85;
  let R = `<div style="position:relative;width:${RW}px;height:${Y0 + RH * 10 + 20}px">`;
  R += `<div style="position:absolute;left:0;top:0;width:${RW}px;text-align:center;font-size:40px;font-weight:900;color:${TXT}">${esc(s.rt || '득실차로 본 기대 승수 → 실제 승수')}</div>`;
  (s.wins || []).forEach((w, i) => {
    const q = pk(s, w.at, 1.1, 1), e = eo(q), col = colOf(w.c), y = Y0 + 70 + i * 250, vis = c01(q * 4), t = T(w.team || '');
    const v = Math.round(w.exp + (w.act - w.exp) * e), sc = n => BW * n / MX;
    R += `<div style="opacity:${vis}">`;
    R += `<div class="chip" style="position:absolute;left:0;top:${y}px;width:120px;height:94px">${LOGO[t.code] ? `<img src="${LOGO[t.code]}">` : ''}</div>`;
    R += `<div style="position:absolute;left:${BX}px;top:${y - 6}px;font-size:28px;font-weight:800;color:${GRAY}">기대 ${w.exp}승</div>`;
    R += `<div style="position:absolute;left:${BX}px;top:${y + 34}px;width:${sc(w.exp)}px;height:56px;border-radius:10px;background:#D5DAE3"></div>`;
    const a = Math.min(w.exp, v), b = Math.max(w.exp, v);
    if (w.act >= w.exp) R += `<div style="position:absolute;left:${BX + sc(a)}px;top:${y + 34}px;width:${sc(b - a)}px;height:56px;border-radius:0 10px 10px 0;background:${col}"></div>`;
    else R += `<div style="position:absolute;left:${BX + sc(a)}px;top:${y + 34}px;width:${sc(b - a)}px;height:56px;background:repeating-linear-gradient(45deg,${col}55 0 10px,#fff 10px 20px);border:3px dashed ${col};box-sizing:border-box"></div>`;
    R += `<div style="position:absolute;left:${BX}px;top:${y + 34}px;width:${sc(Math.min(v, w.exp))}px;height:56px;border-radius:10px;background:${w.act >= w.exp ? '#D5DAE3' : col}"></div>`;
    R += `<div style="position:absolute;left:${BX}px;top:${y + 100}px;font-size:58px;font-weight:900;color:${col}">실제 ${v}승</div>`;
    const tp = c01((q - .85) / .15), d = w.act - w.exp;
    R += `<div class="badge" style="position:absolute;left:${BX + 330}px;top:${y + 108}px;background:${col};font-size:40px;padding:8px 22px;white-space:nowrap;${pop(tp)}">${d > 0 ? '+' : '−'}${Math.abs(d)}승</div>`;
    if (w.tag) R += `<div style="position:absolute;left:${BX}px;top:${y + 176}px;font-size:30px;font-weight:800;color:${GRAY};opacity:${tp}">${esc(w.tag)}</div>`;
    R += `</div>`;
  });
  R += `</div>`;
  B(LR('', `<div class="row" style="gap:70px;align-items:flex-start;justify-content:center">${L}<div style="width:3px;align-self:stretch;background:${LINE}"></div>${R}</div>`));
};
/* psladder — 10/13 밤 사용자("너무 대충 만들었어" — 달력 아이콘 3칸): 포스트시즌 계단. 왼쪽 아래 와일드카드부터 오른쪽 위 한국시리즈까지
   계단이 호흡마다 솟고 그 단의 팀 로고가 올라선다. 이긴 팀이 다음 단으로 올라간다는 화살표.
   steps:[{name, sub, teams:[{team, rank}], at, trophy}] */
SCENE.psladder = (lt, s) => {
  const st = s.steps || [], N = st.length, CW = 330, GAP = 34, W = N * CW + (N - 1) * GAP, H = 700, HB = [170, 250, 330, 410], LG = 96;
  let h = `<div style="position:relative;width:${W}px;height:${H}px">` + (s.title ? `<div style="position:absolute;left:0;top:10px;font-size:54px;font-weight:900;color:${TXT}">${esc(s.title)}</div>` : '');
  st.forEach((p, i) => {
    const q = pk(s, p.at, .8, 1), e = eo(q), bh = (HB[i] || 410) * e, x = i * (CW + GAP), last = i === N - 1;
    const col = last ? ACC : i === 0 ? '#5B6B86' : i === 1 ? '#45577A' : '#2F4166';
    h += `<div style="position:absolute;left:${x}px;bottom:0;width:${CW}px;height:${bh.toFixed(1)}px;border-radius:18px 18px 0 0;background:${col};opacity:${c01(bh / 40).toFixed(3)};overflow:hidden;color:#fff;display:flex;flex-direction:column;align-items:center;padding-top:22px;box-sizing:border-box">
      <div style="font-size:44px;font-weight:900;white-space:nowrap">${esc(p.name)}</div>
      <div style="font-size:30px;font-weight:800;opacity:.85;white-space:nowrap;margin-top:6px">${esc(p.sub || '')}</div></div>`;
    const tm = p.teams || [], top = H - (HB[i] || 410) - LG - 50, tp = c01((q - .45) / .4);
    h += `<div class="row" style="position:absolute;left:${x}px;top:${top}px;width:${CW}px;justify-content:center;gap:${tm.length > 1 ? 10 : 0}px;align-items:flex-end;${pop(tp)}">` +
      tm.map((t, k) => { const tt = T(t.team || ''); return (k ? `<div style="font-size:34px;font-weight:900;color:${GRAY};padding-bottom:44px">vs</div>` : '') +
        `<div class="col" style="align-items:center;gap:4px"><div class="chip" style="width:${LG}px;height:${LG * .78}px">${LOGO[tt.code] ? `<img src="${LOGO[tt.code]}">` : ''}</div><div style="font-size:30px;font-weight:900;color:${TXT}">${esc(t.rank || '')}</div></div>`; }).join('') +
      (p.trophy ? `<div style="width:80px;height:80px;margin-left:12px;margin-bottom:30px"><svg viewBox="0 0 60 60" width="100%" height="100%"><path d="M18,8 H42 V24 C42,33 36,38 30,38 C24,38 18,33 18,24 Z" fill="#E8A100"/><path d="M18,12 H8 C8,22 12,26 18,26 M42,12 H52 C52,22 48,26 42,26" stroke="#E8A100" stroke-width="4" fill="none"/><rect x="26" y="38" width="8" height="10" fill="#E8A100"/><rect x="18" y="48" width="24" height="6" rx="2" fill="#E8A100"/></svg></div>` : '') + `</div>`;
    if (i < N - 1) { const qn = pk(s, st[i + 1].at, .8, 1), ap = c01((qn - .2) / .5), ax = x + CW - 40, ay = H - (HB[i] || 410) - 40;
      h += `<div style="position:absolute;left:${ax - 10}px;top:${ay - 128}px;width:${GAP + 100}px;opacity:${ap};text-align:center">
        <div style="font-size:28px;font-weight:900;color:${ACC};white-space:nowrap">이긴 팀 ↗</div>
        <svg width="${GAP + 100}" height="80" viewBox="0 0 134 80"><path d="M10,72 Q60,4 118,28" fill="none" stroke="${ACC}" stroke-width="7" stroke-linecap="round" stroke-dasharray="${(ap * 160).toFixed(0)} 220"/><path d="M106,14 L121,29 L102,37" fill="none" stroke="${ACC}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="${c01((ap - .7) / .3)}"/></svg></div>`; }
  });
  h += `</div>`;
  B(LR('', h));
};
/* rankstrip — 10/13 밤 사용자("한눈에 안 들어온다"): 서로 다른 기록(ERA·홈런·실책)을 같은 막대로 늘어놓으면 막대 길이가 뜻이 없다.
   한 줄 = 기록 이름·값 + 1위~10위 칸, 팀 로고가 자기 순위 칸으로 미끄러져 들어가 칸이 색으로 찬다(왼쪽 = 잘함, 오른쪽 = 못함).
   rows:[{k, v, rank, from, n(기본 10), zone:[a,b], zl, at}] · team · title · text/textAt */
SCENE.rankstrip = (lt, s) => {
  const rows = s.rows || [], t = T(s.team || ''), SW = 92, SG = 6, LW = 440, RH = rows.length > 4 ? 120 : 134, LG = rows.length > 4 ? 52 : 66;
  const cOf = (r, n) => r <= (n === 10 ? 3 : 1) ? GREEN : r > n - (n === 10 ? 3 : 1) ? RED : '#3B4A63';
  let h = s.title ? `<div class="title" style="font-size:54px;font-weight:900;text-align:center;margin-bottom:12px;${s._same ? '' : pop(seg(lt, 0, .4))}">${esc(s.title)}</div>` : '';
  h += `<div class="row" style="justify-content:center;gap:0;margin-bottom:4px"><div style="width:${LW}px"></div><div class="row" style="width:${10 * (SW + SG)}px;justify-content:space-between;font-size:28px;font-weight:900"><span style="color:${GREEN}">◀ 잘함</span><span style="color:${RED}">못함 ▶</span></div></div>`;
  rows.forEach((r, i) => {
    const n = r.n || 10, q = pk(s, r.at, 1.0, 1), e = eo(q), vis = c01(q * 5), zone = r.zone;
    const tgt = zone ? (zone[0] + zone[1]) / 2 : r.rank, st = r.from != null ? r.from : n + 1.6, pos = st + (tgt - st) * e;
    const col = zone ? RED : cOf(r.rank, n), land = c01((q - .8) / .2), TW = n * (SW + SG);
    let tr = `<div style="position:relative;width:${10 * (SW + SG)}px;height:${RH - 24}px">`;
    for (let k = 1; k <= n; k++) {
      const zc = k <= (n === 10 ? 3 : 1) ? '#E3F5EA' : k > n - (n === 10 ? 3 : 1) ? '#FCE7E8' : '#EEF1F6', x = (k - 1) * (SW + SG), on = !zone && k === r.rank, inZ = zone && k >= zone[0] && k <= zone[1];
      tr += `<div style="position:absolute;left:${x}px;top:8px;width:${SW}px;height:${RH - 40}px;border-radius:14px;background:${on ? mixC(zc, col, land) : inZ ? mixC(zc, '#F7B9BC', land) : zc};display:flex;align-items:flex-end;justify-content:center;padding-bottom:4px;box-sizing:border-box;font-size:28px;font-weight:900;color:${on && land > .5 ? '#fff' : '#9AA3B2'}">${k}위</div>`;
    }
    if (zone && r.zl) tr += `<div class="badge" style="position:absolute;left:${(zone[0] - 1) * (SW + SG)}px;top:-26px;width:${(zone[1] - zone[0] + 1) * (SW + SG) - SG}px;text-align:center;box-sizing:border-box;background:${RED};font-size:26px;padding:2px 0;display:flex;justify-content:center;${pop(land)}">${esc(r.zl)}</div>`;
    if (r.from != null) { const xa = (r.from - .5) * (SW + SG), xb = (pos - .5) * (SW + SG);
      tr += `<div style="position:absolute;left:${Math.min(xa, xb)}px;top:${(RH - 24) / 2 - 3}px;width:${Math.abs(xb - xa)}px;height:6px;background:${col};opacity:${vis * .5};border-radius:3px"></div>`; }
    const cx = (pos - .5) * (SW + SG) - SG / 2;
    if (!zone) tr += `<div class="chip" style="position:absolute;left:${(cx - LG / 2).toFixed(1)}px;top:${rows.length > 4 ? 10 : 14}px;width:${LG}px;height:${LG * .78}px;opacity:${vis};background:#fff;border-radius:14px;box-shadow:0 6px 16px rgba(18,22,31,.22);border:4px solid ${col}">${LOGO[t.code] ? `<img src="${LOGO[t.code]}">` : ''}</div>`;
    tr += `</div>`;
    h += `<div class="row" style="justify-content:center;gap:0;align-items:center;height:${RH}px;opacity:${vis}">
      <div class="col" style="width:${LW}px;gap:0;align-items:flex-start"><div style="font-size:36px;font-weight:900;color:${TXT};white-space:nowrap">${esc(r.k)}</div>
      <div class="num" style="font-size:54px;font-weight:900;color:${col};white-space:nowrap;line-height:1.05">${esc(r.v || '')}</div></div>${tr}</div>`;
  });
  if (s.text) h += `<div class="big gold" style="margin-top:14px;font-size:${s.size || 50}px;text-align:center;${pop(pk(s, s.textAt, .5, 1))}">${esc(s.text)}</div>`;
  B(LR('', `<div class="col" style="align-items:center;gap:0">${h}</div>`));
};
/* @@WDL1013 end */
