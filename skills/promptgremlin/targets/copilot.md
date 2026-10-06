---
family: copilot
kind: tool
last_verified: 2026-10-01
sources: [chat, agent]
---
## All models
- First tell which Copilot surface the prompt is for, because the guidance differs. IDE chat and inline suggestions work from open files and the selection; the cloud agent takes an assigned issue or a task and returns a pull request. If unstated, default to chat. (chat#Indicate relevant code, agent#Making sure your issues are well-scoped; hand-written: chat default)
- Chat: open with the overall goal in a sentence, then list the specific requirements beneath it. Add example inputs and outputs, or point at unit tests that define the behaviour. (chat#Start general, then get specific, #Give examples)
- Chat: replace pronouns with names ("the `createUser` function", "the code in your last response"), and name the library or put the import in view if it is uncommon. Have the user highlight code or open the file, and use `@workspace` (VS Code) or `@project` (JetBrains) for wider context. (chat#Avoid ambiguity, #Indicate relevant code)
- Chat: split a big job into small sequential prompts, each building on the last; start a new thread for a new task so stale history does not leak in. (chat#Break complex tasks into simpler tasks, #Keep history relevant)
- Cloud agent: treat the issue or task text as the prompt. Include the problem, acceptance criteria (say whether tests are expected), and which files to change. File paths help but are optional, since the agent can search the codebase itself. (agent#Making sure your issues are well-scoped)
- Cloud agent: skip tasks that are ambiguous, security- or PII-sensitive, production-critical, or broad refactors across repositories. Tell the user to narrow or keep them. (agent#Choosing the right type of tasks to give to Copilot)
- Cloud agent: for uncertain work, the prompt should ask for research and a plan on a branch first, with the pull request opened only after the user reviews the diff. (agent#Researching, planning, and iterating before opening a pull request)
- Follow-ups on a pull request are `@copilot` comments from someone with write access. Batch them with Start a review so the agent handles them together. (agent#Using comments to iterate on a pull request)
- Standing instructions are not prompt text. Repo-wide ones go in `.github/copilot-instructions.md`, path-specific ones in `.github/instructions/**/*.instructions.md` with an `applyTo` glob, and `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are also read. Put build, test, and validate commands there so the agent can check its own work; `copilot-setup-steps.yml` pre-installs dependencies. (agent#Adding custom instructions to your repository, #Pre-installing dependencies in GitHub Copilot's environment)
- Recurring specialist roles are custom agents (Markdown agent profiles with their own tool access), pickable when assigning. (agent#Creating custom agents)
