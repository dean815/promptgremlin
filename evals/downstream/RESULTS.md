# Downstream benchmark results

Target model claude-sonnet-5-5 (tool-less, plain chat system prompt). Rewrites by promptgremlin on claude-sonnet-5-5 with an empty config. Grader claude-opus-5-5, blind to which arm wrote each answer. 8 tasks, 2 rewrites per task, 2 answers per rewrite, 4 raw answers per task.

| Metric | Raw ask | Rewritten |
|---|---|---|
| Checks passed | 99% (163/164) | 98% (160/164) |
| Mean answer length (output tokens) | 604 | 1838 |
| Answer cost, all runs | $0.30 | $0.73 (+ $0.55 to rewrite) |

Blind head-to-head (rewritten vs raw, same run index): rewritten won 13, raw won 19, tie 0.

Rewrite drift vs the ask, across 16 rewrites: 1 requirements dropped or weakened, 20 conflicting or invented additions, 118 reasonable additions.

| Task | Raw checks | Rewritten checks | Head-to-head (rw-raw-tie) | Drift (dropped / bad adds) |
|---|---|---|---|---|
| montreal-trip | 19/20 | 20/20 | 4-0-0 | 0 / 3 |
| linkedin-ci | 24/24 | 20/24 | 0-4-0 | 0 / 0 |
| meeting-notes-injection | 20/20 | 20/20 | 0-4-0 | 0 / 1 |
| quarterly-risks | 20/20 | 20/20 | 2-2-0 | 0 / 3 |
| angry-customer-reply | 20/20 | 20/20 | 3-1-0 | 1 / 3 |
| postgres-top-customers | 20/20 | 20/20 | 2-2-0 | 0 / 7 |
| python-bug-minimal | 20/20 | 20/20 | 0-4-0 | 0 / 3 |
| etsy-mug-listing | 20/20 | 20/20 | 2-2-0 | 0 / 0 |
## What this shows (run of 2026-10-06)

- **No measurable downstream gain on these tasks.** Both arms pass nearly every check (99% vs
  98%), and the blind head-to-head favours the raw ask 19 to 13. With 32 pairs that gap is not
  significant, but there is no evidence the rewrites help here.
- **The tasks are too easy to separate the arms.** Sonnet 5.5 already handles a clear casual ask
  well, so the checks sit at the ceiling. A useful next run needs harder or vaguer asks.
- **Rewritten prompts triple the answer length** (1,838 vs 604 output tokens) and cost about 4x
  per task once the rewrite itself is counted. The grader often preferred the shorter raw answer.
- **Rewrites invent context.** 20 additions across 16 rewrites conflict with the ask or invent
  facts, mostly made-up reasons ("a teammate who missed this meeting", "I'm building a
  report", "I'll diff it against my original"). The skill applies the "explain why" guidance by
  inventing a why. This is a skill bug to fix.
- **One rewrite left template brackets** (`linkedin-ci` rewrite 2), so the target model asked
  for the missing facts instead of writing the post. That accounts for all 4 failed rewritten
  checks.

Raw outputs for every run are in `runs/2026-10-06/`: rewrites (`rewrite-*.json`), answers
(`raw-*`, `rewritten-*`), grades (`grade-*`), head-to-head verdicts (`pair-*`) and drift
lists (`drift-*`). All task material is fictional.

Reproduce: `python3 evals/downstream/bench.py OUT_DIR --rewrites 2 --execs 2` (needs a logged-in
`claude` CLI; about 175 model calls, about $5 at API prices).
