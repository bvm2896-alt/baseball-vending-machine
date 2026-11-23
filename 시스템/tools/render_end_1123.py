# 엔딩 A(자판기) 본 화질 렌더: 0~12초(도입) + 12~28초(되풀이 16초) → 2560x1440 60fps
from playwright.sync_api import sync_playwright
import os,subprocess,sys
out='/home/claude/kia23/ending'; fd=out+'/fr'; os.makedirs(fd,exist_ok=True)
FPS=60; N=28*FPS
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=2560/1920)
    p.goto(f'file://{out}/pv.html?theme=A'); p.wait_for_function('window.__ready===true',timeout=20000)
    for i in range(N):
        f=f'{fd}/{i:05d}.jpg'
        if os.path.exists(f): continue
        p.evaluate('t=>window.render(t)',i/FPS); p.screenshot(path=f,type='jpeg',quality=96)
        if i%240==0: print(i,flush=True)
    b.close()
enc=['-c:v','libx264','-profile:v','high','-pix_fmt','yuv420p','-crf','14','-preset','medium','-g','120','-movflags','+faststart']
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-start_number','0','-i',fd+'/%05d.jpg','-frames:v',str(12*FPS),*enc,out+'/endcard_intro.mp4'],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-start_number',str(12*FPS),'-i',fd+'/%05d.jpg','-frames:v',str(16*FPS),*enc,out+'/endcard_loop.mp4'],check=True)
print('done')
