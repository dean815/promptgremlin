---
family: qwen
kind: family
last_verified: 2026-10-01
sources: [prompt-guide, open-weights-card]
---
## All models
- Alibaba publishes one generic Model Studio prompt guide (not per model) and a Hugging Face card for the open-weights Qwen3.8-27B. The API models below have no prompting pages of their own, so model sections are inferred from the card or hand-written. (hand-written: no per-model guide; prompt-guide, open-weights-card)
- Structure the prompt with the guide's framework and drop elements that do not apply: context, objective, style, tone, audience, response format. Style, tone, and audience are the parts braindumps usually omit; ask the user or pick a stated default. (prompt-guide#Use prompt frameworks)
- Be specific about purpose, direction, and how the work should be done; the guide treats this as the single most important step. (prompt-guide#Build clear and specific prompts)
- Add one or two output examples when format, tone, or consistency matters. For JSON extraction, an example plus a JSON template is the guide's top defense against hallucinated fields. (prompt-guide#Tip 1, #Optimization case: Extracting)
- For multi-stage tasks write numbered task steps under their own label. When a task breaks into a fixed sequence of simpler questions, prompt chaining over several turns beats one big prompt. (prompt-guide#Tip 2, #Tip 4)
- Separate units (instructions, pasted documents, examples) with rare marker runs such as `###`, `===`, or `>>>`; put long pasted text in its own delimited block, not inside a sentence. (prompt-guide#Tip 3, #Optimization case: Guide AI assistant)
- Prefer direct instructions over associative descriptions, state constraints as a short list (for example prioritize accuracy, do not alter quoted text), and use unambiguous nouns, such as "language type" in place of "language". (prompt-guide#Optimization cases)
- Asking for the thinking process before the verdict helps on non-reasoning calls. Qwen3.8 thinks by default, so skip chain-of-thought scaffolding unless thinking is switched off. (prompt-guide#Tip 4; open-weights-card#API Usage; hand-written for the combination)
- Sampling settings go beside the prompt, not in it. The card's values for Qwen3.8: thinking mode `temperature` 1.0, `top_p` 0.95, `top_k` 20; non-thinking `temperature` 0.7, `top_p` 0.8, `presence_penalty` 1.5. Framework support varies. (open-weights-card#Best Practices)
- For agent tasks give the model room: the card suggests up to 262,144 reasoning tokens and 131,072 for the final answer where the framework takes separate limits. (open-weights-card#Best Practices)

## Effort
- Documented for Qwen3.8 open weights (card): `reasoning_effort` `xhigh` (default), `medium`, `low`. Map low to `low`, medium to `medium`, high and max to `xhigh`; there is no `high` value. Thinking is on by default; on Qwen Cloud switch it off with `"enable_thinking": false` (self-hosted servers nest it in `chat_template_kwargs`). (open-weights-card#API Usage)
- Do not default agents to `low`; retries can lengthen multi-turn runs. (open-weights-card#API Usage)
- Whether the API models accept these values is (unverified); read only from the card. Chat app: none documented. (hand-written)

## qwen3-8-max
- Flagship API model; no model page was fetched. Treat the Qwen3.8 card as its closest reference, with thinking on by default. (open-weights-card#API Usage; hand-written)
- Spend effort on a full prompt: framework, examples, explicit format. (prompt-guide#Use prompt frameworks)

## qwen3-7-plus
- Previous generation; the Qwen3.8 card does not cover it, so its thinking and effort controls are (unverified). Prefer the generic guide's techniques and do not assume `xhigh`. (hand-written)

## qwen3-8-flash
- Speed tier; no model page fetched. Keep the prompt short, single-purpose, and explicit about output format, and keep effort at `medium` or `low` for simple work, `xhigh` only for hard reasoning. (hand-written: inferred from Flash positioning)
