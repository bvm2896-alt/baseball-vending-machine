// 10/25 사용자 "줄바꿈 제대로 안 할래?"(곽빈·김주원 '내년 풀타임 = 첫 / 조건'): 장면 끝마다 <br> 없이 자동으로 접힌 글을 찾는다. 사용: node tools/wrap_check.js 미리보기.html
const path=require('path');const {chromium}=require('playwright');
(async()=>{const [src]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.resolve(src));await p.waitForTimeout(900);
const r=await p.evaluate(()=>{const out=[];const ends=[...BD,EP.total];
 for(let k=0;k<ends.length;k++){window.render(ends[k]-0.1);
  const w=document.createTreeWalker(document.getElementById('body'),NodeFilter.SHOW_TEXT);let n;
  while((n=w.nextNode())){const t=n.textContent.trim(); if(t.length<2) continue;
   const rg=document.createRange(); rg.selectNodeContents(n); const tops=new Set([...rg.getClientRects()].filter(r=>r.width>2).map(r=>Math.round(r.top/4)));
   if(tops.size>=2) out.push(k+' | '+tops.size+'줄 | '+t.slice(0,40));}
  /* 10/25 사용자 "첫 등판 원이 너무 영상 끝에 붙어 있어": 화면 가장자리 72px 안쪽(안전 영역)을 넘는 글·그림 */
  for(const e of document.querySelectorAll('#body *')){ if(e.children.length && !['svg','IMG'].includes(e.tagName)) continue; if(e.closest('svg') && e.tagName!=='svg') continue; const r=e.getBoundingClientRect(); if(r.width<4||r.height<4||r.width>1500) continue; const cs=getComputedStyle(e); if(+cs.opacity===0||cs.visibility==='hidden') continue;
   const bg=cs.backgroundColor!=='rgba(0, 0, 0, 0)'||e.textContent.trim()||['svg','IMG'].includes(e.tagName); if(!bg) continue;
   if(r.right>1920-72||r.left<72) out.push(k+' | 가장자리 | '+(e.textContent.trim().slice(0,30)||e.tagName)+' x '+Math.round(r.left)+'~'+Math.round(r.right));}}
 return out;});
console.log([...new Set(r)].join('\n')||'자동 줄바꿈 없음');await b.close();})();
