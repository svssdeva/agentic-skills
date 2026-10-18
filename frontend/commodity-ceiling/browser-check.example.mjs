// Real-browser run of the quota card via Chrome DevTools Protocol (no Playwright on this machine).
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
import path from 'node:path';

const CHROME = process.env.BROWSER_EXE || 'C:/Users/Admin/AppData/Local/claude-seo/ms-playwright/chromium-1234/chrome-win64/chrome.exe';
const PORT = 9333;
const HERE = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const PAGE = 'file:///' + path.join(HERE, 'index.html').replace(/\\/g, '/');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const chrome = spawn(CHROME, ['--headless=new', '--no-sandbox', '--disable-gpu', `--remote-debugging-port=${PORT}`, '--window-size=400,900', 'about:blank'], { stdio: 'ignore' });
let ws, id = 0; const pending = new Map();
async function connect() {
  for (let i = 0; i < 40; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json`); const tabs = await r.json(); const t = tabs.find((x) => x.type === 'page'); if (t) return t.webSocketDebuggerUrl; } catch {}
    await sleep(250);
  }
  throw new Error('chrome did not start');
}
function send(method, params = {}) {
  return new Promise((res, rej) => { const i = ++id; pending.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params })); });
}
const evalJs = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails)); return r.result.value; };
const offline = (on) => send('Network.emulateNetworkConditions', { offline: on, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
const cardText = () => evalJs(`document.getElementById('card').innerText.replace(/\\s+/g,' ').trim()`);
const click = (id) => evalJs(`(()=>{const b=document.getElementById(${JSON.stringify(id)});if(!b)return 'MISSING '+${JSON.stringify(id)};b.click();return 'clicked'})()`);
const results = []; const ok = (name, pass, detail) => { results.push({ name, pass, detail }); console.log((pass ? 'PASS ' : 'FAIL ') + name + (detail ? ' :: ' + detail : '')); };

try {
  const url = await connect();
  ws = new WebSocket(url);
  await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id).res(d.result ?? d); pending.delete(d.id); } };
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
  await send('Page.navigate', { url: PAGE }); await sleep(600);

  ok('loads in next step', /2 of 2 sessions used/.test(await cardText()) && /Upgrade plan/.test(await cardText()), (await cardText()).slice(0, 90));
  ok('no horizontal scroll at 400px', await evalJs('document.documentElement.scrollWidth <= document.documentElement.clientWidth'), await evalJs('document.documentElement.scrollWidth+" vs "+document.documentElement.clientWidth'));
  const shot = (await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 })).data; writeFileSync(path.join(HERE, 'shot-next.jpg'), Buffer.from(shot, 'base64'));

  // all nine states show their copy
  const expect = { loading: null, empty: 'No plan yet', partial: 'Refresh date unavailable', success: 'Upgraded to 4 sessions', error: "Couldn't load your session count", offline: "You're offline", denied: 'Only the account owner', undo: 'Undo upgrade', next: "You've used both sessions" };
  for (const [k, s] of Object.entries(expect)) {
    await click('state-' + k); await sleep(80);
    const txt = await cardText(); const pressed = await evalJs(`document.querySelectorAll('[aria-pressed="true"]').length`);
    ok('state ' + k, (s ? txt.includes(s) : !/[A-Za-z]/.test(txt)) && pressed === 1, s ? '' : 'skeleton, no text');
  }
  const errShot = (await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 })).data;
  await click('state-error'); await sleep(80); writeFileSync(path.join(HERE, 'shot-error.jpg'), Buffer.from((await send('Page.captureScreenshot', { format: 'jpeg', quality: 70 })).data, 'base64'));

  // Scenario 1: Retry, offline within 600 ms, back online -> must not stick on skeleton
  await click('retry-btn'); await sleep(200); await offline(true); await sleep(300);
  const offTxt = await cardText(); await offline(false); await sleep(900);
  const after = await cardText();
  ok('retry+offline+online does not stick on skeleton', /2 of 2 sessions used/.test(after) && !(await evalJs(`!!document.querySelector('[aria-busy="true"]')`)), 'while offline: ' + offTxt.slice(0, 60) + ' | after: ' + after.slice(0, 60));

  // Scenario 2: undo countdown resumes from time left after 3 s offline
  await click('state-next'); await sleep(80); await click('upgrade-btn'); await sleep(2100);
  const before = await evalJs(`(document.getElementById('undo-btn')||{}).innerText||''`);
  await offline(true); await sleep(3000); await offline(false); await sleep(150);
  const resumed = await evalJs(`(document.getElementById('undo-btn')||{}).innerText||''`);
  const n = parseInt((resumed.match(/(\d+)/) || [])[1] || '0', 10);
  ok('undo resumes from time left (expect ~5 s)', n >= 4 && n <= 6, `before offline: ${before} | after: ${resumed}`);
  await sleep(6500); ok('undo expires to success', /Upgraded to 4 sessions/.test(await cardText()) && !(await evalJs(`!!document.getElementById('undo-btn')`)), (await cardText()).slice(0, 70));

  // Scenario 3: offline 12 s during countdown -> success on return
  await click('state-next'); await sleep(80); await click('upgrade-btn'); await sleep(500);
  await offline(true); await sleep(12000); await offline(false); await sleep(200);
  ok('offline 12 s during undo -> success, no undo button', /Upgraded to 4 sessions/.test(await cardText()) && !(await evalJs(`!!document.getElementById('undo-btn')`)), (await cardText()).slice(0, 70));

  // Scenario 4: ten rapid switches
  for (const k of ['undo', 'loading', 'error', 'denied', 'partial', 'offline', 'success', 'empty', 'next', 'undo']) { await click('state-' + k); }
  await sleep(100);
  ok('ten rapid switches leave one aria-pressed', (await evalJs(`document.querySelectorAll('[aria-pressed="true"]').length`)) === 1 && (await evalJs(`document.querySelector('[aria-pressed="true"]').id`)) === 'state-undo');

  // Keyboard: focus lands on undo-btn after upgrade; tab order reaches controls
  await click('state-next'); await sleep(80); await click('upgrade-btn'); await sleep(80);
  ok('focus moves to undo button after upgrade', (await evalJs('document.activeElement && document.activeElement.id')) === 'undo-btn');
  await click('undo-btn'); await sleep(80);
  ok('undo returns to next step', /You've used both sessions/.test(await cardText()));

  // Dark theme: tokens applied with emulated prefers-color-scheme: dark
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'dark' }] }); await sleep(100);
  const bgDark = await evalJs('getComputedStyle(document.body).backgroundColor');
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: 'light' }] }); await sleep(100);
  const bgLight = await evalJs('getComputedStyle(document.body).backgroundColor');
  ok('dark and light backgrounds differ', bgDark !== bgLight, `${bgDark} vs ${bgLight}`);
} catch (e) { console.log('ERROR', e.message); } finally {
  const passed = results.filter((r) => r.pass).length; console.log(`\n${passed}/${results.length} passed`);
  try { ws && ws.close(); } catch {} chrome.kill();
  writeFileSync(path.join(HERE, 'browser_test_results.json'), JSON.stringify(results, null, 2));
}
