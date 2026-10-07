// 썸네일 렌더: node thumb.js render_thumb.html out/2026-09-03_thumb.jpg
const {chromium}=require('playwright'); const path=require('path');
(async()=>{ const src=process.argv[2], out=process.argv[3];
  const opts={}; if(process.env.CHROME_PATH) opts.executablePath=process.env.CHROME_PATH;
  const W=parseInt(process.env.THUMB_W||'1080',10), H=parseInt(process.env.THUMB_H||'1920',10);   // 롱폼 썸네일은 1280x720 (build.py 가 환경변수로 준다, 9/18)
  const b=await chromium.launch(opts); const p=await b.newPage({viewport:{width:W,height:H}});
  await p.goto('file://'+path.resolve(src)); await p.waitForTimeout(400);
  await p.waitForFunction(()=>!window.__thumbAsync||window.__thumbDone,null,{timeout:15000}).catch(()=>console.log('경고: 썸네일 글씨 맞춤이 15초 안에 안 끝남'));   // 10/7: 세로 썸네일은 폰트를 다 불러온 뒤 글씨 크기를 정한다(보이는 칸 x 75~1005)
  const rep=await p.evaluate(()=>window.__thumbReport||''); if(rep) console.log('썸네일 글씨(잉크 x, 보이는 칸 75~1005): '+rep);
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>{}))));   // 큰 로고(webp 2500px)가 다 그려진 뒤 찍는다(9/16)
  await p.waitForTimeout(300);
  await p.screenshot({path:path.resolve(out),type:'jpeg',quality:90}); await b.close(); console.log(out); })();
