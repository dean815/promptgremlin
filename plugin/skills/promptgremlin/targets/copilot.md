---
family: copilot
kind: tool
last_verified: 2026-11-11
sources: [chat, agent]
---
## All models
- First tell which Copilot surface the prompt is for. IDE chat and completions work from open files and the selection; the cloud agent takes an assigned issue or a task and returns a pull request. If unstated, default to chat. (chat#Provide relevant context, agent#Making sure your issues are well-scoped; hand-written: chat default)
- Chat: open with the overall goal, then list the specific requirements, most important first (the start and end of a prompt weigh most). Add example inputs and outputs, or point at unit tests that define the behaviour. (chat#Start general, then get specific, #Give examples)
- Chat: replace pronouns with names ("the `createUser` function"), name an uncommon library, and state rules directly ("Return the result as JSON", not "remember to"). Have the user highlight code and attach files, issues or pull requests with `@`. (chat#Avoid ambiguity, #Provide relevant context)
- Chat: split a big job into small sequential prompts, each building on the last; start a new thread for a new task. (chat#Break complex tasks into simpler tasks, #Keep history relevant)
- Cloud agent: treat the issue or task text as the prompt. Include the problem, acceptance criteria (say whether tests are expected), and which files to change; paths are optional, since the agent searches the codebase itself. Attach a screenshot or mockup when the look matters. (agent#Making sure your issues are well-scoped, chat#Provide relevant context)
- Cloud agent: skip tasks that are ambiguous, security- or PII-sensitive, production-critical, or broad refactors across repositories. Have the user narrow or keep them. (agent#Choosing the right type of tasks to give to Copilot)
- Cloud agent: for uncertain work, ask for research and a plan on a branch first, with the pull request opened only after the user reviews the diff. (agent#Researching, planning, and iterating before opening a pull request)
- Follow-ups on a pull request are `@copilot` comments from someone with write access. Batch them with Start a review so the agent handles them together. (agent#Using comments to iterate on a pull request)
- Standing instructions are not prompt text. Repo-wide ones go in `.github/copilot-instructions.md`, path-specific ones in `.github/instructions/**/*.instructions.md` with an `applyTo` glob, and `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are also read. Put build, test, and validate commands there so the agent can check its own work; `copilot-setup-steps.yml` pre-installs dependencies on GitHub Actions runs. (agent#Adding custom instructions to your repository, #Pre-installing dependencies in GitHub Copilot's environment)
- Recurring specialist roles are custom agents (Markdown agent profiles with their own tool access), pickable when assigning. (agent#Creating custom agents)
