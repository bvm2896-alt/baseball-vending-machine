#!/usr/bin/env python3
"""누끼(배경 제거) — ISNet(isnet-general-use.onnx) 1024px. 10/21 골든글러브 컷 썸네일(디아즈) 때 씀. tools/cutout.py(u2net 320px)보다 경계가 깨끗하다.
사용: python3 tools/isnet_cutout.py 원본.jpg 출력.png
모델(178MB, 깃에 안 올림): 아래 경로 중 하나에 둔다. 없으면 클라우드에서
  curl -sSL -o ~/.u2net/isnet-general-use.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx
  (GitHub 은 클라우드 프록시에서 받아진다. huggingface 는 막혀 있음)
쓰기 전 반드시: 원본 옆에 놓고 헬멧·귀덮개·손·목을 4배 확대해서 본다(스킬 yagu-poster-thumbnail 6-0). 옆 사람 손·팔이 반투명으로 남으면 그 사진은 버리는 게 낫다."""
import sys, os, numpy as np, onnxruntime as ort
from PIL import Image
CANDS = [os.path.expanduser('~/.u2net/isnet-general-use.onnx'), os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'isnet-general-use.onnx')]
MODEL = next((p for p in CANDS if os.path.exists(p)), None)
if not MODEL: sys.exit('모델 없음: ' + ' 또는 '.join(CANDS))
S = ort.InferenceSession(MODEL, providers=['CPUExecutionProvider'])
def mask(im):
    im = im.convert('RGB'); W, H = im.size
    x = np.asarray(im.resize((1024, 1024), Image.LANCZOS)).astype(np.float32) / 255. - 0.5
    o = S.run(None, {S.get_inputs()[0].name: x.transpose(2, 0, 1)[None]})[0][0, 0]
    o = (o - o.min()) / (o.max() - o.min() + 1e-8)
    return Image.fromarray((o * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    im = Image.open(src).convert('RGB'); r = im.copy(); r.putalpha(mask(im)); r.save(out); print(out, im.size)
