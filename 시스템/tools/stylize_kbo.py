#!/usr/bin/env python3
"""누끼(RGBA png)에 'KBO 2026 홍보 이미지' 느낌의 보정 — 10/4 밤 사용자 레퍼런스(신한 SOL KBO 리그 배너).
느낌: 강한 국부 대비(HDR/clarity) + 디테일 선명 + 채도 약간 낮춤 + 그림자는 푸른 톤·밝은 곳은 중립 + S 커브.
사용: python3 tools/stylize_kbo.py in.png out.png [strength 0~1, 기본 1]"""
import sys, numpy as np, cv2
from PIL import Image

def stylize(im, k=1.0):
    im = im.convert('RGBA'); a = np.asarray(im)[:, :, 3]
    rgb = np.asarray(im.convert('RGB')).astype(np.float32) / 255.0
    bgr = cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
    # 1) 국부 대비(CLAHE on L)
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB); L, A, B = cv2.split(lab)
    L2 = cv2.createCLAHE(clipLimit=2.0 + 1.0 * k, tileGridSize=(8, 8)).apply(L)
    L = cv2.addWeighted(L, 1 - 0.7 * k, L2, 0.7 * k, 0)
    lab = cv2.merge([L, A, B]); bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    f = bgr.astype(np.float32) / 255.0
    # 2) clarity(큰 반경 하이패스) + 3) 미세 선명
    blur = cv2.GaussianBlur(f, (0, 0), 8); f = np.clip(f + 0.55 * k * (f - blur), 0, 1)
    blur = cv2.GaussianBlur(f, (0, 0), 1.2); f = np.clip(f + 0.5 * k * (f - blur), 0, 1)
    # 4) 채도 ↓ + 그림자 푸른 톤(split toning)
    hsv = cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= (1 - 0.18 * k); f = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0
    lum = (0.114 * f[:, :, 0] + 0.587 * f[:, :, 1] + 0.299 * f[:, :, 2])[:, :, None]
    shadow = np.clip(1 - lum * 1.6, 0, 1)                     # 어두운 곳일수록 1
    tint = np.array([0.10, 0.02, -0.06], dtype=np.float32)    # BGR: 파랑 +, 빨강 -
    f = np.clip(f + shadow * tint * k, 0, 1)
    # 5) S 커브
    x = np.linspace(0, 1, 256, dtype=np.float32); s = 1 / (1 + np.exp(-(x - 0.5) * 7.0)); s = (s - s.min()) / (s.max() - s.min())
    lut = (x * (1 - 0.6 * k) + s * 0.6 * k)
    f = lut[(np.clip(f, 0, 1) * 255).astype(np.uint8)]
    out = cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_BGR2RGB)
    return Image.merge('RGBA', (*Image.fromarray(out).split(), Image.fromarray(a)))

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]; k = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    stylize(Image.open(src), k).save(dst); print(dst)
