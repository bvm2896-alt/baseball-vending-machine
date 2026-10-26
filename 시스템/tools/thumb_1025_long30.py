# 롱폼㉚ 썸네일 v2 — R26 숫자 앞 + R3 불빛, 이동욱 상체 크게, 제목 하단 2줄
import numpy as np, json, os, sys, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
W, H = 2560, 1440
FD = '/mnt/user-data/uploads/야구자판기/폰트/'
FONT = FD + 'Jalnan2.ttf'
A = dict(hw=440, cx=1280, head_top=42, nine_h=820, nine_x=250, nine_y=150, logo_w=700, logo_cx=2080, logo_cy=640,
         t1='롯데 새 감독 이동욱', t2='9년 탈락 끊을까?', tw=0.835, t_left=0.04, gap=24, t_bottom=1418)
for kv in sys.argv[1:]:
    k, v = kv.split('='); A[k] = type(A[k])(v)

# ---------- 배경: 남색 → 가운데 빨강 불빛 + 빛줄기
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
navy = np.array([8, 18, 44], np.float32); red = np.array([200, 16, 46], np.float32)
r = np.sqrt(((xx - W / 2) / 1700) ** 2 + ((yy - 520) / 900) ** 2)
g = np.clip(1 - r, 0, 1) ** 1.6
bg = navy * (1 - g[..., None]) + red * g[..., None]
ang = np.arctan2(yy - 520, xx - W / 2)
rays = (0.5 + 0.5 * np.cos(ang * 18)) ** 6 * np.clip(1 - r * 0.7, 0, 1) * 0.26
bg = bg + rays[..., None] * np.array([255, 120, 120])
bot = np.clip((yy - 880) / 560, 0, 1) ** 1.2
bg = bg * (1 - 0.75 * bot[..., None]) + np.array([4, 8, 22]) * 0.75 * bot[..., None]
vig = np.clip(np.sqrt(((xx - W / 2) / W) ** 2 * 2.2 + ((yy - H / 2) / H) ** 2 * 1.2), 0, 1)
bg = bg * (1 - 0.30 * vig[..., None] ** 2)
rng = np.random.default_rng(3); bg += rng.normal(0, 3.0, bg.shape)
can = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert('RGBA'); os.makedirs('v2', exist_ok=True); can.convert('RGB').save('v2/bg_only.jpg')

# ---------- 인물 (이동욱 상반신 누끼)
cut = Image.open('ldw_cut.png').convert('RGBA')
HEAD_W0, HEAD_TOP0 = 510, 90; s = A['hw'] / HEAD_W0
pw, ph = int(cut.width * s), int(cut.height * s)
pim = cut.resize((pw, ph), Image.LANCZOS)
pa = np.asarray(pim).astype(np.float32)
# 살짝 보정: 대비·채도 소폭, 그림자 남색
rgb = pa[..., :3] / 255; l = (rgb @ np.array([.3, .59, .11]))[..., None]
rgb = np.clip(l + (rgb - l) * 1.08, 0, 1); rgb = np.clip((rgb - .5) * 1.06 + .5 + .01, 0, 1)
pa[..., :3] = rgb * 255
x0 = A['cx'] - pw // 2; y0 = A['head_top'] - int(HEAD_TOP0 * s)
layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.paste(Image.fromarray(pa.astype(np.uint8)), (x0, y0))
Lp = np.asarray(layer).astype(np.float32); Al = Lp[..., 3] / 255
# 뒤 그림자(후광 위 깊이)
sh = cv2.GaussianBlur(Al, (0, 0), 22) * 0.55
c = np.asarray(can).astype(np.float32); c[..., :3] *= (1 - sh[..., None]); can = Image.fromarray(c.astype(np.uint8))
# 림라이트(빨강·위쪽 가장자리)
er = cv2.erode((Al > .5).astype(np.uint8), np.ones((9, 9), np.uint8)).astype(np.float32)
edge = np.clip(Al - cv2.GaussianBlur(er, (0, 0), 5), 0, 1) * 0.55
Lp[..., :3] = Lp[..., :3] * (1 - edge[..., None]) + np.array([255, 120, 110]) * edge[..., None]
layer = Image.fromarray(np.clip(Lp, 0, 255).astype(np.uint8))
can.alpha_composite(layer)
os.makedirs('v2', exist_ok=True)
pm = Image.fromarray((Al * 255).astype(np.uint8)); pm.save('v2/mask_이동욱.png')

# ---------- 앞 오브젝트: 왼쪽 큰 '9' (어깨 잘린 끝을 덮음), 오른쪽 롯데 로고
def text_img(t, size, fill, stroke=0, sfill=(255, 255, 255), font=FONT):
    f = ImageFont.truetype(font, size)
    b = f.getbbox(t, stroke_width=stroke)
    im = Image.new('RGBA', (b[2] - b[0] + 40, b[3] - b[1] + 40), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - b[0], 20 - b[1]), t, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return im.crop(im.getbbox())

def with_shadow(im, off=(18, 22), blur=16, op=.6, depth=0, dcol=(120, 6, 24)):
    pad = 60 + depth
    out = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = np.asarray(im)[..., 3]
    shimg = Image.new('RGBA', out.size, (0, 0, 0, 0)); sa = np.zeros(out.size[::-1], np.uint8)
    sa[pad + off[1]:pad + off[1] + im.height, pad + off[0]:pad + off[0] + im.width] = a
    sa = cv2.GaussianBlur(sa.astype(np.float32), (0, 0), blur) * op
    shimg = Image.fromarray(np.dstack([np.zeros_like(sa)] * 3 + [sa]).astype(np.uint8)); out.alpha_composite(shimg)
    for d in range(depth, 0, -2):  # 3D 두께
        solid = Image.new('RGBA', im.size, dcol + (255,)); solid.putalpha(im.getchannel('A'))
        out.alpha_composite(solid, (pad + d, pad + d))
    out.alpha_composite(im, (pad, pad)); return out, pad

nine = text_img('9', 1000, (226, 0, 43), stroke=22, sfill=(255, 255, 255))
nine = nine.resize((int(nine.width * A['nine_h'] / nine.height), A['nine_h']), Image.LANCZOS)
n3, pad = with_shadow(nine, depth=26)
can.alpha_composite(n3, (A['nine_x'] - pad, A['nine_y'] - pad))
nine_box = [A['nine_x'], A['nine_y'], A['nine_x'] + nine.width, A['nine_y'] + nine.height]

logo = Image.open('/home/claude/pc/KBO_logos/롯데.webp').convert('RGBA')
lw = A['logo_w']; logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
l3, pad = with_shadow(logo, depth=0)
lx, ly = A['logo_cx'] - logo.width // 2, A['logo_cy'] - logo.height // 2
can.alpha_composite(l3, (lx - pad, ly - pad))
logo_box = [lx, ly, lx + logo.width, ly + logo.height]

# ---------- 제목 2줄 (하단, 좌측 정렬 안전 영역 안)
maxw = int(A['tw'] * W); xl = int(A['t_left'] * W)
def line(t, fill):
    im = text_img(t, 300, fill, stroke=14, sfill=(10, 14, 30))
    return im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
L2 = line(A['t2'], (255, 214, 0)); L1 = line(A['t1'], (255, 255, 255))
# 두 줄 폭 같게 맞추면 높이가 달라짐 → 줄 높이 0.15H 이상 확인
y2 = A['t_bottom'] - L2.height; y1 = y2 - A['gap'] - L1.height
# 제목 뒤 어두운 띠(글씨 대비)
band = np.zeros((H, W), np.float32); band[y1 + 30:] = 1; band = cv2.GaussianBlur(band, (0, 0), 50) * 0.72
c = np.asarray(can).astype(np.float32); c[..., :3] *= (1 - band[..., None]); can = Image.fromarray(c.astype(np.uint8))
for im, y in ((L1, y1), (L2, y2)):
    sd, pad = with_shadow(im, off=(10, 14), blur=12, op=.75)
    can.alpha_composite(sd, (xl - pad, y - pad))
out = can.convert('RGB'); out.save('v2/final.jpg', quality=93)
obj = np.zeros((H, W), np.uint8)
om = Image.new('L', (W, H), 0)
for im_, (ox, oy) in ((nine, (A['nine_x'], A['nine_y'])), (logo, (lx, ly))):
    om.paste(im_.getchannel('A'), (ox, oy), im_.getchannel('A'))
om.save('v2/mask_objects.png')

out.resize((1280, 720), Image.LANCZOS).save('v2/final_1280.jpg', quality=92)
lay = dict(kind='long',
           title=[dict(text=A['t1'], box=[xl, y1, xl + L1.width, y1 + L1.height]), dict(text=A['t2'], box=[xl, y2, xl + L2.width, y2 + L2.height])],
           sub=[], objects=dict(nine=nine_box, logo=logo_box), objects_mask='v2/mask_objects.png',
           people=[dict(name='이동욱', mask='v2/mask_이동욱.png', z=1, row=0, side='C', kind='상반신(미디어)', upscale=round(s, 3),
                        head_w=A['hw'], hero=True, src='선수이미지/누끼/경기_이동욱_상반신_2020_스포츠경향.png')],
           meta=dict(structure='R26 숫자 앞 + R3 불빛(1인 상체)', font='Jalnan2', color='남색+롯데 빨강, 제목 흰/노랑', bg='남색→빨강 방사 빛줄기', lookOut=False))
json.dump(lay, open('v2/layout.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('title lines h', L1.height / H, L2.height / H, 'top', y1 / H, 'scale', s, 'person', x0, y0, pw, ph)
