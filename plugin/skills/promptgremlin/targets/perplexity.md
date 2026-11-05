---
family: perplexity
kind: tool
last_verified: 2026-10-01
sources: [agent-prompt-guide, prompt-the-agent]
---
## All models
- The only fetchable official guide covers the Agent API, not the Perplexity web or app search box. For the API, write two fields; for the app, only the `input`-style question applies. (agent-prompt-guide#Instructions; hand-written: app scope)
- `input` is what gets searched. Make it specific: name entities, time range, and the unit of the answer, and use the vocabulary that would appear on the relevant pages. Add a few disambiguating words when a term has several meanings. (prompt-the-agent#Ground the run, agent-prompt-guide#Best Practices)
- `instructions` is the system prompt, re-read on every loop step: role, tone, output language, citation and formatting rules, grounding rules. Test: if a rule should hold even for an unrelated question, it goes in `instructions`; if it concerns this request, it goes in `input`. (prompt-the-agent#`instructions` vs `input`)
- Keep `instructions` short, since its cost repeats per step. With a `preset` set, `instructions` replaces the preset's tuned prompt rather than extending it, so omit it unless app-specific behaviour is needed. (agent-prompt-guide#Instructions)
- Do not explain `web_search` or `fetch_url` or tell it when to search. Those built-in tools work without coaching; control step count with `max_steps`. (agent-prompt-guide#Instructions)
- Hard constraints (allowed domains, dates, region) belong in the `web_search` filter parameters, not prose in `input`; parameters are enforced, prose may not survive every loop step. Structured output goes in `response_format`. These are request fields, not prompt text. (agent-prompt-guide#Use Parameters, Not Prose, for Hard Constraints)
- Give list requests a count ("top 5"). Without a cap the length is arbitrary. (agent-prompt-guide#Best Practices)
- Citations: ask in `instructions` for a citation style such as inline by domain, not for full URLs in the answer. Models can mistype URLs, so the user's code should read sources from the structured `search_results` items. (agent-prompt-guide#Reading Sources from the Response)
- Add grounding lines to `instructions`: say so explicitly when searches return nothing relevant after rephrasing, and disclose partial matches (an adjacent period, a related entity, a lookalike product) up front before answering. (agent-prompt-guide#Reduce Hallucinations)
