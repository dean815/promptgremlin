---
family: deepseek
kind: family
last_verified: 2026-10-01
sources: [thinking-mode]
---
## Effort
- API (OpenAI format): `reasoning_effort` `"low"`, `"high"`, `"max"` plus thinking toggle `{"thinking": {"type": "enabled"}}`, sent in `extra_body` with the OpenAI SDK. Default is enabled at `high`. Other requested names are remapped by the API (medium to high, ultra to max); send low to `low`, medium and high to `high`, max to `max`. Anthropic format uses `output_config.effort`. The Responses API toggle (`reasoning.effort`, `none` disables) is (unverified): the source table is flattened. (thinking-mode#Thinking Mode Toggle and Effort Control)
- Chat app: no control documented. (hand-written)

## deepseek-v4-pro
- Lineup frozen for tests on 2026-10-29.

## deepseek-flash
- Lineup frozen for tests on 2026-10-29.
