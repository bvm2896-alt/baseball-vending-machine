// 프레임 렌더: render.html 을 15fps 로 JPEG 저장.  node frames.js <총길이초>
const {chromium}=require('playwright');
const path=require('path'); const fs=require('fs');
(async()=>{ const FPS=15, DUR=parseFloat(process.argv[2]||'45');
  const opts={}; if(process.env.CHROME_PATH) opts.executablePath=process.env.CHROME_PATH;
  const b=await chromium.launch(opts);
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+path.join(__dirname,'work','render.html')); await p.waitForTimeout(900);
  const n=Math.ceil(FPS*DUR);
  for(let i=0;i<n;i++){ await p.evaluate(t=>window.render(t), i/FPS);
    await p.screenshot({path:path.join(__dirname,'work','frames',`f${String(i).padStart(4,'0')}.jpg`),type:'jpeg',quality:88});}
  await b.close(); console.log('frames', n); })();
