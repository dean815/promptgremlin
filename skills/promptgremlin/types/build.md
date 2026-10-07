---
type: build
default_target: claude-code
---
# build: a new product, app, tool or feature

## Slots
Impact: high = ask in quick mode if not covered; low = deep mode only.

1. **speed** (high): MVP to see it working, or a solid v1 (tests, error
   handling, clean structure)? Suggest from wording: "quick", "prototype",
   "for me", "try" → MVP; "for customers", "production", "team" → solid v1.
2. **stack** (high): analyze the request and suggest a concrete stack
   (platform, language, framework, storage, hosting) with a one-line reason
   tied to the request. Options: the suggestion / a named alternative that
   fits / "your call, simplest that works" / their own. "No preference" →
   receiver picks the simplest stack and says why.
3. **v1 features** (high): offer 4–6 candidate features from the request,
   suggest the 2–3 that make it usable, multi-select. The prompt says to build
   only the features picked; it names as out of scope only what the person
   excluded.
4. **users and data** (high): just me with local data, or accounts and a
   server? Suggest "just me" unless the request mentions others.
5. **done check** (medium): how the person will judge it works (run it, click
   through a flow). Suggest a concrete check from the v1 features.
6. **existing code** (medium): new repo or inside an existing one; what not
   to touch. Suggest "new folder" unless a repo is named.
7. **look and feel** (low): styling, dark mode, accessibility level.
8. **deploy** (low): local only, or deployed where.

## Prompt skeleton
Situation and goal (who it's for, from the brief) → speed mode and what it
means for this run (MVP: thinnest working slice, no tests unless asked;
solid: tests for core logic, error handling) → stack with reasons → v1
features as a checklist, "build only these" → what the person excluded → where to build, what not
to touch → how to verify by running it → when to ask vs decide → done line.

## Type guidance
- Agentic coding prompts work best with scope, verification and a done line
  spelled out; the receiver should run the app, not just write it.
- Say "build only the listed features"; coding agents expand scope when it's
  unstated. Leave unasked details (naming, styling, edge-case rules) to the
  agent, with "decide and note your choice".
- For MVP, say plainly that throwaway structure is fine, so the agent doesn't
  build abstractions; for solid v1, say what quality bar means here.
- Suggest a stack the receiver can actually scaffold in one session.

## Sources (to wire into the freshness engine)
Claude Code best practices (Anthropic), Codex prompting guide (OpenAI),
Cursor rules docs. Vendor target notes already cover wording.
