// 10/10 사용자 "이미지가 다음 장면과 같으면 그대로 있고 텍스트만 자연스럽게" → 이어지는 두 장면에서 같은 사진·같은 이름·같은 카드 글자가 움직이면 찾는다.
// node tools/continuity_check.js work/pv.html <장면수> [초/장면=4]
const path = require('path');
const { chromium } = require(path.join(__dirname, '..', 'node_modules', 'playwright'));
(async () => {
  const [src, nArg, secArg] = process.argv.slice(2); const N = +nArg, SEC = +(secArg || 4);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +(process.env.VW || 1920), height: +(process.env.VH || 1080) } /* 세로 컷: VW=1080 VH=1920 */ });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + path.resolve(src)); await p.waitForTimeout(800);
  const snap = async t => { await p.evaluate(t => window.render(t), t); await p.waitForTimeout(20);
    return p.evaluate(() => { const o = {}; const root = document.querySelector('#body'); if (!root) return o;
      const op = el => { let a = 1; for (let e = el; e && e !== document.body; e = e.parentElement) { const c = getComputedStyle(e); if (c.visibility === 'hidden') return 0; a *= +c.opacity; } return a; };
      root.querySelectorAll('img').forEach(im => { const r = im.getBoundingClientRect(); if (r.width < 40 || op(im) < .9) return; const k = 'img:' + im.src.length + ':' + im.src.slice(-40); (o[k] = o[k] || []).push([r.left, r.top, r.width, r.height]); });
      root.querySelectorAll('.mega, .num, .title, .label, .badge').forEach(el => { if (el.children.length || op(el) < .9) return; const t = el.textContent.trim(); if (!t) return; const r = el.getBoundingClientRect(); const k = 'txt:' + t; (o[k] = o[k] || []).push([r.left, r.top, r.width, r.height]); });
      return o; }); };
  let bad = 0, prev = await snap(2.85);
  for (let i = 1; i < N; i++) {
    const st0 = await snap(SEC * i + 0.25), cur = await snap(SEC * i + 2.85), msgs = [];
    /* 앞 장면 끝에 있던 사진·글자가 이번 장면 시작에서 사라졌다가(다시 뜨는 중) 끝에는 같은 자리에 있으면 = 다시 뜨는 애니메이션 */
    for (const k in cur) if (prev[k] && !st0[k] && prev[k].length === 1 && cur[k].length === 1) msgs.push(`다시 뜸 ${k.startsWith('img') ? '사진' : '"' + k.slice(4, 20) + '"'}`);
    for (const k in cur) { if (!prev[k] || prev[k].length !== 1 || cur[k].length !== 1) continue;
      const [a] = prev[k], [c] = cur[k], d = Math.max(Math.abs(a[0] - c[0]), Math.abs(a[1] - c[1]), Math.abs(a[2] - c[2]), Math.abs(a[3] - c[3]));
      if (d > 6) msgs.push(`${k.startsWith('img') ? '사진' : '"' + k.slice(4, 20) + '"'} ${d.toFixed(0)}px`); }
    if (msgs.length) { bad++; console.log(`장면 ${i - 1}→${i}: ` + msgs.slice(0, 5).join(' | ')); }
    prev = cur;
  }
  console.log(`끝: 움직임 의심 ${bad}곳`); await b.close();
})();
