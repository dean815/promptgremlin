---
family: gemini
kind: family
last_verified: 2026-11-11
sources: [prompting-strategies, latest-model, whats-new-4, whats-new-3-8, whats-new-3-5, thinking]
---
## All models
- Be brief and direct. Gemini 3.x and 4 reason internally, and long persuasive or elaborate prompt machinery written for older models can make them over-analyze. State the goal, constraints, and output shape once. (whats-new-3-5#Prompting best practices, prompting-strategies#Core prompting principles)
- Pick one delimiter style per prompt, XML-style tags or Markdown headings, and do not mix them. Define any ambiguous term or parameter where it first appears. (prompting-strategies#Core prompting principles)
- Put role, hard constraints, and output format in the system instruction, or at the very top of a user prompt. With big context (documents, code, transcripts), paste the context first, then the question last, opened by a bridge such as "Based on the information above". (prompting-strategies#Core prompting principles)
- Default answers are terse. If the user wants a chatty, detailed, or tutorial-style reply, say so in the prompt. (prompting-strategies#Core prompting principles, whats-new-3-5#Prompting best practices)
- Do not script chain-of-thought or ask it to show its plan in the answer; it already thinks internally. For hard problems one plain line asking it to think hard is enough, and the real lever is the thinking level. (prompting-strategies#Enhancing reasoning and planning)
- Treat text, images, audio, and video as equal inputs; name each one in the instructions that concern it. (prompting-strategies#Core prompting principles)
- For agent prompts, decide and write down: how deeply to analyze before acting, whether to follow the plan or pivot on new evidence, how hard to retry on errors, what counts as a risky write versus a harmless read, when to ask instead of assume, how chatty to be between tool calls, and how exact the final output must be. (prompting-strategies#Agentic workflows)
- If the model over-calls tools, drop the thinking level first; only then add a system instruction capping the number of tool calls. (whats-new-3-5#Reducing unnecessary tool calls)
- Settings go beside the prompt, not in it. Do not emit `temperature`, `top_p`, `top_k`, or `candidate_count` for 3.x or 4; use `thinking_level`, never `thinking_budget`, and never both. For repeatable output, write explicit rules into the system instruction. Do not prefill the model's turn. (whats-new-3-5#Parameter updates and best practices in Gemini 3.x, whats-new-4#Migrate from Gemini 3 and earlier, prompting-strategies#Experiment with model parameters; hand-written: `candidate_count`, prefill)
- Tool results: extra instructions for the model go at the end of the function response text, after two line breaks, not as separate parts. (whats-new-3-5#Inline instructions in function responses)

## Effort
- API: `thinking_level`, values `minimal`, `low`, `medium`, `high`. Map low to `low`, medium to `medium`, high and max to `high`. Defaults: `medium` on Gemini 4 and 3.8/3.6 Flash, `minimal` on Flash-Lite, `high` on 3.1 Pro and 3 Flash Preview. Per-model levels are in each section. (thinking#Controlling thinking)
- To save tokens, lower the level rather than setting a small `max_output_tokens`, which truncates mid-thought. (thinking#Token limits and `max_output_tokens`)
- Gemini app: no source documents a thinking control; use a plain "think hard" line when needed. (hand-written)

## gemini-4-carbon
- Flagship and deepest reasoner: more thinking per turn to explore and self-check, so slower and costlier than Argon. Pick it for root-cause debugging, architecture, dense multimodal synthesis, proofs, and security audits. (whats-new-4#Choosing between Carbon, Argon, and other models)
- Levels: `low`, `medium` (default), `high`; no `minimal`. `low` for simple or cost-sensitive work, `high` for hard math, science, and the toughest code. (whats-new-4#Understanding thinking levels)
- `max_output_tokens` caps thinking plus answer: leave it unset or at 32,768+. Answers over 64K tokens need `background: true` and a higher cap. (whats-new-4#Larger output and long decode)
- No watched page has Gemini 4 prompt advice; All models rules are assumed to apply (unverified). (hand-written)

## gemini-4-argon
- The efficient Gemini 4 model: same context window, tools, and thinking levels as Carbon, with faster replies and fewer thinking tokens per turn. Use it for interactive coding, day-to-day feature work, and fast production loops; move to Carbon when depth matters more than speed. (whats-new-4#Choosing between Carbon, Argon, and other models)
- Levels: `low`, `medium` (default), `high`; no `minimal`. Level and output-limit advice is the same as Carbon's. (thinking#Controlling thinking; hand-written: Argon guide, not watched)

## gemini-3-8-flash
- The default general-purpose model, tuned for long software-engineering, agent, and enterprise work. Levels: `low`, `medium` (default), `high`. `minimal` is not supported; never emit it. (latest-model#Latest models across modalities, thinking#Controlling thinking)
- Use `low` for latency-bound jobs such as drafts, live chat, or quick analysis; `medium` for complex code and agents; `high` for math and hard multi-step reasoning. (whats-new-3-8#Understanding reasoning levels)
- It spends more tokens on long tasks by design (small reasoning steps, iterative tool calls, self-checking); for everyday tasks lower the effort, or use 3.6 Flash. (whats-new-3-8#What's new in Gemini 3.8 Flash)

## gemini-3-6-flash
- Levels: `minimal`, `low`, `medium` (default), `high`. (thinking#Controlling thinking)
- The direct replacement for 3.5 Flash, with lower token use; the old 3.5 Flash id routes here. Prompts written for 3.5 Flash carry over. (whats-new-3-5#Model overview, #Choosing the right Flash model)
- Level guide: `minimal` for chat and quick facts, `low` for short code or agent tasks and light analysis, `medium` for complex code and agents, `high` for the hardest problems. (whats-new-3-5#New default effort level: `medium`)

## gemini-3-5-flash-lite
- For low-cost, high-volume work that does not need full Flash reasoning depth. (whats-new-3-5#Choosing the right Flash model)
- Defaults to `minimal`; accepts all four levels. For anything needing analysis, ask for `medium` or `high` in the settings line. (thinking#Controlling thinking)
- Keep the prompt short and single-purpose. (hand-written: inferred from Lite positioning)

## gemini-3-1-flash-lite
- Low-cost model for high-volume, simple tasks. Do not hand it multi-step reasoning jobs; route those to a full Flash model. (whats-new-3-5#Choosing the right Flash model)
- Defaults to `minimal`; accepts all four levels. (thinking#Controlling thinking)

## gemini-3-1-pro-preview
- Preview. Defaults to `high`; accepts `low`, `medium`, `high`; `minimal` is not supported. (thinking#Controlling thinking)
- For simple lookups or classification, set `low` rather than paying for default-level thinking. (thinking#Best practices)

## gemini-3-flash-preview
- Preview; for new GA work the sources point to 3.8 or 3.6 Flash. Defaults to `high`; all four levels. (whats-new-3-5#Choosing the right Flash model, thinking#Controlling thinking)
- Sources give "Gemini 3 Flash" three system-instruction habits: tell it to trust the supplied current date and year for time-sensitive searches; state its knowledge cutoff (January 2025); and for answers that must come only from supplied material, tell it to use nothing else and say when the answer is absent. (prompting-strategies#Gemini 3 Flash strategies)
