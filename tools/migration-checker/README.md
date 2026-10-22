# Migration Checker — first working version

A local Python tool for reviewing a CSV of old/new URL pairs. No third-party Python packages or paid services required. Python 3.10+ must already be installed.

## Start on Windows

1. Extract the entire ZIP to a folder.
2. Double-click `start-windows.cmd` (requires the Python launcher).
3. Your default browser opens the local interface. Keep the console window open while using it.
4. Choose **Load synthetic demo**, then **Run checks**. Expected: **1 PASS, 3 FAIL, 4 REVIEW**.
5. Download the report. Close the console window when finished.

If the launcher is unavailable, run `python app.py` from this folder. macOS/Linux users can run `python3 app.py`. The server binds only to 127.0.0.1 on an available port. This is a local workstation tool, not a publicly hosted application.

## Check your own mapping

Load a UTF-8 CSV or paste CSV text, using these column names:

- `old_url`, `new_url`: required absolute HTTP(S) URLs.
- `expected_title`, `expected_h1`: optional exact text expectations, with whitespace normalized. If blank, checks require one nonempty element each.
- `expected_canonical`: optional; defaults to new_url. Relative page canonicals are resolved against the document/base URL.

Maximum 50 pairs, fetched sequentially. Only check URLs you intend to request. Credential-bearing URLs and fragments are rejected. No credentials/cookies are supplied. The checker follows up to five redirects and reads up to 2 MB per response; each request has an eight-second socket timeout. Large or slow batches can take several minutes. There is no cancel button; stop the app to interrupt a run.

URL comparisons preserve path case, trailing slashes and query strings. Scheme/hostname/default ports are normalized. Supply the exact intended final new URL. An unchanged old/new URL does not require a redirect. HTTP 301/308 are treated as permanent; temporary redirects and chains are review items.

## Reports

- PASS: all configured checks passed.
- FAIL: an observed mismatch, missing redirect, bad destination status, or metadata failure.
- REVIEW: blocked/rate-limited/server-error response, request failure, temporary redirect, chain, loop, or non-HTML destination requiring investigation.

A FAIL row may also include REVIEW findings. Read the findings column. Reports contain UTC check time, expected/actual values, redirect paths, final URLs/statuses and findings. CSV cells that could act as spreadsheet formulas are prefixed with an apostrophe. Reports are downloaded locally; the app does not retain a run history.

CLI alternative: `python checker.py template.csv --output migration-report.csv`.

## Synthetic validation

`python -m unittest discover -s . -v`

Tests use a real local HTTP server, with eight deliberately constructed cases: correct redirect, wrong target, 404, wrong title/H1/canonical, temporary redirect, redirect chain, 403, and loop. Additional checks cover HTML extraction, unsafe CSV formulas, invalid inputs, UI responses, downloadable report generation and request-token enforcement. The fixtures are not client data or proof of a successful production migration.

Limitations: initial response HTML only; no JavaScript rendering, visual inspection, full content comparison, robots/noindex checks, browser/session authentication, sitemap crawl or indexing claims. A one-H1 requirement is this checklist's convention, not a universal SEO rule. No benchmarked time savings. An owner-supplied browser screenshot and downloaded CSV were reviewed on October 16, 2026: all eight demo cases matched the expected 1 PASS, 3 FAIL and 4 REVIEW results. A narrow Result column observed in that screenshot was subsequently corrected; the revised layout still needs a browser recheck. The exact launcher path and Python version were not captured. Implemented with AI assistance; designed to be read and extended as a Python learning project.

Files to explore: `checker.py` contains CSV parsing, HTTP fetching, HTML extraction and checks; `app.py` supplies the local interface and demo routes; `test_checker.py` provides repeatable tests.

## Twenty-page practice migration

Double-click `start-exercise-windows.cmd` for a fictional community website with original, flawed and corrected versions. Follow [EXERCISE.md](EXERCISE.md) for the guided review. The exercise includes ten seeded defects, two known checker blind spots, downloadable mappings and an answer key. Run `python exercise.py --benchmark` to reproduce both reports automatically.
