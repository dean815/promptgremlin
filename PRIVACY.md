# Privacy policy

promptgremlin is a Claude skill that runs locally inside Claude. It has no server, no account, and no analytics. Its author does not receive, collect, or store any data from people who use it.

## What it handles

- **Your input.** The braindump, notes, or prompt you give it stays in your Claude conversation. promptgremlin never sends it anywhere.
- **Vendor documentation.** To write prompts from current guidance, the bundled script (`skills/promptgremlin/scripts/guidance.py`) fetches public prompting-guide and model-list pages from the vendors listed in `skills/promptgremlin/sources.json`, over HTTPS. Each request carries only the page URL and the user agent `promptgremlin/3.3 (+https://github.com/dean815/promptgremlin)`, and no user data. Those vendors' own privacy policies apply to their sites.
- **Model suggestion data.** To suggest a model for your task, the same script fetches two more kinds of public file, with the same user agent and no user data: the scoreboard snapshot from `raw.githubusercontent.com` (this project's `scoreboard` branch on GitHub; `PROMPTGREMLIN_SCOREBOARD_URL` overrides the address), and the current release's `table.csv` and `cost.csv` from `livebench.ai`. The task type and target you pick are used only on your machine to read those files; they are not sent. GitHub's and LiveBench's own privacy policies apply to their sites.
- **Local cache.** Fetched pages are cached on your machine in `~/.cache/promptgremlin` (override with `PROMPTGREMLIN_CACHE`) and reused for up to 24 hours. Delete that folder at any time.
- **Optional config.** If you create `~/.config/promptgremlin/config.json`, the skill reads it locally to set defaults. If you list context sources there, Claude may read them to write your prompt, and the skill names them in its output. Nothing from them leaves your Claude session through promptgremlin.

## Claude

Your conversations with Claude are handled under Anthropic's own privacy policy, not this one.

## Contact

Questions or concerns: open an issue at https://github.com/dean815/promptgremlin/issues.
