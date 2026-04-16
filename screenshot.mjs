import puppeteer from 'puppeteer';
import { existsSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';

const url   = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] || '';
const dir   = join(fileURLToPath(new URL('.', import.meta.url)), 'temporary screenshots');

if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

// Auto-increment — never overwrite
const n    = readdirSync(dir).filter(f => /^screenshot-\d/.test(f)).length + 1;
const name = label ? `screenshot-${n}-${label}.png` : `screenshot-${n}.png`;
const out  = join(dir, name);

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 900, deviceScaleFactor: 1 });
await page.goto(url, { waitUntil: 'networkidle0', timeout: 30_000 });
await page.screenshot({ path: out, fullPage: true });
await browser.close();

console.log(`  ✔  Saved → ${out}`);
