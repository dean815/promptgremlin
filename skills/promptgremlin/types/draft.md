---
type: draft
default_target: claude-ai
---
# draft: prose a person will send or publish

## Slots
1. **facts** (high): the specifics only the person knows (names, dates,
   numbers, what happened). Ask for them directly; never invent. If the
   person gives none, the prompt tells the receiver to ask for them first.
2. **reader and relationship** (high): who reads it and how the person stands
   with them.
3. **point and ask** (high): what the reader should know or do after reading.
4. **tone and voice** (medium): tone words, or a sample of the person's
   writing to match. Suggest from the relationship.
5. **length and channel** (medium): email, LinkedIn, Slack, letter; word limit.
6. **must not** (medium): things not to say, promise, or threaten.

## Prompt skeleton
Situation and relationship → the facts, as given → the point and the ask →
tone and voice → length and channel → must-nots → human-voice rules → stop
line (the draft only).

Human-voice rules to include, adapted to the channel: plain words, mixed
sentence lengths, specific details over general claims, no stock AI phrasing
(for example "I hope this finds you well", "delve", "navigate", "in today's
fast-paced world", "game-changer", "I wanted to reach out"), no tidy
three-item lists, no em-dashes, no closing summary of what was just said.

## Hand-off
Always add an **edit pass** after the prompt:
1. A ready-to-paste prompt: "Edit this draft to sound like a person wrote it.
   Remove stock AI phrasing, filler openers and closers, tidy lists of three,
   em-dashes, and vague claims. Keep every fact and the length. Return only
   the edited draft."
2. A short checklist for the person: rewrite the first and last lines in your
   own words; check every fact; read it aloud once.

## Sources
Wikipedia "Signs of AI writing" (for the AI-tells list); vendor writing
guidance.
