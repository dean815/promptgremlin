---
family: meta
kind: family
last_verified: 2026-10-12
sources: [reasoning, glimmer-prompting, llama-prompting]
---
## Effort
- Wonder and Spark API: `reasoning_effort` on Chat Completions, `reasoning.effort` on Responses: `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. Map low to `low`, medium to `medium`, high to `high`, max to `max` on `muse-wonder-1-0` or `muse-spark-1-3` Standard tier, otherwise `xhigh`. If omitted, it still reasons at its own depth. (reasoning#How it works)
- Muse Glimmer (self-hosted): `reasoning_strength` argument to `apply_chat_template`: `low`, `medium`, `high` (default), `xhigh`. (glimmer-prompting#Reasoning and chain-of-thought)
- Meta AI app: no control documented. (hand-written)

## muse-wonder-1-0
- Lineup frozen for tests on 2026-10-29.

## muse-spark-1-3
- Lineup frozen for tests on 2026-10-29.

## muse-spark-1-2
- Lineup frozen for tests on 2026-10-29.

## muse-spark-1-1
- Lineup frozen for tests on 2026-10-29.

## muse-glimmer
- Lineup frozen for tests on 2026-10-29.
