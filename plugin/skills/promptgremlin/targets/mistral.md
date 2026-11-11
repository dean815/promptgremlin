---
family: mistral
kind: family
last_verified: 2026-11-11
sources: [prompting, reasoning]
---
## All models
- Mistral has one generic prompting page for all its models and a reasoning page; there are no per-model prompting pages. Model sections below come from those pages and the models lineup page, and are hand-written where they go further. (hand-written: no per-model guide; prompting, reasoning)
- Start with a one-line purpose, "You are a <role>, your task is to <task>", then organized sections. Write for a reader with no prior context, so the prompt stands alone. (prompting#Providing a Purpose, #Structure)
- Use Markdown headings or XML-style tags to mark sections (instructions, categories, response format, examples). If you cannot control a system prompt, concatenate it ahead of the user query in one user message. (prompting#Formatting, #System Prompt)
- Show a few examples when format matters, either inline under an Examples heading or as fake user and assistant turns before the real query. (prompting#Example Prompting)
- Replace blurry words ("too long", "interesting", "better", "many") with objective measures or an explicit definition. (prompting#Avoid Subjective and Blurry Words)
- Long prompts breed contradictions. Rewrite overlapping rules as a decision tree of ordered if/otherwise branches. (prompting#Avoid Contradictions)
- Do not make the model count words or characters; supply the counts as input fields and ask for decisions against them. (prompting#Do Not Make LLMs Count Words)
- Make the model emit only what is strictly needed (the changed field, not the whole record), since generation is slower than reading. (prompting#Do Not Generate Too Many Tokens)
- For ratings use a worded scale, each level defined in a phrase (Very Low to Very Good), not a bare 1-to-5. Convert to numbers afterward if needed. (prompting#Prefer Worded Scales)
- For classification, asking for the bare label is cheapest; asking for a JSON object is more reliable and flexible. Enforcing a JSON schema is the `response_format` parameter, not prompt text. (prompting#Prompting Examples)
- Break complex work into stated steps and give facts the answer must draw on in their own section. Re-test prompts when the model changes. (prompting#Prompting Examples, #Advice)
- With reasoning on, later turns must carry the whole earlier assistant message, thinking chunk included; dropping it hurts quality. That is code, not prompt text. (reasoning#Multi-turn conversations)

## Effort
- API: `reasoning_effort` on chat completions (and inside `completion_args` on the Agents and Conversations endpoints). Values depend on the model. `mistral-large-4`: `"low"`, `"medium"`, `"high"` only; map max to `"high"`. `mistral-small-4`: `"high"` (`message.content` becomes a list of thinking and text chunks) or `"none"` (plain string); map low to `"none"`, high and max to `"high"`; medium is undocumented (unverified). (reasoning#Model, #Mistral Large 4 reasoning effort, #Handling thinking chunks)
- Le Chat and other apps: no control documented. (hand-written)

## mistral-large-4
- Current flagship: state-of-the-art open-weight general-purpose multimodal model. (lineup page)
- API id `mistral-large-4` or `mistral-large-4-0`. It rejects `none`, `minimal`, `xhigh`, and `max`; set `high` explicitly as the starting point and step down to `medium` or `low` when tokens or latency matter. The preview's `none` is now `low`. (reasoning#Mistral Large 4 reasoning effort)
- Nothing model-specific is published on prompting, so use the family-wide rules above; keep prompts self-contained and re-test after switching from Large 3. (hand-written)

## mistral-small-4
- Hybrid model that unifies instruct, reasoning, and coding. The reasoning page lists it as `mistral-small-2603` with adjustable `reasoning_effort`, no extra setup. (lineup page; reasoning#Model)
- Keep prompts compact and set `"none"` for simple classification or extraction. (hand-written)
