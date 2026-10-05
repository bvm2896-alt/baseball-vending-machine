#!/usr/bin/env python3
"""카드용 사진 자르기 — 사람 '전체'(몸·팔·손·글러브)를 재서 카드 가운데에 둔다.
10/5 사용자: "얼굴만 가운데 놓고 가운데 정렬했다고 하지 말고 몸이나 손 등 사진 전체를 보고 가운데에 놓아라"
사용: python3 tools/card_crop.py 입력.jpg 출력.jpg 비율(가로/세로, 예 0.81) [위여백비율 0.05]
- u2net 마스크에서 가장 큰 사람 덩어리의 상자(bbox)를 잡고, 상자 폭이 다 들어가는 가장 작은 카드 비율 창을 상자 가운데에 맞춰 자른다.
- 상자가 사진 높이 때문에 다 안 들어가면(옆으로 긴 투구 자세 등) '잘림' 경고 → 그 사진은 세로 카드에 쓰지 않는다."""
import sys, os, numpy as np
from PIL import Image
import onnxruntime as ort, cv2
src, dst, r = sys.argv[1], sys.argv[2], float(sys.argv[3]); topm = float(sys.argv[4]) if len(sys.argv) > 4 else 0.05
model = next(p for p in ['/tmp/claude-0/hw/u2net.onnx', os.path.join(os.path.dirname(__file__), '..', 'models', 'u2net.onnx')] if os.path.exists(p))
im = Image.open(src).convert('RGB'); W, H = im.size
x = np.asarray(im.resize((320, 320), Image.LANCZOS)).astype(np.float32) / 255.0
x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).astype(np.float32).transpose(2, 0, 1)[None]
s = ort.InferenceSession(model, providers=['CPUExecutionProvider'])
o = s.run(None, {s.get_inputs()[0].name: x})[0][0][0]; o = (o - o.min()) / max(1e-6, o.max() - o.min())
m = (cv2.resize(o, (W, H)) > 0.5).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])) if n > 1 else 0
x0, y0, bw, bh = st[k, 0], st[k, 1], st[k, 2], st[k, 3]; x1, y1 = x0 + bw, y0 + bh
cw = min(W, bw * 1.10); ch = cw / r
cut = False
if ch > H: ch = H; cw = ch * r; cut = cw < bw * 1.0
cx = x0 + bw / 2
L = int(round(min(max(0, cx - cw / 2), W - cw))); T = int(round(min(max(0, y0 - topm * ch), H - ch)))
out = im.crop((L, T, L + int(cw), T + int(ch)))
out.save(dst, quality=93)
off = (cx - (L + cw / 2)) / cw * 100   # 사람 상자 가운데가 카드 가운데에서 몇 % 벗어났나(+ 오른쪽)
print(f'{os.path.basename(src)} 사람상자 x{x0}-{x1} y{y0}-{y1} ({bw}x{bh}) → 자름 {L},{T} {int(cw)}x{int(ch)} | 가운데 어긋남 {off:+.1f}% | 몸 잘림 {"예" if cut else "아니오"}')
