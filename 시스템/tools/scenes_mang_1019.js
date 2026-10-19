/* @@MANG1019 10/19 롱폼⑳ 「KIA 한국시리즈 우승 망상회」 — 사용자 "볼게 많아야 하고 귀여운 애니메이션도… 창의적으로".
   tools/inject_mang_1019.py 가 template_long.html 의 function render 앞에 넣는다(원본을 고치면 다시 주입).
   ① 망냥이: 채널 오리지널 꼬마 호랑이(구단 마스코트 아님). 장면마다 s.mood(idle·cheer·cry·calc·faint·shock·think·wave·love·sweat)·s.say(말풍선)
   ② 효과: s.fx = 'confetti'·'rain'·'sparkle'·'fireworks' (여러 개면 배열)
   ③ 망상 구름 전환: s.dreamNo(망상 n번째 경기) 가 있으면 장면 첫 1.3초 동안 생각 구름이 피어올랐다 터진다
   ④ 새 장면: mscore(전광판 망상 스코어) · dice(주사위 6개 중 1개) · gauge(확률이 줄어드는 배터리) */
(function () {
  const cl = (v, a, b) => Math.max(a, Math.min(b, v)), e3 = x => 1 - Math.pow(1 - cl(x, 0, 1), 3);
  const bk = x => { x = cl(x, 0, 1); const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const H = (i, k) => { const v = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return v - Math.floor(v); };   /* 결정적 난수(프레임마다 같은 값) */
  const KIA = '#EA0029', GOLD = '#FFC93C', OR = '#FF9A2E', OR2 = '#F07C12', CREAM = '#FFF1DC', INK = '#3A2414', PINK = '#FF8FA3';

  /* ── ① 망냥이 ───────────────────────────────────────────── */
  /* 구단별 오리지널 캐릭터(10/19 사용자 "구단마다 캐릭터" — 실제 구단 마스코트를 닮게 그리지 않는다. 팀 이름·팀색에서 따온 일반 동물)
     KIA 꼬마 호랑이(망냥이) · 삼성 파란 갈기 꼬마 사자 · LG 자주색 쌍둥이 아기곰 · KT 검정 꼬마 부엉이 */
  const SPC = { tiger: { B: OR, E: OR2, C: CREAM }, lion: { B: '#F3C25B', E: '#C99332', C: '#FFF3D6', M: '#1F5BD6' },
    bear: { B: '#C8336A', E: '#93204D', C: '#FFE1EA' }, owl: { B: '#3A3A44', E: '#1C1C22', C: '#ECE4D6' } };
  const TEAM_SP = { KIA: 'tiger', '삼성': 'lion', LG: 'bear', KT: 'owl' };
  function crit(sp, mood, t, o = {}) {
    if (sp === 'bear' && !o.single) return `<svg viewBox="-10 -20 220 250" width="100%" height="100%" style="overflow:visible"><g transform="translate(-34 34) scale(.74)">${crit('bear', mood, t, Object.assign({}, o, { single: 1, inner: 1 }))}</g><g transform="translate(78 44) scale(.68)">${crit('bear', mood, t + .37, Object.assign({}, o, { single: 1, inner: 1, hammer: null }))}</g></svg>`;
    const P = SPC[sp] || SPC.tiger, BC = P.B, EC = P.E, CC = P.C;
    const spd = { idle: 2.2, cheer: 6, cry: 3, calc: 4, faint: 1.5, shock: 9, think: 1.6, wave: 3, love: 3, sweat: 5 }[mood] || 2.2;
    const jump = mood === 'cheer' ? -Math.abs(Math.sin(t * 6)) * 26 : mood === 'love' ? -Math.abs(Math.sin(t * 3)) * 10 : Math.sin(t * spd) * 5;
    const tilt = mood === 'faint' ? 18 + Math.sin(t * 1.5) * 4 : mood === 'shock' ? Math.sin(t * 40) * 2.5 : mood === 'cry' ? Math.sin(t * 6) * 2 : Math.sin(t * 1.7) * 3;
    const blink = (t % 3.1) < 0.12 && !['faint', 'shock', 'love'].includes(mood);
    const EX = sp === 'owl' ? [74, 126] : [78, 122], EY = sp === 'owl' ? 88 : 90;
    let eyes;
    if (mood === 'faint') eyes = EX.map(x => `<path d="M${x - 9} ${EY - 4}q9 -10 18 0q-9 10 -14 2q4 -6 8 0" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round" transform="rotate(${(t * 300) % 360} ${x} ${EY - 2})"/>`).join('');
    else if (mood === 'love') eyes = EX.map(x => `<path d="M${x} ${EY + 8} l-12 -12 a7 7 0 0 1 12 -6 a7 7 0 0 1 12 6 z" fill="${KIA}" transform="scale(${1 + .12 * Math.sin(t * 8)})" transform-origin="${x} ${EY}"/>`).join('');
    else if (mood === 'cheer') eyes = EX.map(x => `<path d="M${x - 11} ${EY + 2} q11 -14 22 0" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`).join('');
    else if (blink) eyes = EX.map(x => `<path d="M${x - 10} ${EY} h20" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`).join('');
    else { const r = mood === 'shock' ? 13 : 11, ry = mood === 'shock' ? 13 : 14, lx = mood === 'calc' ? Math.sin(t * 4) * 2 : 0;
      eyes = EX.map(x => `<ellipse cx="${x + lx}" cy="${EY}" rx="${r}" ry="${ry}" fill="${INK}"/><circle cx="${x + lx + 4}" cy="${EY - 5}" r="4.5" fill="#fff"/><circle cx="${x + lx - 3}" cy="${EY + 5}" r="2" fill="#fff"/>`).join(''); }
    const mouth = sp === 'owl' ? `<path d="M92 104 l8 16 l8 -16z" fill="#F2A23A" stroke="#C97A12" stroke-width="2" stroke-linejoin="round"/>${mood === 'cheer' || mood === 'shock' ? '<path d="M94 112 l6 10 l6 -10" fill="#B3263A"/>' : ''}` : ({ cheer: `<path d="M86 116 q14 22 28 0 z" fill="#B3263A"/><path d="M92 124 q8 6 16 0" fill="${PINK}"/>`, cry: `<path d="M88 124 q12 -10 24 0" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>`,
      shock: `<ellipse cx="100" cy="122" rx="7" ry="${9 + Math.sin(t * 20) * 1.5}" fill="#B3263A"/>`, faint: `<path d="M90 120 q5 5 10 0 q5 5 10 0" fill="none" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/>`,
      sweat: `<path d="M90 121 q10 -6 20 0" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>`, love: `<path d="M88 116 q12 14 24 0" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>` }[mood]
      || `<path d="M100 112 v5 M100 117 q-7 7 -12 1 M100 117 q7 7 12 1" fill="none" stroke="${INK}" stroke-width="3.5" stroke-linecap="round"/>`);
    const arm = (side, ang) => `<g transform="rotate(${ang} ${100 + side * 40} 158)"><rect x="${100 + side * 40 - 11}" y="150" width="22" height="46" rx="11" fill="${BC}" stroke="${EC}" stroke-width="2"/><circle cx="${100 + side * 40}" cy="194" r="11" fill="${CC}"/></g>`;
    let aL = 20, aR = -20;
    if (mood === 'cheer') { aL = 150 + Math.sin(t * 12) * 18; aR = -150 - Math.sin(t * 12) * 18; }
    else if (mood === 'wave') { aR = -140 + Math.sin(t * 9) * 28; }
    else if (mood === 'cry') { aL = 140 + Math.sin(t * 10) * 6; aR = -140 - Math.sin(t * 10) * 6; }
    else if (mood === 'calc') { aL = 70; aR = -60 + Math.sin(t * 14) * 10; }
    else if (mood === 'shock') { aL = 120; aR = -120; }
    else if (mood === 'think') { aR = -125; }
    else if (mood === 'faint') { aL = 40; aR = -70; }
    else if (mood === 'love') { aL = 110; aR = -110; }
    /* 뿅망치: o.hammer = 오른팔 각도(도). 빨간 망치머리 + 노란 양끝 */
    let ham = '';
    if (o.hammer != null) { aR = o.hammer;
      ham = `<g transform="rotate(${o.hammer} 140 158)"><rect x="135" y="186" width="10" height="70" rx="5" fill="#F6D365" stroke="#C99A20" stroke-width="2"/><g transform="translate(140 262)"><rect x="-38" y="-22" width="76" height="44" rx="18" fill="#FF3B5C" stroke="#B3132F" stroke-width="3"/><rect x="-46" y="-24" width="14" height="48" rx="6" fill="#FFD43B" stroke="#C99A20" stroke-width="2"/><rect x="32" y="-24" width="14" height="48" rx="6" fill="#FFD43B" stroke="#C99A20" stroke-width="2"/><path d="M-20 -10 h20" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".6"/></g></g>`; }
    let extra = '';
    if (mood === 'cry') for (let i = 0; i < 4; i++) { const p = (t * 1.6 + i / 4) % 1; [70, 130].forEach((x, k) => { extra += `<path d="M${x + (k ? 8 : -8) * p * 3} ${104 + p * 70} q-6 10 0 14 q6 -4 0 -14z" fill="#6EC6FF" opacity="${1 - p}"/>`; }); }
    if (mood === 'sweat' || mood === 'shock') { const p = (t * 1.2) % 1; extra += `<path d="M150 ${50 + p * 30} q-8 14 0 18 q8 -4 0 -18z" fill="#8ED6FF" opacity="${1 - p * .8}"/>`; }
    if (mood === 'faint') for (let i = 0; i < 3; i++) { const a = t * 3 + i * 2.1; extra += `<text x="${100 + Math.cos(a) * 58}" y="${22 + Math.sin(a) * 14}" font-size="22" text-anchor="middle" fill="${GOLD}">★</text>`; }
    if (mood === 'think') for (let i = 0; i < 3; i++) { const q = .5 + .5 * Math.sin(t * 3 - i); extra += `<circle cx="${150 + i * 16}" cy="${30 - i * 14}" r="${5 + i * 3}" fill="#fff" stroke="#C9D0DB" stroke-width="2" opacity="${q.toFixed(2)}"/>`; }
    if (mood === 'calc') { const d = ['1', '17', '17%'][Math.floor(t * 2) % 3]; extra += `<g transform="translate(62 150) rotate(-8)"><rect width="76" height="62" rx="10" fill="#2E3440"/><rect x="7" y="7" width="62" height="20" rx="4" fill="#B8F5C8"/><text x="64" y="23" font-size="16" font-weight="900" text-anchor="end" fill="#1F3B28" font-family="monospace">${d}</text>${[0, 1, 2].map(c => [0, 1].map(r => `<rect x="${9 + c * 21}" y="${33 + r * 13}" width="15" height="9" rx="2" fill="${(Math.floor(t * 8) % 6) === c + r * 3 ? GOLD : '#7A8394'}"/>`).join('')).join('')}</g>`; }
    if (mood === 'cheer') for (let i = 0; i < 4; i++) { const a = t * 2 + i * 1.57, r = 74 + Math.sin(t * 5 + i) * 6; extra += `<text x="${100 + Math.cos(a) * r}" y="${100 + Math.sin(a) * r * .7}" font-size="20" text-anchor="middle" fill="${GOLD}" opacity="${.5 + .5 * Math.sin(t * 7 + i)}">✦</text>`; }
    const tailW = Math.sin(t * 4) * 12;
    const tail = sp === 'tiger' ? `<path d="M140 196 q40 6 46 -26 q${4 + tailW} -22 ${-8 + tailW} -30" fill="none" stroke="${BC}" stroke-width="16" stroke-linecap="round"/><path d="M176 178 l10 -4 M180 162 l10 0" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`
      : sp === 'lion' ? `<path d="M140 196 q40 6 44 -24" fill="none" stroke="${BC}" stroke-width="12" stroke-linecap="round"/><circle cx="${184 + tailW * .3}" cy="168" r="13" fill="${P.M}"/>` : sp === 'bear' ? `<circle cx="146" cy="200" r="11" fill="${BC}" stroke="${EC}" stroke-width="2"/>` : '';
    const ears = sp === 'owl' ? `<path d="M46 52 l8 -40 l26 26z" fill="${BC}" stroke="${EC}" stroke-width="3" stroke-linejoin="round"/><path d="M154 52 l-8 -40 l-26 26z" fill="${BC}" stroke="${EC}" stroke-width="3" stroke-linejoin="round"/>`
      : sp === 'lion' ? `<circle cx="54" cy="46" r="15" fill="${BC}" stroke="${EC}" stroke-width="3"/><circle cx="146" cy="46" r="15" fill="${BC}" stroke="${EC}" stroke-width="3"/>`
      : `<circle cx="50" cy="44" r="${sp === 'bear' ? 23 : 21}" fill="${BC}" stroke="${EC}" stroke-width="3"/><circle cx="50" cy="44" r="10" fill="${sp === 'bear' ? CC : PINK}"/><circle cx="150" cy="44" r="${sp === 'bear' ? 23 : 21}" fill="${BC}" stroke="${EC}" stroke-width="3"/><circle cx="150" cy="44" r="10" fill="${sp === 'bear' ? CC : PINK}"/>`;
    const mane = sp === 'lion' ? Array.from({ length: 14 }, (_, i) => { const a = i / 14 * 6.283 + Math.sin(t * 2) * .03; return `<circle cx="${(100 + Math.cos(a) * 66).toFixed(1)}" cy="${(92 + Math.sin(a) * 64).toFixed(1)}" r="24" fill="${P.M}"/>`; }).join('') : '';
    const stripes = sp === 'tiger' ? `<path d="M88 32 q12 14 24 0 M84 46 q16 12 32 0 M38 86 l16 4 M38 102 l16 -2 M162 86 l-16 4 M162 102 l-16 -2" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>` : '';
    const bodyStr = sp === 'tiger' ? `<path d="M58 172 l14 4 M56 188 l14 0 M142 172 l-14 4 M144 188 l-14 0" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>` : sp === 'owl' ? `<path d="M88 176 q6 6 12 0 q6 6 12 0 M84 192 q8 6 16 0 q8 6 16 0" fill="none" stroke="#B8AE9C" stroke-width="3"/>` : '';
    const face = sp === 'owl' ? `<circle cx="74" cy="88" r="26" fill="#fff" stroke="#F2A23A" stroke-width="5"/><circle cx="126" cy="88" r="26" fill="#fff" stroke="#F2A23A" stroke-width="5"/>`
      : `<ellipse cx="100" cy="114" rx="32" ry="24" fill="${CC}"/><circle cx="62" cy="110" r="10" fill="${PINK}" opacity=".7"/><circle cx="138" cy="110" r="10" fill="${PINK}" opacity=".7"/>`;
    const nose = sp === 'owl' ? '' : `<path d="M93 104 h14 l-7 8z" fill="${INK}" stroke="${INK}" stroke-width="2" stroke-linejoin="round"/>`;
    const hat = sp === 'tiger' ? `<path d="M62 30 q38 -26 76 0 l-8 10 q-30 -16 -60 0z" fill="${KIA}"/>`
      : sp === 'owl' ? `<g transform="rotate(-8 100 20)"><path d="M58 32 q42 -14 84 0 l-10 6 q-32 -8 -64 0z" fill="#111"/><path d="M70 30 l26 -62 l30 60z" fill="#111" stroke="#2A2A2A" stroke-width="2"/><path d="M73 24 q26 -8 52 0 l-2 7 q-24 -6 -48 0z" fill="#EC1C2A"/><text x="101" y="10" font-size="20" text-anchor="middle" fill="#FFD43B">★</text></g>` : '';
    const sq = o.squash || 0, sx = 1 + sq * .18, sy = 1 - sq * .28, fl = o.flip ? -1 : 1;
    const g = `<g transform="translate(100 230) scale(${(fl * sx).toFixed(3)} ${sy.toFixed(3)}) translate(-100 -230)"><g transform="translate(0 ${jump.toFixed(1)}) rotate(${tilt.toFixed(1)} 100 200)">
      ${tail}${arm(-1, aL)}${o.hammer != null ? '' : arm(1, aR)}
      <ellipse cx="100" cy="182" rx="50" ry="40" fill="${BC}" stroke="${EC}" stroke-width="3"/>
      <ellipse cx="100" cy="190" rx="30" ry="26" fill="${CC}"/>${bodyStr}
      <ellipse cx="78" cy="218" rx="18" ry="11" fill="${sp === 'owl' ? '#F2A23A' : BC}" stroke="${EC}" stroke-width="2"/><ellipse cx="122" cy="218" rx="18" ry="11" fill="${sp === 'owl' ? '#F2A23A' : BC}" stroke="${EC}" stroke-width="2"/>
      ${mane}${ears}
      <circle cx="100" cy="92" r="64" fill="${BC}" stroke="${EC}" stroke-width="3"/>${stripes}${face}
      ${eyes}${nose}${mouth}${hat}${o.hammer != null ? arm(1, aR) + ham : ''}
      ${extra}</g></g>`;
    return o.inner ? g : `<svg viewBox="-10 -20 220 250" width="100%" height="100%" style="overflow:visible">${g}</svg>`;
  }
  /* 10/20 01:17 사용자 "캐릭터는 (그림 그대로 말고) 새로 만들어서 표정도 바뀌게, 대신 비슷한 느낌으로" →
     채널 오리지널 꼬마 호랑이 '망냥이 2'(굵은 검정 외곽선·큰 머리 스티커 그림체). 구단 로고·글자 없음. 가슴 번호 17 = 우승 확률 17%.
     mood: idle·cheer·cry·calc·faint·shock·think·wave·love·sweat */
  const mang = (mood, t) => {
    const O = '#1A1210', SK = '#F8C253', SK2 = '#1A1210', CR = '#FFF4E2', RD = '#E8213B', PK = '#FF8FA3', W = 4.5;
    const blink = (t % 3.3) < 0.12 && !['faint', 'shock', 'love', 'cheer', 'cry'].includes(mood);
    const bob = { cheer: -Math.abs(Math.sin(t * 6)) * 16, love: -Math.abs(Math.sin(t * 3)) * 8, shock: -6 }[mood] ?? Math.sin(t * 2.2) * 3;
    const tilt = { faint: 14 + Math.sin(t * 1.5) * 3, shock: Math.sin(t * 40) * 2, cry: Math.sin(t * 6) * 2, think: -6 + Math.sin(t * 1.6) * 2, wave: Math.sin(t * 3) * 3 }[mood] ?? Math.sin(t * 1.7) * 2.5;
    /* 팔 각도(어깨 기준, 0 = 아래로) */
    let aL = 18, aR = -18;
    if (mood === 'cheer') { aL = 150 + Math.sin(t * 12) * 14; aR = -150 - Math.sin(t * 12) * 14; }
    else if (mood === 'wave') aR = -140 + Math.sin(t * 9) * 26;
    else if (mood === 'cry') { aL = 28 + Math.sin(t * 10) * 4; aR = -28 - Math.sin(t * 10) * 4; }
    else if (mood === 'calc') { aL = 60; aR = -60; }
    else if (mood === 'shock') { aL = 110; aR = -110; }
    else if (mood === 'think') aR = -130;
    else if (mood === 'love') { aL = 95; aR = -95; }
    const arm = (x, ang) => `<g transform="rotate(${ang.toFixed(1)} ${x} 196)"><rect x="${x - 11}" y="190" width="22" height="46" rx="11" fill="${SK}" stroke="${O}" stroke-width="${W}"/><path d="M${x - 9} 214 l9 3 M${x + 9} 214 l-9 3 M${x - 9} 224 l8 2" stroke="${O}" stroke-width="3.5" stroke-linecap="round"/><circle cx="${x}" cy="234" r="11" fill="${CR}" stroke="${O}" stroke-width="${W}"/></g>`;
    /* 몸: 흰 유니폼 + 빨간 목둘레·소매 + 번호 17, 짧은 다리 */
    const body = `<rect x="76" y="246" width="20" height="26" rx="9" fill="${SK}" stroke="${O}" stroke-width="${W}"/><rect x="104" y="246" width="20" height="26" rx="9" fill="${SK}" stroke="${O}" stroke-width="${W}"/>
      <path d="M66 210 L66 250 Q100 262 134 250 L134 210 Z" fill="${SK}" stroke="${O}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M62 196 Q62 176 100 176 Q138 176 138 196 L137 230 Q100 240 63 230 Z" fill="#FFFFFF" stroke="${O}" stroke-width="${W}" stroke-linejoin="round"/>
      <path d="M84 178 Q100 192 116 178" fill="none" stroke="${RD}" stroke-width="6" stroke-linecap="round"/>
      <path d="M64 220 Q100 230 136 220" fill="none" stroke="${RD}" stroke-width="5"/>`;   /* 10/20 사용자 "유니폼에 17 없애" */
    /* 귀: 둥근 귀 + 분홍 속귀 */
    const ears = `<circle cx="44" cy="52" r="20" fill="${SK}" stroke="${O}" stroke-width="${W}"/><circle cx="44" cy="55" r="10" fill="${CR}"/>
      <circle cx="156" cy="52" r="20" fill="${SK}" stroke="${O}" stroke-width="${W}"/><circle cx="156" cy="55" r="10" fill="${CR}"/>`;
    /* 얼굴: 큰 둥근 머리 + 크림색 볼·입 둘레 + 이마 줄무늬 3개 + 볼 줄무늬 */
    const head = `<ellipse cx="100" cy="104" rx="72" ry="66" fill="${SK}" stroke="${O}" stroke-width="${W}"/>
      <path d="M29 96 l22 6 l-21 4 z M30 114 l20 5 l-19 5 z" fill="${O}"/>
      <path d="M171 96 l-22 6 l21 4 z M170 114 l-20 5 l19 5 z" fill="${O}"/>
      <path d="M58 128 Q66 110 100 112 Q134 110 142 128 Q138 158 100 160 Q62 158 58 128 Z" fill="${CR}"/>`;
    /* 꼬리: 몸 뒤 오른쪽으로 말려 올라간 줄무늬 꼬리 */
    const tail = `<path d="M128 240 Q170 244 172 210 Q174 188 160 182" fill="none" stroke="${O}" stroke-width="${16 + W * 2}" stroke-linecap="round"/>
      <path d="M128 240 Q170 244 172 210 Q174 188 160 182" fill="none" stroke="${SK}" stroke-width="16" stroke-linecap="round"/>
      <path d="M150 236 l4 12 M166 222 l12 4 M170 202 l12 -2" stroke="${O}" stroke-width="5" stroke-linecap="round"/>`;
    /* 모자: 앞으로 쓴 빨간 야구모자 + 흰 야구공 마크, 챙은 오른쪽 */
    const cap = `<g transform="translate(100 56) scale(.8) translate(-100 -56)"><path d="M50 58 Q54 22 100 20 Q146 22 150 58 Q100 46 50 58 Z" fill="${RD}" stroke="${O}" stroke-width="${W}" stroke-linejoin="round"/>
      <circle cx="100" cy="38" r="10" fill="#fff" stroke="${O}" stroke-width="3"/><path d="M95 32 q4 6 0 12 M105 32 q-4 6 0 12" fill="none" stroke="${RD}" stroke-width="2"/></g>`;   /* 10/20 사용자 "모자는 좀 작게" → 80% */
    /* 눈 */
    const EX = [74, 126], EY = 104;
    let eyes;
    if (blink) eyes = EX.map(x => `<path d="M${x - 10} ${EY} q10 5 20 0" fill="none" stroke="${O}" stroke-width="5" stroke-linecap="round"/>`).join('');
    else if (mood === 'cheer' || mood === 'wave') eyes = EX.map(x => `<path d="M${x - 11} ${EY + 4} q11 -15 22 0" fill="none" stroke="${O}" stroke-width="5.5" stroke-linecap="round"/>`).join('');
    else if (mood === 'love') eyes = EX.map(x => `<path d="M${x} ${EY + 10} l-12 -12 a7 7 0 0 1 12 -7 a7 7 0 0 1 12 7 z" fill="${RD}" stroke="${O}" stroke-width="2.5" transform="scale(${(1 + .1 * Math.sin(t * 8)).toFixed(3)})" transform-origin="${x} ${EY}"/>`).join('');
    else if (mood === 'cry') eyes = EX.map((x, k) => `<path d="M${x - 11} ${EY - 2} q11 9 22 0" fill="none" stroke="${O}" stroke-width="5" stroke-linecap="round"/><path d="M${x + (k ? -12 : -2)} ${EY - 16} l${k ? -10 : 10} 6" stroke="${O}" stroke-width="4" stroke-linecap="round"/>`).join('');
    else if (mood === 'faint') eyes = EX.map(x => `<path d="M${x - 8} ${EY - 8} l16 16 M${x + 8} ${EY - 8} l-16 16" stroke="${O}" stroke-width="5" stroke-linecap="round"/>`).join('');
    else { const r = mood === 'shock' ? 15 : 13, lx = mood === 'think' ? -3 : mood === 'calc' ? Math.sin(t * 4) * 2 : 0, ly = mood === 'think' ? -4 : mood === 'calc' ? 3 : 0;
      eyes = EX.map(x => `<ellipse cx="${x}" cy="${EY}" rx="${r}" ry="${r + 2}" fill="${O}"/><circle cx="${x + 4 + lx}" cy="${EY - 5 + ly}" r="${mood === 'shock' ? 3.5 : 5}" fill="#fff"/><circle cx="${x - 4 + lx}" cy="${EY + 5 + ly}" r="2.2" fill="#fff"/>`).join(''); }
    /* 눈썹: 감정에 따라 */
    const brow = { sweat: 'M60 84 l22 -6 M140 84 l-22 -6', cry: 'M60 82 l22 -7 M140 82 l-22 -7', think: 'M62 82 l20 2 M118 78 l20 -4', shock: 'M60 78 q12 -8 24 -2 M116 76 q12 -6 24 2', calc: 'M62 84 l20 -3 M138 84 l-20 -3', cheer: 'M60 76 q11 -9 22 -3 M118 73 q11 -6 22 3', wave: 'M60 76 q11 -9 22 -3 M118 73 q11 -6 22 3', love: 'M60 74 q11 -9 22 -3 M118 71 q11 -6 22 3', faint: 'M60 80 q6 -5 11 0 q6 5 11 0 M118 80 q6 -5 11 0 q6 5 11 0' }[mood] || 'M60 80 q11 -7 22 -3 M118 77 q11 -4 22 3';   /* 10/20 사용자 "기본은 왜 눈썹이 없어 — 없는 것 다" */
    const brows = brow ? `<path d="${brow}" fill="none" stroke="${O}" stroke-width="6.5" stroke-linecap="round"/>` : '';
    /* 코·입 */
    const nose = `<path d="M90 118 q10 -5 20 0 q-3 9 -10 10 q-7 -1 -10 -10 z" fill="#E8607A" stroke="${O}" stroke-width="3" stroke-linejoin="round"/>`;
    const mouth = ({ cheer: `<path d="M84 134 q16 22 32 0 z" fill="#B3263A" stroke="${O}" stroke-width="3"/><path d="M92 142 q8 6 16 0" fill="${PK}"/>`,
      wave: `<path d="M86 134 q14 16 28 0" fill="none" stroke="${O}" stroke-width="4" stroke-linecap="round"/>`,
      love: `<path d="M86 134 q14 14 28 0" fill="none" stroke="${O}" stroke-width="4" stroke-linecap="round"/>`,
      cry: `<path d="M86 146 q14 -12 28 0" fill="none" stroke="${O}" stroke-width="4" stroke-linecap="round"/>`,
      shock: `<ellipse cx="100" cy="142" rx="9" ry="12" fill="#B3263A" stroke="${O}" stroke-width="3"/>`,
      sweat: `<path d="M88 142 q6 -5 12 0 q6 5 12 0" fill="none" stroke="${O}" stroke-width="4" stroke-linecap="round"/>`,
      faint: `<path d="M88 142 q6 -5 12 0 q6 5 12 0" fill="none" stroke="${O}" stroke-width="4" stroke-linecap="round"/>`,
      think: `<path d="M92 140 l16 -2" stroke="${O}" stroke-width="4" stroke-linecap="round"/>`,
      calc: `<path d="M92 139 q8 5 16 0" fill="none" stroke="${O}" stroke-width="4" stroke-linecap="round"/>` })[mood]
      || `<path d="M100 128 v5 M100 133 q-8 8 -14 2 M100 133 q8 8 14 2" fill="none" stroke="${O}" stroke-width="4" stroke-linecap="round"/>`;
    const blush = ['cheer', 'love', 'wave', 'idle'].includes(mood) || !mood ? `<ellipse cx="56" cy="126" rx="10" ry="6" fill="${PK}" opacity=".7"/><ellipse cx="144" cy="126" rx="10" ry="6" fill="${PK}" opacity=".7"/>` : '';
    /* 감정 효과 */
    let ex = '';
    if (mood === 'cry') for (let i = 0; i < 3; i++) { const p = (t * 1.6 + i / 3) % 1; [70, 130].forEach((x, k) => { ex += `<path d="M${x + (k ? 6 : -6) * p * 3} ${112 + p * 60} q-6 10 0 14 q6 -4 0 -14z" fill="#6EC6FF" opacity="${(1 - p).toFixed(2)}"/>`; }); }
    if (mood === 'sweat' || mood === 'shock') { const p = (t * 1.2) % 1; ex += `<path d="M170 ${56 + p * 30} q-9 15 0 19 q9 -4 0 -19z" fill="#8ED6FF" stroke="${O}" stroke-width="2" opacity="${(1 - p * .8).toFixed(2)}"/>`; }
    if (mood === 'think') for (let i = 0; i < 3; i++) { const q = .5 + .5 * Math.sin(t * 3 - i); ex += `<circle cx="${172 + i * 12}" cy="${30 - i * 14}" r="${4 + i * 3}" fill="#fff" stroke="${O}" stroke-width="2.5" opacity="${q.toFixed(2)}"/>`; }
    if (mood === 'love') for (let i = 0; i < 3; i++) { const p = (t * .8 + i / 3) % 1; ex += `<text x="${40 + i * 60}" y="${40 - p * 50}" font-size="${22 + i * 4}" fill="${RD}" opacity="${(1 - p).toFixed(2)}">♥</text>`; }
    if (mood === 'cheer') for (let i = 0; i < 4; i++) { const a = t * 2 + i * 1.57, r = 96 + Math.sin(t * 5 + i) * 6; ex += `<text x="${(100 + Math.cos(a) * r).toFixed(0)}" y="${(130 + Math.sin(a) * r * .7).toFixed(0)}" font-size="22" text-anchor="middle" fill="${GOLD}" opacity="${(.5 + .5 * Math.sin(t * 7 + i)).toFixed(2)}">✦</text>`; }
    if (mood === 'faint') for (let i = 0; i < 3; i++) { const a = t * 3 + i * 2.1; ex += `<text x="${(100 + Math.cos(a) * 56).toFixed(0)}" y="${(22 + Math.sin(a) * 12).toFixed(0)}" font-size="20" text-anchor="middle" fill="${GOLD}">★</text>`; }
    if (mood === 'calc') { const d = ['1', '17', '17%'][Math.floor(t * 2) % 3]; ex += `<g transform="translate(64 190) rotate(-6)"><rect width="72" height="56" rx="9" fill="#2E3440" stroke="${O}" stroke-width="3"/><rect x="6" y="6" width="60" height="18" rx="4" fill="#B8F5C8"/><text x="62" y="21" font-size="15" font-weight="900" text-anchor="end" fill="#1F3B28" font-family="monospace">${d}</text>${[0, 1, 2].map(c => [0, 1].map(r => `<rect x="${8 + c * 20}" y="${30 + r * 12}" width="14" height="8" rx="2" fill="${(Math.floor(t * 8) % 6) === c + r * 3 ? GOLD : '#7A8394'}"/>`).join('')).join('')}</g>`; }
    const g = `<g transform="translate(0 ${bob.toFixed(1)}) rotate(${tilt.toFixed(1)} 100 250)"><g transform="translate(0 -16)">${arm(66, aL)}${arm(134, aR)}${body}</g>${ears}${head}${cap}${brows}${eyes}${blush}${nose}${mouth}${ex}</g>`;
    return `<svg viewBox="-10 -14 220 300" width="100%" height="100%" style="overflow:visible">${g}</svg>`;
  };
  window.mangSVG = mang;

  /* ── ② 효과 ───────────────────────────────────────────── */
  function fxHTML(kind, lt) {
    let h = '';
    if (kind === 'confetti' || kind === 'fireworks') {
      const C = [KIA, GOLD, '#FFFFFF', '#12161F', '#FF7A59'], n = kind === 'fireworks' ? 120 : 80;
      for (let i = 0; i < n; i++) {
        const t0 = H(i, 1) * .6, p = lt - t0; if (p < 0) continue;
        const x = H(i, 2) * 1920 + Math.sin(p * 3 + i) * 40, y = -40 + p * (260 + H(i, 3) * 260), r = (p * (200 + H(i, 4) * 400) + i * 37) % 360;
        if (y > 1100) continue;
        h += `<div style="position:absolute;left:${x.toFixed(0)}px;top:${y.toFixed(0)}px;width:${10 + H(i, 5) * 10}px;height:${16 + H(i, 6) * 12}px;background:${C[i % C.length]};border-radius:3px;transform:rotate(${r.toFixed(0)}deg) scaleX(${Math.cos(p * 6 + i).toFixed(2)});opacity:.95"></div>`;
      }
      if (kind === 'fireworks') for (let b = 0; b < 4; b++) {
        const t0 = .2 + b * .45, p = lt - t0; if (p < 0 || p > 1.4) continue;
        const cx = 300 + H(b, 9) * 1320, cy = 160 + H(b, 8) * 260, R = e3(p / .8) * 170, o = cl(1.4 - p, 0, 1);
        for (let k = 0; k < 18; k++) { const a = k / 18 * 6.283; h += `<div style="position:absolute;left:${(cx + Math.cos(a) * R).toFixed(0)}px;top:${(cy + Math.sin(a) * R + p * p * 60).toFixed(0)}px;width:12px;height:12px;border-radius:50%;background:${[GOLD, KIA, '#fff'][b % 3]};box-shadow:0 0 16px ${[GOLD, KIA, '#fff'][b % 3]};opacity:${o.toFixed(2)}"></div>`; }
      }
    }
    if (kind === 'rain') {
      const cx = 1786, p = e3(lt / .5);   /* 비구름은 망냥이 머리 위에만 */
      h += `<div style="position:absolute;left:${cx - 170}px;top:${560 - (1 - p) * 120}px;width:340px;height:120px;opacity:${p.toFixed(2)};transform:scale(.8);transform-origin:170px 60px">${[[40, 50, 60], [120, 30, 80], [210, 45, 66], [280, 62, 48]].map(([x, y, r]) => `<div style="position:absolute;left:${x - r}px;top:${y - r / 2}px;width:${r * 2}px;height:${r * 1.4}px;border-radius:50%;background:#8C95A5"></div>`).join('')}</div>`;
      for (let i = 0; i < 26; i++) { const q = (lt * 1.4 + H(i, 1)) % 1; h += `<div style="position:absolute;left:${(cx - 110 + H(i, 2) * 220).toFixed(0)}px;top:${(640 + q * 200).toFixed(0)}px;width:5px;height:30px;border-radius:3px;background:#6EC6FF;opacity:${(p * (1 - q)).toFixed(2)};transform:rotate(12deg)"></div>`; }
    }
    if (kind === 'sparkle') for (let i = 0; i < 22; i++) {
      const o = .5 + .5 * Math.sin(lt * 4 + i * 1.7), s = 18 + H(i, 3) * 26;
      h += `<div style="position:absolute;left:${(H(i, 1) * 1880).toFixed(0)}px;top:${(140 + H(i, 2) * 700).toFixed(0)}px;font-size:${s.toFixed(0)}px;color:${i % 3 ? GOLD : '#fff'};opacity:${(o * c01(lt / .4)).toFixed(2)};text-shadow:0 0 12px ${GOLD}">✦</div>`;
    }
    return h;
  }

  /* ── ③ 망상 구름 전환 ───────────────────────────────────── */
  function dreamHTML(s, lt) {
    const D = 1.35; if (lt > D) return '';
    const grow = e3(lt / .45), out = cl((lt - .95) / .4, 0, 1), sc = .2 + .8 * bk(lt / .5) + out * .6, op = 1 - out;
    const puffs = [[0, 0, 300], [-260, 40, 200], [260, 40, 210], [-150, -120, 190], [150, -120, 200], [-360, -40, 140], [360, -40, 150], [0, 150, 220], [-200, 160, 170], [200, 160, 170]];
    const cloud = puffs.map(([x, y, r]) => `<div style="position:absolute;left:${960 + x - r}px;top:${500 + y - r * .8}px;width:${r * 2}px;height:${r * 1.6}px;border-radius:50%;background:#FFFFFF;box-shadow:0 10px 40px rgba(120,90,200,.18)"></div>`).join('');
    const trail = [[1740, 860, 26], [1640, 780, 40], [1500, 700, 58]].map(([x, y, r], i) => `<div style="position:absolute;left:${x - r}px;top:${y - r}px;width:${r * 2}px;height:${r * 2}px;border-radius:50%;background:#fff;opacity:${cl((lt - i * .08) / .2, 0, 1) * op}"></div>`).join('');
    const n = s.dreamNo, tt = s.dreamTitle || '';
    return `<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 46%, rgba(186,160,255,${(.35 * grow * op).toFixed(2)}), rgba(30,20,60,${(.45 * grow * op).toFixed(2)}) 70%)"></div>${trail}
      <div style="position:absolute;inset:0;transform:scale(${sc.toFixed(3)});transform-origin:960px 520px;opacity:${op.toFixed(2)}">${cloud}
        <div style="position:absolute;left:0;right:0;top:${360}px;text-align:center;font-weight:900;color:#7A5BD8;font-size:46px;letter-spacing:-1px">${esc(s.dreamTop || '✦ 생각만 해도 행복한 ✦')}</div>
        <div style="position:absolute;left:0;right:0;top:${420 + ((s.dreamLabel || '').length > 7 ? 18 : 0)}px;text-align:center;font-weight:900;color:${KIA};font-size:${(s.dreamLabel || '').length > 7 ? 140 : 170}px;letter-spacing:-6px;line-height:1">${esc(s.dreamLabel || ('망상 ' + n + '경기'))}</div>
        <div style="position:absolute;left:0;right:0;top:${590}px;text-align:center;font-weight:800;color:#12161F;font-size:52px;letter-spacing:-1.5px">${esc(tt)}</div></div>`;
  }


  /* ── ⑤ 어두운 톤(10/19 사용자 "영상은 썸네일과 비슷한 어두운 톤") — EP.theme === 'dark' ── */
  const DARK = () => EP.theme === 'dark';
  if (DARK()) {
    const st = document.createElement('style');
    st.textContent = `html,body,#stage{background:#14080A!important}body{color:#F4EDE4}#brand{color:#F4EDE4}#chap{background:#EA0029}
#meta .d,#railTitle{color:#E8D9CF!important}#prog{background:#3A2226}#asof{background:#24161A;color:#F4EDE4;border-color:#4A2E33}
.mega,.big,.card .v{color:#F4EDE4}.card{background:#22151A;border-color:#3D262B;box-shadow:0 18px 48px rgba(0,0,0,.45)}
.card .l,.gray{color:#BCA9A2}.photo{background:#2A1A1E;border-color:#4A2E33;box-shadow:0 18px 50px rgba(0,0,0,.5)}
.st>div{background:#22151A;border-color:#3D262B}.st>div i{color:#BCA9A2}
.chip{background:radial-gradient(circle,#FFF8EE 0%,#EFDFCC 100%);box-shadow:0 0 0 4px rgba(255,201,60,.30),0 10px 26px rgba(0,0,0,.45)}.chip img{padding:9%;box-sizing:border-box}
#sub span{background:rgba(10,4,6,.92);box-shadow:0 0 0 3px rgba(255,201,60,.35)}
.title.gold,.chaptitle .kk{color:#FF5A63}
#vtitle .l{color:#F4EDE4}#vtitle .l.a{color:#FF5A63}#vtitle .bs{color:#BCA9A2}html.vert #hdr{border-bottom-color:#3D262B}`;   /* 10/20 사용자 '가운데 빨간 글씨가 번진 것처럼' — 진한 빨강(#EA0029)은 어두운 배경에서 밝기 차가 작아 영상 압축 때 번진다 → 밝은 빨강 */
    document.head.appendChild(st);
    const RP = [[/background:\s*#12161F/gi, 'background:#3A1218'], [/solid #12161F/gi, 'solid #F4EDE4'], [/background:\s*#fff(fff)?\b/gi, 'background:#22151A'],
      [/#E3E7EE/gi, '#3D262B'], [/#E9EDF3/gi, '#2A1A1E'], [/#F4F6FA/gi, '#1A0D10'], [/#6A7382/gi, '#BCA9A2'], [/#C9D0DB/gi, '#6E5A5E'], [/#D5DBE5/gi, '#4A3338'],
      [/#2B3240/gi, '#4A2E33'], [/#C9D3E3/gi, '#4A2E33'], [/#2B3A55/gi, '#E8D9CF'], [/#12161F/gi, '#F4EDE4']];
    const dk = h => { RP.forEach(([a, b]) => { h = h.replace(a, b); }); return h; };
    const rgb = c => { const m = String(c).match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(',').map(parseFloat); return { r: v[0], g: v[1], b: v[2], a: v[3] == null ? 1 : v[3] }; };
    const lum = o => .299 * o.r + .587 * o.g + .114 * o.b;
    /* mixC 처럼 rgb() 로 만들어진 흰 칸·검은 글자까지: 그린 뒤 화면에 보이는 색으로 한 번 더 바꾼다. data-nodark 안쪽(주사위 등)과 로고 칩은 그대로 */
    function domDark(root) {
      const els = [...root.querySelectorAll('*')];
      els.forEach(el => { if (el.closest('[data-nodark],.chip,svg')) return; const cs = getComputedStyle(el), bg = rgb(cs.backgroundColor);
        if (bg && bg.a > .4 && lum(bg) > 222) el.style.backgroundColor = '#22151A';
        ['borderTopColor'].forEach(k => { const b = rgb(cs[k]); if (b && parseFloat(cs.borderTopWidth) > 0 && lum(b) > 200) el.style.borderColor = '#3D262B'; }); });
      els.forEach(el => { if (el.closest('[data-nodark],.chip,svg')) return; const cs = getComputedStyle(el), fg = rgb(cs.color); if (!fg || lum(fg) > 70) return;
        let p = el, under = null; while (p && p !== root.parentElement) { const b = rgb(getComputedStyle(p).backgroundColor); if (b && b.a > .4) { under = b; break; } p = p.parentElement; }
        if (!under || lum(under) < 120) el.style.color = '#F4EDE4'; });
    }
    const _B = B; B = h => { _B(dk(h)); domDark(document.getElementById('body')); };   /* 장면 HTML 을 한 번에 어두운 톤으로 */
    window.__darkify = dk;
  }
  function darkStage(t) {
    if (!DARK()) return '';
    const gx = 50 + 6 * Math.sin(t * .4), gy = 30 + 4 * Math.cos(t * .3);
    document.getElementById('stage').style.background = `radial-gradient(55% 62% at ${gx}% ${gy}%, rgba(168,32,44,.55), rgba(20,8,10,0) 72%), repeating-conic-gradient(from ${(-8 + Math.sin(t * .2) * 3).toFixed(2)}deg at 50% -25%, rgba(255,130,70,.07) 0deg 3deg, rgba(0,0,0,0) 3deg 11deg), radial-gradient(120% 90% at 50% 120%, #060203 0%, rgba(6,2,3,0) 60%), #14080A`;
    let h = '';
    for (let i = 0; i < 34; i++) { const q = (t * (.04 + H(i, 1) * .05) + H(i, 2)) % 1, x = H(i, 3) * 1920 + Math.sin(t * .8 + i) * 30, y = 1100 - q * 1200, r = 2 + H(i, 4) * 4;
      h += `<div style="position:absolute;left:${x.toFixed(0)}px;top:${y.toFixed(0)}px;width:${(r * 2).toFixed(1)}px;height:${(r * 2).toFixed(1)}px;border-radius:50%;background:#FFB45A;box-shadow:0 0 ${(r * 4).toFixed(0)}px #FF8A3D;opacity:${(.75 * Math.sin(q * 3.14)).toFixed(2)}"></div>`; }
    return h;
  }

  /* 오버레이(마스코트·효과·구름)를 장면 위에 매 프레임 그린다 */
  window.__mangFx = function (t, s, lt) {
    let ov = document.getElementById('mangOv');
    if (!ov) { ov = document.createElement('div'); ov.id = 'mangOv'; ov.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:5;overflow:hidden';
      const st = document.getElementById('stage'), sub = document.getElementById('sub');
      /* 10/20 컷 쇼츠(세로): #sub 가 body 로 옮겨져 있고 장면(#stage)은 장면마다 확대·이동된다 → 덧그림은 body 에 1080x1920 좌표로 */
      if (EP.vertical) { ov.style.cssText = 'position:absolute;left:0;top:0;width:1080px;height:1920px;pointer-events:none;z-index:5;overflow:hidden'; document.body.appendChild(ov); sub.style.zIndex = 6; sub.style.position = 'absolute'; }
      else { st.insertBefore(ov, sub); sub.style.zIndex = 6; sub.style.right = '300px'; sub.style.left = '300px'; } }
    let h = darkStage(t);
    /* 10/20 사용자 "아직 누가 이긴다고 말도 안 했는데 폭죽이… 캐릭터도 벌써 2승 1패!" — s.revealAt(호흡 번호): 결과를 말하는 그 호흡에서 폭죽·말풍선·표정이 같이 나온다 */
    const rv = (() => { if (s.revealAt == null) return null; const sg = (EP.segT || [])[s.startLine] || []; if (!sg.length) return null;
      const i = Math.floor(s.revealAt), f = s.revealAt - i, a0 = sg[i] ?? sg[sg.length - 1], a1 = sg[i + 1] ?? a0 + 1.2; return a0 + (a1 - a0) * f; })();
    const fl = rv == null ? lt : t - rv;
    if (fl >= 0) [].concat(s.fx || []).forEach(k => { h += fxHTML(k, fl); });
    let hd = s.dreamNo ? dreamHTML(s, lt) : '';
    if (EP.vertical) {   /* 세로: 가로 1920x1080 좌표 효과를 0.5625배로 줄여 위아래 3칸에 깔고, 구름은 장면 칸(650~1320) 위에 */
      const T_ = (y, x) => `<div style="position:absolute;left:0;top:${y}px;width:1920px;height:1080px;transform:scale(.5625);transform-origin:0 0">${x}</div>`;
      h = T_(0, h) + T_(607, h) + T_(1214, h) + (hd ? T_(681, hd) : ''); hd = '';
    }
    h += hd;
    /* 요소 애니메이션: 사진·로고가 살짝 둥실 */
    document.querySelectorAll('#body .photo, #body .chip').forEach((el, i) => { el.style.translate = `0 ${(Math.sin(t * 1.8 + i * 1.3) * 5).toFixed(1)}px`; });
    const bonk = s.bonk;
    if (bonk) {   /* 망상 스코어: 이긴 팀 캐릭터가 진 팀 캐릭터에게 뿅망치 */
      const ph = lt - .5, cyc = ph < 0 ? -1 : ph % 1.7, hit = cyc >= .55 && cyc < .9, after = ph > .55;
      const ent = e3(c01(lt / .45)), lx = 1420, wx = lx + 176, yy = 560 + (1 - ent) * 400;
      const ang = cyc < 0 ? -150 : cyc < .4 ? -150 - 60 * e3(cyc / .4) : cyc < .55 ? -210 + 150 * e3((cyc - .4) / .15) : cyc < 1.1 ? -60 - 90 * e3((cyc - .55) / .55) : -150;   /* 들고 있다(-150) → 뒤로 젖힘(-210) → 내려침(-60) */
      const sq = hit ? Math.sin(c01((cyc - .55) / .35) * 3.14) : 0;
      const loseMood = after ? 'faint' : 'sweat', winMood = cyc > .9 || cyc < 0 ? 'cheer' : 'idle';
      const pow = hit ? `<div style="position:absolute;left:${lx + 10}px;top:${yy - 70}px;width:220px;height:120px;display:flex;align-items:center;justify-content:center;transform:scale(${(.6 + .6 * Math.sin(c01((cyc - .55) / .35) * 3.14)).toFixed(2)}) rotate(-10deg)"><svg viewBox="0 0 220 120" width="220" height="120" style="position:absolute"><path d="M110 4 l18 30 l36 -18 l-6 36 l44 4 l-36 22 l30 30 l-42 -6 l-6 36 l-26 -28 l-26 30 l-6 -38 l-42 8 l28 -32 l-36 -20 l42 -6 l-8 -36 l36 18z" fill="#FFD43B" stroke="#E5484D" stroke-width="5"/></svg><span style="position:relative;font-size:52px;font-weight:900;color:#E5484D;letter-spacing:-2px">뿅!</span></div>` : '';
      h += `<div style="position:absolute;left:${lx}px;top:${yy}px;width:236px;height:268px;filter:drop-shadow(0 10px 16px rgba(0,0,0,.35))">${crit(TEAM_SP[bonk.lose] || 'tiger', loseMood, t, { squash: sq })}</div>
        <div style="position:absolute;left:${wx}px;top:${yy - 10}px;width:236px;height:268px;filter:drop-shadow(0 10px 16px rgba(0,0,0,.35))">${crit(TEAM_SP[bonk.win] || 'tiger', winMood, t, { hammer: ang, flip: true })}</div>${pow}`;
    }
    if (s.crew && !bonk) {   /* 상대 구단 캐릭터: 왼쪽 아래 */
      const ent = e3(c01((lt - .1) / .5)), cx = 36, cy = 800 + (1 - ent) * 300;
      const say2 = s.crewSay ? `<div style="position:absolute;left:${cx + 214}px;top:${cy - 40}px;${pop(seg(lt, .35, .35))}"><div style="background:#fff;border:4px solid #12161F;border-radius:26px;padding:12px 26px;font-size:40px;font-weight:900;letter-spacing:-1px;color:#12161F;white-space:nowrap">${esc(s.crewSay)}</div></div>` : '';
      h += `${say2}<div style="position:absolute;left:${cx}px;top:${cy}px;width:236px;height:268px;filter:drop-shadow(0 10px 16px rgba(0,0,0,.35))">${crit(TEAM_SP[s.crew] || 'lion', s.crewMood || 'idle', t + 1.3)}</div>`;
    }
    if (EP.mascot !== false && s.mood !== 'none' && !bonk) {
      const before = rv != null && t < rv, mood = before ? (s.preMood || 'think') : (s.mood || 'idle'), ent = c01((t - 0.2) / .6), VV = !!EP.vertical, x = VV ? 838 : 1668, y = VV ? 120 - (1 - e3(ent)) * 300 : 800 + (1 - e3(ent)) * 300;   /* 세로: 오른쪽 위(머리줄과 제목 사이) */
      const say = s.say && !before ? `<div style="position:absolute;left:${x - 330}px;top:${VV ? y + 150 : y - 40}px;width:330px;display:flex;justify-content:flex-end;${pop(rv == null ? seg(lt, .25, .35) : seg(t - rv, 0, .35))}"><div style="background:#fff;border:4px solid #12161F;border-radius:26px;padding:12px 26px;font-size:40px;font-weight:900;letter-spacing:-1px;color:#12161F;white-space:nowrap;box-shadow:0 8px 0 rgba(18,22,31,.15)">${esc(s.say)}</div></div>` : '';
      h += `${say}<div style="position:absolute;left:${x}px;top:${y}px;width:236px;height:268px;filter:drop-shadow(3px 0 0 #fff) drop-shadow(-3px 0 0 #fff) drop-shadow(0 3px 0 #fff) drop-shadow(0 -3px 0 #fff) drop-shadow(0 10px 16px rgba(0,0,0,.45))">${mang(mood, t)}</div>`;
    }
    ov.innerHTML = h;
  };

  /* ── ④ 새 장면 ───────────────────────────────────────── */
  /* mscore: 전광판. s.left·s.right(팀), s.score "5 : 2", s.tag, s.text, s.win('L'|'R') */
  /* 10/20 00:49 사용자 "이건 굳이 카드 안에 없어도 될거같아" — 경고 문구를 사진 카드 없이 배경 위 글로 */
  SCENE.warn = (lt, s) => {
    const a = e3(cl((lt - .05) / .4, 0, 1)), b = e3(cl((lt - .25) / .5, 0, 1)), c = e3(cl((lt - .5) / .5, 0, 1));
    B(`<div class="col" style="width:100%;align-items:center;text-align:center;gap:0">
      <div style="font-weight:900;color:#E5484D;font-size:54px;letter-spacing:24px;padding-left:24px;opacity:${a.toFixed(3)}">WARNING</div>
      <div style="margin-top:28px;width:${Math.round(560 * a)}px;height:4px;background:#C70125"></div>
      <div data-keep="1" style="margin-top:58px;font-weight:900;color:#F4EDE4;font-size:108px;line-height:1.28;letter-spacing:-3px;opacity:${b.toFixed(3)};transform:translateY(${((1 - b) * 24).toFixed(1)}px)">본 영상은 채널 주인장의<br>망상임을 알려드립니다</div>
      <div style="margin-top:44px;font-weight:800;color:#BDB2AC;font-size:48px;letter-spacing:-1px;opacity:${c.toFixed(3)}">※ 경기 결과는 모두 예측이에요</div>
      <div style="margin-top:46px;width:${Math.round(560 * c)}px;height:4px;background:#C70125"></div></div>`);
  };
  /* mups: 선발 맞대결 두 쌍(10/20 사용자 "누구 대 누구 말하는데 사진은 대니엘밖에 — 다 나오게").
     s.pairs = [{tag, at, l:{img,name,team,focus}, r:{img,name,team,focus}, notes:[{t, at}]}] — 말하는 호흡(at)에 그 쌍이 뜬다 */
  SCENE.mups = (lt, s) => {
    const P = k => { const b = brP(s, k, .45); return b == null ? 1 : b; };
    const TCc = t => t === 'KIA' ? KIA : t === 'KT' ? '#3A3A44' : t === '삼성' ? '#074CA1' : '#6A7382';
    const card = (x, q) => { const src = photoSrc(x.img);
      return `<div style="display:flex;flex-direction:column;align-items:center;gap:14px">
        <div style="position:relative;width:250px;height:320px;border-radius:26px;overflow:hidden;background:#2A1A1E;border:5px solid ${TCc(x.team)};box-shadow:0 18px 44px rgba(0,0,0,.5)">${src ? `<img src="${src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${x.focus || '50% 15%'}">` : ''}</div>
        <div style="font-size:52px;font-weight:900;letter-spacing:-2px;color:#F4EDE4;white-space:nowrap">${esc(x.name)}</div></div>`; };
    const cols = (s.pairs || []).map(pr => { const q = P(pr.at ?? 0);
      const notes = (pr.notes || []).map(n => `<div style="font-size:40px;font-weight:900;color:${n.hi ? '#FF5A63' : '#F4EDE4'};letter-spacing:-1px;white-space:nowrap;${pop(P(n.at))}">${esc(n.t)}</div>`).join('');
      return `<div style="display:flex;flex-direction:column;align-items:center;gap:22px;opacity:${c01(q * 1.6).toFixed(3)};transform:translateY(${((1 - e3(q)) * 40).toFixed(1)}px)">
        <span style="display:inline-block;background:#3D262B;color:#F4EDE4;font-size:40px;font-weight:900;padding:8px 30px;border-radius:999px;white-space:nowrap">${esc(pr.tag)}</span>
        <div style="display:flex;align-items:center;gap:26px">${card(pr.l, q)}<div style="font-size:56px;font-weight:900;color:#BCA9A2;margin-bottom:60px">VS</div>${card(pr.r, q)}</div>
        <div style="display:flex;flex-direction:column;align-items:center;gap:6px;min-height:110px">${notes}</div></div>`; }).join('');
    B(`<div style="display:flex;justify-content:center;align-items:flex-start;gap:150px;width:100%">${cols}</div>`);
  };
  SCENE.mscore = (lt, s) => {
    const [a, b] = String(s.score || '0 : 0').split(':').map(x => parseInt(x)), stop = .55 + .35;
    const roll = (v, d) => { const p = c01((lt - .3 - d) / .6); if (p >= 1) return v; return Math.floor((lt * 23 + d * 7) % 10); };
    const wL = a > b, glow = c01((lt - 1.1) / .3);
    const box = (team, v, win, d) => `<div style="display:flex;flex-direction:column;align-items:center;gap:22px">
        <div style="${pop(seg(lt, d * .3, .4))};transform-origin:50% 50%"><div style="zoom:.8">${sideChip(team, 'M')}</div></div>
        <div style="position:relative;width:240px;height:262px;border-radius:30px;background:#12161F;border:8px solid ${win && glow > 0 ? GOLD : '#2B3240'};box-shadow:${win ? `0 0 ${(60 * glow).toFixed(0)}px ${GOLD}` : 'none'};display:flex;align-items:center;justify-content:center;overflow:hidden">
          <div style="position:absolute;left:0;right:0;top:50%;height:4px;background:#000;opacity:.6"></div>
          <span class="num" style="font-size:200px;font-weight:900;color:${win ? GOLD : '#FFFFFF'};letter-spacing:-8px;line-height:1;font-variant-numeric:tabular-nums">${roll(v, d)}</span></div>
        ${win ? `<div class="badge" style="background:${KIA};font-size:40px;padding:8px 30px;margin-top:-44px;position:relative;z-index:2;${pop(seg(lt, 1.15, .35))}">WIN</div>` : '<div style="height:22px"></div>'}</div>`;
    const tag = s.tag ? `<div class="badge" style="background:#7A5BD8;font-size:34px;${rise(seg(lt, 0, .4), 16)}">✦ ${esc(s.tag)}</div>` : '';
    B(`<div class="col" style="width:100%;align-items:center;gap:18px">${tag}<div class="row" style="gap:70px;align-items:flex-start">${box(s.left, a, wL, 0)}<div style="font-size:110px;font-weight:900;color:#C9D0DB;margin-top:200px">:</div>${box(s.right, b, !wL, .15)}</div>
      ${s.text ? `<div class="big" data-keep="1" style="margin-top:0;font-size:${s.size || 96}px;color:${wL ? KIA : '#12161F'};${pop(seg(lt, 1.3, .45))}">${br(s.text)}</div>` : ''}</div>`);
  };
  /* dice: 주사위 6개 → 1개만 금색. s.big "약 17%", s.sub "6번 중 1번", s.title */
  SCENE.dice = (lt, s) => {
    const pip = { 1: [[50, 50]], 2: [[28, 28], [72, 72]], 3: [[25, 25], [50, 50], [75, 75]], 4: [[28, 28], [72, 28], [28, 72], [72, 72]], 5: [[25, 25], [75, 25], [50, 50], [25, 75], [75, 75]], 6: [[28, 22], [72, 22], [28, 50], [72, 50], [28, 78], [72, 78]] };
    const fin = [3, 5, 2, 6, 4, 1], hit = 5, settle = 1.2;
    const dice = fin.map((f, i) => {
      const d0 = i * .08, p = c01((lt - d0) / settle), rolling = p < 1, face = rolling ? 1 + Math.floor(H(i, Math.floor(lt * 14)) * 6) : f;
      const rot = rolling ? (1 - e3(p)) * 540 * (i % 2 ? 1 : -1) : 0, jy = rolling ? -Math.abs(Math.sin(p * 9)) * 60 * (1 - p) : 0;
      const on = !rolling && i === hit && lt > settle + .3, dim = !rolling && i !== hit && lt > settle + .3;
      return `<div data-nodark="1" style="position:relative;width:200px;height:200px;border-radius:40px;background:${on ? GOLD : '#FFFFFE'};border:6px solid ${on ? '#E0A400' : '#C8B8B0'};box-shadow:${on ? `0 0 70px ${GOLD}` : '0 16px 36px rgba(18,22,31,.14)'};transform:translateY(${jy.toFixed(0)}px) rotate(${rot.toFixed(0)}deg) scale(${on ? 1.12 + .03 * Math.sin(lt * 6) : 1});opacity:${dim ? .35 : 1}">
        ${pip[face].map(([x, y]) => `<div style="position:absolute;left:${x * 2 - 17}px;top:${y * 2 - 17}px;width:34px;height:34px;border-radius:50%;background:${on ? KIA : (face === 1 ? KIA : '#111111')}"></div>`).join('')}
        ${on ? `<div class="badge" style="position:absolute;left:50%;top:-74px;transform:translateX(-50%);background:${KIA};font-size:32px;white-space:nowrap">우승!</div>` : ''}</div>`;
    }).join('');
    B(`<div class="col" style="width:100%;align-items:center;gap:40px">${s.title ? `<div class="badge" style="background:#12161F;font-size:34px;${rise(seg(lt, 0, .4), 16)}">${esc(s.title)}</div>` : ''}
      <div class="row" style="gap:40px;margin-top:60px">${dice}</div>
      <div class="row" style="gap:36px;align-items:baseline;${pop(seg(lt, settle + .45, .5))}"><span class="big" style="font-size:150px;color:${KIA}">${esc(s.big || '약 17%')}</span><span class="big" style="font-size:80px">${esc(s.sub || '')}</span></div></div>`);
  };
  /* gauge: 배터리가 단계마다 줄어든다. s.steps:[{label, team, pass(%), at}] → 누적 = 곱 */
  SCENE.gauge = (lt, s) => {
    const st = s.steps || [], cum = []; let c = 100; st.forEach(x => { c = c * x.pass / 100; cum.push(c); });
    let k = -1; st.forEach((x, i) => { if (lt >= (x.at ?? i * .8) + .2) k = i; });
    const from = k <= 0 ? 100 : cum[k - 1], to = k < 0 ? 100 : cum[k], p = k < 0 ? 0 : e3((lt - ((st[k].at ?? k * .8) + .2)) / .7), v = from + (to - from) * p;
    const col = v > 60 ? '#22C55E' : v > 30 ? '#F59E0B' : KIA;
    const W = 1100, Hh = 230;
    const bat = `<div style="position:relative;width:${W}px;height:${Hh}px;border:12px solid #12161F;border-radius:44px;padding:14px;background:#fff">
        <div style="height:100%;width:${v.toFixed(1)}%;border-radius:26px;background:linear-gradient(180deg, ${col}, ${col}CC);transition:none"></div>
        <div style="position:absolute;right:-46px;top:${Hh / 2 - 50}px;width:34px;height:100px;border-radius:0 14px 14px 0;background:#12161F"></div>
        <div class="num" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:130px;font-weight:900;color:#12161F;letter-spacing:-4px">${Math.round(v)}%</div></div>`;
    const chips = st.map((x, i) => { const on = i <= k; return `<div style="display:flex;flex-direction:column;align-items:center;gap:10px;opacity:${on ? 1 : .35};${pop(seg(lt, (x.at ?? i * .8), .4))}">${sideChip(x.team, 'M')}<div style="font-size:40px;font-weight:900;color:#12161F">${esc(x.label)}</div><div style="font-size:48px;font-weight:900;color:${on ? KIA : '#6A7382'}">× ${x.pass}%</div></div>`; }).join('<div style="font-size:60px;color:#C9D0DB;font-weight:900;margin-top:40px">→</div>');
    B(`<div class="col" style="width:100%;align-items:center;gap:44px">${s.title ? `<div class="badge" style="background:#12161F;font-size:34px">${esc(s.title)}</div>` : ''}${bat}<div class="row" style="gap:34px;align-items:flex-start">${chips}</div></div>`);
  };
  Object.assign(MOTION, { mups: () => 1.2, warn: () => 1.1, mscore: () => 1.8, dice: () => 2.2, gauge: s => .9 + (s.steps || []).length * .8 });
})();
/* @@MANG1019END */
