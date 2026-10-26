# 10/25 롱폼㉙ 검수 — 사용자 "사진이 너무 자주 바뀌고 틀의 크기가 자주 바뀌니까 보는게 너무 불편해" / "너무 빨리 틀의 크기가 바뀌어"
# pstat: ① 같은 사람 묶음에서 사진만 바뀌면 틀은 그대로 두고 새 사진이 겹쳐 나타난다 ② 날짜 칸(steps d) 폭을 같은 사람 묶음 전체의 가장 긴 글에 맞춰 고정
#        ③ 새 그림: seasons(시즌 칸 채우기) · mini(작은 얼굴 + 이름) · hops(구단 로고를 따라 이동)
import io, re, sys
for p in sys.argv[1:]:
    s = io.open(p, encoding='utf-8').read()
    if '@@PSTAT1025' in s: print('skip(이미 적용)', p); continue
    a = s.index('SCENE.pstat = (lt, s) => {')
    # ① 사진
    i = s.index('const photo = `', a); j = s.index('`;', i) + 2
    old = s[i:j]
    new = ("/* @@PSTAT1025 ① */ const xfade = !keepP && keepN && pr && photoSrc(pr.img) && photoSrc(s.img);\n"
           "    const photo = xfade ? `<div style=\"flex:0 0 auto;position:relative\">${NP({ img: pr.img, team: pr.team, focus: pr.focus }, PW, PH_)}<div style=\"position:absolute;left:0;top:0;opacity:${c01(seg(lt, 0, .6)).toFixed(3)}\">${NP({ img: s.img, team: s.team, focus: s.focus }, PW, PH_)}</div></div>`\n"
           "      : " + old[len('const photo = '):])
    s = s[:i] + new + s[j:]
    # ② steps 날짜 칸 폭
    k = s.index("if (z.type === 'steps') {", a)
    s = s[:k] + s[k:].replace("if (z.type === 'steps') {",
        "if (z.type === 'steps') { /* @@PSTAT1025 ② */ const SDW = Math.max(V ? 170 : 210, 10 + Math.ceil(Math.max(0, ...[s, ...CHN(s, 'pstat').filter(x => x.name === s.name)].flatMap(x => (x.viz || []).filter(y => y.type === 'steps').flatMap(y => (y.items || []).map(w => TW(w.d, V ? 32 : 36, 800)))))));", 1)
    seg_ = s[k:k + 4000]
    seg2 = seg_.replace('<div style="width:${V ? 170 : 210}px;font-size:${V ? 32 : 36}px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(x.d)}</div>',
                        '<div style="width:${SDW}px;flex:0 0 auto;font-size:${V ? 32 : 36}px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(x.d)}</div>', 1)
    if seg2 == seg_: s = s[:k] + s[k:].replace("if (z.type === 'steps') { /* @@PSTAT1025 ② */ " + s[k:].split("if (z.type === 'steps') { /* @@PSTAT1025 ② */ ",1)[1].split(';',1)[0] + ';', "if (z.type === 'steps') {", 1); print('  steps 폭: 이 파일엔 이미 같은 기능(세로 sDW) — 건너뜀')
    else: s = s[:k] + seg2 + s[k + 4000:]
    # ③ 새 그림
    k = s.index("if (z.type === 'duo')", a)
    NEW = r'''/* @@PSTAT1025 ③ seasons: 시즌 칸이 차례로 차오른다 {type:'seasons', title, items:[{t:'2019', at, hi, c, w}]} */
      if (z.type === 'seasons') { const its = z.items || [], BW = z.bw || (V ? 92 : 104);
        return `<div class="col" style="gap:12px;align-items:flex-start">${z.title ? `<div style="font-size:34px;font-weight:800;color:${GRAY};white-space:nowrap;opacity:${c01(P({ at: z.titleAt ?? ((its[0] || {}).at ?? 0) }, .4) * 2).toFixed(3)}">${esc(z.title)}</div>` : ''}<div class="row" style="gap:10px;flex-wrap:nowrap;align-items:stretch">` + its.map(x => { const q = P(x, .35), c = x.hi ? (x.c ? colOf(x.c) : '#E8A100') : (x.c ? colOf(x.c) : '#3B6FD8');
          return `<div style="position:relative;width:${x.w || BW}px;height:${V ? 96 : 110}px;border-radius:16px;background:#E3E8F0;overflow:hidden;flex:0 0 auto;transform:scale(${(x.hi ? .9 + .1 * eo(q) : 1).toFixed(3)})"><div style="position:absolute;left:0;top:0;bottom:0;width:${(100 * eo(q)).toFixed(1)}%;background:${c}"></div><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:${x.fs || (V ? 30 : 34)}px;font-weight:900;color:${q > .45 ? '#fff' : '#9AA6B8'};white-space:nowrap;line-height:1.05;text-align:center">${br(x.t)}</div></div>`; }).join('') + `</div></div>`; }
      /* mini: 작은 얼굴 + 이름(이름이 나오는 다른 선수) {type:'mini', items:[{img, name, team, k, at}]} */
      if (z.type === 'mini') return `<div class="row" style="gap:34px;flex-wrap:nowrap;align-items:center">` + (z.items || []).map(x => { const q = P(x, .45), src = photoSrc(x.img), D = V ? 96 : 112;
          return `<div class="row" style="gap:14px;align-items:center;flex-wrap:nowrap;${pop(q)}"><div style="position:relative;width:${D}px;height:${D}px;border-radius:50%;overflow:hidden;border:4px solid #fff;box-shadow:0 8px 20px rgba(18,22,31,.18);background:#E9EDF3;flex:0 0 auto">${src ? faceImg(src, x, '50% 18%') : ''}</div><div class="col" style="align-items:flex-start;gap:0"><div class="row" style="gap:8px;align-items:center;flex-wrap:nowrap">${x.team ? LOGOI(x.team, 36) : ''}<b style="font-size:${V ? 36 : 40}px;font-weight:900;white-space:nowrap">${esc(x.name || '')}</b></div>${x.k ? `<div style="font-size:${V ? 28 : 30}px;font-weight:800;color:${GRAY};white-space:nowrap">${esc(x.k)}</div>` : ''}</div></div>`; }).join('') + `</div>`;
      /* hops: 구단 로고를 따라 이어지는 길(선이 차오르며 다음 로고) {type:'hops', items:[{team, t, at} | {icon, t, at, hi}]} */
      if (z.type === 'hops') { const its = z.items || [], LG = V ? 80 : 96; let h = `<div class="row" style="gap:0;flex-wrap:nowrap;align-items:flex-start">`;
        its.forEach((x, i) => { const q = P(x, .45);
          if (i) h += `<div style="width:${V ? 36 : 52}px;height:8px;border-radius:4px;background:#C9D2E0;position:relative;flex:0 0 auto;margin:${LG / 2 - 4}px 6px 0"><div style="position:absolute;left:0;top:0;bottom:0;width:${(100 * eo(c01(q * 1.6))).toFixed(1)}%;background:${ACC};border-radius:4px"></div></div>`;
          h += `<div class="col" style="align-items:center;gap:6px;${pop(c01(q * 1.6 - .5))}">${x.team ? LOGOI(x.team, LG) : `<div style="width:${LG}px;height:${LG}px;border-radius:50%;background:${x.hi ? tc : '#3B4A63'};color:#fff;display:flex;align-items:center;justify-content:center;font-size:${V ? 26 : 30}px;font-weight:900;white-space:nowrap">${esc(x.icon || '')}</div>`}<div style="font-size:${V ? 26 : 30}px;font-weight:900;white-space:nowrap;color:${x.hi ? tc : TXT}">${esc(x.t || '')}</div></div>`; });
        return h + `</div>`; }
      '''
    s = s[:k] + NEW + s[k:]
    io.open(p, 'w', encoding='utf-8').write(s); print('patched', p)
