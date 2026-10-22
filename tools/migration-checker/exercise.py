"""Fictional 20-page migration exercise; Python 3.10+, standard library only."""
import csv
import html
import io
import threading
import webbrowser
from collections import Counter
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from app import Handler, page
from checker import check, parse_csv, report_csv

PAGES = [('welcome','Welcome'), ('about','About the center'), ('classes','Classes'),
         ('volunteer','Volunteer'), ('events','Events'), ('contact','Contact'),
         ('membership','Membership'), ('access','Accessibility'), ('hours','Opening hours'),
         ('transport','Getting here'), ('art','Art studio'), ('music','Music room'),
         ('garden','Community garden'), ('library','Library'), ('fitness','Fitness room'),
         ('cooking','Cooking classes'), ('languages','Language exchange'),
         ('families','Family activities'), ('donate','Support the center'), ('news','Center news')]
# Expected findings are an explicit answer key, independent of the checker.
DEFECTS = [
    ('welcome','Wrong redirect target','FAIL','unexpected destination'),
    ('about','Destination returns 404','FAIL','Destination returns HTTP 404'),
    ('classes','Missing title','FAIL','Expected one nonempty title'),
    ('volunteer','Wrong H1','FAIL','h1 does not match'),
    ('events','Canonical points at old URL','FAIL','Canonical does not match'),
    ('contact','Temporary redirect','REVIEW','temporary status'),
    ('membership','Redirect chain','REVIEW','more than one hop'),
    ('access','Redirect loop','REVIEW','Redirect loop'),
    ('hours','Missing opening-hours paragraph','PASS',None),
    ('transport','Missing meta description','PASS',None),
]


def mapping(base, mode):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['old_url','new_url','expected_title','expected_h1','expected_canonical'])
    for slug, title in PAGES:
        new = f'{base}/exercise/{mode}/new/{slug}'
        writer.writerow([f'{base}/exercise/{mode}/old/{slug}', new,
                         title + ' | Cedar Community Center', title, new])
    return output.getvalue()


class ExerciseHandler(Handler):
    def do_GET(self):
        if self.headers.get('Host') != urlsplit(self.base).netloc:
            self.send(403, 'Open the printed 127.0.0.1 address.'); return
        path = urlsplit(self.path).path
        if path == '/exercise/':
            links = ''.join(f'<li>{html.escape(title)}: <a href="/exercise/before/{slug}">Original</a> · '
                f'<a href="/exercise/broken/new/{slug}">Migrated</a> · '
                f'<a href="/exercise/fixed/new/{slug}">Corrected</a></li>' for slug, title in PAGES)
            self.send(200, page('''<section><h2>Practice migration: Cedar Community Center</h2>
<p>Fictional local website. Twenty mapped pages; ten seeded defects. No client data.</p>
<ol><li>Download the <a href="/exercise/broken.csv" download>flawed migration mapping</a>.</li>
<li><a href="/" target="_blank" rel="noopener">Open the checker</a>, load that CSV, run checks and download your report.</li>
<li>Compare original and migrated pages below. Record what you would fix before launch, including problems absent from the report.</li>
<li>Download the <a href="/exercise/fixed.csv" download>corrected mapping</a> and run it in the checker.</li>
<li>After your review, open the <a href="/exercise/answers">answer key</a>.</li></ol>
<p>Both versions are supplied for comparison. PASS covers only configured checks. Keep the console open during the exercise.</p></section>
<section><h2>Page comparison</h2><ul>''' + links + '</ul></section>')); return
        if path in ('/exercise/broken.csv', '/exercise/fixed.csv'):
            self.send(200, mapping(self.base, path.rsplit('/',1)[-1][:-4]), 'text/csv; charset=utf-8'); return
        if path == '/exercise/answers':
            rows = ''.join(f'<tr><td>{slug}</td><td>{label}</td><td>{result}</td></tr>' for slug,label,result,_ in DEFECTS)
            self.send(200, page('<section><h2>Answer key — spoilers</h2><p>Flawed: 12 PASS, 5 FAIL, 3 REVIEW. Corrected: 20 PASS.</p>'
                '<p>Eight of ten seeded defects are flagged. Body content and meta descriptions are outside checker scope and return PASS. '
                'Ten other pages are clean controls. REVIEW means investigate; a loop prevents access, while a temporary redirect may be intentional.</p>'
                '<div class="scroll"><table><tr><th>Page</th><th>Seeded defect</th><th>Result</th></tr>' + rows + '</table></div>'
                '<p>The corrected version restores all missing or incorrect content and metadata, restores the missing destination, '
                'and uses direct permanent redirects to each intended destination. Compare it with your proposed corrections.</p>'
                '<p>This constructed benchmark is not a production accuracy estimate or proof of indexing.</p><a href="/exercise/">Back</a></section>')); return
        if path.startswith('/exercise/'):
            self.exercise_page(path); return
        super().do_GET()

    def exercise_page(self, path):
        parts = path.strip('/').split('/')
        if len(parts) == 3 and parts[1] == 'before':
            mode, stage, slug = 'before', 'new', parts[2]
        elif len(parts) == 4 and parts[1] in ('broken','fixed') and parts[2] in ('old','new','hop'):
            _, mode, stage, slug = parts
        else:
            self.send(404, 'Not found'); return
        if slug not in dict(PAGES):
            self.send(404, 'Not found'); return
        target = f'/exercise/{mode}/new/{slug}'
        broken = mode == 'broken'
        if stage in ('old','hop'):
            status = 301
            if broken and stage == 'old':
                if slug == 'welcome': target = '/exercise/broken/new/news'
                if slug == 'contact': status = 302
                if slug == 'membership': target = '/exercise/broken/hop/membership'
                if slug == 'access': target = '/exercise/broken/old/access'
            self.send(status, '', headers={'Location': target}); return
        if broken and slug == 'about':
            self.send(404, 'Synthetic missing page'); return
        title = dict(PAGES)[slug]
        title_tag = f'<title>{html.escape(title)} | Cedar Community Center</title>'
        h1, canonical = title, path
        description = f'<meta name="description" content="Explore {html.escape(title.lower())} at Cedar Community Center.">'
        paragraph = ('Open Monday to Friday, 09:00–18:00. Saturday, 10:00–14:00.' if slug == 'hours'
                     else f'Learn about {title.lower()} at Cedar Community Center.')
        if broken:
            if slug == 'classes': title_tag = ''
            if slug == 'volunteer': h1 = 'Unrelated page heading'
            if slug == 'events': canonical = '/exercise/broken/old/events'
            if slug == 'hours': paragraph = ''
            if slug == 'transport': description = ''
        self.send(200, f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">{title_tag}{description}
<link rel="canonical" href="{canonical}"></head><body><p>Fictional practice site · {mode}</p>
<main><h1>{html.escape(h1)}</h1><p>{html.escape(paragraph)}</p></main>
<p><a href="/exercise/">Return to exercise</a></p></body></html>''')


def run_benchmark(base, output):
    output.mkdir(parents=True, exist_ok=True)
    expected = {slug:(result,finding) for slug,_,result,finding in DEFECTS}
    summaries, errors = [], []
    for mode in ('broken','fixed'):
        csv_text = mapping(base, mode)
        results = [check(row) for row in parse_csv(csv_text)]
        (output / f'{mode}-mapping.csv').write_text(csv_text, encoding='utf-8')
        (output / f'{mode}-report.csv').write_text(report_csv(results), encoding='utf-8-sig')
        for (slug,_), row in zip(PAGES, results):
            status,finding = expected.get(slug, ('PASS',None)) if mode == 'broken' else ('PASS',None)
            if row['result'] != status or (finding and finding not in row['findings']):
                errors.append(f'{mode}/{slug}: expected {status} / {finding}; got {row["result"]} / {row["findings"]}')
        summaries.append(f'{mode}: {dict(Counter(r["result"] for r in results))}')
    text = '\n'.join(summaries + errors + [
        'Seeded defects: 10. Expected flagged: 8. Known misses: body content, meta description.',
        'Clean controls: 10. Expected false flags on controls: 0.',
        'Constructed local fixture only; not production accuracy. Reports contain ephemeral local URLs.',
        'Expected outcomes verified.' if not errors else 'OUTCOME MISMATCH: investigate before citing results.'
    ]) + '\n'
    (output / 'summary.txt').write_text(text, encoding='utf-8')
    print(text)
    return not errors


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark', action='store_true')
    parser.add_argument('--output', type=Path, default=Path('exercise-results'))
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1',0), ExerciseHandler)
    base = f'http://127.0.0.1:{server.server_port}'
    if args.benchmark:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            success = run_benchmark(base, args.output)
        finally:
            server.shutdown(); server.server_close(); thread.join()
        raise SystemExit(0 if success else 1)
    print(base + '/exercise/\nKeep this window open. Press Ctrl+C to stop.')
    webbrowser.open(base + '/exercise/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
