---
family: kimi
kind: family
last_verified: 2026-10-01
sources: [best-practice, effort, k3-quickstart, thinking]
---
## All models
- Moonshot publishes one generic prompt best-practice page (not per model) plus thinking and effort docs. Model sections draw on the thinking, effort, and K3 quickstart pages and the lineup page; anything past those is hand-written. (hand-written: no per-model guide; best-practice, effort, k3-quickstart, thinking)
- Say what you want in detail, including audience, format, and length. The model cannot guess, so a vague request gets a generic answer. (best-practice#Write Clear Instructions)
- Put the role and standing rules in the system message and the material to process in the user message. (best-practice#Requesting the Model to Assume a Role)
- Delimit distinct inputs with triple quotes, XML tags, or headings, and when steps matter, write them out in order. (best-practice#Using Delimiters, #Clearly Define the Steps)
- Show an example of the desired output when a style is hard to describe. (best-practice#Provide Examples of Desired Output)
- Set length in paragraphs or bullets; an exact word count is imprecise. (best-practice#Specify the Desired Length)
- For answers from supplied text, say to use only that text and give the exact fallback sentence when the answer is missing. (best-practice#Guide the Model to Use Reference Text)
- With many scenario-specific instructions, classify the query first and supply only the matching instructions. (best-practice#Categorize to Identify Instructions)
- Long chats: summarize old turns into the system message. Long documents: summarize by chunk, then summarize the summaries. (best-practice#For Long-Running Dialog, #Chunk and Recursively Build)
- Thinking models need no "think step by step" line. They return `reasoning_content` apart from `content`, so ask for the answer only. (thinking#Read reasoning_content; hand-written for the prompt consequence)
- Sampling is fixed on K3 and not modifiable on K2.7-code and K2.6; leave `temperature` and its siblings out. Multi-turn code must return the full assistant message, `reasoning_content` and `tool_calls` included. (k3-quickstart#Important limits, thinking#Configure multi-step tool calls)

## Effort
- K3: top-level `reasoning_effort`, values `low`, `high`, `max` (default `max`); thinking cannot be disabled. Map low to `low`, medium and high to `high`, max to `max`. Drop any K2.x `thinking` block. (effort#Fields, k3-quickstart#Reasoning effort)
- K2.7-code: no effort field; thinking always on. K2.6: no effort field; `thinking.type` is `enabled` (default) or `disabled`, `thinking.keep` is `null` or `"all"`. For a quick K2.6 answer use `disabled`. (thinking#Choose the right thinking model; hand-written for the quick-answer advice)
- Kimi app: no control documented. (hand-written)

## kimi-k3
- Flagship: 2.8T parameters, native vision, 1M context; built for long-horizon coding, knowledge work, and deep reasoning. Output cap defaults to 131,072 tokens. (k3-quickstart#Introducing Kimi K3, #Important limits)
- To make it continue from a prefix, end `messages` with an assistant message that has `partial: true`. Image input needs base64 or `ms://<file-id>`, not public URLs. (k3-quickstart#Partial Mode, #Important limits)
- Official web search is not recommended right now; do not design prompts around it. (k3-quickstart#Important limits)

## kimi-k2-7-code
- Dedicated coding model, 256K context, with thinking and Preserved Thinking always on. Do not send `thinking` or `reasoning_effort`. A highspeed variant behaves identically. (thinking#Choose the right thinking model, lineup page)
- For tool-calling runs set `max_tokens` of at least 16,000 so reasoning is not cut off. (thinking#Configure multi-step tool calls)

## kimi-k2-6
- General-purpose thinking model with text and vision input, 256K context. Thinking defaults on and can be disabled; add `thinking.keep: "all"` for multi-turn continuity. (thinking#Control kimi-k2.6 thinking, lineup page)
- For tool-calling runs set `max_tokens` of at least 16,000. (thinking#Configure multi-step tool calls)
