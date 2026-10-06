---
family: deepseek
kind: family
last_verified: 2026-10-01
sources: [thinking-mode]
---
## All models
- DeepSeek publishes no prompting guide. The official material is the thinking-mode page (parameters and multi-turn rules) and the model and pricing page, so the craft rules here are hand-written and the parameter rules are sourced. (hand-written: no official guide; thinking-mode)
- Thinking is on by default. In thinking mode `temperature`, `presence_penalty`, and `frequency_penalty` are accepted but ignored, and `top_p` is clamped to 0.95 to 1.0, so do not promise creativity or determinism through sampling; shape it in the prompt. (thinking-mode#Input and Output Parameters)
- With thinking on, skip chain-of-thought scaffolding and "reason step by step" lines. Give the goal, constraints, success test, and answer format. (hand-written)
- Both models take 1M tokens of context and up to 384K output. Both support JSON output and tool calls. (lineup page)
- Thinking mode can run several reason-then-call rounds before answering. In agent prompts, describe each tool by when to use it and what it returns, and say when to stop calling and answer. (thinking-mode#Tool Calls; hand-written for the prompt advice)
- When a request carries tools, every earlier turn's `reasoning_content` must be sent back or the API returns 400; without tools it is ignored. This is client code, not prompt text. (thinking-mode#Tool Calls)
- FIM completion and chat-prefix completion are beta and non-thinking only. They are completion modes, not instruction prompts; flag that if the user wants them. (lineup page)
- For output that code will parse, ask for JSON explicitly in the prompt and name the keys. (hand-written; lineup page confirms JSON output)

## Effort
- API (OpenAI format): `reasoning_effort` `"low"`, `"high"`, `"max"` plus thinking toggle `{"thinking": {"type": "enabled"}}`, sent in `extra_body` with the OpenAI SDK. Default is enabled at `high`. Other requested names are remapped by the API (medium to high, ultra to max); send low to `low`, medium and high to `high`, max to `max`. Anthropic format uses `output_config.effort`. The Responses API toggle (`reasoning.effort`, `none` disables) is (unverified): the source table is flattened. (thinking-mode#Thinking Mode Toggle and Effort Control)
- Chat app: no control documented. (hand-written)

## deepseek-v4-pro
- Flagship (V4-Pro-0813); text input only, no vision, and pricier than Flash. Use for the hard reasoning and agent jobs and write the fuller prompt for it. (lineup page; hand-written for the guidance)
- Supports thinking and non-thinking; thinking is the default. (lineup page)

## deepseek-flash
- Fast, low-cost model (V4.1-Flash); image input is supported. The older `deepseek-v4-flash` names still resolve to it. Keep prompts short and single-purpose. (lineup page; hand-written for the prompt advice)
- Supports thinking and non-thinking; thinking is the default. For simple extraction or formatting, request `low` effort. (lineup page; hand-written)
