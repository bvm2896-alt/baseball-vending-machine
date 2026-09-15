// 미리보기: node shot.js 12.5 [out.png]  → 해당 초의 화면 한 장
const {chromium}=require('playwright'); const path=require('path');
(async()=>{ const t=parseFloat(process.argv[2]||'0'); const out=process.argv[3]||'preview.png';
  const opts={}; if(process.env.CHROME_PATH) opts.executablePath=process.env.CHROME_PATH;
  const b=await chromium.launch(opts); const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.join(__dirname,'work','render.html')); await p.waitForTimeout(900);
  await p.evaluate(t=>window.render(t), t);
  await p.screenshot({path:path.join(__dirname,out)}); await b.close(); console.log(out); })();
