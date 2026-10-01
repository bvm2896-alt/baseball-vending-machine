const path=require('path'); const { chromium } = require(require('path').join(__dirname,'..','node_modules','playwright'));
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+path.resolve(process.argv[2])); await p.waitForTimeout(800);
for (const t of process.argv[3].split(',').map(Number)) {
  const r=await p.evaluate(t=>{window.render(t); const body=document.getElementById('body');
    let L=1e9,R=-1e9; const hits=[];
    body.querySelectorAll('*').forEach(e=>{const c=e.getBoundingClientRect(); if(c.width<2||c.height<2) return;
      const cs=getComputedStyle(e); if(cs.visibility==='hidden'||+cs.opacity<0.05) return;
      const ownText=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
      const vis = ownText || e.tagName==='IMG' || ['path','circle','rect','line','ellipse','polygon'].includes(e.tagName) || (cs.backgroundColor!=='rgba(0, 0, 0, 0)' && cs.backgroundColor!=='transparent' && c.width<1700) || (cs.borderStyle!=='none' && parseFloat(cs.borderWidth)>0 && c.width<1700);
      if(!vis) return;
      // 글자는 실제 글자 폭으로
      let l=c.left, r=c.right;
      if(ownText && !e.children.length){ const rg=document.createRange(); rg.selectNodeContents(e); const rr=rg.getBoundingClientRect(); l=rr.left; r=rr.right; }
      L=Math.min(L,l); R=Math.max(R,r);});
    return {L:Math.round(L),R:Math.round(R),center:Math.round((L+R)/2),off:Math.round((L+R)/2-960)};},t);
  console.log(t, JSON.stringify(r));
}
await b.close();})();
