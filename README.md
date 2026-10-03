# AI Search Lab

Kyle Murray's Astro portfolio: web operations, structured CMS content, and AI discoverability experiments.

## Start with the evidence

- `/projects`: recruiter entry point for implemented examples.
- `/ev-lab`: Sanity + Astro implementation case study; `/vehicles` and `/compare` contain the demo.
- `/web-ops#applied-example`: optional-form defect, ownership decision, fix, and verification boundary.
- `/experiments/javascript-rendered-content`: rendering fixtures and an AI evaluation protocol, with AI evaluation explicitly pending.
- `/about`: background and links to work evidence.

The existing `/` route remains the EV offers listing; `/ai-search-lab` is the portfolio landing page.

## Develop and validate

Requires Node.js >=22.12.0.

```sh
npm ci
npm run dev
```

```sh
npm run build
npm run check:evidence
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
