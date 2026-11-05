---
family: replit
kind: tool
last_verified: 2026-10-01
sources: [prompting]
---
## All models
- Plan before prompting: split the goal into ordered stages (structure, core logic, storage, extras) and write the prompt for the first stage only, listing later stages as "next". A single "build everything" prompt is the main thing to avoid. (prompting#Plan first, #Build incrementally)
- Be specific about outputs: pages and routes, fields with required and format rules, where submitted data goes, and edge cases. Name the exact element, effect, and timing for visual changes. (prompting#Be specific)
- State what you want, not what to avoid. Rewrite any "don't make it X" as the positive design or behaviour. (prompting#Use positive language)
- Use plain, short sentences; break complex asks into bullets. Drop formal phrasing that sounds architectural. (prompting#Keep it simple)
- State the stack and the visible result explicitly (for example a full-stack app with auth and a database, and what the first screen shows), and what is out of scope this round. (hand-written: stack and out-of-scope lines; the source covers incremental scoping)
- Mention specific files, not the whole project, and attach mockups, screenshots, or sample data when appearance matters. Do not attach everything. (prompting#Provide relevant files, #Show examples)
- For a bug, include the exact error text, the relevant snippet, the file, what the user was trying to do, and what they already tried. (prompting#Debugging effectively)
- For an open choice (payments, library), the prompt should ask Agent to compare options and tradeoffs first rather than build one; the user turns on Plan mode for this. (prompting#Ask for guidance)
- Start a new chat when the topic changes. Checkpoints save progress after each working step so the user can roll back; that is a Replit control, not prompt text. (prompting#Provide relevant files [new chat]; prompting#Build incrementally [Checkpoints])
- When a result is off, the next prompt adds detail, an example, or a simpler restatement, not a repeat. (prompting#Iterate on your prompts)
