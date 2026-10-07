# Guided benchmark results

Does the v3 interview get the person's real requirements into the prompt? Seven thin requests
(build, change-code, research, analyze-data, product-doc, image, draft), each with a hidden
intent sheet of 8-11 requirements the person has in mind but did not type. A simulated person
sees only that sheet and answers whatever the skill asks; it says "no preference" for anything
not on the sheet and never volunteers items. The grader checks each final prompt against the
sheet and lists facts the prompt made up, then, for text tasks, checks the target model's
answer against the sheet.

Run 2, 2026-10-07 (after the writer's source check). Run 1 is in `RESULTS-run1.md`.
7 tasks, 2 runs per arm. Skill and simulated person on claude-sonnet-5-5; answers by claude-sonnet-5-5; grader claude-opus-5-5. The simulated person answers only from a hidden intent sheet. Arms: raw = request as typed; v2 = one-shot rewrite; quick / deep = v3 interview.

| Arm | Intent in final prompt | Contradicted | Invented facts | Intent met by answer | Rounds | Questions | Words typed | Failed runs |
|---|---|---|---|---|---|---|---|---|
| raw | 0% | 0 | 0 | 23% | 0.0 | 0.0 | 0.0 | 0 |
| v2 | 27% | 15 | 62 | 17% | 0.0 | 0.0 | 0.0 | 0 |
| quick | 93% | 1 | 9 | 79% | 1.0 | 5.6 | 84.6 | 0 |
| deep | 93% | 0 | 9 | 89% | 2.2 | 9.1 | 117.2 | 0 |

Per task, intent in final prompt (and met by answer):

| Task | raw | v2 | quick | deep |
|---|---|---|---|---|
| habit-tracker (build) | 0% | 9% | 95% | 100% |
| slow-csv-export (change-code) | 0% | 61% | 100% | 50% |
| vector-db-research (research) | 0% (0%) | 11% (0%) | 100% (56%) | 100% (83%) |
| churn-analysis (analyze-data) | 0% (62%) | 38% (50%) | 100% (78%) | 100% (75%) |
| workspaces-prd (product-doc) | 0% (0%) | 0% (0%) | 88% (81%) | 100% (100%) |
| coffee-instagram (image) | 0% | 39% | 67% | 100% |
| landlord-heater (draft) | 0% (20%) | 30% (20%) | 100% (100%) | 100% (100%) |

## Reading this

- **raw** scores 0% on the prompt by design: the hidden requirements were never typed. Its
  answer score shows what a thin request gets you.
- **v2** (the one-shot rewrite) does worse than raw on answers: it fills gaps by guessing, and
  the guesses contradict the person (15 times) or invent facts (62).
- **quick** (one round of questions, suggested answers first) gets 93% of the hidden
  requirements into the prompt with no made-up purposes, at about 85 words typed.
- **deep** adds rounds; it matters most for technical constraints and image scene details.

## Limits

- The simulated person answers cleanly and cooperatively; real answers are messier.
- 2 runs per arm per task. The skill, the simulated person and the target model are the same
  model family; the grader is a larger model from that family.
- build, change-code and image are scored on the prompt only: running a coding agent or an
  image generator is outside this harness. Research answers have no web access, so prompts
  that demand dated sources score lower on answers than they would with search.
- Headless runs can see the logged-in account's name; the harness scrubs private terms from
  all output before it is saved.

Reproduce: `python3 evals/guided/bench.py OUT_DIR --reps 2` (needs a logged-in `claude` CLI).
Raw run output: `runs/2026-10-06/` (run 1) and `runs/2026-10-07/` (run 2).
