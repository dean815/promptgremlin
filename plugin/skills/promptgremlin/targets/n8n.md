---
family: n8n
kind: tool
last_verified: 2026-10-01
sources: [tools-agent]
---
## All models
- n8n's docs say little about prompt craft. The only fetchable page is the Tools Agent node reference, which describes fields, not wording, so most of this is node placement. (hand-written: thin docs; tools-agent for the fields below)
- Decide where each piece goes. Standing guidance for the agent (role, decision rules, tool-use rules, tone) goes in the System Message option. The per-run task or user query goes in the Prompt (User Message) field, either static text or an expression, or comes from `chatInput` on the previous node. Return the prompt as two labelled pieces. (tools-agent#System Message, #Prompt)
- System Message is for steering decisions: when to use which connected tool, what to do if none fits, when to stop. Do not paste tool descriptions; name what each tool is for in a line each. (tools-agent#System Message; hand-written: do not duplicate tool descriptions)
- Dynamic data enters the user prompt with expressions that pull from earlier nodes, not by pasting sample values. Name the field the expression reads. (tools-agent#Prompt; hand-written: field naming)
- Output shape is a node setting, not prompt prose. Require Specific Output Format connects an output parser (auto-fixing, item list, or structured), and the prompt then only needs to describe the fields' meaning. (tools-agent#Require Specific Output Format)
- Tool parameters filled by the model use `$fromAI()` in the tool node; the prompt should say what values the model can reasonably infer, not duplicate the schema. (tools-agent#Dynamic parameters for tools with `$fromAI()`)
- For sending, modifying, or deleting actions, suggest the Human review step on that tool instead of a "ask before acting" line. (tools-agent#Human review for tool calls)
- Max Iterations (default 10) caps agent runs; if the task needs more steps, tell the user to raise it rather than adding "keep trying". (tools-agent#Max Iterations)
