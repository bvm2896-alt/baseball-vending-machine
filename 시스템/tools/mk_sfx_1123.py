# 11/23 23:04 사용자 "엔딩 장면 너가 간단한 효과음 같은 것만 넣어줘" — 엔딩(테마 A) 움직임에 맞춘 짧은 효과음을 직접 합성(내려받은 소리 없음)
import numpy as np, wave, subprocess, sys
SR=44100; rng=np.random.default_rng(7)
def env(n,tau): return np.exp(-np.arange(n)/(tau*SR))
def tone(f,d,tau,a): n=int(d*SR); t=np.arange(n)/SR; return a*np.sin(2*np.pi*f*t)*env(n,tau)
def lp(x,k): return np.convolve(x,np.ones(k)/k,mode='same')
def tick(a=.10): n=int(.03*SR); x=rng.standard_normal(n)*env(n,.006); return a*(x-lp(x,12))
def click(a=.16): x=tone(1900,.05,.008,a); y=tone(170,.08,.02,a*1.2); z=np.zeros(max(len(x),len(y))); z[:len(x)]+=x; z[:len(y)]+=y; return z
def clink(a=.13):
    z=np.zeros(int(.5*SR))
    for off,g in ((0,1),(.075,.55)):
        for f,w in ((2637,1),(3951,.6),(5274,.3)):
            x=tone(f,.4,.07,a*g*w); i=int(off*SR); z[i:i+len(x)]+=x[:len(z)-i]
    return z
def thunk(a=.30):
    n=int(.3*SR); t=np.arange(n)/SR; f=110-45*np.minimum(1,t/.12); ph=2*np.pi*np.cumsum(f)/SR
    return a*np.sin(ph)*env(n,.06)+lp(rng.standard_normal(n),40)*env(n,.02)*a*.5
def whoosh(d=.4,a=.06): n=int(d*SR); x=lp(rng.standard_normal(n),18); x=x-lp(x,400); return a*x*np.hanning(n)*3
def ding(a=.15):
    z=np.zeros(int(1.2*SR))
    for f,w,tau in ((1568,1,.30),(2349,.55,.22),(3136,.25,.15)):
        x=tone(f,1.2,tau,a*w); z[:len(x)]+=x
    return z
def put(buf,t,x,g=1.0):
    i=int(t*SR); x=x[:max(0,len(buf)-i)]; buf[i:i+len(x)]+=x*g
def loop_cycle(buf,t0,g):
    put(buf,t0+.45,click(),g); put(buf,t0+1.28,thunk(),g*.8); put(buf,t0+2.6,whoosh(.5),g)
intro=np.zeros(int(12.0*SR)+SR)
put(intro,.10,whoosh(.5,.07))
for i in range(7): put(intro,1.30+i*.085,tick(),.9)
put(intro,3.10,clink()); put(intro,3.45,click()); put(intro,4.88,thunk()); put(intro,5.35,whoosh(.6,.08)); put(intro,6.0,ding())
loop_cycle(intro,8.0,.7)
loop=np.zeros(int(16.0*SR)+SR)
for c in range(4): loop_cycle(loop,c*4.0,.55)
for nm,x,d in (('intro',intro,None),('loop',loop,None)):
    x=np.clip(x,-.9,.9); w=wave.open(nm+'.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
E='/mnt/user-data/outputs/kia23/sys/'
for nm in ('intro','loop'):
    src=E+f'endcard_{nm}.mp4'; d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src],capture_output=True,text=True).stdout)
    r=subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-i',nm+'.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-ar','44100','-ac','1','-t',f'{d:.3f}','-movflags','+faststart',f'endcard_{nm}.mp4'],capture_output=True,text=True)
    print(nm,d,r.returncode,r.stderr[-200:])
