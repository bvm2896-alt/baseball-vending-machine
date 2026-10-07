/* @@SAFEZONE 10/7 — 쇼츠 목록(격자) 칸에서 실제로 보이는 영역 안에 글씨를 최대로(사용자 "썸네일 텍스트가 살짝 짤리는데 이 안에서 텍스트 최대화")
   실측(10/7 채널 Shorts 탭 캡처 1179x2556, 업로드한 썸네일 3장을 칸에 맞춰 대조, 일치도 0.98): 칸은 썸네일을 0.403배로 그려
   1080x1920 중 x 55~1025 · y 151~1769 만 보인다(좌우 55px · 위아래 151px 잘림). 아래는 '조회수' 글자 때문에 1560(SAFE_BOTTOM).
   글씨는 여기서 20px 더 안쪽(x 75~1005, 폭 930)에 '잉크(실제 글자 획)' 기준으로 넣는다.
   또 하나: 템플릿 스크립트가 도는 순간엔 KBO 폰트가 아직 안 불려 와서(document.fonts.check = false) 대체 폰트 폭으로 크기를 정했고,
   실제 폰트로 그리면 폭이 달라져 넘쳤다(클라우드 ① 썸네일 box 80~1036). → 폰트를 다 불러온 뒤에 크기를 정한다(TS.ready). */
const TS=(()=>{
  const VIS={L:55,R:1025,T:151,B:1769}, PAD=20, L=VIS.L+PAD, R=VIS.R-PAD, W=R-L;
  const cx=document.createElement('canvas').getContext('2d');
  function ink(sp){   // 한 줄(span)의 실제 글자 획 왼쪽·오른쪽 끝(화면 px)
    const cs=getComputedStyle(sp), b=sp.getBoundingClientRect();
    cx.font=`${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    cx.letterSpacing=(cs.letterSpacing==='normal')?'0px':cs.letterSpacing;
    const m=cx.measureText(sp.textContent), sw=(parseFloat(cs.webkitTextStrokeWidth)||0)/2;
    const ow=sp.offsetWidth||b.width||1, k=b.width/ow||1;   // 부모 transform(scale) 반영
    const l=b.left+(-m.actualBoundingBoxLeft-sw)*k, r=b.left+(m.actualBoundingBoxRight+sw)*k;
    return {l,r,w:r-l};
  }
  const fs=sp=>parseFloat(getComputedStyle(sp).fontSize);
  const setF=(sp,f)=>{sp.style.fontSize=f.toFixed(1)+'px';};
  function fitW(sp,target,maxF){   // 잉크 폭이 target 이 되는 글자 크기(넘지 않게)
    target=Math.min(target||W,W);
    for(let i=0;i<8;i++){ const w=ink(sp).w; if(w<=0) return; const f=Math.min(maxF||9999,fs(sp)*target/w); setF(sp,f); if(Math.abs(ink(sp).w-target)<1.5) break; }
    for(let i=0;i<60&&ink(sp).w>target;i++) setF(sp,fs(sp)-1);
  }
  function capW(sp,target){ target=Math.min(target||W,W); for(let i=0;i<8&&ink(sp).w>target;i++) setF(sp,fs(sp)*target/ink(sp).w*0.998); }
  function minL(sps){ return Math.min(...sps.map(sp=>ink(sp).l)); }
  function clamp(sps){   // 10/7 사용자 "다 잘리는 건 아니고 잘리는 썸네일만" → 보이는 칸(75~1005) 밖으로 나가는 줄만 고친다. 안 나가는 줄은 그대로.
    let n=0;
    for(const sp of sps){ if(!sp.textContent.trim()) continue; let i=ink(sp);
      if(i.l<L){ const cur=parseFloat(sp.style.left)||0; if(getComputedStyle(sp).position==='static') sp.style.position='relative'; sp.style.left=(cur+L-i.l).toFixed(1)+'px'; i=ink(sp); n++; }
      for(let k=0;k<80&&i.r>R;k++){ setF(sp,fs(sp)*0.995); i=ink(sp); if(k===0) n++; } }   // 왼쪽 끝은 그대로 두고 그 줄만 오른쪽 끝이 1005 안에 들 때까지 줄인다
    return n;
  }
  function ready(){ return Promise.all([...document.fonts].map(f=>f.load().catch(()=>{}))).then(()=>document.fonts.ready); }
  function fitBottom(e,sps,B){ B=B||1560; for(let i=0;i<40&&e&&e.getBoundingClientRect().bottom>B;i++){ for(const sp of sps) if(sp.style.fontSize) setF(sp,fs(sp)*0.97); if(parseFloat(getComputedStyle(e).fontSize)>2) setF(e,fs(e)*0.97); } }   // 아래 '조회수' 글자(1588~)에 안 가리게
  function report(sps){ return sps.filter(sp=>sp.textContent.trim()).map(sp=>{const i=ink(sp);return `${sp.textContent} ${Math.round(i.l)}~${Math.round(i.r)}`;}).join(' / '); }
  return {VIS,L,R,W,B:1560,ink,fitW,capW,minL,clamp,fitBottom,ready,report};
})();
window.__thumbAsync=true;
