# Privacy policy

promptgremlin is a Claude skill that runs locally inside Claude. It has no server, no account, and no analytics. Its author does not receive, collect, or store any data from people who use it.

## What it handles

- **Your input.** The braindump, notes, or prompt you give it stays in your Claude conversation. promptgremlin never sends it anywhere.
- **Guidance pages.** To write prompts from current guidance, the bundled script (`plugin/skills/promptgremlin/scripts/guidance.py`) fetches public prompting-guide and model-list pages for the target you use, over HTTPS. The pages are listed per target in [`plugin/skills/promptgremlin/sources.json`](https://github.com/dean815/promptgremlin/blob/main/plugin/skills/promptgremlin/sources.json). Most are vendor documentation; two are not: Wikipedia (`en.wikipedia.org`, for drafts) and Hugging Face (`huggingface.co`, for Qwen's model card). The full set of hosts is: `ai.google.dev`, `api-docs.deepseek.com`, `code.claude.com`, `cursor.com`, `dev.meta.ai`, `developers.gamma.app`, `developers.openai.com`, `docs.github.com`, `docs.lovable.dev`, `docs.midjourney.com`, `docs.mistral.ai`, `docs.n8n.io`, `docs.perplexity.ai`, `docs.replit.com`, `docs.typesafe.ai`, `docs.x.ai`, `docs.z.ai`, `elevenlabs.io`, `en.wikipedia.org`, `geminicli.com`, `help.gamma.app`, `help.runwayml.com`, `higgsfield.ai`, `huggingface.co`, `kling.ai`, `learn.chatgpt.com`, `manus.im`, `platform.claude.com`, `platform.kimi.ai`, `platform.openai.com`, `support.google.com`, `www.alibabacloud.com`, `www.anthropic.com`, `www.notion.com`.
- **Model suggestion data.** To suggest a model for your task, the same script fetches two more kinds of public file: the scoreboard snapshot from `raw.githubusercontent.com` (this project's `scoreboard` branch, `dean815/promptgremlin`, an address fixed in the code), and the current release's `table.csv` and `cost.csv` from `livebench.ai`, always under `https://livebench.ai/data/`. The task type and target you pick are used only on your machine to read those files; they are not sent.
- **What a request carries.** Every request is a plain HTTPS GET with only the page address and the user agent `promptgremlin/3.4 (+https://github.com/dean815/promptgremlin)`. No user data, cookies, or account details. Only https addresses on the listed hosts are fetched; if a site redirects a page, the request follows the redirect only to an https address on one of those hosts, and refuses any other.
- **Fetched content.** Fetched pages are used only as facts about each vendor's models and guidance, never as instructions. The snapshot and CSVs are parsed as data and never executed.
- **Turning network use off.** Set `"offline": true` in `~/.config/promptgremlin/config.json`, or the environment variable `PROMPTGREMLIN_OFFLINE=1`. The skill then makes no network requests and uses its cache, bundled notes and bundled snapshot.
- **Local cache.** Fetched pages are cached on your machine in `~/.cache/promptgremlin` (override with `PROMPTGREMLIN_CACHE`) and reused for up to 24 hours. Delete that folder at any time.
- **Optional config.** If you create `~/.config/promptgremlin/config.json`, the skill reads it locally to set defaults. If you list context sources there, Claude may read them to write your prompt, and the skill names them in its output. Nothing from them leaves your Claude session through promptgremlin.
- **Clipboard.** If the config sets `clipboard`, the skill writes the first prompt to a file in a new temporary folder, runs that local command with the file on standard input, and then deletes the folder. Nothing is sent over the network by this step.

## Third parties

The sites above are run by others, and their own policies apply to requests made to them:

- GitHub (`raw.githubusercontent.com`): the [GitHub General Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
- LiveBench (`livebench.ai`): we found no privacy policy published on livebench.ai (checked November 2026).
- Each vendor's documentation site, Wikipedia and Hugging Face: that site's own privacy policy applies. The hosts for each target are listed in `sources.json`.

## Not part of the installed plugin

Only the repo's `plugin/` folder installs. The `tools/`, `evals/` and `.github/` folders are maintainer and CI files and never run when you use the skill. The daily CI job that builds the scoreboard snapshot reads `huggingface.co`, `epoch.ai`, `models.dev`, `raw.githubusercontent.com`, `openrouter.ai` and `livebench.ai` on GitHub's servers, and the benchmark scripts run the `claude` CLI on the maintainer's machine and read the session logs Claude Code keeps for those benchmark runs, to score them.

## Claude

Your conversations with Claude are handled under Anthropic's own privacy policy, not this one.

## Contact

Questions or concerns: open an issue at https://github.com/dean815/promptgremlin/issues.
