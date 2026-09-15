// 썸네일 렌더: node thumb.js render_thumb.html out/2026-09-03_thumb.jpg
const {chromium}=require('playwright'); const path=require('path');
(async()=>{ const src=process.argv[2], out=process.argv[3];
  const opts={}; if(process.env.CHROME_PATH) opts.executablePath=process.env.CHROME_PATH;
  const b=await chromium.launch(opts); const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+path.resolve(src)); await p.waitForTimeout(400);
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));   // 큰 로고(webp 2500px)가 다 그려진 뒤 찍는다(9/16)
  await p.waitForTimeout(300);
  await p.screenshot({path:path.resolve(out),type:'jpeg',quality:90}); await b.close(); console.log(out); })();
