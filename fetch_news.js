// 네이버 스포츠 KBO 뉴스 헤드라인(+상위 기사 본문 일부)을 모아 data/news_latest.json 으로 저장
// 사용법: node fetch_news.js        (콘티 쓸 때 "오늘 가장 핫한 이야기" 재료로 쓴다)
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const HERE = __dirname, DATA = path.join(HERE, 'data');
fs.mkdirSync(DATA, { recursive: true });
const URLS = [
  'https://m.sports.naver.com/kbaseball/news?sectionId=kbo&sort=popular',
  'https://m.sports.naver.com/kbaseball/news?sectionId=kbo',
  'https://m.sports.naver.com/kbaseball/news',
];
const TEAMS = ['삼성', 'KT', 'kt', 'LG', '기아', 'KIA', '두산', 'NC', '롯데', 'SSG', '한화', '키움'];
const ymd = () => { const d = new Date(); return d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0'); };

(async () => {
  try { require('child_process').execSync('chcp 65001', { stdio: 'ignore' }); } catch (e) {}
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 2400 }, locale: 'ko-KR',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36' });
  let items = [];
  for (const url of URLS) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(2500);
      for (let i = 0; i < 4; i++) { await page.mouse.wheel(0, 2000); await page.waitForTimeout(600); }
      const got = await page.evaluate(() => {
        const seen = new Set(), out = [];
        for (const a of document.querySelectorAll('a[href*="/article/"]')) {
          const href = a.href.split('?')[0];
          const t = (a.innerText || '').replace(/\s+/g, ' ').trim();
          if (!t || t.length < 12 || seen.has(href)) continue;
          seen.add(href); out.push({ title: t.slice(0, 120), url: href });
        }
        return out;
      });
      if (got.length >= 10) { items = got; console.log('목록:', url, got.length + '건'); break; }
      console.log('부족:', url, got.length);
    } catch (e) { console.log('실패:', url, e.message.split('\n')[0]); }
  }
  // 팀 이름이 들어간 기사 우선, 상위 10개 본문 앞부분 수집
  const score = it => TEAMS.filter(t => it.title.includes(t)).length + (/연패|연승|무득점|끝장|위기|충격|역전|탈락|확정|매직넘버|1위|5위/.test(it.title) ? 2 : 0);
  items.sort((a, b) => score(b) - score(a));
  const top = items.slice(0, 10);
  for (const it of top) {
    try {
      await page.goto(it.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(1500);
      const body = await page.evaluate(() => {
        const cand = document.querySelector('#comp_news_article, ._article_content, .article_body, #newsEndContents, article') || document.body;
        return (cand.innerText || '').replace(/\s+/g, ' ').trim();
      });
      it.body = body.slice(0, 1800);
    } catch (e) { it.body = ''; }
  }
  await browser.close();
  const out = { fetchedAt: new Date().toISOString(), count: items.length, top, headlines: items.slice(0, 60).map(i => i.title) };
  const text = JSON.stringify(out, null, 2);
  fs.writeFileSync(path.join(DATA, `news_${ymd()}.json`), text, 'utf8');
  fs.writeFileSync(path.join(DATA, 'news_latest.json'), text, 'utf8');
  console.log(`OK 헤드라인 ${items.length}건, 본문 ${top.filter(t => t.body).length}건`);
  top.slice(0, 10).forEach((t, i) => console.log(` ${i + 1}. ${t.title}`));
})();
