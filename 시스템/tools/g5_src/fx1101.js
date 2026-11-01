/* @@FX1101 11/1 롱폼㊱ — 움직임 사전 #16 흔들림(부정 수치 1회). errs: 실책·부정 기록 카드가 뜬 직후 한 번만 좌우로 흔들린다.
   errs: {title, items:[{k, v, at}], text, textAt}  — 화면 전체가 아니라 카드만 흔들림(사전 금지 규칙). */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb);
  SCENE.errs = (lt, s) => {
    const K = s._same, its = s.items || [];
    let h = titleH(lt, s, 56, 30, K && s._prev.title === s.title);
    h += `<div class="row" style="gap:60px;justify-content:center">` + its.map((x, i) => {
      const pv = K ? (s._prev.items || [])[i] : null, was = !!(pv && pv.at != null && pv.at < 50);   /* 이어지는 장면: 앞에서 이미 보인 카드만 그대로 */
      const p = was ? 1 : AT(s, x.at, .4, 0), sh = (was || x.shake === false) ? 1 : AT(s, (x.at != null && x.at >= 0 ? x.at : 0) + .35, .7, 0);
      return `<div style="width:640px;height:330px;border-radius:36px;background:#fff;border:8px solid ${RED};box-shadow:0 14px 36px rgba(229,72,77,.18);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;${rise(p, 40)}">
        <div style="${MK.css.shake(sh, 14)}" class="col">
        <div style="font-size:54px;font-weight:900;color:#3B4A63;letter-spacing:-1.5px;white-space:nowrap;text-align:center">${esc(x.k)}</div>
        <div class="num" style="font-size:150px;font-weight:900;color:${RED};letter-spacing:-5px;line-height:1.05;text-align:center">${esc(x.v)}</div></div></div>`; }).join('') + `</div>`;
    h += textH(lt, s, .8, 64);
    wrapC(h);
  };
  Object.assign(MOTION, { errs: s => .8 });
})();
/* @@FX1101END */
