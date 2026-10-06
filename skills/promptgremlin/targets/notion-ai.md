---
family: notion-ai
kind: tool
last_verified: 2026-10-01
sources: [custom-agent]
---
## All models
- The only fetchable source covers building Custom Agents. It says nothing about one-off asks in Notion's chat or page AI, so treat those as lighter versions of the same rules. (custom-agent; hand-written: one-off asks)
- First decide which this is. A Custom Agent is a standing automation, with instructions, triggers, and tool access, shared with a team. A one-off ask runs once and has none of those. Do not write trigger or schedule language into a one-off. (custom-agent#Identify a workflow your Custom Agent can automate; hand-written: one-off distinction)
- For an agent, write the instructions as a goal and outcome, not every step. Say precisely when and where it acts (a named channel plus the kind of request that triggers it), not a general "whenever someone asks". (custom-agent#How to build a Custom Agent)
- Name the pages, databases, and people in scope with @mentions rather than vague phrases like "our docs". For a one-off, do the same. (custom-agent#How to build a Custom Agent)
- Spell out branching in if-this-then-that form: what to do when the answer exists, when it does not, and who gets escalated items. State where output goes. (custom-agent#Review your Custom Agent instructions, #How to build a Custom Agent)
- Give a short example of a good response and one to avoid, to set style. Set boundaries: which existing page to update instead of creating new ones, and which channels it must stay out of. (custom-agent#How to build a Custom Agent)
- Triggers are configured outside the prose: an @mention, a new database page, a Slack message, or a schedule like Monday morning. Name the intended trigger in a note to the user, not as an instruction line. (custom-agent#Add event-based or scheduled triggers)
- Access is granted in the Tools and access section, view-only unless it must edit. Do not write "you have access to X" in the prompt; tell the user to grant it. (custom-agent#Connect tools and check that your Custom Agent has access to them)
- Tell the user to run it manually and test in a safe channel or database before enabling triggers, and to check the Activity tab when output is off. Fix instructions against what it did, not what was intended. (custom-agent#Safely test, iterate, and revert changes if needed)
