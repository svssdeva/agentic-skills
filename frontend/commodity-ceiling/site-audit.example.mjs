// Read-only audit of a live site: consistency walk + failure states, via CDP in headless Chromium.
// Usage: node audit.mjs https://site.tld [maxRoutes]
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';

const CHROME = process.env.BROWSER_EXE || 'C:/Users/Admin/AppData/Local/imput/Helium/Application/chrome.exe';
const PORT = 9344;
const BASE = process.argv[2]; const MAX = parseInt(process.argv[3] || '8', 10);
const HERE = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const OUT = path.join(HERE, 'shots'); mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const chrome = spawn(CHROME, ['--headless=new', '--no-sandbox', '--disable-gpu', `--remote-debugging-port=${PORT}`, '--window-size=400,860', 'about:blank'], { stdio: 'ignore' });
let ws, id = 0; const pending = new Map(); const consoleErrors = [];
async function connect() { for (let i = 0; i < 40; i++) { try { const tabs = await (await fetch(`http://127.0.0.1:${PORT}/json`)).json(); const t = tabs.find((x) => x.type === 'page'); if (t) return t.webSocketDebuggerUrl; } catch {} await sleep(250); } throw new Error('no chrome'); }
const send = (method, params = {}) => new Promise((res) => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true }); return r.result ? r.result.value : null; };
const nav = async (url) => { consoleErrors.length = 0; await send('Page.navigate', { url }); await sleep(2500); };
const shot = async (name) => { const d = (await send('Page.captureScreenshot', { format: 'jpeg', quality: 60 })).data; writeFileSync(path.join(OUT, name + '.jpg'), Buffer.from(d, 'base64')); };
const probe = async () => ev(`(()=>{const q=(s)=>document.querySelector(s);const txt=(e)=>e?e.innerText.replace(/\\s+/g,' ').trim().slice(0,160):'';return {title:document.title,h1:txt(q('h1')),nav:txt(q('nav, header')),footer:txt(q('footer')),links:[...document.querySelectorAll('a[href^="/"]')].map(a=>a.getAttribute('href')).filter(h=>!h.includes('#')&&!/\\.(png|jpg|svg|pdf|xml)$/.test(h)),hscroll:document.documentElement.scrollWidth>document.documentElement.clientWidth,scrollW:document.documentElement.scrollWidth,imgsNoAlt:[...document.images].filter(i=>!i.alt).length,imgs:document.images.length,buttonsNoName:[...document.querySelectorAll('button')].filter(b=>!(b.innerText.trim()||b.getAttribute('aria-label'))).length,fontFamilies:[...new Set([...document.querySelectorAll('h1,h2,p,a,button')].map(e=>getComputedStyle(e).fontFamily.split(',')[0]))].slice(0,5),focusVisible:!![...document.styleSheets].flatMap(s=>{try{return [...s.cssRules]}catch{return []}}).find(r=>/focus-visible/.test(r.selectorText||'')),lang:document.documentElement.lang,viewport:!!q('meta[name="viewport"]')}})()`);

const rows = [];
try {
  ws = new WebSocket(await connect()); await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d.result ?? d); pending.delete(d.id); } else if (d.method === 'Runtime.exceptionThrown') consoleErrors.push((d.params.exceptionDetails.exception || {}).description || d.params.exceptionDetails.text); else if (d.method === 'Log.entryAdded' && d.params.entry.level === 'error') consoleErrors.push(d.params.entry.text); };
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable'); await send('Log.enable');
  await nav(BASE); const home = await probe(); await shot('00-home');
  rows.push({ route: '/', ...home, errors: consoleErrors.length });
  const routes = [...new Set(home.links)].filter((r) => r !== '/').slice(0, MAX);
  let i = 1;
  for (const r of routes) { await nav(BASE + r); const p = await probe(); await shot(String(i).padStart(2, '0') + '-' + r.replace(/\W+/g, '_')); rows.push({ route: r, ...p, errors: consoleErrors.length }); i++; }
  // failure states
  await nav(BASE + '/this-page-does-not-exist-xyz'); const nf = await probe(); await shot('90-notfound'); rows.push({ route: '404 probe', ...nf, errors: consoleErrors.length });
  await nav(BASE); await send('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
  const target = routes[0] || '/'; await send('Page.navigate', { url: BASE + target }); await sleep(2500);
  const off = await probe(); await shot('91-offline-nav'); rows.push({ route: 'offline then navigate ' + target, ...off, errors: consoleErrors.length });
  await send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
} catch (e) { console.log('ERROR', e.message); } finally { try { ws && ws.close(); } catch {} chrome.kill(); }
writeFileSync(path.join(HERE, 'audit.json'), JSON.stringify(rows, null, 2));
for (const r of rows) console.log(`${r.route} | title="${r.title}" | h1="${r.h1}" | nav="${(r.nav || '').slice(0, 70)}" | hscroll=${r.hscroll}(${r.scrollW}) | imgsNoAlt=${r.imgsNoAlt}/${r.imgs} | btnNoName=${r.buttonsNoName} | fonts=${(r.fontFamilies || []).join('/')} | focusVisible=${r.focusVisible} | errors=${r.errors}`);
