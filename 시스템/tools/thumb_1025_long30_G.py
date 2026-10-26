# 롱폼㉚ 썸네일 G — 1인(롯데 옷 합성) + 거대 '가을 / 야구' 글씨(R23), 로고 없음, 주아체 테두리 없음
import numpy as np, json, os, sys, cv2
from PIL import Image, ImageDraw, ImageFont
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
W, H = 2560, 1440
FONT = '/tmp/claude-0/-home-claude/a7d618fa-8384-52cc-a9a7-18438cf12374/scratchpad/fonts/Jua-Regular.ttf'
A = dict(hw=345, cx=1280, head_top=30, big_h=470, big_y=120, gap_c=430, t2c='255,212,0', bigc='228,0,43', bg='navy', out='vG',
         big_l='가을', big_r='야구', grade='color')
for kv in sys.argv[1:]:
    k, v = kv.split('=', 1); A[k] = type(A[k])(v)
col = lambda s: tuple(int(x) for x in s.split(','))

def text_img(t, size, fill, bold=0):
    f = ImageFont.truetype(FONT, size); b = f.getbbox(t, stroke_width=bold)
    im = Image.new('RGBA', (b[2] - b[0] + 60, b[3] - b[1] + 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((30 - b[0], 30 - b[1]), t, font=f, fill=fill, stroke_width=bold, stroke_fill=fill)
    return im.crop(im.getbbox())

def shade(can, im, xy, hard=12, hop=.6, blur=26, bop=.55):
    a = np.zeros((H, W), np.float32); x, y = xy; al = np.asarray(im)[..., 3].astype(np.float32) / 255
    y0, x0 = max(0, y), max(0, x); y1, x1 = min(H, y + im.height), min(W, x + im.width)
    a[y0:y1, x0:x1] = al[y0 - y:y1 - y, x0 - x:x1 - x]
    wide = cv2.GaussianBlur(np.roll(a, 10, 0), (0, 0), blur) * bop; hd = np.roll(a, hard, 0) * hop
    c = np.asarray(can).astype(np.float32); c[..., :3] *= (1 - wide[..., None]); c[..., :3] *= (1 - hd[..., None])
    can = Image.fromarray(c.astype(np.uint8)); can.alpha_composite(im, (x, y)); return can

# 배경: 남색 바탕, 가운데 위쪽 은은한 빛, 좌우 대칭
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W / 2) / 1500) ** 2 + ((yy - 420) / 800) ** 2); g = np.clip(1 - r, 0, 1) ** 1.4
if A['bg'] == 'navy': c0, c1 = np.array([5, 12, 32]), np.array([28, 58, 120])
else: c0, c1 = np.array([10, 10, 12]), np.array([60, 60, 66])
bg = c0 * (1 - g[..., None]) + c1 * g[..., None]
ang = np.arctan2(yy - 420, xx - W / 2)
bg += ((0.5 + 0.5 * np.cos(ang * 14)) ** 8 * np.clip(1 - r * .8, 0, 1) * .12)[..., None] * np.array([180, 210, 255])
bot = np.clip((yy - 860) / 580, 0, 1); bg = bg * (1 - .7 * bot[..., None])
bg += np.random.default_rng(5).normal(0, 2.2, bg.shape)
can = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert('RGBA')

# 거대 글씨: 머리 양옆 '가을' | '야구' (사람 뒤)
bc = col(A['bigc'])
BL = text_img(A['big_l'], 900, bc, bold=4); BR = text_img(A['big_r'], 900, bc, bold=4)
sc = A['big_h'] / max(BL.height, BR.height)
BL = BL.resize((int(BL.width * sc), int(BL.height * sc)), Image.LANCZOS); BR = BR.resize((int(BR.width * sc), int(BR.height * sc)), Image.LANCZOS)
gc = A['gap_c']  # 가운데 비우는 반폭
xl = W // 2 - gc - BL.width; xr = W // 2 + gc
can = shade(can, BL, (xl, A['big_y']), hard=14, hop=.45, blur=30, bop=.5)
can = shade(can, BR, (xr, A['big_y']), hard=14, hop=.45, blur=30, bop=.5)
big_boxes = [[xl, A['big_y'], xl + BL.width, A['big_y'] + BL.height], [xr, A['big_y'], xr + BR.width, A['big_y'] + BR.height]]

# 인물
CUT = Image.open('hf/cut_C.png').convert('RGBA'); HW0, HT0 = 389, 93
s = A['hw'] / HW0; pw, ph = int(CUT.width * s), int(CUT.height * s)
pa = np.asarray(CUT.resize((pw, ph), Image.LANCZOS)).astype(np.float32)
rgb = pa[..., :3] / 255; l = (rgb @ np.array([.3, .59, .11]))[..., None]
rgb = np.clip(l + (rgb - l) * 1.06, 0, 1); rgb = np.clip((rgb - .5) * 1.06 + .51, 0, 1)
pa[..., :3] = rgb * 255
x0 = A['cx'] - pw // 2; y0 = A['head_top'] - int(HT0 * s)
layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.paste(Image.fromarray(pa.astype(np.uint8)), (x0, y0))
Lp = np.asarray(layer).astype(np.float32); Al = Lp[..., 3] / 255
sh = cv2.GaussianBlur(Al, (0, 0), 26) * .6
c = np.asarray(can).astype(np.float32); c[..., :3] *= (1 - sh[..., None]); can = Image.fromarray(c.astype(np.uint8))
er = cv2.erode((Al > .5).astype(np.uint8), np.ones((9, 9), np.uint8)).astype(np.float32)
edge = np.clip(Al - cv2.GaussianBlur(er, (0, 0), 5), 0, 1) * .45 * np.clip(1 - (np.arange(H)[:, None] - 650) / 200, 0, 1)
Lp[..., :3] = Lp[..., :3] * (1 - edge[..., None]) + np.array([150, 190, 255]) * edge[..., None]
can.alpha_composite(Image.fromarray(np.clip(Lp, 0, 255).astype(np.uint8)))
os.makedirs(A['out'], exist_ok=True); Image.fromarray(np.asarray(layer)[..., 3]).save(f"{A['out']}/mask_이동욱.png")

# 제목(가운데, 아랫줄은 재생시간 자리 피해서 0.76W)
def line(t, fill, mw):
    im = text_img(t, 300, fill, bold=6); return im.resize((mw, int(im.height * mw / im.width)), Image.LANCZOS)
L1 = line('롯데 새 감독 이동욱', (255, 255, 255), int(.80 * W)); L2 = line('9년 탈락 끊을까?', col(A['t2c']), int(.76 * W))
y2 = 1418 - L2.height; y1 = y2 - 22 - L1.height
band = np.zeros((H, W), np.float32); band[y1 - 10:] = 1; band = cv2.GaussianBlur(band, (0, 0), 34) * .9
c = np.asarray(can).astype(np.float32); c[..., :3] *= (1 - band[..., None]); can = Image.fromarray(c.astype(np.uint8))
x1_, x2_ = (W - L1.width) // 2, (W - L2.width) // 2
can = shade(can, L1, (x1_, y1)); can = shade(can, L2, (x2_, y2))
out = can.convert('RGB'); out.save(f"{A['out']}/final.jpg", quality=93); out.resize((1280, 720), Image.LANCZOS).save(f"{A['out']}/final_1280.jpg", quality=92)
lay = dict(kind='long', title=[dict(text='롯데 새 감독 이동욱', box=[x1_, y1, x1_ + L1.width, y1 + L1.height]), dict(text='9년 탈락 끊을까?', box=[x2_, y2, x2_ + L2.width, y2 + L2.height])],
           sub=[], objects=dict(big=big_boxes),
           people=[dict(name='이동욱', mask=f"{A['out']}/mask_이동욱.png", z=1, row=0, side='C', kind='상반신(합성)', upscale=round(s, 3), head_w=A['hw'], hero=True, src='hf/cut_C.png')],
           meta=dict(structure='1인 + 거대 글씨 좌우(R23)', font='배민 주아체', color='남색+롯데 빨강 큰 글씨, 제목 흰/노랑', bg='남색 단색 빛'))
json.dump(lay, open(f"{A['out']}/layout.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('title top', round(y1 / H, 3), 'big', big_boxes, 'person', x0, y0, pw, ph)
