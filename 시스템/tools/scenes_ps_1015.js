/* @@PS1015 */
/* 10/15 롱폼 「와일드카드 리뷰 + 준플레이오프 예측」 — 쇼츠 리뷰 장면(diamond·count·race, tools/scenes_review_1011.js)을 롱폼 템플릿에서도 쓰게 하는 덮개.
   tools/inject_ps_1015.py 가 이 블록을 template_long.html·template_long_v.html 의 function render 앞에 넣는다. 원본을 고치면 다시 주입. */
(() => {
const TCOL = n => { const c = TEAMCOL[(T(n) || {}).code] || '#6A7382'; return c === '#4A4A4A' ? '#12161F' : c; };
const LOGOI = (n, px, st = '') => `<img src="${LOGO[(T(n) || {}).code] || ''}" style="width:${px}px;height:${px}px;object-fit:contain;display:block;${st}">`;
const ppop = p => `opacity:${c01(p * 1.6)};transform:scale(${p <= 0 ? .5 : .5 + .5 * eb(p)})`;
const pill = (txt, bg, fs = 34, extra = '') => `<span style="display:inline-block;background:${bg};color:#fff;font-size:${fs}px;font-weight:900;padding:8px 24px;border-radius:999px;letter-spacing:-1px;white-space:nowrap;${extra}">${txt}</span>`;
const bp = (s, k, d = .45) => { if (k == null || k < 0) return 1; if (k >= 50) return 0; const b = brP(s, k, d); return b == null ? 1 : b; };
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
/* @@PS2_1015 */
/* 10/15 사용자 "카드 안 글은 딱 봤을 때 이해되게 — 인포그래픽·모션그래픽으로 · 카드 안에 넣지 말고 그냥 보여줘".
   흰 카드 틀 없이 사진·로고·그림을 바로 보여 주는 장면들. (scenes_ps_1015.js 안쪽, 같은 덮개에서 TCOL·LOGOI·ppop·pill·bp 를 쓴다)
   wcrule   와일드카드 규칙 — 팀마다 '통과에 필요한 승리' 칸, 4위 팀은 1칸이 미리 차 있음
   duel     선발 맞대결 — 카드 없이 사진 두 장 + 로고·이름 + 큰 VS
   speedgun 구속 — 투수 사진 + 계기판 바늘이 올라가며 숫자가 157·158 까지
   gamestrip 맞대결 16경기 — 경기마다 이긴 팀 로고 + 날짜, 묶음 괄호(LG 7승 2패 / KIA 7연승)
   faceoff  두 사람(또는 두 팀) 비교 — 양옆 사진, 가운데 항목별 막대(또는 글) + 앞선 쪽 표시
   abdots   투수 vs 타자 — 타수만큼 공 동그라미(안타·홈런·삼진·아웃), 동그라미 안에 글자
   relay    불펜 이어 던지기 — 7·8·9회 아웃 칸을 투수별 색으로 채움
   rundiff  득점·실점 막대 + 차이
   ring10   마지막 10경기 도넛
   series5  준플레이오프 다섯 경기 칸 — 장소(홈 로고) + 이긴 팀 로고/물음표 */
(() => {
  const ttl = (lt, s, mb = 28) => s.title ? `<div style="margin-bottom:${mb}px;${s.cont ? '' : pop(seg(lt, 0, .4))}">${pill(esc(s.title), '#12161F', 44, 'padding:10px 34px')}</div>` : '';
  const same = s => !!(s.cont && s._prev && s._prev.type === s.type);
  /* 10/15 사용자 "KIA·LG 색이 다 같아 보여": 장면마다 팀 색을 바꿔 쓸 수 있게(s.tc = {팀: 색}) — 빨강끼리 맞붙으면 한쪽을 파랑으로 */
  const TC = (s, t) => (s.tc && t && (s.tc[t] || s.tc[(T(t) || {}).code])) || TCOL(t);
  const big = (lt, s) => s.text ? `<div class="big gold" style="margin-top:26px;font-size:${s.size || 64}px;${pop(bp(s, s.textAt ?? 50, .5))}">${br(s.text)}</div>` : '';
  /* 카드 틀 없는 사진: 둥근 모서리 + 그림자만. 사진이 없으면 로고를 그대로(원·상자 없이) */
  const NP = (x, w, h) => { const src = photoSrc(x.img);
    if (!src) return `<div data-anchor="1" style="width:${w}px;height:${h}px;display:flex;align-items:center;justify-content:center;flex:0 0 auto">${LOGOI(x.team, Math.round(Math.min(w, h) * .86), 'filter:drop-shadow(0 16px 30px rgba(18,22,31,.18))')}</div>`;
    return `<div data-anchor="1" style="position:relative;width:${w}px;height:${h}px;flex:0 0 auto;border-radius:30px;overflow:hidden;background:#E9EDF3;box-shadow:0 24px 54px rgba(18,22,31,.24)">${faceImg(src, x, '50% 12%')}</div>`; };
  const NAME = (x, fs = 56, logo = 58) => `<div class="row" style="gap:12px;justify-content:center;align-items:center;margin-top:18px;flex-wrap:nowrap">${x.team && photoSrc(x.img) ? LOGOI(x.team, logo) : ''}<b data-keep="1" style="font-size:${fs}px;font-weight:900;letter-spacing:-2px;white-space:nowrap">${esc(x.name || '')}</b></div>${x.role ? `<div style="font-size:${Math.round(fs * .56)}px;font-weight:800;color:${GRAY};margin-top:4px;white-space:nowrap">${esc(x.role)}</div>` : ''}`;

  /* ── wcrule ──
     {"type":"wcrule","title":"…","teams":[{"team":"LG","rank":"정규시즌 4위","need":2,"have":1,"goal":"1승만 더 하면 통과","at":1},{"team":"두산","rank":"정규시즌 5위","need":2,"have":0,"goal":"2승 해야 통과","at":2}],
      "slotAt":2,"advAt":3,"advLabel":"4위 혜택","goalAt":4} */
  SCENE.wcrule = (lt, s) => {
    const tms = s.teams || [], ps = bp(s, s.slotAt ?? 0, .5), pa = bp(s, s.advAt ?? 50, .6), pg = bp(s, s.goalAt ?? 50, .5);
    const col = (x, i) => {
      const c = TCOL(x.team), pl = bp(s, x.at ?? i, .5);
      let sl = '';
      for (let k = 0; k < (x.need || 2); k++) {
        const filled = k < (x.have || 0), fp = filled ? pa : 0, dp = c01((ps - k * .15) * 1.4);
        sl += `<div style="position:relative;width:150px;height:150px;opacity:${dp};transform:scale(${.7 + .3 * eo(dp)})">
          <div style="position:absolute;inset:0;border-radius:50%;border:7px dashed #BFC7D4;background:#F6F8FB"></div>
          <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:900;color:#B0B8C6">${filled ? '' : '승'}</div>
          ${filled ? `<div style="position:absolute;inset:0;border-radius:50%;background:${c};box-shadow:0 14px 34px ${c}66;display:flex;align-items:center;justify-content:center;color:#fff;font-size:50px;font-weight:900;${ppop(fp)}">1승</div>` : ''}</div>`;
      }
      const adv = (x.have || 0) && s.advLabel ? `<div style="height:62px;margin-top:6px;${ppop(pa)}">${pill(esc(s.advLabel), GOLD_, 34, 'padding:8px 24px;color:#12161F')}</div>` : `<div style="height:62px;margin-top:6px"></div>`;
      return `<div class="col" style="align-items:center;width:640px">
        <div style="${pop(pl)}">${LOGOI(x.team, 210, 'filter:drop-shadow(0 16px 30px rgba(18,22,31,.18))')}</div>
        <div style="font-size:40px;font-weight:900;color:${GRAY};margin-top:8px;opacity:${c01(pl * 1.6)}">${esc(x.rank || '')}</div>
        <div class="row" style="gap:30px;margin-top:22px;flex-wrap:nowrap">${sl}</div>${adv}
        <div style="margin-top:8px;${ppop(pg)}">${pill(esc(x.goal || ''), c, 50, 'padding:12px 38px;box-shadow:0 14px 30px rgba(0,0,0,.18)')}</div></div>`;
    };
    const vs = `<div style="font-size:80px;font-weight:900;font-style:italic;color:#C3CAD6;letter-spacing:-3px;margin-top:-120px">VS</div>`;
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 30)}<div class="row" style="gap:40px;align-items:center;flex-wrap:nowrap">${tms[0] ? col(tms[0], 0) : ''}${vs}${tms[1] ? col(tms[1], 1) : ''}</div></div>`);
  };
  const GOLD_ = '#FFD166';

  /* ── duel ── {"type":"duel","left":{"img","name","team","role","at"},"right":{…},"vsAt":1} */
  SCENE.duel = (lt, s) => {
    const L = s.left || {}, R = s.right || {}, W = s.pw || 420, H = Math.round(W / .774);
    const side = (x, d) => { const p = x.at == null ? seg(lt, d, .5) : bp(s, x.at, .5); return `<div class="col" style="align-items:center;${rise(p, 40)}">${NP(x, W, H)}${NAME(x, 62, 62)}</div>`; };
    const pv_ = s.vsAt == null ? seg(lt, .3, .45) : bp(s, s.vsAt, .45);
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 22)}<div class="row" style="gap:120px;align-items:center;flex-wrap:nowrap">${side(L, 0)}
      <div style="font-size:150px;font-weight:900;font-style:italic;color:${ACC};letter-spacing:-6px;${pop(pv_)}">VS</div>${side(R, .15)}</div></div>`);
  };

  /* ── speedgun ── {"type":"speedgun","title","pitcher":{img,name,team,role},"items":[{"vs":"박해민","v":157,"at":0,"res":"삼진","resAt":2}],"min":100,"max":165,"unit":"킬로"} */
  SCENE.speedgun = (lt, s) => {
    const P_ = s.pitcher || {}, mn = s.min ?? 100, mx = s.max ?? 165, R_ = 150, CX = 190, CY = 190, LEN = Math.PI * R_;
    const g = (x, i) => { const p = bp(s, x.at ?? i, 1.1), e = eo(p), v = mn + (x.v - mn) * e, fr = (v - mn) / (mx - mn), ang = Math.PI * (1 - fr);
      const nx = CX + (R_ - 26) * Math.cos(ang), ny = CY - (R_ - 26) * Math.sin(ang), rp = bp(s, x.resAt ?? 50, .5), c = fr > .85 ? RED : ACC;
      return `<div class="col" style="align-items:center;width:400px;${rise(c01(p * 3), 30)}">
        <div class="row" style="gap:10px;align-items:center;font-size:42px;font-weight:900;letter-spacing:-1.5px">${x.team ? LOGOI(x.team, 50) : ''}<span>${esc(x.vs || '')}</span><span style="color:${GRAY};font-size:34px">상대</span></div>
        <svg viewBox="0 0 380 210" width="380" height="210" style="margin-top:8px">
          <path d="M${CX - R_},${CY} A${R_},${R_} 0 0 1 ${CX + R_},${CY}" fill="none" stroke="#E3E7EE" stroke-width="34" stroke-linecap="round"/>
          <path d="M${CX - R_},${CY} A${R_},${R_} 0 0 1 ${CX + R_},${CY}" fill="none" stroke="${c}" stroke-width="34" stroke-linecap="round" stroke-dasharray="${(LEN * fr).toFixed(1)} 2000"/>
          <line x1="${CX}" y1="${CY}" x2="${nx.toFixed(1)}" y2="${ny.toFixed(1)}" stroke="#12161F" stroke-width="10" stroke-linecap="round"/><circle cx="${CX}" cy="${CY}" r="18" fill="#12161F"/></svg>
        <div class="num" style="font-size:120px;font-weight:900;letter-spacing:-5px;line-height:1;color:${c};margin-top:-6px">${Math.round(v)}<span style="font-size:44px;color:${GRAY};margin-left:8px;letter-spacing:-1px">${esc(s.unit || '킬로')}</span></div>
        <div style="height:80px;margin-top:14px;${ppop(rp)}">${x.res ? pill(esc(x.res), RED, 50, 'padding:10px 40px') : ''}</div></div>`; };
    const W = 400, H = Math.round(W / .774);
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 20)}<div class="row" style="gap:70px;align-items:center;flex-wrap:nowrap">
      <div class="col" style="align-items:center;${rise(seg(lt, 0, .45), 30)}">${NP(P_, W, H)}${NAME(P_, 54, 54)}</div>
      ${(s.items || []).map(g).join('')}</div></div>`);
  };

  /* ── gamestrip ── {"type":"gamestrip","title","teams":{"K":"KIA","L":"LG"},"games":[["3/31","K"],…],"rows":[[0,8],[9,15]],"at":0.3,"step":.06,"dimTo":9,"hideFrom":9,
       "groups":[{"from":0,"to":8,"label":"6월 16일까지 · LG 7승 2패","team":"LG","at":2,"sub":"그중 …","subAt":2.5}]}
       경기마다 이긴 팀 로고(원 안에 통째로) + 날짜. rows 로 줄을 나눈다(기간별). */
  SCENE.gamestrip = (lt, s) => {
    const G_ = s.games || [], n = G_.length, C_ = same(s), rows = s.rows || [[0, n - 1]];
    const mxr = Math.max(...rows.map(r => r[1] - r[0] + 1)), SW = Math.min(s.sw || 168, Math.floor((EP.vertical ? 1040 : 1720) / mxr)), CD = SW - 24;
    const pv = C_ ? (s._prev.groups || []).map(g => g.label) : [], pvs = C_ ? (s._prev.groups || []).filter(g => g.sub).map(g => g.sub) : [];
    const pS = C_ ? (s._prev.hideFrom ?? n) : 0;
    let h = ttl(lt, s, rows.length > 1 ? 22 : 34);
    rows.forEach(([a, b]) => {
      h += `<div style="position:relative;width:${SW * (b - a + 1)}px;margin-bottom:${rows.length > 1 ? 10 : 0}px"><div class="row" style="gap:0;flex-wrap:nowrap">`;
      for (let k = a; k <= b; k++) { const [d, w] = G_[k], tm = (s.teams || {})[w] || w, c = TC(s, tm);
        const p = k >= (s.hideFrom ?? n) ? 0 : k < pS ? 1 : bp(s, (s.at ?? 0) + (k - pS) * (s.step ?? .06), .4), dim = k < (s.dimTo || 0);
        h += `<div class="col" style="width:${SW}px;align-items:center;gap:6px;opacity:${(dim ? .28 : 1) * c01(p * 1.6)};transform:translateY(${(1 - eo(p)) * 30}px)">
          <div style="width:${CD}px;height:${CD}px;border-radius:50%;background:${c}14;border:${Math.round(CD * .06)}px solid ${c};display:flex;align-items:center;justify-content:center;box-shadow:0 10px 22px rgba(18,22,31,.12)">${LOGOI(tm, Math.round(CD * .66))}</div>
          <div class="num" style="font-size:${Math.max(26, Math.round(CD * .2))}px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(d)}</div></div>`; }
      h += `</div>`;
      const gs_ = (s.groups || []).filter(g => g.from >= a && g.to <= b);
      gs_.forEach(g => { const p = pv.includes(g.label) ? 1 : bp(s, g.at ?? 50, .5), c = TC(s, g.team), x0 = (g.from - a) * SW + 10, x1 = (g.to - a + 1) * SW - 10;
        const sp = g.sub ? (pvs.includes(g.sub) ? 1 : bp(s, g.subAt ?? 50, .5)) : 0;
        h += `<div style="position:relative;left:${x0}px;width:${x1 - x0}px;height:96px;margin-top:6px;opacity:${c01(p * 1.6)}">
          <div style="height:22px;border:6px solid ${c};border-top:none;border-radius:0 0 18px 18px;transform-origin:50% 0;transform:scaleX(${.3 + .7 * eo(p)})"></div>
          <div class="row" style="justify-content:center;gap:16px;margin-top:12px;flex-wrap:nowrap"><span style="display:inline-block;${ppop(p)}">${pill(esc(g.label), c, 42, 'padding:8px 28px')}</span>${g.sub ? `<span style="display:inline-block;${ppop(sp)}">${pill(esc(g.sub), '#12161F', 38, 'padding:8px 24px')}</span>` : ''}</div></div>`; });
      if (!gs_.length && rows.length > 1) h += `<div style="height:102px"></div>`;   /* 괄호 자리를 늘 같은 높이로 → 다음 장면에서 괄호가 생겨도 줄이 안 움직임 */
      h += `</div>`;
    });
    B(`<div class="col" style="width:100%;align-items:center">${h}${big(lt, s)}</div>`);
  };

  /* ── faceoff ── {"type":"faceoff","title","left":{img,name,team,role},"right":{…},"rows":[{"k":"LG전 타율","l":"2할 8리","r":"2할 2푼 8리","lv":.208,"rv":.228,"low":false,"at":0,"hide":false}],"text","textAt"}
       lv/rv 가 있으면 가운데에서 바깥으로 자라는 막대(더 좋은 쪽 진하게, low:true 면 작을수록 좋음), 없으면 글 + 앞선 쪽(w:"l"|"r") 표시 */
  SCENE.faceoff = (lt, s) => {
    const L = s.left || {}, R = s.right || {}, rows = s.rows || [], C_ = same(s), PVn = C_ ? (s._prev.rows || []).filter(r => !r.hide).length : 0;
    const CL = s.leftColor || TC(s, L.team), CR = s.rightColor || TC(s, R.team), W = EP.vertical ? (photoSrc(L.img) ? 230 : 170) : (s.pw || 340), H = Math.round(W / .774);
    const sideP = (x, d) => `<div class="col" style="align-items:center;width:${W + 20}px;flex:0 0 auto;${C_ ? '' : rise(seg(lt, d, .45), 30)}">${NP(x, W, photoSrc(x.img) ? H : W)}${NAME(x, 50, 50)}</div>`;
    const allT = rows.every(r => r.lv == null), RH = EP.vertical ? (rows.length >= 5 ? 84 : 100) : rows.length >= 5 ? 100 : 118, KW = 240;
    /* 10/15 사용자 "텍스트랑 사진이 겹쳐": 가운데 표 폭을 화면 폭(본문 1808)에서 양옆 사진 칸을 뺀 만큼으로 계산 — 넘쳐서 글자가 사진 위로 가던 것 */
    const HALF = Math.floor(((EP.vertical ? 1040 : 1700 - 2 * (W + 20) - 60) - KW) / 2), BW = allT ? 0 : Math.max(90, Math.min(180, HALF - 210)), VW = HALF - BW;
    const body = rows.map((r, i) => {
      if (r.hide) return `<div style="height:${RH}px"></div>`;
      const p = i < PVn ? 1 : bp(s, r.at ?? i, .6), e = eo(p), num = r.lv != null && r.rv != null;
      let lw = 0, rw = 0, lb = false, rb = false;
      if (num) { const m = Math.max(1e-9, r.lv, r.rv); lw = r.lv / m * BW * e; rw = r.rv / m * BW * e; lb = r.low ? r.lv < r.rv : r.lv > r.rv; rb = r.low ? r.rv < r.lv : r.rv > r.lv; }
      else { lb = r.w === 'l'; rb = r.w === 'r'; }
      const vstyle = (b, c, tx = '') => `font-size:${num ? (String(tx).length > 5 ? 40 : 50) : 44}px;font-weight:900;letter-spacing:-2px;color:${b ? c : (num ? '#9AA3B2' : '#6A7382')};white-space:nowrap`;
      const chk = c => `<span style="display:inline-flex;width:46px;height:46px;border-radius:50%;background:${c};color:#fff;font-size:30px;font-weight:900;align-items:center;justify-content:center;flex:0 0 auto;${ppop(c01(p * 2 - .6))}">✓</span>`;
      return `<div class="row" style="height:${RH}px;gap:0;flex-wrap:nowrap;align-items:center;opacity:${c01(p * 1.6)};border-top:${i ? 3 : 0}px solid #EDF0F4">
        <div class="row" style="width:${VW + (num ? BW : 0)}px;justify-content:flex-end;gap:14px;flex-wrap:nowrap">${!num && lb ? chk(CL) : ''}<span class="num" style="${vstyle(lb || (!num && !rb), CL, r.l)}">${esc(r.l || '')}</span>${num ? `<div style="flex:0 0 auto;width:${lw.toFixed(1)}px;height:46px;border-radius:23px 0 0 23px;background:${lb ? CL : '#D5DAE2'}"></div>` : ''}</div>
        <div style="width:${KW}px;flex:0 0 ${KW}px;padding:0 26px;box-sizing:border-box;text-align:center;font-size:36px;font-weight:900;letter-spacing:-1.5px;color:#3B4A63;line-height:1.15">${br(r.k || '')}</div>
        <div class="row" style="width:${VW + (num ? BW : 0)}px;justify-content:flex-start;gap:14px;flex-wrap:nowrap">${num ? `<div style="flex:0 0 auto;width:${rw.toFixed(1)}px;height:46px;border-radius:0 23px 23px 0;background:${rb ? CR : '#D5DAE2'}"></div>` : ''}<span class="num" style="${vstyle(rb || (!num && !lb), CR, r.r)}">${esc(r.r || '')}</span>${!num && rb ? chk(CR) : ''}</div></div>`;
    }).join('');
    const mid = `<div class="col" style="align-items:center;gap:0">${body}</div>`;
    if (EP.vertical) { B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 20)}<div class="row" style="gap:60px;align-items:center;flex-wrap:nowrap;margin-bottom:24px">${sideP(L, 0)}<div style="font-size:60px;font-weight:900;font-style:italic;color:#C3CAD6">vs</div>${sideP(R, .12)}</div>${mid}${big(lt, s)}</div>`); return; }
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 20)}<div class="row" style="gap:30px;align-items:center;flex-wrap:nowrap">${sideP(L, 0)}${mid}${sideP(R, .12)}</div>${big(lt, s)}</div>`);
  };

  /* ── abdots ── {"type":"abdots","left":{투수},"right":{타자 또는 팀},"total":"10타수 1안타","totalAt":2,
       "groups":[{"k":"H","n":1,"at":2},{"k":"O","n":5,"at":2,"to":"K","toAt":3},{"k":"O","n":4,"at":2}],"chips":[{"label":"볼넷 5개","at":1,"c":"#16A34A"}],"cols":10}
       k: H 안타 · HR 홈런 · K 삼진 · O 아웃 */
  const DK = { H: ['안타', '#16A34A', '#fff'], HR: ['홈런', '#E8A100', '#fff'], K: ['삼진', '#E5484D', '#fff'], O: ['아웃', '#EEF1F5', '#9AA3B2'] };
  SCENE.abdots = (lt, s) => {
    const L = s.left || {}, R = s.right || {}, C_ = same(s) && (s._prev.left || {}).img === L.img, W = EP.vertical ? 230 : (s.pw || 340), H = Math.round(W / .774);
    const dots = []; (s.groups || []).forEach(g => { for (let k = 0; k < (g.n || 1); k++) dots.push(g); });
    const n = dots.length, cols = s.cols || Math.min(n, n > 12 ? 7 : 10), D_ = n > 12 ? 92 : 104, GAP = 16;
    const dh = dots.map((g, k) => { const p = bp(s, (g.at ?? 0) + k * .03, .35), tp = g.to ? bp(s, g.toAt ?? 50, .4) : 0, kk = g.to && tp > .5 ? g.to : g.k, [lb, bg, fg] = DK[kk] || DK.O;
      return `<div style="width:${D_}px;height:${D_}px;border-radius:50%;background:${bg};border:${kk === 'O' ? `4px solid #DCE1E8` : '0'};display:flex;align-items:center;justify-content:center;color:${fg};font-size:${Math.round(D_ * .3)}px;font-weight:900;letter-spacing:-1px;box-shadow:${kk === 'O' ? 'none' : `0 10px 22px ${bg}66`};opacity:${c01(p * 1.6)};transform:scale(${(.5 + .5 * eb(p)) * (g.to && tp > 0 && tp < 1 ? 1 + .25 * Math.sin(Math.PI * tp) : 1)})">${lb}</div>`; });
    const grid = `<div style="display:grid;grid-template-columns:repeat(${cols},${D_}px);gap:${GAP}px;justify-content:center">${dh.join('')}</div>`;
    const tp = bp(s, s.totalAt ?? 0, .5);
    const chips = (s.chips || []).map(c => `<span style="${ppop(bp(s, c.at ?? 50, .5))};display:inline-block">${pill(esc(c.label), c.c || '#12161F', 40, 'padding:8px 28px')}</span>`).join('');
    const mid = `<div class="col" style="align-items:center;gap:26px;width:${Math.max(cols * (D_ + GAP) + 20, 7 * (92 + 16) + 20)}px">
      <div class="num" style="font-size:84px;font-weight:900;letter-spacing:-3px;line-height:1;${pop(tp)}">${esc(s.total || '')}</div>${grid}
      ${chips ? `<div class="row" style="gap:18px;justify-content:center;min-height:70px">${chips}</div>` : ''}</div>`;
    const side = (x, d, keep) => `<div class="col" style="align-items:center;flex:0 0 auto;${keep ? '' : rise(seg(lt, d, .45), 30)}">${NP(x, W, photoSrc(x.img) ? H : W)}${NAME(x, 48, 48)}</div>`;
    const pair = `${side(L, 0, C_)}<div style="font-size:60px;font-weight:900;font-style:italic;color:#C3CAD6">vs</div>${side(R, .12, C_ && (s._prev.right || {}).img === R.img)}`;
    if (EP.vertical) { B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 20)}<div class="row" style="gap:50px;align-items:center;flex-wrap:nowrap;margin-bottom:26px">${pair}</div>${mid}${big(lt, s)}</div>`); return; }
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 20)}<div class="row" style="gap:50px;align-items:center;flex-wrap:nowrap">${pair}${mid}</div>${big(lt, s)}</div>`);
  };

  /* ── relay ── {"type":"relay","title","team":"LG","inn":[7,8,9],"pitchers":[{"name":"케네디","outs":3,"at":1}, …],"brace":{"label","at"},"note":{"inn":0,"label","at"},"text","textAt"} */
  SCENE.relay = (lt, s) => {
    const inn = s.inn || [7, 8, 9], CW = EP.vertical ? 112 : 160, IW = CW * 3, GAP = 34, PAL = s.colors || ['#C30452', '#3B4A63', '#E8A100', '#1F9D55', '#2563EB'];
    const cells = []; (s.pitchers || []).forEach((p_, i) => { for (let k = 0; k < (p_.outs || 3); k++) cells.push({ i, p: p_, first: k === 0 }); });
    let h = ttl(lt, s, 34);
    h += `<div class="row" style="gap:${GAP}px;flex-wrap:nowrap;align-items:flex-start">` + inn.map((n_, ii) => {
      let row = '';
      for (let k = 0; k < 3; k++) { const c = cells[ii * 3 + k]; const p = c ? bp(s, c.p.at ?? 0, .45) : 0, col = c ? PAL[c.i % PAL.length] : '#EEF1F5';
        const run = c ? cells.filter((z, j) => z.i === c.i && Math.floor(j / 3) === ii).length : 0, firstHere = c && (k === 0 || cells[ii * 3 + k - 1].i !== c.i);
        row += `<div style="position:relative;width:${CW}px;height:130px;background:#EEF1F5;border-right:${k < 2 ? 4 : 0}px solid #fff">
          <div style="position:absolute;inset:0;background:${col};transform-origin:0 50%;transform:scaleX(${eo(p)})"></div>
          ${firstHere ? `<div style="position:absolute;left:0;top:0;height:100%;width:${run * CW}px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:${run === 1 ? 34 : 44}px;font-weight:900;letter-spacing:-1.5px;white-space:nowrap;z-index:2;opacity:${c01(p * 2 - .4)}">${esc(c.p.name)}</div>` : ''}</div>`; }
      return `<div class="col" style="align-items:center;gap:14px;${rise(seg(lt, ii * .1, .4), 24)}"><div style="font-size:46px;font-weight:900">${n_}회</div>
        <div class="row" style="gap:0;border-radius:24px;overflow:hidden;flex-wrap:nowrap;box-shadow:0 12px 28px rgba(18,22,31,.12)">${row}</div>
        <div class="row" style="gap:0;flex-wrap:nowrap">${[1, 2, 3].map(o => `<div style="width:${CW}px;text-align:center;font-size:26px;font-weight:800;color:#9AA3B2">아웃 ${o}</div>`).join('')}</div></div>`; }).join('') + `</div>`;
    if (s.note) { const p = bp(s, s.note.at ?? 50, .5); h += `<div style="width:${IW * inn.length + GAP * (inn.length - 1)}px;margin-top:6px;height:76px;position:relative"><div style="position:absolute;left:${(s.note.inn || 0) * (IW + GAP)}px;width:${IW}px;text-align:center;${ppop(p)}">${pill(esc(s.note.label), '#12161F', 34, 'padding:8px 24px')}</div></div>`; }
    if (s.brace) { const p = bp(s, s.brace.at ?? 50, .5), Wd = IW * inn.length + GAP * (inn.length - 1);
      h += `<div style="width:${Wd}px;margin-top:10px;opacity:${c01(p * 1.6)}"><div style="height:26px;border:6px solid ${TCOL(s.team || 'LG')};border-top:none;border-radius:0 0 18px 18px"></div><div style="text-align:center;margin-top:16px;${ppop(p)}">${pill(esc(s.brace.label), TCOL(s.team || 'LG'), 48, 'padding:10px 34px')}</div></div>`; }
    B(`<div class="col" style="width:100%;align-items:center">${h}${big(lt, s)}</div>`);
  };

  /* ── rundiff ── {"type":"rundiff","title","rows":[{"team":"KIA","rs":769,"ra":664,"at":1}],"max":850} */
  SCENE.rundiff = (lt, s) => {
    const rows = s.rows || [], mx = s.max || Math.max(...rows.map(r => Math.max(r.rs, r.ra))) * 1.05, BW = EP.vertical ? 420 : 760;
    const one = (r, i) => { const p = bp(s, r.at ?? i, .9), e = eo(p), d = r.rs - r.ra, dc = d >= 0 ? GREEN : RED, dp = c01(p * 1.6 - .7);
      const bar = (lb, v, c) => `<div class="row" style="gap:16px;align-items:center;flex-wrap:nowrap"><div style="width:96px;font-size:36px;font-weight:900;color:${c}">${lb}</div>
        <div style="width:${(v / mx * BW * e).toFixed(1)}px;height:54px;border-radius:0 27px 27px 0;background:${c}"></div><div class="num" style="font-size:44px;font-weight:900;letter-spacing:-1.5px;color:${c};opacity:${c01(p * 2)}">${Math.round(v * e)}점</div></div>`;
      return `<div class="row" style="gap:40px;align-items:center;flex-wrap:nowrap;opacity:${c01(p * 3)}">
        <div style="width:170px;display:flex;justify-content:center">${LOGOI(r.team, 160)}</div>
        <div class="col" style="gap:14px;align-items:flex-start;width:${BW + 300}px">${bar('득점', r.rs, '#2563EB')}${bar('실점', r.ra, '#9AA3B2')}</div>
        <div class="num" style="width:300px;font-size:120px;font-weight:900;letter-spacing:-5px;color:${dc};${ppop(dp)}">${d >= 0 ? '+' : '−'}${Math.abs(d)}</div></div>`; };
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 30)}<div class="col" style="gap:50px;align-items:flex-start">${rows.map(one).join('')}</div>${big(lt, s)}</div>`);
  };

  /* ── ring10 ── {"type":"ring10","title","items":[{"team":"KIA","w":7,"l":3,"at":1}]} */
  SCENE.ring10 = (lt, s) => {
    const it = s.items || [], RR = 170, SW = 52, CX = 210;
    const one = (x, i) => { const p = bp(s, x.at ?? i, 1.0), n = x.w + x.l, c = TC(s, x.team), a0 = -Math.PI / 2, step = 2 * Math.PI / n, gap = .07;
      let segs = '';
      for (let k = 0; k < n; k++) { const sp = c01(p * n * .9 - k * .8), win = k < x.w, a1 = a0 + k * step + gap / 2, a2 = a1 + (step - gap) * eo(sp);
        if (sp <= 0) continue; const P1 = [CX + RR * Math.cos(a1), CX + RR * Math.sin(a1)], P2 = [CX + RR * Math.cos(a2), CX + RR * Math.sin(a2)];
        segs += `<path d="M${P1[0].toFixed(1)},${P1[1].toFixed(1)} A${RR},${RR} 0 0 1 ${P2[0].toFixed(1)},${P2[1].toFixed(1)}" fill="none" stroke="${win ? c : '#D5DAE2'}" stroke-width="${SW}"/>`; }
      return `<div class="col" style="align-items:center;gap:6px;${rise(c01(p * 3), 30)}">
        <div style="position:relative;width:${CX * 2}px;height:${CX * 2}px"><svg viewBox="0 0 ${CX * 2} ${CX * 2}" width="${CX * 2}" height="${CX * 2}" style="position:absolute;inset:0">
          <circle cx="${CX}" cy="${CX}" r="${RR}" fill="none" stroke="#F1F3F7" stroke-width="${SW}"/>${segs}</svg>
          <div class="col" style="position:absolute;inset:0;align-items:center;justify-content:center;gap:0">${LOGOI(x.team, 120)}</div></div>
        <div class="num" style="font-size:76px;font-weight:900;letter-spacing:-3px;margin-top:6px"><span style="color:${c}">${x.w}승</span> <span style="color:#9AA3B2">${x.l}패</span></div></div>`; };
    const leg = `<div class="row" style="gap:28px;margin-top:12px;font-size:32px;font-weight:800;color:${GRAY}"><span>한 칸 = 한 경기</span></div>`;
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 24)}<div class="row" style="gap:180px;flex-wrap:nowrap">${it.map(one).join('')}</div>${leg}</div>`);
  };

  /* ── series5 ── {"type":"series5","title","games":[{"n":"1차전","venue":"광주","home":"KIA","win":"KIA"|"LG"|"?"|null,"off":false,"glow":"LG","tag":"만약","at":0}],
       "brace":{"from":2,"to":3,"label","team","at"},"pills":[{"label","at","c"}]} */
  SCENE.series5 = (lt, s) => {
    const G_ = s.games || [], SW = EP.vertical ? 210 : 300, C_ = same(s), PG = C_ ? (s._prev.games || []) : [];
    const J = x => JSON.stringify(x || {});
    let h = ttl(lt, s, 30);
    h += `<div style="position:relative"><div class="row" style="gap:0;flex-wrap:nowrap;align-items:flex-start">` + G_.map((g, k) => {
      const keep = C_ && PG[k] && J({ ...PG[k], at: 0 }) === J({ ...g, at: 0 }), p = keep ? 1 : bp(s, g.at ?? 0, .5), c = g.win && g.win !== '?' ? TC(s, g.win) : '#BFC7D4';
      const glow = g.glow ? `<div style="position:absolute;left:8px;right:8px;top:-14px;bottom:-14px;border-radius:34px;background:${TC(s, g.glow)}18;border:5px solid ${TC(s, g.glow)};${C_ && PG[k] && PG[k].glow === g.glow ? '' : `opacity:${c01(bp(s, g.glowAt ?? g.at ?? 0, .5) * 1.6)}`}"></div>` : '';
      const res = g.off ? `<div style="width:170px;height:170px;border-radius:50%;border:6px dashed #D5DAE2;display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:800;color:#B0B8C6;text-align:center;line-height:1.2">안 열림</div>`
        : g.win === '?' ? `<div style="width:170px;height:170px;border-radius:50%;border:7px dashed #9AA3B2;display:flex;align-items:center;justify-content:center;font-size:96px;font-weight:900;color:#9AA3B2;${ppop(p)}">?</div>`
        : g.win ? `<div style="width:170px;height:170px;border-radius:50%;background:#fff;border:8px solid ${c};display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px ${c}44;${ppop(p)}">${LOGOI(g.win, 118)}</div>`
        : `<div style="width:170px;height:170px;border-radius:50%;border:6px dashed #D5DAE2"></div>`;
      return `<div class="col" style="position:relative;width:${SW}px;align-items:center;gap:14px;opacity:${g.off ? .55 : 1}">${glow}
        <div style="position:relative;font-size:44px;font-weight:900">${esc(g.n)}</div>
        <div class="row" style="position:relative;gap:8px;align-items:center;font-size:36px;font-weight:800;color:#3B4A63;flex-wrap:nowrap">${LOGOI(g.home, 52)}<span>${esc(g.venue)}</span></div>
        <div style="position:relative;margin-top:6px">${res}</div>
        <div style="position:relative;height:56px">${g.tag ? `<div style="${ppop(p)}">${pill(esc(g.tag), '#12161F', 30, 'padding:6px 20px')}</div>` : ''}</div></div>`; }).join('') + `</div>`;
    if (s.brace) { const b = s.brace, p = C_ && s._prev.brace && s._prev.brace.label === b.label ? 1 : bp(s, b.at ?? 50, .5), c = TC(s, b.team || 'LG');
      h += `<div style="position:relative;left:${b.from * SW + 20}px;width:${(b.to - b.from + 1) * SW - 40}px;margin-top:4px;opacity:${c01(p * 1.6)}"><div style="height:24px;border:6px solid ${c};border-top:none;border-radius:0 0 18px 18px"></div>
        <div style="text-align:center;margin-top:14px;${ppop(p)}">${pill(esc(b.label), c, 42, 'padding:8px 28px')}</div></div>`; }
    h += `</div>`;
    const pl = (s.pills || []).map(q => `<span style="display:inline-block;${C_ && (s._prev.pills || []).some(z => z.label === q.label) ? '' : ppop(bp(s, q.at ?? 50, .5))}">${pill(esc(q.label), q.c || '#12161F', 42, 'padding:8px 28px')}</span>`).join('');
    B(`<div class="col" style="width:100%;align-items:center">${h}${pl ? `<div class="row" style="gap:22px;margin-top:22px;justify-content:center">${pl}</div>` : ''}${big(lt, s)}</div>`);
  };


  /* ── pstat ── 인물 한 명 + 기록 (profile 대신, 10/15 사용자 "그래프 붙으면 사진이 너무 작다 · 카드 글이 구구절절").
     사진은 늘 같은 크기(480×620, 카드 틀 없음), 오른쪽에 이름 + 그림(viz: trend 가로 막대 · steps 시간 줄 · stamp 도장 · duo 큰 숫자 둘) + 기록(stats: 칸 없이 숫자만).
     {"type":"pstat","img","team","name","sub","viz":[…],"stats":[{"k","v","at","hi"}],"text","textAt"} — viz·stats 형식은 profile 과 같다 */
  SCENE.pstat = (lt, s) => {
    const V = !!EP.vertical, PW = V ? 400 : 480, PH_ = Math.round(PW / .774), RW = V ? 700 : 1000, BWm = V ? 300 : 560, NF = V ? 92 : 108;
    const pr = s._prev && s._prev.type === 'pstat' ? s._prev : null, J = x => JSON.stringify(x);
    const keepP = !!(pr && ((photoSrc(pr.img) && photoSrc(pr.img) === photoSrc(s.img)) || (!s.img && pr.team === s.team && !pr.img)));
    const keepN = !!(pr && pr.name === s.name), had = x => pr && [...(pr.viz || []), ...(pr.stats || [])].some(y => J(y) === J(x));
    const P = (x, d = .5) => had(x) ? 1 : bp(s, x.at ?? 0, d);
    const tc = s.team ? TCOL(s.team) : ACC, colOf = c => c === 'bad' ? RED : c === 'good' ? GREEN : c === 'gold' ? '#E8A100' : (c || '#3B4A63');
    const photo = `<div style="flex:0 0 auto;${keepP ? '' : rise(seg(lt, 0, .5), 40)}">${NP({ img: s.img, team: s.team, focus: s.focus }, PW, PH_)}</div>`;
    const head = `<div style="${keepN ? '' : pop(seg(lt, .05, .45))};transform-origin:left center"><div data-keep="1" style="font-size:${NF}px;font-weight:900;letter-spacing:-4px;line-height:1.05;white-space:nowrap">${esc(s.name || '')}</div>
      ${s.sub ? `<div style="margin-top:12px">${pill(esc(s.sub), tc, V ? 32 : 36, 'padding:6px 22px')}</div>` : ''}</div>`;
    const blocks = (s.viz || []).map(z => {
      if (z.type === 'trend') { const its = z.items || [];
        /* 10/15 사용자 "기존 그래프가 작아지면서 새 그래프가 생겨": 같은 사람 묶음 전체에서 가장 큰 값으로 막대 길이를 정한다 → 이어지는 장면에서 막대가 안 줄어든다 */
        const chainV = []; for (let q = s; q && q.type === 'pstat' && q.name === s.name; q = q._prev) (q.viz || []).forEach(w => w.type === 'trend' && (w.items || []).forEach(x => chainV.push(+x.v)));
        for (let q = s._next; q && q.type === 'pstat' && q.name === s.name; q = q._next) (q.viz || []).forEach(w => w.type === 'trend' && (w.items || []).forEach(x => chainV.push(+x.v)));
        const mx = Math.max(...chainV, ...its.map(x => +x.v)) * 1.05 || 1;
        return `<div class="col" style="gap:14px;align-items:flex-start">${z.title ? `<div style="font-size:34px;font-weight:900;color:${GRAY}">${esc(z.title)}</div>` : ''}` + its.map(x => { const q = had(z) && (pr.viz || []).some(y => (y.items || []).some(w => J(w) === J(x))) ? 1 : bp(s, x.at ?? 0, .6), c = colOf(x.c);
          return `<div class="row" style="gap:18px;align-items:center;flex-wrap:nowrap;opacity:${c01(q * 2)}"><div style="width:${V ? 170 : 200}px;font-size:${V ? 34 : 38}px;font-weight:800;color:#3B4A63;white-space:nowrap">${esc(x.x)}</div>
            <div style="width:${(x.v / mx * BWm * eo(q)).toFixed(1)}px;height:${V ? 50 : 58}px;border-radius:0 29px 29px 0;background:${c}"></div>
            <div class="num" style="font-size:${V ? 54 : 64}px;font-weight:900;letter-spacing:-2px;color:${c};white-space:nowrap">${esc(x.vt)}</div></div>`; }).join('') + `</div>`; }
      if (z.type === 'steps') { const its = z.items || [];
        return `<div class="col" style="gap:${its.length > 3 ? 8 : 16}px;align-items:flex-start;position:relative">` + its.map((x, k) => { const q = had(z) ? 1 : bp(s, x.at ?? 0, .45), c = colOf(x.c);
          return `<div class="row" style="gap:20px;align-items:center;flex-wrap:nowrap;${rise(q, 20)}"><div style="width:${V ? 170 : 210}px;font-size:${V ? 32 : 36}px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(x.d)}</div>
            <div style="width:26px;height:26px;border-radius:50%;background:${c};flex:0 0 auto"></div>
            <div style="font-size:${its.length > 3 ? (V ? 40 : 46) : (V ? 46 : 54)}px;font-weight:900;letter-spacing:-1.5px;color:${x.c ? c : TXT};white-space:nowrap">${br(String(x.t).replace(/\n/g, ' '))}</div></div>`; }).join('') + `</div>`; }
      if (z.type === 'stamp') { const q = P(z, .45), c = z.c === 'bad' ? RED : z.c === 'good' ? GREEN : '#E8A100';
        return `<div style="display:inline-block;border:8px solid ${c};color:${c};border-radius:22px;padding:10px 30px;font-size:${Math.min(z.size || 60, V ? 50 : 60)}px;font-weight:900;letter-spacing:-2px;white-space:nowrap;opacity:${c01(q * 1.6)};transform:rotate(-3deg) scale(${q <= 0 ? 1.6 : 1.6 - .6 * eo(q)})">${esc(z.t)}</div>`; }
      if (z.type === 'duo') return `<div class="row" style="gap:70px;flex-wrap:nowrap">` + (z.items || []).map(x => { const q = had(z) ? 1 : bp(s, x.at ?? 0, .45), c = colOf(x.c);
          return `<div class="col" style="align-items:flex-start;gap:2px;${pop(q)}"><div style="font-size:34px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(x.k)}</div><div class="num" style="font-size:${V ? 80 : 96}px;font-weight:900;letter-spacing:-3px;color:${c};line-height:1.05;white-space:nowrap">${esc(x.v)}</div></div>`; }).join('') + `</div>`;
      return '';
    }).join('');
    const sts = (s.stats || []).filter(x => !x.ghost);
    const stH = sts.length ? `<div class="row" style="gap:${V ? 36 : 54}px;flex-wrap:wrap;align-items:flex-end">` + sts.map(x => { const q = P(x, .45), c = x.hi ? tc : TXT;
      return `<div class="col" style="align-items:flex-start;gap:0;${rise(q, 20)}"><div style="font-size:${V ? 30 : 34}px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(x.k)}</div><div class="num" style="font-size:${V ? 54 : 64}px;font-weight:900;letter-spacing:-2px;color:${c};white-space:nowrap;line-height:1.1">${esc(x.v)}</div></div>`; }).join('') + `</div>` : '';
    const right = `<div class="col" style="width:${RW}px;flex:0 0 ${RW}px;align-items:flex-start;justify-content:flex-start;text-align:left;gap:${V ? 26 : 34}px;height:${PH_}px;padding-top:${V ? 10 : 40}px;box-sizing:border-box">${head}${stH}${blocks}${s.text ? `<div class="big gold" style="font-size:${s.size || 64}px;${pop(bp(s, s.textAt ?? 50, .5))}">${br(s.text)}</div>` : ''}</div>`;
    B(`<div class="row" style="width:100%;gap:${V ? 44 : 64}px;justify-content:center;align-items:center;flex-wrap:nowrap">${photo}${right}</div>`);
  };

  /* ── pgroup ── 인물 2~3명 + 큰 기록 (people 카드 대신). {"type":"pgroup","title","items":[{"img","name","team","v","k","at"}],"vAt"} */
  SCENE.pgroup = (lt, s) => {
    const V = !!EP.vertical, it = s.items || [], W = it.length >= 3 ? 280 : (V ? 300 : 380), H = Math.round(W / .774);
    const one = (x, i) => { const p = bp(s, x.at ?? 0, .5), q = bp(s, x.vAt ?? s.vAt ?? 0, .5), c = TCOL(x.team);
      return `<div class="row" style="gap:30px;align-items:center;flex-wrap:nowrap;${rise(p, 30)}">${NP(x, W, H)}
        <div class="col" style="align-items:flex-start;gap:6px"><div class="row" style="gap:12px;align-items:center;flex-wrap:nowrap">${x.team ? LOGOI(x.team, 56) : ''}<b style="font-size:62px;font-weight:900;letter-spacing:-2px;white-space:nowrap">${esc(x.name)}</b></div>
          <div style="margin-top:14px;font-size:34px;font-weight:800;color:${GRAY};white-space:nowrap;${pop(q)}">${br(x.k || '')}</div>
          <div class="num" style="font-size:${V ? 64 : 76}px;font-weight:900;letter-spacing:-3px;color:${c};white-space:nowrap;line-height:1.05;${pop(q)}">${br(x.v || '')}</div></div></div>`; };
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, 30)}<div class="row" style="gap:${V ? 50 : 90}px;flex-wrap:${V ? 'wrap' : 'nowrap'};justify-content:center">${it.map(one).join('')}</div>${big(lt, s)}</div>`);
  };

  Object.assign(MOTION, { wcrule: () => .8, duel: () => .9, speedgun: () => 1.2, gamestrip: () => 1.2, faceoff: () => .9, abdots: () => 1.0, relay: () => .9, rundiff: () => 1.0, ring10: () => 1.0, series5: () => .8, pstat: () => .9, pgroup: () => .9 });
})();
/* @@PS2_1015END */
})();
/* @@PS1015END */
