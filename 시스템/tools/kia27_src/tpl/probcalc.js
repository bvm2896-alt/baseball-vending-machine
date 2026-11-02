/* @@PROB1101 11/1 롱폼㉟ 「한국시리즈 KT 우승 확률」 — 사용자 "텍스트로 떼우지 말고 모션그래픽·인포그래픽으로".
   probcalc: 큰 확률 숫자 + 0~100% 막대 + 더하기/빼기 칩. 칩이 그 호흡에 튀어나오면 숫자와 막대가 그만큼 움직인다.
     {title, base:81.8, baseLabel, team, chips:[{k:'90승 전력', d:3, at, team}], text, textAt}   — 칩 at<0 = 이미 나온 칩(움직임 없음)
     같은 chain 의 cont 장면이면 앞 장면에 있던 칩은 그대로, 새 칩만 튀어나온다.
   probpair: 두 갈래 결과 나란히. {title, items:[{team, label, v, at, hi}], text, textAt} */
const TCOL_P = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
const LOGOI_P = (n, px) => { const c_ = (T(n) || {}).code; return LOGO[c_] ? `<img src="${LOGO[c_]}" style="width:${px}px;height:${px}px;object-fit:contain;display:block">` : ''; };
SCENE.probcalc = (lt, s) => { const e3 = x => 1 - Math.pow(1 - c01(x), 3);
  const ch = s.chips || [], P0 = s._same ? (s._prev.chips || []) : [], base = +s.base || 0;
  const was = c => P0.some(o => o.k === c.k && o.d === c.d);
  const pr = ch.map((c, i) => was(c) || (c.at != null && c.at < 0) ? 1 : pk(s, c.at, .7, seg(lt, .4 + i * .3, .7)));
  let v = base; ch.forEach((c, i) => { v += c.d * e3(pr[i]); });
  const W = 1400, BH = 64, col = s.team ? TCOL_P(s.team) : ACC, sameT = s._same && s._prev.title === s.title;
  const bq = sameT ? 1 : seg(lt, .05, .5), nq = s._same || s.baseAt == null ? 1 : pk(s, s.baseAt, .5, 0);
  let h = titleH(lt, s, 54, 14, sameT);
  h += `<div class="col" style="align-items:center;gap:22px;${sameT ? '' : rise(bq, 26)}">
    <div class="row" style="gap:22px;align-items:center;opacity:${nq.toFixed(3)}">${s.team ? LOGOI_P(s.team, 110) : ''}
      <div class="num" style="font-size:200px;font-weight:900;letter-spacing:-6px;line-height:1;color:${col}">${v.toFixed(s.dec ?? 1)}<span style="font-size:96px;margin-left:6px">%</span></div></div>
    ${s.baseLabel ? `<div style="opacity:${nq.toFixed(3)};font-size:36px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(s.baseLabel)}</div>` : ''}
    <div style="position:relative;width:${W}px;height:${BH}px;border-radius:${BH / 2}px;background:#E9EDF3;overflow:hidden">
      <div style="position:absolute;left:0;top:0;bottom:0;width:${(W * c01(v / 100)).toFixed(1)}px;border-radius:${BH / 2}px;background:linear-gradient(90deg, ${col}CC, ${col})"></div>
      <div style="position:absolute;left:${(W * base / 100).toFixed(1)}px;top:-4px;width:6px;height:${BH + 8}px;background:#12161F;opacity:.55"></div></div>
    <div class="row" style="width:${W}px;justify-content:space-between;font-size:30px;font-weight:800;color:#9AA3B2;margin-top:-10px"><span>0%</span><span>100%</span></div>
  </div>`;
  if (ch.length) h += `<div class="row" style="margin-top:20px;gap:18px;justify-content:center;flex-wrap:wrap;max-width:1700px">` + ch.map((c, i) => {
      const p = pr[i], plus = c.d > 0, cc = plus ? GREEN : RED, sg = (plus ? '+' : '−') + Math.abs(c.d);
      return `<div class="row" style="gap:14px;align-items:center;padding:12px 26px;border-radius:24px;background:#fff;border:5px solid ${cc};box-shadow:0 10px 24px rgba(18,22,31,.10);${pop(p)}">
        ${c.team ? LOGOI_P(c.team, 54) : ''}<span style="font-size:40px;font-weight:900;letter-spacing:-1px;white-space:nowrap">${esc(c.k)}</span>
        <span class="num" style="font-size:54px;font-weight:900;color:${cc};white-space:nowrap">${sg}</span></div>`; }).join('') + `</div>`;
  if (s.text) h += `<div class="big gold" style="margin-top:22px;font-size:${s.size || 64}px;${pop(pk(s, s.textAt, .5, 1))}">${br(s.text)}</div>`;
  wrapC(h);
};
SCENE.probpair = (lt, s) => { const e3 = x => 1 - Math.pow(1 - c01(x), 3);
  const it = s.items || [], W = 760;
  let h = titleH(lt, s, 54, 18, s._same && s._prev.title === s.title);
  h += `<div class="row" style="gap:70px;justify-content:center;align-items:stretch">` + it.map((x, i) => {
    const q = (s._same || (x.at != null && x.at < 0)) ? 1 : pk(s, x.at, .8, seg(lt, .3 + i * .4, .8)), col = TCOL_P(s.team || x.team), v = (+x.v) * e3(q);
    const hq = x.hi && !(s._same) ? c01((q - 1) * 0 + (lt - (x.at != null && x.at >= 0 ? 0 : 0)) * 0) : 0, hp = x.hi ? pk(s, (x.at != null && x.at >= 0 ? x.at : 0) + .9, .8, 0) : 0;   /* 11/1 움직임 사전: 강조 칸 = 광택 스윕 1회(숫자 다 올라간 뒤) */
    return `<div class="pane col" style="position:relative;overflow:hidden;width:${W}px;border-radius:36px;padding:34px 30px;gap:18px;align-items:center;border:${x.hi ? 8 : 4}px solid ${x.hi ? col : LINE};${rise(c01(q * 2.5), 40)}">${x.hi ? MK.sweep(hp, 'rgba(37,99,235,.18)') : ''}
      <div class="row" style="gap:16px;align-items:center"><span style="font-size:52px;font-weight:900;letter-spacing:-1.5px;white-space:nowrap">${esc(x.label || '')}</span></div>
      <div class="num" style="position:relative;font-size:190px;font-weight:900;letter-spacing:-6px;line-height:1;color:${col}">${v.toFixed(s.dec ?? 1)}<span style="font-size:70px">%</span></div>
      <div style="position:relative;width:${W - 80}px;height:40px;border-radius:20px;background:#E9EDF3;overflow:hidden"><div style="width:${((W - 80) * c01(v / 100)).toFixed(1)}px;height:40px;border-radius:20px;background:${col}"></div></div></div>`; }).join('') + `</div>`;
  if (s.text) h += `<div class="big gold" style="margin-top:30px;font-size:${s.size || 64}px;${pop(pk(s, s.textAt, .5, 1))}">${br(s.text)}</div>`;
  wrapC(h);
};
Object.assign(MOTION, { probcalc: s => .6 + (s.chips || []).length * .3, probpair: () => 1.2 });
/* @@PROB1101END */
