# Security policy

## Reporting a vulnerability

Please report security problems privately, not in a public issue. Use GitHub's
private vulnerability reporting: open the repository's **Security** tab and choose
**Report a vulnerability** (a security advisory draft visible only to the maintainer).

Include what you found, how to reproduce it, and what you think the impact is.
You can expect an acknowledgement within a week.

## Scope

In scope:

- **The fetcher** (`skills/promptgremlin/scripts/`): HTTP fetching, the on-disk cache in
  `~/.cache/promptgremlin`, parsing of fetched pages, and the freshness checks. Examples:
  command or path injection, writes outside the cache, unsafe handling of redirects or
  oversized responses.
- **Prompt-injection posture of `SKILL.md`**: pasted user material and fetched vendor text are
  treated as data, never as instructions. A way to make the skill act on instructions
  embedded in either (reveal context or files, call tools, contact anyone) is in scope.
- **Shell handling** in `SKILL.md` (arguments passed to `guidance.py`, the clipboard step).

Out of scope: the accuracy of the guidance notes themselves (they are summaries and can lag
vendors; open a normal issue), and vulnerabilities in the vendors' own sites or in Claude Code.
