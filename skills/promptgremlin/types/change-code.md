---
type: change-code
default_target: claude-code
---
# change-code: fix, speed up, refactor or migrate existing code

## Slots
1. **where** (high): repo, files, entry point. Suggest from paths or code
   pasted; "no preference" isn't allowed, ask again if missing.
2. **symptom** (high): what's wrong and how to reproduce or measure it
   (error, input size, timing). Suggest from the request's wording.
3. **must not change** (high): public API or function signature, output
   format, dependencies, behaviour other code relies on. Suggest "keep the
   signature and output identical".
4. **change size** (high): minimal targeted fix, or free to refactor?
   Suggest minimal.
5. **verify** (medium): tests to run, a benchmark, or a manual check.
   Suggest the existing tests if any are visible.
6. **ask first** (medium): actions that need a check-in (new dependency,
   deleting files, migrations, touching other modules).
7. **environment** (low): language version, platform, constraints such as
   memory or row counts.

## Prompt skeleton
What's wrong and where (symptom, reproduction) → suspected cause only if the
person named one → constraints that must hold, with reasons from the brief →
change size → verification steps → ask-first list → done line.

## Type guidance
- Give the reproduction and the measurement; agents fix the wrong thing when
  "slow" or "broken" isn't pinned down.
- Say what must stay identical; refactors drift public behaviour.
- Tell the agent not to change tests to make them pass.

## Sources
Claude Code best practices (Anthropic), Codex prompting guide (OpenAI).
