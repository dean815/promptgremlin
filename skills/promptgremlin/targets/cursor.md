---
family: cursor
kind: tool
last_verified: 2026-10-01
sources: [prompting, rules]
---
## All models
- Name the files, folders, or symbols in scope with `@` references (`@path`, `@Terminals`, `@Chats`, a git-diff mention) when the user knows them. When they don't, say nothing about location: Agent searches the codebase itself, and a guessed path is worse than none. (prompting#@ mentions)
- Tell the writer to attach screenshots or mockups when the task is UI work or a visual bug, and to refer to the image in the prompt ("match the attached layout") rather than transcribing an error or design by hand. (prompting#Image input)
- Keep one task per chat. Context is a fixed window shared by rules, tool definitions, skills, MCP catalogs, and history, and old turns get summarised once it fills. For an unrelated task, the prompt is a fresh chat; carry over only what is needed, or point at the old thread with `@Chats`. (prompting#Context usage)
- Put the task in the prompt and the standing conventions in rules. Anything the user has repeated across chats (naming, test commands, "never edit dist/") belongs in a rule file, so say where it goes instead of restating it in every prompt. Rules live in `.cursor/rules/*.mdc` (must be `.mdc`; a plain `.md` there is ignored), in `AGENTS.md` at the root or a subfolder, in User Rules under Customize, or in Team Rules from the dashboard. (rules#Project rules, #Rule file structure, #AGENTS.md)
- If you are drafting a rule file, set its activation deliberately: always on, auto-attached by `globs`, chosen by Agent from its `description`, or manual via `@rule-name`. A rule with no `description` and no `globs` is only applied when @-mentioned. (rules#Rule anatomy)
- Rule text should be short, concrete, and point at an example file instead of pasting code. Skip style-guide copies and command lists Agent already knows; add a rule only for a mistake it keeps repeating. (rules#Best practices, #What to avoid in rules)
- Rules shape Agent chat only. They do not affect Tab completion, and User Rules are not applied to inline edit (Cmd/Ctrl+K), so an inline-edit prompt must carry its own constraints. (rules#FAQ)
- For a recurring working style (review checklist, TDD), suggest a skill invoked with `/` and used as a Custom Mode so it stays active across turns, rather than pasting the checklist each time. Custom Modes exist only in the Agents Window and the CLI, not the editor chat. (prompting#Custom Modes)
- Match the task to a model: a faster one for quick edits and exploration, a more capable one for multi-file refactors. The user switches in the model picker, so say so outside the prompt text. (prompting#Changing models)
- Say whether Agent should plan first or edit directly, and name the check to run (tests, build, linter). (hand-written: common agent-prompt practice, not stated in these pages)
