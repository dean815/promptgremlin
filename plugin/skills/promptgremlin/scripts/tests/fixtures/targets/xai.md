---
family: xai
kind: family
last_verified: 2026-10-12
sources: [model-pages, reasoning]
---
## Effort
- API: `reasoning.effort` (Responses API) or `reasoning_effort` (xAI SDK), values `"low"`, `"medium"`, `"high"` (default), `"xhigh"`; it cannot turn reasoning off. Map max to `"xhigh"` (grok-4.6 and later; older models treat it as `"high"`). Low suits fast agent loops and simple tool calls, medium data analysis and long context, xhigh the hardest problems when latency does not matter. (reasoning#Effort levels, #Summary table)
- Grok apps and Grok Bot: no effort control is documented; use a plain "take your time" line. (hand-written)

## grok-4-7
- Lineup frozen for tests on 2026-10-29.
