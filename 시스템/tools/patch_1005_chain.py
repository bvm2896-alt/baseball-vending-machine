# -*- coding: utf-8 -*-
"""10/5 롱폼⑦ 검수: 장면 묶음(chain) — 같은 인물·같은 틀이 이어지면 사라졌다 나타나지 않게(사용자 7번째 지적).
template_long.html · template_long_v.html 두 곳에 같은 고침을 넣는다(이미 들어가 있으면 건너뜀)."""
import re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

R = []   # (old, new) — old 는 파일마다 정확히 한 번 있어야 한다

# ① profile: 묶음이면 사진·이름 그대로, 사진이 바뀌면 틀은 두고 사진만 겹쳐 바꾼다
R.append(("""  const H0 = s.h || 620, PW = s.pw == null ? 480 : s.pw, sts = s.stats || [], K = s._keep;
  const src = photoSrc(s.img);
  const vis = (PW && src) ? `<div class="photo" style="width:${PW}px;height:${H0}px;flex:0 0 auto;${K ? '' : rise(seg(lt, 0, .5), 40)}"><img src="${src}" style="object-fit:cover;object-position:${esc(s.focus || '50% 0%')}"></div>` : PH(s, H0, seg(lt, 0, .5));""",
"""  const H0 = s.h || 620, PW = s.pw == null ? 480 : s.pw, sts = s.stats || [], K = s._keep || s._chain;   /* 10/5: 같은 사람 묶음(chain)이면 사진·이름은 그대로 */
  const src = photoSrc(s.img);
  const vis = (PW && src) ? chainPhoto(s, src, PW, H0, lt, K) : PH(s, H0, seg(lt, 0, .5));"""))
R.append(("""      ${s.sub ? `<div class="badge" style="margin-top:14px;background:${ACC}">${esc(s.sub)}</div>` : ''}</div>
    ${s.text ? (() => {""",
"""      ${s.sub ? `<div class="badge" style="margin-top:14px;background:${ACC};${K && s._prev && s._prev.sub !== s.sub ? pop(seg(lt, .05, .4)) : ''}">${esc(s.sub)}</div>` : ''}</div>
    ${s.text ? (() => {"""))

# ② speech: 같은 묶음이면 사진·이름 그대로 + 이름 크기·여백을 profile 과 같게(묶음에 profile 이 있으면) + 말풍선 안 12구단 칩
R.append(("""  const KP = K || !!(s._keep && s._prev && ['profile', 'speech'].includes(s._prev.type));
  const PV = K ? (s._prev.bubbles || []).filter(b => !b.hide).length : 0;
  const vis = src ? `<div class="photo" style="width:${PW}px;height:${H0}px;flex:0 0 auto;${KP ? '' : rise(seg(lt, 0, .5), 40)}"><img src="${src}" style="object-fit:cover;object-position:${esc(s.focus || '50% 0%')}"></div>` : PH(s, H0, seg(lt, 0, .5));
  let t = `<div class="col" style="height:${H0}px;justify-content:flex-start;align-items:flex-start;gap:22px;padding-top:4px">
    <div style="${KP ? '' : rise(seg(lt, .04, .45), 22)}"><div class="mega" style="font-size:${s.size || 104}px">${br(s.name || '')}</div>
      ${s.sub ? `<div class="badge" style="margin-top:12px;background:${ACC}">${esc(s.sub)}</div>` : ''}</div>`;""",
"""  const KP = K || s._chain || !!(s._keep && s._prev && ['profile', 'speech'].includes(s._prev.type));
  const PV = K ? (s._prev.bubbles || []).filter(b => !b.hide).length : 0;
  const PF = (CHAINS[s._cid] || []).some(j => SC[j].type === 'profile');   /* 10/5: 묶음에 profile 이 있으면 이름 크기·여백을 profile 과 똑같이(이름이 안 움직이게) */
  const vis = src ? chainPhoto(s, src, PW, H0, lt, KP) : PH(s, H0, seg(lt, 0, .5));
  let t = `<div class="col" style="height:${H0}px;justify-content:flex-start;align-items:flex-start;gap:22px;padding-top:${PF ? 8 : 4}px">
    <div style="${KP ? '' : rise(seg(lt, .04, .45), 22)}"><div class="mega" style="font-size:${s.size || (PF ? 116 : 104)}px">${br(s.name || '')}</div>
      ${s.sub ? `<div class="badge" style="margin-top:${PF ? 14 : 12}px;background:${ACC};${KP && s._prev && s._prev.sub !== s.sub ? pop(seg(lt, .05, .4)) : ''}">${esc(s.sub)}</div>` : ''}</div>`;"""))
R.append(("""        <div style="font-size:${b.size || 60}px;font-weight:900;letter-spacing:-2px;line-height:1.22;text-align:left;color:${b.hi ? ACC : TXT}">${br(b.text || '')}</div></div></div>`;""",
"""        <div style="font-size:${b.size || 60}px;font-weight:900;letter-spacing:-2px;line-height:1.22;text-align:left;color:${b.hi ? ACC : TXT}">${br(b.text || '')}</div>${b.chips && typeof NPB12 !== 'undefined' ? `<div style="display:grid;grid-template-columns:repeat(6,auto);gap:8px;margin-top:6px">${NPB12.map((x, j) => `<div style="${pop(c01(q * 2.2 - .5 - j * .06))}">${npbChip(x, 112, 46, 22)}</div>`).join('')}</div>` : ''}</div></div>`;"""))

# ③ slide: 묶음이면 밀지 않는다(자리가 이미 고정)
R.append(("""  if (k !== PK) { SLIDE = (s._keep && PW && w) ? (w - PW) / 2 : 0; SAT = start; PK = k; }""",
"""  if (k !== PK) { SLIDE = (s._keep && !s._chain && PW && w) ? (w - PW) / 2 : 0; SAT = start; PK = k; }"""))

# ④ autoCenter: 재는 부분을 measureLR 로 떼고, 묶음 전체를 한 번에 맞추는 ensureCx 를 쓴다
R.append(("""function autoCenter(s, measure) {
  const body = document.getElementById('body'), el = body.firstElementChild; if (!el || s.noCenter) { s._cx = 0; return; }
  /* 좌표로 직접 그린 대칭 그림(저울·선로·트레이드·갈림길·점수판 등)과 확대판(Bp .port)은 건드리지 않는다 */
  if (['rankline', 'trade', 'zigzag', 'password', 'backdoor', 'toc', 'chapter', 'gantt', 'flow', 'funnel', 'domino', 'flip'].includes(s.type) || body.querySelector('.port')) { s._cx = 0; return; }
  if (measure) {
    const B0 = body.getBoundingClientRect(); let L = 1e9, R = -1e9;""",
"""/* 10/5: 보이는 내용의 좌우 끝(L·R)과 기준 칸(data-anchor = 인물 사진, 없으면 L)을 잰다. 대칭으로 그린 장면은 null(가운데 맞춤 안 함) */
function measureLR(s) {
  const body = document.getElementById('body'), el = body.firstElementChild; if (!el || s.noCenter) return null;
  if (['rankline', 'trade', 'zigzag', 'password', 'backdoor', 'toc', 'chapter', 'gantt', 'flow', 'funnel', 'domino', 'flip', 'npbdraft', 'snake', 'vs2'].includes(s.type) || body.querySelector('.port')) return null;
  {
    const B0 = body.getBoundingClientRect(); let L = 1e9, R = -1e9;"""))
R.append(("""      L = Math.min(L, l); R = Math.max(R, r); });
    s._cx = (L < R) ? Math.round((B0.left + B0.width / 2) - (L + R) / 2) : 0;
  }
  if (Math.abs(s._cx) >= 6) { el.style.position = 'relative'; el.style.left = s._cx + 'px'; }   /* transform 대신 left — 장면 애니메이션(transform)과 겹치지 않게 */""",
"""      L = Math.min(L, l); R = Math.max(R, r); });
    if (!(L < R)) return null;
    const an = body.querySelector('[data-anchor]');
    return { L, R, A: an ? an.getBoundingClientRect().left : L, C: B0.left + B0.width / 2 };
  }
}
/* 장면 첫 프레임에 한 번: 묶음(chain)이면 묶음 안 장면을 전부 '다 그려진 모습'으로 그려 재고, 기준 칸(사진)이 묶음 내내 같은 x 에 오면서
   묶음 전체 내용이 화면 가운데에 오는 값을 장면마다 정한다 → 장면이 바뀌어도 사진·이름이 1px 도 안 움직인다 */
function ensureCx(k) {
  const s = SC[k]; if (!s || s._cx != null) return;
  const keep = NOW, ms = (CHAINS[s._cid] || [k]).length > 1 ? CHAINS[s._cid] : [k];
  const endOf = j => (j < BD.length ? BD[j] : (EP.total || (BD[BD.length - 1] || 0) + 3)) - 0.02;
  const M = ms.map(j => { const m = SC[j]; NOW = endOf(j); (SCENE[m.type] || SCENE.big)(99, m); return measureLR(m); });
  NOW = keep;
  const ok = M.filter(x => x);
  if (!ok.length) { ms.forEach(j => SC[j]._cx = 0); return; }
  if (ms.length === 1) { s._cx = Math.round(ok[0].C - (ok[0].L + ok[0].R) / 2); return; }
  const lmin = Math.min(...ok.map(x => x.L - x.A)), rmax = Math.max(...ok.map(x => x.R - x.A)), X = ok[0].C - (lmin + rmax) / 2;
  ms.forEach((j, i) => SC[j]._cx = M[i] ? Math.round(X - M[i].A) : 0);
}
function autoCenter(s, measure) {
  const body = document.getElementById('body'), el = body.firstElementChild; if (!el) return;
  if (measure && s._cx == null) { const m = measureLR(s); s._cx = m ? Math.round(m.C - (m.L + m.R) / 2) : 0; }
  const chained = (CHAINS[s._cid] || []).length > 1;
  if (Math.abs(s._cx || 0) >= 6 || (chained && s._cx)) { el.style.position = 'relative'; el.style.left = s._cx + 'px'; }   /* transform 대신 left — 장면 애니메이션(transform)과 겹치지 않게. 묶음은 1px 도 맞춘다 */"""))

# ⑤ render: 장면 정보는 처음 한 번(prepAll), 묶음 판정, 크로스페이드(ghost)
RENDER_NEW = r"""/* 10/5 롱폼⑦ 사용자 7번째 지적("같은 인물·같은 틀이 이어지면 절대 사라졌다 나타나지 않게"): 장면 묶음(chain)
   = 콘티 s.chain 이 같거나 / profile·speech 가 같은 이름이거나 / 이어 그리기(_same: cont·toc 등).
   묶음 안: 본문이 안 흐려지고, 가운데 맞춤은 묶음 전체로 한 번(ensureCx), 사진이 바뀌면 틀은 두고 사진만 겹쳐 바뀐다(chainPhoto).
   묶음이 아닌 장면 전환: 빈 화면 없이 앞 장면이 0.3초 겹쳐 사라진다(크로스페이드, 가로만). */
const chainKey = s => !s ? '' : s.chain ? 'C:' + s.chain : (['profile', 'speech'].includes(s.type) && s.name) ? 'P:' + s.name : '';
let PREP = false; const CHAINS = {};
function prepAll() {
  if (PREP) return; PREP = true;
  const J = x => JSON.stringify(x == null ? null : x);   // 9/19: 앞 장면과 같은 뼈대(표·국기 줄)면 그 부분은 다시 안 그린다
  SC.forEach((s, k) => {
    const prev = k > 0 ? SC[k - 1] : null;                   // 9/18: 같은 사진이면 사진은 그대로 두고 글/칩만 바뀌게
    s._prev = prev; s._next = SC[k + 1] || null;
    s._keep = !!(prev && photoSrc(prev.img) && photoSrc(prev.img) === photoSrc(s.img));
    /* 9/27: 표에 줄이 하나씩 늘어나는 h2h 는 앞 장면에 있던 줄은 그대로 두고 새 줄만 아래에 붙는다 */
    s._prevN = 0;
    if (prev && prev.type === 'h2h' && s.type === 'h2h' && (prev.title || '') === (s.title || '')) {
      const a = prev.rows || [], b = s.rows || []; let n = 0; while (n < a.length && n < b.length && a[n].when === b[n].when) n++; s._prevN = n;
    }
    s._same = !!(prev && prev.type === s.type && (
      (s.type === 'h2h' && J(prev.rows) === J(s.rows) && (prev.title || '') === (s.title || '')) ||
      (s.type === 'matchup' && prev.left === s.left && prev.right === s.right && !photoSrc(s.img)) ||
      (s.type === 'toc') ||   /* 9/28: 목차 → 목차는 사라지지 않고 강조만 옮긴다 */
      (s.cont && ['gantt', 'flow', 'cells', 'funnel', 'flip', 'rankline', 'password', 'scale', 'stack', 'contracts', 'people', 'tiles', 'statbars', 'steps', 'speech', 'bars', 'facegrid', 'scoreboard', 'teamgrid', 'npbdraft'].includes(s.type))));
    s._chain = !!(prev && ((chainKey(s) && chainKey(prev) === chainKey(s)) || s._same));
    s._cid = s._chain ? prev._cid : k; (CHAINS[s._cid] = CHAINS[s._cid] || []).push(k);
  });
  /* 9/19 + 10/5: profile 묶음(같은 사람 또는 같은 사진)의 최대 칩 수 — 칩 크기를 처음부터 맞춰 둔다 */
  SC.forEach((s, k) => { if (s.type !== 'profile') return;
    let a = k, b = k; const same = (x, y) => x && y && x.type === 'profile' && y.type === 'profile' && (x._cid === y._cid || photoSrc(x.img) && photoSrc(x.img) === photoSrc(y.img));
    while (a > 0 && same(SC[a - 1], SC[a])) a--;
    while (b + 1 < SC.length && same(SC[b], SC[b + 1])) b++;
    let m = 0; for (let j = a; j <= b; j++) m = Math.max(m, (SC[j].stats || []).length);
    s._nmax = m; });
}
/* 크로스페이드: 앞 장면의 다 그려진 모습을 #ghost 에 복사해 0.3초 동안 흐리게 */
function ghostOf(k, t, start) {
  let G = document.getElementById('ghost'); const s = SC[k], dt = t - start;
  const on = !EP.vertical && k > 0 && s && !(s._keep || s._chain) && dt >= 0 && dt < 0.3;
  if (!on) { if (G && G.innerHTML) { G.innerHTML = ''; G.style.opacity = '0'; } return; }
  const body = document.getElementById('body');
  if (!G) { G = document.createElement('div'); G.id = 'ghost';
    G.style.cssText = 'position:absolute;left:56px;width:1808px;top:146px;height:714px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;pointer-events:none';
    body.parentNode.insertBefore(G, body.nextSibling); }
  const p = SC[k - 1], keep = NOW; ensureCx(k - 1); NOW = start - 0.02; (SCENE[p.type] || SCENE.big)(99, p); autoCenter(p); NOW = keep;
  G.innerHTML = body.innerHTML; G.style.opacity = String((1 - c01(dt / 0.3)).toFixed(3));
}
function render(t) {
  prepAll();
  let k = 0; while (k < BD.length && t >= BD[k]) k++;
  const start = k === 0 ? 0 : BD[k - 1], end = k < BD.length ? BD[k] : (EP.total || start + 3);
  const kk = Math.min(k, SC.length - 1), s = SC[kk] || { type: 'big', text: '' };
  const need = (MOTION[s.type] || MOTION.big)(s), fit = Math.max(0.6, (end - start) * 0.75);
  const lt = (t - start) * (need > fit ? need / fit : 1);
  NOW = t;
  if (SC[kk]) ensureCx(kk);   /* 장면 첫 프레임: 다 그려진 마지막 모습으로 재서 가운데 맞춤 값(묶음이면 묶음 전체로) */
  NOW = t;
  if (SC[kk]) ghostOf(kk, t, start);
  NOW = t;
  (SCENE[s.type] || SCENE.big)(lt, s);
  autoCenter(s);   /* 10/1 밤 사용자 3번째 지적 "오른쪽으로 치우쳐 있어 가운데로" → 보이는 내용 전체를 재서 화면 가운데로 */
  document.querySelectorAll('#body [data-fit]').forEach(el => {        // 한 줄짜리 강조 문구를 칸 폭에 맞춰 줄인다
    const lim = +el.dataset.fit; let fs = parseFloat(el.style.fontSize || getComputedStyle(el).fontSize), g = 0;
    while (el.scrollWidth > lim && fs > 46 && g++ < 60) { fs -= 3; el.style.fontSize = fs + 'px'; }
  });
  document.getElementById('body').style.opacity = (s._keep || s._chain) ? '1' : String(c01((t - start) / 0.3));
  const gx = 50 + 4 * Math.sin(t * .5), gy = 22 + 2 * Math.cos(t * .37);
  document.getElementById('stage').style.background = `radial-gradient(60% 50% at ${gx}% ${gy}%, ${ACC}22 0%, rgba(244,246,250,0) 70%),#F4F6FA`;
  slide(k, t, s, start);
  drawRail(k, t); drawSub(t);
}
/* 사진 칸: 묶음 안에서 사진이 바뀌면 틀은 그대로 두고 앞 사진 위에 새 사진이 0.5초 동안 겹쳐 나타난다 */
function chainPhoto(s, src, PW, H0, lt, still) {
  const P = s._prev, ps = s._chain && P ? photoSrc(P.img) : '', q = (ps && ps !== src) ? c01(lt / .5) : 1;
  return `<div class="photo" data-anchor="1" style="width:${PW}px;height:${H0}px;flex:0 0 auto;${still ? '' : rise(seg(lt, 0, .5), 40)}">${q < 1 ? `<img src="${ps}" style="position:absolute;left:0;top:0;object-fit:cover;object-position:${esc(P.focus || '50% 0%')}">` : ''}<img src="${src}" style="position:relative;object-fit:cover;object-position:${esc(s.focus || '50% 0%')}${q < 1 ? ';opacity:' + q.toFixed(3) : ''}"></div>`;
}
window.render = render; render(0);"""

def patch(path):
    src = open(path, encoding='utf-8').read()
    if 'function prepAll()' in src:
        print('이미 적용됨', path); return
    for old, new in R:
        n = src.count(old)
        assert n == 1, (path, n, old[:80])
        src = src.replace(old, new)
    a = src.index('function render(t) {'); b = src.index('window.render = render; render(0);') + len('window.render = render; render(0);')
    src = src[:a] + RENDER_NEW + src[b:]
    if 'template_long_v' in path:
        old = "if (g && (s._same || s._keep))"
        assert src.count(old) == 1
        src = src.replace(old, "if (g && (s._same || s._keep || s._chain))")
    open(path, 'w', encoding='utf-8').write(src)
    print('ok', path)

for f in ('template_long.html', 'template_long_v.html'):
    patch(os.path.join(ROOT, f))
