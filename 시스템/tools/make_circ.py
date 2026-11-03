import onnxruntime as ort, numpy as np, sys, os
from PIL import Image
sess=ort.InferenceSession('/home/claude/models/u2net_human_seg.onnx',providers=['CPUExecutionProvider'])
iname=sess.get_inputs()[0].name
def mask_of(im):
    x=im.convert('RGB').resize((320,320),Image.LANCZOS); a=np.asarray(x).astype(np.float32)/255.
    a=(a-[0.485,0.456,0.406])/[0.229,0.224,0.225]; a=a.transpose(2,0,1)[None].astype(np.float32)
    m=sess.run(None,{iname:a})[0][0,0]; m=(m-m.min())/(m.max()-m.min()+1e-6)
    return np.asarray(Image.fromarray((m*255).astype(np.uint8)).resize(im.size,Image.LANCZOS)).astype(np.float32)/255.
def make(src,dst,size=500,k=2.7,top=0.12):
    im=Image.open(src).convert('RGB'); W,H=im.size; m=mask_of(im)
    rows=np.where((m>.5).sum(1)>max(3,W*0.01))[0]; ht=rows[0]
    band=[r for r in range(ht+int(H*0.05),ht+int(H*0.12)) if r<H]
    ws=[];cs=[]
    for r in band:
        c=np.where(m[r]>.5)[0]
        if len(c): ws.append(c[-1]-c[0]); cs.append((c[0]+c[-1])/2)
    hw=float(np.median(ws)); cx=float(np.median(cs))
    S=int(k*hw); L=int(cx-S/2); T=int(ht-top*S)
    a=np.asarray(im).astype(np.float32); mm=m[...,None]
    white=np.full_like(a,255.); comp=a*mm+white*(1-mm)
    canvas=np.full((S,S,3),255.,np.float32)
    x0,y0=max(0,L),max(0,T); x1,y1=min(W,L+S),min(H,T+S)
    canvas[y0-T:y1-T,x0-L:x1-L]=comp[y0:y1,x0:x1]
    out=Image.fromarray(canvas.clip(0,255).astype(np.uint8)).resize((size,size),Image.LANCZOS)
    out.save(dst,quality=93); return (W,H,ht,hw,cx,S)
if __name__=='__main__':
    for s,d in zip(sys.argv[1::2],sys.argv[2::2]): print(os.path.basename(d),make(s,d))
