"""Small, dependency-free migration checker. Python 3.10+. Initial HTML only."""
import csv
import io
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit, urljoin
from urllib.request import Request, build_opener, HTTPRedirectHandler

MAX_ROWS = 50
MAX_BYTES = 2_000_000
REDIRECTS = {301, 302, 303, 307, 308}


def url_key(value):
    p = urlsplit(value.strip())
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password or p.fragment:
        raise ValueError('Use absolute HTTP(S) URLs without credentials or fragments.')
    port = p.port
    host = p.hostname.lower()
    host = '[' + host + ']' if ':' in host else host
    if port and (p.scheme, port) not in [('http', 80), ('https', 443)]:
        host += ':' + str(port)
    return urlunsplit((p.scheme, host, p.path or '/', p.query, ''))


def parse_csv(text):
    reader = csv.DictReader(io.StringIO(text.lstrip('\ufeff')))
    required = {'old_url', 'new_url'}
    allowed = required | {'expected_title', 'expected_h1', 'expected_canonical'}
    if not reader.fieldnames or not required <= set(reader.fieldnames):
        raise ValueError('CSV must include old_url and new_url columns.')
    if len(reader.fieldnames) != len(set(reader.fieldnames)) or set(reader.fieldnames) - allowed:
        raise ValueError('Duplicate or unknown CSV columns. Use the provided template.')
    rows = []
    for line, row in enumerate(reader, 2):
        if None in row or any(v is None for v in row.values()):
            raise ValueError(f'Line {line}: wrong number of columns.')
        row = {k: v.strip() for k, v in row.items()}
        try:
            for key in ('old_url', 'new_url'):
                row[key] = url_key(row[key])
            row['expected_canonical'] = url_key(row.get('expected_canonical') or row['new_url'])
        except ValueError as exc:
            raise ValueError(f'Line {line}: {exc}') from exc
        rows.append(row)
        if len(rows) > MAX_ROWS:
            raise ValueError(f'Use at most {MAX_ROWS} URL pairs per run.')
    if not rows:
        raise ValueError('Add at least one URL pair.')
    return rows


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url, timeout=8):
    """Follow at most five redirects; retain each observed status and destination."""
    opener = build_opener(NoRedirect())
    chain, visited = [], set()
    try:
        for _ in range(6):
            url = url_key(url)
            if url in visited:
                raise ValueError('Redirect loop')
            visited.add(url)
            req = Request(url, headers={'User-Agent': 'MigrationChecker/0.1', 'Accept': 'text/html'})
            try:
                response = opener.open(req, timeout=timeout)
            except HTTPError as exc:
                response = exc
            with response:
                status = response.code
                chain.append({'url': url, 'status': status})
                if status in REDIRECTS:
                    location = response.headers.get('Location')
                    if not location:
                        raise ValueError('Redirect missing Location header')
                    url = urljoin(url, location)
                    continue
                raw = response.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    raise ValueError('Response exceeds 2 MB limit')
                charset = response.headers.get_content_charset() or 'utf-8'
                return {'url': url, 'status': status, 'chain': chain,
                        'html': raw.decode(charset, errors='replace'),
                        'type': response.headers.get_content_type(), 'error': ''}
        raise ValueError('More than five redirects')
    except (URLError, OSError, ValueError, LookupError, HTTPException) as exc:
        return {'url': url, 'status': None, 'chain': chain, 'html': '', 'type': '', 'error': str(exc)}


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titles, self.headings, self.canonicals = [], [], []
        self.active = None
        self.parts = []
        self.base = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('title', 'h1'):
            self.active, self.parts = tag, []
        if tag == 'base' and self.base is None and attrs.get('href'):
            self.base = attrs['href']
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href', ''))

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == self.active:
            (self.titles if tag == 'title' else self.headings).append(' '.join(''.join(self.parts).split()))
            self.active = None


def check(row):
    findings = []
    def add(level, message):
        findings.append((level, message))
    old = fetch(row['old_url'])
    new = old if row['old_url'] == row['new_url'] else fetch(row['new_url'])
    if old['error']:
        add('REVIEW', 'Old URL could not be assessed: ' + old['error'])
    elif old['status'] in (401, 403, 429) or old['status'] >= 500:
        add('REVIEW', f"Old URL returned HTTP {old['status']}; access/server response needs investigation")
    else:
        if old['url'] != row['new_url']:
            add('FAIL', 'Old URL ends at an unexpected destination')
        if row['old_url'] != row['new_url']:
            if len(old['chain']) < 2:
                add('FAIL', 'Old URL does not redirect')
            elif any(h['status'] not in (301, 308) for h in old['chain'][:-1]):
                add('REVIEW', 'Redirect includes a temporary status')
            if len(old['chain']) > 2:
                add('REVIEW', 'Redirect chain has more than one hop')
        if old['status'] != 200:
            add('FAIL', f"Old URL finishes with HTTP {old['status']}")
    meta = Metadata()
    if new['error']:
        add('REVIEW', 'Destination could not be assessed: ' + new['error'])
    elif new['status'] in (401, 403, 429) or new['status'] >= 500:
        add('REVIEW', f"Destination returned HTTP {new['status']}; access/server response needs investigation")
    elif new['status'] != 200:
        add('FAIL', f"Destination returns HTTP {new['status']}")
    elif new['type'] not in ('text/html', 'application/xhtml+xml'):
        add('REVIEW', 'Destination is not HTML; metadata unassessed')
    else:
        if new['url'] != row['new_url']:
            add('FAIL', 'Expected new URL redirects elsewhere')
        meta.feed(new['html'])
        for label, values, expected in [('title', meta.titles, row.get('expected_title')), ('h1', meta.headings, row.get('expected_h1'))]:
            if len(values) != 1 or not values[0]:
                add('FAIL', f'Expected one nonempty {label}; found {len(values)}')
            elif expected and values[0] != ' '.join(expected.split()):
                add('FAIL', f'{label} does not match expected text')
        if len(meta.canonicals) != 1 or not meta.canonicals[0]:
            add('FAIL', 'Expected one nonempty canonical link')
        else:
            try:
                base = urljoin(new['url'], meta.base) if meta.base else new['url']
                if url_key(urljoin(base, meta.canonicals[0])) != row['expected_canonical']:
                    add('FAIL', 'Canonical does not match expected URL')
            except ValueError:
                add('FAIL', 'Canonical URL is invalid')
    result = 'FAIL' if any(x[0] == 'FAIL' for x in findings) else 'REVIEW' if findings else 'PASS'
    return {**row, 'result': result, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
            'old_final_url': old['url'], 'old_status': old['status'],
            'redirect_chain': ' -> '.join(f"{h['status']} {h['url']}" for h in old['chain']),
            'new_final_url': new['url'], 'new_status': new['status'],
            'actual_title': ' | '.join(meta.titles), 'actual_h1': ' | '.join(meta.headings),
            'actual_canonical': ' | '.join(meta.canonicals),
            'findings': '; '.join(f'{level}: {message}' for level, message in findings) or 'Configured checks passed'}


def report_csv(results):
    output = io.StringIO(newline='')
    fields = list(dict.fromkeys(k for row in results for k in row))
    writer = csv.DictWriter(output, fields)
    writer.writeheader()
    for row in results:
        # Neutralize spreadsheet formulas in untrusted URL/page content.
        writer.writerow({k: "'" + str(v) if str(v).lstrip().startswith(('=', '+', '-', '@')) else v for k, v in row.items()})
    return output.getvalue()


if __name__ == '__main__':
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path, default=Path('migration-report.csv'))
    args = parser.parse_args()
    try:
        results = [check(row) for row in parse_csv(args.input.read_text(encoding='utf-8-sig'))]
    except (ValueError, OSError) as exc:
        parser.exit(2, str(exc) + '\n')
    args.output.write_text(report_csv(results), encoding='utf-8-sig')
    print(f'Saved {len(results)} results to {args.output}')
