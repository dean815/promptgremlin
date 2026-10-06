---
family: meta
kind: family
last_verified: 2026-10-06
sources: [reasoning, glimmer-prompting, llama-prompting]
---
## All models
- Meta has no prompting guide for Muse Spark; its docs give a reasoning page and a models page. Muse Glimmer has its own prompting page, and Llama 4 has a legacy how-to. Spark rules below are sourced from the reasoning page or hand-written. (hand-written: no Spark prompting guide; reasoning, glimmer-prompting, llama-prompting)
- Muse Spark always reasons (`reasoning_effort: "none"` returns HTTP 400) and its raw reasoning is never returned. If the user wants to see the logic, ask for a short rationale or evidence list inside the answer. (reasoning#How it works, #Constraints; hand-written for the workaround)
- Reasoning tokens share the output limit with the visible answer, so a cramped limit truncates the answer. Prompt for a bounded answer and leave headroom in `max_tokens`. (reasoning#Token usage)
- Lookups, formatting, and translation do not need deep reasoning; ask for low effort there and save high for proofs, complex code, trade-off analysis, and planning. (reasoning#When to reach for reasoning)
- Specific role and task beat a generic helper persona, and constraints (format, length, tone) go up front. Skip meta-instructions about how the model works internally. (glimmer-prompting#Effective system prompts; hand-written for applying it to Spark)
- Legacy Llama 4 (not a lineup model, so no section): explicit instructions beat open-ended ones, and a restrictions list (what to exclude, "say you don't know") sharpens answers. (llama-prompting#Crafting effective prompts, #Restrictions)
- Llama 4, format and chatter: few-shot examples fix format; to get bare JSON or labels combine a role, rules, and one example answer. (llama-prompting#Few-shot prompting, #Limiting extraneous tokens)
- Llama 4, facts and reasoning: paste retrieved facts into the prompt and say to answer only from them; for reasoning, list the steps to follow. Repeated sampling with a majority vote is a pipeline choice. (llama-prompting#Retrieval-augmented generation, #Chain-of-thought prompting, #Self-consistency)
- Llama 4 uses its own chat template; let the serving stack apply it. Its reasoning controls were not fetched. (hand-written)

## Effort
- Muse Spark API: `reasoning_effort` on Chat Completions, `reasoning.effort` on the Responses API: `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. Map low to `low`, medium to `medium`, high to `high`, max to `max` on `muse-spark-1-3` Standard tier, otherwise `xhigh`. Omitted, it still reasons at a model-chosen depth. (reasoning#How it works)
- Muse Glimmer (self-hosted): `reasoning_strength` argument to `apply_chat_template`: `low`, `medium`, `high` (default), `xhigh`. (glimmer-prompting#Reasoning and chain-of-thought)
- Meta AI app: no control documented. (hand-written)

## muse-spark-1-3
- Latest and recommended: tuned for agentic work (multi-step tool, browser, long-horizon) with better coding than 1.2. Accepts text, image, video, PDF; context 1,048,576 tokens. (lineup page)
- Only version with `max`, and only on Standard tier, not `-contributor`. Audio input is not fully supported; use 1.2 or Muse Voice Transcribe for audio. (reasoning#How it works; lineup page)

## muse-spark-1-2
- Previous version; same context and modalities, and audio input works. No `max` level. (lineup page; reasoning#How it works)

## muse-spark-1-1
- Original version, Standard tier only; same context and modalities. No `max`; for new work prefer 1.3. (lineup page; reasoning#How it works)

## muse-glimmer
- Open-weight multimodal model distilled from Spark, run on your own hardware; default context 128K. Messages go through the tokenizer's `apply_chat_template`, never hand-built strings. (lineup page; glimmer-prompting#Chat template)
- Supports one tool call per turn, no parallel calls, so write agent prompts that proceed one tool at a time. (glimmer-prompting#Tool calling)
- Sampling `temperature` 1.0, `top_p` 0.95, `top_k` 64, and generous `max_tokens` for long reasoning. (glimmer-prompting#Temperature and sampling, #Common pitfalls)
