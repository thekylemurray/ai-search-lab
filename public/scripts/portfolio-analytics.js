(() => {
  const id = 'G-M2J2LQWKYX';
  const host = 'ai-search-lab.pages.dev';
  const key = 'portfolio-analytics-consent';
  const panel = document.querySelector('[data-analytics-choice]');
  if (!panel || location.hostname !== host || location.pathname.startsWith('/render-tests/')) return;
  const read = () => { try { return localStorage.getItem(key); } catch { return null; } };
  const save = value => { try { localStorage.setItem(key, value); } catch {} };
  let started = false;
  function start() {
    if (started) return;
    started = true;
    window['ga-disable-' + id] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    const debug = new URLSearchParams(location.search).get('analytics_debug') === '1';
    const path = location.pathname;
    let referrer = '';
    try { referrer = new URL(document.referrer).origin + '/'; } catch {}
    window.gtag('js', new Date());
    window.gtag('config', id, {
      send_page_view: false,
      page_location: location.origin + path,
      page_referrer: referrer,
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      ...(debug ? { debug_mode: true } : {})
    });
    const send = (name, extra = {}) => window.gtag('event', name, {
      page_path: path,
      page_location: location.origin + path,
      ...extra
    });
    const projects = {
      '/case-studies/discoverability-foundation': 'discoverability-foundation',
      '/case-studies/collibra-product-innovations': 'collibra-product-innovations',
      '/ev-lab': 'ev-landing-lab',
      '/web-ops': 'web-operations',
      '/experiments/neutral-rendering-results': 'neutral-rendering-study'
    };
    const project = projects[path.replace(/\/+$/, '')];
    send('page_view', project ? { project_id: project } : {});
    document.addEventListener('click', event => {
      if (window['ga-disable-' + id]) return;
      const anchor = event.target.closest?.('a[href]');
      if (!anchor) return;
      let url;
      try { url = new URL(anchor.href, location.href); } catch { return; }
      if (url.origin === location.origin && url.pathname === '/resume/Kyle_Murray_Resume.pdf') {
        send('resume_click', { resource_id: 'public_resume' });
      } else if (url.protocol === 'mailto:') {
        send('contact_click', { contact_method: 'email' });
      } else if (url.hostname === 'www.linkedin.com' && url.pathname.replace(/\/+$/, '') === '/in/thekylemurray') {
        send('linkedin_click', { contact_method: 'linkedin' });
      }
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.appendChild(script);
  }
  const consent = read();
  panel.hidden = consent === 'granted' || consent === 'denied';
  if (consent === 'granted') start();
  document.querySelectorAll('[data-analytics-settings]').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => { panel.hidden = false; });
  });
  panel.querySelector('[data-analytics-accept]').addEventListener('click', () => {
    save('granted');
    panel.hidden = true;
    if (started && window['ga-disable-' + id]) location.reload();
    else start();
  });
  panel.querySelector('[data-analytics-decline]').addEventListener('click', () => {
    save('denied');
    panel.hidden = true;
    window['ga-disable-' + id] = true;
    // Reload after withdrawal to remove the already-loaded third-party runtime.
    if (started) location.reload();
  });
})();
