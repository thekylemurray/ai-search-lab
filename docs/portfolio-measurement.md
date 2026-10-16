# Portfolio measurement

Implementation date: 2026-10-16 UTC. Property: G-M2J2LQWKYX.
Status: implementation prepared; production receipt and GA4 configuration pending.

## Questions and events

| Question | Event | Parameters | Limit |
| --- | --- | --- | --- |
| Which project pages are visited? | page_view | page_path, project_id on five mapped project pages | A view does not prove reading; web-ops counts the whole page |
| Where do visitors open the résumé? | resume_click | page_path, resource_id=public_resume | Click, not a completed download or reading |
| Where do visitors initiate email contact? | contact_click | page_path, contact_method=email | Click, not a sent message |
| Where do visitors open LinkedIn? | linkedin_click | page_path, contact_method=linkedin | Click, not a connection |

Each consenting document load sends one explicit page_view; automatic initial page views are disabled. No SPA router is installed. Only the production hostname is eligible. Rendering fixtures are excluded. Consent is opt-in, remembered locally, and can be withdrawn. No Google script is requested before acceptance. No tracking prevents link navigation. Query strings/fragments are removed from configured page locations, and referrers are reduced to their origin. Custom click parameters are fixed labels, never mailto destinations or form values.

## Required GA4 setup before merge

In Admin → Data streams → this web stream, turn Enhanced measurement OFF. This implementation owns page views and the three click events; enhanced downloads/outbound/form/history events would add overlapping measurements and can collect additional URL information. Do not install a second Google tag or GTM container.

Create event-scoped custom dimensions for project_id, resource_id and contact_method if you want them in standard explorations. Page path is also available through GA4's built-in page dimensions. Keep Google signals and advertising features disabled. No key events are required for this initial validation.

## Production validation after deployment

1. In a fresh browser session, visit the production homepage. Verify no gtag/js or Google Analytics collection requests before consent. Decline and verify again.
2. Reopen Analytics preferences and allow. Check the network panel for one page_view, with this measurement ID. Check GA4 Realtime for receipt.
3. For DebugView, append ?analytics_debug=1 to the page being tested. This opts only that document into debug mode; it is not persisted across navigation. Visit each of the five mapped project pages and inspect page_view/project_id.
4. Test résumé, email, and LinkedIn once each. Confirm resume_click, contact_click and linkedin_click, their source page, and fixed labels in DebugView. Cancel the email composer; no message needs to be sent.
5. Test a nested element inside a link and keyboard activation. Confirm one event per activation and normal navigation.
6. Visit a rendering fixture and a deployment preview: no Google script should load. Withdraw consent and confirm subsequent page loads/clicks do not collect.
7. Record date, browser, deployed commit, event counts and screenshots from DebugView. Keep test observations separate from organic usage. Do not claim GA4 receipt based only on local queue tests.

## Evidence boundary

Automated checks can establish command generation, event classification, consent gating, production-host gating and generated-page wiring. They cannot establish delivery to Google, account configuration, real visitor behavior, hiring outcomes, or conversion lift. The portfolio case study should be published as verified only after the production steps above are recorded.

References: https://developers.google.com/analytics/devguides/collection/ga4/events
