# Changelog

## 3.0.0

Guided sharpening: the skill now interviews before it writes.

- Classifies each request into a task type (build, change-code, research, analyze-data,
  product-doc, image, video, draft, agent, judgment, general); each type lists what an agent
  needs, the question for each gap, and a prompt skeleton (`skills/promptgremlin/types/`).
- Interview depth: `quick` (default, one round of up to 4 questions with suggested answers),
  `deep` ("interview me"), or `skip` ("just write it"). Set a default with the `interview`
  config key.
- No guessing: every fact in the prompt traces to the request, the answers, or an accepted
  default. A source check strips made-up purposes, reasons and relationships, and never turns
  "no preference" into a rule.
- The interview runs in the conversation (the skill no longer forks); a `promptgremlin-writer`
  agent loads guidance and writes, keeping vendor notes out of the main context. Without the
  agent (claude.ai), the skill follows `writer.md` itself.
- Draft prompts include human-voice rules and an edit pass; image and video prompts list what
  to change first if the result misses.
- The skill hands over the prompt and stops; it never carries out the task itself.
- Output: "Assumptions" is replaced by Confirmed / Defaults.
- New benchmarks with published method and run output: `evals/downstream/` (raw vs one-shot
  rewrite) and `evals/guided/` (hidden requirements, simulated person).
- User agent is now `promptgremlin/3.0`.

## 2.0.0

First public release.

- Turns a braindump, rough notes, or a weak prompt into a paste-ready prompt for any of 33
  registered AI models and tools (chat models, coding agents, image/video/audio tools, and
  workflow tools), written to each vendor's current official guidance.
- Three modes: `rewrite` (default; splits multi-part asks into ordered prompts), `port`
  (move a prompt to another target), `autopsy` (diagnose why a prompt underperforms).
- Live freshness checks on every run: flags new models, retired models, changed doc
  sections, and stale notes; fetches over HTTPS with an identifying user agent and a 24-hour
  cache.
- An effort suggestion with each prompt, naming the real control on that surface.
- Treats pasted material and fetched vendor text as data, never instructions; reports
  embedded instructions instead of acting on them.
- Optional personal config (`default_target`, `pin_model`, `context_sources`, `clipboard`).
- Weekly GitHub Action that runs the tests and the freshness check and keeps one issue
  updated when anything drifts.
- Claude Code plugin, plus a build script for a claude.ai skill upload.
