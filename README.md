# promptgremlin

![promptgremlin: a gremlin turning crumpled notes into structured prompts](assets/promptgremlin-banner.webp)

Turns a thin request for real work into a targeted, paste-ready prompt for any
registered AI model or tool. It works out what kind of task you're asking for,
asks the few questions that would change the result (each with a suggested
answer), and writes the prompt to that vendor's current official guidance.
Every run checks the vendor's model list and watched doc sections, and flags
new releases, retired models, changed guidance, and stale notes.

Built for work that needs steering: coding, building a product, research, data
analysis, product docs, image and video generation, and drafts that have to
sound like a person wrote them.

## How it works

    /promptgremlin build me a habit tracker app

1. **Classify.** The request is matched to a task type (build, change-code,
   research, analyze-data, product-doc, image, video, draft, agent, judgment,
   or general). Each type knows what an agent needs for that kind of work.
2. **Interview.** One round of up to 4 questions about the gaps that matter
   most, each with a suggested answer and its reason, so "ok" or a few words
   is enough. Say "interview me" for a deeper walk through every detail, or
   "just write it" to skip the questions.
3. **Write.** A writer agent loads the vendor's guidance and writes the
   prompt. Every fact in it comes from your request, your answers, or a
   default you accepted; nothing is made up to fill a gap.

Each prompt comes in a code block with an effort suggestion naming the real
control on that surface, what you confirmed vs what was defaulted, the changes
made and why, and a one-line freshness report. Draft prompts add an edit pass
for stripping AI tells; image and video prompts add what to change first if
the result misses.

Other modes: `port` (move a prompt to another target) and `autopsy` (diagnose
why a prompt underperforms, using the task type's checklist).

## Supported targets

33 targets. Use the key or any alias.

Model families:

- `anthropic`: `claude`, `claude-ai`, `claude-api`
- `openai`: `gpt`, `chatgpt`, `openai-api`
- `gemini`: `google-gemini`, `gemini-api`
- `xai`: `grok`, `x-ai`
- `zhipu`: `glm`, `z-ai`, `zai`
- `qwen`: `alibaba`, `qwen-api`
- `deepseek`: `deepseek-api`
- `mistral`: `mistral-ai`
- `meta`: `muse`, `llama`, `meta-ai`
- `kimi`: `moonshot`, `kimi-api`

Tools and products (a tool that sits on a model family also loads that family's notes):

- `claude-code`: `cc` (also loads `anthropic` notes)
- `codex`: `codex-cli`, `openai-codex` (also loads `openai` notes)
- `gemini-cli`: `gemini-code` (also loads `gemini` notes)
- `cursor`: `cursor-agent`, `windsurf`
- `copilot`: `github-copilot`
- `lovable`: `lovable-dev`
- `replit`: `replit-agent`
- `perplexity`: `pplx`
- `manus`: `manus-ai`
- `nano-banana`: `nanobanana`, `gemini-image`
- `gpt-image`: `openai-image`, `dall-e`
- `midjourney`: `mj`
- `google-video`: `veo`, `flow`, `omni`, `gemini-omni`, `google-flow`
- `sora`: `openai-video`
- `runway`: `runwayml`
- `kling`: `kling-ai`
- `higgsfield`: `higgsfield-ai`
- `elevenlabs`: `eleven-labs`, `11labs`
- `n8n`: `n8n-ai`
- `gamma`: `gamma-app`
- `notion-ai`: `notion`, `notion-agents`
- `jev`: `typesafe`
- `grok-bot`: `grokbot`, `grok-bots` (also loads `xai` notes)

## Install

Claude Code (marketplace):

    claude plugin marketplace add dean815/promptgremlin
    claude plugin install promptgremlin@promptgremlin

claude.ai (skill upload): build the zip, then upload `dist/promptgremlin.zip` as a custom skill.

    tools/build-claude-ai-zip.sh

Without a shell, the skill falls back to fetching the vendor pages with
whatever web tool is available, or to the bundled notes alone.

## Network and privacy

Full details: [PRIVACY.md](PRIVACY.md).

- Each run fetches the target's vendor documentation pages (and model-list
  pages) over HTTPS with an identifying user agent,
  `promptgremlin/3.0 (+https://github.com/dean815/promptgremlin)`. It does not
  pretend to be a browser.
- Responses are cached in `~/.cache/promptgremlin` for 24 hours. Override the
  location with `PROMPTGREMLIN_CACHE`. The briefing header labels each state:
  `live` (fetched this run), `cached` (under 24 hours old, no request made),
  `stale` (cache served after a failed fetch or offline).
- Nothing you write is sent anywhere: requests carry only the vendor page URLs.
- The Midjourney and Runway notes are fetched from those vendors' public
  help-center JSON API.
- Fetched text is treated as reference material, never as instructions.

## Config

`~/.config/promptgremlin/config.json`, all keys optional:

    {
      "default_target": "claude-code",
      "pin_model": "opus-5-5",
      "context_sources": ["a skill or folder the prompt may draw on"],
      "clipboard": "pbcopy",
      "interview": "quick"
    }

`interview` sets the default depth: `quick` (one round), `deep`, or `skip`.

`clipboard` is a local command that the skill runs, with the first prompt on
its standard input. Set it only to a command you trust.

## Limitations

- The notes in `skills/promptgremlin/targets/` are paraphrased summaries of
  vendor guidance and can lag the vendors. When a watched section changes or the
  notes are old, the run flags it (`DRIFT`, `STALE`) and says so in the
  Guidance line; the changed text wins over the notes.
- Freshness checks need network access. Offline, the notes are used as they are
  and the run says so.
- A vendor redesign can break a page parse; the run reports `FETCH-FAIL` rather
  than guessing.

## Maintenance

    python3 skills/promptgremlin/scripts/guidance.py --check-all
    python3 skills/promptgremlin/scripts/guidance.py --refresh <target>
    python3 skills/promptgremlin/scripts/guidance.py --refresh <target> --commit

A weekly GitHub Action runs the check and keeps one issue updated when anything
drifts.

## Evals

- **Guided benchmark** ([evals/guided/RESULTS.md](evals/guided/RESULTS.md)): seven thin
  requests with hidden requirements, answered by a simulated person. With the one-round
  interview, 93% of the hidden requirements reached the prompt (v2's one-shot rewrite: 27%),
  and answers met 79% of them (the raw request: 23%). Full method, limits and raw run output
  are published.
- **Downstream benchmark** ([evals/downstream/RESULTS.md](evals/downstream/RESULTS.md)): v2's
  one-shot rewrite on simple, complete requests showed no measurable gain and invented
  context; that result led to the v3 interview.
- **Output-contract evals** ([evals/RESULTS.md](evals/RESULTS.md)): v2-era checks of format
  and targeted behaviours. They measure contract compliance, not answer quality.

## Tests

    python3 skills/promptgremlin/scripts/run_tests.py

## Trademarks

Product names are trademarks of their owners. This project is not affiliated
with or endorsed by any of them.

## License

MIT
