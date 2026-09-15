// 구글 뉴스(검색)에서 최근 24시간 KBO 기사를 모아 data/news_latest.json 으로 저장 (+상위 기사 본문 일부)
// 사용법: node fetch_news.js        (콘티 쓸 때 "오늘 가장 핫한 이야기" 재료로 쓴다)
// 순위는 fetch_rank.js 가 네이버 스포츠에서 따로 가져온다. 구글이 아무것도 못 주면 네이버 스포츠 뉴스로 대신한다.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const HERE = __dirname, DATA = path.join(HERE, 'data');
fs.mkdirSync(DATA, { recursive: true });

// 구글 뉴스 검색어 (최근 1일). 여러 검색어 결과를 합치고 제목이 같은 건 하나로
const QUERIES = ['프로야구', 'KBO 리그', '프로야구 순위', '가을야구', '프로야구 연패 OR 연승', '프로야구 부상 OR 복귀'];
const gnews = q => `https://news.google.com/rss/search?q=${encodeURIComponent(q + ' when:1d')}&hl=ko&gl=KR&ceid=KR:ko`;
const NAVER = ['https://m.sports.naver.com/kbaseball/news?sectionId=kbo&sort=popular', 'https://m.sports.naver.com/kbaseball/news?sectionId=kbo'];
const TEAMS = ['삼성', 'KT', 'kt', 'LG', '기아', 'KIA', '두산', 'NC', '롯데', 'SSG', '한화', '키움'];
const ymd = () => { const d = new Date(); return d.getFullYear() + String(d.getMonth() + 1).padStart(2, '0') + String(d.getDate()).padStart(2, '0'); };
const unesc = s => (s || '').replace(/<!\[CDATA\[|\]\]>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'").replace(/\s+/g, ' ').trim();
const norm = t => t.replace(/\[[^\]]*\]|\([^)]*\)/g, '').replace(/[^가-힣a-zA-Z0-9]/g, '').slice(0, 40);

async function fromGoogle() {
  const seen = new Map();
  for (const q of QUERIES) {
    try {
      const r = await fetch(gnews(q), { headers: { 'User-Agent': 'Mozilla/5.0' } });
      const xml = await r.text();
      const items = xml.split('<item>').slice(1);
      for (const it of items) {
        const g = tag => { const m = it.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`)); return m ? unesc(m[1]) : ''; };
        let title = g('title'); const source = g('source'); const link = g('link'); const pub = g('pubDate');
        if (source && title.endsWith(' - ' + source)) title = title.slice(0, -(source.length + 3)).trim();
        if (!title || title.length < 10 || !link) continue;
        const k = norm(title);
        if (!seen.has(k)) seen.set(k, { title: title.slice(0, 120), url: link, source, pubDate: pub, hits: 1 });
        else seen.get(k).hits += 1;   // 여러 검색어에서 같이 나오면 그만큼 화제
      }
      console.log('구글:', q, items.length + '건');
    } catch (e) { console.log('구글 실패:', q, e.message.split('\n')[0]); }
  }
  return [...seen.values()];
}

async function fromNaver(page) {
  for (const url of NAVER) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(2500);
      for (let i = 0; i < 4; i++) { await page.mouse.wheel(0, 2000); await page.waitForTimeout(600); }
      const got = await page.evaluate(() => {
        const seen = new Set(), out = [];
        for (const a of document.querySelectorAll('a[href*="/article/"]')) {
          const href = a.href.split('?')[0]; const t = (a.innerText || '').replace(/\s+/g, ' ').trim();
          if (!t || t.length < 12 || seen.has(href)) continue;
          seen.add(href); out.push({ title: t.slice(0, 120), url: href, source: '네이버 스포츠', hits: 1 });
        }
        return out;
      });
      if (got.length >= 10) { console.log('네이버(대체):', got.length + '건'); return got; }
    } catch (e) { console.log('네이버 실패:', e.message.split('\n')[0]); }
  }
  return [];
}

(async () => {
  try { require('child_process').execSync('chcp 65001', { stdio: 'ignore' }); } catch (e) {}
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 2400 }, locale: 'ko-KR',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36' });
  let items = await fromGoogle();
  let from = '구글 뉴스';
  if (items.length < 10) { items = await fromNaver(page); from = '네이버 스포츠(대체)'; }
  // 팀 이름·자극적 키워드가 들어간 기사, 여러 검색어에 걸린 기사 우선. 상위 12개는 본문 앞부분도 가져온다
  const score = it => TEAMS.filter(t => it.title.includes(t)).length + (it.hits - 1) * 1.5
    + (/연패|연승|무득점|끝장|위기|충격|역전|탈락|확정|매직넘버|1위|3위|5위|골절|부상|복귀|퇴출|방출|트레이드|드래프트|은퇴|징계|사과/.test(it.title) ? 2 : 0)
    - (/\b(MLB|메이저리그|오타니|이정후|김하성)\b/.test(it.title) && !TEAMS.some(t => it.title.includes(t)) ? 3 : 0);
  items.sort((a, b) => score(b) - score(a));
  const top = items.slice(0, 12);
  for (const it of top) {
    try {
      await page.goto(it.url, { waitUntil: 'load', timeout: 40000 });   // 구글 뉴스 링크는 원문 언론사로 넘어간다
      await page.waitForTimeout(2500);
      it.url = page.url();
      const body = await page.evaluate(() => {
        const sel = '#comp_news_article, ._article_content, .article_body, #newsEndContents, #articleBody, #article-body, #articeBody, .article-body, .news_end, #news_body_area, .article_txt, #CmAdContent, article';
        const cand = document.querySelector(sel) || document.body;
        return (cand.innerText || '').replace(/\s+/g, ' ').trim();
      });
      it.body = body.slice(0, 1800);
    } catch (e) { it.body = ''; }
  }
  await browser.close();
  const out = { fetchedAt: new Date().toISOString(), from, count: items.length, top, headlines: items.slice(0, 80).map(i => i.title + (i.source ? ` (${i.source})` : '')) };
  const text = JSON.stringify(out, null, 2);
  fs.writeFileSync(path.join(DATA, `news_${ymd()}.json`), text, 'utf8');
  fs.writeFileSync(path.join(DATA, 'news_latest.json'), text, 'utf8');
  console.log(`OK [${from}] 헤드라인 ${items.length}건, 본문 ${top.filter(t => t.body).length}건`);
  top.slice(0, 12).forEach((t, i) => console.log(` ${i + 1}. ${t.title}${t.source ? ' (' + t.source + ')' : ''}`));
})();
