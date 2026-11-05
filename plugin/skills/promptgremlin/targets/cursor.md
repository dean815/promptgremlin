---
family: cursor
kind: tool
last_verified: 2026-10-12
sources: [prompting, rules]
---
## All models
- Name the files or folders in scope with `@` references (`@path`, `@Terminals`, `@Chats`, `@Browser`, a git-diff mention) when the user knows them. When they don't, say nothing about location: Agent searches on its own, and a guessed path is worse than none. (prompting#@ mentions)
- For UI work or a visual bug, attach screenshots or mockups and refer to the image in the prompt ("match the attached layout") instead of transcribing an error or design. (prompting#Image input)
- Keep one task per chat. Rules, tool definitions, skills, MCP catalogs, and history share one context window, and older turns get summarised as it fills. For an unrelated task, start a fresh chat; carry over only what is needed, or point at the old thread with `@Chats`. (prompting#Context usage)
- Put the task in the prompt and standing conventions in rules: anything repeated across chats (naming, test commands, "never edit dist/") belongs in a rule file, so say where it goes instead of restating it. Rules live in `.cursor/rules/` as `.mdc` files (subfolders allowed; a plain `.md` there is ignored), in `AGENTS.md` at the root or any subfolder (nested files add to their parents), in User Rules under Customize, or in Team Rules. On conflict, Team beats Project beats User. (rules#Project rules, #Rule file structure, #AGENTS.md, #Format and how Team Rules are applied)
- When drafting a rule file, set its activation on purpose: always on, auto-attached by `globs`, picked by Agent from its `description`, or manual via `@rule-name`. With neither `description` nor `globs`, it applies only when @-mentioned. (rules#Rule anatomy)
- Keep rule text short and concrete; skip style guides and commands Agent already knows, and add a rule only for a repeated mistake. Point at an example file instead of pasting code, saying what to look for. A `@file` in a rule is read on demand, not inlined, so what must always be in context goes in the rule body. (rules#Best practices, #What to avoid in rules, #Referencing files from a rule)
- Rules shape Agent chat only: not Tab completion, and User Rules don't reach inline edit (Cmd/Ctrl+K), so an inline-edit prompt must carry its own constraints. (rules#FAQ)
- For a recurring working style (review checklist, TDD), suggest a skill invoked with `/` and used as a Custom Mode so it stays active across turns. Custom Modes exist only in the Agents Window and the CLI. (prompting#Custom Modes)
- Faster models suit quick edits and exploration, more capable ones multi-file refactors. The user switches in the model picker, so say so outside the prompt text. (prompting#Changing models)
- Say whether Agent should plan first or edit directly, and name the check to run (tests, build, linter). (hand-written: common agent-prompt practice, not stated in these pages)
