/* @@LOTTE1006 — 10/6 롯데 경우의 수 쇼츠 전용 모션그래픽(사용자 "이해가 되기 쉽게 모션그래픽·인포그래픽을 재미있고 간단명료하게").
   tools/inject_lotte_1006.py 가 template_issue.html 의 `const SUBS = EP.subs` 앞에 넣는다(고칠 땐 이 파일을 고치고 다시 주입).
   호흡 맞춤: render 가 s._t(절대 시각)를 넣어 준다 → bp(s,k) = 그 장면 첫 줄의 k번째 호흡이 시작된 뒤 진행도(0~1).
   장면: fate · ps5 · stand · ladder · sched6 · pepper · mission · tally · lose8 · h2h · finale */
const LT_ = n => T(n);
const TCOL = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
const LOGOI = (n, px, st = '') => `<img src="${LOGO[(T(n) || {}).code] || ''}" style="width:${px}px;height:${px}px;object-fit:contain;display:block;${st}">`;
function bp(s, k, d = .45, li) {
  const L = (EP.segT || [])[li == null ? s.startLine : li];
  if (k < 0) return 1; if (k >= 50) return 0;
  if (!L || s._t == null) return 1;
  const kk = Math.floor(k), t0 = L[Math.min(kk, L.length - 1)] + (k - kk) * .9;
  return c01((s._t - t0 + .08) / d);
}
const ap = (p, px = 30) => `opacity:${c01(p * 1.6)};transform:translateY(${(1 - eo(p)) * px}px)`;
const ppop = p => `opacity:${c01(p * 1.6)};transform:scale(${p <= 0 ? .5 : .5 + .5 * eb(p)})`;
const pill = (txt, bg, fs = 34, extra = '') => `<span style="display:inline-block;background:${bg};color:#fff;font-size:${fs}px;font-weight:900;padding:8px 24px;border-radius:999px;letter-spacing:-1px;white-space:nowrap;${extra}">${txt}</span>`;
/* 고춧가루 통(롯데 로고 붙음) */
function shaker(w, rot = 0, inv = false) {
  const h = w * 200 / 120, lg = LOGO[(T('롯데') || {}).code] || '';
  return `<svg width="${w}" height="${h}" viewBox="0 0 120 200" style="display:block;overflow:visible;transform:rotate(${rot}deg);transform-origin:50% 70%"><g transform="${inv ? 'rotate(180 60 100)' : ''}">
    <defs><linearGradient id="shk" x1="0" x2="1"><stop offset="0" stop-color="#C81E2B"/><stop offset=".45" stop-color="#F0444C"/><stop offset="1" stop-color="#B3121F"/></linearGradient></defs>
    <rect x="22" y="6" width="76" height="40" rx="12" fill="#12161F"/>
    ${[[42, 18], [60, 14], [78, 18], [51, 30], [69, 30]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="4.2" fill="#F4F6FA"/>`).join('')}
    <rect x="30" y="44" width="60" height="12" fill="#2A303C"/>
    <rect x="12" y="54" width="96" height="140" rx="26" fill="url(#shk)"/>
    <rect x="24" y="64" width="12" height="110" rx="6" fill="#fff" opacity=".22"/>
    <circle cx="60" cy="122" r="34" fill="#fff"/></g>
    ${lg ? `<image href="${lg}" x="32" y="${inv ? 50 : 94}" width="56" height="56" preserveAspectRatio="xMidYMid meet"/>` : ''}
  </svg>`;
}
/* 가루 알갱이: (x0,y0) 에서 targets 쪽으로 떨어짐. 시각 t(초) 기준 반복 */
function flakes(t, x0, y0, targets, n = 26, on = 1) {
  if (on <= 0) return '';
  let h = '';
  for (let i = 0; i < n; i++) {
    const per = 1.1, ph = ((t + i * per / n) % per) / per, tg = targets[i % targets.length];
    const jx = ((i * 37) % 23 - 11) * 3, jy = ((i * 53) % 17 - 8) * 2;
    const x = x0 + (tg[0] + jx - x0) * ph, y = y0 + (tg[1] + jy - y0) * ph + 0 * ph;
    const r = 5 + (i % 3) * 2;
    h += `<div style="position:absolute;left:${x.toFixed(1)}px;top:${y.toFixed(1)}px;width:${r}px;height:${r}px;border-radius:${i % 2 ? 2 : r}px;background:${i % 4 ? '#E5484D' : '#B3121F'};opacity:${(Math.sin(Math.PI * ph) * on).toFixed(2)};transform:rotate(${i * 40}deg)"></div>`;
  }
  return h;
}
const wob = (t, k = 1) => Math.sin(t * 9 + k) * 4;

/* 0 — 3·4·5위 받침대 위 세 팀이 자리를 바꾸고, 아래 롯데 고춧가루 통 */
SCENE.fate = (lt, s) => {
  const W = 900, slotX = [W / 2 - 290, W / 2, W / 2 + 290], ped = [{ r: '3위', h: 230 }, { r: '4위', h: 180 }, { r: '5위', h: 140 }];
  const teams = s.teams || ['KIA', 'LG', '두산'];
  const P = [[0, 1, 2], [1, 2, 0], [2, 0, 1], [1, 0, 2], [0, 2, 1], [2, 1, 0]];
  const ph = Math.max(0, lt - .5) / .75, f = Math.floor(ph), fr = eo(c01((ph - f) / .55));
  const a = P[f % P.length], b = P[(f + 1) % P.length];
  let h = `<div style="position:relative;width:${W}px;height:800px">`;
  h += `<div style="position:absolute;left:0;right:0;top:0;text-align:center;${pop(seg(lt, 0, .4))}">${pill('3·4·5위 아직 몰라요', '#12161F', 40)}</div>`;
  const base = 520;
  ped.forEach((p, i) => {
    h += `<div style="position:absolute;left:${slotX[i] - 120}px;top:${base - p.h}px;width:240px;height:${p.h}px;border-radius:22px 22px 0 0;background:linear-gradient(180deg,#FFFFFF,#E4E9F1);border:3px solid ${LINE};display:flex;align-items:flex-start;justify-content:center;padding-top:22px;${ap(seg(lt, .05 + i * .08, .4), 40)}">
      <span style="font-size:64px;font-weight:900;letter-spacing:-2px;color:${i ? TXT : 'var(--acc)'}">${p.r}</span></div>`;
  });
  teams.forEach((tm, i) => {
    const x = slotX[a[i]] + (slotX[b[i]] - slotX[a[i]]) * fr, yTop = base - ped[a[i]].h + (ped[a[i]].h - ped[b[i]].h) * fr;
    const y = yTop - 170 - Math.sin(Math.PI * fr) * 70;
    h += `<div style="position:absolute;left:${x - 80}px;top:${y}px;width:160px;height:160px;border-radius:40px;background:#fff;border:4px solid ${TCOL(tm)};box-shadow:0 12px 30px rgba(18,22,31,.14);display:flex;align-items:center;justify-content:center;${ppop(seg(lt, .2 + i * .1, .5))}">${LOGOI(tm, 124)}
      <div style="position:absolute;right:-18px;top:-22px;width:56px;height:56px;border-radius:50%;background:#12161F;color:#fff;font-size:38px;font-weight:900;display:flex;align-items:center;justify-content:center">?</div></div>`;
  });
  h += `<div style="position:absolute;left:0;right:0;top:${base}px;height:8px;background:#12161F;border-radius:4px"></div>`;
  /* 아래: 롯데 로고 + 흔드는 고춧가루 통 */
  const sp = seg(lt, .5, .5), sh = Math.sin(lt * 10) * 10 * c01((lt - .9) * 3);
  h += `<div style="position:absolute;left:${W / 2 - 290}px;top:572px;width:580px;height:220px;display:flex;align-items:center;justify-content:center;gap:34px;${ap(sp, 40)}">
     <div style="width:200px;height:200px;border-radius:48px;background:#fff;border:4px solid ${TCOL('롯데')};display:flex;align-items:center;justify-content:center;box-shadow:0 14px 34px rgba(18,22,31,.14)">${LOGOI('롯데', 160)}</div>
     <div style="transform:translateY(${-10}px)">${shaker(120, -28 + sh)}</div></div>`;
  h += `<div style="position:absolute;left:0;top:0;width:${W}px;height:800px;pointer-events:none">${flakes(lt, W / 2 + 120, 560, slotX.map(x => [x, base - 260]), 22, c01((lt - 1.0) * 2))}</div>`;
  h += `</div>`;
  B(h);
};

/* 1 — 가을야구 5팀: 1·2위는 흐리게, 3·4·5위 칸은 점선 상자 + '미확정' */
SCENE.ps5 = (lt, s) => {
  const it = s.items || [];
  let h = `<div style="margin-bottom:70px;${pop(seg(lt, 0, .4))}">${pill('2026 가을야구 5팀', 'var(--acc)', 46)}</div><div class="row" style="gap:16px;align-items:flex-end;position:relative">`;
  it.forEach((x, i) => {
    const dim = !!x.dim, p = seg(lt, .1 + i * .12, .45);
    h += `<div class="col" style="width:164px;gap:12px;${ap(p, 50)};opacity:${dim ? .4 * c01(p * 1.6) : c01(p * 1.6)}">
      <div style="font-size:44px;font-weight:900;letter-spacing:-1px;color:${dim ? GRAY : TXT}">${esc(x.r)}</div>
      <div style="width:164px;height:164px;border-radius:36px;background:#fff;border:3px solid ${dim ? LINE : TCOL(x.team)};display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(18,22,31,.08);transform:rotate(${dim ? 0 : wob(lt, i) * .6}deg)">${LOGOI(x.team, 124)}</div>
      <div style="font-size:36px;font-weight:800;color:${dim ? GRAY : TXT};white-space:nowrap">${esc(x.nm || x.team)}</div></div>`;
  });
  h += `</div>`;
  const q = bp(s, 1);
  h += `<div style="position:relative;width:900px;height:250px;margin-top:-10px">
    <div style="position:absolute;left:${900 - 3 * 164 - 2 * 16 - 18}px;top:-298px;width:${3 * 164 + 2 * 16 + 36}px;height:338px;border:6px dashed ${RED};border-radius:34px;opacity:${c01(q * 1.6)}"></div>
    <div style="position:absolute;left:${900 - (3 * 164 + 2 * 16) / 2 - 190}px;top:58px;width:380px;text-align:center;${ppop(q)}">${pill('아직 미확정', RED, 58, 'padding:14px 40px;transform:rotate(-4deg)')}</div></div>`;
  B(h);
};

/* 2·3 — 현재 성적 줄 + 사이 '○경기 차' 알약. rows:[{team,r,w,l,at}] gaps:[{label,at}] (cont 면 앞 줄 그대로) */
SCENE.stand = (lt, s) => {
  const rows = s.rows || [], gaps = s.gaps || [], RH = 170, GH = 74;
  let h = `<div style="position:relative;width:900px;height:${rows.length * RH + (rows.length - 1) * GH}px">`;
  rows.forEach((r, i) => {
    const p = r.at == null ? 1 : r.at < 0 ? 1 : bp(s, r.at), top = i * (RH + GH);
    if (p <= 0) return;
    h += `<div class="pane" style="position:absolute;left:0;top:${top}px;width:900px;height:${RH}px;border-radius:34px;display:flex;align-items:center;padding:0 34px;gap:26px;${r.hi ? `border-color:${TCOL(r.team)};` : ''}${r.at != null && r.at >= 0 ? ap(p, 40) : ''}">
      <div style="width:104px;font-size:56px;font-weight:900;color:${TCOL(r.team)};letter-spacing:-2px">${esc(r.r)}</div>
      ${LOGOI(r.team, 116)}
      <div style="font-size:54px;font-weight:900;letter-spacing:-2px;width:140px;text-align:left">${esc(T(r.team).nm || r.team)}</div>
      <div class="num" style="flex:1;text-align:right;font-size:76px;font-weight:900;letter-spacing:-3px"><span>${r.w}</span><span style="font-size:44px;color:${GRAY}">승 </span><span>${r.l}</span><span style="font-size:44px;color:${GRAY}">패</span></div></div>`;
  });
  gaps.forEach((g, i) => {
    const p = g.at < 0 ? 1 : bp(s, g.at), top = (i + 1) * RH + i * GH;
    if (p <= 0) return;
    h += `<div style="position:absolute;left:0;right:0;top:${top}px;height:${GH}px;display:flex;align-items:center;justify-content:center;gap:16px">
      <div style="position:absolute;left:450px;top:-28px;width:6px;height:${GH + 56}px;margin-left:-3px;background:#12161F;border-radius:3px;opacity:${c01(p * 1.6)}"></div>
      <div style="position:relative;${ppop(p)}">${pill(esc(g.label), g.color || '#12161F', 44, 'padding:10px 34px')}</div></div>`;
  });
  h += `</div>`;
  B(h);
};

/* 4 — 순위별 가는 길: 3위 준PO 직행 / 4위 1승 안고 / 5위 2승 필요 */
SCENE.ladder = (lt, s) => {
  const rows = [
    { r: '3위', to: '준플레이오프 직행', tag: '바로 진출', c: 'var(--acc)', at: 0 },
    { r: '4위', to: '와일드카드', tag: '1승 안고 시작', c: GREEN, at: 1, balls: [1, 0] },
    { r: '5위', to: '와일드카드', tag: '두 번 다 이겨야', c: RED, at: 2, balls: [0, 0] }];
  let h = `<div class="col" style="gap:34px;width:900px">`;
  rows.forEach((x, i) => {
    const p = bp(s, x.at), ar = eo(seg(p * .6, 0, .5));
    h += `<div class="row" style="gap:22px;width:900px;justify-content:flex-start;${ap(p, 40)}">
      <div style="width:150px;height:150px;border-radius:36px;background:${x.c};color:#fff;font-size:62px;font-weight:900;display:flex;align-items:center;justify-content:center;flex:0 0 auto">${x.r}</div>
      <svg width="110" height="60" viewBox="0 0 110 60" style="flex:0 0 auto"><path d="M4 30 H${4 + 80 * ar}" stroke="#12161F" stroke-width="10" stroke-linecap="round"/>${ar > .95 ? '<path d="M78 12 L102 30 L78 48" fill="none" stroke="#12161F" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>' : ''}</svg>
      <div class="pane" style="flex:1;border-radius:30px;padding:20px 26px;display:flex;flex-direction:column;align-items:flex-start;gap:10px;border-color:${x.c}">
        <div style="font-size:50px;font-weight:900;letter-spacing:-2px">${x.to}</div>
        <div class="row" style="gap:14px">${pill(x.tag, x.c, 34)}${x.balls ? x.balls.map((b, j) => `<div style="width:50px;height:50px;border-radius:50%;border:5px solid ${b ? GREEN : RED};background:${b ? GREEN : '#fff'};color:#fff;font-size:28px;font-weight:900;display:flex;align-items:center;justify-content:center;${ppop(seg(p * 1.2, .3 + j * .15, .4))}">${b ? '승' : ''}</div>`).join('') : ''}</div></div></div>`;
  });
  h += `</div>`;
  B(h);
};

/* 5 — 롯데 남은 6경기 카드: 날짜 순 → (호흡 groupAt) 팀별로 두 장씩 모임 */
SCENE.sched6 = (lt, s) => {
  const G = s.games || [], CW = 272, CH = 214, GX = 26, GY = 26, X0 = (900 - 3 * CW - 2 * GX) / 2, Y0 = 250;
  const ord = s.groups || ['두산', 'KIA', 'LG'];
  const g = eo(bp(s, s.groupAt ?? 2, .8));
  let h = `<div style="position:relative;width:900px;height:${Y0 + 2 * CH + GY + 110}px">`;
  const p0 = bp(s, 0);
  h += `<div class="row" style="position:absolute;left:0;right:0;top:0;gap:26px;${ap(p0, 30)}">
    <div style="width:190px;height:190px;border-radius:44px;background:#fff;border:4px solid ${TCOL('롯데')};display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(18,22,31,.12);position:relative">${LOGOI('롯데', 150, 'filter:grayscale(.3)')}</div>
    <div class="col" style="align-items:flex-start;gap:10px"><div style="font-size:64px;font-weight:900;letter-spacing:-2px">${esc(s.head || '8위 롯데')}</div>
      <div style="${ppop(seg(lt, .5, .45))}">${pill(esc(s.badge || '가을야구 탈락 확정'), RED, 40, 'transform:rotate(-3deg)')}</div></div></div>`;
  const cnt = {};
  G.forEach((x, i) => {
    const k = ord.indexOf(x.vs), j = (cnt[x.vs] = (cnt[x.vs] || 0) + 1) - 1;
    const c1 = i % 3, r1 = Math.floor(i / 3), c2 = k, r2 = j;
    const X = X0 + (c1 + (c2 - c1) * g) * (CW + GX), Y = Y0 + (r1 + (r2 - r1) * g) * (CH + GY) - Math.sin(Math.PI * g) * 30 * (c1 !== c2 ? 1 : 0);
    const p = bp(s, s.cardsAt ?? 1, .35 + i * .12);
    if (p <= 0) return;
    h += `<div class="pane" style="position:absolute;left:${X}px;top:${Y}px;width:${CW}px;height:${CH}px;border-radius:30px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;border-color:${g > .5 ? TCOL(x.vs) : LINE};border-width:${g > .5 ? 5 : 3}px;${ppop(c01(p * (1 + i * .25)))}">
      <div style="font-size:36px;font-weight:900;color:${GRAY};letter-spacing:-1px">${esc(x.d)}</div>${LOGOI(x.vs, 104)}
      <div style="font-size:30px;font-weight:800;color:${GRAY}">${esc(x.place)}</div></div>`;
  });
  ord.forEach((tm, k) => {
    const p = c01((g - .85) / .15);
    const nG = G.filter(x => x.vs === tm).length;
    h += `<div style="position:absolute;left:${X0 + k * (CW + GX)}px;top:${Y0 + 2 * CH + GY + 20}px;width:${CW}px;text-align:center;${ppop(p)}">${pill('× ' + nG + '번', TCOL(tm), 44)}</div>`;
  });
  h += `</div>`;
  B(h);
};

/* 6 — 고춧가루: 통을 흔들면 가루가 세 팀 위로, 맞은 로고가 움찔 */
SCENE.pepper = (lt, s) => {
  const W = 900, tms = s.teams || ['두산', 'KIA', 'LG'], xs = [W / 2 - 280, W / 2, W / 2 + 280], ty = 470;
  const shake = Math.sin(lt * 12) * 14 * c01((lt - .4) * 3), on = c01((lt - .6) * 2);
  let h = `<div style="position:relative;width:${W}px;height:800px">`;
  h += `<div style="position:absolute;left:${W / 2 - 75}px;top:0;${ap(seg(lt, 0, .45), -40)}">${shaker(150, shake, true)}</div>`;
  h += flakes(lt, W / 2 - 6, 70, xs.map(x => [x, ty + 20]), 34, on);
  tms.forEach((tm, i) => {
    const hit = on * (0.5 + 0.5 * Math.sin(lt * 15 + i * 2));
    h += `<div style="position:absolute;left:${xs[i] - 95}px;top:${ty}px;width:190px;height:190px;border-radius:44px;background:#fff;border:4px solid ${TCOL(tm)};display:flex;align-items:center;justify-content:center;box-shadow:0 12px 30px rgba(18,22,31,.12);transform:translateX(${hit * 6 - 3}px) rotate(${(hit - .5) * 6}deg);${''}">${LOGOI(tm, 148)}
      <div style="position:absolute;right:-16px;top:-30px;font-size:58px;${EMOJI};opacity:${on}">💦</div></div>`;
  });
  const q = bp(s, 1);
  h += `<div style="position:absolute;left:0;right:0;top:690px;text-align:center;${ppop(q)}">${pill('고춧가루 = 탈락 팀이 순위 싸움 팀을 잡는 것', '#12161F', 38, 'padding:14px 30px')}</div>`;
  h += `</div>`;
  B(h);
};

/* 7 — 세 팀 미션 카드 */
SCENE.mission = (lt, s) => {
  const it = s.items || [];
  let h = `<div style="margin-bottom:44px;${pop(seg(lt, 0, .4))}">${pill('세 팀의 미션', '#12161F', 52, 'padding:12px 40px')}</div><div class="row" style="gap:24px">`;
  it.forEach((x, i) => {
    const p = seg(lt, .3 + i * .3, .5), fl = Math.cos(Math.PI * (1 - eo(p)));
    h += `<div class="pane col" style="width:284px;height:430px;border-radius:34px;gap:22px;border-color:${TCOL(x.team)};border-width:5px;opacity:${c01(p * 2)};transform:perspective(900px) rotateY(${(1 - eo(p)) * 90}deg)">
      ${LOGOI(x.team, 150)}<div style="font-size:52px;font-weight:900;letter-spacing:-2px;color:${TCOL(x.team)};line-height:1.15;text-align:center">${br(x.goal)}</div></div>`;
  });
  h += `</div>`;
  B(h);
};

/* 8~13 — 남은 경기 칸(동그라미). head:{team,txt}, rule:{txt,at}, rows:[{team,n,slots:[..],vs:[..],at,count,countAt}], result:{txt,team,at}
   칸 종류: 'w' 승(팀색) / 'l' 패(회색 X) / 'R' 롯데에 패(롯데 도장) / 'm' 아직(점선, '많아야' 칸) / '' 빈 칸.  vs 가 있으면 칸 아래 상대 로고(롯데전은 빨간 테). */
SCENE.tally = (lt, s) => {
  const rows = s.rows || [], same = s.cont && s._same, D_ = 80, GAP = 10;
  let h = '';
  if (s.head) {
    const hp = same ? 1 : seg(lt, 0, .4);
    h += `<div class="row" style="gap:18px;margin-bottom:26px;${pop(hp)}">${s.head.team ? LOGOI(s.head.team, 84) : ''}<span style="font-size:56px;font-weight:900;letter-spacing:-2px;color:${s.head.team ? TCOL(s.head.team) : TXT}">${esc(s.head.txt)}</span></div>`;
  }
  if (s.rule) {
    const rp = bp(s, s.rule.at || 0);
    h += `<div style="margin-bottom:34px;min-height:76px;${ppop(rp)}">${pill(esc(s.rule.txt), '#12161F', 44, 'padding:12px 34px')}</div>`;
  }
  h += `<div class="col" style="gap:${s.vsRow ? 26 : 36}px;width:900px">`;
  rows.forEach((r, ri) => {
    const n = r.n || 0, sl = r.slots || [];
    h += `<div class="pane" style="width:900px;border-radius:32px;padding:20px 24px;display:flex;align-items:center;gap:18px;${same ? '' : ap(seg(lt, .15 + ri * .15, .45), 30)}">
      <div class="col" style="width:110px;gap:4px;flex:0 0 auto">${LOGOI(r.team, 86)}<div style="font-size:22px;font-weight:800;color:${GRAY};white-space:nowrap">남은 ${n}경기</div></div>
      <div class="row" style="gap:${GAP}px;flex:1;justify-content:flex-start">`;
    for (let i = 0; i < n; i++) {
      const k = sl[i] || '', at = Array.isArray(r.at) ? r.at[i] : r.at, p = k ? (at == null ? 1 : bp(s, at + i * 0.0, .35 + i * .1)) : 0;
      const pp = k ? c01(p * (1 + i * .3)) : 0;
      let face = `<div style="position:absolute;inset:0;border-radius:50%;border:5px solid ${LINE};background:#fff"></div>`;
      if (k === 'lw') face += `<div style="position:absolute;inset:0;border-radius:50%;background:#C9D0DB;display:flex;align-items:center;justify-content:center;color:#fff;font-size:34px;font-weight:900">패</div>`;   // 10/7: 패 → 승 바뀜
      if (k === 'lw' && pp > 0) face += `<div style="position:absolute;inset:0;border-radius:50%;background:${TCOL(r.team)};display:flex;align-items:center;justify-content:center;color:#fff;font-size:34px;font-weight:900;${ppop(pp)}">승</div>`;
      if (k === 'w' && pp > 0) face += `<div style="position:absolute;inset:0;border-radius:50%;background:${TCOL(r.team)};display:flex;align-items:center;justify-content:center;color:#fff;font-size:34px;font-weight:900;${ppop(pp)}">승</div>`;
      if (k === 'l' && pp > 0) face += `<div style="position:absolute;inset:0;border-radius:50%;background:#C9D0DB;display:flex;align-items:center;justify-content:center;color:#fff;font-size:34px;font-weight:900;${ppop(pp)}">패</div>`;
      if (k === 'R' && pp > 0) face += `<div style="position:absolute;inset:0;border-radius:50%;background:#C9D0DB;border:6px solid ${RED};display:flex;align-items:center;justify-content:center;color:#fff;font-size:34px;font-weight:900;${ppop(pp)}">패<div style="position:absolute;right:-14px;top:-14px;width:42px;height:42px;border-radius:50%;background:#fff;border:3px solid ${RED};display:flex;align-items:center;justify-content:center">${LOGOI('롯데', 32)}</div></div>`;
      if (k === 'm' && pp > 0) face += `<div style="position:absolute;inset:0;border-radius:50%;border:5px dashed ${TCOL(r.team)};background:${TCOL(r.team)}18;opacity:${c01(pp * 1.6)}"></div>`;
      const vs = (r.vs || [])[i];
      h += `<div class="col" style="gap:6px;flex:0 0 auto"><div style="position:relative;width:${D_}px;height:${D_}px">${face}</div>
        ${s.vsRow && vs ? `<div style="width:56px;height:56px;border-radius:14px;background:#fff;border:${vs === '롯데' ? `4px solid ${RED}` : `2px solid ${LINE}`};display:flex;align-items:center;justify-content:center">${LOGOI(vs, 42)}</div>` : ''}</div>`;
    }
    h += `</div>`;
    if (Array.isArray(r.count)) {   // 10/7: [{t, at}] — 호흡에 맞춰 숫자가 바뀜(마지막으로 시작한 것)
      let cur = null; r.count.forEach(c => { const q = bp(s, c.at, .5); if (q > 0) cur = { t: c.t, q }; });
      h += `<div style="width:150px;text-align:center;font-size:40px;line-height:1.1;font-weight:900;letter-spacing:-2px;color:${r.countColor || TCOL(r.team)};white-space:nowrap;flex:0 0 auto;${cur ? ppop(cur.q) : 'opacity:0'}">${cur ? br(cur.t) : ''}</div>`;
    } else if (r.count) { const cp = bp(s, r.countAt ?? (Array.isArray(r.at) ? Math.max(...r.at.filter(x => x != null)) : (r.at ?? 0)), .5, null);
      h += `<div style="width:150px;text-align:center;font-size:${/\n/.test(r.count) ? 40 : 54}px;line-height:1.1;font-weight:900;letter-spacing:-2px;color:${r.countColor || TCOL(r.team)};white-space:nowrap;flex:0 0 auto;${ppop(cp)}">${br(r.count)}</div>`; }
    else h += `<div style="width:150px;flex:0 0 auto"></div>`;
    h += `</div>`;
  });
  h += `</div>`;
  if (Array.isArray(s.result)) {   // 10/7: 결과 알약이 호흡마다 바뀜
    let cur = null; s.result.forEach(x => { const q = bp(s, x.at, .5); if (q > 0) cur = { x, q }; });
    h += `<div style="margin-top:34px;min-height:96px;${cur ? ppop(cur.q) : 'opacity:0'}">${cur ? pill(esc(cur.x.txt), cur.x.team ? TCOL(cur.x.team) : GREEN, 58, 'padding:14px 44px;box-shadow:0 14px 34px rgba(18,22,31,.2)') : ''}</div>`;
  } else if (s.result) {
    const rp = bp(s, s.result.at, .5);
    h += `<div style="margin-top:34px;min-height:96px;${ppop(rp)}">${pill(esc(s.result.txt), s.result.team ? TCOL(s.result.team) : GREEN, 58, 'padding:14px 44px;box-shadow:0 14px 34px rgba(18,22,31,.2)')}</div>`;
  } else if (s.resultSpace) h += `<div style="margin-top:34px;min-height:96px"></div>`;   // 다음 줄 결과 자리 미리 비움(표가 안 밀리게)
  if (s.note !== false) h += `<div style="margin-top:14px;font-size:26px;font-weight:700;color:${GRAY}">※ 무승부 없을 때 기준</div>`;
  B(h);
};

/* 14 — LG 8연패 칸 + 사직 롯데 2연전 */
SCENE.lose8 = (lt, s) => {
  let h = `<div class="row" style="gap:20px;margin-bottom:30px;${pop(seg(lt, 0, .4))}">${LOGOI('LG', 110)}<span style="font-size:76px;font-weight:900;letter-spacing:-3px;color:${TCOL('LG')}">지금 8연패</span></div>`;
  h += `<div class="row" style="gap:14px;margin-bottom:44px">`;
  for (let i = 0; i < 8; i++) { const p = seg(lt, .25 + i * .1, .35);
    h += `<div style="width:92px;height:92px;border-radius:50%;background:${RED};color:#fff;font-size:42px;font-weight:900;display:flex;align-items:center;justify-content:center;${ppop(p)}">패</div>`; }
  h += `</div><div class="row" style="gap:26px">`;
  (s.games || []).forEach((g, i) => {
    const p = bp(s, s.gamesAt ?? 1, .45 + i * .15);
    h += `<div class="pane col" style="width:420px;border-radius:32px;padding:24px 18px;gap:12px;border-color:${TCOL('롯데')};border-width:5px;${ppop(c01(p * (1 + i * .5)))}">
      <div style="font-size:44px;font-weight:900;letter-spacing:-1px">${esc(g.d)}</div>
      <div class="row" style="gap:18px">${LOGOI('LG', 100)}<span style="font-size:44px;font-weight:900;color:${GRAY}">vs</span>${LOGOI('롯데', 100)}</div>
      <div style="font-size:34px;font-weight:800;color:${GRAY}">${esc(g.place)}</div></div>`;
  });
  h += `</div>`;
  B(h);
};

/* 15 — 롯데 vs 세 팀 상대전적 막대(승 초록·무 회색·패 빨강) + 합계 */
SCENE.h2h = (lt, s) => {
  const rows = s.rows || [], BW = 520;
  let h = `<div style="margin-bottom:34px;${pop(seg(lt, 0, .4))}" class="row">${LOGOI('롯데', 90)}<span style="font-size:52px;font-weight:900;letter-spacing:-2px;margin-left:16px">올해 이 세 팀 상대 전적</span></div><div class="col" style="gap:22px">`;
  rows.forEach((r, i) => {
    const p = eo(seg(lt, .3 + i * .3, .6)), tot = r.w + r.d + r.l;
    h += `<div class="pane row" style="width:900px;border-radius:28px;padding:16px 24px;gap:20px;justify-content:flex-start;${ap(seg(lt, .2 + i * .3, .4), 30)}">
      <div class="row" style="gap:6px;width:110px;flex:0 0 auto"><span style="font-size:30px;font-weight:800;color:${GRAY}">vs</span>${LOGOI(r.team, 70)}</div>
      <div style="width:${BW}px;height:56px;border-radius:14px;background:#E9EDF3;overflow:hidden;display:flex;flex:0 0 auto">
        <div style="width:${BW * r.w / tot * p}px;background:${GREEN}"></div><div style="width:${BW * r.d / tot * p}px;background:#A9B2C0"></div><div style="width:${BW * r.l / tot * p}px;background:${RED}"></div></div>
      <div class="num" style="flex:1;text-align:right;font-size:38px;font-weight:900;white-space:nowrap;opacity:${c01(p * 1.5)}">${r.w}승${r.d ? ` ${r.d}무` : ''} ${r.l}패</div></div>`;
  });
  h += `</div>`;
  const t = s.total || {}, q = bp(s, s.totalAt ?? 1, .5);
  h += `<div style="margin-top:40px;${ppop(q)}" class="row"><span style="font-size:44px;font-weight:900;color:${GRAY};margin-right:18px">합계</span><span class="num" style="font-size:96px;font-weight:900;letter-spacing:-4px"><span style="color:${GREEN}">${t.w}승</span> <span style="color:${GRAY}">${t.d}무</span> <span style="color:${RED}">${t.l}패</span></span></div>`;
  B(h);
};

/* 16 — 마지막 날 두 구장 */
SCENE.finale = (lt, s) => {
  let h = `<div style="margin-bottom:40px;${ppop(seg(lt, 0, .45))}">${pill(esc(s.title || ''), RED, 56, 'padding:14px 44px')}</div><div class="col" style="gap:30px">`;
  (s.games || []).forEach((g, i) => {
    const p = bp(s, g.at ?? i + 1, .5);
    h += `<div class="pane row" style="width:860px;border-radius:36px;padding:26px 30px;gap:30px;${ap(p, 40)}">
      <div style="width:150px;font-size:54px;font-weight:900;letter-spacing:-2px">${esc(g.place)}</div>
      ${LOGOI(g.a, 150)}<span style="font-size:56px;font-weight:900;color:${GRAY}">vs</span>${LOGOI(g.b, 150)}</div>`;
  });
  h += `</div>`;
  B(h);
};
/* 17 — 마지막 질문: 고춧가루 통이 세 팀 위를 오가며 뿌리고, 아래 세 팀 카드 */
SCENE.q3 = (lt, s) => {
  const W = 900, tms = s.teams || ['KIA', 'LG', '두산'], xs = [W / 2 - 300, W / 2, W / 2 + 300];
  const sx = W / 2 + Math.sin(lt * 1.6) * 260, on = c01((lt - .5) * 2);
  let h = `<div style="position:relative;width:${W}px;height:810px">`;
  h += `<div style="position:absolute;left:${sx - 55}px;top:0;${ap(seg(lt, 0, .4), -30)}">${shaker(110, Math.sin(lt * 12) * 10, true)}</div>`;
  h += flakes(lt, sx, 160, xs.map(x => [x, 520]), 30, on);
  h += `<div style="position:absolute;left:0;right:0;top:230px;text-align:center;font-size:${s.size || 84}px;font-weight:900;letter-spacing:-3px;line-height:1.15;${pop(seg(lt, .1, .5))}">${br(s.text || '')}</div>`;
  tms.forEach((tm, i) => {
    const p = seg(lt, .35 + i * .18, .5);
    h += `<div class="pane col" style="position:absolute;left:${xs[i] - 135}px;top:470px;width:270px;height:320px;border-radius:36px;gap:16px;border-color:${TCOL(tm)};border-width:5px;${ap(p, 50)}">
      ${LOGOI(tm, 170)}<div style="font-size:52px;font-weight:900;letter-spacing:-2px;color:${TCOL(tm)}">${esc(T(tm).nm || tm)}</div></div>`;
  });
  h += `</div>`;
  B(h);
};
/* ── 10/7 리뷰·김도영 43호 편 추가 ── */
/* crown: 두 팀 카드 위 '유리' 알약이 from 팀에서 to 팀으로 넘어감(moveAt 초). {title, teams:[a,b], recs:[..], label, moveAt} */
SCENE.crown = (lt, s) => {
  const tm = s.teams || ['KIA', 'LG'], X = [190, 710], mv = eo(seg(lt, s.moveAt ?? 1.0, .8));
  let h = `<div style="position:relative;width:900px;height:780px">`;
  h += `<div style="position:absolute;left:0;right:0;top:0;text-align:center;${pop(seg(lt, 0, .4))}">${pill(esc(s.title || '3위 싸움 조건'), '#12161F', 46, 'padding:12px 36px')}</div>`;
  tm.forEach((t, i) => {
    const on = i === 0 ? 1 - mv : mv;
    h += `<div class="pane col" style="position:absolute;left:${X[i] - 190}px;top:250px;width:380px;height:470px;border-radius:40px;gap:20px;border-color:${on > .5 ? TCOL(t) : LINE};border-width:${on > .5 ? 7 : 3}px;transform:scale(${.94 + .08 * on});${ap(seg(lt, .1 + i * .15, .45), 40)}">
      ${LOGOI(t, 210)}<div style="font-size:62px;font-weight:900;letter-spacing:-2px">${esc(T(t).nm || t)}</div>
      ${(s.recs || [])[i] ? `<div class="num" style="font-size:40px;font-weight:800;color:${GRAY}">${esc(s.recs[i])}</div>` : ''}</div>`;
  });
  const x = X[0] + (X[1] - X[0]) * mv, y = 130 - Math.sin(Math.PI * mv) * 70;
  h += `<div style="position:absolute;left:${x - 220}px;top:${y}px;width:440px;text-align:center;${ppop(seg(lt, .4, .45))}">${pill(esc(s.label || '3위 유리'), RED, 50, 'padding:12px 30px;box-shadow:0 14px 30px rgba(229,72,77,.35)')}
    <div style="width:0;height:0;margin:6px auto 0;border-left:22px solid transparent;border-right:22px solid transparent;border-top:28px solid ${RED}"></div></div>`;
  h += `</div>`;
  B(h);
};
/* results: 경기 결과 줄. rows:[{l,ls,r,rs,tag,tagColor,at}], streak:{team,n,label,at} */
SCENE.results = (lt, s) => {
  const rows = s.rows || [];
  let h = s.title ? `<div style="margin-bottom:34px;${pop(seg(lt, 0, .4))}">${pill(esc(s.title), '#12161F', 44)}</div>` : '';
  h += `<div class="col" style="gap:30px">`;
  rows.forEach((r, i) => {
    const p = r.at == null ? seg(lt, .1 + i * .3, .45) : bp(s, r.at), lw = r.ls > r.rs;
    h += `<div class="col" style="gap:14px;${ap(p, 40)}"><div class="pane row" style="width:880px;height:190px;border-radius:36px;gap:26px">
      ${LOGOI(r.l, 130, lw ? '' : 'opacity:.55')}<div class="num" style="font-size:110px;font-weight:900;letter-spacing:-3px"><span style="color:${lw ? TCOL(r.l) : '#AAB2BF'}">${r.ls}</span><span style="color:${GRAY};margin:0 22px">:</span><span style="color:${lw ? '#AAB2BF' : TCOL(r.r)}">${r.rs}</span></div>${LOGOI(r.r, 130, lw ? 'opacity:.55' : '')}</div>
      ${r.tag ? `<div style="${ppop(c01(p * 1.4 - .3))}">${pill(esc(r.tag), r.tagColor || (lw ? TCOL(r.l) : TCOL(r.r)), 42)}</div>` : ''}</div>`;
  });
  h += `</div>`;
  if (s.streak) { const st = s.streak, q = bp(s, st.at ?? 1);
    h += `<div class="row" style="gap:16px;margin-top:40px;${ap(q, 30)}">${LOGOI(st.team, 90)}${Array.from({ length: st.n }, (_, k) => `<div style="width:90px;height:90px;border-radius:50%;background:${GREEN};color:#fff;font-size:42px;font-weight:900;display:flex;align-items:center;justify-content:center;${ppop(c01(q * 2 - k * .3))}">승</div>`).join('')}<span style="font-size:60px;font-weight:900;color:${GREEN};margin-left:10px">${esc(st.label || '')}</span></div>`; }
  B(h);
};
/* pct2: 두 팀 승률 나란히 + 차이. teams:[{team,pct,rec}], diff, diffAt */
SCENE.pct2 = (lt, s) => {
  const it = s.teams || [];
  let h = `<div style="margin-bottom:36px;${pop(seg(lt, 0, .4))}">${pill(esc(s.title || '승률'), '#12161F', 46)}</div><div class="row" style="gap:30px">`;
  it.forEach((x, i) => {
    h += `<div class="pane col" style="width:420px;border-radius:36px;padding:34px 10px;gap:14px;border-color:${x.hi ? TCOL(x.team) : LINE};border-width:${x.hi ? 6 : 3}px;${ap(seg(lt, .15 + i * .2, .45), 40)}">
      ${LOGOI(x.team, 130)}<div class="num" style="font-size:104px;font-weight:900;letter-spacing:-4px;color:${x.hi ? TCOL(x.team) : TXT}">${esc(x.pct)}</div>
      <div class="num" style="font-size:36px;font-weight:800;color:${GRAY}">${esc(x.rec || '')}</div></div>`;
  });
  h += `</div>`;
  const q = bp(s, s.diffAt ?? 1);
  h += `<div style="margin-top:44px;${ppop(q)}">${pill('차이 ' + esc(s.diff || ''), RED, 64, 'padding:16px 46px')}</div>`;
  B(h);
};
/* q3p: 큰 질문 + 사진 카드 세 장. {text, items:[{img,label,team,focus,hi}]} */
SCENE.q3p = (lt, s) => {
  const it = s.items || [];
  let h = `<div class="mega" style="font-size:${s.size || 96}px;margin-bottom:40px;${pop(seg(lt, 0, .5))}">${br(s.text || '')}</div><div class="row" style="gap:22px;align-items:stretch">`;
  it.forEach((x, i) => {
    const src = photoSrc(x.img), p = seg(lt, .25 + i * .2, .5);
    h += `<div class="pane col" style="width:285px;border-radius:30px;padding:16px 14px 22px;gap:14px;${x.hi ? `border-color:${TCOL(x.team || 'KIA')};border-width:6px;` : ''}${ap(p, 50)}">
      <div style="width:255px;height:300px;border-radius:22px;overflow:hidden;background:#E9EDF3">${src ? `<img src="${src}" style="width:100%;height:100%;object-fit:cover;object-position:${esc(x.focus || '50% 10%')}">` : ''}</div>
      <div style="font-size:46px;font-weight:900;letter-spacing:-2px;line-height:1.15;text-align:center;color:${x.hi ? TCOL(x.team || 'KIA') : TXT}">${br(x.label || '')}</div></div>`;
  });
  h += `</div>`;
  B(h);
};
Object.assign(MOTION, { q3p: () => 1.0, crown: () => 1.9, results: () => .9, pct2: () => .8, q3: () => 1.0, fate: () => 1.0, ps5: () => .9, stand: () => .6, ladder: () => .6, sched6: () => .8, pepper: () => .8, mission: () => 1.2, tally: () => .6, lose8: () => 1.2, h2h: () => 1.4, finale: () => .6 });
/* @@LOTTE1006 END */
