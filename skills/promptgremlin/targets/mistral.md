---
family: mistral
kind: family
last_verified: 2026-10-06
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
- API: `reasoning_effort` on chat completions (and inside `completion_args` on the Agents and Conversations endpoints). Documented values are `"high"` (full thinking chunk, so `message.content` becomes a list of thinking and text chunks) and `"none"` (minimal thinking, no chunk, plain string). Map low to `"none"`, high and max to `"high"`; medium has no documented value (unverified). Third-party `zai-glm-5-3` on Mistral's API: `low`/`high`/`max`, never `none`; always a chunk list. (reasoning#Model, #Handling thinking chunks)
- Le Chat and other apps: no control documented. (hand-written)

## mistral-large-4
- Current flagship: state-of-the-art open-weight general-purpose multimodal model. (lineup page)
- The reasoning page lists it as `mistral-large-4-0` with adjustable `reasoning_effort`, no extra setup. Map low to `"none"`, high to `"high"` (see Effort). (reasoning#Model)
- Nothing model-specific is published on prompting, so use the family-wide rules above; keep prompts self-contained and re-test after switching from Large 3. (hand-written)

## mistral-medium-3-5
- Frontier multimodal model tuned for agentic and coding work (no longer the flagship). Supports `reasoning_effort`; use `"high"` for agent and code tasks. (lineup page; reasoning#Model)
- Give agent prompts an explicit finish condition and approval boundaries. (hand-written)

## mistral-small-4
- Hybrid model that unifies instruct, reasoning, and coding. The reasoning page documents `reasoning_effort` on `mistral-small-latest`; that this alias is Small 4 is (unverified). (lineup page; reasoning#Model)
- Keep prompts compact and set `"none"` for simple classification or extraction. (hand-written)

## mistral-large-3
- Open-weight general-purpose multimodal model. The reasoning page does not list it, so a `reasoning_effort` setting is (unverified); do not rely on one. (lineup page; reasoning#Model)
- With no documented reasoning control, put the stepwise instructions and worked examples in the prompt. (prompting#Prompting Examples)
