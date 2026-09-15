// 네이버 스포츠 KBO 팀 순위를 브라우저로 열어 HTML을 저장한 뒤 parse_rank.py 로 JSON을 만든다.
// 사용법:  node fetch_rank.js        → data/rank_YYYYMMDD.json, data/rank_latest.json, data/rank_latest.html
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const HERE = __dirname;
const DATA = path.join(HERE, 'data');
fs.mkdirSync(DATA, { recursive: true });

// 네이버가 주소를 바꿀 수 있어서 후보를 순서대로 시도한다.
const URLS = [
  'https://m.sports.naver.com/kbaseball/record/kbo?category=kbo&tab=teamRank',
  'https://m.sports.naver.com/kbaseball/record/kbo?category=kbo',
  'https://sports.naver.com/kbaseball/record/kbo?category=kbo&tab=teamRank',
  'https://sports.news.naver.com/kbaseball/record/index?category=kbo',
];

const ymd = () => { const d = new Date(); return d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0'); };

(async () => {
  // 윈도우 콘솔 한글 깨짐 방지
  try { require('child_process').execSync('chcp 65001', { stdio: 'ignore' }); } catch (e) {}
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1280, height: 2200 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36',
    locale: 'ko-KR',
  });
  let html = null, used = null;
  for (const url of URLS) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      // 순위표가 그려질 때까지: 승률 지표(wra)와 '위' 표기가 함께 나타나면 준비된 것
      await page.waitForFunction(() => {
        const h = document.body.innerHTML;
        return h.includes('class="blind">wra<') && h.includes('<span class="blind">위</span>');
      }, { timeout: 20000 });
      await page.waitForTimeout(800);
      html = await page.content();
      used = url;
      break;
    } catch (e) {
      console.log('실패:', url, '-', e.message.split('\n')[0]);
    }
  }
  await browser.close();
  if (!html) { console.error('순위표를 가져오지 못했습니다.'); process.exit(2); }

  const htmlPath = path.join(DATA, 'rank_latest.html');
  fs.writeFileSync(htmlPath, html, 'utf8');

  // 파이썬 파서 실행
  let out;
  try {
    out = execFileSync('python', ['-X', 'utf8', path.join(HERE, 'parse_rank.py'), htmlPath],
      { encoding: 'utf8', env: { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONUTF8: '1' } });
  } catch (e) {
    console.error('parse_rank.py 실패:', e.stderr || e.message); process.exit(3);
  }
  const json = JSON.parse(out);
  json.sourceUrl = used;
  json.fetchedAt = new Date().toISOString();
  if (!json.standings || json.standings.length !== 10) {
    console.error('팀 수가 10개가 아닙니다:', json.standings ? json.standings.length : 0); process.exit(4);
  }
  const text = JSON.stringify(json, null, 2);
  fs.writeFileSync(path.join(DATA, `rank_${ymd()}.json`), text, 'utf8');
  fs.writeFileSync(path.join(DATA, 'rank_latest.json'), text, 'utf8');

  console.log(`OK  ${used}`);
  for (const t of json.standings) {
    console.log(`${String(t.rank).padStart(2)}위 ${t.team.padEnd(3)} ${t.win}승 ${t.lose}패 ${t.draw}무  승률 ${t.winRate}  게임차 ${t.gameBehind}  ${t.streak}`);
  }
})();
