"""Local browser interface and synthetic demo. Run with Python 3.10+."""
import base64
import csv
import html
import io
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit
from checker import check, parse_csv, report_csv

TOKEN = secrets.token_urlsafe(32)
TEMPLATE = 'old_url,new_url,expected_title,expected_h1,expected_canonical\n'


def demo_csv(base):
    output = io.StringIO()
    output.write(TEMPLATE)
    writer = csv.writer(output)
    for old, new in [('good', 'good'), ('wrong', 'good'), ('missing', 'missing'), ('metadata', 'bad'), ('temporary', 'good'), ('chain', 'good'), ('blocked', 'blocked'), ('loop', 'good')]:
        writer.writerow([base + '/fixture/old-' + old, base + '/fixture/' + new, 'Welcome', 'Welcome', base + '/fixture/' + new])
    return output.getvalue()


def page(content):
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Migration Checker</title>
<style>body{font:16px system-ui;background:#f3f5f9;color:#172435;max-width:1100px;margin:3rem auto;padding:0 1rem}h1{font-size:2.5rem}section{background:white;padding:1.5rem;border-radius:12px;margin:1rem 0}textarea{width:100%;box-sizing:border-box;min-height:180px;font:14px monospace}button,.button{display:inline-block;background:#174f85;color:white;border:0;padding:.7rem 1rem;border-radius:5px;font:inherit;cursor:pointer}a{color:#174f85}td,th{text-align:left;padding:.7rem;border-bottom:1px solid #ccd4df;vertical-align:top;overflow-wrap:anywhere}table{border-collapse:collapse;width:100%}th:first-child,td:first-child{white-space:nowrap;overflow-wrap:normal;min-width:5rem}.scroll{overflow:auto}small{color:#46566b}.PASS{color:#196432}.FAIL{color:#a11919}.REVIEW{color:#795000}</style>
<h1>Migration Checker</h1><p>Check URL mappings, then focus your review on exceptions.</p>''' + content + '</html>'


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    @property
    def base(self):
        return f'http://127.0.0.1:{self.server.server_port}'

    def send(self, status, body, kind='text/html; charset=utf-8', headers=None):
        data = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

    def fixture(self, path):
        redirects = {'old-good': (301, 'good'), 'old-wrong': (301, 'bad'), 'old-missing': (301, 'missing'), 'old-metadata': (301, 'bad'), 'old-temporary': (302, 'good'), 'old-chain': (301, 'old-good'), 'old-blocked': (301, 'blocked'), 'old-loop': (301, 'old-loop')}
        name = path.rsplit('/', 1)[-1]
        if name in redirects:
            status, target = redirects[name]
            self.send(status, '', headers={'Location': '/fixture/' + target})
        elif name == 'blocked':
            self.send(403, 'Synthetic blocked response')
        elif name in ('good', 'bad'):
            title = 'Welcome' if name == 'good' else 'Wrong title'
            canonical = '/fixture/good' if name == 'good' else '/fixture/wrong-canonical'
            self.send(200, f'<html><head><title>{title}</title><link rel="canonical" href="{canonical}"></head><body><h1>{title}</h1><p>Synthetic test fixture; not a client migration.</p></body></html>')
        else:
            self.send(404, 'Synthetic missing page')

    def do_GET(self):
        # Loopback binding plus Host validation prevents DNS-rebinding access.
        if self.headers.get('Host') != urlsplit(self.base).netloc:
            self.send(403, 'Open the printed 127.0.0.1 address.'); return
        path = urlsplit(self.path).path
        if path.startswith('/fixture/'):
            self.fixture(path); return
        if path == '/template.csv':
            self.send(200, TEMPLATE, 'text/csv; charset=utf-8'); return
        if path != '/':
            self.send(404, 'Not found'); return
        text = demo_csv(self.base) if urlsplit(self.path).query == 'demo=1' else TEMPLATE
        self.send(200, page(f'''<section><h2>1. Add your URL mapping</h2>
<p><a href="/?demo=1">Load synthetic demo</a> · <a href="/template.csv" download>Download CSV template</a></p>
<p>Use up to 50 pairs. Optional expected title and H1 fields check exact text after whitespace normalization. Canonical defaults to the new URL. Keep trailing slashes and query strings intentional.</p>
<label>Load a UTF-8 CSV file <input type="file" id="file" accept=".csv,text/csv"></label>
<form method="post" action="/check"><input type="hidden" name="token" value="{TOKEN}"><p><label for="mapping">CSV mapping</label></p><textarea id="mapping" name="mapping" required>{html.escape(text)}</textarea>
<p><button id="run">Run checks</button> <span id="progress" role="status"></span></p></form></section>
<section><h2>What this checks</h2><p>HTTP redirects, final status, initial-HTML title, H1, and canonical. It does not execute JavaScript or assess visual layout, indexing, content parity, or a complete migration.</p><p>Runs locally and requests only supplied URLs and their redirects. Review the URLs before running. Results are displayed in this session; download your report to keep it.</p></section>
<script>document.querySelector('#file').onchange=async e=>{{const f=e.target.files[0];if(f)document.querySelector('#mapping').value=await f.text();}};document.querySelector('form').onsubmit=()=>{{document.querySelector('#run').disabled=true;document.querySelector('#progress').textContent='Checking URLs… larger batches may take several minutes.';}};</script>'''))

    def do_POST(self):
        if self.headers.get('Host') != urlsplit(self.base).netloc or self.path != '/check':
            self.send(403, 'Invalid request'); return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 200_000:
                raise ValueError('Input must be under 200 KB.')
            data = parse_qs(self.rfile.read(length).decode('utf-8'))
            if not secrets.compare_digest(data.get('token', [''])[0], TOKEN):
                self.send(403, 'Reload the app and try again.'); return
            rows = parse_csv(data.get('mapping', [''])[0])
        except (ValueError, UnicodeError) as exc:
            self.send(400, page('<section><h2>Check your input</h2><p>' + html.escape(str(exc)) + '</p><a href="/">Back</a></section>')); return
        results = [check(row) for row in rows]
        csv_data = base64.b64encode(('\ufeff' + report_csv(results)).encode()).decode()
        counts = ' · '.join(f'{sum(r["result"] == level for r in results)} {level}' for level in ('PASS', 'FAIL', 'REVIEW'))
        table = ''.join('<tr>' + ''.join('<td>' + html.escape(str(row[k])) + '</td>' for k in ('result', 'old_url', 'new_url', 'findings')) + '</tr>' for row in results)
        self.send(200, page(f'''<section><h2>Results</h2><p>{counts}</p><p>PASS means the configured checks passed. FAIL identifies a mismatch. REVIEW means a response or redirect needs investigation. A row can contain both failures and review items; read its findings.</p><a class="button" download="migration-report.csv" href="data:text/csv;base64,{csv_data}">Download report</a> <a href="/">Start another check</a><div class="scroll"><table><thead><tr><th>Result</th><th>Old URL</th><th>New URL</th><th>Findings</th></tr></thead><tbody>{table}</tbody></table></div></section>'''))


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    url = f'http://127.0.0.1:{server.server_port}/'
    print('Migration Checker: ' + url + '\nKeep this window open. Press Ctrl+C to stop.')
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
