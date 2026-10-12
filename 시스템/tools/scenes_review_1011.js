/* @@REVIEW1011 */
/* 10/11 경기 리뷰 쇼츠 모션그래픽 3종 (사용자 "경기 내용을 다루는 리뷰 · 이해되기 쉽게 애니메이션·인포그래픽·모션그래픽 · 볼 게 많게").
   diamond — 야구장 다이아몬드 위에 주자가 들어오고(안타·볼넷), 홈런이면 공이 담장을 넘고 주자들이 홈으로 들어온다. 아웃 카운트·점수판이 같이 바뀐다.
     {"type":"diamond","title":"6회초 · 롯데 공격","away":"롯데","home":"KIA","score":[0,0],"outs":2,
      "steps":[{"at":1,"who":"레이예스","bases":["레이예스",null,null],"label":"레이예스 안타"},
               {"at":2,"who":"나승엽","bases":["나승엽","레이예스",null],"label":"나승엽 안타"},
               {"at":3,"who":"고승민","bases":["고승민","나승엽","레이예스"],"label":"고승민 볼넷 · 만루"},
               {"at":4,"who":"한동희","hr":true,"runs":4,"bases":[null,null,null],"label":"한동희 만루 홈런"}]}
     bases = [1루,2루,3루] 주자 이름. hr:true 면 공이 담장을 넘고 who+주자 전원이 홈으로. scored:[이름] 은 홈런이 아닌 득점(희생플라이). outs 는 그 단계 뒤 아웃 수. runs 는 더해지는 점수.
   count — 한 타석 투구 순서(S 스트라이크·B 볼·F 헛스윙·X 파울)가 한 구씩 쌓이고 B/S 불이 켜진다 → 결과 알약 → (after) 방망이 투척.
     {"type":"count","title":"3회초 선두타자","pitcher":{"name":"후라도","team":"삼성","img":…},"batter":{"name":"최원준","team":"KT","img":…},
      "pitches":["S","B","B","B","F","B"],"pitchAt":1,"result":{"label":"볼넷","color":"#16A34A"},"after":{"at":2,"label":"방망이 투척","bat":true}}
   race — 기록 경쟁 막대: 숫자가 from→to 로 올라가고 +N 알약, 아래 차이 알약.
     {"type":"race","title":"최다 안타 경쟁","unit":"안타","max":212,"items":[{"name":"레이예스","team":"롯데","img":…,"from":205,"to":207,"at":1,"hi":true},{"name":"최원준","team":"KT","img":…,"from":204,"to":205,"at":2}],
      "diff":{"label":"2개 차","at":3}}
   시간은 호흡(bp) 으로만. */
(() => {
  const ttl = (lt, s, mb = 22) => s.title ? `<div style="margin-bottom:${mb}px;${pop(s._same ? 1 : seg(lt, 0, .4))}">${pill(esc(s.title), '#12161F', 44, 'padding:10px 34px')}</div>` : '';
  const secs = (s, k, cap = 4) => k == null ? cap : bp(s, k, cap) * cap;   // 호흡 k 가 시작된 뒤 지난 초(cap 까지)
  const faceCard = (x, w = 250, h = 150) => { const src = photoSrc(x.img);
    return `<div class="pane row" style="width:${w}px;height:${h}px;border-radius:26px;padding:0;overflow:hidden;gap:0;border-color:${TCOL(x.team)}">
      <div style="width:${h - 10}px;height:100%;position:relative;overflow:hidden;background:#E9EDF3;flex:0 0 auto">${src ? faceImg(src, x, '50% 15%') : LOGOI(x.team, h - 10)}</div>
      <div class="col" style="flex:1;gap:6px;align-items:flex-start;padding-left:16px"><div style="font-size:${x.name.length > 3 ? 34 : 40}px;font-weight:900;letter-spacing:-1.5px">${esc(x.name)}</div>${x.role ? `<div style="font-size:26px;font-weight:800;color:${GRAY}">${esc(x.role)}</div>` : ''}</div></div>`; };

  /* ── diamond ── */
  const BX = [[450, 520], [670, 330], [450, 140], [230, 330], [450, 520]];
  const posAt = b => { b = Math.max(0, Math.min(4, b)); const i = Math.floor(b), f = b - i; if (i >= 4) return BX[4]; const a = BX[i], c = BX[i + 1]; return [a[0] + (c[0] - a[0]) * f, a[1] + (c[1] - a[1]) * f]; };
  SCENE.diamond = (lt, s) => {
    const steps = s.steps || [];
    let ci = -1, cp = 0;
    steps.forEach((st, i) => { const p = st.at == null ? 1 : bp(s, st.at, st.hr ? 1.3 : .7); if (p > 0) { ci = i; cp = p; } });
    const e = eo(cp);
    const base0 = { bases: [null, null, null], outs: s.outs || 0 };
    const cur = ci >= 0 ? steps[ci] : base0, prev = ci > 0 ? steps[ci - 1] : base0;
    const pb = prev.bases || [], cb = cur.bases || [];
    const at = (bases, n) => { const k = bases.indexOf(n); return k < 0 ? null : k + 1; };
    const names = [...new Set([...pb.filter(Boolean), ...cb.filter(Boolean), cur.who, ...(cur.scored || []), ...(cur.out || [])].filter(Boolean))];
    const runners = names.map(n => { const from = at(pb, n) ?? 0; let to = at(cb, n), dead = false;
      if ((cur.out || []).includes(n)) { to = from + .72; dead = true; }   // out:[이름] — 다음 베이스로 가다가 잡힘(✗)
      else if (to == null) to = (cur.hr || (cur.scored || []).includes(n)) ? 4 : (n === cur.who ? 0 : from);
      return { n, from, to, dead }; });
    // 점수: 앞 단계까지 전부 + 현재 단계는 주자가 홈에 닿을 때
    let sc = (s.score || [0, 0]).slice(); const bi = s.batIdx ?? 0;
    steps.forEach((st, i) => { if (i < ci) sc[bi] += st.runs || 0; });
    const scoreNow = ci >= 0 && (cur.runs || 0) > 0 && e > .85;
    if (scoreNow) sc[bi] += cur.runs;
    const outs = ci >= 0 ? (cur.outs ?? prev.outs ?? s.outs ?? 0) : (s.outs || 0);
    const TEAM = s.bat || s.away, col = TCOL(TEAM);
    let h = ttl(lt, s, 10);
    // 위 줄: 아웃 카운트(왼쪽) · 점수판(오른쪽) — 구장 위에 따로 둬서 홈런 표시와 안 겹치게
    const sb = (t, v, i) => `<div class="row" style="gap:10px;align-items:center">${LOGOI(t, 54)}<span class="num" style="color:#fff;font-size:48px;font-weight:900;min-width:60px;text-align:right;${scoreNow && i === bi ? `color:#FFD166;transform:scale(1.15)` : ''}">${v}</span></div>`;
    h += `<div class="row" style="width:900px;justify-content:space-between;align-items:center;margin-bottom:8px;${rise(s._same ? 1 : seg(lt, .05, .4), 20)}">
      <div class="row" style="gap:12px;align-items:center;background:#12161F;border-radius:999px;padding:10px 22px"><span style="color:#fff;font-size:30px;font-weight:900">OUT</span>${[0, 1, 2].map(k => `<div style="width:32px;height:32px;border-radius:50%;background:${k < outs ? '#E5484D' : '#555C6A'};border:3px solid #fff"></div>`).join('')}</div>
      <div class="row" style="gap:18px;align-items:center;background:#12161F;border-radius:26px;padding:10px 22px;position:relative">${sb(s.away, sc[0], 0)}<span style="color:#9AA3B2;font-size:36px;font-weight:900">:</span>${sb(s.home, sc[1], 1)}
        ${scoreNow ? `<div style="position:absolute;right:0;top:-62px;${ppop(c01((e - .85) * 6))}">${pill('+' + cur.runs, '#FFD166', 40, 'color:#12161F;padding:6px 22px')}</div>` : ''}</div></div>`;
    h += `<div style="position:relative;width:900px;height:620px;${rise(s._same ? 1 : seg(lt, .05, .45), 30)}">`;
    // 구장: 외야 잔디(부채꼴) · 내야 흙 · 내야 잔디 · 베이스 · 마운드 · 파울 라인
    h += `<svg viewBox="0 0 900 620" width="900" height="620" style="position:absolute;left:0;top:0">
      <defs><radialGradient id="dg" cx="50%" cy="80%" r="75%"><stop offset="0" stop-color="#62BA62"/><stop offset="1" stop-color="#3B8A3F"/></radialGradient>
        <clipPath id="dc"><rect x="0" y="0" width="900" height="620" rx="34"/></clipPath></defs>
      <g clip-path="url(#dc)"><path d="M450,560 L-120,20 A700,700 0 0 1 1020,20 Z" fill="url(#dg)"/>
      <path d="M450,575 L735,330 Q450,60 165,330 Z" fill="#C9A06A"/>
      <polygon points="450,520 670,330 450,140 230,330" fill="#6CC56C"/>
      <circle cx="450" cy="335" r="36" fill="#D9B27B"/>
      <path d="M450,520 L-20,120 M450,520 L920,120" stroke="#fff" stroke-width="5" opacity=".85"/>
      ${[1, 2, 3].map(k => `<rect x="${BX[k][0] - 19}" y="${BX[k][1] - 19}" width="38" height="38" fill="#fff" transform="rotate(45 ${BX[k][0]} ${BX[k][1]})" stroke="#CFCFCF" stroke-width="3"/>`).join('')}
      <polygon points="430,500 470,500 470,520 450,538 430,520" fill="#fff" stroke="#CFCFCF" stroke-width="3"/></g></svg>`;
    // 주자
    runners.forEach(r => {
      const b = r.from + (r.to - r.from) * e; let [x, y] = posAt(b); if (b <= 0.001) { x -= 78; y -= 10; } const nmTop = b <= 0.001;   // 타석(홈)에 선 타자는 왼쪽 타자석에
      const done = r.to === 4 && b > 3.9, fresh = r.from === 0 && r.to > 0;
      const gone = r.dead && e > .98, op = done ? c01((4 - b) * 8) : gone ? .35 : 1, sz = 66;
      h += `<div style="position:absolute;left:${x - sz / 2}px;top:${y - sz / 2 - 6}px;width:${sz}px;height:${sz}px;border-radius:50%;background:${col};border:5px solid #fff;box-shadow:0 8px 18px rgba(0,0,0,.3);opacity:${op};${fresh && e < .2 ? `transform:scale(${.5 + 2.5 * e})` : ''}"></div>
        <div style="position:absolute;left:${x - 100}px;top:${nmTop ? y - sz / 2 - 44 : y + sz / 2 - 4}px;width:200px;text-align:center;opacity:${op}"><span style="display:inline-block;background:rgba(18,22,31,.85);color:#fff;font-size:30px;font-weight:900;padding:2px 14px;border-radius:999px;white-space:nowrap">${esc(r.n)}</span></div>`;
      if (r.dead && e > .7) h += `<div style="position:absolute;left:${x - 40}px;top:${y - 46}px;width:80px;height:80px;${ppop(c01((e - .7) * 4))}"><svg viewBox="0 0 100 100" width="80" height="80"><circle cx="50" cy="50" r="44" fill="${RED}" stroke="#fff" stroke-width="6"/><path d="M30,30 L70,70 M70,30 L30,70" stroke="#fff" stroke-width="12" stroke-linecap="round"/></svg></div>`;
    });
    // 홈런 공
    if (cur.hr && ci >= 0) {
      const q = c01((cp - .05) / .6), bx = 450 + 60 * q, by = 520 - 560 * q + 140 * q * q;
      if (q > 0 && q < 1) h += `<div style="position:absolute;left:${bx - 16}px;top:${by - 16}px;width:32px;height:32px;border-radius:50%;background:#fff;border:3px solid #E5484D;box-shadow:0 4px 10px rgba(0,0,0,.3)"></div>`;
      if (q >= .55) h += `<div style="position:absolute;left:0;right:0;top:34px;text-align:center;${ppop(c01((q - .55) * 3))}">${pill('홈런!', RED, 60, 'padding:12px 40px;box-shadow:0 14px 30px rgba(229,72,77,.4)')}</div>`;
    }
    // 아래 설명 알약
    if (ci >= 0 && cur.label) h += `<div style="position:absolute;left:0;right:0;bottom:16px;text-align:center;${ppop(c01(cp * 2))}">${pill(esc(cur.label), cur.hr ? RED : col, 46, 'padding:12px 40px;box-shadow:0 12px 28px rgba(0,0,0,.25)')}</div>`;
    else if (s.lead) h += `<div style="position:absolute;left:0;right:0;bottom:16px;text-align:center;${ppop(seg(lt, .3, .4))}">${pill(esc(s.lead), '#12161F', 46, 'padding:12px 40px')}</div>`;
    h += `</div>`;
    if (s.text) h += `<div class="big gold" style="margin-top:24px;font-size:${s.size || 64}px;${pop(bp(s, s.textAt ?? 50, .5))}">${br(s.text)}</div>`;
    B(h);
  };

  /* ── count ── */
  const batSvg = c => `<svg viewBox="0 0 200 60" width="100%" height="100%"><path d="M8,34 q0,-10 14,-10 l120,-6 q50,-4 50,12 q0,16 -50,12 l-120,-6 q-14,0 -14,-10 z" fill="${c}"/><rect x="4" y="22" width="26" height="24" rx="8" fill="#12161F"/></svg>`;
  SCENE.count = (lt, s) => {
    const ps = s.pitches || [], q = secs(s, s.pitchAt ?? 0, 6), step = s.step || .3;
    const shown = Math.min(ps.length, Math.floor(q / step) + (s.pitchAt == null ? ps.length : 0));
    let balls = 0, strikes = 0;
    ps.slice(0, shown).forEach(v => { if (v === 'B') balls++; else if (v === 'S' || v === 'F') strikes = Math.min(2, strikes + 1); else if (v === 'X' && strikes < 2) strikes++; });
    const done = shown >= ps.length, rp = s.result && s.result.at != null ? (done ? bp(s, s.result.at, .5) : 0) : (done ? c01((q - ps.length * step) / .4) : 0);
    let h = ttl(lt, s, 18);
    h += `<div class="row" style="gap:26px;align-items:center;${rise(s._same ? 1 : seg(lt, .05, .4), 30)}">${s.pitcher ? faceCard({ role: '투수', ...s.pitcher }, 390, 180) : ''}<div style="font-size:50px;font-weight:900;color:${GRAY}">vs</div>${s.batter ? faceCard({ role: '타자', ...s.batter }, 390, 180) : ''}</div>`;
    // B / S 불
    const light = (n, on, c) => Array.from({ length: n }, (_, k) => `<div style="width:64px;height:64px;border-radius:50%;background:${k < on ? c : '#2B3140'};border:4px solid #fff;box-shadow:${k < on ? `0 0 22px ${c}` : 'none'}"></div>`).join('');
    h += `<div class="row" style="margin-top:26px;gap:40px;background:#12161F;border-radius:30px;padding:18px 40px;${rise(s._same ? 1 : seg(lt, .15, .4), 30)}">
      <div class="row" style="gap:12px;align-items:center"><span style="color:#fff;font-size:42px;font-weight:900;margin-right:8px">B</span>${light(3, balls, '#16A34A')}</div>
      <div class="row" style="gap:12px;align-items:center"><span style="color:#fff;font-size:42px;font-weight:900;margin-right:8px">S</span>${light(2, strikes, '#FACC15')}</div></div>`;
    // 투구 순서
    const LBL = { S: '스트라이크', B: '볼', F: '헛스윙', X: '파울' }, COL = { S: '#FACC15', B: '#16A34A', F: '#FACC15', X: '#9AA3B2' };
    h += `<div class="row" style="margin-top:28px;gap:14px;align-items:flex-end;justify-content:center;flex-wrap:nowrap">`;
    ps.forEach((v, k) => { const vis = k < shown, p = vis ? c01((q - k * step) / .3) : 0;
      h += `<div class="col" style="gap:8px;width:${Math.min(146, Math.floor(900 / ps.length) - 10)}px;${vis ? ppop(p) : 'opacity:0'}"><div style="font-size:26px;font-weight:800;color:${GRAY}">${k + 1}구</div>
        <div style="width:112px;height:112px;border-radius:50%;background:${COL[v] || GRAY};color:${v === 'B' || v === 'X' ? '#fff' : '#12161F'};font-size:60px;font-weight:900;display:flex;align-items:center;justify-content:center;border:5px solid #fff;box-shadow:0 8px 18px rgba(0,0,0,.18)">${v === 'F' ? 'S' : v === 'X' ? 'F' : v}</div>
        <div style="font-size:${v === 'S' ? 26 : 30}px;font-weight:900;white-space:nowrap">${LBL[v] || v}</div></div>`; });
    h += `</div>`;
    // 결과
    if (s.result) h += `<div style="margin-top:30px;${ppop(rp)}">${pill(esc(s.result.label), s.result.color || GREEN, 56, 'padding:12px 44px;box-shadow:0 12px 28px rgba(0,0,0,.2)')}</div>`;
    // 뒤이은 장면(방망이 투척)
    if (s.after) { const ap_ = bp(s, s.after.at ?? 50, .8);
      if (ap_ > 0) { const rot = -40 + 400 * eo(ap_), dx = 520 * eo(ap_), dy = -160 * Math.sin(Math.PI * c01(ap_));
        h += `<div style="position:absolute;left:120px;top:${(s.batY ?? 760)}px;width:230px;height:70px;transform:translate(${dx}px,${dy}px) rotate(${rot}deg);opacity:${c01(ap_ * 4)}">${batSvg('#B5651D')}</div>
          <div style="position:absolute;right:50px;top:${(s.batY ?? 760) - 10}px;${ppop(c01(ap_ * 1.3 - .3))}">${pill(esc(s.after.label), RED, 46, 'padding:10px 30px')}</div>`; } }
    B(h);
  };

  /* ── race ── */
  SCENE.race = (lt, s) => {
    const it = s.items || [], max = s.max || Math.max(...it.map(x => x.to)) * 1.04, min = s.min ?? Math.min(...it.map(x => Math.min(x.from, x.to))) * .9;
    let h = ttl(lt, s, 26);
    h += `<div class="col" style="gap:34px;width:900px">`;
    it.forEach((x, i) => {
      const show = seg(lt, .1 + i * .15, .4), p = x.at == null ? 1 : x.at < 0 ? 1 : bp(s, x.at, .9), e = eo(p);
      const v = x.from + (x.to - x.from) * e, w = Math.max(60, (v - min) / (max - min) * 560), col = TCOL(x.team), src = photoSrc(x.img), d = x.to - x.from;
      h += `<div class="pane" style="width:900px;border-radius:34px;padding:18px 26px;display:flex;align-items:center;gap:20px;border-color:${x.hi ? col : LINE};border-width:${x.hi ? 6 : 3}px;${ap(show, 40)}">
        <div style="width:120px;height:120px;border-radius:50%;overflow:hidden;position:relative;background:#E9EDF3;flex:0 0 auto;border:5px solid ${col}">${src ? faceImg(src, x, '50% 15%') : LOGOI(x.team, 110)}</div>
        <div class="col" style="flex:1;align-items:flex-start;gap:10px">
          <div class="row" style="gap:12px;align-items:center;width:100%"><div style="font-size:42px;font-weight:900;letter-spacing:-1.5px">${esc(x.name)}</div>${LOGOI(x.team, 44)}<div style="flex:1"></div>
            <div class="num" style="font-size:72px;font-weight:900;letter-spacing:-3px;color:${col};line-height:1">${Math.round(v)}<span style="font-size:32px;color:${GRAY};margin-left:6px">${esc(s.unit || '')}</span></div></div>
          <div style="position:relative;width:100%;height:30px;background:#E9EDF3;border-radius:15px;overflow:visible"><div style="width:${w}px;height:30px;border-radius:15px;background:${col}"></div>
            ${d > 0 && p > 0 ? `<div style="position:absolute;left:${w + 12}px;top:-12px;${ppop(c01(p * 1.5))}">${pill('+' + d, d >= 2 ? RED : '#12161F', 30, 'padding:4px 16px')}</div>` : ''}</div>
          ${x.sub ? `<div style="font-size:28px;font-weight:800;color:${GRAY}">${esc(x.sub)}</div>` : ''}</div></div>`;
    });
    h += `</div>`;
    if (s.diff) { const q = bp(s, s.diff.at ?? 50, .5); h += `<div style="margin-top:34px;${ppop(q)}">${pill(esc(s.diff.label), s.diff.color || RED, 56, 'padding:12px 44px')}</div>`; }
    if (s.text) h += `<div class="big gold" style="margin-top:26px;font-size:${s.size || 60}px;${pop(bp(s, s.textAt ?? 50, .5))}">${br(s.text)}</div>`;
    B(h);
  };
  Object.assign(MOTION, { diamond: () => .7, count: () => .8, race: () => .8 });
})();
/* @@REVIEW1011END */
