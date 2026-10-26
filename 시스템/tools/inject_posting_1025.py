# 10/25 롱폼㉙ 검수 — 사용자 "이 부분 카드와 텍스트로 떼우지 말고 인포그래픽, 모션그래픽, 애니메이션 이런걸 활용해서 직관적이고 이해가 잘되게"
# 포스팅 절차 장면(SCENE.posting)을 template_long.html 의 function render 앞에 넣는다. 다시 돌리면 예전 블록을 바꿔 끼운다.
import re, sys, io
BLOCK = r'''/* @@POST1025 포스팅 절차 모션 그래픽(10/25 롱폼㉙ 「다음 메이저리거」) — tools/inject_posting_1025.py 가 넣는다(이 파일을 고치면 다시 주입)
   {type:'posting', step:1~6, chain, cont, team(원래 구단, 없으면 KBO), deal:'SD'(계약하는 구단 칸)}
   step 1 신청(11/1~12/5) · 2 사무국 → 30개 구단 공시 · 3 30일 협상(시계) · 4 계약 → 이적료가 원래 구단으로 · 5 이적료 = 보장 금액에 따라 · 6 못 하면 복귀
   각 요소는 자기 step 장면에서만 움직이고, 뒤 장면에선 다 그려진 채로 남는다(이어지는 장면은 새 요소만 움직인다) */
(function () {
  const LOGOI = (n, px, st = '') => { const c_ = (T(n) || {}).code, kb = c_ === 'KBO';   /* 10/25 KBO 공식 로고(엠블럼 + KBO, 가로 2.47:1 — 사용자가 보낸 공식 로고)는 넓게 */
    return `<img src="${LOGO[c_] || ''}" style="width:${kb ? Math.round(px * 1.85) : px}px;height:${kb ? Math.round(px * .75) : px}px;object-fit:contain;display:block;${st}">`; };
  const cl = (v, a, b) => Math.max(a, Math.min(b, v)), e3 = x => 1 - Math.pow(1 - cl(x, 0, 1), 3);
  const TT = (s, k) => { const segs = (EP.segT || [])[s.startLine] || []; if (!segs.length) return null;
    const i = Math.floor(k), f = k - i, t0 = segs[i] ?? segs[segs.length - 1], t1 = segs[i + 1] ?? (t0 + 1.5);
    const d = NOW - (t0 + (t1 - t0) * f); return d < 0 ? null : d; };
  const MLB30 = [['ARI', '#A71930'], ['ATL', '#CE1141'], ['BAL', '#DF4601'], ['BOS', '#BD3039'], ['CHC', '#0E3386'], ['CWS', '#27251F'],
    ['CIN', '#C6011F'], ['CLE', '#00385D'], ['COL', '#33006F'], ['DET', '#0C2340'], ['HOU', '#EB6E1F'], ['KC', '#004687'],
    ['LAA', '#BA0021'], ['LAD', '#005A9C'], ['MIA', '#00A3E0'], ['MIL', '#12284B'], ['MIN', '#002B5C'], ['NYM', '#FF5910'],
    ['NYY', '#132448'], ['ATH', '#003831'], ['PHI', '#E81828'], ['PIT', '#27251F'], ['SD', '#2F241D'], ['SF', '#FD5A1E'],
    ['SEA', '#0C2C56'], ['STL', '#C41E3A'], ['TB', '#092C5C'], ['TEX', '#003278'], ['TOR', '#134A8E'], ['WSH', '#AB0003']];
  const W = 1728, H = 640;
  /* 칸 좌표 */
  const LP = { x: 10, y: 70, w: 340, h: 470 };            /* 원래 구단(KBO) */
  const MB = { x: 520, y: 40, w: 290, h: 200 };           /* 메이저리그 사무국 */
  const RC = { cx: 665, cy: 450, r: 92 };                 /* 30일 시계 */
  const GD = { x: 990, y: 40, cols: 6, cell: 118, d: 92 }; /* 30개 구단 */
  const dotC = i => ({ x: GD.x + (i % GD.cols) * GD.cell + GD.cell / 2, y: GD.y + Math.floor(i / GD.cols) * 106 + 53 });
  SCENE.posting = (lt, s) => {
    const st = s.step || 1;
    /* A(step, 호흡, 걸리는 초): 이 요소가 얼마나 그려졌나(0~1). 앞 step 에서 이미 나온 건 1, 뒤 step 것은 0 */
    const A = (step, k, d = .6) => { if (st > step) return 1; if (st < step) return 0; if (k != null && k < 0) return 1; const t = TT(s, k); return t == null ? 0 : cl(t / (d * SPD), 0, 1); };
    const dealI = Math.max(0, MLB30.findIndex(x => x[0] === (s.deal || 'SD')));
    /* 10/25 검수(계약선이 다른 구단 원·'30개 구단 모두와 협상' 글자를 지나감): 계약 구단을 셋째 줄 맨 왼쪽 칸(12번)에 놓아 선수 → 계약 구단 선이 아무것도 안 지나가게 — 자리만 바꾸고 차례(불 켜지는 순서)는 그대로 */
    const DS = 12, dc = i => dotC(i === dealI ? DS : i === DS ? dealI : i);
    const fail = A(6, 0, .6);                                  /* 6: 못 하면 — 계약 길은 흐려진다 */
    /* 1 신청 */
    const pIn = A(1, 0, .5), cal = A(1, 0.2, 1.6), docFly = A(2, 0, .9);
    /* 2 공시 */
    const mbIn = A(1, 0, .5), mbHot = A(2, 1, .5), wave = A(2, 2, 1.2), stamp = A(2, 3, .45);   /* 10/25 검수: '30개' 말할 때 30개 다 켜지게(1.8 → 1.2초) */
    /* 3 협상 */
    const ringIn = A(3, 2, .5), ringRun = A(3, 2.3, 2.6), talk = A(3, 1, .7);
    /* 4 계약·이적료 */
    const deal = A(4, 0, .5), money = A(4, 2, 1.2);
    /* 5 계산 */
    const calc = A(5, 1, .6), later = A(5, 3, .5);
    /* 6 복귀 */
    const back = A(6, 0.3, 1.0);
    const ringDays = st >= 6 ? Math.round(18 * (1 - e3(A(6, 0, 1.4)))) : Math.round(30 - 12 * e3(ringRun));   /* 30일 → (협상 중) 18일 남음 → 6: 0일 */
    const dim = x => `opacity:${(x).toFixed(3)}`;
    let svg = '';
    /* 신청서가 선수 → 사무국으로 날아간다 */
    if (docFly > 0 && docFly < 1) { const x0 = LP.x + LP.w - 20, y0 = LP.y + 200, x1 = MB.x + 30, y1 = MB.y + 110, q = e3(docFly);
      const x = x0 + (x1 - x0) * q, y = y0 + (y1 - y0) * q - Math.sin(q * Math.PI) * 80;
      svg += `<g transform="translate(${x} ${y})"><rect x="-26" y="-34" width="52" height="68" rx="6" fill="#fff" stroke="#2F6BFF" stroke-width="4"/><path d="M-14,-14 h28 M-14,0 h28 M-14,14 h18" stroke="#2F6BFF" stroke-width="4"/></g>`; }
    /* 사무국 → 30개 구단 전파(공시) */
    if (wave > 0) for (let w = 0; w < 3; w++) { const q = cl(wave * 1.6 - w * .3, 0, 1); if (q <= 0 || q >= 1 && st > 2) continue;
      const r = 60 + q * 520; svg += `<circle cx="${MB.x + MB.w / 2}" cy="${MB.y + MB.h / 2}" r="${r}" fill="none" stroke="#2F6BFF" stroke-width="${6 - 4 * q}" opacity="${(1 - q) * .55}"/>`; }
    /* 협상: 선수 ↔ 30개 구단 */
    if (talk > 0) { const y = LP.y + 250, op = talk * (1 - .75 * fail) * (1 - e3(deal));   /* 10/25: 계약이 되면 협상 줄·글은 완전히 사라진다(계약선이 그 위를 지나가지 않게) */
      svg += `<line x1="${LP.x + LP.w + 10}" y1="${y}" x2="${GD.x - 20}" y2="${y}" stroke="#2F6BFF" stroke-width="7" stroke-dasharray="18 14" stroke-dashoffset="${-(NOW * 60) % 64}" opacity="${op}"/>
        <path d="M${GD.x - 20},${y} l-22,-14 v28 z M${LP.x + LP.w + 10},${y} l22,-14 v28 z" fill="#2F6BFF" opacity="${op}"/>`; }
    /* 계약: 선수 ─ 계약 구단 실선 */
    /* 10/25 검수: 계약선이 사무국 상자·다른 구단 글자를 지나가던 것 → 사무국 아래(y 300)로 지나가 SD 원 왼쪽 끝에서 멈춤, 실패(6)면 지움 */
    if (deal > 0 && fail < 1) { const c = dc(dealI), x0 = LP.x + LP.w + 10, y0 = LP.y + 262, x1 = c.x - GD.d / 2 - 10, y1 = c.y, op = 1 - fail;
      const mx = (x0 + x1) / 2, B = t => { const u = 1 - t; return [u*u*u*x0 + 3*u*u*t*mx + 3*u*t*t*mx + t*t*t*x1, u*u*u*y0 + 3*u*u*t*y0 + 3*u*t*t*y1 + t*t*t*y1]; };
      const q = e3(deal), N = 24; let d_ = `M${x0},${y0}`; for (let k = 1; k <= N; k++) { const [x, y] = B(q * k / N); d_ += ` L${x.toFixed(1)},${y.toFixed(1)}`; }
      svg += `<path d="${d_}" fill="none" stroke="#1F9D55" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="${op}"/>`; }
    /* 이적료: 계약 구단 → 원래 구단으로 돈이 날아간다 */
    if (money > 0 && st >= 4) { const c = dc(dealI), tx = LP.x + LP.w / 2, ty = LP.y - 30;
      for (let b = 0; b < 5; b++) { const q = cl(money * 1.5 - b * .12, 0, 1); if (q <= 0) continue; if (q >= 1 && st > 4) continue;
        const e = e3(q), x = c.x + (tx - c.x) * e, y = c.y + (ty - c.y) * e - Math.sin(e * Math.PI) * 160;
        svg += `<g transform="translate(${x} ${y}) rotate(${-12 + b * 6})" opacity="${q >= 1 ? 0 : 1 - .75 * fail}"><rect x="-34" y="-20" width="68" height="40" rx="6" fill="#1F9D55" stroke="#fff" stroke-width="3"/><circle r="11" fill="#fff"/><text y="6" text-anchor="middle" font-size="16" font-weight="900" fill="#1F9D55">$</text></g>`; } }
    /* 6: 못 하면 원래 구단으로 */
    if (back > 0) { const x0 = GD.x - 30, y0 = LP.y + 420, x1 = LP.x + LP.w + 20, y1 = LP.y + 420, q = e3(back);
      svg += `<path d="M${x0},${y0} Q${(x0 + x1) / 2},${y0 + 70} ${x0 + (x1 - x0) * q},${y0 + (y1 - y0) * q}" fill="none" stroke="#E5484D" stroke-width="9" stroke-linecap="round"/>`
        + (q > .95 ? `<path d="M${x1},${y1} l26,-18 v36 z" fill="#E5484D"/>` : ''); }
    /* 30일 시계 */
    const ring = ringIn > 0 ? (() => { const frac = ringDays / 30, C = 2 * Math.PI * RC.r, red = st >= 6;
      return `<g opacity="${ringIn}"><circle cx="${RC.cx}" cy="${RC.cy}" r="${RC.r}" fill="#fff" stroke="#E3E8F0" stroke-width="18"/>
        <circle cx="${RC.cx}" cy="${RC.cy}" r="${RC.r}" fill="none" stroke="${red ? '#E5484D' : '#2F6BFF'}" stroke-width="18" stroke-linecap="round" stroke-dasharray="${(C * frac).toFixed(1)} ${C}" transform="rotate(-90 ${RC.cx} ${RC.cy})"/>
        <text x="${RC.cx}" y="${RC.cy + 6}" text-anchor="middle" font-size="64" font-weight="900" fill="${red ? '#E5484D' : '#12161F'}" font-family="inherit">${ringDays}</text>
        <text x="${RC.cx}" y="${RC.cy + 46}" text-anchor="middle" font-size="30" font-weight="900" fill="#6A7382" font-family="inherit">일 남음</text></g>`; })() : '';
    /* HTML 칸들 */
    const box = (b, inner, st_) => `<div style="position:absolute;left:${b.x}px;top:${b.y}px;width:${b.w}px;height:${b.h}px;${st_}">${inner}</div>`;
    const person = c => `<svg viewBox="0 0 40 60" width="120" height="150"><circle cx="20" cy="11" r="9" fill="${c}"/><path d="M6,58 L6,32 Q6,22 20,22 Q34,22 34,32 L34,58 Z" fill="${c}"/></svg>`;
    const leftIn = e3(pIn), ret = A(6, 1.0, .4);   /* 10/25 사용자 "원래 구단 복귀가 0.1초도 안 있다가 지나가" — '원래 구단으로' 말할 때 뜨고 다음 장면은 늦게(ENTER) */
    const left = box(LP, `<div class="col" style="width:100%;height:100%;box-sizing:border-box;border-radius:30px;background:#fff;box-shadow:0 18px 40px rgba(18,22,31,.12);align-items:center;justify-content:flex-start;padding-top:22px;gap:6px;border:5px solid ${ret > 0 ? '#E5484D' : '#fff'}">
        <div class="row" style="gap:10px;align-items:center">${LOGOI(s.team || 'KBO', 64)}</div>
        <div style="margin-top:4px">${person('#2B3445')}</div><b style="font-size:38px;font-weight:900">선수</b>
        <div style="margin-top:10px;width:300px;${dim(cl(cal * 3, 0, 1))}"><div style="text-align:center;font-size:36px;font-weight:900;color:#2F6BFF;white-space:nowrap">11/1 ~ 12/5</div>
          <div style="height:16px;border-radius:8px;background:#E3E8F0;overflow:hidden;margin-top:6px"><div style="height:100%;width:${(100 * e3(cal)).toFixed(1)}%;background:#2F6BFF;border-radius:8px"></div></div></div>
        ${money > 0 && st < 6 ? `<div style="position:absolute;right:-40px;top:-46px;background:#1F9D55;color:#fff;border-radius:22px;padding:6px 18px;font-size:32px;font-weight:900;white-space:nowrap;transform:scale(${(.7 + .3 * e3(cl((money - .6) / .4, 0, 1))).toFixed(3)});opacity:${cl((money - .6) / .4, 0, 1).toFixed(3)}">+ 이적료</div>` : ''}
        ${ret > 0 ? `<div style="position:absolute;left:50%;top:-58px;z-index:5;transform:translateX(-50%) scale(${(.7 + .3 * e3(ret)).toFixed(3)});opacity:${ret.toFixed(3)};background:#E5484D;color:#fff;border-radius:22px;padding:6px 20px;font-size:32px;font-weight:900;white-space:nowrap">↩ 원래 구단 복귀</div>` : ''}
      </div>`, `opacity:${c01(pIn * 1.4)};transform:translateY(${((1 - leftIn) * 40).toFixed(1)}px)`);
    const mbI = e3(mbIn);
    const mlb = box(MB, `<div class="col" style="width:100%;height:100%;box-sizing:border-box;border-radius:30px;background:#0F1626;align-items:center;justify-content:center;gap:10px;box-shadow:0 0 ${(40 * mbHot * (st === 2 ? 1 : 0)).toFixed(0)}px rgba(47,107,255,.8),0 18px 40px rgba(18,22,31,.2);position:relative">
        ${LOGOI('MLB', 96)}<b style="font-size:34px;font-weight:900;color:#fff;white-space:nowrap">메이저리그 사무국</b>
        ${stamp > 0 ? `<div style="position:absolute;right:-34px;top:-30px;border:6px solid #E5484D;color:#E5484D;background:#fff;border-radius:16px;padding:2px 18px;font-size:48px;font-weight:900;white-space:nowrap;transform:rotate(-8deg) scale(${(1.5 - .5 * e3(stamp)).toFixed(3)});opacity:${c01(stamp * 2).toFixed(3)}">공시</div>` : ''}
      </div>`, `opacity:${c01(mbIn * 1.4)};transform:translateY(${((1 - mbI) * 40).toFixed(1)}px)`);
    /* 30개 구단 칸: 공시 때 차례로 켜진다 */
    const lit = st > 2 ? 30 : st < 2 ? 0 : Math.floor(30 * e3(cl(wave * 1.15, 0, 1)) + 1e-6);
    let dots = '';
    MLB30.forEach(([ab, col], i) => { const c = dc(i), on = i < lit, isDeal = i === dealI && deal > 0, gone = fail > 0;
      const bg = on ? (gone ? '#C9D0DA' : col) : '#E3E8F0', fg = on ? '#fff' : '#9AA6B8';
      const sc = on && st === 2 ? 1 + .18 * Math.max(0, 1 - (lit - i) / 4) : isDeal && st === 4 ? 1 + .15 * e3(deal) : 1;
      /* 10/25 검수(SD 테두리가 글자를 가려 'CD'처럼 · '계약' 꼬리표가 MIN 아래): 계약 구단은 초록 원 + 흰 틈 + 바깥 테두리, 나머지 구단은 흐리게 · 꼬리표는 계약선 위 빈 곳에 */
      const dimO = deal > 0 && !isDeal && !gone && st >= 4 && st < 6 ? 1 - .6 * e3(deal) : 1;
      dots += `<div style="position:absolute;left:${c.x - GD.d / 2}px;top:${c.y - GD.d / 2}px;width:${GD.d}px;height:${GD.d}px;border-radius:50%;background:${isDeal && !gone ? '#1F9D55' : bg};color:${isDeal && !gone ? '#fff' : fg};display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:900;letter-spacing:-1px;opacity:${dimO.toFixed(3)};transform:scale(${sc.toFixed(3)});${isDeal && !gone ? 'box-shadow:0 0 0 5px #fff,0 0 0 11px #1F9D55;z-index:2;' : ''}">${isDeal && !gone ? ab : ''}</div>`;   /* 10/25 규칙 검수(영어 약어 30개): 구단 원은 색만, 계약 구단만 글자 */
      if (isDeal && !gone) dots += `<div style="position:absolute;left:${(LP.x + LP.w + c.x - GD.d / 2) / 2 - 230}px;top:${LP.y + 188}px;width:460px;text-align:center;opacity:${deal.toFixed(3)}"><span style="background:#1F9D55;color:#fff;border-radius:18px;padding:4px 18px;font-size:34px;font-weight:900;white-space:nowrap">${s.dealName || '샌디에이고'} 계약</span><span style="margin-left:10px;font-size:30px;font-weight:900;color:#6A7382;white-space:nowrap">예시</span></div>`; });
    const gIn = A(2, 1.6, .5);
    const glab = `<div style="position:absolute;left:${GD.x}px;top:${GD.y + 5 * 106 + 6}px;width:${GD.cols * GD.cell}px;text-align:center;font-size:36px;font-weight:900;opacity:${gIn.toFixed(3)}">메이저리그 <span class="num" style="color:#2F6BFF">${lit}</span>개 구단</div>`;
    const tlab = '';   /* 10/25 검수: '30개 구단 모두와 협상' 은 나레이션 되풀이 → 양쪽 화살표만 */
    const calcBox = '';   /* 10/25 검수: '이적료 = 보장 금액에 따라' 는 나레이션 되풀이 → 뺌 */
    const failLab = back > 0 ? `<div style="position:absolute;left:${LP.x + LP.w + 80}px;top:${LP.y + 498}px;width:${GD.x - LP.x - LP.w - 160}px;text-align:center;opacity:${e3(back).toFixed(3)}"><span style="background:#E5484D;color:#fff;border-radius:18px;padding:4px 18px;font-size:30px;font-weight:900;white-space:nowrap">30일 안에 계약 ✕</span></div>` : '';
    const title = s.title ? `<div class="title" style="font-size:52px;font-weight:900;text-align:center;margin-bottom:14px;${s._same || s._chain ? '' : pop(seg(lt, 0, .4))}">${esc(s.title)}</div>` : '';
    B(`<div class="col" style="align-items:center;width:100%">${title}<div style="position:relative;width:${W}px;height:${H}px;flex:0 0 auto">
      ${left}${mlb}${dots}${glab}${tlab}${calcBox}${failLab}
      <svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" style="position:absolute;left:0;top:0;overflow:visible;pointer-events:none">${svg}${ring}</svg></div></div>`);
  };
  Object.assign(MOTION, { posting: () => 1 });
})();
/* @@POST1025END */
'''
for p in sys.argv[1:]:
    s = io.open(p, encoding='utf-8').read()
    s = re.sub(r'/\* @@POST1025 .*?/\* @@POST1025END \*/\n', '', s, flags=re.S)
    i = s.index('function render(t) {')
    s = s[:i] + BLOCK + s[i:]
    io.open(p, 'w', encoding='utf-8').write(s); print('injected', p)
