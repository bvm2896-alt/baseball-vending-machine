/* ───── 10/5 롱폼⑦ 「일본 드래프트는 왜 제비뽑기」 새 인포그래픽 장면: npbdraft · snake · icontiles · vs2 ─────
   글자만 있는 장면 금지(사용자 10/5) → 전부 그림이 움직이는 장면. template_long.html / template_long_v.html 둘 다 같은 코드.
   10/5 재검수(사용자 7번째 "사라졌다 다시 생겨"): npbdraft 는 s.chain 이 같으면 한 틀 — 카드·칩·제목은 그대로, 아래 칸(zone)만 바뀐다.
   틀 높이는 늘 HH(600) 고정 → 장면이 바뀌어도 제목·칩이 위아래로 안 움직인다. */
const GOLD = typeof GOLD_ === "undefined" ? "#E8A100" : GOLD_;
const NPB12 = [
  { n: '요미우리', c: '#F97709' }, { n: '한신', c: '#FFE201', t: '#12161F' }, { n: 'DeNA', c: '#004B9E' }, { n: '히로시마', c: '#E30C19' }, { n: '야쿠르트', c: '#1E3A6B' }, { n: '주니치', c: '#0D3B8E' },
  { n: '소프트뱅크', c: '#F5C400', t: '#12161F' }, { n: '니혼햄', c: '#0B5BAA' }, { n: '라쿠텐', c: '#8A0F2E' }, { n: '세이부', c: '#13225B' }, { n: '롯데', c: '#121212' }, { n: '오릭스', c: '#B2922B' }];
const NPB_BY = {}; NPB12.forEach(x => NPB_BY[x.n] = x);
const npbChip = (x, w, h, fs, extra = '') => `<div style="width:${w}px;height:${h}px;border-radius:${Math.round(Math.min(h, 110) * .28)}px;background:${x.c || '#3B4A63'};color:${x.t || '#fff'};display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.12;font-size:${fs}px;font-weight:900;letter-spacing:-1px;box-shadow:0 8px 18px rgba(18,22,31,.16);white-space:nowrap;${extra}">${esc(x.n).replace(/\n/g, '<br>')}</div>`;
/* 봉투: p = 종이가 올라온 정도(0~1), win = 당첨 종이(빨간 '교섭권 확정' 도장), mark = 떨어진 종이에 작은 마크(2015 이전), qm = 앞면에 '?'(누가 뽑을지 모름) */
function envelopeH(w, h, p, win, mark, name, blank, qm) {
  const pw = Math.round(w * .78), ph = Math.round(h * .9), up = Math.round(eo(p) * (h * .62));
  const stamp = win ? `<div style="position:absolute;left:50%;top:30%;transform:translate(-50%,-50%) rotate(-10deg) scale(${(.4 + .6 * eb(c01(p * 1.3 - .2))).toFixed(3)});border:5px solid ${RED};color:${RED};border-radius:10px;padding:4px 10px;font-size:${Math.round(h * .17)}px;line-height:1.1;font-weight:900;white-space:nowrap;opacity:${c01(p * 1.6 - .5)}">교섭권<br>확정</div>`
    : mark ? `<div style="position:absolute;left:50%;top:30%;transform:translate(-50%,-50%);width:${Math.round(h * .26)}px;height:${Math.round(h * .26)}px;border-radius:50%;border:4px solid #B9C1CE;color:#B9C1CE;font-size:${Math.round(h * .1)}px;font-weight:900;display:flex;align-items:center;justify-content:center;opacity:${c01(p * 1.6 - .5)}">NPB</div>`
    : blank ? `<div style="position:absolute;left:50%;top:30%;transform:translate(-50%,-50%);font-size:${Math.round(h * .15)}px;font-weight:900;color:#C8CFD9;opacity:${c01(p * 1.6 - .5)}">백지</div>` : '';
  return `<div style="position:relative;width:${w}px;height:${h}px">
    <div style="position:absolute;left:${Math.round((w - pw) / 2)}px;bottom:${Math.round(h * .08)}px;width:${pw}px;height:${ph}px;background:#fff;border:3px solid #D6DBE3;border-radius:8px;transform:translateY(${-up}px);box-shadow:0 6px 14px rgba(18,22,31,.12)">${stamp}</div>
    <div style="position:absolute;left:0;bottom:0;width:${w}px;height:${Math.round(h * .62)}px;background:linear-gradient(180deg,#F6E9C8,#E9D5A4);border:3px solid #C9A96A;border-radius:10px;box-sizing:border-box"></div>
    <div style="position:absolute;left:0;bottom:${Math.round(h * .62) - 3}px;width:0;height:0;border-left:${Math.round(w / 2)}px solid transparent;border-right:${Math.round(w / 2)}px solid transparent;border-top:${Math.round(h * .3)}px solid #D9BE82;transform-origin:50% 0;transform:rotate(${(-170 * c01(p * 2)).toFixed(1)}deg);opacity:${p > .5 ? .25 : 1}"></div>
    ${qm ? `<div style="position:absolute;left:0;bottom:${Math.round(h * .06)}px;width:${w}px;text-align:center;font-size:${Math.round(h * .42)}px;line-height:1;font-weight:900;color:#B08A3E">?</div>`
      : name ? `<div style="position:absolute;left:0;bottom:${Math.round(h * .12)}px;width:${w}px;text-align:center;font-size:${Math.round(h * .17)}px;font-weight:900;color:#7A5B1E">${esc(name)}</div>` : ''}</div>`;
}
/* 이름 모르는 선수(예시) 카드 그림 */
const NPB_SIL = `<svg viewBox="0 0 340 420" width="100%" height="100%" preserveAspectRatio="xMidYMid slice" style="display:block"><rect width="340" height="420" fill="#DDE3EC"/><circle cx="170" cy="150" r="74" fill="#B4BFCE"/><path d="M30,420 C30,300 95,248 170,248 C245,248 310,300 310,420 Z" fill="#B4BFCE"/><text x="170" y="182" text-anchor="middle" font-size="100" font-weight="900" fill="#fff">?</text></svg>`;
const npbTeams = x => (x || NPB12.map(y => y.n)).map(n => typeof n === 'string' ? (NPB_BY[n] || { n, c: '#3B4A63' }) : n);
/* 아래 칸 종류 — 묶음 안에서 종류가 같으면(예: 봉투 추첨이 이어짐) 그대로, 다르면 앞 칸은 0.3초 흐려지며 사라지고 새 칸이 뜬다 */
const npbZoneKey = s => JSON.stringify([(s.bid || []).join(','), s.notes || null, s.rankX || null, s.ballot || null, s.slips || null, s.question || null]);
/* npbdraft 틀 배치(칩 칸·아래 칸) */
function npbLayout(s) {
  const W = 1760, HH = s.hh || 640, teams = npbTeams(s.teams), n = teams.length, noP = !s.player; let RX = noP ? 0 : 440, RW = noP ? W : W - 440;
  const bigC = noP && n <= 4, cols = n > 6 ? 6 : n;
  const cw = bigC ? 320 : noP ? 262 : n > 6 ? 200 : 250, chh = bigC ? 116 : 100, gx = bigC ? 40 : 20, gy = 20;
  const rows_ = Math.ceil(n / cols), chipsBottom = rows_ * chh + (rows_ - 1) * gy, gridW = cols * cw + (cols - 1) * gx;
  /* 10/5: 카드 + 오른쪽 내용 묶음이 화면 가운데에 오게 — 오른쪽 칸 폭을 실제 쓰는 폭(칩·봉투 줄 중 넓은 것)으로 줄이고 통째로 가운데로 민다 */
  let shift = 0;
  if (!noP) { const N = (s.bid || []).length, envW = N ? N * (N <= 2 ? 240 : N <= 4 ? 220 : N <= 8 ? 140 : 96) + (N - 1) * (N <= 4 ? 40 : 16) : 0;
    const useW = Math.min(RW, Math.max(gridW, envW, s.rankX ? 1060 : 0, s.ballot ? 840 : 0, 760));
    shift = Math.round((W - (RX + useW)) / 2); RX += shift; RW = useW; }
  const gx0 = RX + Math.round((RW - gridW) / 2);
  const pos = teams.map((x, i) => ({ x: gx0 + (i % cols) * (cw + gx), y: Math.floor(i / cols) * (chh + gy) }));
  return { W, HH, teams, n, noP, RX, RW, bigC, cw, chh, pos, chipsBottom, ZT: chipsBottom + 34, MX: RX + RW / 2, shift };
}
/* 아래 칸 그리기. fin = 다 그려진 모습(앞 장면 칸을 흐리게 남길 때) */
function npbZone(s, lt, L, fin) {
  const PK = (at, d, fb) => fin ? 1 : (at != null && at < 0) ? 1 : pk(s, at, d, fb);
  const bid = s.bid || [], N = bid.length, byN = n => L.teams.find(t => t.n === n) || NPB_BY[n] || { n };
  let z = '', lines = '';
  /* ① 봉투 추첨(실제 있었던 일 · 예시) */
  if (N) {
    const pb = PK(s.bidAt, .7, seg(lt, .6, .7)), pd = s.drawAt != null ? PK(s.drawAt, .8, seg(lt, 1.6, .8)) : 0, po = (s.winner && s.openAt != null) ? PK(s.openAt, .7, seg(lt, 2.8, .7)) : 0, pr = s.rebidText ? PK(s.rebidAt, .5, seg(lt, 4.0, .5)) : 0;
    if (!L.noP) L.teams.forEach((x, i) => { if (!bid.includes(x.n) || pb <= 0) return; const c = L.pos[i], x1 = c.x + L.cw / 2, y1 = c.y + L.chh, f = eo(c01(pb * 1.4 - i * .02)), lost = po > 0 && x.n !== s.winner;
      const x2 = x1 + (L.shift + 390 - x1) * f, y2 = y1 + (330 - y1) * f;
      lines += `<line x1="${x1}" y1="${y1}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${lost ? '#C8CFD9' : x.c || ACC}" stroke-width="7" stroke-linecap="round" opacity="${lost ? .5 : .9}"/>`; });
    if (pd > 0) { const ew = N <= 2 ? (L.bigC ? 300 : 240) : N <= 4 ? 220 : N <= 8 ? 140 : 96, eh = N <= 2 ? (L.bigC ? 220 : 190) : N <= 4 ? 170 : N <= 8 ? 120 : 86, eg = N <= 4 ? 40 : 16;
      const tot = N * ew + (N - 1) * eg, ex0 = L.RX + Math.round((L.RW - tot) / 2), ey = L.ZT + Math.round(eh * .62) + 6;
      bid.forEach((n, i) => { const x = byN(n), win = n === s.winner, q = fin ? 1 : c01(pd * 1.6 - i * .12), wob = (!fin && po <= 0 && pd >= 1) ? Math.sin(NOW * 9 + i) * 3 : 0;
        z += `<div style="position:absolute;left:${ex0 + i * (ew + eg)}px;top:${ey}px;transform:translateY(${((1 - eo(q)) * 60).toFixed(1)}px) rotate(${wob.toFixed(1)}deg);opacity:${c01(q * 1.4)}">${envelopeH(ew, eh, po, win, !!s.mark && !win, s.anonEnv ? '' : x.n, po > 0 && !win && !s.mark)}</div>`; });
      const lab = pr > 0 ? esc(s.rebidText) : po >= 1 ? esc(s.openLabel || `${s.winner}만 교섭권`) : esc(s.drawLabel || '봉투를 뽑아요');
      z += `<div class="badge" style="position:absolute;left:${L.MX}px;top:${ey + eh + 16}px;translate:-50% 0;background:${pr > 0 ? ACC : po >= 1 ? RED : '#12161F'};font-size:34px;padding:8px 26px;white-space:nowrap;${fin ? '' : pop(c01(pd * 1.3))}">${lab}</div>`; }
  }
  /* ② 알약(사실 몇 개를 차례로) */
  let y0 = L.ZT + 6;
  if (s.notes) { const ns = s.notes, hgt = 96, gap = 18, top = (s.ballot || s.rankX) ? L.ZT + 6 : L.ZT + Math.max(0, Math.round((L.HH - L.ZT - (ns.length * hgt + (ns.length - 1) * gap)) / 2) - 10);
    y0 = top + ns.length * (hgt + gap) + 16;
    ns.forEach((nt, i) => { const p = PK(nt.at, .45, seg(lt, .2 + i * .4, .45)), c = nt.c || ACC;
      z += `<div style="position:absolute;left:${L.MX}px;top:${top + i * (hgt + gap)}px;translate:-50% 0;${pop(p)}"><div style="display:flex;align-items:center;gap:16px;height:${hgt}px;padding:0 38px 0 26px;border-radius:999px;background:#fff;border:4px solid ${c};box-shadow:0 10px 26px rgba(18,22,31,.1);white-space:nowrap">
        <span style="width:24px;height:24px;border-radius:50%;background:${c};flex:0 0 auto"></span><span style="font-size:52px;font-weight:900;letter-spacing:-1.5px;color:${nt.hi ? c : TXT}">${esc(nt.t)}</span></div></div>`; }); }
  /* ③ 순위대로(꼴찌부터) 줄 → 빨간 X */
  if (s.rankX) { const r = s.rankX, p = PK(r.at, .5, seg(lt, .1, .5)), px = PK(r.xAt, .5, seg(lt, 1, .5)), SW = 1060, sx = L.MX - SW / 2, n = 12;
    let dots = ''; for (let i = 0; i < n; i++) dots += `<div style="position:absolute;left:${(70 + i * (SW - 140) / (n - 1) - 15).toFixed(1)}px;top:30px;width:30px;height:30px;border-radius:50%;background:${i === 0 ? '#3B4A63' : '#C9D0DB'};${pop(c01(p * 2 - i * .05))}"></div>`;
    z += `<div style="position:absolute;left:${sx}px;top:${y0}px;width:${SW}px;height:120px;${rise(p, 20)}">
      <div style="position:absolute;left:70px;right:70px;top:42px;height:6px;border-radius:3px;background:#C9D0DB"></div>${dots}
      <div style="position:absolute;left:0;top:76px;font-size:40px;font-weight:900;color:#3B4A63">꼴찌</div><div style="position:absolute;right:0;top:76px;font-size:40px;font-weight:900;color:#8C95A3">1위</div>
      <div style="position:absolute;left:50%;top:72px;transform:translateX(-50%);font-size:46px;font-weight:900;color:#3B4A63;white-space:nowrap">${esc(r.text || '꼴찌 팀부터 순서대로')}</div>
      <svg width="${SW}" height="120" style="position:absolute;left:0;top:0;overflow:visible"><line x1="${SW * .3}" y1="-6" x2="${(SW * .3 + SW * .4 * eo(c01(px * 2))).toFixed(1)}" y2="${(-6 + 132 * eo(c01(px * 2))).toFixed(1)}" stroke="${RED}" stroke-width="16" stroke-linecap="round" opacity="${c01(px * 4)}"/>
        <line x1="${SW * .7}" y1="-6" x2="${(SW * .7 - SW * .4 * eo(c01(px * 2 - 1))).toFixed(1)}" y2="${(-6 + 132 * eo(c01(px * 2 - 1))).toFixed(1)}" stroke="${RED}" stroke-width="16" stroke-linecap="round" opacity="${c01(px * 4 - 2)}"/></svg></div>`;
    y0 += 160; }
  /* ④ 이름 없는 봉투 줄(누가 뽑을지 아직 모름) + 설명 알약 */
  if (s.ballot) { const b = s.ballot, p = PK(b.at, .6, seg(lt, .3, .6)), n = b.n || 4, ew = b.ew || 180, eh = Math.round(ew * .8), eg = 30, tot = n * ew + (n - 1) * eg, ex0 = L.MX - tot / 2, top = (s.rankX || s.notes) ? y0 : L.ZT + Math.max(10, Math.round((L.HH - L.ZT - eh - 80) / 2));
    for (let i = 0; i < n; i++) { const q = fin ? 1 : c01(p * 1.6 - i * .12), wob = fin ? 0 : Math.sin(NOW * 8 + i * 1.7) * 3 * c01(p * 2 - 1);
      z += `<div style="position:absolute;left:${ex0 + i * (ew + eg)}px;top:${top}px;transform:translateY(${((1 - eo(q)) * 50).toFixed(1)}px) rotate(${wob.toFixed(1)}deg);opacity:${c01(q * 1.4)}">${envelopeH(ew, eh, 0, false, false, '', false, true)}</div>`; }
    if (b.label) z += `<div class="badge" style="position:absolute;left:${L.MX}px;top:${top + eh + 18}px;translate:-50% 0;background:${b.c || '#12161F'};font-size:40px;padding:10px 34px;white-space:nowrap;${fin ? '' : pop(c01(p * 1.4 - .3))}">${esc(b.label)}</div>`; }
  /* ⑤ 12구단이 동시에 쪽지를 낸다(선수 이름은 숨김) */
  if (s.slips) { const sl = s.slips, p = PK(sl.at, 1.0, seg(lt, .3, 1.0)), bw = 620, bh = 200, bx = L.MX - bw / 2, by = L.ZT + 90;
    let inBox = 0;
    L.pos.forEach((c, i) => { const q = fin ? 1 : c01(p * 1.6 - (i % 6) * .08 - Math.floor(i / 6) * .05); if (q >= 1) inBox++; if (q <= 0 || q >= 1) return;
      const x1 = c.x + L.cw / 2 - 36, y1 = c.y + L.chh - 10, x2 = L.MX - 36 + (i - 5.5) * 16, y2 = by + 20, e = eo(q);
      const x = x1 + (x2 - x1) * e, y = y1 + (y2 - y1) * e - Math.sin(Math.PI * e) * 50;
      z += `<div style="position:absolute;left:${x.toFixed(1)}px;top:${y.toFixed(1)}px;width:72px;height:56px;background:#fff;border:3px solid #D6DBE3;border-radius:7px;box-shadow:0 4px 10px rgba(18,22,31,.14);display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;color:#8C95A3;opacity:${c01((1 - q) * 8).toFixed(3)};transform:rotate(${((i % 3 - 1) * 10 * (1 - e)).toFixed(1)}deg)">?</div>`; });
    z = `<div style="position:absolute;left:${bx}px;top:${by}px;width:${bw}px;height:${bh}px;border-radius:30px;background:#12161F;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;box-shadow:0 14px 34px rgba(18,22,31,.22);${fin ? '' : pop(seg(lt, 0, .4))}">
      <div style="position:absolute;left:50%;top:18px;transform:translateX(-50%);width:240px;height:14px;border-radius:7px;background:#3B4A63"></div>
      <div style="font-size:50px;font-weight:900;letter-spacing:-1.5px;margin-top:18px">${esc(sl.box || '1순위 이름 제출')}</div><div style="font-size:40px;font-weight:900;color:#FFD400">${inBox} / 12장</div></div>` + z;
    if (sl.label) z += `<div class="badge" style="position:absolute;left:${L.MX}px;top:${by + bh + 30}px;translate:-50% 0;background:${ACC};font-size:40px;padding:10px 34px;white-space:nowrap;${fin ? '' : pop(c01(p * 1.5 - .5))}">${esc(sl.label)}</div>`; }
  /* ⑥ 큰 질문 */
  if (s.question) { const p = PK(s.question.at, .5, seg(lt, .15, .5));
    z += `<div style="position:absolute;left:${L.RX}px;width:${L.RW}px;top:${L.ZT + 40}px;text-align:center;${pop(p)}"><div class="big gold" data-keep="1" style="font-size:${s.question.size || 86}px;line-height:1.18;letter-spacing:-3px">${br(s.question.text)}</div></div>`; }
  return { z, lines };
}
/* npbdraft: 12구단(또는 s.teams) 칩 + (선수 카드) + 아래 칸. 사용법은 콘티 생성기 gen_1005_long7.py 참고 */
SCENE.npbdraft = (lt, s) => {
  const L = npbLayout(s), CH = !!s._chain && s._prev && s._prev.type === 'npbdraft', P = CH ? s._prev : null;
  const sameT = CH && JSON.stringify(P.teams || null) === JSON.stringify(s.teams || null);
  const bid = s.bid || [], N = bid.length;
  const pIn = CH ? 1 : seg(lt, 0, .5);
  const PK = (at, d, fb) => (at != null && at < 0) ? 1 : pk(s, at, d, fb);
  const pb = N ? PK(s.bidAt, .7, seg(lt, .6, .7)) : 0, po = (N && s.winner && s.openAt != null) ? PK(s.openAt, .7, seg(lt, 2.8, .7)) : 0;
  /* 칩 */
  let chips = '';
  L.teams.forEach((x, i) => { const c = L.pos[i], on = bid.includes(x.n), lost = po > 0 && on && x.n !== s.winner, win = po > 0 && x.n === s.winner;
    const dim = N && pb > .2 && !on ? .22 : 1, pp = sameT ? 1 : seg(pIn * 2.2 + (CH ? lt * 2 : 0), i * .06, .5);
    chips += `<div style="position:absolute;left:${c.x}px;top:${c.y}px;${sameT ? '' : pop(pp)}"><div style="opacity:${dim};filter:grayscale(${lost ? c01(po * 2) : 0});">${npbChip(x, L.cw, L.chh, L.bigC ? 46 : L.noP ? 38 : 34, win ? `outline:6px solid ${GOLD};outline-offset:4px;transform:scale(${(1 + .08 * eo(po)).toFixed(3)})` : '')}</div></div>`; });
  /* 왼쪽 선수 카드(묶음 안에서는 그대로) */
  const pl = s.player || {}, src = photoSrc(pl.img);
  const pic = pl.sil ? NPB_SIL : src ? photoImg(Object.assign({}, pl, { fit: pl.fit || 'cover' }), src, 380, 470, pl.focus || '50% 10%') : '';
  const card = L.noP ? '' : `<div style="position:absolute;left:${L.shift}px;top:0;width:380px;${CH ? '' : rise(pIn, 40)}"><div class="pane" data-anchor="1" style="width:380px;border-radius:28px;overflow:hidden;border:5px solid ${N && pb > .3 ? ACC : '#E4E9F1'}">
      <div style="width:100%;height:470px;overflow:hidden;background:#E9EDF3;position:relative"><div class="pp" style="position:absolute;inset:0">${pic}</div></div>
      <div class="col" style="padding:14px 10px;gap:4px"><div style="font-size:52px;font-weight:900;letter-spacing:-1.5px">${esc(pl.name || '')}</div>${pl.sub ? `<div class="label" style="font-size:28px;color:${GRAY};white-space:nowrap">${esc(pl.sub)}</div>` : ''}</div></div>
      ${pl.tag ? `<div class="badge" style="position:absolute;left:-12px;top:-20px;background:${RED};font-size:32px;padding:6px 22px">${esc(pl.tag)}</div>` : ''}
      ${N && pb > .3 ? `<div class="badge" style="position:absolute;left:50%;top:-22px;translate:-50% 0;background:${ACC};font-size:30px;padding:6px 20px;white-space:nowrap;${pop(c01(pb * 1.5 - .4))}">${esc(s.bidLabel || (N + '개 구단 지명'))}</div>` : ''}</div>`;
  /* 아래 칸: 묶음 안에서 칸 종류가 바뀌면 앞 칸은 0.3초 흐려지며 사라지고 새 칸은 살짝 늦게 */
  const Zn = npbZone(s, lt, L, false);
  let zone = Zn.z, lines = Zn.lines;
  if (CH && npbZoneKey(P) !== npbZoneKey(s)) { const fo = 1 - c01(lt / .3);
    if (fo > 0) { const Zp = npbZone(P, 99, npbLayout(P), true); zone = `<div style="position:absolute;inset:0;opacity:${fo.toFixed(3)}">${Zp.z}</div><div style="position:absolute;inset:0;opacity:${c01((lt - .15) / .3).toFixed(3)}">${Zn.z}</div>`; } }
  let h = titleH(lt, s, 52, 18, CH && P.title === s.title);
  h += `<div style="position:relative;width:${L.W}px;height:${L.HH}px"><svg width="${L.W}" height="${L.HH}" style="position:absolute;left:0;top:0;overflow:visible">${lines}</svg>${chips}${card}${zone}</div>`;
  B(LR('', `<div class="col" style="width:100%;align-items:center">${h}</div>`));
};
/* snake: 지명 순서 — 칩 한 줄(order: 이름 배열, '\n' 줄바꿈 가능, KBO 팀이면 로고) + 화살표가 줄마다 방향 바꿔 쓸고 지나감.
   rows:[{label, dir:1|-1, at}] · hiFirst:{label, at} 첫 칸 강조 · ch 칩 높이 */
SCENE.snake = (lt, s) => {
  const order = s.order || [], n = order.length || 1, rows = s.rows || [{ label: '', dir: 1 }], W = 1700, CHH = s.ch || 130;
  const cw = Math.min(150, Math.floor((W - 18 * (n - 1)) / n)), gap = Math.floor((W - cw * n) / Math.max(1, n - 1)), top = s.logos ? 240 : CHH + 40;
  const hf = s.hiFirst, ph = hf ? pk(s, hf.at, .5, seg(lt, .4, .5)) : 0;
  let chips = '';
  order.forEach((nm, i) => { const t = T(nm), lg = s.logos && LOGO[(t || {}).code], x = NPB_BY[nm] || { n: nm, c: s.colors && s.colors[i] || '#3B4A63' };
    const hi = i === 0 && ph > 0 ? `outline:6px solid ${GOLD};outline-offset:5px;` : '';
    chips += `<div style="position:absolute;left:${i * (cw + gap)}px;top:0;width:${cw}px;${pop(seg(lt, .05 + i * .05, .4))}">${lg ? `<div class="chip" style="width:${cw}px;height:${cw}px;border-radius:30px;${hi}"><img src="${lg}"></div><div class="label" style="margin-top:8px;text-align:center;font-size:30px;color:${TXT};white-space:nowrap">${esc(t.nm || nm)}</div>` : npbChip(x, cw, CHH, s.fs || 30, hi)}</div>`; });
  if (hf) chips += `<div class="badge" style="position:absolute;left:0;top:-62px;background:${GOLD};color:#12161F;font-size:32px;padding:6px 20px;white-space:nowrap;${pop(ph)}">${esc(hf.label || '1순위')}</div>`;
  let arrows = '', y = top + 30;
  rows.forEach((r, k) => { const p = pk(s, r.at, 1.4, seg(lt, .5 + k * 1.6, 1.4)), dir = r.dir || 1, x0 = dir > 0 ? cw / 2 : W - cw / 2, x1 = dir > 0 ? W - cw / 2 : cw / 2, xt = x0 + (x1 - x0) * eo(p), col = k % 2 ? '#3B4A63' : ACC;
    arrows += `<svg width="${W}" height="80" style="position:absolute;left:0;top:${y}px;overflow:visible"><line x1="${x0}" y1="40" x2="${xt.toFixed(1)}" y2="40" stroke="${col}" stroke-width="14" stroke-linecap="round" opacity="${c01(p * 3)}"/>
      <g transform="translate(${xt.toFixed(1)},40) rotate(${dir > 0 ? 0 : 180})" opacity="${c01(p * 3)}"><path d="M-8,-26 L32,0 L-8,26 Z" fill="${col}"/></g></svg>
      <div class="badge" style="position:absolute;${dir > 0 ? 'left:0' : 'right:0'};top:${y - 44}px;background:${col};font-size:34px;padding:6px 22px;white-space:nowrap;${pop(c01(p * 3))}">${esc(r.label || '')}</div>`;
    y += 120; });
  let h = titleH(lt, s, 54, hf ? 84 : 30, s._chain && s._prev && s._prev.title === s.title);
  h += `<div style="position:relative;width:${W}px;height:${y}px">${chips}${arrows}</div>`;
  h += textH(lt, s, .6 + rows.length * 1.6, 64);
  wrapC(h);
};
/* icontiles: 그림 아이콘 + 숫자 카드(돈뭉치·입장권·달력·트로피·공). items:[{icon:'bills'|'ticket'|'calendar'|'trophy'|'ball', n(지폐 장수), v, k, top, at, color}]
   10/5 재검수(제목만 1~2초 떠 있음): 카드 틀은 처음부터 깔고, 안의 그림·숫자만 말할 때 채운다 */
const DICON = {
  bills: (n, c) => { let o = ''; for (let i = 0; i < n; i++) o += `<g transform="translate(0,${-i * 9})"><rect x="10" y="60" width="180" height="80" rx="10" fill="${c}" stroke="#fff" stroke-width="4"/><circle cx="100" cy="100" r="22" fill="#fff" opacity=".85"/><text x="100" y="110" text-anchor="middle" font-size="28" font-weight="900" fill="${c}">¥</text></g>`; return `<svg viewBox="0 0 200 150" width="100%" height="100%" style="overflow:visible">${o}</svg>`; },
  ticket: (n, c) => `<svg viewBox="0 0 200 150" width="100%" height="100%"><path d="M12,40 h176 a0,0 0 0 0 0,0 v22 a14,14 0 0 0 0,28 v22 h-176 v-22 a14,14 0 0 0 0,-28 z" fill="${c}"/><rect x="34" y="62" width="70" height="10" rx="5" fill="#fff" opacity=".9"/><rect x="34" y="82" width="46" height="10" rx="5" fill="#fff" opacity=".7"/><line x1="140" y1="46" x2="140" y2="106" stroke="#fff" stroke-width="4" stroke-dasharray="8 8"/></svg>`,
  calendar: (n, c) => `<svg viewBox="0 0 200 150" width="100%" height="100%"><rect x="30" y="30" width="140" height="110" rx="14" fill="#fff" stroke="${c}" stroke-width="8"/><rect x="30" y="30" width="140" height="34" rx="14" fill="${c}"/><rect x="60" y="18" width="12" height="28" rx="6" fill="${c}"/><rect x="128" y="18" width="12" height="28" rx="6" fill="${c}"/><text x="100" y="118" text-anchor="middle" font-size="44" font-weight="900" fill="${c}">${esc(n || '')}</text></svg>`,
  trophy: (n, c) => `<svg viewBox="0 0 200 150" width="100%" height="100%"><path d="M60,20 h80 v40 a40,40 0 0 1 -80,0 z" fill="${c}"/><path d="M60,30 h-25 a0,0 0 0 0 0,0 v20 a30,30 0 0 0 30,28" fill="none" stroke="${c}" stroke-width="10"/><path d="M140,30 h25 v20 a30,30 0 0 1 -30,28" fill="none" stroke="${c}" stroke-width="10"/><rect x="88" y="98" width="24" height="22" fill="${c}"/><rect x="60" y="120" width="80" height="16" rx="6" fill="${c}"/></svg>`,
  ball: (n, c) => `<svg viewBox="0 0 200 150" width="100%" height="100%"><circle cx="100" cy="75" r="56" fill="#fff" stroke="${c}" stroke-width="8"/><path d="M62,40 q20,35 0,70 M138,40 q-20,35 0,70" fill="none" stroke="${RED}" stroke-width="7" stroke-linecap="round"/></svg>`,
};
SCENE.icontiles = (lt, s) => {
  const its = s.items || [], n = its.length || 1, W = Math.min(560, Math.floor((1700 - 30 * (n - 1)) / n)), VS = s.vsize || (n <= 2 ? 110 : n === 3 ? 92 : 76);
  const pIn = s._chain ? 1 : seg(lt, 0, .4);
  let h = titleH(lt, s, 58, 30, s._chain && s._prev && s._prev.title === s.title);
  h += `<div class="row" style="gap:30px;align-items:stretch;justify-content:center">` + its.map((it, i) => { const c = it.color || ACC, p = pk(s, it.at, .5, seg(lt, .2 + i * .3, .5)), ic = DICON[it.icon] || DICON.ball, cnt = Math.max(1, Math.round((it.n || 1) * eo(p)));
    const on = `opacity:${c01(p * 1.4).toFixed(3)};transform:scale(${(.88 + .12 * eo(p)).toFixed(3)})`;
    return `<div class="pane col" style="width:${W}px;border-radius:32px;padding:28px 24px;gap:14px;justify-content:center;${it.hi ? `border:4px solid ${p > .3 ? 'var(--acc)' : '#E4E9F1'};background:#fff;` : ''}${rise(pIn, 30)}">
      <div style="width:${Math.min(240, W - 60)}px;height:${Math.round(Math.min(240, W - 60) * .75)}px;flex:0 0 auto;${on}">${ic(it.icon === 'bills' ? cnt : it.n, c)}</div>
      ${it.top ? `<div class="label" style="font-size:38px;font-weight:800;color:${GRAY};text-align:center;white-space:nowrap;${on}">${br(it.top)}</div>` : ''}
      <div class="num" style="font-size:${VS}px;font-weight:900;color:${c};text-align:center;line-height:1.05;letter-spacing:-3px;white-space:nowrap;${on}">${br(it.v || '')}</div>
      ${it.k ? `<div class="title" style="font-size:44px;font-weight:900;text-align:center;line-height:1.25;${on}">${br(it.k)}</div>` : ''}</div>`; }).join('') + `</div>`;
  h += textH(lt, s, .4 + n * .3, 68);
  wrapC(h);
};
/* vs2: 일본 1순위(12칩 동시 → 봉투) vs 한국 1순위(꼴찌 팀 고정) 한 화면 비교.
   10/5 재검수(왼쪽 칸만 먼저 떠서 한쪽으로 치우침): 두 칸 틀은 처음부터 가운데에 같이, 안의 내용만 차례로 */
SCENE.vs2 = (lt, s) => {
  const pIn = seg(lt, 0, .4), p1 = pk(s, s.leftAt, .6, seg(lt, .2, .6)), p2 = pk(s, s.rightAt, .6, seg(lt, 1.2, .6));
  const mini = NPB12.map((x, i) => `<div style="${pop(c01(p1 * 2 - i * .05))}">${npbChip(x, 118, 54, 24)}</div>`).join('');
  const kbo = (s.kbo || ['키움', '두산', 'KIA', '롯데', 'KT', 'NC', '삼성', 'SSG', '한화', 'LG']).map((n, i) => { const t = T(n); return `<div class="col" style="gap:6px;${pop(c01(p2 * 2 - i * .06))}"><div class="chip" style="width:66px;height:66px;border-radius:18px;${i === 0 && p2 >= 1 ? `outline:5px solid ${GOLD};outline-offset:3px;` : ''}"><img src="${LOGO[t.code] || ''}"></div></div>`; }).join('');
  const pane = (title, inner, foot, c, p) => `<div class="pane col" style="width:830px;border-radius:32px;padding:26px 24px 24px;gap:18px;border-top:12px solid ${c};${rise(pIn, 30)}">
    <div class="title" style="font-size:46px;font-weight:900;color:${c}">${esc(title)}</div>${inner}<div class="badge" style="background:${c};font-size:36px;padding:10px 28px;white-space:nowrap;${pop(c01(p * 1.6 - .5))}">${esc(foot)}</div></div>`;
  const left = pane(s.leftTitle || '일본 1순위', `<div style="display:grid;grid-template-columns:repeat(6,118px);gap:10px;justify-content:center">${mini}</div><div class="row" style="gap:10px;justify-content:center">${[0, 1, 2].map(i => `<div style="${pop(c01(p1 * 2 - .6 - i * .1))}">${envelopeH(90, 70, 0, false, false, '', false, true)}</div>`).join('')}</div>`, s.leftFoot || '12구단 동시 입찰 → 봉투 추첨', ACC, p1);
  const right = pane(s.rightTitle || '한국 1순위', `<div class="row" style="gap:8px;justify-content:center;flex-wrap:nowrap">${kbo}</div><svg width="760" height="50" style="overflow:visible"><line x1="20" y1="25" x2="${(20 + 700 * eo(p2)).toFixed(1)}" y2="25" stroke="#3B4A63" stroke-width="10" stroke-linecap="round" opacity="${c01(p2 * 4)}"/><g transform="translate(${(20 + 700 * eo(p2)).toFixed(1)},25)" opacity="${c01(p2 * 4)}"><path d="M-6,-20 L26,0 L-6,20 Z" fill="#3B4A63"/></g></svg>`, s.rightFoot || '지난해 꼴찌부터 순서대로', '#3B4A63', p2);
  let h = titleH(lt, s, 52, 22, false);
  h += `<div class="row" style="gap:36px;align-items:stretch;justify-content:center">${left}${right}</div>`;
  h += textH(lt, s, 2.0, 64);
  wrapC(h);
};
MOTION.npbdraft = s => (s.bid || []).length ? (s.rebidText ? 4.6 : s.winner ? 3.6 : 2.6) : s.slips ? 1.6 : 1.0;
MOTION.snake = s => .6 + ((s.rows || [{}]).length) * 1.6;
MOTION.icontiles = s => .4 + ((s.items || []).length) * .3 + .5;
MOTION.vs2 = () => 2.4;
