# -*- coding: utf-8 -*-
"""10/17 사용자 "말 끊김을 내가 일일이 말해야 해?": 녹음된 줄 음성에서 실제로 쉰 자리를 재서 대본의 호흡(' / ')과 대조한다.
쓰기: python tools/pause_check.py episodes/<콘티>.json [음성폴더]
  - 대본에 없는 자리에서 0.22초 넘게 쉼 → '엉뚱한 쉼'(예: '이 루로 / 뛰다잡혔어요'처럼 단어 사이에서 끊김)
  - 대본 호흡 자리에서 쉼이 0.05초도 없음 → '붙어 읽음'(예: '뛰다잡혔어요')
쉼 위치는 '말하는 시간 비례'로 음절 번호에 놓는다(±1.5음절 오차). 결과 = 줄 번호, 어디서 쉬었는지(앞뒤 글자), 길이."""
import json, os, re, subprocess, sys

def syl_units(t):
    """글자별 길이 단위: 한글 1, 숫자·영문 1.3, 나머지 0"""
    return [1.0 if '가' <= c <= '힣' else 1.3 if c.isalnum() else 0.0 for c in t]

def silences(path, thr='-35dB', mind=0.05):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', f'silencedetect=n={thr}:d={mind}', '-f', 'null', '-'], capture_output=True, text=True)
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    d = float(re.findall(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)[0][2]) if 'Duration' in r.stderr else 0
    m = re.findall(r'Duration: (\d+):(\d+):([\d.]+)', r.stderr)
    if m: d = int(m[0][0]) * 3600 + int(m[0][1]) * 60 + float(m[0][2])
    if len(en) < len(st): en.append(d)
    return d, list(zip(st, en))

def check_line(path, narr, unplanned=0.22, missing=0.05):
    chunks = [c.replace('+', '') for c in narr.split(' / ')]
    text = ''.join(chunks); u = syl_units(text); U = sum(u) or 1
    bounds, acc = [], 0.0   # 호흡 경계의 누적 음절 위치
    for c in chunks[:-1]:
        acc += sum(syl_units(c)); bounds.append(acc)
    d, sil = silences(path)
    sil = [(a, b) for a, b in sil if a > 0.08 and b < d - 0.08]        # 앞뒤 무음 제외
    talk = d - sum(b - a for a, b in sil);
    # 앞뒤 무음도 빼고 말한 시간만
    _, allsil = silences(path)
    lead = allsil[0][1] if allsil and allsil[0][0] <= 0.08 else 0
    tail = (d - allsil[-1][0]) if allsil and allsil[-1][1] >= d - 0.08 else 0
    talk -= lead + tail
    def pos_of(t):   # 시각 → 누적 음절
        s = t - lead - sum(min(b, t) - a for a, b in sil if a < t)
        return max(0.0, min(U, s / max(talk, 1e-6) * U))
    def ctx(p):      # 음절 위치 p 앞뒤 글자
        k, acc2 = 0, 0.0
        for k, w in enumerate(u):
            acc2 += w
            if acc2 >= p - 1e-6: break
        return text[max(0, k - 4):k + 1] + '|' + text[k + 1:k + 5]
    found, out, cand = set(), [], []
    for a, b in sorted(sil, key=lambda x: x[0] - x[1]):   # 긴 쉼부터 호흡 자리에 짝짓는다(짧은 숨이 자리를 먼저 차지하지 않게)
        p = pos_of((a + b) / 2)
        free = [x for x in bounds if x not in found and abs(x - p) <= 2.0]
        if free: found.add(min(free, key=lambda x: abs(x - p))); continue
        if b - a >= unplanned: out.append(('엉뚱한 쉼', round(b - a, 2), ctx(p)))
    # 붙어 읽음은 '-다 / ' 처럼 문장 가운데 연결 자리(뛰다/잡혔어요)만 알린다 — 문장 끝·조사 뒤에서 안 쉬는 건 자연스러움
    for k, bd in enumerate(bounds):
        if bd not in found and re.search(r'(다가?|고|며|면서|지만|는데)$', chunks[k].strip()):
            out.append(('붙어 읽음', 0, ctx(bd)))
    return out

# 10/18 사용자(롱폼⑰ v5 지적 3가지)를 녹음 전에 대본에서 잡는다: python tools/pause_check.py --lint episodes/<콘티>.json
#  ① 감탄사('와~' 같은 말)로 시작하는 호흡  ② '-면서 / -면서'처럼 같은 끝말이 이어지는 호흡(듣기 불편)  ③ '이 차전'처럼 수와 단위가 떨어진 읽기(이/차전으로 끊김)
INTERJ = re.compile(r'^(와|우와|오|아|어|헐|대박|이야|아이고|자)(?! ?(회|점|대|이닝|번|명|개|타수|승|패|년|월|일|차전|연승|연패|루|할|푼|리|위|백|십|천|만))[ ,!~.]')   # '오 회말'(숫자 5)은 감탄사 아님
def lint_lines(narrs):
    out = []
    for i, n in enumerate(narrs):
        bs = [b.lstrip('+').strip() for b in n.split(' / ') if b.strip()]
        for b in bs:
            if INTERJ.match(b): out.append((i, '감탄사', b))
        ends = [re.sub(r'[.,!?]+$', '', b)[-2:] for b in bs]
        for k in range(1, len(ends)):
            if ends[k] == ends[k - 1] and ends[k] in ('면서', '는데', '지만', '었고', '했고', '하고', '나와', '해서', '어서', '아서'):
                out.append((i, '같은 끝말 연속', bs[k - 1] + ' / ' + bs[k]))
        for m in re.finditer(r'(?<![가-힣])(일|이|삼|사|오|칠|팔) (차전|연승|연패|루)', n):
            out.append((i, '수·단위 띄어 읽기', n[max(0, m.start() - 6):m.end() + 3]))
    return out

if __name__ == '__main__':
    if sys.argv[1] == '--lint':
        ep = json.load(open(sys.argv[2], encoding='utf-8')); w = lint_lines([l.get('narr', '') for l in ep['lines']])
        for x in w: print('%02d' % x[0], x[1], '|', x[2])
        print('대본 의심', len(w)); sys.exit(0)
    ep = json.load(open(sys.argv[1], encoding='utf-8'))
    vd = sys.argv[2] if len(sys.argv) > 2 else os.path.join('work', 'voice_' + os.path.splitext(os.path.basename(sys.argv[1]))[0])
    bad = 0
    for i, l in enumerate(ep['lines']):
        f = os.path.join(vd, f'{i:02d}.mp3')
        if not os.path.exists(f) or not l.get('narr'): continue
        r = check_line(f, l['narr'])
        if r:
            bad += 1; print(f'{i:02d}', l['narr']); [print('    ', *x) for x in r]
    print('의심 줄', bad)
