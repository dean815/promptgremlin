---
family: qwen
kind: family
last_verified: 2026-10-12
sources: [prompt-guide, open-weights-card]
---
## Effort
- Documented for Qwen3.8 open weights (card): `reasoning_effort` `xhigh` (default), `medium`, `low`. Map low to `low`, medium to `medium`, high and max to `xhigh`; there is no `high` value. Thinking is on by default; on Qwen Cloud switch it off with `"enable_thinking": false` (self-hosted servers nest it in `chat_template_kwargs`). (open-weights-card#API Usage)
- Do not default agents to `low`; retries can lengthen multi-turn runs. (open-weights-card#API Usage)
- Whether the API models accept these values is (unverified); read only from the card. Chat app: none documented. (hand-written)

## qwen3-8-max
- Lineup frozen for tests on 2026-10-29.

## qwen3-7-plus
- Lineup frozen for tests on 2026-10-29.

## qwen3-8-flash
- Lineup frozen for tests on 2026-10-29.
