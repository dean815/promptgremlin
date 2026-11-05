# Changelog

## 3.4.1

- The scoreboard snapshot's address is fixed in the code; the `PROMPTGREMLIN_SCOREBOARD_URL`
  override is gone, so no setting from your environment sits beside an address the skill
  fetches.
- A test's sample hostile text no longer spells out a download-and-run command.

## 3.4.0

Directory resubmission: a smaller install, no network unless you allow it, and fetched data
kept to facts.
- The plugin now lives in `plugin/`, and only that folder installs. The repo's `tools/`,
  `evals/` and `.github/` folders are maintainer and CI files and are no longer part of the
  plugin.
- Offline switch: `"offline": true` in the config, or `PROMPTGREMLIN_OFFLINE=1`, stops all
  network use. Runs use the cache, the bundled notes and the bundled snapshot.
- Fetching accepts https addresses on the documented hosts only, and a redirect is followed
  only to an https address on one of them. LiveBench is always read from
  `https://livebench.ai/data/`; the scoreboard snapshot can no longer choose that address.
- Fetched vendor text is treated as facts about the vendor's models and guidance, never as
  instructions, and model names from fetched data are filtered before they reach the reply.
  Page headings print only as short plain labels, and all page text sits inside the
  vendor-text fence.
- The fetched scoreboard snapshot is shape-checked before use; a malformed one falls back to
  the bundled copy instead of stopping model suggestions, as does a LiveBench CSV that can't
  be parsed. Only known flag codes print, and a
  fetched model name may only use words already in its id or aliases.
- `"offline"` in the config also accepts `"true"`, `"1"`, `"yes"` and `"on"`.
- Meta's Llama guide is read from `dev.meta.ai`, the address `www.llama.com` redirects to.
- Every LiveBench number in the plugin's test fixtures is now invented; none are copied from
  LiveBench.
- OpenRouter is only a cross-check: the snapshot carries no price, effort level or default
  taken from it, and the Data line names models.dev and LiteLLM.
- README: examples for sharpen, port and autopsy, a Troubleshooting section, the
  `model_priority` and `offline` config keys, and the full list of hosts the skill contacts.
  PRIVACY.md links the third-party privacy policies.
- User agent is now `promptgremlin/3.4`.

## 3.3.0

Model suggestions.
- When a request names no model or effort, the interview's model-and-effort question now
  comes from `guidance.py --suggest`: the best-quality pick for the task type, the best-value
  option beside it (unless it is the same model), how the session's model compares, and an
  "Also consider" line when another vendor is clearly better or cheaper. With no target named,
  every vendor is compared and the option picked sets the target.
- Every model number in the reply comes from that script's output, with a dated Data line. The
  writer copies the `Model:` block as it is, before `Where to run`.
- Sources: LMArena and Epoch AI (CC BY 4.0), models.dev and LiteLLM (MIT) and OpenRouter, joined
  daily into a `scoreboard.json` snapshot; LiveBench is fetched directly from `livebench.ai`
  and never republished. A dated copy of the snapshot ships with the skill as a fallback.
- Cost compares cost per task where LiveBench measures it, list price otherwise, as a ratio.
- Effort comes from each model's notes; `EFFORT-MISMATCH` flags OpenRouter disagreeing.
- Cursor and Copilot compare the model families they offer. Vendor pricing pages are watched
  for drift.
- New outbound requests: `raw.githubusercontent.com` and `livebench.ai` (see PRIVACY.md).
  User agent is now `promptgremlin/3.3`.
- Guided bench gains model-block checks and two tasks.

## 3.2.3

- plugin.json now declares the directory listing icon, as the plugin reference describes. No
  change to how the skill behaves.

## 3.2.2

Smaller install, for the plugin directory's review ("ship fewer files").
- The public repo no longer ships benchmark run output (611 files) or the README banner image;
  both are attached to the GitHub release instead. The repo goes from 708 files to 96.
- The plugin icon is 512px and 75 KB, down from 1254px and 705 KB; same image.
- No change to how the skill behaves.

## 3.2.1

- Fix: prompts sometimes reached the person without a code block. The writer's reply comes
  back from its subagent with every line indented, and relaying it could strip the fence
  lines too. The relay now drops the indentation and keeps every fence at the left margin.
  16 of 16 test runs delivered fenced prompts, including the long-run case that failed before.

## 3.2.0

From the first weekly review of real runs (TOOL-67 to TOOL-70):

- Agent prompts (Claude Code, Codex, Cursor and other agent tools) get a run-setup question
  before writing: where it runs, which model and which effort, suggested from the current
  session. The prompt is tuned to that model, and the reply ends with a `Where to run:` line.
- Every instruction is stated, found or added. First person only for what the person said;
  found and added items are listed under `Defaults I added — veto any`, which replaces the
  old Confirmed / Defaults section.
- Build: "clone" or "identical to" requests suggest the full feature set and a solid v1; a
  run-length question; long runs get a stretch phase after the checklist.
- Unattended builds keep a running app and a PROGRESS.md handoff after each milestone; a
  prompt that overrides part of CLAUDE.md keeps its end-of-work steps.
- Guided benchmark, 4 tasks, quick mode: 99% of hidden requirements in the prompt, 0
  contradictions, answers meet 97% of them, still one round of questions.

## 3.1.2

Weekly refresh of vendor notes (15 targets flagged on 2026-10-13); every target and guide now
checks clean.

- Gemini: Gemini 3.8 Flash and 3.6 Flash covered; 3.5 Flash and 3.7 Flash retired; thinking
  levels updated.
- Meta: new Muse Wonder 1.0 (preview, long-horizon agent and coding work), now the flagship.
- Nano Banana: Nano Banana 2.1 is detected and is the default; 3.1 Flash Image marked
  previous-generation; new grounding and video-to-image notes.
- xAI and Grok Bot: reasoning-effort and encrypted-reasoning changes; tagging a Bot on X.
- OpenAI and Codex, Cursor (rules can reference files), Gamma (Plan, Express and Research
  modes), Google Video (Veo and Flow tips), Notion AI, Qwen, Zhipu: notes updated.
- Stable watch lists for Gamma, Manus and Notion AI, which were fingerprinting page footers and
  a subtitle and raising false drift.

## 3.1.1

- Anthropic notes refreshed: Claude Haiku 5.5 added (effort replaces the thinking budget, search
  with today's date, early stopping in long agent prompts, verifying code changes, chatbots
  holding to their system prompt); Claude Haiku 4.5 retired.
- Effort guidance updated: Haiku 5.5 defaults to medium like Opus 5.5, per-model starting
  levels for Sonnet 5.5 and Haiku 5.5, and per-message effort changes that keep the prompt
  cache.

## 3.1.0

- Research and draft prompts now draw on watched public guides, checked for changes like the
  vendor notes: `guide-research` (Anthropic's multi-agent research write-up, OpenAI's deep
  research guide) and `guide-draft` (Wikipedia's "Signs of AI writing"). Other task types say
  which target notes cover them.
- Stricter source check in the writer: agreements stay as loose as the person left them, bans
  cover only what was ruled out, no rules for slots nobody raised, no invented folder or file
  names, no claims about attached material. On the four hardest benchmark tasks, made-up
  details fell from 9 to 5 and contradictions from 1 to 0.
- v2's output-contract evals are retired to `evals/v2-contract/` as a record.
- User agent is now `promptgremlin/3.1`.

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
