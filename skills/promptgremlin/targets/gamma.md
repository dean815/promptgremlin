---
family: gamma
kind: tool
last_verified: 2026-10-05
sources: [agent, api-parameters]
---
## All models
- Two surfaces. The Agent in the Gamma app takes a prompt, asks a few questions, shows a plan, then builds. The Generate API takes `inputText` plus parameters. Pick one and write for it; do not mix. Default to the Agent if unsure. (agent#Step 1: Start with a prompt; api-parameters#Quick reference)
- Agent: a sentence is enough, and more is welcome (pasted notes, attached files, template). Cover goal, audience, what matters most, and the story. If the content is final, say "use this text as-is"; to skip its questions, say to decide for itself. (agent#Step 1, #Step 2, #FAQs & Common Issues)
- Agent: the plan step decides the story and look, so the prompt should have enough to fix them. Revisions are plain-language edits to named slides; ask for a restyle, not a regeneration, if only the look is wrong. (agent#Step 3: Review the plan, #How do I make changes?)
- Agent: user-uploaded images (added with the + button before generating) replace automatic image sourcing; say which to use. (agent#Step 1)
- API: the prompt is `inputText`, from a few words to long notes, plus `additionalInstructions` (max 5000 chars) for layout, visual style, and tone. Do not let it contradict `textMode`. (api-parameters#inputText, #additionalInstructions)
- API: choose `textMode` per source: `generate` expands brief text, `condense` shortens long text, `preserve` keeps wording. These are parameters, not prompt text. (api-parameters#textMode)
- API: card count and splitting are parameters. `numCards` (default 10) applies only with `cardSplit` set to `auto`; `inputTextBreaks` splits on `\n---\n` in the text and ignores `numCards`. (api-parameters#numCards, #cardSplit)
- API: `format` (presentation, document, social, webpage), `themeId`, `textOptions` (amount, tone, audience, language), and `imageOptions` (source, model, style) are separate fields. Tone and audience matter only in `generate` mode. Image style benefits from a few words for consistency. (api-parameters#format, #textOptions, #imageOptions)
- API: to use only your own images, put long-lived public URLs in `inputText` where they should appear and set `imageOptions.source` to `noImages`. (api-parameters#inputText, #imageOptions)
