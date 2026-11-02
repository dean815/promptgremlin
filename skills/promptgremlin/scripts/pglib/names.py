"""Map the model names each data source uses onto our canonical model ids.

Shared by the snapshot builder (CI, joining sources) and the skill (LiveBench names).
"""
import re

from .lineup import norm_id

EFFORTS = "minimal|low|medium|high|xhigh|max|thinking"
# Arena packs more into the bracket than the effort: "(xHigh, Codex Harness)", "(Thinking 16K, ...)".
BRACKET = re.compile(rf"\s*\(\s*({EFFORTS})\b[^)]*\)\s*$", re.I)
SUFFIX = re.compile(rf"[-_]({EFFORTS})$", re.I)


def split_effort(name):
    for rx in (BRACKET, SUFFIX):
        m = rx.search(name)
        if m:
            return name[:m.start()], m.group(1).lower()
    return name, None


def _forms(name):
    """The whole name first, so a name like "qwen3.8-max" is not read as an effort."""
    out = []
    for n in (name, split_effort(name)[0]):
        for f in (norm_id(n), norm_id(n.rsplit("/", 1)[-1])):
            if f not in out:
                out.append(f)
    return out


def canonical(source, name, aliases):
    for form in _forms(name):
        for mid, e in aliases.items():
            if form in {norm_id(n) for n in e.get("names", {}).get(source, [])}:
                return mid
        for mid, e in aliases.items():
            if any(re.search(p, form) for p in e.get("patterns", {}).get(source, [])):
                return mid
        if form in aliases:
            return form
    return None
