---
title: Direct URL Retrieval Pilot
description: Three rendering URLs tested through an AI assistant's web retrieval tool, with exact requests, access errors, and an inconclusive result.
status: "Access pilot recorded; answer evaluation blocked"
updated: 2026-10-06
tags: ["AI Search", "JavaScript", "Technical SEO"]
---

## Result

On October 5, 2026 in Raleigh (October 6 UTC), an AI assistant's web retrieval tool attempted to open all three published rendering fixtures. **None returned page content.** Each returned “not accessible via this tool.”

This is a recorded access pilot with an inconclusive rendering result. It does not show that the pages are unavailable to everyone, that JavaScript caused the failure, or that any variant performs better in AI search. The planned answer-quality experiment remains blocked.

## Question and method

Could this assistant retrieve enough page text from a supplied URL to identify the fixture's recommendation and context?

One batched tool call opened the static, pre-rendered, and client-rendered URLs. The protocol and scoring criteria were written before that call. This was direct-URL access, not open-web discovery.

Environment: ChatGPT Work assistant using its web retrieval tool. The tool did not expose a model version. The assistant had already seen repository ground truth, so this was not blinded: only newly returned web text could support an answer.

Exact answer instruction:

> Using only text returned by the web retrieval tool for [URL], state the main recommendation and experiment context. If either is unavailable, report unavailable. Do not fill gaps from repository or conversation context.

The actual tool request supplied three URLs through the open operation. It did not submit this natural-language instruction to a separate model or independent chat session.

## Observations and constrained answers

| Supplied URL | Tool observation | Recommendation answer | Context answer | Usable page citation |
| --- | --- | --- | --- | --- |
| [Static](https://ai-search-lab.pages.dev/render-tests/static/) | Access error; no page body | Unavailable | Unavailable | None |
| [Pre-rendered](https://ai-search-lab.pages.dev/render-tests/pre-rendered/) | Access error; no page body | Unavailable | Unavailable | None |
| [Client-rendered](https://ai-search-lab.pages.dev/render-tests/client/) | Access error; no page body | Unavailable | Unavailable | None |

These answers are the assistant's constrained responses to the returned errors, not independent model outputs. Tool-generated error references are not citations supporting page content.

- Page-body retrieval: **0 of 3 URLs** in one batch.
- Factual accuracy and completeness: **not assessable** because no page text was returned.
- Usable retrieved-page citations: **0 of 3 URLs**, not an organic citation rate.
- Rendering comparison: **inconclusive**.

## Raw evidence

- [Protocol, URLs, prompt, and scoring criteria (JSON)](/evidence/retrieval-2026-10-06/protocol.json)
- [Exact request and raw tool response (JSON)](/evidence/retrieval-2026-10-06/raw-tool-response.json)

The raw response preserves access errors and tool-generated references. No successful retrieval or citation has been substituted from repository content.

## Search follow-up

On October 6 local time, two search backends were queried with the same diagnostic query: site:ai-search-lab.pages.dev/render-tests/ "initial HTML".

The first returned no results. The second returned ten off-domain results and no target-domain result. Off-domain results were excluded from the evidence set. These observations do not establish that the pages are unindexed, and the search follow-up is not a rendering comparison or a fresh-session answer test.

[Search requests and observed result URLs (JSON)](/evidence/retrieval-2026-10-06/search-followup.json) are recorded separately. Third-party page text is not reproduced.

## What this demonstrates

Record failed observations, distinguish an access problem from a content-quality score, and avoid claiming a rendering effect when retrieval itself fails.

The [local rendering checks](/experiments/javascript-rendered-content/) still establish initial-HTML availability. They answer a different question from external retrieval.

## Limits and next run

This was one request per URL in one existing conversation, with no repeated fresh sessions. The variants differ in titles, metadata, labels, and timestamp. Network access, extraction behavior, or caching may explain the failure; this run cannot identify the cause.

Next, verify that the chosen AI product can open a test URL. Then use neutral content with matched metadata and run at least three fresh sessions per variant in varied order. Preserve complete answers and actual cited URLs, and score only facts supported by successful retrieval. Keep no-URL discovery testing separate.
