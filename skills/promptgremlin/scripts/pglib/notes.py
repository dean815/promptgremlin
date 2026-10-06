"""Notes files: frontmatter + '## All models' / '## Effort' / '## <model-id>' blocks."""
import datetime as dt
import re
from pathlib import Path
from typing import NamedTuple

H2 = re.compile(r"^## (.+?)\s*$")
RESERVED = ("All models", "Effort")


class Notes(NamedTuple):
    meta: dict
    blocks: dict


def _value(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip() for x in v[1:-1].split(",") if x.strip()]
    return v


def parse(text):
    meta, body = {}, text
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = _value(v)
            body = text[end + 4:]
    blocks, title, buf = {}, None, []
    for line in body.splitlines():
        m = H2.match(line)
        if m:
            if title is not None:
                blocks[title] = "\n".join(buf).strip()
            title, buf = m.group(1), []
        elif title is not None:
            buf.append(line)
    if title is not None:
        blocks[title] = "\n".join(buf).strip()
    return Notes(meta, blocks)


def load(path):
    return parse(Path(path).read_text(encoding="utf-8"))


def model_ids(n):
    return [t for t in n.blocks if t not in RESERVED]


def is_stale(n, today, days=90):
    lv = n.meta.get("last_verified")
    if not lv:
        return True
    return (today - dt.date.fromisoformat(lv)).days > days


def set_last_verified(n, iso_date):
    return Notes({**n.meta, "last_verified": iso_date}, dict(n.blocks))


def remove_blocks(n, titles):
    removed = {t: n.blocks[t] for t in titles if t in n.blocks}
    kept = {t: b for t, b in n.blocks.items() if t not in removed}
    return Notes(dict(n.meta), kept), removed


def render(n):
    fm = "\n".join(f"{k}: [{', '.join(v)}]" if isinstance(v, list) else f"{k}: {v}"
                   for k, v in n.meta.items())
    body = "\n\n".join(f"## {t}\n{b}" for t, b in n.blocks.items())
    return f"---\n{fm}\n---\n{body}\n"


def save(n, path):
    Path(path).write_text(render(n), encoding="utf-8")
