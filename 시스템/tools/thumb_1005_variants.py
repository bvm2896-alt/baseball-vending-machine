# 10/5 밤 롱폼⑦ 썸네일 A·B·C 시안 생성(클라우드에서 씀: SP 경로와 thpv7.py 는 scratchpad 기준) — 최종은 C, gen_1005_long7.py thumb 에 들어감
import json, os, subprocess, sys
SP = os.path.dirname(os.path.abspath(__file__))
GLOW = "filter:drop-shadow(0 0 12px #000) drop-shadow(0 0 12px rgba(0,0,0,.9)) drop-shadow(0 6px 8px rgba(0,0,0,.95))"
TXT = "font-family:'GM','NB',sans-serif;color:#fff;line-height:1;white-space:nowrap;letter-spacing:-2px;" + GLOW
RED = "#E3101E"
NPB12 = [('요미우리','#F97709','#fff'),('한신','#FFE201','#12161F'),('DeNA','#004B9E','#fff'),('히로시마','#E30C19','#fff'),('야쿠르트','#1E3A6B','#fff'),('주니치','#0D3B8E','#fff'),
         ('소프트뱅크','#F5C400','#12161F'),('니혼햄','#0B5BAA','#fff'),('라쿠텐','#8A0F2E','#fff'),('세이부','#13225B','#fff'),('롯데','#121212','#fff'),('오릭스','#B2922B','#fff')]

def env(w, h, win=False, qm=False, up=0.62):
    pw, ph = round(w*.78), round(h*.9); u = round(up*h*.62) if win else 0
    stamp = (f'<div style="position:absolute;left:50%;top:32%;transform:translate(-50%,-50%) rotate(-10deg);border:{max(4,round(w*.025))}px solid {RED};color:{RED};border-radius:12px;padding:6px 14px;'
             f'font-size:{round(h*.15)}px;line-height:1.08;font-weight:900;white-space:nowrap;text-align:center;font-family:GM,sans-serif">교섭권<br>확정</div>') if win else ''
    q = f'<div style="position:absolute;left:0;bottom:{round(h*.06)}px;width:{w}px;text-align:center;font-size:{round(h*.42)}px;line-height:1;font-weight:900;color:#B08A3E;font-family:GM,sans-serif">?</div>' if qm else ''
    return (f'<div style="position:relative;width:{w}px;height:{h}px">'
            f'<div style="position:absolute;left:{(w-pw)//2}px;bottom:{round(h*.08)}px;width:{pw}px;height:{ph}px;background:#fff;border:3px solid #D6DBE3;border-radius:8px;transform:translateY({-u}px);box-shadow:0 6px 14px rgba(0,0,0,.35)">{stamp}</div>'
            f'<div style="position:absolute;left:0;bottom:0;width:{w}px;height:{round(h*.62)}px;background:linear-gradient(180deg,#F6E9C8,#E3CB92);border:3px solid #B9924E;border-radius:10px;box-sizing:border-box"></div>'
            f'<div style="position:absolute;left:0;bottom:{round(h*.62)-3}px;width:0;height:0;border-left:{w//2}px solid transparent;border-right:{w//2}px solid transparent;border-top:{round(h*.3)}px solid #D9BE82;transform-origin:50% 0;transform:rotate({-170 if win else 0}deg);opacity:{0 if win else 1}"></div>{q}</div>')

def at(x, y, inner, rot=0, z='', op=1, sc=1):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg) scale({sc});opacity:{op};{z}">{inner}</div>'

def chip(n, c, t, w=176, h=60, fs=32):
    return f'<div style="width:{w}px;height:{h}px;border-radius:16px;background:{c};color:{t};display:flex;align-items:center;justify-content:center;font-size:{fs}px;font-weight:900;letter-spacing:-1px;font-family:GM,sans-serif;box-shadow:0 8px 18px rgba(0,0,0,.55);border:3px solid rgba(255,255,255,.85)">{n}</div>'

HIG = "누끼/거친_경기_히구치_포효0826"   # 543x800, 몸 상자 x0~494
DOME = {"img": "상황별/거친_도쿄돔_도시대항", "blur": 1, "bright": 0.6, "sat": 0.95, "pos": "50% 40%"}
base = {"layout": "hero", "rays": 0, "sparks": 0, "top": "", "band": False, "textStyle": "glow", "glow": 12, "ls": -2}

# ── A: 봉투 추첨 — 히구치 왼쪽, 오른쪽 위 큰 당첨 봉투(교섭권 확정) + 뒤로 '?' 봉투들, 글씨 오른쪽 아래
A = dict(base)
A.update(people=[{"img": HIG, "z": 2, "left": 10, "top": -14, "h": 790, "wpx": 536, "glow": 22}],
         bgImg=dict(DOME, over="linear-gradient(270deg,rgba(4,8,22,.78) 0%,rgba(4,8,22,.45) 50%,rgba(4,8,22,.25) 100%),linear-gradient(180deg,rgba(0,0,0,0) 50%,rgba(0,0,0,.6) 100%)"),
         vig="radial-gradient(120% 100% at 40% 40%,rgba(0,0,0,0) 50%,rgba(0,0,0,.7) 100%)",
         layers=[{"z": 1, "html": at(600, 70, env(150, 140, qm=True), -14, op=.85) + at(1100, 40, env(140, 130, qm=True), 12, op=.85) + at(560, 214, env(120, 112, qm=True), 8, op=.7) + at(1150, 200, env(120, 112, qm=True), -10, op=.7)},
                 {"z": 3, "html": at(790, 110, env(300, 250, win=True, up=.6), 6)}],
         txtCss="left:auto;right:34px;top:auto;bottom:30px;align-items:flex-end",
         maxW=760, lines=[[{"t": "일본 드래프트 1순위는", "c": "#fff", "s": 62}],
                          [{"t": "제비뽑기", "c": "#fff", "s": 128, "box": RED, "mt": 14}, {"t": "로", "c": "#fff", "s": 128}],
                          [{"t": "뽑는다", "c": "#fff", "s": 128, "mt": 6}]])

# ── B: 일본 vs 한국 반반 — 왼쪽 일본(도쿄돔·히구치), 오른쪽 한국(KBO 드래프트 무대·하현승), 가운데 VS
HHS = "누끼/거친_경기_하현승_드래프트_키움제공_up"   # 683x1060
def half_bg(img, poly, tint):
    return (f'<div style="position:absolute;inset:0;clip-path:polygon({poly})"><img src="{{{{IMG}}}}" style="position:absolute;inset:-6px;width:calc(100% + 12px);height:calc(100% + 12px);object-fit:cover;filter:blur(1.5px) brightness(.55)">'
            f'<div style="position:absolute;inset:0;background:{tint}"></div></div>')
lab = lambda x, y, t, bg, fg='#fff', fs=46: at(x, y, f'<div style="background:{bg};color:{fg};font-family:GM,sans-serif;font-size:{fs}px;font-weight:900;padding:8px 22px 4px;border-radius:12px;white-space:nowrap;box-shadow:0 6px 0 rgba(0,0,0,.5)">{t}</div>')
big = lambda x, y, t, fs=112, c='#fff', anchor='0': f'<div style="position:absolute;left:{x}px;top:{y}px;transform:translateX({anchor});{TXT};font-size:{fs}px;color:{c}">{t}</div>'
B = dict(base)
B.update(bgCss="#05070D", people=[{"img": HIG, "z": 2, "left": 40, "top": 40, "h": 700, "wpx": 475, "glow": 18},
                                   {"img": HHS, "z": 2, "left": 820, "top": 70, "h": 700, "wpx": 451, "glow": 18}],
         layers=[{"z": 0, "img": "상황별/거친_도쿄돔_도시대항", "html": half_bg('', '0 0,690px 0,590px 100%,0 100%', 'linear-gradient(180deg,rgba(120,0,10,.25),rgba(10,0,0,.55))')},
                 {"z": 0, "img": "상황별/거친_드래프트_단체", "html": half_bg('', '690px 0,100% 0,100% 100%,590px 100%', 'linear-gradient(180deg,rgba(0,30,110,.3),rgba(0,0,20,.6))')},
                 {"z": 1, "html": '<svg width="1280" height="720" style="position:absolute;inset:0"><line x1="690" y1="0" x2="590" y2="720" stroke="#fff" stroke-width="8"/></svg>'},
                 {"z": 5, "html": lab(40, 34, '🇯🇵 일본', RED) .replace('🇯🇵 ', '') + lab(1240, 34, '한국', '#1F4FD8').replace('left:1240px', 'left:1240px;transform-origin:100% 0;translate:-100% 0')
                         + at(640, 300, '<div style="width:150px;height:150px;border-radius:50%;background:#FFD400;color:#12161F;font-family:GM,sans-serif;font-size:76px;font-weight:900;display:flex;align-items:center;justify-content:center;border:6px solid #fff;box-shadow:0 10px 30px rgba(0,0,0,.7);letter-spacing:-4px">VS</div>').replace('left:640px', 'left:565px')
                         + big(30, 470, '1순위 겹치면', 60) + big(30, 548, '<span style="background:%s;padding:4px 14px 0;border-radius:10px">제비뽑기</span>' % RED, 118)
                         + big(1250, 470, '1순위는', 60, anchor='-100%') + big(1250, 548, '<span style="background:#1F4FD8;padding:4px 14px 0;border-radius:10px">꼴찌 팀</span>', 118, anchor='-100%')}],
         lines=[])

# ── C: 12구단이 몰린다 — 히구치 가운데, 12구단 이름표가 양옆에서 몰려듦(화살표), 아래 큰 글씨
C = dict(base)
L, R = NPB12[:6], NPB12[6:]
ch = ''
for i, (n, c, t) in enumerate(L):
    ch += at(40 + (i % 2) * 40 + i * 14, 40 + i * 64, chip(n, c, t), (-6 + i * 2))
for i, (n, c, t) in enumerate(R):
    ch += at(1064 - (i % 2) * 40 - i * 14, 40 + i * 64, chip(n, c, t), (6 - i * 2))
arrows = '<svg width="1280" height="720" style="position:absolute;inset:0"><defs><marker id="ah" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#FFD400"/></marker></defs>' + \
         ''.join(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y2}" stroke="#FFD400" stroke-width="6" stroke-linecap="round" marker-end="url(#ah)" opacity=".95"/>' for x1, x2, y, y2 in [(300, 430, 120, 170), (300, 430, 260, 240), (980, 850, 120, 170), (980, 850, 260, 240)]) + '</svg>'
C.update(people=[{"img": "누끼/거친_경기_히구치_오지2026봄", "z": 2, "left": 339, "top": 4, "h": 760, "wpx": 602, "glow": 18}],
         bgImg=dict(DOME, bright=0.55, over="radial-gradient(70% 80% at 50% 35%,rgba(4,8,22,.15) 0%,rgba(4,8,22,.7) 100%),linear-gradient(180deg,rgba(0,0,0,0) 50%,rgba(0,0,0,.65) 100%)"),
         vig="radial-gradient(120% 100% at 50% 40%,rgba(0,0,0,0) 55%,rgba(0,0,0,.7) 100%)",
         layers=[{"z": 3, "html": ch}, {"z": 3, "html": arrows}, {"z": 4, "html": at(778, 292, '<div style="display:flex;align-items:center;gap:10px;background:rgba(10,14,26,.82);border:3px solid rgba(255,255,255,.9);border-radius:999px;padding:8px 22px 6px 16px;font-family:GM,sans-serif;color:#fff;font-size:32px;letter-spacing:-1px;white-space:nowrap;box-shadow:0 6px 16px rgba(0,0,0,.6)"><span style="width:10px;height:28px;border-radius:5px;background:#E3101E;display:inline-block"></span>히구치 신</div>')}],
         txtCss="bottom:14px", maxW=1220,
         lines=[[{"t": "일본은 드래프트 1순위를", "c": "#fff", "s": 62}],
                [{"t": "제비뽑기", "c": "#fff", "s": 150, "box": RED, "mt": 12}, {"t": "로 뽑는다", "c": "#fff", "s": 150}]])

for k, v in dict(A=A, B=B, C=C).items():
    json.dump(v, open(f'{SP}/th_{k}.json', 'w', encoding='utf-8'), ensure_ascii=False)
    r = subprocess.run(['python3', f'{SP}/../thpv7.py', f'{SP}/th_{k}.json', f'{SP}/th_{k}.jpg'], capture_output=True, text=True)
    print(k, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-400:])
