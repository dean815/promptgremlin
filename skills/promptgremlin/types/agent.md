---
type: agent
default_target: claude-code
---
# agent: standing instructions, automations, system prompts

## Slots
1. **trigger** (high): when it runs (schedule, event, on demand).
2. **scope and account** (high): which workspace, team, repo or inbox it acts
   in. Never guess an account.
3. **permissions** (high): read-only, or what it may write, send or change.
   Suggest read-only.
4. **output** (high): what it produces and where it goes.
5. **failure** (medium): what to do when a source is down or data is missing.
6. **escalation** (low): when to stop and ask a person.

## Prompt skeleton
Role only if it changes behaviour → what to do each run → scope and account →
permissions with reasons from the brief → output and destination → failure
behaviour → stop condition per run.

## Type guidance
- State permissions positively and narrowly; list forbidden actions.
- Give the failure behaviour; agents improvise when a source is down.

## Sources
Vendor agent and system-prompt guidance (target notes).
