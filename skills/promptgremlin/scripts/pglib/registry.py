"""sources.json: load, save, resolve a user's target name, and validate entries."""
import json
import re
from pathlib import Path

from . import lineup as L
from . import notes as N

FORMATS = {"md", "md.txt", "text", "json-helpcenter", "html", "github-api", "none"}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(reg, path):
    Path(path).write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")


def note_ids_by_key(notes_dir, reg):
    out = {}
    for key in reg:
        p = Path(notes_dir) / f"{key}.md"
        out[key] = N.model_ids(N.load(p)) if p.exists() else []
    return out


def resolve(name, reg, ids_by_key):
    """Target key, or (family key, model id) when the name is a model."""
    q = L.norm_id(name)
    for key, e in reg.items():
        if q == key or q in (L.norm_id(a) for a in e.get("aliases", [])):
            return key, None
    for key, ids in ids_by_key.items():
        m = L.match_model(q, ids)
        if m:
            return key, m
    for key, e in reg.items():
        for a in [key] + e.get("aliases", []):
            if q.startswith(L.norm_id(a) + "-"):
                return key, q
    raise KeyError(name)


def validate(reg):
    errs = []
    for key, e in reg.items():
        if e.get("kind") not in ("family", "tool"):
            errs.append(f"{key}: kind must be family or tool")
        for u in e.get("uses", []):
            if u not in reg:
                errs.append(f"{key}: uses unknown target {u}")
        lus = e.get("lineup") or []
        if isinstance(lus, dict):
            lus = [lus]
        for i, lu in enumerate(lus):
            tag = f"{key}: lineup" if len(lus) == 1 else f"{key}: lineup[{i}]"
            for field in ("url", "format", "model_regex"):
                if field not in lu:
                    errs.append(f"{tag} missing {field}")
            try:
                re.compile(lu.get("model_regex", ""))
            except re.error as x:
                errs.append(f"{tag} regex {x}")
        if not e.get("sources"):
            errs.append(f"{key}: no sources")
        for name, s in e.get("sources", {}).items():
            fmt = s.get("format")
            if fmt not in FORMATS:
                errs.append(f"{key}.{name}: bad format {fmt}")
            if fmt != "none" and "url" not in s and "url_pattern" not in s:
                errs.append(f"{key}.{name}: needs url or url_pattern")
    return errs
