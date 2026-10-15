/* @@HW1014 */
/* 10/14 롱폼⑭ 한화 감독 잔혹사 — 새 장면 2종.
   yearcount: 훅. 구단 로고 + 연도 숫자가 from 에서 to 까지 굴러 올라가고(countAt~countEnd 호흡), stamp 가 stampAt 호흡에 쾅.
     {"type":"yearcount","team":"한화","from":2006,"to":2026,"countAt":0,"countEnd":2,"stamp":"감독 재계약 0번","stampAt":3,"top":"마지막 재계약 2006년 11월"}
   yearline: 연도 축. items 의 로고(또는 별)가 그 해 자리로 떨어진다(at 호흡). 같은 해 근처는 위로 쌓인다.
     {"type":"yearline","from":2005,"to":2027,"ticks":[...],"items":[{"y":2025.9,"team":"LG","label":"2025년 11월","at":3,"c":"good"}],
      "gaps":[{"a":2006.9,"b":2026.8,"label":"감독 재계약 없음","at":1}], "brace":{"a":2006.85,"b":2019.8,"label":"13년 가까이","at":2},
      "dots":[{"y":2014.8,"label":"감독 · 윗선","at":1,"big":false}]}
     cont(같은 chain)면 앞 장면에 있던 로고·점은 그대로, 새것만 떨어진다. */
(() => {
  const V = () => !!EP.vertical;
  SCENE.yearcount = (lt, s) => {
    const t = T(s.team || '한화'), y0 = s.from || 2006, y1 = s.to || 2026;
    const T0 = (EP.segT || [])[s.startLine] || [], a = T0[Math.floor(s.countAt ?? 0)], b = T0[Math.floor(s.countEnd ?? 2)];   /* countAt~countEnd 호흡 동안 숫자가 오른다 */
    const q = eo(a == null || b == null || b <= a ? seg(lt, .2, 2.4) : c01((NOW - a) / (b - a)));
    const yr = Math.round(y0 + (y1 - y0) * q), LG = V() ? 300 : 380, FS = V() ? 230 : 300;
    const ps = pk(s, s.stampAt ?? 3, .35, seg(lt, 3, .35));
    let h = s.top ? `<div class="badge" style="background:#12161F;font-size:${V() ? 40 : 44}px;padding:10px 30px;margin-bottom:26px;${pop(seg(lt, 0, .4))}">${esc(s.top)}</div>` : '';
    h += `<div class="row" style="gap:${V() ? 40 : 70}px;align-items:center;${rise(seg(lt, 0, .45), 26)}">
      ${LOGO[t.code] ? `<div style="width:${LG}px;height:${LG}px;display:flex;align-items:center;justify-content:center"><img src="${LOGO[t.code]}" style="width:100%;height:100%;object-fit:contain"></div>` : ''}
      <div class="col" style="align-items:center;gap:6px"><div class="num" style="font-size:${FS}px;font-weight:900;letter-spacing:-10px;line-height:1;color:${q >= 1 ? RED : TXT}">${yr}</div>
      <div style="font-size:${V() ? 40 : 46}px;font-weight:900;color:${GRAY};letter-spacing:-1px">${esc(s.sub || '')}</div></div></div>`;
    if (s.stamp) h += `<div style="margin-top:30px;display:inline-block;border:10px solid ${RED};color:${RED};border-radius:24px;padding:10px 40px;font-size:${V() ? 84 : 104}px;font-weight:900;letter-spacing:-3px;white-space:nowrap;transform:rotate(-6deg) scale(${(1 + 1.2 * (1 - eo(ps))).toFixed(3)});opacity:${c01(ps * 2.5)}">${esc(s.stamp)}</div>`;
    wrapC(h);
  };

  SCENE.yearline = (lt, s) => {
    /* 자리는 같은 chain 의 모든 장면 항목을 합쳐 한 번에 정한다 → 장면이 바뀌어도 카드·축이 안 움직임 */
    const Y0 = s.from || 2005, Y1 = s.to || 2027, W = V() ? 980 : 1640, PADX = 50, LG = V() ? 88 : 140, GX = 16;
    const x = y => PADX + (y - Y0) / (Y1 - Y0) * (W - PADX * 2);
    const sib = s.chain ? (EP.scenes || []).filter(z => z.type === 'yearline' && z.chain === s.chain) : [s];
    const tms = it => it.star ? ['★'] : (it.teams || [it.team || it.label]);
    const key = it => tms(it).join('+') + '@' + it.y;
    const U = new Map(); sib.forEach(z => (z.items || []).forEach(it => { if (!U.has(key(it))) U.set(key(it), it); }));
    const all = [...U.values()].sort((a, b) => b.y - a.y);
    const LBLW = V() ? 150 : 244, CH = LG + 62;
    const wOf = it => Math.max(tms(it).length * LG + (tms(it).length - 1) * 8 + 16, LBLW);
    const NR = all.length > 1 ? 2 : all.length;               /* 줄 수: 항목 2개 이상이면 두 줄 */
    const pos = {}; for (let r = 0; r < NR; r++) {            /* 줄마다 겹치지 않게 옆으로 밀기(순서 유지, 이동 최소) */
      const L = all.filter((it, i) => (it.row != null ? it.row : i % NR) === r).map(it => ({ k: key(it), c: x(it.y), w: wOf(it) })).sort((a, b) => a.c - b.c);
      const cl = []; L.forEach(o => { cl.push({ it: [o], W: o.w, s: o.c - o.w / 2 });
        while (cl.length > 1) { const A = cl[cl.length - 2], B = cl[cl.length - 1]; if (A.s + A.W + GX <= B.s) break;
          const it = A.it.concat(B.it); let off = 0; const of = it.map(q => { const m = off + q.w / 2; off += q.w + GX; return m; });
          cl.splice(cl.length - 2, 2, { it, W: off - GX, s: it.reduce((a, q, k) => a + q.c - of[k], 0) / it.length }); } });
      for (let i = cl.length - 1; i >= 0; i--) { const lim = i === cl.length - 1 ? W : cl[i + 1].s - GX; if (cl[i].s + cl[i].W > lim) cl[i].s = lim - cl[i].W; }
      for (let i = 0; i < cl.length; i++) { const lim = i === 0 ? 0 : cl[i - 1].s + cl[i - 1].W + GX; if (cl[i].s < lim) cl[i].s = lim; }
      cl.forEach(C => { let o = C.s; C.it.forEach(q => { pos[q.k] = { p: o + q.w / 2, w: q.w, r }; o += q.w + GX; }); });
    }
    const anyBrace = sib.some(z => z.brace), anyDot = sib.some(z => (z.dots || []).length), anyGap = sib.some(z => (z.gaps || []).length);
    const AX = NR ? 20 + NR * CH + (NR - 1) * 26 + 70 : (anyDot ? 190 : 150), H = AX + 104 + (anyBrace ? 96 : 0);
    const P = s._same ? s._prev : null, had = new Set(P ? (P.items || []).map(key) : []), hadD = new Set(P ? (P.dots || []).map(d => d.y + d.label) : []), hadG = new Set(P ? (P.gaps || []).map(g => g.label) : []);
    let h = titleH(lt, s, V() ? 48 : 52, 18, s._same && P && P.title === s.title);
    let g = `<div style="position:absolute;left:0;top:${AX}px;width:${W}px;height:8px;border-radius:4px;background:#12161F"></div>`;
    const ticks = s.ticks || []; for (let y = Y0; y <= Y1; y++) {
      const big = ticks.includes(y);
      g += `<div style="position:absolute;left:${x(y) - 2}px;top:${AX - (big ? 12 : 6)}px;width:4px;height:${big ? 32 : 20}px;background:${big ? '#12161F' : '#AAB2BF'}"></div>`;
      if (big) g += `<div class="num" style="position:absolute;left:${x(y)}px;top:${AX + 50}px;translate:-50% 0;font-size:${V() ? 30 : 34}px;font-weight:900;color:${GRAY}">${y}</div>`;
    }
    (s.gaps || []).forEach(gp => { const q = hadG.has(gp.label) ? 1 : pk(s, gp.at, .8, seg(lt, .3, .8)), w = (x(gp.b) - x(gp.a)) * eo(q);
      g += `<div style="position:absolute;left:${x(gp.a)}px;top:${AX - 62}px;width:${w.toFixed(1)}px;height:42px;border-radius:21px;border:4px dashed ${gp.c === 'bad' ? RED : '#AAB2BF'};background:${gp.c === 'bad' ? '#FCE7E8' : '#F1F3F7'}"></div>`;
      if (gp.label) g += `<div style="position:absolute;left:${(x(gp.a) + x(gp.b)) / 2}px;top:${AX - 140}px;translate:-50% 0;font-size:${V() ? 44 : 56}px;font-weight:900;color:${gp.c === 'bad' ? RED : GRAY};white-space:nowrap;opacity:${c01((q - .6) * 3)}">${esc(gp.label)}</div>`; });
    (s.dots || []).forEach(d => { const q = hadD.has(d.y + d.label) ? (P && (P.dots || []).find(z => z.y === d.y && z.label === d.label && !!z.big === !!d.big) ? 1 : pk(s, d.at, .4, .4)) : pk(s, d.at, .4, seg(lt, .3, .4)), R = d.big ? 40 : 28, cc = d.c === 'bad' ? RED : '#E8A100';
      g += `<div style="position:absolute;left:${x(d.y) - R}px;top:${AX + 4 - R}px;width:${R * 2}px;height:${R * 2}px;border-radius:50%;background:${cc};border:6px solid #fff;box-shadow:0 6px 16px rgba(18,22,31,.25);${pop(q)}"></div>`;
      if (d.label) g += `<div class="badge" style="position:absolute;left:${x(d.y)}px;top:${AX - R - 14}px;translate:-50% -100%;background:${cc};font-size:${d.big ? 40 : 36}px;line-height:1.15;padding:8px 18px;white-space:nowrap;text-align:center;${pop(q)}">${br(d.label)}</div>`; });
    let lines = '', cards = '';
    all.forEach(it => { const k = key(it), ps = pos[k], cur = (s.items || []).find(z => key(z) === k);
      /* 10/14 롱폼⑭ 검수(빈 축 5초): s.ghost = 아직 안 나온 구단 자리를 흐린 회색 로고로 먼저 보여 주고, 말할 때 진짜 카드가 떨어지며 회색은 사라진다 */
      if (s.ghost && !had.has(k)) { const gq = cur ? pk(s, cur.at, .55, 0) : 0, gop = .28 * eo(seg(lt, .15, .6)) * (1 - c01(gq * 3));
        if (gop > .005) { const gtop = AX - 70 - CH - ps.r * (CH + 26);
          const glogos = tms(it).map(tn => LOGO[T(tn).code] ? `<img src="${LOGO[T(tn).code]}" style="width:${LG}px;height:${LG}px;object-fit:contain;filter:grayscale(1)">` : '').join('');
          cards += `<div style="position:absolute;left:${ps.p}px;top:${gtop}px;translate:-50% 0;width:${ps.w}px;display:flex;justify-content:center;opacity:${gop.toFixed(3)}"><div style="display:flex;gap:8px;padding:4px 8px;border-radius:20px;border:5px dashed #AAB2BF">${glogos}</div></div>`; } }
      if (!cur) return;
      const old = had.has(k), q = old ? 1 : pk(s, cur.at, .55, seg(lt, .3, .55)), c = x(it.y);
      const col = cur.c === 'bad' ? RED : cur.c === 'good' ? GREEN : cur.c === 'gold' ? '#E8A100' : '#3B4A63';
      const top = AX - 70 - CH - ps.r * (CH + 26), dy = (1 - eo(q)) * -140, op = c01(q * 2), lq = c01((q - .6) * 2.5);
      lines += `<line x1="${ps.p}" y1="${top + CH}" x2="${c}" y2="${AX - 4}" stroke="${col}" stroke-width="4" stroke-linecap="round" opacity="${(lq * .7).toFixed(2)}"/>
        <circle cx="${c}" cy="${AX + 4}" r="${(11 * lq).toFixed(1)}" fill="${col}" stroke="#fff" stroke-width="4"/>`;
      const logos = tms(it).map(tn => tn === '★' ? `<div style="width:${LG}px;height:${LG}px;display:flex;align-items:center;justify-content:center;font-size:${LG * .9}px;line-height:1;color:#E8A100">★</div>`
        : (LOGO[T(tn).code] ? `<img src="${LOGO[T(tn).code]}" style="width:${LG}px;height:${LG}px;object-fit:contain">` : '')).join('');
      cards += `<div style="position:absolute;left:${ps.p}px;top:${top}px;translate:-50% 0;width:${ps.w}px;height:${CH}px;display:flex;flex-direction:column;align-items:center;gap:6px;opacity:${op};transform:translateY(${dy.toFixed(1)}px)">
        <div style="display:flex;gap:8px;padding:4px 8px;background:#fff;border-radius:20px;border:5px solid ${col};box-shadow:0 8px 20px rgba(18,22,31,.18)">${logos}</div>
        ${cur.label ? `<div class="badge" style="background:${col};font-size:${V() ? 30 : 38}px;padding:4px 16px;white-space:nowrap">${esc(cur.label)}</div>` : ''}</div>`; });
    g += `<svg width="${W}" height="${H}" style="position:absolute;left:0;top:0;overflow:visible">${lines}</svg>` + cards;
    if (s.brace) { const b = s.brace, q = P && P.brace && P.brace.label === b.label ? 1 : pk(s, b.at, .5, seg(lt, .6, .5));
      g += `<div style="position:absolute;left:${x(b.a)}px;top:${AX + 98}px;width:${x(b.b) - x(b.a)}px;height:26px;border:6px solid ${RED};border-top:none;border-radius:0 0 16px 16px;${pop(q)}"></div>
        <div class="badge" style="position:absolute;left:${(x(b.a) + x(b.b)) / 2}px;top:${AX + 132}px;translate:-50% 0;background:${RED};font-size:${V() ? 40 : 46}px;padding:8px 26px;white-space:nowrap;${pop(q)}">${esc(b.label)}</div>`; }
    h += `<div style="position:relative;width:${W}px;height:${H + (anyBrace ? 30 : 0)}px">${g}</div>`;
    if (s.text) h += `<div class="big gold" style="margin-top:10px;font-size:${s.size || 56}px;${pop(pk(s, s.textAt, .5, 1))}">${br(s.text)}</div>`;
    wrapC(h);
  };
})();
/* @@HW1014END */
