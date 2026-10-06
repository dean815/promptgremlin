---
family: gemini-cli
kind: tool
last_verified: 2026-10-01
sources: [gemini-md, plan-mode]
---
## All models
- There is no official prompting guide for Gemini CLI itself; the model underneath follows the Gemini notes, and only context files and plan mode are documented for the CLI. (hand-written: no official guide)
- Standing rules (style, conventions, do/don't) belong in a `GEMINI.md`, not repeated in every prompt. It loads from `~/.gemini/GEMINI.md` for all projects, from the workspace and its parent directories, and just-in-time from folders the model touches. All found files are concatenated and sent with every prompt. (gemini-md#Understand the context hierarchy)
- Keep each task prompt about this task only: goal, files or directories in scope, what must not change, and how to check it worked. Name the paths; do not make the CLI guess. (hand-written)
- To split a large context file, import others with `@./path.md` lines (relative or absolute). `/memory show` prints what the model actually receives; `/memory reload` rescans after edits. The filename can be changed via `context.fileName` in `settings.json`, a string or list, for example to also read `AGENTS.md`. (gemini-md#Modularize context with imports, #Manage context with the `/memory` command, #Customize the context file name)
- For anything non-trivial, have it plan first: `/plan <goal>` switches to Plan Mode and submits the goal; `gemini --approval-mode=plan` starts in it; Shift+Tab cycles Default, Auto-Edit, Plan. (plan-mode#How to enter Plan Mode)
- Plan Mode is read-only apart from writing Markdown plan files. It researches, discusses the approach, and waits for the user's go-ahead before drafting the formal plan, so write the prompt as a goal plus constraints, not a finished design, and tell it to surface options. (plan-mode#How to use Plan Mode, #Tool Restrictions)
- The user can open the plan with Ctrl+X to edit steps or leave inline comments, then approve with automatic or manual edit acceptance. Do not pre-write the plan file into the prompt. (plan-mode#Collaborative plan editing)
- To steer how it plans for a task type, name the skill to use ("use the migration skill to plan..."). Tool permissions and extra allowed commands are policy files in `~/.gemini/policies/`, set outside the prompt, so never try to grant them in prompt text. (plan-mode#Custom planning with skills, #Custom policies)
- With an auto model, planning routes to a Pro model and implementation after approval to a Flash model; the prompt need not ask for either. (plan-mode#Automatic Model Routing)
- Headless: `gemini --approval-mode plan -p "<prompt>"` runs a plan non-interactively; exiting Plan Mode there switches to YOLO mode, so a headless prompt must state what is off-limits. (plan-mode#Non-interactive execution)
