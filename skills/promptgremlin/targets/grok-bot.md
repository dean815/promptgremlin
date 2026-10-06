---
family: grok-bot
kind: tool
last_verified: 2026-10-05
sources: [bots, overview]
---
## All models
- Grok Bot has product docs but no prompting guide; the model underneath is the product's choice (see the xai notes). These rules cover writing for a durable Bot rather than a one-off chat. (hand-written: no official prompting guide; bots, overview)
- A Bot is a named, long-lived agent with its own conversation and memory that runs on a persistent cloud computer (browser, filesystem, terminal) and keeps working with your laptop closed. Write for an owner of an outcome over weeks, not for a single answer. (overview#What makes Grok Bot different)
- Produce two pieces when the braindump mixes them. The Bot description (set from the Bot menu or Edit Profile) holds rules that stay true: durable preferences, boundaries, responsibilities. The message in the conversation holds the task of the moment. (bots#Edit a Bot)
- Describe the job in operational terms: what it owns, which inputs it pulls, what it produces, and who consumes the output. Name it for a specific job, because a vague "helper" role gives it little to work with. (bots#Give each Bot a clear job)
- If the braindump spans different goals, tools or sources, working styles, approval boundaries, or schedules, recommend separate Bots, and keep the roster as small as the work allows. (bots#Give each Bot a clear job, #Organize a team of Bots)
- Write approval boundaries explicitly into the description: which external actions (messages, account changes, spending) need sign-off first. Memory is not a safe place for a boundary. (bots#What a Bot remembers, #Organize a team of Bots)
- Keep changing facts out of the description. Name the source system instead, and tell the Bot to reopen current data before any consequential decision. (bots#What a Bot remembers)
- A good first message gives a real task across a few tools: what to do, where to work, what context to pull, and what finished looks like. (overview#A good first handoff)
- Some sites block automation or need a human step, and the Bot hands those back to you. Say what it should do at that point, for example stop and report, rather than leaving it to improvise. (overview#FAQ; hand-written for the instruction)
- All your Bots share one computer, files, and logins, and a shared template exposes the description, skills, and routines. Never put keys, internal URLs, or customer data in either. (overview#Your Bots share one computer, bots#Share a Bot)
- A recurring schedule or a repeatable path is saved as a skill or routine after the Bot has done it once, so describe what each run should produce rather than the calendar. A duplicate Bot keeps the profile and routines but not memory, so restate the new scope. (overview#What makes Grok Bot different, bots#Duplicate a Bot; hand-written for the phrasing)
