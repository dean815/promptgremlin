---
family: openai
kind: family
last_verified: 2026-10-12
sources: [prompt-engineering, latest-model, chatgpt]
---
## Effort
API: `reasoning.effort` (Responses) or `reasoning_effort` (Chat Completions); Astra and 6.1 Sol reject `none` (use `low`), Luna accepts it; map `minimal` to `low`. Codex: Light (`low`), Medium, High, Extra High. ChatGPT app: write `Effort: <low|medium|high> (ChatGPT app: the model picker's thinking/effort option, pick the nearest; not API reasoning.effort)`, or "not settable here" if the plan has no such option. Don't invent app option names, but still give the line. (latest-model#Update API and model parameters, codex:best-practices#Strong first use, hand-written)

## gpt-6-astra
- Lineup frozen for tests on 2026-10-29.

## gpt-6-1-sol
- Lineup frozen for tests on 2026-10-29.

## gpt-6-luna
- Lineup frozen for tests on 2026-10-29.
