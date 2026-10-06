from pglib import registry

REG = {"anthropic": {"kind": "family", "aliases": ["claude"]},
       "openai": {"kind": "family", "aliases": ["gpt", "chatgpt"]},
       "claude-code": {"kind": "tool", "uses": ["anthropic"]}}
IDS = {"anthropic": ["claude-opus-5-5"], "openai": ["gpt-6-astra"], "claude-code": []}


def test_resolve_key_and_alias():
    assert registry.resolve("Claude Code", REG, IDS) == ("claude-code", None)
    assert registry.resolve("ChatGPT", REG, IDS) == ("openai", None)


def test_resolve_model_name():
    assert registry.resolve("opus 5.5", REG, IDS) == ("anthropic", "claude-opus-5-5")


def test_resolve_unreleased_model_by_alias_prefix():
    assert registry.resolve("gpt-6.2", REG, IDS) == ("openai", "gpt-6-2")


def test_resolve_unknown_raises():
    try:
        registry.resolve("dall-e", REG, IDS)
    except KeyError:
        return
    raise AssertionError("expected KeyError")


def test_validate_reports_problems():
    errs = registry.validate({
        "x": {"kind": "family", "uses": ["nope"],
              "lineup": {"url": "u", "format": "md", "model_regex": "("},
              "sources": {"a": {"format": "pdf"}, "b": {"format": "md"}}},
        "y": {"kind": "gadget"}})
    text = "\n".join(errs)
    for needle in ("x: uses unknown target nope", "x: lineup regex", "x.a: bad format pdf",
                   "x.b: needs url or url_pattern", "y: kind", "y: no sources"):
        assert needle in text, needle


def test_validate_accepts_good_entry():
    assert registry.validate({"z": {"kind": "tool", "sources": {
        "a": {"url": "https://x/a.md", "format": "md"}}}}) == []


def test_validate_accepts_lineup_list_and_flags_bad_spec():
    good = {"url": "u", "format": "md", "model_regex": "x"}
    base = {"kind": "tool", "sources": {"a": {"url": "https://x/a.md", "format": "md"}}}
    assert registry.validate({"z": {**base, "lineup": [good, good]}}) == []
    errs = registry.validate({"z": {**base, "lineup": [good, {"url": "u", "format": "md",
                                                              "model_regex": "("}]}})
    assert any(e.startswith("z: lineup[1] regex") for e in errs)
    errs = registry.validate({"z": {**base, "lineup": [good, {"url": "u"}]}})
    assert "z: lineup[1] missing format" in errs
