---
family: gamma
kind: tool
last_verified: 2026-10-12
sources: [agent, api-parameters]
---
## All models
- Two surfaces. The Agent in the Gamma app takes a prompt, may ask questions and show a plan, then builds. The Generate API takes `inputText` plus parameters. Pick one and write for it; do not mix. Default to the Agent if unsure. (agent#Step 1: Start with a prompt; api-parameters#Quick reference)
- Agent: name the mode. Plan (the default) asks a few questions and waits for approval of a plan; Express skips both and drafts at once; Research gathers web sources first and works only with Plan. Mobile browsers start in Express. (agent#Choose how you want to create)
- Agent: a sentence is enough, and more is welcome (pasted notes, attached files, template, connected tools). Cover goal, audience, what matters most, and the story; in Express the prompt is all it gets, so leave none out. If the content is final, say to keep the wording; to skip Plan's questions, say to use its own judgment. (agent#Step 1: Start with a prompt, #Step 2: Answer a few quick questions, #FAQs & Common Issues)
- Agent: the plan fixes story, style, and look, so give enough to set them. Revisions are plain-language edits to named slides; ask for a restyle, not a regeneration, if only the look is wrong. (agent#Step 3: Review the plan, #How do I make changes?, #Can I change the look without starting over?)
- Agent: user-uploaded images (added with the + button before generating) replace automatic image sourcing; say which to use. (agent#Step 1: Start with a prompt)
- API: the prompt is `inputText`, from a few words to long notes, plus `additionalInstructions` (max 5000 chars) for layout, visual style, and tone. Do not let it contradict `textMode`. (api-parameters#inputText, #additionalInstructions)
- API: choose `textMode` per source: `generate` expands brief text, `condense` shortens long text, `preserve` keeps wording. These are parameters, not prompt text. (api-parameters#textMode)
- API: card count and splitting are parameters. `numCards` (default 10) applies only with `cardSplit` set to `auto`; `inputTextBreaks` splits on `\n---\n` in the text and ignores `numCards`. (api-parameters#numCards, #cardSplit)
- API: `format` (presentation, document, social, webpage), `themeId`, `textOptions` (amount, tone, audience, language), and `imageOptions` (source, model, style) are separate fields. Tone and audience matter only in `generate` mode. Image style benefits from a few words for consistency. (api-parameters#format, #textOptions, #imageOptions)
- API: to use only your own images, put long-lived public URLs in `inputText` where they should appear and set `imageOptions.source` to `noImages`. (api-parameters#inputText, #imageOptions)
