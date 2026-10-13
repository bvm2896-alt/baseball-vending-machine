/* ───── 10/8 밤 롱폼⑨ 검수 반영: 글자 칩 대신 그림(인포그래픽) ─────
   사용자: "텍스트로만 떼우지 말고 모션그래픽과 인포그래픽으로 이해가 되기 쉽게", "이어지는 장면은 사라졌다 생기지 않게".
   ① profile·speech 장면에 viz:[…] — 오른쪽 글 칸(이름·배지 아래)에 그림을 붙인다. 같은 사람 묶음에서 앞 장면과 같은 그림 조각은 다시 안 뜬다.
      steps(시간 순서 줄) · trend(전→후 막대) · rank(순위 메달) · poll(팬 여론 사람 아이콘) · split(두 쪽 의견) · meter(기록 게이지)
      streak(연속 기록 칸) · branch(갈림길) · stamp(도장) · duo(아이콘 숫자 칸)
   ② slotboard: 팀 외국인 자리판(기존 roster 장면과 이름 겹침 피함)(얼굴 + 자리 + 도장) / debate: 팬 커뮤니티 양쪽 주장 */
const VG = ACC, VB = RED, VN = '#3B4A63';
const vcol = c => c === 'bad' ? VB : c === 'good' ? VG : c === 'gold' ? '#E8A100' : c || VN;
const VSVG = {
  money: c => `<svg viewBox="0 0 60 60" width="100%" height="100%"><rect x="4" y="14" width="52" height="32" rx="6" fill="${c}"/><circle cx="30" cy="30" r="9" fill="#fff"/><text x="30" y="35" font-size="14" font-weight="900" text-anchor="middle" fill="${c}">$</text></svg>`,
  trophy: c => `<svg viewBox="0 0 60 60" width="100%" height="100%"><path d="M18,8 H42 V24 C42,33 36,38 30,38 C24,38 18,33 18,24 Z" fill="${c}"/><path d="M18,12 H8 C8,22 12,26 18,26 M42,12 H52 C52,22 48,26 42,26" stroke="${c}" stroke-width="4" fill="none"/><rect x="26" y="38" width="8" height="10" fill="${c}"/><rect x="18" y="48" width="24" height="6" rx="2" fill="${c}"/></svg>`,
  cal: c => `<svg viewBox="0 0 60 60" width="100%" height="100%"><rect x="6" y="10" width="48" height="44" rx="7" fill="#fff" stroke="${c}" stroke-width="4"/><rect x="6" y="10" width="48" height="13" rx="6" fill="${c}"/><rect x="16" y="4" width="5" height="12" rx="2" fill="${c}"/><rect x="39" y="4" width="5" height="12" rx="2" fill="${c}"/></svg>`,
  scout: c => `<svg viewBox="0 0 60 60" width="100%" height="100%"><circle cx="18" cy="34" r="12" fill="none" stroke="${c}" stroke-width="5"/><circle cx="42" cy="34" r="12" fill="none" stroke="${c}" stroke-width="5"/><path d="M28,32 H32" stroke="${c}" stroke-width="5"/><path d="M12,22 L18,12 M48,22 L42,12" stroke="${c}" stroke-width="4" stroke-linecap="round"/></svg>`,
  person: c => ICON.person(c),
  ball: c => `<svg viewBox="0 0 60 60" width="100%" height="100%"><circle cx="30" cy="30" r="24" fill="#fff" stroke="${c}" stroke-width="4"/><path d="M16,12 C24,22 24,38 16,48 M44,12 C36,22 36,38 44,48" stroke="${RED}" stroke-width="3" fill="none" stroke-dasharray="3 3"/></svg>`,
  arm: c => `<svg viewBox="0 0 60 60" width="100%" height="100%"><circle cx="30" cy="30" r="24" fill="${c}"/><path d="M30,16 V44 M16,30 H44" stroke="#fff" stroke-width="7" stroke-linecap="round"/></svg>`,
};
const vIcon = (k, c, w) => `<div style="width:${w}px;height:${w}px;flex:0 0 auto">${(VSVG[k] || VSVG.person)(c)}</div>`;
/* 앞 장면(같은 사람 묶음)의 같은 viz 조각이면 애니메이션 없이 그대로 */
function vPrev(s, j) { const P = s._prev; if (!(s._chain && P && P.viz)) return null; return [].concat(P.viz)[j] || null; }
const jeq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
function vItemP(s, j, it, k, i, lt, base) {
  /* 10/10: 앞 장면에 같은 칸(글·색이 같음 — 언제 뜨는지 at 만 다름)이 있었으면 다시 안 뜬다 */
  const noAt = x => { if (!x) return x; const { at, ...r } = x; return r; };
  const pv = vPrev(s, j); if (pv && pv.type === it.type && jeq(noAt((pv.items || [])[i]), noAt(k))) return 1;
  return pk(s, k && k.at, .5, seg(lt, base + i * .18, .5));
}
const VIZ = {};
VIZ.steps = (lt, s, it, j, W) => {
  const its = it.items || [], n = its.length, cw = W / Math.max(n, it.slots || n), H = it.h || 300;
  const ps = its.map((k, i) => vItemP(s, j, it, k, i, lt, .2));
  let last = -1; ps.forEach((p, i) => { if (p > 0.02) last = i; });
  const xs = its.map((_, i) => cw * i + cw / 2), lineEnd = last < 0 ? xs[0] : xs[Math.max(0, last - 1)] + (xs[last] - xs[Math.max(0, last - 1)]) * eo(ps[last] || 0);
  let h = `<div style="position:relative;width:${W}px;height:${H}px">
    <div style="position:absolute;left:${xs[0]}px;top:78px;height:10px;width:${Math.max(0, lineEnd - xs[0]).toFixed(1)}px;border-radius:5px;background:linear-gradient(90deg,${vcol(its[0] && its[0].c)},${vcol(its[Math.max(0, last)] && its[Math.max(0, last)].c)})"></div>`;
  its.forEach((k, i) => { const p = ps[i], c = vcol(k.c);
    h += `<div style="position:absolute;left:${(xs[i] - cw / 2 + 8).toFixed(1)}px;top:0;width:${(cw - 16).toFixed(1)}px;display:flex;flex-direction:column;align-items:center;${pop(p)}">
      <div class="badge" style="background:${c};font-size:30px;padding:6px 18px;white-space:nowrap">${esc(k.d || '')}</div>
      <div style="width:40px;height:40px;border-radius:50%;background:#fff;border:9px solid ${c};margin-top:10px;box-sizing:border-box"></div>
      <div style="margin-top:16px;background:${c}12;border:4px solid ${c};border-radius:24px;padding:14px 18px;width:100%;box-sizing:border-box;text-align:center;font-size:${k.size || 40}px;font-weight:900;letter-spacing:-1.5px;line-height:1.22;color:${k.c === 'bad' ? VB : k.c === 'good' ? VG : TXT}">${br(k.t || '')}</div></div>`; });
  return h + `</div>`;
};
/* 10/13 밤 사용자("잠깐 지나가는 그래프로 보기에는 무슨 그래프인지 한눈에 안 들어와"): 순위 흐름(invert)은 막대 대신 꺾은선 —
   왼쪽 눈금 'N위'(위가 1위), 날짜마다 점, 점끼리 선이 호흡(at)에 맞춰 이어짐, 점 위에 'N위'. it.bars:true 면 예전 막대 */
VIZ.rankline = (lt, s, it, j, W) => {
  const its = it.items || [], NS = Math.max(its.length, it.slots || 0), rs = its.map(k => +k.v || 1);
  const lo = Math.min(...rs), hi = Math.max(...rs), R = []; for (let r = lo; r <= hi; r++) R.push(r);
  const AX = 110, CW = Math.min(Math.max(250, Math.floor(820 / Math.max(1, NS))), Math.floor((W - AX) / Math.max(1, NS))), GW = AX + CW * NS, PH = it.ph || Math.max(200, Math.min(260, (R.length - 1) * 70)), T0 = 74;   /* 점이 둘뿐이어도 그림 폭 930 안팎 — 작게 왼쪽에 붙지 않게 */
  const y = r => T0 + (R.length > 1 ? (r - lo) / (hi - lo) * PH : PH / 2), x = i => AX + CW * (i + .5);
  const ps = its.map((k, i) => vItemP(s, j, it, k, i, lt, .2));
  const pvT = vPrev(s, j), pT = it.title ? (pvT && pvT.title === it.title ? 1 : pk(s, it.titleAt, .4, seg(lt, .1, .4))) : 0;
  let h = it.title ? `<div class="badge" style="background:${VN};font-size:32px;padding:8px 22px;${pop(pT)}">${esc(it.title)}</div>` : '';
  let svg = R.map(r => `<line x1="${AX - 10}" x2="${GW}" y1="${y(r)}" y2="${y(r)}" stroke="#DCE2EA" stroke-width="3" stroke-dasharray="${r === 1 ? '0' : '8 10'}"/>`).join('');
  its.forEach((k, i) => { if (!i) return; const q = eo(c01(ps[i] * 1.3)); if (q <= 0) return;
    const x1 = x(i - 1), y1 = y(rs[i - 1]), x2 = x1 + (x(i) - x1) * q, y2 = y1 + (y(rs[i]) - y1) * q;
    svg += `<line x1="${x1}" y1="${y1}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${vcol(k.c)}" stroke-width="9" stroke-linecap="round"/>`; });
  its.forEach((k, i) => { const q = c01(ps[i] * 1.6 - (i ? .5 : 0)); if (q <= 0) return;
    svg += `<circle cx="${x(i)}" cy="${y(rs[i])}" r="${(20 * eo(q)).toFixed(1)}" fill="${vcol(k.c)}" stroke="#fff" stroke-width="6"/>`; });
  h += `<div style="position:relative;width:${GW}px;height:${T0 + PH + 70}px">
    ${R.map(r => `<div style="position:absolute;left:0;width:${AX - 22}px;text-align:right;top:${y(r) - 20}px;font-size:32px;font-weight:800;color:${r === 1 ? ACC : GRAY};white-space:nowrap">${r}위</div>`).join('')}
    <svg style="position:absolute;left:0;top:0;overflow:visible" width="${GW}" height="${T0 + PH + 70}">${svg}</svg>
    ${its.map((k, i) => { const q = c01(ps[i] * 1.6 - (i ? .5 : 0));
      return `<div class="num" style="position:absolute;left:${x(i) - CW / 2}px;width:${CW}px;text-align:center;top:${y(rs[i]) - 82}px;font-size:52px;font-weight:900;letter-spacing:-2px;color:${vcol(k.c)};white-space:nowrap;${pop(q)}">${esc(k.vt || k.v + '위')}</div>
        <div style="position:absolute;left:${x(i) - CW / 2}px;width:${CW}px;text-align:center;top:${T0 + PH + 22}px;font-size:32px;font-weight:800;color:#6A7382;white-space:nowrap;opacity:${c01(q * 2)}">${br(k.x || '')}</div>`; }).join('')}
  </div>`;
  return h;
};
VIZ.trend = (lt, s, it, j, W) => {
  if (it.invert && !it.bars) return VIZ.rankline(lt, s, it, j, W);
  /* slots: 막대 자리 수(뒤 장면에서 막대가 늘어도 앞 막대가 안 움직이게) · mx: 높이 기준값(묶음에서 같게) · title: 위 작은 배지 */
  const its = it.items || [], mx0 = it.mx || Math.max(...its.map(k => +k.v || 0), 1e-9), BH = it.bh || 230, BW = 190, GAP = it.gap || 70;
  /* 10/13 사용자 "2위에서 4위로 떨어진 건데 그래프는 올라가는 것처럼 보여": invert=true(순위)면 1위가 가장 높은 막대 — 높이값 = (최대 순위 + 1 − 순위) */
  const HV = k => it.invert ? (mx0 + 1 - (+k.v || 0)) : (+k.v || 0), mx = it.invert ? Math.max(...its.map(HV), 1e-9) : mx0;
  const ps = its.map((k, i) => vItemP(s, j, it, k, i, lt, .2)), NS = Math.max(its.length, it.slots || 0);
  const tot = NS * BW + (NS - 1) * GAP;
  const pvT = vPrev(s, j), pT = it.title ? (pvT && pvT.title === it.title ? 1 : pk(s, it.titleAt, .4, seg(lt, .1, .4))) : 0;
  let h = it.title ? `<div class="badge" style="background:${VN};font-size:32px;padding:8px 22px;${pop(pT)}">${esc(it.title)}</div>` : '';
  h += `<div style="position:relative;width:${W}px;height:${BH + 150}px">`;
  const x0 = it.left ? 20 : (W - tot) / 2 - (it.delta || it.dslot ? 60 : 0), top = 70;
  its.forEach((k, i) => { const p = ps[i], hh = Math.max(.16, HV(k) / mx) * BH * eo(p), c = vcol(k.c), x = x0 + i * (BW + GAP);
    h += `<div style="position:absolute;left:${x}px;top:${top + BH - hh}px;width:${BW}px;height:${hh.toFixed(1)}px;border-radius:20px 20px 6px 6px;background:${c};opacity:${c01(p * 2)}"></div>
      <div class="num" style="position:absolute;left:${x + BW / 2 - (BW + GAP - 20) / 2}px;width:${BW + GAP - 20}px;text-align:center;top:${top + BH - hh - 10}px;transform:translateY(-100%);white-space:nowrap;font-size:${it.vfs || (String(k.vt || k.v).length > 5 ? 50 : 62)}px;font-weight:900;letter-spacing:-2px;color:${c};opacity:${c01(p * 2 - .6)}">${esc(k.vt || k.v)}</div>
      <div style="position:absolute;left:${x - 50}px;width:${BW + 100}px;text-align:center;top:${top + BH + 14}px;font-size:34px;font-weight:800;color:#6A7382;white-space:nowrap;opacity:${c01(p * 2)}">${br(k.x || '')}</div>`; });
  if (its.length >= 2) { const a = its.length - 2, b = its.length - 1, p = ps[b], xa = x0 + a * (BW + GAP) + BW + 18, xb = x0 + b * (BW + GAP) - 18;
    const ya = top + BH - Math.max(.16, HV(its[a]) / mx) * BH + 34, yb = top + BH - Math.max(.16, HV(its[b]) / mx) * BH + 34,   /* 10/10: 화살표는 막대 윗부분 높이로(위 숫자와 안 겹치게) */ q = c01((p - .3) * 1.6), c = vcol(it.dc);
    const xe = xa + (xb - xa) * eo(q), ye = ya + (yb - ya) * eo(q), ang = Math.atan2(yb - ya, xb - xa);
    h += `<svg style="position:absolute;left:0;top:0;overflow:visible" width="${W}" height="${BH + 150}"><path d="M${xa},${ya} L${xe.toFixed(1)},${ye.toFixed(1)}" stroke="${c}" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 18"/>
      ${q > .9 ? `<path d="M${(xb - 34 * Math.cos(ang - .5)).toFixed(1)},${(yb - 34 * Math.sin(ang - .5)).toFixed(1)} L${xb},${yb} L${(xb - 34 * Math.cos(ang + .5)).toFixed(1)},${(yb - 34 * Math.sin(ang + .5)).toFixed(1)}" stroke="${c}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>` : ''}</svg>`;
    if (it.delta) { const pd = pk(s, it.deltaAt, .5, c01((p - .6) * 2.5)), xd = x0 + tot + 40;
      h += `<div style="position:absolute;left:${xd}px;top:${top + BH / 2 - 50}px;${pop(pd)}"><div class="badge" style="background:${c};font-size:44px;padding:12px 26px;white-space:nowrap">${esc(it.delta)}</div></div>`; } }
  return h + `</div>`;
};
VIZ.rank = (lt, s, it, j, W) => {
  const pv = vPrev(s, j), p = pv && jeq(pv, it) ? 1 : pk(s, it.at, .55, seg(lt, .2, .55)), c = it.c === 'bad' ? VB : it.r && /^1위|최다|최초/.test(it.r) ? '#E8A100' : it.r && /2위/.test(it.r) ? '#8A9BB0' : VG;
  return `<div class="row" style="gap:34px;align-items:center;${pop(p)}">
    <div style="width:200px;height:200px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff8 0,#fff0 45%),${c};display:flex;align-items:center;justify-content:center;flex-direction:column;box-shadow:0 14px 34px ${c}55;border:8px solid #fff;outline:5px solid ${c};transform:rotate(${((1 - eo(p)) * -30).toFixed(1)}deg)">
      <div style="font-size:${(it.r || '').length > 3 ? 40 : 64}px;font-weight:900;color:#fff;letter-spacing:-2px;line-height:1.05;text-align:center">${br(it.r || '')}</div></div>
    <div class="col" style="align-items:flex-start;gap:4px"><div style="font-size:40px;font-weight:800;color:#6A7382">${esc(it.k || '')}</div>
      <div class="num" style="font-size:110px;font-weight:900;letter-spacing:-4px;line-height:1;color:${it.c === 'bad' ? VB : TXT}">${esc(it.v || '')}</div></div></div>`;
};
VIZ.poll = (lt, s, it, j, W) => {
  const its = it.items || [];
  let h = it.title ? `<div class="badge" style="background:${VN};font-size:32px;padding:8px 22px;margin-bottom:6px">${esc(it.title)}</div>` : '';
  h += its.map((k, i) => { const p = vItemP(s, j, it, k, i, lt, .2), c = vcol(k.c), n = k.n || 4;
    return `<div class="row" style="gap:22px;align-items:center;${rise(c01(p * 1.5), 20)}">
      <div class="row" style="gap:4px;width:${Math.max(n, it.nmax || 6) * 46}px">${Array.from({ length: n }, (_, m) => `<div style="width:42px;height:64px;${pop(c01(p * 3 - m * .25))}">${ICON.person(c)}</div>`).join('')}</div>
      <div class="col" style="align-items:flex-start;gap:0"><div style="font-size:${k.size || 48}px;font-weight:900;letter-spacing:-1.5px;color:${c === VN ? TXT : c};white-space:nowrap">${br(k.t || '')}</div>${k.note ? `<div style="font-size:30px;font-weight:800;color:#6A7382">${esc(k.note)}</div>` : ''}</div></div>`; }).join('');
  return `<div class="col" style="align-items:flex-start;gap:16px">${h}</div>`;
};
VIZ.split = (lt, s, it, j, W) => {
  /* 10/10 사용자("오버페이 비판 VS 너무 비싸게 줬다 — 같은 뜻인데 VS가 이상"): 맞서는 두 의견만 VS, 말뜻 풀이는 sep:'=' */
  /* 10/8 밤 사용자: 이어지는 장면에서 카드 틀·사람 그림은 그대로, 바뀐 글만 사라지고 새로 뜬다 */
  const side = (k, i) => { const pv = vPrev(s, j), o = pv && pv.type === 'split' ? pv[i ? 'right' : 'left'] || null : null, c = vcol(k.c);
    const p = pk(s, k.at, .5, seg(lt, .2 + i * .4, .5)), keepBox = !!(o && vcol(o.c) === c && (o.n || 3) === (k.n || 3)), sameW = keepBox && o.who === k.who, sameT = keepBox && o.t === k.t;
    const fade = q => `opacity:${c01(q * 1.4).toFixed(3)}`;
    return `<div class="col" style="flex:1 1 0;min-width:0;background:${c}10;border:4px solid ${c};border-radius:28px;padding:20px 22px 24px;gap:12px;align-items:center;${keepBox ? '' : pop(p)}">
      <div class="badge" style="background:${c};font-size:30px;padding:6px 18px;white-space:nowrap;${sameW || !keepBox ? '' : fade(p)}">${esc(k.who || '')}</div>
      <div class="row" style="gap:2px">${Array.from({ length: k.n || 3 }, () => `<div style="width:34px;height:52px">${ICON.person(c)}</div>`).join('')}</div>
      <div style="font-size:${k.size || 44}px;font-weight:900;letter-spacing:-1.5px;line-height:1.22;text-align:center;color:${c === VN ? TXT : c};${sameT || !keepBox ? '' : fade(p)}">${br(k.t || '')}</div></div>`; };
  /* 10/10: 양쪽 카드가 아직 안 떴을 때 VS 동그라미만 떠 있지 않게 — 왼쪽 카드와 같이 뜬다(앞 장면에도 split 이면 그대로) */
  const pvS = vPrev(s, j), vsP = pvS && pvS.type === 'split' ? 1 : pk(s, (it.left || {}).at, .5, seg(lt, .2, .5));
  return `<div class="row" style="width:${W}px;gap:26px;align-items:stretch">${side(it.left || {}, 0)}<div style="align-self:center;width:84px;height:84px;flex:0 0 auto;border-radius:50%;background:${TXT};color:#fff;font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center;${it.sep && it.sep !== 'VS' ? 'font-size:56px;' : ''}${vsP < 1 ? pop(vsP) : ''}">${esc(it.sep || 'VS')}</div>${side(it.right || {}, 1)}</div>`;
};
VIZ.meter = (lt, s, it, j, W) => {
  const pv = vPrev(s, j), p = pv && jeq(pv, it) ? 1 : pk(s, it.at, 1.2, seg(lt, .2, 1.2)), c = vcol(it.c), BW = W - 40, x = (it.v / it.max) * BW * eo(p);
  const xr = it.rec != null ? it.rec / it.max * BW : null;
  return `<div style="position:relative;width:${W}px;height:${it.recLabel ? 230 : 170}px">
    <div style="position:absolute;left:20px;top:${it.recLabel ? 80 : 40}px;width:${BW}px;height:80px;border-radius:40px;background:#E9EDF3;overflow:hidden"><div style="height:100%;width:${x.toFixed(1)}px;background:${c};border-radius:40px"></div></div>
    <div class="num" style="position:absolute;left:${Math.max(20, 20 + x - 300).toFixed(1)}px;width:280px;text-align:right;top:${it.recLabel ? 86 : 46}px;font-size:56px;font-weight:900;color:#fff;letter-spacing:-2px;opacity:${c01(p * 3 - 1)}">${esc(it.vt || it.v)}</div>
    ${xr != null ? `<div style="position:absolute;left:${(20 + xr - 4).toFixed(1)}px;top:${it.recLabel ? 60 : 20}px;width:8px;height:120px;background:${TXT};opacity:${c01(p * 3)}"></div>
      <div class="badge" style="position:absolute;right:20px;top:0;background:${TXT};font-size:32px;padding:6px 18px;white-space:nowrap;opacity:${c01(p * 3)}">${esc(it.recLabel || '')}</div>` : ''}
    ${it.k ? `<div style="position:absolute;left:20px;top:${it.recLabel ? 6 : -40}px;font-size:36px;font-weight:800;color:#6A7382">${esc(it.k)}</div>` : ''}</div>`;
};
VIZ.streak = (lt, s, it, j, W) => {
  const n = it.n || 10, pv = vPrev(s, j), p0 = pv && jeq(pv, it) ? 1 : pk(s, it.at, it.dur || 1.4, seg(lt, .2, 1.4)), p = eo(p0), c = vcol(it.c || 'good'), bw = Math.min(84, Math.floor((W - (n - 1) * 10) / n));
  return `<div class="col" style="align-items:flex-start;gap:16px">
    <div class="row" style="gap:10px">${Array.from({ length: n }, (_, m) => { const q = c01(p * n - m); return `<div style="width:${bw}px;height:${bw}px;border-radius:16px;border:5px solid ${c};background:${q > .5 ? c : '#fff'};display:flex;align-items:center;justify-content:center;transform:scale(${(.85 + .15 * eo(q)).toFixed(3)})">${q > .5 ? `<svg viewBox="0 0 40 40" width="70%" height="70%"><path d="M8,21 L17,30 L33,11" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>` : ''}</div>`; }).join('')}</div>
    <div class="row" style="gap:16px;align-items:baseline"><div class="num" style="font-size:84px;font-weight:900;letter-spacing:-3px;color:${c}">${Math.max(0, Math.min(n, Math.floor(p * n + 0.5)))}경기 연속</div><div style="font-size:44px;font-weight:900;color:${TXT}">${esc(it.label || '')}</div></div>
    ${it.from ? `<div class="badge" style="background:${VN};font-size:30px;padding:6px 18px">${esc(it.from)}</div>` : ''}</div>`;
};
VIZ.branch = (lt, s, it, j, W) => {
  const its = it.items || [], pv = vPrev(s, j), p0 = pv && pv.type === 'branch' && jeq(pv.from, it.from) ? 1 : pk(s, it.at, .5, seg(lt, .2, .5));
  const RH = 104, H = Math.max(its.length * RH + (its.length - 1) * 16, 140), LW = it.lw || 380;
  let h = `<div style="position:relative;width:${W}px;height:${H}px">
    <div style="position:absolute;left:0;top:${H / 2 - 62}px;width:${LW}px;height:124px;border-radius:28px;background:${vcol(it.fc)};color:#fff;display:flex;align-items:center;justify-content:center;text-align:center;font-size:${it.fsize || 44}px;font-weight:900;letter-spacing:-1.5px;line-height:1.2;${pop(p0)}">${br(it.from || '')}</div>`;
  its.forEach((k, i) => { const p = vItemP(s, j, it, k, i, lt, .5), c = vcol(k.c), y = i * (RH + 16) + RH / 2, x1 = LW + 10, x2 = LW + 150;
    h += `<svg style="position:absolute;left:0;top:0;overflow:visible" width="${W}" height="${H}"><path d="M${x1},${H / 2} C${x1 + 70},${H / 2} ${x2 - 70},${y} ${(x1 + (x2 - x1) * eo(p)).toFixed(1)},${y}" stroke="${c}" stroke-width="8" fill="none" stroke-linecap="round" opacity="${c01(p * 2)}"/></svg>
      <div style="position:absolute;left:${x2 + 10}px;top:${y - RH / 2}px;height:${RH}px;padding:0 30px;border-radius:24px;border:5px solid ${c};background:#fff;display:flex;align-items:center;gap:14px;font-size:${k.size || 46}px;font-weight:900;letter-spacing:-1.5px;color:${c === VN ? TXT : c};white-space:nowrap;${slideX(p, -30)}">${k.logo && LOGO[(T(k.logo) || {}).code] ? `<img src="${LOGO[T(k.logo).code]}" style="height:${RH - 24}px">` : ''}${esc(k.t || '')}</div>`; });
  return h + `</div>`;
};
VIZ.stamp = (lt, s, it, j, W) => {
  const pv = vPrev(s, j), p = pv && jeq(pv, it) ? 1 : pk(s, it.at, .35, seg(lt, .25, .35)), c = vcol(it.c || 'bad');
  return `<div style="display:inline-block;transform:rotate(${it.rot ?? -6}deg) scale(${(1.8 - .8 * eo(p)).toFixed(3)});opacity:${c01(p * 3)};border:10px solid ${c};border-radius:24px;padding:10px 36px;color:${c};font-size:${it.size || 76}px;font-weight:900;letter-spacing:-2px;background:#ffffffd0;white-space:nowrap;margin:10px 0 0 10px">${esc(it.t || '')}</div>`;
};
VIZ.duo = (lt, s, it, j, W) => {
  const its = it.items || [];
  const pv = vPrev(s, j), po = pv && pv.type === 'duo' ? pv.items || [] : [];
  return `<div class="row" style="gap:24px;flex-wrap:wrap;row-gap:20px;max-width:${Math.min(W, 1100)}px">${its.map((k, i) => { const p = vItemP(s, j, it, k, i, lt, .2), c = vcol(k.c), o = po[i];   /* 10/10: 칸이 많으면 다음 줄로(화면 밖으로 안 나가게) */
    const keepBox = !!(o && (o.icon || 'money') === (k.icon || 'money') && vcol(o.c) === c), fade = `opacity:${c01(p * 1.4).toFixed(3)}`;
    return `<div class="row" style="${k.ghost ? 'visibility:hidden;' : ''}gap:20px;align-items:center;background:#fff;border:4px solid ${c === VN ? '#E3E7EE' : c};border-radius:28px;padding:18px 30px 18px 22px;box-shadow:0 14px 34px rgba(18,22,31,.10);${keepBox ? '' : rise(p, 20)}">${vIcon(k.icon || 'money', c === VN ? ACC : c, 92)}
      <div class="col" style="align-items:flex-start;gap:2px"><div class="num" style="font-size:${k.size || 70}px;font-weight:900;letter-spacing:-2.5px;line-height:1.05;color:${c === VN ? TXT : c};white-space:nowrap;${keepBox && o.v !== k.v ? fade : ''}">${esc(k.v || '')}</div><div style="font-size:32px;font-weight:800;color:#6A7382;white-space:nowrap;${keepBox && o.k !== k.k ? fade : ''}">${esc(k.k || '')}</div></div></div>`; }).join('')}</div>`;
};
/* 10/8 밤 사용자("굳이 왼쪽에 치우쳐 배치할 필요 없다, 가운데로"): 그림 칸을 1180 고정으로 잡지 않고 내용만큼만 → 가운데 맞춤이 실제 그림 기준이 된다 */
function vizW(it, W) {
  if (it.w) return it.w;
  const n = (it.items || []).length;
  if (it.type === 'steps') { const NS = Math.max(it.slots || 0, n); return Math.min(W, NS * (NS <= 2 ? 440 : NS === 3 ? 370 : NS === 4 ? 295 : 236)); }
  if (it.type === 'trend' && it.invert && !it.bars) { const NS = Math.max(n, it.slots || 0); return Math.min(W, 110 + NS * Math.max(250, Math.floor(820 / Math.max(1, NS)))); }   /* 10/13 밤: 순위 꺾은선 */
  if (it.type === 'trend') { const NS = Math.max(n, it.slots || 0); return Math.min(W, NS * 190 + (NS - 1) * (it.gap || 70) + (it.delta || it.dslot ? 340 : 120)); }
  if (it.type === 'split') return Math.min(W, 960);
  if (it.type === 'meter') return Math.min(W, 1000);
  if (it.type === 'branch') return Math.min(W, (it.lw || 380) + 160 + 520);
  return W;
}
function vizHTML(lt, s, W) {
  const vs = [].concat(s.viz || []); if (!vs.length) return '';
  return vs.map((it, j) => (VIZ[it.type] ? VIZ[it.type](lt, s, it, j, vizW(it, W)) : '')).join('');
}
/* profile·speech 에 viz 를 붙인다(원래 장면을 그린 뒤 글 칸 맨 아래에) */
for (const ty of ['profile', 'speech']) {
  const orig = SCENE[ty];
  SCENE[ty] = (lt, s) => {
    /* 10/8 밤 컷 쇼츠(세로): 그림이 사진 옆 좁은 칸에 들어가면 화면 전체가 작아져 글씨가 안 읽힌다 →
       같은 묶음에 그림이 있으면 사진을 조금 줄이고(340×440, 묶음 전체 같은 크기), 그림은 사진·이름 아래 전체 폭 가운데로 */
    if (EP.vertical && !s._vfix) { s._vfix = 1;
      const CHx = (CHAINS[s._cid] || [s._k]).map(j => SC[j]).filter(Boolean);
      if (s.viz || CHx.some(x => x.viz)) { if (s.h == null) s.h = 440; if (s.pw == null) s.pw = 340; } }
    orig(lt, s);
    /* 10/10 컷 쇼츠(세로): 같은 사람 묶음에서 장면마다 내용 높이(기록·그림·말풍선)가 달라 사진·이름이 위아래로 움직였다 →
       2단(.lr)은 내용 높이만큼만(height auto)·위 맞춤, 본문은 위에서부터 쌓는다(setBody) → 사진·이름 자리는 묶음 내내 그대로 */
    if (EP.vertical) { const lr0 = document.querySelector('#body > .lr'); if (lr0) { lr0.style.height = 'auto'; lr0.style.alignItems = 'flex-start';
      /* 기록 칩(.st)은 사진 옆이 아니라 사진·이름 아래 가운데로 — 칩 셋이 사진 옆에 붙으면 묶음 폭이 1355px 이 되어 화면 전체가 0.72배로 작아졌다 */
      const st0 = lr0.querySelector(':scope > .t > .col > .st'); if (st0) { st0.style.width = 'auto'; st0.style.justifyContent = 'center'; st0.style.marginTop = '30px'; st0.style.maxWidth = '1040px'; [...st0.children].forEach(c => c.style.flex = '0 0 auto'); lr0.after(st0);   /* 칩 넷 이상이면 두 줄로(박찬호 칩 넷이 한 줄 1170px → 화면 작아짐) */ } } }
    if (!s.viz) return;
    const col = document.querySelector('#body .lr > .t > .col'); if (!col) return;
    /* 10/13 밤 사용자("너무 오른쪽으로 치우쳐 · 조율해 줘"): 사진/로고 칸 + 그림이 화면 폭(1780)을 넘으면 가운데 맞춤이 안 돼 오른쪽 끝에 붙었다 → 그림 폭을 남은 자리만큼으로 줄인다 */
    let W = s.vw || 1180;
    if (!EP.vertical) { const lrA = col.closest('.lr'), phA = lrA && lrA.firstElementChild; if (phA && phA !== col.closest('.t')) W = Math.min(W, Math.max(720, 1760 - phA.offsetWidth - 70)); }
    const d = document.createElement('div'); d.className = 'vzw'; d.style.cssText = `display:flex;flex-direction:column;gap:22px;align-items:flex-start;margin-top:4px`;
    d.innerHTML = vizHTML(lt, s, W);
    const vfOf = (x, d) => { if (x.vizFirst != null) return !!x.vizFirst; const P = x._prev;
      if (d < 30 && P && P._cid === x._cid && ['profile', 'speech'].includes(P.type)) return P.viz ? (!(P.stats || []).length || vfOf(P, d + 1)) : false;
      return !(x.stats || []).length; };
    const vf = vfOf(s, 0);
    if (EP.vertical) { const lr = col.closest('.lr'); lr.style.height = 'auto'; d.style.alignItems = 'center'; d.style.marginTop = '30px';
      /* 10/10: 앞 장면이 그림을 먼저 보여 줬으면 새 기록(.st)은 그림 아래로(컷11 '마감' 칩이 끼어들어 타임라인이 142px 내려갔음) */
      const stB = vf ? lr.parentNode.querySelector(':scope > .st') : null; stB ? stB.before(d) : lr.parentNode.appendChild(d); return; }
    /* 10/10 사용자 "4위 텍스트 밑으로 4년 100억이 들어가게": 묶음에서 그림이 기록(stats)보다 먼저 나왔으면 그림은 그 자리 그대로, 기록은 그림 아래에 */
    /* 바로 앞 장면(같은 묶음)이 그림을 먼저 보여 줬으면(그림만 있었거나 그림이 위였으면) 그림을 위에 그대로, 앞 장면이 기록만 있었으면 기록을 그대로 두고 그림을 아래에 */
    const stEl = vf ? col.querySelector(':scope > .st') : null;
    stEl ? col.insertBefore(d, stEl) : col.appendChild(d);
    col.style.overflow = 'visible';   /* 10/8 밤: 높이는 그대로(글 칸이 커지면 이름이 위로 움직임) — 넘치는 만큼은 본문 아래 빈칸으로 */
  };
}

/* slotboard: 팀 외국인 자리판 — slots:[{img|sil, name, pos, money, tag, tc, tagAt, at, x, xAt, note}], team, title, text */
SCENE.slotboard = (lt, s) => {
  const sl = s.slots || [], n = sl.length, K = !!(s._chain && s._prev && s._prev.type === 'slotboard'), PS = K ? s._prev.slots || [] : [];
  const CW = n >= 5 ? 320 : n === 4 ? 400 : 460, D = n >= 5 ? 210 : n === 4 ? 250 : 280, tt = s.team ? T(s.team) : null, anyTag = sl.some(k => k.tag) || PS.some(k => k.tag) || (s._next && s._next.type === 'slotboard' && (s._next.slots || []).some(k => k.tag));
  let h = s.title ? `<div class="row" style="gap:20px;align-items:center;margin-bottom:30px;${K && s._prev.title === s.title ? '' : pop(seg(lt, 0, .4))}">${tt && LOGO[tt.code] ? `<img src="${LOGO[tt.code]}" style="height:110px">` : ''}<div class="title" style="font-size:66px;font-weight:900">${br(s.title)}</div></div>` : '';
  h += `<div class="row" style="gap:28px;align-items:flex-start;justify-content:center">` + sl.map((k, i) => {
    const old = PS.find(o => o.name === k.name && o.img === k.img && o.pos === k.pos), p = old ? 1 : pk(s, k.at, .5, seg(lt, .15 + i * .15, .5));
    const tp = k.tag ? (old && old.tag === k.tag ? 1 : pk(s, k.tagAt, .35, seg(lt, .6 + i * .2, .35))) : 0, xp = k.x ? (old && old.x ? 1 : pk(s, k.xAt, .4, seg(lt, .8, .4))) : 0;
    const src = k.img ? photoSrc(k.img) : '', tc = vcol(k.tc || 'good');
    /* 10/8 밤 사용자("왜 비어있어?"): 사람 실루엣(사진 빠진 것처럼 보임) 대신 — 실제 선수는 사진, 아직 안 정해진 자리(tbd)는 점선 원 + 물음표 */
    const face = src ? `<img src="${src}" style="width:100%;height:100%;object-fit:cover;object-position:${esc(k.focus || '50% 8%')};filter:grayscale(${(xp * .9).toFixed(2)})">`
      : `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:${Math.round(D * .52)}px;font-weight:900;color:${ACC};line-height:1;padding-bottom:${Math.round(D * .04)}px">?</div>`;
    const ip = k.inset ? (old && old.inset && old.inset.img === k.inset.img ? 1 : pk(s, k.insetAt, .4, seg(lt, .9, .4))) : 0, IS = Math.round(D * .44);
    return `<div class="col" style="width:${CW}px;align-items:center;gap:12px;${rise(p, 30)}">
      <div class="badge" style="background:${k.pc || VN};font-size:36px;padding:8px 24px;white-space:nowrap">${esc(k.pos || '')}</div>
      <div style="position:relative;width:${D}px;height:${D}px">
        <div style="position:absolute;inset:0;border-radius:50%;overflow:hidden;${src ? 'background:#E9EDF3;border:6px solid #fff;' : `background:${ACC}12;border:6px dashed ${ACC};`}box-shadow:0 10px 26px rgba(18,22,31,.16);display:flex;justify-content:center">${face}</div>
        ${k.inset ? `<div style="position:absolute;right:${-Math.round(D * .16)}px;top:${-Math.round(D * .06)}px;width:${IS}px;height:${IS}px;border-radius:50%;overflow:hidden;border:5px solid #fff;box-shadow:0 8px 20px rgba(18,22,31,.22);background:#E9EDF3;${pop(ip)}"><img src="${photoSrc(k.inset.img)}" style="width:100%;height:100%;object-fit:cover"></div>` : ''}
        ${k.x ? `<svg style="position:absolute;inset:0;overflow:visible" viewBox="0 0 100 100"><path d="M22,22 L${(22 + 56 * eo(xp)).toFixed(1)},${(22 + 56 * eo(xp)).toFixed(1)} M78,22 L${(78 - 56 * eo(c01(xp * 2 - 1))).toFixed(1)},${(22 + 56 * eo(c01(xp * 2 - 1))).toFixed(1)}" stroke="${VB}" stroke-width="9" stroke-linecap="round"/></svg>` : ''}
        ${k.tag ? `<div style="position:absolute;left:50%;bottom:-18px;transform:translateX(-50%) rotate(-6deg) scale(${(1.7 - .7 * eo(tp)).toFixed(3)});opacity:${c01(tp * 3)};border:6px solid ${tc};border-radius:16px;padding:4px 18px;background:#fff;color:${tc};font-size:40px;font-weight:900;white-space:nowrap">${esc(k.tag)}</div>` : ''}</div>
      <div style="font-size:${Math.max(...String(k.name || '').split('\n').map(x => x.length)) > 6 ? 46 : 56}px;font-weight:900;letter-spacing:-1.5px;line-height:1.15;margin-top:${anyTag ? 40 : 14}px;white-space:nowrap;text-align:center">${br(k.name || '')}</div>
      ${k.money ? `<div style="font-size:38px;font-weight:800;color:#6A7382;white-space:nowrap">${esc(k.money)}</div>` : ''}
      ${k.note ? `<div style="font-size:36px;font-weight:800;color:${vcol(k.nc)};text-align:center;line-height:1.2;${pop(pk(s, k.noteAt, .4, 1))}">${br(k.note)}</div>` : ''}</div>`;
  }).join('') + `</div>`;
  /* 10/8 밤: 가운데 파란 글 대신 묶음 괄호 — bracket:{a, b(자리 번호), label, at, c}. 묶음 안에 괄호가 있으면 자리를 늘 비워 둔다 */
  const BK = (CHAINS[s._cid] || []).map(j => SC[j]).find(x => x && x.type === 'slotboard' && x.bracket);
  if (s.bracket || BK) {
    const bk = s.bracket || BK.bracket, RW = n * CW + (n - 1) * 28, x1 = bk.a * (CW + 28) + 40, x2 = bk.b * (CW + 28) + CW - 40, c = vcol(bk.c || 'bad');
    const bp = !s.bracket ? 0 : K && s._prev.bracket && s._prev.bracket.label === bk.label ? 1 : pk(s, bk.at, .45, seg(lt, 1, .45));
    h += `<div style="position:relative;width:${RW}px;height:118px;margin-top:14px;${s.bracket ? '' : 'visibility:hidden'}">
      <div style="position:absolute;left:${x1}px;width:${x2 - x1}px;top:0;height:36px;border:6px solid ${c};border-top:none;border-radius:0 0 22px 22px;opacity:${c01(bp * 2).toFixed(3)};clip-path:inset(0 ${((1 - eo(bp)) * 50).toFixed(1)}% 0 ${((1 - eo(bp)) * 50).toFixed(1)}%)"></div>
      <div class="badge" style="position:absolute;left:${(x1 + x2) / 2}px;top:52px;translate:-50% 0;background:${c};font-size:40px;padding:10px 30px;white-space:nowrap;${pop(c01(bp * 1.6 - .4))}">${esc(bk.label || '')}</div></div>`;
  }
  const slot = s.textSlot ?? ((CHAINS[s._cid] || []).some(j => SC[j] && SC[j].type === 'slotboard' && SC[j].text) || s.text ? 1 : 0);
  const TS = s.text ? (s.size || 60) : (((CHAINS[s._cid] || []).map(j => SC[j]).find(x => x && x.text) || {}).size || 60);
  if (slot) h += `<div class="big gold" style="margin-top:34px;min-height:${Math.round(TS * 1.3)}px;font-size:${TS}px;${s.text ? (K && s._prev.text === s.text ? '' : pop(pk(s, s.textAt, .5, seg(lt, 1, .5)))) : 'visibility:hidden'}">${br(s.text || '·')}</div>`;
  wrapC(h);
};

/* debate: 팬 커뮤니티 양쪽 주장 — left/right:{label, t, c, at} */
SCENE.debate = (lt, s) => {
  const side = (k, i) => { const p = pk(s, k.at, .5, seg(lt, .2 + i * .5, .5)), c = vcol(k.c || (i ? 'bad' : 'good'));
    return `<div class="col" style="width:${EP.vertical ? 470 : 700}px;background:${c}10;border:5px solid ${c};border-radius:36px;padding:28px 30px 34px;gap:18px;align-items:center;${pop(p)}">
      <div class="badge" style="background:${c};font-size:44px;padding:10px 34px">${esc(k.label || '')}</div>
      <div class="row" style="gap:6px">${Array.from({ length: 5 }, (_, m) => `<div style="width:56px;height:84px;${pop(c01(p * 3 - m * .2))}">${ICON.person(c)}</div>`).join('')}</div>
      <div style="font-size:${k.size || 54}px;font-weight:900;letter-spacing:-2px;line-height:1.24;text-align:center;color:${TXT}">${br(k.t || '')}</div></div>`; };
  let h = titleH(lt, s, 56, 30);
  h += `<div class="row" style="gap:40px;align-items:center">${side(s.left || {}, 0)}<div style="width:120px;height:120px;border-radius:50%;background:${TXT};color:#fff;font-size:48px;font-weight:900;display:flex;align-items:center;justify-content:center;${pop(seg(lt, .5, .4))}">VS</div>${side(s.right || {}, 1)}</div>`;
  wrapC(h);
};

/* allfa: 10개 구단 외국인 선수(아시아쿼터 포함) 얼굴 원 + 작은 이름 — teams:[{team, players:[{img, name}]}], title.
   10/8 밤 사용자: "모든 외국인(아시아쿼터 포함)의 프로필 사진을 동그랗게 넣고 프로필 사진 밑에 이름을 작게 써서 나열". 구단 순서대로 왼쪽부터 차례로 뜬다 */
SCENE.allfa = (lt, s) => {
  const tms = s.teams || [], n = tms.length || 1, CW = Math.floor((1780 - (n - 1) * 6) / n), D = s.d || Math.min(112, CW - 56);
  let h = s.title ? `<div class="title" style="font-size:52px;font-weight:900;margin-bottom:22px;${pop(seg(lt, 0, .4))}">${esc(s.title)}</div>` : '';
  h += `<div class="row" style="gap:6px;align-items:flex-start;justify-content:center">` + tms.map((tm, i) => {
    const t = T(tm.team), p0 = seg(lt, .15 + i * .1, .45);
    return `<div class="col" style="width:${CW}px;align-items:center;gap:8px">
      <div style="height:62px;display:flex;align-items:center;${pop(p0)}">${LOGO[t.code] ? `<img src="${LOGO[t.code]}" style="height:58px;max-width:${CW - 20}px;object-fit:contain">` : ''}</div>
      ${(tm.players || []).map((pl, j) => `<div class="col" style="align-items:center;gap:4px;${pop(c01(p0 * 1.5 - .12 - j * .1))}">
        <div style="width:${D}px;height:${D}px;border-radius:50%;overflow:hidden;border:4px solid #fff;box-shadow:0 6px 16px rgba(18,22,31,.16);background:#E9EDF3"><img src="${photoSrc(pl.img)}" style="width:100%;height:100%;object-fit:cover"></div>
        <div style="font-size:27px;font-weight:800;letter-spacing:-1px;white-space:nowrap;color:${TXT}">${esc(pl.name || '')}</div></div>`).join('')}</div>`;
  }).join('') + `</div>`;
  wrapC(h);
};
MOTION.allfa = s => .6 + (s.teams || []).length * .1 + .6;
