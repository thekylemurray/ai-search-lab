# Practice a website migration

Cedar Community Center is a fictional 20-page website. Compare original content, a flawed migration with ten seeded defects, and a corrected migration. Everything runs locally with the existing checker.

## Your first session (about 30–45 minutes)

1. Extract the complete Migration Checker ZIP. With Python 3.10+ installed, double-click **start-exercise-windows.cmd**. On other systems run `python3 exercise.py` from this folder.
2. Keep the console open. Your browser opens the exercise instructions and all twenty pages.
3. Download the flawed mapping, open the checker using the exercise link, load the CSV and run it. Save your report.
4. Write down what each finding means. Which items prevent launch? Which need investigation? Compare original and migrated pages, including opening hours and the transport page's HTML source.
5. Record each issue's page, observation, impact, proposed correction and verification method. A PASS means only that configured checks passed.
6. Run the supplied corrected mapping and save its report. Compare results, then open the answer key in the app.

The corrected version is prebuilt. Comparing it is not the same as implementing repairs yourself. Later, change one flawed route in `exercise.py` and predict its new result before rerunning.

## Answer key (spoilers)

| Page | Seeded defect | Result | Correction |
| --- | --- | --- | --- |
| welcome | Redirect points to news | FAIL | Point to welcome |
| about | New page returns 404 | FAIL | Restore destination |
| classes | Missing title | FAIL | Restore title |
| volunteer | Incorrect H1 | FAIL | Restore heading |
| events | Canonical points to old URL | FAIL | Use destination canonical |
| contact | Temporary 302 | REVIEW | Direct permanent 301 |
| membership | Two-hop redirect | REVIEW | Direct permanent 301 |
| access | Redirect loop | REVIEW | Redirect to destination |
| hours | Opening-hours paragraph removed | PASS — known miss | Restore paragraph; compare manually |
| transport | Meta description removed | PASS — known miss | Restore description; inspect HTML |

The remaining ten pages are clean controls. Flawed: **12 PASS, 5 FAIL, 3 REVIEW**. Corrected: **20 PASS**. Eight of ten seeded defects are flagged; two are outside scope. Each seeded defect is on a separate page. Multiple findings on one page count as one flagged case.

These constructed fixtures do not establish production accuracy, time savings or SEO outcomes. No JavaScript rendering, indexing or visual/accessibility audit is performed. A corrected PASS report does not certify an entire migration. No client/employer data is included.

## Reproduce the benchmark

Run `python exercise.py --benchmark` from this folder. It starts a temporary local HTTP server, calls the existing checker against both versions and writes mappings, timestamped reports and a summary to `exercise-results/`. It exits nonzero if an expected status or diagnostic is missing. The server then stops; exported local URLs document that run and are not durable links. Interactive checks must use CSVs from the currently running exercise.

Run automated checks with `python -m unittest discover -s . -v`.

## Evidence after your session

Keep both reports, a screenshot and a short note explaining one redirect issue and one problem automation missed. Record the date, environment and what you personally reviewed. Only then describe that hands-on review in your portfolio. Automated verification and your review are separate evidence.
