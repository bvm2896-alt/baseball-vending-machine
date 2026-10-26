# -*- coding: utf-8 -*-
"""야구자판기 썸네일 관문 검사 (스킬 yagu-thumb-zero) — claude/썸네일-관문-코드.md 그대로"""
import json, sys, os, argparse
import numpy as np
from PIL import Image
try:
    import cv2
except Exception:
    cv2 = None

TH = {
    'long':   dict(title_line_h=0.150, title_top=0.55, face_w=0.100, safe_x=0.035, dur_box=(0.883, 0.903)),
    'shorts': dict(title_line_h=0.070, title_top=0.50, face_w=0.180, safe_x=0.070, vis=(55, 1025, 151, 1560)),
}
FAIL, PASS, SKIP, WARN = 'FAIL', 'PASS', 'SKIP', 'WARN'

def load_alpha(p, W, H):
    m = Image.open(p)
    if m.mode in ('RGBA', 'LA'): m = m.split()[-1]
    else: m = m.convert('L')
    if m.size != (W, H): m = m.resize((W, H))
    return np.asarray(m)

def load_mask(p, W, H):
    return load_alpha(p, W, H) > 127

def bbox(m):
    ys, xs = np.where(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1) if len(xs) else None

def box_mask(boxes, W, H):
    m = np.zeros((H, W), bool)
    for b in boxes:
        x0, y0, x1, y1 = [int(round(v)) for v in b]
        m[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] = True
    return m

def faces_in(img_bgr, region):
    try:
        from skimage.feature import Cascade
        from skimage import data as skd
    except Exception:
        return None
    x0, y0, x1, y1 = region
    crop = img_bgr[y0:y1, x0:x1, ::-1]
    if crop.size == 0: return []
    g = (0.299 * crop[:, :, 0] + 0.587 * crop[:, :, 1] + 0.114 * crop[:, :, 2]) / 255.0
    k = min(1.0, 420.0 / max(g.shape))
    if k < 1:
        from skimage.transform import rescale
        g = rescale(g, k, anti_aliasing=True)
    det = Cascade(skd.lbp_frontal_face_cascade_filename())
    mn = max(18, int(min(g.shape) * 0.12))
    out = det.detect_multi_scale(img=g, scale_factor=1.15, step_ratio=1, min_size=(mn, mn), max_size=(int(min(g.shape) * 0.95),) * 2)
    return [(int(d['c'] / k) + x0, int(d['r'] / k) + y0, int(d['width'] / k), int(d['height'] / k)) for d in out]

def holes_and_bits(m):
    if cv2 is None: return None
    u = m.astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(u, 8)
    big = st[1:, cv2.CC_STAT_AREA].max() if n > 1 else 0
    bits = int(sum(1 for a in st[1:, cv2.CC_STAT_AREA] if 0 < a < big * 0.02 and a > 30))
    inv = (1 - u)
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(inv, 4)
    H, W = m.shape; holes = 0
    for i in range(1, n2):
        x, y, w, h, a = st2[i]
        if x > 0 and y > 0 and x + w < W and y + h < H and a > max(80, big * 0.0015): holes += 1
    cs, _ = cv2.findContours(u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cs: return holes, bits, 0
    c = max(cs, key=cv2.contourArea)
    per = cv2.arcLength(c, True)
    sm = cv2.GaussianBlur(u * 255, (0, 0), 3) > 127
    cs2, _ = cv2.findContours(sm.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    per2 = cv2.arcLength(max(cs2, key=cv2.contourArea), True) if cs2 else per
    return holes, bits, round(per / max(per2, 1), 3)

def run(img_path, lay, hist=None, conf=None):
    im = Image.open(img_path).convert('RGB'); W, H = im.size
    arr = np.asarray(im); bgr = arr[:, :, ::-1].copy()
    kind = lay.get('kind') or ('shorts' if H > W else 'long')
    T = dict(TH[kind]); T.update((conf or {}).get(kind, {}))
    R = []
    add = lambda g, name, res, val, why='': R.append((g, name, res, val, why))
    sz = os.path.getsize(img_path) / 1048576
    okdim = (W, H) in ((2560, 1440), (1280, 720)) if kind == 'long' else (W, H) == (1080, 1920)
    add('G1', '크기·용량', PASS if okdim and sz <= 2 else FAIL, f'{W}x{H}, {sz:.2f}MB')
    titles = lay.get('title') or []
    tb = [t['box'] for t in titles]
    if tb:
        lh = min((b[3] - b[1]) for b in tb) / H
        add('G2', '제목 줄 높이', PASS if lh >= T['title_line_h'] else FAIL, f'가장 작은 줄 {lh:.3f}H (기준 {T["title_line_h"]:.3f}H)')
        ww = max((b[2] - b[0]) for b in tb) / W
        add('G2b', '제목 폭', PASS if ww >= 0.80 else FAIL, f'가장 긴 줄 {ww:.2f}W (기준 0.80W)')
    else:
        add('G2', '제목 줄 높이', FAIL, 'layout.title 없음')
    if tb:
        top = min(b[1] for b in tb) / H
        res = PASS if top >= T['title_top'] else FAIL
        why = f'제목 윗변 {top:.2f}H (기준 ≥{T["title_top"]:.2f}H)'
        sx = T['safe_x'] * W
        if any(b[0] < sx - 12 or b[2] > W - sx + 12 for b in tb): res = FAIL; why += ' · 좌우 안전 여백 침범'
        if kind == 'long':
            dx, dy = T['dur_box']
            if any(b[2] > dx * W and b[3] > dy * H for b in tb): res = FAIL; why += ' · 재생시간 표시 자리 침범'
        add('G3', '제목 하단·안전 영역', res, why)
        add('G4', '글자 잘림', FAIL if any(t.get('clipped') for t in titles) else PASS, ', '.join(t['text'] for t in titles if t.get('clipped')) or '없음')
    P = lay.get('people') or []
    masks = []
    for p in P:
        try: masks.append(load_mask(p['mask'], W, H))
        except Exception as e: masks.append(None); add('G0', f'마스크 {p.get("name")}', FAIL, str(e))
    tmask = box_mask(tb + [s['box'] for s in (lay.get('sub') or [])], W, H)
    face = {}
    for p, m in zip(P, masks):
        if m is None: continue
        b = bbox(m)
        if not b: continue
        x0, y0, x1, y1 = b; hh = int((y1 - y0) * 0.38)
        F = faces_in(bgr, (x0, y0, x1, min(H, y0 + max(hh, 60))))
        if F is None: face[p['name']] = None; continue
        F = [f for f in F if m[min(H - 1, f[1] + f[3] // 2), min(W - 1, f[0] + f[2] // 2)]]
        face[p['name']] = (max(F, key=lambda f: f[2]) if F else None, [])
    if not face or all(v is None for v in face.values()):
        add('G5', '얼굴 보임', SKIP, '검출기 없음')
    else:
        miss = [n for n, v in face.items() if v and v[0] is None]
        add('G5', '얼굴 정면·3/4로 보임', WARN if miss else PASS, ', '.join(miss) or f'{len(face)}명 모두')
        if (lay.get('meta') or {}).get('lookOut'): add('G7', '바깥 보기', SKIP, '눈 검사(TOP 12)')
        hw = []
        for p, m in zip(P, masks):
            if m is None: continue
            bb = bbox(m)
            if not bb: continue
            y = bb[1] + int((bb[3] - bb[1]) * 0.12); row = np.where(m[y])[0]
            est = (row.max() - row.min()) * 0.8 if len(row) else 0
            v = face.get(p['name']); det = v[0][2] if v and v[0] is not None else 0
            hw.append(max(est, det))
        if hw: add('G9', '가장 큰 머리', PASS if max(hw) / W >= T['face_w'] else FAIL, f'{max(hw) / W:.3f}W (기준 {T["face_w"]:.3f}W)')
        cover = []
        fb = {n: v[0] for n, v in face.items() if v and v[0] is not None}
        for p, m in zip(P, masks):
            f = fb.get(p['name'])
            if f is None: continue
            x, y, w, h = f; reg = np.zeros((H, W), bool); reg[y:y + h, x:x + w] = True
            front = np.zeros((H, W), bool)
            for q, mq in zip(P, masks):
                if q is not p and mq is not None and q.get('z', 0) > p.get('z', 0): front |= mq
            c = (reg & (front | tmask)).sum() / max(1, reg.sum())
            if c > 0.02: cover.append(f'{p["name"]} {c * 100:.0f}%')
        add('G11', '얼굴 가림 0', FAIL if cover else PASS, ', '.join(cover) or '0%')
        near = []
        names = list(fb)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                a, b2 = fb[names[i]], fb[names[j]]
                gap = max(b2[0] - (a[0] + a[2]), a[0] - (b2[0] + b2[2]), b2[1] - (a[1] + a[3]), a[1] - (b2[1] + b2[3]))
                if gap < 0.15 * min(a[2], b2[2]): near.append(f'{names[i]}–{names[j]}')
        add('G12', '얼굴 간격', FAIL if near else PASS, ', '.join(near) or '모두 0.15 머리 폭 이상')
    up = [f'{p["name"]} {p["upscale"]:.2f}' for p in P if p.get('upscale', 1) > 1.25]
    add('G8', '확대 1.25배 이하', FAIL if up else (PASS if P else SKIP), ', '.join(up) or '전원 이하')
    kinds = {p.get('kind', '경기') for p in P}
    add('G16', '사진 종류 통일', FAIL if len(kinds) > 1 else (PASS if P else SKIP), '/'.join(kinds) or '-')
    if any(m is not None for m in masks):
        allm = np.zeros((H, W), bool)
        for m in masks:
            if m is not None: allm |= m
        b = bbox(allm)
        ys, xs = np.where(allm); cx = xs.mean() / W
        lm, rm = b[0] / W, (W - b[2]) / W
        res = PASS if abs(cx - 0.5) <= 0.05 and abs(lm - rm) <= 0.05 else FAIL
        add('G10', '좌우 균형', res, f'무게중심 x {cx:.3f} · 여백 좌 {lm:.3f} / 우 {rm:.3f}')
        ghost = []
        for p, m in zip(P, masks):
            if m is None: continue
            a = load_alpha(p['mask'], W, H) > 20
            bb = bbox(a)
            if not bb or bb[3] >= H - 2: continue
            band = np.zeros((H, W), bool); y0 = max(bb[1], bb[3] - max(12, int((bb[3] - bb[1]) * 0.06))); band[y0:bb[3]] = True; band &= a
            front = tmask.copy()
            for q, mq in zip(P, masks):
                if q is not p and mq is not None and q.get('z', 0) > p.get('z', 0): front |= mq
            vis = (band & ~front).sum() / max(1, band.sum())
            if vis > 0.35: ghost.append(f'{p["name"]} 끝선 {vis * 100:.0f}% 보임')
        add('G13', '잘린 아래 끝 숨김', FAIL if ghost else PASS, ', '.join(ghost) or '전원 화면 밑·앞사람·제목 뒤')
        edge = []
        for p, m in zip(P, masks):
            if m is None: continue
            l, r, t = m[:, :2].sum(), m[:, -2:].sum(), m[:2, :].sum()
            if max(l, r) > 0.04 * H or t > 0.02 * W: edge.append(f'{p["name"]}(좌{l} 우{r} 위{t})')
        add('G14', '가장자리에 잘린 몸', FAIL if edge else PASS, ', '.join(edge) or '없음')
        rows = {}
        for p, m in zip(P, masks):
            if m is not None and len(P) >= 3: rows.setdefault(p.get('row', 0), []).append((p, m))
        bad = []
        for rw, items in rows.items():
            items.sort(key=lambda x: bbox(x[1])[0])
            for (p1, m1), (p2, m2) in zip(items, items[1:]):
                b1, b2 = bbox(m1), bbox(m2)
                ov = max(0, b1[2] - b2[0]) / max(1, min(b1[2] - b1[0], b2[2] - b2[0]))
                if not (0.20 <= ov <= 0.55): bad.append(f'{p1["name"]}–{p2["name"]} {ov:.2f}')
        add('G15', '이웃 겹침 20~55%', FAIL if bad else (PASS if rows else SKIP), ', '.join(bad) or '정상')
        q = []
        for p, m in zip(P, masks):
            if m is None: continue
            a = load_alpha(p['mask'], W, H) > 200
            bb = bbox(a)
            if not bb: continue
            a[max(bb[1], bb[3] - int((bb[3] - bb[1]) * 0.04)):] = False
            r = holes_and_bits(a)
            if r and (r[1] or r[2] > 1.25): q.append(f'{p["name"]} 떨어진 조각{r[1]} 톱니{r[2]} (몸 안 틈 {r[0]}개)')
        add('G17', '누끼 구멍·조각·톱니', FAIL if q else (PASS if cv2 is not None else SKIP), ', '.join(q) or '깨끗')
        zone = np.zeros((H, W), bool); ztop = b[1]; zbot = int(min(tb, key=lambda x: x[1])[1]) if tb else b[3]
        fill = (allm | tmask)
        gh, gw = 6, 8; cells = 0; empty = 0
        for i in range(gh):
            for j in range(gw):
                y0 = ztop + (zbot - ztop) * i // gh; y1 = ztop + (zbot - ztop) * (i + 1) // gh
                x0 = b[0] + (b[2] - b[0]) * j // gw; x1 = b[0] + (b[2] - b[0]) * (j + 1) // gw
                if y1 <= y0 or x1 <= x0: continue
                cells += 1
                if fill[y0:y1, x0:x1].mean() < 0.08 and 0 < i and 0 < j < gw - 1: empty += 1
        add('G18', '덩어리 안 빈 구멍', SKIP if len(P) < 3 else (FAIL if cells and empty / cells > 0.10 else PASS), f'빈 칸 {empty}/{cells}')
        cz = allm[ztop:max(ztop + 1, zbot), int(W * 0.42):int(W * 0.58)].mean() if zbot > ztop else 1
        add('G20', '가운데 빈약 금지', SKIP if len(P) < 3 else (FAIL if cz < 0.35 else PASS), f'가운데 띠 채움 {cz:.2f} (기준 0.35)')
        soft = np.zeros((H, W), bool)
        for p in P:
            try: soft |= load_alpha(p['mask'], W, H) > 20
            except Exception: pass
        objm = np.zeros((H, W), bool)
        if lay.get('objects_mask'):  # 10/25: 의도적으로 좌우에 둔 앞 오브젝트(숫자·로고)는 '배경 바닥' 대칭 검사에서 뺀다 — 오브젝트 균형은 G10·눈 검사
            try: objm = load_alpha(lay['objects_mask'], W, H) > 20
            except Exception: pass
        bgm = ~(allm | soft | tmask | objm)
        lum = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]) / 255
        L_ = np.where(bgm[:, :W // 2], lum[:, :W // 2], np.nan); Rr = np.where(bgm[:, W - W // 2:][:, ::-1], lum[:, W - W // 2:][:, ::-1], np.nan)
        st_ = max(8, H // 20); dd = []
        for y in range(0, H - st_, st_):
            l_, r_ = L_[y:y + st_], Rr[y:y + st_]
            if np.isfinite(l_).sum() > 50 and np.isfinite(r_).sum() > 50: dd.append(abs(np.nanmedian(l_) - np.nanmedian(r_)))
        d = max(dd) if dd else 0
        add('G19', '배경 좌우 대칭', FAIL if d > 0.12 else PASS, f'줄별 밝기 차 최대 {d:.3f} (기준 0.12)')
        # G22 앞줄 몸 보임 (사용자 10/11 "얼굴만 둥둥 띄워서 나열", 10/24 "맨 밑에줄이 너무 얼굴만 둥둥 떠있어서 위로 올려야")
        # 맨 앞 줄(z 최대) 사람마다: 제목 윗변 - 머리 꼭대기 ≥ 2.0 × 머리 폭 (머리 + 가슴까지 제목 위로). 10/24 1.4→2.0: v2(1.5~1.8)도 "아직 너무 얼굴만" 지적. head_w 없으면 SKIP
        if tb:
            ttop = min(b_[1] for b_ in tb); zmax = max(p.get('z', 0) for p in P); fl = []
            for p, m in zip(P, masks):
                if m is None or p.get('z', 0) != zmax or not p.get('head_w'): continue
                bb = bbox(m); r_ = (ttop - bb[1]) / p['head_w']
                if r_ < 2.0: fl.append(f"{p['name']} {r_:.2f}")
            hv = any(p.get('head_w') for p in P)
            add('G22', '앞줄 몸 보임(얼굴만 둥둥 금지)', SKIP if not hv else (FAIL if fl else PASS), ', '.join(fl) or '앞줄 전원 2.0 머리 폭 이상', '대형을 위로 올려 가슴까지 제목 위에 보이게')
    meta = lay.get('meta') or {}
    if hist:
        last = hist[-3:]
        same = [h.get('title', '?') for h in last if sum(meta.get(k) == h.get(k) for k in ('structure', 'font', 'color', 'bg')) >= 2]
        add('G21', '최근 3편과 다름', FAIL if same else PASS, ', '.join(same) or '구조·폰트·색·배경 중 3개 이상 다름')
    else:
        add('G21', '최근 3편과 다름', SKIP, 'thumb_log.json 없음')
    return R

def report(R, out=None):
    lines = ['| 관문 | 항목 | 결과 | 수치 | 고치는 법 |', '|---|---|---|---|---|'] + [f'| {g} | {n} | {r} | {v} | {w} |' for g, n, r, v, w in R]
    s = '\n'.join(lines); nf = sum(1 for x in R if x[2] == FAIL)
    s += f'\n\nFAIL {nf} · PASS {sum(1 for x in R if x[2] == PASS)} · SKIP {sum(1 for x in R if x[2] == SKIP)}'
    if out: open(out, 'w', encoding='utf-8').write(s)
    print(s); return nf

def export_layout_html(html_path, out_dir, W, H, title_sel, person_sels, sub_sel=None, meta=None):
    """HTML 템플릿 썸네일에서 layout.json 을 뽑는다(playwright). person_sels: {"이름": "CSS 선택자"} — 그 요소만 남기고 찍어 알파 마스크를 만든다."""
    from playwright.sync_api import sync_playwright
    os.makedirs(os.path.join(out_dir, 'masks'), exist_ok=True)
    lay = {'kind': 'shorts' if H > W else 'long', 'title': [], 'sub': [], 'people': [], 'meta': meta or {}}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': W, 'height': H})
        pg.goto('file://' + os.path.abspath(html_path)); pg.wait_for_timeout(900)
        js_box = '''(sel)=>[...document.querySelectorAll(sel)].map(e=>{const r=e.getBoundingClientRect();
          const rg=document.createRange(); rg.selectNodeContents(e); const q=rg.getBoundingClientRect();
          return {text:e.innerText.trim(), box:[q.left,q.top,q.right,q.bottom], clipped: e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2}})'''
        lay['title'] = pg.evaluate(js_box, title_sel)
        if sub_sel: lay['sub'] = pg.evaluate(js_box, sub_sel)
        for name, sel in person_sels.items():
            pg.evaluate('''(sel)=>{document.querySelectorAll('body *').forEach(e=>e.style.visibility='hidden');
              const t=document.querySelector(sel); let a=t; while(a){a.style.visibility='visible'; a=a.parentElement;}
              t.querySelectorAll('*').forEach(e=>e.style.visibility='visible');
              const st=document.createElement('style'); st.textContent='html,body,body *,#st,#st *,#st #blk,#st #blk *{background:transparent!important;background-image:none!important;box-shadow:none!important;text-shadow:none!important} #st .bg,#spk,#st .bar{display:none!important}'; document.head.appendChild(st);
              document.querySelectorAll('body *').forEach(e=>{if(e!==t&&!e.contains(t)&&!t.contains(e)) e.style.visibility='hidden'; else if(e!==t&&e.contains(t)) e.style.background='transparent';});}''', sel)
            mp = os.path.join(out_dir, 'masks', f'{name}.png')
            pg.screenshot(path=mp, omit_background=True)
            if Image.open(mp).mode != 'RGBA': raise SystemExit('마스크에 알파가 없음 — 배경을 투명으로 못 만듦(템플릿 CSS 확인)')
            lay['people'].append({'name': name, 'mask': mp, 'z': 1, 'row': 0, 'side': 'C', 'kind': '경기'})
            pg.reload(); pg.wait_for_timeout(900)
        b.close()
    json.dump(lay, open(os.path.join(out_dir, 'layout.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return lay


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('img'); ap.add_argument('layout')
    ap.add_argument('--hist'); ap.add_argument('--conf'); ap.add_argument('--out')
    a = ap.parse_args()
    lay = json.load(open(a.layout, encoding='utf-8'))
    hist = json.load(open(a.hist, encoding='utf-8')) if a.hist and os.path.exists(a.hist) else None
    conf = json.load(open(a.conf, encoding='utf-8')) if a.conf and os.path.exists(a.conf) else None
    sys.exit(1 if report(run(a.img, lay, hist, conf), a.out) else 0)
