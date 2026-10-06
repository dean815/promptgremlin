---
family: openai
kind: family
last_verified: 2026-10-01
sources: [prompt-engineering, latest-model, chatgpt]
---
## All models
- GPT models want precise instructions that hand over the logic and data needed, so state the task, output shape, and constraints outright; don't count on inference. (prompt-engineering#Prompting current models)
- Lay the prompt out as identity, instructions, examples, then context, with Markdown headers for sections and XML tags around pasted documents. Reference data goes near the end. (prompt-engineering#Message formatting with Markdown and XML)
- For few-shot, give diverse inputs paired with the exact desired outputs. (prompt-engineering#Few-shot learning)
- In API use, durable rules belong in `instructions` or a developer message; they outrank `input`. (prompt-engineering#Message roles and instruction following)
- It asks before acting when intent is vague, and may stop at a plan or "yes, I can". When the user wants the work done, the prompt should say to infer intent from context, treat request-style phrasing as an instruction, and run to a finished result; prepare everything it already may do, so the user's only step left is approving the finished result. (latest-model#Initiative and follow-through)
- List which actions need no sign-off and which are destructive or irreversible and must stop. Say not to add warnings, disclaimers, or approval steps for risks that are only hypothetical. (latest-model#Initiative and follow-through)
- It's more sensitive to AGENTS.md and skill files: say the user's instructions outrank them, and tell it to name the file when one makes it pause. (latest-model#Instruction following)
- It defaults to lists, tables, and Markdown, with recurring stock phrases. Specify prose or structure, and name the phrases to avoid. (latest-model#Personality and writing style)
- Say when and how much to delegate to subagents; it may under-delegate. For coding, say how much testing fits: none for small reversible edits, relevant checks once, then stop. (latest-model#Subagent delegation, #Testing and verification)
- API requests: with effort above `none`, leave out `temperature`, `top_p`, `top_logprobs`. (latest-model#Update API and model parameters)
- ChatGPT app prompts: headings for context, instructions, constraints. One deliverable per prompt. For facts, ask for sources, labelled uncertainty, and a list of assumptions. (chatgpt#Scope the problem, #Write the prompt clearly, #Improve accuracy)
- The GPT-6 guidance was written for Astra; test it on the target model. (latest-model#Prompting best practices)

## Effort
API: `reasoning.effort` (Responses) or `reasoning_effort` (Chat Completions); Astra and Sol reject `none` (use `low`), Luna accepts it. Codex: Light (`low`), Medium, High, Extra High. ChatGPT app: write `Effort: <low|medium|high> (ChatGPT app: the model picker's thinking/effort option, pick the nearest; not API reasoning.effort)`, or "not settable here" if the plan has no such option. Levels aren't documented for the app: don't invent option names, but still give the line. (latest-model#Update API and model parameters, codex:best-practices#Strong first use, hand-written)

## gpt-6-astra
- Flagship, and the model the GPT-6 prompt advice was written against. (latest-model#Prompting best practices)
- No `none` effort; tool calling needs Responses (Chat Completions supports the model, not tools). In Codex, start at Light (`low`). (latest-model#Limitations, codex:best-practices#Strong first use)

## gpt-6-1-sol
- No dedicated page: apply the Astra advice, then compare. (latest-model#Prompting best practices)
- No `none` effort (use `low`); tool calling needs Responses. Codex's docs name it the model to use when available. (latest-model#Limitations, codex:best-practices#Strong first use)

## gpt-6-luna
- No dedicated page: apply the Astra advice, then compare. (latest-model#Prompting best practices)
- Accepts `none`, but Chat Completions function calling works only at `none`; reasoning with tools needs Responses. In Codex, start at High. (latest-model#Update API and model parameters, codex:best-practices#Strong first use)
