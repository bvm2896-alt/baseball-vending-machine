/* @@SCORE1101 11/1 롱폼㉟ — 사용자 "요소 엄청 많이 고려해서 분석가처럼". 항목별 점수판(줄다리기).
   scorecard: {title, l:'KT', r:'삼성', rows:[{k, w:'L'|'R', at}], tally:{at}, base:{v, at}, res:{v, at}}
   - 줄은 말하는 순간 뜬다(at). 자리는 처음부터 잡아 두어 줄이 밀리지 않는다.
   - 가운데 항목 이름, 앞선 쪽으로 구단 색 막대가 뻗는다. 같은 chain 의 cont 장면이면 이미 뜬 줄은 그대로.
   - tally(몇 대 몇)·base→res(확률)는 말하는 순간에만 뜬다. */
(() => {
  const e3 = x => 1 - Math.pow(1 - c01(x), 3);
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  SCENE.scorecard = (lt, s) => {
    const K = s._same, rows = s.rows || [], n = rows.length, W = 1640, RH = 74, LW = 420;
    const cl = TC_(s.l), cr = TC_(s.r);
    const pr = rows.map(x => AT(s, x.at, .55, 0));
    const tq = s.tally ? AT(s, s.tally.at, .5, 0) : 0;
    const nl = rows.filter((x, i) => x.w === 'L' && pr[i] > .5).length, nr = rows.filter((x, i) => x.w === 'R' && pr[i] > .5).length;
    let h = '';
    const head = `<div class="row" style="width:${W}px;justify-content:space-between;align-items:center;margin-bottom:10px">
      <div style="width:${LW}px;text-align:left;font-size:96px;font-weight:900;letter-spacing:-2px;color:${cl}">${esc(s.l)}</div>
      <div class="col" style="align-items:center;gap:0"><div style="font-size:44px;font-weight:900;color:#5F6B80;letter-spacing:-1px;white-space:nowrap">${esc(s.title || '')}</div>
        <div class="num" style="height:84px;line-height:84px;font-size:80px;font-weight:900;letter-spacing:-2px;color:#12161F;opacity:${c01(tq * 1.6).toFixed(3)};transform:scale(${(1.25 - .25 * e3(tq)).toFixed(3)})">${nl}<span style="color:#9AA3B2;margin:0 18px">:</span>${nr}</div></div>
      <div style="width:${LW}px;text-align:right;font-size:96px;font-weight:900;letter-spacing:-2px;color:${cr}">${esc(s.r)}</div></div>`;
    const CW = 780, PH = 92;
    const col_ = side => rows.map((x, i) => [x, i]).filter(([x]) => x.w === side).map(([x, i]) => {
      const p = pr[i], c = side === 'L' ? cl : cr;
      return `<div style="width:${CW}px;height:${PH - 14}px;margin-bottom:14px;border-radius:22px;background:#fff;border:5px solid ${p > .5 ? c : LINE};box-shadow:0 8px 20px rgba(18,22,31,.08);display:flex;align-items:center;gap:22px;padding:0 30px;box-sizing:border-box;flex-direction:${side === 'L' ? 'row' : 'row-reverse'};opacity:${c01(p * 2).toFixed(3)};transform:translateX(${((1 - e3(p)) * (side === 'L' ? -60 : 60)).toFixed(1)}px)">
        <div style="flex:0 0 auto;width:48px;height:48px;border-radius:50%;background:${c};color:#fff;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:900">✓</div>
        <div style="font-size:52px;font-weight:900;letter-spacing:-1.5px;white-space:nowrap;color:#12161F">${esc(x.k)}</div></div>`; }).join('');
    const body = `<div class="row" style="width:${W}px;justify-content:space-between;align-items:flex-start;gap:40px">
      <div class="col" style="align-items:flex-start">${col_('L')}</div><div class="col" style="align-items:flex-end">${col_('R')}</div></div>`;
    h += `<div class="col" style="align-items:center;gap:4px;${K ? '' : rise(seg(lt, 0, .45), 24)}">${head}${body}</div>`;
    if (s.base && s.res) {
      const bq = AT(s, s.base.at, .5, 0), rq = AT(s, s.res.at, .6, 0), d = (+s.res.v) - (+s.base.v), v = (+s.base.v) + d * e3(rq), dc = d >= 0 ? GREEN : RED;
      h += `<div class="row" style="margin-top:8px;gap:30px;align-items:center;height:120px;opacity:${c01(bq * 2).toFixed(3)}">
        <div class="num" style="font-size:64px;font-weight:900;color:#9AA3B2">${(+s.base.v).toFixed(0)}%</div>
        <div style="font-size:54px;font-weight:900;color:${dc};opacity:${c01(rq * 2).toFixed(3)}">${d >= 0 ? '+' : '−'}${Math.abs(d)}</div>
        <div style="font-size:54px;font-weight:900;color:#9AA3B2;opacity:${c01(rq * 2).toFixed(3)}">→</div>
        <div class="num" style="font-size:110px;font-weight:900;letter-spacing:-3px;color:${cl};opacity:${c01(rq * 2).toFixed(3)}">${v.toFixed(0)}%</div></div>`;
    }
    wrapC(h);
  };
  Object.assign(MOTION, { scorecard: s => .6 + (s.rows || []).length * .2 });
})();
/* @@SCORE1101END */
