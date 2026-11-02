/* @@REF1102 11/2 사용자 레퍼런스 합치기(디자인-레퍼런스-1102.md): 주 A3 rf_card · B3 rf_bars · C1 rf_band / 섞기 A1 rf_gold · B1 rf_bars(glass) · C3 rf_duo
   + 화면 전체 사진 바탕 레이어(#sbg): 장면 s.bg = {img, f(필터), pos} 또는 {css(그라디언트)} — 전환 0.3초 동안 앞 장면 바탕과 겹쳐 바뀜(툭 끊김 없음)
   색 바꾸기(테마) 대상이 아니다: 루트에 data-nodark, 테마가 바꾸는 색 코드는 쓰지 않는다 */
(() => {
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d, fb != null ? fb : 0);
  const ACC = { HT: '#EA0029', SS: '#0A5BD1', LG: '#C30452', OB: '#2B2A7A', KT: '#EB1C24', NC: '#315288', LT: '#D00F31', SK: '#CE0E2D', HH: '#FF6600', WO: '#820024' };
  const DARKT = { HT: '#2A060B', SS: '#06142E', LG: '#26040F', OB: '#0B0A26', KT: '#1A0507', NC: '#081426', LT: '#06122A', SK: '#28050A', HH: '#2A1102', WO: '#22030A' };
  const code = t => { const tt = T(t); return tt ? tt.code : ''; };
  const AC = t => ACC[code(t)] || '#E5484D';
  const LGo = (t, w) => { const c = code(t); return c && LOGO[c] ? `<img src="${LOGO[c]}" style="width:${w}px;height:${w}px;object-fit:contain;filter:drop-shadow(0 4px 10px rgba(0,0,0,.45))">` : ''; };
  const YEL = '#FFD43B', INK = '#11151E', MUTE2 = '#C9D0DE';
  const WL = t => [...String(t || '')].reduce((n, ch) => n + (ch.charCodeAt(0) > 0x3000 ? 1 : ch === ' ' ? .35 : .6), 0);   /* 11/3 '텍스트 삐져나감': 글 폭(글자 크기 1 기준) */
  const FIT = (t, base, w) => Math.max(28, Math.min(base, Math.floor(w / Math.max(.1, WL(t)))));
  const op = q => `opacity:${c01(q * 1.6).toFixed(3)}`;
  const up = (q, d = 30) => `opacity:${c01(q * 1.6).toFixed(3)};transform:translateY(${((1 - eo(q)) * d).toFixed(1)}px)`;
  const pic = (img, focus, extra = '') => { const src = photoSrc(img); return src ? `<img src="${src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${focus || '50% 18%'};${extra}">` : ''; };
  const ROOT = (h, extra = '') => B(`<div data-nodark="1" style="position:relative;width:1808px;height:714px;color:#FFFFFF;${extra}">${h}</div>`);
  const ttl = (lt, s) => s.title ? `<div class="title" style="position:absolute;left:0;right:0;top:0;text-align:center;font-size:60px;font-weight:900;letter-spacing:-2px;color:#FFFFFF;text-shadow:0 4px 18px rgba(0,0,0,.55);${s._same && s._prev && s._prev.title === s.title ? '' : op(seg(lt, 0, .4))}">${esc(s.title)}</div>` : '';

  /* ── 사진 바탕 레이어 ── */
  const setL = (el, b, o) => {
    if (!b || o <= 0) { el.style.opacity = '0'; return; }
    const key = b.css || b.img || '';
    if (el.dataset.k !== key) { el.dataset.k = key;
      if (b.css) { el.style.backgroundImage = b.css; el.style.filter = 'none'; }
      else { const src = photoSrc(b.img); el.style.backgroundImage = src ? `url("${src}")` : 'none'; el.style.filter = b.f || 'blur(4px) brightness(.32) contrast(1.2) saturate(1.3)'; el.style.backgroundPosition = b.pos || 'center 25%'; } }
    el.style.opacity = o.toFixed(3);
  };
  window.__sbgPaint = (kk, t, start) => {
    const st = document.getElementById('stage'); if (!st) return;
    let L = document.getElementById('sbg');
    if (!L) { L = document.createElement('div'); L.id = 'sbg'; L.style.cssText = 'position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:0';
      L.innerHTML = ['a', 'b'].map(c => `<div class="${c}" style="position:absolute;inset:-40px;background-size:cover;background-repeat:no-repeat;opacity:0"></div>`).join('') + '<div class="v" style="position:absolute;inset:0"></div>';
      st.insertBefore(L, st.firstChild); }
    const cur = (SC[kk] || {}).bg || null, prv = kk > 0 ? ((SC[kk - 1] || {}).bg || null) : null, q = c01((t - start) / 0.3);
    const same = !!(cur && prv && (cur.css || cur.img) === (prv.css || prv.img) && (cur.f || '') === (prv.f || ''));
    setL(L.querySelector('.a'), same ? null : prv, 1 - q);
    setL(L.querySelector('.b'), cur, same ? 1 : q);
    const vin = (cur && !cur.css ? (same ? 1 : q) : 0) + (prv && !prv.css && !same ? (1 - q) : 0);
    L.querySelector('.v').style.boxShadow = vin > 0 ? `inset 0 0 300px rgba(0,0,0,${(0.8 * Math.min(1, vin)).toFixed(3)})` : 'none';
  };

  /* ── A3 rf_card: 팀 컬러 선수 카드 {img, focus, name, team, kicker, big:{v, k, sub, at}, minor:[{k, v, at}], imgAt, nameAt}
     바탕은 s.bg 를 안 주면 팀 색 사선 무늬 ── */
  SCENE.rf_card = (lt, s) => {
    const c = AC(s.team), pq = AT(s, s.imgAt, .5, seg(lt, 0, .5)), nq = AT(s, s.nameAt, .45, seg(lt, .1, .45));
    let h = `<div style="position:absolute;left:40px;top:0;width:700px;height:714px;clip-path:polygon(0 0,100% 0,88% 100%,0 100%);overflow:hidden;${op(pq)}">${pic(s.img, s.focus, 'filter:contrast(1.18) saturate(1.12)')}<div style="position:absolute;inset:0;box-shadow:inset 0 0 160px rgba(0,0,0,.65)"></div></div>
      <div style="position:absolute;left:40px;top:0;width:14px;height:714px;background:${c};${op(pq)}"></div>
      <div style="position:absolute;left:820px;top:40px;display:flex;align-items:center;gap:22px;${up(nq)}">${LGo(s.team, 112)}<div><div style="font-size:32px;font-weight:800;color:${c === '#0A5BD1' ? '#7DB0FF' : '#FF7A7A'};letter-spacing:2px">${esc(s.kicker || '')}</div><div style="font-size:100px;font-weight:900;line-height:1.02;letter-spacing:-3px">${esc(s.name || '')}</div></div></div>`;
    if (s.big) { const bq = AT(s, s.big.at, .5, seg(lt, .3, .5));
      h += `<div style="position:absolute;left:820px;top:240px;display:flex;align-items:flex-end;gap:26px;${up(bq, 40)}"><div class="num" style="font-size:${FIT(s.big.v, s.big.size || 210, 940 - 26 - Math.max(...String(s.big.k || '').split('\n').map(l => WL(l) * 54)))}px;font-weight:900;line-height:.92;letter-spacing:-8px;white-space:nowrap">${esc(s.big.v)}</div>
        <div style="font-size:54px;font-weight:900;line-height:1.15;margin-bottom:22px;white-space:nowrap">${br(s.big.k || '')}${s.big.sub ? `<br><span style="color:${YEL}">${esc(s.big.sub)}</span>` : ''}</div></div>`; }
    const mi = s.minor || [];
    if (mi.length) h += `<div style="position:absolute;left:820px;top:560px;display:flex;align-items:center;gap:40px">` + mi.map((m, i) => { const q = AT(s, m.at, .45, seg(lt, .5 + i * .2, .45));
      return `${i ? `<div style="width:3px;height:64px;background:rgba(255,255,255,.35);${op(q)}"></div>` : ''}<div style="display:flex;align-items:baseline;gap:14px;white-space:nowrap;${up(q, 20)}"><span style="font-size:40px;font-weight:800;color:${MUTE2}">${esc(m.k)}</span><b class="num" style="font-size:66px;font-weight:900;letter-spacing:-2px">${esc(m.v)}</b></div>`; }).join('') + `</div>`;
    ROOT(h);
  };

  /* ── A1 rf_gold: 조명 무대 + 금테 카드 {img, focus, name, en, team, profile:[..], stats:[{k, v, hi, at}], cardAt} — 바탕 s.bg 없으면 금빛 무대 ── */
  SCENE.rf_gold = (lt, s) => {
    const cq = AT(s, s.cardAt, .55, seg(lt, 0, .55));
    let h = `<div style="position:absolute;left:640px;top:0;width:500px;height:700px;border-radius:26px;padding:13px;background:linear-gradient(135deg,#FFE6A0,#B8860B 40%,#FFF1C2 60%,#9C6B12);box-shadow:0 30px 80px rgba(0,0,0,.6),0 0 60px rgba(255,200,90,.35);${up(cq, 50)}">
      <div style="position:relative;width:100%;height:100%;border-radius:16px;overflow:hidden;background:#000">${pic(s.img, s.focus, 'filter:contrast(1.15) saturate(1.1)')}
      <div style="position:absolute;left:0;right:0;bottom:0;height:240px;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.86))"></div>
      <div style="position:absolute;left:24px;top:20px;font-size:28px;font-weight:900;letter-spacing:4px;color:#FFE6A0">${esc(s.season || '2026 SEASON')}</div>
      <div style="position:absolute;right:18px;top:12px">${LGo(s.team, 84)}</div>
      <div style="position:absolute;left:24px;bottom:22px">${s.en ? `<div style="font-size:28px;font-weight:800;color:#FFE6A0;letter-spacing:2px">${esc(s.en)}</div>` : ''}<div style="font-size:68px;font-weight:900;letter-spacing:-2px">${esc(s.name || '')}</div></div></div></div>`;
    const pf = s.plist || s.profile || [];   /* 11/2: 글 목록은 plist(검사기가 profile=True 를 '프로필 장면'으로 읽음) */
    if (pf.length) h += `<div style="position:absolute;right:${1808 - 590}px;top:110px;text-align:right;display:flex;flex-direction:column;gap:14px;font-size:38px;font-weight:800;color:#F3E2BF;${up(cq)}">${pf.map(x => `<div style="white-space:nowrap">${esc(x)}</div>`).join('')}</div>`;
    h += `<div style="position:absolute;left:1200px;top:150px;display:flex;flex-direction:column;gap:26px">` + (s.stats || []).map((x, i) => { const q = AT(s, x.at, .45, seg(lt, .4 + i * .25, .45));
      const v = x.hi ? `<span style="background:${YEL};color:${INK};padding:0 16px;border-radius:12px">${esc(x.v)}</span>` : esc(x.v);
      return `<div style="${up(q, 24)}"><div style="font-size:32px;font-weight:800;color:#F3E2BF">${esc(x.k)}</div><div class="num" style="font-size:${x.size || 100}px;font-weight:900;line-height:1.05;letter-spacing:-2px;white-space:nowrap">${v}</div></div>`; }).join('') + `</div>`;
    ROOT(h);
  };

  /* ── B3 rf_bars (glass:true → B1): {title, items:[{label, place, venue, v, unit, dec, at, hi}], ref:{v, lab}, max, valAt}
     기준(ref)을 넘는 막대는 노랗게 빛남. 바탕은 s.bg 사진 ── */
  SCENE.rf_bars = (lt, s) => {
    const its = s.items || [], n = its.length, MX = s.max || 100, H = s.h || 400, BW = n > 7 ? 118 : n > 4 ? 150 : 200, GAP = n > 7 ? 26 : 40;
    const W = n * BW + (n - 1) * GAP, X0 = Math.round((1808 - W) / 2), YB = 560;
    let h = ttl(lt, s);
    if (s.glass) h += `<div style="position:absolute;left:${X0 - 150}px;top:90px;width:${W + 300}px;height:610px;border-radius:36px;background:rgba(255,255,255,.10);border:2px solid rgba(255,255,255,.22);box-shadow:0 30px 80px rgba(0,0,0,.35);${op(seg(lt, 0, .4))}"></div>`;
    if (s.ref) { const y = YB - H * s.ref.v / MX, rq = AT(s, s.ref.at, .4, seg(lt, .1, .4));
      h += `<div style="position:absolute;left:${X0 - 40}px;width:${W + 80}px;top:${y}px;border-top:4px dashed rgba(255,255,255,.5);${op(rq)}"></div><div style="position:absolute;left:${X0 + W + 60}px;top:${y - 22}px;font-size:30px;font-weight:800;color:${MUTE2};white-space:nowrap;${op(rq)}">${esc(s.ref.lab || (s.ref.v + '%'))}</div>`; }   /* 11/3: 기준선 이름은 오른쪽(긴 이름이 막대에 겹치던 것) */
    its.forEach((it, i) => {
      const q = AT(s, it.at, .6, seg(lt, .2 + i * .1, .6)), vq = it.valAt != null ? AT(s, it.valAt, .4, 0) : (s.valAt != null ? AT(s, s.valAt, .4, 0) : q);
      const hot = it.hi != null ? it.hi : (s.ref && it.v >= s.ref.v), col = hot ? YEL : 'rgba(255,255,255,.55)', bh = it.from != null ? H * (it.from + (it.v - it.from) * eo(q)) / MX : H * it.v / MX * eo(q), x = X0 + i * (BW + GAP);   /* 11/3 KT편: from → v 로 자라거나 줄어듦 */
      const val = (it.dec != null ? Number(it.v).toFixed(it.dec) : String(it.v)) + (it.unit || '');
      h += `<div style="position:absolute;left:${x}px;top:${YB - bh}px;width:${BW}px;height:${bh}px;border-radius:16px 16px 6px 6px;background:${col};${hot ? `box-shadow:0 0 34px rgba(255,212,59,.55);` : ''}"></div>
        <div class="num" style="position:absolute;left:${x - 30}px;width:${BW + 60}px;top:${YB - H * it.v / MX - 56}px;text-align:center;font-size:${n >= 7 ? 36 : BW < 130 ? 40 : 48}px;font-weight:900;color:${hot ? '#FFFFFF' : MUTE2};${op(vq)}">${esc(val)}</div>
        <div style="position:absolute;left:${x - 30}px;width:${BW + 60}px;top:${YB + 12}px;text-align:center;font-size:${BW < 130 ? 32 : 38}px;font-weight:900;white-space:nowrap;${op(q)}">${esc(it.label || '')}</div>
        ${it.place ? `<div style="position:absolute;left:${x}px;width:${BW}px;top:${YB + 58}px;display:flex;justify-content:center;${op(q)}"><span style="padding:2px 14px;border-radius:10px;background:${AC(it.venue || '')};font-size:24px;font-weight:900">${esc(it.place)}</span></div>` : ''}`;
    });
    if (s.brk) { const bq = AT(s, s.brk.at, .45, 0), xa = X0 + s.brk.a * (BW + GAP), xb = X0 + s.brk.b * (BW + GAP) + BW, top = Math.min(...its.slice(s.brk.a, s.brk.b + 1).map(it => YB - H * it.v / MX)) - 120;   /* 11/3: 막대 묶음 괄호 */
      h += `<div style="position:absolute;left:${xa - 10}px;width:${xb - xa + 20}px;top:${top}px;${op(bq)}"><div style="text-align:center;margin-bottom:8px"><span style="padding:4px 20px;border-radius:14px;background:${YEL};color:${INK};font-size:34px;font-weight:900;white-space:nowrap">${esc(s.brk.lab)}</span></div><div style="height:22px;border:5px solid ${YEL};border-bottom:0;border-radius:14px 14px 0 0"></div></div>`; }
    ROOT(h);
  };

  /* ── C1 rf_band: 사진 위 기록 띠 {who, tag, team, vals:[{v, k, at, hi}], whoAt} — 바탕 s.bg 사진(밝게 보정) ── */
  SCENE.rf_band = (lt, s) => {
    const wq = AT(s, s.whoAt, .45, seg(lt, 0, .45)), vs = s.vals || [];
    let h = `<div style="position:absolute;left:0;right:0;top:${s.top || 190}px;display:flex;flex-direction:column;align-items:center;gap:36px">
      <div style="display:flex;align-items:center;gap:18px;font-size:66px;font-weight:900;letter-spacing:-2px;text-shadow:0 4px 18px rgba(0,0,0,.6);${up(wq)}">${s.team ? LGo(s.team, 84) : ''}<span>${esc(s.who || '')}</span>${s.tag ? `<span style="color:${YEL};${s.tagAt != null ? op(AT(s, s.tagAt, .4, 1)) : ''}">#${esc(s.tag)}</span>` : ''}</div>
      <div style="display:flex;align-items:flex-end;gap:48px">` + vs.map((x, i) => { const q = AT(s, x.at, .45, seg(lt, .3 + i * .25, .45));
        return `${i ? `<div style="width:4px;height:130px;background:rgba(255,255,255,.5);${op(q)}"></div>` : ''}<div style="text-align:center;${up(q, 26)}"><div class="num" style="font-size:${x.size || 128}px;font-weight:900;line-height:1;letter-spacing:-3px;white-space:nowrap;color:${x.hi ? YEL : '#FFFFFF'};text-shadow:0 6px 24px rgba(0,0,0,.6)">${esc(x.v)}</div><div style="font-size:36px;line-height:44px;height:44px;color:${MUTE2};font-weight:800;margin-top:10px;white-space:nowrap">${esc(x.k || '')}</div></div>`; }).join('') + `</div></div>`;
    ROOT(h);
  };

  /* 11/2 2라운드 검수: 이름이 얼굴을 덮지 않게 이름 줄을 카드 아래(기록 위)로 */
  /* ── C3 rf_duo: 카드 두 장 비교 {title, cards:[{img, focus, name, team, at, stats:[{k, v, hi, at}]}]} ── */
  SCENE.rf_duo = (lt, s) => {
    const cs = s.cards || [], CW = cs.length > 2 ? 520 : 680, GAP = 80, W = cs.length * CW + (cs.length - 1) * GAP, X0 = Math.round((1808 - W) / 2);
    let h = ttl(lt, s);
    cs.forEach((c, i) => { const q = AT(s, c.at, .5, seg(lt, .1 + i * .3, .5)), x = X0 + i * (CW + GAP);
      h += `<div style="position:absolute;left:${x}px;top:110px;width:${CW}px;height:590px;border-radius:30px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.5);${up(q, 40)}">${pic(c.img, c.focus, 'filter:contrast(1.15)')}
        <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.9))"></div>
        <div style="position:absolute;left:0;top:0;bottom:0;width:12px;background:${AC(c.team)}"></div>
        <div style="position:absolute;left:34px;bottom:${((c.stats || []).length || s.reserveStats) ? 176 : 30}px;display:flex;align-items:center;gap:14px"><div style="font-size:60px;font-weight:900;text-shadow:0 3px 12px #000">${esc(c.name || '')}</div></div>
        <div style="position:absolute;left:34px;right:34px;bottom:28px;display:flex;justify-content:space-between;align-items:flex-end">` + (c.stats || []).map((x, j) => { const sq = AT(s, x.at, .45, q);
          const v = x.hi ? `<span style="background:${YEL};color:${INK};padding:0 14px;border-radius:10px">${esc(x.v)}</span>` : esc(x.v);
          const sw = (CW - 68) / Math.max(1, (c.stats || []).length) - 24;
          return `<div style="${op(sq)}"><div style="font-size:${FIT(x.k, 30, sw)}px;font-weight:800;color:${MUTE2};white-space:nowrap">${esc(x.k)}</div><div class="num" style="font-size:${FIT(x.v, j ? 70 : 92, sw - (x.hi ? 28 : 0))}px;font-weight:900;line-height:1.05;white-space:nowrap">${v}</div></div>`; }).join('') + `</div></div>`; });
    ROOT(h);
  };

  Object.assign(MOTION, { rf_card: s => .8, rf_gold: s => .8, rf_bars: s => .9, rf_band: s => .8, rf_duo: s => .8 });
})();
/* @@REF1102END */
