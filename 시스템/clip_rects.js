// 11/8 영상 장면(bt_clip) 자리 재기: node clip_rects.js <render.html> <times.json> <out.json>
//   times.json = [초, ...] → out.json = [[x, y, w, h, clip] 또는 null, ...] (CSS px, 화면 1920x1080 기준)
const path = require('path'); const fs = require('fs'); const { chromium } = require('playwright');
(async () => {
  const [, , html, timesF, outF] = process.argv;
  const CW = parseInt(process.env.FRAME_W || '1920', 10), CH = parseInt(process.env.FRAME_H || '1080', 10);
  const o = {}; if (process.env.CHROME_PATH) o.executablePath = process.env.CHROME_PATH;
  if (process.env.FRAME_NO_GPU === '1') o.args = ['--disable-gpu', '--disable-gpu-compositing'];
  const b = await chromium.launch(o); const p = await b.newPage({ viewport: { width: CW, height: CH } });
  await p.goto('file://' + path.resolve(html)); await p.waitForTimeout(500);
  await p.waitForFunction(() => window.__ready !== false, null, { timeout: 15000 }).catch(() => {});
  const ts = JSON.parse(fs.readFileSync(timesF, 'utf-8')); const res = [];
  for (const t of ts) {
    await p.evaluate(t => window.render(t), t);
    res.push(await p.evaluate(() => { const e = document.getElementById('clipbox'); if (!e) return null; const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height, e.dataset.clip]; }));
  }
  fs.writeFileSync(outF, JSON.stringify(res)); await b.close();
})().catch(e => { console.error(e); process.exit(1); });
