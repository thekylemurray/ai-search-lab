---
title: Can AI Systems Retrieve JavaScript-Rendered Content Reliably?
description: Testing whether delivery architecture affects how AI systems retrieve, understand, and cite identical content.
status: Planning
updated: 2026-06-07
tags: ["AI Search", "JavaScript", "Content Architecture", "Technical SEO"]
---

## Question

If identical content exists across different rendering approaches, does delivery architecture change whether AI systems retrieve, understand, or cite it?

## Hypothesis

AI systems will retrieve and cite static HTML more reliably than client-side rendered content.

Expected reliability:

1. Static HTML
2. Server-rendered HTML
3. Client-side rendered JavaScript content

## Method

Create three test pages with identical visible content:

- Static Astro page
- Server-rendered page
- Client-side rendered page

Each page should use the same:

- Title
- Headings
- Body copy
- Metadata
- Internal links
- URL depth
- Topic focus

The only variable should be how the content is delivered.

## Test Variants

| Variant | Rendering Method | Expected AI Accessibility |
|---|---|---|
| Static | HTML available immediately | High |
| Server-rendered | HTML generated before response | High |
| Client-rendered | Content appears after JavaScript runs | Lower |

## Evaluation Criteria

Each page will be tested for:

- Retrieval
- Summary accuracy
- Citation behavior
- Content completeness
- Entity recognition

## Test Prompts

Example prompts:

- Summarize the test page.
- What is the main recommendation on this page?
- What rendering method does this page use?
- Does this page explain AI retrieval reliability?

## Scorecard

| Variant | Retrieved | Correct Summary | Cited | Notes |
|---|---|---|---|---|
| Static HTML | — | — | — | — |
| Pre-rendered HTML | — | — | — | — |
| Client-rendered JS | — | — | — | — |

## Expected Outcome

Static HTML should be easier for AI systems to retrieve, summarize, and cite because the primary content is available immediately in the document.

Client-rendered content may be more fragile because some crawlers and retrieval systems may not execute JavaScript consistently.

## Next Step

Build the three test pages and compare how AI systems retrieve and describe each one.

## Test Pages

- [Static HTML test page](/render-tests/static)
- [Pre-rendered HTML test page](/render-tests/pre-rendered)
- [Client-rendered JavaScript test page](/render-tests/client)