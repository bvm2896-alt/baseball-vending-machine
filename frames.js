// 프레임 렌더 → 바로 mp4 인코딩.  node frames.js <총길이초> <출력mp4> [fps] [배율] [동시작업수]
//   화면은 1080x1920 으로 그리고 배율(기본 1.3333 → 1440x2560, 2K)로 확대해 찍는다.
//   여러 페이지가 구간을 나눠 동시에 찍고(기본 CPU 수-1, 최대 4) 각자 ffmpeg 로 조각 mp4 를 만든 뒤 이어 붙인다.
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs'); const os = require('os'); const { spawn } = require('child_process');

function ffArgs(fps, W, H, out) {
  return ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-vf', `scale=${W}:${H}:flags=lanczos`, '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-tune', 'animation',
    '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', String(fps), '-g', String(fps * 2), '-movflags', '+faststart', out];
}

async function worker(browser, idx, from, to, fps, scale, W, H, out, quality, onProgress) {
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
  await p.goto('file://' + path.join(__dirname, 'work', 'render.html')); await p.waitForTimeout(900);
  const ff = spawn('ffmpeg', ffArgs(fps, W, H, out), { stdio: ['pipe', 'inherit', 'inherit'] });
  let err = null; ff.on('error', e => { err = e; });
  const write = buf => new Promise(res => { if (!ff.stdin.write(buf)) ff.stdin.once('drain', res); else res(); });
  for (let i = from; i < to; i++) {
    await p.evaluate(t => window.render(t), i / fps);
    await write(await p.screenshot({ type: 'jpeg', quality }));
    if ((i - from) % 60 === 0) onProgress(60);
  }
  ff.stdin.end();
  await new Promise(res => ff.on('close', res));
  await p.close();
  if (err) throw err;
  return to - from;
}

(async () => {
  const DUR = parseFloat(process.argv[2] || '45'), OUT = process.argv[3] || path.join(__dirname, 'work', 'silent.mp4');
  const FPS = parseInt(process.argv[4] || '60', 10), SCALE = parseFloat(process.argv[5] || '1.3333');
  const NW = Math.max(1, Math.min(4, parseInt(process.argv[6] || String(os.cpus().length - 1), 10) || 1));
  const QUALITY = parseInt(process.env.FRAME_JPEG_Q || '95', 10);
  const W = Math.round(1080 * SCALE / 2) * 2, H = Math.round(1920 * SCALE / 2) * 2;
  const n = Math.ceil(FPS * DUR);
  const opts = {}; if (process.env.CHROME_PATH) opts.executablePath = process.env.CHROME_PATH;
  const browser = await chromium.launch(opts);
  const t0 = Date.now(); let done = 0;
  const onProgress = k => { done += k; if (done % (FPS * 10) < 60) process.stdout.write(`  ${Math.min(n, done)}/${n} 프레임 (${Math.round((Date.now() - t0) / 1000)}초)\n`); };
  const parts = [], jobs = [];
  const per = Math.ceil(n / NW);
  for (let w = 0; w < NW; w++) {
    const from = w * per, to = Math.min(n, (w + 1) * per);
    if (from >= to) break;
    const part = path.join(__dirname, 'work', `silent_part${w}.mp4`);
    parts.push(part); jobs.push(worker(browser, w, from, to, FPS, SCALE, W, H, part, QUALITY, onProgress));
  }
  await Promise.all(jobs);
  await browser.close();
  if (parts.length === 1) { fs.renameSync(parts[0], OUT); }
  else {
    const lst = path.join(__dirname, 'work', 'silent_parts.txt');
    fs.writeFileSync(lst, parts.map(x => `file '${path.basename(x)}'`).join('\n'));
    await new Promise((res, rej) => { const c = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', OUT], { stdio: 'inherit' }); c.on('close', code => code ? rej(new Error('concat 실패 ' + code)) : res()); });
    for (const x of parts) { try { fs.unlinkSync(x); } catch (e) {} }
    try { fs.unlinkSync(lst); } catch (e) {}
  }
  console.log(`frames ${n} → ${W}x${H} ${FPS}fps, ${NW}개 동시, ${Math.round((Date.now() - t0) / 1000)}초`);
})().catch(e => { console.error('프레임 렌더 오류:', e.message); process.exit(1); });
