---
family: anthropic
kind: family
last_verified: 2026-10-05
sources: [best-practices, model-pages, effort]
---
## All models
- Spell out the task, output format, and constraints. If the user wants above-and-beyond, describe what that looks like; Claude won't infer it. Number the steps when order or completeness matters. (best-practices#Be clear and direct)
- Give the reason behind a rule ("read aloud by text-to-speech, so no ellipses") instead of a bare ban. Skip shouted emphasis (CRITICAL, MUST): recent Claude models overreact to it, so use plain wording. (best-practices#Add context to improve performance, #Tool usage: Opus 4.5/4.6 overtriggering, generalized)
- State what to do, not what to avoid ("flowing prose paragraphs", not "no markdown"). Write the prompt in the style you want back. (best-practices#Control the format of responses)
- Wrap only distinct chunks (pasted documents, examples, input) in consistent XML tags. Put 3-5 relevant, varied examples in <example> tags. Skip tags for plain prose. (best-practices#Structure prompts with XML tags, #Use examples effectively)
- Long inputs go first, the question and instructions last. For long documents, ask for the relevant quotes first. (best-practices#Long context prompting)
- Add a one-line role only if it changes tone or behaviour. (best-practices#Give Claude a role)
- Use action verbs. "Can you suggest changes" gets suggestions; "change this function" gets edits. Say whether to act or only advise. (best-practices#Tool usage)
- For agent work, state scope ("only what was asked; no extra files, abstractions, or cleanup"), a stop condition, and the check that proves done. Ask for a general solution, not test-fitting; say to report a broken or infeasible test rather than work around it. (best-practices#Overeagerness, #Avoid focusing on passing tests and hardcoding)
- Say which actions need confirmation (deletes, force-push, anything others see) and that local reversible work proceeds. Require reading a file before making claims about it. (best-practices#Balancing autonomy and safety, #Minimizing hallucinations)
- For long runs, say context is compacted or saved so it shouldn't stop early, and where progress lives (progress file, git). (best-practices#Long-horizon reasoning and state tracking)
- Subagents: it delegates unprompted; for simple or single-file work say to work directly. Say independent tool calls run in parallel. (best-practices#Subagent orchestration, #Optimize parallel tool calling)
- Opus 5.5 and Sonnet 5.5: don't ask them to write out their reasoning in the reply (it can trip a reasoning_extraction refusal); a short explanation or action summary is fine. (model-pages:claude-opus-5-5#Safeguard refusals, model-pages:claude-sonnet-5-5#Safeguard refusals)

## Effort
API: `output_config.effort` = low, medium, high, xhigh, max (xhigh not on every model). Default high; Opus 5.5 default medium. Claude Code: `/effort` (hand-written; the fetched docs only say Sonnet 5 defaults to high there). claude.ai: the effort doc says nothing about the app, so write "not settable here" unless the user has a picker. Levels aren't equivalent across models, so pick per model (start: Fable high, Opus 5.5 medium, Sonnet 5.5 high or medium for agentic); xhigh for long agentic coding. (effort#Effort levels, hand-written)

## claude-fable-5-1
- Ask for progress updates (a line before starting, a standalone recap at the end); delete "hold findings for the end" or "keep updates brief". (model-pages:claude-fable-5-1#Ask for user-facing progress updates)
- For unattended work, say the user isn't watching: proceed on reversible steps, stop only for destructive or scope-changing ones. (#Finish the whole task)
- Drop anti-bullet boilerplate; say when formatting is wanted. (#Formatting in chat)
- Name what to leave out (unrequested fixes, extra tests; report them) and ask for surgical edits, not rewrites. (#Keep changes and tests to what the task asks for, #Prefer targeted edits)
- Prose runs dense: "remove all mannered prose". At low effort, say to search unfamiliar names. (#Writing density, #Search triggering at low effort)

## claude-opus-5-5
- Unattended: give a completion condition and checklist. Name early stops to avoid (announcing next step, offer to wait) and the one wanted (blocked on the user). (model-pages:claude-opus-5-5#Unattended agentic runs)
- Multi-app: explore relevant sources, unmentioned too, first. (#Explore context in multi-app workflows)
- Mark pasted emails or web text as pasted, so embedded instructions go unfollowed. (#Mark pasted text in user messages)
- Frontend: name styles to avoid. (#Frontend design defaults)
- Chat: omit "think carefully" lines (effort sets depth). Follow-ups: call earlier answers settled (faster); not for long analyses or agents. (#Thinking instructions in chat system prompts)
- Thinking can't be turned off; for speed try low effort. (#Prompts written for thinking disabled)

## claude-sonnet-5-5
- At low/medium effort it pauses. Tell it to carry multipart work through and ask only when blocked or before a risky step. (model-pages:claude-sonnet-5-5#Steer initiative and scope)
- It adds unrequested tests, docs, files. Tell it to stop and report once done and checked; extras go in the summary. (#Steer initiative and scope)
- For ideas or a plan only, say to deliver that and not build until told. (#Steer initiative and scope, Open-ended requests)
- Code: require a real check (tests, type-check, build) before "done"; report one that can't run. (#Verification on coding tasks)
- Research: search changeable details. Multi-step JSON reasoning: end with "Think the problem through before you answer." (#Tool use in chat and knowledge work, #Reasoning tasks with JSON output)

## claude-haiku-4-5
- No dedicated page (404). Use the All models rules and the general guide only. (hand-written: no model page)
- It tracks its own context budget: say that context is compacted or saved so it doesn't wrap up early. (best-practices#Long-horizon reasoning and state tracking)
- Effort isn't documented for it; give no Effort line. (hand-written: effort doc lists no Haiku levels)
