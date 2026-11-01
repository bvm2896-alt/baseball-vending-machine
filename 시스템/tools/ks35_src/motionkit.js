/* @@MOTIONKIT 11/1 사용자 "영상 디자인 효과(이즈 인·이즈 아웃·스프링·바운스·순차 등장·페이드·슬라이드·확대 전환·공유 요소 전환 등)를 학습해 적절하게".
   공용 움직임 도구 MK — 모든 장면에서 쓴다. p = 0~1 진행값(seg/pk 결과).
   규칙(사용자 지적 반영): 큰 글자·국기·사진은 넘침(오버슛) 금지(9/19) → spring/bounce 는 칩·점·배지 같은 작은 요소에만.
   사진 크기는 이어지는 장면에서 바뀌지 않는다(11/1) → 사진에는 zoom 효과 쓰지 않는다. 깜빡임 금지 → 페이드는 0.15초 이상. */
const MK = (() => {
  const c = x => x < 0 ? 0 : x > 1 ? 1 : x;
  const E = {
    linear: t => c(t),
    inCubic: t => Math.pow(c(t), 3),                                   /* 이즈 인: 천천히 출발 → 빠르게(퇴장용) */
    outCubic: t => 1 - Math.pow(1 - c(t), 3),                          /* 이즈 아웃: 빠르게 출발 → 끝에서 천천히(등장 기본) */
    inOutCubic: t => { t = c(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; },   /* 이동·전환 */
    outQuint: t => 1 - Math.pow(1 - c(t), 5),                          /* 강조 감속(MD3 emphasized decelerate 근사) */
    outBack: (t, s = 1.2) => { t = c(t); return 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2); },   /* 살짝 넘쳤다 돌아옴 */
    spring: (t, z = .55, w = 14) => { t = c(t); if (t >= 1) return 1; const wd = w * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t)); },   /* 스프링: 툭 넘쳤다 튕기며 멈춤 */
    outExpo: t => { t = c(t); return t >= 1 ? 1 : 1 - Math.pow(2, -10 * t); },   /* 지수 감속 — 숫자 카운트업 기본 */
    elastic: t => { t = c(t); return t === 0 ? 0 : t === 1 ? 1 : Math.pow(2, -10 * t) * Math.sin((t * 10 - .75) * (2 * Math.PI / 3)) + 1; },   /* 엘라스틱 — 결론 숫자 한 번만 */
    inBack: (t, s = 1.4) => { t = c(t); return (s + 1) * t * t * t - s * t * t; },   /* 예비동작(움츠렸다 출발) */
    steps: (t, n = 6) => Math.floor(c(t) * n) / n,
    bounce: t => { t = c(t); const n = 7.5625, d = 2.75; if (t < 1 / d) return n * t * t; if (t < 2 / d) return n * (t -= 1.5 / d) * t + .75; if (t < 2.5 / d) return n * (t -= 2.25 / d) * t + .9375; return n * (t -= 2.625 / d) * t + .984375; },   /* 바운스: 바닥에 튕김 */
  };
  const css = {
    /* 등장 */
    fade: p => `opacity:${c(p).toFixed(3)}`,
    rise: (p, px = 40) => `opacity:${c(p * 1.5).toFixed(3)};transform:translateY(${((1 - E.outCubic(p)) * px).toFixed(1)}px)`,
    slide: (p, dir = 'l', px = 120) => { const v = (1 - E.outQuint(p)) * px, tx = dir === 'l' ? -v : dir === 'r' ? v : 0, ty = dir === 'u' ? -v : dir === 'd' ? v : 0; return `opacity:${c(p * 2).toFixed(3)};transform:translate(${tx.toFixed(1)}px,${ty.toFixed(1)}px)`; },
    springPop: (p, from = .6) => `opacity:${c(p * 3).toFixed(3)};transform:scale(${(from + (1 - from) * E.spring(p)).toFixed(4)})`,   /* 칩·배지·점만 */
    bounceDrop: (p, px = 80) => `opacity:${c(p * 3).toFixed(3)};transform:translateY(${(-(1 - E.bounce(p)) * px).toFixed(1)}px)`,   /* 점·공 아이콘만 */
    zoomIn: (p, from = .92) => `opacity:${c(p * 1.6).toFixed(3)};transform:scale(${(from + (1 - from) * E.outCubic(p)).toFixed(4)})`,   /* 판·카드 전체(사진 단독 ✗) */
    wipe: (p, dir = 'l') => { const r = (100 - 100 * E.inOutCubic(p)).toFixed(1); return `clip-path:inset(${dir === 'd' ? `0 0 ${r}% 0` : dir === 'u' ? `${r}% 0 0 0` : dir === 'r' ? `0 0 0 ${r}%` : `0 ${r}% 0 0`})`; },   /* 마스크 리빌 */
    pop: (p, from = .7) => `opacity:${c(p * 2.5).toFixed(3)};transform:scale(${(from + (1 - from) * E.outBack(p)).toFixed(4)})`,   /* 스케일 팝(살짝 넘침) — 칩·배지 */
    blur: (p, px = 12) => `opacity:${c(p * 1.5).toFixed(3)};filter:blur(${((1 - E.outCubic(p)) * px).toFixed(1)}px)`,   /* 블러 인 — 배경·보조 글 */
    dim: (on, p, lo = .3) => `opacity:${(on ? 1 : 1 - (1 - lo) * E.outCubic(p)).toFixed(3)}`,   /* 하이라이트&디밍: 주인공 외 흐리게 */
    grow: (p, axis = 'x') => `transform:scale${axis === 'x' ? 'X' : 'Y'}(${E.outCubic(p).toFixed(4)});transform-origin:${axis === 'x' ? 'left center' : 'center bottom'}`,   /* 막대 성장(오버슈트 금지) */
    anticip: (p) => { const e = p < .2 ? 1 - .05 * Math.sin(p / .2 * Math.PI / 2) : .95 + .05 * E.outBack((p - .2) / .8); return `transform:scale(${e.toFixed(4)})`; },   /* 예비동작: 움츠렸다 커짐(1위 공개 직전) */
    clash: (p, side = 'l', px = 600) => { const e = E.outQuint(p), x = (1 - e) * px * (side === 'l' ? -1 : 1), j = p > .55 && p < .8 ? Math.sin((p - .55) / .25 * Math.PI * 3) * 3 : 0; return `transform:translateX(${(x + j).toFixed(1)}px);opacity:${c(p * 3).toFixed(3)}`; },   /* 매치업: 양쪽이 들어와 부딪힘 */
    shake: (p, amp = 10) => p <= 0 || p >= 1 ? '' : `transform:translateX(${(Math.sin(p * Math.PI * 6) * amp * (1 - p)).toFixed(1)}px)`,   /* 부정·경고 수치 한 번만 */
  };
  /* 순차 등장: i 번째 요소 시작 시각 */
  const stagger = (i, base = .15, step = .08) => base + i * step;
  /* 숫자 롤링(카운트업): 끝 자리수·소수 자리 유지 */
  const count = (v, p, dec) => { const n = +v; if (isNaN(n)) return String(v); const d = dec != null ? dec : (String(v).split('.')[1] || '').length; return (n * E.outCubic(p)).toFixed(d); };
  /* 하이라이트 스윕(광택이 한 번 지나감) — 강조 카드 안쪽에 겹쳐 넣는 div */
  const sweep = (p, color = 'rgba(255,255,255,.55)') => p <= 0 || p >= 1 ? '' : `<div style="position:absolute;inset:0;pointer-events:none;overflow:hidden;border-radius:inherit"><div style="position:absolute;top:-20%;bottom:-20%;width:28%;left:${(-30 + 160 * E.inOutCubic(p)).toFixed(1)}%;transform:skewX(-18deg);background:linear-gradient(90deg,transparent,${color},transparent)"></div></div>`;
  /* 선 그리기: SVG path 에 stroke-dasharray/offset */
  const draw = (p, len = 2000) => `stroke-dasharray="${len}" stroke-dashoffset="${(len * (1 - E.inOutCubic(p))).toFixed(1)}"`;
  /* 오도미터: 자리별 숫자 띠가 굴러감(1의 자리부터) — 정수·소수 모두 */
  const odo = (v, p, h = 1.1) => [...String(v)].map((ch, i, a) => { if (!/\d/.test(ch)) return `<span>${ch}</span>`; const k = +ch, q = E.outCubic(c((p - (a.length - 1 - i) * .06) / .8)), y = -(k + 10 * (1 - q)) % 10;
      return `<span style="display:inline-block;height:${h}em;overflow:hidden;vertical-align:top"><span style="display:block;transform:translateY(${(y * h).toFixed(3)}em)">${[0,1,2,3,4,5,6,7,8,9].map(d => `<span style="display:block;height:${h}em;line-height:${h}em">${d}</span>`).join('')}</span></span>`; }).join('');
  /* 원형 게이지(SVG): 값% 까지 원호, 12시 시작 */
  const gauge = (pct, p, r = 80, sw = 18, col = '#2563EB', bg = '#E6EAF0') => { const C = 2 * Math.PI * r, off = C * (1 - c(pct / 100) * E.outCubic(p)), w = 2 * (r + sw);
      return `<svg width="${w}" height="${w}" viewBox="0 0 ${w} ${w}"><circle cx="${w / 2}" cy="${w / 2}" r="${r}" fill="none" stroke="${bg}" stroke-width="${sw}"/><circle cx="${w / 2}" cy="${w / 2}" r="${r}" fill="none" stroke="${col}" stroke-width="${sw}" stroke-linecap="round" stroke-dasharray="${C.toFixed(1)}" stroke-dashoffset="${off.toFixed(1)}" transform="rotate(-90 ${w / 2} ${w / 2})"/></svg>`; };
  /* 형광펜 밑줄: 강조 단어 뒤에 깔리는 띠(단어 등장 +0.15초) */
  const marker = (p, col = 'rgba(255,212,59,.55)') => `<span style="position:absolute;left:-4%;right:-4%;bottom:6%;height:38%;background:${col};border-radius:6px;z-index:-1;transform:scaleX(${E.outCubic(p).toFixed(4)});transform-origin:left center"></span>`;
  /* 어절 분할 등장: 문장을 어절마다 아래에서 올라오게(마스크) */
  const words = (txt, p, step = .12, dur = .5) => String(txt).split(' ').map((w, i) => { const q = c((p * (1 + step * 8) - i * step) / dur);
      return `<span style="display:inline-block;overflow:hidden;vertical-align:bottom;padding:0 .12em"><span style="display:inline-block;transform:translateY(${((1 - E.outCubic(q)) * 100).toFixed(1)}%);opacity:${c(q * 2).toFixed(3)}">${w}</span></span>`; }).join('');
  /* 후속 동작: 사진 → 이름 → 기록 순 지연(초) */
  const follow = (i, base = 0, gap = .1) => base + i * gap;
  /* 순위 재정렬: 키로 짝지은 위·아래 보간 */
  const reorder = (y0, y1, p) => y0 + (y1 - y0) * E.inOutCubic(p);
  /* 펄스 고리(결론 숫자 뒤 한 번 퍼짐) */
  const pulse = (p, color = 'rgba(37,99,235,.35)') => p <= 0 || p >= 1 ? '' : `<div style="position:absolute;left:50%;top:50%;width:100%;height:100%;transform:translate(-50%,-50%) scale(${(1 + .35 * E.outCubic(p)).toFixed(3)});border:6px solid ${color};border-radius:inherit;opacity:${(1 - p).toFixed(3)};pointer-events:none"></div>`;
  /* 타이프라이터(인용문) */
  const type = (txt, p) => { const a = [...String(txt)], n = Math.round(a.length * c(p)); return a.slice(0, n).join(''); };
  return { E, css, stagger, count, sweep, draw, pulse, type, odo, gauge, marker, words, follow, reorder };
})();
/* 장면 전환(s.tr): 'fade'(기본, 기존 그대로) · 'slide'(새 장면이 오른쪽에서 밀고 들어옴) · 'zoom'(살짝 커지며 등장 — 확대 전환) · 'up'(아래에서 올라옴).
   같은 chain 의 cont 장면(공유 요소 전환)에는 적용 안 함. render 끝에서 #body 에 transform 을 준다. */
function MK_tr(s, t, start) {
  const b = document.getElementById('body'); if (!b) return;
  if (!s || s._keep || s._chain || !s.tr || s.tr === 'fade') return;   /* 기존 slide() 의 transform 은 건드리지 않는다 */
  const p = c01((t - start) / .45), e = MK.E.outQuint(p); if (p >= 1) return;
  const add = x => { b.style.transform = ((b.style.transform || '') + ' ' + x).trim(); };
  add(s.tr === 'through' ? `scale(${(.92 + .08 * e).toFixed(4)})` : s.tr === 'slide' ? `translateX(${((1 - e) * 160).toFixed(1)}px)` : s.tr === 'zoom' ? `scale(${(.94 + .06 * e).toFixed(4)})` : s.tr === 'up' ? `translateY(${((1 - e) * 70).toFixed(1)}px)` : '');   /* through = 페이드 스루(주제 바뀜) */
}
/* @@MOTIONKITEND */
