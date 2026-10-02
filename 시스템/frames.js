// 프레임 렌더 → 바로 mp4 인코딩.  node frames.js <총길이초> <출력mp4> [fps] [배율] [동시작업수]
//   화면은 1080x1920 으로 그리고 배율(기본 1.3333 → 1440x2560, 2K)로 확대해 찍는다.
//   여러 페이지가 구간을 나눠 동시에 찍고(기본 CPU 수-1, 최대 4) 각자 ffmpeg 로 조각 mp4 를 만든 뒤 이어 붙인다.
const path = require('path'); const fs = require('fs'); const os = require('os'); const { spawn } = require('child_process');
const { chromium } = require('playwright');
const CW = parseInt(process.env.FRAME_W || '1080', 10), CH = parseInt(process.env.FRAME_H || '1920', 10);   // 롱폼은 1920x1080 (build.py 가 환경변수로 준다, 9/18)
const WORK = process.env.KBO_WORK ? path.resolve(__dirname, process.env.KBO_WORK) : path.join(__dirname, 'work');   // 시리즈 창마다 다른 작업 폴더(동시 제작용)

/* 10/2: 회사 PC 2K 렌더에서 크롬 GPU 가 6번 죽어 크롬이 꺼짐("GPU process isn't usable") → FRAME_NO_GPU=1 이면 GPU 없이(소프트웨어로) 그린다.
   build.py 가 GPU 오류로 한 번 실패하면 이 값을 켜고 남은 장면만 다시 그린다. */
function launchOpts() {
  const o = {}; if (process.env.CHROME_PATH) o.executablePath = process.env.CHROME_PATH;
  if (process.env.FRAME_NO_GPU === '1') { o.args = ['--disable-gpu', '--disable-gpu-compositing']; console.log('  (그래픽 GPU 끄고 그림)'); }
  return o;
}

function ffArgs(fps, W, H, out) {
  return ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-',
    '-vf', `scale=${W}:${H}:flags=lanczos`, '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-tune', 'animation',
    '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', String(fps), '-g', String(fps * 2), '-movflags', '+faststart', out];
}

async function worker(browser, idx, from, to, fps, scale, W, H, out, quality, onProgress) {
  const p = await browser.newPage({ viewport: { width: CW, height: CH }, deviceScaleFactor: scale });
  await p.goto('file://' + path.join(WORK, 'render.html')); await p.waitForTimeout(900);
  const ff = spawn('ffmpeg', ffArgs(fps, W, H, out), { stdio: ['pipe', 'ignore', 'pipe'] });
  let err = null, errText = ''; ff.on('error', e => { err = e; }); ff.stdin.on('error', e => { err = err || e; });
  ff.stderr.on('data', d => { errText += d.toString(); if (errText.length > 4000) errText = errText.slice(-4000); });
  const closed = new Promise(res => ff.on('close', res));
  const write = buf => new Promise(res => { if (!ff.stdin.write(buf)) ff.stdin.once('drain', res); else res(); });
  let shot = 0;
  for (let i = from; i < to && !err; i++) {
    await p.evaluate(t => window.render(t), i / fps);
    await write(await p.screenshot({ type: 'jpeg', quality })); shot++;
    if ((i - from) % 60 === 0) onProgress(60);
  }
  ff.stdin.end();
  const code = await closed;
  await p.close();
  if (err) throw new Error(`ffmpeg 실행 오류(조각 ${idx}): ${err.message}\n${errText}`);
  if (code !== 0) throw new Error(`ffmpeg 종료 코드 ${code}(조각 ${idx}, ${shot}프레임)\n${errText}`);
  const size = fs.existsSync(out) ? fs.statSync(out).size : 0;
  if (shot === 0 || size < 1000 + 50 * shot) throw new Error(`조각 ${idx} 영상이 비었어요 (${shot}프레임, ${size}바이트, 범위 ${from}~${to})\n${errText}`);
  return to - from;
}

/* 10/1 조각 렌더(롱폼 — 사용자 "수정할 때마다 처음부터 다시 만들어야 돼? 너무 오래 걸려"):
   node frames.js --chunks <jobs.json>
   jobs.json = {fps, scale, quality, W, H, jobs:[{t0, t1, n, out, warm:[초...]}], accentOut}
   장면 하나 = 조각 하나. 조각의 j번째 프레임은 t0 + j/fps (장면 시작 기준)로 찍는다 → 앞 줄 길이가 바뀌어 장면이 통째로 밀려도 그림이 같다.
   찍기 전에 warm 시각들(앞 장면들의 마지막 프레임)을 한 번씩 그려 둔다(앞 장면 DOM·폭을 이어받는 장면이 전체 렌더와 똑같이 나오게).
   진행 막대는 window.__NOPROG 로 끄고 build.py 가 ffmpeg 로 따로 그린다. */
function ffNullArgs(fps) { return ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-', '-f', 'null', '-']; }
async function chunkMode(jobsFile) {
  const J = JSON.parse(fs.readFileSync(jobsFile, 'utf-8'));
  const fps = J.fps, scale = J.scale, W = J.W, H = J.H, quality = J.quality || 95, TEST = !!process.env.FRAMES_NULL;   // FRAMES_NULL: 인코딩 없이(클라우드 시험용)
  const NW = Math.max(1, Math.min(4, parseInt(process.env.FRAME_WORKERS || String(os.cpus().length - 1), 10) || 1));
  const opts = launchOpts();
  const t0all = Date.now(); const total = J.jobs.reduce((a, j) => a + j.n, 0); let done = 0, lastLog = 0;
  const queue = J.jobs.slice(); let accent = null;
  /* 10/2 밤: 그래픽카드 없는 회사 PC 는 크롬 하나로 2K 를 1만 장 넘게 찍으면 캡처가 터졌다(Unable to capture screenshot).
     → 장면(조각) 하나마다 크롬을 새로 띄우고 끝나면 닫는다. 터지면 그 장면만 최대 3번 다시(처음부터 다시 그리지 않음). */
  async function oneJob(job) {
    const b = await chromium.launch(opts);
    try {
      const p = await b.newPage({ viewport: { width: CW, height: CH }, deviceScaleFactor: scale });
      await p.goto('file://' + path.join(WORK, 'render.html')); await p.waitForTimeout(900);
      await p.evaluate(() => { window.__NOPROG = true; });
      if (accent == null) accent = await p.evaluate(() => getComputedStyle(document.getElementById('progBar')).backgroundColor);
      for (const w of (job.warm || [])) await p.evaluate(t => window.render(t), w);
      const ff = spawn('ffmpeg', TEST ? ffNullArgs(fps) : ffArgs(fps, W, H, job.out), { stdio: ['pipe', 'ignore', 'pipe'] });
      let err = null, errText = ''; ff.on('error', e => { err = e; }); ff.stdin.on('error', e => { err = err || e; });
      ff.stderr.on('data', d => { errText += d.toString(); if (errText.length > 4000) errText = errText.slice(-4000); });
      const closed = new Promise(res => ff.on('close', res));
      const write = buf => new Promise(res => { if (!ff.stdin.write(buf)) ff.stdin.once('drain', res); else res(); });
      let shot = 0;
      try {
        for (let j = 0; j < job.n && !err; j++) {
          const t = Math.min(job.t0 + j / fps, job.t1 - 1e-4);
          await p.evaluate(tt => window.render(tt), t);
          await write(await p.screenshot({ type: 'jpeg', quality }));
          shot++;
        }
      } finally { ff.stdin.end(); }
      const code = await closed;
      if (err) throw new Error(`ffmpeg 실행 오류(조각 ${path.basename(job.out)}): ${err.message}\n${errText}`);
      if (code !== 0) throw new Error(`ffmpeg 종료 코드 ${code}(조각 ${path.basename(job.out)})\n${errText}`);
      if (!TEST) {
        const size = fs.existsSync(job.out) ? fs.statSync(job.out).size : 0;
        if (size < 1000) throw new Error(`조각 영상이 비었어요: ${job.out} (${size}바이트)\n${errText}`);
        if (job.final) fs.renameSync(job.out, job.final);   // 10/2: 다 그린 조각은 바로 제 이름으로 → 도중에 터져도 다음 실행이 이어서 그린다
      }
      return shot;
    } finally { try { await b.close(); } catch (e) {} }
  }
  async function runWorker(wi) {
    while (queue.length) {
      const job = queue.shift(); let last = null;
      for (let a = 1; a <= 3; a++) {
        try { const n = await oneJob(job); done += n; last = null; break; }
        catch (e) { last = e; try { if (fs.existsSync(job.out)) fs.unlinkSync(job.out); } catch (_) {}
          process.stdout.write(`  조각 ${path.basename(job.final || job.out)} ${a}번째 실패 → ${a < 3 ? '크롬 새로 띄워 다시' : '포기'}: ${String(e.message).split('\n')[0].slice(0, 120)}\n`); }
      }
      if (last) throw last;
      if (done - lastLog >= fps * 10) { lastLog = done; process.stdout.write(`  ${done}/${total} 프레임 (${Math.round((Date.now() - t0all) / 1000)}초)\n`); }
    }
  }
  const ws = []; for (let w = 0; w < Math.min(NW, Math.max(1, J.jobs.length)); w++) ws.push(runWorker(w));
  await Promise.all(ws);
  if (J.accentOut) fs.writeFileSync(J.accentOut, JSON.stringify({ accent }));
  console.log(`chunks ${J.jobs.length}개 · frames ${total} → ${W}x${H} ${fps}fps, ${Math.round((Date.now() - t0all) / 1000)}초`);
}

(async () => {
  if (process.argv[2] === '--chunks') return chunkMode(process.argv[3]);
  const DUR = parseFloat(process.argv[2] || '45'), OUT = process.argv[3] || path.join(WORK, 'silent.mp4');
  const FPS = parseInt(process.argv[4] || '60', 10), SCALE = parseFloat(process.argv[5] || '1.3333');
  const NW = Math.max(1, Math.min(4, parseInt(process.argv[6] || process.env.FRAME_WORKERS || String(os.cpus().length - 1), 10) || 1));
  const QUALITY = parseInt(process.env.FRAME_JPEG_Q || '95', 10);
  const W = Math.round(CW * SCALE / 2) * 2, H = Math.round(CH * SCALE / 2) * 2;
  const n = Math.ceil(FPS * DUR);
  if (!(n > 0)) throw new Error(`총 길이·fps 가 이상해요 (길이 ${process.argv[2]}, fps ${process.argv[4]})`);
  const opts = launchOpts();
  const browser = await chromium.launch(opts);
  const t0 = Date.now(); let done = 0;
  const onProgress = k => { done += k; if (done % (FPS * 10) < 60) process.stdout.write(`  ${Math.min(n, done)}/${n} 프레임 (${Math.round((Date.now() - t0) / 1000)}초)\n`); };
  const parts = [], jobs = [];
  const per = Math.ceil(n / NW);
  for (let w = 0; w < NW; w++) {
    const from = w * per, to = Math.min(n, (w + 1) * per);
    if (from >= to) break;
    const part = path.join(WORK, `silent_part${w}.mp4`);
    parts.push(part); jobs.push(worker(browser, w, from, to, FPS, SCALE, W, H, part, QUALITY, onProgress));
  }
  await Promise.all(jobs);
  await browser.close();
  if (parts.length === 1) { fs.renameSync(parts[0], OUT); }
  else {
    const lst = path.join(WORK, 'silent_parts.txt');
    fs.writeFileSync(lst, parts.map(x => `file '${path.basename(x)}'`).join('\n'));
    await new Promise((res, rej) => { let e = ''; const c = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', OUT], { stdio: ['ignore', 'ignore', 'pipe'] }); c.stderr.on('data', d => { e += d.toString(); }); c.on('close', code => code ? rej(new Error('concat 실패 ' + code + '\n' + e)) : res()); });
    for (const x of parts) { try { fs.unlinkSync(x); } catch (e) {} }
    try { fs.unlinkSync(lst); } catch (e) {}
  }
  const outSize = fs.existsSync(OUT) ? fs.statSync(OUT).size : 0;
  if (outSize < 1000 + 50 * n) throw new Error(`무음 영상이 비었어요 (${outSize}바이트) — ffmpeg 가 프레임을 못 받았어요`);
  console.log(`frames ${n} → ${W}x${H} ${FPS}fps, ${NW}개 동시, ${Math.round((Date.now() - t0) / 1000)}초, ${Math.round(outSize / 1048576)}MB`);
})().catch(e => { console.error('프레임 렌더 오류:', e.message); process.exit(1); });
