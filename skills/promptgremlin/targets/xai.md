---
family: xai
kind: family
last_verified: 2026-10-12
sources: [model-pages, reasoning]
---
## All models
- xAI publishes no prompting guide for its text models. The official material is a model page (specs, API notes) and a reasoning page (the effort control), so the craft rules below are hand-written and the parameter rules are sourced. (hand-written: no official guide; model-pages, reasoning)
- Reasoning is always on and cannot be disabled; the model already works through problems before answering. Skip "think step by step" scaffolding and visible-plan requests; state the goal, constraints, and answer shape instead. (reasoning#Key Features, #The `reasoning_effort` parameter; hand-written for the advice)
- Put stable material first (role, rules, reference documents, tool descriptions) and the changing question last, so the shared prefix stays identical across requests. Cache routing is an API setting, not prompt text: `prompt_cache_key` on the Responses API, the `x-grok-conv-id` header on Chat Completions. (model-pages#Important details)
- Never emit `presence_penalty`, `frequency_penalty`, or `stop` for these reasoning models; the API returns an error. (reasoning#The `reasoning_effort` parameter)
- Input is text and images, output is text only, so a prompt can attach images but must not ask for image, audio, or file generation. (model-pages#At a glance)
- Tools available are function calling, web search, X search, and code execution. For agent prompts, say which tool answers which kind of question (web for pages, X search for posts, code execution for calculation) and when memory alone is not acceptable; the knowledge cutoff is May 2026. (model-pages#At a glance; hand-written for the routing advice)
- For long agent loops, tell the model what must be kept when history is compacted (open tasks, decisions, file paths). Compaction itself is an API feature, not prompt text. (model-pages#Important details; hand-written for the keep-list)
- Multi-turn reasoning continuity is code, not prompt text: on the Responses API, return the reasoning items (with their encrypted content) unchanged in the next request. Never paste or restate earlier reasoning in the prompt. (model-pages#Important details; reasoning#Encrypted Reasoning Content)

## Effort
- API: `reasoning.effort` (Responses API) or `reasoning_effort` (xAI SDK), values `"low"`, `"medium"`, `"high"` (default), `"xhigh"`; it cannot turn reasoning off. Map max to `"xhigh"` (grok-4.6 and later; older models treat it as `"high"`). Low suits fast agent loops and simple tool calls, medium data analysis and long context, xhigh the hardest problems when latency does not matter. (reasoning#Effort levels, #Summary table)
- Grok apps and Grok Bot: no effort control is documented; use a plain "take your time" line. (hand-written)

## grok-4-7
- Current recommended model, API name `grok-4.7`: 500,000-token context, May 2026 cutoff, no text output limit, reasoning always on at any effort. The model page lists only the Responses API for it. (model-pages#At a glance, #Using the API)
- A "Fast" variant is the same model on faster infrastructure, available only inside Cursor and Grok Build, not the public API. Prompts do not change. (model-pages#Fast variant)
- Encrypted reasoning returns on every Responses API reply without being requested, but only a summary of the reasoning can be streamed, so do not write prompts that depend on quoting its own reasoning. (model-pages#Important details; reasoning#Summarized Reasoning Content; hand-written for the consequence)
