"""Read a vendor's model list and compare it with the models our notes cover."""
import re

from .sections import sections


def norm_id(s):
    s = re.sub(r"[\s_./]+", "-", s.strip().lower())
    return re.sub(r"-+", "-", s).strip("-")


def parse(text, spec):
    scope = text
    if spec.get("section"):
        want = spec["section"].lower()
        scope = "\n".join(f"{t}\n{b}" for _, t, b in sections(text) if want in t.lower())
    rx = re.compile(spec["model_regex"], re.I)
    exclude = {norm_id(x) for x in spec.get("exclude", [])}
    out = []
    for m in rx.finditer(scope):
        mid = norm_id(m.group(0))
        if mid not in out and mid not in exclude:
            out.append(mid)
    return out


def flagship(models, spec):
    if not models:
        return None
    rule = spec.get("flagship", "first")
    if rule == "first":
        return models[0]
    rx = re.compile(rule, re.I)
    return next((m for m in models if rx.fullmatch(m)), models[0])


def compare(models, note_ids):
    return [m for m in models if m not in note_ids], [m for m in note_ids if m not in models]


def match_model(query, ids):
    q = norm_id(query)
    if q in ids:
        return q
    hits = [i for i in ids if i.endswith("-" + q)]
    if len(hits) == 1:
        return hits[0]
    toks = q.split("-")
    hits = [i for i in ids if all(t in i.split("-") for t in toks)]
    return hits[0] if len(hits) == 1 else None
