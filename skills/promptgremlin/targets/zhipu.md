---
family: zhipu
kind: family
last_verified: 2026-10-06
sources: [glm-flagship, glm-flash, migration]
---
## All models
- Z.ai publishes no prompting guide for GLM. What exists is the GLM-5.3 feature and parameter page, a migration checklist, and a GLM-5.3-Flash page with worked task prompts; per-model sections below come from those, and general craft is hand-written. (hand-written: no official guide; glm-flagship, glm-flash, migration)
- Reasoning is forced on for GLM-5.3 and the Flash models: `thinking.type` accepts only `enabled`, and `disabled` errors. Never write "answer without thinking"; for a quick answer lower the effort setting instead. (glm-flagship#Feature Changes, migration#3. Deep Thinking)
- Sampling lives beside the prompt: `temperature` defaults to 1.0 and `top_p` to 0.95; tune one, not both. (migration#2. Update Sampling Parameters)
- Context is 1M tokens in, up to 128K out. For long agent or coding runs leave `max_tokens` generous. (glm-flagship#Feature Changes, migration#Migration Checklist; hand-written for the advice)
- Typical call shape is a system message that fixes a role and tech stack, then a user message with the concrete deliverable. Mirror it: role and stack in the system part, the task and finish line in the user part. (glm-flagship#Quick Start)
- For agent and coding tasks, define the finish line: what artifact is delivered, how to run or check it, and what must be reported at the end. Do this as acceptance criteria, not as a step-by-step recipe, for GLM-5.3's long tasks. (glm-flagship#Stronger Coding; hand-written for the acceptance-criteria phrasing)
- Streaming reasoning and tool-call arguments are client code (`stream`, `tool_stream`, reading `reasoning_content`), not prompt text. (migration#4. Streaming Output and Tool Calls)

## Effort
- API: `thinking: {"type": "enabled"}` plus top-level `reasoning_effort`, values `low`, `high`, `max` (default `max`). Map low to `low`, medium and high to `high`, max to `max`; there is no medium level. Use `max` for complex coding. A formerly `thinking.type: "disabled"` request becomes `enabled` with `low`. (glm-flagship#Feature Changes, migration#Migration Checklist)
- Z.ai chat app: no control documented; ask in plain words. (hand-written)

## glm-5-3
- Flagship, text-only input. Built for long-horizon software and agent work and trained to take whole tasks end to end, so give the goal and acceptance criteria, not a decomposition. (glm-flagship#Overview, #Stronger Coding)
- Strong at security research and vulnerability work; state the authorization and scope in the prompt when that is the job. (glm-flagship#Overview; hand-written for the scope advice)

## glm-5-3-flash
- Native multimodal: images (URL preferred, or Base64), video, and files as input. Recommended settings: `temperature` 1, `top_p` 0.95, `reasoning_effort` `max`, `thinking.clear_thinking` `false`. (glm-flash#How to Use)
- Its documented task prompts share a shape: analyze the inputs first (structure, sources, design system), build, then render or run and compare against the reference, iterate on differences, and end by reporting what is covered, what was verified, and what risks remain. (glm-flash#Best Practices)
- For reports and models, forbid invented figures, require sources, and ask it to separate disclosed facts, assumptions, and conclusions. For deliverables, name the audience, page count, structure, and style. (glm-flash#Best Practices)

## glm-5-3-flashx
- Same model behavior and parameters as `glm-5-3-flash`, served faster (about 200 tokens per second); use the Flash notes. (glm-flash#Model Overview, #How to Use)

## glm-5-2
- Predecessor on the same base model; its own page was not fetched, so nothing 5.2-specific is confirmed. Reuse the GLM-5.3 prompt shape, with less reliance on very long unsupervised runs. (glm-flagship#Overview; hand-written)
- The migration notice implies 5.2 accepted `thinking.type: "disabled"`. Whether 5.2 takes `reasoning_effort` is (unverified); omit it and send only the thinking setting. (migration#Migration Checklist)
