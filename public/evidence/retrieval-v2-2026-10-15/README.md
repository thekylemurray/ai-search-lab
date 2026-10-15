# Evidence provenance

`runs.json` transcribes the nine responses supplied by the operator. Markdown emphasis and link formatting are normalized; answer wording, labels and cited destinations are retained. These are not raw provider exports. Run 01 contained a duplicate paste of the same answer: `paste_occurrences: 2` preserves that fact while the record counts as one run.

`preflights.json` contains labeled summaries of the two unsuccessful Astra and three Gemini preflights, excluded from scored-run totals. Gemini preflight A's trailing pipe in the cited link remains unresolved. No preflight C was supplied for Astra after both controls failed.

Assigned prompts come from the prepared guide; the actual prompts submitted in Gemini were not independently captured. Reporting timestamps are not execution timestamps. Fresh chats, unchanged model/mode and memory settings are unconfirmed. All nine access-evidence fields are unverified because responses and URLs alone do not establish retrieval.

The C answers contain six unavailable items, not six incorrect factual assertions. We leave factual accuracy NA, and separately report unavailable-item counts. A/B scores measure factual agreement with the known fixture, not retrieval verification. Citing a requested URL does not establish that a page was fetched.

The operator confirmed in this conversation that C displayed its six details in a regular browser. Browser/version, console observations and independently captured screenshot evidence were not supplied.
