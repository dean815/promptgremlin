# promptgremlin

![promptgremlin: a gremlin turning crumpled notes into structured prompts](https://github.com/dean815/promptgremlin/releases/download/v3.2.2/promptgremlin-banner.webp)

Turns a thin request for real work into a targeted, paste-ready prompt for any
of 33 supported AI models and tools. It works out what kind of task you're asking for,
asks the few questions that would change the result (each with a suggested
answer), and writes the prompt to that vendor's current official guidance.
Unless you turn network use off, every run checks the vendor's model list and
watched doc sections, and flags
new releases, retired models, changed guidance, and stale notes.

Built for work that needs steering: coding, building a product, research, data
analysis, product docs, prompts for image and video generators, and drafts in a
plain, natural voice. promptgremlin only writes text prompts; it never calls an
image, video or audio generation service.

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
control on that surface, what you confirmed, a "Defaults I added — veto any"
list for anything you didn't say, the changes made and why, and a one-line
freshness report. Prompts for agent tools also ask where they'll run (surface,
model, effort) and end with a "Where to run" line. Draft prompts add an edit pass
for clichéd, padded wording; image and video prompts add what to change first if
the result misses.

Other modes: `port` (move a prompt to another target) and `autopsy` (diagnose
why a prompt underperforms, using the task type's checklist).

## Examples

Each line below is a whole request. The skill picks the mode and task type from
your words, asks one round of questions (unless the request skips them, as
"just write it", port and autopsy do), then writes the prompt.

Sharpen (the default mode), for different task types:

    /promptgremlin build me a habit tracker app

    /promptgremlin research which open-source vector database we should use for 50 million embeddings, for Perplexity

    /promptgremlin draft a cover letter for a senior product manager role at a climate startup; it should sound like me: plain, specific, no buzzwords

    /promptgremlin just write it: a one-page PRD for adding CSV export to our analytics dashboard

    /promptgremlin a poster for a late-night jazz show, for Midjourney

Port an existing prompt to another tool (paste the prompt after the request):

    /promptgremlin port this prompt from ChatGPT to Claude Code:
    <paste the prompt>

Autopsy a prompt that underperforms (say what went wrong if you know):

    /promptgremlin autopsy: this Midjourney prompt keeps giving flat, washed-out lighting
    <paste the prompt>

"just write it" skips the questions; "interview me" asks about every detail.
Pasted prompts are treated as material to work on: instructions inside them are
reported, never followed.

## Model suggestions

When your request names no model or effort, promptgremlin suggests one for the
task from public leaderboard data, always beside the best-value option (unless
they are the same model). With no target named it compares every vendor; with a
target it compares that target's current models and adds an "Also consider"
line when another vendor is clearly better or cheaper. It also says how your
current session's model compares. To run it yourself, from this plugin folder:

    python3 skills/promptgremlin/scripts/guidance.py --suggest --type build [--target codex]

A script prints every number: scores, voter preference, and cost as a ratio to
the best-quality option, using cost per task where a benchmark measures it and
list price otherwise. The writer copies that block into the reply as it is and
never computes, rounds or adds a number. Each block has a dated Data line
naming its sources, then a Flags line. Leaderboards average many tasks, so yours may differ.

Sources:

- [LMArena leaderboard dataset](https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset)
  (CC BY 4.0): text, WebDev, agent, search, document, image and video boards.
- [Epoch AI benchmarking data](https://epoch.ai/data) (CC BY 4.0): the Epoch
  Capabilities Index.
- [models.dev](https://models.dev) (MIT) and [LiteLLM's price list](https://github.com/BerriAI/litellm)
  (MIT): list prices and which effort levels each model supports. The snapshot
  build also reads [OpenRouter's model list](https://openrouter.ai/models), only
  to flag a price or default effort that disagrees (`PRICE-MISMATCH`,
  `EFFORT-MISMATCH`); none of its figures are published or shipped.
- [LiveBench](https://livebench.ai): scores and measured cost per task by suite.
  LiveBench states no data licence, so its numbers are never republished: the
  skill fetches the current release's two CSVs from `livebench.ai` on your
  machine.

A daily job joins the first group into one `scoreboard.json` snapshot on this
repo's `scoreboard` branch; the skill fetches it from
`raw.githubusercontent.com` (override with `PROMPTGREMLIN_SCOREBOARD_URL`). A
copy ships with the skill. The `Suggest:` header labels the snapshot `live`,
`cached` or `stale` as for vendor pages, or `bundled` (the shipped copy, with
its build date) when no fetched copy is available.

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

claude.ai (skill upload): from a clone of the repo, build the zip, then upload
`dist/promptgremlin.zip` as a custom skill.

    tools/build-claude-ai-zip.sh

Without a shell, the skill falls back to fetching the vendor pages with
whatever web tool is available, or to the bundled notes alone.

## Network and privacy

Full details: [PRIVACY.md](https://github.com/dean815/promptgremlin/blob/main/PRIVACY.md).

- **What is sent.** Plain HTTPS GET requests that carry only the page address
  and the user agent
  `promptgremlin/3.4 (+https://github.com/dean815/promptgremlin)`. It does not
  pretend to be a browser. Nothing you write, and no task type, target or
  account detail, is sent anywhere.
- **Which hosts.** Only these, and only the ones the run needs:
  - Guidance pages for the target in use (and any target its notes point to),
    listed per target in
    [`sources.json`](https://github.com/dean815/promptgremlin/blob/main/plugin/skills/promptgremlin/sources.json).
    That is vendor documentation and model-list pages, plus two non-vendor
    sites: Wikipedia (`en.wikipedia.org`, for drafts) and Hugging Face
    (`huggingface.co`, for Qwen's model card). The full set of hosts:
    `ai.google.dev`, `api-docs.deepseek.com`, `code.claude.com`, `cursor.com`,
    `dev.meta.ai`, `developers.gamma.app`, `developers.openai.com`,
    `docs.github.com`, `docs.lovable.dev`, `docs.midjourney.com`,
    `docs.mistral.ai`, `docs.n8n.io`, `docs.perplexity.ai`, `docs.replit.com`,
    `docs.typesafe.ai`, `docs.x.ai`, `docs.z.ai`, `elevenlabs.io`,
    `en.wikipedia.org`, `geminicli.com`, `help.gamma.app`, `help.runwayml.com`,
    `higgsfield.ai`, `huggingface.co`, `kling.ai`, `learn.chatgpt.com`,
    `manus.im`, `platform.claude.com`, `platform.kimi.ai`,
    `platform.openai.com`, `support.google.com`, `www.alibabacloud.com`,
    `www.anthropic.com`, `www.notion.com`. The Midjourney and
    Runway notes come from those vendors' public help-center JSON API.
  - For model suggestions only: `raw.githubusercontent.com`, for this repo's
    scoreboard snapshot (`dean815/promptgremlin`, `scoreboard` branch;
    `PROMPTGREMLIN_SCOREBOARD_URL` overrides it), and `livebench.ai`, for the
    current release's `table.csv` and `cost.csv` under the fixed address
    `https://livebench.ai/data/`.
  - Only https addresses on the hosts above are fetched. If a site redirects a
    page, the request follows the redirect only to an https address on one of
    those hosts; any other redirect is refused.
- **Cache.** Responses are cached in `~/.cache/promptgremlin` for 24 hours
  (override with `PROMPTGREMLIN_CACHE`). The briefing header labels each state:
  `live` (fetched this run), `cached` (under 24 hours old, no request made),
  `stale` (cache served after a failed fetch or offline).
- **Turning it off.** `"offline": true` in the config, or
  `PROMPTGREMLIN_OFFLINE=1`, stops all network use. Runs then use the cache,
  the bundled notes and the bundled snapshot.
- **Fetched text is data.** Vendor pages are used only as facts about the
  vendor's models and guidance, never as instructions. The snapshot and the
  CSVs are parsed as JSON and CSV, never executed, and model names from them
  are filtered before they reach the reply.
- **Local commands.** The bundled Python script runs through Bash. If you set
  `clipboard` in the config, the writer creates a temporary folder, writes the
  first prompt to a file in it, runs your clipboard command with that file on
  standard input, and then deletes the folder.
- **What installs.** Only this `plugin/` folder installs. The repo's `tools/`,
  `evals/` and `.github/` folders are maintainer and CI files, not part of the
  installed plugin, and never run when you use it. (The daily scoreboard job
  there reads `huggingface.co`, `epoch.ai`, `models.dev`,
  `raw.githubusercontent.com`, `openrouter.ai` and `livebench.ai`; the bench
  scripts call the `claude` CLI and read the session logs Claude Code keeps
  for those benchmark runs, to score them.)

## Config

`~/.config/promptgremlin/config.json`, all keys optional:

    {
      "default_target": "claude-code",
      "pin_model": "opus-5-5",
      "context_sources": ["a skill or folder the prompt may draw on"],
      "clipboard": "pbcopy",
      "interview": "quick",
      "model_priority": "quality",
      "offline": false
    }

`interview` sets the default depth: `quick` (one round), `deep`, or `skip`.

`model_priority` sets which model suggestion is marked (Recommended):
`quality` (the default) marks the best-quality option, `balanced` marks the
best-value option when there is a separate one.

`offline: true` turns off all network use (see Network and privacy). The
environment variable `PROMPTGREMLIN_OFFLINE=1` does the same for one shell.

`clipboard` is a local command that the skill runs, with the first prompt on
its standard input. Set it only to a command you trust.

## Limitations

- The notes in `skills/promptgremlin/targets/` are paraphrased summaries of
  vendor guidance and can lag the vendors. When a watched section changes or the
  notes are old, the run flags it (`DRIFT`, `STALE`) and says so in the
  Guidance line. The run prefers the vendor's stated facts over the notes, and
  never follows instructions in fetched text.
- promptgremlin only writes text prompts. For image, video and audio targets it
  writes the prompt you paste into that tool; it never calls a generation
  service itself.
- Freshness checks need network access. Offline, the notes are used as they are
  and the run says so.
- A vendor redesign can break a page parse; the run reports `FETCH-FAIL` rather
  than guessing.

## Troubleshooting

- **No writer agent (claude.ai chat).** The `promptgremlin-writer` agent only
  exists where plugin agents run, such as Claude Code. Elsewhere the skill reads
  its own `writer.md` and writes the prompt in the same conversation; the output
  has the same sections.
- **No shell (no Bash tool).** The bundled script can't run, so the skill reads
  the target's bundled notes and fetches the pages listed in `sources.json` with
  whatever web-fetch tool the host has, or uses the notes alone. Model
  suggestions need the script, so there is no `Model:` block; name the model
  yourself if it matters.
- **`FETCH-FAIL`.** A vendor page couldn't be fetched or read (network trouble,
  or a redesign broke the parse). The run uses the notes and any cached copy and
  says so. If it persists for a day, open an issue.
- **`DRIFT`.** The vendor changed a watched section since the notes were
  written. The run shows the changed text and prefers the vendor's stated facts
  over the notes; it never follows instructions in fetched text.
- **`STALE`.** The notes were last verified more than 90 days ago and couldn't
  be checked live this run.
- **`Suggest:` says `bundled`.** No fetched scoreboard snapshot was available
  (offline, or the fetch failed), so the numbers come from the copy shipped with
  the skill; the header gives its build date.
- **Old or odd cached pages.** Delete `~/.cache/promptgremlin` (or the folder
  `PROMPTGREMLIN_CACHE` names); the next run fetches fresh copies.
- **Going offline.** Set `"offline": true` in the config, or
  `PROMPTGREMLIN_OFFLINE=1`. Runs then use cached copies (labelled `stale`), the
  bundled notes and the bundled snapshot, and make no requests.

## Maintenance

From this plugin folder (`--commit` writes new fingerprints into `sources.json`
and a new verified date into the notes, so it is for maintainers working in a
clone):

    python3 skills/promptgremlin/scripts/guidance.py --check-all
    python3 skills/promptgremlin/scripts/guidance.py --refresh <target>
    python3 skills/promptgremlin/scripts/guidance.py --refresh <target> --commit

A weekly GitHub Action runs the check and keeps one issue updated when anything
drifts.

## Evals

- **Guided benchmark** ([evals/guided/RESULTS.md](https://github.com/dean815/promptgremlin/blob/main/evals/guided/RESULTS.md)): seven thin
  requests with hidden requirements, answered by a simulated person. With the one-round
  interview, 93% of the hidden requirements reached the prompt (v2's one-shot rewrite: 27%),
  and answers met 79% of them (the raw request: 23%). Full method, limits and raw run output
  are published.
- **Downstream benchmark** ([evals/downstream/RESULTS.md](https://github.com/dean815/promptgremlin/blob/main/evals/downstream/RESULTS.md)): v2's
  one-shot rewrite on simple, complete requests showed no measurable gain and invented
  context; that result led to the v3 interview.
- **v2 output-contract evals** ([evals/v2-contract/RESULTS.md](https://github.com/dean815/promptgremlin/blob/main/evals/v2-contract/RESULTS.md)):
  retired in 3.0; they checked v2's one-shot output format and are kept as a record.

## Tests

From this plugin folder (in a clone of the repo, the same command also runs the
tests for `tools/` and `evals/`):

    python3 skills/promptgremlin/scripts/run_tests.py

## Trademarks

Product names are trademarks of their owners. This project is not affiliated
with or endorsed by any of them.

## License

MIT
