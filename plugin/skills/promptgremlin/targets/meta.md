---
family: meta
kind: family
last_verified: 2026-11-11
sources: [reasoning, glimmer-prompting, llama-prompting]
---
## All models
- Meta has no prompting guide for Muse Wonder, Muse Spark, or Muse Ember; its docs give a reasoning page and a models page. Muse Glimmer has its own prompting page, and Llama 4 has a legacy how-to. Wonder, Spark, and Ember rules below are sourced from the reasoning page or hand-written. (hand-written: no Wonder/Spark/Ember prompting guide; reasoning, glimmer-prompting, llama-prompting)
- Muse Wonder, Muse Spark, and Muse Ember always reason (`reasoning_effort: "none"` returns HTTP 400) and raw reasoning is never returned. If the user wants to see the logic, ask for a short rationale or evidence list inside the answer; the Responses API can add an optional `reasoning.summary`, which may come back empty. (reasoning#How it works, #Constraints, #Reasoning summaries; hand-written for the workaround)
- Reasoning tokens share the output limit with the visible answer, so a cramped limit truncates the answer, worst at `max`. Prompt for a bounded answer and leave headroom in `max_tokens`. (reasoning#Token usage)
- Lookups, formatting, and translation do not need deep reasoning; ask for low effort there and save higher effort for proofs, complex code, trade-off analysis, and planning. (reasoning#When to reach for reasoning)
- Specific role and task beat a generic helper persona, and constraints (format, length, tone) go up front. Skip meta-instructions about how the model works internally. (glimmer-prompting#Effective system prompts; hand-written for applying it to Wonder, Spark, and Ember)
- Legacy Llama 4 (not a lineup model, so no section): explicit instructions beat open-ended ones, and a restrictions list (what to exclude, "say you don't know") sharpens answers. (llama-prompting#Crafting effective prompts, #Restrictions)
- Llama 4, format and chatter: few-shot examples fix format; to get bare JSON or labels combine a role, rules, and one example answer. (llama-prompting#Few-shot prompting, #Limiting extraneous tokens)
- Llama 4, facts and reasoning: paste retrieved facts into the prompt and say to answer only from them; for reasoning, list the steps to follow. Repeated sampling with a majority vote is a pipeline choice. (llama-prompting#Retrieval-augmented generation, #Chain-of-thought prompting, #Self-consistency)
- Llama 4 uses its own chat template; let the serving stack apply it. Its reasoning controls were not fetched. (hand-written)

## Effort
- Wonder, Spark, and Ember API: `reasoning_effort` on Chat Completions, `reasoning.effort` on Responses: `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. Map low, medium, high directly; max to `max` on `muse-wonder-1-0`, `muse-ember-1-0`, or Standard `muse-spark-1-3`, else `xhigh`. Default: `max` on Wonder and Ember, `high` on Spark. (reasoning#How it works)
- Muse Glimmer (self-hosted): `reasoning_strength` argument to `apply_chat_template`: `low`, `medium`, `high` (default), `xhigh`. (glimmer-prompting#Reasoning and chain-of-thought)
- Meta AI app: no control documented. (hand-written)

## muse-wonder-1-0
- Meta's most capable model, in preview: built for hard software engineering and long-horizon agent runs (multi-file repo changes, planning, sub-agent delegation, parallel tool calls, error recovery) and sticks closely to detailed instructions, so a full spec with acceptance criteria pays off. Accepts text, image, video, audio, PDF; context 1,048,576 tokens. (lineup page)
- `max` effort is its default; keep it for work where a correct answer matters more than speed (tracing a concurrency bug, planning a large migration) and lower it elsewhere. Muse Wonder Full lives only in Muse Code; `max` on the API does not select it. (reasoning#Max reasoning on Muse Wonder, #How it works)
- Same request body as Spark and Ember, so switching is just the model id; use those for volume. (lineup page)

## muse-spark-1-3
- Latest Spark and the recommended Spark version: tuned for agentic work (multi-step tool, browser, long-horizon) with better coding than 1.2. Accepts text, image, video, PDF; context 1,048,576 tokens. Prefer it over Wonder when cost or latency matters; hand bulk repeated steps to Ember. (lineup page)
- Supports `max` only on Standard tier, not `-contributor`. Audio input is not fully supported; use 1.2 or Muse Voice Transcribe for audio. (reasoning#How it works; lineup page)

## muse-spark-1-2
- Previous version; same context and modalities, and audio input works. No `max` level. (lineup page; reasoning#How it works)

## muse-spark-1-1
- Original version, Standard tier only; same context and modalities. No `max`; for new work prefer 1.3. (lineup page; reasoning#How it works)

## muse-ember-1-0
- The efficient execution model, Standard mode only: built for bounded work repeated at volume (sub-agent tasks, tool calls, routing, the same job over many images, files, or records). Let Wonder or Spark plan and hand Ember one narrow, self-contained task per request with a fixed output shape. Accepts text, image, video, audio, PDF. (lineup page; hand-written for the task shape)
- Supports `max`, which is also its default, so ask for low effort on routing and classification. Same request body as Spark. (reasoning#How it works; lineup page)

## muse-glimmer
- Open-weight multimodal model distilled from Spark, run on your own hardware; default context 128K. Messages go through the tokenizer's `apply_chat_template`, never hand-built strings. (lineup page; glimmer-prompting#Chat template)
- Supports one tool call per turn, no parallel calls, so write agent prompts that proceed one tool at a time. (glimmer-prompting#Tool calling)
- Sampling `temperature` 1.0, `top_p` 0.95, `top_k` 64, and generous `max_tokens` for long reasoning. (glimmer-prompting#Temperature and sampling, #Common pitfalls)
