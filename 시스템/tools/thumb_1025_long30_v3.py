# 롱폼㉚ 썸네일 v3 여러 안 — 9 없음, 롯데 로고는 배경, 폰트·색 변경
import numpy as np, json, os, sys, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
W, H = 2560, 1440
FD = '/mnt/user-data/uploads/야구자판기/폰트/'
F = dict(noto=FD + 'NotoSansKR-Black.otf', gmarket=FD + 'GmarketSansBold.ttf', jalnan=FD + 'Jalnan2.ttf', kbo=FD + 'KBO Dia Gothic_bold.ttf')
FD2 = '/tmp/claude-0/-home-claude/a7d618fa-8384-52cc-a9a7-18438cf12374/scratchpad/fonts/'
F.update(wanted=FD2+'WantedSans-ExtraBlack.otf', gothica1=FD2+'GothicA1-Black.ttf', dohyeon=FD2+'DoHyeon-Regular.ttf', myeongjo=FD2+'NanumMyeongjo-ExtraBold.ttf', songmyung=FD2+'SongMyung-Regular.ttf', gugi=FD2+'Gugi-Regular.ttf', hahmlet=FD2+'Hahmlet-Black.ttf', jua=FD2+'Jua-Regular.ttf', plex=FD2+'IBMPlexSansKR-Bold.ttf')
LOGO = Image.open('/home/claude/pc/KBO_logos/롯데.webp').convert('RGBA')
CUTF = os.environ.get('CUTF', 'ldw_cut_ext.png'); CUT = Image.open(CUTF).convert('RGBA')
HEAD_W0, HEAD_TOP0, CUTL, CUTR = 510, 90, 965, 1029
if 'HEAD' in os.environ: HEAD_W0, HEAD_TOP0 = map(int, os.environ['HEAD'].split(','))
OUT = os.environ.get('OUT', 'v3'); HWO = int(os.environ.get('HW', '0')); CXO = int(os.environ.get('CX', '0'))

V = {
 'A': dict(font='noto', c1=(255, 255, 255), c2=(255, 46, 76), st=(6, 12, 30), bg='navy', logo='halo', hero='color', hw=395, rim=(110, 170, 255),
           meta=dict(structure='1인 상체 + 로고 후광', font='Noto Sans KR Black', color='남색+롯데 빨강 강조', bg='남색 그라데이션+로고 후광')),
 'B': dict(font='gmarket', c1=(255, 255, 255), c2=(140, 210, 255), st=(70, 0, 16), bg='red', logo='pattern', hero='color', rim=(255, 220, 220),
           meta=dict(structure='1인 상체 + 팀 패턴(R27)', font='Gmarket Sans Bold', color='롯데 빨강 배경+하늘색 강조', bg='빨강 + 로고 패턴')),
 'C': dict(font='kbo', c1=(255, 255, 255), c2=(255, 40, 70), st=(0, 0, 0), bg='black', logo='redmono', hero='bw', rim=(255, 60, 80),
           meta=dict(structure='1인 흑백 + 거대 단색 로고(R23)', font='KBO Dia Gothic Bold', color='흑백 인물+빨강', bg='검정 + 빨강 단색 로고')),
 'D': dict(font='noto', c1=(10, 30, 70), c2=(214, 0, 40), st=(255, 255, 255), bg='day', logo='big', hero='color', hw=395, rim=(255, 255, 255),
           meta=dict(structure='1인 상체 + 로고 크게 뒤(낮)', font='Noto Sans KR Black', color='흰·하늘 + 남색/빨강 글씨', bg='밝은 하늘 + 로고')),
}
A = dict(hw=415, cx=1350, head_top=30, tw=0.80, t_left=0.04, gap=22, t_bottom=1418,
         t1='롯데 새 감독 이동욱', t2='9년 탈락 끊을까?')

def text_img(t, size, fill, font, stroke=0, sfill=(0, 0, 0)):
    f = ImageFont.truetype(font, size); b = f.getbbox(t, stroke_width=stroke)
    im = Image.new('RGBA', (b[2] - b[0] + 60, b[3] - b[1] + 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((30 - b[0], 30 - b[1]), t, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return im.crop(im.getbbox())

def shadow_paste(can, im, xy, off=(10, 14), blur=12, op=.75):
    a = np.zeros((H, W), np.float32); x, y = xy
    al = np.asarray(im)[..., 3].astype(np.float32) / 255
    ys, xs = slice(max(0, y + off[1]), min(H, y + off[1] + im.height)), slice(max(0, x + off[0]), min(W, x + off[0] + im.width))
    a[ys, xs] = al[:ys.stop - ys.start, :xs.stop - xs.start]
    a = cv2.GaussianBlur(a, (0, 0), blur) * op
    c = np.asarray(can).astype(np.float32); c[..., :3] *= (1 - a[..., None]); can = Image.fromarray(c.astype(np.uint8))
    can.alpha_composite(im, (x, y)); return can

def make(k):
    P = V[k]; yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / 1700) ** 2 + ((yy - 520) / 900) ** 2); g = np.clip(1 - r, 0, 1) ** 1.5
    if P['bg'] == 'navy':
        c0, c1_ = np.array([6, 14, 36]), np.array([30, 70, 150]); dark = np.array([3, 7, 20])
    elif P['bg'] == 'red':
        c0, c1_ = np.array([120, 6, 26]), np.array([228, 20, 52]); dark = np.array([40, 2, 10])
    elif P['bg'] == 'black':
        c0, c1_ = np.array([8, 8, 10]), np.array([48, 44, 48]); dark = np.array([0, 0, 0])
    elif P['bg'] == 'day':
        c0, c1_ = np.array([150, 200, 236]), np.array([252, 253, 255]); dark = np.array([244, 247, 252])
    else:
        c0, c1_ = np.array([10, 30, 70]), np.array([120, 190, 240]); dark = np.array([4, 12, 32])
    bg = c0 * (1 - g[..., None]) + c1_ * g[..., None]
    ang = np.arctan2(yy - 520, xx - W / 2)
    if P['bg'] in ('navy', 'sky', 'day'):
        bg += ((0.5 + 0.5 * np.cos(ang * 16)) ** 6 * np.clip(1 - r * .7, 0, 1) * .18)[..., None] * np.array([200, 230, 255])
    can = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert('RGBA')
    # 로고(배경)
    if P['logo'] == 'pattern':
        sm = LOGO.resize((300, int(300 * LOGO.height / LOGO.width)), Image.LANCZOS)
        a = np.asarray(sm).astype(np.float32); a[..., :3] = 255; a[..., 3] *= .10; sm = Image.fromarray(a.astype(np.uint8))
        pat = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for j, y in enumerate(range(-100, H, 280)):
            for x in range(-200 + (j % 2) * 210, W, 420): pat.alpha_composite(sm, (x, y))
        can.alpha_composite(pat)
        big = LOGO.resize((1900, int(1900 * LOGO.height / LOGO.width)), Image.LANCZOS)
        can.alpha_composite(big, ((W - big.width) // 2, 70))
    elif P['logo'] == 'halo':
        big = LOGO.resize((2050, int(2050 * LOGO.height / LOGO.width)), Image.LANCZOS)
        a = np.asarray(big).astype(np.float32); a[..., :3] *= .82; big = Image.fromarray(a.astype(np.uint8))
        can.alpha_composite(big, ((W - big.width) // 2, 40))
    elif P['logo'] == 'redmono':
        big = LOGO.resize((2300, int(2300 * LOGO.height / LOGO.width)), Image.LANCZOS)
        a = np.asarray(big).astype(np.float32); l = a[..., :3] @ np.array([.3, .59, .11]) / 255
        a[..., :3] = (np.array([60, 0, 10]) * (1 - l[..., None]) + np.array([235, 20, 50]) * l[..., None])
        big = Image.fromarray(a.astype(np.uint8)); can.alpha_composite(big, ((W - big.width) // 2 - (-40), -20))
    else:
        big = LOGO.resize((2200, int(2200 * LOGO.height / LOGO.width)), Image.LANCZOS)
        can.alpha_composite(big, ((W - big.width) // 2 - (-40), 20))
    # 아래 어둠(제목 자리)·비네트 — 좌우 대칭
    bot = np.clip((yy - 820) / 620, 0, 1) ** 1.1
    vig = np.clip(np.sqrt(((xx - W / 2) / W) ** 2 * 2.2 + ((yy - H / 2) / H) ** 2 * 1.2), 0, 1) ** 2
    c = np.asarray(can).astype(np.float32)
    c[..., :3] = c[..., :3] * (1 - (.12 if P['bg'] == 'day' else .35) * vig[..., None]); c[..., :3] = c[..., :3] * (1 - .8 * bot[..., None]) + dark * .8 * bot[..., None]
    can = Image.fromarray(np.clip(c, 0, 255).astype(np.uint8))
    # 인물
    hw = HWO or P.get('hw', A['hw']); s = hw / HEAD_W0; pw, ph = int(CUT.width * s), int(CUT.height * s)
    pa = np.asarray(CUT.resize((pw, ph), Image.LANCZOS)).astype(np.float32)
    rgb = pa[..., :3] / 255; l = (rgb @ np.array([.3, .59, .11]))[..., None]
    if P['hero'] == 'bw': rgb = np.repeat(np.clip((l - .5) * 1.18 + .5, 0, 1), 3, 2)
    else: rgb = np.clip(l + (rgb - l) * 1.08, 0, 1); rgb = np.clip((rgb - .5) * 1.06 + .51, 0, 1)
    al = pa[..., 3] / 255
    # 어깨 옆 사진 틀 직선: 바깥 160px 을 부드럽게 녹여 직선이 안 보이게 (바탕이 어두운 아래쪽에서만)
    xs = np.arange(pw)[None, :]; ysr = np.arange(ph)[:, None]
    dl = np.clip(xs / (190 * s / .81), 0, 1); dr = np.clip((pw - 1 - xs) / (190 * s / .81), 0, 1)
    rowl = np.clip((ysr - (CUTL - 150) * s) / (150 * s), 0, 1); rowr = np.clip((ysr - (CUTR - 150) * s) / (150 * s), 0, 1)
    fade = (1 - rowl * (1 - dl ** 1.3)) * (1 - rowr * (1 - dr ** 1.3))
    # (어깨는 ldw_cut_ext.png 에서 사진 틀 밖으로 자연스럽게 이어 붙임 — 녹이기 안 함)
    pa = np.dstack([rgb * 255, al * 255])
    x0 = (CXO or A['cx']) - pw // 2; y0 = A['head_top'] - int(HEAD_TOP0 * s)
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); layer.paste(Image.fromarray(pa.astype(np.uint8)), (x0, y0))
    Lp = np.asarray(layer).astype(np.float32); Al = Lp[..., 3] / 255
    sh = cv2.GaussianBlur(Al, (0, 0), 24) * .55
    c = np.asarray(can).astype(np.float32); c[..., :3] *= (1 - sh[..., None]); can = Image.fromarray(c.astype(np.uint8))
    er = cv2.erode((Al > .5).astype(np.uint8), np.ones((9, 9), np.uint8)).astype(np.float32)
    edge = np.clip(Al - cv2.GaussianBlur(er, (0, 0), 5), 0, 1) * .5 * np.clip(1 - (np.arange(H)[:, None] - 700) / 200, 0, 1)
    Lp[..., :3] = Lp[..., :3] * (1 - edge[..., None]) + np.array(P['rim']) * edge[..., None]
    can.alpha_composite(Image.fromarray(np.clip(Lp, 0, 255).astype(np.uint8)))
    os.makedirs(f'{OUT}{k}', exist_ok=True)
    full = np.asarray(layer)[..., 3]  # 마스크
    Image.fromarray(full).save(f'{OUT}{k}/mask_이동욱.png')
    # 제목
    maxw = int(A['tw'] * W); xl = int(A['t_left'] * W); fo = F[os.environ.get('FONT', P['font'])]
    def line(t, fill, mw):
        im = (text_img(t, 300, fill, fo, stroke=6, sfill=fill) if os.environ.get('NOSTROKE') else text_img(t, 300, fill, fo, stroke=13, sfill=P['st']))  # NOSTROKE: 같은 색으로 6px 두껍게(윤곽선 아님)
        return im.resize((mw, int(im.height * mw / im.width)), Image.LANCZOS)
    # 가운데 정렬. 아랫줄은 재생시간 표시 자리(x>0.883W·y>0.903H)를 피하려고 폭 0.76W
    L1, L2 = line(A['t1'], P['c1'], maxw), line(A['t2'], P['c2'], int(0.76 * W))
    xl1, xl2 = (W - L1.width) // 2, (W - L2.width) // 2
    y2 = A['t_bottom'] - L2.height; y1 = y2 - A['gap'] - L1.height
    band = np.zeros((H, W), np.float32)
    if os.environ.get('NOSTROKE'): band[y1 - 10:] = 1; band = cv2.GaussianBlur(band, (0, 0), 34) * .9
    else: band[y1 + 40:] = 1; band = cv2.GaussianBlur(band, (0, 0), 50) * .72
    c = np.asarray(can).astype(np.float32)
    if P['bg'] == 'day':
        bd = np.zeros((H, W), np.float32); bd[y1 - 24:] = 1; bd = cv2.GaussianBlur(bd, (0, 0), 3)[..., None]
        c[..., :3] = c[..., :3] * (1 - bd) + np.array([246, 249, 253]) * bd
        c[y1 - 38:y1 - 24, :, :3] = np.array([214, 0, 40])  # 롯데 빨강 줄
    else: c[..., :3] *= (1 - band[..., None])
    can = Image.fromarray(c.astype(np.uint8))
    op_ = .35 if P['bg'] == 'day' else .75
    if os.environ.get('NOSTROKE'):
        # 스킬 8-3: 두꺼운 아래 그림자(0 6px 0 .6 @1280 → 12px) + 넓은 흐린 그림자. 밝은 배경은 그림자 약하게
        for L_, (x_, y_) in ((L1, (xl1, y1)), (L2, (xl2, y2))):
            if P['bg'] != 'day':
                can = shadow_paste(can, Image.new('RGBA', L_.size, (0, 0, 0, 0)), (x_, y_), off=(0, 0), blur=1, op=0)
                a = np.zeros((H, W), np.float32); al = np.asarray(L_)[..., 3].astype(np.float32) / 255
                a[y_:y_ + L_.height, x_:x_ + L_.width] = al
                wide = cv2.GaussianBlur(np.roll(a, 10, 0), (0, 0), 26) * .55
                hard = np.roll(a, 12, 0) * .6
                c = np.asarray(can).astype(np.float32); c[..., :3] *= (1 - wide[..., None]); c[..., :3] *= (1 - hard[..., None]); can = Image.fromarray(c.astype(np.uint8))
                can.alpha_composite(L_, (x_, y_))
            else:
                can = shadow_paste(can, L_, (x_, y_), off=(0, 8), blur=14, op=.18)
    else:
        can = shadow_paste(can, L1, (xl1, y1), op=op_); can = shadow_paste(can, L2, (xl2, y2), op=op_)
    out = can.convert('RGB'); out.save(f'{OUT}{k}/final.jpg', quality=93); out.resize((1280, 720), Image.LANCZOS).save(f'{OUT}{k}/final_1280.jpg', quality=92)
    lay = dict(kind='long', title=[dict(text=A['t1'], box=[xl1, y1, xl1 + L1.width, y1 + L1.height]), dict(text=A['t2'], box=[xl2, y2, xl2 + L2.width, y2 + L2.height])],
               sub=[], people=[dict(name='이동욱', mask=f'{OUT}{k}/mask_이동욱.png', z=1, row=0, side='C', kind='상반신(미디어)', upscale=round(s, 3),
                                    head_w=hw, hero=True, src=CUTF)], meta=P['meta'])
    json.dump(lay, open(f'{OUT}{k}/layout.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(k, 'title', round(L1.height / H, 3), round(L2.height / H, 3), 'top', round(y1 / H, 3))

for k in (sys.argv[1:] or V): make(k)
