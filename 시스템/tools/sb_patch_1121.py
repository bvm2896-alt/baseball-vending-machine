# 스포츠 중계 플랫(EP.sb) 코드를 template_long.html 에 끼운다. 사용: python3 sb_patch.py <원본> <결과>
import sys, io
src, dst = sys.argv[1], sys.argv[2]
t = io.open(src, encoding='utf-8').read()
if '@@SB1121' in t:
    a = t.index('  /* @@SB1121'); b = t.index('/* @@SBEND */') + len('/* @@SBEND */\n'); t = t[:a] + t[b:]
def rep(a, b, n=1):
    global t
    assert t.count(a) == n, (a[:60], t.count(a)); t = t.replace(a, b)
sb = io.open('/home/claude/fx21/sb.js', encoding='utf-8').read()
# 1) 장면 그림
rep("  /* ── 카메라: 묶음(_cid) 단위로", sb + "  /* ── 카메라: 묶음(_cid) 단위로")
# 2) 켜는 값
if 'const SB = !!EP.sb;' not in t: rep("const MGON = EP.mg !== false;", "const MGON = EP.mg !== false;\nconst SB = !!EP.sb;   /* 11/21 스포츠 중계 플랫 */")
# 3) 글꼴·자막·진행 막대
CSS = "    if (SB) { const c2 = document.createElement('style'); c2.textContent = \"body,#stage,#stage *{font-family:'KBO','YG','Malgun Gothic',sans-serif!important}html,body,#stage{background:#16171C!important}#mg{letter-spacing:0!important}#sub span{background:#16171C!important;color:#fff!important;box-shadow:none!important;border-radius:0!important}#prog{background:rgba(0,0,0,.25)!important}#progBar{background:#E9C46A!important}#mgbg::after{display:none!important}\"; document.head.appendChild(c2); }   /* @@SBCSS */\n"
if '@@SBCSS' not in t: rep("    document.head.appendChild(css);\n    BG = document.createElement('div'); BG.id = 'mgbg';", "    document.head.appendChild(css);\n" + CSS + "    BG = document.createElement('div'); BG.id = 'mgbg';")
# 4) 바탕: 팀 색 단색 + 사선 띠(챕터가 바뀌면 왼→오로 닦임)
BGJ = """    if (SB) { const kc = Math.max(0, Math.min(k || 0, SC.length - 1)), s0 = SC[kc] || {}, c1 = s0.tc || '#1E3B36', c2 = s0.tc2 || '#173029', P = kc > 0 ? SC[kc - 1] : null, p1 = P ? (P.tc || '#1E3B36') : c1, p2 = P ? (P.tc2 || '#173029') : c2, dt = t - (kc === 0 ? 0 : BD[kc - 1]);
      const lay = (a, b) => `<div style="position:absolute;inset:0;background:${a}"></div><div style="position:absolute;left:-200px;top:610px;width:2400px;height:300px;background:${b};transform:rotate(-6deg)"></div>`;
      let key = c1 + c2, html = null;
      if ((p1 !== c1 || p2 !== c2) && dt >= 0 && dt < .45) { const q = eio(dt / .45); key = 'x' + q.toFixed(4) + c1 + p1; html = lay(p1, p2) + `<div style="position:absolute;inset:0;clip-path:inset(0 ${(FW * (1 - q)).toFixed(1)}px 0 0)">${lay(c1, c2)}</div>`; }
      if (BG._sb !== key) { BG._sb = key; BG.innerHTML = html || lay(c1, c2); } return; }   /* @@SBBG */
"""
if '@@SBBG' not in t: rep("  function paintBG(t, k) {\n", "  function paintBG(t, k) {\n" + BGJ)
# 5) 이음 판
BUGJ = """    if (SB) { const tc = (SC[Math.min(k, SC.length - 1)] || {}).tc || '#1E3B36'; BUG.innerHTML = `<div style="background:#ECE5D8;color:${tc};font-size:28px;font-weight:900;line-height:34px;padding:8px 18px">야구자판기</div>` + (txt || (prev && ft < 1) ? `<div style="position:relative;overflow:hidden;width:${W}px;height:50px;background:#16171C"><div style="position:absolute;left:18px;top:8px;right:0;height:34px;line-height:34px;font-size:28px;font-weight:700;color:#fff;white-space:nowrap">${cur}</div></div>` : ''); return; }   /* @@SBBUG */
"""
if '@@SBBUG' not in t: rep("    BUG.innerHTML = `<div style=\"background:${HOLO};color:${INK0};font-size:27px", BUGJ + "    BUG.innerHTML = `<div style=\"background:${HOLO};color:${INK0};font-size:27px")
# 6) 챕터 전환 선
a = "background:${GOLD};box-shadow:0 0 18px rgba(200,226,255,.6)\"></div>`; }"
if a in t: rep(a, "background:${SB ? '#E9C46A' : GOLD};box-shadow:${SB ? 'none' : '0 0 18px rgba(200,226,255,.6)'}\"></div>`; }")
io.open(dst, 'w', encoding='utf-8').write(t); print('ok', dst, len(t))
# 7) 새 사진 얼굴 자리(MGF)
import json, os
if os.path.exists('/home/claude/fx21/mgf_add.json'):
    t = io.open(dst, encoding='utf-8').read(); i = t.index('window.MGF = ') + 13; j = t.index('};', i) + 1
    m = json.loads(t[i:j]); m.update(json.load(io.open('/home/claude/fx21/mgf_add.json', encoding='utf-8')))
    if os.path.exists('/home/claude/fx21/mgf_fix.json'): m.update(json.load(io.open('/home/claude/fx21/mgf_fix.json', encoding='utf-8')))
    t = t[:i] + json.dumps(m, ensure_ascii=False) + t[j:]; io.open(dst, 'w', encoding='utf-8').write(t); print('MGF', len(m))
