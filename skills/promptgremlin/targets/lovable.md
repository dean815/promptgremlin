---
family: lovable
kind: tool
last_verified: 2026-10-01
sources: [prompting]
---
## All models
- Before drafting, the writer should be able to state four things: what is being built, who it is for, why they would use it, and the one key action. If the braindump lacks them, ask or invent plain placeholders and flag them; vague direction yields vague output. (prompting#Plan before you prompt)
- Scope by component, not page. Prompt for one block (hero, pricing table, filter dropdown), then review before the next. A full-page prompt produces noise. For a first prompt on a new app, say it is a foundation pass and list what is deliberately not included yet. (prompting#Prompt by component, not page; hand-written: the not-included list)
- Name the stack and the visible result. State framework or backend preferences if they matter, and describe what should be on screen when done: sections in order, the main call to action, and the states (logged in or out, empty, loading, error). (prompting#Build with the backend in mind; hand-written: stack naming)
- Write the real copy: actual headlines, button labels, and sample data, not lorem ipsum. Real words expose layout problems early. (prompting#Design with real content)
- Use small UI nouns (tab bar, chip, dropdown, toast, toggle) rather than "a settings screen". Build one element first, then layer states and interactions on it. (prompting#Speak atomic: buttons, cards, modals)
- Set the look with opinionated adjectives and concrete properties: mood words plus type, spacing, colour, radius, motion. Specific, opinionated wording beats generic words like "colourful". Say the style once per section, and tell the user to save a settled style in project knowledge instead of restating it. (prompting#Use buzzwords to dial in aesthetic, #Get the design right first; hand-written: the contrast example)
- For any change to existing work, give three parts: what to build, where it goes, and what must stay untouched ("only the orders page", "keep the styling", "leave login alone"). (prompting#Say what to change and what to leave alone)
- Layout prompts follow header, content, action order, with visual parts listed in sequence and styled. For a one-element tweak, suggest the preview toolbar and use verbs like replace, update, adjust. (prompting#Use prompt patterns for layouts, #Point at elements with the preview toolbar)
- For a vague or large feature, end the prompt by inviting Lovable to ask whatever questions it needs, and suggest Plan mode. (prompting#Make Lovable ask clarifying questions)
- One meaningful change per prompt; the user bookmarks working versions in version history before risky changes. That is a UI habit, not prompt text. (prompting#Iterate with version history)
