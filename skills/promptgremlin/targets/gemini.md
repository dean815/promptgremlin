---
family: gemini
kind: family
last_verified: 2026-10-01
sources: [prompting-strategies, latest-model, whats-new-3-5, thinking]
---
## All models
- Be brief and direct. Gemini 3.x reasons internally, and long persuasive or elaborate prompt machinery written for older models can make it over-analyze. State the goal, constraints, and output shape once. (whats-new-3-5#Prompting best practices, prompting-strategies#Core prompting principles)
- Pick one delimiter style per prompt, XML-style tags or Markdown headings, and do not mix them. Define any ambiguous term or parameter where it first appears. (prompting-strategies#Core prompting principles)
- Put role, hard constraints, and output format in the system instruction, or at the very top of a user prompt. With big context (documents, code, transcripts), paste the context first, then the question last, opened by a bridge such as "Based on the information above". (prompting-strategies#Core prompting principles)
- Default answers are terse. If the user wants a chatty, detailed, or tutorial-style reply, say so in the prompt. (prompting-strategies#Core prompting principles, whats-new-3-5#Prompting best practices)
- Do not script chain-of-thought ("first plan, then reason step by step in your answer"); the model already thinks internally. For hard problems, one plain line asking it to think hard is enough, and the real lever is the thinking level. (prompting-strategies#Enhancing reasoning and planning, whats-new-3-5#Migrate from Gemini 2.5)
- Treat text, images, audio, and video as equal inputs; name each one in the instructions that concern it. (prompting-strategies#Core prompting principles)
- For agent prompts, decide and write down: how far to plan before acting, whether to follow the plan or pivot on new evidence, how many retries on errors, what counts as a risky write versus a harmless read, when to ask instead of assume, and how chatty to be between tool calls. (prompting-strategies#Agentic workflows)
- If the model over-calls tools, drop the thinking level first; only then add a system instruction capping the number of tool calls. (whats-new-3-5#Reducing unnecessary tool calls)
- Settings go beside the prompt, not in it. Do not emit `temperature`, `top_p`, `top_k`, or `candidate_count` for 3.x; use `thinking_level`, never `thinking_budget`, and never both. For repeatable output, write explicit rules into the system instruction. (whats-new-3-5#Parameter updates and best practices in Gemini 3.x, #Migrate from Gemini 2.5)
- Tool results: extra instructions for the model go at the end of the function response text, after two line breaks, not as separate parts. (whats-new-3-5#Inline instructions in function responses)

## Effort
- API: `thinking_level` in the generation config, string values `minimal`, `low`, `medium`, `high`. Map low to `low`, medium to `medium`, high and max to `high`. Default is `medium` on 3.8, 3.7, 3.6 and 3.5 Flash, `minimal` on the Flash-Lite models, `high` on 3.1 Pro and 3 Flash Preview. Which levels each model accepts is in its section. (thinking#Controlling thinking, whats-new-3-5#New default effort level)
- Gemini app: no source documents a thinking control there; leave it out and use a plain "think hard" line in the prompt when needed. (hand-written)

## gemini-3-8-flash
- Flagship, tuned for long software-engineering, agent, and enterprise work. Levels: `low`, `medium` (default), `high`. `minimal` returns an error; never emit it. (latest-model#Understanding reasoning levels)
- It spends more tokens on long tasks by design (small reasoning steps, iterative tool calls, self-checking); for everyday tasks, lower the effort to cut token use. (latest-model#What's new in Gemini 3.8 Flash)

## gemini-3-7-flash
- Levels: `low`, `medium` (default), `high`; no `minimal`. (thinking#Controlling thinking)
- Otherwise follow All models; the sources add nothing model-specific. (hand-written: no 3.7-specific guidance)

## gemini-3-6-flash
- Levels: `minimal`, `low`, `medium` (default), `high`. (thinking#Controlling thinking)
- Otherwise follow All models; the sources add nothing model-specific. (hand-written: no 3.6-specific guidance)

## gemini-3-5-flash
- GA, built for agentic and coding loops. Levels: `minimal` to `high`, default `medium`; `low` is strong for short code or agent tasks. (whats-new-3-5#What's new, #New default effort level)
- Reasoning carries across turns on its own; in stateless calls the full history, thought signatures included, must be sent back. That is a code concern, not prompt text. (whats-new-3-5#Thought preservation)

## gemini-3-5-flash-lite
- Defaults to `minimal` thinking; levels `minimal` to `high`. For anything needing analysis, ask for `medium` or `high` in the settings line. (thinking#Controlling thinking)
- Keep the prompt short and single-purpose. (hand-written: inferred from Lite positioning)

## gemini-3-1-flash-lite
- Stable low-cost model for high-volume, simple tasks. Defaults to `minimal`; all four levels work. Do not hand it multi-step reasoning jobs; route those to a bigger Flash. (whats-new-3-5#Choosing the right Flash model, #Controlling thinking)

## gemini-3-1-pro-preview
- Preview. Defaults to `high`; accepts `low`, `medium`, `high`, and `minimal` is not supported. (thinking#Controlling thinking, whats-new-3-5#thinking levels table)
- For simple asks, set `low` rather than letting it think at the default. (hand-written)

## gemini-3-flash-preview
- Preview, superseded by 3.5 Flash for GA use. Defaults to `high`; all four levels. (whats-new-3-5#Choosing the right Flash model, thinking#Controlling thinking)
- Sources give "Gemini 3 Flash" two system-instruction habits: for time-sensitive questions, tell it to trust the supplied current date and year; for answers that must come only from supplied material, tell it to use nothing else and say when the answer is absent. (prompting-strategies#Gemini 3 Flash strategies)
