---
family: claude-code
kind: tool
last_verified: 2026-11-11
sources: [best-practices]
---
## All models
- Name the file, the symptom, and what "fixed" looks like; add `@path` references, pasted screenshots, or piped command output the user already has. State any preference between reasonable approaches and what not to add ("no new libraries"). (best-practices#Write a specific prompt)
- Point at an existing pattern to copy ("follow HotDogWidget.php") instead of describing the design. Spell out only what Claude can't find by reading the repo: team decisions, the env var a test needs. (best-practices#Write a specific prompt, #Tell Claude what it can't see)
- Claude builds the smallest thing that satisfies a request. For the fuller version say "be ambitious" and list what that covers (empty and error states, edge cases). (best-practices#Write a specific prompt)
- Leave out "think hard", "be thorough", "keep going until done", and IMPORTANT or ALL CAPS: they don't raise effort and lead to over-work or over-applied rules. Depth comes from `/effort` (medium by default here) or `ultrathink` in one message. (best-practices#What you can stop doing, #Change the model and effort)
- Include a pass/fail check Claude can run (named tests, build, linter, fixture diff, screenshot against the mockup) and tell it to keep going until it passes. Ask for evidence (the command and its output), not "all tests pass". (best-practices#Give Claude a check to run)
- For an unattended run, state what done looks like, the check, what it may touch, and where the result goes; a `/goal` condition or Stop hook enforces the check. (best-practices#Let Claude run without you, #Give Claude a check to run)
- For an unclear feature, tell it to interview the user until it could write the spec, then write it to a file; the build starts from that spec in a fresh session. (best-practices#Brainstorm with Claude first)
- Ask for review in a fresh subagent against the spec, reporting only gaps that affect correctness and skipping style, so it doesn't push over-engineering. (best-practices#Review against your spec)
- Ask for subagents only for parallel work, noisy output, or independent review, with short summaries back; delegating doesn't improve the answer. (best-practices#Know what subagents cost)
- If the prompt will live in CLAUDE.md, keep only lines Claude can't work out from the code. A line it keeps skipping needs a shorter file, not emphasis; if it must happen every time, say to make it a hook or deny rule. (best-practices#Keep CLAUDE.md short, #Enforce the rules that can't have exceptions)
- If the user already corrected Claude twice on one problem, the prompt should be a fresh restart that folds in what was learned (the user runs `/clear` first). (best-practices#Steer the session)
