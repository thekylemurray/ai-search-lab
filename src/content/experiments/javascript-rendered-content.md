---
title: Can AI Systems Retrieve JavaScript-Rendered Content Reliably?
description: A working rendering fixture with reproducible HTML checks and a separate plan for measuring AI retrieval.
status: "Implemented; AI evaluation pending"
updated: 2026-10-03
tags: ["AI Search", "JavaScript", "Content Architecture", "Technical SEO"]
---

## What this demonstrates

This experiment separates a question I can verify locally—whether the primary content is present in the initial HTML—from a question that requires external observations: whether an AI system retrieves, summarizes, and cites it accurately.

The deliverable is three working routes, a shared content fixture, and an automated check of the generated HTML. It is not evidence of improved rankings or AI citations.

## Implementation and technical decisions

- [Static HTML](/render-tests/static) reads the shared fixture during the Astro build.
- [Pre-rendered HTML](/render-tests/pre-rendered) does the same and includes a build timestamp. It is a second build-time control, **not request-time server rendering**.
- [Client-rendered JavaScript](/render-tests/client) initially contains a loading message; a browser script inserts the recommendation and context.

All three now import `src/data/renderTestContent.ts`, avoiding the independently copied client content in the original implementation. The repository uses Astro's default static output with no server adapter configured.

Page titles, descriptions, rendering labels, and the timestamp differ. This is an implementation comparison, not yet a controlled causal test of AI retrieval.

## Reproduce the HTML check

From the repository root:

```sh
npm ci
npm run build
npm run check:evidence
```

The full build reads the public Sanity dataset for the separate EV demo and therefore needs network access. The HTML check reads the generated `dist/render-tests/` files, excludes script and style content, and asserts the presence or absence of the exact recommendation.

The October 3, 2026 local build and all three HTML assertions passed. The build generated 26 pages; this count includes the wider portfolio and EV demo.

| Variant | Observed initial HTML | What the check establishes |
|---|---|---|
| Static | Recommendation present | Content can be read without executing browser JavaScript |
| Pre-rendered | Recommendation present | The build-time control also contains the content |
| Client | Loading message; recommendation absent | Primary content needs browser JavaScript |

[Review the check source](https://github.com/thekylemurray/ai-search-lab/blob/main/scripts/check-render-output.mjs) and [shared fixture](https://github.com/thekylemurray/ai-search-lab/blob/main/src/data/renderTestContent.ts).

## Interpretation and limits

Initial HTML availability is an observable property of the implementation. It does not establish what a particular crawler executes, whether a page is indexed, or whether an answer engine will cite it. No external AI retrieval results have been recorded here.

The recommendation inside the fixture is test content, not a finding about every AI system. The current topic also describes rendering itself; a future test should use neutral factual content to reduce that cue.

## Next evaluation protocol

1. Normalize titles, metadata, headings, and visible copy; remove the timestamp and variant labels from the evaluation pages.
2. Publish the variants and record their URLs, content revision, availability, and test date.
3. For each tested product, record its displayed model/version, browsing mode, exact prompt, and whether a URL was supplied. Keep direct-URL extraction separate from open-web discovery.
4. Run at least three fresh sessions per variant in varied order with the same prompts. Save complete responses and cited URLs.
5. Score summary accuracy against a fixed list of facts. Report retrieval success, factual completeness, and citation occurrence separately, with raw counts and failed runs.

Suggested direct-URL prompt: “Using this page, state its main recommendation and explain the experiment context: [URL].” For open-web discovery, use the same neutral topic question without a URL.

## Evidence still needed

A dated run log with raw answers, exact citations, and scoring is required before drawing conclusions about AI behavior. Differences could reflect indexing, caching, product behavior, or content cues as well as rendering.
