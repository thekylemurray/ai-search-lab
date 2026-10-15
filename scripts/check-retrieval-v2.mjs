import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { study } from '../src/data/retrievalStudyV2.js';
const strip = html => html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '');
const bodies = [];
for (const variant of ['a', 'b', 'c']) {
  const html = await readFile(new URL(`../dist/render-tests/v2/${variant}/index.html`, import.meta.url), 'utf8');
  const head = html.match(/<head[^>]*>([\s\S]*?)<\/head>/i)[1];
  const body = strip(html).match(/<body[^>]*>([\s\S]*?)<\/body>/i)[1];
  assert.ok(head.includes(`<title>${study.title}</title>`));
  assert.ok(head.includes(`name="description" content="${study.description}"`));
  assert.deepEqual([...body.matchAll(/<h[12][^>]*>(.*?)<\/h[12]>/g)].map(m => m[1]), [study.title, 'Visitor information']);
  for (const fact of study.facts) {
    assert.equal(body.includes(fact.value), variant !== 'c', `${variant}: ${fact.label}`);
    assert.ok(!head.includes(fact.value), `${variant}: answer leaked into head`);
  }
  assert.equal(body.includes('Loading workshop details...'), variant === 'c');
  assert.ok(!/Build timestamp|Rendering method/.test(body));
  bodies.push(body);
}
assert.equal(bodies[0], bodies[1], 'Build-time controls must have identical bodies');
console.log(`PASS: ${study.revision}; matched titles/headings, six facts in a/b and absent from initial c HTML, no head leakage. Not an AI retrieval result.`);
