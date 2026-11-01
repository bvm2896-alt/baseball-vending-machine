base=open('/mnt/user-data/outputs/po34/template_long.html',encoding='utf-8').read()
a="${card(s.img, PWc, PHc)}${board}</div>`);"
assert base.count(a)==1
base=base.replace(a,"${card(s.img, PWc, PHc, '', s.img ? '' : (s.team || ''))}${board}</div>`);   /* 11/1: 사진 없는 기록판은 구단 색 + 로고 */")
a="'diamond', 'count', 'race', 'tline'].includes(s.type))));   /* 10/24 tline 추가 */"
assert base.count(a)==1
base=base.replace(a,"'diamond', 'count', 'race', 'tline', 'question', 'hero', 'board', 'water', 'probpair', 'probcalc', 'chalk', 'clip', 'scorecard', 'matchtbl'].includes(s.type))));   /* 10/24 tline 추가 · 11/1 hero·board·water 등 새 장면도 이어받기(사진·틀 그대로) */")
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
base=base[:i]+open('tpl/motionkit.js',encoding='utf-8').read()+'\n'+open('tpl/probcalc.js',encoding='utf-8').read()+'\n'+open('tpl/styles1101.js',encoding='utf-8').read()+'\n'+open('tpl/score1101.js',encoding='utf-8').read()+'\n'+open('tpl/match1101.js',encoding='utf-8').read()+'\n'+base[i:]
a="  slide(k, t, s, start);\n"
assert base.count(a)==1
base=base.replace(a,a+"  MK_tr(s, t, start);   /* 11/1 장면 전환 효과(s.tr) */\n")
open('template_long.html','w',encoding='utf-8').write(base); print('assembled')
