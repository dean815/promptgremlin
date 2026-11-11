---
family: grok-bot
kind: tool
last_verified: 2026-11-11
sources: [bots, overview]
---
## All models
- Grok Bot has product docs but no prompting guide; the model underneath is the product's choice (see the xai notes). The rules below are for a durable Bot, not a one-off chat. (hand-written: no official prompting guide; bots, overview)
- A Bot is a named, long-lived agent with its own conversation and memory; all Bots share one persistent cloud computer (browser, filesystem, terminal). Write for an outcome it owns over weeks, not one answer. (overview#What makes Grok Bot different)
- Produce two pieces when the braindump mixes them. A lasting-rules message, phrased "From now on ..." and ending with a request to remember it, holds what stays true: durable preferences, boundaries, responsibilities. An ordinary message holds the task of the moment. Personal Bots have no description any more; only a shared team Bot has one. (bots#Edit a Bot)
- The first message to a new Bot gives its job, its sources, and its approval boundaries, asks it to remember them, then sets a real first task with a clear finish line. (bots#Create a Bot)
- Describe the job in operational terms: what it owns, which inputs it pulls, what it produces, and who consumes it. (hand-written)
- A job needing a long-lived owner gets its own focused Bot; keep the roster small. The primary Bot coordinates the others, so send cross-Bot requests to it. (bots#Create a Bot, #Your primary Bot)
- State approval boundaries as lasting rules: which external actions (messages, account changes, spending) need sign-off. Memory alone is not a safe place for a boundary; back it with approvals or an Auto-review rule. (bots#What a Bot remembers)
- A Bot saves on its own and not always visibly, so anything that must persist gets an explicit "remember that ...". Logins, cards, and contact details go in Vault, not memory. (bots#What a Bot remembers)
- Keep changing facts out of memory. Name the source system and tell the Bot to reopen or cite current data before any consequential decision. (bots#What a Bot remembers)
- Say what the Bot should do when a site blocks automation or needs a human step, such as stop and report. (hand-written)
- A shared template (public link by default, or team-only) shows the Bot's identity, description, skills, and routines, and a Bot may reuse private-chat context in a group chat. Keep keys, internal URLs, and customer data out of anything shared; name what must stay out of group chats. (bots#Share a Bot, #What a Bot remembers)
- A task the Bot is walked through once can be saved as a skill and rerun as a routine, so describe what each run should produce rather than the calendar. A duplicate keeps profile, skills, and routines but not memory or history, so restate the new scope. (overview#What makes Grok Bot different, bots#Organize your roster; hand-written for the phrasing)
