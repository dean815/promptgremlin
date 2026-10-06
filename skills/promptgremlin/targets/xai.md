---
family: xai
kind: family
last_verified: 2026-10-05
sources: [model-pages, reasoning]
---
## All models
- xAI publishes no prompting guide for its text models. The official material is a model page (specs, API notes) and a reasoning page (the effort control), so the craft rules below are hand-written and the parameter rules are sourced. (hand-written: no official guide; model-pages, reasoning)
- Reasoning cannot be turned off, so do not ask for "think step by step" scaffolding or a visible plan. State the goal, constraints, and answer shape and let the model reason on its own. (hand-written; reasoning#The reasoning_effort parameter)
- Put stable material first (role, rules, reference documents, tool descriptions) and the changing question last, so the shared prefix stays identical across requests and cache hits stay reliable. Caching is routed by `prompt_cache_key` on the Responses API, a header or API setting rather than prompt text. (model-pages#Important details)
- Never emit `presence_penalty`, `frequency_penalty`, or `stop` for these reasoning models; the API rejects the request. (reasoning#The reasoning_effort parameter)
- Input is text and images, output is text only, so a prompt can attach images but must not ask for image, audio, or file generation. (model-pages#At a glance)
- Tools available are function calling, web search, X search, and code execution. For agent prompts, say which tool answers which kind of question (web for pages, X search for posts, code execution for calculation) and when memory alone is not acceptable; the knowledge cutoff is May 2026. (model-pages#At a glance; hand-written for the routing advice)
- For long agent loops, tell the model what must be kept when history is compacted (open tasks, decisions, file paths). Compaction itself is an API feature, not prompt text. (model-pages#Important details; hand-written for the keep-list)
- Multi-turn reasoning continuity is code: pass the returned reasoning items back unchanged on the Responses API. Do not paste reasoning into the prompt. (model-pages#Important details)

## Effort
- API: `reasoning_effort` (top level on SDK and Chat Completions calls) or `reasoning.effort` (Responses API), values `"low"`, `"medium"`, `"high"` (default), `"xhigh"`. Map low to `"low"`, medium to `"medium"`, high to `"high"`, max to `"xhigh"`. Low suits latency-sensitive agent loops and simple tool calls; medium suits data analysis and long-context work; xhigh is for the hardest problems when latency does not matter. (reasoning#Effort levels, #Summary table)
- Grok apps and Grok Bot: no effort control is documented; use a plain "take your time" line. (hand-written)

## grok-4-7
- Current recommended model, API name `grok-4.7`: 500,000-token context, May 2026 cutoff, reasoning always on at any effort. (model-pages#At a glance)
- A "Fast" variant is the same model on faster infrastructure, available only inside Cursor and Grok Build, not the public API. Prompts do not change. (model-pages#Fast variant)
- A reasoning summary can be streamed, but raw reasoning cannot, so do not write prompts that depend on quoting its own reasoning. (reasoning#Summarized Reasoning Content; hand-written for the consequence)
