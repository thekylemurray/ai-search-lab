# Discoverability foundation — October 3, 2026

Prepared against main at `d60e5a14c1d02d639b3f8d04f24c9dc7430365a7`.

## Problem and implementation

Portfolio pages had titles and descriptions, but the vehicle listings, detail routes, comparison view, and confirmation route lacked a shared HTML document head. Canonical URLs, machine-readable page descriptions, and a generated sitemap were not implemented.

A shared `DocumentLayout.astro` now supplies a complete document, metadata, canonicals, Open Graph tags, and minimal WebSite/WebPage JSON-LD. `BaseLayout.astro` retains the portfolio navigation and footer while delegating the document to this layout. Vehicle templates use the same document without adding portfolio navigation.

Astro's production site is configured as `https://ai-search-lab.pages.dev`. Trailing-slash canonical URLs match the 308 redirect observed for the live `/ai-search-lab` route during this work. The official sitemap integration discovers generated routes, including CMS and content-collection routes. `robots.txt` advertises the sitemap and permits crawling.

## Decisions

- `/` and `/vehicles/` show the same underlying offers. The root canonical points to `/vehicles/`; the root stays accessible but is excluded from the sitemap. This is a preference signal, not a redirect or guarantee of search-engine selection.
- `/thank-you/` is noindex and omitted from the sitemap. Its copy no longer promises contact by a vehicle specialist or implies that visiting it establishes successful delivery.
- Rendering fixtures remain self-canonical and in the sitemap for future retrieval investigation. Their similar content may affect indexing; their inclusion is not evidence that engines will index each variant.
- JSON-LD describes the actual website and pages. Sample vehicles are not represented as verified commercial Product/Offer entities. CMS text is escaped before embedding JSON in a script element.
- No fabricated publication dates, last-modified timestamps, review scores, or outcome metrics are added.

## Verification

- `npm run build`: passed against the public Sanity dataset; 27 HTML pages generated, plus robots.txt and sitemap files.
- `npm run check:evidence`: passed all existing attribution scenarios and rendering assertions.
- `npm run check:discoverability`: passed checks across 27 HTML documents and 25 sitemap entries. Checks cover single document heads and titles, descriptions, canonical URLs and target files, Open Graph URL alignment, parseable JSON-LD and page-field consistency, noindex handling, and sitemap coverage.
- `git diff --check`: passed.
- Browser QA could not run because the installed Playwright runtime has no Chromium executable. Responsive rendering and browser console behavior remain unverified in this pass.

These are generated-output checks. They do not establish full Schema.org validation, rich-result eligibility, deployed behavior, indexing, traffic, or AI citations. Canonical and sitemap verification on the deployed site remains a post-merge step. The build still depends on the external Sanity dataset.

## Portfolio evidence

Implemented consistent metadata and canonical handling across an Astro portfolio and CMS-generated vehicle routes, added a generated sitemap and WebSite/WebPage JSON-LD, and verified 27 generated HTML documents with automated output checks.

Next: deploy after review, inspect the published output, then execute the documented AI retrieval evaluation and preserve raw observations. Measurement events and end-to-end lead delivery are a separate work item.

## Reference documentation

- https://docs.astro.build/en/guides/integrations-guide/sitemap/
- https://schema.org/WebPage
