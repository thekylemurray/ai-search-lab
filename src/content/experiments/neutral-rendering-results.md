---
title: Initial HTML and AI Answers — A Nine-Run Exploratory Study
description: User-supplied Gemini Flash-lite responses matched six facts on initial-HTML pages and returned unavailable on a JavaScript-content page, with retrieval provenance unverified.
status: "Nine responses collected; exploratory result"
updated: 2026-10-15
tags: ["AI Search", "JavaScript", "Content Architecture", "Technical SEO"]
---

## Result

Across nine user-supplied responses attributed to Gemini Flash-lite, both initial-HTML control pages received six correct fact answers in all three runs per page. The JavaScript-content page received six “Unavailable” answers in all three runs. Every supplied response included the requested page URL.

**This is a repeatable pattern in the supplied answers, not proof of an isolated causal rendering effect.** We do not have provider retrieval logs. All access classifications remain unverified, including the answers that matched the facts.

| Page | Content delivery | Runs | Factual answer result | Requested URL included |
|---|---|---|---|---|
| A | Build-time HTML | 3 | 6/6 matches in each run | 3/3 |
| B | Identical build-time control | 3 | 6/6 matches in each run | 3/3 |
| C | Browser JavaScript inserts facts | 3 | Six unavailable items in each run; accuracy NA | 3/3 |

A/B together supplied 36 matching fact answers across six runs. C supplied no factual answers; it did not assert six incorrect facts. Its responses do not distinguish a page-access failure from a failure to extract the details. Citation occurrence alone would have hidden this difference in answer usefulness.

## Question and implementation

Could one AI product extract the same six facts from a supplied URL when they were delivered in initial HTML versus inserted by JavaScript?

I prepared a fictional workshop fixture with six facts, matched titles, descriptions and headings, and three versioned routes. A/B are identical build-time controls; C inserts the facts with JavaScript. These are **two rendering conditions**, not three distinct architectures. The pages contain no visible rendering labels or timestamps. Canonical URLs differ, and C initially shows a loading message.

- [Page A](/render-tests/v2/a/)
- [Page B](/render-tests/v2/b/)
- [Page C](/render-tests/v2/c/)
- [Frozen implementation at the study merge](https://github.com/thekylemurray/ai-search-lab/tree/f6331feb1a9f4639711246f55ec4c1311835b99d/src/pages/render-tests/v2)

The fixture revision is `retrieval-v2.1`, merged in PR #8 as `f6331feb1a9f4639711246f55ec4c1311835b99d`. Initial deployment checks returned HTTP 200 for A/B/C. A/B contained all six facts outside scripts/styles; C contained the loading state and insertion script. I confirmed C displayed the details in my regular browser. This does not establish that an AI product executed its script. The client facts are also present in its inline script payload, so a tool could potentially extract them without executing JavaScript.

## Procedure and evidence quality

The [prewritten guide](https://github.com/thekylemurray/ai-search-lab/blob/f6331feb1a9f4639711246f55ec4c1311835b99d/docs/retrieval-study-v2.md) defined the prompts, answer key and balanced sequence: A/B/C, B/C/A, C/A/B. Each assigned prompt differed only by URL. The operator was instructed to use a fresh chat for every run, retain Flash-lite mode, and avoid corrections or retries.

The evidence consists of responses pasted into the project conversation. Flash-lite was identified at preflight; continued use was instructed but not reconfirmed independently for every run. Fresh-chat use, memory settings, exact browsing mode and exact model build remain unconfirmed. Assigned prompts are preserved, but actual submitted prompts were not captured independently. No original provider exports or tool traces are available.

Responses were reported October 14–15, 2026, America/New_York. **Those are reporting dates, not verified execution dates.** The pause before run 07 is visible in reporting times; whether execution also spanned both days remains unresolved. Run 01 contained a duplicate paste and is counted once. No replacement or invalid run was reported.

## Run-level observations

| Run | Page | Reported locally | Factual matches | Unavailable items | Requested URL included |
|---|---|---|---|---|---|
| 01 | A | Oct 14, 23:27:03 | 6/6 | 0 | Yes |
| 02 | B | Oct 14, 23:27:35 | 6/6 | 0 | Yes |
| 03 | C | Oct 14, 23:28:17 | NA | 6 | Yes |
| 04 | B | Oct 14, 23:28:57 | 6/6 | 0 | Yes |
| 05 | C | Oct 14, 23:29:35 | NA | 6 | Yes |
| 06 | A | Oct 14, 23:30:08 | 6/6 | 0 | Yes |
| 07 | C | Oct 15, 19:24:17 | NA | 6 | Yes |
| 08 | A | Oct 15, 19:30:34 | 6/6 | 0 | Yes |
| 09 | B | Oct 15, 19:31:06 | 6/6 | 0 | Yes |

No wrong factual assertions appear in the nine supplied responses. The listed links match the assigned URLs as pasted; they are not independently verified provider citation records. A/B correctness is a factual-match score with unverified retrieval provenance.

## Preflights — excluded from results

Two preflights attributed to GPT-6 Astra Medium reported that A/B were unavailable; testing in that environment stopped before scored runs. Gemini preflights then returned all six matching facts for A/B and unavailable for C. These five preflights are not pooled with the nine-run set, and this is not a controlled comparison of AI products.

Gemini preflight A's pasted source link ended with a pipe character. Whether this was a copy artifact or actual link error was not resolved. The nine scored responses did not contain that malformed destination.

## Interpretation and practical value

The observed answer pattern is consistent with a limitation related to how the facts were delivered. It is insufficient to identify the mechanism: caching, extraction behavior, account history, URL-specific treatment or alternate sources may contribute. A/B duplicates may be deduplicated by retrieval systems. Correct answers do not establish live retrieval, and unavailable answers do not prove the entire page was inaccessible.

For web production, the project demonstrates how to make a content-availability question testable, verify initial HTML, define a scoring procedure, and separate factual answers from citation occurrence. It does not establish an organic discovery rate, traffic gain, conversion gain, universal crawler behavior or improved AI visibility.

A suitable portfolio statement is: “Built matched rendering fixtures and evaluated nine user-supplied Gemini Flash-lite responses; documented complete factual matches for initial-HTML controls and unavailable answers for the client-content variant, with explicit retrieval and causality limits.”

## Evidence and next validation

- [Nine normalized response transcripts, assigned prompts and scores (JSON)](/evidence/retrieval-v2-2026-10-15/runs.json)
- [Separate preflight summaries (JSON)](/evidence/retrieval-v2-2026-10-15/preflights.json)
- [Evidence provenance notes](/evidence/retrieval-v2-2026-10-15/README.md)
- [Original fixture and historical access pilot](/experiments/javascript-rendered-content/)

The transcripts normalize Markdown formatting; they are not raw provider exports. Small sample size, one topic/product, duplicate controls, public facts/source code, potential caching and unconfirmed session settings limit generalization. The public answer key could also be found elsewhere. None of the nine records qualifies as independently verified retrieval.

A stronger follow-up would capture provider-visible retrieval evidence and exact session settings, confirm execution times, and repeat with multiple fresh synthetic fact sets. Preserve this set unchanged rather than retroactively upgrading its evidence quality.
