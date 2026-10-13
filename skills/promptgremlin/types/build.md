---
type: build
default_target: claude-code
---
# build: a new product, app, tool or feature

## Slots
Impact: high = ask in quick mode if not covered; low = deep mode only.

1. **speed** (high): MVP to see it working, or a solid v1 (tests, error
   handling, clean structure)? Scale the suggestion to the wording. Thin
   words ("quick", "prototype", "try", "MVP", "spike") → MVP. Ambition wins
   over those, and over "for me": "clone", "identical", "parity", "match X",
   "for customers", "production", "team", "solid" → solid v1. "for me" with
   no ambition word → MVP.
2. **stack** (high): analyze the request and suggest a concrete stack
   (platform, language, framework, storage, hosting) with a one-line reason
   tied to the request. Options: the suggestion / a named alternative that
   fits / "your call, simplest that works" / their own. "No preference" →
   receiver picks the simplest stack and says why.
3. **v1 features** (high): offer 4–6 candidate features from the request,
   multi-select. Scale the suggestion to the wording. "clone X", "identical
   to X", "parity", "match X", "the full X" → suggest the full feature set,
   every area listed. Thin words ("quick", "prototype", "MVP", "just the
   core") → suggest the 2–3 that make it usable. When the wording says
   neither, suggest those 2–3. The prompt says to build only the features
   picked; it names as out of scope only what the person excluded.
4. **users and data** (high): just me with local data, or accounts and a
   server? Suggest "just me" unless the request mentions others.
5. **run length** (high): one sitting that stops when the checklist is done,
   or a long run (maximize tokens, a named budget, overnight, "as long as it
   takes")? Suggest one sitting unless the request already asks for a long
   run; those words cover the slot, so don't ask again. In quick mode, when
   tokens, a budget, overnight, or keeping going is mentioned and the length
   is still open, ask this before users and data.
6. **done check** (medium): how the person will judge it works (run it, click
   through a flow). Suggest a concrete check from the v1 features.
7. **existing code** (medium): new repo or inside an existing one; what not
   to touch. Suggest "new folder" unless a repo is named.
8. **look and feel** (low): styling, dark mode, accessibility level.
9. **deploy** (low): local only, or deployed where.

## Prompt skeleton
Situation and goal (who it's for, from the brief) → speed mode and what it
means for this run (MVP: thinnest working slice, no tests unless asked;
solid: tests for core logic, error handling) → stack with reasons → v1
features as a checklist, "build only these" → what the person excluded →
run length → where to build, what not to touch → how to verify by running
it → when to ask vs decide → when the answer is a long run, a stretch phase
after the checklist (the checklist is the first phase, not the stop: keep
going on the same product until the length or budget is used) → done line.
With a stretch phase, the done line is the end of that phase; otherwise it
is the checklist.

## Type guidance
- Agentic coding prompts work best with scope, verification and a done line
  spelled out; the receiver should run the app, not just write it.
- Say "build only the listed features"; coding agents expand scope when it's
  unstated. Leave unasked details (naming, styling, edge-case rules) to the
  agent, with "decide and note your choice".
- For MVP, say plainly that throwaway structure is fine, so the agent doesn't
  build abstractions; for solid v1, say what quality bar means here.
- Suggest a stack the receiver can actually scaffold in one session.
- Scale both suggestions to the request. A "clone X" or "identical to X"
  request suggests the full feature set and a solid v1.
- A long run answer gets a stretch phase after the checklist. Finish the
  listed features first, then keep going on that same product (edge cases,
  failure states, polish, and tests that fit the finish level) until the
  length or budget is used. Stay inside the features they picked, and don't
  build what they excluded. Name the early stop to avoid: ending when the
  list is checked off.

## Sources
Watched through the target's own notes: Claude Code, Codex, Cursor and Copilot best-practice pages (run for whichever target the prompt is for).
