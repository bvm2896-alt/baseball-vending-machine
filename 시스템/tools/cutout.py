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
# 10/12 사용자 "지운 다음 되살리지 말고 안 지우면 되잖아": 누끼는 바깥 배경만 뺀다.
#       인물 안쪽에 생긴 투명 구멍(헬멧 챙 밑·팔과 몸 사이 어두운 부분 등 — 바깥 배경과 이어지지 않은 투명 영역)은 지우지 않고 원본 픽셀 그대로 둔다.
#       바깥과 이어진 오목한 부분(챙 끝과 헬멧 사이 같은 진짜 배경)은 그대로 뺀다. 끄려면 --keep-holes
if '--keep-holes' not in sys.argv:
    try:
        import cv2
        am = np.asarray(m)
        fgm = (am > 128).astype(np.uint8)
        # 작은 틈(≤20px)으로만 바깥과 이어진 구멍도 '안쪽'으로 본다
        closed = cv2.morphologyEx(fgm, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
        bgm = (1 - closed).astype(np.uint8)
        nb, lab = cv2.connectedComponents(bgm, connectivity=4)
        border = set(np.unique(np.concatenate([lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]])))
        enc = np.isin(lab, [i for i in range(1, nb) if i not in border])
        # 닫힘 연산은 구멍 가장자리를 둥글게 깎으므로, 구멍마다 상자 안에서 '줄·칸의 인물 픽셀 사이' 투명 픽셀을 구멍으로 본다(실제 윤곽에 맞춤)
        holes = np.zeros_like(fgm, dtype=bool)
        ne, el = cv2.connectedComponents(enc.astype(np.uint8), connectivity=4)
        for k in range(1, ne):
            yy, xx = np.where(el == k); pad = 12
            y0, y1 = max(0, yy.min() - pad), min(fgm.shape[0] - 1, yy.max() + pad)
            x0, x1 = max(0, xx.min() - pad), min(fgm.shape[1] - 1, xx.max() + pad)
            sub = fgm[y0:y1 + 1, x0:x1 + 1]
            rowf = np.zeros_like(sub, dtype=bool); colf = np.zeros_like(sub, dtype=bool)
            for r in range(sub.shape[0]):
                w = np.where(sub[r])[0]
                if len(w) > 1: rowf[r, w.min():w.max() + 1] = sub[r, w.min():w.max() + 1] == 0
            for c in range(sub.shape[1]):
                w = np.where(sub[:, c])[0]
                if len(w) > 1: colf[w.min():w.max() + 1, c] = sub[w.min():w.max() + 1, c] == 0
            holes[y0:y1 + 1, x0:x1 + 1] |= rowf & colf
        if holes.any():
            am = np.where(holes, 255, am).astype(np.uint8)
            am = cv2.GaussianBlur(am, (0, 0), 0.5)
            m = Image.fromarray(am)
            print('안쪽 구멍', int(holes.sum()), 'px 는 지우지 않음')
    except Exception as e:
        print('구멍 보존 건너뜀', e)
# 10/12 사용자 "그대로 안 나온다": u2net 은 윤곽을 1~3px 깎고 어두운 부분(턱 밑 그늘·소매 끝)을 배경으로 지운다.
#       배경이 어두운 단색(야간 사진)이면 — 테두리 픽셀 밝기 중앙값 < 40 — 인물 윤곽을 10px 넓힌 띠 안에서
#       '배경보다 분명히 밝은 픽셀'은 전부 인물로 둔다(원본 그대로). 밝은 배경 사진은 건드리지 않는다.
if '--no-darkkey' not in sys.argv:
    try:
        import cv2
        rgb = np.asarray(im).astype(np.float32); lum = rgb.max(2)
        edge = np.concatenate([lum[0, :], lum[-1, :], lum[:, 0], lum[:, -1]])
        bgmed = float(np.median(edge))
        if bgmed < 40:
            am = np.asarray(m).astype(np.uint8)
            band = cv2.dilate((am > 128).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61))) > 0
            keep = band & (lum > bgmed + 10)
            keep = cv2.morphologyEx(keep.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
            am2 = np.where(keep, 255, am).astype(np.uint8)
            # 띠 안에서 배경(어두움)인데 u2net 이 반투명으로 남긴 가장자리는 배경 쪽으로 — 검은 테두리 방지
            dark = band & (lum <= bgmed + 6) & ~keep
            am2 = np.where(dark, np.minimum(am2, 0), am2).astype(np.uint8)
            # 10/12 사용자 "여기 안 건드리고 그대로": 인물 픽셀 사이에 낀 어두운 틈(헬멧 챙 밑면·뺨과 귀 덮개 사이, 40px 이하)은
            #       배경이 아니라 그늘진 인물 부분이다 → 줄 단위로 양쪽에 인물 픽셀이 있고 틈이 어두우면 전부 인물로 둔다
            fgb = am2 > 128; GAP = 40
            for r in range(fgb.shape[0]):
                w = np.where(fgb[r])[0]
                if len(w) < 2: continue
                gaps = np.where(np.diff(w) > 1)[0]
                for g in gaps:
                    a0, a1 = w[g] + 1, w[g + 1]
                    if a1 - a0 <= GAP and (lum[r, a0:a1] <= bgmed + 25).all():
                        am2[r, a0:a1] = 255
            am2 = cv2.GaussianBlur(am2, (0, 0), 0.6)
            m = Image.fromarray(am2)
            print('어두운 배경: 윤곽 띠 안 밝은 픽셀', int((keep & (am < 200)).sum()), 'px 되찾음')
    except Exception as e:
        print('어두운 배경 보정 건너뜀', e)
rgba = im.convert('RGBA'); rgba.putalpha(m); rgba.save(dst)
print('ok', dst, im.size, 'fg%', round(float(a.mean()) * 100, 1))
