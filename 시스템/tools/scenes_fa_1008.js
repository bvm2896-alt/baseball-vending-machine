/* ───── 10/8 롱폼⑨ 「외국인 선수 재계약」 새 인포그래픽 장면: tiers · capbar ─────
   tiers: 10개 구단을 세 갈래 칸으로 — groups:[{title, teams:[구단], at}], on(칸 번호, 강조), hi(구단, 강조 + 나머지 흐림),
          notes:{구단: '짧은 말'}(로고 밑 작은 글, notesAt 호흡), text. 같은 chain('tiers') 이면 칸·로고는 그대로, 강조·글만 바뀐다.
   capbar: 몸값 막대 — segs:[{label, v(만 달러), color, at}], cap(한도 선), capLabel, ext(늘어난 한도, extAt), max, title, text. */
SCENE.tiers = (lt, s) => {
  const gs = s.groups || [], K = !!(s._chain && s._prev && s._prev.type === 'tiers'), hiT = s.hi ? T(s.hi).code : null, on = s.on ?? -1;
  /* 10/8 밤: hiAt = 강조 팀이 그 호흡에 켜진다(팀 이름 줄을 뺀 뒤 소개 줄에서 바로 강조) */
  const hp = s.hi && s.hiAt != null ? eo(pk(s, s.hiAt, .5, 1)) : 1;
  const LG = s.logo || 150, CH = (CHAINS[s._cid] || []).map(j => SC[j]).filter(x => x && x.type === 'tiers');
  /* 10/8 밤: 묶음 안에 글·notes 가 한 번이라도 있으면 그 자리를 늘 비워 둔다(글이 사라져도 표가 안 움직이게) */
  const anyText = CH.some(x => x.text), anyNotes = CH.some(x => x.notes);
  let h = s.title ? titleH(lt, s, 56, 30, K && s._prev && s._prev.title === s.title) : CH.some(x => x.title) ? `<div class="title" style="font-size:56px;font-weight:900;margin-bottom:30px;visibility:hidden">·</div>` : '';   /* 10/8 밤: 묶음에 제목이 생겨도 표가 안 내려가게 */
  h += `<div class="row" style="gap:34px;align-items:stretch;justify-content:center">` + gs.map((g, k) => {
    const p = K && (s._prev.groups || [])[k] && !(s._prev.hideFrom != null && k >= s._prev.hideFrom) ? 1 : pk(s, g.at, .45, seg(lt, .15 + k * .3, .45));
    const hide = s.hideFrom != null && k >= s.hideFrom, isOn = on === k, gc = g.color || ACC;
    const cols = g.teams.length <= 2 ? 2 : 3;
    const cells = g.teams.map((tm, j) => {
      const t = T(tm), isHi = hiT && t.code === hiT, dim = hiT && !isHi ? 1 - .7 * hp : 1;
      const note = (s.notes || {})[tm], pn = note ? (K && (s._prev.notes || {})[tm] === note ? 1 : pk(s, s.notesAt == null ? g.at : s.notesAt, .4, seg(lt, .5 + k * .25, .4))) : 0;
      return `<div class="col" style="width:${LG + 120}px;gap:8px;align-items:center;opacity:${dim};transition:none">
        <div class="chip" style="width:${LG}px;height:${LG}px;${isHi ? `outline:7px solid ${ACC}${Math.round(hp * 255).toString(16).padStart(2, '0')};outline-offset:4px;border-radius:50%` : ''}">${LOGO[t.code] ? `<img src="${LOGO[t.code]}">` : ''}</div>
        <div class="title" style="font-size:44px;font-weight:900;letter-spacing:-1px;white-space:nowrap;margin-top:10px">${esc(tm)}</div>
        ${anyNotes || s.notes ? `<div class="label" style="height:50px;font-size:38px;font-weight:900;color:${ACC};white-space:nowrap;${pop(pn)}">${esc(note || '')}</div>` : ''}</div>`;
    }).join('');
    return `<div class="pane col" style="border-radius:32px;padding:${isOn ? '26px 18px 24px' : '28px 20px 26px'};gap:18px;align-items:center;${isOn ? `border:5px solid ${gc};background:#fff;` : ''}opacity:${hide ? 0 : (on >= 0 && !isOn ? .45 : 1) * c01(p * 1.5)};${K && p === 1 ? '' : rise(p, 30)}">
      <div class="badge" style="background:${isOn || on < 0 ? gc : '#8A93A3'};font-size:40px;padding:10px 30px;white-space:nowrap">${esc(g.title)}</div>
      <div style="display:grid;grid-template-columns:repeat(${cols},${LG + 120}px);gap:14px 6px;justify-content:center">${cells}</div></div>`;
  }).join('') + `</div>`;
  const TS = s.text ? (s.size || 66) : ((CH.find(x => x.text) || {}).size || 66);   /* 비워 둔 칸도 글이 있는 장면과 같은 크기 */
  if (s.text || anyText) h += `<div class="big gold" style="margin-top:26px;font-size:${TS}px;min-height:${Math.round(TS * 1.3)}px;${!s.text ? 'visibility:hidden' : K && s._prev.text === s.text ? '' : pop(pk(s, s.textAt, .5, seg(lt, .9, .5)))}">${br(s.text || '·')}</div>`;
  wrapC(h);
};

SCENE.capbar = (lt, s) => {
  const segs = s.segs || [], W = s.w || (EP.vertical ? 1080 : 1560),   /* 10/8 밤: 세로 컷은 막대를 좁혀 화면을 크게 */
    MX = s.max || 450, px = v => v / MX * W, K = !!(s._chain && s._prev && s._prev.type === 'capbar');
  /* 10/8 밤: 묶음 안에 한도 선·늘어난 한도·글이 한 번이라도 있으면 그 자리를 늘 비워 둔다(막대가 위아래로 안 움직이게) */
  const CH = (CHAINS[s._cid] || []).map(j => SC[j]).filter(x => x && x.type === 'capbar'), aCap = CH.some(x => x.cap) || s.cap, aExt = CH.some(x => x.ext) || s.ext, aTxt = CH.some(x => x.text) || s.text;
  let h = titleH(lt, s, 56, 34, K && s._prev.title === s.title);
  let x = 0, bars = '';
  segs.forEach((g, i) => {
    const was = K && (s._prev.segs || []).some(o => o.label === g.label && o.v === g.v);
    const p = was ? 1 : pk(s, g.at, .55, seg(lt, .2 + i * .35, .55)), w = px(g.v) * eo(p);
    bars += `<div style="position:absolute;left:${x}px;top:0;height:150px;width:${w.toFixed(1)}px;background:${g.color || ACC};border-right:4px solid #fff;overflow:hidden;display:flex;flex-direction:column;justify-content:center;padding-left:22px;box-sizing:border-box">
      <div style="font-size:${px(g.v) < 260 ? 34 : 42}px;font-weight:900;color:#fff;white-space:nowrap;letter-spacing:-1px;opacity:${c01((p - .6) * 3)}">${esc(g.label)}</div>
      <div class="num" style="font-size:${px(g.v) < 260 ? 36 : 46}px;font-weight:900;color:#fff;white-space:nowrap;opacity:${c01((p - .6) * 3)}">${esc(g.vt || (g.v + '만 달러'))}</div></div>`;
    x += px(g.v);
  });
  const line = (v, lab, c, dash, p) => `<div style="position:absolute;left:${px(v) - 3}px;top:-70px;height:290px;border-left:6px ${dash ? 'dashed' : 'solid'} ${c};opacity:${c01(p * 1.5)}"></div>
    <div class="badge" style="position:absolute;left:${px(v)}px;top:${dash ? 236 : -128}px;translate:-50% 0;background:${c};font-size:36px;padding:8px 22px;white-space:nowrap;${pop(p)}">${esc(lab)}</div>`;
  const pc = s.cap ? (K && s._prev.cap === s.cap ? 1 : pk(s, s.capAt, .45, seg(lt, .1, .45))) : 0;
  const pe = s.ext ? (K && s._prev.ext === s.ext ? 1 : pk(s, s.extAt, .45, seg(lt, 1.2, .45))) : 0;
  h += `<div style="position:relative;width:${W}px;height:150px;margin:${aCap ? 150 : 20}px 0 ${aExt ? 170 : 30}px;background:#EEF1F6;border-radius:24px;overflow:visible">
    <div style="position:absolute;inset:0;border-radius:24px;overflow:hidden">${bars}</div>
    ${s.cap ? line(s.cap, s.capLabel || `한도 ${s.cap}만 달러`, '#12161F', false, pc) : ''}${s.ext ? line(s.ext, s.extLabel || `${s.ext}만 달러`, RED, true, pe) : ''}</div>`;
  const TS = s.text ? (s.size || 66) : ((CH.find(x => x.text) || {}).size || 66);
  if (aTxt) h += `<div class="big gold" style="margin-top:20px;font-size:${TS}px;min-height:${Math.round(TS * 1.3)}px;${!s.text ? 'visibility:hidden' : K && s._prev.text === s.text ? '' : pop(pk(s, s.textAt, .5, seg(lt, 1.2, .5)))}">${br(s.text || '·')}</div>`;
  wrapC(h);
};
