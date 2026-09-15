// 썸네일 렌더: node thumb.js render_thumb.html out/2026-09-03_thumb.jpg
const {chromium}=require('playwright'); const path=require('path');
(async()=>{ const src=process.argv[2], out=process.argv[3];
  const opts={}; if(process.env.CHROME_PATH) opts.executablePath=process.env.CHROME_PATH;
  const b=await chromium.launch(opts); const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.resolve(src)); await p.waitForTimeout(700);
  await p.screenshot({path:path.resolve(out),type:'jpeg',quality:90}); await b.close(); console.log(out); })();
