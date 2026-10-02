#!/usr/bin/env python3
"""누끼(배경 제거) — u2net ONNX(onnxruntime)로 알파 매트 생성. 사용: python3 tools/cutout.py in.jpg out.png [model]
10/1 밤: 썸네일 '선수만 딱' 용. 모델은 /tmp/claude-0/hw/u2net.onnx 또는 시스템\\models\\u2net.onnx"""
import sys, os, numpy as np
from PIL import Image, ImageFilter
import onnxruntime as ort
src, dst = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else next(p for p in ['/tmp/claude-0/hw/u2net.onnx', os.path.join(os.path.dirname(__file__), '..', 'models', 'u2net.onnx')] if os.path.exists(p))
im = Image.open(src).convert('RGB'); W, H = im.size
x = np.asarray(im.resize((320, 320), Image.LANCZOS)).astype(np.float32) / 255.0
x = (x - np.array([0.485, 0.456, 0.406], dtype=np.float32)) / np.array([0.229, 0.224, 0.225], dtype=np.float32)
x = x.transpose(2, 0, 1)[None]
sess = ort.InferenceSession(model, providers=['CPUExecutionProvider'])
out = sess.run(None, {sess.get_inputs()[0].name: x})[0][0][0]
out = (out - out.min()) / max(1e-6, out.max() - out.min())
m = Image.fromarray((out * 255).astype('uint8')).resize((W, H), Image.LANCZOS)
# 가장자리 살짝 다듬기: 반투명 띠를 줄이고 경계 부드럽게
a = np.asarray(m).astype(np.float32) / 255.0
a = np.clip((a - 0.15) / 0.7, 0, 1)
# 10/2: 320px 마스크를 그냥 키우면 경계가 뭉개져 '번져' 보임 → 원본 사진을 길잡이로 guided filter 로 경계를 실제 윤곽에 붙인다
try:
    import cv2
    g = np.asarray(im).astype(np.float32) / 255.0
    r = max(4, round(min(W, H) / 250))
    def gf(I, P, r, eps):   # 회색조 guided filter (He et al.)
        bf = lambda x: cv2.boxFilter(x, -1, (2 * r + 1, 2 * r + 1))
        mI, mP = bf(I), bf(P); cov = bf(I * P) - mI * mP; var = bf(I * I) - mI * mI
        A = cov / (var + eps); B = mP - A * mI
        return bf(A) * I + bf(B)
    a = gf(cv2.cvtColor(g, cv2.COLOR_RGB2GRAY), a.astype(np.float32), r, 1e-3)
    a = np.clip((a - 0.1) / 0.8, 0, 1)
    m = Image.fromarray((a * 255).astype('uint8'))
except Exception as e:
    print('guided filter 없음 → 예전 방식', e)
    m = Image.fromarray((a * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
rgba = im.convert('RGBA'); rgba.putalpha(m); rgba.save(dst)
print('ok', dst, im.size, 'fg%', round(float(a.mean()) * 100, 1))
