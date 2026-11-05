---
family: mistral
kind: family
last_verified: 2026-10-06
sources: [prompting, reasoning]
---
## Effort
- API: `reasoning_effort` on chat completions (and inside `completion_args` on the Agents and Conversations endpoints). Documented values are `"high"` (full thinking chunk, so `message.content` becomes a list of thinking and text chunks) and `"none"` (minimal thinking, no chunk, plain string). Map low to `"none"`, high and max to `"high"`; medium has no documented value (unverified). Third-party `zai-glm-5-3` on Mistral's API: `low`/`high`/`max`, never `none`; always a chunk list. (reasoning#Model, #Handling thinking chunks)
- Le Chat and other apps: no control documented. (hand-written)

## mistral-large-4
- Lineup frozen for tests on 2026-10-29.

## mistral-medium-3-5
- Lineup frozen for tests on 2026-10-29.

## mistral-small-4
- Lineup frozen for tests on 2026-10-29.

## mistral-large-3
- Lineup frozen for tests on 2026-10-29.
