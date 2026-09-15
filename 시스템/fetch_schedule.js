// 네이버 스포츠 KBO 일정: 오늘·내일 경기(팀·구장·시간·예고 선발투수)를 data/schedule_latest.json 으로 저장
// 사용법: node fetch_schedule.js [YYYY-MM-DD ...]   (날짜 없으면 오늘과 내일)
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const HERE = __dirname, DATA = path.join(HERE, 'data');
fs.mkdirSync(DATA, { recursive: true });
const TEAMS = ['삼성', 'KT', 'kt', 'LG', 'KIA', '두산', 'NC', '롯데', 'SSG', '한화', '키움'];
const iso = d => d.toISOString().slice(0, 10);
const kst = () => new Date(Date.now() + 9 * 3600 * 1000);   // 컨테이너/PC 시간대와 무관하게 한국 날짜
let dates = process.argv.slice(2).filter(a => /^\d{4}-\d{2}-\d{2}$/.test(a));
if (!dates.length) { const t = kst(); const n = new Date(t.getTime() + 86400000); dates = [iso(t), iso(n)]; }

(async () => {
  try { require('child_process').execSync('chcp 65001', { stdio: 'ignore' }); } catch (e) {}
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 2400 }, locale: 'ko-KR',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36' });
  const out = { fetchedAt: new Date().toISOString(), days: {} };
  for (const d of dates) {
    const url = `https://m.sports.naver.com/kbaseball/schedule/index?date=${d}`;
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(3000);
      const cards = await page.evaluate(() => {
        // 경기 카드: 팀 이름이 2개 이상 들어간 가장 작은 블록들을 모은다
        const names = ['삼성', 'KT', 'kt', 'LG', 'KIA', '두산', 'NC', '롯데', 'SSG', '한화', '키움'];
        const all = [...document.querySelectorAll('li, div, section, article')];
        const picked = [];
        for (const el of all) {
          const t = (el.innerText || '').replace(/\s+/g, ' ').trim();
          if (t.length < 10 || t.length > 400) continue;
          const hit = names.filter(n => t.includes(n)).length;
          if (hit < 2) continue;
          // 자식 중에 같은 조건을 만족하는 게 있으면 부모는 건너뜀(가장 작은 블록만)
          const child = [...el.querySelectorAll('li, div, section, article')].some(c => { const ct = (c.innerText || '').replace(/\s+/g, ' ').trim(); return ct.length >= 10 && ct.length <= 400 && names.filter(n => ct.includes(n)).length >= 2; });
          if (child) continue;
          picked.push(t);
        }
        return [...new Set(picked)];
      });
      const games = cards.map(t => {
        const norm = t.replace(/\bkt\b/g, 'KT');
        // 카드 원문 순서대로 팀 2개: "예정 KT 로건 롯데 홈 김진욱 …" → 원정 KT(선발 로건), 홈 롯데(선발 김진욱)
        const found = TEAMS.filter(n => n !== 'kt').map(n => ({ n, i: norm.indexOf(n) })).filter(x => x.i >= 0).sort((a, b) => a.i - b.i);
        const teams = [...new Set(found.map(x => x.n))].slice(0, 2);
        const time = (norm.match(/\b(\d{1,2}:\d{2})\b/) || [])[1] || '';
        let stadium = (norm.match(/(잠실|고척|수원|인천|문학|대전|대구|사직|부산|창원|광주|울산|포항|청주)/) || [])[1] || '';
        // 팀 이름 바로 뒤에 오는 사람 이름(팀명·'홈'·'경기' 등이 아닌 한글/영문 2~6자)을 예고 선발로 본다
        const STOP = new Set(['홈', '경기', '예정', '종료', '취소', '우천', '엔드', '바로가기', '중계', '문자', '하이라이트', '선발', '경기전', '경기중', '연기']);
        const toks = norm.split(' ');
        const starterAfter = team => {
          let k = toks.indexOf(team);
          if (k < 0) return '';
          if (toks[k + 1] === '홈') k++;                 // 홈 팀은 "삼성 홈 페덱" 처럼 '홈' 뒤에 선발이 온다
          const w = toks[k + 1] || '';
          return (/^[가-힣A-Za-z]{2,6}$/.test(w) && !STOP.has(w) && !TEAMS.includes(w)) ? w : '';
        };
        const homeIdx = toks.indexOf('홈');
        let away = teams[0] || '', home = teams[1] || '';
        if (homeIdx > 0 && TEAMS.includes(toks[homeIdx - 1]) && teams.includes(toks[homeIdx - 1] === 'kt' ? 'KT' : toks[homeIdx - 1])) {
          home = toks[homeIdx - 1] === 'kt' ? 'KT' : toks[homeIdx - 1]; away = teams.find(x => x !== home) || away;
        }
        const awayStarter = starterAfter(away), homeStarter = starterAfter(home);
        const starters = [...t.matchAll(/선발\s*[:：]?\s*([가-힣A-Za-z]{2,10})/g)].map(m => m[1]);
        if (!starters.length && (awayStarter || homeStarter)) starters.push(awayStarter || '?', homeStarter || '?');
        const HOME_STADIUM = { 'LG': '잠실', '두산': '잠실', '키움': '고척', 'KT': '수원', 'SSG': '인천', '한화': '대전', '삼성': '대구', '롯데': '부산', 'NC': '창원', 'KIA': '광주' };
        if (!stadium && home) stadium = HOME_STADIUM[home] || '';
        const score = norm.match(/(\d{1,2})\s*[:：]\s*(\d{1,2})/);
        const status = /종료|경기종료/.test(t) ? '종료' : /취소|우천/.test(t) ? '취소' : /예정|선발/.test(t) ? '예정' : '';
        return { teams, away, home, awayStarter, homeStarter, time, stadium, starters, status, score: score ? [+score[1], +score[2]] : null, raw: t.slice(0, 300) };
      }).filter(g => g.teams.length === 2);
      out.days[d] = games;
      console.log(`${d}: ${games.length}경기`);
      games.forEach(g => console.log(`  ${g.away}(${g.awayStarter || '?'}) @ ${g.home}(${g.homeStarter || '?'}) ${g.stadium} ${g.time} ${g.status} ${g.score ? g.score.join(':') : ''}`));
    } catch (e) { console.log('실패:', d, e.message.split('\n')[0]); out.days[d] = []; }
  }
  await browser.close();
  fs.writeFileSync(path.join(DATA, 'schedule_latest.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log('OK → data/schedule_latest.json');
})();
