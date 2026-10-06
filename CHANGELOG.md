# Changelog

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
