import assert from 'node:assert/strict';
import { readdir, readFile, access } from 'node:fs/promises';
import { join } from 'node:path';

const root = new URL('../dist/', import.meta.url);
const origin = 'https://ai-search-lab.pages.dev';
const decode = value => value.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const attrs = tag => Object.fromEntries([...tag.matchAll(/([\w:-]+)="([^"]*)"/g)].map(([, key, value]) => [key, decode(value)]));
const pages = new Map();
async function inspect(dir = '') {
  for (const entry of await readdir(new URL(dir, root), { withFileTypes: true })) {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) { await inspect(`${path}/`); continue; }
    if (!path.endsWith('.html')) continue;
    const html = await readFile(new URL(path, root), 'utf8');
    const route = '/' + path.replace(/index\.html$/, '');
    const head = html.match(/<head\b[^>]*>([\s\S]*?)<\/head>/i)?.[1];
    assert.ok(head, `${route}: missing document head`);
    assert.equal((html.match(/<html\b/gi) || []).length, 1, `${route}: document nesting`);
    assert.match(html, /<html lang="en">/);
    const titles = [...head.matchAll(/<title>([\s\S]*?)<\/title>/g)];
    assert.equal(titles.length, 1, `${route}: title count`);
    assert.ok(titles[0][1].trim(), `${route}: empty title`);
    const meta = [...head.matchAll(/<meta\b[^>]*>/g)].map(([tag]) => attrs(tag));
    const descriptions = meta.filter(m => m.name === 'description');
    assert.equal(descriptions.length, 1, `${route}: description count`);
    assert.ok(descriptions[0].content.trim(), `${route}: empty description`);
    const links = [...head.matchAll(/<link\b[^>]*>/g)].map(([tag]) => attrs(tag));
    const canonicals = links.filter(l => l.rel === 'canonical');
    assert.equal(canonicals.length, 1, `${route}: canonical count`);
    const canonical = canonicals[0].href;
    assert.equal(canonical, new URL(route === '/' ? '/vehicles/' : route, origin).href, `${route}: canonical mismatch`);
    const url = new URL(canonical);
    assert.equal(url.search + url.hash, '', `${route}: tracking in canonical`);
    const noindex = meta.some(m => m.name === 'robots' && m.content.includes('noindex'));
    assert.equal(noindex, route === '/thank-you/', `${route}: indexability`);
    assert.equal(meta.find(m => m.property === 'og:url')?.content, canonical);
    const json = [...head.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
    assert.equal(json.length, noindex ? 0 : 1, `${route}: JSON-LD count`);
    if (!noindex) {
      const data = JSON.parse(json[0][1]);
      const page = data['@graph'].find(n => n['@type'] === 'WebPage');
      assert.equal(page.url, canonical);
      assert.equal(page.name, decode(titles[0][1]));
      assert.equal(page.description, descriptions[0].content);
      assert.equal(data['@context'], 'https://schema.org');
    }
    pages.set(new URL(route, origin).href, { canonical, noindex });
  }
}
await inspect();
const index = await readFile(new URL('sitemap-index.xml', root), 'utf8');
const listed = new Set();
for (const [, location] of index.matchAll(/<loc>(.*?)<\/loc>/g)) {
  const url = new URL(decode(location));
  assert.equal(url.origin, origin);
  const xml = await readFile(new URL(url.pathname.slice(1), root), 'utf8');
  for (const [, loc] of xml.matchAll(/<loc>(.*?)<\/loc>/g)) listed.add(decode(loc));
}
for (const url of listed) {
  const page = pages.get(url);
  assert.ok(page, `Sitemap route missing from build: ${url}`);
  assert.equal(page.noindex, false);
  assert.equal(page.canonical, url, `Noncanonical sitemap entry: ${url}`);
}
for (const [url, page] of pages) {
  assert.equal(listed.has(url), !page.noindex && page.canonical === url, `Sitemap coverage: ${url}`);
  await access(new URL(decodeURI(new URL(page.canonical).pathname).slice(1) + 'index.html', root));
}
const robots = await readFile(new URL('robots.txt', root), 'utf8');
assert.ok(robots.includes(`Sitemap: ${origin}/sitemap-index.xml`));
assert.ok(!robots.includes('Disallow: /'));
console.log(`PASS: ${pages.size} HTML documents; metadata, canonicals, JSON-LD, noindex, and ${listed.size} sitemap entries. Output checks only; no indexing or rich-result claim.`);
