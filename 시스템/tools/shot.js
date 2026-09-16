// 미리보기 html 의 장면을 png 로: node tools/shot.js work/preview.html 0,2,5 work/pv
// 세 번째 인자 = 줄 번호들(각 줄의 0.95초 시점을 찍음), 네 번째 = 출력 접두(pv_0.png …)
const path = require('path');
const { chromium } = require(path.join(__dirname, '..', 'node_modules', 'playwright'));
(async () => {
  const [src, linesArg, prefix] = process.argv.slice(2);
  const lines = (linesArg || '0').split(',').map(Number);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + path.resolve(src)); await p.waitForTimeout(800);
  for (const n of lines) {
    await p.evaluate(t => window.render(t), n + 0.95); await p.waitForTimeout(100);
    await p.screenshot({ path: `${prefix || 'pv'}_${n}.png` }); console.log('shot', n);
  }
  await b.close();
})();
