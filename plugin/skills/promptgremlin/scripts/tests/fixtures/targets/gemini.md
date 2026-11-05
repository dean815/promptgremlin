---
family: gemini
kind: family
last_verified: 2026-10-12
sources: [prompting-strategies, latest-model, whats-new-3-5, thinking]
---
## Effort
- API: `thinking_level`, values `minimal`, `low`, `medium`, `high`. Map low to `low`, medium to `medium`, high and max to `high`. Defaults: `medium` on 3.8 and 3.6 Flash, `minimal` on 3.5 Flash-Lite, `high` on 3.1 Pro and 3 Flash Preview. Per-model levels are in each section. (thinking#Controlling thinking)
- To save tokens, lower the level rather than setting a small `max_output_tokens`, which truncates mid-thought. (thinking#Token limits and `max_output_tokens`)
- Gemini app: no source documents a thinking control; use a plain "think hard" line when needed. (hand-written)

## gemini-3-8-flash
- Lineup frozen for tests on 2026-10-29.

## gemini-3-6-flash
- Lineup frozen for tests on 2026-10-29.

## gemini-3-5-flash-lite
- Lineup frozen for tests on 2026-10-29.

## gemini-3-1-flash-lite
- Lineup frozen for tests on 2026-10-29.

## gemini-3-1-pro-preview
- Lineup frozen for tests on 2026-10-29.

## gemini-3-flash-preview
- Lineup frozen for tests on 2026-10-29.
