---
family: claude-code
kind: tool
last_verified: 2026-10-06
sources: [best-practices]
---
## All models
- Name the files, directories, or functions in scope, with `@path` references where the user has them. Say what not to touch or create; "scope the task" cuts corrections. (best-practices#Provide specific context in your prompts, #Provide rich content)
- Point at an existing pattern to copy ("follow HotDogWidget.php") instead of describing the design; for a "why is it like this" question, name the source to read (e.g. git history). For a bug, give the symptom, the likely location, and what "fixed" looks like. (best-practices#Provide specific context in your prompts)
- Include a check Claude can run (named tests, build, linter, screenshot diff) and tell it to iterate until it passes. Ask for evidence (test output, the command and its result), not "it works". Fix root causes; don't suppress the error. (best-practices#Give Claude a way to verify its work)
- Verify against real behaviour, not only unit tests. For an unattended run, say the stop condition is that check passing; a `/goal` condition can enforce that across a session. (best-practices#Give Claude a way to verify its work)
- Say whether to ask or proceed. For an unclear or large feature, tell it to interview the user with the AskUserQuestion tool, then write a spec to a file. (best-practices#Let Claude interview you)
- For multi-file or unfamiliar-code changes, ask for a plan before edits, with edits starting after approval. Skip planning when the diff fits in one sentence: say "do it directly". (best-practices#Explore first, then plan, then code)
- Scope any investigation ("look in src/auth/ for token refresh") or send it to a subagent, so exploration doesn't fill the context. Never write an open-ended "investigate X". (best-practices#Use subagents for investigation, #Avoid common failure patterns)
- Ask for review in a fresh subagent against named criteria, and tell it to flag only gaps that affect correctness or the stated requirements, so it doesn't push over-engineering. (best-practices#Add an adversarial review step)
- If the prompt will live in CLAUDE.md, keep each line one Claude can't infer from the code; add IMPORTANT to a single line it keeps skipping, not many. If it must happen every time, say to make it a hook. (best-practices#Write an effective CLAUDE.md, #Set up hooks)
- If the user already corrected Claude twice on one problem, the prompt should be a fresh restart that folds in what was learned (the user runs `/clear` first). Say if it should commit and open a PR when done. (best-practices#Course-correct early and often)
