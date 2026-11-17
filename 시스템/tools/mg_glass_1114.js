/* @@MG1110 11/9~10 사용자 "모션그래픽이 잔뜩 멋지게 들어간 홍보영상 같은 분위기" · "어두운 베이스" · "앞으로 모든 영상은 이렇게 모션 그래픽을 넣어서" · "지금부터 해"(삼성 2027편부터)
   근거·사양: 프로젝트 claude/모션그래픽-제작법.md, 스킬 yagu-motion-graphics.
   - 전체 화면 레이어 #mg (1920×1080): 장면마다 새 디자인으로 그린다(#body 는 비움)
   - 움직이는 어두운 바탕(#mgbg) · 왼쪽 위 이음 판(야구자판기 + 챕터) · 장면 묶음마다 카메라 · 이어지지 않는 장면 경계에 금·파랑 사선 전환
   - 같은 묶음(_chain·_keep)에서는 사진·이름·제목·이미 보인 칸이 그대로(사라졌다 다시 ✗), 카메라도 묶음 전체에서 한 번만 흐른다 */
const MGON = EP.mg !== false;
/* 11/13 00:43 사용자 "줄바꿈 처리 잘해"('…않으려는 / 핑계' 한 단어만 다음 줄) → 여러 줄 글은 줄 길이를 고르게, 낱말 중간에서 안 끊음 */
try { const _st = document.createElement('style'); _st.textContent = '#mg .ab div,#mg .ab span{text-wrap:balance;word-break:keep-all}' + ['Black|800 900', 'Bold|600 700', 'Medium|400 500'].map(x => { const [w, r] = x.split('|'); return `@font-face{font-family:'YG';src:url('__FONT_DIR__/YG-KR-${w}.otf') format('opentype');font-weight:${r}}@font-face{font-family:'YG';src:url('__FONT_DIR__/YG-Inter-${w}.otf') format('opentype');font-weight:${r};unicode-range:U+0020-007E,U+00A0-00FF}`; }).join('') + "body,#stage,#stage *{font-family:'YG','KBO','Malgun Gothic',sans-serif!important}#mg{letter-spacing:-.012em}"; document.head.appendChild(_st); } catch (e) {}
const VERT = !!EP.vertical, FW = VERT ? 1080 : 1920, FH = VERT ? 1920 : 1080;   /* 11/10 쇼츠(세로 1080×1920)도 같은 모션 층 — v_ 장면 */
const MG = (() => {
  const GOLD = '#A9E9FF', BLU = '#6C8CFF', SOFT = '#B7A6FF', REDC = '#FF7A70', TX = '#F6F8FF', MU = '#BCC8E8', INK0 = '#070A14', GRN = '#7DE3B0';
  const HOLO = 'linear-gradient(100deg,#7EF0FF,#A78BFF 52%,#FF8AD8)', HOLOT = `background:${HOLO};-webkit-background-clip:text;background-clip:text;color:transparent`, GLASS = 'background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.05));backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px)', DOTS = '<div style="position:absolute;inset:0;pointer-events:none;background-image:radial-gradient(circle,rgba(0,0,0,.30) 0 30%,transparent 33%);background-size:10px 10px;mix-blend-mode:multiply"></div>';
  const ss = x => { x = c01(x); return x * x * (3 - 2 * x); };
  const SM = 1.6, sg = (lt, a, d) => c01((lt - a) / (d * SPD * SM));
  const AT = (s, at, d, fb) => (at != null && at < 0) ? 1 : (at != null && at >= 50) ? 0 : pk(s, at, d * SM, fb != null ? fb : 0);
  const e4 = x => 1 - Math.pow(1 - c01(x), 4), eio = x => { x = c01(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }, ex = x => { x = c01(x); return x >= 1 ? 1 : 1 - Math.pow(2, -10 * x); };
  const L = (a, b, p) => a + (b - a) * p;
  const op = q => `opacity:${ss(q * 1.25).toFixed(3)}`;
  const up = (q, d = 30) => `opacity:${ss(q * 1.25).toFixed(3)};transform:translateY(${((1 - e4(q)) * d).toFixed(1)}px)`;
  /* 11/13 22:10 사용자 "디자인 효과들을 이용해서… 남발 말고 적절하게" → 등장할 때만 움직이고 끝나면 멈추는 효과 묶음(같은 그림 깜빡임 ✗) */
  const SQW = q => q >= 1 ? 0 : -Math.exp(-4.5 * c01(q)) * Math.cos(10 * c01(q));
  const SQ = q => { const w = SQW(q); return `scale(${(1 + .26 * w).toFixed(3)},${(1 - .26 * w).toFixed(3)})`; };   /* 스쿼시 앤 스트레치 */
  const SHEEN = q => q <= 0 || q >= 1 ? '' : `<div style="position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:linear-gradient(105deg,transparent 36%,rgba(255,255,255,.85) 47%,rgba(150,225,255,.6) 52%,rgba(255,170,240,.5) 57%,transparent 66%);background-size:320% 100%;background-position:${(160 - 320 * ss(q)).toFixed(1)}% 0;mix-blend-mode:screen"></div>`;   /* 홀로그래픽: 빛이 한 번 훑고 끝 */
  const GLI = q => { if (q <= 0 || q >= 1) return ''; const k = 1 - q, st = Math.floor(q * 9) % 3, d = (k * 14 * (st === 1 ? .35 : 1)).toFixed(1), j = (k * (st === 0 ? 10 : st === 1 ? -6 : 3)).toFixed(1); return `text-shadow:${d}px 0 rgba(255,60,120,.85),-${d}px 0 rgba(60,220,255,.85);transform:translateX(${j}px) skewX(${(k * (st === 0 ? -6 : 4)).toFixed(1)}deg);`; };   /* 글리치: 등장 순간만 */
  const HALF = (x, y, w, hh, q, c = '#9DB7DA') => true ? '' : `<div class="ab" style="left:${x}px;top:${y}px;width:${w}px;height:${hh}px;opacity:${(.32 * ss(q)).toFixed(3)};background-image:radial-gradient(circle,${c} 0 28%,transparent 31%);background-size:18px 18px;-webkit-mask-image:radial-gradient(ellipse at 50% 45%,#000 5%,transparent 68%);mask-image:radial-gradient(ellipse at 50% 45%,#000 5%,transparent 68%)"></div>`;   /* 하프톤 망점 */
  const LIQ = (w, hh, lvl, q) => { const yy = hh * (1 - lvl * e4(c01(q * 1.15))), A = (1 - c01(q)) * 13, ph = q * 13; let d = `M0 ${hh} L0 ${yy.toFixed(1)}`; for (let i = 1; i <= 12; i++) { const xx = w * i / 12; d += ` L${xx.toFixed(1)} ${(yy + A * Math.sin(ph + i * 1.05)).toFixed(1)}`; } return `<svg width="${w}" height="${hh}" style="position:absolute;left:0;top:0;border-radius:34px"><defs><linearGradient id="lq${Math.round(lvl * 1000)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="rgba(160,200,255,${(.14 * (1 - c01(q * 1.2 - .2))).toFixed(3)})"/><stop offset="1" stop-color="rgba(160,200,255,.16)"/></linearGradient></defs><path d="${d} L${w} ${hh} Z" fill="url(#lq${Math.round(lvl * 1000)})"/><path d="${d}" fill="none" stroke="rgba(200,226,255,${(.55 * (1 - c01(q * 1.3 - .3))).toFixed(3)})" stroke-width="2"/></svg>`; };   /* 리퀴드: 차오르며 출렁이다 잔잔해짐 */
  const code = t => { const tt = T(t || ''); return tt ? tt.code : ''; };
  const LG = (t, w) => { const c = code(t); return c && LOGO[c] ? `<img data-nofx="1" src="${LOGO[c]}" style="width:${w}px;height:${w}px;object-fit:contain;filter:drop-shadow(0 4px 10px rgba(0,0,0,.5));flex:0 0 auto">` : ''; };
  const WL = t => [...String(t || '')].reduce((n, ch) => n + (ch.charCodeAt(0) > 0x3000 ? 1 : ch === ' ' ? .32 : /[0-9]/.test(ch) ? .62 : .58), 0);
  const FIT = (t, base, w, min = 26) => Math.max(min, Math.min(base, Math.floor(w * .93 / Math.max(.1, WL(t)))));
  const J = x => JSON.stringify(x == null ? null : x);
  /* 글자마다 아래에서 마스크로 올라옴(넘침 ✗) — q 0→1 이 전체 진행, 마지막 글자가 q=1 에 끝난다 */
  const KIN = (txt, q, extra = '') => { const a = [...String(txt == null ? '' : txt)], n = a.length, g = n > 1 ? Math.min(.09, .6 / (n - 1)) : 0, sp = 1 + g * (n - 1);
    if (q >= 1) return `<span style="white-space:pre;${extra}">${esc(txt)}</span>`;
    return `<span style="display:inline-block;white-space:pre;${extra}">` + a.map((ch, i) => { const pp = e4(c01(q * sp - i * g));
      return `<span style="display:inline-block;overflow:hidden;vertical-align:top;line-height:1.18"><span style="display:inline-block;white-space:pre;transform:translateY(${((1 - pp) * 105).toFixed(1)}%);opacity:${c01(pp * 2).toFixed(3)}">${esc(ch)}</span></span>`; }).join('') + '</span>'; };
  /* 숫자만 있는 값(102, 7)은 0→값으로 올라가고, 글이 섞인 값(5할·94억 1천만)은 아래에서 밀려 올라온다(없던 값을 보여 주지 않게) */
  const NUMV = (v, q) => { const sv = String(v == null ? '' : v); if (/^\d{1,4}$/.test(sv) && q < 1) return String(Math.round(+sv * ex(q))); return sv; };
  const MASK = (inner, q, extra = '') => q >= 1 ? `<span style="${extra}">${inner}</span>` : `<span style="display:inline-block;overflow:hidden;vertical-align:top;${extra}"><span style="display:inline-block;transform:translateY(${((1 - e4(q)) * 105).toFixed(1)}%)">${inner}</span></span>`;
  /* 사진: 얼굴(MGF) 기준으로 칸 안 가로 위치(want = 칸 폭의 몇 % 에 얼굴), 세로는 머리 위 여백 */
  const MGF = window.MGF || {};
  const pos = (img, w, h, want = .5, fy0) => { const f = MGF[img] || null, sz = PSIZE[img] || (f ? [f[2], f[3]] : null);
    let px = 50, py = fy0 != null ? fy0 : 20;
    if (f && sz) { const sc = Math.max(w / sz[0], h / sz[1]), W2 = sz[0] * sc, H2 = sz[1] * sc;
      if (W2 - w > 1) px = 100 * c01(((f[4] ?? f[0]) * W2 - want * w) / (W2 - w));
      if (H2 - h > 1) py = 100 * c01((Math.max(0, f[1] - .06) * H2 - .08 * h) / (H2 - h)); }
    return `${px.toFixed(1)}% ${py.toFixed(1)}%`; };
  const PIC = (img, w, h, want, extra = '', focus) => { const src = photoSrc(img); if (!src) return '';
    const p = MGF[img] ? pos(img, w, h, want) : (focus || '50% 20%');
    return `<img data-nofx="1" src="${src}" style="position:absolute;left:0;top:0;width:${w}px;height:${h}px;object-fit:cover;object-position:${p};${extra}">`; };

  /* ── 레이어 ── */
  let ST, BG, A, Bx, EDGE, BUG;
  function layers() {
    if (A) return; ST = VERT ? document.body : document.getElementById('stage');   /* 세로: 원래 장면(#stage)은 장면마다 확대·이동되므로 모션 층은 body 에 1080×1920 좌표로 */
    const css = document.createElement('style');
    css.textContent = `html,body,#stage{background:${INK0}!important}#hdr{display:none!important}#body{opacity:0!important;pointer-events:none}#sbg{display:none!important}
#prog{background:rgba(255,255,255,.07)!important;height:5px;z-index:46}#progBar{background:${GOLD}!important}
#sub{z-index:40}#sub span{background:rgba(6,9,14,.86)!important;color:#F2F4F8!important;box-shadow:0 0 0 1px rgba(255,255,255,.10),0 10px 30px rgba(0,0,0,.35)!important;border-radius:36px}
#mg,#mgbg{position:absolute;left:0;top:0;width:${FW}px;height:${FH}px;overflow:hidden;pointer-events:none}#mgbg::after{content:'';position:absolute;inset:0;pointer-events:none;opacity:.5;mix-blend-mode:overlay;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .5 0 0 0 0 .5 0 0 0 .55 0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>")}#mg .ab{position:absolute}${VERT ? '#vtitle{display:none!important}#prog{display:none!important}#stage{background:transparent!important}#relArrow{z-index:50}' : ''}`;
    document.head.appendChild(css);
    BG = document.createElement('div'); BG.id = 'mgbg'; BG.style.zIndex = '0';
    const M = document.createElement('div'); M.id = 'mg'; M.style.zIndex = '5';
    M.innerHTML = `<div id="mgB" style="position:absolute;inset:0"></div><div id="mgA" style="position:absolute;inset:0"></div><div id="mgE" style="position:absolute;inset:0"></div>`;
    BUG = document.createElement('div'); BUG.id = 'mgbug'; BUG.style.cssText = `position:absolute;left:${VERT ? 48 : 56}px;top:${VERT ? 60 : 40}px;z-index:45;display:flex;align-items:stretch;pointer-events:none`;
    ST.insertBefore(BG, ST.firstChild); ST.appendChild(M); ST.appendChild(BUG);
    A = document.getElementById('mgA'); Bx = document.getElementById('mgB'); EDGE = document.getElementById('mgE');
  }
  /* ── 움직이는 바탕: 떠도는 빛 두 개 + 사선 줄 + 가운데 격자 + 빛줄기 ── */
  /* 11/10 01:12 사용자 "가만히 있는 장면에서도 화면이 이리저리 움직여서 정신사나워" → 바탕은 멈춰 있다(빛·줄·격자 고정, 한 번만 그림) */
  function paintBG(t, k) {
    if (!VERT) { const kc = Math.max(0, Math.min(k || 0, SC.length - 1)), sc0 = SC[kc] || {}, c1 = sc0.tc || '#2458E6', c2 = sc0.tc2 || '#7B3BFF';
      const blobs = (a, b) => `<div style="position:absolute;inset:0;background:${INK0}"></div><div style="position:absolute;left:-220px;top:-290px;width:1150px;height:920px;border-radius:50%;background:${a};filter:blur(150px);opacity:.74"></div><div style="position:absolute;right:-280px;bottom:-340px;width:940px;height:820px;border-radius:50%;background:${b};filter:blur(150px);opacity:.46"></div><div style="position:absolute;left:640px;top:560px;width:520px;height:400px;border-radius:50%;background:#19C2FF;filter:blur(140px);opacity:.16"></div>`;
      /* 11/14 검수: 팀 색이 바뀌는 경계에서 바탕만 먼저 툭 바뀌어 앞 장면이 새 색 위에 잠깐 얹혔다 → 바탕도 장면 전환과 같이(선 전환이면 선을 따라, 아니면 0.3초에 스며듦) */
      const P = kc > 0 ? SC[kc - 1] : null, p1 = P ? (P.tc || '#2458E6') : c1, p2 = P ? (P.tc2 || '#7B3BFF') : c2, dt = t - (kc === 0 ? 0 : BD[kc - 1]), kind = kc > 0 ? trKind(kc) : '', TD = kind === 'line' ? .45 : .4;
      if ((p1 !== c1 || p2 !== c2) && dt >= 0 && dt < TD) { const q = kind === 'line' ? eio(dt / TD) : ss(c01(dt / .3)); BG.dataset.c = '';
        BG.innerHTML = `<div style="position:absolute;inset:0">${blobs(p1, p2)}</div><div style="position:absolute;inset:0;${kind === 'line' ? `clip-path:inset(0 ${(FW * (1 - q)).toFixed(1)}px 0 0)` : `opacity:${q.toFixed(3)}`}">${blobs(c1, c2)}</div>`; return; }
      if (BG.dataset.c === c1 + c2) return; BG.dataset.c = c1 + c2;
      BG.innerHTML = blobs(c1, c2); return; }
    if (BG.dataset.done) return; BG.dataset.done = '1';
    /* 11/13 23:13 사용자 "영상 배경도 좀 바꿔보고" → 롱폼 바탕 = 야간 경기장(옛 전광판의 짙은 초록 + 조명탑 불빛 + 외야 곡선). 색은 바탕 1 + 강조(금) 1, 멈춰 있음 */
    BG.innerHTML = `<div style="position:absolute;inset:0;background:radial-gradient(${VERT ? '900px 1100px at 30% 32%' : '1000px 760px at 26% 30%'},rgba(60,110,190,.22),transparent 70%),radial-gradient(${VERT ? '800px 900px at 76% 78%' : '900px 640px at 80% 74%'},rgba(200,226,255,.07),transparent 70%),${INK0}"></div>
      <div style="position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.028) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.028) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:radial-gradient(ellipse at 50% 50%,#000 30%,transparent 80%)"></div>`;
  }
  /* ── 이음 판: 야구자판기 금판 + 챕터 칸(챕터가 바뀔 때 글만 0.32초에 위로 넘어감) ── */
  const CHM = EP.mgChapters || CH;   /* 쇼츠: 이음 판 칸 이름만(설명란 챕터 ✗) */
  function chapAt(k) { const ln = (SC[Math.min(k, SC.length - 1)] || {}).startLine ?? k; let i = -1; for (let j = 0; j < CHM.length; j++) if (ln >= (CHM[j].from || 0) && (CHM[j].to == null || ln <= CHM[j].to)) i = j; return i; }
  function paintBug(k, t) {
    const i = chapAt(k), ci = i >= 0 ? CHM[i] : null; let txt = ci ? (ci.short || ci.title || '') : '';
    let prev = '', ft = 1;
    if (k > 0) { const pi = chapAt(k - 1); if (pi !== i) { const st0 = BD[k - 1] || 0; ft = c01((t - st0) / .32); prev = pi >= 0 ? (CHM[pi].short || CHM[pi].title || '') : ''; } }
    const W = Math.max(FIT(txt, 30, 1, 30) && 0, Math.ceil(Math.max(WL(txt), WL(prev)) * 28) + 40);
    const cur = `<span style="position:absolute;left:0;top:${((1 - e4(ft)) * 40).toFixed(1)}px;opacity:${c01(ft * 2).toFixed(3)}">${esc(txt)}</span>` + (prev && ft < 1 ? `<span style="position:absolute;left:0;top:${(-e4(ft) * 40).toFixed(1)}px;opacity:${(1 - c01(ft * 2)).toFixed(3)}">${esc(prev)}</span>` : '');
    BUG.innerHTML = `<div style="background:${HOLO};color:${INK0};font-size:27px;font-weight:900;padding:8px 20px;border-radius:999px;letter-spacing:-.5px">야구자판기</div>`
      + (txt || (prev && ft < 1) ? `<div style="position:relative;overflow:hidden;width:${W}px;height:48px;${GLASS};margin-left:6px;transform:skewX(-12deg);box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)"><div style="position:absolute;left:20px;top:8px;right:0;height:34px;transform:skewX(12deg);font-size:27px;font-weight:700;color:${TX};white-space:nowrap">${cur}</div></div>` : '');
  }

  /* ── 공통 조각 ── */
  const slashLines = (x, q, h = 1200) => `<div class="ab" style="left:${L(x + 700, x, e4(q)).toFixed(1)}px;top:-60px;width:24px;height:${h}px;background:${BLU};transform:skewX(-12deg);opacity:${c01(q * 1.5).toFixed(3)}"></div><div class="ab" style="left:${L(x + 800, x + 46, e4(c01(q * 1.1 - .05))).toFixed(1)}px;top:-60px;width:7px;height:${h}px;background:${GOLD};transform:skewX(-12deg)"></div>`;
  const eyebrow = (txt, q, x, y, extra = '') => txt ? `<div class="ab" style="left:${x}px;top:${y}px;${op(q)};${extra}"><div style="width:${(90 * e4(q)).toFixed(1)}px;height:5px;background:${GOLD};margin-bottom:14px"></div><div style="font-size:32px;font-weight:700;color:${GOLD};letter-spacing:1px;white-space:nowrap">${esc(txt)}</div></div>` : '';
  /* 오른쪽 사선 사진 패널(선수 장면 공통) — keep 이면 그대로, 사진이 바뀌면 0.5초 겹쳐 바뀜 */
  const PX = 800, PWD = 1120;
  /* 사진이 작아 1.25배 넘게 키워야 하면(11/2 규칙) 화면 높이 패널 대신 액자 카드(사진 1.25배 이하) */
  const need = (img, w, h) => { const f = MGF[img], sz = PSIZE[img] || (f ? [f[2], f[3]] : null); return sz ? Math.max(w / sz[0], h / sz[1]) : 1; };
  const szOf = img => { const f = MGF[img]; return PSIZE[img] || (f ? [f[2], f[3]] : [1200, 900]); };
  /* 11/10 01:14 사용자 "사진이 쓸데없이 너무 크고 내용에 집중되지 않아 — 내용을 더 크게" → 사진은 왼쪽 액자(560×712 — 11/13 자막 위 끝(878) 위에서 끝나게, 1.25배 이하), 오른쪽 1080px 가 내용 */
  const CX0 = 730, CW0 = 1080;
  function panel(s, lt, q, prevImg) {
    const src = photoSrc(s.img), [W, H] = src ? szOf(s.img) : [560, 712];
    let w = Math.round(Math.min(560, W * 1.25)), hh = Math.round(Math.min(712, H * 1.25));
    /* 11/10 10:20 사용자 "사진만 바뀌는 거라면 페이드로 사진만 바뀌게" → 앞 사진 위로 새 사진이 0.5초 페이드, 액자 크기는 그사이 부드럽게 맞춰짐 */
    const chg = !!(prevImg && photoSrc(prevImg) && photoSrc(prevImg) !== src && src), xq = chg ? ss(c01(lt / .5)) : 1;
    if (chg && xq < 1) { const [W0, H0] = szOf(prevImg); w = Math.round(L(Math.min(560, W0 * 1.25), w, xq)); hh = Math.round(L(Math.min(712, H0 * 1.25), hh, xq)); }
    const x = 100 + Math.round((560 - w) / 2), y = 150 + Math.round((712 - hh) / 2);
    let inner = src ? PIC(s.img, w, hh, .5, 'filter:contrast(1.05) saturate(1.05)', s.focus) : `<div style="position:absolute;inset:0;background:linear-gradient(135deg,#1A2433,#0E1520)"></div><div style="position:absolute;left:50%;top:46%;transform:translate(-50%,-50%)">${LG(s.team, 260)}</div>`;
    if (chg && xq < 1) inner = PIC(prevImg, w, hh, .5, 'filter:contrast(1.05) saturate(1.05)') + `<div style="position:absolute;inset:0;opacity:${xq.toFixed(3)}">${inner}</div>`;
    return `<div class="ab" style="left:${x}px;top:${(y + (1 - e4(q)) * 30).toFixed(1)}px;width:${w}px;height:${hh}px;border-radius:44px;overflow:hidden;opacity:${c01(q * 2).toFixed(3)};box-shadow:0 36px 80px rgba(0,0,0,.5)">${inner}${DOTS}<div style="position:absolute;inset:0;border-radius:44px;box-shadow:inset 0 0 0 2px rgba(255,255,255,.28)"></div></div>`;
  };
  const ghostWord = (txt0, lt, y = 120) => { const txt = ''; return txt ? `<div class="ab" style="left:${L(60, -60, c01(lt / 12)).toFixed(1)}px;top:${y}px;font-size:250px;font-weight:900;color:rgba(255,255,255,.035);white-space:nowrap;letter-spacing:-6px">${esc(txt)}</div>` : ''; };
  /* 이름 + 위 작은 금색 줄 */
  function nameBlock(s, lt, q, keep, x = CX0, y = 160, wmax = CW0, noLine = false, ebq = null) {
    const nf = FIT(s.name || '', 150, wmax, 84), et = s.sub || s.kicker || '';
    /* 11/10 10:19 사용자 "사진과 이름이 같은데 전부 사라지고 다시 떠" → 이름·금색 막대는 그대로, 위 작은 글만 바뀜(ebq) */
    const eb = ebq != null && et ? `<div class="ab" style="left:${x}px;top:${y}px"><div style="width:90px;height:5px;background:${GOLD};margin-bottom:14px"></div><div style="font-size:32px;font-weight:700;color:${GOLD};letter-spacing:1px;white-space:nowrap;${up(ebq, 14)}">${esc(et)}</div></div>` : eyebrow(et, keep ? 1 : c01(q * 1.4), x, y);
    return eb
      + `<div class="ab" style="left:${x - 4}px;top:${y + 62}px;font-size:${nf}px;font-weight:900;letter-spacing:-4px;line-height:1.15;color:${TX};white-space:nowrap">${keep ? esc(s.name || '') : KIN(s.name || '', c01(q * 1.1 - .1))}</div>`
      + (noLine ? '' : `<div class="ab" style="left:${x}px;top:${y + 62 + nf * 1.2 + 10}px;width:${((wmax - 40) * e4(keep ? 1 : c01(q * 1.2 - .2))).toFixed(1)}px;height:2px;background:rgba(232,236,242,.22)"></div>`);
  }

  /* ── 장면 그림(전체 화면 좌표) ── */
  const R = {};
  /* C1 rf_band: 사진을 화면 가득(어둡게) + 왼쪽 정렬 큰 값 */
  R.rf_band = (lt, s) => {
    const P = s._prev && s._prev.type === 'rf_band' ? s._prev : null, pv_ = P ? (P.vals || []) : [];
    const sameWho = !!(P && P.who === s.who && (P.tag || '') === (s.tag || '') && (P.team || '') === (s.team || ''));
    const wq = sameWho ? 1 : AT(s, s.whoAt, .9, sg(lt, 0, .9)), vs = s.vals || [];
    const keepV = i => !!(sameWho && pv_.length === vs.length && pv_[i] && !(pv_[i].at >= 50) && pv_[i].v === vs[i].v && (pv_[i].k || '') === (vs[i].k || '') && !!pv_[i].hi === !!vs[i].hi);
    const img = s.bg && s.bg.img, X = 120;
    let h = '';
    const bgq = (P && P.bg && P.bg.img === img) ? 1 : ss(lt / .45);   /* 사진 바탕이 툭 나타나지 않게 0.45초에 깔림(전체 미리보기 jumpscan 에서 찾음) */
    if (img) h += `<div class="ab" style="inset:0;overflow:hidden;opacity:${bgq.toFixed(3)}">${PIC(img, 1920, 1080, .64, 'filter:blur(8px) brightness(.42) saturate(1.05);transform:scale(1.06)')}</div><div class="ab" style="inset:0;opacity:${bgq.toFixed(3)};background:linear-gradient(90deg,rgba(11,16,24,.94) 0%,rgba(11,16,24,.72) 45%,rgba(11,16,24,.25) 78%),linear-gradient(0deg,rgba(11,16,24,.85),transparent 42%)"></div>`;
    else h += ghostWord(s.who, lt, 140);
    const Y0 = s.top ? Math.max(170, s.top + 10) : 230, hasFig = !!s.fig;
    h += `<div class="ab" style="left:${X}px;top:${Y0}px;display:flex;align-items:center;gap:22px">${s.team ? `<div style="${op(wq)}">${LG(s.team, 78)}</div>` : ''}<div style="font-size:${FIT(s.who, 86, 1400)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${sameWho ? esc(s.who || '') : KIN(s.who || '', wq)}</div>${s.tag ? `<div style="padding:6px 18px;background:${GOLD};color:${INK0};font-size:36px;font-weight:900;transform:skewX(-12deg);white-space:nowrap;${s.tagAt != null && !sameWho ? op(AT(s, s.tagAt, .45, 1)) : op(wq)}"><div style="transform:skewX(12deg)">${esc(s.tag)}</div></div>` : ''}</div>`;
    h += `<div class="ab" style="left:${X}px;top:${Y0 + 112}px;width:${(380 * e4(wq)).toFixed(1)}px;height:3px;background:linear-gradient(90deg,${GOLD},transparent)"></div>`;
    if (vs.length) { const tw = vs.reduce((a, x) => a + WL(x.v) * (x.size || 150), 0) + (vs.length - 1) * 70, k = Math.min(1, 1640 / tw);
      h += `<div class="ab" style="left:${X}px;top:${Y0 + 170}px;display:flex;align-items:flex-start;gap:${Math.round(56 * k)}px">` + vs.map((x, i) => { const q = keepV(i) ? 1 : AT(s, x.at, .7, sg(lt, .3 + i * .25, .7)), sz = Math.round((x.size || 150) * k);
        return `${i ? `<div style="width:3px;height:${Math.round(sz * .8)}px;margin-top:${Math.round(sz * .14)}px;background:rgba(255,255,255,.3);${op(q)}"></div>` : ''}<div style="text-align:left"><div class="num" style="font-size:${sz}px;font-weight:900;line-height:1.12;letter-spacing:-3px;white-space:nowrap;color:${x.hi ? GOLD : TX};text-shadow:0 8px 30px rgba(0,0,0,.5)">${q >= 1 ? esc(x.v) : KIN(x.v, q)}</div><div style="font-size:36px;line-height:44px;height:44px;color:${MU};font-weight:700;margin-top:12px;white-space:nowrap;${op(c01(q * 1.3 - .3))}">${esc(x.k || '')}</div></div>`; }).join('') + `</div>`; }
    if (hasFig) { const F = s.fig, fq = (P && J(P.fig) === J(F)) ? 1 : AT(s, F.at, .55, sg(lt, .5, .55)), FY = (s.figY || 400) + 146;
      if (F.type === 'steps') { const its = F.items || [], n = its.length, ws = its.map(it => (it.w || 300) + 40), gp = 110, W0 = ws.reduce((a, b) => a + b, 0) + (n - 1) * gp; let x0 = X;
        its.forEach((it, k) => { const w = ws[k], x = x0 + ws.slice(0, k).reduce((a, b) => a + b, 0) + k * gp, iq = it.at != null ? AT(s, it.at, .5, 1) : 1;
          h += `<div class="ab" style="left:${x}px;top:${(FY + (1 - e4(iq)) * 30).toFixed(1)}px;width:${w}px;height:140px;${op(iq)};display:flex;align-items:center;justify-content:center;${it.hi ? `background:${GOLD};color:${INK0}` : `background:rgba(255,255,255,.08);color:${TX};box-shadow:inset 0 0 0 2px rgba(255,255,255,.14)`};clip-path:polygon(6% 0,100% 0,94% 100%,0 100%)"><div style="font-size:${FIT(it.lab, 44, w - 60)}px;font-weight:900;white-space:nowrap">${esc(it.lab)}</div></div>`;
          if (k < n - 1) { const jq = its[k + 1].at != null ? AT(s, its[k + 1].at, .45, 1) : 1, jn = its[k + 1].join || '→';
            h += `<div class="ab" style="left:${x + w}px;width:${gp}px;top:${FY + 30}px;text-align:center;font-size:64px;font-weight:900;color:${GOLD};${op(jq)}">${esc(jn === '−' ? '−' : jn)}</div>`; } }); }
      /* squad: 한 팀 선수 n명(사람 그림) — 처음부터 흐린 윤곽으로 있다가 fillAt 에 왼쪽부터 채워지고, 아래 합계 막대가 자라 capAt 에 금색 상한선 */
      if (F.type === 'squad') { const n = F.n || 40, per = Math.ceil(n / 2), IW = 56, GX = Math.floor((1440 - per * IW) / (per - 1)), fl = AT(s, F.fillAt ?? 1, 1.2, 1), cq = AT(s, F.capAt ?? 2, .6, 1), sq = c01(fl * 1.15 - .15);
        const man = (c, o) => `<svg width="${IW}" height="84" viewBox="0 0 56 84" style="display:block;opacity:${o}"><circle cx="28" cy="16" r="13" fill="${c}"/><path d="M6 84 V52 Q6 34 28 34 Q50 34 50 52 V84 Z" fill="${c}"/></svg>`;
        for (let i = 0; i < n; i++) { const r = Math.floor(i / per), c = i % per, on = c01(fl * (n + 8) / 8 - i / 8);
          h += `<div class="ab" style="left:${X + c * (IW + GX)}px;top:${FY + r * 108}px;${op(fq)}">${man('rgba(255,255,255,.14)', 1)}<div style="position:absolute;inset:0;transform:translateY(${((1 - e4(on)) * 10).toFixed(1)}px)">${man('#DCE3EE', on.toFixed(3))}</div></div>`; }
        h += `<div class="ab" style="left:${X + per * (IW + GX) - GX + 26}px;top:${FY + 58}px;font-size:76px;font-weight:900;color:${GOLD};white-space:nowrap;${op(fl)}">${Math.max(1, Math.round(n * c01(fl * 1.1)))}명</div>`;
        const BY = FY + 260, BW = 1680, cx = BW * .9;
        h += `<div class="ab" style="left:${X}px;top:${BY}px;width:${BW}px;height:96px;background:rgba(255,255,255,.06);border-radius:32px;${op(fq)}"></div>`
          + `<div class="ab" style="left:${X}px;top:${BY}px;width:${(cx * .86 * e4(sq)).toFixed(1)}px;height:96px;border-radius:32px;background:linear-gradient(90deg,#2F5D9C,${SOFT})"></div>`
          + `<div class="ab" style="left:${X + 28}px;top:${BY + 22}px;font-size:44px;font-weight:900;color:${TX};white-space:nowrap;${op(c01(sq * 1.5 - .3))}">${esc(F.sumLab || '')}</div>`
          + `<div class="ab" style="left:${X + cx - 3}px;top:${(BY - 30 + (1 - e4(cq)) * -20).toFixed(1)}px;width:6px;height:${(156 * e4(cq)).toFixed(1)}px;background:${GOLD};box-shadow:0 0 18px rgba(200,226,255,.6)"></div>`
          + `<div class="ab" style="left:${X + cx + 22}px;top:${BY + 14}px;font-size:56px;font-weight:900;color:${GOLD};white-space:nowrap;${up(cq, 16)}">${esc(F.capLab || '상한')}</div>`; } }
    return h;
  };
  /* C3 rf_duo: 양쪽 사선 패널이 부딪히고 가운데 빛기둥 */
  R.rf_duo = (lt, s) => {
    /* 11/10 01:14 사용자 "사진이 쓸데없이 너무 크고" → 두 사람은 같은 크기 액자 두 장(1.25배 이하) + 이름·기록은 크게 */
    const cs = s.cards || [], P = s._prev && s._prev.type === 'rf_duo' ? s._prev : null;
    /* 11/10 11:04 사용자 "김도환은 그대로 있고 바뀌는 사진만 바뀌게" → 두 장 중 한 사람이라도 그대로면 이어지는 장면(dc):
       액자는 제자리, 바뀐 쪽만 사진 0.5초 페이드 · 이름은 앞 이름이 위로 빠지고 새 이름 · 그 사람 글은 앞 글이 빠진 뒤 */
    const dc = !!(P && (P.cards || []).some((pc, i) => cs[i] && pc.img === cs[i].img && pc.name === cs[i].name && !(pc.at >= 50)));
    const sameT = !!(P && P.title === s.title), tq = sameT ? 1 : sg(lt, P && (s._chain || dc) ? .12 : 0, 1.0);
    const dims = x => { const c2 = x.cards || [], hs = c2.some(c => (c.stats || []).length), w2 = c2.slice(0, 2).map(c => szOf(c.img)); const H2 = Math.round(Math.min(hs ? 500 : 600, ...w2.map(z => z[1] * 1.25))), AR = Math.min(...w2.map(z => z[0] / Math.max(1, z[1])));
      /* 11/13 00:50 사용자 "꼭 얼굴만 화면 가득차게 확대해서 보여줘야돼? 몸까지 좀 보여지게" → 세로 사진을 가로 액자에 꽉 채우면 얼굴만 남는다: 액자 비율을 사진 비율에 맞춤(조금만 잘림) */
      return [Math.round(Math.min(640, ...w2.map(z => z[0] * 1.25), H2 * AR * 1.08)), H2]; };
    let [CWd, CHd] = dims(s); const Y0 = 245;
    if (dc) { const [pw, ph] = dims(P), mq = ss(c01(lt / .4)); CWd = Math.round(L(pw, CWd, mq)); CHd = Math.round(L(ph, CHd, mq)); }
    const ZP = (c, w, hh) => PIC(c.img, w, hh, .5, 'filter:contrast(1.06)' + (c.zoom > 1 ? `;transform:scale(${c.zoom});transform-origin:${c.zo || '50% 40%'}` : ''), c.focus);
    let h = '';
    cs.slice(0, 2).forEach((c, i) => { const pc = P && (P.cards || [])[i], keepC = !!(pc && pc.img === c.img && pc.name === c.name && !(pc.at >= 50)), swapC = dc && !keepC && pc && !(pc.at >= 50);
      const q = keepC || swapC ? 1 : AT(s, c.at, .7, sg(lt, i * .1, .7)), L0 = i === 0;
      const x = L0 ? 960 - 50 - CWd : 960 + 50, nq = keepC ? 1 : swapC ? sg(lt, .15, .7) : c01(q * 1.3 - .3), st = c.stats || [];
      let inner = ZP(c, CWd, CHd) + DOTS, nm = `<div style="position:absolute;left:30px;right:30px;bottom:18px;font-size:${FIT(c.name, 86, CWd - 60)}px;font-weight:900;letter-spacing:-3px;color:${TX};white-space:nowrap">${nq >= 1 ? esc(c.name) : KIN(c.name, nq)}</div>`;
      if (swapC) { const xq = ss(c01(lt / .5)), oq = c01(lt / .25);
        if (xq < 1) inner = ZP(pc, CWd, CHd) + `<div style="position:absolute;inset:0;opacity:${xq.toFixed(3)}">${inner}</div>`;
        if (oq < 1) nm = `<div style="position:absolute;left:30px;right:30px;bottom:${(18 + 26 * e4(oq)).toFixed(1)}px;font-size:${FIT(pc.name, 86, CWd - 60)}px;font-weight:900;letter-spacing:-3px;color:${TX};white-space:nowrap;opacity:${(1 - ss(oq)).toFixed(3)}">${esc(pc.name)}</div>` + nm;
        const pst = (pc.stats || []).filter(y => !(y.at >= 50)), so = c01(lt / .25);
        if (pst.length && so < 1) { const sw0 = Math.floor((CWd - (pst.length - 1) * 20) / pst.length);
          h += `<div class="ab" style="left:${x}px;top:${Y0 + CHd + 22}px;width:${CWd}px;display:flex;gap:20px;opacity:${(1 - ss(so)).toFixed(3)}">` + pst.map(xs => `<div style="width:${sw0}px"><div style="font-size:${FIT(xs.k, 32, sw0)}px;font-weight:700;color:${GOLD};white-space:nowrap">${esc(xs.k)}</div><div class="num" style="font-size:${FIT(xs.v, 60, sw0)}px;font-weight:900;color:${xs.hi ? GOLD : TX};white-space:nowrap;line-height:1.12">${esc(xs.v)}</div></div>`).join('') + `</div>`; } }
      h += `<div class="ab" style="left:${x}px;top:${(Y0 + (1 - e4(q)) * 30).toFixed(1)}px;width:${CWd}px;height:${CHd}px;border-radius:32px;overflow:hidden;opacity:${c01(q * 2).toFixed(3)};box-shadow:0 26px 60px rgba(0,0,0,.45),inset 0 0 0 1px rgba(255,255,255,.08)">${inner}<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,16,24,.9),transparent 42%)"></div><div style="position:absolute;left:0;right:0;top:0;height:7px;background:${L0 ? GOLD : BLU}"></div>
        ${nm}</div>`;
      if (st.length) { const sw = Math.floor((CWd - (st.length - 1) * 20) / st.length);
        h += `<div class="ab" style="left:${x}px;top:${Y0 + CHd + 22}px;width:${CWd}px;display:flex;gap:20px">` + st.map(xs => { const hadS = keepC && (pc.stats || []).some(y => y.k === xs.k && y.v === xs.v && !(y.at >= 50)), sq = hadS ? 1 : Math.min(AT(s, xs.at, .5, nq), c01(q * 2), swapC ? c01((lt - .25) / .3) : 1);   /* 11/10 01:19 사용자: 카드가 나오기 전엔 그 사람 글도 안 보이게 */
          return `<div style="width:${sw}px;${up(sq, 18)}"><div style="font-size:${FIT(xs.k, 32, sw)}px;font-weight:700;color:${GOLD};white-space:nowrap">${esc(xs.k)}</div><div class="num" style="font-size:${FIT(xs.v, 60, sw)}px;font-weight:900;color:${xs.hi ? GOLD : TX};white-space:nowrap;line-height:1.12">${MASK(esc(NUMV(xs.v, sq)), sq)}</div></div>`; }).join('') + `</div>`; } });
    if (P && P.title && P.title !== s.title && (s._chain || dc)) { const oq = c01(lt / .25), pp = String(P.title).split(' · ');   /* 같은 묶음에서 제목이 바뀌면 앞 제목은 0.25초에 위로 빠짐 */
      if (oq < 1) h += `<div class="ab" style="left:0;right:0;top:${(140 - 26 * e4(oq)).toFixed(1)}px;text-align:center;white-space:nowrap;opacity:${(1 - ss(oq)).toFixed(3)}"><span style="font-size:${FIT(pp[0], 70, 1000)}px;font-weight:900;color:${TX};letter-spacing:-2px">${esc(pp[0])}</span>${pp[1] ? `<span style="font-size:${FIT(pp.slice(1).join(' · '), 52, 760)}px;font-weight:900;color:${GOLD};margin-left:24px">${esc(pp.slice(1).join(' · '))}</span>` : ''}</div>`; }
    if (s.title) { const parts = String(s.title).split(' · '); const big = parts[0], small = parts.slice(1).join(' · ');
      h += `<div class="ab" style="left:0;right:0;top:140px;text-align:center;white-space:nowrap"><span style="font-size:${FIT(big, 70, 1000)}px;font-weight:900;color:${TX};letter-spacing:-2px">${sameT ? esc(big) : KIN(big, tq)}</span>${small ? `<span style="font-size:${FIT(small, 52, 760)}px;font-weight:900;color:${GOLD};margin-left:24px">${sameT ? esc(small) : KIN(small, c01(tq * 1.2 - .2))}</span>` : ''}</div>`; }
    return h;
  };
  /* 연표: 축이 그려지고 칸마다 점·날짜·내용 */
  R.tline = (lt, s) => {
    /* 11/10 01:17 사용자 "첫 장면에서 두 번째 장면으로 자연스럽게 넘어가지 않고 뚝뚝 끊겨": 같은 묶음에서 제목·칸 글이 바뀌면
       앞 글은 0.25초에 위로 빠지고 새 글이 아래에서 올라온다(바뀐 칸은 그 말을 하는 호흡 at 에) · hl = 그 호흡에 칸이 한 번 반짝(링) */
    const its = s.items || [], P = s._prev && s._prev.type === 'tline' && s._prev._cid === s._cid ? s._prev : null, pits = P ? (P.items || []) : [];
    const n = its.length, SPAN = Math.min(n === 4 ? 1320 : 1500, (n - 1) * 560), X0 = 960 - SPAN / 2, X1 = 960 + SPAN / 2, Y = 560, dx = n > 1 ? (X1 - X0) / (n - 1) : 0;
    const split = t => { const p = String(t || '').split(' · '); return p.length > 1 ? [p[0], p.slice(1).join(' · ')] : ['', p[0]]; };
    const [ey, tt] = split(s.title), [pey, ptt] = P ? split(P.title) : ['', ''];
    let h = '';
    h += eyebrow(ey, P && pey === ey ? 1 : sg(lt, 0, .8), 120, 170);
    const TY = ey ? 230 : 190, tf = t => FIT(t, 78, 1600);
    if (P && ptt !== tt) { const oq = c01(lt / .25), nq = sg(lt, .12, .9);
      if (oq < 1) h += `<div class="ab" style="left:116px;top:${(TY - 30 * e4(oq)).toFixed(1)}px;font-size:${tf(ptt)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap;opacity:${(1 - ss(oq)).toFixed(3)}">${esc(ptt)}</div>`;
      h += `<div class="ab" style="left:116px;top:${TY}px;font-size:${tf(tt)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${KIN(tt, nq)}</div>`; }
    else { const tq = P ? 1 : sg(lt, 0, 1.0); h += `<div class="ab" style="left:116px;top:${TY}px;font-size:${tf(tt)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${tq >= 1 ? esc(tt) : KIN(tt, tq)}</div>`; }
    const prevOf = x => pits.find(y => y.d === x.d && !(y.at >= 50));
    const qs = its.map(x => { if (x.at != null && x.at >= 50) return 0; const pv = prevOf(x); if (pv && pv.t === x.t) return 1; if (pv && x.at != null && x.at < 0) return 1; return AT(s, x.at, .6, 1); });
    let last = -1; qs.forEach((q, i) => { if (q > 0 || prevOf(its[i])) last = i; });
    const lineP = last < 0 ? 0 : (last + (prevOf(its[last]) ? 1 : Math.min(1, e4(qs[last])))) / Math.max(1, n - 1);
    h += `<div class="ab" style="left:${X0}px;top:${Y - 2}px;width:${X1 - X0}px;height:4px;background:rgba(255,255,255,.10)"></div><div class="ab" style="left:${X0}px;top:${Y - 2}px;width:${((X1 - X0) * c01(lineP)).toFixed(1)}px;height:4px;background:linear-gradient(90deg,${BLU},${GOLD})"></div>`;
    const colOf = c => c === 'bad' ? REDC : c === 'gold' ? GOLD : c === 'good' ? GRN : SOFT;
    const cw = Math.min(n > 4 ? 300 : 520, (dx || 600) - 20);
    const tfs0 = t => { const tl = String(t).split('\n'); return Math.min(...tl.map(l => FIT(l, 60, cw))); }, uniF = s.uni ? Math.min(...its.map(x => tfs0(x.t))) : 0, tfs = t => s.uni ? uniF : tfs0(t);   /* 11/12 uni: 칸마다 글자 크기 같게(카운트다운 표) */
    its.forEach((x, i) => { const q = qs[i], pv = prevOf(x), cx = X0 + dx * i, c = colOf(x.c), swap = !!(pv && pv.t !== x.t), dotQ = pv ? 1 : q;
      const hq = x.hl != null ? AT(s, x.hl, .6, 0) : 0, ring = hq > 0 && hq < 1 ? `,0 0 0 ${(6 + 22 * hq).toFixed(1)}px rgba(200,226,255,${(.5 * (1 - hq)).toFixed(3)})` : '';
      const ph = x.at != null && x.at >= 50 ? 0 : (P ? 1 : sg(lt, .15, .8));   /* 11/10 10:33: 결과가 나오기 전에도 칸 이름·빈 점은 보임(빈 화면 ✗) */
      if (ph > 0 && dotQ < 1) h += `<div class="ab" style="left:${cx - 14}px;top:${Y - 14}px;width:28px;height:28px;border-radius:50%;background:${INK0};box-shadow:0 0 0 4px rgba(255,255,255,.22);${op(ph)}"></div>`;
      h += `<div class="ab" style="left:${cx - 18}px;top:${Y - 18}px;width:36px;height:36px;border-radius:50%;background:${INK0};box-shadow:0 0 0 6px ${c}${dotQ >= 1 ? `,0 0 22px ${c}` : ''}${ring};transform:scale(${(dotQ > 0 ? L(.2, 1, e4(dotQ)) : 0).toFixed(3)})"></div>`;
      h += `<div class="ab" style="left:${cx - cw / 2}px;width:${cw}px;top:${Y - 116}px;text-align:center;font-size:${FIT(x.d, 40, cw)}px;font-weight:700;color:${MU};white-space:nowrap;${pv ? '' : up(Math.max(q, ph), -16)}">${esc(x.d)}</div>`;
      const txt = (t, f, extra) => `<div class="ab" style="left:${cx - cw / 2}px;width:${cw}px;top:${Y + 46}px;text-align:center;font-size:${f}px;line-height:1.2;font-weight:900;color:${c};white-space:nowrap;${extra}">${String(t).split('\n').map(esc).join('<br>')}</div>`;
      if (swap) { const oq = c01(q / .45); if (oq < 1) h += txt(pv.t, tfs(pv.t), `opacity:${(1 - ss(oq)).toFixed(3)};transform:translateY(${(-22 * e4(oq)).toFixed(1)}px)`); h += txt(x.t, tfs(x.t), up(c01((q - .25) / .75), 22)); }
      else h += txt(x.t, tfs(x.t), pv ? '' : up(q, 20)); });
    return h;
  };
  /* 질문: 큰 글자 두 줄(앞부분 흰색 · 뒷부분 금색) + 뒤에 큰 물음표 + 로고 */
  R.question = (lt, s) => {
    const parts = String(s.text || '').split(' · '), a = parts.length > 1 ? parts[0] : '', b = parts.length > 1 ? parts.slice(1).join(' · ') : parts[0];
    const P = s._prev && s._prev.type === 'question' && s._prev.text === s.text && J(s._prev.logos || []) === J(s.logos || []) ? s._prev : null;   /* 11/12 검수: 같은 질문 이어지는 장면(e2→e3)에서 글이 지워졌다 다시 타이핑 ✗ */
    const q0 = P ? 1 : sg(lt, 0, 1.0), q1 = P ? 1 : (s.textAt != null ? AT(s, s.textAt, 1.0, 0) : q0), q2 = P ? 1 : (s.textAt != null ? AT(s, s.textAt + .25, 1.0, 0) : sg(lt, a ? .35 : 0, 1.0)), lq = P ? 1 : AT(s, s.logoAt, .5, sg(lt, .6, .5)), lg = s.logos || [];
    let h = `<div class="ab" style="right:100px;top:40px;font-size:900px;line-height:1;font-weight:900;color:transparent;-webkit-text-stroke:4px rgba(200,226,255,${(s.noQ ? 0 : .28 * c01(q0 * 2)).toFixed(3)})">?</div>`;
    const many = lg.length > 3, Y = many ? 230 : 300;
    if (a) h += `<div class="ab" style="left:120px;top:${Y}px;font-size:${FIT(a, 88, 1500)}px;font-weight:900;letter-spacing:-3px;color:${TX};white-space:nowrap">${KIN(a, q1)}</div>`;
    h += `<div class="ab" style="left:120px;top:${Y + (a ? 120 : 40)}px;font-size:${FIT(b, a ? 104 : 118, 1560)}px;font-weight:900;letter-spacing:-3px;color:${GOLD};white-space:nowrap">${KIN(b, q2)}</div>`;
    h += `<div class="ab" style="left:120px;top:${Y + (a ? 270 : 210)}px;width:${(520 * e4(q2)).toFixed(1)}px;height:4px;background:linear-gradient(90deg,${GOLD},transparent)"></div>`;
    if (lg.length) { const w = many ? 110 : (s.logoSize || 180) * .85;
      h += `<div class="ab" style="left:120px;top:${Y + (a ? 320 : 260)}px;display:flex;gap:${many ? 30 : 46}px">` + lg.map((t, i) => `<div style="${up(c01(lq * (1 + lg.length * .12) - i * .12), 26)}">${LG(t, w)}</div>`).join('') + `</div>`; }
    return h;
  };
  /* 선수 기록(pstat): 오른쪽 사선 사진 · 왼쪽 이름 · 아래로 쌓이는 칸(도장·단계·한마디·기록) */
  R.pstat = (lt, s) => {
    const pr = s._prev && /^(pstat|rf_card|speech)$/.test(s._prev.type) ? s._prev : null;
    const keepP = !!(pr && photoSrc(pr.img) && photoSrc(pr.img) === photoSrc(s.img)), keepN = !!(pr && pr.name === s.name && /^(pstat|rf_card)$/.test(pr.type)), ebSame = keepN && (pr.sub || pr.kicker || '') === (s.sub || '');
    const JJ = x => JSON.stringify(x, (k, v) => k === 'hi' ? undefined : k === 'at' ? (v >= 50 ? 'H' : undefined) : v);
    const had = x => keepN && pr.type === s.type && [...(pr.viz || []), ...(pr.stats || [])].some(y => JJ(y) === JJ(x));
    const P = (x, d = .5) => (x.at ?? 0) >= 50 ? 0 : had(x) ? 1 : AT(s, x.at ?? 0, d, 1);
    const IA = s.imgAt != null && !keepP && !keepN ? AT(s, s.imgAt, .7, 0) : (keepP || keepN ? 1 : sg(lt, 0, .7));
    let h = panel(s, lt, keepP || keepN ? 1 : IA, keepN && pr ? pr.img : null);
    h += nameBlock(s, lt, keepN ? 1 : (s.imgAt != null ? IA : sg(lt, .05, .9)), keepN, CX0, 160, CW0, false, keepN && !ebSame ? sg(lt, .08, .45) : null);
    const grp = (CHAINS[s._cid] || [s._k]).map(k => SC[k]).filter(x => x && x.type === 'pstat' && x.name === s.name);
    const nSteps = Math.max(0, ...grp.map(x => Math.max(0, ...(x.viz || []).filter(z => z.type === 'steps').map(z => (z.items || []).length))));
    const nViz = Math.max(...grp.map(x => (x.viz || []).length + ((x.stats || []).length ? 1 : 0)));
    const X = CX0, W = CW0, tight = nSteps > 3 || nViz > 3; let y = 430;
    /* 11/10 10:33 사용자 "이런 장면 안 나오게"(사진·이름 없이 도장만 떠 있는 빈 화면) → 사진이 나오기 전 도장은 화면 가운데 크게(그 장면의 주제),
       사진이 들어오면 제자리로 줄어들며 이동 */
    const pre = s.imgAt != null && !keepP && !keepN, stz = (s.viz || []).filter(z => z.type === 'stamp'), gm = pre ? e4(c01(IA * 1.1)) : 1, GS = 1.45;
    const gW = Math.max(200, ...stz.map(z => WL(z.t) * FIT(z.t, tight ? 52 : 66, W - 80, 34) + 70)), gH = stz.reduce((a, z) => a + FIT(z.t, tight ? 52 : 66, W - 80, 34) + 50, 0) - 50;
    const gx = L(960 - gW * GS / 2, X, gm), gy = L(520 - gH * GS / 2, 430, gm), gsc = L(GS, 1, gm);
    (s.viz || []).forEach(z => {
      if (z.type === 'stamp') { const q = P(z, .5), c = z.c === 'bad' ? REDC : z.c === 'good' ? GRN : GOLD, fs = FIT(z.t, tight ? 52 : 66, W - 80, 34), pop = 1;
        const tx = gx - X, ty = gy + (y - 430) * gsc - y;
        if (q > 0) h += `<div class="ab" style="left:${X}px;top:${y}px;transform-origin:left top;transform:translate(${tx.toFixed(1)}px,${ty.toFixed(1)}px) scale(${(gsc * pop).toFixed(3)});opacity:${c01(q * 2).toFixed(3)}"><div style="display:inline-block;padding:8px 30px;background:${c};color:${INK0};font-size:${fs}px;font-weight:900;letter-spacing:-1px;white-space:nowrap;border-radius:32px;position:relative;overflow:hidden;transform-origin:0 100%;transform:${SQ(q)}">${esc(z.t)}${SHEEN(q)}</div></div>`;
        y += fs + 50; }
      else if (z.type === 'steps') { const its = z.items || [], fs = tight ? 46 : 58, rh = fs + (tight ? 22 : 30), dw = Math.max(...grp.flatMap(x => (x.viz || []).filter(v => v.type === 'steps').flatMap(v => (v.items || []).map(w => WL(w.d) * 34 + 14))), 130);
        const qs = its.map(x => (x.at ?? 0) >= 50 ? 0 : had(z) && (pr.viz || []).some(v => (v.items || []).some(w => JJ(w) === JJ(x))) ? 1 : AT(s, x.at ?? 0, .5, 1));
        let last = -1; qs.forEach((q, k) => { if (q > 0) last = k; });
        /* 점을 잇는 세로선이 지금 줄까지 그어진다(내용 쪽 모션) */
        if (last > 0) { const lp = (last - 1 + e4(qs[last])) * rh; h += `<div class="ab" style="left:${X + dw + 25}px;top:${y + rh / 2 - 6}px;width:3px;height:${lp.toFixed(1)}px;background:linear-gradient(${BLU},${GOLD})"></div>`; }
        its.forEach((x, k) => { const q = qs[k], c = x.c === 'bad' ? REDC : x.c === 'gold' ? GOLD : x.c === 'good' ? GRN : TX;
          const tt = String(x.t).replace(/\n/g, ' '), tf = FIT(tt, fs, W - dw - 70, 30);
          h += `<div class="ab" style="left:${X}px;top:${y}px;width:${W}px;height:${rh - 8}px;display:flex;align-items:center;gap:20px;${up(q, 18)}"><div style="width:${dw}px;flex:0 0 auto;font-size:34px;font-weight:700;color:${MU};white-space:nowrap">${esc(x.d)}</div><div style="width:18px;height:18px;flex:0 0 auto;border-radius:50%;background:${c};box-shadow:0 0 0 5px ${INK0}"></div><div style="font-size:${tf}px;font-weight:900;color:${c};white-space:nowrap;letter-spacing:-1px">${esc(tt)}</div></div>`;
          y += rh; });
        for (let k = its.length; k < nSteps; k++) y += rh;
        y += 16; }
      else if (z.type === 'quote') { const q = P(z, .55), f1 = FIT(z.text, 48, W - 130, 20), two = f1 < 42, fs = two ? FIT(z.text, 48, (W - 130) * 1.75, 36) : f1, uq = c01(q * 1.4 - .4);
        h += `<div class="ab" style="left:${X}px;top:${y}px;width:${W}px;padding:22px 30px 26px 90px;background:rgba(255,255,255,.06);border-radius:36px;${up(q, 20)}"><div style="position:absolute;left:24px;top:-8px;font-size:120px;line-height:1;color:${GOLD};font-weight:900">“</div>${z.date ? `<div style="font-size:30px;font-weight:700;color:${GOLD};margin-bottom:8px">${esc(z.date)}</div>` : ''}<div style="font-size:${fs}px;font-weight:900;color:${TX};line-height:1.3;word-break:keep-all;text-wrap:balance">${esc(z.text)}</div><div style="height:4px;margin-top:12px;width:${(e4(uq) * 100).toFixed(1)}%;background:linear-gradient(90deg,${GOLD},transparent)"></div></div>`;
        y += fs * 1.3 * (two ? 2 : 1) + (z.date ? 42 : 0) + 84; }
    });
    const st = s.stats || [];
    /* 11/13 00:52 사용자 "이 형식(작은 글 · 점 · 값 목록)은 이해가 잘 안돼" → 기록은 타일(이름 작게 · 값 크게), 3개 이상이면 2열 */
    if (st.length) { const cols = st.length > 2 ? 2 : st.length, cw = Math.floor((W - (cols - 1) * 24) / cols);
      h += `<div class="ab" style="left:${X}px;top:${Math.max(y, 430)}px;width:${W}px;display:flex;flex-wrap:wrap;gap:24px">` + st.map(x => { const q = P(x, .55), vf = FIT(x.v, 64, cw - 36, 28);
        return `<div style="width:${cw}px;padding:16px 20px 20px;border-radius:36px;background:${x.hi ? 'rgba(200,226,255,.16)' : 'rgba(255,255,255,.06)'};box-shadow:inset 0 4px 0 ${x.hi ? GOLD : BLU};${up(q, 18)}"><div style="font-size:${FIT(x.k, 32, cw - 36, 24)}px;font-weight:700;color:${x.hi ? GOLD : MU};white-space:nowrap">${esc(x.k)}</div><div class="num" style="font-size:${vf}px;font-weight:900;color:${TX};white-space:nowrap;line-height:1.15;margin-top:6px">${MASK(esc(NUMV(x.v, q)), q)}</div></div>`; }).join('') + `</div>`; }
    return h;
  };
  /* 선수 카드(rf_card): 이름 + 아주 큰 값 하나 + 작은 기록 */
  R.rf_card = (lt, s) => {
    const pr = s._prev && /^(pstat|rf_card|speech)$/.test(s._prev.type) ? s._prev : null;
    const keepP = !!(pr && photoSrc(pr.img) && photoSrc(pr.img) === photoSrc(s.img)), keepN = !!(pr && pr.name === s.name && /^(pstat|rf_card)$/.test(pr.type)), ebSame = keepN && (pr.sub || pr.kicker || '') === (s.kicker || ''), sameT = keepN && pr.type === s.type;
    const IA = keepP || keepN ? 1 : AT(s, s.imgAt, .7, sg(lt, 0, .7)), NA = keepN ? 1 : AT(s, s.nameAt, .9, sg(lt, .05, .9));
    let h = panel(s, lt, IA, keepN && pr ? pr.img : null) + nameBlock(Object.assign({}, s, { sub: s.kicker }), lt, NA, keepN, CX0, 160, CW0, false, keepN && !ebSame ? sg(lt, .08, .45) : null);
    const b = s.big || {}, sameB = !!(sameT && pr.big && pr.big.v === b.v), bq = sameB ? 1 : AT(s, b.at, .8, 1), bs = FIT(b.v, Math.min((b.size || 150) * 1.2, 210), CW0, 80);
    const BY = 440;
    if (b.v) h += `<div class="ab" style="left:${CX0 - 6}px;top:${BY}px;font-size:${bs}px;font-weight:900;letter-spacing:-5px;line-height:1.1;color:${GOLD};white-space:nowrap;text-shadow:0 10px 40px rgba(0,0,0,.4)">${bq >= 1 ? esc(b.v) : KIN(b.v, bq)}</div>`
      + (b.k ? `<div class="ab" style="left:${CX0}px;top:${BY + bs * 1.12 + 6}px;font-size:${FIT(b.k, 48, CW0)}px;font-weight:700;color:${MU};white-space:nowrap;${op(c01(bq * 1.3 - .3))}">${esc(b.k)}</div>` : '');
    const mn = s.minor || [];
    if (mn.length) { const cw = Math.floor((CW0 - (mn.length - 1) * 24) / mn.length), my = BY + bs * 1.12 + 90;
      h += `<div class="ab" style="left:${CX0}px;top:${my}px;display:flex;gap:24px">` + mn.map(x => { const had = sameT && (pr.minor || []).some(y => y.k === x.k && y.v === x.v), q = had ? 1 : AT(s, x.at, .55, 1);
        return `<div style="width:${cw}px;padding:14px 20px 18px;border-radius:36px;background:rgba(255,255,255,.06);box-shadow:inset 0 4px 0 ${BLU};${up(q, 18)}"><div style="font-size:${FIT(x.k, 32, cw - 36, 24)}px;font-weight:700;color:${MU};white-space:nowrap">${esc(x.k)}</div><div class="num" style="font-size:${FIT(x.v, 62, cw - 36, 28)}px;font-weight:900;color:${TX};white-space:nowrap;line-height:1.15">${MASK(esc(NUMV(x.v, q)), q)}</div></div>`; }).join('') + `</div>`; }
    return h;
  };
  /* 발언(speech): 오른쪽 사진 · 왼쪽 인용 카드가 쌓이고, 지금 말하는 줄(hi)만 밝게 */
  R.speech = (lt, s) => {
    const pr = s._prev && /^(pstat|rf_card|speech)$/.test(s._prev.type) ? s._prev : null;
    const keepP = !!(pr && photoSrc(pr.img) && photoSrc(pr.img) === photoSrc(s.img)), keepN = !!(pr && pr.name === s.name && pr.type === 'speech');
    const IA = keepP || keepN ? 1 : sg(lt, 0, .7);
    let h = panel(s, lt, IA, keepN && pr ? pr.img : null);
    h += nameBlock(Object.assign({}, s, { sub: '' }), lt, keepN ? 1 : sg(lt, .05, .9), keepN, CX0, 110, CW0, true);
    const bs = s.bubbles || [], grp = (CHAINS[s._cid] || [s._k]).map(k => SC[k]).filter(x => x && x.type === 'speech');
    const nB = Math.max(...grp.map(x => (x.bubbles || []).length)), W = CW0, fs = nB > 2 ? 40 : 50;
    let y = 340;
    bs.forEach((b, i) => { const shown = (b.at ?? 0) < 50, had = keepN && (pr.bubbles || []).some(x => x.text === b.text && !(x.at >= 50)), q = !shown ? 0 : had ? 1 : AT(s, b.at, .55, 1);
      const hi = !!b.hi, lines = Math.ceil(WL(b.text) * fs / (W - 130)), hgt = Math.round(lines * fs * 1.32 + (b.date ? 40 : 0) + 50);
      h += `<div class="ab" style="left:${CX0}px;top:${y}px;width:${W}px;height:${hgt}px;box-sizing:border-box;padding:4px 30px 0 92px;display:flex;flex-direction:column;justify-content:center;border-radius:36px;background:${hi ? 'rgba(200,226,255,.13)' : 'rgba(255,255,255,.05)'};box-shadow:inset 5px 0 0 ${hi ? GOLD : 'rgba(255,255,255,.22)'};${up(q, 20)}"><div style="position:absolute;left:24px;top:${Math.round(hgt / 2 - 34)}px;font-size:110px;line-height:1;color:${hi ? GOLD : 'rgba(255,255,255,.3)'};font-weight:900">“</div>${b.date ? `<div style="font-size:30px;font-weight:700;line-height:1.1;color:${hi ? GOLD : MU};margin-bottom:6px">${esc(b.date)}</div>` : ''}<div style="font-size:${fs}px;font-weight:900;color:${hi ? TX : 'rgba(242,244,248,.6)'};line-height:1.32;word-break:keep-all;text-wrap:balance">${esc(b.text)}</div></div>`;
      y += hgt + 20; });
    return h;
  };
  /* B3 rf_bars: 가로 막대(라벨 왼쪽 · 막대가 자라며 빛이 지나감 · 값은 끝에), 강조 줄만 금색 */
  R.rf_bars = (lt, s) => {
    const its = s.items || [], mx = s.max || Math.max(...its.map(x => x.v)) * 1.1, n = its.length, X = 120, LW = 560, BW = 1680 - LW - 40, BH = n > 3 ? 70 : 92, GP = n > 3 ? 46 : 70, tq = sg(lt, 0, 1.0);
    const tp = String(s.title || '').split(' · ');
    let h = ghostWord(tp[0], lt, 140) + eyebrow(tp.length > 1 ? tp.slice(1).join(' · ') : '', c01(tq * 1.4), X, 170)
      + `<div class="ab" style="left:${X - 4}px;top:${tp.length > 1 ? 232 : 190}px;font-size:${FIT(tp[0], 80, 1600)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${KIN(tp[0], tq)}</div>`;
    const Y0 = 420 + (n < 3 ? 40 : 0);
    its.forEach((x, i) => { const q = AT(s, x.at, .9, 1), vq = AT(s, x.valAt ?? x.at, .5, 1), y = Y0 + i * (BH + GP), w = BW * x.v / mx * e4(q), c = x.hi ? GOLD : BLU;
      h += `<div class="ab" style="left:${X}px;top:${y}px;width:${LW}px;height:${BH}px;display:flex;align-items:center;font-size:${FIT(x.label, s.lfs ? s.lfs + 4 : 40, LW - 10, 26)}px;font-weight:900;color:${x.hi ? GOLD : TX};white-space:nowrap;${op(q)}">${esc(x.label)}</div>`
        + `<div class="ab" style="left:${X + LW + 40}px;top:${y}px;width:${BW}px;height:${BH}px;background:rgba(255,255,255,.05)"></div>`
        + `<div class="ab" style="left:${X + LW + 40}px;top:${y}px;width:${w.toFixed(1)}px;height:${BH}px;background:${x.hi ? `linear-gradient(90deg,#B8964F,${GOLD})` : `linear-gradient(90deg,#2F5D9C,${SOFT})`};box-shadow:0 0 30px ${x.hi ? 'rgba(200,226,255,.35)' : 'rgba(76,130,201,.3)'}"></div>`
        + (q > 0 && q < 1 ? `<div class="ab" style="left:${(X + LW + 40 + w - 140).toFixed(1)}px;top:${y}px;width:140px;height:${BH}px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35))"></div>` : '')
        + `<div class="ab" style="left:${(X + LW + 40 + Math.max(w, 0) + 22).toFixed(1)}px;top:${y + BH / 2 - 30}px;font-size:${FIT(x.txt, 52, Math.max(260, X + LW + 40 + BW - (X + LW + 40 + BW * x.v / mx) - 40), 30)}px;font-weight:900;color:${c};white-space:nowrap;${op(vq)}">${esc(x.txt || '')}</div>`; });
    return h;
  };
  /* 샐러리캡 막대: 틀이 그려지고 → 합계가 차오름(빛) → 상한선이 내려와 꽂힘(빨강 번짐) → 남는 칸 금 빗금 */
  R.rf_capbar = (lt, s) => {
    /* 11/10 01:26 사용자 "같은 막대그래프 장면인데 화면전환이 한 번 되고 다시 그래프를 보여주니까 정신사나워 — 그대로 있고 내용만 바뀌면" → 앞 장면도 막대면(묶음이 아니어도) 틀·상한선은 그대로,
       합계 막대는 앞 값에서 새 값으로 늘거나 줄고, 제목은 바뀔 때만 앞 글이 위로 빠지고 새 글이 올라온다. 앞 장면에만 있던 칸(빼는 몫·남는 돈 등)은 0.2초에 빠진다 */
    const K = !!(s._prev && s._prev.type === 'rf_capbar'), KC = !!(K && s._chain), A0 = { total: s.totalAt, left: s.leftAt, cap: s.capAt }, MX = s.mx || 175, X0 = 120, BW = 1680, Y = 470, BH = 170;
    const X = v => X0 + BW * v / MX, P = K ? s._prev : null, sameWho = !!(P && P.who === s.who), wq = sameWho ? 1 : AT(s, s.whoAt, .9, sg(lt, K ? .12 : 0, .9));
    let h = '';
    if (K) { const oq = c01(lt / .2); if (oq < 1) { const sv = NOW;   /* 11/10: 묶음(KC) 안에서도 앞에만 있던 칸(결과·빠지는 몫)이 툭 사라지지 않게 */
      NOW = BD[s._k - 1] - .001; const old = R.rf_capbar(99, Object.assign({}, P, { _prev: null, _chain: false, _under: 1, _capSame: P.cap === s.cap && P.capLab === s.capLab })); NOW = sv;   /* 앞 막대 장면의 칸·글은 0.2초에 빠짐(틀·같은 값은 새 장면이 그대로 그림) */
      h += `<div class="ab" style="inset:0;opacity:${(1 - ss(oq)).toFixed(3)}">${old}</div>`; } }
    if (P && !sameWho) { const oq = c01(lt / .25); if (oq < 1 && !K) h += `<div class="ab" style="left:${X0}px;top:${(180 - 24 * e4(oq)).toFixed(1)}px;font-size:${FIT(P.who, 66, 1100)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap;opacity:${(1 - ss(oq)).toFixed(3)};padding-left:${P.team ? 90 : 0}px">${esc(P.who || '')}</div>`; }
    h += `<div class="ab" style="left:${X0}px;top:180px;display:flex;align-items:center;gap:20px">${s.team ? `<div style="${op(P && P.team === s.team ? 1 : wq)}">${LG(s.team, 70)}</div>` : ''}<div style="font-size:${FIT(s.who, 66, 1100)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${sameWho ? esc(s.who || '') : KIN(s.who || '', wq)}</div>${s.tag ? `<div style="padding:6px 18px;background:${GOLD};color:${INK0};font-size:34px;font-weight:900;transform:skewX(-12deg);white-space:nowrap;${op(sameWho && P.tag === s.tag ? 1 : AT(s, s.tagAt, .45, 1))}"><div style="transform:skewX(12deg)">${esc(s.tag)}</div></div>` : ''}</div>`;
    const tot = s.total || 0, cap = s.cap || 0, pt = K ? (P.total || 0) : 0;
    /* 앞 장면이 막대가 아니면(사이에 다른 장면이 끼었으면) '이미 보인 것(at -1)'도 처음부터 다시 그린다 — 다른 장면 위에 다 그려진 막대가 툭 나타나지 않게 */
    if (!K) { if (A0.total != null && A0.total < 0) A0.total = null; if (A0.cap != null && A0.cap < 0) A0.cap = null; }
    const fq = K ? 1 : sg(lt, 0, .7), cq = K && P.cap === cap ? 1 : AT(s, A0.cap, .55, sg(lt, .1, .55)), lq = AT(s, A0.left, .6, 1);
    let tq = AT(s, A0.total, .9, sg(lt, .15, .9)); if (K && pt !== tot && (A0.total == null || A0.total < 0)) tq = sg(lt, .1, .9);
    const tcur = L(K ? pt : 0, tot, e4(K && pt === tot ? 1 : tq)), tw = BW * tcur / MX, XT = K && pt !== tot ? X(tcur) : X(tot);   /* 11/10: 합계가 바뀌는 동안 뒤 칸(더하는 몫·남는 돈)도 합계 끝을 따라감 */
    /* 틀(선처럼 그려짐) */
    h += `<div class="ab" style="left:${X0}px;top:${Y}px;width:${(BW * e4(fq)).toFixed(1)}px;height:${BH}px;background:rgba(255,255,255,.05);box-shadow:inset 0 0 0 2px rgba(232,236,242,.16)"></div>`;
    /* 합계 */
    h += `<div class="ab" style="left:${X0}px;top:${Y}px;width:${tw.toFixed(1)}px;height:${BH}px;background:linear-gradient(90deg,#2F5D9C,${SOFT})"></div>`;
    if (tq > 0 && tq < 1) h += `<div class="ab" style="left:${(X0 + tw - 160).toFixed(1)}px;top:${Y}px;width:160px;height:${BH}px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35))"></div>`;
    if (s.totalLab || s.totalTxt) { const sameTL = !!(K && P.totalLab === s.totalLab && P.totalTxt === s.totalTxt), xq = sameTL ? 1 : s.totalTxtAt != null ? AT(s, s.totalTxtAt, .5, 1) : tq;
      h += `<div class="ab" style="left:${X0 + 28}px;top:${Y + 12}px;${op(sameTL || (K && P.totalLab === s.totalLab) ? 1 : K ? c01(lt / .3) : tq)}"><div style="font-size:34px;font-weight:700;color:#E6EDF7;white-space:nowrap">${esc(s.totalLab || '')}</div><div class="num" style="font-size:64px;font-weight:900;line-height:1.08;white-space:nowrap;color:#fff">${MASK(esc(s.totalTxt || ''), xq)}</div></div>`; }
    if (cap > tot && (s.leftTxt || s.leftLab)) { const x1 = XT, x2 = X(cap);
      h += `<div class="ab" style="left:${x1}px;top:${Y}px;width:${((x2 - x1) * e4(lq)).toFixed(1)}px;height:${BH}px;background:repeating-linear-gradient(115deg,${GOLD} 0 22px,#A78BFF 22px 44px);box-shadow:0 0 34px rgba(200,226,255,.4)"></div>
        <div class="ab" style="left:${Math.min((x1 + x2) / 2, x2 - 210) - 300}px;width:600px;top:${Y + BH + 22}px;text-align:center;${up(lq, 18)}"><div class="num" style="font-size:84px;font-weight:900;color:${GOLD};line-height:1;white-space:nowrap">${esc(s.leftTxt || '')}</div><div style="font-size:36px;font-weight:700;color:${MU};margin-top:10px;white-space:nowrap">${esc(s.leftLab || '')}</div></div>`; }
    if (s.minus) { const m = s.minus, mq = AT(s, m.at, .6, 1), x1 = XT, w = BW * m.v / MX, over = tot + m.v > cap;
      h += `<div class="ab" style="left:${x1}px;top:${Y - 8}px;width:${(w * e4(mq)).toFixed(1)}px;height:${BH + 16}px;background:repeating-linear-gradient(135deg,rgba(234,104,96,.95) 0 14px,rgba(150,40,46,.95) 14px 28px);box-shadow:0 0 26px rgba(224,103,95,.4)"></div>
        <div class="ab" style="left:${x1 + w / 2 - 300}px;width:600px;top:${Y - 120}px;text-align:center;${up(mq, -16)}"><div style="font-size:32px;font-weight:700;color:#F6B8B2;white-space:nowrap">${esc(m.lab || '')}</div><div class="num" style="font-size:54px;font-weight:900;color:#FF8A80;white-space:nowrap">${m.sign == null ? '− ' : esc(m.sign)}${esc(m.txt || '')}</div></div>`;
      if (s.minus2) { const m2 = s.minus2, q2 = AT(s, m2.at, .6, 1), x2 = XT + BW * m.v / MX, w2 = BW * m2.v / MX;
        h += `<div class="ab" style="left:${x2}px;top:${Y - 8}px;width:${(w2 * e4(q2)).toFixed(1)}px;height:${BH + 16}px;background:repeating-linear-gradient(135deg,rgba(240,168,80,.95) 0 14px,rgba(150,92,30,.95) 14px 28px)"></div>
          <div class="ab" style="left:${x2 + w2 / 2 - 300}px;width:600px;top:${Y + BH + 84}px;text-align:center;${up(q2, 16)}"><div class="num" style="font-size:50px;font-weight:900;color:#FFC078;white-space:nowrap">${m2.sign == null ? '+ ' : esc(m2.sign)}${esc(m2.txt || '')}</div><div style="font-size:30px;font-weight:700;color:#FFD8A8;white-space:nowrap">${esc(m2.lab || '')}</div></div>`; }
      if (s.ghost) { const g = s.ghost, gq = AT(s, g.at, .6, 1), gx = XT + BW * m.v / MX, gw = BW * g.v / MX;
        h += `<div class="ab" style="left:${gx}px;top:${Y - 8}px;width:${gw.toFixed(1)}px;height:${BH + 16}px;border:4px dashed rgba(255,150,140,.9);box-sizing:border-box;background:rgba(224,103,95,.12);${op(gq)}"></div>
          <div class="ab" style="left:${gx + gw / 2 - 300}px;width:600px;top:${Y + BH + 84}px;text-align:center;${op(gq)}"><div class="num" style="font-size:50px;font-weight:900;color:${GRN};white-space:nowrap">${esc(g.txt || '')}</div><div style="font-size:30px;font-weight:700;color:${MU};white-space:nowrap">${esc(g.lab || '')}</div></div>`; }
      if (s.result) { const r = s.result, rq = AT(s, r.at, .55, 1), rx = over ? X(cap) : (X(tot + m.v) + X(cap)) / 2;
        const rw = Math.min(1000, Math.max(600, WL(r.txt) * 70 + 40)), rl = Math.max(80, Math.min(1840 - rw, rx - rw / 2));
        h += `<div class="ab" style="left:${rl}px;width:${rw}px;top:${Y + BH + (s.ghost || s.minus2 ? 186 : 112)}px;text-align:center;${up(rq, 18)}"><div style="font-size:32px;font-weight:700;color:${MU};white-space:nowrap">${esc(r.lab || '')}</div><div class="num" style="font-size:${FIT(r.txt, 70, rw)}px;font-weight:900;color:${over ? '#FF8A80' : GOLD};line-height:1.08;white-space:nowrap">${esc(r.txt || '')}</div></div>`; } }
    if (s.over) { const o = s.over, oq = AT(s, o.at, .6, 1), x1 = X(cap), w = BW * o.v / MX;
      h += `<div class="ab" style="left:${x1}px;top:${Y}px;width:${(w * e4(oq)).toFixed(1)}px;height:${BH}px;${o.dash ? `border:4px dashed #FF8A80;box-sizing:border-box;background:rgba(224,103,95,.18)` : 'background:linear-gradient(180deg,#F07A70,#B8343B)'}"></div>
        <div class="ab" style="left:${x1 + 24}px;width:480px;top:${Y + BH + 20}px;font-size:36px;font-weight:900;color:#FF9A90;white-space:nowrap;${op(oq)}">${esc(o.lab || '')}</div>`;
      if (s.rate) { const rq = AT(s, s.rate.at, .55, 1);
        h += `<div class="ab" style="left:${Math.min(1800 - 600, x1 + w / 2 - 300)}px;width:600px;top:${Y + BH + 84}px;text-align:center;${up(rq, 18)}"><span style="display:inline-block;padding:10px 30px;background:${REDC};color:#fff;font-size:46px;font-weight:900;white-space:nowrap;transform:skewX(-10deg)">${esc(s.rate.txt)}</span></div>`; } }
    if (cap && !(s._under && s._capSame)) { const cx = X(cap), dq = e4(cq);   /* 11/14: 앞 장면 사본에서는 같은 상한선을 또 그리지 않음(0.2초 동안 선이 겹쳐 더 밝아 보임) */
      h += `<div class="ab" style="left:${cx - 3}px;top:${Y - 66}px;width:6px;height:${((BH + 132) * dq).toFixed(1)}px;background:${REDC};box-shadow:0 0 18px rgba(224,103,95,.75)"></div>`;
      if (!s.minus) h += `<div class="ab" style="left:${cx - 600}px;width:600px;top:${Y - 116}px;text-align:right;font-size:38px;font-weight:900;color:#FF9A90;white-space:nowrap;${op(cq)}">${esc(s.capLab || '')} ▼</div>`;
      else if (s.capBelow) h += `<div class="ab" style="left:${cx - 614}px;width:600px;top:${Y + BH + 22}px;text-align:right;font-size:30px;font-weight:700;color:#FF9A90;white-space:nowrap;${op(cq)}">${esc(s.capLab || '')} ▶</div>`; }
    return h;
  };


  /* ═════ 세로 쇼츠(1080×1920) 장면 — 11/10 「2027 FA 일정」부터 ═════
     자리: 위 이음 판(y60) · 제목(y150~300, 처음부터 끝까지 그대로) · 내용 y400~1300 · 자막 y1345 · 그 아래(유튜브 글·버튼 자리)는 비움 */
  let TT;
  function paintTitle(t) {
    if (!TT) { TT = document.createElement('div'); TT.id = 'mgtitle'; TT.style.cssText = 'position:absolute;left:0;top:0;width:1080px;height:330px;z-index:44;pointer-events:none'; ST.appendChild(TT); }
    const tl = (EP.vtitle || [])[0] || '', q = 1   /* 쇼츠 첫 프레임부터 제목이 다 보이게(3초 안 2027 FA) */, w = FIT(tl, 112, 960, 60);
    TT.innerHTML = `<div style="position:absolute;left:60px;right:60px;top:150px;text-align:center;font-size:${w}px;font-weight:900;letter-spacing:-3px;color:${TX};white-space:nowrap;line-height:1.1">${q >= 1 ? esc(tl) : KIN(tl, q)}</div>
      <div style="position:absolute;left:${540 - 180 * e4(q)}px;top:${150 + w * 1.18 + 14}px;width:${(360 * e4(q)).toFixed(1)}px;height:6px;background:${GOLD}"></div>`; }
  const VY0 = 400, VX = 60, VW = 960;
  /* 두 사람 카드(같은 크기) — 같은 사람이면 그대로 */
  R.v_duo = (lt, s) => {
    const cs = s.cards || [], P = s._prev && s._prev.type === 'v_duo' ? s._prev : null, CWv = 450, CHv = 600, Y = 430;
    let h = '';
    cs.slice(0, 2).forEach((c, i) => { const pc = P && P.cards[i], keep = !!(pc && pc.img === c.img), q = keep ? 1 : AT(s, c.at, .7, sg(lt, i * .1, .7)), x = i ? 1080 - 60 - CWv : 60;
      h += `<div class="ab" style="left:${x}px;top:${(Y + (1 - e4(q)) * 30).toFixed(1)}px;width:${CWv}px;height:${CHv}px;border-radius:34px;overflow:hidden;opacity:${c01(q * 2).toFixed(3)};box-shadow:0 26px 60px rgba(0,0,0,.45),inset 0 0 0 1px rgba(255,255,255,.08)">${PIC(c.img, CWv, CHv, .5, 'filter:contrast(1.06)', c.focus)}<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,16,24,.92),transparent 45%)"></div><div style="position:absolute;left:0;right:0;top:0;height:8px;background:${i ? BLU : GOLD}"></div>
        <div style="position:absolute;left:28px;right:20px;bottom:22px;font-size:${FIT(c.name, 92, CWv - 50)}px;font-weight:900;letter-spacing:-3px;color:${TX};white-space:nowrap">${keep || q >= 1 ? esc(c.name) : KIN(c.name, c01(q * 1.3 - .3))}</div></div>`; });
    if (s.tag) { const same = P && P.tag === s.tag, tq = same ? 1 : AT(s, s.tagAt, .5, sg(lt, .2, .5));
      if (P && P.tag && !same) { const oq = c01(lt / .25); if (oq < 1) h += `<div class="ab" style="left:0;right:0;top:${(1070 - 24 * e4(oq)).toFixed(1)}px;text-align:center;opacity:${(1 - ss(oq)).toFixed(3)}"><span style="font-size:50px;font-weight:900;color:${GOLD};white-space:nowrap">${esc(P.tag)}</span></div>`; }
      h += `<div class="ab" style="left:0;right:0;top:1070px;text-align:center;${up(tq, 20)}"><span style="font-size:${FIT(s.tag, 54, 960)}px;font-weight:900;color:${GOLD};white-space:nowrap">${esc(s.tag)}</span></div>`; }
    if (s.stamp) { const q = AT(s, s.stampAt, .5, 0), pop = q >= 1 ? 1 : L(1.5, 1, e4(q));
      h += `<div class="ab" style="left:0;right:0;top:1160px;text-align:center;opacity:${c01(q * 2).toFixed(3)}"><span style="display:inline-block;padding:12px 36px;border:5px solid ${REDC};color:#FF9A90;font-size:62px;font-weight:900;white-space:nowrap;transform:rotate(-3deg) scale(${pop.toFixed(3)});background:rgba(224,103,95,.10)">${esc(s.stamp)}</span></div>`; }
    return h;
  };
  /* 세로 일정표: 왼쪽 세로 축이 다음 날짜까지 그어지고 점이 찍힌 뒤 날짜·내용이 올라옴. 아직 안 온 날짜는 빈 점만(빈 화면 ✗), 방금 칸은 금색 */
  R.v_tline = (lt, s) => {
    /* 11/10 17:21 사용자 "텍스트 간격·정렬 맞춰" → 칸마다 같은 높이 틀: 날짜(50) · 제목(86, 점과 같은 높이 가운데) · 보조(46) — 보조 글이 없어도 같은 칸, 칸 사이 간격 일정. 강조 틀은 글 위아래 같은 여백(20) */
    const its = s.items || [], n = its.length, X = 130, Y0 = 512, DY = 226, TX0 = X + 62;
    const qs = its.map(x => AT(s, x.at, .7, 0)), last = qs.reduce((m, q, i) => q > 0 ? i : m, -1);
    let h = `<div class="ab" style="left:${X - 2}px;top:${Y0}px;width:4px;height:${DY * (n - 1)}px;background:rgba(255,255,255,.10)"></div>`;
    let reach = 0; qs.forEach((q, i) => { if (q > 0) reach = i - 1 + Math.min(1, q * 1.6); });
    if (reach > 0) h += `<div class="ab" style="left:${X - 3}px;top:${Y0}px;width:6px;height:${(DY * reach).toFixed(1)}px;background:linear-gradient(180deg,${SOFT},${GOLD})"></div>`;
    its.forEach((it, i) => { const q = qs[i], y = Y0 + i * DY, cur = i === last, hi = !!it.hi && q > 0, dq = c01(q * 1.6 - .6), c = cur || hi ? GOLD : '#C9D3E2', dim = q > 0 && !cur && !hi ? .62 : 1;
      if (hi) { const gq = c01(q * 1.2 - .5), top = y - 113, bot = y + (it.s ? 113 : 63);
        h += `<div class="ab" style="left:${X + 34}px;top:${top}px;width:${1080 - X - 34 - 60}px;height:${bot - top}px;border-radius:32px;box-shadow:inset 0 0 0 3px rgba(200,226,255,${(.85 * gq).toFixed(3)});background:rgba(200,226,255,${(.07 * gq).toFixed(3)})"></div>`; }
      h += `<div class="ab" style="left:${X - 16}px;top:${y - 16}px;width:32px;height:32px;border-radius:50%;background:${INK0};box-shadow:0 0 0 4px rgba(255,255,255,.22)"></div>`;
      if (q > 0) h += `<div class="ab" style="left:${X - 20}px;top:${y - 20}px;width:40px;height:40px;border-radius:50%;background:${c};transform:scale(${(dq >= 1 ? 1 : L(.2, 1, e4(dq))).toFixed(3)});opacity:${c01(dq * 3).toFixed(3)};box-shadow:0 0 ${cur || hi ? 26 : 0}px rgba(200,226,255,.65)"></div>`;
      const tq = c01(q * 1.4 - .3), TW = 1080 - TX0 - 90;
      h += `<div class="ab" style="left:${TX0}px;top:${y - 93}px;width:${TW}px;height:50px;line-height:50px;font-size:42px;font-weight:700;color:${cur || hi ? GOLD : MU};white-space:nowrap;opacity:${dim};${up(tq, 18)}">${esc(it.d)}</div>
        <div class="ab" style="left:${TX0}px;top:${y - 43}px;width:${TW}px;height:86px;line-height:86px;font-size:${FIT(it.t, 74, TW)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap;opacity:${dim}">${MASK(esc(it.t), tq)}</div>`;
      if (it.s) h += `<div class="ab" style="left:${TX0}px;top:${y + 47}px;width:${TW}px;height:46px;line-height:46px;font-size:${FIT(it.s, 38, TW)}px;font-weight:700;color:${hi ? '#F4DFA8' : MU};white-space:nowrap;opacity:${dim};${up(c01(q * 1.2 - .45), 14)}">${esc(it.s)}</div>`; });
    return h;
  };
  /* 두 줄 두 칸 선수 카드: 칸 틀은 처음부터(흐리게), 이름을 부를 때 사진이 들어옴. 같은 묶음이면 그대로, 묶음이 바뀌면(포수 → 외야) 제목만 바뀌고 앞 카드는 0.2초에 빠진 뒤 새 카드 */
  R.v_grid = (lt, s) => {
    const cs = s.cards || [], P = s._prev && s._prev.type === 'v_grid' ? s._prev : null, CW2 = 465, CH2 = 380, GX = 30, GY = 26, Y = 490;   /* 11/10 17:21: 아래 칸과 자막(1345) 사이 70px 띄움 */
    let h = '';
    const sameT = !!(P && P.title === s.title), tq = sameT ? 1 : sg(lt, P ? .12 : 0, .8);
    if (P && P.title && !sameT) { const oq = c01(lt / .25); if (oq < 1) h += `<div class="ab" style="left:60px;top:${(400 - 24 * e4(oq)).toFixed(1)}px;opacity:${(1 - ss(oq)).toFixed(3)}"><span style="display:inline-block;padding:8px 26px;background:${GOLD};color:${INK0};font-size:52px;font-weight:900;transform:skewX(-10deg)">${esc(P.title)}</span></div>`; }
    h += `<div class="ab" style="left:60px;top:400px;opacity:${c01(tq * 2).toFixed(3)}"><span style="display:inline-block;padding:8px 26px;background:${GOLD};color:${INK0};font-size:52px;font-weight:900;transform:skewX(-10deg)">${tq >= 1 ? esc(s.title) : KIN(s.title, tq)}</span></div>`;
    cs.slice(0, 4).forEach((c, i) => { const x = 60 + (i % 2) * (CW2 + GX), y = Y + Math.floor(i / 2) * (CH2 + GY), pc = P && P.cards[i];
      const keep = !!(pc && sameT && pc.img === c.img && !(pc.at >= 50)), q = keep ? 1 : AT(s, c.at, .6, 0), oldOn = pc && !sameT && !(pc.at >= 50);
      h += `<div class="ab" style="left:${x}px;top:${y}px;width:${CW2}px;height:${CH2}px;border-radius:32px;background:rgba(255,255,255,.035);box-shadow:inset 0 0 0 2px rgba(255,255,255,.10)"></div>`;
      if (oldOn) { const oq = c01(lt / .2); if (oq < 1) h += `<div class="ab" style="left:${x}px;top:${y}px;width:${CW2}px;height:${CH2}px;border-radius:32px;overflow:hidden;opacity:${(1 - ss(oq)).toFixed(3)}">${PIC(pc.img, CW2, CH2, .5, 'filter:contrast(1.06)', pc.focus)}<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,16,24,.92),transparent 50%)"></div><div style="position:absolute;left:24px;bottom:16px;font-size:${FIT(pc.name, 70, 300)}px;font-weight:900;color:${TX};white-space:nowrap">${esc(pc.name)}</div></div>`; }
      if (q > 0) h += `<div class="ab" style="left:${x}px;top:${(y + (1 - e4(q)) * 24).toFixed(1)}px;width:${CW2}px;height:${CH2}px;border-radius:32px;overflow:hidden;opacity:${c01(q * 2).toFixed(3)};box-shadow:0 20px 44px rgba(0,0,0,.4)">${PIC(c.img, CW2, CH2, .5, 'filter:contrast(1.06)', c.focus)}<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(11,16,24,.94),transparent 52%)"></div>
          <div style="position:absolute;right:16px;top:14px">${LG(c.team, 74)}</div><div style="position:absolute;left:24px;right:16px;bottom:16px;font-size:${FIT(c.name, 74, CW2 - 60)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${q >= 1 || keep ? esc(c.name) : KIN(c.name, c01(q * 1.3 - .3))}</div></div>`;
      if (c.tag && q > 0) { const gq = AT(s, c.tagAt, .5, 0), pop = gq >= 1 ? 1 : L(1.4, 1, e4(gq));
        h += `<div class="ab" style="left:${x + 14}px;top:${y + 16}px;opacity:${c01(gq * 2).toFixed(3)};transform-origin:left top;transform:rotate(-4deg) scale(${pop.toFixed(3)})"><span style="display:inline-block;padding:8px 18px;background:${REDC};color:#fff;font-size:34px;font-weight:900;white-space:nowrap">${esc(c.tag)}</span></div>`; } });
    return h;
  };
  /* 12월 달력(새 모션): 칸이 차례로 깔리고, 말하는 날짜에 원이 그려지며 아래 설명 띠가 바뀜. 앞에서 표시한 날짜는 그대로 */
  R.v_cal = (lt, s) => {
    const P = s._prev && s._prev.type === 'v_cal' ? s._prev : null, first = 2, days = 31, CWc = 132, CHc = 108, X0 = 78, Y0 = 500, gq = P ? 1 : sg(lt, 0, .8);
    let h = `<div class="ab" style="left:0;right:0;top:395px;text-align:center;font-size:58px;font-weight:900;color:${TX};${op(P ? 1 : sg(lt, 0, .6))}">${esc(s.month || '')}</div>`;
    '일월화수목금토'.split('').forEach((d, i) => { h += `<div class="ab" style="left:${X0 + i * CWc}px;top:${Y0 - 20}px;width:${CWc}px;text-align:center;font-size:32px;font-weight:700;color:${i === 0 ? '#E58C86' : MU};${op(gq)}">${d}</div>`; });
    const mk = {}; (s.marks || []).forEach(m => { mk[m.day] = m; });
    for (let d = 1; d <= days; d++) { const idx = first + d - 1, col = idx % 7, row = Math.floor(idx / 7), x = X0 + col * CWc, y = Y0 + 34 + row * CHc, cq = P ? 1 : c01(gq * 1.6 - (idx / 35) * .6);
      const m = mk[d], mq = m ? AT(s, m.at, .6, 0) : 0, mc = m && m.c === 'red' ? REDC : GOLD;
      h += `<div class="ab" style="left:${x + 4}px;top:${y + 4}px;width:${CWc - 8}px;height:${CHc - 8}px;border-radius:34px;background:rgba(255,255,255,${m && mq > 0 ? (.04 + .1 * mq).toFixed(3) : '.035'});opacity:${c01(cq * 2).toFixed(3)}"></div>
        <div class="ab" style="left:${x}px;top:${y + 22}px;width:${CWc}px;text-align:center;font-size:44px;font-weight:${m && mq > 0 ? 900 : 700};color:${m && mq > 0 ? mc : col === 0 ? '#E58C86' : '#D6DDE8'};opacity:${c01(cq * 2).toFixed(3)}">${d}</div>`;
      if (m && mq > 0) { const C2 = 2 * Math.PI * 52;
        h += `<svg class="ab" style="left:${x + CWc / 2 - 58}px;top:${y + CHc / 2 - 58}px;overflow:visible" width="116" height="116"><circle cx="58" cy="58" r="52" fill="none" stroke="${mc}" stroke-width="7" stroke-linecap="round" stroke-dasharray="${C2.toFixed(1)}" stroke-dashoffset="${(C2 * (1 - e4(mq))).toFixed(1)}" transform="rotate(-90 58 58)"/></svg>`; } }
    /* 아래 설명 띠: 지금 줄에서 새로 표시하는 날짜의 설명(앞 띠는 위로 빠짐) */
    const cur = (s.marks || []).filter(m => m.at != null && m.at >= 0 && m.at < 50).pop(), prv = P ? (P.marks || []).filter(m => m.at != null && m.at < 50).pop() : null, BY = 1150;
    if (prv && cur && prv.day !== cur.day) { const oq = c01(lt / .25); if (oq < 1) h += band(prv, BY - 24 * e4(oq), 1 - ss(oq), 1); }
    if (cur) h += band(cur, BY, 1, AT(s, cur.at, .6, 0), AT(s, cur.sAt, .5, 0));
    return h;
    function band(m, y, o, q, sq = 1) { const mc = m.c === 'red' ? REDC : GOLD, hasImg = !!m.img, IW = 150;
      return `<div class="ab" style="left:60px;top:${y.toFixed(1)}px;width:960px;height:170px;border-radius:34px;${GLASS};box-shadow:inset 0 0 0 2px ${mc}55;opacity:${(o * c01(q * 2)).toFixed(3)};overflow:hidden">
        ${hasImg ? `<div style="position:absolute;left:12px;top:10px;width:${IW}px;height:${IW}px;border-radius:50%;overflow:hidden">${PIC(m.img, IW, IW, .5, '')}</div>` : `<div style="position:absolute;left:0;top:0;bottom:0;width:12px;background:${mc}"></div>`}
        <div style="position:absolute;left:${hasImg ? IW + 40 : 44}px;right:20px;top:24px;font-size:${FIT(m.lab, 60, hasImg ? 740 : 860)}px;font-weight:900;color:${mc === GOLD ? GOLD : '#FF9A90'};white-space:nowrap">${MASK(esc(m.lab), c01(q * 1.3 - .2))}</div>
        <div style="position:absolute;left:${hasImg ? IW + 40 : 44}px;right:20px;top:100px;font-size:${FIT(m.sub || '', 42, hasImg ? 740 : 860)}px;font-weight:700;color:${TX};white-space:nowrap;${up(sq, 14)}">${esc(m.sub || '')}</div></div>`; }
  };
  /* 마지막 질문: 큰 두 줄 + 10구단 로고 다섯 칸 두 줄 */
  R.v_q = (lt, s) => {
    const P = s._prev && s._prev.type === 'v_q' ? s._prev : null, tx = s.text || [];
    let h = '';
    tx.forEach((t, i) => { const q = P ? 1 : sg(lt, i * .25, .9);
      h += `<div class="ab" style="left:0;right:0;top:${430 + i * 135}px;text-align:center;font-size:${FIT(t, 104, 960)}px;font-weight:900;letter-spacing:-3px;color:${i ? GOLD : TX};white-space:nowrap">${q >= 1 ? esc(t) : KIN(t, q)}</div>`; });
    const TEAMS = ['삼성', 'LG', '한화', 'SSG', 'KT', '롯데', 'NC', 'KIA', '두산', '키움'];
    TEAMS.forEach((tm, i) => { const q = P ? 1 : c01(sg(lt, .5 + i * .06, .6)), x = 93 + (i % 5) * 186, y = 820 + Math.floor(i / 5) * 210;
      h += `<div class="ab" style="left:${x}px;top:${(y + (1 - e4(q)) * 20).toFixed(1)}px;width:150px;height:150px;border-radius:38px;background:rgba(255,255,255,.06);display:flex;align-items:center;justify-content:center;opacity:${c01(q * 2).toFixed(3)}">${LG(tm, 118)}</div>`; });
    return h;
  };


  /* ═════ 11/13 「2027 FA 공시 총정리」 — 가로 장면 3종 (새 모션: 스코어보드 글자 넘김) ═════ */
  const GCOL = { A: '#9BE8FF', B: '#B7A6FF', C: '#C5CEE6', '?': '#7A8597' };
  const FLAPPOOL = '가나다라마바사아자차카타파하FAKBO0123456789';
  /* 스코어보드 넘김: 글자 칸마다 3~4번 넘어가다 제 글자에 멈춤(칸 가운데 가는 줄 = 넘김판) */
  function flap(txt, q, fs, col = TX, seed = 0, tile = true, always = false) {
    const POOL = /^\d+$/.test(String(txt || '')) ? '0123456789' : FLAPPOOL;
    const a = [...String(txt || '')], n = a.length, tw = Math.round(fs * .98), th = Math.round(fs * 1.28);
    return `<span style="display:inline-flex;gap:${Math.round(fs * .08)}px;vertical-align:middle">` + a.map((ch, i) => {
      if (ch === ' ') return `<span style="display:inline-block;width:${Math.round(fs * .34)}px"></span>`;
      const p = c01(q * (1 + n * .18) - i * .18), done = p >= 1, k = Math.floor(p * 4), fr = p * 4 - k;
      const show = done ? ch : POOL[(k * 7 + i * 5 + seed * 3) % POOL.length], sy = done ? 1 : Math.max(.12, Math.abs(Math.cos(Math.PI * fr)));
      const vis = p > 0 || always ? 1 : 0;
      return `<span style="position:relative;display:inline-flex;align-items:center;justify-content:center;width:${tw}px;height:${th}px;${tile ? `background:linear-gradient(180deg,#1B2331 0 49%,#141B27 51% 100%);border-radius:${Math.round(fs * .12)}px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.06)` : ''};opacity:${vis}">`
        + `<span style="display:inline-block;transform:scaleY(${sy.toFixed(3)});font-size:${fs}px;font-weight:900;color:${done ? col : 'rgba(242,244,248,.55)'};line-height:1">${esc(show)}</span>`
        + (tile ? `<span style="position:absolute;left:0;right:0;top:50%;height:2px;margin-top:-1px;background:rgba(0,0,0,.55)"></span>` : '') + `</span>`;
    }).join('') + `</span>`;
  }
  const gradeBadge = (g, q, sz = 70) => `<div style="width:${sz}px;height:${sz}px;border-radius:36px;display:flex;align-items:center;justify-content:center;background:${g === 'A' ? HOLO : (GCOL[g] || GCOL['?'])};color:${INK0};font-size:${Math.round(sz * .62)}px;font-weight:900;position:relative;overflow:hidden;transform-origin:50% 100%;transform:${SQ(q)};opacity:${c01(q * 2.5).toFixed(3)}">${esc(g)}${g === 'A' ? SHEEN(q) : ''}</div>`;
  /* 오프닝: 큰 숫자(넘김판) + 등급 막대 + 오른쪽 두 사람 */
  R.fa_count = (lt, s) => {
    const P = s._prev && s._prev.type === 'fa_count' ? s._prev : null, nq = AT(s, s.nAt != null ? s.nAt : 0, 1.4, 0);
    let h = `<div class="ab" style="left:110px;top:170px;${op(P || s._k === 0 ? 1 : sg(lt, 0, .5))}"><div style="width:90px;height:5px;background:${GOLD};margin-bottom:16px"></div><div style="font-size:46px;font-weight:800;color:${MU};white-space:nowrap">${esc(s.label || '')}</div></div>`;
    h += `<div class="ab" style="left:104px;top:270px;display:flex;align-items:flex-end;gap:18px">${flap(String(s.n), nq, 170, GOLD, 1, true, true)}<span style="font-size:120px;font-weight:900;color:${TX};line-height:1;margin-bottom:22px;opacity:${c01(nq * 1.5 - .5).toFixed(3)}">명</span></div>`;
    const gs = s.grades || [], tot = gs.reduce((m, x) => m + x.n, 0) || 1, BW = 760, gq = AT(s, s.gradesAt, 1.0, 0);
    if (gq > 0) { let x = 110;
      h += `<div class="ab" style="left:110px;top:560px;width:${BW}px;height:64px;border-radius:34px;background:rgba(255,255,255,.05)"></div>`;
      gs.forEach((g, i) => { const w = BW * g.n / tot, q = c01(gq * 1.6 - i * .3);
        h += `<div class="ab" style="left:${x}px;top:560px;width:${(w * e4(q)).toFixed(1)}px;height:64px;background:${GCOL[g.g]};${i === 0 ? 'border-radius:34px 0 0 12px;' : ''}${i === gs.length - 1 ? 'border-radius:0 12px 12px 0;' : ''}"></div>
          <div class="ab" style="left:${110 + i * 260}px;width:250px;top:644px;${up(c01(q * 1.5 - .3), 16)}"><div style="font-size:44px;font-weight:900;color:${GCOL[g.g]};white-space:nowrap">${g.g}등급 ${g.n}명</div></div>`;
        x += w; }); }
    const fq = AT(s, s.facesAt, .7, 0);
    (s.faces || []).forEach((f, i) => { const q = c01(fq * 1.3 - i * .25), x = 1040 + i * 400, W = 370, H = 520;
      if (q > 0) h += `<div class="ab" style="left:${x}px;top:${(190 + (1 - e4(q)) * 30).toFixed(1)}px;width:${W}px;height:${H}px;border-radius:32px;overflow:hidden;opacity:${c01(q * 2).toFixed(3)};box-shadow:0 24px 56px rgba(0,0,0,.45)">${PIC(f.img, W, H, .5, 'filter:contrast(1.05)', f.focus)}${DOTS}<div style="position:absolute;inset:0;background:linear-gradient(0deg,rgba(7,10,20,.92),transparent 45%)"></div><div style="position:absolute;left:24px;bottom:18px;font-size:72px;font-weight:900;color:${TX};letter-spacing:-2px">${esc(f.name)}</div></div>`; });
    if (s.pred) h += `<div class="ab" style="right:60px;top:60px;padding:8px 16px;border:3px solid ${REDC};color:#FF9A90;font-size:28px;font-weight:900">예상 명단 · 미리보기</div>`;
    return h;
  };
  /* 등급표: A·B·C 카드 세 장, 말하는 카드만 밝게 */
  R.fa_grade = (lt, s) => {
    const cs = s.cards || [], W = 540, G = 30, X0 = (1920 - (W * 3 + G * 2)) / 2, Y = 170, H = 610;
    const Pg = s._prev && s._prev.type === 'fa_grade' ? s._prev : null, hq = Pg && Pg.hi !== s.hi ? ss(c01(lt / .35)) : 1;
    const onOf = (hi, i) => hi == null || hi < 0 || hi === i ? 1 : .42;
    /* 11/14 사용자 "텍스트만 있어서 눈에 안 들어온다 — 텍스트+그림으로": 기준은 순위 띠(세 등급 구간 가운데 내 구간에 불), 보상은 선수 그림 + 돈 막대(길이 = 연봉의 몇 %) */
    const GRAPH = (c, col) => { const cq = AT(s, c.critAt, .6, 0), pq = AT(s, c.compAt, .8, 0), IW = W - 68;
      const zrow = (lab, val, y, j) => { const qq = c01(cq * 1.4 - j * .3);
        return `<div style="position:absolute;left:34px;top:${y}px;width:${IW}px;height:46px;display:flex;align-items:center;${op(c01(qq * 2))}"><div style="width:106px;font-size:26px;font-weight:700;color:${MU};white-space:nowrap">${lab}</div><div style="display:flex;gap:5px;width:186px;height:22px">${[0, 1, 2].map(z => `<div style="flex:${[3, 3, 4][z]};border-radius:6px;background:rgba(255,255,255,.10);position:relative;overflow:hidden">${z === c.zone ? `<div style="position:absolute;inset:0;border-radius:6px;background:${col};transform-origin:left;transform:scaleX(${e4(qq).toFixed(3)})"></div>` : ''}</div>`).join('')}</div><div style="margin-left:18px;font-size:${FIT(val, 36, 160)}px;font-weight:900;color:${TX};white-space:nowrap">${esc(val)}</div></div>`; };
      const man = no => `<svg width="64" height="64" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="rgba(255,255,255,.07)" stroke="${no ? 'rgba(255,255,255,.28)' : col}" stroke-width="2.5"/><circle cx="32" cy="25" r="9" fill="${no ? 'rgba(255,255,255,.32)' : col}"/><path d="M14 53c2-12 9-17 18-17s16 5 18 17z" fill="${no ? 'rgba(255,255,255,.32)' : col}"/>${no ? '<line x1="13" y1="51" x2="51" y2="13" stroke="#FF7A70" stroke-width="5" stroke-linecap="round"/>' : ''}</svg>`;
      const bar = (pct, y, j, lab) => { const qq = c01(pq * 1.6 - j * .4), w = pct * e4(qq);
        return `<div style="position:absolute;left:34px;top:${y}px;height:46px;width:${Math.max(0, w).toFixed(1)}px;border-radius:23px;background:linear-gradient(90deg,${col}66,${col});${op(c01(qq * 4))}"></div><div style="position:absolute;left:${(34 + w + 14).toFixed(1)}px;top:${y}px;height:46px;display:flex;align-items:center;font-size:32px;font-weight:900;color:${TX};white-space:nowrap;${op(c01(qq * 2 - .5))}">${esc(lab)}</div>`; };
      const mq = c01(pq * 1.6);
      return `<div style="position:absolute;left:34px;top:148px;font-size:26px;font-weight:700;color:${MU}">기준 · 연봉 순위</div>
        ${zrow('팀 안', c.team || '', 186, 0)}${zrow('리그', c.lg || '', 238, 1)}
        ${c.extra ? `<div style="position:absolute;left:34px;right:20px;top:290px;font-size:${FIT(c.extra, 24, IW)}px;font-weight:700;color:${MU};white-space:nowrap;${op(c01(cq * 1.4 - .6))}">${esc(c.extra)}</div>` : ''}
        <div style="position:absolute;left:34px;right:34px;top:330px;height:2px;background:rgba(255,255,255,.1)"></div>
        <div style="position:absolute;left:34px;top:346px;font-size:26px;font-weight:700;color:${MU}">영입하는 팀이 내는 보상</div>
        <div style="position:absolute;left:34px;top:388px;display:flex;align-items:center;gap:18px;${up(mq, 14)}">${man(!c.prot)}<div><div style="font-size:34px;font-weight:900;color:${c.prot ? col : TX};white-space:nowrap">${c.prot ? '보상선수 1명' : '보상선수 없음'}</div>${c.prot ? `<div style="font-size:24px;font-weight:700;color:${MU};white-space:nowrap">${esc(c.prot)}</div>` : ''}</div></div>
        ${bar(c.p1, 470, 1, (c.prot ? '+ ' : '') + '연봉 ' + c.p1 + '%')}
        ${c.p2 ? `<div style="position:absolute;left:34px;top:521px;font-size:24px;font-weight:700;color:${MU};${op(c01(pq * 1.6 - .7))}">또는 선수 없이</div>${bar(c.p2, 552, 2, '연봉 ' + c.p2 + '%')}` : ''}`; };
    let h = '';
    cs.forEach((c, i) => { const q = AT(s, c.at, .7, 0), x = X0 + i * (W + G), dim = Pg ? L(onOf(Pg.hi, i), onOf(s.hi, i), hq) : onOf(s.hi, i), col = GCOL[c.g];
      const bw = Pg ? L(Pg.hi === i ? 1 : 0, s.hi === i ? 1 : 0, hq) : (s.hi === i ? 1 : 0);
      if (q <= 0) return;
      h += `<div class="ab" style="left:${x}px;top:${(Y + (1 - e4(q)) * 28).toFixed(1)}px;width:${W}px;height:${H}px;border-radius:36px;${GLASS};box-shadow:inset 0 0 0 ${(1 + 2 * bw).toFixed(2)}px ${bw > .02 ? col + Math.round(255 * Math.max(.08, bw)).toString(16).padStart(2, '0') : 'rgba(255,255,255,.08)'}${bw > .02 ? `,0 0 40px ${col}${Math.round(51 * bw).toString(16).padStart(2, '0')}` : ''};opacity:${(c01(q * 2) * dim).toFixed(3)}">
        <div style="position:absolute;left:34px;top:26px;display:flex;align-items:center;gap:20px">${gradeBadge(c.g, 1, 96)}<div style="font-size:60px;font-weight:900;color:${TX}">${esc(c.head)}</div></div>
        ${c.zone != null ? GRAPH(c, col) : `<div style="position:absolute;left:34px;right:30px;top:160px;font-size:28px;font-weight:700;color:${MU}">기준</div>
        ${(c.crit || []).map((t, j) => { const cq = AT(s, c.critAt, .55, 0); const qq = c01(cq * 1.4 - j * .3); return `<div style="position:absolute;left:34px;right:20px;top:${200 + j * 58}px;font-size:${FIT(t, 40, W - 60)}px;font-weight:800;color:${TX};white-space:nowrap;${up(qq, 14)}">${esc(t)}</div>`; }).join('')}
        <div style="position:absolute;left:34px;right:34px;top:330px;height:2px;background:rgba(255,255,255,.1)"></div>
        <div style="position:absolute;left:34px;top:352px;font-size:28px;font-weight:700;color:${MU}">영입하는 팀이 내는 보상</div>
        ${(c.comp || []).map((t, j) => { const cq = AT(s, c.compAt, .55, 0); const qq = c01(cq * 1.4 - j * .3); return `<div style="position:absolute;left:34px;right:20px;top:${394 + j * 62}px;font-size:${FIT(t, 40, W - 60)}px;font-weight:900;color:${j === 0 ? col : TX};white-space:nowrap;${up(qq, 14)}">${esc(t)}</div>`; }).join('')}`}
      </div>`; });
    const nq = AT(s, s.noteAt, .5, 0);
    if (s.note && nq > 0) h += `<div class="ab" style="left:0;right:0;top:812px;text-align:center;${up(nq, 14)}"><span style="font-size:36px;font-weight:800;color:${GOLD}">${esc(s.note)}</span></div>`;
    return h;
  };
  /* 말 카드(사진이 없는 감독·단장): 왼쪽 팀 로고 + 이름, 오른쪽 큰 따옴말 — 다른 사람 사진을 쓰지 않으려고 */
  R.fa_quote = (lt, s) => {
    const q0 = sg(lt, 0, .6), bq = AT(s, s.at, .8, 0), noPic = !s.img && !s.team && !s.mono;   /* 11/12 검수: 사진·로고가 없는 사람(익명 단장)은 지어낸 글자 원 ✗ → 원 없이 이름만 */
    let h = (noPic ? '' : `<div class="ab" style="left:${360 - 150}px;top:${(200 + (1 - e4(q0)) * 20).toFixed(1)}px;opacity:${c01(q0 * 2).toFixed(3)}">${s.img ? `<div style="width:300px;height:300px;border-radius:50%;overflow:hidden">${PIC(s.img, 300, 300, .5, '')}</div>` : s.team ? LG(s.team, 300) : `<div style="width:300px;height:300px;border-radius:50%;background:linear-gradient(135deg,#1A2433,#0E1520);box-shadow:inset 0 0 0 3px rgba(200,226,255,.5);display:flex;align-items:center;justify-content:center;font-size:${FIT(s.mono || '', 110, 220)}px;font-weight:900;color:${GOLD};letter-spacing:-2px">${esc(s.mono || '')}</div>`}</div>`) + `
      <div class="ab" style="left:100px;top:${noPic ? 330 : 540}px;width:520px;text-align:center;${op(q0)}"><div style="font-size:${FIT(s.name, 76, 520)}px;font-weight:900;color:${TX};letter-spacing:-2px;white-space:nowrap">${esc(s.name)}</div><div style="margin-top:8px;font-size:34px;font-weight:700;color:${MU};white-space:nowrap">${esc(s.role || '')}</div></div>`;
    const t = s.text || '', fs = Math.min(64, FIT(t, 64, 2 * 960, 40));
    h += `<div class="ab" style="left:720px;top:${(250 + (1 - e4(bq)) * 24).toFixed(1)}px;width:1100px;min-height:300px;border-radius:40px;${GLASS};opacity:${c01(bq * 2).toFixed(3)};display:flex;flex-direction:column;justify-content:center;padding:36px 54px;box-sizing:border-box"><svg style="position:absolute;left:0;top:0;width:100%;height:100%;overflow:visible"><rect pathLength="1" rx="26" style="x:1px;y:1px;width:calc(100% - 2px);height:calc(100% - 2px);fill:none;stroke:rgba(200,226,255,.7);stroke-width:2.5;stroke-dasharray:1;stroke-dashoffset:${(1 - eio(bq)).toFixed(4)}"/></svg>
      <div style="font-size:30px;font-weight:800;color:${GOLD}">${esc(s.date || '')}</div>
      <div style="margin-top:10px;font-size:${fs}px;font-weight:900;color:${TX};line-height:1.32;word-break:keep-all;text-wrap:balance;padding-left:.47em;text-indent:-.47em"><span style="color:${GOLD}">“</span>${esc(t)}<span style="color:${GOLD}">”</span></div></div>`;
    return h;
  };
  /* 팬 반응 말풍선 피드(새 모션): 팀 로고 + '팬 반응' 제목, 말풍선이 차례로 톡 올라와 쌓임(앞 말풍선은 그대로) */
  R.fa_fans = (lt, s) => {
    /* 11/13 00:53 사용자 "말풍선이 나올 때마다 팬 반응이 깜빡깜빡" → 앞 장면도 같은 팀 팬 반응이면 머리(로고·제목)는 그대로 */
    const PF = !!(s._prev && s._prev.type === 'fa_fans' && s._prev.team === s.team && (s._prev.title || '') === (s.title || ''));
    const bs = s.bubbles || [], q0 = PF ? 1 : sg(lt, 0, .5);
    let h = `<div class="ab" style="left:100px;top:${(160 + (1 - e4(q0)) * 16).toFixed(1)}px;display:flex;align-items:center;gap:22px;opacity:${c01(q0 * 2).toFixed(3)}">${LG(s.team, 120)}<div><div style="font-size:30px;font-weight:700;color:${MU}">${esc(s.sub || '')}</div><div style="font-size:64px;font-weight:900;color:${TX};letter-spacing:-2px">${esc(s.title || '팬 반응')}</div></div></div>`;
    bs.forEach((b, i) => { const q = AT(s, b.at, .55, 0); if (q <= 0) return;
      const right = i % 2 === 1, y = 360 + i * 175, col = b.c === 'bad' ? '#F3D9D2' : '#F1ECDF', rot = (right ? 1.2 : -1.2) + (1 - e4(q)) * (right ? 5 : -5);
      h += `<div class="ab" style="${right ? 'right:120px' : 'left:120px'};top:${(y + (1 - e4(q)) * 26).toFixed(1)}px;max-width:1300px;opacity:${c01(q * 2).toFixed(3)};transform-origin:${right ? 'right' : 'left'} bottom;transform:rotate(${rot.toFixed(2)}deg) ${SQ(q)}">
        <div style="position:relative;padding:22px 34px;border-radius:30px;${right ? 'border-bottom-right-radius:8px' : 'border-bottom-left-radius:8px'};background:${col};box-shadow:7px 9px 0 rgba(0,0,0,.42),inset 0 -3px 0 rgba(0,0,0,.08);font-size:${FIT(b.t, 60, 1220, 34)}px;font-weight:900;color:${b.c === 'bad' ? '#7A1F18' : '#151C28'};white-space:nowrap">${esc(b.t)}</div></div>`; });
    return h;
  };
  /* 구단 명단판: 왼쪽 = 로고·팀·남은 돈, 오른쪽 = 넘김판 줄(사진 · 이름 · 포지션 · 구분 · 등급) */
  R.fa_board = (lt, s) => {
    const rows = s.rows || [], n = rows.length, P = s._prev && s._prev.type === 'fa_board' && s._prev.team === s.team && s._prev.title === s.title ? s._prev : null;
    let h = '';
    /* 왼쪽 */
    h += HALF(60, 110, 600, 440, P ? 1 : sg(lt, 0, .8));
    if (s.pos) {
      h += `<div class="ab" style="left:100px;top:300px;width:520px;text-align:center;${op(P ? 1 : sg(lt, 0, .5))}"><div style="font-size:${FIT(s.title, 110, 520)}px;font-weight:900;color:${TX};letter-spacing:-3px">${esc(s.title)}</div><div style="margin:18px auto 0;width:120px;height:6px;background:${GOLD}"></div></div>`;
    } else {
      const lq = P ? 1 : sg(lt, 0, .6);
      const KN_ = s.kn || (s.team === 'KIA' ? '기아' : s.team);
      h += `<div class="ab" style="left:100px;top:${(140 + (1 - e4(lq)) * 20).toFixed(1)}px;width:560px;opacity:${c01(lq * 2).toFixed(3)}"><div style="display:flex;align-items:center;gap:16px">${LG(s.team, 78)}<div style="font-size:${FIT(s.title, 32, 440)}px;font-weight:700;color:${MU};white-space:nowrap">${esc(s.title)}</div></div><div style="margin-top:2px;font-size:${FIT(KN_, 200, 540)}px;font-weight:900;letter-spacing:-.045em;line-height:1.08;color:${TX};white-space:nowrap">${esc(KN_)}</div></div>`;
    }
    if (s.room) { const rq = AT(s, s.room.at, .9, 0), Pr = P && P.room;
      if (rq > 0 || Pr) h += `<div class="ab" style="left:100px;top:470px;width:520px;height:200px;overflow:hidden;border-radius:34px;${GLASS};box-shadow:inset 0 0 0 2px rgba(200,226,255,.35);${Pr ? '' : up(rq, 20)}">
          ${s.room.v ? LIQ(520, 200, .16 + .7 * c01(s.room.v / 110), Pr ? 1 : rq) : ''}<div style="position:absolute;left:36px;top:26px;font-size:30px;font-weight:700;color:${MU}">2027년 남은 돈</div>
          <div style="position:absolute;left:34px;top:66px;font-size:${FIT(s.room.txt, 96, 460, 48)}px;font-weight:900;letter-spacing:-.03em;white-space:nowrap"><span style="display:inline-block;${HOLOT};opacity:${(Pr ? 1 : ss(rq * 1.3)).toFixed(3)};transform:translateY(${(Pr ? 0 : (1 - e4(rq)) * 18).toFixed(1)}px)">${esc(s.room.txt)}</span></div></div>`;
      if (s.room.alt) { const aq = AT(s, s.room.alt.at, .6, 0); if (aq > 0) h += `<div class="ab" style="left:100px;top:690px;width:520px;text-align:left;${up(aq, 14)}"><span style="display:inline-block;padding:8px 20px;background:rgba(200,226,255,.14);box-shadow:inset 0 0 0 2px ${GOLD};color:${GOLD};font-size:${FIT(s.room.alt.txt, 34, 440)}px;font-weight:900;white-space:nowrap;${GLI(aq)}">${esc(s.room.alt.txt)}</span></div>`; }
      if (s.floor) { const fq = AT(s, s.floor.at, .6, 0); if (fq > 0) h += `<div class="ab" style="left:100px;top:690px;width:520px;text-align:left;${up(fq, 14)}"><span style="display:inline-block;padding:8px 18px;border:3px solid ${REDC};color:#FF9A90;font-size:${FIT(s.floor.txt + ' · 모자란 돈의 30% 납부', 34, 430)}px;font-weight:900;white-space:nowrap">${esc(s.floor.txt)} · 모자란 돈의 30% 납부</span></div>`; }
    }
    if (s.verdict) { const vq = AT(s, s.verdictAt, .55, 0); if (vq > 0) { const pop = vq >= 1 ? 1 : L(1.35, 1, e4(vq));
      h += `<div class="ab" style="left:100px;top:${s.floor || (s.room && s.room.alt) ? 762 : 700}px;width:520px;text-align:left;opacity:${c01(vq * 2).toFixed(3)}"><span style="display:inline-block;padding:12px 26px;background:${GOLD};color:${INK0};font-size:${FIT(s.verdict, 42, 470)}px;font-weight:900;white-space:nowrap;position:relative;overflow:hidden;border-radius:14px;transform-origin:0 100%;transform:${SQ(vq)}">${esc(s.verdict)}${SHEEN(vq)}</span></div>`; } }
    if (s.tag) { const tq = AT(s, s.tagAt, .5, 0); if (tq > 0) h += `<div class="ab" style="left:${s.tagPos === 'right' ? 700 : 100}px;top:${s.tagY || (s.tagPos === 'right' ? 660 : s.room ? 762 : 470)}px;width:${s.tagPos === 'right' ? 1120 : 520}px;text-align:left;${up(tq, 16)}"><span style="display:inline-block;padding:10px 26px;background:${GOLD};color:${INK0};font-size:44px;font-weight:900">${esc(s.tag)}</span></div>`; }
    /* 오른쪽 넘김판 */
    const BX = 700, BW = 1120, TOP = 150, AV = 660, rh = Math.min(132, Math.floor((AV - 54) / Math.max(1, n))), fs = Math.min(56, Math.round(rh * .44));
    if (!n) { h += `<div class="ab" style="left:${BX}px;top:380px;width:${BW}px;text-align:center;${op(sg(lt, .2, .6))}"><span style="font-size:72px;font-weight:900;color:${MU}">FA 자격 선수 없음</span></div>`; return h; }
    const PV0 = s._k > 0 ? SC[s._k - 1] : null, hq = P || (PV0 && PV0.type === 'fa_board' && !!PV0.pos === !!s.pos && (PV0.rows || []).length) ? 1 : sg(lt, 0, .5);   /* 11/14: 앞 장면도 명단판이면(팀이 달라도) 머리줄은 그대로 */
    h += `<div class="ab" style="left:${BX}px;top:${TOP}px;width:${BW}px;height:44px;display:flex;align-items:center;font-size:28px;font-weight:700;color:${MU};${op(hq)}"><span style="width:${BW - (s.pos ? 320 : 360)}px;padding-left:${rh + 30}px">선수</span>${s.pos ? '<span style="width:200px">소속</span>' : '<span style="width:240px">포지션</span>'}<span style="width:120px;text-align:center">등급${s.pred ? ' <span style="color:#FF9A90;font-size:22px">예상</span>' : ''}</span></div>`;
    h += `<div class="ab" style="left:${BX}px;top:${TOP + 46}px;width:${(BW * eio(hq)).toFixed(1)}px;height:2px;background:linear-gradient(90deg,${GOLD},rgba(200,226,255,.15))"></div>`;   /* 라인 애니메이션 */
    const Pb = s._prev && s._prev.type === 'fa_board' && s._prev.team === s.team ? s._prev : null, offq = 1 - ss(c01(lt / .35));
    const anyHl = (s.hl || []).length && AT(s, s.hlAt, .5, 0) > 0;
    rows.forEach((r, i) => { const q = AT(s, r.at, 1.0, 0), y = TOP + 54 + i * rh, hl0 = (s.hl || []).includes(r.name), was = !!(Pb && (Pb.hl || []).includes(r.name)), hq2 = hl0 ? (was && Pb.hlAt != null ? 1 : AT(s, s.hlAt, .5, 0)) : (was ? offq : 0), hl = hq2 > 0;
      const dim = anyHl && !hl && (s.hl || []).length < n ? .55 : 1, face = rh - 26;
      h += `<div class="ab" style="left:${BX}px;top:${y}px;width:${BW}px;height:${rh - 12}px;border-radius:36px;${GLASS};box-shadow:inset 0 0 0 ${hl && hq2 > 0 ? 2 : 1}px ${hl && hq2 > 0 ? `rgba(200,226,255,${(.8 * hq2).toFixed(3)})` : 'rgba(255,255,255,.06)'};opacity:${(c01(q * 3) * dim).toFixed(3)}">
        <div style="position:absolute;left:14px;top:${(rh - 12 - face) / 2}px;width:${face}px;height:${face}px;border-radius:50%;overflow:hidden;background:#1A2433">${r.img ? PIC(r.img, face, face, .5, '') : `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center">${LG(r.team || s.team, Math.round(face * .78))}</div>`}</div>
        <div style="position:absolute;left:${face + 34}px;top:0;bottom:0;display:flex;align-items:center">${flap(r.name, q, fs, TX, i)}</div>
        ${s.pos ? '' : `<div style="position:absolute;left:${BW - 360}px;top:0;bottom:0;display:flex;align-items:center;font-size:${Math.round(fs * .7)}px;font-weight:800;color:${TX};${op(c01(q * 1.6 - .5))}">${esc(r.pos)}</div>`}
        <div style="position:absolute;left:${BW - 320}px;top:0;bottom:0;display:flex;align-items:center;gap:10px;font-size:${Math.round(fs * (s.pos ? .7 : .62))}px;font-weight:${s.pos ? 800 : 700};color:${s.pos ? TX : MU};${op(c01(q * 1.6 - .6))}">${s.pos && r.team ? LG(r.team, Math.round(fs * .9)) : ''}${s.pos ? esc(r.kind || '') : ''}</div>
        <div style="position:absolute;left:${BW - 120 + (120 - Math.min(76, rh - 30)) / 2}px;top:${(rh - 12 - Math.min(76, rh - 30)) / 2}px">${gradeBadge(r.grade, c01(q * 1.5 - .7), Math.min(76, rh - 30))}</div>
      </div>`; });
    if (s.pred) h += `<div class="ab" style="right:60px;top:60px;padding:8px 16px;border:3px solid ${REDC};color:#FF9A90;font-size:28px;font-weight:900">예상 명단 · 미리보기</div>`;
    return h;
  };

  /* ── 11/12 MLB 직장폐쇄 편 새 모션 ── */
  /* lo_clock(새 모션): 하루 24시간 눈금자 — 시각마다 핀이 꽂히고, 두 시각 사이 띠가 차오르며 'N시간'이 0부터 올라간다 */
  R.lo_clock = (lt, s) => {
    const P = s._prev && s._prev.type === 'lo_clock' && s._prev._cid === s._cid ? s._prev : null;
    const X0 = 170, X1 = 1750, Y = 640, hx = h => X0 + (X1 - X0) * h / 24;
    const [ey, tt] = (() => { const p = String(s.title || '').split(' · '); return p.length > 1 ? [p[0], p.slice(1).join(' · ')] : ['', p[0]]; })();
    const pT = P ? String(P.title || '') : null, sameT = pT === String(s.title || '');
    let h = eyebrow(ey, P ? 1 : sg(lt, 0, .8), 120, 140);
    const tq = sameT ? 1 : sg(lt, 0, 1.0);
    h += `<div class="ab" style="left:116px;top:${ey ? 200 : 170}px;font-size:${FIT(tt, 84, 1600)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${tq >= 1 ? esc(tt) : KIN(tt, tq)}</div>`;
    const rq = P ? 1 : sg(lt, .1, .9);
    h += `<div class="ab" style="left:${X0}px;top:${Y - 3}px;width:${((X1 - X0) * e4(rq)).toFixed(1)}px;height:6px;border-radius:3px;background:rgba(255,255,255,.18)"></div>`;
    for (let i = 0; i <= 24; i++) { const x = hx(i), big = i % 6 === 0, q = c01(rq * 1.3 - i / 24 * .3);
      h += `<div class="ab" style="left:${x - 1.5}px;top:${Y + 10}px;width:3px;height:${big ? 26 : 14}px;background:rgba(255,255,255,${big ? .45 : .2});${op(q)}"></div>`;
      if (big) h += `<div class="ab" style="left:${x - 80}px;width:160px;top:${Y + 44}px;text-align:center;font-size:32px;font-weight:700;color:${MU};${op(q)}">${i === 12 ? '정오' : i === 24 ? '자정' : i + '시'}</div>`; }
    const colOf = c => c === 'bad' ? REDC : c === 'gold' ? GOLD : SOFT;
    const pm = x => P && (P.marks || []).find(y => y.lab === x.lab && !(y.at >= 50));
    (s.marks || []).forEach((m, i) => { const keep = !!pm(m), q = keep ? 1 : (m.at != null && m.at >= 50 ? 0 : AT(s, m.at, .7, 1)); if (q <= 0) return;
      const x = hx(m.h), c = colOf(m.c), up_ = i % 2 === 0, pinH = 150;
      h += `<div class="ab" style="left:${x - 3}px;top:${(Y - pinH * e4(q)).toFixed(1)}px;width:6px;height:${(pinH * e4(q)).toFixed(1)}px;background:${c};box-shadow:0 0 14px ${c}"></div>`;
      h += `<div class="ab" style="left:${x - 20}px;top:${Y - 20}px;width:40px;height:40px;border-radius:50%;background:${INK0};box-shadow:0 0 0 7px ${c},0 0 26px ${c};transform:scale(${L(.2, 1, e4(q)).toFixed(3)})"></div>`;
      const cw = 420, cx = Math.max(60, Math.min(1860 - cw, x - cw / 2)), cy = Y - pinH - 190;
      h += `<div class="ab" style="left:${cx}px;top:${(cy + (1 - e4(q)) * 24).toFixed(1)}px;width:${cw}px;height:170px;border-radius:34px;background:rgba(10,14,22,.9);box-shadow:inset 0 0 0 2px ${c};${op(q)};display:flex;flex-direction:column;align-items:center;justify-content:center">
        <div style="font-size:${FIT(m.sub || '', 64, cw - 40)}px;font-weight:900;color:${c};white-space:nowrap;line-height:1.1">${esc(m.sub || '')}</div>
        <div style="margin-top:8px;font-size:${FIT(m.lab, 40, cw - 40)}px;font-weight:800;color:${TX};white-space:nowrap">${esc(m.lab)}</div></div>`; });
    const G = s.gap; if (G) { const pg = P && P.gap && P.gap.a === G.a && P.gap.b === G.b && !(P.gap.at >= 50), q = pg ? 1 : (G.at != null && G.at >= 50 ? 0 : AT(s, G.at, 1.1, 0));
      if (q > 0) { const xa = hx(G.a), xb = hx(G.b), w = (xb - xa) * e4(q);
        h += `<div class="ab" style="left:${xa}px;top:${Y - 9}px;width:${w.toFixed(1)}px;height:18px;border-radius:9px;background:linear-gradient(90deg,${GOLD},${REDC});box-shadow:0 0 22px rgba(200,226,255,.45)"></div>`;
        const n = Math.round((G.b - G.a) * ex(q)), lab = G.lab != null ? G.lab : `${n}시간`;
        h += `<div class="ab" style="left:${(xa + xb) / 2 - 300}px;width:600px;top:${Y + 92}px;text-align:center;${op(c01(q * 2))}"><span class="num" style="font-size:96px;font-weight:900;color:${GOLD};letter-spacing:-3px">${q >= 1 ? esc(lab) : (n + '시간')}</span>${G.sub ? `<div style="margin-top:8px;font-size:32px;font-weight:800;color:${TX}">${esc(G.sub)}</div>` : ''}</div>`; } }
    if (s.note) { const nq = P && P.note && P.note.t === s.note.t ? 1 : AT(s, s.note.at, .6, 0), nx = s.note.h != null ? hx(s.note.h) : 960;   /* 11/12 23:50: 같은 장면에서 제목을 바꾸지 않고, 덧붙는 설명은 눈금 아래 작은 줄로 */
      if (nq > 0) h += `<div class="ab" style="left:${nx - 500}px;width:1000px;top:${Y + 108 + (1 - e4(nq)) * 14}px;text-align:center;${op(nq)}"><span style="display:inline-block;padding:10px 26px;border-radius:34px;background:rgba(255,255,255,.06);box-shadow:inset 0 0 0 2px rgba(255,255,255,.16);font-size:36px;font-weight:800;color:#C9D3E2;white-space:nowrap">${esc(s.note.t)}</span></div>`; }
    return h;
  };
  /* lo_roster(새 모션): 40인 로스터 칸(사람 그림 40개) — 선수 한 명이 칸으로 들어가 잠기거나(영입 막힘) 칸에서 빠져나와 KBO 팀으로 감, lock 이면 칸 전체에 자물쇠 */
  R.lo_roster = (lt, s) => {
    const P = s._prev && s._prev.type === 'lo_roster' && s._prev._cid === s._cid ? s._prev : null;
    const [ey, tt] = (() => { const p = String(s.title || '').split(' · '); return p.length > 1 ? [p[0], p.slice(1).join(' · ')] : ['', p[0]]; })();
    const sameT = P && P.title === s.title;
    let h = eyebrow(ey, P ? 1 : sg(lt, 0, .8), 120, 130);
    if (P && !sameT) { const oq = c01(lt / .25), nq = sg(lt, .12, .9), pp = String(P.title || '').split(' · '), ptt = pp.length > 1 ? pp.slice(1).join(' · ') : pp[0];
      if (oq < 1) h += `<div class="ab" style="left:116px;top:${(190 - 30 * e4(oq)).toFixed(1)}px;font-size:${FIT(ptt, 74, 1700)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap;opacity:${(1 - ss(oq)).toFixed(3)}">${esc(ptt)}</div>`;
      h += `<div class="ab" style="left:116px;top:190px;font-size:${FIT(tt, 74, 1700)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${KIN(tt, nq)}</div>`; }
    else { const tq = P ? 1 : sg(lt, 0, 1.0); h += `<div class="ab" style="left:116px;top:190px;font-size:${FIT(tt, 74, 1700)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${tq >= 1 ? esc(tt) : KIN(tt, tq)}</div>`; }
    const GX0 = 130, GY0 = 380, CW = 84, RH = 112, COLS = 10, N = 40, SLOT = N - 1, gq = P ? 1 : sg(lt, .15, 1.0);
    const man = (c, o) => `<svg width="56" height="84" viewBox="0 0 56 84" style="display:block;opacity:${o}"><circle cx="28" cy="16" r="13" fill="${c}"/><path d="M6 84 V52 Q6 34 28 34 Q50 34 50 52 V84 Z" fill="${c}"/></svg>`;
    const lockSvg = (w, c) => `<svg width="${w}" height="${w * 1.2}" viewBox="0 0 50 60"><path d="M12 26 V17 Q12 4 25 4 Q38 4 38 17 V26" fill="none" stroke="${c}" stroke-width="6"/><rect x="5" y="26" width="40" height="30" rx="6" fill="${c}"/><circle cx="25" cy="39" r="4.5" fill="${INK0}"/><rect x="23" y="41" width="4" height="9" fill="${INK0}"/></svg>`;
    const lkq = s.mode === 'lock' ? (P && P.mode === 'lock' ? 1 : AT(s, s.at, .8, 0)) : 0;
    const slotXY = i => [GX0 + (i % COLS) * CW, GY0 + Math.floor(i / COLS) * RH];
    for (let i = 0; i < N; i++) { const [x, y] = slotXY(i), on = c01(gq * 1.4 - i / N * .4);
      if (i === SLOT && s.img) continue;
      const hq = s.hiN && i < s.hiN ? (P && P.hiN === s.hiN ? 1 : AT(s, s.hiAt, .6, 0)) : 0;   /* 11/12 hiN: 앞 N칸 금색(예: 26인 로스터) */
      h += `<div class="ab" style="left:${x}px;top:${y}px;transform:translateY(${((1 - e4(on)) * 12).toFixed(1)}px);opacity:${(c01(on * 2) * (1 - .55 * lkq)).toFixed(3)}">${man('#C9D3E2', 1)}${hq > 0 ? `<div style="position:absolute;inset:0;opacity:${hq.toFixed(3)}">${man(GOLD, 1)}</div>` : ''}</div>`; }
    h += `<div class="ab" style="left:${GX0}px;top:${GY0 + 4 * RH + 6}px;font-size:34px;font-weight:800;color:${MU};${op(gq)}">${esc(s.sub || '40인 로스터')}</div>`;
    if (lkq > 0) { const pop = L(.6, 1, e4(lkq));
      h += `<div class="ab" style="left:${GX0 - 20}px;top:${GY0 - 20}px;width:${COLS * CW + 10}px;height:${4 * RH + 20}px;border-radius:38px;background:rgba(224,103,95,${(.10 * lkq).toFixed(3)});box-shadow:inset 0 0 0 ${(4 * lkq).toFixed(1)}px rgba(224,103,95,.7)"></div>`;
      h += `<div class="ab" style="left:${GX0 + COLS * CW / 2 - 90}px;top:${GY0 + 2 * RH - 130}px;transform:scale(${pop.toFixed(3)});opacity:${c01(lkq * 2).toFixed(3)};filter:drop-shadow(0 10px 30px rgba(0,0,0,.6))">${lockSvg(180, REDC)}</div>`; }
    /* 선수 한 명: in = 오른쪽 카드 → 칸으로 들어가 잠김 · out = 칸 → 오른쪽 카드 + KBO 팀 로고 */
    if (s.img) { const [sx, sy] = slotXY(SLOT), CXc = 1440, CYc = 470, mq = AT(s, s.at, 1.0, 0), m = s.mode === 'in' ? e4(mq) : s.mode === 'out' ? 1 - e4(mq) : 1;
      const pq = P && P.img === s.img ? 1 : sg(lt, .1, .7);
      const cx = L(CXc, sx + 28, m), cy = L(CYc, sy + 40, m), r = L(150, 46, m);
      const ring = m > .98 ? GOLD : SOFT;
      h += `<div class="ab" style="left:${(cx - r).toFixed(1)}px;top:${(cy - r).toFixed(1)}px;width:${(2 * r).toFixed(1)}px;height:${(2 * r).toFixed(1)}px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 ${(r > 80 ? 6 : 4)}px ${ring},0 18px 40px rgba(0,0,0,.5);opacity:${c01(pq * 2).toFixed(3)}">${PIC(s.img, Math.round(2 * r), Math.round(2 * r), .5, '')}</div>`;
      const nq = c01(1 - m * 1.6) * c01(pq * 2);
      h += `<div class="ab" style="left:${CXc - 260}px;width:520px;top:${CYc + 170}px;text-align:center;opacity:${nq.toFixed(3)}"><div style="font-size:66px;font-weight:900;color:${TX};letter-spacing:-2px">${esc(s.name || '')}</div></div>`;
      if (s.mode === 'in' && mq > 0) { const kq = c01((mq - .7) / .3); h += `<div class="ab" style="left:${sx + 30}px;top:${sy + 34}px;transform:scale(${L(.3, 1, e4(kq)).toFixed(3)});opacity:${kq.toFixed(3)}">${lockSvg(40, GOLD)}</div>`; }
      if (s.mode === 'out' && s.toTeam && mq > 0) { const tq = c01((mq - .5) / .5);
        h += `<div class="ab" style="left:${CXc + 200}px;top:${CYc - 80}px;${up(tq, 20)}">${LG(s.toTeam, 160)}</div>`; } }
    if (s.cap) { const cq = P && P.cap === s.cap ? 1 : AT(s, s.capAt != null ? s.capAt : s.at, .6, 0);
      const bad = s.capC === 'bad';
      h += `<div class="ab" style="left:1110px;width:700px;top:${(800 + (1 - e4(cq)) * 20).toFixed(1)}px;text-align:center;${op(cq)}"><span style="display:inline-block;padding:14px 30px;border-radius:36px;background:${bad ? 'rgba(224,103,95,.16)' : 'rgba(200,226,255,.14)'};box-shadow:inset 0 0 0 2px ${bad ? REDC : GOLD};font-size:${FIT(s.cap, 46, 640)}px;font-weight:900;color:${bad ? REDC : GOLD};white-space:nowrap">${esc(s.cap)}</span></div>`; }
    return h;
  };
  /* ── 11/12 13:18 사용자 "어려운 설명은 단순 텍스트가 아니라 시각 자료로 이해가 쉽게" → lo_flow: 사람·구단 그림(노드) + 화살표(흐름) + 막힘(✕·자물쇠) + 문 닫힘(셔터)
     nodes [{id,x,y,ic,lab,sub,at,c,dim}] · edges [{a,b,lab,at,stopAt,two,bend}] · wall {x,at,lab} · boxes [{x,y,w,h,lab,at,c}] · cap */
  const FLIC = {
    mail: c => `<svg width="170" height="130" viewBox="0 0 120 92"><rect x="4" y="6" width="112" height="80" rx="8" fill="${c}"/><path d="M8 12 L60 52 L112 12" fill="none" stroke="${INK0}" stroke-width="6" stroke-linejoin="round" opacity=".55"/><circle cx="96" cy="68" r="10" fill="${INK0}" opacity=".35"/></svg>`,
    web: c => `<svg width="190" height="150" viewBox="0 0 126 100"><rect x="4" y="6" width="118" height="88" rx="8" fill="none" stroke="${c}" stroke-width="5"/><rect x="4" y="6" width="118" height="18" rx="6" fill="${c}"/><circle cx="16" cy="15" r="3.5" fill="${INK0}"/><circle cx="27" cy="15" r="3.5" fill="${INK0}"/><rect x="16" y="34" width="44" height="48" rx="4" fill="${c}" opacity=".55"/><circle cx="38" cy="50" r="8" fill="${INK0}" opacity=".6"/><path d="M24 80 Q38 60 52 80 Z" fill="${INK0}" opacity=".6"/><path d="M76 40 L76 74 L102 57 Z" fill="${c}" opacity=".55"/></svg>`,
    trophy: c => `<svg width="140" height="150" viewBox="0 0 94 100"><path d="M24 6 H70 V36 Q70 62 47 62 Q24 62 24 36 Z" fill="${c}"/><path d="M24 14 H8 Q8 40 28 44 M70 14 H86 Q86 40 66 44" fill="none" stroke="${c}" stroke-width="6"/><rect x="41" y="60" width="12" height="18" fill="${c}"/><rect x="24" y="78" width="46" height="16" rx="4" fill="${c}"/></svg>`,
    news: c => `<svg width="170" height="140" viewBox="0 0 120 100"><rect x="6" y="8" width="108" height="86" rx="8" fill="${c}"/><g fill="${INK0}" opacity=".55"><rect x="18" y="20" width="84" height="12" rx="3"/><rect x="18" y="42" width="38" height="38" rx="3"/><rect x="64" y="44" width="38" height="7" rx="3"/><rect x="64" y="58" width="38" height="7" rx="3"/><rect x="64" y="72" width="28" height="7" rx="3"/></g></svg>`,
    jp: c => `<svg width="190" height="150" viewBox="0 0 126 100"><path d="M6 44 Q63 6 120 44 V96 H6 Z" fill="${c}"/><circle cx="63" cy="66" r="18" fill="${INK0}" opacity=".6"/></svg>`,
    owner: c => `<svg width="150" height="150" viewBox="0 0 100 100"><circle cx="50" cy="26" r="15" fill="${c}"/><path d="M20 98 V66 Q20 46 50 46 Q80 46 80 66 V98 Z" fill="${c}"/><path d="M50 48 L44 58 L50 86 L56 58 Z" fill="${INK0}"/><rect x="30" y="4" width="40" height="7" rx="2" fill="${c}"/><rect x="36" y="0" width="28" height="8" rx="2" fill="${c}"/></svg>`,
    union: c => `<svg width="190" height="150" viewBox="0 0 130 100"><g opacity=".75"><circle cx="24" cy="34" r="12" fill="${c}"/><path d="M4 98 V70 Q4 52 24 52 Q44 52 44 70 V98 Z" fill="${c}"/><circle cx="106" cy="34" r="12" fill="${c}"/><path d="M86 98 V70 Q86 52 106 52 Q126 52 126 70 V98 Z" fill="${c}"/></g><circle cx="65" cy="26" r="15" fill="${c}"/><path d="M38 98 V66 Q38 46 65 46 Q92 46 92 66 V98 Z" fill="${c}"/></svg>`,
    player: c => `<svg width="130" height="150" viewBox="0 0 86 100"><circle cx="43" cy="28" r="15" fill="${c}"/><path d="M27 22 Q43 6 59 22 L66 24 L27 24 Z" fill="${c}"/><path d="M13 98 V68 Q13 48 43 48 Q73 48 73 68 V98 Z" fill="${c}"/></svg>`,
    team: c => `<svg width="170" height="150" viewBox="0 0 114 100"><path d="M8 40 L57 8 L106 40 Z" fill="${c}"/><rect x="14" y="42" width="86" height="54" rx="4" fill="${c}"/><rect x="26" y="54" width="14" height="14" rx="2" fill="${INK0}"/><rect x="50" y="54" width="14" height="14" rx="2" fill="${INK0}"/><rect x="74" y="54" width="14" height="14" rx="2" fill="${INK0}"/><rect x="48" y="76" width="18" height="20" rx="2" fill="${INK0}"/></svg>`,
    roster: c => { let g = ''; for (let i = 0; i < 15; i++) { const x = 14 + (i % 5) * 18, y = 18 + Math.floor(i / 5) * 24; g += `<circle cx="${x + 7}" cy="${y + 5}" r="4.5" fill="${c}"/><path d="M${x} ${y + 21} V${y + 15} Q${x} ${y + 10} ${x + 7} ${y + 10} Q${x + 14} ${y + 10} ${x + 14} ${y + 15} V${y + 21} Z" fill="${c}"/>`; }
      return `<svg width="170" height="150" viewBox="0 0 114 100"><rect x="4" y="6" width="106" height="90" rx="10" fill="none" stroke="${c}" stroke-width="4"/>${g}</svg>`; },
    doc: c => `<svg width="120" height="150" viewBox="0 0 80 100"><path d="M6 4 H54 L74 24 V96 H6 Z" fill="${c}"/><path d="M54 4 V24 H74" fill="none" stroke="${INK0}" stroke-width="3" opacity=".5"/><g stroke="${INK0}" stroke-width="4" opacity=".55"><line x1="16" y1="40" x2="64" y2="40"/><line x1="16" y1="52" x2="64" y2="52"/><line x1="16" y1="64" x2="52" y2="64"/></g><path d="M18 82 Q26 74 32 82 T46 80" fill="none" stroke="${INK0}" stroke-width="3" opacity=".6"/></svg>`,
    ghost: c => `<svg width="120" height="150" viewBox="0 0 80 100"><path d="M6 4 H54 L74 24 V96 H6 Z" fill="none" stroke="${c}" stroke-width="3.5" stroke-dasharray="8 7"/><text x="40" y="66" text-anchor="middle" font-size="40" font-weight="900" fill="${c}">?</text></svg>`,
    kbo: c => `<svg width="170" height="150" viewBox="0 0 114 100"><path d="M8 40 L57 8 L106 40 Z" fill="${c}"/><rect x="14" y="42" width="86" height="54" rx="4" fill="${c}"/><text x="57" y="80" text-anchor="middle" font-size="26" font-weight="900" fill="${INK0}">KBO</text></svg>`,
    stadium: c => `<svg width="220" height="150" viewBox="0 0 146 100"><path d="M6 44 Q73 6 140 44 V96 H6 Z" fill="${c}"/><rect x="54" y="56" width="38" height="40" rx="3" fill="${INK0}"/><g fill="${INK0}" opacity=".5"><rect x="18" y="58" width="14" height="10" rx="2"/><rect x="114" y="58" width="14" height="10" rx="2"/></g></svg>`,
  };
  const LOCK = (w, c) => `<svg width="${w}" height="${w * 1.2}" viewBox="0 0 50 60"><path d="M12 26 V17 Q12 4 25 4 Q38 4 38 17 V26" fill="none" stroke="${c}" stroke-width="6"/><rect x="5" y="26" width="40" height="30" rx="6" fill="${c}"/><circle cx="25" cy="39" r="4.5" fill="${INK0}"/><rect x="23" y="41" width="4" height="9" fill="${INK0}"/></svg>`;
  /* ── 11/13 00:39 사용자 "이런 텍스트만 나오게 하지 말라니까" → lo_pay: 구단 연봉 막대(세로) + 상한선·하한선(그어짐·✕) + 차이 괄호 + 막대 위 꼬리표
     bars [{v(0~1),lab,c,at,segs:[{f,c,lab}]}] · lines [{v,v0,lab,c,at,xAt,cutAt}] · brk {a,b,lab,at} · tags [{i,lab,c,at}] · cap */
  R.lo_pay = (lt, s) => {
    const P = s._prev && s._prev.type === 'lo_pay' && s._prev._cid === s._cid ? s._prev : null;
    const bars = s.bars || [], n = bars.length, X0 = s.x0 || 300, X1 = s.x1 || 1460, BY = s.by || 790, TOP = s.top || 300, H = BY - TOP;
    const slot = (X1 - X0) / Math.max(1, n), BW = Math.min(s.bw || 150, slot * .62);
    const col = c => c === 'gold' ? GOLD : c === 'bad' ? REDC : c === 'grn' ? GRN : c === 'mu' ? '#5E6B80' : SOFT;
    const yv = v => BY - H * v;
    let sv = `<line x1="${X0 - 30}" y1="${BY}" x2="${X1 + 30}" y2="${BY}" stroke="rgba(255,255,255,.25)" stroke-width="4"/>`, h = '';
    const cuts = (s.lines || []).filter(l => l.cutAt != null);
    bars.forEach((b, i) => { const q = AT(s, b.at, .8, 0); if (q <= 0) return; const cx = X0 + slot * (i + .5), x = cx - BW / 2;
      if (b.segs) { let acc = 0; b.segs.forEach(g => { const sq = AT(s, g.at != null ? g.at : b.at, .7, 0); if (sq <= 0) { acc += g.f; return; }
          const y1 = yv(acc), y2 = yv(acc + g.f * e4(sq)), c = col(g.c);
          sv += `<rect x="${x.toFixed(1)}" y="${y2.toFixed(1)}" width="${BW.toFixed(1)}" height="${(y1 - y2).toFixed(1)}" fill="${c}" opacity=".9" stroke="${INK0}" stroke-width="4"/>`;
          if (g.lab) h += `<div class="ab" style="left:${(x + BW + 30).toFixed(1)}px;top:${((y1 + yv(acc + g.f)) / 2 - 28).toFixed(1)}px;font-size:${FIT(g.lab, 46, 560)}px;font-weight:900;color:${c};white-space:nowrap;${op(sq)}">${esc(g.lab)}</div>`;
          acc += g.f; }); }
      else { const v = b.v * e4(q), c = col(b.c); let top = yv(v);
        cuts.forEach(l => { const cq = AT(s, l.cutAt, .6, 0); if (cq > 0 && b.v > l.v) { const ly = yv(l.v);
            sv += `<rect x="${x.toFixed(1)}" y="${top.toFixed(1)}" width="${BW.toFixed(1)}" height="${(ly - top).toFixed(1)}" fill="none" stroke="${REDC}" stroke-width="4" stroke-dasharray="12 9" opacity="${c01(cq * 2).toFixed(3)}"/>`;
            sv += `<rect x="${x.toFixed(1)}" y="${top.toFixed(1)}" width="${BW.toFixed(1)}" height="${(ly - top).toFixed(1)}" fill="${c}" opacity="${(.9 * (1 - .8 * cq)).toFixed(3)}"/>`; top = ly; } });
        if (b.ghost) { sv += `<rect x="${x.toFixed(1)}" y="${top.toFixed(1)}" width="${BW.toFixed(1)}" height="${(BY - top).toFixed(1)}" fill="${c}" fill-opacity=".12" stroke="${c}" stroke-width="5" stroke-dasharray="14 10"/>`;   /* 11/13: 근거 없는 크기 → 점선 + ? */
          h += `<div class="ab" style="left:${(cx - 60).toFixed(1)}px;width:120px;top:${((top + BY) / 2 - 40).toFixed(1)}px;text-align:center;font-size:64px;font-weight:900;color:${c};${op(q)}">?</div>`; }
        else sv += `<rect x="${x.toFixed(1)}" y="${top.toFixed(1)}" width="${BW.toFixed(1)}" height="${(BY - top).toFixed(1)}" fill="${c}" opacity=".9"/>`; }
      if (b.lab) h += `<div class="ab" style="left:${(cx - slot / 2).toFixed(1)}px;width:${slot.toFixed(1)}px;top:${BY + 14}px;text-align:center;font-size:${FIT(b.lab, 34, slot - 10)}px;font-weight:800;color:${MU};white-space:nowrap;${op(q)}">${esc(b.lab)}</div>`; });
    (s.lines || []).forEach(l => { const q = AT(s, l.at, .8, 0); if (q <= 0) return; const xq = l.xAt != null ? AT(s, l.xAt, .5, 0) : 0;
      const mv = l.v0 != null ? L(l.v0, l.v, e4(AT(s, l.moveAt != null ? l.moveAt : l.at, .9, 0))) : l.v, y = yv(mv), c = xq > .5 ? REDC : col(l.c || 'gold');
      const x2 = X0 - 40 + (X1 - X0 + 80) * e4(q);
      sv += `<line x1="${X0 - 40}" y1="${y.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y.toFixed(1)}" stroke="${c}" stroke-width="8" stroke-linecap="round" ${xq > .5 ? 'stroke-dasharray="18 14"' : ''} opacity="${(1 - .3 * xq).toFixed(3)}"/>`;
      if (l.lab) h += `<div class="ab" style="left:${X1 + 60}px;top:${(y - 30).toFixed(1)}px;font-size:${FIT(l.lab, 46, 1880 - X1 - 60)}px;font-weight:900;color:${c};white-space:nowrap;${op(q)}">${esc(l.lab)}</div>`;
      if (xq > 0) { const mx = (X0 + X1) / 2, p2 = L(.4, 1, e4(xq)); sv += `<g transform="translate(${mx} ${y.toFixed(1)}) scale(${p2.toFixed(3)})" opacity="${c01(xq * 2).toFixed(3)}"><circle r="40" fill="${INK0}" stroke="${REDC}" stroke-width="7"/><path d="M-16 -16 L16 16 M16 -16 L-16 16" stroke="${REDC}" stroke-width="9" stroke-linecap="round"/></g>`; } });
    if (s.brk) { const b = s.brk, q = AT(s, b.at, .7, 0); if (q > 0) { const A = bars[b.a], B = bars[b.b], ya = yv(A.v), yb = yv(B.v), bx = X0 + slot * (b.b + .5) + Math.max(BW / 2 + 40, 190);
        sv += `<line x1="${(X0 + slot * (b.a + .5) + BW / 2 + 8).toFixed(1)}" y1="${ya.toFixed(1)}" x2="${(bx + 20).toFixed(1)}" y2="${ya.toFixed(1)}" stroke="${GOLD}" stroke-width="4" stroke-dasharray="10 10" opacity="${q.toFixed(3)}"/>`;
        const yy = L(yb, ya, e4(q)); sv += `<path d="M${bx} ${yb} H${bx + 20} V${yy.toFixed(1)} H${bx}" fill="none" stroke="${GOLD}" stroke-width="7" stroke-linejoin="round"/>`;
        if (b.lab) h += `<div class="ab" style="left:${bx + 44}px;top:${((ya + yb) / 2 - 36).toFixed(1)}px;font-size:${FIT(b.lab, 52, 1880 - bx - 44)}px;font-weight:900;color:${GOLD};white-space:nowrap;line-height:1.15;${op(q)}">${esc(b.lab).replace(/\n/g, '<br>')}</div>`; } }
    (s.tags || []).forEach(t => { const q = AT(s, t.at, .6, 0); if (q <= 0) return; const b = bars[t.i], cx = X0 + slot * (t.i + .5), y = yv(b.v) - 76, c = col(t.c || 'gold');
      h += `<div class="ab" style="left:${(cx - 200).toFixed(1)}px;width:400px;top:${(y + (1 - e4(q)) * 16).toFixed(1)}px;text-align:center;${op(q)}"><span style="display:inline-block;padding:8px 18px;border-radius:34px;background:rgba(11,16,24,.85);box-shadow:inset 0 0 0 2px ${c};font-size:${FIT(t.lab, 36, 380)}px;font-weight:900;color:${c};white-space:nowrap">${esc(t.lab)}</span></div>`; });
    h = `<svg class="ab" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">${sv}</svg>` + h;
    if (s.cap) { const cq = P && P.cap === s.cap ? 1 : AT(s, s.capAt != null ? s.capAt : 0, .6, 0), bad = s.capC === 'bad';
      h += `<div class="ab" style="left:${(s.capX || 960) - 500}px;width:1000px;top:${(s.capY || 170) + (1 - e4(cq)) * 20}px;text-align:center;${op(cq)}"><span style="display:inline-block;padding:14px 30px;border-radius:36px;background:${bad ? 'rgba(224,103,95,.16)' : 'rgba(200,226,255,.14)'};box-shadow:inset 0 0 0 2px ${bad ? REDC : GOLD};font-size:${FIT(s.cap, 46, 940)}px;font-weight:900;color:${bad ? REDC : GOLD};white-space:nowrap">${esc(s.cap)}</span></div>`; }
    return h;
  };
  R.lo_flow = (lt, s) => {
    const P = s._prev && s._prev.type === 'lo_flow' && s._prev._cid === s._cid ? s._prev : null;
    const [ey, tt] = (() => { const p = String(s.title || '').split(' · '); return p.length > 1 ? [p[0], p.slice(1).join(' · ')] : ['', p[0]]; })();
    const sameT = P && P.title === s.title;
    let h = eyebrow(ey, P ? 1 : sg(lt, 0, .8), 120, 130);
    if (P && !sameT) { const oq = c01(lt / .25), nq = sg(lt, .12, .9), pp = String(P.title || '').split(' · '), ptt = pp.length > 1 ? pp.slice(1).join(' · ') : pp[0];
      if (oq < 1) h += `<div class="ab" style="left:116px;top:${(190 - 30 * e4(oq)).toFixed(1)}px;font-size:${FIT(ptt, 74, 1700)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap;opacity:${(1 - ss(oq)).toFixed(3)}">${esc(ptt)}</div>`;
      h += `<div class="ab" style="left:116px;top:190px;font-size:${FIT(tt, 74, 1700)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${KIN(tt, nq)}</div>`; }
    else { const tq = P ? 1 : sg(lt, 0, 1.0); h += `<div class="ab" style="left:116px;top:190px;font-size:${FIT(tt, 74, 1700)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${tq >= 1 ? esc(tt) : KIN(tt, tq)}</div>`; }
    const col = c => c === 'gold' ? GOLD : c === 'bad' ? REDC : c === 'grn' ? GRN : c === 'mu' ? '#5E6B80' : '#C9D3E2';
    const pq = (P0, id, key, at) => { const o = P0 && (P0[key] || []).find(z => z.id === id); return o && !(o.at >= 50) && (o.at == null || o.at < 0 || true) ? null : 1; };
    const hadF = (key, f) => !!(P && (P[key] || []).some(z => f(z) && !(z.at >= 50)));
    (s.boxes || []).forEach(b => { const q = hadF('boxes', z => z.x === b.x && z.y === b.y && z.lab === b.lab) ? 1 : AT(s, b.at, .6, 0); if (q <= 0) return; const c = col(b.c);
      h += `<div class="ab" style="left:${b.x}px;top:${b.y}px;width:${b.w}px;height:${b.h}px;border-radius:40px;background:${b.c === 'bad' ? 'rgba(224,103,95,.08)' : 'rgba(255,255,255,.035)'};box-shadow:inset 0 0 0 2px ${b.c ? c : 'rgba(255,255,255,.12)'};${op(q)}"></div>`;
      if (b.lab) h += `<div class="ab" style="left:${b.x + 24}px;top:${b.y + 16}px;font-size:30px;font-weight:800;color:${b.c ? c : MU};${op(q)}">${esc(b.lab)}</div>`; });
    const N = {}; (s.nodes || []).forEach(n => N[n.id] = n);
    /* 화살표·막힘·셔터: 한 장 SVG */
    let sv = '';
    (s.edges || []).forEach(e => { const A = N[e.a], B = N[e.b]; if (!A || !B) return; const q = hadF('edges', z => z.a === e.a && z.b === e.b) ? 1 : AT(s, e.at, .7, 0); if (q <= 0) return;
      const sq = e.stopAt != null ? AT(s, e.stopAt, .5, 0) : 0, okq = e.okAt != null ? AT(s, e.okAt, .5, 0) : 0;
      const dx = B.x - A.x, dy = B.y - A.y, d = Math.hypot(dx, dy), ux = dx / d, uy = dy / d, r0 = e.r0 || 120, r1 = e.r1 || 120;
      const x0 = A.x + ux * r0, y0 = A.y + uy * r0, x1 = B.x - ux * r1, y1 = B.y - uy * r1, bend = e.bend || 0;
      const mx = (x0 + x1) / 2 - uy * bend, my = (y0 + y1) / 2 + ux * bend, len = Math.hypot(x1 - x0, y1 - y0) * (bend ? 1.08 : 1);
      const c = sq > .5 ? REDC : okq > .5 ? GRN : e.c === 'gold' ? GOLD : e.c === 'bad' ? REDC : '#C9D3E2', dq = e4(q);
      sv += `<path d="M${x0.toFixed(1)} ${y0.toFixed(1)} Q${mx.toFixed(1)} ${my.toFixed(1)} ${x1.toFixed(1)} ${y1.toFixed(1)}" fill="none" stroke="${c}" stroke-width="9" stroke-linecap="round" ${sq > .5 ? 'stroke-dasharray="16 14"' : `stroke-dasharray="${len.toFixed(0)}" stroke-dashoffset="${(len * (1 - dq)).toFixed(1)}"`} opacity="${(sq > 0 ? 1 - .35 * sq : 1).toFixed(3)}"/>`;
      const ah = (px, py, vx, vy) => { const L2 = Math.hypot(vx, vy), a = vx / L2, b = vy / L2; return `<path d="M${(px - a * 26 - b * 15).toFixed(1)} ${(py - b * 26 + a * 15).toFixed(1)} L${px.toFixed(1)} ${py.toFixed(1)} L${(px - a * 26 + b * 15).toFixed(1)} ${(py - b * 26 - a * 15).toFixed(1)}" fill="none" stroke="${c}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" opacity="${c01(dq * 3 - 2).toFixed(3)}"/>`; };
      sv += ah(x1, y1, x1 - mx, y1 - my); if (e.two) sv += ah(x0, y0, x0 - mx, y0 - my);
      const lx = .25 * x0 + .5 * mx + .25 * x1, ly = .25 * y0 + .5 * my + .25 * y1;
      if (e.lab) sv += `<text x="${lx.toFixed(1)}" y="${(ly - (e.labDy != null ? e.labDy : 52)).toFixed(1)}" text-anchor="middle" font-size="${e.fs || 44}" font-weight="900" fill="${c}" opacity="${c01(dq * 2 - .6).toFixed(3)}" style="paint-order:stroke" stroke="${INK0}" stroke-width="10">${esc(e.lab)}</text>`;
      if (sq > 0) { const p2 = L(.4, 1, e4(sq)); sv += `<g transform="translate(${lx.toFixed(1)} ${ly.toFixed(1)}) scale(${p2.toFixed(3)})" opacity="${c01(sq * 2).toFixed(3)}"><circle r="34" fill="${INK0}" stroke="${REDC}" stroke-width="6"/><path d="M-14 -14 L14 14 M14 -14 L-14 14" stroke="${REDC}" stroke-width="8" stroke-linecap="round"/></g>`; } });
    if (s.wall) { const w = s.wall, q = AT(s, w.at, .9, 0);
      if (q > 0) { const y1 = L(250, w.y1 || 760, e4(q)), X = w.x;
        sv += `<rect x="${X - 44}" y="250" width="88" height="${(y1 - 250).toFixed(1)}" rx="8" fill="#2A3242" stroke="${REDC}" stroke-width="4"/>`;
        for (let yy = 280; yy < y1 - 10; yy += 34) sv += `<line x1="${X - 36}" y1="${yy}" x2="${X + 36}" y2="${yy}" stroke="#46526A" stroke-width="4"/>`; } }
    if (sv) h += `<svg class="ab" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">${sv}</svg>`;
    if (s.wall) { const w = s.wall, q = AT(s, w.at, .9, 0), lq = c01((q - .75) / .25);
      if (lq > 0) h += `<div class="ab" style="left:${w.x - 60}px;top:${(Math.round(L(250, w.y1 || 760, e4(q))) / 2 + 250 / 2 - 72).toFixed(1)}px;transform:scale(${L(.5, 1, e4(lq)).toFixed(3)});opacity:${lq.toFixed(3)};filter:drop-shadow(0 10px 24px rgba(0,0,0,.6))">${LOCK(120, REDC)}</div>`;
      if (w.lab && lq > 0) h += `<div class="ab" style="left:${w.x - 300}px;width:600px;top:${w.labY || 870}px;text-align:center;font-size:${w.fs || 64}px;font-weight:900;color:${REDC};letter-spacing:-1px;${op(lq)}">${esc(w.lab)}</div>`; }
    (s.nodes || []).forEach(n => { const q = hadF('nodes', z => z.id === n.id) ? 1 : AT(s, n.at, .6, 0); if (q <= 0) return;
      const xq = n.expAt != null ? AT(s, n.expAt, .5, 0) : 0, gone = n.goneAt != null ? AT(s, n.goneAt, .5, 0) : 0, hq = n.hiAt != null ? AT(s, n.hiAt, .5, 0) : 0;
      const c0 = col(n.c), c = xq > .5 ? '#5E6B80' : hq > .5 ? GOLD : c0, ic = n.img && photoSrc(n.img) ? `<div style="position:relative;display:inline-block;width:120px;height:120px;border-radius:50%;overflow:hidden;background:#fff;box-shadow:0 0 0 4px ${c}">${PIC(n.img, 120, 120, .5, '')}</div>` : n.logo && LG(n.logo, 110) ? `<div style="display:inline-block;padding:10px;border-radius:38px;background:rgba(255,255,255,${hq > .5 ? .92 : 0});box-shadow:${hq > .5 ? 'inset 0 0 0 5px ' + GOLD : 'none'}">${LG(n.logo, Math.round(140 * (n.lsz || 1)))}</div>` : (FLIC[n.ic] || FLIC.player)(c);   /* 11/13 검수: 구단은 집 아이콘 말고 실제 로고 */
      const o = ss(q * 1.25) * (1 - gone) * (n.dim ? .45 : 1);
      h += `<div class="ab" style="left:${n.x - 230}px;width:460px;top:${n.y - 85}px;text-align:center;opacity:${o.toFixed(3)};transform:translateY(${((1 - e4(q)) * 24).toFixed(1)}px)"><div style="display:inline-block;transform:scale(${s.isz || 1.45});transform-origin:50% 100%;filter:drop-shadow(0 12px 26px rgba(0,0,0,.45))">${ic}</div>
        ${n.lab ? `<div style="margin-top:10px;font-size:${FIT(n.lab, n.fs || 50, 440)}px;font-weight:900;color:${xq > .5 ? MU : TX};white-space:nowrap;letter-spacing:-1px">${esc(n.lab)}</div>` : ''}${n.sub ? `<div style="margin-top:4px;font-size:${FIT(n.sub, 34, 440)}px;font-weight:800;color:${n.subC === 'bad' ? REDC : n.subC === 'gold' ? GOLD : MU};white-space:nowrap">${esc(n.sub)}</div>` : ''}</div>`;
      if (xq > 0 && n.stamp) h += `<div class="ab" style="left:${n.x - 110}px;width:220px;top:${n.y - 40}px;text-align:center;transform:rotate(-12deg) scale(${L(1.6, 1, e4(xq)).toFixed(3)});opacity:${(c01(xq * 2) * (1 - gone)).toFixed(3)}"><span style="display:inline-block;padding:6px 18px;border:6px solid ${REDC};border-radius:34px;font-size:46px;font-weight:900;color:${REDC};background:rgba(11,16,24,.7)">${esc(n.stamp)}</span></div>`;
      if (n.lockAt != null) { const lk = AT(s, n.lockAt, .6, 0); if (lk > 0) h += `<div class="ab" style="left:${n.x + 40}px;top:${n.y - 110}px;transform:scale(${L(.4, 1, e4(lk)).toFixed(3)});opacity:${c01(lk * 2).toFixed(3)}">${LOCK(70, REDC)}</div>`; } });
    if (s.cap) { const cq = P && P.cap === s.cap ? 1 : AT(s, s.capAt != null ? s.capAt : 0, .6, 0), bad = s.capC === 'bad';
      h += `<div class="ab" style="left:${s.capX != null ? s.capX - 500 : 460}px;width:1000px;top:${(s.capY || 800) + (1 - e4(cq)) * 20}px;text-align:center;${op(cq)}"><span style="display:inline-block;padding:14px 30px;border-radius:36px;background:${bad ? 'rgba(224,103,95,.16)' : 'rgba(200,226,255,.14)'};box-shadow:inset 0 0 0 2px ${bad ? REDC : GOLD};font-size:${FIT(s.cap, 46, 940)}px;font-weight:900;color:${bad ? REDC : GOLD};white-space:nowrap">${esc(s.cap)}</span></div>`; }
    return h;
  };
  /* ── 11/12 23:49 사용자 "이 장면 달력으로 보여주면 좋을 것 같아" → lo_cal: 달력 3장(12월·2월·3월)에 마감 날짜 동그라미, 지금 마감은 금색
     months [{lab, sub, first(일요일=0), days}] · items [{m(0~2), d 또는 [d1,d2], time, t, at, hl}] */
  R.lo_cal = (lt, s) => {
    const P = s._prev && s._prev.type === 'lo_cal' ? s._prev : null;
    const [ey, tt] = (() => { const p = String(s.title || '').split(' · '); return p.length > 1 ? [p[0], p.slice(1).join(' · ')] : ['', p[0]]; })();
    const tq = P && P.title === s.title ? 1 : sg(lt, 0, 1.0);
    let h = eyebrow(ey, P ? 1 : sg(lt, 0, .8), 120, 130) + `<div class="ab" style="left:116px;top:190px;font-size:${FIT(tt, 74, 1700)}px;font-weight:900;letter-spacing:-2px;color:${TX};white-space:nowrap">${tq >= 1 ? esc(tt) : KIN(tt, tq)}</div>`;
    const W = 500, G = 80, NM = Math.max(1, (s.months || []).length), X0 = (1920 - (NM * W + (NM - 1) * G)) / 2, Y0 = 300, CW = W / 7, HH = 74, WH = 40, RH = 50, anyHl = (s.items || []).some(it => it.hl);
    const sq = P ? 1 : sg(lt, .1, .7);
    (s.months || []).forEach((M, mi) => {
      const x = X0 + mi * (W + G), its = (s.items || []).filter(it => it.m === mi), hot = its.some(it => it.hl && AT(s, it.at, .5, 0) > 0);
      const rows = Math.ceil((M.first + M.days) / 7), Hs = HH + WH + rows * RH + 16;
      h += `<div class="ab" style="left:${x}px;top:${Y0 + (1 - e4(sq)) * 24}px;width:${W}px;height:${Hs}px;border-radius:32px;overflow:hidden;background:rgba(255,255,255,.045);box-shadow:inset 0 0 0 2px ${hot ? GOLD : 'rgba(255,255,255,.12)'}${hot ? ',0 0 40px rgba(200,226,255,.25)' : ''};opacity:${(ss(sq) * (anyHl && !hot ? .55 : 1)).toFixed(3)}">
        <div style="height:${HH}px;background:${hot ? GOLD : '#2A3448'};display:flex;align-items:center;justify-content:center;gap:14px"><span style="font-size:46px;font-weight:900;color:${hot ? INK0 : TX}">${esc(M.lab)}</span><span style="font-size:26px;font-weight:800;color:${hot ? INK0 : MU}">${esc(M.sub || '')}</span></div>
        <div style="display:flex;height:${WH}px;align-items:center">${['일', '월', '화', '수', '목', '금', '토'].map((d, i) => `<div style="width:${CW}px;text-align:center;font-size:22px;font-weight:800;color:${i === 0 ? '#E0675F' : i === 6 ? '#7DA6E8' : MU}">${d}</div>`).join('')}</div>`;
      for (let d = 1; d <= M.days; d++) { const c = M.first + d - 1, cx = (c % 7) * CW, cy = HH + WH + Math.floor(c / 7) * RH;
        h += `<div style="position:absolute;left:${cx}px;top:${cy}px;width:${CW}px;height:${RH}px;line-height:${RH}px;text-align:center;font-size:26px;font-weight:700;color:${c % 7 === 0 ? '#C77' : '#AEB8C8'}">${d}</div>`; }
      h += `</div>`;
      /* 표시: 하루 = 동그라미, 기간 = 띠 */
      its.forEach(it => { const q = AT(s, it.at, .6, 0); if (q <= 0) return; const c0 = it.hl ? GOLD : '#7DA6E8';
        const d1 = Array.isArray(it.d) ? it.d[0] : it.d, d2 = Array.isArray(it.d) ? it.d[1] : it.d;
        for (let d = d1; d <= d2; ) { const c = M.first + d - 1, row = Math.floor(c / 7), endC = Math.min(d2, d + (6 - c % 7)), c2 = M.first + endC - 1;
          const lx = x + (c % 7) * CW, ty = Y0 + HH + WH + row * RH, wpx = (c2 - c + 1) * CW;
          if (d1 === d2) h += `<div class="ab" style="left:${lx + CW / 2 - 30}px;top:${ty + RH / 2 - 30}px;width:60px;height:60px;border-radius:50%;box-shadow:inset 0 0 0 5px ${c0}${it.hl ? ',0 0 22px rgba(200,226,255,.6)' : ''};transform:scale(${L(1.8, 1, e4(q)).toFixed(3)});opacity:${c01(q * 2).toFixed(3)}"></div>`;
          else h += `<div class="ab" style="left:${lx + 3}px;top:${ty + 5}px;width:${(wpx - 6) * e4(q)}px;height:${RH - 10}px;border-radius:34px;background:${it.hl ? 'rgba(200,226,255,.28)' : 'rgba(125,166,232,.22)'};box-shadow:inset 0 0 0 3px ${c0}"></div>`;
          d = endC + 1; } });
      /* 아래 설명 */
      const ly = Y0 + Hs + 24;
      its.forEach((it, k) => { const q = AT(s, it.at, .6, 0); if (q <= 0) return; const c0 = it.hl ? GOLD : anyHl ? MU : TX;
        h += `<div class="ab" style="left:${x}px;width:${W}px;top:${ly + k * 62 + (1 - e4(q)) * 14}px;text-align:center;white-space:nowrap;${op(q)}"><span style="font-size:${FIT((it.time ? it.time + ' ' : '') + it.t, 40, W)}px;font-weight:900;color:${c0}">${it.time ? `<span style="color:${it.hl ? GOLD : '#7DA6E8'}">${esc(it.time)}</span> ` : ''}${esc(it.t)}</span></div>`; });
    });
    return h;
  };
  /* ── 카메라: 묶음(_cid) 단위로 한 번 흐른다(사진 크기가 장면 사이에서 바뀌지 않게) ── */
  const CAMS = { rf_band: 'push', question: 'push', rf_duo: 'push', tline: 'drift', pstat: 'drift', rf_card: 'drift', speech: 'drift', rf_capbar: 'pull', rf_bars: 'pull' };
  function cam(k, t) { return ''; }   /* 11/10 01:12 사용자 "가만히 있는 장면에서도 화면이 이리저리 움직여서 정신사나워" → 카메라 이동 없음 */
  /* ── 한 장면 그리기(NOW 는 t) ── */
  const LT = {};
  /* 11/12 00:28 사용자 "처음엔 목차들을 다 보여주고 나레이션으로 설명은 하지마 · 그 목차의 순서가 되면 목차를 보여주고 이야기하려는 부분이 강조되게 —
     지금 여기까지 이야기했다는 느낌": 장면에 toc={hi, sec, hiAt} 이 있으면 그 장면 끝 sec 초(말 없는 holdAfter)에 목차 판이 덮인다.
     지난 칸 = 흐린 체크, 지금 칸 = 금색 띠(앞 칸에서 미끄러져 옴), 다음 칸 = 흰색. hi 가 없거나 hiAt 전이면 전체만 보임(오프닝) */
  function tocLayer(k, lt) { const s = SC[k], T = s && s.toc, its = EP.toc || []; if (!T || !its.length) return '';
    const dur = BD[k] - (k > 0 ? BD[k - 1] : 0), t0 = T.full ? 0 : dur - (T.sec || 2.4), q = c01((lt - t0) / .35);   /* 11/12 13:15: full = 챕터 다리 대사 줄 전체 동안 목차판 */ if (q <= 0) return '';
    const hi = T.hi == null ? -1 : T.hi, hq = hi < 0 ? 0 : c01((lt - t0 - (T.hiAt != null ? T.hiAt : .35)) / .6), from = hi - 1;
    const n = its.length, RH = Math.min(96, Math.floor(640 / n)), Y0 = 300 + Math.round((640 - RH * n) / 2), X = 300, W = 1320;
    const pos = from + (hi - from) * e4(hq), barY = Y0 + pos * RH;
    let h = `<div class="ab" style="inset:0;background:rgba(8,11,17,${ss(q).toFixed(3)})"></div>`;
    h += `<div class="ab" style="left:${X}px;top:${(170 + (1 - e4(q)) * 20).toFixed(1)}px;${op(q)}"><div style="width:90px;height:5px;background:${GOLD};margin-bottom:14px"></div><div style="font-size:64px;font-weight:900;color:${TX};letter-spacing:-2px">${esc(EP.tocTitle || '오늘의 순서')}</div></div>`;
    h += `<div class="ab" style="left:${X - 30}px;top:${Y0}px;width:4px;height:${RH * n}px;background:rgba(255,255,255,.12);${op(q)}"></div>`;
    if (hi >= 0) h += `<div class="ab" style="left:${X - 30}px;top:${Y0}px;width:4px;height:${Math.max(0, (pos + 1) * RH).toFixed(1)}px;background:${GOLD};${op(q)}"></div>`;
    if (hi >= 0 && hq > 0 && pos >= -0.99) h += `<div class="ab" style="left:${X - 10}px;top:${(barY + 6).toFixed(1)}px;width:${W}px;height:${RH - 12}px;border-radius:36px;background:linear-gradient(90deg,rgba(200,226,255,.24),rgba(200,226,255,.06));box-shadow:inset 4px 0 0 ${GOLD};opacity:${c01(hq * 2 + (from >= 0 ? 1 : 0)).toFixed(3)}"></div>`;
    its.forEach((it, i) => { const iq = c01(q * 1.6 - i * .06), past = hi >= 0 && i < hi, cur = i === hi && hq > .5;
      const col = cur ? GOLD : past ? 'rgba(170,180,196,.55)' : TX, mk = past ? '✓' : String(i + 1).padStart(2, '0');
      h += `<div class="ab" style="left:${X + 20}px;top:${Y0 + i * RH}px;height:${RH}px;display:flex;align-items:center;gap:30px;${up(iq, 14)}">
        <div style="width:64px;font-size:${Math.round(RH * .42)}px;font-weight:900;color:${cur ? GOLD : past ? 'rgba(170,180,196,.55)' : MU}">${mk}</div>
        <div style="font-size:${Math.min(Math.round(RH * .5), FIT(it, 50, 1100))}px;font-weight:900;color:${col};white-space:nowrap;letter-spacing:-1px">${esc(it)}</div></div>`; });
    return h; }
  function draw(k, lt) { const s = SC[k]; const f = R[s.type]; return (f ? f(lt, s) : '') + tocLayer(k, lt); }
  const TRW = .5;
  const PERSON = /^(pstat|rf_card|speech|rf_duo|v_duo|v_grid)$/, TRK = {};
  function trBase(k) { const s = SC[k], p = SC[k - 1]; if (!s || !p) return 'push';
    if (chapAt(k) !== chapAt(k - 1)) return 'line';
    if (PERSON.test(s.type) && !PERSON.test(p.type)) return 'zoom';
    if (/^(question|rf_band|v_q|v_cal)$/.test(s.type)) return 'up';
    return 'push'; }
  function trKind(k) { if (TRK[k]) return TRK[k]; let pk = -1; for (let j = k - 1; j > 0; j--) if (!(SC[j]._chain || SC[j]._keep || (SC[j].type === 'rf_capbar' && SC[j - 1].type === 'rf_capbar'))) { pk = j; break; }
    let kd = trBase(k); const pv = pk > 0 ? trKind(pk) : '';
    if (kd === pv && kd !== 'line') kd = { push: 'up', up: 'zoom', zoom: 'push' }[kd];
    return (TRK[k] = kd); }
  /* 앞 장면을 다시 그릴 때는 그 장면이 끝나던 순간의 lt 로(99 로 그리면 시간 따라 바뀌는 것이 전환 순간 튐 — 10:21 물음표 순간이동) */
  const endLt = k => LT[k] != null ? LT[k] : Math.max(0, BD[k] - (k > 0 ? BD[k - 1] : 0) - .001);
  function post(t) {
    if (!MGON) return; layers();
    let k = 0; while (k < BD.length && t >= BD[k]) k++;
    const kk = Math.min(k, SC.length - 1), start = kk === 0 ? 0 : BD[kk - 1], s = SC[kk];
    if (!s) return;
    NOW = t; paintBG(t, kk); paintBug(kk, t); if (VERT) paintTitle(t);
    let lt = LT[kk] != null ? LT[kk] : (t - start);
    A.style.transform = cam(kk, t); A.style.transformOrigin = '50% 46%';
    /* 같은 사람 장면에서 내용만 바뀔 때: 앞 내용이 0.18초에 빠진 뒤 새 내용이 나오게(겹쳐 보임 ✗) — 늦춤은 다음 1초에 걸쳐 0으로 */
    const P1 = kk > 0 ? SC[kk - 1] : null, soft1 = !!(P1 && /^(pstat|rf_card|speech)$/.test(s.type) && /^(pstat|rf_card|speech)$/.test(P1.type) && ((s._chain || s._keep) ? P1.type !== s.type : (photoSrc(s.img) && photoSrc(s.img) === photoSrc(P1.img) || s.name && s.name === P1.name && (s.type === 'speech') === (P1.type === 'speech'))));
    const lag = soft1 ? .18 * (1 - c01((t - start - .18) / 1.0)) : 0;
    if (lag > 0) { NOW = t - lag; lt = Math.max(0, lt - lag); }
    A.innerHTML = draw(kk, lt); NOW = t;
    /* 11/10 01:12 사용자 "전환 효과가 너무 정신사나워" + 01:24 "화면전환 효과가 하나만 있어서 지루해" → 차분한 전환 네 가지를 경계 성격에 따라 돌려 쓴다(0.45초 이하, 큰 색판·흔들림 ✗)
       line = 챕터가 바뀔 때 가는 금색 선이 지나가며 드러남 · zoom = 사람 장면으로 들어갈 때 살짝 다가옴 · push = 같은 챕터 다른 이야기는 옆으로 밀림 · up = 질문·숫자 띠는 아래에서 올라옴. 같은 종류가 연달아 나오면 다음 것으로 */
    const dt = t - start, kind = trKind(kk), TD = kind === 'line' ? .45 : .4, sameFrame = kk > 0 && s.type === 'rf_capbar' && SC[kk - 1].type === 'rf_capbar', P0 = kk > 0 ? SC[kk - 1] : null,
      samePer = !!(P0 && /^(pstat|rf_card|speech)$/.test(s.type) && /^(pstat|rf_card|speech)$/.test(P0.type) && (photoSrc(s.img) && photoSrc(s.img) === photoSrc(P0.img) || s.name && s.name === P0.name && (s.type === 'speech') === (P0.type === 'speech'))),
      duoC = !!(P0 && s.type === 'rf_duo' && P0.type === 'rf_duo' && (P0.cards || []).some((pc, i) => (s.cards || [])[i] && pc.img === s.cards[i].img && pc.name === s.cards[i].name && !(pc.at >= 50))),
      tr = kk > 0 && !(s._chain || s._keep || sameFrame || samePer || duoC) && dt >= 0 && dt < TD;   /* 같은 사람·같은 사진이면 화면 전환 없이 바뀐 내용만(10:19) */   /* 막대 → 막대는 전환 없이 그대로(01:26) */
    A.style.clipPath = 'none'; A.style.transform = ''; Bx.style.transform = ''; Bx.style.clipPath = 'none';
    if (EDGE.innerHTML) EDGE.innerHTML = '';
    if (tr) { NOW = BD[kk - 1] - 0.001; Bx.innerHTML = draw(kk - 1, endLt(kk - 1)); NOW = t; Bx.style.display = 'block';
      const p = dt / TD;
      if (kind === 'line') { const q = eio(p), X = q * FW;
        A.style.opacity = '1'; A.style.clipPath = `inset(0 ${(FW - X).toFixed(1)}px 0 0)`; Bx.style.opacity = '1'; Bx.style.clipPath = `inset(0 0 0 ${X.toFixed(1)}px)`;
        EDGE.innerHTML = `<div style="position:absolute;left:${(X - 2).toFixed(1)}px;top:0;width:4px;height:${FH}px;background:${GOLD};box-shadow:0 0 18px rgba(200,226,255,.6)"></div>`; }
      else { const o = 1 - ss(dt / .2), e = e4(c01(dt / TD));   /* 새 장면 판은 처음부터 보이고(칸·글이 자기 등장으로 나타남) 앞 장면만 0.2초에 빠짐 → 빈 화면 순간 없음 */
        Bx.style.opacity = (1 - ss(dt / .1)).toFixed(3); A.style.opacity = ss((dt - .1) / .15).toFixed(3);   /* 11/12 검수(F-206): 앞 장면이 0.1초에 다 빠진 뒤 새 장면이 0.1~0.25초에 들어옴 — 겹침 0 */
        if (kind === 'push') { Bx.style.transform = `translateX(${(-60 * ss(dt / .2)).toFixed(1)}px)`; A.style.transform = `translateX(${(60 * (1 - e)).toFixed(1)}px)`; }
        else if (kind === 'zoom') { Bx.style.transform = `scale(${(1 + .03 * ss(dt / .2)).toFixed(4)})`; A.style.transform = `scale(${(.97 + .03 * e).toFixed(4)})`; }
        else if (kind === 'up') { A.style.transform = `translateY(${(50 * (1 - e)).toFixed(1)}px)`; } } }
    else if (kk > 0 && ((s._chain || s._keep) && P0.type !== s.type || samePer && !(s._chain || s._keep)) && dt >= 0 && dt < .22) {   /* 같은 사진으로 이어지지만 장면 종류가 바뀌면 앞 장면 글·칸은 0.2초에 빠짐(툭 사라짐 ✗) — 사진 액자는 같은 자리라 그대로 */
      A.style.opacity = '1'; NOW = BD[kk - 1] - 0.001; Bx.innerHTML = draw(kk - 1, endLt(kk - 1)); NOW = t; Bx.style.display = 'block'; Bx.style.opacity = (1 - ss(dt / .2)).toFixed(3); }
    else { A.style.opacity = '1'; if (Bx.innerHTML) { Bx.innerHTML = ''; Bx.style.display = 'none'; } }
  }
  /* 원래 장면 함수 자리: #body 는 비우고 lt 만 기억(호흡 맞춤 lt 를 그대로 쓰려고) */
  if (MGON) Object.keys(R).forEach(ty => { SCENE[ty] = (lt, s) => { if (s && s._k != null && lt !== 99) LT[s._k] = lt; B(''); }; });
  return { post, R };
})();
