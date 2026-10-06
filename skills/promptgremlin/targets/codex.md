---
family: codex
kind: tool
last_verified: 2026-10-06
sources: [best-practices, prompting]
---
## All models
- Build the prompt from four parts: the goal, the context (files, folders, docs, error text), the constraints, and what "done" means (tests passing, bug no longer reproducing). (best-practices#Strong first use: Context and prompts)
- Point at files: `@path` mentions in the CLI or app; the IDE extension adds open files itself. Spell out any path or line range it won't see. (best-practices#Strong first use, prompting#How to read these examples)
- For a bug, give numbered repro steps and the suspected files; these matter more than a summary. Tell it to reproduce first, then patch, then run checks and report commands and results. (prompting#Fix a bug)
- Name the exact build, test, and lint commands, or it can't check its own work. Ask for tests when needed and a diff review before finishing. (best-practices#Common mistakes, #Improve reliability with testing and review)
- Keep durable rules (repo layout, run/test/lint commands, conventions, do-not rules, definition of done) in AGENTS.md, not in each prompt. The closest file to the working directory wins. Keep it short; `/init` scaffolds one. (best-practices#Make guidance reusable with AGENTS.md)
- For hard or ambiguous work, ask for a plan before editing: `/plan`, or tell it to interview the user first. With Goal mode available, `/goal` sets a persistent goal after the plan. (best-practices#Plan first for difficult tasks, prompting#Prompting Codex)
- State boundaries: what must not change, and what needs approval first. Tight sandbox and approval settings are the default; cloud tasks have no internet unless enabled. (best-practices#Configure Codex for consistency, prompting#Delegate refactor to the cloud)
- One chat per coherent outcome; use git worktrees when parallel tasks touch the same files. A mid-run message steers (Enter in the CLI) or queues for the next turn (Tab). (best-practices#Organize long-running chats, #Common mistakes, prompting#Steering and queuing)
- For review, say the focus (`/review` takes custom instructions; `@codex review` on a GitHub PR). A prompt reused for a repeated job should become a skill. (prompting#Do a local code review, best-practices#Turn repeatable work into skills)
- The model controls and effort labels are in the openai notes. (hand-written: pointer)
