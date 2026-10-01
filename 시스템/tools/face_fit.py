#!/usr/bin/env python3
"""썸네일 cut5 용 선수 배치 계산 — 누끼 png 들의 얼굴 상자(OpenCV)를 재서 얼굴 높이·얼굴 중심 y 가 전부 같게 h/left/top 을 낸다.
사용: python3 tools/face_fit.py 누끼/권희동 누끼/레이예스_롯데 ... [--F 215] [--cy 255] [--W 1280]  → JSON 출력(콘티 thumb.faces 에 붙여 넣기)"""
import sys, os, json, cv2, numpy as np
from PIL import Image
args = [a for a in sys.argv[1:] if not a.startswith('--')]; opt = dict(a[2:].split('=') for a in sys.argv[1:] if a.startswith('--') and '=' in a)
F = float(opt.get('F', 215)); CY = float(opt.get('cy', 255)); W = float(opt.get('W', 1280))
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '선수이미지')
casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
out = []; slot = W / max(1, len(args))
for i, n in enumerate(args):
    p = next((os.path.join(base, n + e) for e in ('', '.png', '.jpg') if os.path.exists(os.path.join(base, n + e))), None)
    im = Image.open(p).convert('RGB'); g = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
    fs = sorted(casc.detectMultiScale(g, 1.1, 5, minSize=(60, 60)), key=lambda b: -b[2] * b[3])
    if not len(fs): print('얼굴 못 찾음', n, file=sys.stderr); x, y, w, h = 0, 0, im.size[0], im.size[1] * .35
    else: x, y, w, h = [int(v) for v in fs[0]]
    s = F / h; out.append({'img': n, 'h': round(im.size[1] * s), 'left': round(slot * (i + .5) - (x + w / 2) * s), 'top': round(CY - (y + h / 2) * s)})
print(json.dumps(out, ensure_ascii=False))
