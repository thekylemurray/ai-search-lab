import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const expected = 'Make the primary content available in the initial HTML when access without JavaScript is a requirement.';
for (const variant of ['static', 'pre-rendered', 'client']) {
  const html = await readFile(new URL(`../dist/render-tests/${variant}/index.html`, import.meta.url), 'utf8');
  // Inspect document content, excluding script payloads and styles. This is not an AI retrieval test.
  const body = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, '').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '');
  const hasRecommendation = body.includes(expected);
  assert.equal(hasRecommendation, variant !== 'client', `${variant}: unexpected initial HTML content`);
  if (variant === 'client') assert.ok(body.includes('Loading client-rendered test content...'));
  console.log(`PASS: ${variant}: recommendation ${hasRecommendation ? 'present' : 'absent'} in initial HTML.`);
}
