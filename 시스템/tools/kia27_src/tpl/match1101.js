/* @@MATCH1101 11/1 롱폼㉟ — 분석가 검수 "±2점 대신 1~7차전 선발 매치업 표로". 차전별 선발 맞대기 + 판정 칩 → 7전 4선승 확률.
   matchtbl: {l:'KT', r:'삼성', title, rows:[{g:'1차전', v:'수원', L:{name, img}, R:{name, img}, verdict:'L'|'E'|'R', at, vAt}], res:{t, v, at}}
   - 줄은 at 에 뜨고, 판정 칩은 vAt(없으면 at)에 찍힌다. 같은 chain 의 cont 장면이면 이미 뜬 줄·칩은 그대로. */
(() => {
  const e3 = x => 1 - Math.pow(1 - c01(x), 3);
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  const AV = (x, side, col) => {
    const src = x && x.img ? photoSrc(x.img) : null;
    const pic = src ? `<div style="width:76px;height:76px;border-radius:50%;overflow:hidden;flex:0 0 auto;border:4px solid ${col};box-sizing:border-box;background:#E9EDF3"><img src="${src}" style="width:100%;height:100%;object-fit:cover;object-position:50% 15%"></div>`
                    : `<div style="width:76px;height:76px;border-radius:50%;flex:0 0 auto;border:4px dashed #B8C0CC;box-sizing:border-box"></div>`;
    return `<div style="display:flex;align-items:center;gap:16px;flex-direction:${side === 'L' ? 'row' : 'row-reverse'};width:430px">${pic}
      <div style="font-size:50px;font-weight:900;letter-spacing:-1.5px;white-space:nowrap;color:${x && x.img ? '#12161F' : '#8A93A3'}">${esc((x && x.name) || '')}</div></div>`;
  };
  SCENE.matchtbl = (lt, s) => {
    const K = s._same, rows = s.rows || [], cl = TC_(s.l), cr = TC_(s.r), RH = 96, W = 1680;
    let h = `<div class="row" style="width:${W}px;justify-content:space-between;align-items:flex-end;margin-bottom:8px">
      <div style="width:520px;text-align:left;font-size:80px;font-weight:900;letter-spacing:-2px;color:${cl}">${esc(s.l)}</div>
      <div style="font-size:44px;font-weight:900;color:#5F6B80;letter-spacing:-1px;white-space:nowrap;padding-bottom:12px">${esc(s.title || '')}</div>
      <div style="width:520px;text-align:right;font-size:80px;font-weight:900;letter-spacing:-2px;color:${cr}">${esc(s.r)}</div></div>`;
    h += rows.map(x => {
      const p = AT(s, x.at, .5, 0), q = AT(s, x.vAt != null ? x.vAt : x.at, .45, 0);
      const vc = x.pct != null ? (x.pct > 50 ? cl : x.pct < 50 ? cr : '#8A93A3') : x.verdict === 'L' ? cl : x.verdict === 'R' ? cr : '#8A93A3';
      const vt = x.pct != null ? `KT ${x.pct}%` : x.verdict === 'L' ? `${s.l} 우세` : x.verdict === 'R' ? `${s.r} 우세` : '팽팽';   /* 11/1 차전별 KT 승리 확률(50 미만이면 상대 색) */
      return `<div style="position:relative;width:${W}px;height:${RH - 10}px;margin-bottom:10px;border-radius:22px;background:#fff;border:4px solid ${q > .5 ? vc : LINE};box-shadow:0 6px 16px rgba(18,22,31,.07);display:flex;align-items:center;justify-content:space-between;padding:0 26px;box-sizing:border-box;${MK.css.slide(p, 'l', 70)}">
        ${AV(x.L, 'L', cl)}
        <div style="display:flex;align-items:center;gap:22px">
          <div style="width:200px;text-align:center"><div style="font-size:46px;font-weight:900;letter-spacing:-1px;white-space:nowrap">${esc(x.g)}</div><div style="font-size:28px;font-weight:800;color:#8A93A3;white-space:nowrap">${esc(x.v || '')}</div></div>
          <div style="width:240px;height:64px;border-radius:32px;background:${vc};color:#fff;display:flex;align-items:center;justify-content:center;font-size:40px;font-weight:900;white-space:nowrap;${MK.css.springPop(q, .55)}">${esc(vt)}</div></div>
        ${AV(x.R, 'R', cr)}</div>`; }).join('');
    if (s.res) {
      const rq = AT(s, s.res.at, .6, 0), v = (+s.res.v) * e3(rq);
      h += `<div class="row" style="margin-top:6px;gap:26px;align-items:center;height:110px;opacity:${c01(rq * 2).toFixed(3)}">
        <div style="font-size:46px;font-weight:900;color:#5F6B80;white-space:nowrap">${esc(s.res.t || '')}</div>
        <div class="num" style="font-size:104px;font-weight:900;letter-spacing:-3px;color:${cl}">${v.toFixed(s.res.dec ?? 1)}<span style="font-size:58px">%</span></div></div>`;
    }
    wrapC(`<div class="col" style="align-items:center;${K ? '' : rise(seg(lt, 0, .45), 24)}">${h}</div>`);
  };
  Object.assign(MOTION, { matchtbl: s => .6 + (s.rows || []).length * .15 });
})();
/* @@MATCH1101END */
