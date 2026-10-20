/* @@CPITCH1020 10/20 밤 롱폼 「준PO 3차전 리뷰 · PO 1차전」 — 사용자 "왜 왼손타자가 카라스코한테 강한지 애니메이션같은걸로 보여주면 더 이해가 잘 되고 직관적".
   tools/inject_cpitch_1020.py 가 template_long.html·template_long_v.html 의 function render 앞에 넣는다(이 파일을 고치면 다시 주입).
   cpitch: 포수 시점 체인지업 궤적 두 칸.
     s.panels = [{tag, brk(옆으로 휘는 정도 0~1), res:'miss'|'hit', at(이 줄 호흡 번호) | done:true(이미 끝난 모습) | 없음(? 자리)}]
     s.gap = {panel, text, at}  — 노린 곳과 실제 공 사이 화살표 글(예: '약 16cm 덜 휨')
     s.stats = {title, rows:[{k, v(숫자), at, hi}], src, at} — 아래 띠(헛스윙률 비교)
   어두운 판을 장면 안에 직접 그려서 밝은/어두운 테마 어느 쪽에서도 같은 모습이다.
   근거: 야구공작소 카라스코 스카우팅 리포트 — 체인지업 수평 변화량 리그 평균 대비 -6.4인치(≈16cm), 좌타자 상대 헛스윙률 11.1%·우타자 42.9%. */
(function () {
  const cl = (v, a, b) => Math.max(a, Math.min(b, v)), e3 = x => 1 - Math.pow(1 - cl(x, 0, 1), 3);
  const W = 760, Hh = 500;
  /* 포수 시점(화면 오른쪽 = 왼손 타자 타석). 오른손 투수의 체인지업은 투수 팔 쪽(화면 왼쪽 = 왼손 타자 바깥쪽)으로 휜다 */
  const R = [372, 128], G = [418, 384], PIV = [612, 318];   /* 놓는 곳 · 타자가 노린 곳(휘지 않았을 때 도착점) · 방망이 축(손) */
  const ZX = 296, ZY = 196, ZW = 214, ZH = 236;
  const BAT0 = -62, BAT1 = -196, BATL = 290;                /* 방망이 각도: 시작(위·오른쪽) → 끝(존을 가로질러 왼쪽 아래) */
  const PDUR = 1.05, SW0 = .72;                             /* 공이 오는 시간(초) · 스윙 시작 u */
  const pathAt = (u, E) => { const b = Math.pow(u, 2.6);
    return [R[0] + (G[0] - R[0]) * u + (E[0] - G[0]) * b, R[1] + (G[1] - R[1]) * u + (E[1] - G[1]) * b]; };
  const endOf = brk => [G[0] - 190 * brk, G[1] + 30 * brk];   /* brk 1 = 보통 체인지업(크게 바깥으로) */
  function batter(ang, alpha) {
    const a = ang * Math.PI / 180, bx = PIV[0] + Math.cos(a) * BATL, by = PIV[1] + Math.sin(a) * BATL;
    return `<g opacity="${alpha}"><line x1="${PIV[0]}" y1="${PIV[1]}" x2="${bx.toFixed(1)}" y2="${by.toFixed(1)}" stroke="#E9C58F" stroke-width="15" stroke-linecap="round"/>
      <line x1="${PIV[0]}" y1="${PIV[1]}" x2="${(PIV[0] + Math.cos(a) * 70).toFixed(1)}" y2="${(PIV[1] + Math.sin(a) * 70).toFixed(1)}" stroke="#1B1B1B" stroke-width="10" stroke-linecap="round"/></g>`;
  }
  /* 10/20 23:30 사용자 "재현 그림으로"(실루엣 금지 규칙) — 왼손 타자를 사람처럼 그린 그림(실제 구단 유니폼·로고 없음, 포수 시점: 홈플레이트 쪽=화면 왼쪽을 보고 선다) */
  const bodyFig = k => `<defs>
      <linearGradient id="jz${k}" x1="0" x2="1"><stop offset="0" stop-color="#F4F5F7"/><stop offset=".65" stop-color="#DADDE3"/><stop offset="1" stop-color="#A9AFBA"/></linearGradient>
      <linearGradient id="pt${k}" x1="0" x2="1"><stop offset="0" stop-color="#F6F6F4"/><stop offset="1" stop-color="#B9BDC4"/></linearGradient>
      <radialGradient id="hm${k}" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#4A5A82"/><stop offset=".55" stop-color="#1E2A4A"/><stop offset="1" stop-color="#0E1528"/></radialGradient>
      <linearGradient id="sk${k}" x1="0" x2="1"><stop offset="0" stop-color="#E9B993"/><stop offset="1" stop-color="#B9825E"/></linearGradient></defs>
    <ellipse cx="648" cy="496" rx="92" ry="10" fill="rgba(0,0,0,.35)"/>
    <path d="M672 404 q30 22 32 46 l-8 40 h-22 l4 -38 q-10 -18 -30 -30z" fill="url(#pt${k})" stroke="#8E949E" stroke-width="2"/>
    <path d="M630 404 q-28 18 -36 44 l2 42 h22 l-2 -40 q10 -16 32 -28z" fill="url(#pt${k})" stroke="#8E949E" stroke-width="2"/>
    <rect x="590" y="460" width="26" height="30" rx="5" fill="#1E2A4A"/><rect x="676" y="460" width="24" height="30" rx="5" fill="#1E2A4A"/>
    <path d="M582 486 h40 q4 8 -4 10 h-38 q-6 -4 2 -10z" fill="#111"/><path d="M670 486 h38 q6 8 -2 10 h-38 q-4 -4 2 -10z" fill="#111"/>
    <path d="M626 266 q22 -12 56 -2 q10 40 0 96 l-4 46 h-50 l-6 -48 q-8 -50 4 -92z" fill="url(#jz${k})" stroke="#8E949E" stroke-width="2"/>
    <path d="M654 262 v146" stroke="#1E2A4A" stroke-width="3" opacity=".55"/>
    <rect x="624" y="398" width="58" height="12" rx="3" fill="#1E2A4A"/>
    <path d="M638 232 q10 -4 22 0 l-2 34 h-18z" fill="url(#sk${k})"/>
    <path d="M622 272 q-22 8 -20 34" stroke="url(#jz${k})" stroke-width="22" stroke-linecap="round" fill="none"/>
    <path d="M602 304 q2 10 10 14" stroke="url(#sk${k})" stroke-width="15" stroke-linecap="round" fill="none"/>
    <path d="M684 274 q20 18 8 42 q-30 8 -70 4" stroke="url(#jz${k})" stroke-width="20" stroke-linecap="round" fill="none"/>
    <path d="M660 318 q-26 4 -44 0" stroke="url(#sk${k})" stroke-width="14" stroke-linecap="round" fill="none"/>
    <ellipse cx="644" cy="214" rx="24" ry="27" fill="url(#sk${k})"/>
    <path d="M622 210 q-2 -36 30 -40 q38 0 42 34 q2 22 -10 32 l-10 2 q-4 -20 -22 -22 q-16 -2 -30 -6z" fill="url(#hm${k})"/>
    <path d="M626 200 q-20 2 -30 10 q14 2 30 -2z" fill="#0E1528"/>
    <path d="M666 214 q14 2 16 22 l-14 6 q-4 -14 -2 -28z" fill="#16203A"/>
    <path d="M636 186 q14 -10 30 -6" stroke="rgba(255,255,255,.45)" stroke-width="4" stroke-linecap="round" fill="none"/>`;
  const gloves = `<circle cx="${PIV[0]}" cy="${PIV[1]}" r="13" fill="#E8E8E8" stroke="#1E2A4A" stroke-width="3"/>`;
  const zone = `<rect x="${ZX}" y="${ZY}" width="${ZW}" height="${ZH}" fill="rgba(255,255,255,.05)" stroke="#FFFFFF" stroke-width="4" rx="4"/>
      <path d="M${ZX + ZW / 3} ${ZY}v${ZH}M${ZX + 2 * ZW / 3} ${ZY}v${ZH}M${ZX} ${ZY + ZH / 3}h${ZW}M${ZX} ${ZY + 2 * ZH / 3}h${ZW}" stroke="rgba(255,255,255,.22)" stroke-width="2"/>
      <path d="M${ZX - 6} 474h${ZW + 12}v12l-${(ZW + 12) / 2} 22l-${(ZW + 12) / 2} -22z" fill="#F4F1EA" opacity=".9"/>`;
  function panel(pn, q, pr) {
    /* q: 0~ (이 칸이 시작한 뒤 초 단위 진행) — null 이면 아직 안 던짐 */
    const E = endOf(pn.brk), started = q != null;
    const u = started ? cl(q / PDUR, 0, 1) : 0;
    const sw = started ? e3(cl((u - SW0) / (1 - SW0), 0, 1)) : 0;
    const after = started ? Math.max(0, q - PDUR) : 0;
    let svg = `<defs><radialGradient id="cpg${pn.i}" cx="50%" cy="35%" r="75%"><stop offset="0" stop-color="#22324D"/><stop offset="1" stop-color="#0C1424"/></radialGradient></defs>
      <rect width="${W}" height="${Hh}" fill="url(#cpg${pn.i})"/><ellipse cx="${W / 2}" cy="${Hh + 40}" rx="${W * .62}" ry="120" fill="#4A3424" opacity=".55"/>
      <circle cx="${R[0]}" cy="${R[1]}" r="10" fill="rgba(255,255,255,.25)"/><text x="${R[0] + 20}" y="${R[1] + 8}" font-size="22" font-weight="800" fill="rgba(255,255,255,.55)" text-anchor="start">투수</text>
      ${zone}${bodyFig(pn.i)}`;
    /* 노린 곳(휘지 않았을 때 갈 길) — 점선 */
    const gl = started ? cl(u * 1.4, 0, 1) : 0;
    if (started) svg += `<path d="M${R[0]} ${R[1]} L${G[0]} ${G[1]}" stroke="rgba(255,255,255,.35)" stroke-width="4" stroke-dasharray="10 12" opacity="${gl.toFixed(2)}"/>`;
    /* 방망이: 스윙 잔상 */
    const ang = BAT0 + (BAT1 - BAT0) * sw;
    if (sw > 0 && sw < 1) for (let k = 3; k >= 1; k--) svg += batter(BAT0 + (BAT1 - BAT0) * Math.max(0, sw - k * .09), (.12 * (4 - k)).toFixed(2));
    svg += batter(ang, 1) + gloves;
    /* 공 궤적 점 + 공 */
    if (started) {
      const n = 16;
      for (let k = 0; k <= n; k++) { const uu = k / n; if (uu > u) break; const [x, y] = pathAt(uu, E);
        svg += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${(3 + 7 * uu * uu).toFixed(1)}" fill="${pn.res === 'hit' ? '#FFB020' : '#5EC8FF'}" opacity="${(.25 + .5 * uu).toFixed(2)}"/>`; }
      let [bx, by] = pathAt(u, E), br_ = 6 + 20 * u * u;
      if (pn.res === 'hit' && after > 0) { const f = e3(after / .7); bx = E[0] + (560 - E[0]) * f; by = E[1] + (70 - E[1]) * f; br_ = 26 - 18 * f; }
      if (pn.res === 'hit' && after > .7) {} else if (!(pn.res === 'miss' && after > .5)) svg += `<circle cx="${bx.toFixed(1)}" cy="${by.toFixed(1)}" r="${br_.toFixed(1)}" fill="#FFFFFF" stroke="#D4362F" stroke-width="3"/>`;
      else svg += `<circle cx="${E[0]}" cy="${E[1]}" r="26" fill="#FFFFFF" stroke="#D4362F" stroke-width="3"/>`;
      if (pn.res === 'hit' && after > 0 && after < .55) { const p = after / .55;
        svg += `<g transform="translate(${E[0]} ${E[1]}) scale(${(.6 + .8 * e3(p)).toFixed(2)})" opacity="${(1 - p * .8).toFixed(2)}"><path d="M0 -70 L16 -22 L66 -30 L28 4 L54 48 L6 26 L-22 66 L-24 18 L-70 8 L-30 -16 L-46 -60 L-8 -30z" fill="#FFD43B"/></g>`; }
      /* 노린 곳 ↔ 실제 공 사이 화살표 */
      if (after > .35) { const p = e3((after - .35) / .4), x0 = G[0], x1 = x0 + (E[0] - x0) * p, y = Math.max(G[1], E[1]) + 52;
        svg += `<g opacity="${cl(p * 1.5, 0, 1).toFixed(2)}"><circle cx="${G[0]}" cy="${G[1]}" r="26" fill="none" stroke="#FFD43B" stroke-width="5" stroke-dasharray="8 7"/><text x="${G[0] - 8}" y="${G[1] - 40}" font-size="26" font-weight="900" fill="#FFD43B" text-anchor="middle">노린 곳</text>
          <line x1="${x0}" y1="${y}" x2="${x1.toFixed(1)}" y2="${y}" stroke="${pn.res === 'hit' ? '#FFB020' : '#5EC8FF'}" stroke-width="6"/>
          ${Math.abs(E[0] - x0) > 40 ? `<path d="M${x1.toFixed(1)} ${y} l18 -12 v24z" fill="${pn.res === 'hit' ? '#FFB020' : '#5EC8FF'}"/>` : ''}</g>`; }
    } else {
      svg += `<text x="${W / 2}" y="${Hh / 2 + 30}" font-size="150" font-weight="900" fill="rgba(255,255,255,.18)" text-anchor="middle">?</text>`;
    }
    /* 결과 배지 */
    const rp = started ? e3(cl((after - .15) / .35, 0, 1)) : 0;
    const badge = rp > 0 ? `<div style="position:absolute;right:26px;top:84px;padding:8px 26px;border-radius:999px;font-size:40px;font-weight:900;letter-spacing:-1px;color:#fff;
        background:${pn.res === 'hit' ? '#E5484D' : '#2F6FED'};opacity:${cl(rp * 1.4, 0, 1).toFixed(3)};transform:scale(${(.8 + .2 * rp).toFixed(3)})">${pn.res === 'hit' ? '딱! 정타' : '헛스윙'}</div>` : '';
    const gapTxt = pr.gap && pr.gap.panel === pn.i && pr.gapP > 0 ? `<div style="position:absolute;left:24px;top:80px;padding:5px 16px;border-radius:14px;background:rgba(8,12,22,.86);white-space:nowrap;font-size:24px;font-weight:900;color:#FFD43B;letter-spacing:-1px;opacity:${cl(pr.gapP * 1.4, 0, 1).toFixed(3)}">${esc(pr.gap.text)}</div>` : '';
    const tagP = pn.tagP;
    return `<div data-nodark="1" style="position:relative;flex:0 0 ${W}px;width:${W}px;height:${Hh}px;border-radius:30px;overflow:hidden;box-shadow:0 18px 44px rgba(0,0,0,.35);opacity:${cl(tagP * 1.5, 0, 1).toFixed(3)};transform:translateY(${((1 - e3(tagP)) * 30).toFixed(1)}px)">
        <svg viewBox="0 0 ${W} ${Hh}" width="${W}" height="${Hh}" style="position:absolute;inset:0">${svg}</svg>
        <div style="position:absolute;left:24px;top:22px;padding:6px 24px;border-radius:999px;background:${pn.hi ? '#C8102E' : 'rgba(255,255,255,.16)'};color:#fff;font-size:38px;font-weight:900;letter-spacing:-1px;white-space:nowrap">${esc(pn.tag)}</div>
        ${badge}${gapTxt}${true ? '<div style="position:absolute;left:28px;top:78px;font-size:20px;font-weight:700;color:rgba(255,255,255,.5)">※ 이해를 돕는 단순화 그림</div>' : ''}</div>`;
  }
  SCENE.cpitch = (lt, s) => {
    const P = (k, d, off = 0, fb = 0) => { if (k == null) return null; const b = brP(s, k, d, off); return b == null ? c01((lt - (fb + off)) / d) : b; };
    const T = k => { if (k == null) return null; const segs = (EP.segT || [])[s.startLine] || [];   /* 그 호흡이 시작한 뒤 지난 초 */
      const i = Math.floor(k), t0 = segs[i] != null ? segs[i] : (k * 1.6); const lo = (segs.length ? NOW - t0 : lt - k * 1.6); return lo < 0 ? null : lo; };
    const pans = (s.panels || []).map((pn, i) => {
      const o = Object.assign({ i }, pn);
      o.tagP = pn.enterAt == null ? 1 : P(pn.enterAt, .45);
      return o; });
    const gapP = s.gap ? (s.gap.at == null ? 1 : P(s.gap.at, .45, .2)) : 0;
    const pr = { gap: s.gap, gapP };
    const html = pans.map(pn => panel(pn, pn.done ? 99 : (pn.at == null ? null : T(pn.at)), pr)).join('');
    const st = s.stats || {}, sp = s.stats ? (st.at == null ? 1 : P(st.at, .45)) : 0;
    const rows = (st.rows || [{ k: '', v: 0 }, { k: '', v: 0 }]).map(r => { const p = r.at == null ? sp : P(r.at, .7);
      return `<div style="display:flex;align-items:center;gap:14px;opacity:${c01(p * 2).toFixed(3)}"><span style="font-size:34px;font-weight:900;color:#E6EBF3;white-space:nowrap">${esc(r.k)}</span>
        <div style="position:relative;width:160px;height:30px;border-radius:15px;background:rgba(255,255,255,.12);overflow:hidden"><div style="height:100%;width:${(r.v / (st.max || 50) * 100 * e3(p)).toFixed(1)}%;border-radius:15px;background:${r.hi ? '#E5484D' : '#2F6FED'}"></div></div>
        <span class="num" style="font-size:46px;font-weight:900;color:${r.hi ? '#FF6B6B' : '#FFFFFF'};width:130px">${(r.v * e3(p)).toFixed(1)}%</span></div>`; }).join('');
    const strip = `<div data-nodark="1" style="display:flex;align-items:center;justify-content:center;gap:36px;flex:0 0 auto;width:1560px;height:108px;border-radius:26px;background:#0F1828;opacity:${cl(sp * 1.5, 0, 1).toFixed(3)}">
        <div style="display:flex;flex-direction:column;gap:2px"><span style="font-size:34px;font-weight:900;color:#FFD43B;white-space:nowrap">${esc(st.title || '')}</span><span style="font-size:22px;font-weight:700;color:#9AA6B8;white-space:nowrap">${esc(st.src || '')}</span></div>
        ${rows}</div>`;
    B(`<div class="col" style="width:100%;align-items:center;gap:24px"><div class="row" style="gap:40px;flex-wrap:nowrap">${html}</div>${strip}</div>`);
  };
  Object.assign(MOTION, { cpitch: () => 2.4 });
})();
/* @@CPITCH1020END */
