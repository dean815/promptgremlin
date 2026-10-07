# Guided benchmark results

7 tasks, 2 runs per arm. Skill and simulated person on claude-sonnet-5-5; answers by claude-sonnet-5-5; grader claude-opus-5-5. The simulated person answers only from a hidden intent sheet. Arms: raw = request as typed; v2 = one-shot rewrite; quick / deep = v3 interview.

| Arm | Intent in final prompt | Contradicted | Invented facts | Intent met by answer | Rounds | Questions | Words typed | Failed runs |
|---|---|---|---|---|---|---|---|---|
| raw | 0% | 0 | 0 | 23% | 0.0 | 0.0 | 0.0 | 0 |
| v2 | 30% | 12 | 70 | 17% | 0.0 | 0.0 | 0.0 | 0 |
| quick | 92% | 0 | 28 | 89% | 1.0 | 6.8 | 83.2 | 1 |
| deep | 99% | 0 | 29 | 88% | 2.2 | 12.7 | 125.4 | 0 |

Per task, intent in final prompt (and met by answer):

| Task | raw | v2 | quick | deep |
|---|---|---|---|---|
| habit-tracker (build) | 0% | 14% | 100% | 100% |
| slow-csv-export (change-code) | 0% | 61% | 50% | 100% |
| vector-db-research (research) | 0% (0%) | 0% (0%) | 100% (89%) | 100% (89%) |
| churn-analysis (analyze-data) | 0% (62%) | 44% (50%) | 100% (75%) | 100% (78%) |
| workspaces-prd (product-doc) | 0% (0%) | 0% (0%) | 100% (88%) | 100% (89%) |
| coffee-instagram (image) | 0% | 39% | 100% | 94% |
| landlord-heater (draft) | 0% (20%) | 30% (20%) | 100% (100%) | 100% (90%) |
