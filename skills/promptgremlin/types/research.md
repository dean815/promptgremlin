---
type: research
default_target: claude-ai
---
# research: find out, compare, survey, recommend

## Slots
1. **decision** (high): what the answer feeds (a choice between options, a
   plan, a briefing). Suggest from the request.
2. **strategy** (high): quick scan (an hour's reading), wide survey (many
   options, shallow), deep dive (few options, thorough), or wide then deep on
   the top 2. For a tool with subagents or deep-research mode, offer parallel
   research per option. Suggest from the question's shape: "which X" → wide
   then deep; "how does X work" → deep.
3. **context and constraints** (high): options already known or ruled out;
   limits such as budget, scale, stack, region.
4. **output** (medium): comparison table, recommendation with reasons,
   briefing, citations. Suggest table + recommendation for "which X".
5. **sources** (medium): recency window, primary sources only, sources to
   avoid. Suggest last 12–18 months and primary docs for fast-moving topics.
6. **stop rule** (low): how many options, how long, when enough is enough.

## Prompt skeleton
Decision and context → what's known or ruled out → constraints → strategy
spelled out as steps → source rules → output shape → stop rule.

## Type guidance
- Research agents do better with an explicit breadth/depth plan and a stop
  rule; without one they either stop early or sprawl.
- Ask for claims tied to sources, and for "unknown" rather than guesses.
- With subagent-capable tools, describe how to split the work and how to
  merge results.

## Sources
Anthropic's multi-agent research system write-up; OpenAI and Google deep
research docs; Perplexity prompting guide.
