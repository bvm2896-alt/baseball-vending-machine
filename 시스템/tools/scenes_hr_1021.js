/* @@HR1021 10/21 새벽 롱폼㉒ — 사용자 "이런 애니메이션(다이아몬드)만 쓰니까 너무 질리는데 다른걸로 바꿔봐 더 재미있게".
   tools/inject_hr_1021.py 가 template_long.html·template_long_v.html 의 function render 앞에 넣는다(이 파일을 고치면 다시 주입).
   공통: 중계 화면 같은 점수 띠(bug) — {inn, score:[원정, 홈], outs, bases:[1루,2루,3루](이름|null), away, home}
   hrcam: 홈런 트래커(옆에서 본 밤 구장, 공 궤적·비거리·불꽃) + 왼쪽 선수 사진
     {img, name, team, bug, launchAt(호흡 번호·소수 가능), dist('145m'|없음), dir('center'|'lc'), burst('솔로 홈런'), runners:['하주석',...], scoreTo:[7,0]}
   rally: 플레이 카드 릴레이 — 카드가 한 장씩 뒤집히며 결과 도장, 점수 띠의 주자·아웃·점수가 같이 바뀐다
     {bug, plays:[{name, img, team, res, kind:'out'|'on'|'run', at, bases, outs, score, rbi}]} */
(function () {
  /* 로고·팀색은 다른 묶음 안에만 있어서 여기서 다시 둔다 */
  const LOGOI = (n, px, st = '') => `<img src="${LOGO[(T(n) || {}).code] || ''}" style="width:${px}px;height:${px}px;object-fit:contain;display:block;${st}">`;
  const TCOL = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  const TXT = typeof window.TXT !== 'undefined' ? window.TXT : '#12161F';
  const cl = (v, a, b) => Math.max(a, Math.min(b, v)), e3 = x => 1 - Math.pow(1 - cl(x, 0, 1), 3), eob = t => { t = cl(t, 0, 1); const c = 1.70158; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
  /* 호흡 k(소수 가능)가 시작한 뒤 지난 초. 아직이면 null */
  const TT = (s, k) => { if (k == null) return 99; const segs = (EP.segT || [])[s.startLine] || [];
    if (!segs.length) return null; const i = Math.floor(k), f = k - i, t0 = segs[i] ?? segs[segs.length - 1], t1 = segs[i + 1] ?? (t0 + 1.5);
    const d = NOW - (t0 + (t1 - t0) * f); return d < 0 ? null : d; };
  const card = (img, w, h, extra = '') => { const src = photoSrc(img);
    return `<div style="position:relative;width:${w}px;height:${h}px;flex:0 0 auto;border-radius:26px;overflow:hidden;background:#1A2234;box-shadow:0 22px 50px rgba(10,14,24,.35);${extra}">${src ? faceImg(src, {}, '50% 14%') : ''}</div>`; };
  /* 점수 띠 */
  function bug(b, sc, outs, bases, pulse = 0, plus = '') {
    const base = (on, x, y) => `<rect x="${x - 13}" y="${y - 13}" width="26" height="26" rx="4" transform="rotate(45 ${x} ${y})" fill="${on ? '#FFC93C' : 'rgba(255,255,255,.14)'}" stroke="${on ? '#FFE08A' : 'rgba(255,255,255,.35)'}" stroke-width="2.5"/>`;
    const dots = [0, 1, 2].map(i => `<span style="width:20px;height:20px;border-radius:50%;background:${i < outs ? '#FF5A63' : 'rgba(255,255,255,.18)'};display:inline-block"></span>`).join('');
    const num = (v, i) => `<span class="num" style="font-size:54px;font-weight:900;color:#fff;min-width:44px;text-align:center;display:inline-block;transform:scale(${i === 0 ? 1 + .25 * pulse : 1})">${v}</span>`;
    return `<div data-nodark="1" style="position:relative;display:flex;align-items:center;gap:26px;height:88px;padding:0 30px;border-radius:44px;background:#0F1626;box-shadow:0 14px 34px rgba(10,14,24,.30);flex:0 0 auto">
      <div style="display:flex;align-items:center;gap:14px">${LOGOI(b.away || 'KIA', 54)}${num(sc[0], 0)}<span style="font-size:40px;font-weight:900;color:#5F6B80">:</span>${num(sc[1], 1)}${LOGOI(b.home || 'LG', 54)}</div>
      <div style="width:2px;height:52px;background:rgba(255,255,255,.18)"></div>
      <div style="font-size:38px;font-weight:900;color:#FFD43B;white-space:nowrap">${esc(b.inn || '')}</div>
      <svg width="92" height="70" viewBox="0 0 92 70">${base(!!bases[1], 46, 18)}${base(!!bases[2], 18, 46)}${base(!!bases[0], 74, 46)}</svg>
      <div style="display:flex;gap:8px;align-items:center"><span style="font-size:26px;font-weight:900;color:#9AA6B8;margin-right:4px">OUT</span>${dots}</div>
      ${plus ? `<div style="position:absolute;left:96px;top:-46px;font-size:52px;font-weight:900;color:#FFD43B;text-shadow:0 4px 14px rgba(0,0,0,.45);opacity:${cl(pulse * 3, 0, 1)};transform:translateY(${((1 - pulse) * 16).toFixed(1)}px)">${esc(plus)}</div>` : ''}</div>`;
  }
  /* ── hrcam v2 (10/21 사용자 "공 날아가는거밖에 없는거야? 더 재미가 없어졌는데") ──
     투구 → 스윙(딱!·번쩍·흔들림) → 카메라가 공을 따라감(배경이 흘러감·비거리 숫자) → 담장 넘김(관중 들썩·불꽃 3번·꽃가루·글자 쾅)
     → 작은 다이아몬드에서 주자들이 한 명씩 홈으로 들어오고 점수가 1점씩 오른다 */
  const PW = 1180, PH = 540, GY = 452, HOME = 170, FENCE = 1960, WW = 2520;
  const R0 = (seed => { let r = seed; return () => (r = (r * 9301 + 49297) % 233280) / 233280; });
  const FANS = (() => { const r = R0(11), o = []; for (let i = 0; i < 420; i++) { const x = 2000 + r() * 520, top = 300 - (x - 2000) * .36, y = top + 10 + r() * (GY - top - 14);
      o.push([x, y, 2.2 + r() * 2.6, r() < .5 ? '#C70125' : r() < .5 ? '#FFD43B' : '#E6EBF3', r() * 6.28]); } return o; })();
  const CONF = (() => { const r = R0(5), o = []; for (let i = 0; i < 70; i++) o.push([r() * PW, -40 - r() * 260, 6 + r() * 7, ['#FFD43B', '#FF5A63', '#5BD08A', '#6FA8FF', '#FFFFFF'][i % 5], r() * 6.28, .6 + r() * .8]); return o; })();
  function figure(x, ang, team, alpha = 1) {   /* 옆에서 본 타자(오른쪽 = 투수 쪽). ang = 방망이 각도(도) */
    const a = ang * Math.PI / 180, hx = x + 26, hy = GY - 88, bx = hx + Math.cos(a) * 92, by = hy + Math.sin(a) * 92;
    return `<g opacity="${alpha}"><ellipse cx="${x + 10}" cy="${GY + 4}" rx="46" ry="7" fill="rgba(0,0,0,.35)"/>
      <path d="M${x - 8} ${GY} L${x + 4} ${GY - 52} L${x + 18} ${GY - 52} L${x + 40} ${GY}" stroke="#E9ECF1" stroke-width="15" stroke-linecap="round" fill="none"/>
      <rect x="${x - 6}" y="${GY - 112}" width="34" height="64" rx="15" fill="#1B2238"/><rect x="${x - 6}" y="${GY - 64}" width="34" height="8" fill="${TCOL(team)}"/>
      <circle cx="${x + 12}" cy="${GY - 128}" r="17" fill="#E3B48E"/><path d="M${x - 6} ${GY - 130} a18 18 0 0 1 36 0 h10 v5 h-46z" fill="${TCOL(team)}"/>
      <line x1="${x + 8}" y1="${GY - 100}" x2="${hx}" y2="${hy}" stroke="#1B2238" stroke-width="11" stroke-linecap="round"/>
      <line x1="${hx}" y1="${hy}" x2="${bx.toFixed(1)}" y2="${by.toFixed(1)}" stroke="#E9C58F" stroke-width="10" stroke-linecap="round"/><circle cx="${hx}" cy="${hy}" r="7" fill="#F4F4F4"/></g>`;
  }
  function pitcher(x) { return `<g><ellipse cx="${x}" cy="${GY + 2}" rx="60" ry="9" fill="#B98B5B"/>
      <path d="M${x - 14} ${GY} L${x - 4} ${GY - 44} L${x + 8} ${GY - 44} L${x + 20} ${GY}" stroke="#D9DDE4" stroke-width="12" stroke-linecap="round" fill="none"/>
      <rect x="${x - 12}" y="${GY - 96}" width="28" height="56" rx="12" fill="#D9DDE4"/><circle cx="${x + 2}" cy="${GY - 110}" r="14" fill="#E3B48E"/><path d="M${x - 13} ${GY - 112} a15 15 0 0 1 30 0 h-30z" fill="#2B2F3A"/>
      <line x1="${x - 4}" y1="${GY - 86}" x2="${x - 34}" y2="${GY - 70}" stroke="#D9DDE4" stroke-width="9" stroke-linecap="round"/></g>`; }
  const BASES = [[110, 196], [194, 112], [110, 28], [26, 112], [110, 196]];   /* 홈 → 1루 → 2루 → 3루 → 홈 (인셋 안 좌표) */
  const onPath = p => { const i = Math.min(3, Math.floor(p)), f = Math.min(1, p - i), a = BASES[i], b = BASES[i + 1]; return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]; };
  SCENE.hrcam = (lt, s) => {
    const b = s.bug || {}, land = s.dir === 'lc' ? [2210, 300] : [2290, 270], apexY = s.dir === 'lc' ? 62 : 46;
    /* 발사 순간 기준 시각(발사 전이면 음수) — 투구가 발사 0.5초 전부터 보이게 */
    const segs = (EP.segT || [])[s.startLine] || [], k_ = s.launchAt || 0, i_ = Math.floor(k_), f_ = k_ - i_;
    const t0_ = segs.length ? (segs[i_] ?? segs[segs.length - 1]) + (((segs[i_ + 1] ?? ((segs[i_] ?? 0) + 1.5)) - (segs[i_] ?? 0)) * f_) : null;
    const tRaw = t0_ == null ? null : NOW - t0_, t = tRaw == null ? -9 : tRaw, PITCH = .5, FL = 1.9, L = FL + .02;
    const pre = t;
    const u = cl(t / FL, 0, 1), flying = t > 0, landed = t > L;
    const at = v => [HOME + 30 + (land[0] - HOME - 30) * v, (1 - v) * (1 - v) * (GY - 92) + 2 * v * (1 - v) * (apexY * 2 - (GY - 92 + land[1]) / 2) + v * v * land[1]];
    /* 투구: 발사 0.5초 전부터(이 호흡 시작 전이면 화면 밖) */
    const tPitch = t + PITCH; const pitchU = cl(tPitch / PITCH, 0, 1);
    const [bx0, by0] = flying ? at(u) : [560 - 26 + (HOME + 30 - 560 + 26) * pitchU, GY - 110 + 18 * pitchU];
    const camX = cl(bx0 - 420, 0, WW - PW) * (flying ? 1 : 0), X = x => x - camX;
    const shake = t > 0 && t < .3 ? Math.sin(t * 90) * 8 * (1 - t / .3) : landed && t < L + .45 ? Math.sin(t * 80) * 10 * (1 - (t - L) / .45) : 0;
    const swing = t < -.12 ? -128 : t < 0 ? -128 + (133 * (t + .12) / .12) : t < .3 ? 5 - 70 * (t / .3) : -65;
    const excite = cl((u - .78) * 5, 0, 1), fx = landed ? t - L : -1;
    let trail = ''; if (flying) { const n = 48, pts = []; for (let i = 0; i <= n; i++) { const [x, y] = at(u * i / n); pts.push(X(x).toFixed(1) + ',' + y.toFixed(1)); }
      trail = `<polyline points="${pts.join(' ')}" fill="none" stroke="url(#trl2)" stroke-width="10" stroke-linecap="round"/><polyline points="${pts.join(' ')}" fill="none" stroke="#FFF6D0" stroke-width="2.5" opacity=".9"/>`; }
    const lights = [260, 820, 1380, 1940, 2500].map(x => { const sx = x - camX * .45; return `<circle cx="${sx}" cy="40" r="120" fill="url(#hlit2)" opacity=".5"/><rect x="${sx - 34}" y="18" width="68" height="26" rx="4" fill="#F4F1E2"/><rect x="${sx - 3}" y="44" width="6" height="120" fill="#36425E"/>`; }).join('');
    const stripes = Array.from({ length: 18 }, (_, i) => `<rect x="${X(i * 150)}" y="${GY}" width="75" height="${PH - GY}" fill="#fff" opacity=".045"/>`).join('');
    const fans = FANS.map(([x, y, r, c, ph]) => `<circle cx="${X(x).toFixed(1)}" cy="${(y - Math.abs(Math.sin(t * 13 + ph)) * 9 * excite).toFixed(1)}" r="${r.toFixed(1)}" fill="${c}" opacity=".8"/>`).join('');
    const boom = (k, dx, dy, col) => { const q = cl((fx - k * .32) / 1.0, 0, 1); if (q <= 0 || q >= 1) return '';
      const cx = X(land[0] + dx), cy = land[1] - 70 + dy; return Array.from({ length: 20 }, (_, i) => { const a = i / 20 * 6.283, r1 = 18 + 92 * e3(q), r0 = Math.max(0, r1 - 40);
        return `<line x1="${(cx + Math.cos(a) * r0).toFixed(1)}" y1="${(cy + Math.sin(a) * r0).toFixed(1)}" x2="${(cx + Math.cos(a) * r1).toFixed(1)}" y2="${(cy + Math.sin(a) * r1).toFixed(1)}" stroke="${i % 2 ? col : '#FFFFFF'}" stroke-width="5" stroke-linecap="round" opacity="${(1 - q).toFixed(2)}"/>`; }).join(''); };
    const conf = fx > 0 ? CONF.map(([x, y0, sz, c, ph, sp]) => { const y = y0 + fx * 260 * sp; if (y > PH + 20) return ''; return `<rect x="${(x + Math.sin(fx * 3 + ph) * 26).toFixed(1)}" y="${y.toFixed(1)}" width="${sz}" height="${(sz * .55).toFixed(1)}" fill="${c}" transform="rotate(${((fx * 300 + ph * 57) % 360).toFixed(0)} ${x.toFixed(1)} ${y.toFixed(1)})"/>`; }).join('') : '';
    const svg = `<svg width="${PW}" height="${PH}" viewBox="0 0 ${PW} ${PH}" style="display:block">
      <defs><linearGradient id="hsky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060B1A"/><stop offset=".7" stop-color="#14254A"/><stop offset="1" stop-color="#1F3A66"/></linearGradient>
        <radialGradient id="hlit2"><stop offset="0" stop-color="#FFF7D6" stop-opacity=".9"/><stop offset="1" stop-color="#FFF7D6" stop-opacity="0"/></radialGradient>
        <linearGradient id="trl2" x1="0" x2="1"><stop offset="0" stop-color="#FFD43B" stop-opacity=".05"/><stop offset="1" stop-color="#FFD43B" stop-opacity=".95"/></linearGradient>
        <linearGradient id="hgr2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E8B4E"/><stop offset="1" stop-color="#1D6A39"/></linearGradient></defs>
      <rect width="${PW}" height="${PH}" fill="url(#hsky2)"/>${lights}
      <path d="M${X(2000)} 300 L${X(WW)} ${300 - (WW - 2000) * .36} L${X(WW)} ${GY} L${X(2000)} ${GY} Z" fill="#101A30"/>${fans}
      <rect x="0" y="${GY}" width="${PW}" height="${PH - GY}" fill="url(#hgr2)"/>${stripes}
      <ellipse cx="${X(420)}" cy="${GY + 30}" rx="330" ry="34" fill="#B98B5B" opacity=".85"/>
      <rect x="${X(FENCE)}" y="${GY - 74}" width="34" height="74" fill="#0F4D2C"/><rect x="${X(FENCE)}" y="${GY - 80}" width="34" height="8" fill="#FFD43B"/>
      ${pitcher(X(560))}
      <path d="M${X(HOME) - 24} ${GY + 2} h48 l-8 14 h-32 z" fill="#F4F4F4"/>
      ${figure(X(HOME - 46), swing, s.team || 'KIA')}
      ${t > -.02 && t < .22 ? `<g opacity="${(1 - t / .22).toFixed(2)}">${Array.from({ length: 12 }, (_, i) => { const a = i / 12 * 6.283, r = 22 + 60 * (t / .22); return `<line x1="${X(HOME + 30)}" y1="${GY - 92}" x2="${(X(HOME + 30) + Math.cos(a) * r).toFixed(1)}" y2="${(GY - 92 + Math.sin(a) * r).toFixed(1)}" stroke="#FFF6D0" stroke-width="6" stroke-linecap="round"/>`; }).join('')}</g>` : ''}
      ${trail}
      ${flying && !landed ? `<ellipse cx="${X(bx0).toFixed(1)}" cy="${GY + 6}" rx="${(16 - 8 * Math.sin(u * Math.PI)).toFixed(1)}" ry="5" fill="rgba(0,0,0,.35)"/>` : ''}
      ${t > -PITCH && !landed ? `<circle cx="${X(bx0).toFixed(1)}" cy="${by0.toFixed(1)}" r="28" fill="#FFE9A0" opacity="${flying ? .3 : 0}"/><circle cx="${X(bx0).toFixed(1)}" cy="${by0.toFixed(1)}" r="${flying ? 14 : 9}" fill="#FFFFFF" stroke="#E5484D" stroke-width="2.5" opacity="${tPitch > 0 ? 1 : 0}"/>` : ''}
      ${boom(0, 0, 0, '#FFD43B')}${boom(1, -150, 40, '#FF5A63')}${boom(2, 120, -10, '#6FA8FF')}
      ${conf}
      ${t > 0 && t < .12 ? `<rect width="${PW}" height="${PH}" fill="#FFFFFF" opacity="${(.55 * (1 - t / .12)).toFixed(2)}"/>` : ''}
    </svg>`;
    const ddak = t > 0 && t < .9 ? `<div style="position:absolute;left:${X(HOME) + 40}px;top:${GY - 250}px;font-size:96px;font-weight:900;color:#FFFFFF;letter-spacing:-3px;-webkit-text-stroke:4px #C70125;transform:rotate(-10deg) scale(${(.5 + .5 * eob(cl(t / .25, 0, 1))).toFixed(3)});opacity:${cl((.9 - t) / .3, 0, 1).toFixed(2)}">딱!</div>` : '';
    const distTxt = s.dist ? `${Math.round((parseInt(s.dist, 10) || 0) * e3(u))}m` : '';
    const distBox = s.dist ? `<div style="position:absolute;right:26px;top:20px;display:flex;flex-direction:column;align-items:flex-end;opacity:${flying ? 1 : 0}"><span style="font-size:28px;font-weight:900;color:#9AA6B8">비거리</span><span class="num" style="font-size:90px;font-weight:900;letter-spacing:-3px;color:#FFD43B;line-height:1">${distTxt}</span></div>` : '';
    const over = u > .8 && !landed ? `<div style="position:absolute;left:50%;top:22px;transform:translateX(-50%);font-size:50px;font-weight:900;color:#FFFFFF;white-space:nowrap;opacity:${cl((u - .8) * 6, 0, 1).toFixed(2)}">넘어간다!</div>` : '';
    const burstP = landed ? cl((fx - .02) / .45, 0, 1) : 0;
    const burst = s.burst ? `<div style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%) rotate(-4deg) scale(${burstP <= 0 ? .4 : (.4 + .6 * eob(burstP)).toFixed(3)});opacity:${cl(burstP * 2, 0, 1).toFixed(2)};font-size:140px;font-weight:900;letter-spacing:-5px;color:#FFD43B;white-space:nowrap;text-shadow:0 8px 0 #A3001B, 0 18px 40px rgba(0,0,0,.6)">${esc(s.burst)}</div>` : '';
    /* 주자 돌기 */
    const RN = s.runners || [], bs = b.bases || [null, null, null], SEG = .34, T0 = L + .25;
    const startOf = n => { const k = bs.indexOf(n); return k < 0 ? 0 : k + 1; };
    const posOf = n => landed ? Math.min(4, startOf(n) + Math.max(0, (fx - .25) / SEG)) : startOf(n);
    const arrived = RN.map(n => posOf(n) >= 4), got = arrived.filter(Boolean).length;
    const lastIn = RN.reduce((m, n) => posOf(n) >= 4 ? Math.max(m, T0 + (4 - startOf(n)) * SEG) : m, -1), pulse = lastIn > 0 ? Math.max(0, 1 - (t - lastIn) / .4) : 0;
    const inP = landed ? cl((fx - .05) / .3, 0, 1) : 0;
    const inset = RN.length ? `<div style="position:absolute;left:22px;top:22px;width:220px;height:224px;border-radius:22px;background:rgba(6,10,20,.78);border:2px solid rgba(255,255,255,.18);opacity:${inP.toFixed(2)}">
      <svg width="220" height="224" viewBox="0 0 220 224"><path d="M110 196 L194 112 L110 28 L26 112 Z" fill="#2E8B4E" stroke="#C7A06A" stroke-width="5"/>
        ${BASES.slice(1, 4).map(([x, y]) => `<rect x="${x - 10}" y="${y - 10}" width="20" height="20" transform="rotate(45 ${x} ${y})" fill="#F4F4F4"/>`).join('')}<path d="M99 192 h22 l-4 9 h-14z" fill="#F4F4F4"/>
        ${RN.map((n, i) => { const p = posOf(n); if (p >= 4) return ''; const [x, y] = onPath(p); return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="13" fill="${startOf(n) === 0 ? '#FFD43B' : '#FF5A63'}" stroke="#fff" stroke-width="3"/>`; }).join('')}</svg>
      <div style="position:absolute;left:0;right:0;bottom:-44px;text-align:center;font-size:32px;font-weight:900;color:#FFD43B;white-space:nowrap;text-shadow:0 2px 6px rgba(0,0,0,.6)">${got ? got + '명 홈인' : ''}</div></div>` : '';
    const chips = RN.length ? `<div style="position:absolute;left:26px;bottom:20px;display:flex;gap:12px">${RN.map((n, i) => { const p = arrived[i] ? cl((t - (T0 + (4 - startOf(n)) * SEG)) / .3, 0, 1) : 0;
      return `<div style="display:flex;align-items:center;gap:8px;height:54px;padding:0 20px;border-radius:27px;background:#C70125;color:#fff;font-size:31px;font-weight:900;white-space:nowrap;opacity:${cl(p * 2, 0, 1).toFixed(2)};transform:translateY(${((1 - e3(p)) * 18).toFixed(1)}px)">${esc(n)} <span style="color:#FFD43B">홈인</span></div>`; }).join('')}</div>` : '';
    const sc0 = (b.score || [0, 0]).slice();
    const basesNow = landed ? [0, 1, 2].map(k => { const n = bs[k]; return n && posOf(n) < 4 ? n : null; }) : bs;
    const panel = `<div data-nodark="1" style="position:relative;width:${PW}px;height:${PH}px;border-radius:30px;overflow:hidden;flex:0 0 auto;box-shadow:0 24px 54px rgba(10,14,24,.32);transform:translate(${shake.toFixed(1)}px,${(shake * .5).toFixed(1)}px)">${svg}${ddak}${distBox}${over}${burst}${inset}${chips}</div>`;
    const PWc = 418, PHc = Math.round(PWc / .774);
    const left = `<div style="position:relative;flex:0 0 auto">${card(s.img, PWc, PHc)}<div style="position:absolute;left:0;right:0;bottom:0;height:150px;border-radius:0 0 26px 26px;background:linear-gradient(180deg,rgba(10,14,24,0),rgba(10,14,24,.88))"></div>
      <div style="position:absolute;left:24px;bottom:20px;display:flex;align-items:center;gap:12px">${LOGOI(s.team || 'KIA', 54)}<b style="font-size:60px;font-weight:900;letter-spacing:-2px;color:#fff;white-space:nowrap">${esc(s.name || '')}</b></div></div>`;
    B(`<div class="col" style="width:100%;align-items:center;gap:22px">${bug(b, [sc0[0] + got, sc0[1]], b.outs || 0, basesNow, pulse, got ? `+${got}` : '')}
      <div class="row" style="gap:34px;flex-wrap:nowrap;align-items:center">${left}${panel}</div></div>`);
  };
  /* ── rally ── */
  SCENE.rally = (lt, s) => {
    const b = s.bug || {}, pl = s.plays || [];
    const P = pl.map(x => { const tt = TT(s, x.at); return tt == null ? 0 : cl(tt / .55, 0, 1); });
    let cur = -1; P.forEach((p, i) => { if (p >= .5) cur = i; });
    const st = cur < 0 ? { score: b.score || [0, 0], outs: b.outs || 0, bases: b.bases || [null, null, null] } : pl[cur];
    const runP = cur >= 0 && pl[cur].kind === 'run' ? P[cur] : 0;
    const CW = 262, CH = Math.round(CW / .774);
    const cards = pl.map((x, i) => { const p = P[i], ang = (1 - e3(p)) * 88, out = x.kind === 'out', run = x.kind === 'run';
      const col = out ? '#5F6B80' : run ? '#E8A100' : '#C70125';
      return `<div class="col" style="align-items:center;gap:12px;flex:0 0 auto;opacity:${cl(p * 3, 0, 1).toFixed(2)};transform:perspective(900px) rotateY(${ang.toFixed(1)}deg) translateY(${run ? -10 * e3(p) : 0}px)">
        <div style="position:relative">${card(x.img, CW, CH, `${out ? 'filter:grayscale(.85) brightness(.85);' : ''}${run ? `outline:7px solid #FFC93C;box-shadow:0 0 0 7px #FFC93C, 0 24px 60px rgba(232,161,0,.55);` : ''}`)}
          <div style="position:absolute;left:50%;bottom:16px;transform:translateX(-50%) rotate(-5deg) scale(${p <= 0 ? 1.5 : (1.5 - .5 * e3(cl(p * 1.4 - .3, 0, 1))).toFixed(3)});opacity:${cl(p * 2 - .5, 0, 1).toFixed(2)};border:6px solid ${col};background:rgba(255,255,255,.94);color:${col};border-radius:16px;padding:4px 16px;font-size:${run ? 40 : 36}px;font-weight:900;white-space:nowrap">${esc(x.res)}</div></div>
        <b style="font-size:46px;font-weight:900;letter-spacing:-1.5px;white-space:nowrap;color:${out ? '#5F6B80' : TXT}">${esc(x.name)}</b></div>`; });
    const arrows = cards.map((c, i) => i < cards.length - 1 ? c + `<div style="flex:0 0 auto;font-size:44px;font-weight:900;color:${P[i + 1] > .3 ? '#C70125' : '#C9D2E0'};margin-top:-60px">›</div>` : c).join('');
    const pulse = runP > 0 ? Math.sin(runP * Math.PI) : 0;
    B(`<div class="col" style="width:100%;align-items:center;gap:40px">${bug(b, st.score, st.outs, st.bases, pulse, runP > 0 ? (pl[cur].rbi || '+1') : '')}
      <div class="row" style="gap:14px;flex-wrap:nowrap;align-items:center">${arrows}</div></div>`);
  };

  /* ── plog ── 투수 기록판(10/21 사용자 "투수들 투구 기록도 나오면 재미있을거같은데 애니메이션이랑"): 왼쪽 사진 + 오른쪽 어두운 기록판
     {img, name, team, sub, stamp:{t, at}, blocks:[{type:'inn', ip, tag1, at} | {type:'pitch', n, at, k} | {type:'k', n, at} | {type:'runs', n, at} | {type:'zero', k, at} | {type:'line', items:[[k,v,hi]], at}]} — KBO 박스스코어 */
  SCENE.plog = (lt, s) => {
    const RW = 1040, tc = TCOL(s.team || 'KIA');
    const Pr = (k, d) => { const tt = TT(s, k); return tt == null ? 0 : cl(tt / d, 0, 1); };
    const lab = (t, op = 1) => `<div style="font-size:30px;font-weight:900;color:#9AA6B8;white-space:nowrap;opacity:${op}">${esc(t)}</div>`;
    const blk = z => { const p = Pr(z.at, z.type === 'pitch' ? 1.6 : z.type === 'inn' ? 1.2 : z.type === 'k' ? 1.1 : .6), op = cl(p * 4, 0, 1).toFixed(2);
      if (z.type === 'inn') { const nb = Math.max(5, Math.ceil(z.ip - 1e-6)), wh = Math.floor(z.ip + 1e-6), fr = Math.round((z.ip - wh) * 3);
        const txt = wh + (fr ? (fr === 1 ? '⅓' : '⅔') : '') + '이닝';
        const bx = Array.from({ length: nb }, (_, i) => { const f = cl(z.ip - i, 0, 1), g = cl(p * (nb + 1) - i, 0, 1) * f;
          return `<div class="col" style="align-items:center;gap:6px"><div style="position:relative;width:66px;height:66px;border-radius:12px;border:3px solid #2C3A55;background:#0A1120;overflow:hidden"><div style="position:absolute;left:0;top:0;bottom:0;width:${(g * 100).toFixed(1)}%;background:linear-gradient(180deg,#FFD866,#F2B705)"></div>
            <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;color:${g > .5 ? '#3A2414' : '#4F5D78'}">${i + 1}</div></div>
            ${i === 0 && z.tag1 ? `<div style="font-size:24px;font-weight:900;color:#5BD08A;white-space:nowrap;opacity:${cl(p * 3 - .5, 0, 1).toFixed(2)}">${esc(z.tag1)}</div>` : `<div style="height:${z.tag1 ? 30 : 0}px"></div>`}</div>`; }).join('');
        return `<div class="col" style="gap:10px;align-items:flex-start;opacity:${op}">${lab('이닝')}<div class="row" style="gap:10px;align-items:flex-start;flex-wrap:nowrap">${bx}<div class="num" style="margin-left:18px;font-size:66px;font-weight:900;color:#FFD43B;white-space:nowrap;line-height:66px">${txt}</div></div></div>`; }
      if (z.type === 'pitch') { const PER = 26, n = z.n, sh = Math.round(n * e3(p));
        const dots = Array.from({ length: n }, (_, i) => `<span style="width:20px;height:20px;border-radius:50%;display:inline-block;background:${i < sh ? '#F4F1E2' : 'rgba(255,255,255,.08)'};${i < sh ? 'box-shadow:inset -3px -3px 0 rgba(199,1,37,.35)' : ''};transform:scale(${i === sh - 1 ? 1.35 : 1})"></span>`).join('');
        return `<div class="col" style="gap:10px;align-items:flex-start;opacity:${op}">${lab(z.k || '투구 수')}<div class="row" style="gap:24px;align-items:center;flex-wrap:nowrap"><div style="display:grid;grid-template-columns:repeat(${PER},20px);gap:6px">${dots}</div><div class="num" style="font-size:72px;font-weight:900;color:#FFFFFF;white-space:nowrap">${sh}<span style="font-size:36px;color:#9AA6B8"> 구</span></div></div></div>`; }
      if (z.type === 'k') { const ks = Array.from({ length: z.n }, (_, i) => { const q = cl(p * (z.n + 2) / 1.4 - i * .7, 0, 1);
          return `<div style="width:56px;height:68px;border-radius:12px;background:#E5484D;color:#fff;font-size:44px;font-weight:900;display:flex;align-items:center;justify-content:center;opacity:${cl(q * 2, 0, 1).toFixed(2)};transform:scale(${q <= 0 ? .4 : (.4 + .6 * eob(q)).toFixed(3)}) rotate(${((1 - e3(q)) * -12).toFixed(1)}deg)">K</div>`; }).join('');
        return `<div class="col" style="gap:10px;align-items:flex-start;opacity:${op}">${lab('삼진')}<div class="row" style="gap:8px;align-items:center;flex-wrap:nowrap">${ks || `<div class="num" style="font-size:66px;font-weight:900;color:#5F6B80">0개</div>`}${z.n ? `<div class="num" style="margin-left:14px;font-size:66px;font-weight:900;color:#FF6B6B;white-space:nowrap">${z.n}개</div>` : ''}</div></div>`; }
      if (z.type === 'runs') { const bs = Array.from({ length: z.n }, (_, i) => { const q = cl(p * 3 - i * .35, 0, 1);
          return `<div style="width:46px;height:46px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FF8A90,#E5222E);box-shadow:0 0 18px rgba(255,90,99,.55);opacity:${cl(q * 2, 0, 1).toFixed(2)};transform:scale(${q <= 0 ? .3 : (.3 + .7 * eob(q)).toFixed(3)})"></div>`; }).join('');
        return `<div class="col" style="gap:10px;align-items:flex-start;opacity:${op}">${lab('실점')}<div class="row" style="gap:10px;align-items:center;flex-wrap:nowrap">${bs}<div class="num" style="margin-left:14px;font-size:66px;font-weight:900;color:#FF6B6B;white-space:nowrap">${z.n}점</div></div></div>`; }
      if (z.type === 'zero') return `<div class="row" style="gap:28px;align-items:center;flex-wrap:nowrap;opacity:${op}"><div class="col" style="gap:0;align-items:flex-start">${lab(z.k)}<div class="num" style="font-size:150px;font-weight:900;letter-spacing:-6px;color:#5BD08A;line-height:1;transform:scale(${p <= 0 ? 1.6 : (1.6 - .6 * e3(p)).toFixed(3)});transform-origin:left center">0<span style="font-size:60px">개</span></div></div>
          <div style="border:7px solid #5BD08A;color:#5BD08A;border-radius:18px;padding:6px 22px;font-size:46px;font-weight:900;white-space:nowrap;transform:rotate(-6deg) scale(${cl(p * 2 - .6, 0, 1) <= 0 ? 1.5 : (1.5 - .5 * e3(cl(p * 2 - .6, 0, 1))).toFixed(3)});opacity:${cl(p * 3 - 1.2, 0, 1).toFixed(2)}">${esc(z.stamp || '')}</div></div>`;
      if (z.type === 'line') return `<div class="row" style="gap:46px;align-items:flex-end;flex-wrap:nowrap;opacity:${z.items.some(x => x[3] != null) ? 1 : op}">${(z.items || []).map(([k, v, hi, ia], i) => { const q = ia == null ? cl(p * 3 - i * .4, 0, 1) : Pr(ia, .5);
          return `<div class="col" style="gap:0;align-items:flex-start;opacity:${cl(q * 2, 0, 1).toFixed(2)};transform:translateY(${((1 - e3(q)) * 16).toFixed(1)}px)">${lab(k)}<div class="num" style="font-size:62px;font-weight:900;color:${hi ? '#FF6B6B' : '#FFFFFF'};white-space:nowrap">${esc(v)}</div></div>`; }).join('')}</div>`;
      return ''; };
    const sp = s.stamp ? Pr(s.stamp.at, .45) : 0;
    const head = `<div class="row" style="gap:18px;align-items:center;justify-content:flex-start;flex-wrap:nowrap;width:100%">${LOGOI(s.team || 'KIA', 60)}<b style="font-size:64px;font-weight:900;letter-spacing:-2px;color:#fff;white-space:nowrap">${esc(s.name || '')}</b>
      <span style="font-size:30px;font-weight:900;color:#0F1626;background:${tc === '#12161F' ? '#E6EBF3' : '#FFD43B'};border-radius:22px;padding:6px 18px;white-space:nowrap">${esc(s.sub || '')}</span>
      ${s.stamp ? `<div style="position:absolute;right:48px;bottom:64px;border:6px solid #FFD43B;color:#FFD43B;border-radius:16px;padding:4px 18px;font-size:40px;font-weight:900;white-space:nowrap;transform:rotate(-4deg) scale(${sp <= 0 ? 1.5 : (1.5 - .5 * e3(sp)).toFixed(3)});opacity:${cl(sp * 1.6, 0, 1).toFixed(2)}">${esc(s.stamp.t)}</div>` : ''}</div>`;
    const PWc = 480, PHc = 640;
    const board = `<div data-nodark="1" class="col" style="width:${RW}px;height:${PHc}px;box-sizing:border-box;padding:30px 44px;border-radius:30px;background:linear-gradient(160deg,#141E33,#0B1222);box-shadow:0 24px 54px rgba(10,14,24,.32);gap:20px;position:relative;align-items:flex-start;justify-content:flex-start;flex:0 0 auto">${head}<div style="width:100%;height:2px;background:rgba(255,255,255,.12)"></div>${(s.blocks || []).map(blk).join('')}
      <div style="position:absolute;right:30px;bottom:18px;font-size:22px;font-weight:700;color:#5F6B80">기록: KBO 박스스코어</div></div>`;
    B(`<div class="row" style="width:100%;gap:40px;justify-content:center;align-items:center;flex-wrap:nowrap">${card(s.img, PWc, PHc)}${board}</div>`);
  };
  Object.assign(MOTION, { plog: () => 2.4, hrcam: () => 4.6, rally: s => .6 + (s.plays || []).length * .5 });
})();
/* @@HR1021END */
