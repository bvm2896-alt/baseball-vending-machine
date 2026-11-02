base=open('/mnt/user-data/outputs/po34/template_long.html',encoding='utf-8').read()
a="${card(s.img, PWc, PHc)}${board}</div>`);"
assert base.count(a)==1
base=base.replace(a,"${card(s.img, PWc, PHc, '', s.img ? '' : (s.team || ''))}${board}</div>`);   /* 11/1: 사진 없는 기록판은 구단 색 + 로고 */")
a="'diamond', 'count', 'race', 'tline'].includes(s.type))));   /* 10/24 tline 추가 */"
assert base.count(a)==1
base=base.replace(a,"'diamond', 'count', 'race', 'tline', 'question', 'hero', 'board', 'water', 'probpair', 'probcalc', 'chalk', 'clip', 'scorecard', 'matchtbl', 'errs', 'rest', 'grid', 'mu_pgames', 'mu_hr2', 'mu_streak', 'mu_abs', 'mu_blocks', 'mu_closer', 'mu_pen2', 'ks_sched', 'ks_prob7', 'ks_outs', 'ks_rank', 'mu_donut', 'mu_fly', 'mu_choice', 'mu_inn', 'mu_pstat', 'vA_gap', 'vA_units', 'vA_errs', 'vA_battery', 'vA_innings', 'vA_days', 'vA_tiles', 'vA_games', 'vA_rank', 'vA_relay', 'vA_saves', 'vA_streak', 'vB_units', 'vB_meter', 'vB_only', 'vB_rings', 'vB_split', 'vB_three', 'vB_inn', 'vB_pen', 'vB_branch', 'vB_next'].includes(s.type))));   /* 10/24 tline 추가 · 11/1 hero·board·water 등 새 장면도 이어받기 · 11/1 22시 사용자 \"같은 글자 왜 없어졌다 나타나\" → 새 그림 장면 전부 이어받기 */")
q1="<div class=\"chip\" style=\"width:${LS}px;height:${LS}px;${pop(seg(lt, .5 + i * (n_ >= 8 ? .06 : .12), .4))}\">"
assert base.count(q1)==1
base=base.replace(q1,"<div class=\"chip\" style=\"width:${LS}px;height:${LS}px;${s._same ? '' : pop(seg(lt, .5 + i * (n_ >= 8 ? .06 : .12), .4))}\">")
lg="const leg = `<div class=\"row\" style=\"gap:28px;margin-top:12px;font-size:32px;font-weight:800;color:${GRAY}\"><span>한 칸 = 한 경기</span></div>`;"
assert base.count(lg)==1
base=base.replace(lg,"const leg = '';   /* 11/1 사용자 \"한 칸 한 경기 텍스트 빼\" */")
import re as _re
m=_re.search(r"  h \+= `<div class=\"row\" style=\"justify-content:center;gap:0;margin-bottom:4px\">.*?◀ 잘함.*?\n", base)
assert m
base=base[:m.start()]+"  /* 11/1 사용자 '잘함 못함 텍스트 빼' */\n"+base[m.end():]
rec='<div style="position:absolute;right:30px;bottom:18px;font-size:22px;font-weight:700;color:#5F6B80">기록: KBO 박스스코어</div>'
assert base.count(rec)==1
base=base.replace(rec,'')   # 11/1 사용자 '기록 표시 지워'
mg="let mega = `<div class=\"mega\" style=\"font-size:${s.size || 126}px;${pop(seg(lt, 0, .6))}\">${br(s.text || '여러분 생각은?')}</div>`;"
assert base.count(mg)==1
base=base.replace(mg,"let mega = `<div class=\"mega\" style=\"font-size:${s.size || 126}px;${s._same && s._prev.text === s.text ? '' : pop(seg(lt, 0, .6))}\">${br(s.text || '여러분 생각은?')}</div>`;   /* 11/1 mega 그대로 */")
pd="color:${hi ? 'var(--acc)' : TXT}\">${esc(it.team || '')}</div>"
assert base.count(pd)==1
base=base.replace(pd,"color:${hi ? 'var(--acc)' : TXT}\">${s.noName ? '' : esc(it.team || '')}</div>")   # 11/1 로고+구단 이름 중복 빼기
i=base.index('function render(t) {')
base=base[:i]+open('tpl/motionkit.js',encoding='utf-8').read()+'\n'+open('tpl/ref1102.js',encoding='utf-8').read()+'\n'+open('tpl/probcalc.js',encoding='utf-8').read()+'\n'+open('tpl/styles1101.js',encoding='utf-8').read()+'\n'+open('tpl/score1101.js',encoding='utf-8').read()+'\n'+open('tpl/match1101.js',encoding='utf-8').read()+'\n'+open('tpl/fx1101.js',encoding='utf-8').read()+'\n'+open('tpl/visB.js',encoding='utf-8').read()+'\n'+open('tpl/visA.js',encoding='utf-8').read()+'\n'+open('tpl/mu1101.js',encoding='utf-8').read()+'\n'+open('tpl/facex.js',encoding='utf-8').read()+'\n'+open('tpl/ks1102.js',encoding='utf-8').read()+'\n'+base[i:]
a="  slide(k, t, s, start);\n"
assert base.count(a)==1
base=base.replace(a,a+"  MK_tr(s, t, start);   /* 11/1 장면 전환 효과(s.tr) */\n")
a5="const keep = C_ && PG[k] && J({ ...PG[k], at: 0, appear: 0 }) === J({ ...g, at: 0, appear: 0 })"
assert base.count(a5)==1
base=base.replace(a5,a5+" && !(PG[k].at >= 50)")   # 11/1 롱폼㊱ 검수: 자리만 잡은 칸(at≥50)은 이어받지 않음
a6="background:#fff;border:8px solid ${c};display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px ${c}44;${ppop(p)}\">${LOGOI(g.win, 118)}"
assert base.count(a6)==1
base=base.replace(a6,"display:flex;align-items:center;justify-content:center;${ppop(p)}\">${LOGOI(g.win, 150)}")   # 11/1 롱폼㊱ 규칙 검수: 로고 틀(흰 원) 빼기
a7='${tchip(r.team, 70)}<div class="title" style="font-size:38px;font-weight:900">${esc(r.team)}</div>'
assert base.count(a7)==1
base=base.replace(a7,'${tchip(r.team, 70)}')   # 11/1 롱폼㊱ 규칙 검수: 점수판 로고+구단 이름 중복 빼기
a8="let w = n <= 2 ? 460 : n === 3 ? 400 : n === 4 ? 330 : 300,"
assert base.count(a8)==1
base=base.replace(a8,"let w = n <= 2 ? 460 : n === 3 ? 400 : n === 4 ? 330 : n === 5 ? 300 : 250,")   # 11/1 롱폼㊱ 검수: 6장 묶음이 화면 밖으로 넘침
open('template_long.html','w',encoding='utf-8').write(base); print('assembled')

# 11/1 20:17 사용자 "사진 무조건 가운데로" — 매 프레임 그린 뒤 얼굴 위치로 cover 사진 가로 맞춤
_t=open('template_long.html',encoding='utf-8').read()
_a="  (SCENE[s.type] || SCENE.big)(lt, s);"
assert _t.count(_a)==1
_t=_t.replace(_a,"  (SCENE[s.type] || SCENE.big)(lt, s); __faceFix(); __logoDedup(s);")
_b="  autoCenter(s);   /* 10/1 밤"
assert _t.count(_b)==1
_t=_t.replace(_b,"  autoCenter(s); __titleFix(s);   /* 10/1 밤")
open('template_long.html','w',encoding='utf-8').write(_t)

# 11/1 22:30 검수: 장면이 바뀌는 0.3초 크로스페이드(ghost)에 앞 장면이 제목 고정·얼굴 맞춤 없이 그려져 제목·내용이 아래로 툭 내려가던 것
_t=open('template_long.html',encoding='utf-8').read()
_c="NOW = start - 0.02; (SCENE[p.type] || SCENE.big)(99, p); autoCenter(p); NOW = keep;"
assert _t.count(_c)==1
_t=_t.replace(_c,"NOW = start - 0.02; const _bt = body.style.transform, _bo = body.style.opacity; body.style.transform = 'none'; (SCENE[p.type] || SCENE.big)(99, p); __faceFix(); __logoDedup(p); autoCenter(p); __titleFix(p); NOW = keep;")
_d="G.innerHTML = body.innerHTML; G.style.opacity"
assert _t.count(_d)==1
_t=_t.replace(_d,"G.innerHTML = body.innerHTML; body.style.transform = _bt; G.style.opacity")   # 새 장면 확대 효과(scale)가 남은 채로 재서 앞 장면 제목이 프레임마다 흔들리던 것
open('template_long.html','w',encoding='utf-8').write(_t)
# 11/2 검수 2차: 막대 5~6개 묶음(갈림길별 우승 확률)이 너무 작게 그려지던 것 — 5~6개는 한 단계 크게
_t=open('template_long.html',encoding='utf-8').read()
_e="const big = n <= 3, LS = big ? 56 : n <= 4 ? 48 : 38, NS = big ? 104 : n <= 4 ? 84 : 56, BH = big ? 64 : n <= 4 ? 52 : 30, PAD = big ? 26 : n <= 4 ? 18 : 6;"
assert _t.count(_e)==1
_t=_t.replace(_e,"const big = n <= 3, LS = big ? 56 : n <= 4 ? 48 : n <= 6 ? 42 : 38, NS = big ? 104 : n <= 4 ? 84 : n <= 6 ? 66 : 56, BH = big ? 64 : n <= 4 ? 52 : n <= 6 ? 36 : 30, PAD = big ? 26 : n <= 4 ? 18 : n <= 6 ? 10 : 6;")
open('template_long.html','w',encoding='utf-8').write(_t)
# 11/2 검수 2차: 사진·로고 둥실(±5px) — 장면 안에서 로고가 계속 오르내리고, 전환 0.3초(ghost)엔 둥실 없이 그려져 로고가 툭 튐(F-136·F-138) → 끔
_t=open('template_long.html',encoding='utf-8').read()
_f="document.querySelectorAll('#body .photo, #body .chip').forEach((el, i) => { el.style.translate = `0 ${(Math.sin(t * 1.8 + i * 1.3) * 5).toFixed(1)}px`; });"
assert _t.count(_f)==1
_t=_t.replace(_f,"/* 둥실 끔 */")
open('template_long.html','w',encoding='utf-8').write(_t)
# 11/2 10:00 사용자 "배경이 너무 흰색이라 눈이 살짝 부신데 약간 더 어둡게" — 화면 바탕만 한 톤 어둡게(카드·글자는 그대로)
import os as _os
_BG=_os.environ.get('K35_BG','#E4E8EE')
_t=open('template_long.html',encoding='utf-8').read()
for _a,_b in [("html,body{width:1920px;height:1080px;overflow:hidden;background:#F4F6FA}","html,body{width:1920px;height:1080px;overflow:hidden;background:%s}"%_BG),
              ("#stage{position:relative;width:1920px;height:1080px;background:#F4F6FA}","#stage{position:relative;width:1920px;height:1080px;background:%s}"%_BG),
              ("${ACC}22 0%, rgba(244,246,250,0) 70%),#F4F6FA`;","${ACC}22 0%, rgba(244,246,250,0) 70%),"+_BG+"`;")]:
    assert _t.count(_a)==1, _a[:30]; _t=_t.replace(_a,_b)
open('template_long.html','w',encoding='utf-8').write(_t)
# 11/2 10:04 사용자 "어두운 거 위주에 약간 밝은 걸 섞는 느낌 / 흰색·검은색만이 아니라 적절한 다른 색을 섞어도" — EP.theme 로 고르는 어두운 바탕 팔레트(navy·teal·navyW)
_t=open('template_long.html',encoding='utf-8').read()
_anchor="  function darkStage(t) {"
assert _t.count(_anchor)==1
_theme=r'''
  /* ── 11/2 어두운 바탕 팔레트: EP.theme = 'navy'(남색 바탕+밝은 남색 카드) / 'teal'(청록 바탕+밝은 청록 카드) / 'navyW'(남색 바탕+흰 카드) ── */
  const TP = { navy: { bg: '#121A2B', glow: 'rgba(70,110,200,.30)', card: '#1F2A42', soft: '#18223A', line: '#2F3C5A', tx: '#EEF2F8', mu: '#A3AEC4', sub: 'rgba(8,12,22,.94)', prog: '#26324D', kt: '#C9D2E2', pill: '#34415F' },
    teal: { bg: '#0F1F25', glow: 'rgba(40,150,160,.28)', card: '#1A323A', soft: '#15282E', line: '#2B4952', tx: '#EAF5F5', mu: '#9BB5B8', sub: 'rgba(5,14,17,.94)', prog: '#22393F', kt: '#C6D6D8', pill: '#2F4C55' },
    m1: { bg: '#2B3652', glow: 'rgba(110,150,230,.30)', card: '#3A4767', soft: '#334060', line: '#4C5A7C', tx: '#F1F4FA', mu: '#BCC5D8', sub: 'rgba(14,20,34,.94)', prog: '#3E4B6B', kt: '#D3DAE8', pill: '#4A5880' },
    m2: { bg: '#3A4664', glow: 'rgba(130,165,235,.30)', card: '#4A5779', soft: '#425071', line: '#5C6A8E', tx: '#F4F6FB', mu: '#C8D0E0', sub: 'rgba(16,22,38,.94)', prog: '#4D5A7C', kt: '#CFD7E6', pill: '#5A6890' },
    m3: { bg: '#4B5877', glow: 'rgba(150,180,240,.30)', card: '#5B698B', soft: '#536182', line: '#6E7CA0', tx: '#F6F8FC', mu: '#D2D9E7', sub: 'rgba(18,24,40,.94)', prog: '#5E6B8E', kt: '#CFD7E6', pill: '#6A79A0' },
    navyW: { bg: '#18233A', glow: 'rgba(90,130,220,.28)', card: null, soft: null, line: null, tx: '#F1F4FA', mu: '#B4BED2', sub: 'rgba(8,12,22,.94)', prog: '#2C3955', kt: '#C9D2E2', pill: '#34415F' } };
  const TPC = TP[EP.theme];
  window.__TPC = TPC || null;
  if (TPC) {
    const st = document.createElement('style');
    st.textContent = `html,body,#stage{background:${TPC.bg}!important}#brand{color:${TPC.tx}}#chap{background:#EA0029}#meta .d,#railTitle{color:${TPC.mu}!important}#prog{background:${TPC.prog}}
#sub span{background:${TPC.sub};box-shadow:0 0 0 2px rgba(255,255,255,.10)}` + (TPC.card ? `.card{background:${TPC.card};border-color:${TPC.line}}.photo{background:${TPC.soft};border-color:${TPC.line}}.pane{background:${TPC.card}!important;border-color:${TPC.line}!important}` : '');
    document.head.appendChild(st);
    const RP = TPC.card ? [[/background:\s*#12161F/gi, 'background:' + TPC.kt], [/background:\s*#fff(fff)?\b/gi, 'background:' + TPC.card], [/background:\s*white\b/gi, 'background:' + TPC.card],
      [/#E3E7EE/gi, TPC.line], [/#E9EDF3/gi, TPC.soft], [/#EEF1F6/gi, TPC.soft], [/#EEF1F5/gi, TPC.soft], [/#F4F6F9/gi, TPC.soft], [/#F4F6FA/gi, TPC.soft], [/#D5DBE4/gi, TPC.line], [/#D5DBE5/gi, TPC.line],
      [/#6A7382/gi, TPC.mu], [/#5B6576/gi, TPC.mu], [/#3B4A63/gi, TPC.mu], [/#8D97A6/gi, TPC.mu], [/#12161F/gi, TPC.tx]] : [];
    const dk = h => { RP.forEach(([a, b]) => { h = h.replace(a, b); }); return h; };
    const rgb = c => { const m = String(c).match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(',').map(parseFloat); return { r: v[0], g: v[1], b: v[2], a: v[3] == null ? 1 : v[3] }; };
    const lum = o => .299 * o.r + .587 * o.g + .114 * o.b;
    function domTheme(root) {
      const els = [...root.querySelectorAll('*')];
      if (TPC.card) els.forEach(el => { if (el.closest('[data-nodark],.chip,svg')) return; const cs = getComputedStyle(el), bg = rgb(cs.backgroundColor);
        if (bg && bg.a > .4 && lum(bg) > 232) el.style.backgroundColor = TPC.card; });
      /* 검은 칸(KT 색 막대·검은 알약): 글자 없는 막대는 밝은 강철색, 글자 있는 작은 알약은 한 톤 밝은 남색 */
      const underOf = el => { let p = el.parentElement; while (p && p !== root.parentElement) { const b = rgb(getComputedStyle(p).backgroundColor); if (b && b.a > .4) return b; p = p.parentElement; } return null; };
      els.forEach(el => { if (el.closest('[data-nodark],.chip,svg')) return; const cs = getComputedStyle(el), bg = rgb(cs.backgroundColor); if (!bg || bg.a < .4 || !(bg.r < 32 && bg.g < 32 && bg.b < 42 && bg.b - bg.r < 16)) return;
        const u = underOf(el); if (u && lum(u) > 120) return;
        const txt = (el.textContent || '').trim(), r = el.getBoundingClientRect();
        if (!txt && !el.querySelector('img')) el.style.backgroundColor = TPC.kt; else if (r.height < 140) el.style.backgroundColor = TPC.pill; });
      els.forEach(el => { if (el.closest('[data-nodark],.chip,svg')) return; const cs = getComputedStyle(el); const bw = parseFloat(cs.borderTopWidth), bc = rgb(cs.borderTopColor);
        if (bw > 0 && bc && lum(bc) < 45) el.style.borderColor = TPC.kt; });
      els.forEach(el => { if (el.closest('[data-nodark],.chip,svg')) return; const cs = getComputedStyle(el), fg = rgb(cs.color); if (!fg || lum(fg) > 140) return;
        let p = el, under = null; while (p && p !== root.parentElement) { const b = rgb(getComputedStyle(p).backgroundColor); if (b && b.a > .4) { under = b; break; } p = p.parentElement; }
        if (!under || lum(under) < 120) el.style.color = lum(fg) > 60 ? TPC.mu : TPC.tx; });
      els.forEach(el => { if (el.closest('[data-nodark],.chip,svg')) return; const cs = getComputedStyle(el), fg = rgb(cs.color); if (!fg || lum(fg) < 200) return;
        let p = el, under = null; while (p && p !== root.parentElement) { const b = rgb(getComputedStyle(p).backgroundColor); if (b && b.a > .4) { under = b; break; } p = p.parentElement; }
        if (under && lum(under) > 185) el.style.color = TPC.bg; });
    }
    const _B2 = B; B = h => { _B2(dk(h)); domTheme(document.getElementById('body')); };
  }
'''
_t=_t.replace(_anchor,_theme+_anchor)
_g="document.getElementById('stage').style.background = `radial-gradient(60% 50% at ${gx}% ${gy}%, ${ACC}22 0%, rgba(244,246,250,0) 70%),"
assert _t.count(_g)==1
_t=_t.replace(_g,"document.getElementById('stage').style.background = window.__TPC ? `radial-gradient(60% 55% at ${gx}% ${gy}%, ${window.__TPC.glow} 0%, rgba(0,0,0,0) 70%),${window.__TPC.bg}` : `radial-gradient(60% 50% at ${gx}% ${gy}%, ${ACC}22 0%, rgba(244,246,250,0) 70%),")
open('template_long.html','w',encoding='utf-8').write(_t)

# 11/2 레퍼런스 디자인: 화면 전체 사진 바탕 레이어(#sbg) — 매 프레임 바탕을 그린 직후
_t=open('template_long.html',encoding='utf-8').read()
_h="  slide(k, t, s, start);\n"
assert _t.count(_h)==1
_t=_t.replace(_h,"  if (window.__sbgPaint) window.__sbgPaint(kk, t, start);\n"+_h)
open('template_long.html','w',encoding='utf-8').write(_t)
