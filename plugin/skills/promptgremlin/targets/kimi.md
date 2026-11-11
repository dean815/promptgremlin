---
family: kimi
kind: family
last_verified: 2026-11-11
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
- Sampling is fixed on K3 and K3.1 Pro; leave `temperature` and its siblings out. Multi-turn and tool-loop code must return the full assistant message unchanged, `reasoning_content` and `tool_calls` included; both models require it. (k3-quickstart#Important limits, effort#Fields, thinking#Frequently Asked Questions)

## Effort
- K3.1 Pro and K3: top-level `reasoning_effort`, values `low`, `high`, `max` (default `max`); thinking cannot be disabled, so use `low` when reasoning runs too long. Map low to `low`, medium and high to `high`, max to `max`. Neither takes a `thinking` block; drop any carried over from K2.x. (effort#Fields, thinking#Choose the right thinking model, k3-quickstart#FAQ)
- Kimi app: no control documented. (hand-written)

## kimi-k3-1-pro
- Flagship thinking model: reasoning and Preserved Thinking are always on, and `reasoning_content` may come back beside the answer. Never send a `thinking` parameter; set only `model` and, if wanted, `reasoning_effort`. (thinking#Choose the right thinking model, #Call kimi-k3.1-pro)
- It has its own quickstart, which is not a watched source: a post-trained K3 with 1M context and the same limits as K3 (fixed sampling, 131,072 default output cap, no public image URLs), pitched at coding, 3D creation, and financial research. The K3 notes below carry over. (hand-written: K3.1 Pro quickstart)

## kimi-k3
- Previous-generation flagship, still served: 2.8T parameters, native vision, 1M context; built for long-horizon coding with little supervision, knowledge work, and reasoning. Output cap defaults to 131,072 tokens and can be raised to 1,048,576. (k3-quickstart#Overview, #Important limits)
- To make it continue from a prefix, end `messages` with an assistant message that has `partial: true`. Image input needs base64 or `ms://<file-id>`, not public URLs. (k3-quickstart#Partial Mode, #Important limits)
- For parsed output use `json_schema` with `strict: true`; it constrains the final `content` only, so parse that field and not the reasoning. (k3-quickstart#Structured output)
