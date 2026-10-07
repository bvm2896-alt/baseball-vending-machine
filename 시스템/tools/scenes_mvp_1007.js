/* ───── 10/7 롱폼⑧ 「2026 MVP 레이스」 새 인포그래픽 장면: mvp10 ─────
   지난 10년(2016~2025) MVP 열 칸 한 줄: 연도 · 구단 로고 · 이름 → 줄마다 보여 주는 것만 바뀐다(s.show).
   show: 'role'(투수/타자 배지 + 개수) · 'hr'(그해 홈런왕이 MVP를 놓친 칸에 빨간 표시, 같은 해엔 초록. 공동 홈런왕처럼 이름이 5자 넘으면 글씨 23px) · 'rank'(팀 정규시즌 순위 배지)
         · 'first'(1위 팀 칸만 강조) · 'pick'(한 해만 크게 + 칩).  extra = 11번째 칸(2026 후보, 점선).
   같은 chain('mvp10') 이면 칸·로고·이름은 그대로 있고 배지·표시만 새로 뜬다(사라졌다 다시 생기지 않음). */
const MVP_ROLE = { P: { t: '투수', c: '#2F6FD6' }, H: { t: '타자', c: '#E8730C' } };
SCENE.mvp10 = (lt, s) => {
  const its = (s.items || []).slice(), ex = s.extra || null, all = ex ? its.concat([Object.assign({ extra: true }, ex)]) : its;
  const n = all.length, CW = Math.min(170, Math.floor((1760 - 10 * (n - 1)) / n)), LG = Math.min(118, CW - 34), K = s._chain;
  const show = s.show || '', pick = s.pick, pAt = k => pk(s, k, .5, seg(lt, .25, .5));
  let h = titleH(lt, s, 56, 28, K && s._prev && s._prev.title === s.title);
  h += `<div class="row" style="gap:10px;align-items:stretch;justify-content:center">` + all.map((it, i) => {
    const pIn = K ? 1 : seg(lt, .15 + i * .09, .45), t = T(it.team || ''), isPick = pick != null && String(it.y) === String(pick);
    const dim = (show === 'first' && it.rank !== 1 && !it.extra) || (pick != null && !isPick) ? .32 : 1;
    const role = MVP_ROLE[it.role] || null, pr = show === 'role' ? pAt(s.roleAt == null ? 0 : s.roleAt) : 0;
    const hrBad = show === 'hr' && it.hr && it.hr !== '=' , hrSame = show === 'hr' && it.hr === '=', ph = show === 'hr' ? pAt(s.hrAt == null ? 0 : s.hrAt) : 0;
    const prk = show === 'rank' || show === 'first' ? pAt(s.rankAt == null ? 0 : s.rankAt) : 0;
    const bd = it.extra ? `border:4px dashed ${it.bad ? RED : '#9AA3B2'};background:#F7F9FC;` : isPick ? 'border:5px solid var(--acc);background:#fff;' : (show === 'first' && it.rank === 1) ? `border:5px solid ${GOLD};background:#fff;` : '';
    const rankC = it.rank === 1 ? GOLD : it.rank <= 4 ? '#3B4A63' : RED;
    return `<div class="pane col" style="width:${CW}px;border-radius:24px;padding:20px 6px 18px;gap:10px;align-items:center;${bd}opacity:${(c01(pIn * 1.6) * dim).toFixed(3)};${K ? '' : rise(pIn, 26)}">
      <div class="num" style="font-size:40px;font-weight:900;color:#5B6576;letter-spacing:-1px">${esc(String(it.y))}</div>
      <div class="chip" style="width:${LG}px;height:${LG}px">${t && LOGO[t.code] ? `<img src="${LOGO[t.code]}">` : ''}</div>
      <div class="title" style="font-size:${it.name.length >= 4 ? 34 : 40}px;font-weight:900;letter-spacing:-1.5px;white-space:nowrap">${esc(it.name)}</div>
      <div style="height:76px;display:flex;align-items:center;justify-content:center">${
        role && show === 'role' ? `<div style="background:${role.c};color:#fff;border-radius:999px;padding:6px 18px;font-size:36px;font-weight:900;${pop(pr)}">${role.t}</div>`
        : (show === 'rank' || show === 'first') && it.rank ? `<div style="background:${rankC};color:#fff;border-radius:14px;padding:4px 16px;font-size:40px;font-weight:900;${pop(prk)}">${it.rank}위</div>`
        : hrSame ? `<div style="color:${GREEN};font-size:32px;font-weight:900;line-height:1.05;text-align:center;${pop(ph)}">홈런왕<br>= MVP</div>`
        : hrBad ? `<div style="color:${RED};font-size:${String(it.hr).length >= 5 ? 23 : 30}px;font-weight:900;line-height:1.05;text-align:center;white-space:nowrap;${pop(ph)}">홈런왕<br>${esc(it.hr)}</div>` : ''}</div></div>`;
  }).join('') + `</div>`;
  if (show === 'role' && s.count) h += `<div class="row" style="gap:40px;justify-content:center;margin-top:30px">${s.count.map(c => `<div class="big" style="font-size:72px;color:${(MVP_ROLE[c.r] || {}).c || ACC};${pop(pAt(c.at))}">${esc(c.t)}</div>`).join('')}</div>`;
  if (s.chips) h += `<div class="row" style="gap:24px;justify-content:center;margin-top:30px">${s.chips.map(c => `<div class="pane" style="border-radius:999px;padding:12px 34px;font-size:52px;font-weight:900;${c.hi ? 'border:4px solid var(--acc);color:var(--acc);' : ''}${pop(pAt(c.at))}">${esc(c.t)}</div>`).join('')}</div>`;
  if (s.text) h += `<div class="big gold" style="margin-top:30px;font-size:${s.size || 76}px;${pop(pAt(s.textAt == null ? 1 : s.textAt))}">${br(s.text)}</div>`;
  wrapC(h);
};
