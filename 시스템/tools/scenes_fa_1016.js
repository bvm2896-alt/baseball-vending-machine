/* @@FA1016 */
/* 10/16 롱폼⑯ 「올겨울 FA 대어 몸값 예상」 — 억 단위 몸값 장면들. tools/inject_fa_1016.py 가 두 템플릿 function render 앞에 넣는다.
   pricebar  몸값 눈금(0~150억) 위에 실제 계약(얼굴 원 + '이름 65억' 알약 + 눈금까지 줄)과 내 예상 범위(눈금 아래 색 띠)를 올린다.
     {"type":"pricebar","title","max":150,"marks":[{"v":65,"name":"박해민","sub":"4년","img","team","at","row","ghost":true}],
      "bands":[{"from":15,"to":30,"name":"정수빈","img","team","label":"15억~30억","tag":"7위","at"}],"line":{"v":100,"label":"100억","at"},"text","textAt"}
     같은 chain 이면 앞 장면에 있던 표시·띠는 그대로(다시 안 뜸), 새 것만 뜬다. 눈금도 그대로.
   pricerows 정리 표 — 선수마다 한 줄(순위·얼굴·이름) + 같은 눈금 위 예상 띠. {"rows":[{"rank","name","img","team","from","to","at","hide"}],"line":{v,label,at},"max"}
   compgrade FA 보상 등급 — A·B·C 칸마다 '연봉 지폐 ×n' + '보상 선수 1명' 그림. {"cols":[{"g":"A","opt":[{"bills":2,"person":true},{"bills":3}],"at"}],"hi":"B"}
   comptrans 보상 흐름 — 선수가 원래 팀 → 새 팀으로, 돈·선수가 새 팀 → 원래 팀으로. {"moveAt","backAt"}
   tline     날짜 줄 — 점 + 날짜 + 두세 단어. {"items":[{"d","t","at","c"}]} */
(() => {
  const TC_ = n => { const c = TEAMCOL[(T(n) || {}).code] || '#3B4A63'; return c === '#4A4A4A' ? '#12161F' : c; };
  const LG_ = (n, px, st = '') => `<img src="${LOGO[(T(n) || {}).code] || ''}" style="width:${px}px;height:${px}px;object-fit:contain;display:block;${st}">`;
  const pp = p => `opacity:${c01(p * 1.6)};transform:scale(${p <= 0 ? .5 : .5 + .5 * eb(p)})`;
  const PL = (txt, bg, fs = 34, extra = '') => `<span style="display:inline-block;background:${bg};color:#fff;font-size:${fs}px;font-weight:900;padding:6px 22px;border-radius:999px;letter-spacing:-1px;white-space:nowrap;${extra}">${txt}</span>`;
  const P = (s, k, d = .5) => { if (k == null || k < 0) return 1; if (k >= 50) return 0; const b = brP(s, k, d); return b == null ? 1 : b; };
  const circ = (x, D) => { const src = photoSrc(x.img), c = x.team ? TC_(x.team) : '#3B4A63';
    return `<div style="width:${D}px;height:${D}px;border-radius:50%;overflow:hidden;position:relative;flex:0 0 auto;background:#E9EDF3;border:5px solid ${c};box-sizing:border-box;box-shadow:0 10px 24px rgba(18,22,31,.2)">${src ? `<img src="${src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${esc(x.focus || '50% 14%')}">` : (x.team ? LG_(x.team, D - 16, 'margin:3px') : '')}</div>`; };
  const prevOf = (s, type) => s._chain && s._prev && s._prev.type === type ? s._prev : null;
  const ttl = (lt, s, still) => s.title ? `<div class="title" style="font-size:52px;font-weight:900;text-align:center;margin-bottom:18px;${still ? '' : pop(seg(lt, 0, .4))}">${br(s.title)}</div>` : '';
  const big = (s, keep) => s.text ? `<div class="big gold" style="margin-top:18px;font-size:${s.size || 64}px;text-align:center;${keep ? '' : pop(P(s, s.textAt ?? 0, .5))}">${br(s.text)}</div>` : '';

  /* ── pricebar ── */
  /* 줄(row)은 묶음(chain) 전체 표시를 한꺼번에 보고 자동으로 정한다 — 알약끼리 겹치지 않게, 묶음 안에서는 자리가 안 바뀌게 */
  const pillW = m => { const t = `${m.name} ${m.vt || m.v + '억'}${m.sub ? ' ' + m.sub : ''}`; let w = 0; for (const ch of t) w += /[가-힣]/.test(ch) ? 35 : ch === ' ' ? 10 : 21; return Math.round(w + 50); };
  SCENE.pricebar = (lt, s) => {
    const MX = s.max || 150, W = s.w || 1560, px = v => v / MX * W, pr = prevOf(s, 'pricebar');
    const CH = (CHAINS[s._cid] || []).map(j => SC[j]).filter(x => x && x.type === 'pricebar');
    const ALL = CH.length ? CH : [s];
    const uni = []; ALL.forEach(x => (x.marks || []).forEach(m => { if (!uni.some(u => u.name === m.name && u.v === m.v)) uni.push(m); }));
    uni.sort((p_, q_) => p_.v - q_.v);
    const D = 112, RS = 188, LAY = {}, pills = [], circs = [];
    /* 줄 자동 배치: 같은 줄에서 알약(가운데 → 오른쪽으로 → 왼쪽으로)·얼굴 원이 안 겹치는 가장 낮은 줄 */
    uni.forEach((m, k) => { const x = px(m.v), w = pillW(m), cw = (m.imgs ? m.imgs.length : 1) * (D + 8), nx = uni[k + 1], tight = nx && px(nx.v) - x < (w + pillW(nx)) / 2 + 14;
      for (let r = 0; r < 6; r++) {
        if (circs.some(o => o.r === r && Math.abs(o.x - x) < (o.w + cw) / 2 + 6)) continue;
        const C_ = [x - w / 2, x + w / 2], R_ = [x - D / 2, x - D / 2 + w], L_ = [x + D / 2 - w, x + D / 2], opts = tight ? [L_, C_, R_] : [C_, R_, L_];
        const ok = opts.find(([a_, b_]) => a_ >= -20 && b_ <= W + 20 && !pills.some(o => o.r === r && a_ < o.b + 14 && b_ > o.a - 14));
        if (ok) { pills.push({ r, a: ok[0], b: ok[1] }); circs.push({ r, x, w: cw }); LAY[m.name + '|' + m.v] = { r, a: ok[0], w }; return; }
      }
      LAY[m.name + '|' + m.v] = { r: 0, a: x - w / 2, w }; });
    const rowsN = Math.max(1, ...Object.values(LAY).map(o => o.r + 1));
    const anyBand = ALL.some(x => (x.bands || []).length), anyTxt = ALL.some(x => x.text);
    const AX = 40 + rowsN * RS, H = AX + (anyBand ? 236 : 80);
    const had = (m, key) => pr && (pr[key] || []).some(o => o.name === m.name && (key === 'marks' ? o.v === m.v : o.from === m.from && o.to === m.to));
    let h = `<div style="position:absolute;left:0;top:${AX}px;width:${W}px;height:12px;border-radius:6px;background:#C9D0DB"></div>`;
    for (let v = 0; v <= MX; v += 25) h += `<div style="position:absolute;left:${px(v) - 2}px;top:${AX - 8}px;width:4px;height:28px;background:#AEB6C3"></div>
      <div class="num" style="position:absolute;left:${px(v)}px;top:${AX + 24}px;translate:-50% 0;font-size:34px;font-weight:800;color:#8A93A3;white-space:nowrap">${v}${v ? '억' : ''}</div>`;
    const ln = s.line || (ALL.find(x => x.line) || {}).line;
    if (ln) { const q = pr && pr.line && pr.line.v === ln.v ? 1 : (s.line ? P(s, ln.at ?? 0, .5) : 0);
      h += `<div style="position:absolute;left:${px(ln.v) - 3}px;top:0px;width:6px;height:${AX + 12}px;background:repeating-linear-gradient(${RED} 0 14px,transparent 14px 24px);opacity:${c01(q * 1.5)}"></div>
        <div style="position:absolute;left:${px(ln.v)}px;top:-52px;translate:-50% 0;${pp(q)}">${PL(esc(ln.label || ln.v + '억'), RED, 36)}</div>`; }
    const ms = (s.marks || []).map((m, i) => ({ m, q: had(m, 'marks') ? 1 : P(s, m.at ?? i * .3, .5), L: LAY[m.name + '|' + m.v] || { r: 0, a: px(m.v) - 100, w: 200 } }));
    /* 줄(막대)을 먼저 다 그리고 → 알약·얼굴을 위에(다른 표시의 줄이 알약을 가로지르지 않게) */
    ms.forEach(({ m, q, L: Lr }) => { const cy = AX - 26 - Lr.r * RS, c = m.team ? TC_(m.team) : '#3B4A63';
      h += `<div style="position:absolute;left:${px(m.v) - 3}px;top:${cy}px;width:6px;height:${AX - cy}px;${m.ghost ? `background:repeating-linear-gradient(#8A93A3 0 10px,transparent 10px 18px)` : `background:${c}`};opacity:${c01(q * 1.6)}"></div>`; });
    ms.forEach(({ m, q, L: Lr }) => { const cy = AX - 26 - Lr.r * RS, c = m.team ? TC_(m.team) : '#3B4A63', imgs = m.imgs || [{ img: m.img, team: m.team }];
      const faces = m.ghost ? `<div style="width:${D}px;height:${D}px;border-radius:50%;border:5px dashed #9AA3B2;box-sizing:border-box;display:flex;align-items:center;justify-content:center;font-size:50px;font-weight:900;color:#9AA3B2;background:#F4F6F9">?</div>` : `<div class="row" style="gap:8px;justify-content:center;flex-wrap:nowrap">${imgs.map(x => circ({ img: x.img, team: x.team || m.team, focus: x.focus }, D)).join('')}</div>`;
      h += `<div style="position:absolute;left:${px(m.v)}px;top:${cy - D}px;translate:-50% 0;${pp(q)}">${faces}</div>
        <div style="position:absolute;left:${Lr.a}px;top:${cy - D - 62}px;width:${Lr.w}px;display:flex;justify-content:center;${pp(q)}">${PL(`${esc(m.name)} <span class="num">${esc(m.vt || m.v + '억')}</span>${m.sub ? ` <span style="font-weight:800;opacity:.85">${esc(m.sub)}</span>` : ''}`, m.ghost ? '#8A93A3' : c, 36, 'padding:6px 22px')}</div>`; });
    (s.bands || []).forEach(b => {
      const q = had(b, 'bands') ? 1 : P(s, b.at ?? 0, .7), e = eo(q), c = b.color || (b.team ? TC_(b.team) : ACC), x0 = px(b.from), w = (px(b.to) - x0) * e;
      const cx = Math.min(W - 230, Math.max(230, (x0 + px(b.to)) / 2));
      h += `<div style="position:absolute;left:${x0}px;top:${AX - 18}px;width:${w.toFixed(1)}px;height:48px;border-radius:24px;background:${c};opacity:${c01(q * 3) * .92};box-shadow:0 8px 20px ${c}55"></div>
        <div class="row" style="position:absolute;left:${cx}px;top:${AX + 84}px;translate:-50% 0;gap:16px;align-items:center;flex-wrap:nowrap;${pp(c01((q - .3) / .7))}">
          ${b.img ? circ({ img: b.img, team: b.team }, 110) : ''}<div class="col" style="align-items:flex-start;gap:0">
          <div style="font-size:34px;font-weight:900;color:${GRAY};white-space:nowrap">${esc(b.name || '')}${b.tag ? ` · ${esc(b.tag)}` : ''} 예상</div>
          <div class="num" style="font-size:66px;font-weight:900;letter-spacing:-2px;color:${c};white-space:nowrap;line-height:1.05">${esc(b.label || `${b.from}억~${b.to}억`)}</div></div></div>`;
    });
    const K = pr && pr.title === s.title;
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, K)}<div style="position:relative;width:${W}px;height:${H}px;margin-top:${ln ? 56 : 0}px">${h}</div>${anyTxt ? (s.text ? big(s, pr && pr.text === s.text) : `<div class="big" style="font-size:${s.size || 64}px;margin-top:18px;visibility:hidden">·</div>`) : ''}</div>`);
  };

  /* ── faces ── 인물 2~4명 카드(틀 없는 사진) + 이름 + 큰 글(note) + 말풍선(say). {"items":[{"img","name","team","role","note","at","say","sayAt"}],"title"} */
  SCENE.faces = (lt, s) => {
    const its = s.items || [], n = its.length, W = n >= 4 ? 340 : n === 3 ? 380 : its.some(x => x.say) ? 360 : 430, H = Math.round(W / .774);
    const one = (x, i) => { const p = P(s, x.at ?? i * .25, .5), q = x.say ? P(s, x.sayAt ?? 50, .5) : 0, src = photoSrc(x.img);
      return `<div class="col" style="align-items:center;gap:0;width:${W + 40}px;${rise(p, 30)}">
        <div style="position:relative;width:${W}px;height:${H}px;border-radius:30px;overflow:hidden;background:#E9EDF3;box-shadow:0 24px 54px rgba(18,22,31,.24)">${src ? faceImg(src, x, '50% 12%') : ''}</div>
        <div class="row" style="gap:10px;align-items:center;margin-top:16px;flex-wrap:nowrap">${x.team ? LG_(x.team, 50) : ''}<b style="font-size:54px;font-weight:900;letter-spacing:-2px;white-space:nowrap">${esc(x.name)}</b></div>
        ${x.role ? `<div style="font-size:32px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(x.role)}</div>` : ''}
        ${x.note ? `<div class="num" style="font-size:72px;font-weight:900;color:#E8A100;letter-spacing:-2px;line-height:1.1;${pp(P(s, x.noteAt ?? x.at ?? 0, .5))}">${esc(x.note)}</div>` : ''}
        ${x.say ? `<div style="position:relative;margin-top:22px;${pp(q)}"><div style="position:absolute;left:50%;top:-18px;translate:-50% 0;width:0;height:0;border-left:18px solid transparent;border-right:18px solid transparent;border-bottom:20px solid ${ACC}"></div>
          <div style="border:4px solid ${ACC};background:#fff;border-radius:26px;padding:14px 26px;font-size:38px;font-weight:900;line-height:1.25;text-align:center;white-space:nowrap">${br(x.say)}</div></div>` : ''}</div>`; };
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, false)}<div class="row" style="gap:${n >= 4 ? 26 : 70}px;justify-content:center;align-items:flex-start;flex-wrap:nowrap">${its.map(one).join('')}</div></div>`);
  };

  /* ── pricerows ── 정리 표 */
  SCENE.pricerows = (lt, s) => {
    const MX = s.max || 150, LW = 440, W = s.w || 1120, px = v => v / MX * W, rows = s.rows || [], pr = prevOf(s, 'pricerows'), RH = rows.length > 6 ? 86 : 100;
    const had = r => pr && (pr.rows || []).some(o => o.name === r.name && !o.hide);
    let h = `<div class="row" style="gap:0;flex-wrap:nowrap;height:56px;align-items:flex-end"><div style="width:${LW}px"></div><div style="position:relative;width:${W}px;height:56px">`;
    for (let v = 0; v <= MX; v += 25) h += `<div class="num" style="position:absolute;left:${px(v)}px;bottom:6px;translate:-50% 0;font-size:32px;font-weight:800;color:#8A93A3;white-space:nowrap">${v}${v ? '억' : ''}</div>`;
    h += `</div></div><div style="position:relative">`;
    rows.forEach((r, i) => {
      const q = r.hide ? 0 : had(r) ? 1 : P(s, r.at ?? i * .4, .6), e = eo(q), c = r.team ? TC_(r.team) : ACC;
      h += `<div class="row" style="gap:0;flex-wrap:nowrap;height:${RH}px;align-items:center;border-top:3px solid #EDF0F4;opacity:${r.hide ? 0 : 1}">
        <div class="row" style="width:${LW}px;gap:16px;align-items:center;flex-wrap:nowrap;${rise(q, 16)}">${PL(esc(r.rank || ''), '#12161F', 34, 'min-width:70px;text-align:center')}${circ(r, RH - 12)}<b style="font-size:52px;font-weight:900;letter-spacing:-2px;white-space:nowrap">${esc(r.name)}</b></div>
        <div style="position:relative;width:${W}px;height:${RH}px">
          ${[0, 25, 50, 75, 100, 125, 150].filter(v => v <= MX).map(v => `<div style="position:absolute;left:${px(v)}px;top:0;bottom:0;border-left:2px solid #EEF1F5"></div>`).join('')}
          <div style="position:absolute;left:${px(r.from)}px;top:${RH / 2 - 24}px;width:${((px(r.to) - px(r.from)) * e).toFixed(1)}px;height:48px;border-radius:24px;background:${c};opacity:.92"></div>
          <div class="num" style="position:absolute;left:${px(r.to) + 18}px;top:${RH / 2 - 34}px;font-size:54px;font-weight:900;letter-spacing:-2px;color:${c};white-space:nowrap;opacity:${c01((q - .5) * 3)}">${esc(r.label || `${r.from}~${r.to}억`)}</div></div></div>`;
    });
    const ln = s.line || (((CHAINS[s._cid] || []).map(j => SC[j]).find(x => x && x.line)) || {}).line;
    if (ln) { const q = s.line ? (pr && pr.line ? 1 : P(s, ln.at ?? 0, .5)) : 0;
      h += `<div style="position:absolute;left:${LW + px(ln.v) - 3}px;top:-10px;width:6px;height:${rows.length * RH + 20}px;background:repeating-linear-gradient(${RED} 0 14px,transparent 14px 24px);opacity:${c01(q * 1.5)}"></div>
        <div style="position:absolute;left:${LW + px(ln.v)}px;top:${rows.length * RH + 16}px;translate:-50% 0;${pp(q)}">${PL(esc(ln.label), RED, 32)}</div>`; }
    h += `</div>`;
    const K = pr && pr.title === s.title;
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, K)}<div class="col" style="align-items:flex-start;gap:0;width:${LW + W + 230}px">${h}</div>${(CHAINS[s._cid] || []).map(j => SC[j]).some(x => x && x.text) ? `<div style="margin-top:60px;visibility:${s.text ? 'visible' : 'hidden'}">${s.text ? big(s) : `<div class="big" style="margin-top:18px;font-size:${((CHAINS[s._cid] || []).map(j => SC[j]).find(x => x && x.text) || {}).size || 64}px">·</div>`}</div>` : ''}</div>`);
  };

  /* ── compgrade ── 보상 등급 */
  const BILL = (c, lab = '연봉') => `<div style="width:150px;height:90px;border-radius:12px;background:${c};position:relative;box-shadow:0 6px 14px ${c}55;flex:0 0 auto"><div style="position:absolute;inset:8px;border:3px solid rgba(255,255,255,.55);border-radius:8px"></div>
    <div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;font-size:34px;font-weight:900">${lab}</div></div>`;
  const HALF = c => `<div style="width:75px;height:90px;border-radius:12px 0 0 12px;background:${c};opacity:.85;flex:0 0 auto;position:relative"><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#fff;font-size:32px;font-weight:900">½</div></div>`;
  const MAN = c => `<div style="width:104px;height:104px;flex:0 0 auto">${ICON.person ? ICON.person(c) : ''}</div>`;
  SCENE.compgrade = (lt, s) => {
    const cols = s.cols || [], pr = prevOf(s, 'compgrade'), G = '#1F9D55';
    const had = c => pr && (pr.cols || []).some(o => o.g === c.g && !o.hide);
    const one = (cl, i) => {
      const q = cl.hide ? 0 : had(cl) ? 1 : P(s, cl.at ?? i, .6), hi = s.hi === cl.g, c = hi ? ACC : '#3B4A63';
      const opt = (o, k) => { const n = Math.floor(o.bills || 0), half = (o.bills || 0) % 1 > 0;
        return `<div class="col" style="gap:10px;align-items:center">
          <div class="row" style="gap:8px;flex-wrap:nowrap;align-items:center">${Array.from({ length: n }, () => BILL(G)).join('')}${half ? HALF(G) : ''}${o.person ? `<span style="font-size:44px;font-weight:900;color:${GRAY}">+</span>${MAN('#3B4A63')}` : ''}</div>
          <div style="font-size:42px;font-weight:900;color:${TXT};white-space:nowrap">연봉 ×${o.bills}${o.person ? ' + 선수 1명' : ''}</div></div>`; };
      const os = (cl.opt || []).map(opt);
      return `<div class="col" style="width:${s.cw || (cols.length === 1 ? 760 : 560)}px;align-items:center;gap:18px;padding:30px 10px;border-radius:30px;background:${hi ? '#F2F6FF' : '#F6F8FB'};border:5px solid ${hi ? c : 'transparent'};box-sizing:border-box;visibility:${cl.hide ? 'hidden' : 'visible'};${cl.hide ? '' : pp(q)}">
        <div style="font-size:104px;font-weight:900;color:${c};letter-spacing:-3px;line-height:1">${esc(cl.g)}<span style="font-size:56px">등급</span></div>
        ${os.join(`<div style="font-size:40px;font-weight:900;color:#9AA3B2">또는</div>`)}</div>`;
    };
    const K = pr && pr.title === s.title;
    const TX = (CHAINS[s._cid] || []).map(j => SC[j]).find(x => x && x.type === 'compgrade' && x.text);
    const tail = s.text ? big(s, pr && pr.text === s.text) : TX ? `<div class="big" style="margin-top:18px;font-size:${TX.size || 64}px;visibility:hidden">·</div>` : '';
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, K)}<div class="row" style="gap:34px;align-items:stretch;flex-wrap:nowrap">${cols.map(one).join('')}</div>${tail}</div>`);
  };

  /* ── comptrans ── 보상 흐름 */
  SCENE.comptrans = (lt, s) => {
    const W = 1500, pm = P(s, s.moveAt ?? 0, 1.0), pb = P(s, s.backAt ?? 50, 1.0), em = eo(pm), eb_ = eo(pb), G = '#1F9D55';
    const box = (lab, x, c) => `<div class="col" style="position:absolute;left:${x}px;top:190px;width:340px;height:260px;border-radius:36px;background:#F3F5F9;border:6px solid ${c};align-items:center;justify-content:center;gap:10px">
      <div style="width:150px;height:130px">${DICON && DICON.doc ? '' : ''}<svg viewBox="0 0 60 50" width="100%" height="100%"><path d="M6,46 V20 L30,6 L54,20 V46 Z" fill="${c}"/><rect x="24" y="28" width="12" height="18" fill="#fff"/></svg></div>
      <div style="font-size:48px;font-weight:900;color:${c}">${lab}</div></div>`;
    const x0 = 230, x1 = W - 230 - 0, man = (x, y, c, o) => `<div style="position:absolute;left:${x - 50}px;top:${y}px;width:100px;height:100px;opacity:${o}">${ICON.person(c)}</div>`;
    const fx = x0 + (x1 - x0) * em, arcY = 40 - Math.sin(Math.PI * em) * 40;
    const bx = x1 - (x1 - x0) * eb_, arcB = 470 + Math.sin(Math.PI * eb_) * 20;
    let h = box('원래 팀', 60, '#3B4A63') + box('새 팀', W - 400, ACC);
    h += `<div style="position:absolute;left:${fx - 60}px;top:${arcY}px;opacity:${c01(pm * 3)}" class="col">${PL('FA 선수', ACC, 30)}<div style="width:100px;height:100px;margin:6px auto 0">${ICON.person(ACC)}</div></div>`;
    h += `<div class="row" style="position:absolute;left:${bx - 150}px;top:${arcB}px;gap:10px;align-items:center;flex-wrap:nowrap;opacity:${c01(pb * 3)}">${BILL(G, '돈')}<span style="font-size:40px;font-weight:900;color:${GRAY}">+</span><div style="width:84px;height:84px">${ICON.person('#3B4A63')}</div></div>`;
    if (pb > 0) h += `<div style="position:absolute;left:${W / 2}px;top:572px;translate:-50% 0;${pp(c01((pb - .5) * 2))}">${PL('보상', G, 44, 'padding:8px 34px')}</div>`;
    const arrows = `<svg style="position:absolute;left:0;top:0" width="${W}" height="660"><path d="M${x0 + 200},90 Q${W / 2},${-10} ${x1 - 200},90" fill="none" stroke="${ACC}" stroke-width="6" stroke-dasharray="14 12" opacity="${c01(pm * 2) * .6}"/>
      <path d="M${x1 - 200},560 Q${W / 2},${640} ${x0 + 200},560" fill="none" stroke="${G}" stroke-width="6" stroke-dasharray="14 12" opacity="${c01(pb * 2) * .6}"/></svg>`;
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, false)}<div style="position:relative;width:${W}px;height:650px">${arrows}${h}</div></div>`);
  };

  /* ── tline ── 날짜 줄 */
  SCENE.tline = (lt, s) => {
    const its = s.items || [], n = its.length, W = Math.min(1640, 420 * n), gap = W / n;
    let h = `<div style="position:absolute;left:${gap / 2}px;top:132px;width:${W - gap}px;height:10px;border-radius:5px;background:#D5DAE2"></div>`;
    its.forEach((x, i) => { const q = P(s, x.at ?? i, .5), c = x.c === 'gold' ? '#E8A100' : x.c === 'bad' ? RED : x.c === 'good' ? GREEN : x.c || '#3B4A63', cx = gap * (i + .5);
      if (i) h += `<div style="position:absolute;left:${gap * (i - .5)}px;top:132px;width:${(gap * eo(q)).toFixed(1)}px;height:10px;border-radius:5px;background:${c}"></div>`;
      h += `<div style="position:absolute;left:${cx - 30}px;top:107px;width:60px;height:60px;border-radius:50%;background:${c};box-shadow:0 8px 18px ${c}55;${pp(q)}"></div>
        <div class="num" style="position:absolute;left:${cx}px;top:20px;translate:-50% 0;font-size:44px;font-weight:900;color:${GRAY};white-space:nowrap;opacity:${c01(q * 2)}">${esc(x.d)}</div>
        <div style="position:absolute;left:${cx}px;top:196px;translate:-50% 0;font-size:${x.big ? 64 : 52}px;font-weight:900;letter-spacing:-2px;color:${x.c ? c : TXT};white-space:nowrap;text-align:center;line-height:1.15;${rise(q, 20)}">${br(x.t)}</div>`; });
    B(`<div class="col" style="width:100%;align-items:center">${ttl(lt, s, false)}<div style="position:relative;width:${W}px;height:360px">${h}</div>${big(s)}</div>`);
  };

  Object.assign(MOTION, { faces: s => .4 + (s.items || []).length * .25, pricebar: s => .4 + (s.marks || []).length * .3 + (s.bands || []).length * .7, pricerows: s => .5 + (s.rows || []).length * .4, compgrade: () => 1.2, comptrans: () => 2.0, tline: s => .4 + (s.items || []).length * .4 });
})();
/* @@FA1016END */
