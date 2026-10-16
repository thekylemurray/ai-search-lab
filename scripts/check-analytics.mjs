import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const source = fs.readFileSync('public/scripts/portfolio-analytics.js', 'utf8');
function run({ consent = null, hostname = 'ai-search-lab.pages.dev', pathname = '/', search = '', blockedStorage = false } = {}) {
  const handlers = {}, appended = [], stored = {}, buttons = {};
  let reloads = 0;
  const button = key => buttons[key] ||= { hidden: true, addEventListener: (_, cb) => { handlers[key] = cb; } };
  const panel = { hidden: true, querySelector: button };
  const document = {
    referrer: 'https://example.com/private?email=secret',
    querySelector: () => panel,
    querySelectorAll: () => [button('settings')],
    addEventListener: (_, cb) => { handlers.click = cb; },
    createElement: () => ({}),
    head: { appendChild: script => appended.push(script) }
  };
  const location = { hostname, pathname, search, origin: 'https://' + hostname, href: 'https://' + hostname + pathname + search, reload: () => { reloads++; } };
  const window = {};
  const localStorage = { getItem: () => { if (blockedStorage) throw Error(); return consent; }, setItem: (key, value) => { if (blockedStorage) throw Error(); stored[key] = value; } };
  vm.runInNewContext(source, { window, document, location, localStorage, URL, URLSearchParams });
  return { window, handlers, appended, panel, stored, reloads: () => reloads, commands: () => Array.from(window.dataLayer || [], entry => Array.from(entry)), click: href => handlers.click({ target: { closest: () => ({ href }) } }) };
}
for (const consent of [null, 'denied']) {
  const app = run({ consent });
  assert.equal(app.appended.length, 0);
  assert.equal(app.commands().length, 0);
}
for (const options of [{ hostname: 'localhost' }, { hostname: 'preview.ai-search-lab.pages.dev' }, { pathname: '/render-tests/v2/a/' }]) {
  assert.equal(run({ ...options, consent: 'granted' }).appended.length, 0);
}
const app = run({ pathname: '/ev-lab/', search: '?analytics_debug=1&email=secret' });
app.handlers['[data-analytics-accept]']();
app.handlers['[data-analytics-accept]']();
assert.equal(app.appended.length, 1);
const config = app.commands().find(c => c[0] === 'config');
assert.equal(config[1], 'G-M2J2LQWKYX');
assert.equal(config[2].send_page_view, false);
assert.equal(config[2].debug_mode, true);
assert.equal(config[2].page_referrer, 'https://example.com/');
assert.equal(app.commands().filter(c => c[1] === 'page_view').length, 1);
assert.equal(app.commands().find(c => c[1] === 'page_view')[2].project_id, 'ev-landing-lab');
app.click('https://ai-search-lab.pages.dev/resume/Kyle_Murray_Resume.pdf');
app.click('mailto:private@example.com?body=secret');
app.click('https://www.linkedin.com/in/thekylemurray');
app.click('https://evil.example/resume/Kyle_Murray_Resume.pdf');
app.click('https://www.linkedin.com/in/someone-else');
assert.deepEqual(app.commands().filter(c => c[0] === 'event').map(c => c[1]), ['page_view', 'resume_click', 'contact_click', 'linkedin_click']);
assert.ok(!JSON.stringify(app.commands()).includes('secret'));
assert.ok(!JSON.stringify(app.commands()).includes('private@example'));
app.handlers['[data-analytics-decline]']();
const count = app.commands().length;
app.click('mailto:private@example.com');
assert.equal(app.commands().length, count);
assert.equal(app.reloads(), 1);
assert.equal(run({ consent: 'granted' }).commands().find(c => c[0] === 'config')[2].debug_mode, undefined);
run({ blockedStorage: true }).handlers['[data-analytics-accept]']();
assert.ok(fs.readFileSync('dist/index.html','utf8').includes('/scripts/portfolio-analytics.js'));
assert.ok(!fs.readFileSync('dist/render-tests/v2/a/index.html','utf8').includes('/scripts/portfolio-analytics.js'));
console.log('Analytics checks passed: consent, host exclusions, single page view, click classification, sanitization, debug scope, withdrawal and generated wiring. This automated check does not verify GA4 receipt; see the dated screenshot evidence.');
