# Recruiter evidence audit — October 3, 2026

Reviewed `main` at `f139fe459682dd7a05fd021137496acfd3d3765b` and the current implementation. The June 24 Web Ops addition (`8a756af`) introduced the process framework; the July 17 About change (`f139fe4`) improved the photo layout. Neither added measured outcomes or work artifacts.

## Priorities

| Priority | Page | Evidence gap | Addition in this change | Next evidence to collect |
|---|---|---|---|---|
| 1 | Web Ops | Generic workflow and checklist; no actual decision, defect, or result | Applied optional-form defect walkthrough, ownership rationale, code fix, regression checks, release gate | An anonymized real launch record: scope, personal responsibility, issue log, sign-off, dates, and measured rework or turnaround |
| 2 | EV Landing Lab | Implemented functionality hidden behind a short technology overview | Problem, scope, data flow, source links, tradeoffs, verified implementation boundaries | CMS-to-page screenshots, verified test lead delivery, publish-time baseline, and event validation |
| 3 | JavaScript rendering experiment | Planning copy despite existing fixtures; inaccurate request-time SSR description; duplicated client fixture | Correct build-time classification, shared content, automated initial-HTML check, explicit AI test protocol | Dated model/product run log, raw responses/citations, scoring criteria, and repeated trials |
| 4 | Projects and About | Projects linked to EV homepage as AI Search Lab; About asserted working style without proof links | Three evidence entry points and explicit prototype status; corrected Lab destination | Only verified role scope and outcome summaries tied to real work artifacts |
| 5 | AI-understand and SEO-vs-AI | Hypotheses and empty scorecards; no completed observations | Retained their existing Planning/Draft status; kept secondary to working examples | Finish one narrow evaluation before expanding topics; remove or replace subjective “citation likelihood” with observed citation occurrence |

## Guardrails for future claims

- Report personal contributions separately from team responsibilities.
- Label reconstructions and sample workflows. Do not present them as historical employer artifacts.
- Distinguish implemented behavior, local checks, deployed browser validation, and business outcomes.
- A technical fix is not proof of revenue recovery or conversion improvement.
- For a percentage, retain numerator, denominator, baseline, time window, and measurement source. For time savings, show the prior workflow and comparable tasks.
- Do not add employer metrics, screenshots, customer data, or internal materials without confirming accuracy and permission to share.

## Technical findings

The vehicle template rendered the form only when `showLeadForm === true`, while the inline script always accessed the UTM inputs. The change checks input existence and tests the absent-form path, decoded values, and missing parameters. It preserves current-page attribution behavior; it does not add cross-page persistence.

The rendering fixtures use Astro static output. Both `/render-tests/static` and `/render-tests/pre-rendered` generate HTML at build time. No server adapter is configured. The browser-rendered route now imports the same content module. Labels, metadata, and a timestamp remain differences, explicitly documented as confounders rather than calling this a controlled AI experiment.

Other production gaps are documented, not silently represented as solved: no required vehicle-field validation, phone/text preferences without phone collection, no checked-in deployment/webhook configuration, no confirmed end-to-end lead-delivery report, and no analytics event implementation demonstrated in the reviewed pages.

## Validation

- `npm ci --no-audit --no-fund`: completed.
- `npm run build`: passed, 26 static pages, with reads from the configured Sanity dataset.
- `npm run check:evidence`: passed after build. All three attribution scenarios and all three initial-HTML assertions passed.
- `git diff --check`: passed.
- Internal route links on the six edited portfolio pages resolve to generated HTML files.
- Browser QA attempted with Playwright, but the installed runtime had no Chromium executable. Browser behavior and responsive layout remain unverified in this run.
- No lead form was submitted; no external AI retrieval experiment was run.

## Review and deployment

Committed locally on `portfolio/recruiter-evidence`. Remote publication was blocked: Git had no push credentials, and the GitHub integration returned 403 (Resource not accessible by integration). No draft PR was created and no production deployment was performed. The handoff contains an apply-ready Git patch. Source links target `main`; links to newly added helpers become available after merge. Preview those files locally until then.
