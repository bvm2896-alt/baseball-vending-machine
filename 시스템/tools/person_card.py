#!/usr/bin/env python3
"""인물 카드 자르기 — 얼굴과 몸을 '함께' 보고 사람을 카드 가운데에 둔다(10/6 밤 사용자: "선수 사진은 얼굴, 몸 고려해서 가운데 맞추는 거 규칙에 넣어").
사용: python3 tools/person_card.py 입력 출력.jpg 비율(가로/세로, 예 0.85) [--top=0.06] [--zoom=1.0] [--mask=누끼.png]
- --cx=0.56: 손을 높이 든 사진처럼 '위 22% = 얼굴'이 틀리는 사진은 가운데(사진 폭 비율)를 직접 준다 — 얼굴과 몸통 사이 값으로, 결과를 눈으로 확인.
- --nobox=1: 방망이를 휘두른 사진처럼 몸 상자가 방망이에 끌릴 때 얼굴+몸통 평균만 쓴다.
- --nopad=1: 경기 사진은 절대 덧대지 않는다(가장자리가 어두워 단색으로 잘못 판정될 때).
- --mask: 이미 만든 누끼 png(같은 사진, 다른 사람을 지운 것)의 투명도를 사람 마스크로 쓴다(심판·동료가 붙어 있을 때).
- u2net 으로 가장 큰 사람 덩어리를 잡고 세 중심을 잰다: 얼굴(덩어리 위 22% 의 가운데) · 몸 상자(팔·손·방망이 포함 bbox 가운데) · 몸통(카드에 보이는 높이 안 사람 픽셀의 무게중심).
- 기준 = (얼굴 + 몸 상자 + 몸통) / 3. 얼굴만 가운데(몸이 한쪽으로 쏠림)도, 상자만 가운데(뻗은 팔에 끌려 얼굴이 쏠림)도 아니게.
- 카드 창이 사진 밖으로 나가면 그 쪽 가장자리 줄의 배경색을 늘려 덧댄다(자르지 않고 가운데를 지킨다).
- 결과 카드 안에서 세 중심이 각각 몇 % 어긋났는지 출력한다(±8% 안이면 통과)."""
import sys, os, numpy as np
from PIL import Image
import onnxruntime as ort, cv2
a = [x for x in sys.argv[1:] if not x.startswith('--')]
opt = {k: v for k, v in (x[2:].split('=', 1) for x in sys.argv[1:] if x.startswith('--'))}
mask_png = opt.pop('mask', None); opt = {k: float(v) for k, v in opt.items()}
src, dst, r = a[0], a[1], float(a[2]); topm = opt.get('top', 0.06); zoom = opt.get('zoom', 1.0)
model = next(p for p in ['/tmp/claude-0/hw/u2net.onnx', os.path.join(os.path.dirname(__file__), '..', 'models', 'u2net.onnx')] if os.path.exists(p))
im = Image.open(src).convert('RGB'); W, H = im.size
x = np.asarray(im.resize((320, 320), Image.LANCZOS)).astype(np.float32) / 255.0
x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).astype(np.float32).transpose(2, 0, 1)[None]
s = ort.InferenceSession(model, providers=['CPUExecutionProvider'])
o = s.run(None, {s.get_inputs()[0].name: x})[0][0][0]; o = (o - o.min()) / max(1e-6, o.max() - o.min())
m = (cv2.resize(o, (W, H)) > 0.5).astype(np.uint8)
if mask_png:
    mk = Image.open(mask_png).convert('RGBA')
    m = (np.asarray(mk.resize((W, H)))[:, :, 3] > 100).astype(np.uint8)
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])) if n > 1 else 0
m = (lab == k)
x0, y0, bw, bh = [int(v) for v in st[k, :4]]; x1, y1 = x0 + bw, y0 + bh
# 카드 크기: 사진 높이(위 여백 포함) 기준, zoom>1 이면 더 좁게(확대)
ch = min(H - max(0, y0 - topm * H), H) / zoom; cw = ch * r
_a = np.asarray(im); _k = max(4, W // 50)
uni = max(np.median(_a[:, :_k].std(axis=1).max(1)), np.median(_a[:, -_k:].std(axis=1).max(1))) <= 12 and not opt.get('nopad')   # --nopad=1: 경기 사진(어두운 배경이라 단색으로 잘못 잡힐 때)
if cw > W and not uni: cw = W; ch = cw / r   # 경기 사진은 덧대지 않고 높이를 줄인다(세로 사진 → 가로 카드)
T = int(round(max(0, y0 - topm * ch)))
if T + ch > H: T = int(H - ch)
vis = m[T:int(T + ch)]
ys, xs = np.where(m[y0:y0 + max(8, int(bh * 0.22))]); face = float(np.median(xs))
box = (x0 + x1) / 2
cols = vis.sum(0); torso = float((cols * np.arange(W)).sum() / max(1, cols.sum()))
cx = (face + box + torso) / 3
if opt.get('nobox'): cx = (face + torso) / 2   # --nobox=1: 방망이·뻗은 팔이 상자를 한쪽으로 끌 때(타격 폴로스루) 얼굴+몸통만
if 'cx' in opt: cx = opt['cx'] * W
L = int(round(cx - cw / 2)); Rr = L + int(round(cw))
arr = np.asarray(im)
pl, pr = max(0, -L), max(0, Rr - W)
if (pl or pr) and not uni:   # 경기 사진처럼 가장자리가 배경 단색이 아니면 덧대지 않는다(늘린 줄무늬가 보임) → 창을 사진 안으로 밀고 어긋남을 출력
    sh = pl - pr; L += sh; Rr += sh; pl = pr = 0
if pl or pr:   # 모자란 쪽은 가장자리 4px 띠의 줄별 중앙값 색으로 덧댐
    lc = np.median(arr[:, :4], axis=1).astype(np.uint8); rc = np.median(arr[:, -4:], axis=1).astype(np.uint8)
    arr = np.concatenate([np.repeat(lc[:, None], pl, 1), arr, np.repeat(rc[:, None], pr, 1)], 1)
    L += pl; Rr += pl
out = Image.fromarray(arr[T:int(T + ch), L:Rr])
out.save(dst, quality=94)
def off(v): return (v + pl - (L + (Rr - L) / 2)) / (Rr - L) * 100
print(f'{os.path.basename(src)} {W}x{H} → {out.size[0]}x{out.size[1]} | 카드 안 어긋남(+오른쪽): 얼굴 {off(face):+.1f}% · 몸상자 {off(box):+.1f}% · 몸통 {off(torso):+.1f}% · 덧댐 좌{pl} 우{pr}px'
      + (f' | 몸상자가 카드보다 넓음({bw}>{Rr-L})' if bw > Rr - L else ''))
