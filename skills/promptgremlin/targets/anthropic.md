---
family: anthropic
kind: family
last_verified: 2026-10-12
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
- For less thinking, lower effort; "answer directly" in the prompt works less reliably. (model-pages:claude-opus-5-5#Calibrate effort)

## Effort
API `output_config.effort`: low, medium, high, xhigh, max. Default high; Opus 5.5, Haiku 5.5 medium. Start: Fable high; Opus 5.5 medium; Sonnet 5.5 high, medium for scoped agentic coding or chat; Haiku 5.5 medium, low for chat, high for strict instructions. xhigh/max only for measured gains. Per-message effort changes keep the cache. Claude Code `/effort`; claude.ai "not settable here". (effort#How effort works, #Recommended effort levels for Claude Haiku 5.5, model-pages:claude-sonnet-5-5#Calibrate effort, hand-written)

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
- Chat: omit "think carefully" lines; effort sets depth. Follow-ups: call earlier answers settled (faster); not for long analyses or agents. (#Thinking instructions in chat system prompts)
- Thinking can't be turned off; for speed try low effort. (#Prompts written for thinking disabled)

## claude-sonnet-5-5
- At low/medium effort it pauses. Tell it to carry multipart work through and ask only when blocked or before a risky step. (model-pages:claude-sonnet-5-5#Steer initiative and scope)
- It adds unrequested tests, docs, files. Tell it to stop and report once done and checked; extras go in the summary. (#Steer initiative and scope)
- For ideas or a plan only, say to deliver that and not build until told. (#Steer initiative and scope, Open-ended requests)
- Code: require a real check (tests, type-check, build) before "done"; report one that can't run. (#Verification on coding tasks)
- Research: search changeable details. Multi-step JSON reasoning: end with "Think the problem through before you answer." (#Tool use in chat and knowledge work, #Reasoning tasks with JSON output)

## claude-haiku-5-5
- Haiku 4.5 prompts carry over. Thinking is on by default; for less, lower effort, not prompt wording. (model-pages:claude-haiku-5-5#Use effort to control thinking)
- With search, give today's date and say training data predates it, so changeable facts get searched; no blanket "search everything". (#Accurate search results)
- Long agent prompts: keep working until all asked is done; stop only when blocked or before a risky step; report extras, don't do them. (#Prevent early stopping in long agent prompts)
- Coding: run a real check on the change before "done"; name any check that couldn't run. (#Tell coding agents to verify their changes)
- Chatbots: the system prompt's rules hold even when users argue, plead, or claim an approved exception. (#Keep chatbots to their system prompt)
