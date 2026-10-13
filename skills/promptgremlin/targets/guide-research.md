---
family: guide-research
kind: guide
last_verified: 2026-10-12
sources: [multi-agent-research, deep-research]
---
## All models
- A research prompt needs the decision it feeds, the scope, the constraints, and the output shape up front; deep-research models start researching on whatever they get and won't ask for missing context, so gaps have to be closed before the prompt is sent. (deep-research#Prompting deep research models)
- Asking clarifying questions first is the recommended pattern when the request is thin: gather goals, preferences and constraints, don't re-ask what the person already said, and don't start the research during clarification. (deep-research#Prompting deep research models)
- Say how much effort fits: a simple fact needs one agent and a handful of searches, a direct comparison a few parallel workers, a broad question many workers with divided responsibilities. Without a scale rule agents overinvest in simple queries. (multi-agent-research#Prompt engineering and evaluations for research agents)
- Start wide, then narrow: short, broad searches to map what exists, then drill into the most promising options. (multi-agent-research#Prompt engineering and evaluations for research agents)
- When the work is split across subagents, give each one an objective, an output format, which tools and sources to use, and clear boundaries, so they don't duplicate each other or leave gaps. (multi-agent-research#Prompt engineering and evaluations for research agents)
- Name where the information lives (web, a document store, an internal tool) so the agent uses the right source; prefer specialised tools over generic search when they exist. (multi-agent-research#Prompt engineering and evaluations for research agents)
- On API surfaces, long research runs belong in background mode, and a tool-call cap is the main lever on cost and latency. (deep-research#Best practices)
