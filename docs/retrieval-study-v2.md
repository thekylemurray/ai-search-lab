# Neutral-content retrieval study: nine-run guide

**Status: prepared; not yet run. Content revision: retrieval-v2.1.**

## What we are trying to learn

Can one AI product accurately extract six facts from a supplied page when those facts are in the initial HTML versus inserted by JavaScript?

This is a small exploratory direct-URL extraction study. It does not measure organic discovery, rankings, traffic, or citation uplift. A and B are identical build-time controls; C uses browser JavaScript. There are **two rendering conditions**, with two control URLs. Report each URL separately; do not treat A/B as distinct architectures or the six control runs as six independent content samples.

The content describes a fictional paper workshop, not rendering or AI. The pages have matching titles, descriptions, headings, notice and final facts. URLs/canonicals necessarily differ, and C has a loading state and script. The original `/render-tests/static/`, `/pre-rendered/`, and `/client/` pages are retained unchanged for the older pilot.

## Before starting — deployment and access gate

1. Merge the preparation PR and wait for the production deployment to finish. Do not test undeployed URLs.
2. Record the merged commit SHA, deployment time and `retrieval-v2.1` below. Freeze the pages for all nine runs. Any fact change requires a new revision and a new run set.
3. In a browser, open all three pages. Each must show the same six workshop facts with JavaScript enabled. Inspect the initial response/source: A/B contain the facts; C does not. Check the browser console on C. Save dated observations. Build checks alone do not prove browser execution.
4. In a separate fresh chat using the chosen product/model and web mode, perform one access preflight on each URL. Use the corresponding prompt below. Label these P-A, P-B and P-C; preserve them but **do not count them in the nine scored runs**.
5. If neither control returns page-specific facts, stop: the study is blocked for that environment. Record the errors rather than scoring answer accuracy as zero. If at least one control works, proceed and retain all later failures, including failures on C. A C-only failure is an observation, not a reason to discard the run.

A browser or curl reaching the page does not establish that the chosen AI product can retrieve it. A correct answer alone does not prove JavaScript execution: products may use caches or alternate sources. Keep preflight attempts because they can themselves affect caching.

## Your task — one prompt per fresh chat

Use the same product, displayed model and browsing mode throughout. Prefer temporary chats with memory/personalization disabled where available; record the setting. Do not paste the answer key, this guide, repository content or previous answers into those chats. If model identity is not displayed, write “not exposed”; do not guess.

Run in the order below. Each row is a **new chat**, including repeats. Send the prompt once, save the complete response and citations, and do not correct, regenerate or coach it. Preserve a failed response just like a successful one. If you accidentally violate the protocol, mark the run invalid with a reason and append a replacement ID; never silently overwrite it. If the product changes models/modes mid-study, record that and analyze separately or start a new labeled set.

| Run | Page | URL |
|---|---|---|
| 01 | A | https://ai-search-lab.pages.dev/render-tests/v2/a/ |
| 02 | B | https://ai-search-lab.pages.dev/render-tests/v2/b/ |
| 03 | C | https://ai-search-lab.pages.dev/render-tests/v2/c/ |
| 04 | B | https://ai-search-lab.pages.dev/render-tests/v2/b/ |
| 05 | C | https://ai-search-lab.pages.dev/render-tests/v2/c/ |
| 06 | A | https://ai-search-lab.pages.dev/render-tests/v2/a/ |
| 07 | C | https://ai-search-lab.pages.dev/render-tests/v2/c/ |
| 08 | A | https://ai-search-lab.pages.dev/render-tests/v2/a/ |
| 09 | B | https://ai-search-lab.pages.dev/render-tests/v2/b/ |

This balanced rotation varies order; it is not randomization or blinding.

### Copyable prompt A — runs 01, 06, 08

```text
Open https://ai-search-lab.pages.dev/render-tests/v2/a/ and use only that page to answer: Where is the workshop, on what day does it run, what time does it start, how long does it last, how many participants can attend, and what should a visitor bring? Give one short answer for each item and cite the page you actually used. If the page or an item is unavailable, say unavailable. Do not infer missing facts or use other sources.
```

### Copyable prompt B — runs 02, 04, 09

```text
Open https://ai-search-lab.pages.dev/render-tests/v2/b/ and use only that page to answer: Where is the workshop, on what day does it run, what time does it start, how long does it last, how many participants can attend, and what should a visitor bring? Give one short answer for each item and cite the page you actually used. If the page or an item is unavailable, say unavailable. Do not infer missing facts or use other sources.
```

### Copyable prompt C — runs 03, 05, 07

```text
Open https://ai-search-lab.pages.dev/render-tests/v2/c/ and use only that page to answer: Where is the workshop, on what day does it run, what time does it start, how long does it last, how many participants can attend, and what should a visitor bring? Give one short answer for each item and cite the page you actually used. If the page or an item is unavailable, say unavailable. Do not infer missing facts or use other sources.
```

## Run-set record

- Operator and run-set ID:
- Merged commit / deployment time / content revision:
- Product / displayed model / browsing mode:
- Memory/personalization settings:
- Browser and initial-response verification, time and observations:
- Preflights P-A / P-B / P-C: dates, complete answers and cited URLs:
- Gate decision and reason:
- Start/end timestamps (include timezone):

## Blank scoring worksheet

All cells are deliberately unscored. Do not fill them with expected outcomes.

| Run | Page | Timestamp + timezone | Model/mode or change | Access evidence | Correct /6 or NA | Wrong facts | Missing facts | Exact-page citation? | Other source? | Raw response location |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | A | | | | | | | | | |
| 02 | B | | | | | | | | | |
| 03 | C | | | | | | | | | |
| 04 | B | | | | | | | | | |
| 05 | C | | | | | | | | | |
| 06 | A | | | | | | | | | |
| 07 | C | | | | | | | | | |
| 08 | A | | | | | | | | | |
| 09 | B | | | | | | | | | |

For each raw response save the run ID, exact sent prompt, complete answer, tool errors if visible, and actual citation target URLs. A response saying “I accessed it” is not sufficient evidence of access. Do not publish private chat-sharing links or account details; redacted text exports are sufficient. You can bring the saved answers back for scoring.

## Scoring rules — apply after collection

The answer key below is for the evaluator only. Do not send it to the tested chats.

| Item | Ground truth | Acceptable equivalence |
|---|---|---|
| Location | Cedar Room at Bellweather Hall | Both room and hall must be present |
| Day | Saturday | Case differences |
| Start | 10:40 a.m. | 10:40 AM or 10:40 in unambiguous morning context |
| Duration | 75 minutes | 1 hour 15 minutes |
| Capacity | 14 participants | 14 people |
| Bring | one blue pencil | A blue pencil |

Classify each requested item as correct, wrong, or missing/unavailable; no partial points. Count explicit contradictions as wrong. Flag unsupported extra assertions separately. On runs with assessable page-derived content, correct + wrong + missing must total six.

Record access evidence separately: **page text observed**, **page text partially observed**, **explicit access failure**, or **unverified**. When the product exposes no retrieved text, a plausible answer or link is only indirect evidence; label access unverified. Inspect cited targets after saving the answer, without interacting further with the tested chat. A citation to a different variant, this guide, or another source is a source deviation, even if the facts match.

For explicit access failure without page text, mark factual accuracy/completeness **NA**, retain any unsupported answers and errors, and count the failure in access totals. Do not silently turn it into six incorrect answers. When access is unverified, a factual-match score may be recorded but must be labeled unverified and excluded from verified-retrieval claims.

Report exact-page citation occurrence separately (yes/no; ignore trailing-slash normalization and fragments). A citation is not itself proof of extraction or proof that every claim is supported.

## Results format to publish after the study

For each page, report scheduled/completed/invalid runs, observed access categories, factual-match scores with verification status, exact-page citations out of completed runs, wrong facts and missing facts. Preserve raw counts and failures. Keep the three preflights separate. No results exist yet.

A defensible conclusion names the product, mode, date, revision and sample size: “In these three runs per URL, we observed …”. Equal results are useful. All-access-failure results mean the question remains unassessed in that environment.

Limitations include tiny sample size, one topic/product, duplicate control content, caching, same-account history, indexing/deduplication, and public facts/source code that could be found elsewhere. Different canonical URLs and the client loading state remain. Even correct C answers do not establish that the tool executed its script. This study can report a pattern; it cannot establish a universal or isolated causal rendering effect.
