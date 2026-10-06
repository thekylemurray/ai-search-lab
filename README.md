# AI Search Lab

Kyle Murray's Astro portfolio: web operations, structured CMS content, and AI discoverability experiments.

## Start with the evidence

- `/projects`: recruiter entry point for implemented examples.
- `/ev-lab`: Sanity + Astro implementation case study; `/vehicles` and `/compare` contain the demo.
- `/web-ops#applied-example`: optional-form defect, ownership decision, fix, and verification boundary.
- `/experiments/javascript-rendered-content`: rendering fixtures and an AI evaluation protocol, with an inconclusive direct-URL access pilot and a repeated-session protocol.
- `/about`: background and links to work evidence.

The root route is the portfolio entrance; /vehicles/ contains the EV offers demo and /ai-search-lab/ retains the wider lab introduction.

## Develop and validate

Requires Node.js >=22.12.0.

```sh
npm ci
npm run dev
```

```sh
npm run build
npm run check:evidence
npm run check:discoverability
npm run preview
```

The full static build reads the configured public Sanity dataset for vehicle pages, so it requires network access. No secret is required by the checked-in read client. The separate Sanity Studio lives in `studio-kyles-ev-landing-lab/`.

`check:evidence` first checks attribution handling using small input stand-ins, then inspects built rendering fixtures under `dist/`. It must run after a successful build. These checks do not submit lead forms, validate downstream delivery, or test AI retrieval.

## Content and implementation

- `src/content/experiments/`: Markdown entries validated by `src/content.config.ts`.
- `src/layouts/`: shared portfolio and experiment layouts.
- `src/pages/`: Astro routes, including CMS-backed vehicle views.
- `src/data/renderTestContent.ts`: shared rendering fixture.
- `src/lib/attribution.js`: optional-form attribution helper.
- `scripts/`: reproducible evidence checks.

See [the portfolio evidence audit](docs/portfolio-evidence-audit.md) for priorities, claim boundaries, validation, and evidence still needed. Business performance and AI citation improvements are not established by this repository.

## Discoverability foundation

All HTML routes use a shared document layout for titles, descriptions, canonical URLs, Open Graph metadata, and minimal WebSite/WebPage JSON-LD. Vehicle views retain their existing presentation. The production origin is configured in `astro.config.mjs`; trailing-slash URLs match the observed Cloudflare redirect behavior.

The portfolio root and separate vehicle listing are self-canonical and included in the generated sitemap. `/thank-you/` has `noindex, follow` and is excluded from the sitemap. `robots.txt` allows crawling and advertises the sitemap index. Rendering fixtures remain self-canonical and included so later retrieval evaluations can observe them; they are similar-content test pages, and independent indexing is not guaranteed.

`npm run check:discoverability` inspects every generated HTML page and sitemap entry after a build. It verifies document metadata, canonical targets, basic JSON-LD consistency, and sitemap/indexability alignment. It is not a Schema.org validator, browser test, indexing report, or proof of AI citation improvement. No Product/Offer markup is asserted for the sample vehicle inventory.

## Recruiter case study and retrieval pilot

- /case-studies/discoverability-foundation/: problem, implementation, verification, and claim boundaries.
- /experiments/direct-url-retrieval-pilot/: October 5, 2026 local-date pilot (October 6 UTC); all three direct opens returned access errors. Rendering effects and answer accuracy remain unevaluated.
- public/evidence/retrieval-2026-10-06/: protocol, exact tool request/response, and a separate search follow-up log.
