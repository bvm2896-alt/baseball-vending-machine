// 10/10 사용자 "텍스트가 그래프랑 겹치잖아" → 장면마다 끝 화면에서 글자 줄(한 줄씩)이 다른 글자·색칠된 상자와 겹치는지 자동으로 찾는다.
// node tools/overlap_check.js work/pv.html <장면수> [초/장면=4] [끝 오프셋=2.85]
const path = require('path');
const { chromium } = require(path.join(__dirname, '..', 'node_modules', 'playwright'));
(async () => {
  const [src, nArg, secArg, offArg] = process.argv.slice(2);
  const N = +nArg, SEC = +(secArg || 4), OFF = +(offArg || 2.85);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +(process.env.VW || 1920), height: +(process.env.VH || 1080) } /* 세로 컷: VW=1080 VH=1920 */ });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + path.resolve(src)); await p.waitForTimeout(800);
  let bad = 0;
  for (let i = 0; i < N; i++) {
    await p.evaluate(t => window.render(t), SEC * i + OFF); await p.waitForTimeout(30);
    const r = await p.evaluate(() => {
      const root = document.querySelector('#body') || document.body, out = [];
      const vis = el => { for (let e = el; e && e !== document.body; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity < .35) return false; } return true; };
      const lines = [], boxes = [];
      const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      for (let n; (n = tw.nextNode());) { if (!n.textContent.trim()) continue; const el = n.parentElement; if (!vis(el) || el.closest('svg')) continue;
        const rg = document.createRange(); rg.selectNodeContents(n);
        for (const q of rg.getClientRects()) if (q.width > 4 && q.height > 8) lines.push({ el, t: n.textContent.trim().slice(0, 18), r: { l: q.left + 2, t: q.top + q.height * .2, R: q.right - 2, B: q.bottom - q.height * .2 } }); }
      for (const el of root.querySelectorAll('*')) { const cs = getComputedStyle(el); const bg = cs.backgroundColor, hasBg = (bg && bg !== 'transparent' && !/rgba\(.*,\s*0\)$/.test(bg)) || (cs.backgroundImage !== 'none' && el.tagName !== 'DIV') || el.tagName === 'IMG';
        if (!hasBg || !vis(el)) continue; const q = el.getBoundingClientRect(); if (q.width < 6 || q.height < 6 || q.width > 1700) continue; boxes.push({ el, r: { l: q.left, t: q.top, R: q.right, B: q.bottom } }); }
      const ov = (a, c) => Math.max(0, Math.min(a.R, c.R) - Math.max(a.l, c.l)) * Math.max(0, Math.min(a.B, c.B) - Math.max(a.t, c.t));
      const area = a => (a.R - a.l) * (a.B - a.t);
      for (let x = 0; x < lines.length; x++) {
        const A = lines[x];
        for (let y = x + 1; y < lines.length; y++) { const C = lines[y]; if (A.el === C.el) { /* 같은 요소 안 줄끼리 */ if (ov(A.r, C.r) > .15 * Math.min(area(A.r), area(C.r))) out.push(`글자끼리: "${A.t}" / "${C.t}"`); continue; }
          if (ov(A.r, C.r) > .15 * Math.min(area(A.r), area(C.r))) out.push(`글자끼리: "${A.t}" / "${C.t}"`); }
        for (const Bx of boxes) { if (Bx.el.contains(A.el)) continue; /* 글자를 감싼 배지·카드는 괜찮음 */
          if (A.el.contains(Bx.el)) continue;
          // 상자가 글자보다 뒤에 깔린 배경(글자를 품은 카드의 형제 배경)인지: 상자가 글자 줄을 완전히 덮으면 배경으로 본다
          const o = ov(A.r, Bx.r), nm = `<${Bx.el.tagName.toLowerCase()} ${(Bx.el.className || '').toString().slice(0, 20)}>`;
          if (o > .12 * area(A.r) && o < .98 * area(A.r)) out.push(`글자-상자: "${A.t}" ↔ ${nm}`);
          else if (o >= .98 * area(A.r) && Bx.el.tagName !== 'IMG') { /* 상자 안에 완전히 들어간 글자: 글자색과 상자색이 비슷하면 안 보이는 것 */
            const rgb = s => (s.match(/[\d.]+/g) || []).slice(0, 3).map(Number), a = rgb(getComputedStyle(A.el).color), c = rgb(getComputedStyle(Bx.el).backgroundColor);
            if (a.length === 3 && c.length === 3 && Math.hypot(a[0] - c[0], a[1] - c[1], a[2] - c[2]) < 90) out.push(`글자가 같은 색 상자에 묻힘: "${A.t}" ↔ ${nm}`); }
          else if (o >= .98 * area(A.r) && Bx.el.tagName === 'IMG' && !Bx.el.closest('.lr > div:first-child')) {} }
      }
      /* 10/10: 화면이 통째로 줄어든 장면·너무 작은 글씨(사용자 화면에서 안 읽힘)도 같이 */
      for (const im of root.querySelectorAll('img')) { const q = im.getBoundingClientRect(); if (q.width > 30 && vis(im) && (q.left < 8 || q.right > innerWidth - 8)) { out.push(`사진이 화면 밖으로 ${Math.round(q.left)}~${Math.round(q.right)}`); break; } }
      for (const A of lines) if (A.r.l < 8 || A.r.R > innerWidth - 8) { out.push(`글자가 화면 밖: "${A.t}"`); break; }
      const sc = parseFloat((root.firstElementChild && root.firstElementChild.style.scale) || 1) || 1;
      if (sc < .97) out.push(`화면 통째 축소 ${sc.toFixed(2)}배`);
      for (const A of lines) { const fs = parseFloat(getComputedStyle(A.el).fontSize) * sc; if (fs < 26) { out.push(`작은 글씨 ${fs.toFixed(0)}px: "${A.t}"`); break; } }
      const mg = root.querySelector('.mega'); if (mg && parseFloat(getComputedStyle(mg).fontSize) < 80) out.push(`이름 작아짐 ${getComputedStyle(mg).fontSize}`);
      return [...new Set(out)].slice(0, 6);
    });
    if (r.length) { bad++; console.log(`장면 ${i}: ` + r.join(' | ')); }
  }
  console.log(`끝: 겹침 의심 ${bad}장면 / ${N}`);
  await b.close();
})();
